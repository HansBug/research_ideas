第二个问题：这些既在范围内、又该进 expected 的问题，在最近一次完整 8 格运行里漏了多少、怎么漏的。

先把两个口径分开，否则数字对不上：

| 口径 | 值 | 说明 |
| --- | ---: | --- |
| 8 格应命中的可入缺陷实例 | **22** | 每格按本轮人工结果应命中的条数之和 |
| 去重后命中 | **16** | 按人工 diff 去重的缺陷条数 |
| 漏检 | **6** | 27% |
| 多报 | **0** | 发布的 issue 无一条是人工复核不认的 |
| 实际发布 issue 条数 | 20 | 比去重缺陷数多，因为多条 issue 可描述同一缺陷（`0000` 的两条 `Power_Off`、`0029` 的 `REQ-007`+`REQ-008`）|

**16 + 6 = 22**，多报 0。也就是说这条流水线当前的问题不是乱报，而是**报得不够**。

### 漏在哪个环节

把 6 条漏检逐条追到流水线的**首失节点**。先说三点口径，否则这张表容易被读过头：

1. **6 条是实例数，对应 3 个去重缺陷**（`0000` / `0029` / `0050` 各跨 2 格）。形态只有「复合事件被合并」与「缺初始边」两类，**样本很薄**，不足以支撑「这条流水线在某类缺陷上系统性失效」这样的结论。
2. **`lost_at` 取首失点单值**，同一条可能被多个环节共同放过。`0000` 与 `0050` 的证据原文即记录 `review_requirements` 判了 accept 并把它列为已覆盖——该环节实际上也没拦住。
3. **本表的环节枚举不含 `prepare` / `review_requirements` / `publish`**，所以下面「其余环节各 0 条」只对枚举内的节点成立，**不能读成整条流水线中段无损失**。

| 环节 | 漏检数 | |
| --- | ---: | --- |
| `split_requirements`（拆需求） | **3** | |
| `bind_attribution`（绑归因） | **3** | |
| **合计** | **6** | |

枚举内其余 6 个环节各 0 条：`convert_assertions`（转断言）、`precheck_and_seal`（预检封存）、`review_assertions`（审断言）、`release_results`（放行）、`adjudicate_results`（裁决）、unknown。

**在被计数的环节里，漏检集中在头尾两端。**`convert_assertions` 到 `adjudicate_results` 这段是把需求变成断言、再变成结论的主干，它一条都没漏；丢失发生在「需求还没被拆出来」与「结论已经有了但被归因挡掉」这两处。但按上面第 2、3 点，这不等于中段无损失——`review_requirements` 被证据原文点名却没有计数桶。

### 归因这一关挡掉了多少

把 123 条可表述断言全部重放一遍归因，结果是：

| 归因结论 | 条数 | 占比 | 能否成为 expected issue |
| --- | ---: | ---: | --- |
| `safe` | **67** | 54% | 可以 |
| `representation_debt` | **38** | 31% | 不能——判定所依赖的元素落在该 pair 的 `attribution_exclusions` 里 |
| `unattributed` | **18** | 15% | 不能——找不到源头映射 |
| **合计** | **123** | 100% | |

**56 / 123 = 46% 的正确断言仅因归因就被挡住。**这是硬门控不是软降级：非 `safe` 的 False 会被强制移入 `excluded_findings`，无法成为 confirmed issue。

两档的成因**不同**，不能合并叙述：`representation_debt` 38 条全部是 `exclusion_intersection`，即判定所依赖的元素踩在 R4.5 投影合成出来的节点上（`UnspecifiedInitial`、`FinalWait*`、`InvalidInitial*`）；`unattributed` 18 条则是 `no_safe_trace_entry` 16 条与 `path_taint_ambiguous` 2 条，属「找不到可信源头映射」，**不是踩合成节点**。前者不是 bug——排除合成元素上的判定正是为了不把 converter 的产物记成生成方的缺陷；但代价是 **31% 的真实缺陷因为「证据踩在合成节点上」而无法上报**。

⚠️ 另需注明：这 123 条是把**人工手写的断言**重放一遍归因的结果，不是该次 8 格运行的实际产出分布，两者不可混读。

其中最尖锐的一处来自 `initial_target` 的两次归因修复。该谓词原先在两个分支上都不记录它读的那个 entry：`47f92913` 先补了多入口分支，本轮 `3d0049c1` 再补了单入口分支。如实记录后判定就开始踩到合成节点上——**`initial_target` 相关的 21 条里有 18 条（86%）为 `representation_debt`，跨 15 个 pair**（另 3 条为 `safe`）。按逐条回放复合态入口数，其中约 13 条由本轮的单入口分支修复直接导致，另 5 条（`0016`#1、`0029`#3、`0032`#1、`0048`#1、`0048`#2）来自上一轮已修的多入口分支。修复本身是对的（同一份证据不该因为走了哪个分支而给出两种归因），但它把「归因看不见」变成了「确定性排除」，把一个隐性偏差变成了显性、可计数的损失。

### prompt 侧：漏检是被指令要求的，不是没照做

**整条流水线里不存在任何「缺陷方向清单」。**prompt 是严格的 NL 义务驱动：一个候选 issue 只有在 (a) 某段 NL 把它陈述为义务、**且** (b) 19 个谓词之一能表达它 时才可能存在。8 个缺陷方向以及任何等价的分类法，**从未被告知给任何一个 producer**——而且这是设计使然，prompt 里有多处明令禁止引入 issue 分类：`prompts.py:7`「do not emit a benchmark issue taxonomy」、`prompts.py:19`「This rule does not import a hidden issue taxonomy」、`prompts.py:223`「Do not hard-code benchmark-specific partitions or expected issues」。

**因此 producer 能看到的唯一按方向的信号，是每个谓词那一行 `exposes:` 字段**（由 `predicates.py:754` 渲染）——19 个短语，埋在一个 18.7 KB 的词表块里。**没有任何一句话要求模型去排查**死端、吸收态、自造事件、克隆状态、未展开的子状态机或伪状态类型错误，在 NL 本身没把这些写成义务时尤其如此。

> 审计原文（保留英文，供核对）：There is no defect-direction checklist anywhere in the pipeline. The prompts are strictly NL-obligation-driven: a candidate issue can only exist if (a) an NL segment states it as an obligation, AND (b) one of the 19 predicates can express it. Neither the 8 directions nor any equivalent taxonomy is ever named to a producer -- by design.

三条主要成因。中文是本节的归纳，`>` 引用块内为 prompt 原文（证据，保留英文）：

1. **流水线只能报 NL 陈述为义务的东西，没有任何指令让它去找模型自身的缺陷。**按审计估算，153 条人工发现里约有 40 条落在「splitter 被明确要求不要为之开需求」的形状里**——死端与吸收态、终态集为空、自造事件、克隆状态、fork/join/junction/choice 类型错配、未展开的 `<<submachine>>`：这些缺陷是制品自身的属性，而不是对某句 NL 的复述，因此根本没有入口。**

   > prompts.py:6 'Cover every normative NL segment; mark descriptive context as context rather than inventing a requirement.' + prompts.py:526 'Derive the Requirement from the natural language, not from the model. You are shown the model so you can spell its identifiers correctly and see what it declares -- not so you can read the obligation off it.' + prompts.py:7 'never turn a tool warning into a requirement ... do not emit a benchmark issue taxonomy.'

   审计原文：This is a deliberate anti-leakage design and it is why the 19 `exposes:` phrases in predicates.py are the only defect-direction signal in a ~60 KB prompt. Every direction whose defect is a property of the artefact rather than a restatement of a sentence -- dead ends and absorbing states, an empty terminating set, self-invented events, clone states, fork/join/junction/choice type errors, an unexpanded `<<submachine>>` -- has no entry point. Roughly 40 of the 153 human items sit in shapes the splitter is instructed not to open a requirement for.

2. **三条「合并表示」豁免把真实缺陷转成了「表示层限制」，于是它们被当作需要披露的事项，而不是需要断言的缺陷。**

   > prompts.py:46 'If the model exposes one combined event for a natural-language conjunction or disjunction, use that exact declared event and state the representation limitation; do not invent separate atomic events from punctuation or an opaque label.' / prompts.py:62 'do not require nonexistent atomic events or reject solely because punctuation suggests an AND/OR interpretation' / prompts.py:82 'This helper proves indistinguishability only for empty or identical guards; an unsupported guarded case is a limitation, not an issue.'

   审计原文：These name the observed defect shapes almost verbatim -- '三个条件被压成一个复合事件名' and '条件被折进事件名' -- and pre-classify them as acceptable. The counter-rule that would stop this (prompts.py:113, 123 `Limitation non-waiver`) is scoped to 'source, trigger, destination, hierarchy, or effect mismatch' and does not reach event-merging or distinguishability. The knock-on is worse than the direct loss: once the merged event is accepted as the trigger, the source/event has a single target and `guard_distinguishable` returns vacuous True, so the distinguishability requirement that prompts.py:19-21 mandates for exactly this NL shape files as satisfied.

3. **入口与守卫这两个方向所依赖的两个谓词，恰好在有缺陷的那个配置上返回 True，而没有任何 prompt 文本对此预警。**

   > predicates.py:190-191 (all the splitter and reviewer are told about `initial_target`) 'asserts: entering this composite starts in this child / exposes: wrong or missing initial child; entry lands in the wrong mode' -- no `caveat` field is set, so no `boundary:` line is rendered; and predicates.py:280 'asserts: a shared source and trigger cannot reach two targets indistinguishably' with no statement that one target yields True.

   审计原文：Verified live: `[*] -> TurnOn : /Start` gives `initial_target("Root","Root.TurnOn") = True` while the same payload shows the producer `unconditional: false, trigger: Root.Start`; and a single-target source/event gives `guard_distinguishable = True`. Both are silent positive passes on the defect, so 'entry' (25 items) and 'guard' (22 items) -- the two largest directions after reachability -- fail closed. The prompt makes it worse by asserting the opposite semantics at renderer.py:88-89 ('a guarded or triggered entry is only taken when its condition already holds'), so a producer that reasons correctly from the payload still gets True and files the requirement satisfied. Neither behaviour is expressible any other way: no predicate can say 'the initial edge shall carry no trigger', and none can say 'this transition shall have a guard'.

**一个反向证据，用来排除最容易被想到的解释。**在全部 prompt 里检索数量上限类措辞（`at most` / `no more than` / `top N` / `most important` / `prioritise`）——**零命中**。没有任何 prompt 限制需求数、断言数或 issue 数，也没有任何一句让模型「只报最重要的几条」。唯一与数量有关的指令方向相反：`prompts.py:47` 要求「每条 Requirement 至少一条断言，且映射必须完整」。所以漏检不能归因于产出被截断或被要求精简——**是判定范围本身没把这些问题包进来。**

### prompt 说的与实现做的不一致：9 处

这类不一致比 prompt 写漏更危险——模型按 prompt 的描述去理解谓词语义，而谓词实际行为不同，于是它写出的断言在自己看来成立、在实现里落空。

| # | 谓词 | 造成的漏检 |
| --: | --- | --- |
| 1 | `initial_target` | the direct prompt-side cause of the '带触发的初始边' miss |
| 2 | `initial_target` | same root cause, stated as a second visible inconsistency in the payload text |
| 3 | `guard_distinguishable` | the direct prompt-side cause of the '同事件两目标不可区分' miss whenever the model has collapsed the alternatives |
| 4 | `cardinality` | makes `cardinality` return True on models whose author-owned mode count is wrong (measured: cardinality(0043.PumpControl, 3) = True over Region1 + Region2 + a synthetic node) |
| 5 | `reaches` | both directions: fabricated reachability defects from a short horizon, and no refusal to alert the reviewer |
| 6 | `reaches` | a `reaches` False can mean 'not reachable', 'you spelled it wrong', 'that is a pseudostate' or 'your horizon was short', and the prompt distinguishes none of them |
| 7 | `terminates` | removes the only expressible form of '整机不能终止' |
| 8 | `state_declared` | minor on its own; contributes to the pseudostate direction being invisible |
| 9 | `guard_distinguishable / FBMCQ` | no live effect found, but it is a stale contradiction sitting in the prompt module |

逐处完整引文（prompt 原文保留英文，那是证据）：

**1. `initial_target`**

- prompt 让模型这样理解：renderer.py:87-89 (`initial_entries_note`, in the splitter/reviewer/converter payload): 'Declared entries per composite. Entry takes an `unconditional` edge when one exists; a guarded or triggered entry is only taken when its condition already holds. `initial_target` claims are decided against this'. Combined with predicates.py:190 'entering this composite starts in this child', a producer reads: a triggered entry does not decide entry, so `initial_target` should be False for it.
- 实现实际怎么做：predicate_api.py:876-898 returns the single declared entry's target regardless of trigger or guard -- 'A single declared entry *is* the entry, whatever labels it. pyfcstm counts an edge as unconditional only when it carries neither guard nor event, so `[*] -> RunningState : /Activate_Pump` was "conditional" and the predicate refused -- on 22 of the corpus's 169 composites'. Reproduced: model `[*] -> TurnOn : /Start`, payload `{"unconditional": false, "trigger": "Root.Start"}`, `initial_target(composite="Root", child="Root.TurnOn")` -> True.
- 位置：renderer.py:87-89 vs assertions/predicate_api.py:876-898

**2. `initial_target`**

- prompt 让模型这样理解：renderer.py:99-105: 'When a composite lists two or more entries and none is unconditional, `initial_target` cannot answer at all and raises.' The implicature is that the single-entry case answers correctly.
- 实现实际怎么做：predicate_api.py:882-898 short-circuits on `len(entries) == 1` *before* any unconditional test, so the single-entry case answers from an edge the note has just told the producer is not decisive. The raise described in the note only covers `len(entries) >= 2 and no unconditional` (predicate_api.py:922-927).
- 位置：renderer.py:99-105 vs assertions/predicate_api.py:882-927

**3. `guard_distinguishable`**

- prompt 让模型这样理解：prompts.py:89 'When an accepted Requirement says alternative targets must be distinguishable, its predicate is `guard_distinguishable(source=..., trigger=...)` and it is *already* in the positive direction: True means no proven overlapping targets, False identifies the conflict.' predicates.py:280 'a shared source and trigger cannot reach two targets indistinguishably'.
- 实现实际怎么做：Also returns True when there is exactly one target -- predicate_api.py:1048 (`len(targets) <= 1 -> not indistinguishable`) and predicate_api.py:1007 (`not bool(conflicting_targets(...))` over an empty conflict set). 'True means no proven overlapping targets' is technically consistent, but the prompt never says that 'no alternatives declared at all' is one of the ways to get True, which is exactly the defect state.
- 位置：prompts.py:89 / predicates.py:280 vs assertions/predicate_api.py:1004-1007, 1040-1048

**4. `cardinality`**

- prompt 让模型这样理解：predicates.py:308 (rendered to the Requirement Splitter and Requirement Reviewer): 'count: an integer; pseudo-states are not counted'. predicates.py:300 'this scope declares exactly this many non-pseudo states'.
- 实现实际怎么做：predicate_api.py:1089-1090 counts every direct substate with `is_pseudo == False`, which includes converter-synthesised nodes (`UnspecifiedInitial`, `FinalWaittr_*`, `InvalidInitialtr_*`) -- these are ordinary states in the inspect table, not pseudostates. The converter and reviewer prompts know this (prompts.py:115, 125) but the requirement stages do not.
- 位置：predicates.py:300-308 (via vocabulary_prompt(), predicates.py:749-764) vs assertions/predicate_api.py:1089-1090; the missing warning is present only at prompts.py:115 and prompts.py:125

**5. `reaches`**

- prompt 让模型这样理解：prompts.py:62 (reviewer) 'What you can require is an adequate horizon: `within_cycles` on `occupancy_after` / `reaches`, `bound` on Family P.' and prompts.py:127 'A False produced by too small a horizon is a bounded artifact, not a defect, and publishing one is the failure this gate exists to stop.' Both sentences name `reaches` alongside `occupancy_after` as if the two behave the same way.
- 实现实际怎么做：`occupancy_after` has a horizon self-check that raises rather than returning a bounded False (predicate_api.py:1109-1134). `reaches` has none -- predicate_api.py:1273-1287 goes straight to `_reaches_within`, which returns a plain False. Verified: same binding, `within_cycles=1` -> False, `within_cycles=3` -> True, both silent. The prompt's 'gate' exists in code for one of the two predicates it names.
- 位置：prompts.py:62, 117, 127 vs assertions/predicate_api.py:1109-1134 (has the check) and 1273-1287 (does not)

**6. `reaches`**

- prompt 让模型这样理解：predicates.py:417-422 caveat names exactly one boundary -- 'It ignores triggers, so it cannot stand in for occupancy_after.' prompts.py:362 repeats it: '`reaches` ignores triggers and cannot stand in for `occupancy_after`.'
- 实现实际怎么做：Two further silent-False boundaries go unmentioned. (a) An undeclared but well-formed target returns False, not a refusal -- verified: `reaches(source="Root.Outer", target="Root.NoSuchState", within_cycles=3)` -> False. Its Family-S sibling `cardinality` refuses in the analogous case ('the model declares no state at ..., so it has no substates to count. A count over a scope that does not exist decides nothing', predicate_api.py:1084-1088), and `guard_distinguishable` refuses too (predicate_api.py:999-1003); `reaches` alone answers. (b) `hit()` matches only `cycle.active_states` (predicate_api.py:1431-1438), which never contains a pseudostate, so a pseudo target is a constant False.
- 位置：predicates.py:417-422 and prompts.py:362 vs assertions/predicate_api.py:1273-1287, 1431-1438; contrast predicate_api.py:1080-1088 and 998-1003

**7. `terminates`**

- prompt 让模型这样理解：predicates.py:446 field spec 'scope: the configuration to start from, or "[*]" for a cold start'; predicates.py:452 example `terminates(scope="[*]") # can the model finish at all from a cold start`; predicates.py:725-728 'That is true even when the claim is about the run ending: `terminates(scope="[*]")` asks whether a cold start can finish, and the anchor is still the initial configuration.'
- 实现实际怎么做：The call is legal, but the *requirement* carrying it is hard-rejected upstream unless `behavior_phase == "initialization"`: capability.py:687-714 `initialization_anchored_findings` raises in nodes.py:1246-1250 ('requirements are anchored or named against what the frozen model already says'), and prompts.py:211/524 forbid `[*]` outside initialization. A whole-machine 'can it ever finish' claim is naturally phase=termination, so the vocabulary advertises a call the requirement contract will not let through.
- 位置：predicates.py:446-452, 725-728 vs discover/capability.py:687-714 + prompts.py:211, 524, 543

**8. `state_declared`**

- prompt 让模型这样理解：predicates.py:106 'kind: one of "leaf" (no substates), "composite" (has substates), "pseudo" (an initial/final marker), or "any" (declared at all)'.
- 实现实际怎么做：predicate_api.py:750-758 accepts a wider alias set than the prompt lists -- 'leaf'\|'simple', 'composite'\|'submachine'\|'compound', 'pseudo'\|'pseudostate', 'any'\|'declared'\|''. Harmless in itself, but the schema Literal is built from the prompt's four values (predicates.py:576), and the prompt's gloss of 'pseudo' as 'an initial/final marker' is narrower than the model's own `is_pseudo` flag, which is how fork/join/junction/choice fall out of the vocabulary's field of view entirely.
- 位置：predicates.py:106 vs assertions/predicate_api.py:750-758

**9. `guard_distinguishable / FBMCQ`**

- prompt 让模型这样理解：prompts.py:351 (FBMCQ_CAPABILITY_BOUNDARY) 'Use `conflicting_targets(source=..., event=...)` for guard indistinguishability; it already ranges over every valuation and refuses to answer rather than guessing.'
- 实现实际怎么做：`conflicting_targets` is not callable from an assertion. environment.py:19-23 states the opposite: 'There is no `simulate`, no `fbmcq`, no `states`, no `transitions`, no `transition_exists`, no `path`, no `topology`.' The only reachable name is the predicate `guard_distinguishable`. FBMCQ_CAPABILITY_BOUNDARY is defined at prompts.py:350-353 and, on inspection, is never appended to any prompt -- it is dead text superseded by PREDICATE_EVIDENCE_BOUNDARY (prompts.py:355-366), which correctly says `guard_distinguishable`. Worth confirming before relying on either quote.
- 位置：prompts.py:350-353 (unreferenced) vs assertions/environment.py:19-23 and prompts.py:358


`initial_target` 那一行正是前面那个 86% 降级的源头：prompt 告诉模型「带触发的入口不决定进入」，而实现对单一入口一律照答，于是 `initial_target(Root, Root.TurnOn)` 在带触发的初始边上返回 `True`——**正向放过了一个有缺陷的模型**。

### 按缺陷方向看 prompt 的引导是否到位

| 方向 | 人工条数 | prompt 有引导 | 充分性 |
| --- | ---: | :-: | --- |
| `reachability` | 26 | ✓ | 不足 |
| `entry` | 25 | ✓ | 不足 |
| `guard` | 22 | ✓ | 不足 |
| `hierarchy` | 21 | ✓ | 部分充分（containment 充分，复合态未展开为无） |
| `effect_action` | 10 | ✓ | 不足 |
| `pseudostate` | 9 | ✗ | 无 |
| `event` | 5 | ✓ | 不足（且有反向禁令） |
| `cardinality` | 5 | ✓ | 不足 |

8 个方向里 **8 个的引导被判为不充分**。注意「有引导」与「充分」是两件事：多数方向 prompt 都提到了，但提到的是谓词能证明什么，不是「该去找哪种缺陷」。

---

逐格审计数据（8 格，含每格已发布 issue、漏检条目与环节归属）：[loopaudit_cells.json](https://gist.github.com/HansBug/daa977482df22711e8e0d00fc80c406c#file-loopaudit_cells-json) ｜ 归因重放（123 条逐条）[loopaudit_replay_attribution.json](https://gist.github.com/HansBug/daa977482df22711e8e0d00fc80c406c#file-loopaudit_replay_attribution-json) ｜ prompt 审计 [loopaudit_prompt.json](https://gist.github.com/HansBug/daa977482df22711e8e0d00fc80c406c#file-loopaudit_prompt-json) ｜ 过滤器审计 [loopaudit_filters.json](https://gist.github.com/HansBug/daa977482df22711e8e0d00fc80c406c#file-loopaudit_filters-json)
