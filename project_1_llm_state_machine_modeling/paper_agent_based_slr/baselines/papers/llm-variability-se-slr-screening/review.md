# Beyond Accuracy: LLM Variability in Evidence Screening for Software Engineering SLRs

## 1. 快速结论卡片

| 字段 | 内容 |
|---|---|
| 标题 | Beyond Accuracy: LLM Variability in Evidence Screening for Software Engineering SLRs |
| 年份 | 2026 |
| 分层 | P0 |
| 阅读状态 | 已读全文文本-paper_content核验 |
| 证据等级 | 全文文本级；图表/表格细节待人工 PDF 核对 |
| 核验入口 | [bibtex.bib](./bibtex.bib)、[paper_content.txt](./paper_content.txt)；未人工打开 PDF 核对图表 |
| 输入 | 2 个真实 SE SLR 的题名、摘要、关键词与人工 inclusion/exclusion 标签；完整记录 126 + 392 篇 |
| 输出 | LLM / 传统分类器的 screening 决策、准确率 / F1、跨轮一致性、metadata 组合影响、采用 LLM screening 的实践 checklist |
| 方法/系统形态 | 受控实验；12 个 API LLM + 4 个传统 ML 分类器；固定 prompt、温度 0、5 次重复运行；非 agent 系统 |
| 覆盖阶段 | 主要覆盖 SLR study screening；附带讨论元数据准备、人工复核路由和采用前 pilot validation |
| 人审/审计机制 | 原文提出 unanimity 自动化 + disagreement 送人工复核 + verification sampling；但没有提供 claim-to-source 或 per-record 审计包 |
| 实验/指标 | 2 个 SE SLR、518 条完整记录；accuracy、F1、Gwet AC2、bootstrap CI、随机效应 meta-analysis、SESOI |
| 主要发现 | LLM 在温度 0 下仍有残余变异；摘要是关键输入；LLM 对传统 ML 没有稳定可泛化优势；采用时应以治理、成本、可复现和元数据约束为依据 |
| 对 paper2 的作用 | 强约束 paper2 的 screening evaluation、模型变异、human audit gate 和 run record 设计；不覆盖多阶段 agent SLR 或报告级 claim-to-source |
## 2. D1-D7 全文核验评分

emoji 口径见 [../../GUIDE.md](../../GUIDE.md)；本表单元格只放 emoji。

| D1 主题 | D2 流程 | D3 自动化 | D4 审计 | D5 评价 | D6 SE | D7 威胁 |
|---|---|---|---|---|---|---|
| 🟢 | 🟠 | 🟡 | 🟡 | 🟢 | 🟢 | 🟡 |

| 维度 | 评分 | 全文证据锚点 | 判定理由 |
|---|---:|---|---|
| D1 主题贴合度 | 🟢 | `paper_content.txt` Page 1 Abstract；Page 2 研究问题段 | 原文明确研究 SE SLR 的 study screening，并把风险集中在 false negative、模型选择、元数据输入和传统分类器对比上，和 paper2 的 screening 阶段直接相关。 |
| D2 SLR/SMS 流程覆盖度 | 🟠 | `paper_content.txt` §3 Methods / Page 3--6；§5 Guidelines / Page 12--13 | 实验任务只实质覆盖 study screening / selection，不做检索、抽取、编码、综合或报告生成。虽然 guidelines 提到 adoption checklist 和人工路由，但仍是单阶段 screening 工作。 |
| D3 LLM/agent 自动化深度 | 🟡 | `paper_content.txt` §3.3 / Page 4--6；Figure 4 prompt template | 使用 12 个 LLM 对每条记录和 inclusion criterion 打 1--7 分，再按阈值转成 include/exclude；流程输入输出清楚，但不是 agentic 多阶段系统，也没有工具调用或自主规划。 |
| D4 人工审计与可追踪性 | 🟡 | `paper_content.txt` §5 / Page 12--13 | 原文建议多轮推理、一致决策自动化、冲突样本送人工复核、自动筛选样本抽检，并要求记录模型/API 标识和环境配置；这是有用的治理建议，但未交付可复查的 per-record provenance 或 claim-to-source 证据链。 |
| D5 评价严谨性 | 🟢 | `paper_content.txt` §3.1--3.5 / Page 3--6；§4 / Page 7--12；§6 / Page 13 | 有真实 SE SLR 数据、12 个 LLM、4 个传统 ML baseline、重复运行、一致性分析、bootstrap CI、元数据消融和限制讨论。局限是仅 2 个 SLR、5 次迭代、无成本收益分析。 |
| D6 SE / CCF 相关性 | 🟢 | `paper_content.txt` Page 1 keywords；§1 / Page 1--2；§6 / Page 13 | 论文直接面向 Software Engineering SLR screening，数据来自 HCI-AI 与教育游戏化相关 SE review，虽然是 arXiv preprint，主题社区强相关。 |
| D7 novelty 威胁强度 | 🟡 | `paper_content.txt` §5 checklist / Page 12--13；§7 / Page 13--14 | 对 paper2 的威胁集中在 screening 模块：它已经证明模型变异、摘要依赖、传统 ML 对照和 human-review routing 的必要性。它不覆盖 agent workflow、抽取/综合/报告、run record 或报告级证据绑定，因此不是完整 P0 竞品，但必须作为 screening 强基线正面对比。 |

## 3. 论文解决的问题与背景

论文的出发点是 SE SLR 的 study screening 成本高、容易不一致，且 false negative 会直接损害综述有效性。作者指出，传统双人独立筛选加交叉验证虽能降低风险，但当候选文献达到数千条时，人力成本仍然很高。LLM 被视为可降低成本的候选方案，但原文认为已有研究仍缺少三个关键证据：不同 LLM 在同一协议下表现如何、题名/摘要/关键词不同组合对结果有什么影响、LLM 相比传统监督分类器是否有稳定收益。

这篇论文的定位不是提出新的 SLR agent，而是做 screening 阶段的受控评价和治理建议。它尤其强调“accuracy 之外”的问题：温度设为 0 也不等于完全可复现，API 模型版本会漂移，输入元数据缺失会改变结果，单一模型在一个 SLR 上表现好不能直接外推到另一个 SLR。这个问题设定对 paper2 很关键，因为 paper2 若声称 agent workflow 能可靠接管筛选阶段，必须回答这类变异和审计问题。

## 4. 方法 / 系统拆解

输入是两个真实 SE SLR 的候选记录和人工参考标签。SLR1 来源于 HCI 与 AI convergence 的 tertiary study 样本，原始 134 条题名中最终恢复 126 条完整题名、摘要、关键词记录；SLR2 来源于 game-based / gamified learning 中用户分类策略的 mapping study，448 条去重候选中最终整合 392 条完整记录。

流程分三期。Phase 1 比较 12 个 LLM，包括 OpenAI、Gemini、Anthropic 和 Llama 系列。每条文献按 inclusion criterion 构造固定 prompt，让模型返回 1--7 的 Likert 分数；两个标准都大于等于 5 才判为 include。每个模型、每个数据集重复 5 次，温度设为 0，用于观察残余非确定性。Phase 2 从两个 SLR 中各抽 50 条记录，比较 abstract only、abstract+title、abstract+title+keywords、abstract+keywords、title+keywords 五种输入组合。Phase 3 用每个 SLR 各 50 条训练传统分类器，TF-IDF 表示后训练 Multinomial NB、Logistic Regression、Random Forest 和 SVM，并与零样本 LLM 对比。

LLM 的角色是单条记录分类器，不负责检索、抽取、证据综合或报告写作。系统没有 agent 协作，也没有自主规划。人机协作主要出现在建议层面：作者在 §5 提出采用前先做代表性 pilot，自动化只处理多轮 unanimous 决策，冲突样本交给人工复核，并对自动化样本做抽检。证据/日志方面，作者建议记录软件版本、环境配置、推理参数、精确模型/API 标识和多轮一致性，但论文没有描述一个可导出的 run record 或 per-paper 决策日志格式。

## 5. 实验 / 评价设计

RQ1 问不同 LLM family 的 screening 表现和跨轮稳定性如何；RQ2 问题名、摘要、关键词组合如何影响分类质量；RQ3 问 LLM 是否相对传统 ML 分类器有优势。数据集是两个真实 SE SLR，共 518 条完整记录。Phase 1 使用所有完整记录，Phase 2 使用 100 条随机样本，Phase 3 每个 SLR 取 50 条训练传统分类器、其余测试。

主要指标包括 accuracy、F1-score、Gwet AC2 和 bootstrap 置信区间。作者解释选择 accuracy 是因为两个数据集类别不平衡程度较低，但后续也指出 class imbalance 会让 trivial exclude baseline 显得不差，因此建议报告 precision、recall、F1 等多指标。元数据组合分析使用 bootstrap 估计 95% CI，并用 DerSimonian-Laird 随机效应模型聚合效应，SESOI 设为正负 2 个百分点。baseline 包括四个传统机器学习分类器，而不是其他 agentic SLR 系统。

人工标注方面，参考标签来自原 SLR 的 inclusion/exclusion 决策；原文没有重新组织专家标注，也没有报告多名人工 reviewer 的一致性重算。统计方式相对完整，但局限也明确：仅两个英文教育相关 SE SLR，API 调用发生在 2025 年 5--10 月，模型更新会影响复现，5 次迭代只能说明存在非确定性，不能充分估计所有不稳定场景。

## 6. 主要结果与结论

Phase 1 显示模型间差异很大。SLR1 中 gpt-4o mean accuracy 为 0.830159，低端模型约 0.611111；SLR2 中 gpt-4.1 mean accuracy 为 0.835204，而 gpt-3.5-turbo 仅 0.369898。作者据此报告 SLR1 上约 22 个百分点、SLR2 上约 47 个百分点的模型差异。即使温度设为 0，多数模型仍在 5 轮之间出现决策变异；Gwet AC2 从 0.55 到 1.0 不等。

Phase 2 的核心结论是摘要不可替代。abstract+keywords、title+abstract、title+abstract+keywords 相对 abstract only 的聚合效应都接近 0，且位于正负 2 个百分点 SESOI 内；title+keywords 则显著退化，估计效应为 -5.55 个百分点，95% CI 为 [-9.94, -1.16]。因此 paper2 不能把 title/keywords-only screening 写成与 full metadata 同等可靠，除非有自己的证据。

Phase 3 显示 LLM 与传统方法没有稳定可泛化的性能分离。SLR1 中若干 LLM 在 accuracy 和 F1 上较强，但置信区间与传统模型重叠；SLR2 中 Logistic Regression 接近 top LLM，部分区间重叠。作者最后建议，选择 LLM 还是传统模型不应只看聚合性能，而应考虑成本、透明性、可复现性、元数据可用性和治理约束。

## 7. 局限与可复现性

原文局限写得比较清楚：外部有效性受限于 2 个英文、教育相关 SE SLR；API 模型是在 2025 年 5--10 月访问，版本漂移会影响复现；5 次重复能证明残余非确定性，但可能低估方差；未纳入 fine-tuned 或专门模型；未做成本收益分析；screening 错误也可能部分来自人工参考标签的歧义。

可复现性方面，论文给出模型列表、prompt template、输入特征组合、指标和统计方法，并建议记录精确模型/API 标识、环境配置和推理参数。但 `paper_content.txt` 中未发现代码仓库、数据下载链接或完整逐条预测文件；因此只能判为实验描述较完整，制品级复现仍待核验。

## 8. 对 paper2 story / 实验设计的影响

paper2 必须避免笼统声称 LLM screening 比传统方法更好。这篇论文直接说明 LLM 的优势依赖数据集、模型、输入元数据和指标，且传统 Logistic Regression 在某些设置下可接近 top LLM。paper2 若包含 screening 模块，应把传统 ML、trivial exclude、单模型 LLM、多轮一致性策略作为 baseline 或 sanity check。

paper2 的 human audit gate 可以借鉴其 unanimity + disagreement routing，但要进一步做出差异化：不仅记录冲突，还要保存每条文献的输入、模型输出、阶段决策、人工裁决、错误类别和下游 claim 影响。paper2 也应在 run record 中显式记录模型 ID、调用时间、prompt、温度、输入 metadata 是否完整，并把 title/abstract/keywords 缺失作为 eligibility 或 risk 字段。

## 9. 可用于写作的引用角度

- 在 SE SLR screening 中，近期研究显示不同 LLM 即使在统一协议和温度 0 下也存在明显模型间差异和跨轮变异，因此自动化筛选不能只报告单次 accuracy。
- Hida 等人的结果提示，abstract availability 是 LLM screening 的关键条件，title+keywords-only 设置会显著退化；这支持本文把输入完整性纳入 run record 和 eligibility gate。
- 该工作将 LLM 与传统 ML 分类器置于同一 screening 协议下，发现 LLM 没有稳定可泛化优势；本文因此把 agentic workflow 的贡献限定在多阶段证据链和审计机制，而不是单纯声称筛选分类器更强。
- 其 unanimity 自动化与人工复核建议可作为本文 human audit gate 的前置相关工作，但本文需要进一步覆盖 per-stage provenance 和 report-level claim-to-source。

## 10. 待复核清单

- 人工打开 PDF 核对 Figure 5--12 和 Table 2 的图表版式，确认 `paper_content.txt` 未漏掉关键视觉信息。
- 查 arXiv 后续版本或期刊扩展稿，核验是否已有正式出版、DOI、代码或数据链接。
- 复核 Phase 3 训练/测试划分是否有固定随机种子；`paper_content.txt` 未明确给出。
- 若用于 paper2 baseline 表，补充该文是否公开逐条预测、prompt 脚本和完整数据清洗结果。
