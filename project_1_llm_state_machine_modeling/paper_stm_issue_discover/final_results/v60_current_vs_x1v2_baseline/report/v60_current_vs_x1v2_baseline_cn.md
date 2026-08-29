# v60/current 与 X1v2 baseline 的最终人工监督评测

> 本报告的主结果只来自 `derived/manual_adjudication_v2/` 的最终人工监督裁定；旧 Judge v3.2、reviews/11、reviews/12 和旧 witness audit 只作为 calibration/proposal 或历史诊断，不作为本次论文真值。

## 口径与范围

协议版本为 `issue-189-195-manual-evidence-v2`，按 issue #189 的 D/A 事实与义务审查、issue #195 的 expected relation 与 validity 轴执行。先判断作者 NL/PlantUML 上的承重事实，再判 `D2/D1/D0/A0`，逐条对 145 个 expected 给出 `FULL_MATCH/PARTIAL_MATCH/NO_MATCH`，最后由后端确定性闭合 `VALID_KNOWN/VALID_NOVEL/INVALID` 与 `K/N/I`。`D0/A0 -> INVALID -> I`；`D2/D1` 且存在正关系为 `VALID_KNOWN -> K`，全部 `NO_MATCH` 才是 `VALID_NOVEL -> N`。

A0 只有 `FALSE_POSITIVE` 和 current-only 的 `NOT_A_DEFECT_CLAIM`；X1v2 不使用后者。W 是独立证据轴：W2 必须同时有原始 executable object、typed input、精确 artifact hash、terminal true/false 和 receipt；缺一项退为 W1/W0。W、L、predicate usage 和方法自报标签不参与 validity、relation、hit 或 FP。

raw-first reviewer 输入使用双方共同 allowlist：两侧 report 均映射为 claim/reason，`location_text` 固定为空；双方都附对应 pair 的 NL、PlantUML 和 source SHA-256。raw target pointer/hash、producer-specific location、predicate、receipt、W、旧 Judge 标签和最终语义标签不进入盲审投影；精确 raw identity/hash 只在 proposal 提交后通过 sealed unblind mapping 进入主 session 的回读与仲裁。字段缺失按 schema 差异保留，不填零。完整 field-level mapping 见 [semantic Judge protocol](../../../discover_matrix/docs/protocol/semantic_judge_protocol.md#双侧-reviewer-输入映射)。

raw inventory 从冻结归档重新枚举：v60/current `1271` reports、X1v2 `512` findings，双方各 `162` method cells；expected ledger `145` 条，dense relation 为 `258535` 行。详情见 [inventory](../derived/manual_adjudication_v2/inventory.json) 和 [protocol](../derived/manual_adjudication_v2/protocol_freeze_v2.md)。

## 主结果

表中 delta 均为 v60/current 减 X1v2 baseline；分号前为 numerator 差，后为百分点差。结构化来源是 [summary.json](../derived/manual_adjudication_v2/summary.json)，每个 report 的稳定审计键是 `report_id`。

| 指标 | v60/current | X1v2 baseline | delta (n; pp) |
|---|---:|---:|---:|
| overall hit@1 / FULL | `310/435 = 71.26%` | `212/435 = 48.74%` | `+98; +22.53 pp` |
| L2 hit@1 / FULL | `105/117 = 89.74%` | `46/117 = 39.32%` | `+59; +50.43 pp` |
| hit@3 | `119/145 = 82.07%` | `104/145 = 71.72%` | `+15; +10.34 pp` |
| hit@all | `86/145 = 59.31%` | `38/145 = 26.21%` | `+48; +33.10 pp` |
| L2 hit@3 | `37/39 = 94.87%` | `26/39 = 66.67%` | `+11; +28.21 pp` |
| L2 hit@all | `33/39 = 84.62%` | `5/39 = 12.82%` | `+28; +71.79 pp` |
| supported coverage, round units | `337/435 = 77.47%` | `245/435 = 56.32%` | `+92; +21.15 pp` |
| supported coverage, unique expected | `128/145 = 88.28%` | `116/145 = 80.00%` | `+12; +8.28 pp` |
| report-based precision | `980/1271 = 77.10%` | `411/512 = 80.27%` | `+569; -3.17 pp` |
| report-based FP rate | `291/1271 = 22.90%` | `101/512 = 19.73%` | `+190; +3.17 pp` |
| partial_only_known_report | `110/1271 = 8.65%` | `45/512 = 8.79%` | `+65; -0.13 pp` |
| partial_only_known_expected | `21/145 = 14.48%` | `24/145 = 16.55%` | `-3; -2.07 pp` |
| ledger K_hit | `119/145 = 82.07%` | `104/145 = 71.72%` | `+15; +10.34 pp` |
| ledger N_group composition | `121/429 = 28.21%` | `132/337 = 39.17%` | `-11; -10.96 pp` |
| ledger I_group composition | `189/429 = 44.06%` | `101/337 = 29.97%` | `+88; +14.09 pp` |
| ledger-based precision | `119/429 = 27.74%` | `104/337 = 30.86%` | `+15; -3.12 pp` |
| ledger-based FP rate | `189/429 = 44.06%` | `101/337 = 29.97%` | `+88; +14.09 pp` |
| FULL-hit max W2 | `197/310 = 63.55%` | `0/212 = 0.00%` | `+197; +63.55 pp` |
| FULL-hit max W1 | `113/310 = 36.45%` | `212/212 = 100.00%` | `-99; -63.55 pp` |
| FULL-hit max W0 | `0/310 = 0.00%` | `0/212 = 0.00%` | `+0; +0.00 pp` |
| W2 / all expected | `197/435 = 45.29%` | `0/435 = 0.00%` | `+197; +45.29 pp` |

`K_hit` 是三轮中至少一次 FULL 的 unique expected issue；N/I 是同一 side、同一 pair 内按人工确认的 substantive property、author-source locus、repair obligation 和 cause 合并的操作性 group。当前 N/I group counts 为 `121`/`189`，baseline 为 `132`/`101`；不跨 side、pair，也不按文本相似度合并。L2 ledger precision/FP 为 `not_applicable`，因为 N/I group 没有自然的 L2 expected 归属。

## D/A、K/N/I 与关系

以下表格使用 report 分母；relation 表使用 dense `(report, expected)` 分母。完整逐条记录见 [v60 decisions](../derived/manual_adjudication_v2/v60_report_decisions.json)、[baseline decisions](../derived/manual_adjudication_v2/x1v2_report_decisions.json) 和 [dense relations](../derived/manual_adjudication_v2/relation_decisions.json)。

| 类别 | v60/current | X1v2 baseline | delta (n; pp) |
|---|---:|---:|---:|
| D2 | `721/1271 = 56.73%` | `408/512 = 79.69%` | `+313; -22.96 pp` |
| D1 | `259/1271 = 20.38%` | `3/512 = 0.59%` | `+256; +19.79 pp` |
| D0 | `120/1271 = 9.44%` | `2/512 = 0.39%` | `+118; +9.05 pp` |
| A0 | `171/1271 = 13.45%` | `99/512 = 19.34%` | `+72; -5.88 pp` |
| K | `749/1271 = 58.93%` | `279/512 = 54.49%` | `+470; +4.44 pp` |
| N | `231/1271 = 18.17%` | `132/512 = 25.78%` | `+99; -7.61 pp` |
| I | `291/1271 = 22.90%` | `101/512 = 19.73%` | `+190; +3.17 pp` |
| FULL_MATCH | `685/184295 = 0.37%` | `265/74240 = 0.36%` | `+420; +0.01 pp` |
| PARTIAL_MATCH | `279/184295 = 0.15%` | `110/74240 = 0.15%` | `+169; +0.00 pp` |
| NO_MATCH | `183331/184295 = 99.48%` | `73865/74240 = 99.49%` | `+109466; -0.02 pp` |

`PARTIAL_MATCH` 提供 supported coverage，但不计主 hit，也不计 FP。只有最终 `INVALID` 计 report-based FP；`VALID_NOVEL` 不是 FP。hit@1 的分母是 435 个 expected-round 单元，hit@3/all 的分母是 145 个 unique expected；L2 对应 117/39。

## W 与 predicate

| W 轴 | v60/current | X1v2 baseline |
|---|---:|---:|
| finding-level W0/W1/W2 | `0/749/522` / `1271` | `1/511/0` / `512` |
| FULL-hit max W2/W1/W0 | `197/113/0` / `310` | `0/212/0` / `212` |
| W2/all-expected | `197/435 = 45.29%` | `0/435 = 0.00%` |

W-on-hits 的分母是有 FULL 的 expected-round hit 单元；W2/all-expected 的分母固定为全部 435 个 expected-round 单元，二者不能互换。

current 的 predicate usage 只统计 frozen 19-registry 中的合法 precise binding。冻结 evaluator 的 planned scope（`planned_scope`，当前 15 个 ID）与逐报告观察到的 `report_bound_plan_count` 分开；每行另记录 route、precise binding、receipt present、terminal true/false、全部 usage 的 W0/W1/W2 以及 FULL-hit supporting usage。receipt 缺失或失败仍留在 usage 分母。baseline 没有同构 predicate schema，predicate usage 明确为 `not_applicable`，不填 0。详见 [predicate_witness_audit.json](../derived/manual_adjudication_v2/predicate_witness_audit.json) 和 [predicate_source_provenance.json](../derived/manual_adjudication_v2/predicate_source_provenance.json)。

| predicate | frozen scope / report-bound plan | routed / precise | receipt | terminal true / false | all usage W0/W1/W2 | FULL-hit usage W0/W1/W2 |
|---|---:|---:|---:|---:|---:|---:|
| `S1` | `yes/0` | `0/0` | `0` | `0/0` | `0/0/0` / `0` | `0/0/0` / `0` |
| `S2` | `yes/166` | `166/166` | `166` | `0/166` | `0/0/166` / `166` | `0/0/80` / `80` |
| `S3` | `yes/93` | `93/93` | `93` | `0/93` | `0/0/93` / `93` | `0/0/63` / `63` |
| `S4` | `yes/6` | `6/6` | `6` | `0/6` | `0/0/6` / `6` | `0/0/6` / `6` |
| `S5` | `yes/337` | `337/337` | `337` | `0/63` | `0/274/63` / `337` | `0/27/7` / `34` |
| `S6` | `yes/0` | `0/0` | `0` | `0/0` | `0/0/0` / `0` | `0/0/0` / `0` |
| `G1` | `yes/105` | `105/105` | `105` | `0/79` | `0/26/79` / `105` | `0/23/72` / `95` |
| `G2` | `yes/1` | `1/1` | `1` | `0/1` | `0/0/1` / `1` | `0/0/0` / `0` |
| `G3` | `yes/0` | `0/0` | `0` | `0/0` | `0/0/0` / `0` | `0/0/0` / `0` |
| `G4` | `yes/0` | `0/0` | `0` | `0/0` | `0/0/0` / `0` | `0/0/0` / `0` |
| `R1` | `yes/0` | `0/0` | `0` | `0/0` | `0/0/0` / `0` | `0/0/0` / `0` |
| `R2` | `yes/32` | `32/32` | `32` | `0/32` | `0/0/32` / `32` | `0/0/0` / `0` |
| `R3` | `no/0` | `0/0` | `0` | `0/0` | `0/0/0` / `0` | `0/0/0` / `0` |
| `R4` | `yes/0` | `0/0` | `0` | `0/0` | `0/0/0` / `0` | `0/0/0` / `0` |
| `V1` | `yes/0` | `0/0` | `0` | `0/0` | `0/0/0` / `0` | `0/0/0` / `0` |
| `V2` | `no/0` | `0/0` | `0` | `0/0` | `0/0/0` / `0` | `0/0/0` / `0` |
| `V3` | `no/0` | `0/0` | `0` | `0/0` | `0/0/0` / `0` | `0/0/0` / `0` |
| `V4` | `yes/85` | `85/85` | `85` | `0/82` | `0/3/82` / `85` | `0/3/72` / `75` |
| `V5` | `no/0` | `0/0` | `0` | `0/0` | `0/0/0` / `0` | `0/0/0` / `0` |

## Calibration 与审查

444 条 frozen N 与 106 条 frozen I 共 550 条 calibration/reference rows。raw-first blind calibration 的 strict D/A agreement 为 `546/550 = 99.27%`，dense relation agreement 为 `549/550 = 99.82%`；mismatch `5` 条，[targeted reread](../derived/manual_adjudication_v2/pane5_targeted_re_review.json) 对 mismatch 的闭合为 `5/5`，总 targeted reread 记录为 `15` 条，closure=`True`，sentinel 为 `True`，calibration status 为 `PASS`。reference 同单位聚合见 [reference_ledger_aggregate.json](../derived/manual_adjudication_v2/reference_ledger_aggregate.json)。

主 session 是用户授权的 pane5 人类监督 adjudication session。每条最终记录都有 `human_confirmation=true`、`human_supervised_session=true`、primary/final `human:pane5-supervised-adjudicator`；independent reviewer 如实记录为 `subagent:raw-first-independent-proposal`，先 raw-first blind，再解盲比较，未冒充真人。逐条 evidence-read、授权消息/时间、attestation 和 closure 见 [pane5_evidence_reads.json](../derived/manual_adjudication_v2/pane5_evidence_reads.json)、[pane5_adjudications.json](../derived/manual_adjudication_v2/pane5_adjudications.json)、[human_supervised_authorization.json](../derived/manual_adjudication_v2/human_supervised_authorization.json) 与 [review_log.json](../derived/manual_adjudication_v2/review_log.json)。

## 成本与限制

| 阶段 | v60/current | X1v2 baseline |
|---|---:|---:|
| method cost | `$7.18277320`; eligible=True | `$6.77501040`; eligible=True |
| Judge cost | `$39.78176580`; eligible=False | `$11.45008520`; eligible=True |
| Judge logical calls | `1374` | `not recorded` |

台账不是完整缺陷宇宙；人工归并是本协议下的 operational group，不宣称本体论上的唯一缺陷数。L2 的语义边界、baseline schema 差异、baseline 缺少原始 predicate receipt、v60 Judge 成本中未定价调用，以及观察性比较不能推出因果，都是限制。v27/v46 和旧 v3.2 headline 只保留在 archive/history，不混入本报告主分母。

## 复算入口

```bash
PYTHONPATH=project_1_llm_state_machine_modeling/paper_stm_issue_discover/evaluation/src python project_1_llm_state_machine_modeling/paper_stm_issue_discover/scripts/evaluation/validate_manual_adjudication.py --directory project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline/derived/manual_adjudication_v2
PYTHONPATH=project_1_llm_state_machine_modeling/paper_stm_issue_discover/evaluation/src:project_1_llm_state_machine_modeling/paper_stm_issue_discover/scripts/evaluation python project_1_llm_state_machine_modeling/paper_stm_issue_discover/scripts/evaluation/recompute_manual_adjudication.py --directory project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline/derived/manual_adjudication_v2
```

上述命令只读取冻结 raw/reference 和 canonical decisions，不调用 provider，不重跑 method/Judge，也不修改 raw。MANIFEST 绑定所有 canonical JSON/TSV、过程审计、输入 hash 和 supporting artifact。
