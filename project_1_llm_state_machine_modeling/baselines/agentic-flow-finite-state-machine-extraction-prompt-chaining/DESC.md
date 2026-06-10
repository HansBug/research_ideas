# 使用提示链的有限状态机抽取智能体流程 / An Agentic Flow for Finite State Machine Extraction using Prompt Chaining

## 基本信息

- **标题**：An Agentic Flow for Finite State Machine Extraction using Prompt Chaining
- **中文标题**：使用提示链的有限状态机抽取智能体流程
- **作者**：Fares Wael, Youssef Maklad, Ali Hamdi, Wael Elsersy
- **单位**：MSA University, Giza, Egypt
- **发表**：arXiv preprint arXiv:2507.11222, 2025
- **DOI**：原文未提供 DOI
- **链接**：https://arxiv.org/abs/2507.11222

**代码/仓库获取方式**：
- 原文称 FlowFSM 源码开源于 https://github.com/YoussefMaklad/FlowFSM。
- 本轮核验该 GitHub 仓库当前可访问，但根目录仅见 `.gitignore` 和 `README.md`；README 写明 “The source code of FlowFSM will be shared soon inshallah.” 因此，虽然论文给出仓库入口，但截至本次建档核验时未能获取实现源码，代码可复现性需人工后续复查。

**数据集获取方式**：
- 输入来源为公开 RFC 文档；论文实验覆盖 FTP 与 RTSP 协议，并明确 Figure 1 使用 RFC-959 中定义的 FTP FSM。
- 原文未提供实验用 RFC chunk、人工标注 ground truth、TP/FP/FN 明细或完整抽取结果的公开下载链接；评估正确性通过人工 cross-reference 官方协议 RFC 和 standard references 完成。

## 简报

**解决的问题**

本文提出 FlowFSM，用 LLM agent、prompt chaining 与 chain-of-thought reasoning 从原始 RFC 协议文档中抽取有限状态机，面向协议分析、安全验证和 fuzzing 等下游任务。

- **输入**：原始 RFC 文档文本；实验覆盖 FTP 和 RTSP 两类网络协议。
- **方法**：先清洗/解析 RFC 章节树并提取 leaf chunks，再用三阶段 prompt chaining 逐步完成 command extraction、state transition analysis 和 rulebook synthesis；实现框架基于 CrewAI。
- **输出**：协议 FSM 的结构化 rulebook，描述每个命令的 purpose、合法前序命令/状态、合法后续命令/状态，以及由此得到的状态、消息/命令与转移。

```text
输入层：RFC 协议规范文档（FTP / RTSP）
  ↓
预处理层：去页眉页脚/格式噪声 → 章节树解析 → leaf chunk 收集 + appendix path
  ↓
智能体方法层：Command Extraction → State Transition Analysis → Rulebook Synthesis
  ↓
输出层：命令 rulebook + 协议状态/消息/转移 + FSM 抽取指标
```

**实验结果总结**：FlowFSM 在 FTP 上得到 TP=90、FP=18、FN=12，precision 83.33%、recall 88.24%、F1 85.71%；在 RTSP 上得到 TP=18、FP=4、FN=3，precision 81.82%、recall 85.71%、F1 83.72%。作者认为提示链策略能在较高 recall 下控制 hallucinated transitions，但仍需要后续验证。

**研究动机**

协议 FSM 是验证、漏洞分析和协议 fuzzing 的基础，而传统静态分析、动态分析和 NLP 抽取方法会遭遇路径爆炸、覆盖不足或自然语言歧义。LLM 具备文档理解和推理能力，但单次 prompt 容易受上下文窗口和随机输出影响。FlowFSM 的动机是通过 agentic flow 和 prompt chaining 把复杂 FSM 抽取拆成可解释的连续步骤。

**方法创新**

1. 把 RFC 文档解析成层次树和 leaf chunks，为 LLM 提供更稳定的上下文组织。
2. 用三阶段 prompt chaining 而非单次 prompt 直接生成整张 FSM。
3. 输出中间 rulebook，使命令目的、前序约束和后续约束可审查。
4. 用 CrewAI 组织多 agent / flow，可扩展到不同 LLM provider、文件解析和 RAG 工具。

**实验设计**

- 模型：`llama3.3-70b-versatile`、`deepseek-r1-distill-llama-70b`、`llama3-70b-8192`。
- 协议：FTP 与 RTSP，用于覆盖不同协议结构、交互复杂度和文档风格。
- 评估：人工将抽取转移与协议 RFC 和 standard references 对照，统计 TP、FP、FN、precision、recall、F1。

**结论与不足**

FlowFSM 是 direct STM extraction baseline：从自然语言协议规格抽取 FSM-family 工件，LLM/agent 是方法核心。限制是实验规模小，只评估 2 个协议；源码仓库当前未提供实现；人工 ground truth 和抽取结果未公开；输出是 rulebook/FSM 抽取结果，没有进入模型检查或 repair 闭环。

## 研究问题与动机

### 问题背景

FSM 可以表示协议状态、触发转移的输入/事件，以及控制转移的条件。网络协议实现的异常状态转移常与安全漏洞相关，因此协议 FSM 被用于 formal verification、vulnerability analysis、protocol fuzzing 和 reverse engineering。RFC 文档描述了许多协议的功能行为，但自然语言规范存在歧义、不完整覆盖和跨章节依赖。

### 核心问题

论文围绕两个研究问题组织实验：

1. FlowFSM 抽取协议状态机的准确性如何？
2. FlowFSM 能否泛化到不同协议规范？

更具体地说，作者想验证 prompt chaining 是否能同时减少 false positives 和 false negatives，并在 FTP 与 RTSP 这两类协议上保持相近性能。

### 研究动机

传统 FSM extraction 路线包括网络流量分析、静态代码分析、动态程序分析和 NLP-based specification extraction。它们分别受限于观察覆盖、路径爆炸、输入质量和自然语言歧义。LLM 近年来在程序分析、代码生成、漏洞检测和协议 fuzzing 中表现出潜力，但 security-critical protocol analysis 仍需要增量提示和人工验证来提高精度。

### 研究意义

与 Project 1 类似，FlowFSM 把非形式化/半形式化文本规范转成结构化状态机工件。它虽然面向网络协议而非控制系统，但对“需求/规范文档如何切块、如何逐步抽取状态/事件/转移、如何生成可审计中间表示”有直接参考价值。

## 核心方法

### 方法概述

FlowFSM 分为两个主要阶段：

1. **RFC Document Processing**：对原始 RFC 文本去除页眉、页脚和格式 artifact；把文档解析为带有 section title、body、path 和 subsections 的树结构；收集 leaf node bodies 作为 downstream chunks；同时生成 ordered appendix path 帮助 LLM 理解章节结构。
2. **FSM Extraction using Prompt Chaining**：用一系列互相依赖的 prompts 逐步抽取命令、状态转移和 rulebook。形式上，若 $P_i$ 是第 $i$ 个 prompt，$R_i$ 是响应，整体过程被写作 $R_{i+1} = M(P_i(R_i))$。

### RFC 文档结构化

论文把 RFC 文档表示为层次树：

$$
T = (N, E)
$$

其中 $N$ 是 section nodes 集合，$E \subseteq N \times N$ 是 parent-child edges。解析函数 $P:S \to T$ 依据章节编号模式递归分割文本。没有子节点的 leaf node body 被收集为后续处理 chunk。

### Prompt Chaining Architecture

三阶段提示链为：

1. **Command Extraction**：从 RFC chunks 中抽取候选命令，并按功能类别标注，形成 command inventory。
2. **State Transition Analysis**：识别每个命令的 precondition states 和 postcondition states，映射允许的 command sequences。
3. **Rulebook Synthesis**：把前两步结果形式化为三章式 rulebook。

### Rulebook 输出结构

每个协议命令被组织为三个部分：

1. **Command Purpose & Outlines**：命令功能、对系统状态的影响、触发的状态转移和执行时序约束。
2. **Valid Preceding Commands**：命令执行前必须满足的状态/前序命令，验证合法命令链。
3. **Valid Subsequent Commands**：命令执行后可能的合法后续命令与状态转移，并排除非法转移。

论文示例对 FTP `PASS` 命令生成 rulebook：`PASS` 必须紧跟 `USER`，执行后进入可能需要 account information 的状态，并允许后续 `RETR`、`TYPE` 等命令。

### Implementation

FlowFSM 基于 CrewAI 实现。CrewAI 提供 `Crew` abstraction、event-driven orchestration、多 LLM provider 集成、web search、file parsing 和 vector store retrieval for RAG 等能力。论文称 FlowFSM 把 RFC processing、context retrieval 和 stepwise FSM extraction 封装为独立模块。

### 是否使用 few-shot / CoT / RAG / 自动反馈 / 修复闭环

- **few-shot**：正文 related work 中提到 PROSPER 使用 few-shot；FlowFSM 自身没有给出明确 few-shot 实验细节。
- **CoT**：有，摘要和方法多处明确使用 chain-of-thought reasoning。
- **RAG**：实现背景提到 CrewAI 可集成 vector store retrieval for RAG；正文没有报告 FlowFSM 实验中具体 RAG 配置或消融。
- **自动反馈 / 修复闭环**：有 prompt chaining 的逐步依赖与 rulebook synthesis，但没有对错误 FSM 的自动 repair loop。
- **形式化验证 / 模型检查 / 仿真**：没有将输出送入模型检查器；评估依赖人工核对 RFC，输出可服务 verification/fuzzing。

## 实验与评估

### 数据集

- **协议**：FTP 与 RTSP。
- **输入文档**：原始 RFC 文档；论文明确 FTP FSM 参考 RFC-959，RTSP 的具体 RFC 编号正文未明确给出。
- **Ground truth / validation**：正确性由人工 cross-reference 官方协议 RFC 文档和 standard references 判断；原文未发布完整标注文件。

### 评估指标

- **TP**：抽取且人工核验正确的状态转移。
- **FP**：错误或 hallucinated transition。
- **FN**：协议中存在但抽取流程遗漏的有效转移。
- **Precision / Recall / F1**：按标准公式计算。

### 实验设置

- 使用三个 LLM：`llama3.3-70b-versatile`、`deepseek-r1-distill-llama-70b`、`llama3-70b-8192`。
- 协议选择依据：FTP 与 RTSP 在协议结构、交互复杂度和文档风格上有差异。
- 评估目标：回答准确性和跨协议泛化两个 RQ。

### 主要实验结果

| 协议 | TP | FP | FN | Precision | Recall | F1 |
|---|---:|---:|---:|---:|---:|---:|
| FTP | 90 | 18 | 12 | 83.33% | 88.24% | 85.71% |
| RTSP | 18 | 4 | 3 | 81.82% | 85.71% | 83.72% |

作者指出两个观察：

1. **Recall-Precision tradeoff**：FlowFSM 更倾向捕获更多候选转移，因此 recall 高于 precision；对安全应用来说，遗漏转移可能比额外候选更危险。
2. **跨协议稳定性**：FTP 和 RTSP precision 差约 1.51%，F1 差约 1.99%，作者认为该差异表明方法对不同协议有一定泛化能力。

### 方法优势

- 输出 rulebook 比直接 FSM 图更便于人工审计命令合法性和状态依赖。
- prompt chaining 降低一次性抽取复杂度，便于定位错误来自哪一阶段。
- 在两个协议上 F1 都超过 83%，显示了 agentic LLM pipeline 抽取协议 FSM 的可行性。
- 对 hallucinated transitions 使用 precision 显式计量，而不是只报告成功案例。

### 方法的局限性

- 只评估 FTP 与 RTSP 两个协议，样本规模很小。
- 原文未提供每个协议的完整 ground truth、抽取 rulebook、错误明细或评审协议。
- GitHub 仓库当前未发布源码，难以复现实验。
- 计算/运行成本被作者列为限制，但没有给出具体 token/time 成本表。
- 没有与 PROSPER、RFCNLP、Hermes 等直接在同一数据集上量化对比。

## 与本研究的关系

### 相关性分析

**BASELINE评估：🟢。**

本文构成 Project 1 的直接 STM baseline：输入是自然语言协议规范文档，输出是 FSM-family 行为模型，LLM/agent/prompt chaining 是核心方法。与 Project 1 的差异是领域为网络协议，输出偏 protocol command rulebook 与 flat FSM，不是控制系统层次状态机；但任务定义仍是 `文本规格 -> 状态机族模型`。

### 四条件建议

| 条件 | 建议 | 理由 |
|---|---|---|
| LLM4Modeling | 🟢 | 核心贡献是用 LLM agent 和 prompt chaining 抽取 FSM。 |
| NL输入 | 🟢 | 输入是 RFC 自然语言协议规范。 |
| LLM方法 | 🟢 | LLM、CoT、prompt chaining 和 agentic flow 是核心流程。 |
| STM族输出 | 🟢 | 输出为协议 finite-state machine / rulebook，明确包含 states、commands/messages 和 transitions。 |

### 可借鉴之处

- Project 1 可借鉴三阶段拆解：先抽取事件/命令 inventory，再抽取 pre/post state，最后合成状态机。
- Rulebook 结构可迁移为状态机中间表示，用于人工审查和 LLM-as-Judge 评审。
- 对 false positive / false negative 的显式统计，可用于 Project 1 评价“多抽一些候选再验证”是否合理。
- CrewAI agentic flow 可作为实现参考，但因源码未公开，需要独立复现。

### 存在的不足与改进空间

- Project 1 需要面向控制系统需求中的变量、守卫、动作、时间约束和安全性质，FlowFSM 主要处理协议命令序列。
- FlowFSM 未接入 DSL parser / semantic checker / model checker；Project 1 可在 rulebook synthesis 后加结构化 gate。
- 当前证据链不完整：源码、数据、完整 prompt、完整输出未公开，难以作为严格 reproducible baseline。

### 对本研究的启发

FlowFSM 强调“中间 rulebook”而不是直接让 LLM 输出最终状态图，这对 Project 1 很重要。对于复杂需求，可以先生成可审查的状态-事件-前置/后置约束表，再由确定性程序合成状态机，并把每条转移连接回原文证据。这样比直接生成 Mermaid/PlantUML 更利于审计、修复和统计错误。

## 重要的相关工作

### 1. 重要的前身类工作

**PROSPER: Extracting protocol specifications using large language models**

- **主要内容**：用 LLM 从 RFC 文档抽取 FSM，结合 textual analysis、artifact mining、prompt engineering 和 few-shot learning。
- **与本文关系**：FlowFSM 的直接 LLM 协议 FSM 抽取前身。本文相关工作称 PROSPER 在 30 个 RFC 上优于 rule-based baseline。
- **对 Project 1 的意义**：说明 LLM 从规范文档抽取 FSM 已有明确研究链条。

**ProtocolGPT: Inferring state machine from the protocol implementation via large language model**

- **主要内容**：从协议实现代码而不是规范文档中推断 FSM，使用 GPT-4、embedding retrieval 和 sequential prompt queries。
- **与本文关系**：同为 LLM + protocol FSM inference，但输入是代码实现；FlowFSM 输入是 RFC 文档。

**RFCNLP: Automated attack synthesis by extracting finite state machines from protocol specification documents**

- **主要内容**：结合机器学习和规则，从 RFC 文档抽取 FSM 并合成攻击。
- **与本文关系**：非 LLM 或弱 LLM 前身，证明从规范抽取部分 FSM 也能支持安全分析。

**Hermes**

- **主要内容**：用 neural parser 和 symbolic IR synthesis 从 cellular network specifications 合成 FSM。
- **与本文关系**：更接近 3GPP/cellular 方向的前身，与 FlowFSM 同属 `NL specification -> FSM`，但方法不是 agentic prompt chaining。

### 2. 直接参与实验的 baseline

原文没有报告与 PROSPER、ProtocolGPT、RFCNLP 或 Hermes 在同一实验设置上的量化对比。实验主要是 FlowFSM 在 FTP/RTSP 上的自评估，因此这些相关工作没有直接参与本文实验 baseline。

### 3. 提供了重要论证的工作

**协议 verification / fuzzing / reverse engineering 文献**

- TLS verified models、AFLNet、Ferry、NetPlier 等工作说明协议 FSM 对验证、fuzzing 和 state-aware analysis 重要。
- 这些文献支撑本文动机：如果 FSM 抽取质量不足，下游安全分析会受影响。

### 4. 在技术上提供了支持的工作

**ReAct 与 AI Chains**

- ReAct 支持 reasoning and acting 的 LLM agent 思想。
- AI Chains 支持把复杂任务拆解成透明、可控的 prompt chain。
- FlowFSM 明确受这些思想启发，把 FSM extraction 分解成连续、可解释步骤。

**CrewAI**

- CrewAI 是本文实现基础；提供 multi-agent orchestration 和工具集成能力。

### 5. 其他重要工作

**LLM / RAG / cybersecurity 相关文献**

- DeepSeek-R1、RAG for knowledge-intensive NLP、LLM for fuzzing/cybersecurity 等工作构成 FlowFSM 选型和背景论证，但不是本文的直接实验对比对象。

## 文献分类总结

FlowFSM 位于“LLM agent + prompt chaining + 协议 FSM 抽取”的链条中。它比泛 LLM 建模论文更直接，因为输出确实是 FSM-family 工件；也比纯协议安全论文更适合作为 Project 1 baseline，因为它把文档到状态机抽取作为核心任务。当前应评为 🟢 direct baseline，但复现实验前必须处理源码未发布、ground truth 未公开和实验规模较小三个风险。
