# AGENTS.md

> 面向在本仓库工作的 AI Agent（及人类协作者）。动手前先读本文件。

## 项目

OpenSysprep — 从「系统总裁封装工具（Scpt 3.0.0.178）」的逆向分析出发：**一步到位重构** —— 以原工具为功能与行为规格蓝本，用 Rust 洁净重写为独立、可公开审计的系统封装/部署工具。不走二进制补丁/过渡版本路线。

## 里程碑与现状

- M0 项目基建：✅ 完成（Rust 骨架、CI 双平台、素材归档）
- M1 规格提炼：✅ 完成 —— `docs/spec/capabilities.md`、`docs/spec/behavior-matrix.md`
- M2 架构与骨架：进行中 —— 子命令与模块边界、配置规范、日志规范
- M3 核心功能实现与测试：待开始
- M4 Windows VM 验收与 v0.1 构建：待开始

推进方式：由 Hermes 常驻目标（`/goal`）驱动，提示词见 `docs/goal-prompt.md`。进度：`docs/progress.md`；经验：`docs/lessons.md`。

## 目录

- `src/` — Rust 源码（主程序；`cargo test` 随包自检）
- `tools/` — 逆向与分析工具（Python ≥3.11；优先标准库；`python3 -m unittest discover -s tools -v`）
- `scripts/` — Windows 侧脚本（PowerShell）
- `docs/` — 规格（`docs/spec/`）、验证清单（`docs/verify-windows.md`）、进度与经验、GOAL 提示词
- `dist/` — 构建产物，**不入库**
- `work/` — 本机分析工作区（素材、日志、脚本），**不入库**

## 硬性规则

- 仓库不包含任何原厂二进制或闭源代码；实现中不得出现主页/搜索引擎/新标签页/推广/静默安装类功能（红线详见 `docs/spec/behavior-matrix.md`，CI 有静态审计）。
- 每个改动带可运行自检（`#[test]` 或 `test_*.py`）；证据（命令输出、文件路径、CI 链接）随结论给出。
- 运行级验证只允许在 Windows 虚拟机中进行；静态验证在 CI。
- CI 必须保持绿色：Linux 跑 clippy/测试/跨目标检查/红线审计；Windows runner 构建并**实际运行**产物。红了先修 CI。
- 每个里程碑结束时：更新 `docs/progress.md` 与 `docs/lessons.md`、用 skill_manage 沉淀可复用流程、回看修正计划。
- 文档、提交信息用中文；不写个人信息（姓名/单位/联系方式）。
- 提交：中文短句，一次提交一件事。

## 常用命令

- `cargo test` / `cargo clippy --all-targets -- -D warnings`
- 跨目标检查（Linux 上验 Windows 代码）：`rustup target add x86_64-pc-windows-msvc && cargo check --target x86_64-pc-windows-msvc`
- Python 自检：`python3 -m unittest discover -s tools -v`

## 背景速览（避免重复劳动）

- 原工具：Delphi + ASPack 主程序；部署引擎 UPX 加壳；全栈 Delphi。
- 原工具篡改链（仅供行为对照，不作实现依赖）：主程序封装时写入部署组件（`ScTasks.exe` / `ScDeploy.exe` / `Scdata.sc`）→ 目标机首次部署时执行 → 改 IE 主页、Edge/Chrome `Secure Preferences`（伪造 HMAC 签名，配合 `prefs_enclave_x64.dll`）、默认搜索与新标签页（`https://newtabx.com/`）。
- 相关模块：`FUNN` / `FUNNX64` / `FUNNKR` / `FUNNKRX64`（部署引擎）、`FUNM*`（魔改 ForensiT DefProf）、`FUNN` 内嵌 `FUNB`（"setedge" 浏览器配置组件）。
- 详细偏移与证据见只读参考 `/root/dev/scpt-analysis`。

## 协作约定

- 修改 `src/` 或 `tools/` 逻辑必须留下可运行自检。
- 先查证（官方文档/资料）再动手；不确定的行为先静态分析；禁止在真机运行原工具，验证只在 VM 快照里做。
