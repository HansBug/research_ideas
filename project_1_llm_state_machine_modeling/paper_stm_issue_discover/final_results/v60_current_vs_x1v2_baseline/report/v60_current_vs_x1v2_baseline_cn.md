# v60/current 与 X1v2 baseline 的最终实验结果

## 结论

在相同的 54 pair、3 round、145 条 expected issue 和冻结 Judge 口径下，v60/current 的 overall hit@1/FULL 为 `306/435 = 70.34%`，高于 X1v2 baseline 的 `211/435 = 48.51%`，差值为 `+21.83` 个百分点。L2 FULL 为 `104/117 = 88.89%`，相对 baseline 的 `46/117 = 39.32%` 提高 `+49.57` 个百分点。report-level semantic precision 为 `91.66%`，比 baseline 高 `11.58` 个百分点。

v60 的 FULL-hit max-W2 为 `211/306 = 68.95%`，另有 `95/306 = 31.05%` 的 FULL hit 最高为 W1，W0 为 `0/306 = 0%`。`W2/全部 expected = 219/435 = 50.34%` 的分母不同，不能互换。X1v2 没有同构的 19 谓词 receipt schema，但 W 并不依赖该谓词体系：对其 512 条冻结 finding 的 Judge-blinded 两轮独立逐条回溯审计得到 `W0/W1/W2 = 1/511/0`。因此 X1v2 的 predicate usage 不适用，W 轴适用且可比较。

这些结果说明该冻结 v60 制品在本 ledger 和 Judge 口径上的覆盖更高；它们不证明对未包含在 ledger 的全部缺陷空间、其他 FCSTM 片段或其他模型的同等效果。当前证据也不覆盖时钟、不变式、正交 region/并发、hybrid 或无界时序语义。v60 与其他完整运行是独立 LLM 采样，不能把运行间差异归因为某一项代码修改。

## 实验对象与公平性

| 项目 | v60/current | X1v2 baseline |
|---|---|---|
| method | commit `66b5d71aecd73f6eeddac082037f7c34e04da057`；run `915d56e45a634c27aa03866f03818c6d` | 162 个 legacy `record.json`；没有顶层 method commit，见已知缺口 |
| method 模型 | `gpt-5.6-luna` | `gpt-5.6-luna` |
| method 并发/重试 | `workers=16`，`transport_retries=8` | legacy record 未保存同构运行参数 |
| method 完整性 | `162/162` terminal；crash `0`、failed pair `0`、diagnostic `0` | `162/162` record；method 层无缺格 |
| Judge | commit `05cf0da6f7d9fcf1de26c349b586fc71c268f1c5` | 同一 commit |
| Judge 协议 | issue #195，`github-issue-195.d774d9bd3e4c.issue-189-clarification.v3.2` | 同一协议；execution erratum commit `265d977c81132cf6320b28dcde95ec46950f7e91` |
| universe | 54 pair × 3 round；145 expected，435 round-level expected | 相同 |

两侧都由冻结 Judge 的 composite-selected `PairJudgeResult` 复算，选择路径和 result hash 由 composite receipt 限定。X1v2 Judge 历史上有 4 个 schema-terminal source cell，经独立 repair result 补齐；composite 已明确保留失败和替代结果。v60 Judge 无 source failure。原始制品、commit、hash 和来源运行目录见 [顶层 manifest](../archive_manifest.json) 与两侧 [v60 manifest](../raw/v60_current/archive_manifest.json)、[baseline manifest](../raw/x1v2_baseline/archive_manifest.json)。

`FULL`、`PARTIAL`、`NONE` 是 issue #195 Judge 的 expected relation；`VALID_KNOWN`、`VALID_NOVEL`、`INVALID` 是 report validity。W0/W1/W2 是 issue #189 的 method evidence 等级。本报告的 L2 子集由外置 ledger 的 `l_level` 标注；L 是 issue #189 的信息需求维度，method 不在运行时输出或裁定 `l_level`。方法内部的 `D2/D1/D0` 与 Judge 的 validity 是不同维度：仅 `D2/D1` 进入方法发布面，`D0` 不发布，Judge 仍独立裁定报告有效性与 expected relation。一次 terminal backend `true` 或 `false` 可满足 W2 的执行条件，`pass` 本身不构成已发布 violation，publication 还依赖精确问题语义和 D 判定。相关口径见 [semantic Judge protocol](../../../discover_matrix/docs/protocol/semantic_judge_protocol.md)、[final metrics policy](../../../discover_matrix/docs/protocol/final_output_metrics_policy.md) 和 [ground-truth limitations](../../../discover_matrix/docs/protocol/ground_truth_limitations.md)。

## 主结果

`hit@1` 在本文中固定指 round-level FULL：435 个 `(expected issue, round)` 记录中的 FULL 数；`hit@3` 指 145 个 expected 中三轮至少一次 FULL；`hit@all` 指三轮均 FULL。L2 使用 39 个 expected、117 个 round-level expected。计数、分母和百分比均来自 [机器汇总](../derived/recomputed_summary.json)。

| 指标 | v60/current | X1v2 baseline | 差值 |
|---|---:|---:|---:|
| overall hit@1 / FULL | `306/435 = 70.34%` | `211/435 = 48.51%` | `+21.83` pp |
| L2 hit@1 / FULL | `104/117 = 88.89%` | `46/117 = 39.32%` | `+49.57` pp |
| hit@3 | `118/145 = 81.38%` | `104/145 = 71.72%` | `+9.66` pp |
| hit@all | `84/145 = 57.93%` | `37/145 = 25.52%` | `+32.41` pp |
| PARTIAL | `30/435 = 6.90%` | `33/435 = 7.59%` | `-0.69` pp |
| NONE | `99/435 = 22.76%` | `191/435 = 43.91%` | `-21.15` pp |
| report semantic precision | `1165/1271 = 91.66%` | `410/512 = 80.08%` | `+11.58` pp |
| root-cause cluster precision | `1108/1208 = 91.72%` | `409/511 = 80.04%` | `+11.68` pp |

每轮结果如下。K/N/I 顺序为 `VALID_KNOWN/VALID_NOVEL/INVALID`；cluster 以 `(pair_id, round, root_cause_cluster_key)` 分组，含 K 时优先计 K。

| arm / round | overall FULL | L2 FULL | report K/N/I | cluster K/N/I |
|---|---:|---:|---:|---:|
| v60 r1 | `99/145 = 68.28%` | `35/39 = 89.74%` | `248/138/29` | `233/133/28` |
| v60 r2 | `107/145 = 73.79%` | `36/39 = 92.31%` | `248/159/39` | `239/153/34` |
| v60 r3 | `100/145 = 68.97%` | `33/39 = 84.62%` | `225/147/38` | `217/133/38` |
| baseline r1 | `64/145 = 44.14%` | `12/39 = 30.77%` | `85/45/43` | `85/44/43` |
| baseline r2 | `73/145 = 50.34%` | `17/39 = 43.59%` | `91/45/27` | `91/45/27` |
| baseline r3 | `74/145 = 51.03%` | `17/39 = 43.59%` | `100/44/32` | `100/44/32` |
| v60 合并 | `306/435 = 70.34%` | `104/117 = 88.89%` | `721/444/106` | `689/419/100` |
| baseline 合并 | `211/435 = 48.51%` | `46/117 = 39.32%` | `276/134/102` | `276/133/102` |

`VALID_NOVEL` 不是 FP；ledger-unmatched report 和 `PARTIAL` 也不是 FP。这里的 semantic FP 以 `INVALID` 计。v60 的 INVALID report 从 `102` 变为 `106`，但报告总数由 `512` 增至 `1271`，所以 precision 仍提高；报告必须同时给出绝对数和比例，不能只保留有利的一侧。

## FULL hit 中的最高 W 与全部 expected 的 W2

| 口径 | v60/current | X1v2 baseline |
|---|---:|---:|
| FULL hit 的 max-W2 | `211/306 = 68.95%` | `0/211 = 0.00%` |
| FULL hit 的 max-W1 | `95/306 = 31.05%` | `211/211 = 100.00%` |
| FULL hit 的 max-W0 | `0/306 = 0%` | `0/211 = 0%` |
| W2 / 全部 expected | `219/435 = 50.34%` | `0/435 = 0.00%` |

该表不是 finding-level W 分布。v60 的数值来自 [expected-witness audit](../raw/v60_current/judge/composite/evaluator/expected_issue_witness_audit.json)；X1v2 的数值来自 [X1v2 finding 审计](../derived/x1v2_witness_level_audit.json) 和 [X1v2 FULL-hit 审计](../derived/x1v2_full_hit_max_witness_audit.json)。两侧都只在每个 `FULL` expected row 的 `full_report_ids` 内取最高 W。v60 的 `627` 条 W2 evidence record 与 `627` 个 W2 audit bundle 一一对应，无孤儿 bundle。X1v2 没有原运行期 executable witness、evaluation receipt、精确 evaluated-artifact hash 和 terminal result，所以 W2 为 `0`；这不是 Judge 事后核验的倒灌结果。

X1v2 finding-level W 为 `W0/W1/W2 = 1/511/0`，分母 `512`。按 round 分别为 r1=`1/172/0`（`173`）、r2=`0/163/0`（`163`）、r3=`0/176/0`（`176`）。按 frozen Judge validity 的后置关联分层为 `VALID_KNOWN=0/276/0`、`VALID_NOVEL=1/133/0`、`INVALID=0/102/0`；这些 association 只在双审后用于分层，未参与 W 判定。overall 的 211 个 FULL hit 为 `W2/W1/W0 = 0/211/0`；L2 的 46 个 FULL hit 为 `0/46/0`。两次 Judge-blinded 独立审阅覆盖均为 `512/512`，两轮标签没有 W 级分歧；独立语义复核支持一条受限 post-review correction，将 `0036:r1:0036:r1:baseline_issue_4` 从共同 W1 裁为 W0。它不是 FULL supporting report，所以 hit 级结果不变，详见 [审计决策记录](../reviews/05_x1v2_witness_level_reaudit.md)。

## Predicate usage

三个集合必须分开：冻结 registry 有 19 个谓词；full-scale-15 计划集合为 15 个；v60 有真实 terminal receipt 的计划谓词为 12 个，即 `12/15`。`G3`、`S6`、`V1` 没有 terminal receipt。`G3` 和 `V1` 的原因是 `no_method_route_or_contract`；`S6` 有 8 个 receipt，但全部 `input_contract_missing`，所以不是 terminal use。`R3`、`V2`、`V3`、`V5` 不在 full-scale-15 的计划分母中。19 个冻结谓词均保留 registry 定义和 backend 目标；未计划或本轮未执行不改变其学术资格。

下表的“候选/精确”是 issue-candidate evidence record；只产生 pass receipt 的 G4、R1、R4 因而在这两列为 0。“receipt”覆盖 route/receipt 审计面；“终态 P/V”是 backend terminal pass/violation。`W2` 是该谓词支持的 W2 finding 数，不是命中数。详细字段见 [predicate_table](../derived/recomputed_summary.json) 与 [字段说明](../SCHEMA.md)。

| ID | family / 语义 | 计划 | 候选/精确 | receipt | 终态 P/V | W2 | 退化或 zero-use 原因 |
|---|---|---:|---:|---:|---:|---:|---|
| S1 | structural / element exists | 是 | `2/1` | `121` | `119/0` | `0` | `2` input missing；W1=`1`，W0=`1` |
| S2 | structural / transition exists | 是 | `235/234` | `387` | `152/235` | `234` | W0=`1` |
| S3 | structural / trigger-set equals | 是 | `96/96` | `249` | `153/96` | `96` | 无 |
| S4 | structural / state-action attached | 是 | `6/6` | `18` | `12/6` | `6` | 无 |
| S5 | structural / transition-guard equals | 是 | `356/356` | `356` | `0/81` | `81` | `275` input missing，W1=`275` |
| S6 | structural / transition-effect attached | 是 | `8/8` | `8` | `0/0` | `0` | `8` input missing，W1=`8` |
| G1 | graph / finite may-reach | 是 | `113/112` | `113` | `0/81` | `80` | `32` input missing，W1=`32`，W0=`1` |
| G2 | graph / declared completion must-reach | 是 | `2/2` | `2` | `0/2` | `2` | 无 |
| G3 | graph / route avoids forbidden set | 是 | `0/0` | `0` | `0/0` | `0` | `no_method_route_or_contract` |
| G4 | graph / coaccessible to marked node | 是 | `0/0` | `12` | `12/0` | `0` | pass-only receipt |
| R1 | runtime / event consumed | 是 | `0/0` | `34` | `34/0` | `0` | pass-only receipt |
| R2 | runtime / state reached after trace window | 是 | `46/46` | `162` | `116/46` | `46` | 无 |
| R3 | runtime / behavior occurs | 否 | `0/0` | `0` | `0/0` | `0` | not planned |
| R4 | runtime / state retained | 是 | `0/0` | `4` | `4/0` | `0` | pass-only receipt |
| V1 | verification / guards disjoint | 是 | `0/0` | `0` | `0/0` | `0` | `no_method_route_or_contract` |
| V2 | verification / guards complete | 否 | `0/0` | `0` | `0/0` | `0` | not planned |
| V3 | verification / response within bound | 否 | `0/0` | `0` | `0/0` | `0` | not planned |
| V4 | verification / deadlock free | 是 | `88/88` | `94` | `6/82` | `82` | `6` input missing，W1=`6` |
| V5 | verification / state invariant | 否 | `0/0` | `0` | `0/0` | `0` | not planned |

X1v2 没有同构的 19 谓词 registry 或 terminal receipt schema，因此不能将 v60 的 predicate usage、pass/violation 或退化项对它强行填为可比指标。W 不属于这个限制：X1v2 的 W1 由具体定位质量决定，W2 则严格要求其自身运行期的可执行对象和 terminal 记录。

## K/N/I 的语义边界与学术来源

`VALID_KNOWN` 表示与 ledger 已知问题语义相符；`VALID_NOVEL` 是语义有效但不等同于某条 ledger expected 的报告；`INVALID` 是语义 FP。它们与 expected hit 是不同维度：一个 W1 report 可以形成 `VALID_KNOWN`/FULL，一个 `VALID_NOVEL` 不应被称为 FP，也不能让 `INVALID` 与同一 finding 的 FULL/PARTIAL 同时成立。

冻结的 19 个 predicate ID、输入语义和 source ID 见 [predicate registry](../reference/predicate_registry.json)。来源 catalog 与审计见 [current source catalog](../reference/current_source_catalog.json) 和 [source audit](../../../related_work/provenance/CURRENT_SOURCE_AUDIT.md)。学术来源资格、当前输入的 soundness fragment 与一次 backend true/false 是不同维度；bibliography/source metadata 不参与运行时 W2 gate。该叙述不声称每个谓词具有完全相同的来源类型组合，也不把 source catalog 的 metadata 用作重设 W2 的门。

## 成本与运行完整性

method 和 Judge 成本分别报告。v60 method 的 `$7.18277320` 具有成本资格；X1v2 corrected method cost 的 `$6.77501040` 也具有成本资格。两者的 method cost 比约为 `1.06x`。v60 Judge 的 `$39.78176580` 是已记录成本，但 `cost_eligible=false`：`1,374` 个逻辑调用中有 `10` 个应计费调用缺少可定价 usage，因此不能作为精确完整总价，也不能与 baseline Judge 成本作精确倍率比较。X1v2 Judge composite 的 total incurred cost 是 `$11.45008520`，具有成本资格；其中 selected result cost 为 `$10.79275320`，历史 failed source cells 产生 `$0.65733200` 原始失败成本，必须保留在 total incurred cost 中。

| arm / 阶段 | 调用与 token/cost 审计 | 成本资格 |
|---|---|---|
| v60 method | `1,065` 个已计价 provider 调用；input=`18,765,114`，output=`2,534,776`，cache read=`19,400,960`，cache write=`0`；`$7.18277320` | eligible |
| v60 method 阶段成本 | contract extraction=`$1.54225050`，contract completion=`$0.71855510`，discovery grounding=`$3.74355360`，D adjudication=`$1.13929390`，D correction=`$0.03912000` | eligible |
| v60 Judge | `1,374` logical calls；priced=`1,364`，unpriced billable=`10`；provider retry=`110`，non-provider outer retry=`14`，schema validation failure=`267`；phase counts=`212/208/112/283/283/276`（relation primary 1/2/arbitration，validity primary 1/2/arbitration）；`$39.78176580` | ineligible；归档的 Judge cost audit 未保存可完整加总的 input/output/cache token breakdown |
| baseline method | `646` logical calls，`890` billable provider requests，`658` outer attempts；uncached input=`16,388,498`，output=`2,660,559`，cache read=`15,232,000`，cache creation=`0`；`$6.77501040` | eligible |
| baseline Judge | `725` logical calls，`868` provider requests，completed=`864`，failed=`4`；input=`45,719,344`，uncached=`26,260,656`，cache read=`19,458,688`，cache creation=`0`，output=`1,921,847`；total incurred `$11.45008520` | eligible |

v60 method 的五个阶段成本占总 method cost 分别为 `21.47%`、`10.00%`、`52.12%`、`15.86%` 和 `0.54%`。X1v2 legacy method-cost audit 不保存同构阶段分类，不能伪造阶段占比。Judge 以公平和准确性为目标，成本统计仅用于审计，不用于倒推或修改 Judge。

## v59/v60 的 evaluator-only paired comparison

该比较不是 X1v2 主比较，而是 v59 与 v60 的 S2 receipt 审计。修正后的定义将三类 carrier 分开：同一精确 typed carrier key 的交集为 `147`；`matched_input_verdict_flips=0`；`before_only_carriers=221`；`after_only_carriers=235`。one-sided carrier 是独立 LLM 采样、route 或 report surface 差异，不能被称为“同输入 backend verdict change”。完整对象、reason/basis 和 carrier 身份见 [paired comparison JSON](../raw/v60_current/judge/composite/evaluator/before_after_paired_comparison.json) 与 [中文摘要](../raw/v60_current/judge/composite/evaluator/before_after_paired_comparison_cn.md)。

该 comparison 的 matched flip 为 0，只说明交集中的 147 个 exact typed carrier 没有 terminal verdict 翻转；它不能把其余观察差异严格归因于 soundness/S2 修正，也不应替代 v60 与 X1v2 的主结果比较。

## 限制与复算入口

- ledger 不是完整缺陷宇宙；结果只对当前 145 条 expected、54 pair 和该冻结 input closure 作陈述，也不覆盖时钟、不变式、正交 region/并发、hybrid 或无界时序语义。
- X1v2 缺失顶层 method commit、19-predicate receipt schema 和同构阶段成本字段；predicate usage 保持 `not_applicable`。W 已通过 512 条双审回溯补齐，其中 W2 为零来自缺少 baseline 自身的运行期可执行见证，不由 later Judge 填补。
- v60 Judge 的 10 个无可定价 usage 调用使 Judge 和 method+Judge 合并成本不具完整资格；不得估算补齐。
- method/Judge 原始 JSON 仍保留 provenance 的绝对源路径；离线复算只使用 archive 内稳定相对路径。源根与 archive 目标的映射见 manifest，原始 `runs/` 路径不构成复算依赖。
- 本报告未启动新 method、Judge 或 provider 调用，也未修改冻结 method/Judge、19 谓词、registry、prompt、route、W/D 或 issue #195 口径。

复算从 [归档 README](../README.md) 的 `validate` 命令开始。该命令检查每侧 SHA-256、派生汇总与 publication manifest（生成后），然后从 `raw/`、`reference/` 重算主指标。审查记录位于 [reviews/](../reviews/)，完成的发布清单位于 [publication_manifest.json](../publication_manifest.json)。
