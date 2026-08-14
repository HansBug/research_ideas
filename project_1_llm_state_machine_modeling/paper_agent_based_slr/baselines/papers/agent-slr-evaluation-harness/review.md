# Evaluating AI-based Scientific Knowledge Synthesis with Epidemiological Systematic Reviews

## 1. 快速结论卡片

| 字段 | 内容 |
|---|---|
| 标题 | Evaluating AI-based Scientific Knowledge Synthesis with Epidemiological Systematic Reviews |
| 年份 | 2026 |
| 作者 / venue / 出版状态 | Shreyansh Padarha、Ryan Othniel Kearns 等；arXiv:2603.22327; 本轮未核验正式 peer-reviewed / CCF 状态 |
| 分层 | P0 |
| 阅读状态 | 已读全文文本-paper_content核验；未人工打开 PDF 图表，不写图表级核对结论 |
| 证据等级 | 全文文本级；图表/表格细节待人工 PDF 核对 |
| 核验入口 | [bibtex.bib](./bibtex.bib)、[paper_content.txt](./paper_content.txt)、[paper.pdf](./paper.pdf) |
| 研究脉络 | agent式 SLR 工作流与评价基准 |
| 引用角色 | 直接新颖性门槛 / 强 baseline |
| LLM/agent 角色 | LLM 参与单阶段或少数阶段任务；未形成完整 agent 式 SLR 工作流。 |
| 证据溯源粒度 | 人工核验或 benchmark/gold 级；未必有 claim-level provenance。 |
| 输入 | WHO priority pathogen 相关系统综述的检索记录、开放全文 PDF、PERG 专家筛选与抽取标注 |
| 输出 | AgentSLR 数据集、分阶段 评价基准、筛选/抽取指标、成本与专家验证结果 |
| 方法/系统形态 | LLM-assisted SLR workflow + stage-isolated 评价基准；含检索、筛选、OCR、结构化抽取和报告生成组件 |
| 覆盖阶段 | 检索、题摘筛选、PDF-to-Markdown、全文筛选、参数/模型/暴发抽取；报告生成有流程但主文说明不纳入评价构造 |
| 不覆盖阶段 | 不覆盖阶段需按全文方法章节复核；当前不得据此写“完整覆盖 SLR 生命周期”。 |
| 人审/审计机制 | PERG 专家标注作 human reference，六名流行病学专家做输出质量审计；附录描述 HITL validation interface，但正文不等同完整 claim-level provenance 系统 |
| 人类角色 | 领域专家gold / 标注者 / 事后评价者（具体角色见人审机制字段） |
| 审计时机 | 仅评价阶段 / 运行后审计 |
| 主张追踪状态 | benchmark/gold 级与专家评价；不等同生产期报告级 claim-to-source trace。 |
| 决策日志状态 | per-stage 叙述级；结构化日志待核验 |
| 冲突处理机制 | 原文未给出明确冲突处理或不适用 |
| 审计导出性 | 有表格/JSON/schema 输出线索；是否形成可审计证据包待 artifact audit。 |
| 实验/指标 | 16,248 article records；3,808 parameter、687 model、189 outbreak extractions；五个 frontier reasoning models；precision、recall、macro F1、field-level F1、专家评分、成本 |
| 模型/API 设置 | GPT-5、Claude、Sonnet、Opus、DeepSeek、Kimi、GLM、GPT；具体版本/调用日期按原文与 artifact 待复核 |
| 提示词状态 | 附录/正文给出 prompt 或片段；完整可复用性待核验 |
| 温度/重复/随机种子 | 原文未给出或本轮未抽取 temperature / seed / repeats |
| 主要发现 | 无单一模型支配全流程；结构化抽取是瓶颈，平均 field-level extraction F1 未超过 0.67；human abstract triage 可把 full-text 筛选 recall 提到 0.92；成本最高低可差 96 倍 |
| 关键结果锚点 | review.md §2 D1-D7 证据锚点 + §5/§6 实验与结果；SUMMARY 数字不得脱离单篇锚点引用 |
| 数值使用许可 | 仅文本级引用；正式写作前需 PDF 图表/表格核对 |
| 对 paper2 的作用 | 强约束 paper2 的 evaluation story：不能只声称自动化 SLR，而要证明 SE 场景、证据链、run record、人审 gate 和失败分类的差异 |
| 受影响主张 ID | C1,C2,C5,C7 |
| 威胁类型 | 直接覆盖 + 评价协议约束 |
| 威胁的 paper2 主张 | 强约束 paper2 的 evaluation story：不能只声称自动化 SLR，而要证明 SE 场景、证据链、run record、人审 gate 和失败分类的差异 |
| 支持的 paper2 主张 | 支持 paper2 将贡献收窄到可审计 evidence workflow、run record、人工审计 gate 与 claim-to-source trace，而非泛称自动综述生成。 |
| paper2 应避免的主张 | 避免写“首次 agentic SLR / 首次自动化 evidence synthesis”；必须承认跨域强近邻并收窄到 SE 场景和可审计证据包。 |
| baseline 可用性 | 定性强baseline；若代码/数据可得，后续再判定是否可运行复现。 |
| 对比方式 | 可复现需改造 / 阶段化评价协议baseline |
| 代码状态 | 给出代码/数据入口；本轮未打开 URL 核验，不能承诺可运行 |
| 数据状态 | 公开数据线索；原文称 HuggingFace/benchmark dataset，但本轮未打开 URL 或核验 license |
| 许可状态 | 未核验；不得据此承诺可复现或可再分发 |
| 制品入口 | 本轮仅做 paper_content 文本级线索识别，未打开外部 URL；具体 URL、commit、license 和 smoke 运行留待下一轮 artifact audit |
| 运行可行性 | 可复现需改造 / 阶段化评价协议baseline |
| 可复现资产 / 阻塞项 | 代码、数据、prompt、license、正式 venue/DOI 与 PDF 图表级数值均按 §7 / §10 待复核清单处理；未核验项不得支撑强实验比较。 |

## 2. D1-D7 全文核验评分

| D1 主题 | D2 流程 | D3 自动化 | D4 审计 | D5 评价 | D6 SE | D7 威胁 |
|---|---|---|---|---|---|---|
| 🟢 | 🟢 | 🟢 | 🟡 | 🟢 | 🟠 | 🟢 |

| 维度 | 评分 | 全文证据锚点 | 判定理由 |
|---|---:|---|---|
| D1 主题贴合度 | 🟢 | `paper_content.txt` Page 1 Abstract；Page 3 §Evaluation Harness | 论文直接把 SLR 作为 LLM scientific knowledge synthesis 的评价场景，且提出 AgentSLR 数据集和 harness，不是泛泛谈科研助手。 |
| D2 SLR/SMS 流程覆盖度 | 🟢 | Page 2 Figure 1；Page 3 §3.1；Page 4 §3.2 | 明确覆盖检索、题摘筛选、PDF 转换、全文筛选、结构化抽取，并有报告生成流程；虽然报告生成未被评价，流程覆盖仍达到强档。 |
| D3 LLM/agent 自动化深度 | 🟢 | Page 3-4 §3.1；Page 5 §4.2 | 使用 LLM 完成多阶段筛选、OCR 后全文处理、tool-calling/schema-constrained extraction，并比较 GPT-5.2、gpt-oss-120b、Kimi、GLM、DeepSeek 等模型。 |
| D4 人工审计与可追踪性 | 🟡 | Page 2 contributions；Page 7 §5.4；Page 76 Appendix M | PERG 标注和专家 survey 提供强 human reference；但主实验重点是评价 harness，不是每条生成 claim 的可导出审计包，HITL interface 仍带设计/未来工作属性。 |
| D5 评价严谨性 | 🟢 | Page 4 §4.1；Page 5-9 §5；Page 36 Appendix F | 有大规模专家参考数据、多模型比较、阶段隔离指标、消融筛选策略、专家审计和成本分析，足以作为评价协议强 baseline。 |
| D6 SE / CCF 相关性 | 🟠 | `bibtex.bib` arXiv cs.IR；Page 1-2 epidemiology / public health setting | 场景是传染病流行病学和公共卫生 SLR，不是 SE/CCF venue；对 paper2 是跨域方法与评价参照。 |
| D7 novelty 威胁 | 🟢 | Page 3 §3；Page 7 §5.3-5.4；Page 9 §6.3-6.4 | 已覆盖 agent/LLM SLR workflow、阶段化评价、人类参考标注、专家审计、成本与失败模式；paper2 若主张 agentic SLR evaluation 或 evidence handling，必须正面对比。 |

## 3. 论文解决的问题与背景

论文认为 SLR 是高成本、高风险且强证据约束的知识综合任务，适合作为 LLM 能力评价对象。流行病学 SLR 尤其难，因为同一参数可能按年龄、地理、严重程度、研究设计等上下文被多种方式报告；模型只“找到数字”不够，还必须把数字和正确上下文绑定。作者与 PERG 合作，把 WHO priority pathogens 的专家标注作为 human reference，目标不是证明 LLM 可无人替代专家，而是把检索、筛选、结构化抽取拆成可定位失败的评价任务。

## 4. 方法 / 系统拆解

输入端包括数据库检索式、题名摘要、开放全文 PDF 和 PERG 标注。流程先查询 OpenAlex、PubMed、Europe PMC，并用去重、缓存和全文下载管线形成候选；随后用 ScreenPrompt 风格提示执行题摘筛选，再把 PDF 经 OCR 转成 Markdown，进入更严格的全文筛选。结构化抽取分三类：epidemiological parameters、transmission models、outbreaks。抽取阶段先判断文章是否含目标数据，再用 schema-constrained tool calls 填写字段，并对人口上下文做 tagging。

输出端是分阶段预测、结构化抽取记录、统计 artefact 和报告生成材料。报告生成通过标准化代码生成 figures/tables/statistics 后再由 LLM refine，但作者明确说报告生成不属于本研究评价构造，因为 narrative synthesis 与 meta-analysis 需要额外 expert-grounded tests。证据/审计方面，核心是用 PERG 专家标注评估机器输出；附录还描述 validation tool interface，可让专家 verify、reject、revise，但主文证据更偏评价而非生产级审计系统。

## 5. 实验 / 评价设计

RQ 没有以编号形式列出，但实验实际围绕三个问题：不同 LLM 在 SLR 各阶段是否表现一致，结构化抽取瓶颈在哪里，以及不同筛选策略如何影响 evidence survival 与成本。数据来自 PERG priority pathogen SLR：七个 pathogen 用于筛选，四个用于参数/模型抽取，Lassa 和 Zika 用于 outbreak 抽取。基线/比较对象是五个 frontier reasoning models；Claude Opus/Sonnet 4.5 尝试失败并被记录为 refusal。

指标包括筛选 precision、recall、macro F1；抽取被拆成 flagging、count、field-level extraction；匹配无唯一 ID 的多条抽取时使用相似度和 assignment。人工评估由六名流行病学专家完成，评价 flagging precision、field-level extraction accuracy 和 1-7 competence。成本评估按每 pathogen run 的 token、OCR 与模型费用计算。

## 6. 主要结果与结论

全文结果支持三个强结论。第一，scientific synthesis 不是单一能力：Kimi-K2.5 题摘筛选最好，gpt-oss-120b 全文筛选最好，抽取任务领先模型又不同。第二，结构化抽取是主要瓶颈：五个模型平均 field-level extraction F1 均未超过 0.67，参数抽取尤其低，没有模型达到 0.60。第三，人机流程设计影响证据保留：AI abstract 到 AI full-text 的两阶段策略 recall 为 0.81，human abstract 到 AI full-text 提升到 0.92 且 F1 为 0.87，direct full-text recall 为 0.89 但成本和运行时间显著增加。

专家验证给出的部署边界很清楚：参数和 outbreak 抽取可作为可纠正起点，模型抽取 competence 较低。作者结论是 AgentSLR 可显著压缩 review 阶段时间，但不能支持无人监督部署。

## 7. 局限与可复现性

可复现性较强：摘要页给出 Dataset 和 Harness Code 入口，正文说明释放 metadata、URLs、structured annotations，并有代码下载/OCR说明。限制包括：开放获取文章只覆盖约 27.0% PERG corpus；英文筛选会漏掉多语种证据；评价偏 evidence survival，低 precision 会把负担转移到下游；没有评价 meta-analysis 和最终 review writing。arXiv 版本未等同正式 peer-reviewed 版本。

## 8. 对 paper2 story / 实验设计的影响

paper2 不能把“LLM 用于 SLR 多阶段 workflow”作为宽泛 novelty。更可 defend 的差异应落在 SE research object、agent run record、claim-to-source trace、人工审计 gate、错误传播分析，以及是否能把每条生成结论追溯到源文献证据。实验上应借鉴 AgentSLR 的 stage-isolated metrics，而不是只给端到端报告质量分。

## 9. 可用于写作的引用角度

- AgentSLR 可作为“跨域医学 SLR 中大规模 阶段化 评价基准”的强近邻，用来说明当前 LLM 证据综合研究已经开始从单点 prompt 转向流程级评价。
- 该文的失败模式支持 paper2 强调证据链和人工 gate：筛选 false negative 会永久移除证据，抽取 context error 会把正确数值绑到错误 claim。
- 该文不应被写成 SE baseline；它是临床/流行病学 SLR 方法学 baseline。

## 10. 待复核清单

- 后续写正式 Related Work 前，人工打开 PDF 核对 Figure 1-5 与 Table 1-3 的版面和数值。
- 核验 oxrml.com/agent-slr 的 dataset/harness code 当前可访问性、license 与具体 commit。
- 检查 arXiv 后续是否出现正式会议/期刊版本。
- 若 paper2 采用类似 F1/field-level 指标，需复核 Appendix C/E/F 的完整 metric 定义。
