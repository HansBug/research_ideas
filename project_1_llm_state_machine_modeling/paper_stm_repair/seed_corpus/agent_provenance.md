# seed corpus agent provenance

本文件记录 PR-R1.5 内部文献筛查与单篇全文 agent 的细账。跨 PR 摘要同步到 [../plan/agent_provenance.md](../plan/agent_provenance.md)。

| 时间 | agent | 类型 | 输入 | 输出 | 状态 | 失败 / 风险 | 复查 |
|---|---|---|---|---|---|---|---|
| 2026-06-14 | 主 session | 初始化 | PR #100/#104/R1 strict 协议 | seed_corpus 框架与初始候选矩阵 | completed | 初始候选多为 pending，需全文 agent 逐篇核验 | 待 review |
| 2026-06-14 | literature scout A/B/C | 只读预侦察 | baselines / sources / external query plan | 候选线索与检索策略 | completed | 已整合到 candidate/search/screening/exclusion | 主 session 已复核 |
| 2026-06-14 | paper-reader batch 1 | 单篇全文核验 | `sefm-llm-state-machine` / `llms-emp-stm-subset` / `ttool-ai-smd-subset` / `designing-fsm-gpt4` / `umple-nl-state-machine` / `from-use-cases-to-statecharts` | 6 个 `seed_desc.md` 与 `artifacts.md` | completed | SA/SS 结论已回填 summary/matrix | implementation review 已触发修复 |
| 2026-06-14 | paper-reader batch 2 | 单篇全文核验 | `beyond-scenarios-state-models` / `scenarios-statecharts-interrelated` / `executable-state-machines-structured-text` | 3 个 `seed_desc.md` 与 `artifacts.md` | completed | 1 个 NN-D 负例、2 个 SS-B/SA-3 已回填 | implementation review 已触发修复 |
| 2026-06-14 | implementation review fix | C/I 修复 | deepseek / codex / claude implementation comments | `req-mermaid-statechart` 单篇目录、27 条 screening ledger、TTool timing 降级、R2 blocker handoff | completed | 主 seed 保守计数降为 3，交由 PR-R2 处理四例下限 | 主 session + Rawls 只读顾问复核 |

| 2026-06-14 | R1.6 completion/use-case/scenario subagents | 只读候选核验 | `completion-sysml-gwt` / `towards-automatic-model-completion` / `automated-transition-use-cases-uml-sm` / `from-use-cases-to-statecharts` / `execution-nl-req-bt-sm` / scenario-statechart 候选 | completion-only、BT intermediate、sequence/formal scenario 与 classic use-case manual queue 结论 | completed | 多数为 `SA-3/SA-5` 或 P1/P3 失败，不计主 seed | 主 session 已回填 matrix/ledger |
| 2026-06-14 | R1.6 LLM/recent subagent | 只读候选核验 | `fsm-bench-20`、IJISRT UML state diagrams、TechScience/HF unified UML dataset、fbAssistant 等 | `fsm-bench-20` outputs 未冻结；`unified-uml-multimodal-validation` 为条件候选；IJISRT paper-only | completed | synthetic requirement、license unclear、outputs missing | 主 session 已下载/冻结可公开 artifacts |
| 2026-06-14 | main session | R1.6 整合 | Crossref / Zenodo / GitHub / HF / PDF 下载 / search rounds | 36 candidates、15 paper dirs、4 主/条件主 handoff、11 manual queue | completed | PR-R2 仍需 case-level freeze；R1.6 不跑四例 | 待 implementation review |
