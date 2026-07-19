# Pair `0058`：NL + PlantUML STM0 + FCSTM STM0

[上一组 `0057`](../0057/README.md) | [返回 60 组索引](../../PAIR_INDEX.md) | [下一组 `0059`](../0059/README.md)

- LLM：`Claude`
- 模型/场景： Digital camera state machine diagrams
- NL SHA-256：`6af3966c8b0e12004a22622cded88b07df6fef9d558534442e3309694543c76d`
- PlantUML SHA-256：`5181a79ba0047ffa94d309464ba44fa0600aa5f0c939e20cd72a7f8ad674bea5`
- FCSTM SHA-256：`be359318c44dcd6785b7f3e2daf75f4a22fdd041b236ba9dd0ea43ddf15de5cf`
- 结构裁决：`structure_preserved`
- FCSTM execution eligible：`false`
- Discover eligible：`false`
- 主 session 对读：root-to-deep priority route、fork 三出边、22条 macro、6个 placeholder与 scoped `Join2.fork2/Flash` 齐；并发不推断。
- 三个原始文件：[NL](./nl.txt) | [PlantUML](./plantuml.puml) | [FCSTM](./fcstm.fcstm)
- 审计入口：[canonical](../../canonical/llms_emp_stm_results_0058.json) | [冻结 FCSTM](../../fcstm/llms_emp_stm_results_0058.fcstm) | [case report](../../case_reports/llms_emp_stm_results_0058.json) | [人工总账](../../MANUAL_REVIEW.md)

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

state TurnOn {
state "TurnOn" as TurnOn_state
}
TurnOn_state : {max=2s, min=2s}

[*] --> TurnOn_state
TurnOn_state --> fork1

fork fork1
fork1 --> AutoFocus
fork1 --> DetLight
fork1 --> choice3

state AutoFocus {
state "AutoFocus" as AutoFocus_state
}
AutoFocus_state : {max=2s, min=1s}

AutoFocus_state --> choice1 : [memFull=true]

state DetLight {
state "DetLight" as DetLight_state
}
DetLight_state : {max=1s, min=0s}

DetLight_state --> choice2 : <<GaStep>>{prob=0.4}

state ChargedFlash {
state "ChargedFlash" as ChargedFlash_state
}
ChargedFlash_state : {max=4s, min=2s}

choice3 --> ChargedFlash_state
ChargedFlash_state --> Junction3 : [Charged=true]
choice3 --> Junction3

Junction3 --> Join2

choice2 --> Join2
choice2 --> Join1 : [sunny=true]

Join1 --> Junction2

Junction2 --> TakePicture
TakePicture --> WriteMemory
state WriteMemory {
state "WriteMemory" as WriteMemory_state
}
WriteMemory_state : {max=3s, min=2s}

WriteMemory_state --> Junction1
Junction1 --> TurnOff
TurnOff --> [*]

state Join2 {
fork2 --> Junction2
fork2 --> Flash
}

Flash --> Terminate

@enduml
```

## 转换后 FCSTM STM0

```fcstm
state llms_emp_stm_results_0058 named "llms_emp_stm_results_0058" {
    event _memFull_true named "[memFull=true]";
    event _GaStep_prob_0_4 named "<<GaStep>>{prob=0.4}";
    event _Charged_true named "[Charged=true]";
    event _sunny_true named "[sunny=true]";
    state TurnOn named "TurnOn" {
        state UnspecifiedInitial named "Unspecified initial";
        state TurnOn_state named "TurnOn\n[PlantUML body] {max=2s, min=2s}";
        [*] -> TurnOn_state;
        TurnOn_state -> [*];
        [*] -> UnspecifiedInitial;
    }
    pseudo state fork1 named "fork1";
    state AutoFocus named "AutoFocus" {
        state UnspecifiedInitial named "Unspecified initial";
        state AutoFocus_state named "AutoFocus\n[PlantUML body] {max=2s, min=1s}";
        AutoFocus_state -> [*] : /_memFull_true;
        [*] -> UnspecifiedInitial;
    }
    state DetLight named "DetLight" {
        state UnspecifiedInitial named "Unspecified initial";
        state DetLight_state named "DetLight\n[PlantUML body] {max=1s, min=0s}";
        DetLight_state -> [*] : /_GaStep_prob_0_4;
        [*] -> UnspecifiedInitial;
    }
    state ChargedFlash named "ChargedFlash" {
        state UnspecifiedInitial named "Unspecified initial";
        state ChargedFlash_state named "ChargedFlash\n[PlantUML body] {max=4s, min=2s}";
        [*] -> ChargedFlash_state;
        ChargedFlash_state -> [*] : /_Charged_true;
        [*] -> UnspecifiedInitial;
    }
    state WriteMemory named "WriteMemory" {
        state UnspecifiedInitial named "Unspecified initial";
        state WriteMemory_state named "WriteMemory\n[PlantUML body] {max=3s, min=2s}";
        WriteMemory_state -> [*];
        [*] -> UnspecifiedInitial;
    }
    state Join2 named "Join2" {
        state UnspecifiedInitial named "Unspecified initial";
        state fork2 named "fork2";
        state Flash named "Flash";
        fork2 -> [*];
        fork2 -> Flash;
        [*] -> UnspecifiedInitial;
    }
    state choice3 named "choice3";
    state choice1 named "choice1";
    state choice2 named "choice2";
    state Junction3 named "Junction3";
    state Join1 named "Join1";
    state Junction2 named "Junction2";
    state TakePicture named "TakePicture";
    state Junction1 named "Junction1";
    state TurnOff named "TurnOff";
    state Flash named "Flash";
    state Terminate named "Terminate";
    [*] -> TurnOn;
    TurnOn -> fork1;
    fork1 -> AutoFocus;
    fork1 -> DetLight;
    fork1 -> choice3;
    AutoFocus -> choice1 : /_memFull_true;
    DetLight -> choice2 : /_GaStep_prob_0_4;
    choice3 -> ChargedFlash;
    ChargedFlash -> Junction3 : /_Charged_true;
    choice3 -> Junction3;
    Junction3 -> Join2;
    choice2 -> Join2;
    choice2 -> Join1 : /_sunny_true;
    Join1 -> Junction2;
    Junction2 -> TakePicture;
    TakePicture -> WriteMemory;
    WriteMemory -> Junction1;
    Junction1 -> TurnOff;
    TurnOff -> [*];
    Join2 -> Junction2;
    Flash -> Terminate;
}
```

[上一组 `0057`](../0057/README.md) | [返回 60 组索引](../../PAIR_INDEX.md) | [下一组 `0059`](../0059/README.md)
