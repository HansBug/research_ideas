# 从受控自然语言需求到 Coq 中的验证、校验与测试 / Validating, Verifying and Testing Timed Data-Flow Reactive Systems in Coq from Controlled Natural-Language Requirements

## 基本信息

- **标题**：Validating, Verifying and Testing Timed Data-Flow Reactive Systems in Coq from Controlled Natural-Language Requirements
- **中文标题**：从受控自然语言需求到 Coq 中的验证、校验与测试
- **作者**：Igor de Araújo Meira
- **单位**：Universidade Federal de Pernambuco
- **发表**：硕士学位论文
- **年份**：2020
- **DOI**：原文未提供
- **链接**：https://repositorio.ufpe.br/bitstream/123456789/38121/1/DISSERTA%C3%87%C3%83O%20Igor%20de%20Ara%C3%BAjo%20Meira.pdf

**代码/仓库获取方式**：
- 原文未提供稳定公开仓库链接。

**数据集获取方式**：
- 延续 NAT2TEST/DFRS 路线，原文未提供统一公开 benchmark 下载链接。

## 简报

- **输入**：controlled natural-language requirements
- **方法**：在 Coq 中自动生成 DFRS 规格，并进一步做 validation、verification 和 testing
- **输出**：Coq 中的可验证 timed DFRS 模型

```text
CNL 需求 -> Coq 中的 DFRS 规格 -> validation / verification / testing
```

一句话结论：这是一篇学位论文而非期刊论文，但它把自然语言到反应式形式模型的自动化链条补得更完整。

## 研究问题与动机

### 核心问题
如何把 NAT2TEST 这条受控自然语言到 DFRS 的路线推进到更系统的验证与校验层面。

### 研究动机
让需求建模、完备性检查、形式证明和测试生成形成统一闭环。

## 核心方法

### 方法概述
在 Coq 中自动生成和分析 timed DFRS，并支持模型有界探索与无用户干预的 well-formedness 验证。

### 方法要点
- 继承前作的 controlled natural-language 入口。
- 强调 validation 与 verification 的统一化。
- 输出仍是形式化反应模型。

## 实验与评估

### 数据集
- **数据/案例**：NAT2TEST/DFRS 路线中的控制与嵌入式系统案例
- **来源类型**：研究案例

### 主要实验结果
论文表明模型探索、性质验证和测试生成可在统一 Coq 框架内完成。

### 方法的局限性
这是学位论文，不是统一 benchmark 论文；输出形式对一般 MBSE 工程师仍较重。

## 与本研究的关系

### 相关性分析
- **BASELINE评估**：🟢
- **评估理由**：输入仍是受控自然语言需求，输出是明确的行为模型与验证闭环，任务高度相关。
- **与本研究的主要差异**：本研究更关注状态机工件本身与控制系统建模表达，本文更强调 Coq 形式化闭环。

### 可借鉴之处
对需求建模后立即做 validation / verification / testing 的完整流程有直接借鉴意义。

## 文献分类总结

- **类别**：受控自然语言到形式化反应模型扩展版
- **BASELINE评估**：🟢
- **输入**：受控自然语言需求
- **输出**：Coq 中的 timed DFRS
- **输出模型类型**：Formal reactive model in Coq
- **使用的LLM**：未使用
- **主要方法**：自动生成 Coq 中的 DFRS 规格，并在同一框架内完成校验、验证和测试。
