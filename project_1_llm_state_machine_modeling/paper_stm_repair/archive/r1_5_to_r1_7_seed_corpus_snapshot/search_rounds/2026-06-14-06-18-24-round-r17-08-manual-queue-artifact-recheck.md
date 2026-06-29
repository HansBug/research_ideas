> **Cold archive / deprecated historical snapshot.** 本文件已经脱离当前 R5.5+ 主线，只用于追溯 R1.5--R1.7 旧 seed_corpus 的历史证据链；不得作为当前 seed、baseline、eligibility 或主实验事实源。当前事实请回到 `paper_stm_repair/corpora/`、`paper_stm_repair/reports/` 与 `paper_stm_repair/pipeline/` 的对应入口。

## 归档来源与时间考据

| 字段 | 值 |
|---|---|
| 原始来源路径 | `project_1_llm_state_machine_modeling/paper_stm_repair/seed_corpus/search_rounds/2026-06-14-06-18-24-round-r17-08-manual-queue-artifact-recheck.md` |
| 当前归档路径 | `archive/r1_5_to_r1_7_seed_corpus_snapshot/search_rounds/2026-06-14-06-18-24-round-r17-08-manual-queue-artifact-recheck.md` |
| 时间前缀 / 内容冻结依据 | `1ac506152b891e755971eb623717fa45f05da644` — 2026-06-14 06:18:24 +0800 — docs(paper1-r1.7): 完成广域strict seed文库扩展 |
| 迁入 archive commit | `928933dd3bf941aa2e5f39c43dca7c4c33f04500` — 2026-06-14 18:14:27 +0800 — docs(paper1-r1.8-b): 重构seed文库三件套 |
| 当前事实源替代入口 | [../../../corpora/seed_library/SUMMARY.md](../../../corpora/seed_library/SUMMARY.md)、[../../../corpora/repair_baselines/SUMMARY.md](../../../corpora/repair_baselines/SUMMARY.md)、[../../../corpora/nl_datasets/SUMMARY.md](../../../corpora/nl_datasets/SUMMARY.md)、[../../../reports/SUMMARY.md](../../../reports/SUMMARY.md) |

# round-r17-08-manual-queue-artifact-recheck

| 字段 | 内容 |
|---|---|
| 日期 | 2026-06-14 |
| source | publisher exact + artifact search |
| query / 入口 | R1.6 manual queue and R1.7 new manual candidates |
| raw evidence | `manual_download_queue.md; exclusion_ledger.md` |
| 原始命中 / 尝试 | 11 legacy + 2 new manual candidates checked |
| 操作者 | main session + scout/review subagents |

## 处理结果

Downloaded `towards-automatic-model-completion` from arXiv and excluded it as `X_REPAIR_ONLY`; kept 10 still-blocked legacy items; added two new manual pending items.

## 排除 / 噪声

Most legacy items remain paywalled or browser-only; artifact search found no public code/model package for classic closed candidates.

## blocker / 降级

若对应 source 受阻或只能提供 metadata，已在 raw JSONL、manual queue 或本 round 中保留。`paper-only`、`private-only`、`SA-3/SA-4/SA-5` 不进入主 seed 计数。

## 下一步

Manual queue now has status distribution and PR-R2 impact; closed items are not blockers for R2 if not used.

## 可复查字段表

| 字段 | 记录 |
|---|---|
| round_id | `round-r17-08-manual-queue-artifact-recheck` |
| source | publisher exact + artifact search |
| query / query cluster | R1.6 manual queue and R1.7 new manual candidates |
| top-k / page cap | 见 raw evidence；API dump 通常为 20--30，exact-title 以 DOI / title 为准。 |
| raw hit count | 11 legacy + 2 new manual candidates checked |
| entered candidate_matrix IDs | 见 [candidate_matrix.md](../legacy_ledgers/2026-06-14-11-18-35-candidate-matrix.md) 的 `R1.7` 批次行。 |
| entered fulltext / artifact IDs | 见 [papers/](../../../corpora/seed_library/) 新增 R1.7 单篇目录。 |
| excluded IDs + exclusion code | 见 [exclusion_ledger.md](../legacy_ledgers/2026-06-14-06-18-24-exclusion-ledger.md)。 |
| pending / still-blocked | 见 [manual_download_queue.md](../legacy_ledgers/2026-06-14-06-18-24-manual-download-queue.md) 状态分布。 |
| noise pattern | 见本文件“排除 / 噪声”。 |
| 下一步 | Manual queue now has status distribution and PR-R2 impact; closed items are not blockers for R2 if not used. |
