# BPM 定义、实例与任务工作路径

核验日期：2026-09-22；源码基线 `2026.08-jdk25-SNAPSHOT`。方法与行号是源码事实，执行建议尚未通过运行验证。本次没有启动 BPM 或发布流程。

源码提供的官方入口：[BPM 手册](https://doc.iocoder.cn/bpm/)。本轮未访问其正文。根 `pom.xml:19` 与 `yudao-server/pom.xml:50` 中 BPM 依赖为注释；`yudao-dependencies/pom.xml:50` 声明 Flowable `8.0.0`，使用时复核当前有效依赖。

## 定义与发布

- `yudao-module-bpm/src/main/java/cn/iocoder/yudao/module/bpm/controller/admin/definition/BpmModelController.java:184` 的 `deployModel` 使用 `bpm:model:deploy` 并传入当前用户。
- `yudao-module-bpm/src/main/java/cn/iocoder/yudao/module/bpm/service/definition/BpmModelServiceImpl.java:251` 的事务发布检查模型管理员、BPMN、表单与审批人规则，再创建定义、挂起旧定义、保存 deploymentId。
- `yudao-module-bpm/src/main/java/cn/iocoder/yudao/module/bpm/service/definition/BpmProcessDefinitionServiceImpl.java:135` 通过带租户的 Flowable deployment 部署，校验定义 key/name 并保存扩展信息；`:171` 挂起定义时不级联挂起既有实例。

执行建议：发布问题从模型管理权限、BPMN 与表单/候选配置逐层定位。变更模型后核定义版本和旧实例行为；不能把“旧定义已挂起”写成“全部旧实例已停止”。需要运行中实例迁移时先明确目标实例集与迁移策略，再检查该版本 Flowable 支持和测试环境。

## 发起权限与实例

- `yudao-module-bpm/src/main/java/cn/iocoder/yudao/module/bpm/controller/admin/task/BpmProcessInstanceController.java:124` 创建实例接口当前使用权限码 `bpm:process-instance:query`。查问题时按真实实现核对，不能根据动词臆造 `:create` 权限。
- `yudao-module-bpm/src/main/java/cn/iocoder/yudao/module/bpm/service/definition/BpmProcessDefinitionServiceImpl.java:92` 的 `canUserStartProcessDefinition` 优先使用显式用户名单；其非空时直接返回名单判断，只有用户名单空时才检查部门名单，两者都空才开放发起。不能概括为“用户或部门任意命中”。
- `yudao-module-bpm/src/main/java/cn/iocoder/yudao/module/bpm/service/task/BpmProcessInstanceServiceImpl.java:760` 是带事务的 VO 创建入口，`:773` DTO 入口没有该事务注解；`:785` 的共用创建实现校验定义、挂起状态、发起权限、自选审批人，并过滤系统保留变量后启动实例。
- 同文件 `:839` 的 `validateStartUserSelectAssignees` 校验预测路径中的自选节点名单及用户存在；不能仅凭此方法声称禁用用户已经排除。

执行建议：区分界面可见、Controller 权限、定义发起范围、候选策略及实际 assignee。跨模块创建流程时检查调用者的事务边界，不把某个入口的注解套用到所有调用。验证无权限用户、空自选名单、系统保留变量与业务单号关联。

## 审批人及任务动作

- `yudao-module-bpm/src/main/java/cn/iocoder/yudao/module/bpm/framework/flowable/core/candidate/BpmTaskCandidateInvoker.java:57` 验证人工节点策略参数，自动通过/拒绝节点有不同校验分支；`:165` 的 `removeDisableUsers` 从候选集合移除不存在或禁用用户。
- `yudao-module-bpm/src/main/java/cn/iocoder/yudao/module/bpm/controller/admin/task/BpmTaskController.java:156` 与 `:164` 分别通过/拒绝，使用 `bpm:task:update`。
- `yudao-module-bpm/src/main/java/cn/iocoder/yudao/module/bpm/service/task/BpmTaskServiceImpl.java:317` 的 `validateTask` 检查存在和非空 assignee 与当前用户匹配，保留无人审批自动处理分支。
- 同文件 `:573` 的 `approveTask` 事务内验证签名/意见、处理委派或后加签、写审批状态与评论、校验下一审批人，`:656` 调用 Flowable complete；`:835` 的 `rejectTask` 按拒绝策略退回指定节点或结束流程。
- `yudao-module-bpm/src/main/java/cn/iocoder/yudao/module/bpm/service/task/BpmProcessInstanceServiceImpl.java:972` 的完成事件只把仍为 RUNNING 的实例转为 APPROVE，不能无条件把结束实例视为审批通过。

执行建议：先写出本动作允许的原状态、操作者、目标状态与业务回写。验证错误审批人、重复动作、通过/拒绝以及受改动影响的委派/加签分支；发生回滚时同时检查 Flowable 状态、扩展数据和业务单据。不要直接写 engine 表修补展示状态。

## 测试入口与缺口

- `yudao-module-bpm/src/test/java/cn/iocoder/yudao/module/bpm/service/definition/BpmModelServiceImplTest.java:61`/`:82` 为 BPMN/simple 导出，`:105` 模型不存在，`:117` BPMN 导入；这些用例不能证明完整发布审批链。
- `yudao-module-bpm/src/test/java/cn/iocoder/yudao/module/bpm/framework/flowable/core/candidate/BpmTaskCandidateInvokerTest.java:75` 等方法测试候选计算，`:256` 检查禁用用户移除。
- candidate 的 user、post、group、role 及 expression 策略测试在核验时有 `@Disabled`，执行前检查当前类和方法状态，不能把跳过记为通过。

按改动范围选择数据库/Flowable 测试和受控业务流程验收，报告真实执行结果。仅导出 XML 或拿到 HTTP 200 不足以证明审批人与业务状态正确。
