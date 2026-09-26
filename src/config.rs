//! 配置（TOML 明文，人类可读可审）。M3：先定结构与校验，写文件/对接 GUI 后续里程碑。

use std::fmt;

/// 部署任务类型（对齐原工具"部署前/部署中/部署后"任务计划的洁净子集）。
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Phase {
    Pre,
    Mid,
    Post,
}

impl Phase {
    pub fn from_str(s: &str) -> Option<Self> {
        match s {
            "pre" | "deploy_pre" | "部署前" => Some(Phase::Pre),
            "mid" | "deploy_mid" | "部署中" => Some(Phase::Mid),
            "post" | "deploy_post" | "部署后" => Some(Phase::Post),
            _ => None,
        }
    }
    pub fn label(&self) -> &'static str {
        match self {
            Phase::Pre => "部署前",
            Phase::Mid => "部署中",
            Phase::Post => "部署后",
        }
    }
}

/// 一条部署任务：显式命令 + 阶段。不提供任何"隐式行为"。
#[derive(Debug, Clone)]
pub struct Task {
    pub name: String,
    pub phase: Phase,
    /// 要执行的命令行（用户显式声明；执行时逐条白名单校验）。
    pub command: String,
}

/// 校验错误（带字段定位）。
#[derive(Debug)]
pub struct ConfigError(pub String);

impl fmt::Display for ConfigError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}", self.0)
    }
}

/// 任务白名单：只允许调用已声明的外部程序名（不含路径、不带参数）。
/// ponytail: 白名单内置于配置而非代码硬编码——审计时一目了然；需要加程序就加配置。
pub struct TaskPolicy {
    pub allowed_programs: Vec<String>,
}

impl TaskPolicy {
    /// 校验任务命令的"程序名"是否在白名单。
    /// 规则：取命令行第一个空白前的一段，按文件名（去路径）比较。
    pub fn validate(&self, task: &Task) -> Result<(), ConfigError> {
        let head = task.command.split_whitespace().next().unwrap_or("");
        if head.is_empty() {
            return Err(ConfigError(format!("任务 {} 的命令为空", task.name)));
        }
        let prog = filename(head);
        if self
            .allowed_programs
            .iter()
            .any(|p| p.eq_ignore_ascii_case(&prog))
        {
            Ok(())
        } else {
            Err(ConfigError(format!(
                "任务 {} 调用的程序「{}」不在白名单（见 TaskPolicy.allowed_programs）",
                task.name, prog
            )))
        }
    }
}

fn filename(s: &str) -> String {
    // ponytail: 手写文件名提取，避免为这一行引入路径解析差异。
    s.rsplit(['\\', '/']).next().unwrap_or(s).to_string()
}

#[cfg(test)]
mod tests {
    use super::*;

    fn policy() -> TaskPolicy {
        TaskPolicy {
            allowed_programs: vec!["pnputil.exe".into(), "reg.exe".into()],
        }
    }

    #[test]
    fn phase_parses_and_labels() {
        assert_eq!(Phase::from_str("pre"), Some(Phase::Pre));
        assert_eq!(Phase::from_str("部署后"), Some(Phase::Post));
        assert_eq!(Phase::from_str("bogus"), None);
        assert_eq!(Phase::Mid.label(), "部署中");
    }

    #[test]
    fn policy_allows_whitelisted_program() {
        let t = Task {
            name: "装驱动".into(),
            phase: Phase::Post,
            command: "C:\\Windows\\pnputil.exe /add-driver x.inf".into(),
        };
        assert!(policy().validate(&t).is_ok());
    }

    #[test]
    fn policy_rejects_unknown_program_and_empty() {
        let p = policy();
        let bad = Task {
            name: "x".into(),
            phase: Phase::Pre,
            command: "format.com C:".into(),
        };
        assert!(p.validate(&bad).is_err());
        let empty = Task {
            name: "y".into(),
            phase: Phase::Pre,
            command: "   ".into(),
        };
        assert!(p.validate(&empty).is_err());
    }

    #[test]
    fn browser_paths_are_never_whitelisted_by_default() {
        // 红线回归：默认白名单策略对象（空）拒绝一切；浏览器可执行名不在内置样例白名单。
        let empty = TaskPolicy {
            allowed_programs: vec![],
        };
        let t = Task {
            name: "z".into(),
            phase: Phase::Post,
            command: "chrome.exe --hijack".into(),
        };
        assert!(empty.validate(&t).is_err());
    }
}
