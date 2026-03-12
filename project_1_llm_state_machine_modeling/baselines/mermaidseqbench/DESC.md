# MermaidSeqBench：面向 Mermaid 顺序图生成的评测基准 / MermaidSeqBench: An Evaluation Benchmark for LLM-to-Mermaid Sequence Diagram Generation

## 基本信息

- **标题**：MermaidSeqBench: An Evaluation Benchmark for LLM-to-Mermaid Sequence Diagram Generation
- **中文标题**：MermaidSeqBench：面向 Mermaid 顺序图生成的评测基准
- **作者**：Basel Shbita, Farhan Ahmed, Chad DeLuca
- **单位**：IBM Research
- **发表**：arXiv preprint, 2025
- **DOI**：原文未提供
- **链接**：https://arxiv.org/abs/2511.14967

**代码/仓库获取方式**：
- 论文明确提供 GitHub 仓库：https://github.com/IBM/MermaidSeqBench-Eval

**数据集获取方式**：
- 论文明确提供 Hugging Face 数据集：https://huggingface.co/datasets/ibm-research/MermaidSeqBench

## 简报

这篇论文把“文本到 sequence diagram”系统化成了 benchmark。虽然输出不是状态机，但 sequence diagram 是最接近行为建模的公开预印本高频方向之一。

- **输入**：文本提示
- **方法**：构建 132 样本 benchmark，并使用 LLM-as-a-judge 进行细粒度评估
- **输出**：Mermaid sequence diagrams 与多维评分

```text
文本提示 -> LLM 生成 Mermaid 顺序图 -> judge LLM 细粒度打分 -> benchmark 排名
```

论文价值主要在 benchmark 和评估范式，而不是新生成 pipeline。

## 研究问题与动机

### 问题背景

LLM 生成文本化图（如 Mermaid、PlantUML）越来越常见，但 sequence diagram 缺少统一 benchmark，导致不同模型结果难以比较。

### 核心问题

1. 如何构造可复用的文本到顺序图 benchmark。
2. 不同参数规模和模型家族在 sequence diagram 任务上有何差异。
3. judge LLM 是否能提供足够细粒度的结构评估。

### 研究动机

作者希望填补“text-to-diagram evaluation”中的 sequence diagram 空白。

## 核心方法

### 方法概述

MermaidSeqBench 从人工样本出发，结合 LLM 扩展与规则变化生成 132 个 benchmark 样本，再使用 DeepSeek-V3 与 GPT-OSS 两个 judge 分别从多维度评估 Qwen、Llama、Granite 等模型。

### 关键技术

1. **132 样本 benchmark**。
2. **双 judge LLM**：DeepSeek-V3 与 GPT-OSS。
3. **多模型横评**：Qwen 2.5、Llama 3.1/3.2、Granite 3.3。

## 实验与评估

### 数据集

- MermaidSeqBench 共 **132** 个样本。
- 仓库和数据集公开。

### 主要实验结果

1. 强模型（如 Qwen 2.5-7B、Llama 3.1-8B）明显优于小模型。
2. DeepSeek-V3 与 GPT-OSS 的打分尺度不同，表明 judge 选择会影响绝对分数。
3. 该 benchmark 揭示了 sequence diagram 生成仍存在明显能力差距。

### 方法的局限性

1. 输出是顺序图，不是状态机。
2. 结果依赖 LLM judge。
3. benchmark 仍偏软件交互流程，而非控制系统行为。

## 与本研究的关系

### 相关性分析

- **BASELINE评估**：🟠
- **原因**：任务与行为建模相邻，但输出不是状态机族模型。

### 可借鉴之处

1. benchmark 设计和公开方式很值得参考。
2. judge 双模型配置对本项目做自动评审有启发。
3. Mermaid 这种文本化图表示与本项目的文本化状态机输出兼容。

### 存在的不足与改进空间

1. 缺少状态语义。
2. 没有控制系统场景。
3. 结构评分仍不是形式化等价检查。

### 对本研究的启发

状态机 benchmark 若要公开，完全可以沿用 MermaidSeqBench 这种“文本工件 + judge + 公开数据集”路线。

## 重要的相关工作

### 1. 重要的前身类工作

- 原文把 requirements-to-sequence-diagram 和 UML 建模研究作为直接背景。

### 2. 直接参与实验的baseline

- 直接评测对象为 Qwen、Llama、Granite 三个家族的多个尺寸模型。

### 3. 提供了重要论证的工作

- 文本到图形表示的 LLM 能力增长，为 sequence benchmark 的必要性提供了论证。

### 4. 在技术上提供了支持的工作

- Mermaid、LLM-as-a-judge 和公开 Hugging Face 数据集是核心技术支撑。

### 5. 其他重要工作

- 论文显式引用了 `How LLMs Aid in UML Modeling`、`Model Generation with LLMs: From Requirements to UML Sequence Diagrams` 和 `MCeT`。

## 文献分类总结

- **研究定位**：文本到顺序图的 benchmark 论文
- **任务类型**：数据集/评测集建设
- **输入工件**：文本提示
- **输出工件**：Mermaid sequence diagrams
- **输出模型类型**：UML/Mermaid 顺序图
- **使用的LLM**：Qwen 2.5、Llama 3.x、Granite 3.3；judge 为 DeepSeek-V3、GPT-OSS
- **验证方式**：benchmark 打分
- **对本研究价值**：适合作为行为图 benchmark 与自动评审设计的公开参照
