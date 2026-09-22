# 交易、支付、退款与积分

核验日期：2026-09-22，源码基线 `2026.08-jdk25-SNAPSHOT`。路径及方法行为是源码事实；下面执行流程与验收项是工作建议。本次未启动模块或执行财务操作。

源码提供的官方入口：[支付启动](https://doc.iocoder.cn/pay/build/)、[商城启动](https://doc.iocoder.cn/mall/build/)。本轮未访问正文；不能据入口链接声称官网对应实现已核验。

## 选择业务边界

根 `pom.xml:18`、`:22`、`:23` 分别注释 member/pay/mall；server POM 对应依赖也被注释。mall 聚合 product、promotion、trade、statistics 等子模块，修改交易前核对实际子模块 POM 与调用的 API。

支付单处理渠道事实，业务订单处理发货/权益等业务状态，会员流水处理积分变动。跨域动作沿现有 API 和 handler 查找，不直接写另一模块的表替代现有业务方法。商品价格/促销问题先定位 product/promotion 与 `TradePriceServiceImpl`，只有产生支付金额或订单状态变化时再展开支付链。

## 支付与异步通知

| 源码位置 | 已核实行为 |
| --- | --- |
| `yudao-module-pay/src/main/java/cn/iocoder/yudao/module/pay/api/order/dto/PayOrderCreateReqDTO.java:66` | 支付金额为 Integer，单位分；退款 DTO 的 `api/refund/dto/PayRefundCreateReqDTO.java:64` 同样声明分。 |
| `yudao-module-pay/src/main/java/cn/iocoder/yudao/module/pay/controller/admin/notify/PayNotifyController.java:63` | 渠道支付通知入口，`:85` 为退款入口；调用对应渠道 client 解析通知后进入 Service。 |
| `yudao-module-pay/src/main/java/cn/iocoder/yudao/module/pay/service/order/PayOrderServiceImpl.java:116` | `createOrder` 按 appId 与 merchantOrderId 查重返回已有单。`:263` 的通知按渠道切换租户，经代理进入事务。`:292` 成功通知以状态判断和条件更新处理；重复成功不重复创建通知任务。 |
| `yudao-module-pay/src/main/java/cn/iocoder/yudao/module/pay/service/notify/PayNotifyServiceImpl.java:97` | 建立业务通知任务，事务提交后异步触发；`:187` 附近使用 Redis 任务锁，`:270` 根据结果和次数安排重试。 |

执行建议：区分“渠道通知未到”“渠道解析失败”“支付状态未更新”“业务通知重试中”“业务单拒绝状态变化”。记录脱敏单号、渠道、租户、原状态、目标状态与通知任务；不要直接重放真实扣款接口诊断回调。验证重复成功通知不会重复生效，错误渠道/金额/商户单号不被接纳，失败任务仍保留可追踪状态。

## 商城订单与售后

- `yudao-module-mall/yudao-module-trade/src/main/java/cn/iocoder/yudao/module/trade/controller/app/order/AppTradeOrderController.java:74` 创建订单，`:81` 接收 update-paid。
- `yudao-module-mall/yudao-module-trade/src/main/java/cn/iocoder/yudao/module/trade/service/order/TradeOrderUpdateServiceImpl.java:186` 事务编排创建及 `TradeOrderHandler`；`:285` 处理支付成功，`:304` 条件更新订单状态，`:313` 调用支付后 handler。`:343` 的 `validatePayOrderPaid` 查询支付 API 并核成功状态、金额及 merchantOrderId。
- `yudao-module-pay/src/main/java/cn/iocoder/yudao/module/pay/service/refund/PayRefundServiceImpl.java:93` 创建退款；`:155` 校验支付状态、累计退款金额以及未完成退款。`:137` 附近远程退款异常仍留待回调/轮询确认；调用异常不能直接判定渠道未退款。
- `yudao-module-mall/yudao-module-trade/src/main/java/cn/iocoder/yudao/module/trade/service/aftersale/AfterSaleServiceImpl.java:346` 发起售后退款；`:364` 保持原业务状态待回调；`:386` 完成退款处理；`:425` 查询并校验退款结果、金额与 merchantRefundId。

执行建议：变更订单流程前列出允许的源/目标状态及 handler 副作用。库存、优惠券、积分和退款补偿应沿订单与订单项事件核对。验收至少覆盖被修改转换的成功、重复和非法原状态；涉及退款增加金额超限、部分退款及响应不确定时后续确认，使用模拟渠道完成测试。

## 会员积分

- `yudao-module-member/src/main/java/cn/iocoder/yudao/module/member/controller/admin/user/MemberUserController.java:70` 的 update-point 使用 `member:user:update-point` 权限并调用积分流水服务。
- `yudao-module-member/src/main/java/cn/iocoder/yudao/module/member/service/point/MemberPointRecordServiceImpl.java:68` 的 `createPointRecord` 事务内更新余额并写流水；`:76` 预读余额不足时记录后返回。该方法没有按 bizId 去重。
- `yudao-module-member/src/main/java/cn/iocoder/yudao/module/member/dal/mysql/user/MemberUserMapper.java:96` 的 `updatePointDecr` SQL 按 id 扣减，当前语句没有余额下限条件。不能声称并发扣减已被此语句保护。
- `yudao-module-mall/yudao-module-trade/src/main/java/cn/iocoder/yudao/module/trade/service/order/handler/TradeMemberPointOrderHandler.java:38` 下单扣分，`:44` 收货赠分，`:62`/`:71` 取消补偿，`:82`/`:84` 售后订单项补偿。

执行建议：新增或修复积分场景时先检查上层事件是否去重、余额读写的并发条件和补偿触发次数。验证“调用返回”与流水实际落库是否一致；重复或并发测试应落到余额与业务流水结果，价格计算测试不能代替该验证。这里只记录现有实现边界，不因技能调用擅自修复业务逻辑。

## 测试入口与实际限制

- `yudao-module-pay/src/test/java/cn/iocoder/yudao/module/pay/service/order/PayOrderServiceTest.java:58` 继承 `BaseDbAndRedisUnitTest`，`:600`/`:631` 覆盖重复成功与待支付通知场景。
- `yudao-module-pay/src/test/java/cn/iocoder/yudao/module/pay/service/refund/PayRefundServiceTest.java:57` 同样使用数据库/Redis 测试基类，`:248` 金额超限，`:267` 已有进行中退款，`:474` 重复成功。
- `yudao-module-mall/yudao-module-trade/src/test/java/cn/iocoder/yudao/module/trade/service/price/calculator/TradePointUsePriceCalculatorTest.java:259` 是积分价格计算不足场景，非积分流水并发测试。
- 以下类在核验时带类级 `@Disabled`：`yudao-module-pay/src/test/java/cn/iocoder/yudao/module/pay/service/notify/PayNotifyServiceTest.java:50`；`yudao-module-mall/yudao-module-trade/src/test/java/cn/iocoder/yudao/module/trade/service/order/TradeOrderUpdateServiceTest.java:56`；同 trade 测试包 `service/aftersale/AfterSaleServiceTest.java:45`；`yudao-module-member/src/test/java/cn/iocoder/yudao/module/member/service/user/MemberUserServiceImplTest.java:34`。

运行前先确认模块参与 reactor、测试前置数据库/Redis和禁用状态；只报告实际执行结果，不能把存在文件或跳过测试计作通过。
