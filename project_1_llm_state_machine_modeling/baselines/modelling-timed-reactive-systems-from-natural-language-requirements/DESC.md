# 从自然语言需求建模定时反应式系统 / Modelling Timed Reactive Systems from Natural-Language Requirements

## 基本信息

- **标题**：Modelling Timed Reactive Systems from Natural-Language Requirements
- **中文标题**：从自然语言需求建模定时反应式系统
- **作者**：Gustavo Carvalho, Ana Cavalcanti, Augusto Sampaio
- **单位**：University of York / Universidade Federal de Pernambuco
- **发表**：Formal Aspects of Computing
- **年份**：2016
- **DOI**：10.1007/s00165-016-0387-x
- **链接**：https://doi.org/10.1007/s00165-016-0387-x

**代码/仓库获取方式**：
- 原文未提供稳定公开代码/仓库链接。

**数据集获取方式**：
- 原文未提供独立 benchmark 下载链接；输入是描述功能、反应和时序属性的自然语言需求。

## 简报

- **输入**：自然语言需求
- **方法**：自动构建 DFRS 中间模型，并提供 symbolic / expanded 两种表示
- **输出**：timed reactive system 模型（DFRS）

```text
自然语言需求 -> DFRS 自动建模 -> symbolic / expanded reactive model
```

一句话结论：这是本轮最贴近“自然语言 -> 状态式行为模型”的经典非 LLM 直接基线之一，而且明确处理时间与反应语义。

## 研究问题与动机

### 问题背景
系统开发早期往往只有自然语言需求，而其中的功能、反应和时间约束容易含糊不清。

### 核心问题
如何从自然语言需求自动得到可分析的定时反应式系统模型。

### 研究动机
在开发早期就把需求变成可检查一致性、完整性和可生成测试的形式化模型。

## 核心方法

### 方法概述
作者提出 Data-Flow Reactive System (DFRS) 模型，并给出从自然语言需求自动得到 symbolic DFRS 与 expanded DFRS 的流程。

### 方法要点
- 直接从自然语言需求出发。
- 兼顾功能、反应和时间属性。
- 模型既可用于一致性/完备性分析，也可用于测试生成。

## 实验与评估

### 数据集
- **数据/案例**：定时反应式系统需求案例
- **来源类型**：文中示例与方法评估

### 主要实验结果
论文表明 DFRS 可自动从自然语言需求获得，并支持 reachability、determinism、completeness 等有界分析。

### 方法的局限性
依赖受控的需求表达与领域假设；输出是 DFRS 而非 UML statechart。

## 与本研究的关系

### 相关性分析
- **BASELINE评估**：🟢
- **评估理由**：输入是自然语言需求，输出是明确的状态式反应模型，任务定义与本研究高度一致。
- **与本研究的主要差异**：模型类型更偏 DFRS/时序数据流反应系统，而不是层次 statechart。

### 可借鉴之处
对时间约束与反应语义的显式建模，对控制系统状态机建模非常重要。

## 文献分类总结

- **类别**：自然语言到定时反应模型直接建模
- **BASELINE评估**：🟢
- **输入**：自然语言需求
- **输出**：DFRS 模型
- **输出模型类型**：Timed reactive system model
- **使用的LLM**：未使用
- **主要方法**：从自然语言需求自动构建 symbolic / expanded DFRS，并支持有界分析。
