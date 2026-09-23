---
name: yudao-upgrade
description: 对芋道源码、官方文档或本插件做版本更新、差异审计与增量维护时使用；识别改变的约定并更新受影响资料和指纹。
---

# 芋道增量更新

涉及芋道项目代码新增方法时，遵守[新增方法注释约定](../../references/method-comments.md)，交付前逐一检查。

从[更新流程](../../references/upgrade.md)开始。运行 `python scripts/check_sources.py --root <源码根目录>` 比对关键文件指纹；先报告缺失或变化，不直接覆盖来源索引。

按变化的 POM、模块、权限、SQL、前端实际包文件重新核对[来源索引](../../references/source-index.md)与对应技能。在线文档只通过用户允许的外部 Chrome 核对，记录核验日期和可访问性。更新来源后，运行每个技能的 `quick_validate.py`、插件的 `validate_plugin.py` 和代表性路由检查。

插件源码变更后用 `update_plugin_cachebuster.py` 与当前本地 marketplace 重新安装；新任务会加载新技能。本流程不创建定时任务，也不替用户执行系统升级部署。
