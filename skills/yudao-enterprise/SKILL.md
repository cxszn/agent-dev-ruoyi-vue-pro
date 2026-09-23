---
name: yudao-enterprise
description: 按业务边界定位和开发芋道 ruoyi-vue-pro 的 ERP 进销存、CRM 客户、MES 生产、WMS 仓储、HRM 人事、FMS 财务、PMS 项目、OA 办公和 IM 通信。适用于这些企业业务模块的状态、权限、单据及跨模块联动。
---

# 芋道企业业务

涉及芋道项目代码新增方法时，遵守[新增方法注释约定](../../references/method-comments.md)，交付前逐一检查。

先确定用户描述的业务对象与模块：销售库存/采购走 ERP，客户公海/商机合同走 CRM，生产工单走 MES，仓库作业走 WMS，人事薪资走 HRM，账套凭证走 FMS，项目迭代走 PMS，办公申请走 OA，会话消息走 IM。名称相似的库存、客户、用户或单据不能视为同一实体。

按[企业业务工作路径](references/workflow.md)只读当前任务涉及的入口；核根 POM、模块 POM、server 依赖和相关 API。基线中九模块都默认未启用，不把目录存在视为服务可用。

变更前写清操作者、对象归属、允许的原状态、目标状态与副作用，再沿 Controller → Service → Mapper/跨模块 API → 测试追踪。使用现有状态枚举、领域权限和条件更新；不要以通用 CRUD 覆盖审核、入库、入职、结账或消息幂等语义。

OA 或其它业务发起人工审批时配合 `yudao-workflow`；真实财务支付/退款用 `yudao-commerce`；页面变化按当前前端仓库处理。交付包含受影响业务链、状态/权限验证和未运行的环境项，运行中单据调整与数据迁移以任务授权为边界。
