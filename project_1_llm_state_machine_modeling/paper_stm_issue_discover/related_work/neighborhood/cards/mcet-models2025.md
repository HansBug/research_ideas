# 卡片 · **MCeT**（MODELS 2025）

⭐ **本轨最接近我们 `discover` 任务形状的一篇**：它正面做「用 LLM 判一个行为模型对不对」，输出是自然语言缺陷清单，参照物是自然语言需求 —— 与我们完全同形。⛔ 但制品是**时序图**而非状态机，缺陷分类学不共享，⛔ **本仓库已裁定为「邻域标杆」，不作对照系**。

⭐ **证据基础**：arXiv HTML 全文（`2508.00630v1`，逐节通读）+ ⭐ **实际 clone 的仓库源码**（HEAD `8b1b6507`）。⭐ 凡标 M 的都附逐字英文片段；⛔ 凡从代码读出而论文未写的，单列并标 **M(code)**。

---

## A. 元信息

| 字段 | 值 |
| :-- | :-- |
| `id` | `mcet-models2025` |
| `title` | MCeT: Behavioral Model Correctness Evaluation using Large Language Models |
| `year` | **2025**（Crossref `issued` = `2025-10-05`，⭐ 非 early-access） |
| `venue` | ACM/IEEE 28th International Conference on Model Driven Engineering Languages and Systems (**MODELS 2025**), pp. 84–95 |
| `ccf` | ⭐ **B**（仓库 [ccf_venues/conf-b-models/](../../../../../ccf_venues/conf-b-models/)） |
| `doi` | [`10.1109/MODELS67397.2025.00014`](https://doi.org/10.1109/MODELS67397.2025.00014) —— ⭐ **已实际核**：Crossref 返回标题 / container / pages 全部匹配 |
| `arxiv` | [`2508.00630`](https://arxiv.org/abs/2508.00630)（HTML 全文可读） |
| `url` | 仓库 [github.com/Huawei-TTE/MCeT](https://github.com/Huawei-TTE/MCeT) |
| 作者 / 单位 | Khaled Ahmed, Jialing Song, Ou Wei, Bingzhou Zheng（**Huawei Research Canada**）+ Boqi Chen（McGill，实习期间完成部分工作） |
| `artifact_type` | ⭐ **UML 时序图**（PlantUML 文本语法）。⚠️ 仓库里另有 activity diagram 的 textX 语法与访问器（`plantuml_grammar.tx` / `plantuml_activity.py`），⛔ 但论文只评测时序图 |
| `task` | ⭐ **缺陷检测**（模型 vs 自然语言需求，输出 NL 缺陷清单）—— ⛔ 不做生成、不做修复 |
| `boundary` | ⭐ **邻域**（时序图；⛔ 非 $M=(S,E,V,Tr,A)$） |

---

## B. LLM 应用形态

### B1 · 流水线阶段

⭐ 论文把它描述成**两阶段**：`MCeT-A`（原子检查）→ `MCeT-X`（高权威交叉核查）。⭐ 展开到调用粒度（阶段划分依据 = 仓库源码 `mcet_sequence.py` + 三个 check 类）：

```
[人/AI] 需求文本 (.txt) + PlantUML 时序图 (.puml)
  │
  ├─ 视角 1 · Holistic check
  │    [LLM] 整图 vs 整需求（few-shot + CoT，×5 采样）
  │      → [LLM] 「出现 > N/2 次的留下」投票聚合   ⛔ 投票也是 LLM 做的
  │      → [LLM] align/归一
  │
  ├─ 视角 2 · Diagram-atom check
  │    [确定性] textX 解析 PlantUML → 抽 diagram-atom（消息 + 两端参与者）+ 去重
  │      → [LLM] 每个 atom 问 8 条**固定** Yes/No 问题（×5 采样）
  │      → [LLM] combine_by_atom 蒸馏成「每 atom 一条 issue」
  │
  └─ 视角 3 · Requirement-atom check
       [LLM] 把需求切成 requirement-atom（zero-shot，JSON 数组）
         → [LLM] 每 5 条 atom 一批，问 Correct? / Complete?（×5 采样）
         → [LLM] combine_by_atom 蒸馏

  ↓  MCeT-X
  [确定性] 取「无 issue 的 requirement-atom」= Correct Requirement-atoms
  [LLM] 用它们过滤 holistic issues     （junior vs senior 角色扮演）
  [LLM] 用它们过滤 diagram-atom issues （同上）
  [确定性] 三份清单求并 → 最终输出
```

⭐ **计数（按仓库源码的调用点数）：约 13 个 LLM 阶段 · 3 个确定性阶段。** ⛔ 确定性的三处是：**PlantUML 解析 + atom 抽取去重**、**correct-req-atom 的选取**、**最终三路求并**。⛔ **其余全部是 LLM，连投票聚合都是。**

### B2 · 每次 LLM 调用的角色

| 调用 | 角色 |
| :-- | :-- |
| holistic check | ⛔ **评审者**（LLM 自评，整图） |
| holistic 投票聚合 | ⛔ **裁决者**（判「哪些 issue 出现够多次」）—— ⚠️ 本该是计数，却交给了 LLM |
| requirement split | ⭐ **抽取器**（NL → 原子需求） |
| requirement-atom check | ⛔ **评审者** |
| diagram-atom check | ⛔ **评审者** |
| `combine_by_atom` 蒸馏 | **解释者 / 归并器**（把同一 atom 的多次采样结果压成一条） |
| 高权威交叉核查 ×2 | ⛔⛔ **裁决者**（判「另一个 LLM 报的 issue 是不是幻觉」） |

⛔ **全流水线没有任何一处 sound oracle 参与判定。** ⭐ 唯一的确定性组件（textX parser）只负责**切原子**，不负责**判对错**。

### B3 · prompt 策略

`few-shot`（holistic 与 diagram-atom prompt 内嵌一个完整 worked example：Alice/Bob 认证 + DNS 攻击）· `CoT`（M：*"use chain-of-thought [43] to analyze the differences"*）· `self-consistency`（N=5 采样）· `角色扮演`（⭐ **junior engineer vs senior engineer**，用来编码权威等级）· ⚠️ **准结构化输出**：prompt 内给 JSON 形状 + 用 `answer_start` 预填开头做受限起步，⛔ **但没有 schema validator** —— 解析失败靠 `try/except` + `num_retries: 20` 冷重试，⛔ 不把解析错误回灌给模型。

⭐ **prompt 全部公开**（11 个 JSON，共 51,876 字节）→ 见 D 节。

### B4 · ⭐⭐ 循环与裁决者（本轨最关键一格）

| 子字段 | 值 |
| :-- | :-- |
| 有无循环 | ⛔⛔ **无。** ⭐ MCeT 是**严格前馈**的两阶段管线：`MCeT-A → MCeT-X` 各跑一次，⛔ **没有修订轮、没有反馈回灌、没有终止判据** |
| ⭐ **裁决者是谁** | ⛔⛔ **LLM 自评，全程。** ⭐ 且是**分层的 LLM 自评**：`requirement-atom check` 的结论被立为「高权威」，用来否决 `holistic` 与 `diagram-atom` 的结论 |
| 终止条件 | ⭐ **不适用**（无循环）。⚠️ 唯一的重试是 JSON 解析失败的冷重试，上限 `num_retries: 20`（M(code)，`config_mcet_seq.json`） |
| 最大轮数 | ⭐ **1**（每个视角内 5 次**并行采样**，⛔ 不是 5 轮迭代） |
| ⭐ 有无报**边际收益** | ⭐⭐ **有，而且是本卡最有用的数字** —— 见下 |

#### B4a · ⭐⭐ 阶段边际收益（`MCeT-A` → `MCeT-X`，全 FBench / GPT-4o-mini，Table II）

| 指标 | MCeT-A（组合，未交叉核查） | MCeT-X（组合，已交叉核查） | Δ |
| :-- | --: | --: | :-- |
| Total | 1524 | 1155 | ⭐ −369 |
| True positives | 1096 | 938 | ⛔ **−158** |
| False positives | 428 | 217 | ⭐ **−211** |
| Precision | 0.72 | **0.81** | ⭐ +0.09 |
| FBench recall | 92（68.1%） | 88（65.2%） | ⛔ **−2.9pp** |
| New true issues | 487 | 391 | ⛔ −96 |

⭐ **M 逐字**：*"cross-checking successfully reduces the number of false positive issues in the combined MCeT-A results from 428 to 217 in the combined MCeT-X results, eliminating 211 false positives, while only reducing true positives by 158 issues from 1096 to 938."*（§VI-A）

⭐⭐ **这一格对我们的意义**：⭐ 他们**明确报了「多花一个 LLM 阶段换来什么」**，⛔ 并且诚实承认那一步**同时杀掉了 158 条真 issue**，⛔ 净精度提升的代价是召回下降 2.9pp。⭐ 他们的处理方式不是藏，而是**把两档都保留成用户可选的配置**（见 C 节 `adverse_results`）。

#### B4b · ⭐ 单视角逐档收益（同表）

| 指标 | Holistic（baseline） | Diagram-atom | **Requirement-atom** |
| :-- | --: | --: | --: |
| Total | 134 / 69 (A/X) | 505 / 201 | 885（A=X） |
| Precision | 0.58 / 0.62 | 0.50 / 0.65 | ⭐ **0.86** |
| FBench recall | 34.1% / 20% | 31.9% / 23.7% | ⭐ **59.3%** |

⚠️ **注意口径**：`Req.-Atom` 列 A=X，因为**它自己就是权威，不被任何东西过滤**（M：*"the issues in the 'Req.-Atom check' column are the same in MCeT-A and MCeT-X since the requirement-atom MCeT-A results are the higher authority used as reference for cross-checking."*）。

#### B4c · ⭐ 成本倍数（Table III，8 图 / 10% 子集）

| 模型 | baseline K tok/图 | MCeT-X K tok/图 | ⭐ 倍数 | baseline 分钟/图 | MCeT-X 分钟/图 | ⭐ 倍数 |
| :-- | --: | --: | --: | --: | --: | --: |
| GPT-4o-mini | 12 | 80.5 | ⭐ **6.7×** | 0.6 | 4.5 | 7.5× |
| GPT-4o | 13.5 | 86.7 | 6.4× | 0.5 | 4.5 | 9.0× |
| DeepSeek-v3 | 18.1 | 124.9 | 6.9× | 1.5 | 10.3 | 6.9× |
| DeepSeek-R1 | 31.1 | 236.2 | 7.6× | 8 | 77.4 | 9.7× |

⭐⭐ **这是全轨最直接可比的一个数**：⛔ 他们用 **6.4–7.6× 的 token** 买到 **+0.01 ~ +0.27 精度** 与 **+21.4 ~ +42.8pp 召回**；⛔ 我们 v46 用 **212.6×** 买到 **−15.82pp**。⭐ 差了一个半数量级，⛔ 而差别的来源正是 B4 那一格：**他们的额外 token 全部花在「换视角重问」，我们的 79% 花在「让 LLM 自我批判并修订」。**

### B5 · ⭐ 中间表示

| 子字段 | 值 |
| :-- | :-- |
| 有无 | ⭐ **有（两层，⛔ 但都不是缺陷分类学）** |
| 形态 | ① **diagram-atom** = 一条消息 + 其两端参与者；② **requirement-atom** = 「至多一个动作 + 一到多个参与者」的原子需求；③ ⭐ **8 条固定 Yes/No 问题清单**（仅用于 diagram-atom 检查） |
| ⭐ 是否闭合 | ⚠️ **分层不同**：⭐ **问题清单闭合**（8 条硬编码）；⭐ **diagram-atom 闭合**（由文法确定性抽出）；⛔ **requirement-atom 开放**（LLM 自由切分）；⛔⛔ **缺陷本身完全开放** —— 输出是自由英文散文，**没有任何缺陷类型枚举** |
| ⭐ 谁定的 | ⭐ 8 条问题：**作者硬编码在源码里**（`message_correctness_one_shot.py:28-37`），⛔ **对每个 atom 全问，不做选择** —— ⛔ **没有「LLM 自动选类」这一步** |

⭐ **8 条问题逐字（M(code)，`QuestionList.questions`）** —— ⭐ 结构上是 **4 个维度 × 2 个正反问法**：

| # | 问题 | 期望答案 |
| :-: | :-- | :-: |
| 1 | Is this sequence diagram message **correct** according to the requirements? | Yes |
| 2 | Should we **change** this sequence diagram message in any way (without adding details) to make it align with the requirements? | No |
| 3 | Is this sequence diagram message (including its related context) **complete** (has all relevant details) according to the requirements? | Yes |
| 4 | Should we **add any missing details** to this sequence diagram message or its context (the given PlantUML) to make it align with the requirements? | No |
| 5 | Are the **participants** of this sequence diagram message correct according to the requirements? | Yes |
| 6 | Should we **change any of the participants** of this sequence diagram message to make it align with the requirements? | No |
| 7 | Is the **direction** of this sequence diagram message correct according to the requirements? | Yes |
| 8 | Should the **direction** of this sequence diagram message be flipped to make it align with the requirements? | No |

⭐⭐ **值得注意的设计**：⭐ 同一件事**正问一遍反问一遍**（1/2、3/4、5/6、7/8），⛔ 这是在用**问法冗余**代替我们那种「谓词 + 求值器」的机械判定。⛔ 但它**不聚合正反答案的一致性** —— 代码里两问各自独立产 issue，只在 `combine_by_atom` 里被 LLM 蒸馏成一条。

⭐ **原子概念有出处**：M 逐字 *"Prior work has proposed several other 'atoms' that can be checked during the manual correctness checking of sequence diagrams [41], e.g., incorrect messages, participants, lifelines, conditions, etc."* —— ⭐ [41] = Yue, Briand, Labiche, TOSEM 2013。⚠️ 他们**主动收窄**了：*"Our definition of a diagram-atom covers both messages and their participants, which are the main building blocks and the most frequent elements"*，⛔ **lifelines / conditions / combined fragments 都被排除在 atom 之外**（只作为「上下文」进 prompt）。

### B6 · 模型

| 模型 | 用在哪 | 备注 |
| :-- | :-- | :-- |
| **GPT-4o-mini** | ⭐ 主结果（全 76 图） | M：*"GPT-4o-mini is selected as it is a lightweight, cost-efficient, and fast LLM with good performance"* |
| **GPT-4o** | RQ3（8 图） | |
| **DeepSeek-v3** | RQ3（8 图） | |
| **DeepSeek-R1** | RQ3（8 图） | ⭐ 唯一的 reasoning 模型 |

⭐ **有四模型对照**，⛔ **但主结果只用最弱的那个**（GPT-4o-mini）。⚠️ **代际风险很大**：GPT-4o-mini 是 2024-07 的模型，DeepSeek-R1 是 2025-01；⛔ 本卡所有数字都要按「上一代模型」打折读 —— ⭐ 尤其 §VI-C 自己就承认 DeepSeek-R1 的**裸 holistic** 召回（50%）已经接近 GPT-4o-mini 上整套 MCeT 的水平，M 逐字：*"This is because the LLM's reasoning attempts a fine-grained evaluation, similar to the MCeT approach"*。⛔⛔ **换句话说，他们自己给出了「方法收益会被模型代际吃掉」的证据。**

⭐ 采样参数：`temperature = 0.7`，`top_p = 1`，`num_votes = 5`（M：*"All LLMs are configured with a temperature and top-p of 0.7 and 1, respectively. The number of votes is set to five."*）。

### B7 · ⭐ 确定性成分（⛔ 只有三处，全部不在判定端）

| 环节 | 是什么 | 干什么 |
| :-- | :-- | :-- |
| PlantUML 解析 | ⭐ **textX 文法**（`plantuml_sequence_grammar.tx`，117 行；activity 版 178 行） | 把 `.puml` 解析成 AST → 建图 → 抽 message 节点 |
| atom 抽取与去重 | `puml_graph.py` + `question_strs` 集合去重 | ⛔ **重复消息只问一次** |
| 最终求并 | Python 列表合并 | 三路清单并集 |

⭐ M 逐字（§II）：*"automatically processing a sequence diagram designed with PlantUML is as simple as parsing the syntax, converting it to an abstract syntax tree, and performing any further processing on the tree."*

⛔⛔ **没有模型检查器、没有求解器、没有仿真、没有任何语义层判定。** ⭐ 与我们的对比极其鲜明：**我们有 pyfcstm 这个 sound oracle 但把它放在求值端；他们连 oracle 都没有，判定端全是 LLM。**

---

## C. 实验

| 字段 | 值 |
| :-- | :-- |
| `baseline` | ⭐ **只有内部 ablation**：`Holistic check` 单独跑当 baseline（M：*"We use the direct holistic check results as a comparison baseline."*）。⛔ **无任何外部工具 / 外部方法对照** —— 理由是他们自陈无前作（见 F 节的 first 主张） |
| `dataset` | ⭐ **FBench**（他们自己起的名），源自 Ferrari et al. REW 2024 [5]。⭐ 28 份真实工业需求（Lockheed Martin CPS 需求 / PURE / user stories），作者注入 requirement smells 造出 **87 个变体**，⛔ 剔除「生成了错类型图」与「未给扣分理由」的，⭐ **剩 76 个用于评测**。⭐ 图由 **ChatGPT (GPT-3.5)** 生成 |
| ⭐ 分母怎么定的 | ⭐ **两个分母，⛔ 口径不同**：① `Precision` 分母 = MCeT 自己报的 issue 数（1524 / 1155），⛔ **随方法变动**；② `FBench recall` 分母 = **人报 issue 数 = 135**（由 92/68.1% 与 88/65.2% 反算，⚠️ **论文正文从未写出这个 135**，S 级推算） |
| `metrics` | `Total` · `True positives` · `False positives` · `Precision` · `FBench recall` · `New true issues` · `Avg K tokens/diagram` · `Avg minutes/diagram`。⛔⛔ **没有任何 `@k` 多轮口径** —— ⭐ 5 次采样被**内部合并掉**了，⛔ 不作为报告维度 |
| ⭐ `judged_by` | ⛔⛔ **本文两位作者亲判**（M：*"we rely on the human judgement of two of the authors of this paper. Both authors are software engineers with 4 and 6 years of experience."*）。⭐ **有标注者间一致性**：在前 20% 图上双人独立判，**Cohen's $\kappa$ = 0.79**（M：*"which results in 0.79, indicating a substantial agreement, close to 0.8 which indicates almost perfect agreement"*），⭐ 分歧讨论后统一判据；⛔ **其余 80% 的 issue 是两人分工、每条只有一个判定者** |
| `human_baseline` | ⭐ **有（但是作为 ground truth 而非对照臂）**：Ferrari et al. 的两位研究者（也是资深工程师）对每张图按 0–5 打 5 项分，⭐ 非满分时写出扣分理由 → 这些理由即人报 issue |
| `runs` | ⛔⛔ **每张图只跑一次 MCeT**（内部 5 次采样）。⛔ **无重复实验、无方差、无置信区间**。⚠️ §VII 自己承认：*"LLMs are probabilistic in nature, it is possible to get different issues each time MCeT is run on a use case. To address this consistency issue, we implemented a voting mechanism"* —— ⛔ **用投票代替了报方差** |
| ⭐ `adverse_results` | ⭐⭐ **处理得相当漂亮，直接可借鉴 —— 见下** |

### C1 · ⭐⭐ 他们怎么写不利结果（⭐ 我们 −15.82pp 可直接照抄的写法）

⭐ **共四处不利结果，全部明写、全部给了机制解释、⛔ 无一处被藏**：

1. ⭐ **核心步骤会杀真 issue** —— 交叉核查砍掉 158 条真 issue、召回从 68.1% 掉到 65.2%。⭐ **处理方式：不辩解，改成让用户选档。** M 逐字：*"Thus, MCeT-A is beneficial when higher true positives are desired by the user (e.g., in safety critical systems), while MCeT-X is useful in exploratory projects, when the user desires less false positives."* ⭐⭐ **这就是把「有得有失」翻译成「两个配置档」的标准动作。**
2. ⭐ **给了一个自己被砍掉的真 issue 的完整反例**（`g02-uc-cm-req.v0` 的 `Navigate to the website`），⭐ 逐字解释为什么权威判据在这里失效：*"the LLM finds that the Navigate to the website is in the diagram, but fails to detect the issue with the other participant of this message, the website. Thus, the correctly identified diagram-atom is filtered out."*
3. ⭐ **一个模型上召回反向下滑** —— DeepSeek-v3 召回 71.4% → 50%。M 逐字：*"Only DeepSeek-v3 has a drop in recall (from 71.4% to 50%), however, DeepSeek-v3 cross-checked results still outperform the baseline holistic precision and recall."* ⭐ 明写掉了，⛔ 但**紧跟一句相对 baseline 仍占优**做缓冲。
4. ⭐ **把 false positive 转化成副产品** —— 需求本身模糊导致的 FP，被重新解释成有用信号：*"Thus, MCeT-X false positives can help the user spot problems in the requirements."* ⚠️ **这一招要谨慎学**：⛔ 它没有量化「有多少 FP 属于这一类」，⛔ 属于叙事性缓冲而非证据。
5. ⭐ 未来工作里把这一条列为待修项：*"We plan to investigate preventing the cross-checking approach from eliminating real issues."*

---

## D. 资产（⛔ 全部实际取过）

| 资源类型 | 状态 | URL / 路径 | ⭐ 核验证据 |
| :-- | :-: | :-- | :-- |
| 论文全文 | ⭐ 🟢 | [arxiv.org/abs/2508.00630](https://arxiv.org/abs/2508.00630) | ⭐ HTML 全文可读（`2508.00630v1`，2025-08-01），逐节通读；⭐ 正式版 DOI 经 Crossref 核实（pages 84–95） |
| ⭐ **实验代码** | ⭐ 🟢 | [github.com/Huawei-TTE/MCeT](https://github.com/Huawei-TTE/MCeT) | ⭐ 机械核验逐字：`HEAD 8b1b65073e · 文件 288（非文档 202）· release 0 · license 无`。⭐ 已 `git clone` 实读：**唯一 commit** `8b1b6507 "Hello MCeT" (2025-07-30)`，⛔ 单次代码倾倒、无历史。⭐ 22 个 Python 文件 / 5,887 行；核心 6 个 check 模块齐全（`holistic_correctness.py` 471 行 · `requirement_correctness.py` 326 · `message_correctness_one_shot.py` 356 · `combine_atom_check_issues.py` 405 · `combine_holistic_req_atom_check_issues.py` 312 · `puml_visitor.py` 1632）。⛔⛔ **无 LICENSE / COPYING**，⛔ 无测试、无 CI、无 `requirements.txt` 锁版本 |
| ⭐ **数据集 / Benchmark** | ⭐ 🟢 | `model_evaluation/model_evaluation/Ferrari/` | ⭐ **84 组 `(.txt 需求, .puml 图, .score 评分)`** 三件套完整入库。⚠️ **不等于论文的 76** —— ⛔ 仓库里**没有 eligibility 清单**说明哪 11 个被剔除，⛔ 复现主结果分母需自行重建 |
| ⭐ **Ground truth** | ⭐ 🟢 | 同上：84 个 `.score` + `Ferrari/correctness_mistakes_collection.txt` | ⭐ **人报 issue 就在仓库里**。`.score` 是 Ferrari 原始五维评分 + `Observations:` / `Issues:` 自由文本；⛔ 且额外有一份 **CSV 形态的 `correctness_mistakes_collection.txt`（`name,score,reason`，62 行）** —— ⭐ 这份就是 correctness 维度的人工缺陷台账（例：`1.autopilot.v2,3,<= 6 is incorrect interpretation of at most 6`）。⛔ **全部自由英文散文，无缺陷类型标签、无定位字段、无一条对齐到具体消息** |
| 实验结果细则 | ⛔ ⚪ | — | ⛔⛔ **只有论文里的 Table I / II / III。** ⛔ 仓库里**没有任何 run 输出**：无逐图 issue 清单、无 1524 条 issue 的人工判定标签、无 token/时间原始记录。⭐ 而全文最贵的资产恰恰是那 1524 + 347 条人工判定 —— ⛔ **它没有被放出来**，⛔ 因此 precision 与 recall **无法被第三方复算** |
| Artifact / 复现包 | ⛔ ⚪ | — | ⛔ 无 Zenodo / 4open / OSF DOI，⛔ 无 MODELS artifact badge 迹象 |
| ⭐ **prompt 是否公开** | ⭐ 🟢 | `model_evaluation/model_evaluation/prompts/` | ⭐⭐ **11 个 JSON 全公开，共 51,876 字节，已逐个读过**：`prompt_holistic_check.json`(6167，⭐ 含完整 few-shot 样例) · `prompt_requirements_split.json`(631) · `prompt_requirements_check.json`(1416) · `prompt_message_correctness_one_shot_no_example.json`(2152) · `prompt_filter_diagram_issues_by_reqs.json`(1211，⭐ junior/senior 角色扮演原文) · `prompt_filter_req_issues_by_diagram.json`(1202) · `prompt_holistic_vote_feedback.json`(2666) · `prompt_combine_atom.json`(1054) · `prompt_message_feedback.json`(3465) · `prompt_align_correctness_completeness.json`(16946) · `prompt_distill_message_feedback.json`(14966)。⭐ 8 条 atom 问题不在 JSON 里，⛔ 硬编码在 `message_correctness_one_shot.py:28-37` |
| 配置模板 | ⭐ 🟢 | `config_mcet_seq.json` | ⭐ 含 `num_votes: 5` / `num_retries: 20` / `parallel: True` / `temperature: 0.7` / `top_p: 1`，⭐ 与论文一致；⛔ API key 与 server 为占位符（正确做法） |

### ⭐ 终裁：🟢（⛔ 但是**不可复算的 🟢**）

⭐ 仓库是**真货**：代码、prompt、数据、ground truth 四样都在，⛔ 远好于本轨常见的空壳。⛔⛔ **但它缺的那一样恰好是最关键的一样：人工判定标签。** ⭐ 没有它，论文的 0.81 / 65.2% 只能被**重跑**（花钱、且换模型必然漂移），⛔ **不能被复算**。

⚠️ **另有两处会实际卡住复现的问题（M(code)）**：

1. ⛔ **README 的运行命令是错的**：README 写 `python correctness_property.py`，⛔ 而仓库里的主脚本叫 **`mcet_sequence.py`**，⛔ `correctness_property.py` 不存在。
2. ⚠️ **README 的示例配置文件名也不存在**（`config_0.3.1_seq_template.json`），⛔ 仓库里只有 `config_mcet_seq.json`。

---

## E. 对 M1 的意义

### 1. ⭐ 可取之处（⛔ 具体到能搬的设计决定）

1. ⭐⭐ **「换视角重问」比「自我批判重修」划算得多 —— 这是本卡最重要的一条。** ⭐ 他们的三个视角**问的是同一份制品**，⛔ 只换**输入的切分粒度**（整图 / 逐消息 / 逐需求），⛔ **不让任何一个视角去修另一个视角的产物**。⭐ 收益极其清楚：`holistic` 单独召回 34.1%，加两个视角后 68.1%，⭐ **翻倍**；成本 6.7×。⛔ 而我们 v46 把 79% 的 token 花在**让 LLM 批判并修订自己**，收益 ≈ 0、成本 212.6×。⭐⭐ **M1 应当考虑把「修订轮」的预算改投到「换切分粒度重问」上。**
2. ⭐⭐ **「谁被切成原子」这个选择，本身就是最大的效果变量。** ⭐ 三个视角里最强的是 **requirement-atom（precision 0.86 / recall 59.3%）**，⛔ 最弱的是 diagram-atom（0.50 / 31.9%），⭐ 差距接近一倍。⭐ 他们给的机制解释非常干净，M 逐字：*"the requirement-atom check does not exhibit this problem, because the task of the LLM is to assess correctness of the diagram, not the requirements. This is a simpler task ... as the check is context-free"* —— ⭐⭐ **判据：让 LLM 判的那个东西必须是「自足的」（context-free）；一旦它的正确性依赖周边上下文，precision 就崩。** ⭐ 这条**直接可用于 M1 给谓词分族**：我们的结构族谓词本质是 context-free 的，仿真族/BMC 族是 context-sensitive 的 —— ⛔ 后者的多报率应当被预期为更高，⭐ 而这与我们 v46 的多报分布值得对拍。
3. ⭐ **「不对称权威」是一个比多数投票更聪明的聚合形态。** ⛔ 他们**没有**把三个视角对称投票，⭐ 而是先离线量出哪个视角 precision 最高（Table I），⭐ 再让它**单向否决**另两个，⛔ 自己不被否决。⭐ 实测 FP −211 / TP −158，净精度 +0.09。⭐ **M1 若要做多视角，这个形态比 majority vote 更值得抄** —— ⛔ 前提是先量出各视角的 precision 排序。
4. ⭐ **同一维度正反两问，是低成本的一致性装置。** ⭐ 8 条问题实为 4 维 × 2 极性（「对不对」/「要不要改」）。⛔ 他们没有把正反答案的矛盾当信号用（⚠️ 见下 E2.4），⭐ 但形式本身很便宜，⭐ 可用于我们的谓词提问端。
5. ⭐⭐ **不利结果的写法直接可抄。** ⭐ 面对「核心步骤同时杀掉 158 条真 issue」，⛔ 他们不辩解、不弱化，⭐ 而是**把它转成两个可选配置档**并给出选择判据（安全关键 → 要召回选 MCeT-A；探索性 → 要精度选 MCeT-X），⭐ 再给一个自己被误杀的完整反例，⭐ 最后把它列进 future work。⭐⭐ **我们的 −15.82pp 可以照这个骨架写**：不掩饰、给机制、给档位、给反例、列待修。
6. ⭐ **成本必须报，而且要按模型分档报。** ⭐ Table III 把 `K tokens/图` 与 `分钟/图` 与精度召回并列，⭐ 于是「值不值」这个问题读者自己能算。⛔ 我们的 212.6× 就该这样摆出来。

### 2. ⛔ 不可取 / 陷阱（⚠️ 尤其：它踩了我们踩过的哪些坑）

1. ⛔⛔ **判定端零 sound oracle，且把「幻觉裁决」也交给 LLM。** ⭐ 整条流水线唯一的确定性组件（textX parser）只切原子、不判对错；⛔ **「这条 issue 是不是幻觉」这个最需要可信底座的判断，是由另一次 LLM 调用做的**。⭐ 后果他们自己量了：`MCeT-X` 误杀 158 条真 issue（14.4% 的真 issue）。⭐⭐ **这恰好从反面印证 M1 第二条设计原则**：⛔ 裁决者是 LLM 自评时，它的误杀率不可控；⭐ 我们手上有 pyfcstm，⛔ 不该重复这个形态。
2. ⛔⛔ **连投票计数都交给了 LLM。** ⭐ `prompt_holistic_vote_feedback.json` 逐字要求模型 *"Please find the issues that appear more than {threshold} times and report them"*，⛔ threshold = `vote // 2` = 2。⭐ **「数一个字符串出现了几次」是一个纯确定性任务**，⛔ 交给 LLM 只会引入额外方差，⛔ 而这一步的成本是一次全上下文调用。⭐⭐ **M1 的判据应当是：凡能被确定性做掉的聚合，一律不给 LLM。**
3. ⛔⛔ **权威等级的排序，是在评测集自己的 21% 上定的，⛔ 而那 21% 仍留在主结果里。** ⭐ Table I（16 图）用来决定「requirement-atom 是高权威」，⛔ 而 §V-B 明写那 16 图就是 *"the first 20% of the diagrams"*，⛔ §VI 又明写 Table II 是 *"applying MCeT on all pairs of sequence diagrams and requirements in FBench"*。⛔⛔ **没有留出集，且设计决定的调参集与报告集重叠。** ⚠️ 按本仓库 §3.5 口径，这属于需要显式声明的问题；⛔ 论文的 Threats to Validity **没有提这一点**。⭐ 对我们的启示不是「他们作弊」，⭐ 而是：**我们也不设留出集（永久裁定），因此更要把「哪一条规则是被哪个样本逼出来的」按引入动机逐条标注** —— ⛔ 靠「反正大家都不留出」是过不了自己的审查的。
4. ⛔ **8 条问题的正反冗余被浪费了。** ⭐ 正反两问本可以做成一致性信号（「说对又说要改」= 该 atom 可疑），⛔ 但代码里两问各自独立产 issue（`if 'No' in Answer` 就记一条），⛔ 矛盾不被检出，⛔ 反而**放大了 issue 数量**（diagram-atom 505 条 / precision 0.50）。⭐⭐ **陷阱形态：加冗余提问却不加冗余判据，只会把噪声乘以 2。**
5. ⛔⛔ **释出代码与论文描述不一致（M(code)，⛔ 我们自己写论文时的直接教训）。** ⭐ 论文 §IV-B / §IV-C 两处都写 *"we only keep issues appearing in N/2 of the LLM responses"* / *"We also utilize voting for this step"*，⛔ **但 HEAD `8b1b6507` 的代码里，这两个 check 的多数票过滤都不生效**：
   - `message_correctness_one_shot.py:223-236` —— 多数票那几行**被整段注释掉了**（`# questions_for_feedback_majority = [pair for pair in found_issues if q_number_counts[pair[1]] > (vote / 2)]`），⛔ 实际执行的是 `combine_by_atom`：**5 次采样的 issue 全量求并，再由 LLM 蒸馏成每 atom 一条**。
   - `requirement_correctness.py:141-215` —— 从头到尾**没有任何 threshold**，同样是**并集 + LLM 蒸馏**。
   - ⭐ 只有 holistic check 真的做了阈值过滤（且由 LLM 执行）。
   - ⚠️ **裁定态度**：⛔ 不能断言实验是这样跑的（释出代码可能晚于/早于实验版本），⭐ 但**能断言「按论文描述与按释出代码，得到的是两种不同的聚合语义」**（并集 vs 多数票，对 precision/recall 影响方向相反）。⭐⭐ **对我们的教训：方法描述里每一个「我们做了 X」都要能在代码里指出那一行。**
6. ⛔ **无外部 baseline。** ⭐ 全部对照是自己的 ablation。⚠️ 这与 L1 的实测结论一致（**外部可比数字 0 条**），⛔ 说明这个任务形状目前**整个领域都没有共同基线** —— ⛔ 我们不能指望从这里借一个 baseline 数。
7. ⛔ **主结果只用最弱模型，且自己给出了「方法收益会被代际吃掉」的证据。** ⭐ DeepSeek-R1 的裸 holistic 召回 50%，⛔ 已接近 GPT-4o-mini 全套 MCeT；⭐ 论文自己解释是因为 reasoning 模型**自发地做了类似 requirement-atom 的细粒度分解**。⛔⛔ **这是对「结构化多视角」这一类方法的普遍威胁**，⭐ 也是我们必须在 SOTA 模型上验证 M1 的直接理由。
8. ⛔ **无方差、无重复、无 `@k`。** ⭐ 5 次采样被内部吃掉，⛔ 不作为报告维度。⭐ 我们的 `hit@1/@3/@all` 三口径在这一点上**严格更强**，⛔ 不要向下对齐。

### 3. ⚠️ 与我们的关键差别（⛔ 为什么不能直接照搬）

| 维度 | MCeT | ⭐ 我们（v46） | ⛔ 后果 |
| :-- | :-- | :-- | :-- |
| 制品 | ⭐ 时序图（消息序列，**扁平**） | ⭐ pyfcstm 状态机（**层次 + 守卫 + 动作**） | ⛔ 「消息 + 两端参与者」这个 atom 定义在状态机上无对应物；⛔ 我们的 atom 至少要覆盖 state / transition / guard / action / hierarchy 五类，⛔ **他们的 8 条问题清单不能平移** |
| 判定装置 | ⛔ 纯 LLM（无 oracle） | ⭐ pyfcstm 求值器（sound） | ⭐ 我们有他们没有的东西；⛔ **不该向下兼容成纯 LLM 判定** |
| 输出形态 | ⛔ 自由英文散文 issue | ⭐ 可机械求值的断言脚本 | ⛔ 他们的 precision 只能靠人读散文来判（1524 条人工判定）；⭐ 我们的可自动求值 —— ⛔ **他们的成本结构与我们不可比** |
| 缺陷分类学 | ⛔⛔ **无**（零个类别） | ⭐ 19 条闭合谓词 + 五类多报分类 | ⛔⛔ **这正是「不作对照系」裁定的技术原因**：⛔ 没有共享类别，就没有共享分母，⛔ 65.2% 与我们的 60.4% **是两个不同分母上的数，不可并列** |
| 循环 | ⛔ **无**（严格前馈） | ⭐ 有（四条修订/契约循环） | ⭐ 他们从未付出修订成本，⛔ 所以他们的 6.7× 与我们的 212.6× **不是同一件事的两个取值** |
| 需求切分 | ⛔ LLM 自由切（开放） | ⭐ LLM 切 + 契约门 + 评审 | ⭐ 我们的切分有确定性门把关，⛔ 他们没有 |
| 谓词/问题选择 | ⛔ **不选**（8 条全问） | ⭐ **LLM 自动选**（从 19 条里挑） | ⭐⭐ **这是一个真正的形态差异**：⛔ 他们的清单只有 8 条，全问得起；⛔ 我们 19 条全问的成本与噪声都不可接受。⚠️ **但「全问」这条路值得 M1 重新算一遍账** —— ⛔ v46 的 324 格里 `edge_declared` 被问 **0.0%**，⭐ 而「不选、全问」在结构族上可能反而更稳 |
| 判定者 | ⛔ 本文两作者（$\kappa=0.79$，⛔ 其余单人判） | ⭐ 人工逐位判定（574 位 + 288 簇） | ⭐ 两边都是作者自判，⛔ 都有同一个偏置；⭐ **但他们报了 $\kappa$，⛔ 我们没有** —— ⭐⭐ **这是我们该补的一格** |

⭐⭐ **一句话结论**：⭐ MCeT 值得抄的是**「换视角重问」这个 token 分配策略**与**「不对称权威聚合」这个形态**，⛔ 绝对不值得抄的是**把判定与幻觉裁决全交给 LLM**。⭐ 我们与它的关系是：**它在没有 oracle 的情况下把 LLM 的组织形态做到了很不错的地步；我们有 oracle 却把它用错了位置。**

---

## F. ⛔ 用户额外提问的逐条回答

### F1 · ⭐⭐ 「自一致性多视角」到底怎么做的？

⭐ **先纠一个容易混的点：论文里有两套互不相同的机制，都被冠以 self-consistency 的名义。**

**机制 A · 视角内多次采样投票（N = 5）**

- ⭐ **是同一个模型跑多次** —— **确认**：M(code) `num_answers=num_votes` 即**一次请求取 5 个 completion**，`temperature=0.7`；⛔ **不是多个模型、不是多个 prompt**。
- ⭐ 聚合方式：**由一次额外的 LLM 调用做模糊计数**。M 逐字（§IV-A）：*"after collecting N sets of accuracy and completeness issues from N LLM responses, we do one more LLM invocation, this time asking the LLM to keep issues that appear in N/2 of the responses, and discard the rest. We use the language capability of LLMs for combining votes as the same issue could be phrased in different ways in each response."*
- ⛔ **所以不是投票、不是取交、不是取并 —— 是「LLM 判断哪些语义相同的 issue 出现了超过 2 次」。** ⭐ threshold 在代码里是 `vote // 2 = 2`（M(code) `holistic_correctness.py:206`）。
- ⚠️ **且只有 holistic 视角真的这么做**（详见 E2.5）：diagram-atom 的多数票代码被注释掉，requirement-atom 从来没有阈值，⛔ 两者实际是**并集 + LLM 蒸馏**。

**机制 B · 视角间「高权威交叉核查」（论文正文称 self-consistency）**

- ⭐ **几个视角：3 个** —— `Holistic`（整图 vs 整需求）· `Diagram-atom`（逐消息 vs 整需求）· `Requirement-atom`（整图 vs 逐原子需求）。
- ⭐ **是不是同一个模型跑多次：是。** ⛔ 三个视角用**同一个底层模型**（M：*"We use GPT-4o-mini within MCeT to evaluate the diagrams in FBench"*），⛔ 区别只在 **prompt 与输入切分粒度**，⛔ **不是多模型集成**。
- ⭐⭐ **聚合方式：不是投票、不是取交、不是取并 —— 是「单向否决 + 最后求并」。** 三步：
  1. ⭐ 取 `Correct Requirement-atoms` = MCeT-A 没报任何 issue 的那些原子需求；
  2. ⭐ 用它们分别去过滤 holistic issues 与 diagram-atom issues（**两次独立 LLM 调用**），⛔ 冲突者判为幻觉丢弃；
  3. ⭐ 把「过滤后的 holistic」+「过滤后的 diagram-atom」+「**未经过滤的** requirement-atom」**求并**。
- ⭐ **权威等级是靠角色扮演编码进 prompt 的**，M 逐字（§IV-D）：*"the prompt refers to the issues under check as issues found by a junior engineer, while the correct requirement-atoms as requirements found correct by a senior (higher authority) engineer."* ⭐ prompt 原文（`prompt_filter_diagram_issues_by_reqs.json`）：*"Here are some issues that a junior software engineer found in this diagram: {issues} Moreover, a senior engineer identified that all the parts in the diagram relevant to the following requirements are correct: {requirements} Now, go through all the diagram issues that the junior engineer found, and if any issues belong to parts in the diagram that the senior engineer deemed as correct, then discard this issue."*
- ⭐ **不是对称的**：requirement-atom 只否决别人、⛔ 自己不被否决（所以 Table II 里它的 A 列 = X 列）。
- ⚠️ **他们自己明说这不是典型 self-consistency**：*"Typical self-consistency relies on majority voting between several LLM responses [44], However, we rely on the observation that each different type of check has its complexities, strengths, and weaknesses [46]."*

**⭐⭐ 0.58 → 0.81 这两个数：核实结果 = 两个数都真，⛔ 但归因不能算在交叉核查头上。**

- ⭐ **0.58** = `Holistic check (Baseline)` 的 `MCeT-A` precision（Table II 第 1 列）。
- ⭐ **0.81** = `Combined checks` 的 `MCeT-X` precision（Table II 最后 1 列）。
- ⭐ 摘要逐字：*"Our combined approach improves upon the precision of the direct approach from 0.58 to 0.81 in a dataset of real requirements."*
- ⛔⛔ **关键拆解**：0.58 → 0.81 里**包含了两件事** —— ① 增加两个新视角（0.58 → **0.72**）；② 交叉核查（0.72 → **0.81**）。⭐ §VI-A 自己就把这一步写清楚了：*"Our combined atomic and holistic approach achieves a 0.72 precision which is improved to 0.81 with cross-checking."* ⭐⭐ **所以「自一致性交叉核查」的净贡献是 +0.09，不是 +0.23。** ⛔ 引用这篇时若只说 0.58 → 0.81 并归给 self-consistency，会**高估该机制约 2.5 倍**。
- ⚠️ 另有一组**不同的** 0.36 → 0.57（Table III，同为 GPT-4o-mini 但只跑 8 图子集）—— ⛔ **不要与 0.58 → 0.81 混用**，两者分母不同。

### F2 · ⭐⭐ 它怎么把需求拆成原子的？

- ⭐ **拆分是 LLM 做的，⛔ 不是人做的。** M 逐字（§IV-C）：*"This check leverage the reasoning capability of LLMs to split the requirements into requirement-atoms by an LLM invocation using prompt P-3."*
- ⭐ **原子的定义（作者定的，非借用）**：*"we define as a requirement that includes at most one action involving one or more participants"*，⭐ 例：*"the sentence 'Bob shall then ask cat for the user data, which she returns' is split into 'Bob shall ask cat for the user data', 'Cat shall return the user data to Bob'."*
- ⚠️⚠️ **但拆分 prompt 极其单薄** —— M(code) `prompt_requirements_split.json` **全文只有 631 字节**，逐字：*"Given the following requirements, split them into different requirements and place each as an entry in a Json Array"*。⛔⛔ **注意：这个 prompt 里根本没有出现「atom」「at most one action」「self-contained」等任何一条论文所述的原子性判据**，⛔ 也没有示例、⛔ 没有约束、⛔ 没有反例。⛔ **论文正文的原子定义没有进 prompt。**
- ⭐ **切分只做一次**（`num_answers=1`，M(code) `requirement_correctness.py:47`）—— ⛔ **切分本身不投票、不复采、不评审、不被任何门检查**。⚠️ 这是整条流水线的**单点故障**：所有 requirement-atom（最强视角）都建立在这一次未加约束的 LLM 调用之上。
- ⭐ **有覆盖账吗？分两层看：**
  - ⭐ **原子 → 判定 这一层有（确定性强制）**：M(code) 代码按位置枚举 `json_response["Analysis form"][req_num]`，⛔ 每个原子**必须**拿到 `Correct?` / `Complete?` 的 Yes/No，⛔ 拿不到就抛 `IndexError` 并重试（上限 20）。⭐ 所以**不存在「某个原子没被检查」**。⭐ 批大小 5（`slice_size = 5`）。
  - ⛔⛔ **需求文本 → 原子 这一层完全没有。** ⛔ **没有任何机制核对「切出来的原子是否覆盖了原需求全文」**：⛔ 无回译校验、⛔ 无覆盖率统计、⛔ 无「哪句话没变成原子」的登记。⛔ 论文**也从未报告原子数量**（既无总数、也无每图均值）。⛔⛔ **因此「哪些需求没被检查到」这个问题，在这篇工作里既无答案也无装置。**
- ⭐⭐ **对我们的直接对照**：⭐ 我们的 `split_requirements` 有契约门 + reviewer + 台账分母（98 条），⛔ **在覆盖问责这一格上我们严格更强**；⭐ 而他们靠「原子多到 885 条」的暴力覆盖拿到 59.3% 召回 —— ⚠️ **暴力覆盖没有覆盖证明，但确实有召回。**

### F3 · ⭐ 它的缺陷分类学是什么？

- ⛔⛔ **它没有缺陷分类学。** ⭐ 输出是**自由英文散文**，⛔ 唯一的分类是**二分**：`Correctness` 与 `Completeness`。
- ⭐ 这两个类别的定义**借自 Ferrari et al.**，M 逐字（§III）：*"1 Accurate: The behavior described by the model is consistent with the requirements, and 2 Complete: The model covers all requirements present in the text with sufficient detail. We borrow these definitions from prior work on manually evaluating sequence diagrams [5]."*
- ⭐ prompt 里对这两类还加了一条互斥纪律（M(code) `prompt_holistic_check.json`）：*"Do not deduct for the same mistake in both 'Correctness' and 'Completeness'."*
- ⭐ **最接近「闭合集合」的东西是那 8 条 Yes/No 问题**（见 B5）：4 维（消息正确性 / 完整性 / 参与者 / 方向）× 2 极性，⛔ **作者硬编码在源码里**，⛔ 不可配置、⛔ 不从语料归纳、⛔ 也不由 LLM 选择（**全部 atom 全问 8 条**）。
- ⛔ **谁定的**：`Correctness`/`Completeness` 两类 = 借自 [5]；8 条问题 = 作者自定，⛔ 论文正文**没有为这 8 条给出任何外部出处**（§III 只说 atom 概念参考 [41] Yue et al. TOSEM 2013，⛔ 且明确收窄到「消息 + 参与者」）。
- ⭐⭐ **这是「不作对照系」裁定的技术根据**：⛔ 没有类别，就没有共享分母；⛔ 他们的 issue 是散文、由人读判真假，⛔ 我们的是台账条目、按位判命中 —— ⛔ **65.2% 与 60.4% 不可并列。**

### F4 · ⭐ 判定谁做的？ground truth 怎么来的？有无一致性？

**判定（MCeT 输出的真/假）**

- ⛔⛔ **本文两位作者亲判。** M 逐字：*"we rely on the human judgement of two of the authors of this paper. Both authors are software engineers with 4 and 6 years of experience. One of the authors participated in teaching a software engineering course for three offerings where he graded sequence diagrams submitted by students. The other participated in teaching and grading for an algorithms course."*
- ⭐ **有标注者间一致性：Cohen's $\kappa$ = 0.79**，⭐ 在**前 20% 的图**上双人独立判后计算。M 逐字：*"We then measured the inter-rater reliability using the Cohen's kappa statistic [54], which results in 0.79, indicating a substantial agreement, close to 0.8 which indicates almost perfect agreement."*
- ⭐ 分歧处理：*"Afterwards, both authors discussed the rating of issues for which they disagreed. Both authors settled the disagreements and decided on a common approach of judging any future issues similar to the disputed issues."*
- ⛔ **其余 80% 分工单判**：*"we split the remaining MCeT-detected issues among both authors who proceeded to judge the correctness of each issue"* —— ⛔ 即**大多数判定只有一个判定者，无二审**。
- ⭐ 判定规模：**RQ1/RQ2 判了 1524 条，RQ3 判了 347 条**（M：*"we evaluated a total of 1524 issues for RQ1 and RQ2, and 347 issues for RQ3"*）。⛔ 这批标签**未随仓库释出**（见 D 节）。
- ⚠️ **自判偏置**：作者判自己工具的输出，⛔ §VII 承认了主观性（*"The subjective judgments from the two authors influences the evaluation"*）⭐ 但缓解手段只有 $\kappa$ 与统一判据，⛔ **无第三方复核、无盲判**。

**Ground truth（人报 issue）**

- ⭐ **来自 Ferrari et al. REW 2024 [5]，不是本文产出** —— ⭐ 这一点很关键：**ground truth 与被测工具的作者是两批人**，⭐ 这比判定环节干净。
- ⭐ 产生方式：*"Each generated diagram was scored on a zero-to-five scale by one of two researchers, who are also experienced software engineers, according to five metrics ... Whenever the score is not a perfect five, the researchers identified the issues in the diagram that affected the score, we use these issues as a ground truth of issues found in the diagram by experienced engineers."*
- ⛔ **原始 ground truth 的一致性未在本文给出**：*"More details on the steps taken to ensure the reliability of the ground truth are provided in Ferrari et al.'s paper [5]."* ⛔ **本文不报 Ferrari 侧的 $\kappa$**；⭐ 且注意 *"by **one of** two researchers"* —— ⛔ **每张图只有一个人打分**。
- ⭐ **等价判据是宽松的**（这会抬高 recall）：*"We define equivalent issues as issues that describe the same root cause of the problem in the diagram, even if they have different levels of details."* ⭐ 论文用 Fig. 5 举例：人说「整图缺条件」，MCeT 说「某条消息缺条件」，⭐ **判为等价**。⛔⛔ **这个「同根因即等价」的口径由作者自己执行、无第三方核，⛔ 且明显偏向抬高 FBench recall。**
- ⭐ **实测确认 ground truth 在仓库里**：84 个 `.score` 文件 + `correctness_mistakes_collection.txt`（62 行 CSV）。⭐ 示例逐字：`1.autopilot.v2,3,<= 6 is incorrect interpretation of at most 6`；`20.pacemaker.v0,2,not correct - who's user and who is new patient?` —— ⛔ **确实是自由散文，⛔ 无类别标签、⛔ 无消息级定位**。

### F5 · ⛔ 它自陈的 first 是怎么说的？（⚠️ 四处逐字 + 限定词标注）

⭐ **本仓库「说了四遍、限定词逐级脱落」这一记录 —— 核实结果：成立。** ⭐ 四处逐字如下（`grep` 全文，⛔ 无第五处）：

| # | 位置 | ⭐ 逐字原文 | ⭐ 携带的限定词 |
| :-: | :-- | :-- | :-- |
| **1** | **Abstract**（第 118 行） | *"In this paper, we propose MCeT, **the first fully automated tool** to evaluate the correctness of **a behavioral model, sequence diagrams in particular**, against its corresponding **requirements text** and produce a list of issues that the model has."* | ⭐ ①「fully automated」②「tool」（非 approach）③⭐ **「sequence diagrams in particular」**④「requirements text」⑤ 输出限定「produce a list of issues」。⛔ **无 TBOOK 谦辞** |
| **2** | **Introduction 末**（第 168 行） | *"**To the best of our knowledge**, MCeT is **the first LLM-based approach** to evaluate a behavioral diagram model against **free-style requirements texts**, detecting discrepancies between them, and **reporting all issue explanations in natural language**."* | ⭐ ①⭐ **「To the best of our knowledge」**②⭐ **「LLM-based」**（最强的一处收窄）③「free-style」④「reporting ... in natural language」。⛔ **丢了「sequence diagrams in particular」** |
| **3** | **Contributions (1)**（第 173 行） | *"We propose **the first automated behavioral model evaluation approach** to evaluate a behavioral diagram model against its **free-style requirements textual description**."* | ⛔⛔ **限定词最少的一处**：⛔ 丢了 TBOOK、⛔ 丢了「LLM-based」、⛔ 丢了「sequence diagrams in particular」、⛔ 丢了「fully」、⛔ 丢了输出形态限定。⭐ 只剩「automated」+「free-style」 |
| **4** | **Conclusions**（第 1122 行） | *"**To the best of our knowledge**, MCeT is **the first approach to perform fully automated evaluation of a behavioral model against its requirements**."* | ⭐ 保留 TBOOK 与「fully automated」；⛔⛔ **丢了「LLM-based」、丢了「sequence diagrams in particular」、丢了「free-style」、丢了 NL 输出限定** —— ⛔ **这是四处里覆盖面最宽的表述**（字面上把所有非 LLM 的形式化模型评测方法也一并否掉了，⛔ 而 §I 自己刚列过 [14]–[19] 那一串模型检查 / 定理证明工作） |

⭐⭐ **归纳**：⭐ 从摘要（5 个限定词、含图类限定）→ 引言（换成 TBOOK + LLM-based）→ 贡献（**限定词最少**）→ 结论（**范围最宽**）。⛔ **限定词并非单调递减，而是「在不同处丢掉不同的限定」**，⭐ 净效果是：⛔ **任何单独引用一处的读者都会得到一个比论文实际支持的范围更宽的主张。**

⭐ **另一处「可轻易适配任何建模语言」的原文（§IV 开头，第 287 行）：**

> ⭐ *"In our current approach, we process sequence diagrams in PlantUML, **however, the technique can be easily adapted to process any other modeling language**."*

⛔⛔ **这句话与它自己的 Threats to Validity 直接冲突**，§VII 逐字：

> ⛔ *"Finally, our approach may not generalize to other types of behavioral models, we aim to expand our study into other types of behavioral models as part of our future work."*

⭐⭐ **裁定**：⭐ 两句可以勉强并存（一句说「**语言**」= 具体语法，一句说「**模型类型**」= 语义种类），⛔ **但 §IV 那句没有任何证据支撑**：⛔ 全文只在时序图上评测，⛔ 且它们的核心 atom 定义（「消息 + 两端参与者」）是**时序图专有**的，⛔ 在状态机上根本没有对应物。⭐⭐ **对我们的用处**：⭐ 这正是「MCeT 是邻域标杆而非对照系」这条裁定的**论文自证**——⛔ 引用时若有人拿 §IV 那句主张它已覆盖状态机，⭐ 直接用 §VII 那句反驳。

### F6 · ⭐ 资产：prompt / 数据集 / ground truth 在不在里面？

⭐ **已 `git clone` 到 `/tmp/l3/assets/mcet/repo`（⛔ 未提交进仓库）实读。** ⭐ 三问的答案：

| 问 | 答 | 证据 |
| :-- | :-: | :-- |
| ⭐ **prompt 在不在？** | ⭐⭐ **在，且完整** | ⭐ `prompts/` 下 **11 个 JSON，51,876 字节**，已逐个读过；⭐ 含 holistic 的完整 few-shot 样例、junior/senior 角色扮演原文、投票聚合 prompt。⚠️ **一处例外**：8 条 atom 问题**不在 JSON 里**，⛔ 硬编码在 `message_correctness_one_shot.py:28-37` |
| ⭐ **数据集在不在？** | ⭐ **在，⚠️ 但计数与论文不符** | ⭐ `Ferrari/` 下 **84 组 `(.txt, .puml, .score)`**；⛔ 论文用的是 **76** 个变体，⛔ 仓库**无 eligibility 清单**说明剔除了哪些 |
| ⭐ **ground truth 在不在？** | ⭐⭐ **在，⭐ 且有两种形态** | ⭐ ① 84 个 `.score`（Ferrari 原始五维分 + `Observations:` / `Issues:` 散文）；⭐ ② `Ferrari/correctness_mistakes_collection.txt` —— **62 行 CSV `name,score,reason`**，即 correctness 维度的人工缺陷台账 |
| ⛔ **人工判定标签在不在？** | ⛔⛔ **不在** | ⛔ 那 **1524 + 347 条** 判定（precision 的全部依据）**没有释出**；⛔ 仓库里没有任何 run 输出、逐图 issue 清单或 token 记录 |
| ⛔ **license 在不在？** | ⛔ **不在** | ⛔ 无 `LICENSE` / `COPYING`（机械核验与 `git ls-files` 双证）。⚠️ **法律上默认 all rights reserved** —— ⛔ 若 M1 想直接复用其 prompt 或代码，**需先解决授权**，不能默认可用 |

⭐ **机械核验输出逐字**（`python3 -m tools.verify_assets`）：

```
| https://github.com/Huawei-TTE/MCeT | 🟢 | HEAD `8b1b65073e` · 文件 288（非文档 202）· release 0 · license 无 |
```

⭐ **人工补充**：⭐ 唯一 commit `8b1b65073e6ab57a5b2575656733c249967e3f83 "Hello MCeT" (2025-07-30)`；⭐ 22 个 `.py` / 5,887 行；⛔ 无测试、无 CI、无锁版本依赖；⛔ README 的运行入口写错（见 D 节）。

---

## G. ⛔ 存疑与未核项

1. ⚠️ **人报 issue 的总分母（135）是我反算的，⛔ 论文正文从未写出。** —— 由 Table II `92 (68.1%)` 与 `88 (65.2%)` 反算得 $92/0.681 = 135.1$、$88/0.652 = 135.0$，⭐ 两式自洽，⭐ 故 135 是可靠的（S 级）。⛔ 但**论文没给这个数**是一个真实的报告缺陷 —— ⛔ 读者无法在不做除法的情况下知道 recall 的分母。
2. ⚠️ **释出代码与论文的聚合语义不一致（并集 vs 多数票），⛔ 无法判定实验实际按哪一套跑的。** —— 已试过：⭐ 通读三个 check 模块、⭐ 查 `git log`（**只有一个 commit**，⛔ 无从比对时间线）。⛔ 仓库无 run 输出可反推。⭐ **本卡的处理**：只断言「两种语义不同」，⛔ 不断言实验跑的是哪种。
3. ⚠️ **`requirement-atom` 的数量完全未知。** —— 论文不报，⛔ 仓库无 run 输出。⛔ 因此「885 条 issue 摊到多少个原子上」「每图切出多少原子」都无法算，⛔ 也就无法评估其覆盖密度。
4. ⚠️ **权威等级的调参集（16 图）是否**确实**包含在主结果的 76 图内 —— 我判为「是」，⛔ 但论文没有一句话正面确认。** —— 依据：§V-B 说那 16 图是 *"the first 20% of the diagrams (according to the order in the FBench paper)"*，§VI 说 Table II 是 *"all pairs ... in FBench"*。⭐ 两句合起来只能推出重叠（S 级）。⛔ 论文**没有**「我们把这 16 图排除出主结果」这类声明，⛔ 也没有在 Threats 里提这一点。
5. ⚠️ **仓库 84 组 vs 论文 76 个变体的差额（8 组）具体是哪些，无法确定。** —— 已试过：⭐ 数 `.puml`/`.score`/`.txt`、⭐ 查 `correctness_mistakes_collection.txt`（62 行，⛔ 与 76 也不等）。⛔ 仓库无筛选清单。⛔ **直接后果：第三方无法复现论文的分母。**
6. ⚠️ **IEEE Xplore 正式版（`document/11245361`）未取。** —— 已试过：⭐ 只用了 arXiv v1 全文 + Crossref 元数据核 DOI。⛔ **因此无法排除 camera-ready 与 arXiv v1 存在数字或措辞差异**（⚠️ 尤其 F5 的四处 first 表述、⚠️ 以及 §VI-B 那处 `1,094` vs Table II `1096` 的不一致 —— ⛔ 后者在 arXiv v1 里是**真实存在的内部矛盾**，⭐ 由 `1096 − 158 = 938` 可判 Table II 的 1096 才是对的）。
7. ⚠️ **Table III 的 8 图子集是按「GPT-4o-mini 在主结果上的 per-case precision」分层抽的**（M：*"we split the 0-1 precision range into 8 equal segments, and randomly select one diagram from each segment"*）—— ⭐ 即**选样用了主实验的结果数据**。⭐ 他们的理由（覆盖好与坏两端）是站得住的，⛔ 但这使 RQ3 的绝对数字**不能当作独立子样本的无偏估计**。⛔ 我未能判定这对 Table III 的方向性结论（reasoning 模型更贵但更准）有多大影响。
8. ⚠️ **`prompt_filter_req_issues_by_diagram.json` 在仓库与 config 里都存在，⛔ 但论文完全没提。** —— 它做的是**反方向**过滤（用「正确的 diagram-atom」去否决 requirement-atom issues），⛔ 而论文明确说 requirement-atom 是不被过滤的高权威。⛔ 我无法确定它是死代码、是消融实验残留、还是实际参与了某个未报告的配置。⚠️ **若它实际生效，Table II 的 `Req.-Atom check` A 列 = X 列这条说明就不成立。**
9. ⚠️ **Ferrari 侧 ground truth 的标注者间一致性未知。** —— 论文推给 [5]，⛔ 我未取 Ferrari et al. REW 2024 原文核。⭐ 已知的是**每张图只有两位研究者中的一位打分**，⛔ 故那一侧大概率也没有逐图双标。
