# 主程序全量反汇编（objdump 线性扫描）

对象：`scpt-analysis/01-unpacked/Scpt.unpacked.exe`（Delphi x86 32-bit，ImageBase `0x400000`，`.text` 5,623,808 B）

## 产物

| 文件 | 内容 | 规模 |
|---|---|---|
| `Scpt.text.asm` | `.text` 全量反汇编（Intel 语法，无机器码列） | **2,164,808 行 / 65.8 MB / 24.5 s** |
| `Scpt.itext.asm` | `.itext` 全量反汇编（含程序入口） | 3,613 行 |

## 生成命令

```bash
objdump -D -M intel --no-show-raw-insn -j .text  <exe> > Scpt.text.asm
objdump -D -M intel --no-show-raw-insn -j .itext <exe> > Scpt.itext.asm
```
（脚本：`tools/scpt/disasm.sh`）

## 完整性校验（实测）

| 指标 | 值 |
|---|---|
| 指令行数 | 2,164,808 |
| 地址范围 | `0x401000` – `0x95d266` |
| 字节跨度 / 节区大小 | 5,620,326 / 5,623,808 = **99.94%**（尾部为 0 填充，objdump 记 `...`） |
| 未解码 `(bad)` | 30,926 行 = **1.43%** |
| stderr | 空 |

程序入口在 `.itext`：RVA `0x561280` → VA `0x961280`
```
961280: push ebp
961281: mov  ebp,esp
961283: add  esp,0xfffffff0
961286: push ebx
961287: mov  eax,0x94f320
96128c: call 0x40f58c        # 直接调用已解析成绝对地址 → 可顺着读
```

## 怎么用（导航）

- **跳进某个目标**：`grep -n -m1 -A30 "^  625378:" Scpt.text.asm`（地址是**无前导零**的小写十六进制，与 objdump 打印一致）。
- **直接 call/jmp 已解析**：`call 0x40f58c` 就是绝对地址 → 可以人工顺着调用图走（Delphi 的跨单元调用多半是直接调用）。
- **找数据引用**：`grep "ds:0x" ` 找绝对地址访问；`.rsrc`/`.idata` 的 RVA ≈ 文件偏移，可直接在镜像里核对字节。

## 局限（实测，别当可用性缺失）

1. **线性扫描分不清 `.text` 里的数据**：Delphi 把 RTTI / resourcestring / 窗体表放在 `.text`，因此除 1.43% 显式 `(bad)` 外，**还有一部分数据被当成指令** → 指令级计数（如 "jmp DWORD PTR" 数量）不可全信。要读语义需递归下降反汇编器（IDR / Ghidra / `r2 -A`）。
2. **没有符号**：函数边界、名字、参数都需外部信息（DFM 事件名 / VMT 单元名，见 `module-map.md` §7 的 Delphi 补名办法）。
3. **不能按 API 名 grep 调用点**：本程序 API 走 Delphi 运行期解析（`.idata` 里只有名字字符串，代码不按地址引用它；`GetProcAddress`/`LoadLibraryA`/`GetModuleHandleA` 三件套在导入表里）。另外我们重建的镜像把尾部节区并进了 `.rsrc`，PE 导入视图不可靠。
4. 本产物是**只读分析**：反汇编不执行样本，也不修改原镜像。
