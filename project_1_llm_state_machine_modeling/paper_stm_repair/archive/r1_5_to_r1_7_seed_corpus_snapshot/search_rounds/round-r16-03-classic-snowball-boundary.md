# round-r16-03-classic-snowball-boundary

| 字段 | 内容 |
|---|---|
| 日期 | 2026-06-14 |
| source | subagent snowballing / Crossref / DBLP / OpenAlex / DOI |
| 操作者 | classic/use-case/scenario subagents + main session 复核 |
| 目的 | 从 use-case/statechart/scenario/completion 经典方向补充候选，同时强化 negative evidence。 |

## 候选处理

| ID | 结论 |
|---|---|
| `completion-sysml-gwt` | 本地 PDF/全文已复制并建目录；`X_REPAIR_ONLY` confirmed，不计 strict seed。 |
| `towards-automatic-model-completion` | GWT / completion 近邻，arXiv/PDF 线索；当前保持 completion boundary。 |
| `automated-transition-use-cases-uml-sm` | use case -> UML state machine 经典线索，DOI `10.1007/978-3-642-21470-7_9`；manual queue。 |
| `from-use-cases-to-statecharts` | R1.5 已有；`SS-B / SA-3`，paper-only。 |
| `execution-nl-req-bt-sm` | 年份校正为 2012，JSS DOI `10.1016/j.jss.2012.06.013`；BT intermediate + closed artifact，不计。 |
| `generating-statechart-designs-from-scenarios` | 输入为 sequence/scenario diagrams，`X_SEQUENCE_CLASS`。 |
| `requirements-analysis-prototyping-scenarios-statecharts` | 更像 statechart->scenario/prototype 或 co-evolution；不计。 |
| `synthesis-revisited-scenario-based` | LSC/MSC formal scenario，年份校正为 2005，DOI `10.1007/978-3-540-31847-7_18`；不计。 |
| `maritaca-use-case-behavior-models` | classic strong title/abstract；closed IEEE，无 artifact；manual queue。 |
| `dependable-product-families-usecases-state-machines` | classic strong title/abstract；closed IEEE，无 artifact；manual queue。 |
| `semi-auto-efsm-standard-docs` | standard/protocol risk；manual queue / sentinel。 |

## negative evidence 贡献

本轮说明：大量 classic statechart / scenario / completion 工作虽题名接近，但通常在 P1、P3 或 SA 上失败；因此 R1.6 不应为凑四例放宽 hard gate。

## 可复查字段表

| 字段 | 记录 |
|---|---|
| `round_id` | `r16-03-classic-snowball-boundary` |
| source | Crossref / DBLP / OpenAlex / DOI / subagent snowballing |
| query / query cluster | use-case -> statechart / UML state machine、scenario -> statechart、GWT / completion、standard document -> EFSM 等 classic / boundary query。 |
| top-k / page cap | 12 candidates |
| raw hit count | 12 |
| dedup count | 12 |
| entered candidate_matrix IDs | `completion-sysml-gwt`、`towards-automatic-model-completion`、`automated-transition-use-cases-uml-sm`、`execution-nl-req-bt-sm`、`generating-statechart-designs-from-scenarios`、`requirements-analysis-prototyping-scenarios-statecharts`、`synthesis-revisited-scenario-based`、`maritaca-use-case-behavior-models`、`dependable-product-families-usecases-state-machines`、`semi-auto-efsm-standard-docs` 等 |
| entered fulltext / artifact IDs | `completion-sysml-gwt`；同时复核 R1.5 已有 `from-use-cases-to-statecharts` / `scenarios-statecharts-interrelated` 等目录。 |
| excluded IDs + exclusion code | `completion-sysml-gwt` -> `X_REPAIR_ONLY`；`generating-statechart-designs-from-scenarios` -> `X_SEQUENCE_CLASS`；`synthesis-revisited-scenario-based` -> `X_FORMAL_SPEC` / `X_SEQUENCE_CLASS`；`requirements-analysis-prototyping-scenarios-statecharts` -> `X_NO_GEN_REL?`；`semi-auto-efsm-standard-docs` -> `CONTROL_STANDARD_EXCEPTION_PENDING` before reviewer. |
| pending / still-blocked | `automated-transition-use-cases-uml-sm`、`execution-nl-req-bt-sm`、`maritaca-use-case-behavior-models`、`dependable-product-families-usecases-state-machines`、`semi-auto-efsm-standard-docs` 等仍需人工 / 机构访问；但均不得在未全文核验前计主 seed。 |
| snowballing_parent_id | `from-use-cases-to-statecharts`、`beyond-scenarios-state-models`、`completion-sysml-gwt`、`execution-nl-req-bt-sm`、`automated-transition-use-cases-uml-sm` |
| noise pattern | classic statechart / scenario / completion 工作常在 P1（输入非 NL）、P3（不是初始生成）或 SA（paper-only / closed）失败。 |
| 下一步 | 保留 manual queue 与 sentinel，PR-R2 只从 `seed_selection_candidates.md` 裁决主 / 条件主候选，不因 classic 题名相近而放宽 hard gate。 |
