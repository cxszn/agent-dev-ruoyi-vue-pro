# 来源变更与插件维护

## 检测

运行 `python scripts/check_sources.py --root "<当前项目根目录>"`，必须显式指定待核验项目。脚本比较 `references/source-manifest.json` 的关键文件、各源码模块目录与 SQL 目录的 SHA-256 聚合指纹、POM 版本和启用模块；只读，返回 0 表示基线匹配，1 表示变化或缺失。构建产物目录会跳过。项目包含 Git 元数据时，另记录当前提交和实际 diff。

## 判断影响

| 变化 | 复核范围 |
| --- | --- |
| 根/BOM/server POM | Java、Spring Boot、插件/依赖、实际启用模块、构建/测试命令；留意根 POM 4.1.0 与 BOM 4.1.1 的现有差异。 |
| Controller/权限 Service | API 前缀、VO、权限字符串、角色菜单、租户与相关测试。 |
| SQL | 方言、表/索引/数据、DO/Mapper、增量迁移与回滚。 |
| 前端仓库 | 新增 `package.json` 后才记录具体版本、路由/API/构建命令并做浏览器验收。 |
| 官网文档 | 经外部 Chrome 核 URL/标题/正文与访问权限；按主题修改引用和规则，不批量复制全文。 |

## 更新与验证

仅改受影响的资料、技能与指纹清单，记录核验日期和适用版本；保留旧来源的差异说明直到完成针对性复核。官网目录变更写入 `references/docs-index.json`，以分组/标题和已知 URL 定位对应记录，分别更新链接来源和正文状态；未访问的正文保持 `not-read`。随后运行 `python scripts/docs_index.py check --source-root "<项目根目录>"` 与 `python scripts/docs_index.py render`，更新 [docs-index.md](docs-index.md)。

运行 `skill-creator/scripts/quick_validate.py` 检查每个技能，`plugin-creator/scripts/validate_plugin.py` 检查插件，再核内部链接、来源相对路径和代表任务的路由。对多租户移除至少推演“多个租户存在同名账号”和“lambda 内 return 后还有外围业务”的行为；模拟结果不能代替实际迁移或编译验证。

插件已经安装到 Codex 后，使用 `plugin-creator/scripts/update_plugin_cachebuster.py <插件路径>` 更新本地缓存标识，再用个人 marketplace 名称执行 `codex plugin add dev-ruoyi-vue-pro@personal`。验证 `codex plugin list` 的安装状态；新任务加载更新后的技能。不要手改插件缓存或建立定时任务。

维护前通过 `codex plugin list --marketplace personal --json` 确认插件源码位置，再修改源码并重新安装。`agent-templates/` 改动后需同步到实际使用的个人或项目 Agent 配置目录，并核验名称唯一性。

外部技能包的更新先比较 `references/imports/` 中的来源指纹和随附使用声明，再按技能职责合并同名内容；保留当前项目已核验的约定。API、凭据、权限写入、生成结果覆盖和再分发范围有差异时，明确处理差异后再安装或发布。本机导入不自动扩大对外分享授权。
