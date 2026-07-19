# Pair `0048`：NL + PlantUML STM0 + FCSTM STM0

[上一组 `0047`](../0047/README.md) | [返回 60 组索引](../../PAIR_INDEX.md) | [下一组 `0049`](../0049/README.md)

- LLM：`DeepSeek`
- 模型/场景： Digital camera state machine diagrams
- NL SHA-256：`6af3966c8b0e12004a22622cded88b07df6fef9d558534442e3309694543c76d`
- PlantUML SHA-256：`91951da63cfb9eef882f8f3b45d69fbba6c22dcc4c1f1247dd4a7f91a2f079ab`
- FCSTM SHA-256：`693151e680a8b4c6dd33ec78a7630dc9391ad8d42e960e7fd274077c1b82ae0a`
- 结构裁决：`structure_preserved`
- FCSTM execution eligible：`false`
- Discover eligible：`false`
- 主 session 对读：19 state、24 edge、两个 final、fan-out 与 timing body 均保留。
- 三个原始文件：[NL](./nl.txt) | [PlantUML](./plantuml.puml) | [FCSTM](./fcstm.fcstm)
- 审计入口：[canonical](../../canonical/llms_emp_stm_results_0048.json) | [冻结 FCSTM](../../fcstm/llms_emp_stm_results_0048.fcstm) | [case report](../../case_reports/llms_emp_stm_results_0048.json) | [人工总账](../../MANUAL_REVIEW.md)

## NL

```text
1. The system begins in the TurnOn state, which has two possible execution times, with a maximum of 2 seconds and a minimum of 2 seconds, before transitioning to the fork1 state.
2. The TurnOn state transitions into a fork1 state, which contains parallel paths leading to AutoFocus and DetLight.
3. The AutoFocus state has execution times of 2 seconds maximum and 1 second minimum before proceeding to the choice1 state, which is triggered when the condition memFull=true is true.
4. The DetLight state has execution times of 1 second maximum and 0 seconds minimum, transitioning to the choice2 state when the condition <>{prob=0.4} is met.
5. If the fork1 state transitions to choice3, it proceeds to the ChargedFlash state, which has execution times of 4 seconds maximum and 2 seconds minimum.
6. The ChargedFlash state can lead to Junction3, where the system starts and proceeds to the Join2 state. The transition occurs when Charged=true.
7. The choice3 state also transitions to Junction3, and once the system reaches Junction3, it joins the Join2 state.
8. The choice2 state transitions to Join2, and if the condition sunny=true is met, it further joins the Join1 state, which leads to Junction2.
9. In the Junction2 state, the system proceeds to TakePicture, followed by WriteMemory, with execution times of 3 seconds maximum and 2 seconds minimum.
10. After WriteMemory completes, the system enters Junction1 before proceeding to TurnOff, which ends the process and transitions back to the initial state, represented by [*].
11. In the Fork2 state, which is part of the Join2 substate, the system can either proceed to Junction2 or Flash. If the Flash state is activated, it transitions to Terminate, ending the sequence.
```

## 原装 PlantUML STM0

```plantuml
@startuml
stm [stateMachine] SystemStateMachine [SystemStateMachineDiagram]

[*] --> TurnOn
TurnOn : max=2s, min=2s
TurnOn --> fork1

fork1 --> AutoFocus
fork1 --> DetLight

AutoFocus : max=2s, min=1s
AutoFocus --> choice1 : [memFull=true]

DetLight : max=1s, min=0s
DetLight --> choice2 : <<GaStep>>{prob=0.4}

fork1 --> choice3
choice3 --> ChargedFlash
ChargedFlash : max=4s, min=2s
ChargedFlash --> Junction3 : [Charged=true]
choice3 --> Junction3
Junction3 --> Join2

choice2 --> Join2 : [sunny=true]
Join2 --> Join1
Join1 --> Junction2

Junction2 --> TakePicture
TakePicture --> WriteMemory
WriteMemory : max=3s, min=2s
WriteMemory --> Junction1
Junction1 --> TurnOff
TurnOff --> [*]

Join2 --> Fork2
Fork2 --> Junction2
Fork2 --> Flash
Flash --> Terminate
Terminate --> [*]

@enduml
```

## 转换后 FCSTM STM0

```fcstm
state llms_emp_stm_results_0048 named "[stateMachine] SystemStateMachine [SystemStateMachineDiagram]" {
    event _memFull_true named "[memFull=true]";
    event _GaStep_prob_0_4 named "<<GaStep>>{prob=0.4}";
    event _Charged_true named "[Charged=true]";
    event _sunny_true named "[sunny=true]";
    state TurnOn named "TurnOn\n[PlantUML body] max=2s, min=2s";
    state AutoFocus named "AutoFocus\n[PlantUML body] max=2s, min=1s";
    state DetLight named "DetLight\n[PlantUML body] max=1s, min=0s";
    state ChargedFlash named "ChargedFlash\n[PlantUML body] max=4s, min=2s";
    state WriteMemory named "WriteMemory\n[PlantUML body] max=3s, min=2s";
    state fork1 named "fork1";
    state choice1 named "choice1";
    state choice2 named "choice2";
    state choice3 named "choice3";
    state Junction3 named "Junction3";
    state Join2 named "Join2";
    state Join1 named "Join1";
    state Junction2 named "Junction2";
    state TakePicture named "TakePicture";
    state Junction1 named "Junction1";
    state TurnOff named "TurnOff";
    state Fork2 named "Fork2";
    state Flash named "Flash";
    state Terminate named "Terminate";
    [*] -> TurnOn;
    TurnOn -> fork1;
    fork1 -> AutoFocus;
    fork1 -> DetLight;
    AutoFocus -> choice1 : /_memFull_true;
    DetLight -> choice2 : /_GaStep_prob_0_4;
    fork1 -> choice3;
    choice3 -> ChargedFlash;
    ChargedFlash -> Junction3 : /_Charged_true;
    choice3 -> Junction3;
    Junction3 -> Join2;
    choice2 -> Join2 : /_sunny_true;
    Join2 -> Join1;
    Join1 -> Junction2;
    Junction2 -> TakePicture;
    TakePicture -> WriteMemory;
    WriteMemory -> Junction1;
    Junction1 -> TurnOff;
    TurnOff -> [*];
    Join2 -> Fork2;
    Fork2 -> Junction2;
    Fork2 -> Flash;
    Flash -> Terminate;
    Terminate -> [*];
}
```

[上一组 `0047`](../0047/README.md) | [返回 60 组索引](../../PAIR_INDEX.md) | [下一组 `0049`](../0049/README.md)
