# 独立事实与数值复算审查（历史冻结 Judge v3.2 快照）

## 范围和方法

审查者独立读取 `raw/v60_current/judge/source_runs/`、`raw/x1v2_baseline/judge/source_runs/`、两侧 composite receipt、v60 `method/method/` 与 `audit_bundles/`、baseline `record.json`、`reference/ledger.json` 和 corrected cost audit。没有读取本目录最终报告的汇总数值，没有调用 provider，也没有编辑仓库文件。

复算以 composite 的 `pair_receipts` 与 result SHA-256 选择 Judge pair result；162 个选中 pair-round 均 hash 一致且无重复。L2 使用 `reference/ledger.json` 中 39 条 L2 issue，而非历史 `l_tier.json`。

## 结果

下列结果是当时冻结的 Judge v3.2 快照，与 [历史机器汇总](../derived/recomputed_summary.json) 一致；
它们不替代当前 `derived/manual_adjudication_v2/summary.json` 的最终人工监督主结果。

| 指标 | v60/current | X1v2 baseline |
|---|---:|---:|
| overall FULL | `306/435 = 70.34%` | `211/435 = 48.51%` |
| L2 FULL | `104/117 = 88.89%` | `46/117 = 39.32%` |
| hit@3 | `118/145 = 81.38%` | `104/145 = 71.72%` |
| hit@all | `84/145 = 57.93%` | `37/145 = 25.52%` |
| report K/N/I；precision | `721/444/106；91.66%` | `276/134/102；80.08%` |
| cluster K/N/I；precision | `689/419/100；91.72%` | `276/133/102；80.04%` |

v60 FULL-hit max W 为 `W2/W1/W0 = 211/95/0`，`W2/全部 expected = 219/435`。`627` 条 W2 evidence record 与 `627` 个 audit bundle 一一对应。实际 terminal predicate execution 为 `1,237` 次，其中 pass=`608`、violation=`629`；使用的计划谓词为 `12/15`。X1v2 的 512 条 finding 已由 Judge-blinded 两轮独立逐条回溯审计覆盖：finding-level `W0/W1/W2 = 1/511/0`，r1=`1/172/0`、r2=`0/163/0`、r3=`0/176/0`；FULL-hit max `W2/W1/W0 = 0/211/0`，L2 FULL-hit max `0/46/0`，`W2/全部 expected = 0/435`。两轮标签没有 W 级分歧，独立语义复核支持一条 W1->W0 的受限 post-review correction。X1v2 predicate usage 仍为 `not_applicable`，因为它没有同构的 19-predicate terminal receipt schema。

## 发现与裁定

- I：v60 Judge 的 `10` 个应计费调用缺 usage，`judge_cost_eligible=false`。报告保留 `$39.78176580` 为已记录成本，不把它写成完整精确总价。
- M：`l_tier.json` 与 archive 的完整 `ledger.json` 字节 hash 不同，但 L2 ID 集合相同。复算和报告只使用归档 hash 一致的 `ledger.json`。
- 无 C/I 级数值错误。

审查者初稿把 X1v2 selected-result Judge cost `$10.79275320` 汇总为 Judge 成本。主 session 回到 [baseline composite](../raw/x1v2_baseline/judge/composite-summary.json) 裁定：正式成本须报告 `total_incurred_cost_usd=$11.45008520`，并单列 selected result cost `$10.79275320` 与原始失败成本 `$0.65733200`。最终报告采用此裁定。

## 交班前独立复核

当前 pane5 session 另行组织只读复算，不读取报告汇总，不调用 provider，也不修改实验制品。复核再次运行归档 `validate`，并以 composite-selected `PairJudgeResult`、expected-witness、method/cost audit、ledger 和 registry JSON 交叉检查。v60 与 X1v2 的 hit、L2、hit@3、hit@all、K/N/I、cluster、W、predicate usage、cost eligibility 和 S2 paired comparison 三分法均与本记录和 `derived/recomputed_summary.json` 一致；未发现新的事实错误。
