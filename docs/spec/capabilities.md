# 能力清单（M1 规格）

> 来源：对「系统总裁封装工具（Scpt）」的静态逆向分析成果（只读参考：本机 `/root/dev/scpt-analysis` 与本仓库 `work/` 素材）。
> 方法：**证据 → 能力 → 处置**；每一行必须有证据支撑，无证据不写（宁缺勿编）。
> 处置口径：**重写** = 能力保留、洁净实现；**剔除** = 永久禁止（红线）；**待核** = 证据不足，后续里程碑再定。

## 0. 产品红线（永久禁止，不得存在任何代码路径）

1. 任何浏览器主页 / 起始页 / 新标签页 / 默认搜索引擎的设置或"修复"；
2. 任何扩展与软件的静默、强制或推广性安装；
3. 任何计费 / 联盟 / 推广参数（如 `tn=`、联盟 ID）及推广网络上报；
4. 任何对抗审计的行为：伪装成系统组件（版本信息仿冒）、随机化文件名、自动清除痕迹。

> 逐条依据见 [behavior-matrix.md](behavior-matrix.md)；CI 有静态审计步骤强制执行。

## 1. 封装准备（操作机侧）

| # | 能力 | 证据（示例） | 原行为 | 处置 |
|---|------|--------------|--------|------|
| 1.1 | 封装流程步骤化 | 主程序步骤字符串 `[Sysprep.AddDeployfiles] ScTasks` | 图形化多步骤流程，向待封装系统"加载部署组件" | 重写：显式子命令，步骤透明可见 |
| 1.2 | 部署组件注入 | `FUNNKRX64` / `FUNNKR`、`ScTasks.exe`、`ScDeploy.exe` | 释放引擎到 `\System32\`，经 Run/RunOnce 触发 | 重写：组件只放自有目录；注册项可见、可卸载 |
| 1.3 | 部署配置生成 | `Scdata.sc`（`[Sysprep.AddDeployfiles.CreateScdata]`） | 私有 / 不透明配置格式 | 重写：TOML 明文配置，人类可读可审 |
| 1.4 | Sysprep 调用 | 官方流程对照（MS Learn）；`sysprep utility` 类模块 | 调用 / 伴随系统 sysprep | 重写：直接调用系统 `sysprep.exe`，不捆绑微软文件 |
| 1.5 | 驱动 / 组件处理 | `SetupCL` / `Windows Setup API` 类模块（FUNC 等） | 捆绑并调用 | 待核：优先评估系统自带工具（pnputil / DISM）覆盖范围 |
| 1.6 | 封装日志 | `~\Temp\~ScLog\ScTaskRun.log` | 临时目录日志，可被清理 | 重写：`%ProgramData%\OpenSysprep\logs`，不自动删除 |

## 2. 部署执行（目标机侧）

| # | 能力 | 证据（示例） | 原行为 | 处置 |
|---|------|--------------|--------|------|
| 2.1 | 首启任务链 | Run/RunOnce 值 `ScDesktop` / `ScAir` / `ScReg` / `DrvCeo` / `InDeploy` / `Es4InDeploy` | 多阶段任务链，执行后自清理 | 重写：单一 `once` 命令，执行后可显式卸载 |
| 2.2 | 系统设置应用 | 引擎注册表操作代码 | 广泛修改系统设置 | 重写：只执行任务文件中显式声明的项，白名单校验 |
| 2.3 | 默认用户配置 | `FUNM*`（魔改 ForensiT DefProf；`NTUSER.DAT`、`SCRUNTEMP`） | 修改默认用户注册表 | 重写：仅显式声明项；**永不触碰浏览器相关键** |
| 2.4 | 静默软件安装 | 联盟推广链证据 | 静默安装推广软件 | **剔除**（红线 2） |
| 2.5 | 浏览器配置 | `https://newtabx.com/`、`prefs_enclave_x64.dll`、`dh.sejai.com`、`tn=90013418_hao_pg` | 改主页 / 搜索 / 新标签页，伪造 Secure Preferences 签名 | **剔除**（红线 1、3） |
| 2.6 | 伪装与痕迹清理 | 模块版本信息冒用「NT Kernel & System」等 | 伪装系统组件、自动清理痕迹 | **剔除**（红线 4） |

## 3. 商业模式（不进入本项目）

| # | 能力 | 证据 | 处置 |
|---|------|------|------|
| 3.1 | 联盟计费 / 积分 | 语言文件「联盟计费ID」「把你的推广软件集成到系统」等 | **剔除** |
| 3.2 | 推广资源管理与下发 | `PUBC*` 系列模块（含第三方安装包） | **剔除** |

## 4. 第三方组件（不复制）

原工具内嵌多种第三方二进制（存在改造与伪装）：7-Zip、SetACL、ForensiT DefProf、Sysinternals 类工具、Inno Setup 安装包等（证据：模块版本信息与字符串）。
处置：**不内嵌第三方二进制**；功能优先调用系统自带组件或由用户自备，理由记录于提交说明。

## 5. 待核清单（进入 M2/M3 前验证）

- 1.5：驱动处理的实际范围与必要性；
- "系统体检 / 优化"类功能的完整清单（当前证据零散）；
- 镜像打包 / 导出方式（未确认，勿假设）。

## 6. 参考（官方 / 权威）

- Microsoft Learn：*Sysprep (System Preparation) Overview*、*Sysprep Process Overview*、*Use Answer Files with Sysprep*、*generalize*
- Chalmers 大学研究（2020）：*HMAC and "secure preferences": Revisiting chromium-based browsers security*（静默修改受保护浏览器配置的已知攻击面）
