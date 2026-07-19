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
- FCSTM execution eligible：`false`
- Discover eligible：`false`
- 主 session 对读：完整对读：Off 与 Operate 三子态共 5 状态、9 边逐一保留；Operate 跨层 keyOff 使用 forced exit，Off 的 shutdown 仍是带事件 root final，内部加速/制动/停止链无遗漏。
- 三个原始文件：[NL](./nl.txt) | [PlantUML](./plantuml.puml) | [FCSTM](./fcstm.fcstm)
- 审计入口：[canonical](../../canonical/llms_emp_feedback_final_0052.json) | [冻结 FCSTM](../../fcstm/llms_emp_feedback_final_0052.fcstm) | [case report](../../case_reports/llms_emp_feedback_final_0052.json) | [人工总账](../../MANUAL_REVIEW.md)

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
