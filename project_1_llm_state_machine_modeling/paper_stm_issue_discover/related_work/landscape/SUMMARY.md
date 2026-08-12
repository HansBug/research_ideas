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

### 1.1 ⭐⭐ 【用户明确决策 2026-08-13】MCeT = **邻域标杆**，⛔ **不作对照系**

〔用户明确决策〕逐字：**「MCeT 这个没有对照价值啊，你说这玩意是顺序图，我们是状态机，本身都不是一类制品，没法直接碰的……MCeT 顶多算是邻域标杆这样的，不过还是很有价值的，对 X1 那边的可能是个参考。」**

| 项 | 裁定 | ⛔ 后续约束 |
| :-- | :-- | :-- |
| 作 `hit@1` 对照系 / baseline | ⛔ **不作** | ⛔ 不得把它的 `34.1%` / `68.1%` 与本文任何数并列或换算 |
| 定位 | ⭐ **邻域标杆**（neighborhood landmark） | ⭐ Related Work 主动引、主动划界；⛔ 不进对照表 |
| 对 X1 的参考价值 | ⭐ **保留**（见 §4.2.1） | ⭐ 仅作**设计参考**，⛔ 不作可比数字 |

⭐ **裁定理由是分类学层面的**：顺序图是**交互轨迹的偏序**，状态机是**状态 / 迁移 / 守卫的结构** —— ⛔ 两者的缺陷分类学不共享。⭐⭐ 这把门② 从「一个可被其余三门补偿的技术性缺项」升格为**不可比**。

⛔⛔ **这条裁定没有处理、⚠️ 也不得顺势并掉的一件事**：⭐ 「不作对照系」解决的是**能不能拿它的数字比**；⛔ 它**不解决**「它那句零限定的 first 会不会被审稿人引来打我们」—— ⭐ 那是**写作风险**。

⭐⭐ **写作风险的处置是主动划界**：在 Related Work 里显著地引它，**明说它做顺序图、我们做状态机**。⛔⛔ **但不要用「制品不同」当论据去挡那句 first** —— ⚠️ 下面「⛔ 「制品不同」这条防线被 MCeT 自己的文本掏空」一节已证明：⭐ 它自陈技术可轻易适配任何建模语言，⛔ 这条挡板一推就倒。⭐ 差异化必须落在 §5 那三条（**缺口挂在哪一格 · 裁决在被判对象上求值 · 可重放**）上。

### ⛔⛔ 而且它自己声称了一个「首个」—— ⚠️ 说了**四遍**，限定词逐级脱落

⛔⛔ **本节初版有一条错误的「纠正」，已于 2026-08-12 删除并改写。** ⚠️ 初版称核验者的引文「the first approach to perform fully automated evaluation of a behavioral model against its requirements」是**引文失真**、「原文不是这个措辞」—— ⛔ **原文就是这个措辞**，逐字在 §IX Conclusions 第 1044–1047 行。⭐ 核验者引的是 §IX，⛔ 而我只查了 §I 就宣布它失真。

⭐⭐ **这次失误的形态值得记下**：⛔ 我核的是「这句引文**和我正在看的那一段**对不对得上」，⭐ 而正确的核法是「这句引文**在全文任何地方**存不存在」。⚠️ **一篇论文可以把同一个主张说四遍、每遍限定词都不同** —— ⛔ 只核一处就宣布失真，等于用局部否定全局。

#### 四个版本（⛔ 限定词逐级脱落）

| 位置 | 逐字原文 | 限定词 |
| :-- | :-- | :-- |
| **Abstract**（L27–29） | `we propose MCeT, the first fully automated tool to evaluate the correctness of a behavioral model, sequence diagrams in particular, against its corresponding requirements text` | ⛔ 无 LLM-based · ⛔ 无 free-style · ⚠️ 有软化语 "sequence diagrams in particular" |
| **§I**（L129–132） | `To the best of our knowledge, MCeT is the first LLM-based approach to evaluate a behavioral diagram model against free-style requirements texts` | ⭐ **四个**：LLM-based · behavioral **diagram** model · **free-style** · issue 解释用自然语言 |
| **§I Contributions (1)**（L137–139） | `We propose the first automated behavioral model evaluation approach to evaluate a behavioral diagram model against its free-style requirements textual description` | ⛔ 丢 LLM-based；留 diagram + free-style |
| ⛔⛔ **§IX Conclusions**（L1044–1047） | `To the best of our knowledge, MCeT is the first approach to perform fully automated evaluation of a behavioral model against its requirements.` | ⛔⛔ **一个都没有** |

⛔⛔ **按 §IX 那一版读，这个 first 字面覆盖任何「自动评估行为模型 vs 需求」的工作，⛔ 包括我们** —— ⚠️ 而 Conclusion 恰是审稿人与后续引用者最常摘的位置。⭐ 初版据 §I 排的那张「三条限定给我们留了空间」的表因此**不是有效的空间分析**：它分析的是四个版本里限定**最多**的一版。

#### ⛔ 「制品不同」这条防线被 MCeT 自己的文本掏空

| 逐字原文 | 位置 | 后果 |
| :-- | :-- | :-- |
| `In our current approach, we process sequence diagrams in PlantUML, however, the technique can be easily adapted to process any other modeling language.` | L330–332 | ⛔ **作者自陈技术可轻易适配任何建模语言** |
| `Behavioral diagrams, e.g., activity diagrams, sequence …`（其定义含 state changes 与 responses to external events） | L56–58 | ⚠️ **状态机落在它自己的 behavioral diagram 定义之内** |
| `we aim to expand our study into other types of behavioral models as part of our future work` | L955–957 | ⚠️ ⛔ **我们做的事，被这篇 MODELS 2025 在正文里点名为 future work** |

#### ⭐ 唯一真实的挡板，⛔ 但它是对冲不是收回

⭐ §VII External Validity（L955–957）自陈 `our approach may not generalize to other types of behavioral models` —— ⚠️ 那是对**实验外部效度**的对冲，⛔ **不是对首创主张的收回**，⚠️ 且它与 L332 的「易于适配」在同一篇里互相矛盾。⛔ 引用它等于把两句话一起端上桌。

⭐⭐ **结论比初版更硬**：⛔ 在本轮覆盖范围内，C-① 的新颖性档位**不应高于「与既有工作不同」** —— ⚠️ 而按 §IX 那一版，**连这个上限都可能偏高**。⛔ L1 不裁定档位（§0.1.2），⭐ 这条事实原样交 R1。

⭐ 三处**真实**的差别（⛔ 按 §2 前置纪律 ①，后两项只进对照表列、⛔ 不进计数）：

| 差别 | MCeT | 本文 |
| :-- | :-- | :-- |
| **制品** | UML 序列图 | 状态机（$M = (S,E,V,Tr,A)$） |
| **判定是否可机械求值** | ⚠️ ⛔ **初版写「issue 是散文、无字段结构」，那不准，已改。** ⭐ 实测其 `prompts/*.json` 制品：**裁决是 LLM 自报的 Yes/No 离散标签**，带 JSON 信封、Correctness/Completeness 类型轴、requirement-atom / diagram-atom 定位（`"Correct?" : "Yes/No answer"` / `"Complete?" : "Yes/No answer"`）。⛔ **不要再写「无字段结构」—— 制品在手的审稿人一查就翻。** ⭐ 真正的差别是：**裁决由 LLM 自己吐出，⛔ 不是在制品上按可判定过程求值出来的** | ⭐ 断言在制品上求值 |
| **可否重放** | ⛔ 结论不变，⭐ 现有一手依据：prompts / 源码 / 输入 / 人工真值（散文态）**已公开**，⛔ **但「135 条离散 issue 的切分」与「两名作者对每条 issue 的 Yes/No 判定」都没公开** → ⭐ 第三方可以**重跑** MCeT，⛔ **不能独立复算任何一条 issue 的真伪** | ⭐ 断言可在制品上独立复算 |

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
| **Completion of SysML state machines from GWT requirements**（SoSyM 23(6)，DOI [`10.1007/s10270-024-01228-3`](https://doi.org/10.1007/s10270-024-01228-3)） | ✅（**已有的部分 SysML 状态机**） | ⛔ **否（只有正面锚）** | ⛔ **不计入**（⭐ 层 2 全文已裁定） | ⭐ 状态机 → **界内** |
| `inference-time-intervention` / `ai-driven-consistency-sysml` | ✅ | ✅ / ⚠️ | 邻域 | Capella/SysML 架构图 · UCD/BD |

$$k_{\text{界内}} = 0, \qquad k_{\text{邻域}} = 2$$

⭐ **那个「+1 待裁定」已由层 2 全文精读结掉**：⛔ GWT 那篇的 `«satisfy»` 关系**只从已生成的模型片段指向需求**（§4），⚠️ **失败的需求没有任何模型元素，因此没有链接、也没有任何反向记号** —— ⭐ 追溯图是一份**成功清单**，⛔ 不是覆盖账。而 §8 Listing 5 行 5–7 的三道检查是**生成闸门**（`Only if the validation is successful it is possible to move on to the translation phase`），⛔ 不是输出。⭐⭐ **它是「带静默闸门的生成器」，⛔ 不是检查侧工作。**

⚠️ ⛔ **一个悬空的待裁定项会带着交付通过全部关口**（§0.1.1 自己点名的风险）；⭐ 现已结掉。

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

⭐⭐ **层 2 全文已确认「跳过即静默」，⛔ 三条独立证据同向**：

1. ⭐ **§8 那句是模态祈使，不是已实现的产出物**：`In any case, detected violations **should be signalled** to the System Analyst with proper warnings` —— ⛔ `should be` 是建议。⭐ 实测：全文 `warn` **仅 1 次**（就是这句）、`uncovered` / `not covered` **0 命中**；⭐ **该论文 §9** Tool Layer 的三个组件里**没有任何一个产出报告或清单**，`Validator` 的职责逐字是「Only if the validation is successful it is possible to move on to the translation phase」—— ⭐ 一个**布尔闸门**。
2. ⭐⭐ **该论文 §12 作者自陈本文没做这件事**（⭐ 最硬的一条）：`Even if this paper **does not explicitly address** these two features … the verification of completeness **could be addressed by** constructing some SysML model queries that retrieve "model anomalies" as isolated states, transitions that are not mapped on any requirements or **requirements that are not satisfied by any model element**` —— ⭐ 「未被任何模型元素满足的需求」被作者**逐字点名**，⛔ 但归入将来式，且前置一句明写「this paper does not explicitly address」。
3. ⚠️ **两个真实跳过实例，落盘处只有正文散文**：Appendix A.3 的 `REQ−4.1 is **only partially matched**` 与 `The translation of all the detected requirement patterns **but the REQ−2.1**`。⛔⛔ **REQ−2.1 更严重**：它不是被跳过，⚠️ 是**被翻译后产生了错误模型而无人察觉**（两个 guard 不互斥导致非确定），⭐ 靠**外部模型检查器 + 人工纠正**兜底 —— ⛔ 本方法既不检出也不登记。

⭐⭐ **裁定：`paper_story.md` §5.1「它让测不了的东西显式暴露」是站得住的差异化落点。** ⭐ 且 §12 那句是**作者自陈** —— ⭐⭐ 按 §0.1.7 第 2 条，**这是少数几条能合法进 Motivation 的材料**（⛔ 我方检索出来的空格不能）。

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

⭐ **LASHED 与 SoSyM §6.3 是同一困难在两个不同形式主义上的独立现身。**

⚠️⚠️ ⛔ **但「说明这是任务族的**结构性状况**」这句已于 2026-08-12 降级** —— ⭐ 按 §4.2 #1：**仅 2 篇支撑**。⛔ 从 2 例推一个关于「任务族」的全称性质是全称化。⭐ **合法表述**：「⭐ 至少两篇工作（不同形式主义）**各自独立地**报告了同一困难」，⛔ 不写「这是任务族的结构性状况」。

⚠️ **同表另两行同样只有单例支撑**，⛔ 亦按 §4.2 #1 标注：「元素召回不是缺陷召回」**仅 1 篇**（生成侧组件级 P/R）· 「相对差不是绝对覆盖」**仅 1 篇**（CBR vs UCDR 的 15.6%）。⭐ 三条**类型**各自成立，⛔ 但**普遍性**都没有分母支撑。

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

⛔⛔ **但这张表有三条口径边界，⚠️ 初版一条都没声明**（2026-08-12 由 C3 补）：

1. ⛔⛔ **它是纯标题级正则（`title-only`）。** ⚠️ 读者会把 `conformance 0/2748` 读成**三族近年没有 conformance 工作**。⭐ 反证：MODELS 2023 主会标题里**就有** *An Experimental Evaluation of Conformance Testing Techniques in Active Automata Learning* —— ⭐ **那个 0 是「该族标题」的 0**。⚠️ 同理 ICSE'23 NIER 的 *Anti-Patterns in Temporal Specifications* 标题不含 STM 词，⛔ 标题级扫描对那条线**不灵**。
2. ⛔⛔ **2748 是三个成分不同质的数相加**：**ICSE 剔了卫星卷**（896 = 纯主会）、**ASE 含卫星卷**（1096 含 industry / tool demo / NIER）。⛔ 两者按不同口径进同一个分母 —— ⭐ 这正是「**比率只能跨同类分母比**」：⚠️ **成分差异在合计数上完全看不见**。
3. ⚠️ **PACMSE v1 121 / v2 242 与「FSE 主会 393」是两段不同年份的口径拼接**（393 = ESEC/FSE 2022+2023；FSE 2024/2025 主会改发 PACMSE），⛔ 不是并列关系。
4. ⛔ **「343 与『设计/模型制品』求交后仅 15」的求交词表没给** —— ⚠️ 这与 `pool_audit.md` §1 自己刚立的规矩逐字冲突：⭐ **同一份交付里，边界门落了脚本，这个求交没落。**

⭐ **完整台账见 [search_ledger.md](./search_ledger.md)** —— ⛔ 该文件是 Q3-B 档的**硬义务**，⚠️ 初版整体缺失，由 C3 发现后补。

⚠️⚠️ **但这句话只对主会成立，⛔ 不对 ICSE 卫星卷成立。** ⭐ ICSE 的 NIER / SEIP / SEET / Companion 在 DBLP 是**独立卷**，本轮只扫了主会卷。⛔ 实证后果：ICSE'23 NIER 的 *Anti-Patterns (Smells) in Temporal Specifications* **不在**那 896 条里，是靠关键词检索才捞到的。

⚠️ **另一条工具性零，⛔ 不得当证据**：一次检索用了无效的 DBLP venue key `venue:FSE:`（正确是 `venue:SIGSOFT FSE:`），⛔ 其返回的 0 是**工具性零**而非事实性零。⭐ 已用正确 key 重跑。

### 4.2b ⛔⛔ Q3 漏掉了一个候选，⚠️ 而仓库另一份文件称它「唯一可用的外部对照」

⛔⛔ **这是一处仓库内自相矛盾，由 C2 反驳发现。** [`discover_matrix/docs/protocol/ground_truth_limitations.md`](../../discover_matrix/docs/protocol/ground_truth_limitations.md) 逐字写着：

> ```
> 原论文（Wang et al. 2025, Internetware，DOI 10.1145/3755881.3755926）的公开 workbook
> `Experiment Results.xlsx` / sheet `STM Results` 对 60 个生成结果逐 case 记录三类问题，
> 各带 `Resolved` 标记。它是唯一可用的外部对照，因为它的判定方式与我们不同：
> 它对着作者重建的参考模型算 grammar-point F1，而我们仅凭 NL 建立正向命…
> ```

⛔ **而 L1 的全部交付物里，`Internetware` 出现 0 次**（`grep -c` 于 `SUMMARY.md` / `pool_audit.md` / `CONTINGENCY_L1.md` / `story_suggestions.md` / `adjudication_sosym.md` 全为 0）。⚠️ **同一批 54 pair 所依据的那 60 个模型，其原论文的人工问题清单，在 Q3 的 14+ 条逐条筛除里一次都没出现。**

⚠️ 按 `CONTINGENCY_L1.md` §0.1.5 第 1 条，**任何一个「0 篇」都必须附可复现筛除记录** —— ⛔ 这一条候选**连筛都没筛**。

⭐ **它大概率过不了门①**（它对着作者重建的参考模型算 grammar-point F1，属生成后自评），⛔ **但那是判据，不是豁免**：⚠️ 「它不合格」必须**写出来**，⛔ 不能靠没提到。⭐ 已列为层 2 待核第 1 项。

⚠️⚠️ **两份仓库文件对同一对象给出相反定位** —— 一份称「唯一可用的外部对照」，另一份的筛除记录里零出现。⛔ 审稿人只需要引其中一份。⭐ **必须收口**：要么在 Q3 里正式筛除它并写明理由，要么更正 `ground_truth_limitations.md` 的措辞。

### 4.2c ⚠️ 「为什么必须自建」这个答案，⛔ 只答了一半

⛔ C2 反驳指出：Q3 的筛除记录回答的是「**文献里有没有可换算的数字**」，⚠️ 而 X1 质询问的是「**你们能不能跑一个外部对照**」。⭐ **两者不是同一个问题**，⛔ 而 §4.1 的三条不可换算**全部只适用于搬运数字，一条都不适用于运行别人的方法**。

⚠️ 三条加重情节：

1. ⭐ **最近的候选可运行**：MCeT 四门里只失守门②，⛔ 而门② 是**我们自己划的**形式主义边界。它的实现、prompt、评测数据集全部公开（L140–142），⛔ 且作者自陈技术可轻易适配任何建模语言（L332）。⚠️ 所以「不能比」目前的真实内容是「**没试过**」，⛔ 不是「不可能」。
2. ⛔⛔ **X1 复刻的恰好是已知的弱臂**：MCeT 摘要 L33–35 逐字 `directly asking an LLM to compare a diagram to requirements finds less than 35% of issues that experienced engineers can find` —— ⚠️ **朴素直问就是 MCeT 的 holistic 臂**，它已被量过（34.1% vs 组合臂 68.1%），⭐ 是两条臂里差的那条。
3. ⚠️ **三种不可换算是把双刃剑**：⭐ 它的有效结论是「外部数字不可搬进来」，⛔ **但它同时意味着我们的 60.4% 也不可被外部读懂**。

#### ⭐⭐ 2026-08-13 更新：用户已裁定其中两条

⭐ 按 §1.1 的裁定，上述三条加重情节的处置如下 —— ⛔ **注意只裁掉了两条半，第 1 条剩一半仍待答**：

| # | 处置 |
| :-- | :-- |
| **1** | ⭐ **裁掉一半**：「拿它的数字比」⛔ **已排除**（不同类制品）。⚠️ ⛔ **但「把 MCeT 适配到状态机上跑一遍」是另一件事** —— ⭐ 作者自陈可适配、实现公开，⛔ **这个不做的理由仍需一个明确答复**（⚠️ 候选答复：适配后它已不是 MCeT，而是我们替它设计的一个新方法，⛔ 那样的对照系其强弱由我们决定 → 稻草人风险反而更大）。⭐ 该半条上交 R1 |
| **2** | ⭐ **转为正面价值**，见 §4.2.1 —— ⛔ 「复刻弱臂」这个指控在**不作对照**的前提下不成立，⭐ 反而变成 X1 朴素臂的**先验与 prompt 参照** |
| **3** | ⭐ **保留为写作约束**：⛔ 「我们的 60.4% 不可被外部读懂」仍然成立，⭐ 故正文必须**自带口径说明**，⛔ 不得裸报数字 |

### 4.2.1 ⭐ MCeT 对 X1 的参考价值（⭐ 用户裁定明确保留）

⭐ **三条，⛔ 全是设计参考，⛔ 不是可比数字**：

1. ⭐⭐ **X1 的朴素臂 = MCeT 的 holistic 臂。** ⚠️ 「朴素直问在这个任务族上大约什么量级」**已被别人量过**（顺序图上 34.1%）。⛔ 不可与我方 `hit@1` 比，⭐ 但给 X1 一个**先验**：⚠️ 若 X1 朴素臂显著高于该量级，应回头查 prompt 是否无意泄漏。
2. ⭐ **它的 holistic prompt 公开** —— ⭐ X1 拟朴素臂措辞时可对照，⛔ **避免把朴素臂写弱（稻草人是 X1 的头号学术风险）**。⭐ 有据胜过凭空拟。
3. ⚠️ **它的 issue 判定靠两名作者人工 Yes/No（$\kappa = 0.79$）** —— ⭐ 印证 X1「全人工判定 hit」的必要性，⛔ 也预示工作量量级。

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

⭐⭐ **「2022+ = 0」这个数已于 2026-08-12 从「没找到」升级为「找到了三条、逐条因边界门出局」** —— ⭐ 后者是**强得多**的交付形态：

| 2022+ 模式目录 | 出局理由（⭐ 逐条核过） |
| :-- | :-- |
| **UPPAAL 模式目录**（IST 2022，DOI [`10.1016/j.infsof.2022.107100`](https://doi.org/10.1016/j.infsof.2022.107100)） | ⛔ **界外**：UPPAAL / TCTL / timed observer automata |
| ⭐⭐ **QUARTET**（Menghi 等，**TSE 49(4):2741–2760, 2023**，DOI [`10.1109/TSE.2022.3230059`](https://doi.org/10.1109/TSE.2022.3230059)） | ⛔ **界外**：目标逻辑 PRCTL，正文逐字 `interpreted over discrete-time Markov reward models … states labelled with probabilities and rewards`，算子含步界 $\phi_1 U^N_J \phi_2$，后端 PRISM —— ⭐ **概率 + 奖励 + 步界三样全中**。⭐ **全文 21 页已读** |
| **PSSM doActivity 模式**（TSE 50, 2024，DOI [`10.1109/TSE.2024.3422845`](https://doi.org/10.1109/TSE.2024.3422845)） | ⛔ **界外（部分可用）**：11 条模式内容**全在 doActivity 并发与正交区上**。⭐ **全文 17 页已读**。⚠️ 但它自陈用途逐字是 `patterns on a checklist to be used in model reviews or automated static analysis tools`，⭐ **是本轮最接近「闭合词表 + 逐条机械检查」的一例** |

⭐⭐ **QUARTET 同时给「近年后继外流」这条提供了一手证据**：正文逐字 `we extended our previous catalog of patterns and its DSL [35], [36], [37]`，⭐ **其中 [35] 正是 Menghi TSE'21** —— ⛔ 同一团队、同一目录的量化扩展，⭐ 而它落到了界外。⚠️ **但「全部」仍不可写**（另两条候选未核）。

⚠️ **三条目录全部自陈不闭合** —— ⭐ QUARTET 全文四处，例如 `patterns are (by definition) not meant to be exhaustive` · `the catalog can be extended over time`。⭐ 使「模式目录自陈不闭合」从**两例变三例**。

⭐ **「选模式」仍是人**：QUARTET 的自动化是 **DSL → PRCTL → PRISM 的翻译**，⛔ 不是「决定检查什么」 —— ⭐ 与 Dwyer 一系判定完全一致。
| (ii) 标准化可执行语义 / 静态约束（SCXML · PSSM · OCL-USE · EVL · CSUR'23 综述） | 5 | 2 | ✅ 是 |

⭐⭐ **两个模式目录都自陈不闭合**：Menghi TSE'21 明写 pattern system **not intended to be exhaustive or static**；ICSE'23 NIER 明写 **preliminary catalog**，且自陈「几乎没有关于时序规约质量属性的既有定义」。⭐ 唯一自称闭合的是 **EARS 的 5 个模板**，⛔ 但它作用于**需求文本**而非模型。

⚠️⚠️ **「(i) 类 2022+ 为零」与「近年后继全部外流」两条已于 2026-08-12 降级** —— ⛔ C3 覆盖 challenge 在 Dwyer 前向引用图（1674 篇被引，168 篇 2022+）里找到**至少 3 条未外流的 2022+ 后继候选**：

| 编号 | 篇目 | 为什么它冲击这条断言 |
| :-- | :-- | :-- |
| **N-01** | *Mission Specification Patterns for Mobile Robots: Providing Support for Quantitative Properties*，IEEE TSE 49（2023），DOI [`10.1109/TSE.2022.3230059`](https://doi.org/10.1109/TSE.2022.3230059) | ⭐⭐ **Menghi TSE'21 同一条线的 2022+ 后继**；⚠️ "quantitative" 有引入概率 / 实时的风险，⏳ **边界门待核** |
| **N-02** | *Specifying Temporal Properties in UML Using Patterns: A Tool-Supported Approach*，MODELS Companion（2023），DOI [`10.1109/MODELS-C59198.2023.00071`](https://doi.org/10.1109/MODELS-C59198.2023.00071) | ⭐⭐ **模式目录 + 工具支持，落在 UML 上、2022+** |
| **N-03** | *Towards A Catalogue of Requirement Patterns for Space Robotic Missions*，FMAS@iFM（2025），DOI [`10.4204/EPTCS.436.12`](https://doi.org/10.4204/EPTCS.436.12) | ⭐ 2025 年的需求模式目录；⚠️ 标题自带 "Towards"，⭐ 很可能又是一个自陈不闭合的 preliminary catalog |

⛔ **三条都还没读正文、边界门都没落到叶子**，⚠️ 所以**不主张原断言为假**。⭐ 但按 §4.2 #1，那句「**全部**」建立在 **2 例**分母上，⛔ **已站不住**。

⭐ **降级后的合法表述**：「**在本轮覆盖内所见的近年后继落在界外或邻域**（⚠️ **仅 2 例支撑**）」，⛔ 不写「全部外流」。⛔ 这条只能进 Related Work + 覆盖范围声明，⛔ 不得进 Motivation（§0.1.7）。

⚠️ **连带**：若 N-01/N-02/N-03 中任一条通过边界门，**(i) 类从「仅 6 篇支撑（2022+ 计 0）」变为满 3 篇** —— ⛔ **这不动 Q4 的档位**（A 档要求「≥3 篇界内**闭合词表交给自动化**」，仍是 0），⭐ 但**推翻这条外流断言**。

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

⚠️⚠️ **「唯一」已于 2026-08-12 降级为「≥2 篇」。** ⛔ C3 在 Dwyer 引用图里找到同形候选：*Translating Requirements in Property Specification Patterns using LLMs*（AI4CC-IPS-RCRA-SPIRIT@AI\*IA 2024，⛔ **无 DOI，仅题录级待核**）—— ⭐ **预定义模式集 + LLM 选模式**，形状与 Zrelli 逐项对应。

⭐ Zrelli 等 JSS 2026 是本轮「闭合集合 + 选类交给模型」同时成立的工作**之一**（⚠️ **仅 2 例支撑，其中 1 例仅题录级**）。 ⭐ 它按 §0.1.1 判为**邻域**，⛔ 但正因如此把 B 档子情况的触发条件顶到了边界线上：

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
| **1** | ⭐⭐ **已核完（层 2 全文）**：GWT 那篇**确认「跳过即静默」** | ⭐⭐ **本轮最高价值的确认** —— 见 §3.3 |
| **2** | ⛔ **已核完**：`Scaling Assessment of Student Models`（SEET@ICSE 2026）**不含状态机** | ⭐ 作者自陈评测限于 class + activity diagram（§5 External Validity）；全文 `state machine` **0 命中** → ⭐ **维持邻域** |
| **3** | ⛔ **已核完**：MCeT 的分母 **135 未印，且公开制品也算不出来** | ⭐ 全文三位数频次表 `135` 零命中；⚠️ 且 Table III 的第二个分母（**14**）同样只能反推 —— ⭐⭐ **这篇的体例就是只印分子与百分比、从不印分母**，⛔ 不是 135 这一处的偶然遗漏。⛔ 其公开制品的人工真值是**自由散文**（84 个 `.score`），⚠️ **切成 135 条离散 issue 的那一步既没印也没放进制品** |
| **4** | ⭐ **已核完（部分）**：`baselines/*/DESC.md` 那四组转述数字**全部与原文一致** | ⭐ 层 2 已回 `paper_content.txt` 逐条核（`ai-driven` Table 4 · `rebeca` L771-779 · `designing-fsm` Table 2/3/4）→ ⭐ **该项义务可销账** |
| **5** | ⛔⛔ **已核完，且前提是错的**：`Automata Models for Effective Bug Pattern Description` **既无目录、也不界内** | ⛔ `catalog` / `taxonomy` / `predefined` 全文**各 0 命中**；其 "bug pattern" 是**对单个 bug 现学的 DFA**（`we apply automata learning to identify patterns in failures`）。⛔ 被查制品是 **Java 代码 / 运行系统**（§III `The set of failed tests, called bugs`；§X-A `given in Java code`）→ ⭐ **归邻域**。⭐ 其价值改为 §3.3 的**又一个反面参照**（§III 逐字 `producing regular languages that approximate the bug` + §V 的 `don't care` 松弛） |
| **5b** | ⚠️ **两条 caveat 必须保持可见** | ⛔ Automata Models 的判读基于 **arXiv v2 预印本**，⚠️ **未与 IEEE 刊出版逐字比对**；⛔ SoSyM 2021 的「约 23 个观测算子」是**从散文清点的下界**，⚠️ 权威定义在**未获取的图**里 —— ⛔ **两者都不得写成已定** |
| **6** | ⏳ 未做：LLM4MDE 映射的 **11 篇 Model Validation 具名清单** | ⭐ 把 Q5 计数从 3 提高或证否的最短路径 |
| **7** | ⛔ **已核完**：`Unified verification and monitoring of executable UML specifications`（SoSyM **2021**） | ⭐⭐ **它的观察者自动机守卫底层是「任意无副作用 C 表达式」**（Appendix C.1 逐字 `any C expression without side effect on model execution can be used`）→ ⛔ **不是闭合词表**。性质**人手写**（Appendix A.2 `expressed as PUSMs from the system requirements`）。表达不了时**改换自动机类别**（Büchi ↔ observer）⛔ 而非记缺口。⚠️ **2021 年，⛔ 进不了 2022+ 门槛**。⚠️ 证据级别混合：Abstract + 附录 A–D + 作者 Lean artifact 为一手，⛔ **正文 §1–§8 与全部图未获取**（闭放，四处交叉确认） |
| **8** | ⛔⛔ **新增（C2 反驳发现）**：Q3 漏筛了 Wang et al. Internetware 2025 的 workbook | ⚠️ 而 `ground_truth_limitations.md` 逐字称它「**唯一可用的外部对照**」—— 见 §4.2b |

---

## 8. ⛔ 覆盖范围声明（⚠️ 所有「未见 X」的合法前提）

**venue 族**：ICSE / ESEC-FSE / ASE（2748 条题录全卷 TOC 机械扫，2022–2025 主会）· MODELS 2023/2024/2025 主会（83 篇全量 TOC）· SoSyM vol 23/24/25（2024–2026 全量逐期）· RE 2022–2025 + REJ vol 29/30（33 篇全量）· ECMFA 2023/2024/2025（38 篇全量）· CAV/FM/FMSD（⚠️ **仅覆盖一个关键词簇**）· arXiv。

**年份窗**：2022–2026 为主窗；≤2021 为次窗（仅为人工检视类量级背景而查）。

**入口**：DBLP publication search API（含 `venue:` 过滤）· DBLP 会议卷 TOC 全量抓取后本地 grep · JOT contents · conf.researchr · WebSearch · 三次一手 PDF 取件。

### ⛔ 明确没跑的（⚠️ 「未见」的边界就在这里）—— ⭐ 2026-08-12 经 C3 补轮更新

⭐ **覆盖已从 2748 条扩到 5154 条（+2406，+88%）**，⛔ **五问一问都没换档** —— ⭐ 那本身是一次独立稳健性检验，⛔ 但**不能**写成「说明该方向为空」（§0.1.7）。

| 原 # | 状态 |
| :-- | :-- |
| 1 · ACM DL / IEEE Xplore / Scopus / WoS 字段化或全文检索 | ⛔ **仍未跑** —— ⚠️ **本轮最大假阴性来源**。⭐ 已用 OpenAlex 10 串做**摘要级**部分缓解，⛔ 不等于全文检索 |
| 2 · ICSE 卫星卷 · FSE workshop / Industry | ⭐ **已跑**（1445 条）。⚠️ 剩余：ICSE SEIP/SEET 若在 DBLP 另立卷 —— ⛔ 本轮枚举未见独立卷，**该推定未独立复核** |
| 3 · MODELS 2022 主会 · MODELS Companion 全部 · STAF LLM4MDE/LLM4SE | ⭐ **前两项已跑**（577 条）。⛔ **STAF 系工作坊仍一篇未扫** |
| 4 · REFSQ 2022–2026 · REW | ⭐ **REFSQ 主会 + workshop 已全跑**（261 条）。⛔ **REW 仍未跑** |
| 5 · 前向引用追踪 | ⭐ **MCeT · SoSyM 2026 · Dwyer'99 三条已跑**。⛔ **mCUTE · Nejati'19 未跑** |
| 6 · ECMFA 2022/2026 · SoSyM vol 21–22 · MODELSWARD | ⛔ **仍未跑** |
| 7 · Simulink Model Advisor · SDV 性质模板 | ⚠️ **入口已定位、内容待人工核验**：两条 404、一条动态壳。⭐ `hisf_` 规则集与 SDV Example Properties 子库经搜索摘要确认存在，⛔ 全表未取件 |
| 8 · RV 规约语言族（Salt/LOLA/TeSSLa/MOP） | ⛔ **仍未跑** |
| 9 · 非英文文献 · 工业白皮书 | ⛔ **仍未跑** |
| 10 · 两串 429 未取回 | ⭐ **两串均已取回**：`requirements traceability state machine` 命中 1 条（CSER 2012，⛔ 不过门槛）· `statechart consistency requirements` **跑了 0 命中**。⚠️ 两个数都是 **DBLP 标题级 AND** 的弱结果 |

### ⛔ C3 新发现的「没跑」（⚠️ 初版既没跑、也没登记）

| # | 未登记的角度 | 为什么要紧 |
| :-- | :-- | :-- |
| **11** | ~~期刊族整体缺席~~ → ⭐ **已补**（+6000 条，2022–2026 八家） | ⭐ 结果：`LLM ∩ STM` = **4 / 6000**，⛔ **无一在已有状态机上找缺陷**；`assertion\|contract\|invariant` ∩ 状态机族制品 = **0 / 6000**。⭐ **五问仍一问未换档。** ⚠️ 三条口径限制见下 |
| **11a** ⛔⛔ | ⚠️ **补轮的入口是 OpenAlex 不是 DBLP** | ⛔ DBLP 当时持续 500/503，⭐ 只完成 38/40 格的题录数交叉核对。⚠️ 两个入口成员集**不同质**（early-access 年 vs 卷年、online-first 是否计入），⛔ **未做逐条集合比对** |
| **11b** ⛔⛔ | ⚠️ **四家期刊的「0」只等同于标题级零** | ⛔ Elsevier / Springer 不向 Crossref 交摘要 —— 实测摘要可得率 **EMSE 43% · JSS 40% · IST 35% · SQJ 28%**（⭐ 而 TSE 98% · TOSEM/STVR 100%）。⚠️ **IST / JSS 恰是我方取数最多的两家** |
| **11c** ⛔⛔ | ⚠️ **补期刊族又漏了四家** | ⛔ **ASEJ**（Automated Software Engineering，⚠️ **原任务书名单里就没有它**）· **SCP** · ⭐⭐ **JOT**（⚠️ **ECMFA 2019 起在此出版**）· ⭐⭐ **IET Software**（⚠️ **§6.3 第 1 条那条唯一直接讲状态机的他人自陈就出自它**）。⭐ **下一轮最高收益仍在期刊侧** |
| **12** ⭐⭐ | **2026 年卷全线未扫** | ⛔ **声明的窗（2022–2026）与实际扫的窗（到 2025）不一致**，⚠️ 差的正是最近一年，⭐ 而 Q5 全部计数只认 2022+ |
| **13** ⭐⭐ | **形式化方法 / 测试族整体缺席**：FormaliSE · NFM · iFM+FMAS · SEFM · FASE · TACAS · SPIN · ISSTA · ICST · ICFEM · SANER | ⛔ C3 的引用追踪**恰好在 FormaliSE 2025 与 FMAS@iFM 2025 各捞到一条 Q4 候选** |
| **14** ⭐ | **反向雪球（读参考文献表）** | ⭐ MCeT / SoSyM 2026 / Completion-of-SysML 的 related work 是同类工作最密的一处 |
| **15** ⭐⭐ | **两份现成的第三方候选池**：LLM4MDE 映射（EMSE 2026）的 **86 篇具名清单** · **N-08**（CoRR 2026 UML×LLM 综述）的清单 | ⛔ **跨类漏登记** —— ⚠️ 前者只藏在 §7 待核第 6 项，覆盖声明的读者看不到它没跑 |
| **16** ⭐ | **同类工业规则集只登记了 Simulink 一家**：Eclipse OCL / USE / EVL / Epsilon · Papyrus · MagicDraw / EA 的内置校验规则 | ⛔ §5.4「都没有一篇把表达不了的义务显式记成缺口」正是工业规则集最可能证否的地方 —— ⭐ 已找到反例线索（见下） |
| **17** | **Semantic Scholar `/paper/search` 端点** | ⛔ 匿名请求硬性 429，⭐ 需 API key 重试 |
| **18** | **ASE 2022 若有 workshop 卷** | ⚠️ DBLP `conf/kbse` 下无 `ase2022w`，⛔ 该缺席**未独立复核** |

### ⭐⭐ 一条对 §5.4 的反驳线索（⚠️ 摘要级，⛔ 三条限制）

⭐ [MathWorks 高完整性建模指南 ↔ Model Advisor 映射表](https://www.mathworks.com/help/slcheck/ref/model-advisor-checks-for-high-integrity-systems-modeling-guidelines.html) 的做法与我方断言相反：一套带稳定编号的规则集（Stateflow 侧 `hisf_XXXX`），⭐⭐ **且该映射表显式列出「哪些指南没有对应的检查」并给出理由 —— 逐字 `automation isn't possible`**。

⛔ **三条限制**：① **摘要级**，全表未取件（动态壳 + 404 拦住）；② 对象是 **Stateflow**，并行状态与 temporal logic 有相当部分**落在边界门外**；③ 它是**工具指南而非文献**，⭐ 按 §0.1.8 只能作**存在性移交**，⛔ 不作规范性出处、⛔ 不由 L1 定级。

### ⭐ C3 新命中的 18 条候选

⛔ **全部标题 / 摘要级，一篇正文都没读**；⛔ 边界门判定同为**待核初判**。⭐ 完整表见 [search_ledger.md](./search_ledger.md)。⚠️ 其中三条会改变已有表述：**N-01/N-02/N-03**（冲击「近年后继全部外流」，见 §5.2）· **N-06**（冲击 §5.4 的**唯一**那个措辞）· **N-18**（⭐ *Formalizing UML State Machines for Automated Verification – A Survey*，CSUR 2023，⚠️ **仓库 `state_machine_types/` 已收全文，⛔ 而本份交付五问一次都没用它** —— ⭐ 一份 2022+ 界内综述闲置，同时 Q1 各类目在为 2022+ 发愁）。

⭐ 另两条应正式进 Q3 的逐条筛除记录（⭐ 使筛除记录从 14+ 增至 16+）：**N-10**（NDSS 2023，⛔ 缺门① —— 模型是它自己学出来的，属生成后自评）· **N-11**（EASE 2023，⛔ 缺门② —— 对象是需求文本、执行者是人）。

### ⚠️ 一条事实纠正

⭐ DBLP `conf/ecmdafa` 收录**止于 ECMFA 2018** —— ⛔ 那是 **DBLP 的收录断层，不是会议停办**。ECMFA 自 2019 起在 *Journal of Object Technology* 出版，2026 年将办第 22 届 @ STAF。⚠️ 本条为执行者报告，⛔ 本方**未独立复核**。
