# SurveyEval: Towards Comprehensive Evaluation of LLM-Generated Academic Surveys

## 1. 快速结论卡片

| 字段 | 内容 |
|---|---|
| 标题 | SurveyEval: Towards Comprehensive Evaluation of LLM-Generated Academic Surveys |
| 年份 | 2025（BibTeX/arXiv；正文 ACM reference 写 2026 preprint/in progress，需后续核验） |
| 作者 / venue / 出版状态 | Jiahao Zhao、Shuaixing Zhang 等；arXiv:2512.02763; 本轮未核验正式 peer-reviewed / CCF 状态 |
| 分层 | P2 |
| 阅读状态 | 已读全文文本-paper_content核验 |
| 证据等级 | 全文文本级；图表/表格细节待人工 PDF 核对 |
| 核验入口 | [bibtex.bib](./bibtex.bib)、[paper_content.txt](./paper_content.txt) |
| 研究脉络 | 自动 survey / literature review 生成与评价 |
| 引用角色 | 背景近邻 / 局部 claim 风险或禁用 claim 证据 |
| LLM/agent 角色 | LLM 参与单阶段或少数阶段任务；未形成完整 agent 式 SLR 工作流。 |
| 证据溯源粒度 | 人工核验或 benchmark/gold 级；未必有 claim-level provenance。 |
| 输入 | 自动 survey 系统以 survey title 为 query 生成的长文 survey、human-authored reference surveys、aligned reference literature collections。 |
| 输出 | SurveyEval benchmark，包括 overall quality、outline coherence、引用准确性 三类评价结果。 |
| 方法/系统形态 | 自动 survey 质量评价 benchmark，使用 LLM-as-a-Judge 加 human reference 和 principle-based outline judging；不是 SLR 执行系统。 |
| 覆盖阶段 | 覆盖 retrieval/organization/content synthesis 系统的输出评价、outline 评价和 reference list 评价；不覆盖 SLR 检索、筛选、抽取、编码过程。 |
| 不覆盖阶段 | 不覆盖SLR 检索、筛选、抽取、编码过程。 |
| 人审/审计机制 | 使用 human-written reference surveys 和 reference literature collections 作为评价锚点；没有人工审计日志或 claim-level provenance。 |
| 人类角色 | 领域专家gold / 标注者 / 事后评价者（具体角色见人审机制字段） |
| 审计时机 | 仅评价阶段 / 运行后审计 |
| 主张追踪状态 | reference survey / reference literature collection 评价级；无 claim-level provenance。 |
| 决策日志状态 | 无或仅论文叙述 |
| 冲突处理机制 | 原文未给出明确冲突处理或不适用 |
| 审计导出性 | 不可导出或仅论文叙述；正式写作不得承诺可审计 artifact。 |
| 实验/指标 | 7 个学科、38 个 topics；整体质量 1-5 分，outline 三维 1-10 分，reference 用 Recall/Precision/F1；比较 Kimi、GLM、Doubao、Chengpian、SurveyX、SurveyGo、ScienceOne。 |
| 模型/API 设置 | Kimi、GLM；具体版本/调用日期按原文与 artifact 待复核 |
| 提示词状态 | 正文提到 prompt；完整模板待核验 |
| 温度/重复/随机种子 | 重复；正式复现前需回原文核对 |
| 主要发现 | 专用 survey-generation systems 总体优于通用长文/论文写作系统；ScienceOne 在 reference evaluation 中高于 SurveyX；citation reliability 仍是弱点。 |
| 关键结果锚点 | review.md §2 D1-D7 证据锚点 + §5/§6 实验与结果；SUMMARY 数字不得脱离单篇锚点引用 |
| 数值使用许可 | 仅文本级引用；正式写作前需 PDF 图表/表格核对 |
| 对 paper2 的作用 | 可作为 report/survey 生成 评价协议参照，尤其是 引用准确性、veracity、有证据支撑的断言 和 以人工参考为锚点的 LLM-as-a-Judge。 |
| 受影响主张 ID | C5,C6 |
| 威胁类型 | 评价协议约束 + 禁用 claim 证据 |
| 威胁的 paper2 主张 | 可作为 report/survey 生成 评价协议参照，尤其是 引用准确性、veracity、有证据支撑的断言 和 以人工参考为锚点的 LLM-as-a-Judge。 |
| 支持的 paper2 主张 | 支持 paper2 把报告生成 claim 收窄为“生成必须可审计”，并把 citation validity、unsupported claim 和 有证据支撑的断言 纳入评价。 |
| paper2 应避免的主张 | 避免声称自动 survey / review generation 尚无人研究；避免把文本流畅度、引用准确率或 LLM-as-Judge 总分等同于 SLR/SMS 方法学可靠性。 |
| baseline 可用性 | 仅related-work背景或局部强近邻；不作为主流程可运行 baseline。 |
| 对比方式 | 协议/指标baseline |
| 代码状态 | 未提及源码入口；本轮不得写成 code 可用 |
| 数据状态 | 构建 SurveyEval benchmark；公开入口与 license 本轮未识别，待核验 |
| 许可状态 | 未核验；不得据此承诺可复现或可再分发 |
| 制品入口 | 本轮仅做 paper_content 文本级线索识别，未打开外部 URL；具体 URL、commit、license 和 smoke 运行留待下一轮 artifact audit |
| 运行可行性 | 协议/指标baseline |
| 可复现资产 / 阻塞项 | 代码、数据、prompt、license、正式 venue/DOI 与 PDF 图表级数值均按 §7 / §10 待复核清单处理；未核验项不得支撑强实验比较。 |

## 2. D1-D7 全文核验评分

| D1 主题 | D2 流程 | D3 自动化 | D4 审计 | D5 评价 | D6 SE | D7 威胁 |
|---:|---:|---:|---:|---:|---:|---:|
| 🟡 | 🟡 | 🟡 | 🟡 | 🟢 | 🟠 | 🟠 |

| 维度 | 评分 | 全文证据锚点 | 判定理由 |
|---|---:|---|---|
| D1 主题贴合度 | 🟡 | `paper_content.txt:19-36`, `paper_content.txt:58-77` | 论文面向 LLM-generated academic surveys 的系统评价，和 literature review/survey 生成 相关；但不是 systematic literature review 或 evidence synthesis workflow。 |
| D2 SLR/SMS 流程覆盖度 | 🟡 | `paper_content.txt:20-23`, `paper_content.txt:151-154`, `paper_content.txt:228-241` | 被评系统包含 retrieval、organization、content synthesis，benchmark 评价内容、outline 和 references；这些覆盖 review composition 的多个输出维度，但不覆盖 screening、data extraction、coding 或 full SLR protocol。 |
| D3 LLM/agent 自动化深度 | 🟡 | `paper_content.txt:242-283`, `paper_content.txt:309-320` | SurveyEval 使用 LLM-as-a-Judge 评测 generated surveys，并对不同系统的生成结果做统一评价；自动化深度体现在 evaluator，而非多阶段 agent review execution。 |
| D4 人工审计与可追踪性 | 🟡 | `paper_content.txt:151-154`, `paper_content.txt:253-274`, `paper_content.txt:228-241` | human-authored reference surveys 和 reference literature collections 提供评价锚点，reference metrics 可检查 citation list；但没有保存生成过程决策日志、人工审计记录或 claim-to-source trace。 |
| D5 评价严谨性 | 🟢 | `paper_content.txt:137-168`, `paper_content.txt:195-215`, `paper_content.txt:287-357` | 有跨学科 benchmark、多个系统、明确指标和主结果表，且把内容、结构、引用分开评价；短文未给出 judge prompt/model 和人工一致性细节，但评价设计仍比普通 demo 扎实。 |
| D6 SE / CCF 相关性 | 🟠 | `paper_content.txt:37-45`, `paper_content.txt:140-150` | 主题是泛 academic survey evaluation，学科含 Computer Science 和 STEM，不是软件工程或 CCF SE venue；对 paper2 是方法学背景。 |
| D7 对本文 novelty 的威胁强度 | 🟠 | `paper_content.txt:350-357`, `paper_content.txt:358-364` | 它威胁 paper2 的报告生成评价和 citation reliability 评价口径，但不覆盖 agent-based SLR workflow、人工审计 gate、SE setting 或 stage-level run record。 |

## 3. 论文解决的问题与背景

SurveyEval 解决的是自动 academic survey 生成系统的评价问题。作者指出，LLM-based automatic survey systems 已经把 retrieval、organization 和 content synthesis 组织成端到端生成管线，但近期工作更关注构建生成系统，如何评价这些复杂系统仍然不足。现有评价常依赖单个案例的 ad-hoc human subjective scoring，缺少可复用、可量化、能支持跨系统比较和 capability diagnosis 的 benchmark。

它的背景与 paper2 的报告阶段直接相关。paper2 如果生成 SLR/SMS 报告，不能只展示文本流畅度，也不能只让一个 LLM judge 给总分。SurveyEval 把评价拆成 overall quality、outline coherence、引用准确性，并引入 human-written reference surveys 作为 anchor，提供了一个可借鉴但仍需审慎使用的评价结构。

## 4. 方法 / 系统拆解

SurveyEval 的输入包括多个自动 survey 系统针对同一 survey title/query 生成的 survey、人工撰写的高质量 reference survey，以及对齐的 reference literature collections。数据集覆盖 7 个学科，共 38 个 topics，其中 Computer Science 20 个 topics，六个 STEM disciplines 包括 astronomy、biology、chemistry、geography、aerospace、physics 共 18 个 topics。每个 topic 都有目标系统生成 survey、human-authored reference survey 和用于 citation verification 的 reference literature collection。

评价分三部分。第一，Overall content quality 使用 LLM-as-a-Judge with human-written reference。评价维度包括 coverage、structure、relevance、synthesis、critical analysis，以及扩展的 veracity、originality proportion、depth of content，统一采用 1-5 分。这里的 human reference 不是最终真理，而是 judging model 的质量锚点，用来减少 rubric-only judge 对空泛长文的高估。

第二，Outline evaluation 使用 principle-based LLM-as-a-Judge，不使用 human reference。作者认为 outline 较短，直接与人工 outline 对比会过于僵硬，因此使用 structural organization、content value、descriptiveness 三维，每维 1-10 分。第三，Reference evaluation 使用 Citation Recall、Citation Precision 和 F1，直接比较生成 survey 的 reference list 与 human-written survey/reference set 的对齐程度。

全文没有把 survey 生成 本身拆成 agent roles。被评系统包括通用长文写作系统 Kimi、GLM，paper-writing systems Chengpian、Doubao，以及 dedicated survey-generation systems SurveyX、SurveyGo、ScienceOne。实验设置是所有系统接收相同 original survey title 作为 query，并且都具备 web retrieval 能力。

## 5. 实验 / 评价设计

论文没有显式列出 RQ，但实验设计可以还原为三个问题：如何构建跨学科 survey evaluation benchmark；不同类型的自动 survey 系统在内容质量、outline coherence 和 引用准确性 上表现如何；human reference 能否让 LLM-as-a-Judge 对高层次 survey quality 更敏感。

数据集统计显示 38 个 topics 平均 26.1 个 sections、120.6 个 references。Computer Science 有 20 个 topics，平均 34.7 个 sections、220.2 个 references；六个 STEM disciplines 每类 3 个 topics。系统类别和输入控制较清楚：所有系统使用同一 title query，评价标准一致。指标方面，content overall 使用 8 个 1-5 维度；outline 使用 Struc./Cont./Desc. 三个 1-10 维度；reference 使用 Recall、Precision、F1。

人工标注/专家评审方面，文中依赖 human-authored high-quality reference surveys 作为 anchor，并有 aligned reference literature collections；但没有说明 reference surveys 的作者资质、撰写流程、质量审核、inter-annotator agreement，也没有报告 LLM judge 的具体模型、prompt、温度或重复运行稳定性。这些是后续使用该 benchmark 思路时必须补足的证据缺口。

## 6. 主要结果与结论

Overall Evaluation 显示，专用 survey-generation systems 分数最高。Table 2 中，Computer Science 上 ScienceOne 平均 4.14、SurveyGo 3.99，高于 Kimi 3.26、GLM 3.36、Doubao 3.46、Chengpian 2.53、SurveyX 2.77。Six STEM Disciplines 上 ScienceOne 平均 4.36、SurveyGo 4.34，也高于通用/论文写作系统。作者总结为：通用长文模型语言流畅和相关性较好，但 originality、synthesis、critical analysis 弱；paper-writing systems 结构更强但模板化；专用系统有更清晰 taxonomy、更连贯 synthesis 和更好的 fact-opinion separation。

Outline Evaluation 中，专用 survey-generation systems 整体更强。Computer Science 上 ScienceOne total 24.55、SurveyGo 23.69、Doubao 23.62、GLM 23.13、SurveyX 22.37；Six STEM 上 ScienceOne 23.56、SurveyGo 22.17、SurveyX 22.08，GLM 14.33 明显偏低。作者认为有效 outline design 既要捕捉结构，也要体现 scholarly intent。

Reference Evaluation 只比较了能输出完整 reference lists 的 SurveyX 和 ScienceOne。SurveyX Recall/Precision/F1 为 76.85/75.09/75.96，ScienceOne 为 90.58/84.28/87.32。作者据此指出 ScienceOne 文献 grounding 更强、错误或不匹配引用更少；同时 citation reliability，尤其是避免 unsupported references，仍是很多系统的关键弱点。

## 7. 局限与可复现性

论文篇幅较短，结论可用但复现信息不足。第一，正文没有明确 judge model、prompt、temperature、重复次数和方差，难以判断 LLM-as-a-Judge 的稳定性。第二，human-written reference surveys 的构造与质量控制没有充分展开。第三，reference evaluation 的 ground-truth reference set 来自 human survey/reference collection，但不同合格 survey 可能引用不同代表性文献，precision/recall 可能惩罚合理替代引用。第四，论文没有在 `paper_content.txt` 中出现代码或数据公开链接，当前只能把 benchmark 设计作为方法线索，而不能直接复跑。

此外，本地 BibTeX 年份为 2025，正文 ACM reference 写 2026 且 DOI 是 placeholder，说明版本状态仍不稳定。正式引用前必须核验 arXiv、正式 proceedings 或 DOI。

## 8. 对 paper2 story / 实验设计的影响

SurveyEval 对 paper2 最大价值在评价层，而非方法层。paper2 如果生成 SLR/SMS 报告，可以借鉴三分法：内容质量、结构/outline、引用或证据 grounding。尤其是 veracity、有证据支撑的断言、reference precision/recall/F1 可以转化成 paper2 的 claim-to-source 和 unsupported claim 指标。

但 paper2 不能照搬其 LLM-as-a-Judge 作为唯一质量证据。SurveyEval 自己也依赖 human reference 来减少 rubric-only judge 的宽松评分。paper2 若使用 LLM judge，应保留人工抽查、judge prompt、judge model version、重复运行和 disagreement analysis，并把评价目标收窄到可证据核验的 factuality/citation/claim support，而不是泛泛“综述质量”。

## 9. 可用于写作的引用角度

1. 可作为自动 survey/报告生成 评价相关工作：SurveyEval 把 LLM-generated academic surveys 的评价拆成 overall quality、outline coherence 和 引用准确性。
2. 可作为 citation grounding 指标来源：生成 survey 的 reference list 可用 recall、precision、F1 与 human reference collection 比较，但应承认合理替代引用的限制。
3. 可作为 LLM judge 风险缓解例子：human-written reference survey 可为 judge 提供上下文锚点，减少 rubric-only 评分对空泛文本的过度宽容。
4. 不应把它写成 SLR 自动化工具或 SE baseline；它是泛学科 survey evaluation benchmark。

## 10. 待复核清单

1. 当前只读 `paper_content.txt`，未回 PDF 核对 Figure 1 和表格排版。
2. 需核验年份、正式 venue 和 DOI：本地 BibTeX 为 2025，正文写 2026 preprint/in progress 且 DOI placeholder。
3. 需查找是否公开 benchmark 数据、human reference surveys、judge prompts 和 evaluation scripts。
4. 若 paper2 采用其 reference metrics，需要设计对“合理但非 reference set 文献”的人工复核机制，避免把 citation diversity 误判为 hallucination。
