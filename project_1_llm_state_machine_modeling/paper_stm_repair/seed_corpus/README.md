# PR-R1.7 strict seed 文献文库

本目录是第一篇论文新主线 `paper_stm_repair` 下的专属 seed 文库，服务于后续 `<NL, STM_0> -> STM_k / Better STM` 任务的样本构造、四例冻结、转换器压力分析和相关工作定位。

## 定位

- **本目录做什么**：系统检索、筛查、全文阅读并编码可能满足 `NL -> T0 FSM/HSM/EFSM/statechart` 生成关系的文献 / artifact，形成可审计的 seed 候选池。
- **本目录不做什么**：不冻结最终四例样本，不实现转换器，不跑真实 LLM，不证明修正 loop 有效。
- **与上游的关系**：继承 [../evidence/strict_seed_literature_survey.md](../evidence/strict_seed_literature_survey.md) 的 strict seed 定义、排除码、SS/SA 双轴分级。
- **与下游的关系**：向 PR-R2 提供可复查候选；PR-R2 再冻结同一组 `>=4` 四例样本。R1.7 当前只声称 bounded snapshot v3，不声称全域 census。

## 使用顺序

1. 先读本 [README.md](./README.md) 理解文库边界。
2. 再读 [GUIDE.md](./GUIDE.md) 执行检索、筛查、下载、全文阅读与编码。
3. 用 [SUMMARY.md](./SUMMARY.md) 查看当前统计、候选列表、风险和下一步。
4. 查 [candidate_matrix.md](./candidate_matrix.md)、[screening_ledger.md](./screening_ledger.md)、[exclusion_ledger.md](./exclusion_ledger.md)、[manual_download_queue.md](./manual_download_queue.md)、[search_log.md](./search_log.md) 和 [seed_selection_candidates.md](./seed_selection_candidates.md) 获取细节。
5. 进入 [papers/](./papers/) 下单篇目录时，先读 `bibtex.bib`，再读 `paper_content.txt`，必要时核对 `paper.pdf`，最后看 `seed_desc.md` 与 `artifacts.md`。

## strict seed 速记

只有同时满足以下条件，才可标为 `SS-A`：

1. 输入主源是自然语言需求、用例、场景、系统描述或文本规格。
2. 输出属于 `T0` 的 `FSM / HSM / EFSM / statechart` 家族。
3. 存在 `NL -> STM` generation / synthesis / derivation / extraction-from-NL 关系。
4. 有可追踪证据指针。

`protocol FSM`、BPMN/process、Petri/CSP/Rebeca/Event-B/TLA+/LTL/STL、`T1+` / hybrid、repair-only、co-exist-only、形式规格或已有图模型转换均不得进入主 strict seed。

## PR-R1.6 / R1.7 交接速记

- 当前可交接给 PR-R2 的主 / 条件主候选、R1.7 negative evidence 与 fallback 见 [seed_selection_candidates.md](./seed_selection_candidates.md)。
- `SS-A/SS-B + SA-1/SA-2` 只是进入 PR-R2 人工裁决的必要条件；当前计数还必须检查 [candidate_matrix.md](./candidate_matrix.md) 的 `计数资格`，最终四例仍需 case-level freeze。
- `SA-3/SA-4/SA-5`、paper-only、private-only、completion-only、scenario/formal input、protocol/standard sentinel 和 `sources/` 构造项均不计 PR-R2 主 / 条件主 seed 候选。
- `fsm-bench-20` 是强 pipeline fallback，但没有公开冻结 generated outputs；若使用，需要 PR-R2 复跑并保存 run record。
