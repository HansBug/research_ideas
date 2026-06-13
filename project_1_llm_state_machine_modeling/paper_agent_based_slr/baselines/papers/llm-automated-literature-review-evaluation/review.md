# Large Language Models for Automated Literature Review: An Evaluation of Reference Generation, Abstract Writing, and Review Composition

## 1. 快速结论卡片

| 字段 | 内容 |
|---|---|
| 标题 | Large Language Models for Automated Literature Review: An Evaluation of Reference Generation, Abstract Writing, and Review Composition |
| 年份 | 2024 / arXiv v5 显示 2025-08-21 更新时间 |
| 作者 / venue / 出版状态 | Xuemei Tang、Xufeng Duan、Zhenguang G. Cai；arXiv 预印本，未在本轮核验正式 peer-reviewed venue |
| 分层 | P0 |
| 阅读状态 | 已读全文文本-paper_content核验 |
| 证据等级 | 全文文本级；图表/表格细节待人工 PDF 核对 |
| 核验入口 | [bibtex.bib](./bibtex.bib)、[paper_content.txt](./paper_content.txt)、[paper.pdf](./paper.pdf) |
| 研究脉络 | LLM 自动 literature review 评价；reference hallucination；review composition evaluation |
| 引用角色 | 评价 baseline / 禁用 claim / 自动综述生成风险证据 |
| 研究任务 | 评估 LLM 在文献综述写作中的三类能力：生成参考文献、写摘要、写短综述 |
| 输入 | Annual Reviews 2023 年 51 个 review journals 中 1,105 篇综述的 title、keywords、abstract、context、reference set |
| 输出 | LLM 生成的 10 条参考文献、摘要、约 1000 词 literature review 及配套引用 |
| 覆盖阶段 | reporting、reference generation、review composition、evaluation；不覆盖真实 SLR 检索/筛选/抽取/编码流程 |
| 不覆盖阶段 | 不覆盖真实 SLR 检索/筛选/抽取/编码流程。 |
| 方法/系统形态 | 自动评价框架；非 agent 工作流；用 human-written review 作 gold standard，结合 Semantic Scholar、NLI、embedding、ROUGE、KPR 评价 |
| LLM/agent 角色 | LLM 只作为被评测生成器；没有多 agent 协作、规划 agent 或执行型 reviewer agent |
| 人审/审计机制 | 自动引用核验方法用 100 条生成引用做三人多数投票验证；没有 report-level 人工审计 gate 或 claim-to-source 审计包 |
| 人类角色 | 运行中审查者或用户反馈；需区分是否为正式审计 gate |
| 审计时机 | 原文未给出清晰审计时机或本轮未抽取 |
| 主张追踪状态 | reference metadata matching 级；无 report-level claim-to-source 审计包。 |
| 决策日志状态 | 无或仅论文叙述 |
| 冲突处理机制 | 原文未给出明确冲突处理或不适用 |
| 审计导出性 | 有表格/JSON/schema 输出线索；是否形成可审计证据包待 artifact audit。 |
| 证据溯源粒度 | reference metadata matching 与 human-written article comparison；没有 per-claim page-level provenance |
| 实验对象/数据集 | 1,105 篇 Annual Reviews 2023 综述，跨 Biology、Chemistry、Mathematics、Physics、Social Science、Technology 等类别 |
| baselines / metrics | 5 个 LLM；reference precision/recall/F1/title search rate、TRUE/GPT-4o NLI、embedding similarity、ROUGE、KPR、ANOVA、100 条引用人工验证 |
| 主要结果 | Claude-3.5-Sonnet 在 reference generation / KPR 等指标上较强，但所有模型仍有明显 reference hallucination；模型表现随学科变化 |
| 可复现资产 | 摘要称数据和代码在 anonymous repository；本轮未访问仓库与 license |
| 主要局限 | 评价指标不覆盖 fluency/结构完整性；可能有训练数据重叠；Semantic Scholar 检索可能漏召回；未评价完整 SLR methodology compliance |
| 威胁的 paper2 主张 | 威胁“自动生成综述文本/引用即可可靠”的宽泛 claim；约束 paper2 的 evaluation metrics 与 unsupported-claim 控制 |
| 支持的 paper2 主张 | 支持 paper2 将贡献收窄到可审计 evidence workflow、run record、人工审计 gate 与 claim-to-source trace，而非泛称自动综述生成。 |
| paper2 应避免的主张 | 避免声称“首次 LLM/agent 自动化 SLR”“完整覆盖 SLR 生命周期”“PRISMA 合规”，也不得把 arXiv 预印本当作 CCF/peer-reviewed 事实。 |
| 差异化要求 | paper2 必须区别于“评价 LLM 写综述”的任务，强调 SE SLR/SMS 工作流、阶段证据链、人工审计和 claim-level provenance |
| 对 paper2 实验设计的启发 | 应加入 reference hallucination、citation validity、semantic coverage、factual consistency、unsupported claim rate、人工审计一致性等指标 |

| 威胁的 paper2 主张 | 见 §8 对 paper2 story / 实验设计的影响；正式写作前需回到本 review 的证据锚点核验。 |
| 支持的 paper2 主张 | 支持 paper2 将贡献收窄到可审计 evidence workflow、run record、人工审计 gate 与 claim-to-source trace，而非泛称自动综述生成。 |
| paper2 应避免的主张 | 避免声称“首次 LLM/agent 自动化 SLR”“完整覆盖 SLR 生命周期”“PRISMA 合规”，也不得把 arXiv 预印本当作 CCF/peer-reviewed 事实。 |
| baseline 可用性 | 定性强baseline；若代码/数据可得，后续再判定是否可运行复现。 |
| 对比方式 | 协议/指标baseline |
| 代码状态 | 声称有/正文出现 GitHub 或 code 线索；本轮未打开核验 |
| 数据状态 | 声称有/正文出现 dataset 或 data availability 线索；license 未核验 |
| 许可状态 | 未核验；不得据此承诺可复现或可再分发 |
| 制品入口 | 本轮仅从 paper_content/review 识别线索；URL、commit、license 和 smoke 运行留待下一轮 artifact audit |
| 运行可行性 | 协议/指标baseline |
| 可复现资产 / 阻塞项 | 代码、数据、prompt、license、正式 venue/DOI 与 PDF 图表级数值均按 §7 / §10 待复核清单处理；未核验项不得支撑强实验比较。 |

| 模型/API 设置 | GPT-4、GPT-4o、Claude、Sonnet、Llama、DeepSeek、Qwen、GPT；具体版本/调用日期按原文与 artifact 待复核 |
| 提示词状态 | 附录/正文给出 prompt 或片段；完整可复用性待核验 |
| 温度/重复/随机种子 | temperature 0；正式复现前需回原文核对 |

| 关键结果锚点 | review.md §2 D1-D7 证据锚点 + §5/§6 实验与结果；SUMMARY 数字不得脱离单篇锚点引用 |
| 数值使用许可 | 仅文本级引用；正式写作前需 PDF 图表/表格核对 |

| 受影响主张 ID | C5,C6,C7 |
| 威胁类型 | 评价协议约束 + 禁用 claim 证据 |

## 2. D1-D7 全文核验评分

| D1 主题 | D2 流程 | D3 自动化 | D4 审计 | D5 评价 | D6 SE | D7 威胁 |
|---|---|---|---|---|---|---|
| 🟢 | 🟠 | 🟡 | 🟠 | 🟢 | 🟠 | 🟡 |

| 维度 | 评分 | 证据锚点 | 判定理由 | 相对粗筛变化 |
|---|---:|---|---|---|
| D1 主题贴合度 | 🟢 | `paper_content.txt` Abstract 与 §1：评估 LLM 自动 literature review writing，包括 reference generation、abstract writing、review composition | 主题直接落在 LLM 自动文献综述写作与可靠性评价上，和 paper2 报告生成 / 证据可靠性高度相关 | 保持强 |
| D2 SLR/SMS 流程覆盖度 | 🟠 | §3.2 Task Design：三项任务只围绕 reference generation、abstract writing、review composition | 它不执行 SLR/SMS 的检索、筛选、抽取、编码和研究质量评价，只评估写作端输出；流程覆盖应降为单端 reporting/evaluation | 从粗筛的中降为弱 |
| D3 LLM/agent 自动化深度 | 🟡 | §4.1：5 个 LLM 用官方 API、temperature 0 生成任务输出 | LLM 是生成器和被评测对象，但没有 agent 工作流、工具调用规划或人机协作流程；自动化深度是单轮/任务级生成 | 保持中但明确非 agent |
| D4 人工审计与可追踪性 | 🟠 | §4.5：100 条生成 reference 由 3 名 annotator 多数投票验证自动评价；§3.3 用 Semantic Scholar / NLI 自动核验 | 有人工验证自动引用评价可靠性的抽样，但没有可用于真实综述生产的 人工审计 gate、decision log 或 claim-to-source provenance | 从粗筛的弱保持弱，理由更明确 |
| D5 评价严谨性 | 🟢 | §4：1,105 篇 Annual Reviews，5 个 LLM，多任务、多指标、跨学科 ANOVA，100 条人工验证 kappa 0.71 / accuracy 86% | 评价规模和指标体系较完整，尤其适合作为 paper2 的 evaluation baseline 和 hallucination 风险证据 | 保持强 |
| D6 SE/CCF 相关性 | 🟠 | 数据来自 Annual Reviews，跨自然科学/社科/技术，不是 SE SLR；arXiv 预印本 | 方法学重要但不是软件工程 / CCF venue 直接 baseline | 保持弱 |
| D7 对本文 novelty 的威胁 | 🟡 | §3--4 给出自动评估框架和 LLM 写综述可靠性结论 | 它不威胁 paper2 的 agentic SE SLR workflow 主体，但强约束“自动综述生成”和“引用可靠性评价”部分；paper2 必须正面讨论其指标与风险 | 保持中 |

## 3. 论文解决的问题与背景

这篇论文关注的是 LLM 是否能够可靠承担文献综述写作中的关键生成任务。原文指出，literature review 需要收集、组织、总结大量文献，工作量大，因此研究者开始使用 ChatGPT 等 LLM 辅助写综述；但这些模型在不使用 RAG 的情况下是否能生成可靠引用、摘要和综述文本仍不清楚。

与 paper2 的距离在于：它不是一个执行 SLR/SMS 流程的系统，也不处理 inclusion/exclusion、data extraction 或 coding；它更像一个自动评价框架，用来量化 LLM 在“写综述”和“生成引用”时的 hallucination、semantic coverage 和 factual consistency。它给 paper2 的最重要启发是：如果 paper2 输出最终报告，就必须把 citation validity、claim grounding 和 hallucination 当作核心评价，而不能只展示报告文本看起来流畅。

## 4. 方法 / 系统拆解

| 子模块 | 输入 | 输出 | LLM/agent 角色 | 人工角色 | 证据锚点 |
|---|---|---|---|---|---|
| 数据集构造 | Annual Reviews 2023 的 title、keywords、abstract、contents、references | 1,105 篇 human-written review 数据集 | 无 | 无，使用人类已发表综述作 gold standard | §3.1、§4.1 |
| Reference Generation | title + keywords | 每篇 10 条 reference metadata，含 title、authors、journal、year、volume、page | 5 个 LLM 生成参考文献 | 无实时人工参与 | §3.2、Appendix Table 5 |
| Abstract Writing | title + keywords | 与原文长度接近的 abstract | 5 个 LLM 生成摘要 | 无 | §3.2 |
| Review Composition | title + keywords + abstract | 约 1000 词 literature review + 10 条引用 | 5 个 LLM 生成综述和引用 | 无 | §3.2、Appendix Table 5 |
| Reference hallucination evaluation | LLM 生成引用、Semantic Scholar 候选、human-cited references | title search rate、precision、recall、F1 | 无；自动评价管线 | 100 条样本由 3 人验证自动评价 | §3.3、§4.5 |
| Context evaluation | LLM 生成摘要/综述、人类原文 | TRUE/GPT-4o NLI、embedding similarity、ROUGE、KPR | GPT-4o 被用作 NLI / key point recall 判断组件之一 | 无常规人工评价 | §3.3、§4.1 |

其系统思路不是“LLM agent 执行综述流程”，而是“用人类综述数据构造 benchmark，再用自动指标评估 LLM 的综述生成能力”。因此它适合作为评价协议 / risk baseline，而不是流程型直接竞品。

## 5. 实验 / 评价设计

| 项 | 内容 |
|---|---|
| RQ / 评价问题 | LLM 是否能生成真实可靠引用、与 human-written abstract / review 保持 factual consistency 和 semantic coverage，以及不同学科表现是否不同 |
| 数据集/案例 | 2023 年 Annual Reviews 网站 51 个 review journals 的 1,105 篇综述；原文按 Dewey 分类到 Biology、Chemistry、Mathematics、Physics、Social Science、Technology 等类别 |
| gold/reference | human-written literature reviews 及其 reference set；100 条 LLM 生成引用的人类多数投票用于验证自动评价 |
| LLM | Claude-3.5-Sonnet-20240620、GPT-4o-2024-08-16、Qwen-2.5-72B-Instruct、DeepSeek-V3、Llama-3.2-3B-Instruct |
| prompt/setting | 三个固定 JSON 输出 prompt；temperature=0；Reference Generation 和 Review Composition 中每篇生成 10 条引用 |
| baselines | 主要是 LLM 间对比；没有传统 SLR automation / RAG 系统 baseline |
| metrics | title search rate、reference precision/recall/F1、first-author relaxed F1、TRUE/GPT-4o entailment、embedding similarity、ROUGE、KPR、ANOVA、kappa / accuracy |
| 主要数字 | Reference Generation 中 Claude F1=33.08，Llama F1=4.90；Review Composition 中 Claude reference F1=41.42、KPR=62.32；人工验证自动引用评价 kappa=0.71、accuracy=86% |
| 统计方式 | 跨学科 one-way ANOVA；引用年份/学科分布分析；100 条样本人工验证自动 evaluator |
| 成本/人工时间 | 原文未明确给出 API 成本、token 成本或人工标注时间 |
| 失败分析 | 重点分析 reference hallucination、metadata 维度错误、学科差异和可能的数据泄漏 |

## 6. 主要结果与结论

| claim | 原文证据 | 数值/表格 | 可支持的写作强度 | 注意事项 |
|---|---|---|---|---|
| LLM 仍严重存在 reference hallucination | Table 1 / Table 3 的 precision、recall、F1 | Claude 在 Reference Generation F1 最高也只有 33.08；Llama F1 为 4.90 | 强：可引用为自动综述写作的可靠性风险 | 数值来自 Annual Reviews 数据，不一定直接外推到 SE SLR |
| Review Composition 中引用准确率高于单独 Reference Generation | §4.2 / Table 3 | Claude Review Composition reference F1=41.42，高于 Reference Generation F1=33.08 | 中：说明文本和引用有互相约束效果 | 仍远不足以说明引用可靠 |
| 摘要生成指标差异不大但需要多指标评估 | Table 2 | Claude similarity 81.17，TRUE 78.90；DeepSeek GPT-4o entailment 96.84 | 中：支持多指标评价 | TRUE / GPT-4o judge 自身也可能有偏差 |
| 学科影响 reference precision | §4.4 / Table 4 / Figure 4 | Mathematics precision 较高，Chemistry 较低；citation count 与 precision 正相关 | 中：可作为领域差异风险 | 学科分类和数据来源特定 |
| 自动 reference evaluator 有一定可靠性 | §4.5 | 100 条引用，kappa=0.71，accuracy=86% | 中强：可借鉴人工抽样验证设计 | 样本只有 100 条，且 annotator 是研究团队成员 |

## 7. 局限与可复现性

| 维度 | 原文情况 | 对 paper2 的影响 |
|---|---|---|
| 数据范围 | 只使用 Annual Reviews 2023，且可能与训练数据重叠 | paper2 若用最新 SE 文献，应避免训练污染并记录检索日期 |
| 评价指标 | 作者承认没有覆盖 fluency、topic coverage、结构 coherent 等传统质量维度 | paper2 需要补 unsupported claim、traceability、人工审计和透明报告指标 |
| 搜索/引用验证 | 主要依赖 Semantic Scholar API；Google Scholar 因无开放 API 未作为主工具 | paper2 citation checking 应记录检索源、失败和漏召回风险 |
| 人工验证 | 100 条引用，3 名 annotator，多数投票；未报告更大规模人工审计 | paper2 若主打 audit，需要更系统的人审协议和错误分类 |
| 代码 / 数据 | Abstract 说匿名仓库公开数据和代码，本轮未访问验证 | 正式引用前需核验仓库、license、数据可用性和版本 |
| 模型漂移 | 固定列出模型和日期版本；但 LLM 快速迭代 | paper2 run record 必须保存精确 model_id、调用日期和 endpoint |

## 8. 对 paper2 story / 实验设计的影响

| paper2 claim | 该文作用 | 证据锚点 | 写作处理 |
|---|---|---|---|
| agent 工作流 能生成最终报告 | 削弱宽泛生成 claim | Table 1/3 显示引用生成仍有大量 hallucination | 必须改写为“生成需被审计”，不能写“可靠自动生成” |
| claim-to-source / citation verification 是必要模块 | 支持 | §3.3 reference hallucination metrics 与 §4.5 人工验证 | 把 citation validity / unsupported claim 率设为核心指标 |
| paper2 是首次 LLM automated literature review | 禁止 | §2 Related Work 和本文自身就是 automated literature review evaluation | 不得使用 firstness；改写为 SE 场景 + 可审计 workflow 的组合差异 |
| 多指标评价比单一文本相似度更合理 | 支持 | §3.3 同时使用 precision/recall/F1、NLI、embedding、ROUGE、KPR | paper2 evaluation 应至少覆盖 citation、coverage、factuality、audit cost |
| SE 场景外推 | 需要谨慎 | 数据来自 Annual Reviews，不是 SE SLR | 只能作为跨域评价协议 baseline，不是 SE 直接证据 |

## 9. 可用于写作的引用角度

- Tang 等人的评价框架显示，即使较强 LLM 在自动文献综述引用生成中仍会产生大量 hallucinated references，因此报告生成阶段必须配套 citation verification 和人工审计。
- 该文把 reference generation、abstract writing 和 review composition 分解为三个可评价任务，并用 precision/recall、NLI、ROUGE、KPR 等多指标评估，说明自动综述评价不能只依赖流畅度或单一相似度。
- 该文不是一个 SLR/SMS 执行系统；它不覆盖 inclusion/exclusion、data extraction 或 coding，因此 paper2 可将其定位为 evaluation baseline，而不是 workflow baseline。
- 它的 100 条引用人工验证可作为 paper2 设计抽样审计协议的参考，但 paper2 需要进一步扩展到 claim-to-source、per-stage decision log 和 SE SLR 场景。

## 10. 待复核清单

| 优先级 | 待复核项 | 原因 |
|---|---|---|
| 高 | 打开 PDF 核对 Table 1--4、Figure 2--4 与 Appendix prompt / data distribution | `paper_content.txt` 已清理 PDF 提取残留 NUL；表格解析仍可能有格式误差 |
| 高 | 访问 anonymous repository，确认代码、数据、license、commit / snapshot | Abstract 声称公开，但本轮未在线核验 |
| 中 | 核验是否已有正式发表版本或后续 leaderboard | arXiv v5 更新时间为 2025-08-21，可能存在新版本或正式 venue |
| 中 | 复核 TRUE / GPT-4o / KPR 的实现细节和 prompt | 若 paper2 采用类似指标，需要可复现细节 |
| 中 | 评估 Annual Reviews 数据与 SE SLR 数据差异 | 防止把跨域结果过度外推到 SE 社区 |
