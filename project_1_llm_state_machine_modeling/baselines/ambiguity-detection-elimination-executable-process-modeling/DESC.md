# 自动可执行流程建模中的歧义检测与消除 / Ambiguity Detection and Elimination in Automated Executable Process Modeling

## 基本信息

- **标题**：Ambiguity Detection and Elimination in Automated Executable Process Modeling
- **中文标题**：自动可执行流程建模中的歧义检测与消除
- **作者**：Ion Matei、Praveen Kumar Menaka Sekar、Maksym Zhenirovskyy、Hon Yung Wong、Sayuri Kohmura、Shinji Hotta、Akihiro Inomata
- **单位**：Fujitsu Research of America；University of Maryland, College Park；Fujitsu Limited
- **发表**：arXiv:2604.10884，2026-04-14 预印本
- **DOI**：10.48550/arXiv.2604.10884
- **链接**：[arXiv](https://arxiv.org/abs/2604.10884)；[PDF](https://arxiv.org/pdf/2604.10884)；[artifact](https://github.com/ionmatei/ambiguity-detection)

**代码/仓库获取方式**：
- 原文说明 ambiguity detection/repair prompts、input data、reports、representative models 和 demo movie 位于 `https://github.com/ionmatei/ambiguity-detection`；本次建档时 GitHub 页面可访问。
- 该仓库是本文实验 artifact 入口；未在本次逐文件复核其脚本是否可完整复现实验。

**数据集获取方式**：
- 原文使用两个日本市町村的 diabetic nephropathy health-guidance policy case studies；City 1/City 2 原始 policy PDF、synthetic patient input data、ambiguity report、repair report、representative BPMN XML 在上述 GitHub 仓库中给出。
- 数据不是 STM 数据集，而是 healthcare policy -> executable BPMN simulation 样例。

## 简报

本文解决的问题是：当 LLM 从同一自然语言政策/指南反复生成 executable BPMN 模型时，多个模型可能都结构有效，却产生不同模拟 KPI 行为；这说明源文本可能支持多个可执行解释。作者提出 simulation-based ambiguity detection + model-based diagnosis + evidence-based text repair 的闭环，用行为差异定位并修复源文本歧义。

- **输入**：自然语言政策/临床指南叙述、同一合成患者数据、权威补充材料，以及重复生成的 BPMN 模型与 simulation traces。
- **方法**：多次 LLM 生成 BPMN，基于 KPI output distribution 与 normalized entropy 检测不稳定；选择 dominant KPI classes 的 representative models；用 model-based diagnosis 将行为差异定位到 gateway logic，再映射回原文片段；最后用证据支持的最小文本改写修复歧义。
- **输出**：ambiguity report、repaired process narrative、traceability metadata，以及经再生成/再模拟验证更稳定的 executable BPMN behavior。

```text
输入层：自然语言政策文本 + synthetic patient data + supporting evidence
  -> 方法层：重复 BPMN generation/simulation -> KPI entropy -> gateway-level MBD -> narrative mapping -> evidence-based repair
  -> 输出层：歧义报告 + 修复后的政策文本 + 更一致的 executable BPMN 行为分布
```

实验在两个 diabetic nephropathy policy case studies 上各生成 100 个 BPMN 模型并模拟。City 1 修复后超过 90% 生成模型给出同一 KPI outcome；City 2 修复后 70% 生成模型给出同一 outcome。本文是 BPMN/process 修复与验证强近邻，不是 STM exact baseline。

**可比字段快照**：

- **输入**：自然语言 healthcare policy narrative；生成阶段还需要 synthetic patient population 和权威补充材料。
- **输出**：repaired natural-language specification、ambiguity/repair reports、executable BPMN models 的更稳定 KPI behavior。
- **输出模型类型**：BPMN executable process model / simulation behavior；强行为近邻，非 STM 族。
- **使用的 LLM**：原文明确说明所有 LLM steps 使用 GPT-5.1。
- **主要方法**：repeated generation + simulation distribution entropy + model-based diagnosis over gateways + evidence-grounded narrative repair。
- **反馈/验证机制**：simulation-in-the-loop；normalized entropy 和 KPI distribution 是主反馈；修复后通过 regeneration/re-simulation 复验。
- **形式化验证**：使用 model-based diagnosis 与 minimal hitting sets，但没有状态机性质模型检查。
- **代码/数据开放性**：artifact GitHub 原文提供且本次页面可访问；完整复现性待人工进一步核验。

## 研究问题与动机

### 问题背景

自然语言政策和临床指南常需要转换为 executable models 以支持 simulation、quantitative evaluation 和 decision making。BPMN 能表达 workflow logic，也能被 workflow engine 执行。LLM 已能自动生成 BPMN，但自然语言往往 ambiguity、incomplete 或 context-dependent，导致 repeated generation 产生多个结构有效但行为不同的模型。

### 核心问题

论文提出的问题是：在没有 ground-truth BPMN 模型时，如何判断源文本是否支持 stable executable interpretation，并将行为差异定位回具体叙述片段、进而修复源文本？

### 研究动机

单一 BPMN 模型的结构正确不等于语义正确。作者观察到部分政策描述产生 elevated entropy and multimodal KPI distributions，表明文本本身可能允许多种合理 gateway interpretation。传统 ambiguity detection 多停留在文本层面，无法判断歧义是否真正影响 executable behavior。

### 研究意义

本文把 ambiguity 定义为“自然语言规格允许多个逻辑一致但模拟行为不同的可执行解释”。这对 Project 1 很重要：状态机需求中的守卫歧义、事件顺序歧义和条件范围歧义，也应通过可执行行为或验证 profile 暴露，而不是只靠关键词检测。

### 现有方法的局限性

传统 QuARS/requirements ambiguity 方法多为 lexical/syntactic heuristics；controlled natural language 能预防歧义但要求强约束；LLM rewriting 若没有证据可能产生流畅但不受支持的改写。本文用 simulation-output divergence 和 diagnosis 约束 repair，避免任意改写。

### 研究目标

目标不是证明某个生成 BPMN 语义正确，而是检测文本是否支持稳定可执行解释，并用最小、可追溯、证据支持的修改减少生成行为 variability。

## 核心方法

### 方法概述

方法由四个阶段组成：

1. **automatic text-to-executable model generation**：沿用 prior pipeline 从自然语言 clinical specification 生成 executable BPMN。
2. **BPMN simulation output distribution analysis**：对同一文本独立生成多个 BPMN，使用同一 synthetic population 模拟，统计 KPI combinations 的 empirical distribution 和 normalized Shannon entropy。
3. **model-based diagnosis**：从不同 dominant KPI classes 选择 representative models，比较 traces，定位 first divergent KPI-producing task，再构造 gateway conflict sets 并求 minimal diagnoses。
4. **ambiguity elimination and narrative refinement**：将 diagnosed gateway logic 映射到源文本片段，用权威材料选择支持解释，最小改写原文，并用 regeneration/re-simulation 复验。

### Entropy-based ambiguity detection

对每个模型 simulation 的 KPI vector $y = (y_1, y_2, ..., y_d)$ 建立 unique KPI output combinations 的 probability mass function。normalized entropy $Hnorm$ 取值 [0,1]：低值表示生成集中，高值表示多个竞争解释。作者使用 very high / high / moderate / low consistency 四档。

### Model-based diagnosis

component set 是 target model 中的 gateways。observations 是 reference 与 target simulation 的 activity-level KPI outputs。每个 divergent trace 找到 last correct task 和 first erroneous task；位于二者之间的 target gateways 构成 conflict set。所有 conflict sets 上求 minimal hitting sets，得到最小 gateway diagnosis。随后用 path-based logical condition equivalence 删除不能解释差异的 gateways。

### Narrative repair

repair prompt 执行四步：

1. ambiguity localization and mapping：把 ambiguity instance 精确映射到原文位置。
2. evidence-based interpretation selection：用 supplemental material 选择明确支持的解释。
3. minimal disambiguation synthesis：只改写受影响片段，明确 AND/OR、temporal dependencies、conditions。
4. narrative reconstruction：把修订片段放回全文，并保留 traceability metadata。

### LLM/agent 设置

- 所有涉及 LLM 的步骤使用 GPT-5.1。
- LLM 用于自动 BPMN generation、translation/preprocessing pipeline、ambiguity localization、evidence-based repair 等。
- 方法不是多 agent 架构；核心闭环由 deterministic simulation/MBD 与 LLM prompt repair 组合而成。

### 形式化/验证成分

- BPMN 是 executable model，simulation 是核心证据。
- MBD 是形式化诊断思路；minimal hitting sets 是关键求解对象。
- 但本文没有对 BPMN 或状态机进行 temporal logic model checking；它的 correctness notion 是 KPI stability / behavioral consistency，而非性质证明。

## 实验与评估

### 数据集

实验使用两个 diabetic nephropathy health-guidance policies，来自两个日本 municipality。每个 policy 用同一 synthetic patient population 进行 simulation。City 1 偏行政框架和长期管理；City 2 更 operational/clinical，包含 eligibility、exclusion 和 follow-up logic。

### 评估指标

- normalized entropy over KPI distributions。
- KPI combinations frequency。
- 修复前后 dominant outcome concentration。
- gateway-level diagnosis 与 ambiguity/repair reports 的可解释性。

KPIs 包括 Notification Count、Health Guidance Count、Guidance Resource Utilization、Health Improvement Rate、Medical Cost Savings。

### 实验设置

- 每个 policy 独立生成 100 个 BPMN 模型。
- 每个模型在同一 synthetic patient data 上模拟。
- 从 dominant KPI classes 中选 reference/target models 做 diagnosis。
- repair 使用 Tokyo Program for Prevention of Severe Progression of Diabetic Nephropathy 作为 supplemental material。

### 主要实验结果

- **City 1**：原始 policy 产生多个 distinct KPI combinations。diagnosis 定位 Check Inclusion Eligibility 与 Check Health Guidance Acceptance。修复后超过 90% 生成模型产生同一 outcome，对应 very high generation consistency。
- **City 2**：定位到四个 divergence sources，包括 quantitative urinary albumin testing eligibility 中 Category A vs Category A OR B 的解释差异。修复后 70% 生成模型产生同一 outcome，对应 high generation consistency。

### 方法优势

- 把歧义检测与 executable behavior 绑定，只处理影响 KPI 的 ambiguity。
- MBD 将模型行为差异定位到 gateways，有助于精准修复源文本。
- repair 有 evidence grounding 和 traceability metadata。
- 修复后通过 regeneration/re-simulation 复验，形成闭环。

### 方法的局限性

- 只能检测会影响监控 KPI 且在 sampled input population 中暴露的歧义。
- localization/repair 仍依赖 GPT-5.1 prompt 和 supporting evidence 完整性。
- 仅两个 case studies，领域窄。
- 输出和诊断对象是 BPMN gateways，不是 STM transitions/guards。

## 与本研究的关系

### 相关性分析

**BASELINE评估建议：`🟠`。**

四条件建议如下：

| 条件 | 建议 | 理由 |
|---|---|---|
| LLM4Modeling | 🟢 | LLM 生成 executable BPMN 并参与 repair。 |
| NL输入 | 🟢 | 输入和修复对象是自然语言政策叙述。 |
| LLM方法 | 🟢 | GPT-5.1 是生成、定位和修复的重要组件。 |
| STM族输出 | 🟡 | executable BPMN/gateway behavior 是强行为近邻，但不是 STM family。 |

它不能作为 Project 1 exact STM direct baseline，因为目标不是从需求生成状态机，而是从政策文本生成/修复 BPMN executable process specification。它适合作为“生成-仿真-诊断-修复”闭环强近邻。

### 研究定位与差异化

Project 1 的修复对象是状态机结构、迁移、守卫、时间约束等；本文修复的是自然语言源文本中的 BPMN gateway ambiguity。共同点是都把 LLM 生成物放入可执行/可诊断闭环，而不是一次性输出。

### 可借鉴之处

- **行为分布稳定性**：对同一需求多次生成状态机并比较 trace/property outcomes，可检测需求或模型生成不稳定。
- **gateway-to-text 映射**：可迁移为 transition/guard-to-requirement span mapping。
- **证据支持 repair**：状态机修复不应只改模型，也可反向提示需求歧义并保留 traceability。
- **entropy/noise 区分**：生成失败和真实规格歧义应分开记录。

### 存在的不足与改进空间

- 未生成 STM 族模型，无法作为状态机 direct baseline。
- KPI-based equivalence 可能掩盖未监控行为差异。
- 没有安全/活性/时间性质验证。
- 依赖 GPT-5.1 与外部证据，对 provider drift 敏感。

### 对本研究的启发

Project 1/4 可在 agent-loop 中加入 repeated generation + simulation/profile entropy：若多个状态机对同一 verification profile 结果分歧大，应先诊断需求/守卫歧义，再决定修模型还是修需求。本文也说明，repair report 应包含源片段、诊断元素、修改理由和支持证据。

## 重要的相关工作

### 1. 重要的前身类工作

- Requirements ambiguity detection 与 QuARS：提供文本歧义检测背景。
- Attempto Controlled English：代表受控自然语言降低歧义的传统路线。

### 2. 直接参与实验的baseline

- 作者 prior executable BPMN generation pipeline 与 Automatic Generation of Executable BPMN Models from Medical Guidelines：是本文生成/模拟基础。
- SpiffWorkflow：执行 BPMN 并产生 simulation traces 的底层工具。

### 3. 提供了重要论证的工作

- Model-based diagnosis 经典工作（Reiter、de Kleer & Williams）：提供 minimal diagnosis / hitting set 理论基础。
- BPMN behavioral difference diagnosis：提供 process model diagnosis 背景。

### 4. 在技术上提供了支持的工作

- Python AST normalization：用于 path-based logical condition equivalence。
- Tokyo diabetic nephropathy prevention program material：为 repair 提供 authoritative evidence。

### 5. 其他重要工作

- Process modeling with LLMs、BPMN generation and ambiguity-aware process modeling 等工作被原文用于说明相邻生成质量提升路线，但本文重点在 behavior-grounded ambiguity repair。

## 文献分类总结

本文是 LLM executable BPMN 生成后的 ambiguity diagnosis/repair 强近邻。它对 Project 1 的价值不在 BPMN 输出，而在行为证据驱动的闭环修复方法。建议入账为 `🟠` BPMN/process 强近邻，四条件为 `🟢/🟢/🟢/🟡`。
