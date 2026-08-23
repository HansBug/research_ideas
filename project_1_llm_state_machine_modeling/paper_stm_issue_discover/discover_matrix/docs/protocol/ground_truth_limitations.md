# expected issue 分母的已知缺口

> **现行 Judge 解释**：冻结 D2+D1 ledger 仍是 hit/recall 的唯一分母，但不是现实缺陷全集。
> 按 [issue #195 同步入口](./semantic_judge_protocol.md)，台账外发布报告必须先独立审计
> 核心主张：成立且全部 relation 为 NO 时是 `VALID_NOVEL`，不算 hit 或 FP；不成立或达不到
> 最低举证责任时才是 `INVALID`，且全部 relation 为 NO。不得从 ledger-unmatched 自动推出
> novel，也不得从 ledger-unmatched 自动推出 invalid。

> **评测侧边界**：本文件只说明台账分母的已知缺口，不定义当前谓词。文中的历史断言
> 名称和旧分层只用于解释台账形成过程；当前四族注册表、W1/W2 和变更门以
> [`pipeline/evidence_discovery/`](../../../pipeline/evidence_discovery/) 为准。

本文件记录 evaluator-side ground truth（Issue [#166](https://github.com/HansBug/research_ideas/issues/166) 的 47 条 E1）**系统性不覆盖**哪些问题类，以及每处缺口是"问题定义边界"还是"待补欠账"。它是论文 threats to validity 一节的直接材料。

判定命中的原则见 [hit_criterion.md](./hit_criterion.md)。**评测语料本身的建模对象筛选见 [nl_scope_rule.md](./nl_scope_rule.md)** —— 10 份 NL 中 1 份（其 6 个 pair 末位均为 8）要求 fork/join 与秒级计时，而 $M = (S, E, V, Tr, A)$ 既无正交区也无时钟，故该规约族不进入评测分母；该文件同时给出全量 / 筛选后 / 被排除部分的三份数字。原论文逐 case 的问题记录见 [paper_reported_problems.json](../../../archive/r10_ledger_v1_and_v46/scripts/paper_reported_problems.json)（由 [extract_paper_problems.py](../../../archive/r10_ledger_v1_and_v46/scripts/extract_paper_problems.py) 从论文公开 workbook 提取，60/60 对齐）。

---

## 1. 外部锚点：原论文自己记录了什么

原论文（Wang et al. 2025, Internetware，DOI 10.1145/3755881.3755926）的公开 workbook `Experiment Results.xlsx` / sheet `STM Results` 对 60 个生成结果逐 case 记录三类问题，各带 `Resolved` 标记。它是**台账构建期唯一可用的外部交叉核对源** —— ⛔ **不是 `hit@1` 的参照系**（⚠️ 按 L1 的 Q3 四条门它缺门①③：被检对象是该论文自己生成的模型、且全篇无缺陷 recall，逐条筛除见 [related_work/landscape/search_ledger.md](../../../related_work/landscape/search_ledger.md) 的 N-19）。

⭐ 之所以**可用于交叉核对**，正**因为**它的判定方式与我们不同，而我们**仅凭 NL 建立正向命题、禁止使用参考模型**。⭐⭐ **同一个属性在两种用途下符号相反**：判定方式不同 → 作独立第二来源**有价值**，作性能参照系**不可用**。

⚠️ **它的判定方式不是一种，是四种**（⛔ 本句 2026-08-12 更正 —— 原文写「它对着作者重建的参考模型算 grammar-point F1」，⚠️ 那**只描述了其中一类**）：**format** 由 PlantUML checker **自动**报 · **grammar** 人工对照 SysML 标准 · **semantic** 人工对照 55 条语义 · ⭐ **只有 requirements-consistency 这一类才走参考模型的 grammar-point F1**。

语义 / 需求一致性类共 50 条，散布 41 个 case：

| 论文语义类目 | 条数 | 涉及 case | 台帐有 E1 的 case | 覆盖率 |
| --- | ---: | ---: | ---: | ---: |
| **missing region（缺正交区）** | **18** | 18 | 7 | **39%** |
| composite state 误用 | 8 | 8 | 3 | 38% |
| **missing state / transition** | **7** | 7 | **1** | **14%** |
| interaction error | 7 | 7 | 5 | 71% |
| missing final state | 5 | 5 | 2 | 40% |
| pseudostate（junction / fork / join） | 5 | 4 | 4 | 100% |

四象限交叉：

| | 论文有语义错 | 论文无语义错 |
| --- | ---: | ---: |
| 台帐有 E1 | 17 | 12 |
| 台帐无 E1 | 24 | 7 |

---

## 2. 缺口一：正交并发（问题定义边界，不补）

**裁决：不补进 expected issue，作为 limitation 如实陈述。**

原论文的最大语义问题类是 `missing regions`（18 条 / 18 个 case，论文 Table 9 记 20 条）。台帐对其覆盖率仅 39%，其余 11 个 case 被排除，排除类型为 `E2a/pump_hierarchy_or_concurrency_ambiguity`、`E3/uav_concurrency_or_textual_effect_boundary`、`E2c/orthogonal_region_assertion_missing`。

**这不是方法未能检出，是本轮评测的边界**：本轮 Discover 实验的断言对象是 FSM / HSM / EFSM 类状态机模型，其形式定义中**不含正交区与并发语义**；同理，时间约束类（台帐 taxonomy 的 `TO`，实际 0 条）也不在本轮的断言对象内。语料侧有对应边界：R4.5 表示层的 `r4_5_boundary` 明写 `do not infer guard/effect/timing/concurrency`，`PlantUML concurrent region 29/29` 只保留结构与顺序、不声称已实现正交并发执行。

**论文中应如实写明**：分母系统性排除了基线论文最大的一类语义问题（18/50 = 36% 的语义条目），原因是该类不在本轮评测的断言对象内，而非方法未能检出。不得把该类的缺席呈现为 "这些模型没有此类问题"。§2.1 给出它与总纲创新点的关系。

### 2.1 与总纲创新点的关系（已裁定）

[TARGET.md](../../../../../TARGET.md) 第 238 行的创新点 1 写「系统性解决层次化状态、**并发行为**和时间属性的建模难题」。这与本节的 limitation **不冲突**，因为两者说的是不同的东西：

| | 对象 | 陈述 |
| --- | --- | --- |
| 总纲创新点 | **建模方法的能力** | 方法面向含层次、并发、时间的控制系统状态机 |
| 本节 limitation | **本轮 effectiveness 实验 oracle 的覆盖范围** | 这批 60 例的 expected issue 分母不含并发与时间类可判定命题 |

分母不含它们有两条独立于方法能力的原因：

1. **语料的表示层不推断并发与时间**。R4.5 的 `r4_5_boundary` 明写 `do not infer guard/effect/timing/concurrency`；`PlantUML concurrent region 29/29` 只保留结构与顺序，不声称已实现正交并发执行。所以即使方法能建模并发，**这批 FCSTM 制品里没有可供断言的并发语义**。
2. **oracle 无法在归因安全的前提下形成并发/时间命题**。台帐门槛要求逐 issue 绑定 attribution-safe source trace entry；并发相关的候选一律落在 `E2a/E2c/E3`（`pump_hierarchy_or_concurrency_ambiguity`、`orthogonal_region_assertion_missing`、`uav_concurrency_or_textual_effect_boundary`），时间类落在 `E2c/camera_timing_adapter_missing`。

**论文中的正确写法**：把它写成**评测边界**而非方法边界——"本次 effectiveness 实验的 expected issue 集合不含正交并发与时间约束类命题，因为该批语料的表示层按设计不推断这两类语义，oracle 亦无法在归因安全前提下形成对应命题；方法本身对这两类的支持不在本实验的度量范围内。"

不要写成"方法不支持并发"，也不要写成"这些模型没有并发问题"——后者与基线论文的记录直接矛盾（`missing regions` 是其最大语义类）。

---

## 3. 缺口二：over-specification（整类无槽位）

台帐的 8 类 taxonomy（`SH` / `IT` / `TR` / `GC` / `UA` / `EA` / `TO` / `DA`）**没有任何一类承担 "凭空多出的状态或迁移"**，而 `UA` 明确拒绝该角色（"单纯 NL 未提及不得归入 UA"）。

原论文**有**这一类：Table 10 的一级分类含 `Over-specification`，在 ACT 图上占 33%（9 例 `Extra ActivityNode`）。实例：`0001` 的作者 PlantUML 第 14 行 `OperationalState --> ClampingLoseState : Transition to Clamping Lose State`，而 `ClampingLoseState` 在该 case 的 NL 里从未出现。

**这是真缺口，不是问题定义边界**——多出的状态属于 FSM/HSM/EFSM 完全能表达的范围。

**这一轮把这个缺口量化了：60 pair 的逐条审阅判出 31 条 `extra`**（生成方多出、参考与 NL 都没有），占 154 条计入问题的 **20%**。它们**完全可归因于生成模型**，因此在候选分层（[manual_review/STRATIFICATION.md](../../ledger_v2/provenance/STRATIFICATION.md)）里单列为 `over_specification` 层并计入可入 E1。

分层过程还暴露一个判据陷阱，值得记下来：`over_specification` 与 `reference_only` 有**完全相同的词法外形**（理由都写「NL 未要求 / NL 从未提及 / 参考独有」），区别只在**缺失方向**——

| 档位 | 含义 | 可归因于生成方 |
| --- | --- | :-: |
| `problem` + 「NL 未要求」 | 参考有、NL 没点名、生成方缺 | ✗ |
| `extra` + 「NL 未要求」 | 参考没有、NL 没点名、**生成方凭空造** | ✓ |

只按词法判会把两者判反。首版分层正是如此：`0049`#4 与 `0056`#3 两条 `extra`（都是凭空新增）被归入 `reference_only` 并当作「不可归因」划掉。现由 `verdict` 短路决定，见 [stratify_candidates.py](../../../archive/r10_ledger_v1_and_v46/scripts/stratify_candidates.py) 的 `classify`，并有专门的回归测试。

**处理方式**：台帐若要收这一类，需新增一个 `OS` 类（8 类 taxonomy 现无槽位、`UA` 明确拒绝该角色）；若不收，则应在 threats 中按 31 条 / 20% 的规模明确列为整类漏判，而不再只说「整类无槽位」。

---

## 4. 缺口三：7 个 case 连候选都未记录

以下 7 个 case 论文记录了具体语义问题，台帐既无 E1、`observations` 亦为空，且全部标 `no_supported_finding`：

| case | LLM | 论文记录的语义问题 |
| --- | --- | --- |
| `0003` | GPT-4o | missing final state |
| `0012` | GPT-4 | missing final state |
| `0052` | Claude | missing final state |
| `0013` | GPT-4 | use region |
| `0022` | Llama | missing composite state |
| `0032` | Kimi | missing composite state |
| `0027` | Llama | missing regions |

`0003` / `0012` / `0052` 是同一 NL（HSUV）的三个不同 LLM，论文对三者都记 `missing final state`。

**`no_supported_finding` 这个 status 的措辞有风险**：它会被读成"该模型无问题"，而实际含义是 "仅凭 NL 在严格蕴含门槛下形成不了可执行命题"。这 7 个至少应改为 `candidate_only` 并补记候选与排除理由。

其中 `0013` / `0027` 属 §2 的正交并发缺口；`0003` / `0012` / `0052` 的 `missing final state` 与 `0022` / `0032` 的 `missing composite state` **不属于任何已声明的问题定义边界**，是待补欠账。

**一个可能的机会点**：台帐建立于当前 19 谓词体系之前，其"正向断言可执行"门槛是对 `transition_exists` / `transitions` / `states` / `initial_child` / `effect_deltas` / `path` 六个底层原语判定的。当前谓词表中的 `terminates`（直接判定某配置能否终止）与 `cardinality` / `containment` 可能使部分当年判不了的命题变得可判——**"终态存在"与"能终止" 不是一回事**，一个模型可以声明 `FinalState` 却到不了它。是否据此补充，见对应的裁决记录。

---

## 5. 缺口四：台账里的「pyfcstm 报了」是错的归因（⛔ 论文不得沿用）

**台账多条记录的 `statement` 把某些事实归给了 pyfcstm，实际上那是我们自己的表示层做的。** 最直白的一处是 `EIS-0047-01`，它逐字写着「pyfcstm 明确报 "PlantUML initial target outside child scope: CollisionAvoidanceSystem.Frontend.Idle"，并生成 InvalidInitialtr_0005 / InvalidInitialtr_0009」——这句诊断文本与这两个状态名**都由本仓库自己的** [`plantuml_source_lowering.py`](../../../pipeline/representation/src/paper_stm_representation/plantuml_source_lowering.py) 产生（消息在 `render_initial()`、占位符在其后一行的 `registry.reserve`）；pyfcstm submodule 全库对这三个字符串**零命中**。

同类归因错误还有 7 处，形如「pyfcstm 投影得到 …」「pyfcstm 投影确认 …」。**投影是我们的 `plantuml_source_lowering.py`，pyfcstm 只读投影的结果。** 少数确实成立的除外（例如 `EIS-0012-01` 讲的按声明顺序选边，确是 pyfcstm 的仿真语义）。

### ⛔ 台账不改，只在此登记

**`expected_issue_set.json` 保持冻结。** 它的 `statement` 是 v46 判定者的**比对对象**，事后修改被判定所依据的 ground truth，比修改结果更严重。故本条只登记、不回改，v46 的 588 位判定完全不受影响。

### 这条影响的是写作，不是数字

⛔ **论文不得出现「pyfcstm 报告了 X」这类表述。** 直接照抄台账措辞会在正文里留下一个审稿人一查即倒的错误归因。⚠️ **更正（2026-08-11）**：交付给模型的制品上，**那 6 个入口类 pair 的 `INIT` 家族诊断确为 0 条**。⚠️ **但全语料不是 0** —— 复算得 `W_INITIAL_UNCONDITIONAL_MISSING` **22 条 / 15 个 pair**（`0000 0002 0007 0008 0014 0016 0017 0018 0019 0030 0033 0040 0042 0050 0057`），其中 `0000` 那条原文正是 `EIS-0000-01` 描述的缺陷。⛔ **此前本处写「INIT 家族诊断为 0 条」是错的，已就地更正。** 更准确的表述是：**诊断存在，但不对模型可见** —— `discover/renderer.py` 只把 `working_contract.summary` 的三个 status key（`simulation_status` / `source_static_discovery_status` / `diagnostic_binding_status`）投进 prompt，**逐条诊断记录不进模型上下文**。

### ✅ 这条链路本身完全成立，不需要任何辩护

【用户明确裁定 2026-08-11】**「这个问题在转换阶段就暴露了，然后 fcstm STM0 里面如实反映了这一点，然后最终也因此输出了这一点，那没有任何毛病，非常合理。我们的贡献本身就是模型转换 + 问题发现，没有任何越界的主张。」**

所以这条链路是**方法按设计工作**，不是污染：缺陷在转换阶段暴露 → 中间表示如实反映 → 断言据此求值为假 → 报出来。contribution ① 主张的正是「模型转换 + 形式化检查 / 仿真 / 验证」这条完整链路，**报出它完全在主张范围之内**。

### ⛔ 论文里根本不提这件事

【用户明确裁定 2026-08-11】**「paper 里没必要提这件事，根本都不需要解释的，顶多是被人问了的话回答一下而已。」**

所以本节的定位是**备查**：它不是待写的内容，也不是待披露的局限。正文不声明、不免责、不给替代口径、不提占位符。⛔ 唯一的作用是当审稿人问起时能答得上来，以及**防止写作时抄错那一句**。

两句不能写，仅此而已：

1. ⛔ 不写「pyfcstm 报了**这个**缺陷」——⚠️ 具体到台账点名的那些入口类缺陷，**它确实一条都没报**（那 6 个 pair 的 INIT 家族诊断为 0）；⛔ 但**不要把这句话推广成「pyfcstm 什么都没报」**——全语料它报了 22 条 `W_INITIAL_UNCONDITIONAL_MISSING`（15 个 pair）。照抄台账措辞会犯的错是**归因**（把我们自己表示层发的诊断说成 pyfcstm 发的），不是「pyfcstm 完全沉默」。
2. ⛔ 不写「我们发现的是工具查不出的缺陷」——同样是越界主张，而且没必要

## 6. 分母的构成偏差（不是缺口，但必须披露）

E1 条数与 **NL 的具体程度**强相关，与 NL 长度无关：

| E1 条数 | 领域 | NL 词数 |
| ---: | --- | ---: |
| 11 | Digital camera | 282 |
| 10 | high-level driving module | **71** |
| 7 | autonomous mode | 434 |
| 0 | **base brake subsystem** | 80 |
| 0 | **HSUV** | 65 |

两个 NL 最含糊的领域在**全部 6 个 LLM 上都是 0 条**。原论文的模板规则第三条明写 "Requirements must avoid explicitly stating the number of elements or inter-element relations"，这直接压低了可形成的命题数。

同源的一个偏差是**可绑定性**：命题需要一个可绑定的状态名才能实例化。`0020` 有 `AutoFinalState` 这个名字故计 E1，`0050` 是同一缺陷但没有该状态名故计 E0。后果是 "模型越含糊、可判定缺陷越少"。

**因此 per-LLM 的 E1 矩阵（Claude 1 条 vs Kimi 13 条，13 倍）不得作为缺陷率比较呈现**，只能作为"可判定缺陷数"呈现，并与原论文 F1 的跨度（Claude 80.27 vs Kimi 66.68，1.2 倍）并列对照。

---

## 7. 建议的分母表述

不要写"60 个模型中共有 47 个缺陷"。如实写：

> 我们在 evaluator 侧构建了 N 条 expected issue，其定义是：**能仅凭 NL 文本形成正向命题、被作者源 PlantUML 直接矛盾、且在当前谓词面上可执行判定的作者源缺陷**。它不是 60 个模型缺陷的完备集，也不是缺陷率的无偏估计。已知系统性排除：正交并发与时间约束（问题定义边界）、over-specification（整类无槽位）；已知构成偏差：NL 具体程度与状态名可绑定性。
