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
