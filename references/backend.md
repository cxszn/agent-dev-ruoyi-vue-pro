# 后端定位与实现模式

适用范围：本索引所列的 `2026.08-jdk25-SNAPSHOT` 源码基线；使用时核对当前项目。

## 从请求追踪到数据

1. 从 `yudao-server/pom.xml` 和根 `pom.xml` 确认模块确实启用。目录存在而 POM 注释掉时，先检查模块开启文档、依赖与配置影响。
2. 在 `yudao-module-<domain>/src/main/java/cn/iocoder/yudao/module/<domain>/` 找 `controller/admin` 或 `controller/app`，接口出入参在相应 `vo`；`WebProperties.java:21-24` 将两类包映射到 `/app-api`、`/admin-api`。
3. 顺 `service` → `dal/dataobject` → `dal/mysql` 或 `dal/redis` 找职责。跨模块公共契约看 `api`/DTO；遇到双向 Maven 依赖再设计独立 API 模块。
4. 修改请求与结果时保持 VO、Service、Mapper、文档/调用方一致；不直接把 DO 当作接口公共契约的默认做法。[官方项目结构](https://doc.iocoder.cn/project-intro/)解释了 Admin/App 的不同响应范围。

示例：`UserController.java:53-107` 用 `@Valid`、`@PreAuthorize` 与 `CommonResult`；`AdminUserServiceImpl.java:114,321` 调 Mapper；`AdminUserMapper.java:13-39` 继承 `BaseMapperX` 并用 `LambdaQueryWrapperX`。这是找相似实现的入口，不是所有模块的强制样板。

## 权限与多租户检查

- 按钮/菜单缺失：核 `system_menu` → `system_role_menu`/角色分配 → `AuthController.getPermissionInfo()` → 前端动态路由/权限指令 → Controller `@PreAuthorize`。`MenuController.java:29-97` 管菜单接口，`PermissionServiceImpl.java:143-158` 处理角色菜单关联。
- 前端按钮隐藏仅改善体验，后端权限最终生效；[Vue3 菜单路由文档](https://doc.iocoder.cn/vue3/route/)对此有明确说明。
- 多租户涉及 `yudao-framework/yudao-spring-boot-starter-biz-tenant` 的上下文、过滤器和 DB 拦截器；数据权限涉及 `yudao-spring-boot-starter-biz-data-permission`。修改查询时检查当前模块是否接入、规则是否覆盖新表与异步路径。

## 验证选择

- 业务逻辑：找相邻 `src/test` 用例，针对受影响模块运行目标测试。
- 依赖与 Boot 4 行为：先解析有效 POM；根 POM 4.1.0 和 BOM 4.1.1 有差异，记录实际解析结果。
- API/权限：核实际权限字符串、请求前缀、角色权限、无权响应与有权响应。线上数据库或权限写入需另按任务授权。
