# 自然语言需求到系统模型生成基准 / A System Model Generation Benchmark from Natural Language Requirements

## 基本信息

- **标题**：A System Model Generation Benchmark from Natural Language Requirements
- **中文标题**：自然语言需求到系统模型生成基准
- **作者**：Dongming Jin, Zhi Jin, Linyu Li, Zheng Fang, Jia Li, Xiaohong Chen, Yixing Luo
- **单位**：Peking University；Wuhan University；East China Normal University；Beijing Institute of Control Engineering
- **发表**：arXiv preprint, 2025
- **DOI**：原文未提供
- **链接**：https://arxiv.org/abs/2508.03215

**代码/仓库获取方式**：
- 原文说明会发布 SysMBench 与 evaluation framework，但首页未给出明确公开仓库链接。

**数据集获取方式**：
- 原文声称随论文发布 SysMBench 的标注与评估框架；当前 PDF 首页未给出稳定公开入口。

## 简报

这篇论文不是提出新的状态机生成方法，而是把“自然语言需求 -> 系统模型”正式做成 benchmark。作者构建了 151 个人工整理场景，并提出 SysMEval-F1 等评测方法，用于衡量 LLM 生成系统模型的能力。

- **输入**：自然语言 requirements description
- **方法**：人工构建 benchmark + 语法覆盖标注 + 自动/半自动评测框架
- **输出**：带 ground truth 的系统模型 benchmark、评测指标与基线结果

```text
自然语言需求 -> 参考系统模型 -> 统一评测框架 -> 比较不同 prompting / LLM 配置
```

核心价值在于：它把“系统模型生成”从零散案例变成了可复用 benchmark，但其输出工件不专门聚焦状态机。

## 研究问题与动机

### 问题背景

系统模型生成和代码生成不同，受限于专门建模语言语法、公开样本稀缺和领域差异大，导致缺少稳定 benchmark。

### 核心问题

1. 如何构造覆盖广、可评估的 requirements-to-model benchmark。
2. 如何用比 BLEU 更贴合建模任务的方式评价生成质量。
3. 当前 LLM 在该任务上的性能上限有多低。

### 研究动机

作者希望先把“能不能测”这件事做好，再推动系统模型生成方法本身的发展。

## 核心方法

### 方法概述

论文构建 SysMBench：每个样本包含自然语言需求、特定建模语言中的参考模型、语法类别标注和评估接口。随后对 zero-shot、few-shot、CoT、grammar prompting 等设置做基线实验。

### 关键技术

1. **151 个人工整理场景**：覆盖多个工程领域。
2. **语法 taxonomy**：标注系统模型的语言构造覆盖情况。
3. **SysMEval-F1**：比简单 n-gram 相似度更关注建模构造匹配。
4. **多 prompting 基线**：为后续方法提供公共起点。

## 实验与评估

### 数据集

- 共 151 个人工整理样本。
- 覆盖多个系统工程相关领域。
- 同时提供语法构造标签。

### 主要实验结果

1. 现有 LLM 在 SysMBench 上整体表现仍然偏弱。
2. 论文摘要明确给出最好结果仅约 **BLEU 4%**、**SysMEval-F1 62%**。
3. 这说明“自然语言到系统模型”仍远未达到成熟可用水平。

### 方法的局限性

1. 是 benchmark，不是新生成 pipeline。
2. 输出是广义 system model，不是专门的状态机 benchmark。
3. 公开入口在首页未写清，短期复用仍有阻力。

## 与本研究的关系

### 相关性分析

- **BASELINE评估**：🟠
- **原因**：任务与 `project_1` 高度邻近，但论文主要贡献是 benchmark 和评估，而不是控制系统状态机生成方法本身。

### 可借鉴之处

1. 很适合借鉴其 benchmark 设计口径和语法覆盖标注思路。
2. SysMEval-F1 这类结构感知评估指标对状态机也有启发。
3. 可帮助本项目思考“控制系统状态机 benchmark 应该如何构造”。

### 存在的不足与改进空间

1. 缺少状态机工件的单独分析。
2. 领域更泛，未突出控制系统。
3. 目前更偏“评测基础设施”而不是“可比较 baseline”。

### 对本研究的启发

对 `project_1` 来说，这篇论文最重要的价值不是方法，而是 benchmark 组织方式和统一评分视角。

## 重要的相关工作

### 1. 重要的前身类工作

- 原文将既有的 SysML/AADL 等系统建模语言实践视为 system model generation benchmark 的语义来源。

### 2. 直接参与实验的baseline

- 论文直接比较了 zero-shot、few-shot、CoT、grammar prompting 等多种 prompting 设置。

### 3. 提供了重要论证的工作

- 既有代码生成 benchmark 和自动评测研究被用于说明：建模任务也需要统一测试集和结构化指标。

### 4. 在技术上提供了支持的工作

- SysML v2 官方文本语法材料为语法 taxonomy 提供了直接依据。

### 5. 其他重要工作

- 多领域系统工程案例为 benchmark 场景来源提供了题材基础。

## 文献分类总结

- **研究定位**：自然语言到系统模型生成 benchmark
- **任务类型**：数据集/评测集建设
- **输入工件**：自然语言需求描述
- **输出工件**：参考系统模型与评测结果
- **输出模型类型**：广义系统模型
- **使用的LLM**：多种开源 LLM 基线
- **验证方式**：BLEU + SysMEval-F1 + prompting 对比
- **对本研究价值**：为状态机 benchmark 设计和评测指标选择提供直接借鉴
