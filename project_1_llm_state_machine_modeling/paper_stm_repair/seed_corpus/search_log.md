# strict seed search log

本文件记录 PR-R1.5 的检索边界。当前条目是初始 bounded snapshot，不代表全域 census。

| 批次 | 日期 | source | query / 入口 | cap | 原始命中 | 去重后 | 进入 title/abstract | 进入 fulltext/artifact | 失败 / blocker | 早停理由 | 备注 |
|---|---|---|---|---:|---:|---:|---:|---:|---|---|---|
| local-baseline-r1 | 2026-06-14 | 本地 baseline + R1 台账 | `baseline_candidate_matrix.md` + strict survey 初判 | 20 | 12 | 12 | 12 | 10 | 0 | 初始执行批次 | 覆盖 positive 与 protocol negative sentinel |
| external-query-plan | 2026-06-14 | Semantic Scholar / arXiv / OpenAlex / IEEE / ACM / DBLP / publisher | 见 [GUIDE.md](./GUIDE.md) §2.2 | 待执行 | 待执行 | 待执行 | 待执行 | 待执行 | 待执行 | 待执行 | 后续批次按 query cluster 展开 |
| snowballing-plan | 2026-06-14 | references / cited-by | 从 `from-use-cases-to-statecharts`、`synthesizing-statecharts...`、`structure-event` 等候选出发 | 待执行 | 待执行 | 待执行 | 待执行 | 待执行 | 待执行 | 待执行 | 记录 `snowballing_parent_id` |
| external-openalex-nl-req-sm | 2026-06-14 | OpenAlex | `natural language requirements state machine generation` | top 20 | 20 | 未人工去重 | 未筛查 | 0 | 高噪声：首批命中 LeCun/Quantum Espresso 等非目标 | query 过宽，早停；需 exact phrase / 排除词 | 原始结果见 `search_results/openalex_nl_req_state_machine.jsonl` |
| external-openalex-use-case-statechart | 2026-06-14 | OpenAlex | `use case statechart generation` | top 20 | 20 | 未人工去重 | 未筛查 | 0 | 高噪声：NuSMV/UPPAAL 等工具泛命中 | query 过宽，早停；需 exact phrase / venue / title filter | 原始结果见 `search_results/openalex_use_case_statechart.jsonl` |
| external-planner-scout | 2026-06-14 | mixed web / arXiv / ACM / Springer / ResearchGate line search | scout agent query plan | 20 candidates | 20 | 20 | 10+ | 待核 | 部分链接为 publisher / RG，需要人工下载 | 作为 external candidate seeds 写入 `candidate_matrix.md` |
| sources-scout | 2026-06-14 | local `sources/` | `FSM/HSM/EFSM + T0 + A/A + high-priority` 抽样策略 | 10 candidate lines | 10 | 10 | 0 | 0 | sources 不自动 strict | 作为 source candidate / possible student seed，不直接标 SS-A |
