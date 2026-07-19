# Pair `0050`：NL + PlantUML STM0 + FCSTM STM0

[上一组 `0049`](../0049/README.md) | [返回 60 组索引](../../PAIR_INDEX.md) | [下一组 `0051`](../0051/README.md)

- LLM：`Claude`
- 模型/场景：high-level driving module
- 作者输出阶段：`Result with Semantic Checking`
- 作者输出单元格：`AE52`；Excel row：`52`
- Phase-I fallback：`false`
- 相对 Phase-I 是否变化：`false`
- Phase-I PlantUML SHA-256：`317f517490d7ed5d6520fc8f56045625d4d9c9b870a058e6a0f1d2c21a1e24e4`
- NL SHA-256：`f1c3dc88371b8256352e7ab6ee7eb42424de6e11dfde70d185f224dd1d05a7a8`
- PlantUML SHA-256：`317f517490d7ed5d6520fc8f56045625d4d9c9b870a058e6a0f1d2c21a1e24e4`
- FCSTM SHA-256：`e177a0ff8af9e12db063c42b377b8615e99f9fd4b1825ab51ee71d7e3364f8a4`
- 结构裁决：`structure_preserved`
- source states / transitions：`5` / `9`
- mapped / blocked / silent drop：`9` / `0` / `0`
- final / lifecycle / body coverage：`3/3` / `0/0` / `0/0`
- concurrent region / separator coverage：`0/0` / `0/0`
- source normalization coverage：`0/0`
- official raw / validation：`state_diagram` / `state_diagram`
- official identity states / transitions：`5` / `9`
- official identity remaps：state `0` / transition endpoint `0`
- AST audit：`passed`
- FCSTM execution eligible：`false`
- Discover eligible：`false`
- 主 session 对读：完整对读：HumanDrivingMode 空 composite、AutonomousMode 三子态共 5 状态、9 边全在；带事件 root initial、局部 final wait、两个 Power Off root final 均保留，HumanDriving 缺 child initial 留债。
- 三个原始文件：[NL](./nl.txt) | [PlantUML](./plantuml.puml) | [FCSTM](./fcstm.fcstm)
- 审计入口：[canonical](../../canonical/llms_emp_feedback_final_0050.json) | [冻结 FCSTM](../../fcstm/llms_emp_feedback_final_0050.fcstm) | [case report](../../case_reports/llms_emp_feedback_final_0050.json) | [人工总账](../../MANUAL_REVIEW.md)

## 作者阶段 lineage

| stage | output cell | present | output SHA-256 | feedback | resolved |
|---|---|---|---|---|---|
| `phase_i_generation` | `I52` | `true` | `317f517490d7ed5d6520fc8f56045625d4d9c9b870a058e6a0f1d2c21a1e24e4` | - | - |
| `phase_ii_format` | `U52` | `false` | `-` | - | - |
| `phase_ii_grammar` | `Z52` | `false` | `-` | - | - |
| `phase_ii_semantic` | `AE52` | `true` | `317f517490d7ed5d6520fc8f56045625d4d9c9b870a058e6a0f1d2c21a1e24e4` | None | - |

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
| `R45.DEBT.missing_explicit_initial` | 1 |
| `R45.DEBT.opaque_transition_label_semantics` | 5 |

## NL

```text
1 The human driving mode is represented by a simple state. 2 The autonomous mode has sub-states and is represented by a sub machine state. 3. when power on, the system turn into human driving mode 4when front_distance > 10, auto transport to autonomous state 4. transit to human driving mode when receive human steering cmd, brake pressed, in (auto final) 5 when power off, it will transit to final state
```

## 作者 Phase-II 最终 PlantUML STM0

```plantuml
@startuml

[*] --> HumanDrivingMode : Power On

state HumanDrivingMode {
}

state AutonomousMode {
[*] --> SubState1
SubState1 --> SubState2
SubState2 --> SubState3
SubState3 --> [*]
}

HumanDrivingMode --> AutonomousMode : [front_distance > 10]

AutonomousMode --> HumanDrivingMode : human steering cmd\nor brake pressed\nor in (auto final)

HumanDrivingMode --> [*] : Power Off
AutonomousMode --> [*] : Power Off

@enduml
```

## 转换后 FCSTM STM0

```fcstm
state llms_emp_feedback_final_0050 named "llms_emp_feedback_final_0050" {
    event Power_On named "Power On";
    event _front_distance_10 named "[front_distance > 10]";
    event human_steering_cmd_nor_brake_pressed_nor_in_auto_final named "human steering cmd\\nor brake pressed\\nor in (auto final)";
    event Power_Off named "Power Off";
    state InitialWaittr_0001 named "Awaiting initial event: Power On";
    state HumanDrivingMode named "HumanDrivingMode" {
        state UnspecifiedInitial named "Unspecified initial";
        [*] -> UnspecifiedInitial;
    }
    state AutonomousMode named "AutonomousMode" {
        state SubState1 named "SubState1";
        state SubState2 named "SubState2";
        state SubState3 named "SubState3";
        state FinalWaittr_0005 named "Completed final boundary: AutonomousMode.SubState3";
        [*] -> SubState1;
        SubState1 -> SubState2;
        SubState2 -> SubState3;
        SubState3 -> FinalWaittr_0005;
    }
    [*] -> InitialWaittr_0001;
    InitialWaittr_0001 -> HumanDrivingMode : /Power_On;
    !HumanDrivingMode -> AutonomousMode : /_front_distance_10;
    !AutonomousMode -> HumanDrivingMode : /human_steering_cmd_nor_brake_pressed_nor_in_auto_final;
    !HumanDrivingMode -> [*] : /Power_Off;
    !AutonomousMode -> [*] : /Power_Off;
}
```

[上一组 `0049`](../0049/README.md) | [返回 60 组索引](../../PAIR_INDEX.md) | [下一组 `0051`](../0051/README.md)
