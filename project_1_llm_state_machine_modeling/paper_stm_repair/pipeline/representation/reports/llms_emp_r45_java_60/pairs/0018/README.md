# Pair `0018`：NL + PlantUML STM0 + FCSTM STM0

[上一组 `0017`](../0017/README.md) | [返回 60 组索引](../../PAIR_INDEX.md) | [下一组 `0019`](../0019/README.md)

- LLM：`GPT-4`
- 模型/场景： Digital camera state machine diagrams
- NL SHA-256：`6af3966c8b0e12004a22622cded88b07df6fef9d558534442e3309694543c76d`
- PlantUML SHA-256：`7dd9957bddd73250391bc3a00775069cd896aee734df139fd35820c2893b0b9a`
- FCSTM SHA-256：`e556d42c5c057ae3182d43ff0ac087777cdd2b337c2d7bebd354b108a14ae573`
- 结构裁决：`structure_preserved`
- FCSTM execution eligible：`false`
- Discover eligible：`false`
- 主 session 对读：21 条多层 macro 均有 exit/continuation/entry；8 个 missing initial placeholder 明示；fan-out/timing 不推断。
- 三个原始文件：[NL](./nl.txt) | [PlantUML](./plantuml.puml) | [FCSTM](./fcstm.fcstm)
- 审计入口：[canonical](../../canonical/llms_emp_stm_results_0018.json) | [冻结 FCSTM](../../fcstm/llms_emp_stm_results_0018.fcstm) | [case report](../../case_reports/llms_emp_stm_results_0018.json) | [人工总账](../../MANUAL_REVIEW.md)

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
[*] --> TurnOn : 2 sec
state fork1
TurnOn --> fork1

fork1 --> AutoFocus : 1-2 sec
state AutoFocus {
    state choice1
    AutoFocus -down-> choice1 : memFull=true
}

fork1 --> DetLight : <1 sec
state DetLight {
    state choice2
    DetLight -down-> choice2 : <<GaStep>>{prob=0.4}
}

fork1 --> choice3
state choice3 {
    state ChargedFlash: 2-4 sec
    choice3 -down-> ChargedFlash
    ChargedFlash -down-> Junction3 : Charged=true
    choice3 -down-> Junction3
}

state Junction3 {
    state Join2
    Junction3 --> Join2
}
state Join2 {
    state Fork2
    Join2 --> Fork2
    state Join1
    choice2 --> Join1 when : sunny=true
    Join1 --> Junction2
}

state Flash {
    Fork2 --> Flash
    Flash --> Terminate
}

state Junction2 {
    state TakePicture
    Junction2 --> TakePicture
    TakePicture --> WriteMemory : 2-3 sec
}

state WriteMemory {
    state Junction1
    WriteMemory --> Junction1
}

state TurnOff
Junction1 --> TurnOff
TurnOff -left->[*]
@enduml
```

## 转换后 FCSTM STM0

```fcstm
state llms_emp_stm_results_0018 named "llms_emp_stm_results_0018" {
    event _2_sec named "2 sec";
    event _1_2_sec named "1-2 sec";
    event memFull_true named "memFull=true";
    event _1_sec named "<1 sec";
    event _GaStep_prob_0_4 named "<<GaStep>>{prob=0.4}";
    event Charged_true named "Charged=true";
    event when_sunny_true named "when sunny=true";
    event _2_3_sec named "2-3 sec";
    state InitialWaittr_0001 named "Awaiting initial event: 2 sec";
    state fork1 named "fork1";
    state AutoFocus named "AutoFocus" {
        state UnspecifiedInitial named "Unspecified initial";
        state choice1 named "choice1";
        ! * -> choice1 : /memFull_true;
        [*] -> UnspecifiedInitial;
    }
    state DetLight named "DetLight" {
        state UnspecifiedInitial named "Unspecified initial";
        state choice2 named "choice2";
        ! * -> choice2 : /_GaStep_prob_0_4;
        choice2 -> [*] : /when_sunny_true;
        [*] -> UnspecifiedInitial;
    }
    state choice3 named "choice3" {
        state UnspecifiedInitial named "Unspecified initial";
        state ChargedFlash named "ChargedFlash\n[PlantUML body] 2-4 sec";
        ! * -> ChargedFlash;
        ChargedFlash -> [*] : /Charged_true;
        [*] -> UnspecifiedInitial;
    }
    state Junction3 named "Junction3" {
        state UnspecifiedInitial named "Unspecified initial";
        state Join2 named "Join2";
        ! * -> Join2;
        [*] -> UnspecifiedInitial;
    }
    state Join2 named "Join2" {
        state UnspecifiedInitial named "Unspecified initial";
        state Fork2 named "Fork2";
        state Join1 named "Join1";
        [*] -> Join1 : /when_sunny_true;
        ! * -> Fork2;
        Join1 -> [*];
        Fork2 -> [*];
        [*] -> UnspecifiedInitial;
    }
    state Flash named "Flash" {
        state UnspecifiedInitial named "Unspecified initial";
        state Terminate named "Terminate";
        ! * -> Terminate;
        [*] -> UnspecifiedInitial;
    }
    state Junction2 named "Junction2" {
        state UnspecifiedInitial named "Unspecified initial";
        state TakePicture named "TakePicture";
        ! * -> TakePicture;
        TakePicture -> [*] : /_2_3_sec;
        [*] -> UnspecifiedInitial;
    }
    state WriteMemory named "WriteMemory" {
        state UnspecifiedInitial named "Unspecified initial";
        state Junction1 named "Junction1";
        ! * -> Junction1;
        Junction1 -> [*];
        [*] -> UnspecifiedInitial;
    }
    state TurnOff named "TurnOff";
    state TurnOn named "TurnOn";
    [*] -> InitialWaittr_0001;
    InitialWaittr_0001 -> TurnOn : /_2_sec;
    TurnOn -> fork1;
    fork1 -> AutoFocus : /_1_2_sec;
    fork1 -> DetLight : /_1_sec;
    fork1 -> choice3;
    choice3 -> Junction3 : /Charged_true;
    !choice3 -> Junction3;
    DetLight -> Join2 : /when_sunny_true;
    Join2 -> Junction2;
    Join2 -> Flash;
    Junction2 -> WriteMemory : /_2_3_sec;
    WriteMemory -> TurnOff;
    TurnOff -> [*];
}
```

[上一组 `0017`](../0017/README.md) | [返回 60 组索引](../../PAIR_INDEX.md) | [下一组 `0019`](../0019/README.md)
