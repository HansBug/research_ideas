# 最佳流程模型表示是什么？面向 LLM 流程建模的比较分析 / What is the Best Process Model Representation? A Comparative Analysis for Process Modeling with Large Language Models

## 基本信息

- **标题**：What is the Best Process Model Representation? A Comparative Analysis for Process Modeling with Large Language Models
- **中文标题**：最佳流程模型表示是什么？面向大语言模型流程建模的比较分析
- **作者**：Alexis Brissard、Frédéric Cuppens、Amal Zouaq
- **单位**：Polytechnique Montréal；LabCys；LAMA-WeST Lab
- **发表**：arXiv:2507.11356，2025-07-15 预印本
- **DOI**：10.48550/arXiv.2507.11356
- **链接**：[arXiv](https://arxiv.org/abs/2507.11356)；[PDF](https://arxiv.org/pdf/2507.11356)；[GitHub](https://github.com/Lama-West/Process_Model_Representations)；[PMo Dataset Zenodo](https://doi.org/10.5281/zenodo.15857588)

**代码/仓库获取方式**：
- 原文明确说明项目代码、数据、prompts 和 results 可在 `https://github.com/Lama-West/Process_Model_Representations` 获取；本次建档时 GitHub 页面可访问。
- PMo Dataset DOI 为 `10.5281/zenodo.15857588`；本次 HTTP 头检查可解析到 Zenodo DOI 页面，未进一步下载核验内容。

**数据集获取方式**：
- 原文构建 PMo Dataset：55 个 process descriptions，对应 9 种 process model representations。
- 数据来源包括 Mangler dataset、PMoBenchmark、PET-7、BPMN for Research、CCC19；Zenodo DOI 如上。

## 简报

本文解决的问题是：LLM-based process modeling 中出现了许多流程模型表示（PMR），例如 BPMN XML、Graphviz、Mermaid、PME JSON、POWL code、BPMN text、JSON branches 等，但它们在 token compactness、expressivity、readability、visualization、usability、extensibility 以及实际生成效果上缺少系统比较。作者构建 PMo Dataset，并比较 9 种 PMR 在 PMo 和 PMG 任务中的表现。

- **输入**：自然语言 process descriptions。
- **方法**：为每个 ground-truth BPMN 转换出 9 种 PMR；从 PMo 需求角度做定性/定量评分；再用 LLaMA-3.3-70B 在统一 prompt 下生成不同 PMR，并用 element counts 和 PME similarity 比较。
- **输出**：不同 PMR 的 ground truth / generated representations，以及 PMR suitability ranking；不是一个新 BPMN 生成器本身。

```text
输入层：55 个自然语言流程描述 + ground-truth BPMN
  -> 方法层：BPMN-to-PMR converters + PMR requirement evaluation + LLaMA-3.3-70B PMG experiments
  -> 输出层：9 种 PMR 对比结果 + PMo Dataset + PMG similarity scores
```

结果显示，Mermaid 在 PMo 六项综合指标中最好；BPMN text 在 PMG task 中 process element similarity 最高。LLM 普遍 under-generate process elements，尤其 gateways；branching PMRs（BPMN text、JSON branches）能部分缓解 omissions。本文是 representation/evaluation 强近邻，不是 STM generation baseline。

**可比字段快照**：

- **输入**：自然语言流程描述。
- **输出**：BPMN/Graphviz/Mermaid/PME/Simplified XML/POWL code/BPMN text/JSON branches 等 process model representations。
- **输出模型类型**：process model representations；部分可转换为 BPMN；非 STM 族。
- **使用的 LLM**：LLaMA-3.3-70B，通过 Google Vertex AI API；temperature 0.2、top-p 0.95。
- **主要方法**：PMR taxonomy + PMo Dataset + converter validation + standardized prompting + element count / PME similarity evaluation。
- **需求词工程**：中；每种 PMR prompt 提供一致结构、formatting guidelines 和示例。
- **运行仿真/验证**：无仿真；有 representation conversion validation 和 similarity evaluation。
- **形式化验证**：无 model checking；重点是 representation suitability 与 generation similarity。

## 研究问题与动机

### 问题背景

LLM 在 BPM 领域被用于 process model generation，但直接生成标准 BPMN 受 context length、冗长 XML 和结构错误限制。研究者因此引入多种 PMR 作为输出抽象或中间表示。不同论文各用各的表示、评估方法和 benchmark，难以比较。

### 核心问题

本文回答三个 RQ：不同 PMR 有哪些关键特征；哪些 PMR 最适合 LLM-based PMo；哪些 PMR 在 PMG 中产生最佳生成效果。

### 研究动机

如果输出表示不合适，LLM 可能遗漏 gateways、简化结构或产生无效格式。选择 PMR 会影响 token cost、可读性、可视化、工具集成和模型质量。本文希望为未来 LLM process modeling pipeline 提供 representation selection 依据。

### 研究意义

对 Project 1，本文最重要的启发是：状态机生成也需要比较不同 representation，例如 JSON schema、DSL、Mermaid stateDiagram、PlantUML、pyfcstm DSL、XML 等，不能默认某一种最适合 LLM。

### 现有方法的局限性

现有 PMG 工作常各自使用 Graphviz/Mermaid、POWL code、BPMN text、JSON branches 等 PMR，并在小数据集/不同指标上报告结果；缺少统一 dataset 和同一 LLM 下的表示层比较。

### 研究目标

构建 largest gold-standard PMo dataset to date（原文称 55 pairs），并在 9 种 PMR 上比较 PMo suitability 与 PMG performance。

## 核心方法

### 方法概述

方法分为：

1. 定义 process model、PMR、PMR model。
2. 选择 9 种 PMR 并描述语言、graph/branch based、executable、visualizable、schema 等特征。
3. 构建 PMo Dataset。
4. 定义 PMo with LLMs 的 6 个 PMR requirements。
5. 用 LLaMA-3.3-70B 在每种 PMR 上做 PMG 实验。

### 9 种 PMR

包括 BPMN XML、BPMN process、Graphviz、Mermaid、PME JSON、Simplified XML、POWL code、BPMN text、JSON branches。它们在 compactness、expressiveness、visualization、parsability、schema support 等方面差异明显。

### PMo Dataset

数据集含 55 个 process descriptions，来源：

- Mangler dataset：24 pairs。
- PMoBenchmark：20 pairs。
- PET-7：6 pairs。
- BPMN for Research：4 pairs。
- CCC19：1 pair。

作者选择这些来源是因为模型由专家手工构造或验证；没有采用 MaD，因为原文认为其模型/描述 variability 不足。BPMN ground truth 经 label cleanup、layout improvement、decision/condition positioning 等 preprocessing，再自动转换到各 PMR。

### PMR suitability requirements

六项要求：Token compactness、Expressivity、Human readability、Visualization capabilities、Usability、Extensibility。定量看长度和 element coverage，定性看可读性、可视化、可解析/可编辑/工具支持和扩展难度。

### PMG 实验

为公平比较，PMG 限制元素为 standard tasks、start/end events、exclusive/parallel gateways、sequence flows。每种 PMR prompt 保持同样 task description/general instructions，并提供各自 format guidelines 和示例。LLM 使用 LLaMA-3.3-70B，Vertex AI API，Top-P 0.95、Temperature 0.2。

### 评估指标

- element counts：各类型 process elements 数量。
- PME similarity：对 tasks/events/gateways/sequence flows 做 semantic matching，使用 sentence transformer `stsb-mpnet-base-v2` 和 0.7 threshold，再计算 Dice-Sørensen coefficient。

## 实验与评估

### PMo suitability 结果

Table 4 中 Mermaid 平均最高 4.00，得益于 token compactness 和 visualization；Graphviz 3.67；BPMN process / Simplified XML 约 3.50；BPMN XML 3.33；POWL code 2.83；BPMN text 2.67；JSON branches 3.00。BPMN 原始 XML expressivity 高但 compactness/readability 差。

### PMG 结果

LLM 生成模型普遍比 ground truth 小，平均少约 8.23 个 nodes，gateways 缺失尤为明显：exclusive gateways 平均少 3.01，parallel gateways 少 1.72。BPMN text 和 JSON branches 由于显式 branching structure，生成 element counts 更接近 ground truth。

PME similarity 表中 BPMN text overall 0.54、JSON branches 0.53，为最高；Mermaid 0.48、Graphviz 0.47；POWL code 0.27，且 40% generated models invalid，说明在有限 prompt budget 下 code PMR 不一定可靠。

### 主要结论

- Mermaid 最适合一般 PMo with LLMs，因为 compact、可视化、可读性较好。
- BPMN text 最适合 PMG similarity，因为 branching structure 能减少 gateways omissions。
- 单一 PMR 未必适合所有阶段，pipeline 可在不同阶段使用不同 PMR。

### 方法优势

- 系统比较 PMR，而非提出又一个单点生成器。
- 数据集、代码、prompts、results 原文声明公开。
- 明确指出 under-generation/gateway omission 是 LLM process generation 的普遍问题。
- 对 representation design 提供可复用评估维度。

### 方法的局限性

- PMo suitability 评分仍带作者主观性。
- PMR 格式标准化选择可能影响 LLM 行为。
- 未包含 BPMN Sketch、JSON-Nets 等潜在 PMR。
- PME similarity 受生成元素数量影响大。
- PMG 实验只覆盖简化元素集，不含 swimlanes/data objects 等复杂现实模型。
- 没有人工评估 generated models。

## 与本研究的关系

### 相关性分析

**BASELINE评估建议：`🟠`。**

四条件建议如下：

| 条件 | 建议 | 理由 |
|---|---|---|
| LLM4Modeling | 🟢 | 研究对象是 LLM process modeling / process model generation。 |
| NL输入 | 🟢 | PMG 输入是自然语言 process descriptions。 |
| LLM方法 | 🟢 | LLaMA-3.3-70B 是 PMG 实验核心。 |
| STM族输出 | 🟡 | PMRs 是 BPMN/process 表示，强行为近邻但非 STM-family。 |

它不能评为 exact STM direct baseline，因为论文比较 BPMN/process model representations，并不生成或评估状态机族模型。

### 研究定位与差异化

本文更像“表示选择与评估方法”论文，而非生成系统论文。对 Project 1，它可作为设计 STM 输出格式的依据：不同表示会影响 LLM 的结构召回、gateway/transition 保存、可解析性和后续验证。

### 可借鉴之处

- **representation benchmark**：Project 1 可比较 pyfcstm DSL、JSON IR、PlantUML/Mermaid statechart、UML XML 等。
- **under-generation 指标**：状态机生成也可能少 states/transitions/guards，应统计元素缺失。
- **多维要求**：compactness、expressivity、readability、visualization、usability、extensibility 可迁移到 STM representation selection。
- **semantic element matching**：可用于状态/事件/动作 label matching。

### 存在的不足与改进空间

- 没有控制系统或 STM 数据。
- 没有验证生成模型可执行/可满足性质。
- LLaMA 单模型实验不能代表所有 LLM。
- 只比较 process representations，不涉及 repair/feedback loop。

### 对本研究的启发

Project 1 不应默认“让 LLM 输出最终 DSL”就是最优。可以先做小规模 representation ablation：同样需求、同样模型、不同 STM 表示，比较 parse success、state/transition/guard F1、semantic diagnostics、token cost 和修复难度。

## 重要的相关工作

### 1. 重要的前身类工作

- ConverMod、ProMoAI、MAO、BPMN-chatbot、多模态 process extraction：提供主要 PMR 来源。
- Mangler、PMoBenchmark、PET、BPMN for Research、CCC19：PMo Dataset 来源。

### 2. 直接参与实验的baseline

- 9 种 PMR 本身是实验对象：BPMN、BPMN process、Graphviz、Mermaid、PME、Simplified XML、POWL code、BPMN text、JSON branches。
- LLaMA-3.3-70B 是统一 PMG 生成模型。

### 3. 提供了重要论证的工作

- Kourani 等 LLM process modeling benchmark、自改进分析。
- Fettke/Houy 等 LLM process modeling ability evaluation。
- Bellan PET dataset 与 process extraction benchmark。

### 4. 在技术上提供了支持的工作

- sentence transformer `stsb-mpnet-base-v2`：PME semantic matching。
- BPMNDiffViz 与 process model similarity tools：相关评估背景。

### 5. 其他重要工作

- BPMN Sketch Miner、JSON-Nets 等未纳入但被作者作为 future exploration 候选。

## 文献分类总结

本文是 BPMN/process representation selection 强近邻。它的主要价值是告诉 Project 1：输出表示本身就是实验变量。建议入账为 `🟠` BPMN/process 强近邻，四条件为 `🟢/🟢/🟢/🟡`。
