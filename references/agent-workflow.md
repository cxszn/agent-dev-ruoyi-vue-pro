# Codex Agent 分工

Codex 官方[子 Agent 文档](https://learn.chatgpt.com/docs/agent-configuration/subagents)（2026-09-22 通过外部 Chrome 核对）规定：真实自定义 Agent 是独立 TOML，放在个人 `~/.codex/agents/` 或项目 `.codex/agents/`；必需 `name`、`description`、`developer_instructions`。插件的技能 `agents/openai.yaml` 仅用于技能展示与调用策略，不是子 Agent 定义。当前插件 manifest 不声明 Agent 自动安装字段。

本插件的 `agent-templates/` 提供两份真实格式的 TOML，并在个人 `~/.codex/agents/` 同名安装：

| 角色 | 输入 | 输出 | 边界 |
| --- | --- | --- | --- |
| `yudao_source_auditor` | 目标工作树、任务、版本疑点 | POM/源码/测试的路径和行号、已核实差异、待验证点 | 只读，不把官网文档当成当前源码。 |
| 内置 `worker` | 已收窄的功能目标、文件所有权、验收 | 最小改动、测试证据 | 仅用户要求实施且任务范围已明确时使用。 |
| `yudao_change_reviewer` | 固定 diff、原任务验收和测试结果 | 按严重度排序的正确性/权限/数据风险与证据 | 只读，不把风格偏好当缺陷。 |

主 Agent 负责范围、决策、集成和最终结论。只有用户或适用项目/技能指令明确要求委派时才启动子 Agent；把独立只读工作分出去，写操作指定文件所有权，等待结果后亲自复核关键结论。

使用这些 Agent 时，传入当前项目的工作树与版本，并核对资料基线的适用性。更新模板后同步个人 TOML 并用 `tomllib` 与实际代理发现能力验证。
