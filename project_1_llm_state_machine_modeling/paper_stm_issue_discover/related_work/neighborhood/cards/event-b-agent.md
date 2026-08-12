# 卡片 · **Event-B Agent**（NL → Event-B，⭐ 模型检查 + 定理证明双 oracle，⭐ 反例与证明状态双通道引导修复）

⭐ **全文可得**：本地 [`baselines/event-b-agent/`](../../../../baselines/event-b-agent/) 有 `paper.pdf` + `paper_content.txt`（23 页全文，含 References）。⭐ **另外从官方 artifact 里取回了论文没给的两个数字**（循环上限）与 **4 份 prompt 原文**。

---

## A. 元信息

| 字段 | 值 | 级别 |
| :-- | :-- | :-: |
| `id` | `event-b-agent` | — |
| `title` | Event-B Agent: Towards LLM Agent for Formal Model Synthesis and Repair | M |
| `year` | ⭐ **2026**（正式发表年） | M |
| `venue` | ⭐ **FSE 2026** —— ⭐ *Proc. ACM Softw. Eng.* Vol. 3, No. FSE, Article FSE211 | M |
| `ccf` | ⭐ **A**（[ccf_venues/conf-a-fse/](../../../../../ccf_venues/conf-a-fse/)） | M |
| `doi` | ⭐ **`10.1145/3808218`** —— ⭐ **已核**：Crossref 返回 title 完全一致、container `Proceedings of the ACM on Software Engineering`、vol 3 / issue FSE / pp. **4804–4826**、published `2026-06-30`、publisher ACM。⚠️ **一处小口径差**：⭐ PDF 页脚写 `Article FSE211 (July 2026), 23 pages`，⭐ Crossref 给 `page 4804-4826` 与 `2026-06-30`；⭐ 二者不矛盾（⭐ 卷内页码 vs 文章号；⭐ 月份差一个月是 ACM 常见的 online-first 与 issue date 差） | M |
| `arxiv` | [2605.17475](https://arxiv.org/abs/2605.17475) —— ⭐ **已核**：arXiv API 返回 title 完全一致，`published 2026-05-17T14:23:45Z`，⭐ 且该记录**自带** `arxiv:doi = 10.1145/3808218`（⭐ 与上一行互相印证） | M |
| `artifact_type` | ⭐ **Event-B 形式模型**（context + machine；⭐ 变量 + 不变式 + 带守卫的事件 + refinement 链）+ ⭐⭐ **证明制品**（proof tree / proof obligations） | M |
| `task` | ⭐ **生成**（NL 需求 → 形式模型）+ ⭐⭐ **修复**（模型与证明**联合**修复）。⛔ 不是缺陷检测 | M |
| `boundary` | ⭐ **邻域** —— ⭐ Event-B 明列在 L3 硬门 2 的可收对象里。⭐ 结构上它是「变量 + 守卫 + 动作」的离散迁移系统（逐字 `An Event-B model M is a discrete transition system grounded in set theory and first-order logic`），⛔ **无时钟、无不变式意义上的 timing、无正交并发区**，⛔ 但也**没有显式命名状态集 $S$**（状态即变量赋值），⭐ 且多了 refinement 层与证明义务 —— ⭐ 故不判界内、不判界外 | S |

---

## B. LLM 应用形态

### B1 · 流水线阶段（⭐ **三大阶段 · 内含两个嵌套循环 · LLM 环节 4 类**）

```
[人] 提供 NL 需求文档 REQ（可含轻量标签如 EQP / FUN）
  ↓
① [LLM] Refinement Strategy Planning
     把 REQ 划分成 n 个不相交子集 REQ_M1..REQ_Mn（⭐ 每步一个 refinement level）
     + 提出每两步之间的 gluing invariant（⭐ 先用自然语言）
  ↓  （⭐ 全系统只跑 1 次 —— artifact 实测 #Calls = 1.00）
② 对每个 refinement step i：
     [LLM] Model Synthesis（⭐ JSON schema 约束，schema 编码了 Event-B 文法）
        ⇄ [确定性] parse + 编译进 Event-B  ──编译错误──▶ 回灌给同一个 LLM
                                              （⭐ 内循环 A：well-formedness）
  ↓
③ [LLM/确定性] Model & Proof Repair
     ①○ [sound oracle·ProB 模型检查器（有界）] 找违反 invariant 的反例 trace
              （⭐ 边界由 LLM 提议：model_checking_parameters prompt）
              ──反例──▶ [LLM] model repair
     ②○ [sound oracle·Rodin 自动证明器 + SMT（CVC4 / Z3 / PP）] 放 proof obligations
              ──失败的 PO + proof tree──▶ [确定性] pattern matching 命中 7 类 repair rule
                                        ──推荐规则──▶ [LLM] fix strategy decision
                                        ──选一个 atomic repair function + 参数──▶
                                        [确定性] 执行该 atomic function、更新 proof state
              （⭐ 内循环 B：直到 PO discharged 或 trial limit）
  ↓  ⭐ 每次改模型后 [确定性] **重放全部证明**，⛔ 被失效的证明不算成功
所有 refinement step 走完 ⇒ 终态模型
```

⭐ 阶段自陈（§1 逐字）：`(1) Refinement Stratey Planning. ... (2) Model Synthesis. ... (3) Model & Proof Repair.`
⭐⭐ **神经符号分工的自陈（§4.1 逐字，⭐ 这段是全文最该抄的一段）**：`Event-B Agent adopts a neurosymbolic design, where semantic tasks such as refinement planning, model synthesis, and repair are delegated to specialized LLMs, while deterministic components handle the rest. Model checkers, SMT solvers, and theorem provers verify synthesized models, pattern matching identifies candidate repair rules from the proof state, and atomic repair functions apply updates to models and proofs. This separation combines the flexibility of LLMs with the reliability of symbolic reasoning, achieving both semantic versatility and soundness.`〔M〕

### B2 · 每次 LLM 调用的角色

| 调用 | 角色 |
| :-- | :-- |
| Refinement strategy planning LLM | ⭐ **规划者**（拆需求到 refinement 步）+ **生成器**（提 gluing invariant 的 NL 草案） |
| Model synthesis LLM | ⭐ **翻译器**（NL 需求 → Event-B JSON）+ **修复者**（吃编译错误改 well-formedness） |
| Model repair LLM | ⭐ **修复者**（吃模型检查反例） |
| ⭐⭐ Fix strategy decision LLM | ⭐⭐ **规划者 / 选择器** —— ⛔ **它不写代码，只做两件事**：逐字 `(1) selecting the appropriate function based on the current proof state and recommended repair rules; and (2) proposing the values of function parameters` |
| （提模型检查边界） | ⭐ **规划者** —— 逐字 `The model repair LLM suggests suitable bounds, within which the model checker searches for states that violate invariants` |

⛔⛔ **同样地：本流水线里没有任何一次 LLM 调用担任「评审者」或「裁决者」。** ⭐ 裁决全部由 ProB + 定理证明器 + SMT 承担。〔S〕

### B3 · prompt 策略

`结构化输出约束`（⭐⭐ **JSON schema 直接编码 Event-B 文法** —— 逐字 `we design a JSON schema that encodes the grammar of Event-B shown in Figure 3. The schema encodes structural constraints, for example, every machine must contain at least one event, and may include variables, invariants, and variants`）· ⭐⭐ `工具调用 / function calling`（⭐ **修复动作被限制成一个函数库** —— 见 B5）· `few-shot`（⭐ artifact 里有 `system_desc_example.txt`）· `结构化反馈回灌`（编译错误 / 反例 / proof tree 逐字注入）· `角色扮演`（prompt 以 `Given the ...` 指令式开场）。⛔ **无 RAG · 无多智能体辩论 · 无 self-consistency 投票。**〔M〕

⭐⭐ **一条重要的形态观察（⛔ 论文正文没讲，⭐ 从 artifact prompt 原文看出来的）**：⭐ `fix_model_checking.txt` 里塞了一整段**通用 Event-B 建模纪律**，逐字节选：`For each variable v in machine, include an invariant 'v \in | \subset | \subseteq ...' to specify its type.` · `Make sure sets are not misplaced into constants, e.g. sets are types that are capitalized.` · `Clauses such as "if...else..." are not supported by Event-B, use two events with different guards to represent the logic.` · `Never remove machine or event refinements.`

⭐ 这些**全部是可写成 validator 的确定性约束**（⭐ 类型必须声明、set 不能当 constant、`if-else` 不合法），⛔ **但它们被放在 prompt 里而不是做成门**。⭐⭐ **这正好是本仓库 §11「schema validator 只放能完美判定的约束」的反向验证**：⭐ 一个 CCF-A 的成熟系统，把这类纪律放在**生成端 prompt + 编译器做最终裁决**，⛔ 而不是加一道会一票否决的 validator。〔M（prompt 逐字）+ S（对照 §11 的解读）〕

### B4 · ⭐⭐ 循环与裁决者（⛔ 本卡最重要的一格）

| 子字段 | 值 | 级别 |
| :-- | :-- | :-: |
| 有无循环 | ⭐⭐ **有，三层嵌套**：① well-formedness 循环（编译器裁决）· ② 模型检查修复循环（ProB 裁决）· ③ 证明修复循环（定理证明器 + SMT 裁决）；⭐ 外层再套 refinement step 的迭代 | M |
| ⭐⭐ **裁决者是谁** | ⭐⭐ **全部 `sound oracle` 或 `parser / 编译器`，⛔ 无一处 LLM 自评**：<br>① `parser / 编译器`（Event-B 编译）<br>② ⭐ `sound oracle` —— **ProB 模型检查器**（有界）<br>③ ⭐⭐ `sound oracle` —— **Rodin 自动证明器 + SMT（CVC4 / Z3 / PP）**（⭐ **无界**） | M |
| ⭐⭐ **验收权在 oracle 手里，不在规则手里** | ⭐⭐ §4.4.4 逐字（⭐ **这段是本卡对 M1 最直接的一句**）：`A sequence of repairs is accepted only if their combined effect discharges the target PO. Once discharged, SMT solvers and theorem provers guarantee its validity. After each model modification, all proofs are replayed to ensure that any invalidated proofs are not considered successful. As a result, soundness is ensured by the verification pipeline rather than the repair rules.` | M |
| 终止条件 | ⭐ **收敛或 trial limit**：逐字 `This procedure is repeated for each refinement step until all proof obligations are discharged or the trial limit is reached` · `This iterative process continues until the proof is discharged or the trial limit is reached` | M |
| ⭐ 最大轮数 | ⛔⛔ **论文只说「trial limit」，从不给数**（⭐ 已 grep 全文：只有 285 行与 495 行两处 `trial limit`，⛔ 无数值、无 `K_max`、无 `temperature`、无 `seed`）。⭐⭐ **artifact 里找到了默认值**：`AgentPreferenceInitializer.java` 逐字 `prefs.putInt(PREF_MAX_ATTEMPTS_SYNTH, 5);` · `prefs.putInt(PREF_MAX_ATTEMPTS_PROOF, 5);` —— ⭐ 即**合成侧 5 次、证明侧 5 次**（⭐ 两个独立预算）。⭐ 仓库 README 逐字确认这两项是可配的：`The remaining options control which component of Event-B Agent is enabled, and how many iterations of LLM invocations are allowed as specified in the paper`（⚠️ 「as specified in the paper」— ⛔ **但论文实际没写**） | ⭐ 论文侧：**原文未提供**；⭐ artifact 侧：**M** |
| ⭐⭐ 有无报告**逐轮**边际收益 | ⛔⛔ **没有。** ⭐ 见 B4a | M |

#### B4a · ⛔⛔ 逐轮收益：**本文不报**，⭐ 但报了两个**相邻但不等价**的东西

⛔ **必须先把三个「轮」分清，⛔ 混了就会错读**：

| 「轮」的种类 | 本文有没有报 | 说明 |
| :-- | :-: | :-- |
| ⛔ **修复轮**（第 1 轮 / 第 2 轮 …）| ⛔⛔ **没有** | ⛔ 这正是我们最想要的那一格，⛔ **本文完全没有** |
| ⭐ **refinement 步**（抽象模型 → 逐级具体）| ⭐ **有**（Fig 6）| ⭐ 见下表 |
| ⭐ **消融档**（有/无 repair guidance）| ⭐ **有**（Table 4）| ⭐ 见下表 |

⭐ **① 按 refinement 步的演化（Fig 6，§5.5 逐字）**：`Across all refinement steps, the average PDR is maintained at a consistently high level (97.86–98.50%). The average RC gradually increases from 31.19% in the abstract models to 97.13% in the final model, while average RF rises from 30.24% to 93.79%.`

| 指标 | 抽象模型（第 1 步） | 终态模型 | Δ |
| :-- | :-: | :-: | :-: |
| PDR | ~98.5% | 97.86% | ⭐ **基本平**（97.86–98.50% 区间内） |
| RC | 31.19% | 97.13% | **+65.94pp** |
| RF | 30.24% | 93.79% | **+63.55pp** |

⚠️ **但这不是「循环的边际收益」** —— ⭐ RC/RF 从 31% 涨到 97% 是**因为后面的 refinement 步才开始覆盖后面的需求**（⭐ 抽象模型按设计只覆盖 `REQ_M1`），⛔ **不是因为修复把错的改对了**。⛔ **不要把这条当成「有 sound oracle 的循环逐轮持续获益」的证据。**〔S〕

⭐ **② 消融（Table 4，Overall）—— ⭐ 这是唯一能量化「引导有多值钱」的一格**：

| 档 | PDR | RC | RF |
| :-- | :-: | :-: | :-: |
| (1) None enabled（⛔ 无 refinement、⛔ 无 repair guidance）| 0.9559 | 0.8363 | 0.7701 |
| (2) Refinement only | 0.9650 | 0.8955 | 0.8350 |
| (3) Repair guidance only | 0.9693 | 0.9494 | 0.8665 |
| ⭐ (4) Event-B Agent（全） | **0.9786** | **0.9713** | **0.9379** |
| ⭐ **(1) → (4) 的 Δ** | **+2.27pp** | **+13.50pp** | ⭐ **+16.78pp** |

⛔⛔ **一个必须记住的口径陷阱**：⭐ 「None enabled」**并没有关掉修复循环**，⛔ 只关掉了**引导**。⭐ 逐字 `This baseline isolates the capability of the LLM in model construction and repair when provided only with the model and verification results from the model checker and theorem provers.` ⛔ **所以本文没有任何「完全不修复」的对照臂** —— ⛔ **「修复循环整体值多少」在本文里无法算出来**，⭐ 只能算「引导比裸修复多值 +16.78pp（RF）」。〔M + S〕

#### B4b · ⭐⭐ 那么「有 sound oracle 的循环」到底花了多少钱？—— ⭐ 本文报了，⭐ 而且这个数很刺眼

⭐ Table 6（Overall，27 系统均值；⭐ Δ 与占比列由本卡自算，⭐ 三项 token 相加 `5348.19 + 99727.81 + 1552789.15 = 1657865.15` **与 Overall 完全相等**，⭐ 可复算）：

| 组件 | Time (min) | #Calls | #Tokens | ⭐ token 占比 |
| :-- | :-: | :-: | --: | :-: |
| Refinement Strategy Planning | 1.20 | 1.00 | 5,348.19 | **0.32%** |
| Model Synthesis | 25.07 | 13.59 | 99,727.81 | **6.02%** |
| ⭐⭐ **Model & Proof Repair** | **43.71** | **42.74** | **1,552,789.15** | ⭐⭐ **93.66%** |
| Overall | 74.45 | 57.33 | 1,657,865.15 | 100% |

⭐⭐⭐ **直接对照我们那条实测**：⭐ 我们的「修订机器吃 **79%** 的 token 而覆盖净变化 ≈ 0」；⭐ **它的修复机器吃 93.66% 的 token** —— ⛔ **比例更极端**。⭐⭐ **差别不在花了多少，⭐ 在于换回了什么**：⭐ 它换回 RF +16.78pp（⭐ 且这只是「引导」的增量，⭐ 修复整体的贡献更大但不可算），⛔ **我们换回 ≈ 0**。

⭐ 论文自己怎么为这个 93.66% 辩护（§5.4 逐字）：`The model & proof repair step takes on average 43.71 minutes, 42.74 LLM calls, and 1552789.15 tokens, largely due to high number of proof obligations (182.41 on average). #Calls is lower than PO count because many POs are discharged automatically, while the remaining require more complex reasoning or additional premises, where LLM-based model & proof repair becomes necessary.` ⭐ **即：把成本归因到「PO 条数」这个可解释的分母上，⭐ 并指出大多数 PO 是自动过的、LLM 只处理剩下的硬骨头。** ⭐⭐ **这个辩护结构可以直接借鉴** —— ⭐ 我们的 212.6× 也该挂到一个可解释的分母上（⭐ 台账条目数 / 断言条数），⛔ 而不是只报一个倍数。

⭐ 另一条同类辩护（§5.4 逐字）：`In practice, Event-B experts typically spend substantially more time on interactive proofs. In contrast, the average time to attempt discharging a single PO in Event-B Agent remains below 0.30 minutes across all partitions (0.18, 0.30, and 0.22 minutes), with an overall average of 0.24 minutes.` —— ⭐ **把绝对成本换算成「单位工作量成本」再和人类专家比。**

### B5 · ⭐⭐ 中间表示（⛔ 本卡第二重要的一格）

| 子字段 | 值 | 级别 |
| :-- | :-- | :-: |
| 有无 | ⭐ **有，三层** | M |
| 形态①：**JSON schema**（Event-B 文法）| ⭐ 编码 Fig 3 的完整文法 —— context（sets / constants / axioms / theorems）+ machine（refines / sees / variables / invariants / variants / theorems / events）+ event（any / where / then）。⭐ 逐字 `Because the schema is language-agnostic, it can be readily adapted to other formal specification languages` | M |
| 形态②：⭐⭐ **7 类 proof-state 修复规则目录**（Table 2）| ⭐ 逐字类名：`1 Contradictory Goal` · `2 True by Definition` · `3 Existential Goal` · `4 Equality PO` · `5 Well-Definedness` · `6 Quantified Invariant Preservation` · `7 Uninstantiated Hypothesis` + ⭐ 兜底：`If the current proof state does not fall into one of the known categories, the LLM falls back on a set of general default rules` | M |
| 形态③：⭐⭐⭐ **atomic repair function 库**（Fig 7，4 大类）| ⭐ 逐字：`Model modification strategies` · `Proof modification strategies` · `Joint model–proof modification strategies` · `Information Retrieval strategies`。⭐ 逐字定义「atomic」：`The functions are described as "atomic" because they represent the smallest modification units` | M |
| ⭐⭐ **是否闭合** | ⭐⭐⭐ **闭合** —— ⛔ 而且是**强闭合**：⭐ 逐字 `To mitigate this issue, Event-B Agent restricts modifications to a library of atomic repair functions (e.g., strengthen an invariant) that correspond to a set of fix strategies to update models and proofs.` ⭐⭐ **LLM 不能自由写编辑动作，只能从函数库里选一个并填参数。** ⭐ artifact 的 `fix_proof_with_strategy.txt` 逐字印证：`complete the proof by calling the most suitable function` · `Available Proof Tactics: {{proof_tactics}}` · `You must follow the ***rules for calling functions***` | M |
| ⭐⭐ **谁选类** | ⭐⭐ **两段式：确定性 pattern matching 先选「哪一类」，⭐ 然后 LLM 选「具体哪个函数 + 什么参数」。** ⭐ 逐字 `pattern matching identifies candidate repair rules from the proof state`（§4.1）· `Based on pattern matching over the proof state, the former retrieves repair rules to construct prompts for the latter`（§4.4.4）· `the fix strategy decision LLM analyzes the scenario, considers the recommended rules, and attempts repairs`（§4.4.2） | M |
| ⭐ 目录**从哪来** | ⛔⛔ **从作者自己手工做证明的经验里归纳的**，⭐ 论文明说：逐字 `These categories and rules were derived empirically based on our experience in manually discharging proofs. While not exhaustive, they capture recurring patterns observed across a wide range of models.` ⭐ §7.2 再次自陈：`The current libraries of repair rules and fix strategies are not exhaustive, as they were derived empirically from proof patterns across diverse systems.` | M |

⭐⭐⭐ **这是本簇对我们 B5 那一问的最强先例**：⭐ 我们是「**闭合 19 条谓词词表 + LLM 自动选**」；⭐⭐ 它是「**闭合 7 类规则（确定性 pattern matching 选）+ 闭合 atomic function 库（LLM 选）+ 兜底 default rules**」。⭐ **所以「闭合集 + LLM 自动选」不但有先例，⭐ 而且在 CCF-A 上被明确写成「用来抑制 LLM 幻觉」的手段**（逐字 `which may hallucinate during repair. To mitigate this issue, Event-B Agent restricts modifications to a library of atomic repair functions`）。

⭐ **实测各类被用到多少（Fig 7，§5.5 逐字）**：`model modifications account for 38.36% of successful invocations, followed by proof modifications at 33.62%. Joint model–proof modifications contribute 18.97%, ... retrieve information functions, such as model checking, make up 9.10%` —— ⭐⭐ **四类全被用到**，⛔ 没有「有一半词表没人用」的情况。⚠️ **对照我们 v46 只用到 15/19** —— ⭐ 这是一个可比的健康度指标。

### B6 · 模型

⭐ **单一 backbone，⛔ 无多模型对照**：⭐ `GPT-5`（medium reasoning，**2025-08-07 版**）。⭐ 逐字 `We use GPT-5 (medium reasoning configuration, 2025-08-07 version) as the backbone LLM in our experiments to demonstrate that formal model synthesis and repair remain challenging even for one of the most advanced LLMs.`

⭐⭐ **所有 baseline 用同一个 backbone**（Table 3 表注逐字 `GPT-5 with medium reasoning level is used as the backbond LLM for all methods.` —— ⚠️ 原文有 typo `backbond`）。⭐ **这是本簇里模型代际最新、也最公平的一家**：⛔ 与 PAT-Agent 的 o3-mini / claude-3-7 一代不同，⛔ **它的绝对数字不需要打太多代际折扣**。⭐ artifact 的 preference 里另有 `claude_key` / `gemini_key` 槽位，⛔ **但论文只报 GPT-5**。〔M〕

### B7 · ⭐ 确定性成分（⭐ 本簇最厚的一层）

| 环节 | 是什么 | 级别 |
| :-- | :-- | :-: |
| ⭐ **ProB 模型检查器** | 逐字 `model checking was performed by ProB, a model checker for Event-B that checks deadlock-freeness, liveliness, consistency of axioms, and invariants preservation`。⛔ **有界** | M |
| ⭐⭐ **Rodin 自动证明器 + SMT** | ⭐ `PP (Predicator Prover)` + `CVC4` + `Z3`。⭐⭐ **无界** —— 逐字 `theorem proving provides unbounded reasoning` | M |
| ⭐ **PO 生成器**（Rodin 原生） | ⭐⭐ **断言不是 LLM 造的，是工具从模型机械导出的** —— 见 C 节「断言从哪来」 | M |
| ⭐ Event-B 编译器 / parser | 逐字 `The candidate model is parsed and compiled into Event-B code. Compilation errors are fed back to the LLM` | M |
| ⭐⭐ **pattern matching 选规则类** | ⭐ 从 proof state（含 model / proof / repair history / PO type）机械命中 7 类之一 | M |
| ⭐⭐ **atomic repair function 执行器** | ⭐ LLM 只选函数与参数，⛔ **执行是确定性的**：逐字 `the LLM selects an atomic function and proposes the corresponding parameters, and the proof state is updated after executing the function` | M |
| ⭐⭐ **证明重放** | ⭐ 逐字 `After each model modification, all proofs are replayed to ensure that any invalidated proofs are not considered successful` —— ⭐⭐ **这是一道防「改 A 破 B」的确定性回归门** | M |
| ⭐ gluing invariant 的两步验证 | ⭐ 逐字 `(1) counterexample checking and contradiction detection with the model checker, and (2) attempting proofs relevant to the gluing invariants before other proofs. Only after no counterexamples are found and the proofs succeed, the gluing invariants will be accepted into M` | M |
| 集成环境 | ⭐ Rodin 3.9 IDE 插件（Java 17 + Eclipse 2024-03） | M |

---

## C. 实验

| 字段 | 值 | 级别 |
| :-- | :-- | :-: |
| `baseline` | ⭐ **有，三个，⛔ 全部适配到同一 I/O 设定与同一语言（Event-B）**：① `LLM + auto provers`（GPT-5 直接生成 + Rodin PP/CVC4/Z3 discharge）；② ⭐ `Cursor`（⭐ 商用通用 coding agent，⛔ **关掉 web search**，⭐ 其余功能保留）；③ ⭐⭐ `Adapted PAT-Agent`（⭐ 把 PAT-Agent 改造成产 Event-B：`mapping context and machine constructs to PAT's constants, variables, guarded actions, and processes; rewriting syntax documentation and examples in Event-B; replacing the PAT model checker with ProB ...; and omitting proof obligations`）。⭐ 逐字公平化处理：`After model synthesis by Cursor and PAT-Agent, we apply the automated provers from baseline (1) to their outputs, ensuring all baselines are evaluated under comparable conditions.` | M |
| `dataset` | ⭐ **27 系统 / 平均 182.41 PO**。⭐ 来源：Abrial 的经典 Event-B 开发 + 真实系统（EB4EB 文献）。⭐ 逐字 `we manually construct the requirement document based on the descriptions of the systems`（⛔ **需求文档是作者手写的**）。⭐ **三档划分口径明确且事前可得**：按需求条数分 `Simple`（3–8）/ `Medium`（9–13）/ `Complex`（14–24），⭐ **各 9 个**；⭐ 论文明说为什么用需求条数：逐字 `it is available prior to model construction and correlates with modeling complexity` · `Other potential metrics (e.g., proof size or structural properties) are either unavailable before construction or do not reliably reflect modeling difficulty` —— ⭐⭐ **「分档判据必须事前可得」这条口径值得直接借鉴** | M |
| `metrics` | ⭐ **三个，且都有形式化定义**：`PDR`（proof obligation discharge rate，分母 $\lvert PO_M \rvert$）· `RC`（requirement coverage，分母 $\lvert REQ_M \rvert$）· `RF`（requirement fulfillment = covered ∧ 相关 PO 全 discharged）。⛔ **无 `@k` 类多轮口径。** ⭐⭐ **但有一个我们没有的东西**：⭐ **`RF/RC` 比值**（见 C.2） | M |
| ⭐ `judged_by` | ⭐ **PDR 由 sound oracle 自动判**（⛔ 无争议）。⚠️⚠️ **但 RC / RF 是半自动的，⛔ 且有一处必须记的隐患**：⭐ 逐字 `During model construction, we instruct the corresponding LLM to generate labels for elements corresponding to the requirements they represent` —— ⛔⛔ **即「这个模型元素覆盖了哪条需求」是由生成模型自己贴标签的**；⭐ 作者做的补救是格式纠错：逐字 `In our experiments, this labeling is performed by LLMs but occasionally violates the expected format, affecting automatic matching and underestimating RC and RF. We manually corrected such cases for all methods to ensure fair and consistent evaluation.` ⛔ **纠的是格式，⛔ 不是「这个元素是否真的编码了那条需求」。** ⛔ **无标注者间一致性、无 $\kappa$、无第三方判定。** | M（引文）+ S（隐患解读） |
| `human_baseline` | ⛔ **无**（⛔ 无 user study）。⭐ 但 §5.4 有一句定性对比：`In practice, Event-B experts typically spend substantially more time on interactive proofs` —— ⛔ **无数字支撑** | M |
| `runs` | ⛔⛔ **未报运行次数、⛔ 未报方差、⛔ 未报 seed / temperature**（⭐ 已 grep：全文无 `seed` / `temperature`）。⭐ 论文用一段**换定义**的方式处理这件事（§7.1 逐字）：`Although GPT-5 introduces nondeterminism through stochastic decoding, we mitigate this via schema-based constraints and verifier-mediated acceptance. Moreover, reproducibility here refers to the stability of the improvement process rather than identical modeling outputs, as multiple correct models may exist. The PO-guarded repair ensures that accepted changes do not regress the model with respect to the target PO` | M |
| ⭐ `adverse_results` | ⭐ **处理得相当好，⭐ 三处** —— 见 C.1 | — |

### C.1 ⭐⭐ 它怎么处理不利结果（⭐ 三处，⛔ 都没藏）

⭐ **① 消融档在两个子集上打赢了全系统，⛔ 它照实报并解释**：

| 情形 | 数字 | 论文怎么写 |
| :-- | :-- | :-- |
| ⛔ `Simple` 上「Repair guidance only」的 RC/RF **高于**全系统 | .9861 / .9583 **vs** .9639 / .9417 | ⭐ 逐字 `On the "Simple" and "Medium" partitions, some ablations obtain marginally higher scores, but these gains are limited and do not persist across the dataset as a whole.` ⭐ 并进一步解释趋势：`This suggests that refinement becomes increasingly important for ensuring correctness in more complex systems.` |
| ⛔ `Medium` 上「Refinement only」的 PDR **高于**全系统 | .9861 **vs** .9700 | 同上 |
| ⛔⛔ `Complex` 上**最朴素的 baseline**（LLM + auto provers）的 RC **高于**全系统 | ⭐ **.9886 vs .9834** —— ⛔ **而且 Table 3 里这个 .9886 是加粗的（即标为最佳）** | ⭐ 论文用 RF/RC 比值把它解释掉（见 C.2），⛔ 但**没有在正文里点名说「这一格我们输了」** |

⭐ **② 「repair guidance 在复杂系统上会退化」也照实报**：逐字 `However, its PDR decreases as system complexity increases, likely due to implementation limitations. The repair module currently supports only a fixed set of atomic repair functions, which suffices for simple cases but is inadequate for more complex obligations.` ⭐⭐ **把退化归因到自己闭合库的不足** —— ⚠️ **这一条对我们尤其重要**（⭐ 我们的 19 条闭合词表面临同一风险）。

⭐ **③ refinement 假设不成立时会怎样，它自己量化了**：⭐ RC/RF 的可计算性依赖一个假设（逐字 `we assume that once a requirement is covered and fulfilled in an abstract model M_i, it remains so in the subsequent refinement models`），⛔ 而假设成立的证据是 Refinement PDR。⭐ Table 5 报的 `Refinement only` 档在 `Complex` 上 Refinement PDR **只有 46.53%**，⭐ 论文逐字：`without sufficiently validated refinement steps, the observed requirement-level metrics become inflated and unreliable`。⭐⭐ **即：它主动指出「在这一档，我自己的 RC/RF 是不可靠的」。**

### C.2 ⭐⭐⭐ `RF/RC` 比值 —— ⭐ 一个我们没有、但应该有的反真空指标

⭐ 逐字（§5.2）：`It is also worth noting that lower RC and RF values imply that PDR could have been superficially inflated, as the generated formal system may bypass more challenging requirements. Moreover, the ratio RF/RC for our method is 0.97, substantially higher than those of the three baselines (0.75, 0.77, and 0.82). This indicates that once a requirement is captured in the formal model, Event-B Agent is able to discharge nearly all corresponding proof obligations.`

⭐⭐ **这段做了两件我们没做的事**：
1. ⭐⭐ **点名「高 PDR 可能是靠绕开难需求刷出来的」** —— ⛔ 即**主动揭示自己主指标的作弊路径**，⭐ 然后用 RC 把它堵住。
2. ⭐⭐ **RF/RC 是一个「诚实度」比值** —— ⭐ 覆盖了多少 vs 覆盖了的里面证明了多少。⭐ 0.97 vs 0.75/0.77/0.82 说明 baseline 是「多报覆盖、少证明」。

### C.3 ⚠️ 真空性（vacuity）：⭐ 论文**明确讨论**，⛔ 但它把「让 PO 真空成立」当作**合法修复**

⭐ 三处逐字：
- §2.1：`FUN–1 is vacuously true for INITIALISATION and stop_empty events.`
- §5.5 修复案例 (3)：`Event-B Agent calls the StrengthenGuard function and adds grd7 : 1 ≤ i to event find_not_better, since i can never be 0 due to the design of the algorithm. As a result, the post-state invariant inv′ becomes vacuously true and the invariant preservation PO is discharged.`
- §4.4.4：`soundness is ensured by the verification pipeline rather than the repair rules.`

⭐ **我方读法**：⭐ 在 Event-B 里「收紧一个本来就不可能被违反的守卫」是**正当的**（⭐ 它把算法的真实前提显式化了），⛔ **但这个动作的形状与「靠让义务真空来过检查」是同一个形状**。⭐⭐ 而它的**防线不是禁止这个动作，而是 RC/RF**：⛔ 如果模型靠真空化绕开需求，⛔ RC 会掉（元素不再编码那条需求）。⭐⭐ **即：反真空不靠禁止，靠一个独立的覆盖度指标从侧面钉住。** 〔M（三处引文）+ S（读法）〕

### C.4 ⭐ 断言 / 性质从哪来（⭐ 本簇里最干净的一家）

| 来源 | 谁产的 | 有没有被验证 |
| :-- | :-- | :-- |
| ⭐⭐ **proof obligations** | ⭐⭐ **Rodin 工具从模型机械导出** —— ⛔ **不是 LLM 造的、也不是人写的**。⭐ 逐字（§1）`Proof obligations can be generated to ensure well-definedness of expressions, preservation of invariants, feasibility of events under their guards, and termination of the model` | ⭐ **不需要验证** —— ⭐ 它们是元模型定义性的 |
| ⭐ **requirement invariants** | ⭐ LLM 把 NL 需求形式化成 invariant / axiom / event | ⭐ 间接靠 RC/RF + PO 验；⛔ **没有独立检查「这条 invariant 是不是忠实翻译了那条需求」** |
| ⭐ **gluing invariants** | ⭐ LLM 提（先 NL，再形式化） | ⭐⭐ **有独立两步验证**（见 B7 最后一行）：⛔ 反例检查 + 矛盾检测 + **优先证明**，⭐ 三者都过才准进模型 |

⭐⭐⭐ **这是本簇对「性质本身对不对」这一问的最好答案**：⭐ **把断言的主体（PO）交给工具机械生成，⛔ 而不是让 LLM 造断言。** ⭐ LLM 只造两样东西：needs-formalizing 的 invariant，与 gluing invariant；⭐ **而后者被单独设了三重门。**

---

## D. ⭐ 资产（⛔ 逐条实际取过）

| 资源类型 | 状态 | URL / 路径 | ⭐ 核验证据 |
| :-- | :-: | :-- | :-- |
| 论文全文 | 🟢 | [arXiv:2605.17475](https://arxiv.org/abs/2605.17475) · [doi:10.1145/3808218](https://doi.org/10.1145/3808218) · 本地 `paper.pdf` | ⭐ arXiv API title 一致 + 该记录自带 ACM DOI · Crossref 记录一致 · ⭐⭐ **CC-BY 4.0**（PDF 首页逐字 `This work is licensed under a Creative Commons Attribution 4.0 International License.`）· 本地 23 页全文已通读 |
| ⭐ **实验代码** | 🟢 | [github.com/HongshuW/EventB_Agent](https://github.com/HongshuW/EventB_Agent) | ⭐ 逐字工具输出：`HEAD b6e9d83be2 · 文件 866（非文档 733）· release 0 · license 无`。⭐ 顶层实取：`Cursor_Pipeline_Adaptation/ EventB_Agent_Core/ EventB_Agent_UI/ PAT_Pipeline_Adaption/ data_analysis/ resources/ README.md .project .gitignore`。⭐⭐ **两个 baseline 的适配层都放了**（`Cursor_Pipeline_Adaptation/` 与 `PAT_Pipeline_Adaption/`）—— ⭐ 这在本轨里少见 |
| ⛔ **license** | 🟠 | — | ⛔⛔ **仓库无 LICENSE 文件**（⭐ 工具报 `license 无`，⭐ 顶层清单里确实没有）。⭐ 论文本身是 CC-BY 4.0，⛔ **但代码无授权声明** —— ⭐ 严格说**代码的复用授权不明**。⚠️ 与 PAT-Agent（至少有一份非商业 license）相比更弱 |
| ⭐ **数据集** | 🟢 | `resources/datasets/` | ⭐ 目录实取存在（⭐ `resources/` 下只有 `datasets/` 一个子目录）。⛔ **本轮未下钻到条目级**，⛔ 故未独立核到「27 个系统」这个数与其格式。⭐ README 逐字确认它是运行入口：`Dataset Location: full path to the dataset, e.g. <path to Event-B Agent>\resources\datasets` |
| ⭐ **实验结果细则** | 🟢 | `data_analysis/{raw_data,processed_data,scripts}/` | ⭐ 三个子目录实取存在。⭐⭐ **有 raw_data 与 scripts** —— ⭐ 即**从原始日志到成表的链路是放出来的**，⛔ 不只是论文里的表。⭐ README 逐字：`Event-B Agent > Collect Evaluation Data will extract the data and save to ...`。⚠️ **但逐轮修复数据是否在 raw_data 里，本轮未核** |
| ⭐⭐ **prompt 是否公开** | 🟢 | `EventB_Agent_Core/src/eventb_agent_core/llm/prompts/` | ⭐⭐ **全部是纯文本 / JSON，⭐ 本卡实际下载并逐字读过 3 份**。⭐ 完整清单（23 个文件）：`refine_strategy.txt` · `synthesize_machine.txt` · `refine_model.txt` · `fix_compilation_errors.txt` · ⭐ `fix_model_checking.txt` · ⭐ `fix_proof_with_strategy.txt` · `fix_proof_no_strategy.txt` · `model_checking_parameters.txt` · `system_desc_example.txt` · ⭐⭐ **7 类规则各一份 JSON**（`contradiction_in_goal_rules.json` · `wd_rules.json` · `card_wd_rules.json` · `equality_po_rules.json` · `existential_in_goal_rules.json` · `quantified_invariant.json` · `added_hyp_rules.json` · `inv_rules.json` · `gluing_inv_rules.json` · `general_rules.json`）+ ⭐ `simplified/` 下 4 份精简版。⭐⭐ **这是本簇 prompt 公开度最高的一家**（⛔ 对比 PAT-Agent 只给两张 PNG） |
| ⭐ **超参（论文没给的）** | 🟢 | `EventB_Agent_Core/src/eventb_agent_core/preference/AgentPreferenceInitializer.java` | ⭐⭐ 逐字取回：`prefs.putInt(PREF_MAX_ATTEMPTS_SYNTH, 5);` · `prefs.putInt(PREF_MAX_ATTEMPTS_PROOF, 5);` · `prefs.putBoolean(PREF_ENABLE_REF, true);` · `prefs.putBoolean(PREF_ENABLE_FIX, true);`。⭐ **即论文里含糊的「trial limit」= 5 + 5** |
| ⭐ Artifact / 复现包 DOI | 🟢 | [doi:10.5281/zenodo.19642103](https://doi.org/10.5281/zenodo.19642103) | ⭐ 逐字工具输出：`HTTP 200 · text/html; charset=utf-8`。⭐ 论文 §9 Data Availability 与脚注 1 都给了这个 DOI。⚠️ **只核到 200 与 content-type，⛔ 未核内容**（⭐ 未确认 Zenodo 包与 GitHub HEAD 是否一致、也未确认它非空壳） |
| ⛔ **可复现门槛** | 🟠 | README 「Prerequisite」 | ⚠️ ⛔ **重装成本很高**：`Java 17` + `Eclipse IDE for Eclipse Committers 2024-03` + `Rodin 3.9 developer version` + 手工配 target platform + 手装 `SMT Solvers` / `ProB for Rodin` / 可选 `M2E - SLF4J` 三个 Eclipse 插件站点。⭐ **代码全在，⛔ 但「拿下来就能跑」不成立** —— ⭐ 按简报「取到的够不够复现」这一维，⛔ 判 🟠 |

⭐ **总评**：⭐⭐ **prompt 与规则目录的公开度是本簇最好的**，⭐ 加上两个 baseline 适配层与 raw_data + scripts，⭐ **它是三家里最可审计的一家**。⛔ 两个扣分项：**代码无 license**、**环境重建门槛高**。

---

## E. ⭐ 对 M1 的意义

### 1. ⭐⭐ 可取之处

1. ⭐⭐⭐ **「LLM 只选函数 + 填参数，执行交给确定性执行器」这个形状是本簇最该搬的一件东西。** ⭐ 它的引入理由与我们完全同源（逐字 `the fix strategy decision LLM, which may hallucinate during repair. To mitigate this issue, Event-B Agent restricts modifications to a library of atomic repair functions`）。⭐⭐ **映射到我们**：⛔ 我们的 `convert_assertions` 目前让 LLM **自由写断言脚本**，⭐ 然后靠契约门事后拒；⭐ **它的形状是让 LLM 从固定动作库里选一个原子操作**。⭐ 后者的失败模式是「选错了函数」（⭐ 可枚举、可反馈、可重选），⛔ 前者的失败模式是「写出一个门永远不接受的东西」（⛔ 就是我们撞过的 18/18 死路）。
2. ⭐⭐⭐ **「断言主体由工具机械导出，⛔ 不让 LLM 造」**（C.4）。⭐ Event-B 的 PO 全是 Rodin 从模型算出来的，⭐ LLM 只负责把需求写成 invariant。⭐⭐ **映射到我们**：⭐ 我们已经有 pyfcstm，⭐ **「哪些性质该被检查」这件事本可以部分从元模型机械导出**（⭐ 可达性、确定性、完备性一类），⛔ 而不是每条都靠 LLM 从 19 条里选。⭐ 这与我们「把 pyfcstm 从求值端搬到裁决端」是同一个方向的两步。
3. ⭐⭐⭐ **`RF/RC` 这个「诚实度比值」+「主动揭示自己主指标的作弊路径」**（C.2）。⭐ 逐字 `lower RC and RF values imply that PDR could have been superficially inflated, as the generated formal system may bypass more challenging requirements`。⭐⭐ **映射到我们**：⭐ 我们的 `hit@k` 有一个对称的作弊路径 —— ⛔ **靠多报换命中**。⭐ 我们已经报五类多报，⛔ **但没有一个「命中/尝试」的比值指标**把它压成一个数。⭐ **`RF/RC` 是一个现成的形状**。
4. ⭐⭐ **「改模型后重放全部证明」这道确定性回归门**（B7）。⭐ 逐字 `all proofs are replayed to ensure that any invalidated proofs are not considered successful`。⭐⭐ **映射到我们**：⛔ 我们的修订循环目前**不检查「改这一条把已经对的那一条改坏了」**。⭐ 这道门是 0 token 的确定性检查（⭐ 对应我们 v46 里性价比最高的 `precheck_and_seal`）。
5. ⭐⭐ **成本辩护的两个结构**（B4b）：① **把总成本挂到一个可解释的分母上**（⭐ 它挂 PO 条数，⭐ 我们可以挂台账条数 / 断言条数）；② **换算成单位工作量再与人类专家比**（⭐ 它给 0.24 min/PO）。⭐ 我们的 **212.6×** 目前是一个裸倍数，⛔ 没有分母、⛔ 没有人类基线。
6. ⭐ **「分档判据必须事前可得」**（C 节 dataset 行）。⭐ 逐字 `it is available prior to model construction`。⭐ 一句话就把「按结果分档」的质疑挡住了。
7. ⭐ **消融档打赢全系统时照实报并解释趋势**（C.1 ①）。⭐ 我们要写 −15.82pp，⭐ 这个写法是直接模板。

### 2. ⛔ 不可取 / 陷阱

1. ⛔⛔ **它没有「完全不修复」的对照臂**（B4a 末），⛔ 所以**「修复循环整体值多少」在它的论文里算不出来**。⭐ 我们的 X1 恰恰有这个对照（⭐ 朴素单提示基线），⛔ **这一点上我们比它严格，不要退**。⭐ 反过来也意味着：⛔ **不能引 Event-B Agent 来支持「修复循环有正收益」** —— ⭐ 它只支持「引导比裸修复好」。
2. ⛔⛔⛔ **`RC` / `RF` 的标签是生成模型自己贴的**（C 节 judged_by）。⛔ 作者只纠了格式，⛔ 没有独立核实「这个元素真的编码了那条需求」。⛔ **这是一个真实的自证式风险** —— ⭐ 若我们照搬这个度量方式，⛔ 会踩本仓库 §3.5 第 5 条（自证式验证）。⭐ **我们的 574 位人工逐位判定在这一点上明显更硬。**
3. ⛔⛔ **闭合库在复杂样本上会不够用，⛔ 而且它自己承认了**（C.1 ②，逐字 `supports only a fixed set of atomic repair functions, which suffices for simple cases but is inadequate for more complex obligations`）。⛔ **我们的 19 条闭合词表面临完全相同的风险**，⭐ 而它给出的缓解手段是**分解**（⭐ refinement 把复杂系统拆小，让证明落回库的覆盖范围）—— ⭐ 逐字 `Refinement decomposes complex systems into smaller ones, in which proofs fall within the reach of the repair guidance system`。⭐⭐ **这个「用分解补闭合集的不足」的思路值得记**。
4. ⛔ **单一 backbone、⛔ 未报运行次数、⛔ 无方差、⛔ 无 seed**。⭐ 它用「reproducibility 指的是改进过程的稳定性而非输出一致」把这件事换了定义（C 节 runs 逐字）。⚠️ **这个换定义在缺陷检测任务上不成立** —— ⭐ 我们的 `hit@3` 与 `hit@all` 的差正是「采样稳定性」，⛔ 不能换掉。
5. ⛔ **让 PO 真空成立被当作合法修复**（C.3）。⛔ 若我们把裁决权交给 pyfcstm，⛔ **必须提前想清楚「靠让谓词真空成立来过门」算不算发现**。
6. ⛔ **代码无 license** —— ⭐ 反面教材。

### 3. ⚠️ 与我们的关键差别（⛔ 说明为什么不能直接照搬）

1. ⛔⛔⛔ **它有一个我们结构上没有的东西：机械导出的验证义务（PO）。** ⭐ Event-B 的元模型自带「什么必须被证明」（⭐ well-definedness / invariant preservation / feasibility / refinement / termination），⭐ 所以它的循环有一个**客观、完备、可枚举的目标集合**，⛔ 且**目标集合与被测对象无关地生成**。⛔⛔ **我们的任务没有这个** —— ⭐ 「模型违背了 NL 的哪一处」不存在一个元模型能机械导出的义务集。⭐⭐ **这是本卡最重要的一条差别**：⛔ 它的循环之所以能靠 sound oracle 收敛，⛔ **前提是目标是「让所有导出的义务被 discharge」这种单调、可判定、可穷举的目标**；⛔ 我们的目标（找出缺陷）既不单调也不可穷举。⛔ **所以「把裁决者换成 sound oracle」在我们这里不能是一比一移植**，⭐ 只能是「**把可机械导出的那一部分义务真正机械化**」+「**把 LLM 的动作空间收成闭合函数库**」这两件事。
2. ⛔ **任务方向相反**（生成+修复 vs 缺陷检测），⛔ 与 PAT-Agent 卡同一条差别。
3. ⭐ **制品邻域而非界内**：⭐ Event-B 无命名状态集、无层次结构，⛔ 我们的 $M$ 有 HSM 层次。⭐ 按 L3 规定不设边界门，⛔ **但进论文必须回 L1 重走**。
4. ⚠️ **规模**：⭐ 它 27 系统 / 平均 182.41 PO / 单 backbone / 次数未报；⭐ 我们 54 pair × 2 模型 × 3 轮 = 324 格 / 台账 98 条 / 三口径同报。

---

## F. ⛔ 存疑与未核项

1. ⚠️⚠️ **逐轮修复收益完全拿不到** —— ⭐ 已试过：① 通读全文 23 页（⛔ 无逐轮表）；② `grep -niE "trial limit|max.*iterat|round|budget|at most [0-9]"` 全文（⛔ 只命中两处无数值的 `trial limit`）；③ 检查 artifact `data_analysis/` 顶层（⭐ 有 `raw_data/` 与 `scripts/`，⛔ **未下钻到文件级，故不知道逐轮数据在不在里面**）。⭐⭐ **这是本卡最大的缺口，⭐ 也是最值得后续下钻的一处** —— ⭐ 若 `raw_data/` 里有逐轮日志，⭐ **就能自算出「有 sound oracle 的循环第 3–5 轮还有没有收益」这个我们最想要的数**。
2. ⚠️ **`trial limit = 5 + 5` 是 artifact 默认值，⛔ 不等于论文实验用值** —— ⭐ 已取到 `AgentPreferenceInitializer.java` 的 `initializeDefaultPreferences()`，⛔ **但论文没写实验时用的是不是默认值**，⛔ 也没有配置文件快照可对。⛔ **不得写成「论文用了 5 轮」。**
3. ⚠️ **Zenodo 包（`10.5281/zenodo.19642103`）只核到 HTTP 200** —— ⛔ 未核内容、⛔ 未核是否与 GitHub HEAD `b6e9d83be2` 一致、⛔ 未排除空壳。⭐ 已试过 `tools.verify_assets`（⛔ 它对非 GitHub 域只查 HTTP 头，⛔ 不查内容）。
4. ⚠️ **数据集未下钻到条目级** —— ⭐ 已试过 `gh api` 列 `resources/` 顶层（⭐ 只到 `datasets/` 目录名），⛔ **「27 个系统」这个数与其格式、有无 ground truth 均未独立核到**，⭐ 只有论文自陈。
5. ⚠️ **`Cursor` baseline 的版本 / 日期未报** —— ⭐ 论文引的是 `https://cursor.com/ Accessed: 2025-09-11`。⛔ **一个商用 agent 没有版本号，⛔ 该 baseline 数字不可复现。**
6. ⚠️ **Table 3 `Complex` 档 RC 那一格加粗给了朴素 baseline（.9886 > .9834），⛔ 正文没点名承认** —— ⭐ 它用 RF/RC 比值间接解释掉了。⚠️ 我方读法是「解释成立但没有明说输在哪」，⛔ **这是我方判断，不是论文的说法**。〔I〕
7. ⚠️ **每 PO 的 token 成本无法分解到「模型检查修复」vs「证明修复」** —— ⭐ Table 6 把两者合成一个 `Model & Proof Repair` 列。⛔ 因此**无法回答「有界模型检查那条循环和无界证明那条循环各花多少」**，⛔ 而这对我们选 oracle 很关键。
8. ⚠️ **PDF 是 arXiv v1（2026-05-17）；⛔ ACM 正式版（pp. 4804–4826）未取全文核对差异** —— ⭐ 已试过 Crossref 元数据（一致），⛔ 未取 ACM PDF。
