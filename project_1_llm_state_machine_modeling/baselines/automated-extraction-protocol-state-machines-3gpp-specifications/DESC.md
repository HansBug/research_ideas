# 使用领域提示与 LLM 集成从 3GPP 规格自动抽取协议状态机 / Automated Extraction of Protocol State Machines from 3GPP Specifications with Domain-Informed Prompts and LLM Ensembles

## 基本信息

- **标题**：Automated Extraction of Protocol State Machines from 3GPP Specifications with Domain-Informed Prompts and LLM Ensembles
- **中文标题**：使用领域提示与 LLM 集成从 3GPP 规格自动抽取协议状态机
- **作者**：Miao Zhang, Runhan Feng, Hongbo Tang, Yu Zhao, Jie Yang, Hang Qiu, Qi Liu
- **单位**：Information Engineering University, China；Purple Mountain Laboratories, China
- **发表**：arXiv preprint arXiv:2510.14348, 2025
- **DOI**：原文未提供 DOI
- **链接**：https://arxiv.org/abs/2510.14348

**代码/仓库获取方式**：
- 原文说明实现了工具 SpecGPT，但正文与参考文献未提供公开代码、项目主页或仓库获取链接。

**数据集获取方式**：
- 输入规格文档来自公开 3GPP 页面：NAS TS 24.501、NGAP TS 38.413、PFCP TS 29.244；正文参考文献给出对应 3GPP dynareport 入口。
- 原文称作者为 NAS、NGAP、PFCP Release 17 手工构建了 ground truth state machine dataset，投入超过 210 人时并经过交叉验证和同行复核，但未提供该 ground truth 数据集的公开下载链接。

## 简报

**解决的问题**

本文解决的是如何从复杂、冗长、频繁更新的 3GPP 自然语言技术规格中自动抽取协议状态机，减少人工建模对专家的依赖。

- **输入**：3GPP Word/文本规格文档，主要覆盖 5G NAS、NGAP、PFCP 协议；文档是面向领域专家的半结构化自然语言标准。
- **方法**：SpecGPT 先清洗并按章节结构合并/切分文档，再用领域知识驱动的 Chain-of-Thought prompt 抽取状态、条件、动作和转移，最后对 GPT-4o、DeepSeek V3、Qwen Turbo、Claude Sonnet 4、Gemini 2.5 Pro 等模型输出做多数投票集成。
- **输出**：协议 FSM，核心转移形如初始状态、动作文本、条件文本、下一状态；最终形成可用于协议分析的 finite state machine。

```text
输入层：3GPP Release 17 协议规格（NAS / NGAP / PFCP）
  ↓
预处理层：文档清洗 + section tree + 段落窗口合并
  ↓
LLM 方法层：状态抽取 → 条件/动作抽取 → JSON 校验与伪状态清理 → 多模型转移对齐/多数投票
  ↓
输出层：协议状态集合 + 条件/动作标注的状态转移 + 最终协议 FSM
```

**实验结果总结**：在 NAS 上，5 个模型均抽取出 18 个状态，状态抽取 F1 为 100%；NAS 转移抽取的 ensemble precision/recall/F1 为 91.86% / 90.43% / 91.14%。PFCP-all 的 F1 为 87.80%，NGAP-all 的 F1 为 69.31%。作者还报告，直接 prompt LLM 输出状态机的 F1 只有 14.87%，说明专门的 in-context prompt 与集成流程是必要的。

**研究动机**

3GPP 不提供协议形式模型，而大量协议验证、fuzzing 和安全分析依赖协议状态机。手工从 3GPP 标准维护状态机成本高、易错、难以及时跟进每年多次更新。LLM 有自然语言理解能力，但面对长篇标准文档会出现幻觉和上下文断裂，因此需要领域 prompt、轻量 RAG/context stitching 和 ensemble 机制。

**方法创新**

1. 针对 3GPP 规格的章节结构设计 section-level paragraph window merging，避免简单滑窗或单段切分导致上下文丢失。
2. 把 FSM 抽取拆为 state extraction、transition extraction、post-processing，并在 prompt 中强制区分 condition 与 action。
3. 设计领域提示来处理 state-oriented protocol 和 procedure-oriented protocol 的差异、伪状态、缩写状态、隐式状态与 cross-reference。
4. 以多 LLM 输出对齐和多数投票减少 hallucinated transitions，提升整体 F1。

**实验设计**

- 目标协议：Release 17 NAS、NGAP、PFCP；另用 NAS Release 15 测试版本泛化。
- 模型：GPT-4o、DeepSeek V3、Qwen Turbo、Claude Sonnet 4、Gemini 2.5 Pro；temperature 0.2。
- Ground truth：作者手工标注 NAS/NGAP/PFCP 状态机，并用 precision、recall、F1 评估状态/转移抽取。
- 对比：与 Hermes/NEUTREX 的 3GPP FSM 抽取结果进行对比；并报告直接 prompt 输出状态机的低 F1。

**结论与不足**

SpecGPT 是 Project 1 直接相关的 `长篇自然语言规格 -> FSM` baseline，尤其展示了 segment、prompt、post-processing、ensemble 对抗幻觉的必要性。但它聚焦通信协议而不是控制系统软件需求；代码和人工 ground truth 未公开；输出 FSM 主要是协议状态转移，未覆盖层次并发、时间约束、控制变量和验证剖面。

## 研究问题与动机

### 问题背景

移动通信网络依赖 3GPP 标准定义协议行为。协议安全验证、形式化分析、fuzz testing 和实现测试通常需要协议状态机作为输入。3GPP 规格以自然语言和半结构化文本维护，覆盖多个 release、协议层与网络功能，因此人工建模难以扩展。

### 核心问题

论文提出的问题可以概括为：

1. 如何从数百页级 3GPP 技术规格中抽取 state machine，而不被上下文长度限制和段落碎片化破坏？
2. 如何让 LLM 正确区分状态、条件、动作和转移，避免生成伪状态或 hallucinated transitions？
3. 多模型 ensemble 能否比单模型更稳健？
4. LLM 方法能否优于 Hermes/NEUTREX 这类神经解析器 + 符号综合方案？

### 研究动机

作者指出 3GPP 通常每年更新五到六次，手工维护 FSM 很难及时跟进。由于 3GPP 不提供 formal models，已有工作依赖专家解释规格并构造状态机，这限制了下游协议验证和测试。LLM 的自然语言理解能力为自动化抽取提供机会，但也需要机制性约束来降低幻觉。

### 研究意义

对协议安全分析而言，SpecGPT 生成的状态机可以作为结构化、可解释的协议行为表示，支撑自动测试、formal verification 和协议演化分析。对 Project 1 而言，它提供了一个处理“长文档需求/规格”的 direct STM baseline，而不是只处理短需求句。

## 核心方法

### 方法概述

SpecGPT 由三部分组成：

1. **Preprocessing**：清洗 3GPP 文档，移除目录、页眉页脚、脚注标记、空行和噪声图表数据；再解析章节号，构造 section tree，并把同一父节点下的叶子段落合并成语义一致的 chunk。
2. **Domain-Informed Prompt Engineering**：把 FSM 抽取拆成状态抽取、转移抽取和后处理。prompt 中显式要求抽取官方状态、区分 condition/action、引用原文 span、执行 rationality recheck，并按 JSON 格式返回。
3. **Model Ensembling**：使用多个 LLM 对相同输入生成候选转移，再根据初始状态、目标状态和 action/condition span overlap 进行对齐，以 majority voting 形成最终 FSM。

### FSM 表述

论文把蜂窝网络协议状态机定义为五元组：

$$
\langle Q, \Sigma, q_0, \delta, F \rangle
$$

其中 $Q$ 是状态集合，$\Sigma$ 是输入/转移符号集合，$q_0$ 是初始状态集合，$\delta: Q \times \Sigma \to Q$ 是转移函数，$F$ 是终止状态集合。实际抽取中，每个 transition 还带有 condition 与 action 文本 span。

### 预处理与文本切分

传统固定滑窗可能截断上下文，单段切分又会产生大量无效查询。SpecGPT 利用 3GPP 规格的层次章节编号构造 section tree，自底向上把叶节点内容合并到父节点，得到适合 LLM 输入的 coherent windows。这一点对 Project 1 的长需求文档处理有直接借鉴价值。

### Prompt 工程

- **State extraction**：区分 state-oriented protocols 和 procedure-oriented protocols。前者有显式状态名，如 `5GMM-REGISTERED`；后者状态可能是某个 procedure 完成情况。
- **Transition extraction**：条件和动作经常在同一句中，SpecGPT 在 prompt 中明确 condition 是触发响应的前提，action 是满足条件后执行的行为，并加入 few-shot examples。
- **Post-processing**：解析 JSON、检查格式、移除 pseudo-states 和 empty states。
- **Context optimization**：加入历史上下文、显式/隐式信息综合推理、基于章节号的轻量 cross-reference 检索。原文将 cross-reference 处理称为 simplified RAG，但强调不需要外部知识库或 embedding storage。

### Ensemble 算法

不同模型会抽取不同 span 或 hallucinate transition。SpecGPT 定义 transition $T_i = (Sinit_i, A_i, C_i, Snext_i)$，要求状态精确匹配，action/condition span overlap 不小于阈值 $\theta$；实验中 $\theta = 0.75$。对齐后采用多数投票聚合最终状态机。

### 是否使用 few-shot / CoT / RAG / 自动反馈 / 修复闭环

- **few-shot**：有，在 condition/action 分离中使用 few-shot examples。
- **CoT**：有，正文明确采用 Chain-of-Thought prompting 分解任务。
- **RAG**：有轻量 cross-reference handling；不是完整 embedding RAG，而是基于章节号和多文本输入的简化检索增强。
- **自动反馈 / 修复闭环**：有 JSON structural validation 和 post-processing，但没有像 repair agent 那样迭代修复 FSM。
- **形式化验证 / 模型检查 / 仿真**：没有把输出 FSM 输入模型检查器；formal role 主要是输出状态机可支撑 downstream verification/testing。

## 实验与评估

### 数据集

- **输入文档**：Release 17 NAS、NGAP、PFCP 3GPP 规格；泛化实验使用 NAS Release 15。
- **Ground truth**：作者手工构建 NAS、NGAP、PFCP 详细状态机数据集。原文称该标注投入超过 210 person-hours，由多名领域专家交叉验证和迭代 peer review。
- **规模证据**：NAS ground truth 包含 18 个 distinct states 和 179 个 transitions；R15 NAS 抽取出 142 个 transitions，约比 R17 少 20%。

### 评估指标

- Precision、Recall、F1-score。
- transition 正确性要求状态精确匹配，condition 与 action span overlap 超过 0.75。
- 成本指标包括输入/输出 token 数和每个模型每个协议运行时间。

### 实验设置

- 模型：Claude Sonnet 4、DeepSeek V3、Gemini 2.5 Pro、GPT-4o、Qwen Turbo。
- 温度：0.2。
- 硬件：32GB RAM、Intel Core i7-14700 CPU。
- 成本估计：约 $2.7/NAS、$1.6/NGAP、$1.5/PFCP 每次运行。

### 主要实验结果

1. **NAS 状态抽取**：5 个模型全部抽取出 18 个状态，F1 为 100%。
2. **NAS 转移抽取**：单模型 F1 从 68.77% 到 85.29%；ensemble 达到 precision 91.86%、recall 90.43%、F1 91.14%。
3. **PFCP 与 NGAP**：PFCP-all F1 为 87.80%，PFCP-session F1 为 92.30%；NGAP-all F1 为 69.31%，其中 UCM 层只有 60.93%，说明复杂/歧义规格仍有挑战。
4. **与 Hermes/NEUTREX 对比**：Hermes 在 5G NAS actions/conditions 上报告 81.39% / 86.40% accuracy；SpecGPT 对应为 86.41% / 92.94%。在 Hermes ground truth 上，LLM tagging F1 为 88.90%，高于 NEUTREX-Labeled 的 65.20% 和 NEUTREX-Unlabeled 的 67.82%。
5. **直接 prompt 对比**：作者尝试直接 prompt 这些 LLM 输出不同协议的状态机，F1 只有 14.87%，说明完整 pipeline 对性能至关重要。
6. **成本与泛化**：GPT-4o 在 NAS/NGAP/PFCP 上分别约 20/12/10 分钟；Gemini 2.5 Pro 时间最长。Release 15 NAS 抽取结果与版本演进预期一致。

### 方法优势

- 直接处理真实标准文档，而不是短句或模板化需求。
- 输出是状态机族模型，且带 condition/action span，可追溯到原文。
- 多模型 ensemble 明显缓解 hallucinated transitions。
- 比 Hermes 这类专门 neural parser 更少依赖任务特定训练。

### 方法的局限性

- 人工 ground truth 未公开，难以复核 F1 与 transition 对齐细节。
- SpecGPT 工具代码未公开。
- NGAP 复杂层级上的 F1 明显较低，说明对歧义、层级和跨段关系仍不稳。
- 输出未进入模型检查或仿真闭环；论文只说明可服务 downstream verification/testing。
- 研究对象是通信协议规格，不是控制系统软件需求；状态机语义也主要是协议状态转换。

## 与本研究的关系

### 相关性分析

**BASELINE评估：🟢。**

本文是 Project 1 的直接 STM baseline：输入是自然语言/半结构化技术规格文档，输出是协议 FSM，LLM 是核心抽取模块。它与控制系统状态机生成的领域不同，但任务本体完全落在 `文档/需求/规格 -> 状态机族模型`，而且其长文档处理和 ensemble 设计对 Project 1 非常有参考价值。

### 四条件建议

| 条件 | 建议 | 理由 |
|---|---|---|
| LLM4Modeling | 🟢 | 核心贡献是用 LLM 自动抽取协议 state machine。 |
| NL输入 | 🟢 | 输入是 3GPP 自然语言/半结构化标准文档。 |
| LLM方法 | 🟢 | CoT prompt、few-shot、轻量 RAG/context、multi-LLM ensemble 都是核心方法。 |
| STM族输出 | 🟢 | 输出为 protocol finite state machine，包含状态与条件/动作转移。 |

### 可借鉴之处

- 对 Project 1 的长需求文档场景，可借鉴 section tree + bottom-up merging，而非简单按 token 切块。
- prompt 中强制引用原文 span，可提升 run record 的可审计性。
- 状态/条件/动作分步抽取比直接输出整机更易做错误定位。
- 多模型 ensemble 与 majority voting 可作为 baseline 或 ablation 维度。
- 直接 prompt F1 只有 14.87% 的结果可用于论证“工程化 pipeline”必要性。

### 存在的不足与改进空间

- Project 1 需要处理功能安全需求、控制变量、guard/action、时间约束和安全性质，而 SpecGPT 主要处理协议状态与文本 span。
- SpecGPT 没有 repair loop；Project 1 可以在其基础上加入 DSL parse、semantic checker 和 verification feedback。
- 未公开 ground truth 会影响作为可复现实验 baseline 的可用性；可作为方法 baseline，但不一定能直接复现实验。

### 对本研究的启发

本文提示 Project 1：当输入从单条需求扩展为文档级需求时，核心难点会从“LLM 会不会生成状态机”转向“上下文组织、跨段引用、证据对齐、幻觉过滤和 ensemble/validation”。因此 Project 1 的 run record 应保存 chunk、prompt、原文 span、post-processing 和 voting 结果，而不是只保存最终状态机。

## 重要的相关工作

### 1. 重要的前身类工作

**Hermes: unlocking security analysis of cellular network protocols by synthesizing finite state machines from natural language specifications**

- **主要内容**：用 neural parser、domain-specific language 和逻辑驱动 FSM generation 从 3GPP 规格合成 FSM。
- **与本文关系**：SpecGPT 的主要 SOTA 对比对象。本文认为 Hermes 侧重显式转移抽取，不足以捕获隐式语义。
- **对 Project 1 的意义**：Hermes 是非 LLM/弱 LLM 时代的重要协议 FSM 抽取 baseline，可作为 direct STM extraction 前身。

**RFCNLP: Automated attack synthesis by extracting finite state machines from protocol specification documents**

- **主要内容**：从 RFC 文档抽取 FSM，并用于 automated attack synthesis。
- **与本文关系**：提供“协议文档 -> FSM -> 安全分析”的前身任务，但难以扩展到复杂 3GPP cellular protocols。

### 2. 直接参与实验的 baseline

**Hermes / NEUTREX**

- Hermes 是本文协议 FSM 抽取的 SOTA baseline。
- NEUTREX 是 Hermes 中的 neural constituency parser，用于标注 states、conditions、actions 等 transition components。
- 本文用 Hermes 论文报告的 NAS 结果和 Hermes ground truth 上的 tagging 任务评估 LLM 与 NEUTREX 的差异。

### 3. 提供了重要论证的工作

**3GPP 安全分析与协议验证工作**

- 5GReasoner、LTEInspector、5G-AKA formal analysis、CoreScan、CoreCrisis 等工作说明协议安全分析高度依赖准确状态机或协议模型。
- 这些工作为 SpecGPT 的 utility 提供动机：自动抽取 FSM 可降低 verification/testing 的手工建模成本。

### 4. 在技术上提供了支持的工作

**Chain-of-Thought、few-shot、RAG、self-consistency / hallucination 文献**

- Wei 等 CoT prompting、Parnami and Lee few-shot survey、Gao 等 RAG survey、Wang 等 self-consistency，以及 hallucination survey/inevitability 文献，共同支撑本文 prompt optimization 与 ensemble 设计。

### 5. 其他重要工作

**LLM 协议规格/解析相关工作**

- PROSPER、LLM for validating network protocol parsers、SpecGen 等工作表明 LLM 可用于协议规格提取或形式规格生成，但本文重点放在 3GPP protocol FSM extraction。

## 文献分类总结

SpecGPT 位于“LLM 文档理解 + 协议状态机抽取 + 安全验证前处理”的研究链条中。它对 Project 1 的价值不在控制系统领域本身，而在于给出成熟的文档级 direct STM extraction pipeline：结构化切分、领域 prompt、few-shot/CoT、原文 span grounding、post-processing 和 multi-model ensemble。当前最大复用风险是代码与 ground truth 未公开，因此应把它作为方法学强 baseline 和论文写作对比对象，而不是马上作为完全可复现实验 baseline。
