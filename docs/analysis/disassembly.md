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
3. **按 API 名 grep 只能命中「运行期解析」的那部分**：动态解析的 API（如 `SetupInstallServicesFromInfSectionW`）以 UTF-16 字面量存在、可查（见下节）；**静态导入**的 API（`DeviceIoControl`/`CreateProcessW`/`RegSetValueExW`，UTF-16 出现 0 次）查不到。另外重建镜像把尾部节区并进了 `.rsrc`，PE 导入视图本身不可靠。
4. 本产物是**只读分析**：反汇编不执行样本，也不修改原镜像。

## 函数图 + 字面量交叉引用（替代反编译器的导航方案）

**为什么可行**：Delphi 2009+ 把字符串常量存成 **UTF-16**，代码用**绝对地址**引用；而 Delphi 把常量字符串也放在 `.text` 里。实测 9,503 个 UTF-16 字面量中 **3,750 个** 能在 `.text` 找到绝对引用 → 于是「哪个函数引用了哪条路径/注册表/URL」可以直接查表，**不需要伪代码**。

生成：`tools/scpt/xref.py <exe> <Scpt.text.asm> <输出目录>`（只读，~45 s）

| 产物 | 内容 | 规模 |
|---|---|---|
| `functions.tsv` | 函数边界（**call 目标**为界，剔除 `(bad)` 数据区）+ 调用点/被调次数 | 72,640 函数 |
| `literal-xref.tsv` | `函数 \t 字面量VA \t 引用地址 \t 类别 \t 字面量` | 9,422 条（API 4,197 / 路径 490 / 注册表 27 / URL 20 / 其他 4,688） |

**用法**：`awk -F'\t' '$5 ~ /sysceo\/|Services|Sysprep\./' literal-xref.tsv`

### 已定位的行为锚点（函数地址 → 行为）

| 函数 | 证据（该函数引用的字面量） | 行为 |
|---|---|---|
| `0x008b47e1`、`0x0090fa89`、`0x00911300` | `[Sysprep.RemoveDriver] Begin/End`、`[Sysprep.LoadsrsDrivers] Begin/End/OS Win10`、`Cmdline Nil` | 驱动卸载 / SRS 驱动加载主流程 |
| `0x0089adee`、`0x0089aeff` | `\System32\drivers\`、`[Sysprep.SafeModule] Driver install failed` | 驱动安装（SafeModule） |
| `0x008affcd`、`0x008b0049` | `reg delete HKEY_LOCAL_MACHINE\SYSTEM\ControlSet00x\Enum\Root\ACPI_HAL /f` | **HAL 设备清理**（换机兼容） |
| `0x0090ec52`、`0x0090ef09` | `SYSTEM\CurrentControlSet\Services\intelppm` | 电源管理服务调整 |
| `0x0090d037`、`0x008b257d` | `DriverSigningPolicy=Ignore`、`Software\Policies\...\Driver Signing` | 驱动签名策略改写 |
| `0x0091da57` | `reg\|3\|integer\|SYSTEM\ControlSet001\Services\USBSTOR\|AutoRun\|1` | U 盘自动播放策略 |
| `0x008d1284` | `http://api.sysceo.cn/apps?us=` | **上报/计费接口** |
| `0x008e1fe8`、`0x008e275d`、`0x008e424b` | `lm.sysceo.cn/apps/getaid?name=`、`getScauth?scid=`、`sysceo.cn/scauth?id=` | **授权/登录/计费**（配合 `This mode needs to log in to the Sysceo.cn account`） |
| `0x0093ded2` | `http://con.sysceo.cn/sc/version.html?` | 版本检查 |
| `0x00942384`、`0x009440cd` | `www.sysceo.com/dc`、`/usm`、`bbs.sysceo.com` | 主界面推广链接区 |
| `0x0089c95b`、`0x008a2059` | `\SysCeo\Tool\` | 工具落盘目录 |

### 局限（实测）

- 函数边界只用 **call 目标**：尾调用（`jmp`）目标与数据误码不进表；函数数 72,640 偏多（含数据误判），用作「最近起点」够用，不是带名字的函数清单。
- `API` 类 4,197 条覆盖 2,186 个函数，其中多数是 **Delphi 导入解析器**集中引用（如 `0x007fe260` 引用 34 条 `SetupDi*`），不能直接当"调用点"。**被 PE 导入表静态导入的 API 名不会出现在字面量里**（`DeviceIoControl`/`CreateProcessW`/`RegSetValueExW` 只有 ASCII 形态，UTF-16 出现 0 次）。
- 因此本方案回答的是「**谁写了这条注册表/路径/URL**」，不是「谁调用了某个静态导入 API」。
