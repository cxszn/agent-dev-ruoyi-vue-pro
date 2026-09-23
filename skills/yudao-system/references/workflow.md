# 脚本使用与数据配置

## 连接与查询

先从任务和项目配置确定完整管理端 API 地址（包含实际管理端前缀）。使用现有正常认证流程取得访问令牌，将原始令牌放入当前进程的 `YUDAO_TOKEN`，不包含 `Bearer ` 前缀；不要把令牌写入命令、JSON 配置、对话或日志。脚本不保存凭证、不接收 `--token/--password`，也不提供绕过验证码的自动登录。

环境变量：

| 变量 | 含义 |
|---|---|
| `YUDAO_API_BASE` | 任务指定的管理端 API 基址；也可用 `--api-base` |
| `YUDAO_TOKEN` | 当前任务的原始访问令牌；可用交互终端的 `--prompt-token` 替代 |
| `YUDAO_TENANT_ID` | 当前租户 ID；也可用 `--tenant-id`，不会默认猜测 `1` |
| `YUDAO_VISIT_TENANT_ID` | 仅在任务明确使用代访租户时提供；也可用 `--visit-tenant-id` |

使用 HTTPS 或任务指定的受控本地开发地址。只有核实该环境关闭多租户后，才选择 `--without-tenant`；此参数仅省略请求头，不修改服务端配置。正常情况下每次查询和创建均保留 `tenant-id`，代访时同时保留 `visit-tenant-id`。

以下命令从插件根目录执行；连接参数由环境提供：

```sh
python -X utf8 skills/yudao-system/scripts/system_creator.py --action query-roles
python -X utf8 skills/yudao-system/scripts/system_creator.py --action query-users --keyword 张
python -X utf8 skills/yudao-system/scripts/system_creator.py --action query-depts
python -X utf8 skills/yudao-system/scripts/system_creator.py --action query-posts
python -X utf8 skills/yudao-system/scripts/system_creator.py --action query-dicts --keyword 状态
python -X utf8 skills/yudao-system/scripts/system_creator.py --action query-dict-data --type order_status
python -X utf8 skills/yudao-system/scripts/system_creator.py --action query-menus --keyword 订单
python -X utf8 skills/yudao-system/scripts/system_creator.py --action query-tenants
```

`--keyword` 在完整查询结果上匹配名称/编码；用户匹配 `username/nickname`。当前核对版本的 `UserPageReqVO` 不接受 `nickname` 查询字段，因此不能照搬来源的参数。字典项使用 `/system/dict-data/page?dictType=...` 查询启用和禁用记录；`simple-list` 只返回启用数据，不用于判定不存在。

所有分页从 `pageNo=1` 开始，持续读取直到条数等于 `total`。总数变化、重复 ID、提前空页或结构异常使查询失败。结果不是事务快照；执行期间外部并发写入仍可能触发唯一性冲突，此时停止并重查。

CLI 只输出识别主数据所需字段，不输出用户联系方式或原始响应错误正文。`--output new-result.json` 可另存结果；文件必须不存在，避免覆盖。库的 `query()` 返回原始业务记录，调用者需要自行按任务裁剪。

## 先查后建

JSON 配置支持 `roles`、`dicts`、`menus`，及只读引用 `users`、`depts`、`posts`。所有创建记录显式指定 `status`（`0` 启用、`1` 禁用）；未指定 `sort` 时新记录使用 `0`。示例用于说明结构，需替换为实际获授权数据：

```json
{
  "roles": [
    {"name": "订单审核", "code": "order_review", "status": 1}
  ],
  "dicts": [
    {
      "type": "order_status",
      "name": "订单状态",
      "status": 0,
      "items": [
        {"value": "pending", "label": "待处理", "status": 0, "sort": 1},
        {"value": "done", "label": "已处理", "status": 0, "sort": 2}
      ]
    }
  ],
  "users": [{"keyword": "operator"}],
  "depts": [{"keyword": "运营部"}],
  "posts": [{"keyword": "order_operator"}]
}
```

```sh
python -X utf8 skills/yudao-system/scripts/system_creator.py --config master-data.json
python -X utf8 skills/yudao-system/scripts/system_creator.py --config master-data.json --apply
```

第一条仅查询并返回计划，第二条在本次任务已授权后重新查询再创建。`--apply` 是执行开关，不能替代用户授权。已经明确授权具体创建任务时，可以直接用第二条；无需另加统一确认轮次。

工具先校验整份配置，再完成所有必要查询和冲突检查，最后才写入。已有记录按精确身份复用，提供的字段与现有值不一致时报错，不悄悄更新或改用同名其他编码。用户、部门、岗位的只读引用须精确匹配唯一记录；零个或多个匹配阻断本批创建。

角色创建仅发送 `RoleSaveReqVO` 支持字段。核对版本的服务层自动设置 `type=CUSTOM`、`dataScope=ALL`，计划通过 `serverDefaults` 显示；本工具不会自行分配数据权限、用户或菜单。若需要限定数据范围，先将该事项纳入具体授权与实施方案，完成后再绑定用户。

字典类型可以为空字典；已有类型也会检查配置中列出的字典项，只补缺失项。停用类型只能复用已有项，不能新增项；服务端会拒绝向停用类型添加字典项，工具在预查阶段阻断。既有值对应另一个标签、状态不同或标签已用于其他值时停止。字典项 `value` 必须是字符串，避免数值/字符串标识转换。

## 菜单

菜单配置示例（`parentId` 必须改为查询确认的真实父节点 ID；根目录可用 `0`）：

```json
{
  "menus": [
    {
      "name": "订单管理", "parentId": 120, "type": 2, "status": 0,
      "path": "order", "component": "order/index", "componentName": "OrderIndex",
      "visible": true, "keepAlive": true, "alwaysShow": false
    }
  ]
}
```

目录 `type=1` 需要 `path`；页面 `type=2` 需要 `path/component/componentName`；按钮 `type=3` 需要 `permission`，不带组件、图标或路径。新菜单默认 `visible=true`、`keepAlive=false`、`alwaysShow=false`，实际发送字段均出现在计划里。父节点必须已经存在且为目录或页面，不能在同一个批次猜测新父节点的 ID。先创建目录并重查，再创建页面和按钮。

创建菜单不附带角色授权。菜单权限字符串应与当前前后端对应实现一致，按钮集合按功能选取，不固定生成六条记录。菜单关系与授权验收见 [API 与菜单关系](api-reference.md)。

## Python 调用与失败恢复

从本技能实际路径导入 `scripts/system_utils.py`；库入口是 `SystemClient` 和 `process_config`，不是来源的全局初始化接口。令牌仍从进程环境获取：

```python
import os
from system_utils import SystemClient, process_config

client = SystemClient(
    os.environ["YUDAO_API_BASE"], os.environ["YUDAO_TOKEN"],
    tenant_id=os.environ["YUDAO_TENANT_ID"],
    visit_tenant_id=os.environ.get("YUDAO_VISIT_TENANT_ID"),
)
roles = client.query("roles", keyword="订单")
plan = process_config(client, {"roles": [{"name": "订单审核", "code": "order_review", "status": 1}]})
```

任何查询错误抛出 `SystemAPIError`；输入冲突抛出 `DataConflict`；均不能转换成空列表后继续。批次写入没有跨请求事务，失败抛出 `ApplyError`，包含 `completed` 与 `failed_operation`。CLI 返回非零退出码，并把已完成操作和结果不确定的操作输出到标准错误；服务端已落库但响应丢失时同样视为结果不确定。重新查询并复用已创建 ID 后再补齐，不能盲目重复 POST。

预查、模拟测试和创建接口成功均不代表运行环境验收。任务完成报告须区分实际运行的 API、返回的记录 ID、未执行的角色授权和未验证的前端结果。
