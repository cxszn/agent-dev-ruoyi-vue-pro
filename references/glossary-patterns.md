# 术语与判断规则

| 术语 | 这里的含义与来源 |
| --- | --- |
| `yudao-dependencies` | Maven BOM，管集中依赖版本；`project-intro` 与 `yudao-dependencies/pom.xml`。 |
| `yudao-framework` | 通用及业务 starter，如 Web、MyBatis、租户、数据权限；`project-intro` 与实际目录。 |
| `yudao-module-xxx` | 业务模块；目录存在和被顶层/server POM 启用是两回事。 |
| `yudao-server` | 运行聚合入口；`yudao-server/pom.xml`、`YudaoServerApplication.java`。 |
| Admin/App Controller | 分别向管理后台和用户端暴露接口，默认 `/admin-api`/`/app-api`；`WebProperties.java:21-24`。 |
| ReqVO/RespVO | 控制器请求/响应契约；与 DO 的持久化职责分开。 |
| DO / Mapper / RedisDAO | 数据对象、数据库映射与 Redis 访问封装；`project-intro`。 |
| API / DTO | 跨模块调用契约；出现环形模块依赖时要重新划定接口边界。 |
| `system_menu` / `system_role_menu` | 菜单记录和角色菜单授权关联；MySQL 初始化脚本与 `PermissionServiceImpl`。 |

## 快速决策

- **新增后端功能**：先找同模块相邻 CRUD 与测试，再按请求、服务、数据、权限、前端调用链补齐；跨模块才考虑 `api`。
- **菜单不可见**：先判定菜单数据、角色授权、接口返回和组件路径哪段断开，再修该段。
- **版本不一致**：从实际 POM 和有效依赖开始；README 与官网用于定位，不作为当前构建的事实替身。
- **只有前端文档**：给出设计与待核路径；需要 `package.json` 和真实运行后才报告构建/页面通过。
- **数据库升级**：先审增量 SQL 与全局数据，再在授权的环境执行；避免用完整初始化脚本替代迁移。
