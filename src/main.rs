//! OpenSysprep —— 系统封装/部署工具（由「系统总裁封装工具」反编译成果洁净重写）。
//!
//! 无参数启动 = GUI（对齐原工具体验）；功能子命令按 docs/spec/ 逐个对接。

mod gui;

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
