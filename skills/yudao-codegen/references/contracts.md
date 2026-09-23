# 字段、API 与产物契约

用于需求建模、人工补全生成结果与增量字段变更。以下源码位置相对目标后端根；核验基线及导入差异见[来源说明](import-provenance.md)。已有项目实现与本次业务约束优先于候选映射。

## 结构与命名

- Boot 基线的代码位于 `yudao-module-{moduleName}/src/main/java/{basePackagePath}/module/{moduleName}/`。Cloud 项目是否拆 `*-api`/`*-server` 由 POM 和实际包布局确认；`CodegenEngine.getTemplates` 会在 Boot 模式移除这层输出目录。
- DO、Mapper、Service 与 Controller 以业务包隔离；VO 位于 `controller/{admin|app}/{businessName}/vo/`，不是统一 `controller/admin/vo/{Entity}`。
- `moduleName`、`businessName`、`className` 分别控制模块、包/页面目录与实体类。`CodegenEngine.initBindingMap` 从去模块前缀后的类名生成 `simpleClassName_strikeCase`：当前接口路径及权限前缀使用它，可能与 `businessName` 不同。例如包目录 `dictdata` 对应路由 `dict-data`。核对最终 Controller、前端 API、菜单 SQL 三者一致，不能只拼表名。
- `scene` 是管理后台/用户 App；`frontType` 是 UI 模板。管理端 UniApp 仍可使用 ADMIN 场景。用户 App 场景的权限、当前用户范围和响应脱敏须按业务补齐，不能把生成结果直接当成完整授权模型。

## 字段映射：给出候选，再核对契约

| 业务含义 | 候选类型与控件 | 核对重点 |
| --- | --- | --- |
| 名称、标题、编码 | varchar / String / 输入框 | 长度、唯一性；编码是否保留前导零，不能改为数字。 |
| 金额、价格 | decimal / BigDecimal / 数值输入 | 精度、单位、舍入；已有项目可能使用整数分。API 数字/字符串表示沿用真实序列化。 |
| 数量、排序 | int 或 bigint / Integer 或 Long / 数值输入 | 范围、负数、是否可小数；引用 ID 应使用实际选择组件。 |
| 状态、类别 | 整数或字符串 / 同类型字典选择 | 实际字典值与默认状态；不能把所有“状态”配成同一字典。 |
| 开关、是否 | boolean 或数值枚举 / 相同契约的单选或开关 | tinyint(1) 不足以证明 API 为 Boolean；开启值可能为 0。 |
| 日期、生日 | date / 项目实际日期类型 / 日期控件 | 仅日期与时间戳分开；不要固定生日为 LocalDateTime。 |
| 时间、时间范围 | datetime 等 / LocalDateTime 等 / 日期时间控件 | 时区、序列化、范围边界；PageReqVO 与 Mapper 条件一致。 |
| 备注、描述 | varchar/text / String / 多行输入 | 最大长度；富文本仅在业务需要且项目有相应处理时使用。 |
| 图片、附件 | URL、文件 ID 或集合 / 项目对应上传组件 | 单值/多值、上传响应、存储形式；不能因字段名含 image 就改变数据模型。 |
| 用户、部门等关联 | 目标主键类型 / 已有选择组件 | 选项接口、数据范围及展示名称；先查询复用，勿自动创建依赖。 |

已有表按 DDL、MyBatis 类型处理器与实际元数据决定 Java 类型；`float/double` 不一律改 BigDecimal，`date` 不一律改 LocalDateTime。生成器 `CodegenBuilder.processColumnUI` 当前按字段后缀给出默认值：status/sex 为 radio、type 为 select、image/file 为上传、content/description 为 editor，Boolean 为 radio、LocalDateTime 为 datetime。它们是默认推导，可按业务与目标组件能力修正。

字典优先级：用户指定的真实类型 → 已有字段/同类功能使用的类型 → 查询得到的候选类型及值。核对启用状态、值类型、标签与业务意义；语义匹配有歧义时列候选，未匹配时保留合适的普通控件或待决项。系统查询入口见 [yudao-system](../../yudao-system/SKILL.md)，不固定导入来源脚本的旧函数签名。

## Java 层检查

| 层 | 生成后需要成立的契约 |
| --- | --- |
| DO | 对应实际表/列与主键；复用 BaseDO 的审计/删除字段，租户隔离按框架配置和同类实体确认。当前模板输出 BaseDO，并排除 tenantId，不能据此宣称表没有租户隔离，也不能统一改成 TenantBaseDO。 |
| 主键 | 当前 `codegen/java/dal/do.vm` 为主键输出 `@TableId`，字符串主键使用 `IdType.INPUT`；MySQL 自增由 DDL 和实际 ID 策略决定。`@KeySequence` 面向序列数据库，不代替 MySQL 自增或主键映射。 |
| Mapper | 复用 `BaseMapperX`、`LambdaQueryWrapperX`，查询条件与 PageReqVO 一致；自定义 XML 与表别名按实际 SQL 核对。 |
| Service | 复用项目的 BeanUtils/转换器；修改和删除处理不存在记录，联合保存有正确事务与父子关联。批量删除是否需业务校验由关联约束决定，不能套用“批量操作无需校验”。 |
| Controller | 参数与返回使用真实主键类型；管理端动作带相应权限，分页返回 PageResult。`BeanUtils.toBean` 只是当前模板选择，已有 MapStruct 逻辑按需保留。 |
| VO | create/update 的必填与 ID 规则分别成立，分页参数和返回数据各有用途；`@Schema(requiredMode=...)` 不替代运行时校验。选择 VO/DO 模式后按实际产物审查。 |

审计字段通常由框架填充，不应在创建/修改表单中任意开放。新表是否加入 `tenant_id` 取决于隔离需求及租户配置；现有表只能按实际字段处理。错误码加入目标模块已有编号段并查重，不照抄示例常量值。

## API 与 Web 页面

下面是当前生成模板契约索引，不能作为未知服务可直接调用的地址清单；运行前应核对已部署 Controller、环境和 API 前缀。

| 动作 | HTTP 与相对路径 | 请求与结果 | 管理端动作权限 |
| --- | --- | --- | --- |
| 新建 | POST `/{moduleName}/{routeName}/create` | JSON 创建数据 → 实际主键类型 | create |
| 修改 | PUT `.../update` | JSON 更新数据 → Boolean | update |
| 删除 | DELETE `.../delete` | query `id` → Boolean | delete |
| 批量删除 | DELETE `.../delete-list` | query `ids` → Boolean；受 delete-batch-enable 与表模式控制 | delete |
| 详情 | GET `.../get` | query `id` → 响应数据 | query |
| 分页 | GET `.../page` | PageReqVO 查询参数 → `{list,total}`，由 CommonResult 包装 | query |
| 树列表 | GET `.../list` | 树查询参数 → 列表；不套分页 | query |
| 导出/导入 | `.../export-excel`、`.../import` 等 | 按实际生成开关与 Controller 核对文件协议 | export / import |

`routeName` 指上面的 `simpleClassName_strikeCase`。客户端是否已经解包 CommonResult、是否自动附加 `/admin-api`、Token 与租户头，从当前请求封装读取，避免重复前缀与 `data.data`。

Vue3 Element Plus 模板使用 `import request from '@/config/axios'`，GET 使用 `params`、POST/PUT 使用 `data`，详情/删除模板含 query ID。当前模板导出 `XxxApi` 对象；导入来源的独立函数导出不是所有版本的统一形式。Vben 分支分别读取其实际模板，不能把 Element Plus 组件与请求 API 混用。

页面与表单至少对齐：搜索重置回第一页、分页 `{list,total}`、字典值类型、编辑回填、校验/提交状态、成功后列表刷新、取消删除不报成功、按钮权限与后端相同。复用已有 Dialog、Pagination、字典和上传组件；是否全局组件或自动导入，以 Vite 配置/声明文件为证，不能从来源示例推断。

新增页面通常落在 `src/views/{moduleName}/{businessName}/`，API 在 `src/api/{moduleName}/{businessName}/`。实际文件集合由模板、主子表、VO 类型及导入/测试开关决定，不承诺固定 12 个文件。

## 关键源码入口

- `yudao-module-infra/src/main/java/cn/iocoder/yudao/module/infra/service/codegen/inner/CodegenEngine.java`：`initBindingMap`（526 行）、`getTemplates`（633 行）、Java/前端文件路径方法（694 行起）。
- `yudao-module-infra/src/main/java/cn/iocoder/yudao/module/infra/service/codegen/inner/CodegenBuilder.java`：`processColumnOperation`、`processColumnUI`。
- `yudao-module-infra/src/main/resources/codegen/java/`：`dal/do.vm`、`dal/mapper.vm`、`controller/controller.vm`、`controller/vo/saveReqVO.vm`、`service/serviceImpl.vm`。
- `yudao-module-infra/src/main/resources/codegen/vue3/api/api.ts.vm`；其它前端分支按 `CodegenEngine.FRONT_TEMPLATES` 定位。
