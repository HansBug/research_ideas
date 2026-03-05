# 基于大语言模型与提示工程技术的有限状态机设计自动化增强 / Enhancing Finite State Machine Design Automation with Large Language Models and Prompt Engineering Techniques

## 基本信息
- **标题（中文）**：基于大语言模型与提示工程技术的有限状态机设计自动化增强
- **标题（英文）**：Enhancing Finite State Machine Design Automation with Large Language Models and Prompt Engineering Techniques
- **作者**：Qun-Kai Lin, Cheng Hsu, Tian-Sheuan Chang
- **单位**：National Yang Ming Chiao Tung University, Department of Electronics and Electrical Engineering, Hsinchu, Taiwan
- **发表**：2024 IEEE Asia Pacific Conference on Circuits and Systems (APCCAS)
- **年份**：2024
- **页码**：475-478
- **链接**：https://ieeexplore.ieee.org/abstract/document/10808959/
- **arXiv**：arXiv:2506.00001v1 [cs.AR]

**代码/仓库获取方式**：原文未提供公开代码/仓库获取链接。

**数据集获取方式**：论文使用HDLBits平台的20个FSM设计问题作为测试集，可通过HDLBits网站（https://hdlbits.01xz.net/）访问这些问题。

## 简报

**解决的问题**：评估主流大语言模型（Claude 3 Opus、ChatGPT-4、ChatGPT-4o）在有限状态机（FSM）的硬件描述语言（HDL）设计自动化中的能力，并提出提示工程优化方法以提升成功率。

- **输入**：
  - HDLBits平台的20个FSM设计问题描述
  - 系统化Markdown格式的提示（包含规格说明、I/O列表、模块声明）
  - To-do-Oriented Prompting (TOP) Patch（针对特定问题的任务导向提示补丁）

- **方法**：
  - 系统化Markdown格式提示工程
  - TOP Patch提示优化策略
  - 与Chain-of-Thought (CoT)技术结合的多轮对话

- **输出**：
  - SystemVerilog格式的FSM代码
  - 各模型在不同问题类型上的成功率评估
  - 针对特定问题类型（同步复位、one-hot编码）的优化方案

```
┌─────────────────────────────────────────────────────────────────┐
│                           输入层                                 │
├─────────────────────────────────────────────────────────────────┤
│ • HDLBits FSM设计问题（20个）                                    │
│ • 系统化Markdown格式提示（规格+I/O+模块声明）                    │
│ • TOP Patch任务导向补丁（可选）                                  │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                         方法框架                                 │
├─────────────────────────────────────────────────────────────────┤
│  LLM生成 → 语法检查 → 功能验证                                   │
│         ↓                                                        │
│  [TOP Patch优化：任务分解 + 概念澄清 + 顺序执行]                 │
│         ↓                                                        │
│  [多轮对话：错误反馈 + 人工提示 + CoT引导]                       │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                          输出层                                  │
├─────────────────────────────────────────────────────────────────┤
│ • SystemVerilog FSM代码                                          │
│ • 成功率评估（Claude 3 Opus: 41%, ChatGPT-4: 32%, 4o: 31%）     │
│ • 优化后成功率（同步复位：30%→70%, one-hot：0%→90%）            │
└─────────────────────────────────────────────────────────────────┘
```

**实验结果总结**：在单次生成场景下，Claude 3 Opus达到41%的总体成功率（20个问题中成功11个），优于ChatGPT-4（32%）和ChatGPT-4o（31%）。使用TOP Patch后，ChatGPT-4o在同步复位问题上的成功率从30%提升至70%，Claude 3 Opus在one-hot FSM设计上达到90%成功率。

**研究动机**：虽然LLM在HDL设计自动化中展现出潜力，但现有研究缺乏对主流LLM在FSM设计任务上的系统性比较，且对于复杂设计场景（如同步复位、one-hot编码、长规格描述）的成功率较低。需要探索有效的提示工程策略来提升LLM的FSM设计能力。

**方法创新**：
1. 系统化Markdown格式提示：使用结构化格式（规格说明、I/O表格、状态转换表）提升LLM对问题的理解
2. TOP Patch策略：在提示末尾添加任务导向的"To-do"列表，引导LLM按顺序执行关键步骤
3. 与CoT结合的多轮对话框架：将TOP Patch作为工作流框架，集成Chain-of-Thought技术处理复杂设计

**实验设计**：
- **对比对象**：Claude 3 Opus、ChatGPT-4、ChatGPT-4o
- **数据集**：HDLBits平台的20个FSM设计问题（包括基础FSM、同步/异步复位、one-hot编码、复杂游戏逻辑等）
- **评估指标**：单次生成成功率（每个问题5次独立测试）、语法正确性、功能正确性
- **实验设置**：仅提供模块接口，不提供额外提示；对于依赖前序问题的任务，提供正确的转换表或代码

**结论与不足**：
- **主要结论**：Claude 3 Opus在稳定性和成功率上表现最佳；TOP Patch能显著提升特定问题类型的成功率；系统化提示格式对所有模型都有效
- **优势**：TOP Patch方法简单高效，人工干预少，可与其他提示工程技术集成
- **局限性**：
  1. 所有模型在one-hot设计（需要直接推导布尔方程）上表现较差
  2. 处理真值表和卡诺图时容易出错
  3. 对于状态数量少但逻辑复杂的FSM，容易误解状态转换关系
  4. ChatGPT-4o默认使用异步复位，需要特殊提示才能正确处理同步复位
  5. TOP Patch的生成仍需人工设计，自动化生成需要进一步训练和微调
