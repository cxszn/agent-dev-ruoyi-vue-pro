# 改造与验收

## 1. 只读清点

在目标源码根目录运行相应搜索；命中项是审计输入，不是自动删除清单。

```sh
rg -n 'yudao-spring-boot-starter-biz-tenant' -g pom.xml .
rg -n 'TenantUtils|TenantContextHolder|TenantBaseDO|TenantCommonApi|TenantService|TenantDO|@TenantIgnore|@TenantJob' -g '*.java' .
rg -n 'tenant_id|tenantId|tenant-id|visit-tenant-id|yudao\.tenant' -g '*.xml' -g '*.yaml' -g '*.yml' -g '*.sql' -g '*.java' .
```

MySQL 下可先查询租户权限菜单；其它方言按实际语法调整。再根据返回的 `parent_id`、`component` 和页面名称定位父目录、页面和全部子节点，检查其是否混有非租户业务。

```sql
SELECT id, name, permission, parent_id, path, component
FROM system_menu
WHERE permission LIKE 'system:tenant:%'
   OR permission LIKE 'system:tenant-package:%';
```

对已核实的菜单集合查看 `system_role_menu` 关联，并检查租户套餐 `menu_ids` 等引用。实际删除脚本使用本次读取得到的集合，明确行数预期与逻辑删除策略。不能复用其它项目的菜单 ID，也不能按包含 `tenant` 的字符串匹配直接删除所有记录。

## 2. 数据与运行状态

- 先统计各表按 `tenant_id` 的记录数量，检查全局共享表、唯一索引和业务层唯一性检查，确认切换后的账号/角色/组织/编码冲突。
- 若保留一个租户，准备可恢复的筛选迁移或继续隔离其它租户数据的机制；关闭拦截器本身不能保证只读该租户。
- 若合并多个租户，明确权限归属、业务关联与标识冲突的转换规则，并用样本数据验证；不能简单将所有 `tenant_id` 更新成同一值。
- 允许保留 `tenant_id` 作为来源字段，但新增记录的默认值、非空约束、ORM 映射和联合唯一索引必须与新语义一致。
- 租户专属表 `system_tenant` / `system_tenant_package` 何时删除取决于应用兼容顺序；完成备份与恢复验证、确认没有仍运行的引用后再执行授权的迁移。同步维护实际支持方言的初始化 SQL 和测试数据。
- 明确旧登录态、OAuth2 Token、带租户前缀的缓存、在途 MQ 消息和定时任务的转换或失效策略。采用有范围的切换，不将全库缓存清空当作默认操作。

## 3. 后端清理地图

下列路径以本技能来源基线为例，实际项目先搜索确认。

| 范围 | 相对路径或定位词 | 处理要点 |
| --- | --- | --- |
| 租户业务 | `yudao-module-system/src/main/java/cn/iocoder/yudao/module/system/` 内 `controller/admin/tenant`、`controller/app/tenant`、`service/tenant`、`dal/dataobject/tenant`、`dal/mysql/tenant`、`convert/tenant`、`api/tenant` | 沿调用关系移除专属接口、VO、服务、DAO；保留其它模块依赖的能力或先改写调用 |
| 租户 API | `yudao-framework/yudao-common/src/main/java/cn/iocoder/yudao/framework/common/biz/system/tenant/TenantCommonApi.java` | 先处理所有消费者 |
| 框架 | `yudao-framework/yudao-spring-boot-starter-biz-tenant`、`yudao-framework/pom.xml`、`yudao-dependencies/pom.xml` | 删除模块时同步聚合与依赖管理，复核所有实际消费者 |
| IoT 消费者 | `yudao-module-iot/yudao-module-iot-biz/pom.xml` | 当前基线是多子模块结构，不能套用扁平路径 |
| 测试 | `yudao-module-system/src/test/java/cn/iocoder/yudao/module/system/service/tenant` | 专属测试随功能移除；非租户业务测试保留并更新上下文 |
| 配置 | `yudao-server/src/main/resources/application.yaml` 的 `yudao.tenant`，以及实际生效的 profile/外部配置 | 核对忽略 URL、表、缓存与访问租户配置，查明覆盖关系 |

### TenantUtils 的行为保护

先区分调用属于被删除的租户专属业务，还是应保留的其它业务。以下示例只演示后者的改写原则。

```java
// 原包装中的条件 return 仅退出 lambda。
TenantUtils.execute(tenantId, () -> {
    if (skip) return;
    sendNotice();
});
writeAudit();

// 展开后仍须执行后续审计，不能把上面的 return 原样提到外层。
if (!skip) {
    sendNotice();
}
writeAudit();
```

`Callable<V>` 形式要保留赋值或返回结果，并检查调用处的异常契约：本基线包装器捕获 `Exception` 后抛出 `RuntimeException`，展开代码可能引入受检异常或改变异常类型。若调用位于循环或多分支中，逐项验证作用域、执行次数和控制流；不要用字符串批量替换 lambda。`addTenantHeader` 是否删除由外部服务契约决定。

移除 `@TenantJob` 后原先按每个租户调用的任务可能变为一次读取全部数据，要重新验证查询范围、批处理量、幂等键及失败重试；保留任务方法体不等于保持原行为。`TenantContextHolder` 的读取如果参与条件、归属字段或业务参数，需要按已确认的单租户语义改写。

## 4. 配置关闭模式

本基线 `YudaoTenantAutoConfiguration` 类级声明 `@ConditionalOnProperty(prefix = "yudao.tenant", value = "enable", matchIfMissing = true)`，`false` 会阻止这个自动配置的装配。缺省则开启。

这只能证明当前自动配置的条件。目标项目可能另有 `@Import`、`@Component`、独立自动配置、外部配置覆盖或显式租户判断；先查装配来源，再通过条件报告/启动验收确认。关闭隔离的模式同样需要第 2 节的数据可见性决策，不因改动只有一个配置项就跳过。

## 5. 前端与验证

定位实际前端仓库的 `package.json`、锁文件和源码后，搜索 `tenant`、`tenantId`、`tenant-id`、`visit-tenant-id`、租户管理/套餐菜单、租户选择/切换、请求封装和本地存储。Vue3 候选路径如 `src/views/system/tenant`、`src/api/system/tenant` 必须经文件核对后采用；Vben/Vue2 不继承这些路径。只有仓库链接或 README 时，标记前端未覆盖。

根据当前 POM 的启用模块选择最小编译和业务测试；不要以 `-DskipTests` 的编译成功代替测试通过。至少保留以下场景的可核查结果：

| 场景 | 期望依据 |
| --- | --- |
| 两个租户拥有同名账号/编码 | 登录解析和唯一性符合已确认的保留/合并规则 |
| 列表、详情、导出、后台任务 | 访问同一设计范围，未混入应隔离数据 |
| 包装内包含副作用、返回值或局部 return | 业务执行次数、结果与异常契约保持预期 |
| 旧 Token/缓存/MQ 消息 | 符合转换或失效策略，没有遗留身份串用 |
| 前端登录、动态菜单与请求头 | 真实页面和网络请求符合所选模式 |

最后复查引用与依赖。允许有明确用途的来源字段或外部租户协议残留，说明原因；不把全仓库 `tenant` 零命中作为验收目标。
