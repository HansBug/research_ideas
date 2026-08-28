# v60/current 与 X1v2 baseline 最终结果归档

本目录是 Paper1 当前实验结果、复核和交班的唯一稳定入口。它保存 v60/current 与 X1v2 baseline 的冻结方法/Judge 制品、引用数据、离线派生汇总、正式中文报告、审查记录与 publication manifest。归档不包含 provider request/response stream、缓存、凭据、锁文件、`.part` 或 launcher 日志；保留的结构化 JSON 足以离线复算报告指标。

| 路径 | 内容 |
| --- | --- |
| `raw/v60_current/` | v60 method、Judge composite 与 composite-selected source runs |
| `raw/x1v2_baseline/` | 162 个 X1v2 method record、冻结 Judge composite、source runs 与 method-cost audit |
| `reference/` | 145 条 ledger、冻结 19-predicate registry、source catalog 与输入闭包引用 |
| `derived/recomputed_summary.json` | 从 raw/reference 和完整 X1v2 W audit 机械复算的主汇总 |
| `derived/x1v2_witness_level_audit.json` | 512 条 baseline finding 的两轮独立 W 审计与裁决记录 |
| `derived/x1v2_full_hit_max_witness_audit.json` | 435 条 expected row 的 FULL-only max-W 聚合 |
| `report/` | 当前 [中文正式报告](./report/v60_current_vs_x1v2_baseline_cn.md) |
| `reviews/` | 数值、语义、文风与审计审查记录 |
| `archive_manifest.json` 与 `publication_manifest.json` | 归档与发布面文件的 SHA-256 清单 |

字段、分母、适用范围和数据缺口见 [SCHEMA.md](./SCHEMA.md)。当前主宇宙为 54 pair、3 round、145 expected issue、435 round-level expected row；L2 为 39 expected、117 row。`FULL/PARTIAL/NONE` 是 expected relation，`VALID_KNOWN/VALID_NOVEL/INVALID` 是 report validity，只有 `INVALID` 进入 semantic FP。

## 当前比较

| 指标 | v60/current | X1v2 baseline |
| --- | ---: | ---: |
| overall FULL / hit@1 | 306/435 = 70.34% | 211/435 = 48.51% |
| L2 FULL / hit@1 | 104/117 = 88.89% | 46/117 = 39.32% |
| hit@3 | 118/145 = 81.38% | 104/145 = 71.72% |
| hit@all | 84/145 = 57.93% | 37/145 = 25.52% |
| report semantic precision | 1165/1271 = 91.66% | 410/512 = 80.08% |
| FULL-hit max-W2 / W1 / W0 | 211/95/0（分母 306） | 0/211/0（分母 211） |

W 不绑定 19 谓词。X1v2 的 predicate usage 因其没有同构 registry/receipt schema 而不适用；其 W 仍经 512 条冻结 finding 的双审回溯得到 W0/W1/W2 = 1/511/0。baseline 没有运行期 executable witness，因此没有 W2；Judge 的事后事实核验不会倒灌为 baseline method W2。

## 离线复算

从仓库根执行下列权威入口。命令只读取归档、不会调用 provider，也不依赖未跟踪 `runs/`：

```bash
PYTHONPATH=project_1_llm_state_machine_modeling/paper_stm_issue_discover/evaluation/src:project_1_llm_state_machine_modeling/paper_stm_issue_discover \
venv/bin/python -m paper_stm_evaluation.final_results_archive validate \
  --archive-root project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline
```

维护者在明确需要更新报告或 review 的 publication manifest 时可运行同一模块的 `finalize`，随后必须再次 `validate`。`pipeline.evidence_discovery.reporting.final_results_archive` 保留为兼容入口；它不是 archive 的正式所有者。

## 冻结引用与限制

v60 method commit 为 `66b5d71aecd73f6eeddac082037f7c34e04da057`，method run ID 为 `915d56e45a634c27aa03866f03818c6d`，Judge commit 为 `05cf0da6f7d9fcf1de26c349b586fc71c268f1c5`，协议为 `github-issue-195.d774d9bd3e4c.issue-189-clarification.v3.2`。registry、prompt/schema、input、run contract 与 Judge protocol 的完整 SHA-256 位于 manifests 和正式报告。

本结果只支持冻结 ledger、输入闭包、Judge、`gpt-5.6-luna` 和已声明 FCSTM/soundness fragment。历史 X1v2 `59.8%/70.3%/47.9%` 使用旧 Judge 与不同网格，已被当前 rejudge 替代；历史材料见 [实验历史索引](../../archive/experiment_history/README.md)。
