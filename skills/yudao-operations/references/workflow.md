# 构建、测试、部署与观测

核验日期：2026-09-22。所有路径相对当前 ruoyi-vue-pro 源码根目录；行号为插件基线定位点，更换源码后重新查找符号。以下是代码核读结果，没有执行系统构建、测试或部署。

## 构建与启动

| 定位 | 已核事实 | 对任务的影响 |
| --- | --- | --- |
| `pom.xml:10` | 聚合模块存在启用和注释状态 | `-pl` 选择前确认模块参与 reactor；目录存在不等于会打包 |
| `pom.xml:43` | revision 为 `2026.08-jdk25-SNAPSHOT`，`:45` Java 25 | 检查 `java -version`、`mvn -version` 与 CI/容器运行 JDK |
| `pom.xml:52` 与 `yudao-dependencies/pom.xml:20` | 根配置 Spring Boot 4.1.0，BOM 属性 4.1.1 | 注解处理器与依赖实际版本可能不同；依赖问题核 effective POM 与 dependency tree |
| `pom.xml:80` | 编译器配置 Lombok、MapStruct 等处理器 | 生成代码缺失先查处理器解析和编译器错误，不手写覆盖生成类 |
| `yudao-server/src/main/resources/application.yaml:6` | 默认 profile 为 local | 外部启动参数可覆盖，日志中的实际激活 profile 才能证明运行配置 |
| `yudao-server/Dockerfile:3` | 示例运行镜像为 Java 21 | 与 Java 25 编译目标存在差异，部署前须按目标产物核兼容性并适配 |

根据当前权限在目标工作树或隔离构建目录执行 Maven；构建会生成 target 等内容。处理首次错误后重试对应阶段，不通过关闭处理器、排除依赖或删除测试掩盖根因。若只需 dependency/effective POM，先说明解析可能访问配置的仓库；不要把过往构建成功当作当前环境证据。

## 测试选择

- `yudao-framework/yudao-spring-boot-starter-test/src/main/java/cn/iocoder/yudao/framework/test/core/ut/BaseDbUnitTest.java:24` 创建无 Web 的测试上下文；`:25` 激活 unit-test，`:26` 每个测试后执行 `/sql/clean.sql`。先核模块内 unit-test 数据源和 SQL，不能让清理脚本指向业务库。
- 同目录 `BaseMockitoUnitTest.java`、`BaseRedisUnitTest.java`、`BaseDbAndRedisUnitTest.java` 是不同依赖范围的入口；新增测试沿用目标模块现有基类，不默认所有测试都连接真实 Redis。
- 代表测试 `yudao-module-infra/src/test/java/cn/iocoder/yudao/module/infra/service/job/JobServiceImplTest.java:31` 导入目标 Service，`:38` Mock 调度器，`:69` 断言数据库状态及调度参数。Service 测试覆盖不替代真实调度器验收。

命令按当前 Maven 和模块状态确定。可从根目录使用 `mvn -pl yudao-module-infra -am '-Dtest=JobServiceImplTest' '-Dsurefire.failIfNoSpecifiedTests=false' test` 作为已有用例的定向执行候选；先确认该测试与当前改动相关。这里只允许依赖模块没有同名测试，目标模块仍需有实际测试报告和非零执行数。H2 通过不能推断目标数据库方言、索引或锁行为也通过。

## 部署准备与验收

`script/shell/deploy.sh:12` 使用 development profile，`:29` 备份、`:42` 替换 Jar、`:61` 停服务、`:94` 启动、`:107` 检查健康状态，`:160` 直接调用 deploy。读取该脚本不等于应直接执行；核对目标配置中是否真有 development profile，以及现有服务管理器、路径、权限、备份目录和停止策略。脚本健康检查只判断 HTTP 状态码，验收还需响应内容和任务相关业务请求。

发布前确认目标制品来自哪次已验证源码、运行 JDK、有效 profile、迁移与配置变更、回退制品及恢复条件。授权执行后记录制品校验值、运行进程/容器状态、健康响应和受影响业务场景。失败时按已确认回退边界处理，不能用反复重启代替定位。

## 排障与观测

- 启动失败：从第一条 cause 追到配置绑定、Bean/依赖、数据库/Redis/MQ 连接或 schema；核实际 profile 与外部覆盖项，不直接打印完整配置或连接密钥。
- 请求失败：保存请求路径、状态码、业务错误码、时间和 traceId，关联 Controller → Service → SQL/中间件。仅为复现所需的日志级别做短期调整，并记录恢复方式。
- `yudao-framework/yudao-spring-boot-starter-monitor/src/main/java/cn/iocoder/yudao/framework/tracer/config/YudaoTracerAutoConfiguration.java:28` 控制 tracer 自动配置，`:36` 从 `GlobalOpenTelemetry` 取 tracer，`:50` 注册 TraceFilter；Bean 存在不能证明 exporter 或采集端已接收 span。
- `yudao-framework/yudao-spring-boot-starter-monitor/src/main/java/cn/iocoder/yudao/framework/tracer/config/YudaoMetricsAutoConfiguration.java:18` 控制 metrics 配置，`:22` 添加 application 标签；观察目标指标是否实际产生，不只看配置键。
- `yudao-server/src/main/resources/application-local.yaml:164` 和 `application-dev.yaml:140` 配置 Actuator 路径，其 exposure 包含全部端点；运行环境应核实真实暴露范围与访问控制，调试时避免直接复制示例对公网开放。

证据按实际执行记录：编译/测试报告、有效运行参数、经过脱敏的首因日志、接口结果、监控端实际接收数据。只读诊断无法完成的远端验证应保留为待验证项。
