> **Cold archive / deprecated historical snapshot.** 本文件已经脱离当前 R5.5+ 主线，只用于追溯 R1.5--R1.7 旧 seed_corpus 的历史证据链；不得作为当前 seed、baseline、eligibility 或主实验事实源。当前事实请回到 `paper_stm_repair/corpora/`、`paper_stm_repair/reports/` 与 `paper_stm_repair/pipeline/` 的对应入口。

## 归档来源与时间考据

| 字段 | 值 |
|---|---|
| 原始来源路径 | `project_1_llm_state_machine_modeling/paper_stm_repair/seed_corpus/search_rounds/2026-06-14-04-37-38-round-r16-01-crossref-refined.md` |
| 当前归档路径 | `archive/r1_5_to_r1_7_seed_corpus_snapshot/search_rounds/2026-06-14-04-37-38-round-r16-01-crossref-refined.md` |
| 时间前缀 / 内容冻结依据 | `9a4463cbd6e5ba46b89e796938d9ab0756bd3eb8` — 2026-06-14 04:37:38 +0800 — docs(paper1-r1.6): 完成strict seed扩展文库 |
| 迁入 archive commit | `928933dd3bf941aa2e5f39c43dca7c4c33f04500` — 2026-06-14 18:14:27 +0800 — docs(paper1-r1.8-b): 重构seed文库三件套 |
| 当前事实源替代入口 | [../../../corpora/seed_library/SUMMARY.md](../../../corpora/seed_library/SUMMARY.md)、[../../../corpora/repair_baselines/SUMMARY.md](../../../corpora/repair_baselines/SUMMARY.md)、[../../../corpora/nl_datasets/SUMMARY.md](../../../corpora/nl_datasets/SUMMARY.md)、[../../../reports/SUMMARY.md](../../../reports/SUMMARY.md) |

# round-r16-01-crossref-refined

| 字段 | 内容 |
|---|---|
| 日期 | 2026-06-14 |
| source | Crossref API + DOI landing page |
| 操作者 | main session |
| 目的 | 用 exact / refined title query 补 PR-R1.5 宽 query 噪声，定位 classic use-case / UML state diagram / statechart extraction 候选。 |

## Query 与结果摘要

| query | top hits / 处理 |
|---|---|
| `MARITACA From Textual Use Case Descriptions to Behavior Models` | 命中 `MARITACA: From Textual Use Case Descriptions to Behavior Models`，DOI `10.1109/DSN-W.2017.33`；进入 manual queue。 |
| `Modeling Dependable Product-Families From Use Cases to State Machine Models` | 命中 DOI `10.1109/LADC.2016.28`；进入 manual queue。 |
| `A Comparison of LLMs for UML State Diagrams Generation` | 命中 DOI `10.38124/ijisrt/26feb1435`；PDF 可下载，已建单篇目录。 |
| `A Novel Unified Framework for Automated Generation and Multimodal Validation of UML Diagrams` | 命中 DOI `10.32604/cmes.2025.075442`；TechScience PDF 与 HF state subset 可用，已建单篇目录。 |
| `Rscharter Framework Extracting Statechart Diagram Elements Requirements Specification` | 命中 SSRN DOI `10.2139/ssrn.4964857`；待人工全文。 |

## 去重 / 纳入 / 排除

- 新增候选：`maritaca-use-case-behavior-models`、`dependable-product-families-usecases-state-machines`、`ijisrt-uml-state-diagrams-llm`、`unified-uml-multimodal-validation`、`rscharter-statechart-elements`。
- 排除：无直接排除；但 MARITACA / product-family 当前均为 closed/paper pending，不计主 seed。
- 早停理由：Crossref exact title 已足够定位 DOI；全文和 artifact 由后续 source-specific 核验处理。

## 噪声经验

- exact title / exact phrase 比 PR-R1.5 的 broad OpenAlex query 更有效。
- 但 Crossref 只能提供 metadata，不能替代 fulltext / artifact judgement。

## 可复查字段表

| 字段 | 记录 |
|---|---|
| `round_id` | `r16-01-crossref-refined` |
| source | Crossref API + DOI landing page |
| query / query cluster | 5 个 exact title / refined title query：MARITACA、Dependable Product-Families、IJISRT UML State Diagrams、Unified UML Multimodal Validation、Rscharter |
| top-k / page cap | 每个 exact query 取 top DOI 命中；总 cap 约 15 raw hits |
| raw hit count | 15 |
| dedup count | 5 |
| entered candidate_matrix IDs | `maritaca-use-case-behavior-models`、`dependable-product-families-usecases-state-machines`、`ijisrt-uml-state-diagrams-llm`、`unified-uml-multimodal-validation`、`rscharter-statechart-elements` |
| entered fulltext / artifact IDs | `ijisrt-uml-state-diagrams-llm`、`unified-uml-multimodal-validation` |
| excluded IDs + exclusion code | 本轮无直接 hard exclude；`maritaca-*` / `dependable-*` / `rscharter-*` 均保持 pending / manual。 |
| pending / still-blocked | `maritaca-use-case-behavior-models`、`dependable-product-families-usecases-state-machines`、`rscharter-statechart-elements` 需要人工 / 机构访问或 SSRN 全文。 |
| snowballing_parent_id | N/A；本轮是 exact refined DOI search。 |
| noise pattern | exact title 比 broad OpenAlex 噪声低，但 Crossref metadata 不能替代全文或 artifact 判断。 |
| 下一步 | 已下载可访问 PDF / HF artifact；closed / SSRN 项进入 manual queue。 |
