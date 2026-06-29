# R5.5.2 PlantUML blocked 样例恢复更新

> 证据引用说明：正文中的方括号引用（如 `src-*`、`clm-*`、`cmd-*`）均指向文末审计附录。这些键是稳定 ASCII key，不按数字顺序重排。

## 1. 定位

本 report 记录 PR-R5.5.2 对 `llms-emp-stm-subset` 三个 PlantUML blocked 样例的转换前恢复结果。它**只覆盖 R5.5.2 的增量事实**：在不改 raw `pairs.jsonl` / 一手资源、不新增 parallel pipeline、不把 conversion recovery 计入 repair gain 的前提下，现有 PlantUML pre-SCXML normalization / recovery 环节让三个原 blocked 样例可经 official PlantUML SCXML 路径进入 `.fcstm` readiness 画像 [clm-r552-boundary][clm-r552-no-repair-gain]。

本 report supersede 旧 R5.5 main seed profile / negative evidence report 中关于 `llms-emp` blocked 数量与三个 blocked row 的当前性；旧 report 仍可用于理解 R5.5.1 前的历史画像、特征矩阵和方向性讨论，但当前状态数字必须以本 report 与当前 machine artifacts 为准 [clm-r552-status][src-r552-case]。

## 2. 核心结论

1. `llms-emp-stm-subset` 当前仍是 `60 = 10` 个唯一 NL cluster × `6` 个 LLM 输出；R5.5.2 后 pair 状态为 `converted=16 / partial=44 / blocked=0`，且 60 条 `canonical_status` 均为 `converted`、`parse_status=ok`、`inspect_status=ok` [clm-r552-status][cmd-r552-status]。
2. 三个原 blocked 样例 `0018`、`0028`、`0037` 均已变为 `partial`，但都带有 `R5.LOSS.r3_1_normalization_replay_not_repair`，因此只能说明 conversion readiness 恢复，不能写成 repair loop 修复收益 [clm-r552-targets][clm-r552-no-repair-gain]。
3. 与 R5.5 base matrix 相比，`llms-emp` 60 条中只有这三个目标样例发生状态变化：`blocked -> partial`；其余 57 条没有从 `converted/partial` 退化，关键 source trace 字段保持一致 [clm-r552-no-regression][cmd-r552-no-regression]。注意：一次完整重跑会刷新部分已是 `partial` 的派生 `.fcstm` / loss attribution，已观测到 `llms_emp_stm_results_0024` 的 `fcstm_sha256` 与 `r5_loss_codes` 发生非状态漂移；这不是新增 recovery target，也不改变其 `partial`/source trace 结论 [clm-r552-derived-drift]。
4. 全 seed sweep 的 pair 状态同步从 `converted=529 / partial=504 / blocked=23 / not_applicable=20 / needs_generation=2` 变为 `converted=529 / partial=508 / blocked=19 / not_applicable=20 / needs_generation=2`。除三个 `llms-emp` 目标外，`unified_uml_state_train_0265` 也因同一低风险 normalization 规则被 collateral 恢复为 partial；该 synthetic collateral 只能作为 conversion audit fact，不改变 paper 主 seed 定位 [clm-r552-global][cmd-r552-no-regression]。
5. 学术 story 的主边界不因此扩张：T0 离散 FSM/HSM/UML-SysML statechart artifacts 仍是主线；Digital Camera / T1 cluster 仍只能作为 supplementary stress，guard/action/time 的语义抽象问题仍留给 R5.7 / R6 之后逐例裁决 [clm-r552-scope]。

## 3. `llms-emp` 10×6 当前全体画像

本节把最新 `llms-emp-stm-subset` 状态直接展开为 10 个唯一 NL cluster × 6 个 LLM 输出。注意这里的分母是 **10 条唯一 NL** 与 **60 条 LLM-generated STM_0 输出**，不是 60 条互不相关的需求；所有行都来自一手 `Experiment Results.xlsx` 的 `Requirement Description + Generation PlantUML`，且通过 `sheet/row/column + workbook sha256` 回溯 [clm-r552-denominator][src-r552-pairs]。

状态口径：🟢 = `converted`（`.fcstm` parse/inspect ok 且无当前 loss/caveat）；🟡 = `partial`（可进入后续资格审查，但带 normalization / lowering / semantic caveat）；🔴 = `blocked`。R5.5.2 后当前没有 🔴 blocked [clm-r552-10x6][src-r552-case]。

### 3.1 十个 NL cluster 的完整结论表

| # | NL / seed | 来源系统 / seed 来源 | 控制语义 | 时间等级 | 结构族 | 行为特征 | 6 个 LLM 输出状态 | story 角色 | 主要风险 / 当前结论 |
|---:|---|---|---|---|---|---|---|---|---|
| 0 | `llms_emp_nl_00_hldcs_high_level_driving_module`<br>high-level driving module | HLDCS | 自动驾驶模式控制 | `T0` | `HSM` | 守卫式条件、动作/entry-exit、变量/数据条件、层级、伪状态 | 🟡6 | `main_candidate` | 条件标签仍作事件；需 R3.1 规范化回放；层级 lowering caveat |
| 1 | `llms_emp_nl_01_hstbs_state_machine_diagram_of_the_base`<br>State machine diagram of the base brake subsystem | HSTBS | 制动子系统控制 | `T0` | `FSM` | 守卫式条件、动作/entry-exit、伪状态 | 🟢4 / 🟡2 | `main_candidate` | 需 R3.1 规范化回放 |
| 2 | `llms_emp_nl_02_real_time_softwa_pump_control_state_machine`<br>Pump Control state machine | Real-Time Software Design for Embedded Systems | 泵子系统模式控制 | `T0` | `HSM` | 守卫式条件、层级 | 🟢3 / 🟡3 | `main_candidate` | 需 R3.1 规范化回放；层级 lowering caveat |
| 3 | `llms_emp_nl_03_hsuv_hybrid_sport_utility_vehicle_hsuv`<br>Hybrid Sport Utility Vehicle, HSUV | HSUV | 车辆运行模式控制 | `T0` | `HSM` | 守卫式条件、动作/entry-exit、层级 | 🟢3 / 🟡3 | `main_candidate` | 需 R3.1 规范化回放 |
| 4 | `llms_emp_nl_04_real_time_softwa_state_machine_for_train_control`<br>state machine for Train Control | Real-Time Software Design for Embedded Systems | 列车运动控制 | `T0` | `HSM` | 守卫式条件、动作/entry-exit、层级 | 🟢1 / 🟡5 | `main_candidate` | 需 R3.1 规范化回放；层级 lowering caveat |
| 5 | `llms_emp_nl_05_mocv_microwave_oven_control_with_entry`<br>Microwave Oven Control with entry and exit actions | MOCV | 微波炉控制：timer-like caveat | `T0.5` | `UML-SysML statechart` | 守卫式条件、动作/entry-exit、变量/数据条件、显式时间 | 🟢1 / 🟡5 | `main_candidate` | 需 R3.1 规范化回放；层级 lowering caveat |
| 6 | `llms_emp_nl_06_dscs_uav_swarm_state_machine_diagram`<br>UAV swarm state machine diagram | DSCS | 无人机群任务控制 | `T0` | `HSM` | 守卫式条件、动作/entry-exit、层级 | 🟢3 / 🟡3 | `main_candidate` | 需 R3.1 规范化回放；层级 lowering caveat |
| 7 | `llms_emp_nl_07_hldcs_collision_avoidance_sub_machine_st`<br>Collision avoidance sub-machine state diagram | HLDCS | 碰撞规避模式控制 | `T0` | `UML-SysML statechart` | 守卫式条件、层级、并发/区域 | 🟢1 / 🟡5 | `main_candidate` | 需 R3.1 规范化回放；跨层级迁移表示损失；层级 lowering caveat |
| 8 | `llms_emp_nl_08_dcs_digital_camera_state_machine_diagr`<br>Digital camera state machine diagrams | DCS | 相机控制：显式执行时间与伪状态压力样例 | `T1` | `UML-SysML statechart` | 守卫式条件、动作/entry-exit、变量/数据条件、层级、伪状态、并发/区域、显式时间 | 🟡6 | `supplementary_stress` | 条件标签仍作事件；需 R3.1 规范化回放；跨层级迁移表示损失；层级 lowering caveat |
| 9 | `llms_emp_nl_09_hldcs_autonomous_mode`<br>autonomous mode | HLDCS | 自动驾驶模式控制 | `T0` | `HSM` | 守卫式条件、动作/entry-exit、变量/数据条件、层级、伪状态 | 🟡6 | `main_candidate` | 条件标签仍作事件；需 R3.1 规范化回放；跨层级迁移表示损失；层级 lowering caveat |

### 3.2 10×6 LLM 输出矩阵

| NL cluster | 时间 / 结构 | GPT-4o | GPT-4 | Llama | Kimi | DeepSeek | Claude |
|---|---|---|---|---|---|---|---|
| `00` high-level driving module | `T0` / `HSM` | 🟡 `0000` | 🟡 `0010` | 🟡 `0020` | 🟡 `0030` | 🟡 `0040` | 🟡 `0050` |
| `01` State machine diagram of the base brake subsystem | `T0` / `FSM` | 🟢 `0001` | 🟢 `0011` | 🟡 `0021` | 🟢 `0031` | 🟡 `0041` | 🟢 `0051` |
| `02` Pump Control state machine | `T0` / `HSM` | 🟢 `0002` | 🟢 `0013` | 🟡 `0023` | 🟡 `0033` | 🟡 `0043` | 🟢 `0053` |
| `03` Hybrid Sport Utility Vehicle, HSUV | `T0` / `HSM` | 🟢 `0003` | 🟢 `0012` | 🟡 `0022` | 🟡 `0032` | 🟡 `0042` | 🟢 `0052` |
| `04` state machine for Train Control | `T0` / `HSM` | 🟡 `0004` | 🟡 `0014` | 🟡 `0024` | 🟡 `0034` | 🟡 `0044` | 🟢 `0054` |
| `05` Microwave Oven Control with entry and exit actions | `T0.5` / `UML-SysML statechart` | 🟡 `0005` | 🟡 `0015` | 🟡 `0025` | 🟡 `0035` | 🟡 `0045` | 🟢 `0055` |
| `06` UAV swarm state machine diagram | `T0` / `HSM` | 🟢 `0006` | 🟡 `0016` | 🟡 `0026` | 🟢 `0036` | 🟡 `0046` | 🟢 `0056` |
| `07` Collision avoidance sub-machine state diagram | `T0` / `UML-SysML statechart` | 🟢 `0007` | 🟡 `0017` | 🟡 `0027` | 🟡 `0037` | 🟡 `0047` | 🟡 `0057` |
| `08` Digital camera state machine diagrams | `T1` / `UML-SysML statechart` | 🟡 `0008` | 🟡 `0018` | 🟡 `0028` | 🟡 `0038` | 🟡 `0048` | 🟡 `0058` |
| `09` autonomous mode | `T0` / `HSM` | 🟡 `0009` | 🟡 `0019` | 🟡 `0029` | 🟡 `0039` | 🟡 `0049` | 🟡 `0059` |

### 3.3 10×6 全量 row-level 明细表

本表把 60 条 LLM-generated `STM_0` 逐行展开，避免只看 cluster 汇总时漏掉“同一 NL 下不同 LLM 输出的结构复杂度、转换来源与 loss 差异”。`states/trans` 来自 seed sweep archive 中的 canonical 状态 / 迁移计数；`source` 是当前进入 canonical / `.fcstm` 的 official PlantUML SCXML 路径来源；`fcstm_loss_rows` 只表示 R4.5 lowering/exporter 记录的 representation loss rows；R5 readiness caveat 另由 `caveat 简码` / `r5_loss_codes` 表示。因此可能出现 `fcstm_loss_rows=0` 但仍有 `norm-replay` caveat 的情况，例如 `0037` [clm-r552-row-detail][src-r552-archive][src-r552-case]。

caveat 简码：`norm-replay` = R3.1 / R5.5.2 pre-SCXML normalization replay；`guard→event` = 条件式 transition label 暂被降为 event；`src↑composite` / `tgt↑composite` = 端点提升到组合状态边界；`comp→initial` = 指向组合状态时降到 initial child；`initial推断` = 初始子状态由顺序 / start-state 约定推断；`cross-scope` = 跨层级迁移无法无损表示。

| NL# | LLM | pair | 状态 | source | states/trans | fcstm_loss_rows | caveat 简码 | story role |
|---:|---|---|---|---|---:|---:|---|---|
| 0 | GPT-4o | `0000` | 🟡 `partial` | `official_scxml_raw` | 7/7 | 3 | comp→initial<br>guard→event<br>src↑composite | `main_candidate` |
| 0 | GPT-4 | `0010` | 🟡 `partial` | `official_scxml_raw` | 6/8 | 3 | guard→event | `main_candidate` |
| 0 | Llama | `0020` | 🟡 `partial` | `official_scxml_r3_1_normalized_replay` | 8/9 | 3 | guard→event<br>src↑composite<br>norm-replay | `main_candidate` |
| 0 | Kimi | `0030` | 🟡 `partial` | `official_scxml_raw` | 7/7 | 1 | guard→event | `main_candidate` |
| 0 | DeepSeek | `0040` | 🟡 `partial` | `official_scxml_r3_1_normalized_replay` | 7/6 | 2 | guard→event<br>norm-replay | `main_candidate` |
| 0 | Claude | `0050` | 🟡 `partial` | `official_scxml_raw` | 9/9 | 1 | guard→event | `main_candidate` |
| 1 | GPT-4o | `0001` | 🟢 `converted` | `official_scxml_raw` | 5/6 | 0 | — | `main_candidate` |
| 1 | GPT-4 | `0011` | 🟢 `converted` | `official_scxml_raw` | 5/6 | 0 | — | `main_candidate` |
| 1 | Llama | `0021` | 🟡 `partial` | `official_scxml_r3_1_normalized_replay` | 5/6 | 0 | norm-replay | `main_candidate` |
| 1 | Kimi | `0031` | 🟢 `converted` | `official_scxml_raw` | 5/6 | 0 | — | `main_candidate` |
| 1 | DeepSeek | `0041` | 🟡 `partial` | `official_scxml_r3_1_normalized_replay` | 5/6 | 0 | norm-replay | `main_candidate` |
| 1 | Claude | `0051` | 🟢 `converted` | `official_scxml_raw` | 5/6 | 0 | — | `main_candidate` |
| 2 | GPT-4o | `0002` | 🟢 `converted` | `official_scxml_raw` | 6/6 | 0 | — | `main_candidate` |
| 2 | GPT-4 | `0013` | 🟢 `converted` | `official_scxml_raw` | 6/8 | 0 | — | `main_candidate` |
| 2 | Llama | `0023` | 🟡 `partial` | `official_scxml_r3_1_normalized_replay` | 5/4 | 0 | norm-replay | `main_candidate` |
| 2 | Kimi | `0033` | 🟡 `partial` | `official_scxml_r3_1_normalized_replay` | 6/7 | 1 | initial推断<br>norm-replay | `main_candidate` |
| 2 | DeepSeek | `0043` | 🟡 `partial` | `official_scxml_r3_1_normalized_replay` | 6/6 | 0 | norm-replay | `main_candidate` |
| 2 | Claude | `0053` | 🟢 `converted` | `official_scxml_raw` | 6/6 | 0 | — | `main_candidate` |
| 3 | GPT-4o | `0003` | 🟢 `converted` | `official_scxml_raw` | 7/7 | 0 | — | `main_candidate` |
| 3 | GPT-4 | `0012` | 🟢 `converted` | `official_scxml_raw` | 7/7 | 0 | — | `main_candidate` |
| 3 | Llama | `0022` | 🟡 `partial` | `official_scxml_r3_1_normalized_replay` | 7/9 | 0 | norm-replay | `main_candidate` |
| 3 | Kimi | `0032` | 🟡 `partial` | `official_scxml_r3_1_normalized_replay` | 7/13 | 0 | norm-replay | `main_candidate` |
| 3 | DeepSeek | `0042` | 🟡 `partial` | `official_scxml_r3_1_normalized_replay` | 7/9 | 0 | norm-replay | `main_candidate` |
| 3 | Claude | `0052` | 🟢 `converted` | `official_scxml_raw` | 7/8 | 0 | — | `main_candidate` |
| 4 | GPT-4o | `0004` | 🟡 `partial` | `official_scxml_r3_1_normalized_replay` | 10/9 | 1 | comp→initial<br>norm-replay | `main_candidate` |
| 4 | GPT-4 | `0014` | 🟡 `partial` | `official_scxml_raw` | 11/8 | 4 | comp→initial<br>initial推断 | `main_candidate` |
| 4 | Llama | `0024` | 🟡 `partial` | `official_scxml_r3_1_normalized_replay` | 9/10 | 1 | comp→initial<br>norm-replay | `main_candidate` |
| 4 | Kimi | `0034` | 🟡 `partial` | `official_scxml_r3_1_normalized_replay` | 10/13 | 1 | initial推断<br>norm-replay | `main_candidate` |
| 4 | DeepSeek | `0044` | 🟡 `partial` | `official_scxml_r3_1_normalized_replay` | 9/9 | 1 | initial推断<br>norm-replay | `main_candidate` |
| 4 | Claude | `0054` | 🟢 `converted` | `official_scxml_raw` | 9/8 | 0 | — | `main_candidate` |
| 5 | GPT-4o | `0005` | 🟡 `partial` | `official_scxml_raw` | 8/16 | 11 | comp→initial<br>initial推断<br>src↑composite | `main_candidate` |
| 5 | GPT-4 | `0015` | 🟡 `partial` | `official_scxml_raw` | 15/22 | 17 | src↑composite<br>tgt↑composite | `main_candidate` |
| 5 | Llama | `0025` | 🟡 `partial` | `official_scxml_r3_1_normalized_replay` | 7/16 | 0 | norm-replay | `main_candidate` |
| 5 | Kimi | `0035` | 🟡 `partial` | `official_scxml_r3_1_normalized_replay` | 7/16 | 0 | norm-replay | `main_candidate` |
| 5 | DeepSeek | `0045` | 🟡 `partial` | `official_scxml_r3_1_normalized_replay` | 17/20 | 7 | comp→initial<br>src↑composite<br>norm-replay | `main_candidate` |
| 5 | Claude | `0055` | 🟢 `converted` | `official_scxml_raw` | 7/16 | 0 | — | `main_candidate` |
| 6 | GPT-4o | `0006` | 🟢 `converted` | `official_scxml_raw` | 8/12 | 0 | — | `main_candidate` |
| 6 | GPT-4 | `0016` | 🟡 `partial` | `official_scxml_raw` | 13/11 | 2 | src↑composite | `main_candidate` |
| 6 | Llama | `0026` | 🟡 `partial` | `official_scxml_r3_1_normalized_replay` | 5/5 | 0 | norm-replay | `main_candidate` |
| 6 | Kimi | `0036` | 🟢 `converted` | `official_scxml_raw` | 6/7 | 0 | — | `main_candidate` |
| 6 | DeepSeek | `0046` | 🟡 `partial` | `official_scxml_r3_1_normalized_replay` | 5/6 | 0 | norm-replay | `main_candidate` |
| 6 | Claude | `0056` | 🟢 `converted` | `official_scxml_raw` | 9/10 | 0 | — | `main_candidate` |
| 7 | GPT-4o | `0007` | 🟢 `converted` | `official_scxml_raw` | 21/15 | 0 | — | `main_candidate` |
| 7 | GPT-4 | `0017` | 🟡 `partial` | `official_scxml_raw` | 6/10 | 5 | initial推断<br>src↑composite<br>tgt↑composite | `main_candidate` |
| 7 | Llama | `0027` | 🟡 `partial` | `official_scxml_r3_1_normalized_replay` | 8/9 | 1 | src↑composite<br>norm-replay | `main_candidate` |
| 7 | Kimi | `0037` | 🟡 `partial` | `official_scxml_r3_1_normalized_replay` | 12/10 | 0 | norm-replay | `main_candidate` |
| 7 | DeepSeek | `0047` | 🟡 `partial` | `official_scxml_r3_1_normalized_replay` | 10/15 | 3 | cross-scope<br>initial推断<br>norm-replay | `main_candidate` |
| 7 | Claude | `0057` | 🟡 `partial` | `official_scxml_raw` | 14/10 | 2 | initial推断 | `main_candidate` |
| 8 | GPT-4o | `0008` | 🟡 `partial` | `official_scxml_raw` | 27/27 | 18 | guard→event<br>cross-scope<br>src↑composite | `supplementary_stress` |
| 8 | GPT-4 | `0018` | 🟡 `partial` | `official_scxml_r3_1_normalized_replay` | 21/21 | 15 | guard→event<br>cross-scope<br>initial推断<br>src↑composite<br>norm-replay | `supplementary_stress` |
| 8 | Llama | `0028` | 🟡 `partial` | `official_scxml_r3_1_normalized_replay` | 21/23 | 3 | guard→event<br>norm-replay | `supplementary_stress` |
| 8 | Kimi | `0038` | 🟡 `partial` | `official_scxml_raw` | 23/24 | 18 | comp→initial<br>guard→event<br>cross-scope<br>initial推断<br>src↑composite<br>tgt↑composite | `supplementary_stress` |
| 8 | DeepSeek | `0048` | 🟡 `partial` | `official_scxml_r3_1_normalized_replay` | 21/24 | 3 | guard→event<br>norm-replay | `supplementary_stress` |
| 8 | Claude | `0058` | 🟡 `partial` | `official_scxml_r3_1_normalized_replay` | 26/22 | 18 | guard→event<br>initial推断<br>src↑composite<br>tgt↑composite<br>norm-replay | `supplementary_stress` |
| 9 | GPT-4o | `0009` | 🟡 `partial` | `official_scxml_raw` | 20/26 | 20 | guard→event<br>cross-scope<br>tgt↑composite | `main_candidate` |
| 9 | GPT-4 | `0019` | 🟡 `partial` | `official_scxml_raw` | 22/26 | 20 | guard→event<br>initial推断<br>src↑composite | `main_candidate` |
| 9 | Llama | `0029` | 🟡 `partial` | `official_scxml_r3_1_normalized_replay` | 19/27 | 22 | guard→event<br>initial推断<br>tgt↑composite<br>norm-replay | `main_candidate` |
| 9 | Kimi | `0039` | 🟡 `partial` | `official_scxml_raw` | 20/26 | 17 | guard→event | `main_candidate` |
| 9 | DeepSeek | `0049` | 🟡 `partial` | `official_scxml_raw` | 21/29 | 23 | guard→event<br>cross-scope<br>tgt↑composite | `main_candidate` |
| 9 | Claude | `0059` | 🟡 `partial` | `official_scxml_raw` | 22/25 | 16 | guard→event | `main_candidate` |

### 3.4 十个 NL cluster 的画像与后续使用口径

本表沿用 [2026-06-29-00-03-56 主 seed profile](./2026-06-29-00-03-56-llms-emp-main-seed-profile.md) 的 cluster 画像口径，但把状态数字更新到 R5.5.2 后的 `blocked=0` 当前事实。它回答“每条唯一 NL 在论文 story 中应如何使用”，而不是替代逐 row 的 raw pair 审计 [clm-r552-cluster-current][src-r552-clusters]。

| # | NL / 模型名 | role | 控制语义 | 时间 / 结构 | 行为特征 | 6 输出状态 | 主要 caveat / loss | 当前使用结论 |
|---:|---|---|---|---|---|---|---|---|
| 0 | `llms_emp_nl_00_hldcs_high_level_driving_module`<br>high-level driving module | `main_candidate` | 自动驾驶模式控制 | `T0` / `HSM` | 守卫式条件、动作/entry-exit、变量/数据条件、层级、伪状态 | 🟡6 | guard→event×6<br>src↑composite×2<br>norm-replay×2<br>comp→initial×1 | 可作为 T0 主候选池输入；后续 R5.7/R6 仍需逐例裁决 guard/action/lowering。 |
| 1 | `llms_emp_nl_01_hstbs_state_machine_diagram_of_the_base`<br>State machine diagram of the base brake subsystem | `main_candidate` | 制动子系统控制 | `T0` / `FSM` | 守卫式条件、动作/entry-exit、伪状态 | 🟢4 / 🟡2 | norm-replay×2 | 可作为 T0 主候选池输入；后续 R5.7/R6 仍需逐例裁决 guard/action/lowering。 |
| 2 | `llms_emp_nl_02_real_time_softwa_pump_control_state_machine`<br>Pump Control state machine | `main_candidate` | 泵子系统模式控制 | `T0` / `HSM` | 守卫式条件、层级 | 🟢3 / 🟡3 | norm-replay×3<br>initial推断×1 | 可作为 T0 主候选池输入；后续 R5.7/R6 仍需逐例裁决 guard/action/lowering。 |
| 3 | `llms_emp_nl_03_hsuv_hybrid_sport_utility_vehicle_hsuv`<br>Hybrid Sport Utility Vehicle, HSUV | `main_candidate` | 车辆运行模式控制 | `T0` / `HSM` | 守卫式条件、动作/entry-exit、层级 | 🟢3 / 🟡3 | norm-replay×3 | 可作为 T0 主候选池输入；后续 R5.7/R6 仍需逐例裁决 guard/action/lowering。 |
| 4 | `llms_emp_nl_04_real_time_softwa_state_machine_for_train_control`<br>state machine for Train Control | `main_candidate` | 列车运动控制 | `T0` / `HSM` | 守卫式条件、动作/entry-exit、层级 | 🟢1 / 🟡5 | norm-replay×4<br>comp→initial×3<br>initial推断×3 | 可作为 T0 主候选池输入；后续 R5.7/R6 仍需逐例裁决 guard/action/lowering。 |
| 5 | `llms_emp_nl_05_mocv_microwave_oven_control_with_entry`<br>Microwave Oven Control with entry and exit actions | `main_candidate` | 微波炉控制：timer-like caveat | `T0.5` / `UML-SysML statechart` | 守卫式条件、动作/entry-exit、变量/数据条件、显式时间 | 🟢1 / 🟡5 | src↑composite×3<br>norm-replay×3<br>comp→initial×2<br>initial推断×1<br>tgt↑composite×1 | 可进入主候选池，但 timer-like cue 必须单独标注 caveat。 |
| 6 | `llms_emp_nl_06_dscs_uav_swarm_state_machine_diagram`<br>UAV swarm state machine diagram | `main_candidate` | 无人机群任务控制 | `T0` / `HSM` | 守卫式条件、动作/entry-exit、层级 | 🟢3 / 🟡3 | norm-replay×2<br>src↑composite×1 | 可作为 T0 主候选池输入；后续 R5.7/R6 仍需逐例裁决 guard/action/lowering。 |
| 7 | `llms_emp_nl_07_hldcs_collision_avoidance_sub_machine_st`<br>Collision avoidance sub-machine state diagram | `main_candidate` | 碰撞规避模式控制 | `T0` / `UML-SysML statechart` | 守卫式条件、层级、并发/区域 | 🟢1 / 🟡5 | initial推断×3<br>norm-replay×3<br>src↑composite×2<br>cross-scope×1<br>tgt↑composite×1 | 可作为 T0 主候选池输入；后续 R5.7/R6 仍需逐例裁决 guard/action/lowering。 |
| 8 | `llms_emp_nl_08_dcs_digital_camera_state_machine_diagr`<br>Digital camera state machine diagrams | `supplementary_stress` | 相机控制：显式执行时间与伪状态压力样例 | `T1` / `UML-SysML statechart` | 守卫式条件、动作/entry-exit、变量/数据条件、层级、伪状态、并发/区域、显式时间 | 🟡6 | guard→event×6<br>src↑composite×4<br>norm-replay×4<br>cross-scope×3<br>initial推断×3 | 作为 supplementary / stress；不支撑 T0 主 claim。 |
| 9 | `llms_emp_nl_09_hldcs_autonomous_mode`<br>autonomous mode | `main_candidate` | 自动驾驶模式控制 | `T0` / `HSM` | 守卫式条件、动作/entry-exit、变量/数据条件、层级、伪状态 | 🟡6 | guard→event×6<br>tgt↑composite×3<br>cross-scope×2<br>initial推断×2<br>src↑composite×1 | 可作为 T0 主候选池输入；后续 R5.7/R6 仍需逐例裁决 guard/action/lowering。 |

### 3.5 LLM 维度与 loss 分布

| LLM | converted | partial | blocked | 结论 |
|---|---:|---:|---:|---|
| `GPT-4o` | 5 | 5 | 0 | 有可直接候选，也有 caveat |
| `GPT-4` | 3 | 7 | 0 | 有可直接候选，也有 caveat |
| `Llama` | 0 | 10 | 0 | 全 partial，需要 R5.7 重点审查 |
| `Kimi` | 2 | 8 | 0 | 有可直接候选，也有 caveat |
| `DeepSeek` | 0 | 10 | 0 | 全 partial，需要 R5.7 重点审查 |
| `Claude` | 6 | 4 | 0 | converted 比例最高 |

| loss code | 出现次数 | 学术含义 |
|---|---:|---|
| `R5.LOSS.r3_1_normalization_replay_not_repair` | 27 | 需要 pre-SCXML normalization replay；只能计 conversion readiness，不能算 repair gain。 |
| `R45.LOSS.condition_like_label_lowered_as_event` | 18 | 条件式 label 被保留为 event；这是后续 guard/event/action repair target 的核心候选。 |
| `R45.LOSS.source_lifted_to_composite_boundary` | 13 | 源端点被提升到组合状态边界；表示层级 lowering caveat。 |
| `R45.LOSS.initial_inferred_from_source_order_or_start_state` | 13 | 初始子状态由顺序或 start-state 约定推断；表示 caveat。 |
| `R45.LOSS.composite_target_lowered_to_initial_child` | 7 | 指向组合状态的迁移被降到 initial child；表示 caveat。 |
| `R45.LOSS.target_lifted_to_composite_boundary` | 7 | 目标端点被提升到组合状态边界；表示 caveat。 |
| `R45.LOSS.cross_scope_transition_unrepresentable` | 6 | 跨层级迁移无法无损表示；需要后续逐例资格审查。 |

## 4. 代表性 PlantUML vs `.fcstm` 对照

本节不把 `.fcstm` 片段当作人工改写结果；它们是从一手 `Generation PlantUML` 经 committed PlantUML recovery archive / SCXML / R4.5 lowering 代码重放得到的派生视图。片段只用于解释当前数据流与主要 caveat，完整复验命令见 [cmd-r552-snippets] [clm-r552-snippets][src-r552-pairs][src-r552-recovery]。

| pair | 状态 | 为什么选它 | conversion source | canonical states / transitions | fcstm_loss_rows / 主要 caveat |
|---|---|---|---|---:|---|
| `llms_emp_stm_results_0001` | 🟢 `converted` | 最小可用 FSM：制动子系统，无当前 loss，用于说明 pipeline 正向路径。 | `official_scxml_raw` | 5 / 6 | 0 / 无 |
| `llms_emp_stm_results_0000` | 🟡 `partial` | HSM 自动驾驶：条件式 `Front Distance > 10` 在 `.fcstm` 中被保留为 named event，体现 R5.7 必须处理 guard/event/action。 | `official_scxml_raw` | 7 / 7 | 3 / `R45.LOSS.composite_target_lowered_to_initial_child`, `R45.LOSS.condition_like_label_lowered_as_event`, `R45.LOSS.source_lifted_to_composite_boundary` |
| `llms_emp_stm_results_0018` | 🟡 `partial` | 原 blocked：GPT-4 Digital Camera；R5.5.2 后可导出，但显式时间、概率/choice 与层级损失集中，仍只是 supplementary stress。 | `official_scxml_r3_1_normalized_replay` | 21 / 21 | 15 / `R45.LOSS.condition_like_label_lowered_as_event`, `R45.LOSS.cross_scope_transition_unrepresentable`, `R45.LOSS.initial_inferred_from_source_order_or_start_state`, `R45.LOSS.source_lifted_to_composite_boundary`, `R5.LOSS.r3_1_normalization_replay_not_repair` |
| `llms_emp_stm_results_0028` | 🟡 `partial` | 原 blocked：Llama Digital Camera；大量 `min/max` / 条件标签进入 event，说明 T1 不能支撑 T0 主 claim。 | `official_scxml_r3_1_normalized_replay` | 21 / 23 | 3 / `R45.LOSS.condition_like_label_lowered_as_event`, `R5.LOSS.r3_1_normalization_replay_not_repair` |
| `llms_emp_stm_results_0037` | 🟡 `partial` | 原 blocked：Kimi Collision Avoidance；机器 loss 主要剩 normalization replay，但 NL 中 orthogonal regions / concurrency 语义仍需后续人工裁决。 | `official_scxml_r3_1_normalized_replay` | 12 / 10 | 0 / `R5.LOSS.r3_1_normalization_replay_not_repair` |
| `llms_emp_stm_results_0039` | 🟡 `partial` | committed selected smoke 样例：Autonomous / Collision 条件最密集，展示 guard-like 条件被保留为 event。 | `official_scxml_raw` | 20 / 26 | 17 / `R45.LOSS.condition_like_label_lowered_as_event` |
| `llms_emp_stm_results_0045` | 🟡 `partial` | DeepSeek Microwave：timer-like cue、entry/exit 和层级边界 caveat，是 T0.5 主池边界样例。 | `official_scxml_r3_1_normalized_replay` | 17 / 20 | 7 / `R45.LOSS.composite_target_lowered_to_initial_child`, `R45.LOSS.source_lifted_to_composite_boundary`, `R5.LOSS.r3_1_normalization_replay_not_repair` |

这里的 `fcstm_loss_rows` 与 readiness `conversion_status` 不是同一层口径：`fcstm_loss_rows=0` 只表示 lowering/exporter 未记录 representation loss row；只要 row 带有 `R5.LOSS.r3_1_normalization_replay_not_repair` 等 caveat，报告状态仍应按 case matrix 记为 `partial` [clm-r552-row-detail][clm-r552-no-repair-gain]。

### 4.1 `llms_emp_stm_results_0001` — clean_converted

- LLM / NL cluster：`gpt-4o` / `llms_emp_nl_01_hstbs_state_machine_diagram_of_the_base`；时间等级 `T0`；结构族 `FSM`；当前状态 `converted`。
- 一手 locator：`sheet=STM Results; row=1; columns=Requirement Description,Generation PlantUML,LLMs,Model Source,Model Name,PlantUML`。
- 解读：最小可用 FSM：制动子系统，无当前 loss，用于说明 pipeline 正向路径。

PlantUML `STM_0` 片段：
```plantuml
@startuml
[*] --> InitialState
...
InitialState --> BrakingState : Brake Signal Received
InitialState --> OperationalState : Signal Transmission Fails
...
BrakingState --> ClampingState : Entering Clamping State
ClampingState : Brake Caliper Clamping State
...
OperationalState --> InitialState : Signal Feedback Sent
BrakingState --> InitialState : Signal Feedback Sent
```

`.fcstm` 派生片段：
```text
state llms_emp_stm_results_0001 named "llms_emp_stm_results_0001" {
    [*] -> start;
    event Brake_Signal_Received named "Brake Signal Received";
    event Entering_Clamping_State named "Entering Clamping State";
    event Signal_Feedback_Sent named "Signal Feedback Sent";
    event Signal_Transmission_Fails named "Signal Transmission Fails";
    pseudo state start named "start";
    state InitialState named "InitialState";
    state BrakingState named "BrakingState";
    state OperationalState named "OperationalState";
    state ClampingState named "ClampingState";
    start -> InitialState;
    InitialState -> BrakingState : Brake_Signal_Received;
    InitialState -> OperationalState : Signal_Transmission_Fails;
    BrakingState -> ClampingState : Entering_Clamping_State;
    BrakingState -> InitialState : Signal_Feedback_Sent;
    OperationalState -> InitialState : Signal_Feedback_Sent;
}
```


### 4.2 `llms_emp_stm_results_0000` — guard_as_event

- LLM / NL cluster：`gpt-4o` / `llms_emp_nl_00_hldcs_high_level_driving_module`；时间等级 `T0`；结构族 `HSM`；当前状态 `partial`。
- 一手 locator：`sheet=STM Results; row=0; columns=Requirement Description,Generation PlantUML,LLMs,Model Source,Model Name,PlantUML`。
- 解读：HSM 自动驾驶：条件式 `Front Distance > 10` 在 `.fcstm` 中被保留为 named event，体现 R5.7 必须处理 guard/event/action。

PlantUML `STM_0` 片段：
```plantuml
@startuml
[*] --> HumanDriving
...
state HumanDriving {
    [*] --> InitialState : Power On
    InitialState : Initial State
    InitialState --> Autonomous : Front Distance > 10
    Autonomous --> HumanDriving : Human Steering Cmd or Brake Pressed
    HumanDriving --> FinalState : Power Off
    FinalState : Final State
...
state Autonomous {
    [*] --> InitialState : Enter Autonomous
    InitialState : Initial State
```

`.fcstm` 派生片段：
```text
state llms_emp_stm_results_0000 named "llms_emp_stm_results_0000" {
    [*] -> start;
    pseudo state start named "start";
    state HumanDriving named "HumanDriving" {
        [*] -> startHumanDriving;
        event Enter_Autonomous named "Enter Autonomous";
        event Exit_Autonomous named "Exit Autonomous";
        event Front_Distance_10 named "Front Distance > 10";
        event Human_Steering_Cmd_or_Brake_Pressed named "Human Steering Cmd or Brake Pressed";
        event Power_Off named "Power Off";
        event Power_On named "Power On";
        pseudo state startHumanDriving named "startHumanDriving";
        state InitialState named "InitialState";
        state FinalState named "FinalState";
        state Autonomous named "Autonomous" {
            [*] -> startAutonomous;
            pseudo state startAutonomous named "startAutonomous";
        }
        ! * -> FinalState : Power_Off;
        startHumanDriving -> InitialState : Power_On;
        InitialState -> Autonomous : Front_Distance_10;
        InitialState -> FinalState : Exit_Autonomous;
```


### 4.3 `llms_emp_stm_results_0018` — recovered_t1_complex

- LLM / NL cluster：`gpt-4` / `llms_emp_nl_08_dcs_digital_camera_state_machine_diagr`；时间等级 `T1`；结构族 `UML-SysML statechart`；当前状态 `partial`。
- 一手 locator：`sheet=STM Results; row=18; columns=Requirement Description,Generation PlantUML,LLMs,Model Source,Model Name,PlantUML`。
- 解读：原 blocked：GPT-4 Digital Camera；R5.5.2 后可导出，但显式时间、概率/choice 与层级损失集中，仍只是 supplementary stress。

PlantUML `STM_0` 片段：
```plantuml
@startuml
[*] --> TurnOn : 2 sec
state fork1
TurnOn --> fork1
...
fork1 --> AutoFocus : 1-2 sec
state AutoFocus {
    state choice1
    AutoFocus -down-> choice1 : memFull=true
...
fork1 --> DetLight : <1 sec
state DetLight {
    state choice2
    DetLight -down-> choice2 : <<GaStep>>{prob=0.4}
```

`.fcstm` 派生片段：
```text
state llms_emp_stm_results_0018 named "llms_emp_stm_results_0018" {
    [*] -> start;
    event _1_2_sec named "1-2 sec";
    event _2_sec named "2 sec";
    event _1_sec named "<1 sec";
    pseudo state start named "start";
    state TurnOn named "TurnOn";
    state fork1 named "fork1";
    state TurnOff named "TurnOff";
    state end named "end";
    state AutoFocus named "AutoFocus" {
        [*] -> choice1;
        event memFull_true named "memFull=true";
        state choice1 named "choice1";
        ! * -> choice1 : memFull_true;
    }
    state DetLight named "DetLight" {
        [*] -> choice2;
        event when_sunny_true named "when sunny=true";
        event _GaStep_prob_0_4 named "«GaStep»{prob=0.4}";
...
        ! * -> choice2 : _GaStep_prob_0_4;
...
        [*] -> ChargedFlash;
```


### 4.4 `llms_emp_stm_results_0028` — recovered_t1_timing_labels

- LLM / NL cluster：`llama` / `llms_emp_nl_08_dcs_digital_camera_state_machine_diagr`；时间等级 `T1`；结构族 `UML-SysML statechart`；当前状态 `partial`。
- 一手 locator：`sheet=STM Results; row=28; columns=Requirement Description,Generation PlantUML,LLMs,Model Source,Model Name,PlantUML`。
- 解读：原 blocked：Llama Digital Camera；大量 `min/max` / 条件标签进入 event，说明 T1 不能支撑 T0 主 claim。

PlantUML `STM_0` 片段：
```plantuml
@startuml
...
[*] --> TurnOn
TurnOn: TurnOn, min: 2s, max: 2s
TurnOn --> fork1: after 2s
fork1 --> AutoFocus: min: 1s, max: 2s
fork1 --> DetLight: min: 0s, max: 1s
fork1 --> choice3:
AutoFocus --> choice1: memFull=true
choice1 --> choice3:
DetLight --> choice2: <<GaStep>>{prob=0.4}
choice2 --> Join2: sunny=true
choice2 --> Join1:
```

`.fcstm` 派生片段：
```text
state llms_emp_stm_results_0028 named "llms_emp_stm_results_0028" {
    [*] -> start;
    event Charged_true named "Charged=true";
    event after_2s named "after 2s";
    event memFull_true named "memFull=true";
    event min_0s_max_1s named "min: 0s, max: 1s";
    event min_1s_max_2s named "min: 1s, max: 2s";
    event min_2s_max_3s named "min: 2s, max: 3s";
    event min_2s_max_4s named "min: 2s, max: 4s";
    event sunny_true named "sunny=true";
    event _GaStep_prob_0_4 named "«GaStep»{prob=0.4}";
    pseudo state start named "start";
    state TurnOn named "TurnOn";
    state fork1 named "fork1";
    state AutoFocus named "AutoFocus";
    state DetLight named "DetLight";
    state choice3 named "choice3";
    state choice1 named "choice1";
...
    start -> TurnOn;
    TurnOn -> fork1 : after_2s;
    fork1 -> AutoFocus : min_1s_max_2s;
    fork1 -> DetLight : min_0s_max_1s;
```


### 4.5 `llms_emp_stm_results_0037` — recovered_collision_regions

- LLM / NL cluster：`kimi` / `llms_emp_nl_07_hldcs_collision_avoidance_sub_machine_st`；时间等级 `T0`；结构族 `UML-SysML statechart`；当前状态 `partial`。
- 一手 locator：`sheet=STM Results; row=37; columns=Requirement Description,Generation PlantUML,LLMs,Model Source,Model Name,PlantUML`。
- 解读：原 blocked：Kimi Collision Avoidance；机器 loss 主要剩 normalization replay，但 NL 中 orthogonal regions / concurrency 语义仍需后续人工裁决。

PlantUML `STM_0` 片段：
```plantuml
@startuml
stm CollisionAvoidanceSystem
[*] --> InitialState
...
InitialState --> FrontendCollision : Frontend Collision Detected
InitialState --> RearEndCollision : Rear-End Collision Detected
InitialState --> PedestrianCollision : Pedestrian Collision Detected
...
[FrontendCollision] -down-> [BrakingControl] : Brake Signal Received
[RearEndCollision] -down-> [SteeringControl] : Steering Signal Received
[PedestrianCollision] -down-> [EmergencyStop] : Emergency Stop Signal Received
...
[BrakingControl] --> [*] : Collision Avoided
[SteeringControl] --> [*] : Collision Avoided
[EmergencyStop] --> [*] : Collision Avoided
```

`.fcstm` 派生片段：
```text
state llms_emp_stm_results_0037 named "llms_emp_stm_results_0037" {
    [*] -> start;
    event Brake_Signal_Received named "Brake Signal Received";
    event Collision_Avoided named "Collision Avoided";
    event Emergency_Stop_Signal_Received named "Emergency Stop Signal Received";
    event Frontend_Collision_Detected named "Frontend Collision Detected";
    event Pedestrian_Collision_Detected named "Pedestrian Collision Detected";
    event Rear_End_Collision_Detected named "Rear-End Collision Detected";
    event Steering_Signal_Received named "Steering Signal Received";
    state FrontendCollision_2ab70d named "FrontendCollision_2ab70d";
    state BrakingControl_55527e named "BrakingControl_55527e";
    state RearEndCollision_ab600a named "RearEndCollision_ab600a";
    state SteeringControl_01e978 named "SteeringControl_01e978";
    state PedestrianCollision_3ebdfd named "PedestrianCollision_3ebdfd";
    state EmergencyStop_72d167 named "EmergencyStop_72d167";
    pseudo state start named "start";
    state InitialState named "InitialState";
    state FrontendCollision named "FrontendCollision";
...
    FrontendCollision_2ab70d -> BrakingControl_55527e : Brake_Signal_Received;
    BrakingControl_55527e -> end : Collision_Avoided;
    RearEndCollision_ab600a -> SteeringControl_01e978 : Steering_Signal_Received;
    SteeringControl_01e978 -> end : Collision_Avoided;
```


### 4.6 `llms_emp_stm_results_0039` — selected_guard_dense

- LLM / NL cluster：`kimi` / `llms_emp_nl_09_hldcs_autonomous_mode`；时间等级 `T0`；结构族 `HSM`；当前状态 `partial`。
- 文件入口：[selected_seed_examples/llms-emp-kimi-autonomous-collision/stm0.puml](../selected_seed_examples/llms-emp-kimi-autonomous-collision/stm0.puml) 与 [selected_seed_examples/llms-emp-kimi-autonomous-collision/model.fcstm](../selected_seed_examples/llms-emp-kimi-autonomous-collision/model.fcstm)。
- 解读：这是当前 smoke panel 中最适合说明 guard/event/action 问题的 committed pair。PlantUML 里多处 `dist_to_front<25 && extra_lane=true`、`auto_finished=true`、`pedestrian_detected || ...` 看起来像 guard；但在 `.fcstm` 中仍作为 `event ... named "原始条件文本"` 保留，R5.7 不能跳过逐例语义裁决直接把它们当作 guard。

PlantUML `STM_0` 片段：
```plantuml
@startuml
[*] --> AutonomousMode
...
state AutonomousMode {
InitialState --> HighwayMode : high_way=true
InitialState --> UrbanMode : urban_way=true
...
state HighwayMode {
cruise --> lane_change : dist_to_front<25 && extra_lane=true
lane_change --> cruise : lane change completed
lane_change --> [*] : dist_to_exit<2
HighwayMode --> FinishState : auto_finished=true
...
state UrbanMode {
enter_urban --> lane_change_urban : dist_to_front<15 && extra_lane=true
```

`.fcstm` 派生片段：
```text
state llms_emp_stm_results_0039 named "llms_emp_stm_results_0039" {
    [*] -> start;
    event front_inactive_rear_inactive_pedestrian_inactive named "front_inactive && rear_inactive && pedestrian_inactive";
    event pedestrian_detected_dist_to_rear_5_vel_30_dist_to_front_15_in_HighwayMode_dist_to_front_10_in_UrbanMode named "pedestrian_detected || (dist_to_rear<5 && vel>30) || (dist_to_front<15 in HighwayMode || dist_to_front<10 in UrbanMode)";
...
        state HighwayMode named "HighwayMode" {
            event dist_to_exit_2 named "dist_to_exit<2";
            event dist_to_front_25_extra_lane_true named "dist_to_front<25 && extra_lane=true";
...
            cruise -> lane_change : dist_to_front_25_extra_lane_true;
            cruise -> endHighwayMode : dist_to_exit_2;
```

### 4.7 `llms_emp_stm_results_0045` — t05_timer_like

- LLM / NL cluster：`deepseek` / `llms_emp_nl_05_mocv_microwave_oven_control_with_entry`；时间等级 `T0.5`；结构族 `UML-SysML statechart`；当前状态 `partial`。
- 一手 locator：`sheet=STM Results; row=45; columns=Requirement Description,Generation PlantUML,LLMs,Model Source,Model Name,PlantUML`。
- 解读：DeepSeek Microwave：timer-like cue、entry/exit 和层级边界 caveat，是 T0.5 主池边界样例。

PlantUML `STM_0` 片段：
```plantuml
@startuml
stm MicrowaveStateMachine [Microwave State Machine]
...
[*] --> DoorShut
...
state DoorShut {
[*] --> DoorShutIdle
DoorShutIdle --> DoorShutIdle : Cancel
DoorShutIdle --> DoorOpen : Door Opened
...
state DoorOpen {
[*] --> DoorOpenIdle
DoorOpenIdle --> DoorOpenWithItem : Item Placed
DoorOpenWithItem --> DoorOpenIdle : Item Removed
DoorOpenWithItem --> DoorShutWithItem : Door Closed [zero time set]
```

`.fcstm` 派生片段：
```text
state llms_emp_stm_results_0045 named "llms_emp_stm_results_0045" {
    [*] -> start;
    pseudo state start named "start";
    state DoorShut named "DoorShut" {
        [*] -> startDoorShut;
        event Cancel named "Cancel";
        event Door_Opened named "Door Opened";
        pseudo state startDoorShut named "startDoorShut";
        state DoorShutIdle named "DoorShutIdle";
        state DoorOpen named "DoorOpen" {
            [*] -> startDoorOpen;
            event Cancel named "Cancel";
            event Cooking_Time_Entered named "Cooking Time Entered";
            event Door_Closed_zero_time_set named "Door Closed [zero time set]";
            event Door_Opened named "Door Opened";
            event Item_Placed named "Item Placed";
            event Item_Removed named "Item Removed";
            event Timer_Expired named "Timer Expired";
            pseudo state startDoorOpen named "startDoorOpen";
...
                [*] -> startDoorShutWithItem;
                pseudo state startDoorShutWithItem named "startDoorShutWithItem";
...
                startDoorShutWithItem -> DoorShutWithItemIdle;
```

## 5. 当前计数快照

### 5.1 `llms-emp` 60 pair

| conversion_status | pairs |
|---|---:|
| `converted` | 16 |
| `partial` | 44 |
| `blocked` | 0 |

### 5.2 全 seed sweep pair

| status | pairs |
|---|---:|
| `converted` | 529 |
| `partial` | 508 |
| `blocked` | 19 |
| `not_applicable` | 20 |
| `needs_generation` | 2 |

### 5.3 PlantUML recovery report

下表是 PlantUML recovery artifact 的当前计数快照，用于说明本次恢复发生在 official SCXML 之前的 conversion readiness 层；它支撑“`llms-emp-stm-subset.failed_after=0` 与全局 normalization 可审计”这两个事实，但不支撑 repair gain [clm-r552-recovery][src-r552-recovery][src-r552-ledger]。

| 指标 | 数量 |
|---|---:|
| PlantUML 一手 pair 总数 | 1049 |
| 原始官方 SCXML 已可转换 | 550 |
| 原始失败 | 499 |
| all-rules 技术通过 | 480 |
| low-risk / main eligibility 通过 | 470 |
| normalization ledger source-trace 完整行数 | 3908/3908 |
| normalization 后仍失败 | 19 |
| `llms-emp-stm-subset` failed after | 0 |

## 6. 学术风险与禁止主张

1. 禁止把本次 `blocked -> partial` 写成 Better STM repair loop 的效果；它发生在 official SCXML 之前的 conversion readiness 层 [clm-r552-no-repair-gain]。
2. 禁止把 `partial` 直接写成语义正确。三个恢复样例均仍有 loss code 或 caveat；`partial` 的含义是“可进入后续资格审查 / 修正候选池”，不是“无损转换” [clm-r552-targets]。
3. 禁止用 synthetic collateral `unified_uml_state_train_0265` 影响 `llms-emp` 主 seed story；它只能说明 normalization 规则的全局副作用被记录并可审计 [clm-r552-global]。
4. R5.6 scope 可删除“`llms-emp` blocked negative evidence”作为当前事实，但不能删除 Digital Camera/T1 supplementary stress、conversion gain 不计 repair gain、guard/action/time 需后续裁决这些限制 [clm-r552-scope]。

## 7. 后续入口

- R5.5 收口：以本 report 更新 [STATUS.md](../STATUS.md)、[reports/SUMMARY.md](./SUMMARY.md) 与 PR #134 comment。
- R5.6：更新 paper story / model scope 时，应把 `llms-emp` 当前状态写成 `16 converted / 44 partial / 0 blocked`，并保留 T0 主线与 Digital Camera supplementary stress。
- R5.7/R6：优先处理 `condition_like_label_lowered_as_event`、层级 boundary lowering、并发/区域与 timer-like caveat；这些不是 R5.5.2 已解决的问题。

## 审计附录：证据链与事实源

### A.1 来源考据表

| source path | source creation commit | prefix commit | substantive fact commit 判定理由 | non-prefix revision/migration commit | canonical machine source |
|---|---|---|---|---|---|
| `reports/2026-06-29-19-55-45-r5-5-2-plantuml-blocked-recovery.md` | 本 PR 工作树创建；提交后以本文件 git history 为准 | `2026-06-29 19:55:45 +0800` | R5.5.2 重新运行 PlantUML recovery、seed sweep 与 llms-emp profile 后形成新的当前事实：`llms-emp blocked=0`。 | 无 | [llms_emp_case_matrix.jsonl](../pipeline/readiness_audit/llms_emp_profile/llms_emp_case_matrix.jsonl)、[plantuml_recovery_report.json](../pipeline/conversion/reports/plantuml_recovery_report.json)、[sweep_report.json](../pipeline/readiness_audit/seed_sweep/sweep_report.json) |

> 注：`plantuml_recovery_report.json` 与 `manifest.json` 中的 `generator_code_commit` 记录的是 clean generator 代码提交（生成 artifact 前的代码状态），而不是承载 artifact 的最终 commit；这是为了避免 report 自指 hash / artifact commit 递归问题。复核时应同时检查 `generator_worktree_dirty=false` 与当前 PR diff 中 artifact 文件是否同步提交。

### A.2 上游事实源清单

| 编号 / 引用键 | source_id | 事实源 | 类型 | 用途 | 关键锚点 |
|---|---|---|---|---|---|
| [src-r552-case] | `case_matrix` | [llms_emp_case_matrix.jsonl](../pipeline/readiness_audit/llms_emp_profile/llms_emp_case_matrix.jsonl) | `jsonl` | 支撑 60 pair 当前状态、三个恢复样例、source trace 与 no-repair-gain 布尔口径 | `conversion_status`、`canonical_status`、`repair_contribution_allowed=false`、`raw_pair_id in {0018,0028,0037}` |
| [src-r552-clusters] | `cluster_profiles` | [llms_emp_cluster_profiles.jsonl](../pipeline/readiness_audit/llms_emp_profile/llms_emp_cluster_profiles.jsonl) | `jsonl` | 支撑 10 个唯一 NL cluster 的时间等级、结构族、行为特征、status 分布和 loss 分布 | `nl_cluster_index`、`status_counts`、`behavior_feature_profile`、`loss_code_counts` |
| [src-r552-pairs] | `llms_emp_pairs` | [pairs.jsonl](../corpora/seed_library/llms-emp-stm-subset/assets/extracted/pairs.jsonl) | `jsonl` | 支撑 10 unique NL × 6 LLM-generated `STM_0` 分母、一手 workbook locator 与 PlantUML 原文片段 | `pair_id`、`nl_text`、`stm0_text`、`llm`、`source_locator`、`source_sha256` |
| [src-r552-partial] | `partial_ledger` | [llms_emp_partial_attribution_ledger.jsonl](../pipeline/readiness_audit/llms_emp_profile/llms_emp_partial_attribution_ledger.jsonl) | `jsonl` | 支撑 44 条 partial 归因与 no-repair-gain caveat 文本说明 | `r5_loss_code`、`r5_loss_codes`、`notes` |
| [src-r552-blocked] | `blocked_probe` | [llms_emp_blocked_probe.jsonl](../pipeline/readiness_audit/llms_emp_profile/llms_emp_blocked_probe.jsonl) | `jsonl` | 支撑当前 `llms-emp blocked=0` | row count = 0 |
| [src-r552-recovery] | `plantuml_recovery_report` | [plantuml_recovery_report.json](../pipeline/conversion/reports/plantuml_recovery_report.json) | `json` | 支撑 official PlantUML recovery、rule ids 与 low-risk / main eligibility 统计 | `summary.by_seed.llms-emp-stm-subset.failed_after=0`、`items[pair_id]` |
| [src-r552-ledger] | `normalization_ledger` | [plantuml_normalization_ledger.jsonl](../pipeline/conversion/reports/plantuml_normalization_ledger.jsonl) | `jsonl` | 支撑每条 normalization 变更的 rule id/source locator/raw hash | rows with target `pair_id` |
| [src-r552-sweep] | `sweep_report` | [sweep_report.json](../pipeline/readiness_audit/seed_sweep/sweep_report.json) | `json` | 支撑全 seed sweep 当前 pair 状态 | `summary.pair_status_counts` |
| [src-r552-index] | `records_index` | [records_index.json](../pipeline/readiness_audit/seed_sweep/records_index.json) | `json` | 支撑全局 no-regression 与 collateral unified row 定位 | `record_id`、`status`、`archive_path` |
| [src-r552-archive] | `record_archives` | [artifact archives](../pipeline/readiness_audit/artifact_archives/archives/) | `zip` | 支撑高基数 per-pair record 复验 | `llms-emp-stm-subset_records/*.json`、`unified-uml-multimodal-validation_records/*.json` |

### A.3 Claim-evidence map

| 编号 / 引用键 | claim_id | 结论 / claim | 类型 | 上游事实源与锚点 | 复验命令 | 置信度 | 限制 / caveat |
|---|---|---|---|---|---|---|---|
| [clm-r552-boundary] | `R5.5.2-C0` | 本 report 只覆盖 PlantUML pre-SCXML recovery，不新增 pipeline、不修改 raw assets。 | `prohibition` | [src-r552-case] source hash fields；PR diff 不含 `corpora/.../assets/raw` / `pairs.jsonl`。 | [cmd-r552-no-regression] | `high` | 不能据此声称修正循环已运行。 |
| [clm-r552-status] | `R5.5.2-C1` | `llms-emp` 当前为 `converted=16 / partial=44 / blocked=0`。 | `count` | [src-r552-case] `conversion_status`；[src-r552-blocked] row count。 | [cmd-r552-status] | `high` | readiness 状态，不是最终实验结果。 |
| [clm-r552-targets] | `R5.5.2-C2` | 三个原 blocked 样例 `0018/0028/0037` 均恢复为 `partial`，canonical/parse/inspect 均可用。 | `trace` | [src-r552-case] rows by `raw_pair_id`；[src-r552-recovery] matching `items[pair_id]`。 | [cmd-r552-status] | `high` | `partial` 不等于语义无损。 |
| [clm-r552-denominator] | `R5.5.2-C2a` | `llms-emp` 的实验分母是 10 条唯一 NL cluster 与 60 条 LLM-generated `STM_0`，不能写成 60 条互不相关需求。 | `denominator` | [src-r552-pairs] `nl_sha256` unique count = 10、row count = 60；[src-r552-case] `nl_cluster_id` unique count = 10。 | [cmd-r552-status] | `high` | row 仍按 LLM 输出计入 conversion readiness；需求族分析按 NL cluster 汇总。 |
| [clm-r552-10x6] | `R5.5.2-C2b` | 当前 10×6 矩阵中 16 条 converted、44 条 partial、0 条 blocked；Llama/DeepSeek 在该矩阵中全为 partial，Claude converted 数最多。 | `count/profile` | [src-r552-case] `conversion_status` by `nl_cluster_id`/`llm_family`；[src-r552-partial] loss attribution。 | [cmd-r552-status] | `high` | 这是 readiness/profile 结论，不代表最终主实验 eligibility 已冻结。 |
| [clm-r552-row-detail] | `R5.5.2-C2d` | 60 条 row-level 明细表中的 conversion source、canonical states/transitions、`fcstm_loss_rows` 与 caveat 简码均来自当前 case matrix 与 seed sweep record archive。 | `trace/profile` | [src-r552-case] rows；[src-r552-archive] per-pair records `conversion_source`、`canonical_states_count`、`canonical_transitions_count`、`loss_count`。 | [cmd-r552-status] / [cmd-r552-snippets] | `high` | `fcstm_loss_rows` 是 lowering/exporter 层 loss row，不等于 readiness `conversion_status`；完整模型仍以 archive / replay 命令复验。 |
| [clm-r552-cluster-current] | `R5.5.2-C2e` | 十个 NL cluster 的 role/time/structure/feature/status/loss 画像已更新为 R5.5.2 后 `blocked=0` 的当前事实。 | `profile` | [src-r552-clusters] `status_counts`、`time_level`、`structure_family`、`behavior_feature_profile`、`loss_code_counts`。 | [cmd-r552-status] | `high` | cluster 画像服务 story 与采样决策，不替代 row-level eligibility 审查。 |
| [clm-r552-snippets] | `R5.5.2-C2c` | report 中 PlantUML vs `.fcstm` 对照片段均可从一手 pairs 与 committed recovery archive 经现有 converter/lowering 代码重放得到。 | `trace/example` | [src-r552-pairs] raw `stm0_text`；[src-r552-recovery] `structured_export_path`；[src-r552-case] status/loss；R4.5 lowering code。 | [cmd-r552-snippets] | `medium` | 片段为人类解释用摘录；完整模型必须回到原始 pair、SCXML/canonical 与 run artifacts 复验。 |
| [clm-r552-no-regression] | `R5.5.2-C3` | 相对 R5.5 base，`llms-emp` 只有三个目标样例从 `blocked` 改为 `partial`，其余 57 条无状态退化且 source trace 不变。 | `trace` | `git show origin/paper1/r5.5-llms-emp-deep-profile:...case_matrix.jsonl` vs [src-r552-case]。 | [cmd-r552-no-regression] | `high` | 只比较 case matrix 的状态和 source trace 字段；不证明模型语义完全等价，也不承诺派生 `.fcstm` hash 完全不漂移。 |
| [clm-r552-derived-drift] | `R5.5.2-C3b` | 完整重跑中 `llms_emp_stm_results_0024` 出现非状态派生漂移：`fcstm_sha256` 与 `r5_loss_codes` 更新，但 `conversion_status=partial`、source trace 与 repair-gain 禁止口径不变。 | `trace` | R5.5 base case matrix vs [src-r552-case] row `llms_emp_stm_results_0024`。 | [cmd-r552-no-regression] 的补充 diff 检查 | `medium` | 这说明 no-regression gate 是“状态/source trace 不退化”，不是 bit-for-bit artifact freeze。`target_lifted_to_composite_boundary` 到 `composite_target_lowered_to_initial_child` 的归因方向变化对后续 repair target 可能有语义影响；R5.7/R6 若依赖 0024，应回到 raw STM/SCXML/FCSTM 做逐例复核。 |
| [clm-r552-global] | `R5.5.2-C4` | 全 seed sweep 当前为 `converted=529 / partial=508 / blocked=19 / not_applicable=20 / needs_generation=2`，其中 `unified_uml_state_train_0265` 是 collateral `blocked -> partial`。 | `count` | [src-r552-sweep] `summary.pair_status_counts`；[src-r552-index] record status diff。 | [cmd-r552-no-regression] | `high` | unified synthetic collateral 不进入主 seed claim。 |
| [clm-r552-recovery] | `R5.5.2-C5` | PlantUML recovery 后 `llms-emp-stm-subset.failed_after=0`，全局 low-risk/main eligibility 为 470，normalization ledger 3908 行均带 source locator、源行 hash 与源文件 hash。 | `count/trace` | [src-r552-recovery] `summary.by_seed.llms-emp-stm-subset` 与 `summary.main_eligibility_included`；[src-r552-ledger] 全行 `source_pairs_path/source_locator/source_line_sha256/source_file_sha256`。 | [cmd-r552-recovery] | `high` | conversion eligibility，不是 repair success。 |
| [clm-r552-no-repair-gain] | `R5.5.2-C6` | R5.5.2 recovery 不得计入 repair gain。 | `prohibition` | [src-r552-case] `repair_contribution_allowed=false`；[src-r552-partial] `R5.LOSS.r3_1_normalization_replay_not_repair` 与 no-repair-gain `notes`；[src-r552-recovery] `conversion_contract`。 | [cmd-r552-status] | `high` | 后续 paper 只能把它写成输入可用性恢复。 |
| [clm-r552-scope] | `R5.5.2-C7` | 当前 scope 仍应保持 T0 主线 + Digital Camera supplementary stress；只是 `llms-emp` blocked negative evidence 不再作为当前事实。 | `decision` | [src-r552-case] `time_level`、`r5_6_story_role`、target rows；[src-r552-partial] caveat。 | [cmd-r552-status] | `medium` | R5.6/R5.7 仍需正式 story/protocol 冻结。 |

### A.4 复验命令

[cmd-r552-status]

```bash
PYTHONPATH=project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/conversion/src:project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/representation/src:project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/readiness_audit/src \
python -m paper_stm_repair_smoke.cli validate
python - <<'PY'
import json, collections
from pathlib import Path
base = Path('project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/readiness_audit/llms_emp_profile')
rows = [json.loads(l) for l in (base/'llms_emp_case_matrix.jsonl').read_text(encoding='utf-8').splitlines() if l.strip()]
print(collections.Counter(r['conversion_status'] for r in rows))
for pid in ['llms_emp_stm_results_0018','llms_emp_stm_results_0028','llms_emp_stm_results_0037']:
    print(pid, next(r for r in rows if r['raw_pair_id'] == pid)['conversion_status'])
PY
```

[cmd-r552-no-regression]

```bash
git show origin/paper1/r5.5-llms-emp-deep-profile:project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/readiness_audit/llms_emp_profile/llms_emp_case_matrix.jsonl > /tmp/r5_5_llms_emp_case_matrix.baseline.jsonl
python - <<'PY'
import json
from pathlib import Path
from collections import Counter
base_path = Path('/tmp/r5_5_llms_emp_case_matrix.baseline.jsonl')
new_path = Path('project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/readiness_audit/llms_emp_profile/llms_emp_case_matrix.jsonl')
target = {'llms_emp_stm_results_0018', 'llms_emp_stm_results_0028', 'llms_emp_stm_results_0037'}
rank = {'converted': 0, 'partial': 1, 'blocked': 2}
base = {json.loads(line)['raw_pair_id']: json.loads(line) for line in base_path.read_text(encoding='utf-8').splitlines() if line.strip()}
new = {json.loads(line)['raw_pair_id']: json.loads(line) for line in new_path.read_text(encoding='utf-8').splitlines() if line.strip()}
assert len(base) == 60 and len(new) == 60
assert set(base) == set(new)
assert {pid for pid, row in base.items() if row['conversion_status'] == 'blocked'} == target
for pid, old in base.items():
    cur = new[pid]
    for key in ['nl_sha256', 'stm0_sha256', 'source_sha256', 'nl_source_locator', 'stm_source_locator']:
        assert old.get(key) == cur.get(key), (pid, key)
    if pid not in target:
        assert rank[cur['conversion_status']] <= rank[old['conversion_status']], (pid, old['conversion_status'], cur['conversion_status'])
for pid in target:
    assert new[pid]['conversion_status'] == 'partial'
print('baseline:', Counter(row['conversion_status'] for row in base.values()))
print('current:', Counter(row['conversion_status'] for row in new.values()))
PY
```

[cmd-r552-recovery]

```bash
export PLANTUML_JAR=/path/to/plantuml.jar  # 本次实测使用本机 bundled PlantUML jar；新环境需按 README/GUIDE 配置。
PYTHONPATH=project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/conversion/src \
python -m paper_stm_repair_conversion.cli recover-plantuml \
  --reports-dir project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/conversion/reports \
  --run-dir project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/conversion/artifacts/plantuml_recovery/r3_1_committed/workdir \
  --archive-dir project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/conversion/artifacts/plantuml_recovery/r3_1_committed \
  --run-id r5.5.2-plantuml-blocked-recovery \
  --created-at 2026-06-29T21:14:14+08:00
```

[cmd-r552-snippets]

```bash
PYTHONPATH=project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/conversion/src:project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/representation/src \
python - <<'PY'
import json, zipfile, tempfile
from pathlib import Path
from paper_stm_repair_conversion.adapters.scxml import convert_scxml, ScxmlOptions
from paper_stm_repair_representation.lowering import FCSTMExporter
root = Path('project_1_llm_state_machine_modeling/paper_stm_repair')
pairs = {json.loads(l)['pair_id']: json.loads(l) for l in (root/'corpora/seed_library/llms-emp-stm-subset/assets/extracted/pairs.jsonl').read_text(encoding='utf-8').splitlines() if l.strip()}
case_rows = {json.loads(l)['raw_pair_id']: json.loads(l) for l in (root/'pipeline/readiness_audit/llms_emp_profile/llms_emp_case_matrix.jsonl').read_text(encoding='utf-8').splitlines() if l.strip()}
recovery = json.loads((root/'pipeline/conversion/reports/plantuml_recovery_report.json').read_text(encoding='utf-8'))
items = {i['pair_id']: i for i in recovery['items'] if i.get('seed_id') == 'llms-emp-stm-subset'}
zip_path = Path(recovery['artifact_archive']['archive_path'])
for pid in ['llms_emp_stm_results_0001','llms_emp_stm_results_0000','llms_emp_stm_results_0018','llms_emp_stm_results_0028','llms_emp_stm_results_0037','llms_emp_stm_results_0039','llms_emp_stm_results_0045']:
    item = items[pid]
    preflight = item.get('raw_preflight') if item.get('raw_conversion_pass') else item.get('normalized_preflight')
    member = preflight['structured_export_path']
    source = 'official_scxml_raw' if item.get('raw_conversion_pass') else 'official_scxml_r3_1_normalized_replay'
    with tempfile.TemporaryDirectory() as td:
        scxml = Path(td) / f'{pid}.scxml'
        with zipfile.ZipFile(zip_path) as zf:
            scxml.write_bytes(zf.read(member))
        result = convert_scxml(
            scxml,
            example_id=pid,
            seed_id='llms-emp-stm-subset',
            options=ScxmlOptions(
                adapter='plantuml', source_format='plantuml', conversion_source='official_scxml',
                canonical_extraction_method=f'report snippet replay {source}', status_on_success='converted',
                fallback_used=False, fallback_scope=None, timing_level='none', source_language='PlantUML state diagram'),
            structured_export_relpath=member,
            structured_export_sha256=preflight.get('structured_export_sha256'),
        )
        exported = FCSTMExporter(result.to_canonical_dict()).export()
        readiness_status = case_rows[pid]['conversion_status']
        print(
            pid,
            pairs[pid]['source_locator'],
            source,
            'canonical_states/transitions=', f'{len(result.states)}/{len(result.transitions)}',
            'fcstm_loss_rows=', len(exported['loss_rows']),
            'readiness_status=', readiness_status,
            'exporter_internal_status=', exported['status'],
        )
PY
```
