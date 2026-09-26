//! 任务执行器：按阶段执行白名单内的任务。只执行配置显式声明的命令，无任何隐式行为。

use crate::config::{Phase, Task, TaskPolicy};
use std::process::Command;

/// 执行结果（供 CLI 输出与测试断言）。
pub struct RunOutcome {
    pub name: String,
    pub phase: Phase,
    pub success: bool,
    pub detail: String,
}

/// 执行给定阶段的全部任务（执行前逐条再过一次白名单——防配置被外部改动）。
pub fn run_phase(tasks: &[Task], policy: &TaskPolicy, phase: Phase) -> Vec<RunOutcome> {
    tasks
        .iter()
        .filter(|t| t.phase == phase)
        .map(|t| {
            // 红线：执行前二次校验；失败即拒绝执行该任务（不静默跳过）。
            if let Err(e) = policy.validate(t) {
                return RunOutcome {
                    name: t.name.clone(),
                    phase: t.phase,
                    success: false,
                    detail: format!("拒绝执行: {e}"),
                };
            }
            match execute(t) {
                Ok(out) => RunOutcome {
                    name: t.name.clone(),
                    phase: t.phase,
                    success: true,
                    detail: out,
                },
                Err(e) => RunOutcome {
                    name: t.name.clone(),
                    phase: t.phase,
                    success: false,
                    detail: e,
                },
            }
        })
        .collect()
}

/// 拆分命令行并执行。ponytail: 按空白拆分够用（配置是我们自己审过的白名单命令）；
/// 需要引号嵌套时升级为 shell 解析。
fn execute(task: &Task) -> Result<String, String> {
    let mut parts = task.command.split_whitespace();
    let prog = parts.next().ok_or("命令为空")?;
    let args: Vec<&str> = parts.collect();
    let output = Command::new(prog)
        .args(&args)
        .output()
        .map_err(|e| format!("启动失败: {e}"))?;
    let stdout = String::from_utf8_lossy(&output.stdout).trim().to_string();
    let stderr = String::from_utf8_lossy(&output.stderr).trim().to_string();
    if output.status.success() {
        Ok(if stdout.is_empty() {
            "完成".into()
        } else {
            stdout
        })
    } else {
        Err(if stderr.is_empty() {
            format!("退出码 {:?}", output.status.code())
        } else {
            stderr
        })
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn policy() -> TaskPolicy {
        TaskPolicy {
            // ponytail: 测试用系统无关命令：Windows 用 cmd，Unix 用 echo。
            allowed_programs: if cfg!(windows) {
                vec!["cmd.exe".into()]
            } else {
                vec!["echo".into(), "false".into()]
            },
        }
    }

    fn task(cmd: &str) -> Task {
        Task {
            name: "t".into(),
            phase: Phase::Pre,
            command: cmd.into(),
        }
    }

    #[test]
    fn runs_whitelisted_and_reports_success() {
        let cmd = if cfg!(windows) {
            "cmd.exe /c echo hello"
        } else {
            "echo hello"
        };
        let tasks = vec![task(cmd)];
        let out = run_phase(&tasks, &policy(), Phase::Pre);
        assert_eq!(out.len(), 1);
        assert!(out[0].success, "detail: {}", out[0].detail);
        assert!(out[0].detail.contains("hello"));
    }

    #[test]
    fn non_whitelisted_task_is_refused() {
        let tasks = vec![task("definitely_not_allowed.exe --x")];
        let out = run_phase(&tasks, &policy(), Phase::Pre);
        assert!(!out[0].success);
        assert!(
            out[0].detail.contains("拒绝执行"),
            "detail: {}",
            out[0].detail
        );
    }

    #[test]
    fn failing_command_is_reported_not_hidden() {
        let cmd = if cfg!(windows) {
            "cmd.exe /c exit /b 3"
        } else {
            "false"
        };
        let tasks = vec![task(cmd)];
        let out = run_phase(&tasks, &policy(), Phase::Pre);
        assert!(!out[0].success);
    }

    #[test]
    fn only_matching_phase_runs() {
        let cmd = if cfg!(windows) {
            "cmd.exe /c echo hi"
        } else {
            "echo hi"
        };
        let tasks = vec![Task {
            name: "post-only".into(),
            phase: Phase::Post,
            command: cmd.into(),
        }];
        assert!(run_phase(&tasks, &policy(), Phase::Pre).is_empty());
    }
}
