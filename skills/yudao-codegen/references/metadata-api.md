# 生成器元数据与接口

用于配置或调试生成器；不是预授权 API 操作说明。源码基线为 2026-09-22 本地 ruoyi-vue-pro 快照，运行时先核对部署版本、前缀、认证及用户授权。接口与字段来自 `yudao-module-infra/src/main/java/cn/iocoder/yudao/module/infra/controller/admin/codegen/`。

## 四组选项独立配置

| 维度 | 本基线枚举 | 使用方式 |
| --- | --- | --- |
| templateType | ONE=1、TREE=2、MASTER_NORMAL=10、MASTER_ERP=11、MASTER_INNER=12、SUB=15 | 表模型；移动端不属于这一组。 |
| frontType | Vue2 Element UI=10、Vue3 Element Plus=20、Vben2 Antd Schema=30、Vben5 Antd Schema/General=40/41、Antdv Next Schema/General=42/43、Element Plus Schema/General=50/51、Admin UniApp WOT=60 | 同为 Vue3 也需要区分 UI 和 Schema/General。 |
| scene | ADMIN=1、APP=2 | Controller 包/类前缀与权限场景。 |
| voType | VO=10、DO=20 | `yudao.codegen` 配置；影响创建/修改/响应产物，分页请求不在其覆盖范围。 |

依据位于 `yudao-module-infra/src/main/java/cn/iocoder/yudao/module/infra/enums/codegen/`：`CodegenTemplateTypeEnum.java`、`CodegenFrontTypeEnum.java`、`CodegenSceneEnum.java`、`CodegenVOTypeEnum.java`。换版本按枚举复核，不从来源基准推断数字。

## 操作接口

以下路径均在 Controller 相对前缀 `/infra/codegen` 下，实际网络地址还需当前应用前缀。权限前缀均为 `infra:codegen:`。

| 方法与路径 | 参数/响应 | 性质与权限后缀 |
| --- | --- | --- |
| GET `/db/table/list` | query `dataSourceConfigId`，可选 `name/comment`；过滤已导入表 | 读取数据库结构，query |
| GET `/table/list` | query `dataSourceConfigId` | 读取已导入定义，query |
| GET `/detail` | query `tableId` → 表和字段定义 | 读取元数据，query |
| POST `/create-list` | JSON `{dataSourceConfigId, tableNames}` → 元数据 ID 列表 | 写入生成器元数据，create；不创建业务表 |
| PUT `/update` | JSON `{table, columns}` | 修改生成器元数据，update；不等于 ALTER TABLE |
| PUT `/sync-from-db` | query `tableId` | 从当前数据库同步元数据，update；可能重建列配置 |
| GET `/preview` | query `tableId` → 生成文件内容集合 | 预览，preview；不写入业务源码 |
| GET `/download` | query `tableId` → ZIP | 下载，download；不部署代码或执行 SQL |

来源：`CodegenController.java:48`（数据库列表）、`:83`（详情）、`:95`（导入）、`:102`（更新）、`:111`（同步）、`:138`（预览）、`:147`（下载）。带写入性质的接口需匹配已授权环境与对象范围；只要求生成代码不自动授权修改在线生成器配置。

## 元数据字段

`CodegenUpdateReqVO` 包含 `table: CodegenTableSaveReqVO` 与 `columns: CodegenColumnSaveReqVO[]`。更新前读取原始明细，保留 ID 与未修改配置，不凭空构造替换整个对象。

- 表：`id`、`scene`、`tableName/tableComment`、`moduleName/businessName/className/classComment`、`author`、`templateType/frontType`、`parentMenuId`、`remark`。
- 子表：`masterTableId` 是生成器主表定义 ID；`subJoinColumnId` 是子表关联字段的元数据 ID；`subJoinMany` 是是否一对多。它们不是业务数据记录 ID。
- 树表：`treeParentColumnId/treeNameColumnId` 是父键和名称列的元数据 ID。
- 每列结构：`id/tableId`、`columnName/dataType/columnComment`、`nullable/primaryKey/ordinalPosition`、`javaType/javaField`。
- 每列行为：`createOperation/updateOperation/listOperation/listOperationResult`、`listOperationCondition`、`dictType`、`htmlType`、`example`。Java 类型和属性名以实际字段定义为准，VO 中的示例文字不是字段契约。

主子表先核对列确属该子表、父子键类型一致、子表业务字段与主表集合属性无冲突。普通/内嵌模式通常联合保存，ERP 模式独立编辑子记录；按当前模板及生成结果确认事务和权限。树表核对父键可空/根值、循环与删除边界，不能只依赖请求 VO 的校验注解。

`yudao.codegen` 还包含 `basePackage`、`dbSchemas`、`deleteBatchEnable`、`unitTestEnable`、`importEnable`；对生成集合的影响见 [workflow](workflow.md)。字段同步会重建部分列元数据，先保存配置再比较，详见该页的同步说明。
