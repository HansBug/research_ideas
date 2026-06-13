# ARISE: Agentic Rubric-Guided Iterative Survey Engine for Automated Scholarly Paper Generation

## 1. 快速结论卡片

| 字段 | 内容 |
|---|---|
| 标题 | ARISE: Agentic Rubric-Guided Iterative Survey Engine for Automated Scholarly Paper Generation |
| 年份 | 2025 |
| 作者 / venue / 出版状态 | Zi Wang、Xingqiao Wang 等；arXiv:2511.17689; 本轮未核验正式 peer-reviewed / CCF 状态 |
| 分层 | P1 |
| 近邻强度备注 | agentic survey engine 强近邻；SUMMARY 归 P1 而非 P0，因为其主线是 survey 生成/refinement，不是 SLR/SMS evidence workflow。 |
| 阅读状态 | 已读全文文本-paper_content核验 |
| 证据等级 | 全文文本级；图表/表格细节待人工 PDF 核对 |
| 核验入口 | [bibtex.bib](./bibtex.bib)、[paper_content.txt](./paper_content.txt)；未人工打开 PDF 图表 |
| 研究脉络 | 自动 survey / literature review 生成与评价 |
| 引用角色 | 模块级 baseline / 重要相关工作定位 |
| LLM/agent 角色 | LLM/agent 执行部分检索、筛选、抽取、组织、生成或评价环节；具体阶段见方法/覆盖阶段字段。 |
| 证据溯源粒度 | decision-log / trace 级 provenance；需核验是否能导出完整证据包。 |
| 输入 | 用户 survey theme、子主题、来源/venue 线索、检索得到或用户提供的引用列表 |
| 输出 | 可编辑 LaTeX survey manuscript、BibTeX、PDF、reviewer feedback、meta-review revision plan、chunk-level scores |
| 方法/系统形态 | CrewAI 多 agent 系统，22 个 specialized agents；citation-first retrieval、citation-keyed memory、citation-preserving outline synthesis、evidence-locked targeted revision |
| 覆盖阶段 | 主题扩展、引用检索/过滤/验证、知识库构建、outline、分节写作、编辑、引用补全、LaTeX 格式化、rubric peer-review loop |
| 不覆盖阶段 | 不覆盖 SLR/SMS 的双人筛选、纳入/排除审计、抽取表、编码协议、质量评价和系统综述级报告审计。 |
| 人审/审计机制 | 多 LLM reviewer 评分和反馈；cross-family judge；human expert before/after evaluation；citation traceability audit；chunk-level scores 和 trajectories |
| 人类角色 | 原文有人类参与线索；角色需在正式写作前复核 |
| 审计时机 | 原文未给出清晰审计时机或本轮未抽取 |
| 主张追踪状态 | 引用级 / chunk级 citation traceability 线索；不等同 SLR 抽取表或报告级 claim ledger。 |
| 决策日志状态 | 无或仅论文叙述 |
| 冲突处理机制 | 原文未给出明确冲突处理或不适用 |
| 审计导出性 | 有表格/JSON/schema 输出线索；是否形成可审计证据包待 artifact audit。 |
| 实验/指标 | 10 篇 human-written baseline、SurveyForge/SurveyX/AutoSurvey；7 维 20 子类 rubric；tri-judge/bi-judge、Krippendorff’s Alpha、human expert score、eCTR、模型容量 ablation、成本/时间 |
| 模型/API 设置 | GPT-4、GPT-4.1、Claude、Sonnet、Gemini、GPT；具体版本/调用日期按原文与 artifact 待复核 |
| 提示词状态 | 附录/正文给出 prompt 或片段；完整可复用性待核验 |
| 温度/重复/随机种子 | 原文未给出或本轮未抽取 temperature / seed / repeats |
| 主要发现 | ARISE tri-judge avg 92.48，高于 baseline；human evaluation 从 70.2 提升到 83.7；报告 eCTR=1.00；单篇生成约 10-20 美元、约 3.5 小时 |
| 关键结果锚点 | review.md §2 D1-D7 证据锚点 + §5/§6 实验与结果；SUMMARY 数字不得脱离单篇锚点引用 |
| 数值使用许可 | 仅文本级引用；正式写作前需 PDF 图表/表格核对 |
| 对 paper2 的作用 | 对 agentic survey 生成 + rubric-guided refinement + citation traceability 构成强 novelty 威胁；paper2 需强调 SE-SLR 流程、人工审计、claim-level evidence 和可复现 run record |
| 受影响主张 ID | C1,C3,C5,C6,C7 |
| 威胁类型 | 局部覆盖 + 禁用 claim 证据 |
| 威胁的 paper2 主张 | 对 agentic survey 生成 + rubric-guided refinement + citation traceability 构成强 novelty 威胁；paper2 需强调 SE-SLR 流程、人工审计、claim-level evidence 和可复现 run record |
| 支持的 paper2 主张 | 支持 paper2 把报告生成 claim 收窄为“生成必须可审计”，并把 citation validity、unsupported claim 和 有证据支撑的断言 纳入评价。 |
| paper2 应避免的主张 | 避免声称自动 survey / review generation 尚无人研究；避免把文本流畅度、引用准确率或 LLM-as-Judge 总分等同于 SLR/SMS 方法学可靠性。 |
| baseline 可用性 | 协议/指标baseline或局部强baseline；主要用于模块级对照与写作定位。 |
| 对比方式 | 协议/指标baseline / survey生成强近邻 |
| 代码状态 | 声称有/正文出现 GitHub 或 code 线索；本轮未打开核验 |
| 数据状态 | 声称有/正文出现 dataset 或 data availability 线索；license 未核验 |
| 许可状态 | 未核验；不得据此承诺可复现或可再分发 |
| 制品入口 | 本轮仅从 paper_content/review 识别线索；URL、commit、license 和 smoke 运行留待下一轮 artifact audit |
| 运行可行性 | 协议/指标baseline / survey生成强近邻 |
| 可复现资产 / 阻塞项 | 代码、数据、prompt、license、正式 venue/DOI 与 PDF 图表级数值均按 §7 / §10 待复核清单处理；未核验项不得支撑强实验比较。 |

## 2. D1-D7 全文核验评分

emoji 口径：🟢 强，🟡 中，🟠 弱，⚪ 无 / 背景。

| D1 主题 | D2 流程 | D3 自动化 | D4 审计 | D5 评价 | D6 SE | D7 威胁 |
|---|---|---|---|---|---|---|
| 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟠 | 🟢 |

| 维度 | 评分 | 全文证据锚点 | 判定理由 |
|---|---:|---|---|
| D1 主题贴合度 | 🟢 | Abstract；Introduction；Methodology System Overview | 直接研究 automated scholarly survey 生成，并明确对标 AutoSurvey、SurveyX、SurveyForge 等 ASG 系统。 |
| D2 SLR/SMS 流程覆盖度 | 🟢 | Citation Preparation；Structured Knowledge Base；Outline；Composition；Refinement | 覆盖主题扩展、检索、引用整理、summary KB、outline、写作、评审和修订，至少四个以上 review/report 相关环节；但不是严格 PRISMA SLR。 |
| D3 LLM/agent 自动化深度 | 🟢 | Figure 1；System Overview；Experimental Design | 22 个专门 agent，检索、验证、写作、格式化和 reviewer loop 都有明确输入输出，是强多阶段 agent 工作流。 |
| D4 人工审计与可追踪性 | 🟢 | CKM/CPOS/ELSR；Bias Controls；Reference Reliability；Appendix 1/4/5 | 有 citation-keyed memory、citation-preserving invariant、evidence-locked section revision、chunk-level scores、cross-family judge 和 eCTR；虽非人工逐 claim 审计，但可追踪设计强。 |
| D5 评价严谨性 | 🟢 | Tables 2-6；Human Evaluation；Reference Reliability；Reliability Evaluation | 自动与人工评价、baseline 对比、model ablation、inter-rater reliability、citation trace audit、成本时间报告齐全；局限是人类评价样本较小且大量依赖 LLM judges。 |
| D6 SE / CCF 相关性 | 🟠 | bibtex: arXiv cs.DL；baseline topics 为 LLM/AI 泛学术 survey | 非 SE/CCF，任务是泛学术 survey 生成；对 SE SLR 方法学相关但不是软件工程直接 baseline。 |
| D7 对本文 novelty 的威胁强度 | 🟢 | Methodology 全部；Tables 2-6；Limitations | 覆盖 paper2 可能声称的 agent 工作流、rubric-guided refinement、citation traceability 和生成评价核心组合，是强威胁；差异必须放在 SE evidence synthesis 和人工审计证据链。 |

## 3. 论文解决的问题与背景

ARISE 的问题设定是：现有 automated survey-generation 系统常依赖 preprint-heavy sources、单次生成、质量控制不足、格式不稳定，而且缺乏 peer-review-style feedback。作者认为真实学术写作是迭代的，需要检索、组织、写作、评审和修订的闭环。

这篇论文对 paper2 的压力比 LiRA 更大，因为它不仅写作，还把 citation-first retrieval、knowledge base、rubric review 和 LaTeX finalization 串成一个完整工程系统。它也直接使用“transparent”和“reproducible”等词汇，因此 paper2 不能泛泛声称“我们首次把 agent 用于 survey 生成”。必须将目标收窄到 SE-SLR/SMS 的证据流程和人工审计。

## 4. 方法 / 系统拆解

ARISE 的 Citation Preparation 从用户给定主题开始，Expansion Agent 生成相关子主题，用户可 refine/approve；Domain-scoping Agent 推荐合适的 publisher portals、academic search/indexing services 和 open-access repositories；Citation Retrieval Agent 收集候选引用元数据，然后去重和格式验证。Structured Knowledge Base Construction 会尝试通过 URL 获取全文或摘要，失败则用 author/title fallback search，仍失败就写入 Error List。成功获取的内容被 summarizer 压缩成 contribution-focused entry，并以 `refN -> summary` 形式进入 citation-keyed memory。

Outline 阶段把 citation summaries 分批生成 partial outlines，再由 Merging Agent 合并，Validation Agent 检查结构和 gap。CPOS 要求合并后 `cite(C)=cite(A)∪cite(B)`，缺失 citation index 会被 backfill。Composition 阶段按 section 查询 `cite(S)`，只注入相关 CKM summaries，Writing Agent 起草，Editor Agent 改流畅性和局部冗余。Citation Completion Agent 补 DOI、venue、year 等 BibTeX 字段；Formatting Agent 清洗 LaTeX 命令和表格环境。

Refinement 是核心闭环：当前 draft 被切成连续 page chunks，多 reviewer agents 使用共享 rubric 独立打分和反馈，平均分达阈值则接受，否则 summary agent 合成 meta-review revision plan，refinement/editor agents 只修改被点名 sections。ELSR 要求新文字只能基于该 section 已引用的 CKM entries，不允许引入未引用 claim 或 reference。这个设计对 paper2 的 claim-to-source traceability 有直接参考价值。

## 5. 实验 / 评价设计

系统用 CrewAI 实现，非 reviewer agents 默认使用 GPT-4.1；reviewer pool 包括 GPT-4.1、Gemini 2.5 Pro、Claude 3.7 Sonnet，并报告排除 generator family 的 bi-judge 设置。评价 rubric 有 7 个维度、20 个子类：Scope、Literature、Analysis、Originality、Organization、Presentation、References，每个子类 1-5 分，总分 100。

Baseline 包括 10 篇近年 human-authored survey papers，以及 SurveyForge、SurveyX、AutoSurvey 的可得输出。由于 availability constraints，SurveyForge 和 SurveyX 各 10 篇，AutoSurvey 3 篇。实验还包含 refinement trajectory、4 名专家对 5 篇生成 survey 的 before/after human evaluation、`gpt-4.1-mini` vs `gpt-4.1` model ablation、PyMuPDF + CrossRef/Semantic Scholar/arXiv 的 reference traceability audit、Krippendorff’s Alpha reviewer agreement。

## 6. 主要结果与结论

Table 2 中 ARISE tri-judge avg 为 92.48，bi-judge avg 为 92.43，高于 SurveyForge、human baseline、AutoSurvey 和 SurveyX。Table 3 显示 ARISE 在 7 个 rubric category 均领先，References 得分 4.98，Literature 4.95，Organization 4.82。作者报告 Krippendorff’s Alpha 均超过 0.966，最高 0.987。

Table 4 给出一个 refinement trajectory：平均 reviewer score 从 87.0 经 3 轮到 92.7，超过目标 92.0。Table 5 的 human evaluation 中，5 个 topic 的平均 total score 从 70.2 到 83.7，平均子类分从 3.51 到 4.18。Table 6 的 model ablation 显示 `gpt-4.1-mini` 从 83.09 到 88.04，`gpt-4.1` 从 86.53 到 92.48。Reference Reliability 部分报告 eCTR=1.00、Hallucination Rate=0.00，但这是基于 final PDF references 能否匹配外部数据库，不等同于每个正文 claim 都被正确引用支持。

## 7. 局限与可复现性

Appendix Limitations 中作者承认评估框架主要依赖 LLM reviewer，时间和资源限制导致未能让 human reviewers 参与主评价；虽然正文有人类专家 before/after 评价，但规模只有 4 名专家、5 篇生成 survey。系统依赖商业 LLM API、Serper API、rate limits、context caps 和 quota，单篇生成约 10-20 美元、约 3.5 小时，refinement 占 30-40% 时间。

可复现性方面，论文声称 supplementary materials 提供 generated drafts、reviewer feedback、meta-review synthesis 和 codebase，但 `paper_content.txt` 没有本地展开这些材料。eCTR 只验证参考文献可匹配外部数据库，不验证引用是否支持对应句子。写作时应把“reference traceability”表述为 reference-list verifiability 和 citation-keyed grounding，而不是完整事实性保证。

## 8. 对 paper2 story / 实验设计的影响

ARISE 是 paper2 必须正面对比的强近邻。它已经覆盖 agent roles、retrieval、citation curation、knowledge base、outline synthesis、LaTeX output、LLM reviewer loop、structured feedback、revision trajectory、reference traceability audit。paper2 不能简单声称“多 agent + rubric + citation traceability”就是 novelty。

paper2 的可防守差异应是：面向 SE SLR/SMS 而非泛 survey writing；处理 structured screening/data extraction/coding decisions，而不只是文稿生成；每个包含/排除、每条 evidence cell、每个 generated claim 都保留可审计 provenance；人类审计不是事后小样本评分，而是 workflow gate；评价包含 reviewer 能否复核和重放 run record。实验可借鉴 ARISE 的 chunk-level rubric 和 eCTR，但必须补充 claim-support audit、decision log completeness、schema-valid run record 和 SE case benchmark。

## 9. 可用于写作的引用角度

可引用为“最新 agentic survey systems 已经把检索、引用整理、知识库、outline、写作和 rubric-guided refinement 集成到完整 LaTeX 生成流程中”。也可引用为“citation-keyed memory 和 evidence-locked targeted revision 是限制 hallucination/scope drift 的一种系统设计，但其报告的 reference reliability 主要验证引用条目可匹配外部数据库”。

不应引用为“已解决自动 SLR”。论文更像 automated scholarly survey paper generation，不包含标准 SLR 的 protocol registration、dual screening、data extraction adjudication 或 risk-of-bias assessment。

## 10. 待复核清单

- Supplementary materials 是否真实包含 22 个 agent prompt、topic subfolders、review output、generated drafts 和 codebase。
- AutoSurvey 只有 3 篇可得输出，baseline 数量不平衡是否影响结果。
- eCTR=1.00 是否仅对 ARISE final references 有效，还是覆盖全部生成内容和所有 baseline。
- Human evaluation 的专家背景、评分一致性和盲评设置是否在 Appendix 6 充分披露。
- 是否存在后续正式发表版本或代码仓库更新，尤其是 GPT-4.1/Gemini/Claude 版本漂移。
