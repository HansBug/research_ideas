# 基于 SysML 的文本到模型自动化 / Text to model via SysML: Automated generation of dynamical system computational models from unstructured natural language text via enhanced System Modeling Language diagrams

## 基本信息

- **标题**：Text to model via SysML: Automated generation of dynamical system computational models from unstructured natural language text via enhanced System Modeling Language diagrams
- **中文标题**：基于 SysML 的文本到模型自动化
- **作者**：Matthew Anderson Hendricks, Alice Cicirello
- **单位**：University of Cambridge, Department of Engineering
- **发表**：arXiv preprint, 2025
- **DOI**：原文未提供
- **链接**：https://arxiv.org/abs/2507.06803

**代码/仓库获取方式**：
- 原文首页未提供统一公开代码仓库链接。

**数据集获取方式**：
- 原文主要以若干 case study 展示方法可行性，未给出统一公开数据集下载入口。

## 简报

论文试图解决的是“如何从非结构化工程文本自动得到可计算的动态系统模型”。它把 SysML 作为中间表示，用 NLP 和 LLM 辅助抽取名词、关系、属性和值，再把 SysML 图进一步转成代码和 dynamical system computational model。

- **输入**：与目标系统相关的一组文档，以及描述特定系统的输入文本
- **方法**：五步式 text-to-model pipeline，利用 NLP/LLM 辅助生成 SysML BDD、属性值和关系，再做代码/模型生成
- **输出**：增强后的 SysML 图与最终的计算模型

```text
文档语料 -> 关键信息抽取 -> SysML 图生成 -> 代码生成 -> 动态系统计算模型
```

它与状态机生成不同，更接近“文本到工程模型”的广义 MBSE 自动化。

## 研究问题与动机

### 问题背景

复杂工程系统的动力学建模需要大量领域知识与手工整理，前期分析和模型搭建成本很高。

### 核心问题

1. 能否从非结构化工程文本中自动抽取可建模信息。
2. SysML 能否作为文本和计算模型之间的桥梁。
3. LLM 在哪些子步骤上有价值，哪些步骤仍要依赖规则/NLP。

### 研究动机

作者希望减少专家手工把文本知识转为可执行模型的负担，并证明“LLM only”并不是最优路线。

## 核心方法

### 方法概述

方法分五步执行：抽取关键名词、抽取关系、构建增强 SysML 图、生成代码、再生成计算模型。LLM 不直接端到端生成最终模型，而是用于若干中间环节的候选生成与验证。

### 关键技术

1. **SysML 作为中间表示**：把文本信息组织为结构化工程图。
2. **NLP + LLM 混合**：关键名词、关系、属性值等使用不同技术组合。
3. **模板化代码生成**：结合领域知识模板获得最终计算模型。
4. **case study 展示**：如 simple pendulum 的 end-to-end 例子。

## 实验与评估

### 数据集

- 论文以多个 case study 展示可行性。
- 文摘明确提到 simple pendulum 的 end-to-end 例子。

### 主要实验结果

1. 使用 SysML 中间层的方案优于纯 LLM-only 方案。
2. 该方法能完成从文本到计算模型的端到端演示。
3. LLM 在局部验证和抽取环节有效，但不是唯一核心。

### 方法的局限性

1. 输出不是状态机，而是动态系统计算模型。
2. 依赖大量模板与领域知识注入。
3. benchmark 和公开工件不足。

## 与本研究的关系

### 相关性分析

- **BASELINE评估**：🟠
- **原因**：输入端高度相似，都是自然语言到工程模型；但输出是 SysML BDD 和计算模型，不是状态机族模型。

### 可借鉴之处

1. 很值得借鉴其“LLM 只负责局部困难步骤”的混合 pipeline。
2. SysML 中间表示的设计思路对状态机生成也有启发。
3. 证明了直接 end-to-end LLM 生成未必优于工具化分解。

### 存在的不足与改进空间

1. 与控制系统状态机任务并不直接可比。
2. 缺少形式化验证闭环。
3. 工程案例公开性不强。

### 对本研究的启发

`project_1` 可以借鉴“中间结构化模型 + 局部 LLM”的方式，避免把全部难点压给一个 prompt。

## 重要的相关工作

### 1. 重要的前身类工作

- 原文把 text-to-DSL、文本到反应堆模型等工作视为相关前身，说明工程文本到形式化模型早有探索。

### 2. 直接参与实验的baseline

- 论文主要与 LLM-only 结果作比较，而非与状态机生成论文直接对比。

### 3. 提供了重要论证的工作

- 动态系统建模与复杂系统分析相关研究用来论证自动建模的工程需求。

### 4. 在技术上提供了支持的工作

- SysML、NLP 抽取和模板化代码生成构成了该方法的三类基础技术。

### 5. 其他重要工作

- simple pendulum 等示例说明该方法更偏“可计算模型”而非“行为状态图”。

## 文献分类总结

- **研究定位**：文本到广义工程模型的 MBSE 论文
- **任务类型**：结构化抽取 + SysML 中间表示 + 计算模型生成
- **输入工件**：非结构化工程文本
- **输出工件**：SysML 图和计算模型
- **输出模型类型**：SysML BDD / dynamical system model
- **使用的LLM**：LLM 参与局部抽取和验证
- **验证方式**：case study 对比与 end-to-end 演示
- **对本研究价值**：适合作为“LLM 与工具链混合建模”的邻近参照
