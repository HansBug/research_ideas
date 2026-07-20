# Pair `0056`：NL + PlantUML STM0 + FCSTM STM0

[上一组 `0055`](../0055/README.md) | [返回 60 组索引](../../PAIR_INDEX.md) | [下一组 `0057`](../0057/README.md)

- LLM：`Claude`
- 模型/场景：UAV swarm state machine diagram
- 作者输出阶段：`Result with Semantic Checking`
- 作者输出单元格：`AE58`；Excel row：`58`
- Phase-I fallback：`false`
- 相对 Phase-I 是否变化：`true`
- Phase-I PlantUML SHA-256：`bf93ab42299d56f2aca29149e61760019633d58293e0b2b464360e4d5c20c97f`
- NL SHA-256：`a01c022f5380700b6c13800497291640b4d64abbadce1d8984be0c14880ebeb3`
- PlantUML SHA-256：`5021744139f603fe986abdb886eb4dae03c71911218a4d7880a494f3455bd816`
- FCSTM SHA-256：`fd7db3768259ed25a603f87bed193b2bbbfa16d4c1a8c18907dd04227cd6df6c`
- review subject SHA-256：`94d7c7f422e15210dc40322b8b5f4209deb3c87aa4a1eb516507def3bad0fa15`
- working contract SHA-256：`e23a550d0cb9f39fb5dffdb5436944a2f067e54ada1f9089ba89656c048d9cbd`
- 结构裁决：`structure_preserved`
- source states / transitions：`8` / `13`
- mapped / blocked / silent drop：`13` / `0` / `0`
- final / lifecycle / body coverage：`1/1` / `0/0` / `0/0`
- concurrent region / separator coverage：`2/2` / `1/1`
- source normalization coverage：`0/0`
- official raw / validation：`state_diagram` / `state_diagram`
- official identity states / transitions：`8` / `13`
- official identity remaps：state `0` / transition endpoint `0`
- AST audit：`passed`
- legacy whole-model FCSTM execution / Discover：`false` / `false`
- working bundle usage gate：`discover_input_with_capability_mask`
- ownership source / compiler / agent：`23` / `20` / `0`
- source macro / positive identity trace / conversion boundary trace：`15` / `23` / `0`
- capability source-static / simulation / transition-trace：`eligible_with_exclusions` / `ineligible` / `ineligible`
- compiler-only diagnostic policy：`rejected_conversion_artifact`；main-result conversion artifact limit：`0`
- 主 session 对读：`pass`；ownership/macro/capability 均为 `pass`；Case 0056 passes conversion-attribution review. This does not assert NL/PlantUML correctness or runtime equivalence; authored defects remain eligible for later source-grounded Discover. No conversion-specific blocker was found in the exact reviewed occurrences.
- source anchors：`source-ref:llms_emp_feedback_final_0056.puml:line:5\|state SearchState {, source-ref:llms_emp_feedback_final_0056.puml:line:12\|NoIntercept --> Intercepted : Intercepted`；FCSTM anchors：`element-ref:source:state:SearchState@line:8\|state SearchState named "SearchState\n[PlantUML concurrent region 0] states=SearchState.Area1, SearchState.Area2, SearchState.Area3; transitions=tr_0002, tr_0003, tr_0004, tr_0005\n[PlantUML concurrent region 1] states=SearchState.NoIntercept, SearchState.Intercepted; transitions=tr_0006, tr_0007, tr_0008\n[PlantUML concurrent separator] region 0 -> 1 at llms_emp_feedback_final_0056.puml:line:10" {, element-ref:compiler:transition_segment:tr_0007:segment:1@line:19\|NoIntercept -> Intercepted : /Intercepted;`
- 三个原始文件：[NL](./nl.txt) | [PlantUML](./plantuml.puml) | [FCSTM](./fcstm.fcstm)
- 审计入口：[canonical](../../canonical/llms_emp_feedback_final_0056.json) | [冻结 FCSTM](../../fcstm/llms_emp_feedback_final_0056.fcstm) | [case report](../../case_reports/llms_emp_feedback_final_0056.json) | [working contract](../../working_contracts/llms_emp_feedback_final_0056.json) | [source trace](../../source_traces/llms_emp_feedback_final_0056.json) | [人工总账](../../MANUAL_REVIEW.md)

## 主 session 三方语义对应

| projection | assessment | NL anchor | PlantUML anchor | FCSTM anchor | source roots | compiler members | rationale |
|---|---|---|---|---|---|---|---|
| `direct` | `preserved` | 1 This state machine model describes the state transitions of a UAV swarm. | source-ref:llms_emp_feedback_final_0056.puml:line:5\|state SearchState { | element-ref:source:state:SearchState@line:8\|state SearchState named "SearchState\n[PlantUML concurrent region 0] states=SearchState.Area1, SearchState.Area2, SearchState.Area3; transitions=tr_0002, tr_0003, tr_0004, tr_0005\n[PlantUML concurrent region 1] states=SearchState.NoIntercept, SearchState.Intercepted; transitions=tr_0006, tr_0007, tr_0008\n[PlantUML concurrent separator] region 0 -> 1 at llms_emp_feedback_final_0056.puml:line:10" { | source:state:SearchState | - | Case 0056 binds source:state:SearchState to the exact authored occurrence 'state SearchState {'; it is present as a direct FCSTM state projection with the same source identity and parent relation. |
| `macro` | `preserved_with_exclusions` | intercepted | source-ref:llms_emp_feedback_final_0056.puml:line:12\|NoIntercept --> Intercepted : Intercepted | element-ref:compiler:transition_segment:tr_0007:segment:1@line:19\|NoIntercept -> Intercepted : /Intercepted; | source:transition:tr_0007 | compiler:transition_segment:tr_0007:segment:1 | Case 0056 binds source:transition:tr_0007 to the exact authored occurrence 'NoIntercept --> Intercepted : Intercepted'; it is present as a source-owned transition root whose cited FCSTM line belongs to a protected compiler macro; the raw label remains opaque. |

## Risk occurrence 第二遍复核

| obligation | risk tag | assessment | PlantUML evidence | FCSTM evidence | ownership evidence | rationale |
|---|---|---|---|---|---|---|
| `review:final_boundary:0001:tr_0013` | `final_boundary` | `source_fact_preserved` | source-ref:llms_emp_feedback_final_0056.puml:line:22\|SearchState --> [*] : Mission Complete | element-ref:compiler:transition_segment:tr_0013:segment:1@line:29\|!SearchState -> [*] : /Mission_Complete; | compiler:transition_segment:tr_0013:segment:1, source:transition:tr_0013 | Case 0056 risk final_boundary occurrence review:final_boundary:0001:tr_0013: The authored PlantUML final boundary is preserved by the bound FCSTM termination macro rather than being converted into an ordinary user state. |
| `review:concurrent_region:0002:SearchState:region:0` | `concurrent_region` | `capability_excluded` | source-ref:llms_emp_feedback_final_0056.puml:line:10\|-- | element-ref:source:region:SearchState:region:0@line:8\|state SearchState named "SearchState\n[PlantUML concurrent region 0] states=SearchState.Area1, SearchState.Area2, SearchState.Area3; transitions=tr_0002, tr_0003, tr_0004, tr_0005\n[PlantUML concurrent region 1] states=SearchState.NoIntercept, SearchState.Intercepted; transitions=tr_0006, tr_0007, tr_0008\n[PlantUML concurrent separator] region 0 -> 1 at llms_emp_feedback_final_0056.puml:line:10" { | source:region:SearchState:region:0 | Case 0056 risk concurrent_region occurrence review:concurrent_region:0002:SearchState:region:0: The authored region occurrence and its FCSTM metadata projection are present, while executable orthogonal-region semantics remain capability-excluded. |
| `review:concurrent_region:0003:SearchState:region:1` | `concurrent_region` | `capability_excluded` | source-ref:llms_emp_feedback_final_0056.puml:line:10\|-- | element-ref:source:region:SearchState:region:1@line:8\|state SearchState named "SearchState\n[PlantUML concurrent region 0] states=SearchState.Area1, SearchState.Area2, SearchState.Area3; transitions=tr_0002, tr_0003, tr_0004, tr_0005\n[PlantUML concurrent region 1] states=SearchState.NoIntercept, SearchState.Intercepted; transitions=tr_0006, tr_0007, tr_0008\n[PlantUML concurrent separator] region 0 -> 1 at llms_emp_feedback_final_0056.puml:line:10" { | source:region:SearchState:region:1 | Case 0056 risk concurrent_region occurrence review:concurrent_region:0003:SearchState:region:1: The authored region occurrence and its FCSTM metadata projection are present, while executable orthogonal-region semantics remain capability-excluded. |
| `review:explicit_concurrency:0004:001-multiple_initial_fanout` | `explicit_concurrency` | `capability_excluded` | source-ref:llms_emp_feedback_final_0056.puml:line:11\|[*] --> NoIntercept, source-ref:llms_emp_feedback_final_0056.puml:line:6\|[*] --> Area1 | element-ref:compiler:transition_segment:tr_0002:segment:1@line:14\|[*] -> Area1;, element-ref:compiler:transition_segment:tr_0006:segment:1@line:18\|[*] -> NoIntercept; | source:transition:tr_0002, source:transition:tr_0006 | Case 0056 risk explicit_concurrency occurrence review:explicit_concurrency:0004:001-multiple_initial_fanout: The authored concurrency occurrence remains visible, but the FCSTM projection does not claim fork/join product semantics and is excluded from runtime evidence. |

## 作者阶段 lineage

| stage | output cell | present | output SHA-256 | feedback | resolved |
|---|---|---|---|---|---|
| `phase_i_generation` | `I58` | `true` | `bf93ab42299d56f2aca29149e61760019633d58293e0b2b464360e4d5c20c97f` | - | - |
| `phase_ii_format` | `U58` | `false` | `-` | - | - |
| `phase_ii_grammar` | `Z58` | `false` | `-` | - | - |
| `phase_ii_semantic` | `AE58` | `true` | `5021744139f603fe986abdb886eb4dae03c71911218a4d7880a494f3455bd816` | 1. missing regions | 1.0 |

## Official identity ledger

- status：`aligned`
- canonical / official states：`8` / `8`
- aligned transition endpoints：`13`

本组 state identity 无需重映射。

本组 transition endpoint 无需重映射。

## Source normalization ledger

本组没有 source-input normalization。

## Concurrent region ledger

| owner | region | direct states | direct transitions | separator before | separator after |
|---|---:|---|---|---|---|
| `SearchState` | 0 | SearchState.Area1, SearchState.Area2, SearchState.Area3 | tr_0002, tr_0003, tr_0004, tr_0005 | - | llms_emp_feedback_final_0056.puml:line:10 |
| `SearchState` | 1 | SearchState.NoIntercept, SearchState.Intercepted | tr_0006, tr_0007, tr_0008 | llms_emp_feedback_final_0056.puml:line:10 | - |

## Operational debt

| reason code | count |
|---|---:|
| `R45.DEBT.concurrent_region_semantics` | 1 |
| `R45.DEBT.multiple_initial_fanout` | 1 |
| `R45.DEBT.opaque_transition_label_semantics` | 7 |

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

[*] --> SearchState

state SearchState {
[*] --> Area1
Area1 --> Area2
Area2 --> Area3
Area3 --> Area1
--
[*] --> NoIntercept
NoIntercept --> Intercepted : Intercepted
Intercepted --> NoIntercept : Intercept Resolved
}

SearchState --> FormationAdjustment : Intercepted
FormationAdjustment --> SearchState : Adjustment Complete

SearchState --> AttackState : Task Assignment Received
AttackState --> SearchState : Attack Complete [Decrease UAV Count]

SearchState --> [*] : Mission Complete

@enduml
```

## 转换后 FCSTM STM0

```fcstm
state llms_emp_feedback_final_0056 named "llms_emp_feedback_final_0056" {
    event Intercepted named "Intercepted";
    event Intercept_Resolved named "Intercept Resolved";
    event Adjustment_Complete named "Adjustment Complete";
    event Task_Assignment_Received named "Task Assignment Received";
    event Attack_Complete_Decrease_UAV_Count named "Attack Complete [Decrease UAV Count]";
    event Mission_Complete named "Mission Complete";
    state SearchState named "SearchState\n[PlantUML concurrent region 0] states=SearchState.Area1, SearchState.Area2, SearchState.Area3; transitions=tr_0002, tr_0003, tr_0004, tr_0005\n[PlantUML concurrent region 1] states=SearchState.NoIntercept, SearchState.Intercepted; transitions=tr_0006, tr_0007, tr_0008\n[PlantUML concurrent separator] region 0 -> 1 at llms_emp_feedback_final_0056.puml:line:10" {
        state Area1 named "Area1";
        state Area2 named "Area2";
        state Area3 named "Area3";
        state NoIntercept named "NoIntercept";
        state Intercepted named "Intercepted";
        [*] -> Area1;
        Area1 -> Area2;
        Area2 -> Area3;
        Area3 -> Area1;
        [*] -> NoIntercept;
        NoIntercept -> Intercepted : /Intercepted;
        Intercepted -> NoIntercept : /Intercept_Resolved;
    }
    state FormationAdjustment named "FormationAdjustment";
    state AttackState named "AttackState";
    [*] -> SearchState;
    !SearchState -> FormationAdjustment : /Intercepted;
    FormationAdjustment -> SearchState : /Adjustment_Complete;
    !SearchState -> AttackState : /Task_Assignment_Received;
    AttackState -> SearchState : /Attack_Complete_Decrease_UAV_Count;
    !SearchState -> [*] : /Mission_Complete;
}
```

[上一组 `0055`](../0055/README.md) | [返回 60 组索引](../../PAIR_INDEX.md) | [下一组 `0057`](../0057/README.md)
