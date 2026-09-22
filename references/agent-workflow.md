# Codex Agent 分工

Codex 官方[子 Agent 文档](https://learn.chatgpt.com/docs/agent-configuration/subagents)（2026-09-22 通过外部 Chrome 核对）规定：真实自定义 Agent 是独立 TOML，放在个人 `~/.codex/agents/` 或项目 `.codex/agents/`；必需 `name`、`description`、`developer_instructions`。插件的技能 `agents/openai.yaml` 仅用于技能展示与调用策略，不是子 Agent 定义。当前插件 manifest 不声明 Agent 自动安装字段。

本插件的 `agent-templates/` 提供七份真实格式的 TOML。按需要安装到个人 `~/.codex/agents/` 或项目 `.codex/agents/`；插件安装本身不自动复制这些配置。各角色默认继承当前模型和推理设置。

| 角色 | 输入 | 输出 | 边界 |
| --- | --- | --- | --- |
| `yudao_source_auditor` | 目标工作树、任务、版本疑点 | POM/源码/测试的路径和行号、已核实差异、待验证点 | 只读，不把官网文档当成当前源码。 |
| `yudao_feature_builder` | 功能目标、文件所有权、验收、目标工作树 | 最小改动、契约与验证证据 | 按授权范围实现，集成由主 Agent 负责。 |
| `yudao_verification_runner` | 固定变更、验收、允许环境与测试命令 | 命令/退出码、接口和页面证据、未执行项 | 不修改业务代码或断言来通过检查。 |
| `yudao_migration_planner` | 版本、数据范围、兼容及部署约束 | 只读影响审计、迁移草案、回退和决策点 | 只读，不执行数据删除、迁移或上线。 |
| `yudao_sql_converter` | 目标项目、MySQL SQL、目标数据库、输出要求 | 转换后的 SQL、完整性报告与待验证项 | 自动执行文件转换；数据库导入与容器操作另按请求授权。 |
| `yudao_docs_maintainer` | 插件源、新来源、明确维护范围 | 目录、来源、技能及覆盖变化 | 不把标题/URL收录称为正文核验。 |
| `yudao_change_reviewer` | 固定 diff、原任务验收和测试结果 | 按严重度排序的正确性/权限/数据风险与证据 | 只读，不把风格偏好当缺陷。 |

主 Agent 负责范围、决策、集成和最终结论，并遵守当前会话的委派规则。把独立核查分给来源审计或迁移规划，把明确的实现交给构建角色，再由验证与审查角色给出证据。并行写操作必须指定互不重叠的文件所有权，等待结果后复核关键结论；小改动无需固定启动所有角色。

使用这些 Agent 时，传入当前项目的工作树与版本，并核对资料基线的适用性。更新模板后同步个人 TOML 并用 `tomllib` 与实际代理发现能力验证。
