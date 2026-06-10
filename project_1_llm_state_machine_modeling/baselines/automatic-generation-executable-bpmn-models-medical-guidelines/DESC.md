# 从医学指南自动生成可执行 BPMN 模型 / Automatic Generation of Executable BPMN Models from Medical Guidelines

## 基本信息

- **标题**：Automatic Generation of Executable BPMN Models from Medical Guidelines
- **中文标题**：从医学指南自动生成可执行 BPMN 模型
- **作者**：Praveen Kumar Menaka Sekar、Ion Matei、Maksym Zhenirovskyy、Hon Yung Wong、Sayuri Kohmura、Shinji Hotta、Akihiro Inomata
- **单位**：University of Maryland；Fujitsu Research of America；Fujitsu Limited
- **发表**：arXiv:2604.07817，2026-04-09 预印本
- **DOI**：10.48550/arXiv.2604.07817
- **链接**：[arXiv](https://arxiv.org/abs/2604.07817)；[PDF](https://arxiv.org/pdf/2604.07817)；[Project page](https://praveen1098.github.io/Automated-BPMN-Generation/)

**代码/仓库获取方式**：
- 论文首页给出 project page：`https://praveen1098.github.io/Automated-BPMN-Generation/`；本次建档时页面可访问。
- 原文没有在正文中直接给出完整代码仓库 URL；project page 是否包含完整脚本/数据需后续人工核验。

**数据集获取方式**：
- 原文使用日本 3 个城市的 diabetic nephropathy prevention / health guidance policy documents，并构造 1,000 synthetic patient records 做 simulation。
- 原文未在正文中给出完整数据下载链接；是否通过 project page 提供待核验。

## 简报

本文解决的问题是：如何把医疗/公共卫生政策文档自动转换为可在 workflow engine 中执行、带数据绑定和 KPI instrumentation 的 BPMN 模型，用于 simulation-based policy evaluation。它不仅生成 BPMN 图，还增加 gateway conditions、schema binding、Python execution code 和 KPI counters。

- **输入**：PDF medical guideline/policy documents，可能为日文；以及 patient database schema。
- **方法**：PDF extraction + translation + data-grounded narrative generation + BPMN synthesis/structural repair + SpiffWorkflow executable augmentation + KPI instrumentation/simulation + entropy uncertainty detection。
- **输出**：可由 SpiffWorkflow 执行的 BPMN 2.0 模型、Python execution code、simulation traces、KPI evaluation 和 uncertainty/entropy reports。

```text
输入层：医学指南 PDF + patient database schema
  -> 方法层：文档清洗/翻译 -> 数据库约束 narrative -> BPMN XML + 8 条规则 repair -> executable augmentation -> KPI simulation
  -> 输出层：executable data-aware BPMN model + KPI/entropy evaluation
```

实验在三个日本城市 diabetic nephropathy guidance policies 上进行，使用 Gemini 2.5 Pro、Gemini 2.5 Flash、GPT-5.1，每个 backend 每个城市生成 100 个模型，并在 1,000 个 synthetic patient records 上执行。well-structured policy 上 Gemini Pro 达到 100% ground-truth match；raw per-patient decision agreement overall 超过 92%；entropy 随文档复杂度单调升高。本文是 healthcare BPMN/process 强近邻，非 STM direct baseline。

**可比字段快照**：

- **输入**：自然语言/表格医学政策 PDF + patient schema。
- **输出**：SpiffWorkflow-executable BPMN models、script/service task code、gateway Boolean expressions、KPI traces。
- **输出模型类型**：BPMN executable workflow model，强行为近邻；非 STM 族。
- **使用的 LLM**：Gemini 2.5 Pro、Gemini 2.5 Flash、GPT-5.1；translation、narrative generation、BPMN synthesis、KPI-to-task mapping 都涉及 LLM。
- **主要方法**：data-grounded formal narrative + BPMN XML generation + eight-rule validate/repair loop + executable augmentation + KPI simulation。
- **反馈/验证机制**：BPMN structural validation、Python AST parse、schema binding checks、SpiffWorkflow execution、KPI agreement、entropy uncertainty detector。
- **形式化验证**：有规则验证与执行仿真，但不是 temporal logic/model checking。
- **代码/数据开放性**：project page 有入口；完整代码/数据需人工核验。

## 研究问题与动机

### 问题背景

医疗机构和地方政府依赖自然语言政策来协调患者筛查、健康指导和慢病管理。将这些政策转成可执行模型仍大量依赖人工，限制了政策评估和优化的速度。BPMN 是广泛采用的 process notation，但单纯生成图并不足以支持 simulation-based analysis。

### 核心问题

论文围绕四个 RQ：pipeline 是否能处理多样 policy formats；是否能生成可直接运行的 BPMN；是否能自动绑定 KPIs；自动模型在多大程度上复现 human-designed models 的 decisions。

### 研究动机

既有 text-to-BPMN 方法多停留在 structural output，不绑定数据库 schema、不生成可执行代码、不进行 KPI-based functional equivalence。作者要把“文本到图”推进到“文本到可执行、可评估、可诊断的政策模型”。

### 研究意义

对 LLM4Modeling 而言，本文强调模型生成后的 executability 和 functional equivalence，而不是只看图结构相似。对 Project 1，它提示状态机建模也应保留可运行/可仿真的语义，并通过需求样本或 verification profile 检查行为一致性。

### 现有方法的局限性

原文指出 rule-based/NLP 方法难处理非标准表达、多语言和 domain jargon；LLM-driven 方法如 BPMN-Chatbot、BPMNGen、ProMoAI 等多不绑定数据库 schema 或不做 execution-ready output；GIVUP 偏 formal verification，而本文偏 data-driven execution。

### 研究目标

目标是端到端把 medical guidelines 转为 executable, data-aware, KPI-instrumented BPMN models，并用 entropy detector 标记 ambiguity / uncertainty。

## 核心方法

### 方法概述

pipeline 包含六个阶段：

1. **Document Processing**：用 PyMuPDF4LLM 提取 PDF 文本/表格，并修复 layout、hyphenation、Unicode、数值阈值等问题。
2. **Translation**：把非英语文档翻译成英语，保留表格结构、编号、阈值和 regulatory terms。
3. **Data-grounded Narrative Generation**：生成 formal narrative，使每个条件表达式只引用 patient database columns。
4. **BPMN Synthesis and Structural Validation**：生成 BPMN XML，并用 8 条结构规则 validate/repair。
5. **Executable Augmentation**：把 BPMN 转成 SpiffWorkflow-executable form，给 tasks/gateways 添加 Python code / expressions。
6. **KPI Instrumentation and Simulation**：LLM majority vote 映射 KPIs 到 tasks，执行 1,000 synthetic patients，收集 KPIs 和 entropy。

### Data-grounded narrative generation

该阶段把自然语言 policy criteria 转成 database-executable Boolean expressions：

- structural analysis：分解 workflow stages。
- criterion tokenization：抽取 atomic predicates 和 AND/OR/negation/range/set membership。
- expression-tree construction：按优先级生成表达式树。
- database-schema mapping：将 predicate leaf 映射到 patient database columns，不匹配时不发明变量。
- expression generation：输出 Python syntax Boolean expressions，供 BPMN gateway conditions 使用。

### BPMN synthesis 与八条规则

LLM 接收 narrative 和可用 database variables，生成 BPMN XML。validator 检查：唯一 start event、至少一个 end event、task incoming/outgoing、gateway split/merge、exclusive gateway default flow、non-default condition expression、duplicate target、condition variables 是否在 schema 中。修复包括插入 merge gateway、拆分 split/merge gateway、设置 default flow、XML entity encoding、删除 duplicate flows、用 LLM 映射 invalid variable 等。

### Executable augmentation

generic user tasks 被转成 script/service tasks；每个任务得到 Python code block 读写 workflow data context。gateway conditions 转成 raw Python Boolean expressions，并用 `ast.parse` 检查。data context 基于 pandas-backed patient records。augmentation 保持 gateway condition set invariant，确保不改变 decision logic。

### KPI evaluation 与 entropy detector

KPI-to-task mapping 由 LLM 重复投票确定。每个模型在 1,000 synthetic patients 上执行。对每个 policy/backend，生成多个模型，统计 KPI combinations 的 normalized Shannon entropy：0% 表示完全一致，接近 100% 表示高度不一致。entropy 用于区分 well-specified policies 与 ambiguous policies，并区分 LLM noise 与 genuine policy vagueness。

### LLM/agent 设置

- 使用 Gemini 2.5 Pro、Gemini 2.5 Flash、GPT-5.1。
- Google models 使用 thinking mode。
- LLM 是多阶段模块，不是单一 prompt；没有明确多智能体协作。

## 实验与评估

### 数据集

- 3 个日本城市 diabetic nephropathy health guidance policies。
- 每个城市有 human-designed BPMN baseline。
- 每个 backend 每个城市生成 100 个 candidate models。
- 所有模型用相同 1,000 synthetic patient records 执行。

### 评估指标

- five KPIs：Notification Count、Health Guidance Count、Guidance Resource Utilization、Health Improvement Rate、Medical Cost Savings。
- normalized entropy over KPI combinations。
- per-patient agreement、F1、recall、balanced accuracy、Cohen’s $\kappa$。
- generation failure 和 variable-binding error 分析。

### 实验设置

City 1 是 well-structured policy；City 2 包含 compound Boolean eligibility；City 3 最复杂，包含跨 fiscal years 的 implicit temporal dependencies。三种 backend 对每个 city 都生成 100 个模型。

### 主要实验结果

- **City 1**：Gemini 2.5 Pro 100/100 生成模型匹配 human baseline，entropy 0.0%；Gemini Flash / GPT-5.1 ground-truth match 约 86%-87%。
- **City 2**：Gemini Pro dominant cluster 70.7% match ground truth；Flash 46% match 且 20% failures；GPT-5.1 48% ground truth、38% near-miss。
- **City 3**：所有 backend entropy 高；Gemini Pro normalized entropy 99.6%，Flash 64.8%，GPT-5.1 65.2%，说明高不确定性更像文档 intrinsic ambiguity。
- **per-patient agreement**：City 1 κ ≥ 0.918；City 2 中等；City 3 κ 接近 0，即使 raw agreement > 92%，暴露 rare eligible class 的 base-rate paradox。

### 方法优势

- 不是只生成 BPMN 图，而是生成可执行、数据绑定、KPI-instrumented 模型。
- structural validation + repair + Python parse/schema checks 多重 guardrail。
- entropy detector 可以发现源政策 ambiguity。
- functional equivalence 相比纯 graph similarity 更贴近政策评估目标。

### 方法的局限性

- 只有 3 个 test cases，且均为 healthcare diabetic nephropathy policies。
- BPMN construct palette 受限，不包含 parallel gateways、timers、sub-processes 等。
- 合成患者数据不等于真实临床 outcome validation。
- output 是 BPMN，不是 STM；不能评估状态机结构完整性。

## 与本研究的关系

### 相关性分析

**BASELINE评估建议：`🟠`。**

四条件建议如下：

| 条件 | 建议 | 理由 |
|---|---|---|
| LLM4Modeling | 🟢 | 核心是 LLM 从指南生成可执行建模工件。 |
| NL输入 | 🟢 | 输入为自然语言/表格 policy documents。 |
| LLM方法 | 🟢 | LLM 贯穿翻译、narrative、BPMN、KPI 映射。 |
| STM族输出 | 🟡 | executable BPMN 是强行为近邻，不是 STM family。 |

本文不能算 direct STM baseline，因为它输出 BPMN workflow，且关注 medical policy decision pathways，而非状态机 states/events/transitions/guards/actions。

### 研究定位与差异化

这是“LLM text-to-executable process model”的强近邻。它与 Project 1 的共同点在于从非形式化需求生成可机读行为模型，并用执行/仿真闭环检查行为；差异在于目标语言 BPMN 以及 healthcare policy domain。

### 可借鉴之处

- **schema-grounded guard generation**：状态机守卫也应只引用已定义变量，类似 R8。
- **parse/semantic repair loop**：pyfcstm 可替代 SpiffWorkflow 作为 validator。
- **KPI/profile execution**：Project 1 可用 scenario traces / verification profiles 做 functional equivalence。
- **uncertainty detection**：重复生成状态机的结果分布可衡量需求歧义或模型不稳定。

### 存在的不足与改进空间

- 不包含 STM 语义、时钟约束或 model checking。
- 领域狭窄；对工业控制系统迁移需谨慎。
- 公开 artifact 完整性待复核。
- 部分 repair 仍依赖 LLM 变量映射，可能引入 silent mistakes。

### 对本研究的启发

Project 1 应把“生成状态机”与“能运行/能检查”绑定。类似本文八条 BPMN structural rules，可以为 STM 设计 start state、transition totality、guard variables、event/action consistency、no orphan states 等 gate，并在 run record 中记录每轮 diagnostics。

## 重要的相关工作

### 1. 重要的前身类工作

- Friedrich et al. text-to-BPMN：早期 rule-based/NLP 流程模型生成。
- BPMN Sketch Miner：受限输入下的 live BPMN synthesis。

### 2. 直接参与实验的baseline

- Human-designed BPMN baselines：用于 KPI functional equivalence。
- Gemini 2.5 Pro、Gemini 2.5 Flash、GPT-5.1：本文主要 LLM backends。

### 3. 提供了重要论证的工作

- Automatic BPMN Model Generation from Textual Process Descriptions：作者 prior generic BPMN reconstruction pipeline。
- GIVUP：文本到 BPMN 并做 LTL model checking 的邻近工作。
- ProMoAI、BPMN-Chatbot、BPMNGen：LLM process modeling 相关系统。

### 4. 在技术上提供了支持的工作

- PyMuPDF4LLM：PDF extraction。
- SpiffWorkflow：workflow execution engine。
- Python AST parsing：gateway expression syntax validation。

### 5. 其他重要工作

- diabetic nephropathy aggravation prevention program 与日本相关临床政策文献：提供 KPIs 和 domain context。

## 文献分类总结

本文是 LLM-to-executable-BPMN 强近邻，强调数据绑定、执行仿真和 uncertainty detection。它对 Project 1 的方法启发强，但输出不是状态机族，因此建议入账为 `🟠`，四条件为 `🟢/🟢/🟢/🟡`。
