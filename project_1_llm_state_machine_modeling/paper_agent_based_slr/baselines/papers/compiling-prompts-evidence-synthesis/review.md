# Compiling Prompts, Not Crafting Them: A Reproducible Workflow for AI-Assisted Evidence Synthesis

## 1. 快速结论卡片

| 字段 | 内容 |
|---|---|
| 标题 | Compiling Prompts, Not Crafting Them: A Reproducible Workflow for AI-Assisted Evidence Synthesis |
| 年份 | 2025 |
| 作者 / venue / 出版状态 | Teo Susnjak；arXiv:2509.00038; 本轮未核验正式 peer-reviewed / CCF 状态 |
| 分层 | P1 |
| 阅读状态 | 已读全文文本-paper_content核验 |
| 证据等级 | 全文文本级；图表/表格细节待人工 PDF 核对 |
| 核验入口 | [bibtex.bib](./bibtex.bib)、[paper_content.txt](./paper_content.txt)；未人工打开 PDF 图表 |
| 研究脉络 | agent式证据综合与闭环文献总结 |
| 引用角色 | 模块级 baseline / 重要相关工作定位 |
| LLM/agent 角色 | 原文未给出明确 LLM/agent 执行角色；按相关工作背景处理。 |
| 证据溯源粒度 | decision-log / trace 级 provenance；需核验是否能导出完整证据包。 |
| 输入 | SLR task declaration、context file / criteria、gold-standard labelled abstracts、metric、fixed model settings |
| 输出 | compiled screener artefact、prompt/exemplars/config/metrics/run log 的可审计 bundle、示例 screening decision |
| 方法/系统形态 | Research-in-brief preprint；提出 declarative LM-program tuning / prompt compilation workflow，并给 DSPy MIPROv2 abstract-screening code example |
| 覆盖阶段 | 概念上说适用于 SLR stages；正文可执行例子只展示 abstract screening module |
| 不覆盖阶段 | 不覆盖阶段需按全文方法章节复核；当前不得据此写“完整覆盖 SLR 生命周期”。 |
| 人审/审计机制 | 设计层面要求 versioned context、gold-standard examples、metric、prompt/data hashes、model ID、decoding params、run log；没有真实人工 audit study |
| 人类角色 | 领域专家gold / 标注者 / 事后评价者（具体角色见人审机制字段） |
| 审计时机 | 仅评价阶段 / 运行后审计 |
| 主张追踪状态 | benchmark/gold 级；不等同生产期 claim trace |
| 决策日志状态 | per-stage 叙述级；结构化日志待核验 |
| 冲突处理机制 | 原文未给出明确冲突处理或不适用 |
| 审计导出性 | 有 trace/log/dialogue 或 protocol 线索；是否可作为 run record 导出待 artifact audit。 |
| 实验/指标 | 无完整实证 benchmark；Appendix 给最小代码例子和 toy-like gold examples；没有报告真实数据集上的 accuracy/recall/F1 |
| 模型/API 设置 | 原文未给出或本轮未抽取模型清单 |
| 提示词状态 | 附录/正文给出 prompt 或片段；完整可复用性待核验 |
| 温度/重复/随机种子 | seed、重复；正式复现前需回原文核对 |
| 主要发现 | 主要是方法倡议：把 brittle manual prompts 改为 task declaration + test suite + automated prompt tuning + packaged artefact |
| 关键结果锚点 | review.md §2 D1-D7 证据锚点 + §5/§6 实验与结果；SUMMARY 数字不得脱离单篇锚点引用 |
| 数值使用许可 | 仅文本级引用；正式写作前需 PDF 图表/表格核对 |
| 对 paper2 的作用 | 可作为 prompt/workflow reproducibility 的早期背景；不能作为已验证 agent-based SLR 系统或强性能证据 |
| 受影响主张 ID | C7 |
| 威胁类型 | 背景定位 + 评价协议约束 |
| 威胁的 paper2 主张 | 可作为 prompt/workflow reproducibility 的早期背景；不能作为已验证 agent-based SLR 系统或强性能证据 |
| 支持的 paper2 主张 | 支持 paper2 强调阶段化 evidence package、deterministic execution boundary、人类反馈闭环和 run record，而不是单次生成报告。 |
| paper2 应避免的主张 | 避免写“首次 agentic SLR / 首次自动化 evidence synthesis”；必须承认跨域强近邻并收窄到 SE 场景和可审计证据包。 |
| baseline 可用性 | 协议/指标baseline或局部强baseline；主要用于模块级对照与写作定位。 |
| 对比方式 | 仅related-work背景 / reproducibility参照 |
| 代码状态 | 声称有/正文出现 GitHub 或 code 线索；本轮未打开核验 |
| 数据状态 | 声称有/正文出现 dataset 或 data availability 线索；license 未核验 |
| 许可状态 | 未核验；不得据此承诺可复现或可再分发 |
| 制品入口 | 本轮仅从 paper_content/review 识别线索；URL、commit、license 和 smoke 运行留待下一轮 artifact audit |
| 运行可行性 | 仅related-work背景 / reproducibility参照 |
| 可复现资产 / 阻塞项 | 代码、数据、prompt、license、正式 venue/DOI 与 PDF 图表级数值均按 §7 / §10 待复核清单处理；未核验项不得支撑强实验比较。 |

## 2. D1-D7 全文核验评分

emoji 口径见 [../../GUIDE.md](../../GUIDE.md)。

| D1 | D2 | D3 | D4 | D5 | D6 | D7 |
|---|---|---|---|---|---|---|
| 🟢 | 🟠 | 🟠 | 🟡 | 🟠 | 🟠 | 🟠 |

| 维度 | 评分 | 全文证据锚点 | 判定理由 |
|---|---:|---|---|
| D1 主题贴合度 | 🟢 | Page 1 Abstract：AI-assisted evidence synthesis、SLR automation；Page 2 Introduction：abstract screening、data extraction、quality assessment、evidence syntheses | 主题直接是 SLR/evidence synthesis LLM workflow 的 reproducibility。 |
| D2 SLR/SMS 流程覆盖度 | 🟠 | Page 3 Box 1：Abstract Screening Example；Page 4：framework applicable to all stages but example is abstract screening | 正文只有 abstract screening module 的蓝图和代码，其他阶段是倡议/展望，不能按多阶段覆盖计分。 |
| D3 LLM/agent 自动化深度 | 🟠 | Page 4 Appendix A：DSPy MIPROv2 code compiles ChainOfThought(ScreenAbstract)；没有真实 workflow 运行结果表 | 有 programmatic LLM module 示例，但缺少真实多阶段自动化或 agent 工作流，实证深度弱。 |
| D4 人工审计与可追踪性 | 🟡 | Page 3 Box 1：config.yaml、prompt.txt、exemplars.json、metrics.json、run log、hashes、model ID、decoding params | 审计设计很清楚，但主要是 blueprint；未展示真实 run record 或人工 audit protocol，因此中等。 |
| D5 评价严谨性 | 🟠 | Page 4：functional Python implementation / code example；Appendix A：minimal example，未给 benchmark metrics | 没有真实数据集、baseline、指标结果或统计分析，只能弱分。 |
| D6 SE/CCF 相关性 | 🟠 | `bibtex.bib`：arXiv cs.CL；正文示例是医学 PICOS / digital CBT abstract screening | 方法学相关，但不是 SE venue，也没有 SE dataset 验证。 |
| D7 对本文 novelty 的威胁 | 🟠 | Page 4 Conclusion：conceptual blueprint and working implementation；未来需 fully test and expand to other SLR stages | 对 paper2 的 prompt reproducibility claim 有背景约束，但不威胁 agent 工作流、audit gate、SE evaluation 的核心组合。 |

## 3. 论文解决的问题与背景

论文针对 prompt fragility。作者指出 LLM 有潜力加速 SLR，但当前方法依赖 brittle manually crafted prompts，影响 reliability 和 reproducibility。背景中列举 screening、data extraction、risk-of-bias/quality assessment 中 prompt 或模型配置导致的性能波动，例如 prompt 改写、few-shot 顺序、LLM family 不同都会影响 accuracy、sensitivity、kappa 等。

与 2026 年的 methods article 相比，这篇更像早期 research-in-brief：它提出把 prompt engineering 从 ad hoc “prompt alchemy” 转为 declarative LM-program tuning，并用一个 abstract screening code example 说明可执行路径，但没有做完整实证验证。

## 4. 方法 / 系统拆解

框架由四个组件构成。第一，Define the Goal：输入 schema 为 title、abstract、keywords，label space 是 Include、Exclude、Unsure；Unsure 作为 Include 或 route to human review 的 policy 写入固定 spec；versioned context file 记录 PICO criteria、study designs 和 review questions。第二，Codify the Standard：准备 expert-labelled abstracts，并定义 machine-testable metric。第三，Compile the Program：compiler 在 pinned model build、temperature=0、fixed seed 和预算 B 下探索 instruction templates 和 few-shot exemplars，并记录 data/prompt hashes、model ID、decoding parameters。第四，Package the Artefact：输出 config.yaml、prompt.txt、exemplars.json、metrics.json 和 run log，并映射它支持的 PRISMA 条目，例如 protocol transparency 和 decision traceability。

Appendix A 给出 DSPy 例子：`ScreenAbstract` signature 有 criteria、study_aims、research_question、abstract 输入，decision、reasoning、confidence 输出；gold_standard 中有 Include、Exclude、Unsure 三类示例；metric 是 predicted decision 是否等于 gold decision；optimizer 用 MIPROv2 编译 ChainOfThought(ScreenAbstract)；compiled_screener 保存为 `screen_abstract_v1.json` 并可重载用于新 abstract。

## 5. 实验 / 评价设计

严格说，本文没有完整实验。它没有报告真实 SLR dataset 上的 train/validation/test split、baseline 对比、accuracy/precision/recall/F1、人工标注一致性或错误分析。正文 Table 1 汇总的是其他研究中 prompt-induced performance swings，用于论证问题存在，不是作者自己的实验结果。

Appendix 的代码例子使用 digital CBT / MDD 的 PICOS criteria 和少量示例 abstract，目的是展示 workflow structure，而不是验证性能。Gold-standard examples 注释中写到真实集合可能需要 10-50 个 high-quality examples，但正文没有展示作者实际收集和评估这样的集合。

## 6. 主要结果与结论

主要结论是方法性主张：SLR automation 需要从 manual prompt crafting 转向 structured, testable, version-controlled workflow。作者认为 prompt compilation 可把 researcher 的 scientific intent 与 model-specific implementation 分离，把自然语言指令和 examples 当作可调 artefacts，并通过 validation data 与 metric 搜索更合适配置。

这些结论在本文中是 blueprint-level，不是实证证明。正文没有给出 prompt compilation 在真实 SLR 任务中优于 manual prompting 的作者实验数值。写 paper2 时只能把它作为 reproducible prompt workflow 的概念背景，不能引用为“已验证提升 SLR 自动化性能”的证据。

## 7. 局限与可复现性

局限来自证据层级：preprint 篇幅短，缺少真实实验表、数据集、baseline、统计分析和失败案例。虽然 appendix 给出代码，但 API key、真实运行环境、完整 notebook、真实 gold examples 和 compiled artefact 是否可获取，需要另行核验。

可复现性设计本身值得借鉴：作者要求 fixed seed、temperature、model build、data/prompt hashes、config、metrics 和 run log。问题是本文没有把这些作为真实研究运行记录完整展示。后续 2026 methods article 对这些缺口有更详细验证，因此 paper2 若需要强证据，应优先引用 2026 方法文，而把本篇作为前身或概念动机。

## 8. 对 paper2 story / 实验设计的影响

paper2 应吸收它的两个设计原则。第一，prompt 不是临时文本，而是应作为 versioned artefact 管理，和 criteria、examples、metric、model settings、run logs 一起保存。第二，SLR 阶段任务应先形式化为输入/输出 schema 和 metric，再谈自动化。

但 paper2 不能把这篇当作 完整 baseline。它没有 agent roles、没有 multi-stage SLR execution、没有 人工审计 gate 的实证记录，也没有 SE 数据集验证。若 novelty matrix 中纳入它，应标注为 “prompt reproducibility / artefact packaging background”，而不是 “agent 式 SLR 工作流 baseline”。

## 9. 可用于写作的引用角度

- 作为 prompt fragility 背景：SLR automation 中 prompt wording 和模型配置会影响 reliability/reproducibility。
- 作为 workflow design 引用：AI-assisted evidence synthesis 应把 task declaration、test suite、prompt compilation 和 artefact packaging 串成可审计流程。
- 作为 claims-to-avoid 提醒：不能因为有 code example 就声称一个完整 SLR automation system 已被实证验证。

## 10. 待复核清单

- 检查 Google Colab notebook 是否真实可访问，以及是否包含比论文 appendix 更完整的运行结果。
- 不引用其“novel/first”类表述作为 paper2 claim；只引用可证实的 workflow design。
- 若纳入 novelty matrix，标注为弱实证 / conceptual blueprint。
- 优先与 2026 `prompt-optimisation-evidence-synthesis` 合并定位，避免重复夸大同一作者路线。
