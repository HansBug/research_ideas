# STM Source Landscape Execution Plan

## 1. 本 PR 目标

1. 建立与 PR #96 同构的 paper workspace。
2. 落地 #95 -> #85 初筛矩阵与下载 handoff。
3. 明确后续 manuscript-start 前必须完成的 G0--G10 gate。

## 2. 后续 gate

| Gate | 目标 | 当前 PR 状态 |
|---|---|---|
| G0 | artifact / copyright boundary | 只提交 metadata/BibTeX/CSV，未完成最终 release |
| G1 | retrospective protocol audit | 未完成；本 PR 只建入口 |
| G2 | coding reliability audit | 未完成；本 PR 只建入口 |
| G3 | related-work 查重 | 本 PR 完成 metadata-level 初筛，待全文核验 |
| G4 | RQ-to-data / eligibility alignment | 未完成；需后续 eligibility rules |
| G5 | cross-paper boundary / anti-salami | story 中已标注，需 companion boundary 文档 |
| G6 | CCF-A survey / mapping bar | venue gate 已建，待 checklist |
| G7 | external usefulness / validation | 未完成 |
| G8 | negative / excluded sample audit | 本 PR 提供 Skip / excluded 起点，待正式 negative audit |
| G9 | benchmark-card pilot | 未完成 |
| G10 | LLM extraction baseline / contamination audit | 未完成 |

## 3. 四例真实运行判断

不需要运行四个真实 LLM 例子。本 PR 不涉及 agent-loop method、真实 LLM provider、Path-1/Path-2 runtime 或 `.env` 调用；它只新增文档、CSV、BibTeX 与 planning evidence。若后续 G10 需要 LLM extraction sensitivity，必须先 `source .env` 并产出 run record。
