# 历史考据独立审查

审查范围：Git history、tags、提交 diff、正式报告、历史 manifest、`archive/experiment_history/README.md` 与 `historical_raw_inventory.json`。

## 复核方法

```bash
git log --all --follow -- project_1_llm_state_machine_modeling/paper_stm_issue_discover/archive/r10_ledger_v1_and_v46
git ls-tree -r -l b6ec2917f16104d3a8ac8b07c8a519dca2bfacf6 -- project_1_llm_state_machine_modeling/paper_stm_issue_discover/archive/r10_ledger_v1_and_v46
git log --all --follow -- project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline/derived/x1v2_witness_level_audit.json
```

v46 的 `ca41369e46c09eafe6bfbfe64c3754b02c6d8fee`、54x2x3、324/324、旧 99 ledger 与 `355/588`、`139/196`、`95/196` 同正式材料一致。v27-stream 的 `2accd7213bad43955314efc6daec8b74e614b03f`、145 ledger、54x3、`276/435`、`107/145`、`76/145`、`45.74%` 与旧 report 一致，且不可与 current Judge/K/N/I 混用。v60/current 与 current X1v2 的 anchors、主指标和 legacy method 缺少顶层 source commit 的限制均已正确保留。

| 严重度 | Finding | Evidence | 处理 |
| --- | --- | --- | --- |
| Medium | v46 inventory 将 `b6ec...` 历史 source commit 与当前 retained subset 的 157 files/3,566,243 bytes 混为同一树，并误称当前目录保存全部独有材料。 | `b6ec...` 有 478 files、15,909,573 bytes；当前 tracked subset 有 157 files、2,817,579 bytes；之间有 321 deletions。 | pending: 分开 source tree 与 current subset，并说明完整恢复只能由 named commit 完成。 |
| Medium | final archive inventory 锚定 `edf859...`，但该 commit 早于 X1v2 W audit。 | `edf...` 有 2366 archive files；`d31a8d171c08c2cc32650d0c08c4e8ac6b43818c` 已包含 W audit，archive tree 为 2671 files。 | pending: 用 `d31a8d171...` 作为覆盖完整 current archive 的 source commit。 |

v27 complete method raw 仅在未跟踪 `runs/`，不建立 ZIP 的结论合理。审查为只读，未读取该目录，provider 调用与 billable 调用均为 0。

结论：修复两项 provenance 记录后可作 targeted rereview。

## 2026-08-28 定向复审

复审确认 v46 inventory 已区分 `b6ec2917f16104d3a8ac8b07c8a519dca2bfacf6` 的 478-file historical source tree（15,909,573 bytes）和当前 157-file retained subset（2,817,579 bytes），并明确完整恢复只能从该 commit 进行。v60/X1v2 archive anchor 已改为包含 W audit 的 `d31a8d171c08c2cc32650d0c08c4e8ac6b43818c`；v27 complete raw 仍只存在于未跟踪 `runs/`，没有被虚构为 ZIP。

结论：通过。无剩余高/中严重度 finding；未修改文件，provider 与 billable 调用均为 0。
