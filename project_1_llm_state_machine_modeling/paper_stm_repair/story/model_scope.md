# R5.6 model scope：paper story / claim 边界冻结

> **定位**：本文件是 R5.6 的 paper story / model scope / claim boundary 入口。它把 R5.5 的 `llms-emp-stm-subset` 主 seed 池画像转成论文可写范围、资源角色和禁止外推边界。它不是 R7 主实验预注册，也不是 R5.7 repair target taxonomy；后续 R5.7 / R6 / R7 必须继承本文件的范围约束。
>
> **证据引用说明**：正文中的 `[src-*]`、`[clm-*]`、`[cmd-*]` 为文末稳定 ASCII 证据键，不按数字重排；新增证据只新增 key。

## 1. R5.6 结论摘要

| 问题 | R5.6 冻结结论 | 证据 |
|---|---|---|
| 主实验优先 seed 池 | `llms-emp-stm-subset` 是 R5.5/R5.6 阶段经设计决策优先深度画像的主 seed 池；这不是对所有候选池做 pairwise ranking 后得到的事实排名。 | [src-case]、[src-cluster]、[src-profile-report] |
| 主池规模 | 60 raw pairs = 10 个唯一 NL clusters × 6 个 LLM-generated `STM_0`。 | [clm-denominator] |
| 当前链路状态 | 16 converted / 44 partial / 0 blocked；60/60 canonical converted、parse ok、inspect ok。 | [clm-status] |
| 主线模型范围 | T0 离散 FSM / HSM / 离散 UML-SysML statechart 子集；`EFSM-lite` 作为 in-scope envelope / candidate mode 保留，但当前 `llms-emp` 主池没有被独立标为 `EFSM-lite` 的 cluster。 | [clm-main-scope] |
| caveat | T0.5 timer-like cue 只作为 caveat / annotation，不支撑 timed automata claim。 | [clm-t05-caveat] |
| supplementary stress | Digital Camera / T1-ish case 只作 supplementary stress / limitation / negative evidence。 | [clm-t1-stress] |
| 禁止外推 | 不外推到 timed automata、hybrid automata、arbitrary UML、protocol FSM、完整形式化验证或任意 UML 修复。 | [clm-forbidden-scope] |
| repair gain 边界 | conversion / normalization / `.fcstm` lowering / 可执行化收益不计 repair-loop gain。 | [clm-no-repair-gain] |

## 2. Scope contract：时间等级 × 结构家族

R5.6 的范围判定必须把**时间等级**和**结构家族**拆成正交维度。后续 R5.7 / R7 不得把某个维度的 caveat 自动升级为另一个维度的 main claim。

| 时间等级 / 结构家族 | FSM | HSM | EFSM-lite | 离散 UML-SysML statechart 子集 | protocol FSM | timed automata | hybrid automata | arbitrary UML |
|---|---|---|---|---|---|---|---|---|
| T0 离散 | main | main | main envelope；当前主池 0 个独立 `EFSM-lite` cluster | main，仅限 §3 子集 | excluded / related-work-only | excluded | excluded | excluded |
| T0.5 timer-like cue | caveat / annotation | caveat / annotation | caveat / annotation | caveat / annotation | excluded | excluded | excluded | excluded |
| T1+ / 真时间语义 | supplementary-stress 或 excluded | supplementary-stress 或 excluded | supplementary-stress 或 excluded | supplementary-stress 或 excluded | excluded | excluded | excluded | excluded |

### 2.1 判定解释

- **main**：可支撑论文主实验范围和 headline claim，但仍需 R7 eligibility 与 R8 repair result 支撑效果主张。
- **caveat / annotation**：可用于解释模型中存在 timer-like textual cue 或 abstraction loss；不能写成 timed automata 支持。
- **supplementary-stress**：可进入 appendix / stress / limitation / negative evidence；不能支撑主线 T0 headline claim。
- **excluded / related-work-only**：只能作为相关工作、排除说明或威胁，不进入主实验 claim。

### 2.2 Denominator 与证据入口

R5.6 对 `llms-emp-stm-subset` 使用四个报告口径，其中主结果分母与 caveat / stress / 全量资源分母必须区分，避免把 timer-like cue 或 stress case 混入 T0 headline：

| 口径 | cluster | pair | 用途 | 证据 |
|---|---:|---:|---|---|
| `T0 headline main` | 8 | 48 | R7/R8 主结果优先 denominator；当前覆盖离散 FSM/HSM/离散 statechart 子集，不包含独立 `EFSM-lite` cluster。 | [src-case]、[src-cluster]、[cmd-r56-counts] |
| `T0.5 caveat / annotation` | 1 | 6 | 可作为 timer-like cue caveat、annotation 或 loss 讨论；不得进入 timed automata claim。 | [src-case]、[src-cluster]、[cmd-r56-role-time] |
| `T1-ish supplementary stress` | 1 | 6 | Digital Camera / T1-ish 只作 stress、limitation 或 appendix。 | [src-case]、[src-cluster]、[cmd-r56-role-time] |
| `all llms-emp raw pairs` | 10 | 60 | seed 池总规模、转换 readiness、资源画像；不是 60 个独立需求。 | [clm-denominator] |

注意：机器字段 `r5_6_story_role=main_candidate` 当前包含 8 个 T0 cluster 和 1 个 T0.5 cluster。R5.6 的 paper headline 不能直接使用该字段作为主结果 denominator；必须再按 `time_level` 切分，得到 `T0 headline main = 8 clusters / 48 pairs`，并把 T0.5 单独降级为 caveat [clm-t05-caveat]。

### 2.3 矩阵逐类理由

| 判定类 | 适用单元格 | 为什么这样判定 | 证据 / 后续检查 |
|---|---|---|---|
| `main` | T0 × FSM/HSM/离散 statechart 子集；T0 × EFSM-lite 仅作 in-scope envelope / candidate mode | 当前主 seed 池中 8/10 cluster、48/60 pair 是 T0；这些制品可经 canonical / parse / inspect 链路进入后续 repair 前置表示。当前 `cluster_profiles.structure_family` 没有独立 `EFSM-lite` 取值，R7 若无新增证据应收窄 headline wording。 | [src-case]、[src-cluster]、[cmd-r56-counts]；R7 仍需 eligibility 复核。 |
| `caveat / annotation` | T0.5 × FSM/HSM/离散 statechart 子集；EFSM-lite-candidate 仍仅为 annotation / monitor | timer-like cue 只体现文本时间提示或 event abstraction，不具备 clocks / timed automata 语义。 | [cmd-r56-role-time]；R5.7 只能定义 monitor / annotation / loss，不得定义 timed repair target。 |
| `supplementary-stress 或 excluded` | T1+ × FSM/HSM/离散 statechart 子集；EFSM-lite-candidate 不改变 stress / excluded 角色 | Digital Camera / T1-ish cluster 可暴露范围压力，但不能支撑 T0 headline 或 timed semantics。 | [cmd-r56-role-time]；R7 若纳入只能列 supplementary/stress，不进主 denominator。 |
| `excluded / related-work-only` | protocol FSM / timed automata / hybrid automata / arbitrary UML 所有时间等级 | 当前数据、表示桥和评价门都未冻结这些模型族的语义、diagnostics 或 repair target。 | [clm-forbidden-scope]；若后续出现相关样例，只能作 related work、limitation 或 negative evidence。 |

## 3. `UML-SysML statechart` 的 in-scope 子集

本文件中的 `UML-SysML statechart` 不是任意 UML 行为图。R5.6 仅允许把以下**离散、单区域、可降低到 canonical STM / `.fcstm` 的子集**放入 main scope：

| 元素 | R5.6 角色 | R5.7 交接 |
|---|---|---|
| simple / composite state | main | 后续 repair 可检查缺失、冗余、层级错误。 |
| transition | main | 后续 repair 可检查目标、源、触发、guard/action 分解。 |
| event trigger | main | 后续 repair 可检查 event 覆盖与触发一致性。 |
| guard-like textual condition | main 范围内的候选语义元素，但 R5.6 不判缺陷 | R5.7 决定 trigger/guard/action taxonomy。 |
| action / effect textual label | main 范围内的候选语义元素，但 R5.6 不判缺陷 | R5.7 决定可修复 / 可抽象 / 仅记录。 |
| entry / exit / do activity textual record | caveat / candidate semantic element | R5.7 决定是否进入 repair target 或 loss ledger。 |
| choice / junction / initial / final pseudo-state | main，只限离散伪状态 | R5.7/R6 应保持 pseudo-state 与 stoppable state 的语义区分。 |

以下构造显式不属于 main scope：orthogonal region、并发 / fork / join、deep history、deferred event、submachine state、复杂 signal / change / time event 语义、连续时间约束、混成动态、跨 diagram 组合语义。若后续样例出现这些构造，只能进入 caveat / supplementary-stress / excluded，不得提升为 main claim [clm-statechart-subset]。

### 3.1 `EFSM-lite` 的工作定义与当前证据状态

R5.6 使用 `EFSM-lite` 只是为了描述当前 `llms-emp` 样例中出现的**离散变量、文本 guard / action 与有限状态控制流**，不是完整 data-rich EFSM 或协议状态机。进入 main scope 的 `EFSM-lite` 必须同时满足：

1. 控制骨架仍是有限状态 / 层次状态机，可降低到本项目 canonical STM / `.fcstm`。
2. guard / action 是离散、文本性、可追溯到 `NL` 或 raw `STM_0` 标签的候选语义元素。
3. 不要求求解复杂数据域、不引入连续变量、不引入真实时钟语义，也不声称覆盖完整 protocol FSM。

若某个样例的变量、数据结构或消息协议需要独立数据语义才能判定行为正确性，R5.6 只能把它标为 caveat / supplementary-stress / excluded；R5.7 可把相关现象列为 candidate target，但不得把它升级为 main repair claim。

当前证据状态需要特别区分：`EFSM-lite` 是 R5.6 为后续 taxonomy 预留的**范围上限 / 候选模式**，不是 `llms_emp_cluster_profiles.jsonl` 中已经出现的独立 `structure_family` 标签。当前 10 个 cluster 的结构族只有 6 HSM / 3 UML-SysML statechart / 1 FSM，独立 `EFSM-lite` cluster 数为 0 [src-cluster]、[cmd-r56-counts]。因此 R7 若不能补充或裁决出可审计的 EFSM-lite eligible 样例，paper headline 必须收窄为 FSM/HSM/离散 statechart 子集，不得把 EFSM-lite 写成已有数据覆盖的模型族。

## 4. 资源角色冻结

| 资源 / 样例族 | R5.6 角色 | 主体证据 | 可写内容 | 禁止写法 |
|---|---|---|---|---|
| `llms-emp-stm-subset` | main seed pool | 60 pair / 10 NL / 16 converted / 44 partial / 0 blocked | 主实验优先围绕其 T0 离散 FSM/HSM/statechart artifacts 设计；离散 guard/action/变量线索可作为 R5.7 `EFSM-lite` 候选，但当前没有独立 `EFSM-lite` cluster denominator。 | 不写成 60 个独立需求；不把 partial 当失败；不把 conversion readiness 当 repair result；不把 EFSM-lite 写成已有独立样本族。 |
| selected smoke examples | dry-run / sanity panel | 4 个静态 `<NL, STM_0, fcstm>` 样例 | 用于 R5.6/R5.7/R6 最小连通性和读者理解。 | 不作为最终实验上限或主结果替代。 |
| `sefm-llm-state-machine` | readable smoke / small example | 1 个 SSC7 generated Umple 输出 + 9 个 NL description | 可作可读补充案例或格式差异说明。 | 不按 9 个 generated pair 计算。 |
| `unified-uml-multimodal-validation` | synthetic stress / negative evidence | 989 个有效 generated PlantUML pair | 可作合成压力源，说明跨来源泛化风险。 | 不包装成真实控制系统需求主池。 |
| `ttool-ai-smd-subset` | conversion pressure / conditional supplementary | 6 个 TTool XML 条件 pair / 4 个唯一 NL | 可说明转换压力和 SMD 边界。 | 不在未切清 T0/SMD 与 leakage 前进入主实验。 |
| Digital Camera / T1-ish cluster | supplementary stress | 1/10 cluster、6/60 pair | 可作 T1-ish stress / limitation。 | 不支撑 T0 主 claim 或 timed automata claim。 |

## 5. Claim boundary

| Claim 类型 | 当前写法 | 当前强度 | 降级写法 | 禁止外推 |
|---|---|---|---|---|
| 任务定义 | “We study feedback-driven repair of initial state-machine artifacts conditioned on NL requirements.” | main evidence supports | 若 R7/R8 样本不足，改为 “pilot study of ...”。 | 不写 “first/strongest NL-to-STM generator”。 |
| 主 seed 池 | “We use an auditable seed pool of 10 NL clusters and 60 LLM-generated initial state machines.” | main evidence supports | 若 eligibility 缩小，按 eligible subset 报告。 | 不写成 60 独立需求。 |
| 模型范围 | “Our main scope is discrete T0 FSM/HSM/statechart artifacts, with EFSM-lite kept as a candidate in-scope envelope pending R7 eligibility.” | scope upper envelope / narrowing risk；FSM/HSM/statechart 有当前样例支撑，EFSM-lite pending / zero-current-example | 若 R7 排除 EFSM-lite / statechart 子集，按更窄范围降级。 | 不外推到 timed / hybrid / arbitrary UML / protocol FSM；不把 EFSM-lite 写成当前已有独立数据覆盖。 |
| Better STM | “Better STM is an evaluation target under pre-registered diagnostics, scenarios, regression and adjudication.” | current support = definition only | R8 前只能写 “will be evaluated”。 | 不写已证明 improvement。 |
| Repair loop 效果 | “The workflow is designed to support structured repair feedback.” | current support = design only | R8 前写设计，不写效果。 | 不写 repair loop 已提升质量。 |
| Conversion attribution | “We separate conversion readiness from repair gain.” | main evidence supports | 若 R8 台账不完整，只作 case analysis。 | 不把 normalization / lowering / parsing success 算 repair gain。 |

## 6. 对 R5.7 / R6 / R7 的约束

1. R5.7 可定义 repair target taxonomy，但不得重新打开本文件已排除的 timed / hybrid / arbitrary UML / protocol FSM 主 claim。
2. R5.7 必须把 `condition_like_label_lowered_as_event`、entry/action loss、hierarchy lowering 等 representation symptoms 标为候选，而不是直接当作已确认缺陷。
3. R6 repair loop 只能在 frozen `<NL, STM_0>` 上运行；不得把 pre-repair normalization 当作修复步骤。
4. R7 eligibility 必须区分 main pool、dry-run panel、supplementary stress、negative evidence。
5. R8 结果必须以 eligible repair runs 为主；失败、partial、回滚、不收敛不得静默删除。

## 7. 审计附录：证据链与事实源

### A.1 上游事实源清单

| 引用键 | source_id | 事实源 | 类型 | 用途 |
|---|---|---|---|---|
| [src-case] | `llms_emp_case_matrix` | [../pipeline/readiness_audit/llms_emp_profile/llms_emp_case_matrix.jsonl](../pipeline/readiness_audit/llms_emp_profile/llms_emp_case_matrix.jsonl) | JSONL | pair status、time level、story role、loss code、parse/inspect status。 |
| [src-cluster] | `llms_emp_cluster_profiles` | [../pipeline/readiness_audit/llms_emp_profile/llms_emp_cluster_profiles.jsonl](../pipeline/readiness_audit/llms_emp_profile/llms_emp_cluster_profiles.jsonl) | JSONL | cluster time level、structure family、story role、10 NL 口径。 |
| [src-partial] | `llms_emp_partial_ledger` | [../pipeline/readiness_audit/llms_emp_profile/llms_emp_partial_attribution_ledger.jsonl](../pipeline/readiness_audit/llms_emp_profile/llms_emp_partial_attribution_ledger.jsonl) | JSONL | partial attribution、R5.7 candidate-only 标记。 |
| [src-profile-report] | `llms_emp_main_seed_profile` | [../reports/2026-06-29-00-03-56-llms-emp-main-seed-profile.md](../reports/2026-06-29-00-03-56-llms-emp-main-seed-profile.md) | Markdown report | 人类可读 10 cluster / 60 pair 画像。 |
| [src-r552-report] | `r5_5_2_recovery` | [../reports/2026-06-29-19-55-45-r5-5-2-plantuml-blocked-recovery.md](../reports/2026-06-29-19-55-45-r5-5-2-plantuml-blocked-recovery.md) | Markdown report | blocked recovery 当前性和 16/44/0 状态。 |
| [src-scope-handoff] | `r5_5_scope_handoff` | [../experiment_design/scope/2026-06-29-17-33-35-r5-5-scope-handoff.md](../experiment_design/scope/2026-06-29-17-33-35-r5-5-scope-handoff.md) | Markdown + audit appendix | R5.5 -> R5.6 scope 交接。 |
| [src-status] | `paper_stm_repair_status` | [../STATUS.md](../STATUS.md) | Markdown summary | 当前状态总账和不可写结论。 |

### A.2 Claim-evidence map

| 引用键 | claim_id | 结论 / claim | 类型 | 上游事实源 | 复验命令 | 置信度 | caveat |
|---|---|---|---|---|---|---|---|
| [clm-denominator] | `R5.6-SCOPE-C1` | `llms-emp` denominator 是 60 raw pairs = 10 unique NL clusters × 6 LLM outputs。 | count | [src-case]、[src-cluster] | [cmd-r56-counts] | high | 不可写成 60 独立需求。 |
| [clm-status] | `R5.6-SCOPE-C2` | 当前状态为 16 converted / 44 partial / 0 blocked；60/60 canonical converted、parse ok、inspect ok。 | count | [src-case]、[src-r552-report] | [cmd-r56-counts] | high | 只能说明 pre-repair readiness。 |
| [clm-main-scope] | `R5.6-SCOPE-C3` | 主线模型范围上限是 T0 离散 FSM/HSM/离散 statechart 子集，并把 EFSM-lite 作为候选 in-scope envelope 保留。 | decision | [src-cluster]、[src-scope-handoff] | [cmd-r56-counts] | medium | 当前主池 0 个独立 EFSM-lite cluster；R7 eligibility 可进一步收窄到 FSM/HSM/离散 statechart。 |
| [clm-t05-caveat] | `R5.6-SCOPE-C4` | T0.5 只作为 timer-like caveat / annotation。 | classification | [src-case]、[src-cluster] | [cmd-r56-counts] | high | 不支撑 timed automata。 |
| [clm-t1-stress] | `R5.6-SCOPE-C5` | Digital Camera / T1-ish cluster 只作 supplementary stress。 | classification | [src-case]、[src-cluster] | [cmd-r56-counts] | high | 不支撑 T0 main claim。 |
| [clm-forbidden-scope] | `R5.6-SCOPE-C6` | timed / hybrid / arbitrary UML / protocol FSM 均不进入 headline claim。 | prohibition | [src-scope-handoff]、本文件 §2–§3 | 人工复验 | high | related work 可讨论，但不作结果外推。 |
| [clm-statechart-subset] | `R5.6-SCOPE-C7` | UML-SysML statechart 仅指离散可降低子集，不等于 arbitrary UML。 | definition | 本文件 §3、R5.6 PR body review 修复 | 人工复验 | medium | R7/R8 若遇到新构造需降级。 |
| [clm-no-repair-gain] | `R5.6-SCOPE-C8` | conversion / normalization / lowering 不计 repair gain。 | prohibition | [src-case]、[src-partial]、[src-status] | [cmd-r56-attribution] | high | R8 需三阶段归因。 |

### A.3 复验命令

```bash
# [cmd-r56-counts]
python - <<'PY'
import json, pathlib, collections
base=pathlib.Path('project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/readiness_audit/llms_emp_profile')
case=[json.loads(l) for l in (base/'llms_emp_case_matrix.jsonl').read_text().splitlines() if l.strip()]
clusters=[json.loads(l) for l in (base/'llms_emp_cluster_profiles.jsonl').read_text().splitlines() if l.strip()]
print('pairs', len(case), 'clusters', len(clusters))
print('status', collections.Counter(r['conversion_status'] for r in case))
print('canonical', collections.Counter(r['canonical_status'] for r in case))
print('parse', collections.Counter(r['parse_status'] for r in case))
print('inspect', collections.Counter(r['inspect_status'] for r in case))
print('pair time', collections.Counter(r['time_level'] for r in case))
print('cluster time', collections.Counter(r['time_level'] for r in clusters))
print('cluster family', collections.Counter(r['structure_family'] for r in clusters))
print('cluster role', collections.Counter(r['r5_6_story_role'] for r in clusters))
PY
```

```bash
# [cmd-r56-role-time]
python - <<'PY'
import json, pathlib, collections
base=pathlib.Path('project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/readiness_audit/llms_emp_profile')
case=[json.loads(l) for l in (base/'llms_emp_case_matrix.jsonl').read_text().splitlines() if l.strip()]
clusters=[json.loads(l) for l in (base/'llms_emp_cluster_profiles.jsonl').read_text().splitlines() if l.strip()]
print('case role x time', collections.Counter((r['r5_6_story_role'], r['time_level']) for r in case))
print('cluster role x time', collections.Counter((r['r5_6_story_role'], r['time_level']) for r in clusters))
PY
```

```bash
# [cmd-r56-attribution]
python - <<'PY'
import json, pathlib, collections
base=pathlib.Path('project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/readiness_audit/llms_emp_profile')
case=[json.loads(l) for l in (base/'llms_emp_case_matrix.jsonl').read_text().splitlines() if l.strip()]
partial=[json.loads(l) for l in (base/'llms_emp_partial_attribution_ledger.jsonl').read_text().splitlines() if l.strip()]
print('repair_contribution_allowed', collections.Counter(r['repair_contribution_allowed'] for r in case))
print('partial attribution', collections.Counter(r['primary_attribution'] for r in partial))
print('r5_7_candidate_only', collections.Counter(r['r5_7_candidate_only'] for r in partial))
PY
```
