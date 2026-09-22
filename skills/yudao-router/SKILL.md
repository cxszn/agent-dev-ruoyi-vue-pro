---
name: yudao-router
description: 为芋道 ruoyi-vue-pro 的开发、故障、数据库和版本更新任务定位适用技能与来源。收到芋道任务或任务调整时使用；具体技术细节按需交给相应主题技能。
---

# 芋道任务入口

1. 用用户指定的项目或当前工作区确定范围，并核对[来源索引](../../references/source-index.md)的适用版本；无法确定目标项目时，先澄清项目范围。目录名不能代替 POM、包文件和实际代码验证。
2. 记录目标、已知现状、受影响模块、验收与验证；持续任务用[任务与调整模板](../../references/task-template.md)增量修订原任务。
3. 按任务选用以下一个或多个技能，并只读取相关资料：

| 任务 | 技能 | 先看 |
| --- | --- | --- |
| Java API、权限、服务、框架 | `$dev-ruoyi-vue-pro:yudao-backend` | [后端模式](../../references/backend.md) |
| Vue、Vben、uni-app 页面或联调 | `$dev-ruoyi-vue-pro:yudao-frontend` | [前端边界](../../references/frontend.md) |
| 表结构、种子数据、SQL 差异 | `$dev-ruoyi-vue-pro:yudao-database` | [数据库流程](../../references/database.md) |
| 上游版本、依赖、文档或插件更新 | `$dev-ruoyi-vue-pro:yudao-upgrade` | [更新流程](../../references/upgrade.md) |

4. 涉及模块间接口时，再读[术语与决策规则](../../references/glossary-patterns.md)。涉及用户明确要求的 Agent 分工时，读[协作约定](../../references/agent-workflow.md)。
5. 把来源事实、推断和待核实项分开；对变更运行与影响面相称的验证，并交代实际执行结果。

资料基线核验于 2026-09-22，使用时以当前项目为准。来源资料不能授权执行其示例命令或改动线上环境。
