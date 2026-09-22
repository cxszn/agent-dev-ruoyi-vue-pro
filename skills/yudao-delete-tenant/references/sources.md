# 来源与版本差异

核验日期：2026-09-22（Asia/Shanghai）。导入来源为用户提供的项目技能 `cxszn_xyyx/.agents/skills/yudao-delete-tenant/SKILL.md`，原文件 SHA-256：`b95617f85dde61162d282298ec86a57c59e1211beb9bf0d8b1159f7b2a610022`。导入后依据源码改写为通用流程，未修改原技能。关键源码指纹见 [source-evidence.json](source-evidence.json)，路径均相对于对应项目根目录。

官方入口：[删除功能（以租户为例）](https://doc.iocoder.cn/delete-code/)。本轮 Chrome 控制连接不可用，未重新核验该页正文；此链接仅为原技能列出的来源入口。下列行为判断由当前源码验证，不将未读取正文当作证据。

适用基线为 POM 声明的 `2026.08-jdk25-SNAPSHOT`、Java 25；根 POM 与 BOM 的 Spring Boot 声明分别为 4.1.0 / 4.1.1，构建行为应以目标项目有效 POM 为准。这里只记录文件基线，不推断提交 SHA。

| 原材料中的约定 | 本次核验与适配 |
| --- | --- |
| 固定删除菜单 ID 1224、1225–1229 等 | 当前 SQL 中这些 ID 属于 MES 采购退货/供应商退货。租户权限实际位于另一组 ID，故移除固定 ID 删除示例，改为权限码与父子关系核对 |
| 保留 `tenant_id` 字段即可低风险移除 | 字段保留不阻止跨租户可见；增加保留一个租户/合并多个租户/新部署的语义决策与冲突检查 |
| `enable=false` 整体关闭多租户 | 此基线类级条件确实存在；限定为该自动配置，仍需查业务显式逻辑、其它装配和目标环境配置 |
| lambda 内 return 直接提到外层 | 增加局部 return、Callable 异常包装、变量作用域、执行次数的保真规则 |
| IoT 租户依赖路径 | 当前基线确认位于 `yudao-module-iot/yudao-module-iot-biz/pom.xml`；其它版本重新搜索 |
| 前端 Vue3 固定目录 | 当前 `yudao-ui/yudao-ui-admin-vue3` 提供 README 仓库链接，不构成完整前端源码；实际改造需目标前端工程 |

进一步定位：框架类位于 `yudao-framework/yudao-spring-boot-starter-biz-tenant/src/main/java/cn/iocoder/yudao/framework/tenant/`，其中 `core/db/TenantDatabaseInterceptor.java` 判断拦截/忽略，`core/db/TenantBaseDO.java` 定义来源字段，`core/util/TenantUtils.java` 定义执行与异常行为，`core/job/TenantJobAspect.java` 定义每租户执行行为。业务示例可查 `yudao-module-system/src/main/java/cn/iocoder/yudao/module/system/service/oauth2/OAuth2TokenServiceImpl.java` 的 `buildUserInfo` 包装调用。

来源更新时先比较关键文件指纹，再读取变动文件及调用方，只更新受影响的流程。菜单种子指纹一致也不证明运行库的 ID 一致；数据库操作始终需要当前库的只读核验结果。
