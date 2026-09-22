# 芋道文档导航索引

由 `scripts/docs_index.py render` 根据 [docs-index.json](docs-index.json) 生成。

收录 27 个分组、382 个目录项：51 项有已知 URL，331 项的具体 URL 待定位；6 页正文此前已读，2 页此前访问受限。

导航来源：本任务先前轮次的外部 Chrome 侧栏记录，结合当前源码中的官方链接。观察日期：2026-09-22。

本轮刷新状态：blocked。本轮未重新抓取官网。未掌握的具体URL保留null，不能将标题收录等同正文阅读。

标题收录不等于正文已读；源码提供的链接也不等于网页可访问。根据任务先读对应技能，再通过允许的浏览器核对需要的页面。

快速查找：`python scripts/docs_index.py search 租户 --json`；按技能筛选：`python scripts/docs_index.py search --skill yudao-codegen`。

## 分组概览

| 分组 | 项数 | 已知 URL |
| --- | ---: | ---: |
| 萌新必读 | 19 | 9 |
| 后端手册 | 36 | 6 |
| 中间件手册 | 7 | 1 |
| 工作流手册 | 17 | 1 |
| 大屏手册 | 2 | 1 |
| 支付手册 | 10 | 1 |
| 会员手册 | 8 | 0 |
| 商城手册 | 24 | 2 |
| ERP 手册 | 10 | 2 |
| CRM 手册 | 11 | 2 |
| AI 大模型手册 | 39 | 2 |
| IoT 物联网手册 | 22 | 1 |
| MES 手册 | 36 | 2 |
| WMS 手册 | 12 | 2 |
| HRM 人力资源 | 12 | 2 |
| FMS 财务管理 | 10 | 2 |
| PMS 项目管理 | 8 | 2 |
| OA 协同办公 | 12 | 2 |
| IM 即时通讯手册 | 10 | 2 |
| 公众号手册 | 12 | 1 |
| 系统手册 | 7 | 0 |
| 运维手册 | 9 | 0 |
| 前端手册 Vue 3.x | 11 | 2 |
| 前端手册 Vben 5.x | 9 | 2 |
| 前端手册 Vue 2.x | 7 | 2 |
| 前端手册 Admin Uniapp | 9 | 2 |
| 更新日志 | 13 | 0 |

## 萌新必读

| 文档 | 任务技能 | 阅读状态 |
| --- | --- | --- |
| 简介（URL 待定位） | [yudao-bootstrap](../skills/yudao-bootstrap/SKILL.md) | 正文未读 |
| 交流群（URL 待定位） | [yudao-bootstrap](../skills/yudao-bootstrap/SKILL.md) | 正文未读 |
| [视频教程](https://doc.iocoder.cn/video/) | [yudao-bootstrap](../skills/yudao-bootstrap/SKILL.md) | 正文未读 |
| 功能列表（URL 待定位） | [yudao-bootstrap](../skills/yudao-bootstrap/SKILL.md) | 正文未读 |
| [快速启动（后端项目）](https://doc.iocoder.cn/quick-start/) | [yudao-bootstrap](../skills/yudao-bootstrap/SKILL.md) | 正文已读（此前核验） |
| [快速启动（前端项目）](https://doc.iocoder.cn/quick-start-front/) | [yudao-bootstrap](../skills/yudao-bootstrap/SKILL.md) | 正文已读（此前核验） |
| [接口文档](https://doc.iocoder.cn/api-doc/) | [yudao-bootstrap](../skills/yudao-bootstrap/SKILL.md) | 正文未读 |
| [技术选型](https://doc.iocoder.cn/technology/) | [yudao-bootstrap](../skills/yudao-bootstrap/SKILL.md) | 正文未读 |
| [项目结构](https://doc.iocoder.cn/project-intro/) | [yudao-bootstrap](../skills/yudao-bootstrap/SKILL.md) | 正文已读（此前核验） |
| 代码热加载（URL 待定位） | [yudao-bootstrap](../skills/yudao-bootstrap/SKILL.md) | 正文未读 |
| 一键改包（URL 待定位） | [yudao-bootstrap](../skills/yudao-bootstrap/SKILL.md) | 正文未读 |
| [迁移模块（适合新项目）](https://doc.iocoder.cn/migrate-module/) | [yudao-bootstrap](../skills/yudao-bootstrap/SKILL.md) | 正文未读 |
| [删除功能（以租户为例）](https://doc.iocoder.cn/delete-code/) | [yudao-delete-tenant](../skills/yudao-delete-tenant/SKILL.md) | 正文未读 |
| [表结构变更（版本升级）](https://doc.iocoder.cn/sql-update/) | [yudao-database](../skills/yudao-database/SKILL.md) | 正文已读（此前核验） |
| 国产信创数据库（DM 达梦、大金、OpenGauss、瀚高）（URL 待定位） | [yudao-database](../skills/yudao-database/SKILL.md) | 正文未读 |
| 如何去除 Redis 缓存（URL 待定位） | [yudao-async](../skills/yudao-async/SKILL.md) | 正文未读 |
| 内网穿透（URL 待定位） | [yudao-bootstrap](../skills/yudao-bootstrap/SKILL.md) | 正文未读 |
| 面试题、简历模版、简历优化（URL 待定位） | [yudao-bootstrap](../skills/yudao-bootstrap/SKILL.md) | 正文未读 |
| 项目外包（URL 待定位） | [yudao-bootstrap](../skills/yudao-bootstrap/SKILL.md) | 正文未读 |

## 后端手册

| 文档 | 任务技能 | 阅读状态 |
| --- | --- | --- |
| [新建模块](https://doc.iocoder.cn/module-new/) | [yudao-codegen](../skills/yudao-codegen/SKILL.md) | 此前访问受限 |
| 代码生成【单表】（新增功能）（URL 待定位） | [yudao-codegen](../skills/yudao-codegen/SKILL.md) | 正文未读 |
| 代码生成【主子表】（URL 待定位） | [yudao-codegen](../skills/yudao-codegen/SKILL.md) | 正文未读 |
| 代码生成（树表）（URL 待定位） | [yudao-codegen](../skills/yudao-codegen/SKILL.md) | 正文未读 |
| 代码生成（移动端）（URL 待定位） | [yudao-codegen](../skills/yudao-codegen/SKILL.md) | 正文未读 |
| [功能权限](https://doc.iocoder.cn/resource-permission/) | [yudao-security](../skills/yudao-security/SKILL.md) | 此前访问受限 |
| 数据权限（URL 待定位） | [yudao-security](../skills/yudao-security/SKILL.md) | 正文未读 |
| 用户体系（URL 待定位） | [yudao-security](../skills/yudao-security/SKILL.md) | 正文未读 |
| 三方登录（URL 待定位） | [yudao-integration](../skills/yudao-integration/SKILL.md) | 正文未读 |
| OAuth 2.0（SSO 单点登录)（URL 待定位） | [yudao-integration](../skills/yudao-integration/SKILL.md) | 正文未读 |
| SaaS 多租户【字段隔离】（URL 待定位） | [yudao-security](../skills/yudao-security/SKILL.md) | 正文未读 |
| SaaS 多租户【数据库隔离】（URL 待定位） | [yudao-security](../skills/yudao-security/SKILL.md) | 正文未读 |
| WebSocket 实时通信（URL 待定位） | [yudao-integration](../skills/yudao-integration/SKILL.md) | 正文未读 |
| 异常处理（错误码）（URL 待定位） | [yudao-backend](../skills/yudao-backend/SKILL.md) | 正文未读 |
| 参数校验、时间传参（URL 待定位） | [yudao-backend](../skills/yudao-backend/SKILL.md) | 正文未读 |
| 分页实现（URL 待定位） | [yudao-backend](../skills/yudao-backend/SKILL.md) | 正文未读 |
| [VO 对象转换、数据翻译](https://doc.iocoder.cn/vo/) | [yudao-backend](../skills/yudao-backend/SKILL.md) | 正文未读 |
| [文件存储（上传下载）](https://doc.iocoder.cn/file/) | [yudao-integration](../skills/yudao-integration/SKILL.md) | 正文未读 |
| Excel 导入导出（URL 待定位） | [yudao-integration](../skills/yudao-integration/SKILL.md) | 正文未读 |
| 操作日志、访问日志、异常日志（URL 待定位） | [yudao-integration](../skills/yudao-integration/SKILL.md) | 正文未读 |
| [MyBatis 数据库](https://doc.iocoder.cn/mybatis/) | [yudao-database](../skills/yudao-database/SKILL.md) | 正文未读 |
| MyBatis 联表&分页查询（URL 待定位） | [yudao-database](../skills/yudao-database/SKILL.md) | 正文未读 |
| 多数据源（读写分离）、事务（URL 待定位） | [yudao-database](../skills/yudao-database/SKILL.md) | 正文未读 |
| Redis 缓存（URL 待定位） | [yudao-async](../skills/yudao-async/SKILL.md) | 正文未读 |
| 本地缓存（URL 待定位） | [yudao-async](../skills/yudao-async/SKILL.md) | 正文未读 |
| 异步任务（URL 待定位） | [yudao-async](../skills/yudao-async/SKILL.md) | 正文未读 |
| 分布式锁（URL 待定位） | [yudao-async](../skills/yudao-async/SKILL.md) | 正文未读 |
| 幂等性（防重复提交）（URL 待定位） | [yudao-async](../skills/yudao-async/SKILL.md) | 正文未读 |
| 请求限流（RateLimiter）（URL 待定位） | [yudao-async](../skills/yudao-async/SKILL.md) | 正文未读 |
| HTTP 接口签名（防篡改）（URL 待定位） | [yudao-security](../skills/yudao-security/SKILL.md) | 正文未读 |
| HTTP 接口加解密（URL 待定位） | [yudao-security](../skills/yudao-security/SKILL.md) | 正文未读 |
| 单元测试（URL 待定位） | [yudao-operations](../skills/yudao-operations/SKILL.md) | 正文未读 |
| 验证码（URL 待定位） | [yudao-security](../skills/yudao-security/SKILL.md) | 正文未读 |
| [工具类 Util](https://doc.iocoder.cn/util/) | [yudao-backend](../skills/yudao-backend/SKILL.md) | 正文未读 |
| 配置管理（URL 待定位） | [yudao-backend](../skills/yudao-backend/SKILL.md) | 正文未读 |
| 数据库文档（URL 待定位） | [yudao-database](../skills/yudao-database/SKILL.md) | 正文未读 |

## 中间件手册

| 文档 | 任务技能 | 阅读状态 |
| --- | --- | --- |
| [定时任务](https://doc.iocoder.cn/job/) | [yudao-async](../skills/yudao-async/SKILL.md) | 正文未读 |
| 消息队列（内存）（URL 待定位） | [yudao-async](../skills/yudao-async/SKILL.md) | 正文未读 |
| 消息队列（Redis）（URL 待定位） | [yudao-async](../skills/yudao-async/SKILL.md) | 正文未读 |
| 消息队列（RocketMQ）（URL 待定位） | [yudao-async](../skills/yudao-async/SKILL.md) | 正文未读 |
| 消息队列（RabbitMQ）（URL 待定位） | [yudao-async](../skills/yudao-async/SKILL.md) | 正文未读 |
| 消息队列（Kafka）（URL 待定位） | [yudao-async](../skills/yudao-async/SKILL.md) | 正文未读 |
| 限流熔断（URL 待定位） | [yudao-async](../skills/yudao-async/SKILL.md) | 正文未读 |

## 工作流手册

| 文档 | 任务技能 | 阅读状态 |
| --- | --- | --- |
| 工作流演示（URL 待定位） | [yudao-workflow](../skills/yudao-workflow/SKILL.md) | 正文未读 |
| [功能开启](https://doc.iocoder.cn/bpm/) | [yudao-workflow](../skills/yudao-workflow/SKILL.md) | 正文未读 |
| 工作流（达梦适配）（URL 待定位） | [yudao-workflow](../skills/yudao-workflow/SKILL.md) | 正文未读 |
| 审批接入（流程表单）（URL 待定位） | [yudao-workflow](../skills/yudao-workflow/SKILL.md) | 正文未读 |
| 审批接入（业务表单）（URL 待定位） | [yudao-workflow](../skills/yudao-workflow/SKILL.md) | 正文未读 |
| 流程设计器（BPMN）（URL 待定位） | [yudao-workflow](../skills/yudao-workflow/SKILL.md) | 正文未读 |
| 流程设计器（钉钉、飞书）（URL 待定位） | [yudao-workflow](../skills/yudao-workflow/SKILL.md) | 正文未读 |
| 选择审批人、发起人自选（URL 待定位） | [yudao-workflow](../skills/yudao-workflow/SKILL.md) | 正文未读 |
| 会签、或签、依次审批（URL 待定位） | [yudao-workflow](../skills/yudao-workflow/SKILL.md) | 正文未读 |
| 流程发起、取消、重新发起（URL 待定位） | [yudao-workflow](../skills/yudao-workflow/SKILL.md) | 正文未读 |
| 审批通过、不通过、驳回（URL 待定位） | [yudao-workflow](../skills/yudao-workflow/SKILL.md) | 正文未读 |
| 审批加签、减签（URL 待定位） | [yudao-workflow](../skills/yudao-workflow/SKILL.md) | 正文未读 |
| 审批转办、委派、抄送（URL 待定位） | [yudao-workflow](../skills/yudao-workflow/SKILL.md) | 正文未读 |
| 执行监听器、任务监听器（URL 待定位） | [yudao-workflow](../skills/yudao-workflow/SKILL.md) | 正文未读 |
| 流程表达式（URL 待定位） | [yudao-workflow](../skills/yudao-workflow/SKILL.md) | 正文未读 |
| 流程审批通知（URL 待定位） | [yudao-workflow](../skills/yudao-workflow/SKILL.md) | 正文未读 |
| 移动端审批（URL 待定位） | [yudao-workflow](../skills/yudao-workflow/SKILL.md) | 正文未读 |

## 大屏手册

| 文档 | 任务技能 | 阅读状态 |
| --- | --- | --- |
| [报表设计器](https://doc.iocoder.cn/report/) | [yudao-integration](../skills/yudao-integration/SKILL.md) | 正文未读 |
| 大屏设计器（URL 待定位） | [yudao-integration](../skills/yudao-integration/SKILL.md) | 正文未读 |

## 支付手册

| 文档 | 任务技能 | 阅读状态 |
| --- | --- | --- |
| [功能开启](https://doc.iocoder.cn/pay/build/) | [yudao-commerce](../skills/yudao-commerce/SKILL.md) | 正文未读 |
| 支付宝支付接入（URL 待定位） | [yudao-commerce](../skills/yudao-commerce/SKILL.md) | 正文未读 |
| 微信公众号支付接入（URL 待定位） | [yudao-commerce](../skills/yudao-commerce/SKILL.md) | 正文未读 |
| 微信小程序支付接入（URL 待定位） | [yudao-commerce](../skills/yudao-commerce/SKILL.md) | 正文未读 |
| 支付宝、微信退款接入（URL 待定位） | [yudao-commerce](../skills/yudao-commerce/SKILL.md) | 正文未读 |
| 支付宝转账接入（URL 待定位） | [yudao-commerce](../skills/yudao-commerce/SKILL.md) | 正文未读 |
| 微信转账接入（URL 待定位） | [yudao-commerce](../skills/yudao-commerce/SKILL.md) | 正文未读 |
| 钱包充值、支付、退款（URL 待定位） | [yudao-commerce](../skills/yudao-commerce/SKILL.md) | 正文未读 |
| 模拟支付、退款（URL 待定位） | [yudao-commerce](../skills/yudao-commerce/SKILL.md) | 正文未读 |
| 移动端支付管理（URL 待定位） | [yudao-commerce](../skills/yudao-commerce/SKILL.md) | 正文未读 |

## 会员手册

| 文档 | 任务技能 | 阅读状态 |
| --- | --- | --- |
| 功能开启（URL 待定位） | [yudao-commerce](../skills/yudao-commerce/SKILL.md) | 正文未读 |
| 微信公众号登录（URL 待定位） | [yudao-commerce](../skills/yudao-commerce/SKILL.md) | 正文未读 |
| 微信小程序登录（URL 待定位） | [yudao-commerce](../skills/yudao-commerce/SKILL.md) | 正文未读 |
| 微信小程序订阅消息（URL 待定位） | [yudao-commerce](../skills/yudao-commerce/SKILL.md) | 正文未读 |
| 微信小程序码（URL 待定位） | [yudao-commerce](../skills/yudao-commerce/SKILL.md) | 正文未读 |
| 会员用户、标签、分组（URL 待定位） | [yudao-commerce](../skills/yudao-commerce/SKILL.md) | 正文未读 |
| 会员等级、积分、签到（URL 待定位） | [yudao-commerce](../skills/yudao-commerce/SKILL.md) | 正文未读 |
| 移动端会员管理（URL 待定位） | [yudao-commerce](../skills/yudao-commerce/SKILL.md) | 正文未读 |

## 商城手册

| 文档 | 任务技能 | 阅读状态 |
| --- | --- | --- |
| [商城演示](https://doc.iocoder.cn/mall-preview/) | [yudao-commerce](../skills/yudao-commerce/SKILL.md) | 正文未读 |
| [功能开启](https://doc.iocoder.cn/mall/build/) | [yudao-commerce](../skills/yudao-commerce/SKILL.md) | 正文未读 |
| 商城装修（URL 待定位） | [yudao-commerce](../skills/yudao-commerce/SKILL.md) | 正文未读 |
| 在线客服（URL 待定位） | [yudao-commerce](../skills/yudao-commerce/SKILL.md) | 正文未读 |
| 【商品】商品分类（URL 待定位） | [yudao-commerce](../skills/yudao-commerce/SKILL.md) | 正文未读 |
| 【商品】商品属性（URL 待定位） | [yudao-commerce](../skills/yudao-commerce/SKILL.md) | 正文未读 |
| 【商品】商品 SPU 与 SKU（URL 待定位） | [yudao-commerce](../skills/yudao-commerce/SKILL.md) | 正文未读 |
| 【商品】商品评价（URL 待定位） | [yudao-commerce](../skills/yudao-commerce/SKILL.md) | 正文未读 |
| 【交易】购物车（URL 待定位） | [yudao-commerce](../skills/yudao-commerce/SKILL.md) | 正文未读 |
| 【交易】交易订单（URL 待定位） | [yudao-commerce](../skills/yudao-commerce/SKILL.md) | 正文未读 |
| 【交易】售后退款（URL 待定位） | [yudao-commerce](../skills/yudao-commerce/SKILL.md) | 正文未读 |
| 【交易】快递发货（URL 待定位） | [yudao-commerce](../skills/yudao-commerce/SKILL.md) | 正文未读 |
| 【交易】门店自提（URL 待定位） | [yudao-commerce](../skills/yudao-commerce/SKILL.md) | 正文未读 |
| 【交易】分销返佣（URL 待定位） | [yudao-commerce](../skills/yudao-commerce/SKILL.md) | 正文未读 |
| 【营销】优惠劵（URL 待定位） | [yudao-commerce](../skills/yudao-commerce/SKILL.md) | 正文未读 |
| 【营销】积分商城（URL 待定位） | [yudao-commerce](../skills/yudao-commerce/SKILL.md) | 正文未读 |
| 【营销】拼团活动（URL 待定位） | [yudao-commerce](../skills/yudao-commerce/SKILL.md) | 正文未读 |
| 【营销】秒杀活动（URL 待定位） | [yudao-commerce](../skills/yudao-commerce/SKILL.md) | 正文未读 |
| 【营销】砍价活动（URL 待定位） | [yudao-commerce](../skills/yudao-commerce/SKILL.md) | 正文未读 |
| 【营销】满减送活动（URL 待定位） | [yudao-commerce](../skills/yudao-commerce/SKILL.md) | 正文未读 |
| 【营销】限时折扣（URL 待定位） | [yudao-commerce](../skills/yudao-commerce/SKILL.md) | 正文未读 |
| 【营销】内容管理（URL 待定位） | [yudao-commerce](../skills/yudao-commerce/SKILL.md) | 正文未读 |
| 【统计】会员、商品、交易统计（URL 待定位） | [yudao-commerce](../skills/yudao-commerce/SKILL.md) | 正文未读 |
| 移动端商城管理（URL 待定位） | [yudao-commerce](../skills/yudao-commerce/SKILL.md) | 正文未读 |

## ERP 手册

| 文档 | 任务技能 | 阅读状态 |
| --- | --- | --- |
| [ERP 演示](https://doc.iocoder.cn/erp-preview/) | [yudao-enterprise](../skills/yudao-enterprise/SKILL.md) | 正文未读 |
| [功能开启](https://doc.iocoder.cn/erp/build/) | [yudao-enterprise](../skills/yudao-enterprise/SKILL.md) | 正文未读 |
| 【产品】产品信息、分类、单位（URL 待定位） | [yudao-enterprise](../skills/yudao-enterprise/SKILL.md) | 正文未读 |
| 【库存】产品库存、库存明细（URL 待定位） | [yudao-enterprise](../skills/yudao-enterprise/SKILL.md) | 正文未读 |
| 【库存】其它入库、其它出库（URL 待定位） | [yudao-enterprise](../skills/yudao-enterprise/SKILL.md) | 正文未读 |
| 【库存】库存调拨、库存盘点（URL 待定位） | [yudao-enterprise](../skills/yudao-enterprise/SKILL.md) | 正文未读 |
| 【采购】采购订单、入库、退货（URL 待定位） | [yudao-enterprise](../skills/yudao-enterprise/SKILL.md) | 正文未读 |
| 【销售】销售订单、出库、退货（URL 待定位） | [yudao-enterprise](../skills/yudao-enterprise/SKILL.md) | 正文未读 |
| 【财务】采购付款、销售收款（URL 待定位） | [yudao-enterprise](../skills/yudao-enterprise/SKILL.md) | 正文未读 |
| 移动端 ERP（URL 待定位） | [yudao-enterprise](../skills/yudao-enterprise/SKILL.md) | 正文未读 |

## CRM 手册

| 文档 | 任务技能 | 阅读状态 |
| --- | --- | --- |
| [CRM 演示](https://doc.iocoder.cn/crm-preview/) | [yudao-enterprise](../skills/yudao-enterprise/SKILL.md) | 正文未读 |
| [功能开启](https://doc.iocoder.cn/crm/build/) | [yudao-enterprise](../skills/yudao-enterprise/SKILL.md) | 正文未读 |
| 【线索】线索管理（URL 待定位） | [yudao-enterprise](../skills/yudao-enterprise/SKILL.md) | 正文未读 |
| 【客户】客户管理、公海客户（URL 待定位） | [yudao-enterprise](../skills/yudao-enterprise/SKILL.md) | 正文未读 |
| 【商机】商机管理、商机状态（URL 待定位） | [yudao-enterprise](../skills/yudao-enterprise/SKILL.md) | 正文未读 |
| 【合同】合同管理、合同提醒（URL 待定位） | [yudao-enterprise](../skills/yudao-enterprise/SKILL.md) | 正文未读 |
| 【回款】回款管理、回款计划（URL 待定位） | [yudao-enterprise](../skills/yudao-enterprise/SKILL.md) | 正文未读 |
| 【产品】产品管理、产品分类（URL 待定位） | [yudao-enterprise](../skills/yudao-enterprise/SKILL.md) | 正文未读 |
| 【通用】数据权限（URL 待定位） | [yudao-enterprise](../skills/yudao-enterprise/SKILL.md) | 正文未读 |
| 【通用】跟进记录、待办事项（URL 待定位） | [yudao-enterprise](../skills/yudao-enterprise/SKILL.md) | 正文未读 |
| 移动端 CRM（URL 待定位） | [yudao-enterprise](../skills/yudao-enterprise/SKILL.md) | 正文未读 |

## AI 大模型手册

| 文档 | 任务技能 | 阅读状态 |
| --- | --- | --- |
| [AI 大模型演示](https://doc.iocoder.cn/ai-preview/) | [yudao-ai](../skills/yudao-ai/SKILL.md) | 正文未读 |
| [功能开启](https://doc.iocoder.cn/ai/build/) | [yudao-ai](../skills/yudao-ai/SKILL.md) | 正文未读 |
| AI 聊天对话（URL 待定位） | [yudao-ai](../skills/yudao-ai/SKILL.md) | 正文未读 |
| AI 绘画创作（URL 待定位） | [yudao-ai](../skills/yudao-ai/SKILL.md) | 正文未读 |
| AI 知识库（RAG）（URL 待定位） | [yudao-ai](../skills/yudao-ai/SKILL.md) | 正文未读 |
| AI 音乐创作（URL 待定位） | [yudao-ai](../skills/yudao-ai/SKILL.md) | 正文未读 |
| AI 写作助手（URL 待定位） | [yudao-ai](../skills/yudao-ai/SKILL.md) | 正文未读 |
| AI 思维导图（URL 待定位） | [yudao-ai](../skills/yudao-ai/SKILL.md) | 正文未读 |
| AI 工具（function calling）（URL 待定位） | [yudao-ai](../skills/yudao-ai/SKILL.md) | 正文未读 |
| AI 工作流（URL 待定位） | [yudao-ai](../skills/yudao-ai/SKILL.md) | 正文未读 |
| Dify 工作流（URL 待定位） | [yudao-ai](../skills/yudao-ai/SKILL.md) | 正文未读 |
| FastGPT 工作流（URL 待定位） | [yudao-ai](../skills/yudao-ai/SKILL.md) | 正文未读 |
| Coze 智能体（URL 待定位） | [yudao-ai](../skills/yudao-ai/SKILL.md) | 正文未读 |
| 推理模式（thinking）（URL 待定位） | [yudao-ai](../skills/yudao-ai/SKILL.md) | 正文未读 |
| 联网搜索（URL 待定位） | [yudao-ai](../skills/yudao-ai/SKILL.md) | 正文未读 |
| MCP Client 客户端（URL 待定位） | [yudao-ai](../skills/yudao-ai/SKILL.md) | 正文未读 |
| MCP Server 服务端（URL 待定位） | [yudao-ai](../skills/yudao-ai/SKILL.md) | 正文未读 |
| 【模型接入】Claude（URL 待定位） | [yudao-ai](../skills/yudao-ai/SKILL.md) | 正文未读 |
| 【模型接入】OpenAI（URL 待定位） | [yudao-ai](../skills/yudao-ai/SKILL.md) | 正文未读 |
| 【模型接入】通义千问（URL 待定位） | [yudao-ai](../skills/yudao-ai/SKILL.md) | 正文未读 |
| 【模型接入】DeepSeek（URL 待定位） | [yudao-ai](../skills/yudao-ai/SKILL.md) | 正文未读 |
| 【模型接入】字节豆包（URL 待定位） | [yudao-ai](../skills/yudao-ai/SKILL.md) | 正文未读 |
| 【模型接入】腾讯混元（URL 待定位） | [yudao-ai](../skills/yudao-ai/SKILL.md) | 正文未读 |
| 【模型接入】硅基流动（URL 待定位） | [yudao-ai](../skills/yudao-ai/SKILL.md) | 正文未读 |
| 【模型接入】MiniMax（URL 待定位） | [yudao-ai](../skills/yudao-ai/SKILL.md) | 正文未读 |
| 【模型接入】月之暗面（URL 待定位） | [yudao-ai](../skills/yudao-ai/SKILL.md) | 正文未读 |
| 【模型接入】百川智能（URL 待定位） | [yudao-ai](../skills/yudao-ai/SKILL.md) | 正文未读 |
| 【模型接入】文心一言（URL 待定位） | [yudao-ai](../skills/yudao-ai/SKILL.md) | 正文未读 |
| 【模型接入】LLAMA（URL 待定位） | [yudao-ai](../skills/yudao-ai/SKILL.md) | 正文未读 |
| 【模型接入】智谱 GLM（URL 待定位） | [yudao-ai](../skills/yudao-ai/SKILL.md) | 正文未读 |
| 【模型接入】讯飞星火（URL 待定位） | [yudao-ai](../skills/yudao-ai/SKILL.md) | 正文未读 |
| 【模型接入】微软 OpenAI（URL 待定位） | [yudao-ai](../skills/yudao-ai/SKILL.md) | 正文未读 |
| 【模型接入】谷歌 Gemini（URL 待定位） | [yudao-ai](../skills/yudao-ai/SKILL.md) | 正文未读 |
| 【模型接入】Stable Diffusion（URL 待定位） | [yudao-ai](../skills/yudao-ai/SKILL.md) | 正文未读 |
| 【模型接入】Midjourney（URL 待定位） | [yudao-ai](../skills/yudao-ai/SKILL.md) | 正文未读 |
| 【模型接入】Suno（URL 待定位） | [yudao-ai](../skills/yudao-ai/SKILL.md) | 正文未读 |
| 【模型接入】Grok（URL 待定位） | [yudao-ai](../skills/yudao-ai/SKILL.md) | 正文未读 |
| 【模型接入】阶跃星辰（URL 待定位） | [yudao-ai](../skills/yudao-ai/SKILL.md) | 正文未读 |
| 移动端 AI 大模型（URL 待定位） | [yudao-ai](../skills/yudao-ai/SKILL.md) | 正文未读 |

## IoT 物联网手册

| 文档 | 任务技能 | 阅读状态 |
| --- | --- | --- |
| [功能开启](https://doc.iocoder.cn/iot/build/) | [yudao-iot](../skills/yudao-iot/SKILL.md) | 正文未读 |
| 产品管理（URL 待定位） | [yudao-iot](../skills/yudao-iot/SKILL.md) | 正文未读 |
| 设备管理（URL 待定位） | [yudao-iot](../skills/yudao-iot/SKILL.md) | 正文未读 |
| 物模型配置（URL 待定位） | [yudao-iot](../skills/yudao-iot/SKILL.md) | 正文未读 |
| 设备网关与子设备（URL 待定位） | [yudao-iot](../skills/yudao-iot/SKILL.md) | 正文未读 |
| 设备动态注册（URL 待定位） | [yudao-iot](../skills/yudao-iot/SKILL.md) | 正文未读 |
| 设备接入（概述）（URL 待定位） | [yudao-iot](../skills/yudao-iot/SKILL.md) | 正文未读 |
| 设备接入（HTTP 协议）（URL 待定位） | [yudao-iot](../skills/yudao-iot/SKILL.md) | 正文未读 |
| 设备接入（MQTT 协议）（URL 待定位） | [yudao-iot](../skills/yudao-iot/SKILL.md) | 正文未读 |
| 设备接入（EMQX 协议）（URL 待定位） | [yudao-iot](../skills/yudao-iot/SKILL.md) | 正文未读 |
| 设备接入（TCP 协议）（URL 待定位） | [yudao-iot](../skills/yudao-iot/SKILL.md) | 正文未读 |
| 设备接入（UDP 协议）（URL 待定位） | [yudao-iot](../skills/yudao-iot/SKILL.md) | 正文未读 |
| 设备接入（WebSocket 协议）（URL 待定位） | [yudao-iot](../skills/yudao-iot/SKILL.md) | 正文未读 |
| 设备接入（CoAP 协议）（URL 待定位） | [yudao-iot](../skills/yudao-iot/SKILL.md) | 正文未读 |
| 设备接入（Modbus Client 模式）（URL 待定位） | [yudao-iot](../skills/yudao-iot/SKILL.md) | 正文未读 |
| 设备接入（Modbus Server 模式）（URL 待定位） | [yudao-iot](../skills/yudao-iot/SKILL.md) | 正文未读 |
| 设备接入（自定义协议）（URL 待定位） | [yudao-iot](../skills/yudao-iot/SKILL.md) | 正文未读 |
| 场景联动（URL 待定位） | [yudao-iot](../skills/yudao-iot/SKILL.md) | 正文未读 |
| 数据流转（URL 待定位） | [yudao-iot](../skills/yudao-iot/SKILL.md) | 正文未读 |
| 告警配置（URL 待定位） | [yudao-iot](../skills/yudao-iot/SKILL.md) | 正文未读 |
| OTA 固件升级（URL 待定位） | [yudao-iot](../skills/yudao-iot/SKILL.md) | 正文未读 |
| 移动端 IoT 物联网（URL 待定位） | [yudao-iot](../skills/yudao-iot/SKILL.md) | 正文未读 |

## MES 手册

| 文档 | 任务技能 | 阅读状态 |
| --- | --- | --- |
| [MES 演示](https://doc.iocoder.cn/mes-preview/) | [yudao-enterprise](../skills/yudao-enterprise/SKILL.md) | 正文未读 |
| [功能开启](https://doc.iocoder.cn/mes/build/) | [yudao-enterprise](../skills/yudao-enterprise/SKILL.md) | 正文未读 |
| 【基础】物料产品、分类、计量单位（URL 待定位） | [yudao-enterprise](../skills/yudao-enterprise/SKILL.md) | 正文未读 |
| 【基础】客户管理、供应商管理（URL 待定位） | [yudao-enterprise](../skills/yudao-enterprise/SKILL.md) | 正文未读 |
| 【基础】车间设置、工作站设置（URL 待定位） | [yudao-enterprise](../skills/yudao-enterprise/SKILL.md) | 正文未读 |
| 【基础】编码规则（URL 待定位） | [yudao-enterprise](../skills/yudao-enterprise/SKILL.md) | 正文未读 |
| 【生产】工序设置、工艺流程（URL 待定位） | [yudao-enterprise](../skills/yudao-enterprise/SKILL.md) | 正文未读 |
| 【生产】生产工单（URL 待定位） | [yudao-enterprise](../skills/yudao-enterprise/SKILL.md) | 正文未读 |
| 【生产】生产排产、工序流转卡（URL 待定位） | [yudao-enterprise](../skills/yudao-enterprise/SKILL.md) | 正文未读 |
| 【生产】生产报工（URL 待定位） | [yudao-enterprise](../skills/yudao-enterprise/SKILL.md) | 正文未读 |
| 【生产】安灯配置、安灯呼叫（URL 待定位） | [yudao-enterprise](../skills/yudao-enterprise/SKILL.md) | 正文未读 |
| 【生产】工作记录（URL 待定位） | [yudao-enterprise](../skills/yudao-enterprise/SKILL.md) | 正文未读 |
| 【仓库】仓库与库区库位、条码赋码、SN码（URL 待定位） | [yudao-enterprise](../skills/yudao-enterprise/SKILL.md) | 正文未读 |
| 【仓库】批次管理、库存现有量、库存事务（URL 待定位） | [yudao-enterprise](../skills/yudao-enterprise/SKILL.md) | 正文未读 |
| 【仓库】到货通知、采购入库、采购退货（URL 待定位） | [yudao-enterprise](../skills/yudao-enterprise/SKILL.md) | 正文未读 |
| 【仓库】生产领料、生产退料、物料消耗（URL 待定位） | [yudao-enterprise](../skills/yudao-enterprise/SKILL.md) | 正文未读 |
| 【仓库】产品产出、产品入库（URL 待定位） | [yudao-enterprise](../skills/yudao-enterprise/SKILL.md) | 正文未读 |
| 【仓库】发货通知、销售出库、销售退货（URL 待定位） | [yudao-enterprise](../skills/yudao-enterprise/SKILL.md) | 正文未读 |
| 【仓库】外协发料、外协入库（URL 待定位） | [yudao-enterprise](../skills/yudao-enterprise/SKILL.md) | 正文未读 |
| 【仓库】其他入库、其他出库（URL 待定位） | [yudao-enterprise](../skills/yudao-enterprise/SKILL.md) | 正文未读 |
| 【仓库】调拨单、装箱管理（URL 待定位） | [yudao-enterprise](../skills/yudao-enterprise/SKILL.md) | 正文未读 |
| 【仓库】库存盘点（URL 待定位） | [yudao-enterprise](../skills/yudao-enterprise/SKILL.md) | 正文未读 |
| 【质量】检测项设置、常见缺陷（URL 待定位） | [yudao-enterprise](../skills/yudao-enterprise/SKILL.md) | 正文未读 |
| 【质量】质检方案（URL 待定位） | [yudao-enterprise](../skills/yudao-enterprise/SKILL.md) | 正文未读 |
| 【质量】来料检验（IQC）（URL 待定位） | [yudao-enterprise](../skills/yudao-enterprise/SKILL.md) | 正文未读 |
| 【质量】过程检验（IPQC）（URL 待定位） | [yudao-enterprise](../skills/yudao-enterprise/SKILL.md) | 正文未读 |
| 【质量】出货检验（OQC）（URL 待定位） | [yudao-enterprise](../skills/yudao-enterprise/SKILL.md) | 正文未读 |
| 【质量】退货检验（RQC）（URL 待定位） | [yudao-enterprise](../skills/yudao-enterprise/SKILL.md) | 正文未读 |
| 【质量】待检任务、检验结果、缺陷记录（URL 待定位） | [yudao-enterprise](../skills/yudao-enterprise/SKILL.md) | 正文未读 |
| 【设备】设备类型、设备台账（URL 待定位） | [yudao-enterprise](../skills/yudao-enterprise/SKILL.md) | 正文未读 |
| 【设备】点检保养项目、点检保养方案（URL 待定位） | [yudao-enterprise](../skills/yudao-enterprise/SKILL.md) | 正文未读 |
| 【设备】点检记录、保养记录、维修单（URL 待定位） | [yudao-enterprise](../skills/yudao-enterprise/SKILL.md) | 正文未读 |
| 【工具】工具类型、工装夹具台账（URL 待定位） | [yudao-enterprise](../skills/yudao-enterprise/SKILL.md) | 正文未读 |
| 【排班】班组设置、节假日设置（URL 待定位） | [yudao-enterprise](../skills/yudao-enterprise/SKILL.md) | 正文未读 |
| 【排班】排班计划、排班日历（URL 待定位） | [yudao-enterprise](../skills/yudao-enterprise/SKILL.md) | 正文未读 |
| 移动端 MES（URL 待定位） | [yudao-enterprise](../skills/yudao-enterprise/SKILL.md) | 正文未读 |

## WMS 手册

| 文档 | 任务技能 | 阅读状态 |
| --- | --- | --- |
| [WMS 演示](https://doc.iocoder.cn/wms-preview/) | [yudao-enterprise](../skills/yudao-enterprise/SKILL.md) | 正文未读 |
| [功能开启](https://doc.iocoder.cn/wms/build/) | [yudao-enterprise](../skills/yudao-enterprise/SKILL.md) | 正文未读 |
| 【基础】仓库（URL 待定位） | [yudao-enterprise](../skills/yudao-enterprise/SKILL.md) | 正文未读 |
| 【基础】商品、SKU、分类、品牌（URL 待定位） | [yudao-enterprise](../skills/yudao-enterprise/SKILL.md) | 正文未读 |
| 【基础】往来企业（供应商、客户）（URL 待定位） | [yudao-enterprise](../skills/yudao-enterprise/SKILL.md) | 正文未读 |
| 【库存】库存记录、流水、统计（URL 待定位） | [yudao-enterprise](../skills/yudao-enterprise/SKILL.md) | 正文未读 |
| 【单据】入库（URL 待定位） | [yudao-enterprise](../skills/yudao-enterprise/SKILL.md) | 正文未读 |
| 【单据】出库（URL 待定位） | [yudao-enterprise](../skills/yudao-enterprise/SKILL.md) | 正文未读 |
| 【单据】移库（URL 待定位） | [yudao-enterprise](../skills/yudao-enterprise/SKILL.md) | 正文未读 |
| 【单据】盘库（URL 待定位） | [yudao-enterprise](../skills/yudao-enterprise/SKILL.md) | 正文未读 |
| 【其它】WMS、MES、ERP 对比（URL 待定位） | [yudao-enterprise](../skills/yudao-enterprise/SKILL.md) | 正文未读 |
| 移动端 WMS（URL 待定位） | [yudao-enterprise](../skills/yudao-enterprise/SKILL.md) | 正文未读 |

## HRM 人力资源

| 文档 | 任务技能 | 阅读状态 |
| --- | --- | --- |
| [HRM 演示](https://doc.iocoder.cn/hrm-preview/) | [yudao-enterprise](../skills/yudao-enterprise/SKILL.md) | 正文未读 |
| [功能开启](https://doc.iocoder.cn/hrm/build/) | [yudao-enterprise](../skills/yudao-enterprise/SKILL.md) | 正文未读 |
| 【组织】工作台、组织架构（URL 待定位） | [yudao-enterprise](../skills/yudao-enterprise/SKILL.md) | 正文未读 |
| 【员工】员工管理（URL 待定位） | [yudao-enterprise](../skills/yudao-enterprise/SKILL.md) | 正文未读 |
| 【招聘】招聘管理（URL 待定位） | [yudao-enterprise](../skills/yudao-enterprise/SKILL.md) | 正文未读 |
| 【考勤】考勤管理（URL 待定位） | [yudao-enterprise](../skills/yudao-enterprise/SKILL.md) | 正文未读 |
| 【社保】社保管理（URL 待定位） | [yudao-enterprise](../skills/yudao-enterprise/SKILL.md) | 正文未读 |
| 【薪资】计薪设置、薪资档案（URL 待定位） | [yudao-enterprise](../skills/yudao-enterprise/SKILL.md) | 正文未读 |
| 【薪资】月度工资、工资条（URL 待定位） | [yudao-enterprise](../skills/yudao-enterprise/SKILL.md) | 正文未读 |
| 【绩效】绩效模板、绩效计划（URL 待定位） | [yudao-enterprise](../skills/yudao-enterprise/SKILL.md) | 正文未读 |
| 【绩效】绩效考核、绩效档案（URL 待定位） | [yudao-enterprise](../skills/yudao-enterprise/SKILL.md) | 正文未读 |
| 移动端 HRM（URL 待定位） | [yudao-enterprise](../skills/yudao-enterprise/SKILL.md) | 正文未读 |

## FMS 财务管理

| 文档 | 任务技能 | 阅读状态 |
| --- | --- | --- |
| [FMS 演示](https://doc.iocoder.cn/fms-preview/) | [yudao-enterprise](../skills/yudao-enterprise/SKILL.md) | 正文未读 |
| [功能开启](https://doc.iocoder.cn/fms/build/) | [yudao-enterprise](../skills/yudao-enterprise/SKILL.md) | 正文未读 |
| 【设置】账套管理、财务参数、财务指标（URL 待定位） | [yudao-enterprise](../skills/yudao-enterprise/SKILL.md) | 正文未读 |
| 【设置】币别、科目、辅助核算、初始余额（URL 待定位） | [yudao-enterprise](../skills/yudao-enterprise/SKILL.md) | 正文未读 |
| 【设置】凭证字、常用摘要、凭证模板（URL 待定位） | [yudao-enterprise](../skills/yudao-enterprise/SKILL.md) | 正文未读 |
| 【凭证】凭证管理（URL 待定位） | [yudao-enterprise](../skills/yudao-enterprise/SKILL.md) | 正文未读 |
| 【账簿】账簿管理（URL 待定位） | [yudao-enterprise](../skills/yudao-enterprise/SKILL.md) | 正文未读 |
| 【报表】财务报表（URL 待定位） | [yudao-enterprise](../skills/yudao-enterprise/SKILL.md) | 正文未读 |
| 【结账】期末结账（URL 待定位） | [yudao-enterprise](../skills/yudao-enterprise/SKILL.md) | 正文未读 |
| 移动端 FMS（URL 待定位） | [yudao-enterprise](../skills/yudao-enterprise/SKILL.md) | 正文未读 |

## PMS 项目管理

| 文档 | 任务技能 | 阅读状态 |
| --- | --- | --- |
| [PMS 演示](https://doc.iocoder.cn/pms-preview/) | [yudao-enterprise](../skills/yudao-enterprise/SKILL.md) | 正文未读 |
| [功能开启](https://doc.iocoder.cn/pms/build/) | [yudao-enterprise](../skills/yudao-enterprise/SKILL.md) | 正文未读 |
| 【项目中心】工作台与项目管理（URL 待定位） | [yudao-enterprise](../skills/yudao-enterprise/SKILL.md) | 正文未读 |
| 【项目中心】项目详情与迭代（URL 待定位） | [yudao-enterprise](../skills/yudao-enterprise/SKILL.md) | 正文未读 |
| 【项目中心】工作项与协作（URL 待定位） | [yudao-enterprise](../skills/yudao-enterprise/SKILL.md) | 正文未读 |
| 【知识中心】知识库管理（URL 待定位） | [yudao-enterprise](../skills/yudao-enterprise/SKILL.md) | 正文未读 |
| 【知识中心】文档与协作（URL 待定位） | [yudao-enterprise](../skills/yudao-enterprise/SKILL.md) | 正文未读 |
| 移动端 PMS（URL 待定位） | [yudao-enterprise](../skills/yudao-enterprise/SKILL.md) | 正文未读 |

## OA 协同办公

| 文档 | 任务技能 | 阅读状态 |
| --- | --- | --- |
| [OA 演示](https://doc.iocoder.cn/oa-preview/) | [yudao-enterprise](../skills/yudao-enterprise/SKILL.md) | 正文未读 |
| [功能开启](https://doc.iocoder.cn/oa/build/) | [yudao-enterprise](../skills/yudao-enterprise/SKILL.md) | 正文未读 |
| 【协作】日程、任务、计划与汇报（URL 待定位） | [yudao-enterprise](../skills/yudao-enterprise/SKILL.md) | 正文未读 |
| 【协作】公告、讨论、通讯录与笔记（URL 待定位） | [yudao-enterprise](../skills/yudao-enterprise/SKILL.md) | 正文未读 |
| 【办公】企业邮箱（URL 待定位） | [yudao-enterprise](../skills/yudao-enterprise/SKILL.md) | 正文未读 |
| 【办公】企业云盘（URL 待定位） | [yudao-enterprise](../skills/yudao-enterprise/SKILL.md) | 正文未读 |
| 【行政】办公用品、用印管理（URL 待定位） | [yudao-enterprise](../skills/yudao-enterprise/SKILL.md) | 正文未读 |
| 【行政】会议室、车辆管理（URL 待定位） | [yudao-enterprise](../skills/yudao-enterprise/SKILL.md) | 正文未读 |
| 【流程】公文管理（URL 待定位） | [yudao-enterprise](../skills/yudao-enterprise/SKILL.md) | 正文未读 |
| 【流程】出差、费用报销（URL 待定位） | [yudao-enterprise](../skills/yudao-enterprise/SKILL.md) | 正文未读 |
| 【流程】考勤、请假、加班、转正与离职（URL 待定位） | [yudao-enterprise](../skills/yudao-enterprise/SKILL.md) | 正文未读 |
| 移动端 OA（URL 待定位） | [yudao-enterprise](../skills/yudao-enterprise/SKILL.md) | 正文未读 |

## IM 即时通讯手册

| 文档 | 任务技能 | 阅读状态 |
| --- | --- | --- |
| [IM 演示](https://doc.iocoder.cn/im-preview/) | [yudao-enterprise](../skills/yudao-enterprise/SKILL.md) | 正文未读 |
| [功能开启](https://doc.iocoder.cn/im/build/) | [yudao-enterprise](../skills/yudao-enterprise/SKILL.md) | 正文未读 |
| 【好友】好友关系、好友申请（URL 待定位） | [yudao-enterprise](../skills/yudao-enterprise/SKILL.md) | 正文未读 |
| 【群聊】群组、群成员、入群申请（URL 待定位） | [yudao-enterprise](../skills/yudao-enterprise/SKILL.md) | 正文未读 |
| 【消息】私聊、群聊、频道消息（URL 待定位） | [yudao-enterprise](../skills/yudao-enterprise/SKILL.md) | 正文未读 |
| 【频道】频道、频道素材（URL 待定位） | [yudao-enterprise](../skills/yudao-enterprise/SKILL.md) | 正文未读 |
| 【内容】表情、敏感词（URL 待定位） | [yudao-enterprise](../skills/yudao-enterprise/SKILL.md) | 正文未读 |
| 【通话】语音通话、视频通话、共享屏幕（URL 待定位） | [yudao-enterprise](../skills/yudao-enterprise/SKILL.md) | 正文未读 |
| 【WebSocket】实时推送与离线消息（URL 待定位） | [yudao-enterprise](../skills/yudao-enterprise/SKILL.md) | 正文未读 |
| 移动端 IM 即时通讯（URL 待定位） | [yudao-enterprise](../skills/yudao-enterprise/SKILL.md) | 正文未读 |

## 公众号手册

| 文档 | 任务技能 | 阅读状态 |
| --- | --- | --- |
| [功能开启](https://doc.iocoder.cn/mp/build/) | [yudao-integration](../skills/yudao-integration/SKILL.md) | 正文未读 |
| 公众号接入（URL 待定位） | [yudao-integration](../skills/yudao-integration/SKILL.md) | 正文未读 |
| 公众号粉丝（URL 待定位） | [yudao-integration](../skills/yudao-integration/SKILL.md) | 正文未读 |
| 公众号标签（URL 待定位） | [yudao-integration](../skills/yudao-integration/SKILL.md) | 正文未读 |
| 公众号消息（URL 待定位） | [yudao-integration](../skills/yudao-integration/SKILL.md) | 正文未读 |
| 模版消息（URL 待定位） | [yudao-integration](../skills/yudao-integration/SKILL.md) | 正文未读 |
| 自动回复（URL 待定位） | [yudao-integration](../skills/yudao-integration/SKILL.md) | 正文未读 |
| 公众号菜单（URL 待定位） | [yudao-integration](../skills/yudao-integration/SKILL.md) | 正文未读 |
| 公众号素材（URL 待定位） | [yudao-integration](../skills/yudao-integration/SKILL.md) | 正文未读 |
| 公众号图文（URL 待定位） | [yudao-integration](../skills/yudao-integration/SKILL.md) | 正文未读 |
| 公众号统计（URL 待定位） | [yudao-integration](../skills/yudao-integration/SKILL.md) | 正文未读 |
| 移动端公众号管理（URL 待定位） | [yudao-integration](../skills/yudao-integration/SKILL.md) | 正文未读 |

## 系统手册

| 文档 | 任务技能 | 阅读状态 |
| --- | --- | --- |
| 短信配置（URL 待定位） | [yudao-integration](../skills/yudao-integration/SKILL.md) | 正文未读 |
| 邮件配置（URL 待定位） | [yudao-integration](../skills/yudao-integration/SKILL.md) | 正文未读 |
| 站内信配置（URL 待定位） | [yudao-integration](../skills/yudao-integration/SKILL.md) | 正文未读 |
| Webhook（钉钉、飞书、企微）（URL 待定位） | [yudao-integration](../skills/yudao-integration/SKILL.md) | 正文未读 |
| 数据脱敏、字段权限（URL 待定位） | [yudao-security](../skills/yudao-security/SKILL.md) | 正文未读 |
| 敏感词（URL 待定位） | [yudao-integration](../skills/yudao-integration/SKILL.md) | 正文未读 |
| 地区 & IP 库（URL 待定位） | [yudao-integration](../skills/yudao-integration/SKILL.md) | 正文未读 |

## 运维手册

| 文档 | 任务技能 | 阅读状态 |
| --- | --- | --- |
| 开发环境（URL 待定位） | [yudao-operations](../skills/yudao-operations/SKILL.md) | 正文未读 |
| Linux 部署（URL 待定位） | [yudao-operations](../skills/yudao-operations/SKILL.md) | 正文未读 |
| Docker 部署（URL 待定位） | [yudao-operations](../skills/yudao-operations/SKILL.md) | 正文未读 |
| Jenkins 部署（URL 待定位） | [yudao-operations](../skills/yudao-operations/SKILL.md) | 正文未读 |
| 宝塔部署（URL 待定位） | [yudao-operations](../skills/yudao-operations/SKILL.md) | 正文未读 |
| 1Panel 部署（URL 待定位） | [yudao-operations](../skills/yudao-operations/SKILL.md) | 正文未读 |
| HTTPS 证书（URL 待定位） | [yudao-operations](../skills/yudao-operations/SKILL.md) | 正文未读 |
| 服务监控（URL 待定位） | [yudao-operations](../skills/yudao-operations/SKILL.md) | 正文未读 |
| Tomcat WAR 部署（URL 待定位） | [yudao-operations](../skills/yudao-operations/SKILL.md) | 正文未读 |

## 前端手册 Vue 3.x

| 文档 | 任务技能 | 阅读状态 |
| --- | --- | --- |
| [开发规范](https://doc.iocoder.cn/vue3/dev-spec/) | [yudao-frontend](../skills/yudao-frontend/SKILL.md) | 正文已读（此前核验） |
| [菜单路由](https://doc.iocoder.cn/vue3/route/) | [yudao-frontend](../skills/yudao-frontend/SKILL.md) | 正文已读（此前核验） |
| Icon 图标（URL 待定位） | [yudao-frontend](../skills/yudao-frontend/SKILL.md) | 正文未读 |
| 字典数据（URL 待定位） | [yudao-frontend](../skills/yudao-frontend/SKILL.md) | 正文未读 |
| 系统组件（URL 待定位） | [yudao-frontend](../skills/yudao-frontend/SKILL.md) | 正文未读 |
| 通用方法（URL 待定位） | [yudao-frontend](../skills/yudao-frontend/SKILL.md) | 正文未读 |
| 配置读取（URL 待定位） | [yudao-frontend](../skills/yudao-frontend/SKILL.md) | 正文未读 |
| CRUD 组件（URL 待定位） | [yudao-frontend](../skills/yudao-frontend/SKILL.md) | 正文未读 |
| 国际化（URL 待定位） | [yudao-frontend](../skills/yudao-frontend/SKILL.md) | 正文未读 |
| IDE 调试（URL 待定位） | [yudao-frontend](../skills/yudao-frontend/SKILL.md) | 正文未读 |
| 代码格式化（URL 待定位） | [yudao-frontend](../skills/yudao-frontend/SKILL.md) | 正文未读 |

## 前端手册 Vben 5.x

| 文档 | 任务技能 | 阅读状态 |
| --- | --- | --- |
| [开发规范](https://doc.iocoder.cn/vben5/dev-spec/) | [yudao-frontend](../skills/yudao-frontend/SKILL.md) | 正文未读 |
| [菜单路由](https://doc.iocoder.cn/vben5/route/) | [yudao-frontend](../skills/yudao-frontend/SKILL.md) | 正文未读 |
| 图标、主题、国际化（URL 待定位） | [yudao-frontend](../skills/yudao-frontend/SKILL.md) | 正文未读 |
| 字典数据（URL 待定位） | [yudao-frontend](../skills/yudao-frontend/SKILL.md) | 正文未读 |
| 系统组件（URL 待定位） | [yudao-frontend](../skills/yudao-frontend/SKILL.md) | 正文未读 |
| 通用方法（URL 待定位） | [yudao-frontend](../skills/yudao-frontend/SKILL.md) | 正文未读 |
| 配置读取（URL 待定位） | [yudao-frontend](../skills/yudao-frontend/SKILL.md) | 正文未读 |
| IDE 调试（URL 待定位） | [yudao-frontend](../skills/yudao-frontend/SKILL.md) | 正文未读 |
| 代码格式化（URL 待定位） | [yudao-frontend](../skills/yudao-frontend/SKILL.md) | 正文未读 |

## 前端手册 Vue 2.x

| 文档 | 任务技能 | 阅读状态 |
| --- | --- | --- |
| [开发规范](https://doc.iocoder.cn/vue2/dev-spec/) | [yudao-frontend](../skills/yudao-frontend/SKILL.md) | 正文未读 |
| [菜单路由](https://doc.iocoder.cn/vue2/route/) | [yudao-frontend](../skills/yudao-frontend/SKILL.md) | 正文未读 |
| Icon 图标（URL 待定位） | [yudao-frontend](../skills/yudao-frontend/SKILL.md) | 正文未读 |
| 字典数据（URL 待定位） | [yudao-frontend](../skills/yudao-frontend/SKILL.md) | 正文未读 |
| 系统组件（URL 待定位） | [yudao-frontend](../skills/yudao-frontend/SKILL.md) | 正文未读 |
| 通用方法（URL 待定位） | [yudao-frontend](../skills/yudao-frontend/SKILL.md) | 正文未读 |
| 配置读取（URL 待定位） | [yudao-frontend](../skills/yudao-frontend/SKILL.md) | 正文未读 |

## 前端手册 Admin Uniapp

| 文档 | 任务技能 | 阅读状态 |
| --- | --- | --- |
| [开发规范](https://doc.iocoder.cn/admin-uniapp/dev-spec/) | [yudao-frontend](../skills/yudao-frontend/SKILL.md) | 正文未读 |
| [菜单路由](https://doc.iocoder.cn/admin-uniapp/route/) | [yudao-frontend](../skills/yudao-frontend/SKILL.md) | 正文未读 |
| 图标、主题、国际化（URL 待定位） | [yudao-frontend](../skills/yudao-frontend/SKILL.md) | 正文未读 |
| 字典数据（URL 待定位） | [yudao-frontend](../skills/yudao-frontend/SKILL.md) | 正文未读 |
| 系统组件（URL 待定位） | [yudao-frontend](../skills/yudao-frontend/SKILL.md) | 正文未读 |
| 通用方法（URL 待定位） | [yudao-frontend](../skills/yudao-frontend/SKILL.md) | 正文未读 |
| IDE 调试（URL 待定位） | [yudao-frontend](../skills/yudao-frontend/SKILL.md) | 正文未读 |
| 代码格式化（URL 待定位） | [yudao-frontend](../skills/yudao-frontend/SKILL.md) | 正文未读 |
| 运行发布（URL 待定位） | [yudao-frontend](../skills/yudao-frontend/SKILL.md) | 正文未读 |

## 更新日志

| 文档 | 任务技能 | 阅读状态 |
| --- | --- | --- |
| 【v2026-09】（URL 待定位） | [yudao-upgrade](../skills/yudao-upgrade/SKILL.md) | 正文未读 |
| 【v2026-08】（URL 待定位） | [yudao-upgrade](../skills/yudao-upgrade/SKILL.md) | 正文未读 |
| 【v2026-07】（URL 待定位） | [yudao-upgrade](../skills/yudao-upgrade/SKILL.md) | 正文未读 |
| 【v2026-06】（URL 待定位） | [yudao-upgrade](../skills/yudao-upgrade/SKILL.md) | 正文未读 |
| 【v2026-05】（URL 待定位） | [yudao-upgrade](../skills/yudao-upgrade/SKILL.md) | 正文未读 |
| 【v2026-04】（URL 待定位） | [yudao-upgrade](../skills/yudao-upgrade/SKILL.md) | 正文未读 |
| 【v2026-03】（URL 待定位） | [yudao-upgrade](../skills/yudao-upgrade/SKILL.md) | 正文未读 |
| 【v2026-01】（URL 待定位） | [yudao-upgrade](../skills/yudao-upgrade/SKILL.md) | 正文未读 |
| 【v2025-12】（URL 待定位） | [yudao-upgrade](../skills/yudao-upgrade/SKILL.md) | 正文未读 |
| 【v2025-11】（URL 待定位） | [yudao-upgrade](../skills/yudao-upgrade/SKILL.md) | 正文未读 |
| 【v2025-10】（URL 待定位） | [yudao-upgrade](../skills/yudao-upgrade/SKILL.md) | 正文未读 |
| 【v2025-09】（URL 待定位） | [yudao-upgrade](../skills/yudao-upgrade/SKILL.md) | 正文未读 |
| 【v2025-08】（URL 待定位） | [yudao-upgrade](../skills/yudao-upgrade/SKILL.md) | 正文未读 |
