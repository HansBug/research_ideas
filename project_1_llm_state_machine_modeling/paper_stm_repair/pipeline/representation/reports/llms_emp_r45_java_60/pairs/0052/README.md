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
- FCSTM SHA-256：`164347c6c5a96a5487ee5a95aa418aae9ce8191bb96922843e67ffadcb285f59`
- review subject SHA-256：`a40c100674aabaec42d0aa0bf12dbafd3cf2c9ad4064ce005b1b6126189945f4`
- working contract SHA-256：`6e286979576d9c0c0b34bb391a9c78cfa0155ad4fbca06de43c67575050ac03b`
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
- ownership source / compiler / agent：`14` / `16` / `0`
- source macro / positive identity trace / conversion boundary trace：`9` / `14` / `0`
- capability source-static / simulation / transition-trace：`eligible_with_exclusions` / `ineligible` / `ineligible`
- compiler-only diagnostic policy：`rejected_conversion_artifact`；main-result conversion artifact limit：`0`
- 主 session 对读：`pass`；ownership/macro/capability 均为 `pass`；Case 0052 passes conversion-attribution review. This does not assert NL/PlantUML correctness or runtime equivalence; authored defects remain eligible for later source-grounded Discover. No conversion-specific blocker was found in the exact reviewed occurrences. Fresh v6 main-session review re-read NL, PlantUML, FCSTM, working contract, and source trace after the portable Java identity change; source/FCSTM/trace bytes are unchanged and verification remains fail-closed.
- source anchors：`source-ref:llms_emp_feedback_final_0052.puml:line:6\|state Operate {, source-ref:llms_emp_feedback_final_0052.puml:line:10\|Braking --> Idle : stop`；FCSTM anchors：`element-ref:source:state:Operate@line:8\|state Operate named "Operate" {, element-ref:compiler:transition_segment:tr_0006:segment:1@line:15\|Braking -> Idle : /stop;`
- 三个原始文件：[NL](./nl.txt) | [PlantUML](./plantuml.puml) | [FCSTM](./fcstm.fcstm)
- 审计入口：[canonical](../../canonical/llms_emp_feedback_final_0052.json) | [冻结 FCSTM](../../fcstm/llms_emp_feedback_final_0052.fcstm) | [case report](../../case_reports/llms_emp_feedback_final_0052.json) | [working contract](../../working_contracts/llms_emp_feedback_final_0052.json) | [source trace](../../source_traces/llms_emp_feedback_final_0052.json) | [人工总账](../../MANUAL_REVIEW.md)

## 主 session 三方语义对应

| projection | assessment | NL anchor | PlantUML anchor | FCSTM anchor | source roots | compiler members | rationale |
|---|---|---|---|---|---|---|---|
| `direct` | `preserved` | Operate | source-ref:llms_emp_feedback_final_0052.puml:line:6\|state Operate { | element-ref:source:state:Operate@line:8\|state Operate named "Operate" { | source:state:Operate | - | Case 0052 binds source:state:Operate to the exact authored occurrence 'state Operate {'; it is present as a direct FCSTM state projection with the same source identity and parent relation. |
| `macro` | `preserved_with_exclusions` | Braking | source-ref:llms_emp_feedback_final_0052.puml:line:10\|Braking --> Idle : stop | element-ref:compiler:transition_segment:tr_0006:segment:1@line:15\|Braking -> Idle : /stop; | source:transition:tr_0006 | compiler:transition_segment:tr_0006:segment:1 | Case 0052 binds source:transition:tr_0006 to the exact authored occurrence 'Braking --> Idle : stop'; it is present as a source-owned transition root whose cited FCSTM line belongs to a protected compiler macro; the raw label remains opaque. |

## Risk occurrence 第二遍复核

| obligation | risk tag | assessment | PlantUML evidence | FCSTM evidence | ownership evidence | rationale |
|---|---|---|---|---|---|---|
| `review:final_boundary:0001:tr_0009` | `final_boundary` | `source_fact_preserved` | source-ref:llms_emp_feedback_final_0052.puml:line:15\|Off --> [*] : shutdown | element-ref:compiler:transition_segment:tr_0009:segment:1@line:22\|Off -> [*] : /shutdown; | compiler:transition_segment:tr_0009:segment:1, source:transition:tr_0009 | Case 0052 risk final_boundary occurrence review:final_boundary:0001:tr_0009: The authored PlantUML final boundary is preserved by the bound FCSTM termination macro rather than being converted into an ordinary user state. |

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
    }
    state Off named "Off";
    [*] -> Off;
    Off -> Operate : /start;
    !Operate -> Off : /keyOff;
    Off -> [*] : /shutdown;
}
```

[上一组 `0051`](../0051/README.md) | [返回 60 组索引](../../PAIR_INDEX.md) | [下一组 `0053`](../0053/README.md)
