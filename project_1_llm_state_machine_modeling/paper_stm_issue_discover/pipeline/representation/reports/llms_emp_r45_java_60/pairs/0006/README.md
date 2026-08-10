# Pair `0006`：NL + PlantUML STM0 + FCSTM STM0

[上一组 `0005`](../0005/README.md) | [返回 60 组索引](../../PAIR_INDEX.md) | [下一组 `0007`](../0007/README.md)

- LLM：`GPT-4o`
- 模型/场景：UAV swarm state machine diagram
- 作者输出阶段：`Result with Semantic Checking`
- 作者输出单元格：`AE8`；Excel row：`8`
- Phase-I fallback：`false`
- 相对 Phase-I 是否变化：`true`
- Phase-I PlantUML SHA-256：`3dfdda2a0f6144429bd81717778a05f021bd455cad0efa0f29192f6a041b0952`
- NL SHA-256：`a01c022f5380700b6c13800497291640b4d64abbadce1d8984be0c14880ebeb3`
- PlantUML SHA-256：`ccec84b8ca1817cde5454b29b82b32dd353123b547fea8240e3d438be88fd667`
- FCSTM SHA-256：`380745924ea919eff312f99bde7ae3271d34204c6e40d25ed0f808ac2071a699`
- review subject SHA-256：`ca73f03d595f27974b0ca009ca9fb633d1fea8791c03736ccd88fc152d5c5b40`
- working contract SHA-256：`7a0a928c30381d594256b75b9272ef4560bfd7fc2a4341d8d35d966ff674c67a`
- 结构裁决：`structure_preserved`
- source states / transitions：`7` / `8`
- mapped / blocked / silent drop：`8` / `0` / `0`
- final / lifecycle / body coverage：`0/0` / `0/0` / `5/5`
- concurrent region / separator coverage：`0/0` / `0/0`
- source normalization coverage：`0/0`
- official raw / validation：`state_diagram` / `state_diagram`
- official identity states / transitions：`7` / `8`
- official identity remaps：state `0` / transition endpoint `0`
- AST audit：`passed`
- legacy whole-model FCSTM execution / Discover：`false` / `false`
- working bundle usage gate：`discover_input_with_capability_mask`
- ownership source / compiler / agent：`20` / `18` / `0`
- source macro / positive identity trace / conversion boundary trace：`13` / `20` / `0`
- capability source-static / simulation / transition-trace：`eligible_with_exclusions` / `ineligible` / `ineligible`
- compiler-only diagnostic policy：`rejected_conversion_artifact`；main-result conversion artifact limit：`0`
- 主 session 对读：`pass`；ownership/macro/capability 均为 `pass`；Case 0006 passes the current attribution-safe forward review; this does not assert global behavior equivalence, and unsupported runtime semantics remain fail-closed.
- source anchors：`source-ref:llms_emp_feedback_final_0006.puml:line:2\|state "UAV Swarm State Machine" as UAVSwarmStateMachine {, source-ref:llms_emp_feedback_final_0006.puml:line:7\|Searching --> Intercepted : Interception Detected`；FCSTM anchors：`element-ref:source:state:UAVSwarmStateMachine@line:8\|state UAVSwarmStateMachine named "UAV Swarm State Machine" {, element-ref:compiler:transition_segment:tr_0002:segment:1@line:24\|Searching -> Intercepted : /Interception_Detected;`
- 三个原始文件：[NL](./nl.txt) | [PlantUML](./plantuml.puml) | [FCSTM](./fcstm.fcstm)
- 审计入口：[canonical](../../canonical/llms_emp_feedback_final_0006.json) | [冻结 FCSTM](../../fcstm/llms_emp_feedback_final_0006.fcstm) | [case report](../../case_reports/llms_emp_feedback_final_0006.json) | [working contract](../../working_contracts/llms_emp_feedback_final_0006.json) | [source trace](../../source_traces/llms_emp_feedback_final_0006.json) | [人工总账](../../MANUAL_REVIEW.md)

## 主 session 三方语义对应

| projection | assessment | NL anchor | PlantUML anchor | FCSTM anchor | source roots | compiler members | rationale |
|---|---|---|---|---|---|---|---|
| `direct` | `preserved` | 1 This state machine model describes the state transitions of a UAV swarm. | source-ref:llms_emp_feedback_final_0006.puml:line:2\|state "UAV Swarm State Machine" as UAVSwarmStateMachine { | element-ref:source:state:UAVSwarmStateMachine@line:8\|state UAVSwarmStateMachine named "UAV Swarm State Machine" { | source:state:UAVSwarmStateMachine | - | Case 0006 binds source:state:UAVSwarmStateMachine to authored PlantUML occurrence 'state "UAV Swarm State Machine" as UAVSwarmStateMachine {' and current FCSTM occurrence 'state UAVSwarmStateMachine named "UAV Swarm State Machine" {'; the source semantic root remains attributable while any compiler-owned projection stays protected and cannot become an independent Repair target. |
| `macro` | `preserved_with_exclusions` | intercepted | source-ref:llms_emp_feedback_final_0006.puml:line:7\|Searching --> Intercepted : Interception Detected | element-ref:compiler:transition_segment:tr_0002:segment:1@line:24\|Searching -> Intercepted : /Interception_Detected; | source:transition:tr_0002 | compiler:transition_segment:tr_0002:segment:1 | Case 0006 binds source:transition:tr_0002 to authored PlantUML occurrence 'Searching --> Intercepted : Interception Detected' and current FCSTM occurrence 'Searching -> Intercepted : /Interception_Detected;'; the source semantic root remains attributable while any compiler-owned projection stays protected and cannot become an independent Repair target. |

## Risk occurrence 第二遍复核

| obligation | risk tag | assessment | PlantUML evidence | FCSTM evidence | ownership evidence | rationale |
|---|---|---|---|---|---|---|
| `review:multi_segment_macro:0001:tr_0005` | `multi_segment_macro` | `compiler_artifact_excluded` | source-ref:llms_emp_feedback_final_0006.puml:line:13\|AdjustingFormation --> Searching : Adjustment Complete, source-ref:llms_emp_feedback_final_0006.puml:line:19\|AttackingTarget --> Searching : Attack Complete | element-ref:compiler:route_control:R45RouteToken@line:1\|def int R45RouteToken = 0;, element-ref:compiler:transition_segment:tr_0005:segment:1@line:12\|AdjustingFormation -> [*] : /Adjustment_Complete effect { R45RouteToken = 5; };, element-ref:compiler:transition_segment:tr_0005:segment:2@line:21\|FormationAdjustment -> Searching : if [R45RouteToken == 5] effect { R45RouteToken = 0; }; | compiler:route_control:R45RouteToken, compiler:transition_segment:tr_0005:segment:1, compiler:transition_segment:tr_0005:segment:2, source:transition:tr_0005 | Case 0006 multi_segment_macro occurrence review:multi_segment_macro:0001:tr_0005 binds exact source refs to working-contract elements compiler:route_control:R45RouteToken, compiler:transition_segment:tr_0005:segment:1, compiler:transition_segment:tr_0005:segment:2, source:transition:tr_0005. All emitted segments collapse to one source transition root; no segment is promoted as a separate authored transition or editable issue target. |
| `review:route_controller:0002:tr_0005` | `route_controller` | `compiler_artifact_excluded` | source-ref:llms_emp_feedback_final_0006.puml:line:13\|AdjustingFormation --> Searching : Adjustment Complete, source-ref:llms_emp_feedback_final_0006.puml:line:19\|AttackingTarget --> Searching : Attack Complete | element-ref:compiler:route_control:R45RouteToken@line:1\|def int R45RouteToken = 0;, element-ref:compiler:transition_segment:tr_0005:segment:1@line:12\|AdjustingFormation -> [*] : /Adjustment_Complete effect { R45RouteToken = 5; };, element-ref:compiler:transition_segment:tr_0005:segment:2@line:21\|FormationAdjustment -> Searching : if [R45RouteToken == 5] effect { R45RouteToken = 0; }; | compiler:route_control:R45RouteToken, compiler:transition_segment:tr_0005:segment:1, compiler:transition_segment:tr_0005:segment:2, source:transition:tr_0005 | Case 0006 route_controller occurrence review:route_controller:0002:tr_0005 binds exact source refs to working-contract elements compiler:route_control:R45RouteToken, compiler:transition_segment:tr_0005:segment:1, compiler:transition_segment:tr_0005:segment:2, source:transition:tr_0005. R45RouteToken and routed segments remain compiler_owned, protected, and excluded from confirmed issues, Repair, Confirm acceptance, and main results. |
| `review:multi_segment_macro:0003:tr_0007` | `multi_segment_macro` | `compiler_artifact_excluded` | source-ref:llms_emp_feedback_final_0006.puml:line:13\|AdjustingFormation --> Searching : Adjustment Complete, source-ref:llms_emp_feedback_final_0006.puml:line:19\|AttackingTarget --> Searching : Attack Complete | element-ref:compiler:route_control:R45RouteToken@line:1\|def int R45RouteToken = 0;, element-ref:compiler:transition_segment:tr_0007:segment:1@line:17\|AttackingTarget -> [*] : /Attack_Complete effect { R45RouteToken = 7; };, element-ref:compiler:transition_segment:tr_0007:segment:2@line:22\|Attack -> Searching : if [R45RouteToken == 7] effect { R45RouteToken = 0; }; | compiler:route_control:R45RouteToken, compiler:transition_segment:tr_0007:segment:1, compiler:transition_segment:tr_0007:segment:2, source:transition:tr_0007 | Case 0006 multi_segment_macro occurrence review:multi_segment_macro:0003:tr_0007 binds exact source refs to working-contract elements compiler:route_control:R45RouteToken, compiler:transition_segment:tr_0007:segment:1, compiler:transition_segment:tr_0007:segment:2, source:transition:tr_0007. All emitted segments collapse to one source transition root; no segment is promoted as a separate authored transition or editable issue target. |
| `review:route_controller:0004:tr_0007` | `route_controller` | `compiler_artifact_excluded` | source-ref:llms_emp_feedback_final_0006.puml:line:13\|AdjustingFormation --> Searching : Adjustment Complete, source-ref:llms_emp_feedback_final_0006.puml:line:19\|AttackingTarget --> Searching : Attack Complete | element-ref:compiler:route_control:R45RouteToken@line:1\|def int R45RouteToken = 0;, element-ref:compiler:transition_segment:tr_0007:segment:1@line:17\|AttackingTarget -> [*] : /Attack_Complete effect { R45RouteToken = 7; };, element-ref:compiler:transition_segment:tr_0007:segment:2@line:22\|Attack -> Searching : if [R45RouteToken == 7] effect { R45RouteToken = 0; }; | compiler:route_control:R45RouteToken, compiler:transition_segment:tr_0007:segment:1, compiler:transition_segment:tr_0007:segment:2, source:transition:tr_0007 | Case 0006 route_controller occurrence review:route_controller:0004:tr_0007 binds exact source refs to working-contract elements compiler:route_control:R45RouteToken, compiler:transition_segment:tr_0007:segment:1, compiler:transition_segment:tr_0007:segment:2, source:transition:tr_0007. R45RouteToken and routed segments remain compiler_owned, protected, and excluded from confirmed issues, Repair, Confirm acceptance, and main results. |
| `review:synthetic_state:0005:001-UnspecifiedInitial` | `synthetic_state` | `compiler_artifact_excluded` | source-ref:llms_emp_feedback_final_0006.puml:line:2\|state "UAV Swarm State Machine" as UAVSwarmStateMachine { | element-ref:compiler:state:llms_emp_feedback_final_0006.UnspecifiedInitial@line:7\|state UnspecifiedInitial named "Unspecified initial";, element-ref:source:state:UAVSwarmStateMachine@line:8\|state UAVSwarmStateMachine named "UAV Swarm State Machine" { | compiler:state:llms_emp_feedback_final_0006.UnspecifiedInitial, source:state:UAVSwarmStateMachine | Case 0006 synthetic_state occurrence review:synthetic_state:0005:001-UnspecifiedInitial binds exact source refs to working-contract elements compiler:state:llms_emp_feedback_final_0006.UnspecifiedInitial, source:state:UAVSwarmStateMachine. The placeholder makes the authored missing, invalid, or final boundary visible while the synthetic state itself remains a non-repairable compiler artifact. |

## 作者阶段 lineage

| stage | output cell | present | output SHA-256 | feedback | resolved |
|---|---|---|---|---|---|
| `phase_i_generation` | `I8` | `true` | `3dfdda2a0f6144429bd81717778a05f021bd455cad0efa0f29192f6a041b0952` | - | - |
| `phase_ii_format` | `U8` | `false` | `-` | - | - |
| `phase_ii_grammar` | `Z8` | `false` | `-` | - | - |
| `phase_ii_semantic` | `AE8` | `true` | `ccec84b8ca1817cde5454b29b82b32dd353123b547fea8240e3d438be88fd667` | 1.missing regions<br>2. interaction error | - |

## Official identity ledger

- status：`aligned`
- canonical / official states：`7` / `7`
- aligned transition endpoints：`8`

本组 state identity 无需重映射。

本组 transition endpoint 无需重映射。

## Source normalization ledger

本组没有 source-input normalization。

## Concurrent region ledger

本组没有 PlantUML orthogonal/concurrent region separator。

## Operational debt

| reason code | count |
|---|---:|
| `R45.DEBT.missing_explicit_initial` | 1 |
| `R45.DEBT.opaque_state_body_semantics` | 5 |
| `R45.DEBT.opaque_transition_label_semantics` | 4 |

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
state "UAV Swarm State Machine" as UAVSwarmStateMachine {

[*] --> Searching
Searching : Target Search Task

Searching --> Intercepted : Interception Detected
Searching --> Attack : Task Assignment Received

state FormationAdjustment {
[*] --> AdjustingFormation
AdjustingFormation : Adjusting Formation after Interception
AdjustingFormation --> Searching : Adjustment Complete
}

state Attack {
[*] --> AttackingTarget
AttackingTarget : Performing Attack
AttackingTarget --> Searching : Attack Complete
}

Intercepted : UAV Swarm Intercepted
Intercepted --> FormationAdjustment

Attack : Entered Attack State
}
@enduml
```

## 转换后 FCSTM STM0

```fcstm
def int R45RouteToken = 0;
state llms_emp_feedback_final_0006 named "llms_emp_feedback_final_0006" {
    event Interception_Detected named "Interception Detected";
    event Task_Assignment_Received named "Task Assignment Received";
    event Adjustment_Complete named "Adjustment Complete";
    event Attack_Complete named "Attack Complete";
    state UnspecifiedInitial named "Unspecified initial";
    state UAVSwarmStateMachine named "UAV Swarm State Machine" {
        state FormationAdjustment named "FormationAdjustment" {
            state AdjustingFormation named "AdjustingFormation\n[PlantUML body] Adjusting Formation after Interception";
            [*] -> AdjustingFormation;
            AdjustingFormation -> [*] : /Adjustment_Complete effect { R45RouteToken = 5; };
        }
        state Attack named "Attack\n[PlantUML body] Entered Attack State" {
            state AttackingTarget named "AttackingTarget\n[PlantUML body] Performing Attack";
            [*] -> AttackingTarget;
            AttackingTarget -> [*] : /Attack_Complete effect { R45RouteToken = 7; };
        }
        state Searching named "Searching\n[PlantUML body] Target Search Task";
        state Intercepted named "Intercepted\n[PlantUML body] UAV Swarm Intercepted";
        FormationAdjustment -> Searching : if [R45RouteToken == 5] effect { R45RouteToken = 0; };
        Attack -> Searching : if [R45RouteToken == 7] effect { R45RouteToken = 0; };
        [*] -> Searching;
        Searching -> Intercepted : /Interception_Detected;
        Searching -> Attack : /Task_Assignment_Received;
        Intercepted -> FormationAdjustment;
    }
    [*] -> UnspecifiedInitial;
}
```

[上一组 `0005`](../0005/README.md) | [返回 60 组索引](../../PAIR_INDEX.md) | [下一组 `0007`](../0007/README.md)
