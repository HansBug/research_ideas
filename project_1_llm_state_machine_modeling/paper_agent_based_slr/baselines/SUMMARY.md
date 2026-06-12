# baselines/SUMMARY.md：PR-B0 近邻 baseline 总账

> 更新时间：`2026-06-13 02:40:00`（Asia/Shanghai）
> 本文件记录 LLM-based SLR / agentic literature-review 近邻 baseline 的粗筛结果。它不是最终系统综述结论；所有 title / abstract 级判断后续都要回到 PDF / `paper_content.txt` 做全文核验。

## 1. 当前总览

| 项 | 数量 / 状态 |
|---|---:|
| arXiv title / abstract 候选 | 34 |
| 本地建库 P0/P1 候选 | 25 |
| P0 强 baseline | 10 |
| P1 高度关注 | 15 |
| P2 背景相关 | 9 |
| CCF title-level 命中 | 1 条 CCF-adjacent / ICSE workshop 线索 |
| 人工下载清单 | [search/manual-download-needed.bib](./search/manual-download-needed.bib) |

## 2. 口径说明

- 分层：P0 = 强 baseline；P1 = 高度关注 / 局部强 baseline；P2 = 背景相关。
- D1-D7：D1 主题、D2 流程、D3 自动化、D4 审计、D5 评价、D6 SE/CCF、D7 novelty 威胁；完整标准见 [GUIDE.md](./GUIDE.md)。
- emoji 列只写 emoji：🟢 强，🟡 中，🟠 弱，⚪ 无或背景。
- `核验阶段` 默认为粗筛；只有后续人工逐段阅读 PDF / `paper_content.txt` 后才能升级为全文核验。

## 3. P0/P1 本地建库总表

| 年份 | 分层 | 标题 | D1 | D2 | D3 | D4 | D5 | D6 | D7 | 本地目录 | 初步判断 |
|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| 2026 | P0 | Evaluating AI-based Scientific Knowledge Synthesis with Epidemiological Systematic Reviews | 🟢 | 🟢 | 🟢 | 🟡 | 🟢 | 🟠 | 🟢 | [review.md](./papers/agent-slr-evaluation-harness/review.md) | AgentSLR evaluation harness 面向 AI-based scientific knowledge synthesis，含专家标注数据和分阶段评测，强约束本文评价协议。 |
| 2026 | P0 | A Multi-Agent Human-LLM Collaborative Framework for Closed-Loop Scientific Literature Summarization | 🟢 | 🟢 | 🟢 | 🟢 | 🟡 | 🟠 | 🟢 | [review.md](./papers/closed-loop-literature-summarization/review.md) | multi-agent human-LLM collaborative framework，覆盖 filtering、data extraction、summarization 与 human oversight，是闭环 literature summarization / evidence package 强近邻。 |
| 2026 | P0 | Eligibility-Aware Evidence Synthesis: An Agentic Framework for Clinical Trial Meta-Analysis | 🟢 | 🟡 | 🟢 | 🟡 | 🟡 | 🟠 | 🟢 | [review.md](./papers/eligibility-aware-evidence-synthesis/review.md) | agentic framework for clinical trial meta-analysis，覆盖 eligibility-aware evidence synthesis，约束端到端 evidence synthesis claim。 |
| 2026 | P0 | EviSearch: A Human in the Loop System for Extracting and Auditing Clinical Evidence for Systematic Reviews | 🟢 | 🟡 | 🟢 | 🟢 | 🟡 | 🟠 | 🟢 | [review.md](./papers/evisearch/review.md) | 多 agent clinical evidence extraction，强调 per-cell provenance 与 human verification，是 traceability/evidence package 强近邻。 |
| 2026 | P0 | Beyond Accuracy: LLM Variability in Evidence Screening for Software Engineering SLRs | 🟢 | 🟠 | 🟡 | 🟡 | 🟢 | 🟢 | 🟡 | [review.md](./papers/llm-variability-se-slr-screening/review.md) | 直接面向软件工程 SLR screening，评估 LLM variability 与 false negative 风险，强约束本文 screening claim。 |
| 2026 | P0 | LR-Robot: An Human-in-the-Loop LLM Framework for Systematic Literature Reviews with Applications in Financial Research | 🟢 | 🟢 | 🟢 | 🟢 | 🟠 | 🟠 | 🟢 | [review.md](./papers/lr-robot/review.md) | Human-in-the-loop LLM framework for SLR，覆盖筛选与综合，直接威胁 human audit + SLR 自动化组合 claim。 |
| 2026 | P0 | SWARM-SLR AIssistant: A Unified Framework for Scalable Systematic Literature Review Automation | 🟢 | 🟡 | 🟢 | 🟡 | 🟠 | 🟠 | 🟢 | [review.md](./papers/swarm-slr-aiassistant/review.md) | SLR 自动化统一框架 + agent-based assistant，直接覆盖本文的 agent workflow 近邻。 |
| 2025 | P0 | LatteReview: A Multi-Agent Framework for Systematic Review Automation Using Large Language Models | 🟢 | 🟡 | 🟢 | 🟡 | 🟡 | 🟠 | 🟢 | [review.md](./papers/latte-review/review.md) | 多 agent 框架自动化 SLR screening、relevance scoring、structured extraction，是直接竞品级 baseline。 |
| 2024 | P0 | Large Language Models for Automated Literature Review: An Evaluation of Reference Generation, Abstract Writing, and Review Composition | 🟢 | 🟡 | 🟡 | 🟠 | 🟢 | 🟠 | 🟡 | [review.md](./papers/llm-automated-literature-review-evaluation/review.md) | 评估 LLM 自动文献综述的 reference generation、abstract writing、review composition 与 hallucination，直接约束 factuality claim。 |
| 2024 | P0 | Accelerating Clinical Evidence Synthesis with Large Language Models | 🟢 | 🟢 | 🟡 | 🟡 | 🟢 | 🟠 | 🟡 | [review.md](./papers/trialmind/review.md) | LLM pipeline for clinical evidence synthesis，覆盖 study search、screening、data extraction，并有 benchmark，构成强方法学 baseline。 |
| 2026 | P1 | Assistance to Autonomy: A Systematic Literature Review of Agentic AI across the Software Development Life Cycle | 🟢 | 🟡 | 🟢 | 🟡 | 🟢 | 🟢 | 🟡 | [review.md](./papers/agentic-ai-sdlc-slr/review.md) | agentic AI across SDLC 的 SLR，并使用/验证 multi-agent screening pipeline；SE 场景强相关但主题是 agentic AI landscape。 |
| 2026 | P1 | Can Deep Research Agents Retrieve and Organize? Evaluating the Synthesis Gap with Expert Taxonomies | 🟢 | 🟡 | 🟢 | 🟠 | 🟢 | 🟠 | 🟡 | [review.md](./papers/deep-research-agents-synthesis-gap/review.md) | 评估 deep research agents 的 retrieval/organization 与 expert taxonomies，和 agentic literature review 的 coverage/synthesis gap 直接相关。 |
| 2026 | P1 | On the Use of a Large Language Model to Support the Conduction of a Systematic Mapping Study: A Brief Report from a Practitioner's View | 🟢 | 🟡 | 🟡 | 🟡 | 🟠 | 🟡 | 🟡 | [review.md](./papers/llm-support-systematic-mapping-report/review.md) | 实践者视角报告 LLM 支持 systematic mapping，覆盖流程经验、prompt effort 与挑战，对 SMS 场景很相关。 |
| 2026 | P1 | A Reproducible Optimisation Protocol for Calibrating Prompt-Based Large Language Model Workflows in Evidence Synthesis | 🟢 | 🟡 | 🟡 | 🟢 | 🟢 | 🟠 | 🟡 | [review.md](./papers/prompt-optimisation-evidence-synthesis/review.md) | reproducible optimisation protocol for prompt-based LLM workflows in evidence synthesis，强约束 reproducibility / prompt calibration claim。 |
| 2026 | P1 | SLRMentor: An LLM-Based Tool Supporting Learning of SLR in Software Engineering | 🟢 | 🟠 | 🟡 | 🟡 | 🟠 | 🟢 | 🟡 | [review.md](./papers/slrmentor/review.md) | 面向软件工程 SLR 学习与 planning 的 LLM assistant，SE 场景强相关但偏教育/planning。 |
| 2026 | P1 | SurveyLens: A Discipline-Aware Benchmark for Automatic Survey Generation | 🟢 | 🟡 | 🟡 | 🟠 | 🟢 | 🟠 | 🟡 | [review.md](./papers/surveylens/review.md) | automatic survey generation benchmark，评估 retrieval/organization/synthesis，可约束自动 survey generation claim。 |
| 2025 | P1 | Can Agents Judge Systematic Reviews Like Humans? Evaluating SLRs with LLM-based Multi-Agent System | 🟢 | 🟡 | 🟢 | 🟡 | 🟡 | 🟠 | 🟡 | [review.md](./papers/agents-judge-systematic-reviews/review.md) | LLM-based multi-agent system 评估 SLR 质量并对齐 PRISMA，和本文 reviewer/audit gate 有直接关系。 |
| 2025 | P1 | ARISE: Agentic Rubric-Guided Iterative Survey Engine for Automated Scholarly Paper Generation | 🟢 | 🟡 | 🟢 | 🟡 | 🟡 | 🟠 | 🟡 | [review.md](./papers/arise-agentic-survey-engine/review.md) | agentic rubric-guided iterative survey engine，覆盖主题扩展、引用整理、摘要/草稿生成和同行评审式评价，对报告生成与质量控制阶段有威胁。 |
| 2025 | P1 | Compiling Prompts, Not Crafting Them: A Reproducible Workflow for AI-Assisted Evidence Synthesis | 🟢 | 🟡 | 🟡 | 🟡 | 🟡 | 🟠 | 🟡 | [review.md](./papers/compiling-prompts-evidence-synthesis/review.md) | 提出 prompt compilation / reproducible workflow for AI-assisted evidence synthesis，约束 reproducibility 与 prompt workflow claim。 |
| 2025 | P1 | LiRA: A Multi-Agent Framework for Reliable and Readable Literature Review Generation | 🟢 | 🟡 | 🟢 | 🟠 | 🟢 | 🟠 | 🟡 | [review.md](./papers/lira-literature-review-agents/review.md) | multi-agent literature review generation，显式评估 readability/factual accuracy/citation quality，对报告生成阶段有约束。 |
| 2025 | P1 | Evaluating Prompting Strategies and Large Language Models in Systematic Literature Review Screening: Relevance and Task-Stage Classification | 🟢 | 🟠 | 🟡 | 🟠 | 🟢 | 🟠 | 🟡 | [review.md](./papers/llm-slr-screening-prompting-strategies/review.md) | 系统评估不同 LLM 与 prompting strategy 在 SLR screening 的表现，提供 screening 指标和成本基线。 |
| 2025 | P1 | Leveraging LLMs for Semi-Automatic Corpus Filtration in Systematic Literature Reviews | 🟢 | 🟠 | 🟡 | 🟡 | 🟡 | 🟠 | 🟡 | [review.md](./papers/llmsurver-corpus-filtration/review.md) | 用多个 LLM 与 consensus scheme 做 SLR corpus filtration，并有人监督 visual interface，和人审筛选强相关。 |
| 2024 | P1 | Mixture of Knowledge Minigraph Agents for Literature Review Generation | 🟢 | 🟡 | 🟢 | 🟠 | 🟢 | 🟠 | 🟡 | [review.md](./papers/knowledge-minigraph-agents-review/review.md) | collaborative knowledge minigraph agents for literature review generation，偏 synthesis/report generation，对自动综述写作有参考价值。 |
| 2024 | P1 | LLAssist: Simple Tools for Automating Literature Review Using Large Language Models | 🟢 | 🟡 | 🟡 | 🟠 | 🟠 | 🟠 | 🟡 | [review.md](./papers/llassist/review.md) | 开源 LLAssist 工具自动化文献 review 的 extraction 与 relevance evaluation，可作工具类对照。 |
| 2024 | P1 | High-performance automated abstract screening with large language model ensembles | 🟢 | 🟠 | 🟡 | 🟠 | 🟢 | 🟠 | 🟡 | [review.md](./papers/llm-abstract-screening-ensembles/review.md) | LLM ensemble 用于 systematic review abstract screening，提供 screening 阶段强评价基线。 |

## 4. P2 保留候选

| 年份 | 标题 | arXiv | D1 | D2 | D3 | D4 | D5 | D6 | D7 | 保留理由 |
|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| 2026 | LLM-Assisted Empirical Software Engineering: Systematic Literature Review and Research Agenda | [2604.26192](https://arxiv.org/abs/2604.26192) | 🟡 | 🟠 | ⚪ | ⚪ | 🟡 | 🟢 | 🟠 | LLM-assisted empirical SE 的 SLR/agenda，不是自动化 SLR 工具，但 SE 背景强。 |
| 2026 | OpenExtract: Automated Data Extraction for Systematic Reviews in Health | [2603.13338](https://arxiv.org/abs/2603.13338) | 🟡 | 🟠 | 🟡 | 🟠 | 🟡 | 🟠 | 🟠 | automated data extraction for health systematic reviews，偏 extraction 局部基线。 |
| 2025 | Agentic AutoSurvey: Let LLMs Survey LLMs | [2509.18661](https://arxiv.org/abs/2509.18661) | 🟡 | 🟡 | 🟢 | 🟠 | 🟡 | 🟠 | 🟠 | multi-agent automated survey framework，偏 LLM survey 写作。 |
| 2025 | AutoSurvey2: Empowering Researchers with Next Level Automated Literature Surveys | [2510.26012](https://arxiv.org/abs/2510.26012) | 🟡 | 🟡 | 🟡 | 🟠 | 🟡 | 🟠 | 🟠 | multi-stage automated literature survey pipeline，偏 survey generation 背景。 |
| 2025 | Patience is all you need! An agentic system for performing scientific literature review | [2504.08752](https://arxiv.org/abs/2504.08752) | 🟡 | 🟡 | 🟢 | 🟠 | 🟡 | 🟠 | 🟠 | agentic scientific literature review / QA，偏跨域文献搜索与蒸馏。 |
| 2025 | SurveyEval: Towards Comprehensive Evaluation of LLM-Generated Academic Surveys | [2512.02763](https://arxiv.org/abs/2512.02763) | 🟡 | 🟡 | 🟡 | 🟠 | 🟢 | 🟠 | 🟠 | LLM-generated academic survey evaluation benchmark，偏 survey 质量评价背景。 |
| 2025 | SurveyG: A Multi-Agent LLM Framework with Hierarchical Citation Graph for Automated Survey Generation | [2510.07733](https://arxiv.org/abs/2510.07733) | 🟡 | 🟡 | 🟢 | 🟠 | 🟡 | 🟠 | 🟠 | multi-agent survey generation with citation graph，偏 survey generation 背景。 |
| 2025 | SurveyGen: Quality-Aware Scientific Survey Generation with Large Language Models | [2508.17647](https://arxiv.org/abs/2508.17647) | 🟡 | 🟡 | 🟡 | 🟠 | 🟡 | 🟠 | 🟠 | quality-aware scientific survey generation，偏 survey generation/evaluation。 |
| 2024 | Automated Literature Review Using NLP Techniques and LLM-Based Retrieval-Augmented Generation | [2411.18583](https://arxiv.org/abs/2411.18583) | 🟡 | 🟡 | 🟡 | 🟠 | 🟠 | 🟠 | 🟠 | NLP+RAG 自动生成 literature review，偏报告生成和 RAG 背景。 |

## 5. 强 baseline 对 story 的威胁

| baseline 组 | 代表论文 | 威胁的 claim | 后续差异化要求 |
|---|---|---|---|
| 多 agent / agentic SLR workflow | LatteReview、SWARM-SLR AIssistant、LR-Robot、Closed-loop literature summarization、AgentSLR evaluation harness | “agent workflow 自动化 SLR”本身已不是充分 novelty | 必须强调 SE 场景、阶段化 run record、claim-to-source 不可断链、透明报告与人工审计门。 |
| 人工参与与 provenance / audit | EviSearch、LR-Robot、Closed-loop literature summarization、Prompt optimisation evidence synthesis | “human-in-the-loop + 可追踪证据综合”已有强近邻 | 必须证明本文审计链覆盖报告级 claim、筛选决策、抽取记录、编码与证据定位，而不是只做用户反馈。 |
| SLR screening / corpus filtration | LLM variability in SE SLR screening、LLM abstract screening ensembles、LLMSurver、Prompting strategies | 局部筛选模块已有系统评价 | 本文不能把筛选准确率当唯一贡献；若评估筛选，需对比 false negative、模型变异、人工复核和成本。 |
| 自动 survey / review generation | LiRA、ARISE、SurveyLens、Knowledge Minigraph Agents | “自动生成综述文本”已有密集工作 | 本文若写报告生成，必须把重点落在证据链、unsupported claim 控制和透明报告，而非生成质量本身。 |
| SE 场景近邻 | LLM variability in SE SLR screening、SLRMentor、Agentic AI across SDLC SLR、LLM-assisted empirical SE SLR | SE 社区已有 LLM+SLR 讨论 | 本文必须定位为可审计 agent workflow / evidence package，而不是泛泛 LLM 辅助 SE SLR。 |

## 6. 当前总体判断

1. **不能再把 novelty 写成“首次 LLM / agent 自动化 SLR”**：P0 中已有多个 multi-agent、human-in-the-loop、SLR automation 或 evidence synthesis 框架。
2. **本文还有潜在空间，但必须收窄**：较稳妥的 story 是“面向软件工程 SLR/SMS 的可审计 agent 工作流”，强调阶段化证据包、claim-to-source 不可断链、人工审计门、透明报告和失败分类。
3. **实验必须支撑审计可靠性，而不是只展示生成结果**：后续 A3/A5 至少要评价证据定位正确性、unsupported claim 率、审计拦截率、筛选 false negative 风险、人工成本和透明报告完整性。
4. **CCF 负证据必须保守**：本轮 CCF 主会 / 期刊 title-level 粗筛未发现完整组合 baseline，但 coverage 有缺口，不能据此声称 CCF 近三年没有相关工作。

## 7. CCF 与人工下载

- CCF coverage / gap 见 [search/ccf-venue-coverage-gaps.md](./search/ccf-venue-coverage-gaps.md)。
- CCF title-level 粗筛见 [search/ccf-abc-2024-2026-title-abstract-screening.md](./search/ccf-abc-2024-2026-title-abstract-screening.md)。
- 当前人工下载清单见 [search/manual-download-needed.bib](./search/manual-download-needed.bib)。其中 `WSESE@ICSE 2025` 命中与 SE SLR + LLM 直接相关，应在用户拿到全文后升级单篇目录。

## 8. 后续工作建议

1. 优先全文细读 10 篇 P0，形成正式 Related Work 对照矩阵。
2. 把 P1 中的 screening / prompt calibration / survey generation 工作拆成局部 baseline，映射到 A2/A3/A5 的模块级评价。
3. 获取 WSESE@ICSE 2025 workshop 论文全文，并核验是否已有软件工程社区关于 LLM 执行 / 复制 SLR 的直接讨论。
4. 在上游 story 中降级“自动化 SLR”宽泛 claim，强化“可审计证据包 + human audit gate + SE 场景”的组合贡献。
5. 后续如果要写 CCF A 类级别论文，需要补一个更严格的 fulltext baseline review PR，不能只依赖当前粗筛。

## 9. 更新日志

| 时间 | 更新内容 |
|---|---|
| `2026-06-13 02:40:00` | PR-B0 实现：建立 25 篇 P0/P1 本地 baseline 文库，重写 README/GUIDE/SUMMARY，更新 arXiv 34 篇粗筛表与 CCF coverage/gap。 |
| `2026-06-13 01:20:00` | 初始 arXiv / CCF 粗筛与自动 PDF 下载。 |
