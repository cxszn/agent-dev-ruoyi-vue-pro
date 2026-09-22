# 启动、版本与模块装配

源码核验日：2026-09-22。以下行号定位资料基线；换工作树后按符号重新检索。[共享来源索引](../../../references/source-index.md)记录基线差异。

## 入口与事实

| 入口 | 核验点 |
| --- | --- |
| `pom.xml:10`、`:43`、`:45`、`:52` | 默认编译 dependencies/framework/server/system/infra；revision 为 `2026.08-jdk25-SNAPSHOT`，Java 为 25，根 Spring Boot 属性为 4.1.0。其它业务模块被注释。 |
| `yudao-dependencies/pom.xml:20`、`:27` | BOM 声明 Spring Boot 4.1.1 与 MyBatis Plus 3.5.17；与根 POM不一致，不能挑一个版本当成完整依赖结论。 |
| `yudao-server/pom.xml:23` | 服务直接依赖 system、infra；后面的业务依赖多处于注释中。 |
| `yudao-server/src/main/java/cn/iocoder/yudao/server/YudaoServerApplication.java:16` | 扫描 `${yudao.info.base-package}.server` 和 `.module`。 |
| `yudao-server/src/main/resources/application.yaml:5`、`:265` | 默认 profile 为 local；基础包由 `yudao.info.base-package` 提供。查看具体 profile 时只提取相关键，避免输出凭据。 |
| `yudao-ui/` 下各工程的 `README.md` | 核验材料主要提供独立前端仓库入口；少量 Vue3示例不等于完整前端工程。 |

## 按任务执行

1. 用当前 POM确认版本及有效模块；用 `java -version`、`mvn -version`核对实际工具链。IDE与命令行可能使用不同 JDK。
2. 依赖版本有分歧时，检查 Maven有效模型，例如在当前项目执行 `mvn help:effective-pom`并定位受影响依赖、插件；记录解析失败和实际源，不把失败结果推成已确认版本。
3. 找实际启用的 `application-<profile>.yaml`、数据源类型、SQL方言、Redis与任务/MQ等组件。将“依赖未启动”“连接目标错误”“缺表”“Bean未装配”分别追到根因。
4. 启用已有模块时，同时核对根 `<modules>`、`yudao-server`依赖，以及目标模块引用的其它模块。多层模块以其自身 POM为准，例如聚合目录与可运行依赖的 artifactId未必相同。
5. 迁移或改包时，先搜索旧包名和 Maven坐标的使用位置，再检查 Java包路径、启动扫描、`yudao.info.base-package`、生成器配置和测试导入。不能只重命名目录。
6. 启动前先明确数据库初始化策略：新建开发数据库可按对应方言建库；已有数据库走增量结构核对，不直接全量导入基础 SQL。
7. 前端按当前 `package.json`的 engines、packageManager、scripts和锁文件执行。核对后端基础 URL、代理、API前缀、租户请求参数；不能把 Vue2、Element Plus、Vben或UniApp启动方式互用。

## 验收

- 指定模块实际参加构建；服务依赖已包含其实现；启动日志证实应用就绪且相关 Bean/接口存在。
- 登录和一个目标模块的只读接口有实际响应；需要前端时在真实浏览器核对 URL、页面、请求结果。
- 模块新增数据库或运行组件需求有明确记录。编译通过不能代替服务启动，服务启动不能代替业务链验收。
- 记录工具链与有效版本；未运行的服务、数据库、前端验证明确列为未验证。

本流程是源码核验的工程步骤。[后端快速启动](https://doc.iocoder.cn/quick-start/)在本任务先前轮次读过；[迁移模块](https://doc.iocoder.cn/migrate-module/)为源码中的官方链接，正文待复核。本轮未重新读取官网正文；文档入口与可用性见共享索引。
