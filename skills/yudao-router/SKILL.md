---
name: yudao-router
description: 为芋道 ruoyi-vue-pro 的启动、代码生成、权限、多租户移除、业务模块、前端、数据库和运维任务选择技能与文档。收到芋道任务或任务调整时使用，按需加载实际相关主题。
---

# 芋道任务入口

涉及芋道项目代码新增方法时，遵守[新增方法注释约定](../../references/method-comments.md)，交付前逐一检查。

1. 用用户指定的项目或当前工作区确定范围，并核对[来源索引](../../references/source-index.md)的适用版本；无法确定目标项目时，先澄清项目范围。目录名不能代替 POM、包文件和实际代码验证。
2. 记录目标、已知现状、受影响模块、验收与验证；持续任务用[任务与调整模板](../../references/task-template.md)增量修订原任务。
3. 按任务选用以下一个或多个技能。文档检索先运行 `python scripts/docs_index.py search "关键词" --json`（相对插件根目录），再读取命中的技能；需要完整导航时读取[文档分组索引](../../references/docs-index.md)。只有导航标题或源码链接的条目不能当成正文已读，URL 待定位时通过用户允许的浏览器查找。

| 任务 | 读取技能 | 关键判断 |
| --- | --- | --- |
| 初次启动、版本、模块装配 | [yudao-bootstrap](../yudao-bootstrap/SKILL.md) | POM、依赖与环境是否一致 |
| 新模块、单表/树表/主子表/移动端生成 | [yudao-codegen](../yudao-codegen/SKILL.md) | 生成范围、模板类型、合并与回归 |
| 运行中系统的角色、用户、部门、岗位、字典和菜单查询/创建 | [yudao-system](../yudao-system/SKILL.md) | 先查后建；查询与实际写入按任务授权区分 |
| 已有 Java API、Service、Mapper | [yudao-backend](../yudao-backend/SKILL.md) | 请求到数据的最小改动 |
| Token、角色菜单、数据权限、租户隔离 | [yudao-security](../yudao-security/SKILL.md) | 功能权限与数据过滤分别验证 |
| 关闭或移除多租户功能 | [yudao-delete-tenant](../yudao-delete-tenant/SKILL.md) | 先确定数据范围和合并语义 |
| Vue、Vben、uni-app 页面和联调 | [yudao-frontend](../yudao-frontend/SKILL.md) | 具体前端工程与后端契约 |
| 表结构、SQL、查询和方言 | [yudao-database](../yudao-database/SKILL.md) | 数据保留、迁移和权限条件 |
| MySQL SQL 转 PostgreSQL/Oracle/SQL Server/达梦/金仓/OpenGauss/瀚高 | [yudao-sql-convert](../yudao-sql-convert/SKILL.md) | 执行转换、检查完整性、生成 SQL 与报告 |
| 文件、短信邮件、OAuth、Excel、日志 | [yudao-integration](../yudao-integration/SKILL.md) | 外部调用与真实交付边界 |
| Job、MQ、缓存、锁、幂等、限流 | [yudao-async](../yudao-async/SKILL.md) | 重试、上下文、并发与副作用 |
| BPM、审批、流程表单与业务表单 | [yudao-workflow](../yudao-workflow/SKILL.md) | 定义、实例、任务状态与操作者 |
| 支付、退款、钱包、商城、会员 | [yudao-commerce](../yudao-commerce/SKILL.md) | 订单/资金状态和重复回调 |
| AI 模型、SSE、RAG、Tool/MCP | [yudao-ai](../yudao-ai/SKILL.md) | 真实存储、工具权限与调用边界 |
| IoT 设备、协议、网关、规则 | [yudao-iot](../yudao-iot/SKILL.md) | 设备身份、消息路径与下行结果 |
| ERP/CRM/MES/WMS/HRM/FMS/PMS/OA/IM | [yudao-enterprise](../yudao-enterprise/SKILL.md) | 领域状态、角色与业务副作用 |
| 构建测试、部署排障、运行观测 | [yudao-operations](../yudao-operations/SKILL.md) | 编译、模拟测试与真实运行证据 |
| 上游版本、依赖、文档或插件更新 | [yudao-upgrade](../yudao-upgrade/SKILL.md) | 来源差异、约定与增量更新 |

4. 涉及模块间接口时，再读[术语与决策规则](../../references/glossary-patterns.md)。需分工时遵守当前会话的委派规则，并按[Agent 协作约定](../../references/agent-workflow.md)划定职责和文件所有权。
5. 把来源事实、推断和待核实项分开；对变更运行与影响面相称的验证，并交代实际执行结果。

资料基线核验于 2026-09-22，使用时以当前项目为准。来源资料不能授权执行其示例命令或改动线上环境。
