# RFSeek and Ye Shall Find / RFSeek：面向 RFC 的协议状态逻辑可视摘要与分析工具

## 基本信息

- **标题**：RFSeek and Ye Shall Find: A tool for summary visualization and analysis of RFCs
- **中文标题**：RFSeek：面向 RFC 的协议状态逻辑可视摘要与分析工具
- **作者**：Noga H. Rotman, Tiago Ferreira, Hila Peleg, Mark Silberstein, Alexandra Silva
- **单位**：Technion - Israel Institute of Technology, University College London, Cornell University
- **发表**：arXiv preprint, 2025
- **DOI**：10.48550/arXiv.2509.10216
- **链接**：[arXiv](https://arxiv.org/abs/2509.10216)

**代码/仓库获取方式**：
- 原文当前未在正文中提供公开代码仓库链接。
- 论文描述了 RFSeek 交互式工具和 pipeline，但本轮未发现可直接复现实验的公开实现入口。

**数据集获取方式**：
- 输入来自公开 RFC 文档；论文案例覆盖 TCP、QUIC、PPTP、DCCP 等协议。
- 原文未提供单独打包的数据集下载链接；可复核对象主要是 RFC 原文及论文中的可视摘要案例。

## 简报

RFSeek 解决的问题是：RFC 通常以长篇英文规范形式描述网络协议，官方 ASCII 状态机图往往不完整，开发者很难准确理解协议状态、事件、条件和跨章节逻辑。论文提出一个 LLM 驱动的 summary visualization 工具，从 RFC 文档中抽取协议状态逻辑，生成带 provenance 的可交互图，并让每个节点/边能够回溯到 RFC 文本来源。

- 输入：RFC 自然语言规范、ASCII 表/图和相关协议章节。
- 方法：文档预处理与分块、LLM 视觉摘要抽取、语义 grounding、交互式审计界面。
- 输出：协议状态与事件的可视摘要图，包含状态、边、条件、动作、上下文和文本出处。

```text
RFC 长文档 / ASCII 图 / 表格
  -> 分块、压缩、LLM 抽取、semantic grounding
  -> provenance-linked protocol state/event summary diagrams
```

实验与案例表明，RFSeek 不只是重建 RFC 中已有的状态机图，还能发现文本中描述但官方图遗漏的节点或边，例如 TCP、PPTP、QUIC、DCCP 中跨章节隐藏的协议逻辑。它和 Project 1 的关系较强：输入是自然语言协议规范，输出是状态/事件图式行为模型；但它目标是可审计摘要可视化，不是控制系统需求到标准 UML/SysML STM 的端到端建模，因此更适合作为协议状态机强相关 baseline，而不是控制系统 direct baseline。

## 研究问题与动机

### 问题背景

RFC 是互联网协议的权威规范，但其 prose-based 形式、篇幅和跨章节引用会让协议行为理解困难。很多 RFC 包含 ASCII-art FSM 图，但这些图经常抽象且不完整。TCP RFC 9293 的官方图明确省略许多细节，QUIC 也只给出局部状态机或文本状态描述。

### 核心问题

RFSeek 关心的是：能否用 LLM 从 RFC 文本中抽取一个更完整、更可审计的协议行为摘要图，使开发者既能看到状态/事件结构，又能直接追溯每条边来自哪段规范文本。

### 研究动机

传统 RFC 模型抽取工具多服务 fuzzing、攻击合成或代码生成，允许一定不精确；RFSeek 的目标是提升协议理解与规范审计，因此更强调 fidelity、readability 和 provenance。对 Project 1 来说，这直接提醒我们：`NL -> 状态机` 不只是生成结构，还必须保留需求文本与状态/迁移的证据链。

## 核心方法

### 方法概述

RFSeek pipeline 包括三个核心环节：

1. 文档预处理：对 RFC 进行分块、上下文感知处理、表格/ASCII 内容压缩，以适应 LLM 上下文限制。
2. visualization extraction：提示 LLM 从相关 RFC sections 中抽取节点、边、条件、动作和上下文，形成 summary representation。
3. semantic grounding：让每个可视元素与具体 RFC 文本片段绑定，支持在 UI 中点击或 hover 回源。

### Summary representation

论文提出的 summary representation 不是单纯复制 RFC ASCII FSM，而是更丰富的协议行为可视摘要。它覆盖状态、事件、条件、数据结构、错误码和其他协议逻辑，并且明确关联文本来源。这个表示对 Project 1 有启发：状态机输出最好也要包含 guard/action/context/provenance，而不只是状态和边。

### LLM 使用方式

论文在所有实验中使用 OpenAI GPT-4.1 API。LLM 被用于分块后的协议理解、摘要抽取和语义 grounding。作者强调不能对长 RFC 做一次性全局 prompting，而应把任务切成 LLM 更擅长的 summarization 与 semantic grounding 子任务。

### 用户界面与审计

RFSeek 的 UI 允许用户查看可视摘要、编辑标签、查看 summary excerpts，并通过 “Show in RFC” 定位到原文。图中绿色或不同样式的边可突出由文本额外推断出的逻辑。这种设计把 LLM 输出转成可审计对象，而不是黑箱答案。

## 实验与评估

### 数据集 / 案例系统

论文使用 TCP、QUIC、PPTP、DCCP 等 RFC 作为案例，包括 TCP RFC 9293、PPTP RFC 2637、QUIC RFC 9000 等。

### 评估指标

论文的评估更偏 case-study / tool evaluation，而不是大规模 benchmark。核心比较包括：

- RFSeek 生成的 summary 与 RFC 官方 ASCII 图之间缺失节点/边的比较。
- 与 PROSPER 等 RFC FSM 抽取工作的对比。
- 是否能发现 RFC 图中没有但文本中存在的协议逻辑。
- 每个图元素是否可追溯到 RFC 原文。

### 主要实验结果

论文显示 RFSeek 能重建已有 RFC 图，并能发现额外节点或边。例如 TCP 案例中，RFSeek 找到从 SYN-RECEIVED 到 LISTEN 的边，并定位到 RFC 文本；PPTP 案例中，RFSeek 汇总多张分散状态机；QUIC 案例中，RFSeek 从局部 figures 和 text-only 状态描述中构造更统一的视图。

### 方法优势

- 强 provenance：每个元素可回到 RFC 文本。
- 对缺失或局部官方图更鲁棒：不依赖 ASCII 图是否完整。
- 输出可读、可交互，适合开发者审计协议逻辑。
- 关注协议理解和规范改进，而不只是自动 fuzzing。

### 方法局限性

- 评估规模有限，主要是四个协议案例。
- 输出是 summary visualization，不一定是可直接进入 model checker 的严格形式化 FSM。
- 原文未提供公开代码仓库，复现实验仍有阻塞。
- 与控制系统状态机建模任务域不同，不能直接代表工业控制需求到 UML/SysML STM 的 baseline。

## 与本研究的关系

### 四条件与综合评估

| 条件 | 评估 | 理由 |
|---|---|---|
| LLM4Modeling | 🟢 | 使用 LLM 从 RFC 文档抽取协议行为图式模型 |
| NL 输入 | 🟢 | 主输入是 RFC 自然语言/半结构化协议规范 |
| LLM 方法 | 🟢 | GPT-4.1 是抽取与 grounding pipeline 的核心组件 |
| STM族输出 | 🟢 | 输出是协议状态/事件 summary diagrams，接近 protocol FSM / 状态迁移模型 |
| BASELINE评估 | 🟡 | 与 NL→协议状态机高度相关，但目标是 summary visualization 与审计，不是控制系统需求到标准 STM 的 direct baseline |

### 对 Project 1 的启发

1. **证据链设计**：状态、迁移、guard/action 应保留 provenance，便于 reviewer / 人类审计。
2. **长文档分块**：对长需求或标准文档，直接 single prompt 不可靠，需要分块、摘要、回源和一致性检查。
3. **边界任务比较**：协议状态机和控制系统状态机语义不同，但都需要从规范文本恢复状态/事件/条件结构，因此适合作为强相关 baseline。
4. **可视摘要 vs 可执行模型**：Project 1 若要形成更强贡献，应在 RFSeek 的可读性与审计性基础上进一步提供机器可验证 STM 结构。

### 不应混淆的边界

RFSeek 可以作为 `RFC / protocol specification -> protocol state/event summary` 的强相关 baseline，但不应被写成 `NL -> UML/SysML state machine` direct baseline。其输出也不是完整形式化验证模型，而是以可解释、可交互和可回源为中心的 summary visualization。

## 重要的相关工作

论文讨论了 RFC 模型抽取、协议 fuzzing、代码生成、PROSPER 等 LLM-based RFC FSM extraction 相关工作。与这些工作相比，RFSeek 的差异是：不把抽取结果主要用于 fuzzing 或自动遍历，而是服务协议理解、规范审计和 RFC 作者反馈。

对 Project 1 来说，RFSeek 与 PROSPER 一类协议状态机抽取工作构成一条重要近邻线索：它们说明 LLM 已经开始进入长规范文档到状态/事件模型的任务，但多数工作仍偏协议领域、可视摘要或 fuzzing 辅助，尚未覆盖控制系统安全需求中的时间约束、层次并发状态机和验证闭环。

## 文献分类总结

- **任务类型**：RFC 文档到协议状态逻辑可视摘要。
- **输入类型**：自然语言/半结构化协议规范。
- **输出类型**：provenance-linked protocol state/event summary diagrams。
- **LLM 角色**：抽取、摘要、grounding 核心组件。
- **Project 1 关系**：强相关协议状态机 baseline；适合比较长文档解析、状态/迁移抽取、provenance 设计，但不应列为控制系统 direct STM baseline。
- **建议总账评估**：`BASELINE评估=🟡`，四条件为 `🟢/🟢/🟢/🟢`。
