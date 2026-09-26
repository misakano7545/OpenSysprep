# 进度记录

> 里程碑驱动；日期为北京时间（CST）。证据 = 命令输出 / 提交 / CI 链接。

## M0 项目基建（完成）

- 产出：Rust 骨架（version/help + 自检）、CI 双平台（Linux 自检 / Windows 构建+运行+artifact）、AGENTS.md、GOAL 提示词、素材归档 `work/`
- 证据：提交 `5389f74`；CI 全绿 → https://github.com/misakano7545/OpenSysprep/actions/runs/36245980008
- 本地：`cargo test` 1 用例通过；`python3 -m unittest discover -s tools -v` 3 用例通过；`./target/release/opensysprep version` 正常

## M1 规格提炼（完成）

- 产出：`docs/spec/capabilities.md`（能力清单）、`docs/spec/behavior-matrix.md`（行为对照表）；更新 `docs/verify-windows.md`（新路线验收清单）；CI 增加「红线静态审计」步骤
- 证据：本地测试通过（cargo + python）；提交 `356e8fc`；CI 全绿 → https://github.com/misakano7545/OpenSysprep/actions/runs/36246455570
- 阻塞：无

## M2 架构与骨架（完成）

- GUI 骨架（egui/eframe 0.32）：左侧导航 + 页面占位 + 状态栏；页面结构对齐原工具（封装 / 部署设置 / 任务计划 / 驱动 / 系统优化 / 关于）
- 启动方式：无参数 = GUI（对齐原工具体验）；`gui` 子命令同义
- 新增依赖：`eframe`（GUI；理由：用户需求，且无可更小可行方案）
- 构建策略：本机零编译，全部构建/验证收敛到 GitHub Actions（Linux job 只做 check 级验证，Windows job 编译+测试+运行+artifact）
- 证据：提交 `039f2de`；CI 全绿（test + windows 双 job，Windows 实际运行 opensysprep.exe 并上传 artifact）→ https://github.com/misakano7545/OpenSysprep/actions/runs/36248587190
- 阻塞：无

## 待决策（暂停项）

- 许可证选择（属公开发布决策；未定前不添加 LICENSE 文件）

## M3 核心功能实现与测试（进行中）

- ✅ `doctor`（封装体检，只读）：CLI 子命令 `opensysprep doctor`；检查项含 sysprep.exe 存在性、系统盘、WMI 一致性等（Windows/Linux 各自实现，Linux 输出占位项）
- ✅ 任务模型 + 白名单校验（`src/config.rs`）：`Phase`（部署前/中/后）、`Task`、`TaskPolicy.validate`（程序名白名单）；含红线回归测试（浏览器可执行名永不进默认白名单）
- ✅ TOML 配置装载（`FileConfig::parse`）：解析 `opensysprep.toml` + 全量校验（阶段合法、命令非空、程序名过白名单）；示例 `examples/opensysprep.example.toml`
- ✅ 任务执行器（`src/runner.rs`）+ `run` 子命令：按阶段执行；执行前**二次白名单校验**（防配置被外部改动）；失败任务显式报告不隐藏
- ✅ CI 事故修复：clippy `-D warnings` 拒绝 `RunOutcome.phase` 未读取 → 输出中展示阶段（`1eeac90` 红 → `7279e28` 绿）
- 新增依赖：`serde` + `toml`（TOML 1.0 官方方案；理由：手写解析器风险大于收益）
- 待做：GUI 对接（体检/任务页接真数据）、`install`/`uninstall`（组件自有目录）、`once`（首启执行）
- 证据：CI Run 7 全绿（test + windows 双 job）→ https://github.com/misakano7545/OpenSysprep/actions（commit `7279e28`）

## 解析补全：FUNQ 完整脱壳 + 主程序重生成（完成）

- **FUNQ = `Scaddnet`**（Sysceo.com，v3.0.0.0）：SC 网络助手——宽带/ADSL 拨号连接、IP 设置、网络位置、任务栏快捷方式（资源证据：`[ADSL]`/`[宽带连接]` 配置、`.lnk` 快捷方式、`TSccnet` 网络设置窗体）；已核**零浏览器相关代码**
- 脱壳：ASPack 2.42 完整脱壳（7/7 块 + 壳区尾部资源保留），11 节区有效、61/61 资源 IN、OEP `0x2a8b2c`；产物 `work/engines/FUNQ.unpacked.exe`（sha256 `934e9663…`）
- 附带修复：`unpack.rebuild()` 的 `SizeOfOptionalHeader` 取值 bug（原误取 OptionalHeader Magic，节表偏移错 0x2B）→ 主程序脱壳版重生成：节表有效、205 资源；`scpt-analysis/01-unpacked/Scpt.unpacked.exe`（sha256 `34d33227…`）
- 复现脚本入库：`tools/scpt/`（9 个脚本 + README，纯数据解压，不执行样本）
- 文档：`docs/analysis/module-map.md`（FUNQ 待核项已消除，新增「脱壳产物与复现方法」节）

## 模块解析补全：三项核验 + 42 模块逐个 dossier（完成）

- **逐模块 dossier**：44 个文件（42 模块 + 3 内嵌组件 + 脱壳副本）自动解析版本信息/架构/导入/资源/双编码字符串 → `docs/analysis/module-dossiers.md` + `work/analysis/dossier.json`
- **42 个模块身份全部落地**，其中大量是**伪装**：`FUND/FUNF/FUNFX64` = 微软 `sysprep.EXE` 5.1.2600.1106（XP SP1 原件版本号）、`FUNE/FUNG/FUNGX64` = `SetupCL`、`FUNB/FUNC` = `SETUPAPI.DLL`、`PUBCB/PUBCC/PUBCD` = "Microsoft Time-Stamp Service"、`FUNNKR/FUNNKRX64` = `ntkrnlmp.exe`；而正式版 `FUNN/FUNNX64` 反而**匿名**成 `TOOL`
- **`FUNNKR` vs `FUNN`**：同引擎两条发行线，**不是改名**——KR = mini 驱动 + `ScProtect` 服务 + 冒充内核，**零浏览器篡改**；正式线 = 内嵌 FUNA/FUNB/FUNC 篡改组件 + `Mboxinstall` 推广，**无驱动**；窗体集相同（x86 3 / x64 4），`Sysprep.*`/`Cb_*` 标记都在主程序而非引擎
- **`PUBCE` 清单**：Inno Setup 5.6.0 → 软件魔盒 `AppBox 3.0.0.15` + `AbUpdate`/`AbLauncher`/`uninst` + aria2(nt5/nt6) + 迅雷 5.0.2.289 + 7za 9.20 + `Counter_BD`（245 文件）
- **`PUBCH`/`PUBCI`**：`PUBCI` = 权限编辑/账户解析（AUTHZ/DUI70/DUser/DSPARSE/SAM/DSROLE + ACL 编辑器控件名）；`PUBCH` **未确证**（无导入名/无字符串）；两者资源被**厂商侧**"文本化"损坏（`0x00→0x20`、GBK 非法对→`0x3F`）→ 不可执行、不可复原
- 修 bug：版本信息解析（键名粘着长度字段，必须**后缀匹配**）——`tools/scpt/full_inventory.py` 与 `dossier.py` 同步修正；此前该表恒为空
- 基座可信：原包 20 个 UPX 模块用 `upx -d` 独立重脱壳，与 `work/engines` **sha256 逐一相同**
