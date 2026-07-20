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
- review subject SHA-256：`883b74b2e0906bcc730992056e9e9ea2b773f6f42506ddf56df45516d2e196d6`
- working contract SHA-256：`285987e443e9b0d0ab1bc2b8ada8e91cc402626dae5c0afb27719f4b66bc9e7c`
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
- legacy whole-model FCSTM execution / Discover：`false` / `false`
- working bundle usage gate：`discover_input_with_capability_mask`
- ownership source / compiler / agent：`57` / `48` / `0`
- source macro / positive identity trace / conversion boundary trace：`33` / `51` / `6`
- capability source-static / simulation / transition-trace：`eligible_with_exclusions` / `ineligible` / `ineligible`
- compiler-only diagnostic policy：`rejected_conversion_artifact`；main-result conversion artifact limit：`0`
- 主 session 对读：`pass`；ownership/macro/capability 均为 `pass`；Case 0058 passes conversion-attribution review. This does not assert NL/PlantUML correctness or runtime equivalence; authored defects remain eligible for later source-grounded Discover. Five doubled-quote repairs and the trailing end-marker quote are isolated as input normalizations; fork/timing facts remain visible but runtime-excluded.
- source anchors：`source-ref:llms_emp_feedback_final_0058.puml:line:3\|state TurnOn {, source-ref:llms_emp_feedback_final_0058.puml:line:43\|choice2 --> Join1 : [sunny=true]`；FCSTM anchors：`element-ref:source:state:TurnOn@line:6\|state TurnOn named "TurnOn" {, element-ref:compiler:transition_segment:tr_0013:segment:1@line:70\|choice2 -> Join1 : /_sunny_true;`
- 三个原始文件：[NL](./nl.txt) | [PlantUML](./plantuml.puml) | [FCSTM](./fcstm.fcstm)
- 审计入口：[canonical](../../canonical/llms_emp_feedback_final_0058.json) | [冻结 FCSTM](../../fcstm/llms_emp_feedback_final_0058.fcstm) | [case report](../../case_reports/llms_emp_feedback_final_0058.json) | [working contract](../../working_contracts/llms_emp_feedback_final_0058.json) | [source trace](../../source_traces/llms_emp_feedback_final_0058.json) | [人工总账](../../MANUAL_REVIEW.md)

## 主 session 三方语义对应

| projection | assessment | NL anchor | PlantUML anchor | FCSTM anchor | source roots | compiler members | rationale |
|---|---|---|---|---|---|---|---|
| `direct` | `preserved` | TurnOn | source-ref:llms_emp_feedback_final_0058.puml:line:3\|state TurnOn { | element-ref:source:state:TurnOn@line:6\|state TurnOn named "TurnOn" { | source:state:TurnOn | - | Case 0058 binds source:state:TurnOn to the exact authored occurrence 'state TurnOn {'; it is present as a direct FCSTM state projection with the same source identity and parent relation. |
| `macro` | `preserved_with_exclusions` | choice2 | source-ref:llms_emp_feedback_final_0058.puml:line:43\|choice2 --> Join1 : [sunny=true] | element-ref:compiler:transition_segment:tr_0013:segment:1@line:70\|choice2 -> Join1 : /_sunny_true; | source:transition:tr_0013 | compiler:transition_segment:tr_0013:segment:1 | Case 0058 binds source:transition:tr_0013 to the exact authored occurrence 'choice2 --> Join1 : [sunny=true]'; it is present as a source-owned transition root whose cited FCSTM line belongs to a protected compiler macro; the raw label remains opaque. |

## Risk occurrence 第二遍复核

| obligation | risk tag | assessment | PlantUML evidence | FCSTM evidence | ownership evidence | rationale |
|---|---|---|---|---|---|---|
| `review:multi_segment_macro:0001:tr_0001` | `multi_segment_macro` | `compiler_artifact_excluded` | source-ref:llms_emp_feedback_final_0058.puml:line:8\|[*] --> TurnOn_state | element-ref:compiler:transition_segment:tr_0001:segment:1@line:58\|[*] -> TurnOn;, element-ref:compiler:transition_segment:tr_0001:segment:2@line:9\|[*] -> TurnOn_state; | compiler:transition_segment:tr_0001:segment:1, compiler:transition_segment:tr_0001:segment:2, source:transition:tr_0001 | Case 0058 risk multi_segment_macro occurrence review:multi_segment_macro:0001:tr_0001: The single authored transition remains one source-owned semantic root; all bound FCSTM segments are protected compiler artifacts and cannot become repair targets. |
| `review:multi_segment_macro:0002:tr_0002` | `multi_segment_macro` | `compiler_artifact_excluded` | source-ref:llms_emp_feedback_final_0058.puml:line:9\|TurnOn_state --> fork1 | element-ref:compiler:transition_segment:tr_0002:segment:1@line:10\|TurnOn_state -> [*];, element-ref:compiler:transition_segment:tr_0002:segment:2@line:59\|TurnOn -> fork1; | compiler:transition_segment:tr_0002:segment:1, compiler:transition_segment:tr_0002:segment:2, source:transition:tr_0002 | Case 0058 risk multi_segment_macro occurrence review:multi_segment_macro:0002:tr_0002: The single authored transition remains one source-owned semantic root; all bound FCSTM segments are protected compiler artifacts and cannot become repair targets. |
| `review:multi_segment_macro:0003:tr_0006` | `multi_segment_macro` | `compiler_artifact_excluded` | source-ref:llms_emp_feedback_final_0058.puml:line:21\|AutoFocus_state --> choice1 : [memFull=true] | element-ref:compiler:transition_segment:tr_0006:segment:1@line:17\|AutoFocus_state -> [*] : /_memFull_true;, element-ref:compiler:transition_segment:tr_0006:segment:2@line:63\|AutoFocus -> choice1 : /_memFull_true; | compiler:transition_segment:tr_0006:segment:1, compiler:transition_segment:tr_0006:segment:2, source:transition:tr_0006 | Case 0058 risk multi_segment_macro occurrence review:multi_segment_macro:0003:tr_0006: The single authored transition remains one source-owned semantic root; all bound FCSTM segments are protected compiler artifacts and cannot become repair targets. |
| `review:multi_segment_macro:0004:tr_0007` | `multi_segment_macro` | `compiler_artifact_excluded` | source-ref:llms_emp_feedback_final_0058.puml:line:28\|DetLight_state --> choice2 : <<GaStep>>{prob=0.4} | element-ref:compiler:transition_segment:tr_0007:segment:1@line:23\|DetLight_state -> [*] : /_GaStep_prob_0_4;, element-ref:compiler:transition_segment:tr_0007:segment:2@line:64\|DetLight -> choice2 : /_GaStep_prob_0_4; | compiler:transition_segment:tr_0007:segment:1, compiler:transition_segment:tr_0007:segment:2, source:transition:tr_0007 | Case 0058 risk multi_segment_macro occurrence review:multi_segment_macro:0004:tr_0007: The single authored transition remains one source-owned semantic root; all bound FCSTM segments are protected compiler artifacts and cannot become repair targets. |
| `review:multi_segment_macro:0005:tr_0008` | `multi_segment_macro` | `compiler_artifact_excluded` | source-ref:llms_emp_feedback_final_0058.puml:line:35\|choice3 --> ChargedFlash_state | element-ref:compiler:transition_segment:tr_0008:segment:1@line:65\|choice3 -> ChargedFlash;, element-ref:compiler:transition_segment:tr_0008:segment:2@line:29\|[*] -> ChargedFlash_state; | compiler:transition_segment:tr_0008:segment:1, compiler:transition_segment:tr_0008:segment:2, source:transition:tr_0008 | Case 0058 risk multi_segment_macro occurrence review:multi_segment_macro:0005:tr_0008: The single authored transition remains one source-owned semantic root; all bound FCSTM segments are protected compiler artifacts and cannot become repair targets. |
| `review:multi_segment_macro:0006:tr_0009` | `multi_segment_macro` | `compiler_artifact_excluded` | source-ref:llms_emp_feedback_final_0058.puml:line:36\|ChargedFlash_state --> Junction3 : [Charged=true] | element-ref:compiler:transition_segment:tr_0009:segment:1@line:30\|ChargedFlash_state -> [*] : /_Charged_true;, element-ref:compiler:transition_segment:tr_0009:segment:2@line:66\|ChargedFlash -> Junction3 : /_Charged_true; | compiler:transition_segment:tr_0009:segment:1, compiler:transition_segment:tr_0009:segment:2, source:transition:tr_0009 | Case 0058 risk multi_segment_macro occurrence review:multi_segment_macro:0006:tr_0009: The single authored transition remains one source-owned semantic root; all bound FCSTM segments are protected compiler artifacts and cannot become repair targets. |
| `review:multi_segment_macro:0007:tr_0017` | `multi_segment_macro` | `compiler_artifact_excluded` | source-ref:llms_emp_feedback_final_0058.puml:line:55\|WriteMemory_state --> Junction1 | element-ref:compiler:transition_segment:tr_0017:segment:1@line:46\|WriteMemory_state -> [*];, element-ref:compiler:transition_segment:tr_0017:segment:2@line:74\|WriteMemory -> Junction1; | compiler:transition_segment:tr_0017:segment:1, compiler:transition_segment:tr_0017:segment:2, source:transition:tr_0017 | Case 0058 risk multi_segment_macro occurrence review:multi_segment_macro:0007:tr_0017: The single authored transition remains one source-owned semantic root; all bound FCSTM segments are protected compiler artifacts and cannot become repair targets. |
| `review:final_boundary:0008:tr_0019` | `final_boundary` | `source_fact_preserved` | source-ref:llms_emp_feedback_final_0058.puml:line:57\|TurnOff --> [*] | element-ref:compiler:transition_segment:tr_0019:segment:1@line:76\|TurnOff -> [*]; | compiler:transition_segment:tr_0019:segment:1, source:transition:tr_0019 | Case 0058 risk final_boundary occurrence review:final_boundary:0008:tr_0019: The authored PlantUML final boundary is preserved by the bound FCSTM termination macro rather than being converted into an ordinary user state. |
| `review:multi_segment_macro:0009:tr_0020` | `multi_segment_macro` | `compiler_artifact_excluded` | source-ref:llms_emp_feedback_final_0058.puml:line:61\|fork2 --> Junction2 | element-ref:compiler:transition_segment:tr_0020:segment:1@line:37\|fork2 -> [*];, element-ref:compiler:transition_segment:tr_0020:segment:2@line:77\|Join2 -> Junction2; | compiler:transition_segment:tr_0020:segment:1, compiler:transition_segment:tr_0020:segment:2, source:transition:tr_0020 | Case 0058 risk multi_segment_macro occurrence review:multi_segment_macro:0009:tr_0020: The single authored transition remains one source-owned semantic root; all bound FCSTM segments are protected compiler artifacts and cannot become repair targets. |
| `review:multi_segment_macro:0010:tr_0022` | `multi_segment_macro` | `compiler_artifact_excluded` | source-ref:llms_emp_feedback_final_0058.puml:line:65\|Flash --> Terminate | element-ref:compiler:transition_segment:tr_0022:segment:1@line:39\|Flash -> [*];, element-ref:compiler:transition_segment:tr_0022:segment:2@line:78\|Join2 -> Terminate; | compiler:transition_segment:tr_0022:segment:1, compiler:transition_segment:tr_0022:segment:2, source:transition:tr_0022 | Case 0058 risk multi_segment_macro occurrence review:multi_segment_macro:0010:tr_0022: The single authored transition remains one source-owned semantic root; all bound FCSTM segments are protected compiler artifacts and cannot become repair targets. |
| `review:synthetic_state:0011:001-UnspecifiedInitial` | `synthetic_state` | `compiler_artifact_excluded` | source-ref:llms_emp_feedback_final_0058.puml:line:3\|state TurnOn { | element-ref:compiler:state:llms_emp_feedback_final_0058.TurnOn.UnspecifiedInitial@line:7\|state UnspecifiedInitial named "Unspecified initial";, element-ref:source:state:TurnOn@line:6\|state TurnOn named "TurnOn" { | compiler:state:llms_emp_feedback_final_0058.TurnOn.UnspecifiedInitial, source:state:TurnOn | Case 0058 risk synthetic_state occurrence review:synthetic_state:0011:001-UnspecifiedInitial: The helper state is a protected compiler-owned projection for a source structural fact; diagnostics on the helper itself are conversion artifacts. |
| `review:synthetic_state:0012:002-UnspecifiedInitial` | `synthetic_state` | `compiler_artifact_excluded` | source-ref:llms_emp_feedback_final_0058.puml:line:16\|state AutoFocus { | element-ref:compiler:state:llms_emp_feedback_final_0058.AutoFocus.UnspecifiedInitial@line:15\|state UnspecifiedInitial named "Unspecified initial";, element-ref:source:state:AutoFocus@line:14\|state AutoFocus named "AutoFocus" { | compiler:state:llms_emp_feedback_final_0058.AutoFocus.UnspecifiedInitial, source:state:AutoFocus | Case 0058 risk synthetic_state occurrence review:synthetic_state:0012:002-UnspecifiedInitial: The helper state is a protected compiler-owned projection for a source structural fact; diagnostics on the helper itself are conversion artifacts. |
| `review:synthetic_state:0013:003-UnspecifiedInitial` | `synthetic_state` | `compiler_artifact_excluded` | source-ref:llms_emp_feedback_final_0058.puml:line:23\|state DetLight { | element-ref:compiler:state:llms_emp_feedback_final_0058.DetLight.UnspecifiedInitial@line:21\|state UnspecifiedInitial named "Unspecified initial";, element-ref:source:state:DetLight@line:20\|state DetLight named "DetLight" { | compiler:state:llms_emp_feedback_final_0058.DetLight.UnspecifiedInitial, source:state:DetLight | Case 0058 risk synthetic_state occurrence review:synthetic_state:0013:003-UnspecifiedInitial: The helper state is a protected compiler-owned projection for a source structural fact; diagnostics on the helper itself are conversion artifacts. |
| `review:synthetic_state:0014:004-UnspecifiedInitial` | `synthetic_state` | `compiler_artifact_excluded` | source-ref:llms_emp_feedback_final_0058.puml:line:30\|state ChargedFlash { | element-ref:compiler:state:llms_emp_feedback_final_0058.ChargedFlash.UnspecifiedInitial@line:27\|state UnspecifiedInitial named "Unspecified initial";, element-ref:source:state:ChargedFlash@line:26\|state ChargedFlash named "ChargedFlash" { | compiler:state:llms_emp_feedback_final_0058.ChargedFlash.UnspecifiedInitial, source:state:ChargedFlash | Case 0058 risk synthetic_state occurrence review:synthetic_state:0014:004-UnspecifiedInitial: The helper state is a protected compiler-owned projection for a source structural fact; diagnostics on the helper itself are conversion artifacts. |
| `review:synthetic_state:0015:005-UnspecifiedInitial` | `synthetic_state` | `compiler_artifact_excluded` | source-ref:llms_emp_feedback_final_0058.puml:line:39\|state Join2 <<join>> | element-ref:compiler:state:llms_emp_feedback_final_0058.Join2.UnspecifiedInitial@line:34\|state UnspecifiedInitial named "Unspecified initial";, element-ref:source:state:Join2@line:33\|state Join2 named "Join2" { | compiler:state:llms_emp_feedback_final_0058.Join2.UnspecifiedInitial, source:state:Join2 | Case 0058 risk synthetic_state occurrence review:synthetic_state:0015:005-UnspecifiedInitial: The helper state is a protected compiler-owned projection for a source structural fact; diagnostics on the helper itself are conversion artifacts. |
| `review:synthetic_state:0016:006-UnspecifiedInitial` | `synthetic_state` | `compiler_artifact_excluded` | source-ref:llms_emp_feedback_final_0058.puml:line:50\|state WriteMemory { | element-ref:compiler:state:llms_emp_feedback_final_0058.WriteMemory.UnspecifiedInitial@line:44\|state UnspecifiedInitial named "Unspecified initial";, element-ref:source:state:WriteMemory@line:43\|state WriteMemory named "WriteMemory" { | compiler:state:llms_emp_feedback_final_0058.WriteMemory.UnspecifiedInitial, source:state:WriteMemory | Case 0058 risk synthetic_state occurrence review:synthetic_state:0016:006-UnspecifiedInitial: The helper state is a protected compiler-owned projection for a source structural fact; diagnostics on the helper itself are conversion artifacts. |
| `review:source_normalization:0017:001` | `source_normalization` | `compiler_artifact_excluded` | source-ref:llms_emp_feedback_final_0058.puml:line:4\|state ""TurnOn"" as TurnOn_state | - | source:normalization:1 | Case 0058 risk source_normalization occurrence review:source_normalization:0017:001: The transport-only normalization is isolated in the conversion boundary and cannot support a source-level issue or repair claim. rule_id=source_input.workbook_doubled_state_quotes; before=state ""TurnOn"" as TurnOn_state; after=state "TurnOn" as TurnOn_state. |
| `review:source_normalization:0018:002` | `source_normalization` | `compiler_artifact_excluded` | source-ref:llms_emp_feedback_final_0058.puml:line:17\|state ""AutoFocus"" as AutoFocus_state | - | source:normalization:2 | Case 0058 risk source_normalization occurrence review:source_normalization:0018:002: The transport-only normalization is isolated in the conversion boundary and cannot support a source-level issue or repair claim. rule_id=source_input.workbook_doubled_state_quotes; before=state ""AutoFocus"" as AutoFocus_state; after=state "AutoFocus" as AutoFocus_state. |
| `review:source_normalization:0019:003` | `source_normalization` | `compiler_artifact_excluded` | source-ref:llms_emp_feedback_final_0058.puml:line:24\|state ""DetLight"" as DetLight_state | - | source:normalization:3 | Case 0058 risk source_normalization occurrence review:source_normalization:0019:003: The transport-only normalization is isolated in the conversion boundary and cannot support a source-level issue or repair claim. rule_id=source_input.workbook_doubled_state_quotes; before=state ""DetLight"" as DetLight_state; after=state "DetLight" as DetLight_state. |
| `review:source_normalization:0020:004` | `source_normalization` | `compiler_artifact_excluded` | source-ref:llms_emp_feedback_final_0058.puml:line:31\|state ""ChargedFlash"" as ChargedFlash_state | - | source:normalization:4 | Case 0058 risk source_normalization occurrence review:source_normalization:0020:004: The transport-only normalization is isolated in the conversion boundary and cannot support a source-level issue or repair claim. rule_id=source_input.workbook_doubled_state_quotes; before=state ""ChargedFlash"" as ChargedFlash_state; after=state "ChargedFlash" as ChargedFlash_state. |
| `review:source_normalization:0021:005` | `source_normalization` | `compiler_artifact_excluded` | source-ref:llms_emp_feedback_final_0058.puml:line:51\|state ""WriteMemory"" as WriteMemory_state | - | source:normalization:5 | Case 0058 risk source_normalization occurrence review:source_normalization:0021:005: The transport-only normalization is isolated in the conversion boundary and cannot support a source-level issue or repair claim. rule_id=source_input.workbook_doubled_state_quotes; before=state ""WriteMemory"" as WriteMemory_state; after=state "WriteMemory" as WriteMemory_state. |
| `review:source_normalization:0022:006` | `source_normalization` | `compiler_artifact_excluded` | source-ref:llms_emp_feedback_final_0058.puml:line:67\|@enduml" | - | source:normalization:6 | Case 0058 risk source_normalization occurrence review:source_normalization:0022:006: The transport-only normalization is isolated in the conversion boundary and cannot support a source-level issue or repair claim. rule_id=source_input.workbook_trailing_end_quote; before=@enduml"; after=@enduml. |
| `review:explicit_concurrency:0023:001-ambiguous_unlabeled_fanout` | `explicit_concurrency` | `capability_excluded` | source-ref:llms_emp_feedback_final_0058.puml:line:11\|state fork1 <<fork>>, source-ref:llms_emp_feedback_final_0058.puml:line:12\|fork1 --> AutoFocus, source-ref:llms_emp_feedback_final_0058.puml:line:13\|fork1 --> DetLight, source-ref:llms_emp_feedback_final_0058.puml:line:14\|fork1 --> choice3 | element-ref:compiler:transition_segment:tr_0003:segment:1@line:60\|fork1 -> AutoFocus;, element-ref:compiler:transition_segment:tr_0004:segment:1@line:61\|fork1 -> DetLight;, element-ref:compiler:transition_segment:tr_0005:segment:1@line:62\|fork1 -> choice3;, element-ref:source:state:fork1@line:13\|pseudo state fork1 named "fork1"; | source:state:fork1, source:transition:tr_0003, source:transition:tr_0004, source:transition:tr_0005 | Case 0058 risk explicit_concurrency occurrence review:explicit_concurrency:0023:001-ambiguous_unlabeled_fanout: The authored concurrency occurrence remains visible, but the FCSTM projection does not claim fork/join product semantics and is excluded from runtime evidence. |
| `review:explicit_concurrency:0024:002-ambiguous_unlabeled_fanout` | `explicit_concurrency` | `capability_excluded` | source-ref:llms_emp_feedback_final_0058.puml:line:14\|fork1 --> choice3, source-ref:llms_emp_feedback_final_0058.puml:line:35\|choice3 --> ChargedFlash_state, source-ref:llms_emp_feedback_final_0058.puml:line:37\|choice3 --> Junction3 | element-ref:compiler:transition_segment:tr_0008:segment:1@line:65\|choice3 -> ChargedFlash;, element-ref:compiler:transition_segment:tr_0010:segment:1@line:67\|choice3 -> Junction3;, element-ref:source:state:choice3@line:49\|state choice3 named "choice3"; | source:state:choice3, source:transition:tr_0008, source:transition:tr_0010 | Case 0058 risk explicit_concurrency occurrence review:explicit_concurrency:0024:002-ambiguous_unlabeled_fanout: The authored concurrency occurrence remains visible, but the FCSTM projection does not claim fork/join product semantics and is excluded from runtime evidence. |
| `review:explicit_concurrency:0025:003-ambiguous_unlabeled_fanout` | `explicit_concurrency` | `capability_excluded` | source-ref:llms_emp_feedback_final_0058.puml:line:60\|state fork2 <<fork>>, source-ref:llms_emp_feedback_final_0058.puml:line:61\|fork2 --> Junction2, source-ref:llms_emp_feedback_final_0058.puml:line:62\|fork2 --> Flash | element-ref:compiler:transition_segment:tr_0020:segment:1@line:37\|fork2 -> [*];, element-ref:compiler:transition_segment:tr_0021:segment:1@line:38\|fork2 -> Flash;, element-ref:source:state:Join2.fork2@line:35\|pseudo state fork2 named "fork2"; | source:state:Join2.fork2, source:transition:tr_0020, source:transition:tr_0021 | Case 0058 risk explicit_concurrency occurrence review:explicit_concurrency:0025:003-ambiguous_unlabeled_fanout: The authored concurrency occurrence remains visible, but the FCSTM projection does not claim fork/join product semantics and is excluded from runtime evidence. |
| `review:explicit_concurrency:0026:004-explicit_concurrency_pseudostate` | `explicit_concurrency` | `capability_excluded` | source-ref:llms_emp_feedback_final_0058.puml:line:11\|state fork1 <<fork>> | element-ref:source:state:fork1@line:13\|pseudo state fork1 named "fork1"; | source:state:fork1 | Case 0058 risk explicit_concurrency occurrence review:explicit_concurrency:0026:004-explicit_concurrency_pseudostate: The authored concurrency occurrence remains visible, but the FCSTM projection does not claim fork/join product semantics and is excluded from runtime evidence. |
| `review:explicit_concurrency:0027:005-explicit_concurrency_pseudostate` | `explicit_concurrency` | `capability_excluded` | source-ref:llms_emp_feedback_final_0058.puml:line:45\|state Join1 <<join>> | element-ref:source:state:Join1@line:42\|pseudo state Join1 named "Join1"; | source:state:Join1 | Case 0058 risk explicit_concurrency occurrence review:explicit_concurrency:0027:005-explicit_concurrency_pseudostate: The authored concurrency occurrence remains visible, but the FCSTM projection does not claim fork/join product semantics and is excluded from runtime evidence. |
| `review:explicit_concurrency:0028:006-explicit_concurrency_pseudostate` | `explicit_concurrency` | `capability_excluded` | source-ref:llms_emp_feedback_final_0058.puml:line:60\|state fork2 <<fork>> | element-ref:source:state:Join2.fork2@line:35\|pseudo state fork2 named "fork2"; | source:state:Join2.fork2 | Case 0058 risk explicit_concurrency occurrence review:explicit_concurrency:0028:006-explicit_concurrency_pseudostate: The authored concurrency occurrence remains visible, but the FCSTM projection does not claim fork/join product semantics and is excluded from runtime evidence. |

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
