> **Cold archive / deprecated historical snapshot.** 本目录保存旧 R1.6/R1.7 检索轮次记录，只用于追溯 search coverage、query strategy 和 negative evidence；不得作为当前 seed / baseline / eligibility 事实源。

# search_rounds/ — 历史检索轮次入口

## 0. 归档来源与时间考据

| 字段 | 值 |
|---|---|
| 原始来源路径 | `project_1_llm_state_machine_modeling/paper_stm_repair/seed_corpus/search_rounds/` |
| 当前归档路径 | `archive/r1_5_to_r1_7_seed_corpus_snapshot/search_rounds/` |
| 目录时间口径 | README 为 R5.5.1 重新生成的目录索引；各 round 文件的 freeze commit 见各自头部。 |
| 迁入 archive commit | `928933dd3bf941aa2e5f39c43dca7c4c33f04500` — 2026-06-14 18:14:27 +0800 — docs(paper1-r1.8-b): 重构seed文库三件套 |
| 当前事实源替代入口 | [../../../corpora/seed_library/SUMMARY.md](../../../corpora/seed_library/SUMMARY.md)、[../../../corpora/repair_baselines/SUMMARY.md](../../../corpora/repair_baselines/SUMMARY.md)、[../../../corpora/nl_datasets/SUMMARY.md](../../../corpora/nl_datasets/SUMMARY.md)、[../../../reports/SUMMARY.md](../../../reports/SUMMARY.md) |

## 1. 文件清单

| 文件 | 原用途 | 当前使用方式 |
|---|---|---|
| [2026-06-14-04-37-38-round-r16-01-crossref-refined.md](./2026-06-14-04-37-38-round-r16-01-crossref-refined.md) | R1.6/R1.7 检索轮次记录。 | 只作 search coverage / query history / negative evidence 背景。 |
| [2026-06-14-04-37-38-round-r16-02-llm-recent-artifact.md](./2026-06-14-04-37-38-round-r16-02-llm-recent-artifact.md) | R1.6/R1.7 检索轮次记录。 | 只作 search coverage / query history / negative evidence 背景。 |
| [2026-06-14-04-37-38-round-r16-03-classic-snowball-boundary.md](./2026-06-14-04-37-38-round-r16-03-classic-snowball-boundary.md) | R1.6/R1.7 检索轮次记录。 | 只作 search coverage / query history / negative evidence 背景。 |
| [2026-06-14-06-18-24-round-r17-01-openalex-broad-nl-requirements.md](./2026-06-14-06-18-24-round-r17-01-openalex-broad-nl-requirements.md) | R1.6/R1.7 检索轮次记录。 | 只作 search coverage / query history / negative evidence 背景。 |
| [2026-06-14-06-18-24-round-r17-02-crossref-refined-usecase-statechart.md](./2026-06-14-06-18-24-round-r17-02-crossref-refined-usecase-statechart.md) | R1.6/R1.7 检索轮次记录。 | 只作 search coverage / query history / negative evidence 背景。 |
| [2026-06-14-06-18-24-round-r17-03-crossref-textual-usecase-behavior.md](./2026-06-14-06-18-24-round-r17-03-crossref-textual-usecase-behavior.md) | R1.6/R1.7 检索轮次记录。 | 只作 search coverage / query history / negative evidence 背景。 |
| [2026-06-14-06-18-24-round-r17-04-arxiv-llm-requirements.md](./2026-06-14-06-18-24-round-r17-04-arxiv-llm-requirements.md) | R1.6/R1.7 检索轮次记录。 | 只作 search coverage / query history / negative evidence 背景。 |
| [2026-06-14-06-18-24-round-r17-05-semanticscholar-blocker.md](./2026-06-14-06-18-24-round-r17-05-semanticscholar-blocker.md) | R1.6/R1.7 检索轮次记录。 | 只作 search coverage / query history / negative evidence 背景。 |
| [2026-06-14-06-18-24-round-r17-06-dblp-exact-title.md](./2026-06-14-06-18-24-round-r17-06-dblp-exact-title.md) | R1.6/R1.7 检索轮次记录。 | 只作 search coverage / query history / negative evidence 背景。 |
| [2026-06-14-06-18-24-round-r17-07-classic-fulltext-wave.md](./2026-06-14-06-18-24-round-r17-07-classic-fulltext-wave.md) | R1.6/R1.7 检索轮次记录。 | 只作 search coverage / query history / negative evidence 背景。 |
| [2026-06-14-06-18-24-round-r17-08-manual-queue-artifact-recheck.md](./2026-06-14-06-18-24-round-r17-08-manual-queue-artifact-recheck.md) | R1.6/R1.7 检索轮次记录。 | 只作 search coverage / query history / negative evidence 背景。 |

## 2. 读取纪律

1. 每个 round 文件开头均记录原始路径、时间前缀依据 commit 和迁入 archive commit。
2. round 文件中的旧统计只代表当轮检索，不代表当前 seed library 总账。
3. 若要判断当前条目状态，必须回到 [../../../corpora/seed_library/SUMMARY.md](../../../corpora/seed_library/SUMMARY.md)。
4. 若要判断 R5/R5.5 主 seed 池，应读 [../../../reports/SUMMARY.md](../../../reports/SUMMARY.md)。
