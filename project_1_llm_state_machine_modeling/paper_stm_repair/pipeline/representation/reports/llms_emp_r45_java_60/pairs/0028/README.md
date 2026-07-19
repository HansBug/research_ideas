# Pair `0028`：NL + PlantUML STM0 + FCSTM STM0

[上一组 `0027`](../0027/README.md) | [返回 60 组索引](../../PAIR_INDEX.md) | [下一组 `0029`](../0029/README.md)

- LLM：`Llama`
- 模型/场景： Digital camera state machine diagrams
- NL SHA-256：`6af3966c8b0e12004a22622cded88b07df6fef9d558534442e3309694543c76d`
- PlantUML SHA-256：`ef9eb75e567c05b8516af0e319003e7de3b473791a3b76727595941bb1716d36`
- FCSTM SHA-256：`3e59578a7514f1ab184bf6340d2a995e6ab2e03073e85b6f5f33f320fb567dba`
- 结构裁决：`structure_preserved`
- FCSTM execution eligible：`false`
- Discover eligible：`false`
- 主 session 对读：Camera 19 state、25 edge 与两个 final 齐；fan-out/timing/body 仅结构保存。
- 三个原始文件：[NL](./nl.txt) | [PlantUML](./plantuml.puml) | [FCSTM](./fcstm.fcstm)
- 审计入口：[canonical](../../canonical/llms_emp_stm_results_0028.json) | [冻结 FCSTM](../../fcstm/llms_emp_stm_results_0028.fcstm) | [case report](../../case_reports/llms_emp_stm_results_0028.json) | [人工总账](../../MANUAL_REVIEW.md)

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
stm CameraSystem
[*] --> TurnOn
TurnOn: TurnOn, min: 2s, max: 2s
TurnOn --> fork1: after 2s
fork1 --> AutoFocus: min: 1s, max: 2s
fork1 --> DetLight: min: 0s, max: 1s
fork1 --> choice3:
AutoFocus --> choice1: memFull=true
choice1 --> choice3:
DetLight --> choice2: <<GaStep>>{prob=0.4}
choice2 --> Join2: sunny=true
choice2 --> Join1:
choice3 --> ChargedFlash: min: 2s, max: 4s
ChargedFlash --> Junction3: Charged=true
Junction3 --> Join2:
choice3 --> Junction3:
Junction2 --> TakePicture: min: 2s, max: 3s
TakePicture --> WriteMemory:
WriteMemory --> Junction1:
Junction1 --> TurnOff:
TurnOff --> [*]:
Join2 --> Fork2:
Fork2 --> Junction2:
Fork2 --> Flash:
Flash --> Terminate:
@enduml
```

## 转换后 FCSTM STM0

```fcstm
state llms_emp_stm_results_0028 named "CameraSystem" {
    event after_2s named "after 2s";
    event min_1s_max_2s named "min: 1s, max: 2s";
    event min_0s_max_1s named "min: 0s, max: 1s";
    event memFull_true named "memFull=true";
    event _GaStep_prob_0_4 named "<<GaStep>>{prob=0.4}";
    event sunny_true named "sunny=true";
    event min_2s_max_4s named "min: 2s, max: 4s";
    event Charged_true named "Charged=true";
    event min_2s_max_3s named "min: 2s, max: 3s";
    state TurnOn named "TurnOn\n[PlantUML body] TurnOn, min: 2s, max: 2s";
    state fork1 named "fork1";
    state AutoFocus named "AutoFocus";
    state DetLight named "DetLight";
    state choice3 named "choice3";
    state choice1 named "choice1";
    state choice2 named "choice2";
    state Join2 named "Join2";
    state Join1 named "Join1";
    state ChargedFlash named "ChargedFlash";
    state Junction3 named "Junction3";
    state Junction2 named "Junction2";
    state TakePicture named "TakePicture";
    state WriteMemory named "WriteMemory";
    state Junction1 named "Junction1";
    state TurnOff named "TurnOff";
    state Fork2 named "Fork2";
    state Flash named "Flash";
    state Terminate named "Terminate";
    [*] -> TurnOn;
    TurnOn -> fork1 : /after_2s;
    fork1 -> AutoFocus : /min_1s_max_2s;
    fork1 -> DetLight : /min_0s_max_1s;
    fork1 -> choice3;
    AutoFocus -> choice1 : /memFull_true;
    choice1 -> choice3;
    DetLight -> choice2 : /_GaStep_prob_0_4;
    choice2 -> Join2 : /sunny_true;
    choice2 -> Join1;
    choice3 -> ChargedFlash : /min_2s_max_4s;
    ChargedFlash -> Junction3 : /Charged_true;
    Junction3 -> Join2;
    choice3 -> Junction3;
    Junction2 -> TakePicture : /min_2s_max_3s;
    TakePicture -> WriteMemory;
    WriteMemory -> Junction1;
    Junction1 -> TurnOff;
    TurnOff -> [*];
    Join2 -> Fork2;
    Fork2 -> Junction2;
    Fork2 -> Flash;
    Flash -> Terminate;
}
```

[上一组 `0027`](../0027/README.md) | [返回 60 组索引](../../PAIR_INDEX.md) | [下一组 `0029`](../0029/README.md)
