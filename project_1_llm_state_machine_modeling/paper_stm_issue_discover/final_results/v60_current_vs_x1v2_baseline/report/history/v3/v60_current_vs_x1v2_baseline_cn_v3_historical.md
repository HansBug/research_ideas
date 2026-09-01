# v60/current 与 X1v2 baseline 的历史 v3 评测记录

> **Superseded.** 当前论文主结果已迁移到
> [v4 公平对照报告](../../v60_current_vs_x1v2_baseline_v4_cn.md)。本文件保留作历史复算
> 记录，不是当前 headline，不用于当前主结论或 precision/hit 表。

> 主结果使用 v60/current 的既有最终人工监督裁定与 X1v2 baseline v3 对全部非 K 报告的逐条人工重审。v2 是历史输入；v3 不覆盖或修改 frozen K、raw、current、method 或 Judge 制品。

## 口径与范围

current/v60 使用 `issue-189-195-manual-evidence-v2`；baseline 非 K 重审使用 `issue-189-195-baseline-ni-v3`。两侧都按 issue #189/#195 的事实、D/A、expected relation 和机械 K/N/I 闭合执行。顺序固定为：作者源事实 -> D2/D1/D0/A0 -> validity -> 全部 145 个 expected relation -> K/N/I。

v3 只重审 baseline 原非 K 的 233 条；279 条已有 K 从 v2 按字节内容/字段快照冻结复制。D0/A0 均为 I，A0 仅使用 `FALSE_POSITIVE`；W、predicate、Judge 输出和 ledger 缺失不能决定 validity。

raw inventory 与 ledger 均由归档重新读取：current `1271` 条、baseline `512` 条、expected `145` 条。结构化来源是 [current v2 summary](../../../derived/manual_adjudication_v2/summary.json)、[baseline v3 summary](../../../derived/manual_adjudication_v3_baseline_ni/recomputed_summary_v3.json) 和 [v3 manifest](../../../derived/manual_adjudication_v3_baseline_ni/publication_manifest_v3_baseline_ni.json)。

## 主结果

delta 为 v60/current 减 X1v2 baseline；分号前是 numerator 差，分号后是百分点差。hit@1 的分母是 145 个 expected × 3 个 round，即 435 个 expected-round units；不是单轮的 145。

| 指标 | v60/current | X1v2 baseline | delta (n; pp) |
|---|---:|---:|---:|
| overall hit@1 / FULL | `310/435 = 71.26%` | `227/435 = 52.18%` | `+83; +19.08 pp` |
| L2 hit@1 / FULL | `105/117 = 89.74%` | `50/117 = 42.74%` | `+55; +47.01 pp` |
| hit@3 | `119/145 = 82.07%` | `106/145 = 73.10%` | `+13; +8.97 pp` |
| hit@all | `86/145 = 59.31%` | `46/145 = 31.72%` | `+40; +27.59 pp` |
| L2 hit@3 | `37/39 = 94.87%` | `26/39 = 66.67%` | `+11; +28.21 pp` |
| L2 hit@all | `33/39 = 84.62%` | `8/39 = 20.51%` | `+25; +64.10 pp` |
| supported coverage, round units | `337/435 = 77.47%` | `264/435 = 60.69%` | `+73; +16.78 pp` |
| supported coverage, unique expected | `128/145 = 88.28%` | `119/145 = 82.07%` | `+9; +6.21 pp` |
| report-based precision | `980/1271 = 77.10%` | `417/512 = 81.45%` | `+563; -4.34 pp` |
| report-based FP rate | `291/1271 = 22.90%` | `95/512 = 18.55%` | `+196; +4.34 pp` |
| partial_only_known_report | `110/1271 = 8.65%` | `56/512 = 10.94%` | `+54; -2.28 pp` |
| partial_only_known_expected | `21/145 = 14.48%` | `13/145 = 8.97%` | `+8; +5.52 pp` |
| ledger K_hit | `119/145 = 82.07%` | `106/145 = 73.10%` | `+13; +8.97 pp` |
| ledger/group diagnostic ratio | `240/429 = 55.94%` | `204/299 = 68.23%` | `+36; -12.28 pp` |
| ledger/group diagnostic invalid share | `189/429 = 44.06%` | `95/299 = 31.77%` | `+94; +12.28 pp` |
| FULL-hit max W2 | `197/310 = 63.55%` | `0/227 = 0.00%` | `+197; +63.55 pp` |
| FULL-hit max W1 | `113/310 = 36.45%` | `227/227 = 100.00%` | `-114; -63.55 pp` |
| FULL-hit max W0 | `0/310 = 0.00%` | `0/227 = 0.00%` | `+0; +0.00 pp` |
| W2 / all expected | `197/435 = 45.29%` | `0/435 = 0.00%` | `+197; +45.29 pp` |

baseline ledger/group composition 为 `K_hit=106`、`N_group=98`、`I_group=95`，分母为三者之和；I group 仅为 invalid diagnostic cluster，不是真实缺陷。L2 ledger precision 与 baseline predicate usage 均为 `not_applicable`，并保留 reason。

## D/A 与 K/N/I

| 类别 | v60/current | X1v2 baseline | delta (n; pp) |
|---|---:|---:|---:|
| D2 | `721/1271 = 56.73%` | `342/512 = 66.80%` | `+379; -10.07 pp` |
| D1 | `259/1271 = 20.38%` | `75/512 = 14.65%` | `+184; +5.73 pp` |
| D0 | `120/1271 = 9.44%` | `85/512 = 16.60%` | `+35; -7.16 pp` |
| A0 | `171/1271 = 13.45%` | `10/512 = 1.95%` | `+161; +11.50 pp` |
| K | `749/1271 = 58.93%` | `312/512 = 60.94%` | `+437; -2.01 pp` |
| N | `231/1271 = 18.17%` | `105/512 = 20.51%` | `+126; -2.33 pp` |
| I | `291/1271 = 22.90%` | `95/512 = 18.55%` | `+196; +4.34 pp` |
| FULL_MATCH | `685/184295 = 0.37%` | `288/74240 = 0.39%` | `+397; -0.02 pp` |
| PARTIAL_MATCH | `279/184295 = 0.15%` | `124/74240 = 0.17%` | `+155; -0.02 pp` |
| NO_MATCH | `183331/184295 = 99.48%` | `73828/74240 = 99.45%` | `+109503; +0.03 pp` |

`PARTIAL_MATCH` 进入 supported coverage，不进入主 FULL hit；只有 INVALID/I 进入 report-based FP。K hit 在 expected ID 层去重，N 以 substantive group 展示，I cluster 独立命名。

## W 与 predicate

W0/W1/W2 是独立证据轴，不参与 validity、relation、hit 或 FP。W2 只接受报告自带 executable object、typed input、精确 artifact hash、terminal result 和原始 receipt；后验 Judge 不能升级 baseline W。

| finding-level W | v60/current | X1v2 baseline |
|---|---:|---:|
| W0 | `0/1271` | `1/512` |
| W1 | `749/1271` | `511/512` |
| W2 | `522/1271` | `0/512` |

| FULL-hit witness | v60/current | X1v2 baseline |
|---|---:|---:|
| maximum W2 | `197/310 = 63.55%` | `0/227 = 0.00%` |
| maximum W1 | `113/310 = 36.45%` | `227/227 = 100.00%` |
| maximum W0 | `0/310 = 0.00%` | `0/227 = 0.00%` |

W-on-hits 的分母分别是 current `310` 与 baseline `227` 个 FULL expected-round units；W2/all-expected 的分母固定为 `435`，不能互换。

current predicate usage 见 [predicate_witness_audit.json](../../../derived/manual_adjudication_v2/predicate_witness_audit.json)，planned scope 为 `full-scale-15`、`15` 个 ID。全部 usage 与 FULL-hit supporting usage 分母分开，receipt 缺失/失败仍留在 usage 分母；baseline predicate usage 为 `not_applicable`，不是零。

| predicate | planned | report-bound | precise | receipt | all usage W0/W1/W2 | FULL-hit usage W0/W1/W2 |
|---|---:|---:|---:|---:|---:|---:|
| `S1` | `yes` | `0` | `0` | `0` | `0/0/0 / 0` | `0/0/0 / 0` |
| `S2` | `yes` | `166` | `166` | `166` | `0/0/166 / 166` | `0/0/80 / 80` |
| `S3` | `yes` | `93` | `93` | `93` | `0/0/93 / 93` | `0/0/63 / 63` |
| `S4` | `yes` | `6` | `6` | `6` | `0/0/6 / 6` | `0/0/6 / 6` |
| `S5` | `yes` | `337` | `337` | `337` | `0/274/63 / 337` | `0/27/7 / 34` |
| `S6` | `yes` | `0` | `0` | `0` | `0/0/0 / 0` | `0/0/0 / 0` |
| `G1` | `yes` | `105` | `105` | `105` | `0/26/79 / 105` | `0/23/72 / 95` |
| `G2` | `yes` | `1` | `1` | `1` | `0/0/1 / 1` | `0/0/0 / 0` |
| `G3` | `yes` | `0` | `0` | `0` | `0/0/0 / 0` | `0/0/0 / 0` |
| `G4` | `yes` | `0` | `0` | `0` | `0/0/0 / 0` | `0/0/0 / 0` |
| `R1` | `yes` | `0` | `0` | `0` | `0/0/0 / 0` | `0/0/0 / 0` |
| `R2` | `yes` | `32` | `32` | `32` | `0/0/32 / 32` | `0/0/0 / 0` |
| `R3` | `no` | `0` | `0` | `0` | `0/0/0 / 0` | `0/0/0 / 0` |
| `R4` | `yes` | `0` | `0` | `0` | `0/0/0 / 0` | `0/0/0 / 0` |
| `V1` | `yes` | `0` | `0` | `0` | `0/0/0 / 0` | `0/0/0 / 0` |
| `V2` | `no` | `0` | `0` | `0` | `0/0/0 / 0` | `0/0/0 / 0` |
| `V3` | `no` | `0` | `0` | `0` | `0/0/0 / 0` | `0/0/0 / 0` |
| `V4` | `yes` | `85` | `85` | `85` | `0/3/82 / 85` | `0/3/72 / 75` |
| `V5` | `no` | `0` | `0` | `0` | `0/0/0 / 0` | `0/0/0 / 0` |

## 成本

成本只报告冻结 run record 中已有的金额和 eligibility；本 v3 重审没有新增 provider、method 或 Judge 调用。

| 阶段 | v60/current | X1v2 baseline |
|---|---:|---:|
| method | `$7.18277320`; eligible=`True` | `$6.77501040`; eligible=`True` |
| Judge | `$39.78176580`; eligible=`False` | `$11.45008520`; eligible=`True` |

## Baseline round/pair 分布

下表只展示 baseline v3；完整 pair-level JSON 位于 [recomputed summary](../../../derived/manual_adjudication_v3_baseline_ni/recomputed_summary_v3.json)。

| round | reports | K | N | I | D2 | D1 | D0 | A0 |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 173 | 99 | 40 | 34 | 110 | 29 | 31 | 3 |
| 2 | 163 | 99 | 36 | 28 | 113 | 22 | 25 | 3 |
| 3 | 176 | 114 | 29 | 33 | 119 | 24 | 29 | 4 |

| pair | reports | K | N | I | D2 | D1 | D0 | A0 |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0000 | 7 | 5 | 1 | 1 | 4 | 2 | 1 | 0 |
| 0001 | 4 | 4 | 0 | 0 | 4 | 0 | 0 | 0 |
| 0002 | 7 | 7 | 0 | 0 | 6 | 1 | 0 | 0 |
| 0003 | 6 | 0 | 3 | 3 | 0 | 3 | 2 | 1 |
| 0004 | 12 | 5 | 6 | 1 | 4 | 7 | 1 | 0 |
| 0005 | 9 | 9 | 0 | 0 | 7 | 2 | 0 | 0 |
| 0006 | 7 | 3 | 4 | 0 | 4 | 3 | 0 | 0 |
| 0007 | 9 | 4 | 5 | 0 | 7 | 2 | 0 | 0 |
| 0009 | 13 | 7 | 2 | 4 | 7 | 2 | 4 | 0 |
| 0010 | 18 | 18 | 0 | 0 | 18 | 0 | 0 | 0 |
| 0011 | 6 | 5 | 1 | 0 | 5 | 1 | 0 | 0 |
| 0012 | 5 | 2 | 1 | 2 | 2 | 1 | 2 | 0 |
| 0013 | 9 | 9 | 0 | 0 | 9 | 0 | 0 | 0 |
| 0014 | 15 | 12 | 0 | 3 | 11 | 1 | 3 | 0 |
| 0015 | 4 | 4 | 0 | 0 | 4 | 0 | 0 | 0 |
| 0016 | 2 | 1 | 1 | 0 | 1 | 1 | 0 | 0 |
| 0017 | 3 | 1 | 2 | 0 | 1 | 2 | 0 | 0 |
| 0019 | 19 | 13 | 6 | 0 | 15 | 4 | 0 | 0 |
| 0020 | 11 | 6 | 2 | 3 | 4 | 4 | 3 | 0 |
| 0021 | 5 | 0 | 1 | 4 | 0 | 1 | 4 | 0 |
| 0022 | 7 | 0 | 4 | 3 | 0 | 4 | 3 | 0 |
| 0023 | 5 | 5 | 0 | 0 | 4 | 1 | 0 | 0 |
| 0024 | 18 | 17 | 0 | 1 | 17 | 0 | 1 | 0 |
| 0025 | 14 | 13 | 1 | 0 | 13 | 1 | 0 | 0 |
| 0026 | 7 | 7 | 0 | 0 | 7 | 0 | 0 | 0 |
| 0027 | 9 | 5 | 4 | 0 | 5 | 4 | 0 | 0 |
| 0029 | 18 | 15 | 2 | 1 | 13 | 4 | 1 | 0 |
| 0030 | 10 | 10 | 0 | 0 | 10 | 0 | 0 | 0 |
| 0031 | 8 | 0 | 0 | 8 | 0 | 0 | 8 | 0 |
| 0032 | 10 | 5 | 3 | 2 | 3 | 5 | 2 | 0 |
| 0033 | 11 | 8 | 2 | 1 | 10 | 0 | 1 | 0 |
| 0034 | 29 | 22 | 0 | 7 | 22 | 0 | 6 | 1 |
| 0035 | 11 | 7 | 2 | 2 | 9 | 0 | 2 | 0 |
| 0036 | 17 | 0 | 13 | 4 | 8 | 5 | 4 | 0 |
| 0037 | 10 | 5 | 4 | 1 | 6 | 3 | 1 | 0 |
| 0039 | 5 | 3 | 1 | 1 | 2 | 2 | 0 | 1 |
| 0040 | 6 | 2 | 3 | 1 | 2 | 3 | 1 | 0 |
| 0041 | 8 | 0 | 2 | 6 | 2 | 0 | 6 | 0 |
| 0042 | 4 | 3 | 1 | 0 | 4 | 0 | 0 | 0 |
| 0043 | 7 | 6 | 0 | 1 | 6 | 0 | 1 | 0 |
| 0044 | 4 | 2 | 0 | 2 | 2 | 0 | 2 | 0 |
| 0045 | 6 | 3 | 3 | 0 | 6 | 0 | 0 | 0 |
| 0046 | 13 | 5 | 4 | 4 | 5 | 4 | 3 | 1 |
| 0047 | 11 | 10 | 1 | 0 | 11 | 0 | 0 | 0 |
| 0049 | 19 | 9 | 6 | 4 | 15 | 0 | 3 | 1 |
| 0050 | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 0 |
| 0051 | 6 | 0 | 0 | 6 | 0 | 0 | 6 | 0 |
| 0052 | 4 | 0 | 2 | 2 | 2 | 0 | 2 | 0 |
| 0053 | 8 | 5 | 0 | 3 | 5 | 0 | 0 | 3 |
| 0054 | 9 | 5 | 0 | 4 | 3 | 2 | 3 | 1 |
| 0055 | 8 | 4 | 2 | 2 | 6 | 0 | 1 | 1 |
| 0056 | 10 | 7 | 0 | 3 | 7 | 0 | 3 | 0 |
| 0057 | 6 | 4 | 2 | 0 | 6 | 0 | 0 | 0 |
| 0059 | 22 | 9 | 8 | 5 | 17 | 0 | 5 | 0 |

## 非 K 迁移与分组

v3 non-K 迁移计数来自 [summary_v3.json](../../../derived/manual_adjudication_v3_baseline_ni/summary_v3.json)：`{"I->I": 28, "I->K": 30, "I->N": 43, "N->I": 67, "N->K": 3, "N->N": 62}`。新增 K 的完整 report/expected 映射见 summary 的 `non_k_migrations.rows`。

| migration | count |
|---|---:|
| `I->I` | `28` |
| `I->K` | `30` |
| `I->N` | `43` |
| `N->I` | `67` |
| `N->K` | `3` |
| `N->N` | `62` |

新增 K 共 `33` 条非 K report，全部标记为 `reclassified_from_non_k=true`；下面保留其 report 到 ledger relation 的可追溯映射，完整字段仍以 summary JSON 为准。

| report_id | FULL ledger IDs | PARTIAL ledger IDs |
|---|---|---|
| `0000:r1:baseline_issue_2` | `EIS-0000-02` | `-` |
| `0002:r1:baseline_issue_3` | `EIS-0002-03` | `-` |
| `0002:r2:baseline_issue_1` | `EIS-0002-01` | `EIS-0002-02` |
| `0002:r3:baseline_issue_1` | `EIS-0002-01, EIS-0002-02` | `-` |
| `0002:r3:baseline_issue_2` | `EIS-0002-01` | `-` |
| `0004:r3:baseline_issue_5` | `-` | `EIS-0004-01` |
| `0005:r3:baseline_issue_2` | `-` | `EIS-0005-02` |
| `0005:r3:baseline_issue_3` | `-` | `EIS-0005-02` |
| `0005:r3:baseline_issue_8` | `-` | `EIS-0005-03` |
| `0007:r1:baseline_issue_2` | `-` | `EIS-0007-02` |
| `0007:r2:baseline_issue_3` | `-` | `EIS-0007-02` |
| `0015:r3:baseline_issue_2` | `-` | `EIS-0015-01` |
| `0015:r3:baseline_issue_3` | `-` | `EIS-0015-01` |
| `0019:r1:baseline_issue_2` | `-` | `EIS-0019-03` |
| `0019:r1:baseline_issue_3` | `EIS-0019-02` | `-` |
| `0019:r3:baseline_issue_2` | `EIS-0019-03` | `-` |
| `0019:r3:baseline_issue_5` | `EIS-0019-03` | `-` |
| `0020:r1:baseline_issue_1` | `EIS-0020-02` | `-` |
| `0020:r2:baseline_issue_1` | `EIS-0020-02` | `-` |
| `0027:r1:baseline_issue_1` | `EIS-0027-01` | `-` |
| `0027:r2:baseline_issue_1` | `-` | `EIS-0027-01` |
| `0027:r2:baseline_issue_2` | `EIS-0027-01` | `-` |
| `0029:r1:baseline_issue_1` | `EIS-0029-02` | `-` |
| `0032:r1:baseline_issue_1` | `DIFF-0032-03` | `EIS-0032-01` |
| `0032:r3:baseline_issue_1` | `EIS-0032-01` | `-` |
| `0033:r1:baseline_issue_3` | `EIS-0033-02` | `-` |
| `0037:r2:baseline_issue_3` | `EIS-0037-01` | `-` |
| `0039:r3:baseline_issue_1` | `-` | `EIS-0039-02` |
| `0053:r2:baseline_issue_3` | `EIS-0053-01` | `-` |
| `0054:r2:baseline_issue_1` | `VU-0054-01` | `-` |
| `0054:r3:baseline_issue_1` | `VU-0054-01` | `-` |
| `0056:r3:baseline_issue_4` | `EIS-0056-02` | `-` |
| `0059:r1:baseline_issue_2` | `EIS-0059-01` | `INS-0059-03` |

N report/group 视图：原始非 K N `132`，corrected N `105`，substantive N group `98`，root-cause group `98`；N 的 D2/D1 为 `50/55`，group size distribution 为 `{"1": 92, "2": 5, "3": 1}`。current/v60 的 N 为 `231` 条报告，其中 D2/D1 为 `38/193`；当前 `121` 个 group 是 mechanical grouping count，不能直接写成 `121` 个已经完成同深度人工语义复核的独立缺陷。
I 构成见 `a0_subtypes`：baseline 的 `{"FALSE_POSITIVE": 10}`；current 的 A0 subtype 当前记录为 `NOT_A_DEFECT_CLAIM=118`、`FALSE_POSITIVE=53`。抽样复核提示其中一部分来源于 projection/lowering/runtime delegation 归因，subtype 仍应作为诊断成分解释，不能把 I cluster 表述为 novel defect。

| historical comparison | K | N | I |
|---|---:|---:|---:|
| v2 frozen scope | `279` | `132` | `101` |
| v3 combined | `312` | `105` | `95` |

未合并 I 的敏感性为 `204/299 = 68.23%`；这是未合并 invalid 报告时的诊断性 ledger/group 比值，只用于说明聚类对分母的影响，不是论文主 precision。主 precision 始终使用 report-level `(K+N)/all reports`，因为 I 不是实质缺陷实体。

## 论文解释口径

本报告把 K、N、I 的统计单位明确分开：K 按 expected ledger ID 认领并在 expected 层去重；N
才按同一 side、同一 pair、同一规范义务、source locus/root cause、property 和最小修复意图
归并，允许跨 round；I 不做 substantive defect grouping，只保留 report-level invalid 统计，
必要时另报 diagnostic cluster。该划分与软件测试中 known-fault/false-positive disposition
和 distinct-bug evaluation unit 的区分一致，但完整的 same-pair/same-obligation 规则是本项目
在文献启发下的 operationalization，不是任一单篇论文的原定义。

台账是由博士生/研究人员依据作者 NL、PlantUML 和来源材料人工维护的
`expert-annotated expected issue ledger`，属于 source-backed expected inventory，不宣称穷尽
未知缺陷空间。论文不应把它称为 complete ground truth。

文献依据与适用边界见 [academic citation review](../../../derived/manual_adjudication_v3_baseline_ni/reviews/academic_citation_review.md)。主要锚点包括 Porter et al. (IEEE TSE 1995, DOI `10.1109/32.391380`)、Klees et al. (CCS 2018, DOI `10.1145/3243734.3243804`)、NIST SATE IV (SP 500-297, DOI `10.6028/NIST.SP.500-297`)、Pearson et al. (ICSE 2017, DOI `10.1109/ICSE.2017.62`)、Ahmed et al. (MODELS 2025, DOI `10.1109/MODELS67397.2025.00014`) 和 Martinez et al. (EMSE, DOI `10.1007/s10664-016-9470-4`)。

## 审计与限制

每条 v3 非 K 记录保留 raw/source refs、hash、145 relations、两份独立 proposal 和 pane5 confirmation；当前 review log 记录 `8` 个独立 reviewer、`233/233` 决策覆盖、`146` 条分歧和 `233` 条 pane5 仲裁。Track B proposal 是 blind proposal，不是最终人工裁定。旧 v2/Judge 只作冻结 scope、历史 provenance 或工具诊断，不倒灌 v3 标签。

审计限制包括：台账不保证覆盖完整缺陷宇宙；人工归并是 operationalization；current N 的
mechanical groups 中仍有少量条目需要更深的 source-first 复核；current I 的 A0 subtype 可能
混入表示/归因债务；L2 对 N/I 无自然归属；baseline 没有 current-side predicate schema；观察性
比较不推出因果。legacy/probe proposal 保留但被 v3 manifest 明确排除。

## 离线复算

```bash
PYTHONPATH=project_1_llm_state_machine_modeling/paper_stm_issue_discover/evaluation/src python project_1_llm_state_machine_modeling/paper_stm_issue_discover/scripts/evaluation/build_manual_adjudication_v3_baseline_ni.py --archive-root project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline --output project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline/derived/manual_adjudication_v3_baseline_ni
python project_1_llm_state_machine_modeling/paper_stm_issue_discover/scripts/evaluation/build_baseline_n_groups_v3.py --decisions project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline/derived/manual_adjudication_v3_baseline_ni/baseline_report_decisions_v3.json --output project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline/derived/manual_adjudication_v3_baseline_ni/baseline_n_groups_v3.json
python project_1_llm_state_machine_modeling/paper_stm_issue_discover/scripts/evaluation/recompute_baseline_v3_summary.py --archive-root project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline --output project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline/derived/manual_adjudication_v3_baseline_ni/recomputed_summary_v3.json
python project_1_llm_state_machine_modeling/paper_stm_issue_discover/scripts/evaluation/validate_baseline_v3.py --archive-root project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline
python project_1_llm_state_machine_modeling/paper_stm_issue_discover/scripts/evaluation/build_baseline_v3_manifest.py --archive-root project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline
```
