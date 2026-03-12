# MCeT：利用大语言模型进行行为模型正确性评估 / MCeT: Behavioral Model Correctness Evaluation using Large Language Models

## 基本信息

- **标题**：MCeT: Behavioral Model Correctness Evaluation using Large Language Models
- **中文标题**：MCeT：利用大语言模型进行行为模型正确性评估
- **作者**：Khaled Ahmed, Jialing Song, Boqi Chen, Ou Wei, Bingzhou Zheng
- **单位**：Huawei Research Canada；McGill University
- **发表**：arXiv preprint, 2025
- **DOI**：原文未提供
- **链接**：https://arxiv.org/abs/2508.00630

**代码/仓库获取方式**：
- 论文明确提供公开仓库：https://github.com/Huawei-TTE/MCeT

**数据集获取方式**：
- 原文说明 implementation、prompts 和 evaluation dataset 均在线公开，入口同上。

## 简报

MCeT 做的是“自动发现 sequence diagram 与需求之间的错位问题”，不负责生成图，而负责检查图。论文把这类工作做成了公开工具与数据集。

- **输入**：需求文本 + sequence diagrams
- **方法**：多检查器 + self-consistency + issue aggregation
- **输出**：自然语言问题报告

```text
需求 + 顺序图 -> 多视角检查 -> issue 合并与过滤 -> 错误报告
```

它对状态机任务的价值在于“生成后怎么自动查错”。

## 研究问题与动机

### 问题背景

行为模型图即使由经验工程师手工绘制，也常与需求不完全对齐；而 LLM 生成后这种问题只会更多，因此需要自动 correctness evaluator。

### 核心问题

1. 能否自动发现 sequence diagram 与需求不一致的问题。
2. LLM-as-a-judge 如何避免只给出高幻觉率的泛化点评。
3. 多检查器组合能否比直接整体判别更可靠。

### 研究动机

作者希望提供一个真正可放进建模流程的自动审查器，而不是只做人工评阅。

## 核心方法

### 方法概述

MCeT 将需求拆成 requirement atoms，再让不同检查器分别比对顺序图，最后通过 self-consistency 和 issue aggregation 汇总结果。

### 关键技术

1. **atom-based checking**：避免整体判断过于粗糙。
2. **多检查器互补**：降低单一判断器的幻觉。
3. **公开工具化实现**：可直接复用。

## 实验与评估

### 数据集

- 基于真实 requirements 与 sequence diagrams。
- 论文提到一组 **16** 张图中含 **27** 个人工标注问题，同时在完整 FBENCH 上做评估。

### 主要实验结果

1. 直接方法 precision 约 **0.58**，MCeT 提升到 **0.81**。
2. 能发现约 **65%** 的人工报告问题，比对照高约 **90%**。
3. 平均每张图还能报告约 **6** 个额外问题。

### 方法的局限性

1. 输出仍是问题报告，不是状态机。
2. 任务聚焦顺序图。
3. 最终 issue 质量仍依赖底层 LLM。

## 与本研究的关系

### 相关性分析

- **BASELINE评估**：🟠
- **原因**：这是行为模型评估器，不是状态机生成器；但对生成后自动审查很有参考价值。

### 可借鉴之处

1. requirement atoms 的思想可迁移到状态/迁移/守卫检查。
2. “多检查器 + 聚合”很适合状态机语义评审。
3. 公开代码和数据集可直接复用其评估范式。

### 存在的不足与改进空间

1. 没有处理状态机特有语义。
2. 以顺序图为主，不是控制系统模型。
3. 更像后处理模块而非 baseline。

### 对本研究的启发

`project_1` 后续若要补“验证器”或“修复器”，MCeT 是非常值得参考的邻近工作。

## 重要的相关工作

### 1. 重要的前身类工作

- 原文把直接整体评判 sequence diagram 的做法视为前身，但指出其 recall 和 precision 都不理想。

### 2. 直接参与实验的baseline

- 直接 baseline 是 holistic checking，以及不同底层 LLM 的 MCeT 变体。

### 3. 提供了重要论证的工作

- 行为模型与需求错位会在实际工程中频繁发生，这一观察构成研究动机。

### 4. 在技术上提供了支持的工作

- requirement atoms、self-consistency 和 FBENCH 数据集构成关键技术支撑。

### 5. 其他重要工作

- 论文公开的 prompts 和工具使其具备较高复现价值。

## 文献分类总结

- **研究定位**：行为模型自动评估工具
- **任务类型**：验证 / 问题报告生成
- **输入工件**：需求文本 + 顺序图
- **输出工件**：issue 报告
- **输出模型类型**：sequence diagram correctness evaluation
- **使用的LLM**：GPT-4o-mini、GPT-4o、DeepSeek-v3、DeepSeek-R1
- **验证方式**：precision / recall / human-reported issue 对照
- **对本研究价值**：可直接借鉴其生成后自动检查思路
