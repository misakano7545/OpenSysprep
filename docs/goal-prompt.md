# GOAL 提示词（Hermes `/goal`）

> 用途：让 Hermes 以常驻目标（standing goal）自驱完成「一步到位重构」。
> 用法：将下面 text 代码块**整段（保留换行）**粘贴给 `/goal`；`verify:` / `constraints:` / `boundaries:` / `stop when:` 四个字段行会自动成为「完成契约」。也可改用 `/goal draft` 让 Hermes 先起草契约再设置。
> 运行环境：仓库 `/root/dev/OpenSysprep`（本机）。

```text
把「系统总裁封装工具」的反编译成果一步到位重构为开源项目 OpenSysprep：用 Rust 洁净重写其核心封装/部署能力——原工具只作功能与行为规格蓝本，全部浏览器篡改与推广行为一律剔除；不走二进制补丁过渡，直接重构。按四个里程碑推进：M1 规格提炼（docs/spec/ 能力清单 + 行为对照表）→ M2 架构与骨架 → M3 核心功能实现与测试 → M4 Windows VM 验收与 v0.1 构建。全程自驱并自我进化：先查证（官方文档/资料）再动手；每个里程碑把可复用流程用 skill_manage 沉淀为 Hermes 技能、把踩坑与结论写进 docs/lessons.md、进度写进 docs/progress.md 并同步更新 AGENTS.md；定期回看并修正计划，不发散、不空等、不自造范围。
verify: 里程碑证据链齐全：cargo test 与 python3 -m unittest discover -s tools -v 通过；推送到 origin/main 后 GitHub Actions（test + windows 两个 job）全绿，Windows job 实际运行 opensysprep.exe 并产出 artifact；仓库含 docs/spec/（能力与行为对照表）、docs/verify-windows.md（验收清单）、docs/progress.md（进度记录）；v0.1 构建产物可运行并附演示说明。
constraints: 仓库不得包含任何原厂二进制或闭源代码；实现中不得出现主页/搜索引擎/新标签页/推广/静默安装类功能与代码路径；运行级验证只在 Windows 虚拟机按文档执行；文档与提交用中文、不含个人信息；CI 始终保持绿色；新增依赖取最小并说明理由。
boundaries: 主战场 /root/dev/OpenSysprep（含 work/ 本机素材）；只读参考 /root/dev/scpt-analysis；远端 git@github.com:misakano7545/OpenSysprep.git（允许推送 main 以触发 CI；推送失败则记录阻塞并继续本地主线，不另建仓库）。
stop when: 需要凭据、资金、许可证或公开发布决策时；需要不可逆/破坏性操作时；规格与事实冲突无法自决时。停止前先说明现状与可选路径。
```

## 质量门（建议添加）

```bash
/goal gate add "cd /root/dev/OpenSysprep && cargo test && python3 -m unittest discover -s tools -v"
```

## 补充判据（随时追加，不打断循环）

```bash
/subgoal 每个里程碑结束时：更新 Studio 任务卡与 docs/progress.md，沉淀该阶段技能，并列出下一阶段 3 条以内的下一步
/subgoal 任何"完成/已修好"的结论都必须附可复现证据（命令输出、文件路径、CI 链接）
```

## 行为说明（Hermes 侧）

- 每轮结束后由判官模型判定 done / continue / blocked / wait；预算默认约 20 轮。
- 预算用尽或暂停后：`/goal resume` 继续（计数清零）；`/goal status` 查看状态；`/goal show` 查看契约。
- 推送后盯 CI：Agent 用后台进程监视时，判官会自动进入 wait（不消耗轮次、不空转），CI 结束后自动续跑。
- 自我学习/进化机制已写入目标文本（技能沉淀 + lessons/progress/AGENTS 更新 + 定期修正计划）。
