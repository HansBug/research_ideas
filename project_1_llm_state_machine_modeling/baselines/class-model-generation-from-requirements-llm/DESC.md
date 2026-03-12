# 基于大语言模型的需求到类模型生成 / Class Model Generation from Requirements using Large Language Models

## 基本信息

- **标题**：Class Model Generation from Requirements using Large Language Models
- **中文标题**：基于大语言模型的需求到类模型生成
- **作者**：Jackson Nguyen, Rui En Koe, Fanyu Wang, Chetan Arora, Alessio Ferrari
- **单位**：Monash University；University College Dublin
- **发表**：arXiv preprint, 2026
- **DOI**：10.1145/3786146.3788643
- **链接**：https://arxiv.org/abs/2603.09100

**代码/仓库获取方式**：
- 论文给出公开工件仓库：https://github.com/jackson0076/FIT4701-GenAI

**数据集获取方式**：
- 仓库中提供需求与类图相关工件；论文也引用公开挑战集作为数据来源之一。

## 简报

这篇论文直接比较 GPT-5、Claude Sonnet 4、Gemini 2.5 Flash Thinking 和 Llama-3.1-8B 在“需求 -> PlantUML 类图”任务上的表现，并结合 Grok、Mistral 和人工评审做系统比较。

- **输入**：自然语言需求
- **方法**：CoT 抽取实体、属性、关联，再生成 PlantUML 类图
- **输出**：UML class diagram

```text
需求文本 -> 实体/属性/关联抽取 -> PlantUML 生成 -> LLM judge + 人工评审
```

它和状态机任务不同，但在“需求到结构化模型”的实验设计上非常接近。

## 研究问题与动机

### 问题背景

类图生成是需求建模中一个高频但耗时的任务，也是最容易被 LLM 自动化的建模环节之一。

### 核心问题

1. 当前主流 LLM 生成类图的水平如何。
2. LLM-as-a-judge 与人工评审是否一致。
3. 不同模型在结构提取上的差异是否稳定。

### 研究动机

作者希望为 requirements-to-model 任务提供更严格的多模型、多评审者比较。

## 核心方法

### 方法概述

方法用 CoT 从需求中提取 domain entities、attributes、associations，再生成 PlantUML 表示，随后让 Grok、Mistral 和人工评审者从多个维度给出排名和统计分析。

### 关键技术

1. **多模型横评**：GPT-5、Claude、Gemini、Llama。
2. **双 LLM judge + 人工评审**。
3. **统计显著性分析**：含 effect size 等比较。

## 实验与评估

### 数据集

- 论文使用多领域 requirements-driven 类图案例。
- 工件仓库公开，可复查 prompts、结果和评分材料。

### 主要实验结果

1. GPT-5 和 Claude Sonnet 4 排名最靠前。
2. Grok 与 Mistral 两个 judge 的排序总体一致。
3. 论文证明 LLM judge 可用于 requirements-to-model 任务的辅助评审，但仍需人工兜底。

### 方法的局限性

1. 输出是类图，不是行为模型。
2. 语义正确性仍难仅靠自动评审完全覆盖。
3. 与控制系统状态转换语义不直接对应。

## 与本研究的关系

### 相关性分析

- **BASELINE评估**：🟠
- **原因**：任务非常接近“需求到模型”，但工件类型是类图而不是状态机。

### 可借鉴之处

1. 多模型横评设计非常适合复用到状态机生成实验。
2. LLM judge + human evaluation 的组合值得借鉴。
3. PlantUML 作为文本中间表示与本项目已有实践兼容。

### 存在的不足与改进空间

1. 缺少行为与时序语义。
2. 不涉及状态、事件、守卫等核心信息。
3. 仍未把需求噪声与修复闭环连接起来。

### 对本研究的启发

这篇论文为 `project_1` 提供了非常实用的实验学设计模板，尽管其输出工件不在状态机主线内。

## 重要的相关工作

### 1. 重要的前身类工作

- 原文延续了 Ferrari 团队在 requirements-to-UML 方向的工作脉络。

### 2. 直接参与实验的baseline

- 直接对比对象是 GPT-5、Claude Sonnet 4、Gemini 2.5 Flash Thinking 和 Llama-3.1-8B。

### 3. 提供了重要论证的工作

- 既有 requirements-to-UML 与 LLM 建模研究被用于说明：需求到图模型自动化已具备实验基础。

### 4. 在技术上提供了支持的工作

- PlantUML、Grok judge、Mistral judge 与统计检验共同支撑实验。

### 5. 其他重要工作

- 公开 GitHub 工件使这篇论文在复查和后续复现实验方面价值较高。

## 文献分类总结

- **研究定位**：需求到 UML 类图生成
- **任务类型**：直接生成
- **输入工件**：自然语言需求
- **输出工件**：PlantUML 类图
- **输出模型类型**：UML class diagram
- **使用的LLM**：GPT-5、Claude Sonnet 4、Gemini 2.5 Flash Thinking、Llama-3.1-8B
- **验证方式**：LLM judges + human evaluation
- **对本研究价值**：对实验设计和评测组织方式最有参考意义
