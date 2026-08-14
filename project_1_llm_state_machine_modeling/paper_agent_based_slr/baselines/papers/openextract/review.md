# OpenExtract: Automated Data Extraction for Systematic Reviews in Health

## 1. 快速结论卡片

| 字段 | 内容 |
|---|---|
| 标题 | OpenExtract: Automated Data Extraction for Systematic Reviews in Health |
| 年份 | 2026 |
| 作者 / venue / 出版状态 | Jim Achterberg、Bram Van Dijk 等；arXiv:2603.13338; 本轮未核验正式 peer-reviewed / CCF 状态 |
| 分层 | P2 |
| 阅读状态 | 已读全文文本-paper_content核验 |
| 证据等级 | 全文文本级；图表/表格细节待人工 PDF 核对 |
| 核验入口 | [bibtex.bib](./bibtex.bib)、[paper_content.txt](./paper_content.txt) |
| 研究脉络 | 证据抽取、证据溯源与审计 |
| 引用角色 | 背景近邻 / 局部 claim 风险或禁用 claim 证据 |
| LLM/agent 角色 | LLM/agent 执行部分检索、筛选、抽取、组织、生成或评价环节；具体阶段见方法/覆盖阶段字段。 |
| 证据溯源粒度 | 人工核验或 benchmark/gold 级；未必有 claim-level provenance。 |
| 输入 | SLR 中的论文全文、待抽取的数据条目、候选输出标签；评测案例来自 digital health SLR。 |
| 输出 | 每个 data entry 的结构化 JSON 标签选择，以及不同 LLM 与人工抽取结果的一致性/precision/recall。 |
| 方法/系统形态 | 开源 RAG pipeline，面向 SLR data extraction 的单阶段自动化工具，不是完整 SLR agent 工作流。 |
| 覆盖阶段 | 主要覆盖 data extraction；评测案例中使用 ASReview 做 title/abstract screening，但 OpenExtract 本身不负责检索、筛选、综合或报告。 |
| 不覆盖阶段 | 不覆盖检索、题摘筛选、编码综合和完整报告生成；主要威胁证据抽取 / provenance 环节。 |
| 人审/审计机制 | 两名人工研究者抽取数据作为比较参照；pipeline 取 top-3 相关 chunks 作为 LLM 上下文，但原文未说明 per-answer provenance 或人工审计门。 |
| 人类角色 | 运行中审查者或用户反馈；需区分是否为正式审计 gate |
| 审计时机 | 原文未给出清晰审计时机或本轮未抽取 |
| 主张追踪状态 | chunk 上下文级；无 per-answer provenance 或人工审计 gate。 |
| 决策日志状态 | per-stage 叙述级；结构化日志待核验 |
| 冲突处理机制 | 原文未给出明确冲突处理或不适用 |
| 审计导出性 | 有表格/JSON/schema 输出线索；是否形成可审计证据包待 artifact audit。 |
| 实验/指标 | 数字健康 SLR 初始检索 7,323 篇，ASReview 筛到 249 篇 relevant；随机抽 50 篇用于评估，本文报告前 10 篇、150 个数据点；指标含 Cohen's kappa、precision、recall。 |
| 模型/API 设置 | DeepSeek、Qwen；具体版本/调用日期按原文与 artifact 待复核 |
| 提示词状态 | 正文提到 prompt；完整模板待核验 |
| 温度/重复/随机种子 | 原文未给出或本轮未抽取 temperature / seed / repeats |
| 主要发现 | DeepSeek V3.1 与 Qwen2.5 72B 的 precision/recall 均约 0.8；Qwen2.5 7B 明显较低；LLM 之间一致性高于 LLM 与人工之间一致性。 |
| 关键结果锚点 | review.md §2 D1-D7 证据锚点 + §5/§6 实验与结果；SUMMARY 数字不得脱离单篇锚点引用 |
| 数值使用许可 | 仅文本级引用；正式写作前需 PDF 图表/表格核对 |
| 对 paper2 的作用 | 可作为 SLR extraction 阶段的局部 baseline，提醒 paper2 的抽取模块必须处理人类解释差异、结构化输出和表格/图像证据缺失。 |
| 受影响主张 ID | C3,C5 |
| 威胁类型 | 局部覆盖 + 禁用 claim 证据 |
| 威胁的 paper2 主张 | 可作为 SLR extraction 阶段的局部 baseline，提醒 paper2 的抽取模块必须处理人类解释差异、结构化输出和表格/图像证据缺失。 |
| 支持的 paper2 主张 | 支持 paper2 将 claim-to-source trace、page/table/cell 级证据定位和 人工审计 gate 作为核心贡献与指标。 |
| paper2 应避免的主张 | 避免声称 page/table/cell 级 evidence provenance 是空白；避免只保存最终答案而缺少证据定位。 |
| baseline 可用性 | 仅related-work背景或局部强近邻；不作为主流程可运行 baseline。 |
| 对比方式 | 仅related-work背景 / extraction 局部baseline |
| 代码状态 | 给出 GitHub 开源 pipeline 入口；本轮未打开 URL、commit 或 license 核验 |
| 数据状态 | 使用 digital health SLR / article chunks；数据公开性与 license 待核验 |
| 许可状态 | 未核验；不得据此承诺可复现或可再分发 |
| 制品入口 | 本轮仅做 paper_content 文本级线索识别，未打开外部 URL；具体 URL、commit、license 和 smoke 运行留待下一轮 artifact audit |
| 运行可行性 | 仅related-work背景 / extraction 局部baseline |
| 可复现资产 / 阻塞项 | 代码、数据、prompt、license、正式 venue/DOI 与 PDF 图表级数值均按 §7 / §10 待复核清单处理；未核验项不得支撑强实验比较。 |

## 2. D1-D7 全文核验评分

| D1 主题 | D2 流程 | D3 自动化 | D4 审计 | D5 评价 | D6 SE | D7 威胁 |
|---:|---:|---:|---:|---:|---:|---:|
| 🟡 | 🟠 | 🟡 | 🟠 | 🟡 | 🟠 | 🟠 |

| 维度 | 评分 | 全文证据锚点 | 判定理由 |
|---|---:|---|---|
| D1 主题贴合度 | 🟡 | `paper_content.txt:22-31`, `paper_content.txt:46-57` | 论文直接研究 LLM 辅助 systematic literature review 的 data extraction，属于 SLR 关键环节；但任务边界明确限定为抽取，不覆盖完整 SLR/SMS。 |
| D2 SLR/SMS 流程覆盖度 | 🟠 | `paper_content.txt:49-52`, `paper_content.txt:105-135`, `paper_content.txt:181-186` | OpenExtract 自身只处理 data extraction。评测案例另用 ASReview 完成筛选，但该筛选不是 OpenExtract 的 LLM workflow 部分，因此流程覆盖度只能算单环节。 |
| D3 LLM/agent 自动化深度 | 🟡 | `paper_content.txt:65-74`, `paper_content.txt:88-104` | 有清楚的 RAG 输入输出链：chunking、embedding 检索 top-3 chunks、LLM 从候选标签中输出 JSON；但没有 agent planning、多阶段 orchestration 或闭环修复。 |
| D4 人工审计与可追踪性 | 🟠 | `paper_content.txt:88-100`, `paper_content.txt:137-146`, `paper_content.txt:155-164` | 原文用两名人工研究者抽取结果作为评测参照，并要求 LLM 基于上下文 chunks 输出结构化 JSON；但没有说明系统保存每个答案对应 chunk、人工审核决策日志或 claim-to-source trace。 |
| D5 评价严谨性 | 🟡 | `paper_content.txt:128-140`, `paper_content.txt:147-169` | 有真实 SLR 场景、人工参照、Cohen's kappa、precision/recall 和多 LLM 比较；但当前论文只报告前 10 篇、150 个数据点，样本较小，且不含误差分类或跨领域复现。 |
| D6 SE / CCF 相关性 | 🟠 | `paper_content.txt:3-4`, `paper_content.txt:105-114` | 领域是 health/digital health systematic review，方法学对 SLR 自动抽取有用，但不是软件工程、LLM4SE 或 MDE 场景。 |
| D7 对本文 novelty 的威胁强度 | 🟠 | `paper_content.txt:181-190` | 它威胁 paper2 的 data extraction 局部能力，尤其是 RAG 抽取和结构化标签输出；但不覆盖 agent-based multi-stage workflow、人工审计 gate、报告级 主张绑定或 SE 评价。 |

## 3. 论文解决的问题与背景

OpenExtract 的问题背景很清楚：系统综述中的 data extraction 工作量大，特别是当综述主题很宽、纳入论文很多、需要抽取的字段又很细时，人工逐篇阅读成本高。作者认为已有 ASReview 这类工具能辅助 literature screening，但如果把 SLR 每一步都抽象给 LLM，研究者会失去对范围和流程的控制。因此本文刻意只聚焦 data extraction 阶段，目标是在不牺牲粒度的情况下，用 LLM 从论文文本中自动预测结构化 data entries。

这个定位对 paper2 有价值，因为它代表一种谨慎的局部自动化路径：不声称端到端替代 SLR，而是把一个明确可评测的环节抽出来，使用人工抽取结果做参照。它也说明 paper2 若要做端到端 agent 工作流，必须解释为什么多阶段组合不会降低研究者对 scope、criteria 和证据解释的控制。

## 4. 方法 / 系统拆解

OpenExtract 是 RAG pipeline。输入包括论文文本、用户定义的数据条目问题和候选输出标签。系统先把每篇文章切成 1000-token segments，相邻 segments 有 500-token overlap。然后用 PubMedBERT embedding 对 chunk 和 data entry/query 编码，通过 cosine similarity 选出每个 data entry 最相关的 top-3 chunks。作者说明这种 chunking 加 BERT 512-token 截断的组合相当于 sliding-window 机制，保证文本不同部分都能被考虑。

LLM 接收 QUESTION、ANSWERS 和 CONTEXT，任务是在候选标签中选择正确 option IDs，并且只返回 JSON array。prompt 明确要求 LLM 作为 meticulous research assistant，从提供的 research paper context chunks 回答，不要输出 JSON 之外的文本。模型通过 OpenRouter 调用，实验选择 DeepSeek V3.1、Qwen2.5 Instruct 72B 和 Qwen2.5 Instruct 7B，理由是开放权重、成本低和参数规模不同。

人机协作主要体现在两处。第一，研究者仍定义 data entries 和 output labels，GitHub repository 中据称有详细条目和标签。第二，两个 human researchers 的抽取结果被用作评测参照。系统不是 interactive human-in-the-loop：全文没有写用户如何逐条接受/拒绝 LLM 输出，也没有报告审计日志、错误原因分类或每个 JSON 答案的 evidence provenance。

## 5. 实验 / 评价设计

评测案例是一个 digital health SLR，研究问题是哪些 data analysis techniques 适用于不同 digital health applications。作者准备了 15 个 data entries 及候选标签，主题包括 digital health application 类型、study participants 数量、prediction models、evaluation metrics 等。

检索源包括 Web of Science、IEEE Xplore、PubMed 和 ACM Digital Library，时间截至 2025 年 6 月。初始检索得到 7,323 篇文章。筛选阶段使用 ASReview 辅助 title/abstract screening，纳入标准是 digital health applications 且使用 predictive analytics 或 machine learning，并且在 real-life medical setting 中测试；当 ASReview 连续推荐 10 篇 irrelevant articles 时停止，最终得到 249 篇 relevant articles。

评价上，作者随机选择 50 篇论文评估 pipeline，但本文只报告该随机子集中前 10 篇的结果，对应 10 篇乘以 15 个 data entries，即 150 个数据点。人工参照来自前两名作者。指标包括 Cohen's kappa，用于比较两名人工研究者和三个 LLM 之间的 inter-rater reliability；另有 precision/recall，定义为：LLM 选出的任何由至少一个研究者给出的答案算 TP，两个研究者都未给出的答案算 FP，两个研究者都给出但 LLM 漏掉的答案算 FN。

## 6. 主要结果与结论

Table 1 显示，两个 human researchers 之间 Cohen's kappa 为 0.925，显著高于人工与 LLM 之间的一致性。Researcher 1 与 DeepSeek、Qwen 72B、Qwen 7B 的 kappa 分别为 0.763、0.784、0.512；Researcher 2 与三者分别为 0.749、0.751、0.496。DeepSeek 与 Qwen 72B 之间 kappa 为 0.852，高于它们与人工之间的一致性，作者据此指出 LLM 之间可能存在相似偏差。

Table 2 显示，DeepSeek precision/recall 均为 0.820，Qwen 72B precision 为 0.846、recall 为 0.813，Qwen 7B precision 为 0.624、recall 为 0.564。作者的解释是该任务主要是 in-context knowledge retrieval，DeepSeek V3.1 的巨大通用知识未必带来优势；但当模型缩小到 Qwen 7B 时，性能明显下降。

结论部分把 OpenExtract 定位为开源 RAG pipeline，可用于大规模 SLR 的自动 data extraction，也可迁移到其他结构化文本抽取任务。作者对结果使用“promising”而非完全替代人工的表述，这是 paper2 写作可借鉴的谨慎口径。

## 7. 局限与可复现性

作者明确列出两个局限。第一，评测用 SLR 的 search query 很宽，且没有使用 MeSH terms，因此 digital health 案例本身只是 illustrative purpose。第二，pipeline 目前只 parse text，遗漏 figures 和 tables 中的信息，未来需要 multimodal foundation models 解析图表。

可复现性方面，摘要给出 OpenExtract GitHub 链接，方法部分也说明 data entries 和 output labels 在 GitHub repository 中。当前本地核验只基于 `paper_content.txt`，没有访问仓库，也没有打开 PDF 图 1。因此代码是否完整、prompt/配置是否可直接复跑、评测随机 50 篇的剩余 40 篇结果是否存在，仍需后续检查。

## 8. 对 paper2 story / 实验设计的影响

第一，OpenExtract 是 paper2 extraction 阶段的局部强参照。paper2 若声称“结构化抽取”能力，需要至少说明与 RAG top-k chunk + JSON label selection 的差异，例如是否保存 chunk-level provenance、是否支持自由文本证据摘录、是否有人工确认和修复闭环。

第二，OpenExtract 的 evaluation 提醒 paper2 不应把一个人工标注者当作唯一 ground truth。它承认 data extraction 往往没有单一真值，并使用两个研究者的并集/交集设计 TP/FP/FN。paper2 的抽取评价也应处理 annotator disagreement、ambiguous fields 和 partial correctness。

第三，图表证据缺失是 SLR 抽取中的现实问题。paper2 如果只处理 PDF 文本，应明确把 table/figure extraction 列为 out-of-scope 或提供 fallback 审计提示，避免把证据链写得过满。

## 9. 可用于写作的引用角度

1. 可作为 extraction-stage baseline：OpenExtract 用 RAG 从 SLR 论文文本中选择结构化 data entry labels，并与两名人工研究者抽取结果比较。
2. 可作为 evaluation design 参照：系统综述抽取字段可能没有单一 ground truth，评价需要显式处理人工分歧。
3. 可作为局限引用：仅解析正文文本会遗漏图表中的关键信息，这会影响自动抽取系统的证据完整性。
4. 不应把它写成完整 SLR 自动化或 agent 式 SLR 工作流；它有意限定在 data extraction 阶段。

## 10. 待复核清单

1. 当前只读 `paper_content.txt`，未回 PDF 核对 Figure 1 和表格版式。
2. 需访问 GitHub 仓库核验代码、data entries、labels、prompt、随机 50 篇评测材料是否完整公开。
3. 需确认 arXiv 版本是否已有正式 venue/DOI；本地 BibTeX 目前只支持 arXiv 引用。
4. 若 paper2 使用它做 baseline，需要补充抽取字段类别、错误类型和图表信息缺失比例，原文当前没有给出这些细节。
