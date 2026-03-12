# 从场景与时序性质精确识别有限状态机 / Exact Finite-State Machine Identification from Scenarios and Temporal Properties

## 基本信息

- **标题**：Exact Finite-State Machine Identification from Scenarios and Temporal Properties
- **中文标题**：从场景与时序性质精确识别有限状态机
- **作者**：Vladimir Ulyantsev, Igor Buzhinsky, Anatoly Shalyto
- **单位**：ITMO University 等
- **发表**：International Journal on Software Tools for Technology Transfer
- **年份**：2017
- **DOI**：10.1007/s10009-016-0442-1
- **链接**：https://doi.org/10.1007/s10009-016-0442-1

**代码/仓库获取方式**：
- 原文下载稿未提供稳定公开仓库链接。

**数据集获取方式**：
- 原文未给统一公开 benchmark；输入来自 scenarios 与 temporal properties。

## 简报

- **输入**：场景集合 + temporal properties
- **方法**：求解最小化/精确 FSM identification 问题
- **输出**：满足场景与时序性质的 FSM

```text
场景 + 时序性质 -> 精确识别 / 约束求解 -> 最小 FSM
```

一句话结论：它不是自然语言入口，但在“行为证据 + 形式化性质 -> FSM”这条线上很强，可作为状态机综合后端基线。

## 研究问题与动机

### 问题背景
有限状态机既用于验证，也用于可视化软件模型，关键难点是如何得到更小、更一般化的自动机。

### 核心问题
如何从场景和时序性质中精确识别满足约束的最小 FSM。

### 研究动机
在保证满足规格的前提下，得到更紧凑、可理解的状态机模型。

## 核心方法

### 方法概述
作者把 FSM identification 建模为精确求解问题，在场景和时序约束下综合最小 FSM。

### 方法要点
- 兼顾正例场景与时序性质。
- 目标不是任意可行解，而是更小的精确 FSM。
- 更适合作为后端状态机求解器。

## 实验与评估

### 数据集
- **数据/案例**：场景 + temporal properties 示例
- **来源类型**：算法实验

### 主要实验结果
原文表明精确方法可生成更小、更一般化的 FSM，并保持对规格的满足。

### 方法的局限性
输入不是自然语言，而是已提炼的场景和时序性质；与需求文本之间还需要额外桥接层。

## 与本研究的关系

### 相关性分析
- **BASELINE评估**：🟡
- **评估理由**：输出是直接可比的 FSM，但输入是形式化行为证据，不是需求文本。
- **与本研究的主要差异**：本研究需要完成需求理解；该文重点是状态机识别求解。

### 可借鉴之处
适合作为自然语言/LLM 前端之后的状态机求解与压缩后端。

## 文献分类总结

- **类别**：场景与性质约束下的 FSM 综合
- **BASELINE评估**：🟡
- **输入**：场景 + 时序性质
- **输出**：FSM
- **输出模型类型**：Finite-state machine
- **使用的LLM**：未使用
- **主要方法**：在场景和 temporal properties 约束下精确识别满足要求的最小 FSM。
