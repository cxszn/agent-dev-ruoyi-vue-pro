# 前端版本与可验证边界

## 选择真实前端工程

已核验源码基线的 `yudao-ui` 下有 `yudao-ui-admin-vue3`、`yudao-ui-admin-vben`、`yudao-ui-admin-vue2`、`yudao-ui-admin-uniapp`、`yudao-ui-mall-uniapp` 五个目录。四个仅有 README 链接；Vue3 目录另有 5 个 MES API/视图片段，没有 `package.json`。这些文件不足以完成前端构建或真实页面验收。使用对应的独立前端仓库后，再按实际 `package.json`、锁文件和配置选择命令。

[官方快速启动](https://doc.iocoder.cn/quick-start-front/)把管理后台列为独立仓库：Vue3 + Element Plus、Vue3 + Vben、Vue2 + Element UI、Vue3 + uni-app。文档示例命令需结合对应仓库的实际工程文件核对。

## Vue3 Element Plus 的文档路径

[开发规范](https://doc.iocoder.cn/vue3/dev-spec/)以岗位管理为例：`src/api/system/post/index.ts`、`src/views/system/post/index.vue`、`PostForm.vue`。API 调用经过 axios 封装，包含授权和租户头、令牌刷新等；变更时核对用户实际仓库实现。业务页面可拆列表与表单，模块组件放模块目录。

[菜单路由](https://doc.iocoder.cn/vue3/route/)区分静态与登录后从后端菜单生成的动态路由；按钮示例用 `v-hasPermi`、`v-hasRole`，后端仍负责最终鉴权。菜单问题按后端 `get-permission-info`、角色授权、路由组件路径、权限字符串逐段查，不只看页面文件。

Vben、Vue2、uni-app 的路由、UI 库、构建命令各自独立。只有实际仓库到手后才能确认目录名、版本和运行结果。
