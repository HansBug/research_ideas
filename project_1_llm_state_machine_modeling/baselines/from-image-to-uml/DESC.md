# 从图像到 UML：基于 LLM 的 UML 图像生成初步结果 / From Image to UML: First Results of Image-Based UML Diagram Generation Using LLMs

## 基本信息

- **标题**：From Image to UML: First Results of Image-Based UML Diagram Generation Using LLMs
- **中文标题**：从图像到 UML：基于 LLM 的 UML 图像生成初步结果
- **作者**：Aaron Conrardy, Jordi Cabot
- **单位**：Luxembourg Institute of Science and Technology; University of Luxembourg
- **发表**：LLM4MDE 2024, in CEUR Workshop Proceedings Vol. 3727
- **DOI**：原文未给出 DOI
- **链接**：https://ceur-ws.org/Vol-3727/paper5.pdf
- **页码**：55-65

**代码/仓库获取方式**：
- 原文给出示例与工具入口：
  - IMG2UML examples: https://github.com/BESSER-PEARL/IMG2UML-Examples
  - BESSER examples: https://github.com/BESSER-PEARL/BESSER-examples

**数据集获取方式**：
- 论文实验使用 4 张 UML 类图图像样例（含手绘图与语义异常图）。
- 可复用示例与说明主要通过上述 GitHub 仓库获取。

## 简报

论文研究视觉/多模态 LLM 是否能够把手绘 UML 类图图片转换成可机读的 PlantUML 类图代码。作者比较 GPT-4V、Gemini Pro、Gemini Ultra 和 CogVLM 在 4 个不同复杂度样例上的表现。

- **输入**：手绘或图像化 UML 类图
- **方法**：将图像输入多模态 LLM，要求输出 PlantUML；通过 3 种 prompt、3 次重复实验评估错误数与语法错误
- **输出**：PlantUML 类图代码

```text
UML 图像 -> 多模态 LLM 识别与转写 -> PlantUML 类图
```

一句话结论：GPT-4V 在图像到 UML 转写上明显优于其他模型，但复杂图像、多关系语法和语义异常输入仍会显著拉低表现。

## 研究问题与动机

### 问题背景

在建模实践中，很多 UML 图最初只是白板或纸面草图。如果不能快速转成机读模型，这些图就很难进入低代码、代码生成或模型测试流程。

### 核心问题

1. 视觉 LLM 是否能完整重建 UML 类图。
2. 输出的 PlantUML 语法是否稳定正确。
3. 图复杂度、图本身的语义正确性和 prompt 描述长度如何影响结果。

### 研究动机

作者把这个问题视为“low-modeling”中的关键缺环，即让非正式草图更容易进入正式建模流水线。

## 核心方法

### 方法概述

作者使用 4 个 UML 类图样例和 4 个视觉 LLM，针对每个 prompt/模型/图像组合做 3 次独立尝试，以生成 PlantUML 类图。

### 关键技术

1. **多模型比较**：GPT-4V、Gemini Pro、Gemini Ultra、CogVLM。
2. **多 prompt 设计**：比较不同描述粒度的 prompt 对生成质量的影响。
3. **错误度量**：统计缺失元素、幻觉元素、语法错误与拒答。
4. **复杂度因素分析**：4 个样例按复杂度递增，并包含一个语义不合理但语法合法的图。

## 实验与评估

### 数据集

- 4 个 UML 类图图像样例
- 3 个 prompts
- 4 个 LLM
- 每组 3 次独立运行，总计 144 次生成

### 评估指标

- 错误数（缺失/幻觉元素）
- PlantUML 语法错误次数
- 无输出/拒绝输出次数

### 主要实验结果

1. **GPT-4V** 在 36 次生成中 **0 次语法错误、0 次拒答**，总体最佳。
2. **Gemini Pro** 与 **Gemini Ultra** 都有 **16/36** 次语法错误；Ultra 还有 **8/36** 次拒答。
3. **CogVLM** 语法错误最高，达到 **20/36**。
4. 图像复杂度上升时，各模型错误数整体上升。
5. 3 个 prompts 中，最简短的 **prompt 1** 整体效果最好，说明更长描述未必更优。

### 方法优势

1. 直接覆盖“图像到模型”这一多模态建模入口。
2. 结果细分到语法错误、拒答和复杂度影响，分析比较清楚。
3. 开源 examples 仓库便于后续复现。

### 方法的局限性

1. 只覆盖 UML 类图，不涉及状态图或状态机。
2. 样例仅 4 个，规模仍然偏小。
3. 输出即使语法正确，也仍可能存在缺失和幻觉，需要人工复核。

## 与本研究的关系

### 相关性分析

- **BASELINE评估**：🟠
- **原因**：它是多模态 UML 图识别，不是自然语言到状态机建模；但它与 `project_1` 中图形输入、模型数字化和邻近行为图识别方向有关。

### 可借鉴之处

1. 可借鉴其对“图复杂度”和“prompt 长度”影响的实验设计。
2. 可与已有的 `I4.0` 论文共同构成“多模态图样到模型”的邻近 baseline。
3. 可为以后处理手绘状态图/白板状态机提供初始证据。

### 存在的不足与改进空间

1. 缺少后续一致性检查或模型修复。
2. 只做类图识别，距离控制系统行为模型仍较远。
3. 数据规模太小，不足以支持强泛化结论。

### 对本研究的启发

1. 多模态输入在工业现场可能很有价值，但必须接后处理验证。
2. 对状态机类图像，语法正确不等于行为语义正确。
3. 视觉 LLM 可以作为前端识别器，后面仍需结构约束和 formal check。

## 重要的相关工作

### 1. 重要的前身类工作

- 原文把 Img2UML 与 ReSECDI 视为传统图像到 UML 识别方向的直接前身。

### 2. 直接参与实验的 baseline

- GPT-4V、Gemini Pro、Gemini Ultra、CogVLM 构成文中的直接实验比较对象。

### 3. 提供了重要论证的工作

- 先前的文本到 UML 研究（如原文引用的 [3][4]）被用来说明 LLM 已能处理文本建模任务，但图像到 UML 仍缺少研究。

### 4. 在技术上提供了支持的工作

- Design2Code、Make-real 等图像到代码工作被用来证明视觉 LLM 已经能做“图像到结构化工件”转换。

### 5. 其他重要工作

- [IMG2UML-Examples](https://github.com/BESSER-PEARL/IMG2UML-Examples) 是最直接的复现实验入口。

## 文献分类总结

- **研究定位**：多模态 UML 图识别
- **任务类型**：图像到模型的邻近 baseline
- **输入工件**：UML 类图图像
- **输出工件**：PlantUML 类图代码
- **输出模型类型**：UML 类图
- **使用的LLM**：GPT-4V, Gemini Pro, Gemini Ultra, CogVLM
- **验证方式**：错误计数 + 语法错误/拒答统计
- **数据与开放性**：示例仓库公开，样例规模小
- **对本研究价值**：为图像状态图/状态机数字化提供弱相关、多模态证据

