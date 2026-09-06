> **Cold archive / deprecated historical snapshot.** 本目录已经脱离当前 R5.5+ 主线，只用于追溯 R1.5--R1.7 旧 `seed_corpus/` 的历史证据链；不得作为当前 seed、baseline、eligibility 或主实验事实源。当前事实请回到 [../../corpora/seed_library/SUMMARY.md](../../corpora/seed_library/SUMMARY.md)、[../../corpora/repair_baselines/SUMMARY.md](../../corpora/repair_baselines/SUMMARY.md)、[../../corpora/nl_datasets/SUMMARY.md](../../corpora/nl_datasets/SUMMARY.md) 与 [../../reports/SUMMARY.md](../../reports/SUMMARY.md)。

# R1.5--R1.7 seed_corpus 历史快照

## 0. 归档来源与时间考据

| 字段 | 值 |
|---|---|
| 原始来源路径 | `project_1_llm_state_machine_modeling/paper_stm_repair/seed_corpus/` |
| 当前归档路径 | `archive/r1_5_to_r1_7_seed_corpus_snapshot/` |
| 迁入 archive commit | `928933dd3bf941aa2e5f39c43dca7c4c33f04500` — 2026-06-14 18:14:27 +0800 — docs(paper1-r1.8-b): 重构seed文库三件套 |
| archive 哨兵校准 commit | `ceec28053349d68c13968dd69bb4ca70774317b0` — 2026-06-16 23:39:55 +0800 — docs(paper1-r1.8): 校准历史archive目录哨兵口径 |
| 当前事实源替代入口 | [../../corpora/seed_library/SUMMARY.md](../../corpora/seed_library/SUMMARY.md)、[../../corpora/repair_baselines/SUMMARY.md](../../corpora/repair_baselines/SUMMARY.md)、[../../corpora/nl_datasets/SUMMARY.md](../../corpora/nl_datasets/SUMMARY.md)、[../../reports/SUMMARY.md](../../reports/SUMMARY.md) |

## 1. 定位

本目录是 PR-R1.8-B 从旧 `seed_corpus/` 迁移出来的历史审计快照，只用于追溯 R1.5--R1.7 的旧横向 ledger、检索轮次与 raw search results。**当前 seed library 的横向事实真源不是本目录，而是 [../../corpora/seed_library/SUMMARY.md](../../corpora/seed_library/SUMMARY.md)。**

## 2. 内容结构

| 路径 | 内容 | 使用方式 |
|---|---|---|
| [legacy_ledgers/](./legacy_ledgers/) | 旧 `candidate_matrix`、`screening_ledger`、`exclusion_ledger`、`manual_download_queue`、`baseline_seed_method_crosswalk`、`seed_selection_candidates`、旧 `SUMMARY/GUIDE` 与文献审计 provenance；文件已按原始 freeze commit 秒级时间前缀重命名。 | 只作审计；当前横向统计以 seed library SUMMARY 为准。 |
| [search_rounds/](./search_rounds/) | R1.6 / R1.7 每轮检索 markdown 记录；非 README 文件已按原始 freeze commit 秒级时间前缀重命名。 | 解释 search coverage 与 negative evidence。 |
| [search_results/](./search_results/) | OpenAlex / Crossref / arXiv / Semantic Scholar 等 raw JSONL。 | 原始检索证据，不直接作为当前事实。 |

## 3. legacy ledger 清单

| 文件 | 使用方式 |
|---|---|
| [2026-06-14-06-18-24-exclusion-ledger.md](./legacy_ledgers/2026-06-14-06-18-24-exclusion-ledger.md) | 旧 seed_corpus ledger / 历史台账；只作审计追溯。 |
| [2026-06-14-06-18-24-manual-download-queue.md](./legacy_ledgers/2026-06-14-06-18-24-manual-download-queue.md) | 旧 seed_corpus ledger / 历史台账；只作审计追溯。 |
| [2026-06-14-06-18-24-search-log.md](./legacy_ledgers/2026-06-14-06-18-24-search-log.md) | 旧 seed_corpus ledger / 历史台账；只作审计追溯。 |
| [2026-06-14-11-18-35-baseline-seed-method-crosswalk.md](./legacy_ledgers/2026-06-14-11-18-35-baseline-seed-method-crosswalk.md) | 旧 seed_corpus ledger / 历史台账；只作审计追溯。 |
| [2026-06-14-11-18-35-candidate-matrix.md](./legacy_ledgers/2026-06-14-11-18-35-candidate-matrix.md) | 旧 seed_corpus ledger / 历史台账；只作审计追溯。 |
| [2026-06-14-11-18-35-screening-ledger.md](./legacy_ledgers/2026-06-14-11-18-35-screening-ledger.md) | 旧 seed_corpus ledger / 历史台账；只作审计追溯。 |
| [2026-06-14-11-18-35-seed-selection-candidates.md](./legacy_ledgers/2026-06-14-11-18-35-seed-selection-candidates.md) | 旧 seed_corpus ledger / 历史台账；只作审计追溯。 |
| [2026-06-14-15-49-35-agent-provenance.md](./legacy_ledgers/2026-06-14-15-49-35-agent-provenance.md) | 旧 seed_corpus ledger / 历史台账；只作审计追溯。 |
| [2026-06-14-15-49-35-seed-corpus-guide.md](./legacy_ledgers/2026-06-14-15-49-35-seed-corpus-guide.md) | 旧 seed_corpus ledger / 历史台账；只作审计追溯。 |
| [2026-06-14-15-49-35-seed-corpus-summary.md](./legacy_ledgers/2026-06-14-15-49-35-seed-corpus-summary.md) | 旧 seed_corpus ledger / 历史台账；只作审计追溯。 |

## 4. search round 清单

| 文件 | 使用方式 |
|---|---|
| [2026-06-14-04-37-38-round-r16-01-crossref-refined.md](./search_rounds/2026-06-14-04-37-38-round-r16-01-crossref-refined.md) | 旧检索轮次记录；只作 search coverage / negative evidence 背景。 |
| [2026-06-14-04-37-38-round-r16-02-llm-recent-artifact.md](./search_rounds/2026-06-14-04-37-38-round-r16-02-llm-recent-artifact.md) | 旧检索轮次记录；只作 search coverage / negative evidence 背景。 |
| [2026-06-14-04-37-38-round-r16-03-classic-snowball-boundary.md](./search_rounds/2026-06-14-04-37-38-round-r16-03-classic-snowball-boundary.md) | 旧检索轮次记录；只作 search coverage / negative evidence 背景。 |
| [2026-06-14-06-18-24-round-r17-01-openalex-broad-nl-requirements.md](./search_rounds/2026-06-14-06-18-24-round-r17-01-openalex-broad-nl-requirements.md) | 旧检索轮次记录；只作 search coverage / negative evidence 背景。 |
| [2026-06-14-06-18-24-round-r17-02-crossref-refined-usecase-statechart.md](./search_rounds/2026-06-14-06-18-24-round-r17-02-crossref-refined-usecase-statechart.md) | 旧检索轮次记录；只作 search coverage / negative evidence 背景。 |
| [2026-06-14-06-18-24-round-r17-03-crossref-textual-usecase-behavior.md](./search_rounds/2026-06-14-06-18-24-round-r17-03-crossref-textual-usecase-behavior.md) | 旧检索轮次记录；只作 search coverage / negative evidence 背景。 |
| [2026-06-14-06-18-24-round-r17-04-arxiv-llm-requirements.md](./search_rounds/2026-06-14-06-18-24-round-r17-04-arxiv-llm-requirements.md) | 旧检索轮次记录；只作 search coverage / negative evidence 背景。 |
| [2026-06-14-06-18-24-round-r17-05-semanticscholar-blocker.md](./search_rounds/2026-06-14-06-18-24-round-r17-05-semanticscholar-blocker.md) | 旧检索轮次记录；只作 search coverage / negative evidence 背景。 |
| [2026-06-14-06-18-24-round-r17-06-dblp-exact-title.md](./search_rounds/2026-06-14-06-18-24-round-r17-06-dblp-exact-title.md) | 旧检索轮次记录；只作 search coverage / negative evidence 背景。 |
| [2026-06-14-06-18-24-round-r17-07-classic-fulltext-wave.md](./search_rounds/2026-06-14-06-18-24-round-r17-07-classic-fulltext-wave.md) | 旧检索轮次记录；只作 search coverage / negative evidence 背景。 |
| [2026-06-14-06-18-24-round-r17-08-manual-queue-artifact-recheck.md](./search_rounds/2026-06-14-06-18-24-round-r17-08-manual-queue-artifact-recheck.md) | 旧检索轮次记录；只作 search coverage / negative evidence 背景。 |

## 5. 历史链接说明

archive 内文件按历史快照保留，部分正文中的旧相对链接仍可能指向迁移前的 `papers/`、`candidate_matrix.md`、`manual_download_queue.md` 等路径。需要当前可点击事实时，请回到：

- 当前 seed library 入口：[../../corpora/seed_library/README.md](../../corpora/seed_library/README.md)
- 当前 seed library 总账：[../../corpora/seed_library/SUMMARY.md](../../corpora/seed_library/SUMMARY.md)
- 当前单条目目录：[../../corpora/seed_library/](../../corpora/seed_library/)

## 6. 迁移哨兵

| 哨兵 | 当前状态 |
|---|---|
| 候选 / screening | `47/47`，见当前 [SUMMARY.md](../../corpora/seed_library/SUMMARY.md) §2 / §5。 |
| 单条目目录 | R1.7 历史快照口径为 24 个单篇目录；post-R1.8-B 当前口径为 36 个单条目证据目录，见当前 [SUMMARY.md](../../corpora/seed_library/SUMMARY.md) §2 / §8。 |
| 旧九 crosswalk | `9/9`，见当前 [SUMMARY.md](../../corpora/seed_library/SUMMARY.md) §7.1。 |
| R2 handoff | 4 个主 / 条件主候选，见当前 [SUMMARY.md](../../corpora/seed_library/SUMMARY.md) §4 / §6。 |
| manual queue | `2 downloaded/excluded；2 excluded-by-metadata；10 still-blocked；2 new-manual-pending`，见当前 [SUMMARY.md](../../corpora/seed_library/SUMMARY.md) §8。 |

## 7. 更新日志

| 时间 | 更新内容 |
|---|---|
| 2026-06-29 03:12:00 | R5.5.1 加固 archive cold/deprecated 标记、秒级文件名前缀与来源 commit 考据。 |
| 2026-06-14 17:55:00 | PR-R1.8-B 创建 archive 快照，归档旧横向 ledger、search rounds 和 raw search results。 |
