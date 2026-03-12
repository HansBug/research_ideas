# 从用例到状态图再到对象模型 / An Approach to Building Object Models with UML in Embedded Systems

## 基本信息

- **标题**：An Approach to Building Object Models with UML in Embedded Systems
- **中文标题**：从用例到状态图再到对象模型
- **作者**：Mohamed T. Kimour, Djamel Meslati
- **单位**：University of Annaba
- **发表**：Journal of Computing and Information Technology, 12(3)
- **年份**：2004
- **DOI**：原文未提供
- **链接**：https://pdfs.semanticscholar.org/51a5/02f94e69a794ac0dcc10802a86b9dcb80523.pdf

**代码/仓库获取方式**：
- 原文未提供公开代码/仓库获取链接。

**数据集获取方式**：
- 原文未提供独立数据集；方法以嵌入式系统 use case 文本为输入。

## 简报

这篇论文的主任务是从嵌入式系统 use cases 建立对象模型，但其核心桥梁步骤是先把 use case 转成 statechart。

- **输入**：嵌入式系统 use case 自然语言描述
- **方法**：系统分解后，先把 use case 转为描述受控部件状态的 statechart，再从 statechart 识别对象
- **输出**：statechart（中间产物） + object model（最终产物）

```text
use case 文本 -> 状态图构建 -> 对象识别 -> 对象模型
```

一句话结论：它不是纯粹“文本到状态机”的最终论文，但 statechart 是方法链路中的核心步骤，适合作为经典过渡基线。

## 研究问题与动机

### 问题背景
嵌入式系统开发中，use case 是需求入口，但直接从 use case 识别对象往往存在模糊和歧义。

### 核心问题
如何借助 statechart 这个更精确的动态模型，桥接 use case 与对象模型之间的落差。

### 研究动机
通过 statechart 先清理行为语义，再系统化地做对象识别。

## 核心方法

### 方法概述
作者先对系统做层次分解，再把自然语言 use case 转成以受控单元状态为核心的 statechart，随后从状态图中识别对象。

### 方法要点
- 先 statechart、后 object model，而不是直接做名词提取。
- 重点面向 embedded systems。
- 把歧义消解放在 statechart 建立阶段完成。

## 实验与评估

### 数据集
- **数据/案例**：嵌入式系统 use case 示例
- **来源类型**：说明性案例

### 主要实验结果
论文证明 statechart 可以作为从 use case 走向更完整 UML 分析模型的有效中间层。

### 方法的局限性
最终产物重点是对象模型而非状态机；原文对自动化工具和大规模评测交代有限。

## 与本研究的关系

### 相关性分析
- **BASELINE评估**：🟡
- **评估理由**：输入是自然语言 use cases，statechart 是关键中间产物，但最终论文关注点是对象模型而非只输出状态机。
- **与本研究的主要差异**：本研究希望直接停在状态机模型；该文把状态图当作继续做结构建模的桥梁。

### 可借鉴之处
对控制系统或嵌入式系统而言，“先行为、后结构”的路线很值得借鉴。

### 对本研究的启发
当需求文本较长时，可先建立 statechart 中间层，再决定是否继续派生其他模型。

## 重要的相关工作

### 1. 重要的前身类工作
- 论文立足于 UML/use case 驱动的嵌入式系统开发脉络。

### 2. 提供了重要论证的工作
- 它说明了 statechart 在需求澄清与对象识别之间可以充当精确中间层。

### 3. 在技术上提供了支持的工作
- 层次分解、use case 建模和 statechart 建模是核心支撑技术。

## 文献分类总结

- **类别**：用例到状态图中间建模
- **BASELINE评估**：🟡
- **输入**：嵌入式系统 use case 文本
- **输出**：statechart（中间） + object model（最终）
- **输出模型类型**：Statechart / object model
- **使用的LLM**：未使用
- **主要方法**：先把 use case 转成 statechart，再基于状态图识别对象并构建对象模型。
