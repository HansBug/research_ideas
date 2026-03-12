# 超越场景：从用例生成状态模型 / Beyond Scenarios: Generating State Models from Use Cases

## 基本信息

- **标题**：Beyond Scenarios: Generating State Models from Use Cases
- **中文标题**：超越场景：从用例生成状态模型
- **作者**：Stéphane S. Somé
- **单位**：University of Ottawa
- **发表**：ICSE 2002 Workshop on Scenarios and State Machines
- **年份**：2002
- **DOI**：原文未提供
- **链接**：https://www.site.uottawa.ca/~ssome/UCEdWeb/publis/ICSE02_Scenario_Workshop.pdf

**代码/仓库获取方式**：
- 原文未提供公开代码/仓库获取链接。

**数据集获取方式**：
- 原文未提供统一 benchmark；输入是 use case 规格。

## 简报

本文直接研究如何从 use cases 生成状态模型，是本轮补充里与 `project_1` 任务定义最接近的经典前身之一。

- **输入**：use case 规格
- **方法**：围绕 use case 的系统化转换规则生成 state models
- **输出**：state models

```text
use case 规格 -> 规则化转换 -> state models
```

一句话结论：它虽然仍然依赖结构化 use case，而非自由自然语言长文，但已经非常接近“需求文本到状态模型”的直接 baseline。

## 研究问题与动机

### 问题背景
场景和 use case 常被用于需求获取，但系统设计更需要全局状态模型。

### 核心问题
如何从 use cases 中抽取足够的行为信息，自动生成更完整的状态模型。

### 研究动机
把需求级 use case 更直接地连接到可分析、可设计的行为模型。

## 核心方法

### 方法概述
作者提出从 use case 出发构建 state model 的方法，不再停留在场景描述层。

### 方法要点
- 以 use case 为直接输入。
- 目标产物是状态模型，而不是单纯 sequence-like 轨迹。
- 属于经典 rule-based / model-driven 路线。

## 实验与评估

### 数据集
- **数据/案例**：use case 案例
- **来源类型**：说明性案例

### 主要实验结果
方法展示了从 use cases 自动生成状态模型的可行性，说明需求级工件可以直接驱动行为建模。

### 方法的局限性
对自由自然语言的覆盖仍有限；需要 use case 规格满足较强的结构化约束。

## 与本研究的关系

### 相关性分析
- **BASELINE评估**：🟢
- **评估理由**：输入仍属于需求级文本工件，输出是状态模型，任务定义与本研究高度贴近。
- **与本研究的主要差异**：该文依赖 use case 规格这一较结构化入口；本研究希望更直接处理控制系统自然语言描述/需求。

### 可借鉴之处
其最有价值的地方是把“用例文本 -> 状态模型”明确成一条独立 pipeline，而不是附属步骤。

### 对本研究的启发
当控制系统需求能被标准化为 use case 或事件-响应模板时，这类经典方法能提供很强的前身基线。

## 重要的相关工作

### 1. 重要的前身类工作
- use case / scenario 驱动需求工程是本文的直接背景。

### 2. 提供了重要论证的工作
- 论文支持了“需求级工件足以驱动状态模型生成”的观点。

### 3. 在技术上提供了支持的工作
- 基于规则的 use case 转换与状态模型构建是主要技术核心。

## 文献分类总结

- **类别**：用例到状态模型直接建模
- **BASELINE评估**：🟢
- **输入**：use case 规格
- **输出**：state models
- **输出模型类型**：State model
- **使用的LLM**：未使用
- **主要方法**：对 use case 规格应用规则化转换，自动生成状态模型。
