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
- 待做：TOML 配置文件解析（读 `opensysprep.toml`）、任务执行器、GUI 对接（体检/任务页接真数据）
- 证据：提交 `1eeac90`；CI 运行中 → https://github.com/misakano7545/OpenSysprep/actions/runs/36250982179
