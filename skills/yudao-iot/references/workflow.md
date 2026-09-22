# IoT 链路与验收

核验日期：2026-09-22；源码基线 `2026.08-jdk25-SNAPSHOT`。路径与行号为当前源码事实；执行方案和验收用例是建议，未作为已运行结果。

源码提供的官方入口：[IoT 启动](https://doc.iocoder.cn/iot/build/)。本轮未访问其正文，协议细节以当前源码与实际配置复核。

## 模块与进程

`yudao-module-iot/pom.xml:9` 聚合 biz/core/gateway。根 `pom.xml:26` 和 `yudao-server/pom.xml:114` 注释 IoT 聚合与业务依赖。`yudao-module-iot/yudao-module-iot-gateway/src/main/java/cn/iocoder/yudao/module/iot/gateway/IotGatewayServerApplication.java:7` 有独立启动类。先核对业务服务、网关、消息中间件与存储的实际配置，按任务范围确认启用状态。

## 任务入口

| 请求 | 源码入口与事实 |
| --- | --- |
| 消息查询/下行 | `yudao-module-iot/yudao-module-iot-biz/src/main/java/cn/iocoder/yudao/module/iot/controller/admin/device/IotDeviceMessageController.java:50` 查询消息，`:87` 发送下行。 |
| 网关消息契约 | `yudao-module-iot/yudao-module-iot-gateway/src/main/java/cn/iocoder/yudao/module/iot/gateway/service/device/message/IotDeviceMessageServiceImpl.java:41` 序列化，`:70` 反序列化，`:98` 发送消息。 |
| 业务消息路由 | `yudao-module-iot/yudao-module-iot-biz/src/main/java/cn/iocoder/yudao/module/iot/service/device/message/IotDeviceMessageServiceImpl.java:123` 分上下行；`:170` 处理上行与响应；`:160` 补充设备 ID 和设备所属租户。 |
| MQTT 接入 | `yudao-module-iot/yudao-module-iot-gateway/src/main/java/cn/iocoder/yudao/module/iot/gateway/protocol/mqtt/IotMqttProtocol.java:43` 实现 `IotProtocol`。其它协议从同级 `protocol` 子目录定位，按真实协议选 handler，避免混用 MQTT 与 EMQX 接入方式。 |
| 物模型 | `yudao-module-iot/yudao-module-iot-biz/src/main/java/cn/iocoder/yudao/module/iot/service/thingmodel/IotThingModelServiceImpl.java:79` 创建；`:98` 更新；`:174` 校验 identifiers；`:189` 转换属性值；`:427` 唯一性校验。 |
| 场景规则 | `yudao-module-iot/yudao-module-iot-biz/src/main/java/cn/iocoder/yudao/module/iot/service/rule/scene/IotSceneRuleServiceImpl.java:200` 根据设备租户运行匹配与动作；`:216` 定时触发先检查规则存在、启用和定时触发器。 |
| 数据流转 | `yudao-module-iot/yudao-module-iot-biz/src/main/java/cn/iocoder/yudao/module/iot/service/rule/data/IotDataRuleServiceImpl.java` 与 `IotDataSinkServiceImpl.java`；按规则与目标分别检查。 |
| OTA | `yudao-module-iot/yudao-module-iot-biz/src/main/java/cn/iocoder/yudao/module/iot/service/ota/IotOtaTaskServiceImpl.java`、`IotOtaTaskRecordServiceImpl.java`、`IotOtaFirmwareServiceImpl.java`；固件、任务及设备记录是不同入口。 |

## 接入和消息排查

1. 固定一条可脱敏的实际报文、设备/产品标识、时间、协议、方向及 requestId；核对设备是直连、网关还是子设备。
2. 沿协议认证/解码 → 网关消息 Service → 消息投递 → 业务处理 → 属性/事件存储和规则追踪，标出首次缺失或变化的字段。
3. 下行追踪业务 Service → 网关 serverId → 协议连接 → 设备应答，不能用后台接口成功代替设备执行成功。
4. 核对重连、未认证、字段类型不匹配、响应关联及规则重复触发等受影响场景，优先复用本模块测试。

源码限制：业务消息 `sendDeviceMessage` 在 `:142` 取得不到 serverId 时抛 `DEVICE_DOWNSTREAM_FAILED_SERVER_ID_NULL`；短连接 PULL 的待拉取消息表只是相邻设计注释，不能告诉用户它已经实现。修复应依据目标协议和已实现链路，不能通过伪造 serverId 掩盖未支持能力。

## 物模型、规则和固件改动

- 物模型 identifier 和属性类型会影响上行转换与 Modbus 点位；更新实现会同步点位冗余字段，改变标识前检查调用者与历史数据。
- 规则需区分设备消息触发、定时触发、数据转发；修改条件与动作后分别验证不匹配、匹配、禁用及设备租户上下文。
- OTA 先核对目标设备集、固件兼容条件、任务记录和失败状态。先在指定测试设备验证下载与状态回报，不能因“维护技能”请求而执行任何固件下发。

## 可用测试与缺口

- `yudao-module-iot/yudao-module-iot-biz/src/test/java/cn/iocoder/yudao/module/iot/service/device/message/IotDeviceMessageServiceImplTest.java:43` 继承 `BaseMockitoUnitTest`；`:120` 检查上行投递，`:136` 检查下行缺少 serverId，`:172` 检查日志表不存在时查询空结果。
- `yudao-module-iot/yudao-module-iot-biz/src/test/java/cn/iocoder/yudao/module/iot/service/thingmodel/IotThingModelServiceImplTest.java` 与 `service/rule/data/IotDataRuleServiceImplTest.java` 可按实际改动选用。
- `yudao-module-iot/yudao-module-iot-gateway/src/test/java/cn/iocoder/yudao/module/iot/gateway/protocol/mqtt/IotDirectDeviceMqttProtocolIntegrationTest.java:51` 带 `@Disabled`，`:88` 认证、`:111` 属性上报、`:144` 事件上报仅证明有示例。

本次未启动模块、连接设备或运行这些测试。以后交付分别报告业务单测、协议集成与受控设备验收；测试环境缺少某层时明确未验证项。
