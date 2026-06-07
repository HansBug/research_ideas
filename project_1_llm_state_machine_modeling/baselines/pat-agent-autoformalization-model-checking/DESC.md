# PAT-Agent：面向模型检查的自动形式化 / PAT-Agent: Autoformalization for Model Checking

## 基本信息

- **标题**：PAT-Agent: Autoformalization for Model Checking
- **中文标题**：PAT-Agent：面向模型检查的自动形式化
- **作者**：Xinyue Zuo, Yifan Zhang, Hongshu Wang, Yufan Cai, Zhe Hou, Jing Sun, Jin Song Dong
- **单位**：National University of Singapore；Griffith University；University of Auckland
- **发表**：arXiv preprint, 2025；论文与仓库 README 均标注 accepted by ASE 2025，最终正式出版页元数据后续使用前仍建议复核
- **年份**：2025
- **DOI**：10.48550/arXiv.2509.23675
- **PDF来源与核验**：本轮使用用户已下载的 PDF（本目录 `paper.pdf`）；公开核验入口为 arXiv 与作者 GitHub，核验日期 2026-06-07。

**代码/仓库获取方式**：
- 论文脚注和参考文献明确给出公开仓库：[ZuoXinyue/PAT-Agent](https://github.com/ZuoXinyue/PAT-Agent)。
- 仓库包含 `Automated_Pipelines/`、`Interface/`、`PAT.Console/`、`Experiments_Demo/`、`Appendix/` 等目录，可获取自动 pipeline、交互界面、PAT model checker 工件、实验 demo 和补充结果。
- 仓库许可为 `PAT-Agent Research License (Non-Commercial)`，定位为非商业研究/教学用途实验原型。

**数据集获取方式**：
- 论文声明 code、datasets 和 interface 均公开；当前仓库中 `Datasets/` 下可直接获取 `PAT.json`、`A4F.json`、`UCS.json` 和数据格式说明。
- 三个评测集来源为：PAT library 的 26 个系统、Alloy4Fun 改编的 8 个系统、Understanding Concurrent Systems 教材整理的 6 个系统；合计 40 个建模样例、133 条验证断言。

## 简报

PAT-Agent 解决的是“从自然语言系统描述自动构造可被模型检查的形式模型，并根据模型检查反馈修复模型”的问题。它不是状态机图生成方法，而是把自然语言系统行为和用户给定性质转为 PAT/CSP# 形式模型与断言，再用 PAT model checker 检查 deadlock-freedom、reachability 和 LTL 性质，失败时用 counterexample trace 触发局部修复。

- **输入**：自然语言系统描述；自然语言或界面化填写的用户性质；每条性质带期望验证结果 `VALID` / `INVALID`。
- **方法**：Planning LLM 抽取 constants、variables、actions、guards 等建模元素，生成结构化计划；Code Generation LLM 基于计划、PAT 语法提示和 RAG 示例生成 CSP# / PAT code；PAT 执行模型检查；Repair Loop 根据反例 trace 生成局部修复指令并迭代更新模型。
- **输出**：可编译的 PAT/CSP# 形式模型、PAT assertion、验证结果、反例 trace、修复后的模型。

```text
自然语言系统描述 + 用户性质与期望结果
  -> semantic prompts + Planning LLM
  -> 结构化建模元素与代码生成计划
  -> Code Generation LLM + PAT syntax/RAG examples
  -> PAT/CSP# 模型 + PAT assertions
  -> PAT model checking
  -> counterexample-guided repair
  -> 满足用户期望验证结果的形式模型
```

实验上，论文在 40 个系统、133 条断言上报告完整 PAT-Agent pipeline 达到 `CSR/FPR/APR = 1.0000/1.0000/1.0000`，并通过消融显示 Planning LLM 和 Repair Loop 都是关键贡献；用户研究表明交互界面对非形式化方法专家也有帮助。

## 研究问题与动机

### 问题背景

形式化方法能为软件、硬件、并发系统和安全关键系统提供严格的正确性保证，但实际采用门槛高：工程师需要掌握形式语言、建模风格、断言语言和模型检查工具。LLM 具备自然语言理解和代码生成能力，因此可以降低从非形式化需求到形式模型的门槛。

### 核心问题

论文聚焦三个核心问题：

1. 如何从自然语言系统描述生成可被 PAT 模型检查器接受的 CSP# 形式模型。
2. 如何避免 LLM 直接生成 formal code 时出现语法错误、语义错位和漏建关键约束。
3. 如何把模型检查反馈，尤其是 counterexample / violation trace，转化为可执行的自动修复指令。

### 研究动机

已有 LLM 自动形式化工作更多关注 LTL、TLA+、Z、Isabelle 等公式或证明层面的翻译；系统级模型生成仍容易停留在 direct NL-to-code，且对复杂并发模型、共享变量和性质满足性支持不足。PAT-Agent 的动机是把 LLM 的生成能力与 PAT 的形式验证能力结合起来，形成可检查、可修复、可交互的端到端建模流程。

### 研究意义

对形式化方法社区，它提供了一个 NL -> CSP# / PAT 的自动化原型；对 `project_1`，它提供了“LLM 生成 + formal verifier + counterexample repair”的高价值闭环范式，尤其适合借鉴到状态机建模后的验证与修复阶段。

### 现有方法的局限性

论文指出，直接让 LLM 从自然语言生成形式模型容易失败，主要原因包括：

1. 形式语言语法复杂，LLM 可能产生不可编译代码。
2. 自然语言与形式逻辑之间存在语义鸿沟，LLM 可能误解用户意图。
3. 直接生成缺少可解释中间表示，难以定位建模错误。
4. 若没有模型检查反馈，错误模型很难自动收敛到满足性质的实现。

### 研究目标

PAT-Agent 的目标是给定自然语言描述 $N$ 和一组用户需求 $Q = \{(\phi_i, o_i)\}$，构造一个 well-formed PAT model $M^\star$，使每个性质 $\phi_i$ 在 PAT 验证下得到用户期望结果 $o_i$。该目标强调的不是单次生成质量，而是通过计划、生成、验证和修复得到最终可验证模型。

## 核心方法

### 方法概述

PAT-Agent 包含四个核心组件：

1. **Planning LLM**：从自然语言系统描述中抽取 constants、variables、processes、actions、guard conditions、state changes 等语义元素，并生成 detailed model generation plan。
2. **Code Generation LLM**：将计划转成 PAT specification language 中的 CSP# 代码，同时利用 PAT 语法文档、常见错误提示和 RAG 检索到的 `<plan, code>` 示例。
3. **Model Checker (PAT)**：对生成模型执行 deadlock-freedom、reachability、LTL verification，并比较实际验证结果与用户期望 `VALID` / `INVALID`。
4. **Repair Loop**：当某条性质结果不匹配时，读取 PAT 返回的 counterexample / violation trace，生成局部修复指令，再让 Code Generation LLM 修改模型。

### 输入处理与中间表示

输入由两部分组成：

1. **系统描述**：自然语言描述系统目标、子系统、交互方式和行为。例如 car 示例中包含 driver、key、door、motor 四个过程。
2. **需求/性质**：用户指定待验证性质和期望结果。性质可对应 deadlock-free、reachability 或 LTL；界面中可通过变量-值对、下拉选项和内部翻译生成断言。

Planning LLM 不直接输出代码，而是先生成 JSON-serializable 的结构化元素和自然语言代码计划。论文把这类中间表示称为 semantic prompt / model generation plan，其槽位包括常量名称和值、变量类型和值域、动作名称、guard 条件和状态更新。

### Semantic Prompt 与 Planning LLM

Planning LLM 使用参数化 semantic prompts，而不是自由形式 prompt。每个 prompt 通常包含：

1. role specification，说明当前抽取任务；
2. supporting context，包含系统描述和前序阶段已抽取元素；
3. structural guidance，规定输出元素字段；
4. validation rules，例如常量必须先于变量声明、命名不能冲突、变量可能值需要由常量定义。

这种设计的作用是把“模糊自然语言 -> formal code”的大任务拆为多个可检查的结构化抽取任务，从而提高可解释性和后续代码生成稳定性。

### Code Generation LLM 与 RAG 示例

Code Generation LLM 接收详细计划并输出 PAT/CSP# 模型。论文默认配置中，Planning LLM 使用 OpenAI `o3-mini-2025-01-31`，Code Generation LLM 使用 Anthropic `claude-3-7-sonnet-20250219`；还评估了 DeepSeek-R1 及不同模型组合。

代码生成 prompt 包含两类增强：

1. **syntax cue**：紧凑 PAT 语法说明和早期实验中常见错误，例如分号、同步、断言格式问题。
2. **RAG exemplar**：从 curated `<plan, code>` 数据库中按 plan 相似度检索最接近示例；若没有高度相似样例，也作为 one-shot code structure 示例。

### PAT 模型检查

生成模型进入 PAT 后，使用 PAT 的内置检查能力验证：

1. `#assert P deadlockfree`：检查 deadlock-freedom。
2. `#assert P reaches cond`：检查 reachability。
3. `#assert P |= F`：检查 LTL 公式。

论文特别强调用户提供的是“性质 + 期望结果”。因此通过与否不是简单看 PAT 返回 `VALID`，而是看实际验证结果是否匹配用户期望。例如某个危险状态可达性的期望可能是 `INVALID`；若 PAT 判断可达，则说明需求未满足。

### Verification-Guided Repair Loop

当验证结果不匹配时，PAT 返回 counterexample trace。Repair Loop 不重新运行完整 planning，而是在当前模型上做局部修复：

1. 从 trace 中抽取导致失败的动作序列。
2. 用 locality-of-fault heuristic 排序可疑动作：越接近 violation point、出现越频繁的动作优先级越高。
3. 按性质类型生成 repair directive，例如 safety violation 常建议 tighten guard，liveness / deadlock 问题可能建议 loosen guard 或补充 outgoing transition。
4. 将修复指令、当前模型和失败信息回填给 Code Generation LLM，生成修改后的模型。

论文将最大修复轮数设为 `Kmax = 5`。若 5 轮后仍未满足所有需求，系统返回最新模型和 counterexample trace。

### 交互式界面

虽然 pipeline 可全自动运行，论文还实现了 web-based interface，支持非形式化方法专家交互式建模：

1. chatbot 根据高层自然语言描述判断是否可复用历史 verified examples；
2. information gathering 界面展示 Planning LLM 抽取出的 constants、variables、actions；
3. requirements specification 界面帮助用户定义性质与期望结果；
4. plan/code/verification viewers 允许用户查看计划、代码、断言、验证结果和反例；
5. repair dashboard 支持手工编辑或触发自动修复。

该界面还维护一个 verified systems 数据库，新验证成功的模型会加入其中，以支持后续复用。

### 形式化定义

论文将 pipeline 抽象为以下变换：

$$
T_{\mathrm{plan}} : L_{NL} \rightarrow \Pi \rightarrow P
$$

$$
T_{\mathrm{gen}} : P \rightarrow M
$$

$$
V : M \times Q \rightarrow \{MATCH, MISMATCH\}^{m} \times C
$$

$$
T_{\mathrm{repair}} : M \times C \times R \rightarrow M
$$

这里 $L_{NL}$ 是自然语言规格集合，$\Pi$ 是结构化 semantic prompt 空间，$P$ 是详细生成计划，$M$ 是 well-formed PAT models，$Q$ 是用户性质及期望结果集合，$C$ 是 PAT 返回的 counterexample traces，$R$ 是修复指令集合。

## 实验与评估

### 数据集

论文使用三个数据集，共 40 个系统、133 条断言：

| 数据集 | 来源 | 系统数 | 断言数 | 说明 |
|---|---|---:|---:|---|
| PAT | PAT library | 26 | 74 | 来自 PAT 示例库的自然语言描述与需求 |
| UCS | Understanding Concurrent Systems | 6 | 19 | 从 CSP 教材整理的并发系统样例 |
| A4F | Alloy4Fun | 8 | 40 | 从 Alloy4Fun 数据集改编为可用 CSP# 表达的任务 |
| Overall | 三者合计 | 40 | 133 | 论文主实验全集 |

仓库 `Datasets/README.md` 显示，每条数据包含 `modelName`、`modelDesc`、`interactionMode`、`subsystems`、`assertions` 等字段；这对后续复现实验和迁移 benchmark 很有价值。

### 评估指标

论文使用三个指标：

1. **CSR (Compilation Success Rate)**：生成模型可编译比例。
2. **FPR (Full-Pass Rate)**：系统所有断言均达到期望结果的比例。
3. **APR (Average Pass Rate)**：断言层面的平均满足比例。

这里的 “pass” 指 PAT 验证结果与用户指定期望结果一致，而不是单纯指性质为真。

### 实验设置

默认 PAT-Agent 配置为 `<o3, Claude>`：

1. Planning LLM：OpenAI `o3-mini-2025-01-31`。
2. Code Generation LLM：Anthropic `claude-3-7-sonnet-20250219`。
3. 额外模型：DeepSeek-R1，用于直接生成和不同 planner / generator 组合对比。
4. 直接生成 baseline：R1、o3、Claude 单模型直接从自然语言生成 PAT code，但仍给同样的 RAG exemplar 和语法文档，以保证公平性。

### RQ1：正式模型生成效果

直接 LLM generation 在 overall 上的表现为：

| 方法 | CSR | FPR | APR |
|---|---:|---:|---:|
| R1 direct | 0.4250 | 0.3750 | 0.3910 |
| o3 direct | 0.7250 | 0.5250 | 0.6391 |
| Claude direct | 0.7500 | 0.4750 | 0.6316 |
| PAT-Agent `<o3, Claude>` | 1.0000 | 1.0000 | 1.0000 |

论文解释，PAT-Agent 的 100% 并不代表初始生成完全无错，而是 verification-guided repair loop 能不断利用 counterexample feedback 修复模型，直到所有用户指定需求满足。

### RQ2：消融实验

整体消融结果：

| 方法 | CSR | FPR | APR |
|---|---:|---:|---:|
| Full Pipeline | 1.0000 | 1.0000 | 1.0000 |
| Without Repair Loop | 1.0000 | 0.7500 | 0.8045 |
| Without Planning Model | 0.7500 | 0.6000 | 0.7594 |
| Without Both Components | 0.7500 | 0.4750 | 0.6316 |

这说明：

1. Planning LLM 主要提升结构化建模质量和可编译性。
2. Repair Loop 主要把初始可编译但未满足性质的模型推进到 full-pass。
3. 两者同时去掉时，退化为 direct NL-to-code，效果接近普通 LLM baseline。

### Repair Loop 轮次效果

Overall 数据上，修复轮次提升如下：

| 轮次 | CSR | FPR | APR |
|---|---:|---:|---:|
| Round 0 | 1.0000 | 0.7500 | 0.8045 |
| Round 1 | 1.0000 | 0.7750 | 0.8722 |
| Round 2 | 1.0000 | 0.8750 | 0.9549 |
| Round 5 | 1.0000 | 1.0000 | 1.0000 |

这组结果是本文对 `project_1` 最重要的证据：formal verifier 返回的反例不仅能做结果判定，还能成为 LLM 修复模型的结构化反馈。

### RQ3：时间效率

论文记录了常量/变量分析、动作抽取、指令生成、代码生成、修复和验证的 wall-clock time。默认 `<o3, Claude>` pipeline 在最终可验证系统上的 median runtime 为 **4.34 minutes per system**。论文还指出 verification 时间整体较低，主要耗时在 LLM planning / generation / repair。

### 用户研究

论文招募 20 名参与者，背景为 2-8 年计算机科学经验，其中 30% 有 PAT 或 CSP# 经验。参与者分为 control group 和 experimental group，各 10 人，并完成 4 个系统建模任务。

结果如下：

| 指标 | PAT-Agent 组均值 | 对照组均值 | p-value |
|---|---:|---:|---:|
| Time (min) | 12.85 | 17.11 | 1.16E-02 |
| Assertion Accuracy | 0.9958 | 0.7500 | 1.85E-07 |
| System Accuracy | 0.9688 | 0.6633 | 2.66E-05 |

作者据此认为，交互式界面能降低 formal modeling 和 assertion writing 的认知负担，尤其帮助没有形式化方法背景的用户。

### 方法优势

1. 把自然语言 autoformalization、模型检查和 repair loop 串成端到端闭环。
2. 不是单次 direct generation，而是通过 semantic prompts 和 planning 控制中间表示。
3. 使用 PAT 的真实 verification feedback，而不是只靠 LLM 自评或语法检查。
4. 数据集、代码、界面和实验 demo 公开，复现价值高。
5. 用户界面支持人工检查和编辑中间表示，便于非专家使用。

### 方法的局限性

1. **输出不是状态机图或 Project1 DSL**：最终工件是 PAT/CSP# 形式模型，语义上可对应 labelled transition system，但不是 UML state machine / Statechart / SysML state machine。
2. **自然语言输入质量敏感**：模糊或不完整描述会导致欠规格模型。
3. **repair heuristics 有任务偏置**：当前规则主要针对数据集中出现的 safety / liveness 类错误，不保证能泛化到所有失败类型。
4. **语言和工具绑定**：实现基于 PAT 和 CSP#，迁移到 UPPAAL、Event-B、Alloy、Petri nets 等需要重写语法提示、示例库和反馈解析。
5. **40 个系统规模仍有限**：实验覆盖多来源样例，但还不是工业级控制系统 corpus。
6. **LLM 随机性仍存在**：论文通过固定模型版本和多轮修复缓解，但没有消除生成随机性。

## 与本研究的关系

### 相关性分析

- **BASELINE评估**：🟠
- **评估理由**：PAT-Agent 的输入是自然语言系统描述，且任务包含行为模型生成、模型检查和修复闭环，和 `project_1` 的“生成-验证-修复”研究目标高度相关；但它的输出是 PAT/CSP# 形式模型与断言，不是状态机、Statechart、SysML 状态机或本项目目标 DSL，因此不能作为直接状态机生成 baseline。
- **建议类别**：需求到形式模型 / 模型检查闭环 / 验证反馈修复邻近 baseline。

### 为什么不能算直接 baseline

`project_1` 的直接 baseline 应满足“自然语言需求/描述 -> 状态机族模型”。PAT-Agent 虽然生成的 CSP# 模型在语义上会被 PAT 展开为 labelled transition system，但其用户可见输出与实验产物是 CSP# process algebra code 和 PAT assertions，而不是可比较的状态机工件。因此它不适合直接进入“状态机结构、状态/迁移/守卫/action 抽取质量”的公平对比表。

### 为什么仍然值得保留

PAT-Agent 对 `project_1` 的价值主要在方法链路，而不是输出工件：

1. 它提供了真实 formal verifier in the loop 的 LLM 建模 pipeline。
2. 它把 counterexample trace 转成 targeted repair directive，这正是状态机建模后续修复可以借鉴的核心机制。
3. 它把用户期望 `VALID/INVALID` 纳入需求定义，避免“模型检查只返回真/假但不知道用户意图”的问题。
4. 它提供公开数据集和复现实验，可作为构建 Project1 verification-feedback baseline 的参考。

### 可借鉴之处

1. **结构化 planning**：Project1 可把自然语言需求先转为 states、events、guards、actions、timing constraints 的中间 JSON，再生成目标状态机 DSL。
2. **syntax cue + RAG 示例**：可将 pyfcstm / target DSL 的语法、常见错误和已验证样例作为 code generation prompt 的稳定支撑。
3. **counterexample-guided repair**：若 Project1 后续接入 model checker，可将反例 trace 映射到可疑状态、迁移、guard 或 action，并生成局部修复提示。
4. **expected outcome 设计**：对 safety negative property，用户期望可能是不可达；这对状态机验证场景生成和 profile-based verification 都很关键。
5. **交互式中间表示审查**：非专家可以审阅 constants、variables、actions，这启发 Project1 在生成过程中暴露可编辑的模型元素表。

### 存在的不足与改进空间

1. 输出工件和 Project1 不同，无法直接比较状态机结构完整性。
2. 没有专门处理层次化状态机、并发 state regions、时间约束和控制系统领域模式。
3. 修复策略主要是 guard tightening / loosening 等启发式，尚未形成状态机元素级故障定位理论。
4. 数据集多为 PAT / Alloy / CSP 教材或样例库改编，不是控制系统自然语言需求 corpus。
5. 论文评估终点是“与用户指定 assertions 的结果匹配”，仍可能遗漏未指定性质或需求覆盖不足问题。

### 对本研究的启发

PAT-Agent 可作为 `project_1` 生成-验证-修复闭环的重要邻近参考：本研究可以保留“semantic planning + formal checker + counterexample repair”的框架，但把输出替换为控制系统状态机 DSL，并把验证 feedback 从 PAT/CSP# 反例迁移到状态机元素级错误定位、时间约束修复和安全/活性性质 profile。

## 重要的相关工作

### 1. 重要的前身类工作

- **PAT / Process Analysis Toolkit**：论文以 PAT 作为模型检查后端，并引用 PAT 的 CAV 2009 工具论文 [1] 以及 stateful timed CSP 相关工作 [2]。PAT 提供 deadlock、reachability、LTL 等 verification engine，是本文闭环的 symbolic backbone。
- **CSP / 并发系统教材**：论文评测中的 UCS 数据来自 Roscoe 的 Understanding Concurrent Systems [3]，支撑其 CSP 风格建模样例来源。
- **TLA+、Z、Isabelle 等传统形式规格**：论文在 discussion 中将自己与自然语言到主流 formal notation 的 autoformalization 工作对照，强调 CSP# 缺少公开 corpus 和 end-to-end translator。

### 2. 直接参与实验的 baseline

- **Direct R1 / o3 / Claude generation**：三种直接从自然语言生成 PAT code 的单模型 baseline，仍给 RAG 示例和语法文档；整体 FPR 分别为 0.3750、0.5250、0.4750。
- **Pipeline model combinations**：论文比较 `<o3, Claude>`、`<R1, Claude>`、`<R1, R1>`、`<R1, o3>`、`<o3, R1>`、`<o3, o3>`，说明 planner / generator 组合会显著影响结构化输出和最终验证结果。
- **Ablation variants**：Without Planning Model、Without Repair Loop、Without Both Components 是最关键的结构消融 baseline。

### 3. 提供了重要论证的工作

- **nl2spec / NL2LTL**：自然语言到 temporal logic 的 LLM autoformalization 工作 [4][5]，论文用它们说明 LLM 已能处理细粒度公式，但系统级模型合成更复杂。
- **Alloy / B-method LLM formal specification**：论文引用 Alloy 公式生成和 B-method 规格生成研究 [6][7]，并指出这些工作通常偏简单系统或 direct mapping。
- **LLM hallucination 研究**：论文引用 hallucination survey 和 LLM lies 等研究 [8][9]，作为“LLM 形式模型生成不能只靠单次输出”的论证来源。

### 4. 在技术上提供了支持的工作

- **Self-planning / plan-and-act**：论文引用 self-planning code generation 和 long-horizon agent planning [10][11]，支持其“拆分复杂生成任务”的设计。
- **Compiler feedback / code generation metrics**：CSR、FPR、APR 的评价设计与代码生成/软件工程评估文献相关 [12][13][14]。
- **Program specification synthesis and proof repair**：Baldur、LeMur、Enchanting、FVEL 等工作 [15][16][17][18] 为 LLM + formal verification / repair 的研究脉络提供背景。

### 5. 其他重要工作

- **UPPAAL、FDR、ProB、PEPA、Petri nets**：论文在 discussion 中提到 workflow 可迁移到其他 model checker 或建模语言 [19][20][21][22][23]，但需要相应语法文档、示例库和 verification feedback 适配。
- **Automated program refinement**：作者团队相关 POPL 2025 工作 [24] 关注用 refinement calculus 指导和验证 code LLM；它与 PAT-Agent 同属“LLM + formal feedback”方向，但输出目标不同。

## 文献分类总结

- **研究定位**：自然语言到可验证形式模型的 LLM agent 框架。
- **任务类型**：autoformalization；formal model generation；model checking；counterexample-guided repair；interactive formal modeling。
- **输入工件**：自然语言系统描述；用户性质及期望结果；可通过界面填写结构化 assertion 条件。
- **输出工件**：PAT/CSP# 形式模型；PAT assertions；verification results；counterexample traces；修复后的模型。
- **输出模型类型**：Process algebra / CSP# model with LTS semantics，不是状态机图或 SysML/UML state machine。
- **使用的 LLM**：默认 OpenAI `o3-mini-2025-01-31` 作为 Planning LLM，Anthropic `claude-3-7-sonnet-20250219` 作为 Code Generation LLM；实验还使用 DeepSeek-R1。
- **主要方法**：semantic prompt-based planning + RAG/example-guided formal code generation + PAT model checking + counterexample-guided repair loop。
- **需求词工程**：高｜结构化 semantic prompts、JSON-like 中间表示、PAT syntax cue、RAG one-shot exemplar、repair directives｜prompt 是整个 pipeline 的控制程序。
- **运行仿真**：低-中｜主要是 PAT verification 与反例 trace，不是连续系统仿真或 hardware-in-the-loop｜运行角色是 state-space exploration / model checking。
- **形式化验证**：高｜PAT model checking，覆盖 deadlock-freedom、reachability、LTL，并将反例用于修复｜是论文核心闭环。
- **代码/仓库是否公开**：是；公开 GitHub 仓库，非商业研究许可。
- **数据集/benchmark 是否公开**：是；`Datasets/PAT.json`、`Datasets/A4F.json`、`Datasets/UCS.json` 可直接获取。
- **BASELINE评估**：🟠
- **对 Project1 的核心价值**：不适合作为直接状态机生成 baseline，但非常适合作为“LLM 生成状态机后的形式验证反馈与迭代修复”方法参照。

## References

[1] Jun Sun, Yang Liu, Jin Song Dong, and Jun Pang. 2009. PAT: Towards Flexible Verification under Fairness. Computer Aided Verification. https://doi.org/10.1007/978-3-642-02658-4_59

[2] Jun Sun, Yang Liu, Jin Song Dong, Yan Liu, Ling Shi, and Étienne André. 2013. Modeling and Verifying Hierarchical Real-time Systems using Stateful Timed CSP. ACM Transactions on Software Engineering and Methodology. https://doi.org/10.1145/2430536.2430537

[3] Andrew W. Roscoe. 2010. Understanding Concurrent Systems. Springer. https://link.springer.com/book/10.1007/978-1-84882-258-0

[4] Matthias Cosler, Christopher Hahn, Daniel Mendoza, Frederik Schmitt, and Caroline Trippel. 2023. nl2spec: Interactively Translating Unstructured Natural Language to Temporal Logics with Large Language Models. CAV. https://doi.org/10.1007/978-3-031-37706-8_19

[5] Francesco Fuggitti and Tathagata Chakraborti. 2023. NL2LTL: A Python Package for Converting Natural Language Instructions to Linear Temporal Logic Formulas. AAAI. https://doi.org/10.1609/aaai.v37i13.26869

[6] Yang Hong, Shan Jiang, Yulei Fu, and Sarfraz Khurshid. 2025. On the Effectiveness of Large Language Models in Writing Alloy Formulas. arXiv. https://arxiv.org/abs/2502.15441

[7] Alfredo Capozucca, Daniil Yampolskyi, Alexander Goldberg, and Maximiliano Cristiá. 2025. Do AI Assistants Help Students Write Formal Specifications? A Study with ChatGPT and the B-Method. arXiv. https://arxiv.org/abs/2502.07789

[8] Ziwei Ji et al. 2023. Survey of Hallucination in Natural Language Generation. ACM Computing Surveys. https://doi.org/10.1145/3571730

[9] Jia-Yu Yao, Kun-Peng Ning, Zhen-Hui Liu, Mu-Nan Ning, and Li Yuan. 2023. LLM Lies: Hallucinations are not Bugs, but Features as Adversarial Examples. arXiv. https://arxiv.org/abs/2310.01469

[10] Xue Jiang, Yihong Dong, Lecheng Wang, Zheng Fang, Qiwei Shang, Ge Li, Zhi Jin, and Wenpin Jiao. 2024. Self-planning Code Generation with Large Language Models. ACM Transactions on Software Engineering and Methodology. https://doi.org/10.1145/3672456

[11] Lutfi Eren Erdogan, Nicholas Lee, Sehoon Kim, Suhong Moon, Hiroki Furuta, Gopala Anumanchipalli, Kurt Keutzer, and Amir Gholami. 2025. Plan-and-Act: Improving Planning of Agents for Long-Horizon Tasks. arXiv. https://arxiv.org/abs/2503.09572

[12] Mark Chen et al. 2021. Evaluating Large Language Models Trained on Code. arXiv. https://arxiv.org/abs/2107.03374

[13] Xin Wang et al. 2022. Compilable Neural Code Generation with Compiler Feedback. arXiv. https://arxiv.org/abs/2203.05132

[14] Dan Hendrycks et al. 2021. Measuring Coding Challenge Competence with APPS. arXiv. https://arxiv.org/abs/2105.09938

[15] Emily First, Markus N. Rabe, Talia Ringer, and Yuriy Brun. 2023. Baldur: Whole-Proof Generation and Repair with Large Language Models. ESEC/FSE. https://doi.org/10.1145/3611643.3616243

[16] Haoze Wu, Clark Barrett, and Nina Narodytska. 2023. LeMUR: Integrating Large Language Models in Automated Program Verification. arXiv. https://arxiv.org/abs/2310.04870

[17] Cheng Wen et al. 2024. Enchanting Program Specification Synthesis by Large Language Models using Static Analysis and Program Verification. CAV. https://doi.org/10.1007/978-3-031-65630-9_15

[18] Yuchen Zhang, Xiaoyu Wang, Qian Li, et al. 2024. FVEL: An Interactive Formal Verification Environment with Large Language Models. NeurIPS. https://arxiv.org/abs/2410.18748

[19] Gerd Behrmann, Alexandre David, and Kim G. Larsen. 2004. A Tutorial on UPPAAL. Springer. https://doi.org/10.1007/978-3-540-30080-9_7

[20] Thomas Gibson-Robinson, Philip Armstrong, Alexandre Boulgakov, and Andrew W. Roscoe. 2014. FDR3: A Modern Refinement Checker for CSP. TACAS. https://doi.org/10.1007/978-3-642-54862-8_13

[21] Michael Leuschel and Michael Butler. 2003. ProB: A Model Checker for B. FM. https://doi.org/10.1007/978-3-540-45236-2_46

[22] Jane Hillston. 1996. A Compositional Approach to Performance Modelling. Cambridge University Press. https://doi.org/10.1017/CBO9780511569951

[23] Carl Adam Petri. 1966. Communication with Automata. University of Bonn dissertation. https://catalog.hathitrust.org/Record/000678138

[24] Yufan Cai, Zhe Hou, David Sanán, Xiaokun Luan, Yun Lin, Jun Sun, and Jin Song Dong. 2025. Automated Program Refinement: Guide and Verify Code Large Language Model with Refinement Calculus. Proceedings of the ACM on Programming Languages. https://doi.org/10.1145/3704861
