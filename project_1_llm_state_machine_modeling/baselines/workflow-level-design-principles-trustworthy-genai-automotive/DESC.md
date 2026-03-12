# 面向可信生成式 AI 的汽车系统工程工作流级设计原则 / Workflow-Level Design Principles for Trustworthy GenAI in Automotive System Engineering

## 基本信息

- **标题**：Workflow-Level Design Principles for Trustworthy GenAI in Automotive System Engineering
- **中文标题**：面向可信生成式 AI 的汽车系统工程工作流级设计原则
- **作者**：Chih-Hong Cheng, Brian Hsuan-Cheng Liao, Adam Molin, Hasan Esen
- **单位**：Carl von Ossietzky University of Oldenburg；DENSO AUTOMOTIVE Deutschland
- **发表**：arXiv preprint, 2026
- **DOI**：原文未提供
- **链接**：https://arxiv.org/abs/2602.19614

**代码/仓库获取方式**：
- 原文未提供公开代码或实验仓库链接。

**数据集获取方式**：
- 原文案例建立在公司内部汽车规格、既有 SysML v2 工件和验证资产之上，未提供公开下载链接。

## 简报

论文讨论的不是“让 LLM 一次性生成完整模型”，而是如何把 GenAI 纳入安全关键汽车系统工程流程，并用可追溯、可验证的方式控制风险。作者把任务拆成 requirement delta 识别、SysML v2 架构更新、编译与静态分析、回归测试追踪四段，强调工作流分解优于 big-bang prompting。

- **输入**：大型需求规格中的变更片段、既有 SysML v2 架构工件、既有验证/测试资产
- **方法**：section-wise decomposition + diversity sampling + 轻量 NLP sanity checks + SysML v2 编译与静态分析
- **输出**：更新后的 SysML v2 架构工件、重新追踪的回归测试与验证工件

```text
需求变更 -> 分段识别 delta -> LLM 更新 SysML v2 工件 -> 编译/静态分析 -> 回归测试追踪
```

一句话判断：这是很强的“可信 MBSE 工作流”论文，但不是直接从自然语言端到端生成状态机的论文。

## 研究问题与动机

### 问题背景

汽车系统规格通常篇幅长、变化频繁，而且必须与既有模型、验证和回归测试保持一致。单次大 prompt 往往会遗漏关键变更，难以满足安全关键工程要求。

### 核心问题

1. 如何在大规格文本中更可靠地发现 requirement delta。
2. 如何把这些 delta 稳定传播到 SysML v2 架构与验证工件。
3. 如何通过编译、静态分析和回归测试保持流程可信。

### 研究动机

作者的核心动机是减少“LLM 直接生成看起来对、但工程上不可追溯”的风险，把 LLM 约束在可验证的工作流环节内。

## 核心方法

### 方法概述

方法将 end-to-end 生成拆成多个较小步骤：先按章节和变化点定位 requirement delta，再对模型更新做多样化采样与 sanity checks，最后将结果送入 SysML v2 编译和静态分析。

### 关键技术

1. **分段式 prompting**：避免一次性处理 100+ 页规格带来的遗漏。
2. **多样化采样**：通过多个候选响应覆盖潜在变更。
3. **轻量 NLP 检查**：先做低成本 sanity checks，再进入更昂贵的模型更新。
4. **工具链校验**：对生成后的 SysML v2 工件做编译和静态分析。
5. **测试可追溯性**：把 requirement delta 回写到 regression test selection。

## 实验与评估

### 数据集

- 以一个端到端汽车系统工程流程为主案例。
- 输入包含大型真实规格文本、既有 SysML v2 架构和验证资产。

### 主要实验结果

1. monolithic prompting 在大规格文本下更容易遗漏关键变化。
2. section-wise decomposition 配合 diversity sampling 与 sanity checks 能提升 completeness 和 correctness。
3. 更新后的模型能够继续通过编译和静态分析，说明流程层面的可验证性更强。

### 方法的局限性

1. 工业案例与验证资产未公开，复现实验门槛高。
2. 重点在工作流可信性，不是专门优化状态机生成质量。
3. 更偏“需求变更传播”而非“从零建模”。

## 与本研究的关系

### 相关性分析

- **BASELINE评估**：🟡
- **原因**：输入仍然是自然语言需求变化，输出落到 SysML v2 工件更新与验证，但任务本质是增量传播和工作流编排，不是从自然语言直接生成状态机。

### 可借鉴之处

1. 很适合作为 `project_1` 后续“生成-验证-修复”闭环的工程工作流参照。
2. 其“先识别 delta，再更新模型，再回归测试”的结构可迁移到控制系统状态机维护。
3. 强调了安全关键场景下 prompt 分解和工具校验的重要性。

### 存在的不足与改进空间

1. 没有把状态机作为核心输出工件单独评测。
2. 没有形成公开 benchmark。
3. 对控制系统自然语言到状态机的直接比较价值有限。

### 对本研究的启发

`project_1` 可以借鉴其“工作流拆分 + 工具校验 + 可追溯回写”的理念，把状态机生成步骤嵌入更完整的工程闭环。

## 重要的相关工作

### 1. 重要的前身类工作

- 原文把 Reflexion / self-debugging 一类 LLM 自反馈工作作为通用前身，用于说明为何安全关键工程不应依赖一次性 prompting。

### 2. 直接参与实验的baseline

- 直接对比的是 monolithic prompting 与 section-wise workflow，而不是外部状态机 baseline。

### 3. 提供了重要论证的工作

- 原文借助安全关键系统工程与需求变更传播相关工作论证：可信性、可追溯性和验证闭环比“生成得快”更重要。

### 4. 在技术上提供了支持的工作

- SysML v2 官方工件、编译与静态分析工具链构成了该方法的关键基础设施。

### 5. 其他重要工作

- 论文还引用了 PDF 解析与文档处理工具作为 requirements delta 抽取链路的支撑组件。

## 文献分类总结

- **研究定位**：LLM 参与的 MBSE 增量建模与验证工作流
- **任务类型**：需求变更传播 / 模型更新 / 回归测试追踪
- **输入工件**：自然语言需求变化 + 既有 SysML v2 工件
- **输出工件**：更新后的 SysML v2 架构与验证工件
- **输出模型类型**：SysML v2 架构模型
- **使用的LLM**：Qwen3、Nemotron3、GPT-OSS 等开源模型
- **验证方式**：sanity checks + 编译 + 静态分析 + regression traceability
- **对本研究价值**：适合作为“生成后如何做可信传播与验证”的工作流参照
