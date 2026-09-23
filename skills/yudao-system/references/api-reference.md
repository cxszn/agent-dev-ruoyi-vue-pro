# API 契约与菜单关系

核对样本：`ruoyi-vue-pro` 的 `2026.08-jdk25-SNAPSHOT`。以下路径均相对于该源码根目录；改包项目应通过类名重新定位。调用前再核对本次项目的 Controller、VO、权限与 API 前缀，不将样本当作所有分支的承诺。

管理端系统源码位于 `yudao-module-system/src/main/java/cn/iocoder/yudao/module/system/`，下文类路径相对这个目录。该样本不是 `yudao-cloud` 的 `-api/-server` 模块布局。

## 已封装的接口

| 用途 | 方法及路径（相对管理端前缀） | 权限 | 当前响应 |
|---|---|---|---|
| 角色查询 | GET `/system/role/page` | `system:role:query` | `PageResult<RoleRespVO>` |
| 用户查询 | GET `/system/user/page` | `system:user:query` | `PageResult<UserRespVO>` |
| 部门查询 | GET `/system/dept/list` | `system:dept:query` | 扁平部门列表 |
| 岗位查询 | GET `/system/post/page` | `system:post:query` | 分页岗位列表 |
| 字典类型查询 | GET `/system/dict-type/page` | `system:dict:query` | 分页字典类型列表 |
| 字典项查询 | GET `/system/dict-data/page` | `system:dict:query` | 分页字典项列表，可传 `dictType` |
| 菜单查询 | GET `/system/menu/list` | `system:menu:query` | 扁平菜单列表，不是登录菜单树 |
| 租户查询 | GET `/system/tenant/page` | `system:tenant:query` | 分页租户列表 |
| 角色创建 | POST `/system/role/create` | `system:role:create` | 新记录 ID |
| 字典类型创建 | POST `/system/dict-type/create` | `system:dict:create` | 新记录 ID |
| 字典项创建 | POST `/system/dict-data/create` | `system:dict:create` | 新记录 ID |
| 菜单创建 | POST `/system/menu/create` | `system:menu:create` | 新记录 ID |

响应外层为 `CommonResult`：整数 `code=0` 表示业务成功，业务值在 `data`；分页值含 `list` 与 `total`。HTTP 成功不能代替业务码检查。分页成功、完整且身份明确后才可判定不存在；任何异常都不代表空数据。

框架 `NumberSerializer` 会将达到 JavaScript 安全整数边界的 Long 输出为十进制字符串。工具接受正整数及十进制字符串形式的记录 ID，并将 `id/parentId` 规范为 Python 整数以无精度损失地比较；创建响应也遵循此规则，不能将合法大 ID 误判为失败。

源码定位：`controller/admin/permission/{Role,Menu}Controller.java`、`controller/admin/user/UserController.java`、`controller/admin/dept/{Dept,Post}Controller.java`、`controller/admin/dict/{DictType,DictData}Controller.java`、`controller/admin/tenant/TenantController.java`。

## 字段与查重

| 记录 | 请求 VO | 支持的创建字段 / 身份 |
|---|---|---|
| 角色 | `controller/admin/permission/vo/role/RoleSaveReqVO.java` | `name, code, sort, status, remark`；按 `code` 查重，并核对名称 |
| 字典类型 | `controller/admin/dict/vo/type/DictTypeSaveReqVO.java` | `name, type, status, remark`；按 `type` 查重 |
| 字典项 | `controller/admin/dict/vo/data/DictDataSaveReqVO.java` | `sort, label, value, dictType, status, colorType, cssClass, remark`；同类型按 `value` 查重，同时核对 `label` |
| 菜单 | `controller/admin/permission/vo/menu/MenuSaveVO.java` | `name, type, sort, parentId, permission, path, icon, component, componentName, status, visible, keepAlive, alwaysShow`；同父节点按 `name` 查重 |

`RoleSaveReqVO` 没有 `type/dataScope/dataScopeDeptIds`。`service/permission/RoleServiceImpl.java#createRole` 在服务层设为自定义角色且数据范围 ALL；请求体塞入 `dataScope` 不会按预期限定权限。数据范围变更应使用单独接口并取得对应授权。

`DictDataController#getSimpleDictDataList` 仅返回启用项；`dal/mysql/dict/DictDataMapper.java#selectPage` 按 `dictType` 精确过滤。主数据存在性判断使用分页接口且不筛掉禁用记录。`UserPageReqVO` 支持用户名等字段，但没有 `nickname`；工具完整查询后进行昵称筛选。

`service/dict/DictDataServiceImpl.java#validateDictTypeExists` 要求新增字典项的类型已启用；向停用类型补项在预查时中止，避免新建一个停用类型后才发现其条目无法创建。

## 菜单、角色与租户

| 类型 | 值 | 作用 |
|---|---|---|
| 目录 | `1` | 分组和路径前缀 |
| 页面 | `2` | 对应实际 Vue 组件及路由 |
| 按钮 | `3` | 权限标识，不生成页面路由 |

父关系通过 `parentId` 建立，根值为 `0`。`service/permission/MenuServiceImpl.java` 校验父节点存在且为目录/页面、同级名称唯一和组件名唯一；按钮的 `component/componentName/icon/path` 会清空。不要在找不到父节点时自动改挂根目录。

`dal/dataobject/permission/MenuDO.java` 标记 `@TenantIgnore`，菜单定义共享；角色关系与租户套餐仍影响可见范围。创建菜单可能影响共享定义，应在目标授权中明确。管理菜单列表与登录后权限菜单树用途不同。

| 接口 | 作用 | 关键语义 |
|---|---|---|
| GET `/system/auth/get-permission-info` | 登录用户、角色码、权限码、菜单树 | `AuthConvert#buildMenuTree` 移除按钮、按 sort 排序并构建树 |
| GET `/system/permission/list-role-menus?roleId=...` | 查询该角色现有菜单 ID 集合 | 需要 `system:permission:assign-role-menu` |
| POST `/system/permission/assign-role-menu` | `{roleId, menuIds}` | `menuIds` 是目标完整集合，遗漏旧值会撤销其授权 |
| GET `/system/permission/list-user-roles?userId=...` | 查询用户现有角色 ID 集合 | 需要 `system:permission:assign-user-role` |
| POST `/system/permission/assign-user-role` | `{userId, roleIds}` | `roleIds` 是目标完整集合，遗漏旧值会撤销其授权 |
| POST `/system/permission/assign-role-data-scope` | `{roleId, dataScope, dataScopeDeptIds}` | 独立的数据范围权限变更 |

这些权限接口保留为按需参考，未封装成当前 CLI 的可执行动作。其实际实现见 `controller/admin/permission/PermissionController.java` 与 `service/permission/PermissionServiceImpl.java`。当任务明确要求新增授权时，先读取当前完整集合，计算加入后的集合并审查差异；不要将追加需求转为覆盖写入。角色菜单还受租户套餐过滤，写入后须重新查询实际集合。

菜单验收沿着“菜单定义 → 租户套餐与角色菜单 → 用户角色 → 权限信息接口 → 当前前端路由/组件”检查。`MenuServiceImpl` 的创建/修改/删除和权限分配已有相应缓存失效逻辑，不能仅凭来源教程就声称页面一定有“刷新菜单缓存”按钮。检查本次前端的实际 store、路由与刷新方式；当前快照未提供独立前端运行证据。

`tenant-id` 和可选的 `visit-tenant-id` 由任务上下文提供。框架来源位于 `yudao-framework/yudao-spring-boot-starter-biz-tenant` 和 Web 框架工具类，不能从 URL、角色名或数据库示例猜租户。

## 来源声明但未提供的能力

来源文档的能力清单大于其实际 Python 实现。当前工具以 `--help` 为准；以下均不能假装可调用：

- `query_approval_roles/find_or_create_approval_role/create_approval_role_group/add_users_to_approval_role`：来源工具库没有这些函数；当前 system Controller 未找到对应审批角色 API。BPM 的审批人策略需要独立核对，不能直接套用来源的 `candidateGroups/groupType/username` 示例。
- `query_dept_positions`、分类字典 `query-categories`、`query_sql_table_dict`、`query_dict`：来源脚本未实现，当前 system Controller 未提供同名契约。岗位使用已验证的 `PostController`。
- `query-datasources`、`query-quartz-jobs`：来源 CLI 未实现；当前源码实际在 infra 的 `DataSourceConfigController` 和 `JobController`，不在本工具范围。数据源可能含凭证，不得用完整响应输出代替必要字段查询。
- `create-menu/delete-menu/create-role/assign-role-menus/list-role-menus` 等来源教程动作与 `add_menus_to_role/add_users_to_role` 函数不在来源 CLI/工具函数表中。当前版本仅通过 JSON 配置支持创建角色/字典/菜单；更新、删除和权限分配须另按任务实现，不能调用虚构命令。
- 来源描述“自动绑定 admin”与实际 `find_or_create_role` 签名不符；当前实现明确不提供此副作用。

核对了来源脚本 AST、函数表、CLI action_map，以及当前样本 Controller/VO/Service。没有连接真实业务 API、数据库或容器，未验证目标环境权限与前端菜单可见性。
