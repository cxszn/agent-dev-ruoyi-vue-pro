# UniApp 管理端接入与验收

用于 `frontType=60` 的 Admin UniApp WOT 页面。移动端是前端变体，可配合单表、树表、主子表；`scene=ADMIN` 与 `scene=APP` 决定后端场景，不能因手机页面自动切换为用户 App 权限模型。

本基线已核验生成模板与测试；本地 `yudao-ui/yudao-ui-admin-uniapp` 只有项目入口说明，未包含可运行的完整工程或 package.json。因此 Vue、Vite、TypeScript、WOT 的实际版本以及请求封装/路由插件必须从目标前端重新读取，来源固定版本不作为兼容承诺。

## 文件与接入点

当前 `CodegenEngine.FRONT_TEMPLATES` 为单表映射五类文件，相对移动端根目录：

| 文件 | 职责 |
| --- | --- |
| `src/api/{moduleName}/{businessName}/index.ts` | 数据类型、查询与写入 API。 |
| `src/pages-{moduleName}/{businessName}/index.vue` | 搜索、列表、分页与导航。 |
| `src/pages-{moduleName}/{businessName}/components/search-form.vue` | 独立搜索条件组件。 |
| `src/pages-{moduleName}/{businessName}/form/index.vue` | 新建/编辑、校验、保存。 |
| `src/pages-{moduleName}/{businessName}/detail/index.vue` | 详情及有权限的操作入口。 |

树表另有 breadcrumb 组件，主子/ERP 模式选择不同详情页及子表表单；检查实际生成文件集合。路径中的模块名与业务名来自配置，不能全部硬编码为 `pages-system`。按目标工程的 `pages.json`、分包或 `definePage` 插件登记入口，生成页面不保证自动出现在导航中。

## 模板契约与运行时核验

- 当前 API 模板使用 `import { http } from '@/http/http'`，分页类型来自 `@/http/types`；`http.get<T>(url, params)`、`http.post<T>(url, data)`、`http.put<T>(url, data)`、`http.delete<T>(url)` 与 Web Axios 封装形式不同。读取目标 `http` 定义核验其额外参数、响应解包、base URL 和认证，不从来源推断第三参数含义。
- API 路径使用 `/{moduleName}/{simpleClassName_strikeCase}`；单表分页、树表列表、主子列表和 ERP 子表操作必须分别对应 Controller。`businessName` 用于页面目录，可能与接口路由段不同。
- 当前模板根据主键 Java 类型生成 number 或 string。页面路由收到的 ID 先按目标路由约定处理，再保持实际业务主键类型；字符串 ID 不做无条件 `Number(id)`。大整数的 JSON 表示需按服务实际序列化和前端精度要求确定。
- 模板使用 WOT `wd-*` 组件、`useToast`、`useAccess().hasAccessByCodes`、`navigateBackPlus`、`definePage` 与字典 hooks；这些封装是否存在、如何导入，必须在目标工程核对。表单 `validate()` 返回 `{valid}` 是当前模板假定，WOT 版本变更时核实实际类型。
- 普通/内嵌主子表核对联合提交字段，ERP 模式核对子记录独立 API 和关联字段；一对一缺失记录、主子字段重名、子表主键类型必须保持后端约定。
- `-1` 如仅代表搜索“全部”，提交 API 前移除；它不是业务状态值。搜索重置页码和列表，连续触底不能并发请求同一页，失败重试不能漏页或重复追加；跟随目标工程已有分页方案。
- 保存或删除后返回列表/详情时检查刷新生命周期。页面仍驻留时仅 onMounted 可能不重取数据，按当前 onShow/事件方案实现；不能仅依赖“返回成功”提示验收。

## 验证范围

生成器层：相关 `CodegenEngineUniappTest` 断言文件集合和生成语义；覆盖字符串主键、树表与此次涉及的主子模式。保留现有 `CodegenEngineAbstractTest` 的普通断言行为，见 [workflow](workflow.md)。

真实工程层：按实际 package.json 运行类型检查/构建，再验证列表搜索与分页、详情、创建/编辑/删除、无权限按钮、路由与返回刷新；主子表加关联保存/删除，树表加父子边界。需要浏览器验证时遵守用户指定的浏览器工具。缺少前端工程或运行环境时准确报告验证止于模板，不声称移动端已运行。

源码入口（相对后端根）：

- `yudao-module-infra/src/main/java/cn/iocoder/yudao/module/infra/service/codegen/inner/CodegenEngine.java:148`：UniApp 文件映射。
- `yudao-module-infra/src/main/resources/codegen/vue3_admin_uniapp/api/api.ts.vm:1`：HTTP、类型与主子接口。
- `yudao-module-infra/src/main/resources/codegen/vue3_admin_uniapp/views/form/index.vue.vm:758`：详情加载与提交；`views/detail/index.vue.vm:109`：详情/删除；列表及树表模板位于同一目录。
- `yudao-module-infra/src/test/java/cn/iocoder/yudao/module/infra/service/codegen/inner/CodegenEngineUniappTest.java:29`：生成器回归入口。
