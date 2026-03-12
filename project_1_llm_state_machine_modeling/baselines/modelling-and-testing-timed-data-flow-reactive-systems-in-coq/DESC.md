# 从受控自然语言需求到 Coq 中的定时数据流反应系统建模与测试 / Modelling and Testing Timed Data-Flow Reactive Systems in Coq from Controlled Natural-Language Requirements

## 基本信息

- **标题**：Modelling and Testing Timed Data-Flow Reactive Systems in Coq from Controlled Natural-Language Requirements
- **中文标题**：从受控自然语言需求到 Coq 中的定时数据流反应系统建模与测试
- **作者**：Gustavo Carvalho, Igor Meira
- **单位**：Universidade Federal de Pernambuco
- **发表**：arXiv preprint
- **年份**：2019
- **DOI**：10.48550/arXiv.1910.13553
- **链接**：https://arxiv.org/abs/1910.13553

**代码/仓库获取方式**：
- 原文未给出稳定公开仓库链接。

**数据集获取方式**：
- 原文提到文献案例与 Embraer 航空工业案例，但未提供统一公开下载入口。

## 简报

- **输入**：controlled natural-language requirements
- **方法**：自动把 DFRS 规格翻译为 Coq 中的形式模型，并结合 QuickChick 做测试
- **输出**：Coq 中的 timed DFRS 形式模型 + 测试

```text
CNL 需求 -> DFRS/Coq 自动翻译 -> 性质验证与测试生成
```

一句话结论：它把自然语言到反应式行为模型的链条继续推进到了 Coq，可视为更强形式化版本的直接基线。

## 研究问题与动机

### 问题背景
已有 DFRS 工作主要完成模型获取，但验证与测试仍分散在多个工具和表示之间。

### 核心问题
如何把受控自然语言需求直接导向 Coq 中的统一建模、验证与测试框架。

### 研究动机
在一个形式化环境里同时完成规范化建模、性质验证与测试生成。

## 核心方法

### 方法概述
论文从受控自然语言需求自动得到 Coq 规格，并在 Coq/QuickChick 环境中完成验证与测试。

### 方法要点
- 入口是 controlled natural language。
- 目标模型是 Coq 中的 timed DFRS。
- 支持性质验证与 mutation-based 测试评估。

## 实验与评估

### 数据集
- **数据/案例**：文献案例与 Embraer 航空工业案例
- **来源类型**：混合案例

### 主要实验结果
原文报告在较短时间内取得较高 mutation score，说明该形式化建模与测试链条可行。

### 方法的局限性
要求受控自然语言；输出更偏 theorem-prover 中的模型表示，而不是工程上常见的状态图语法。

## 与本研究的关系

### 相关性分析
- **BASELINE评估**：🟢
- **评估理由**：输入是受控自然语言需求，输出是明确的状态式反应系统形式模型，仍属于直接可比基线。
- **与本研究的主要差异**：该文落点在 Coq/DFRS，而本研究更偏状态机建模工件与后续验证闭环。

### 可借鉴之处
对“建模后立即进入形式化验证与测试”的闭环设计非常值得借鉴。

## 文献分类总结

- **类别**：受控自然语言到形式化反应模型
- **BASELINE评估**：🟢
- **输入**：受控自然语言需求
- **输出**：Coq 中的 timed DFRS
- **输出模型类型**：Formal reactive model in Coq
- **使用的LLM**：未使用
- **主要方法**：把受控自然语言需求自动翻译为 Coq 中的 DFRS，并结合 QuickChick 做测试。
