# 基于 SysML v2 的 LLM 语义对齐与集成 / LLM-Assisted Semantic Alignment and Integration in Collaborative Model-Based Systems Engineering Using SysML v2

## 基本信息

- **标题**：LLM-Assisted Semantic Alignment and Integration in Collaborative Model-Based Systems Engineering Using SysML v2
- **中文标题**：基于 SysML v2 的 LLM 语义对齐与集成
- **作者**：Zirui Li, Stephan Husung, Haoze Wang
- **单位**：Technische Universität Ilmenau, Product and Systems Engineering Group
- **发表**：arXiv preprint, 2025（作者版同时说明已被 IEEE ISSE 2025 接收）
- **DOI**：作者版首页未给出
- **链接**：https://arxiv.org/abs/2508.16181

**代码/仓库获取方式**：
- 原文首页未提供公开代码仓库链接。

**数据集获取方式**：
- 论文围绕协同 MBSE 集成场景构造示例模型，未给出统一公开数据集入口。

## 简报

这篇论文关注跨组织协同 MBSE 中的“语义对齐”问题。输入是多个独立开发的 SysML v2 模型，作者利用 variation points、part definitions、ports 等 SysML v2 构造，再借助 LLM 进行 prompt-driven alignment，输出则是更一致的集成模型。

- **输入**：多个语义不完全一致的 SysML v2 模型
- **方法**：prompt-driven semantic alignment + SysML v2 结构构造辅助集成
- **输出**：语义对齐后的 SysML v2 集成模型

```text
独立 SysML v2 模型 -> 差异识别 / 语义对齐 -> 集成规则生成 -> 对齐后的协同模型
```

它不是状态机生成论文，但属于 LLM 进入 MBSE 工具链的重要旁支。

## 研究问题与动机

### 问题背景

跨组织协同 MBSE 经常面临术语、结构和粒度不一致的问题。即使采用 SysML v2，也不能自动解决语义对齐。

### 核心问题

1. LLM 是否能辅助不同 SysML v2 模型之间的语义对齐。
2. 哪些 SysML v2 结构最适合承载 alignment 信息。
3. prompt 设计如何在集成过程中逐步改进。

### 研究动机

作者的目标是减少人工模型集成成本，让 LLM 作为协同 MBSE 的“语义调和器”。

## 核心方法

### 方法概述

方法围绕 SysML v2 的 variation points、parts、ports 等构造展开，通过多轮 prompt 逐步识别语义相近或冲突的元素，并形成集成结果。

### 关键技术

1. **SysML v2 原生构造**：避免只在自由文本层面做对齐。
2. **prompt iteration**：逐轮改进 alignment 结果。
3. **协同场景导向**：强调多个模型之间的关系而非单模型生成。

## 实验与评估

### 数据集

- 论文以 collaborative MBSE 集成场景为主，未给出大规模公开 benchmark。

### 主要实验结果

1. LLM 能在一定程度上帮助识别和解释语义差异。
2. SysML v2 的结构化构造可提升集成过程的可解释性。
3. 论文重点是方法论与交互式 alignment 流程，而不是大规模 quantitative 排名。

### 方法的局限性

1. 任务是模型对齐，不是模型生成。
2. 缺少公开 benchmark 和大规模统计。
3. 未专门聚焦行为模型或状态机。

## 与本研究的关系

### 相关性分析

- **BASELINE评估**：🟠
- **原因**：论文不做自然语言到状态机生成，而是做 SysML v2 模型之间的语义集成；对 `project_1` 的价值主要在多来源模型融合环节。

### 可借鉴之处

1. 可借鉴其“先结构化，再对齐”的思路处理多轮生成结果合并。
2. 对未来做多模型 ensemble 或修复结果合并有启发。
3. 说明 SysML v2 构造本身可以成为 LLM 对齐的支点。

### 存在的不足与改进空间

1. 没有处理状态机特有的事件、守卫和并发语义。
2. 不涉及自然语言输入。
3. 没有形成可直接对比的 baseline 实验表。

### 对本研究的启发

当 `project_1` 后续考虑“多个候选状态机如何合并”时，这篇论文提供了可借鉴的语义对齐视角。

## 重要的相关工作

### 1. 重要的前身类工作

- 原文把 ontology-based alignment 与 SysML 模型语义检查工作作为重要前身。

### 2. 直接参与实验的baseline

- 论文没有设置外部生成 baseline，重点是 alignment prompt 的迭代设计。

### 3. 提供了重要论证的工作

- 协同 MBSE 的语义不一致问题构成了论文的主要问题动机。

### 4. 在技术上提供了支持的工作

- SysML v2、OWL/ontology 映射和 variation point 建模构成技术支持。

### 5. 其他重要工作

- 论文把 LLM 看作集成辅助器而不是最终裁决者，这一点对工程可追溯性很重要。

## 文献分类总结

- **研究定位**：协同 MBSE 语义对齐
- **任务类型**：模型对齐 / 模型集成
- **输入工件**：多个 SysML v2 模型
- **输出工件**：集成后的对齐模型
- **输出模型类型**：SysML v2 结构模型
- **使用的LLM**：原文未强调固定单一模型
- **验证方式**：案例驱动的对齐流程分析
- **对本研究价值**：适合作为多候选模型融合与一致性整理的旁证
