# SCPT 全量解析：模块 → 功能 → 原实现 → Rust 还原方案

> 证据来源：主程序脱壳镜像（`01-unpacked/Scpt.unpacked.exe`）、45 个模块（`work/engines/`）、205 个资源、语言文件 567 条文案（其中 411 条界面控件）。
> 自动扫描原始输出：`work/analysis/full_inventory.md`、`feature_matrix.md`、`main_flow.txt`、`strings_detail.md`、`unknown_modules.md`、`ui_controls.txt`。
> 目标：**功能 1:1 还原，零流氓**（不实现任何浏览器篡改、推广安装、内核锁）。

---

## 一、总览：SCPT 是什么、怎么工作

**三层结构**（所有模块都能归到这三层）：

| 层 | 组成 | 职责 |
|---|---|---|
| ① 主程序 | `Scpt.exe`（Delphi + ASPack） | 界面 + 封装流程编排（60 个流程标记）+ 资源仓库（45 个模块、语言、皮肤、测试数据） |
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

## 四、45 个模块映射表

| 模块 | 身份（证据） | 对应功能 | Rust 方案 |
|---|---|---|---|
| `FUNA` | IDE/HDC 控制器 INF（Win2000 5.1.2600） | SRS/磁盘控制器驱动 | 保留功能，不捆绑 INF |
| `FUNI` | HAL/CA 相关 INF | SRS/硬件抽象层 | 同上 |
| `FUNB` | devcon 改造版（UpdateDriverForPlugAndPlayDevicesW） | 驱动安装 | 用 `pnputil` 替代 |
| `FUNC` | devcon 改造版（含 devcon.pdb，x64） | 驱动安装 | 同上 |
| `FUND` | 网络设置（NetSetupPrepareSysPrep/netshell/SetupOobeBnk，伪装"sysprep utility"） | 网络位置设置 | 用 `netsh`/`PowerShell` 实现 |
| `FUNF`/`FUNFX64` | 同 FUND | 网络位置设置 | 同上 |
| `FUNE`/`FUNG`/`FUNGX64` | SetupCL（sysprep 的 SetupComplete 执行器，SYSTEM hive 操作） | 首启脚本执行 | 用系统自带 setupcomplete.cmd 机制 |
| `FUNH` | NTLDR（NT 引导加载器） | 引导修复 | 剔换系统文件；需要时用 `bcdboot` |
| `FUNJ` | SetACL（Helge Klein） | 文件/注册表权限 | 用 `icacls`/`reg` 替代 |
| `FUNK` | 7-Zip（Igor Pavlov，13MB） | 驱动包/资源包解压 | 用系统 `tar`（Win10+ 内置）替代 |
| `FUNM`/`FUNMKR`/`FUNMX64`/`FUNMKRX64` | ForensiT DefProf 魔改（NTUSER.DAT/SCRUNTEMP ×111） | 默认用户配置移植（首次进桌面项） | 保留功能，白名单显式项 |
| `FUNN`/`FUNNX64` | ScTasks 部署引擎（浏览器篡改 ×86） | 部署任务执行 | 重写（剔篡改） |
| `FUNNKR`/`FUNNKRX64` | 同引擎改名版（伪装 NT Kernel & System；无篡改标识命中） | 部署执行（另一种封装方式） | 待运行验证；Rust 只做单一洁净引擎 |
| `FUNO`/`FUNOX64` | 部署辅助（OEM×51/部署×38/任务栏×19） | 部署时 OEM/任务栏 | 并入 once 任务项 |
| `FUNP`/`FUNR`/`FUNS`/`FUNX`/`PUBCA`/`PUBCF` | 进度界面模块（进度界面×372–437） | 部署进度皮肤 | 轻量进度输出（不做像素还原） |
| `FUNT`/`FUNU`/`FUNY`/`PUBCG` | 小程序（OEM/任务栏） | 辅助 | 并入 once 任务项 |
| `FUNZ` | 界面模块（进度界面×68） | 部署界面 | 同上 |
| `FUNQ` | **`Scaddnet`**（Sysceo.com，v3.0.0.0；ASPack 2.42 **已完整脱壳**，见下）——网络助手：`[ADSL]`/`[宽带连接]` 配置、`.lnk` 快捷方式、`TSccnet` 网络设置窗体、uMlSkin 皮肤 | 宽带/ADSL 拨号连接、IP 设置、网络位置、任务栏固定 | 用 `netsh`/`rasdial`/PowerShell 实现；已核**零浏览器相关代码** |
| `FUNV` | OEM 素材 ZIP（`Scoem/<品牌>/`，OEM×878） | OEM 智能识别素材 | 保留功能，素材由用户提供 |
| `FUNA_embed`/`FUNC_embed` | FUNN 内嵌组件（UPX） | 部署链子模块 | 重写 |
| `FUNB_embed` | FUNN 内嵌 DLL（setedge + OpenSSL 加密） | **浏览器篡改 + HMAC 伪造** | **剔除** |
| `PUBCB`/`PUBCC`/`PUBCD` | **内核驱动 scdrv/Scufd.sys**（x86/x64/NT5） | 脚本锁/防删除 | **剔除** |
| `PUBCE` | Inno Setup 安装包（19MB） | 第三方组件安装 | **剔除**（按需用户自装） |
| `PUBCH`/`PUBCI` | 小型 native（PUBCI 含 AUTHZ/SAM/DSROLE → 权限/账户） | 权限/账户处理 | 用系统工具替代 |

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

## 六、待核项

- `FUNNKR` 与 `FUNN` 的行为差异（是否仅改名）；
- `PUBCE` 安装包的具体内容（第三方组件清单）；
- `PUBCH`/`PUBCI` 的具体用途（权限/账户相关）。

## 七、脱壳产物与复现方法

| 产物 | 说明 | 校验 |
|---|---|---|
| `work/engines/FUNQ.unpacked.exe` | FUNQ（Scaddnet）完整脱壳：ASPack 2.42，7/7 块 + 壳区尾部资源，11 节区有效，61/61 资源 IN，OEP `0x2a8b2c` | sha256 `934e96634259a767ddb700a81cf33beca94be3395758609c102e417d7d2885d3` |
| `scpt-analysis/01-unpacked/Scpt.unpacked.exe` | 主程序完整脱壳（本轮用修复后的重建逻辑重生成，节表有效，205 资源） | sha256 `34d33227de1367790086a36dd4e40747de59ebcae829dd165d6104519fb35b70` |

复现脚本（`tools/scpt/`；本机原始副本在 `work/analysis/`，只做纯数据解压、不执行样本）：
- `unpack.py` — ASPack 解压核心（含块表驱动的 in-place 解压 + PE 重建）
- `funq_finish.py` — FUNQ 收尾（本次新增：壳区尾部资源保留 + `.rsrc` 真实范围修正）
- `finish.py` — 主程序收尾（壳区资源补丁 + 资源导出）
