# SCPT 全量解析：模块 → 功能 → 原实现 → Rust 还原方案

> 证据来源：主程序脱壳镜像（`01-unpacked/Scpt.unpacked.exe`）、**42 个模块 + 3 个内嵌组件**（`work/engines/`）、205 个资源、语言文件 567 条文案（其中 411 条界面控件）。
> 逐模块原始证据（版本信息/导入/资源/特征字符串）：`docs/analysis/module-dossiers.md`（自动生成，44 条）。
> 校验：42 个模块中原为 UPX 加壳的 20 个，用 `upx -d` 从原包独立重脱壳后与 `work/engines` **sha256 逐一相同** → 分析基座无损。
> 自动扫描原始输出：`work/analysis/full_inventory.md`、`feature_matrix.md`、`main_flow.txt`、`strings_detail.md`、`unknown_modules.md`、`ui_controls.txt`。
> 目标：**功能 1:1 还原，零流氓**（不实现任何浏览器篡改、推广安装、内核锁）。

---

## 一、总览：SCPT 是什么、怎么工作

**三层结构**（所有模块都能归到这三层）：

| 层 | 组成 | 职责 |
|---|---|---|
| ① 主程序 | `Scpt.exe`（Delphi + ASPack） | 界面 + 封装流程编排（60 个流程标记）+ 资源仓库（42 个模块 + 3 个内嵌组件、语言、皮肤、测试数据） |
| ② 部署引擎 | `FUNN` 家族（ScTasks） | 封装时被写入目标系统，首次开机执行部署（原来含浏览器篡改） |
| ③ 辅助工具/驱动 | `FUN*` / `PUBC*` | 驱动包解压(7-Zip)、驱动安装(devcon)、权限(SetACL)、默认用户配置(DefProf)、内核驱动(Scufd.sys) 等 |

**封装流程**（主程序标记串联，按出现频次排序）：

| 步骤标记 | 次数 | 作用 | Rust 方案 |
|---|---:|---|---|
| `Sysprep.AddDeployfiles` | 54 | 把部署组件写进目标系统（部署链起点） | 重写为 `install`（组件写自有目录） |
| `ScfudDevice.NTlock` | 40 | 内核驱动锁脚本（防篡改，见 §3.13） | **剔除** |
| `Sysprep.Systemsettings` | 27 | 应用系统设置（优化项/首次进桌面项） | 重写（白名单） |
| `Sysprep.LoadsrsDrivers` | 21 | 加载 SRS 磁盘控制器驱动 | 重写（pnputil/DISM） |
| `Sysprep.Run` | 19 | 调用系统 sysprep 封装 | 重写（直接调 sysprep.exe） |
| `Sysprep.RemoveDriver` | 9 | 卸载本机设备驱动 | 重写（pnputil） |
| `Sysprep.SafeModule` | 9 | 「防流氓」特权模块 | **剔除**（联盟特权，含劫持检测） |
| `HotFix.Install` | 8 | 补丁安装 | 待核 |
| `Sysprep.WriteUnattend` | 8 | 写应答文件（unattend） | 重写 |
| `Sysprep.SynchronizationInfo` | 6 | 同步封装前信息（主页/收藏夹） | 重写为**仅收藏夹/文档**，主页项**剔除** |
| `Sysprep.ChangeHdc` | 5 | 更换 IDE/HDC 控制器驱动（换机兼容） | 重写 |
| `Sysprep.ChangeStandardPC` | 4 | 电源模式改 StandardPC | 重写（可选） |
| `Sysprep.Decodesysprep` | 4 | 写入封装文件（解码） | 重写 |
| `Sysprep.ClearJunkfiles` | 3 | 封装后清理垃圾文件 | 重写 |
| `Sysprep.ClearOldinfo` | 3 | 清理旧信息 | 重写 |
| `Sysprep.NT6.Type` | 3 | NT6 系统类型适配 | 重写 |
| `Sysprep.SccNet` | 3 | 网络设置 | 重写 |
| `Sysprep.Shal` | 3 | HAL 相关处理 | 待核 |
| `Sysprep.AddDeployfiles.CreateScdata` | 2 | 生成部署配置 `Scdata.sc` | 重写（TOML 明文） |

---

## 二、功能清单（来自语言文件 411 控件）→ 模块 → 原实现 → Rust 方案

### 3.1 系统体检 / 封装体检
- 原功能：`Gb_Osallinfo`（系统体检：系统名称/内核版本/位宽/封装支持/系统分区/当前用户/运行环境/容量）、`Btn_Scan`（封装体检）、`Btn_OsRepair`（一键修复）
- 涉及模块：主程序内实现（无独立模块）
- Rust：✅ **已实现**（`src/doctor.rs` + GUI 封装页）——检查 sysprep 存在性、克隆痕迹等；待补：系统信息展示、一键修复（只读建议 + 显式修复项）

### 3.2 封装方式与封装流程
- 原功能：`Gb_Sysprep_Type`（封装方式：传统/防流氓/大客户高级）、`Lab_AfterSysprep`（封装后：停留/重启/关机）、`Cb_Uninstalldriver`（卸载本机驱动）、`Cb_LoadSrsDrv`（加载 SRS）、`Cb_Cleanjunkfiles`（清理垃圾）、`Cb_Dllcache`（清理 DLLCache）
- 涉及模块：`Sysprep.*` 系列 + `FUND/FUNF/FUNFX64`（NetSetupPrepareSysPrep/OOBE）、`FUNE/FUNG/GX64`（SetupCL）、`FUNA/FUNI`（INF）
- 原实现：调用系统 `sysprep.exe /generalize /oobe`，配套写 unattend、换 HDC 驱动、清理
- Rust：重写 `Sysprep.*` 流程为显式子命令：`doctor` → `apply`（白名单设置）→ `sysprep`（调系统 sysprep）→ `clean`；**删除**「防流氓/大客户」两种联盟特权方式

### 3.3 部署设置与部署模块
- 原功能：`Gb_DeploySet`（部署设置）、`Gb_DeployModular`（部署模块：四格进度/Aero 风格/多彩进度条/图片控件）、`Lab_DeployResolution`、`Lab_DeployFontcolour`
- 涉及模块：`FUNP`/`PUBCA`/`PUBCF`/`FUNR`/`FUNS`/`FUNX`（进度界面×372–437）、`FUNZ`（界面）、`FUNT/U/Y/PUBCG`（小程序）
- 原实现：部署期间显示自定义进度界面（皮肤控件 + 文字/颜色/进度条配置）
- Rust：**保留功能**，实现为 `once` 执行时的控制台/轻量进度输出；GUI 皮肤不做逐像素还原（见 §5 边界）

### 3.4 任务计划（部署前/中/后）
- 原功能：`Tilte_MFTasklist`（编辑任务计划）、`Btn_RunPlan1/2/3`（部署前/中/后）、`Btn_Add`（添加任务）、`Items_Tasktype`/`Items_Tasktip`
- 涉及模块：`FUNN` 家族（部署引擎，任务执行）
- 原实现：GUI 编辑任务 → 写入 `Scdata.sc` → 部署时由 ScTasks 逐条执行
- Rust：✅ **已实现核心**（`src/config.rs` TOML + `src/runner.rs` 阶段执行 + `run` 子命令 + 白名单校验）；待补：GUI 任务计划页接真数据、任务编辑器

### 3.5 驱动（SRS / 驱动包 / 设备安装）
- 原功能：`Gb_SRS`（导入磁盘控制器驱动）、`RB_LoadSCsrs`（内置 SRS）/`RB_Loaddiy`（指定驱动）、`Cb_Driveinstall`（联网安装缺失驱动）、`Cb_ClearSrs`（清理多余 SRS）
- 涉及模块：`FUNA`/`FUNI`（IDE/HDC、HAL INF）、`FUNK`（7-Zip 解压驱动包）、`FUNB`/`FUNC`（devcon 改造版：UpdateDriverForPlugAndPlayDevicesW）、`FUNJ`（SetACL 权限）
- 原实现：7-Zip 解压驱动包 → devcon/pnputil 安装 → SetACL 设权限 → 换 HDC 驱动保证换机兼容
- Rust：重写：`drivers` 子命令（扫描驱动目录 → `pnputil /add-driver`）；**不捆绑**内置 SRS（NC 版权 + 体积），改由用户提供；不内嵌 7-Zip/devcon/SetACL（用系统 `tar`/`pnputil`/`icacls`）

### 3.6 系统优化
- 原功能：`optimize_*` 20+ 项（磁盘访问超时、内存配置、程序响应、处理器资源、NTFS 管理、Aero 视觉、开始菜单显示、任务栏预览、允许未签名驱动、WINS 查询、网络快速转发、TTL、网络参数、文件列表刷新、进程优先级、启动分区优化、数据储存、DllCache 备份）
- 涉及模块：主程序内实现（注册表写入）
- 原实现：批量写注册表/服务配置
- Rust：重写为 **显式清单**：每条优化 = 一条注册表变更（配置里声明，白名单校验，可回滚）；GUI 系统优化页列出条目 + 勾选

### 3.7 OEM 智能识别
- 原功能：`Btn_OemSet`（OEM 设置）、`SA_Gb_oem`（遇品牌电脑设置计算机属性/桌面壁纸/部署图片）
- 涉及模块：`FUNV`（OEM 素材包：`Scoem/<品牌>/{bg.jpg,nt5.bmp,nt5.ico,nt5.ini,nt6.bmp,nt6.ini}`，OEM 命中 ×878）、`FUNM*`（默认用户配置）
- 原实现：按主板品牌匹配素材目录 → 设置 OEM 信息/壁纸/部署图
- Rust：**保留功能**，但**不捆绑**素材包（20+ 品牌版权图）；实现：读 OEM 标识 → 从用户提供的素材目录匹配；`oem` 子命令

### 3.8 首次进桌面（部署时应用）
- 原功能（语言文件）：`Gb_Targetsys_Desktop`（首次进桌面）、刷新率/颜色质量、`Cb_Locktaskbar`/`Cb_Unlocktaskbar`（任务栏固定/取消）、`Cb_MoveDocuments`（智能转移我的文档）、`Cb_MoveFavorites`（智能转移 IE 收藏夹）、`Cb_MovePageFile`（智能转移虚拟内存）、`Cb_CloseKeypad`（关闭小键盘）、`Cb_Dormancy`（开启休眠）、`Cb_AutoSetip`（自动设置 IP：固定/随机）、`Cb_SetNetWork`（自动设置网络位置）、`Cb_CloseRestartbox`（关闭重启对话框）、`Cb_SetResolution`（设置分辨率）、`Cb_ResolutionSos`（黑屏急救 Ctrl+F11）
- 涉及模块：`FUNM*`（DefProf 默认用户配置移植：NTUSER.DAT/SCRUNTEMP，命中 ×111）、`FUNN`（部署时应用）、`FUND/FUNF`（网络设置 netshell）
- 原实现：部署时改默认用户注册表 + 系统设置
- Rust：重写为 `once` 的显式任务项（白名单内）；**主页/新标签相关一律不做**（原 `Cb_Saveiehp` 主页同步项直接剔除）

### 3.9 清理
- 原功能：`Cb_Cleanjunkfiles`（清理垃圾）、`Cb_Dllcache`（DLLCache 备份/还原）、`Sysprep.ClearOldinfo`
- 涉及模块：主程序 + 部署引擎
- Rust：重写 `clean` 子命令（清理清单显式声明）

### 3.10 高级设置
- 原功能：`Btn_Sysprepaset`（高级设置）、`Rb_Sysprep_Type*`（联盟特权方式）、`SA_Gb_hijack`（部署主控被劫持的处理策略）
- 涉及模块：主程序
- Rust：**剔除**（联盟特权 + 劫持检测属流氓机制）

### 3.11 【剔除】浏览器篡改（核心红线）
- 证据：`FUNN`/`FUNNX64`（浏览器篡改命中 ×86：`newtabx`、`sejai`、`hao_pg`、`prefs_enclave`、`BLBeacon`）、`FUNB_embed.raw`（内嵌 DLL：`setedge`、`Secure Preferences`、`newtabx` + OpenSSL AES/GHASH/SHA 用于伪造 HMAC 签名）、`Sysprep.SynchronizationInfo`
- 原实现：改 IE 主页/收藏夹同步、改 Edge/Chrome `Secure Preferences` 新标签页 = `https://newtabx.com/`、默认搜索劫持（`dh.sejai.com`、百度 `tn=90013418_hao_pg`）、伪造 HMAC 使设置无法还原
- Rust：**不实现**。CI 红线审计强制（src/ 出现这些标识即构建失败）

### 3.12 【剔除】推广安装
- 证据：`Cb_Mboxinstall`（联网安装总裁软件安装器）、`Lab_Mbox`（软件魔盒）、`PUBCE`（19MB Inno Setup 安装包）、联盟计费文案（`Lab_Ceounionuid`）
- Rust：**不实现**

### 3.13 【剔除】内核驱动与脚本锁（"卸载不掉"的根因）
- 证据：主程序 `Scufd.sys` + `\\.\ScfudDevice` + `[ScfudDevice] Unlock Kernel` + `[ScfudDevice.NTlock] 无法修改脚本属性/关闭脚本失败`；`PUBCB/PUBCC/PUBCD`（x86/x64/NT5 三版驱动，PDB：`driver\nt6\...\scdrv.pdb`，服务名伪装 `Microsoft Time-Stamp Service`）
- 原实现：内核驱动锁住部署脚本（`.sc`）属性，用户无法修改/删除 → 篡改无法清除
- Rust：**不实现**（零内核驱动、零脚本锁；我们的部署配置是明文 TOML，用户随时可改可删）

---

## 四、42 个模块 + 3 个内嵌组件：逐个映射

> 身份全部来自**逐模块自动解析**（版本信息资源 + 导入表 + 资源树 + 双编码字符串），原始证据见 `module-dossiers.md`。
> PE 时间戳：`FUNN`/`FUNNX64` = 2026-05-15；`FUNNKR` 家族与 `FUNM` 家族 = 2025-05-23；`FUNO` = 2021-04-09。
> 「伪装」= 版本信息冒充他人（Microsoft/内核）。

### 4.1 部署引擎（ScTasks 线）

| 模块 | 身份（证据） | 对应功能 | Rust 方案 |
|---|---|---|---|
| `FUNN` | 版本信息**匿名**：`CompanyName/FileDescription/ProductName = TOOL`（2026-05-15）；内嵌 DATA = FUNA/FUNB/FUNC | 正式部署引擎：执行部署任务 + **内嵌浏览器篡改组件** + `Mboxinstall`（软件魔盒，含 MD5 校验） | 重写为单一洁净引擎 |
| `FUNNX64` | 同上（x64，14.6MB） | 同上 | 同上 |
| `FUNNKR` | **伪装** `Microsoft` / `ntkrnlmp.exe` / "NT Kernel & System" / 6.1.7601.17514；**无内嵌组件**；独有 `MiniDriverInstall`、`DriverMessage`、`System32\drivers`、`CurrentControlSet\Services\ScProtect` | KR 版部署引擎：**不篡改浏览器**，改为装 mini 驱动 + 建 `ScProtect` 服务（内核态保护） | 只做洁净引擎，**不实现驱动与服务伪装** |
| `FUNNKRX64` | 同上（x64） | 同上 | 同上 |

### 4.2 系统设置 / 首启执行

| 模块 | 身份（证据） | 对应功能 | Rust 方案 |
|---|---|---|---|
| `FUND` | **伪装** `Microsoft` / `sysprep utility` / 内部名 `sysprep.EXE` / 5.1.2600.1106 (xpsp1.020828-1920)——即 XP SP1 原件版本号；含 IE 注册表 `Internet Explorer\International`、`TypedURLs` | 网络位置/网络设置（netshell、`NetSetupPrepareSysPrep`）；另写 IE 痕迹相关键 | `netsh`/PowerShell；IE 相关**不做** |
| `FUNF`、`FUNFX64` | 同 `FUND`（x86 / x64 两份） | 同上 | 同上 |
| `FUNE`、`FUNG`、`FUNGX64` | **伪装** `Microsoft` / `SetupCL utility` / `Setupcl.EXE` | sysprep 首启执行器（SetupComplete + SYSTEM hive 操作） | 用系统自带 `setupcomplete.cmd` |
| `FUNH` | NTLDR（283KB，DOS COM 形态）；内含 `ntkrnlmp.exe`/`ntkrnlup.exe`（单/多核内核与 HAL 清单） | 引导文件替换 + 内核/HAL 适配（`Sysprep.Shal`/`ChangeStandardPC`） | 需要时用 `bcdboot`；**不替换系统内核** |
| `FUNI` | 313B INF 文本 | HAL/CA 相关 INF | 不捆绑 |

### 4.3 驱动与权限

| 模块 | 身份（证据） | 对应功能 | Rust 方案 |
|---|---|---|---|
| `FUNB` | **伪装** `Microsoft` / "Windows Setup API" / 内部名 `SETUPAPI.DLL`（x86） | devcon 改造版：`UpdateDriverForPlugAndPlayDevicesW` 装驱动 | `pnputil` |
| `FUNC` | 同上（x64） | 同上 | `pnputil` |
| `FUNJ` | `Helge Klein` / `SetACL` | 文件/注册表权限设置 | `icacls`/`reg` |
| `FUNK` | 改标 `SysCeo` / "SysCeo Runtime library" / `Sczip`（内核为 Igor Pavlov 7-Zip 9.20）；内嵌 DATA = FUNA…FUNI（8 个 INF） | 驱动包/资源包解压 + 自带 SRS INF 集 | 系统 `tar`；INF 由用户提供 |
| `PUBCB`、`PUBCC` | 内核驱动 `scdrv`（x86 / x64）；PDB `driver\nt6\objfre_win7_*\scdrv.pdb`；**服务名伪装 "Microsoft Time-Stamp Service"** | **内核驱动**：脚本/文件锁 + 强制删除 | **不实现**（零内核驱动） |
| `PUBCD` | 同族 NT5 版（XP/2003 线，含 WoSign 签名链） | 同上 | **不实现** |
| `PUBCI` | x64；导入 `AUTHZ/DSPARSE/DSROLE/DUI70/DUser/RPCRT4/Secur32/UxTheme/logoncli/netutils/samcli`；宽字符含 ACL 编辑器对话框控件名（`Static add ACE`/`PermissionEntry`/`objperm`/`ClearPerm`/`InheritImmediateAuditing`…） | **权限编辑 / 账户解析工具**：给文件/注册表对象设或清 ACL（DUI70+DSPARSE=现代"选择用户或组"） | 用 `icacls`；**不实现**（详见 §6.3） |
| `PUBCH` | x64、MSVC；**无导入表/资源/字符串**；含 `mov rax, gs:[0x60]`（PEB 自解析 API）2 处 | **防流氓线的 x64 载荷/存根**（形态确证；具体动作无据可证） | **不实现**（详见 §6.3–6.4） |

### 4.4 用户配置 / 部署界面

| 模块 | 身份（证据） | 对应功能 | Rust 方案 |
|---|---|---|---|
| `FUNM`、`FUNMX64` | `ForensiT Limited` / "Set Default Profile" / `Defprof` 魔改；内嵌 DATA = FUNA/FUNB/FUNE（含篡改组件） | 默认用户配置移植（`NTUSER.DAT`/`SCRUNTEMP`） | 保留功能，白名单显式项 |
| `FUNMKR`、`FUNMKRX64` | 同上（KR 变体）；**内嵌 5 个组件 FUNA/FUNB/FUNE/FUNF/FUNG**（比 `FUNM` 多 FUNF/FUNG → 自足打包）；`FUNMKRX64` 另有 `ScProtectInstall`/`MiniDriverInstall` + ForceDelete 驱动 PDB | KR 版默认用户配置 + 驱动安装 | 同上；**不实现驱动部分** |
| `FUNO`、`FUNOX64` | `Sysceo.com` / `ScDeployBG_x86`/`_x64`；`DecryptScdata`、`Scdata.sc` | 部署后台/背景程序（读配置、跑部署阶段） | 并入 `once` |
| `FUNP`、`PUBCA` | `Sysceo.com` / `ScProcessBar_x86`、`ScColourProcessBar_x86` | 部署进度条 / 彩色进度条界面 | 轻量进度输出（不做像素还原） |
| `PUBCF` | `Sysceo.com` / `Scpicm`（`TSCPM`/`TTKMF` 窗体，`/Edeploy`） | 部署图片/部署界面程序 | 同上 |
| `PUBCG` | `SysCeo.Com` / `ScRestart`（`TFORM1`） | 部署后重启/关机提示 | 并入 `once` |
| `FUNX` | `Sysceo.com` / `Scskipwlan`（`TSWLAN` 窗体） | 跳过 WLAN/OOBE 网络设置 | 并入 `once` |
| `FUNY` | `SysCeo.Com` / `ScSFC`（`TFORM1`）；引用 `ScDeploy.exe`/`ScTasks.exe` | 部署辅助（SFC/部署链） | 并入 `once` |
| `FUNT` | `Www.SysCeo.Com` / `ScClosemsbox` | 小型助手（提示框处理） | 并入 `once` |
| `FUNU` | `SysCeo.Com` / `By:Noime` | 小型助手 | 并入 `once` |
| `FUNZ` | 极小 Delphi 应用（资源仅 `DVCLAL`，无窗体） | 无 UI 的部署链模块 | **不实现** |

### 4.5 网络 / 素材 / 推广

| 模块 | 身份（证据） | 对应功能 | Rust 方案 |
|---|---|---|---|
| `FUNQ` | `Sysceo.com` / `Scaddnet` 3.0.0.0（**ASPack 2.42 已完整脱壳**，见 §7）——`[ADSL]`/`[宽带连接]` 配置、`.lnk`、`TSCCNET` 窗体 | 宽带/ADSL 拨号、IP 设置、网络位置、任务栏固定 | `netsh`/`rasdial`；已核**零浏览器相关代码** |
| `FUNV` | OEM 素材 ZIP（6.5MB，`Scoem/<品牌>/`，OEM×320） | OEM 智能识别素材 | 保留功能，素材由用户提供 |
| `FUNR` | `SysCeo.com` / "驱动总裁在线安装程序"（`TONLINESETUP`） | 联网安装驱动（驱动总裁） | **不实现**（用户自备驱动） |
| `FUNS` | `SysCeo.com` / "软件魔盒在线安装程序"（PDB `E:\Data\Sysceo\CeoMbox\mbolinst`） | 联网安装软件魔盒（推广） | **不实现** |
| `PUBCE` | Inno Setup 5.6.0 安装包 → `app/AppBox.exe` = `SysCeo.com`「软件魔盒」3.0.0.15 | 推广安装（软件魔盒 + aria2 + 迅雷 + 7z + 自更新） | **不实现**（清单见 §6.2） |

### 4.6 内嵌组件（从 `FUNN`/`FUNM` 的 DATA 资源解出）

| 组件 | 来源/身份 | 作用 | Rust 方案 |
|---|---|---|---|
| `FUNA_embed` | 内嵌于 `FUNN`/`FUNM`（伪装 `TOOL`/`Crun.exe`） | 部署链子模块（启动器） | 重写 |
| `FUNB_embed` | **浏览器配置 DLL**（`bcfgs`，含 `setedge` + BoringSSL/OpenSSL 链） | 浏览器篡改 + **伪造 HMAC 使设置不可还原** | **剔除** |
| `FUNC_embed` | 内嵌于 `FUNN`（Delphi，x86） | 部署链子模块 | 重写 |

---

## 五、1:1 还原边界（明确范围）

**1:1 = 功能层面一致**（用户能做的操作、达成的效果一致），**不是**逐字节复制二进制，也**不包含**任何流氓机制。

**保留并还原（按优先级）**：
1. 封装体检（doctor）✅ 已有雏形
2. 封装设置 + 封装流程（apply → sysprep → clean）
3. 任务计划（部署前/中/后 + TOML 配置）✅ 已有核心
4. 驱动导入（pnputil 封装）
5. 首次进桌面项（分辨率/任务栏/文档转移/虚拟内存/IP/网络/小键盘/休眠）
6. 系统优化（显式清单、可回滚）
7. OEM 智能识别（素材由用户提供）
8. 部署进度展示（轻量）

**永久剔除**：浏览器主页/新标签/搜索（§3.11）、推广安装（§3.12）、内核驱动与脚本锁（§3.13）、联盟特权与计费（§3.10）、伪装与痕迹清理。

**不还原（技术理由）**：DELPHI 皮肤像素级界面、捆绑的第三方二进制（7-Zip/SetACL/devcon/NTLDR/驱动包/品牌素材）。

---

## 六、待核项：核验结论（全部已核，无遗留）

### 6.1 `FUNNKR` vs `FUNN` —— 同一引擎的两条发行线，**不是改名**

| 维度 | `FUNN` / `FUNNX64` | `FUNNKR` / `FUNNKRX64` |
|---|---|---|
| 版本信息 | **匿名**：`CompanyName`/`FileDescription`/`ProductName` = `TOOL` | **伪装**：`Microsoft Corporation` / `ntkrnlmp.exe` / "NT Kernel & System" / `6.1.7601.17514`（Win7 SP1 内核版本号） |
| PE 时间戳 | 2026-05-15 | 2025-05-23 |
| 体积（x86） | 12,525,840 | 3,383,808 |
| 内嵌 DATA 组件 | FUNA / FUNB / FUNC（**篡改组件**） | **无** |
| 浏览器篡改标识 | `newtabx.com`、`sejai.com`、`Secure Preferences`、`User Data\Default\Secure` | **零命中**（差集为空） |
| 独有机制 | `Mboxinstall`（软件魔盒安装 + MD5 校验） | `MiniDriverInstall`、`DriverMessage`、`System32\drivers`、`CurrentControlSet\Services\ScProtect` |
| 窗体类 / 任务标记 | x86 有 3 个 / x64 有 4 个窗体类，**两版完全相同**；`Sysprep.*`、`Cb_*` 标记都在主程序、不在引擎 | 同 |

**结论**：`KR` 是**内核化发行线**——「装 mini 驱动 + 建 `ScProtect` 服务 + 冒充系统内核」替代「劫持浏览器」；正式线反之（劫持浏览器 + 匿名版本信息）。
两者共用同一引擎骨架与窗体集，差异集中在**尾部机制与内嵌载荷**。
Rust 侧：只实现**单一洁净引擎**，两条线的流氓机制都不还原（§五）。

### 6.2 `PUBCE` 安装包清单

Inno Setup **5.6.0 (unicode)**，`AppName = 软件魔盒`；解包 **245 个文件**（`work/pubce/`）：

| 组件 | 身份（版本信息） | 作用 |
|---|---|---|
| `app/AppBox.exe` | `SysCeo.com`「软件魔盒」3.0.0.15 | 主程序（软件商店/推荐墙 UI） |
| `app/plug/update/AbUpdate.exe` | 软件魔盒更新模块 3.0.0.0 | 自更新 |
| `app/plug/AbLauncher.exe` | 软件魔盒-智能模块 3.0.0.2 | 拉起/守护 |
| `app/UninsFile/uninst.exe` + `istask.dll` | 软件魔盒-卸载 3.0.0.11 | 卸载 + 计划任务 |
| `app/plug/aria2/aria2c.exe`、`aria2c_nt5.exe` | aria2（无版本信息） | 下载引擎（NT6/NT5 双版） |
| `app/plug/xunlei/download/*` | `Thunder Networking Technologies` 5.0.2.289 | **迅雷 P2P 下载引擎**（含 `dl_peer_id.dll`、`XLbt.dll`） |
| `app/plug/7z/7za.dll` | `Igor Pavlov` 7-Zip 9.20 | 解压 |
| `app/plug/Counter.exe` | `Sysceo.com`「Counter_BD」2.0.0.0 | 计数/上报 |
| `app/Skin/{dark,light}`、`app/Languages/{zh_cn,zh_hk,zh_tw,en_us}.ini` | — | 皮肤（182 文件）/ 多语言（4 文件） |
| `tmp/botva2.dll`、`InnoCallback.dll` | — | Inno 皮肤/回调库 |

Rust 侧：**不实现**（不捆绑、不联网推广）。

### 6.3 `PUBCH` / `PUBCI` 用途 + 资源损坏（无法执行、无法复原）

**事实**：两者是 **x64 小体量 native 程序**（4032B / 5007B，MSVC，含 `.pdata`），原本存放在主程序的 `DATA` 资源里。

**损坏归属（厂商侧）**：原包 20 个 UPX 模块用 `upx -d` **独立重脱壳**后与 `work/engines/` 逐一 **sha256 相同**（说明我们的导出链无损）；而 PUBCH/PUBCI 在 ASPack 解压后的 `.rsrc` 流里**就已经是损坏字节**，同一区域前后的字符串表、相邻的 `LANGS/SCCHS` 均完好。

**损坏模型**（用 DOS stub 逐字节反推验证）：

1. 每个 `0x00` → `0x20`（空格）；
2. GBK 非法双字节序列（前导 `0x81–0xFE` + 非法尾字节）折叠成单个 `0x3F`（`?`）。

例：标准 14 字节 DOS stub `0E 1F BA 0E 00 B4 09 CD 21 B8 01 4C CD 21` 在文件里正是 `0E 1F 3F 20 3F 3F 3F 4C 3F`。
后果：`e_lfanew`、`Machine`（`64 3F`）、节表数值字段等**不可逆丢失** → `file` 只认出 "MS-DOS executable"。

**可确证部分**：

- `PUBCI`：导入 `AUTHZ.dll`、`DSPARSE.dll`、`DSROLE.dll`、`DUI70.dll`、`DUser.dll`、`RPCRT4.dll`、`Secur32.dll`、`UxTheme.dll`、`logoncli.dll`、`netutils.dll`、`samcli.dll`；宽字符含 ACL 编辑器对话框控件名（`Static add ACE`、`PermissionEntry`、`objperm`、`propperm`、`ClearPerm`、`InheritImmediateAuditing`…）
  → **权限编辑 / 账户解析工具**：`DUI70`+`DSPARSE` = 现代"选择用户或组"对话框，`SAM/DSROLE/logoncli/netutils` = 账户与 SID 解析，`AUTHZ` = 访问检查；用途是为文件/注册表对象**设置或清除 ACL**（配合 §3.13 的脚本锁）。
- `PUBCH`（x64，4032B）**无导入名、无字符串、无 manifest**——第一轮只能判"未确证"。第二轮专项反查后的结论见 §6.4。

Rust 侧：**不实现**（权限用系统 `icacls`/`reg`）。

### 6.4 `PUBCH` 专项反查（第二轮：引用点 + 载荷特征）

**反查路径与结果**：

| 反查手段 | 结果 |
|---|---|
| 损坏 stub 在全镜像的位置 | 仅 **2 处**：`0x51e1b1c`（= PUBCH 资源 RVA `0x51e1adc` + `0x40`）、`0x51e2adc`（= PUBCI RVA + `0x40`）→ **无完好副本**；损坏发生在厂商存资源之前 |
| 模块名引用（全模块 + 主程序搜 `PUBCH`/`PUBCI`） | **0 处**（各模块里的 `PUB` 命中全是 Delphi RTTI 噪声 `NonPublicType`/`IsPublicType`）→ 名字不落地，由**加密配置**（见更新日志「配置文件私人专属加密」）驱动落盘 |
| 宽字符提取 | PUBCH **0 条**；PUBCI 28 条 = 完整 ACL 编辑器控件名集（`ACEEditor`/`ACEType`/`PermissionsList`/`objperm`/`propPermHeader`/`InheritImmediateAuditing`/`ChangePrincipal`/`ShowBasic`…） |
| x64 代码惯用法 | PUBCH 含 **`mov rax, gs:[0x60]`（PEB）两处**（损坏形态 `65 48 3F 25 60 20 20 20`，按损坏模型可复原为 `65 48 8B 04 25 60 00 00 00`）；PUBCI **0 处** |

**判定**：`PUBCH` = **无导入表 + 经 PEB 自解析 API 的小型 x64 载荷/存根**（不是常规可执行程序：没有导入、资源、清单、版本信息，也没有任何字符串常量可达路径）。
**具体动作仍无法确证**——没有任何字符串/资源可作依据，仅能确定其"载荷形态"。

**语境（不作确证，仅记录）**：更新日志（`scpt-analysis/04-evidence/公告.txt`）显示防流氓线长期主线：
- `3.0.0.122`（2021-05-21）「新增 SC 部署过程中防止文件被删除的保护功能 [仅支持 防流氓封装方式/大客户封装方式]」
- `3.0.0.119`（2021-04-10）「新增 SC 配置文件私人专属加密功能 [同上两种封装方式]」
- `3.0.0.98`「部署主控被劫持的行为处理选项」；几乎每个版本都写「加强/升级防流氓机制代码」
- `3.0.0.178`（2026-05-15）「加强防流氓机制代码」

Rust 侧：**不实现**（该载荷属于防流氓/KR 线专属，功能不在还原范围内）。

### 6.5 附带查获（本轮新增证据）

| 证据 | 内容 |
|---|---|
| 主程序内嵌 **ZIP 驱动包** | `ScProtect_10x64.sys`、`ScProtect_81x64.sys`、`ScProtect_8x64.sys`、`ScProtect_7x64.sys`（Win10/8.1/8/7 各一），由 `MiniDriverInstall`/`ScProtectInstall` 安装 |
| 驱动伪装名（确认） | `PUBCB`/`PUBCC` = **"Microsoft Time-Stamp Service"**；`PUBCD` = **"WoSign Time Stamping Service"** |
| `ScProtect` 引用者 | `FUNM`(2)、`FUNMX64`(2)、`FUNNKR`(2)、`FUNNKRX64`(2)、`FUNMKR`(10)、`FUNMKRX64`(10) → **KR/防流氓线专属**（正式线 `FUNN` 不引用） |
| 主程序内嵌 **OEM 素材包** | `Scoem/<品牌>/…`（223 个成员：Acer/Alienware/Apple/Asus/BenQ/Compaq/Dell/Founder/Fujitsu/GreatWall/Haier/Hasee/Hedy/Hisense/HP/HUAWEI/IBM/Lenovo/Microsoft/MSI/NEC/Samsung/Sony/Sysceo/TCL/Terrans Force/Thtf/Timi/Toshiba/Tsunis/VmWare + `readme.txt`），`nt5.*`/`nt6.*` 双套 |

## 七、脱壳产物与复现方法

| 产物 | 说明 | 校验 |
|---|---|---|
| `work/engines/FUNQ.unpacked.exe` | FUNQ（Scaddnet）完整脱壳：ASPack 2.42，7/7 块 + 壳区尾部资源，11 节区有效，61/61 资源 IN，OEP `0x2a8b2c` | sha256 `934e96634259a767ddb700a81cf33beca94be3395758609c102e417d7d2885d3` |
| `scpt-analysis/01-unpacked/Scpt.unpacked.exe` | 主程序完整脱壳（本轮用修复后的重建逻辑重生成，节表有效，205 资源） | sha256 `34d33227de1367790086a36dd4e40747de59ebcae829dd165d6104519fb35b70` |

复现脚本（`tools/scpt/`；本机原始副本在 `work/analysis/`，只做纯数据解压、不执行样本）：
- `unpack.py` — ASPack 解压核心（含块表驱动的 in-place 解压 + PE 重建）
- `funq_finish.py` — FUNQ 收尾（壳区尾部资源保留 + `.rsrc` 真实范围修正）
- `finish.py` / `full10.py` — 主程序收尾（壳区资源补丁 + 资源导出）
- `dossier.py` — **全模块 dossier 生成**：版本信息/架构/导入/资源/双编码字符串/关键词命中 → `dossier.json` + `module-dossiers.md`
- `compare_funn_family.py` — 四变体（`FUNN`/`FUNNX64`/`FUNNKR`/`FUNNKRX64`）字符串矩阵与差集
- `funnkr_diff.py` — `FUNN` vs `FUNNKR` 行为差异核验（任务标记/窗体/驱动服务/篡改路径）
- `full_inventory.py`、`feature_map.py`、`strings_detail.py`、`deep_scan_unknown.py` — 盘点与检索

分析产物（原始证据，`work/analysis/`）：

| 产物 | 说明 |
|---|---|
| `dossier.json` / `module-dossiers.md` | 44 个文件逐个 dossier（本仓库 `docs/analysis/module-dossiers.md` 为同一份） |
| `full_inventory.md` / `full_inventory.json` | 46 个文件盘点（含 3 个内嵌组件与脱壳副本） |
| `funn_family_compare.log` / `funnkr_diff.log` | 变体差集原始输出 |
| `work/pubce/` | `PUBCE` 解包产物（245 文件，Inno Setup 5.6.0） |
| `work/engines/` 与 `work/engines-orig-unp/` | 脱壳模块 / 从原包独立重脱壳的校验副本 |
