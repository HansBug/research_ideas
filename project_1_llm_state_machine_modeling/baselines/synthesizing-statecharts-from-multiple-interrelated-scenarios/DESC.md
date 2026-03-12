# 从多个相互关联场景综合状态图 / Synthesizing Statecharts from Multiple Interrelated Scenarios

## 基本信息

- **标题**：Synthesizing Statecharts from Multiple Interrelated Scenarios
- **中文标题**：从多个相互关联场景综合状态图
- **作者**：Simona Vasilache, Jiro Tanaka
- **单位**：University of Tsukuba
- **发表**：International Symposium on Future Software Technology
- **年份**：2001
- **DOI**：原文未提供
- **链接**：https://www.iplab.cs.tsukuba.ac.jp/paper/international/simona-isfst2001.pdf

**代码/仓库获取方式**：
- 原文未提供公开代码/仓库获取链接。

**数据集获取方式**：
- 原文未提供公开数据集；以需求场景和事件轨迹图为输入。

## 简报

本文关注多个彼此有关联的需求场景，研究怎样在考虑场景关系的前提下综合出统一 statechart。

- **输入**：多个相互关联的 scenarios / event trace diagrams
- **方法**：基于规则的多场景综合，显式处理场景之间的关系
- **输出**：综合后的 statecharts

```text
多场景需求 -> 场景关系分析与规则综合 -> statecharts
```

一句话结论：它比“单场景逐个转 statechart”的思路更贴近真实需求文档，属于经典的场景到状态机工作。

## 研究问题与动机

### 问题背景
真实系统需求通常包含大量互相关联的场景，而不是孤立场景。

### 核心问题
如何在不割裂场景关系的前提下，从多个 scenario 自动综合一个更完整的 statechart。

### 研究动机
提升状态图对需求规格的覆盖性和一致性，避免逐场景转换导致的碎片化问题。

## 核心方法

### 方法概述
作者提出一组规则，把多个 interrelated scenarios 综合成 statechart，并把它作为更准确描述需求规格的手段。

### 方法要点
- 明确考虑场景间的共享事件与关系。
- 避免把每个 scenario 分别独立翻译。
- 输出目标是统一状态图，而非若干局部片段。

## 实验与评估

### 数据集
- **数据/案例**：scenario / event trace diagram 示例
- **来源类型**：说明性案例

### 主要实验结果
论文展示了多个相关场景联合综合 statechart 的可行性与表达优势。

### 方法的局限性
输入不是自然语言原文，而是已经整理成场景表示；工具化和规模化实验都比较有限。

## 与本研究的关系

### 相关性分析
- **BASELINE评估**：🟡
- **评估理由**：输出是 statechart，任务主线一致；但输入是场景表示，不是自然语言控制需求。
- **与本研究的主要差异**：本研究要解决文本入口，该文更像场景级后端综合器。

### 可借鉴之处
多场景冲突与合并规则，对本研究处理多条需求语句的整合很有参考价值。

### 对本研究的启发
自然语言需求若先抽取为多个场景，再做统一 statechart 综合，是一条很可行的 pipeline。

## 重要的相关工作

### 1. 重要的前身类工作
- OMT/UML 中 use case 与 scenario 作为需求表达入口是本文的重要前提。

### 2. 提供了重要论证的工作
- 论文指出单场景独立转换不足以覆盖真实需求规格。

### 3. 在技术上提供了支持的工作
- 事件轨迹图、场景关系建模与 statechart 规则综合是核心技术。

## 文献分类总结

- **类别**：多场景到状态图综合
- **BASELINE评估**：🟡
- **输入**：多个互相关联的场景
- **输出**：综合 statechart
- **输出模型类型**：Statechart
- **使用的LLM**：未使用
- **主要方法**：基于场景关系的规则系统，把多个 scenario 联合综合为统一 statechart。
