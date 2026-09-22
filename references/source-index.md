# 来源索引与适用范围

核验日：2026-09-22。资料基线：`2026.08-jdk25-SNAPSHOT`。来源按仓库相对路径、关键文件与 24 个源码/SQL 目录的[SHA-256 清单](source-manifest.json)定位；使用时先核对当前项目的版本与相关实现。

已收录的官网主题导航见[文档分组索引](docs-index.md)，机器可查询记录见[docs-index.json](docs-index.json)。目录标题、已知 URL、正文阅读状态与源码核验是不同证据；本轮 Chrome 连接受阻，保留明确的 URL 待定位和正文未读状态。各专题技能的 `references/workflow.md` 补充了实际源码入口、版本差异和代表测试边界。

## 已核验源码基线

| 范围 | 根目录相对路径及定位 | 已核实事实 |
| --- | --- | --- |
| 顶层版本与模块 | `pom.xml:9-35,43-54` | `revision=2026.08-jdk25-SNAPSHOT`、Java 25、Spring Boot 属性 4.1.0；默认启用 `yudao-dependencies`、`yudao-framework`、`yudao-server`、`yudao-module-system`、`yudao-module-infra`，其余业务模块在顶层 POM 注释中。 |
| BOM | `yudao-dependencies/pom.xml:17-28,101-103` | BOM 自身写 Spring Boot 4.1.1、MyBatis Plus 3.5.17。与顶层 POM 的 Boot 4.1.0 不一致；做依赖变更前需看有效 POM。 |
| 项目说明 | `README.md:28-59,360-408` | 分支定位与技术栈说明；README 的 Boot 4.1.0、MyBatis Plus 3.5.16 与 BOM 声明不完全一致，不能替代 POM。 |
| 运行入口 | `yudao-server/pom.xml:25-52`、`yudao-server/src/main/java/cn/iocoder/yudao/server/YudaoServerApplication.java:16` | 服务聚合 system、infra；入口扫描 server/module 包。 |
| 典型 CRUD | `yudao-module-system/src/main/java/cn/iocoder/yudao/module/system/controller/admin/user/UserController.java:43-107`、`service/user/AdminUserServiceImpl.java:62-114,317-322`、`dal/mysql/user/AdminUserMapper.java:13-39` | Controller 的 VO/校验/权限/`CommonResult` 到 Service、Mapper 的现成路径。 |
| 权限与菜单 | `yudao-module-system/src/main/java/cn/iocoder/yudao/module/system/controller/admin/auth/AuthController.java:96-115`、`service/permission/PermissionServiceImpl.java:143-158,189-200`、`controller/admin/permission/MenuController.java:29-97` | 登录权限信息、角色菜单关联与菜单接口需一起核查。 |
| 数据库 | `sql/mysql/ruoyi-vue-pro.sql:2300,4787,4823,6811`、`sql/tools/convertor.py` | MySQL 基线包含菜单、角色、角色菜单与用户表；其它方言位于 `sql/<方言>/`。 |
| 前端输入 | `yudao-ui/*/README.md`、`yudao-ui/yudao-ui-admin-vue3/src/` | 五个前端目录大多仅有仓库链接；Vue3 目录只有少量 MES 示例，没有 `package.json`，不是完整可构建前端工程。 |
| 测试例子 | `yudao-module-system/src/test/java/cn/iocoder/yudao/module/system/service/user/AdminUserServiceImplTest.java`、`yudao-framework/yudao-spring-boot-starter-test/src/main/java/cn/iocoder/yudao/framework/test/core/ut/BaseDbUnitTest.java:24-27` | 服务测试与数据库测试基类定位。 |

## 官方文档（外部 Chrome 实际核对）

| 主题 | URL | 可用性与用途 |
| --- | --- | --- |
| 前端快速启动 | https://doc.iocoder.cn/quick-start-front/ | 可读；列 Vue3 Element Plus、Vben、Vue2、admin uni-app 等独立前端仓库。 |
| 后端快速启动 | https://doc.iocoder.cn/quick-start/ | 可读；分支、初始化、默认 system/infra 范围。 |
| 项目结构 | https://doc.iocoder.cn/project-intro/ | 可读；Maven 四类模块与 Controller/Service/DAL/API 层。 |
| 表结构变更 | https://doc.iocoder.cn/sql-update/ | 可读；先审 SQL 差异，再选择性执行；全局表数据须单独关注。 |
| Vue3 开发规范 | https://doc.iocoder.cn/vue3/dev-spec/ | 可读；view/API/组件划分，仅适用 Vue3 Element Plus。 |
| Vue3 菜单路由 | https://doc.iocoder.cn/vue3/route/ | 可读；动态菜单、权限指令与后端校验链路。 |
| 新建模块 | https://doc.iocoder.cn/module-new/ | 实际页面为“仅 VIP 可见”；本插件不声称获得正文。 |
| 功能权限 | https://doc.iocoder.cn/resource-permission/ | 实际页面为“仅 VIP 可见”；权限细节以可读文档与源码核查。 |

官网文档是持续更新页，未声明与 `2026.08-jdk25-SNAPSHOT` 同步。页面中示例路径、命令、依赖版本只作为线索；实际工作树优先。`book-to-skill` 技术模式已对 `README.md` 以 plain-text 方法提取，元数据记录为 9 个结构段、约 6K token、无丢弃图像；本插件提炼任务规则与索引，未复制站点全文。
