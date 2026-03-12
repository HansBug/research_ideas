# 基于模式的需求计算机辅助形式化 / Computer-Aided Formalization of Requirements Based on Patterns

## 基本信息

- **标题**：Computer-Aided Formalization of Requirements Based on Patterns
- **中文标题**：基于模式的需求计算机辅助形式化
- **作者**：Xi Wang, Shaoying Liu
- **单位**：Hiroshima University
- **发表**：IEICE Transactions on Information and Systems, E97-D(2)
- **年份**：2014
- **DOI**：10.1587/transinf.E97.D.198
- **链接**：https://doi.org/10.1587/transinf.E97.D.198

**代码/仓库获取方式**：
- 原文描述了原型工具，但未提供稳定公开仓库链接。

**数据集获取方式**：
- 原文未提供统一 benchmark 下载链接；通过实验性需求 formalization 任务验证。

## 简报

- **输入**：文本需求
- **方法**：预定义 formalization patterns，并用 HFSM 组织和驱动形式化过程
- **输出**：formal expressions / formal specifications

```text
文本需求 -> pattern system + HFSM 指导 -> 形式化规格
```

一句话结论：它不直接生成状态机，但用 HFSM 表达 formalization knowledge，这一点对“自动生成状态机前的需求规范化”很有借鉴价值。

## 研究问题与动机

### 核心问题
如何降低需求形式化对专家经验和数学背景的依赖。

### 研究动机
让更多开发者能在工具辅助下把文本需求转成可操作的形式规格。

## 核心方法

### 方法概述
方法把形式化经验沉淀为 pattern system，并用层次有限状态机表示这些 pattern 及其应用流程。

### 方法要点
- pattern knowledge 由计算机维护，而不是完全靠人工记忆。
- HFSM 用于组织 formalization patterns。
- 目标是把文本需求转换为形式表达式。

## 实验与评估

### 数据集
- **数据/案例**：需求形式化实验任务
- **来源类型**：实验任务

### 主要实验结果
原文报告原型工具可以有效辅助需求 formalization，并降低人工负担。

### 方法的局限性
最终输出不是状态机；更偏需求 formalization 支撑工具，而非行为模型生成器。

## 与本研究的关系

### 相关性分析
- **BASELINE评估**：🟠
- **评估理由**：它主要属于前置 formalization 支撑，而不是直接的状态机生成 baseline。
- **与本研究的主要差异**：本研究关注输出状态机模型；该文关注需求 formalization 知识辅助。

### 可借鉴之处
HFSM 组织 pattern knowledge 的方式，对构建“需求解析 -> 状态机片段生成”规则库很有参考价值。

## 文献分类总结

- **类别**：需求形式化支持
- **BASELINE评估**：🟠
- **输入**：文本需求
- **输出**：形式化规格
- **输出模型类型**：Formal specification
- **使用的LLM**：未使用
- **主要方法**：用 pattern system 和 HFSM 组织形式化知识，辅助把文本需求转成形式表达式。
