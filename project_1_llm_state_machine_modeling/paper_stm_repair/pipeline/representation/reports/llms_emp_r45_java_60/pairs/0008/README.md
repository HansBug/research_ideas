# Pair `0008`：NL + PlantUML STM0 + FCSTM STM0

[上一组 `0007`](../0007/README.md) | [返回 60 组索引](../../PAIR_INDEX.md) | [下一组 `0009`](../0009/README.md)

- LLM：`GPT-4o`
- 模型/场景： Digital camera state machine diagrams
- NL SHA-256：`6af3966c8b0e12004a22622cded88b07df6fef9d558534442e3309694543c76d`
- PlantUML SHA-256：`0d7b489764211f6857eb71ab15af67f692a637c2a2a548b5e5ce7d88f255cbd2`
- FCSTM SHA-256：`04e146e89698d5dfe07aa877ab0774af3fd94022ba3bd3dd4b0edb313bf03a2a`
- 结构裁决：`structure_preserved`
- FCSTM execution eligible：`false`
- Discover eligible：`false`
- 主 session 对读：28 state、27 transition、多个 scoped `ExecutionTime/Junction1` 与 TurnOff nested final 完整；时间/概率仅 opaque。
- 三个原始文件：[NL](./nl.txt) | [PlantUML](./plantuml.puml) | [FCSTM](./fcstm.fcstm)
- 审计入口：[canonical](../../canonical/llms_emp_stm_results_0008.json) | [冻结 FCSTM](../../fcstm/llms_emp_stm_results_0008.fcstm) | [case report](../../case_reports/llms_emp_stm_results_0008.json) | [人工总账](../../MANUAL_REVIEW.md)

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
[*] --> TurnOn
state TurnOn {
  [*] --> ExecutionTime
  ExecutionTime --> fork1 : after 2s
}

fork1 --> AutoFocus
fork1 --> DetLight

state AutoFocus {
  [*] --> ExecutionTime
  ExecutionTime --> choice1 : after 1s
}

state DetLight {
  [*] --> ExecutionTime
  ExecutionTime --> choice2 : <<GaStep>>{prob=0.4}
}

fork1 --> choice3

choice1 --> Junction3 : memFull=true
choice3 --> ChargedFlash

state ChargedFlash {
  [*] --> ExecutionTime
  ExecutionTime --> Junction3 : after 2s
}

Junction3 --> Join2 : Charged=true

choice2 --> Join2
Join2 --> Fork2

Fork2 --> Junction2
Fork2 --> Flash

Flash --> Terminate

Junction2 --> TakePicture
TakePicture --> WriteMemory

state WriteMemory {
  [*] --> ExecutionTime
  ExecutionTime --> Junction1 : after 2s
}

Junction1 --> TurnOff

state TurnOff {
  [*] --> ExecutionTime
  ExecutionTime --> [*] : after 2s
}
@enduml
```

## 转换后 FCSTM STM0

```fcstm
state llms_emp_stm_results_0008 named "llms_emp_stm_results_0008" {
    event after_2s named "after 2s";
    event after_1s named "after 1s";
    event _GaStep_prob_0_4 named "<<GaStep>>{prob=0.4}";
    event memFull_true named "memFull=true";
    event Charged_true named "Charged=true";
    state TurnOn named "TurnOn" {
        state ExecutionTime named "ExecutionTime";
        state fork1 named "fork1";
        [*] -> ExecutionTime;
        ExecutionTime -> fork1 : /after_2s;
    }
    state AutoFocus named "AutoFocus" {
        state ExecutionTime named "ExecutionTime";
        state choice1 named "choice1";
        [*] -> ExecutionTime;
        ExecutionTime -> choice1 : /after_1s;
    }
    state DetLight named "DetLight" {
        state ExecutionTime named "ExecutionTime";
        state choice2 named "choice2";
        [*] -> ExecutionTime;
        ExecutionTime -> choice2 : /_GaStep_prob_0_4;
    }
    state ChargedFlash named "ChargedFlash" {
        state ExecutionTime named "ExecutionTime";
        [*] -> ExecutionTime;
        ExecutionTime -> [*] : /after_2s;
    }
    state WriteMemory named "WriteMemory" {
        state ExecutionTime named "ExecutionTime";
        state Junction1 named "Junction1";
        [*] -> ExecutionTime;
        ExecutionTime -> Junction1 : /after_2s;
    }
    state TurnOff named "TurnOff" {
        state ExecutionTime named "ExecutionTime";
        state FinalWaittr_0027 named "Completed final boundary: TurnOff.ExecutionTime";
        [*] -> ExecutionTime;
        ExecutionTime -> FinalWaittr_0027 : /after_2s;
    }
    state fork1 named "fork1";
    state choice3 named "choice3";
    state choice1 named "choice1";
    state Junction3 named "Junction3";
    state Join2 named "Join2";
    state choice2 named "choice2";
    state Fork2 named "Fork2";
    state Junction2 named "Junction2";
    state Flash named "Flash";
    state Terminate named "Terminate";
    state TakePicture named "TakePicture";
    state Junction1 named "Junction1";
    [*] -> TurnOn;
    fork1 -> AutoFocus;
    fork1 -> DetLight;
    fork1 -> choice3;
    choice1 -> Junction3 : /memFull_true;
    choice3 -> ChargedFlash;
    ChargedFlash -> Junction3 : /after_2s;
    Junction3 -> Join2 : /Charged_true;
    choice2 -> Join2;
    Join2 -> Fork2;
    Fork2 -> Junction2;
    Fork2 -> Flash;
    Flash -> Terminate;
    Junction2 -> TakePicture;
    TakePicture -> WriteMemory;
    Junction1 -> TurnOff;
}
```

[上一组 `0007`](../0007/README.md) | [返回 60 组索引](../../PAIR_INDEX.md) | [下一组 `0009`](../0009/README.md)
