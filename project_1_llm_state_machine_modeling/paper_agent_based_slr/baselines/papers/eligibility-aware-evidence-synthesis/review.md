# Eligibility-Aware Evidence Synthesis: An Agentic Framework for Clinical Trial Meta-Analysis

## 1. 快速结论卡片

| 字段 | 内容 |
|---|---|
| 标题 | Eligibility-Aware Evidence Synthesis: An Agentic Framework for Clinical Trial Meta-Analysis |
| 年份 | 2026 |
| 作者 / venue / 出版状态 | Yao Zhao、Zhiyue Zhang 等；arXiv:2604.02678; 本轮未核验正式 peer-reviewed / CCF 状态 |
| 分层 | P0 |
| 阅读状态 | 已读全文文本-paper_content核验；未人工打开 PDF 图表 |
| 证据等级 | 全文文本级；图表/表格细节待人工 PDF 核对 |
| 核验入口 | [bibtex.bib](./bibtex.bib)、[paper_content.txt](./paper_content.txt)、[paper.pdf](./paper.pdf) |
| 研究脉络 | agent式证据综合与闭环文献总结 |
| 引用角色 | 直接新颖性门槛 / 强 baseline |
| LLM/agent 角色 | LLM/agent 执行部分检索、筛选、抽取、组织、生成或评价环节；具体阶段见方法/覆盖阶段字段。 |
| 证据溯源粒度 | decision-log / trace 级 provenance；需核验是否能导出完整证据包。 |
| 输入 | 自然语言临床问题、ClinicalTrials.gov 记录、free-text eligibility criteria、目标 trial eligibility profile、二分类 outcome event data |
| 输出 | 显式 selection rules、function plans、过滤后的 trial set、结构化 trial summaries、eligibility weights、eligibility-weighted meta-analysis estimates |
| 方法/系统形态 | EligMeta：LLM-assisted reasoning + deterministic execution 的 agentic evidence synthesis framework |
| 覆盖阶段 | trial discovery/selection、criteria structuring、eligibility-aware statistical synthesis；不覆盖传统 SLR 的题摘筛选、PDF 全文抽取、质量评价或综述报告写作 |
| 不覆盖阶段 | 不覆盖传统 SLR 的题摘筛选、PDF 全文抽取、质量评价或综述报告写作。 |
| 人审/审计机制 | 规则集在执行前 surfaced for expert review；rules/function plans/parsed values/filtering outcomes logged；penalty rule 可解释，但没有正式用户研究或逐条人工审计实验 |
| 人类角色 | 运行中审查者或用户反馈；需区分是否为正式审计 gate |
| 审计时机 | 原文未给出清晰审计时机或本轮未抽取 |
| 主张追踪状态 | 规则/function/filtering log 级；无报告级 claim-to-source trace。 |
| 决策日志状态 | per-record / reasoning 级线索；导出格式待核验 |
| 冲突处理机制 | 原文未给出明确冲突处理或不适用 |
| 审计导出性 | 有表格/JSON/schema 输出线索；是否形成可审计证据包待 artifact audit。 |
| 实验/指标 | gastric cancer landscape case：4,044 trials 到 39 eligible，13 guideline-cited；olaparib AE meta-analysis：4 RCT，对比 MH 与 EW-MH risk ratio；与 GPT-5.4 Deep Research 和 Codex 作 landscape 对比 |
| 模型/API 设置 | GPT-5、GPT；具体版本/调用日期按原文与 artifact 待复核 |
| 提示词状态 | 附录/正文给出 prompt 或片段；完整可复用性待核验 |
| 温度/重复/随机种子 | 原文未给出或本轮未抽取 temperature / seed / repeats |
| 主要发现 | eligibility weighting 将 vomiting pooled RR 从 2.18 调整为 1.97；Golan 2019 display weight 从 13.6% 到 34.6%；GPT-5.4 找 11 trials，Codex 找 28 trials，EligMeta 找 39 |
| 关键结果锚点 | review.md §2 D1-D7 证据锚点 + §5/§6 实验与结果；SUMMARY 数字不得脱离单篇锚点引用 |
| 数值使用许可 | 仅文本级引用；正式写作前需 PDF 图表/表格核对 |
| 对 paper2 的作用 | 强约束“agentic evidence synthesis + deterministic/auditable execution”叙事；但其统计 meta-analysis 任务和医学 registry 输入与 SE SLR paper2 不同 |
| 受影响主张 ID | C1,C2,C5,C7 |
| 威胁类型 | 局部覆盖 + 评价协议约束 |
| 威胁的 paper2 主张 | 强约束“agentic evidence synthesis + deterministic/auditable execution”叙事；但其统计 meta-analysis 任务和医学 registry 输入与 SE SLR paper2 不同 |
| 支持的 paper2 主张 | 支持 paper2 强调阶段化 evidence package、deterministic execution boundary、人类反馈闭环和 run record，而不是单次生成报告。 |
| paper2 应避免的主张 | 避免写“首次 agentic SLR / 首次自动化 evidence synthesis”；必须承认跨域强近邻并收窄到 SE 场景和可审计证据包。 |
| baseline 可用性 | 定性强baseline；若代码/数据可得，后续再判定是否可运行复现。 |
| 对比方式 | 协议/指标baseline |
| 代码状态 | 声称有/正文出现 GitHub 或 code 线索；本轮未打开核验 |
| 数据状态 | 声称有/正文出现 dataset 或 data availability 线索；license 未核验 |
| 许可状态 | 未核验；不得据此承诺可复现或可再分发 |
| 制品入口 | 本轮仅从 paper_content/review 识别线索；URL、commit、license 和 smoke 运行留待下一轮 artifact audit |
| 运行可行性 | 协议/指标baseline |
| 可复现资产 / 阻塞项 | 代码、数据、prompt、license、正式 venue/DOI 与 PDF 图表级数值均按 §7 / §10 待复核清单处理；未核验项不得支撑强实验比较。 |

## 2. D1-D7 全文核验评分

| D1 主题 | D2 流程 | D3 自动化 | D4 审计 | D5 评价 | D6 SE | D7 威胁 |
|---|---|---|---|---|---|---|
| 🟢 | 🟡 | 🟢 | 🟡 | 🟡 | 🟠 | 🟢 |

| 维度 | 评分 | 全文证据锚点 | 判定理由 |
|---|---:|---|---|
| D1 主题贴合度 | 🟢 | `paper_content.txt` Page 1 Abstract；Page 3 contributions | 明确研究 clinical evidence synthesis 和 meta-analysis，直接属于 evidence synthesis 自动化近邻。 |
| D2 SLR/SMS 流程覆盖度 | 🟡 | Page 3-6 §2.1-2.2；Page 8-13 §3 | 覆盖 trial discovery/selection、criteria structuring、meta-analysis synthesis 三类核心环节；未覆盖常规 SLR 的全文 PDF 抽取、质量评价和报告写作。 |
| D3 LLM/agent 自动化深度 | 🟢 | Page 3 §2；Page 31-32 Appendix A.4；Page 24 Appendix A.3 | LLM 生成 selection rules/function plans、解析 trial metadata、生成 penalty rules；检索、过滤、权重和统计由确定性模块执行，形成清晰输入输出链。 |
| D4 人工审计与可追踪性 | 🟡 | Page 5-6 §2.1；Page 8 §3.1；Page 31-32 Appendix A.4 | 有 expert review 前置、logged intermediate artifacts 和 deterministic audit trail；但没有 reviewer edit log、claim-to-source evidence package 或人工审计实验。 |
| D5 评价严谨性 | 🟡 | Page 8-13 §3；Page 32-33 Appendix D | 有两个案例、与 GPT-5.4/Codex landscape outputs 对比、具体数值和代码可用；但不是大规模 benchmark，gold standard/统计显著性和人工标注协议有限。 |
| D6 SE / CCF 相关性 | 🟠 | `bibtex.bib` arXiv stat.ME；Page 1-2 precision medicine / clinical trial setting | 医学统计/临床试验 evidence synthesis，非 SE/CCF；对 paper2 是方法学背景。 |
| D7 novelty 威胁 | 🟢 | Page 3 contributions；Page 13 Discussion；Appendix A.4 | “LLM reasoning 与 deterministic execution 分离、auditable workflow、agentic evidence synthesis”组合与 paper2 的 agent-loop/run-record story 高度相似，需正面对比。 |

## 3. 论文解决的问题与背景

EligMeta 处理临床证据综合中的两个断裂：一是从大量 clinical trial registry 中根据复杂自然语言临床问题找到相关 trials；二是传统 meta-analysis 主要按统计精度加权，未显式处理 trial eligibility criteria 导致的人群差异。作者认为 precision medicine 场景下，合成结果应对齐目标 cohort，而不仅是把所有试验平均起来。

## 4. 方法 / 系统拆解

框架分两阶段。第一阶段把 free-text clinical query 转成一组 human-readable inclusion/exclusion rules，例如 disease type、intervention class、endpoint、biomarker stratification、enrollment threshold、FDA approval。规则在执行前展示给专家审阅。随后每条规则被转成 function plan：指定 registry fields、LLM parser instruction、comparison operator 和 expected output type。LLM 只做 format-constrained parsing，逻辑比较和过滤由 deterministic functions 执行。FDA drug approval 通过 agentic drug retrieval pipeline 从 Drugs.com 和本地缓存列表获取，LLM 不直接判断批准状态。

第二阶段进行 eligibility-aware meta-analysis。系统把 free-text eligibility criteria 结构化为 `(Type, Entity, Attribute, Value, Condition, Sentence)`，再让 LLM 生成可解释 penalty rules，表示候选 trial 和 target trial 的人群不匹配。penalty 通过确定性函数求和并转成非零 normalized eligibility weights，再进入扩展的 Mantel-Haenszel estimator。所有 penalty evaluation、score transformation 和 statistical pooling 均 deterministically logged。

## 5. 实验 / 评价设计

论文没有正式 RQ 编号。案例一是 gastric cancer landscape analysis：同一 query 先从 ClinicalTrials.gov 返回 4,044 trials，generic pre-filtering 后剩 700，六条规则顺序过滤后得到 39 eligible studies。作者用 NCCN guideline 引用作为临床 relevance proxy，39 个中有 13 个被 guideline targeted therapy/immunotherapy sections 引用。还与 GPT-5.4 Deep Research 和 Codex 比较：GPT-5.4 找到 11 个 trials，其中 8 个 NCCN relevant；Codex 找到 28 个，其中 7 个 NCCN relevant，并错误纳入未 FDA-approved 的 FLX475。

案例二是 olaparib adverse events meta-analysis。系统识别 5 个 eligible trials，选取原研究中的 4 个 RCT 便于对照。以 Golan 2019 为 target trial，LLM 生成 5 条 penalty rules，确定性计算 penalty scores 为 `(0.0, 2.8, 1.8, 2.8)`，再转为 weights `(0.52, 0.13, 0.21, 0.13)`。评价关注 pooled risk ratio 变化和可解释 display weight，而非分类准确率。

## 6. 主要结果与结论

gastric cancer 案例显示，EligMeta 可从大规模 trial registry 中形成明确可审计的过滤链，并恢复一批 guideline-level studies。作者也指出剩余 26 个 trials 包括早期研究或数据不完整研究，可能是 emerging evidence。

olaparib 案例中，传统 Mantel-Haenszel pooled vomiting RR 为 2.18，95% CI 为 1.71-2.79；eligibility-weighted 后为 1.97，95% CI 为 1.76-2.20。Golan 2019 的 display weight 从 13.6% 提升到 34.6%，Moore 2018 从 31.7% 降到 20.5%。作者解释为 Moore 2018 虽有较大样本和较高精度，但 ovarian cancer、多线治疗等 eligibility profile 与 pancreatic cancer target 不匹配。

## 7. 局限与可复现性

可复现性方面，正文给出 Code Availability：`https://github.com/JackZhao1998/EligMeta.git`，数据来自公开 ClinicalTrials.gov。限制包括：依赖 eligibility criteria 的准确抽取与结构化，registry reporting 质量会影响结果；当前依赖 ClinicalTrials.gov，未直接整合全文文献中的风险人数、随访窗口、AE grade、subgroup effect 等细节；penalty rules、severity scores 和 transformation parameters 是模型/专家共同决定的建模选择，需要 sensitivity analysis 和 domain expert calibration；当前只展示 binary outcome 和 MH estimator，连续 outcome、time-to-event、random-effects/Bayesian extension 仍是未来工作。

## 8. 对 paper2 story / 实验设计的影响

EligMeta 对 paper2 最大影响不是 SLR 流程覆盖，而是“LLM 负责语义规划，确定性模块负责执行与统计”的架构叙事。paper2 若采用 agent-loop，应强调每个 stage 的 schema、deterministic validation、日志和 eligibility filter，而不是让 LLM 直接生成最终结论。差异化可落在 SE 文献对象、论文证据抽取、claim-to-source audit 和 systematic review/report 生成，而不是临床 registry/meta-analysis。

## 9. 可用于写作的引用角度

- EligMeta 可作为“agentic evidence synthesis 中将 LLM reasoning 与 deterministic execution 分离”的代表。
- 它说明 evidence synthesis 的可靠性不只取决于检索覆盖，也取决于中间规则、结构化表示和统计权重是否可解释。
- 它不支持“完整 automated SLR”表述；更准确说是面向 clinical trial registry 和 meta-analysis 的 agentic pipeline。

## 10. 待复核清单

- 人工打开 PDF 核对 Figure 1-5、Table 1-2 的公式、流程图和数值。
- 访问 GitHub 仓库确认代码、license、commit、可运行脚本和案例数据。
- 若用于 Related Work，需要核验 GPT-5.4/Codex baseline 输出是否在仓库中可得，以及比较是否公平。
