# 卡片 · Wang, Ge et al., Internetware 2025 —— LLM 生成 SysML 行为模型的实证研究（句法 / 语义幻觉 ＋ model-checking 规则反馈）

⭐ **全文已通读**（⛔ 不是仅据摘要）。⭐⭐ **而且这篇本仓库早就有了** —— ⭐ 它就是 [`baselines/llms_emp/`](../../../../baselines/llms_emp/)，⭐ DOI 逐字对上（`10.1145/3755881.3755926`）。⭐ 本卡的正文断言来自 [`baselines/llms_emp/paper_content.txt`](../../../../baselines/llms_emp/paper_content.txt)（1189 行，全文 12 页）。

⭐⭐ **本卡另有一件事是上游卡片没做的**：⭐ 我**实际把作者公开的三个 Google Sheets 全下载下来了**（⛔ 不只是核 HTTP 200），⭐ 于是 D 节的资产判定、C 节的 `judged_by`、⭐ 以及下面那条「⛔ 公开数据集组成与论文声明对不上」都是**实测**，⛔ 不是从论文推的。

⚠️ **本卡开头先回答任务书最要紧的三问，⛔ 因为第 3 问决定这篇是「强背书」还是「只是同路人」。**

---

## ⭐⭐ 先答第 1 问：「规则清得掉句法、清不掉语义；要靠反例与仿真轨迹」原文逐字是什么、有什么证据

### 逐字原文（⭐ 共三处，⛔ 全部核对过）

**① 摘要（M，逐字）：**

> "The evaluation results show that while the models generally meet syntactic requirements, they consistently lack semantic accuracy. Across both phases, LLMs achieve over 90% grammar accuracy. For semantic accuracy, the average F1-score for ACT reaches 95%, while SD drops to just 50%. **These results demonstrate that while our model-checking rules effectively correct format and syntax, they are insufficient for addressing deeper semantic gaps. Overcoming these challenges requires advanced strategies, such as counterexamples and simulation traces, to provide optimal feedback.** Additionally, model-checking in LLM-based generation is costly, and reducing this cost is another critical issue to address in the future."

**② §1 Introduction（M，逐字）：**

> "Model-checking rules effectively remove syntactic defects (grammar and format), but semantic issues persist, clarifying current limitations and pointing to future research directions."

**③ §6.4 Findings in RQ2（M，逐字 —— ⭐ 这是最完整、也最要紧的一处）：**

> "The results show that model-checking rules effectively correct syntactic hallucinations, addressing structural and grammar errors and ensuring LLMs follow explicit grammar rules. However, semantic hallucinations in SysML have a low resolution rate of 36.89%, highlighting LLMs' difficulty with SysML semantics and reasoning. For requirement consistency, ACT achieves an 83.33% resolution rate, STM 42.14%, and SD only 16.67%. **Model-checking's impact on complex reasoning is limited. As rule complexity increases, LLMs may lose focus on the original requirements, and fixing one issue can introduce new ones.**
>
> **One key reason is the lack of an optimal model-checking feedback mechanism in our study.** To overcome these limitations, formal verification techniques present a promising solution. By automatically verifying model correctness, they can detect errors and generate counterexamples. **These counterexamples can be provided as feedback to the LLM**, aiding in refining its output and improving focus during regeneration. However, we have also noted that **the cost associated with model checking is relatively high.** Due to theoretical constraints inherent in model checking, verifying a specific property or functionality may require substantial time, and **in some cases, may not yield a conclusive verification result.**"

### ⭐⭐ 它给了什么证据 —— ⭐ **答案：有实验，⭐ 而且是逐规则的**

⛔ **这一点与 [sosym2026-state-machine-consistency.md](./sosym2026-state-machine-consistency.md) 那篇形成鲜明对比**：⭐ 那篇的同类论断只有「断言 ＋ worked example ＋ 文献计量旁证」，⛔ 无对照实验。⭐ **这篇有一张 29 条规则 × 逐条解决率的表（Table 11），⛔ 而且我已经逐条复算过。**

| 层次 | ⭐ 规则条数 | ⭐ 解决率（micro，我方复算） | ⭐ 论文自报（macro，逐规则平均） | ⭐ 结论 |
| :-- | :-: | :-: | :-: | :-- |
| ⭐ PlantUML **格式** | 3 | ⭐ **35/37 = 94.59%** | 83.33% | ⭐ **规则有效** |
| ⭐ SysML **语法** | 4 | ⭐ **22/25 = 88.00%** | 90.97% | ⭐ **规则有效** |
| ⛔ SysML **语义** | 6 | ⛔ **31/72 = 43.06%** | ⛔ **36.89%**（⭐ 论文引的就是这个） | ⛔ **规则基本无效** |
| ⛔ **需求一致性** | 16 | ⛔ **56/150 = 37.33%** | ⛔ STM 42.14% · ACT 83.33% · SD 16.67% | ⛔ **规则基本无效** |

⭐ **合计 29 条规则 · 284 条幻觉 · 解决 144 条。** ⭐⭐ **我方已用作者公开的逐条台账独立对账：`resolved == yes` 恰好 `144` 条，⭐ 与论文 `35+22+31+56 = 144` 精确一致**（→ D 节）。

⭐ **代价也报了**（M，§6.2 逐字）：

> "For STM, ACT and SD, the (minimal ratio, maximum ratio) of G$_T$-II and G$_T$-I are **(2.72, 7.67), (4.05, 4.81), (4.00, 4.31)**, respectively. This indicates that **model generation with model-checking feedback enhancement is indeed time-consuming.**"

### ⭐⭐ 第 1 问的裁定 —— ⭐ **这是我们「修订机器零收益」那条实测的强外部背书，⛔ 但要按层次引，不能笼统引**

⭐⭐ **它给出的不是「反馈无效」，而是「反馈的收益按层次断崖式下降」：⭐ 句法层 88–95%，⛔ 语义层 37–43%。** ⭐ 这正好把我们 v46 的 `−15.82pp` ＋「修订机器吃 79% token 而覆盖净变化 ≈ 0」放进了一个可解释的位置：⭐ **我们的 discover 任务整体落在它的「语义层 ＋ 需求一致性层」，⛔ 而那两层恰恰是反馈收益最低的两层。** ⭐ 于是「零收益」不是我们的实现 bug，⛔ 而是一个**有外部实证的层次性现象**。

⛔ **但引用时必须带三条限定，⛔ 否则会被反驳：**

1. ⛔ **它的「解决率」不是「检出率」。** ⭐ 分母是 Phase-I **已经检出**的幻觉条数，⛔ 所以它衡量「反馈能修好多少已知缺陷」，⛔ **不衡量「能发现多少缺陷」** —— ⭐ 而我们的 `hit@k` 衡量的是后者。⛔ **两个数不可直接比。**
2. ⛔ **规则是从被评测样本本身归纳出来的（无 hold-out）** —— ⭐ 见 E §2 第 1 条。⛔ 所以那 88–95% 的句法层数字是 in-sample 上界。
3. ⛔ **`SD 16.67%` 我复算不出**（⭐ 我方 macro = 16.04%，micro = 23.00%）—— ⭐ 见 F §1。

---

## ⭐⭐ 再答第 2 问：句法幻觉 vs 语义幻觉怎么分的、各占多少

### ⚠️ 先记一条：**同一篇里分类学有两种说法**

⭐ §4.2 说 **四类**（M，逐字）：

> "Hallucinations are grouped into four types: **PlantUML formatting errors, SysML grammar errors, SysML semantic inconsistencies, and requirements semantic inconsistencies.**"

⛔ §5.4 说 **三类**（M，逐字）：

> "We define hallucinations as outputs that do not conform to the input requirements, and categorize them into three types: **PlantUML format errors, SysML grammar & semantic errors and requirements inconsistencies.**"

⭐ **实际的表结构（Table 8/9/10）走的是「四类，但语法与语义并在一张表里」**：⭐ Table 8 = 格式 · Table 9 = 语法 ＋ 语义（同表两段）· Table 10 = 需求一致性。⭐ **本卡按四类记，⛔ 并把这处不一致登记为 F §2。**

### ⭐ 判据逐字抄（⛔ 这是「谁来判、拿什么判」这一格）

| 类别 | ⭐ 判据逐字（M，§4.2） | ⭐ 判定者 |
| :-- | :-- | :-- |
| ⭐ **① PlantUML 格式** | "Validates conformance to PlantUML syntax/format rules. **Results are reported automatically by the PlantUML model checker.**" | ⭐ **自动**（工具） |
| ⭐ **② SysML 语法** | "Assesses adherence to SysML grammar. **Because PlantUML lacks a SysML grammar checker, we manually compare each item against the standard and record the errors.**" | ⛔ **人工** |
| ⭐ **③ SysML 语义** | "Assessed compliance with semantics defined in the SysML standard. **As PlantUML does not support semantic validation, we manually check the model against 55 semantics and log violations.**" | ⛔ **人工**（⭐ 对着 55 条清单） |
| ⭐ **④ 需求一致性** | "We define this as evaluating semantic consistency between the generated model and **a reference model.** […] In this study, **we assume the reference model is semantically correct and compute the F1-score between the generated and reference models** to quantify requirement semantic alignment." | ⭐ 半自动（⭐ GP 匹配算 TP/FP/FN） |

⚠️⚠️ **④ 这一格是个术语陷阱，⛔ 必须点出来**：⭐ 它叫 **requirements** semantic checking，⛔ **但操作化是「与参考模型算 F1」** —— ⛔ 即**用人建的参考模型代理需求**，⛔ 判定实际是 **model-vs-model**，⛔ 不是 model-vs-NL。⭐ 这与 [sosym2026-state-machine-consistency.md](./sosym2026-state-machine-consistency.md) 的陷阱是同一种，⛔ 只是换了个名字。⭐ **详见下面第 3 问后的「与我们的问题定义对照」表。**

### ⭐ 各占多少（⛔ 逐表抄下）

⭐ **Table 8 · PlantUML 格式幻觉（37 条）**

| Type | Number | Percentage |
| :-- | :-: | :-: |
| Non-Existent Element | 30 | 81.08% |
| Format Error | 4 | 10.81% |
| Element is not Closed | 3 | 8.11% |
| ⭐ **Total** | **37** | 100.00% |

⭐ **Table 9 · SysML 语法（25 条）＋ 语义（72 条）**

| 分类 | Type | Number | Percentage |
| :-- | :-- | :-: | :-: |
| Grammar | STM: Transition syntax error | 4 | 16.00% |
| Grammar | STM: Composite State syntax error | 2 | 8.00% |
| Grammar | ACT: Fork syntax error | 1 | 4.00% |
| Grammar | ⛔ SD: Block syntax error | **18** | **72.00%** |
| Grammar | ⭐ **Total** | **25** | 100.00% |
| Semantic | ⭐ **STM: missing Regions** | **20** | **27.78%** |
| Semantic | STM: missing PseudoState | 5 | 6.94% |
| Semantic | ACT: normal nodes as ActivityFinalNode | 1 | 1.39% |
| Semantic | ACT: missing ReduceActions | 1 | 1.39% |
| Semantic | ACT: meaningless ActivityPartitions | 1 | 1.39% |
| Semantic | ⛔ SD: missing DestructionOccurrenceSpecification | **44** | **61.11%** |
| Semantic | ⭐ **Total** | **72** | 100.00% |

⚠️⚠️ ⭐ **`STM: missing Regions 20 (27.78%)` 这一行就是本仓库 [CLAUDE.md](../../../../../CLAUDE.md) 「核心技术概念」节里那句「基线论文的最大语义类正是 missing regions」的出处** —— ⭐ 它是 **STM 语义类里最大的一类**（⛔ 全表最大的是 SD 那 44 条）。⭐ **本卡确认该引用成立，⛔ 并把口径钉准为「STM 语义子类内最大」。**

⭐ **Table 10 · 需求一致性幻觉（150 条）**

| 模型 | 分类 | Type | Number | Percentage |
| :-- | :-- | :-- | :-: | :-: |
| STM | Model Inaccuracy | Missing State or Transition | 7 | 30.43% |
| STM | Model Inaccuracy | Incorrect Transition | 6 | 26.09% |
| STM | Model Inaccuracy | Missing Final State | 5 | 21.74% |
| STM | Model Inaccuracy | Missing Composite State | 5 | 21.74% |
| STM | | ⭐ **Total** | **23** | 100.00% |
| ACT | Model Inaccuracy | Missing ActivityNode | 8 | 29.63% |
| ACT | Model Inaccuracy | Incorrect Node Placement | 3 | 11.11% |
| ACT | Model Inaccuracy | Incorrect Parallelism | 3 | 11.11% |
| ACT | Model Inaccuracy | Incorrect Use of Domain Terminology | 2 | 7.41% |
| ACT | Model Inaccuracy | Missing InitialNode | 2 | 7.41% |
| ACT | ⭐ **Over-specification** | ⭐ **Extra ActivityNode** | **9** | **33.33%** |
| ACT | | ⭐ **Total** | **27** | 100.00% |
| SD | Model Inaccuracy | Incorrect Messages type | 45 | 45.00% |
| SD | Model Inaccuracy | Incorrect Messages interaction sequence | 28 | 28.00% |
| SD | Model Inaccuracy | Incorrect CombinedFragment | 13 | 13.00% |
| SD | Model Inaccuracy | Missing Messages | 6 | 6.00% |
| SD | Model Inaccuracy | Missing Lifeline | 5 | 5.00% |
| SD | Model Inaccuracy | Incorrect Lifeline | 3 | 3.00% |
| SD | | ⭐ **Total** | **100** | 100.00% |

⭐⭐ **对我们最有用的两条读数：**

1. ⭐⭐ **STM 的需求一致性缺陷 23 条里，「漏」占 17 条（Missing State/Transition 7 ＋ Missing Final State 5 ＋ Missing Composite State 5 = 74%），「错」占 6 条。** ⭐ 这与我们台账的形态高度同构 —— ⭐ **「漏元素」是主类，⛔ 不是「写错语义」。**
2. ⭐⭐ **`Over-specification`（多报 / 过度建模）只在 ACT 上出现，共 9 条 = ACT 的 33.33%；⛔ STM 与 SD 一条都没有。** ⚠️ ⭐ 这一点值得警惕：⛔ **不是 STM 真的不会过度建模，⭐ 而是它的分类学在 STM 上没有这一类** —— ⭐ 而我们 v46 的五类多报分类恰恰在 STM 上抓到了大量多报。⛔ **所以它的 STM 分类学在「多报」这一维是空的，⛔ 不能当成「STM 不多报」的证据。**

### ⭐ 句法 >90% 但 SD 语义 F1 只有 50% —— ⭐ 任务书这条初筛**成立**（M）

| 指标 | STM | ACT | SD |
| :-- | :-: | :-: | :-: |
| ⭐ Acc$_P$（PlantUML 格式） | >90% | >97% | >98% |
| ⭐ Acc$_S$（SysML 语法） | >98% | >99% | >90% |
| ⛔ **F1（语义一致性）** | ⛔ **69.29%**（65.17%–80.27%） | ⭐ **97.49%** | ⛔ **50.02%** |

⭐ 逐字（§5.3）：

> "ACT attains the highest mean (**97.49%**) […] STM averages **69.29%**(65.17% - 80.27%), suggesting LLMs capture key states and transitions but with incomplete coverage. SD is lowest at **50.02%**, recovering only half of interaction structures and thus proving most challenging for LLM-based generation."

⚠️ ⭐ 摘要写的是「ACT reaches 95%」，⛔ §5.3 写的是 97.49% —— ⭐ 摘要那个是约数。⭐ **引用请用 §5.3 的 97.49%。**

⭐ **还有一格值得单抄（Table 7）** —— ⭐ 它把语法准确率按「嵌套结构 NS」与「字段约束 FC」拆开，⭐ 而**拆开之后 STM 的数字塌了**：

| Model Type | N#NS | N#FC | Acc$_S$@NS | Acc$_S$@FC |
| :-- | :-: | :-: | :-: | :-: |
| STM | 70% | 20% | 97.26% | ⛔ **69.29%** |
| ACT | 100% | 40% | 99.31% | 97.49% |
| SD | 60% | 100% | 99.77% | ⛔ **50.02%** |

⚠️⚠️ **注意：⛔ `Acc_S@FC` 这一列的三个数（69.29 / 97.49 / 50.02）与 §5.3 的三个 F1 数（69.29 / 97.49 / 50.02）逐位相同。** ⭐ 这**极可能是制表时把 F1 列误粘进了 Table 7**，⛔ 而不是两个独立指标恰好三位小数全等。⛔ **本卡不采信 Table 7 的 `Acc_S@FC` 列，⭐ 并登记为 F §3。**

---

## ⭐⭐ 第 3 问（⛔ 任务书说这个区别很关键）：「反例与仿真轨迹当反馈」它自己做了没有

### ⛔⛔ **答案：没有做。⭐ 纯 future work。**

⭐ **三处逐字，⛔ 全部是将来时 / 建议式：**

1. ⭐ 摘要：「Overcoming these challenges **requires** advanced strategies, such as counterexamples and simulation traces, to provide optimal feedback.」
2. ⭐ §1：「Finally, we examine causes of hallucination, **propose** richer feedback (e.g., counterexamples, simulation traces), and high cost of model checking as a **ongoing challenge**.」
3. ⭐ §6.4：「To overcome these limitations, formal verification techniques **present a promising solution.** […] These counterexamples **can be** provided as feedback to the LLM」

⭐ **§8 Conclusion 再确认一次（M，逐字）：**

> "While syntactic errors are mostly resolved, semantic issues persist, suggesting that **the feedback mechanism using formal verification techniques needs further investigation** to help LLMs better understand complex requirements and logical relationships."

### ⭐ 它实际做的反馈是什么 —— ⛔ **自然语言祈使句，⛔ 不是反例**

⭐ Table 11 的 `Checking Rules` 列**逐字就是喂给 LLM 的反馈文案**，⭐ 抄几条看形态：

- `"Do not use non-existent elements"`
- `"Composite State must contain at least one Region."`
- `"Region contains at least one InitialState and State"`
- ⛔ `"Don't miss out State in requirements"`
- ⛔ `"Pay attention to the rationality of the State between Traditions"`（⚠️ ⛔ 原文拼写如此，`Traditions` 应为 `Transitions`）
- ⛔ `"Don't over-design"`

⭐⭐ **这一格的裁定：⭐ 它的反馈是「把规则名用祈使句复述一遍」，⛔ 既没有反例（哪条路径违反了）、⛔ 也没有轨迹（在哪一步违反）、⛔ 也没有定位（哪个元素）。** ⛔ **所以「语义层只修好 37–43%」这个结果，⭐ 与「反馈内容极其贫瘱」是分不开的** —— ⭐ 论文自己也是这么归因的（§6.4「the lack of an optimal model-checking feedback mechanism」）。

⚠️⚠️ ⭐ **这对 M1 是一条很硬的可取之处：⭐ 我们的 `precheck_and_seal` 已经是 pyfcstm 真求值，⭐ 能给出「哪条断言在哪个状态上求值为假」。⭐ 换句话说，⭐ 这篇论文点名要的那个东西（counterexample / simulation trace 当反馈），⭐⭐ 我们已经有了 —— ⛔ 而我们的问题不在这里，⛔ 在于它被放在求值端而不是裁决端。** ⭐ 所以**这篇不能当成「我们该去做反例反馈」的依据，⭐ 而应当当成「反例反馈的必要性有外部背书」的依据。**

---

## ⚠️ 与我们的问题定义对照（⛔ 术语陷阱，⭐ 必须先摆清）

| 维度 | ⭐ 它 | ⭐ 我们（v46） |
| :-- | :-- | :-- |
| ⭐ **主任务** | ⛔ **生成**（NL → PlantUML 行为模型）；⭐ 缺陷检测是**为归纳 taxonomy 而做的副产品** | ⭐ **在既有模型上做缺陷检测** |
| ⭐ 判定分母 | ⛔ **已检出的幻觉条数**（284）· ⭐ F1 的分母是 grammar point 数 | ⭐ NL 需求台账条目（98 条能力分母） |
| ⭐ reference | ⛔ **人建的参考模型**（⭐ 名义上叫 requirements consistency，⛔ 实际是 model-vs-model 的 F1） | ⭐ **NL 文本** |
| ⭐ 有无 recall 分母 | ⛔ **无** —— ⛔ 无「应检出多少」的独立真值 | ⭐ 有（台账 98 条） |
| ⭐ 多轮口径 | ⛔ **无 `@k`** —— ⭐ `temperature = 0` 单次跑 | ⭐ `hit@1` / `hit@3` / `hit@all` 三口径同报 |

⛔⛔ **裁定：⭐ 与我们不是同一个任务，⛔ 它的任何数字都不能当我们的可比数字。** ⭐ 但它的**层次性结论**（句法层反馈有效 / 语义层反馈无效）是**跨任务可迁移的**，⛔ 因为那说的是反馈机制的性质，⛔ 不是某个任务的分数。⭐ **这就是它对我们的全部价值所在。**

---

## A. 元信息

| 字段 | 值 |
| :-- | :-- |
| `id` | `internetware2025-sysml-behavior-generation` |
| `title` | ⭐ **Generating SysML Behavior Models via Large Language Models: an Empirical Study**（M，⭐ 与 [`baselines/llms_emp/bibtex.bib`](../../../../baselines/llms_emp/bibtex.bib) 逐字一致） |
| 作者 | ⭐ **Yuan Wang · Ning Ge**（⭐ 通讯）· **Jiangxi Liu · Zhilong Cao · Zheping Chen · Chunming Hu**（M）—— ⭐ 全部 **School of Software, Beihang University**（⛔ 单一机构，⛔ 无外部合作者） |
| `year` | ⭐ **2025**（M）—— ⚠️ ⭐ 会期 `2025-06-20`–`06-22`，⛔ 而 ACM 落地页写 `Published: 27 October 2025`；⭐ BibTeX 记 `month = jun, year = 2025`。⭐ **两种口径同年，⛔ 无 early-access 歧义** |
| `venue` | ⭐ **Internetware 2025**（16th International Conference on Internetware），⭐ Trondheim, Norway；⭐ ACM，⭐ **SIGSOFT** 赞助；⭐ pages **366–377**（12 页）；⭐ ISBN `979-8-4007-1926-4` |
| `ccf` | ⚠️ **C（⛔ 未独立核验）** —— ⛔ 本仓库 [ccf_venues/](../../../../../ccf_venues/) **未收录 Internetware**（⭐ 已 grep 全库，⛔ 无 `conf-*-internetware`）。⭐ 本仓库 [`baselines/llms_emp/ASSETS.md`](../../../../baselines/llms_emp/ASSETS.md) 记为 `🥉` 即 CCF C。⛔ **本卡沿用该记录，⛔ 但标明未在 ccf_venues 建档、未查第七版目录原件** |
| `doi` | ⭐ [`10.1145/3755881.3755926`](https://doi.org/10.1145/3755881.3755926) —— ⭐ **实际访问过**（⭐ 本地 PDF 5.2 MB ＋ `paper_content.txt`）。⚠️ ⛔ `verify_assets` 对 `doi.org` 得 **HTTP 403**（⭐ ACM DL 的 Cloudflare），⛔ 非 DOI 不存在 |
| `arxiv` | ⛔ **无** |
| `url`（数据） | ⭐ [Google Drive 文件夹](https://drive.google.com/drive/folders/10eo8KDqlBlkQZxPpPCB7R3-aBQZ7Rsm6) —— ⭐ **本轮实取三个工作簿，⛔ 见 D 节** |
| `artifact_type` | ⭐ **SysML v1.6 行为模型，⭐ 以 PlantUML 编码**：⭐ 状态机（STM）· 活动图（ACT）· 时序图（SD） |
| `task` | ⭐ **生成**（主）＋ **缺陷检测 / 缺陷类型学构建** ＋ **修复**（feedback-driven regeneration） |
| `boundary` | ⚠️ **`邻域`**（⛔ 不是纯界内 —— 见下方说明） |

### ⚠️ `boundary` 为什么判 `邻域`

⭐ **三条理由，⛔ 前两条是论文侧，⭐ 第三条是我方实测（⭐ 且方向相反，⭐ 必须一起写）：**

1. ⛔ **语料本身跨三种图型** —— ⭐ ACT 与 SD 按 [README.md](../README.md) §2.1 明确属 `邻域`，⛔ 而它们占 107 行里的多数。
2. ⛔ **它的 55 条语义清单含界外构件** —— ⭐ 我方逐行读过（→ B5）：⛔ `fork` / `join` Pseudostate（⭐ 并发拆分与汇合）· `deepHistory` / `shallowHistory` · ⛔ **`TimeConstraint` / `DurationConstraint` / `TimeObservation` / `DurationObservation`（第 52–55 行，⭐ 时间约束与时间观测）**。⭐ 后四条正是 $TSM$ 相对 $M = (S,E,V,Tr,A)$ 多出来的那部分。
3. ⭐⭐ **但被检的 STM 制品实测基本是界内的** —— ⭐ 我方在冻结 parquet 上实测 38 个 STM 行：⭐ **`basic_hierarchical_state_count > 0` 的有 18 个**（⭐ 即层次状态确实存在，⭐ 属 HSM，⭐ 界内）；⛔⛔ **而 `basic_parallel_count > 0` 的是 `0` 个**（⛔ 即**没有一个 STM 制品含并发区**）。⭐ 状态数 `min/median/max = 0 / 6 / 29`，⭐ 迁移数 `0 / 8 / 34`。

⭐⭐ **所以准确状态是：⭐ 制品层面它的 STM 子集基本落在界内（HSM，⛔ 无并发区），⛔ 而评测维度层面它伸到了界外（fork/join ＋ 时间约束）。** ⭐ 按 L3 不设边界门只要求标注的规矩，⭐ 本卡标 `邻域` 并把这个**方向相反的分裂**写明。

⛔⛔ **提醒（⭐ 这一条对 N1b 特别重要）**：⭐ 若要把它的 **STM 子集**搬进 L1/L2 或当测试制品用，⭐ **那 18 个含层次状态、0 个含并发区的样本是可以过边界门的**，⛔ 但必须**逐样本**过，⛔ 不能整个语料一起过；⛔ 且必须先做 D 节说的去重。

---

## B. LLM 应用形态

### B1 · 流水线阶段（⭐ 两阶段设计，⭐ Figure 3）

```
── Phase-I（⭐ 生成 ＋ 幻觉识别）──────────────────────────────────
[人]      NL 需求（⚠️ 原始来源缺需求时由作者逆向补写）
 → [确定性] RAG 检索：PlantUML 格式说明 ＋ SysML v1.6 规约文本
 → [确定性] prompt 模板装配（⭐ 五段：Role · I · Req · S · E）
 → [LLM]   生成 PlantUML                       ⭐ ← LLM 第 1 处
 → [确定性] PlantUML 格式检查器（⭐ 工具自动报）
 → [人]     SysML 语法人工逐项比对标准
 → [人]     SysML 语义人工比对 55 条清单
 → [半自动] F1 vs 人建参考模型（⭐ 按 grammar point 数 TP/FP/FN）
── Phase-II（⭐ 规则反馈重生成）───────────────────────────────────
 → [确定性] 命中类型 → 查 29 条规则目录 → 注入 prompt 的 E 段
 → [LLM]   重生成（⛔ **fresh session**）        ⭐ ← LLM 第 2 处
 → [人/工具] 同样四维重评
```

⭐⭐ **10 个阶段 · ⛔ 只有 2 个是 LLM · ⭐ 4 个确定性 · ⛔ 3 个是人（＋1 个半自动）。**

⚠️⚠️ **一处关键结构事实（M，§6.2 逐字）：⛔ 四类检查是串行的，⭐ 所以 Phase-II 里重生成发生多次：**

> "Since model-checking tasks for PlantUML format, SysML grammar, SysML semantics, and requirements consistency are performed sequentially, **model regeneration occurs multiple times.** The total generation time is calculated by summing the time for all regeneration tasks."

⭐ **但这不是收敛循环** —— ⭐ 是**四道闸门各过一次**，⛔ 每道不复检、不回头。⭐ 详见 B4。

### B2 · 每次 LLM 调用的角色

| 环节 | 角色 |
| :-- | :-- |
| ⭐ Phase-I 生成 | ⭐ **生成器**（NL → PlantUML 行为模型） |
| ⭐ Phase-II 重生成 | ⭐ **修复者** —— ⚠️ ⛔ 但注意是 **fresh session 冷启动重生成**，⛔ **不是在原产物上改**（M，§4.2 逐字："**To avoid contamination, each regeneration runs in a fresh LLM session.**"） |
| ⛔ 评审者 | ⛔ **无** |
| ⛔ 裁决者 | ⛔ **无** —— ⭐ LLM 从不参与判定 |
| ⛔ 分类器 | ⛔ **无** —— ⭐ 幻觉归类由人做 |
| ⛔ 抽取器 / 规划者 / 解释者 | ⛔ **无** |

⭐⭐ **这一格值得记住：⭐ 全流程 LLM 只干「写」和「重写」两件事，⛔ 一次判定都不做。** ⭐ 与 [_ours-v46.md](./_ours-v46.md) 对比 —— ⭐ 我们 5 个 LLM 节点里有 **3 个在判定**（两个 reviewer ＋ 一个 adjudicator）。

### B3 · prompt 策略

| 策略 | 有无 | 证据 |
| :-- | :-: | :-- |
| ⭐ **RAG** | ⭐ **有** | ⭐ M，§4.2 逐字："We employ a **RAG component to retrieve relevant PlantUML format and SysML v1.6 specification text**"；⭐ §4.6 `Sample(S)`："The sample provides the PlantUML format **with RAG support**, including SysML syntax and semantics" |
| ⭐ **few-shot**（exemplar 模型） | ⭐ **有** | ⭐ M，§1 逐字："with **supplied exemplar models**"；⭐ §4.6 `Sample(S)` 段 |
| ⭐ **角色扮演** | ⭐ **有** | ⭐ M，§4.6 逐字：Role = "**You are an expert in SysML behavioral modeling**," "which helps reinforce the professionalism of the LLM's responses" |
| ⭐ **输出约束**（⛔ prompt 层，⛔ 非受限解码） | ⭐ **有** | ⭐ M，§4.6 `Output Content`："We direct the LLM to **output only the model content**"；⭐ `Output Format`：要求符合 PlantUML 数据格式 |
| ⭐ **反馈回灌** | ⭐ **有** | ⭐ M，§4.6 `Error(E)`："**We feed model checking results as error messages to the LLM**, highlighting issues to improve model accuracy." |
| ⭐ **贪心解码** | ⭐ **有** | ⭐ M，§4.6 逐字："We used **greedy sampling** with a **temperature setting of 0**. Greedy sampling ensures that the LLM selects the most likely result at each step, thus **avoiding the randomness** associated with other sampling methods and **guaranteeing the consistency and reliability** of generated responses." |
| ⛔ CoT | ⛔ **无** | ⭐ 全文无（S） |
| ⛔ self-consistency 投票 | ⛔ **无** | ⭐ 与 `temperature=0` 互斥（S） |
| ⛔ 工具调用 / function calling | ⛔ **无** | ⭐ 全文无（S） |
| ⛔ 多智能体辩论 | ⛔ **无** | ⭐ 全文无（S） |
| ⛔ 受限解码 / JSON schema | ⛔ **无** | ⭐ 输出是裸 PlantUML 文本（S） |

⚠️⚠️ **`temperature = 0` 这条要单独评一句。** ⭐ 论文把它当**优点**写（「guaranteeing the consistency and reliability」），⭐ 并在 Threats 的 Internal Validity 里再强调一次（逐字："we used a greedy decoding strategy and set the temperature to 0, **minimizing randomness and ensuring consistent behavior**"）。⛔⛔ **但它同时消灭了采样方差信息** —— ⭐ 于是这篇**无法回答「某条缺陷是稳定被漏还是偶尔被漏」**。⚠️ ⭐ 这正是本仓库 [CLAUDE.md](../../../../../CLAUDE.md) §3.5.2 设 `metric@k` 要解决的那个问题，⛔ 而它连提出这个问题的口径都没有。⭐ 而且它自己引的参考文献 [65] 恰恰叫 **"The good, the bad, and the greedy: Evaluation of LLMs should not ignore non-determinism"** —— ⛔ **它引了这篇却选了相反的做法**，⚠️ 且未讨论该文的主张。

⭐ **prompt 是否公开** → ⭐ **公开（🟢）**，⭐ 见 D 节（⭐ 三个 Results 表都有 `Prompt` 列）。

### B4 · ⭐⭐ 循环与裁决者（⛔ 本轨最关键的一格）

| 子字段 | 值 |
| :-- | :-- |
| ⭐ **有无循环** | ⚠️ **有，⛔ 但只有一轮，⛔ 且不是收敛循环** —— ⭐ Phase-I → Phase-II，⛔ **Phase-II 之后不再复检、不再回头** |
| ⭐⭐ **裁决者是谁** | ⭐ **① `parser / 编译器`**（⭐ PlantUML model checker，⭐ 自动，⛔ 只管格式）· ⭐ **② `人`**（⛔ SysML 语法、⛔ SysML 语义、⛔ 需求一致性 —— ⭐ 三类中的两类半全靠人工）· ⭐ **③ `确定性规则`**（⭐ F1 的 GP 匹配）。⛔⛔ **`LLM 自评` = 无。⛔ `sound oracle` = 无。⛔ `测试执行` = 无** |
| ⭐ **终止条件** | ⛔ **固定轮数（1 轮）** —— ⛔ 无收敛判据、⛔ 无预算门、⛔ 无 no-progress 计数 |
| ⭐ **最大轮数** | ⭐ **1**（⭐ 四类检查各触发一次重生成，⛔ 但每类不迭代）。⛔ 论文未给任何收敛上限 |
| ⭐⭐ **有无报告循环的边际收益** | ⭐⭐ **有 —— ⭐ 而且是本轨目前最细的一份**（⭐ 逐规则，⛔ 29 条） |

#### ⭐⭐ 逐规则边际收益全表（⛔ Table 11 逐条抄下，⭐ 已复算自洽）

⭐ **这张表是本卡最有价值的一格，⭐ 因为它是「反馈到底修好了什么」的逐条账。**

| 幻觉大类 | 幻觉子类 | ⭐ Checking Rule（⛔ 逐字，⭐ 这就是喂给 LLM 的反馈文案） | ⭐ Resolved |
| :-- | :-- | :-- | :-: |
| PlantUML Format | Non-Existent Element | `Do not use non-existent elements` | ⭐ **30/30** |
| PlantUML Format | Format Error | `The usage of elements comply with data format` | 2/4 |
| PlantUML Format | Element is not Closed | `Paired elements must be closed` | ⭐ **3/3** |
| SysML Grammar | SD use Block syntax error | `Use Block instead of Actor` | 16/18 |
| SysML Grammar | STM use Transition syntax error | `Transition must connect two State` | 3/4 |
| SysML Grammar | STM use Composite State syntax error | `Composite State must contain at least one Region.` | ⭐ **2/2** |
| SysML Grammar | ACT use Fork syntax error | `Fork should contain at least two branches` | ⭐ **1/1** |
| SysML Semantics | STM missing Regions | `Region contains at least one InitialState and State` | 13/20 |
| SysML Semantics | STM missing PseudoState | `STM must contain InitialState and FinalState` | ⛔ **1/5** |
| SysML Semantics | ACT normal nodes as ActivityFinalNode | `ActivityFinal is a special node` | ⛔ **0/1** |
| SysML Semantics | ACT missing ReduceActions | `Use ReduceAction to express loops` | ⛔ **0/1** |
| SysML Semantics | ACT meaningless ActivityPartitions | `No explicit prompt not to use ActivityPartitions` | ⭐ 1/1 |
| SysML Semantics | SD missing DestructionOccurrenceSpecification | `The termination of Message should use DestructionOccurrenceSpecification` | ⛔ **16/44** |
| Req. inconsistency | STM Missing State or Transition | `Don't miss out State in requirements` | ⛔ **2/7** |
| Req. inconsistency | STM Incorrect Transition | `Pay attention to the rationality of the State between Traditions` | ⛔ **0/6** |
| Req. inconsistency | STM Missing Final State | `Don't miss out Final State` | 3/5 |
| Req. inconsistency | STM Missing Composite State | `Use composite states for complex state` | 4/5 |
| Req. inconsistency | ACT Missing ActivityNode | `Don't miss out Activity in requirements` | ⭐ **8/8** |
| Req. inconsistency | ACT Incorrect Node Placement | `Follow SysML layout and flow` | ⭐ **3/3** |
| Req. inconsistency | ACT Incorrect Parallelism | `Use Fork/Join/concurrent regions correctly.` | ⛔ **0/3** |
| Req. inconsistency | ACT Incorrect Use of Domain Terminology | `Use precise domain terms in requirements` | ⭐ **2/2** |
| Req. inconsistency | ACT Missing InitialNode | `Don't miss out InitiaNode` | ⭐ **2/2** |
| Req. inconsistency | ACT Extra ActivityNode | `Don't over-design` | ⭐ **9/9** |
| Req. inconsistency | SD Incorrect Messages type | `The message type should meet the requirements and spec` | ⛔ **12/45** |
| Req. inconsistency | SD Incorrect Messages interaction sequence | `Ensure correct message order.` | ⛔ **8/28** |
| Req. inconsistency | SD Incorrect CombinedFragment | `CombinedFragment should meet the requirements and spec` | ⛔ **1/13** |
| Req. inconsistency | SD Missing Messages | `Include all necessary messages.` | ⛔ **2/6** |
| Req. inconsistency | SD Missing Lifeline | `Include all correct lifelines.` | ⛔ **0/5** |
| Req. inconsistency | SD Incorrect Lifeline | `Include all correct lifelines.` | ⛔ **0/3** |

⭐ **我方复算（⛔ 论文未列这些中间量）：** ⭐ 格式 `35/37 = 94.59%`（micro）· 语法 `22/25 = 88.00%` · 语义 `31/72 = 43.06%` · 需求一致性 `56/150 = 37.33%`（⭐ STM `9/23 = 39.13%` · ACT `24/27 = 88.89%` · SD `23/100 = 23.00%`）。⭐ **四个 micro 分子分母与 §1 自报的 `35/37 · 22/25 · 31/72 · 56/150` 逐位一致 ✅。**

⭐⭐ **而论文正文引的百分数全是 macro（逐规则平均），⛔ 不是 micro** —— ⭐ 我方复算：⭐ 语义 macro `= 36.89%` ✅（⭐ 与论文 §6.4 逐位对上）· ⭐ STM macro `= 42.14%` ✅ · ⭐ ACT macro `= 83.33%` ✅ · ⛔ **SD macro `= 16.04%`，⛔ 而论文写 `16.67%` ✗**（→ F §1）。

⭐⭐⭐ **这一格最要紧的三条读数：**

1. ⭐⭐ **「反馈有效性」按层次断崖：⭐ 句法 88–95% → ⛔ 语义 37–43%。⛔ 落差约 `2.2×`。**
2. ⛔⛔ **有 6 条规则解决率恰好为 `0`**（⭐ `ACT ActivityFinalNode 0/1` · `ACT ReduceActions 0/1` · `ACT Incorrect Parallelism 0/3` · `STM Incorrect Transition 0/6` · `SD Missing Lifeline 0/5` · `SD Incorrect Lifeline 0/3`）。⭐⭐ **注意 `STM Incorrect Transition 0/6` 与 `ACT Incorrect Parallelism 0/3` 这两条 —— ⭐ 它们都是「语义对不对」而非「结构缺没缺」，⛔ 而祈使句式反馈对它们的收益是精确的零。**
3. ⭐⭐ **规则文案的形态与解决率强相关（⭐ 我方观察，⭐ 标 S）：⭐ 凡是「点名缺了哪个具体元素类型」的规则（`Don't miss out Activity` 8/8 · `Don't miss out InitiaNode` 2/2 · `Don't over-design` 9/9 · `Do not use non-existent elements` 30/30）解决率接近满分；⛔ 凡是「要求判断合理性」的规则（`Pay attention to the rationality...` 0/6 · `...should meet the requirements and spec` 1/13、12/45）解决率接近零。** ⭐ 依据是上表 29 行的分布，⛔ 论文自己没做这个切分。

#### ⚠️ 论文自己给的机制解释（⛔ 两句，⭐ 都对我们直接有用）

⭐ **§6.4 逐字（M）：**

> "**As rule complexity increases, LLMs may lose focus on the original requirements, and fixing one issue can introduce new ones.**"

⭐⭐ **这一句里有两个独立发现，⛔ 不要混：**

1. ⛔ **「规则一多，模型就丢开原始需求」** —— ⭐⭐ 这是**隧道视野**的独立外部观察。⭐ 与 [sosym2026-state-machine-consistency.md](./sosym2026-state-machine-consistency.md) 的 "the LLM tends to **exclusively focus on these rules, thus ignoring other consistency aspects**" 是**同一个现象的第二次独立报告**，⭐ 也与我们 v46 `occupancy_after` 的 `nl_cue` 把模型从 `edge_declared` 引开（⛔ 324 格里 `edge_declared` 被问 **0.0%**）同源。⭐⭐ **三处独立观察，⭐ 分属三个团队。⭐ 这已经够写成一条一般性发现了。**
2. ⛔ **「修好一个引入一个」（regression）** —— ⭐ 这一条 SoSyM 那篇**没有**。⚠️ ⭐ 而它对我们是直接可用的：⭐ 我们 v46 观察到「第 3–5 轮零收益」，⛔ 但没有拆开「净零 = 没修好」还是「净零 = 修好的与新引入的相抵」。⭐⭐ **这篇提供了第二种机制的外部证据，⛔ 说明我们那个「净变化 ≈ 0」值得拆开重算。**

⭐ **§6.1 还有一条对语义层的归因（M，逐字）：**

> "This highlights **the difficulty of encoding deep semantic understanding into rule-based prompts**, as current LLMs struggle with this level of abstraction."

### B5 · ⭐ 中间表示

⚠️⚠️ **这篇有三层中间表示，⭐ 全部闭合，⛔ 但没有一层是 LLM 选的。⛔ 三层必须分开谈。**

| | ⭐ ① 缺陷类型学 | ⭐ ② 55 条 SysML 语义清单 | ⭐ ③ 29 条 model-checking 规则目录 |
| :-- | :-- | :-- | :-- |
| 有无 | ⭐ 有 | ⭐ 有 | ⭐ 有 |
| 形态 | ⭐ **缺陷类型学**（4 大类 → 29 子类） | ⭐ **谓词族 / 规约条款清单** | ⭐ **规则目录**（⭐ 每条一句自然语言祈使句） |
| ⭐ **是否闭合** | ⭐ **闭合** | ⭐⭐ **闭合** | ⭐ **闭合** |
| ⭐ **谁定的** | ⛔⛔ **从被评测语料本身归纳**（⭐ Phase-I 实测 → 归类） | ⭐ **预编目录，⭐ 从 UML/SysML 规约抄** | ⛔ **作者按 ① 逐类手写** |
| ⭐ **谁选类** | ⛔ **PlantUML checker（自动）＋ 人（手工比对）** | ⛔ **人**（⭐ 逐条对着清单查） | ⛔ **机械按命中类型注入** |
| ⛔ **LLM 参与选类** | ⛔ **无** | ⛔ **无** | ⛔ **无** |

#### ⭐⭐ ② 的 55 条语义清单 —— ⭐ **本轮实取到了，⛔ 论文正文只在脚注里提了一句**

⭐ 论文脚注 2 逐字（M）："**Detailed grammar and semantics are available in the open-data resource.**"

⭐⭐ **我方实取结果**（⭐ `expresults.xlsx` 的 `SysML Grammar &Semantic` 工作表，⭐ **56 行 = 1 表头 ＋ 55 条**，⭐ 7 列 `Type / Grammar / Source / Elements / Sub Elements / Semantic / Note`）：

| ⭐ 分布 | 条数 |
| :-- | :-: |
| ⭐ **STM** | ⭐ **18** |
| ⭐ **ACT** | ⭐ **8** |
| ⭐ **SD** | ⭐ **29** |
| ⭐ **合计** | ⭐ **55** ✅ |

⭐⭐ **关键事实：⭐ `Source` 列（⭐ 合并单元格，⭐ 前向填充后）55/55 全部有 UML/SysML 规约条款号** —— ⭐ 例如 STM 段是 `14.2.3.2`（Regions）· `14.2.3.3`（Vertices）· `14.2.3.4`（State）· `14.2.3.5`（ConnectionPointReference）· `14.2.3.6`（FinalState）· `14.2.3.7`（Pseudostate）· `14.2.3.8`（Transitions）；⭐ ACT 段是 `15.2.3.2`–`15.2.3.7`；⭐ SD 段是 `17.*` 与 `8.5.3.2` / `8.6.*`。

⭐ **STM 那 18 条逐条**（⛔ 抄要素名，⛔ 不抄整段语义描述）：`Regions` · `Vertices` · `State`（⭐ simple / composite / submachine，⭐ 3 条）· `ConnectionPointReference` · `FinalState` · `Pseudostate`（⭐ initial / deepHistory / shallowHistory / join / fork / junction / choice / entryPoint / exitPoint / terminate，⭐ 10 条）· `Transitions`。

⚠️ ⭐ **`Note` 列有 4 条标 `No Support in PlantUML`**（⭐ 全在 ACT 段：`ObjectNodes` · `ObjectFlow` · `Variables` · `ActivityParameterNode`）。⭐⭐ **即它自己标出了「工具表达不了、所以查不了」的那 4 条 —— ⭐ 这个做法值得学**（⭐ 与我们 `ground_truth_limitations.md` 同一性质）。

#### ⭐⭐ 与我们 19 条谓词的对照（⛔ 这一格最有价值）

| 维度 | ⭐ 它（55 条语义 ＋ 29 条规则） | ⭐ 我们（19 条谓词） |
| :-- | :-- | :-- |
| 闭合性 | ⭐ 闭合 | ⭐ 闭合 |
| ⛔ **谁选** | ⛔⛔ **人 ＋ 工具** —— ⭐ 检测端由人逐条比对 55 条、由 PlantUML checker 报格式，⛔ 然后规则机械注入。⛔ **LLM 只消费，⛔ 不选** | ⭐⭐ **LLM 在每条需求上自动选** |
| ⭐⭐ **出处分级** | ⭐⭐ **55/55 全部挂 UML/SysML 规约条款号** —— ⛔ 即**全部是「② 元模型定义性」**，⛔ **没有一条是「① 领域文献证据」，⛔ 也没有一条是「③ 无外部依据」** | ⭐ **① 有领域证据 12 · ② 元模型定义性 6 · ③ 无外部依据 1**（→ [../provenance/](../provenance/)） |
| ⛔ **29 条规则的出处** | ⛔⛔ **无出处 —— ⭐ 全部从 Phase-I 的实测幻觉倒推手写**（⭐ 见下方） | ⭐ 三类分级 |
| ⭐ 输出粒度 | ⛔ 反馈是**自然语言祈使句**，⛔ 不挂规则 ID、⛔ 不给定位、⛔ 不给反例 | ⭐ 断言脚本挂谓词，⭐ 可机械求值 |
| ⭐ 覆盖率自陈 | ⭐ 4 条标「PlantUML 表达不了」 | ⚠️ 我们实测只用到 15/19 |

⭐⭐⭐ **这一格的三条结论：**

1. ⭐⭐ **`55/55 挂规约条款` 是一个比 SoSyM 那篇更严的出处形态** —— ⭐ SoSyM 2026 的 38 条里只有 8 条挂文献/标准（⭐ 见 [sosym2026-state-machine-consistency.md](./sosym2026-state-machine-consistency.md) B5），⛔ 而这篇的 55 条**逐条**挂 UML/SysML 条款。⛔ **但要注意它挂的全是「规约怎么说」，⛔ 没有一条挂「领域文献为什么这么要求」** —— ⭐ 即它的出处轴只有我们三类里的第 ② 类。
2. ⛔⛔ **它的 29 条规则完全无出处** —— ⭐ 它们**不是**从规约推的，⛔ 而是从「Phase-I 哪里出错了」倒推手写的（⭐ §6 逐字："Based on the findings of RQ1, we introduced model-checking rules **to address the hallucinations identified in Tables 8–10.** **Each rule targets a specific hallucination type**"）。⛔⛔ **这是「引入动机 = 某个样本没做对」的教科书形态**，⛔ 而本仓库 [CLAUDE.md](../../../../../CLAUDE.md) §3.5.-1 正是为这件事设的审查。⭐ **详见 E §2 第 1 条。**
3. ⛔⛔ **它对「闭合词表 ＋ LLM 自动选」这个组合仍然给不出先例** —— ⭐ 又是一票**不算**。⚠️ ⭐ 连同 SoSyM 那篇，⭐ 本轨目前已有**两票**「闭合但人/规则选」，⛔ **零票**「闭合且 LLM 选」。

### B6 · 模型

⭐⭐ **6 个模型，⭐ 这是它相对 TTool-AI 那条线（⛔ 只用 OpenAI）的明显优势。** ⭐ Table 5 逐字抄：

| Type | Name | Version | Context | Publisher |
| :-- | :-- | :-- | :-- | :-- |
| Close-source | GPT-4 | `GPT-4-Turbo` | 128,000 tokens | OpenAI |
| Close-source | GPT-4o | `GPT-4o-2024-11-20` | 128,000 tokens | OpenAI |
| Close-source | Kimi | `Moonshot-v1` | 128,000 tokens | Moonshot AI |
| Close-source | Claude | ⛔ **`Claude 3 Haiku`** | 200,000 tokens | Anthropic |
| Open-source | Llama | `Llama3.1` | 128,000 tokens | Meta AI |
| Open-source | DeepSeek | `DeepSeek-v3` | 128,000 tokens | deepseek |

⭐ **配置（M，§4.5 逐字）**："Closed-source models were accessed via **official APIs**, and open-source models via **Nvidia's API**. To ensure a fair comparison, **all models were configured with identical parameters (e.g., temperature = 0).** Although Claude 3 Haiku supports a 200,000-token context window, our experiments remained within this limit to eliminate context length as a confounding factor."

⭐ Llama 的具体端点从参考文献 [51] 可读出是 `llama-3_1-nemotron-70b-instruct`（⭐ NVIDIA build 页），⛔ 论文正文只写 `Llama3.1`。

⚠️⚠️⚠️ **B6 这一格有一个必须指出的方法学缺陷：⛔⛔ 用 `Claude 3 Haiku` 代表「Claude」。** ⭐ Haiku 是 Claude 3 家族里**最小、最便宜**的一档，⛔ 而同代还有 Sonnet 与 Opus。⭐ 论文自称"all representing the **latest versions** from major providers"（M，§4.5），⛔ **但对 Anthropic 取的是家族最弱档，⛔ 对 OpenAI 取的是 GPT-4-Turbo/4o（旗舰档）**。⛔⛔ **这使跨厂商对比系统性偏向 OpenAI，⛔ 且论文未讨论这一点。** ⚠️ ⭐ 讽刺的是 §5.3 还说 "models showing stronger inductive ability(e.g., **Claude**) performing better" —— ⭐ 即**最弱档的 Claude 在 STM 上仍然表现较好**，⛔ 那反而说明取样偏差把 Claude 低估了。

⚠️ **X1 的代际折扣在这篇上要打**：⭐ 全部数字来自 **2024 年底代**（`GPT-4o-2024-11-20` 是最新的一个）。⛔ 按 X1 的结论（SOTA 与上一代不是一个量级），⛔ **它的绝对数字参考价值要打折**。⭐⭐ **但「反馈收益按层次断崖」这个结构性结论受代际影响小**，⭐ 因为 SoSyM 那篇用 **GPT-5.1** 仍然观察到同类的语义盲区。

### B7 · ⭐ 确定性成分

| 环节 | 是什么 | ⭐ 自动还是人 |
| :-- | :-- | :-- |
| ⭐ PlantUML 格式检查器 | ⭐ PlantUML 自带的 model checker | ⭐ **自动**（⛔ 全流程唯一的自动检查器） |
| ⭐ RAG 检索 | ⭐ 取 PlantUML 格式说明 ＋ SysML v1.6 规约文本 | ⭐ 自动 |
| ⭐ prompt 模板装配 | ⭐ 五段拼装（Role · I · Req · S · E） | ⭐ 自动 |
| ⭐ F1 计算 | ⭐ 按 grammar point 数 TP/FP/FN（⭐ `GP_t = |n_t| + |e_t|`） | ⭐ 半自动 |
| ⛔ **SysML 语法检查器** | ⛔⛔ **不存在 —— ⭐ 人工** | ⛔ 人 |
| ⛔ **SysML 语义检查器** | ⛔⛔ **不存在 —— ⭐ 人工对着 55 条清单** | ⛔ 人 |
| ⛔ **模型检查器 / 求解器** | ⛔⛔ **不存在** | — |
| ⛔ **仿真器** | ⛔⛔ **不存在** | — |

⭐⭐ **论文自己把这件事说得非常清楚（M，§4.4 逐字）：**

> "Although the selected PlantUML tool is user-friendly and complies with the SysML v1.6 specification, **it lacks built-in capabilities for SysML syntax and semantic checking. Consequently, all validations must be performed manually, potentially limiting the comprehensiveness and automation of the research.** Future studies are recommended to utilize more powerful SysML modeling tools or **develop specialized automated model-checking tools** to enhance the comprehensiveness and accuracy of evaluations."

⭐⭐⭐ **B7 这一格的核心发现，⛔ 也是这篇对 M1 最要紧的一条：**

⭐⭐ **它整篇论文的标题里有 "model checking"，⛔ 但它一个模型检查器都没有。** ⭐ 它所谓的 "model-checking rules" 是**人工核对清单 ＋ 自然语言祈使句反馈**。⭐⭐ **于是它的核心结论「反馈对语义层无效」是在「没有 sound oracle」的前提下得出的** —— ⛔ **这恰恰不能证明「有了 sound oracle 也无效」。**

⚠️⚠️ ⭐ **这一点决定了怎么引它。⛔ 正确的引法是：「已有工作在缺乏可靠判定装置的条件下，观察到基于规则文本的反馈对语义层收益极低，并明确指出需要反例与仿真轨迹级的反馈」。⛔ 错误的引法是：「已有工作证明反馈循环对语义缺陷无效」——⛔ 那是过度概括，⛔ 且会顺手否掉我们自己的 pyfcstm 路线。**

---

## C. 实验

| 字段 | 值 |
| :-- | :-- |
| `baseline` | ⛔⛔ **无外部 baseline。** ⛔ 无人类对照臂、⛔ 无非 LLM 方法臂、⛔ 无前人方法复现臂。⭐ **唯一的「对照」是 6 个 LLM 互比 ＋ Phase-I vs Phase-II 自比**。⚠️ ⭐ 参考模型是人建的，⭐ 所以人是**天花板**（F1 的分母），⛔ **不是对照臂** |
| `dataset` | ⭐ **公开语料 107 行**（⭐ 声称 36 ACT / 36 STM / 35 SD，⭐ 5 个领域：equipment manufacturing 29% · rail transportation 24% · IoT 19% · aerospace 19% · military 9%，⭐ 23 个案例系统）。⭐ **实验用 30 个**（⭐ §4.3："We divided the dataset into three categories based on behavior model types and **randomly selected ten models from each**"）。⭐⭐ **我方实取核实：三个 Results 表各含恰好 10 个 distinct `Model Name` × 6 LLM = 60 行 ✅，⭐ 即 Phase-I 共 `30 × 6 = 180` 次生成** |
| ⛔ **数据集建设成本** | ⭐ **524 小时**（M，§1 逐字："After **524 hours** of collection and processing by modeling professionals, we compiled a dataset of 107 validated models"）。⭐ 两个小组：`G_Search`（4 本科 ＋ 1 硕士）· `G_Model`（1 本科 ＋ 2 硕士 ＋ 2 博士），⭐ 每人 100+ 小时建模经验 |
| ⭐ **分母怎么定的** | ⚠️⚠️ ⭐ **三套分母，⛔ 口径不同，⛔ 论文不标注**：⭐ ① **幻觉解决率**的分母 = Phase-I **已检出**的幻觉条数（284）→ ⛔ **无 recall 分母**；⭐ ② **F1** 的分母 = grammar point 数（⭐ `GP_t = |n_t| + |e_t|`）；⭐ ③ **Acc_P** 的分母 = PlantUML 句子数，**Acc_S** 的分母 = GP 数 |
| `metrics` | ⭐ `T_G`（生成时间，秒）· `Acc_P`（PlantUML 格式准确率）· `Acc_S`（SysML 语法准确率）· `F1`（⭐ `2TP/(2TP+FN+FP)`，⭐ 按 GP 匹配）· ⭐ 附加 `Acc_S@NS` / `Acc_S@FC`（⛔ 见 F §3）。⛔⛔ **无任何 `@k` 口径** —— ⭐ `temperature=0` 单次跑 |
| ⭐ `judged_by` | ⛔⛔ **作者自己人工，⛔ 无第三方、⛔ 无标注者间一致性、⛔ 无 $\kappa$、⛔ 无一致率。** ⭐ 逐字：SysML 语法 "**we manually compare each item against the standard** and record the errors"；SysML 语义 "**we manually check the model against 55 semantics** and log violations"。⭐⭐ **但 —— ⭐ 逐条判定台账公开了**（→ D 节），⛔ 这一点比 [sosym2026-state-machine-consistency.md](./sosym2026-state-machine-consistency.md) 强（⭐ 那篇的判定锁在 TTool `.xml` 里） |
| `human_baseline` | ⛔ **无对照臂。** ⚠️ ⭐ 但 §5.5 有一句拿人当标尺的话（M，逐字）："ACT performs the best, **approaching human-level quality**" —— ⭐ 依据是 F1 = 97.49% 对人建参考模型，⛔ **不是与人重新建模做对照实验** |
| `runs` | ⛔⛔ **每格一次，⛔ 报单次，⛔ 无方差、⛔ 无重复采样。** ⭐ `temperature = 0` ＋ greedy decoding，⛔ 论文把消除随机性当优点 |
| ⭐ `adverse_results` | ⭐⭐ **不利结果就是论文的主结论 —— ⭐ 见下方专节** |

### ⭐ Phase-I 的其它数字（⛔ 顺手抄下）

- ⭐ **生成时间**：⭐ "behavioral model generation typically takes **6–15 seconds** in real-world scenarios. **Over 70% of models were generated within 10 seconds.**"（M，§5.1）
- ⭐ **Phase-II 的时间倍数**：⭐ `G_T-II / G_T-I` 的（最小比, 最大比）—— ⭐ **STM (2.72, 7.67)** · **ACT (4.05, 4.81)** · **SD (4.00, 4.31)**
- ⭐ **Phase-II 后的 Acc**：⭐ "For `Acc_P`, STM and SD generation achieved **100%** across all models." ⭐ `Acc_S` 在 STM/ACT 近 100%，⛔ 但 SD 上仍有变异（⭐ GPT-4o 掉到 **93.11%**，⭐ GPT-4 达 **100%**，⭐ Kimi **83.36%**）
- ⭐ **Phase-II 后的 F1 改善举例**：⭐ "**GPT-4o's F1-score improved from 49.79% to 74.11% for SD.**" ⭐ 另称 Kimi 与 Claude 在 SD 上改善最大

### ⭐ 幻觉成因（⛔ §5.4 三条，⭐ 逐字抄）

> "(1) **Insufficient understanding of requirements**: LLMs may misinterpret key points, resulting in inaccurate models or irrelevant elements. (2) **Increased error probability with model complexity**: complex models require better context tracking and constraint handling, leading to higher error rates, particularly in SD tasks. (3) **Limited logical reasoning**: LLMs struggle to translate informal natural language requirements into formal models, **especially in complex scenarios involving concurrency, conditional branches, and state transitions.**"

⚠️ ⭐ 第 (3) 条点名 **concurrency** —— ⛔ 对我们是界外，⭐ 但值得记住：⭐ **它把并发列为最难的一类，⛔ 而我们把并发排除在建模对象外。** ⭐ 这在 Limitations 里可以用来说明「我们的边界不是回避难点，而是问题定义使然」，⛔ 但**必须按 [README.md](../README.md) §3 的防火墙先回 L1 过门**。

### ⭐⭐ `adverse_results` 专节 —— ⭐ 它怎么写不利结果（⛔ 我们的 −15.82pp 可直接借鉴）

⭐⭐ **形态与 SoSyM 那篇不同，⭐ 而且更彻底：⭐⭐ 不利结果不是「附带承认的缺陷」，⛔ 而是「论文的主要贡献」。**

1. ⭐⭐ **摘要最后三句全是不利结果** —— ⭐ "insufficient for addressing deeper semantic gaps" ＋ "requires advanced strategies" ＋ "model-checking in LLM-based generation is **costly**"。⭐⭐ **它把「我们的方法没解决问题」写进了摘要，⭐ 并把这件事本身当成贡献（⭐ 「clarifying current limitations and pointing to future research directions」）。**
2. ⭐ **自我归因到自己的机制，⛔ 不归因到模型** —— ⭐ 逐字："**One key reason is the lack of an optimal model-checking feedback mechanism in our study.**" ⭐⭐ **注意 `in our study` —— ⭐ 它明确把责任放在自己的实验设计上，⛔ 不说「LLM 不行」。**
3. ⭐ **主动报成本劣势** —— ⭐ 时间涨 `2.72×`–`7.67×`，⭐ 且明说 "**indeed time-consuming**"。⚠️ ⭐ 我们的 `212.6×` 也应当这么写。
4. ⭐ **主动报「修一个坏一个」** —— ⭐ "fixing one issue can introduce new ones"。⛔ 这是自曝方法的结构性缺陷。
5. ⭐ **Threats 三节齐全**（Construct / Internal / External），⭐ 且逐条给了缓解措施。⭐ 其中 Internal Validity 主动承认 **需求是作者逆向补写的、主观**（M，逐字："For models without explicit requirements, **we manually created them, which is subjective.** To reduce bias, we cross-checked the reconstructed requirements for consistency with the models."）。

⭐⭐ **形态总结：⭐⭐ 「不利结果 → 写进摘要 ＋ 当成贡献 ＋ 归因到自家机制而非模型 ＋ 主动报成本 ＋ 主动报回归 ＋ Threats 三节」。** ⭐ 这比 SoSyM 那篇更进一步：⭐ **SoSyM 是「坦白承认」，⭐ 这篇是「以此立论」。** ⚠️ ⭐ 对我们 `−15.82pp` 而言，⭐ **这篇提供的正是我们需要的那个写法** —— ⭐ 不是「我们的方法比基线差」，⭐ 而是「我们量化了一个反馈机制在语义层的收益上限，⛔ 并定位到它缺什么」。

---

## D. 资产

⭐⭐ **本轮我实际把三个 Google Sheets 全下载了，⛔ 不只是核 HTTP 200。⭐ 下面每一行的「核验证据」都是实测。**

| 资源类型 | 状态 | URL / 路径 | ⭐ 核验证据 |
| :-- | :-: | :-- | :-- |
| ⭐ 论文全文 | ⭐ **🟢** | [`10.1145/3755881.3755926`](https://doi.org/10.1145/3755881.3755926) · [本地 PDF](../../../../baselines/llms_emp/paper.pdf) | ⭐ **CC-BY 4.0 开放获取**（⭐ 论文首页逐字："This work is licensed under a **Creative Commons Attribution 4.0 International License**"；⭐ ACM 页另标 "Open Access Support provided by: Beihang University"）。⚠️ ⛔ **`verify_assets` 对 `doi.org` 得 `HTTP 403 · HTTPError 403`**（⭐ ACM DL 的 Cloudflare）—— ⛔ **非 DOI 不存在**。⭐ 本仓库已有本地 PDF（5,204,902 B）＋ `paper_content.txt`（1189 行，12 页全文） |
| ⛔ **实验代码** | ⛔ **⚪** | — | ⛔ **不存在。** ⭐ 论文全文无 "code available"、无仓库链接、无 artifact 声明。⭐ Drive 里三个工作簿全是数据与结果表，⛔ **无生成 / 重生成 / RAG / 评测脚本**。⭐ 与 [`baselines/llms_emp/ASSETS.md`](../../../../baselines/llms_emp/ASSETS.md) 的记录一致（⭐ 该文件记 🟠「未发现公开仓库」，⛔ 本卡按「原文明确未提供」判 ⚪） |
| ⭐⭐ **数据集 / Benchmark** | ⚠️ **🟡** | [Drive 文件夹](https://drive.google.com/drive/folders/10eo8KDqlBlkQZxPpPCB7R3-aBQZ7Rsm6) · `Dataset` 工作表 | ⭐ `verify_assets`：**`HTTP 200 · text/html`**。⭐ **我方实取**：Drive 文件夹含 **3 个 Google Sheets** —— `Dataset`（file id `1UtgoNHBAT7sRAc_lxVR1r0DB9c3ViLR_2LpzIYE9Tl4`）· `Experiment Results`（`1Fm60ulxlSz60FtfwQK4unWLBLms0w5sBHEyNhkpNstY`）· `ESE Expriment Results`（`17gpwpWhjFxVtq2o-eoNfZdWZ8pVYz76fR1jr8H7qo94`）。⭐ 经 `export?format=xlsx` 全部 `HTTP 200`（36,392 / 11,569,836 / 2,075,406 B）。⭐ `Dataset` 单工作表 `108 × 6`（⭐ 1 表头 ＋ **107 数据行**），⭐ 列 `Model Name / Model Source / Requirements Description / PlantUML` ＋ 2 个无名列（⭐ 一列放 `selected` 标记、⭐ 一列放 `act` 注记）。⛔⛔ **判 🟡 而非 🟢 的理由见下方「资产终裁」** |
| ⭐⭐ **逐条判定台账**（⛔ ground truth） | ⭐⭐ **🟢** | ⭐ `Experiment Results` → `Hallucinations` 工作表 | ⭐⭐ **这是本篇最有价值的资产。** ⭐ **我方实取**：`Hallucinations` 工作表 **298 行 × 7 列**，⭐ 列为 `Type / Model Source / LLMs / Format Hallucinations / Resolved / Taxonomy / How to fix it`。⭐ 逐行是**一条幻觉实例**，⭐ 含原始错误文本、⭐ 归类、⭐ 修法。⭐⭐ **独立对账通过**：⛔ 298 行 = **284 条实例** ＋ 3 行重复表头 ＋ 11 行空白；⭐ **`Resolved == yes` 恰好 `144` 条**，⭐ 与论文 `35+22+31+56 = 144` **精确一致 ✅**；⭐ `144 yes + 140 no = 284` ✅，⭐ 与论文 `37+25+72+150 = 284` **精确一致 ✅**。⭐ 另有 `Hallucinations Summary` 工作表（`107 × 7`）给逐类汇总与百分比 |
| ⭐⭐ **55 条语义清单** | ⭐⭐ **🟢** | ⭐ `Experiment Results` → `SysML Grammar &Semantic` 工作表 | ⭐ **我方实取**：`56 × 7`（⭐ 1 表头 ＋ **55 条**）。⭐ 列 `Type / Grammar / Source / Elements / Sub Elements / Semantic / Note`。⭐ **`Source` 列前向填充后 55/55 全部有 UML/SysML 规约条款号**。⭐ 分布 **STM 18 · ACT 8 · SD 29**。⭐ `Note` 列 4 条标 `No Support in PlantUML`。⭐⭐ **这就是论文脚注 2 承诺的那份东西，⭐ 确实在** |
| ⭐ 实验结果细则 | ⭐ **🟢** | ⭐ `Experiment Results` → `STM Results` / `ACT Results` / `SD Results` | ⭐ **我方实取**：`STM Results` `61 × 37` · `ACT Results` `73 × 42` · `SD Results` `61 × 36`。⭐ 各含恰好 **10 个 distinct `Model Name` × 6 个 `LLMs`**。⭐ 列覆盖 Phase-I 与 Phase-II 两套：`Generation Time` · `PlantUML Accuracy(+Rate)` · `SysML Grammar Accuracy(+Rate)` · `True/False Positive` · `False Negative` · `F1 Score` · `Format Hallucinations` · `Result with Format Checking` · `Resolved` · `SysML Grammar Hallucinations` · `Result with Grammar Checking` · `Semmantic Hallucinations`（⚠️ 原文拼写如此）· `Result with Semantic Checking` · ⭐ **第二套 `TP/FP/FN/F1`（`.1` 后缀）**。⭐⭐ **即逐样本逐模型逐阶段的原始分全在** |
| ⭐⭐ **prompt 是否公开** | ⭐⭐ **🟢** | ⭐ 三个 Results 工作表的 `Prompt` 列 | ⭐⭐ **公开。** ⭐ **我方实取**：三个 Results 工作表都有 `Prompt` 列。⭐ 另经本仓库冻结的 [human-review parquet](../../../../discussions/2026-04-15-01-03-52-AI-讨论-baselines双绿数据集下载解析与parquet化.assets/llms_emp_human_review.parquet) 复核：**192 行 `prompt_text` 全部非空**（`notna = 192`，`len > 0 = 192`）。⛔ 论文正文只给 Figure 4 一张 ACT prompt 截图，⭐ **但工作簿里是逐样本完整文本** |
| ⛔ Artifact / 复现包 DOI | ⛔ **⚪** | — | ⛔ **不存在。** ⭐ 无 Zenodo / OSF / 4open DOI，⛔ 无版本快照。⛔⛔ **只有 Google Drive —— ⭐ 结构与权限都可能漂移，⛔ 且无 revision 可定位** |
| ⭐ 本仓库冻结副本 | ⭐ **🟢** | ⭐ [`discussions/...parquet 目录`](../../../../discussions/2026-04-15-01-03-52-AI-讨论-baselines双绿数据集下载解析与parquet化.assets/) | ⭐⭐ **SHA-256 三份逐位复核通过 ✅**：`llms_emp_raw_samples.parquet` = `69e5123174f976bf7504eaa334e0670da22b2e0c67329c57539b3866dfe5b045`（107 行）· `llms_emp_complete_samples.parquet` = `d8c0dca59c650149c7c16e433fc54440fc72509c82d57676ca6238f2182fdf2e`（98 行）· `llms_emp_human_review.parquet` = `7b54b06ead32e0a5b6c6d4f2244d11a8e2439c64ad421f01a1b8a9175f16a427`（192 行）。⭐ 三者与 [`baselines/llms_emp/ASSETS.md`](../../../../baselines/llms_emp/ASSETS.md) 记录的哈希**逐位一致** |

### ⭐⭐ 资产终裁 —— ⛔ **数据集判 🟡，⭐ 理由是实测组成与论文声明对不上**

⭐⭐ **这是本卡唯一推翻既有记录的一处。** ⭐ [`baselines/llms_emp/ASSETS.md`](../../../../baselines/llms_emp/ASSETS.md) 把数据集记为 **🟢**，⭐ 并写「107 个 SysML 行为模型，含 36 activity、36 state machine、35 sequence diagrams」。⛔⛔ **我方实取原始 `Dataset` 工作表后发现：那 107 行里只有 65 个不同的条目。**

⭐ **实测证据（⛔ 直接在作者公开的 `Dataset` 工作表上算，⛔ 不是在我们的 parquet 上算）：**

| 度量 | 值 |
| :-- | :-: |
| ⭐ 数据行数 | ⭐ **107** ✅（⭐ 与论文一致） |
| ⛔ **distinct `Model Name`** | ⛔ **65** |
| ⛔ **distinct (`Requirements Description` ＋ `PlantUML`)** | ⛔ **65** |
| ⛔ **重复组数** | ⛔ **35**（⭐ 28 组出现 2 次 · **7 组出现 3 次**） |
| ⛔ **冗余行数** | ⛔ **42** |
| ⛔ 缺 `PlantUML` 的行 | ⛔ **9** |
| ⛔ 缺 `Requirements Description` 的行 | ⛔ **1** |
| ⭐ 去重后有输出的条目 | ⛔ **61** |

⭐ **重复是成块的，⛔ 不是零散的** —— ⭐ 例如 `Multi-physics coupling activity diagram of airborn...` 出现在数据区第 `15 / 64 / 99` 行；`UAV swarm state machine diagram` 在第 `18 / 67 / 102` 行；`Air Defense System State Machine Diagram` 在第 `20 / 69 / 104` 行。⭐⭐ **即约第 15–47 行整块在第 64–94 行重现，⭐ 部分再在第 99–106 行重现第三次。**

⛔⛔ **两个排除的替代解释：**

1. ⛔ **不是我们的 parquet 化脚本的问题** —— ⭐ 我**重新从作者 Drive 下载了原始 `Dataset` 工作表**（`export?format=xlsx`，`HTTP 200`，36,392 B）并在**原始 xlsx 上**复算，⭐ 得到完全相同的 65 / 35 / 42。
2. ⛔ **不是多工作表拼接** —— ⭐ `Dataset` 工作簿只有**一个**工作表（`sheet_names = ['Dataset']`），⭐ 行号 `0`–`106` 连续无缺口。

⭐ **另一处旁证：`Model Source` 列同时出现 `A Practical Guide to SysML`（10 行）与 `Practical Guide to SysML`（5 行）** —— ⭐ 同一本书两种写法，⭐ 与成块复制的痕迹吻合。

⭐⭐⭐ **裁定与后果（⛔ 这一段直接影响 N1b / M1）：**

1. ⛔⛔ **论文的第一条贡献（"We release a curated dataset of **107** SysML behavior models (**36 activity, 36 state machine, and 35 sequence diagrams**)"）与公开工件对不上。** ⭐ 工件里是 **65 个不同条目**，⛔ 其中 9 个无模型 → ⭐ **约 61 个可用条目**。⭐ Table 2 的列合计（36 / 36 / 35 = 107）我逐行验过是自洽的，⛔ **所以问题在工件，⛔ 不在 Table 2**。
2. ⚠️ **我不为它编一个能凑出 107 的解释。** ⭐ 两种可能都存在（⭐ ① 作者把 107 行当成 107 个模型、⛔ ② Drive 表被误传了重复块），⛔ **我无法判定是哪一种** → ⭐ 登记为 F §4。
3. ⭐⭐ **对 N1b / M1 的实际结论：⭐ 「36 个界内状态机可直接拿来用」这个预期要下调。** ⭐ 实取可用的 STM 条目在**去重后约 20–23 个**（⭐ 我方按 PlantUML 关键字判型：去重后 65 行里 `stm ≈ 20`；⭐ 我们 parquet 的推断口径给 `stm = 23`）。⛔⛔ **而且必须先去重、再逐样本过边界门**（⭐ 见 A 节 `boundary` 说明），⛔ **不能直接按 `diagram_type == "stm"` 取 38 行就用** —— ⛔ 那 38 行里含 42 个冗余行摊进来的重复。
4. ⛔⛔ **`diagram_type` 是我们推断的，⛔ 不是工件自带的。** ⭐ 原始 `Dataset` 工作表**没有图型列**（⭐ 只有一个无名列对 11 行标了 `act`）。⭐ 我方实测发现推断会出错：⭐ 有 **6 行**被判 `stm` 而其 `Model Name` 明写 activity（⭐ 如 `Robot activity diagram` · `Send signal activity diagram` · `Occupancy inspection activity diagram` · `Microwave Oven Control with entry and exit activity diagram`）。⛔⛔ **所以取 STM 子集前必须重新分型，⛔ 不能信现有 `diagram_type`。**
5. ⭐ **相比之下，判定台账与 55 条语义清单是干净的 🟢** —— ⭐ 它们与论文数字**精确对账**（144/144、284/284、55/55）。⭐⭐ **即：⭐ 这篇的「结果与判定」资产质量高于「数据集」资产质量。**

---

## E. 对 M1 的意义

### 1. ⭐ 可取之处

| # | 可搬的设计决定 | ⭐ 证据强度 |
| :-: | :-- | :-- |
| **①** | ⭐⭐⭐ **「反馈收益按层次断崖」是我们「修订机器零收益」的分层解释，⭐ 且有 29 条逐规则数据支撑。** ⭐ 句法层 `88–95%` vs 语义层 `37–43%`。⭐⭐ **可直接搬的动作：⭐ 把我们 v46 的修订收益也按「句法层（schema / 契约门）vs 语义层（谓词选取 / 断言构造）」拆开重算。** ⭐ 我们现在只有一个合并的「净变化 ≈ 0」，⛔ 而这篇说明那个 0 很可能是**句法层正收益与语义层零收益相抵**的结果 —— ⭐ 而这恰好与我们已观察到的「`convert` 内部契约重试是唯一净 `+1118` 条断言」吻合 | ⭐ **M**（⭐ Table 11 逐条 ＋ 我方复算） |
| **②** | ⭐⭐ **「修好一个引入一个」（regression）是我们没测过的机制。** ⭐ 逐字 "fixing one issue can introduce new ones"。⭐⭐ **可直接搬的动作：⭐ 我们的逐轮账目前只记「净变化」，⛔ 应当拆成「本轮新命中」与「本轮丢失原有命中」两栏。** ⛔ 若真有回归，⭐ 那么「第 3–5 轮零收益」的正确读法是「修与坏相抵」，⛔ 而不是「什么都没发生」—— ⛔ **两者对 M1 的含义完全相反** | ⭐ **M**（⭐ 原文明写机制；⛔ 但它自己也没给回归的量化数字 → 我方动作是 I） |
| **③** | ⭐⭐ **逐实例判定台账公开 ＋ 与论文数字精确对账。** ⭐ `Hallucinations` 298 行、`resolved=yes = 144` 与论文 `144` 逐位一致。⭐⭐ **这是本轮所有卡片里对账最干净的一篇。** ⭐ 我们的 574 位逐位判据 ＋ 288 簇裁定应当照这个形态发布：⭐ **一行一实例 ＋ 归类列 ＋ 是否解决列 ＋ 修法列**，⭐ 使外部审查者能独立重算主结果 | ⭐ **M**（⭐ 我方实取并对账） |
| **④** | ⭐⭐ **闭合清单逐条挂规约条款号（55/55）。** ⭐ 这是比 SoSyM 那篇（8/38 挂文献）更严的出处形态。⭐ **对我们的用处是校准而非模仿**：⭐ 它的出处**只有**我们三类里的第 ② 类（元模型定义性），⛔ 一条领域文献都没有。⭐⭐ **所以我们的 `① 12 · ② 6 · ③ 1` 在出处**维度**上比它宽（⭐ 我们有领域证据轴），⭐ 在**覆盖率**上比它窄（⛔ 19 vs 55）。⭐ 两条都可写** | ⭐ **M**（⭐ 我方实取 `Source` 列逐行核过） |
| **⑤** | ⭐ **主动标出「工具表达不了、所以查不了」的条目**（⭐ 4 条 `No Support in PlantUML`）。⭐ 与我们 [ground_truth_limitations.md](../../discover_matrix/docs/protocol/ground_truth_limitations.md) 同一性质，⭐ 且是已发表的先例 | ⭐ **M** |
| **⑥** | ⭐⭐ **不利结果的写法：⭐ 不是「坦白承认」，⭐ 而是「以此立论」。** ⭐ 摘要最后三句全是负面结论，⭐ 并把「厘清限制、指出方向」明写成贡献。⭐⭐ **我们的 `−15.82pp` 应当照这个写：⛔ 不是「我们的方法比朴素基线差 15.82pp」，⭐ 而是「我们量化了自我批判型反馈在语义层的收益上限，⛔ 并定位到缺的是可靠判定装置」** | ⭐ **M** |
| **⑦** | ⭐ **归因到自家机制而非模型能力**（⭐ "the lack of an optimal model-checking feedback mechanism **in our study**"）。⭐ 这个措辞很值得学 —— ⭐ 它把负面结果变成可改进项，⛔ 而不是变成「LLM 不行」的悲观结论 | ⭐ **M** |

### 2. ⛔ 不可取 / 陷阱

| # | 陷阱 | ⚠️ 它踩没踩我们踩过的坑 |
| :-: | :-- | :-- |
| **①** | ⛔⛔⛔ **规则从被评测样本本身归纳，⛔ 且无 hold-out —— ⭐ 这是本卡最严重的一条。** ⭐ 流程逐字："**Based on the findings of RQ1**, we introduced model-checking rules **to address the hallucinations identified in Tables 8–10.** **Each rule targets a specific hallucination type**"。⛔⛔ **即：⭐ Phase-I 在 30 个样本上观察到哪里出错 → ⭐ 为那些错各写一条规则 → ⛔ Phase-II 在**同一批 30 个样本**上评测那些规则。** ⭐ 所以 Table 11 的解决率**全部是 in-sample**，⛔ 而论文从未标注这一点，⛔ 也没有留出集 | ⛔⛔ **这正是本仓库 [CLAUDE.md](../../../../../CLAUDE.md) §3.5.-1 第 1 条「按引入动机反向标注」要抓的形态** —— ⭐ 每条规则的引入动机就是「某个样本没做对」。⭐⭐ **而我们对同一问题有明确口径**（⭐ [method_provenance_policy.md](../../discover_matrix/docs/protocol/method_provenance_policy.md)：⭐ 不设 hold-out，⛔ 但方法的由来一律陈述为从领域资料归纳，⛔ 且配套做抽象化自检）。⭐⭐ **这篇是「不设这条纪律会怎样」的现成反面样本：⛔ 29 条规则里，⭐ 像 `Don't miss out Final State` 这样的措辞抽象化之后确实是通用建模原则，⛔ 但像 `No explicit prompt not to use ActivityPartitions` 这样的就纯粹是对某次实测的补丁 —— ⛔ 它甚至不是一条规则，⛔ 而是一句关于 prompt 缺了什么的笔记** |
| **②** | ⛔⛔ **`temperature = 0` 单次跑，⛔ 无 `@k`，⛔ 且把消除方差当优点。** ⭐ 于是它无法区分「稳定被漏」与「偶尔被漏」。⚠️ ⭐ 更该批评的是：⭐ **它引用了 [65]（"Evaluation of LLMs should not ignore non-determinism"）却选了相反做法，⛔ 且未讨论该文主张** | ⛔ **我们 `hit@1 / hit@3 / hit@all` 三口径同报，⭐ 这一点上我们明确更强。⛔ 不要因为它是 CCF 会议论文就采纳它的单次跑口径** |
| **③** | ⛔⛔ **macro / micro 两套口径在同一篇里混用且不标注。** ⭐ §1 给的是 micro 分数（`31/72` `56/150`），⛔ 而 §6.4 引的百分数（`36.89%` `42.14%` `83.33%` `16.67%`）是**逐规则 macro**。⭐ 我方复算确认了这一点（⭐ 语义 macro = 36.89% ✅ 而 micro = 43.06%）。⛔⛔ **落差不小：⭐ 需求一致性 micro = 37.33% 而 macro = 47.80%，⭐ 差 10.5pp** | ⚠️ ⭐ **注意方向不是单向自利的**：⭐ STM 的 macro（42.14%）**高于** micro（39.13%），⛔ 而 ACT 的 macro（83.33%）**低于** micro（88.89%）。⭐ **所以这不是「口径迁就结果」，⛔ 而是「口径未声明」** —— ⛔ 按本仓库 §3.5 第 4 条应记为口径缺陷而非公平性问题。⭐ 我们报任何率时必须**明写 micro 还是 macro** |
| **④** | ⛔⛔ **主要判定全人工，⛔ 无 $\kappa$、⛔ 无第三方、⛔ 无自动检查器。** ⭐ 论文自己承认 PlantUML "lacks built-in capabilities for SysML syntax and semantic checking. Consequently, **all validations must be performed manually**" | ⛔ **这是「自证式验证」的一种**（§3.5 第 5 条）。⭐ 我们的人工判定同样是自判，⛔ 但判据先落盘、⭐ 逐位可复算、⭐ 且求值端有 pyfcstm 兜底。⭐⭐ **它连一个自动求值器都没有 —— ⛔ 这是我们相对它的结构性优势，⭐ 应当写出来** |
| **⑤** | ⛔⛔ **`Claude 3 Haiku` 代表「Claude」，⛔ 而 OpenAI 侧取旗舰档。** ⛔ 跨厂商对比系统性偏向 OpenAI，⛔ 且论文自称"all representing the latest versions"，⛔ 未讨论档位差异 | ⛔ **我们的 `gpt-5.5` vs `claude-opus-4-7` 是旗舰对旗舰，⭐ 这一点上我们是干净的。⭐ 但反过来提醒：⛔ 引用它的跨模型结论时必须标出这个偏差** |
| **⑥** | ⛔⛔ **反馈内容极其贫瘠 —— ⭐ 祈使句复述规则名，⛔ 无定位、⛔ 无反例、⛔ 无轨迹。** ⭐ 例如 `Pay attention to the rationality of the State between Traditions`（⚠️ ⛔ 还带拼写错误），⭐ 解决率 `0/6` | ⭐⭐ **我们的 `precheck_and_seal` 已经比这好一个量级**（⭐ pyfcstm 真求值，⭐ 能定位到断言与状态）。⛔⛔ **所以不能把它的「语义层无效」结论直接套到我们身上 —— ⭐ 它测的是「贫瘠反馈无效」，⛔ 不是「反馈无效」** |
| **⑦** | ⛔⛔ **fresh session 冷启动重生成 —— ⛔ 上一次的失败原因一点都不带过去。** ⭐ 逐字："To avoid contamination, **each regeneration runs in a fresh LLM session.**" | ⛔⛔ **这与本仓库 [CLAUDE.md](../../../../../CLAUDE.md) §10「外层重试不得把失败原因丢弃」直接冲突。** ⭐ 它为了避免上下文污染而放弃了增量信息，⛔ 于是每一轮都是「换个随机数再赌一次」的加强版（⭐ 虽然它注入了规则）。⚠️ ⭐ **但要公平：⭐ 它只跑一轮，⛔ 所以这个代价没有累积。⛔ 我们跑 5 轮，⛔ 若照它这么做代价会放大 5 倍** |
| **⑧** | ⛔ **无 recall 分母。** ⭐ 幻觉的分母是「已检出条数」（284），⛔ 无「应检出多少」的独立真值 → ⛔ 无漏检测量 | ⛔ 与 [sosym2026-state-machine-consistency.md](./sosym2026-state-machine-consistency.md) 同一缺陷。⭐ **我们的 98 条能力分母正是为解决这件事而存在的，⭐ 这是我们相对这两篇的共同优势** |
| **⑨** | ⛔ **公开数据集组成与论文声明对不上**（⛔ 声明 107 个模型 / 实测 65 个不同条目 / 9 个无输出）。⛔ 且无 artifact DOI、⛔ 无版本快照 | ⛔ **这是「report reproducibility support ≠ 我们能取到东西」的又一个样本。⭐ 它的判定台账很干净，⛔ 数据集却不干净 —— ⭐ 说明资产要逐类核，⛔ 不能整篇给一个 emoji** |

### 3. ⚠️ 与我们的关键差别（⛔ 为什么不能直接照搬）

| # | 差别 | ⛔ 为什么阻断照搬 |
| :-: | :-- | :-- |
| **①** | ⛔⛔ **任务主体不同：⭐ 它是生成，⭐ 我们是检测。** ⭐ 它的缺陷检测是**为了归纳 taxonomy 才做的**，⛔ 不是方法产出 | ⛔⛔ **它的「解决率」分母是「已检出的缺陷」，⭐ 我们的 `hit@k` 分母是「台账里应检出的缺陷」。⛔ 前者衡量修复能力，⭐ 后者衡量发现能力。⛔ 两者不可比，⛔ 也不能互相印证具体数值** —— ⭐ 只有**层次性趋势**可迁移 |
| **②** | ⛔⛔ **它的 reference 是人建参考模型，⛔ 不是 NL。** ⚠️ ⭐ 尤其注意：⭐ 它有一类**叫** `Requirements semantic checking`，⛔ 但操作化是「与参考模型算 F1」 | ⛔⛔ **术语陷阱确认成立，⭐ 且比 SoSyM 那篇更隐蔽** —— ⭐ SoSyM 至少老实叫 cross-view consistency，⛔ **这篇用了 "requirements consistency" 这个名字却做的是 model-vs-model**。⛔⛔ **不得把它的 `56/150` 或 `STM 42.14%` 当作 model-vs-NL 的可比数字** |
| **③** | ⛔ **谁选类完全相反** —— ⭐ 它：⛔ 人 ＋ PlantUML checker 判命中哪一类，⛔ 规则机械注入。⭐ 我们：⭐ LLM 逐需求自动选 | ⛔⛔ **所以它对「闭合词表 ＋ LLM 自动选」这个组合给不出任何先例。⛔ 本轨要数的那个组合，⛔ 这篇也不算一票**（⚠️ ⭐ 连同 SoSyM 那篇，⛔ **已连续两票不算**） |
| **④** | ⛔⛔ **它没有 sound oracle，⭐ 且明确把它列为 future work。** ⭐ 全流程唯一的自动检查器是 PlantUML 格式检查器 | ⭐⭐ **这决定了引用它的正确方向：⭐ 它是「缺乏可靠判定装置时会怎样」的证据，⛔ 不是「有了也没用」的证据。** ⭐⭐ **换个角度看：⭐ 它点名要的那个东西（counterexamples / simulation traces 当反馈），⭐ 我们已经有了（pyfcstm 求值） —— ⛔ 所以我们的问题不是「去做反例反馈」，⛔ 而是「已有的反例反馈为什么没转化成命中」。⭐ 这两个问题差别很大，⛔ 别引错方向** |
| **⑤** | ⛔ **它的 STM 只有 10 个样本进实验，⭐ 且每格跑一次** | ⛔ **`n = 10 × 6 LLM × 1 轮`，⛔ 无方差。⭐ 我们 `54 pair × 2 模型 × 3 轮 = 324 格`。⛔ 不要被它「6 个模型」的宽度误导 —— ⛔ 深度（每格轮数）是 1** |
| **⑥** | ⚠️ **界外成分方向相反** | ⭐ 它的**制品**基本界内（⭐ 实测 `basic_parallel_count = 0` 全部 38 行），⛔ 但**评测维度**伸到界外（⭐ fork/join ＋ 4 条时间约束语义）。⛔⛔ **若要取它的 STM 子集当测试制品，⭐ 必须逐样本过门 ＋ 先去重 ＋ 重新分型**（→ D 节终裁第 3/4 条） |

---

## F. 存疑与未核项

1. ⛔⛔ **`SD 16.67%` 复算不出（⭐ 我方实测，⛔ 这是一条真实的数字缺陷）** —— ⭐ §6.4 逐字 "SD only **16.67%**"。⭐ 我方按 Table 11 的 SD 需求一致性 6 条规则复算：⭐ **逐规则 macro = `(12/45 + 8/28 + 1/13 + 2/6 + 0/5 + 0/3)/6 = 16.04%`** · ⭐ **micro = `23/100 = 23.00%`**。⛔ **两个都不是 16.67%。** ⭐ 交叉验证口径成立：⭐ 同一 macro 算法在语义（36.89%）· STM（42.14%）· ACT（83.33%）三处**逐位对上**，⛔ **所以口径是对的，⛔ SD 这一格是算错的**。⚠️ ⭐ `16.67% = 1/6` 恰好是「六条规则里只有一条满分」的值，⛔ 疑为把某一格误当成 `1` 或抄写滑手。⛔ **我不为它编一个能凑出 16.67% 的口径。**
2. ⚠️ **幻觉分类学在同一篇里有两种说法** —— ⭐ §4.2 说 **四类**（"grouped into **four** types: PlantUML formatting errors, SysML grammar errors, SysML semantic inconsistencies, and requirements semantic inconsistencies"），⛔ §5.4 说 **三类**（"categorize them into **three** types: PlantUML format errors, SysML grammar & semantic errors and requirements inconsistencies"）。⭐ 表结构（Table 8/9/10）实际走四类但语法与语义合表。⛔ **本卡按四类记。**
3. ⚠️⚠️ **Table 7 的 `Acc_S@FC` 列疑为误粘 F1 列** —— ⭐ Table 7 给 `STM 69.29% · ACT 97.49% · SD 50.02%`，⛔ 而 §5.3 的三个语义 F1 均值恰好是 `69.29% · 97.49% · 50.02%`，⛔ **三位小数逐位相同**。⭐ 两个指标定义完全不同（⭐ 一个是语法准确率在字段约束子集上的取值，⭐ 一个是语义一致性 F1），⛔ **不可能恰好全等**。⛔ **本卡不采信该列**，⛔ 且未能确认正确值应是多少（⛔ 工作簿里未找到对应表）。
4. ⛔⛔ **公开数据集 107 行只含 65 个不同条目，⛔ 与声明的 `36 / 36 / 35` 无法对账 —— ⭐ 但我无法判定原因** —— ⭐ 已试并已排除两种解释（⛔ 非我方 parquet 化脚本所致：⭐ 我重新从 Drive 下载原始 xlsx 复算得同一结果；⛔ 非多工作表拼接：⭐ 只有一个工作表、行号 0–106 连续）。⛔ **剩下两种可能我无法区分**：⭐ ① 作者把 107 个**行**当成 107 个**模型**（⛔ 即贡献声明本身有误）；⛔ ② Drive 上的表被误传了重复块（⛔ 即论文对、工件错）。⛔ **未联系作者。**
5. ⚠️ **实验用的 30 个样本无法从 `Dataset` 工作表重建** —— ⭐ 该表的 `selected` 标记列只有 **22 行**有标记（⭐ 21 `selected` ＋ 1 `Selected`），⭐ 且去重后只对应 **15 个**不同条目，⛔ **凑不出 30**。⭐⭐ **但可以从三个 Results 工作表重建**（⭐ 各含恰好 10 个 distinct `Model Name`，⭐ 我方已列出全部 30 个名字）。⛔ **所以「哪 30 个进了实验」这件事**只能**通过 Results 表还原，⛔ 不能通过 Dataset 表的标记列还原。**
6. ⚠️ **`ACT Results` 有 72 行而 `STM/SD Results` 各 60 行** —— ⭐ 三者的 distinct `Model Name` 都是 **10**，`LLMs` 都是 **6**，⭐ 所以 `10 × 6 = 60` 是正常规模；⛔ **ACT 多出的 12 行未能确认是什么**（⭐ 疑为汇总行或空行）。⚠️ ⭐ 本仓库冻结的 human-review parquet 也是 `act 72 / stm 60 / sd 60 = 192`，⛔ 即那 12 行被一并抽了进来。⛔ **未逐行核。**
7. ⚠️ **55 条语义里含对我们界外的构件，⛔ 而论文不区分** —— ⭐ 实测：⛔ `fork` / `join` Pseudostate（⭐ 并发）· `deepHistory` / `shallowHistory` · ⛔ **第 52–55 行 `TimeConstraint` / `DurationConstraint` / `TimeObservation` / `DurationObservation`（时间）**。⛔ **若要把这 55 条当出处素材用，⛔ 必须先按 [CLAUDE.md](../../../../../CLAUDE.md) 的边界剔掉这些，⛔ 且必须回 L2 过出处轴**（→ [README.md](../README.md) §3 防火墙）。
8. ⛔ **无实验代码** —— ⭐ prompt 有、数据有、逐条判定有、⛔ **但生成 / 重生成 / RAG 检索 / 评测脚本全无**。⭐ 复现需自行实现 prompt 装配、RAG、PlantUML 检查接线与 regeneration 循环。⛔ **已确认论文全文无仓库链接、无 artifact 声明。**
9. ⚠️⚠️ **Drive 里另有一个 `ESE Expriment Results` 工作簿，⛔ 含论文里根本没有的表** —— ⭐ 我方实取（`2,075,406 B`，`HTTP 200`），⭐ 9 个工作表：`STM Results`（65×26）· `ACT Results`（65×28）· `SD Results`（60×27）· ⭐ **`Time Results`（58×39）· `Validation Results`（62×14）· `Verification Results`（101×30）· `Token Results`（80×18）** · `Visualization`（90×20）· `Supplement`（26×15）。⛔⛔ **`Verification Results` / `Token Results` / `Validation Results` 这三张表在 Internetware 2025 论文里没有对应内容**（⛔ 论文不报 token、不做 verification）。⭐ 文件名里的 `ESE` 疑指 *Empirical Software Engineering* 期刊，⛔ **即这可能是一篇在建的期刊扩展版的数据**。⛔ **本卡未读这三张表，⛔ 也未搜索该扩展版是否已发表。** ⚠️ ⭐ **若它已发表且真的接了 verification 与 token 账，⛔ 那篇对本轨的价值可能高于这篇 —— ⭐ 建议单独追。**
10. ⚠️ **`Internetware` 未在本仓库 [ccf_venues/](../../../../../ccf_venues/) 建档** —— ⭐ 已 grep 全库，⛔ 无 `conf-*-internetware` 目录，⛔ 也无 Internetware 相关行。⭐ 本卡的 `ccf = C` 沿用 [`baselines/llms_emp/ASSETS.md`](../../../../baselines/llms_emp/ASSETS.md) 的 `🥉` 记录，⛔ **未查 CCF 第七版目录原件核实**。
11. ⚠️ **论文内部还有一处数字冲突（⛔ 已定位，⛔ 但影响很小）** —— ⭐ §3.4 逐字写 "36 activity diagrams, **34 state machine diagrams**, and 35 sequence diagrams"（⛔ 合计 105），⛔ 而摘要 / §1 / Table 2 列合计都是 **36 STM**（⭐ 合计 107）。⭐ 我方逐行验过 Table 2 的三列，⭐ **合计确为 36 / 36 / 35 = 107 ✅**，⛔ **所以 §3.4 的 `34` 是笔误。**
12. ⚠️ **Figure 4（ACT 的 prompt 示例）与 Figure 2（STM 示例 ＋ 需求模板）是图片，⛔ 未 OCR** —— ⭐ `paper_content.txt` 只保留图注。⭐⭐ **但影响不大：⭐ prompt 的完整文本在工作簿的 `Prompt` 列里，⭐ 比截图更全**（→ D 节）。⛔ **需求规格模板（Figure 2 右半）的具体字段未核。**
13. ⚠️ **`Acc_S` 的分母 `N^gp_a` 与 F1 的 GP 计数是否同一套，⛔ 未能确认** —— ⭐ 两者都用 grammar point，⛔ 但一个数「正确的 GP」一个数「匹配上的 GP」，⛔ 论文未说明当一个 GP 既语法正确又与参考模型不匹配时如何计入。⛔ **未核。**
