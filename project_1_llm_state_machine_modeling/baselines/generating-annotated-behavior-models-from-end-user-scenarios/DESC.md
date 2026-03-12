# 从终端用户场景生成带注释的行为模型 / Generating Annotated Behavior Models from End-User Scenarios

## 基本信息

- **标题**：Generating Annotated Behavior Models from End-User Scenarios
- **中文标题**：从终端用户场景生成带注释的行为模型
- **作者**：Christophe Damas, Bernard Lambeau, Pierre Dupont, Axel van Lamsweerde
- **单位**：Université catholique de Louvain
- **发表**：IEEE Transactions on Software Engineering
- **年份**：2006
- **DOI**：原下载稿未显式给出
- **链接**：https://webperso.info.ucl.ac.be/~avl/files/avl-tse05.pdf

**代码/仓库获取方式**：
- 原文描述了工具支持的综合技术，但未给出稳定公开仓库链接。

**数据集获取方式**：
- 原文未提供独立公开 benchmark；输入来自 end-user scenarios。

## 简报

- **输入**：simple MSC 场景，包括正例与反例
- **方法**：先综合全局 LTS，再投影为组件局部 LTS，并自动生成状态不变式
- **输出**：带状态注释的行为模型 / local and global LTS

```text
终端用户场景 -> 交互式学习全局 LTS -> 组件投影 + 不变式生成
```

一句话结论：它不只合成行为模型，还自动给状态节点附上可读的语义注释，提高了人工验证可用性。

## 研究问题与动机

### 问题背景
仅由场景归纳出的状态机往往可读性差，状态节点缺少领域语义。

### 核心问题
怎样在不额外要求复杂输入的前提下，从 end-user scenarios 生成更易理解、可验证的行为模型。

### 研究动机
同时提升模型综合的自动化程度和模型结果的人类可解释性。

## 核心方法

### 方法概述
方法先交互式学习全局 LTS，再做组件级投影，并为局部状态生成不变式注释。

### 方法要点
- 输入只需简单 MSC 场景与正反例分类。
- 无需额外 flowchart 或 state assertion。
- 输出模型更利于分析师做人工验证。

## 实验与评估

### 数据集
- **数据/案例**：end-user scenarios
- **来源类型**：说明性案例

### 主要实验结果
论文证明了在仅有场景输入时，也可以自动得到既可执行又更可解释的行为模型。

### 方法的局限性
输入仍非自然语言长文；输出是 LTS 而非 UML 状态图；交互式流程仍需要用户参与正反例判定。

## 与本研究的关系

### 相关性分析
- **BASELINE评估**：🟡
- **评估理由**：核心任务就是需求场景到状态机/LTS，但输入是场景表示，不是自由自然语言。
- **与本研究的主要差异**：本研究更强调直接从文本需求出发；该文强调场景归纳与状态注释。

### 可借鉴之处
状态注释自动生成和正反例交互式学习，对本研究的模型可解释性和人在回路修正很有启发。

## 文献分类总结

- **类别**：场景到可解释行为模型综合
- **BASELINE评估**：🟡
- **输入**：MSC 场景正例/反例
- **输出**：全局/局部 LTS + 状态不变式
- **输出模型类型**：Labeled transition system
- **使用的LLM**：未使用
- **主要方法**：交互式从场景学习全局 LTS，再投影为局部模型并自动生成状态注释。
