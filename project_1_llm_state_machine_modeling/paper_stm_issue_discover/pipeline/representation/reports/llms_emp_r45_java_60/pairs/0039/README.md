# Pair `0039`：NL + PlantUML STM0 + FCSTM STM0

[上一组 `0038`](../0038/README.md) | [返回 60 组索引](../../PAIR_INDEX.md) | [下一组 `0040`](../0040/README.md)

- LLM：`Kimi`
- 模型/场景：autonomous mode
- 作者输出阶段：`Result with Semantic Checking`
- 作者输出单元格：`AE41`；Excel row：`41`
- Phase-I fallback：`false`
- 相对 Phase-I 是否变化：`false`
- Phase-I PlantUML SHA-256：`187fb536bf88351c12f83f63d5b5d2bf1c096b0a99aa9089ce722ba07f2a0391`
- NL SHA-256：`b7425c44960b36c3534f118279e347786d4074191efea7bf9a7c5ba032c9e82c`
- PlantUML SHA-256：`187fb536bf88351c12f83f63d5b5d2bf1c096b0a99aa9089ce722ba07f2a0391`
- FCSTM SHA-256：`fdc4158e2512976baba84cc46cd5eecc7691a4ba434eb7b0f4efecd68a1f0352`
- review subject SHA-256：`7741d512346a06240049ab6027deec0a4473e389bcbc3473829fad65111d4dcb`
- working contract SHA-256：`f0dd2f9f9e88eb2e6c5fc1bb68e9d69b7eecdd926b34837f45ced6c32e56afa7`
- 结构裁决：`structure_preserved`
- source states / transitions：`15` / `26`
- mapped / blocked / silent drop：`26` / `0` / `0`
- final / lifecycle / body coverage：`2/2` / `0/0` / `0/0`
- concurrent region / separator coverage：`0/0` / `0/0`
- source normalization coverage：`0/0`
- official raw / validation：`state_diagram` / `state_diagram`
- official identity states / transitions：`15` / `26`
- official identity remaps：state `0` / transition endpoint `0`
- AST audit：`passed`
- legacy whole-model FCSTM execution / Discover：`false` / `false`
- working bundle usage gate：`discover_input_with_capability_mask`
- ownership source / compiler / agent：`41` / `83` / `0`
- source macro / positive identity trace / conversion boundary trace：`26` / `41` / `0`
- capability source-static / simulation / transition-trace：`eligible_with_exclusions` / `eligible_with_exclusions` / `eligible_with_exclusions`
- compiler-only diagnostic policy：`rejected_conversion_artifact`；main-result conversion artifact limit：`0`
- 主 session 对读：`pass`；ownership/macro/capability 均为 `pass`；Case 0039 passes the current attribution-safe forward review; this does not assert global behavior equivalence, and unsupported runtime semantics remain fail-closed. Amendment record: the substantive subject review remains the one recorded in review_context (first reviewed 2026-07-20T05:44:08Z by gpt-5.5 (session omx-1784393668980-pxpj3q), and it still binds because review_subject_sha256 is unchanged. A scoped re-check was performed 2026-08-17 by claude-opus-5 (main-session LLM, PR #185) because commit bbb04cb1 (2026-07-27) regenerated the 60 working contracts and commit 35eba126 (2026-08-11) renamed the paper workspace, and neither refreshed this registry. The re-review is scoped: a key-by-key diff shows the only contract changes are capability_eligibility.simulation, capability_eligibility.transition_trace and summary.simulation_status (bbb04cb1) plus the four artifact_bindings path strings (35eba126); the remaining 168 keys and the whole of canonical/fcstm/parse_inspect/source_traces are byte-identical, so review_subject_sha256 is unchanged and the original ownership, macro and correspondence findings still stand. The capability block was re-checked against seven invariants: eligible ids are source: only, excluded ids cover the compiler-owned set, the two sets are disjoint, claim_boundary and reason_codes are non-empty, main_result_conversion_artifact_limit is still 0, and usage_gate is unchanged.
- source anchors：`source-ref:llms_emp_feedback_final_0039.puml:line:4\|state AutonomousMode {, source-ref:llms_emp_feedback_final_0039.puml:line:7\|InitialState --> HighwayMode : high_way=true`；FCSTM anchors：`element-ref:source:state:AutonomousMode@line:16\|state AutonomousMode named "AutonomousMode" {, element-ref:compiler:transition_segment:tr_0003:segment:1@line:87\|InitialState -> HighwayMode : /high_way_true;`
- 三个原始文件：[NL](./nl.txt) | [PlantUML](./plantuml.puml) | [FCSTM](./fcstm.fcstm)
- 审计入口：[canonical](../../canonical/llms_emp_feedback_final_0039.json) | [冻结 FCSTM](../../fcstm/llms_emp_feedback_final_0039.fcstm) | [case report](../../case_reports/llms_emp_feedback_final_0039.json) | [working contract](../../working_contracts/llms_emp_feedback_final_0039.json) | [source trace](../../source_traces/llms_emp_feedback_final_0039.json) | [人工总账](../../MANUAL_REVIEW.md)

## 主 session 三方语义对应

| projection | assessment | NL anchor | PlantUML anchor | FCSTM anchor | source roots | compiler members | rationale |
|---|---|---|---|---|---|---|---|
| `direct` | `preserved` | AutonomousMode | source-ref:llms_emp_feedback_final_0039.puml:line:4\|state AutonomousMode { | element-ref:source:state:AutonomousMode@line:16\|state AutonomousMode named "AutonomousMode" { | source:state:AutonomousMode | - | Case 0039 binds source:state:AutonomousMode to authored PlantUML occurrence 'state AutonomousMode {' and current FCSTM occurrence 'state AutonomousMode named "AutonomousMode" {'; the source semantic root remains attributable while any compiler-owned projection stays protected and cannot become an independent Repair target. |
| `macro` | `preserved_with_exclusions` | high_way=true | source-ref:llms_emp_feedback_final_0039.puml:line:7\|InitialState --> HighwayMode : high_way=true | element-ref:compiler:transition_segment:tr_0003:segment:1@line:87\|InitialState -> HighwayMode : /high_way_true; | source:transition:tr_0003 | compiler:transition_segment:tr_0003:segment:1 | Case 0039 binds source:transition:tr_0003 to authored PlantUML occurrence 'InitialState --> HighwayMode : high_way=true' and current FCSTM occurrence 'InitialState -> HighwayMode : /high_way_true;'; the source semantic root remains attributable while any compiler-owned projection stays protected and cannot become an independent Repair target. |

## Risk occurrence 第二遍复核

| obligation | risk tag | assessment | PlantUML evidence | FCSTM evidence | ownership evidence | rationale |
|---|---|---|---|---|---|---|
| `review:final_boundary:0001:tr_0009` | `final_boundary` | `source_fact_preserved` | source-ref:llms_emp_feedback_final_0039.puml:line:16\|lane_change --> [*] : dist_to_exit<2 | element-ref:compiler:state:llms_emp_feedback_final_0039.AutonomousMode.HighwayMode.FinalWaittr_0009@line:21\|state FinalWaittr_0009 named "Completed final boundary: AutonomousMode.HighwayMode.lane_change";, element-ref:compiler:transition_segment:tr_0009:segment:1@line:27\|lane_change -> FinalWaittr_0009 : /dist_to_exit_2; | compiler:state:llms_emp_feedback_final_0039.AutonomousMode.HighwayMode.FinalWaittr_0009, compiler:transition_segment:tr_0009:segment:1, source:transition:tr_0009 | Case 0039 final_boundary occurrence review:final_boundary:0001:tr_0009 binds exact source refs to working-contract elements compiler:state:llms_emp_feedback_final_0039.AutonomousMode.HighwayMode.FinalWaittr_0009, compiler:transition_segment:tr_0009:segment:1, source:transition:tr_0009. The authored final occurrence remains visible through its source root; any completion holder or routing segment is excluded from source-level claims. |
| `review:final_boundary:0002:tr_0010` | `final_boundary` | `source_fact_preserved` | source-ref:llms_emp_feedback_final_0039.puml:line:18\|cruise --> [*] : dist_to_exit<2 | element-ref:compiler:state:llms_emp_feedback_final_0039.AutonomousMode.HighwayMode.FinalWaittr_0010@line:22\|state FinalWaittr_0010 named "Completed final boundary: AutonomousMode.HighwayMode.cruise";, element-ref:compiler:transition_segment:tr_0010:segment:1@line:28\|cruise -> FinalWaittr_0010 : /dist_to_exit_2; | compiler:state:llms_emp_feedback_final_0039.AutonomousMode.HighwayMode.FinalWaittr_0010, compiler:transition_segment:tr_0010:segment:1, source:transition:tr_0010 | Case 0039 final_boundary occurrence review:final_boundary:0002:tr_0010 binds exact source refs to working-contract elements compiler:state:llms_emp_feedback_final_0039.AutonomousMode.HighwayMode.FinalWaittr_0010, compiler:transition_segment:tr_0010:segment:1, source:transition:tr_0010. The authored final occurrence remains visible through its source root; any completion holder or routing segment is excluded from source-level claims. |
| `review:multi_segment_macro:0003:tr_0012` | `multi_segment_macro` | `compiler_artifact_excluded` | source-ref:llms_emp_feedback_final_0039.puml:line:22\|HighwayMode --> FinishState : auto_finished=true, source-ref:llms_emp_feedback_final_0039.puml:line:38\|UrbanMode --> FinishState : auto_finished=true, source-ref:llms_emp_feedback_final_0039.puml:line:41\|AutonomousMode --> HighwayMode : high_way=true, source-ref:llms_emp_feedback_final_0039.puml:line:42\|AutonomousMode --> UrbanMode : urban_way=true | element-ref:compiler:route_control:R45RouteToken@line:1\|def int R45RouteToken = 0;, element-ref:compiler:transition_segment:tr_0012:segment:1@line:30\|enter_hwy -> [*] : /auto_finished_true effect { R45RouteToken = 12; };, element-ref:compiler:transition_segment:tr_0012:segment:2@line:31\|cruise -> [*] : /auto_finished_true effect { R45RouteToken = 12; };, element-ref:compiler:transition_segment:tr_0012:segment:3@line:32\|lane_change -> [*] : /auto_finished_true effect { R45RouteToken = 12; };, element-ref:compiler:transition_segment:tr_0012:segment:4@line:78\|HighwayMode -> FinishState : if [R45RouteToken == 12] effect { R45RouteToken = 0; };, element-ref:compiler:transition_segment:tr_0012:segment:5@line:39\|FinalWaittr_0009 -> [*] : /auto_finished_true effect { R45RouteToken = 12; };, element-ref:compiler:transition_segment:tr_0012:segment:6@line:40\|FinalWaittr_0010 -> [*] : /auto_finished_true effect { R45RouteToken = 12; }; | compiler:route_control:R45RouteToken, compiler:transition_segment:tr_0012:segment:1, compiler:transition_segment:tr_0012:segment:2, compiler:transition_segment:tr_0012:segment:3, compiler:transition_segment:tr_0012:segment:4, compiler:transition_segment:tr_0012:segment:5, compiler:transition_segment:tr_0012:segment:6, source:transition:tr_0012 | Case 0039 multi_segment_macro occurrence review:multi_segment_macro:0003:tr_0012 binds exact source refs to working-contract elements compiler:route_control:R45RouteToken, compiler:transition_segment:tr_0012:segment:1, compiler:transition_segment:tr_0012:segment:2, compiler:transition_segment:tr_0012:segment:3, compiler:transition_segment:tr_0012:segment:4, compiler:transition_segment:tr_0012:segment:5, compiler:transition_segment:tr_0012:segment:6, source:transition:tr_0012. All emitted segments collapse to one source transition root; no segment is promoted as a separate authored transition or editable issue target. |
| `review:route_controller:0004:tr_0012` | `route_controller` | `compiler_artifact_excluded` | source-ref:llms_emp_feedback_final_0039.puml:line:22\|HighwayMode --> FinishState : auto_finished=true, source-ref:llms_emp_feedback_final_0039.puml:line:38\|UrbanMode --> FinishState : auto_finished=true, source-ref:llms_emp_feedback_final_0039.puml:line:41\|AutonomousMode --> HighwayMode : high_way=true, source-ref:llms_emp_feedback_final_0039.puml:line:42\|AutonomousMode --> UrbanMode : urban_way=true | element-ref:compiler:route_control:R45RouteToken@line:1\|def int R45RouteToken = 0;, element-ref:compiler:transition_segment:tr_0012:segment:1@line:30\|enter_hwy -> [*] : /auto_finished_true effect { R45RouteToken = 12; };, element-ref:compiler:transition_segment:tr_0012:segment:2@line:31\|cruise -> [*] : /auto_finished_true effect { R45RouteToken = 12; };, element-ref:compiler:transition_segment:tr_0012:segment:3@line:32\|lane_change -> [*] : /auto_finished_true effect { R45RouteToken = 12; };, element-ref:compiler:transition_segment:tr_0012:segment:4@line:78\|HighwayMode -> FinishState : if [R45RouteToken == 12] effect { R45RouteToken = 0; };, element-ref:compiler:transition_segment:tr_0012:segment:5@line:39\|FinalWaittr_0009 -> [*] : /auto_finished_true effect { R45RouteToken = 12; };, element-ref:compiler:transition_segment:tr_0012:segment:6@line:40\|FinalWaittr_0010 -> [*] : /auto_finished_true effect { R45RouteToken = 12; }; | compiler:route_control:R45RouteToken, compiler:transition_segment:tr_0012:segment:1, compiler:transition_segment:tr_0012:segment:2, compiler:transition_segment:tr_0012:segment:3, compiler:transition_segment:tr_0012:segment:4, compiler:transition_segment:tr_0012:segment:5, compiler:transition_segment:tr_0012:segment:6, source:transition:tr_0012 | Case 0039 route_controller occurrence review:route_controller:0004:tr_0012 binds exact source refs to working-contract elements compiler:route_control:R45RouteToken, compiler:transition_segment:tr_0012:segment:1, compiler:transition_segment:tr_0012:segment:2, compiler:transition_segment:tr_0012:segment:3, compiler:transition_segment:tr_0012:segment:4, compiler:transition_segment:tr_0012:segment:5, compiler:transition_segment:tr_0012:segment:6, source:transition:tr_0012. R45RouteToken and routed segments remain compiler_owned, protected, and excluded from confirmed issues, Repair, Confirm acceptance, and main results. |
| `review:multi_segment_macro:0005:tr_0021` | `multi_segment_macro` | `compiler_artifact_excluded` | source-ref:llms_emp_feedback_final_0039.puml:line:22\|HighwayMode --> FinishState : auto_finished=true, source-ref:llms_emp_feedback_final_0039.puml:line:38\|UrbanMode --> FinishState : auto_finished=true, source-ref:llms_emp_feedback_final_0039.puml:line:41\|AutonomousMode --> HighwayMode : high_way=true, source-ref:llms_emp_feedback_final_0039.puml:line:42\|AutonomousMode --> UrbanMode : urban_way=true | element-ref:compiler:route_control:R45RouteToken@line:1\|def int R45RouteToken = 0;, element-ref:compiler:transition_segment:tr_0021:segment:1@line:60\|enter_urban -> [*] : /auto_finished_true effect { R45RouteToken = 21; };, element-ref:compiler:transition_segment:tr_0021:segment:2@line:61\|lane_change_urban -> [*] : /auto_finished_true effect { R45RouteToken = 21; };, element-ref:compiler:transition_segment:tr_0021:segment:3@line:62\|straight -> [*] : /auto_finished_true effect { R45RouteToken = 21; };, element-ref:compiler:transition_segment:tr_0021:segment:4@line:63\|intersection -> [*] : /auto_finished_true effect { R45RouteToken = 21; };, element-ref:compiler:transition_segment:tr_0021:segment:5@line:64\|exit_urban -> [*] : /auto_finished_true effect { R45RouteToken = 21; };, element-ref:compiler:transition_segment:tr_0021:segment:6@line:79\|UrbanMode -> FinishState : if [R45RouteToken == 21] effect { R45RouteToken = 0; }; | compiler:route_control:R45RouteToken, compiler:transition_segment:tr_0021:segment:1, compiler:transition_segment:tr_0021:segment:2, compiler:transition_segment:tr_0021:segment:3, compiler:transition_segment:tr_0021:segment:4, compiler:transition_segment:tr_0021:segment:5, compiler:transition_segment:tr_0021:segment:6, source:transition:tr_0021 | Case 0039 multi_segment_macro occurrence review:multi_segment_macro:0005:tr_0021 binds exact source refs to working-contract elements compiler:route_control:R45RouteToken, compiler:transition_segment:tr_0021:segment:1, compiler:transition_segment:tr_0021:segment:2, compiler:transition_segment:tr_0021:segment:3, compiler:transition_segment:tr_0021:segment:4, compiler:transition_segment:tr_0021:segment:5, compiler:transition_segment:tr_0021:segment:6, source:transition:tr_0021. All emitted segments collapse to one source transition root; no segment is promoted as a separate authored transition or editable issue target. |
| `review:route_controller:0006:tr_0021` | `route_controller` | `compiler_artifact_excluded` | source-ref:llms_emp_feedback_final_0039.puml:line:22\|HighwayMode --> FinishState : auto_finished=true, source-ref:llms_emp_feedback_final_0039.puml:line:38\|UrbanMode --> FinishState : auto_finished=true, source-ref:llms_emp_feedback_final_0039.puml:line:41\|AutonomousMode --> HighwayMode : high_way=true, source-ref:llms_emp_feedback_final_0039.puml:line:42\|AutonomousMode --> UrbanMode : urban_way=true | element-ref:compiler:route_control:R45RouteToken@line:1\|def int R45RouteToken = 0;, element-ref:compiler:transition_segment:tr_0021:segment:1@line:60\|enter_urban -> [*] : /auto_finished_true effect { R45RouteToken = 21; };, element-ref:compiler:transition_segment:tr_0021:segment:2@line:61\|lane_change_urban -> [*] : /auto_finished_true effect { R45RouteToken = 21; };, element-ref:compiler:transition_segment:tr_0021:segment:3@line:62\|straight -> [*] : /auto_finished_true effect { R45RouteToken = 21; };, element-ref:compiler:transition_segment:tr_0021:segment:4@line:63\|intersection -> [*] : /auto_finished_true effect { R45RouteToken = 21; };, element-ref:compiler:transition_segment:tr_0021:segment:5@line:64\|exit_urban -> [*] : /auto_finished_true effect { R45RouteToken = 21; };, element-ref:compiler:transition_segment:tr_0021:segment:6@line:79\|UrbanMode -> FinishState : if [R45RouteToken == 21] effect { R45RouteToken = 0; }; | compiler:route_control:R45RouteToken, compiler:transition_segment:tr_0021:segment:1, compiler:transition_segment:tr_0021:segment:2, compiler:transition_segment:tr_0021:segment:3, compiler:transition_segment:tr_0021:segment:4, compiler:transition_segment:tr_0021:segment:5, compiler:transition_segment:tr_0021:segment:6, source:transition:tr_0021 | Case 0039 route_controller occurrence review:route_controller:0006:tr_0021 binds exact source refs to working-contract elements compiler:route_control:R45RouteToken, compiler:transition_segment:tr_0021:segment:1, compiler:transition_segment:tr_0021:segment:2, compiler:transition_segment:tr_0021:segment:3, compiler:transition_segment:tr_0021:segment:4, compiler:transition_segment:tr_0021:segment:5, compiler:transition_segment:tr_0021:segment:6, source:transition:tr_0021. R45RouteToken and routed segments remain compiler_owned, protected, and excluded from confirmed issues, Repair, Confirm acceptance, and main results. |
| `review:multi_segment_macro:0007:tr_0022` | `multi_segment_macro` | `compiler_artifact_excluded` | source-ref:llms_emp_feedback_final_0039.puml:line:22\|HighwayMode --> FinishState : auto_finished=true, source-ref:llms_emp_feedback_final_0039.puml:line:38\|UrbanMode --> FinishState : auto_finished=true, source-ref:llms_emp_feedback_final_0039.puml:line:41\|AutonomousMode --> HighwayMode : high_way=true, source-ref:llms_emp_feedback_final_0039.puml:line:42\|AutonomousMode --> UrbanMode : urban_way=true | element-ref:compiler:route_control:R45RouteToken@line:1\|def int R45RouteToken = 0;, element-ref:compiler:transition_segment:tr_0022:segment:10@line:69\|exit_urban -> [*] : /high_way_true effect { R45RouteToken = 22; };, element-ref:compiler:transition_segment:tr_0022:segment:11@line:89\|InitialState -> [*] : /high_way_true effect { R45RouteToken = 22; };, element-ref:compiler:transition_segment:tr_0022:segment:12@line:90\|FinishState -> [*] : /high_way_true effect { R45RouteToken = 22; };, element-ref:compiler:transition_segment:tr_0022:segment:13@line:96\|AutonomousMode -> AutonomousMode : if [R45RouteToken == 22];, element-ref:compiler:transition_segment:tr_0022:segment:14@line:82\|[*] -> HighwayMode : if [R45RouteToken == 22] effect { R45RouteToken = 0; };, element-ref:compiler:transition_segment:tr_0022:segment:15@line:41\|FinalWaittr_0009 -> [*] : /high_way_true effect { R45RouteToken = 22; };, element-ref:compiler:transition_segment:tr_0022:segment:16@line:42\|FinalWaittr_0010 -> [*] : /high_way_true effect { R45RouteToken = 22; };, element-ref:compiler:transition_segment:tr_0022:segment:1@line:33\|enter_hwy -> [*] : /high_way_true effect { R45RouteToken = 22; };, element-ref:compiler:transition_segment:tr_0022:segment:2@line:80\|HighwayMode -> [*] : if [R45RouteToken == 22];, element-ref:compiler:transition_segment:tr_0022:segment:3@line:34\|cruise -> [*] : /high_way_true effect { R45RouteToken = 22; };, element-ref:compiler:transition_segment:tr_0022:segment:4@line:35\|lane_change -> [*] : /high_way_true effect { R45RouteToken = 22; };, element-ref:compiler:transition_segment:tr_0022:segment:5@line:65\|enter_urban -> [*] : /high_way_true effect { R45RouteToken = 22; };, element-ref:compiler:transition_segment:tr_0022:segment:6@line:81\|UrbanMode -> [*] : if [R45RouteToken == 22];, element-ref:compiler:transition_segment:tr_0022:segment:7@line:66\|lane_change_urban -> [*] : /high_way_true effect { R45RouteToken = 22; };, element-ref:compiler:transition_segment:tr_0022:segment:8@line:67\|straight -> [*] : /high_way_true effect { R45RouteToken = 22; };, element-ref:compiler:transition_segment:tr_0022:segment:9@line:68\|intersection -> [*] : /high_way_true effect { R45RouteToken = 22; }; | compiler:route_control:R45RouteToken, compiler:transition_segment:tr_0022:segment:1, compiler:transition_segment:tr_0022:segment:10, compiler:transition_segment:tr_0022:segment:11, compiler:transition_segment:tr_0022:segment:12, compiler:transition_segment:tr_0022:segment:13, compiler:transition_segment:tr_0022:segment:14, compiler:transition_segment:tr_0022:segment:15, compiler:transition_segment:tr_0022:segment:16, compiler:transition_segment:tr_0022:segment:2, compiler:transition_segment:tr_0022:segment:3, compiler:transition_segment:tr_0022:segment:4, compiler:transition_segment:tr_0022:segment:5, compiler:transition_segment:tr_0022:segment:6, compiler:transition_segment:tr_0022:segment:7, compiler:transition_segment:tr_0022:segment:8, compiler:transition_segment:tr_0022:segment:9, source:transition:tr_0022 | Case 0039 multi_segment_macro occurrence review:multi_segment_macro:0007:tr_0022 binds exact source refs to working-contract elements compiler:route_control:R45RouteToken, compiler:transition_segment:tr_0022:segment:1, compiler:transition_segment:tr_0022:segment:10, compiler:transition_segment:tr_0022:segment:11, compiler:transition_segment:tr_0022:segment:12, compiler:transition_segment:tr_0022:segment:13, compiler:transition_segment:tr_0022:segment:14, compiler:transition_segment:tr_0022:segment:15, compiler:transition_segment:tr_0022:segment:16, compiler:transition_segment:tr_0022:segment:2, compiler:transition_segment:tr_0022:segment:3, compiler:transition_segment:tr_0022:segment:4, compiler:transition_segment:tr_0022:segment:5, compiler:transition_segment:tr_0022:segment:6, compiler:transition_segment:tr_0022:segment:7, compiler:transition_segment:tr_0022:segment:8, compiler:transition_segment:tr_0022:segment:9, source:transition:tr_0022. All emitted segments collapse to one source transition root; no segment is promoted as a separate authored transition or editable issue target. |
| `review:route_controller:0008:tr_0022` | `route_controller` | `compiler_artifact_excluded` | source-ref:llms_emp_feedback_final_0039.puml:line:22\|HighwayMode --> FinishState : auto_finished=true, source-ref:llms_emp_feedback_final_0039.puml:line:38\|UrbanMode --> FinishState : auto_finished=true, source-ref:llms_emp_feedback_final_0039.puml:line:41\|AutonomousMode --> HighwayMode : high_way=true, source-ref:llms_emp_feedback_final_0039.puml:line:42\|AutonomousMode --> UrbanMode : urban_way=true | element-ref:compiler:route_control:R45RouteToken@line:1\|def int R45RouteToken = 0;, element-ref:compiler:transition_segment:tr_0022:segment:10@line:69\|exit_urban -> [*] : /high_way_true effect { R45RouteToken = 22; };, element-ref:compiler:transition_segment:tr_0022:segment:11@line:89\|InitialState -> [*] : /high_way_true effect { R45RouteToken = 22; };, element-ref:compiler:transition_segment:tr_0022:segment:12@line:90\|FinishState -> [*] : /high_way_true effect { R45RouteToken = 22; };, element-ref:compiler:transition_segment:tr_0022:segment:13@line:96\|AutonomousMode -> AutonomousMode : if [R45RouteToken == 22];, element-ref:compiler:transition_segment:tr_0022:segment:14@line:82\|[*] -> HighwayMode : if [R45RouteToken == 22] effect { R45RouteToken = 0; };, element-ref:compiler:transition_segment:tr_0022:segment:15@line:41\|FinalWaittr_0009 -> [*] : /high_way_true effect { R45RouteToken = 22; };, element-ref:compiler:transition_segment:tr_0022:segment:16@line:42\|FinalWaittr_0010 -> [*] : /high_way_true effect { R45RouteToken = 22; };, element-ref:compiler:transition_segment:tr_0022:segment:1@line:33\|enter_hwy -> [*] : /high_way_true effect { R45RouteToken = 22; };, element-ref:compiler:transition_segment:tr_0022:segment:2@line:80\|HighwayMode -> [*] : if [R45RouteToken == 22];, element-ref:compiler:transition_segment:tr_0022:segment:3@line:34\|cruise -> [*] : /high_way_true effect { R45RouteToken = 22; };, element-ref:compiler:transition_segment:tr_0022:segment:4@line:35\|lane_change -> [*] : /high_way_true effect { R45RouteToken = 22; };, element-ref:compiler:transition_segment:tr_0022:segment:5@line:65\|enter_urban -> [*] : /high_way_true effect { R45RouteToken = 22; };, element-ref:compiler:transition_segment:tr_0022:segment:6@line:81\|UrbanMode -> [*] : if [R45RouteToken == 22];, element-ref:compiler:transition_segment:tr_0022:segment:7@line:66\|lane_change_urban -> [*] : /high_way_true effect { R45RouteToken = 22; };, element-ref:compiler:transition_segment:tr_0022:segment:8@line:67\|straight -> [*] : /high_way_true effect { R45RouteToken = 22; };, element-ref:compiler:transition_segment:tr_0022:segment:9@line:68\|intersection -> [*] : /high_way_true effect { R45RouteToken = 22; }; | compiler:route_control:R45RouteToken, compiler:transition_segment:tr_0022:segment:1, compiler:transition_segment:tr_0022:segment:10, compiler:transition_segment:tr_0022:segment:11, compiler:transition_segment:tr_0022:segment:12, compiler:transition_segment:tr_0022:segment:13, compiler:transition_segment:tr_0022:segment:14, compiler:transition_segment:tr_0022:segment:15, compiler:transition_segment:tr_0022:segment:16, compiler:transition_segment:tr_0022:segment:2, compiler:transition_segment:tr_0022:segment:3, compiler:transition_segment:tr_0022:segment:4, compiler:transition_segment:tr_0022:segment:5, compiler:transition_segment:tr_0022:segment:6, compiler:transition_segment:tr_0022:segment:7, compiler:transition_segment:tr_0022:segment:8, compiler:transition_segment:tr_0022:segment:9, source:transition:tr_0022 | Case 0039 route_controller occurrence review:route_controller:0008:tr_0022 binds exact source refs to working-contract elements compiler:route_control:R45RouteToken, compiler:transition_segment:tr_0022:segment:1, compiler:transition_segment:tr_0022:segment:10, compiler:transition_segment:tr_0022:segment:11, compiler:transition_segment:tr_0022:segment:12, compiler:transition_segment:tr_0022:segment:13, compiler:transition_segment:tr_0022:segment:14, compiler:transition_segment:tr_0022:segment:15, compiler:transition_segment:tr_0022:segment:16, compiler:transition_segment:tr_0022:segment:2, compiler:transition_segment:tr_0022:segment:3, compiler:transition_segment:tr_0022:segment:4, compiler:transition_segment:tr_0022:segment:5, compiler:transition_segment:tr_0022:segment:6, compiler:transition_segment:tr_0022:segment:7, compiler:transition_segment:tr_0022:segment:8, compiler:transition_segment:tr_0022:segment:9, source:transition:tr_0022. R45RouteToken and routed segments remain compiler_owned, protected, and excluded from confirmed issues, Repair, Confirm acceptance, and main results. |
| `review:multi_segment_macro:0009:tr_0023` | `multi_segment_macro` | `compiler_artifact_excluded` | source-ref:llms_emp_feedback_final_0039.puml:line:22\|HighwayMode --> FinishState : auto_finished=true, source-ref:llms_emp_feedback_final_0039.puml:line:38\|UrbanMode --> FinishState : auto_finished=true, source-ref:llms_emp_feedback_final_0039.puml:line:41\|AutonomousMode --> HighwayMode : high_way=true, source-ref:llms_emp_feedback_final_0039.puml:line:42\|AutonomousMode --> UrbanMode : urban_way=true | element-ref:compiler:route_control:R45RouteToken@line:1\|def int R45RouteToken = 0;, element-ref:compiler:transition_segment:tr_0023:segment:10@line:74\|exit_urban -> [*] : /urban_way_true effect { R45RouteToken = 23; };, element-ref:compiler:transition_segment:tr_0023:segment:11@line:91\|InitialState -> [*] : /urban_way_true effect { R45RouteToken = 23; };, element-ref:compiler:transition_segment:tr_0023:segment:12@line:92\|FinishState -> [*] : /urban_way_true effect { R45RouteToken = 23; };, element-ref:compiler:transition_segment:tr_0023:segment:13@line:97\|AutonomousMode -> AutonomousMode : if [R45RouteToken == 23];, element-ref:compiler:transition_segment:tr_0023:segment:14@line:85\|[*] -> UrbanMode : if [R45RouteToken == 23] effect { R45RouteToken = 0; };, element-ref:compiler:transition_segment:tr_0023:segment:15@line:43\|FinalWaittr_0009 -> [*] : /urban_way_true effect { R45RouteToken = 23; };, element-ref:compiler:transition_segment:tr_0023:segment:16@line:44\|FinalWaittr_0010 -> [*] : /urban_way_true effect { R45RouteToken = 23; };, element-ref:compiler:transition_segment:tr_0023:segment:1@line:36\|enter_hwy -> [*] : /urban_way_true effect { R45RouteToken = 23; };, element-ref:compiler:transition_segment:tr_0023:segment:2@line:83\|HighwayMode -> [*] : if [R45RouteToken == 23];, element-ref:compiler:transition_segment:tr_0023:segment:3@line:37\|cruise -> [*] : /urban_way_true effect { R45RouteToken = 23; };, element-ref:compiler:transition_segment:tr_0023:segment:4@line:38\|lane_change -> [*] : /urban_way_true effect { R45RouteToken = 23; };, element-ref:compiler:transition_segment:tr_0023:segment:5@line:70\|enter_urban -> [*] : /urban_way_true effect { R45RouteToken = 23; };, element-ref:compiler:transition_segment:tr_0023:segment:6@line:84\|UrbanMode -> [*] : if [R45RouteToken == 23];, element-ref:compiler:transition_segment:tr_0023:segment:7@line:71\|lane_change_urban -> [*] : /urban_way_true effect { R45RouteToken = 23; };, element-ref:compiler:transition_segment:tr_0023:segment:8@line:72\|straight -> [*] : /urban_way_true effect { R45RouteToken = 23; };, element-ref:compiler:transition_segment:tr_0023:segment:9@line:73\|intersection -> [*] : /urban_way_true effect { R45RouteToken = 23; }; | compiler:route_control:R45RouteToken, compiler:transition_segment:tr_0023:segment:1, compiler:transition_segment:tr_0023:segment:10, compiler:transition_segment:tr_0023:segment:11, compiler:transition_segment:tr_0023:segment:12, compiler:transition_segment:tr_0023:segment:13, compiler:transition_segment:tr_0023:segment:14, compiler:transition_segment:tr_0023:segment:15, compiler:transition_segment:tr_0023:segment:16, compiler:transition_segment:tr_0023:segment:2, compiler:transition_segment:tr_0023:segment:3, compiler:transition_segment:tr_0023:segment:4, compiler:transition_segment:tr_0023:segment:5, compiler:transition_segment:tr_0023:segment:6, compiler:transition_segment:tr_0023:segment:7, compiler:transition_segment:tr_0023:segment:8, compiler:transition_segment:tr_0023:segment:9, source:transition:tr_0023 | Case 0039 multi_segment_macro occurrence review:multi_segment_macro:0009:tr_0023 binds exact source refs to working-contract elements compiler:route_control:R45RouteToken, compiler:transition_segment:tr_0023:segment:1, compiler:transition_segment:tr_0023:segment:10, compiler:transition_segment:tr_0023:segment:11, compiler:transition_segment:tr_0023:segment:12, compiler:transition_segment:tr_0023:segment:13, compiler:transition_segment:tr_0023:segment:14, compiler:transition_segment:tr_0023:segment:15, compiler:transition_segment:tr_0023:segment:16, compiler:transition_segment:tr_0023:segment:2, compiler:transition_segment:tr_0023:segment:3, compiler:transition_segment:tr_0023:segment:4, compiler:transition_segment:tr_0023:segment:5, compiler:transition_segment:tr_0023:segment:6, compiler:transition_segment:tr_0023:segment:7, compiler:transition_segment:tr_0023:segment:8, compiler:transition_segment:tr_0023:segment:9, source:transition:tr_0023. All emitted segments collapse to one source transition root; no segment is promoted as a separate authored transition or editable issue target. |
| `review:route_controller:0010:tr_0023` | `route_controller` | `compiler_artifact_excluded` | source-ref:llms_emp_feedback_final_0039.puml:line:22\|HighwayMode --> FinishState : auto_finished=true, source-ref:llms_emp_feedback_final_0039.puml:line:38\|UrbanMode --> FinishState : auto_finished=true, source-ref:llms_emp_feedback_final_0039.puml:line:41\|AutonomousMode --> HighwayMode : high_way=true, source-ref:llms_emp_feedback_final_0039.puml:line:42\|AutonomousMode --> UrbanMode : urban_way=true | element-ref:compiler:route_control:R45RouteToken@line:1\|def int R45RouteToken = 0;, element-ref:compiler:transition_segment:tr_0023:segment:10@line:74\|exit_urban -> [*] : /urban_way_true effect { R45RouteToken = 23; };, element-ref:compiler:transition_segment:tr_0023:segment:11@line:91\|InitialState -> [*] : /urban_way_true effect { R45RouteToken = 23; };, element-ref:compiler:transition_segment:tr_0023:segment:12@line:92\|FinishState -> [*] : /urban_way_true effect { R45RouteToken = 23; };, element-ref:compiler:transition_segment:tr_0023:segment:13@line:97\|AutonomousMode -> AutonomousMode : if [R45RouteToken == 23];, element-ref:compiler:transition_segment:tr_0023:segment:14@line:85\|[*] -> UrbanMode : if [R45RouteToken == 23] effect { R45RouteToken = 0; };, element-ref:compiler:transition_segment:tr_0023:segment:15@line:43\|FinalWaittr_0009 -> [*] : /urban_way_true effect { R45RouteToken = 23; };, element-ref:compiler:transition_segment:tr_0023:segment:16@line:44\|FinalWaittr_0010 -> [*] : /urban_way_true effect { R45RouteToken = 23; };, element-ref:compiler:transition_segment:tr_0023:segment:1@line:36\|enter_hwy -> [*] : /urban_way_true effect { R45RouteToken = 23; };, element-ref:compiler:transition_segment:tr_0023:segment:2@line:83\|HighwayMode -> [*] : if [R45RouteToken == 23];, element-ref:compiler:transition_segment:tr_0023:segment:3@line:37\|cruise -> [*] : /urban_way_true effect { R45RouteToken = 23; };, element-ref:compiler:transition_segment:tr_0023:segment:4@line:38\|lane_change -> [*] : /urban_way_true effect { R45RouteToken = 23; };, element-ref:compiler:transition_segment:tr_0023:segment:5@line:70\|enter_urban -> [*] : /urban_way_true effect { R45RouteToken = 23; };, element-ref:compiler:transition_segment:tr_0023:segment:6@line:84\|UrbanMode -> [*] : if [R45RouteToken == 23];, element-ref:compiler:transition_segment:tr_0023:segment:7@line:71\|lane_change_urban -> [*] : /urban_way_true effect { R45RouteToken = 23; };, element-ref:compiler:transition_segment:tr_0023:segment:8@line:72\|straight -> [*] : /urban_way_true effect { R45RouteToken = 23; };, element-ref:compiler:transition_segment:tr_0023:segment:9@line:73\|intersection -> [*] : /urban_way_true effect { R45RouteToken = 23; }; | compiler:route_control:R45RouteToken, compiler:transition_segment:tr_0023:segment:1, compiler:transition_segment:tr_0023:segment:10, compiler:transition_segment:tr_0023:segment:11, compiler:transition_segment:tr_0023:segment:12, compiler:transition_segment:tr_0023:segment:13, compiler:transition_segment:tr_0023:segment:14, compiler:transition_segment:tr_0023:segment:15, compiler:transition_segment:tr_0023:segment:16, compiler:transition_segment:tr_0023:segment:2, compiler:transition_segment:tr_0023:segment:3, compiler:transition_segment:tr_0023:segment:4, compiler:transition_segment:tr_0023:segment:5, compiler:transition_segment:tr_0023:segment:6, compiler:transition_segment:tr_0023:segment:7, compiler:transition_segment:tr_0023:segment:8, compiler:transition_segment:tr_0023:segment:9, source:transition:tr_0023 | Case 0039 route_controller occurrence review:route_controller:0010:tr_0023 binds exact source refs to working-contract elements compiler:route_control:R45RouteToken, compiler:transition_segment:tr_0023:segment:1, compiler:transition_segment:tr_0023:segment:10, compiler:transition_segment:tr_0023:segment:11, compiler:transition_segment:tr_0023:segment:12, compiler:transition_segment:tr_0023:segment:13, compiler:transition_segment:tr_0023:segment:14, compiler:transition_segment:tr_0023:segment:15, compiler:transition_segment:tr_0023:segment:16, compiler:transition_segment:tr_0023:segment:2, compiler:transition_segment:tr_0023:segment:3, compiler:transition_segment:tr_0023:segment:4, compiler:transition_segment:tr_0023:segment:5, compiler:transition_segment:tr_0023:segment:6, compiler:transition_segment:tr_0023:segment:7, compiler:transition_segment:tr_0023:segment:8, compiler:transition_segment:tr_0023:segment:9, source:transition:tr_0023. R45RouteToken and routed segments remain compiler_owned, protected, and excluded from confirmed issues, Repair, Confirm acceptance, and main results. |
| `review:synthetic_state:0011:001-FinalWaittr_0009` | `synthetic_state` | `compiler_artifact_excluded` | source-ref:llms_emp_feedback_final_0039.puml:line:16\|lane_change --> [*] : dist_to_exit<2 | element-ref:compiler:state:llms_emp_feedback_final_0039.AutonomousMode.HighwayMode.FinalWaittr_0009@line:21\|state FinalWaittr_0009 named "Completed final boundary: AutonomousMode.HighwayMode.lane_change"; | compiler:state:llms_emp_feedback_final_0039.AutonomousMode.HighwayMode.FinalWaittr_0009, source:transition:tr_0009 | Case 0039 synthetic_state occurrence review:synthetic_state:0011:001-FinalWaittr_0009 binds exact source refs to working-contract elements compiler:state:llms_emp_feedback_final_0039.AutonomousMode.HighwayMode.FinalWaittr_0009, source:transition:tr_0009. The placeholder makes the authored missing, invalid, or final boundary visible while the synthetic state itself remains a non-repairable compiler artifact. |
| `review:synthetic_state:0012:002-FinalWaittr_0010` | `synthetic_state` | `compiler_artifact_excluded` | source-ref:llms_emp_feedback_final_0039.puml:line:18\|cruise --> [*] : dist_to_exit<2 | element-ref:compiler:state:llms_emp_feedback_final_0039.AutonomousMode.HighwayMode.FinalWaittr_0010@line:22\|state FinalWaittr_0010 named "Completed final boundary: AutonomousMode.HighwayMode.cruise"; | compiler:state:llms_emp_feedback_final_0039.AutonomousMode.HighwayMode.FinalWaittr_0010, source:transition:tr_0010 | Case 0039 synthetic_state occurrence review:synthetic_state:0012:002-FinalWaittr_0010 binds exact source refs to working-contract elements compiler:state:llms_emp_feedback_final_0039.AutonomousMode.HighwayMode.FinalWaittr_0010, source:transition:tr_0010. The placeholder makes the authored missing, invalid, or final boundary visible while the synthetic state itself remains a non-repairable compiler artifact. |
| `review:explicit_concurrency:0013:001-multiple_initial_fanout` | `explicit_concurrency` | `capability_excluded` | source-ref:llms_emp_feedback_final_0039.puml:line:2\|[*] --> AutonomousMode, source-ref:llms_emp_feedback_final_0039.puml:line:44\|[*] --> collision_avoidance_deactive | element-ref:compiler:transition_segment:tr_0001:segment:1@line:98\|[*] -> AutonomousMode;, element-ref:compiler:transition_segment:tr_0024:segment:1@line:99\|[*] -> collision_avoidance_deactive; | source:transition:tr_0001, source:transition:tr_0024 | Case 0039 explicit_concurrency occurrence review:explicit_concurrency:0013:001-multiple_initial_fanout binds exact source refs to working-contract elements source:transition:tr_0001, source:transition:tr_0024. The authored fork, join, or fan-out occurrence remains source-visible, while unsupported concurrent execution is capability_excluded rather than guessed. |

## 作者阶段 lineage

| stage | output cell | present | output SHA-256 | feedback | resolved |
|---|---|---|---|---|---|
| `phase_i_generation` | `I41` | `true` | `187fb536bf88351c12f83f63d5b5d2bf1c096b0a99aa9089ce722ba07f2a0391` | - | - |
| `phase_ii_format` | `U41` | `false` | `-` | - | - |
| `phase_ii_grammar` | `Z41` | `false` | `-` | - | - |
| `phase_ii_semantic` | `AE41` | `true` | `187fb536bf88351c12f83f63d5b5d2bf1c096b0a99aa9089ce722ba07f2a0391` | None | - |

## Official identity ledger

- status：`aligned`
- canonical / official states：`15` / `15`
- aligned transition endpoints：`26`

本组 state identity 无需重映射。

本组 transition endpoint 无需重映射。

## Source normalization ledger

本组没有 source-input normalization。

## Concurrent region ledger

本组没有 PlantUML orthogonal/concurrent region separator。

## Operational debt

| reason code | count |
|---|---:|
| `R45.DEBT.composite_source_activation_dispatch` | 4 |
| `R45.DEBT.composite_source_external_reentry` | 2 |
| `R45.DEBT.multiple_initial_fanout` | 1 |
| `R45.DEBT.opaque_transition_label_semantics` | 20 |

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
[*] --> AutonomousMode

state AutonomousMode {
[*] --> InitialState

InitialState --> HighwayMode : high_way=true
InitialState --> UrbanMode : urban_way=true

state HighwayMode {
[*] --> enter_hwy

enter_hwy --> cruise
cruise --> lane_change : dist_to_front<25 && extra_lane=true
lane_change --> cruise : lane change completed
lane_change --> [*] : dist_to_exit<2

cruise --> [*] : dist_to_exit<2
cruise --> lane_change : dist_to_front<25 && extra_lane=true
}

HighwayMode --> FinishState : auto_finished=true

state UrbanMode {
[*] --> enter_urban

enter_urban --> lane_change_urban : dist_to_front<15 && extra_lane=true
enter_urban --> straight : road ahead is clear
enter_urban --> intersection : intersection=true

lane_change_urban --> straight : lane change complete
lane_change_urban --> exit_urban : dist_to_exit<0.7

straight --> intersection : intersection=true
straight --> lane_change_urban : dist_to_front<15 && extra_lane=true
}

UrbanMode --> FinishState : auto_finished=true
}

AutonomousMode --> HighwayMode : high_way=true
AutonomousMode --> UrbanMode : urban_way=true

[*] --> collision_avoidance_deactive

collision_avoidance_deactive --> collision_avoidance_active : pedestrian_detected || (dist_to_rear<5 && vel>30) || (dist_to_front<15 in HighwayMode || dist_to_front<10 in UrbanMode)

collision_avoidance_active --> collision_avoidance_deactive : front_inactive && rear_inactive && pedestrian_inactive

@enduml
```

## 转换后 FCSTM STM0

```fcstm
def int R45RouteToken = 0;
state llms_emp_feedback_final_0039 named "llms_emp_feedback_final_0039" {
    event high_way_true named "high_way=true";
    event urban_way_true named "urban_way=true";
    event dist_to_front_25_extra_lane_true named "dist_to_front<25 && extra_lane=true";
    event lane_change_completed named "lane change completed";
    event dist_to_exit_2 named "dist_to_exit<2";
    event auto_finished_true named "auto_finished=true";
    event dist_to_front_15_extra_lane_true named "dist_to_front<15 && extra_lane=true";
    event road_ahead_is_clear named "road ahead is clear";
    event intersection_true named "intersection=true";
    event lane_change_complete named "lane change complete";
    event dist_to_exit_0_7 named "dist_to_exit<0.7";
    event pedestrian_detected_dist_to_rear_5_vel_30_dist_to_front_15_in_HighwayMode_dist_to_front_10_in_UrbanMode named "pedestrian_detected || (dist_to_rear<5 && vel>30) || (dist_to_front<15 in HighwayMode || dist_to_front<10 in UrbanMode)";
    event front_inactive_rear_inactive_pedestrian_inactive named "front_inactive && rear_inactive && pedestrian_inactive";
    state AutonomousMode named "AutonomousMode" {
        state HighwayMode named "HighwayMode" {
            state enter_hwy named "enter_hwy";
            state cruise named "cruise";
            state lane_change named "lane_change";
            state FinalWaittr_0009 named "Completed final boundary: AutonomousMode.HighwayMode.lane_change";
            state FinalWaittr_0010 named "Completed final boundary: AutonomousMode.HighwayMode.cruise";
            [*] -> enter_hwy;
            enter_hwy -> cruise;
            cruise -> lane_change : /dist_to_front_25_extra_lane_true;
            lane_change -> cruise : /lane_change_completed;
            lane_change -> FinalWaittr_0009 : /dist_to_exit_2;
            cruise -> FinalWaittr_0010 : /dist_to_exit_2;
            cruise -> lane_change : /dist_to_front_25_extra_lane_true;
            enter_hwy -> [*] : /auto_finished_true effect { R45RouteToken = 12; };
            cruise -> [*] : /auto_finished_true effect { R45RouteToken = 12; };
            lane_change -> [*] : /auto_finished_true effect { R45RouteToken = 12; };
            enter_hwy -> [*] : /high_way_true effect { R45RouteToken = 22; };
            cruise -> [*] : /high_way_true effect { R45RouteToken = 22; };
            lane_change -> [*] : /high_way_true effect { R45RouteToken = 22; };
            enter_hwy -> [*] : /urban_way_true effect { R45RouteToken = 23; };
            cruise -> [*] : /urban_way_true effect { R45RouteToken = 23; };
            lane_change -> [*] : /urban_way_true effect { R45RouteToken = 23; };
            FinalWaittr_0009 -> [*] : /auto_finished_true effect { R45RouteToken = 12; };
            FinalWaittr_0010 -> [*] : /auto_finished_true effect { R45RouteToken = 12; };
            FinalWaittr_0009 -> [*] : /high_way_true effect { R45RouteToken = 22; };
            FinalWaittr_0010 -> [*] : /high_way_true effect { R45RouteToken = 22; };
            FinalWaittr_0009 -> [*] : /urban_way_true effect { R45RouteToken = 23; };
            FinalWaittr_0010 -> [*] : /urban_way_true effect { R45RouteToken = 23; };
        }
        state UrbanMode named "UrbanMode" {
            state enter_urban named "enter_urban";
            state lane_change_urban named "lane_change_urban";
            state straight named "straight";
            state intersection named "intersection";
            state exit_urban named "exit_urban";
            [*] -> enter_urban;
            enter_urban -> lane_change_urban : /dist_to_front_15_extra_lane_true;
            enter_urban -> straight : /road_ahead_is_clear;
            enter_urban -> intersection : /intersection_true;
            lane_change_urban -> straight : /lane_change_complete;
            lane_change_urban -> exit_urban : /dist_to_exit_0_7;
            straight -> intersection : /intersection_true;
            straight -> lane_change_urban : /dist_to_front_15_extra_lane_true;
            enter_urban -> [*] : /auto_finished_true effect { R45RouteToken = 21; };
            lane_change_urban -> [*] : /auto_finished_true effect { R45RouteToken = 21; };
            straight -> [*] : /auto_finished_true effect { R45RouteToken = 21; };
            intersection -> [*] : /auto_finished_true effect { R45RouteToken = 21; };
            exit_urban -> [*] : /auto_finished_true effect { R45RouteToken = 21; };
            enter_urban -> [*] : /high_way_true effect { R45RouteToken = 22; };
            lane_change_urban -> [*] : /high_way_true effect { R45RouteToken = 22; };
            straight -> [*] : /high_way_true effect { R45RouteToken = 22; };
            intersection -> [*] : /high_way_true effect { R45RouteToken = 22; };
            exit_urban -> [*] : /high_way_true effect { R45RouteToken = 22; };
            enter_urban -> [*] : /urban_way_true effect { R45RouteToken = 23; };
            lane_change_urban -> [*] : /urban_way_true effect { R45RouteToken = 23; };
            straight -> [*] : /urban_way_true effect { R45RouteToken = 23; };
            intersection -> [*] : /urban_way_true effect { R45RouteToken = 23; };
            exit_urban -> [*] : /urban_way_true effect { R45RouteToken = 23; };
        }
        state InitialState named "InitialState";
        state FinishState named "FinishState";
        HighwayMode -> FinishState : if [R45RouteToken == 12] effect { R45RouteToken = 0; };
        UrbanMode -> FinishState : if [R45RouteToken == 21] effect { R45RouteToken = 0; };
        HighwayMode -> [*] : if [R45RouteToken == 22];
        UrbanMode -> [*] : if [R45RouteToken == 22];
        [*] -> HighwayMode : if [R45RouteToken == 22] effect { R45RouteToken = 0; };
        HighwayMode -> [*] : if [R45RouteToken == 23];
        UrbanMode -> [*] : if [R45RouteToken == 23];
        [*] -> UrbanMode : if [R45RouteToken == 23] effect { R45RouteToken = 0; };
        [*] -> InitialState;
        InitialState -> HighwayMode : /high_way_true;
        InitialState -> UrbanMode : /urban_way_true;
        InitialState -> [*] : /high_way_true effect { R45RouteToken = 22; };
        FinishState -> [*] : /high_way_true effect { R45RouteToken = 22; };
        InitialState -> [*] : /urban_way_true effect { R45RouteToken = 23; };
        FinishState -> [*] : /urban_way_true effect { R45RouteToken = 23; };
    }
    state collision_avoidance_deactive named "collision_avoidance_deactive";
    state collision_avoidance_active named "collision_avoidance_active";
    AutonomousMode -> AutonomousMode : if [R45RouteToken == 22];
    AutonomousMode -> AutonomousMode : if [R45RouteToken == 23];
    [*] -> AutonomousMode;
    [*] -> collision_avoidance_deactive;
    collision_avoidance_deactive -> collision_avoidance_active : /pedestrian_detected_dist_to_rear_5_vel_30_dist_to_front_15_in_HighwayMode_dist_to_front_10_in_UrbanMode;
    collision_avoidance_active -> collision_avoidance_deactive : /front_inactive_rear_inactive_pedestrian_inactive;
}
```

[上一组 `0038`](../0038/README.md) | [返回 60 组索引](../../PAIR_INDEX.md) | [下一组 `0040`](../0040/README.md)
