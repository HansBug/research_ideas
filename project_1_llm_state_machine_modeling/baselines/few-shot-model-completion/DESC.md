# 基于少样本提示学习的自动模型补全 / Towards using Few-Shot Prompt Learning for Automating Model Completion

## 基本信息

- **标题**：Towards using Few-Shot Prompt Learning for Automating Model Completion
- **中文标题**：基于少样本提示学习的自动模型补全
- **作者**：Meriem Ben Chaaben, Lola Burgueño, Houari Sahraoui
- **单位**：Université de Montréal; University of Malaga
- **发表**：2023 IEEE/ACM 45th International Conference on Software Engineering: New Ideas and Emerging Results (ICSE-NIER)
- **DOI**：10.1109/ICSE-NIER58687.2023.00008
- **链接**：https://doi.org/10.1109/ICSE-NIER58687.2023.00008
- **页码**：7-12

**代码/仓库获取方式**：
- 原文提供 GitHub 仓库：https://github.com/meriembenchaaben/model-completion

**数据集获取方式**：
- 静态图实验基于 ModelSet 数据集（原文引用 SoSyM 2022 数据集论文）。
- 动态图示例使用公开 UML activity diagram examples。
- 原文未提供单独整理后的统一下载页，但仓库与公开数据源可追溯。

## 简报

这篇论文不做从零生成，而是研究“部分模型 -> 缺失元素补全”。作者把类图和活动图中的补全任务重新表述为 few-shot prompt learning 问题，利用 GPT-3 对部分模型做自动 completion。

- **输入**：部分 UML 类图或活动图
- **方法**：把模型元素映射成文本 pattern，构造 few-shot prompts，调用 GPT-3 生成候选补全，再映射回模型元素并排序
- **输出**：补全建议，包括新类、属性、关联名和活动流片段

```text
部分模型 -> 语义映射为 prompt -> GPT-3 补全 -> 解析回模型元素
```

一句话结论：在不微调 LLM 的前提下，few-shot prompt learning 能给出有用的模型补全建议，尤其适合建模过程中的“半自动辅助”。

## 研究问题与动机

### 问题背景

早期软件建模阶段缺少大规模训练数据，导致传统深度学习在模型补全任务上受到限制。作者希望利用大型通用 LLM 的先验知识，绕过专门训练数据稀缺的问题。

### 核心问题

1. 不经微调，few-shot prompt learning 能否支持模型补全。
2. 这种方法在静态图和动态图上是否都可行。
3. 通过简单语义映射能否让 LLM 产出与建模语法一致的补全建议。

### 研究动机

作者希望把 LLM 用作“建模助手”，不是替代建模者，而是在建模迭代过程中给出缺失元素建议。

## 核心方法

### 方法概述

论文将模型补全拆成三步：先把部分模型映射为文本 prompt，再让 GPT-3 续写，最后从续写文本中解析出模型元素建议。

### 关键技术

1. **语义映射**：根据类图或活动图语言特性，把类、属性、关系、动作片段编码为 token pattern。
2. **Few-shot 提示**：从无关领域示例中抽取 shots，指导 GPT-3 按目标格式续写。
3. **多 prompt 聚合**：针对不同 partial model 子集重复查询，再按频率对建议排序。
4. **多任务补全**：覆盖类名补全、属性补全、关联名补全和活动流补全。

## 实验与评估

### 数据集

- 静态图实验：ModelSet 中人工选取 **30** 个领域模型
- 属性实验：随机选取 **212** 个类，删除 75% 属性后测试补全
- 关联名实验：**40** 对关联类名
- 动态图部分主要为示例性展示，使用公开 activity diagram examples

### 评估指标

- 类名补全：Precision / Recall
- 属性补全：Recall
- 关联名补全：Accuracy

### 主要实验结果

1. 类名补全：
   - R1 Precision **0.57**，Recall **0.29**
   - R2 Precision **0.56**，Recall **0.45**
2. 属性补全平均 Recall **0.70**
3. 关联名补全 Accuracy **0.64**
4. 常见领域（如 Bank、University、Library）表现更好，噪声命名域表现更差。

### 方法优势

1. 不依赖领域微调数据。
2. 补全而不是从零生成，更接近真实建模交互。
3. 同时覆盖静态图和动态图，说明方法可迁移。

### 方法的局限性

1. 依赖手工设计语义映射与文本 pattern。
2. 动态图部分仍偏示例性，评估规模有限。
3. 输出是建议集，不是最终一致的完整模型。

## 与本研究的关系

### 相关性分析

- **BASELINE评估**：🟠
- **原因**：它研究的是类图/活动图补全，而不是状态机族模型补全。虽然“completion”思路对 `project_1` 有启发，但按新的 collection 标准，它不能算状态机直接或间接 baseline。

### 可借鉴之处

1. 可借鉴“先将模型映射成文本，再让 LLM 做 completion”的建模思路。
2. 对 `project_1` 的模型修复、补全和 refinement 子流程有直接启发。
3. 说明 partial-model prompting 可能比从零生成更稳。

### 存在的不足与改进空间

1. 没有控制系统状态机专用语义。
2. 缺少 formal verification 反馈。
3. 输出建议仍需人工筛选，没有自动一致性约束。

### 对本研究的启发

1. 可以把状态机生成拆成“粗生成功能骨架 + 定向补全守卫/动作/时序约束”。
2. 对状态机这种结构化工件，completion 可能比 end-to-end 生成更可靠。
3. 频率排序与多 prompt 聚合值得借鉴。

## 重要的相关工作

### 1. 重要的前身类工作

- 原文回顾了基于 graph kernel、LSTM、RoBERTa 和自然语言文档训练的模型补全方法，说明传统学习方法受限于数据稀缺。

### 2. 直接参与实验的 baseline

- 论文没有设置多个 LLM baseline，而是把自身 few-shot prompting 方法作为新想法进行初步验证。

### 3. 提供了重要论证的工作

- ModelSet 数据集论文为静态图实验提供了基础数据来源。

### 4. 在技术上提供了支持的工作

- GPT-3 和 few-shot learning 文献为作者的 prompting 设计提供技术支撑。

### 5. 其他重要工作

- [model-completion 仓库](https://github.com/meriembenchaaben/model-completion) 是复现入口。

## 文献分类总结

- **研究定位**：LLM 辅助模型补全
- **任务类型**：精化/补全
- **输入工件**：部分 UML 类图 / 活动图
- **输出工件**：类、属性、关联名与活动流补全建议
- **输出模型类型**：UML 类图 / 活动图
- **使用的LLM**：GPT-3 (`text-davinci-002`)
- **验证方式**：Precision/Recall/Accuracy
- **数据与开放性**：代码公开，数据来源可追溯
- **对本研究价值**：为状态机补全、修复和局部 refinement 提供方法启发，但只属于弱相关参照
