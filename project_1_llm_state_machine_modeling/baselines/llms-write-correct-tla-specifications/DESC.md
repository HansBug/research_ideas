# LLM 能否写出正确的 TLA+ 规约？/ Can LLMs Write Correct TLA+ Specifications?

## 基本信息

- **标题**：Can LLMs Write Correct TLA+ Specifications? Evaluating Natural-Language-to-TLA+ Generation
- **中文标题**：LLM 能否写出正确的 TLA+ 规约？自然语言到 TLA+ 生成评估
- **作者**：Arslan Bisharat, Brian Ortiz, Eric Spencer, Khushboo Bhadauria, TaiNing Wang, George K. Thiruvathukal, Konstantin Läufer, Mohammed Abuhamad
- **单位**：Department of Computer Science, Loyola University Chicago
- **发表**：arXiv preprint, 2026-06-04
- **年份**：2026
- **DOI**：10.48550/arXiv.2606.05792
- **链接**：https://arxiv.org/abs/2606.05792

**代码/仓库获取方式**：
- 原文在贡献中声明 release code、dataset、models 和 results，但本轮从 `paper_content.txt` 未抽取到作者专门仓库 URL。
- 数据源明确来自 TLA+ Foundation / TLA+ Community 的公开仓库：[tlaplus/examples](https://github.com/tlaplus/examples)。
- 运行环境相关引用包括 [Ollama](https://github.com/ollama/ollama)，但这不是作者评测框架仓库。

**数据集获取方式**：
- 原文使用公开 TLA+Examples 仓库构造 205 个 TLA+ specification benchmark，每个样本包括 `.tla`、自然语言注释和可选 TLC configuration。
- 本文实际测试集中，31 个 test specifications 中排除 5 个缺少 comments 或 TLC config 的样本，得到 26 个 usable test specifications。
- 若后续需要复现实验，需要人工核验作者是否另行发布了 splits、prompts、outputs 和 results；当前 DESC 仅能确认原始规格来源仓库。

## 简报

本文解决的问题是：给定 TLA+ 社区示例中抽取的自然语言注释，当前 LLM 能否生成语法和语义都正确的完整 TLA+ specification。它不是状态机图生成论文，而是 natural-language-to-TLA+ autoformalization 的系统评测；TLA+ 可表达并发/分布式系统的状态变量、next-state relation 和 temporal properties，因此是 Project 1 的强形式行为近邻，但不是 exact STM direct baseline。

- **输入**：从 TLA+Examples 中 `.tla` 文件抽取的自然语言 comments；completion 策略还会额外给定部分 ground-truth TLA+ 前缀/后缀。
- **方法**：评测 30 个 LLM、8 个模型家族、4 种 prompting 策略；生成完整或局部 TLA+ specification 后，用 SANY parser 做语法检查，用 TLC model checker 做有限状态语义验证。
- **输出**：LLM 生成的 TLA+ specification、SANY/TLC pass/fail 结果、文本相似度和 hallucination taxonomy。

```text
TLA+Examples 中的自然语言 comments / 部分 TLA+ 上下文
  -> few-shot / progressive / half-completion / fill-in-middle prompting
  -> 30 个 LLM 生成 TLA+ specification
  -> SANY syntax validation + TLC model checking
  -> 语法/语义正确率、错误类型、模型与策略差异
```

实验结论很保守：open-weight 模型最高 SANY pass rate 为 26.6%，只有 Progressive prompting 产生 TLC passes，整体 TLC pass rate 仅 8.6%；frontier proprietary models 在 few-shot 下也仍存在明显 syntax-semantics gap。论文因此主张，当前 LLM 不能在无人审核条件下可靠生成 TLA+ specifications。

## 研究问题与动机

### 问题背景

TLA+ 被用于 Amazon、Microsoft 等工业场景中的分布式/并发系统验证，但从自然语言需求写出正确 TLA+ specification 需要形式化方法专家。LLM 在代码生成上进步明显，但 TLA+ 是低资源、语法特殊且语义涉及 temporal logic、first-order logic 和 set theory 的形式语言，不能简单套用普通 code generation 经验。

### 核心问题

论文明确提出四个研究问题：

1. LLM 能否生成既 syntactically correct 又 semantically faithful 的 TLA+ specifications。
2. 不同 LLM backends 会产生哪些错误类型。
3. 质量指标如何与模型架构、规模、fine-tuning 关联。
4. LLM 生成 TLA+ 时会反复出现哪些 failure modes 和 hallucinations。

### 研究动机

已有 GenAI/TLA+ 工作更多关注 code-to-spec、syntax-constrained generation 或用 specification 指导 code generation，缺少从自然语言到完整 TLA+ specification 的大规模语义验证评估。论文希望建立一个量化基线，说明当前 LLM 在 formal specification synthesis 上离可靠使用还有多远。

### 研究意义

对 Project 1 而言，这篇论文提供了一个重要负结果：形式语言输出即使语法可解析，也远不等于语义正确。它提醒状态机建模不能只看 DSL parser pass 或图结构表面完整度，必须把模型检查、仿真、trace coverage 或性质验证纳入生成质量评价。

## 核心方法

### 方法概述

论文的 pipeline 是评测型而非提出新生成算法：

1. 从 TLA+Examples 建立 205 个样本的数据集。
2. 以 project-stratified 方式划分 train/validation/test。
3. 设计 four prompting strategies：Few-Shot、Progressive、Fill-in-Middle、Half Completion。
4. 对 25 个 open-weight models 执行 4 策略评测，共 2,600 core runs。
5. 对 5 个 proprietary models 只做 few-shot 评测，共 130 runs。
6. 对所有输出执行 SANY 与 TLC，completion 策略额外计算 BLEU、ROUGE-L、edit distance、exact match 和 line accuracy。

### 输入与中间处理

数据集中每个 TLA+ specification 尽量保留：

- 原始 `.tla` file。
- 自然语言 comments，作为 LLM 主输入。
- TLC configuration file，用于 model checking。

Completion 策略不同于 pure NL-to-spec：Half Completion 给前 50% specification，让模型补后半；Fill-in-Middle 给前 30% 和后 30%，让模型补中间 40%。因此本文既包含 full-generation，也包含 code completion 形式的生成压力测试。

### Prompting 策略

- **Few-Shot**：给 3 个 comments/specification pairs，要求一次性生成完整 TLA+ specification。
- **Progressive**：同样 few-shot，但加入围绕 module declaration、state variables、operators、temporal properties 的分步 instructional messages。
- **Fill-in-Middle**：给 ground truth prefix/suffix 和 `<FILL>` marker，不给 few-shot examples。
- **Half Completion**：给前半 specification、comments 和 configuration，让模型生成后半。

Progressive 是唯一产生 TLC passes 的 open-weight 策略，说明结构化分解对 formal model generation 有帮助，但也引入了 missing terminator、duplicate header 等多步生成特有结构错误。

### 形式化验证与度量

- **SANY**：30 秒 timeout，若 parser 报告 parsing completed 则视为 syntactic pass。
- **TLC**：对 SANY pass 的 specification 结合 TLC config 做 model checking，作为 semantic correctness 近似。
- **文本相似度**：仅对 HC/FIM 可定义目标片段的情况计算 BLEU、ROUGE-L、edit distance、exact match、line accuracy。

这一区分对 Project 1 很重要：parser pass 是最低门槛，model checker pass 才更接近行为语义有效性。

### LLM 设置

open-weight families 包括 DeepSeek R1/Coder、LLaMA、Qwen/QwQ、CodeLLaMA、Granite、Mistral、Phi、Gemma、Starling-LM、GPT-OSS 等，通过 Ollama 运行。Proprietary few-shot 评测包括 GPT-5、GPT-4o、Claude Sonnet/Haiku/Opus 系列。原文强调 proprietary models 未进入多策略核心评测，原因是 reproducibility 和 sensitive system design concerns。

## 实验与评估

### 数据集

- **规模**：205 个 TLA+ specifications，覆盖 98 个 projects。
- **领域**：distributed consensus protocols、concurrency problems、algorithmic puzzles。
- **可用性统计**：187/205 有 comments，106/205 有 config，92/205 同时有 config 与 comments。
- **划分**：train 143、validation 31、test 31；test 中 5 个因缺 comments 或 TLC config 被排除，最终 26 个用于评测。

### 评估指标

- SANY pass rate。
- TLC pass rate。
- Completion 情形的 BLEU、ROUGE-L、edit distance、exact match、line accuracy。
- 错误类型分布与 hallucination taxonomy。

### 主要实验结果

1. **open-weight 多策略**：Few-Shot 的 SANY pass rate 最高，为 26.6%；Progressive 的 SANY pass rate 为 24.9%，但只有 Progressive 有 TLC passes，56/650，约 8.6%。
2. **frontier few-shot**：GPT-5 在 26 个 test specs 上 SANY 26/26、TLC 7/26；Claude Sonnet 4.5 和 Haiku 4.5 均 TLC 3/26；GPT-4o TLC 1/26。即便 frontier model，语义正确率仍远低于语法正确率。
3. **模型规模不稳定**：DeepSeek r1:8b 在 Progressive 下 TLC 14/26，优于 r1:70b；论文认为 reasoning alignment 比参数规模更关键。
4. **code-specialized models 反而弱**：CodeLLaMA、DeepSeek-Coder、Granite 未优于通用模型，可能受 C/Python/Java 语法先验负迁移。

### 错误与 hallucination taxonomy

论文归纳五类系统性错误：

1. Unicode operator substitution：如把 TLA+ ASCII 运算符替换为 Unicode/LaTeX 符号。
2. Cross-language syntax injection：如 semicolons、Markdown backticks、`END` 等非 TLA+ 习惯。
3. Reasoning/formatting leakage：如 `<think>` blocks、Markdown fences、自然语言 prose 混入 module body。
4. Generation length miscalibration：completion 输出长度可偏离 ground truth 数倍。
5. Structural errors：尤其 Progressive 中大量缺少 `====` terminator、重复/缺失 MODULE header。

### 方法优势

- 评测规模和验证流程清晰，覆盖 open-weight 与 proprietary models。
- 同时区分 syntactic correctness 与 semantic correctness，避免把 parser pass 误当可用模型。
- 错误 taxonomy 对后续 grammar-constrained decoding、post-processing、retrieval grounding 和 verifier-guided repair 有直接借鉴价值。

### 方法的局限性

- 每个 model-specification-strategy 只运行一次，未充分覆盖 stochastic variation。
- 26 个 test specs 来自 TLA+ community repository，不代表 Amazon/Microsoft 等不可公开工业规格。
- TLC validation 是 bounded finite-state instances，不能覆盖所有参数规模下的错误。
- 自然语言输入来自 comments，密度不均，和真实需求文档存在差异。

## 与本研究的关系

### 相关性分析

- **BASELINE评估**：🟠（强形式方法近邻；非 exact STM direct baseline）
- **四条件证据**：`LLM4Modeling=🟢`，`NL输入=🟢`，`LLM方法=🟢`，`STM族输出=🟡`。
- **为什么是强近邻**：TLA+ specification 明确描述状态变量、initial predicate、next-state relation 和 temporal properties，可被 TLC model checker 执行/验证，语义上属于强行为模型近邻。
- **为什么不是直接 baseline**：输出不是 UML/SysML/pyfcstm/FSM/Statechart 等状态机族工件；任务目标是 TLA+ formal specification synthesis/evaluation，而不是自然语言到显式状态机结构建模。

### 可借鉴之处

1. Project 1 的 DSL 生成也应区分 parse pass、semantic diagnostics、simulation/model-checking pass。
2. Progressive prompting 可借鉴为“先生成状态/变量/事件/guard/action，再生成迁移与性质”的结构化生成流程。
3. Error taxonomy 可迁移为状态机 DSL 的 hallucination taxonomy：非法符号、跨语言语法污染、reasoning leakage、结构终止符缺失、长度失控。
4. TLC/SANY 两级 gate 可类比为 pyfcstm parse/semantic/design/sim 多级 gate。

### 存在的不足与改进空间

- 论文没有 repair loop；只指出 iterative TLC feedback 是 future work。
- benchmark 输入是 comments 而非完整工业需求；和 Project 1 控制系统需求输入仍有差距。
- 输出为 TLA+，不能直接用于 Project 1 的状态/迁移元素级结构 F1 或 traceability 对比。

### 对本研究的启发

Project 1 可以把本文作为“formal specification generation 的强近邻负基线”引用，用来论证：单纯让 LLM 生成形式模型并不可靠，必须引入结构化中间表示、确定性检查器、语义反馈和迭代修复，才能支撑可审计的状态机建模。

## 重要的相关工作

### 1. 重要的前身类工作

- **Lamport, 2002, Specifying Systems**：TLA+ 语言和工具基础，定义本文目标 formalism 的理论与工程背景。
- **Newcombe et al., 2015, How Amazon Web Services Uses Formal Methods**：用于说明 TLA+ 在 AWS 工业系统中的实际价值。
- **Cirstea et al., 2024, Validating Traces of Distributed Programs against TLA+ Specifications**：用于支撑 Microsoft/Azure 相关形式化实践背景。

### 2. 直接参与实验的 baseline

- 实验 baseline 主要是模型和 prompt 策略组合，而非传统论文算法：30 个 LLM family/model 与 Few-Shot、Progressive、Half Completion、Fill-in-Middle 四类策略。
- Proprietary model 子实验包括 GPT-5、GPT-4o、Claude Sonnet 4.5、Haiku 4.5、Opus 4.1，仅在 few-shot 条件下评测。

### 3. 提供了重要论证的工作

- **Hahn et al., 2022, Formal Specifications from Natural Language**：用于论证 LLM/形式规格任务随目标 formalism 复杂度上升而更困难。
- **Ferrari and Spoletini, 2025, Formal Requirements Engineering and Large Language Models: A Two-Way Roadmap**：用于论证 LLM 与 formal methods 需要互补，不能只依赖生成端。
- **Beg et al., 2025, Leveraging LLMs for Formal Software Requirements**：用于讨论 target formal language 与 pretraining distribution mismatch。

### 4. 在技术上提供了支持的工作

- **Cheng et al., 2025b, Specula** 与 **Helwer, 2025, GenAI-accelerated TLA+ Challenge**：分别代表 multi-component TLA+ pipeline 和 grammar-constrained syntax generation 方向。
- **Ollama Contributors, 2024**：open-weight 模型本地运行环境。
- **Papineni et al., 2002 / Lin, 2004**：BLEU 与 ROUGE-L 文本相似度指标来源。

### 5. 其他重要工作

- **DistAI / Yao et al., 2021**：数据驱动 invariant learning，与 TLA+ 分布式协议规格相关。
- **SpecGen / Ma et al., 2025**：LLM 生成 Java function-level specifications，并使用 verification feedback；原文明确区分其不是 system-level TLA+ generation。
- **Spracklen et al., 2025**：package hallucination 研究，被用于类比 phantom operator / identifier hallucination。

## 文献分类总结

- **类别**：自然语言到 TLA+ 形式规约生成评测；形式方法强近邻。
- **BASELINE评估**：🟠（强近邻，非 exact STM direct baseline）。
- **输入**：TLA+ examples 中抽取的自然语言 comments；部分策略含 TLA+ prefix/suffix/context。
- **输出**：TLA+ specifications 与 SANY/TLC 验证结果。
- **输出模型类型**：TLA+ formal specification / temporal action system，属于强行为模型近邻，不是 STM-family exact artifact。
- **使用的LLM**：30 个 LLM，含 DeepSeek、LLaMA、Qwen、QwQ、GPT-OSS、CodeLLaMA、Mistral、Gemma、Claude/GPT 等。
- **主要方法**：多 prompt 策略生成 + SANY syntax validation + TLC model checking + hallucination/error taxonomy。
