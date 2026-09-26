# Windows 虚拟机验收清单（OpenSysprep）

> M4 运行级验收。静态验证在 CI；本清单只在 Windows 虚拟机（快照）中执行。
> 现状：先立框架，随 M3 功能落地逐步细化命令与检查项。

## 前置

- Windows 10/11 虚拟机 + 干净快照（每次验收前恢复）
- 被测产物：CI（windows job）产出的 `opensysprep.exe` artifact（或本地 `cargo build --release` 产物）
- 只读参考：原工具仅作对照，**不在真机运行原工具**

## A. 产物可运行性

- [ ] `opensysprep.exe version` 有输出且退出码为 0
- [ ] `opensysprep.exe help` 列出全部子命令
- [ ] 无缺失依赖，单文件产物直接可跑

## B. 功能验收（随 M3 落地逐项细化）

- [ ] `install`：组件只写入自有目录；注册项可见、可查询
- [ ] `once`：任务文件显式声明的项正确执行；日志落在 `%ProgramData%\OpenSysprep\logs`
- [ ] `uninstall`：清理干净（目录 / 注册项 / 计划任务均消失）
- [ ] 配置解析：非法配置被拒绝并给出可读错误

## C. 红线验收（必须全部"不存在"）

- [ ] 运行前后：IE 主页未被改动
- [ ] 运行前后：Edge / Chrome 的 `Secure Preferences` 未被改动（前后哈希对比）
- [ ] 运行前后：默认搜索、新标签页设置未被改动
- [ ] 无任何软件 / 扩展被静默安装
- [ ] 无对外推广 / 计费网络请求（抓包）
- [ ] 系统中无伪装命名的组件、无自动清理痕迹行为

## D. 回归与归档

- [ ] 结果（截图 / 日志 / 命令输出）归档到 issue 或 `docs/`
- [ ] 清单勾选完毕，更新 `docs/progress.md`
