# 超越控制流：将资源视角集成到从文本生成多协作流程模型 / Beyond Control-Flow: Integrating the Resource Perspective into Multi-Collaborative Process Modeling from Text

## 基本信息

- **标题**：Beyond Control-Flow: Integrating the Resource Perspective into Multi-Collaborative Process Modeling from Text
- **中文标题**：超越控制流：将资源视角集成到从文本生成多协作流程模型
- **作者**：Anton Antonov、Humam Kourani、Alessandro Berti、Gyunam Park
- **单位**：Fraunhofer Institute for Applied Information Technology FIT；RWTH Aachen University
- **发表**：arXiv:2605.24546；预印本标注为 submitted to EDOC 2026，尚未同行评审
- **DOI**：10.48550/arXiv.2605.24546
- **链接**：[arXiv](https://arxiv.org/abs/2605.24546)；[PDF](https://arxiv.org/pdf/2605.24546)；[artifact](https://github.com/fit-process-mining/resource-perspective-gen-pm)

**代码/仓库获取方式**：
- 原文脚注说明所有 evaluation artifacts 可在 `https://github.com/fit-process-mining/resource-perspective-gen-pm` 获取；本次建档时该 GitHub 页面可访问。
- 论文还引用 POWL 与 ProMoAI 的 GitHub 仓库作为底层工具线索，但本文新增资源视角实验以 `resource-perspective-gen-pm` 为主。

**数据集获取方式**：
- 原文使用来自 Kourani 等过程建模 benchmark 的 10 个业务流程，并人工补充 pool / lane 标注；完整 evaluation artifacts 原文称在上述 GitHub 仓库中提供。
- 数据集不是控制系统 STM 数据集；它是 business process / BPMN collaboration 建模样例。

## 简报

本文解决的问题是：现有 LLM 文本到流程模型方法多聚焦控制流，即活动顺序、并发、选择和循环，却忽略业务流程中的组织参与者、角色和跨组织通信。作者提出资源感知的 ProMoAI/POWL 扩展，使 LLM 从自然语言业务流程描述中同时生成控制流和资源分配，再确定性转换为带 pools、lanes、message events 和 message flows 的 BPMN 2.0 collaboration diagrams。

- **输入**：自然语言 business process descriptions，文本中需要包含足够的参与者、组织单元或角色信息。
- **方法**：扩展 POWL 低层建模语言，使每个可见 activity transition 带 pool/lane 资源上下文；通过 prompt / few-shot / validation / error-handling 让 LLM 生成 resource-aware POWL，再由确定性算法转换为 BPMN collaboration skeleton 并自动布局。
- **输出**：标准 BPMN 2.0 collaboration diagram，包含控制流、pool、lane、message event、message flow 和 diagram layout。

```text
输入层：自然语言流程描述 + few-shot examples
  -> 方法层：LLM 生成 resource-aware POWL -> 控制流翻译 -> pool/lane 传播 -> message flow 插入 -> orthogonal layout
  -> 输出层：BPMN 2.0 collaboration diagram（process + resource perspective）
```

实验在 10 个业务流程、9 个 LLM 上比较 resource-aware 方法与 resource-agnostic ProMoAI baseline。结果显示，加入资源视角不会显著降低控制流 F1；pool/lane 发现由语义相似度和 LLM-as-a-Judge 评估；运行迭代和时延开销总体较小。对 Project 1 而言，它是 BPMN/process 强近邻：具有自然语言输入、LLM 建模和形式化行为模型输出，但输出是 BPMN collaboration，不是 STM 族。

**可比字段快照**：

- **输入**：自然语言业务流程描述。
- **输出**：资源感知 BPMN 2.0 collaboration diagrams。
- **输出模型类型**：BPMN process/collaboration model，强行为模型近邻；非状态机、Statechart 或 SysML 状态机。
- **使用的 LLM**：9 个 LLM；正文表中包括 Grok-4 Fast Reasoning、DeepSeek-v3.2、GPT 5.2、Gemini-3 Flash、Claude Sonnet 4.5、Kimi K2、Claude Haiku 4.5、Qwen3 Next 80B、GPT-5 Mini 等。
- **主要方法**：resource-aware POWL intermediate language + ProMoAI generation + deterministic POWL-to-BPMN collaboration transformation + layouting。
- **需求词工程**：中-高；显式扩展 low-level language、prompt engineering、few-shot examples、validation 与 error-handling。
- **运行仿真/验证**：通过 process mining fitness/precision 的 F1 对控制流质量评估；生成过程有 syntactic/executable model self-correction；非 Project 1 式性质模型检查。
- **代码/数据开放性**：原文称 evaluation artifacts 公开在 GitHub；本次仅确认页面可访问，未逐项复核仓库内容完整性。

## 研究问题与动机

### 问题背景

企业流程天然包含多个组织、角色、系统、客户和供应商。BPMN 2.0 支持用 pools、lanes 和 message flows 表达这些资源与协作关系，但大多数 LLM text-to-model 方法只生成“平面”控制流，不能表达谁执行活动以及跨组织通信如何发生。

### 核心问题

本文关注的问题不是“自然语言到任意 BPMN 控制流”本身，而是：在 LLM 生成流程模型时，能否把 resource perspective 作为模型生成的一等对象，而不是事后标注？换言之，活动顺序、责任分配和跨 participant communication 必须一致生成。

### 研究动机

直接让 LLM 输出 BPMN XML 会同时承担流程逻辑、资源分配、语法正确性和序列化格式，错误面太大。作者选择把 LLM 输出限制在 compact executable intermediate language，随后由程序完成 formal serialization 和 layout，从而提高可控性。

### 研究意义

对 LLM 建模研究而言，本文体现了一种重要设计：LLM 负责高层语义发现和受限中间表示生成，确定性算法负责模型语义保持转换。Project 1 的 STM 建模也可借鉴这种“约束化中间表示 + 确定性落地”的策略，尤其适用于后续把状态、事件、守卫、动作和层次并发分层生成。

### 现有方法的局限性

原文将现有 GenAI process modeling 方法分为若干问题：有些依赖资源密集 fine-tuning，有些采用通用 JSON 而非流程语义优化结构，有些多智能体方法准确但复杂且开销大。多视角流程建模工作要么 transformation 不透明，要么输出偏离标准 BPMN。本文试图提供透明、确定性、标准兼容的多视角转换路径。

### 研究目标

研究目标是生成标准兼容的 multi-collaborative BPMN 模型，并验证加入资源视角是否破坏控制流质量、资源发现是否准确、以及新增复杂度是否带来显著运行开销。

## 核心方法

### 方法概述

整体 pipeline 如下：

1. 从自然语言流程描述出发，调用 LLM 生成 resource-aware POWL 模型。
2. 将 POWL 控制流递归转换为 flat BPMN fragment。
3. 把 transition-level 的 pool/lane assignment 传播到 BPMN nodes。
4. 将跨 pool 的 sequence flow 替换为 throwing/catching message events 和 message flows。
5. 生成 collaboration skeleton，并通过 orthogonal layout routine 自动安排 pools、lanes、nodes 和 edges。

### 资源感知 POWL 扩展

原始 POWL 是层次化 partially ordered workflow language，能够通过 activity、partial order 和 choice graph 表达流程结构，并由 ProMoAI 从文本生成。本文新增组织分配函数，把每个 visible transition 映射到 pool-lane pair。silent transitions 不分配资源，因为它们用于内部控制流。

### BPMN collaboration 转换

转换包含三步：

1. **control-flow translation**：visible transition -> BPMN task；partial order -> parallel gateways；choice graph -> exclusive gateways。
2. **pool/lane assignment**：task node 继承 transition 的 pool/lane；gateway、start/end event 通过邻接节点规则传播资源上下文。
3. **message event/flow insertion**：BPMN 不允许 sequence flow 跨 pool，因此跨 pool 依赖被替换为 source pool 中的 throwing message event、target pool 中的 catching message event 和 message flow。

### Layout generation

layout 先从 flat graph layout 得到初始节点位置，再按 pool 和 lane 的 leftmost node 排序，自上而下放置 pools/lanes，最后保留水平顺序并重新计算 orthogonal edge waypoints。该部分是工程化但重要的，因为 BPMN collaboration diagram 的可读性依赖布局。

### LLM/agent 设置

- LLM 用于生成 resource-aware POWL 代码，而不是直接输出 BPMN XML。
- 原文显式提到修改 prompt engineering、few-shot examples、model generation、validation 和 error-handling。
- 方法不是多智能体架构；它强调 single-stage generation strategy 与 deterministic downstream transformations。
- 生成过程包含 automated self-correction mechanism，以迭代得到 syntactically valid and executable model。

### 形式化/验证成分

本文的“形式化”主要体现在 POWL 的结构化语义、BPMN collaboration constraints、deterministic transformation 和 process-mining quality metrics。它没有像 Project 2/3 那样生成 LTL/CTL 性质并做 model checking；也没有验证状态机安全/活性性质。

## 实验与评估

### 数据集

实验选择 10 个业务流程，来自 Kourani 等 benchmark。作者筛选了包含足够 participant 信息的流程，并手工为原始 control-flow-only ground truth BPMN 添加 pools 和 lanes。表中流程包括 Sales Order、Hiring Process、Procurement Process、Booking System、Incident Reporting、Prototype Building、Subscription Service、Complaint Handling、Internal Audit、University Admission，活动数从 8 到 26，gateways 从 4 到 22，pools/lane 数也不同。

### 评估指标

实验围绕三个 RQ：

1. 加入 resource perspective 是否降低 control-flow quality。
2. LLM 识别 pool/lane 的语义质量如何。
3. 多视角生成的迭代次数和运行时开销如何。

指标包括：

- control-flow quality score：process-mining fitness 和 precision 的 F1。
- needed iterations：生成有效模型所需迭代数。
- time per iteration：每步运行时间。
- semantic similarity：用 all-MiniLM-L6-v2 对 generated/ground-truth pool/lane labels 做 embedding cosine similarity。
- judge-based quality：固定 Grok-4.1 Fast Reasoning 作为 LLM-as-a-Judge，按 activity 对 pool/lane assignment 打分。

### 实验设置

作者用 9 个 proprietary/open-source LLM 评估同一 pipeline，并以 resource-agnostic ProMoAI 作为控制流 baseline。所有流程都有 resource-aware ground truth 用于 pool/lane 比较。

### 主要实验结果

- **控制流质量**：表 2 中所有模型 resource-aware vs baseline 的 paired t-test 均 `p > 0.05`，说明加入资源视角没有显著降低控制流 F1。
- **迭代稳定性**：多数模型迭代次数基本不变；Kimi K2 从 `1.50±0.50` 增至 `2.86±1.89`，表明它较难同时管理控制流和资源 assignment。
- **运行开销**：除少数较大模型外，runtime impact 被描述为 negligible；例如 GPT 5.2 每步时间约从 40 秒增至 60 秒。
- **资源发现**：Judge-based accuracy 普遍较高；semantic similarity 有时较低，是因为有效组织命名可能与 ground truth 词汇不同。

### 方法优势

- 把 resource perspective 与 control flow joint generation，而不是 post-hoc annotation。
- 使用 POWL 中间表示和确定性 BPMN transformation，减少直接 XML 生成的错误。
- 能产生标准 BPMN collaboration diagrams，保留 pools、lanes 和 message flows。
- evaluation artifacts 原文说明公开，便于复查。

### 方法的局限性

- 数据集只有 10 个流程，且 resource ground truth 由作者手工补充。
- 领域是 business process，不是控制系统状态机。
- 输出 BPMN collaboration diagram 不是 STM 族模型，不能评为 direct STM baseline。
- 资源语义存在多种合理建模方式，embedding similarity 可能惩罚合理替代表达。
- 论文是 2026 预印本，尚未同行评审。

## 与本研究的关系

### 相关性分析

**BASELINE评估建议：`🟠`。**

四条件建议如下：

| 条件 | 建议 | 理由 |
|---|---|---|
| LLM4Modeling | 🟢 | 核心贡献是用 LLM 从文本生成流程模型。 |
| NL输入 | 🟢 | 输入是自然语言业务流程描述。 |
| LLM方法 | 🟢 | LLM 是 resource-aware POWL 生成的核心组件。 |
| STM族输出 | 🟡 | BPMN collaboration 是强行为/process 模型近邻，但不是状态机/Statechart/SysML 状态机。 |

不能评为 `🟢` 的原因：Project 1 direct baseline 要求自然语言到 STM-family 输出；本文输出 BPMN collaboration，建模单位是 activity/gateway/pool/lane/message flow，而不是 state/event/transition/guard/action。

### 研究定位与差异化

本文是 BPMN/process modeling 强近邻，尤其适合作为“从文本生成可执行/可转换行为模型”的相关工作，而不是 exact STM direct baseline。它与 Project 1 共享 LLM + 中间表示 + 确定性转换 + 质量评估思想，但目标语义不同。

### 可借鉴之处

- **中间表示设计**：resource-aware POWL 类似 Project 1 可设计的 typed STM IR。
- **结构化转换**：把 LLM 输出限制到程序可解析语言，再由 deterministic transformation 输出正式模型。
- **跨视角约束**：pool/lane/message flow 对应 Project 1 中状态机多视角元素（状态、变量、事件、动作）的联合一致性问题。
- **LLM-as-a-Judge 辅助指标**：用于评价资源 assignment 的合理替代命名，可迁移到状态/事件命名评审。

### 存在的不足与改进空间

- 没有 STM-specific guard/action/time constraints。
- 没有验证控制系统 safety/liveness properties。
- 没有处理需求到状态空间抽象的问题。
- 样本规模小，且非安全关键控制系统。

### 对本研究的启发

Project 1 可采用“受限 STM IR + schema/diagnostics + deterministic renderer/exporter”的模式，让 LLM 先生成结构化状态机要素，再由 pyfcstm 或其他 DSL 进行 parse/semantic/design/sim gate。本文也提示：如果引入状态机资源/角色/通信视角，不应事后贴标签，而应在中间表示中一体化建模。

## 重要的相关工作

### 1. 重要的前身类工作

- POWL 与 ProMoAI：本文直接建立在 POWL/ProMoAI 的 grammar-guided process generation paradigm 上，扩展其资源视角。
- BPMN 2.0 OMG 标准：提供 pools、lanes、message flows 等 collaboration modeling 语义。

### 2. 直接参与实验的 baseline

- ProMoAI：作为 resource-agnostic baseline，用于比较 control-flow quality 与迭代/运行时开销。
- Kourani 等 process modeling benchmark：提供原始业务流程和 resource-agnostic ground truth。

### 3. 提供了重要论证的工作

- BPMN-Chatbot、BPMN Assistant、MAO 等 LLM-based process modeling 方法：说明当前 GenAI process modeling 对中间表示、交互和多阶段架构的探索。
- BPMN 多视角建模工作：提供 data/resource perspectives 的对比背景。

### 4. 在技术上提供了支持的工作

- all-MiniLM-L6-v2 sentence transformer：用于 pool/lane label semantic similarity。
- LLM-as-a-Judge / self-reflection 相关工作：支撑 judge-based quality score 的评估思路。
- hierarchical Manhattan layout：支撑自动 BPMN layouting。

### 5. 其他重要工作

- Reprository、SAP Signavio Academic Models 等流程模型仓库：被原文作为大型 process repository 背景，但由于缺少 paired textual descriptions 或 resource ground truth，未直接作为本文主评测集。

## 文献分类总结

本文属于 LLM-based BPMN/process modeling 的强近邻文献，贡献点是把 text-to-process generation 从单纯控制流提升到 resource-aware collaboration diagrams。它对 Project 1 的价值在于中间表示、确定性转换、结构化 diagnostics 和多维评估，而非直接提供 STM baseline。正式入账时应标为 `🟠` BPMN/process 强近邻，四条件为 `LLM4Modeling=🟢 / NL输入=🟢 / LLM方法=🟢 / STM族输出=🟡`。
