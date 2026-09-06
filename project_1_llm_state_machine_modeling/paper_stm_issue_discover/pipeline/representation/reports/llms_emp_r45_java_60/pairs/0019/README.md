# Pair `0019`：NL + PlantUML STM0 + FCSTM STM0

[上一组 `0018`](../0018/README.md) | [返回 60 组索引](../../PAIR_INDEX.md) | [下一组 `0020`](../0020/README.md)

- LLM：`GPT-4`
- 模型/场景：autonomous mode
- 作者输出阶段：`Result with Semantic Checking`
- 作者输出单元格：`AE21`；Excel row：`21`
- Phase-I fallback：`false`
- 相对 Phase-I 是否变化：`true`
- Phase-I PlantUML SHA-256：`b4c24224cccc1a34efedeafd961ef2b4867aeb0701ce8f8a0ea78691a75c936d`
- NL SHA-256：`b7425c44960b36c3534f118279e347786d4074191efea7bf9a7c5ba032c9e82c`
- PlantUML SHA-256：`6bb3c5c655131a5921877cf44539d859f3dbd27faece819936ad118d48ba4836`
- FCSTM SHA-256：`de769acb086b889400ec92e710a5bafc2212798897a1c7f998e3eebba354c851`
- review subject SHA-256：`f2e2c0ef03b6ee07b4179206ee1527e8a8b4d9488cacfaa1b96403341a8e3c78`
- working contract SHA-256：`016c047647c2cd7dd83882ad580457a14c235806a3e4c8b0bdbcd0e89900e26f`
- 结构裁决：`structure_preserved`
- source states / transitions：`17` / `25`
- mapped / blocked / silent drop：`25` / `0` / `0`
- final / lifecycle / body coverage：`0/0` / `0/0` / `0/0`
- concurrent region / separator coverage：`0/0` / `0/0`
- source normalization coverage：`0/0`
- official raw / validation：`state_diagram` / `state_diagram`
- official identity states / transitions：`17` / `25`
- official identity remaps：state `0` / transition endpoint `0`
- AST audit：`passed`
- legacy whole-model FCSTM execution / Discover：`false` / `false`
- working bundle usage gate：`discover_input_with_capability_mask`
- ownership source / compiler / agent：`42` / `54` / `0`
- source macro / positive identity trace / conversion boundary trace：`25` / `42` / `0`
- capability source-static / simulation / transition-trace：`eligible_with_exclusions` / `eligible_with_exclusions` / `eligible_with_exclusions`
- compiler-only diagnostic policy：`rejected_conversion_artifact`；main-result conversion artifact limit：`0`
- 主 session 对读：`pass`；ownership/macro/capability 均为 `pass`；Case 0019 passes the current attribution-safe forward review; this does not assert global behavior equivalence, and unsupported runtime semantics remain fail-closed. Amendment record: the substantive subject review remains the one recorded in review_context (first reviewed 2026-07-20T05:44:08Z by gpt-5.5 (session omx-1784393668980-pxpj3q), and it still binds because review_subject_sha256 is unchanged. A scoped re-check was performed 2026-08-17 by claude-opus-5 (main-session LLM, PR #185) because commit bbb04cb1 (2026-07-27) regenerated the 60 working contracts and commit 35eba126 (2026-08-11) renamed the paper workspace, and neither refreshed this registry. The re-review is scoped: a key-by-key diff shows the only contract changes are capability_eligibility.simulation, capability_eligibility.transition_trace and summary.simulation_status (bbb04cb1) plus the four artifact_bindings path strings (35eba126); the remaining 168 keys and the whole of canonical/fcstm/parse_inspect/source_traces are byte-identical, so review_subject_sha256 is unchanged and the original ownership, macro and correspondence findings still stand. The capability block was re-checked against seven invariants: eligible ids are source: only, excluded ids cover the compiler-owned set, the two sets are disjoint, claim_boundary and reason_codes are non-empty, main_result_conversion_artifact_limit is still 0, and usage_gate is unchanged.
- source anchors：`source-ref:llms_emp_feedback_final_0019.puml:line:3\|state AutonomousMode {, source-ref:llms_emp_feedback_final_0019.puml:line:7\|InitialState --> HighwayMode: high_way=true`；FCSTM anchors：`element-ref:source:state:AutonomousMode@line:17\|state AutonomousMode named "AutonomousMode" {, element-ref:compiler:transition_segment:tr_0003:segment:1@line:64\|InitialState -> HighwayMode : /high_way_true;`
- 三个原始文件：[NL](./nl.txt) | [PlantUML](./plantuml.puml) | [FCSTM](./fcstm.fcstm)
- 审计入口：[canonical](../../canonical/llms_emp_feedback_final_0019.json) | [冻结 FCSTM](../../fcstm/llms_emp_feedback_final_0019.fcstm) | [case report](../../case_reports/llms_emp_feedback_final_0019.json) | [working contract](../../working_contracts/llms_emp_feedback_final_0019.json) | [source trace](../../source_traces/llms_emp_feedback_final_0019.json) | [人工总账](../../MANUAL_REVIEW.md)

## 主 session 三方语义对应

| projection | assessment | NL anchor | PlantUML anchor | FCSTM anchor | source roots | compiler members | rationale |
|---|---|---|---|---|---|---|---|
| `direct` | `preserved` | AutonomousMode | source-ref:llms_emp_feedback_final_0019.puml:line:3\|state AutonomousMode { | element-ref:source:state:AutonomousMode@line:17\|state AutonomousMode named "AutonomousMode" { | source:state:AutonomousMode | - | Case 0019 binds source:state:AutonomousMode to authored PlantUML occurrence 'state AutonomousMode {' and current FCSTM occurrence 'state AutonomousMode named "AutonomousMode" {'; the source semantic root remains attributable while any compiler-owned projection stays protected and cannot become an independent Repair target. |
| `macro` | `preserved_with_exclusions` | high_way=true | source-ref:llms_emp_feedback_final_0019.puml:line:7\|InitialState --> HighwayMode: high_way=true | element-ref:compiler:transition_segment:tr_0003:segment:1@line:64\|InitialState -> HighwayMode : /high_way_true; | source:transition:tr_0003 | compiler:transition_segment:tr_0003:segment:1 | Case 0019 binds source:transition:tr_0003 to authored PlantUML occurrence 'InitialState --> HighwayMode: high_way=true' and current FCSTM occurrence 'InitialState -> HighwayMode : /high_way_true;'; the source semantic root remains attributable while any compiler-owned projection stays protected and cannot become an independent Repair target. |

## Risk occurrence 第二遍复核

| obligation | risk tag | assessment | PlantUML evidence | FCSTM evidence | ownership evidence | rationale |
|---|---|---|---|---|---|---|
| `review:multi_segment_macro:0001:tr_0012` | `multi_segment_macro` | `compiler_artifact_excluded` | source-ref:llms_emp_feedback_final_0019.puml:line:21\|ExitHighway --> FinishState: auto_finished=true, source-ref:llms_emp_feedback_final_0019.puml:line:35\|exit_urban --> FinishState: auto_finished=true, source-ref:llms_emp_feedback_final_0019.puml:line:37\|HighwayMode --> UrbanMode: urban_way=true, source-ref:llms_emp_feedback_final_0019.puml:line:38\|UrbanMode --> HighwayMode: high_way=true | element-ref:compiler:route_control:R45RouteToken@line:1\|def int R45RouteToken = 0;, element-ref:compiler:transition_segment:tr_0012:segment:1@line:30\|ExitHighway -> [*] : /auto_finished_true effect { R45RouteToken = 12; };, element-ref:compiler:transition_segment:tr_0012:segment:2@line:59\|HighwayMode -> FinishState : if [R45RouteToken == 12] effect { R45RouteToken = 0; }; | compiler:route_control:R45RouteToken, compiler:transition_segment:tr_0012:segment:1, compiler:transition_segment:tr_0012:segment:2, source:transition:tr_0012 | Case 0019 multi_segment_macro occurrence review:multi_segment_macro:0001:tr_0012 binds exact source refs to working-contract elements compiler:route_control:R45RouteToken, compiler:transition_segment:tr_0012:segment:1, compiler:transition_segment:tr_0012:segment:2, source:transition:tr_0012. All emitted segments collapse to one source transition root; no segment is promoted as a separate authored transition or editable issue target. |
| `review:route_controller:0002:tr_0012` | `route_controller` | `compiler_artifact_excluded` | source-ref:llms_emp_feedback_final_0019.puml:line:21\|ExitHighway --> FinishState: auto_finished=true, source-ref:llms_emp_feedback_final_0019.puml:line:35\|exit_urban --> FinishState: auto_finished=true, source-ref:llms_emp_feedback_final_0019.puml:line:37\|HighwayMode --> UrbanMode: urban_way=true, source-ref:llms_emp_feedback_final_0019.puml:line:38\|UrbanMode --> HighwayMode: high_way=true | element-ref:compiler:route_control:R45RouteToken@line:1\|def int R45RouteToken = 0;, element-ref:compiler:transition_segment:tr_0012:segment:1@line:30\|ExitHighway -> [*] : /auto_finished_true effect { R45RouteToken = 12; };, element-ref:compiler:transition_segment:tr_0012:segment:2@line:59\|HighwayMode -> FinishState : if [R45RouteToken == 12] effect { R45RouteToken = 0; }; | compiler:route_control:R45RouteToken, compiler:transition_segment:tr_0012:segment:1, compiler:transition_segment:tr_0012:segment:2, source:transition:tr_0012 | Case 0019 route_controller occurrence review:route_controller:0002:tr_0012 binds exact source refs to working-contract elements compiler:route_control:R45RouteToken, compiler:transition_segment:tr_0012:segment:1, compiler:transition_segment:tr_0012:segment:2, source:transition:tr_0012. R45RouteToken and routed segments remain compiler_owned, protected, and excluded from confirmed issues, Repair, Confirm acceptance, and main results. |
| `review:multi_segment_macro:0003:tr_0021` | `multi_segment_macro` | `compiler_artifact_excluded` | source-ref:llms_emp_feedback_final_0019.puml:line:21\|ExitHighway --> FinishState: auto_finished=true, source-ref:llms_emp_feedback_final_0019.puml:line:35\|exit_urban --> FinishState: auto_finished=true, source-ref:llms_emp_feedback_final_0019.puml:line:37\|HighwayMode --> UrbanMode: urban_way=true, source-ref:llms_emp_feedback_final_0019.puml:line:38\|UrbanMode --> HighwayMode: high_way=true | element-ref:compiler:route_control:R45RouteToken@line:1\|def int R45RouteToken = 0;, element-ref:compiler:transition_segment:tr_0021:segment:1@line:50\|exit_urban -> [*] : /auto_finished_true effect { R45RouteToken = 21; };, element-ref:compiler:transition_segment:tr_0021:segment:2@line:60\|UrbanMode -> FinishState : if [R45RouteToken == 21] effect { R45RouteToken = 0; }; | compiler:route_control:R45RouteToken, compiler:transition_segment:tr_0021:segment:1, compiler:transition_segment:tr_0021:segment:2, source:transition:tr_0021 | Case 0019 multi_segment_macro occurrence review:multi_segment_macro:0003:tr_0021 binds exact source refs to working-contract elements compiler:route_control:R45RouteToken, compiler:transition_segment:tr_0021:segment:1, compiler:transition_segment:tr_0021:segment:2, source:transition:tr_0021. All emitted segments collapse to one source transition root; no segment is promoted as a separate authored transition or editable issue target. |
| `review:route_controller:0004:tr_0021` | `route_controller` | `compiler_artifact_excluded` | source-ref:llms_emp_feedback_final_0019.puml:line:21\|ExitHighway --> FinishState: auto_finished=true, source-ref:llms_emp_feedback_final_0019.puml:line:35\|exit_urban --> FinishState: auto_finished=true, source-ref:llms_emp_feedback_final_0019.puml:line:37\|HighwayMode --> UrbanMode: urban_way=true, source-ref:llms_emp_feedback_final_0019.puml:line:38\|UrbanMode --> HighwayMode: high_way=true | element-ref:compiler:route_control:R45RouteToken@line:1\|def int R45RouteToken = 0;, element-ref:compiler:transition_segment:tr_0021:segment:1@line:50\|exit_urban -> [*] : /auto_finished_true effect { R45RouteToken = 21; };, element-ref:compiler:transition_segment:tr_0021:segment:2@line:60\|UrbanMode -> FinishState : if [R45RouteToken == 21] effect { R45RouteToken = 0; }; | compiler:route_control:R45RouteToken, compiler:transition_segment:tr_0021:segment:1, compiler:transition_segment:tr_0021:segment:2, source:transition:tr_0021 | Case 0019 route_controller occurrence review:route_controller:0004:tr_0021 binds exact source refs to working-contract elements compiler:route_control:R45RouteToken, compiler:transition_segment:tr_0021:segment:1, compiler:transition_segment:tr_0021:segment:2, source:transition:tr_0021. R45RouteToken and routed segments remain compiler_owned, protected, and excluded from confirmed issues, Repair, Confirm acceptance, and main results. |
| `review:multi_segment_macro:0005:tr_0022` | `multi_segment_macro` | `compiler_artifact_excluded` | source-ref:llms_emp_feedback_final_0019.puml:line:21\|ExitHighway --> FinishState: auto_finished=true, source-ref:llms_emp_feedback_final_0019.puml:line:35\|exit_urban --> FinishState: auto_finished=true, source-ref:llms_emp_feedback_final_0019.puml:line:37\|HighwayMode --> UrbanMode: urban_way=true, source-ref:llms_emp_feedback_final_0019.puml:line:38\|UrbanMode --> HighwayMode: high_way=true | element-ref:compiler:route_control:R45RouteToken@line:1\|def int R45RouteToken = 0;, element-ref:compiler:transition_segment:tr_0022:segment:1@line:31\|enter_hwy -> [*] : /urban_way_true effect { R45RouteToken = 22; };, element-ref:compiler:transition_segment:tr_0022:segment:2@line:32\|cruise -> [*] : /urban_way_true effect { R45RouteToken = 22; };, element-ref:compiler:transition_segment:tr_0022:segment:3@line:33\|lane_change -> [*] : /urban_way_true effect { R45RouteToken = 22; };, element-ref:compiler:transition_segment:tr_0022:segment:4@line:34\|ExitHighway -> [*] : /urban_way_true effect { R45RouteToken = 22; };, element-ref:compiler:transition_segment:tr_0022:segment:5@line:61\|HighwayMode -> UrbanMode : if [R45RouteToken == 22] effect { R45RouteToken = 0; }; | compiler:route_control:R45RouteToken, compiler:transition_segment:tr_0022:segment:1, compiler:transition_segment:tr_0022:segment:2, compiler:transition_segment:tr_0022:segment:3, compiler:transition_segment:tr_0022:segment:4, compiler:transition_segment:tr_0022:segment:5, source:transition:tr_0022 | Case 0019 multi_segment_macro occurrence review:multi_segment_macro:0005:tr_0022 binds exact source refs to working-contract elements compiler:route_control:R45RouteToken, compiler:transition_segment:tr_0022:segment:1, compiler:transition_segment:tr_0022:segment:2, compiler:transition_segment:tr_0022:segment:3, compiler:transition_segment:tr_0022:segment:4, compiler:transition_segment:tr_0022:segment:5, source:transition:tr_0022. All emitted segments collapse to one source transition root; no segment is promoted as a separate authored transition or editable issue target. |
| `review:route_controller:0006:tr_0022` | `route_controller` | `compiler_artifact_excluded` | source-ref:llms_emp_feedback_final_0019.puml:line:21\|ExitHighway --> FinishState: auto_finished=true, source-ref:llms_emp_feedback_final_0019.puml:line:35\|exit_urban --> FinishState: auto_finished=true, source-ref:llms_emp_feedback_final_0019.puml:line:37\|HighwayMode --> UrbanMode: urban_way=true, source-ref:llms_emp_feedback_final_0019.puml:line:38\|UrbanMode --> HighwayMode: high_way=true | element-ref:compiler:route_control:R45RouteToken@line:1\|def int R45RouteToken = 0;, element-ref:compiler:transition_segment:tr_0022:segment:1@line:31\|enter_hwy -> [*] : /urban_way_true effect { R45RouteToken = 22; };, element-ref:compiler:transition_segment:tr_0022:segment:2@line:32\|cruise -> [*] : /urban_way_true effect { R45RouteToken = 22; };, element-ref:compiler:transition_segment:tr_0022:segment:3@line:33\|lane_change -> [*] : /urban_way_true effect { R45RouteToken = 22; };, element-ref:compiler:transition_segment:tr_0022:segment:4@line:34\|ExitHighway -> [*] : /urban_way_true effect { R45RouteToken = 22; };, element-ref:compiler:transition_segment:tr_0022:segment:5@line:61\|HighwayMode -> UrbanMode : if [R45RouteToken == 22] effect { R45RouteToken = 0; }; | compiler:route_control:R45RouteToken, compiler:transition_segment:tr_0022:segment:1, compiler:transition_segment:tr_0022:segment:2, compiler:transition_segment:tr_0022:segment:3, compiler:transition_segment:tr_0022:segment:4, compiler:transition_segment:tr_0022:segment:5, source:transition:tr_0022 | Case 0019 route_controller occurrence review:route_controller:0006:tr_0022 binds exact source refs to working-contract elements compiler:route_control:R45RouteToken, compiler:transition_segment:tr_0022:segment:1, compiler:transition_segment:tr_0022:segment:2, compiler:transition_segment:tr_0022:segment:3, compiler:transition_segment:tr_0022:segment:4, compiler:transition_segment:tr_0022:segment:5, source:transition:tr_0022. R45RouteToken and routed segments remain compiler_owned, protected, and excluded from confirmed issues, Repair, Confirm acceptance, and main results. |
| `review:multi_segment_macro:0007:tr_0023` | `multi_segment_macro` | `compiler_artifact_excluded` | source-ref:llms_emp_feedback_final_0019.puml:line:21\|ExitHighway --> FinishState: auto_finished=true, source-ref:llms_emp_feedback_final_0019.puml:line:35\|exit_urban --> FinishState: auto_finished=true, source-ref:llms_emp_feedback_final_0019.puml:line:37\|HighwayMode --> UrbanMode: urban_way=true, source-ref:llms_emp_feedback_final_0019.puml:line:38\|UrbanMode --> HighwayMode: high_way=true | element-ref:compiler:route_control:R45RouteToken@line:1\|def int R45RouteToken = 0;, element-ref:compiler:transition_segment:tr_0023:segment:1@line:51\|enter_urban -> [*] : /high_way_true effect { R45RouteToken = 23; };, element-ref:compiler:transition_segment:tr_0023:segment:2@line:52\|lane_change_urban -> [*] : /high_way_true effect { R45RouteToken = 23; };, element-ref:compiler:transition_segment:tr_0023:segment:3@line:53\|straight -> [*] : /high_way_true effect { R45RouteToken = 23; };, element-ref:compiler:transition_segment:tr_0023:segment:4@line:54\|intersection -> [*] : /high_way_true effect { R45RouteToken = 23; };, element-ref:compiler:transition_segment:tr_0023:segment:5@line:55\|exit_urban -> [*] : /high_way_true effect { R45RouteToken = 23; };, element-ref:compiler:transition_segment:tr_0023:segment:6@line:62\|UrbanMode -> HighwayMode : if [R45RouteToken == 23] effect { R45RouteToken = 0; }; | compiler:route_control:R45RouteToken, compiler:transition_segment:tr_0023:segment:1, compiler:transition_segment:tr_0023:segment:2, compiler:transition_segment:tr_0023:segment:3, compiler:transition_segment:tr_0023:segment:4, compiler:transition_segment:tr_0023:segment:5, compiler:transition_segment:tr_0023:segment:6, source:transition:tr_0023 | Case 0019 multi_segment_macro occurrence review:multi_segment_macro:0007:tr_0023 binds exact source refs to working-contract elements compiler:route_control:R45RouteToken, compiler:transition_segment:tr_0023:segment:1, compiler:transition_segment:tr_0023:segment:2, compiler:transition_segment:tr_0023:segment:3, compiler:transition_segment:tr_0023:segment:4, compiler:transition_segment:tr_0023:segment:5, compiler:transition_segment:tr_0023:segment:6, source:transition:tr_0023. All emitted segments collapse to one source transition root; no segment is promoted as a separate authored transition or editable issue target. |
| `review:route_controller:0008:tr_0023` | `route_controller` | `compiler_artifact_excluded` | source-ref:llms_emp_feedback_final_0019.puml:line:21\|ExitHighway --> FinishState: auto_finished=true, source-ref:llms_emp_feedback_final_0019.puml:line:35\|exit_urban --> FinishState: auto_finished=true, source-ref:llms_emp_feedback_final_0019.puml:line:37\|HighwayMode --> UrbanMode: urban_way=true, source-ref:llms_emp_feedback_final_0019.puml:line:38\|UrbanMode --> HighwayMode: high_way=true | element-ref:compiler:route_control:R45RouteToken@line:1\|def int R45RouteToken = 0;, element-ref:compiler:transition_segment:tr_0023:segment:1@line:51\|enter_urban -> [*] : /high_way_true effect { R45RouteToken = 23; };, element-ref:compiler:transition_segment:tr_0023:segment:2@line:52\|lane_change_urban -> [*] : /high_way_true effect { R45RouteToken = 23; };, element-ref:compiler:transition_segment:tr_0023:segment:3@line:53\|straight -> [*] : /high_way_true effect { R45RouteToken = 23; };, element-ref:compiler:transition_segment:tr_0023:segment:4@line:54\|intersection -> [*] : /high_way_true effect { R45RouteToken = 23; };, element-ref:compiler:transition_segment:tr_0023:segment:5@line:55\|exit_urban -> [*] : /high_way_true effect { R45RouteToken = 23; };, element-ref:compiler:transition_segment:tr_0023:segment:6@line:62\|UrbanMode -> HighwayMode : if [R45RouteToken == 23] effect { R45RouteToken = 0; }; | compiler:route_control:R45RouteToken, compiler:transition_segment:tr_0023:segment:1, compiler:transition_segment:tr_0023:segment:2, compiler:transition_segment:tr_0023:segment:3, compiler:transition_segment:tr_0023:segment:4, compiler:transition_segment:tr_0023:segment:5, compiler:transition_segment:tr_0023:segment:6, source:transition:tr_0023 | Case 0019 route_controller occurrence review:route_controller:0008:tr_0023 binds exact source refs to working-contract elements compiler:route_control:R45RouteToken, compiler:transition_segment:tr_0023:segment:1, compiler:transition_segment:tr_0023:segment:2, compiler:transition_segment:tr_0023:segment:3, compiler:transition_segment:tr_0023:segment:4, compiler:transition_segment:tr_0023:segment:5, compiler:transition_segment:tr_0023:segment:6, source:transition:tr_0023. R45RouteToken and routed segments remain compiler_owned, protected, and excluded from confirmed issues, Repair, Confirm acceptance, and main results. |
| `review:synthetic_state:0009:001-UnspecifiedInitial` | `synthetic_state` | `compiler_artifact_excluded` | source-ref:llms_emp_feedback_final_0019.puml:line:41\|state CollisionAvoidanceSystem { | element-ref:compiler:state:llms_emp_feedback_final_0019.CollisionAvoidanceSystem.UnspecifiedInitial@line:70\|state UnspecifiedInitial named "Unspecified initial";, element-ref:source:state:CollisionAvoidanceSystem@line:67\|state CollisionAvoidanceSystem named "CollisionAvoidanceSystem" { | compiler:state:llms_emp_feedback_final_0019.CollisionAvoidanceSystem.UnspecifiedInitial, source:state:CollisionAvoidanceSystem | Case 0019 synthetic_state occurrence review:synthetic_state:0009:001-UnspecifiedInitial binds exact source refs to working-contract elements compiler:state:llms_emp_feedback_final_0019.CollisionAvoidanceSystem.UnspecifiedInitial, source:state:CollisionAvoidanceSystem. The placeholder makes the authored missing, invalid, or final boundary visible while the synthetic state itself remains a non-repairable compiler artifact. |

## 作者阶段 lineage

| stage | output cell | present | output SHA-256 | feedback | resolved |
|---|---|---|---|---|---|
| `phase_i_generation` | `I21` | `true` | `b4c24224cccc1a34efedeafd961ef2b4867aeb0701ce8f8a0ea78691a75c936d` | - | - |
| `phase_ii_format` | `U21` | `true` | `6bb3c5c655131a5921877cf44539d859f3dbd27faece819936ad118d48ba4836` | syntax error: note right: Autonomous driving mode | YES |
| `phase_ii_grammar` | `Z21` | `false` | `-` | - | - |
| `phase_ii_semantic` | `AE21` | `true` | `6bb3c5c655131a5921877cf44539d859f3dbd27faece819936ad118d48ba4836` | None | - |

## Official identity ledger

- status：`aligned`
- canonical / official states：`17` / `17`
- aligned transition endpoints：`25`

本组 state identity 无需重映射。

本组 transition endpoint 无需重映射。

## Source normalization ledger

本组没有 source-input normalization。

## Concurrent region ledger

本组没有 PlantUML orthogonal/concurrent region separator。

## Operational debt

| reason code | count |
|---|---:|
| `R45.DEBT.composite_source_activation_dispatch` | 2 |
| `R45.DEBT.missing_explicit_initial` | 1 |
| `R45.DEBT.opaque_transition_label_semantics` | 23 |

## NL

```text
1. The system begins in the AutonomousMode state, which transitions into the InitialState substate, marking the starting point of the autonomous driving mode.
2. From the InitialState, the system can transition to either HighwayMode or UrbanMode based on conditions: `high_way=true` for HighwayMode or `urban_way=true` for UrbanMode.
3. In the HighwayMode state, the system begins in the enter_hwy substate, and can transition to cruise or lane_change based on the distance to the front vehicle (`dist_to_front<25`) and the availability of an extra lane (`extra_lane=true`).
4. If the system is in lane_change, it can return to cruise once the lane change is completed or exit the highway if the distance to the exit is less than 2 kilometers (`dist_to_exit<2`).
5. In the cruise substate, if the distance to the front vehicle becomes less than 25 meters (`dist_to_front<25`) and there is an extra lane available, the system transitions to lane_change. The system can also exit the highway if the distance to the exit is less than 2 kilometers (`dist_to_exit<2`).
6. The HighwayMode ends when the system transitions to FinishState, triggered by the `auto_finished=true` condition.
7. In UrbanMode, the system begins in the enter_urban substate. From here, it can transition to lane_change_urban if the distance to the front vehicle is less than 15 meters (`dist_to_front<15`) and an extra lane is available, or straight if the road ahead is clear, or intersection if it detects an intersection (`intersection=true`).
8. In the lane_change_urban substate, the system transitions to straight if the lane change is complete or to exit_urban if the distance to the urban exit is less than 0.7 kilometers (`dist_to_exit<0.7`).
9. In the straight substate, if the system detects an intersection, it transitions to the intersection substate. If the distance to the front vehicle becomes less than 15 meters (`dist_to_front<15`) and an extra lane is available, it transitions to lane_change_urban.
10. The system exits the UrbanMode state by transitioning to FinishState once `auto_finished=true` is satisfied.
11. The system supports dynamic transitions between HighwayMode and UrbanMode based on the conditions `urban_way=true` and `high_way=true`, respectively, facilitating seamless mode shifts during the drive.
12. The collision avoidance system is initially in the collision_avoidance_deactive state. It transitions to collision_avoidance_active when certain conditions are met, such as detecting pedestrians (`pedestrian_detected`), the rear distance being less than 5 meters with a velocity over 30 km/h (`dist_to_rear<5 & vel>30`), or the front distance being less than 15 meters in highway mode or 10 meters in urban mode.
13. Once in the collision_avoidance_active state, the collision avoidance system returns to the collision_avoidance_deactive state when there is no active danger, as indicated by the conditions `front_inactive`, `rear_inactive`, and `pedestrian_inactive`.
```

## 作者 Phase-II 最终 PlantUML STM0

```plantuml
@startuml
[*] --> AutonomousMode: Autonomous mode start
state AutonomousMode {

[*] --> InitialState: Start of autonomous driving mode

InitialState --> HighwayMode: high_way=true
InitialState --> UrbanMode: urban_way=true

state HighwayMode {
[*] --> enter_hwy
enter_hwy --> cruise: dist_to_front<25 & extra_lane=true
enter_hwy --> lane_change: dist_to_front<25 & extra_lane=true

cruise --> lane_change: dist_to_front<25 & extra_lane=true
cruise --> ExitHighway: dist_to_exit<2

lane_change --> cruise: Lane change completed
lane_change --> ExitHighway: dist_to_exit<2
}
ExitHighway --> FinishState: auto_finished=true

state UrbanMode {
[*] --> enter_urban
enter_urban --> lane_change_urban: dist_to_front<15 & extra_lane=true
enter_urban --> straight: Road ahead is clear
enter_urban --> intersection: intersection=true

lane_change_urban --> straight: Lane change completed
lane_change_urban --> exit_urban: dist_to_exit<0.7

straight --> intersection: intersection=true
straight --> lane_change_urban: dist_to_front<15 & extra_lane=true
}
exit_urban --> FinishState: auto_finished=true

HighwayMode --> UrbanMode: urban_way=true
UrbanMode --> HighwayMode: high_way=true
}

state CollisionAvoidanceSystem {
collision_avoidance_deactive --> collision_avoidance_active: pedestrian_detected | (dist_to_rear<5 & vel>30) | (dist_to_front<15 in hwy mode or <10 in urban mode)
collision_avoidance_active --> collision_avoidance_deactive: front_inactive & rear_inactive & pedestrian_inactive
}
@enduml
```

## 转换后 FCSTM STM0

```fcstm
def int R45RouteToken = 0;
state llms_emp_feedback_final_0019 named "llms_emp_feedback_final_0019" {
    event Autonomous_mode_start named "Autonomous mode start";
    event Start_of_autonomous_driving_mode named "Start of autonomous driving mode";
    event high_way_true named "high_way=true";
    event urban_way_true named "urban_way=true";
    event dist_to_front_25_extra_lane_true named "dist_to_front<25 & extra_lane=true";
    event dist_to_exit_2 named "dist_to_exit<2";
    event Lane_change_completed named "Lane change completed";
    event auto_finished_true named "auto_finished=true";
    event dist_to_front_15_extra_lane_true named "dist_to_front<15 & extra_lane=true";
    event Road_ahead_is_clear named "Road ahead is clear";
    event intersection_true named "intersection=true";
    event dist_to_exit_0_7 named "dist_to_exit<0.7";
    event pedestrian_detected_dist_to_rear_5_vel_30_dist_to_front_15_in_hwy_mode_or_10_in_urban_mode named "pedestrian_detected | (dist_to_rear<5 & vel>30) | (dist_to_front<15 in hwy mode or <10 in urban mode)";
    event front_inactive_rear_inactive_pedestrian_inactive named "front_inactive & rear_inactive & pedestrian_inactive";
    state AutonomousMode named "AutonomousMode" {
        state HighwayMode named "HighwayMode" {
            state enter_hwy named "enter_hwy";
            state cruise named "cruise";
            state lane_change named "lane_change";
            state ExitHighway named "ExitHighway";
            [*] -> enter_hwy;
            enter_hwy -> cruise : /dist_to_front_25_extra_lane_true;
            enter_hwy -> lane_change : /dist_to_front_25_extra_lane_true;
            cruise -> lane_change : /dist_to_front_25_extra_lane_true;
            cruise -> ExitHighway : /dist_to_exit_2;
            lane_change -> cruise : /Lane_change_completed;
            lane_change -> ExitHighway : /dist_to_exit_2;
            ExitHighway -> [*] : /auto_finished_true effect { R45RouteToken = 12; };
            enter_hwy -> [*] : /urban_way_true effect { R45RouteToken = 22; };
            cruise -> [*] : /urban_way_true effect { R45RouteToken = 22; };
            lane_change -> [*] : /urban_way_true effect { R45RouteToken = 22; };
            ExitHighway -> [*] : /urban_way_true effect { R45RouteToken = 22; };
        }
        state UrbanMode named "UrbanMode" {
            state enter_urban named "enter_urban";
            state lane_change_urban named "lane_change_urban";
            state straight named "straight";
            state intersection named "intersection";
            state exit_urban named "exit_urban";
            [*] -> enter_urban;
            enter_urban -> lane_change_urban : /dist_to_front_15_extra_lane_true;
            enter_urban -> straight : /Road_ahead_is_clear;
            enter_urban -> intersection : /intersection_true;
            lane_change_urban -> straight : /Lane_change_completed;
            lane_change_urban -> exit_urban : /dist_to_exit_0_7;
            straight -> intersection : /intersection_true;
            straight -> lane_change_urban : /dist_to_front_15_extra_lane_true;
            exit_urban -> [*] : /auto_finished_true effect { R45RouteToken = 21; };
            enter_urban -> [*] : /high_way_true effect { R45RouteToken = 23; };
            lane_change_urban -> [*] : /high_way_true effect { R45RouteToken = 23; };
            straight -> [*] : /high_way_true effect { R45RouteToken = 23; };
            intersection -> [*] : /high_way_true effect { R45RouteToken = 23; };
            exit_urban -> [*] : /high_way_true effect { R45RouteToken = 23; };
        }
        state InitialState named "InitialState";
        state FinishState named "FinishState";
        HighwayMode -> FinishState : if [R45RouteToken == 12] effect { R45RouteToken = 0; };
        UrbanMode -> FinishState : if [R45RouteToken == 21] effect { R45RouteToken = 0; };
        HighwayMode -> UrbanMode : if [R45RouteToken == 22] effect { R45RouteToken = 0; };
        UrbanMode -> HighwayMode : if [R45RouteToken == 23] effect { R45RouteToken = 0; };
        [*] -> InitialState : /Start_of_autonomous_driving_mode;
        InitialState -> HighwayMode : /high_way_true;
        InitialState -> UrbanMode : /urban_way_true;
    }
    state CollisionAvoidanceSystem named "CollisionAvoidanceSystem" {
        state collision_avoidance_deactive named "collision_avoidance_deactive";
        state collision_avoidance_active named "collision_avoidance_active";
        state UnspecifiedInitial named "Unspecified initial";
        [*] -> UnspecifiedInitial;
        collision_avoidance_deactive -> collision_avoidance_active : /pedestrian_detected_dist_to_rear_5_vel_30_dist_to_front_15_in_hwy_mode_or_10_in_urban_mode;
        collision_avoidance_active -> collision_avoidance_deactive : /front_inactive_rear_inactive_pedestrian_inactive;
    }
    [*] -> AutonomousMode : /Autonomous_mode_start;
}
```

[上一组 `0018`](../0018/README.md) | [返回 60 组索引](../../PAIR_INDEX.md) | [下一组 `0020`](../0020/README.md)
