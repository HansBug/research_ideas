# 利用大语言模型从软件需求生成用例模型 / Leveraging Large Language Models for Use Case Model Generation from Software Requirements

## 基本信息

- **标题**：Leveraging Large Language Models for Use Case Model Generation from Software Requirements
- **中文标题**：利用大语言模型从软件需求生成用例模型
- **作者**：Tobias Eisenreich, Nicholas Friedlaender, Stefan Wagner
- **单位**：Technical University of Munich
- **发表**：arXiv preprint, 2025
- **DOI**：原文配套工件 DOI 为 10.5281/zenodo.15441831
- **链接**：https://arxiv.org/abs/2511.09231

**代码/仓库获取方式**：
- 论文配套工件发布在 Zenodo：https://doi.org/10.5281/zenodo.15441831

**数据集获取方式**：
- 同上，Zenodo 页面包含“Use Case Model Generation from Software Requirements”相关工件。

## 简报

这篇论文把 LLM 用在更前端的需求分析工件上：从软件需求中抽取 actors 与 use cases，形成用例模型。它不直接生成状态机，但属于“自然语言需求 -> 结构化 UML 工件”的典型预印本。

- **输入**：软件需求文本
- **方法**：open-weight LLM + prompt engineering，用于抽取 actor 和 use case
- **输出**：用例模型

```text
软件需求 -> actor / use case 抽取 -> UML 用例模型
```

实验证明该方法可把建模时间减少约 60%，但输出仍停留在 use case 层。

## 研究问题与动机

### 问题背景

用例建模在实践中常被跳过，因为人工识别 actors 和 use cases 成本高、重复性强。

### 核心问题

1. LLM 能否显著加速用例建模。
2. 在加速的同时，模型质量是否会显著下降。
3. 工程师是否会把这种辅助视为真正有帮助。

### 研究动机

作者试图验证 LLM 是否适合作为需求分析早期建模助手。

## 核心方法

### 方法概述

论文把用例建模拆成 actor 识别、use case 识别和模型整理三个步骤，由 open-weight Llama 3.1 70B 配合 prompt engineering 完成。

### 关键技术

1. **actor / use case 双阶段抽取**。
2. **prompt engineering**：约束输出结构。
3. **专业工程师参与评估**：而不是只做自动分数。

## 实验与评估

### 数据集

- 探索性研究由 **5 位专业软件工程师**参与。
- 使用真实软件需求进行人工建模与 LLM 辅助建模对比。

### 主要实验结果

1. 建模时间减少约 **60%**。
2. 模型质量保持“大致相当”。
3. 参与者认为该方法在流程上提供了有效引导。

### 方法的局限性

1. 输出是 use case model，不是行为状态机。
2. 规模较小，偏 exploratory study。
3. 未做形式化一致性或后续行为模型传播。

## 与本研究的关系

### 相关性分析

- **BASELINE评估**：🟠
- **原因**：输入与 `project_1` 很接近，但输出只到用例模型，不能直接作为状态机 baseline。

### 可借鉴之处

1. 可借鉴其“先抽 actor / use case，再下游传播”的分阶段建模思路。
2. 说明 LLM 在需求前处理和结构化提取方面很实用。
3. 对后续从需求到状态机前的场景/参与者抽取有帮助。

### 存在的不足与改进空间

1. 缺少行为语义。
2. 没有把 use case 自动传播到 sequence/state machine。
3. 工业控制系统适配性未体现。

### 对本研究的启发

本项目可以把它视为“需求前处理层”的邻近参照，而非最终 baseline。

## 重要的相关工作

### 1. 重要的前身类工作

- 原文将用例建模与既有 ChatGPT/UML 研究视为直接前情脉络。

### 2. 直接参与实验的baseline

- 直接比较的是专业工程师手工建模与 LLM 辅助建模。

### 3. 提供了重要论证的工作

- 需求分析中用例模型常被省略的工程现实，为研究提供了主要动机。

### 4. 在技术上提供了支持的工作

- PlantUML 和 open-weight LLM 是实现该方法的关键支撑。

### 5. 其他重要工作

- 配套 Zenodo 工件为后续复查其 prompts 和实验材料提供了入口。

## 文献分类总结

- **研究定位**：需求到 UML 用例模型
- **任务类型**：直接生成
- **输入工件**：软件需求文本
- **输出工件**：use case model
- **输出模型类型**：UML 用例图
- **使用的LLM**：Llama 3.1 70B
- **验证方式**：专业工程师对照实验
- **对本研究价值**：说明 LLM 在前端需求结构化阶段已较成熟，但尚未走到状态机
