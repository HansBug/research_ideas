# Pair `0047`：NL + PlantUML STM0 + FCSTM STM0

[上一组 `0046`](../0046/README.md) | [返回 60 组索引](../../PAIR_INDEX.md) | [下一组 `0048`](../0048/README.md)

- LLM：`DeepSeek`
- 模型/场景：Collision avoidance sub-machine state diagram
- NL SHA-256：`49854d044ad99f16a710021500f5e972da93b27635a41144d9b91d32444c0f63`
- PlantUML SHA-256：`fff82632ec465f502612c40dfe4ccf552d9cf88db9e0074d533201587108ebd0`
- FCSTM SHA-256：`859be926a59315b66b8b699863aa958d0c80a1c466405b9b2c1e5af20ebaa585`
- 结构裁决：`structure_preserved`
- FCSTM execution eligible：`false`
- Discover eligible：`false`
- 主 session 对读：三 alias composite 及 scoped Idle/Braking/Clamping 独立；3 final 齐；root 缺 initial fail-closed。
- 三个原始文件：[NL](./nl.txt) | [PlantUML](./plantuml.puml) | [FCSTM](./fcstm.fcstm)
- 审计入口：[canonical](../../canonical/llms_emp_stm_results_0047.json) | [冻结 FCSTM](../../fcstm/llms_emp_stm_results_0047.fcstm) | [case report](../../case_reports/llms_emp_stm_results_0047.json) | [人工总账](../../MANUAL_REVIEW.md)

## NL

```text
1. There are three region in this diagram
2. This sub-machine becomes active when a possible frontend collision, rear-end collision or collision with pedestrian is detected.
3. The orthogonal regions of the active mode of collision avoidance allow for concurrent activation different of collision avoidance controls.
```

## 原装 PlantUML STM0

```plantuml
@startuml
stm CollisionAvoidanceSystem [Collision Avoidance State Machine]

state "Frontend Collision Avoidance" as Frontend {
[*] --> Idle
Idle --> Braking : Collision Detected
Braking --> Clamping : Brake Applied
Clamping --> Idle : Collision Avoided
}

state "Rear-End Collision Avoidance" as RearEnd {
[*] --> Idle
Idle --> Braking : Collision Detected
Braking --> Clamping : Brake Applied
Clamping --> Idle : Collision Avoided
}

state "Pedestrian Collision Avoidance" as Pedestrian {
[*] --> Idle
Idle --> Braking : Collision Detected
Braking --> Clamping : Brake Applied
Clamping --> Idle : Collision Avoided
}

Frontend --> [*] : Collision Avoided
RearEnd --> [*] : Collision Avoided
Pedestrian --> [*] : Collision Avoided

@enduml
```

## 转换后 FCSTM STM0

```fcstm
state llms_emp_stm_results_0047 named "CollisionAvoidanceSystem [Collision Avoidance State Machine]" {
    event Collision_Detected named "Collision Detected";
    event Brake_Applied named "Brake Applied";
    event Collision_Avoided named "Collision Avoided";
    state UnspecifiedInitial named "Unspecified initial";
    state Frontend named "Frontend Collision Avoidance" {
        state Idle named "Idle";
        state Braking named "Braking";
        state Clamping named "Clamping";
        [*] -> Idle;
        Idle -> Braking : /Collision_Detected;
        Braking -> Clamping : /Brake_Applied;
        Clamping -> Idle : /Collision_Avoided;
    }
    state RearEnd named "Rear-End Collision Avoidance" {
        state Idle named "Idle";
        state Braking named "Braking";
        state Clamping named "Clamping";
        [*] -> Idle;
        Idle -> Braking : /Collision_Detected;
        Braking -> Clamping : /Brake_Applied;
        Clamping -> Idle : /Collision_Avoided;
    }
    state Pedestrian named "Pedestrian Collision Avoidance" {
        state Idle named "Idle";
        state Braking named "Braking";
        state Clamping named "Clamping";
        [*] -> Idle;
        Idle -> Braking : /Collision_Detected;
        Braking -> Clamping : /Brake_Applied;
        Clamping -> Idle : /Collision_Avoided;
    }
    !Frontend -> [*] : /Collision_Avoided;
    !RearEnd -> [*] : /Collision_Avoided;
    !Pedestrian -> [*] : /Collision_Avoided;
    [*] -> UnspecifiedInitial;
}
```

[上一组 `0046`](../0046/README.md) | [返回 60 组索引](../../PAIR_INDEX.md) | [下一组 `0048`](../0048/README.md)
