# L1 · 技术版图与对照系 —— 五问结论与落档理由

⭐ 本文件是 L1 轨的**总账**。执行规则真源是伞 PR [#179](https://github.com/HansBug/research_ideas/pull/179) §4；落档预案真源是 [../CONTINGENCY_L1.md](../CONTINGENCY_L1.md)。⛔ 本文件不重述它们。

⚠️⚠️ **全份证据级别声明**：本轮**未读任何一篇新收论文的全文**，唯三例外是三篇 S1 预判件（SoSyM 2026 出版方 OA PDF 40 页 · nl2postcond arXiv 全文 24 页 · MCeT 仓库内 `paper_content.txt` 1316 行）。⛔ 因此按 `CONTINGENCY_L1.md` §0.1.5 第 3 条，索引表的「正文读了没」列**一格都还不能填** —— ⛔ 填「是」「✅」一律视为未读。

---

## 0. 五问落档速览

| 问 | 落档 | 判据栏第几条被满足 / 未满足 |
| :-- | :-- | :-- |
| **Q1** 技术路线分类 | ⏳ **待层 2** | ⛔ 界内**没有任何一个类目**能凑满「≥3 篇且含 ≥1 篇 2022+」（§0.1.6 第 1 条）。⚠️ 且起点池对 Q1 的采样有**系统性偏倚**（§2），⛔ 按现有池子排类目大小会失真 |
| **Q2** NL↔模型一致性检查 | ⭐ **B 档**（两条路径都落 B 档交付形态） | ⛔ A 档判据「≥3 篇界内检查侧」**未满足**（$k_{\text{界内}} = 0$）；⭐ B 档情况栏「存在功能等价的两段式路线」**被满足**。⚠️ **但 contribution 后果取决于 N-3 的裁定**，见 §3 |
| **Q3** 外部可比数字 + 「为什么必须自建」 | ⭐ **B 档** | ⛔ A 档「≥1 篇四门全中」**未满足**（逐条筛除 14+ 条候选，**0 条全中**）；⭐ B 档「存在量级背景事实但对象/执行者不同」**被满足** |
| **Q4** 断言 / 契约 / 可执行规约 | ⭐ **B 档，⛔ 不是 C 档** | ⛔ C 档情况栏是**合取**（「闭合词表 = 0」**且**「界内连模式目录都撑不起」），⭐ **第二个条件为假**（模式目录 6 篇实在）；⭐ 且 C 档判据要求「说清 Dwyer 一系为什么不算」—— **说得清** |
| **Q5** LLM 模型评审（2022+） | ⭐ **A 档**（⚠️ 带一条硬限定） | ⭐ 判据第 1 条「≥3 篇 2022+、LLM 在已有行为模型上找问题、有评测口径」**被满足**（3 篇）。⚠️ **但没有一篇的制品是状态机** |

⭐ **按 §0.1.4 第 2 条取档**：Q5 的 A 与 B 有同真区间（若把摘要级那篇暂缓则落 B）—— ⛔ 取**后果更重**的 A 档，⛔ 不许挑对我方有利的 B。

---

## 1. ⭐⭐ 本轮最重要的单条发现：任务形状已经被人做过了

**MCeT**（Ahmed 等，MODELS 2025，pp. 84–95，DOI [`10.1109/MODELS67397.2025.00014`](https://doi.org/10.1109/MODELS67397.2025.00014)）把「**LLM 判已有行为模型 vs 需求正文、逐条锚回需求原子、输出 issue 列表**」这个形状**做完了**，还给了数：precision `0.58 → 0.81`、FBENCH recall `34.1% → 68.1%`。

⛔⛔ **它与我们的差别落在制品类型上，⛔ 不落在任务形状上。** ⚠️ 这句话无论 N-3 怎么裁都成立。

### ⛔⛔ 而且它自己声称了一个「首个」，⭐ 直接压在 C-① 的定位上

⚠️ **本条是独立核验溢出发现的，⛔ 而前面五路调研通篇没提。** MCeT 原文第 129–131 行**逐字**：

> ```
> To the best of our knowledge, MCeT is the first LLM-
> based approach to evaluate a behavioral diagram model against
> free-style requirements texts, detecting discrepancies between
> ```

⭐ **本方逐字核实过这段**（⚠️ 顺带纠正核验者的一处引文失真：它转述为「the first approach to perform fully automated evaluation of a behavioral model against its requirements」，⛔ **原文不是这个措辞** —— 原文是「the first **LLM-based** approach」，且限定语是「**behavioral diagram model**」与「**free-style requirements texts**」）。

⭐⭐ **三条限定给我们留了空间，⛔ 但必须逐条守住，且都不是「制品不同」这一条**：

| MCeT 的限定 | ⭐ 我们的位置 | ⛔ 注意 |
| :-- | :-- | :-- |
| **LLM-based** | 我们也是 | ⛔ 这一条**不给我们空间** |
| **behavioral diagram model** | ⚠️ 状态机也是 behavioral diagram | ⛔ 这一条**也不给空间** —— ⚠️ 不要指望「序列图 ≠ 状态机」能挡住一个说「behavioral diagram model」的 first 主张 |
| **evaluate against free-style requirements texts** | 我们也是 | ⛔ 同样不给空间 |

⛔⛔ **结论：这个 first 主张在字面上覆盖我们。** ⭐ 我们能站住的差异化**不在任务上**，只在 §1 那张表的后两行 —— **判定可机械求值** 与 **可重放**。⚠️ 而按 §2 前置纪律 ①，那两项**只进对照表、不进计数** —— ⭐ 也就是说它们撑不起「新颖性」，⛔ 只撑得起「与既有工作不同」。

⭐ **这是 L1 对 C-① 强度上限最直接的一条输入**：⛔ 在本轮覆盖范围内，C-① 的新颖性档位**不应高于「与既有工作不同」**。⛔ L1 不裁定档位（§0.1.2 禁语），⭐ 但这条事实必须原样交给 R1。

⭐ 三处**真实**的差别（⛔ 按 §2 前置纪律 ①，后两项只进对照表列、⛔ 不进计数）：

| 差别 | MCeT | 本文 |
| :-- | :-- | :-- |
| **制品** | UML 序列图 | 状态机（$M = (S,E,V,Tr,A)$） |
| **判定是否可机械求值** | ⛔ 全程 LLM 自然语言判定；issue 是散文 | ⭐ 可机械求值的断言 |
| **可否重放** | ⛔ 未见重放机制 | ⭐ 断言可在制品上独立复算 |

⚠️ **`baselines/mcet/` 的评级需要重估，⛔ 但「旧口径打的应升级」这个提法前提错了。** ⭐ 实测 [`baselines/GUIDE.md`](../../../baselines/GUIDE.md) §3.5 的四级 emoji 表，**其定义本身就是任务绑定的** —— 🟢 逐字要求「输出必须是状态机族模型…与『自然语言自动生成状态机模型』任务直接可比」。⛔ **在那张表自己的定义下，🟠 是正确的编码**（MCeT 的输出确实不是状态机族模型），⭐ 四级里没有任何一级能表达「issue-discover 口径下最近的可比对象」。⭐⭐ **这张表缺的是一个维度，⛔ 不是缺一次调档。**

⭐ 处置：⛔ 不动 emoji（否则对其余 90 个目录失去一致性）；⭐ 改**理由句**（现文「这是行为模型评估器，不是状态机生成器」⛔ 在 issue-discover 口径下会把我们自己也否掉）；⭐ 并把 issue-discover 四门结果记在**本目录**而非公共 `baselines/`（根 [CLAUDE.md](../../../../CLAUDE.md) §9.5：`baselines/` 是跨论文公共资产）。

---

## 2. Q1 · ⚠️ 起点池的真实缺口是「近年 × 界内」这一格

⭐ 详见 [pool_audit.md](./pool_audit.md)。此处只记结论与外部补充。

| 类目 | 起点池界内 | 2022+ | ICSE/FSE/ASE 族补充 | 判定 |
| :-- | ---: | ---: | :-- | :-- |
| ① 模型检查 | ≥ 12 | 3 | HSM'98 · Reduction/Slicing'97 · USMMC'13 | ⏳ 需层 2 |
| ② conformance / 测试 | ≥ 9 | 2 | EFSM+NSGA-III'19 · mCUTE'19 · Provengo ASE'23 | ⏳ 需层 2 |
| ③ 静态规约检查（OCL / WFR） | **3，全「部分」** | **0** | ⛔ **`OCL\|SCXML\|JML\|design by contract` 在三族 2748 条题录中命中 2**，唯一相关是 FSE'23 的 DL API contract | ⛔ 不满足 2022+ 门槛 |
| ④ 仿真与执行 | ≥ 10 | 3 | — | ⏳ 需层 2 |
| ⑤ **LLM 评审 / 缺陷检测** | **0** | 0 | ⛔ 界内 **0**；邻域 4 条 | ⛔ 起点池 + 本族界内皆空 |
| ⑥ 变形 / 差分 | **0** | 0 | Mutation Model Checking FSE'23 | ⛔ 起点池空 |

### ⛔⛔ 初版在这里写的因果论证**不成立** —— ⭐ 而它错在漏引了两个词

⚠️ 初版称 `DESC_GUIDE.md` §3 拒收「纯方法/纯工具的缺陷发现工作」→ 起点池**系统性遗漏**那一类 → 类目分布失真。⛔ **该论证已被推翻。**

⭐ 原文第 4 条**逐字**是「主要创新在算法、验证、综合或转换方法，但对形式主义本体**、构造方式和基础设施**没有新增**可用**证据的论文」—— ⛔⛔ **初版丢掉了「、构造方式和基础设施」与「可用」，而那两项正是工具论文的立身之处。** ⭐ `README.md` §1 更把「**标准/基础设施**：交换格式、Schema、元模型承载、运行时、**工具链**、互操作设施」列为**第 3 优先收录**。

⛔ **结论被池子本身证伪**：实测工具角色 163 行 · 验证角色 178 行 · 交集且界内 62 行；⭐ 本方抽验 `the-model-checker-spin` · `nusmv-a-new-symbolic-model-verifier` · `uppaal-40` · `torx-automated-model-based-testing` **全部在池子里**。⛔⛔ **纯工具的缺陷发现工作在池子里成堆，不是被系统性遗漏。**

⭐⭐ **真实的偏斜**：那些工具论文**压倒性地是 2018 年以前、且形式主义界外**（时间自动机 / Petri 网 / 概率）。⭐ 所以起点池对 Q1 的真实缺口是 **「近年 × 界内」这一格**。

⚠️⚠️ **为什么这个更正重要**：⛔ 按错误诊断去补「纯方法/纯工具」，会补到一堆池子里**已经有**的东西，而 **2022+ 的真缺口照旧**。⭐ 仍然成立的是 ⑤⑥ 为 0，⛔ 但正确解释是**时间**（2022 年后才兴起，而池子重心在 2018 年前），⛔ 不是「不产出新形式主义所以被规则拒收」。

### ⛔ D 档（换轴）：判据第 1 条**未被满足**

⚠️ 初版称「已出现 1 例」（`designing-fsm-...-gpt4` 落 ②⑤⑥），⛔ **该例证已撤回** —— 它落 ⑤ 是靠把「生成后自评」算成评审侧，而 §5-A 判据第一问明确排除。⭐ 去掉 ⑤ 后它只落 2 类。⭐ **现状：无一例落 ≥3 类**，落 2 类的有两例。

---

## 3. Q2 · $k_{\text{界内}} = 0$，$k_{\text{邻域}} = 2$ —— ⚠️ 档位取决于一条刚补上的默认值

### 3.1 检查侧计数

按 §2 前置纪律 ① 的第一层两问（① 输入里有没有一份**别人给的**模型？② 输出锚不锚在**需求条目**上？）：

| 篇目 | ① | ② | 计入 | 对象 |
| :-- | :-: | :-: | :-- | :-- |
| **MCeT**（MODELS 2025） | ✅ | ✅ | ⭐ 是 | ⚠️ UML 序列图 → **邻域** |
| **Requirements Satisfiability with In-Context Learning**（RE 2024，DOI [`10.1109/RE59067.2024.00025`](https://doi.org/10.1109/RE59067.2024.00025)） | ✅ | ✅（逐条对 8 条 GDPR 需求判满足/不满足） | ⭐ 是 | ⚠️ 文本设计描述 → **邻域** |
| **Completion of SysML state machines from GWT requirements**（SoSyM 23(6)，DOI [`10.1007/s10270-024-01228-3`](https://doi.org/10.1007/s10270-024-01228-3)） | ✅（**已有的部分 SysML 状态机**） | ⚠️ 待层 2 | ⏳ **待裁定** | ⭐ 状态机 → **界内** |
| `inference-time-intervention` / `ai-driven-consistency-sysml` | ✅ | ✅ / ⚠️ | 邻域 | Capella/SysML 架构图 · UCD/BD |

$$k_{\text{界内}} = 0 \ (+1\ \text{待裁定}), \qquad k_{\text{邻域}} = 2$$

⛔⛔ **$k_{\text{邻域}}$ 于 2026-08-12 由 3 更正为 2**：⚠️ `ai-driven-consistency-sysml-diagrams` 被误判为检查侧，⭐ 实际**两问全败** —— 全文无需求条目（`requirement` 仅 3 次且全在 related work / future work / 参考文献），任务是 UCD↔BD 两图互检；且三案例评测检的**每一张图都是它自己用 TTool-AI 生成的**。⛔ **连带后果**：`k ≥ 3 → A 档` 那条分支在正确计数下**不可达**。⚠️ **加重情节**：同一条「生成后自评不算」的判据踢掉了 `chatgpt-uml-assessment` 却对它网开一面 —— ⛔ **判定标准的选择性执行本身就是学术可靠性问题**。逐条证据见 [pool_audit.md](./pool_audit.md) §3。

⭐ **`CONTINGENCY_L1.md` §0.1.1 的 N-3 已于 2026-08-12 补上默认值**：⭐ 邻域**单独计数、不并入界内 $k$**，档位按 $k_{\text{界内}}$ 判；⛔ 但邻域篇目必须逐篇进对照表 + 形状逐项对应者进 `paper_story.md` §14。⚠️ 该缺口是本轮实测暴露的 —— ⛔ 原先 §0.1.1 只给了 Q3-B / Q4-B 的邻域默认值。

### 3.2 ⭐ 两段式路线确凿存在且近年密集，⛔ 但「谁决定检查什么」几乎全是人写

| 篇目 | 链路 | ⭐ 谁决定检查什么 | 边界门 |
| :-- | :-- | :-- | :-- |
| Identifying and fixing ambiguities（SoSyM 23(6)） | NL → FORM-L → 仿真 | ⭐ 规则 + 人（**自陈不可全自动**） | 邻域 |
| Post-Hoc Formal Verification of Automotive Software（RE 2024） | 人工形式化成契约 → 演绎验证 | ⭐ **人写** | 邻域（代码） |
| Spacecraft Operational Designs（MODELS 2023 + SoSyM 24(6)） | 工程师写性质 → 模型检查 | ⭐ **人写** | ⭐ 界内 |
| `pat-agent` / `event-b-agent` / `cir-cvn` / `llm-aided-protocol` | NL → CSP# / Event-B / Petri / SAPIC+ → 检查 | LLM 自动 | ⛔ 多数界外 |
| **Completion of SysML state machines from GWT** | Gherkin 模式 → 需求方案知识库 → 对已有状态机三道检查后补全 | ⭐⭐ **预编的 pattern catalogue** | ⭐ 界内 |
| Dwyer 模式族 | 人从目录挑一条 + 填 placeholder → 模型检查 | ⭐ **人写**（目录只降书写成本） | 界内（LTL/CTL 部分） |

⭐ **7 例中 4 例人写、2 例 LLM 自由生成、1 例预编 catalogue。** ⛔ 本轮覆盖内**未见**「闭合谓词词表 + 对模型逐条机械求值」这一形状。

### 3.3 ⭐⭐ 一条最可能的差异化落点（⛔ 需层 2 确认）

`Completion of SysML state machines from GWT` 是本轮**唯一**「界内 + 需求逐条可追溯（且**把追溯关系物化成模型元素**）」的篇目。⚠️ 它对未能形式化的需求有三种策略：**pessimistic 跳过 / optimistic 部分生成 / default 填默认值**。⛔ 但**跳过项是否被显式登记成覆盖缺口，摘要说不清**。

⭐⭐ **若层 2 确认「跳过即静默」，这正是 `paper_story.md` §5.1「它让测不了的东西显式暴露」的差异化落点。** ⛔ 层 2 必须核这一点 —— 它是本轮最高价值的单条待核事实。

### ⚠️ 两条术语陷阱（⛔ 后续检索必须显式排除）

1. `consistency checking` 在 CSUR 综述里指**多视图模型之间**，⛔ 不是 model vs NL。
2. `conformance checking` 在过程挖掘里指**模型 vs 日志**。

---

## 4. Q3 · ⛔ 0 条四门全中；⭐ 三种「不可换算」各自独立

⭐ 完整的检索矩阵与 14+ 条逐条筛除见各路交付；此处记结论。

### 4.1 ⭐⭐ 三种不可换算 —— ⛔ 它们是独立原因，不是同一条的三种说法

| 不可换算 | 实例 | 为什么不能弥补 |
| :-- | :-- | :-- |
| ⛔ **precision 不能反推 recall** | SoSyM LLM 通道（92% 的分母是**检出数**）· LASHED（逐字自陈 `because the real number of bugs is unknown, it is not possible to compute a proper Recall`） | ⛔ 缺 FN 项，⚠️ 分母是不同集合 |
| ⛔ **元素召回不是缺陷召回** | 生成侧的组件级 P/R（states F1 0.90 / guards 0.23 / actions 0.00） | ⚠️ 分子分母都是**模型元素**；⭐ 一个能复现 90% 状态的生成器，对「这个模型里有哪些错」**一个字都没说** |
| ⛔ **相对差不是绝对覆盖** | 人工检视一系的「CBR 比 UCDR 多检出 15.6% seeded defects」 | ⛔ 两技术之比，⚠️ 不是任一技术的绝对覆盖率 |

⭐⭐ **LASHED 与 SoSyM §6.3 是同一困难在两个不同形式主义上的独立现身** —— ⭐ 说明「缺分母」是这一任务族的**结构性状况**，⛔ 不是某一篇的疏漏。

### 4.2 ⭐ 最强的机械负结果（⛔ 但已被正确设界）

**ICSE / ESEC-FSE / ASE 三族 2022–2025 全卷 TOC 机械扫，共 2748 条题录**（ICSE 主会 896 · ASE 卷 1096 · FSE 主会 393 · PACMSE v1 121 · PACMSE v2 242）：

| 正则 | 命中 |
| :-- | ---: |
| `state machine\|statechart\|state-chart\|\bFSM\b\|\bEFSM\b\|state model\|behaviou?ral model` | ⛔ **0 / 2748** |
| `\bOCL\b\|SCXML\|design by contract\|well-formed\|\bJML\b` | 2 / 2748 |
| `conformance` | 0 / 2748 |
| `\breview\b\|inspection\|walkthrough` | 36 / 2748（⛔ **全部是 code review**） |
| `(LLM\|large language model\|GPT\|ChatGPT)` | 343 / 2748（⚠️ 与「设计/模型制品」求交后仅 **15**） |

⭐ **本方抽验复现**：ICSE 2025 主会实测 **246 条题录**（与报数一致）· 状态机命中 **0** · UML/SysML/MDE **1** · LLM **58** · review/inspection **0**。⭐ 方法可复现。

⚠️⚠️ **但这句话只对主会成立，⛔ 不对 ICSE 卫星卷成立。** ⭐ ICSE 的 NIER / SEIP / SEET / Companion 在 DBLP 是**独立卷**，本轮只扫了主会卷。⛔ 实证后果：ICSE'23 NIER 的 *Anti-Patterns (Smells) in Temporal Specifications* **不在**那 896 条里，是靠关键词检索才捞到的。

⚠️ **另一条工具性零，⛔ 不得当证据**：一次检索用了无效的 DBLP venue key `venue:FSE:`（正确是 `venue:SIGSOFT FSE:`），⛔ 其返回的 0 是**工具性零**而非事实性零。⭐ 已用正确 key 重跑。

### 4.3 ⭐ 用途声明

⛔ 本矩阵**不**用于主张空集、**不**用于主张首创、**不**用于论证 `60.4%` 足够好。⭐ 它回答一个具体质询：「**你们为什么不和已有工作比，而要自己造一个基线**」（X1，#179 §4B）。⭐⭐ **而回答它的是逐条筛除记录，⛔ 不是矩阵里那些 0** —— ⭐ 14+ 条候选各自缺哪一条门、那一条为什么不能换算，才是答案。

---

## 5. Q4 · ⭐ 界内闭合词表 $k = 0$，⛔ 但落 B 档

### 5.1 落档理由（§0.1.4 第 3 条要求逐问写明）

> **Q4 落 B 档，因为 C 档情况栏的第二个条件（「界内连模式目录都撑不起这个形状」）未被满足**，且 C 档判据要求的「说清 Dwyer 一系为什么不算」是说得清的 —— ⭐ **它算模式目录，只是「选模式」这个动作没有交给自动化。**

⚠️ ⛔ **这里曾出过一次错，且是我方的错**：给执行者的作业书写「$k = 0$ → C 档」，⛔ 丢掉了情况栏的那个「**且**」。⭐ 执行者**拒绝照做并回原文举证** —— 根 [CLAUDE.md](../../../../CLAUDE.md) §3.8 反向生效。

### 5.2 界内实况

| 类 | 篇数 | 2022+ | 计为满 3 篇？ |
| :-- | ---: | ---: | :-- |
| (i) 性质规约模式目录（Dwyer'98/'99 · PROPEL'02 · Prospec'03 · Autili TSE'15 · Menghi TSE'21） | 6 | **0** | ⛔ **否** —— 按 §4.2 #1 标注「仅 6 篇支撑（其中 2022+ 计 0 篇）」 |
| (ii) 标准化可执行语义 / 静态约束（SCXML · PSSM · OCL-USE · EVL · CSUR'23 综述） | 5 | 2 | ✅ 是 |

⭐⭐ **两个模式目录都自陈不闭合**：Menghi TSE'21 明写 pattern system **not intended to be exhaustive or static**；ICSE'23 NIER 明写 **preliminary catalog**，且自陈「几乎没有关于时序规约质量属性的既有定义」。⭐ 唯一自称闭合的是 **EARS 的 5 个模板**，⛔ 但它作用于**需求文本**而非模型。

⭐ **(i) 类 2022+ 为零，本身是一条对 story 有用的观察**：⚠️ 界内模式目录这条线的近年后继**全部外流** —— 要么外流到界外（UPPAAL 模式目录，IST 2022，TCTL + timed observer automata），要么外流到邻域（RTL/SVA、代码契约）。⛔ 这条只能进 Related Work + 覆盖范围声明，⛔ 不得进 Motivation（§0.1.7）。

### 5.3 ⭐⭐ 邻域：应答「这不就是把 SVA 那套搬到状态机上吗」的弹药

⛔ 按 N-1 默认值，以下**只用于 `paper_story.md` §14 一行**。

| 工作 | 制品 | 形状哪里像 | ⛔ 哪里不像 |
| :-- | :-- | :-- | :-- |
| ⭐⭐ **Zrelli 等 JSS 2026**（DOI [`10.1016/j.jss.2026.112941`](https://doi.org/10.1016/j.jss.2026.112941)） | 需求文本 → CTL | ⭐⭐ **三样全中**：闭合集合（**11 个预定义模式**作分类标签）+ **选类交给模型**（BERT 分类器）+ LLM 生成 | 制品非 $M$；产出是**待检查的性质公式**，⛔ 不是在已有模型上求值的断言；⚠️ 分类器**必然输出一个标签** → **疑似静默近似**而非显式记缺口 |
| ⭐ **Daikon**（TSE 2001） | 源代码 + 执行迹 | ⭐ 固定模板集 + 全自动实例化 | ⛔ **穷举全模板，不做「选」**；⭐⭐ **grammar 之外不报也不记缺口** —— 正是我们「让测不了的东西显式暴露」的**反面参照** |
| **AutoSVA**（DAC 2021）· AssertLLM（ASPDAC'25）· Spec2Assertion · AssertionForge · SpecAlign · ProofLoop | RTL / spec | ⭐ 形式化反馈回路与我们的修订循环同构 | 全部 RTL；⛔ 无闭合谓词集；⚠️ SpecAlign 自陈「形式反馈可被套利：**可证明但语义无效**的断言」 |
| ⭐ **SpecGen**（arXiv 2401.08807） | Java 源代码 | LLM + 验证器反馈 + 变异修复 | ⭐⭐ **摘要明确把「predefined templates or grammar」当作要摆脱的局限** |
| ⭐ **Are We SOLID Yet?**（ASE 2025，DOI [`10.1109/ASE63991.2025.00350`](https://doi.org/10.1109/ASE63991.2025.00350)） | 源代码 | ⭐ **5 条原则的闭合集合 + 240 条人工核验样本**的 benchmark + LLM 在已有制品上找违规 | 制品是代码；⭐ 但它的**分母做法可借鉴** |

⭐⭐ **一条对 story 直接有用的方向性事实**：⛔ **邻域主流方向与我们相反** —— SpecGen 明文把预定义模板当作局限、往**表达力**走；⭐ 我们反向用**受限表达力换可判定性**。⛔ 这只是方向陈述，⛔ 不得写成孰优孰劣（无对照实验）。⭐ 这是 `paper_story.md` §10 轴 5 那条方向性断言的**现成文献托底**。

### 5.4 ⛔ 一条必须上报、不由 L1 自裁的升级项

**Zrelli 等 JSS 2026 是本轮唯一「闭合集合 + 选类交给模型」同时成立的工作。** ⭐ 它按 §0.1.1 判为**邻域**，⛔ 但正因如此把 B 档子情况的触发条件顶到了边界线上：

- 维持邻域判定 → 界内 $k = 0$ → 常规 B 档，C-② 强度停在「与既有工作不同」，差异化落点是「**选谓词的自动化**」。
- 若 R1 改判计入对照 → 触发 B 档「1–2 篇闭合词表」子情况 → ⛔ **对 contribution 的后果按 A 档执行**：C-② 直接降档。

⭐ **建议的差异化落点是第三点（覆盖缺口的显式化）**：⚠️ 本轮三问里，界内与邻域**都没有**一篇把「表达不了的义务」显式记成缺口 —— Daikon 是 grammar 之外不报，Zrelli 的分类器必然出标签因而疑似静默近似，PSPWizard 的「省略映射」是最接近的先例但那是**工具能力表**而非**逐条义务的缺口账**。⛔ 三条均为摘要级推断，层 2 必须逐篇核。

---

## 6. Q5 · ⭐ A 档，⚠️ 但没有一篇的制品是状态机

### 6.1 计数（按 §5-A 判据三问逐篇过）

| 篇目 | ① 模型是别人给的 | ② 输出是缺陷列表 | ③ 评测分母说得清 | 计 |
| :-- | :-: | :-: | :-- | :-: |
| **MCeT**（MODELS 2025） | ✅ | ✅ | ✅ 135 条人工 issue / 2 名作者判定 / $\kappa = 0.79$ | ⭐ 1 |
| **Reinpold 等**（arXiv [`2411.11582`](https://arxiv.org/abs/2411.11582)） | ✅ | ✅ 逐需求两轴离散标签 | ✅ 27 配对 / **OCL 真值** / 受控植入 | ⭐ 1 |
| **Wang 等 · GPT 评 UML**（JSS，arXiv [`2412.17200`](https://arxiv.org/abs/2412.17200)） | ✅ 学生手绘 | ✅ JSON 扣分理由 | ✅ 40 份报告 × 11 准则 / 人类专家参照 | ⭐ 1（⚠️ 摘要级） |
| **SoSyM 2026 Sultan 等** | ⚠️ 指标表那批是自生成 | ✅ | ⛔ **说不清**（自陈不计 FN） | ⛔ 0 |

⭐⭐ **「制品是已有状态机（$M$）」的评审侧 = 0 篇满足全部三问。** ⛔ 唯一覆盖 SMD 的是 SoSyM 那篇，⚠️ 而它 ①③ 都不过 —— ⭐ 详见 [adjudication_sosym.md](./adjudication_sosym.md)。

### 6.2 ⭐ 外部量化背书（⛔ 不是我方的空格）

**LLM4MDE 系统映射**（Zhang 等，EMSE 2026，DOI [`10.1007/s10664-026-10921-4`](https://doi.org/10.1007/s10664-026-10921-4)，86 篇，2022–2026 初，⭐ 本地已取全文 49 页）：Model Generation **62 篇 (72%)** · **Model Validation 仅 11 篇 (12.8%)** · Model Completion/Repair 12 · Model Transformation 10 · Code Generation 5 · Model Migration 3 · DSL Engineering 2 · Metamodeling 1。

⛔⛔ **但同一篇综述点名的空白清单里没有 Model Validation。** ⭐ 它逐字点的是 metamodeling、model migration、DSL engineering，以及 multi-level / multi-view modeling。⚠️ **因此「某综述把设计模型 LLM 质量保障列为未来方向」这条迹象未能核实，⛔ 不得当事实用。**

⭐ 该综述另有一句**可用**：*"the industry-specific share of Model Validation (36.4%) … does not align with the expectation given its direct relevance to quality assurance"* —— ⚠️ 那是**产业参与度**的自陈，⛔ 不是「该方向为空」。

### 6.3 ⭐ 三条可用的他人自陈局限（§0.1.7 第 2 条的唯一合法路径）

⛔ 我方检索出来的空格**进不了 Motivation**；⭐ 只有他人自陈可以。本轮找到三条（⚠️ 均需层 2 取全文逐字核）：

1. **IET Software 2025**（DOI [`10.1049/sfw2/6714956`](https://doi.org/10.1049/sfw2/6714956)）自陈：即便有 LLM 辅助，活动图与状态机模型之间、以及基本/备选/异常流之间的不一致仍然存在，**因为 LLM 无法跨模型层级做一致性检查**。⭐ **这条直接说的就是状态机。**
2. **SoSyM 2026 Sultan 等**自陈（⭐ 已全文核）：*"even the most advanced LLMs available at the time of evaluation were unable to identify logical dependencies along simple paths involving only two consecutive edges"*。
3. **MCeT** 自陈（⭐ 已全文核）：直接提问 LLM 比对图与需求，只能找到经验工程师所找 issue 的**不足 35%**。

### 6.4 ⭐ 生成侧自报的失败类型（⛔ 不计入评审侧，⭐ 可作缺陷类目的外部佐证）

`llms_emp` 的幻觉四分类（**格式 / 语法 / 语义 / 需求不一致**）· `designing-fsm-...-gpt4` 的 **missing transition / output fault** · `Structure-/Event-Driven SMF` 的组件级 F1（states 0.90 / transitions 0.75 / **guards 0.23 / actions 0.00**）· `Evaluating LLM-Generated FSMs` 的 **process confusion / unhappy-path 覆盖不足 / 自迁移漏检**。

⛔ **这些数值不得进 Q3** —— 分母不同质。

---

## 7. ⛔ 交给层 2 的待核清单（按价值排序）

| # | 待核 | 为什么它最要紧 |
| :-- | :-- | :-- |
| **1** | ⭐⭐ `Completion of SysML state machines from GWT` 的**跳过项是否被显式登记成覆盖缺口** | ⭐ 若「跳过即静默」，这就是 §5.1「让测不了的东西显式暴露」的差异化落点 |
| **2** | `Scaling Assessment of Student Models with LLMs`（SEET@ICSE 2026，DOI [`10.1145/3786580.3786985`](https://doi.org/10.1145/3786580.3786985)）**是否含状态机图** | ⭐ 唯一一条 ②可能为真的 2022+ 候选；若含，它从邻域升为界内 |
| **3** | MCeT 的分母 **135** 在正文或附录中是否印出 | ⚠️ 本轮三式反推一致（134.9/135.1/135.0），⛔ 但正文 grep `\b135\b` 零命中 |
| **4** | `baselines/*/DESC.md` 里那批数字（69/6/92%/87% · 85%/77% · 100%/0%/40%） | ⛔ **全部出自我方转述，不是原文核验过的** |
| **5** | `Automata Models for Effective Bug Pattern Description`（MODELS 2025，DOI [`10.1109/MODELS67397.2025.00017`](https://doi.org/10.1109/MODELS67397.2025.00017)） | ⭐ 与 C-② 的「闭合词表」形状最接近的界内一篇 |
| **6** | LLM4MDE 映射的 **11 篇 Model Validation 具名清单** | ⭐ 把 Q5 计数从 3 提高或证否的最短路径 |
| **7** | `Unified verification and monitoring of executable UML specifications`（SoSyM 2021） | ⭐ 把**性质本身写成 UML 状态机**（观察者自动机），界内、形状最相邻 |

---

## 8. ⛔ 覆盖范围声明（⚠️ 所有「未见 X」的合法前提）

**venue 族**：ICSE / ESEC-FSE / ASE（2748 条题录全卷 TOC 机械扫，2022–2025 主会）· MODELS 2023/2024/2025 主会（83 篇全量 TOC）· SoSyM vol 23/24/25（2024–2026 全量逐期）· RE 2022–2025 + REJ vol 29/30（33 篇全量）· ECMFA 2023/2024/2025（38 篇全量）· CAV/FM/FMSD（⚠️ **仅覆盖一个关键词簇**）· arXiv。

**年份窗**：2022–2026 为主窗；≤2021 为次窗（仅为人工检视类量级背景而查）。

**入口**：DBLP publication search API（含 `venue:` 过滤）· DBLP 会议卷 TOC 全量抓取后本地 grep · JOT contents · conf.researchr · WebSearch · 三次一手 PDF 取件。

### ⛔ 明确没跑的（⚠️ 「未见」的边界就在这里）

1. ⛔ **ACM DL / IEEE Xplore / Scopus / WoS 的字段化或全文检索** —— 全轮未做。⚠️ **这是本轮最大的假阴性来源**：凡「标题不含关键词但正文做了该事」的论文，本轮**系统性看不见**。
2. ⛔ **ICSE 卫星卷**（NIER / SEIP / SEET / Companion）与 **FSE workshop / Industry track** —— 未扫。⚠️ 已有实证后果（见 §4.2）。
3. ⛔ **MODELS 2022 主会** TOC 已下载未扫；**MODELS Companion / Workshops 2022–2025 全部**未扫（⚠️ 本族最大未扫区块）；**STAF 系 LLM4MDE 2024 / LLM4SE 2025–2026 工作坊**一篇未扫。
4. ⛔ **REFSQ 2022–2026**（CCF B，本族天然邻居）与 **REW 2022–2025** —— 完全未跑。
5. ⛔ **前向引用追踪**（MCeT · SoSyM · Dwyer'99 · mCUTE · Nejati'19 的 citing papers）—— 未做。⭐ 这是补 Q1 ⑤ 与 Q3 的下一个最高收益动作。
6. ⛔ **ECMFA 2022（JOT 21(3)）与 2026（JOT 25(3)）** · **SoSyM vol 21–22** · **MODELSWARD** —— 未扫。
7. ⛔ **Simulink / Stateflow 侧的 Model Advisor 规则集与 Design Verifier 性质模板** —— ⚠️ 一片极可能存在闭合规则集的工业侧材料，完全未查。
8. ⛔ **Runtime verification 规约语言族**（Salt / LOLA / TeSSLa / MOP）—— 其 pattern 层可能有闭合词表形态。
9. ⛔ **非英文文献**（CNKI / 万方）与工业白皮书。
10. ⚠️ **两串 DBLP 关键词查询因 HTTP 429 未取回**（`requirements traceability state machine` · `statechart consistency requirements`）—— ⛔ 计为未跑，不是零命中。

### ⚠️ 一条事实纠正

⭐ DBLP `conf/ecmdafa` 收录**止于 ECMFA 2018** —— ⛔ 那是 **DBLP 的收录断层，不是会议停办**。ECMFA 自 2019 起在 *Journal of Object Technology* 出版，2026 年将办第 22 届 @ STAF。⚠️ 本条为执行者报告，⛔ 本方**未独立复核**。
