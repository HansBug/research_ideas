# 硬件可得性：工业单位实际能部署多大的模型

> **本轮核验已完成**（各节残留待核验项集中列在 §7.2）。核验窗口：**2026-08-13**。
>
> ⛔ **本文件只查证事实，不评价 story 好坏。** 它回答 [SUMMARY.md](./SUMMARY.md) §15.2「错误三」留下的问题：⛔ 该文 §12.2 的包络表**假设一台 8×80G 节点（640 GB）可得**并据此算出 ~988B 上限，本文核这个假设本身是否成立。导师那句原话不在此重复，见 [SUMMARY.md](./SUMMARY.md) §15.2。
>
> **来源纪律**：出口管制条款一律回官方原文——Federal Register 全文经 **govinfo.gov**（`www.gpo.gov` 出版）抓取后**逐字**核对，BIS 指南取**官方 PDF 原件**，NVIDIA 表述取 **SEC EDGAR 原始申报**。国产卡规格与工业单位算力现状两节的来源等级明显更低，已逐条标注。
>
> **证据级别口径**（沿用本目录既有约定）：**M** = 官方一手来源逐字可查；**S** = 二级来源（律所简报、新闻、第三方拆解、聚合站、预印本的检索摘要）；**I** = 本文推断或计算。⛔ 标 I 的不得写成事实句。

## 0. 一句话结论

**「一台标准 8×80G H100 节点（640 GB）」这个包络假设，对中国大陆的工业单位在 2026 年不成立**——不是因为管制模糊，而是**两边同时禁**：美方自 **2023-11-17** 起把 A100 / H100 / A800 / H800 全量纳入 3A090 许可要求（**M**），**2026-01-15** 起虽把 H200 档放宽到 case-by-case（**M**），但 NVIDIA 在最近一份 10-Q 里写明**截至 2026-04-26 的整个季度对华数据中心 Hopper 产品出货为零、H200 许可项下未产生任何收入**（**M**）；中方则据报自 **2025-11** 起要求**任何拿了国家资金的数据中心项目只用国产 AI 芯片**（**S**，Reuters 双匿名消息源），而型号研制单位 / 设计所正是这类主体。

**但方向性结论必须分三层说，不能一句话带过：**

1. **「640 GB 可得」这个具体假设站不住**（**M** + **S**）。正确的表述不是「640 GB 太大」，而是「**8×80G H100 这个形态在 2026 年不是一个可采购的东西**」。
2. **「包络远大于方法所需」这个结论仍成立，但倍数从 ~49× 塌到 ~1.9×**（**I**，算术见 §3）。最悲观的现实配置——**一张中国合法在售的 24 GB 消费卡**——4-bit 下仍可容 **~37B 总参**，而方法所需 ≤20B。但这已不是「远大于」，而是「刚好够」。
3. ⛔ **一条方向复杂、必须分档说的事实**：`~988B` 原本支撑的推论是「总能部署一个大到不需要脚手架的开放权重模型」。⛔ **在单卡档它减弱**（单卡到单封装档 37B–198B 都够不上那一档）；**但在整机档它不但成立、还有官方部署证据**——**671B MoE 在昇腾上的官方最低门槛是「2 台 Atlas 800I A2（16 × 64GB = 1024 GB）跑 W8A8」**，且 MindIE 与 vLLM-Ascend **两条独立路径口径一致**（**M**，§4.1）。**即该推论只在「买不起整机、只有单卡或工作站」的单位那里不成立。**

⚠️ **四条不利于「算力不可得」叙事的事实，必须一起摆出**（详见 §3.4 与 §4.7）：

- **(a)** 出口管制管的是**出口**，⛔ 不管**已购硬件的继续使用**——BIS 2026-05-31 指南对此有逐字确认（**M**）。
- **(b)** **一台 8×H20 = 768 GB > 640 GB**，而 H20 在 2024 至 2025-04、及 2025-07 之后合法在华销售、单季销售额曾达 46 亿美元（**M**），⛔ 所以「中国工业单位不可能有 640 GB 级节点」是**错的**。
- **(c)** ⛔ **671B 的门槛远低于本文初稿所写**：⛔ 初稿曾把 CloudMatrix384（384 NPU / 48 服务器）当门槛——**那是错的，已更正**。官方最低门槛是**两台国产整机**（**M**）。所以「国产生态跑不了大 MoE」是**错的**，且「跑得了但要 384 卡」也是**错的**。
- **(d)** **32B 档在昇腾上是官方一等公民**：Qwen3-32B 的 BF16 / W8A8 / W4A4 均**单节点即可**，甚至 Atlas 300I Duo 用 W8A8SC + TP4 都有官方教程（**M**，§4.2）。⛔ 即「国产卡跑不了我们需要的那一档」也是**错的**。

**一条与上述反向、支持「不宜贴边选型」的实测**：官方仓库 issue #1127 报告 **DeepSeek-R1-W8A8 在 2×8×64GB（1024 GB）上 OOM**，而按本文口径它理论上装得下（785 GB）——⛔ **说明真实常驻开销比本文的 0.88 更重，本表在贴边格子上偏乐观**（**S** 实测 · **I** 推断）。

**合起来的诚实表述**：**约束不在「显存买不到」，而在「以什么身份、走什么渠道、在什么合规前提下买」。** 一个能拿到国家资金的型号研制单位，恰恰是**最不能走灰市、最必须用国产**的那类主体（**I**，若 §1.10 的报道成立）。

**§5 / §6 的可引来源情况（诚实优先）**：

- **§5（工业单位实际算力现状）**：⛔ **「中国工业企业私有化 LLM 部署规模」这个具体命题查无严谨来源**——委托方的预判基本成立。但找到了一条**可用的夹逼组合**：**工信部 2026 年 14 号文**（官方规范性文件）逐字承认中小企业「**算力获取**…**难点**」并把「训推一体机」「整合本地闲置、分散算力」写进任务；配一篇学术测算给出档位量级（SME = 单张 RTX 5090 / ~$2k）。⛔ 两者层次不同，不得混说。
- **§6（学术界的算力受限论证）**：**共核实 10 篇**以算力可得性（而非隐私）为选小模型理由的 SE/MDE/RE 论文，其中 **3 篇承重、6 篇半承重、1 篇不承重**。最强的一篇是 **Weyssow et al., TOSEM 2025**，把「单卡 24GB」写进 RQ 设计、模型池筛选与结论句。

## 1. 美国对华 AI 芯片出口管制时间线（逐条，含官方来源）

⚠️ **访问方式说明**：`federalregister.gov` 与 `ecfr.gov` 在本次核验中对本机直连均返回 **302 → `https://unblock.federalregister.gov/`**（见 §7.1），故改用 **govinfo.gov** 的官方 Federal Register HTML 全文（同一出版物）。⛔ 由此带来一个必须记住的口径后果：**本文给出的是「各 IFR 当时颁布的文本」，不是「eCFR 现行合并文本」**——若有 2025–2026 的后续修订未被本文覆盖，可能存在差异（列入 §7.2 待核验）。

### 1.1 2022-10-07 发布 / 2022-10-13 公布：首次设卡，A100 / H100 落网

| 项 | 内容 | 级别 |
| :-- | :-- | :-- |
| 规则名 | Implementation of Additional Export Controls: Certain Advanced Computing and Semiconductor Manufacturing Items; Supercomputer and Semiconductor End Use; Entity List Modification（**interim final rule**） | M |
| 引证 | **87 FR 62186**，FR Doc 2022-21658 | M |
| 官方来源 | [govinfo 全文](https://www.govinfo.gov/content/pkg/FR-2022-10-13/html/2022-21658.htm) · [FR 页面](https://www.federalregister.gov/documents/2022/10/13/2022-21658/implementation-of-additional-export-controls-certain-advanced-computing-and-semiconductor) · [govinfo 详情](https://www.govinfo.gov/app/details/FR-2022-10-13/2022-21658) | M |
| **生效日** | **分级生效**（DATES 段逐字）：**2022-10-07**（§740.2、§740.10、§742.6、§744.23、supp. 1 to part 774 等）；**2022-10-12**（§744.6）；**2022-10-21**（§734.9、supp. 1 to part 734、supp. 1 to part 736、§742.6、§744.1、§744.11、§744.23、§762.2、§772.1、supp. 1 to part 774 等） | M |

**新建 ECCN 3A090 的原始阈值（Items 段逐字）**：

> "a. Integrated circuits that have or are programmable to have an **aggregate bidirectional transfer rate over all inputs and outputs of 600 Gbyte/s or more** to or from integrated circuits other than volatile memories, **and any of the following**: a.1. One or more digital processor units executing machine instructions having a **bit length per operation multiplied by processing performance measured in TOPS**, aggregated over all processor units, **of 4800 or more**; a.2. One or more digital `primitive computational units,' … of 4800 or more; a.3. One or more analog, multi-value, or multi-level `primitive computational units' having a processing performance measured in TOPS multiplied by 8 … of 4800 or more; or a.4. Any combination … sum to 4800 or more."

**注意这里是 AND**：既要 ≥600 GB/s 互连**又**要 bits×TOPS ≥4800。**这个合取结构就是 A800 / H800 存在的原因**——把互连降到 600 GB/s 以下即可脱离管制（**I**，逻辑推论；A800/H800 的具体互连数字为 **S**）。

**同时新建**：ECCN **4A090**（含 3A090 IC 的计算机 / 电子组件 / 部件）、**4D090**（配套软件）、3D001 / 3E001 / 4E001 配套软件与技术控制；**§744.23** 超算与半导体终端用途控制（在具备「knowledge」时，**即便 EAR99 项目**也需许可）；并把 FDP 规则扩展到先进计算与超算（**M**）。

### 1.2 2023-10-17 发布 / 2023-10-25 公布：**堵死降级版，A800 / H800 落网**

| 项 | 内容 | 级别 |
| :-- | :-- | :-- |
| 规则名 | Implementation of Additional Export Controls: Certain Advanced Computing Items; Supercomputer and Semiconductor End Use; Updates and Corrections（**interim final rule**，简称 AC/S IFR） | M |
| 引证 | **88 FR 73458**（pp. 73458–73517），FR Doc 2023-23055，**RIN 0694-AI94**，Docket 231013-0248 | M |
| 官方来源 | [govinfo 全文](https://www.govinfo.gov/content/pkg/FR-2023-10-25/html/2023-23055.htm) · [FR 页面](https://www.federalregister.gov/documents/2023/10/25/2023-23055/implementation-of-additional-export-controls-certain-advanced-computing-items-supercomputer-and) | M |
| **生效日** | DATES 段逐字：**"This rule is effective November 17, 2023"**，仅 supp. 1 to part 736 的第 11 条修订为 **2023-11-17 至 2026-01-01** 有效 | M |
| 同日姊妹规则 | Export Controls on Semiconductor Manufacturing Items，**88 FR 73424**（[FR 页面](https://www.federalregister.gov/documents/2023/10/25/2023-23049/export-controls-on-semiconductor-manufacturing-items)） | M |

**这一版是整条时间线的枢纽。BIS 自己写明动机（逐字）**：

> "BIS learned that certain additional ICs could provide **nearly comparable AI model training capability** to those already controlled under the October 7, 2022 rule…"

**关键改动：删掉互连参数，改成 TPP + performance density 的两档结构（规则正文逐字）**：

> "In ECCN 3A090, this AC/S IFR revises the ``items'' paragraph in the List of Items Controlled section **to remove paragraph a, including paragraphs a.1 through a.4**, and adds in its place a simplified paragraph .a and .b."

**新 3A090 阈值（Items 段逐字）**：

- **3A090.a**：`a.1` TPP **≥ 4800**；**或** `a.2` TPP **≥ 1600** 且 performance density **≥ 5.92**
- **3A090.b**：`b.1` TPP **≥ 2400 且 < 4800** 且 performance density **≥ 1.6 且 < 5.92**；**或** `b.2` TPP **≥ 1600** 且 performance density **≥ 3.2 且 < 5.92**

**TPP 定义（Technical Notes to 3A090 第 1 条，逐字）**：

> "`Total processing performance' (`TPP') is **2 x `MacTOPS' x `bit length of the operation'**, aggregated over all processing units on the integrated circuit."

其中 `MacTOPS` 是 multiply-accumulate（$D = A \times B + C$）的理论峰值 Tera 次/秒；公式里的 2 来自「一次 MAC 记 2 次运算」的数据表惯例，故 $2 \times \mathrm{MacTOPS}$ 通常就等于数据表上标的 TOPS / FLOPS（**M**）。**第 3 条规定按稠密矩阵取值、不含稀疏加速**（**M**）。BIS 自己给的换算例（逐字）：

> "the `TPP' threshold of 4800 can be met with **600 tera integer operations** (or 2 x 300 `MacTOPS') **at 8 bits** or **300 tera FLOPS** (or 2 x 150 `MacTOPS') **at 16 bits**."

**Performance density 定义（Technical Note 第 4 条，逐字）**：

> "`Performance density' is `TPP' divided by `applicable die area'. For purposes of 3A090, `applicable die area' is measured in **millimeters squared** and includes all die area of logic dies manufactured with a process node that uses a **non-planar transistor architecture**."

**目的地范围同时扩大（正文逐字）**：从「China and Macau」改成 **"any destination specified in Country Groups D:1, D:4, or D:5 that is not also specified in Country Groups A:5 or A:6"**（**M**）。

**为什么 A800 / H800 在这一版落网**（**I**，按上述官方公式自行验算）：删掉互连合取项后只看 TPP。A100 的 INT8 稠密约 624 TOPS → $\mathrm{TPP} \approx 624 \times 8 = 4992 \ge 4800$；H100 SXM 的 FP8 稠密约 1979 TFLOPS → $\mathrm{TPP} \approx 1979 \times 8 \approx 15832 \gg 4800$。A800 / H800 与之算力相同、仅降互连，故一并落入 3A090.a。⚠️ **算力数字本身是 S 级**（NVIDIA 数据表口径），公式是 M 级，⛔ 结论是 I 级。

**同时新增 License Exception NAC**（notified advanced computing）：为 3A090.b 类项目提供「事先通知 BIS」的路径；中国大陆与澳门**境内转移不适用**通知要求（**M**）。ECCN 3A090 的 List Based License Exceptions 段逐字：**"NAC: Yes, for 3A090.a, if the item is not designed or marketed for use in datacenters and has a `total processing performance' of 4800 or more; yes, for 3A090.b, if the item is designed or marketed for use in datacenters."**

**Note 2 to 3A090（重要豁免，逐字）**：

> "3A090 does not apply to items that are **not designed or marketed for use in datacenters** and **do not have a `total processing performance' of 4800 or more**."

这条 Note 2 就是消费级显卡能不能对华出货的判据所在，也是后来 4090D / 5090D / 5090D V2 反复改规格的规则依据（**I**）。

### 1.3 2024-04-04：更正与澄清

| 项 | 内容 | 级别 |
| :-- | :-- | :-- |
| 规则名 | Implementation of Additional Export Controls … Updates and Corrections; and Export Controls on Semiconductor Manufacturing Items; Corrections and Clarifications | M |
| 引证 | **89 FR 23876**（[FR 页面](https://www.federalregister.gov/documents/2024/04/04/2024-07004/implementation-of-additional-export-controls-certain-advanced-computing-items-supercomputer-and)） | M |
| 内容 | 更正 2023 两份 IFR 的笔误；删除对 Note 4 to 3A090 的引用；恢复含 `.z` 段的 ECCN 控制；对 3A090 / 4A090 及相关 `.z` 增加 case-by-case 审查政策，**但明确排除按 3A090.a 参数设计或营销用于数据中心的项目** | S ⚠️ |

⚠️ **本条未回原文逐字核对**（本轮未抓取 89 FR 23876 全文），内容取自搜索摘要，**标 S / 待核验**。

### 1.4 2024-12-02 生效 / 2024-12-05 公布：**HBM 本身被管制**

| 项 | 内容 | 级别 |
| :-- | :-- | :-- |
| 规则名 | Foreign-Produced Direct Product Rule Additions, and Refinements to Controls for Advanced Computing and Semiconductor Manufacturing Items（**IFR**） | M |
| 引证 | **89 FR 96790**，FR Doc 2024-28270，**RIN 0694-AJ74**，Docket BIS-2024-0028 | M |
| 官方来源 | [govinfo 全文](https://www.govinfo.gov/content/pkg/FR-2024-12-05/html/2024-28270.htm) · [FR 页面](https://www.federalregister.gov/documents/2024/12/05/2024-28270/foreign-produced-direct-product-rule-additions-and-refinements-to-controls-for-advanced-computing) | M |
| **生效 / 合规日** | DATES 段逐字：**"This rule is effective December 2, 2024"**；HBM 相关修订（含 3A090、3D001、3E001、FDP 与 DRAM 定义变更）**合规日为 2024-12-31**；红旗与 §734.19 合规日为 **2024-12-02** | M |

**新增 3A090.c（Items 段逐字）**：

> "c. High bandwidth memory (HBM) having a `memory bandwidth density' **greater than 2 gigabytes per second per square millimeter**."

**Technical note to 3A090.c（逐字要点）**：`memory bandwidth density` = 封装或堆栈的内存带宽（GB/s）÷ 封装或堆栈面积（mm²）；**不论是否符合 JEDEC HBM 标准均适用**；HBM 与逻辑芯片共封装且逻辑为主导功能的情形除外（**M**）。

⛔ **这一条的杀伤力被普遍低估。BIS 自己写明（逐字）**：

> "**All HBM stacks currently in production exceed this threshold.**"

**即：不是某些 HBM 被管，是当时在产的全部 HBM 都被管。** BIS 给的理由也写得很直白（逐字）：

> "As **indigenous PRC advanced computing ICs rely upon imported HBM**, new ECCN 3A090.c implements restrictions to **slow PRC attempts to indigenize advanced AI chip production**…"

这直接打在**国产卡的供应链**上，而不只是打在 NVIDIA 上——⛔ **§2 的国产卡显存容量能不能持续供应，根子在这里。**

**同时新增 License Exception HBM（§740.25）**：仅授权美方（或符合条件方）拥有并运营的封装站点，且逐字规定**只有 `memory bandwidth density < 3.3 GB/s/mm²` 的 3A090.c 项目**才可走该例外——**"HBM at equal to or greater than this parameter … are of greater sensitivity"**（**M**）。

### 1.5 2025-01-15：AI Diffusion 规则（⛔ **后被停止执行**）

| 项 | 内容 | 级别 |
| :-- | :-- | :-- |
| 规则名 | Framework for Artificial Intelligence Diffusion（IFR） | M |
| 引证 | **90 FR 4544**（[FR 页面](https://www.federalregister.gov/documents/2025/01/15/2025-00636/framework-for-artificial-intelligence-diffusion)） | M |
| 内容 | 对 3A090.a / 4A090.a 及相关 `.z` 施加**全球性**许可要求；并首次控制部分**封闭权重 AI 模型的模型权重** | S ⚠️ |
| 合规日 | 原定 **2025-05-15** 起 | S |

### 1.6 2025-01-16：先进计算 IC 尽职调查规则

| 项 | 内容 | 级别 |
| :-- | :-- | :-- |
| 规则名 | Implementation of Additional Due Diligence Measures for Advanced Computing Integrated Circuits; Amendments and Clarifications; and Extension of Comment Period | M |
| 官方来源 | [FR 页面](https://www.federalregister.gov/documents/2025/01/16/2025-00711/implementation-of-additional-due-diligence-measures-for-advanced-computing-integrated-circuits) · [govinfo PDF](https://www.govinfo.gov/content/pkg/FR-2025-01-16/pdf/2025-00711.pdf)（**91 FR / 90 FR Vol. 90 No. 10**） | M |
| 内容 | 新增 Note 1 to 3A090.a 并修订 3A090.a；给代工厂尽职调查指引；BIS 认定**晶体管数低于 Red Flag 19 的 500 亿门槛的 IC 仍可能达到 3A090 性能阈值**，故此前代工厂在该门槛以下缺乏指引 | S ⚠️ |

⚠️ **§1.5 与 §1.6 未回原文逐字核对**，标 **S / 待核验**。

### 1.7 2025-04-09 / 04-14：**H20 被套上许可要求**

本条来源是 **NVIDIA 向 SEC 的原始申报**，属公司一手陈述（**M**，就「公司如此陈述」这一事实而言）。

| 日期 | 事实 | 级别 |
| :-- | :-- | :-- |
| 2025-04-09 | USG 告知 NVIDIA：向中国（含香港、澳门）及 D:5 国家、或**总部 / 最终母公司在该地**的企业出口 **H20**，以及**任何达到 H20 的内存带宽、互连带宽或其组合**的 IC，**需要许可** | M |
| 2025-04-14 | USG 告知该许可要求**无限期有效**（"in effect for the indefinite future"） | M |
| 2025-04-15 | 8-K 申报：预计 Q1 计提**最高约 55 亿美元** H20 相关费用（存货、采购承诺与相关准备） | M |
| 来源 | [8-K（2025-04-15 申报，nvda-20250409.htm）](https://www.sec.gov/Archives/edgar/data/1045810/000104581025000082/nvda-20250409.htm) | M |
| 2025-05-28 | 实际计提 **45 亿美元**（因部分物料可复用）；许可要求生效前该季 **H20 销售额 46 亿美元** | M |
| 来源 | [Q1 FY2026 CFO commentary](https://www.sec.gov/Archives/edgar/data/1045810/000104581025000115/q1fy26cfocommentary.htm) · [新闻稿](https://www.sec.gov/Archives/edgar/data/1045810/000104581025000115/q1fy26pr.htm) | M |

⚠️ **注意措辞**：这是 USG 对单一企业的**许可要求通知**，⛔ 不是一条公布在 Federal Register 的规则。它的公开证据形态就是公司申报（**M**）。

### 1.8 2025-05-13：AI Diffusion 停止执行 + **昇腾被点名列入 GP 10 风险**

| 项 | 内容 | 级别 |
| :-- | :-- | :-- |
| 官方来源 | [BIS 新闻稿](https://www.bis.gov/press-release/department-commerce-announces-rescission-biden-era-artificial-intelligence-diffusion-rule-strengthens) | M |
| 动作 1 | BIS 启动撤销 AI Diffusion Rule，并指示执法人员**不予执行** | M |
| 动作 2 | 同时发布三份文件：**GP 10 指南**（中国先进计算 IC）、防转移行业指南、关于用于训练 AI 模型的先进计算 IC 的政策声明 | S |
| 动作 3 | GP 10 指南**点名 Huawei Ascend 910B / 910C / 910D**，认定这些芯片「**很可能**」是在违反 EAR 的情况下生产的（"high probability" 许可本应取得而未取得），故任何人使用 / 销售 / 转让 / 融资 / 服务这些芯片都可能触发 GP 10（§764.2(e)）；名单**非穷尽** | S ⚠️ |
| 唯一例外 | 仅为技术分析 / 评估（如破坏性测试）而取得 PRC 3A090 IC 的，BIS 表示不追究 | S ⚠️ |

⚠️ **§1.8 的动作 3 与例外未回官方 PDF 逐字核对**（本轮未定位到该 GP 10 指南 PDF 的直链），标 **S / 待核验**。

但它的**间接影响对本文很重要**：若昇腾在美方眼里带 GP 10 风险，那么**在昇腾上做实验并公开发表**这件事本身，对有美方合作者或美方云资源的作者存在合规摩擦——⛔ 这是**推断（I）**，不是已核实的法律结论。

### 1.9 2025-07-15 起：H20 恢复 + 15% 分成（⛔ **注意「保证」≠「已发证」**）

| 日期 | 事实 | 级别 |
| :-- | :-- | :-- |
| 2025-07-15 | NVIDIA 称正在申请恢复 H20 对华销售，**USG 已保证会批准许可**；同时宣布面向中国的合规 RTX PRO 产品 | S（公司公开声明 / 新闻） |
| 同期 | AMD 获准恢复 **MI308** 对华销售 | S |
| 2025-08 | 报道称美方对这类对华芯片销售收取 **15%** 收入分成 | S ⚠️ |
| 来源 | [NVIDIA Newsroom（X）](https://x.com/nvidianewsroom/status/1944937756289061188) · [CNBC](https://www.cnbc.com/2025/07/15/nvidia-says-us-government-will-allow-it-to-resume-h20-ai-chip-sales-to-china.html) · [Tom's Hardware](https://www.tomshardware.com/tech-industry/artificial-intelligence/nvidia-to-resume-h20-sales-in-china-says-u-s-government-has-promised-to-grant-licenses-deliveries-to-start-soon) | S |

⚠️ **必须保留这个区分**：7 月的公开表述是**保证会批**，不是**已发证**。⛔ 15% 分成的官方文本本轮**未找到**（列入 §7.2）。

### 1.10 2025-11-05（报道日）：**中方反向禁令**——国家资金数据中心只用国产芯片

这一条不是美方管制，但它对「中国工业单位能部署什么」的**约束力比美方管制更直接**，必须进时间线。

| 项 | 内容 | 级别 |
| :-- | :-- | :-- |
| 内容 | 中国政府发布指引，要求**拿了任何国家资金的新建数据中心项目只使用国产 AI 芯片**；完工度 **<30%** 的项目须**移除已装的外国芯片**或取消采购；更靠后的项目 case-by-case | S ⚠️ |
| 覆盖芯片 | 含 **H20**，也含 **B200 / H200**（后两者本就被美方禁运，但据报在灰市广泛流通） | S |
| 规模背景 | 2021 年以来中国 AI 数据中心项目获国家资金逾 **1000 亿美元**（Reuters 对政府招标的统计）；**多数中国数据中心都拿过某种形式的国家资金** | S |
| 未确定项 | ⛔ 是否全国适用抑或仅部分省份，**报道明确说不清楚** | S |
| 来源 | Reuters（2025-11-05，两名消息人士）经二级转载：[Tom's Hardware](https://www.tomshardware.com/tech-industry/semiconductors/china-bans-foreign-ai-chips-from-state-funded-data-centers) · [FDD 分析](https://www.fdd.org/analysis/2025/11/10/signaling-confidence-in-its-domestic-industry-china-bans-foreign-ai-chips-in-state-funded-data-centers/) · [DigiTimes](https://www.digitimes.com/news/a20251106VL205/chips-nvidia-data-technology-beijing.html) | S |

⚠️ **来源等级说明**：这是 **Reuters 引述两名匿名消息人士**，中方 CAC 与 NDRC **未回应置评**。⛔ **没有找到公开的官方政策文本**（列入 §7.2）。因此**不得**把它写成「中国官方规定」，只能写成「据 Reuters 报道」。

**但它对本文 story 的相关性极高**：型号研制单位 / 设计所 / 军工院所**正是**「拿国家资金」的主体。若该指引成立且适用，则这类单位的可选硬件**在中方一侧**就已被限定为国产卡——⛔ **与美方管制无关**。

### 1.11 2026-01-13 发布 / **2026-01-15 生效**：H200 档放宽到 case-by-case

| 项 | 内容 | 级别 |
| :-- | :-- | :-- |
| 规则名 | Revision to License Review Policy for Advanced Computing Commodities（**final rule**，非 IFR） | M |
| 引证 | **91 FR 1684**（pp. 1684–1689），FR Doc 2026-00789，**RIN 0694-AK43**，Docket 260112-0028 | M |
| 官方来源 | [govinfo 全文](https://www.govinfo.gov/content/pkg/FR-2026-01-15/html/2026-00789.htm) · [FR 页面](https://www.federalregister.gov/documents/2026/01/15/2026-00789/revision-to-license-review-policy-for-advanced-computing-commodities) · [BIS 新闻稿](https://www.bis.gov/press-release/department-commerce-revises-license-review-policy-semiconductors-exported-china) | M |
| **生效日** | DATES 段逐字：**"The effective date of this rule is January 15, 2026."** | M |

**SUMMARY 段逐字**：

> "BIS is revising its license review policy for exports of certain semiconductors to China and Macau—**changing it from a presumption of denial to a case-by-case review**. The semiconductors covered by this rule are the **Nvidia H200 and its equivalents, as well as less advanced chips**—provided that (1) the semiconductors are **commercially available in the United States** at the time of publication of this rule and (2) the exporter certifies that: there is sufficient supply of this product in the United States; production of this product for exports to China will not divert global foundry capacity for similar or more advanced products for end users in the United States; the recipient has demonstrated sufficient security procedures; and the item undergoes **independent, third-party testing in the United States** to verify its performance specifications."

**新阈值（正文逐字）**：

> "for advanced computing commodities with a **TPP less than 21,000** (as defined in Technical Note 2 to 3A090.a and 3A090.b), and a **`total DRAM bandwidth' less than 6,500 GB/s** (as defined in the notes to paragraph (dd)(1) in supplement no. 2 to part 748), **such as the NVIDIA H200 or AMD MI325X**, this final rule specifies certain conditions that, if satisfied, allow for license applicants to move from a presumption of denial to a case-by-case license review policy for **exports from the United States** destined to China or Macau."

**仍维持 presumption of denial 的边界（正文逐字）**：对**总部或母公司总部在 D:5 / 澳门的实体，即便该实体位于 D:5 / 澳门之外**（**M**）。⛔ 另据律所简报：**re-export、境外出口、以及中国 / 澳门境内转移仍为 presumption of denial**（**S**，本轮未逐字定位到该段规则原文）。

⛔ **一处必须更正的二级来源说法**：多份律所简报称本规则「维持 B200 / GB200 / GB300 的 presumption of denial」。⛔ **规则原文里根本没有出现 "B200" 字样**——本机对 govinfo 全文做过字符串检索，`find('B200')` 返回 **-1**。正确表述是：**Blackwell 级产品因 TPP 与 DRAM 带宽双双超过 21,000 / 6,500 GB/s 门槛而不符合本规则的放宽条件**（**I**，按官方阈值自行验算：B200 的 FP8 稠密约 4.5 PFLOPS → $\mathrm{TPP} \approx 4500 \times 8 = 36000 > 21000$；显存带宽 8 TB/s $= 8000\ \mathrm{GB/s} > 6500$）。B200 的算力与带宽数字本身是 **S** 级。

**H200 为何刚好过线**（**I**，同上口径）：FP8 稠密约 1979 TFLOPS → $\mathrm{TPP} \approx 15832 < 21000$；HBM3e 带宽 4.8 TB/s $= 4800\ \mathrm{GB/s} < 6500$。**H100 SXM 同样满足**（TPP 同为 ~15832，带宽 3.35 TB/s $= 3350\ \mathrm{GB/s}$），故落在规则所称 "as well as less advanced chips" 之内（**I**）。

**同期关税**：2026-01-14 总统公告对境外生产、经美国转出口的先进计算芯片征 **25%** 从价税，2026-01-15 生效（**S** ⚠️，未回公告原文；但 NVIDIA 10-Q 对「H200 出货须先在美检验、因而入美时承担 25% 关税」有逐字确认，见 §1.14——**该关税对 H200 通道生效这一点是 M**）。

### 1.12 2026-01-14：**中方在美方放宽的次日拦下 H200**

| 项 | 内容 | 级别 |
| :-- | :-- | :-- |
| 内容 | 中国海关被告知 NVIDIA **H200 不准入境**；官方于 01-13 约谈国内科技企业，要求非必要不采购，一名消息人士称措辞「严厉到基本等于暂时禁止」 | S ⚠️ |
| 补充 | 据报 NVIDIA 已备妥首批 **82,000 块 H200**，因该拦阻而搁置 | S ⚠️ |
| 例外讨论 | 据报仅在特殊情形（如与高校合作的研发）可能获批 | S ⚠️ |
| 置评 | ⛔ 中国海关总署、工信部、发改委**均未回应**；NVIDIA 未回应 | S |
| 来源 | Reuters（三名知情人）经转载：[U.S. News](https://www.usnews.com/news/top-news/articles/2026-01-14/chinas-customs-agents-told-nvidias-h200-chips-are-not-permitted-sources-say) · [Taipei Times](https://www.taipeitimes.com/News/biz/archives/2026/01/15/2003850605) | S |

⚠️ **另有二级来源称 2026-03 中旬中方已批准 NVIDIA 向部分中国客户销售 H200。** ⛔ 这条与 NVIDIA 自己的最新申报（§1.14：**截至 2026-04-26 收入为零、能否入境未知**）**张力明显，本文不采用它作为事实**，只记为待核验（§7.2 第 4 项）。

### 1.13 2026-05-31：BIS 指南——**堵住「中资海外子公司」通道**

这一条**已回官方 PDF 原件逐字核对**。

| 项 | 内容 | 级别 |
| :-- | :-- | :-- |
| 文件名 | Guidance Regarding Enforcement of License Requirements for Advanced Computing Items for Entities Headquartered in Country Group D:5 and Macau **[May 31, 2026]** | M |
| 官方来源 | [BIS 官方 PDF](https://www.bis.gov/media/documents/bis-guidance-may-31-2026.pdf) | M |

**逐字要点**：

> "…a license is required to export advanced computing items to entities headquartered in Country Group D:5 … or Macau or with an ultimate parent company headquartered in Country Group D:5 or Macau – **even if the entities themselves are located outside** Country Group D:5 or Macau."

> "This license requirement was **first introduced on November 17, 2023**. It was implemented via an end-user control in **§ 744.23(a)(3)** of the EAR and applied to all advanced computing items (e.g., those specified in Export Control Classification Numbers (ECCNs) **3A090.a and .b, 4A090.a and .b, and related .z paragraph items**)."

> "In January 2025, the AI Diffusion Rule transferred the requirement for these ".a" items from § 744.23(a) **into § 742.6** as part of a new worldwide license requirement. In May 2025, BIS announced that it would **not be enforcing** the AI Diffusion Rule's new compliance requirements."

> "Recently, BIS has received questions as to whether the preexisting license requirement established in November 2023 is still being enforced … **The answer is yes.** Specifically, a license requirement continues to apply under **§ 742.6(a)(6)(iii)(A)** of the EAR to **all destinations outside the United States** for these advanced computing items when such items are for entities headquartered in, or whose ultimate parent company is headquartered in, Country Group D:5 or Macau."

**数据中心运营方的缓和条款（逐字，对 §3.4 承重）**：

> "**Bona fide operators of data centers** who are otherwise engaged in activities consistent with the EAR are **not required to cease the ongoing use, storage, disposal, or servicing** of advanced computing items because of this guidance, **until further notice** from BIS."

这条缓和条款有实质意义：它确认**「继续使用已有的先进计算硬件」不因本指南而被要求停止**——⛔ 即出口管制管的是**出口 / 转让**，不是**存量的继续使用**（**M**，就该指南的文义而言）。这与 §3.4 里「存量 640 GB 级节点确实存在」相互印证。⚠️ 但 "bona fide operators" 在文件中**未被定义**，且未给后续指引的时间表（**S**，律所观察）。

### 1.14 当前状态（截至本文核验日 2026-08-13）

最权威的「实际能不能买到」证据，来自 NVIDIA 最近一份 10-Q（**Q1 FY2027，报告期止 2026-04-26**）。以下均为**逐字**引用（**M**，就「公司如此申报」而言）：

> "**Beginning in February 2026, the U.S. government, or USG, granted licenses that allow us to ship small amounts of H200 products to specific China-based customers. To date, we have not generated any revenue under the H200 licensing program, and do not yet know whether any imports will be allowed into China.** The license requires that the H200s go through an inspection process in the United States prior to any shipment to the customer. As a result, any H200 shipped under the new licensing program will be subject to a **25% tariff** upon importation into the United States."

> "**No shipments of Data Center Hopper products to China occurred during the quarter**, compared with $4.6 billion in the first quarter of fiscal year 2026."

> "The export controls applicable to China are complex and address a variety of parameters, including the total processing performance of a chip, the "performance density" of a chip, the interconnect bandwidth of a chip, and the memory bandwidth of a chip. **Under the current rules and geopolitical landscape, we are unable to create and deliver a competitive product for China's data center market that receives approval from both the USG and the Chinese government.**"

> "As of the end of the first quarter of fiscal year 2027, while we were able to **ship uncontrolled products to China, such as gaming and workstation GPUs**, we were **effectively foreclosed from competing in China's data center computing/compute market**, and our effective foreclosure from the China market helped our competitors build larger developer and customer ecosystems to challenge us worldwide."

来源：[NVIDIA 10-Q，报告期 2026-04-26（SEC EDGAR）](https://www.sec.gov/Archives/edgar/data/0001045810/000104581026000052/nvda-20260426.htm)

⚠️ **时效说明**：Q2 FY2027 的 10-Q 在本核验日（2026-08-13）**尚未申报**——EDGAR 上该 CIK（0001045810）最近的申报是 **2026-06-30 与 2026-07-02 的两份 8-K**。**故上述是目前可得的最新官方季度表述。**

**两条对 §3 直接有用的推论**（**I**）：

1. **数据中心级 NVIDIA GPU 在 2026 年上半年对华出货为零**——⛔ **H20 / H100 / H200 都不是「现在能买到」的东西**。
2. **但「游戏与工作站 GPU」明确仍可出货**（公司逐字称 "uncontrolled products"）。**这就是现实包络的实际下界所在**：消费 / 工作站卡，而不是数据中心卡。

### 1.15 时间线一览

| 生效 / 发生日 | 动作 | 对「640 GB H100 节点可得性」的影响 | 级别 |
| :-- | :-- | :-- | :-- |
| 2022-10-07 / 10-21 | 3A090 建立（600 GB/s 互连 **AND** bits×TOPS ≥4800） | A100 / H100 断供；**降级版 A800 / H800 出现** | M |
| **2023-11-17** | 删互连参数，改 TPP + performance density；目的地扩至 D:1 / D:4 / D:5 | ⛔ **A800 / H800 一并断供**；此后无合法的高端 NVIDIA 训练卡对华通道 | M |
| 2024-12-02（合规 12-31） | 3A090.c：**当时在产的全部 HBM** 受控 | 打击国产卡的 HBM 供应链，而非仅 NVIDIA | M |
| 2025-01-15 | AI Diffusion（含封闭权重模型权重） | 全球性许可要求 | S ⚠️ |
| 2025-04-09 / 14 | **H20 需许可，无限期** | ⛔ 中国最后一条合法数据中心卡通道也关上 | M |
| 2025-05-13 | AI Diffusion 停止执行；**昇腾 910B/C/D 列 GP 10 风险** | 名义放松，实际对昇腾使用者增加合规风险 | M / S ⚠️ |
| 2025-07-15 起 | H20 恢复（+ 报道称 15% 分成） | 短暂恢复 | S |
| **2025-11-05（报道）** | **中方：国家资金数据中心只用国产芯片** | **对型号 / 设计所层级，这是比美方管制更硬的约束** | S ⚠️ |
| **2026-01-15** | **H200 档放宽到 case-by-case**（TPP<21000 **且** DRAM 带宽<6500 GB/s） | 名义放宽 | M |
| 2026-01-14 | **中方拦下 H200 入境** | 名义放宽被中方一侧抵销 | S ⚠️ |
| 2026-05-31 | BIS 指南：D:5 总部实体的海外子公司同样需许可；**但存量可继续使用** | 存量合法，新增受限 | M |
| **2026-04-26 止（最新官方季报）** | **对华数据中心 Hopper 出货 = 0；H200 许可项下收入 = 0** | ⛔ **数据中心级 NVIDIA 卡在现实中不可得** | M |

## 2. 可得硬件的显存容量表（含国产卡）

### 2.1 NVIDIA 侧：中国大陆的现实可得性

| 产品 | 显存 | 中国大陆现状（2026-08） | 来源等级 |
| :-- | :-- | :-- | :-- |
| A100 40G / 80G | 40 / 80 GB HBM2e | ⛔ 2022-10 起需许可。**存量合法可继续用** | M（管制）· M（存量，§1.13） |
| H100 SXM | 80 GB HBM3 | ⛔ 2022-10 起需许可 | M |
| **A800 / H800** | 同 A100 / H100（80 GB 级） | ⛔ **2023-11-17 起一并需许可** | M |
| H200 SXM | 141 GB HBM3e | ⚠️ 2026-01-15 起 case-by-case；**2026-02 起确有发证，但截至 2026-04-26 收入为零、能否入境未知** | M |
| B200 / GB200 / GB300 | 180 GB+ HBM3e | ⛔ 超 21000 TPP / 6500 GB/s 门槛，不符合放宽条件 | I（按官方阈值验算） |
| **H20** | **96 GB HBM3**（⏳ 待核验） | ⛔ 2025-04 起需许可；2025-07 恢复；据报被中方劝退 / 禁于国家资金数据中心；截至 2026-04-26 对华数据中心 Hopper 出货为零 | S ⚠️（规格）· M（出货为零） |
| RTX PRO 6000（全球版） | 96 GB GDDR7 | ⛔ 非中国版 | S |
| **RTX 6000D（中国特供）** | **84 GB GDDR7**，448-bit，~1398 GB/s | ⚠️ 曾在售（约 ¥50,000）；据报**市场失败并被中方禁 / 劝退** | S ⚠️ |
| **RTX 5090D V2（中国在售）** | **24 GB GDDR7**，384-bit，1344 GB/s，AI 2375 TOPS | **合法在售**（发布价 ¥16,499）。属公司所称 "uncontrolled … gaming GPUs" | S（规格）· M（该类别可出货） |
| RTX 5090（全球版） | 32 GB GDDR7，1792 GB/s，AI 3352 TOPS | ⛔ 非中国版；灰市有 | S |

⚠️ **H20 的 96 GB 显存数字本轮只找到二级来源**（聚合站、经销商页、百科），⛔ **NVIDIA 官方数据表未找到**（见 §7.1）。该数字在 §3.4 里**承重**（「8×H20 = 768 GB > 640 GB」这条反向论据依赖它），故标为**待核验**。

⚠️ **RTX 6000D / 5090D V2 的规格同样只有二级来源**（Tom's Hardware、TweakTown、wccftech 等）。但「**5090D V2 在中国在售**」这一点与 NVIDIA 10-Q 的 "we were able to ship uncontrolled products to China, such as gaming and workstation GPUs" **相互印证**（**M** 支持类别，**S** 支持具体型号与容量）。

**关于 4090D / 5090D 反复改规格的机制**（**I**）：Note 2 to 3A090 逐字豁免「非为数据中心设计或营销**且** TPP <4800」的项目，而 2023 版又引入 performance density；消费卡的合规路径是把**带宽与 AI TOPS 压到门槛下**——5090D V2 把带宽从 1792 压到 1344 GB/s、AI TOPS 从 3352 压到 2375、显存从 32 GB 砍到 24 GB（**S**），据报是为压在 1.4 TB/s 线下。

### 2.2 国产 AI 加速卡

⛔ **本节最重要的一条元事实**：**华为在硬件产品页上根本不公布单卡 HBM 容量。** 核验员逐字读了 [Atlas 800I A2 官方产品页](https://e.huawei.com/cn/products/computing/ascend/atlas-800i-a2)，规格表里有 CPU、DDR4 插槽数、电源、网口、尺寸，⛔ **没有 NPU 数量、没有单卡显存、没有算力**。**「910B = 64GB」这个数字的官方出处在软件侧文档，不在硬件规格页。**

⛔ **第二条元事实**：**「910C」这个型号名从未出现在任何华为官方硬件规格表里**，只出现在二级报道（SemiAnalysis / 路透 / CSET）中。⚠️ 连华为自己的论文写的都是 "384 **Ascend 910** NPUs"（[arXiv:2506.12708](https://arxiv.org/abs/2506.12708) 当前版本摘要逐字）。**故若在论文里写「910C 有 xx GB」，没有官方可引证；必须改写成产品形态（Atlas A3 / Atlas 900 A3 SuperPoD）。**

#### 2.2.1 华为昇腾

| 型号 / 产品 | 显存容量 | 带宽 | 算力 | 来源等级 | 链接 |
| :-- | :-- | :-- | :-- | :-- | :-- |
| **Ascend 910（原版 / 910A）裸芯** | **32GB HBM Gen2** | 未给出 | 256 TFLOPS FP16 / 512 TOPS INT8，≤350W，7nm+ | **官方**（Hot Chips 31 华为演讲稿，逐字行 `Memory Interface｜32GB HBM Gen2`） | [DaVinci: A Scalable Architecture（PDF）](https://www.cmc.ca/wp-content/uploads/2020/03/Zhan-Xu-Huawei.pdf) |
| **Ascend 910B（Atlas A2 系列单卡）** | **64GB** | ⛔ 未公布 | ⛔ 未公布 | **官方**（措辞为 `Atlas 800I A2 (8*64G)` / `Atlas A2 inference products (64GB × 8)`） | [Ascend ModelZoo DeepSeek-R1 README](https://gitee.com/ascend/ModelZoo-PyTorch/blob/master/MindIE/LLM/DeepSeek/DeepSeek-R1/README.md) · [vllm-ascend Qwen3-Dense.md](https://github.com/vllm-project/vllm-ascend/blob/main/docs/source/tutorials/models/Qwen3-Dense.md) |
| ⚠️ **Ascend 910B4** | ⚠️ **32GB**（`npu-smi` 显示 `/ 32768` MB） | — | — | S（用户在官方仓库 issue 贴出的实机 `npu-smi info`，⛔ 非厂商规格） | [vllm-ascend issue #8746](https://github.com/vllm-project/vllm-ascend/issues/8746) |
| 910B1/B2/B3 = 64GB、B4 = 32GB 的分档说法 | — | — | — | ⏳ **待核验**（仅见 CSDN / 云厂商文档 / 知乎，⛔ 无华为官方分档表） | — |
| **Atlas A3 节点（即通常所指 910C）** | **8 NPU / 16 die，`64GB × 16` = 1024GB** | — | — | **官方**（vLLM-Ascend 教程逐字：`Atlas A3 inference products have 8 NPUs with dual-die design (16 chips total)`；硬件要求列 `64GB × 16`） | [Qwen3-Dense.md](https://github.com/vllm-project/vllm-ascend/blob/main/docs/source/tutorials/models/Qwen3-Dense.md) |
| **Atlas 900 A3 SuperPoD**（= CloudMatrix384 的整机柜形态） | **384 × 128GB 片上内存**，整机 **48TB 统一编址** | 片上内存带宽最大 **3.2TB/s**；D2D 双向 784GB/s | **307.2 / 288.7 PFLOPS @FP16** | **官方**（逐字读了规格表） | [Atlas 900 A3 SuperPoD 官方页](https://e.huawei.com/cn/products/computing/ascend/atlas-900-a3-superpod) |
| Atlas 800I A3 单机 | **128G × 8** | — | — | S（issue 提问者转述 DeepSeek-V4 教程，⛔ 未在 main 分支逐字复核） | [issue #8746](https://github.com/vllm-project/vllm-ascend/issues/8746) |
| ⚠️ **Atlas 300I Duo 推理卡** | ⚠️ **LPDDR4X 96GB 或 48GB**（**不是 HBM**） | ⚠️ 总带宽仅 **408GB/s** | 280 TOPS INT8 / 140 TFLOPS FP16，150W | **官方**（逐字读了规格表） | [Atlas 300I Duo 官方页](https://e.huawei.com/cn/products/computing/ascend/atlas-300i-duo) |
| **Atlas 350 加速卡（Ascend 950PR）** | **112GB HBM** | **1.4TB/s** | 1561 TFLOPS mxFP4 / 804 TFLOPS mxFP8·INT8 / **425 TFLOPS FP16·BF16**，≤600W，PCIe 5.0 | **官方** | [昇腾社区加速卡页](https://www.hiascend.com/hardware/accelerator-card) |
| **Atlas 950 SuperPoD（Ascend 950DT）** | **1024 × 96GB 片上内存** | **4.0TB/s** | 1 EFLOPS mxFP8/FP8/HiF8，2 EFLOPS mxFP4 | **官方** | [昇腾社区集群页](https://www.hiascend.com/hardware/cluster) |
| Atlas 300T A2 训练卡单卡显存 | ⏳ **待核验** | — | S 称 280 TFLOPS FP16 | ⏳ 待核验（⛔ 官方页未渲染该卡规格） | — |
| ⚠️ 「昇腾 910B2 显存带宽 392GB/s」 | — | ⛔ **疑为误记** | — | ⛔ **S 且存疑**：天翼云文档写 392GB/s 为显存带宽，而华为官方 Atlas 800I A2 页把 **392GB/s 写成「整机互联带宽」**——高度疑似把互联带宽误当显存带宽 | [天翼云规格页](https://www.ctyun.cn/document/10029787/10349596) vs [Atlas 800I A2 官方页](https://e.huawei.com/cn/products/computing/ascend/atlas-800i-a2) |

**910C / A3 显存的官方推导链（⛔ 请照这个链条引用，不要直接引「96GB」）**：三条**官方**事实拼起来——华为官方 A3 SuperPoD 规格表写 `384 * 128GB 片上内存`（48TB）；vLLM-Ascend 官方教程写 A3 节点 `8 NPUs with dual-die design (16 chips total)` 且硬件要求为 `64GB × 16`；华为自家论文写 CloudMatrix384 有 384 颗 NPU。⇒ **每 die 64GB、每封装（双 die）128GB、整机 384 封装 × 128GB = 48TB，三处自洽。**

⛔ **冲突的二级说法必须标为传闻**：SemiAnalysis 系报道流传的 **96GB HBM2e / 1.8TB/s** 与上面官方链条**不一致**；⚠️ CSET 亦指出 910C 规格「可能被下调以对齐 910B」，文档一度把 910C1 的 core 数从 50 改成 24。这些只能当线索。二级入口：[XPU.pub](https://xpu.pub/2025/04/22/huawei-ascend/) · [CSET 报告](https://cset.georgetown.edu/publication/pushing-the-limits-huaweis-ai-chip-tests-u-s-export-controls/) · [Lennart Heim 分析](https://blog.heim.xyz/huawei-ascend-910c/)。

#### 2.2.2 其它国产卡

| 型号 | 显存容量 | 带宽 | 来源等级 | 链接 |
| :-- | :-- | :-- | :-- | :-- |
| **寒武纪 MLU370-X8** | ⚠️ **48GB LPDDR5**（非 HBM） | ⚠️ **614.4 GB/s** | **官方**（逐字读了官网规格表：256 TOPS INT8 / 96 TFLOPS FP16·BF16 / 24 TFLOPS FP32，250W，MLU-Link 聚合 200GB/s） | [寒武纪官网 MLU370-X8](https://www.cambricon.com/index.php?m=content&c=index&a=lists&catid=406) |
| 寒武纪 MLU290-M5 | ⏳ **待核验**（容量未查到；S 称带宽 1.23TB/s） | — | ⏳ 待核验（⛔ 官网该栏目返回 **HTTP 500**） | [栏目链接](https://www.cambricon.com/index.php?m=content&c=index&a=lists&catid=340) |
| 寒武纪 思元590 / MLU590 | ⛔ **官方规格页未找到**。二级说法互相冲突：96GB HBM2e vs 64GB vs 明确标「推测」 | — | ⏳ **待核验** | — |
| 寒武纪 思元690 / MLU690 | ⛔ **官方未发布规格**。二级冲突：96GB HBM3 + 2400GB/s（大摩口径）vs 196GB HBM3（网易财经）。**寒武纪本身公开辟谣过网传新产品规格纪要** | — | ⏳ **待核验** | — |
| 壁仞 BR100 | **64GB HBM2e** | ⚠️ 官宣 2.3TB/s vs 计算口径 1.64TB/s 两说 | S（2022 发布会报道 + Hot Chips 34 材料；⛔ 未逐字打开 HC34 PDF） | [Hot Chips 34 BR100 PDF](https://hc34.hotchips.org/assets/program/conference/day1/GPU%20HPC/HC2022.BirenTech.MikeHong.LingjieXu.v01.pdf) |
| 壁仞 BR104 | **32GB HBM2e**（单 die） | S 称 1.14TB/s | S | 同上 |
| ⛔ **壁仞当前在产品（壁砺 106M / 106B / 166M / 166L）** | ⛔ **官方产品页不公布显存**。逐字读了 106M 页，**全页唯一数字是「峰值功耗 400W」**，无容量、无带宽、无内存类型。第三方称 106M 为 32GB | — | ⛔ **官方确认「未公布」** | [壁砺 106M 官方页](https://www.birentech.com/product/hardware/106m/) |
| **摩尔线程 MTT S4000** | ⚠️ **48 GB** | ⚠️ **768 GB/s** | **官方**（逐字读了规格表：PCIe 5.0 x16，MTLink 240GB/s，最大功耗 450W。⚠️ **官方表只写各精度「支持」，不给 TFLOPS**） | [MTT S4000 官方页](https://www.mthreads.com/product/S4000) |
| ⛔ **摩尔线程 MTT S5000** | ⛔ **官方页不公布显存数字**（逐字确认：无容量、无带宽、无 TDP，只有「FP8 到 FP64 全精度」与整机 token/s）。二级称 80GB / 1.6TB/s / 1000 TFLOPS FP8 | — | ⛔ **官方未公布** + S | [MTT S5000 官方页](https://www.mthreads.com/product/S5000) · [新浪科技](https://finance.sina.com.cn/tech/roll/2026-02-12/doc-inhmpkar4117688.shtml) |
| **天数智芯 智铠100（MR-V100）** | **32 GB HBM2E**（同页 MR-V50 = 16GB HBM2E） | ⛔ 官方页**未给带宽**（S 称 800GB/s） | **官方**（逐字读了规格表：板级功耗 150W，PCIe Gen4 x16。⚠️ 官方页**不给任何 TFLOPS**） | [天数智芯官方产品页](https://www.iluvatar.com/productDetails?fullCode=cpjs-yj-tlxltt-zk100) |
| 天数智芯 天垓100（BI-V100） | **32GB HBM2**，S 称 1.2TB/s、147 TFLOPS FP16 | — | S（⛔ 未打开天垓官方产品页） | — |
| ⛔ **海光 DCU 深算系列** | ⛔ **官方规格页未找到**（`hygon.cn/product/accelerator` 只返回网站的 MIT LICENSE 文本）。二级冲突：K100-AI = 64GB HBM3 + 896GB/s vs 40GB HBM2e vs 64–128GB | — | ⏳ **待核验** | [hygon.cn](https://www.hygon.cn/) · S：[arXiv:2606.28421 集群描述](https://arxiv.org/html/2606.28421v2) |
| 海光深算一号 | 32GB、4×HBM2 通道、最高 1TB/s | — | S（招股说明书转述，⛔ 未打开原件） | — |

⛔ **一条对选型极重要、且容易被容量数字掩盖的事实**：**寒武纪 MLU370-X8 与摩尔线程 S4000 的「48GB」是 LPDDR5 / GDDR 级，不是 HBM；华为 Atlas 300I Duo 的「96GB」是 LPDDR4X，带宽仅 408GB/s。** ⛔ **容量数字相同但带宽差一个量级**，对 32B 级模型的 decode 吞吐影响很大——**不能只按容量选型**（**I**）。

⛔ **除华为外，国产卡厂商普遍不公布显存规格**：壁仞在产品线、摩尔线程 S5000、海光全线、寒武纪 590/690 都是「官方未公布」或「查无官方来源」。**目前能拿到官方出处的国产卡显存数字只有四条**：华为（间接、经软件文档）、寒武纪 MLU370-X8、摩尔线程 S4000、天数智芯智铠100——⚠️ **且后三者是 LPDDR5 / HBM2E 而非新一代 HBM。**

**一条与国产卡显存直接相关的管制事实（已核，M）**：§1.4 的 3A090.c 把「当时在产的全部 HBM」纳入管制，BIS 明说目的是 "slow PRC attempts to indigenize advanced AI chip production"。⛔ **故国产卡的显存容量不是一个纯技术变量，它受 HBM 进口通道约束。**

## 3. 由此推出的现实部署包络（与「8×80G = 640 GB」假设的对比）

### 3.1 计算口径（沿用 [c5_arithmetic_check.md](./c5_arithmetic_check.md) §4.2 已校准口径）

可容总参上限 $P_{\max} = V \times 0.88 / b$，其中 $V$ 是标称显存总量（GB），$0.88$ 是扣除常驻开销后的可用率（框架预留约 8% + KV cache + 激活 / CUDA graph / NCCL 缓冲，合计吃掉标称的 **10–15%**），4-bit 取 $b = 0.57$ B/参（实测锚点区间 **0.55–0.62**，中心 0.57）。**MoE 的全部专家权重须常驻**，故进公式的是**总参**而非激活参数。

⚠️ **两条使本表偏保守的因素**（已在 [SUMMARY.md](./SUMMARY.md) §12.2 记录，此处不重复论证）：专家可卸载到主机内存（DeepSeek-V3 `Q2_K_XS` 官方称 ~40 GB 可跑）；KV 量化到 FP8 可再省。⛔ **本表不采用这些放宽**，与原 640 GB 表口径保持一致，**以保证可比**。

### 3.2 现实包络表

| # | 现实可得配置 | 可得性（2026-08） | 显存总量 | 4-bit 可容总参上限 | 相对 640 GB 基准 | 级别 |
| :-- | :-- | :-- | --: | --: | --: | :-- |
| 1 | **单张 RTX 5090D V2 / 4090D**（中国在售消费卡） | **合法在售** | 24 GB | **~37B** | **0.04×** | S 规格 · I 计算 |
| 2 | 单张 RTX 5090（32G，灰市 / 非中国版）· 或单张 Ascend 910B4 | ⚠️ 灰市 / 国产 | 32 GB | ~49B | 0.05× | S · I |
| 3 | 双卡 RTX 4090D / 5090D V2 工作站 | 合法 | 48 GB | ~74B | 0.07× | S · I |
| 3b | 单张寒武纪 MLU370-X8 或摩尔线程 S4000（⚠️ **LPDDR5 级，非 HBM**） | 国产，官方规格可引 | 48 GB | ~74B | 0.07× | M 规格 · I 计算 |
| 4 | **单张 Ascend 910B（64 GB）** | 国产，中方鼓励 | 64 GB | **~99B** | 0.10× | **M**（经官方软件文档）· I |
| 5 | 单张 RTX 6000D（中国特供 84G） | ⚠️ 据报已被中方禁 / 劝退 | 84 GB | ~130B | 0.13× | S ⚠️ · I |
| 6 | 单张 H20（96G，2024–2025 合法售出的存量） | ⚠️ 仅存量；据报禁于国家资金数据中心 | 96 GB | ~148B | 0.15× | S ⚠️ · I |
| 6b | ⚠️ 单张 Atlas 300I Duo（**96 GB LPDDR4X，带宽仅 408 GB/s**） | 国产在售 | 96 GB | ~148B | 0.15× | M 规格 · I 计算 |
| 7 | **单张 Atlas 350 加速卡（Ascend 950PR，112 GB HBM @ 1.4 TB/s）** | **国产新一代，官方规格** | 112 GB | **~173B** | 0.18× | **M** 规格 · I |
| 7b | 单封装 Atlas A3 NPU（双 die，`64GB × 2`） | 国产 | 128 GB | ~198B | 0.20× | M（官方推导链）· I |
| 8 | 4 张 Ascend 910B（64G） | 国产 | 256 GB | ~395B | 0.40× | M · I |
| 9 | **8 张 Ascend 910B = 一台 Atlas 800I A2 整机** | **国产整机；「设计所能买到的最大常规单机」这一档** | 512 GB | **~790B** | **0.80×** | **M** · I |
| — | ★ **假设的 8×80G H100 节点（原包络假设）** | ⛔ **2022-10 起断供；仅存量** | **640 GB** | **~988B** | **1.00×** | M（管制）· I（计算） |
| 10 | 8 张 H20 = 一台 HGX H20 节点（存量） | ⚠️ 仅存量 | 768 GB | **~1186B** | **1.20×** | S ⚠️ · I |
| 11 | **一台 Atlas A3 节点（8 NPU / 16 die，`64GB × 16`）= 2 台 Atlas 800I A2** | **国产；这正是官方 671B 部署的最低门槛档，见 §4.1** | 1024 GB | **~1581B** | **1.60×** | **M** · I |
| 12 | 8×141G H200 节点 | ⛔ 对华出货为零 | 1128 GB | ~1742B | 1.76× | M · I |
| 12b | 8 张 Atlas 350（112 GB HBM） | 国产新一代 | 896 GB | ~1383B | 1.40× | M 规格 · I |
| 13 | Atlas 900 A3 SuperPoD / CloudMatrix384（384 封装 × 128 GB） | 国产，但⛔ **超大规模云基础设施**，非设计所层级 | **48 TB**（官方口径） | ~74,105B | 75.0× | **M** 显存 · I 计算 |
| 13b | Atlas 950 SuperPoD（1024 × 96 GB @ 4.0 TB/s） | 国产，同上⛔ 非设计所层级 | 96 TB | ~148,211B | 150.0× | **M** 显存 · I 计算 |

**逐格复算**（$V \times 0.88 / 0.57$）：$24 \to 37.1$ · $32 \to 49.4$ · $48 \to 74.1$ · $64 \to 98.8$ · $84 \to 129.7$ · $96 \to 148.2$ · $112 \to 172.9$ · $128 \to 197.6$ · $256 \to 395.2$ · $512 \to 790.5$ · $640 \to 988.1$ · $768 \to 1185.7$ · $896 \to 1383.3$ · $1024 \to 1580.9$ · $1128 \to 1741.5$ · $49152 \to 75883.8$。⚠️ 第 13 行用官方「48 TB」口径（$= 49152$ GB 的官方约整为 48 TB，此处按 $48 \times 1024 = 49152$ GB 反算得 $75884$；若按十进制 48000 GB 则为 $74105$，**表内采用后者以贴合官方措辞**）；第 13b 行 $1024 \times 96 = 98304$ GB $\to 151768$，按十进制 96000 GB 计为 $148211$。

⚠️ **一处必须记下的现实校准**：官方仓库 issue [#1127](https://github.com/vllm-project/vllm-ascend/issues/1127) 报告 **DeepSeek-R1-W8A8 在 2×8×910B2（合计 1024 GB）上 OOM**（`-tp 8 -pp 2`，`--gpu-memory-utilization 0.95`）。按本文口径算 671B 的 8-bit 权重需 $671 \times 1.03 = 691$ GB、计入常驻项后 $691 / 0.88 = 785$ GB $< 1024$ GB，**理论上装得下**。⛔ **故实测的常驻开销比本文的 0.88 更重**——这说明本表在「刚好装得下」的格子上**偏乐观**，不宜按上限贴边选型（**I**）。

### 3.3 与原假设的对比：三条结论，方向各不相同

**结论 A：「640 GB 可得」这个假设本身站不住，但理由不是「买不到大显存」。** 美方一侧，A100 / H100 / A800 / H800 自 2023-11-17 起全无合法通道（**M**）；H200 虽自 2026-02 起有发证，但截至 2026-04-26 出货为零（**M**）。中方一侧，据报国家资金数据中心只许国产（**S** ⚠️）。故正确表述是：⛔ **「8×80G H100 这个形态在 2026 年不是一个可采购的东西」**，而不是「640 GB 太大」。

**结论 B：方向性结论仍成立，但倍数从 ~49× 塌到 ~1.9×。**

| 口径 | 4-bit 上限 | 相对方法所需 ≤20B |
| :-- | --: | --: |
| 原假设（8×80G H100，640 GB） | ~988B | **~49×** |
| **最悲观现实配置（单张 24 GB 在售消费卡）** | **~37B** | **~1.9×** |
| 现实中位（单张 910B，64 GB，**官方 M**） | ~99B | ~4.9× |
| 现实上界（一台 8 卡国产整机，512 GB） | ~790B | ~40× |
| **官方 671B 部署档（2 台整机 / 1 台 A3 节点，1024 GB）** | ~1581B | ~79× |

**一个 32B 模型在 4-bit 下需 $32 \times 0.57 = 18.24$ GB 权重，计入常驻开销后约 $18.24 / 0.88 = 20.7$ GB**（**I**）——⚠️ **这已经贴到一张 24 GB 卡的上沿，几乎没有余量**（长上下文的 KV 会把它顶出去）。换成 32 GB 或 48 GB 则宽松。故「**Qwen 32B 级在单卡跑得动**」这句话在 4-bit 下**勉强成立**、在 BF16 下**明确不成立**（BF16 需 $32 \times 2 = 64$ GB）。

⚠️ **但必须区分「理论装得下」与「官方怎么建议」**：上面 20.7 GB 是本文的 **I 级计算**；⛔ **昇腾官方对 Qwen3-32B 的建议是「单节点 + TP4」**（W8A8）或 **TP2**（W4A4），即 4 张或 2 张 64 GB 卡，**而不是一张卡**（**M**，§4.2）。官方唯一给出的「小配置」路径是 Atlas 300I Duo + W8A8SC + TP4，且代价明确写在参数里：`--dtype float16`、`--max-model-len 20480`、`--max-num-seqs 32`。**故「32B 单卡可跑」不能引官方文档作支撑。**

**结论 C：⛔ 原来那条「总能部署一个大到不需要脚手架的开放权重模型」的推论，在单卡档减弱、⛔ 但在整机档不但成立、反而有官方部署证据支撑。**

它原本靠 ~988B 支撑。现实包络下：

- ⛔ **单卡到单封装档（#1–#7b，37B–198B）都够不上「大到不需要脚手架」那一档。**
- **一台 8 卡 910B 整机（512 GB，~790B）够得上。**
- ⛔ **而且比这更硬**：**671B MoE 在昇腾上的官方最低部署门槛就是「2 台 Atlas 800I A2（16 × 64GB = 1024 GB）跑 W8A8」**——这是 MindIE 与 vLLM-Ascend **两条独立路径给出的一致官方口径**（逐字见 §4.1，**M**）。⛔ **即 671B 级模型的私域部署不需要 CloudMatrix384，两台国产整机就够。**

⚠️ **所以这条反向论据比本文初稿写的更强，必须如实记下**（按 §3.5 的方向性松紧一致原则——⛔ **不利于本目录 story 的一侧同样要写满**）：**一个买得起两台国产整机的单位，确实能部署 671B 级开放权重模型，且有官方教程可循。** 该推论只在**买不起整机、只有单卡或工作站**的单位那里不成立。

⚠️ **两条限定同时保留**：**(a)** ⛔ 官方 issue [#1127](https://github.com/vllm-project/vllm-ascend/issues/1127) 显示该配置在实机上会 OOM，即 1024 GB 是**贴边**而非宽裕（**S**，但在官方仓库内）；**(b)** 用 32 GB 卡（910B4）凑总量是**明确不被支持**的路径——issue [#8746](https://github.com/vllm-project/vllm-ascend/issues/8746)（8×910B4 = 256 GB 能否单机跑 V4-Flash）**至今 open、无官方结论**（**S**）。

### 3.4 ⛔ 四条反向事实，不得省略

1. ⛔ **管制管出口，不管存量使用。** BIS 2026-05-31 指南逐字确认 bona fide 数据中心运营方**不因该指南被要求停止**已有先进计算项目的 use / storage / disposal / servicing（**M**，§1.13）。A100 在 2022-10 之前对华自由销售多年，**中国机构手里的 A100 存量是合法的**（**I**）。
2. ⛔ **存量里确实有 >640 GB 的节点。** H20 在 2024 至 2025-04、以及 2025-07 之后合法在华销售，**单季销售额曾达 46 亿美元**（**M**，NVIDIA 申报）。**一台 8×H20 = 768 GB，4-bit 下 ~1186B，比原假设的 640 GB / 988B 还宽**（**I**；⏳ 依赖 H20 = 96 GB 这个待核验数字）。⛔ **所以「中国工业单位不可能有 640 GB 级节点」是错的。**
3. ⛔ **671B MoE 在国产生态上有官方成功部署，且门槛只有两台整机。** 见 §4.1 与 §4.5。⛔ **「国产卡跑不了大 MoE」是错的**；**「跑得了但要 384 卡超节点」也是错的**（本文初稿的说法，已更正）。
4. ⛔ **方法实际需求的 32B 档在昇腾上单节点即可，有官方教程与官方量化权重。** 见 §4.2。⛔ **「国产卡跑不了我们需要的那一档」是错的。**

**把四条合起来的诚实表述**：**约束不在「显存买不到」，而在「以什么身份、走什么渠道、在什么合规前提下买」。** 一个能拿到国家资金的型号研制单位，恰恰是**最不能走灰市、最必须用国产**的那类主体（**I**，若 §1.10 的报道成立）。

## 4. 软件栈对超大 MoE 的支持现状

### 4.0 结论先行

**有官方公开的成功部署案例，而且不止一条路径。** 671B MoE（DeepSeek-R1/V3）在昇腾上是**有官方教程、有官方量化权重、有官方精度数字**的一等公民；**专家并行（EP）不是「待支持」，而是官方教程里的默认配置项**；且当前主线已推进到 DeepSeek-V4 / GLM-5.2 / Qwen3.5 这一代。

⛔ **但这份「支持」是节点级的**——官方要求以「多少台 8 卡 / 16 卡整机」为单位表述，最小档位是 **2 台 Atlas 800I A2（16 × 64GB = 1024 GB）跑 W8A8**。⛔ **用 32 GB 卡凑总量是明确不被支持的路径。**

**而对本文最关键的一档——Qwen3-32B——支持非常成熟：单节点即可，甚至 Atlas 300I Duo 都有官方教程。**

### 4.1 官方要求的卡数与精度（逐字核验）

| 模型 | 栈 | 官方硬件要求（逐字） | 级别 | 链接 |
| :-- | :-- | :-- | :-- | :-- |
| DeepSeek-R1-W8A8 | **vLLM-Ascend** | `require 1 Atlas 800 A3 (64G × 16) nodes or 2 Atlas 800 A2 (64G × 8) nodes` | **M** | [DeepSeek-R1.md](https://github.com/vllm-project/vllm-ascend/blob/main/docs/source/tutorials/models/DeepSeek-R1.md) |
| DeepSeek-R1 W8A8 | **MindIE** | 「部署DeepSeek-R1模型用W8A8量化权重进行推理则至少需要**2台Atlas 800I A2 (8*64G)**。」 | **M** | [Ascend ModelZoo-PyTorch](https://gitee.com/ascend/ModelZoo-PyTorch/blob/master/MindIE/LLM/DeepSeek/DeepSeek-R1/README.md) |
| DeepSeek-R1 **BF16** | MindIE | ⚠️ **该 README 里没有 BF16 的卡数要求。** 它只说 FP8 权重约 640G、转 BF16 后约 1.3T。**广为流传的「BF16 至少 4 台 800I A2」未在官方 README 中核到** | ⛔ S | 同上 |
| DeepSeek-R1 671B W8A8 | **vLLM-MindSpore** | 2 台 Atlas 800 A2 共 16 × 64GB NPU，配置为 **DP4 × TP4 × EP4** | M（标题与配方名 `deepseek_r1_671b_w8a8_dp4_tp4_ep4` 已确认；⛔ 正文仅见搜索摘要） | [mindspore.cn 教程](https://www.mindspore.cn/vllm_mindspore/docs/zh-CN/master/getting_started/tutorials/deepseek_parallel/deepseek_r1_671b_w8a8_dp4_tp4_ep4.html) |
| DeepSeek-V4-Flash | vLLM-Ascend | `Atlas 800I A2 (64G x 8)` 或 `Atlas 800I A3 (128G x 8)` | S（issue 提问者转述教程） | [issue #8746](https://github.com/vllm-project/vllm-ascend/issues/8746) |

**EP 是官方配置项，逐字证据**：DeepSeek-R1.md 的双机启动脚本含 `--data-parallel-size 4`、`--data-parallel-size-local 2`、`--tensor-parallel-size 4`、**`--enable-expert-parallel`**、`--speculative-config '{"num_speculative_tokens":3,"method":"mtp"}'`。支持矩阵里 DeepSeek V3/3.1/R1 在 A2/A3 上的 **expert parallel、data parallel、PD disaggregation、两种 graph mode 均标 ✅**（**M**）。

**官方给的精度数字**（DeepSeek-R1-W8A8）：`aime2024 accuracy 80.00`、`gpqa accuracy 72.22`。⛔ **官方教程不给吞吐数字**，只给 `ais_bench` / `vllm bench serve` 的跑法（**M**）。

### 4.2 Qwen3-32B 档位（本文的实际需求档）——支持很成熟

以下全部 **M**，出自 [Qwen3-Dense.md](https://github.com/vllm-project/vllm-ascend/blob/main/docs/source/tutorials/models/Qwen3-Dense.md)（基于 vLLM-Ascend **v0.21.0** 验证，main 分支逐字）：

| 变体 | 官方硬件要求（逐字） | 并行度 |
| :-- | :-- | :-- |
| Qwen3-32B（**BF16**） | `1 Atlas A3 inference products (64GB × 16), 1 Atlas A2 inference products (64GB × 8)` | **单节点** |
| Qwen3-32B-**W8A8** | `1 Atlas A3 inference products (64GB × 16) or 1 Atlas A2 inference products (64GB × 8)` | `--tensor-parallel-size 4` |
| Qwen3-32B-**W4A4** | 同上（W4A4 自 v0.11.0rc1 起支持） | `--tensor-parallel-size 2` |
| Qwen3-32B-**W8A8SC** | `Atlas 300I DUO (TP4)` | `--tensor-parallel-size 4`、`--dtype float16`、`--max-model-len 20480`、`--max-num-seqs 32`、`--no-enable-prefix-caching`、`--load-format sharded_state`、`FULL_DECODE_ONLY` |

官方还给了调优档位：高吞吐 / 长上下文 = 单节点 TP4 + W8A8；低延迟 = 单节点 TP8 + W8A8（**M**）。

⚠️ **版本漂移警告**：检索摘要给出的是**旧版**措辞「Qwen3-32B-W8A8 需要 2 张 Atlas 800 A3 (64G × 4) 或 4 张 Atlas 800I A2 (64G × 4)」，⛔ **与 main 分支逐字读到的不一致**。**以上表（main 分支）为准**，并注意 vLLM-Ascend 各版本教程的硬件要求措辞会变。

**其它国产卡跑 Qwen3-32B 的公开支持**：

| 厂商 | 状态 | 级别 | 链接 |
| :-- | :-- | :-- | :-- |
| 华为昇腾 | **官方教程 + 官方量化权重**（W8A8 / W4A4 / W8A8SC-310） | **M** | 上表 |
| 海光 DCU | 宣布 Qwen3 全 8 款（含 32B）「零错误、零兼容性问题」适配 | S（⛔ 厂商公关稿经媒体转载，未找到 hygon.cn 官方原文） | [21ic 转载](https://www.21ic.com/a/986112.html) · [科技日报](https://www.stdaily.com/web/gdxw/2025-04/29/content_333311.html) |
| 昆仑芯 P800 | Qwen3-32B（TP=8）吞吐 1184 tok/s、TTFT 1.8 s；有 vLLM-Kunlun 插件 | S | [Spader.AI](https://spader-ai.com/blog/2026-01-06-xpu-qwen3-deployment/) |
| 摩尔线程 / 寒武纪 | ⛔ **未检索到 Qwen3-32B 的专项官方适配公告**（两家都在 2025-02 的 DeepSeek 适配潮里出现过） | ⛔ **查无来源** | — |

### 4.3 ⛔ 已知的显存 / 生态瓶颈（官方自陈，逐字）

以下全部逐字出自 [vllm-ascend faqs.md](https://github.com/vllm-project/vllm-ascend/blob/main/docs/source/faqs.md)（**M**）：

1. ⛔ **硬件白名单**：`Currently, ONLY Atlas A2 series ... Atlas A3 series ... and Atlas 300I (Ascend-cann-kernels-310p) series are supported`；`Atlas 200I A2 ... unplanned yet`；⚠️ Atlas 300I Duo 标注为 **`[Experimental]`**。
2. ⛔ **算子覆盖的边界就是 TorchNPU 的边界**：`From a technical view, vllm-ascend supports devices if TorchNPU is supported. Otherwise, we have to implement it by using custom ops.` **这是「算子覆盖不足」的官方原话形态。**
3. ⛔ **显存碎片导致 OOM**：`In scenarios where NPUs have limited high bandwidth memory (on-chip memory) capacity, dynamic memory allocation/deallocation during inference can exacerbate memory fragmentation, leading to OOM.` 缓解手段：限 `--max-model-len`、降 `--gpu-memory-utilization`（默认 **0.9**）、`PYTORCH_NPU_ALLOC_CONF=expandable_segments:True`。
4. ⛔ **MLA + graph mode 的头数硬约束**：`the number of queries per KV head must be 32, 64, or 128`；DeepSeek-V2-Lite 只有 16 头因而不支持 graph mode。实机报错原文：`numHeads / numKvHeads = 8, MLA only support {32, 64, 128}.`
5. ⛔ **ACL graph 捕获资源不足**：`ACL graph capture can still fail when the runtime resources required by the selected graph sizes exceed what the current software/hardware stack can provide`，PIECEWISE 模式最明显，⚠️ 且 **vLLM Ascend 已不再自动缩减捕获集**，只能升 HDK/CANN 或手动降 `cudagraph_capture_sizes`。
6. **量化方法覆盖**：`Currently, w8a8, w4a8, and w4a4 quantization methods are already supported`。⛔ **FP8 不在列。**

**社区 issue 反映的真实问题**（**S**，但均在官方仓库内）：

- [#1127](https://github.com/vllm-project/vllm-ascend/issues/1127) DeepSeek-R1-W8A8 在 **2×8×910B2（64GB）** 上 **OOM**（`-tp 8 -pp 2`，`--gpu-memory-utilization 0.95`）
- [#2344](https://github.com/vllm-project/vllm-ascend/issues/2344) **32 卡**（910B1 64G×8 ×4）DP8/TP4 + `--enable-expert-parallel` + torchair graph，EngineCore 初始化失败
- [#2015](https://github.com/vllm-project/vllm-ascend/issues/2015) 910B + v0.9.2rc1 启动即 `Engine core initialization failed`
- [#8746](https://github.com/vllm-project/vllm-ascend/issues/8746) **8×910B4 32GB（合计 256GB）能否单机跑 V4-Flash** —— ⛔ 32GB 卡凑总量的典型碰壁场景，**至今 open、无官方结论**
- [PR #1829](https://github.com/vllm-project/vllm-ascend/pull/1829) 已修：长输入序列在 `fused_moe.py` 里过度 padding 导致的 OOM

### 4.4 支持矩阵现状

**M**，出自 [supported_models.md](https://github.com/vllm-project/vllm-ascend/blob/main/docs/source/user_guide/support_matrix/supported_models.md)：

- **A2 / A3 上 ✅ 完全支持**：DeepSeek V3 / 3.1（240k）、V3.2（160k，唯一 LoRA ✅）、**R1（128k）**、**Qwen3-Dense（128k）**、Qwen3-30B-A3B、Qwen3-235B-A22B（256k）、GLM-4.x
- **🔵 实验性**：DeepSeek V4-Flash / V4-Pro（1M）、Qwen3-Next、GLM-5 / 5.1 / 5.2、Kimi-K2-Thinking、MiniMax-M2.5 / 2.7
- ⚠️ **Atlas 300I DUO 只有两行 ✅**（Qwen3-Dense 20k、Qwen3-30B-A3B 16k），⛔ 且 **BF16 ❌**（只能 W8A8）
- Ascend 950 产品线另有 DeepSeek V4-Flash / Pro 的 `Native mixed MXFP8/MXFP4 weights`
- ⚠️ **矩阵里没有单独的「Qwen3 32B」行**，dense 全部归入 `Qwen3-Dense`；最接近的 32B 独立条目是 `QwQ-32B`（🔵 实验性）

### 4.5 671B MoE 在昇腾上确有官方公开的成功部署

这一条的来源是 **Huawei 自己团队的论文**，属一手来源（**M**，就「Huawei 如此公开报告」这一事实而言）。

| 项 | 内容 | 级别 |
| :-- | :-- | :-- |
| 论文 | *Serving Large Language Models on Huawei CloudMatrix384* | M |
| 来源 | [arXiv:2506.12708](https://arxiv.org/abs/2506.12708) · DOI [10.48550/arXiv.2506.12708](https://doi.org/10.48550/arXiv.2506.12708) · 59 页 / 24 图 · cs.DC | M |
| 系统 | 逐字：**"It integrates 384 Ascend 910 NPUs and 192 Kunpeng CPUs interconnected via an ultra-high-bandwidth Unified Bus (UB) network"** | M |
| 被服务模型 | 逐字：**"Evaluation with the DeepSeek-R1 model"**（671B MoE） | M |
| 并行策略 | 逐字：**"a large-scale expert parallelism strategy supporting EP320 via efficient UB-based token dispatch"** | M |
| 量化 | 逐字：**"INT8 quantization"**；并称 **"INT8 quantization maintains model accuracy across benchmarks"** | M |
| 吞吐 | 逐字：prefill **6,688 tokens/s per NPU**；decode **1,943 tokens/s per NPU**（TPOT <50 ms）；15 ms 严格约束下仍 **538 tokens/s per NPU** | M |

⚠️ **一处版本差异需注意**：v3 摘要写的是 "384 **Ascend 910** NPUs"（型号被泛化），⛔ 而配套论文与二级来源均称是 **910C**。故「CloudMatrix384 用的是 910C」这一点**在本文只能记 S**。

**配套论文**（同为 Huawei 团队）：*xDeepServe: Model-as-a-Service on Huawei CloudMatrix384*，[arXiv:2508.02520](https://arxiv.org/abs/2508.02520)。据其表述：一个 CloudMatrix384 SuperPod = **48 台服务器 × 8 颗 Ascend 910C = 384 颗**；单颗 910C 为**双 die**、经高带宽 NoC 互连、每 die 最多 48 个计算核（故 **768 个 NPU die**）；整域提供数百 PFLOPS FP16、数 TB 片上内存（**S** ⚠️ ——⛔ 本轮**未逐字核对该文全文**，取自搜索摘要）。

### 4.6 ⛔ 已被报告的生态瓶颈：昇腾不原生支持 FP8

**三条证据的强度不同，必须分开说**：

1. **M**：vLLM-Ascend 官方 FAQ 逐字列出支持的量化方法为 `w8a8, w4a8, and w4a4`——⛔ **FP8 不在列**（§4.3 第 6 条）。
2. **M**：CloudMatrix384 主论文摘要逐字出现 **"INT8 quantization"**，且称 "INT8 quantization maintains model accuracy across benchmarks"（§4.5）。
3. ⚠️ **S**：「**因为昇腾 NPU 不原生支持 FP8**，故 FP8 训练的 DeepSeek-R1/V3 必须经**训练后量化（PTQ）转 INT8**」这条**因果**表述取自 2508.02520 的检索摘要，⛔ **未逐字核对全文**。

⛔ **即：「用了 INT8」是官方事实（M）；「因为不支持 FP8 才用 INT8」是待核验的因果（S）。** 但第 1 条（官方支持列表不含 FP8）**独立地印证了同一方向**。

⚠️ **一条重要的时效限定**：**新一代硬件已支持 FP8**——Atlas 350（Ascend 950PR）官方规格含 **mxFP8 804 TFLOPS**，Atlas 950 SuperPoD 官方规格含 **1 EFLOPS mxFP8/FP8/HiF8**，且支持矩阵里 Ascend 950 产品线有 DeepSeek V4 的 `Native mixed MXFP8/MXFP4 weights`（**M**，§2.2.1 与 §4.4）。⛔ **故「昇腾不支持 FP8」只对 910B / A2 / A3 这一代成立，不得写成对昇腾全线的断言。**

**这一点的意义**：⛔ 它不是「跑不了」，而是「**必须多一道量化转换，且转换后的等价性需要自己论证**」。⛔ 对本仓库的实验可复现性有直接影响——**在 910B 级硬件上复现一个 FP8 发布的开放权重模型，其数值行为与在 NVIDIA 上不同**，而这条差异**不能只在 Threats to Validity 里一句话带过**（**I**）。

### 4.7 ⛔ 规模含义：671B 的门槛比 CloudMatrix384 低得多

⛔ **本节的初稿曾把 CloudMatrix384（384 NPU / 48 服务器 / 4 通信机柜）当成 671B 的部署门槛来写——那是错的，已更正。** 官方给出的**最低**门槛是 **2 台 Atlas 800I A2（16 × 64GB = 1024 GB）跑 W8A8**，且 MindIE 与 vLLM-Ascend **两条独立路径口径一致**（§4.1，**M**）。**CloudMatrix384 是吞吐优化的超节点形态，不是可行性门槛。**

**故正确的三段表述是**：

1. **671B 级 MoE 在国产生态上「有官方成功部署案例」已证实（M），且门槛是两台整机、不是超节点（M）。**
2. ⚠️ **但该门槛在实机上是贴边的**——官方仓库 issue #1127 在同等配置下 OOM（**S**，§4.3）。
3. ⛔ **「某个具体的设计所是否买得起两台整机」无证据**（见 §5）——⛔ 这是一个**采购与预算**问题，不是技术可行性问题。

### 4.8 ⏳ 待补项

原列的四项**已全部完成**，见 §4.1–§4.4。⛔ 剩余未解决的是：

- ⛔ **寒武纪 / 壁仞 / 摩尔线程 / 海光**等其余国产栈的**大 MoE**（671B 级）支持情况——⛔ 本轮只找到 DeepSeek 适配潮时期的厂商公关稿，**无官方技术文档级证据**
- ⛔ **摩尔线程 / 寒武纪对 Qwen3-32B 的官方适配公告**——⛔ **查无来源**
- ⚠️ **vLLM-MindSpore 的 671B 教程正文**（仅确认了标题与配方名 `deepseek_r1_671b_w8a8_dp4_tp4_ep4`，⛔ 正文只见搜索摘要）
- ⚠️ 「DeepSeek-R1 **BF16** 至少 4 台 800I A2」这条流传说法——⛔ **未在官方 README 中核到**

## 5. 工业单位实际算力现状（含「查无可引来源」的如实记录）

### 5.1 ⛔ 一句话结论

**有可引来源，但没有任何一条直接回答「中国工业企业私有化 LLM 部署的实际规模」。** ⛔ **委托方的预判基本成立。** 可引的共 6 条，分三类：① 1 篇**全球实测**研究给出自托管 LLM 服务数量与中国占比（⛔ 但测的是公网暴露服务，不是企业内网）；② 4 篇给出「本地算力档位 = 单张消费卡 / 单张 A100」的**具体硬件与价格表**（这是方法论文的动机段与配置表，**不是**行业调查）；③ 1 份**中国官方政策文件**逐字承认中小企业算力获取门槛。

### 5.2 命中清单（均经核验员亲自打开原文）

| # | 来源 | 类型 | 年份 | 逐字 / 准逐字 | 有算力规模数字？ | 链接 |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| 1 | Hou, Han, Zhao, Wang. *Unveiling the Landscape of LLM Deployment in the Wild: An Empirical Study*（⛔ 无正式 venue，预印本） | 学术（实测） | 2025 | "identified **320,102** public-facing LLM services across **15** frameworks"；"the United States leads with **111,728** public LLM services, more than double the number of second-place **China (56,593)**"；"over **100,000** services are hosted by entities categorized as ``Others''"，作者归因为 "smaller cloud vendors, **university networks, hobbyist servers, or edge nodes**" | ⚠️ 有部署**数量**，无算力规模。硬件仅一例：ComfyUI `/system_stats` 泄漏 "**RTX 4090 with 24GB VRAM**" | [arXiv:2505.02502](https://arxiv.org/abs/2505.02502) |
| 2 | Pan, Chodnekar, Roy, Wang. *A Cost-Benefit Analysis of On-Premise Large Language Model Deployment*（⛔ 无正式 venue，预印本） | 学术（测算） | 2025 | 硬件价格表："NVIDIA **RTX 5090-32GB**…**$2,000**" / "NVIDIA **A100-80GB**…**$15,000**"。分档：**SME** = "moderate workloads (**<10M tokens/month**)"、消费级 GPU "**~$2,000**"、回本 "**0.3–3 months**"；**Medium** = "10–50M tokens/month"、"**$15k–$30k** for dual A100 setups"；**Large** = ">50M tokens/month"、"**$40k–$190k**"，且 "often already operate GPU clusters for other workloads"。最小可用："sub-30B deployments are feasible on a **single consumer-grade RTX 5090 ($2k)**" | **最完整的一份**：9 模型 × VRAM × 卡数 × 单价 × 吞吐 | [arXiv:2509.18101](https://arxiv.org/html/2509.18101v3) |
| 3 | Fares, Herbold（Univ. Passau）. *Utilizing LLMs for Industrial Process Automation: A Case Study on Modifying RAPID Programs* | 学术（**工业 SME 实地案例**） | 2025 | "We decided against using a proprietary, cloud-based model due to the **sensitive nature of data** involved."；"is possible **on-premise**, thereby ensuring the protection of sensitive company data"；工业软件是 "carefully guarded **business secrets**"。硬件主张：70B "can be used for inference on a **single A100**"，且 "**no complex hardware setup is required by an SME**"。实跑 **Llama 3.1-70b-instruct-q4_0**（4-bit）+ Ollama，`num_ctx 2048` | ⚠️ 只有「单张 A100」这一句**可行性主张**，**未报告合作企业实际有什么硬件** | [arXiv:2511.11125](https://arxiv.org/html/2511.11125v1) |
| 4 | Bhetwal 等. *Benchmarking Local LLMs for Natural-Language-to-SQL Querying in Biopharmaceutical Manufacturing: An Empirical Benchmark on Consumer-Grade Hardware*（⛔ 无正式 venue） | 学术（基准） | 2026 | 动机逐字：受管制制造业 "operate under regulatory frameworks such as FDA guidance, EU Good Manufacturing Practice (GMP), and the **EU AI Act, which can restrict the use of cloud-based artificial intelligence systems**"。实测四模型全在 **7B–8B** 档 | ⚠️ 有**模型档位**（7B–8B、消费级），具体 GPU 型号与显存未核到 | [arXiv:2606.01338](https://arxiv.org/abs/2606.01338) |
| 5 | 工业和信息化部办公厅《关于开展普惠算力赋能中小企业发展专项行动的通知》**工信厅通信〔2026〕14 号**（成文 2026-03-27，发布 2026-04-02） | **官方（部委规范性文件）** | 2026 | 逐字：「针对中小企业在**算力获取**、应用落地和能力提升中的**难点**」；「**显著降低中小企业获取、使用算力门槛**」；「打通"最后一公里"网络和算力**接入瓶颈**」；「按需建设部署边缘数据中心、**训推一体机**等边缘算力设施」；「鼓励设立**中小企业专属算力池**」；「推动整合**本地闲置、分散算力**」；「加快推广**低成本、轻量化、易部署**、绿色化的普惠算力解决方案」，聚焦「研发设计、生产制造、设备运维、供应链管理」 | ⛔ **无任何具体算力数字**（仅有 2028 年底覆盖 15 类行业中不少于 10 类的目标） | [miit.gov.cn 原文](https://www.miit.gov.cn/zwgk/zcwj/wjfb/tz/art/2026/art_58259bfb30924d6bb225b82b66d1008d.html) |
| 6 | 中国信通院云计算与大数据研究所等《**央国企智算创新实践报告（2025 年）**》 | 半官方（信通院专题报告） | 2025-09 | 逐字：「**部分央国企在算力应用上的投入不足，很多应用尚未上云**」；「对于一些**缺乏资金和技术积累**的企业，可与相关厂商合作开展平台共建」；「**中小型央国企算力需求挖掘期较长**，长期租赁成本可控」；工业领域「智算中心大多部署在**靠近工业现场**的地区，或通过云边协同构建"远端智算训练中心+边缘推理中心"的架构」；中国移动 X 节点「**在私有化场景下，以项目制方式建设**…累计上线**推理卡超过 2.1 万张**」 | ⚠️ 有宏观数字（788 EFLOPS FP16、1085 万标准机架、2.1 万张推理卡），但**全是运营商 / 大型央企侧**，**无单个工业单位的算力口径** | [PDF](https://www.caict.ac.cn/kxyj/qwfb/ztbg/202509/P020250930372667706524.pdf)（⚠️ AES 加密，需本地 `pdftotext`） |

### 5.3 ⚠️ 仅见检索摘要、⛔ 正文未核验的候选（引用前必须自查）

| 来源 | 摘要里说了什么 | ⛔ 未核验的部分 |
| :-- | :-- | :-- |
| Knoop, Holtmann. *Private LLM Inference on Consumer Blackwell GPUs: A Practical Guide for Cost-Effective Local Deployment in SMEs*，[arXiv:2601.09527](https://arxiv.org/abs/2601.09527)（2026-01） | SME 两难：第三方 API 有隐私风险，专业级本地硬件（A100/H100）"prohibitively expensive"；RTX 5090 约 **$2,000** vs H100 **$25,000+**；测 79 配置 × 4 开放权重模型（Qwen3-8B、Gemma3-12B/27B、GPT-OSS-20B）；[代码](https://github.com/hholtmann/llm-consumer-gpu-benchmark) | arXiv ID 与标题已由 abs URL 佐证；⛔ 但 $2,000 / $25,000 等数字**只从检索摘要读到，未打开原文**。**这是与本任务方向最贴的一篇，建议优先亲自核** |
| Khojah 等. *LLM Company Policies and Policy Implications in Software Organizations*，[arXiv:2510.06718](https://arxiv.org/abs/2510.06718) | 已核到：venue 是 **IEEE Software** Special Issue on AIware in the Foundation Models Era；"We examine how **11 companies** create these policies" | ⛔ **检索摘要声称该文讲「blocking AI tools through their firewall」「company size influences strictness」——打开 abs 页后这两条都不在其中。** 未核实前不要引这两句。且该文**完全不涉及算力 / GPU** |
| Deutsch 等. *Security and Privacy Perspectives on Using ChatGPT at the Workplace: An Interview Study*，[Springer 章节](https://link.springer.com/chapter/10.1007/978-3-031-72563-0_13) | grounded theory，**17 名受访者、15 家组织**；以三星因员工把内部源码贴进 ChatGPT 而封禁为动因 | ⛔ 未打开。**且它只讲隐私，不讲算力** |
| *Generative AI for Requirements Engineering: A Systematic Literature Review*，[arXiv:2409.06741](https://arxiv.org/pdf/2409.06741) | 仅 **13.3%** 的 RE + GenAI 研究处理数据隐私与模型安全 | ⛔ 未核。可作为「这一条缺研究」的**空白证据**，但不给算力 |

### 5.4 ⛔ 不合格命中（查到但不能用）

| 来源 | ⛔ 为什么不能用 |
| :-- | :-- |
| DreamFactory「28 On-Premise LLM Deployment Statistics」 | ⛔ **厂商内容营销页**（DreamFactory 卖自托管），无原始方法论。且检索到的多组占比互相矛盾（本地 51.85% vs 云端 49% vs 云端 41.74%），分母不同（spend / revenue / installations），**不可比** |
| Typedef、index.dev、useluminix、Zedly、TrueFoundry、NexaStack、Rexon、iternal、Allganize、Clarion 等 | 全是厂商 / 咨询博客，二级或三级转述 |
| 「IDC：中国智能体开发平台私有化部署市场 2025 年产品收入 17.5 亿元，公有云约 2.5 亿元」 | ⚠️ 数字**看起来正是想要的形状**（约 7:1 偏向私有化），但只见到 [futunn 新闻转述](https://news.futunn.com/en/post/74501371/idc-china-s-private-deployment-market-for-intelligent-agent-development)，**未见 IDC 原报告**；且对象是**智能体开发平台**而非 LLM 本身，也不是工业场景，也没有算力 |
| Deloitte AI Infrastructure Survey、Gartner *Predicts 2026: AI Sovereignty* | ⛔ 均**仅见二手转述**，原报告在付费墙后；且是**预期 / 预测**，不是现状实测 |
| CSDN / 知乎 / 腾讯云 / 阿里云开发者社区的「私有化部署算力选型指南」（如 4090Ti 48GB≈3 万元、DeepSeek-R1-70B 需 512G 显存≈8 张昇腾 910B、4 卡 L40S 替代 A100 省 40%） | ⛔ **技术博客，无来源、无方法、无署名机构**，学术上不可引。**数字看着最「解渴」恰恰因为它们没有出处约束** |
| 信通院《中国算力发展指数白皮书》《先进计算暨算力发展指数蓝皮书》《人工智能算力基础设施赋能研究报告》《云计算蓝皮书》《高质量大模型基础设施研究报告》 | 均为**真实存在的官方 PDF**，⛔ 但口径是**国家 / 区域级智算中心宏观建设**（EFLOPS、机架数、万卡集群），**与「某个工业单位手上只有几张卡」不是同一层次，硬引会是层级错配** |
| 东方财富 / 华西证券研报（含「私有化部署所需服务器开支测算」表） | 券商研报，二级来源，⛔ 且原始测算依据常来自厂商公众号 |
| 「防止过多采用"私有化部署+项目制"造成市场碎片化」（引称国务院研究室副主任陈昌盛，两会期间） | 措辞很有价值（**官方对私有化部署重复建设的反向意见**），⛔ 但**只在检索摘要中见到，未找到原始出处，不得引用** |
| SafeLLM（海上风电）、放射科本地模型基准、TEE 推理、LegalGuardian 等 | 场景非工业 / 非工程建模；或只讲隐私机制不讲算力现状 |

### 5.5 ⛔ 「查无可引来源」的如实记录

**以下是实际用过的检索词与入口，以及完全空手的方向。**

1. ⛔ **中国工业企业私有化 LLM 部署的规模统计** —— 检索词：`私有化部署 大模型 企业 算力 现状 调研 单卡 服务器 报告`、`工信部 中小企业 数字化转型 算力不足 调查 统计 比例 智能化改造 短板`、`caict.ac.cn 白皮书 人工智能大模型 落地 企业 算力`、`中国信通院 算力发展指数白皮书 中小企业 算力 短板`。⛔ **结论：不存在「X% 中国工业企业已私有化部署 LLM」或「工业企业平均可用 X 张卡」这类权威口径。** 官方只有**政策目标句**（降低门槛）与**宏观总量**（EFLOPS / 机架数），**中间那一层——单位级算力画像——是空的。**
2. ⛔ **军工 / 航天 / 涉密单位的本地 LLM 部署实证** —— 检索词：`军工 航天 涉密 单位 大模型 本地部署 内网 算力受限 论文`。⛔ **全部命中都是技术博客、厂商方案页或安全内参类行业文章，零篇可引学术文献。** 该方向的正式文献很可能在 CNKI / 万方（《信息安全研究》《保密科学技术》《指挥控制与仿真》《航天工业管理》），本轮**无法访问中文库**，未验证。
3. ⛔ **RE / SE 顶会里「因保密只能本地部署」的工业案例** —— 检索词：`requirements engineering industrial case study open-weight LLM "cannot leave" company premises REFSQ industry`、`empirical study developers company policy blocks LLM use proprietary code local model ICSE FSE survey practitioners`、`"industrial partner" LLM deployed locally single GPU confidentiality cannot use cloud API requirements engineering case study`。⛔ **RE 领域零命中**；SE 领域最近的是 §5.2 第 3 条（RAPID 案例，但那是机器人代码不是需求工程）。
4. ⛔ **「工业单位只能本地部署，而本地算力只有 X」这句完整表述** —— ⛔ **没有任何来源把两半话说全。** 隐私那一半（不能上公有云）到处都有；算力那一半（只有 X）**只出现在基准 / 测算论文自己的配置表里**，而那些论文测的是**自己的实验机**，不是任何真实工业单位的存量。**这个缺口本身就是可以在论文里点明的空白。**
5. ⛔ **IDC / Gartner 的「X% 企业自托管」** —— ⛔ 一个研究聚合页自己就标注了这个缺口：「no new 2025-2026 surveys from Gartner, Forrester, or IDC specifying on-premises splits」。**这条不存在。**

⚠️ **未尝试的入口（本轮能力外，如需应人工补）**：Google Scholar 直接检索、ACM DL、IEEE Xplore、DBLP、Semantic Scholar 的结构化检索（⛔ 本轮只有 web search，无学术库 API）；CNKI / 万方 / 维普中文库。

### 5.6 可用的引用组合（诚实版）

**最强的一条可引组合不是单篇，而是「官方政策 + 学术配置表」的夹逼**：

1. 用 **工信部 14 号文**（官方规范性文件，逐字承认「算力获取…难点」，并把「训推一体机」「整合本地闲置、分散算力」「低成本轻量化易部署」写进任务）证明**约束存在**；
2. 用 **arXiv:2509.18101** 的分档表（SME = 单张 RTX 5090 / ~$2k / <10M tokens/月）证明**约束的量级**。

⛔ **但两者是不同层次，不得把后者的数字说成中国工业企业的实测存量。**

⚠️ **arXiv:2505.02502 的 320,102 / 中国 56,593 这个数字很诱人，但要限定写清**：它测的是**公网可达**的自托管服务，⛔ 严格说它是「**暴露面**」而非「部署量」，**真正的企业内网部署恒不在其样本内**——这既是它的局限，也恰好说明「内网部署规模不可测」本身。

⛔ **方向 4（「只能本地、而本地只有 X」）目前无人写全，可作为论文的显式空白陈述**，⛔ 但陈述时只能说「据我们所知尚无实证研究报告工业单位的可用算力存量」，**不得反过来断言「工业单位普遍只有单卡」——那句话没有任何来源能支撑。**

## 6. 学术文献里的算力受限论证（含承重判定）

### 6.1 一句话结论

在 SE / MDE / RE 及邻近领域共核实 **10 篇**明确以「算力可得性 / 硬件受限」（⛔ 而非隐私）作为选用小模型理由的论文：**3 篇承重**（Weyssow TOSEM'25、Alizadeh MSR'25、Mallya REFSQ'26）、**6 篇半承重**、**1 篇不承重**。另有 1 篇（LibreLog / TOSEM'26）理由是隐私 + API 费用而非算力，仅作对照。

**承重判定档位**：**承重** = 核心贡献 claim 明确建立在「小模型也能做到」之上，且用算力可得性论证为什么必须小；**半承重** = 算力理由出现在 Motivation 但核心 claim 不依赖它；**不承重** = 只在 Setup 交代硬件。

### 6.2 主表

| # | 论文标题 | 年份 | Venue | 硬件表述（逐字） | 显存 | 所选模型规模 | 承重判定 | 链接 |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| 1 | Exploring Parameter-Efficient Fine-Tuning Techniques for Code Generation with Large Language Models | 2025 | **ACM TOSEM** 34(7):204 | "For all our experiments, we used a **single NVIDIA RTX A5000 24GB GPU**." | 单卡 24GB | 220M–34B（含 QLoRA 8/4-bit） | **承重** | [10.1145/3714461](https://doi.org/10.1145/3714461) · [arXiv:2308.10462](https://arxiv.org/abs/2308.10462) |
| 2 | Language Models in Software Development Tasks: An Experimental Analysis of Energy and Accuracy | 2025 | **MSR 2025**, pp.725–736 | "GPU: NVIDIA GeForce **RTX3070** — Mem: **8GB**"（laptop）＋"GPU: NVIDIA **A100 PCIe** — Mem: **80GB**" | 8GB / 80GB | ≤20B，4/5/8-bit GGUF | **承重** | [10.1109/MSR66628.2025.00109](https://doi.org/10.1109/MSR66628.2025.00109) · [arXiv:2412.00329](https://arxiv.org/abs/2412.00329) |
| 3 | From Online User Feedback to Requirements: Evaluating LLMs for Classification and Specification Tasks | 2026 | **REFSQ 2026**（LNCS）, pp.161–177 | "Experiments ran on a workstation with an **NVIDIA RTX 4050 GPU (6 GB VRAM)** and 16 GB RAM." | 单卡 **6GB** | Llama2-7B / Llama3-8B / Mistral-7B / Gemma2-9B / Phi-3 Mini | **承重** | [10.1007/978-3-032-21423-2_11](https://doi.org/10.1007/978-3-032-21423-2_11) · [arXiv:2510.23055](https://arxiv.org/abs/2510.23055) |
| 4 | Precision or Peril: A PoC of Python Code Quality from Quantized Large Language Models | 2026 | AI-SQE '26（ACM SIGSOFT workshop）, pp.29–37 | "We used a single machine … equipped with an **Nvidia RTX 3090 GPU (24BG VRAM)**"（⚠️ 原文 typo） | 单卡 24GB | 4×7B，AWQ 4/8-bit / 无量化 | 半承重 | [10.1145/3786175.3788343](https://doi.org/10.1145/3786175.3788343) · [arXiv:2411.10656](https://arxiv.org/abs/2411.10656) |
| 5 | Assessing Small Language Models for Code Generation: An Empirical Study with Benchmarks | 2026 | **J. Syst. Softw.** 236:112815 | "a workstation-grade **NVIDIA L4 GPU with 24 GB VRAM** … a consumer-grade **NVIDIA RTX 3090 GPU**, also featuring **24 GB** of VRAM" | 各 24GB（单卡执行） | 20 个 SLM，0.4B–10B，BF16 无量化 | 半承重（偏承重） | [10.1016/j.jss.2026.112815](https://doi.org/10.1016/j.jss.2026.112815) · [arXiv:2507.03160](https://arxiv.org/abs/2507.03160) |
| 6 | Insights into resource utilization of code small language models serving with runtime engines and execution providers | 2025 | **J. Syst. Softw.** 230:112574 | "All these experiments have been conducted with an **NVIDIA GeForce RTX 4090 GPU with 24 GB memory**" | 单卡 24GB | 12 个 code SLM，定义为 <5B | 半承重 | [10.1016/j.jss.2025.112574](https://doi.org/10.1016/j.jss.2025.112574) · [arXiv:2412.15441](https://arxiv.org/abs/2412.15441) |
| 7 | Instruction-Tuning Open-Weight Language Models for BPMN Model Generation（InstruBPM） | 2025 | ⏳ preprint（venue 待核验） | "Training runs on **2 × L40S (48 GB)** GPUs and completes in about 150 minutes" | 2×48GB | Qwen3-4B + LoRA(BF16) + PTQ | 半承重 | [arXiv:2512.12063](https://arxiv.org/abs/2512.12063) |
| 8 | From Text to DSL: Evaluating Grammar-Based Model Generation Using Open LLMs | 2026 | ⏳ preprint（venue 待核验） | ⛔ **未给出任何 GPU 型号 / 显存**；仅 "inference was performed locally using quantized versions (e.g., GGUF)" | ⛔ **未给出** | 39 个开源 LLM，0.5B–32B，GGUF | 半承重 | [arXiv:2605.15865](https://arxiv.org/abs/2605.15865) |
| 9 | An empirical study of LoRA-based fine-tuning of LLMs for automated test case generation | 2026 | ⏳ preprint（venue 待核验） | "a virtual machine equipped with an **NVIDIA H100 GPU**, 40 CPU cores, 320 GB of system memory"（Azure ML） | 单卡 H100（⛔ **非受限**） | 3 个 ~8B 开源模型 + GPT-4.1 系列 | 半承重 | [arXiv:2604.06946](https://arxiv.org/abs/2604.06946) |
| 10 | On the Effectiveness of Large Language Models in Domain-Specific Code Generation | 2025 | **ACM TOSEM** 34(3):78 | "We train all models in a server with **8 Nvidia A100 (40GB) GPU cards**."（多卡，⛔ 不受限） | 8×40GB | CodeLlama-7B / PolyCoder-2.7B / StarCoder-15.5B | ⛔ **不承重** | [10.1145/3697012](https://doi.org/10.1145/3697012) · [arXiv:2312.01639](https://arxiv.org/abs/2312.01639) |

⚠️ **引用取自 arXiv 全文**（TOSEM / JSS / Springer 正式版有付费墙），**行文与正式版可能有细微差异**。

### 6.3 承重与半承重的逐字引用

#### #1 Weyssow et al., TOSEM 2025 —— 承重（本批最强）

算力约束是整篇论文的组织轴，**独立成节 §3 "APPLYING LLMS WITH LIMITED RESOURCES"**：

> "For instance, a software engineer with access to only a **single consumer GPU (e.g., 24GB of VRAM)** may find full fine-tuning impractical due to the significant memory demands."（§3）

方法论开篇即把它写成设计前提（**§4 Methodology** 首段）：

> "We conduct all the experiments **under a resource-constrained scenario**. Specifically, all the procedures, i.e., fine-tuning and inference, of the models are performed with access to a **single 24GB GPU**. The main objective of our study is to demonstrate whether the fine-tuning of LLMs through PEFT is feasible and desirable over previous approaches and smaller models **in this context**."

模型选择被它裁定（**§4.4**）：

> "Note that we **selected models that fit a single 24GB GPU** for fine-tuning and inference without causing memory overflow."

**核心 claim 直接挂在 24GB 上**（Abstract 要点 + §5 findings）：

> "QLoRA enables the fine-tuning of LLMs **up to 34B parameters for less than 24GB of GPU memory**."
>
> "…under the **same 24GB GPU memory limitation**, the best LLM surpasses the best small model by 39.8%, 41.7%, and …"

甚至 RQ1 的实验参数也被它裁定："We test each model with up to 16 ICL examples, **due to our limited computation resources**."（§4.1）

**判定理由**：不是顺带一提——**RQ 设计、模型池、ICL 样本数、结论表述全部以「单卡 24GB」为分母**，⛔ 去掉这个前提论文的贡献 claim 就不成立。

#### #2 Alizadeh et al., MSR 2025 —— 承重

模型规模上限与量化位宽都由自有硬件裁定（**§IV.A Model Selection**）：

> "**Due to hardware limitations**, we also narrowed down our selections to models with **no more than 20 billion parameters**. The **memory constraints of our desktop GPU** only allow for quantization levels **up to 5 bits**."

Abstract 明确把「买不起 flagship GPU」立为研究前提：

> "Given that deploying LLMs locally requires powerful infrastructure **which might not be affordable for everyone**, we consider both full-precision and quantized models."

Introduction 的两档硬件对照就是论文骨架：

> "One approach for deploying LLMs locally is to utilize a flagship GPU … However, since these GPUs are **not affordable for everyone**, an alternative solution could be using compressed and quantized models that can run on **smaller GPUs or even large CPUs**."

⚠️ **需要注意**：locality 的**第一动机是隐私**（"Using third-party APIs raises data privacy and security concerns for client companies, which motivates the use of locally-deployed language models"），算力是随后决定**模型多大**的二阶约束。但「更大能耗预算的大模型并不总是更准」这个核心 claim 确实建立在 commodity GPU 这一档上，故判承重。

#### #3 Mallya et al., REFSQ 2026 —— 承重

**§2 背景**把「少算力 → 能本地跑」立为选择 lightweight 的理由，且⛔ **未提隐私**：

> "Commercial models such as GPT-4, Claude, and Gemini … are **resource-intensive**, provider-dependent, and difficult to customize. These characteristics limit their suitability for controlled research and **small-scale SE projects**."
>
> "**Lightweight open-source LLMs provide a practical alternative.** They contain fewer parameters and **require less computational power**. As a result, they can **run efficiently on local machines**."

**§4 实验设置**给出本批最低配硬件：

> "Experiments ran on a workstation with an **NVIDIA RTX 4050 GPU (6 GB VRAM)** and 16 GB RAM."

核心 claim 就是「lightweight 能做到多少」：结论是可支撑 feedback filtering / classification / 初稿生成但不能替代分析师；**§7 Threats（External Validity）** 也把它作为边界写明："the study focused on lightweight LLMs; larger models may yield different results."

⚠️ **限定**：6GB 这个数字只出现在 Setup，算力论证在 §1/§2；**两处结合才构成承重。**

#### #4 Melin et al., AI-SQE '26 —— 半承重

**§3.2 Chosen LLMs** 是本批里把「单卡」写得最露骨的一处，且它**决定了整个被测模型池**：

> "We selected four open source LLMs to use for our testing. **Due to limited memory constraints, our LLMs had to be able to fit on a single GPU** with and without quantization. … These constraints limited us to using open source LLMs with **less than 10 billion parameters**."

逐模型理由也重复挂在显存上："We used the 7B version **due to memory constraints**."（WizardCoder）· "we used the 7B version as the **largest GPU-compatible model**."（StarCoder 2）· "Selected for **GPU compatibility**."（LlamaCode 7B）

⛔ **为什么只判半承重**：它的结论方向是**反**的——"These **poor results** indicate that smaller, open source LLMs perform **noticeably worse** than their much larger counterparts."（§4）。⛔ 即核心 claim 不是「小模型也能做到」，不满足承重的第一半；但算力约束确实定义了被测总体，因而不止是 Setup 交代。

#### #5 Hasan et al., JSS 2026 —— 半承重（偏承重）

> "…making them viable for deployment in **resource-constrained environments**."（Abstract）"…we observe that for 10% performance improvements, models can require nearly a **4x increase in VRAM**"（Abstract）"Rationale: This question examines how small language models balance performance with resource usage … helps determine which models are best suited for real-world scenarios with **hardware or time constraints**."（§2 RQ2）"The first setup featured … a workstation-grade **NVIDIA L4 GPU with 24 GB VRAM**. The second setup included … a consumer-grade **NVIDIA RTX 3090 GPU**, also featuring **24 GB** of VRAM."（§2.4.3）

⛔ **为什么不判满承重**：0.4B–10B 的上限来自「SLM」的**定义与研究对象设定**，⛔ **不是**由作者自有硬件天花板推出的；两台机器分配模型的理由写的是 "to balance the computational load and accelerate the evaluation process"。算力承载的是「VRAM–准确率权衡」这一条结论，而非「为什么必须小」。

#### #6 Durán et al., JSS 2025 —— 半承重

算力理由在 **§2.2 背景**，且明确写成「SLM 是解法」：

> "These **smaller companies** often operate with **constrained CPU or GPU resources**, necessitating innovative approaches to make use of language models effectively. In this context, **SLMs emerge as a critical solution**…"

硬件（**§4.6**）："All these experiments have been conducted with an **NVIDIA GeForce RTX 4090 GPU with 24 GB memory** with CUDA Version 12.4, and an AMD Ryzen 9 7950X 16-Core Processor CPU"。

⛔ **判半承重**：核心 claim 是 runtime engine × execution provider 组合对能耗 / 时延 / 资源占用的影响（TORCH+CUDA 省 37.99%–89.16% 能耗），⛔ 不是「小模型也够用」。算力受限出现在 Motivation，且与「隐私」「闭源 API 成本」并列。

#### #7 Çelikmasat et al., InstruBPM（preprint）—— 半承重

> "We begin by selecting Qwen3-4B for its performance-size balance, permissive licensing, and **on-prem deployability (S1)**."（§5.2）

**上下文长度上限**由硬件预算裁定（§5.1，这一处最实在）：

> "increasing the cap to 4096 tokens would roughly **quadruple the attention memory** per layer, which would force smaller batches/throughput **under our hardware budget**, with limited benefit for this dataset's length distribution"

训练硬件："Training runs on **2 × L40S (48 GB)** GPUs and completes in about 150 minutes"（§5.2）。⚠️ **注意是双卡 48GB，不是消费级单卡。**

⛔ **判半承重**：核心 claim（4B 微调模型在结构保真上超过闭源系统）确属「小也够用」，⛔ 但论文把动机写成隐私与成本**并列**："For teams operating under **privacy or cost constraints**, compact instruction-tuned models can be deployed on-premise with near-full precision quality when using medium-bit PTQ."（§7）

#### #8 Baber et al., From Text to DSL（preprint）—— 半承重，⛔ **硬件表述缺失**

Abstract 的算力 / 成本论证（**MDE 领域里这个 framing 最直白的一处**）：

> "While most existing approaches rely on large proprietary models, their **high cost and limited deployability** hinder broader adoption." "These findings demonstrate the feasibility of using **smaller, open-source LLMs** for grammar-conformant DSL generation in MDE workflows, offering a **cost-effective and deployable alternative** to closed LLMs."

**§3.2 LLM Selection**："All models were used without fine-tuning. Where possible, **inference was performed locally using quantized versions (e.g., GGUF)**, otherwise via public APIs."

⚠️ **全文未出现任何 GPU 型号、显存数字或单卡 / 多卡说明**（核验员对 `GPU|VRAM|A100|4090|3090|V100|H100|memory` 做过全文 grep，⛔ 只命中参考文献里的 Phi-3 标题）。因此它的「算力理由」停留在成本 / 可部署性的抽象层，**无硬件锚点**。另 §5 讨论把三个理由并列："in contexts where **privacy, cost, or deployment constraints** limit the use of commercial LLMs."

#### #9 Moradi, LoRA test-gen（preprint）—— 半承重，⛔ **作者侧算力并不受限**

> "…full fine-tuning is computationally expensive, memory-intensive, and difficult to scale. It requires substantial hardware resources and can be **impractical for many organizations**" "…making it particularly suitable for fine-tuning billion-parameter models on domain-specific tasks with **limited hardware resources**."（§4.3）"This result suggests that **organizations** can achieve competitive performance using smaller, more cost-efficient, and **locally deployable** models…"（Discussion）

⛔ 而作者自己的硬件恰恰是**高端**的：

> "…using a virtual machine equipped with an **NVIDIA H100 GPU**, 40 CPU cores, 320 GB of system memory … The use of a **high-performance GPU** enabled efficient fine-tuning of multi-billion-parameter models under mixed-precision…"

⛔ **判半承重**：算力论证的主体是**假想的部署方组织**，⛔ 不是作者；且与 data privacy 并列陈述。**这是一个典型的「算力理由用作 motivation 修辞、但作者自身不受该约束」的样本。**

#### #10 Gu et al., TOSEM 2025 —— ⛔ 不承重（反例样本，供对照）

全文只有一句涉及单卡，位于 **§3.2 模型介绍**："We use the 7B model, which **can be served on a single GPU** while showing efficient and accurate performance on code completion."

而 **§4.4 Experimental Setup** 表明作者算力充裕："We train all models in a server with **8 Nvidia A100 (40GB) GPU cards**."

⛔ 无任何 claim 挂在单卡上。**这正是判据里「只在 Setup 里交代硬件」那一档的干净例子。**

### 6.4 对照观察：隐私 vs 算力

**结论方向：是，隐私远多于算力；⛔ 但「算力」很少单独出现，通常与隐私并列。**

⚠️ **粗略手感：隐私（含 data confidentiality / 不外发代码）: 纯算力可得性 ≈ 3:1 到 5:1。** ⛔ **这不是严谨统计**——没有做系统检索、没定义抽样框、没有分母。证据基础只有以下三条，请按**印证性证据**读：

1. **检索侧的不对称（最有信息量的一条）**：用算力向关键词（`single GPU` / `consumer-grade GPU` / `commodity hardware` / `due to computational constraints` + SE venue）做了 8 轮检索，⛔ **大量结果是消费级显卡选购指南和系统 / 推理优化论文，而非 SE/MDE/RE 论文**；⛔ 检索引擎多次直接回报「未找到匹配的 SE 论文」。而只要把关键词换成隐私向（`privacy` / `on-premise` / `data confidentiality`），SE/RE 侧命中密度明显更高。这说明**算力 framing 在 SE 文献里更稀疏、也更难被检索到**——但也可能只是搜索引擎的索引偏差，不能排除。
2. ⚠️ **在实际读全文的 10 篇里的共现分布**：明确提隐私的 6 篇（#2 #6 #7 #8 #9 及对照的 LibreLog）；**不提隐私、纯算力 framing 的 4 篇**（#1 #3 #4 #5）。⛔ **这个 4/10 的比例严重高估了算力 framing 的真实占比，因为检索本身就是按算力关键词构造的（选择偏差）。** 它唯一能说明的是：**纯算力 framing 确实存在且可找到，不是零。**
3. **对照样本（隐私 + API 成本，⛔ 非算力）**：Ma, Kim & Chen，*Unsupervised, Accurate, and Efficient Log Parsing Using Smaller Open-Source Large Language Models*，**ACM TOSEM, 2026**，[10.1145/3796239](https://doi.org/10.1145/3796239)（arXiv 前身 [2408.01585](https://arxiv.org/abs/2408.01585)，原名 LibreLog / OpenLogParser）。标题里就写 "Smaller Open-Source LLMs"，⛔ 但据检索摘要，其选用 Llama3-8B 的理由是**避免把敏感日志发给商业模型 + 省 API 费用**，硬件用的是 A100，**不是算力受限**。**该文全文未读，上述动机与硬件描述来自检索摘要，待核验。**

### 6.5 一条对本仓库直接有用的形态判据

**当算力理由真正承重时，它有一个可识别的形态特征**：**显存数字会反复出现在 Methodology / RQ 设计 / 模型池筛选 / 结论句里**——#1 的 "24GB" 出现在摘要要点、§3、§4 开篇、§4.4、§4.6、§5 findings、以及图 1 与图 5 的坐标轴上；⛔ 而**若显存只在 Experimental Setup 出现一次**（#10），基本可判不承重。

⚠️ **#3 是介于两者之间的形态**：算力论证在 §1/§2 用**定性措辞**（"require less computational power"），⛔ 具体显存数字只在 Setup 出现一次——**判断承重时必须把两处合起来读。**

## 7. 待核验项与访问受限记录

### 7.1 访问受限（本轮实际遇到）

| 目标 | 现象 | 处置 |
| :-- | :-- | :-- |
| `federalregister.gov`（规则全文） | 直连返回 **302 → `https://unblock.federalregister.gov/`** | 改用 **govinfo.gov** 官方 HTML 全文（同一出版物，`www.gpo.gov` 出版），已逐字核对 |
| `ecfr.gov`（3A090 现行文本） | 同上 302 | 改用 2022 / 2023 / 2024 / 2026 四份规则的 Items 段原文；⚠️ **故本文给出的是「各规则当时颁布的文本」，不是「eCFR 现行合并文本」** |
| `support.huawei.com/enterprise/zh/doc/EDOC1100317202/f3dba488`（Atlas 800T A2 用户指南「技术规格」，含表 3-1 AI 处理器技术规格） | **403 Access Denied**（Akamai edge；WebFetch 与带 UA 的 curl 均被拦，`errors.edgesuite.net`） | ⛔ **这是最可能给出 910B 官方单卡 HBM 的一手文档，未能取得。** 已改用官方**软件侧**文档（Ascend ModelZoo / vLLM-Ascend 教程）获得 `64GB` 官方措辞。⏳ 建议人工用浏览器登录华为支持网核验 |
| `hiascend.com/hardware/accelerator-card?tag=...` | ⛔ **SPA，tag 参数对抓取无效**，只渲染默认的 Atlas 350。Atlas 300T A2 **连导航项都没有** | 已取得 Atlas 350 官方规格；⏳ 300T A2 待核验 |
| `hiascend.com/hardware/cluster` | 页面标题含 Atlas 900 A3 SuperPoD / A2 PoD，⛔ 但**只渲染出 Atlas 950 SuperPoD 的规格表** | 已改用 `e.huawei.com` 官方页取得 Atlas 900 A3 SuperPoD 规格 |
| `hiascend.com/software/mindie/modellist` | 查询工具外壳，返回「本页面呈现的release版本中暂时未查找到该模型的支持信息」，⛔ **无任何模型列表数据** | 已改用 GitHub 上的官方 `supported_models.md` |
| `docs.vllm.ai/projects/ascend/...` | **HTTP 429 Too Many Requests** | 已改用 GitHub raw 逐字获取（**比渲染站更可靠**，渲染站有版本漂移） |
| `raw.githubusercontent.com/.../tutorials/multi_node.md` | **HTTP 404** —— 该文件在 main 分支已不存在，教程已重构进 `tutorials/models/*.md` | ⚠️ **流传的 multi_node 教程链接指向历史版本，勿引** |
| `cambricon.com/...catid=340`（MLU290-M5） | **HTTP 500**（同站 catid=406 的 MLU370-X8 正常） | ⏳ 待核验 |
| `hygon.cn/product/accelerator` | ⛔ 返回的正文只有「海光--用"芯"计算未来」与一段 **MIT LICENSE**，无任何产品规格 | ⏳ **海光 DCU 官方规格全线待核验** |
| `birentech.com/Product/index.html` | **HTTP 404**（`/product/hardware/106m/` 可访问，⛔ 但**不含任何显存数字**） | 已确认是「**官方不公布**」而非「取不到」 |
| `sec.gov` 经 WebFetch | **403 Forbidden** | 改用带 User-Agent 的 `curl` 直取 EDGAR 原始文档，成功 |
| `arxiv.org/pdf/*` 经 WebFetch | 返回未解压 PDF 二进制（FlateDecode），无法提取正文 | 改为 `curl` 下载 + 本地 `pdftotext -layout`，全部成功 |
| `link.springer.com/chapter/10.1007/978-3-032-21423-2_11` | 303 重定向到 `idp.springer.com` 鉴权页 | 改用 Crossref API 核实书目（REFSQ 2026, LNCS, pp.161–177） |
| ACM DL（TOSEM 34(7):204 / 34(3):78）· ScienceDirect（JSS） | 付费墙 | 引用取自 arXiv 全文；⚠️ 与正式版行文可能有细微差异 |
| 信通院《央国企智算创新实践报告（2025）》PDF | ⚠️ **AES 加密 PDF**，WebFetch 只拿到二进制 | 本地 `pdftotext -enc UTF-8` 成功抽出正文（79,916 字节），§5.2 第 6 条引文来自该抽取结果 |
| Deloitte AI Infrastructure Survey · Gartner *Predicts 2026* · IDC 中国智能体开发平台份额 | 付费墙，仅见二手转述 | ⛔ 不采用 |
| CNKI / 万方 / 维普 | ⛔ 无访问能力 | ⏳ §5.5 第 2 项因此未验证 |

⛔ **按仓库规范 §2 第 3 条**：以上访问异常**只记录为「入口已定位 / 内容待人工核验 / 访问异常类型」**，⛔ **不得据此断言事实不存在。**

### 7.2 待核验项清单

| # | 待核验内容 | 为什么重要 | 当前级别 |
| :-- | :-- | :-- | :-- |
| 1 | **H20 的 96 GB 显存**：⛔ 未找到 NVIDIA 官方数据表 | §3.4 反向论据「8×H20 = 768 GB > 640 GB」**依赖它** | S（聚合站 / 经销商 / 百科） |
| 2 | **Ascend 910B 单卡 HBM 容量 = 64GB** —— **已由官方软件文档确认**（`Atlas 800I A2 (8*64G)` / `64GB × 8`）；⛔ **但硬件规格页仍拿不到，且 HBM 型号（HBM2e / HBM3）与带宽官方未公布** | §3.2 表多行依赖容量（已解决）；⛔ 带宽未知会影响 decode 吞吐判断 | **M**（容量）· ⏳ **待核验**（HBM 型号与带宽） |
| 2b | ⛔ **910B 的 B1/B2/B3 = 64GB、B4 = 32GB 分档表** | 决定「一台 8 卡机到底是 512 GB 还是 256 GB」 | ⏳ 待核验（⛔ 无华为官方分档表；B4=32GB 仅有实机 `npu-smi` 截图） |
| 2c | ⛔ **「910C」型号名在官方硬件规格中不存在** | ⛔ **论文里不得写「910C 有 xx GB」**；须改写为 Atlas A3 节点 / Atlas 900 A3 SuperPoD 的官方口径 | **M**（该缺失本身已确认） |
| 2d | ⛔ 海光 DCU 全线、壁仞在产品线、摩尔线程 S5000、寒武纪 590/690 的**官方显存规格** | 若要在论文里给国产卡显存，**目前只有华为（间接）、寒武纪 MLU370-X8、摩尔线程 S4000、天数智芯智铠100 四条有官方出处** | ⛔ **官方未公布 / 查无来源** |
| 3 | **§1.10 中方国家资金数据中心禁令的官方政策文本** | 这是「型号单位只能用国产」的**唯一支柱** | S（Reuters 双匿名消息源；CAC / NDRC 未置评） |
| 4 | 二级来源称 **2026-03 中旬中方已批准 H200 售予部分中国客户** | ⛔ **与 NVIDIA 2026-04-26 季报「收入为零、能否入境未知」张力明显**；本文未采用 | S ⚠️ 存疑 |
| 5 | 2025-08 报道的 **15% 对华芯片销售分成** 的官方文本 | 影响「合法通道的实际成本」 | S；⛔ 官方文本未找到 |
| 6 | **§1.8 GP 10 指南**（点名昇腾 910B/C/D）的官方 PDF 直链与逐字文本 | 影响「在昇腾上做实验并发表」的合规摩擦判断 | S ⚠️ |
| 7 | §1.3（89 FR 23876）、§1.5（AI Diffusion）、§1.6（尽职调查）三份规则⛔ **未回原文逐字核对** | 时间线完整性 | S ⚠️ |
| 8 | **AI Diffusion 是否已在 Federal Register 正式撤销** | ⚠️ 迄今公开信息显示**仅为「不予执行」**；且据报 GAO **2026-05-12** 认定该新闻稿式不执行构成 CRA 下的 "rule" | S ⚠️ |
| 9 | 2026-01-14 总统公告 **25% 从价税** 的原文 | 但 NVIDIA 10-Q 对该关税适用于 H200 通道有逐字确认（**M**） | S ⚠️（公告原文）· M（适用事实） |
| 10 | **RTX 6000D 被中方禁 / 劝退** 的官方依据 | §3.2 表第 5 行的可得性判定 | S ⚠️ |
| 11 | 「**因为**昇腾不原生支持 FP8**所以**转 INT8」这条**因果**的逐字出处（2508.02520 全文） | §4.6；**「用了 INT8」与「官方支持列表不含 FP8」两条已是 M**，⛔ 缺的只是因果链 | S ⚠️（搜索摘要） |
| 12 | **CloudMatrix384 用的是 910C 而非泛化的「910」** | ⚠️ v3 摘要已把型号泛化；且官方硬件规格中无「910C」 | S ⚠️ |
| 12b | ⚠️ 「DeepSeek-R1 **BF16** 至少 4 台 800I A2」这条流传说法 | ⛔ **未在官方 README 中核到**；官方只给了 W8A8 的 2 台要求 | S ⚠️ |
| 12c | vLLM-MindSpore 的 671B `dp4_tp4_ep4` 教程**正文** | 第三条独立官方路径 | M（标题 + 配方名）· ⛔ S（正文） |
| 12d | ⛔ 寒武纪 / 壁仞 / 摩尔线程 / 海光对 **671B 级 MoE** 与 **Qwen3-32B** 的官方适配 | 决定「除华为外还有没有第二条国产路径」 | ⛔ **查无来源**（仅厂商公关稿） |
| 13 | 中国大陆 3A090 级卡的**灰市**实际可得性与价格 | 影响「现实包络」的真实下界 | ⛔ 未查（且对国家资金单位不适用） |
| 14 | 2026-06 至 2026-08 有无更新规则 | 时效 | ⚠️ 本轮检索**未发现** 2026-07 / 08 的新规则；据报 BIS 计划在本财年内正式撤销并替换 AI Diffusion（**S**） |
| 15 | §5.3 四条**仅见摘要**的候选，尤其 **arXiv:2601.09527** | 后者是与本任务方向最贴的一篇 | S ⚠️ |
| 16 | §6.2 中 #7 / #8 / #9 三篇 preprint 的**正式 venue** | 引用规范 | ⏳ 待核验 |
| 17 | §6.4 第 3 条 LibreLog 的**正文动机与硬件** | 对照观察的唯一反例样本 | S ⚠️（仅摘要） |

### 7.3 ⛔ 本文口径声明

**§1 的全部生效日与阈值数字均已回官方原文逐字核对**（govinfo Federal Register 全文 + BIS 官方 PDF + SEC EDGAR 原始申报），⛔ 例外为已在表中标 **S ⚠️** 的 §1.3 / §1.5 / §1.6 / §1.8 动作 3 / §1.9 / §1.10 / §1.12。

**§2.2 与 §4 的昇腾侧事实**已回官方一手来源逐字核对（华为 `e.huawei.com` / `hiascend.com` 官方规格页、Ascend gitee ModelZoo、vLLM-Ascend main 分支官方文档、华为团队 arXiv 论文），⛔ 例外为表中标 **S ⚠️** 或 **⏳ 待核验** 的条目。**§2.2.2 中「官方未公布」的厂商（海光全线、壁仞在产品线、摩尔线程 S5000、寒武纪 590/690）不得给出显存数字。**

⛔ **§3.2 表中所有「4-bit 可容总参上限」列均为 I 级计算**，⛔ 且 §3.2 末尾的实测校准说明它在贴边格子上**偏乐观**——**不得当作选型承诺。**

⛔ **本文相对初稿的两处实质更正**（按 §3.6 就地修改原则，⛔ 错误表述已删除、不保留）：

1. ⛔ **「671B 需要 CloudMatrix384（384 NPU）」→ 错。** 官方最低门槛是 **2 台 Atlas 800I A2（1024 GB）跑 W8A8**，MindIE 与 vLLM-Ascend 口径一致。⛔ 该错误会把「国产生态部署 671B」的门槛高估约 24 倍（384 卡 vs 16 卡）。
2. ⛔ **「910B 单卡显存待核验」→ 已核实为 64GB**（官方软件文档措辞）。连带使 §3.2 第 4 / 8 / 9 行由 ⏳ 升为 **M**。

⛔ **§5 与 §6 的所有论文引用均取自 arXiv 全文或官方 PDF，例外为 §5.3 与 §6.4 第 3 条明确标注「仅见摘要 / 未核验正文」的条目——那些条目引用前必须自查原文。**
