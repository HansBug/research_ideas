# 卡片 · **Coupling LLMs and Model-Driven Engineering to Support Synthetic Generation of BPMN Artifacts**（MODELS-C 2025 / MDE Intelligence）

---

## ⛔⛔ 全文不可得声明（⭐ 读这张卡前必须先读这一节）

⛔⛔ **本篇全文未能取得。⭐ 本卡除 A 节外，⛔ 全部内容仅据摘要 + 已核验元数据 + 会议 TOC。**

⭐ **已实际试过的入口，逐条列出**：

| # | 入口 | 结果 |
| :-: | :-- | :-- |
| 1 | ⭐ arXiv API 按标题精确检索 | ⛔ **0 命中** |
| 2 | ⭐ arXiv API 按作者 `au:Muttillo` 检索 | ⛔ **0 命中** |
| 3 | ⭐ ar5iv | ⛔ **不适用**（⛔ 无 arXiv id） |
| 4 | ⭐ **Unpaywall** `10.1109/MODELS-C68889.2025.00079` | ⛔ **`is_oa: false` · `oa_status: closed` · `oa_locations: []` · `has_repository_copy: false`** |
| 5 | ⭐ **OpenAlex** | ⛔ **`is_oa: False` · `any_repository_has_fulltext: False`**，⭐ 唯一 location 就是 DOI 本身 |
| 6 | ⭐ Semantic Scholar `openAccessPdf` | ⛔ **`url: ""`**（⭐ 空字符串） |
| 7 | ⭐ IEEE Xplore 文档页 `ieeexplore.ieee.org/document/11273209/` | ⛔ **HTTP 202 + JS 壳**，⭐ 抓到的正文只有 IEEE 页脚导航 |
| 8 | ⭐ Crossref 给出的 `xplorestaging` PDF 直链 | ⛔ **HTTP 200 但 `content-type: text/html`**，⭐ 内容是 IEEE 账户/购买页 |
| 9 | ⭐ **JKU 机构库**（⭐ Berardinelli 所在，`epub.jku.at`） | ⛔ **WAF 拦截**：「Verifying your browser … Please enable JavaScript and cookies」 |
| 10 | ⭐ **ResearchGate** 出版物页 | ⛔ **HTTP 403** |
| 11 | ⭐ **MDE Intelligence 2025 workshop 官网** | ⛔ **HTTP 404** —— ⚠️ 站点已滚到 2026 第 8 届，⭐ 2025 年度页不再可达 |
| 12 | ⭐ 网络检索 hosted PDF（⭐ 含 `filetype:pdf` 式查询） | ⛔ **无任何开放副本** |
| 13 | ⭐ 前置工作 IST 2025（⭐ hybrid OA，见下）ScienceDirect 全文 | ⛔ **HTTP 403** |

⭐ **另外核过一条旁路，⛔ 结论是它帮不上**：⭐ 本文摘要自陈「Being built on our previous work」，⭐ 那篇前置工作 [Leveraging synthetic trace generation of modeling operations for intelligent modeling assistants using large language models](https://doi.org/10.1016/j.infsof.2025.107806)（IST 186:107806, 2025）⭐ **确实是 hybrid OA / CC-BY**（⭐ Unpaywall 实测 `is_oa: True, oa_status: hybrid`），⛔ 但 ScienceDirect 对本环境返 403，⭐ 且 Semantic Scholar 把它的摘要 elide 掉了。⛔ **即便取到，它也是另一篇论文**，⛔ 不能用来填本卡的 B/C 格。

⭐⭐ **因此本卡的纪律**：

- ⭐ **A 节** = ⭐ 实核元数据，级别 **M**
- ⭐ **B / C / D / E 节** = ⛔ **每格都标「仅据摘要」**；⛔ 摘要没提的一律写「**原文未提供**」
- ⛔ **不得为了填满卡片而从前置工作、同组其它论文或领域常识倒推** —— ⭐ 凡涉及推测一律标 **I** 并写成「看起来 / 推测 / 未明说」

---

## A. 元信息

| 字段 | 值 | 级别 |
| :-- | :-- | :-: |
| `id` | `models-c2025-bpmn-mde-coupling` | — |
| `title` | Coupling LLMs and Model-Driven Engineering to Support Synthetic Generation of BPMN Artifacts | M |
| `year` | ⭐ **2025**（⭐ Crossref `published: 2025-10-05`） | M |
| `venue` | ⭐ **2025 ACM/IEEE 28th International Conference on Model Driven Engineering Languages and Systems Companion (MODELS-C)** · ⭐ **pp. 556–565** · ⭐ Grand Rapids, MI, USA, 2025-10-05 → 10-10 | M |
| ⭐ **具体 track** | ⭐⭐ **7th Workshop on Artificial Intelligence and Model-Driven Engineering (MDE Intelligence 2025)** —— ⭐ 本轮从 [MODELS-C 2025 官方 TOC PDF](https://www.proceedings.com/content/083/083457webtoc.pdf) 实取并定位：⭐ workshop preface 在 p. 537，⭐ 本文在 **p. 556**，⛔ 落在 MDE Intelligence 区段内 | M |
| `ccf` | ⚠️⚠️ **不能简单记 B。** ⭐ [ccf_venues/01-venue-scope.md](../../../../../ccf_venues/01-venue-scope.md) 第 55 行把 `conf-b-models \| MoDELS \| 会议 \| 🥈` 记为 **B**，⛔ **但那指主会 track**；⭐ 本文在 **Companion 卷的 workshop**，⛔ 不是主会。⭐ **按 workshop 论文计，⛔ 不享 CCF B** | S |
| ⭐ venue 评审强度 | ⭐ MDE Intelligence CFP 自陈「⭐ Each submission is reviewed by **at least 3 program committee members**, and accepted papers are published in the IEEE Satellite Event Proceedings」（⭐ 源：[workshop CFP 页](https://mde-intelligence.github.io/cfp/)） | M |
| `doi` | ⭐ [10.1109/MODELS-C68889.2025.00079](https://doi.org/10.1109/MODELS-C68889.2025.00079) —— ⭐ **本轮经 Crossref API 实核**（⭐ 返回 title / 4 位作者 / `page: 556-565` / container-title / event 全部匹配） | M |
| `arxiv` | ⛔ **无** | M |
| `url` | ⭐ [IEEE Xplore doc 11273209](https://ieeexplore.ieee.org/document/11273209/)（⛔ 付费墙） | M |
| 作者 | ⭐ Vittoriano Muttillo（U. Teramo）· Romina Eramo（U. Teramo）· Riccardo Rubei（U. L'Aquila）· Luca Berardinelli（JKU Linz） | M |
| ⭐ DBLP key | ⭐ `conf/models/MuttilloERB25` | M |
| `artifact_type` | ⭐ **BPMN 制品**（⭐ 摘要标题即 "BPMN Artifacts"）—— ⚠️ ⛔ **「artifact」具体指完整 BPMN 模型、还是建模操作序列（trace），⭐ 摘要未明说**（⭐ 见 G3） | M（BPMN）+ I（粒度） |
| `task` | ⭐⭐ **合成数据生成**（⭐ synthetic generation，⭐ 目的是解决训练数据稀缺）—— ⛔ **不是**缺陷检测、⛔ 不是一致性检查、⛔ 不是验证 | M |
| `boundary` | ⭐ **邻域**（BPMN 与工作流，见 [README.md](../README.md) §2.1） | M |

### ⭐ 摘要全文（⭐ 逐字，⭐ 本卡 B–E 节的唯一依据）

⭐ 来源：⭐ Semantic Scholar Graph API（`DOI:10.1109/MODELS-C68889.2025.00079`）返回的 `abstract` 字段，⭐ 与网络检索抓到的 IEEE Xplore 摘要在内容与语序上一致。⛔ **IEEE Xplore 页面本身因 JS 壳未能直接读取。**

> "The rise of large language models (LLMs) has led to new opportunities and challenges, particularly in model-driven engineering (MDE), where they are utilized to automate various modeling tasks. **However, current research highlights some limitations that hamper the LLMs' effectiveness, e.g., producing formatting errors in the generated modeling artifacts or semantic hallucination in domain modeling.** Modeling business process management (BPM) applications presents significant challenges to end-users, ranging from adhering to OMG standards to ensuring data privacy. Although some approaches have started investigating the intersection between LLMs and BPM modeling, a completely automated process is still far from being realized. **The main blocking issue is represented by the scarcity of modeling data, which is needed to train both LLMs and traditional modeling assistants.** Being built on our previous work, we adopt an MDE framework called **BP-MASTER-LLM**, which is devoted to supporting the specification of BPM models by combining a set of automated modeling tools, i.e., **model-event recorder and modeling assistant**. **Our findings reveal that the prominent LLMs can generate synthetic content even though human models and operations represent a better source of training data for the tested modeling assistant; nonetheless, if instructed properly, LLMs can represent a solution to overcome the data scarcity issue.**"

---

## B. LLM 应用形态（⛔ **全节仅据摘要**）

### B1 · 流水线阶段

⛔⛔ **原文未提供。** ⭐ 摘要只给出框架名与两个组件名，⛔ 没有任何阶段序列、执行者划分或阶段计数。

⭐ **摘要可确认的仅三件事**（级别 **M**）：

1. ⭐ 框架名 **BP-MASTER-LLM**，⭐ 自陈是一个 **MDE framework**
2. ⭐ 它 "combin[es] a set of automated modeling tools"，⭐ 明确点名两个：⭐ **model-event recorder** 与 **modeling assistant**
3. ⭐ LLM 的位置是**产出 synthetic content**，⭐ 该内容用于**训练那个 modeling assistant**

⭐ **由此能推出的最小结构**（级别 **S**，⭐ 从摘要「LLM 生成合成内容 → 用于训练 assistant → 与人类数据对比」这条链直接推出）：

```
[LLM] 生成合成建模内容  ─┐
                        ├→ [确定性?] 训练 modeling assistant → [确定性] 评测 assistant 效果
[人] 真实模型与操作     ─┘        （⭐ 两个训练数据来源做对照）
                                  ⭐ 数据来源经 model-event recorder 采集
```

⚠️ **⭐ 这张图里除 `[LLM]` 一格外全部标 S/I，⛔ 不得当事实引用。** ⭐ 尤其 **阶段总数与 LLM 阶段数：⛔ 原文未提供，⛔ 无法给出数字。**

### B2 · 每次 LLM 调用的角色

| 角色 | 判断 | 级别 |
| :-- | :-- | :-: |
| ⭐ **生成器** | ⭐ **确认** —— ⭐ 摘要逐字 "the prominent LLMs **can generate synthetic content**" | M |
| 抽取器 / 分类器 / 翻译器 / 评审者 / 修复者 / 规划者 / 裁决者 / 解释者 / 检索改写器 | ⛔ **原文未提供**（⛔ 摘要一个都没提） | M |

### B3 · prompt 策略

⛔ **原文未提供**（⛔ 摘要未出现 zero-shot / few-shot / CoT / RAG / schema / function calling 任一字样）。

⚠️ **⭐ 但摘要末句有一条与 prompt 强相关的表述，⭐ 必须单独记下来**（级别 **M**）：

> "nonetheless, **if instructed properly**, LLMs can represent a solution to overcome the data scarcity issue."

⭐ "**if instructed properly**" —— ⭐ 这个短语把结论**条件化到「指令是否得当」上**。⛔ 摘要没说「properly」具体指什么（⛔ 是 prompt 工程？⛔ 是给元模型约束？⛔ 是 few-shot 示例？），⛔ **无法判断**。⭐ 详见 E2 与 G4：⭐ 这个短语在**修辞上**做的事很值得注意。

### B4 · ⭐⭐ 循环与裁决者（⛔ 本轨最关键的一格）

| 子字段 | 值 | 级别 |
| :-- | :-- | :-: |
| **有无循环** | ⛔⛔ **原文未提供** | M |
| **裁决者是谁** | ⛔⛔ **原文未提供** | M |
| **终止条件** | ⛔ **原文未提供** | M |
| **最大轮数** | ⛔ **原文未提供** | M |
| **有无报告逐轮边际收益** | ⛔ **原文未提供** | M |

⛔⛔ **⭐ 本轨最重要的一格，⭐ 本篇一格都填不出来。** ⚠️ **⭐ 这是本卡对 L3 的实际价值上限：⭐ 它在 B4 上贡献为零。**

⚠️ ⭐ 一条**不能**当证据用的观察（级别 **I**）：⭐ 摘要通篇没有出现 iterative / refinement / feedback / repair / validation 任一字样，⛔ 但**摘要不提 ≠ 论文没做**——⛔ 10 页的 workshop 论文摘要本就装不下流水线细节。⛔ **不得据此推断「它没有循环」。**

### B5 · ⭐ 中间表示

| 子字段 | 值 | 级别 |
| :-- | :-- | :-: |
| **有无** | ⛔ **原文未提供** | M |
| **形态** | ⛔ **原文未提供**（⛔ 摘要未提 DSL / pattern catalogue / 缺陷类型学 / 谓词族 / JSON schema 任一） | M |
| ⭐ **是否闭合** | ⛔ **原文未提供** | M |
| ⭐ **谁定的** | ⛔ **原文未提供** | M |
| ⭐ **谁选类** | ⛔ **原文未提供** | M |

⚠️ ⭐ 唯一相关线索（级别 **I**，⛔ 不构成答案）：⭐ 摘要提到 "adhering to **OMG standards**" 是 BPM 建模对终端用户的挑战之一。⭐ OMG 标准即 BPMN 规范本身。⛔ **但「提到标准存在」与「把标准做成中间表示或校验器」是两件事，⛔ 摘要不足以区分。**

### B6 · 模型

⛔⛔ **原文未提供具体型号。** ⭐ 摘要只说 "**the prominent LLMs**"（⭐ 复数，⭐ 故**至少两个**，级别 **S**），⛔ **没有一个模型名、⛔ 没有版本、⛔ 没有日期**。

⚠️ **⭐ 按 schema 的口径，⛔ 这是一个严重缺口**：⭐ 「⭐ 用旧模型得出的结论参考价值要打折」这条判断在本篇上**无法执行**，⛔ 因为不知道用的是哪代模型。⭐ 只能按发表时点（2025-10）推测为 2024–2025 年代（级别 **I**）。

### B7 · ⭐ 确定性成分

⛔ **摘要级别只能确认「存在非 LLM 成分」，⛔ 但具体是什么全部未提供。**

| 环节 | 判断 | 级别 |
| :-- | :-- | :-: |
| ⭐ **MDE 框架 BP-MASTER-LLM** | ⭐ **存在**，⭐ 自陈是 MDE framework —— ⛔ **但「MDE」在此只是一个定语，⛔ 摘要没说它由什么构成** | M |
| ⭐ **model-event recorder** | ⭐ **存在**，⭐ 摘要点名 —— ⭐ 按字面看它是**记录建模操作事件**的工具（级别 **S**）。⛔ 是否有校验职能，⛔ 未提供 | M（存在）+ S（职能） |
| ⭐ **modeling assistant** | ⭐ **存在**，⭐ 摘要点名，⭐ 是**被合成数据训练的那个对象**（级别 **M**）。⚠️ ⛔ 它本身是否 LLM、⛔ 还是传统 recommender，⛔ **摘要未明说** | M（存在）+ 未提供（类型） |
| Ecore / EMF | ⛔ **原文未提供** | M |
| ⭐ **OCL / 元模型约束 / well-formedness 检查** | ⛔⛔ **原文未提供** —— ⚠️ **⭐ 这一格正是用户最想知道的，⛔ 摘要给不出答案** | M |
| ⭐ BPMN schema / XSD 校验 | ⛔ **原文未提供** | M |
| 模型检查器 / 求解器 | ⛔ **原文未提供** | M |

---

## C. 实验（⛔ **全节仅据摘要**）

| 字段 | 值 | 级别 |
| :-- | :-- | :-: |
| `baseline` | ⭐⭐ **有，且能从摘要确认是什么**：⭐ **人类产出的模型与建模操作**（"human models and operations"）⭐ 作为训练数据来源的对照臂 | M |
| `dataset` | ⛔ **原文未提供**（⛔ 无名称、⛔ 无规模、⛔ 无来源、⛔ 无分母口径）。⚠️ ⭐ 唯一相关表述是把 "**scarcity of modeling data**" 立为核心问题 | M |
| `metrics` | ⛔⛔ **原文未提供。** ⛔ 摘要只说人类数据是 "a **better** source"，⛔ **没有任何指标名、⛔ 没有数字、⛔ 没有 `@k` 口径** | M |
| ⭐ `judged_by` | ⛔⛔ **原文未提供**（⛔ 无法判断是作者 / 第三方 / 自动脚本 / LLM-as-judge）。⛔ **无标注者间一致性信息** | M |
| `human_baseline` | ⚠️⚠️ **需要小心区分，⛔ 极易读错**：⭐ 「human models and operations」是**训练数据的对照来源**，⛔ **不是「人类专家执行同一任务作为性能基线」**。⛔ 后者：**原文未提供** | S |
| `runs` | ⛔ **原文未提供**（⛔ 无次数、⛔ 无均值/单次说明、⛔ 无方差） | M |
| ⭐ `adverse_results` | ⭐⭐ **有，⭐ 而且写在摘要里 —— ⭐ 见下方 C1，⭐ 这是本卡对我们唯一的实质贡献** | M |

### ⭐ C1 · ⭐⭐ 它怎么写不利结果（⭐ 摘要级，⛔ 但结构完整）

⭐⭐ **本篇的主结果对自己的方案不利，⛔ 而它没有藏 —— ⭐ 不利结论就在摘要末句，⭐ 与正面结论同一句话里。**

⭐ **逐字拆解那一句**（级别 **M**）：

> "Our findings reveal that **⑴ the prominent LLMs can generate synthetic content** **⑵ even though human models and operations represent a better source of training data for the tested modeling assistant**; **⑶ nonetheless, if instructed properly, LLMs can represent a solution to overcome the data scarcity issue.**"

| 段 | 内容 | ⭐ 修辞功能 |
| :-: | :-- | :-- |
| **⑴** | ⭐ LLM **能**生成合成内容 | ⭐ **先立可行性**（⛔ 一个低门槛的正面事实） |
| **⑵** | ⛔ **但人类数据是更好的训练来源** | ⛔⛔ **这就是不利结果。** ⭐ 用 "even though" 从属连词引入，⭐ 语法上被降级为让步状语 —— ⛔ **不利结论没有独占一个主句** |
| **⑶** | ⭐ "nonetheless, **if instructed properly**" LLM 仍是解法 | ⭐ **用条件从句翻盘**，⭐ 并把结论落在**问题（数据稀缺）被解决**上，⛔ 而不是落在「⭐ 我方比人类好」上 |

⭐⭐ **⭐ 与 TSE 那篇（[tse2026-process-fragment-recommendation.md](./tse2026-process-fragment-recommendation.md) §C1）对照，⭐ 两篇处理不利结果的手法可以并列成一张表**：

| | ⭐ 本篇（MODELS-C 2025） | ⭐ TSE 2026 那篇 |
| :-- | :-- | :-- |
| ⭐ 不利结果的语法位置 | ⛔ **让步状语从句**（"even though …"）—— ⭐ 藏得较深 | ⭐ **摘要主句 + 标题问句** —— ⭐ 摆在最前面 |
| ⭐ 翻盘手段 | ⚠️ **一个未量化的条件**（"if instructed properly"）—— ⛔ **摘要里没有任何数据支撑这个条件** | ⭐ **一个已量化的切分**（">6 nodes 时 LLM 赢 1.69×"）—— ⭐ 有数字 |
| ⭐ 结论落点 | ⭐ 落在「⭐ 问题可被解决」 | ⭐ 落在「⭐ 实践者该怎么选」 |
| ⭐ 我们能否借鉴 | ⚠️ **谨慎** —— ⭐ 这个写法**依赖一个未证明的条件**；⛔ 若我们对 −15.82pp 写「调好 prompt 就行了」而无实测，⛔ 就是同一个毛病 | ⭐⭐ **可直接借鉴** |

⭐⭐ **⭐ 结论：⭐ 本篇提供的是一个「⛔ 不该照抄的」不利结果写法样本。** ⭐ 它的价值恰在于反面：⭐ 「if instructed properly」这种条件式翻盘**在摘要层面读起来很顺**，⛔ 但它把举证责任推给了一个未定义的条件。⚠️ ⭐ 这与本仓库 [talks/GUIDE.md](../../../../../talks/GUIDE.md) §9「⛔ 标 I 的不得写成事实句」以及「⭐ 方向性松紧要一致」两条纪律**存在张力**。

---

## D. ⭐ 资产（⛔ 全部本轮实际取过）

| 资源类型 | 状态 | URL / 路径 | ⭐ 核验证据 |
| :-- | :-: | :-- | :-- |
| 论文全文 | ⛔⛔ **🔒** | [10.1109/MODELS-C68889.2025.00079](https://doi.org/10.1109/MODELS-C68889.2025.00079) | ⭐ **Unpaywall：`is_oa: false` · `oa_status: closed` · `oa_locations: []` · `has_repository_copy: false`**。⭐ OpenAlex：`is_oa: False` · `any_repository_has_fulltext: False`。⭐ IEEE Xplore 页 `HTTP 202` + JS 壳。⭐ Crossref 的 `xplorestaging` PDF 链 → `HTTP 200 / content-type: text/html`（⭐ IEEE 购买页）。⭐ 13 条入口全部记在本卡开头 |
| ⭐ **实验代码** | ⛔ **⚪ / 🟠** | ⭐ **未知** | ⛔⛔ **摘要未提任何 repository / artifact / availability 语句。** ⭐ 检索 `BP-MASTER-LLM` 于 GitHub 与网络：⛔ **0 命中**（⛔ 搜索引擎明确回报「no project, paper, or GitHub repository by that name」）。⚠️ ⭐ 判 ⚪ 会断言「原文明确未提供」，⛔ 而全文不可得故**无法断言**；⭐ **实际口径应为 🟠（信息不清）** |
| ⭐ **数据集 / Benchmark** | ⛔ **🟠** | ⭐ **未知** | ⛔ 摘要无数据集名、无规模、无链接。⚠️ ⭐ 讽刺的是本文**主题就是数据稀缺**，⛔ 却无法确认它产出的合成数据是否公开 |
| 实验结果细则 | ⛔ **🟠** | ⭐ **未知** | ⛔ 摘要仅给一句定性结论（"a better source"），⛔ 无表格、无数字。⛔ 论文内是否有逐条结果，⛔ 无法确认 |
| Artifact / 复现包 | ⛔ **🟠** | ⭐ **未知** | ⛔ 未检出 Zenodo / 4open / OSF 记录。⚠️ ⭐ MDE Intelligence 2025 CFP 未见 artifact evaluation 要求 |
| ⭐ **prompt 是否公开** | ⛔ **🟠** | ⭐ **未知** | ⛔ 摘要提到 "if instructed properly"，⭐ 暗示 prompt 是变量之一，⛔ **但是否公开无法确认** |
| ⚠️ **前置工作（⛔ 另一篇）** | ⭐ **🟡** | [IST 186:107806 (2025)](https://doi.org/10.1016/j.infsof.2025.107806) | ⭐ Unpaywall 实测 **`is_oa: True` · `oa_status: hybrid` · `license: CCBY`**，⭐ 故**原则上可取**；⛔ 但 ScienceDirect 对本环境返 **403**，⭐ 本轮未取到正文。⛔ **注意：这是另一篇论文，⛔ 不能替本卡填格** |
| ⭐ 会议 TOC（⭐ 用于定位 track） | ⭐ **🟢** | [proceedings.com TOC PDF](https://www.proceedings.com/content/083/083457webtoc.pdf) | ⭐ `HTTP=200 SIZE=399150`，⭐ 实提取 16 页，⭐ 在第 506 行定位到本文标题，⭐ 确认落在 **MDE Intelligence 2025**（⭐ preface p. 537）区段 |

### ⭐ 终裁说明

⭐⭐ **资产一栏全线 🔒 / 🟠 / ⚪，⛔ 没有一项 🟢（⭐ 除了会议 TOC，⛔ 那不是论文资产）。**

⚠️ **⭐ 一条口径说明**：⭐ 按 schema，⚪ 的含义是「⛔ **原文明确**未提供 / 不存在」。⛔ **本篇不能用 ⚪**，⭐ 因为全文不可得 → ⭐ **无从知道原文说了什么**。⭐ 所以除论文全文本身（🔒，⭐ 有硬证据）外，⭐ 其余一律 **🟠（信息不清）**，⛔ 而不是 ⚪。⭐ 这个区分不是形式主义：⛔ **判 ⚪ 会让后续读者以为「已确认它没放代码」，⭐ 而真相是「我们没看到论文」。**

---

## E. ⭐ 对 M1 的意义

### 1. ⭐ 可取之处

| # | 能拿走的东西 | ⭐ 说明 |
| :-: | :-- | :-- |
| **1** | ⭐⭐ **「格式错误 vs 语义幻觉」这个二分本身，⭐ 在 MDE 圈子里是被公认的问题陈述** | ⭐ 摘要把它写成 "**current research highlights** some limitations …, e.g., producing **formatting errors** in the generated modeling artifacts or **semantic hallucination** in domain modeling"（级别 **M**）。⭐ 注意 "current research highlights" —— ⭐ 这是**在综述既有文献**。⭐ **对我们的用处：⭐ 这个二分可以作为一个「⭐ 领域已有共识」引用**，⛔ 而不必由我们首创。⚠️ ⭐ 但若要进论文，⛔ 必须回到 L1/L2 的门重走（[README.md](../README.md) §3 防火墙），⛔ 且**应当去引它引的那些原始文献，⛔ 而不是引这篇 workshop 论文** |
| **2** | ⭐ **同组把「合成数据补训练数据」当作一条独立研究线** | ⭐ 摘要把 "scarcity of modeling data" 立为 "the **main blocking issue**"（级别 **M**）。⭐ 这与我们的 54 pair 规模困境同源。⛔ **但他们的解法（生成更多数据）与我们的路线（在小样本上做精细判定）方向不同**，⛔ 不构成可搬的设计 |
| **3** | ⭐ **一个「不利结果写法的反面样本」** | ⭐ 见 C1：⭐ "if instructed properly" 这种未量化条件式翻盘，⛔ **正是我们写 −15.82pp 时要避免的形状** |

### 2. ⛔ 不可取 / 陷阱

| # | 陷阱 | ⭐ 说明 |
| :-: | :-- | :-- |
| **1** | ⛔⛔ **⭐ 不要把这篇当成「§11 纪律的外部对照」——⭐ 该假设未被证实** | ⚠️⚠️ **⭐ 这是本卡最重要的一条结论，⭐ 详见 F1。** ⭐ 摘要**确实**区分了两类失败，⛔ **但那出现在动机段、⭐ 被归因于「current research」**；⛔ 摘要**没有任何**表述说本文用 MDE 手段去**兜住**它们，⛔ 也没有任何量化。⭐ 本文的实际研究对象是**合成训练数据**。⛔ **在取到全文之前，⛔ 不得把它当作 §11 的外部背书。** |
| **2** | ⛔ **⭐ 不要据「摘要没提循环」推断「它没有循环」** | ⭐ 见 B4 末段。⭐ 10 页 workshop 论文的摘要装不下流水线细节。⛔ **摘要沉默不是证据。** |
| **3** | ⚠️ **⭐ 不要把 "human models and operations" 读成人类性能基线** | ⭐ 见 C 节 `human_baseline`。⭐ 它是**训练数据来源**的对照，⛔ 不是「人类做同一任务做得多好」。⛔ 这两件事在引用时**极易混淆**。 |
| **4** | ⚠️ **⭐ 不要用它当「LLM 生成的建模制品质量不行」的证据** | ⭐ 它的结论是「⭐ 作为**训练数据**，⭐ 人类的更好」，⛔ **不是**「⭐ LLM 生成的模型质量差」。⛔ 换个任务就不成立。⭐ 且**模型型号未知**（B6），⛔ 结论的代次适用性无法评估 |

### 3. ⚠️ 与我们的关键差别

| 维度 | ⭐ 它 | ⭐ 我们 | ⛔ 为什么不能照搬 |
| :-- | :-- | :-- | :-- |
| **任务** | ⭐ **合成数据生成**（⭐ 造训练语料） | ⭐ **缺陷检测**（⭐ 判已有模型对不对） | ⛔⛔ **根本不同。** ⭐ 它的成功判据是「⭐ 训出来的 assistant 好不好」，⛔ 是一个**下游代理指标**；⭐ 我们的判据是「⭐ 有没有发现那条缺陷」，⭐ 是**直接判定**。⛔ 两套评测机制不可互换 |
| **LLM 的地位** | ⭐ **数据工厂**（⭐ 产语料） | ⭐ **判定者链条**（⭐ 拆需求 / 造断言 / 裁定） | ⛔ 它不需要 LLM 的产出「正确」，⭐ 只需要「⭐ 足够像真数据以便训练」——⭐ 这是一个**远低于我们**的正确性要求 |
| **不利结果的处理** | ⚠️ ⭐ 让步从句 + 未量化条件翻盘 | ⭐ 待定（−15.82pp） | ⭐ **可作反面参照**，⛔ 不可作正面模板 |
| **B4（⭐ 本轨核心）** | ⛔ **一格都填不出** | ⭐ 有两种裁决者的内部对照 | ⛔ **无可对照** |

---

## F. ⛔ 用户必答问题的逐条回答

### ⭐ F1 · ⭐⭐ 两类失败各自用什么手段兜的？⭐ 格式错误 → 什么？⭐ 语义幻觉 → 什么？⭐⭐ 它有没有试图用确定性检查去抓语义幻觉？

⭐⭐ **⭐ 直接回答：⛔⛔ 原文未提供 —— ⭐ 而且更重要的是，⭐ 摘要里没有任何证据表明本文「兜」了这两类失败中的任何一类。**

⭐ **必须把用户的假设与摘要实际说的话逐字对齐**：

| ⭐ 用户的假设 | ⭐ 摘要实际说的 | ⭐ 判定 |
| :-- | :-- | :-- |
| ⭐ 「它**显式区分了** LLM 生成建模制品的两类失败」 | ⭐ **成立。** ⭐ 逐字："e.g., producing **formatting errors** in the generated modeling artifacts **or** **semantic hallucination** in domain modeling" —— ⭐ 两类并列，⭐ 用 "or" 分开 | ⭐ **✅ 确认（M）** |
| ⭐ 「⭐ **并用 MDE 手段兜住**」 | ⛔⛔ **不成立 / 无从确认。** ⚠️ ⭐ 关键在这个二分出现的**位置与归属**：⭐ 它在摘要**第二句**，⭐ 由 "**current research highlights** some limitations that hamper the LLMs' effectiveness" 引出 —— ⭐ 即这是**在陈述既有文献发现的局限，作为本文的动机**。⛔ **摘要没有任何一句说本文检测、度量、拦截或修复了这两类失败。** | ⛔ **❌ 未确认（M：摘要无此表述）** |

⭐⭐ **⭐ 而且本文的实际研究对象是另一件事**（级别 **M**）：⭐ 摘要自己指认核心问题是 "**The main blocking issue is represented by the scarcity of modeling data**"，⭐ 而贡献是用 LLM 生成合成内容来补这个缺口。⭐ **这是一篇数据增强论文，⛔ 不是一篇制品校验论文。**

⭐ **逐条回答用户的三个子问**：

| 子问 | 答案 | 级别 |
| :-- | :-- | :-: |
| ⭐ **格式错误 → 用什么兜的？**（⭐ 语法 / schema / parser） | ⛔⛔ **原文未提供。** ⛔ 摘要未出现 parser / syntax / schema / XSD / validation 任一字样 | M |
| ⭐ **语义幻觉 → 用什么兜的？**（⭐ 元模型约束 / OCL / 人 / LLM 评审） | ⛔⛔ **原文未提供。** ⛔ 摘要未出现 OCL / metamodel constraint / review / human-in-the-loop 任一字样 | M |
| ⭐⭐ **它有没有试图用确定性检查去抓语义幻觉？** | ⛔⛔ **无法确认 —— ⭐ 但这恰恰是本卡最需要后续跟进的一格** | M |

⭐⭐ **⭐ 关于第三问，⭐ 有一条需要主 session 知道的推理链，⭐ 级别 I，⛔ 不得当事实**：

⭐ 摘要说这是一个 "**MDE framework**"。⭐ 在 MDE 传统里，「用元模型 + OCL 约束去校验生成物」是标准做法。⭐ **所以「它可能确实用确定性约束去抓语义问题」是一个合理猜测。** ⛔ **但这个猜测正好落在我们最危险的方向上** ——⭐ 因为本仓库 [CLAUDE.md](../../../../../CLAUDE.md) §11 的整条纪律就是：⛔ **「⭐ 只有能被完美判定的约束才允许进 schema validator；⛔ 需要语义判断的必须放到 prompt + 评审端」**，⭐ 而我们栽的那次事故正是**把语义判断实现成词法判断**（⛔ `name_in_sentence` 含并列连接词即拒 → ⛔ 18/18 撞死、⛔ 约 16 万 output token 白烧、⛔ 全量 2928 行里 190 行被拒且多为误伤）。

⚠️⚠️ **⭐ 所以这一格的正确结论是：**

> ⛔ **本篇既不能证实、也不能证伪「⭐ 用确定性检查抓语义幻觉」这条路的可行性。** ⭐ 它是一个**高优先级的待取全文对象**（⭐ 见 G1 建议），⛔ **但在取到全文之前，⛔ 它对 §11 的支持度为零。** ⭐ 若日后取到全文并发现它**确实**用 OCL / 元模型约束去抓语义幻觉，⭐ 那**才是** §11 的外部对照 —— ⭐ 且届时需要重点看：⭐ **它有没有报误伤率**（⛔ 这是我们那次事故的核心代价，⛔ 而绝大多数论文不报这个数）。

### ⭐ F2 · ⭐ 兜住的比例是多少？⭐ 有没有量化两类失败各占多少？

⛔⛔ **原文未提供，⭐ 一个数字都没有。**

⭐ **摘要里全部「结果」性表述只有一句，⭐ 且完全定性**（级别 **M**）：

> "human models and operations represent **a better** source of training data for the tested modeling assistant"

⭐ **"a better" —— ⛔ 没有百分比、⛔ 没有指标名、⛔ 没有分母、⛔ 没有显著性。**

⛔ **两类失败的占比：⭐ 摘要连一个总数都没给**，⛔ 更没有分类占比。⭐ 级别 **M（明确未提供）**。

### ⭐ F3 · ⭐ MDE 手段具体是什么（Ecore / EMF / OCL / BPMN schema / 模型检查）？

⭐ **摘要能给出的全部内容，⭐ 逐字**（级别 **M**）：

> "we adopt an MDE framework called **BP-MASTER-LLM**, which is devoted to supporting the specification of BPM models by combining a set of automated modeling tools, i.e., **model-event recorder** and **modeling assistant**."

⭐ **即：⭐ 一个框架名 + 两个组件名，⛔ 零技术栈信息。**

| ⭐ 用户点名的技术 | ⭐ 是否在摘要出现 | 级别 |
| :-- | :-: | :-: |
| Ecore | ⛔ **未出现** | M |
| EMF | ⛔ **未出现** | M |
| ⭐ **OCL** | ⛔ **未出现** | M |
| BPMN schema / XSD | ⛔ **未出现**（⚠️ ⭐ 只出现 "adhering to **OMG standards**" 这一泛指） | M |
| 模型检查 | ⛔ **未出现** | M |

⭐ **能确认的两个组件，⭐ 按字面理解**（级别 **S**，⭐ 从组件命名直接推）：

1. **`model-event recorder`** —— ⭐ 看起来是记录**建模操作事件**的工具（⭐ 即建模者在编辑器里的动作序列）。⭐ 这与该组的前置工作标题「⭐ synthetic trace generation of **modeling operations**」⭐ 在概念上一致。⛔ **但它是不是校验器，⛔ 摘要完全没说。**
2. **`modeling assistant`** —— ⭐ 摘要明确它是**被训练的对象**（⭐ "training data **for the tested modeling assistant**"），⭐ 也就是**评测的下游代理**。⛔ 它本身是 LLM 还是传统 recommender，⛔ 未提供。

⚠️ **⭐ 一条重要观察（级别 S）**：⭐ 从这两个组件名看，⭐ **BP-MASTER-LLM 的重心在「采集与消费建模操作数据」，⛔ 而不在「校验生成物的正确性」。** ⭐ 若这个读法成立，⭐ 那么本文压根**不是**一篇关于「怎么兜住 LLM 失败」的论文 —— ⛔ 那两类失败只是它 motivation 段落里的一句背景。⚠️ ⛔ **但这只是从命名推的，⛔ 不是事实。**

---

## G. ⛔ 存疑与未核项

1. ⛔⛔ **⭐ 全文不可得 —— ⭐ 13 条入口全试过，⭐ 逐条列在本卡开头。** ⚠️ **⭐ 建议：⭐ 本篇是全轮次里「⭐ 潜在价值 vs 已知信息」落差最大的一条**。⭐ 若主 session 能通过机构订阅取到 IEEE Xplore 全文，⭐ 应当**优先重抽这张卡**，⭐ 并重点填三格：⭐ ① **B7 是否有 OCL / 元模型约束**；⭐ ② **B4 有无循环、裁决者是谁**；⭐ ③ **若确有确定性语义检查，⭐ 它报不报误伤率**。
2. ⚠️⚠️ **⭐ 用户假设「⭐ 它用 MDE 手段兜住两类失败」⛔ 未被证实。** ⭐ 摘要只支持「⭐ 它区分了两类失败」这前半句，⭐ 而且是**作为对既有文献的综述**出现在动机段。⛔ **本卡不得被引用为 §11 纪律的外部对照。** ⭐ 详见 F1。
3. ⚠️ **⭐ 「BPMN Artifacts」的粒度未定** —— ⭐ 标题说 "BPMN Artifacts"，⭐ 摘要说 "synthetic content"，⭐ 而两个组件名指向「建模操作」。⛔ **无法确定它生成的是完整 BPMN 模型、还是建模操作序列（editing traces）、还是两者。** ⚠️ ⭐ 这直接影响它是否算「⭐ 行为类模型制品」硬门 2 —— ⭐ 我按 BPMN 判**过门**，⛔ 但若它实际生成的是操作序列而非模型，⛔ 该判定需要复核。
4. ⚠️ **⭐ "if instructed properly" 指什么 —— ⛔ 未提供。** ⭐ 这个短语承载了摘要末句的全部翻盘力量，⛔ 但它可以指 prompt 工程、⛔ few-shot 示例、⛔ 元模型约束注入、⛔ 或输出格式规约中的任何一种。⛔ **无法区分，⭐ 而这恰好是我们最想知道的那一格。**
5. ⚠️ **⭐ 模型型号完全未知**（B6）。⭐ 只知「the prominent LLMs」是复数。⛔ 无法执行 schema 要求的「⭐ 旧模型结论要打折」这条判断。
6. ⚠️ **⭐ `BP-MASTER-LLM` 检索不到任何公开实现** —— ⭐ 已试 GitHub 与网络检索，⛔ 0 命中（⛔ 搜索引擎明确回报无此名项目/仓库）。⚠️ ⭐ 这**不等于**没有仓库（⛔ 可能名字在论文里不同、⛔ 或未公开），⛔ 但也无法判 🟢。
7. ⚠️ **⭐ 前置工作 IST 186:107806 是 CC-BY hybrid OA，⛔ 但本轮未取到正文**（⛔ ScienceDirect 403，⛔ S2 摘要被 elide）。⚠️ ⭐ **建议**：⭐ 若要理解 BP-MASTER-LLM 的框架构成，⭐ 那篇是**开放许可、⭐ 因此更容易合法取得**的入口。⛔ **但它是另一篇论文，⛔ 取到后应当单独抽卡，⛔ 不得用来补本卡的空格。**
8. ⚠️ **⭐ CCF 归属需主 session 裁定** —— ⭐ MoDELS 主会在 [ccf_venues](../../../../../ccf_venues/01-venue-scope.md) 记为 **B**，⛔ 但本文在 **Companion 卷的 MDE Intelligence workshop**。⭐ 我按「⛔ workshop 论文不享主会 CCF 等级」处理，⛔ 但仓库的 `ccf_venues` 目录**没有明文规定 Companion / workshop 该怎么记**，⭐ 故此判为**我方口径**而非既定规则。
9. ⚠️ **⭐ 摘要来源是 Semantic Scholar API，⛔ 不是 IEEE Xplore 页面本身。** ⭐ 两者内容经网络检索摘要交叉比对一致（⭐ 同样的四句、同样的语序、同样的 "main blocking issue" 表述），⛔ 但**未能直接从 IEEE 页面读取原文核对逐字**。⭐ 级别按 **M** 记，⚠️ ⛔ 但这一层间接性应当知道。
