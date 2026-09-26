//! OpenSysprep —— 系统封装/部署工具（由「系统总裁封装工具」逆向分析后的洁净重构）。
//!
//! ponytail: 只留 version/help 保证「构建 → 运行 → CI」闭环；
//! 功能子命令按路线图逐个加，每个都带测试。

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
        Some("help" | "--help" | "-h") | None => {
            usage();
            ExitCode::SUCCESS
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
