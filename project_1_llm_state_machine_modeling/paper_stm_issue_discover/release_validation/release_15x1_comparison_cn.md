# internal RC 固定 15-pair x 1 回归对照

本对照只用于发布结构迁移的技术回归，不构成新的论文主实验。v60 三轮是历史参考；新 run 是一次独立 LLM/Judge 采样，不能把全部观察差异严格归因于结构整理。

固定 pair 为 `0001, 0002, 0004, 0010, 0012, 0013, 0023, 0024, 0029, 0035, 0046, 0049, 0053, 0054, 0056`。v60 参考含 45 个 method/Judge cells、180 个 round-level expected rows 和 60 个跨轮 expected issues；新 RC 含 15 个 cells、60 个 expected rows。原始对应关系、SHA-256、report ID 和 ledger ID 见 `v60_15pair_reference.json` 的 `cells`、`release_15x1_comparison.json` 及 `raw/`。

## 主指标

| 指标 | v60 R1 | v60 R2 | v60 R3 | v60 三轮合并 | internal RC 15x1 |
| --- | ---: | ---: | ---: | ---: | ---: |
| overall FULL / hit@1 | 43/60 (71.67%) | 44/60 (73.33%) | 45/60 (75.00%) | 132/180 (73.33%) | 49/60 (81.67%) |
| L2 FULL / hit@1 | 22/24 (91.67%) | 22/24 (91.67%) | 20/24 (83.33%) | 64/72 (88.89%) | 23/24 (95.83%) |
| semantic precision | 128/139 (92.09%) | 131/143 (91.61%) | 137/144 (95.14%) | 396/426 (92.96%) | 140/143 (97.90%) |
| hit@3（60 个跨轮 expected issues） | 不适用 | 不适用 | 不适用 | 51/60 (85.00%) | 不适用 |
| hit@all（60 个跨轮 expected issues） | 不适用 | 不适用 | 不适用 | 35/60 (58.33%) | 不适用 |

`hit@3` 与 `hit@all` 的样本单位是跨三轮 expected issue，不能用新 15x1 的单轮数据替代。

## W、K/N/I、D 与阶段损失

| 指标 | v60 三轮合并 | internal RC 15x1 |
| --- | ---: | ---: |
| FULL-hit max-W2 | 94/132 (71.21%) | 34/49 (69.39%) |
| FULL-hit max-W1 | 38/132 (28.79%) | 15/49 (30.61%) |
| FULL-hit max-W0 | 0/132 (0.00%) | 0/49 (0.00%) |
| W2 / 全部 expected | 106/180 (58.89%) | 39/60 (65.00%) |
| report-level VALID_KNOWN | 258 | 92 |
| report-level VALID_NOVEL | 138 | 48 |
| report-level INVALID | 30 | 3 |
| root-cause cluster VALID_KNOWN | 244 | 90 |
| root-cause cluster VALID_NOVEL | 121 | 45 |
| root-cause cluster INVALID | 24 | 3 |
| root-cause cluster VALID | 365 | 135 |
| root-cause cluster precision | 365/389 (93.83%) | 135/138 (97.83%) |
| D2 evidence records | 464 | 160 |
| D1 evidence records | 29 | 2 |
| D0 evidence records | 104 | 18 |
| D_UNRESOLVED evidence records | 39 | 10 |
| stage-loss: contract_extraction_or_identity_binding | 30 | 8 |
| stage-loss: publish_adapter | 145 | 51 |
| stage-loss: typed_frontier | 5 | 1 |

FULL-hit max-W 只从 `expected_outcomes[].full_report_ids` 的 supporting reports 取最高等级；`partial_report_ids` 不会抬高 FULL hit。W2/全部 expected 的分母为 round-level expected rows，因此与 W-on-hits 分母不同。K/N/I 与 hit、W、D 均为正交审计轴。

## Predicate usage

计划分母固定为 12：`S1,S2,S3,S4,S5,S6,G1,G4,R1,R4,V1,V4`。终态 receipt 可出现计划外 predicate，但不以观察到的集合缩小计划分母。

| planned predicate | v60 terminal receipts | RC terminal receipts | RC pass/violation | RC FULL-hit contribution | RC error/timeout/degradation |
| --- | ---: | ---: | --- | ---: | --- |
| S1 | 37 | 12 | pass=12, violation=0 | 0 | - |
| S2 | 134 | 44 | pass=14, violation=30 | 17 | - |
| S3 | 65 | 20 | pass=12, violation=8 | 4 | - |
| S4 | 9 | 3 | pass=2, violation=1 | 1 | - |
| S5 | 40 | 14 | pass=0, violation=14 | 1 | {"invalid_input": 34} |
| S6 | 0 | 0 | pass=0, violation=0 | 0 | {"invalid_input": 1} |
| G1 | 34 | 10 | pass=0, violation=10 | 17 | {"invalid_input": 5} |
| G4 | 5 | 2 | pass=2, violation=0 | 0 | - |
| R1 | 12 | 3 | pass=3, violation=0 | 0 | - |
| R4 | 4 | 2 | pass=2, violation=0 | 0 | - |
| V1 | 0 | 0 | pass=0, violation=0 | 0 | - |
| V4 | 41 | 13 | pass=0, violation=13 | 15 | - |

planned terminal predicate usage：v60 10/12；RC 10/12。全部终态谓词集合分别为 11 与 11；RC 的非计划终态谓词为 `R2`。

## 调用、token 与成本

| 项目 | v60 三轮合并 | internal RC 15x1 |
| --- | ---: | ---: |
| method logical calls | 237 | 76 |
| method attempts | 300 | 97 |
| method input tokens | - | - |
| method input tokens excluding cache | 5642254 | 2021932 |
| method output tokens | 807561 | 264225 |
| method cache read tokens | 5336576 | 1686400 |
| method cache write tokens | 0 | 0 |
| method provider retries | 0 | 0 |
| method recorded cost USD | 2.20425552 | 0.7551844 |
| method cost eligible | True | True |
| Judge logical calls | 458 | 156 |
| Judge attempts | 478 | 158 |
| Judge input tokens | 51420292 | 19237213 |
| Judge input tokens excluding cache | - | - |
| Judge output tokens | 2971420 | 1064129 |
| Judge cache read tokens | 20662144 | 8571648 |
| Judge cache write tokens | 0 | 0 |
| Judge provider retries | 19 | 2 |
| Judge recorded cost USD | 13.849762399999998 | 3.58150076 |
| Judge cost eligible | False | True |

## 确定性与采样审计

| 确定性检查 | 结果 |
| --- | --- |
| judge_protocol_sha256 | 通过 |
| matched_typed_carrier_verdicts | 通过 |
| method_terminal_cells | 通过 |
| pair_input_closure_hashes | 通过 |
| profile | 通过 |
| prompt_schema_hash | 通过 |
| registry_hash | 通过 |
| scoped_input_data_hash | 通过 |
| scoped_run_contract_identity | 通过 |
| streaming | 通过 |
| transport_retries | 通过 |

精确 typed carrier 交集为 104；same-input terminal verdict flips 为 0；v60-only/new-only 分别为 109/26。one-sided carrier 仅表示独立采样的 candidate/route surface 差异，不能解释为 backend 对相同输入改变真值。

| 随机指标 | RC 15x1 | v60 min | v60 max | v60 mean | 包络内 | 软带内 |
| --- | ---: | ---: | ---: | ---: | --- | --- |
| overall_full | 81.67% | 71.67% | 75.00% | 73.33% | 否 | 是 |
| l2_full | 95.83% | 83.33% | 91.67% | 88.89% | 否 | 是 |
| semantic_precision | 97.90% | 91.61% | 95.14% | 92.94% | 否 | 是 |
| max_w2_on_hits | 69.39% | 71.21% | 71.21% | 71.21% | 否 | 是 |

结论：未发现结构性语义变化；确定性不变量与 matched same-input carrier 均通过，随机指标处于 v60 轮间包络或预注册软容差内，因此没有要求重跑 54x3/162-cell 的结构性证据。

该目录位于 `release_validation/`，不属于冻结 `final_results`，且被 method release allowlist 排除。
