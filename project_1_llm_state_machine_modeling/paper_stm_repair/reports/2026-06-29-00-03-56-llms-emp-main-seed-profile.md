# R5.5 `llms-emp-stm-subset` main seed profile

## 事实源与复验 / 来源考据

| source path | source creation commit | prefix commit | substantive fact commit 判定理由 | non-prefix revision/migration commit | canonical machine source |
|---|---|---|---|---|---|
| `pipeline/readiness_audit/llms_emp_profile/llms_emp_deep_profile.md` | `ee35e444` (2026-06-28 22:54:39 +0800) | N/A：source 在旧 smoke 前缀冻结后创建，未经历早期路径 prefix move。 | `49f34c39` (2026-06-29 00:03:56 +0800)：补齐 10 cluster 指标表、10×6 LLM 状态矩阵与行为特征矩阵；这是当前主 seed profile 的事实快照。 | 本报告所在的 R5.5.1 migration commit（同一提交内无法自嵌最终 SHA；精确提交用 `git log --follow -- <report>` 复核）；仅迁移 human-facing report 与改写入口，不改 canonical machine facts。 | [llms_emp_case_matrix.jsonl](../pipeline/readiness_audit/llms_emp_profile/llms_emp_case_matrix.jsonl)；[llms_emp_cluster_profiles.jsonl](../pipeline/readiness_audit/llms_emp_profile/llms_emp_cluster_profiles.jsonl)；[llms_emp_cluster_llm_matrix.jsonl](../pipeline/readiness_audit/llms_emp_profile/llms_emp_cluster_llm_matrix.jsonl)；[llms_emp_partial_attribution_ledger.jsonl](../pipeline/readiness_audit/llms_emp_profile/llms_emp_partial_attribution_ledger.jsonl)；[llms_emp_blocked_probe.jsonl](../pipeline/readiness_audit/llms_emp_profile/llms_emp_blocked_probe.jsonl) |

> 本节是本 report 的事实绑定入口：Markdown 只做人类阅读与论文写作 handoff，不替代 canonical JSON/JSONL/ZIP/committed run artifacts。复验时优先回到最后一列机器事实源。

## R5.5 `llms-emp-stm-subset` 主 seed 池深度画像

本 report 迁移自 R5.5 `run-llms-emp-profile` 生成的旧 human summary；当前机器事实源是 [llms_emp_case_matrix.jsonl](../pipeline/readiness_audit/llms_emp_profile/llms_emp_case_matrix.jsonl)、[llms_emp_cluster_profiles.jsonl](../pipeline/readiness_audit/llms_emp_profile/llms_emp_cluster_profiles.jsonl)、[llms_emp_cluster_llm_matrix.jsonl](../pipeline/readiness_audit/llms_emp_profile/llms_emp_cluster_llm_matrix.jsonl) 与 [llms_emp_partial_attribution_ledger.jsonl](../pipeline/readiness_audit/llms_emp_profile/llms_emp_partial_attribution_ledger.jsonl)。本 Markdown 只做人类阅读入口。

### 1. 结论

`llms-emp-stm-subset` 仍是 R6/R7 的主 seed 池，但应按 **proceed_with_supplementary** 口径进入后续阶段：主线可围绕 T0/T0.5 离散状态机族展开；Digital Camera cluster 带显式秒级执行时间与复杂 pseudo-state，应进入 supplementary / stress；3 个 blocked 样例进入 negative evidence / converter follow-up。

关键纪律：60 个 raw pair 是 10 个唯一 NL × 6 个 LLM 输出，不得在论文中写成 60 个独立需求；conversion / normalization / `.fcstm` lowering 均不得计入 repair gain。

#### 1.1 十个 NL cluster 的完整结论表

本表是远程快速决策入口：每行是一条唯一 NL，而不是单个 LLM 输出；`6 个 LLM 输出状态` 按该 NL 对应的 GPT-4o / GPT-4 / Llama / Kimi / DeepSeek / Claude 六个生成结果汇总。

| # | NL / seed | 来源 | 控制语义 | 时间等级 | 结构族 | 行为特征 | 6 个 LLM 输出状态 | story 角色 | 主要风险 / 结论 |
|---:|---|---|---|---|---|---|---|---|---|
| 0 | `llms_emp_nl_00_hldcs_high_level_driving_module`<br>high-level driving module | HLDCS | 自动驾驶模式控制 | `T0` | `HSM` | 守卫式条件、动作/entry-exit、变量/数据条件、层级、伪状态 | 🟡6 | `main_candidate` | 条件标签仍作事件；需 R3.1 规范化回放；层级 lowering caveat |
| 1 | `llms_emp_nl_01_hstbs_state_machine_diagram_of_the_base`<br>State machine diagram of the base brake subsystem | HSTBS | 制动子系统控制 | `T0` | `FSM` | 守卫式条件、动作/entry-exit、伪状态 | 🟢4 / 🟡2 | `main_candidate` | 需 R3.1 规范化回放 |
| 2 | `llms_emp_nl_02_real_time_softwa_pump_control_state_machine`<br>Pump Control state machine | Real-Time Software Design for Embedded Systems | 泵子系统模式控制 | `T0` | `HSM` | 守卫式条件、层级 | 🟢3 / 🟡3 | `main_candidate` | 需 R3.1 规范化回放；层级 lowering caveat |
| 3 | `llms_emp_nl_03_hsuv_hybrid_sport_utility_vehicle_hsuv`<br>Hybrid Sport Utility Vehicle, HSUV | HSUV | 车辆运行模式控制 | `T0` | `HSM` | 守卫式条件、动作/entry-exit、层级 | 🟢3 / 🟡3 | `main_candidate` | 需 R3.1 规范化回放 |
| 4 | `llms_emp_nl_04_real_time_softwa_state_machine_for_train_control`<br>state machine for Train Control | Real-Time Software Design for Embedded Systems | 列车运动控制 | `T0` | `HSM` | 守卫式条件、动作/entry-exit、层级 | 🟢1 / 🟡5 | `main_candidate` | 需 R3.1 规范化回放；层级 lowering caveat |
| 5 | `llms_emp_nl_05_mocv_microwave_oven_control_with_entry`<br>Microwave Oven Control with entry and exit actions | MOCV | 微波炉控制：timer-like caveat | `T0.5` | `UML-SysML statechart` | 守卫式条件、动作/entry-exit、变量/数据条件、显式时间 | 🟢1 / 🟡5 | `main_candidate` | 需 R3.1 规范化回放；层级 lowering caveat |
| 6 | `llms_emp_nl_06_dscs_uav_swarm_state_machine_diagram`<br>UAV swarm state machine diagram | DSCS | 无人机群任务控制 | `T0` | `HSM` | 守卫式条件、动作/entry-exit、层级 | 🟢3 / 🟡3 | `main_candidate` | 需 R3.1 规范化回放；层级 lowering caveat |
| 7 | `llms_emp_nl_07_hldcs_collision_avoidance_sub_machine_st`<br>Collision avoidance sub-machine state diagram | HLDCS | 碰撞规避模式控制 | `T0` | `UML-SysML statechart` | 守卫式条件、层级、并发/区域 | 🟢1 / 🟡4 / 🔴1 | `main_candidate` | 需 R3.1 规范化回放；跨层级迁移表示损失；官方 SCXML 不可得；层级 lowering caveat |
| 8 | `llms_emp_nl_08_dcs_digital_camera_state_machine_diagr`<br>Digital camera state machine diagrams | DCS | 相机控制：显式执行时间与伪状态压力样例 | `T1` | `UML-SysML statechart` | 守卫式条件、动作/entry-exit、变量/数据条件、层级、伪状态、并发/区域、显式时间 | 🟡4 / 🔴2 | `supplementary_stress` | 条件标签仍作事件；需 R3.1 规范化回放；跨层级迁移表示损失；官方 SCXML 不可得；层级 lowering caveat |
| 9 | `llms_emp_nl_09_hldcs_autonomous_mode`<br>autonomous mode | HLDCS | 自动驾驶模式控制 | `T0` | `HSM` | 守卫式条件、动作/entry-exit、变量/数据条件、层级、伪状态 | 🟡6 | `main_candidate` | 条件标签仍作事件；需 R3.1 规范化回放；跨层级迁移表示损失；层级 lowering caveat |

#### 1.2 十个 NL × 六个 LLM 输出状态矩阵

本矩阵用于定位具体 raw pair。四位编号是 `llms_emp_stm_results_XXXX` 的后缀；完整 row 级事实见 [llms_emp_case_matrix.jsonl](../pipeline/readiness_audit/llms_emp_profile/llms_emp_case_matrix.jsonl)。

| # | NL / seed | GPT-4o | GPT-4 | Llama | Kimi | DeepSeek | Claude |
|---:|---|---|---|---|---|---|---|
| 0 | high-level driving module | 🟡 `0000` | 🟡 `0010` | 🟡 `0020` | 🟡 `0030` | 🟡 `0040` | 🟡 `0050` |
| 1 | State machine diagram of the base brake subsystem | 🟢 `0001` | 🟢 `0011` | 🟡 `0021` | 🟢 `0031` | 🟡 `0041` | 🟢 `0051` |
| 2 | Pump Control state machine | 🟢 `0002` | 🟢 `0013` | 🟡 `0023` | 🟡 `0033` | 🟡 `0043` | 🟢 `0053` |
| 3 | Hybrid Sport Utility Vehicle, HSUV | 🟢 `0003` | 🟢 `0012` | 🟡 `0022` | 🟡 `0032` | 🟡 `0042` | 🟢 `0052` |
| 4 | state machine for Train Control | 🟡 `0004` | 🟡 `0014` | 🟡 `0024` | 🟡 `0034` | 🟡 `0044` | 🟢 `0054` |
| 5 | Microwave Oven Control with entry and exit actions | 🟡 `0005` | 🟡 `0015` | 🟡 `0025` | 🟡 `0035` | 🟡 `0045` | 🟢 `0055` |
| 6 | UAV swarm state machine diagram | 🟢 `0006` | 🟡 `0016` | 🟡 `0026` | 🟢 `0036` | 🟡 `0046` | 🟢 `0056` |
| 7 | Collision avoidance sub-machine state diagram | 🟢 `0007` | 🟡 `0017` | 🟡 `0027` | 🔴 `0037` | 🟡 `0047` | 🟡 `0057` |
| 8 | Digital camera state machine diagrams | 🟡 `0008` | 🔴 `0018` | 🔴 `0028` | 🟡 `0038` | 🟡 `0048` | 🟡 `0058` |
| 9 | autonomous mode | 🟡 `0009` | 🟡 `0019` | 🟡 `0029` | 🟡 `0039` | 🟡 `0049` | 🟡 `0059` |

#### 1.3 十个 NL 的行为特征矩阵

这些特征只表示 R5.5 对 NL 与原始 STM_0 的保守画像，不等于 R5.7 已确认 repair target。

| # | NL / seed | 守卫式条件 | 动作/entry-exit | 变量/数据条件 | 层级 | 伪状态 | 并发/区域 | 显式时间 |
|---:|---|---|---|---|---|---|---|---|
| 0 | high-level driving module | ✅ | ✅ | ✅ | ✅ | ✅ | — | — |
| 1 | State machine diagram of the base brake subsystem | ✅ | ✅ | — | — | ✅ | — | — |
| 2 | Pump Control state machine | ✅ | — | — | ✅ | — | — | — |
| 3 | Hybrid Sport Utility Vehicle, HSUV | ✅ | ✅ | — | ✅ | — | — | — |
| 4 | state machine for Train Control | ✅ | ✅ | — | ✅ | — | — | — |
| 5 | Microwave Oven Control with entry and exit actions | ✅ | ✅ | ✅ | — | — | — | ✅ |
| 6 | UAV swarm state machine diagram | ✅ | ✅ | — | ✅ | — | — | — |
| 7 | Collision avoidance sub-machine state diagram | ✅ | — | — | ✅ | — | ✅ | — |
| 8 | Digital camera state machine diagrams | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| 9 | autonomous mode | ✅ | ✅ | ✅ | ✅ | ✅ | — | — |

### 2. 总体统计

| conversion_status | pairs |
|---|---:|
| `blocked` | 3 |
| `converted` | 16 |
| `partial` | 41 |

#### 2.1 时间等级

| time_level | pairs |
|---|---:|
| `T0` | 48 |
| `T0.5` | 6 |
| `T1` | 6 |

#### 2.2 结构家族

| structure_family | pairs |
|---|---:|
| `FSM` | 6 |
| `HSM` | 36 |
| `UML-SysML statechart` | 18 |

#### 2.3 R5.6 story role

| r5_6_story_role | pairs |
|---|---:|
| `main_candidate` | 53 |
| `negative_evidence` | 3 |
| `supplementary_stress` | 4 |

#### 2.4 cluster 口径 story role

| r5_6_story_role | clusters |
|---|---:|
| `main_candidate` | 9 |
| `supplementary_stress` | 1 |

#### 2.5 行为特征画像

本节是 R5.5 的保守 feature census，只支撑 R5.6 scope 决策；不能直接把某个特征计为 R5.7 已确认 repair target。

| feature | clusters |
|---|---:|
| `has_action_or_entry_exit` | 8 |
| `has_concurrency_or_regions` | 2 |
| `has_explicit_time` | 2 |
| `has_guard_like_condition` | 10 |
| `has_hierarchy` | 8 |
| `has_pseudostate` | 4 |
| `has_variables_or_data_conditions` | 4 |

#### 2.6 loss code

| loss code | count |
|---|---:|
| `R45.LOSS.composite_target_lowered_to_initial_child` | 6 |
| `R45.LOSS.condition_like_label_lowered_as_event` | 16 |
| `R45.LOSS.cross_scope_transition_unrepresentable` | 5 |
| `R45.LOSS.initial_inferred_from_source_order_or_start_state` | 12 |
| `R45.LOSS.source_lifted_to_composite_boundary` | 12 |
| `R45.LOSS.target_lifted_to_composite_boundary` | 8 |
| `R5.LOSS.official_scxml_unavailable` | 3 |
| `R5.LOSS.r3_1_normalization_replay_not_repair` | 24 |

### 3. cluster × LLM 交叉矩阵

符号：🟢 = converted；🟡 = partial；🔴 = blocked。emoji 列只编码状态，具体含义见本段。

| cluster | 模型 / 来源 | time | family | GPT-4o | GPT-4 | Llama | Kimi | DeepSeek | Claude |
|---|---|---|---|---|---|---|---|---|---|
| `llms_emp_nl_00_hldcs_high_level_driving_module` | high-level driving module / HLDCS | `T0` | `HSM` | 🟡 `0000` | 🟡 `0010` | 🟡 `0020` | 🟡 `0030` | 🟡 `0040` | 🟡 `0050` |
| `llms_emp_nl_01_hstbs_state_machine_diagram_of_the_base` | State machine diagram of the base brake subsystem / HSTBS | `T0` | `FSM` | 🟢 `0001` | 🟢 `0011` | 🟡 `0021` | 🟢 `0031` | 🟡 `0041` | 🟢 `0051` |
| `llms_emp_nl_02_real_time_softwa_pump_control_state_machine` | Pump Control state machine / Real-Time Software Design for Embedded Systems | `T0` | `HSM` | 🟢 `0002` | 🟢 `0013` | 🟡 `0023` | 🟡 `0033` | 🟡 `0043` | 🟢 `0053` |
| `llms_emp_nl_03_hsuv_hybrid_sport_utility_vehicle_hsuv` | Hybrid Sport Utility Vehicle, HSUV / HSUV | `T0` | `HSM` | 🟢 `0003` | 🟢 `0012` | 🟡 `0022` | 🟡 `0032` | 🟡 `0042` | 🟢 `0052` |
| `llms_emp_nl_04_real_time_softwa_state_machine_for_train_control` | state machine for Train Control / Real-Time Software Design for Embedded Systems | `T0` | `HSM` | 🟡 `0004` | 🟡 `0014` | 🟡 `0024` | 🟡 `0034` | 🟡 `0044` | 🟢 `0054` |
| `llms_emp_nl_05_mocv_microwave_oven_control_with_entry` | Microwave Oven Control with entry and exit actions / MOCV | `T0.5` | `UML-SysML statechart` | 🟡 `0005` | 🟡 `0015` | 🟡 `0025` | 🟡 `0035` | 🟡 `0045` | 🟢 `0055` |
| `llms_emp_nl_06_dscs_uav_swarm_state_machine_diagram` | UAV swarm state machine diagram / DSCS | `T0` | `HSM` | 🟢 `0006` | 🟡 `0016` | 🟡 `0026` | 🟢 `0036` | 🟡 `0046` | 🟢 `0056` |
| `llms_emp_nl_07_hldcs_collision_avoidance_sub_machine_st` | Collision avoidance sub-machine state diagram / HLDCS | `T0` | `UML-SysML statechart` | 🟢 `0007` | 🟡 `0017` | 🟡 `0027` | 🔴 `0037` | 🟡 `0047` | 🟡 `0057` |
| `llms_emp_nl_08_dcs_digital_camera_state_machine_diagr` | Digital camera state machine diagrams / DCS | `T1` | `UML-SysML statechart` | 🟡 `0008` | 🔴 `0018` | 🔴 `0028` | 🟡 `0038` | 🟡 `0048` | 🟡 `0058` |
| `llms_emp_nl_09_hldcs_autonomous_mode` | autonomous mode / HLDCS | `T0` | `HSM` | 🟡 `0009` | 🟡 `0019` | 🟡 `0029` | 🟡 `0039` | 🟡 `0049` | 🟡 `0059` |

### 4. LLM 维度状态

| LLM | converted | partial | blocked |
|---|---:|---:|---:|
| `gpt-4o` | 5 | 5 | 0 |
| `gpt-4` | 3 | 6 | 1 |
| `llama` | 0 | 9 | 1 |
| `kimi` | 2 | 7 | 1 |
| `deepseek` | 0 | 10 | 0 |
| `claude` | 6 | 4 | 0 |

### 5. cluster 画像

| cluster | role | 控制语义 | 行为特征 | time note | 状态分布 | 主要 loss |
|---|---|---|---|---|---|---|
| `llms_emp_nl_00_hldcs_high_level_driving_module` | `main_candidate` | 自动驾驶模式控制 | `has_guard_like_condition`, `has_action_or_entry_exit`, `has_variables_or_data_conditions`, `has_hierarchy`, `has_pseudostate` | 距离/模式条件是离散守卫式线索；无显式 clock。 | {'partial': 6} | `R45.LOSS.composite_target_lowered_to_initial_child`×1, `R45.LOSS.condition_like_label_lowered_as_event`×6, `R45.LOSS.source_lifted_to_composite_boundary`×2, `R5.LOSS.r3_1_normalization_replay_not_repair`×2 |
| `llms_emp_nl_01_hstbs_state_machine_diagram_of_the_base` | `main_candidate` | 制动子系统控制 | `has_guard_like_condition`, `has_action_or_entry_exit`, `has_pseudostate` | “after entering”等顺序短语是 ordering cue，不是 clock 约束。 | {'converted': 4, 'partial': 2} | `R5.LOSS.r3_1_normalization_replay_not_repair`×2 |
| `llms_emp_nl_02_real_time_softwa_pump_control_state_machine` | `main_candidate` | 泵子系统模式控制 | `has_guard_like_condition`, `has_hierarchy` | 离散模式/状态切换；无显式 timing。 | {'converted': 3, 'partial': 3} | `R45.LOSS.initial_inferred_from_source_order_or_start_state`×1, `R5.LOSS.r3_1_normalization_replay_not_repair`×3 |
| `llms_emp_nl_03_hsuv_hybrid_sport_utility_vehicle_hsuv` | `main_candidate` | 车辆运行模式控制 | `has_guard_like_condition`, `has_action_or_entry_exit`, `has_hierarchy` | 用户/动作驱动的离散模式切换；无显式 timing。 | {'converted': 3, 'partial': 3} | `R5.LOSS.r3_1_normalization_replay_not_repair`×3 |
| `llms_emp_nl_04_real_time_softwa_state_machine_for_train_control` | `main_candidate` | 列车运动控制 | `has_guard_like_condition`, `has_action_or_entry_exit`, `has_hierarchy` | 存在 entry/action-like 标签，但无 clock/duration 语义。 | {'converted': 1, 'partial': 5} | `R45.LOSS.composite_target_lowered_to_initial_child`×2, `R45.LOSS.initial_inferred_from_source_order_or_start_state`×3, `R45.LOSS.target_lifted_to_composite_boundary`×1, `R5.LOSS.r3_1_normalization_replay_not_repair`×4 |
| `llms_emp_nl_05_mocv_microwave_oven_control_with_entry` | `main_candidate` | 微波炉控制：timer-like caveat | `has_guard_like_condition`, `has_action_or_entry_exit`, `has_variables_or_data_conditions`, `has_explicit_time` | NL 提到 cooking time 与 timer expires，但没有形式化 clock 语义；本阶段按 T0.5 timer-like caveat 处理。 | {'converted': 1, 'partial': 5} | `R45.LOSS.composite_target_lowered_to_initial_child`×2, `R45.LOSS.initial_inferred_from_source_order_or_start_state`×1, `R45.LOSS.source_lifted_to_composite_boundary`×3, `R45.LOSS.target_lifted_to_composite_boundary`×1, `R5.LOSS.r3_1_normalization_replay_not_repair`×3 |
| `llms_emp_nl_06_dscs_uav_swarm_state_machine_diagram` | `main_candidate` | 无人机群任务控制 | `has_guard_like_condition`, `has_action_or_entry_exit`, `has_hierarchy` | 离散任务状态迁移；无显式 timing。 | {'converted': 3, 'partial': 3} | `R45.LOSS.source_lifted_to_composite_boundary`×1, `R5.LOSS.r3_1_normalization_replay_not_repair`×2 |
| `llms_emp_nl_07_hldcs_collision_avoidance_sub_machine_st` | `main_candidate` | 碰撞规避模式控制 | `has_guard_like_condition`, `has_hierarchy`, `has_concurrency_or_regions` | 无显式 clock / duration；主要 caveat 是并发/正交区域语义。 | {'blocked': 1, 'converted': 1, 'partial': 4} | `R45.LOSS.cross_scope_transition_unrepresentable`×1, `R45.LOSS.initial_inferred_from_source_order_or_start_state`×3, `R45.LOSS.source_lifted_to_composite_boundary`×2, `R45.LOSS.target_lifted_to_composite_boundary`×1, `R5.LOSS.official_scxml_unavailable`×1, `R5.LOSS.r3_1_normalization_replay_not_repair`×2 |
| `llms_emp_nl_08_dcs_digital_camera_state_machine_diagr` | `supplementary_stress` | 相机控制：显式执行时间与伪状态压力样例 | `has_guard_like_condition`, `has_action_or_entry_exit`, `has_variables_or_data_conditions`, `has_hierarchy`, `has_pseudostate`, `has_explicit_time`, `has_concurrency_or_regions` | NL 含秒级执行时间、fork/join 与概率/守卫式线索；不能作为 T0 主结论证据。 | {'blocked': 2, 'partial': 4} | `R45.LOSS.composite_target_lowered_to_initial_child`×1, `R45.LOSS.condition_like_label_lowered_as_event`×4, `R45.LOSS.cross_scope_transition_unrepresentable`×2, `R45.LOSS.initial_inferred_from_source_order_or_start_state`×2, `R45.LOSS.source_lifted_to_composite_boundary`×3, `R45.LOSS.target_lifted_to_composite_boundary`×2, `R5.LOSS.official_scxml_unavailable`×2, `R5.LOSS.r3_1_normalization_replay_not_repair`×2 |
| `llms_emp_nl_09_hldcs_autonomous_mode` | `main_candidate` | 自动驾驶模式控制 | `has_guard_like_condition`, `has_action_or_entry_exit`, `has_variables_or_data_conditions`, `has_hierarchy`, `has_pseudostate` | 距离/模式条件是离散守卫式线索；无显式 clock。 | {'partial': 6} | `R45.LOSS.condition_like_label_lowered_as_event`×6, `R45.LOSS.cross_scope_transition_unrepresentable`×2, `R45.LOSS.initial_inferred_from_source_order_or_start_state`×2, `R45.LOSS.source_lifted_to_composite_boundary`×1, `R45.LOSS.target_lifted_to_composite_boundary`×3, `R5.LOSS.r3_1_normalization_replay_not_repair`×1 |

### 6. partial 归因摘要

| primary_attribution | count |
|---|---:|
| `fcstm_lowering` | 6 |
| `pipeline_artifact` | 19 |
| `r5_7_candidate_only` | 16 |

`pipeline_artifact=True` 表示该症状在 conversion / canonicalization / lowering pipeline 中被观察或暴露；它不等价于“pipeline 是唯一根因”，也不排除 R5.7 逐例判定为 seed-side guard/event/action 缺陷。

### 7. loss code 到 R5.5 归因策略

本节把机器 ledger 中的 `loss_reason_codes` 显式映射到 R5.5 学术归因，避免后续把 conversion / normalization / lowering 收益误写成 repair loop 收益。该表是长期阅读入口；机器事实源仍以 [llms_emp_partial_attribution_ledger.jsonl](../pipeline/readiness_audit/llms_emp_profile/llms_emp_partial_attribution_ledger.jsonl) 与 R5 sweep archive 为准。

| loss code | 观察到的问题 | 来源阶段 | 主归因 | 次级归因 | pipeline artifact | R5.7候选 | 置信度 | R5.7纪律 |
|---|---|---|---|---|---|---|---|---|
| `R5.LOSS.official_scxml_unavailable` | official PlantUML SCXML export was unavailable after raw and normalized probes | `plantuml_toolchain` | `plantuml_toolchain` | `unknown` | `True` | `False` | `high` | blocked / negative evidence；优先做 converter follow-up，不归因给 repair loop。 |
| `R45.LOSS.condition_like_label_lowered_as_event` | condition-like transition label was preserved as an event label rather than a verified guard | `fcstm_lowering` | `r5_7_candidate_only` | `seed_defect`, `fcstm_lowering` | `True` | `True` | `medium` | 只进入 R5.7 候选；必须逐例回到 NL 与原始 PlantUML，不能自动把 event label 升级为 guard。 |
| `R5.LOSS.r3_1_normalization_replay_not_repair` | pre-SCXML normalization replay was required; this is conversion readiness, not repair gain | `plantuml_toolchain` | `pipeline_artifact` | `plantuml_toolchain` | `True` | `False` | `high` | 只说明 R3.1 预处理让 official SCXML 路径可走；不得计入 repair gain。 |
| `R45.LOSS.cross_scope_transition_unrepresentable` | cross-scope transition could not be represented without hierarchy approximation | `fcstm_lowering` | `fcstm_lowering` | `scxml_canonical` | `True` | `False` | `high` | 表示层级/边界 lowering 的可表示性损失；R5.7 只能把它作为表示 caveat 或协议约束处理。 |
| `R45.LOSS.source_lifted_to_composite_boundary` | source endpoint was lifted to a composite-state boundary during representation lowering | `fcstm_lowering` | `fcstm_lowering` | `scxml_canonical` | `True` | `False` | `high` | 表示层级/边界 lowering 的可表示性损失；R5.7 只能把它作为表示 caveat 或协议约束处理。 |
| `R45.LOSS.target_lifted_to_composite_boundary` | target endpoint was lifted to a composite-state boundary during representation lowering | `fcstm_lowering` | `fcstm_lowering` | `scxml_canonical` | `True` | `False` | `high` | 表示层级/边界 lowering 的可表示性损失；R5.7 只能把它作为表示 caveat 或协议约束处理。 |
| `R45.LOSS.composite_target_lowered_to_initial_child` | transition into a composite target was lowered to an initial child | `fcstm_lowering` | `fcstm_lowering` | `scxml_canonical` | `True` | `False` | `high` | 表示层级/边界 lowering 的可表示性损失；R5.7 只能把它作为表示 caveat 或协议约束处理。 |
| `R45.LOSS.initial_inferred_from_source_order_or_start_state` | initial child was inferred from source order or start-state convention | `fcstm_lowering` | `fcstm_lowering` | `pipeline_artifact` | `True` | `False` | `high` | 表示层级/边界 lowering 的可表示性损失；R5.7 只能把它作为表示 caveat 或协议约束处理。 |

### 8. blocked 摘要

| raw_pair_id | cluster | LLM | issue_category | renderability | 当前结论 |
|---|---|---|---|---|---|
| `llms_emp_stm_results_0018` | `llms_emp_nl_08_dcs_digital_camera_state_machine_diagr` | `gpt-4` | `F_unquoted_state_names_with_spaces` | `not_reproducible_from_committed_evidence` | raw 与 normalized PlantUML 均未获得可信 official SCXML；当前只能进入 negative evidence / converter follow-up。 |
| `llms_emp_stm_results_0028` | `llms_emp_nl_08_dcs_digital_camera_state_machine_diagr` | `llama` | `A_non_plantuml_stm_directive` | `not_reproducible_from_committed_evidence` | raw 与 normalized PlantUML 均未获得可信 official SCXML；当前只能进入 negative evidence / converter follow-up。 |
| `llms_emp_stm_results_0037` | `llms_emp_nl_07_hldcs_collision_avoidance_sub_machine_st` | `kimi` | `A_non_plantuml_stm_directive` | `not_reproducible_from_committed_evidence` | raw 与 normalized PlantUML 均未获得可信 official SCXML；当前只能进入 negative evidence / converter follow-up。 |

### 9. 给 R5.6/R5.7 的学术含义

1. 当前主线不宜声称覆盖 timed automata 或任意 UML；主实验应保守限定为 T0/T0.5 的离散 FSM/HSM/UML-SysML statechart artifacts。guard/action/data-condition 只作为 caveat 与 R5.7 候选画像，不作为已确认扩展状态机覆盖 claim。
2. `condition_like_label_lowered_as_event` 是最接近 R5.7 repair target 的候选问题，但必须逐例回到 NL 证据，不能把所有 event label 都自动升级为 guard。
3. `r3_1_normalization_replay`、scope lifting、initial inference 等主要是 conversion / representation attribution，不得写成 repair loop 改善。
4. Digital Camera cluster 可保留为 supplementary / stress，用于说明当前边界为什么不外推到显式时间状态机。
