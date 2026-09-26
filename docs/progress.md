# 进度记录

> 里程碑驱动；日期为北京时间（CST）。证据 = 命令输出 / 提交 / CI 链接。

## M0 项目基建（完成）

- 产出：Rust 骨架（version/help + 自检）、CI 双平台（Linux 自检 / Windows 构建+运行+artifact）、AGENTS.md、GOAL 提示词、素材归档 `work/`
- 证据：提交 `5389f74`；CI 全绿 → https://github.com/misakano7545/OpenSysprep/actions/runs/36245980008
- 本地：`cargo test` 1 用例通过；`python3 -m unittest discover -s tools -v` 3 用例通过；`./target/release/opensysprep version` 正常

## M1 规格提炼（完成）

- 产出：`docs/spec/capabilities.md`（能力清单）、`docs/spec/behavior-matrix.md`（行为对照表）；更新 `docs/verify-windows.md`（新路线验收清单）；CI 增加「红线静态审计」步骤
- 证据：本地测试通过（cargo + python）；提交见 git log（M1 提交）
- 阻塞：无

## M2 架构与骨架（进行中）

- 计划：按规格定义子命令与模块边界（install / once / doctor / uninstall）、TOML 配置规范、日志规范、白名单校验
- 产出目标：可运行的 CLI 结构 + 配置解析自检

## 待决策（暂停项）

- 许可证选择（属公开发布决策；未定前不添加 LICENSE 文件）
