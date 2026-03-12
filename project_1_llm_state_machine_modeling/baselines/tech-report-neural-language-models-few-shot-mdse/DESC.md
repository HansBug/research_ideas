# 面向 MDSE 系统化需求处理的神经语言模型与 Few-Shot 学习技术报告 / Technical Report on Neural Language Models and Few-Shot Learning for Systematic Requirements Processing in MDSE

## 基本信息

- **标题**：Technical Report on Neural Language Models and Few-Shot Learning for Systematic Requirements Processing in MDSE
- **中文标题**：面向 MDSE 系统化需求处理的神经语言模型与 Few-Shot 学习技术报告
- **作者**：Vincent Bertram, Miriam Boß, Evgeny Kusmenko, Imke Helene Nachmann, Bernhard Rumpe, Danilo Trotta, Louis Wachtmeister
- **单位**：RWTH Aachen University
- **发表**：arXiv
- **年份**：2022
- **DOI**：原文未标明 / 当前条目按公开版本整理
- **链接**：https://arxiv.org/abs/2211.09084

**代码/仓库获取方式**：
- 原文未提供公开代码/仓库获取链接。

**数据集获取方式**：
- 基于开源汽车需求集做 few-shot 翻译实验，但第一页未给出统一下载链接。

## 简报

本文关注的问题是：如何利用预训练语言模型与 few-shot learning 把非正式汽车需求翻译到结构化 requirement DSL，以支撑 MDSE 自动处理。

- **输入**：非正式汽车需求文本
- **方法**：先分析需求语料并提炼 DSL 构造，再用 few-shot prompting 驱动预训练语言模型做 requirements-to-DSL 翻译。
- **输出**：结构化 requirement DSL

```text
非正式需求 -> DSL 构造归纳 -> few-shot LLM 翻译 -> requirement DSL
```

一句话结论：说明 LLM 类模型在 requirements formalization 上已有可用潜力，可作为状态机生成前的中间结构层。

## 研究问题与动机

### 问题背景
如何利用预训练语言模型与 few-shot learning 把非正式汽车需求翻译到结构化 requirement DSL，以支撑 MDSE 自动处理。

### 核心问题
作者试图回答：在给定 非正式汽车需求文本 的前提下，怎样更稳定地得到 结构化 requirement DSL，或至少把需求加工为更接近该目标的形式化中间层。

### 研究动机
核心动机是减少需求到行为设计之间的人工鸿沟，提高可追溯性、一致性以及后续验证/执行的可行性。

## 核心方法

### 方法概述
先分析需求语料并提炼 DSL 构造，再用 few-shot prompting 驱动预训练语言模型做 requirements-to-DSL 翻译。

### 方法要点
- 任务入口：非正式汽车需求文本
- 关键处理：从汽车需求到 requirement DSL 的 few-shot 翻译。
- 最终产物：结构化 requirement DSL（Requirement DSL）
- 使用的LLM：预训练语言模型（few-shot）

## 实验与评估

### 数据集
- **数据/案例**：开源汽车需求集
- **来源类型**：开源需求语料
- **制作方法**：作者在其上提炼 DSL 构造并做 few-shot 评估
- **规模**：原文首页未明确

### 实验设置
在开源汽车需求集上评估从自然语言需求到结构化 DSL 的 few-shot 翻译可行性。

### 主要实验结果
说明 LLM 类模型在 requirements formalization 上已有可用潜力，可作为状态机生成前的中间结构层。

### 方法的局限性
输出不是状态机；更像 requirements formalization 的前置工作。

## 与本研究的关系

### 相关性分析
- **BASELINE评估**：🟠
- **评估理由**：任务与需求结构化高度相关，但输出不是状态机模型，只能作为前序支撑线索。
- **与本研究的主要差异**：本课题强调“控制系统自然语言描述/设计/需求 -> 状态机模型”；而该文的输入、输出或自动化阶段与此存在不同程度偏移。

### 可借鉴之处
本研究可直接借鉴“先译到 DSL，再生成行为模型”的两段式路线。

### 存在的不足与改进空间
若把 DSL 明确设计成状态机导向的事件/状态/守卫片段，相关性会进一步提高。

### 对本研究的启发
该文可以作为 `需求形式化` 方向的参照：要么提供直接任务对齐的经典前身，要么提供需求形式化、状态抽取、调试闭环或执行化方面的可复用模块。

## 重要的相关工作

### 1. 重要的前身类工作
- 原文处在 automotive requirements、MDSE 和 LLM few-shot 翻译语境，偏 requirements formalization。

### 2. 直接参与实验的baseline
- 原文大多未设置与 LLM 状态机生成工作的直接公平对比；若有实验，重点也通常在自身流程可行性或案例验证，而非统一 benchmark 对抗。

### 3. 提供了重要论证的工作
- 论文用需求工程、形式化方法、UML/Statecharts/RSML-e/时序逻辑等既有脉络来论证：从需求到行为模型需要中间层、约束层和验证层，而不能只靠手工直觉。

### 4. 在技术上提供了支持的工作
- 原文所依赖的支持技术通常包括时序逻辑、状态机/Statecharts、需求模式、MBSE 工具链、仿真或可执行规格环境。

### 5. 其他重要工作
- 若后续需要把该文用于正式论文写作，建议再回到其参考文献补抽与“需求到状态机建模”最直接的题名级相关工作，补充到横向比较表中。

## 文献分类总结

- **类别**：需求形式化
- **BASELINE评估**：🟠
- **输入**：非正式汽车需求文本
- **输出**：结构化 requirement DSL
- **输出模型类型**：Requirement DSL
- **使用的LLM**：预训练语言模型（few-shot）
- **主要方法**：从汽车需求到 requirement DSL 的 few-shot 翻译。
