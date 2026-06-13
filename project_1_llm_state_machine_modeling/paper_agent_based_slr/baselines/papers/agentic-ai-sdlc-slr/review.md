# Assistance to Autonomy: A Systematic Literature Review of Agentic AI across the Software Development Life Cycle

## 1. 快速结论卡片

| 字段 | 内容 |
|---|---|
| 标题 | Assistance to Autonomy: A Systematic Literature Review of Agentic AI across the Software Development Life Cycle |
| 年份 | 2026 |
| 分层 | P1：SE 场景强相关；对 paper2 的主要威胁来自 multi-agent screening pipeline，而不是综述主题本身 |
| 阅读状态 | 已读全文文本-paper_content核验 |
| 证据等级 | 全文文本级；图表/表格细节待人工 PDF 核对 |
| 核验入口 | [bibtex.bib](./bibtex.bib)、[paper_content.txt](./paper_content.txt)；未人工打开 PDF 图表 |
| 输入 | 四个数据库导出的 raw publication metadata、研究目标/RQ/选择标准 prompt、inclusion/exclusion criteria |
| 输出 | 去重后的候选、quality-control/screening/relevance labels、agent reasoning/dialogue、92 篇人工确认 primary studies、SDLC thematic synthesis |
| 方法/系统形态 | Kitchenham-style SLR + model/domain-agnostic six-step LLM multi-agent screening pipeline；Assistant/Evaluator 双 agent 独立判断并通过 argumentation 解决冲突 |
| 覆盖阶段 | 传统 SLR 覆盖 search、criteria、manual full-text reading、coding、thematic synthesis；LLM 自动化主要覆盖 metadata curation、QC、screening、relevance selection |
| 人审/审计机制 | reviewer approve prompts；agent decisions、reasoning、dialogue 透明；unresolved conflicts default to inclusion；127 篇候选经人工 abstract/full-text two-pass verification；抽样核验 false negatives |
| 实验/指标 | 1609 raw records、1331 processed、796 valid、265 screening pass、127 relevance candidates、92 final studies；100 篇 excluded sample false-negative audit |
| 主要发现 | SDLC 中 Testing & QA、Maintenance、Deployment、Coding 等后期或可执行反馈阶段更成熟；Planner-Executor-Reviewer 是主导模式；工业缓解策略集中在 bounded/verifiable spaces |
| 对 paper2 的作用 | 强约束 paper2 的 SE positioning 和 screening audit：已有 SE SLR 使用 multi-agent screening、dialogue、默认 include、人工 two-pass verification 和 false-negative 抽样 |
## 2. D1-D7 全文核验评分

emoji 口径见 [../../GUIDE.md](../../GUIDE.md)。

| D1 | D2 | D3 | D4 | D5 | D6 | D7 |
|---|---|---|---|---|---|---|
| 🟡 | 🟡 | 🟡 | 🟢 | 🟢 | 🟢 | 🟡 |

| 维度 | 评分 | 全文证据锚点 | 判定理由 |
|---|---:|---|---|
| D1 主题贴合度 | 🟡 | Page 1 Abstract：主题是 agentic AI across SDLC；Page 2 Introduction：贡献之一是 multi-agent screening pipeline | 论文是 SE 领域 SLR，但研究对象是 agentic AI in SDLC；LLM/agent 辅助 SLR 是方法贡献，不是全文主问题，因此中等。 |
| D2 SLR/SMS 流程覆盖度 | 🟡 | Page 4-7 §3：query、time frame、criteria、six-step pipeline、manual two-pass protocol；Page 7：full-text reading 和 coding sheet | SLR 本身覆盖完整流程，但自动化主要落在 metadata curation、QC、screening、relevance selection；抽取/综合仍由人工执行。 |
| D3 LLM/agent 自动化深度 | 🟡 | Page 6-7 §3.4：Assistant/Evaluator 生成/评估 prompts、独立分类、三轮 dialogue、conflict default inclusion；Page 8：使用 gpt-5.4、gpt-5.2、gpt-5-mini、gpt-5-nano、deepseek-v3 | 自动化链清楚，但限于筛选/相关性选择，不是多阶段 SLR 全流程 agent。 |
| D4 人工审计与可追踪性 | 🟢 | Page 6：full transparency of decisions, reasoning, agent dialogue；Page 7：reviewer approves prompt，unresolved conflicts default to inclusion；Page 8-9：manual evaluation 和 false-negative sampling | 明确保留 decision/reasoning/dialogue，并有人工 two-pass verification、默认 include 和抽样 false-negative 审计，满足强审计分。 |
| D5 评价严谨性 | 🟢 | Page 8 Table 2：1609→1331→796→265→127→92；Page 8-9：100 excluded sample，1 false negative；Page 10 Table 3：92 studies by SDLC/evaluation context | 有真实高容量 SLR、人工确认 final set、excluded 抽样核验和定量流程统计，评价设计扎实。 |
| D6 SE/CCF 相关性 | 🟢 | `bibtex.bib`：arXiv cs.SE；Page 1 Keywords：Software Engineering、SDLC、SLR；Page 15 references 含多篇 SE venue/IEEE/TSE 工作 | 直接面向软件工程和 SDLC，是 paper2 目标社区的强相关背景。 |
| D7 对本文 novelty 的威胁 | 🟡 | Page 2：multi-agent screening pipeline with metadata curation、dialogue、inclusion-biased conflict resolution；Page 15 §7：repository contains source code、prompts、raw datasets | 威胁 paper2 的 screening automation、audit 和 SE SLR positioning；但不覆盖抽取、编码、综合、claim-to-source 报告生成的完整组合。 |

## 3. 论文解决的问题与背景

论文主问题是：agentic AI 在软件产品开发生命周期中哪些阶段更成熟、哪些架构模式更常见、工业部署面对哪些挑战和缓解策略。由于 2023 年以后相关论文快速增长，作者认为手工筛选大量文献非常耗时，所以构建了一个多 agent screening pipeline 作为方法学贡献。

这篇论文对 paper2 的价值有两层。第一层是内容背景：它总结 SE 中 agentic AI 的成熟度和 verifiability 规律。第二层更关键：它已经在 SE SLR 中真实使用 multi-agent LLM pipeline 完成高容量筛选，并报告人工核验和 false-negative 风险。这是 paper2 在“agentic SLR workflow” story 里必须正面区分的近邻。

## 4. 方法 / 系统拆解

SLR 研究设计遵循 Kitchenham and Charters。数据库从 Google Scholar、Scopus、IEEE Xplore、ACM DL、ScienceDirect 初始列表中筛选，最终因可复现性和检索限制保留 IEEE、ACM、SpringerLink、Scopus。查询用 CIMO 逻辑构造，覆盖 software lifecycle / development / product、agentic / autonomous / LLM agent、多 agent、tool use / self-reflection / orchestration、automation / efficiency 等词。

multi-agent pipeline 有六步。第一步由 Assistant 和 Evaluator 根据研究目的、RQ 和选择标准生成并评估后续任务 prompt，reviewer 批准后才进入下一步。第二步把 CSV/RIS/BIB 原始导出统一成 CSV 并去重。第三步通过 web scraping 和 API 补齐缺失 abstract。第四步 Quality Control 用单 agent 排除 conference preamble、generic book chapter 等非研究条目，并建议人工核验缺 abstract 的 excluded records。第五步 Screening 中 Assistant 和 Evaluator 独立按 inclusion/exclusion criteria 分类；冲突时最多三轮 inter-agent argumentation，未解决则默认 include。第六步 Relevance Selection 复用同样多 agent 过程，但聚焦 RQ 和 scope alignment。

人工协作不是事后装饰。作者说明 prompt 需要 reviewer approval；自动 pipeline 之后，对候选 relevant publications 做结构化 two-pass manual evaluation：先读 127 篇 abstract 核验 Criteria 6/7/8，再全文阅读 confirmed relevant studies 并用 coding sheet 抽取 SDLC phase、evaluation context、architectural pattern、limitations/mitigations。

## 5. 实验 / 评价设计

RQ1 关注 SDLC 哪些阶段的 agentic AI 成熟度和工业采用最高；RQ2 关注 dominant architectural patterns；RQ3 关注工业环境的挑战和缓解方式。数据来源是 2023 年以来四个数据库的检索结果。流程统计为：1609 raw records、1331 processed records、796 valid publications、265 screening pass、127 relevance candidates、92 manually verified primary studies。

pipeline 可靠性用 excluded sample 检查 false negatives：作者从 agent-based stages 排除的论文中抽样 100 篇，其中 screening exclusion 50 篇、relevance selection exclusion 50 篇。人工核验发现 1 个 false negative，来自 relevance-selection phase；screening phase 为 0/50。作者据此外推全 excluded population 约 7 篇 missed relevant publications，但这只是估计，不应写成确定事实。

thematic synthesis 用 final 92 studies 做编码和统计。Table 3 给出 SDLC phase 与 industrial/academic context 分布：Maintenance 20、Testing & QA 18、Cross-cutting 15、Deployment & Operations 14、Coding & Implementation 12、Requirements Analysis 7、Project Management 3、Design & Architecture 3；工业 context 共 13，academic PoC 共 79。

## 6. 主要结果与结论

核心结论是 output verifiability 是 agentic AI adoption 的主要推动因素。后期 SDLC 阶段更成熟，因为测试结果、编译器输出、fault localization traces、logs、operational metrics 等可执行反馈可以为 self-refinement loops 提供明确目标。Requirements Analysis、Design & Architecture、Project Management 等早期阶段几乎都是 academic PoC，因为缺少稳定 ground-truth feedback。

架构上，Planner-Executor-Reviewer 是最常见模式，Orchestrator 管理子流程；结构化 inter-agent communication 如 JSON 或 LangGraph state graphs 替代自由文本 handoff。Reviewer agent 被解释为 verifiability mechanism。工业缓解策略包括 predefined action space、structured outputs、tool/API communication、stage-specific pass/fail tests、hybrid vector-graph retrieval、knowledge graph memory 等，目的都是把 agent 行为限制在 bounded, verifiable spaces。

## 7. 局限与可复现性

Threats to validity 明确说 query keywords 和 database coverage 可能漏文献；relevance decisions 依赖 prompt 和具体 LLM model，未来模型变化会引入系统性 variability；grey literature 被排除，而工业 agentic AI practice 常先出现在 grey literature；快速演化带来 temporal validity 风险。

可复现性方面，Page 15 §7 声称 online repository 包含 multi-agent pipeline 源码、Assistant/Evaluator prompts、四个数据库的 raw datasets。但 `paper_content.txt` 中链接位置是 “click here”，提取文本没有保留实际 URL；写作前需回 PDF 或网页核验仓库链接是否真的可访问。

## 8. 对 paper2 story / 实验设计的影响

paper2 不能声称 SE SLR 中尚未有人用 multi-agent LLM 做筛选。已有这篇工作实现了 metadata curation、agent dialogue、conflict inclusion default、manual two-pass verification 和 false-negative sampling。paper2 的差异化要具体落在更完整的 SLR 生命周期：不仅筛选，还要抽取、编码、综合、报告生成和 claim-to-source 证据链。

这篇还给 paper2 一个很强的实验设计提醒：screening pipeline 应优先降低 false negatives，冲突默认 include 是合理策略；但要用抽样或全量人工复核估计遗漏风险。paper2 如果引入 agent reviewer，也应保留 agent dialogue、decision reason、人工裁决和 excluded sample audit。

## 9. 可用于写作的引用角度

- 作为 SE 场景近邻：已有 agentic AI across SDLC 的 SLR 使用 multi-agent pipeline 处理高容量筛选，并公开强调 false-negative minimization。
- 作为 human audit 设计参照：该工作把 agent conflict、argumentation、default inclusion 和人工 two-pass verification 组合起来，是 paper2 screening gate 的直接对照。
- 作为 story 支撑：SE agentic systems 的工业采用依赖可验证输出，paper2 可以把 SLR 阶段证据链设计为一种 verifiability mechanism。

## 10. 待复核清单

- 回 PDF 或在线版本核验 §7 的 repository 链接，确认源码、prompts、raw datasets 是否实际可访问。
- 核验 gpt-5.4、gpt-5.2 等模型命名是否为作者原文设定，避免在 paper2 中直接当作现实 API 事实扩写。
- 若引用 false-negative 外推，只能写“作者估计/外推”，不能写成真实漏检总数。
- 检查是否已有 peer-reviewed 版本；当前 BibTeX 是 arXiv cs.SE。
