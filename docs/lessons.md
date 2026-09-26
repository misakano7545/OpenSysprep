# 经验与踩坑

> 惯例：现象 → 结论/做法；按主题归并，新增条目写进对应主题。只记可复用教训，不记流水账。

## 逆向分析

- ASPack 把整个资源区压成一条流；重建 PE 时**资源目录基准必须取数据目录表里的 RVA**（≠ `.rsrc` 节地址），偏移算错会解析出魔数（如 `#1769554670`）。
- `file` 命令对 UPX 变种识别不可靠：直接 `upx -d` 试解，失败再判定未加壳。
- Delphi 程序字符串 ASCII / UTF-16 混排：检索必须双编码并行，单编码会漏掉一半证据。
- 组件嵌套：`FUNN` 内嵌 `FUNA/FUNB/FUNC` 二级 PE（`FUNB` 即浏览器配置组件所在）；定位证据要按「文件 → 资源 → 内嵌组件」逐层落点。
- 短标识符（如 `we2`）命中随机字节会误报；必须看上下文字符串再下结论。
- ASPack 会把**尾部资源**（图标 / 版本信息 / 清单）以**原样字节**存放在 `.aspack` 段的地址范围内：重建时不能丢弃壳区字节，且 `.rsrc` 的 VirtualSize 必须延伸到 `.adata` 起点，否则资源表里这些条目会指向文件外（`OUT!`）。
- PE 重建时 `SizeOfOptionalHeader` 在 **COFF 头**（`e_lfanew+20`），不是 OptionalHeader 的 Magic 字段；取错会让节表整体偏移 0x2B，产物节表报废（资源仍可按 RVA 直读，但外部工具解析不了）。

## 工程 / CI

- `dtolnay/rust-toolchain@stable` 一次装好 components + targets；Linux 上 `cargo check --target x86_64-pc-windows-msvc` 无需链接即可对 Windows 代码做类型检查——把 Windows 相关代码错误提前到 Linux CI 阶段。
- 把产品红线做成 CI 步骤（禁止标识 grep），约束才真正"可执行"，不然只是文档口号。
- 分析素材及时归档到 `work/`（本机、不入库）；临时目录会被系统清理。

## 协作 / 流程

- 里程碑产出一律"文档 + 可运行证据 + CI 链接"三件套；进度记 `docs/progress.md`、经验记 `docs/lessons.md`、约定同步 `AGENTS.md`。
- 面对"一步到位"类重构诉求：不走二进制补丁路线，规格先行（能力清单 + 行为对照表），代码只按规格写。
