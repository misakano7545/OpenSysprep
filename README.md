# OpenSysprep

系统准备（sysprep）场景的开源工具集。

由「系统总裁封装工具（Scpt）」的逆向分析出发：**一步到位重构** —— 以原工具为功能与行为规格蓝本，用 Rust 洁净重写其核心封装/部署能力（不含任何浏览器篡改/推广行为），成为独立、可公开审计的 OpenSysprep。

## 路线图

- [x] 阶段 0：逆向分析与证据归档（脱壳、篡改链定位）
- [x] 阶段 1：规格提炼（[能力清单](docs/spec/capabilities.md)、[行为对照表](docs/spec/behavior-matrix.md)）
- [ ] 阶段 2：Rust 重构（架构骨架 → 核心功能实现与测试）
- [ ] 阶段 3：Windows VM 验收与 v0.1 发布构建
- [ ] 阶段 4：社区审计与迭代

进度记录：[`docs/progress.md`](docs/progress.md) ｜ 经验沉淀：[`docs/lessons.md`](docs/lessons.md)

## 构建 / CI

- GitHub Actions：每次提交自动构建 + 自检；Windows runner 构建 `opensysprep.exe` 并**实际运行**验证，产物作为 artifact 上传
- 本地：
  - `cargo build --release`
  - `cargo test`
  - `python -m unittest discover -s tools -v`

## 自动重构（GOAL）

本项目由 Hermes 常驻目标（`/goal`）驱动推进；提示词与用法见 [`docs/goal-prompt.md`](docs/goal-prompt.md)。

## 结构

- `src/` — Rust 源码（主程序）
- `tools/` — 逆向与补丁工具（Python）
- `scripts/` — Windows 侧检测/清理/验证脚本（PowerShell）
- `docs/` — 分析记录、规格、验证清单、GOAL 提示词
- `dist/` — 构建产物（不入库）

## 说明

- 仅面向自有环境的净化与研究用途；仓库不包含任何原厂二进制。
- 运行级验证在 Windows 虚拟机中进行；静态验证在 CI。
- 协作与 Agent 约定见 `AGENTS.md`。

## 远端

git@github.com:misakano7545/OpenSysprep.git
