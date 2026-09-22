# 认证、权限与租户隔离

源码核验日：2026-09-22。本页依据源码及测试阅读，未声称已在线获取受限文档正文。符号与行号需在当前工作树复核。

## 查找入口

下表 `S` 为 `yudao-module-system/src/main/java/cn/iocoder/yudao/module/system/`；`F` 为 `yudao-framework/`。

| 链路 | 相对路径与定位 |
| --- | --- |
| Token到身份 | `F/yudao-spring-boot-starter-security/src/main/java/cn/iocoder/yudao/framework/security/core/filter/TokenAuthenticationFilter.java:42`、`:71`：doFilterInternal、buildLoginUserByToken；通过OAuth2TokenCommonApi检查token，核对admin/app用户类型。 |
| 登录/免登录端点 | `F/yudao-spring-boot-starter-security/src/main/java/cn/iocoder/yudao/framework/security/config/YudaoWebSecurityConfigurerAdapter.java:125`：收集PermitAll、配置放行路径，最后authenticated；token过滤器在认证链内。 |
| 功能权限 | `S/service/permission/PermissionServiceImpl.java:63`、`:141`：hasAnyPermissions、assignRoleMenu；`S/controller/admin/auth/AuthController.java:96`：getPermissionInfo。 |
| 部门数据权限注册 | `S/framework/datapermission/config/DataPermissionConfiguration.java:18`：为AdminUserDO、DeptDO注册部门列，并给AdminUserDO注册自身ID列。新业务表需按需求注册自己的列。 |
| 部门行过滤 | `F/yudao-spring-boot-starter-biz-data-permission/src/main/java/cn/iocoder/yudao/framework/datapermission/core/rule/dept/DeptDataPermissionRule.java:91`、`:179`：getExpression、addDeptColumn、addUserColumn。 |
| 租户上下文 | `F/yudao-spring-boot-starter-biz-tenant/src/main/java/cn/iocoder/yudao/framework/tenant/core/web/TenantContextWebFilter.java:22`：读请求tenant-id并在finally清理。 |
| 租户访问控制 | `F/yudao-spring-boot-starter-biz-tenant/src/main/java/cn/iocoder/yudao/framework/tenant/core/security/TenantSecurityWebFilter.java:65`：校验登录租户与请求租户、缺失租户及租户有效性。 |
| 租户SQL过滤 | `F/yudao-spring-boot-starter-biz-tenant/src/main/java/cn/iocoder/yudao/framework/tenant/core/db/TenantDatabaseInterceptor.java:41`、`:46`、`:68`：getTenantId、ignoreTable、computeIgnoreTable。 |

## 决策与操作

1. **401或登录异常**：记录请求路径、用户类型、token来源和错误码；沿TokenAuthenticationFilter到OAuth2TokenServiceImpl核查失效/刷新/注销。日志与报告不写原始token。mock登录有独立开关，不能用开启mock的验收替代真实认证。
2. **接口403或菜单缺失**：对齐角色授予、菜单权限字符串、Controller的 `@PreAuthorize("@ss.hasPermission(...)")`、getPermissionInfo返回及前端权限入口。菜单显示仅是前端条件，仍要验证直接请求被后端正确拒绝。
3. **数据太多或为空**：先确认规则适用的表、列、用户类型与角色数据范围，再查看实际SQL/Mapper。DeptDataPermissionRule只对已登录的ADMIN类型处理；无登录用户或其它用户类型返回不追加条件，业务访问控制仍需独立成立。
4. **部门与本人组合**：当前规则将部门和本人条件以OR组合；ALL返回 `null`，不追加范围条件。没有可见部门且不能看自己时，源码 `DeptDataPermissionRule.java:124` 返回 `new EqualsTo(null, null)`，生成 `WHERE null = null` 使结果为空。区分“没有过滤条件”和“过滤后无记录”，也不要仅为“查不出数据”移除规则。
5. **租户异常**：请求tenant-id可能由登录用户补全；显式请求租户不匹配会被拒绝。免登录与忽略租户是两个不同决策，分别检查PermitAll和TenantIgnore/ignoreUrls。
6. **表隔离**：当前TenantDatabaseInterceptor对找不到MyBatis TableInfo的表默认忽略；继承TenantBaseDO的表不忽略，普通映射实体由TenantIgnore决定。自定义SQL、外部表或新增Mapper必须检查实际隔离，不只看是否存在tenant_id列。
7. **异步/任务隔离**：从TenantUtils、TenantJobAspect及消息传递入口确认上下文传播与清理；线程上下文不能假设自动覆盖所有调度或MQ链路。新增忽略范围需描述具体原因和最小作用域。

## 可复用测试与验收

- `yudao-module-system/src/test/java/cn/iocoder/yudao/module/system/service/permission/PermissionServiceTest.java:61`、`:83`、`:130`：超级管理员、普通角色授权及角色菜单分配；同级oauth2目录含OAuth2TokenServiceImplTest。
- `yudao-framework/yudao-spring-boot-starter-biz-data-permission/src/test/java/cn/iocoder/yudao/framework/datapermission/core/rule/dept/DeptDataPermissionRuleTest.java:53`、`:111`、`:210`：无登录、无可见数据、部门与自身组合；按改动补表别名或业务范围案例。
- 至少用两个有不同范围的身份验证列表、详情和修改入口：允许的记录成功，越权记录被拒绝或不可见；查询参数、导出和批量接口遵循同一范围。
- 涉及租户时使用不同主键、相同业务标识的两租户记录，验证按另一租户的记录 ID 查询/修改被拒绝或不可见，并覆盖请求租户不匹配；涉及会员端时增加相同租户不同所有者案例。
- 权限、数据库与浏览器验证分别报告。仅阅读测试、测试通过或管理员页面可见，都不能单独证明完整授权边界。
