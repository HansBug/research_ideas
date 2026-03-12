# NOMAD：从自然语言需求生成 UML 类图的多智能体系统 / NOMAD: A Multi-Agent LLM System for UML Class Diagram Generation from Natural Language Requirements

## 基本信息

- **标题**：NOMAD: A Multi-Agent LLM System for UML Class Diagram Generation from Natural Language Requirements
- **中文标题**：NOMAD：从自然语言需求生成 UML 类图的多智能体系统
- **作者**：Polydoros Giannouris, Sophia Ananiadou
- **单位**：The University of Manchester
- **发表**：arXiv preprint, 2025
- **DOI**：原文未提供
- **链接**：https://arxiv.org/abs/2511.22409

**代码/仓库获取方式**：
- 原文首页未给出专门仓库链接。

**数据集获取方式**：
- 论文使用 Northwind 深入案例与 human-validated class diagram benchmark，首页未提供统一下载地址。

## 简报

NOMAD 把 UML 类图生成拆成多个 role-specialised agents，分别负责实体抽取、关系分类、图综合等，从而提升相较单代理 prompting 的可解释性和效果。

- **输入**：自然语言需求
- **方法**：多智能体 LLM 分解式建模
- **输出**：UML class diagram

```text
需求文本 -> 实体抽取 agent -> 关系分类 agent -> 图综合 agent -> UML 类图
```

它不是状态机论文，但很好地说明了“把建模任务拆开做”对 LLM 工程化很重要。

## 研究问题与动机

### 问题背景

单代理 LLM 生成 UML 图时往往把识别实体、识别关系、保持图一致性混在一起，导致错误模式复杂且难以修复。

### 核心问题

1. 多智能体拆分是否优于直接 prompting。
2. 这种拆分能否提升可解释性和 targeted verification 的可能性。
3. LLM 在类图语义上究竟卡在哪里。

### 研究动机

作者试图借鉴人类工程师的目标分解过程，把 UML 生成过程模块化。

## 核心方法

### 方法概述

NOMAD 用多个 agent 分别处理实体、属性、关系与图综合，并在 Northwind 案例和 benchmark 上与 GPT-4o 直接 prompting 作比较。

### 关键技术

1. **role-specialised agents**。
2. **分阶段验证**：允许按模块定位错误。
3. **混合评测**：深入案例 + benchmark。

## 实验与评估

### 数据集

- Northwind 大案例用于错误分析。
- 另有人工验证的 requirements-to-class-diagram benchmark。

### 主要实验结果

1. NOMAD 在 attribute 和 relationship 质量上优于直接 prompting。
2. 对 GPT-4o 与 DeepSeek-V3 都有提升，但提升幅度因子任务而异。
3. 论文强调 structural accuracy 已较强，真正难点仍在语义一致性。

### 方法的局限性

1. 输出是类图而非状态机。
2. 多智能体管线更复杂，成本更高。
3. benchmark 与控制系统无直接对齐。

## 与本研究的关系

### 相关性分析

- **BASELINE评估**：🟠
- **原因**：输入是自然语言需求，但输出是 UML 类图，不能直接算状态机 baseline；其价值更多在 pipeline 分解方法。

### 可借鉴之处

1. 多 agent 分解非常适合迁移到“状态/事件/迁移/守卫”分工生成。
2. targeted verification 的思路可直接用于状态机元素级修复。
3. 说明“直接 prompting”在复杂建模任务上很快碰到天花板。

### 存在的不足与改进空间

1. 没有行为语义。
2. 缺少控制系统要求与形式化验证。
3. 与状态机的直接可比性有限。

### 对本研究的启发

NOMAD 对 `project_1` 最有价值的不是输出工件，而是任务分解视角。

## 重要的相关工作

### 1. 重要的前身类工作

- 原文把 GPT-3.5 / GPT-4 的 UML 生成研究和 Ferrari 等需求到图工作视为直接前身。

### 2. 直接参与实验的baseline

- 直接 baseline 是 GPT-4o 的 direct prompting，以及对 DeepSeek-V3 的相同对照。

### 3. 提供了重要论证的工作

- 既有研究中“语法还行、语义偏弱”的观察，为 NOMAD 的多阶段设计提供了论证。

### 4. 在技术上提供了支持的工作

- PlantUML、分阶段评估和 Northwind 案例构成技术与实验支撑。

### 5. 其他重要工作

- 论文强调类图 benchmark 的 human validation，这对后续状态机 benchmark 设计也有启发。

## 文献分类总结

- **研究定位**：自然语言到 UML 类图的多智能体生成
- **任务类型**：直接生成
- **输入工件**：自然语言需求
- **输出工件**：UML 类图
- **输出模型类型**：UML class diagram
- **使用的LLM**：GPT-4o、DeepSeek-V3
- **验证方式**：Northwind 案例 + benchmark 对照
- **对本研究价值**：可借鉴其 agent 分解和 targeted verification 思路
