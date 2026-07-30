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

把 6 条漏检逐条追到流水线的具体节点：

| 环节 | 漏检数 | |
| --- | ---: | --- |
| `split_requirements`（拆需求） | **3** | |
| `bind_attribution`（绑归因） | **3** | |
| **合计** | **6** | |

其余 6 个环节各 0 条：`convert_assertions`（转断言）、`precheck_and_seal`（预检封存）、`review_assertions`（审断言）、`release_results`（放行）、`adjudicate_results`（裁决）、unknown。

**漏检集中在头尾两端，中间环节没有丢失。**这一点很重要：`convert_assertions` 到 `adjudicate_results` 这段是把需求变成断言、再变成结论的主干，它一条都没漏。丢失发生在「需求还没被拆出来」和「结论已经有了但被归因挡掉」这两处。

### 归因这一关挡掉了多少

把 123 条可表述断言全部重放一遍归因，结果是：

| 归因结论 | 条数 | 占比 | 能否成为 expected issue |
| --- | ---: | ---: | --- |
| `safe` | **67** | 54% | 可以 |
| `representation_debt` | **38** | 31% | 不能——判定所依赖的元素落在该 pair 的 `attribution_exclusions` 里 |
| `unattributed` | **18** | 15% | 不能——找不到源头映射 |
| **合计** | **123** | 100% | |

**56 / 123 = 46% 的正确断言仅因归因就被挡住。**这不是 bug——把 R4.5 投影合成出来的元素（`UnspecifiedInitial`、`FinalWait*`、`InvalidInitial*`）上的判定排除掉，正是为了不把 converter 的产物记成生成方的缺陷。但它的代价是：**接近一半的真实缺陷因为「证据踩在合成节点上」而无法上报。**

其中最尖锐的一处来自我自己这轮的修复。`initial_target` 原先在单入口分支上不记录它读的那个 entry，我把它改成如实记录后，该谓词的判定就开始踩到合成节点上——**`initial_target` 相关的 21 条里有 18 条（86%）因此降为 `representation_debt`，跨 14 个 pair。**修复本身是对的（同一份证据不该因为走了哪个分支而给出两种归因），但它把「归因看不见」变成了「确定性排除」，把一个隐性问题变成了显性的、可计数的损失。

### prompt 侧：漏检是被指令要求的，不是没照做

**There is no defect-direction checklist anywhere in the pipeline. The prompts are strictly NL-obligation-driven: a candidate issue can only exist if (a) an NL segment states it as an obligation, AND (b) one of the 19 predicates can express it. Neither the 8 directions nor any equivalent taxonomy is ever named to a producer -- by design.**

The only per-direction signal a producer ever sees is the one-line `exposes:` field of each predicate, rendered by predicates.py:754 (`lines.append(f" exposes: {item.proves}")`). That is 19 short phrases inside an 18.7 KB vocabulary block. Nothing tells the model to sweep for dead ends, absorbing states, spurious events, clone states, unexpanded submachines, or pseudostate type errors when the NL……

三条主要成因，逐条附 prompt 原文与位置：

1. **The pipeline can only report what the NL states as an obligation, and nothing tells it to look for model-side defects.**

   > prompts.py:6 'Cover every normative NL segment; mark descriptive context as context rather than inventing a requirement.' + prompts.py:526 'Derive the Requirement from the natural language, not from the model. You are shown the model so you can spell its identifiers correctly and see what it declares -- not so you can read the obligation off it.' + prompts.py:7 'never turn a tool warning into a requirement ... do not emit a benchmark issue taxonomy.'

   This is a deliberate anti-leakage design and it is why the 19 `exposes:` phrases in predicates.py are the only defect-direction signal in a ~60 KB prompt. Every direction whose defect is a property of the artefact rather than a restatement of a sentence -- dead ends and absorbing states, an empty terminating set, self-invented events, clone states, fork/join/junction/choice type errors, an unexpanded `<<submachine>>` -- has no entry point. Roughly 40 of the 153 human items sit in shapes the splitter is instructed not to open a requirement for.

2. **Three merged-representation waivers convert real defects into 'representation limitations' to be disclosed rather than asserted.**

   > prompts.py:46 'If the model exposes one combined event for a natural-language conjunction or disjunction, use that exact declared event and state the representation limitation; do not invent separate atomic events from punctuation or an opaque label.' / prompts.py:62 'do not require nonexistent atomic events or reject solely because punctuation suggests an AND/OR interpretation' / prompts.py:82 'This helper proves indistinguishability only for empty or identical guards; an unsupported guarded case is a limitation, not an issue.'

   These name the observed defect shapes almost verbatim -- '三个条件被压成一个复合事件名' and '条件被折进事件名' -- and pre-classify them as acceptable. The counter-rule that would stop this (prompts.py:113, 123 `Limitation non-waiver`) is scoped to 'source, trigger, destination, hierarchy, or effect mismatch' and does not reach event-merging or distinguishability. The knock-on is worse than the direct loss: once the merged event is accepted as the trigger, the source/event has a single target and `guard_distinguishable` returns vacuous True, so the distinguishability requirement that prompts.py:19-21 mandates for exactly this NL shape files as satisfied.

3. **The two predicates the entry and guard directions depend on return True in precisely the defective configuration, and no prompt text warns of it.**

   > predicates.py:190-191 (all the splitter and reviewer are told about `initial_target`) 'asserts: entering this composite starts in this child / exposes: wrong or missing initial child; entry lands in the wrong mode' -- no `caveat` field is set, so no `boundary:` line is rendered; and predicates.py:280 'asserts: a shared source and trigger cannot reach two targets indistinguishably' with no statement that one target yields True.

   Verified live: `[*] -> TurnOn : /Start` gives `initial_target("Root","Root.TurnOn") = True` while the same payload shows the producer `unconditional: false, trigger: Root.Start`; and a single-target source/event gives `guard_distinguishable = True`. Both are silent positive passes on the defect, so 'entry' (25 items) and 'guard' (22 items) -- the two largest directions after reachability -- fail closed. The prompt makes it worse by asserting the opposite semantics at renderer.py:88-89 ('a guarded or triggered entry is only taken when its condition already holds'), so a producer that reasons correctly from the payload still gets True and files the requirement satisfied. Neither behaviour is e……

**一个反向证据，用来排除最容易被想到的解释。**在全部 prompt 里检索数量上限类措辞（`at most` / `no more than` / `top N` / `most important` / `prioritise`）——**零命中**。没有任何 prompt 限制需求数、断言数或 issue 数，也没有任何一句让模型「只报最重要的几条」。唯一与数量有关的指令方向相反：`prompts.py:47` 要求「每条 Requirement 至少一条断言，且映射必须完整」。所以漏检不能归因于产出被截断或被要求精简——**是判定范围本身没把这些问题包进来。**

### prompt 说的与实现做的不一致：9 处

这类不一致比 prompt 写漏更危险——模型按 prompt 的描述去理解谓词语义，而谓词实际行为不同，于是它写出的断言在自己看来成立、在实现里落空。

| 谓词 | prompt 让模型这样理解 | 实现实际怎么做 | 级别 |
| --- | --- | --- | :-: |
| `initial_target` | renderer.py:87-89 (`initial_entries_note`, in the splitter/reviewer/converter payload): 'Declared entries per composite. Entry takes an `unconditional` edge when one exists; a guarded or triggered entry is only taken when its condition already holds. `initial_…… | predicate_api.py:876-898 returns the single declared entry's target regardless of trigger or guard -- 'A single declared entry *is* the entry, whatever labels it. pyfcstm counts an edge as unconditional only when it carries neither guard nor event, so `[*] ->…… | the direct prompt-side cause of the '带触发的初始边' miss |
| `initial_target` | renderer.py:99-105: 'When a composite lists two or more entries and none is unconditional, `initial_target` cannot answer at all and raises.' The implicature is that the single-entry case answers correctly. | predicate_api.py:882-898 short-circuits on `len(entries) == 1` *before* any unconditional test, so the single-entry case answers from an edge the note has just told the producer is not decisive. The raise described in the note only covers `len(entries) >= 2 an…… | same root cause, stated as a second visible inconsistency in the payload text |
| `guard_distinguishable` | prompts.py:89 'When an accepted Requirement says alternative targets must be distinguishable, its predicate is `guard_distinguishable(source=..., trigger=...)` and it is *already* in the positive direction: True means no proven overlapping targets, False ident…… | Also returns True when there is exactly one target -- predicate_api.py:1048 (`len(targets) <= 1 -> not indistinguishable`) and predicate_api.py:1007 (`not bool(conflicting_targets(...))` over an empty conflict set). 'True means no proven overlapping targets' i…… | the direct prompt-side cause of the '同事件两目标不可区分' miss whenever the model has collapsed the alternatives |
| `cardinality` | predicates.py:308 (rendered to the Requirement Splitter and Requirement Reviewer): 'count: an integer; pseudo-states are not counted'. predicates.py:300 'this scope declares exactly this many non-pseudo states'. | predicate_api.py:1089-1090 counts every direct substate with `is_pseudo == False`, which includes converter-synthesised nodes (`UnspecifiedInitial`, `FinalWaittr_*`, `InvalidInitialtr_*`) -- these are ordinary states in the inspect table, not pseudostates. The…… | makes `cardinality` return True on models whose author-owned mode count is wrong (measured: cardinality(0043.PumpControl, 3) = True over Region1 + Region2 + a synthetic node) |
| `reaches` | prompts.py:62 (reviewer) 'What you can require is an adequate horizon: `within_cycles` on `occupancy_after` / `reaches`, `bound` on Family P.' and prompts.py:127 'A False produced by too small a horizon is a bounded artifact, not a defect, and publishing one i…… | `occupancy_after` has a horizon self-check that raises rather than returning a bounded False (predicate_api.py:1109-1134). `reaches` has none -- predicate_api.py:1273-1287 goes straight to `_reaches_within`, which returns a plain False. Verified: same binding,…… | both directions: fabricated reachability defects from a short horizon, and no refusal to alert the reviewer |
| `reaches` | predicates.py:417-422 caveat names exactly one boundary -- 'It ignores triggers, so it cannot stand in for occupancy_after.' prompts.py:362 repeats it: '`reaches` ignores triggers and cannot stand in for `occupancy_after`.' | Two further silent-False boundaries go unmentioned. (a) An undeclared but well-formed target returns False, not a refusal -- verified: `reaches(source="Root.Outer", target="Root.NoSuchState", within_cycles=3)` -> False. Its Family-S sibling `cardinality` refus…… | a `reaches` False can mean 'not reachable', 'you spelled it wrong', 'that is a pseudostate' or 'your horizon was short', and the prompt distinguishes none of them |
| `terminates` | predicates.py:446 field spec 'scope: the configuration to start from, or "[*]" for a cold start'; predicates.py:452 example `terminates(scope="[*]") # can the model finish at all from a cold start`; predicates.py:725-728 'That is true even when the claim is ab…… | The call is legal, but the *requirement* carrying it is hard-rejected upstream unless `behavior_phase == "initialization"`: capability.py:687-714 `initialization_anchored_findings` raises in nodes.py:1246-1250 ('requirements are anchored or named against what…… | removes the only expressible form of '整机不能终止' |
| `state_declared` | predicates.py:106 'kind: one of "leaf" (no substates), "composite" (has substates), "pseudo" (an initial/final marker), or "any" (declared at all)'. | predicate_api.py:750-758 accepts a wider alias set than the prompt lists -- 'leaf'\|'simple', 'composite'\|'submachine'\|'compound', 'pseudo'\|'pseudostate', 'any'\|'declared'\|''. Harmless in itself, but the schema Literal is built from the prompt's four valu…… | minor on its own; contributes to the pseudostate direction being invisible |
| `guard_distinguishable / FBMCQ` | prompts.py:351 (FBMCQ_CAPABILITY_BOUNDARY) 'Use `conflicting_targets(source=..., event=...)` for guard indistinguishability; it already ranges over every valuation and refuses to answer rather than guessing.' | `conflicting_targets` is not callable from an assertion. environment.py:19-23 states the opposite: 'There is no `simulate`, no `fbmcq`, no `states`, no `transitions`, no `transition_exists`, no `path`, no `topology`.' The only reachable name is the predicate `…… | no live effect found, but it is a stale contradiction sitting in the prompt module |

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
