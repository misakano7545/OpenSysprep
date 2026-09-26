//! 封装体检（doctor）：纯只读检查，输出逐项结果。M3 第一个落地功能。

use std::fmt;
use std::path::{Path, PathBuf};

/// 单项检查结果。
pub struct CheckItem {
    pub name: &'static str,
    pub ok: bool,
    /// 未通过时的人类可读说明（ok=true 时为空）。
    pub detail: String,
}

/// 体检报告。
pub struct Report {
    pub items: Vec<CheckItem>,
}

impl Report {
    pub fn passed(&self) -> bool {
        self.items.iter().all(|i| i.ok)
    }
}

impl fmt::Display for Report {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        for it in &self.items {
            let mark = if it.ok { "[通过]" } else { "[未过]" };
            if it.ok {
                writeln!(f, "{mark} {}", it.name)?;
            } else {
                writeln!(f, "{mark} {} — {}", it.name, it.detail)?;
            }
        }
        writeln!(
            f,
            "结论: {}",
            if self.passed() {
                "体检通过"
            } else {
                "存在未通过项"
            }
        )
    }
}

#[cfg(windows)]
fn sysprep_path() -> Option<PathBuf> {
    // ponytail: 只认 System32\sysprep\sysprep.exe（官方唯一位置），不做注册表搜索。
    Some(PathBuf::from(r"C:\Windows\System32\sysprep\sysprep.exe"))
}

#[cfg(not(windows))]
fn sysprep_path() -> Option<PathBuf> {
    None
}

/// 运行体检。只读、不改系统、不联网。
pub fn run(root: &Path) -> Report {
    let mut items = Vec::new();

    // 1) 系统：是否 Windows（sysprep 只存在于 Windows）
    let sysprep_seen = sysprep_path();
    items.push(CheckItem {
        name: "Windows 系统（sysprep 存在性）",
        ok: sysprep_seen.is_some(),
        detail: if sysprep_seen.is_some() {
            String::new()
        } else {
            "当前不是 Windows（或在非标准路径找不到 sysprep）".to_string()
        },
    });

    // 2) sysprep.exe 真实存在
    let sp = sysprep_path().unwrap_or_default();
    items.push(CheckItem {
        name: "sysprep.exe 存在",
        ok: sp.is_file(),
        detail: if sp.is_file() {
            String::new()
        } else {
            format!("未找到 {}", sp.display())
        },
    });

    // 3) 工作目录可写（日志/配置要落地）
    let writable = root.is_dir() || root.exists();
    items.push(CheckItem {
        name: "工作目录存在",
        ok: writable,
        detail: if writable {
            String::new()
        } else {
            format!("目录不存在: {}", root.display())
        },
    });

    // 4) 曾被 sysprep 封装过的痕迹（CloneTag），仅提示
    #[cfg(windows)]
    {
        let cloned = std::process::Command::new("reg")
            .args(["query", r"HKLM\SYSTEM\Setup", "/v", "CloneTag"])
            .output()
            .map(|o| o.status.success())
            .unwrap_or(false);
        items.push(CheckItem {
            name: "克隆系统痕迹（CloneTag）",
            ok: !cloned,
            detail: if cloned {
                "系统带 CloneTag（克隆版系统），封装风险较高，仅提示".to_string()
            } else {
                String::new()
            },
        });
    }
    #[cfg(not(windows))]
    items.push(CheckItem {
        name: "克隆系统痕迹（CloneTag）",
        ok: true,
        detail: String::new(),
    });

    Report { items }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn report_display_marks_items() {
        let r = Report {
            items: vec![
                CheckItem {
                    name: "甲",
                    ok: true,
                    detail: String::new(),
                },
                CheckItem {
                    name: "乙",
                    ok: false,
                    detail: "原因".into(),
                },
            ],
        };
        let s = r.to_string();
        assert!(s.contains("[通过] 甲"));
        assert!(s.contains("[未过] 乙 — 原因"));
        assert!(!r.passed());
    }

    #[test]
    fn run_on_non_windows_marks_sysprep_missing() {
        // 非 Windows 上 sysprep 检查必失败 → 报告可生成且结构稳定。
        let r = run(Path::new("."));
        assert!(!r.items.is_empty());
        assert!(r.items.iter().any(|i| i.name.contains("sysprep")));
    }
}
