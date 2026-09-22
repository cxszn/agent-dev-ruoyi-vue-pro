# 目标方言与来源限制

以下是审计基线 `sql/tools/convertor.py` 的实际行为，路径相对于目标后端项目。快照与行号见 [source-evidence.json](source-evidence.json)。包装器的检查和序列修正不会自动补全所有方言语义；成功状态仍为 `generated_only`。

## 七种目标

| 规范目标 | 用户常用名称 | 来源转换器的类型与结构行为 | 生成的控制语句 |
| --- | --- | --- | --- |
| `postgres` | PostgreSQL、Postgres、PG | int→int4、bigint→int8、tinyint/smallint→int2、bit→bool、datetime→timestamp、json→jsonb、blob→bytea、decimal→numeric；`deleted` 强制 int2/default 0/not null | 每表 DROP TABLE、DROP/CREATE SEQUENCE；额外重建并插入 dual；seed 使用 BEGIN/COMMIT |
| `oracle` | Oracle、甲骨文 | varchar→varchar2，长度上限4000；int/bigint→number、datetime→date、bit→number(1,0)、text→clob；varchar/text/longtext 强制可空；转义 level、size 列 | CREATE TABLE/SEQUENCE；seed 后 COMMIT；来源不生成 DROP 或 dual |
| `sqlserver` | SQL Server、MSSQL、微软 SQL Server | varchar→nvarchar，长度上限4000；datetime/timestamp→datetime2、bit→varchar(1)、tinyint/smallint→tinyint、text→nvarchar(max)、blob→varbinary(max)；id 强制 bigint IDENTITY；deleted 强制 bit | 每表及 dual 的 DROP/CREATE；GO 分批；seed 使用事务和 IDENTITY_INSERT ON/OFF |
| `dm8` | DM8、达梦、达梦8 | varchar→varchar(n char)；int/bigint保持，tinyint/smallint→smallint；id 强制 bigint IDENTITY；空串默认值的 NOT NULL 被放宽 | CREATE TABLE；seed 使用 IDENTITY_INSERT ON/OFF、COMMIT；来源不生成 DROP、dual 或 sequence |
| `kingbase` | KingbaseES、人大金仓、金仓 | 继承 PostgreSQL 类型映射；text 强制可空，空串默认值的 NOT NULL 被放宽；转义 level 列 | 继承 PostgreSQL 的 DROP、dual、事务与 sequence 行为 |
| `opengauss` | OpenGauss、openGauss、华为高斯 | 继承 Kingbase 的建表行为，但清空保留字列名转义集合 | 继承 PostgreSQL 的 DROP、dual、事务与 sequence 行为 |
| `highgo` | HighGo、瀚高 | 继承 PostgreSQL 转换实现，仅更改目标数据库名称 | 同 PostgreSQL |

常用名称用于识别用户意图，调用时优先使用规范目标。源 CLI 本身只接受规范目标名。上表描述源码行为，不是数据库厂商的兼容性承诺；尤其 Oracle 字符长度、SQL Server smallint 收窄、unsigned 范围、时间精度、JSON 和二进制字面量都需要目标数据库验证。

## 所有目标共同的约定

- 转换对象是 MySQL 初始化 SQL，不是增量迁移。源数据中的 `qrtz` 开头表及其 INSERT 被跳过，Quartz 要使用目标库自身的脚本。PG 系列和 SQL Server 额外生成 `dual`；核对数量时单独列出这些差异。
- 表名、列名转小写；仅部分目标/列名有显式转义，不能保证任意保留字、schema 限定名和大小写标识符可用。
- 主键按名为 `id` 的列重建，原主键定义不是生成依据。其他主键、复合主键或无 id 的表超出这套模型；SQL Server/DM8 还把 id 改为 IDENTITY。
- 普通索引重命名为 `idx_<table>_<编号>`，唯一索引重命名为 `uk_<table>_<编号>`。保留 DESC，省略 ASC；前缀长度被去除，可能扩大唯一约束。索引列不复用 CREATE 的保留字转义。
- 默认值主要直接拼接，AUTO_INCREMENT 与 ON UPDATE 等 MySQL 行为不能视为完整保留。外键、CHECK、独立 ALTER TABLE、视图、触发器、过程、函数和事件没有对应生成分支，包装器应拒绝这些输入。
- 原转换器先打印 preamble/dual，再逐表处理。解析为空只写 stderr 并跳过，可能 exit 0；表完全不被正则发现时甚至没有 stderr。包装器必须独立核对输入与输出。

## INSERT、字符串与序列

源转换器只识别行首精确的 `INSERT INTO`、反引号表名和精确 ` VALUES `。小写、缩进、无反引号表名会遗漏；跨行 VALUES 会截断；同行多条 INSERT 会破坏后续语句。唯一的折行兼容是精确 `)\nVALUES `。包装器拒绝非支持格式，不以“INSERT 数相等”代替完整性检查。

包装器把输入范围收窄为单行、单元组的简单 seed，拒绝多行或双引号字符串、函数调用和 `ON DUPLICATE KEY UPDATE` 等尾部；有 id 的表要求其值位于首列且是整数字面量。建表使用简单、无 schema 前缀的 ASCII 标识符，列名使用反引号，主键/唯一约束放在表级。这里的扫描只拦截已知不支持形式，并不构成完整字面量或 SQL 表达式语法验证。

来源会对整个文本运行 CHARACTER SET、COLLATE、ENGINE、索引前缀等清理，可能改变普通字符串。例如 `'x CHARACTER SET utf8mb4 y'` 变成 `'x y'`。列注释中的转义单引号可能截断，表注释也没有统一目标转义。遇到清理模式、复杂反斜杠转义或异常注释时，按包装器诊断处理，不能静默接受内容变化。

PG 系列对 INSERT 做 `\\`→`\`、`\'`→`''` 替换；Oracle 把所有形似 `YYYY-MM-DD HH:mm:ss` 的字符串改为 `to_date`，不按列类型区分；SQL Server 用文本替换加 `N`，且基线中首值为字符串会出现 `VALUES (N')...` 的错误。因此这些转换仍需结合列类型核查，源值相似不代表目标语义相同。

PG 系列和 Oracle 的原序列起点取“最后一条 INSERT 第一元组第一正整数 + 1”，与 MAX(id) 不同。包装器对支持的单行、id 首列、整数 id 输入计算 `MAX(id) + 1` 并修正生成序列，起点最低为1；列顺序或元组形式超出支持范围时拒绝。原脚本还为每表生成独立 sequence，没有自动给 id 添加 nextval 默认值，应用取号方式仍须核查。

未映射类型在 PostgreSQL/HighGo 中会抛错，而 Oracle/SQL Server/DM8/Kingbase/OpenGauss 可直接输出 `None`；无精度 timestamp 等形式也可能成为 `timestamp(None)`。包装器应将这些占位视为失败，不能交付为有效类型。

## 文件验收与数据库验收

本技能完成条件是新 SQL 与 `.sql.report.json` 均生成，并且报告中的业务表清单、源 INSERT 总数、序列修正和诊断已经核对。包装器进行对象清单/语句计数与若干已知风险检查，不执行完整 SQL 语法分析，也不逐字段证明数据、注释和约束语义等价。

### 报告字段

| 字段 | 实际含义 |
| --- | --- |
| `status`、`database_validation` | 成功为 `generated_only`，失败为 `failed`；数据库验证始终为 `not_run` |
| `target`、`source_name`、`output_file` | 规范目标名与输入/输出文件名；输出字段仅成功时写入 |
| `tables`、`source_insert_statements` | 去除 Quartz 后的源业务表名列表和 INSERT 语句总数；额外 dual 参与内部输出核对，不加入这两个源统计 |
| `quartz_tables_skipped` | 跳过的 qrtz 表名列表 |
| `source_session_or_drop_statements_ignored` | 不作为输出依据的源 DROP、SET、USE、BEGIN、COMMIT 语句数量 |
| `sequence_adjustments` | 已修正的 sequence，每项包含 `table`、`from`、`to` |
| `destructive_statements` | 生成 SQL 中 DROP TABLE / DROP SEQUENCE 的数量；不是全部数据库影响清单 |
| `source_sha256`、`converter_sha256`、`output_sha256` | 输入 SQL、实际项目转换器、生成 SQL 的哈希；输出哈希仅成功时存在 |
| `simple_ddl_parser_version`、`converter_exit_code` | 实际依赖版本和转换器退出码；到达对应阶段才写入 |
| `errors`、`warnings`、`diagnostic_file` | 失败原因、静态验证局限和转换器变化提示；stderr 非空时写入本地日志名 |

失败报告只包含失败前已取得的字段。输入/转换器缺失、输出路径冲突等发生在创建报告之前，CLI 会直接返回错误；不能假设每次失败都有报告。格式/转换/校验失败不发布最终 SQL，转换器 stderr 写入 `.sql.stderr.log` 后停止交付。子进程关闭解析库 INFO 及更低级别的构表日志；WARNING/ERROR 和直接写入 stderr 的解析诊断继续按失败处理。

生成文件中的 COMMIT、IDENTITY_INSERT、序列起点、约束和类型转换也会影响数据库；它们不包含在 `destructive_statements` 的 DROP 计数中。生成这些文本不等于执行它们。

实际导入需在用户授权的目标环境按其版本验证语法、主键/唯一索引、注释、Unicode/空串、日期/二进制值、行数和应用后续取号。此阶段还需确认 DROP 的对象与数据影响，不能因 README 展示 Docker 命令就启动、重建或销毁数据库。

## 已执行验证与复测

已在 `simple-ddl-parser==1.13.0` 下对七种目标执行实际转换：合成样例包含一张业务表、两条乱序 ID 数据和一张应跳过的 Quartz 表；项目默认源 SQL 包含 48 张业务表、5,588 条 INSERT。两组共 14 次生成与结构检查通过，源文件指纹见 [source-evidence.json](source-evidence.json)。这不包含目标数据库导入。

在插件根目录运行防回归测试：

```text
python -m unittest discover -s tests -p test_sql_conversion.py -v
```

使用新目录保存七方言合成样例的输出与报告：

```text
uv run --no-project --with simple-ddl-parser==1.13.0 python tests/verify_sql_targets.py --project-root "<PROJECT_ROOT>" --output-dir "<NEW_ARTIFACT_DIRECTORY>"
```

需要同时复测当前项目默认源文件时，加 `--with-project-source`。该选项会将源 SQL 的转换结果保存在指定目录，按业务数据的保管要求处理；验证脚本不连接数据库。

## 最小负向样本

以下是合成数据，可验证包装器会阻止静默误转换，不是待导入的业务脚本：

```sql
CREATE TABLE `t` (
  `id` bigint NOT NULL,
  `name` varchar(100),
  PRIMARY KEY (`id`)
);
INSERT INTO `t` VALUES (1, 'a'),
(2, 'b');
```

原转换器只保留第一条物理行；输入/输出的 INSERT 头数量仍各为1。将 INSERT 部分替换为下面一条，可验证危险字符串拦截：

```sql
INSERT INTO `t` VALUES (1, 'x CHARACTER SET utf8mb4 y');
```

若替换为下面两条，原 PG/Oracle 会从3开始取号；包装器应报告修正为21。生成结果仍需要目标数据库的运行验证。

```sql
INSERT INTO `t` VALUES (20, 'a');
INSERT INTO `t` VALUES (2, 'b');
```
