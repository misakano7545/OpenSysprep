# tools/scpt —— 原工具（SCPT）分析脚本

纯**数据解压与扫描**工具，用于逆向分析「系统总裁封装工具」的加壳产物；**不执行样本**。

| 脚本 | 用途 |
|---|---|
| `unpack.py` | ASPack（2.12/2.42/other）解压核心：块表驱动的 in-place 解压 + PE 重建 |
| `full10.py` / `finish.py` | 主程序收尾：资源大块解压、壳区资源补丁、PE 重建、资源导出 |
| `funq_finish.py` | FUNQ 收尾：壳区尾部资源保留 + `.rsrc` 真实范围修正（`unpack.py` 的辅助） |
| `funq_rsrc.py` | 手工走 PE 资源目录，检查每条资源数据是否落在文件内（IN/OUT!） |
| `full_inventory.py` | 全模块盘点：类型、加壳、版本信息（身份/伪装）、类别关键词命中 |
| `feature_map.py` | 模块 × 功能关键词矩阵 + 主程序流程标记提取 |
| `dossier.py` | 全模块 dossier：版本信息/架构/子系统/节区/导入/导出/资源树/双编码字符串/关键词命中 → JSON + Markdown |
| `compare_funn_family.py` | `FUNN`/`FUNNX64`/`FUNNKR`/`FUNNKRX64` 四变体字符串矩阵与差集 |
| `funnkr_diff.py` | `FUNN` vs `FUNNKR` 行为差异（任务标记 / 窗体类 / 驱动服务 / 浏览器篡改路径） |
| `strings_detail.py` | 指定模块的区分性字符串（路径/注册表/命令/中文） |
| `deep_scan_unknown.py` | 未知模块深挖（INF 文本直接打印 + 区分性字符串） |

依赖：`pefile`（其余为标准库）。
输入：本机 `work/engines/`（解包后的模块）与 `../scpt-analysis/02-resources/`（原包资源），**均不入库**。

> 说明：部分脚本的**检测模式表**里出现 `newtabx`、`sejai`、`prefs_enclave` 等标识——那是用来在样本中**搜索**这些流氓特征的关键词，不是功能实现。
> 仓库红线审计（CI「红线静态审计」）只覆盖 `src/`，即产品实现代码。
