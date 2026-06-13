# LatteReview: A Multi-Agent Framework for Systematic Review Automation Using Large Language Models

## 1. 快速结论卡片

| 字段 | 内容 |
|---|---|
| 标题 | LatteReview: A Multi-Agent Framework for Systematic Review Automation Using Large Language Models |
| 年份 | 2025 |
| 分层 | P0 |
| 阅读状态 | 已读全文文本-paper_content核验 |
| 证据等级 | 全文文本级；图表/表格细节待人工 PDF 核对 |
| 核验入口 | [bibtex.bib](./bibtex.bib)、[paper_content.txt](./paper_content.txt)、[paper.pdf](./paper.pdf)；未人工逐页打开 PDF 图表 |
| 输入 | 文献标题、摘要、可选图像/多模态输入、纳入/排除标准、用户自定义 schema、可选 RAG 上下文 |
| 输出 | dataframe 增强列、结构化 JSON、评分、理由、certainty、抽取字段、工作流中间结果 |
| 方法/系统形态 | Python 包；LLM provider + reviewer agents + ReviewWorkflow 的多 agent 工作流框架 |
| 覆盖阶段 | 标题/摘要筛选、相关性评分、结构化抽取、条件过滤、并行/串行 reviewer 协作；不覆盖正式报告写作全流程 |
| 人审/审计机制 | 有 senior reviewer 裁决、用户反馈迭代、Pydantic 结构校验、reasoning/certainty 字段；未见 claim-to-source 或逐单元 provenance 证据包 |
| 实验/指标 | SYNERGY 六个数据集 + 自定义心胸影像 scoping review 数据；AUC、accuracy、recall、precision；给出运行成本/速度示例 |
| 主要发现 | SYNERGY AUC 约 0.77--0.95，自定义数据 AUC 约 0.79--0.94；性能强依赖纳入/排除标准清晰度和阈值设定 |
| 对 paper2 的作用 | 强 baseline：直接威胁“多 agent SLR screening/extraction 工作流”claim；paper2 需要把 SE 场景、run record、claim-to-source audit 与失败分类作为差异化 |
## 2. D1-D7 全文核验评分

emoji 口径见 [../../GUIDE.md](../../GUIDE.md)；本表单元格只放 emoji。

| D1 主题 | D2 流程 | D3 自动化 | D4 审计 | D5 评价 | D6 SE | D7 威胁 |
|---|---|---|---|---|---|---|
| 🟢 | 🟡 | 🟢 | 🟡 | 🟢 | 🟠 | 🟢 |

| 维度 | 评分 | 全文证据锚点 | 判定理由 |
|---|---:|---|---|
| D1 主题贴合度 | 🟢 | `paper_content.txt` Page 1 lines 210--530；Page 10 起 `Evaluation` | 论文明确面向 systematic review / meta-analysis 自动化，目标任务就是标题摘要筛选、评分和抽取，主题与 paper2 的 baseline 库高度贴合。 |
| D2 SLR/SMS 流程覆盖度 | 🟡 | `paper_content.txt` Page 1 lines 352--370；Page 6--8 `TitleAbstractReviewer` / `AbstractionReviewer` / `ReviewWorkflow` 附近；Page 10--16 evaluation | 覆盖 screening、scoring、structured extraction、multi-reviewer workflow 和 conditional filtering，达到 2--3 个核心环节；未见检索策略生成、编码综合、最终报告写作的完整 SLR 生命周期实现，因此不评 🟢。 |
| D3 LLM/agent 自动化深度 | 🟢 | `paper_content.txt` Page 4--8 附近 `TitleAbstractReviewer`、`AbstractionReviewer`、`ReviewWorkflow`；Page 26--30 workflow code examples | 有 provider、agent、workflow 三层架构；支持串行/并行 reviewer、junior/senior 裁决、动态过滤和 RAG/多模态上下文，具备明确输入输出链。 |
| D4 人工审计与可追踪性 | 🟡 | `paper_content.txt` Page 1 lines 396--412；Page 19--20 validation / human oversight practical tips | 有用户反馈、senior reviewer、人类小样本验证和 Pydantic 结构校验，也输出 reasoning/certainty；但没有看到 claim-to-source trace、per-cell provenance、审计日志或可导出证据包。 |
| D5 评价严谨性 | 🟢 | `paper_content.txt` Page 10--16；Table 2、Table 4；GitHub line 10331 | 使用 SYNERGY collection 六个真实 review 数据集和自定义数据集，报告 AUC/accuracy/recall/precision，并给出阈值策略、成本与速度；评价比普通 demo 更扎实。 |
| D6 SE/CCF 相关性 | 🟠 | `bibtex.bib` arXiv cs.CL；正文数据主要来自医学/影像 review | 这是泛科学/医学系统综述自动化工具，不是 SE/CCF venue，也不直接面向软件工程 SLR；只能作为跨域方法学强 baseline。 |
| D7 对本文 novelty 的威胁 | 🟢 | `paper_content.txt` Page 1 lines 278--498；Page 12--16 evaluation | 已覆盖多 agent reviewer workflow、筛选/抽取、结构化输出和真实数据评价，对 paper2 的 agent workflow 与 screening/extraction claim 构成直接威胁；paper2 必须转向 SE-specific evidence chain 和审计协议差异化。 |

## 3. 论文解决的问题与背景

论文的问题设定是：系统综述和 meta-analysis 需要反复筛选标题摘要、评估相关性、抽取数据，人工成本高且协议变化会导致大量返工。作者把 LatteReview 定位为 Python-based framework，用 LLM 和 multi-agent system 自动化系统综述中的关键工作。

全文背景强调两点。第一，系统综述的人工流程本身需要多个 reviewer、纳入/排除标准、分轮裁决和可重复执行，适合被抽象为 reviewer agents 与 workflow。第二，LLM 的能力需要被封装成可配置、可验证、可组合的模块，而不是单次聊天提示。因此论文重点不是提出一个固定 review 结果，而是提供一个可组装的 review automation package。

## 4. 方法 / 系统拆解

输入层包括 Pandas dataframe 中的原始文献数据、标题、摘要、可选图像、纳入/排除标准、任务说明、抽取 schema 和可选 additional context。输出层是增强 dataframe：每轮 reviewer 的分数、理由、certainty、抽取字段和后续 round 使用的中间结果。

系统有三类核心组件。Providers 统一 OpenAI、Ollama、LiteLLM 等 provider 接口，降低模型切换成本。Reviewer Agents 包括 `ScoringReviewer`、`TitleAbstractReviewer`、`AbstractionReviewer` 和 `CustomReviewer`，分别负责评分、标题摘要筛选、结构化抽取和用户自定义任务。Workflows 负责 round、依赖、并行 reviewer、动态过滤和结果聚合。

LLM/agent 角色比较清楚：junior reviewer 可用低成本模型并行筛选，senior reviewer 在分歧或不确定时介入，abstraction agent 对选中文献做结构化字段抽取。人机协作主要体现在用户设计 criteria、选择 reviewer 组合、校准阈值、提供反馈和小样本验证。证据/日志层面，论文提到 Pydantic validation、structured JSON、reasoning 和 certainty；但没有证明每个抽取结论都保留到原文句子、页码或表格单元的 provenance。

## 5. 实验 / 评价设计

原文没有以 RQ 编号组织实验，但评价目标很明确：验证 LatteReview 在系统综述标题/摘要筛选任务上的可用性和性能。

第一组数据是 SYNERGY collection，包含六个既有系统综述数据集及其原始纳入/排除标准。作者使用 `TitleAbstractReviewer` 代表性工作流：两个 junior reviewers 分别由 Gemini-1.5-flash 和 GPT-4O-mini 支持；当 junior 分数不同或都给 3 时，GPT-4O senior reviewer 做最终裁决。评分采用 1--5 Likert，阈值策略包括 sensitive、specific 和 balanced。指标包括 accuracy、recall、precision 和 AUC。

第二组数据来自作者既有心胸影像 scoping reviews，自定义三组逐渐复杂的纳入/排除标准。论文报告三种策略下的 performance，并说明更清晰的 prompt/criteria 会带来更稳定的 reviewer 分数。原文还给出一个成本和速度观测：使用两个 junior reviewers 评审 1000 对标题摘要约 1 分钟、成本约 1.20 美元。该数字只能作为作者实验设置下的参考，不能外推到所有 provider 或论文全文抽取场景。

## 6. 主要结果与结论

SYNERGY 六个数据集上的 AUC 约为 0.77 到 0.95，但 precision/recall 随阈值和数据集严重波动。低纳入率数据集中，sensitive threshold 能保 recall，但 precision 很低；specific threshold 可提高 precision，但会牺牲 recall。这说明 LatteReview 不是“自动替代 reviewer”，而是提供可校准的筛选工作流。

自定义数据集上，三组策略的 AUC 约为 0.79、0.82、0.94。作者解释为：清晰、结构化的 criteria 更适合 LLM reviewer 执行，balanced/specific 策略表现更接近。结论部分强调 LatteReview 的价值在于 customizable multi-agent workflow、provider 兼容、RAG/多模态扩展和实际 review 降本增效潜力。

## 7. 局限与可复现性

可复现性方面较强：摘要和正文都说明 GitHub repository、documentation、installable package；正文还提到 repository 包含 datasets、evaluation code 和 workflow configurations。仍需后续人工核查仓库当前状态、license、数据下载方式和版本 tag。

局限方面，作者自己承认 framework 灵活性导致评价困难；不同 workflow、agent 数量、模型选择和阈值都会改变结果。SYNERGY 中 inclusion/exclusion criteria 的异质性和模糊性显著影响性能。人工审计机制仍停留在 sample validation、senior reviewer 和 human oversight 建议层面，没有完整 claim-to-source audit trail。该文是 arXiv 技术报告，不能按 peer-reviewed CCF/SE 论文处理。

## 8. 对 paper2 story / 实验设计的影响

paper2 不能再把“LLM 多 agent 支持系统综述筛选/抽取”写成宽泛 novelty。LatteReview 已经提供了多 agent reviewer、junior/senior 裁决、结构化输出和公开评价。

paper2 应将差异化压到更细的证据链：面向 SE/AI4SE 文献场景；每个 claim、抽取字段、分类决策都有 source span/page/table provenance；run record 保存 prompt、model、usage、错误、重试和 human audit decision；评价不仅看 AUC/accuracy，也看 hallucination/error taxonomy、audit workload、复核成本和 downstream writing correctness。

实验上，LatteReview 可以作为 workflow baseline 或 design baseline。若 paper2 做 screening/extraction，应比较相同数据集、相同纳入/排除标准、相同 LLM budget 下的 recall/precision、uncertain-case routing、人工复核负担和 provenance completeness。

## 9. 可用于写作的引用角度

- LatteReview 可作为近期 LLM multi-agent 系统综述自动化工具代表，说明筛选、评分和结构化抽取已经能通过 configurable reviewer workflow 实现。
- 可用它支撑“现有工具强调 reviewer orchestration 与 structured outputs，但通常缺少 claim-to-source 级证据包和面向 SE 综述写作的审计闭环”这一定位。
- 可在实验设计中引用其 junior/senior reviewer 和 threshold calibration 思路，作为 paper2 human audit gate 的对照。
- 不应把 paper2 写成“首个 agentic SLR 工具”；更稳妥的说法是 paper2 聚焦 SE 文献综述中的 evidence-traceable review generation 和审计记录。

## 10. 待复核清单

- 人工打开 PDF 图表，核对 Table 2、Table 4、Figure 4、Figure 5 的数值和阈值方向是否与 `paper_content.txt` 提取一致。
- 打开 GitHub 仓库，核实代码、数据、workflow config、license、tag 和最近更新时间。
- 检查是否已有正式出版版本；当前只按 arXiv 技术报告处理。
- 若用于实验 baseline，需确认 `lattereview` 包当前 API 是否与论文一致，并记录具体版本。
