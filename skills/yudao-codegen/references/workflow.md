# 新模块与代码生成工作流

源码核验日：2026-09-22。路径均相对当前 ruoyi-vue-pro根目录，换版本后按类名与方法重定位。官方正文未在本轮重新核验，本页来自实际源码与测试阅读。

## 精确入口

下表 `I` 表示 `yudao-module-infra/src/main/java/cn/iocoder/yudao/module/infra/`；`T` 表示 `yudao-module-infra/src/test/java/cn/iocoder/yudao/module/infra/`。

| 路径与符号 | 用途 |
| --- | --- |
| `I/controller/admin/codegen/CodegenController.java:95`、`:111`、`:138`、`:147` | 导入定义、从数据库同步、预览、ZIP下载；具体方法为 createCodegenList、syncCodegenFromDB、previewCodegen、downloadCodegen，实际请求有权限校验。行号漂移时按方法定位。 |
| `I/service/codegen/CodegenServiceImpl.java:131`、`:157`、`:261` | updateCodegen 校验主子关联；syncCodegenFromDB 同步字段；generationCodes载入主子表并按数据源选方言。 |
| `I/enums/codegen/CodegenTemplateTypeEnum.java:16` | ONE=1、TREE=2、MASTER_NORMAL=10、MASTER_ERP=11、MASTER_INNER=12、SUB=15。 |
| `I/enums/codegen/CodegenFrontTypeEnum.java:13` | Vue2 Element UI、Vue3 Element Plus、Vben2/5多套UI、Admin UniApp WOT；不能仅按“Vue3”选模板。 |
| `I/service/codegen/inner/CodegenEngine.java:72`、`:111`、`:387` | 后端/前端模板映射与 execute；模板文件在 `yudao-module-infra/src/main/resources/codegen/`。 |
| `I/framework/codegen/config/CodegenProperties.java:14` | `yudao.codegen`基础包、前端默认类型、VO类型与生成选项。 |
| `yudao-server/src/main/resources/application.yaml:306` | 基线配置中 unit-test-enable、import-enable为 false，不能假设所有下载包都含测试或导入功能。 |
| `T/service/codegen/CodegenServiceImplTest.java:160`、`:177`、`:233`、`:448`、`:482` | 主子表无效关联、数据库同步、单表与主表生成测试。 |
| `T/service/codegen/inner/CodegenEngineUniappTest.java:29`、`:68`、`:82`、`:108` | 移动端单表、树表、生成语义、字符串主键回归；同目录还有Vue2/Vue3/Vben变体测试。 |
| `T/service/codegen/inner/CodegenEngineAbstractTest.java:93` | 默认比对完整文件集合和内容；`codegen.regenerate=true`会写回断言资源，不能作为普通验证开关。 |

## 使用生成器建立功能

1. 新模块先检查同层 POM、包结构和跨模块 API。按当前架构创建模块、注册 reactor和服务依赖；复用现有模块时只添加本次业务。装配详见启动技能，不复制其它模块全部配置。
2. 明确表关系、主键类型、唯一性、租户/审计/逻辑删除字段和目标方言。对现有表先读取结构，不靠截图重新建表。
3. 在生成器中导入表定义，配置业务包名、类名、字段Java类型、查询条件、字典和页面显示项。表模型与前端类型分别设置。
4. 主子表明确主表模式、子表对应的 masterTableId和subJoinColumnId，再核对一对一/一对多与编辑行为。树表核对父ID与名称字段，移动端核对目标工程所用组件库。
5. 预览或下载到待审区域，检查 Controller/VO/Service/DO/Mapper、前端API与页面、SQL与错误码。按文件合并，保留已有业务分支。
6. 生成菜单与按钮后，验证权限码、角色授权、接口 `@PreAuthorize`、登录菜单及前端入口。应用SQL前核对目标库与已有ID；源代码生成不自动授权修改业务数据库。

## 同步字段与维护模板

- `syncCodegen0`会对类型、可空、主键、注释或序号变化的字段删除旧元数据再重建；先保存现有字段配置，核对同步后字典/控件/查询条件，不能当作无损刷新。
- 模板变更先确定受影响的前端与表模型矩阵，只运行相关变体测试。共享Java/SQL模板修改则扩展到它实际覆盖的变体。
- `CodegenEngineAbstractTest`使用已保存的生成结果检查文件集合和内容。只有预期行为已审清时才重建对应断言，然后检查差异并恢复普通断言运行。
- 移动端不止检查字符串渲染：还需检查生成路径、路由登记、主子字段重名、字符串主键与API路径。真实前端构建依赖完整前端工程。

## 验收

新增业务至少覆盖成功创建/修改/查询及无权限或非法输入；主子表补关联与一致性，树表补父子边界；前端检查页面路径、API调用和权限显示。生成器维护需相关 `CodegenServiceImplTest`、`CodegenEngine*Test`结果及生成差异。上述是待执行标准，不代表本插件已跑过这些项目测试。
