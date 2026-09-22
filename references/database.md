# 数据库改动与升级

## 先确定基线

已核验源码基线的 `sql/mysql/ruoyi-vue-pro.sql` 是 MySQL 初始化脚本，`sql/postgresql`、`sql/oracle`、`sql/sqlserver`、`sql/dm` 等有各自文件。目标环境的数据库类型、已有 schema、数据与版本必须另核；不能把基线文件当成当前线上状态。`sql/tools/convertor.py` 是转换工具，转换结果仍需按目标方言校验。

SQL 文件格式转换使用[专用技能](../skills/yudao-sql-convert/SKILL.md)：执行项目中的转换器，保留新输出与 `.sql.report.json`，核对源表/数据语句、解析错误和序列。七种目标的实际支持范围见[方言说明](../skills/yudao-sql-convert/references/dialects.md)。文件生成完成后，目标数据库导入和业务验收是独立步骤。

## 可审查的增量流程

1. 对目标库和目标版本生成结构/数据差异，按模块收缩范围，标出新增、修改、删除与索引变化。
2. 评估历史数据、默认值、空值、回填、外键及回滚。全局配置中的 `system_dict_type`、`system_dict_data`、`system_menu`、邮件/短信/站内信模板需单独审数据差异。
3. 对应更新 DO、Mapper、接口 VO、权限与租户规则；菜单权限还要核 `system_role_menu` 关联。
4. 保存评审后的 SQL 与执行顺序，在受控环境验证数据保留和关键查询。生产执行取决于当前任务授权。

[官方表结构变更文档](https://doc.iocoder.cn/sql-update/)建议在结构/数据同步工具中先预览 SQL，二次检查后选择性执行；它不构成直接运行同步工具的授权。非 MySQL 脚本可能滞后，[后端启动文档](https://doc.iocoder.cn/quick-start/)也提示这一点。
