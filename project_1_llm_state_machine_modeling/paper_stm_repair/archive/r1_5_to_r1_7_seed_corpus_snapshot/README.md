# R1.5--R1.7 seed_corpus 历史快照

## 0. 定位

本目录是 PR-R1.8-B 从旧 `seed_corpus/` 迁移出来的历史审计快照，只用于追溯 R1.5--R1.7 的旧横向 ledger、检索轮次与 raw search results。**当前 seed library 的横向事实真源不是本目录，而是 [../../corpora/seed_library/SUMMARY.md](../../corpora/seed_library/SUMMARY.md)。**

## 1. 内容结构

| 路径 | 内容 | 使用方式 |
|---|---|---|
| [legacy_ledgers/](./legacy_ledgers/) | 旧 `candidate_matrix.md`、`screening_ledger.md`、`exclusion_ledger.md`、`manual_download_queue.md`、`baseline_seed_method_crosswalk.md`、`seed_selection_candidates.md`、旧 `SUMMARY/GUIDE` 与文献审计 provenance。 | 只作审计；当前横向统计以 seed library SUMMARY 为准。 |
| [search_rounds/](./search_rounds/) | R1.6 / R1.7 每轮检索 markdown 记录。 | 解释 search coverage 与 negative evidence。 |
| [search_results/](./search_results/) | OpenAlex / Crossref / arXiv / Semantic Scholar 等 raw JSONL。 | 原始检索证据，不直接作为当前事实。 |

## 2. 历史链接说明

archive 内文件按历史快照保留，部分相对链接仍可能指向迁移前的 `papers/`、`candidate_matrix.md`、`manual_download_queue.md` 等路径。需要当前可点击事实时，请回到：

- 当前 seed library 入口：[../../corpora/seed_library/README.md](../../corpora/seed_library/README.md)
- 当前 seed library 总账：[../../corpora/seed_library/SUMMARY.md](../../corpora/seed_library/SUMMARY.md)
- 当前单条目目录：[../../corpora/seed_library/](../../corpora/seed_library/)

## 3. 迁移哨兵

| 哨兵 | 当前状态 |
|---|---|
| 候选 / screening | `47/47`，见当前 [SUMMARY.md](../../corpora/seed_library/SUMMARY.md) §2 / §5。 |
| 单条目目录 | R1.7 历史快照口径为 24 个单篇目录；post-R1.8-B 当前口径为 36 个单条目证据目录，见当前 [SUMMARY.md](../../corpora/seed_library/SUMMARY.md) §2 / §8。 |
| 旧九 crosswalk | `9/9`，见当前 [SUMMARY.md](../../corpora/seed_library/SUMMARY.md) §7.1。 |
| R2 handoff | 4 个主 / 条件主候选，见当前 [SUMMARY.md](../../corpora/seed_library/SUMMARY.md) §4 / §6。 |
| manual queue | `2 downloaded/excluded；2 excluded-by-metadata；10 still-blocked；2 new-manual-pending`，见当前 [SUMMARY.md](../../corpora/seed_library/SUMMARY.md) §8。 |

## 4. 更新日志

| 时间 | 更新内容 |
|---|---|
| 2026-06-14 17:55:00 | PR-R1.8-B 创建 archive 快照，归档旧横向 ledger、search rounds 和 raw search results。 |
