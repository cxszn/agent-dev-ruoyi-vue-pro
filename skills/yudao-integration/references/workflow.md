# 集成主题流程与源码定位

核验日期：2026-09-22。下列路径相对目标项目根目录，行号用于定位已核验实现；切换版本先按符号重新搜索。完整版本范围见[来源索引](../../../references/source-index.md)。这里只总结源码和测试内容，未据此声称运行过测试或完成外部服务接入。

## 文件存储与上传

- 后端接收文件内容：`yudao-module-infra/src/main/java/cn/iocoder/yudao/module/infra/service/file/FileServiceImpl.java:73`，`createFile(byte[], ...)` 校验文件名、补 MIME/扩展名、生成路径、用主客户端上传，再保存 `FileDO.configId/path/url`。
- 客户端直传：同文件 `:150` 的 `presignPutUrl` 返回上传地址及访问地址；`:169` 的 `createFile(FileCreateReqVO)` 只校验并保存元数据，移除 URL 查询参数。必须继续验证对象实际上传以及私有文件访问，不把登记元数据当作上传完成。
- 存储选择：`yudao-module-infra/src/main/java/cn/iocoder/yudao/module/infra/service/file/FileConfigServiceImpl.java:199` 的 `getFileClient(id)` 和 `:204` 的 `getMasterFileClient`。切换主配置与迁移既有文件是两件操作：已有文件删除在 `FileServiceImpl.java:188` 使用该记录的 `configId` 获取客户端。
- 签名支持：`yudao-module-infra/src/main/java/cn/iocoder/yudao/module/infra/framework/file/core/client/FileClient.java:51` 的默认 `presignPutUrl` 不支持预签名；需确认所选客户端覆写实现。`FileServiceImpl.java:163` 的签名读取仍取当前主客户端，切换存储后旧文件的访问应单独核实。
- 路径策略：`FileServiceImpl.java:108` 的 `generateUploadPath`；日期前缀、时间戳后缀和目录形式由类内开关控制，不假设所有部署自动生成唯一名。变更后核原名、扩展名、非法目录和同名上传。
- 回归入口：`yudao-module-infra/src/test/java/cn/iocoder/yudao/module/infra/service/file/FileServiceImplTest.java:87` 验证 Mock 上传与数据库元数据；`:178` 非法删除路径；`:232` 预签名路径登记；`:428` 非法文件名。这些不证明真实桶权限、CORS 或签名有效期。

处理顺序：确定后端上传或客户端直传 → 定位配置和具体 `FileClient` → 核路径与 URL 契约 → 核数据库记录和对象访问。删除时同时考虑存储对象与数据库记录，先列明目标。

## 短信、邮件、站内信

先查 `userType`（管理用户或会员）、模板 code、模板参数、目标接收者与渠道/账号状态。三种发送结果的语义不同：

| 能力 | 源码入口 | 实际语义与验收 |
| --- | --- | --- |
| 短信 | `yudao-module-system/src/main/java/cn/iocoder/yudao/module/system/service/sms/SmsSendServiceImpl.java:81`，`sendSingleSms` | 模板或渠道禁用仍创建日志，只有双方启用才派发。模板参数按模板声明排序，缺值提前抛错。返回日志 ID 后继续查 `:158` 的 `doSendSms` 结果和 `:177` 的 `receiveSmsStatus` 回执。 |
| 邮件 | `yudao-module-system/src/main/java/cn/iocoder/yudao/module/system/service/mail/MailSendServiceImpl.java:58`，`sendSingleMail` | 合并用户邮箱与显式收件人，过滤邮箱并去重；有效收件人为空会失败。模板禁用仍记日志；`:121` 的 `doSendMail` 才调用邮件客户端并记录结果。附件生命周期需覆盖异步发送。 |
| 站内信 | `yudao-module-system/src/main/java/cn/iocoder/yudao/module/system/service/notify/NotifySendServiceImpl.java:45`，`sendSingleNotify` | 模板禁用直接返回 `null`；启用时格式化模板并创建消息。验收落库、归属用户/类型与读取状态，不套用短信渠道回执。 |

发送链路虽命名为 `mq`，当前短信/邮件通过 Spring Application Event 派发。下面路径均相对 `yudao-module-system/src/main/java/cn/iocoder/yudao/module/system/`：`mq/producer/sms/SmsProducer.java:34`、`mq/producer/mail/MailProducer.java:38`；对应 `mq/consumer/sms/SmsSendConsumer.java:24`、`mq/consumer/mail/MailSendConsumer.java:24` 使用 `@EventListener` 与 `@Async`。排查发送积压或丢失先核目标版本的实际生产者、消费者和执行器，再决定是否涉及外部消息中间件。

代表测试（均相对 `yudao-module-system/src/test/java/cn/iocoder/yudao/module/system/service/`）：

- `sms/SmsSendServiceImplTest.java:136` 与 `:176`：模板启用派发、禁用只记日志；`:223` 参数缺失。
- `mail/MailSendServiceImplTest.java:244`：无有效邮箱；`:271` 与 `:304`：Mock 邮件发送成功/异常后的日志更新。
- `notify/NotifySendServiceImplTest.java:129`：禁用返回空且不格式化、不建消息。

先用 Mock 验证契约，再在已获授权的测试接收者上验收供应商响应/回执。日志、示例和报告只展示脱敏接收者及非敏感错误码。

## 社交登录与 OAuth2

先明确集成方向：用户借助第三方身份登录芋道，查 `social`；其它应用向芋道申请访问令牌，查 `oauth2`。避免把两者的授权码、客户端配置或系统用户 ID 混用。

- 第三方身份：`yudao-module-system/src/main/java/cn/iocoder/yudao/module/system/service/social/SocialUserServiceImpl.java:133`，`authSocialUser` 先按平台类型、code、state 查已有记录，再向 `SocialClientService` 获取身份，用于登录后继续绑定时复用一次性 code。排查应追踪 `socialType/userType/code/state` 契约，报告不输出 token 或原始身份响应。
- 用户绑定：同文件 `:62`，`bindSocialUser` 在事务内清理该社交身份旧绑定及当前用户同类绑定，再插入新绑定。把这项行为纳入改动评估和授权，不能在诊断时随意调用绑定接口。
- 对外 OAuth2：`yudao-module-system/src/main/java/cn/iocoder/yudao/module/system/controller/admin/oauth2/OAuth2OpenController.java:98`，`postAccessToken` 验证 grant type、客户端、scope 和 redirect URI，再分派授权；`:185` 获取授权信息。继续读取 `OAuth2ClientService`、`OAuth2GrantService`、令牌校验和资源接口上的 scope 检查；令牌签发成功不证明资源权限正确。
- 回归入口：`yudao-module-system/src/test/java/cn/iocoder/yudao/module/system/service/social/SocialUserServiceImplTest.java:79` 覆盖旧绑定替换；`:157`、`:192`、`:211` 分别覆盖已存在身份、插入与更新。OAuth2 变更从 `yudao-module-system/src/test/java/cn/iocoder/yudao/module/system/controller/admin/oauth2/OAuth2OpenControllerTest.java` 选择对应授权模式测试，再检查真实回调链路。

## Excel 导入导出

源码：`yudao-framework/yudao-spring-boot-starter-excel/src/main/java/cn/iocoder/yudao/framework/excel/core/util/ExcelUtils.java`。

- `:38` 的类表头导出注册列宽、下拉表单处理器与 `LongStringConverter`，避免长整型精度丢失；`:62` 支持动态表头。当前实现使用 `cn.idev.excel.FastExcelFactory`，不要直接引入旧版本示例里的不同 Excel 库。
- `:75` 的普通 `read` 读取全部数据；`:95` 的 `read(..., maxRowCount)` 到达上限即停止，不会自动报“超限”。若业务要拒绝超限，可读上限加一行后判断，并核现有业务实现和内存开销。
- `:133` 的动态表头读取返回按列下标的 Map。读取成功只证明解析，业务校验、重复行策略、权限和落库事务仍由调用方负责。
- 测试：`yudao-framework/yudao-spring-boot-starter-excel/src/test/java/cn/iocoder/yudao/framework/excel/core/util/ExcelUtilsTest.java:22` 用内存生成三行再限读两行；这是可复用的有界读取用例，不覆盖完整业务导入。

## API 访问日志

源码：`yudao-framework/yudao-spring-boot-starter-web/src/main/java/cn/iocoder/yudao/framework/apilog/core/filter/ApiAccessLogFilter.java`。

- `:94` 经 `ApiAccessLogCommonApi.createApiAccessLogAsync` 保存访问日志；异常日志与业务操作日志应按各自调用链核查。
- `:130` 默认记录请求参数，`:137` 默认不记录响应；方法上的 `@ApiAccessLog` 可调整。排查“缺少日志”先查开关、过滤器、请求处理方法及异步保存链路。
- `:52` 的默认移除字段为 `password/token/accessToken/refreshToken`；自定义敏感字段需要核 `sanitizeKeys`。不可推断所有凭据名或业务敏感字段均已覆盖。
- `:196` 起的 JSON 脱敏捕获解析异常后会返回原字符串；涉及非 JSON 请求或新增敏感字段时，要验脱敏失败分支以及日志本身，不把默认字段列表当完整防泄漏保证。
- 持久化测试：`yudao-module-infra/src/test/java/cn/iocoder/yudao/module/infra/service/logger/ApiAccessLogServiceImplTest.java:99` 的 `testCreateApiAccessLog`。该测试不覆盖过滤器字段脱敏，应按改动另选或补充针对性用例。
