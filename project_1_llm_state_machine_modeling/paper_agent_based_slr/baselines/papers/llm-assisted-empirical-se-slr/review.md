# LLM-Assisted Empirical Software Engineering: Systematic Literature Review and Research Agenda

## 1. 快速结论卡片

| 字段 | 内容 |
|---|---|
| 标题 | LLM-Assisted Empirical Software Engineering: Systematic Literature Review and Research Agenda |
| 年份 | 2026 |
| 作者 / venue / 出版状态 | Victoria Gomes、Delaney Selb 等；arXiv:2604.26192; 本轮未核验正式 peer-reviewed / CCF 状态 |
| 分层 | P2 |
| 阅读状态 | 已读全文文本-paper_content核验 |
| 证据等级 | 全文文本级；图表/表格细节待人工 PDF 核对 |
| 核验入口 | [bibtex.bib](./bibtex.bib)、[paper_content.txt](./paper_content.txt) |
| 研究脉络 | 软件工程 / LLM4SE SLR 语境与方法学 |
| 引用角色 | 背景近邻 / 局部 claim 风险或禁用 claim 证据 |
| LLM/agent 角色 | LLM/agent 执行部分检索、筛选、抽取、组织、生成或评价环节；具体阶段见方法/覆盖阶段字段。 |
| 证据溯源粒度 | citation/来源归因 级；需复核是否能到 claim/page/table-cell。 |
| 输入 | 2020-2025 年 12 个软件工程会议/期刊中的论文全文，先下载 8,641 篇，再用 LLM 关键词做全文过滤。 |
| 输出 | 50 篇 primary studies、69 个 LLM-assisted ESE tasks、角色/阶段/收益/局限/可复现报告实践分类，以及研究议程。 |
| 方法/系统形态 | 软件工程领域的系统文献综述，不是 LLM/agent 自动执行 SLR 的工具。 |
| 覆盖阶段 | 作为 SLR 方法覆盖 venue 选择、全文关键词过滤、人工筛选、数据抽取、编码、综合和报告；作为研究对象，分析 LLM 在 ESE 生命周期中的任务分布。 |
| 不覆盖阶段 | 不覆盖 paper2 设想的完整 agent evidence workflow；主要提供 SE 场景或筛选/方法学边界。 |
| 人审/审计机制 | 两名研究者校准筛选与抽取，争议经讨论解决；提供 replication package 和数据可用性说明，但没有 claim-to-source 自动追踪系统。 |
| 人类角色 | 无正式人审 gate；若有评价者仅作实验评价 |
| 审计时机 | 原文未给出清晰审计时机或本轮未抽取 |
| 主张追踪状态 | 传统 SLR 人工校准与 replication package；无自动 claim-to-source trace。 |
| 决策日志状态 | 无或仅论文叙述 |
| 冲突处理机制 | 原文未给出明确冲突处理或不适用 |
| 审计导出性 | 不可导出或仅论文叙述；正式写作不得承诺可审计 artifact。 |
| 实验/指标 | 8,641 篇下载论文、1,882 篇关键词命中、80 篇候选、50 篇最终纳入；抽取 pilot 中 39 个编码决策、6 个分歧、84.6% agreement。 |
| 模型/API 设置 | 原文未给出或本轮未抽取模型清单 |
| 提示词状态 | 正文提到 prompt；完整模板待核验 |
| 温度/重复/随机种子 | 原文未给出或本轮未抽取 temperature / seed / repeats |
| 主要发现 | LLM 在 ESE 中主要用于分类、过滤和评价；集中在 data processing 与 analysis/synthesis；automation 占主导，decision support 很少；prompt、配置、human validation 等报告不完整。 |
| 关键结果锚点 | review.md §2 D1-D7 证据锚点 + §5/§6 实验与结果；SUMMARY 数字不得脱离单篇锚点引用 |
| 数值使用许可 | 仅文本级引用；正式写作前需 PDF 图表/表格核对 |
| 对 paper2 的作用 | 提供 SE 场景的背景证据和 research gap 支撑，尤其支持 paper2 强调 agentic workflow、人工审计、透明报告和 reproducibility；但它本身不是 agent-based SLR baseline。 |
| 受影响主张 ID | C4 |
| 威胁类型 | 背景定位 |
| 威胁的 paper2 主张 | 提供 SE 场景的背景证据和 research gap 支撑，尤其支持 paper2 强调 agentic workflow、人工审计、透明报告和 reproducibility；但它本身不是 agent-based SLR baseline。 |
| 支持的 paper2 主张 | 支持 paper2 采用 SE SLR/SMS 场景定位，并把透明报告、prompt/model 配置、人类验证和 reproducibility 作为论文主线。 |
| paper2 应避免的主张 | 避免写 SE 社区尚未讨论 LLM-assisted SLR/SMS；应改写为缺少面向 SE SLR/SMS 的可审计 agent evidence workflow。 |
| baseline 可用性 | 仅related-work背景或局部强近邻；不作为主流程可运行 baseline。 |
| 对比方式 | 仅related-work背景 |
| 代码状态 | 声称有/正文出现 GitHub 或 code 线索；本轮未打开核验 |
| 数据状态 | 声称有/正文出现 dataset 或 data availability 线索；license 未核验 |
| 许可状态 | 未核验；不得据此承诺可复现或可再分发 |
| 制品入口 | 本轮仅从 paper_content/review 识别线索；URL、commit、license 和 smoke 运行留待下一轮 artifact audit |
| 运行可行性 | 仅related-work背景 |
| 可复现资产 / 阻塞项 | 代码、数据、prompt、license、正式 venue/DOI 与 PDF 图表级数值均按 §7 / §10 待复核清单处理；未核验项不得支撑强实验比较。 |

## 2. D1-D7 全文核验评分

| D1 主题 | D2 流程 | D3 自动化 | D4 审计 | D5 评价 | D6 SE | D7 威胁 |
|---:|---:|---:|---:|---:|---:|---:|
| 🟡 | 🟠 | ⚪ | 🟡 | 🟢 | 🟢 | 🟠 |

| 维度 | 评分 | 全文证据锚点 | 判定理由 |
|---|---:|---|---|
| D1 主题贴合度 | 🟡 | `paper_content.txt:224-230`, `paper_content.txt:285-288`, `paper_content.txt:696-699` | 论文研究 LLM 如何支持 ESE research workflows，并明确包括 study screening、data extraction、qualitative coding、evidence synthesis、research reporting 等任务；但核心对象是 LLM-assisted ESE 的综述，不是专门提出 LLM/agent 执行 SLR 的系统。 |
| D2 SLR/SMS 流程覆盖度 | 🟠 | `paper_content.txt:572-583`, `paper_content.txt:817-830`, `paper_content.txt:832-835` | 文中把 SLR/SMS 作为 ESE 方法之一，映射 planning、searching、screening、data extraction/synthesis、reporting 等步骤，并报告 secondary studies 中已有 LLM 支持多个阶段；但这只是被综述对象的分类，不是本文实现的 SLR 自动化流程。 |
| D3 LLM/agent 自动化深度 | ⚪ | `paper_content.txt:202-210`, `paper_content.txt:362-364`, `paper_content.txt:1410-1419` | 作者自己的研究方法是人工主导 SLR 加 Python 全文关键词过滤，不使用 LLM/agent 执行多阶段 review。agentic AI 只在 future direction 中出现，不能算自动化深度证据。 |
| D4 人工审计与可追踪性 | 🟡 | `paper_content.txt:365-401`, `paper_content.txt:389-395`, `paper_content.txt:441-442`, `paper_content.txt:1612-1615` | 该 SLR 有人工校准、分歧讨论、结构化抽取表和 replication package，属于可复核的研究流程证据；但它没有报告级 claim-to-source trace、per-cell provenance 或 agent run record。 |
| D5 评价严谨性 | 🟢 | `paper_content.txt:433-441`, `paper_content.txt:688-690`, `paper_content.txt:1173-1189`, `paper_content.txt:1461-1526` | 有明确语料、筛选链条、编码流程、频次分析、透明度评估和 validity threats。虽然是二次研究而非系统实验，但证据链足以作为 SE 背景综述。 |
| D6 SE / CCF 相关性 | 🟢 | `paper_content.txt:15-16`, `paper_content.txt:324-337`, `paper_content.txt:1493-1507` | 直接面向 empirical software engineering，来源限定在 ICSE/FSE/EASE/MSR/ESEM/CAIN/SANER 及 EMSE/IST/JSS/TSE/TOSEM 等软件工程 venue。注意本地 BibTeX 是 arXiv 版本，不能写成已正式 CCF 发表。 |
| D7 对本文 novelty 的威胁强度 | 🟠 | `paper_content.txt:1340-1398`, `paper_content.txt:1410-1420`, `paper_content.txt:1603-1611` | 它不会威胁 paper2 的 agent 工作流 实现本身，但会约束 SE 语境下的 story：paper2 应正面承认 LLM-assisted ESE 已有综述，并把 novelty 收窄到可审计 agent 工作流、证据链和 人工审计 gate。 |

## 3. 论文解决的问题与背景

这篇论文关注的不是“如何自动生成一篇 SLR”，而是“LLM 已经如何被用于 empirical software engineering research”。作者认为 ESE 面临数据规模、方法复杂性和可复现性压力，传统自动化对需要语义解释、抽象和证据综合的任务支持不足。LLM 在分类、总结、推理、代码相关任务上表现突出，因此逐渐被当作 research instrument 使用，用来支持信息抽取、定性编码、大规模 evidence synthesis、study screening 等任务。

全文的核心 gap 是：已有 LLM4SE 综述多把 LLM 当作软件工程工具或被评测对象，例如代码生成、测试、修复、需求工程等；但缺少一个面向 ESE research workflow 的方法学综述，回答 LLM 支持哪些研究任务、分布在哪些生命周期阶段、以何种自动化/增强/决策支持/评价方式介入、带来哪些收益和风险，以及现有研究是否报告了足够的 prompts、model versions、configuration、human validation 等可复现信息。

## 4. 方法 / 系统拆解

输入是 2020-2025 年 12 个软件工程主流会议和期刊的论文全文。作者没有采用普通数据库检索串作为主路径，因为 LLM 支持 ESE research tasks 的信息常出现在 method section，而不一定出现在标题、摘要或关键词。实际流程是：先选定高质量 SE venues，手工下载完整 proceedings/期刊论文，再用 Python/PyMuPDF 对全文搜索 LLM 关键词，排除 references section，接着人工检查关键词命中是否真正满足 inclusion criteria。

输出是一个结构化 SLR 数据集和综合分析。数据抽取表包含 bibliographic info、ESE task、LLM model/version/type/configuration、prompt development、prompts 是否报告、open LLM baseline、human validation、experiment date、benefits、limitations 等字段。两名研究者先用小样本校准筛选和抽取规则，再分工处理剩余论文；不确定或模糊案例通过讨论解决。

LLM/agent 角色方面，本文没有让 LLM 执行自己的 review 流程。LLM 是被综述对象。作者把 primary studies 中的 LLM 角色抽象为 semantic classifier、criteria-based screener、evaluator、synthetic data generator、content transformer、pattern/relational analyst、structured data extractor、logic/consistency auditor、semantic mapper 等，并进一步按 automation、augmentation、decision support、evaluation 分析人机关系。

证据/日志/审计机制主要来自 SLR 方法学：全文关键词过滤脚本、结构化抽取表、校准流程、agreement 统计、replication package 和 data availability。它适合作为 paper2 run record/traceability 设计的反面参照：即便在传统人工 SLR 中，作者也要保存筛选链条、抽取表和编码决策；agentic SLR 更不能只保存最终回答。

## 5. 实验 / 评价设计

RQ 共五个：LLM 支持哪些 ESE tasks；支持哪些 ESE phases；如何集成到 ESE workflows；报告了哪些收益和局限；是否报告足以复现 LLM 使用的信息。数据源是 12 个 SE venues 中 2020-2025 年论文。筛选链条为 8,641 篇下载论文，经全文关键词过滤得到 1,882 篇，再人工检查到 80 篇候选，最终 full-text review 和 data extraction 后纳入 50 篇 primary studies。

评价不是模型实验，没有 LLM baseline、accuracy 或 F1。它的“指标”是综述编码与统计：69 个 LLM-assisted tasks、角色频次、研究方法/生命周期阶段分布、automation/augmentation/decision support/evaluation 占比、benefits/limitations thematic analysis、Q1-Q9 透明度与可复现性报告实践。人工标注方面，pilot extraction 覆盖 3 篇论文、39 个编码决策，6 个分歧，agreement 84.6%；随后剩余论文分工抽取，10 篇存在不确定或模糊点并经讨论解决。统计方式以描述性频次、交叉分布、thematic synthesis 和 narrative synthesis 为主。

## 6. 主要结果与结论

RQ1 显示，LLM 使用集中在结构化、决策导向任务。semantic classifier 有 17 个 tasks，criteria-based screener 有 14 个 tasks，evaluator 有 11 个 tasks。作者据此认为当前使用模式主要是分类、过滤和评价，复杂推理、跨域分析、integrative analysis 仍较少。

RQ2 显示，LLM-supported tasks 跨多个研究方法和阶段，但集中在 data processing 与 analysis/synthesis。MSR 和 controlled experiment/case study 中任务最多，SLR/SMS 处于中间位置。报告阶段几乎没有纳入的实证细节，部分论文只是声明使用 GenAI 写作而未说明具体环节，因此没有被计入。

RQ3 显示，automation 占 60.9%（42 tasks），augmentation 和 evaluation 各 18.8%（13 tasks），decision support 只有 1.5%（1 task）。这个结果对 paper2 很重要：现有 SE 研究更多把 LLM 当作“直接产出决策”的模块，而不是帮助人类研究者审慎决策的可解释协作组件。

RQ4 显示，收益常围绕效率、规模化、分析能力和 human-level alignment；但很多收益是引入 LLM 的先验理由，并不总是在具体研究中实证验证。局限集中在 hallucination/fabrication、classification errors、domain understanding、prompt sensitivity、token/API/cost constraints、inconsistency 和 reproducibility issues。

RQ5 显示，可复现报告不完整。基本的 LLM role 和 model version 较常报告，但 prompts、configuration、实验日期、open LLM baseline、human validation 过程等细节不稳定。作者强调这会把 prompt、参数和交互策略变成“隐藏方法层”，影响复现、解释和审稿。

## 7. 局限与可复现性

作者明确讨论了 construct/internal/external/reliability/conclusion validity。主要局限包括：范围限定在 curated SE venues 和 2020-2025 年，可能漏掉 workshop、preprint、新兴 venue 或窗口外研究；LLM-assisted ESE 的定义需要解释性判断；primary studies 自身报告不足，导致 prompt、配置、人类参与程度等字段只能保守编码；不同研究的数据集、LLM 配置和评价策略异质，不能做因果推断。

可复现性方面，全文声称数据公开在 GitHub repository，包含分析所用完整数据、抽取信息和结构化编码结果；全文关键词过滤代码也给了 GitHub release。当前本地阅读只核验了 `paper_content.txt`，未打开 PDF 图表，也未访问外部 replication package，所以关于图 1、图 6、图 11 的具体可视化细节和仓库文件完整性仍待复核。

## 8. 对 paper2 story / 实验设计的影响

第一，paper2 不能把 SE 社区对 LLM-assisted research workflow 的讨论写成空白。这篇综述已经给出 SE 语境下的系统性背景，并明确指出 classification、screening、evaluation、automation-centered integration 和 reporting gaps。

第二，paper2 的 novelty 应避免宽泛“LLM 支持 ESE/SLR”表述，而应落在更窄的组合：面向 SE SLR/SMS 的 agentic multi-stage workflow、阶段化 run record、claim-to-source trace、人审门和 unsupported claim 控制。

第三，实验设计可以直接吸收这篇论文的风险清单：prompt/configuration/date/model version/human validation 必须进入 run record；评价不能只报任务性能，还要衡量透明度、可复现性、人工审计成本、错误可定位性和 decision support 质量。

## 9. 可用于写作的引用角度

1. 可作为 SE 领域背景引用：已有综述表明 LLM 在 ESE 中多集中于分类、筛选和评价等结构化任务，decision-support 使用很少。
2. 可作为 motivation 引用：LLM-assisted ESE 的透明度和可复现报告仍不完整，prompt、配置和 human validation 细节常被省略。
3. 可作为 story 收窄依据：agentic AI 被作者列为未来方向，尤其是 planning、tool integration 和 multi-step execution，而非已被充分解决的常规实践。
4. 不应把它写成 automated SLR system baseline；它更适合放在 SE-context related work 和 methodology risk 部分。

## 10. 待复核清单

1. 当前只读 `paper_content.txt`，未回 PDF 核对图表；图 1、图 6、图 11 的视觉细节待核对。
2. BibTeX 是 arXiv 元数据，需后续核验是否已有正式 venue/DOI，不得提前写成 CCF/peer-reviewed 事实。
3. 外部 replication package 和 keyword-search GitHub release 尚未打开，数据字段和文件可用性需后续核验。
4. 原文在 related work/结论中有较强自我定位；paper2 写作不要扩展为更宽的 unsupported novelty claim。
