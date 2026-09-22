# dev-ruoyi-vue-pro

面向 Codex 的芋道 `ruoyi-vue-pro` 开发插件。它把后端、前端、数据库和版本更新任务引导到对应技能，并提供经核验的源码定位、官方文档索引与任务模板。

## 使用

在已配置此插件的 Codex 环境中，直接描述芋道任务，或显式调用入口技能：

```text
使用 $dev-ruoyi-vue-pro:yudao-router，检查当前项目的 system 用户分页，并给出修改与验收证据。
```

| 技能 | 适用任务 |
| --- | --- |
| [yudao-router](skills/yudao-router/SKILL.md) | 确认目标项目与任务范围，选择下面的技能 |
| [yudao-backend](skills/yudao-backend/SKILL.md) | Java API、Service、Mapper、模块接口和权限 |
| [yudao-frontend](skills/yudao-frontend/SKILL.md) | 管理后台页面、菜单、API 调用和联调 |
| [yudao-database](skills/yudao-database/SKILL.md) | SQL、表结构、数据升级及多数据库方言 |
| [yudao-upgrade](skills/yudao-upgrade/SKILL.md) | 源码、依赖、文档与本插件的增量更新 |

插件通过 `.codex-plugin/plugin.json` 声明技能。将仓库作为插件源加入已配置的 Codex marketplace 后，可使用 `codex plugin add dev-ruoyi-vue-pro@<marketplace-name>` 安装；已在个人 marketplace 登记时，名称为 `dev-ruoyi-vue-pro@personal`。

## 来源与适用范围

[来源索引](references/source-index.md)记录 `2026.08-jdk25-SNAPSHOT` 基线的仓库相对路径、官方文档链接和核验日期。[指纹清单](references/source-manifest.json)用于检测关键文件及模块目录变化。官网文档持续更新，处理实际任务时先核对当前项目的版本、启用模块和代码。

检查项目与记录的基线是否一致：

```text
python scripts/check_sources.py --root "<项目根目录>"
```

脚本只读；退出码 `0` 表示匹配，`1` 表示文件、模块或版本存在差异。已核验基线中的 `yudao-ui` 不是完整的前端工程，前端任务需针对实际前端仓库检查 `package.json`、路由和构建结果。

后续任务可按[任务与调整模板](references/task-template.md)描述目标、范围和验收。需要子 Agent 协作时，参考[分工约定](references/agent-workflow.md)；`agent-templates/` 中的 TOML 是独立 Agent 配置样例，需放到 Codex 的个人或项目 Agent 配置目录，技能展示文件 `agents/openai.yaml` 不承担这一作用。资料与插件的更新步骤见[维护流程](references/upgrade.md)。
