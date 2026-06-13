# A Reproducible Optimisation Protocol for Calibrating Prompt-Based Large Language Model Workflows in Evidence Synthesis

## 1. 快速结论卡片

| 字段 | 内容 |
|---|---|
| 标题 | A Reproducible Optimisation Protocol for Calibrating Prompt-Based Large Language Model Workflows in Evidence Synthesis |
| 年份 | 2026 |
| 作者 / venue / 出版状态 | Teo Susnjak；arXiv:2605.06937; 本轮未核验正式 peer-reviewed / CCF 状态 |
| 分层 | P1 |
| 阅读状态 | 已读全文文本-paper_content核验 |
| 证据等级 | 全文文本级；图表/表格细节待人工 PDF 核对 |
| 核验入口 | [bibtex.bib](./bibtex.bib)、[paper_content.txt](./paper_content.txt)；未人工打开 PDF 图表 |
| 研究脉络 | agent式证据综合与闭环文献总结 |
| 引用角色 | 模块级 baseline / 重要相关工作定位 |
| LLM/agent 角色 | 原文未给出明确 LLM/agent 执行角色；按相关工作背景处理。 |
| 证据溯源粒度 | decision-log / trace 级 provenance；需核验是否能导出完整证据包。 |
| 输入 | 固定 task contract、machine-readable interface、labelled/reference examples、task metric、student LLM、reflection LLM、train/val/test splits |
| 输出 | GEPA/DSPy compiled prompt harness、saved JSON artefact、evaluation traces、prediction logs、reproducibility checklist、held-out screening metrics |
| 方法/系统形态 | Methods article；用 DSPy + GEPA 把 prompt optimisation 视为科学仪器校准；student model 执行任务，reflection model 只在 calibration 中修订 prompt |
| 覆盖阶段 | 实证验证只覆盖 title/abstract screening；方法上讨论 extraction、coding、risk-of-bias、domain mapping、query generation、tool routing 等可适配任务 |
| 不覆盖阶段 | 不覆盖阶段需按全文方法章节复核；当前不得据此写“完整覆盖 SLR 生命周期”。 |
| 人审/审计机制 | 固定 criteria / task contract；metric 要求 checks trace；保存 specification、metric、settings、traces、environment、logs；专家判断仍保留给 borderline / synthesis decisions |
| 人类角色 | 领域专家gold / 标注者 / 事后评价者（具体角色见人审机制字段） |
| 审计时机 | 运行前 + 运行后复核 |
| 主张追踪状态 | 无明确 claim-to-source trace 或本轮未核验 |
| 决策日志状态 | per-record / reasoning 级线索；导出格式待核验 |
| 冲突处理机制 | 原文未给出明确冲突处理或不适用 |
| 审计导出性 | 有 trace/log/dialogue 或 protocol 线索；是否可作为 run record 导出待 artifact audit。 |
| 实验/指标 | SESR-Eval Study 41，1194 records；Qwen-2.5-7B student、GPT-5-mini reflection；5 seeds；GEPA budgets 2/6/12/24；held-out N=1076 |
| 模型/API 设置 | GPT-5、Qwen、LiteLLM、GPT；具体版本/调用日期按原文与 artifact 待复核 |
| 提示词状态 | 正文提到 prompt；完整模板待核验 |
| 温度/重复/随机种子 | seed、seeds；正式复现前需回原文核对 |
| 主要发现 | structured baseline F1 0.840；max_eval=12 F1 0.848、utility 0.855，提升很小；max_eval=24 反而低于 baseline，说明 budget 不是单调收益 |
| 关键结果锚点 | review.md §2 D1-D7 证据锚点 + §5/§6 实验与结果；SUMMARY 数字不得脱离单篇锚点引用 |
| 数值使用许可 | 仅文本级引用；正式写作前需 PDF 图表/表格核对 |
| 对 paper2 的作用 | 约束 paper2 的 prompt / LLM workflow reproducibility：必须固定 task contract、metric、seeds、model IDs、traces、artefacts 和 run logs，不能只报告最终 prompt |
| 受影响主张 ID | C5,C7 |
| 威胁类型 | 评价协议约束 + 负面证据 |
| 威胁的 paper2 主张 | 约束 paper2 的 prompt / LLM workflow reproducibility：必须固定 task contract、metric、seeds、model IDs、traces、artefacts 和 run logs，不能只报告最终 prompt |
| 支持的 paper2 主张 | 支持 paper2 强调阶段化 evidence package、deterministic execution boundary、人类反馈闭环和 run record，而不是单次生成报告。 |
| paper2 应避免的主张 | 避免写“首次 agentic SLR / 首次自动化 evidence synthesis”；必须承认跨域强近邻并收窄到 SE 场景和可审计证据包。 |
| baseline 可用性 | 协议/指标baseline或局部强baseline；主要用于模块级对照与写作定位。 |
| 对比方式 | 协议/指标baseline |
| 代码状态 | 声称有/正文出现 GitHub 或 code 线索；本轮未打开核验 |
| 数据状态 | 声称有/正文出现 dataset 或 data availability 线索；license 未核验 |
| 许可状态 | 未核验；不得据此承诺可复现或可再分发 |
| 制品入口 | 本轮仅从 paper_content/review 识别线索；URL、commit、license 和 smoke 运行留待下一轮 artifact audit |
| 运行可行性 | 协议/指标baseline |
| 可复现资产 / 阻塞项 | 代码、数据、prompt、license、正式 venue/DOI 与 PDF 图表级数值均按 §7 / §10 待复核清单处理；未核验项不得支撑强实验比较。 |

## 2. D1-D7 全文核验评分

emoji 口径见 [../../GUIDE.md](../../GUIDE.md)。

| D1 | D2 | D3 | D4 | D5 | D6 | D7 |
|---|---|---|---|---|---|---|
| 🟢 | 🟡 | 🟡 | 🟢 | 🟡 | 🟡 | 🟡 |

| 维度 | 评分 | 全文证据锚点 | 判定理由 |
|---|---:|---|---|
| D1 主题贴合度 | 🟢 | Page 1 Abstract：prompt-based LLMs in structured evidence-synthesis tasks；Page 2 Background：systematic reviews、screening、data extraction、quality assessment、synthesis | 直接服务 evidence synthesis / systematic review LLM workflow 的可复现校准。 |
| D2 SLR/SMS 流程覆盖度 | 🟡 | Page 4：validation case 是 title/abstract screening；Page 5 Table 2：列出 data extraction、full-text eligibility、risk-of-bias、coding、mapping、query generation 等适配任务 | 实证只有 screening 一环；方法框架可扩展到多个环节，但未全文验证，所以不能给强覆盖。 |
| D3 LLM/agent 自动化深度 | 🟡 | Page 6：student LLM + reflection LLM；Page 11：GEPA compile；Page 14-15：Qwen-2.5-7B + GPT-5-mini validation | 有明确 LLM workflow 和自动 prompt optimisation，但不是 agentic SLR pipeline，也不执行多阶段综述。 |
| D4 人工审计与可追踪性 | 🟢 | Page 1 Abstract：artefact with specification, metric, settings, evaluation traces；Page 13：保存 task specification、metric、GEPA config、seeds、environment、logs；Page 17 Table 8 checklist | 强调 artefact-level inspectability、trace、metric、environment 和 prediction logs，是 paper2 run record 设计的强 baseline。 |
| D5 评价严谨性 | 🟡 | Page 14-15：SESR-Eval Study 41、1194 records、5 seeds、held-out metrics；Page 15 Limitations：one binary screening task、one benchmark case、one student model | 实验设计清楚且有 baseline/ablation，但范围只有一个 SE screening case 和一个学生模型，作者也明示不可泛化。 |
| D6 SE/CCF 相关性 | 🟡 | Page 14：Study 41 是 software defect prediction systematic mapping；`bibtex.bib`：arXiv cs.LG | 不是 SE venue，但验证任务来自 SE secondary-study screening dataset，和 paper2 实验设计相关。 |
| D7 对本文 novelty 的威胁 | 🟡 | Page 13：compiled workflow as research artefact with provenance；Page 17：reproducibility checklist | 对 paper2 的 prompt calibration、reproducibility、audit artefact claim 构成局部强约束；不覆盖 agent-based SLR 全流程。 |

## 3. 论文解决的问题与背景

论文关注 evidence-synthesis LLM workflow 的 prompt variability。作者认为 LLM 可支持 screening、data extraction、quality assessment 和 synthesis，但 prompt wording、model family、temperature/top-p、manual tweaking 都会影响结果；尤其小模型或本地模型需要更明确校准，才能作为可靠 scientific instruments 使用。

核心问题不是提出新 prompt optimiser，而是把 prompt optimisation 组织为可复现校准协议：固定科学任务规则，只优化包裹这些规则的 prompt harness，并把编译后的工作流保存为可检查 artefact。对 paper2 来说，这篇论文的价值在于给出“LLM workflow 必须如何被审计和复现”的硬标准。

## 4. 方法 / 系统拆解

方法需要四个 ingredients：fixed task contract、mutable prompt harness、labelled/reference examples、executable metric。task contract 定义科学要求，例如 eligibility criteria、extraction schema、coding manual、risk-of-bias rubric 或 review policy；machine-readable interface 定义输入字段、输出字段、label set、parser 和 output-validity rules；prompt harness 是可变 instructional wrapper，也是 GEPA 可修订的唯一层。

workflow 有四步。第一，定义 structured LM-program signature。第二，用 examples 和 metric codify standard。第三，用 GEPA 在 fixed budget 下编译 prompt harness。第四，保存、重载、评估和打包 compiled artefact。student model 是待部署的任务执行模型，正文示例中用 temperature=0.0 减少 evaluation/execution variation；reflection model 更强、更贵，只在 calibration 中读取 metric feedback 并提出 prompt revisions。

审计机制主要来自 metric 和 artefact packaging。metric 不只是 accuracy：binary screening 中 false negatives 得 0，false positives 给 partial credit 0.4，并要求 `checks` 字段提供简短 justification。expanded metric 会把 criteria、title、abstract 附在 feedback 中，让 reflection model 基于具体失败修 prompt。compiled artefact 需要伴随 dataset version、split identifiers、metric source、optimisation config、model/provider details、package versions、seeds、adapter settings 和 prediction logs。

## 5. 实验 / 评价设计

验证目的很克制：检查协议能否暴露和记录 calibration trade-offs，不是排名模型，也不是证明 GEPA 普遍有效。任务是 binary title-and-abstract screening，使用 SESR-Eval Study 41。该 study 有 1194 candidate records，来源是软件缺陷预测的 secondary review。criteria 从 Study 41 source article 抽取并 freeze。

主要 comparator 是 structured unoptimised DSPy program，它与 GEPA 条件共享同样的 criteria、title、abstract inputs、checks/label outputs、student model、temperature、adapter、label normalization 和 held-out examples。GEPA 只改变 prompt harness。实验使用 Qwen-2.5-7B-instruct 作为 student，GPT-5-mini 作为 reflection，5 个 seeds，train/val/test sizes 通常为 59/59/1076，budget 为 max_eval 2、6、12、24。指标包括 accuracy、precision、recall、F1、MCC、Cohen's κ、predicted include rate 和 asymmetric utility。

## 6. 主要结果与结论

structured baseline 的 accuracy 为 0.788±0.004，precision 0.791±0.003，recall 0.896±0.006，F1 0.840±0.004，utility 0.847±0.004。max_eval=2 的 recall 最高，为 0.938±0.033，但 precision 降到 0.762±0.052，predicted include rate 上升，意味着更多 full-text workload。max_eval=12 最平衡：accuracy 0.797±0.023，F1 0.848±0.011，utility 0.855±0.007，相比 structured baseline 只有 ΔF1 +0.008±0.008 和 Δutility +0.008±0.005。max_eval=24 则 F1 0.829±0.021、utility 0.832±0.019，低于 baseline。

结论是 prompt calibration 可改变 operating point，但效果 modest，budget 不是越大越好。作者强调这不是 GEPA 的普遍优势证明，而是展示如何在固定 task contract 下记录、比较和复用 calibration。

## 7. 局限与可复现性

作者明确说该方法不替代 expert judgement；borderline eligibility、ambiguous extraction、risk-of-bias 和 final synthesis 应保持人工监督。性能依赖 labelled examples 质量、模型 provider 稳定性和 metric fidelity。验证只覆盖 one binary screening task、one benchmark case、one student model、small repeated runs，不应泛化到所有 evidence synthesis tasks。

可复现性是本文强项：Supplementary material 包含 Colab tutorial notebook、local smoke-test script、saved compiled artefact 和 example dataset；Table 8 列出 model identifiers、seeds、split sizes、baseline、frozen criteria、metric source、execution environment、artefact、evaluation metrics。环境记录包括 Python 3.11.15、DSPy 3.2.0、GEPA 0.0.27、LiteLLM 1.82.6、OpenAI SDK 2.32.0 等。局限是 exact token-level cost 不可得，provider-side model changes 仍可能破坏数值复现。

## 8. 对 paper2 story / 实验设计的影响

paper2 如果使用 prompts / agent stage prompts / LLM reviewers，不能只保存最终 prompt。至少应保存 fixed task contract、machine-readable interface、mutable prompt harness、metric source、seed、model id、temperature、provider、package versions、data splits、raw predictions、failure feedback 和 compiled artefact。若 paper2 使用 LLM 优化 prompt，也必须说明优化目标偏向 recall、precision、utility 还是 trace compliance。

这篇还提醒 paper2：prompt optimisation 的提升可能很小，且会改变 workload trade-off。paper2 的 screening 评价应同时报告 false negatives、false positives、include rate 和 downstream workload，而不是只报 accuracy/F1。

## 9. 可用于写作的引用角度

- 作为 reproducible LLM workflow 方法背景：evidence-synthesis LLM tasks 应区分 fixed scientific contract 与 mutable prompt harness。
- 作为 run record 设计依据：compiled prompt artefact 需要和 metric、settings、traces、environment、prediction logs 一起保存。
- 作为保守实验依据：prompt optimisation 可能改变 operating point，但不能默认带来普遍性能提升。

## 10. 待复核清单

- 打开 supplementary / Colab 链接，确认 notebook、artefact 和 validation summaries 是否可访问。
- 回 PDF 核对 Figure 2、Table C.12/C.13 数值，当前只读文本提取。
- 若 paper2 引用 max_eval=12 提升，必须写“小幅 operating-point shift”，不能写成显著泛化提升。
- 若采用其协议，补全 token/cost logging，因为原文承认 token-level cost 不可得。
