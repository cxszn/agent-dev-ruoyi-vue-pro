# dev-ruoyi-vue-pro

面向 Codex 的芋道 `ruoyi-vue-pro` 开发插件。提供 19 项任务技能、7 份 Agent 配置模板，以及按官网主题组织的文档导航和源码定位，覆盖从启动、功能开发到迁移与运维的工作流程。

## 使用

在已配置此插件的 Codex 环境中，直接描述芋道任务，或显式调用入口技能：

```text
使用 $dev-ruoyi-vue-pro:yudao-router，检查当前项目的 system 用户分页，并给出修改与验收证据。
```

| 技能 | 适用任务 |
| --- | --- |
| [yudao-router](skills/yudao-router/SKILL.md) | 确认目标项目与任务范围，选择下面的技能 |
| [yudao-bootstrap](skills/yudao-bootstrap/SKILL.md) | 版本、启动环境、模块开启与装配 |
| [yudao-codegen](skills/yudao-codegen/SKILL.md) | 新模块、单表/主子表/树表及移动端代码生成 |
| [yudao-system](skills/yudao-system/SKILL.md) | 系统主数据查询、复用与明确授权后的创建 |
| [yudao-backend](skills/yudao-backend/SKILL.md) | Java API、Service、Mapper、模块接口和权限 |
| [yudao-security](skills/yudao-security/SKILL.md) | Token、角色菜单、数据权限与租户隔离 |
| [yudao-delete-tenant](skills/yudao-delete-tenant/SKILL.md) | 多租户关闭或移除、数据语义与业务行为保护 |
| [yudao-frontend](skills/yudao-frontend/SKILL.md) | 管理后台页面、菜单、API 调用和联调 |
| [yudao-database](skills/yudao-database/SKILL.md) | SQL、表结构、数据升级及多数据库方言 |
| [yudao-sql-convert](skills/yudao-sql-convert/SKILL.md) | 自动执行 MySQL SQL 到七种目标数据库的格式转换与检查 |
| [yudao-integration](skills/yudao-integration/SKILL.md) | 文件、通知、OAuth、Excel、日志等基础能力集成 |
| [yudao-async](skills/yudao-async/SKILL.md) | 定时任务、MQ、缓存、锁、幂等与限流 |
| [yudao-workflow](skills/yudao-workflow/SKILL.md) | BPM 流程定义、表单、审批任务与业务回写 |
| [yudao-commerce](skills/yudao-commerce/SKILL.md) | 支付退款、订单售后、钱包和会员积分 |
| [yudao-ai](skills/yudao-ai/SKILL.md) | 模型、聊天、RAG、工具、MCP 与 AI 编排 |
| [yudao-iot](skills/yudao-iot/SKILL.md) | 设备、协议、网关、物模型、规则与 OTA |
| [yudao-enterprise](skills/yudao-enterprise/SKILL.md) | ERP/CRM/MES/WMS/HRM/FMS/PMS/OA/IM 的业务边界 |
| [yudao-operations](skills/yudao-operations/SKILL.md) | 测试、构建、部署排障及运行证据 |
| [yudao-upgrade](skills/yudao-upgrade/SKILL.md) | 源码、依赖、文档与本插件的增量更新 |

插件通过 `.codex-plugin/plugin.json` 声明技能。将仓库作为插件源加入已配置的 Codex marketplace 后，可使用 `codex plugin add dev-ruoyi-vue-pro@<marketplace-name>` 安装；已在个人 marketplace 登记时，名称为 `dev-ruoyi-vue-pro@personal`。

## 来源与适用范围

[文档导航](references/docs-index.md)收录 27 个分组、382 个目录项，覆盖开发指南、框架与中间件、业务模块、运维和四类前端手册。当前 51 项有已知 URL，331 项的具体 URL 待定位；此前实际读取了 6 页正文，2 页访问受限。本轮浏览器控制连接未恢复，目录依据本任务先前的官网导航记录与当前源码链接整理，不能据此声称所有页面正文都已分析。

用查询工具按需检索，避免每次加载全部目录：

```text
python scripts/docs_index.py search 租户 --json
python scripts/docs_index.py search --skill yudao-codegen
python scripts/docs_index.py check --source-root "<项目根目录>"
```

`references/docs-index.json` 是目录数据源，记录技能路由、URL 来源、正文阅读状态与源码引用；更新后运行 `python scripts/docs_index.py render` 重新生成导航。新增技能的行为约定基于实际源码与代表测试阅读，源码验证与系统运行验收分别记录。

[来源索引](references/source-index.md)记录 `2026.08-jdk25-SNAPSHOT` 基线的仓库相对路径、官方文档链接和核验日期。[指纹清单](references/source-manifest.json)用于检测关键文件及模块目录变化。官网文档持续更新，处理实际任务时先核对当前项目的版本、启用模块和代码。

检查项目与记录的基线是否一致：

```text
python scripts/check_sources.py --root "<项目根目录>"
```

脚本只读；退出码 `0` 表示匹配，`1` 表示文件、模块或版本存在差异。已核验基线中的 `yudao-ui` 不是完整的前端工程，前端任务需针对实际前端仓库检查 `package.json`、路由和构建结果。

## Agent 与维护

七个角色分别负责来源核查、功能实现、验证执行、迁移规划、SQL 转换、资料维护和变更审查，职责及输入输出见[分工约定](references/agent-workflow.md)。`agent-templates/` 中的 TOML 需放到 Codex 的个人 `~/.codex/agents/` 或项目 `.codex/agents/`；复制前核对同名配置，模型与推理设置默认继承。技能的 `agents/openai.yaml` 仅用于技能展示，不会注册子 Agent。

例如可直接提出：`使用 $dev-ruoyi-vue-pro:yudao-sql-convert，把当前项目的 MySQL 初始化 SQL 转成达梦格式，并交付 SQL 和检查报告。` 技能会识别项目的 `sql/tools/convertor.py`，准备隔离依赖并运行包装器。支持 PostgreSQL、Oracle、SQL Server、DM8、Kingbase、OpenGauss、HighGo；输出标记为 `generated_only`，目标数据库导入仍需验证。参数、格式限制和方言差异见[转换技能](skills/yudao-sql-convert/SKILL.md)。

租户移除技能由已有 `yudao-delete-tenant` 导入并重新核验，保留了来源指纹，修正了固定菜单 ID 与当前业务冲突、关闭隔离后的数据可见性、lambda 返回和异常语义等问题；详见[导入来源与差异](skills/yudao-delete-tenant/references/sources.md)。

后续任务按[任务与调整模板](references/task-template.md)描述目标、范围和验收。资料与插件的增量更新步骤见[维护流程](references/upgrade.md)。

## 导入技能包

已整合 `yudao-skills_v1.1.0`：新增 `yudao-system`，并将同名 `yudao-codegen` 的适用流程增量合并到现有技能。来源基于 `yudao-cloud 2026.05-SNAPSHOT`，已按当前单体项目核对结构、API 与生成器约定；原始文件身份和指纹见[导入清单](references/imports/yudao-skills-v1.1.0.json)。

该来源由“爱唱歌的皇阿玛”提供，随附声明允许个人学习与企业商用、禁止复制分发和公开传播。用户于 2026-09-23 确认允许将本次整合内容发布到 `cxszn/agent-dev-ruoyi-vue-pro`；确认范围记录在导入清单中，来源署名与原始使用声明予以保留。
