# R5 seed sweep 抽样分析

抽样规则：按 `status -> entry_id -> pair_id` 排序，每类至少取前 3 条；若该类超过 100 条，再追加中位与末尾各 1 条。高基数全量明细仍以 archive / records_index 为准。

## converted

- machine count: 529

| entry | pair | status | reason | 学术解释 |
|---|---|---|---|---|
| `llms-emp-stm-subset` | `llms_emp_stm_results_0001` | `converted` | `R5.SWEEP.converted_fcstm_parse_inspect_ok` | 可进入 pre-repair `.fcstm` 表示，但仍需保留 loss 与 attribution。 |
| `llms-emp-stm-subset` | `llms_emp_stm_results_0002` | `converted` | `R5.SWEEP.converted_fcstm_parse_inspect_ok` | 可进入 pre-repair `.fcstm` 表示，但仍需保留 loss 与 attribution。 |
| `llms-emp-stm-subset` | `llms_emp_stm_results_0003` | `converted` | `R5.SWEEP.converted_fcstm_parse_inspect_ok` | 可进入 pre-repair `.fcstm` 表示，但仍需保留 loss 与 attribution。 |
| `unified-uml-multimodal-validation` | `unified_uml_state_train_0468` | `converted` | `R5.SWEEP.converted_fcstm_parse_inspect_ok` | 可进入 pre-repair `.fcstm` 表示，但仍需保留 loss 与 attribution。 |
| `unified-uml-multimodal-validation` | `unified_uml_state_train_0997` | `converted` | `R5.SWEEP.converted_fcstm_parse_inspect_ok` | 可进入 pre-repair `.fcstm` 表示，但仍需保留 loss 与 attribution。 |

## partial

- machine count: 504

| entry | pair | status | reason | 学术解释 |
|---|---|---|---|---|
| `llms-emp-stm-subset` | `llms_emp_stm_results_0000` | `partial` | `R5.SWEEP.partial_representation_loss_or_caveat` | 可作为后续 eligibility review 对象；不能无条件进入主实验。 |
| `llms-emp-stm-subset` | `llms_emp_stm_results_0004` | `partial` | `R5.SWEEP.partial_r3_1_normalization_or_representation_loss` | 可作为后续 eligibility review 对象；不能无条件进入主实验。 |
| `llms-emp-stm-subset` | `llms_emp_stm_results_0005` | `partial` | `R5.SWEEP.partial_representation_loss_or_caveat` | 可作为后续 eligibility review 对象；不能无条件进入主实验。 |
| `unified-uml-multimodal-validation` | `unified_uml_state_train_0462` | `partial` | `R5.SWEEP.partial_r3_1_normalization_or_representation_loss` | 可作为后续 eligibility review 对象；不能无条件进入主实验。 |
| `unified-uml-multimodal-validation` | `unified_uml_state_train_0998` | `partial` | `R5.SWEEP.partial_r3_1_normalization_or_representation_loss` | 可作为后续 eligibility review 对象；不能无条件进入主实验。 |

## blocked_or_missing

- machine count: 23

| entry | pair | status | reason | 学术解释 |
|---|---|---|---|---|
| `llms-emp-stm-subset` | `llms_emp_stm_results_0018` | `blocked` | `R5.SWEEP.blocked_official_scxml_unavailable` | 当前工具链负证据；优先归入 R8 negative evidence 或 converter follow-up。 |
| `llms-emp-stm-subset` | `llms_emp_stm_results_0028` | `blocked` | `R5.SWEEP.blocked_official_scxml_unavailable` | 当前工具链负证据；优先归入 R8 negative evidence 或 converter follow-up。 |
| `llms-emp-stm-subset` | `llms_emp_stm_results_0037` | `blocked` | `R5.SWEEP.blocked_official_scxml_unavailable` | 当前工具链负证据；优先归入 R8 negative evidence 或 converter follow-up。 |

## not_applicable_or_needs_generation

- machine count: 22

| entry | pair | status | reason | 学术解释 |
|---|---|---|---|---|
| `designing-fsm-gpt4` | `None` | `needs_generation` | `R5.SWEEP.needs_generation_pipeline_only_no_author_generated_stm0` | 需另开 generation PR 复跑；R5 不生成。 |
| `fsm-bench-20` | `None` | `needs_generation` | `R5.SWEEP.needs_generation_pipeline_only_no_author_generated_stm0` | 需另开 generation PR 复跑；R5 不生成。 |
| `automated-transition-use-cases-uml-sm` | `None` | `not_applicable` | `R5.SWEEP.not_applicable_no_extracted_pairs_jsonl` | 不是作者一手 generated seed；只保留为相关工作或排除证据。 |
