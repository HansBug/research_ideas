# Pair `0057`：NL + PlantUML STM0 + FCSTM STM0

[上一组 `0056`](../0056/README.md) | [返回 60 组索引](../../PAIR_INDEX.md) | [下一组 `0058`](../0058/README.md)

- LLM：`Claude`
- 模型/场景：Collision avoidance sub-machine state diagram
- 作者输出阶段：`Result with Semantic Checking`
- 作者输出单元格：`AE59`；Excel row：`59`
- Phase-I fallback：`false`
- 相对 Phase-I 是否变化：`true`
- Phase-I PlantUML SHA-256：`6678019769df574ad084ce86bfe39e078fce4203e6de76b77755b89c3d037a79`
- NL SHA-256：`49854d044ad99f16a710021500f5e972da93b27635a41144d9b91d32444c0f63`
- PlantUML SHA-256：`dad4f00d0dfce1ab40970f524ea2c95d2c8c9b1e1480b91287c5a009e2662c3c`
- FCSTM SHA-256：`2ef295e6a539dd6a406ba83e12356c94f8d9c14057e9059f437b6d912797da57`
- 结构裁决：`structure_preserved`
- source states / transitions：`10` / `10`
- mapped / blocked / silent drop：`10` / `0` / `0`
- final / lifecycle / body coverage：`0/0` / `0/0` / `0/0`
- concurrent region / separator coverage：`0/0` / `0/0`
- source normalization coverage：`0/0`
- official raw / validation：`state_diagram` / `state_diagram`
- official identity states / transitions：`10` / `10`
- official identity remaps：state `0` / transition endpoint `0`
- AST audit：`passed`
- FCSTM execution eligible：`false`
- Discover eligible：`false`
- 主 session 对读：完整对读：CA 下 Frontend/RearEnd/Pedestrian 三 composite 及各自 Idle/Active 共 10 状态、10 边全在；带 Possible collision 的 root initial 使用 wait，CA 无单一 child initial 以 UnspecifiedInitial 留债。
- 三个原始文件：[NL](./nl.txt) | [PlantUML](./plantuml.puml) | [FCSTM](./fcstm.fcstm)
- 审计入口：[canonical](../../canonical/llms_emp_feedback_final_0057.json) | [冻结 FCSTM](../../fcstm/llms_emp_feedback_final_0057.fcstm) | [case report](../../case_reports/llms_emp_feedback_final_0057.json) | [人工总账](../../MANUAL_REVIEW.md)

## 作者阶段 lineage

| stage | output cell | present | output SHA-256 | feedback | resolved |
|---|---|---|---|---|---|
| `phase_i_generation` | `I59` | `true` | `6678019769df574ad084ce86bfe39e078fce4203e6de76b77755b89c3d037a79` | - | - |
| `phase_ii_format` | `U59` | `false` | `-` | - | - |
| `phase_ii_grammar` | `Z59` | `false` | `-` | - | - |
| `phase_ii_semantic` | `AE59` | `true` | `dad4f00d0dfce1ab40970f524ea2c95d2c8c9b1e1480b91287c5a009e2662c3c` | 1. missing region | - |

## Official identity ledger

- status：`aligned`
- canonical / official states：`10` / `10`
- aligned transition endpoints：`10`

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
| `R45.DEBT.opaque_transition_label_semantics` | 7 |

## NL

```text
1. There are three region in this diagram
2. This sub-machine becomes active when a possible frontend collision, rear-end collision or collision with pedestrian is detected.
3. The orthogonal regions of the active mode of collision avoidance allow for concurrent activation different of collision avoidance controls.
```

## 作者 Phase-II 最终 PlantUML STM0

```plantuml
@startuml
state "Collision Avoidance" as CA {
state Frontend {
[*] --> FCIdle
FCIdle --> FCActive : Frontend collision detected
FCActive --> FCIdle : Collision avoided
}

state RearEnd {
[*] --> RCIdle
RCIdle --> RCActive : Rear-end collision detected
RCActive --> RCIdle : Collision avoided
}

state Pedestrian {
[*] --> PCIdle
PCIdle --> PCActive : Pedestrian collision detected
PCActive --> PCIdle : Collision avoided
}
}

[*] --> CA : Possible collision detected
@enduml
```

## 转换后 FCSTM STM0

```fcstm
state llms_emp_feedback_final_0057 named "llms_emp_feedback_final_0057" {
    event Frontend_collision_detected named "Frontend collision detected";
    event Collision_avoided named "Collision avoided";
    event Rear_end_collision_detected named "Rear-end collision detected";
    event Pedestrian_collision_detected named "Pedestrian collision detected";
    event Possible_collision_detected named "Possible collision detected";
    state InitialWaittr_0010 named "Awaiting initial event: Possible collision detected";
    state CA named "Collision Avoidance" {
        state UnspecifiedInitial named "Unspecified initial";
        state Frontend named "Frontend" {
            state FCIdle named "FCIdle";
            state FCActive named "FCActive";
            [*] -> FCIdle;
            FCIdle -> FCActive : /Frontend_collision_detected;
            FCActive -> FCIdle : /Collision_avoided;
        }
        state RearEnd named "RearEnd" {
            state RCIdle named "RCIdle";
            state RCActive named "RCActive";
            [*] -> RCIdle;
            RCIdle -> RCActive : /Rear_end_collision_detected;
            RCActive -> RCIdle : /Collision_avoided;
        }
        state Pedestrian named "Pedestrian" {
            state PCIdle named "PCIdle";
            state PCActive named "PCActive";
            [*] -> PCIdle;
            PCIdle -> PCActive : /Pedestrian_collision_detected;
            PCActive -> PCIdle : /Collision_avoided;
        }
        [*] -> UnspecifiedInitial;
    }
    [*] -> InitialWaittr_0010;
    InitialWaittr_0010 -> CA : /Possible_collision_detected;
}
```

[上一组 `0056`](../0056/README.md) | [返回 60 组索引](../../PAIR_INDEX.md) | [下一组 `0058`](../0058/README.md)
