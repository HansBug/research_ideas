# Req2LTL：基于层次语义分解的需求到 LTL 自动翻译 / REQ2LTL

## 基本信息

- **标题**：Bridging Natural Language and Formal Specification--Automated Translation of Software Requirements to LTL via Hierarchical Semantics Decomposition Using LLMs
- **中文标题**：连接自然语言与形式规约：基于 LLM 层次语义分解的软件需求到 LTL 自动翻译
- **作者**：Zhi Ma, Cheng Wen, Zhexin Su, Xiao Liang, Cong Tian, Shengchao Qin, Mengfei Yang
- **单位**：Xidian University；Guangzhou Institute of Technology of Xidian University；China Academy of Space Technology
- **发表**：arXiv preprint, 2025-12-19
- **年份**：2025
- **DOI**：10.48550/arXiv.2512.17334
- **链接**：https://arxiv.org/abs/2512.17334

**代码/仓库获取方式**：
- 原文 §X Data Availability 明确说明 full source code 因航天数据保密与内部平台集成暂不能公开。
- 原文给出 demonstration package、usage guide 和 video 的公开入口：[Meng-Nan-MZ/Req2LTL](https://github.com/Meng-Nan-MZ/Req2LTL.git)。
- 该 GitHub 入口是否包含可复现实验代码与完整 prompts，需要后续人工打开仓库核验；本文 DESC 不把 demo package 等同为 full source code。

**数据集获取方式**：
- 学术 benchmark 来自 prior work 中的 Circuit、Navigation、Office Email 三个公开子集，但原文未在正文中给出直接下载链接。
- 工业数据集由航天合作方 requirement documents 构建，包含 112 条 aerospace control systems requirements；原文明确说明 industrial dataset 暂不能公开，未来可能经合作方批准释放部分数据。

## 简报

本文解决的是“自然语言软件/航天控制需求如何自动翻译为 LTL 公式”的问题。核心思路不是让 LLM 一步生成 LTL，而是让 LLM 先把自然语言需求分解成层次化中间表示 OnionL，再由确定性规则把 OnionL 翻译为 LTL。它是 natural-language-to-temporal-logic 的强近邻论文，不是状态机生成论文。

- **输入**：自然语言软件需求；实验中包括 academic lifted NL-to-LTL benchmark 和 112 条航天控制系统工业需求。
- **方法**：REQ2ONIONL 用 LLM、knowledge repository 和 BUILDING-ONIONL chain-of-thought prompt 把需求改写为 OnionL JSON；ONIONL2LTL 先做 machine validation / optional visual human validation，再用 rule-based translator 合成 LTL。
- **输出**：LTL formal specification；可选输出 Mermaid visual tree，用于工程师检查 OnionL 语义结构。

```text
自然语言软件/航天控制需求
  -> LLM + knowledge repository + BUILDING-ONIONL
  -> OnionL 层次语义树 / JSON（scope, relation, atomic proposition）
  -> machine validation + optional visual human validation
  -> deterministic rule-based OnionL2LTL
  -> LTL formula
```

实验上，REQ2LTL 在 112 条工业航天需求上以 GPT-4o backend 达到 88.4% exact match / semantic accuracy、100% syntax validity、99.5% AP recall 和 0.96 BLEU；DeepSeek-V3 backend 也达到 86.6% exact match。消融显示 OnionL、staged prompting 和 verification feedback 都显著贡献性能。

## 研究问题与动机

### 问题背景

形式验证在安全关键工业软件中依赖精确 formal specification，而 LTL 是描述 reactive/embedded systems safety 与 liveness properties 的常用逻辑。然而工业需求通常是自然语言，具有隐含时序语义、嵌套条件、工作模式约束和领域词汇，人工翻译为 LTL 耗时且容易出错。

### 核心问题

论文要回答：

1. REQ2LTL 在标准 academic NL-to-LTL benchmarks 上是否能达到或超过既有方法。
2. 它能否把 real-world industrial aerospace requirements 翻译成 semantically correct 且 syntactically valid 的 LTL。
3. OnionL、BUILDING-ONIONL 和 validation feedback 分别贡献多大。
4. 工业需求中的 temporal ambiguity、nested logic 等结构性挑战是否普遍，以及结构化分解能否缓解这些问题。

### 研究动机

直接用 GPT-4o/DeepSeek-V3 等 LLM 翻译复杂工业需求时，常把“unless”“will be set”“as soon as possible”等表达误映射成过松或错误的 LTL temporal operators。论文认为错误来自 end-to-end 生成缺乏可审计的语义层次，因此提出 OnionL 作为自然语言语义与 LTL 语法之间的中间层。

### 研究意义

对 Project 1，REQ2LTL 的重要性在于展示了“LLM 负责语义结构化，确定性程序负责 formal synthesis”的混合路线。这一设计可迁移到 NL-to-STM：让 LLM 抽取状态、事件、guard、动作和层次关系，再由 deterministic compiler/validator 生成状态机 DSL，而不是直接自由输出图或代码。

## 核心方法

### 方法概述

REQ2LTL 由两个模块组成：

1. **REQ2ONIONL**：把 free-form NL requirement 转换为 structured OnionL expression。
2. **ONIONL2LTL**：验证 OnionL 结构并规则化翻译成 well-formed LTL formula。

该方法显式把“不可靠的语义理解”和“必须正确的形式语法生成”分开：LLM 主要处理语义分解，LTL 输出由规则系统保证语法正确。

### OnionL 中间表示

OnionL 是树结构中间语言，包含三类语义单元：

- **Atomic propositions**：由 `Com`、`Var`、`Rel`、`Formula` 四个字段表示系统组件、变量、关系和数值/表达式。
- **Scopes**：表示 temporal scopes（Globally、Eventually、Next）或 mode scopes。Mode scope 通常作为 implication antecedent。
- **Relations**：表示 conjunction、disjunction、implication，以及 basic/sustained Until 等 temporal relations。

形式上，OnionL 用 recursive grammar 表示 AP、scope application、relational composition 和 nested combination。它不是状态机，而是面向 LTL 公式组合结构的 semantic tree。

### BUILDING-ONIONL 分解算法

算法包含两阶段六步骤：

1. **Stage I: Macro-Structure Extraction**：识别全局 temporal/mode scope，建立顶层 OnionL node。
2. **Stage II: Recursive Clause Decomposition**：递归识别 unary temporal operators、binary logical relations 和 atomic propositions。
3. 最后执行 semantic reduction 与 AP normalization，把 atomic clause 归一到预定义字段。

该过程由 chain-of-thought prompting 驱动，并受 knowledge repository 中 OnionL 定义约束。

### Validation 与 LTL 合成

ONIONL2LTL 首先做 machine validation：depth-first traversal 检查 scope-clause pairing、operator arity/type、redundant chains、undefined operations 和 logical conflicts。可选 manual validation 会把 OnionL JSON 渲染成 Mermaid tree，让工程师检查语义。验证通过后，rule-based translator 将 scope 映射为 LTL unary operator，将 relation 映射为 binary operator，将 AP 重构为 predicate expression。

### LLM 设置

论文实验使用 GPT-4o 和 DeepSeek-V3 两种 backend。框架中 LLM 主要用于 natural-language-to-OnionL semantic decomposition；最终 LTL 由规则翻译器输出。RQ1/RQ2 的 quantitative results 明确关闭 optional manual validation，以反映 fully automated capability。

## 实验与评估

### 数据集

- **Academic Benchmark**：Circuit、Navigation、Office Email 三个 lifted NL-to-LTL 子集，需求较短、语法规则、AP 被抽象为 placeholders。
- **Industrial Dataset**：112 条来自航天合作方的 requirements，覆盖 sun-search controller 与 propulsion management system，涉及 initialization、attitude determination、anomaly handling、fault tolerance 等场景。
- **工业数据复杂度**：平均 43.7 tokens；63.2% 有至少 2 层逻辑嵌套；平均 AP 数 3.7。
- **标注方式**：每条 requirement 由两名 annotators 独立翻译为 LTL，分歧由专家讨论解决，最终由 senior engineer review。

### 评估指标

- **LTL Syntax Validity**：用 Spot parse，并检查是否可编译为 Büchi automaton。
- **Exact Match Accuracy**：由两名专家独立判断生成公式与 reference 的语义/逻辑等价。
- **Atomic Proposition Recall**：比较输出和 gold formula 的 AP set coverage。
- **BLEU**：在 AP abstraction 后评估公式 token-level structural similarity。

### Baselines

论文比较 GPT-4o 与 DeepSeek-V3 backend 下的多种策略：Zero-Shot Prompt、NL2LTL、NL2SPEC、NL2TL，以及 REQ2LTL。Academic benchmark 中还报告了与 NL2TL/NL2LTL/NL2SPEC 的对比。

### 主要实验结果

- **Academic benchmarks**：REQ2LTL 在 Circuit/Navigation/Office Email 上 binary accuracy 约 94.5%–96.7%，BLEU 约 0.97–0.98，表现与 NL2TL 接近并优于 NL2LTL/NL2SPEC。
- **Industrial requirements**：GPT-4o + REQ2LTL 达到 88.4% exact match、100.0% syntax validity、99.5% AP recall、0.96 BLEU；DeepSeek-V3 + REQ2LTL 达到 86.6% exact match、100.0% syntax validity、99.2% AP recall、0.96 BLEU。
- **对比 baseline**：GPT-4o zero-shot exact match 只有 43.8%；NL2TL 为 65.2%；REQ2LTL 明显更强。
- **消融**：去掉 OnionL 后 semantic accuracy 从 88.4% 降到 65.2%；去掉 stage-wise decomposition 降到 58.9%；去掉 verification feedback 主要让 syntax validity 下降到 90.2%。

### 错误分析与案例

论文将 incorrect LTL outputs 分为五类：Temporal Misinterpretation、Conditional Confusion、Loss of Nesting、Incorrect AP Binding、Ambiguity or Context Omission。REQ2LTL 基本消除了前四类结构性错误，剩余错误主要来自输入本身歧义。例如 “as soon as possible” 缺少精确定义，模型默认用 `F` eventuality，而专家期望更接近 `X` next step。论文用 visualized OnionL 展示了人机协同修正：112 条工业需求中 13 条初始语义错误可在 10 分钟内通过可视化界面修正。

### 方法的局限性

- 工业数据与 full source code 暂不能公开，影响复现。
- 结果主要来自 aerospace domain，跨领域泛化未验证。
- LTL 无法表达显式 quantitative timing，论文排除了 response within 5 seconds 等需求；未来计划扩展到 STL/MTL。
- 底层 LLM provider/version drift 会影响输出稳定性。

## 与本研究的关系

### 相关性分析

- **BASELINE评估**：🟠（需求到时序逻辑强近邻；非 exact STM direct baseline）
- **四条件证据**：`LLM4Modeling=🟢`，`NL输入=🟢`，`LLM方法=🟢`，`STM族输出=🟡`。
- **为什么是强近邻**：LTL 是状态机/transition system verification 的核心性质语言，REQ2LTL 面向控制/航天需求，直接服务 formal verification 前置形式化。
- **为什么不是直接 baseline**：输出是 LTL formula，不是状态机、Statechart、FSM、SysML 状态机或 pyfcstm 模型；它生成的是性质/规约公式，而不是系统行为状态结构。

### 可借鉴之处

1. OnionL 的层次 semantic IR 可启发 Project 1 的中间表示，例如把需求拆为 mode scope、temporal scope、trigger condition、effect、exception。
2. LLM 只负责 semantic decomposition，确定性 translator 负责最终 formal artifact，可降低 DSL 语法错误。
3. Visualized intermediate representation 可作为人工审查和 repair-review 的入口。
4. 对 ambiguous requirements 的错误分析可用于 Project 1 的需求澄清和 guard/time constraint disambiguation。

### 存在的不足与改进空间

- 不能直接比较 STM 结构质量，因为没有状态、事件、迁移、动作等显式输出。
- LTL 适合作为状态机 verification properties，但无法替代行为模型本身。
- 数据保密限制较强，短期难以作为完全可复现实验 baseline。

### 对本研究的启发

Project 1 可把 Req2LTL 放在“requirements formalization / property generation near baseline”而非“STM direct baseline”。它尤其支持一个研究论点：复杂工业需求必须先显式化语义结构，再进入形式工件生成；否则 LLM 容易在嵌套条件和隐含时序上犯错。

## 重要的相关工作

### 1. 重要的前身类工作

- **Early rule-based NL-to-formal-spec methods**：原文 [30]–[35] 代表 syntactic preprocessing、pattern matching、attribute grammar 等早期路线，用于说明规则方法在受限域有效但扩展性不足。
- **Seq2Seq / semantic parser / template-guided generators**：原文 [25]、[26]、[36] 等用于说明 data-driven NL–LTL translation 的前身。

### 2. 直接参与实验的baseline

- **NL2LTL**：IBM Research Python package，使用 LLM 将 NL instructions 转为 LTL formulas。
- **NL2SPEC**：template-guided prompting 方法，强调 staged construction、interpretability 和 semantic traceability。
- **NL2TL**：原本面向 lifted STL/TL 的方法，本文改造成 abstracted NL-to-LTL generation baseline。
- **Zero-Shot Prompt**：直接要求 GPT-4o/DeepSeek-V3 从需求生成 LTL，无 template 或 IR。

### 3. 提供了重要论证的工作

- **GPT-4o / DeepSeek-V3 技术报告**：用于说明选用的代表性 LLM backend。
- **Spot / NuSMV 等 LTL 工具生态**：用于论证 LTL 作为 reactive/embedded systems specification language 的实际可验证性。

### 4. 在技术上提供了支持的工作

- **Mermaid**：用于 visualized OnionL tree，支持 human-in-the-loop semantic inspection。
- **Spot**：用于 LTL syntax validity / Büchi automaton compile check。

### 5. 其他重要工作

- 原文 related work 还提到 interactive feedback 与 decomposition 机制，这些工作用于说明 LLM-based formal specification generation 正在从 one-shot prompting 转向结构化、人机协同和可解释中间表示。

## 文献分类总结

- **类别**：自然语言需求到 LTL；需求形式化强近邻。
- **BASELINE评估**：🟠（强近邻，非 exact STM direct baseline）。
- **输入**：自然语言软件/航天控制需求。
- **输出**：LTL formal specification；可选 OnionL/Mermaid intermediate tree。
- **输出模型类型**：Linear Temporal Logic formula，属于验证性质/形式规约，不是 STM-family exact artifact。
- **使用的LLM**：GPT-4o、DeepSeek-V3。
- **主要方法**：LLM 生成 OnionL 层次语义中间表示 + machine validation + rule-based LTL synthesis + optional visual human feedback。
