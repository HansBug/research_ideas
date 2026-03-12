# 场景、目标与状态机：模型综合的双赢组合 / Scenarios, Goals, and State Machines: a Win-Win Partnership for Model Synthesis

## 基本信息

- **标题**：Scenarios, Goals, and State Machines: a Win-Win Partnership for Model Synthesis
- **中文标题**：场景、目标与状态机：模型综合的双赢组合
- **作者**：Christophe Damas, Bernard Lambeau, Axel van Lamsweerde
- **单位**：Université catholique de Louvain
- **发表**：ACM SIGSOFT FSE
- **年份**：2006
- **DOI**：原文下载稿未显式给出
- **链接**：https://webperso.info.ucl.ac.be/~avl/files/avl-fse06.pdf

**代码/仓库获取方式**：
- 原文描述了交互式 synthesizer，但未给出稳定公开仓库链接。

**数据集获取方式**：
- 原文未提供统一 benchmark；输入为终端用户提供的 scenarios 与 goals。

## 简报

- **输入**：end-user scenarios + goals
- **方法**：交互式综合器先从场景生成 LTS，再注入 goals 缩减问题空间
- **输出**：behavior models / labelled transition systems

```text
场景 + 目标 -> 交互式综合与提问 -> LTS 行为模型
```

一句话结论：它通过把 goals 引入场景综合，减少了状态机学习时需要向用户反复提问的数量。

## 研究问题与动机

### 问题背景
仅靠场景学习状态机时，用户交互轮次可能很多，尤其在交互密集系统中。

### 核心问题
如何把 goals 这类额外需求知识注入场景到状态机的综合过程。

### 研究动机
提高场景到行为模型综合的效率与可扩展性。

## 核心方法

### 方法概述
在已有 scenario-to-LTS 综合器基础上引入目标信息，用更少的补充提问学习到更精确的行为模型。

### 方法要点
- 仍以 end-user scenarios 为主要输入。
- 通过 goal 信息缩减候选行为空间。
- 输出是可分析的 LTS 行为模型。

## 实验与评估

### 数据集
- **数据/案例**：交互型应用场景
- **来源类型**：说明性案例

### 主要实验结果
goal 信息能减少综合过程中的用户提问数量，并提升模型学习效率。

### 方法的局限性
输入不再是纯自然语言需求全文，而是结构化 scenario 与 goal；输出是 LTS 而非 UML statechart。

## 与本研究的关系

### 相关性分析
- **BASELINE评估**：🟡
- **评估理由**：任务仍是需求级行为信息到状态机/LTS 的自动综合，但输入偏场景+目标，不是自由文本。
- **与本研究的主要差异**：本研究更强调控制系统自然语言入口与状态机直接生成。

### 可借鉴之处
把额外需求知识注入综合过程、减少交互开销的思想很适合迁移到 LLM+formal synthesis 混合框架。

## 文献分类总结

- **类别**：场景与目标驱动的行为模型综合
- **BASELINE评估**：🟡
- **输入**：end-user scenarios + goals
- **输出**：LTS 行为模型
- **输出模型类型**：Labeled transition system
- **使用的LLM**：未使用
- **主要方法**：在场景综合器中注入 goals，交互式生成 LTS 行为模型。
