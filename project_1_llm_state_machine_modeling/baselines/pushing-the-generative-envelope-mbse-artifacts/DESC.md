# 推进生成式边界：MBSE 工件生成中提示技术与温度的影响 / Pushing the (Generative) Envelope: Measuring the Effect of Prompt Technique and Temperature on the Generation of Model-based Systems Engineering Artifacts

## 基本信息

- **标题**：Pushing the (Generative) Envelope: Measuring the Effect of Prompt Technique and Temperature on the Generation of Model-based Systems Engineering Artifacts
- **中文标题**：推进生成式边界：MBSE 工件生成中提示技术与温度的影响
- **作者**：Erin Smith Crabb, Cedric Bernard, Matthew T. Jones, Daniel Dakota
- **单位**：Leidos Holdings, Inc.
- **发表**：Proceedings of Recent Advances in Natural Language Processing, 2025
- **DOI**：10.26615/978-954-452-098-4-137
- **链接**：https://aclanthology.org/2025.ranlp-1.137/

**代码/仓库获取方式**：
- 原文未给出专门公开的实验代码仓库。

**数据集获取方式**：
- 论文使用 air purifier 与 vacuum 两个 MBSE 题项，未提供独立下载页。

## 简报

这篇论文直接研究了 local LLM 生成 MBSE 工件的能力，其中核心输出之一就是 **SysML v2 state machine diagrams**。作者系统比较 zero-shot、one-shot、few-shot、CoT 和不同 temperature 对 state machine 与 requirements list 生成质量的影响。

- **输入**：简短自然语言系统描述或任务说明
- **方法**：local LLM prompting，对 zero/one/few-shot、CoT 和 temperature 进行重复实验
- **输出**：SysML v2 requirements list 与 state machine diagrams

```text
自然语言题项 -> prompt 设计 / temperature 控制 -> local LLM -> SysML v2 需求列表与状态机图
```

结论上，这篇论文虽然不是控制系统专用方法，但属于少数直接碰到“自然语言 -> SysML 状态机图”的 LLM 预印本/作者版工作。

## 研究问题与动机

### 问题背景

MBSE 人工建模成本高，而云端闭源模型在很多工程场景下存在成本、隐私和部署约束，因此 local LLM 是否足以生成初始 MBSE 工件是一个实际问题。

### 核心问题

1. local LLM 是否能生成可用的 SysML v2 工件。
2. prompt technique 对 state machine generation 的影响有多大。
3. temperature 调节是否显著影响工件质量。

### 研究动机

作者希望证明即使较小的本地模型，只要 prompt 设计得当，也能为系统工程师提供可用的初稿。

## 核心方法

### 方法概述

实验围绕两类工件开展：requirements list 与 state machine diagrams。使用 Mixtral-8x7B-Instruct-v0.1 和 Llama-3-Smaug-8B，对 vacuum 与 air purifier 两个题项在多种 prompt / temperature 配置下重复运行 100 次，并用 METEOR 与 SME 反馈分析结果。

### 关键技术

1. **多 prompt 策略**：zero-shot、one-shot、few-shot、CoT。
2. **多温度设置**：0.2、0.6、0.95。
3. **工件级评价**：分别看 requirements list 和 state machine diagrams。
4. **dot notation 对比**：减少 SysML v2 语法细节对内容评分的干扰。

## 实验与评估

### 数据集

- 两个示例题项：air purifier、vacuum。
- 每种设置重复 100 次生成。

### 主要实验结果

1. one-shot 对 requirements list 效果普遍更稳定。
2. 对 state machine diagrams，air purifier 与 vacuum 的收益并不一致，说明任务和领域差异明显。
3. temperature 对结果影响小于 prompt technique。
4. CoT 在部分 state machine 场景下有帮助，但不能保证稳定提升。

### 方法的局限性

1. 题项规模较小，更像 proof-of-concept。
2. 不是面向控制系统语义的专门 benchmark。
3. 质量评价仍较依赖文本相似度而不是形式化语义。

## 与本研究的关系

### 相关性分析

- **BASELINE评估**：🟢
- **原因**：论文明确包含从自然语言描述生成 SysML v2 state machine diagrams 的实验，任务定义与 `project_1` 的“自然语言到状态机”主线直接相邻，尽管场景较小、工件较简化。

### 可借鉴之处

1. 证明了 local LLM 也能承担状态机初稿生成任务。
2. prompt technique 对状态机生成质量的影响大于 temperature，这一点很实用。
3. 可以把其工件级比较方式直接迁移到本项目实验设计。

### 存在的不足与改进空间

1. 缺少控制系统和工业复杂需求。
2. 没有反馈修复或形式化验证闭环。
3. 评测仍偏文本相似度，不够状态机语义化。

### 对本研究的启发

本项目可以把它视作“轻量自然语言到 SysML 状态机图”的可比 baseline，同时在复杂需求、验证闭环和控制语义上继续拉开差异。

## 重要的相关工作

### 1. 重要的前身类工作

- 原文把既有 ChatGPT/LLM 辅助 MBSE 建模工作作为直接背景，说明大模型已开始进入 SysML 工件生成。

### 2. 直接参与实验的baseline

- 论文直接比较 zero-shot、one-shot、few-shot 与 CoT，不依赖外部算法基线。

### 3. 提供了重要论证的工作

- MBSE 人工建模成本与 local model 部署需求构成了研究必要性的主要论证。

### 4. 在技术上提供了支持的工作

- SysML v2 文本表示与 METEOR 相似度评估是实验基础。

### 5. 其他重要工作

- 论文也引用了更早的 TTool-AI 和泛 MBSE+LLM 研究，表明状态机生成还处于早期阶段。

## 文献分类总结

- **研究定位**：直接自然语言到 MBSE 工件生成
- **任务类型**：直接生成
- **输入工件**：自然语言系统描述
- **输出工件**：requirements list + state machine diagrams
- **输出模型类型**：SysML v2 state machine
- **使用的LLM**：Mixtral-8x7B-Instruct、Llama-3-Smaug-8B
- **验证方式**：100 次重复实验 + METEOR + prompt/temperature 对比
- **对本研究价值**：是少数可直接纳入“LLM 自然语言到状态机图”比较表的新预印本/作者版条目
