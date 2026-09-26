# SCPT 全模块 dossier（自动生成）

> 输入：`work/engines/`（44 个文件：模块 + 内嵌组件 + 主程序脱壳副本）。
> 版本信息/导入/资源由 pefile 解析；字符串为 ASCII + UTF-16 双编码提取。
> 本文件是**原始证据稿**；功能定性与 Rust 方案见 `docs/analysis/module-map.md`。

## 汇总表

| 模块 | 大小 | 架构 | 版本信息(CompanyName / FileDescription) | 导入DLL | 资源类型 | 关键词命中 |
|---|---:|---|---|---:|---|---|
| `FUNA` | 16,078 | - | - | 0 | - | 驱动×4 |
| `FUNB` | 55,808 | x86 | Microsoft Corporation / Windows Setup API / Microsoft® Windo | 5 | MESSAGETABLE×1,STRING×2,VERSION×1 | sysprep×1 |
| `FUNC` | 70,144 | x64 | Microsoft Corporation / Windows Setup API / Microsoft® Windo | 5 | MESSAGETABLE×1,STRING×2,VERSION×1 | sysprep×1 |
| `FUND` | 108,032 | x86 | Microsoft Corporation / sysprep utility / Microsoft(R) Windo | 13 | AVI×1,DIALOG×2,GROUP_ICON×1,ICON×3,MESSAGETABLE×1,STRING×2,VERSION×1 | OEM×9, sysprep×54, 浏览器×2, 网络×1, 驱动×1 |
| `FUNE` | 24,576 | x86 | Microsoft Corporation / SetupCL utility / Microsoft(R) Windo | 1 | MESSAGETABLE×1,VERSION×1 | ACL×4, sysprep×80, 用户配置×1 |
| `FUNF` | 89,088 | x86 | Microsoft Corporation / sysprep utility / Microsoft(R) Windo | 14 | AVI×1,DIALOG×2,GROUP_ICON×1,ICON×3,MESSAGETABLE×1,STRING×2,VERSION×1 | OEM×8, sysprep×54, 浏览器×2, 网络×1 |
| `FUNFX64` | 128,000 | x64 | Microsoft Corporation / sysprep utility / Microsoft(R) Windo | 14 | AVI×1,DIALOG×2,GROUP_ICON×1,ICON×3,MESSAGETABLE×1,STRING×2,VERSION×1 | OEM×8, sysprep×54, 浏览器×2, 网络×1 |
| `FUNG` | 27,136 | x86 | Microsoft Corporation / SetupCL utility / Microsoft(R) Windo | 1 | MESSAGETABLE×1,VERSION×1 | ACL×4, sysprep×80, 用户配置×1 |
| `FUNGX64` | 35,328 | x64 | Microsoft Corporation / SetupCL utility / Microsoft(R) Windo | 1 | MESSAGETABLE×1,VERSION×1 | ACL×4, sysprep×97, 用户配置×1 |
| `FUNH` | 283,760 | - | - | 0 | - | OEM×6, sysprep×3, 伪装×2, 驱动×8 |
| `FUNI` | 313 | - | - | 0 | - | - |
| `FUNJ` | 163,840 | x86 | Helge Klein / SetACL / SetACL | 7 | VERSION×1 | ACL×6, OEM×1 |
| `FUNK` | 13,372,416 | x86 | Igor Pavlov / SysCeo Runtime library / Sczip | 11 | CURSOR×7,DATA×8,GROUP_CURSOR×7,GROUP_ICON×1,ICON×10,MANIFEST×1,RCDATA×4,STRING×22,VERSION×1 | OEM×38, 任务栏×17, 伪装×6, 压缩×4, 总裁系×5, 浏览器×2, 驱动×624 |
| `FUNM` | 4,109,304 | x86 | ForensiT Limited / Set Default Profile / Defprof | 12 | CURSOR×7,DATA×3,GROUP_CURSOR×7,GROUP_ICON×1,ICON×10,RCDATA×4,STRING×31,VERSION×1 | ACL×1, OEM×5, sysprep×20, 任务栏×18, 压缩×1, 总裁系×17, 推广×6, 浏览器×8, 用户配置×56, 虚拟机×1, 部署×171, 驱动×78 |
| `FUNMKR` | 4,488,192 | x86 | ForensiT Limited / Set Default Profile / Defprof | 12 | CURSOR×7,DATA×5,GROUP_CURSOR×7,GROUP_ICON×1,ICON×8,RCDATA×4,STRING×31,VERSION×1 | ACL×1, OEM×5, sysprep×20, 任务栏×18, 伪装×2, 压缩×1, 总裁系×16, 推广×6, 浏览器×8, 用户配置×56, 虚拟机×1, 部署×170, 驱动×90 |
| `FUNMKRX64` | 6,451,200 | x64 | ForensiT Limited / Set Default Profile / Defprof | 12 | CURSOR×7,DATA×5,GROUP_CURSOR×7,GROUP_ICON×1,ICON×8,RCDATA×4,STRING×31,VERSION×1 | ACL×1, OEM×5, sysprep×20, 任务栏×18, 伪装×2, 压缩×1, 总裁系×16, 推广×6, 浏览器×8, 用户配置×56, 虚拟机×1, 部署×170, 驱动×89 |
| `FUNMX64` | 6,067,704 | x64 | ForensiT Limited / Set Default Profile / Defprof | 12 | CURSOR×7,DATA×3,GROUP_CURSOR×7,GROUP_ICON×1,ICON×10,RCDATA×4,STRING×31,VERSION×1 | ACL×1, OEM×5, sysprep×20, 任务栏×18, 压缩×1, 总裁系×17, 推广×6, 浏览器×8, 用户配置×56, 虚拟机×1, 部署×171, 驱动×78 |
| `FUNN` | 12,525,840 | x86 | TOOL / TOOL / TOOL | 14 | CURSOR×7,DATA×3,GROUP_CURSOR×7,GROUP_ICON×1,ICON×10,MANIFEST×1,RCDATA×4,STRING×32,VERSION×1 | OEM×58, sysprep×6, 任务栏×27, 压缩×1, 总裁系×20, 推广×14, 浏览器×35, 浏览器篡改×69, 用户配置×3, 虚拟机×3, 部署×41, 驱动×74 |
| `FUNNKR` | 3,383,808 | x86 | Microsoft Corporation / NT Kernel & System / Microsoft® Wind | 14 | CURSOR×7,GROUP_CURSOR×7,GROUP_ICON×1,ICON×8,MANIFEST×1,RCDATA×4,STRING×32,VERSION×1 | OEM×57, sysprep×7, 任务栏×25, 伪装×2, 压缩×1, 总裁系×17, 推广×12, 浏览器×13, 用户配置×3, 虚拟机×3, 部署×40, 驱动×82 |
| `FUNNKRX64` | 5,518,848 | x64 | Microsoft Corporation / NT Kernel & System / Microsoft® Wind | 14 | CURSOR×7,GROUP_CURSOR×7,GROUP_ICON×1,ICON×8,MANIFEST×1,RCDATA×4,STRING×32,VERSION×1 | OEM×56, sysprep×7, 任务栏×25, 伪装×2, 压缩×1, 总裁系×17, 推广×12, 浏览器×13, 用户配置×3, 虚拟机×3, 部署×40, 驱动×83 |
| `FUNNX64` | 14,659,344 | x64 | TOOL / TOOL / TOOL | 14 | CURSOR×7,DATA×3,GROUP_CURSOR×7,GROUP_ICON×1,ICON×10,MANIFEST×1,RCDATA×4,STRING×32,VERSION×1 | OEM×58, sysprep×6, 任务栏×27, 压缩×1, 总裁系×20, 推广×14, 浏览器×35, 浏览器篡改×69, 用户配置×3, 虚拟机×3, 部署×41, 驱动×75 |
| `FUNO` | 3,398,144 | x86 | Sysceo.com / ScDeployBG_x86 / ScDeployBG_x86 | 12 | CURSOR×7,GROUP_CURSOR×7,GROUP_ICON×1,ICON×10,MANIFEST×1,RCDATA×4,STRING×32,VERSION×1 | OEM×33, sysprep×3, 任务栏×17, 总裁系×13, 浏览器×2, 虚拟机×3, 部署×19, 驱动×8 |
| `FUNOX64` | 5,459,968 | x64 | Sysceo.com / ScDeployBG_x64 / ScDeployBG_x64 | 12 | CURSOR×7,GROUP_CURSOR×7,GROUP_ICON×1,ICON×10,MANIFEST×1,RCDATA×4,STRING×32,VERSION×1 | OEM×33, sysprep×3, 任务栏×17, 总裁系×13, 浏览器×2, 虚拟机×3, 部署×19, 驱动×9 |
| `FUNP` | 4,619,776 | x86 | Sysceo.com / ScProcessBar_x86 / ScProcessBar_x86 | 13 | BITMAP×10,CURSOR×7,GROUP_CURSOR×7,GROUP_ICON×1,ICON×10,MANIFEST×1,RCDATA×6,STRING×38,TESTDATA×1,VERSION×1 | OEM×5, sysprep×1, 任务栏×21, 总裁系×19, 推广×1, 浏览器×2, 部署×20, 驱动×7 |
| `FUNQ` | 1,170,864 | x86 | Sysceo.com / Scaddnet / Scaddnet | 13 | BHLJ×6,CURSOR×7,GROUP_CURSOR×7,GROUP_ICON×1,ICON×4,MANIFEST×1,RCDATA×6,STRING×27,TESTDATA×1,VERSION×1 | 总裁系×2 |
| `FUNR` | 5,930,280 | x86 | SysCeo.com / 驱动总裁在线安装程序 / 驱动总裁在线安装程序 | 13 | BITMAP×10,CURSOR×7,GROUP_CURSOR×7,GROUP_ICON×1,ICON×10,MANIFEST×1,RCDATA×6,STRING×45,TESTDATA×1,VERSION×1 | OEM×3, sysprep×3, 任务栏×22, 总裁系×10, 推广×2, 浏览器×2, 驱动×9 |
| `FUNS` | 5,952,624 | x86 | SysCeo.com / 软件魔盒在线安装程序 / 软件魔盒在线安装程序 | 13 | BITMAP×10,CURSOR×7,GROUP_CURSOR×7,GROUP_ICON×1,ICON×11,MANIFEST×1,RCDATA×6,STRING×45,TESTDATA×1,VERSION×1 | OEM×3, sysprep×3, 任务栏×21, 总裁系×9, 推广×15, 浏览器×2, 驱动×8 |
| `FUNT` | 480,688 | x86 | Www.SysCeo.Com / ScClosemsbox | 7 | BITMAP×11,CURSOR×7,DIALOG×1,GROUP_CURSOR×7,GROUP_ICON×1,ICON×9,RCDATA×3,STRING×16,VERSION×1 | OEM×3, 任务栏×2, 总裁系×1, 驱动×1 |
| `FUNU` | 484,784 | x86 | SysCeo.Com / By:Noime | 7 | BITMAP×11,CURSOR×7,DIALOG×1,GROUP_CURSOR×7,GROUP_ICON×1,ICON×5,RCDATA×3,STRING×16,VERSION×1 | OEM×3, 任务栏×2, 总裁系×1 |
| `FUNV` | 6,569,564 | - | - | 0 | - | OEM×320, 总裁系×11, 虚拟机×11, 驱动×1 |
| `FUNX` | 3,683,760 | x86 | Sysceo.com / Scskipwlan / Scskipwlan | 13 | CURSOR×7,GROUP_CURSOR×7,GROUP_ICON×1,ICON×10,MANIFEST×1,RCDATA×6,STRING×27,TESTDATA×1,VERSION×1 | OEM×3, 任务栏×21, 总裁系×2, 推广×1, 浏览器×2, 部署×3, 驱动×7 |
| `FUNY` | 564,736 | x86 | SysCeo.Com / ScSFC / ScSFC | 8 | BITMAP×11,CURSOR×7,DIALOG×1,GROUP_CURSOR×7,GROUP_ICON×1,ICON×10,RCDATA×3,STRING×17,VERSION×1 | OEM×3, 任务栏×2, 总裁系×2, 部署×2 |
| `FUNZ` | 445,040 | x86 | - | 8 | BITMAP×1,DIALOG×6,GROUP_ICON×1,ICON×4,MANIFEST×1,RCDATA×1,STRING×4 | OEM×4 |
| `PUBCA` | 4,647,936 | x86 | Sysceo.com / ScColourProcessBar_x86 / ScColourProcessBar_x86 | 14 | BITMAP×10,CURSOR×7,GROUP_CURSOR×7,GROUP_ICON×1,ICON×10,MANIFEST×1,RCDATA×6,STRING×38,TESTDATA×1,VERSION×1 | OEM×5, sysprep×1, 任务栏×21, 总裁系×19, 推广×1, 浏览器×2, 部署×20, 驱动×7 |
| `PUBCB` | 15,480 | x86 | Microsoft Corporation / Microsoft Application Virtualization | 1 | VERSION×1 | OEM×2, sysprep×1, 伪装×4, 总裁系×1, 驱动×1 |
| `PUBCC` | 16,504 | x64 | Microsoft Corporation / Microsoft Application Virtualization | 1 | VERSION×1 | OEM×2, sysprep×1, 伪装×4, 总裁系×1, 驱动×1 |
| `PUBCD` | 30,744 | x86 | Microsoft Corporation / Microsoft Application Virtualization | 1 | VERSION×1 | OEM×2, 总裁系×1, 驱动×1 |
| `PUBCE` | 19,224,984 | x86 | Sysceo.com / 软件魔盒 | 5 | GROUP_ICON×1,ICON×10,MANIFEST×1,RCDATA×4,STRING×6,VERSION×1 | 总裁系×1, 推广×1, 驱动×2 |
| `PUBCF` | 4,481,024 | x86 | Sysceo.com / Scpicm / Scpicm | 14 | CURSOR×7,GROUP_CURSOR×7,GROUP_ICON×1,ICON×10,MANIFEST×1,RCDATA×7,STRING×35,TESTDATA×1,VERSION×1 | OEM×5, sysprep×1, 任务栏×22, 总裁系×13, 推广×3, 浏览器×2, 部署×20, 驱动×8 |
| `PUBCG` | 594,432 | x86 | SysCeo.Com / By:Noime / ScRestart | 7 | BITMAP×11,CURSOR×7,DIALOG×1,GROUP_CURSOR×7,GROUP_ICON×1,ICON×9,MANIFEST×1,RCDATA×3,STRING×17,VERSION×1 | OEM×3, 任务栏×2, 总裁系×1 |
| `PUBCH` | 4,032 | - | - | 0 | - | - |
| `PUBCI` | 5,007 | - | - | 0 | - | ACL×1 |
| `funn_unpacked.exe` | 12,525,840 | x86 | TOOL / TOOL / TOOL | 14 | CURSOR×7,DATA×3,GROUP_CURSOR×7,GROUP_ICON×1,ICON×10,MANIFEST×1,RCDATA×4,STRING×32,VERSION×1 | OEM×58, sysprep×6, 任务栏×27, 压缩×1, 总裁系×20, 推广×14, 浏览器×35, 浏览器篡改×69, 用户配置×3, 虚拟机×3, 部署×41, 驱动×74 |
| `funnkrx64_unpacked.exe` | 5,518,848 | x64 | Microsoft Corporation / NT Kernel & System / Microsoft® Wind | 14 | CURSOR×7,GROUP_CURSOR×7,GROUP_ICON×1,ICON×8,MANIFEST×1,RCDATA×4,STRING×32,VERSION×1 | OEM×56, sysprep×7, 任务栏×25, 伪装×2, 压缩×1, 总裁系×17, 推广×12, 浏览器×13, 用户配置×3, 虚拟机×3, 部署×40, 驱动×83 |

### `FUNA`
- 大小 `16,078` · sha256 `b432212eba6507f6…` · 架构 `-` · 子系统 `-` · 入口 `-` · 时间戳 `-`
- 版本信息: 无
- 节区(0): 
- 导入(0 DLL): 
- 内含 DLL 名: `storprop.dll`
- 字符串总数 `179`；关键词命中: 驱动×4
  - 驱动: `CopyFiles = @atapi.sys` | `CopyFiles = @pciide.sys` | `CopyFiles = @pciidex.sys` | `ServiceBinary  = %12%\pciide.sys`

### `FUNB`
- 大小 `55,808` · sha256 `5f9b898315ad8192…` · 架构 `x86` · 子系统 `3` · 入口 `0x5211` · 时间戳 `1037341925`
- 版本信息: CompanyName=`Microsoft Corporation` · FileDescription=`Windows Setup API` · FileVersion=`5.2.3718.0 (dnsrv.021114-1947)` · InternalName=`SETUPAPI.DLL` · LegalCopyright=`© Microsoft Corporation. All rights reserved.` · OriginalFilename=`SETUPAPI.DLL` · ProductName=`Microsoft® Windows® Operating System` · ProductVersion=`5.2.3718.0`
- 节区(3): `.text`, `.data`, `.rsrc`
- 导入(5 DLL): `ADVAPI32.dll`(10), `KERNEL32.dll`(22), `SETUPAPI.dll`(42), `USER32.dll`(4), `msvcrt.dll`(29)
- 资源: MESSAGETABLE×1, STRING×2, VERSION×1
- PDB: `devcon.pdb`
- 内含 DLL 名: `ADVAPI32.dll`, `KERNEL32.dll`, `SETUPAPI.DLL`, `SETUPAPI.dll`, `USER32.dll`, `kernel32.dll`, `msvcrt.dll`, `newdev.dll`, `setupapi.dll`
- 字符串总数 `616`；关键词命中: sysprep×1
  - sysprep: `SetupCloseFileQueue`

### `FUNC`
- 大小 `70,144` · sha256 `99b69330b3fc2a1d…` · 架构 `x64` · 子系统 `3` · 入口 `0x73d0` · 时间戳 `1111711339`
- 版本信息: CompanyName=`Microsoft Corporation` · FileDescription=`Windows Setup API` · FileVersion=`5.2.3790.1830 (srv03_sp1_rtm.050324-1447)` · InternalName=`SETUPAPI.DLL` · LegalCopyright=`© Microsoft Corporation. All rights reserved.` · OriginalFilename=`SETUPAPI.DLL` · ProductName=`Microsoft® Windows® Operating System` · ProductVersion=`5.2.3790.1830`
- 节区(4): `.text`, `.data`, `.pdata`, `.rsrc`
- 导入(5 DLL): `ADVAPI32.dll`(10), `KERNEL32.dll`(26), `SETUPAPI.dll`(42), `USER32.dll`(4), `msvcrt.dll`(27)
- 资源: MESSAGETABLE×1, STRING×2, VERSION×1
- PDB: `devcon.pdb`
- 内含 DLL 名: `ADVAPI32.dll`, `KERNEL32.dll`, `SETUPAPI.DLL`, `SETUPAPI.dll`, `USER32.dll`, `msvcrt.dll`, `newdev.dll`, `setupapi.dll`
- 字符串总数 `648`；关键词命中: sysprep×1
  - sysprep: `SetupCloseFileQueue`

### `FUND`
- 大小 `108,032` · sha256 `89139b29ccdee4a2…` · 架构 `x86` · 子系统 `2` · 入口 `0xa2d5` · 时间戳 `1030608532`
- 版本信息: CompanyName=`Microsoft Corporation` · FileDescription=`sysprep utility` · FileVersion=`5.1.2600.1106 (xpsp1.020828-1920)` · InternalName=`sysprep.EXE` · LegalCopyright=`(C) Microsoft Corporation. All rights reserved.` · OriginalFilename=`sysprep.EXE` · ProductName=`Microsoft(R) Windows(R) Operating System` · ProductVersion=`5.1.2600.1106`
- 节区(3): `.text`, `.data`, `.rsrc`
- 导入(13 DLL): `ADVAPI32.dll`(39), `COMCTL32.dll`(1), `IMAGEHLP.dll`(1), `KERNEL32.dll`(112), `NETAPI32.dll`(6), `SETUPAPI.dll`(40), `SHELL32.dll`(1), `SHLWAPI.dll`(13), `USER32.dll`(30), `USERENV.dll`(1), `WININET.dll`(5), `ntdll.dll`(3), `ole32.dll`(3)
- 资源: AVI×1, DIALOG×2, GROUP_ICON×1, ICON×3, MESSAGETABLE×1, STRING×2, VERSION×1
- PDB: `sysprep.pdb`
- 内含 DLL 名: `ADVAPI32.dll`, `COMCTL32.dll`, `GDI32.dll`, `IMAGEHLP.dll`, `KERNEL32.dll`, `NETAPI32.dll`, `SETUPAPI.dll`, `SHELL32.dll`, `SHLWAPI.dll`, `SRCLIENT.DLL`, `USER32.dll`, `USERENV.dll`, `WININET.dll`, `blackbox.dll`
- 字符串总数 `1421`；关键词命中: OEM×9, sysprep×54, 浏览器×2, 网络×1, 驱动×1
  - 浏览器: `Software\Microsoft\Internet Explorer\International` | `Software\Microsoft\Internet Explorer\TypedURLs`
  - sysprep: `%SystemRoot%\System32\oobe\msoobe.exe /f` | `-bmsd%t%t在 sysprep.inf 中建立所有可用大容量存储设置的列表。` | `-reboot%t%t在完成 SYSPREP.EXE 后重新启动。` | `?:\sysprep\sysprep.inf`
  - 驱动: `WWWWWSRSSj`
  - OEM: `GetOEMCP` | `OEM 重设` | `OEM 重设提示OemReset 选项:  OEMRESET /[ A | AUTO | H | L | R | S ]` | `OEMDefault`
  - 网络: `netshell.dll`

### `FUNE`
- 大小 `24,576` · sha256 `c1e6fddb069b7f0f…` · 架构 `x86` · 子系统 `1` · 入口 `0x55aa` · 时间戳 `1030608534`
- 版本信息: CompanyName=`Microsoft Corporation` · FileDescription=`SetupCL utility` · FileVersion=`5.1.2600.1106 (xpsp1.020828-1920)` · InternalName=`Setupcl.EXE` · LegalCopyright=`(C) Microsoft Corporation. All rights reserved.` · OriginalFilename=`Setupcl.EXE` · ProductName=`Microsoft(R) Windows(R) Operating System` · ProductVersion=`5.1.2600.1106`
- 节区(4): `.text`, `.data`, `.rsrc`, `.reloc`
- 导入(1 DLL): `ntdll.dll`(59)
- 资源: MESSAGETABLE×1, VERSION×1
- PDB: `setupcl.pdb`
- 内含 DLL 名: `ntdll.dll`
- 字符串总数 `379`；关键词命中: ACL×4, sysprep×80, 用户配置×1
  - sysprep: `9XHSETUPCL: SetKey - Failed to Set %ws\%ws (%lx)` | `SETUPCL: BackupRepairHives - Failed to save backup repair SAM hive.` | `SETUPCL: BackupRepairHives - Failed to save backup repair SECURITY hiv` | `SETUPCL: BackupRepairHives - Failed to save backup repair SOFTWARE hiv`
  - 用户配置: `\NTUSER.DAT`
  - ACL: `SETUPCL: ResetACLs - Failed to allocate NewObjectName buffer.` | `SETUPCL: ResetACLs - Failed to open file/directory.` | `SETUPCL: ResetACLs - Failed to query directory.` | `SETUPCL: ResetACLs - Failed to reset ACL on file/directory.`

### `FUNF`
- 大小 `89,088` · sha256 `fc8a390cf1517a6b…` · 架构 `x86` · 子系统 `2` · 入口 `0xbc0e` · 时间戳 `1171691910`
- 版本信息: CompanyName=`Microsoft Corporation` · FileDescription=`sysprep utility` · FileVersion=`5.2.3790.3959 (srv03_sp2_rtm.070216-1710)` · InternalName=`sysprep.EXE` · LegalCopyright=`(C) Microsoft Corporation. All rights reserved.` · OriginalFilename=`sysprep.EXE` · ProductName=`Microsoft(R) Windows(R) Operating System` · ProductVersion=`5.2.3790.3959`
- 节区(3): `.text`, `.data`, `.rsrc`
- 导入(14 DLL): `ADVAPI32.dll`(42), `COMCTL32.dll`(1), `KERNEL32.dll`(83), `NETAPI32.dll`(6), `SETUPAPI.dll`(40), `SHELL32.dll`(1), `SHLWAPI.dll`(13), `USER32.dll`(30), `USERENV.dll`(1), `WININET.dll`(5), `imagehlp.dll`(1), `msvcrt.dll`(35), `ntdll.dll`(2), `ole32.dll`(4)
- 资源: AVI×1, DIALOG×2, GROUP_ICON×1, ICON×3, MESSAGETABLE×1, STRING×2, VERSION×1
- PDB: `sysprep.pdb`
- 内含 DLL 名: `ADVAPI32.dll`, `COMCTL32.dll`, `GDI32.dll`, `KERNEL32.dll`, `NETAPI32.dll`, `SETUPAPI.dll`, `SHELL32.dll`, `SHLWAPI.dll`, `SRCLIENT.DLL`, `USER32.dll`, `USERENV.dll`, `WININET.dll`, `blackbox.dll`, `comdlg32.dll`
- 字符串总数 `1210`；关键词命中: OEM×8, sysprep×54, 浏览器×2, 网络×1
  - 浏览器: `Software\Microsoft\Internet Explorer\International` | `Software\Microsoft\Internet Explorer\TypedURLs`
  - sysprep: `%SystemRoot%\System32\oobe\msoobe.exe /f` | `-bmsd%t%t在 sysprep.inf 中建立所有可用大容量存储设置的列表。` | `-reboot%t%t在完成 SYSPREP.EXE 后重新启动。` | `?:\sysprep\sysprep.inf`
  - OEM: `OEM 重设` | `OEM 重设提示OemReset 选项:  OEMRESET /[ A | AUTO | H | L | R | S ]` | `OEMDefault` | `OEMDuplicatorString`
  - 网络: `netshell.dll`

### `FUNFX64`
- 大小 `128,000` · sha256 `e2f8d885f234a72e…` · 架构 `x64` · 子系统 `2` · 入口 `0x10d80` · 时间戳 `1171690661`
- 版本信息: CompanyName=`Microsoft Corporation` · FileDescription=`sysprep utility` · FileVersion=`5.2.3790.3959 (srv03_sp2_rtm.070216-1710)` · InternalName=`sysprep.EXE` · LegalCopyright=`(C) Microsoft Corporation. All rights reserved.` · OriginalFilename=`sysprep.EXE` · ProductName=`Microsoft(R) Windows(R) Operating System` · ProductVersion=`5.2.3790.3959`
- 节区(4): `.text`, `.data`, `.pdata`, `.rsrc`
- 导入(14 DLL): `ADVAPI32.dll`(42), `COMCTL32.dll`(1), `KERNEL32.dll`(86), `NETAPI32.dll`(6), `SETUPAPI.dll`(40), `SHELL32.dll`(1), `SHLWAPI.dll`(13), `USER32.dll`(30), `USERENV.dll`(1), `WININET.dll`(5), `imagehlp.dll`(1), `msvcrt.dll`(32), `ntdll.dll`(2), `ole32.dll`(4)
- 资源: AVI×1, DIALOG×2, GROUP_ICON×1, ICON×3, MESSAGETABLE×1, STRING×2, VERSION×1
- PDB: `sysprep.pdb`
- 内含 DLL 名: `ADVAPI32.dll`, `COMCTL32.dll`, `GDI32.dll`, `KERNEL32.dll`, `NETAPI32.dll`, `SETUPAPI.dll`, `SHELL32.dll`, `SHLWAPI.dll`, `SRCLIENT.DLL`, `USER32.dll`, `USERENV.dll`, `WININET.dll`, `blackbox.dll`, `comdlg32.dll`
- 字符串总数 `1597`；关键词命中: OEM×8, sysprep×54, 浏览器×2, 网络×1
  - 浏览器: `Software\Microsoft\Internet Explorer\International` | `Software\Microsoft\Internet Explorer\TypedURLs`
  - sysprep: `%SystemRoot%\System32\oobe\msoobe.exe /f` | `-bmsd%t%t在 sysprep.inf 中建立所有可用大容量存储设置的列表。` | `-reboot%t%t在完成 SYSPREP.EXE 后重新启动。` | `?:\sysprep\sysprep.inf`
  - OEM: `OEM 重设` | `OEM 重设提示OemReset 选项:  OEMRESET /[ A | AUTO | H | L | R | S ]` | `OEMDefault` | `OEMDuplicatorString`
  - 网络: `netshell.dll`

### `FUNG`
- 大小 `27,136` · sha256 `1fd9b39a198775c2…` · 架构 `x86` · 子系统 `1` · 入口 `0x598c` · 时间戳 `1171691909`
- 版本信息: CompanyName=`Microsoft Corporation` · FileDescription=`SetupCL utility` · FileVersion=`5.2.3790.3959 (srv03_sp2_rtm.070216-1710)` · InternalName=`Setupcl.EXE` · LegalCopyright=`(C) Microsoft Corporation. All rights reserved.` · OriginalFilename=`Setupcl.EXE` · ProductName=`Microsoft(R) Windows(R) Operating System` · ProductVersion=`5.2.3790.3959`
- 节区(4): `.text`, `.data`, `.rsrc`, `.reloc`
- 导入(1 DLL): `ntdll.dll`(63)
- 资源: MESSAGETABLE×1, VERSION×1
- PDB: `setupcl.pdb`
- 内含 DLL 名: `ntdll.dll`
- 字符串总数 `395`；关键词命中: ACL×4, sysprep×80, 用户配置×1
  - sysprep: `SETUPCL: BackupRepairHives - Failed to save backup repair SAM hive.` | `SETUPCL: BackupRepairHives - Failed to save backup repair SECURITY hiv` | `SETUPCL: BackupRepairHives - Failed to save backup repair SOFTWARE hiv` | `SETUPCL: BackupRepairHives - Failed to save backup repair SYSTEM hive.`
  - 用户配置: `\NTUSER.DAT`
  - ACL: `SETUPCL: ResetACLs - Failed to allocate NewObjectName buffer.` | `SETUPCL: ResetACLs - Failed to open file/directory.` | `SETUPCL: ResetACLs - Failed to query directory.` | `SETUPCL: ResetACLs - Failed to reset ACL on file/directory.`

### `FUNGX64`
- 大小 `35,328` · sha256 `0abfd461be35a1f1…` · 架构 `x64` · 子系统 `1` · 入口 `0x7790` · 时间戳 `1171690661`
- 版本信息: CompanyName=`Microsoft Corporation` · FileDescription=`SetupCL utility` · FileVersion=`5.2.3790.3959 (srv03_sp2_rtm.070216-1710)` · InternalName=`Setupcl.EXE` · LegalCopyright=`(C) Microsoft Corporation. All rights reserved.` · OriginalFilename=`Setupcl.EXE` · ProductName=`Microsoft(R) Windows(R) Operating System` · ProductVersion=`5.2.3790.3959`
- 节区(5): `.text`, `.data`, `.pdata`, `.rsrc`, `.reloc`
- 导入(1 DLL): `ntdll.dll`(61)
- 资源: MESSAGETABLE×1, VERSION×1
- PDB: `setupcl.pdb`
- 内含 DLL 名: `ntdll.dll`
- 字符串总数 `430`；关键词命中: ACL×4, sysprep×97, 用户配置×1
  - sysprep: `SETUPCL: BackupRepairHives - Failed to save backup repair SAM hive.` | `SETUPCL: BackupRepairHives - Failed to save backup repair SECURITY hiv` | `SETUPCL: BackupRepairHives - Failed to save backup repair SOFTWARE hiv` | `SETUPCL: BackupRepairHives - Failed to save backup repair SYSTEM hive.`
  - 用户配置: `\NTUSER.DAT`
  - ACL: `SETUPCL: ResetACLs - Failed to allocate NewObjectName buffer.` | `SETUPCL: ResetACLs - Failed to open file/directory.` | `SETUPCL: ResetACLs - Failed to query directory.` | `SETUPCL: ResetACLs - Failed to reset ACL on file/directory.`

### `FUNH`
- 大小 `283,760` · sha256 `4fdc64b0b6ba825a…` · 架构 `-` · 子系统 `-` · 入口 `-` · 时间戳 `-`
- 版本信息: 无
- 节区(0): 
- 导入(0 DLL): 
- PDB: `boot\bldr\daytona\obj\i386\osloader.pdb`, `osloader.pdb`
- 内含 DLL 名: `KDCOM.DLL`, `hal.dll`, `kdcom.dll`
- 字符串总数 `2544`；关键词命中: OEM×6, sysprep×3, 伪装×2, 驱动×8
  - sysprep: `Unattend Files does not Contain ForceHALDetection.` | `Unattend Files specifies ForceHALDetection.` | `Unattended`
  - 驱动: `NTBOOTDD.SYS` | `\NTBOOTDD.SYS` | `\boot\fs_ext.sys` | `\fs_ext.sys`
  - OEM: `AcpiOemId` | `AcpiOemRevision` | `AcpiOemTableId` | `Comparing OEM ID %s '%6.6s' with '%6.6s' - `
  - 伪装: `ntkrnlmp.exe` | `ntkrnlup.exe`

### `FUNI`
- 大小 `313` · sha256 `532b0a6cc4a17c40…` · 架构 `-` · 子系统 `-` · 入口 `-` · 时间戳 `-`
- 版本信息: 无
- 节区(0): 
- 导入(0 DLL): 
- 字符串总数 `13`；关键词命中: 无

### `FUNJ`
- 大小 `163,840` · sha256 `243dee6b04aa006b…` · 架构 `x86` · 子系统 `3` · 入口 `0x6548` · 时间戳 `1032981298`
- 版本信息: Comments=`Sets Windows NT/2000/XP permissions on files, registry, shares, printers, services` · CompanyName=`Helge Klein` · FileDescription=`SetACL` · FileVersion=`0, 9, 0, 4` · InternalName=`SetACL` · LegalCopyright=`Copyright © 2002 Helge Klein` · OriginalFilename=`SetACL.exe` · ProductName=`SetACL` · ProductVersion=`0, 9, 0, 4`
- 节区(4): `.text`, `.rdata`, `.data`, `.rsrc`
- 导入(7 DLL): `ADVAPI32.dll`(13), `COMCTL32.dll`(1), `GDI32.dll`(24), `KERNEL32.dll`(95), `NETAPI32.dll`(2), `USER32.dll`(86), `WINSPOOL.DRV`(3)
- 资源: VERSION×1
- 内含 DLL 名: `ADVAPI32.dll`, `COMCTL32.DLL`, `COMCTL32.dll`, `GDI32.dll`, `KERNEL32.dll`, `NETAPI32.dll`, `SHELL32.dll`, `USER32.dll`, `comdlg32.dll`, `netmsg.dll`, `user32.dll`
- 字符串总数 `1613`；关键词命中: ACL×6, OEM×1
  - ACL: `Copyright © 2002 Helge Klein` | `Helge Klein` | `SetACL` | `SetACL.exe`
  - OEM: `GetOEMCP`

### `FUNK`
- 大小 `13,372,416` · sha256 `e35068e1f653fa49…` · 架构 `x86` · 子系统 `2` · 入口 `0x20f3d8` · 时间戳 `1731049644`
- 版本信息: CompanyName=`Igor Pavlov` · FileDescription=`SysCeo Runtime library` · FileVersion=`1.06` · InternalName=`Sczip` · LegalCopyright=`Copyright (c) SysCeo All Rights Reserved.` · OriginalFilename=`Sczip.dll` · ProductName=`Sczip` · ProductVersion=`1.06`
- 节区(11): `.text`, `.itext`, `.data`, `.bss`, `.idata`, `.didata`, `.edata`, `.tls`, `.rdata`, `.reloc`, `.rsrc`
- 导入(11 DLL): `advapi32.dll`(20), `comctl32.dll`(35), `gdi32.dll`(94), `kernel32.dll`(1), `ole32.dll`(8), `oleaut32.dll`(2), `shell32.dll`(2), `shlwapi.dll`(1), `user32.dll`(5), `version.dll`(3), `winspool.drv`(1)
- 导出(1): `TMethodImplementationIntercept`
- 资源: CURSOR×7, DATA×8, GROUP_CURSOR×7, GROUP_ICON×1, ICON×10, MANIFEST×1, RCDATA×4, STRING×22, VERSION×1
- DATA 条目(8): `FUNA`, `FUNB`, `FUNC`, `FUND`, `FUNE`, `FUNF`, `FUNH`, `FUNI`
- RCDATA 条目(4): `DVCLAL`, `PACKAGEINFO`, `PLATFORMTARGETS`, `TSCSRSMF`
- 内含 DLL 名: `7zr_x86.dll`, `ADVAPI32.dll`, `Advapi32.dll`, `COMDLG32.dll`, `DWMAPI.DLL`, `GDI32.dll`, `KERNEL32.DLL`, `KERNEL32.dll`, `Kernel32.dll`, `MPR.dll`, `Mapi32.dll`, `NETAPI32.dll`, `OLEAUT32.dll`, `Psapi.dll`
- URL: `http://crls1.wosign.com/ca1.crl0h`, `http://ocsp.digicert.com0C`, `http://ocsp.digicert.com0H`, `http://ocsp.digicert.com0I`, `http://ocsp1.wosign.com/ca10/`
- 字符串总数 `52357`；关键词命中: OEM×38, 任务栏×17, 伪装×6, 压缩×4, 总裁系×5, 浏览器×2, 驱动×624
  - 浏览器: `Monochrome` | `lrMonoChrome`
  - 驱动: `   EXONÉRATION DE GARANTIE.Le logiciel visé par une licence est offert` | ` TArray<System.SysUtils.TLangRec>` | `&TArray<System.SysUtils.TUnitHashEntry>` | `.pesrs`
  - 压缩: `7-Zip (r) [32] 1.06 : Copyright (c) SysCeo All Rights Reserved. : 2017` | `7-Zip cannot find MAPISendMail function` | `7-Zip cannot find the code that works with archives.` | `Igor Pavlov`
  - OEM: `FOEMConvert` | `GetOEMCP` | `OEMConvert` | `OEM_CHARSET`
  - 任务栏: `FMainFormOnTaskBar` | `FTaskbarHandler` | `MainFormOnTaskBar` | `NSystem.Win.TaskbarCore`
  - 总裁系: `7-Zip (r) [32] 1.06 : Copyright (c) SysCeo All Rights Reserved. : 2017` | `Copyright (c) SysCeo All Rights Reserved.` | `Copyright © sysceo.com All Rights Reserved.` | `SysCeo Runtime library`
  - 伪装: `Microsoft Time-Stamp PCA` | `Microsoft Time-Stamp PCA 2010` | `Microsoft Time-Stamp PCA 20100` | `Microsoft Time-Stamp PCA0`

### `FUNM`
- 大小 `4,109,304` · sha256 `37cad1545b3ec19a…` · 架构 `x86` · 子系统 `2` · 入口 `0x2a0abc` · 时间戳 `1747996725`
- 版本信息: CompanyName=`ForensiT Limited` · FileDescription=`Set Default Profile` · FileVersion=`1.11.0.0` · InternalName=`Defprof.exe` · LegalCopyright=`Copyright (C) ForensiT 2010-2016` · OriginalFilename=`Defprof.exe` · ProductName=`Defprof` · ProductVersion=`1.11.0.0`
- 节区(11): `.text`, `.itext`, `.data`, `.bss`, `.idata`, `.didata`, `.edata`, `.tls`, `.rdata`, `.reloc`, `.rsrc`
- 导入(12 DLL): `AdvApi32.dll`(10), `KERNEL32.DLL`(1), `comctl32.dll`(35), `gdi32.dll`(94), `msvcrt.dll`(2), `ole32.dll`(8), `oleaut32.dll`(3), `shell32.dll`(3), `shlwapi.dll`(1), `user32.dll`(5), `version.dll`(3), `winspool.drv`(1)
- 导出(1): `TMethodImplementationIntercept`
- 资源: CURSOR×7, DATA×3, GROUP_CURSOR×7, GROUP_ICON×1, ICON×10, RCDATA×4, STRING×31, VERSION×1
- DATA 条目(3): `FUNA`, `FUNB`, `FUNE`
- RCDATA 条目(4): `DVCLAL`, `PACKAGEINFO`, `PLATFORMTARGETS`, `TSCDMF`
- PDB: `C:\Users\David\Documents\Visual Studio 2012\Projects\Support Projects\Defprof\Release\Defprof.pdb`, `C:\Users\David\Documents\Visual Studio 2012\Projects\upwpmhlp\Release\upwpmhlp.pdb`, `C:\Users\David\Documents\Visual Studio 2015\Projects\ForensiTAppxService\ForensiTAppxService\obj\Release\ForensiTAppxService.pdb`, `C:\Users\David\Documents\Visual Studio 2015\Projects\upwpm\upwpm\obj\Release\upwpm2.pdb`
- 内含 DLL 名: `ADVAPI32.dll`, `AdvApi32.dll`, `DWMAPI.DLL`, `Fwpuclnt.dll`, `IdnDL.dll`, `KERNEL32.DLL`, `KERNEL32.dll`, `Kernel32.dll`, `MSWSOCK.DLL`, `NETAPI32.dll`, `NTDLL.DLL`, `Normaliz.dll`, `OLEAUT32.dll`, `PSAPI.dll`
- URL: `http://ocsp.digicert.com0A`, `http://ocsp.digicert.com0C`, `http://ocsp.digicert.com0I`, `http://ocsp.digicert.com0X`, `http://ocsp.digicert.com0\`
- 字符串总数 `36569`；关键词命中: ACL×1, OEM×5, sysprep×20, 任务栏×18, 压缩×1, 总裁系×17, 推广×6, 浏览器×8, 用户配置×56, 虚拟机×1, 部署×171, 驱动×78
  - 浏览器: `.DEFAULT\Software\Microsoft\Internet Explorer\Main` | `Monochrome` | `SCRUNTEMP\Software\Microsoft\Internet Explorer\Main` | `SCRUNUTEMP\Software\Microsoft\Internet Explorer\Main`
  - sysprep: `OOBEInProgress` | `SkipOOBE` | `Sysprep` | `[Delpoy.After.Systemset.E] Delete sysprep`
  - 驱动: ` TArray<System.SysUtils.TLangRec>` | `&TArray<System.SysUtils.TUnitHashEntry>` | `/TArray<System.SysUtils.TMarshaller.TDisposeRec>` | `:\pagefile.sys`
  - 部署: ` /Edeploy` | `%ws\Software\Microsoft\Windows\CurrentVersion\RunOnce` | `-Deploy` | `-EDeploy`
  - 用户配置: ` ForensiT 2013-2016` | `%s\NTUSER.DAT` | `%ws%ws\ForensiT` | `%ws\AppData\Local\ForensiT`
  - 压缩: `AbZipper`
  - ACL: `RPC_S_UNKNOWN_AUTHZ_SERVICE`
  - OEM: `FOEMConvert` | `GetOEMCP` | `OEMConvert` | `OEM_CHARSET`
  - 任务栏: `FMainFormOnTaskBar` | `FTaskbarHandler` | `MainFormOnTaskBar` | `NSystem.Win.TaskbarCore`
  - 总裁系: `Copyright © sysceo.com All Rights Reserved.` | `E:\Data\Sysceo\SC\SC3.0\Sc3.0\Zip\AbDfBase.pas` | `E:\Data\Sysceo\SC\SC3.0\Sc3.0\Zip\AbDfCryS.pas` | `E:\Data\Sysceo\SC\SC3.0\Sc3.0\Zip\AbDfDec.pas`
  - 虚拟机: `提示:禁止在虚拟机上安装,部署将终止,请到实体机上重试!`
  - 推广: `AppBox` | `Error: Mbox does not exist!` | `Error: Mbox does not exist[MD5]!` | `[Deploy.EDeploy] Mbox False|Vip`

### `FUNMKR`
- 大小 `4,488,192` · sha256 `e3e38d97192df9db…` · 架构 `x86` · 子系统 `2` · 入口 `0x2a0abc` · 时间戳 `1747996833`
- 版本信息: CompanyName=`ForensiT Limited` · FileDescription=`Set Default Profile` · FileVersion=`1.11.0.0` · InternalName=`Defprof.exe` · LegalCopyright=`Copyright (C) ForensiT 2010-2016` · OriginalFilename=`Defprof.exe` · ProductName=`Defprof` · ProductVersion=`1.11.0.0`
- 节区(11): `.text`, `.itext`, `.data`, `.bss`, `.idata`, `.didata`, `.edata`, `.tls`, `.rdata`, `.reloc`, `.rsrc`
- 导入(12 DLL): `AdvApi32.dll`(10), `KERNEL32.DLL`(1), `comctl32.dll`(35), `gdi32.dll`(94), `msvcrt.dll`(2), `ole32.dll`(8), `oleaut32.dll`(3), `shell32.dll`(3), `shlwapi.dll`(1), `user32.dll`(5), `version.dll`(3), `winspool.drv`(1)
- 导出(1): `TMethodImplementationIntercept`
- 资源: CURSOR×7, DATA×5, GROUP_CURSOR×7, GROUP_ICON×1, ICON×8, RCDATA×4, STRING×31, VERSION×1
- DATA 条目(5): `FUNA`, `FUNB`, `FUNE`, `FUNF`, `FUNG`
- RCDATA 条目(4): `DVCLAL`, `PACKAGEINFO`, `PLATFORMTARGETS`, `TSCDMF`
- PDB: `C:\Users\David\Documents\Visual Studio 2012\Projects\Support Projects\Defprof\Release\Defprof.pdb`, `C:\Users\David\Documents\Visual Studio 2012\Projects\upwpmhlp\Release\upwpmhlp.pdb`, `C:\Users\David\Documents\Visual Studio 2015\Projects\ForensiTAppxService\ForensiTAppxService\obj\Release\ForensiTAppxService.pdb`, `C:\Users\David\Documents\Visual Studio 2015\Projects\upwpm\upwpm\obj\Release\upwpm2.pdb`, `E:\Data\Code\Driver\ForceDelete\Debug\Scufd.pdb`, `E:\Data\Code\Driver\ForceDelete\x64\Debug\Scufd.pdb`, `E:\Data\Code\Driver\Scdeleter\Scdeleter\Scdeleter\Bin\Scdeleter.pdb`, `\drv\objfre_win7_amd64\amd64\SuperKillFile.pdb`
- 内含 DLL 名: `ADVAPI32.dll`, `AdvApi32.dll`, `DWMAPI.DLL`, `Fwpuclnt.dll`, `HAL.dll`, `IdnDL.dll`, `KERNEL32.DLL`, `KERNEL32.dll`, `Kernel32.dll`, `MSWSOCK.DLL`, `NETAPI32.dll`, `NTDLL.DLL`, `Normaliz.dll`, `OLEAUT32.dll`
- URL: `http://ocsp.digicert.com0C`, `http://ocsp.digicert.com0I`, `http://ocsp.thawte.com0`, `http://ocsp.verisign.com0`, `http://ocsp.verisign.com0;`
- 字符串总数 `38497`；关键词命中: ACL×1, OEM×5, sysprep×20, 任务栏×18, 伪装×2, 压缩×1, 总裁系×16, 推广×6, 浏览器×8, 用户配置×56, 虚拟机×1, 部署×170, 驱动×90
  - 浏览器: `.DEFAULT\Software\Microsoft\Internet Explorer\Main` | `Monochrome` | `SCRUNTEMP\Software\Microsoft\Internet Explorer\Main` | `SCRUNUTEMP\Software\Microsoft\Internet Explorer\Main`
  - sysprep: `OOBEInProgress` | `SkipOOBE` | `Sysprep` | `[Delpoy.After.Systemset.E] Delete sysprep`
  - 驱动: ` TArray<System.SysUtils.TLangRec>` | `&TArray<System.SysUtils.TUnitHashEntry>` | `/TArray<System.SysUtils.TMarshaller.TDisposeRec>` | `:\pagefile.sys`
  - 部署: ` /Edeploy` | `%ws\Software\Microsoft\Windows\CurrentVersion\RunOnce` | `-Deploy` | `-EDeploy`
  - 用户配置: ` ForensiT 2013-2016` | `%s\NTUSER.DAT` | `%ws%ws\ForensiT` | `%ws\AppData\Local\ForensiT`
  - 压缩: `AbZipper`
  - ACL: `RPC_S_UNKNOWN_AUTHZ_SERVICE`
  - OEM: `FOEMConvert` | `GetOEMCP` | `OEMConvert` | `OEM_CHARSET`
  - 任务栏: `FMainFormOnTaskBar` | `FTaskbarHandler` | `MainFormOnTaskBar` | `NSystem.Win.TaskbarCore`
  - 总裁系: `E:\Data\Sysceo\SC\SC3.0\Sc3.0\Zip\AbDfBase.pas` | `E:\Data\Sysceo\SC\SC3.0\Sc3.0\Zip\AbDfCryS.pas` | `E:\Data\Sysceo\SC\SC3.0\Sc3.0\Zip\AbDfDec.pas` | `E:\Data\Sysceo\SC\SC3.0\Sc3.0\Zip\AbDfEnc.pas`
  - 伪装: `NT Kernel & System` | `ntkrnlmp.exe`
  - 虚拟机: `提示:禁止在虚拟机上安装,部署将终止,请到实体机上重试!`
  - 推广: `AppBox` | `Error: Mbox does not exist!` | `Error: Mbox does not exist[MD5]!` | `[Deploy.EDeploy] Mbox False|Vip`

### `FUNMKRX64`
- 大小 `6,451,200` · sha256 `e4b629ab918bbc24…` · 架构 `x64` · 子系统 `2` · 入口 `0x40e370` · 时间戳 `1747996837`
- 版本信息: CompanyName=`ForensiT Limited` · FileDescription=`Set Default Profile` · FileVersion=`1.11.0.0` · InternalName=`Defprof.exe` · LegalCopyright=`Copyright (C) ForensiT 2010-2016` · OriginalFilename=`Defprof.exe` · ProductName=`Defprof` · ProductVersion=`1.11.0.0`
- 节区(11): `.text`, `.data`, `.bss`, `.idata`, `.didata`, `.edata`, `.tls`, `.rdata`, `.reloc`, `.pdata`, `.rsrc`
- 导入(12 DLL): `AdvApi32.dll`(10), `KERNEL32.DLL`(1), `comctl32.dll`(35), `gdi32.dll`(94), `msvcrt.dll`(2), `ole32.dll`(8), `oleaut32.dll`(3), `shell32.dll`(3), `shlwapi.dll`(1), `user32.dll`(5), `version.dll`(3), `winspool.drv`(1)
- 导出(3): `TMethodImplementationIntercept`, `__dbk_fcall_wrapper`, `dbkFCallWrapperAddr`
- 资源: CURSOR×7, DATA×5, GROUP_CURSOR×7, GROUP_ICON×1, ICON×8, RCDATA×4, STRING×31, VERSION×1
- DATA 条目(5): `FUNA`, `FUNB`, `FUNE`, `FUNF`, `FUNG`
- RCDATA 条目(4): `DVCLAL`, `PACKAGEINFO`, `PLATFORMTARGETS`, `TSCDMF`
- PDB: `C:\Users\David\Documents\Visual Studio 2012\Projects\Support Projects\Defprof\Release\Defprof.pdb`, `C:\Users\David\Documents\Visual Studio 2012\Projects\upwpmhlp\Release\upwpmhlp.pdb`, `C:\Users\David\Documents\Visual Studio 2015\Projects\ForensiTAppxService\ForensiTAppxService\obj\Release\ForensiTAppxService.pdb`, `C:\Users\David\Documents\Visual Studio 2015\Projects\upwpm\upwpm\obj\Release\upwpm2.pdb`, `E:\Data\Code\Driver\ForceDelete\Debug\Scufd.pdb`, `E:\Data\Code\Driver\ForceDelete\x64\Debug\Scufd.pdb`, `E:\Data\Code\Driver\Scdeleter\Scdeleter\Scdeleter\Bin\Scdeleter.pdb`, `\drv\objfre_win7_amd64\amd64\SuperKillFile.pdb`
- 内含 DLL 名: `ADVAPI32.dll`, `AdvApi32.dll`, `DWMAPI.DLL`, `Fwpuclnt.dll`, `HAL.dll`, `IdnDL.dll`, `KERNEL32.DLL`, `KERNEL32.dll`, `Kernel32.dll`, `MSWSOCK.DLL`, `NETAPI32.dll`, `NTDLL.DLL`, `Normaliz.dll`, `OLEAUT32.dll`
- URL: `http://ocsp.digicert.com0C`, `http://ocsp.digicert.com0I`, `http://ocsp.thawte.com0`, `http://ocsp.verisign.com0`, `http://ocsp.verisign.com0;`
- 字符串总数 `49523`；关键词命中: ACL×1, OEM×5, sysprep×20, 任务栏×18, 伪装×2, 压缩×1, 总裁系×16, 推广×6, 浏览器×8, 用户配置×56, 虚拟机×1, 部署×170, 驱动×89
  - 浏览器: `.DEFAULT\Software\Microsoft\Internet Explorer\Main` | `MonochromeP^Y` | `SCRUNTEMP\Software\Microsoft\Internet Explorer\Main` | `SCRUNUTEMP\Software\Microsoft\Internet Explorer\Main`
  - sysprep: `OOBEInProgress` | `SkipOOBE` | `Sysprep` | `[Delpoy.After.Systemset.E] Delete sysprep`
  - 驱动: ` TArray<System.SysUtils.TLangRec>` | `&TArray<System.SysUtils.TUnitHashEntry>(` | `/TArray<System.SysUtils.TMarshaller.TDisposeRec> ` | `:\pagefile.sys`
  - 部署: ` /Edeploy` | `%ws\Software\Microsoft\Windows\CurrentVersion\RunOnce` | `-Deploy` | `-EDeploy`
  - 用户配置: ` ForensiT 2013-2016` | `%s\NTUSER.DAT` | `%ws%ws\ForensiT` | `%ws\AppData\Local\ForensiT`
  - 压缩: `AbZipper`
  - ACL: `RPC_S_UNKNOWN_AUTHZ_SERVICE`
  - OEM: `FOEMConvert` | `GetOEMCP` | `OEMConvert` | `OEM_CHARSET`
  - 任务栏: `FMainFormOnTaskBar` | `FTaskbarHandler` | `MainFormOnTaskBar` | `NSystem.Win.TaskbarCore`
  - 总裁系: `E:\Data\Sysceo\SC\SC3.0\Sc3.0\Zip\AbDfBase.pas` | `E:\Data\Sysceo\SC\SC3.0\Sc3.0\Zip\AbDfCryS.pas` | `E:\Data\Sysceo\SC\SC3.0\Sc3.0\Zip\AbDfDec.pas` | `E:\Data\Sysceo\SC\SC3.0\Sc3.0\Zip\AbDfEnc.pas`
  - 伪装: `NT Kernel & System` | `ntkrnlmp.exe`
  - 虚拟机: `提示:禁止在虚拟机上安装,部署将终止,请到实体机上重试!`
  - 推广: `AppBox` | `Error: Mbox does not exist!` | `Error: Mbox does not exist[MD5]!` | `[Deploy.EDeploy] Mbox False|Vip`

### `FUNMX64`
- 大小 `6,067,704` · sha256 `387f835bd3492e49…` · 架构 `x64` · 子系统 `2` · 入口 `0x40df70` · 时间戳 `1747996706`
- 版本信息: CompanyName=`ForensiT Limited` · FileDescription=`Set Default Profile` · FileVersion=`1.11.0.0` · InternalName=`Defprof.exe` · LegalCopyright=`Copyright (C) ForensiT 2010-2016` · OriginalFilename=`Defprof.exe` · ProductName=`Defprof` · ProductVersion=`1.11.0.0`
- 节区(11): `.text`, `.data`, `.bss`, `.idata`, `.didata`, `.edata`, `.tls`, `.rdata`, `.reloc`, `.pdata`, `.rsrc`
- 导入(12 DLL): `AdvApi32.dll`(10), `KERNEL32.DLL`(1), `comctl32.dll`(35), `gdi32.dll`(94), `msvcrt.dll`(2), `ole32.dll`(8), `oleaut32.dll`(3), `shell32.dll`(3), `shlwapi.dll`(1), `user32.dll`(5), `version.dll`(3), `winspool.drv`(1)
- 导出(3): `TMethodImplementationIntercept`, `__dbk_fcall_wrapper`, `dbkFCallWrapperAddr`
- 资源: CURSOR×7, DATA×3, GROUP_CURSOR×7, GROUP_ICON×1, ICON×10, RCDATA×4, STRING×31, VERSION×1
- DATA 条目(3): `FUNA`, `FUNB`, `FUNE`
- RCDATA 条目(4): `DVCLAL`, `PACKAGEINFO`, `PLATFORMTARGETS`, `TSCDMF`
- PDB: `C:\Users\David\Documents\Visual Studio 2012\Projects\Support Projects\Defprof\Release\Defprof.pdb`, `C:\Users\David\Documents\Visual Studio 2012\Projects\upwpmhlp\Release\upwpmhlp.pdb`, `C:\Users\David\Documents\Visual Studio 2015\Projects\ForensiTAppxService\ForensiTAppxService\obj\Release\ForensiTAppxService.pdb`, `C:\Users\David\Documents\Visual Studio 2015\Projects\upwpm\upwpm\obj\Release\upwpm2.pdb`
- 内含 DLL 名: `ADVAPI32.dll`, `AdvApi32.dll`, `DWMAPI.DLL`, `Fwpuclnt.dll`, `IdnDL.dll`, `KERNEL32.DLL`, `KERNEL32.dll`, `Kernel32.dll`, `MSWSOCK.DLL`, `NETAPI32.dll`, `NTDLL.DLL`, `Normaliz.dll`, `OLEAUT32.dll`, `SHELL32.dll`
- URL: `http://ocsp.digicert.com0A`, `http://ocsp.digicert.com0C`, `http://ocsp.digicert.com0I`, `http://ocsp.digicert.com0X`, `http://ocsp.digicert.com0\`
- 字符串总数 `47462`；关键词命中: ACL×1, OEM×5, sysprep×20, 任务栏×18, 压缩×1, 总裁系×17, 推广×6, 浏览器×8, 用户配置×56, 虚拟机×1, 部署×171, 驱动×78
  - 浏览器: `.DEFAULT\Software\Microsoft\Internet Explorer\Main` | `MonochromeP^Y` | `SCRUNTEMP\Software\Microsoft\Internet Explorer\Main` | `SCRUNUTEMP\Software\Microsoft\Internet Explorer\Main`
  - sysprep: `OOBEInProgress` | `SkipOOBE` | `Sysprep` | `[Delpoy.After.Systemset.E] Delete sysprep`
  - 驱动: ` TArray<System.SysUtils.TLangRec>` | `&TArray<System.SysUtils.TUnitHashEntry>(` | `/TArray<System.SysUtils.TMarshaller.TDisposeRec> ` | `:\pagefile.sys`
  - 部署: ` /Edeploy` | `%ws\Software\Microsoft\Windows\CurrentVersion\RunOnce` | `-Deploy` | `-EDeploy`
  - 用户配置: ` ForensiT 2013-2016` | `%s\NTUSER.DAT` | `%ws%ws\ForensiT` | `%ws\AppData\Local\ForensiT`
  - 压缩: `AbZipper`
  - ACL: `RPC_S_UNKNOWN_AUTHZ_SERVICE`
  - OEM: `FOEMConvert` | `GetOEMCP` | `OEMConvert` | `OEM_CHARSET`
  - 任务栏: `FMainFormOnTaskBar` | `FTaskbarHandler` | `MainFormOnTaskBar` | `NSystem.Win.TaskbarCore`
  - 总裁系: `Copyright © sysceo.com All Rights Reserved.` | `E:\Data\Sysceo\SC\SC3.0\Sc3.0\Zip\AbDfBase.pas` | `E:\Data\Sysceo\SC\SC3.0\Sc3.0\Zip\AbDfCryS.pas` | `E:\Data\Sysceo\SC\SC3.0\Sc3.0\Zip\AbDfDec.pas`
  - 虚拟机: `提示:禁止在虚拟机上安装,部署将终止,请到实体机上重试!`
  - 推广: `AppBox` | `Error: Mbox does not exist!` | `Error: Mbox does not exist[MD5]!` | `[Deploy.EDeploy] Mbox False|Vip`

### `FUNN`
- 大小 `12,525,840` · sha256 `2c90e7a69a5a109f…` · 架构 `x86` · 子系统 `2` · 入口 `0x2dac0c` · 时间戳 `1778808618`
- 版本信息: CompanyName=`TOOL` · FileDescription=`TOOL` · FileVersion=`1.5.0.1` · InternalName=`Crun.exe` · LegalCopyright=`Copyright (C) 2021` · OriginalFilename=`Crun.exe` · ProductName=`TOOL` · ProductVersion=`1.5.0.1`
- 节区(11): `.text`, `.itext`, `.data`, `.bss`, `.idata`, `.didata`, `.edata`, `.tls`, `.rdata`, `.reloc`, `.rsrc`
- 导入(14 DLL): `AdvApi32.dll`(5), `KERNEL32.DLL`(1), `SetupApi.dll`(4), `cfgmgr32.dll`(1), `comctl32.dll`(35), `gdi32.dll`(96), `msvcrt.dll`(2), `ole32.dll`(10), `oleaut32.dll`(3), `shell32.dll`(2), `shlwapi.dll`(1), `user32.dll`(5), `version.dll`(3), `winspool.drv`(1)
- 导出(1): `TMethodImplementationIntercept`
- 资源: CURSOR×7, DATA×3, GROUP_CURSOR×7, GROUP_ICON×1, ICON×10, MANIFEST×1, RCDATA×4, STRING×32, VERSION×1
- DATA 条目(3): `FUNA`, `FUNB`, `FUNC`
- RCDATA 条目(4): `DVCLAL`, `PACKAGEINFO`, `PLATFORMTARGETS`, `TSCTMF`
- PDB: `C++\Browser_noime_enew\DLL_Release\broscfg.pdb`, `E:\workspaces\Crack\SetEdge\Release\EdgeCipherx64.pdb`
- 内含 DLL 名: `ADVAPI32.dll`, `AdvApi32.dll`, `DWMAPI.DLL`, `Fwpuclnt.dll`, `GDI32.dll`, `IMM32.dll`, `IdnDL.dll`, `KERNEL32.DLL`, `KERNEL32.dll`, `Kernel32.dll`, `KernelBase.dll`, `MSIMG32.dll`, `MSWSOCK.DLL`, `NETAPI32.dll`
- URL: `http://dh.sejai.com`, `http://ocsp.digicert.com0A`, `http://ocsp.digicert.com0\`, `http://www.digicert.com/CPS0`
- 字符串总数 `62765`；关键词命中: OEM×58, sysprep×6, 任务栏×27, 压缩×1, 总裁系×20, 推广×14, 浏览器×35, 浏览器篡改×69, 用户配置×3, 虚拟机×3, 部署×41, 驱动×74
  - 浏览器篡改: ` opentabpagetypedefinepagestring="https://newtabx.com/" activenewtabpo` | `"url": "https://www.baidu.com/#tn=90013418_hao_pg&ie={inputEncoding}&w` | `<?xml version="1.0" encoding="utf-8"?><main><Item homepagetype50="3" h` | `C++\Browser_noime_enew\DLL_Release\broscfg.pdb`
  - 浏览器: ` ProxyPassByLocal="FALSE" securitylevel="1" usesecureinput="TRUE" auto` | ` appmodekeepmax="FALSE" newwindowfromoutside="0" forceopenhomepage="TR` | `360Chrome` | `<?xml version="1.0" encoding="utf-8"?><main><Item homepagetype50="3" h`
  - sysprep: `SetupCloseFileQueue` | `SetupCloseInfFile` | `SetupCloseLog` | `SkipOOBE`
  - 驱动: ` TArray<System.SysUtils.TLangRec>` | `&TArray<System.SysUtils.TUnitHashEntry>` | `.system CMD ARGS...    Run CMD ARGS... in a system shell` | `/TArray<System.SysUtils.TMarshaller.TDisposeRec>`
  - 部署: `DecryptScdata` | `Deploy` | `Error:Scdata.sc file missing!` | `Es4InDeploy`
  - 用户配置: `NTUSER.DAT` | `SCRUNTEMP` | `SCRUNTEMP\Control Panel\International`
  - 压缩: `AbZipper`
  - OEM: `&TArray<uSMBIOS.TOEMStringsInformation>` | `+TArray<uSMBIOS_XP.TOEMStringsInformationXP>` | `AutoOem` | `AutoOembg`
  - 任务栏: `FMainFormOnTaskBar` | `FTaskbarHandler` | `Locktaskbar` | `Locktaskbarlist`
  - 总裁系: `Copyright © sysceo.com All Rights Reserved.` | `E:\Data\Sysceo\AD\` | `E:\Data\Sysceo\SC\SC3.0\Sc3.0\Zip\AbDfBase.pas` | `E:\Data\Sysceo\SC\SC3.0\Sc3.0\Zip\AbDfCryS.pas`
  - 虚拟机: `VMware, Inc.` | `VirtualBox` | `VmWare`
  - 推广: `AppBox` | `Error:  Mbox does not exist[MD5]!` | `Error: Mbox does not exist!` | `Error: Mbox does not exist[MD5]!`

### `FUNNKR`
- 大小 `3,383,808` · sha256 `0960562617cc41af…` · 架构 `x86` · 子系统 `2` · 入口 `0x2dbc0c` · 时间戳 `1747995982`
- 版本信息: CompanyName=`Microsoft Corporation` · FileDescription=`NT Kernel & System` · FileVersion=`6.1.7601.17514` · InternalName=`ntkrnlmp.exe` · LegalCopyright=`© Microsoft Corporation. All rights reserved.` · ProductName=`Microsoft® Windows® Operating System` · ProductVersion=`6.1.7601.17514`
- 节区(11): `.text`, `.itext`, `.data`, `.bss`, `.idata`, `.didata`, `.edata`, `.tls`, `.rdata`, `.reloc`, `.rsrc`
- 导入(14 DLL): `AdvApi32.dll`(5), `KERNEL32.DLL`(1), `SetupApi.dll`(4), `cfgmgr32.dll`(1), `comctl32.dll`(35), `gdi32.dll`(96), `msvcrt.dll`(2), `ole32.dll`(10), `oleaut32.dll`(3), `shell32.dll`(2), `shlwapi.dll`(1), `user32.dll`(5), `version.dll`(3), `winspool.drv`(1)
- 导出(1): `TMethodImplementationIntercept`
- 资源: CURSOR×7, GROUP_CURSOR×7, GROUP_ICON×1, ICON×8, MANIFEST×1, RCDATA×4, STRING×32, VERSION×1
- RCDATA 条目(4): `DVCLAL`, `PACKAGEINFO`, `PLATFORMTARGETS`, `TSCTMF`
- 内含 DLL 名: `AdvApi32.dll`, `DWMAPI.DLL`, `Fwpuclnt.dll`, `IdnDL.dll`, `KERNEL32.DLL`, `Kernel32.dll`, `MSWSOCK.DLL`, `NTDLL.DLL`, `Normaliz.dll`, `PSAPI.dll`, `SetupApi.dll`, `Shell32.dll`, `WS2_32.DLL`, `Wship6.dll`
- 字符串总数 `34451`；关键词命中: OEM×57, sysprep×7, 任务栏×25, 伪装×2, 压缩×1, 总裁系×17, 推广×12, 浏览器×13, 用户配置×3, 虚拟机×3, 部署×40, 驱动×82
  - 浏览器: `BrowserHomepage` | `Monochrome` | `SOFTWARE\Microsoft\Internet Explorer\MAIN` | `SOFTWARE\Microsoft\Internet Explorer\Main`
  - sysprep: `SetupCloseFileQueue` | `SetupCloseInfFile` | `SetupCloseLog` | `SkipOOBE`
  - 驱动: ` TArray<System.SysUtils.TLangRec>` | `&TArray<System.SysUtils.TUnitHashEntry>` | `/TArray<System.SysUtils.TMarshaller.TDisposeRec>` | `ClearSrs`
  - 部署: `DecryptScdata` | `Deploy` | `Error:Scdata.sc file missing!` | `Es4InDeploy`
  - 用户配置: `NTUSER.DAT` | `SCRUNTEMP` | `SCRUNTEMP\Control Panel\International`
  - 压缩: `AbZipper`
  - OEM: `&TArray<uSMBIOS.TOEMStringsInformation>` | `+TArray<uSMBIOS_XP.TOEMStringsInformationXP>` | `AutoOem` | `AutoOembg`
  - 任务栏: `FMainFormOnTaskBar` | `FTaskbarHandler` | `Locktaskbar` | `Locktaskbarlist`
  - 总裁系: `E:\Data\Sysceo\SC\SC3.0\Sc3.0\Zip\AbDfBase.pas` | `E:\Data\Sysceo\SC\SC3.0\Sc3.0\Zip\AbDfCryS.pas` | `E:\Data\Sysceo\SC\SC3.0\Sc3.0\Zip\AbDfDec.pas` | `E:\Data\Sysceo\SC\SC3.0\Sc3.0\Zip\AbDfEnc.pas`
  - 伪装: `NT Kernel & System` | `ntkrnlmp.exe`
  - 虚拟机: `VMware, Inc.` | `VirtualBox` | `VmWare`
  - 推广: `AppBox` | `Error:  Mbox does not exist[MD5]!` | `Error: Mbox does not exist!` | `Error: Mbox does not exist[MD5]!`

### `FUNNKRX64`
- 大小 `5,518,848` · sha256 `2e761c25cf584473…` · 架构 `x64` · 子系统 `2` · 入口 `0x46f470` · 时间戳 `1747995977`
- 版本信息: CompanyName=`Microsoft Corporation` · FileDescription=`NT Kernel & System` · FileVersion=`6.1.7601.17514` · InternalName=`ntkrnlmp.exe` · LegalCopyright=`© Microsoft Corporation. All rights reserved.` · ProductName=`Microsoft® Windows® Operating System` · ProductVersion=`6.1.7601.17514`
- 节区(11): `.text`, `.data`, `.bss`, `.idata`, `.didata`, `.edata`, `.tls`, `.rdata`, `.reloc`, `.pdata`, `.rsrc`
- 导入(14 DLL): `AdvApi32.dll`(5), `KERNEL32.DLL`(1), `SetupApi.dll`(2), `cfgmgr32.dll`(1), `comctl32.dll`(35), `gdi32.dll`(96), `msvcrt.dll`(2), `ole32.dll`(10), `oleaut32.dll`(3), `shell32.dll`(2), `shlwapi.dll`(1), `user32.dll`(5), `version.dll`(3), `winspool.drv`(1)
- 导出(3): `TMethodImplementationIntercept`, `__dbk_fcall_wrapper`, `dbkFCallWrapperAddr`
- 资源: CURSOR×7, GROUP_CURSOR×7, GROUP_ICON×1, ICON×8, MANIFEST×1, RCDATA×4, STRING×32, VERSION×1
- RCDATA 条目(4): `DVCLAL`, `PACKAGEINFO`, `PLATFORMTARGETS`, `TSCTMF`
- 内含 DLL 名: `AdvApi32.dll`, `DWMAPI.DLL`, `Fwpuclnt.dll`, `IdnDL.dll`, `KERNEL32.DLL`, `MSWSOCK.DLL`, `NTDLL.DLL`, `Normaliz.dll`, `SetupApi.dll`, `Shell32.dll`, `User32.dll`, `WS2_32.DLL`, `Wship6.dll`, `advapi32.dll`
- 字符串总数 `47752`；关键词命中: OEM×56, sysprep×7, 任务栏×25, 伪装×2, 压缩×1, 总裁系×17, 推广×12, 浏览器×13, 用户配置×3, 虚拟机×3, 部署×40, 驱动×83
  - 浏览器: `BrowserHomepage` | `MonochromeP` | `SOFTWARE\Microsoft\Internet Explorer\MAIN` | `SOFTWARE\Microsoft\Internet Explorer\Main`
  - sysprep: `SetupCloseFileQueue` | `SetupCloseInfFile` | `SetupCloseLog` | `SkipOOBE`
  - 驱动: ` TArray<System.SysUtils.TLangRec>` | `&TArray<System.SysUtils.TUnitHashEntry>(` | `/TArray<System.SysUtils.TMarshaller.TDisposeRec> ` | `ClearSrs`
  - 部署: `DecryptScdata` | `Deploy` | `Error:Scdata.sc file missing!` | `Es4InDeploy`
  - 用户配置: `NTUSER.DAT` | `SCRUNTEMP` | `SCRUNTEMP\Control Panel\International`
  - 压缩: `AbZipper`
  - OEM: `&TArray<uSMBIOS.TOEMStringsInformation>` | `+TArray<uSMBIOS_XP.TOEMStringsInformationXP>` | `AutoOem` | `AutoOembg`
  - 任务栏: `FMainFormOnTaskBar` | `FTaskbarHandler` | `Locktaskbar` | `Locktaskbarlist`
  - 总裁系: `E:\Data\Sysceo\SC\SC3.0\Sc3.0\Zip\AbDfBase.pas` | `E:\Data\Sysceo\SC\SC3.0\Sc3.0\Zip\AbDfCryS.pas` | `E:\Data\Sysceo\SC\SC3.0\Sc3.0\Zip\AbDfDec.pas` | `E:\Data\Sysceo\SC\SC3.0\Sc3.0\Zip\AbDfEnc.pas`
  - 伪装: `NT Kernel & System` | `ntkrnlmp.exe`
  - 虚拟机: `VMware, Inc.` | `VirtualBox` | `VmWare`
  - 推广: `AppBox` | `Error:  Mbox does not exist[MD5]!` | `Error: Mbox does not exist!` | `Error: Mbox does not exist[MD5]!`

### `FUNNX64`
- 大小 `14,659,344` · sha256 `e4881750bc1d5dc8…` · 架构 `x64` · 子系统 `2` · 入口 `0x46e880` · 时间戳 `1778808622`
- 版本信息: CompanyName=`TOOL` · FileDescription=`TOOL` · FileVersion=`1.5.0.1` · InternalName=`Crun.exe` · LegalCopyright=`Copyright (C) 2021` · OriginalFilename=`Crun.exe` · ProductName=`TOOL` · ProductVersion=`1.5.0.1`
- 节区(11): `.text`, `.data`, `.bss`, `.idata`, `.didata`, `.edata`, `.tls`, `.rdata`, `.reloc`, `.pdata`, `.rsrc`
- 导入(14 DLL): `AdvApi32.dll`(5), `KERNEL32.DLL`(1), `SetupApi.dll`(2), `cfgmgr32.dll`(1), `comctl32.dll`(35), `gdi32.dll`(96), `msvcrt.dll`(2), `ole32.dll`(10), `oleaut32.dll`(3), `shell32.dll`(2), `shlwapi.dll`(1), `user32.dll`(5), `version.dll`(3), `winspool.drv`(1)
- 导出(3): `TMethodImplementationIntercept`, `__dbk_fcall_wrapper`, `dbkFCallWrapperAddr`
- 资源: CURSOR×7, DATA×3, GROUP_CURSOR×7, GROUP_ICON×1, ICON×10, MANIFEST×1, RCDATA×4, STRING×32, VERSION×1
- DATA 条目(3): `FUNA`, `FUNB`, `FUNC`
- RCDATA 条目(4): `DVCLAL`, `PACKAGEINFO`, `PLATFORMTARGETS`, `TSCTMF`
- PDB: `C++\Browser_noime_enew\DLL_Release\broscfg.pdb`, `E:\workspaces\Crack\SetEdge\Release\EdgeCipherx64.pdb`
- 内含 DLL 名: `ADVAPI32.dll`, `AdvApi32.dll`, `DWMAPI.DLL`, `Fwpuclnt.dll`, `GDI32.dll`, `IMM32.dll`, `IdnDL.dll`, `KERNEL32.DLL`, `KERNEL32.dll`, `KernelBase.dll`, `MSIMG32.dll`, `MSWSOCK.DLL`, `NETAPI32.dll`, `NTDLL.DLL`
- URL: `http://dh.sejai.com`, `http://ocsp.digicert.com0A`, `http://ocsp.digicert.com0\`, `http://www.digicert.com/CPS0`
- 字符串总数 `76017`；关键词命中: OEM×58, sysprep×6, 任务栏×27, 压缩×1, 总裁系×20, 推广×14, 浏览器×35, 浏览器篡改×69, 用户配置×3, 虚拟机×3, 部署×41, 驱动×75
  - 浏览器篡改: ` opentabpagetypedefinepagestring="https://newtabx.com/" activenewtabpo` | `"url": "https://www.baidu.com/#tn=90013418_hao_pg&ie={inputEncoding}&w` | `<?xml version="1.0" encoding="utf-8"?><main><Item homepagetype50="3" h` | `C++\Browser_noime_enew\DLL_Release\broscfg.pdb`
  - 浏览器: ` ProxyPassByLocal="FALSE" securitylevel="1" usesecureinput="TRUE" auto` | ` appmodekeepmax="FALSE" newwindowfromoutside="0" forceopenhomepage="TR` | `360Chrome` | `<?xml version="1.0" encoding="utf-8"?><main><Item homepagetype50="3" h`
  - sysprep: `SetupCloseFileQueue` | `SetupCloseInfFile` | `SetupCloseLog` | `SkipOOBE`
  - 驱动: ` TArray<System.SysUtils.TLangRec>` | `&TArray<System.SysUtils.TUnitHashEntry>(` | `.system CMD ARGS...    Run CMD ARGS... in a system shell` | `/TArray<System.SysUtils.TMarshaller.TDisposeRec> `
  - 部署: `DecryptScdata` | `Deploy` | `Error:Scdata.sc file missing!` | `Es4InDeploy`
  - 用户配置: `NTUSER.DAT` | `SCRUNTEMP` | `SCRUNTEMP\Control Panel\International`
  - 压缩: `AbZipper`
  - OEM: `&TArray<uSMBIOS.TOEMStringsInformation>` | `+TArray<uSMBIOS_XP.TOEMStringsInformationXP>` | `AutoOem` | `AutoOembg`
  - 任务栏: `FMainFormOnTaskBar` | `FTaskbarHandler` | `Locktaskbar` | `Locktaskbarlist`
  - 总裁系: `Copyright © sysceo.com All Rights Reserved.` | `E:\Data\Sysceo\AD\` | `E:\Data\Sysceo\SC\SC3.0\Sc3.0\Zip\AbDfBase.pas` | `E:\Data\Sysceo\SC\SC3.0\Sc3.0\Zip\AbDfCryS.pas`
  - 虚拟机: `VMware, Inc.` | `VirtualBox` | `VmWare`
  - 推广: `AppBox` | `Error:  Mbox does not exist[MD5]!` | `Error: Mbox does not exist!` | `Error: Mbox does not exist[MD5]!`

### `FUNO`
- 大小 `3,398,144` · sha256 `a7910cad31516aa6…` · 架构 `x86` · 子系统 `2` · 入口 `0x2b8c04` · 时间戳 `1617956270`
- 版本信息: CompanyName=`Sysceo.com` · FileDescription=`ScDeployBG_x86` · FileVersion=`3.0.0.119` · LegalCopyright=`Copyright © sysceo.com All Rights Reserved.` · ProductName=`ScDeployBG_x86` · ProductVersion=`3.0.0.119` · Comments=`ScDeployBG_x86`
- 节区(11): `.text`, `.itext`, `.data`, `.bss`, `.idata`, `.didata`, `.edata`, `.tls`, `.rdata`, `.reloc`, `.rsrc`
- 导入(12 DLL): `KERNEL32.DLL`(125), `advapi32.dll`(17), `comctl32.dll`(35), `gdi32.dll`(96), `msvcrt.dll`(2), `ole32.dll`(9), `oleaut32.dll`(3), `shell32.dll`(1), `shlwapi.dll`(1), `user32.dll`(5), `version.dll`(3), `winspool.drv`(1)
- 导出(1): `TMethodImplementationIntercept`
- 资源: CURSOR×7, GROUP_CURSOR×7, GROUP_ICON×1, ICON×10, MANIFEST×1, RCDATA×4, STRING×32, VERSION×1
- RCDATA 条目(4): `DVCLAL`, `PACKAGEINFO`, `PLATFORMTARGETS`, `TSCBG`
- 内含 DLL 名: `DWMAPI.DLL`, `Fwpuclnt.dll`, `IdnDL.dll`, `KERNEL32.DLL`, `Kernel32.dll`, `MSWSOCK.DLL`, `NTDLL.DLL`, `Normaliz.dll`, `PSAPI.dll`, `SetupApi.dll`, `WS2_32.DLL`, `Wship6.dll`, `advapi32.dll`, `comctl32.dll`
- 字符串总数 `33911`；关键词命中: OEM×33, sysprep×3, 任务栏×17, 总裁系×13, 浏览器×2, 虚拟机×3, 部署×19, 驱动×8
  - 浏览器: `Monochrome` | `lrMonoChrome`
  - sysprep: `SetupCloseFileQueue` | `SetupCloseInfFile` | `SetupCloseLog`
  - 驱动: ` TArray<System.SysUtils.TLangRec>` | `&TArray<System.SysUtils.TUnitHashEntry>` | `/TArray<System.SysUtils.TMarshaller.TDisposeRec>` | `SRSynchronous`
  - 部署: `DecryptScdata` | `Deploy` | `DeployFontcolour` | `Error:Scdata.sc file missing!`
  - OEM: `&TArray<uSMBIOS.TOEMStringsInformation>` | `+TArray<uSMBIOS_XP.TOEMStringsInformationXP>` | `AutoOembg` | `FOEMConvert`
  - 任务栏: `FMainFormOnTaskBar` | `FTaskbarHandler` | `MainFormOnTaskBar` | `NSystem.Win.TaskbarCore`
  - 总裁系: `Copyright © sysceo.com All Rights Reserved.` | `E:\Data\Sysceo\SC\SC3.0\Sc3.0\Zip\AbDfBase.pas` | `E:\Data\Sysceo\SC\SC3.0\Sc3.0\Zip\AbDfCryS.pas` | `E:\Data\Sysceo\SC\SC3.0\Sc3.0\Zip\AbDfDec.pas`
  - 虚拟机: `VMware, Inc.` | `VirtualBox` | `VmWare`

### `FUNOX64`
- 大小 `5,459,968` · sha256 `ab9a0dca866b80ea…` · 架构 `x64` · 子系统 `2` · 入口 `0x43ce20` · 时间戳 `1617956286`
- 版本信息: CompanyName=`Sysceo.com` · FileDescription=`ScDeployBG_x64` · FileVersion=`3.0.0.119` · LegalCopyright=`Copyright © sysceo.com All Rights Reserved.` · ProductName=`ScDeployBG_x64` · ProductVersion=`3.0.0.119` · Comments=`ScDeployBG_x64`
- 节区(11): `.text`, `.data`, `.bss`, `.idata`, `.didata`, `.edata`, `.tls`, `.rdata`, `.reloc`, `.pdata`, `.rsrc`
- 导入(12 DLL): `KERNEL32.DLL`(123), `advapi32.dll`(17), `comctl32.dll`(35), `gdi32.dll`(96), `msvcrt.dll`(2), `ole32.dll`(9), `oleaut32.dll`(3), `shell32.dll`(1), `shlwapi.dll`(1), `user32.dll`(5), `version.dll`(3), `winspool.drv`(1)
- 导出(3): `TMethodImplementationIntercept`, `__dbk_fcall_wrapper`, `dbkFCallWrapperAddr`
- 资源: CURSOR×7, GROUP_CURSOR×7, GROUP_ICON×1, ICON×10, MANIFEST×1, RCDATA×4, STRING×32, VERSION×1
- RCDATA 条目(4): `DVCLAL`, `PACKAGEINFO`, `PLATFORMTARGETS`, `TSCBG`
- 内含 DLL 名: `DWMAPI.DLL`, `Fwpuclnt.dll`, `IdnDL.dll`, `KERNEL32.DLL`, `MSWSOCK.DLL`, `NTDLL.DLL`, `Normaliz.dll`, `SetupApi.dll`, `User32.dll`, `WS2_32.DLL`, `Wship6.dll`, `advapi32.dll`, `comctl32.dll`, `gdi32.dll`
- 字符串总数 `46418`；关键词命中: OEM×33, sysprep×3, 任务栏×17, 总裁系×13, 浏览器×2, 虚拟机×3, 部署×19, 驱动×9
  - 浏览器: `Monochrome` | `lrMonoChrome`
  - sysprep: `SetupCloseFileQueue` | `SetupCloseInfFile` | `SetupCloseLog`
  - 驱动: ` TArray<System.SysUtils.TLangRec>` | `&TArray<System.SysUtils.TUnitHashEntry>(` | `/TArray<System.SysUtils.TMarshaller.TDisposeRec> ` | `SRSynchronous`
  - 部署: `DecryptScdata` | `Deploy` | `DeployFontcolour` | `Error:Scdata.sc file missing!`
  - OEM: `&TArray<uSMBIOS.TOEMStringsInformation>` | `+TArray<uSMBIOS_XP.TOEMStringsInformationXP>` | `AutoOembg` | `FOEMConvert`
  - 任务栏: `FMainFormOnTaskBar` | `FTaskbarHandler` | `MainFormOnTaskBar` | `NSystem.Win.TaskbarCore`
  - 总裁系: `Copyright © sysceo.com All Rights Reserved.` | `E:\Data\Sysceo\SC\SC3.0\Sc3.0\Zip\AbDfBase.pas` | `E:\Data\Sysceo\SC\SC3.0\Sc3.0\Zip\AbDfCryS.pas` | `E:\Data\Sysceo\SC\SC3.0\Sc3.0\Zip\AbDfDec.pas`
  - 虚拟机: `VMware, Inc.` | `VirtualBox` | `VmWare`

### `FUNP`
- 大小 `4,619,776` · sha256 `88f9e5b83904ba17…` · 架构 `x86` · 子系统 `2` · 入口 `0x36a718` · 时间戳 `1617963658`
- 版本信息: CompanyName=`Sysceo.com` · FileDescription=`ScProcessBar_x86` · FileVersion=`3.0.0.6` · LegalCopyright=`Copyright © sysceo.com All Rights Reserved.` · ProductName=`ScProcessBar_x86` · ProductVersion=`3.0.0.6` · Comments=`ScProcessBar`
- 节区(11): `.text`, `.itext`, `.data`, `.bss`, `.idata`, `.didata`, `.edata`, `.tls`, `.rdata`, `.reloc`, `.rsrc`
- 导入(13 DLL): `KERNEL32.DLL`(1), `advapi32.dll`(3), `comctl32.dll`(35), `gdi32.dll`(101), `gdiplus.dll`(555), `msvcrt.dll`(2), `ole32.dll`(8), `oleaut32.dll`(3), `shell32.dll`(1), `user32.dll`(5), `version.dll`(3), `wininet.dll`(4), `winspool.drv`(1)
- 导出(1): `TMethodImplementationIntercept`
- 资源: BITMAP×10, CURSOR×7, GROUP_CURSOR×7, GROUP_ICON×1, ICON×10, MANIFEST×1, RCDATA×6, STRING×38, TESTDATA×1, VERSION×1
- RCDATA 条目(6): `DVCLAL`, `MLSKINREGISTERHINT`, `PACKAGEINFO`, `PLATFORMTARGETS`, `TMLSKINRESDM`, `TSCPB`
- 内含 DLL 名: `DWMAPI.DLL`, `DWRITE.DLL`, `Fwpuclnt.dll`, `IdnDL.dll`, `KERNEL32.DLL`, `Kernel32.dll`, `MSWSOCK.DLL`, `NTDLL.DLL`, `Normaliz.dll`, `PSAPI.dll`, `WS2_32.DLL`, `Wship6.dll`, `advapi32.dll`, `comctl32.dll`
- 字符串总数 `43504`；关键词命中: OEM×5, sysprep×1, 任务栏×21, 总裁系×19, 推广×1, 浏览器×2, 部署×20, 驱动×7
  - 浏览器: `Monochromeh` | `lrMonoChrome`
  - sysprep: `oobe\windeploy.exe`
  - 驱动: ` TArray<System.SysUtils.TLangRec>` | `&TArray<System.SysUtils.TUnitHashEntry>` | `/TArray<System.SysUtils.TMarshaller.TDisposeRec>` | `System.SysConst`
  - 部署: `-Edeploy` | `/Edeploy` | `DecryptScdata` | `Deploy`
  - OEM: `FOEMConvert` | `GetOEMCP` | `OEMConvert` | `OEM_CHARSET`
  - 任务栏: `FHideInTaskbar` | `FMainFormOnTaskBar` | `FMinimizeToTaskbar` | `FTaskbarHandler`
  - 总裁系: `Copyright © sysceo.com All Rights Reserved.` | `E:\Data\Sysceo\SC\SC3.0\SC3.0\XESkin\Graphics32\GR32.pas` | `E:\Data\Sysceo\SC\SC3.0\SC3.0\XESkin\Graphics32\GR32_Layers.pas` | `E:\Data\Sysceo\SC\SC3.0\SC3.0\XESkin\Graphics32\GR32_PortableNetworkGr`
  - 推广: `cmUnion`

### `FUNQ`
- 大小 `1,170,864` · sha256 `575b075ef43430c0…` · 架构 `x86` · 子系统 `2` · 入口 `0x3ef001` · 时间戳 `1543070722`
- 版本信息: CompanyName=`Sysceo.com` · FileDescription=`Scaddnet` · FileVersion=`3.0.0.0` · LegalCopyright=`Copyright © sysceo.com All Rights Reserved.` · ProductName=`Scaddnet` · ProductVersion=`3.0.0.0` · Comments=`Scaddnet`
- 节区(13): `.text`, `.itext`, `.data`, `.bss`, `.idata`, `.didata`, `.edata`, `.tls`, `.rdata`, `.reloc`, `.rsrc`, `.aspack`, `.adata`
- 导入(13 DLL): `advapi32.dll`(1), `comctl32.dll`(1), `gdi32.dll`(1), `gdiplus.dll`(1), `kernel32.dll`(3), `msvcrt.dll`(1), `ole32.dll`(1), `oleaut32.dll`(1), `shell32.dll`(1), `user32.dll`(1), `version.dll`(1), `wininet.dll`(1), `winspool.drv`(1)
- 导出(1): `TMethodImplementationIntercept`
- 资源: BHLJ×6, CURSOR×7, GROUP_CURSOR×7, GROUP_ICON×1, ICON×4, MANIFEST×1, RCDATA×6, STRING×27, TESTDATA×1, VERSION×1
- RCDATA 条目(6): `DVCLAL`, `MLSKINREGISTERHINT`, `PACKAGEINFO`, `PLATFORMTARGETS`, `TMLSKINRESDM`, `TSCCNET`
- 内含 DLL 名: `advapi32.dll`, `comctl32.dll`, `gdi32.dll`, `gdiplus.dll`, `kernel32.dll`, `msvcrt.dll`, `ole32.dll`, `oleaut32.dll`, `shell32.dll`, `user32.dll`, `version.dll`, `wininet.dll`
- URL: `http://ocsp.digicert.com0A`, `http://ocsp.digicert.com0C`, `http://ocsp.digicert.com0H`, `http://ocsp.digicert.com0I`, `http://ocsp.digicert.com0O`
- 字符串总数 `2182`；关键词命中: 总裁系×2
  - 总裁系: `Copyright © sysceo.com All Rights Reserved.` | `Sysceo.com`

### `FUNR`
- 大小 `5,930,280` · sha256 `6b36de43e05c8f66…` · 架构 `x86` · 子系统 `2` · 入口 `0x384c9c` · 时间戳 `1524204982`
- 版本信息: CompanyName=`SysCeo.com` · FileDescription=`驱动总裁在线安装程序` · FileVersion=`1.7.0.0` · LegalCopyright=`Copyright © 江门市易云网络有限公司 All Rights Reserved.` · ProductName=`驱动总裁在线安装程序` · ProductVersion=`1.7.0.0` · Comments=`驱动总裁在线安装程序`
- 节区(11): `.text`, `.itext`, `.data`, `.bss`, `.idata`, `.didata`, `.edata`, `.tls`, `.rdata`, `.reloc`, `.rsrc`
- 导入(13 DLL): `KERNEL32.DLL`(1), `advapi32.dll`(17), `comctl32.dll`(35), `gdi32.dll`(101), `gdiplus.dll`(555), `msvcrt.dll`(2), `ole32.dll`(8), `oleaut32.dll`(3), `shell32.dll`(2), `user32.dll`(5), `version.dll`(3), `wininet.dll`(4), `winspool.drv`(1)
- 导出(1): `TMethodImplementationIntercept`
- 资源: BITMAP×10, CURSOR×7, GROUP_CURSOR×7, GROUP_ICON×1, ICON×10, MANIFEST×1, RCDATA×6, STRING×45, TESTDATA×1, VERSION×1
- RCDATA 条目(6): `DVCLAL`, `MLSKINREGISTERHINT`, `PACKAGEINFO`, `PLATFORMTARGETS`, `TMLSKINRESDM`, `TONLINESETUP`
- 内含 DLL 名: `DWMAPI.DLL`, `DWRITE.DLL`, `Fwpuclnt.dll`, `IdnDL.dll`, `KERNEL32.DLL`, `Kernel32.dll`, `MSWSOCK.DLL`, `Normaliz.dll`, `WS2_32.DLL`, `Wship6.dll`, `advapi32.dll`, `comctl32.dll`, `d2d1.dll`, `gdi32.dll`
- URL: `http://crls1.wosign.com/ca1.crl0h`, `http://drvceoup.sysceo.cn/DCAPI/DrvCeooLinstaller.exe`, `http://ocsp.digicert.com0C`, `http://ocsp.digicert.com0H`, `http://ocsp.digicert.com0I`
- 字符串总数 `47036`；关键词命中: OEM×3, sysprep×3, 任务栏×22, 总裁系×10, 推广×2, 浏览器×2, 驱动×9
  - 浏览器: `Monochrome` | `lrMonoChrome`
  - sysprep: `Btn_SetupClick` | `PASN1_GENERALIZEDTIMEP;p` | `generalizedtime`
  - 驱动: ` TArray<System.SysUtils.TLangRec>` | `&TArray<System.SysUtils.TUnitHashEntry>` | `/TArray<System.SysUtils.TMarshaller.TDisposeRec>` | `System.SysConst`
  - OEM: `FOEMConvert` | `OEMConvert` | `OEM_CHARSET`
  - 任务栏: `FHideInTaskbar` | `FMainFormOnTaskBar` | `FMinimizeToTaskbar` | `FTaskbarHandler`
  - 总裁系: `E:\Data\Sysceo\Dc\Dcinst\XESkin\Graphics32\GR32.pas` | `E:\Data\Sysceo\Dc\Dcinst\XESkin\Graphics32\GR32_Layers.pas` | `E:\Data\Sysceo\Dc\Dcinst\XESkin\Graphics32\GR32_PortableNetworkGraphic` | `E:\Data\Sysceo\Dc\Dcinst\XESkin\Graphics32\GR32_Resamplers.pas`
  - 推广: `EVP_PKEY_union` | `cmUnion`

### `FUNS`
- 大小 `5,952,624` · sha256 `76aeaee3a814f327…` · 架构 `x86` · 子系统 `2` · 入口 `0x384c9c` · 时间戳 `1665552255`
- 版本信息: CompanyName=`SysCeo.com` · FileDescription=`软件魔盒在线安装程序` · FileVersion=`2.0.0.0` · LegalCopyright=`Copyright (C) 2012-2022 Jiangmen Eyun Network Co.,Ltd.` · ProductName=`软件魔盒在线安装程序` · ProductVersion=`2.0.0.0` · Comments=`软件魔盒在线安装程序`
- 节区(11): `.text`, `.itext`, `.data`, `.bss`, `.idata`, `.didata`, `.edata`, `.tls`, `.rdata`, `.reloc`, `.rsrc`
- 导入(13 DLL): `KERNEL32.DLL`(1), `advapi32.dll`(17), `comctl32.dll`(35), `gdi32.dll`(101), `gdiplus.dll`(555), `msvcrt.dll`(2), `ole32.dll`(8), `oleaut32.dll`(3), `shell32.dll`(2), `user32.dll`(5), `version.dll`(3), `wininet.dll`(4), `winspool.drv`(1)
- 导出(1): `TMethodImplementationIntercept`
- 资源: BITMAP×10, CURSOR×7, GROUP_CURSOR×7, GROUP_ICON×1, ICON×11, MANIFEST×1, RCDATA×6, STRING×45, TESTDATA×1, VERSION×1
- RCDATA 条目(6): `DVCLAL`, `MLSKINREGISTERHINT`, `PACKAGEINFO`, `PLATFORMTARGETS`, `TMLSKINRESDM`, `TONLINESETUP`
- 内含 DLL 名: `DWMAPI.DLL`, `DWRITE.DLL`, `Fwpuclnt.dll`, `IdnDL.dll`, `KERNEL32.DLL`, `Kernel32.dll`, `MSWSOCK.DLL`, `Normaliz.dll`, `WS2_32.DLL`, `Wship6.dll`, `advapi32.dll`, `comctl32.dll`, `d2d1.dll`, `gdi32.dll`
- URL: `http://mbox.shanbotv.com/mbox/AppBoxSetup.exe`, `http://ocsp.digicert.com0A`, `http://ocsp.digicert.com0C`, `http://ocsp.digicert.com0H`, `http://ocsp.digicert.com0I`
- 字符串总数 `47076`；关键词命中: OEM×3, sysprep×3, 任务栏×21, 总裁系×9, 推广×15, 浏览器×2, 驱动×8
  - 浏览器: `Monochromed]P` | `lrMonoChrome`
  - sysprep: `Btn_SetupClick` | `PASN1_GENERALIZEDTIME` | `generalizedtime`
  - 驱动: ` TArray<System.SysUtils.TLangRec>` | `&TArray<System.SysUtils.TUnitHashEntry>` | `/TArray<System.SysUtils.TMarshaller.TDisposeRec>` | `System.SysConst`
  - OEM: `FOEMConvert` | `OEMConvert` | `OEM_CHARSET`
  - 任务栏: `FHideInTaskbar` | `FMainFormOnTaskBar` | `FMinimizeToTaskbar` | `FTaskbarHandler`
  - 总裁系: `E:\Data\Sysceo\CeoMbox\mbolinst\XESkin\Graphics32\GR32.pas` | `E:\Data\Sysceo\CeoMbox\mbolinst\XESkin\Graphics32\GR32_Layers.pas` | `E:\Data\Sysceo\CeoMbox\mbolinst\XESkin\Graphics32\GR32_PortableNetwork` | `E:\Data\Sysceo\CeoMbox\mbolinst\XESkin\Graphics32\GR32_Resamplers.pas`
  - 推广: `E:\Data\Sysceo\CeoMbox\mbolinst\XESkin\Graphics32\GR32.pas` | `E:\Data\Sysceo\CeoMbox\mbolinst\XESkin\Graphics32\GR32_Layers.pas` | `E:\Data\Sysceo\CeoMbox\mbolinst\XESkin\Graphics32\GR32_PortableNetwork` | `E:\Data\Sysceo\CeoMbox\mbolinst\XESkin\Graphics32\GR32_Resamplers.pas`

### `FUNT`
- 大小 `480,688` · sha256 `9b5dbdf94d192365…` · 架构 `x86` · 子系统 `2` · 入口 `0x4d490` · 时间戳 `708992537`
- 版本信息: CompanyName=`Www.SysCeo.Com` · FileDescription=`ScClosemsbox` · FileVersion=`3.0.0.0` · LegalCopyright=`*LegalTrademarks` · ProductVersion=`1.0.0.0` · Comments=`D`
- 节区(8): `CODE`, `DATA`, `BSS`, `.idata`, `.tls`, `.rdata`, `.reloc`, `.rsrc`
- 导入(7 DLL): `KERNEL32.DLL`(34), `advapi32.dll`(3), `comctl32.dll`(22), `gdi32.dll`(54), `oleaut32.dll`(3), `user32.dll`(4), `version.dll`(3)
- 资源: BITMAP×11, CURSOR×7, DIALOG×1, GROUP_CURSOR×7, GROUP_ICON×1, ICON×9, RCDATA×3, STRING×16, VERSION×1
- RCDATA 条目(3): `DVCLAL`, `PACKAGEINFO`, `TCMSB`
- 内含 DLL 名: `KERNEL32.DLL`, `MAPI32.DLL`, `USER32.DLL`, `User32.dll`, `advapi32.dll`, `comctl32.dll`, `gdi32.dll`, `imm32.dll`, `kernel32.dll`, `oleaut32.dll`, `user32.dll`, `uxtheme.dll`, `vcltest3.dll`, `version.dll`
- URL: `http://ocsp.digicert.com0A`, `http://ocsp.digicert.com0C`, `http://ocsp.digicert.com0H`, `http://ocsp.digicert.com0I`, `http://ocsp.digicert.com0O`
- 字符串总数 `3890`；关键词命中: OEM×3, 任务栏×2, 总裁系×1, 驱动×1
  - 驱动: `Www.SysCeo.Com`
  - OEM: `CharToOemA` | `OEM_CHARSET` | `OemToCharA`
  - 任务栏: `TaskbarCreated` | `taskbar`
  - 总裁系: `Www.SysCeo.Com`

### `FUNU`
- 大小 `484,784` · sha256 `c946741dd5750901…` · 架构 `x86` · 子系统 `2` · 入口 `0x4c99c` · 时间戳 `708992537`
- 版本信息: CompanyName=`SysCeo.Com` · FileDescription=`By:Noime` · FileVersion=`3.0.0.0` · LegalCopyright=`SysCeo.Com` · ProductVersion=`1.0.0.0`
- 节区(8): `CODE`, `DATA`, `BSS`, `.idata`, `.tls`, `.rdata`, `.reloc`, `.rsrc`
- 导入(7 DLL): `KERNEL32.DLL`(34), `advapi32.dll`(3), `comctl32.dll`(22), `gdi32.dll`(54), `oleaut32.dll`(3), `user32.dll`(4), `version.dll`(3)
- 资源: BITMAP×11, CURSOR×7, DIALOG×1, GROUP_CURSOR×7, GROUP_ICON×1, ICON×5, RCDATA×3, STRING×16, VERSION×1
- RCDATA 条目(3): `DVCLAL`, `PACKAGEINFO`, `PLATFORMTARGETS`
- 内含 DLL 名: `KERNEL32.DLL`, `MAPI32.DLL`, `USER32.DLL`, `User32.dll`, `advapi32.dll`, `comctl32.dll`, `gdi32.dll`, `imm32.dll`, `kernel32.dll`, `noime.dll`, `oleaut32.dll`, `user32.dll`, `uxtheme.dll`, `vcltest3.dll`
- URL: `http://ocsp.digicert.com0A`, `http://ocsp.digicert.com0C`, `http://ocsp.digicert.com0H`, `http://ocsp.digicert.com0I`, `http://ocsp.digicert.com0O`
- 字符串总数 `3890`；关键词命中: OEM×3, 任务栏×2, 总裁系×1
  - OEM: `CharToOemA` | `OEM_CHARSET` | `OemToCharA`
  - 任务栏: `TaskbarCreated` | `taskbar`
  - 总裁系: `SysCeo.Com`

### `FUNV`
- 大小 `6,569,564` · sha256 `ea45ec22ce0ec891…` · 架构 `-` · 子系统 `-` · 入口 `-` · 时间戳 `-`
- 版本信息: 无
- 节区(0): 
- 导入(0 DLL): 
- 字符串总数 `11683`；关键词命中: OEM×320, 总裁系×11, 虚拟机×11, 驱动×1
  - 驱动: `SrS\n `
  - OEM: `Scoem/` | `Scoem/Acer/` | `Scoem/Acer/PK` | `Scoem/Acer/Thumbs.db`
  - 总裁系: `Scoem/Sysceo/` | `Scoem/Sysceo/PK` | `Scoem/Sysceo/Thumbs.db` | `Scoem/Sysceo/nt5.bmp`
  - 虚拟机: `Scoem/VmWare/` | `Scoem/VmWare/PK` | `Scoem/VmWare/bg.jpg` | `Scoem/VmWare/bg.jpg"`

### `FUNX`
- 大小 `3,683,760` · sha256 `38696fe0ffcda9f1…` · 架构 `x86` · 子系统 `2` · 入口 `0x29cb34` · 时间戳 `1525274169`
- 版本信息: CompanyName=`Sysceo.com` · FileDescription=`Scskipwlan` · FileVersion=`3.0.0.2` · LegalCopyright=`Copyright © sysceo.com All Rights Reserved.` · ProductName=`Scskipwlan` · ProductVersion=`3.0.0.2` · Comments=`Scskipwlan`
- 节区(11): `.text`, `.itext`, `.data`, `.bss`, `.idata`, `.didata`, `.edata`, `.tls`, `.rdata`, `.reloc`, `.rsrc`
- 导入(13 DLL): `KERNEL32.DLL`(1), `advapi32.dll`(17), `comctl32.dll`(35), `gdi32.dll`(101), `gdiplus.dll`(555), `msvcrt.dll`(2), `ole32.dll`(8), `oleaut32.dll`(3), `shell32.dll`(1), `user32.dll`(5), `version.dll`(3), `wininet.dll`(4), `winspool.drv`(1)
- 导出(1): `TMethodImplementationIntercept`
- 资源: CURSOR×7, GROUP_CURSOR×7, GROUP_ICON×1, ICON×10, MANIFEST×1, RCDATA×6, STRING×27, TESTDATA×1, VERSION×1
- RCDATA 条目(6): `DVCLAL`, `MLSKINREGISTERHINT`, `PACKAGEINFO`, `PLATFORMTARGETS`, `TMLSKINRESDM`, `TSWLAN`
- 内含 DLL 名: `DWMAPI.DLL`, `KERNEL32.DLL`, `advapi32.dll`, `comctl32.dll`, `gdi32.dll`, `gdiplus.dll`, `imm32.dll`, `kernel32.dll`, `msimg32.dll`, `msvcrt.dll`, `ole32.dll`, `oleaut32.dll`, `shell32.dll`, `user32.dll`
- URL: `http://ocsp.digicert.com0A`, `http://ocsp.digicert.com0C`, `http://ocsp.digicert.com0H`, `http://ocsp.digicert.com0I`, `http://ocsp.digicert.com0O`
- 字符串总数 `35397`；关键词命中: OEM×3, 任务栏×21, 总裁系×2, 推广×1, 浏览器×2, 部署×3, 驱动×7
  - 浏览器: `Monochrome` | `lrMonoChrome`
  - 驱动: ` TArray<System.SysUtils.TLangRec>` | `&TArray<System.SysUtils.TUnitHashEntry>` | `/TArray<System.SysUtils.TMarshaller.TDisposeRec>` | `System.SysConst`
  - 部署: `RUNONCE.exe` | `ScDeploy.exe` | `ScTasks.exe`
  - OEM: `FOEMConvert` | `OEMConvert` | `OEM_CHARSET`
  - 任务栏: `FHideInTaskbar` | `FMainFormOnTaskBar` | `FMinimizeToTaskbar` | `FTaskbarHandler`
  - 总裁系: `Copyright © sysceo.com All Rights Reserved.` | `Sysceo.com`
  - 推广: `cmUnion`

### `FUNY`
- 大小 `564,736` · sha256 `a8df92be162e7503…` · 架构 `x86` · 子系统 `2` · 入口 `0x662ac` · 时间戳 `708992537`
- 版本信息: CompanyName=`SysCeo.Com` · FileDescription=`ScSFC` · FileVersion=`3.0.0.0` · InternalName=`ScSFC` · LegalCopyright=`Copyright ? sysceo.com All Rights Reserved.` · OriginalFilename=`ScSFC` · ProductName=`ScSFC` · ProductVersion=`3.0.0.0` · Comments=`SysCeo.Com`
- 节区(8): `CODE`, `DATA`, `BSS`, `.idata`, `.tls`, `.rdata`, `.reloc`, `.rsrc`
- 导入(8 DLL): `KERNEL32.DLL`(34), `advapi32.dll`(3), `comctl32.dll`(23), `gdi32.dll`(65), `oleaut32.dll`(3), `sfcfiles.dll`(1), `user32.dll`(4), `version.dll`(3)
- 资源: BITMAP×11, CURSOR×7, DIALOG×1, GROUP_CURSOR×7, GROUP_ICON×1, ICON×10, RCDATA×3, STRING×17, VERSION×1
- RCDATA 条目(3): `DVCLAL`, `PACKAGEINFO`, `TFORM1`
- 内含 DLL 名: `KERNEL32.DLL`, `MAPI32.DLL`, `USER32.DLL`, `User32.dll`, `advapi32.dll`, `comctl32.dll`, `gdi32.dll`, `imm32.dll`, `kernel32.dll`, `oleaut32.dll`, `sfcfiles.dll`, `user32.dll`, `uxtheme.dll`, `vcltest3.dll`
- 字符串总数 `4950`；关键词命中: OEM×3, 任务栏×2, 总裁系×2, 部署×2
  - 部署: `ScDeploy.exe` | `ScTasks.exe`
  - OEM: `CharToOemA` | `OEM_CHARSET` | `OemToCharA`
  - 任务栏: `TaskbarCreated` | `taskbar`
  - 总裁系: `Copyright ? sysceo.com All Rights Reserved.` | `SysCeo.Com`

### `FUNZ`
- 大小 `445,040` · sha256 `87870503a4c8d861…` · 架构 `x86` · 子系统 `2` · 入口 `0x1000` · 时间戳 `1154756066`
- 版本信息: 无
- 节区(4): `.text`, `.data`, `.idata`, `.rsrc`
- 导入(8 DLL): `ADVAPI32.DLL`(10), `COMCTL32.DLL`(1), `COMDLG32.DLL`(2), `GDI32.DLL`(1), `KERNEL32.DLL`(67), `OLE32.DLL`(5), `SHELL32.DLL`(8), `USER32.DLL`(52)
- 资源: BITMAP×1, DIALOG×6, GROUP_ICON×1, ICON×4, MANIFEST×1, RCDATA×1, STRING×4
- RCDATA 条目(1): `DVCLAL`
- 内含 DLL 名: `ADVAPI32.DLL`, `COMCTL32.DLL`, `COMDLG32.DLL`, `GDI32.DLL`, `KERNEL32.DLL`, `OLE32.DLL`, `SHELL32.DLL`, `USER32.DLL`, `riched20.dll`, `riched32.dll`, `shlwapi.dll`
- 字符串总数 `1827`；关键词命中: OEM×4
  - OEM: `CharToOemA` | `CharToOemBuffA` | `OemToCharA` | `OemToCharBuffA`

### `PUBCA`
- 大小 `4,647,936` · sha256 `c4007071eb19ea52…` · 架构 `x86` · 子系统 `2` · 入口 `0x36c720` · 时间戳 `1617963556`
- 版本信息: CompanyName=`Sysceo.com` · FileDescription=`ScColourProcessBar_x86` · FileVersion=`3.0.0.6` · LegalCopyright=`Copyright © sysceo.com All Rights Reserved.` · ProductName=`ScColourProcessBar_x86` · ProductVersion=`3.0.0.6` · Comments=`ScColourProcessBar`
- 节区(11): `.text`, `.itext`, `.data`, `.bss`, `.idata`, `.didata`, `.edata`, `.tls`, `.rdata`, `.reloc`, `.rsrc`
- 导入(14 DLL): `KERNEL32.DLL`(129), `advapi32.dll`(17), `comctl32.dll`(35), `gdi32.dll`(101), `gdiplus.dll`(555), `msvcrt.dll`(2), `ole32.dll`(8), `oleaut32.dll`(3), `shell32.dll`(2), `shlwapi.dll`(1), `user32.dll`(5), `version.dll`(3), `wininet.dll`(4), `winspool.drv`(1)
- 导出(1): `TMethodImplementationIntercept`
- 资源: BITMAP×10, CURSOR×7, GROUP_CURSOR×7, GROUP_ICON×1, ICON×10, MANIFEST×1, RCDATA×6, STRING×38, TESTDATA×1, VERSION×1
- RCDATA 条目(6): `DVCLAL`, `MLSKINREGISTERHINT`, `PACKAGEINFO`, `PLATFORMTARGETS`, `TMLSKINRESDM`, `TSCPB`
- 内含 DLL 名: `DWMAPI.DLL`, `DWRITE.DLL`, `Fwpuclnt.dll`, `IdnDL.dll`, `KERNEL32.DLL`, `Kernel32.dll`, `MSWSOCK.DLL`, `NTDLL.DLL`, `Normaliz.dll`, `PSAPI.dll`, `WS2_32.DLL`, `Wship6.dll`, `advapi32.dll`, `comctl32.dll`
- 字符串总数 `43166`；关键词命中: OEM×5, sysprep×1, 任务栏×21, 总裁系×19, 推广×1, 浏览器×2, 部署×20, 驱动×7
  - 浏览器: `Monochrome` | `lrMonoChrome`
  - sysprep: `oobe\windeploy.exe`
  - 驱动: ` TArray<System.SysUtils.TLangRec>` | `&TArray<System.SysUtils.TUnitHashEntry>` | `/TArray<System.SysUtils.TMarshaller.TDisposeRec>` | `System.SysConst`
  - 部署: `-Edeploy` | `/Edeploy` | `DecryptScdata` | `Deploy`
  - OEM: `FOEMConvert` | `GetOEMCP` | `OEMConvert` | `OEM_CHARSET`
  - 任务栏: `FHideInTaskbar` | `FMainFormOnTaskBar` | `FMinimizeToTaskbar` | `FTaskbarHandler`
  - 总裁系: `Copyright © sysceo.com All Rights Reserved.` | `E:\Data\Sysceo\SC\SC3.0\SC3.0\XESkin\Graphics32\GR32.pas` | `E:\Data\Sysceo\SC\SC3.0\SC3.0\XESkin\Graphics32\GR32_Layers.pas` | `E:\Data\Sysceo\SC\SC3.0\SC3.0\XESkin\Graphics32\GR32_PortableNetworkGr`
  - 推广: `cmUnion`

### `PUBCB`
- 大小 `15,480` · sha256 `d837de0fd9b30d65…` · 架构 `x86` · 子系统 `1` · 入口 `0x403e` · 时间戳 `1538034381`
- 版本信息: Comments=`Written by  Windows Printing & Imaging Team` · CompanyName=`Microsoft Corporation` · FileDescription=`Microsoft Application Virtualization OEMUI` · FileVersion=`6, 1, 7600, 16396` · InternalName=`OEMUI` · LegalCopyright=`© Microsoft Corporation. All rights reserved.` · OriginalFilename=`OEMUI.dll` · ProductName=`Microsoft® Windows® Operating System` · ProductVersion=`6.1.7600.16396`
- 节区(6): `.text`, `.rdata`, `.data`, `INIT`, `.rsrc`, `.reloc`
- 导入(1 DLL): `ntoskrnl.exe`(11)
- 资源: VERSION×1
- PDB: `e:\data\sysceo\sc\sc3.0\sc3.0\driver\nt6\objfre_win7_x86\i386\scdrv.pdb`
- 内含 DLL 名: `OEMUI.dll`
- 字符串总数 `144`；关键词命中: OEM×2, sysprep×1, 伪装×4, 总裁系×1, 驱动×1
  - sysprep: `牄癩牥甠汮慯੤찀OOBEInProgress`
  - 驱动: `e:\data\sysceo\sc\sc3.0\sc3.0\driver\nt6\objfre_win7_x86\i386\scdrv.pd`
  - OEM: `Microsoft Application Virtualization OEMUI` | `OEMUI.dll`
  - 总裁系: `e:\data\sysceo\sc\sc3.0\sc3.0\driver\nt6\objfre_win7_x86\i386\scdrv.pd`
  - 伪装: `Microsoft Time-Stamp PCA 2010` | `Microsoft Time-Stamp PCA 20100` | `Microsoft Time-Stamp Service` | `Microsoft Time-Stamp Service0`

### `PUBCC`
- 大小 `16,504` · sha256 `8d4f7da9691b6737…` · 架构 `x64` · 子系统 `1` · 入口 `0x5064` · 时间戳 `1538034298`
- 版本信息: Comments=`Written by  Windows Printing & Imaging Team` · CompanyName=`Microsoft Corporation` · FileDescription=`Microsoft Application Virtualization OEMUI` · FileVersion=`6, 1, 7600, 16396` · InternalName=`OEMUI` · LegalCopyright=`© Microsoft Corporation. All rights reserved.` · OriginalFilename=`OEMUI.dll` · ProductName=`Microsoft® Windows® Operating System` · ProductVersion=`6.1.7600.16396`
- 节区(6): `.text`, `.rdata`, `.data`, `.pdata`, `INIT`, `.rsrc`
- 导入(1 DLL): `ntoskrnl.exe`(9)
- 资源: VERSION×1
- PDB: `e:\data\sysceo\sc\sc3.0\sc3.0\driver\nt6\objfre_win7_amd64\amd64\scdrv.pdb`
- 内含 DLL 名: `OEMUI.dll`
- 字符串总数 `168`；关键词命中: OEM×2, sysprep×1, 伪装×4, 总裁系×1, 驱动×1
  - sysprep: `쳌쳌쳌쳌쳌OOBEInProgress`
  - 驱动: `e:\data\sysceo\sc\sc3.0\sc3.0\driver\nt6\objfre_win7_amd64\amd64\scdrv`
  - OEM: `Microsoft Application Virtualization OEMUI` | `OEMUI.dll`
  - 总裁系: `e:\data\sysceo\sc\sc3.0\sc3.0\driver\nt6\objfre_win7_amd64\amd64\scdrv`
  - 伪装: `Microsoft Time-Stamp PCA 2010` | `Microsoft Time-Stamp PCA 20100` | `Microsoft Time-Stamp Service` | `Microsoft Time-Stamp Service0`

### `PUBCD`
- 大小 `30,744` · sha256 `78b2078a994ad1b0…` · 架构 `x86` · 子系统 `1` · 入口 `0x403e` · 时间戳 `1525937523`
- 版本信息: Comments=`Written by  Windows Printing & Imaging Team` · CompanyName=`Microsoft Corporation` · FileDescription=`Microsoft Application Virtualization OEMUI` · FileVersion=`6, 1, 7600, 16396` · InternalName=`OEMUI` · LegalCopyright=`© Microsoft Corporation. All rights reserved.` · OriginalFilename=`OEMUI.dll` · ProductName=`Microsoft® Windows® Operating System` · ProductVersion=`6.1.7600.16396`
- 节区(6): `.text`, `.rdata`, `.data`, `INIT`, `.rsrc`, `.reloc`
- 导入(1 DLL): `ntoskrnl.exe`(11)
- 资源: VERSION×1
- PDB: `e:\data\sysceo\sc\sc3.0\sc3.0\driver\nt5\objfre_win7_x86\i386\scdrv.pdb`
- 内含 DLL 名: `OEMUI.dll`
- URL: `http://crls1.wosign.com/ca1.crl0h`, `http://ocsp.digicert.com0C`, `http://ocsp.digicert.com0H`, `http://ocsp.digicert.com0I`, `http://ocsp1.wosign.com/ca10/`
- 字符串总数 `185`；关键词命中: OEM×2, 总裁系×1, 驱动×1
  - 驱动: `e:\data\sysceo\sc\sc3.0\sc3.0\driver\nt5\objfre_win7_x86\i386\scdrv.pd`
  - OEM: `Microsoft Application Virtualization OEMUI` | `OEMUI.dll`
  - 总裁系: `e:\data\sysceo\sc\sc3.0\sc3.0\driver\nt5\objfre_win7_x86\i386\scdrv.pd`

### `PUBCE`
- 大小 `19,224,984` · sha256 `bd465c42640ca37d…` · 架构 `x86` · 子系统 `2` · 入口 `0x1181c` · 时间戳 `1528982866`
- 版本信息: Comments=`This installation was built with Inno Setup.` · CompanyName=`Sysceo.com` · FileDescription=`软件魔盒` · FileVersion=`3.0.0.15` · LegalCopyright=`© Jiangmen Eyun Corporation. All rights reserved.` · ProductVersion=`3.0.0.15`
- 节区(8): `.text`, `.itext`, `.data`, `.bss`, `.idata`, `.tls`, `.rdata`, `.rsrc`
- 导入(5 DLL): `advapi32.dll`(1), `comctl32.dll`(1), `kernel32.dll`(1), `oleaut32.dll`(3), `user32.dll`(13)
- 资源: GROUP_ICON×1, ICON×10, MANIFEST×1, RCDATA×4, STRING×6, VERSION×1
- RCDATA 条目(4): `#11111`, `CHARTABLE`, `DVCLAL`, `PACKAGEINFO`
- 内含 DLL 名: `advapi32.dll`, `apphelp.dll`, `clbcatq.dll`, `comctl32.dll`, `comres.dll`, `cryptbase.dll`, `dwmapi.dll`, `kernel32.dll`, `ntmarta.dll`, `oleacc.dll`, `oleaut32.dll`, `profapi.dll`, `propsys.dll`, `setupapi.dll`
- URL: `http://ocsp.digicert.com0A`, `http://ocsp.digicert.com0C`, `http://ocsp.digicert.com0H`, `http://ocsp.digicert.com0I`, `http://ocsp.digicert.com0X`
- 字符串总数 `32707`；关键词命中: 总裁系×1, 推广×1, 驱动×2
  - 驱动: `D-5`SRS` | `SRS>3PTB`
  - 总裁系: `Sysceo.com                                                  `
  - 推广: `软件魔盒                                                        `

### `PUBCF`
- 大小 `4,481,024` · sha256 `c466c0b8e84208ae…` · 架构 `x86` · 子系统 `2` · 入口 `0x34a1ac` · 时间戳 `1617963611`
- 版本信息: CompanyName=`Sysceo.com` · FileDescription=`Scpicm` · FileVersion=`3.2.0.0` · LegalCopyright=`Copyright © sysceo.com All Rights Reserved.` · ProductName=`Scpicm` · ProductVersion=`3.2.0.0` · Comments=`Scpicm`
- 节区(11): `.text`, `.itext`, `.data`, `.bss`, `.idata`, `.didata`, `.edata`, `.tls`, `.rdata`, `.reloc`, `.rsrc`
- 导入(14 DLL): `KERNEL32.DLL`(129), `advapi32.dll`(3), `comctl32.dll`(35), `gdi32.dll`(101), `gdiplus.dll`(555), `msvcrt.dll`(2), `ole32.dll`(8), `oleaut32.dll`(3), `shell32.dll`(2), `shlwapi.dll`(1), `user32.dll`(5), `version.dll`(3), `wininet.dll`(4), `winspool.drv`(1)
- 导出(1): `TMethodImplementationIntercept`
- 资源: CURSOR×7, GROUP_CURSOR×7, GROUP_ICON×1, ICON×10, MANIFEST×1, RCDATA×7, STRING×35, TESTDATA×1, VERSION×1
- RCDATA 条目(7): `DVCLAL`, `MLSKINREGISTERHINT`, `PACKAGEINFO`, `PLATFORMTARGETS`, `TMLSKINRESDM`, `TSCPM`, `TTKMF`
- 内含 DLL 名: `DWMAPI.DLL`, `Fwpuclnt.dll`, `IdnDL.dll`, `KERNEL32.DLL`, `Kernel32.dll`, `MSWSOCK.DLL`, `NTDLL.DLL`, `Normaliz.dll`, `PSAPI.dll`, `WS2_32.DLL`, `Wship6.dll`, `advapi32.dll`, `comctl32.dll`, `gdi32.dll`
- 字符串总数 `42624`；关键词命中: OEM×5, sysprep×1, 任务栏×22, 总裁系×13, 推广×3, 浏览器×2, 部署×20, 驱动×8
  - 浏览器: `MonochromeD` | `lrMonoChrome`
  - sysprep: `oobe\windeploy.exe`
  - 驱动: ` TArray<System.SysUtils.TLangRec>` | `&TArray<System.SysUtils.TUnitHashEntry>` | `/TArray<System.SysUtils.TMarshaller.TDisposeRec>` | `System.SysConst`
  - 部署: `-Edeploy` | `/Edeploy` | `DecryptScdata` | `Deploy`
  - OEM: `FOEMConvert` | `GetOEMCP` | `OEMConvert` | `OEM_CHARSET`
  - 任务栏: `FHideInTaskbar` | `FMainFormOnTaskBar` | `FMinimizeToTaskbar` | `FTaskbarHandler`
  - 总裁系: `Copyright © sysceo.com All Rights Reserved.` | `E:\Data\Sysceo\SC\SC3.0\SC3.0\Zip\AbDfBase.pas` | `E:\Data\Sysceo\SC\SC3.0\SC3.0\Zip\AbDfCryS.pas` | `E:\Data\Sysceo\SC\SC3.0\SC3.0\Zip\AbDfDec.pas`
  - 推广: `CombineModeUnion` | `UnionF` | `cmUnion`

### `PUBCG`
- 大小 `594,432` · sha256 `6860011db908bf68…` · 架构 `x86` · 子系统 `2` · 入口 `0x65090` · 时间戳 `708992537`
- 版本信息: CompanyName=`SysCeo.Com` · FileDescription=`By:Noime` · FileVersion=`3.2.0.0` · InternalName=`ScRestart` · LegalCopyright=`SysCeo.Com` · OriginalFilename=`ScRestart` · ProductName=`ScRestart` · ProductVersion=`3.2.0.0` · Comments=`ScRestart`
- 节区(8): `CODE`, `DATA`, `BSS`, `.idata`, `.tls`, `.rdata`, `.reloc`, `.rsrc`
- 导入(7 DLL): `KERNEL32.DLL`(34), `advapi32.dll`(3), `comctl32.dll`(23), `gdi32.dll`(65), `oleaut32.dll`(3), `user32.dll`(4), `version.dll`(3)
- 资源: BITMAP×11, CURSOR×7, DIALOG×1, GROUP_CURSOR×7, GROUP_ICON×1, ICON×9, MANIFEST×1, RCDATA×3, STRING×17, VERSION×1
- RCDATA 条目(3): `DVCLAL`, `PACKAGEINFO`, `TFORM1`
- 内含 DLL 名: `KERNEL32.DLL`, `MAPI32.DLL`, `USER32.DLL`, `User32.dll`, `advapi32.dll`, `comctl32.dll`, `gdi32.dll`, `imm32.dll`, `kernel32.dll`, `oleaut32.dll`, `user32.dll`, `uxtheme.dll`, `vcltest3.dll`, `version.dll`
- URL: `http://ns.adobe.com/xap/1.0/`
- 字符串总数 `4906`；关键词命中: OEM×3, 任务栏×2, 总裁系×1
  - OEM: `CharToOemA` | `OEM_CHARSET` | `OemToCharA`
  - 任务栏: `TaskbarCreated` | `taskbar`
  - 总裁系: `SysCeo.Com`

### `PUBCH`
- 大小 `4,032` · sha256 `cce684deb858876f…` · 架构 `-` · 子系统 `-` · 入口 `-` · 时间戳 `-`
- 版本信息: 无
- 节区(0): 
- 导入(0 DLL): 
- 字符串总数 `63`；关键词命中: 无

### `PUBCI`
- 大小 `5,007` · sha256 `f987cd6b4fb4650a…` · 架构 `-` · 子系统 `-` · 入口 `-` · 时间戳 `-`
- 版本信息: 无
- 节区(0): 
- 导入(0 DLL): 
- 字符串总数 `55`；关键词命中: ACL×1
  - ACL: `                                ?      F        DSROLE.dll      logonc`

### `funn_unpacked.exe`
- 大小 `12,525,840` · sha256 `2c90e7a69a5a109f…` · 架构 `x86` · 子系统 `2` · 入口 `0x2dac0c` · 时间戳 `1778808618`
- 版本信息: CompanyName=`TOOL` · FileDescription=`TOOL` · FileVersion=`1.5.0.1` · InternalName=`Crun.exe` · LegalCopyright=`Copyright (C) 2021` · OriginalFilename=`Crun.exe` · ProductName=`TOOL` · ProductVersion=`1.5.0.1`
- 节区(11): `.text`, `.itext`, `.data`, `.bss`, `.idata`, `.didata`, `.edata`, `.tls`, `.rdata`, `.reloc`, `.rsrc`
- 导入(14 DLL): `AdvApi32.dll`(5), `KERNEL32.DLL`(1), `SetupApi.dll`(4), `cfgmgr32.dll`(1), `comctl32.dll`(35), `gdi32.dll`(96), `msvcrt.dll`(2), `ole32.dll`(10), `oleaut32.dll`(3), `shell32.dll`(2), `shlwapi.dll`(1), `user32.dll`(5), `version.dll`(3), `winspool.drv`(1)
- 导出(1): `TMethodImplementationIntercept`
- 资源: CURSOR×7, DATA×3, GROUP_CURSOR×7, GROUP_ICON×1, ICON×10, MANIFEST×1, RCDATA×4, STRING×32, VERSION×1
- DATA 条目(3): `FUNA`, `FUNB`, `FUNC`
- RCDATA 条目(4): `DVCLAL`, `PACKAGEINFO`, `PLATFORMTARGETS`, `TSCTMF`
- PDB: `C++\Browser_noime_enew\DLL_Release\broscfg.pdb`, `E:\workspaces\Crack\SetEdge\Release\EdgeCipherx64.pdb`
- 内含 DLL 名: `ADVAPI32.dll`, `AdvApi32.dll`, `DWMAPI.DLL`, `Fwpuclnt.dll`, `GDI32.dll`, `IMM32.dll`, `IdnDL.dll`, `KERNEL32.DLL`, `KERNEL32.dll`, `Kernel32.dll`, `KernelBase.dll`, `MSIMG32.dll`, `MSWSOCK.DLL`, `NETAPI32.dll`
- URL: `http://dh.sejai.com`, `http://ocsp.digicert.com0A`, `http://ocsp.digicert.com0\`, `http://www.digicert.com/CPS0`
- 字符串总数 `62765`；关键词命中: OEM×58, sysprep×6, 任务栏×27, 压缩×1, 总裁系×20, 推广×14, 浏览器×35, 浏览器篡改×69, 用户配置×3, 虚拟机×3, 部署×41, 驱动×74
  - 浏览器篡改: ` opentabpagetypedefinepagestring="https://newtabx.com/" activenewtabpo` | `"url": "https://www.baidu.com/#tn=90013418_hao_pg&ie={inputEncoding}&w` | `<?xml version="1.0" encoding="utf-8"?><main><Item homepagetype50="3" h` | `C++\Browser_noime_enew\DLL_Release\broscfg.pdb`
  - 浏览器: ` ProxyPassByLocal="FALSE" securitylevel="1" usesecureinput="TRUE" auto` | ` appmodekeepmax="FALSE" newwindowfromoutside="0" forceopenhomepage="TR` | `360Chrome` | `<?xml version="1.0" encoding="utf-8"?><main><Item homepagetype50="3" h`
  - sysprep: `SetupCloseFileQueue` | `SetupCloseInfFile` | `SetupCloseLog` | `SkipOOBE`
  - 驱动: ` TArray<System.SysUtils.TLangRec>` | `&TArray<System.SysUtils.TUnitHashEntry>` | `.system CMD ARGS...    Run CMD ARGS... in a system shell` | `/TArray<System.SysUtils.TMarshaller.TDisposeRec>`
  - 部署: `DecryptScdata` | `Deploy` | `Error:Scdata.sc file missing!` | `Es4InDeploy`
  - 用户配置: `NTUSER.DAT` | `SCRUNTEMP` | `SCRUNTEMP\Control Panel\International`
  - 压缩: `AbZipper`
  - OEM: `&TArray<uSMBIOS.TOEMStringsInformation>` | `+TArray<uSMBIOS_XP.TOEMStringsInformationXP>` | `AutoOem` | `AutoOembg`
  - 任务栏: `FMainFormOnTaskBar` | `FTaskbarHandler` | `Locktaskbar` | `Locktaskbarlist`
  - 总裁系: `Copyright © sysceo.com All Rights Reserved.` | `E:\Data\Sysceo\AD\` | `E:\Data\Sysceo\SC\SC3.0\Sc3.0\Zip\AbDfBase.pas` | `E:\Data\Sysceo\SC\SC3.0\Sc3.0\Zip\AbDfCryS.pas`
  - 虚拟机: `VMware, Inc.` | `VirtualBox` | `VmWare`
  - 推广: `AppBox` | `Error:  Mbox does not exist[MD5]!` | `Error: Mbox does not exist!` | `Error: Mbox does not exist[MD5]!`

### `funnkrx64_unpacked.exe`
- 大小 `5,518,848` · sha256 `2e761c25cf584473…` · 架构 `x64` · 子系统 `2` · 入口 `0x46f470` · 时间戳 `1747995977`
- 版本信息: CompanyName=`Microsoft Corporation` · FileDescription=`NT Kernel & System` · FileVersion=`6.1.7601.17514` · InternalName=`ntkrnlmp.exe` · LegalCopyright=`© Microsoft Corporation. All rights reserved.` · ProductName=`Microsoft® Windows® Operating System` · ProductVersion=`6.1.7601.17514`
- 节区(11): `.text`, `.data`, `.bss`, `.idata`, `.didata`, `.edata`, `.tls`, `.rdata`, `.reloc`, `.pdata`, `.rsrc`
- 导入(14 DLL): `AdvApi32.dll`(5), `KERNEL32.DLL`(1), `SetupApi.dll`(2), `cfgmgr32.dll`(1), `comctl32.dll`(35), `gdi32.dll`(96), `msvcrt.dll`(2), `ole32.dll`(10), `oleaut32.dll`(3), `shell32.dll`(2), `shlwapi.dll`(1), `user32.dll`(5), `version.dll`(3), `winspool.drv`(1)
- 导出(3): `TMethodImplementationIntercept`, `__dbk_fcall_wrapper`, `dbkFCallWrapperAddr`
- 资源: CURSOR×7, GROUP_CURSOR×7, GROUP_ICON×1, ICON×8, MANIFEST×1, RCDATA×4, STRING×32, VERSION×1
- RCDATA 条目(4): `DVCLAL`, `PACKAGEINFO`, `PLATFORMTARGETS`, `TSCTMF`
- 内含 DLL 名: `AdvApi32.dll`, `DWMAPI.DLL`, `Fwpuclnt.dll`, `IdnDL.dll`, `KERNEL32.DLL`, `MSWSOCK.DLL`, `NTDLL.DLL`, `Normaliz.dll`, `SetupApi.dll`, `Shell32.dll`, `User32.dll`, `WS2_32.DLL`, `Wship6.dll`, `advapi32.dll`
- 字符串总数 `47752`；关键词命中: OEM×56, sysprep×7, 任务栏×25, 伪装×2, 压缩×1, 总裁系×17, 推广×12, 浏览器×13, 用户配置×3, 虚拟机×3, 部署×40, 驱动×83
  - 浏览器: `BrowserHomepage` | `MonochromeP` | `SOFTWARE\Microsoft\Internet Explorer\MAIN` | `SOFTWARE\Microsoft\Internet Explorer\Main`
  - sysprep: `SetupCloseFileQueue` | `SetupCloseInfFile` | `SetupCloseLog` | `SkipOOBE`
  - 驱动: ` TArray<System.SysUtils.TLangRec>` | `&TArray<System.SysUtils.TUnitHashEntry>(` | `/TArray<System.SysUtils.TMarshaller.TDisposeRec> ` | `ClearSrs`
  - 部署: `DecryptScdata` | `Deploy` | `Error:Scdata.sc file missing!` | `Es4InDeploy`
  - 用户配置: `NTUSER.DAT` | `SCRUNTEMP` | `SCRUNTEMP\Control Panel\International`
  - 压缩: `AbZipper`
  - OEM: `&TArray<uSMBIOS.TOEMStringsInformation>` | `+TArray<uSMBIOS_XP.TOEMStringsInformationXP>` | `AutoOem` | `AutoOembg`
  - 任务栏: `FMainFormOnTaskBar` | `FTaskbarHandler` | `Locktaskbar` | `Locktaskbarlist`
  - 总裁系: `E:\Data\Sysceo\SC\SC3.0\Sc3.0\Zip\AbDfBase.pas` | `E:\Data\Sysceo\SC\SC3.0\Sc3.0\Zip\AbDfCryS.pas` | `E:\Data\Sysceo\SC\SC3.0\Sc3.0\Zip\AbDfDec.pas` | `E:\Data\Sysceo\SC\SC3.0\Sc3.0\Zip\AbDfEnc.pas`
  - 伪装: `NT Kernel & System` | `ntkrnlmp.exe`
  - 虚拟机: `VMware, Inc.` | `VirtualBox` | `VmWare`
  - 推广: `AppBox` | `Error:  Mbox does not exist[MD5]!` | `Error: Mbox does not exist!` | `Error: Mbox does not exist[MD5]!`
