# Pair `0058`：NL + PlantUML STM0 + FCSTM STM0

[上一组 `0057`](../0057/README.md) | [返回 60 组索引](../../PAIR_INDEX.md) | [下一组 `0059`](../0059/README.md)

- LLM：`Claude`
- 模型/场景： Digital camera state machine diagrams
- 作者输出阶段：`Result with Semantic Checking`
- 作者输出单元格：`AE60`；Excel row：`60`
- Phase-I fallback：`false`
- 相对 Phase-I 是否变化：`true`
- Phase-I PlantUML SHA-256：`5181a79ba0047ffa94d309464ba44fa0600aa5f0c939e20cd72a7f8ad674bea5`
- NL SHA-256：`6af3966c8b0e12004a22622cded88b07df6fef9d558534442e3309694543c76d`
- PlantUML SHA-256：`3b3e1b803602348b22a8678535a3d38ce339c1a53c4893a24a1add541daf6ac6`
- FCSTM SHA-256：`c3671ebab588509a1cb44d9b1f0239dd8de66e8369b29e58547a193d10e95939`
- 结构裁决：`structure_preserved`
- source states / transitions：`24` / `22`
- mapped / blocked / silent drop：`22` / `0` / `0`
- final / lifecycle / body coverage：`1/1` / `0/0` / `5/5`
- concurrent region / separator coverage：`0/0` / `0/0`
- source normalization coverage：`6/6`
- official raw / validation：`not_state_diagram` / `state_diagram`
- official identity states / transitions：`24` / `22`
- official identity remaps：state `0` / transition endpoint `0`
- AST audit：`passed`
- FCSTM execution eligible：`false`
- Discover eligible：`false`
- 主 session 对读：完整对读：五处 workbook doubled quote 与尾部引号仅做 6 条逐行可审计恢复；24 个官方实体、22 边、5 个 timing body 全保留，fork1/fork2/Join1 pseudo、Join2 reopened composite 及 TurnOff root final 均符合官方身份。
- 三个原始文件：[NL](./nl.txt) | [PlantUML](./plantuml.puml) | [FCSTM](./fcstm.fcstm)
- 审计入口：[canonical](../../canonical/llms_emp_feedback_final_0058.json) | [冻结 FCSTM](../../fcstm/llms_emp_feedback_final_0058.fcstm) | [case report](../../case_reports/llms_emp_feedback_final_0058.json) | [人工总账](../../MANUAL_REVIEW.md)

## 作者阶段 lineage

| stage | output cell | present | output SHA-256 | feedback | resolved |
|---|---|---|---|---|---|
| `phase_i_generation` | `I60` | `true` | `5181a79ba0047ffa94d309464ba44fa0600aa5f0c939e20cd72a7f8ad674bea5` | - | - |
| `phase_ii_format` | `U60` | `true` | `439857a3e348df562d4461e2c9dd390050e870bcc25a2035dbefa32c8bcc3f99` | syntax error: fork fork1 | YES |
| `phase_ii_grammar` | `Z60` | `false` | `-` | - | - |
| `phase_ii_semantic` | `AE60` | `true` | `3b3e1b803602348b22a8678535a3d38ce339c1a53c4893a24a1add541daf6ac6` | None | - |

## Official identity ledger

- status：`aligned`
- canonical / official states：`24` / `24`
- aligned transition endpoints：`22`

本组 state identity 无需重映射。

本组 transition endpoint 无需重映射。

## Source normalization ledger

| raw ref | rule | before | after |
|---|---|---|---|
| `llms_emp_feedback_final_0058.puml:line:4` | `source_input.workbook_doubled_state_quotes` | `state ""TurnOn"" as TurnOn_state` | `state "TurnOn" as TurnOn_state` |
| `llms_emp_feedback_final_0058.puml:line:17` | `source_input.workbook_doubled_state_quotes` | `state ""AutoFocus"" as AutoFocus_state` | `state "AutoFocus" as AutoFocus_state` |
| `llms_emp_feedback_final_0058.puml:line:24` | `source_input.workbook_doubled_state_quotes` | `state ""DetLight"" as DetLight_state` | `state "DetLight" as DetLight_state` |
| `llms_emp_feedback_final_0058.puml:line:31` | `source_input.workbook_doubled_state_quotes` | `state ""ChargedFlash"" as ChargedFlash_state` | `state "ChargedFlash" as ChargedFlash_state` |
| `llms_emp_feedback_final_0058.puml:line:51` | `source_input.workbook_doubled_state_quotes` | `state ""WriteMemory"" as WriteMemory_state` | `state "WriteMemory" as WriteMemory_state` |
| `llms_emp_feedback_final_0058.puml:line:67` | `source_input.workbook_trailing_end_quote` | `@enduml"` | `@enduml` |

## Concurrent region ledger

本组没有 PlantUML orthogonal/concurrent region separator。

## Operational debt

| reason code | count |
|---|---:|
| `R45.DEBT.ambiguous_unlabeled_fanout` | 3 |
| `R45.DEBT.explicit_concurrency_pseudostate` | 3 |
| `R45.DEBT.missing_explicit_initial` | 6 |
| `R45.DEBT.opaque_state_body_semantics` | 5 |
| `R45.DEBT.opaque_transition_label_semantics` | 4 |
| `R45.DEBT.source_input_normalization` | 6 |

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

## 作者 Phase-II 最终 PlantUML STM0

```plantuml
@startuml

state TurnOn {
state ""TurnOn"" as TurnOn_state
}
TurnOn_state : {max=2s, min=2s}

[*] --> TurnOn_state
TurnOn_state --> fork1

state fork1 <<fork>>
fork1 --> AutoFocus
fork1 --> DetLight
fork1 --> choice3

state AutoFocus {
state ""AutoFocus"" as AutoFocus_state
}
AutoFocus_state : {max=2s, min=1s}

AutoFocus_state --> choice1 : [memFull=true]

state DetLight {
state ""DetLight"" as DetLight_state
}
DetLight_state : {max=1s, min=0s}

DetLight_state --> choice2 : <<GaStep>>{prob=0.4}

state ChargedFlash {
state ""ChargedFlash"" as ChargedFlash_state
}
ChargedFlash_state : {max=4s, min=2s}

choice3 --> ChargedFlash_state
ChargedFlash_state --> Junction3 : [Charged=true]
choice3 --> Junction3

state Join2 <<join>>
Junction3 --> Join2

choice2 --> Join2
choice2 --> Join1 : [sunny=true]

state Join1 <<join>>
Join1 --> Junction2

Junction2 --> TakePicture
TakePicture --> WriteMemory
state WriteMemory {
state ""WriteMemory"" as WriteMemory_state
}
WriteMemory_state : {max=3s, min=2s}

WriteMemory_state --> Junction1
Junction1 --> TurnOff
TurnOff --> [*]

state Join2 {
state fork2 <<fork>>
fork2 --> Junction2
fork2 --> Flash
}

Flash --> Terminate

@enduml"
```

## 转换后 FCSTM STM0

```fcstm
state llms_emp_feedback_final_0058 named "llms_emp_feedback_final_0058\n[PlantUML source normalization source_input.workbook_doubled_state_quotes] llms_emp_feedback_final_0058.puml:line:4: state \"\"TurnOn\"\" as TurnOn_state -> state \"TurnOn\" as TurnOn_state\n[PlantUML source normalization source_input.workbook_doubled_state_quotes] llms_emp_feedback_final_0058.puml:line:17: state \"\"AutoFocus\"\" as AutoFocus_state -> state \"AutoFocus\" as AutoFocus_state\n[PlantUML source normalization source_input.workbook_doubled_state_quotes] llms_emp_feedback_final_0058.puml:line:24: state \"\"DetLight\"\" as DetLight_state -> state \"DetLight\" as DetLight_state\n[PlantUML source normalization source_input.workbook_doubled_state_quotes] llms_emp_feedback_final_0058.puml:line:31: state \"\"ChargedFlash\"\" as ChargedFlash_state -> state \"ChargedFlash\" as ChargedFlash_state\n[PlantUML source normalization source_input.workbook_doubled_state_quotes] llms_emp_feedback_final_0058.puml:line:51: state \"\"WriteMemory\"\" as WriteMemory_state -> state \"WriteMemory\" as WriteMemory_state\n[PlantUML source normalization source_input.workbook_trailing_end_quote] llms_emp_feedback_final_0058.puml:line:67: @enduml\" -> @enduml" {
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
    state Join2 named "Join2" {
        state UnspecifiedInitial named "Unspecified initial";
        pseudo state fork2 named "fork2";
        state Flash named "Flash";
        fork2 -> [*];
        fork2 -> Flash;
        Flash -> [*];
        [*] -> UnspecifiedInitial;
    }
    pseudo state Join1 named "Join1";
    state WriteMemory named "WriteMemory" {
        state UnspecifiedInitial named "Unspecified initial";
        state WriteMemory_state named "WriteMemory\n[PlantUML body] {max=3s, min=2s}";
        WriteMemory_state -> [*];
        [*] -> UnspecifiedInitial;
    }
    state choice3 named "choice3";
    state choice1 named "choice1";
    state choice2 named "choice2";
    state Junction3 named "Junction3";
    state Junction2 named "Junction2";
    state TakePicture named "TakePicture";
    state Junction1 named "Junction1";
    state TurnOff named "TurnOff";
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
    Join2 -> Terminate;
}
```

[上一组 `0057`](../0057/README.md) | [返回 60 组索引](../../PAIR_INDEX.md) | [下一组 `0059`](../0059/README.md)
