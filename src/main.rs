//! OpenSysprep —— 系统封装/部署工具（由「系统总裁封装工具」反编译成果洁净重写）。
//!
//! 无参数启动 = GUI（对齐原工具体验）；功能子命令按 docs/spec/ 逐个对接。

mod config;
mod doctor;
mod gui;
mod runner;

use std::env;
use std::process::ExitCode;

const VERSION: &str = env!("CARGO_PKG_VERSION");

fn version_line() -> String {
    format!(
        "OpenSysprep {} ({}/{})",
        VERSION,
        env::consts::OS,
        env::consts::ARCH
    )
}

fn usage() {
    println!(
        r#"OpenSysprep —— 系统封装/部署工具

用法:
  opensysprep            启动图形界面
  opensysprep gui        同上
  opensysprep doctor     封装体检（只读）
  opensysprep run <pre|mid|post> [配置文件]
                         执行指定阶段的部署任务（默认读取 ./opensysprep.toml）
  opensysprep version    显示版本
  opensysprep help       显示帮助"#
    );
}

fn main() -> ExitCode {
    match env::args().nth(1).as_deref() {
        Some("version" | "--version" | "-v") => {
            println!("{}", version_line());
            ExitCode::SUCCESS
        }
        Some("help" | "--help" | "-h") => {
            usage();
            ExitCode::SUCCESS
        }
        Some("gui" | "--gui") | None => match gui::run() {
            Ok(()) => ExitCode::SUCCESS,
            Err(e) => {
                eprintln!("GUI 启动失败: {e}");
                eprintln!("（无图形环境时请使用 CLI：opensysprep help）");
                ExitCode::from(1)
            }
        },
        Some("doctor") => {
            let report = doctor::run(std::path::Path::new("."));
            print!("{report}");
            if report.passed() {
                ExitCode::SUCCESS
            } else {
                ExitCode::from(1)
            }
        }
        Some("run") => {
            let args: Vec<String> = env::args().skip(2).collect();
            let Some(phase_str) = args.first() else {
                eprintln!("用法: opensysprep run <pre|mid|post> [配置文件]");
                return ExitCode::from(2);
            };
            let Some(phase) = config::Phase::from_str(phase_str) else {
                eprintln!("阶段不合法: {phase_str}（pre/mid/post）");
                return ExitCode::from(2);
            };
            let path = args
                .get(1)
                .cloned()
                .unwrap_or_else(|| "opensysprep.toml".to_string());
            let text = match std::fs::read_to_string(&path) {
                Ok(t) => t,
                Err(e) => {
                    eprintln!("读取配置失败 {path}: {e}");
                    return ExitCode::from(1);
                }
            };
            let (_cfg, policy, tasks) = match config::FileConfig::parse(&text) {
                Ok(v) => v,
                Err(e) => {
                    eprintln!("{e}");
                    return ExitCode::from(1);
                }
            };
            println!(
                "执行阶段: {}（任务 {} 项）",
                phase.label(),
                tasks.iter().filter(|t| t.phase == phase).count()
            );
            let results = runner::run_phase(&tasks, &policy, phase);
            let mut failed = 0;
            for r in &results {
                if r.success {
                    println!("[成功] ({}) {}", r.phase.label(), r.name);
                } else {
                    failed += 1;
                    println!("[失败] ({}) {} — {}", r.phase.label(), r.name, r.detail);
                }
            }
            if results.is_empty() {
                println!("该阶段无任务。");
            }
            if failed == 0 {
                ExitCode::SUCCESS
            } else {
                ExitCode::from(1)
            }
        }
        Some(other) => {
            eprintln!("未知命令: {other}");
            eprintln!();
            usage();
            ExitCode::from(2)
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn version_line_ok() {
        let line = version_line();
        assert!(line.contains("OpenSysprep"), "缺名称: {line}");
        assert!(line.contains(VERSION), "缺版本: {line}");
    }
}
