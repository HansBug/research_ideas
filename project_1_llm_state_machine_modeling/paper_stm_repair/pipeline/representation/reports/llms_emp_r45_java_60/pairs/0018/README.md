# Pair `0018`：NL + PlantUML STM0 + FCSTM STM0

[上一组 `0017`](../0017/README.md) | [返回 60 组索引](../../PAIR_INDEX.md) | [下一组 `0019`](../0019/README.md)

- LLM：`GPT-4`
- 模型/场景： Digital camera state machine diagrams
- 作者输出阶段：`Result with Semantic Checking`
- 作者输出单元格：`AE20`；Excel row：`20`
- Phase-I fallback：`false`
- 相对 Phase-I 是否变化：`true`
- Phase-I PlantUML SHA-256：`7dd9957bddd73250391bc3a00775069cd896aee734df139fd35820c2893b0b9a`
- NL SHA-256：`6af3966c8b0e12004a22622cded88b07df6fef9d558534442e3309694543c76d`
- PlantUML SHA-256：`fffdc9e44b50f80c97cb0886d363b536a96da1fed84402be80ea8987859fbab3`
- FCSTM SHA-256：`b348a2473850107c98f0395a33a8462fe6423d43b52f57915042bec91a48b8bf`
- review subject SHA-256：`374fa113f128bcfdabfb55c789c13298855d06a90170fa5cf54062589361b109`
- working contract SHA-256：`da419d133687da3814f42cc8fcc93b468d9c128b7a4b60f844ae9c06d2dd7ade`
- 结构裁决：`structure_preserved`
- source states / transitions：`18` / `22`
- mapped / blocked / silent drop：`22` / `0` / `0`
- final / lifecycle / body coverage：`1/1` / `0/0` / `0/0`
- concurrent region / separator coverage：`0/0` / `0/0`
- source normalization coverage：`0/0`
- official raw / validation：`state_diagram` / `state_diagram`
- official identity states / transitions：`18` / `22`
- official identity remaps：state `0` / transition endpoint `0`
- AST audit：`passed`
- legacy whole-model FCSTM execution / Discover：`false` / `false`
- working bundle usage gate：`discover_input_with_capability_mask`
- ownership source / compiler / agent：`40` / `33` / `0`
- source macro / positive identity trace / conversion boundary trace：`22` / `40` / `0`
- capability source-static / simulation / transition-trace：`eligible_with_exclusions` / `ineligible` / `ineligible`
- compiler-only diagnostic policy：`rejected_conversion_artifact`；main-result conversion artifact limit：`0`
- 主 session 对读：`pass`；ownership/macro/capability 均为 `pass`；Case 0018 passes conversion-attribution review. This does not assert NL/PlantUML correctness or runtime equivalence; authored defects remain eligible for later source-grounded Discover. No conversion-specific blocker was found in the exact reviewed occurrences. Fresh v6 main-session review re-read NL, PlantUML, FCSTM, working contract, and source trace after the portable Java identity change; source/FCSTM/trace bytes are unchanged and verification remains fail-closed.
- source anchors：`source-ref:llms_emp_feedback_final_0018.puml:line:3\|state TurnOn, source-ref:llms_emp_feedback_final_0018.puml:line:10\|AutoFocus --> choice1 : memFull=true`；FCSTM anchors：`element-ref:source:state:TurnOn@line:11\|state TurnOn named "TurnOn";, element-ref:compiler:transition_segment:tr_0005:segment:1@line:34\|AutoFocus -> choice1 : /memFull_true;`
- 三个原始文件：[NL](./nl.txt) | [PlantUML](./plantuml.puml) | [FCSTM](./fcstm.fcstm)
- 审计入口：[canonical](../../canonical/llms_emp_feedback_final_0018.json) | [冻结 FCSTM](../../fcstm/llms_emp_feedback_final_0018.fcstm) | [case report](../../case_reports/llms_emp_feedback_final_0018.json) | [working contract](../../working_contracts/llms_emp_feedback_final_0018.json) | [source trace](../../source_traces/llms_emp_feedback_final_0018.json) | [人工总账](../../MANUAL_REVIEW.md)

## 主 session 三方语义对应

| projection | assessment | NL anchor | PlantUML anchor | FCSTM anchor | source roots | compiler members | rationale |
|---|---|---|---|---|---|---|---|
| `direct` | `preserved` | TurnOn | source-ref:llms_emp_feedback_final_0018.puml:line:3\|state TurnOn | element-ref:source:state:TurnOn@line:11\|state TurnOn named "TurnOn"; | source:state:TurnOn | - | Case 0018 binds source:state:TurnOn to the exact authored occurrence 'state TurnOn'; it is present as a direct FCSTM state projection with the same source identity and parent relation. |
| `macro` | `preserved_with_exclusions` | memFull=true | source-ref:llms_emp_feedback_final_0018.puml:line:10\|AutoFocus --> choice1 : memFull=true | element-ref:compiler:transition_segment:tr_0005:segment:1@line:34\|AutoFocus -> choice1 : /memFull_true; | source:transition:tr_0005 | compiler:transition_segment:tr_0005:segment:1 | Case 0018 binds source:transition:tr_0005 to the exact authored occurrence 'AutoFocus --> choice1 : memFull=true'; it is present as a source-owned transition root whose cited FCSTM line belongs to a protected compiler macro; the raw label remains opaque. |

## Risk occurrence 第二遍复核

| obligation | risk tag | assessment | PlantUML evidence | FCSTM evidence | ownership evidence | rationale |
|---|---|---|---|---|---|---|
| `review:multi_segment_macro:0001:tr_0001` | `multi_segment_macro` | `compiler_artifact_excluded` | source-ref:llms_emp_feedback_final_0018.puml:line:2\|[*] --> TurnOn : Start | element-ref:compiler:state:llms_emp_feedback_final_0018.InitialWaittr_0001@line:10\|state InitialWaittr_0001 named "Awaiting initial event: Start";, element-ref:compiler:transition_segment:tr_0001:segment:1@line:29\|[*] -> InitialWaittr_0001;, element-ref:compiler:transition_segment:tr_0001:segment:2@line:30\|InitialWaittr_0001 -> TurnOn : /Start; | compiler:state:llms_emp_feedback_final_0018.InitialWaittr_0001, compiler:transition_segment:tr_0001:segment:1, compiler:transition_segment:tr_0001:segment:2, source:transition:tr_0001 | Case 0018 risk multi_segment_macro occurrence review:multi_segment_macro:0001:tr_0001: The single authored transition remains one source-owned semantic root; all bound FCSTM segments are protected compiler artifacts and cannot become repair targets. |
| `review:final_boundary:0002:tr_0022` | `final_boundary` | `source_fact_preserved` | source-ref:llms_emp_feedback_final_0018.puml:line:55\|TurnOff --> [*] | element-ref:compiler:transition_segment:tr_0022:segment:1@line:51\|TurnOff -> [*]; | compiler:transition_segment:tr_0022:segment:1, source:transition:tr_0022 | Case 0018 risk final_boundary occurrence review:final_boundary:0002:tr_0022: The authored PlantUML final boundary is preserved by the bound FCSTM termination macro rather than being converted into an ordinary user state. |
| `review:synthetic_state:0003:001-InitialWaittr_0001` | `synthetic_state` | `compiler_artifact_excluded` | source-ref:llms_emp_feedback_final_0018.puml:line:2\|[*] --> TurnOn : Start | element-ref:compiler:state:llms_emp_feedback_final_0018.InitialWaittr_0001@line:10\|state InitialWaittr_0001 named "Awaiting initial event: Start"; | compiler:state:llms_emp_feedback_final_0018.InitialWaittr_0001, source:transition:tr_0001 | Case 0018 risk synthetic_state occurrence review:synthetic_state:0003:001-InitialWaittr_0001: The helper state is a protected compiler-owned projection for a source structural fact; diagnostics on the helper itself are conversion artifacts. |
| `review:explicit_concurrency:0004:001-ambiguous_unlabeled_fanout` | `explicit_concurrency` | `capability_excluded` | source-ref:llms_emp_feedback_final_0018.puml:line:5\|state fork1 <<fork>>, source-ref:llms_emp_feedback_final_0018.puml:line:6\|fork1 --> AutoFocus, source-ref:llms_emp_feedback_final_0018.puml:line:7\|fork1 --> DetLight | element-ref:compiler:transition_segment:tr_0003:segment:1@line:32\|fork1 -> AutoFocus;, element-ref:compiler:transition_segment:tr_0004:segment:1@line:33\|fork1 -> DetLight;, element-ref:source:state:fork1@line:12\|pseudo state fork1 named "fork1"; | source:state:fork1, source:transition:tr_0003, source:transition:tr_0004 | Case 0018 risk explicit_concurrency occurrence review:explicit_concurrency:0004:001-ambiguous_unlabeled_fanout: The authored concurrency occurrence remains visible, but the FCSTM projection does not claim fork/join product semantics and is excluded from runtime evidence. |
| `review:explicit_concurrency:0005:002-explicit_concurrency_pseudostate` | `explicit_concurrency` | `capability_excluded` | source-ref:llms_emp_feedback_final_0018.puml:line:5\|state fork1 <<fork>> | element-ref:source:state:fork1@line:12\|pseudo state fork1 named "fork1"; | source:state:fork1 | Case 0018 risk explicit_concurrency occurrence review:explicit_concurrency:0005:002-explicit_concurrency_pseudostate: The authored concurrency occurrence remains visible, but the FCSTM projection does not claim fork/join product semantics and is excluded from runtime evidence. |
| `review:explicit_concurrency:0006:003-explicit_concurrency_pseudostate` | `explicit_concurrency` | `capability_excluded` | source-ref:llms_emp_feedback_final_0018.puml:line:22\|state fork2 <<fork>> | element-ref:source:state:fork2@line:17\|pseudo state fork2 named "fork2"; | source:state:fork2 | Case 0018 risk explicit_concurrency occurrence review:explicit_concurrency:0006:003-explicit_concurrency_pseudostate: The authored concurrency occurrence remains visible, but the FCSTM projection does not claim fork/join product semantics and is excluded from runtime evidence. |
| `review:explicit_concurrency:0007:004-explicit_concurrency_pseudostate` | `explicit_concurrency` | `capability_excluded` | source-ref:llms_emp_feedback_final_0018.puml:line:32\|state join2 <<join>> | element-ref:source:state:join2@line:20\|pseudo state join2 named "join2"; | source:state:join2 | Case 0018 risk explicit_concurrency occurrence review:explicit_concurrency:0007:004-explicit_concurrency_pseudostate: The authored concurrency occurrence remains visible, but the FCSTM projection does not claim fork/join product semantics and is excluded from runtime evidence. |
| `review:explicit_concurrency:0008:005-explicit_concurrency_pseudostate` | `explicit_concurrency` | `capability_excluded` | source-ref:llms_emp_feedback_final_0018.puml:line:39\|state join1 <<join>> | element-ref:source:state:join1@line:22\|pseudo state join1 named "join1"; | source:state:join1 | Case 0018 risk explicit_concurrency occurrence review:explicit_concurrency:0008:005-explicit_concurrency_pseudostate: The authored concurrency occurrence remains visible, but the FCSTM projection does not claim fork/join product semantics and is excluded from runtime evidence. |

## 作者阶段 lineage

| stage | output cell | present | output SHA-256 | feedback | resolved |
|---|---|---|---|---|---|
| `phase_i_generation` | `I20` | `true` | `7dd9957bddd73250391bc3a00775069cd896aee734df139fd35820c2893b0b9a` | - | - |
| `phase_ii_format` | `U20` | `true` | `73c201f6fc305cb9ef5075108cd151cda9e6804446df099c24b8d644dd55c2ab` | syntax error: choice2 --> Join1 when : sunny=true | YES |
| `phase_ii_grammar` | `Z20` | `true` | `fffdc9e44b50f80c97cb0886d363b536a96da1fed84402be80ea8987859fbab3` | 1. transition can't connect the state within composite state and composite state itself | YES |
| `phase_ii_semantic` | `AE20` | `true` | `fffdc9e44b50f80c97cb0886d363b536a96da1fed84402be80ea8987859fbab3` | 1.incorrect expression of join, fork, junction | - |

## Official identity ledger

- status：`aligned`
- canonical / official states：`18` / `18`
- aligned transition endpoints：`22`

本组 state identity 无需重映射。

本组 transition endpoint 无需重映射。

## Source normalization ledger

本组没有 source-input normalization。

## Concurrent region ledger

本组没有 PlantUML orthogonal/concurrent region separator。

## Operational debt

| reason code | count |
|---|---:|
| `R45.DEBT.ambiguous_unlabeled_fanout` | 1 |
| `R45.DEBT.explicit_concurrency_pseudostate` | 4 |
| `R45.DEBT.opaque_transition_label_semantics` | 9 |

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
[*] --> TurnOn : Start
state TurnOn
TurnOn --> fork1
state fork1 <<fork>>
fork1 --> AutoFocus
fork1 --> DetLight

state AutoFocus
AutoFocus --> choice1 : memFull=true

state DetLight
DetLight --> choice2 : <<GaStep>>{prob=0.4}

state choice1 <<choice>>
choice1 --> fork2
choice1 --> ChargedFlash : memFull=true

state ChargedFlash
ChargedFlash --> Junction3 : Charged=true

state fork2 <<fork>>
fork2 --> ChargedFlash

state Junction3 <<junction>>
Junction3 --> join2

state choice2 <<choice>>
choice2 --> join2 : sunny=false
choice2 --> join1 : sunny=true

state join2 <<join>>
join2 --> Junction2
join2 --> Flash : activated

state Flash
Flash --> Terminate

state join1 <<join>>
join1 --> Junction2

state Junction2 <<junction>>
Junction2 --> TakePicture

state TakePicture
TakePicture --> WriteMemory

state WriteMemory
WriteMemory --> Junction1

state Junction1 <<junction>>
Junction1 --> TurnOff : end

state TurnOff
TurnOff --> [*]
@enduml
```

## 转换后 FCSTM STM0

```fcstm
state llms_emp_feedback_final_0018 named "llms_emp_feedback_final_0018" {
    event Start named "Start";
    event memFull_true named "memFull=true";
    event _GaStep_prob_0_4 named "<<GaStep>>{prob=0.4}";
    event Charged_true named "Charged=true";
    event sunny_false named "sunny=false";
    event sunny_true named "sunny=true";
    event activated named "activated";
    event end named "end";
    state InitialWaittr_0001 named "Awaiting initial event: Start";
    state TurnOn named "TurnOn";
    pseudo state fork1 named "fork1";
    state AutoFocus named "AutoFocus";
    state DetLight named "DetLight";
    pseudo state choice1 named "choice1";
    state ChargedFlash named "ChargedFlash";
    pseudo state fork2 named "fork2";
    pseudo state Junction3 named "Junction3";
    pseudo state choice2 named "choice2";
    pseudo state join2 named "join2";
    state Flash named "Flash";
    pseudo state join1 named "join1";
    pseudo state Junction2 named "Junction2";
    state TakePicture named "TakePicture";
    state WriteMemory named "WriteMemory";
    pseudo state Junction1 named "Junction1";
    state TurnOff named "TurnOff";
    state Terminate named "Terminate";
    [*] -> InitialWaittr_0001;
    InitialWaittr_0001 -> TurnOn : /Start;
    TurnOn -> fork1;
    fork1 -> AutoFocus;
    fork1 -> DetLight;
    AutoFocus -> choice1 : /memFull_true;
    DetLight -> choice2 : /_GaStep_prob_0_4;
    choice1 -> fork2;
    choice1 -> ChargedFlash : /memFull_true;
    ChargedFlash -> Junction3 : /Charged_true;
    fork2 -> ChargedFlash;
    Junction3 -> join2;
    choice2 -> join2 : /sunny_false;
    choice2 -> join1 : /sunny_true;
    join2 -> Junction2;
    join2 -> Flash : /activated;
    Flash -> Terminate;
    join1 -> Junction2;
    Junction2 -> TakePicture;
    TakePicture -> WriteMemory;
    WriteMemory -> Junction1;
    Junction1 -> TurnOff : /end;
    TurnOff -> [*];
}
```

[上一组 `0017`](../0017/README.md) | [返回 60 组索引](../../PAIR_INDEX.md) | [下一组 `0019`](../0019/README.md)
