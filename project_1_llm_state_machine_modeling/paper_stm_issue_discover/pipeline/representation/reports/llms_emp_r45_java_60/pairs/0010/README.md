# Pair `0010`：NL + PlantUML STM0 + FCSTM STM0

[上一组 `0009`](../0009/README.md) | [返回 60 组索引](../../PAIR_INDEX.md) | [下一组 `0011`](../0011/README.md)

- LLM：`GPT-4`
- 模型/场景：high-level driving module
- 作者输出阶段：`Result with Semantic Checking`
- 作者输出单元格：`AE12`；Excel row：`12`
- Phase-I fallback：`false`
- 相对 Phase-I 是否变化：`false`
- Phase-I PlantUML SHA-256：`73021d0499bdbbc34299e07733dda58162aefdf297e57bd6aae76da940aaed53`
- NL SHA-256：`f1c3dc88371b8256352e7ab6ee7eb42424de6e11dfde70d185f224dd1d05a7a8`
- PlantUML SHA-256：`73021d0499bdbbc34299e07733dda58162aefdf297e57bd6aae76da940aaed53`
- FCSTM SHA-256：`d3d10565f4aaadcc99f7b97f2d78ff6443ce29be439b229ed041fc9d2b1d9f38`
- review subject SHA-256：`e59e77e54e6e61afcb00b1ef0a8942676a470d476a18ca404c35236c933a27b4`
- working contract SHA-256：`e3a1249f1b1f9109e4d0569389ff373b5f26f7c92165b63c3c95f1c299fe264b`
- 结构裁决：`structure_preserved`
- source states / transitions：`5` / `8`
- mapped / blocked / silent drop：`8` / `0` / `0`
- final / lifecycle / body coverage：`0/0` / `0/0` / `6/6`
- concurrent region / separator coverage：`0/0` / `0/0`
- source normalization coverage：`0/0`
- official raw / validation：`state_diagram` / `state_diagram`
- official identity states / transitions：`5` / `8`
- official identity remaps：state `0` / transition endpoint `0`
- AST audit：`passed`
- legacy whole-model FCSTM execution / Discover：`false` / `false`
- working bundle usage gate：`discover_input_with_capability_mask`
- ownership source / compiler / agent：`19` / `15` / `0`
- source macro / positive identity trace / conversion boundary trace：`14` / `19` / `0`
- capability source-static / simulation / transition-trace：`eligible_with_exclusions` / `eligible_with_exclusions` / `eligible_with_exclusions`
- compiler-only diagnostic policy：`rejected_conversion_artifact`；main-result conversion artifact limit：`0`
- 主 session 对读：`pass`；ownership/macro/capability 均为 `pass`；Case 0010 passes the current attribution-safe forward review; this does not assert global behavior equivalence, and unsupported runtime semantics remain fail-closed. Amendment record: the substantive subject review remains the one recorded in review_context (first reviewed 2026-07-20T05:44:08Z by gpt-5.5 (session omx-1784393668980-pxpj3q), and it still binds because review_subject_sha256 is unchanged. A scoped re-check was performed 2026-08-17 by claude-opus-5 (main-session LLM, PR #185) because commit bbb04cb1 (2026-07-27) regenerated the 60 working contracts and commit 35eba126 (2026-08-11) renamed the paper workspace, and neither refreshed this registry. The re-review is scoped: a key-by-key diff shows the only contract changes are capability_eligibility.simulation, capability_eligibility.transition_trace and summary.simulation_status (bbb04cb1) plus the four artifact_bindings path strings (35eba126); the remaining 168 keys and the whole of canonical/fcstm/parse_inspect/source_traces are byte-identical, so review_subject_sha256 is unchanged and the original ownership, macro and correspondence findings still stand. The capability block was re-checked against seven invariants: eligible ids are source: only, excluded ids cover the compiler-owned set, the two sets are disjoint, claim_boundary and reason_codes are non-empty, main_result_conversion_artifact_limit is still 0, and usage_gate is unchanged.
- source anchors：`source-ref:llms_emp_feedback_final_0010.puml:line:2\|[*] --> HumanDriving, source-ref:llms_emp_feedback_final_0010.puml:line:5\|HumanDriving --> Autonomous : Power On`；FCSTM anchors：`element-ref:source:state:HumanDriving@line:8\|state HumanDriving named "HumanDriving\n[PlantUML body] Human Driving Mode";, element-ref:compiler:transition_segment:tr_0002:segment:1@line:14\|HumanDriving -> Autonomous : /Power_On;`
- 三个原始文件：[NL](./nl.txt) | [PlantUML](./plantuml.puml) | [FCSTM](./fcstm.fcstm)
- 审计入口：[canonical](../../canonical/llms_emp_feedback_final_0010.json) | [冻结 FCSTM](../../fcstm/llms_emp_feedback_final_0010.fcstm) | [case report](../../case_reports/llms_emp_feedback_final_0010.json) | [working contract](../../working_contracts/llms_emp_feedback_final_0010.json) | [source trace](../../source_traces/llms_emp_feedback_final_0010.json) | [人工总账](../../MANUAL_REVIEW.md)

## 主 session 三方语义对应

| projection | assessment | NL anchor | PlantUML anchor | FCSTM anchor | source roots | compiler members | rationale |
|---|---|---|---|---|---|---|---|
| `direct` | `preserved` | 1 The human driving mode is represented by a simple state. | source-ref:llms_emp_feedback_final_0010.puml:line:2\|[*] --> HumanDriving | element-ref:source:state:HumanDriving@line:8\|state HumanDriving named "HumanDriving\n[PlantUML body] Human Driving Mode"; | source:state:HumanDriving | - | Case 0010 binds source:state:HumanDriving to authored PlantUML occurrence '[*] --> HumanDriving' and current FCSTM occurrence 'state HumanDriving named "HumanDriving\n[PlantUML body] Human Driving Mode";'; the source semantic root remains attributable while any compiler-owned projection stays protected and cannot become an independent Repair target. |
| `macro` | `preserved_with_exclusions` | autonomous | source-ref:llms_emp_feedback_final_0010.puml:line:5\|HumanDriving --> Autonomous : Power On | element-ref:compiler:transition_segment:tr_0002:segment:1@line:14\|HumanDriving -> Autonomous : /Power_On; | source:transition:tr_0002 | compiler:transition_segment:tr_0002:segment:1 | Case 0010 binds source:transition:tr_0002 to authored PlantUML occurrence 'HumanDriving --> Autonomous : Power On' and current FCSTM occurrence 'HumanDriving -> Autonomous : /Power_On;'; the source semantic root remains attributable while any compiler-owned projection stays protected and cannot become an independent Repair target. |

## Risk occurrence 第二遍复核

本组不要求 risk-tag 第二遍复核。

## 作者阶段 lineage

| stage | output cell | present | output SHA-256 | feedback | resolved |
|---|---|---|---|---|---|
| `phase_i_generation` | `I12` | `true` | `73021d0499bdbbc34299e07733dda58162aefdf297e57bd6aae76da940aaed53` | - | - |
| `phase_ii_format` | `U12` | `false` | `-` | - | - |
| `phase_ii_grammar` | `Z12` | `false` | `-` | - | - |
| `phase_ii_semantic` | `AE12` | `true` | `73021d0499bdbbc34299e07733dda58162aefdf297e57bd6aae76da940aaed53` | None | - |

## Official identity ledger

- status：`aligned`
- canonical / official states：`5` / `5`
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
| `R45.DEBT.opaque_state_body_semantics` | 6 |
| `R45.DEBT.opaque_transition_label_semantics` | 7 |

## NL

```text
1 The human driving mode is represented by a simple state. 2 The autonomous mode has sub-states and is represented by a sub machine state. 3. when power on, the system turn into human driving mode 4when front_distance > 10, auto transport to autonomous state 4. transit to human driving mode when receive human steering cmd, brake pressed, in (auto final) 5 when power off, it will transit to final state
```

## 作者 Phase-II 最终 PlantUML STM0

```plantuml
@startuml
[*] --> HumanDriving
HumanDriving : Human Driving Mode

HumanDriving --> Autonomous : Power On
Autonomous : Autonomous Mode
Autonomous : <<submachine>>

Autonomous --> AutonomousIdle : Front Distance <= 10
AutonomousIdle : Autonomous Idle Mode

AutonomousIdle --> AutonomousActive : Front Distance > 10
AutonomousActive : Autonomous Active Mode

AutonomousActive --> HumanDriving : Human Steering Cmd
AutonomousActive --> HumanDriving : Brake Pressed

HumanDriving --> Autonomous : Front Distance > 10
HumanDriving --> AutonomousFinal : Power Off

AutonomousFinal : Auto Final State
@enduml
```

## 转换后 FCSTM STM0

```fcstm
state llms_emp_feedback_final_0010 named "llms_emp_feedback_final_0010" {
    event Power_On named "Power On";
    event Front_Distance_10 named "Front Distance <= 10";
    event Front_Distance_10_2 named "Front Distance > 10";
    event Human_Steering_Cmd named "Human Steering Cmd";
    event Brake_Pressed named "Brake Pressed";
    event Power_Off named "Power Off";
    state HumanDriving named "HumanDriving\n[PlantUML body] Human Driving Mode";
    state Autonomous named "Autonomous\n[PlantUML body] Autonomous Mode\n[PlantUML body] <<submachine>>";
    state AutonomousIdle named "AutonomousIdle\n[PlantUML body] Autonomous Idle Mode";
    state AutonomousActive named "AutonomousActive\n[PlantUML body] Autonomous Active Mode";
    state AutonomousFinal named "AutonomousFinal\n[PlantUML body] Auto Final State";
    [*] -> HumanDriving;
    HumanDriving -> Autonomous : /Power_On;
    Autonomous -> AutonomousIdle : /Front_Distance_10;
    AutonomousIdle -> AutonomousActive : /Front_Distance_10_2;
    AutonomousActive -> HumanDriving : /Human_Steering_Cmd;
    AutonomousActive -> HumanDriving : /Brake_Pressed;
    HumanDriving -> Autonomous : /Front_Distance_10_2;
    HumanDriving -> AutonomousFinal : /Power_Off;
}
```

[上一组 `0009`](../0009/README.md) | [返回 60 组索引](../../PAIR_INDEX.md) | [下一组 `0011`](../0011/README.md)
