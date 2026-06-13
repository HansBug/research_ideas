# Agentic AutoSurvey: Let LLMs Survey LLMs

## 1. 快速结论卡片

| 字段 | 内容 |
|---|---|
| 标题 | Agentic AutoSurvey: Let LLMs Survey LLMs |
| 年份 | 2025，arXiv:2509.18661 |
| 作者 / venue / 出版状态 | Yixin Liu、Yonghui Wu 等；arXiv:2509.18661; 本轮未核验正式 peer-reviewed / CCF 状态 |
| 分层 | P2 |
| 近邻强度备注 | 多 agent survey 生成 近邻；因目标是 broad academic survey 生成 而非 SLR/SMS 全流程，SUMMARY 保持 P2。 |
| 阅读状态 | 已读全文文本-paper_content核验 |
| 证据等级 | 全文文本级；图表/表格细节待人工 PDF 核对 |
| 核验入口 | `bibtex.bib`；`paper_content.txt` Page 1--29；已清理 PDF 提取残留 NUL 后阅读 |
| 研究脉络 | 自动 survey / literature review 生成与评价 |
| 引用角色 | 背景近邻 / 局部 claim 风险或禁用 claim 证据 |
| LLM/agent 角色 | LLM/agent 执行部分检索、筛选、抽取、组织、生成或评价环节；具体阶段见方法/覆盖阶段字段。 |
| 证据溯源粒度 | 人工核验或 benchmark/gold 级；未必有 claim-level provenance。 |
| 输入 | 用户研究主题；Semantic Scholar 与 arXiv 检索结果；论文标题、摘要、年份、引用数等元数据 |
| 输出 | 自动生成的长篇 survey、聚类报告、12 维 agent-as-judge 质量评估结果 |
| 方法/系统形态 | Claude Code 编排的四 agent 流水线：Paper Search Specialist、Topic Mining & Clustering、Academic Survey Writer、Quality Evaluator |
| 覆盖阶段 | 查询扩展、检索、去重、质量过滤、语义聚类、survey 写作、自动质量评价；未覆盖 SLR/SMS 的人工筛选、编码、抽取表和报告级证据审计 |
| 不覆盖阶段 | 不覆盖 SLR/SMS 的双人筛选、纳入/排除审计、抽取表、编码协议、质量评价和系统综述级报告审计。 |
| 人审/审计机制 | 无正式 人工审计 gate；有 Quality Evaluator agent、引用覆盖目标、缓存和重试；附录给出 subagent prompt，但部分参考文献元数据仍标为待补 |
| 人类角色 | 运行中审查者或用户反馈；需区分是否为正式审计 gate |
| 审计时机 | 运行前 + 运行后复核 |
| 主张追踪状态 | 引用覆盖与 evaluator 线索；无正式 claim-to-source ledger 或人工审计 gate。 |
| 决策日志状态 | 无或仅论文叙述 |
| 冲突处理机制 | 原文未给出明确冲突处理或不适用 |
| 审计导出性 | 有表格/JSON/schema 输出线索；是否形成可审计证据包待 artifact audit。 |
| 实验/指标 | 6 个 COLM 2024 LLM 主题，75--443 篇/主题，847 篇总量；与 AutoSurvey 对比；12 维评分聚合为 Core/Writing/Depth；报告 8.18/10 vs 4.77/10 |
| 模型/API 设置 | Claude、Sonnet、Opus、Llama、Meta-Llama；具体版本/调用日期按原文与 artifact 待复核 |
| 提示词状态 | 附录/正文给出 prompt 或片段；完整可复用性待核验 |
| 温度/重复/随机种子 | 原文未给出或本轮未抽取 temperature / seed / repeats |
| 主要发现 | 多 agent 分工在自动评分中优于 AutoSurvey；大语料主题 RLHF 出现 1334 检索但仅 80 引用的瓶颈；人类深层批判分析仍被作者列为不足 |
| 关键结果锚点 | review.md §2 D1-D7 证据锚点 + §5/§6 实验与结果；SUMMARY 数字不得脱离单篇锚点引用 |
| 数值使用许可 | 仅文本级引用；正式写作前需 PDF 图表/表格核对 |
| 对 paper2 的作用 | 可作为“多 agent 生成 survey”强近邻，提醒 paper2 必须把 novelty 放在 SLR/SMS workflow、run record、人审 gate、claim-to-source 证据链，而非泛称 agentic survey writing |
| 受影响主张 ID | C1,C5,C6,C7 |
| 威胁类型 | 局部覆盖 + 禁用 claim 证据 |
| 威胁的 paper2 主张 | 可作为“多 agent 生成 survey”强近邻，提醒 paper2 必须把 novelty 放在 SLR/SMS workflow、run record、人审 gate、claim-to-source 证据链，而非泛称 agentic survey writing |
| 支持的 paper2 主张 | 支持 paper2 把报告生成 claim 收窄为“生成必须可审计”，并把 citation validity、unsupported claim 和 有证据支撑的断言 纳入评价。 |
| paper2 应避免的主张 | 避免声称自动 survey / review generation 尚无人研究；避免把文本流畅度、引用准确率或 LLM-as-Judge 总分等同于 SLR/SMS 方法学可靠性。 |
| baseline 可用性 | 仅related-work背景或局部强近邻；不作为主流程可运行 baseline。 |
| 对比方式 | 仅related-work背景 / survey生成局部近邻 |
| 代码状态 | 未提及本研究源码；正文 GitHub 命中来自参考文献/背景项，不得当作 artifact 入口 |
| 数据状态 | 未提及可复用数据入口；只描述检索到的 Semantic Scholar / arXiv 运行数据 |
| 许可状态 | 未核验；不得据此承诺可复现或可再分发 |
| 制品入口 | 本轮仅做 paper_content 文本级线索识别，未打开外部 URL；具体 URL、commit、license 和 smoke 运行留待下一轮 artifact audit |
| 运行可行性 | 仅related-work背景 / survey生成局部近邻 |
| 可复现资产 / 阻塞项 | 代码、数据、prompt、license、正式 venue/DOI 与 PDF 图表级数值均按 §7 / §10 待复核清单处理；未核验项不得支撑强实验比较。 |

## 2. D1-D7 全文核验评分

| 维度 | 评分 |
|---|---|
| D1 主题贴合度 | 🟢 |
| D2 SLR/SMS 流程覆盖度 | 🟡 |
| D3 LLM/agent 自动化深度 | 🟢 |
| D4 人工审计与可追踪性 | 🟠 |
| D5 评价严谨性 | 🟡 |
| D6 SE / CCF 相关性 | 🟠 |
| D7 对本文 novelty 的威胁强度 | 🟡 |

| 维度 | 评分 | 全文证据锚点 | 判定理由 |
|---|---|---|---|
| D1 | 🟢 | `paper_content.txt` Page 1 摘要；Page 2 Introduction | 论文直接研究 LLM/agent 自动生成学术 survey，问题设定与 automated literature survey 生成 高度贴合。 |
| D2 | 🟡 | Page 2--5 系统架构；Page 25--29 subagent prompts | 覆盖检索、聚类、综合写作和评价，但没有 SLR/SMS 的纳入排除流程、双人筛选、抽取表、编码和正式综述报告约束。 |
| D3 | 🟢 | Page 2--5 四类 agent；Page 25--29 Task prompt | 四个专门 agent 分工明确，包含输入输出、检索、聚类、写作和评价任务，是实质性多阶段 agent 工作流。 |
| D4 | 🟠 | Page 6 evaluator；Page 9 broader impact；Page 16--19 reference list note | 只有 agent-as-judge 和引用覆盖目标；没有人工复核流程、claim-to-source 审计包或逐条决策日志。参考列表中多条还写着作者元数据待补，说明证据链未闭合。 |
| D5 | 🟡 | Page 5--8 实验；Table 2；Page 20--24 附录统计 | 有 6 个主题、baseline 和指标，但核心结论依赖自动 evaluator，AutoSurvey baseline 因预算被替换底层模型，缺少人类专家评价和显著性分析。 |
| D6 | 🟠 | `bibtex.bib` primaryClass cs.IR；Page 5 主题均为 LLM research | arXiv 预印本，主要面向 LLM 研究 survey 生成；与软件工程 SLR 或 CCF SE venue 没有直接绑定。 |
| D7 | 🟡 | Page 1--2 contributions；Page 25--29 prompts | 对 paper2 的“agent 化多阶段生成”和“自动质量评价”有局部威胁，但不覆盖 SLR/SMS 证据抽取、人审 gate、run record 和 report-level claim traceability。 |

## 3. 论文解决的问题与背景

论文的出发点是 LLM 领域文献增长过快，传统人工 survey 难以及时覆盖快速变化主题。作者认为已有 AutoSurvey、SurveyAgent、PaSa、LitSearch 等系统仍存在 synthesis 不足、引用覆盖有限、评价维度简单、缺少专门 agent 协作等问题。论文因此把问题定义为：如何用多 agent 架构把检索、主题组织、长文 survey 写作和质量评价拆成可执行的自动化流程。

需要注意的是，原文讨论的是 broad academic survey 生成，而不是严格意义上的 systematic literature review 或 systematic mapping。它没有定义研究问题、检索式审计、纳入/排除标准、质量评价表、编码协议或证据综合表。因此它适合支撑 paper2 的 related work 背景，但不能作为“已有工作已完成 agent-based SLR”的证据。

## 4. 方法 / 系统拆解

输入是一个研究主题。Paper Search Specialist 先生成 20--30 个查询变体，并通过 Semantic Scholar 与 arXiv 检索，使用 90% 标题相似度去重，再按年份、摘要完整性、引用阈值和 venue 质量过滤。Topic Mining & Clustering agent 使用 all-MiniLM-L6-v2 将标题和摘要编码成 384 维向量，用 K-means 和 silhouette score 在 5--15 个 K 值间选簇，并用 TF-IDF 生成簇名。

Academic Survey Writer 根据簇组织写作，目标 8000--12000 词，要求至少 50% 引用覆盖并尽量超过 80%，强调跨簇比较、趋势识别、方法差异和 gap。Quality Evaluator 使用 12 个维度评价，分为 Core Quality、Writing Quality、Content Depth 三类。附录 K 给出了四个 subagent 的 Claude Code Task prompt，包括检索 JSON 输出、聚类结构、写作要求和评价 JSON 输出。

证据/日志方面，论文提到 API cache、embedding cache、cluster cache、rate limit backoff 和 progress persistence，但没有给出可复现实验 run record schema。输出端包含聚类报告、生成的 survey、12 维评价 JSON 预期路径。人机协作方面，正文没有描述人类专家在生成中间环节介入，只在 broader impact 中建议自动 survey 应标注 AI 生成并经过人类专家验证。

## 5. 实验 / 评价设计

原文未以 RQ1/RQ2 形式列出研究问题。实验目标是比较 Agentic AutoSurvey 与 AutoSurvey baseline 在自动 survey 质量上的差异。数据集为 6 个 COLM 2024 类别主题：Instruction Tuning、LLM Agents、RLHF Alignment、Synthetic Data、In-Context Learning、Multimodal LLM RL。每个主题检索 75--443 篇不等，总计 847 篇。

baseline 是 AutoSurvey，但作者说明由于预算限制，复现中将底层模型替换为 Meta-Llama-3.1-8B-Instruct。本文系统使用 Claude Sonnet 4.1 做 search subagent，Claude Opus 4.1 做其余 subagent。评价不是人工评审，而是 enhanced-survey-evaluator agent，在 Citation Coverage、Accuracy、Synthesis Quality、Organization、Readability、Academic Rigor、Clarity、Coherence、Comprehensiveness、Critical Analysis、Novelty & Insights、Future Directions 十二维上给 0--10 分，并聚合为 Core/Writing/Depth。

## 6. 主要结果与结论

Table 2 报告 Agentic AutoSurvey 平均 8.18/10，AutoSurvey baseline 为 4.77/10；Core/Writing/Depth 分别为 8.23、8.31、7.92。作者将其解释为专门 agent 分工、跨簇综合和多维评价带来的质量提升。附录给出 LLM Agents 案例：100 篇、9 个簇、总处理时间约 18 分钟，生成约 11000 词 survey；Synthetic Data 和 Multimodal RL 也给出聚类统计。

同时，结果中也暴露出限制。RLHF Alignment 主题检索到更大语料时，正文 discussion 写到 pipeline 曾检索 1334 篇，但 writer 最终只引用 80 篇，约 6% 覆盖，说明单次 drafting pass 压缩长尾文献存在瓶颈。附录聚类质量的 silhouette score 也很低，例如 LLM Agents 0.055，Multimodal RL 0.045，提示主题组织质量不能只看生成文本评分。

## 7. 局限与可复现性

可复现性方面，论文提供了 subagent prompt、部分系统统计、模型配置和 pipeline 说明，但没有看到代码仓库链接、固定数据快照、完整 raw outputs 或 evaluator 原始 JSON。部分参考文献条目标注“Author metadata to be completed in the camera-ready version”，对 citation fidelity 形成风险。

局限包括：系统主要面向 LLM research，不证明跨学科泛化；超大 corpus 下引用覆盖急剧下降；评价依赖 agent-as-judge，主观性没有通过人类专家或 inter-rater agreement 校准；baseline 模型替换使与 AutoSurvey 原系统的公平性需谨慎解释；人类审计、偏见检查、错误定位和修复闭环均未形成可执行机制。

## 8. 对 paper2 story / 实验设计的影响

paper2 不能再把“多 agent 自动生成 survey”作为未被探索的空白来写。更稳妥的 story 是：已有工作已经在 survey 生成 中采用 agent decomposition、semantic clustering 和 LLM-as-judge，但这些系统主要优化长文生成质量，而不是把 SLR/SMS 的筛选、抽取、编码、综合与报告 主张绑定到可审计证据链。

实验设计上，paper2 应避免只用 LLM-as-judge 总分证明质量。Agentic AutoSurvey 的弱点说明 paper2 需要报告 citation/claim 粒度的可追踪率、unsupported claim 率、人工 audit workload、错误类型和 run record 完整性。对于大 corpus，应专门评估 long-tail 文献是否被筛选、抽取和综合，而不是只看最终报告长度或整体评分。

## 9. 可用于写作的引用角度

1. Agentic AutoSurvey 可作为近期多 agent survey 生成 的代表：它把检索、聚类、写作和自动评价拆成四个 Claude Code subagent。
2. 该工作说明 agent decomposition 能提升自动评估下的 survey synthesis 质量，但其证据链主要停留在生成级和 agent-as-judge 级。
3. 其 RLHF 案例显示，较大候选语料会导致引用覆盖瓶颈，这支持 paper2 将 coverage audit 和 run record 作为实验指标。
4. 与 paper2 的差异应写成“从 survey text generation 转向 SLR/SMS evidence workflow and audit”，不要写成先前工作完全没有覆盖 agentic survey/SLR。

## 10. 待复核清单

- 未人工打开 PDF 图表；若要引用 Figure 2--7 的具体数值，应回 PDF 核对图表版式。
- 需要核验是否存在公开代码仓库或数据包；正文未明确给出。
- AutoSurvey baseline 替换为 Llama-3.1-8B 的公平性需要在 related work 中标注，不宜直接引用为通用 SOTA 差距。
- SUMMARY 已保持 P2；使用时应说明其是 survey 生成 近邻而非 SLR/SMS 全流程 baseline。
