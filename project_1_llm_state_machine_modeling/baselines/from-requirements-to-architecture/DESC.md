# 从需求到架构：基于 AI 的半自动软件架构生成 / From Requirements to Architecture: An AI-Based Journey to Semi-Automatically Generate Software Architectures

## 基本信息

- **标题**：From Requirements to Architecture: An AI-Based Journey to Semi-Automatically Generate Software Architectures
- **中文标题**：从需求到架构：基于 AI 的半自动软件架构生成
- **作者**：Tobias Eisenreich, Sandro Speth, Stefan Wagner
- **单位**：University of Stuttgart
- **发表**：arXiv preprint, 2024
- **DOI**：原文未提供
- **链接**：https://arxiv.org/abs/2401.14079

**代码/仓库获取方式**：
- 论文给出探索性 GitHub 分支：https://github.com/qw3ry/requirements2architecture/tree/exploration

**数据集获取方式**：
- 论文使用 MobSTr dataset 中的 91 条需求做初步探索；文中给出数据集 DOI 线索，但不是本方法专有数据集。

## 简报

这是一篇 vision-style 论文，目标是把 requirements、domain model、use case scenarios 和 architecture candidate generation 串成一个半自动流程。它不做状态机，但在“自然语言需求逐步传播到更高阶设计工件”这条线上很有代表性。

- **输入**：requirements、domain model、use case scenarios
- **方法**：多阶段 AI 辅助，从需求分析逐步生成 architecture candidates
- **输出**：软件架构候选

```text
需求 -> 领域模型 / 用例场景 -> 架构候选生成 -> 人工比较与筛选
```

其价值在于说明：很多预印本把终点放在架构而不是行为状态机。

## 研究问题与动机

### 问题背景

软件架构生成高度依赖专家经验，时间成本高，而且往往只探索有限方案空间。

### 核心问题

1. 能否用 AI 半自动生成多个架构候选。
2. 如何把需求、领域模型和场景逐步传播到架构。
3. 人工评审如何嵌入该流程。

### 研究动机

作者希望把需求分析与架构设计之间的人工鸿沟缩短，让工程师可以比较多个候选而不是只画一个方案。

## 核心方法

### 方法概述

论文提出多阶段流程：先从需求生成领域模型和用例场景，再进一步生成架构候选，最后由人工评估和运行时比较。

### 关键技术

1. **分层传播**：requirements -> domain/use case -> architecture。
2. **候选生成**：不只输出一个解。
3. **半自动而非全自动**：强调人类评估保留在环。

## 实验与评估

### 数据集

- 论文在探索性分析中使用 **MobSTr dataset 的 91 条需求**。

### 主要实验结果

1. LLaMA 的初步实验显示有一定可行性。
2. 论文更强调流程设计与研究议程，而非成熟 quantitative 结果。
3. 作者认为候选式生成比单一输出更适合架构设计。

### 方法的局限性

1. 是 vision paper，实证不重。
2. 输出不是状态机。
3. 对控制系统行为建模没有直接支持。

## 与本研究的关系

### 相关性分析

- **BASELINE评估**：🟠
- **原因**：输入与本项目相似，但终点是 architecture candidates，不是状态机模型。

### 可借鉴之处

1. 候选式生成思路可迁移到状态机多候选采样。
2. 其分层传播结构适合借鉴到需求 -> 场景 -> 状态机 pipeline。
3. 强调人工筛选在高层设计中不可缺失。

### 存在的不足与改进空间

1. 缺少行为模型落点。
2. 实验仍偏探索性。
3. 没有验证闭环。

### 对本研究的启发

如果本项目未来考虑“多候选状态机生成与重排”，这篇论文的候选生成思路值得参考。

## 重要的相关工作

### 1. 重要的前身类工作

- 原文承接 requirements-to-domain-model 和软件架构自动化研究。

### 2. 直接参与实验的baseline

- 论文没有形成严格外部 baseline 表，更多是 vision-driven exploratory analysis。

### 3. 提供了重要论证的工作

- 架构设计高度依赖人工经验、候选探索不足，是论文的主要论证基础。

### 4. 在技术上提供了支持的工作

- MobSTr dataset、LLaMA 初步实验与 GitHub 分支为方法探索提供了支撑。

### 5. 其他重要工作

- 论文把 domain model 和 use case scenario 作为中间工件，这对后续状态机场景分解有启发。

## 文献分类总结

- **研究定位**：需求到架构的 AI 辅助设计
- **任务类型**：分阶段候选生成
- **输入工件**：requirements + domain/use case 中间工件
- **输出工件**：architecture candidates
- **输出模型类型**：软件架构
- **使用的LLM**：LLaMA（探索性分析）
- **验证方式**：vision 流程 + exploratory analysis
- **对本研究价值**：说明很多预印本仍停留在架构而非状态机层
