# 数字与实验事实独立审查

审查范围：`derived/recomputed_summary.json`、两臂 Judge composite、v60 method manifest、X1v2 W audit、正式报告、archive/publication manifest，以及 current README、STATUS、story、evaluation、ledger 文档。

## 复核方法

```bash
jq '.' final_results/v60_current_vs_x1v2_baseline/derived/recomputed_summary.json
PYTHONPATH=project_1_llm_state_machine_modeling/paper_stm_issue_discover/evaluation/src:project_1_llm_state_machine_modeling/paper_stm_issue_discover \
venv/bin/python -m paper_stm_evaluation.final_results_archive validate \
  --archive-root project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline
```

## 结果

下列事实与冻结 JSON、raw composite 和正式报告一致：54 pair、3 round、145 expected、435 row；v60 的 `306/435`、`104/117`、`118/145`、`84/145`、`1165/1271`；X1v2 的 `211/435`、`46/117`、`104/145`、`37/145`、`410/512`；v60 report K/N/I 为 `721/444/106`，X1v2 为 `276/134/102`；v60 FULL-hit W2/W1/W0 为 `211/95/0`，X1v2 finding-level W0/W1/W2 为 `1/511/0`、FULL-hit 为 `0/211/0`；v60 planned terminal predicate usage 为 `12/15`，X1v2 不适用。method、run、Judge、registry、prompt/schema、input、run contract 与 protocol anchors 同 manifest 一致。

| 严重度 | Finding | Evidence | 处理 |
| --- | --- | --- | --- |
| High | 最终归档 README 已修改，但 `archive_manifest.json` 与 `publication_manifest.json` 仍登记旧 README hash，权威 validator 失败。 | README 当前为 `3957` bytes、`sha256:f8ffc1...0715ad`；manifest 仍为 `5043` bytes、`sha256:46c9f3...f7db0`。 | pending: 仅用权威 `finalize` 重建两个 manifest，并对 raw/derived/reference 做基线对拍。 |

未发现 legacy X1v2 `59.8%/70.3%/47.9%` 被写成 current 结果。审查为只读；provider 调用与 billable 调用均为 0。

结论：除受控 manifest 更新外，数字与实验事实通过。

## 2026-08-28 定向复审

`finalize` 已仅更新 final archive 的 README、`archive_manifest.json` 与 `publication_manifest.json`。复审再次运行 authoritative archive validator 和 release structure validator，确认 README 为 `3957` bytes、`sha256:f8ffc1...0715ad`，两个 manifest 一致；`raw/`、`derived/`、`reference/` 共 2655 项相对 baseline 零 mismatch，2671 个 archive 文件均已校验。

结论：通过。无剩余高/中严重度 finding；465/465 historical pytest node、资源 hash 与 import boundary 均保持有效，provider 与 billable 调用均为 0。
