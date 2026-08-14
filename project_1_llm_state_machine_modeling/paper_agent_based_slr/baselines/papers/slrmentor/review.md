# SLRMentor: An LLM-Based Tool Supporting Learning of SLR in Software Engineering

## 1. 快速结论卡片

| 字段 | 内容 |
|---|---|
| 标题 | SLRMentor: An LLM-Based Tool Supporting Learning of SLR in Software Engineering |
| 年份 | 2026 |
| 作者 / venue / 出版状态 | Rodolfo Gil-Pereira、Ronnie de Souza Santos 等；arXiv:2606.07831; 本轮未核验正式 peer-reviewed / CCF 状态 |
| 分层 | P1 |
| 阅读状态 | 已读全文文本-paper_content核验 |
| 证据等级 | 全文文本级；图表/表格细节待人工 PDF 核对 |
| 核验入口 | [bibtex.bib](./bibtex.bib)、[paper_content.txt](./paper_content.txt)；未人工打开 PDF 核对图表 |
| 研究脉络 | SLR/SMS 筛选、语料过滤与规划 |
| 引用角色 | 模块级 baseline / 重要相关工作定位 |
| LLM/agent 角色 | LLM/agent 执行部分检索、筛选、抽取、组织、生成或评价环节；具体阶段见方法/覆盖阶段字段。 |
| 证据溯源粒度 | 未见可执行 provenance；只能作为背景或弱审计证据。 |
| 输入 | 用户提出的 SLR 学习问题、研究目标、搜索目标和 inclusion/exclusion criteria 草案 |
| 输出 | 解释型问答、search string 建议、criteria 解释、学习支持与 planning scaffold |
| 方法/系统形态 | LLM-based conversational assistant + RAG + structured chat components；不是 screening / extraction / synthesis agent |
| 覆盖阶段 | 只覆盖 SLR planning 早期阶段：概念理解、search string construction、criteria reasoning |
| 不覆盖阶段 | 不覆盖检索策略冻结、全文抽取、编码、综合、报告生成和报告级 claim-to-source。 |
| 人审/审计机制 | 以 guideline-grounded explanations 和学生自评为主；无正式审计链、无判定日志、无证据包 |
| 人类角色 | 无正式人审 gate；若有评价者仅作实验评价 |
| 审计时机 | 原文未给出清晰审计时机或本轮未抽取 |
| 主张追踪状态 | 无明确 claim-to-source trace 或本轮未核验 |
| 决策日志状态 | 无或仅论文叙述 |
| 冲突处理机制 | 原文未给出明确冲突处理或不适用 |
| 审计导出性 | 不可导出或仅论文叙述；正式写作不得承诺可审计 artifact。 |
| 实验/指标 | 8 名课程学生中 4 名自愿参与；Likert + open-ended feedback；无统计显著性主实验 |
| 模型/API 设置 | Gemini；具体版本/调用日期按原文与 artifact 待复核 |
| 提示词状态 | 正文提到 prompt；完整模板待核验 |
| 温度/重复/随机种子 | 原文未给出或本轮未抽取 temperature / seed / repeats |
| 主要发现 | 工具主要被当作 learning-oriented scaffold，而非最终规划器；有助于解释方法、构造搜索式和理解 criteria，但仍需主动判断 |
| 关键结果锚点 | review.md §2 D1-D7 证据锚点 + §5/§6 实验与结果；SUMMARY 数字不得脱离单篇锚点引用 |
| 数值使用许可 | 仅文本级引用；正式写作前需 PDF 图表/表格核对 |
| 对 paper2 的作用 | 只可作为教育型 SLR assistant 背景，不能作为 screening 或 evidence synthesis 强 baseline |
| 受影响主张 ID | C4,C5 |
| 威胁类型 | 背景定位 |
| 威胁的 paper2 主张 | 只可作为教育型 SLR assistant 背景，不能作为 screening 或 evidence synthesis 强 baseline |
| 支持的 paper2 主张 | 支持 paper2 把筛选阶段评价扩展到 false negative、模型变异、人工复核路由、成本和决策日志，而不是只报告 accuracy/F1。 |
| paper2 应避免的主张 | 避免把筛选 accuracy/F1 当作完整 SLR 自动化贡献；避免忽视 false negative、模型变异和人工复核成本。 |
| baseline 可用性 | 协议/指标baseline或局部强baseline；主要用于模块级对照与写作定位。 |
| 对比方式 | 仅related-work背景 |
| 代码状态 | 未提及源码；只识别到 live version 与验证数据入口 |
| 数据状态 | 验证数据给出 figshare 入口；本轮未打开 URL 或核验 license |
| 许可状态 | 未核验；不得据此承诺可复现或可再分发 |
| 制品入口 | 本轮仅做 paper_content 文本级线索识别，未打开外部 URL；具体 URL、commit、license 和 smoke 运行留待下一轮 artifact audit |
| 运行可行性 | 仅related-work背景 |
| 可复现资产 / 阻塞项 | 代码、数据、prompt、license、正式 venue/DOI 与 PDF 图表级数值均按 §7 / §10 待复核清单处理；未核验项不得支撑强实验比较。 |

## 2. D1-D7 全文核验评分

emoji 口径见 [../../GUIDE.md](../../GUIDE.md)；本表单元格只放 emoji。

| D1 主题 | D2 流程 | D3 自动化 | D4 审计 | D5 评价 | D6 SE | D7 威胁 |
|---|---|---|---|---|---|---|
| 🟢 | 🟠 | 🟡 | 🟠 | 🟠 | 🟢 | 🟠 |

| 维度 | 评分 | 全文证据锚点 | 判定理由 |
|---|---:|---|---|
| D1 主题贴合度 | 🟢 | `paper_content.txt` Abstract / Page 1；§3 / Page 3--4 | 论文明确面向 software engineering 中的 SLR 学习与 planning，和 paper2 的方法论背景相关。 |
| D2 SLR/SMS 流程覆盖度 | 🟠 | `paper_content.txt` Abstract / Page 1；§3 Task Definition / Page 4；§6 / Page 9 | 只支持 planning：概念理解、search string construction、criteria reasoning；不覆盖真实文献筛选、抽取、编码、综合或报告。 |
| D3 LLM/agent 自动化深度 | 🟡 | `paper_content.txt` §3 Tool Development / Page 4；§6 / Page 6--7 | 有 LLM 对话和 RAG 支持，但目标是解释与学习支架，不是多阶段 agent 自动执行。 |
| D4 人工审计与可追踪性 | 🟠 | `paper_content.txt` §3 Validation / Page 4--5；§5.2 / Page 9 | 用户可比较 tool-generated 与手工产物，说明存在反思和人工判断，但没有系统级审计日志或 claim-to-source 机制。 |
| D5 评价严谨性 | 🟠 | `paper_content.txt` §3 Validation / Page 4--5；§4 Results / Page 5--7 | 只有 4 名参与者的 formative pilot，Likert + open-ended 反馈，不是强统计评价。 |
| D6 SE / CCF 相关性 | 🟢 | `paper_content.txt` Abstract / Page 1；References [2], [10], [22], [23] | 直接面向软件工程教育和 EBSE / SLR 教学，和本仓库目标社区强相关。 |
| D7 novelty 威胁强度 | 🟠 | `paper_content.txt` §5 Discussion / Page 7--9；§6 Conclusion / Page 9 | 它威胁的是“SLR planning assistant / learning scaffold”叙事，而不是自动筛选或证据综合；对 paper2 仅是弱到中等的教育型背景。 |

## 3. 论文解决的问题与背景

论文关注的是 SLR 教学问题，而不是把 SLR 自动化到尽头。作者指出，在 EBSE 课程中，初学者常常能完成产出，但对为什么这样设计 search string、为什么这样写 criteria、为什么这样规划 review 过程并不真正理解。规划阶段又是 SLR 质量和可复现性的关键，因此他们想做一个能解释方法、帮助学习、降低入门门槛的 conversational assistant。

这意味着 SLRMentor 的目标不是代替审稿或筛选，而是把 planning decisions 显性化。它关心的是 novice researchers 如何学习 SLR 方法，特别是 search string construction 和 inclusion/exclusion criteria 的 reasoning。对 paper2 来说，这篇更适合作为教育场景和 human explanation scaffold 的参考，而不是 screening 或 extraction baseline。

## 4. 方法 / 系统拆解

方法上，作者采用 Design Science，把 `SLRMentor` 当作一个软件 artifact。系统是一个对话式助手，使用两个通用 LLM（OpenAI 和 Google Gemini）回答三类任务：Mentor Chat 提供 SLR 概念和流程解释，Search String Chat 帮助构造检索式，Criteria Chat 帮助推导 inclusion/exclusion criteria。输出带有解释，强调方法论理解而不是直接照搬答案。

系统还集成了 retrieval-augmented generation，把回答锚定到 curated SLR guidelines 和方法文档，减少不受控生成。作者强调，这是一个 learning-oriented support，而不是最终 artifact 生产器。用户需要自行判断、修订和比较工具建议与手工结果。

验证环节是教学型 pilot。研究在软件工程研究生课程里进行，8 名学生中 4 名自愿匿名参与。参与者先完成课程作业，再用工具处理自己已经做过的同一题目，随后填写 Likert + open-ended 问卷。评价关注清晰度、一致性、是否支持学习、是否便于反思，以及与手工产物的可比性。论文还给出了 figshare 数据链接，说明验证数据可查，但不等于完整实验包。

## 5. 实验 / 评价设计

RQ 很单一：对软件工程研究者而言，一个 conversational assistant 如何支持他们学习 SLR 过程。实验不是性能竞赛，而是 formative evaluation。样本是 4 名博士和 4 名硕士中的 4 名志愿者，任务是对自己课程中做过的 mapping study 或 rapid review 进行 tool-assisted 重访。

指标主要是主观反馈。Table 1--3 汇总了参与者对 Mentor Chat、Search String Chat 和 Criteria Chat 的 Likert 反应。作者没有报告 accuracy、F1、ground-truth match rate 这类传统分类指标，也没有与其他系统做系统性对照。分析方式也主要是描述统计和质性解释，没有统计显著性检验。

因此，这篇论文的“评测”本质上是教育工具可用性和学习支持价值的初步验证，不是任务完成度或自动化准确率验证。它说明工具是否帮助理解、是否便于反思，而不是工具是否能稳定代替人完成 SLR planning。

## 6. 主要结果与结论

结论很清楚：SLRMentor 主要被参与者当成学习支架。Mentor Chat 的解释通常被认为清晰且与已知 SLR 实践一致；Search String Chat 帮助理解关键词、同义词和 Boolean operator 的作用；Criteria Chat 的反馈更分化，但仍被一些参与者视为初学阶段有帮助。

论文最重要的结论不是“它自动化了什么”，而是“它让 method reasoning 更显性”。参与者反复提到工具有助于 parsing complicated requirements、理解 search strategy、比较自己的手工结果与系统建议，但依然需要主动判断和 refinement。作者因此把系统定位为 complementary scaffold，而不是 final decision maker。

在论文末尾，作者还明确指出未来工作要把支持扩展到 study selection、data extraction、quality assessment 和 synthesis。这个表述说明当前版本仍停留在 planning 层，不应被误读为完整 SLR 代理。

## 7. 局限与可复现性

局限主要来自样本和范围。pilot 只有 4 名学生，且都来自同一门研究生课程，因此泛化性有限。作者自己也承认，这个验证不旨在提供统计意义上的强结论，而是初步判断工具是否有学习支持价值。

可复现性上，论文给了 live version 和 figshare 数据链接，属于不错的教育工具实践。但它没有给出可迁移到自动筛选任务的稳定 benchmark，也没有公开一个可直接复用的评测协议。RAG 依赖 curated guidelines，因此工具行为会受知识库内容影响。

## 8. 对 paper2 story / 实验设计的影响

paper2 不应把 SLRMentor 当成筛选或证据综合 baseline。它真正提供的是“解释型 SLR assistant 应该如何帮助用户理解 planning decisions”的背景：用 RAG 锚定指南，用对话暴露 reasoning，让用户比较工具输出和自己的判断。

如果 paper2 涉及 human-in-the-loop 或 explanation UI，这篇可以作为低风险的教育型参考，但必须明确差异：paper2 若是执行型系统，需要处理真实文献流、阶段状态、审计日志和可复核证据链；SLRMentor 只支持学习规划，不产出最终 review artifact。

## 9. 可用于写作的引用角度

- SLRMentor 表明，LLM 辅助工具在 SLR 教学中更适合扮演学习支架，而不是自动决策器。
- 该工具主要支持 search string construction 和 inclusion/exclusion criteria reasoning，这说明规划阶段本身就值得单独建模，而不只是筛选阶段。
- 小规模 pilot 结果显示，初学者更看重解释与反思支持；这可作为本文设计 human-friendly explanation 的背景，但不能替代自动化评测证据。
- 作者明确把后续扩展留给 study selection、extraction 和 synthesis，因此当前版本不应被视为完整 SLR automation baseline。

## 10. 待复核清单

- 人工打开 PDF 核对 Table 1--3 的参与者回答分布与措辞。
- 复核 figshare 链接内容是否包含原始问卷、匿名响应或仅部分数据。
- 若用于 paper2 教育/教学背景，确认其 live version 当前是否仍可访问。
- 注意作者在文中把任务写成 learning support，后续写作不要把它提升为自动筛选系统。
