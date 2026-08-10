> **Cold archive / deprecated historical snapshot.** 本文件已经脱离当前 R5.5+ 主线，只用于追溯 R1.5--R1.7 旧 seed_corpus 的历史证据链；不得作为当前 seed、baseline、eligibility 或主实验事实源。当前事实请回到 `paper_stm_repair/corpora/`、`paper_stm_repair/reports/` 与 `paper_stm_repair/pipeline/` 的对应入口。

## 归档来源与时间考据

| 字段 | 值 |
|---|---|
| 原始来源路径 | `project_1_llm_state_machine_modeling/paper_stm_repair/seed_corpus/search_rounds/2026-06-14-04-37-38-round-r16-02-llm-recent-artifact.md` |
| 当前归档路径 | `archive/r1_5_to_r1_7_seed_corpus_snapshot/search_rounds/2026-06-14-04-37-38-round-r16-02-llm-recent-artifact.md` |
| 时间前缀 / 内容冻结依据 | `9a4463cbd6e5ba46b89e796938d9ab0756bd3eb8` — 2026-06-14 04:37:38 +0800 — docs(paper1-r1.6): 完成strict seed扩展文库 |
| 迁入 archive commit | `928933dd3bf941aa2e5f39c43dca7c4c33f04500` — 2026-06-14 18:14:27 +0800 — docs(paper1-r1.8-b): 重构seed文库三件套 |
| 当前事实源替代入口 | [../../../corpora/seed_library/SUMMARY.md](../../../corpora/seed_library/SUMMARY.md)、[../../../corpora/repair_baselines/SUMMARY.md](../../../corpora/repair_baselines/SUMMARY.md)、[../../../corpora/nl_datasets/SUMMARY.md](../../../corpora/nl_datasets/SUMMARY.md)、[../../../reports/SUMMARY.md](../../../reports/SUMMARY.md) |

# round-r16-02-llm-recent-artifact

| 字段 | 内容 |
|---|---|
| 日期 | 2026-06-14 |
| source | arXiv / Zenodo / GitHub / IJISRT PDF / TechScience PDF / HuggingFace API |
| 操作者 | LLM/recent subagent + main session 复核 |
| 目的 | 查找 2025--2026 LLM 生成 FSM/state diagram 的 strict seed 与 artifact。 |

## 候选处理

| ID | 处理结论 |
|---|---|
| `sefm-llm-state-machine` | 已在 R1.5 本地目录；R1.6 修正年份为 2026。仍为强主候选。 |
| `fsm-bench-20` | Zenodo/GitHub/MIT/dataset/prompt/schema/code 可用；公开包没有 generated outputs / gold，暂不计四例。 |
| `fsm-gen-iec-61499` | 本地 baseline 已有 PDF/全文；控制系统相关性强但私有工具 / 数据 / 输出不可复验，`SA-4`。 |
| `ijisrt-uml-state-diagrams-llm` | PDF 可下载；任务关系清楚但 paper-only，`SA-3`。 |
| `unified-uml-multimodal-validation` | TechScience PDF + HF `UMLCode_StateDiagram` parquet 可下载，999 rows；`SS-B / SA-2` 条件候选。 |
| `umple-nl-state-machine` | R1.5 已有；仍是 `SS-A / SA-3`，不计主 seed。 |
| `designing-fsm-gpt4` | R1.5 已有；年份校正为 2026；仍为 initial-generation-only 条件候选。 |

## 本轮新增 artifact

- `fsm-bench-20/llm-fsm-local-benchmark-v1.0.0.zip` 与 metadata JSON。
- `ijisrt-uml-state-diagrams-llm/paper.pdf` / `paper_content.txt`。
- `unified-uml-multimodal-validation/paper.pdf` / `paper_content.txt` / HF API JSON / state parquet / sample JSON。

## 关键 caveat

- `SA-3` 不计主 seed；paper-only recent LLM 论文不能为四例凑数。
- `fsm-bench-20` 虽然 MIT 且 pipeline 很强，但缺 generated outputs；需要 PR-R2 复跑。
- HF dataset 的 license 未在 API card 中明确记录，PR-R2 必须保留 license caveat。

## 可复查字段表

| 字段 | 记录 |
|---|---|
| `round_id` | `r16-02-llm-recent-artifact` |
| source | arXiv / Zenodo / GitHub / IJISRT PDF / TechScience PDF / HuggingFace API |
| query / query cluster | recent LLM + `state machine` / `FSM` / `UML state diagram` / `requirements`；同时复查 R1.5 已有 LLM 候选。 |
| top-k / page cap | 10 candidates |
| raw hit count | 10 |
| dedup count | 10 |
| entered candidate_matrix IDs | `fsm-bench-20`、`fsm-gen-iec-61499`、`ijisrt-uml-state-diagrams-llm`、`unified-uml-multimodal-validation`，并复核 `sefm-llm-state-machine`、`umple-nl-state-machine`、`designing-fsm-gpt4` |
| entered fulltext / artifact IDs | `fsm-bench-20`、`fsm-gen-iec-61499`、`ijisrt-uml-state-diagrams-llm`、`unified-uml-multimodal-validation`，并沿用 R1.5 三个已有目录 |
| excluded IDs + exclusion code | 无新增 hard exclude；`ijisrt-*` 因 `SA-3` 不计主 seed，`fsm-gen-iec-61499` 因 `SA-4` 不计主 seed。 |
| pending / still-blocked | `fsm-bench-20` generated outputs / gold 未公开冻结；`unified-*` license 不清；`fsm-gen-*` 私有 tool/data/output。 |
| snowballing_parent_id | `sefm-llm-state-machine`、`designing-fsm-gpt4`、`umple-nl-state-machine`（recent LLM near-neighbor 扩展） |
| noise pattern | recent LLM state diagram 论文常为 paper-only / toy examples；artifact 可下载不等于 generated `STM_0` 已冻结。 |
| 下一步 | 将 `unified-*` 交 PR-R2 条件裁决；`fsm-bench-20` 只作 pipeline fallback / rerun candidate。 |
