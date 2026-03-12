# 面向可靠需求验证的推理时干预 / Inference-Time Intervention in Large Language Models for Reliable Requirement Verification

## 基本信息

- **标题**：Inference-Time Intervention in Large Language Models for Reliable Requirement Verification
- **中文标题**：面向可靠需求验证的推理时干预
- **作者**：Paul Darma, James Xie, Annalisa Riccardi
- **单位**：University of Strathclyde；International Space University
- **发表**：arXiv preprint, 2025
- **DOI**：原文未提供
- **链接**：https://arxiv.org/abs/2503.14130

**代码/仓库获取方式**：
- 原文未提供公开代码仓库链接。

**数据集获取方式**：
- 使用两个早期 Capella/SysML 空间任务模型与其需求；未提供公开下载入口。

## 简报

这篇论文关注的是 requirement verification，不是模型生成。作者把 Capella/SysML 模型转成图表示，再对 Llama-3.1-8B 做 inference-time intervention，试图把“需求是否被模型满足”的判断过程做得更稳定。

- **输入**：需求文本 + Capella/SysML 模型图表示
- **方法**：针对少量 attention heads 做 intervention，并结合 self-consistency
- **输出**：需求满足性判断结果

```text
需求 + SysML/Capella 图 -> ITI 干预后的 LLM 推理 -> fulfilled / not fulfilled 判断
```

它不是 baseline 本体，但对“生成后如何验证”有明确参考价值。

## 研究问题与动机

### 问题背景

在工程场景里，仅靠 prompt engineering 或 fine-tuning 很难得到足够稳定、可控的 requirement verification 行为。

### 核心问题

1. 是否能通过 inference-time intervention 细粒度控制 LLM 的验证行为。
2. 这种控制能否优于普通基线和 fine-tuning。
3. 在 MBSE 需求验证任务上能否获得足够高的 precision。

### 研究动机

作者希望把 LLM 从“会说但不稳”的助手，变成在工程判断任务上可调、可控、可验证的推理模块。

## 核心方法

### 方法概述

方法首先把 Capella/SysML 模型编码为图，再让 Llama-3.1-8B 回答 requirement fulfillment 问题。随后通过识别并干预 1-3 个 specialised attention heads 调整模型行为，并以 self-consistency 增强稳定性。

### 关键技术

1. **graph-based reasoning input**：让模型在结构化模型表示上推理。
2. **Inference-Time Intervention**：不重训模型，只在推理时改动少量 heads。
3. **self-consistency**：降低偶然错误。
4. **精度导向评测**：强调工程判断中的 precision。

## 实验与评估

### 数据集

- 两个早期 Capella/SysML 空间任务模型。
- 文摘提到 holdout set 达到 perfect precision。

### 主要实验结果

1. 相比基线模型和 fine-tuning，ITI 明显提升 requirement verification 的可靠性。
2. 只需修改 1-3 个 attention heads 就能显著改变模型行为。
3. 结合 self-consistency 后，在 holdout set 上达到 **perfect precision**。

### 方法的局限性

1. 任务是验证，不是生成。
2. 案例规模较小，主要是空间任务早期模型。
3. 与状态机建模的直接可比性有限。

## 与本研究的关系

### 相关性分析

- **BASELINE评估**：🟠
- **原因**：论文不生成状态机，而是验证需求是否被 MBSE 模型满足；对 `project_1` 的价值主要在后验验证环节。

### 可借鉴之处

1. 对“生成后验证”阶段非常有启发。
2. 显示出结构化模型表示 + LLM 校验比自由文本问答更可靠。
3. 可用于思考状态机生成后的 requirement satisfaction checking。

### 存在的不足与改进空间

1. 不涉及状态机生成。
2. 没有与形式化模型检查深度结合。
3. 数据和模型公开性有限。

### 对本研究的启发

`project_1` 若要做生成-验证-修复闭环，可以考虑类似的“对齐 LLM 验证器”思路，而不只关注生成器。

## 重要的相关工作

### 1. 重要的前身类工作

- 原文把 activation steering / representation engineering 一类 ITI 工作视为直接方法前身。

### 2. 直接参与实验的baseline

- 直接对比对象是未经干预的 baseline 模型和 fine-tuning 方案。

### 3. 提供了重要论证的工作

- MBSE requirement verification 的高精度需求，为该研究提供了问题动机。

### 4. 在技术上提供了支持的工作

- 图表示推理、self-consistency 和 attention head intervention 是核心技术支撑。

### 5. 其他重要工作

- Claude 3.5 被用于交叉核对人工标注，提高了实验标签可靠性。

## 文献分类总结

- **研究定位**：MBSE 需求验证邻近工作
- **任务类型**：验证 / 判断
- **输入工件**：需求文本 + Capella/SysML 模型图
- **输出工件**：需求满足性判断
- **输出模型类型**：验证结论
- **使用的LLM**：Llama-3.1-8B（主模型），Claude-3.5（标注交叉核对）
- **验证方式**：ITI 干预对比 + self-consistency + holdout precision
- **对本研究价值**：为状态机生成后的自动验证器设计提供思路
