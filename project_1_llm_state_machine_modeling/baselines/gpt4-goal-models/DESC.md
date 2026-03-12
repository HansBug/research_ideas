# 使用 GPT-4 创建目标模型：一项探索性研究 / On the Use of GPT-4 for Creating Goal Models: An Exploratory Study

## 基本信息

- **标题**：On the Use of GPT-4 for Creating Goal Models: An Exploratory Study
- **中文标题**：使用 GPT-4 创建目标模型：一项探索性研究
- **作者**：Boqi Chen, Kua Chen, Shabnam Hassani, Yujing Yang, Daniel Amyot, Lysanne Lessard, Gunter Mussbacher, Mehrdad Sabetzadeh, Dániel Varró
- **单位**：McGill University, University of Ottawa, Linköping University
- **发表**：2023 IEEE 31st International Requirements Engineering Conference Workshops (REW)
- **DOI**：10.1109/REW57809.2023.00052
- **链接**：https://doi.org/10.1109/REW57809.2023.00052
- **页码**：262-271

**代码/仓库获取方式**：
- 原文提供 prompts 与评分结果仓库：https://github.com/ChenKua/GRL_GPT

**数据集获取方式**：
- 原文未发布统一 benchmark 数据集下载包。
- 公开内容主要包括 18 个 goal-modeling 问题、Kids Help Phone 与 Social Housing 两个案例的 prompts/评分结果。

## 简报

论文研究 GPT-4 在目标建模上的能力，具体聚焦 Goal-oriented Requirement Language (GRL) 及其文本语法 TGRL。作者既测试 GPT-4 对 goal modeling 概念的掌握，也测试它依据领域描述生成目标模型的能力。

- **输入**：简短或扩展的领域描述、TGRL 语法说明、交互式修正提示
- **方法**：四种 prompt 组合 + 多次重复运行 + 人工评分，分别评估概念掌握、模型覆盖、错误与合理新元素
- **输出**：TGRL 目标模型与对应评估结果

```text
领域描述 / TGRL 语法 -> GPT-4 生成目标模型 -> 多轮评分与聚合分析
```

一句话结论：GPT-4 对 goal modeling 有相当知识储备，但单次生成波动大、错误不少，聚合多次结果往往比任何单次运行更有价值。

## 研究问题与动机

### 问题背景

目标建模在需求工程中很重要，但关于 LLM 是否真正掌握此类建模语言，当时几乎没有直接证据。作者选择 GRL/TGRL 作为可操作、可文本化的测试对象。

### 核心问题

1. GPT-4 掌握了多少目标建模知识。
2. GPT-4 能否根据领域描述生成有价值的 GRL 模型。
3. 交互式修正能在多大程度上提升结果。

### 研究动机

作者关心的不只是“能不能生成”，而是“生成内容有多少来自真实建模知识、多少只是泛泛常识、多少是幻觉”。

## 核心方法

### 方法概述

论文包含三个实验层面：

1. **Experiment B**：18 个概念/应用问题，测 GPT-4 的 goal modeling 基础知识。
2. **Experiment K**：Kids Help Phone 已知案例，比较 4 种 prompts 下的模型生成效果。
3. **Experiment S / I**：Social Housing 与交互修正实验，考察陌生领域和多轮反馈。

### 关键技术

1. **TGRL 文本语法**：将目标模型生成任务转成文本生成任务。
2. **Prompt 组合设计**：比较“是否提供语法描述”“是否提供更长领域上下文”的影响。
3. **多次运行聚合**：每个 prompt 重复运行，以分析波动并聚合有价值元素。
4. **人工评分**：区分正确、部分正确、错误与合理但不在 ground truth 中的元素。

## 实验与评估

### 数据集

- **18** 个 goal-modeling 概念与应用问题
- **2** 个案例：
  - Kids Help Phone（领域内经典案例）
  - Social Housing（相对陌生、无公开现成模型）

### 评估指标

- 概念题平均分
- 覆盖 ground truth 的 intentional elements 比例
- 错误元素比例
- 合理但不在 ground truth 中的元素比例

### 主要实验结果

1. 基础知识实验中，加入上下文后的 R2 平均分约 **3.68/5**，明显高于 R1。
2. Kids Help Phone 生成实验中，各 prompt 对 ground truth intentional elements 的覆盖总体不高，约 **8.1% - 18.1%**。
3. 语法描述能减少错误并提高可读性，但不必然提高总覆盖率。
4. 大量响应元素虽然不在 ground truth 中，但被评为“reasonable”，说明 GPT-4 能提供启发式补充。
5. 作者明确指出：**聚合多次运行结果** 明显优于依赖任何单次运行。

### 方法优势

1. 把 goal modeling 知识测试和模型生成测试结合起来。
2. 采用文本语法 TGRL，使任务更适配 LLM。
3. 对单次波动和多次聚合价值有比较清晰的证据。

### 方法的局限性

1. 输出是 goal model，不是状态机或行为模型。
2. 覆盖率不高，且错误元素比例仍然明显。
3. 很依赖人工评审与案例 ground truth。

## 与本研究的关系

### 相关性分析

- **BASELINE评估**：🟠
- **原因**：目标模型属于需求建模邻近方向，不是状态机/行为模型；但它说明 GPT-4 在“从领域描述到形式化建模文本”任务上已有一定潜力和明显局限。

### 可借鉴之处

1. 使用文本语法承载模型是很值得借鉴的思路。
2. 多 prompt、多次运行再聚合，对 `project_1` 的状态机建模很有启发。
3. “合理但不在 ground truth 中”的评分类别适合描述 LLM 的启发式补充价值。

### 存在的不足与改进空间

1. 与控制系统状态机任务距离较远。
2. 缺少行为语义与验证反馈。
3. 生成覆盖率较低，难以直接作为强 baseline。

### 对本研究的启发

1. 状态机 DSL 或文本化中间表示可能比直接画图更适合 LLM。
2. 不应过度依赖单次输出；多轮聚合可能是必要步骤。
3. 需要把“合理补充”和“错误幻觉”区分开来，而不是简单二分。

## 重要的相关工作

### 1. 重要的前身类工作

- 原文讨论了使用 NLP 或深度学习辅助 iStar/goal model 构建的既有研究，说明目标建模自动化并非从 LLM 开始。

### 2. 直接参与实验的 baseline

- 论文没有与其他 LLM 在同一实验上直接横向比较，GPT-4 本身是主要研究对象。

### 3. 提供了重要论证的工作

- Fill 等关于 GPT-4 在概念建模任务中的实验，被用来说明 LLM 已进入建模研究。
- White 等 prompt patterns 工作为 prompt 设计提供一般性支撑。

### 4. 在技术上提供了支持的工作

- GRL/URN 标准与 TGRL 语法是整个实验的技术基础。

### 5. 其他重要工作

- [GRL_GPT](https://github.com/ChenKua/GRL_GPT) 仓库提供 prompts 和评分结果，可用于后续复核。

## 文献分类总结

- **研究定位**：LLM 目标建模探索
- **任务类型**：泛建模邻近 baseline
- **输入工件**：领域描述 + 文本语法提示
- **输出工件**：GRL/TGRL 目标模型
- **输出模型类型**：Goal model
- **使用的LLM**：GPT-4
- **验证方式**：人工评分 + 多轮聚合分析
- **数据与开放性**：prompts/评分结果公开
- **对本研究价值**：说明文本 DSL、上下文提示和多次聚合对建模任务的重要性
