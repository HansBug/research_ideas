# Pair `0052`：NL + PlantUML STM0 + FCSTM STM0

[上一组 `0051`](../0051/README.md) | [返回 60 组索引](../../PAIR_INDEX.md) | [下一组 `0053`](../0053/README.md)

- LLM：`Claude`
- 模型/场景：Hybrid Sport Utility Vehicle, HSUV
- 作者输出阶段：`Result with Semantic Checking`
- 作者输出单元格：`AE54`；Excel row：`54`
- Phase-I fallback：`false`
- 相对 Phase-I 是否变化：`true`
- Phase-I PlantUML SHA-256：`13021d64f5ea5479d51dadc86dcfd1125d4f8535cd5a807ebf54df1d8df385b1`
- NL SHA-256：`9fe426ba761d5a52c3b670f35410502a5289bdd9489c4a9bfa983e34d565040c`
- PlantUML SHA-256：`bb6d78c3c2529f9a5e6b852f33e3b1731b827b6f8eb79c2dfa02c10bfcbcf7c1`
- FCSTM SHA-256：`dc068a60aa083d94b698b1855a62f17389eb881a8626e7df0587bcb46c0563ac`
- review subject SHA-256：`099d29a72968a74d790a397af6d21c5628a81e7560167546032058067b80af39`
- working contract SHA-256：`7e97dc93ff04abe24b894423d4e71bb193ff4ff6ffe0b87850e8db649836661d`
- 结构裁决：`structure_preserved`
- source states / transitions：`5` / `9`
- mapped / blocked / silent drop：`9` / `0` / `0`
- final / lifecycle / body coverage：`1/1` / `0/0` / `0/0`
- concurrent region / separator coverage：`0/0` / `0/0`
- source normalization coverage：`0/0`
- official raw / validation：`state_diagram` / `state_diagram`
- official identity states / transitions：`5` / `9`
- official identity remaps：state `0` / transition endpoint `0`
- AST audit：`passed`
- legacy whole-model FCSTM execution / Discover：`false` / `false`
- working bundle usage gate：`discover_input_with_capability_mask`
- ownership source / compiler / agent：`14` / `20` / `0`
- source macro / positive identity trace / conversion boundary trace：`9` / `14` / `0`
- capability source-static / simulation / transition-trace：`eligible_with_exclusions` / `eligible_with_exclusions` / `eligible_with_exclusions`
- compiler-only diagnostic policy：`rejected_conversion_artifact`；main-result conversion artifact limit：`0`
- 主 session 对读：`pass`；ownership/macro/capability 均为 `pass`；Case 0052 passes the current attribution-safe forward review; this does not assert global behavior equivalence, and unsupported runtime semantics remain fail-closed. Amendment record: the substantive subject review remains the one recorded in review_context (first reviewed 2026-07-20T05:44:08Z by gpt-5.5 (session omx-1784393668980-pxpj3q), and it still binds because review_subject_sha256 is unchanged. A scoped re-check was performed 2026-08-17 by claude-opus-5 (main-session LLM, PR #185) because commit bbb04cb1 (2026-07-27) regenerated the 60 working contracts and commit 35eba126 (2026-08-11) renamed the paper workspace, and neither refreshed this registry. The re-review is scoped: a key-by-key diff shows the only contract changes are capability_eligibility.simulation, capability_eligibility.transition_trace and summary.simulation_status (bbb04cb1) plus the four artifact_bindings path strings (35eba126); the remaining 168 keys and the whole of canonical/fcstm/parse_inspect/source_traces are byte-identical, so review_subject_sha256 is unchanged and the original ownership, macro and correspondence findings still stand. The capability block was re-checked against seven invariants: eligible ids are source: only, excluded ids cover the compiler-owned set, the two sets are disjoint, claim_boundary and reason_codes are non-empty, main_result_conversion_artifact_limit is still 0, and usage_gate is unchanged.
- source anchors：`source-ref:llms_emp_feedback_final_0052.puml:line:6\|state Operate {, source-ref:llms_emp_feedback_final_0052.puml:line:10\|Braking --> Idle : stop`；FCSTM anchors：`element-ref:source:state:Operate@line:9\|state Operate named "Operate" {, element-ref:compiler:transition_segment:tr_0006:segment:1@line:16\|Braking -> Idle : /stop;`
- 三个原始文件：[NL](./nl.txt) | [PlantUML](./plantuml.puml) | [FCSTM](./fcstm.fcstm)
- 审计入口：[canonical](../../canonical/llms_emp_feedback_final_0052.json) | [冻结 FCSTM](../../fcstm/llms_emp_feedback_final_0052.fcstm) | [case report](../../case_reports/llms_emp_feedback_final_0052.json) | [working contract](../../working_contracts/llms_emp_feedback_final_0052.json) | [source trace](../../source_traces/llms_emp_feedback_final_0052.json) | [人工总账](../../MANUAL_REVIEW.md)

## 主 session 三方语义对应

| projection | assessment | NL anchor | PlantUML anchor | FCSTM anchor | source roots | compiler members | rationale |
|---|---|---|---|---|---|---|---|
| `direct` | `preserved` | Operate | source-ref:llms_emp_feedback_final_0052.puml:line:6\|state Operate { | element-ref:source:state:Operate@line:9\|state Operate named "Operate" { | source:state:Operate | - | Case 0052 binds source:state:Operate to authored PlantUML occurrence 'state Operate {' and current FCSTM occurrence 'state Operate named "Operate" {'; the source semantic root remains attributable while any compiler-owned projection stays protected and cannot become an independent Repair target. |
| `macro` | `preserved_with_exclusions` | Braking | source-ref:llms_emp_feedback_final_0052.puml:line:10\|Braking --> Idle : stop | element-ref:compiler:transition_segment:tr_0006:segment:1@line:16\|Braking -> Idle : /stop; | source:transition:tr_0006 | compiler:transition_segment:tr_0006:segment:1 | Case 0052 binds source:transition:tr_0006 to authored PlantUML occurrence 'Braking --> Idle : stop' and current FCSTM occurrence 'Braking -> Idle : /stop;'; the source semantic root remains attributable while any compiler-owned projection stays protected and cannot become an independent Repair target. |

## Risk occurrence 第二遍复核

| obligation | risk tag | assessment | PlantUML evidence | FCSTM evidence | ownership evidence | rationale |
|---|---|---|---|---|---|---|
| `review:multi_segment_macro:0001:tr_0008` | `multi_segment_macro` | `compiler_artifact_excluded` | source-ref:llms_emp_feedback_final_0052.puml:line:14\|Operate --> Off : keyOff | element-ref:compiler:route_control:R45RouteToken@line:1\|def int R45RouteToken = 0;, element-ref:compiler:transition_segment:tr_0008:segment:1@line:18\|Idle -> [*] : /keyOff effect { R45RouteToken = 8; };, element-ref:compiler:transition_segment:tr_0008:segment:2@line:19\|Accelerating_or_Cruising -> [*] : /keyOff effect { R45RouteToken = 8; };, element-ref:compiler:transition_segment:tr_0008:segment:3@line:20\|Braking -> [*] : /keyOff effect { R45RouteToken = 8; };, element-ref:compiler:transition_segment:tr_0008:segment:4@line:23\|Operate -> Off : if [R45RouteToken == 8] effect { R45RouteToken = 0; }; | compiler:route_control:R45RouteToken, compiler:transition_segment:tr_0008:segment:1, compiler:transition_segment:tr_0008:segment:2, compiler:transition_segment:tr_0008:segment:3, compiler:transition_segment:tr_0008:segment:4, source:transition:tr_0008 | Case 0052 multi_segment_macro occurrence review:multi_segment_macro:0001:tr_0008 binds exact source refs to working-contract elements compiler:route_control:R45RouteToken, compiler:transition_segment:tr_0008:segment:1, compiler:transition_segment:tr_0008:segment:2, compiler:transition_segment:tr_0008:segment:3, compiler:transition_segment:tr_0008:segment:4, source:transition:tr_0008. All emitted segments collapse to one source transition root; no segment is promoted as a separate authored transition or editable issue target. |
| `review:route_controller:0002:tr_0008` | `route_controller` | `compiler_artifact_excluded` | source-ref:llms_emp_feedback_final_0052.puml:line:14\|Operate --> Off : keyOff | element-ref:compiler:route_control:R45RouteToken@line:1\|def int R45RouteToken = 0;, element-ref:compiler:transition_segment:tr_0008:segment:1@line:18\|Idle -> [*] : /keyOff effect { R45RouteToken = 8; };, element-ref:compiler:transition_segment:tr_0008:segment:2@line:19\|Accelerating_or_Cruising -> [*] : /keyOff effect { R45RouteToken = 8; };, element-ref:compiler:transition_segment:tr_0008:segment:3@line:20\|Braking -> [*] : /keyOff effect { R45RouteToken = 8; };, element-ref:compiler:transition_segment:tr_0008:segment:4@line:23\|Operate -> Off : if [R45RouteToken == 8] effect { R45RouteToken = 0; }; | compiler:route_control:R45RouteToken, compiler:transition_segment:tr_0008:segment:1, compiler:transition_segment:tr_0008:segment:2, compiler:transition_segment:tr_0008:segment:3, compiler:transition_segment:tr_0008:segment:4, source:transition:tr_0008 | Case 0052 route_controller occurrence review:route_controller:0002:tr_0008 binds exact source refs to working-contract elements compiler:route_control:R45RouteToken, compiler:transition_segment:tr_0008:segment:1, compiler:transition_segment:tr_0008:segment:2, compiler:transition_segment:tr_0008:segment:3, compiler:transition_segment:tr_0008:segment:4, source:transition:tr_0008. R45RouteToken and routed segments remain compiler_owned, protected, and excluded from confirmed issues, Repair, Confirm acceptance, and main results. |
| `review:final_boundary:0003:tr_0009` | `final_boundary` | `source_fact_preserved` | source-ref:llms_emp_feedback_final_0052.puml:line:15\|Off --> [*] : shutdown | element-ref:compiler:transition_segment:tr_0009:segment:1@line:26\|Off -> [*] : /shutdown; | compiler:transition_segment:tr_0009:segment:1, source:transition:tr_0009 | Case 0052 final_boundary occurrence review:final_boundary:0003:tr_0009 binds exact source refs to working-contract elements compiler:transition_segment:tr_0009:segment:1, source:transition:tr_0009. The authored final occurrence remains visible through its source root; any completion holder or routing segment is excluded from source-level claims. |

## 作者阶段 lineage

| stage | output cell | present | output SHA-256 | feedback | resolved |
|---|---|---|---|---|---|
| `phase_i_generation` | `I54` | `true` | `13021d64f5ea5479d51dadc86dcfd1125d4f8535cd5a807ebf54df1d8df385b1` | - | - |
| `phase_ii_format` | `U54` | `false` | `-` | - | - |
| `phase_ii_grammar` | `Z54` | `false` | `-` | - | - |
| `phase_ii_semantic` | `AE54` | `true` | `bb6d78c3c2529f9a5e6b852f33e3b1731b827b6f8eb79c2dfa02c10bfcbcf7c1` | 1. missing final state | 1.0 |

## Official identity ledger

- status：`aligned`
- canonical / official states：`5` / `5`
- aligned transition endpoints：`9`

本组 state identity 无需重映射。

本组 transition endpoint 无需重映射。

## Source normalization ledger

本组没有 source-input normalization。

## Concurrent region ledger

本组没有 PlantUML orthogonal/concurrent region separator。

## Operational debt

| reason code | count |
|---|---:|
| `R45.DEBT.composite_source_activation_dispatch` | 1 |
| `R45.DEBT.opaque_transition_label_semantics` | 7 |

## NL

```text
1. Once the device is powered on, the system enters the `Operate` state, and based on user actions, it transitions between `Idle`, `Accelerating or Cruising`, and `Braking` states.
2. The system can be turned on with the `start` signal and turned off with the `keyOff` signal.
3. Within the `Operate` state, the system transitions between different substates depending on actions like accelerating, braking, or stopping.
```

## 作者 Phase-II 最终 PlantUML STM0

```plantuml
@startuml

[*] --> Off
Off --> Operate : start

state Operate {
[*] --> Idle
Idle --> Accelerating_or_Cruising : accelerate
Accelerating_or_Cruising --> Braking : brake
Braking --> Idle : stop
Accelerating_or_Cruising --> Idle : stop
}

Operate --> Off : keyOff
Off --> [*] : shutdown

@enduml
```

## 转换后 FCSTM STM0

```fcstm
def int R45RouteToken = 0;
state llms_emp_feedback_final_0052 named "llms_emp_feedback_final_0052" {
    event start named "start";
    event accelerate named "accelerate";
    event brake named "brake";
    event stop named "stop";
    event keyOff named "keyOff";
    event shutdown named "shutdown";
    state Operate named "Operate" {
        state Idle named "Idle";
        state Accelerating_or_Cruising named "Accelerating_or_Cruising";
        state Braking named "Braking";
        [*] -> Idle;
        Idle -> Accelerating_or_Cruising : /accelerate;
        Accelerating_or_Cruising -> Braking : /brake;
        Braking -> Idle : /stop;
        Accelerating_or_Cruising -> Idle : /stop;
        Idle -> [*] : /keyOff effect { R45RouteToken = 8; };
        Accelerating_or_Cruising -> [*] : /keyOff effect { R45RouteToken = 8; };
        Braking -> [*] : /keyOff effect { R45RouteToken = 8; };
    }
    state Off named "Off";
    Operate -> Off : if [R45RouteToken == 8] effect { R45RouteToken = 0; };
    [*] -> Off;
    Off -> Operate : /start;
    Off -> [*] : /shutdown;
}
```

[上一组 `0051`](../0051/README.md) | [返回 60 组索引](../../PAIR_INDEX.md) | [下一组 `0053`](../0053/README.md)
