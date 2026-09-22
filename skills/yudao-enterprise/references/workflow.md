# 企业业务工作路径

核验日期：2026-09-22；源码基线 `2026.08-jdk25-SNAPSHOT`。以下入口及约束来自源码静态核查，未启动模块或执行测试。“实施与验收”是工作建议。

## 启用与资料边界

根 `pom.xml:24` 至 `:33` 中 CRM、ERP、MES、WMS、HRM、FMS、PMS、OA、IM 的 module 为注释；`yudao-server/pom.xml:93` 至 `:163` 的相应依赖也是注释。使用时复核当前工程的模块和依赖，不直接把本基线状态套入其它工作树。

源码提供的官方入口：[ERP](https://doc.iocoder.cn/erp/build/)、[CRM](https://doc.iocoder.cn/crm/build/)、[MES](https://doc.iocoder.cn/mes/build/)、[WMS](https://doc.iocoder.cn/wms/build/)、[HRM](https://doc.iocoder.cn/hrm/build/)、[FMS](https://doc.iocoder.cn/fms/build/)、[PMS](https://doc.iocoder.cn/pms/build/)、[OA](https://doc.iocoder.cn/oa/build/)、[IM](https://doc.iocoder.cn/im/build/)。本轮未访问这些页面正文。

## 按业务选择入口

每项先给真实 Controller 路径，再给 Service 的关键行为；同域其它功能从相邻 service 目录定位。

| 业务 | 源码定位与已核事实 |
| --- | --- |
| ERP 销售出库审核 | `yudao-module-erp/src/main/java/cn/iocoder/yudao/module/erp/controller/admin/sale/ErpSaleOutController.java:47`；`yudao-module-erp/src/main/java/cn/iocoder/yudao/module/erp/service/sale/ErpSaleOutServiceImpl.java:166` 的 `updateSaleOutStatus` 在事务内拒绝相同状态，有收款金额时拒绝反审核；按旧状态条件更新，审核扣库存、反审核回补。 |
| CRM 客户公海 | `yudao-module-crm/src/main/java/cn/iocoder/yudao/module/crm/controller/admin/customer/CrmCustomerController.java:51`；`yudao-module-crm/src/main/java/cn/iocoder/yudao/module/crm/service/customer/CrmCustomerServiceImpl.java:371` 的 `putCustomerPool` 要求 OWNER 领域权限并检查归属、锁定；`:391` 领取检查归属、成交和持有上限。 |
| MES 生产工单 | `yudao-module-mes/src/main/java/cn/iocoder/yudao/module/mes/controller/admin/pro/workorder/MesProWorkOrderController.java:44`；`yudao-module-mes/src/main/java/cn/iocoder/yudao/module/mes/service/pro/workorder/MesProWorkOrderServiceImpl.java:164` 确认只允许 PREPARE → CONFIRMED；`:179` 完成、`:197` 取消均在事务内级联关联任务。 |
| WMS 收货入库 | `yudao-module-wms/src/main/java/cn/iocoder/yudao/module/wms/controller/admin/order/receipt/WmsReceiptOrderController.java:53`；`yudao-module-wms/src/main/java/cn/iocoder/yudao/module/wms/service/order/receipt/WmsReceiptOrderServiceImpl.java:106` 完成要求草稿与明细，按状态条件更新后创建库存；`:124` 取消仅接受草稿。 |
| HRM 入职 | `yudao-module-hrm/src/main/java/cn/iocoder/yudao/module/hrm/controller/admin/employee/HrmEmployeeController.java:176`；`yudao-module-hrm/src/main/java/cn/iocoder/yudao/module/hrm/service/employee/info/HrmEmployeeServiceImpl.java:204` 的 `confirmEmployeeEntry` 事务内仅接受 PENDING_ENTRY，写 ACTIVE 并同步招聘候选人状态。 |
| FMS 凭证审核 | `yudao-module-fms/src/main/java/cn/iocoder/yudao/module/fms/controller/admin/voucher/FmsVoucherController.java:140`；`yudao-module-fms/src/main/java/cn/iocoder/yudao/module/fms/service/voucher/FmsVoucherServiceImpl.java:250` 核账套写权限、会计期间开放，再允许 PENDING_REVIEW 与 APPROVED 之间审核/反审核。 |
| PMS 迭代 | `yudao-module-pms/src/main/java/cn/iocoder/yudao/module/pms/controller/admin/pm/iteration/PmsIterationController.java:71`；`yudao-module-pms/src/main/java/cn/iocoder/yudao/module/pms/service/pm/iteration/PmsIterationServiceImpl.java:112` 启动 PLANNED → ACTIVE，`:128` 完成 ACTIVE → COMPLETED；`:376` 的 `validateProjectWritable` 核成员写权限及项目 ACTIVE 状态。 |
| OA 请假申请 | `yudao-module-oa/src/main/java/cn/iocoder/yudao/module/oa/controller/admin/leave/OaLeaveApplyController.java:64`；`yudao-module-oa/src/main/java/cn/iocoder/yudao/module/oa/service/leave/OaLeaveApplyServiceImpl.java:86` 事务提交申请，`:162` 限本人 NOT_START 草稿，提交写 RUNNING 并绑定新 BPM 实例。 |
| IM 私聊与撤回 | `yudao-module-im/src/main/java/cn/iocoder/yudao/module/im/controller/admin/message/ImPrivateMessageController.java:35` 从登录用户取得发送人；`yudao-module-im/src/main/java/cn/iocoder/yudao/module/im/service/message/ImPrivateMessageServiceImpl.java:71` 按 senderId + clientMessageId 查重，检查好友、内容和敏感词后保存推送；`:160` 撤回要求本人、未撤回且处于配置时间窗。 |

## 同域检索范围

从所选模块的 `src/main/java/cn/iocoder/yudao/module/<模块>/service/` 下按任务关键词检索，避免一次加载全部模块：

- ERP：finance、product、purchase、sale、stock；CRM：business、clue、contact、contract、customer、permission、receivable。
- MES：pro（生产）、qc（质量）、wm（仓储）、md（主数据）、dv（设备）；WMS：inventory、md、order。
- HRM：employee、attendance、recruit、salary、insurance、performance；FMS：voucher、ledger、closing、report。
- PMS：pm、kb；OA：leave、overtime、travel、reimbursement、officialdoc、meetingroom、vehicle、task 等办公对象；IM：message、conversation、friend、group、channel、rtc、websocket。

这些是当前真实 service 子目录的定位词，不代表业务完整性或各功能均已实测。ERP、MES 和 WMS 都有库存相关对象，修改时必须依据具体单据路径与调用 API 确定负责模块。

## 实施与验收

1. 固定一个真实业务对象，明确其所属模块、状态与操作者范围；列出关联单据、库存/账务/人员/消息副作用。
2. 查同类 Controller 权限码和 Service 领域权限。CRM OWNER、FMS 账套、PMS 成员、OA 本人等条件需与通用权限一起验证。
3. 修改状态流时复核事务、按旧状态更新、关联对象更新和失败回滚；修改跨域契约时同步调用方与对应测试，不直接复用名称相似的另一模块 DO。
4. 用受控数据验证正常转换、非法原状态、重复操作、无领域权限以及副作用失败回滚。涉及消息或 BPM，再验证最终消费/流程状态。
5. 输出源码证据与实际执行结果；未启用模块、未配置中间件、没有测试或没有前端源码时说明覆盖限制。

## 已存在的代表测试

| 模块 | 测试路径与准确覆盖范围 |
| --- | --- |
| ERP / CRM | 当前扫描未找到 Java 测试类或 `@Test`；CRM 的测试资源配置不能代替测试覆盖。 |
| MES | `yudao-module-mes/src/test/java/cn/iocoder/yudao/module/mes/service/wm/itemreceipt/MesWmItemReceiptServiceImplTest.java:61` 正常入库，`:133` 非法入库状态；它不是上面工单状态的测试。 |
| WMS | `yudao-module-wms/src/test/java/cn/iocoder/yudao/module/wms/service/order/receipt/WmsReceiptOrderServiceImplTest.java:102` 完成收货，`:144` 重复完成，`:176` 状态条件不匹配。 |
| HRM | `yudao-module-hrm/src/test/java/cn/iocoder/yudao/module/hrm/service/employee/info/HrmEmployeeServiceImplTest.java:218` 非法入职状态。 |
| FMS | `yudao-module-fms/src/test/java/cn/iocoder/yudao/module/fms/service/voucher/FmsVoucherServiceImplTest.java:706` 审核、反审核及审核人字段。 |
| PMS | `yudao-module-pms/src/test/java/cn/iocoder/yudao/module/pms/service/pm/iteration/PmsIterationServiceImplTest.java:141` 已完成迭代不能重新开始。 |
| OA | `yudao-module-oa/src/test/java/cn/iocoder/yudao/module/oa/service/leave/OaLeaveApplyServiceImplTest.java:159` BPM 创建失败后仍保留草稿且实例 ID 为空。 |
| IM | `yudao-module-im/src/test/java/cn/iocoder/yudao/module/im/service/message/ImPrivateMessageServiceImplTest.java:108` clientMessageId 幂等，`:240` 拒绝撤回他人消息。 |

运行前检查当前测试的禁用状态和环境依赖；测试文件存在只证明有代码，不能报告为测试通过。
