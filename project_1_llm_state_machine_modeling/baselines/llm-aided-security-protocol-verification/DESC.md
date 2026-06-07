# 面向安全协议验证的LLM辅助自动建模 / LLM-Aided Automatic Modeling for Security Protocol Verification

## 基本信息

- **标题**：LLM-Aided Automatic Modeling for Security Protocol Verification
- **中文标题**：面向安全协议验证的LLM辅助自动建模
- **作者**：Ziyu Mao, Jingyi Wang, Jun Sun, Shengchao Qin, Jiawen Xiong
- **单位**：Zhejiang University; Singapore Management University; Xidian University; East China Normal University
- **发表**：2025 IEEE/ACM 47th International Conference on Software Engineering (ICSE 2025), pages 642-654
- **DOI**：10.1109/ICSE55347.2025.00197
- **链接**：[IEEE Xplore](https://ieeexplore.ieee.org/abstract/document/11029741)；[DOI](https://doi.org/10.1109/ICSE55347.2025.00197)
- **PDF来源与核验**：本轮使用用户已下载的 PDF（本目录 `paper.pdf`）；公开核验入口为 IEEE Xplore / DOI，核验日期 2026-06-07。

**代码/仓库获取方式**：
- 原文声明 tool implementation、benchmark、experiment data 和 extended paper version 均公开在 GitHub：
  - [GitHub: zerrymore/AutoSM](https://github.com/zerrymore/AutoSM)
- 本轮已用 `git ls-remote https://github.com/zerrymore/AutoSM.git` 核验 GitHub 仓库可访问；核验时间为 2026-06-07。

**数据集获取方式**：
- 原文声明 benchmark、实验数据和工具实现同样发布在上述 GitHub 仓库。
- benchmark 包含 18 个真实安全协议案例，每个案例围绕自然语言协议描述、SAPIC+ 规格和 Tamarin 模型组织；构造时还使用了 Tamarin GitHub 仓库中的已有模型作为来源之一。

## 简报

**解决的问题**：论文面向安全协议符号验证中的建模瓶颈，尝试从自然语言安全协议文档自动生成可交给协议验证器使用的符号模型。它不是直接生成状态机图，而是生成专用 lambda calculus 中间表示，经修复、重写和编译后得到 SAPIC+ 规格以及 Tamarin / ProVerif / DeepSec 可用的符号协议模型。

- **输入**：
  - 安全协议的自然语言文档片段，例如 RFC、论文段落、Tamarin manual、教学材料或非正式协议描述。
  - 必要时包含人工分块后的 protocol chunks。
  - 在工具部署场景中，修复阶段允许轻量用户交互来消解歧义。

- **方法**：
  - 使用 LLM 作为 CCG parser，把协议文档逐块解析为专用 $\lambda$-DSL 表达式。
  - 用 LLM self-validation、静态分析和可选用户交互修复中间模型。
  - 用形式化重写规则把 well-formed $\lambda$-DSL 转为 SAPIC+。
  - 通过 SAPIC+ 编译到 Tamarin、ProVerif、DeepSec 等协议验证器。
  - 通过 trace inclusion 和 SAPIC+ 编译正确性讨论生成模型的可信性。

- **输出**：
  - 专用 lambda calculus 协议规格。
  - 修复后的 well-formed lambda 规格。
  - SAPIC+ 协议规格。
  - Tamarin / ProVerif / DeepSec 后端可验证的符号协议模型。
  - 在 Tamarin 上验证 secrecy、authentication 等安全性质的结果。

```
自然语言协议文档
        |
        v
L-CCG: LLM 逐块语义解析
        |
        v
lambda calculus draft
        |
        v
L-Repair: LLM self-validation + 静态分析 + 可选人工消歧
        |
        v
well-formed lambda specification
        |
        v
Rewriter: lambda -> SAPIC+
        |
        v
Compiler: SAPIC+ -> Tamarin / ProVerif / DeepSec
        |
        v
符号协议模型 + 安全性质验证结果
```

**实验结果总结**：论文构建了 18 个协议的 benchmark，在无人工交互、每个协议运行 5 次的整体评估中，正文 headline 结果为生成 10/18 个正确 symbolic models；Table IV 同时给出更细的 per-protocol success ratio，存在 12 个协议有非零或 `✓` 记录，因此引用时应区分“正文 headline 成功数”和“Table IV 部分运行成功/非零成功率”两个口径。对比 few-shot 直接生成，3-shot baseline 最多成功 4 个案例。中间解析评估中，GPT-4 的平均 exact coverage 为 56.36%，平均 bounded expression rate 为 80.47%；自动修复在复杂案例上仍不足，GPT-4 平均只降低 14.74% 错误，因此部署工具保留了用户交互。

**结论与不足**：论文证明“直接让 LLM 写 Tamarin/SAPIC+ 模型”不可靠，更可行的路线是把 LLM 限制在语义解析与局部修复环节，把可验证工件生成交给受形式化语义约束的中间表示、重写规则和编译器。局限在于：案例规模仍远小于 TLS 1.3 / 5G AKA 等真实大型协议；复杂文档存在长距离、非顺序依赖；$\lambda$-DSL 只覆盖 SAPIC+ 的核心子集；结果依赖 GPT-4 这类闭源强模型，存在 provider drift 与可复现风险。

## 研究问题与动机

### 问题背景

Tamarin、ProVerif、DeepSec 等符号协议验证器已经用于 TLS 1.3、5G AKA、EMV payment 等真实协议分析，并能发现细微安全漏洞。但这些工具要求用户先把协议文档抽象为精确的符号模型，再用一阶逻辑或相应规格语言编码待验证性质。论文指出，这个建模阶段既需要协议专业知识，也需要熟悉验证器建模语言和工具惯例。

论文用若干代表性工作说明建模成本：TLS 1.3 Draft 21 文档约 143 页，符号模型超过 2000 行；5G AKA 相关 3GPP TS 文档约 722 页，7 个模型超过 4000 行；EMV 规范超过 2000 页，对应 40 个模型、超过 2000 行。作者认为当前大量工作关注 reasoning / proving 阶段，而 modeling 阶段自动化不足。

### 核心问题

论文要解决的问题可以概括为：

1. 如何从自然语言安全协议描述中抽取足够精确的协议行为语义。
2. 如何避免 LLM 直接生成形式化协议模型时的幻觉、语法错误和语义偏差。
3. 如何让中间结果对人类足够直观，便于轻量确认和消歧。
4. 如何保证从中间模型到最终验证器输入模型的转换具有可解释的形式化可信性。

### 研究动机

作者明确反对把任务简单看成“代码生成”。原因有两点：

1. 形式化协议建模语言的训练样本远少于 Python 等通用编程语言，LLM 对 SAPIC+ / Tamarin 这类 DSL 不熟悉。
2. 符号模型用于形式化验证，输出必须精确；一个未绑定变量、错误消息结构或错误角色归属都可能导致验证结论失真。

因此，论文的基本设计思想是：LLM 不直接承担最终模型合成，而是承担自然语言语义解析和局部修复；最终可验证模型由形式化中间语言、静态分析、重写规则和已有编译链路逐层生成。

### 研究意义

这篇论文对自动形式化建模有三点意义：

1. 把 LLM 用于 formal verification 的 P1 阶段，即 formal model construction，而不是只用于性质生成或定理证明。
2. 提供了一个“LLM 解析 + 形式化中间表示 + 修复 + 编译 + 验证”的闭环范式。
3. 发布了面向 symbolic protocol model generation 的 18 协议 benchmark，为后续方法比较提供了统一任务。

### 与 Project1 任务的距离

该论文输入是自然语言文档，方法也包含 LLM、修复反馈和形式化验证，但输出不是控制系统状态机、Statechart、SysML 状态机或 Mermaid/Umple 状态机，而是安全协议符号模型。Tamarin 的 multiset rewriting rules 可刻画 labeled transition system，SAPIC+ 也可编译到后端验证模型，但论文目标工件仍是协议验证模型，不是 Project1 所需的状态机族模型。因此它应被视为邻近形式化建模 baseline / 方法参照，而不是直接状态机生成 baseline。

## 核心方法

### 方法概述

方法由四个阶段组成：

1. **L-CCG**：LLM-powered CCG parser，把协议文档解析为专用 lambda calculus 表达式。
2. **L-Repair**：结合 LLM self-validation、LLM view rewriting、静态分析和可选用户交互，把 broken specification 修成 well-formed specification。
3. **Rewriter**：把修复后的 lambda expressions 转换为 SAPIC+ role processes 和 top specification。
4. **Compiler**：用 SAPIC+ 工具链编译到 Tamarin、ProVerif、DeepSec 的输入模型。

作者的关键设计选择是：把 LLM 放在“抽取 necessary ingredients”的位置，而不是让 LLM 直接输出最终验证器模型。

### 专用 $\lambda$-DSL

论文设计了一个面向安全协议的 lambda calculus DSL，用来表示协议中的关键事件。核心事件包括：

- `gen(a, n)`：agent 生成 fresh nonce。
- `send(a, m)`：agent 通过公共信道发送消息。
- `recv(a, m)`：agent 接收消息。
- `know(a, t)`：agent 初始知道某些 terms。
- `op(a, f(t))`：本地操作、term binding 或 signal event。

该 DSL 的好处是比 SAPIC+ / Tamarin 更接近自然语言句子，也比自然语言更适合做静态检查和重写。论文为 DSL 定义了 protocol specification、protocol instance、configuration、trace 等语义对象，并用 operational semantics 描述事件执行。

### L-CCG：LLM 作为语义解析器

L-CCG 的输入是 protocol document，输出是 lambda calculus expressions。由于安全协议文档较长，作者没有把整篇文档一次性送入模型，而是：

1. 把文档顺序切分为 chunks。
2. 对每个 chunk 保留相邻若干 chunk 及其已生成 lambda expressions 作为上下文。
3. 用 few-shot in-context learning 提示 LLM 为当前 chunk 生成 lambda expressions。
4. 逐块累积解析结果。

这一路线专门应对 “lost in the middle” 问题，并让 LLM 聚焦局部上下文。论文说明 prompt 会指导 LLM 编写 lambda expressions，所有 prompts 在公开工件中提供。

### L-Repair：修复 draft model

论文把初始模型常见问题分为三类：

1. **Inconsistency**：LLM 幻觉或随机性导致表达式偏离协议文档，例如消息结构错误或发送角色错误。
2. **Ambiguity**：自然语言省略常识或指代不清，导致变量未绑定。
3. **Unreadability**：接收事件从全局视角写成了接收方无法 pattern match 的消息结构。

L-Repair 对应三类处理：

- 用 LLM self-validation 对照自然语言和 lambda expressions 找错并修正。
- 用 diff 格式示例提示 LLM 把 receive message 转为接收角色可读形式。
- 用基于 Lark parser 的静态分析检测 unbounded variables。
- 在工具模式中，把 message sequence chart 和未绑定变量报告展示给用户，让用户直接编辑中间结果。

整体评估时，作者刻意不引入用户交互，以测试自动化上限；工具实现中则保留轻量交互，因为复杂协议自动修复不足。

### Rewriter：从 lambda calculus 到 SAPIC+

Rewriter 使用规则 $T$ 把每个 role specification 转换为 SAPIC+ local process：

- `know` 转为 local process signature。
- `gen` 转为 `new`。
- `send` 转为 `out`。
- `recv` 转为 `in`。
- `op(..., binds(...))` 转为 `let` binding。
- 其他 `op` 转为 SAPIC+ event。

top specification 的合成还需要收集 local process signatures，并用 few-shot learning 指导 LLM 生成 SAPIC+ 的 top process 初始化部分。

### Compiler 与验证后端

SAPIC+ 作为统一中间规格语言，可编译到三个主流后端：

- Tamarin
- ProVerif
- DeepSec

实验实际运行生成模型时使用 Tamarin prover 1.8.0，其中包含 SAPIC+ platform。模型验证的性质包括 secrecy、authentication 等基础安全性质。

### 正确性与可信性设计

论文的可信性讨论依赖两个层次：

1. 从 $\lambda$-DSL 到 SAPIC+ 的 rewriting soundness：作者建立 trace inclusion 关系，直觉是 lambda specification 的全局事件顺序约束蕴含 SAPIC+ role-local 顺序，因此 SAPIC+ 上成立的 safety trace property 可转移到 lambda specification。
2. SAPIC+ 到后端验证器模型的 compilation soundness：引用 SAPIC+ 论文中已证明的编译正确性。

由此得到直观保证：如果后端模型满足相应 safety trace property，则 SAPIC+ 模型与 lambda DSL 模型也具有相应安全性质保证。需要注意的是，这种保证覆盖形式化模型之间的转换，不等价于证明自然语言文档到 lambda draft 的 LLM 解析完全正确；自然语言到中间表示仍需 validation、静态分析和必要的人类确认。

### LLM / Agent 形态

论文没有使用多智能体协作框架，而是把 LLM 嵌入固定 pipeline 的多个函数中：

- `Parse(ctx, chunk)`：few-shot 语义解析。
- `Validate(P, nl)`：对照文档 self-validation。
- `View(P)`：把接收消息改写为可读形式。
- top specification synthesis：生成 SAPIC+ top specification。

实验使用的模型包括 GPT-3.5-turbo、GPT-4、GPT-4o、Google Gemini-pro，semantic parsing 和 automated repairing 的 temperature 均为 0.4。论文报告 GPT-4 在解析中表现最好，但也指出对闭源 GPT-4 的依赖是外部有效性威胁。

## 实验与评估

### 数据集 / Benchmark

论文包含两类评估数据：

1. **中间语言解析评估数据**：
   - 使用多个协议文档片段评估 L-CCG 是否能抽取 lambda expressions。
   - 文档来源包括 IETF RFC、学术论文、Tamarin manual、Wikipedia、teaching assignment 和 informal texts。
   - 表 II / 表 III 涉及 NSPK、Toy、NSSK、NAXOS、Otway-Rees、SSH、IKEv2、KEMTLS、EDHOC 等协议。

2. **整体方法 benchmark**：
   - 18 个协议案例。
   - 每个 benchmark 条目是自然语言协议文档、SAPIC+ specification、Tamarin model 的组合。
   - 构造流程从 Tamarin GitHub 仓库已有模型出发，抽取或重写对应自然语言文档，再手工构建 SAPIC+ 模型并确保其与 Tamarin 模型在给定安全性质上等价。
   - 论文排除 TLS 1.3、5G AKA 等超大规模协议，聚焦 manageable scale 案例。

18 个整体 benchmark 协议包括：example、Toy、NSPK、NSSK、SigFox、LAKE、NAXOS、X509.1、SSH、EDHOC、KEMTLS、Yahalom、Kao Chow、SPLICE/AS、Otway Rees、Woo and Lam、Denning-Sacco、Stubblebine。

### 评估指标

中间语言解析评估使用：

- **Exact Coverage (EC)**：生成表达式覆盖 ground truth 的比例。
- **Bounded Expressions Rate (BER)**：变量已绑定、可进一步重写的表达式比例。
- **Error Rate (ER)**：表达式错误率，包括额外表达式和错误表达式。
- 论文还讨论 $\delta_e = EC / BER$，用来反映自然语言描述相对符号模型的具体程度。

整体 benchmark 评估使用：

- 生成模型是否通过所有给定安全性质。
- 每个协议运行 5 次，记录 success ratio。
- 给定性质包括 secrecy、authentication 等。
- 语义等价采用近似口径：两个模型在同一性质上都满足，则认为相对于该性质等价。

### 实验设置

- LLM：GPT-3.5-turbo、GPT-4、GPT-4o、Google Gemini-pro。
- temperature：0.4。
- 后端验证：Tamarin prover 1.8.0，含 SAPIC+ platform。
- 整体 benchmark：每个协议运行 5 次，不允许用户交互。
- 对比 baseline：直接 few-shot learning，包括 0-shot、1-shot、2-shot、3-shot。

### 主要实验结果

解析评估：

- GPT-4 在多个模型中表现最好。
- GPT-4 平均 EC 为 56.36%，平均 BER 为 80.47%。
- 小规模且描述明确的协议，如 NSSK、Otway-Rees，lambda expressions 能较好捕获语义，EC 超过 54.55%，BER 超过 78.26%。
- 复杂协议如 IKEv2、EDHOC、KEMTLS 的 EC 较低，因为文档不总是自包含，存在省略、长距离依赖和抽象描述。

修复评估：

- 自动修复依赖 advanced LLM。
- 对复杂案例，自动修复不足以消除全部问题。
- GPT-4 平均降低 14.74% 错误。
- 这也是工具部署中引入用户交互的原因。

整体 benchmark：

- 18 个协议中，方法在 10 个协议上能自动生成正确模型。
- 论文摘要和正文主结论写为“10/18 个协议生成正确模型”；同时 Table IV 中有 12 个协议标记为 `✓` 或出现非零 success ratio（example、Toy、NSPK、NSSK、SigFox、LAKE、X509.1、Yahalom、Kao Chow、Otway Rees、Woo and Lam、Denning-Sacco），其中多项低于 5/5。因此本 DESC 采用 10/18 作为 headline 结果，并把 Table IV 视为含“部分运行成功/非零成功率”的细分口径，避免把 12 项都误写为最终 headline 成功数。
- 失败案例包括 NAXOS、SSH、EDHOC、KEMTLS、SPLICE/AS、Stubblebine。
- 输入文本大小为 51 到 639 tokens。
- SAPIC+ LoC 约 30 到 163，Tamarin model LoC 约 44 到 722。
- few-shot baseline 最多成功 4 个案例，本文方法按正文 headline 成功 10 个案例；Table IV 的非零 success-ratio 细分口径需在引用时单独说明。

### 方法优势

1. **不让 LLM 直接生成最终形式化模型**：降低了符号语言不熟悉和幻觉带来的风险。
2. **中间表示可检查**：lambda expressions 能暴露 unbounded variables、unreadable messages 等问题。
3. **保留人类可理解性**：中间结果比 Tamarin / SAPIC+ 更接近协议文本，适合轻量审查。
4. **转换链路有形式化支撑**：lambda 到 SAPIC+ 的重写规则和 SAPIC+ 编译链路共同支撑可信性讨论。
5. **公开 benchmark 与工具**：论文声明公开 18 协议 benchmark、工具实现和实验数据，利于后续比较。

### 方法的局限性

1. **规模差距**：benchmark 聚焦中等规模协议，与 TLS 1.3、5G AKA 这类真实大型协议仍有距离。
2. **文档自包含假设较强**：复杂协议文档常包含跨章节、跨标准和非顺序依赖，当前 chunk-by-chunk parsing 容易遗漏。
3. **DSL 表达能力有限**：作者承认 $\lambda$-DSL 只覆盖 SAPIC+ 的核心特性，不等价于完整 SAPIC+。
4. **仍需人工消歧**：自动修复对复杂案例不足，工具实践中需要用户编辑中间结果。
5. **闭源模型依赖**：结果依赖 GPT-4 等 advanced closed-source LLM，模型更新会影响可复现性。
6. **性质等价较弱**：整体 correctness 以给定 safety properties 是否都通过为准，类似测试通过，不是完整语义等价。

## 与本研究的关系

### 相关性分析

**BASELINE评估**：🟠

理由如下：

1. 它的输入是自然语言协议文档，这一点与 Project1 的“自然语言需求/描述 -> 形式模型”方向相近。
2. 它使用 LLM、分阶段中间表示、修复反馈、验证器后端和公开 benchmark，这些都对 Project1 的生成-验证-修复闭环有参考价值。
3. 但输出不是状态机、Statechart、SysML 状态机或控制系统行为模型，而是安全协议符号模型、SAPIC+ 规格和 Tamarin / ProVerif / DeepSec 后端模型。
4. 目标领域是安全协议验证，不是控制系统状态机建模；输入文档、建模语义和验证性质都不同。

因此它不能作为 Project1 的直接 baseline，但适合作为“LLM 辅助形式化模型生成 + 验证反馈”的邻近方法参照。

### 可借鉴之处

1. **中间 DSL 设计**：Project1 可以考虑先生成可检查的中间状态机 DSL，再编译到 pyfcstm / UPPAAL / 其他验证器，而不是直接让 LLM 输出最终模型。
2. **LLM 角色收缩**：让 LLM 只负责语义抽取、局部消歧和候选修复，关键转换由确定性程序完成。
3. **静态 diagnostics 反馈**：unbounded variables、unreadability、inconsistency 对应 Project1 中的未定义状态、未绑定事件、不可达迁移、guard/action 不一致等结构化诊断。
4. **验证器驱动 eligibility**：只有通过指定性质或诊断 gate 的模型进入主结果统计，失败运行也保留为审计证据。
5. **benchmark 三元组**：自然语言输入、标准中间模型、验证器模型的组织方式，可迁移为 Project1 的“需求文本、参考状态机、验证/仿真工件”三元组。
6. **可解释修复界面**：用 MSC / 图形视图 + 静态错误报告帮助人类修复中间结果，可借鉴到状态机图或 transition table 的交互式修复。

### 存在的不足与改进空间

1. 对 Project1 而言，SAPIC+ / Tamarin 的协议语义不能直接覆盖控制系统的时间约束、层次状态、并发区域、I/O action 和 guard semantics。
2. 论文的 verification feedback 主要是符号协议性质验证，不包含控制系统仿真、时间自动机 reachability 或状态机结构质量评审。
3. 自动修复效果仍有限，复杂案例需要人类参与；这说明 Project1 若要做闭环修复，不能只依赖 LLM self-validation。
4. benchmark 输入 token 较短，尚不能代表长篇控制需求文档或工业规范。
5. 正确性保证主要覆盖中间模型到后端模型，不覆盖自然语言到中间 DSL 的完全正确性；Project1 仍需 human review、reference model 或 LLM-as-Judge 评估补充。

### 对本研究的启发

该论文最有价值的启发不是“生成什么模型”，而是“如何把 LLM 生成正式模型这件事拆成可验证的工程链路”：

1. 先设计一个足够贴近自然语言、又可做静态分析的中间表示。
2. 对中间表示定义 well-formedness，而不是只看最终模型是否能渲染。
3. 把 LLM 输出限制在容易审查的层面。
4. 用确定性 rewriter / compiler 接管最终模型构造。
5. 用验证器结果和结构化 diagnostics 作为修复反馈与主结果 eligibility gate。

这与 Project1 的“生成-验证-修复”全生命周期目标高度一致，但任务产物不同，因此只能评为 🟠 邻近基线。

### 比较字段抽取

- **输入**：自然语言安全协议描述文档；经人工或工具分块后的 protocol chunks；可选用户交互修复信息。
- **输入形态**：自然语言 + 局部上下文 chunks；来源包括 RFC、论文、manual、Wikipedia、教学材料和非正式文本。
- **输出**：lambda calculus 中间规格、SAPIC+ 规格、Tamarin / ProVerif / DeepSec 可用符号协议模型。
- **输出模型类型**：symbolic protocol model；SAPIC+ process；Tamarin multiset rewriting rule model；不是状态机族模型。
- **使用的LLM**：GPT-3.5-turbo、GPT-4、GPT-4o、Google Gemini-pro。
- **主要方法**：LLM 语义解析 + 静态分析/LLM 修复 + lambda-to-SAPIC+ 重写 + SAPIC+ 编译 + Tamarin 性质验证。
- **few-shot / CoT / RAG / 自动反馈 / 修复闭环**：使用 few-shot in-context learning；使用 LLM self-validation；使用 diff examples 引导修复；无 RAG 证据；无多智能体。
- **形式化验证 / 模型检查 / 仿真 / 约束注入**：高；生成模型在 Tamarin 上验证 secrecy / authentication 等性质；方法本身讨论 trace inclusion 与 SAPIC+ compilation soundness。
- **是否面向控制系统或安全关键系统**：面向安全协议与信息安全验证，不面向控制系统；属于安全关键形式化分析邻近方向。
- **数据集/benchmark 是否公开**：原文声明公开，链接为 [GitHub: zerrymore/AutoSM](https://github.com/zerrymore/AutoSM)。
- **代码/仓库是否公开**：原文声明公开，链接同上。
- **BASELINE评估**：🟠。

## 重要的相关工作

### 1. 重要的前身类工作

**Semi-automated protocol disambiguation and code generation (Yen et al., 2021)**  
论文引用该工作作为 lambda calculus 启发来源之一。它说明自然语言协议描述存在歧义，需要中间表示和半自动消歧，这与本文的 L-Repair 和用户交互设计直接相关。

**Operational semantics of security protocols (Cremers and Mauw, 2005)**  
本文的协议执行语义、well-formedness 和 role/thread 视角继承了安全协议操作语义传统，为 $\lambda$-DSL 的 formal execution model 提供理论支撑。

**SAPIC+: Protocol Verifiers of the World, Unite! (Cheval et al., 2022)**  
SAPIC+ 是本文后端转换链路的关键基础。本文选择先转 SAPIC+，再利用其可编译到 Tamarin、ProVerif、DeepSec 的能力，避免为每个验证器单独生成模型。

### 2. 直接参与实验的 baseline

**Few-shot learning baseline**  
论文把直接 few-shot prompting 作为主要 LLM baseline，包括 0-shot、1-shot、2-shot、3-shot。结果显示 3-shot 最多成功 4 个协议，而本文方法成功 10 个协议，说明简单 prompt 不足以生成可靠符号模型。

**Converting Alice&Bob protocol specifications to Tamarin (Keller and Basin, 2014)**  
论文选取该 correct-by-construction 方法作为补充比较对象。作者为 4 个协议手工构造 Alice&Bob specification 输入，并比较生成的 Tamarin 模型在给定性质上的等价性。结论是该方法和本文方法在这些性质上都能通过验证，但 Alice&Bob 方法要求结构化协议规格，而本文从自然语言文档出发。

### 3. 提供了重要论证的工作

**Tamarin prover (Meier et al., 2013)**  
Tamarin 是本文主要后端验证器，也是实验运行平台。论文把 Tamarin 建模难度作为研究动机之一，同时用 Tamarin 1.8.0 验证生成模型。

**ProVerif (Blanchet, 2001) 与 DeepSec (Cheval et al., 2018)**  
这两个工具与 Tamarin 一起构成 SAPIC+ 可面向的主流协议验证器生态，说明本文生成目标不是单一工具脚本，而是可跨验证器复用的符号协议规格。

**TLS 1.3、5G AKA、EMV 的符号分析工作**  
论文引用这些真实案例说明符号协议验证能发现关键漏洞，但人工建模成本高。它们不参与本文 benchmark，却构成“为什么要自动化建模”的核心论据。

### 4. 在技术上提供支持的工作

**Lost in the Middle (Liu et al., 2024)**  
论文用该工作解释长上下文中间信息容易被 LLM 忽略，因此采用 chunk-by-chunk parsing 和局部上下文机制。

**Language Models are Few-Shot Learners (Brown et al., 2020)**  
本文的 L-CCG parsing、repair prompt 和 top specification synthesis 都使用 few-shot in-context learning。

**Enhancing static analysis for practical bug detection: An LLM-integrated approach (Li et al., 2024)**  
论文引用该工作作为 LLM self-validation 思路来源之一，即让 LLM 对照输入与候选输出检查和修正问题。

**Lark parser**  
L-Repair 中的 `Analysis` 函数使用 Lark parser 根据 BNF 得到 AST，并检测 unbounded variables。这是结构化 diagnostics 的具体实现基础。

### 5. 其他重要工作

**NL2Spec 与交互式 temporal specification synthesis**  
论文把 LLM-aided formal verification 分为 P1 formal model construction、P2 formal specification writing、P3 proving。NL2Spec、NL2TL 和 temporal specification synthesis 主要支撑 P2，而本文强调自己聚焦 P1。

**自动定理证明中的 LLM 工作**  
LeanDojo、DT-Solver、generative language modeling for theorem proving 等工作支撑 P3。本文与它们互补：不是帮 prover 证明，而是帮用户构建可被 prover 分析的模型。

## 文献分类总结

这篇论文位于“自然语言到形式化验证模型自动构造”的研究链条上。它与 Project1 同样面对非形式化文本到高可信形式模型的鸿沟，但目标不是控制系统状态机，而是安全协议符号模型。论文最突出的贡献是把 LLM 能力限制在语义解析和局部修复阶段，并用形式化中间表示、静态分析、重写规则、SAPIC+ 编译和 Tamarin 验证构成一个较完整的证据链。

从 baseline 体系看，它应归为 🟠 弱相关/邻近形式化建模工作：不能直接作为状态机生成对比方法，但非常适合作为 Project1 方法架构、run record schema、diagnostic-driven repair、benchmark eligibility 和验证反馈闭环设计的参考样本。

## References

[1] Ziyu Mao, Jingyi Wang, Jun Sun, Shengchao Qin, and Jiawen Xiong. 2025. LLM-Aided Automatic Modeling for Security Protocol Verification. ICSE 2025. https://doi.org/10.1109/ICSE55347.2025.00197

[2] Simon Meier, Benedikt Schmidt, Cas Cremers, and David Basin. 2013. The Tamarin Prover for the Symbolic Analysis of Security Protocols. CAV 2013. https://doi.org/10.1007/978-3-642-39799-8_48

[3] Bruno Blanchet. 2001. An Efficient Cryptographic Protocol Verifier Based on Prolog Rules. CSFW 2001. https://doi.org/10.1109/CSFW.2001.930138

[4] Matthew Keller and David Basin. 2014. Converting Alice&Bob Protocol Specifications to Tamarin. ETH Zurich technical report. https://doi.org/10.3929/ethz-a-010234219

[5] James Yen, Tamas Levai, Qianru Ye, Xiang Ren, Ramesh Govindan, and Barath Raghavan. 2021. Semi-automated Protocol Disambiguation and Code Generation. SIGCOMM 2021. https://doi.org/10.1145/3452296.3472909

[6] Vincent Cheval, Charlie Jacomme, Steve Kremer, and Robert Künnemann. 2022. SAPIC+: Protocol Verifiers of the World, Unite! USENIX Security 2022. https://www.usenix.org/conference/usenixsecurity22/presentation/cheval

[7] Vincent Cheval, Steve Kremer, and Itsaka Rakotonirina. 2018. DeepSec: Deciding Equivalence Properties in Security Protocols Theory and Practice. IEEE S&P 2018. https://doi.org/10.1109/SP.2018.00019

[8] Cas Cremers and Sjouke Mauw. 2005. Operational Semantics of Security Protocols. Scenarios: Models, Transformations and Tools. https://doi.org/10.1007/11495628_4

[9] Nelson F. Liu, Kevin Lin, John Hewitt, Ashwin Paranjape, Michele Bevilacqua, Fabio Petroni, and Percy Liang. 2024. Lost in the Middle: How Language Models Use Long Contexts. TACL 2024. https://doi.org/10.1162/tacl_a_00638

[10] Tom B. Brown et al. 2020. Language Models are Few-Shot Learners. NeurIPS 2020. https://proceedings.neurips.cc/paper/2020/hash/1457c0d6bfcb4967418bfb8ac142f64a-Abstract.html

[11] Haonan Li, Yu Hao, Yizhuo Zhai, and Zhiyun Qian. 2024. Enhancing Static Analysis for Practical Bug Detection: An LLM-integrated Approach. PACMPL/OOPSLA 2024. https://doi.org/10.1145/3689759

[12] Matthias Cosler, Christopher Hahn, Daniel Mendoza, Frederik Schmitt, and Caroline Trippel. 2023. nl2spec: Interactively Translating Unstructured Natural Language to Temporal Logics with Large Language Models. CAV 2023. https://doi.org/10.1007/978-3-031-37706-8_19

[13] Tamarin Prover Team. Tamarin Prover. https://github.com/tamarin-prover/tamarin-prover

[14] Lark contributors. Lark: A Modern Parsing Library for Python. https://github.com/lark-parser/lark

