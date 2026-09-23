# 菜单、按钮与角色入口

生成菜单 SQL、拟定菜单 API 请求或诊断页面不可见时读取。先读取当前 `system_menu` DDL、`MenuController`/`MenuSaveVO`、生成的 SQL 与前端路由加载器。导入来源的固定 ID、固定父菜单和刷新按钮不能代表目标系统现状。

## 形成可核对的菜单计划

1. 查询完整父菜单候选，核对路径、类型、启用状态及层级；同名结果不能用 `LIMIT 1` 随意选取。先复用已有目录/页面/按钮；菜单名称相同不证明权限或组件相同。
2. 记录每个拟新增/变更节点：父节点、类型、路由 path、组件 component、组件名 componentName、权限 permission、排序和可见性。
3. 与生成的 Controller `@PreAuthorize`、Web `v-hasPermi` 或移动端 `hasAccessByCodes` 逐项核对。当前权限前缀来自 `CodegenEngine.initBindingMap`，不能直接套表名或页面目录。
4. 把角色与租户套餐所需的菜单差异列为独立计划；授权给谁、哪些节点必须明确。`yudao-system` 提供[查询与授权后应用流程](../../yudao-system/SKILL.md)。生成菜单不默认给 admin 或任意用户授权。

## 当前字段语义

| 字段 | 已核验语义与检查 |
| --- | --- |
| type | `MenuTypeEnum`：目录 1、菜单 2、按钮 3。 |
| id / parentId | 基线 MySQL `id` 为 bigint AUTO_INCREMENT；父节点来自查询结果。目录可复用，不能省略目录插入却继续引用未创建 ID。 |
| path | 菜单/目录路由地址；应与当前路由约定匹配，不等同于组件文件路径。 |
| component / componentName | 页面组件路径通常相对 `src/views` 且不带 `.vue`，组件名核对 defineOptions/缓存；目录/按钮不需要页面组件。当前模板对按钮使用空字符串，不强制改为 NULL。 |
| permission | 页面通常为空，按钮与真实后端动作完全一致；查询/详情共用 query，删除/批量删除共用 delete。只有功能存在才添加相应导入/导出权限。 |
| status | CommonStatusEnum：0 启用、1 停用；与 visible 是否展示是两种含义。 |
| visible / keepAlive / alwaysShow | API Boolean 对应 SQL bit 字段，按页面需求显式决定；UI/API 默认值需另核对。 |

当前 `system_menu` 没有 `tenant_id`；菜单全局存储仍受租户套餐与角色菜单范围约束，不能据此推断所有租户都能使用。SQL 的 `component` 长度为 255，而当前 `MenuSaveVO` 的 `@Size(max=200)` 更严格，走 API 时应按实际校验上限处理。

## SQL 草稿与 API 选择

优先采用当前 `codegen/sql/sql.vm` 输出，结合实际 DDL 审查。MySQL/OceanBase 分支通过自增 ID 与同一连接的 `LAST_INSERT_ID()` 关联按钮；其它数据库分别使用其序列/identity 语法。不将毫秒时间戳拼接后缀当作必然唯一的跨库 ID 方案。

草稿示意（方括号表示必须先解析的业务值，不能直接执行）：

```sql
INSERT INTO system_menu
  (name, permission, type, sort, parent_id, path, icon, component, status, component_name)
VALUES
  ('[功能名称]', '', 2, 0, [已确认父菜单ID], '[路由名]', '', '[模块/业务目录/index]', 0, '[组件名]');
SET @page_menu_id = LAST_INSERT_ID();
INSERT INTO system_menu
  (name, permission, type, sort, parent_id, path, icon, component, status)
VALUES
  ('[功能名称]查询', '[实际权限前缀]:query', 3, 1, @page_menu_id, '', '', '', 0);
```

添加实际存在的 create/update/delete/export/import 节点时复用同一个页面 ID；已有页面则使用查询到的 ID，不把旧连接的 `LAST_INSERT_ID()` 当作查询结果。生成脚本需转义来自表注释/名称的 SQL 字符串、检查目标 DDL 和已有记录，并给出重跑策略。不要假定基础表有可支持 upsert 的业务唯一索引。

API 创建页面在当前源码为 POST `/system/menu/create`，由 `MenuSaveVO` 接收；修改为 PUT `/system/menu/update`。请求先查实际版本、前缀与权限，字段采用 camelCase，SQL 采用 snake_case。来源提供的地址仅能辅助定位，不能跳过部署版本核验。

执行 SQL、创建菜单、分配角色各自遵循用户已授权的目标和范围；本地数据库地址不形成自动执行许可。使用已有安全凭证机制，不把密码放进命令参数、脚本或交付日志。更改运行时配置、管理员身份或验证码不属于代码生成的隐含操作。

## 应用后的验收

仅在应用已获授权并实际完成后，读取新增节点、检查父子关系与角色/套餐范围，再用实际登录态核对菜单、组件、按钮和 API。当前 `MenuController` 没有来源所称的“刷新菜单缓存”接口；检查目标版本的服务缓存失效、登录菜单刷新与前端功能后再操作，不编造固定按钮或强制重启流程。

页面不可见沿着节点存在与启用 → 父节点 → 角色/套餐范围 → 登录权限响应 → 动态路由/组件文件 → 按钮与后端权限检查，逐层定位。SQL 文件已生成、HTTP 创建成功均不等于用户已能使用。

源码入口（相对后端根）：`sql/mysql/ruoyi-vue-pro.sql:2300`；`yudao-module-infra/src/main/resources/codegen/sql/sql.vm:28`；`yudao-module-system/src/main/java/cn/iocoder/yudao/module/system/controller/admin/permission/MenuController.java:32` 与同目录 `vo/menu/MenuSaveVO.java:12`；`yudao-module-system/src/main/java/cn/iocoder/yudao/module/system/enums/permission/MenuTypeEnum.java`。
