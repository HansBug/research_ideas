# R5 `llms-emp-stm-subset` directional analysis

## 事实源与复验 / 来源考据

| source path | source creation commit | prefix commit | substantive fact commit 判定理由 | non-prefix revision/migration commit | canonical machine source |
|---|---|---|---|---|---|
| `pipeline/readiness_audit/llms_emp_profile/llms_emp_main_seed_analysis.md` | `bbd974c17da1c113eca847c1ae7ba2969c7f0644` (2026-06-28 19:42:58 +0800) | `bbd974c17da1c113eca847c1ae7ba2969c7f0644` (2026-06-28 19:42:58 +0800, directional analysis / handoff fact freeze) | `bbd974c17da1c113eca847c1ae7ba2969c7f0644`：首次固化 `llms-emp-stm-subset` 作为后续主实验优先 seed 池，并给出 60 case、LLM 维度、问题谱系与 R6/R7 纪律。 | `1ab6af18eda24cf35a10eb9e99e1f59ca9b6b616` (2026-06-29 02:41:50 +0800, R5.5.1 reports/readiness 路径迁移)；后续修正只补 CI 路径、full SHA 与人类入口链接，不改 canonical machine facts。 | [sweep_report.json](../pipeline/readiness_audit/seed_sweep/sweep_report.json)；[records_index.json](../pipeline/readiness_audit/seed_sweep/records_index.json)；[llms-emp archive](../pipeline/readiness_audit/artifact_archives/archives/llms-emp-stm-subset_records.zip)；[pairs.jsonl](../corpora/seed_library/llms-emp-stm-subset/assets/extracted/pairs.jsonl) |
| `pipeline/readiness_audit/handoff/llms_emp_main_seed_handoff.md` | `bbd974c17da1c113eca847c1ae7ba2969c7f0644` (2026-06-28 19:42:58 +0800) | `bbd974c17da1c113eca847c1ae7ba2969c7f0644` (2026-06-28 19:42:58 +0800, directional analysis / handoff fact freeze) | `bbd974c17da1c113eca847c1ae7ba2969c7f0644`：与方向性分析同一事实批次生成，提供 R6/R7 分层选样与禁止主张清单。 | `1ab6af18eda24cf35a10eb9e99e1f59ca9b6b616` (2026-06-29 02:41:50 +0800, R5.5.1 reports/readiness 路径迁移)；后续修正只补 CI 路径、full SHA 与人类入口链接，不改 canonical machine facts。 | [r5_to_r6_repair_inputs.json](../pipeline/readiness_audit/handoff/r5_to_r6_repair_inputs.json)；[r5_to_r7_seed_eligibility.json](../pipeline/readiness_audit/handoff/r5_to_r7_seed_eligibility.json)；[sweep_report.json](../pipeline/readiness_audit/seed_sweep/sweep_report.json) |

> 本节是本 report 的事实绑定入口：Markdown 只做人类阅读与论文写作 handoff，不替代 canonical JSON/JSONL/ZIP/committed run artifacts。复验时优先回到最后一列机器事实源。

## 迁移说明

本 report 是 R5 后 `llms-emp-stm-subset` 主实验方向性判断的 canonical human-facing 入口，合并旧 `llms_emp_main_seed_analysis.md` 与 R5->R6/R7 handoff 摘要，避免在 pipeline 目录下保留第二事实源。

## A. R5 后主实验 seed 方向性分析

## llms-emp-stm-subset 主实验 seed 分析

本文件是 R5 全量摸排后形成的长期研究归纳，用于回答：后续 paper1 主实验为什么优先围绕 `llms-emp-stm-subset` 展开，以及这 60 条一手 `NL + LLM-generated STM_0` 在转换到 `.fcstm` 前后的状态如何。

> 事实源仍是 [sweep_report.json](../pipeline/readiness_audit/seed_sweep/sweep_report.json)、[records_index.json](../pipeline/readiness_audit/seed_sweep/records_index.json)、[archives/llms-emp-stm-subset_records.zip](../pipeline/readiness_audit/artifact_archives/archives/llms-emp-stm-subset_records.zip) 与 [../../../corpora/seed_library/llms-emp-stm-subset/assets/extracted/pairs.jsonl](../corpora/seed_library/llms-emp-stm-subset/assets/extracted/pairs.jsonl)。本 Markdown 是人类阅读入口，不是第二事实真源。

### 1. 方向性结论

`llms-emp-stm-subset` 应作为后续 R6/R7 的主实验优先 seed 池。核心原因是它同时满足：一手公开来源、`<NL, LLM-generated STM_0>` 关系明确、规模适中、字段可审计、同一 NL 下多 LLM 输出可比较、且领域贴近 SysML/UML state machine 行为建模。

| seed 源 | R5 结论 | 后续角色 |
|---|---|---|
| `llms-emp-stm-subset` | 60 个一手 `NL + LLM-generated PlantUML`；10 个唯一 NL × 6 个 LLM 输出 | 主实验核心 seed 池 |
| `unified-uml-multimodal-validation` | 数量大但 synthetic / 通用 feature-description 色彩更强 | stress / robustness / appendix |
| `sefm-llm-state-machine` | 只有 1 个可计 generated STM pair | qualitative / readable smoke case |
| `ttool-ai-smd-subset` | whole AVATAR project XML，尚未冻结纯 T0/SMD 切片 | converter pressure / follow-up |

### 2. 数据规模与统计依赖

| 指标 | 数量 | 说明 |
|---|---:|---|
| raw pair 行数 | 60 | workbook `STM Results` sheet 全量 `Requirement Description + Generation PlantUML` |
| 唯一 NL 需求 | 10 | 每个 NL 对应 6 个 LLM 输出 |
| LLM 输出数 | 60 | GPT-4o、GPT-4、Llama、Kimi、DeepSeek、Claude 各 10 条 |
| unique generated PlantUML | 59 | HSTBS 中 GPT-4 与 Kimi 输出完全相同，因此 unique 少 1 |
| reference PlantUML | 10 | 只能作 reference / leakage 风险说明，不得作为原始 `STM_0` |

这 60 条不能当作 60 个完全独立需求样本。后续论文统计必须以 10 个唯一 NL 为 cluster，并在 LLM-output-level 指标之外报告 clustered interpretation。

### 3. 60 case 全量状态表

符号：🟢 = `converted`；🟡 = `partial`；🔴 = `blocked`。

| # | NL case / 来源 | GPT-4o | GPT-4 | Llama | Kimi | DeepSeek | Claude | 小结 |
|---:|---|---|---|---|---|---|---|---|
| 0 | high-level driving module / HLDCS | 🟡 `0000` | 🟡 `0010` | 🟡 `0020` | 🟡 `0030` | 🟡 `0040` | 🟡 `0050` | 6 partial |
| 1 | State machine diagram of the base brake subsystem / HSTBS | 🟢 `0001` | 🟢 `0011` | 🟡 `0021` | 🟢 `0031` | 🟡 `0041` | 🟢 `0051` | 4 converted, 2 partial |
| 2 | Pump Control state machine / Real-Time Software Design for Embedded Systems | 🟢 `0002` | 🟢 `0013` | 🟡 `0023` | 🟡 `0033` | 🟡 `0043` | 🟢 `0053` | 3 converted, 3 partial |
| 3 | Hybrid Sport Utility Vehicle, HSUV / HSUV | 🟢 `0003` | 🟢 `0012` | 🟡 `0022` | 🟡 `0032` | 🟡 `0042` | 🟢 `0052` | 3 converted, 3 partial |
| 4 | state machine for Train Control / Real-Time Software Design for Embedded Systems | 🟡 `0004` | 🟡 `0014` | 🟡 `0024` | 🟡 `0034` | 🟡 `0044` | 🟢 `0054` | 5 partial, 1 converted |
| 5 | Microwave Oven Control with entry and   exit actions / MOCV | 🟡 `0005` | 🟡 `0015` | 🟡 `0025` | 🟡 `0035` | 🟡 `0045` | 🟢 `0055` | 5 partial, 1 converted |
| 6 | UAV swarm state machine diagram / DSCS | 🟢 `0006` | 🟡 `0016` | 🟡 `0026` | 🟢 `0036` | 🟡 `0046` | 🟢 `0056` | 3 converted, 3 partial |
| 7 | Collision avoidance sub-machine state diagram / HLDCS | 🟢 `0007` | 🟡 `0017` | 🟡 `0027` | 🔴 `0037` | 🟡 `0047` | 🟡 `0057` | 1 converted, 4 partial, 1 blocked |
| 8 |  Digital camera state machine diagrams / DCS | 🟡 `0008` | 🔴 `0018` | 🔴 `0028` | 🟡 `0038` | 🟡 `0048` | 🟡 `0058` | 4 partial, 2 blocked |
| 9 | autonomous mode / HLDCS | 🟡 `0009` | 🟡 `0019` | 🟡 `0029` | 🟡 `0039` | 🟡 `0049` | 🟡 `0059` | 6 partial |

### 4. 转换状态汇总

| 状态 | 数量 | 解释 |
|---|---:|---|
| `converted` | 16 | official SCXML raw 可用，`.fcstm` parse / inspect OK，且无 R5/R4.5 loss |
| `partial` | 41 | 可进入 canonical / fcstm 或部分转换，但存在 normalization / representation loss / caveat |
| `blocked` | 3 | 当前 official SCXML unavailable，无 canonical / fcstm |

| 输出存在性 | 数量 |
|---|---:|
| raw PlantUML archive member | 60 / 60 |
| normalized PlantUML archive member | 27 / 60 |
| official SCXML intermediate | 57 / 60 |
| record 内有 canonical status + structured export hash | 57 / 60 |
| record 内有 fcstm hash | 57 / 60 |
| 仓库持久化 canonical JSON | 3 / 60，仅 selected examples |
| 仓库持久化 `.fcstm` 文件 | 3 / 60，仅 selected examples |

这里的关键解释是：不是只有 3 条能转 `.fcstm`；R5 sweep 中 57 条已经能走到 `.fcstm` 级别并保留 hash / archive 证据，但当前只把 selected examples 的 3 条作为单文件持久化。

### 5. LLM 维度状态

| LLM | converted | partial | blocked | 高频 caveat |
|---|---:|---:|---:|---|
| GPT-4o | 5 | 5 | 0 | `ancestor_target_reentry`×3, `condition_label_as_event`×3, `source_scope_lift`×3 |
| GPT-4 | 3 | 6 | 1 | `source_scope_lift`×4, `initial_lowering`×3, `condition_label_as_event`×2 |
| Llama | 0 | 9 | 1 | `r3_1_normalization_replay`×9, `condition_label_as_event`×2, `source_scope_lift`×2 |
| Kimi | 2 | 7 | 1 | `r3_1_normalization_replay`×4, `condition_label_as_event`×3, `initial_lowering`×3 |
| DeepSeek | 0 | 10 | 0 | `r3_1_normalization_replay`×9, `condition_label_as_event`×3, `initial_lowering`×2 |
| Claude | 6 | 4 | 0 | `condition_label_as_event`×3, `initial_lowering`×2, `r3_1_normalization_replay`×1 |

### 6. 问题谱系与归因

| 问题类别 | 数量 | 初步归因 | 后续处理 |
|---|---:|---|---|
| `R5.LOSS.r3_1_normalization_replay_not_repair` | 24 | conversion readiness；R3.1 normalization replay | 不得计入 repair gain；R7 分层报告 |
| `R45.LOSS.condition_like_label_lowered_as_event` | 16 | seed / PlantUML / representation 共同问题；guard-event 边界不清 | 可作为 guard/event repair target 候选，但必须逐例由 NL 支撑 |
| `R45.LOSS.source_lifted_to_composite_boundary` | 12 | HSM lowering / representation loss | 通常不计 repair target，除非 NL 明确要求层次入口/出口语义 |
| `R45.LOSS.initial_inferred_from_source_order_or_start_state` | 12 | HSM initial lowering caveat | 保留 caveat；不作为 repair gain |
| `R45.LOSS.target_lifted_to_composite_boundary` | 8 | HSM lowering / representation loss | 保留 caveat；不作为 repair gain |
| `R45.LOSS.composite_target_lowered_to_initial_child` | 6 | ancestor re-entry lowering | 保留 caveat；不作为 repair gain |
| `R45.LOSS.cross_scope_transition_unrepresentable` | 5 | cross-scope transition 表示限制 | 进入 C-analysis 或 converter follow-up |
| `R5.LOSS.official_scxml_unavailable` | 3 | conversion blocker / negative evidence | 进入 D-excluded / R8 negative evidence |

学术上最重要的发现是：LLM 生成的 PlantUML `STM_0` 往往不是完全不可用，而是结构看起来像状态机，但 guard / action / event / 层次入口出口等行为语义较薄或不稳定。这支持后续 feedback-driven repair 的研究动机。

### 7. R6 / R7 handoff 建议

R6 不建议直接混入 Unified / TTool，也不建议一开始覆盖全部 60 条。建议先围绕 `llms-emp-stm-subset` 选 12–18 条分层样本跑真实 repair loop：

1. A-main：从 16 个 clean converted 中选 4–6 条，验证 loop 基线能力。
2. B-main-with-caveat：从 `condition_like_label_lowered_as_event` 等 partial 中选 4–6 条，验证 guard/event/semantic underspecification 修正。
3. C-analysis-only：选择 hierarchy / cross-scope loss 较重样本做定性分析，不轻易计入 repair gain。
4. D-negative：3 个 blocked 进入 R8 negative evidence / converter follow-up。

R7 必须冻结以下纪律：

- 按 10 个唯一 NL 做 clustered reporting。
- repair gain 只能从 pre-repair `.fcstm` 到 repaired `.fcstm` 计算。
- reference `PlantUML` 与 checking 后结果不得进入 repair 输入。
- conversion / normalization / representation lowering 只能作 attribution，不能写成修正循环改进。

### 8. 不能据此声称的结论

1. 不能声称 R5 已经执行真实 repair loop。
2. 不能声称已经生成 `STM_k` 或 Better STM 主结果。
3. 不能把 57 条可导出 `.fcstm` 写成 repair 成功。
4. 不能把 60 条当成 60 个独立需求样本。
5. 不能把 conversion / normalization / lowering 的收益计入 repair gain。

## B. R5 -> R6/R7 主实验 seed 交接建议

## R5 -> R6/R7：`llms-emp-stm-subset` 主实验 seed 交接

本文件把 R5 全量摸排后的方向性结论固定为后续阶段可执行的交接建议。完整 60 case 表和问题谱系已收敛到本 report 与 main seed profile；机器事实源仍是 [sweep_report.json](../pipeline/readiness_audit/seed_sweep/sweep_report.json) 与 [llms-emp-stm-subset_records.zip](../pipeline/readiness_audit/artifact_archives/archives/llms-emp-stm-subset_records.zip)。

### 1. 交接结论

`llms-emp-stm-subset` 是 R6/R7 的优先主池。它提供 60 个一手 `NL + LLM-generated PlantUML` pair，实际结构是 10 个唯一 NL × 6 个 LLM 输出。R5 中这 60 条的状态为：16 `converted`、41 `partial`、3 `blocked`。

### 2. 推荐 R6 首轮样本策略

R6 首轮目标是跑通真实 repair loop 和证据链，不是一次性覆盖全部 seed。建议选 12–18 条：

| 分层 | 建议数量 | 进入条件 | 用途 |
|---|---:|---|---|
| A-main | 4–6 | `converted`，loss_count=0，parse / inspect OK | 低转换噪声下验证 repair loop 基线 |
| B-main-with-caveat | 4–6 | `partial`，主要 caveat 是 condition/event/action 语义薄弱，且可由 NL 支撑修正目标 | 验证 feedback-driven repair 的核心价值 |
| C-analysis-only | 3–4 | hierarchy / cross-scope / normalization loss 较重 | 定性分析与 attribution；不轻易计入 repair gain |
| D-negative | 3 | `blocked_official_scxml_unavailable` | R8 negative evidence / converter follow-up |

首轮选样应覆盖至少 5 个唯一 NL、至少 4 个 LLM；同一 NL cluster 中不宜一次性选满 6 个输出，避免 clustered bias。

### 3. R7 必须冻结的规则

1. 以 10 个唯一 NL 为 cluster 做统计解释，60 个 pair 只作为 LLM-output-level 样本。
2. repair gain 只能从 pre-repair `.fcstm` 到 repaired `.fcstm` 计算。
3. reference `PlantUML` 与 checking 后结果不得作为 repair 输入。
4. `r3_1_normalization_replay`、HSM lowering、scope lifting、initial lowering 只能作 attribution，不能写成 repair improvement。
5. `condition_like_label_lowered_as_event` 只有在 NL 明确支持时才进入 guard/event repair target；否则只能作为表示 caveat。

### 4. 后置资源角色

| seed 源 | 后置角色 |
|---|---|
| `unified-uml-multimodal-validation` | stress / robustness / appendix，不作为主源 |
| `sefm-llm-state-machine` | qualitative / readable smoke case |
| `ttool-ai-smd-subset` | converter pressure / T0/SMD slicing follow-up |

### 5. 禁止主张

1. 不能声称 R5 已经执行真实 repair loop。
2. 不能声称 R5 已经生成 `STM_k`。
3. 不能把 57 条可导出 `.fcstm` 写成 repair 成功。
4. 不能把 60 条当成 60 个独立需求。
5. 不能把 conversion / normalization / lowering 的收益计入 repair gain。
