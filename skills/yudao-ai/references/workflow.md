# AI 模型、检索与工具工作路径

核验日期：2026-09-22。源码事实来自 `2026.08-jdk25-SNAPSHOT`；行号是定位锚点，使用时搜索符号复核当前实现。以下“执行与验收”是工作建议，不是已完成的运行测试。

源码提供的官方入口：[AI 启动](https://doc.iocoder.cn/ai/build/)。本轮未访问其正文，实施时仍须核对当前版本资料。

## 基线与入口

- 根 `pom.xml:35` 和 `yudao-server/pom.xml:107` 中 AI 模块被注释；`yudao-module-ai/pom.xml:22` 声明 Spring AI `2.0.0`。根 Boot 属性与 BOM 属性存在差异，依赖工作应读取有效 POM。
- `yudao-module-ai/src/main/java/cn/iocoder/yudao/module/ai/controller/admin/chat/AiChatMessageController.java:59`：`sendMessage` 与 `sendChatMessageStream` 分别处理段式和 `text/event-stream`；消息列表在 `:76` 比较对话所属用户。
- `yudao-module-ai/src/main/java/cn/iocoder/yudao/module/ai/service/chat/AiChatMessageServiceImpl.java:140`：段式发送检查会话所属用户、模型，再召回知识库与可选联网搜索；流式入口为 `:196`。不能以流式方法返回 `Flux` 推断应用已改为 WebFlux。
- `yudao-module-ai/src/main/java/cn/iocoder/yudao/module/ai/service/model/AiModelServiceImpl.java:129`：`getChatModel`；`:159` 的 `getOrCreateVectorStore` 通过模型工厂取得 embedding，`:170` 实际选择 `SimpleVectorStore`，Qdrant/Redis/Milvus 仅是相邻注释分支。依赖存在不等于启用某种存储。

## 聊天与模型

执行与验收：

1. 区分模型供应商调用失败、业务会话权限失败、SSE 被代理缓冲、流中断或持久化失败；定位上面的 Controller 与两条发送 Service 路径。
2. 按模型类型核对数据库模型记录、启用状态、工厂适配器与请求参数，仅记录脱敏配置。
3. 改动共享 prompt/history 构造时同时检查段式和流式。以正常响应、首片响应、供应商错误、取消/断开及非所属用户访问为验收条件，按任务选择受影响场景。

## RAG

源码定位：

- `yudao-module-ai/src/main/java/cn/iocoder/yudao/module/ai/service/knowledge/AiKnowledgeSegmentServiceImpl.java:95`：`createKnowledgeSegmentBySplitContent`；`:126` 更新片段；`:193` 重建索引；`:216` 写向量 metadata。
- 同文件 `:281` 的 `searchDocument` 使用 `knowledgeId` metadata 过滤，可选 rerank 会扩大召回数量再截取；`:365` 的 `splitContentByStrategy` 是分段策略入口。
- `yudao-module-ai/src/main/java/cn/iocoder/yudao/module/ai/service/chat/AiChatMessageServiceImpl.java:304`：`recallKnowledgeSegment`；`:324` 的 `buildPrompt` 负责把检索内容组合入 prompt。

执行与验收：先固定文档样本、知识库 ID、embedding 模型和检索条件，再分别验证解析分段、数据库片段、向量写入及召回。切换 embedding 或存储时核对维度与重建范围；说明数据库写入与远端向量写入的失败后状态，不能假设跨存储原子事务。验证不同知识库不会串检索、禁用/删除片段不再参与召回；只在获准的数据范围内重建索引。

## Tool Calling 与 MCP

源码定位：

- `yudao-module-ai/src/main/java/cn/iocoder/yudao/module/ai/service/model/AiToolServiceImpl.java:75`：`validateToolNameExists` 用 `ToolCallbackResolver` 检查工具名。
- `yudao-module-ai/src/main/java/cn/iocoder/yudao/module/ai/service/chat/AiChatMessageServiceImpl.java:389`：`getToolCallbackListByRoleId` 从角色配置选择工具；`:409` 根据已配置的 MCP 客户端名匹配 `McpSyncClient` 并转换工具回调。
- `yudao-module-ai/pom.xml:172`：MCP 使用 WebMVC server 与普通 client starter；相邻项目注释指出 WebFlux starter 会影响当前 SSE Server。变更依赖前复核当前版本契约。

执行与验收：先区分本地 Spring 工具注册、角色可用工具、MCP 连接与模型是否实际发起调用。检查工具名与 schema、用户/租户上下文和业务权限；用假工具验证非法参数、未配置工具、失败返回及重复请求。MCP 已连接只能证明通信，不能证明业务调用和权限正确。

## TinyFlow

`yudao-module-ai/src/main/java/cn/iocoder/yudao/module/ai/service/workflow/AiWorkflowServiceImpl.java:110` 的 `testWorkflow` 读取请求或保存的 graph，`:123` 的 `parseFlowParam` 遍历节点并为 `llmNode` 绑定模型。AI graph 编排在此处理；人工审批任务应转到 `yudao-workflow`。

执行与验收：固定 graph、输入 variables 与允许的节点副作用，验证节点参数、模型映射和执行结果。不要把名为 test 的接口视为无副作用操作；当前实现会执行 chain。

## 测试覆盖边界

- `yudao-module-ai/src/test/java/cn/iocoder/yudao/module/ai/framework/ai/core/model/chat/OpenAIChatModelTests.java:44` 附近示例方法带 `@Disabled`。
- `yudao-module-ai/src/test/java/cn/iocoder/yudao/module/ai/framework/ai/core/model/mcp/DouBaoMcpTests.java:15` 为 `@Disabled` 外部模型示例，不能作为已验证 MCP 服务的证据。

本参考只核查源码与测试声明，未启动 AI 模块、未调用供应商、未执行向量重建。以后测试需分别报告本地替身结果与经授权的外部集成结果。
