# Pair `0048`：NL + PlantUML STM0 + FCSTM STM0

[上一组 `0047`](../0047/README.md) | [返回 60 组索引](../../PAIR_INDEX.md) | [下一组 `0049`](../0049/README.md)

- LLM：`DeepSeek`
- 模型/场景： Digital camera state machine diagrams
- 作者输出阶段：`Result with Semantic Checking`
- 作者输出单元格：`AE50`；Excel row：`50`
- Phase-I fallback：`false`
- 相对 Phase-I 是否变化：`true`
- Phase-I PlantUML SHA-256：`91951da63cfb9eef882f8f3b45d69fbba6c22dcc4c1f1247dd4a7f91a2f079ab`
- NL SHA-256：`6af3966c8b0e12004a22622cded88b07df6fef9d558534442e3309694543c76d`
- PlantUML SHA-256：`a1de42bed4d559454458b8b096b06dfbebcb660775f1e864fdc87f6980ffcdfb`
- FCSTM SHA-256：`c5e9af79be0eb85505af5b7b84474d748425b366dbed75cc5f86b574e28d3d31`
- review subject SHA-256：`95eb7e8d28f712b6950a940c30b283b00824a85ef8b1f05437bc4b4876c6c081`
- working contract SHA-256：`93249a2d509cd1b5d91b6b58c279f917ed381ee6015235e6144c10624a32469a`
- 结构裁决：`structure_preserved`
- source states / transitions：`19` / `24`
- mapped / blocked / silent drop：`24` / `0` / `0`
- final / lifecycle / body coverage：`2/2` / `0/0` / `5/5`
- concurrent region / separator coverage：`0/0` / `0/0`
- source normalization coverage：`0/0`
- official raw / validation：`state_diagram` / `state_diagram`
- official identity states / transitions：`19` / `24`
- official identity remaps：state `2` / transition endpoint `0`
- AST audit：`passed`
- legacy whole-model FCSTM execution / Discover：`false` / `false`
- working bundle usage gate：`discover_input_with_capability_mask`
- ownership source / compiler / agent：`48` / `39` / `0`
- source macro / positive identity trace / conversion boundary trace：`29` / `48` / `0`
- capability source-static / simulation / transition-trace：`eligible_with_exclusions` / `ineligible` / `ineligible`
- compiler-only diagnostic policy：`rejected_conversion_artifact`；main-result conversion artifact limit：`0`
- 主 session 对读：`pass`；ownership/macro/capability 均为 `pass`；Case 0048 passes conversion-attribution review. This does not assert NL/PlantUML correctness or runtime equivalence; authored defects remain eligible for later source-grounded Discover. No conversion-specific blocker was found in the exact reviewed occurrences.
- source anchors：`source-ref:llms_emp_feedback_final_0048.puml:line:6\|state fork1 <<fork>> {, source-ref:llms_emp_feedback_final_0048.puml:line:12\|AutoFocus --> choice1 : [memFull=true]`；FCSTM anchors：`element-ref:source:state:fork1@line:6\|state fork1 named "fork1" {, element-ref:compiler:transition_segment:tr_0005:segment:1@line:12\|AutoFocus -> [*] : /_memFull_true;`
- 三个原始文件：[NL](./nl.txt) | [PlantUML](./plantuml.puml) | [FCSTM](./fcstm.fcstm)
- 审计入口：[canonical](../../canonical/llms_emp_feedback_final_0048.json) | [冻结 FCSTM](../../fcstm/llms_emp_feedback_final_0048.fcstm) | [case report](../../case_reports/llms_emp_feedback_final_0048.json) | [working contract](../../working_contracts/llms_emp_feedback_final_0048.json) | [source trace](../../source_traces/llms_emp_feedback_final_0048.json) | [人工总账](../../MANUAL_REVIEW.md)

## 主 session 三方语义对应

| projection | assessment | NL anchor | PlantUML anchor | FCSTM anchor | source roots | compiler members | rationale |
|---|---|---|---|---|---|---|---|
| `direct` | `preserved` | fork1 | source-ref:llms_emp_feedback_final_0048.puml:line:6\|state fork1 <<fork>> { | element-ref:source:state:fork1@line:6\|state fork1 named "fork1" { | source:state:fork1 | - | Case 0048 binds source:state:fork1 to the exact authored occurrence 'state fork1 <<fork>> {'; it is present as a direct FCSTM state projection with the same source identity and parent relation. |
| `macro` | `preserved_with_exclusions` | AutoFocus | source-ref:llms_emp_feedback_final_0048.puml:line:12\|AutoFocus --> choice1 : [memFull=true] | element-ref:compiler:transition_segment:tr_0005:segment:1@line:12\|AutoFocus -> [*] : /_memFull_true; | source:transition:tr_0005 | compiler:transition_segment:tr_0005:segment:1 | Case 0048 binds source:transition:tr_0005 to the exact authored occurrence 'AutoFocus --> choice1 : [memFull=true]'; it is present as a source-owned transition root whose cited FCSTM line belongs to a protected compiler macro; the raw label remains opaque. |

## Risk occurrence 第二遍复核

| obligation | risk tag | assessment | PlantUML evidence | FCSTM evidence | ownership evidence | rationale |
|---|---|---|---|---|---|---|
| `review:official_identity_remap:0001:state-001` | `official_identity_remap` | `source_fact_preserved` | source-ref:llms_emp_feedback_final_0048.puml:line:11\|AutoFocus : max=2s, min=1s | element-ref:source:state:fork1.AutoFocus@line:8\|state AutoFocus named "AutoFocus\n[PlantUML body] max=2s, min=1s"; | source:state:fork1.AutoFocus | Case 0048 risk official_identity_remap occurrence review:official_identity_remap:0001:state-001: The occurrence follows the pinned PlantUML qualified Entity/Link identity result, including the recorded remap, instead of substituting a lexical guess. |
| `review:official_identity_remap:0002:state-002` | `official_identity_remap` | `source_fact_preserved` | source-ref:llms_emp_feedback_final_0048.puml:line:14\|DetLight : max=1s, min=0s | element-ref:source:state:fork1.DetLight@line:9\|state DetLight named "DetLight\n[PlantUML body] max=1s, min=0s"; | source:state:fork1.DetLight | Case 0048 risk official_identity_remap occurrence review:official_identity_remap:0002:state-002: The occurrence follows the pinned PlantUML qualified Entity/Link identity result, including the recorded remap, instead of substituting a lexical guess. |
| `review:multi_segment_macro:0003:tr_0005` | `multi_segment_macro` | `compiler_artifact_excluded` | source-ref:llms_emp_feedback_final_0048.puml:line:12\|AutoFocus --> choice1 : [memFull=true] | element-ref:compiler:transition_segment:tr_0005:segment:1@line:12\|AutoFocus -> [*] : /_memFull_true;, element-ref:compiler:transition_segment:tr_0005:segment:2@line:44\|fork1 -> choice1 : /_memFull_true; | compiler:transition_segment:tr_0005:segment:1, compiler:transition_segment:tr_0005:segment:2, source:transition:tr_0005 | Case 0048 risk multi_segment_macro occurrence review:multi_segment_macro:0003:tr_0005: The single authored transition remains one source-owned semantic root; all bound FCSTM segments are protected compiler artifacts and cannot become repair targets. |
| `review:multi_segment_macro:0004:tr_0006` | `multi_segment_macro` | `compiler_artifact_excluded` | source-ref:llms_emp_feedback_final_0048.puml:line:15\|DetLight --> choice2 : <<GaStep>>{prob=0.4} | element-ref:compiler:transition_segment:tr_0006:segment:1@line:13\|DetLight -> [*] : /_GaStep_prob_0_4;, element-ref:compiler:transition_segment:tr_0006:segment:2@line:45\|fork1 -> choice2 : /_GaStep_prob_0_4; | compiler:transition_segment:tr_0006:segment:1, compiler:transition_segment:tr_0006:segment:2, source:transition:tr_0006 | Case 0048 risk multi_segment_macro occurrence review:multi_segment_macro:0004:tr_0006: The single authored transition remains one source-owned semantic root; all bound FCSTM segments are protected compiler artifacts and cannot become repair targets. |
| `review:multi_segment_macro:0005:tr_0014` | `multi_segment_macro` | `compiler_artifact_excluded` | source-ref:llms_emp_feedback_final_0048.puml:line:28\|Join1 --> Junction2 | element-ref:compiler:transition_segment:tr_0014:segment:1@line:20\|Join1 -> [*];, element-ref:compiler:transition_segment:tr_0014:segment:2@line:52\|Join2 -> Junction2; | compiler:transition_segment:tr_0014:segment:1, compiler:transition_segment:tr_0014:segment:2, source:transition:tr_0014 | Case 0048 risk multi_segment_macro occurrence review:multi_segment_macro:0005:tr_0014: The single authored transition remains one source-owned semantic root; all bound FCSTM segments are protected compiler artifacts and cannot become repair targets. |
| `review:final_boundary:0006:tr_0019` | `final_boundary` | `source_fact_preserved` | source-ref:llms_emp_feedback_final_0048.puml:line:35\|TurnOff --> [*] | element-ref:compiler:transition_segment:tr_0019:segment:1@line:57\|TurnOff -> [*]; | compiler:transition_segment:tr_0019:segment:1, source:transition:tr_0019 | Case 0048 risk final_boundary occurrence review:final_boundary:0006:tr_0019: The authored PlantUML final boundary is preserved by the bound FCSTM termination macro rather than being converted into an ordinary user state. |
| `review:multi_segment_macro:0007:tr_0023` | `multi_segment_macro` | `compiler_artifact_excluded` | source-ref:llms_emp_feedback_final_0048.puml:line:42\|Flash --> Terminate | element-ref:compiler:transition_segment:tr_0023:segment:1@line:27\|Flash -> [*];, element-ref:compiler:transition_segment:tr_0023:segment:2@line:60\|Fork2 -> Terminate; | compiler:transition_segment:tr_0023:segment:1, compiler:transition_segment:tr_0023:segment:2, source:transition:tr_0023 | Case 0048 risk multi_segment_macro occurrence review:multi_segment_macro:0007:tr_0023: The single authored transition remains one source-owned semantic root; all bound FCSTM segments are protected compiler artifacts and cannot become repair targets. |
| `review:final_boundary:0008:tr_0024` | `final_boundary` | `source_fact_preserved` | source-ref:llms_emp_feedback_final_0048.puml:line:43\|Terminate --> [*] | element-ref:compiler:transition_segment:tr_0024:segment:1@line:61\|Terminate -> [*]; | compiler:transition_segment:tr_0024:segment:1, source:transition:tr_0024 | Case 0048 risk final_boundary occurrence review:final_boundary:0008:tr_0024: The authored PlantUML final boundary is preserved by the bound FCSTM termination macro rather than being converted into an ordinary user state. |
| `review:synthetic_state:0009:001-UnspecifiedInitial` | `synthetic_state` | `compiler_artifact_excluded` | source-ref:llms_emp_feedback_final_0048.puml:line:6\|state fork1 <<fork>> { | element-ref:compiler:state:llms_emp_feedback_final_0048.fork1.UnspecifiedInitial@line:7\|state UnspecifiedInitial named "Unspecified initial";, element-ref:source:state:fork1@line:6\|state fork1 named "fork1" { | compiler:state:llms_emp_feedback_final_0048.fork1.UnspecifiedInitial, source:state:fork1 | Case 0048 risk synthetic_state occurrence review:synthetic_state:0009:001-UnspecifiedInitial: The helper state is a protected compiler-owned projection for a source structural fact; diagnostics on the helper itself are conversion artifacts. |
| `review:synthetic_state:0010:002-UnspecifiedInitial` | `synthetic_state` | `compiler_artifact_excluded` | source-ref:llms_emp_feedback_final_0048.puml:line:25\|state Join2 <<join>> { | element-ref:compiler:state:llms_emp_feedback_final_0048.Join2.UnspecifiedInitial@line:17\|state UnspecifiedInitial named "Unspecified initial";, element-ref:source:state:Join2@line:16\|state Join2 named "Join2" { | compiler:state:llms_emp_feedback_final_0048.Join2.UnspecifiedInitial, source:state:Join2 | Case 0048 risk synthetic_state occurrence review:synthetic_state:0010:002-UnspecifiedInitial: The helper state is a protected compiler-owned projection for a source structural fact; diagnostics on the helper itself are conversion artifacts. |
| `review:synthetic_state:0011:003-UnspecifiedInitial` | `synthetic_state` | `compiler_artifact_excluded` | source-ref:llms_emp_feedback_final_0048.puml:line:38\|state Fork2 <<fork>> { | element-ref:compiler:state:llms_emp_feedback_final_0048.Fork2.UnspecifiedInitial@line:24\|state UnspecifiedInitial named "Unspecified initial";, element-ref:source:state:Fork2@line:23\|state Fork2 named "Fork2" { | compiler:state:llms_emp_feedback_final_0048.Fork2.UnspecifiedInitial, source:state:Fork2 | Case 0048 risk synthetic_state occurrence review:synthetic_state:0011:003-UnspecifiedInitial: The helper state is a protected compiler-owned projection for a source structural fact; diagnostics on the helper itself are conversion artifacts. |
| `review:explicit_concurrency:0012:001-ambiguous_unlabeled_fanout` | `explicit_concurrency` | `capability_excluded` | source-ref:llms_emp_feedback_final_0048.puml:line:17\|fork1 --> choice3, source-ref:llms_emp_feedback_final_0048.puml:line:6\|state fork1 <<fork>> {, source-ref:llms_emp_feedback_final_0048.puml:line:7\|fork1 --> AutoFocus, source-ref:llms_emp_feedback_final_0048.puml:line:8\|fork1 --> DetLight | element-ref:compiler:transition_segment:tr_0003:segment:1@line:10\|! * -> AutoFocus;, element-ref:compiler:transition_segment:tr_0004:segment:1@line:11\|! * -> DetLight;, element-ref:compiler:transition_segment:tr_0007:segment:1@line:46\|!fork1 -> choice3;, element-ref:source:state:fork1@line:6\|state fork1 named "fork1" { | source:state:fork1, source:transition:tr_0003, source:transition:tr_0004, source:transition:tr_0007 | Case 0048 risk explicit_concurrency occurrence review:explicit_concurrency:0012:001-ambiguous_unlabeled_fanout: The authored concurrency occurrence remains visible, but the FCSTM projection does not claim fork/join product semantics and is excluded from runtime evidence. |
| `review:explicit_concurrency:0013:002-ambiguous_unlabeled_fanout` | `explicit_concurrency` | `capability_excluded` | source-ref:llms_emp_feedback_final_0048.puml:line:17\|fork1 --> choice3, source-ref:llms_emp_feedback_final_0048.puml:line:18\|choice3 --> ChargedFlash, source-ref:llms_emp_feedback_final_0048.puml:line:21\|choice3 --> Junction3 | element-ref:compiler:transition_segment:tr_0008:segment:1@line:47\|choice3 -> ChargedFlash;, element-ref:compiler:transition_segment:tr_0010:segment:1@line:49\|choice3 -> Junction3;, element-ref:source:state:choice3@line:33\|state choice3 named "choice3"; | source:state:choice3, source:transition:tr_0008, source:transition:tr_0010 | Case 0048 risk explicit_concurrency occurrence review:explicit_concurrency:0013:002-ambiguous_unlabeled_fanout: The authored concurrency occurrence remains visible, but the FCSTM projection does not claim fork/join product semantics and is excluded from runtime evidence. |
| `review:explicit_concurrency:0014:003-ambiguous_unlabeled_fanout` | `explicit_concurrency` | `capability_excluded` | source-ref:llms_emp_feedback_final_0048.puml:line:25\|state Join2 <<join>> {, source-ref:llms_emp_feedback_final_0048.puml:line:26\|Join2 --> Join1, source-ref:llms_emp_feedback_final_0048.puml:line:37\|Join2 --> Fork2 | element-ref:compiler:transition_segment:tr_0013:segment:1@line:19\|! * -> Join1;, element-ref:compiler:transition_segment:tr_0020:segment:1@line:58\|!Join2 -> Fork2;, element-ref:source:state:Join2@line:16\|state Join2 named "Join2" { | source:state:Join2, source:transition:tr_0013, source:transition:tr_0020 | Case 0048 risk explicit_concurrency occurrence review:explicit_concurrency:0014:003-ambiguous_unlabeled_fanout: The authored concurrency occurrence remains visible, but the FCSTM projection does not claim fork/join product semantics and is excluded from runtime evidence. |
| `review:explicit_concurrency:0015:004-ambiguous_unlabeled_fanout` | `explicit_concurrency` | `capability_excluded` | source-ref:llms_emp_feedback_final_0048.puml:line:38\|state Fork2 <<fork>> {, source-ref:llms_emp_feedback_final_0048.puml:line:39\|Fork2 --> Junction2, source-ref:llms_emp_feedback_final_0048.puml:line:40\|Fork2 --> Flash | element-ref:compiler:transition_segment:tr_0021:segment:1@line:59\|!Fork2 -> Junction2;, element-ref:compiler:transition_segment:tr_0022:segment:1@line:26\|! * -> Flash;, element-ref:source:state:Fork2@line:23\|state Fork2 named "Fork2" { | source:state:Fork2, source:transition:tr_0021, source:transition:tr_0022 | Case 0048 risk explicit_concurrency occurrence review:explicit_concurrency:0015:004-ambiguous_unlabeled_fanout: The authored concurrency occurrence remains visible, but the FCSTM projection does not claim fork/join product semantics and is excluded from runtime evidence. |

## 作者阶段 lineage

| stage | output cell | present | output SHA-256 | feedback | resolved |
|---|---|---|---|---|---|
| `phase_i_generation` | `I50` | `true` | `91951da63cfb9eef882f8f3b45d69fbba6c22dcc4c1f1247dd4a7f91a2f079ab` | - | - |
| `phase_ii_format` | `U50` | `true` | `4bc691dc6f9fc63dcf230550d577c9cea5fabef5cc5cd66089605e0585352d67` | syntax error: stm [stateMachine] SystemStateMachine [SystemStateMachineDiagram]<br> | YES |
| `phase_ii_grammar` | `Z50` | `false` | `-` | - | - |
| `phase_ii_semantic` | `AE50` | `true` | `a1de42bed4d559454458b8b096b06dfbebcb660775f1e864fdc87f6980ffcdfb` | 1. Missing Junction Pseudostate, Fork Pseudostate, Join <br>use state join1 <<join>> to represent join pseudostate | - |

## Official identity ledger

- status：`aligned`
- canonical / official states：`19` / `19`
- aligned transition endpoints：`24`

| source-parser identity | pinned PlantUML identity | raw ref | reason |
|---|---|---|---|
| `AutoFocus` | `fork1.AutoFocus` | `llms_emp_feedback_final_0048.puml:line:11` | `unique_official_entity_identity` |
| `DetLight` | `fork1.DetLight` | `llms_emp_feedback_final_0048.puml:line:14` | `unique_official_entity_identity` |

本组 transition endpoint 无需重映射。

## Source normalization ledger

本组没有 source-input normalization。

## Concurrent region ledger

本组没有 PlantUML orthogonal/concurrent region separator。

## Operational debt

| reason code | count |
|---|---:|
| `R45.DEBT.ambiguous_unlabeled_fanout` | 4 |
| `R45.DEBT.missing_explicit_initial` | 3 |
| `R45.DEBT.opaque_state_body_semantics` | 5 |
| `R45.DEBT.opaque_transition_label_semantics` | 4 |

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
[*] --> TurnOn
TurnOn : max=2s, min=2s
TurnOn --> fork1

state fork1 <<fork>> {
fork1 --> AutoFocus
fork1 --> DetLight
}

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
state Join2 <<join>> {
Join2 --> Join1
}
Join1 --> Junction2

Junction2 --> TakePicture
TakePicture --> WriteMemory
WriteMemory : max=3s, min=2s
WriteMemory --> Junction1
Junction1 --> TurnOff
TurnOff --> [*]

Join2 --> Fork2
state Fork2 <<fork>> {
Fork2 --> Junction2
Fork2 --> Flash
}
Flash --> Terminate
Terminate --> [*]
@enduml
```

## 转换后 FCSTM STM0

```fcstm
state llms_emp_feedback_final_0048 named "llms_emp_feedback_final_0048" {
    event _memFull_true named "[memFull=true]";
    event _GaStep_prob_0_4 named "<<GaStep>>{prob=0.4}";
    event _Charged_true named "[Charged=true]";
    event _sunny_true named "[sunny=true]";
    state fork1 named "fork1" {
        state UnspecifiedInitial named "Unspecified initial";
        state AutoFocus named "AutoFocus\n[PlantUML body] max=2s, min=1s";
        state DetLight named "DetLight\n[PlantUML body] max=1s, min=0s";
        ! * -> AutoFocus;
        ! * -> DetLight;
        AutoFocus -> [*] : /_memFull_true;
        DetLight -> [*] : /_GaStep_prob_0_4;
        [*] -> UnspecifiedInitial;
    }
    state Join2 named "Join2" {
        state UnspecifiedInitial named "Unspecified initial";
        state Join1 named "Join1";
        ! * -> Join1;
        Join1 -> [*];
        [*] -> UnspecifiedInitial;
    }
    state Fork2 named "Fork2" {
        state UnspecifiedInitial named "Unspecified initial";
        state Flash named "Flash";
        ! * -> Flash;
        Flash -> [*];
        [*] -> UnspecifiedInitial;
    }
    state TurnOn named "TurnOn\n[PlantUML body] max=2s, min=2s";
    state choice1 named "choice1";
    state choice2 named "choice2";
    state choice3 named "choice3";
    state ChargedFlash named "ChargedFlash\n[PlantUML body] max=4s, min=2s";
    state Junction3 named "Junction3";
    state Junction2 named "Junction2";
    state TakePicture named "TakePicture";
    state WriteMemory named "WriteMemory\n[PlantUML body] max=3s, min=2s";
    state Junction1 named "Junction1";
    state TurnOff named "TurnOff";
    state Terminate named "Terminate";
    [*] -> TurnOn;
    TurnOn -> fork1;
    fork1 -> choice1 : /_memFull_true;
    fork1 -> choice2 : /_GaStep_prob_0_4;
    !fork1 -> choice3;
    choice3 -> ChargedFlash;
    ChargedFlash -> Junction3 : /_Charged_true;
    choice3 -> Junction3;
    Junction3 -> Join2;
    choice2 -> Join2 : /_sunny_true;
    Join2 -> Junction2;
    Junction2 -> TakePicture;
    TakePicture -> WriteMemory;
    WriteMemory -> Junction1;
    Junction1 -> TurnOff;
    TurnOff -> [*];
    !Join2 -> Fork2;
    !Fork2 -> Junction2;
    Fork2 -> Terminate;
    Terminate -> [*];
}
```

[上一组 `0047`](../0047/README.md) | [返回 60 组索引](../../PAIR_INDEX.md) | [下一组 `0049`](../0049/README.md)
