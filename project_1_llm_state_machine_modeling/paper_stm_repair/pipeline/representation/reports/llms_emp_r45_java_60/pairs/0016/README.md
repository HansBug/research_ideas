# Pair `0016`：NL + PlantUML STM0 + FCSTM STM0

[上一组 `0015`](../0015/README.md) | [返回 60 组索引](../../PAIR_INDEX.md) | [下一组 `0017`](../0017/README.md)

- LLM：`GPT-4`
- 模型/场景：UAV swarm state machine diagram
- 作者输出阶段：`Result with Semantic Checking`
- 作者输出单元格：`AE18`；Excel row：`18`
- Phase-I fallback：`false`
- 相对 Phase-I 是否变化：`true`
- Phase-I PlantUML SHA-256：`2720cab7a2e9d2d06ff784d4e5821c4905c21408d19b0db0496b679394d06d50`
- NL SHA-256：`a01c022f5380700b6c13800497291640b4d64abbadce1d8984be0c14880ebeb3`
- PlantUML SHA-256：`a7bb3b61e3f044807c5a94d619979c859c49b36e852f429c58a4aae0d979b422`
- FCSTM SHA-256：`2a659fd52ce4d46ce1439dd428a32fe1e558c75206b1bb44ef2e28c8b5f4189d`
- review subject SHA-256：`d63342eca9d9c795d3bead4964c150a1955261ff5edabeae7a4bd289f91a3e8d`
- working contract SHA-256：`35a6bb56c2e9cd744213defe35c1e44e8284136460c34f189e4c54322de3632d`
- 结构裁决：`structure_preserved`
- source states / transitions：`9` / `14`
- mapped / blocked / silent drop：`14` / `0` / `0`
- final / lifecycle / body coverage：`1/1` / `0/0` / `0/0`
- concurrent region / separator coverage：`0/0` / `0/0`
- source normalization coverage：`0/0`
- official raw / validation：`state_diagram` / `state_diagram`
- official identity states / transitions：`9` / `14`
- official identity remaps：state `4` / transition endpoint `5`
- AST audit：`passed`
- legacy whole-model FCSTM execution / Discover：`false` / `false`
- working bundle usage gate：`discover_input_with_capability_mask`
- ownership source / compiler / agent：`23` / `46` / `0`
- source macro / positive identity trace / conversion boundary trace：`14` / `23` / `0`
- capability source-static / simulation / transition-trace：`eligible_with_exclusions` / `ineligible` / `ineligible`
- compiler-only diagnostic policy：`rejected_conversion_artifact`；main-result conversion artifact limit：`0`
- 主 session 对读：`pass`；ownership/macro/capability 均为 `pass`；Case 0016 passes the current attribution-safe forward review; this does not assert global behavior equivalence, and unsupported runtime semantics remain fail-closed.
- source anchors：`source-ref:llms_emp_feedback_final_0016.puml:line:4\|state SearchMission {, source-ref:llms_emp_feedback_final_0016.puml:line:9\|Search --> Region2 : Finished Region1 Search`；FCSTM anchors：`element-ref:source:state:SearchMission@line:11\|state SearchMission named "SearchMission" {, element-ref:compiler:transition_segment:tr_0004:segment:1@line:35\|Search -> Region2 : /Finished_Region1_Search;`
- 三个原始文件：[NL](./nl.txt) | [PlantUML](./plantuml.puml) | [FCSTM](./fcstm.fcstm)
- 审计入口：[canonical](../../canonical/llms_emp_feedback_final_0016.json) | [冻结 FCSTM](../../fcstm/llms_emp_feedback_final_0016.fcstm) | [case report](../../case_reports/llms_emp_feedback_final_0016.json) | [working contract](../../working_contracts/llms_emp_feedback_final_0016.json) | [source trace](../../source_traces/llms_emp_feedback_final_0016.json) | [人工总账](../../MANUAL_REVIEW.md)

## 主 session 三方语义对应

| projection | assessment | NL anchor | PlantUML anchor | FCSTM anchor | source roots | compiler members | rationale |
|---|---|---|---|---|---|---|---|
| `direct` | `preserved` | 1 This state machine model describes the state transitions of a UAV swarm. | source-ref:llms_emp_feedback_final_0016.puml:line:4\|state SearchMission { | element-ref:source:state:SearchMission@line:11\|state SearchMission named "SearchMission" { | source:state:SearchMission | - | Case 0016 binds source:state:SearchMission to authored PlantUML occurrence 'state SearchMission {' and current FCSTM occurrence 'state SearchMission named "SearchMission" {'; the source semantic root remains attributable while any compiler-owned projection stays protected and cannot become an independent Repair target. |
| `macro` | `preserved_with_exclusions` | search | source-ref:llms_emp_feedback_final_0016.puml:line:9\|Search --> Region2 : Finished Region1 Search | element-ref:compiler:transition_segment:tr_0004:segment:1@line:35\|Search -> Region2 : /Finished_Region1_Search; | source:transition:tr_0004 | compiler:transition_segment:tr_0004:segment:1 | Case 0016 binds source:transition:tr_0004 to authored PlantUML occurrence 'Search --> Region2 : Finished Region1 Search' and current FCSTM occurrence 'Search -> Region2 : /Finished_Region1_Search;'; the source semantic root remains attributable while any compiler-owned projection stays protected and cannot become an independent Repair target. |

## Risk occurrence 第二遍复核

| obligation | risk tag | assessment | PlantUML evidence | FCSTM evidence | ownership evidence | rationale |
|---|---|---|---|---|---|---|
| `review:official_identity_remap:0001:state-001` | `official_identity_remap` | `source_fact_preserved` | source-ref:llms_emp_feedback_final_0016.puml:line:12\|state Region2 { | element-ref:source:state:SearchMission.Region1.Region2@line:13\|state Region2 named "Region2" { | source:state:SearchMission.Region1.Region2 | Case 0016 official_identity_remap occurrence review:official_identity_remap:0001:state-001 binds exact source refs to working-contract elements source:state:SearchMission.Region1.Region2. The pinned PlantUML identity decision is preserved as a source fact and is not replaced by a lexical-scope guess from the converter. |
| `review:official_identity_remap:0002:state-002` | `official_identity_remap` | `source_fact_preserved` | source-ref:llms_emp_feedback_final_0016.puml:line:17\|state Region3 { | element-ref:source:state:SearchMission.Region1.Region2.Region3@line:14\|state Region3 named "Region3" { | source:state:SearchMission.Region1.Region2.Region3 | Case 0016 official_identity_remap occurrence review:official_identity_remap:0002:state-002 binds exact source refs to working-contract elements source:state:SearchMission.Region1.Region2.Region3. The pinned PlantUML identity decision is preserved as a source fact and is not replaced by a lexical-scope guess from the converter. |
| `review:official_identity_remap:0003:state-003` | `official_identity_remap` | `source_fact_preserved` | source-ref:llms_emp_feedback_final_0016.puml:line:13\|[*] --> Search, source-ref:llms_emp_feedback_final_0016.puml:line:18\|[*] --> Search | element-ref:source:state:SearchMission.Region1.Search@line:30\|state Search named "Search"; | source:state:SearchMission.Region1.Search | Case 0016 official_identity_remap occurrence review:official_identity_remap:0003:state-003 binds exact source refs to working-contract elements source:state:SearchMission.Region1.Search. The pinned PlantUML identity decision is preserved as a source fact and is not replaced by a lexical-scope guess from the converter. |
| `review:official_identity_remap:0004:state-004` | `official_identity_remap` | `source_fact_preserved` | source-ref:llms_emp_feedback_final_0016.puml:line:18\|[*] --> Search | element-ref:source:state:SearchMission.Region1.Search@line:30\|state Search named "Search"; | source:state:SearchMission.Region1.Search | Case 0016 official_identity_remap occurrence review:official_identity_remap:0004:state-004 binds exact source refs to working-contract elements source:state:SearchMission.Region1.Search. The pinned PlantUML identity decision is preserved as a source fact and is not replaced by a lexical-scope guess from the converter. |
| `review:official_identity_remap:0005:transition-001-tr_0004` | `official_identity_remap` | `source_fact_preserved` | source-ref:llms_emp_feedback_final_0016.puml:line:9\|Search --> Region2 : Finished Region1 Search | element-ref:compiler:transition_segment:tr_0004:segment:1@line:35\|Search -> Region2 : /Finished_Region1_Search; | source:transition:tr_0004 | Case 0016 official_identity_remap occurrence review:official_identity_remap:0005:transition-001-tr_0004 binds exact source refs to working-contract elements source:transition:tr_0004. The pinned PlantUML identity decision is preserved as a source fact and is not replaced by a lexical-scope guess from the converter. |
| `review:official_identity_remap:0006:transition-002-tr_0005` | `official_identity_remap` | `source_fact_preserved` | source-ref:llms_emp_feedback_final_0016.puml:line:13\|[*] --> Search | element-ref:compiler:state:llms_emp_feedback_final_0016.SearchMission.Region1.Region2.InvalidInitialtr_0005@line:20\|state InvalidInitialtr_0005 named "PlantUML initial target outside child scope: SearchMission.Region1.Search"; | source:transition:tr_0005 | Case 0016 official_identity_remap occurrence review:official_identity_remap:0006:transition-002-tr_0005 binds exact source refs to working-contract elements source:transition:tr_0005. The pinned PlantUML identity decision is preserved as a source fact and is not replaced by a lexical-scope guess from the converter. |
| `review:official_identity_remap:0007:transition-003-tr_0006` | `official_identity_remap` | `source_fact_preserved` | source-ref:llms_emp_feedback_final_0016.puml:line:14\|Search --> Region3 : Finished Region2 Search | element-ref:compiler:route_control:R45RouteToken@line:1\|def int R45RouteToken = 0; | source:transition:tr_0006 | Case 0016 official_identity_remap occurrence review:official_identity_remap:0007:transition-003-tr_0006 binds exact source refs to working-contract elements source:transition:tr_0006. The pinned PlantUML identity decision is preserved as a source fact and is not replaced by a lexical-scope guess from the converter. |
| `review:official_identity_remap:0008:transition-004-tr_0007` | `official_identity_remap` | `source_fact_preserved` | source-ref:llms_emp_feedback_final_0016.puml:line:18\|[*] --> Search | element-ref:compiler:state:llms_emp_feedback_final_0016.SearchMission.Region1.Region2.Region3.InvalidInitialtr_0007@line:15\|state InvalidInitialtr_0007 named "PlantUML initial target outside child scope: SearchMission.Region1.Search"; | source:transition:tr_0007 | Case 0016 official_identity_remap occurrence review:official_identity_remap:0008:transition-004-tr_0007 binds exact source refs to working-contract elements source:transition:tr_0007. The pinned PlantUML identity decision is preserved as a source fact and is not replaced by a lexical-scope guess from the converter. |
| `review:official_identity_remap:0009:transition-005-tr_0008` | `official_identity_remap` | `source_fact_preserved` | source-ref:llms_emp_feedback_final_0016.puml:line:19\|Search --> [*] : Finished Region3 Search | element-ref:compiler:state:llms_emp_feedback_final_0016.SearchMission.Region1.InvalidFinaltr_0008@line:31\|state InvalidFinaltr_0008 named "PlantUML final boundary outside source ancestry: @final:SearchMission.Region1.Region2.Region3"; | source:transition:tr_0008 | Case 0016 official_identity_remap occurrence review:official_identity_remap:0009:transition-005-tr_0008 binds exact source refs to working-contract elements source:transition:tr_0008. The pinned PlantUML identity decision is preserved as a source fact and is not replaced by a lexical-scope guess from the converter. |
| `review:multi_segment_macro:0010:tr_0006` | `multi_segment_macro` | `compiler_artifact_excluded` | source-ref:llms_emp_feedback_final_0016.puml:line:14\|Search --> Region3 : Finished Region2 Search, source-ref:llms_emp_feedback_final_0016.puml:line:23\|SearchMission --> FormationAdjust : Interception Detected, source-ref:llms_emp_feedback_final_0016.puml:line:27\|AdjustingFormation --> SearchMission : Finish Adjusting, source-ref:llms_emp_feedback_final_0016.puml:line:30\|SearchMission --> AttackState : Task Assignment Received, source-ref:llms_emp_feedback_final_0016.puml:line:34\|Attacking --> SearchMission : Attack Finished / Decrease UAV swarm count | element-ref:compiler:route_control:R45RouteToken@line:1\|def int R45RouteToken = 0;, element-ref:compiler:transition_segment:tr_0006:segment:1@line:36\|Search -> Region2 : /Finished_Region2_Search effect { R45RouteToken = 6; };, element-ref:compiler:transition_segment:tr_0006:segment:2@line:21\|[*] -> Region3 : if [R45RouteToken == 6] effect { R45RouteToken = 0; }; | compiler:route_control:R45RouteToken, compiler:transition_segment:tr_0006:segment:1, compiler:transition_segment:tr_0006:segment:2, source:transition:tr_0006 | Case 0016 multi_segment_macro occurrence review:multi_segment_macro:0010:tr_0006 binds exact source refs to working-contract elements compiler:route_control:R45RouteToken, compiler:transition_segment:tr_0006:segment:1, compiler:transition_segment:tr_0006:segment:2, source:transition:tr_0006. All emitted segments collapse to one source transition root; no segment is promoted as a separate authored transition or editable issue target. |
| `review:route_controller:0011:tr_0006` | `route_controller` | `compiler_artifact_excluded` | source-ref:llms_emp_feedback_final_0016.puml:line:14\|Search --> Region3 : Finished Region2 Search, source-ref:llms_emp_feedback_final_0016.puml:line:23\|SearchMission --> FormationAdjust : Interception Detected, source-ref:llms_emp_feedback_final_0016.puml:line:27\|AdjustingFormation --> SearchMission : Finish Adjusting, source-ref:llms_emp_feedback_final_0016.puml:line:30\|SearchMission --> AttackState : Task Assignment Received, source-ref:llms_emp_feedback_final_0016.puml:line:34\|Attacking --> SearchMission : Attack Finished / Decrease UAV swarm count | element-ref:compiler:route_control:R45RouteToken@line:1\|def int R45RouteToken = 0;, element-ref:compiler:transition_segment:tr_0006:segment:1@line:36\|Search -> Region2 : /Finished_Region2_Search effect { R45RouteToken = 6; };, element-ref:compiler:transition_segment:tr_0006:segment:2@line:21\|[*] -> Region3 : if [R45RouteToken == 6] effect { R45RouteToken = 0; }; | compiler:route_control:R45RouteToken, compiler:transition_segment:tr_0006:segment:1, compiler:transition_segment:tr_0006:segment:2, source:transition:tr_0006 | Case 0016 route_controller occurrence review:route_controller:0011:tr_0006 binds exact source refs to working-contract elements compiler:route_control:R45RouteToken, compiler:transition_segment:tr_0006:segment:1, compiler:transition_segment:tr_0006:segment:2, source:transition:tr_0006. R45RouteToken and routed segments remain compiler_owned, protected, and excluded from confirmed issues, Repair, Confirm acceptance, and main results. |
| `review:final_boundary:0012:tr_0008` | `final_boundary` | `source_fact_preserved` | source-ref:llms_emp_feedback_final_0016.puml:line:19\|Search --> [*] : Finished Region3 Search | element-ref:compiler:state:llms_emp_feedback_final_0016.SearchMission.Region1.InvalidFinaltr_0008@line:31\|state InvalidFinaltr_0008 named "PlantUML final boundary outside source ancestry: @final:SearchMission.Region1.Region2.Region3";, element-ref:compiler:transition_segment:tr_0008:segment:1@line:37\|Search -> InvalidFinaltr_0008 : /Finished_Region3_Search; | compiler:state:llms_emp_feedback_final_0016.SearchMission.Region1.InvalidFinaltr_0008, compiler:transition_segment:tr_0008:segment:1, source:transition:tr_0008 | Case 0016 final_boundary occurrence review:final_boundary:0012:tr_0008 binds exact source refs to working-contract elements compiler:state:llms_emp_feedback_final_0016.SearchMission.Region1.InvalidFinaltr_0008, compiler:transition_segment:tr_0008:segment:1, source:transition:tr_0008. The authored final occurrence remains visible through its source root; any completion holder or routing segment is excluded from source-level claims. |
| `review:multi_segment_macro:0013:tr_0009` | `multi_segment_macro` | `compiler_artifact_excluded` | source-ref:llms_emp_feedback_final_0016.puml:line:14\|Search --> Region3 : Finished Region2 Search, source-ref:llms_emp_feedback_final_0016.puml:line:23\|SearchMission --> FormationAdjust : Interception Detected, source-ref:llms_emp_feedback_final_0016.puml:line:27\|AdjustingFormation --> SearchMission : Finish Adjusting, source-ref:llms_emp_feedback_final_0016.puml:line:30\|SearchMission --> AttackState : Task Assignment Received, source-ref:llms_emp_feedback_final_0016.puml:line:34\|Attacking --> SearchMission : Attack Finished / Decrease UAV swarm count | element-ref:compiler:route_control:R45RouteToken@line:1\|def int R45RouteToken = 0;, element-ref:compiler:transition_segment:tr_0009:segment:1@line:25\|Region3 -> [*] : /Interception_Detected effect { R45RouteToken = 9; };, element-ref:compiler:transition_segment:tr_0009:segment:2@line:32\|Region2 -> [*] : if [R45RouteToken == 9];, element-ref:compiler:transition_segment:tr_0009:segment:3@line:43\|Region1 -> [*] : if [R45RouteToken == 9];, element-ref:compiler:transition_segment:tr_0009:segment:4@line:38\|Search -> [*] : /Interception_Detected effect { R45RouteToken = 9; };, element-ref:compiler:transition_segment:tr_0009:segment:5@line:57\|SearchMission -> FormationAdjust : if [R45RouteToken == 9] effect { R45RouteToken = 0; };, element-ref:compiler:transition_segment:tr_0009:segment:6@line:27\|InvalidInitialtr_0005 -> [*] : /Interception_Detected effect { R45RouteToken = 9; };, element-ref:compiler:transition_segment:tr_0009:segment:7@line:17\|InvalidInitialtr_0007 -> [*] : /Interception_Detected effect { R45RouteToken = 9; };, element-ref:compiler:transition_segment:tr_0009:segment:8@line:22\|Region3 -> [*] : if [R45RouteToken == 9];, element-ref:compiler:transition_segment:tr_0009:segment:9@line:40\|InvalidFinaltr_0008 -> [*] : /Interception_Detected effect { R45RouteToken = 9; }; | compiler:route_control:R45RouteToken, compiler:transition_segment:tr_0009:segment:1, compiler:transition_segment:tr_0009:segment:2, compiler:transition_segment:tr_0009:segment:3, compiler:transition_segment:tr_0009:segment:4, compiler:transition_segment:tr_0009:segment:5, compiler:transition_segment:tr_0009:segment:6, compiler:transition_segment:tr_0009:segment:7, compiler:transition_segment:tr_0009:segment:8, compiler:transition_segment:tr_0009:segment:9, source:transition:tr_0009 | Case 0016 multi_segment_macro occurrence review:multi_segment_macro:0013:tr_0009 binds exact source refs to working-contract elements compiler:route_control:R45RouteToken, compiler:transition_segment:tr_0009:segment:1, compiler:transition_segment:tr_0009:segment:2, compiler:transition_segment:tr_0009:segment:3, compiler:transition_segment:tr_0009:segment:4, compiler:transition_segment:tr_0009:segment:5, compiler:transition_segment:tr_0009:segment:6, compiler:transition_segment:tr_0009:segment:7, compiler:transition_segment:tr_0009:segment:8, compiler:transition_segment:tr_0009:segment:9, source:transition:tr_0009. All emitted segments collapse to one source transition root; no segment is promoted as a separate authored transition or editable issue target. |
| `review:route_controller:0014:tr_0009` | `route_controller` | `compiler_artifact_excluded` | source-ref:llms_emp_feedback_final_0016.puml:line:14\|Search --> Region3 : Finished Region2 Search, source-ref:llms_emp_feedback_final_0016.puml:line:23\|SearchMission --> FormationAdjust : Interception Detected, source-ref:llms_emp_feedback_final_0016.puml:line:27\|AdjustingFormation --> SearchMission : Finish Adjusting, source-ref:llms_emp_feedback_final_0016.puml:line:30\|SearchMission --> AttackState : Task Assignment Received, source-ref:llms_emp_feedback_final_0016.puml:line:34\|Attacking --> SearchMission : Attack Finished / Decrease UAV swarm count | element-ref:compiler:route_control:R45RouteToken@line:1\|def int R45RouteToken = 0;, element-ref:compiler:transition_segment:tr_0009:segment:1@line:25\|Region3 -> [*] : /Interception_Detected effect { R45RouteToken = 9; };, element-ref:compiler:transition_segment:tr_0009:segment:2@line:32\|Region2 -> [*] : if [R45RouteToken == 9];, element-ref:compiler:transition_segment:tr_0009:segment:3@line:43\|Region1 -> [*] : if [R45RouteToken == 9];, element-ref:compiler:transition_segment:tr_0009:segment:4@line:38\|Search -> [*] : /Interception_Detected effect { R45RouteToken = 9; };, element-ref:compiler:transition_segment:tr_0009:segment:5@line:57\|SearchMission -> FormationAdjust : if [R45RouteToken == 9] effect { R45RouteToken = 0; };, element-ref:compiler:transition_segment:tr_0009:segment:6@line:27\|InvalidInitialtr_0005 -> [*] : /Interception_Detected effect { R45RouteToken = 9; };, element-ref:compiler:transition_segment:tr_0009:segment:7@line:17\|InvalidInitialtr_0007 -> [*] : /Interception_Detected effect { R45RouteToken = 9; };, element-ref:compiler:transition_segment:tr_0009:segment:8@line:22\|Region3 -> [*] : if [R45RouteToken == 9];, element-ref:compiler:transition_segment:tr_0009:segment:9@line:40\|InvalidFinaltr_0008 -> [*] : /Interception_Detected effect { R45RouteToken = 9; }; | compiler:route_control:R45RouteToken, compiler:transition_segment:tr_0009:segment:1, compiler:transition_segment:tr_0009:segment:2, compiler:transition_segment:tr_0009:segment:3, compiler:transition_segment:tr_0009:segment:4, compiler:transition_segment:tr_0009:segment:5, compiler:transition_segment:tr_0009:segment:6, compiler:transition_segment:tr_0009:segment:7, compiler:transition_segment:tr_0009:segment:8, compiler:transition_segment:tr_0009:segment:9, source:transition:tr_0009 | Case 0016 route_controller occurrence review:route_controller:0014:tr_0009 binds exact source refs to working-contract elements compiler:route_control:R45RouteToken, compiler:transition_segment:tr_0009:segment:1, compiler:transition_segment:tr_0009:segment:2, compiler:transition_segment:tr_0009:segment:3, compiler:transition_segment:tr_0009:segment:4, compiler:transition_segment:tr_0009:segment:5, compiler:transition_segment:tr_0009:segment:6, compiler:transition_segment:tr_0009:segment:7, compiler:transition_segment:tr_0009:segment:8, compiler:transition_segment:tr_0009:segment:9, source:transition:tr_0009. R45RouteToken and routed segments remain compiler_owned, protected, and excluded from confirmed issues, Repair, Confirm acceptance, and main results. |
| `review:multi_segment_macro:0015:tr_0011` | `multi_segment_macro` | `compiler_artifact_excluded` | source-ref:llms_emp_feedback_final_0016.puml:line:14\|Search --> Region3 : Finished Region2 Search, source-ref:llms_emp_feedback_final_0016.puml:line:23\|SearchMission --> FormationAdjust : Interception Detected, source-ref:llms_emp_feedback_final_0016.puml:line:27\|AdjustingFormation --> SearchMission : Finish Adjusting, source-ref:llms_emp_feedback_final_0016.puml:line:30\|SearchMission --> AttackState : Task Assignment Received, source-ref:llms_emp_feedback_final_0016.puml:line:34\|Attacking --> SearchMission : Attack Finished / Decrease UAV swarm count | element-ref:compiler:route_control:R45RouteToken@line:1\|def int R45RouteToken = 0;, element-ref:compiler:transition_segment:tr_0011:segment:1@line:50\|AdjustingFormation -> [*] : /Finish_Adjusting effect { R45RouteToken = 11; };, element-ref:compiler:transition_segment:tr_0011:segment:2@line:58\|FormationAdjust -> SearchMission : if [R45RouteToken == 11] effect { R45RouteToken = 0; }; | compiler:route_control:R45RouteToken, compiler:transition_segment:tr_0011:segment:1, compiler:transition_segment:tr_0011:segment:2, source:transition:tr_0011 | Case 0016 multi_segment_macro occurrence review:multi_segment_macro:0015:tr_0011 binds exact source refs to working-contract elements compiler:route_control:R45RouteToken, compiler:transition_segment:tr_0011:segment:1, compiler:transition_segment:tr_0011:segment:2, source:transition:tr_0011. All emitted segments collapse to one source transition root; no segment is promoted as a separate authored transition or editable issue target. |
| `review:route_controller:0016:tr_0011` | `route_controller` | `compiler_artifact_excluded` | source-ref:llms_emp_feedback_final_0016.puml:line:14\|Search --> Region3 : Finished Region2 Search, source-ref:llms_emp_feedback_final_0016.puml:line:23\|SearchMission --> FormationAdjust : Interception Detected, source-ref:llms_emp_feedback_final_0016.puml:line:27\|AdjustingFormation --> SearchMission : Finish Adjusting, source-ref:llms_emp_feedback_final_0016.puml:line:30\|SearchMission --> AttackState : Task Assignment Received, source-ref:llms_emp_feedback_final_0016.puml:line:34\|Attacking --> SearchMission : Attack Finished / Decrease UAV swarm count | element-ref:compiler:route_control:R45RouteToken@line:1\|def int R45RouteToken = 0;, element-ref:compiler:transition_segment:tr_0011:segment:1@line:50\|AdjustingFormation -> [*] : /Finish_Adjusting effect { R45RouteToken = 11; };, element-ref:compiler:transition_segment:tr_0011:segment:2@line:58\|FormationAdjust -> SearchMission : if [R45RouteToken == 11] effect { R45RouteToken = 0; }; | compiler:route_control:R45RouteToken, compiler:transition_segment:tr_0011:segment:1, compiler:transition_segment:tr_0011:segment:2, source:transition:tr_0011 | Case 0016 route_controller occurrence review:route_controller:0016:tr_0011 binds exact source refs to working-contract elements compiler:route_control:R45RouteToken, compiler:transition_segment:tr_0011:segment:1, compiler:transition_segment:tr_0011:segment:2, source:transition:tr_0011. R45RouteToken and routed segments remain compiler_owned, protected, and excluded from confirmed issues, Repair, Confirm acceptance, and main results. |
| `review:multi_segment_macro:0017:tr_0012` | `multi_segment_macro` | `compiler_artifact_excluded` | source-ref:llms_emp_feedback_final_0016.puml:line:14\|Search --> Region3 : Finished Region2 Search, source-ref:llms_emp_feedback_final_0016.puml:line:23\|SearchMission --> FormationAdjust : Interception Detected, source-ref:llms_emp_feedback_final_0016.puml:line:27\|AdjustingFormation --> SearchMission : Finish Adjusting, source-ref:llms_emp_feedback_final_0016.puml:line:30\|SearchMission --> AttackState : Task Assignment Received, source-ref:llms_emp_feedback_final_0016.puml:line:34\|Attacking --> SearchMission : Attack Finished / Decrease UAV swarm count | element-ref:compiler:route_control:R45RouteToken@line:1\|def int R45RouteToken = 0;, element-ref:compiler:transition_segment:tr_0012:segment:1@line:26\|Region3 -> [*] : /Task_Assignment_Received effect { R45RouteToken = 12; };, element-ref:compiler:transition_segment:tr_0012:segment:2@line:33\|Region2 -> [*] : if [R45RouteToken == 12];, element-ref:compiler:transition_segment:tr_0012:segment:3@line:44\|Region1 -> [*] : if [R45RouteToken == 12];, element-ref:compiler:transition_segment:tr_0012:segment:4@line:39\|Search -> [*] : /Task_Assignment_Received effect { R45RouteToken = 12; };, element-ref:compiler:transition_segment:tr_0012:segment:5@line:59\|SearchMission -> AttackState : if [R45RouteToken == 12] effect { R45RouteToken = 0; };, element-ref:compiler:transition_segment:tr_0012:segment:6@line:28\|InvalidInitialtr_0005 -> [*] : /Task_Assignment_Received effect { R45RouteToken = 12; };, element-ref:compiler:transition_segment:tr_0012:segment:7@line:18\|InvalidInitialtr_0007 -> [*] : /Task_Assignment_Received effect { R45RouteToken = 12; };, element-ref:compiler:transition_segment:tr_0012:segment:8@line:23\|Region3 -> [*] : if [R45RouteToken == 12];, element-ref:compiler:transition_segment:tr_0012:segment:9@line:41\|InvalidFinaltr_0008 -> [*] : /Task_Assignment_Received effect { R45RouteToken = 12; }; | compiler:route_control:R45RouteToken, compiler:transition_segment:tr_0012:segment:1, compiler:transition_segment:tr_0012:segment:2, compiler:transition_segment:tr_0012:segment:3, compiler:transition_segment:tr_0012:segment:4, compiler:transition_segment:tr_0012:segment:5, compiler:transition_segment:tr_0012:segment:6, compiler:transition_segment:tr_0012:segment:7, compiler:transition_segment:tr_0012:segment:8, compiler:transition_segment:tr_0012:segment:9, source:transition:tr_0012 | Case 0016 multi_segment_macro occurrence review:multi_segment_macro:0017:tr_0012 binds exact source refs to working-contract elements compiler:route_control:R45RouteToken, compiler:transition_segment:tr_0012:segment:1, compiler:transition_segment:tr_0012:segment:2, compiler:transition_segment:tr_0012:segment:3, compiler:transition_segment:tr_0012:segment:4, compiler:transition_segment:tr_0012:segment:5, compiler:transition_segment:tr_0012:segment:6, compiler:transition_segment:tr_0012:segment:7, compiler:transition_segment:tr_0012:segment:8, compiler:transition_segment:tr_0012:segment:9, source:transition:tr_0012. All emitted segments collapse to one source transition root; no segment is promoted as a separate authored transition or editable issue target. |
| `review:route_controller:0018:tr_0012` | `route_controller` | `compiler_artifact_excluded` | source-ref:llms_emp_feedback_final_0016.puml:line:14\|Search --> Region3 : Finished Region2 Search, source-ref:llms_emp_feedback_final_0016.puml:line:23\|SearchMission --> FormationAdjust : Interception Detected, source-ref:llms_emp_feedback_final_0016.puml:line:27\|AdjustingFormation --> SearchMission : Finish Adjusting, source-ref:llms_emp_feedback_final_0016.puml:line:30\|SearchMission --> AttackState : Task Assignment Received, source-ref:llms_emp_feedback_final_0016.puml:line:34\|Attacking --> SearchMission : Attack Finished / Decrease UAV swarm count | element-ref:compiler:route_control:R45RouteToken@line:1\|def int R45RouteToken = 0;, element-ref:compiler:transition_segment:tr_0012:segment:1@line:26\|Region3 -> [*] : /Task_Assignment_Received effect { R45RouteToken = 12; };, element-ref:compiler:transition_segment:tr_0012:segment:2@line:33\|Region2 -> [*] : if [R45RouteToken == 12];, element-ref:compiler:transition_segment:tr_0012:segment:3@line:44\|Region1 -> [*] : if [R45RouteToken == 12];, element-ref:compiler:transition_segment:tr_0012:segment:4@line:39\|Search -> [*] : /Task_Assignment_Received effect { R45RouteToken = 12; };, element-ref:compiler:transition_segment:tr_0012:segment:5@line:59\|SearchMission -> AttackState : if [R45RouteToken == 12] effect { R45RouteToken = 0; };, element-ref:compiler:transition_segment:tr_0012:segment:6@line:28\|InvalidInitialtr_0005 -> [*] : /Task_Assignment_Received effect { R45RouteToken = 12; };, element-ref:compiler:transition_segment:tr_0012:segment:7@line:18\|InvalidInitialtr_0007 -> [*] : /Task_Assignment_Received effect { R45RouteToken = 12; };, element-ref:compiler:transition_segment:tr_0012:segment:8@line:23\|Region3 -> [*] : if [R45RouteToken == 12];, element-ref:compiler:transition_segment:tr_0012:segment:9@line:41\|InvalidFinaltr_0008 -> [*] : /Task_Assignment_Received effect { R45RouteToken = 12; }; | compiler:route_control:R45RouteToken, compiler:transition_segment:tr_0012:segment:1, compiler:transition_segment:tr_0012:segment:2, compiler:transition_segment:tr_0012:segment:3, compiler:transition_segment:tr_0012:segment:4, compiler:transition_segment:tr_0012:segment:5, compiler:transition_segment:tr_0012:segment:6, compiler:transition_segment:tr_0012:segment:7, compiler:transition_segment:tr_0012:segment:8, compiler:transition_segment:tr_0012:segment:9, source:transition:tr_0012 | Case 0016 route_controller occurrence review:route_controller:0018:tr_0012 binds exact source refs to working-contract elements compiler:route_control:R45RouteToken, compiler:transition_segment:tr_0012:segment:1, compiler:transition_segment:tr_0012:segment:2, compiler:transition_segment:tr_0012:segment:3, compiler:transition_segment:tr_0012:segment:4, compiler:transition_segment:tr_0012:segment:5, compiler:transition_segment:tr_0012:segment:6, compiler:transition_segment:tr_0012:segment:7, compiler:transition_segment:tr_0012:segment:8, compiler:transition_segment:tr_0012:segment:9, source:transition:tr_0012. R45RouteToken and routed segments remain compiler_owned, protected, and excluded from confirmed issues, Repair, Confirm acceptance, and main results. |
| `review:multi_segment_macro:0019:tr_0014` | `multi_segment_macro` | `compiler_artifact_excluded` | source-ref:llms_emp_feedback_final_0016.puml:line:14\|Search --> Region3 : Finished Region2 Search, source-ref:llms_emp_feedback_final_0016.puml:line:23\|SearchMission --> FormationAdjust : Interception Detected, source-ref:llms_emp_feedback_final_0016.puml:line:27\|AdjustingFormation --> SearchMission : Finish Adjusting, source-ref:llms_emp_feedback_final_0016.puml:line:30\|SearchMission --> AttackState : Task Assignment Received, source-ref:llms_emp_feedback_final_0016.puml:line:34\|Attacking --> SearchMission : Attack Finished / Decrease UAV swarm count | element-ref:compiler:route_control:R45RouteToken@line:1\|def int R45RouteToken = 0;, element-ref:compiler:transition_segment:tr_0014:segment:1@line:55\|Attacking -> [*] : /Attack_Finished_Decrease_UAV_swarm_count effect { R45RouteToken = 14; };, element-ref:compiler:transition_segment:tr_0014:segment:2@line:60\|AttackState -> SearchMission : if [R45RouteToken == 14] effect { R45RouteToken = 0; }; | compiler:route_control:R45RouteToken, compiler:transition_segment:tr_0014:segment:1, compiler:transition_segment:tr_0014:segment:2, source:transition:tr_0014 | Case 0016 multi_segment_macro occurrence review:multi_segment_macro:0019:tr_0014 binds exact source refs to working-contract elements compiler:route_control:R45RouteToken, compiler:transition_segment:tr_0014:segment:1, compiler:transition_segment:tr_0014:segment:2, source:transition:tr_0014. All emitted segments collapse to one source transition root; no segment is promoted as a separate authored transition or editable issue target. |
| `review:route_controller:0020:tr_0014` | `route_controller` | `compiler_artifact_excluded` | source-ref:llms_emp_feedback_final_0016.puml:line:14\|Search --> Region3 : Finished Region2 Search, source-ref:llms_emp_feedback_final_0016.puml:line:23\|SearchMission --> FormationAdjust : Interception Detected, source-ref:llms_emp_feedback_final_0016.puml:line:27\|AdjustingFormation --> SearchMission : Finish Adjusting, source-ref:llms_emp_feedback_final_0016.puml:line:30\|SearchMission --> AttackState : Task Assignment Received, source-ref:llms_emp_feedback_final_0016.puml:line:34\|Attacking --> SearchMission : Attack Finished / Decrease UAV swarm count | element-ref:compiler:route_control:R45RouteToken@line:1\|def int R45RouteToken = 0;, element-ref:compiler:transition_segment:tr_0014:segment:1@line:55\|Attacking -> [*] : /Attack_Finished_Decrease_UAV_swarm_count effect { R45RouteToken = 14; };, element-ref:compiler:transition_segment:tr_0014:segment:2@line:60\|AttackState -> SearchMission : if [R45RouteToken == 14] effect { R45RouteToken = 0; }; | compiler:route_control:R45RouteToken, compiler:transition_segment:tr_0014:segment:1, compiler:transition_segment:tr_0014:segment:2, source:transition:tr_0014 | Case 0016 route_controller occurrence review:route_controller:0020:tr_0014 binds exact source refs to working-contract elements compiler:route_control:R45RouteToken, compiler:transition_segment:tr_0014:segment:1, compiler:transition_segment:tr_0014:segment:2, source:transition:tr_0014. R45RouteToken and routed segments remain compiler_owned, protected, and excluded from confirmed issues, Repair, Confirm acceptance, and main results. |
| `review:synthetic_state:0021:001-InvalidInitialtr_0005` | `synthetic_state` | `compiler_artifact_excluded` | source-ref:llms_emp_feedback_final_0016.puml:line:13\|[*] --> Search | element-ref:compiler:state:llms_emp_feedback_final_0016.SearchMission.Region1.Region2.InvalidInitialtr_0005@line:20\|state InvalidInitialtr_0005 named "PlantUML initial target outside child scope: SearchMission.Region1.Search"; | compiler:state:llms_emp_feedback_final_0016.SearchMission.Region1.Region2.InvalidInitialtr_0005, source:transition:tr_0005 | Case 0016 synthetic_state occurrence review:synthetic_state:0021:001-InvalidInitialtr_0005 binds exact source refs to working-contract elements compiler:state:llms_emp_feedback_final_0016.SearchMission.Region1.Region2.InvalidInitialtr_0005, source:transition:tr_0005. The placeholder makes the authored missing, invalid, or final boundary visible while the synthetic state itself remains a non-repairable compiler artifact. |
| `review:synthetic_state:0022:002-InvalidInitialtr_0007` | `synthetic_state` | `compiler_artifact_excluded` | source-ref:llms_emp_feedback_final_0016.puml:line:18\|[*] --> Search | element-ref:compiler:state:llms_emp_feedback_final_0016.SearchMission.Region1.Region2.Region3.InvalidInitialtr_0007@line:15\|state InvalidInitialtr_0007 named "PlantUML initial target outside child scope: SearchMission.Region1.Search"; | compiler:state:llms_emp_feedback_final_0016.SearchMission.Region1.Region2.Region3.InvalidInitialtr_0007, source:transition:tr_0007 | Case 0016 synthetic_state occurrence review:synthetic_state:0022:002-InvalidInitialtr_0007 binds exact source refs to working-contract elements compiler:state:llms_emp_feedback_final_0016.SearchMission.Region1.Region2.Region3.InvalidInitialtr_0007, source:transition:tr_0007. The placeholder makes the authored missing, invalid, or final boundary visible while the synthetic state itself remains a non-repairable compiler artifact. |
| `review:synthetic_state:0023:003-InvalidFinaltr_0008` | `synthetic_state` | `compiler_artifact_excluded` | source-ref:llms_emp_feedback_final_0016.puml:line:19\|Search --> [*] : Finished Region3 Search | element-ref:compiler:state:llms_emp_feedback_final_0016.SearchMission.Region1.InvalidFinaltr_0008@line:31\|state InvalidFinaltr_0008 named "PlantUML final boundary outside source ancestry: @final:SearchMission.Region1.Region2.Region3"; | compiler:state:llms_emp_feedback_final_0016.SearchMission.Region1.InvalidFinaltr_0008, source:transition:tr_0008 | Case 0016 synthetic_state occurrence review:synthetic_state:0023:003-InvalidFinaltr_0008 binds exact source refs to working-contract elements compiler:state:llms_emp_feedback_final_0016.SearchMission.Region1.InvalidFinaltr_0008, source:transition:tr_0008. The placeholder makes the authored missing, invalid, or final boundary visible while the synthetic state itself remains a non-repairable compiler artifact. |

## 作者阶段 lineage

| stage | output cell | present | output SHA-256 | feedback | resolved |
|---|---|---|---|---|---|
| `phase_i_generation` | `I18` | `true` | `2720cab7a2e9d2d06ff784d4e5821c4905c21408d19b0db0496b679394d06d50` | - | - |
| `phase_ii_format` | `U18` | `false` | `-` | - | - |
| `phase_ii_grammar` | `Z18` | `false` | `-` | - | - |
| `phase_ii_semantic` | `AE18` | `true` | `a7bb3b61e3f044807c5a94d619979c859c49b36e852f429c58a4aae0d979b422` | missing regions | - |

## Official identity ledger

- status：`aligned`
- canonical / official states：`9` / `9`
- aligned transition endpoints：`14`

| source-parser identity | pinned PlantUML identity | raw ref | reason |
|---|---|---|---|
| `SearchMission.Region2` | `SearchMission.Region1.Region2` | `llms_emp_feedback_final_0016.puml:line:12` | `official_link_endpoint_identity` |
| `SearchMission.Region3` | `SearchMission.Region1.Region2.Region3` | `llms_emp_feedback_final_0016.puml:line:17` | `official_link_endpoint_identity` |
| `SearchMission.Region2.Search` | `SearchMission.Region1.Search` | `llms_emp_feedback_final_0016.puml:line:13` | `official_link_endpoint_identity` |
| `SearchMission.Region3.Search` | `SearchMission.Region1.Search` | `llms_emp_feedback_final_0016.puml:line:18` | `official_link_endpoint_identity` |

| transition | source before -> after | target before -> after | raw ref |
|---|---|---|---|
| `tr_0004` | `SearchMission.Region1.Search` -> `SearchMission.Region1.Search` | `SearchMission.Region2` -> `SearchMission.Region1.Region2` | `llms_emp_feedback_final_0016.puml:line:9` |
| `tr_0005` | `@initial:SearchMission.Region2` -> `@initial:SearchMission.Region1.Region2` | `SearchMission.Region2.Search` -> `SearchMission.Region1.Search` | `llms_emp_feedback_final_0016.puml:line:13` |
| `tr_0006` | `SearchMission.Region2.Search` -> `SearchMission.Region1.Search` | `SearchMission.Region3` -> `SearchMission.Region1.Region2.Region3` | `llms_emp_feedback_final_0016.puml:line:14` |
| `tr_0007` | `@initial:SearchMission.Region3` -> `@initial:SearchMission.Region1.Region2.Region3` | `SearchMission.Region3.Search` -> `SearchMission.Region1.Search` | `llms_emp_feedback_final_0016.puml:line:18` |
| `tr_0008` | `SearchMission.Region3.Search` -> `SearchMission.Region1.Search` | `@final:SearchMission.Region3` -> `@final:SearchMission.Region1.Region2.Region3` | `llms_emp_feedback_final_0016.puml:line:19` |

## Source normalization ledger

本组没有 source-input normalization。

## Concurrent region ledger

本组没有 PlantUML orthogonal/concurrent region separator。

## Operational debt

| reason code | count |
|---|---:|
| `R45.DEBT.composite_source_activation_dispatch` | 2 |
| `R45.DEBT.invalid_source_final_scope` | 1 |
| `R45.DEBT.invalid_source_initial_target` | 2 |
| `R45.DEBT.opaque_transition_label_semantics` | 8 |

## NL

```text
1 This state machine model describes the state transitions of a UAV swarm.
2 Before the mission is completed, the UAV swarm continuously performs target search tasks, during which it operates within three different state areas.
3 When the UAV swarm is intercepted, it transitions to the formation adjustment state.
4 During flight, if task assignment information is received, it enters the attack state. After completing the attack, the number of UAVs in the swarm decreases accordingly.
```

## 作者 Phase-II 最终 PlantUML STM0

```plantuml
@startuml
[*] --> SearchMission : Start Mission

state SearchMission {
  [*] --> Region1

  state Region1 {
    [*] --> Search
    Search --> Region2 : Finished Region1 Search
  }

  state Region2 {
    [*] --> Search
    Search --> Region3 : Finished Region2 Search
  }

  state Region3 {
    [*] --> Search
    Search --> [*] : Finished Region3 Search
  }
}

SearchMission --> FormationAdjust : Interception Detected

state FormationAdjust {
  [*] --> AdjustingFormation
  AdjustingFormation --> SearchMission : Finish Adjusting
}

SearchMission --> AttackState : Task Assignment Received

state AttackState {
  [*] --> Attacking
  Attacking --> SearchMission : Attack Finished / Decrease UAV swarm count
}
@enduml
```

## 转换后 FCSTM STM0

```fcstm
def int R45RouteToken = 0;
state llms_emp_feedback_final_0016 named "llms_emp_feedback_final_0016" {
    event Start_Mission named "Start Mission";
    event Finished_Region1_Search named "Finished Region1 Search";
    event Finished_Region2_Search named "Finished Region2 Search";
    event Finished_Region3_Search named "Finished Region3 Search";
    event Interception_Detected named "Interception Detected";
    event Finish_Adjusting named "Finish Adjusting";
    event Task_Assignment_Received named "Task Assignment Received";
    event Attack_Finished_Decrease_UAV_swarm_count named "Attack Finished / Decrease UAV swarm count";
    state SearchMission named "SearchMission" {
        state Region1 named "Region1" {
            state Region2 named "Region2" {
                state Region3 named "Region3" {
                    state InvalidInitialtr_0007 named "PlantUML initial target outside child scope: SearchMission.Region1.Search";
                    [*] -> InvalidInitialtr_0007;
                    InvalidInitialtr_0007 -> [*] : /Interception_Detected effect { R45RouteToken = 9; };
                    InvalidInitialtr_0007 -> [*] : /Task_Assignment_Received effect { R45RouteToken = 12; };
                }
                state InvalidInitialtr_0005 named "PlantUML initial target outside child scope: SearchMission.Region1.Search";
                [*] -> Region3 : if [R45RouteToken == 6] effect { R45RouteToken = 0; };
                Region3 -> [*] : if [R45RouteToken == 9];
                Region3 -> [*] : if [R45RouteToken == 12];
                [*] -> InvalidInitialtr_0005;
                Region3 -> [*] : /Interception_Detected effect { R45RouteToken = 9; };
                Region3 -> [*] : /Task_Assignment_Received effect { R45RouteToken = 12; };
                InvalidInitialtr_0005 -> [*] : /Interception_Detected effect { R45RouteToken = 9; };
                InvalidInitialtr_0005 -> [*] : /Task_Assignment_Received effect { R45RouteToken = 12; };
            }
            state Search named "Search";
            state InvalidFinaltr_0008 named "PlantUML final boundary outside source ancestry: @final:SearchMission.Region1.Region2.Region3";
            Region2 -> [*] : if [R45RouteToken == 9];
            Region2 -> [*] : if [R45RouteToken == 12];
            [*] -> Search;
            Search -> Region2 : /Finished_Region1_Search;
            Search -> Region2 : /Finished_Region2_Search effect { R45RouteToken = 6; };
            Search -> InvalidFinaltr_0008 : /Finished_Region3_Search;
            Search -> [*] : /Interception_Detected effect { R45RouteToken = 9; };
            Search -> [*] : /Task_Assignment_Received effect { R45RouteToken = 12; };
            InvalidFinaltr_0008 -> [*] : /Interception_Detected effect { R45RouteToken = 9; };
            InvalidFinaltr_0008 -> [*] : /Task_Assignment_Received effect { R45RouteToken = 12; };
        }
        Region1 -> [*] : if [R45RouteToken == 9];
        Region1 -> [*] : if [R45RouteToken == 12];
        [*] -> Region1;
    }
    state FormationAdjust named "FormationAdjust" {
        state AdjustingFormation named "AdjustingFormation";
        [*] -> AdjustingFormation;
        AdjustingFormation -> [*] : /Finish_Adjusting effect { R45RouteToken = 11; };
    }
    state AttackState named "AttackState" {
        state Attacking named "Attacking";
        [*] -> Attacking;
        Attacking -> [*] : /Attack_Finished_Decrease_UAV_swarm_count effect { R45RouteToken = 14; };
    }
    SearchMission -> FormationAdjust : if [R45RouteToken == 9] effect { R45RouteToken = 0; };
    FormationAdjust -> SearchMission : if [R45RouteToken == 11] effect { R45RouteToken = 0; };
    SearchMission -> AttackState : if [R45RouteToken == 12] effect { R45RouteToken = 0; };
    AttackState -> SearchMission : if [R45RouteToken == 14] effect { R45RouteToken = 0; };
    [*] -> SearchMission : /Start_Mission;
}
```

[上一组 `0015`](../0015/README.md) | [返回 60 组索引](../../PAIR_INDEX.md) | [下一组 `0017`](../0017/README.md)
