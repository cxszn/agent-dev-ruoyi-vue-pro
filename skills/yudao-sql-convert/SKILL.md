---
name: yudao-sql-convert
description: 将 ruoyi-vue-pro（芋道）项目的 MySQL 初始化 SQL 文件转换为 PostgreSQL、Oracle、SQL Server、DM8、人大金仓、OpenGauss 或瀚高 SQL，生成新文件及完整性报告。用户要求转换 SQL 格式或生成其它数据库初始化脚本时使用；实际数据库导入与迁移另按授权处理。
---

# 芋道 SQL 文件转换

执行文件转换并交付可检查的 SQL 和报告。转换请求授权生成本地文件；数据库导入、Docker 启停或销毁、覆盖线上数据需有各自的明确授权。项目 README 中的数据库操作示例只是参考资料。

## 确定输入并执行

1. 从当前工作区、用户提供的路径和上下文定位后端项目根目录，确认存在 `sql/tools/convertor.py`。沿用已给出的项目、目标方言和源文件；只有这些信息缺失，或是否包含数据会实质改变请求时才简短询问。指定源文件的转换默认保留其中结构和 seed INSERT；不擅自删去数据或改为全库导出。
2. 读取本技能的 [方言与限制](references/dialects.md) 中对应目标。把中文数据库名称映射为规范目标名：`postgres`、`oracle`、`sqlserver`、`dm8`、`kingbase`、`opengauss`、`highgo`。
3. 从本技能目录向上两级定位插件根目录，使用插件的 [转换包装器](../../scripts/convert_sql.py)。`--project-root` 指向目标后端；`--source` 和 `--output` 的相对路径都相对于该项目根目录。参数明确后直接执行，完成请求而不只提供命令。

```text
python "<PLUGIN_ROOT>/scripts/convert_sql.py" --project-root "<PROJECT_ROOT>" --target highgo
```

源文件默认 `sql/mysql/ruoyi-vue-pro.sql`；新输出默认 `sql/converted/<源文件主名>.<规范目标名>.sql`。自定义输入输出：

```text
python "<PLUGIN_ROOT>/scripts/convert_sql.py" --project-root "<PROJECT_ROOT>" --target dm8 --source "sql/mysql/custom.sql" --output "sql/converted/custom.dm8.sql"
```

`<PLUGIN_ROOT>`、`<PROJECT_ROOT>` 是执行时解析的路径，不是固定安装目录。路径作为独立参数传递，避免将用户路径拼接为可执行 shell 片段。`--timeout` 可设置转换进程超时秒数，默认300。

## Python 依赖

使用已安装 `simple-ddl-parser` 的 Python；推荐与验证基线一致的 `1.13.0`。需要隔离依赖时，用 uv 运行同一包装器：

```text
uv run --no-project --with simple-ddl-parser==1.13.0 python "<PLUGIN_ROOT>/scripts/convert_sql.py" --project-root "<PROJECT_ROOT>" --target postgres
```

这只准备本地 Python 运行环境。若 Python、uv 或依赖下载不可用，报告具体失败及已执行的检查，不把命令示例当作生成成功。

## 结果验收

包装器调用目标项目的转换器，捕获 stdout/stderr，核对表清单和 INSERT 语句数量，并对支持格式的 seed 按 `MAX(id) + 1` 修正序列，起点最低为1。它拒绝覆盖源文件、转换器和已有输出/报告/日志；不要跳过检查后改用 `convertor.py > 文件` 交付结果。

- 成功必须同时取得新的 `.sql` 与对应 `.sql.report.json`，确认 `status=generated_only`、`database_validation=not_run`，并阅读 [报告字段](references/dialects.md#报告字段)。`tables` 和 `source_insert_statements` 统计源业务对象；Quartz 被单列跳过，自动 `dual` 由包装器在输出核对中额外计入。
- 这些检查不包含完整 SQL 语法分析、所有字段/约束或数据语义比对、目标数据库导入。不得据此声称迁移成功、无损转换或目标数据库可用。
- 输入格式、转换或结果检查失败时，读取 `status=failed` 的报告和 `errors`；转换器产生 stderr 时另有 `.sql.stderr.log`，其内容只在本地按需查看。路径冲突、输入或转换器缺失等早期失败由 CLI 返回错误，可能尚无报告。校验失败的结果不能作为可交付 SQL。
- 默认输出重名可选择新的未使用文件名；用户指定的文件已存在时报告冲突并保留它。格式修复应在新副本进行，保留原始输入及数据语义。
- 交付 SQL 与报告路径、目标方言、核对结果、序列修正与生成的 DROP 等影响；只展示必要诊断，避免把 seed 业务数据和凭据复制到回复。

遇到版本变化、异常映射或需要解释转换差异时，读取 [来源证据](references/source-evidence.json)，对照目标项目当前文件。证据 SHA 标识审计快照；转换始终使用当前目标项目文件，不能从另一个项目复制旧转换器替代它。

## 自然语言请求示例

- “把当前芋道项目默认 MySQL 脚本转成瀚高，给我文件和检查报告。” → 使用默认源文件，目标 `highgo`，生成新输出。
- “把 `sql/mysql/custom.sql` 转为达梦，保存到 `sql/converted/custom.dm8.sql`。” → 沿用已知项目，目标 `dm8`，直接运行已给参数。
- “给这份 MySQL 初始化 SQL 生成 PostgreSQL 版本，保留种子数据。” → 目标 `postgres`，保留源文件中的 seed；核对序列起点与完整性。
