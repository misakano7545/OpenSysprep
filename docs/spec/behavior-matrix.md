# 行为对照表（M1 规格）

> 「原工具行为 → OpenSysprep 处置」逐条对照。**红线**行为永久禁止；重写项见 [capabilities.md](capabilities.md)。
> 证据：本机 `/root/dev/scpt-analysis`（分析报告与字符串证据清单）、`work/`（素材与日志）。

## 一、禁止行为（红线：不得存在任何代码路径）

| # | 原工具行为 | 证据（示例） | 为什么禁止 | 依据 |
|---|------------|--------------|------------|------|
| B1 | 改写 IE 主页（HKLM/HKCU，含 WOW6432Node `Start Page`） | 引擎代码与注册表路径字符串 | 静默变更用户设置 | 红线 1 |
| B2 | 改写 Edge/Chrome `Secure Preferences` 并伪造 HMAC 签名 | `prefs_enclave_x64.dll`、`strSecurePreferences`、`super_mac` 等 | 绕过浏览器防篡改机制 | Chromium 自 v25 起以 HMAC 保护该文件、明确阻止第三方静默修改（研究界已知攻击面） |
| B3 | 默认搜索劫持 | `dh.sejai.com`、`https://www.baidu.com/#tn=90013418_hao_pg...` | 流量变现、侵犯用户选择 | 红线 1、3 |
| B4 | 新标签页 / 起始页写入 | 配置模板 `homepages="https://newtabx.com/..."` | 推广 | 红线 1 |
| B5 | 静默安装扩展 / 软件 | 联盟推广链；`PUBC*` 模块 | 未授权安装 | 红线 2 |
| B6 | 伪装系统组件 | 模块版本信息冒用 Microsoft / 「NT Kernel & System」 | 对抗检测与审计 | 红线 4 |
| B7 | 计费 / 联盟参数 | 语言文件「联盟计费ID」；`tn=` 参数 | 商业推广闭环 | 红线 3 |
| B8 | 自动清理痕迹 | 引擎 `REG delete` 等自清理字符串 | 对抗审计 | 红线 4 |

## 二、重写行为（保留能力，透明、可卸载）

| # | 原工具行为 | OpenSysprep 处置 |
|---|------------|------------------|
| K1 | 部署组件注入 + 首启执行 | 显式 `install` / `once` 子命令；组件集中放自有目录；提供 `uninstall` |
| K2 | 私有配置（`Scdata.sc`） | TOML 明文配置；示例与字段说明随文档提供 |
| K3 | 默认用户配置修改 | 仅应用配置中显式声明、且通过白名单校验的项 |
| K4 | 部署日志 | 标准路径（`%ProgramData%\OpenSysprep\logs`）留存；不自动删除 |
| K5 | 系统设置应用 | 仅任务文件显式声明项；默认不提供任何浏览器相关项 |

## 三、执行保障（约束可执行化）

- **CI 静态审计**：`src/` 中出现红线标识（`newtabx`、`sejai`、`hao_pg`、`90013418`、`prefs_enclave`）即构建失败（见 `.github/workflows/ci.yml`）。
- **VM 验收**：M4 按 [`docs/verify-windows.md`](../verify-windows.md) 执行，逐项确认红线行为不存在、重写行为可用。
- **审计友好**：单文件静态产物；新增依赖最小化并记录理由；文档中文可读。

## 引用

- Microsoft Learn：*Sysprep (System Preparation) Overview* / *Use Answer Files with Sysprep* / *generalize*
- Chalmers 大学（2020）：*HMAC and "secure preferences": Revisiting chromium-based browsers security*
