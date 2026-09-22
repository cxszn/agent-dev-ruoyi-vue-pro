---
name: yudao-frontend
description: 处理芋道管理后台 Vue3 Element Plus、Vben、Vue2、uni-app 的页面、菜单、API 调用和前后端联调时使用。先确认用户提供的具体前端仓库与 package.json。
---

# 芋道前端

先识别实际前端版本和源目录，读取 `package.json`、锁文件与路由/API 实现，再选该版本的文档。详情和资料基线的覆盖范围见[前端边界](../../references/frontend.md)。

Vue3 Element Plus 的文档模式是 `src/api/<module>` 对应 `src/views/<module>`，菜单的可见性、动态路由与后端权限需一起验证。Vben、Vue2 和 uni-app 分别核对本身的工程，不复用 Vue3 的文件路径或命令。

已核验源码基线的 `yudao-ui` 基本只有仓库链接，Vue3 目录只有少量 MES 片段；只有这些输入时，可以给出基于官方文档的方案与来源，不能声称已在完整前端运行或通过构建。
