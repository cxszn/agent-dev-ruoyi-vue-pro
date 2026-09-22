---
name: yudao-backend
description: 在芋道 ruoyi-vue-pro 中新增或调整 Java Controller、Service、Mapper、模块 API、认证权限与测试时使用。以当前工作树实际启用模块和版本为准。
---

# 芋道后端

先核对根 POM、`yudao-dependencies/pom.xml`、`yudao-server/pom.xml`，再定位业务模块。[已核验源码基线](../../references/source-index.md)只有 `system` 和 `infra` 默认启用，其它目录存在不代表参与编译或启动。

为同类功能先找 Controller、ReqVO/RespVO、Service、DO、Mapper 和测试；具体定位与权限路径见[后端模式](../../references/backend.md)。按现有分层写最小改动，跨模块调用先查看 `api` 契约。涉及 Spring Boot 4、MyBatis Plus 或依赖细节时，核对当前 POM 与对应版本的一手资料。

涉及菜单/按钮时，把权限字符串、Controller `@PreAuthorize`、角色菜单关联、登录返回菜单和前端路由当成一条链验证。涉及租户、数据权限或安全时，追踪实际过滤器、注解和测试，而不是只凭 Controller 注解判断。

以受影响模块的测试、编译及接口验收作为完成证据；记录没运行的验证项。
