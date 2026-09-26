//! GUI 骨架（egui/eframe）——页面结构对齐原工具的信息架构。
//! ponytail: 先做导航 + 页面占位 + 状态栏；功能对接在 M3，不写假控件（仅禁用占位按钮）。

use eframe::egui;

/// 页面：名称 + 说明；顺序 = 左侧导航顺序（对齐原工具主要分区）。
pub const PAGES: &[(&str, &str)] = &[
    ("封装", "封装体检、封装方式与封装后处理"),
    ("部署设置", "部署模块外观与部署选项"),
    ("任务计划", "部署前 / 部署中 / 部署后任务清单"),
    ("驱动", "磁盘控制器驱动（SRS）导入"),
    ("系统优化", "明确声明的优化项（白名单校验）"),
    ("关于", "版本、文档与验收清单"),
];

#[derive(Default)]
pub struct App {
    page: usize,
    /// 封装页体检报告（None = 尚未体检）。
    doctor_report: Option<crate::doctor::Report>,
}

impl eframe::App for App {
    fn update(&mut self, ctx: &egui::Context, _frame: &mut eframe::Frame) {
        egui::SidePanel::left("nav")
            .resizable(false)
            .default_width(168.0)
            .show(ctx, |ui| {
                ui.add_space(8.0);
                ui.heading("OpenSysprep");
                ui.label(format!("v{}", env!("CARGO_PKG_VERSION")));
                ui.separator();
                for (i, (name, _)) in PAGES.iter().enumerate() {
                    if ui.selectable_label(self.page == i, *name).clicked() {
                        self.page = i;
                    }
                }
            });
        egui::TopBottomPanel::bottom("status").show(ctx, |ui| {
            ui.horizontal(|ui| {
                ui.label(format!(
                    "OpenSysprep {} · {}",
                    env!("CARGO_PKG_VERSION"),
                    std::env::consts::OS
                ));
                ui.with_layout(egui::Layout::right_to_left(egui::Align::Center), |ui| {
                    ui.label("就绪");
                });
            });
        });
        egui::CentralPanel::default().show(ctx, |ui| {
            let (name, desc) = PAGES[self.page];
            ui.add_space(4.0);
            ui.heading(name);
            ui.label(desc);
            ui.separator();
            if self.page == 0 {
                ui.horizontal(|ui| {
                    if ui.button("封装体检").clicked() {
                        // ponytail: 同步执行（只读、秒回）；卡顿再上线程。
                        self.doctor_report = Some(crate::doctor::run(std::path::Path::new(".")));
                    }
                    // ponytail: 开始封装 = M4（依赖 install/once 全链路），占位禁用。
                    let _ = ui.add_enabled(false, egui::Button::new("开始封装"));
                });
                ui.add_space(4.0);
                if let Some(report) = &self.doctor_report {
                    ui.separator();
                    for item in &report.items {
                        let mark = if item.ok { "✓" } else { "✗" };
                        if item.ok {
                            ui.label(format!("{mark} {}", item.name));
                        } else {
                            ui.label(format!("{mark} {} — {}", item.name, item.detail));
                        }
                    }
                    let verdict = if report.passed() {
                        "体检通过"
                    } else {
                        "存在未通过项"
                    };
                    ui.separator();
                    ui.strong(format!("结论: {verdict}"));
                }
            }
            ui.label("功能对接进行中（M3）：见 docs/spec/capabilities.md。");
        });
    }
}

/// 加载系统中文字体；找不到时回退默认字体（中文可能显示为方块）。
fn setup_fonts(ctx: &egui::Context) {
    // ponytail: 只读系统字体、不打包字体文件；需要离线分发时再内置子集。
    const CANDIDATES: &[&str] = &[
        r"C:\Windows\Fonts\msyh.ttc",
        r"C:\Windows\Fonts\simhei.ttf",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf",
        "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
    ];
    for path in CANDIDATES {
        if let Ok(bytes) = std::fs::read(path) {
            let mut fonts = egui::FontDefinitions::default();
            fonts
                .font_data
                .insert("cjk".to_owned(), egui::FontData::from_owned(bytes).into());
            if let Some(list) = fonts.families.get_mut(&egui::FontFamily::Proportional) {
                list.insert(0, "cjk".to_owned());
            }
            if let Some(list) = fonts.families.get_mut(&egui::FontFamily::Monospace) {
                list.push("cjk".to_owned());
            }
            ctx.set_fonts(fonts);
            return;
        }
    }
}

/// 供 CLI（无参 / `gui` 子命令）调用。
pub fn run() -> eframe::Result<()> {
    let options = eframe::NativeOptions {
        viewport: egui::ViewportBuilder::default()
            .with_title("OpenSysprep")
            .with_inner_size([920.0, 600.0]),
        ..Default::default()
    };
    eframe::run_native(
        "OpenSysprep",
        options,
        Box::new(|cc| {
            setup_fonts(&cc.egui_ctx);
            Ok(Box::new(App::default()))
        }),
    )
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn pages_are_nonempty_and_unique() {
        let mut names: Vec<&str> = PAGES.iter().map(|p| p.0).collect();
        assert!(names.iter().all(|n| !n.is_empty()));
        names.sort_unstable();
        let before = names.len();
        names.dedup();
        assert_eq!(before, names.len(), "页面名重复");
    }
}
