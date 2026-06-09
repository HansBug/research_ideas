# 从需求使用 GPT 4.0 设计 FSM 规格 / Designing FSMs Specifications from Requirements with GPT 4.0

## 基本信息

- **标题**：Designing FSMs Specifications from Requirements with GPT 4.0
- **中文标题**：从需求使用 GPT 4.0 设计 FSM 规格
- **作者**：Omer Nguena Timo, Paul-Alexis Rodriguez, Florent Avellaneda
- **单位**：Université du Québec en Outaouais；Université Paris-Saclay；Université du Québec à Montréal
- **发表**：arXiv preprint arXiv:2603.29140, 2026
- **DOI**：原文未提供 DOI
- **链接**：https://arxiv.org/abs/2603.29140

**代码/仓库获取方式**：
- 原文提到作者实现了 Python prototype，用于调用 GPT-4 API、生成随机 DFSM oracle、生成英文描述、执行语法/语义比较和修复实验，但正文与参考文献未提供公开代码或仓库获取链接。

**数据集获取方式**：
- 原文未提供公开数据集获取链接。实验数据为作者用 Python 模块随机生成的 DFSM oracle 及其英文描述；附录给出部分自然语言生成 pattern，但没有发布完整 oracle/description 数据文件。

## 简报

**解决的问题**

本文研究如何把英文需求描述自动转换为确定性 Mealy 型有限状态机规格，并在 LLM 生成结果有错误时，用测试/诊断信息辅助修复。

- **输入**：合成生成的英文自然语言 DFSM 描述；每条描述由若干句转移描述组成，说明源状态、输入、输出和目标状态。
- **方法**：用 GPT-4/GPT-4o prompt 生成 CSV 格式 DFSM，再用 oracle DFSM 对生成结果做语法差异、语义差异、checking sequence 和 fault-model repair 分析。
- **输出**：CSV 表示的 DFSM，字段为 `State,Input,Output,Next_State`；修复阶段输出修改后的 DFSM 或 repair failure。

```text
输入层：英文 DFSM 需求描述 + 输出格式约束
  ↓
方法层：GPT-4/GPT-4o prompt 生成 CSV DFSM
  ↓
评估/修复层：oracle 比较 → 语法 fault / distinguishing sequence / checking sequence / mutation-machine repair
  ↓
输出层：候选 DFSM 规格 + 修复结果 + 错误类型统计
```

**实验结果总结**：作者用 5、10、25 状态的随机 DFSM 进行模拟实验。GPT-4o 在 5 状态机器上错误较少，在 10 状态机器上错误明显增加；常见错误是 missing transition 和 output fault。基于显式语法 fault 的修复在实验表中达到 100% 成功率；基于 distinguishing sequence 的 10 状态修复成功率为 0%；checking sequence 方法在 5 状态错误样本上成功率为 40%；基于 fault model / mutation machine 的方法在 5 和 10 状态修复实验中达到 100%，但该实验有 oracle 支持且部分 repair domain 被特定转移增强。

**研究动机**

形式化状态机规格支撑分析、代码生成、测试、验证和维护，但从自然语言需求手工设计 FSM 耗时且依赖专家。LLM 有望承担初始规格生成，但生成结果可能存在语法和语义错误，因此必须研究如何检测、分类和修复这些错误，而不能只报告“LLM 可以生成状态机”。

**方法创新**

1. 把 `NL description -> DFSM CSV` 明确设计成可执行状态机规格生成任务，而不是泛 UML 生成。
2. 通过随机 oracle DFSM 与自动英文描述生成，构造可控实验环境，允许精确比较 LLM 生成 FSM 与 oracle 行为。
3. 把 FSM testing 中的语法 fault、distinguishing sequence、checking sequence、mutation machine / fault model 迁入 LLM 生成规格修复场景。
4. 明确比较不同 repair feedback 对 GPT-4 的作用，指出直接塞入大量行为 trace 并不一定有效。

**实验设计**

- 随机生成 oracle DFSM；每个 oracle 自动转成英文描述。
- 用 GPT-4.0/GPT-4o 在温度 0.0 下生成 CSV DFSM。
- 评价生成机器与 oracle 的语法差异和语义差异。
- 分别测试四类 repair：语法 fault prompt、distinguishing input-output sequences、checking sequence、fault-model repair domain。

**结论与不足**

论文给出非常直接的 STM baseline：自然语言描述输入，FSM-family 输出，LLM 是核心生成组件。但数据是合成描述，缺少真实控制系统/工业需求；修复实验大量依赖 oracle 或专家回答，代码与数据未公开，且没有把生成 FSM 接入 UPPAAL、NuSMV 等模型检查工具。

## 研究问题与动机

### 问题背景

论文把 FSM 视为反应式系统的可执行形式规格。它关注的是 Mealy machine / DFSM 这类较抽象的状态-输入-输出-迁移模型，而非 UML Statechart 的层次、并发或时间扩展。形式化定义中，FSM 可写为：

$$
S = (S, s_0, X, Y, T)
$$

其中 $S$ 是状态集，$s_0$ 是初始状态，$X$ 与 $Y$ 分别是输入和输出集合，$T \subseteq S \times X \times Y \times S$ 是转移关系。本文要求生成机器 complete and deterministic。

### 核心问题

核心问题不是简单问 GPT 能否画出状态图，而是：

1. 给定英文状态机描述，GPT-4 能否生成结构化 DFSM 规格？
2. 当生成 DFSM 与期望机器存在差异时，如何客观识别 fault？
3. 哪类反馈最适合辅助修复：显式转移差异、输入输出 trace、checking sequence，还是 fault-model repair domain？

### 研究动机

作者指出，完整自动化规格设计可能困难甚至不可判定，实际可行路线往往是部分自动化并引入专家知识。LLM 可以快速生成近似 FSM，但质量风险会传递到测试、验证和生产系统。因此，围绕 LLM 输出的 fault diagnosis 与 repair 才是让 LLM 进入 MDE 状态机建模的关键。

### 现有方法的局限性

论文讨论了 LLM 生成 OCL、Verilog/HDL、测试等邻近工作，但指出相关工作通常没有研究 LLM 生成规格的自动修复。传统 FSM testing 已有 distinguishing sequence、checking sequence 和 fault model 方法，但这些方法尚未充分用于 LLM-based specification design。

## 核心方法

### 方法概述

整体 pipeline 分为三层：

1. **数据生成层**：随机生成 DFSM oracle；再用模板把每条转移转成英文句子，形成自然语言描述。
2. **LLM 生成层**：用系统角色和用户 prompt 要求 GPT-4o 输出固定 CSV 格式，且强调机器应 complete and deterministic。
3. **评估/修复层**：把生成 CSV 解析为 DFSM，与 oracle 做语法和语义比较；若错误则把 fault evidence 转成新 prompt 或进入 fault-model repair。

### Prompt 与输出格式

正文 Listing 1.2 给出关键 prompt：系统角色把模型设为“从自然语言描述生成 FSM CSV 的专业软件工程师”；用户 prompt 包含完整英文描述，并强制输出顺序 `State,Input,Output,Next_State`，状态名为 `Si`，不允许附加注释。正文代码片段显示模型字段为 `gpt-4o`，temperature 为 0.0；论文叙述中也使用 GPT-4.0 / GPT-4o 表述。

### 语法与语义比较

语法比较关注状态数、状态集合和四类 transition fault：additional transition、missing transition、local output fault、transfer fault。语义比较通过 trace 集合判断两个 input-complete DFSM 是否等价。论文用 distinguishing automaton 来寻找可区分两个 DFSM 的输入序列。

### 四类 repair 方法

1. **基于显式语法 fault 的 prompt repair**：把应存在、不应存在和已正确的转移写回 prompt，让 LLM 重新生成。
2. **基于 distinguishing sequence 的 prompt repair**：把 oracle 对某些输入序列的期望输出写回 prompt。
3. **基于 checking sequence 的 prompt repair**：构造一个 checking sequence，只要求专家给出该输入序列的期望输出，降低专家需要了解完整结构的要求。
4. **基于 fault model / mutation machine 的 repair**：用 LLM 常见错误构造修复域，再通过专家输出查询和 SAT-based mining 选择满足回答的 DFSM；这个方法减少 LLM 在修复中的角色，更依赖形式方法。

### 是否使用 few-shot / CoT / RAG / 自动反馈 / 修复闭环

- **few-shot**：原文 prompt 给出 CSV 输出示例，但没有报告系统性的 few-shot 对比实验。
- **CoT / RAG**：原文未使用 CoT 或 RAG。
- **自动反馈 / 修复闭环**：有。语法 fault、distinguishing sequence 和 checking sequence 会迭代拼接到 prompt；fault-model 方法则形成专家查询与修复域收缩闭环。
- **形式化验证 / 模型检查 / 仿真**：没有使用通用 model checker；但使用 FSM 等价、distinguishing automaton、checking sequence 和 model-based testing 语义作为形式化评估/修复支撑。

## 实验与评估

### 数据集

实验数据由作者随机生成：

- DFSM oracle 的输入参数包括状态数、输入 alphabet 大小和输出 alphabet 大小。
- 正文实验使用 5 个输入、2 个输出，状态数为 5、10 和少量 25。
- 对每个状态规模通常生成 30 个 oracle；25 状态实验只报告 1 个 oracle。
- 每个 oracle 通过英文句式模板转成自然语言描述；附录给出状态和转移描述 pattern。

### 评估指标

- 是否 faulty：生成 DFSM 与 oracle 在语法或语义上是否不同。
- fault type 数量：additional transition、missing transition、local output fault、transfer fault。
- repair succeeding rate：错误机器被修复为正确 DFSM 的比例。
- repair 代价：尝试次数、输出查询数量、输出查询长度、repair domain 是否需要补充特定转移。

### 实验设置

- GPT-4o API；temperature 0.0。
- 生成结果为 CSV DFSM。
- 原文 prototype 用 Python 实现 GPT 调用、随机机器/描述生成和比较方法。
- 最大 repair attempts 设为 $|S| \times |A|$。

### 主要实验结果

1. **生成错误类型**：在 5 状态、30 个 oracle 上，平均总 fault 数约 0.03，最大 1；在 10 状态、30 个 oracle 上，平均总 fault 数约 1.1，最大 11。常见错误为 missing transition 和 output fault。
2. **语法 fault repair**：5 状态有 2 个 faulty generated DFSM，10 状态有 9 个 faulty generated DFSM，表中 repair succeeding rate 均为 100%；25 状态只评估 1 个 oracle，未发现错误。
3. **distinguishing sequence repair**：5 状态 1 个错误样本修复成功率 100%；10 状态 7 个错误样本修复成功率 0%。作者认为大量 trace 信息可能削弱 LLM 注意力。
4. **checking sequence repair**：5 状态 5 个错误样本中，1 个一次修复，1 个三次修复，3 个未修复，总成功率 40%。作者指出 checking sequence 计算耗时，且单个长序列聚合了太多结构信息。
5. **fault-model repair**：5 和 10 状态各 30 个自动生成 oracle；faulty generated DFSM 分别为 15 和 26；表中 repair succeeding rate 均为 100%。但该实验允许在必要时向 repair domain 增加特定转移，以确保 oracle 包含在修复域中。

### 方法优势

- 任务定义非常接近 Project 1：自然语言描述到 FSM-family 规格。
- 明确输出为可解析 CSV DFSM，而不是只生成图片或自由文本。
- 把 LLM 生成质量问题落到 FSM fault model 和测试序列上，便于后续研究复用。
- 结论克制：作者明确指出 LLM 在信息量增加时缺乏精确分析能力。

### 方法的局限性

- 数据是合成英文描述，不是真实控制系统需求；句式由模板生成，和工业自然语言需求分布不同。
- 输出是平坦 DFSM / Mealy machine，不覆盖层次状态、并发、守卫条件、时间约束或动作语义。
- 多数修复实验依赖 oracle；真实场景中 oracle 缺失会显著增加不确定性。
- 代码、随机数据、prompt 实验制品未公开，复现需要重新实现。
- 没有与其他 LLM 状态机生成 baseline 做横向对比，也没有引入人工建模质量评审。

## 与本研究的关系

### 相关性分析

**BASELINE评估：🟢。**

本文是 Project 1 的直接 STM baseline。输入是自然语言 FSM 描述，输出是确定性有限状态机规格，LLM 是核心生成组件；虽然数据为模拟而非真实控制系统需求，但任务链条与“自然语言需求 -> 状态机模型”高度一致，并且额外提供 repair/diagnosis 设计。

### 四条件建议

| 条件 | 建议 | 理由 |
|---|---|---|
| LLM4Modeling | 🟢 | 论文核心就是用 GPT-4/GPT-4o 生成 DFSM 规格，并研究生成错误修复。 |
| NL输入 | 🟢 | 输入是英文自然语言 FSM 描述；虽然由模板合成，但仍是 NL 形式。 |
| LLM方法 | 🟢 | GPT prompt 是生成流程核心，部分 repair 方法也依赖 prompt refinement。 |
| STM族输出 | 🟢 | 输出是 CSV 表示的 deterministic finite state machine / Mealy machine。 |

### 可借鉴之处

- 可作为 Project 1 direct baseline 的最小可复现实验形态：固定输出 DSL/CSV，解析后做语法与语义 gate。
- fault type 可映射到 Project 1 缺陷分类：missing transition、wrong output/action、wrong target 等。
- checking sequence / distinguishing sequence 可作为 LLM 修复反馈的对照组，验证“trace feedback 是否真的可被模型利用”。
- fault-model repair domain 提示 Project 1 可把 LLM 修复限制在结构化候选空间，而不是让 LLM 自由改写全模型。

### 存在的不足与改进空间

- Project 1 需要真实控制系统需求、guard/action/time constraint，而本文主要处理抽象输入/输出 alphabet。
- 本文没有形成 run record、模型调用记录、数据版本和 artifact 发布；若作为复现实验基线，需要补齐证据链。
- 对 LLM 输出错误的判断依赖 oracle，真实需求下需要 LLM-as-Judge、专家审查或形式化性质共同构成替代 oracle。
- 修复方法尚未覆盖层次状态机、变量更新、复杂 guard 和并发状态区域。

### 对本研究的启发

本文最重要的启发是：Project 1 不应只评价“生成出来的状态机长得像不像”，而应把生成物解析为 machine-readable FSM，再用语法 gate、确定性/完备性检查、trace-based 对比和 fault-model repair 形成闭环。对于缺少 oracle 的真实需求，可以借鉴 checking sequence 的专家最小查询思想，把“让专家重画整张图”降级为“让专家回答少量行为 trace”。

## 重要的相关工作

### 1. 重要的前身类工作

**FSM testing 与 checking sequence 传统工作**

- Lee and Yannakakis 的 FSM testing survey、Petrenko 等关于 FSM inference 与 checking sequence 的工作，为本文语义比较和 checking sequence repair 提供理论基础。
- Koufareva、Petrenko 和 Yevtushenko 的 fault-model driven test generation 支撑本文 mutation machine / repair domain 设计。
- Ghedamsi、Bochmann 和 Dssouli 的 multiple fault diagnosis 为本文四类 transition fault 分类提供前身。

### 2. 直接参与实验的 baseline

原文没有把其他 LLM 状态机生成工具作为直接实验 baseline。实验对照主要是 oracle DFSM 与 GPT-4o 生成 DFSM 之间的差异，以及四种 repair 方法之间的比较。

### 3. 提供了重要论证的工作

**LLM 生成规格/代码邻近工作**

- Abukhalaf、Hamdaqa 和 Khomh 的 PathOCL 使用 GPT-4 生成 UML class diagram 的 OCL 约束，为“LLM 生成形式约束”提供邻近证据。
- Thakur 等的 VeriGen 和 Liu 等的 VerilogEval 讨论 LLM 生成 Verilog/HDL 代码和测试数据；本文借此说明 LLM 已被用于行为/硬件规格生成，但这些工作没有研究 FSM 规格修复。
- Bhandari 等关于 LLM-aided FSM testbench generation and bug detection 的工作与 FSM 测试相关，但不是本文的 `NL -> FSM` 生成任务。

### 4. 在技术上提供了支持的工作

**Prompt engineering 文献**

- White 等的 prompt pattern catalog 与 Denny 等关于 Copilot prompt engineering 的研究，为本文 prompt engineering 的必要性提供背景；本文也承认 prompt 质量没有形式保证。

**FSM oracle mining / model-based testing**

- Nguena Timo 关于 mining precise test oracle modelled by FSM 的工作，是 fault-model repair 阶段 SAT-based mining 的直接技术来源。

### 5. 其他重要工作

- Oakes、Famelis 和 Sahraoui 关于 domain-specific ML workflows 的工作为 MDE 中引入 ML/LLM 提供宏观背景。
- Steffen、Howar 和 Merten 关于 active automata learning 的实践视角，为未来把本文方法应用到 industrial-like descriptions 提供潜在线索。

## 文献分类总结

本文位于“LLM 直接生成 FSM 规格 + FSM testing/repair formal methods”的交叉点。它不是泛 UML 建模论文，也不是只做协议分析的状态机抽取论文，而是非常贴近 Project 1 direct baseline 的 `自然语言描述 -> machine-readable FSM` 工作。其主要价值在于把生成质量评价和修复问题做成可形式化比较的实验；主要短板在于数据合成、artifact 未公开、状态机语义较简化，尚未覆盖控制系统状态机中的时间、守卫、层次和并发语义。
