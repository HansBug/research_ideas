# 从场景与需求综合有限状态协议 / Synthesizing Finite-state Protocols from Scenarios and Requirements

## 基本信息

- **标题**：Synthesizing Finite-state Protocols from Scenarios and Requirements
- **中文标题**：从场景与需求综合有限状态协议
- **作者**：Rajeev Alur, Milo Martin, Mukund Raghothaman, Christos Stergiou, Stavros Tripakis, Abhishek Udupa
- **单位**：University of Pennsylvania, UC Berkeley, Aalto University
- **发表**：arXiv preprint
- **年份**：2014
- **DOI**：原文未提供
- **链接**：https://arxiv.org/abs/1402.7150

**代码/仓库获取方式**：
- 原文未提供稳定公开仓库链接。

**数据集获取方式**：
- 原文未提供统一数据集下载链接；输入是 scenarios 与 safety/liveness requirements。

## 简报

- **输入**：Message Sequence Charts 场景 + 安全/活性 requirements
- **方法**：先从场景得到不完整状态机，再补全各进程转移关系使全局积满足需求
- **输出**：distributed finite-state protocols

```text
场景 + 安全/活性需求 -> 不完整状态机 -> 协议补全 -> 有限状态协议
```

一句话结论：它把场景综合推进到“分布式有限状态协议”层面，和控制逻辑状态机综合有明显方法学相通性。

## 研究问题与动机

### 问题背景
MSC 场景直观但不完整，协议实现仍需要完整的状态机。

### 核心问题
如何在已有场景覆盖部分状态的前提下，补全协议状态机使其满足安全与活性需求。

### 研究动机
把场景化规格直接转成可实现、可验证的有限状态协议。

## 核心方法

### 方法概述
论文先从场景导出不完整状态机，再将综合问题转化为受需求约束的转移补全过程。

### 方法要点
- 输入同时包含行为场景和形式化 requirements。
- 强调 distributed implementation。
- 综合对象是各进程的 finite-state machines。

## 实验与评估

### 数据集
- **数据/案例**：协议场景与需求示例
- **来源类型**：算法案例

### 主要实验结果
作者表明在场景充分覆盖目标实现状态时，可以自动得到满足需求的有限状态协议实现。

### 方法的局限性
输入不是自然语言，而是场景和形式化 requirement；更接近协议/分布式系统而非控制系统需求文档。

## 与本研究的关系

### 相关性分析
- **BASELINE评估**：🟡
- **评估理由**：输出是明确的有限状态机/协议，和本研究很近；但输入已是场景与形式化要求。
- **与本研究的主要差异**：本研究更关注自然语言入口和控制系统语义抽取。

### 可借鉴之处
“先得不完整状态机，再做约束补全”的两阶段思想很适合迁移到 LLM 生成后的 repair 阶段。

## 文献分类总结

- **类别**：场景与性质驱动的有限状态协议综合
- **BASELINE评估**：🟡
- **输入**：MSC 场景 + safety/liveness requirements
- **输出**：有限状态协议
- **输出模型类型**：Distributed finite-state machines
- **使用的LLM**：未使用
- **主要方法**：从场景得到不完整状态机，再在需求约束下补全转移关系。
