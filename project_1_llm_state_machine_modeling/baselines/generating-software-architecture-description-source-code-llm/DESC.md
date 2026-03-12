# 利用逆向工程与大语言模型从源码生成软件架构描述 / Generating Software Architecture Description from Source Code using Reverse Engineering and Large Language Model

## 基本信息

- **标题**：Generating Software Architecture Description from Source Code using Reverse Engineering and Large Language Model
- **中文标题**：利用逆向工程与大语言模型从源码生成软件架构描述
- **作者**：Ahmad Hatahet, Christoph Knieke, Andreas Rausch
- **单位**：Technical University of Clausthal
- **发表**：arXiv preprint, 2025
- **DOI**：原文未提供
- **链接**：https://arxiv.org/abs/2511.05165

**代码/仓库获取方式**：
- 原文明确给出 GitHub 仓库：https://github.com/ahmadhatahet/generate-software-architecture-description-using-llm

**数据集获取方式**：
- 论文以案例系统做验证，相关图像、notebooks 和 prompts 在仓库中公开。

## 简报

这篇论文不是从需求生成模型，而是从源码恢复架构描述。它的一个亮点是：除了 component diagram，还显式生成了 per-component **state machine diagrams**，因此与行为恢复有一定直接关系。

- **输入**：源代码 + 逆向工程得到的静态结构信息
- **方法**：先恢复 comprehensive component diagram，再对各组件做 few-shot state machine generation
- **输出**：SAD 中的 component views 与 state machine views

```text
源码 -> 逆向工程提取结构 -> GPT-4o 生成组件图 -> 按组件生成状态机图 -> SAD
```

它不是自然语言到状态机，但在“设计恢复到状态机视图”上值得保留。

## 研究问题与动机

### 问题背景

很多系统缺少最新的 SAD，开发者不得不直接从源码理解结构和行为，成本高且容易产生偏差。

### 核心问题

1. 能否从源码半自动恢复可读的 SAD。
2. LLM 能否把组件内部逻辑转写为状态机图。
3. 逆向工程与 LLM 如何协同，而不是互相替代。

### 研究动机

作者希望缓解“文档老化”问题，让 LLM 辅助软件架构恢复和行为视图恢复。

## 核心方法

### 方法概述

先利用逆向工程工具提取 comprehensive class/component information，再用 GPT-4o 过滤 architecturally significant elements，随后按组件生成 state machine diagrams，并将多视图汇总为 SAD。

### 关键技术

1. **RE + LLM 混合**：结构依赖逆向工程，语义抽象依赖 LLM。
2. **few-shot prompting**：帮助 GPT-4o 生成 state machine views。
3. **多视图 SAD**：同时恢复静态与行为视角。

## 实验与评估

### 数据集

- 论文以 Coffee Machine 等案例系统做展示。
- 仓库公开图像、notebooks 和 prompts。

### 主要实验结果

1. 方法能够生成可读的 component diagrams 和 state machine diagrams。
2. GPT-4o 对显式控制逻辑恢复较好，但对隐含状态层级和复杂语义仍有不足。
3. 作者认为该流程是可行路径，而不是完全自动替代人工架构师。

### 方法的局限性

1. 输入是源码，不是自然语言需求。
2. 状态机恢复质量依赖组件逻辑显式度。
3. 对隐式状态、层次状态和复杂并发行为仍有挑战。

## 与本研究的关系

### 相关性分析

- **BASELINE评估**：🟡
- **原因**：虽然输入不是自然语言，但输出明确包含 state machine diagrams，且任务本质是从既有设计/实现恢复行为模型，能作为状态机恢复邻近 baseline。

### 可借鉴之处

1. 很适合作为“状态机恢复/补全”旁路参考。
2. RE + LLM 混合思路对从设计文档、代码和需求多源恢复状态机很有启发。
3. per-component state machine generation 的设定可迁移到复杂系统分解生成。

### 存在的不足与改进空间

1. 不是需求到状态机。
2. 更偏软件架构恢复，而非控制系统建模。
3. 缺少形式化验证回路。

### 对本研究的启发

本项目若后续考虑“从已有设计/代码反推状态机以辅助修复”，这篇论文可以直接作为近邻参照。

## 重要的相关工作

### 1. 重要的前身类工作

- 原文继承了 reverse engineering、component identification 与 UML/PlantUML 生成的研究脉络。

### 2. 直接参与实验的baseline

- 论文更偏方法展示，没有设置丰富外部生成 baseline。

### 3. 提供了重要论证的工作

- SAD 缺失、过时和与源码不一致的问题，是整篇论文的核心动机。

### 4. 在技术上提供了支持的工作

- Doxygen、PlantUML 和 GPT-4o 是该方法的关键支撑。

### 5. 其他重要工作

- 作者仓库公开了 diagrams、notebooks 和 prompts，复现友好度较高。

## 文献分类总结

- **研究定位**：从设计/实现恢复架构与行为视图
- **任务类型**：恢复 / 生成
- **输入工件**：源代码 + 逆向工程结果
- **输出工件**：SAD、component diagrams、state machine diagrams
- **输出模型类型**：软件架构图 + 状态机图
- **使用的LLM**：GPT-4o
- **验证方式**：案例系统展示与仓库公开工件
- **对本研究价值**：可作为“行为模型恢复”方向的近邻条目
