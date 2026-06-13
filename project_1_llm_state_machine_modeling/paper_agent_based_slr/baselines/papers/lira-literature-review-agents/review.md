# LiRA: A Multi-Agent Framework for Reliable and Readable Literature Review Generation

## 1. 快速结论卡片

| 字段 | 内容 |
|---|---|
| 标题 | LiRA: A Multi-Agent Framework for Reliable and Readable Literature Review Generation |
| 年份 | 2025 |
| 分层 | P0-报告生成与 citation-quality 强近邻 |
| 阅读状态 | 已读全文文本-paper_content核验 |
| 证据等级 | 全文文本级；图表/表格细节待人工 PDF 核对 |
| 核验入口 | [bibtex.bib](./bibtex.bib)、[paper_content.txt](./paper_content.txt)；未人工打开 PDF 图表 |
| 输入 | 综述主题、参考文献标题/摘要或全文；实验中主要使用给定 gold references，另有 retrieval setting |
| 输出 | 长篇 literature review，包括 outline、正文、标题、摘要、结论、编号引用 |
| 方法/系统形态 | LangGraph 多 agent 写作流水线：outline drafter、subsection writer、editor、reviewer、citation grounding/post-processing |
| 覆盖阶段 | 结构规划、分节写作、编辑、LLM reviewer 反馈、citation grounding、有限 retrieval；不覆盖完整检索策略、筛选、risk-of-bias 或数据抽取 |
| 人审/审计机制 | Reviewer agent 按改写的 SLR guideline 给反馈；SME 做输出偏好/打分；引用质量用 CQF1 评估。未见 claim-to-source 审计包或人工裁决日志 |
| 实验/指标 | SciReviewGen 125 篇、ScienceDirect internal 125 篇；DP、MASS-Survey、AutoSurvey；ROUGE、hsr/her/aer、Prometheus 2 writing quality、SME evaluation、CQF1、retrieval ablation |
| 主要发现 | LiRA 在 ROUGE、平均写作质量和 CQF1 上整体领先；AutoSurvey 在部分 recall 类指标上因输出更长占优；retrieval setting 中仅少数指标显著下降 |
| 对 paper2 的作用 | 必须作为 agentic survey/report generation 强 baseline；paper2 若主张多 agent 生成综述，需避开“只做写作质量和引用质量”的已覆盖区域，强调 SE 场景、可审计证据链和更完整 SLR 流程 |
## 2. D1-D7 全文核验评分

emoji 口径：🟢 强，🟡 中，🟠 弱，⚪ 无 / 背景。

| D1 主题 | D2 流程 | D3 自动化 | D4 审计 | D5 评价 | D6 SE | D7 威胁 |
|---|---|---|---|---|---|---|
| 🟢 | 🟡 | 🟢 | 🟡 | 🟢 | 🟠 | 🟢 |

| 维度 | 评分 | 全文证据锚点 | 判定理由 |
|---|---:|---|---|
| D1 主题贴合度 | 🟢 | Abstract；§1 Introduction；§3 The LiRA Framework | 论文直接研究 LLM 多 agent 自动生成 literature review，并把问题放在 SLR 写作阶段不足、可读性和事实准确性语境下。 |
| D2 SLR/SMS 流程覆盖度 | 🟡 | §3.1 outline、§3.2 subsection writing、§3.4 reviewer、§5.2 retrieval、§7 limitations | 覆盖结构规划、综合写作、编辑、引用和有限 retrieval，但 §7 明确当前未覆盖 primary studies、risk of bias、screening 和 search criteria definition，因此不能评为完整流程。 |
| D3 LLM/agent 自动化深度 | 🟢 | §3.1-§3.6；LangGraph implementation | 多个专门 agent 串联并带反馈、记忆、并行写作、引用 grounding，输入输出链条明确，属于实质性 agent workflow。 |
| D4 人工审计与可追踪性 | 🟡 | §3.4 Reviewer Agent；§3.5 Citation Behavior；§4.2 SME evaluation；Appendix D CQF1 | 有 LLM reviewer、引用标题锚定、CQF1 和专家评价，但没有逐 claim/page provenance、人工裁决日志或可导出的 audit packet；只能算中等审计能力。 |
| D5 评价严谨性 | 🟢 | §4.1 baselines；§4.2 metrics；§4.3 datasets；Tables 1-5 | 两个数据集、多个公开 baseline、自动与人工指标、retriever 变体和不同 reviewer model 检查，实验设计较扎实；局限是 ScienceDirect 数据集不可公开。 |
| D6 SE / CCF 相关性 | 🟠 | bibtex: arXiv cs.CL；§4.3 数据集为 CS/ScienceDirect 泛学科 | 该文是 NLP/ASG 方向，不是软件工程 SLR，也未给 CCF/peer-reviewed 版本证据；只能作为跨域方法学 baseline。 |
| D7 对本文 novelty 的威胁强度 | 🟢 | §3 multi-agent writing；§4 baselines/results；§7 future work | 对 paper2 的“agent-based literature review generation、citation quality、writer-reviewer loop”构成强威胁；但 paper2 可从完整 SLR/SMS 流程、SE 任务、claim-level 审计和可复现实验记录区分。 |

## 3. 论文解决的问题与背景

LiRA 关注的是 SLR/literature review 中“已有参考文献之后如何生成高质量综述文章”的问题。作者指出，既有自动化研究更多聚焦检索与筛选，而把发现整理成可读、事实可靠的 review paper 仍然不足。论文因此把目标收窄到写作阶段：在不给任务专门训练或微调的前提下，通过多 agent 分工提升结构、可读性和引用可靠性。

这个定位对 paper2 很关键：LiRA 不是完整 SLR 自动化系统，而是写作/报告生成系统。它可以证明“多 agent 写综述”已经是强近邻，但不能替代检索协议、筛选决策、证据抽取、风险评估和人类审计等 SLR/SMS 全流程证据。

## 4. 方法 / 系统拆解

输入包括主题以及参考文献的标题、摘要或全文。Outline Drafter 先根据最多 50 篇参考文献生成候选 outline 并合并成统一结构；Subsection Writer 按 subsection 描述用 FAISS 检索相关参考材料，逐节写约 1000 词；Editor 改善连贯性、风格和过渡，但声称不改变事实内容；Reviewer Agent 参考 SLR guideline 对 outline 或 section 给结构化反馈，最多 3 轮；Citation Behavior 模块要求用完整文章标题作为语义锚，生成后再转为标准编号引用，并在评价时 redaction 幻觉标题。

LLM/agent 角色是强项：每个 agent 有独立记忆，LangGraph 负责编排，结构化文档和 message pool 用于通信。人机协作主要出现在评价阶段的 SME 打分，而不是生成过程中的 human gate。证据/日志层面，论文有 citation grounding 和 CQF1，但没有保存到 claim-level provenance 的机制；这与 paper2 想要做证据级审计时应明确区分。

## 5. 实验 / 评价设计

论文提出 4 个 RQ：与人写综述相似度、写作质量、引用使用质量、retrieval 场景下能否工作。Baseline 包括 direct prompting、MASS-Survey 和 AutoSurvey，且统一使用 `gpt-4o-mini` 以控制模型差异。数据集为 SciReviewGen 中抽样 125 篇 review，以及 125 篇公司内部 ScienceDirect expert-written reviews。

指标分三类：与人写综述的相似度用 ROUGE-L、heading soft recall、heading entity recall、article entity recall；写作质量用 Prometheus 2 的 coverage/structure/relevance，并辅以 SME 评价；引用质量用 Citation Quality F1。额外实验包括 reviewer 使用 `gemma3:4b` 的模型变体和使用内部 embedding retrieval API 的真实检索设置。统计显著性只在 retrieval setting 中简要报告，细节放在 appendix，全文未给完整复现实验包证据。

## 6. 主要结果与结论

Table 1 显示 LiRA 在两个数据集 ROUGE 上最好或并列最好，但 AutoSurvey 在 hsr/her/aer 等 recall 类结构指标上更高，作者解释主要来自 AutoSurvey 输出更长。Table 2 中 LiRA 的平均 writing quality 在 SciReviewGen 和 ScienceDirect 均最高，结构维度尤其突出。Table 3 的 CQF1 中 LiRA 分别达到 0.76 和 0.73，高于 AutoSurvey 及其他 baseline，支持其 citation-grounded 设计。

Table 4 显示把 reviewer model 换成 `gemma3:4b` 后总体指标差异很小；Table 5 的 retrieval setting 中，aer 和 coverage 显著低于 gold-reference setting，其余指标没有明显下降。结论可以保守写成：LiRA 在给定参考文献或检索参考文献条件下，对长篇综述写作质量和引用可靠性有强实证表现。

## 7. 局限与可复现性

作者在 §7 明确承认 `gpt-4o-mini` 导致结果不可完全复现，且缺少更多开放数据集限制了跨学科泛化。ScienceDirect 数据集是内部数据，内部 retrieval API 也不可复验。当前系统没有处理 primary studies、risk of bias、search criteria definition 和 screening，因此不能被写成完整 SLR 自动化。

可复现性方面，方法描述、baselines 和指标较清楚，但 prompt、完整运行记录、SME 原始标注、内部数据和检索 API 未在 `paper_content.txt` 中明确给出公开入口。写作时不能把该文称为提供完整可审计证据链。

## 8. 对 paper2 story / 实验设计的影响

LiRA 会直接压缩 paper2 在“多 agent 综述写作”和“citation quality”上的 novelty 空间。paper2 如果也做 report generation，必须至少比较 LiRA 或复刻其关键思想：outline planning、section-level writer、reviewer loop、citation grounding，以及 CQF1/写作质量指标。

更好的 story 是把 paper2 定位为：面向 SE SLR/SMS 的 agentic evidence workflow，而不是单纯自动写综述。差异应落在可追踪筛选决策、结构化 evidence extraction、claim-to-source 审计、人类复核记录、run record 和 SE benchmark 上。实验上可借用 LiRA 的写作质量/CQF1 指标，但要新增 process-level correctness 和 auditability 指标。

## 9. 可用于写作的引用角度

可引用为“近期自动 literature review 写作系统已经采用多 agent 分工和 reviewer loop，并在 SciReviewGen 等数据集上系统评估写作质量与引用质量”。也可引用为“现有强系统主要聚焦 report writing，而作者自己承认完整 SLR 中的 screening、search criteria 和 risk-of-bias 等环节仍未纳入”。

不应引用为“首个 agentic SLR 系统”或“完整自动 SLR 流程”。作者贡献段落中有类似强 novelty 表述，但在 paper2 中应避免复述成事实。

## 10. 待复核清单

- 是否存在正式 AAAI/peer-reviewed 版本，以及版本与 arXiv v4 是否一致。
- LiRA 是否公开代码、prompt、SME annotation 和 ScienceDirect 数据替代入口。
- CQF1 的人工/自动标注细节在 Appendix D 中是否足以复现。
- AutoSurvey 修改版是否会影响 baseline 公平性。
- 若 paper2 实验纳入 LiRA，需确认其运行成本、context window、附件读取和 retrieval API 替代方案。
