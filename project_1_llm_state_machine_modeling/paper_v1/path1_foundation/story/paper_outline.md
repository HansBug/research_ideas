# Path-1 第一篇论文章节大纲与主线冻结草案

本文档是 Path-1 第一篇论文的写作骨架。它把导师讨论、PR #9 历史资产、PR #22 方法底座、PR #92 baseline 增量和 9 个五绿直接 baseline 的反证压力合在一起，防止后续论文写成“又一个自然语言生成状态机”或“工程 agent 报告”。

## 1. 导师决策锚点

当前第一篇论文必须按以下锚点推进：

1. 第一篇优先走 **Path-1 基线硬对比**，目标是回答“相对已有 LLM 状态机生成工作，我们的可执行形式化反馈是否带来可验证增量”。
2. **Path-2 控制系统差异化**、变量角色、BMC / LTL、深控制系统语义暂不作为第一篇主线；这些内容进入 future work 或后续论文。
3. **E1 / E2 不是 Hybrid 方法贡献**。E1 是同一方法底座在自建闭环中的运行形态；E2 是同一方法底座通过 skill 在成熟 coding agent 中的运行形态。二者是实验条件，不是两个方法拼装。
4. 论文主文弱化 `fcstm` 名称，优先称为“形式化 / 可执行状态机表示”；工具名放在 implementation / artifact 中。
5. 方法贡献围绕 LLM4STMModeling 的“表示 + 检查 + 仿真 + 修复决策”，不是围绕某个 prompt、某个框架、某个 LLM provider 或 run record。run record 只作为实验复核、打假和排障支撑。

## 2. 9 个五绿直接 baseline 后的现实判断

[../../../baselines/SUMMARY.md](../../../baselines/SUMMARY.md) 当前已记录 9 个五绿直接 baseline。它们覆盖了自然语言 / 文档到 FSM、UML state machine、SysML behavior、Umple、Mermaid statechart、TTool/SysML 等主要路径。

| 直接 baseline | 已经做到什么 | 对本文 claim 的反证压力 | 后续用途 |
|---|---|---|---|
| Designing FSMs from Requirements with GPT-4 | 合成英文 DFSM 描述到 CSV DFSM / Mealy machine，并有 oracle / trace / repair 诊断 | 打穿“NL 到 FSM 是新任务” | direct / approximate 候选，重点比较可执行性与样本真实性 |
| Structure- and Event-Driven Frameworks | 非结构化 reactive-system NL 到 UML 状态机，按 states / transitions / guards / actions 等槽位评 F1 | 打穿“自由文本到状态机生成是新问题” | 最优先 closest prior work，适合复刻策略或同样本近似对比 |
| FlowFSM | RFC 长文档经 prompt chaining 抽取 protocol FSM / rulebook | 打穿“长文档 + agentic flow + FSM 抽取是新问题” | evidence-only 或协议方向近邻；artifact 不完整时不强行硬复现 |
| SpecGPT | 3GPP 规格经领域 CoT 和多模型 ensemble 抽取协议状态机 | 打穿“规格文档到状态机抽取 / ensemble 是新贡献” | evidence-only / near baseline，强调输出领域与 oracle 不可比 |
| Automotive Statechart Generation | 私有汽车需求到 Mermaid statechart，含微调和专家评审 | 打穿“汽车工业 statechart 生成是新场景” | evidence-only；不可复现风险高 |
| Umple Llama3 | NL 到 Umple 状态机代码，比较 zero-shot / one-shot / RAG | 打穿“RAG / few-shot 改善状态机代码生成是新贡献” | structured / RAG prompt baseline 候选 |
| LLMs for EMP | NL 到 PlantUML / SysML 行为模型，含规则检查反馈和公开数据 | 打穿“反馈修复状态机 / 行为模型是独有优势” | 强 closest work；需区分语法反馈与可执行仿真反馈 |
| Pushing the Generative Envelope | 短系统描述到 SysML v2 requirements / state machine diagrams，比较 prompt 技巧 | 打穿“prompt / temperature 是核心贡献” | evidence-only / prompt-technique 对照 |
| TTool-AI | NL 到 SysML blocks / state machines / TTool XML，含知识注入与自动反馈循环 | 打穿“工具集成 + 自动反馈闭环是首创” | 强 closest work；强调本文的控制系统语义、scenario-level feedback、修复决策和组件评价差异；run record 只作实验复核 |

结论：第一篇不能把 novelty 写成“我们能从自然语言生成状态机”。这个主问题已经被多条路线覆盖。本文最稳的增量只能是：

> 将自然语言状态机生成转化为可解析、可执行、可检查、可仿真、可修复的闭环建模任务，并用冻结样本、人工组件级裁决、消融和 closest baseline 对比评估可执行形式化反馈与结构化修复决策对模型质量的边际价值。

## 3. 论文主线四句

### 3.1 Thesis

本文提出并评估一种面向自然语言控制系统需求的 LLM 状态机建模闭环，该闭环通过形式化 / 可执行状态机表示把 LLM 生成结果接入确定性检查、场景仿真和结构化修复决策，并在 Path-1 基线硬对比中检验可执行形式化反馈对模型质量和稳定性的影响。

### 3.2 Gap

已有 LLM 状态机生成工作已经能生成 FSM、UML / SysML state machine、Umple、Mermaid 或 TTool 模型，但多数工作仍偏“生成后评价”或“语法 / schema / 人工反馈”，缺少一个同一实验协议下可执行、可仿真的闭环来说明工具反馈如何改变模型质量与修复过程；run record 只用于复核该过程。

### 3.3 Technical challenge

自然语言需求中的状态、事件、guard、action、变量和异常行为并不天然对齐到状态机组件；LLM 生成错误会跨组件级联；确定性检查只能发现部分缺陷而不能替代 human oracle；修复循环还可能振荡。因此，论文必须同时处理表示、反馈、仿真、修复记忆、人工裁决和 baseline 公平性。

### 3.4 Method insight

LLM 负责语义解释、模型草拟、场景草拟和修复决策；确定性工具负责把候选模型变成可解析、可执行、可仿真的对象，并以结构化 diagnostics / traces / diffs 形成反馈。两者之间用 FixLog 连接修复决策，并用 run record 保存“生成了什么、为什么修、如何修、修后是否回归”，用于实验复核、打假和排障。

## 4. 建议 RQ

| RQ | 问题 | 必需证据 | 失败时的降级写法 |
|---|---|---|---|
| RQ1 | 在与近期直接 baseline 可比的输入 / 输出 / 组件评价协议下，本文方法能否生成更完整、可执行、可检查的状态机？ | frozen sample registry、至少 1 个 same-sample approximate baseline、组件级 human adjudication | 降级为 pilot / diagnostic comparison |
| RQ2 | parse / semantic / inspect / simulation 等可执行形式化反馈分别贡献了什么？ | B0-B5 消融、失败类型学、修复轨迹 | 只报告哪些反馈源最常触发有效修复，不宣称整体提升 |
| RQ3 | 同一方法底座在自建 agent-loop 与成熟 coding-agent skill 形态下，在质量、稳定性、成本和失败模式上有何差异？ | E1/E2 同样本或可比样本 run record、NFRR / human review、成本和失败记录 | 写成 implementation study / exploratory analysis；run record 只作复核证据 |
| RQ4 | 失败样本暴露了哪些状态机建模难点，例如 guard/action/hierarchy/变量/场景 oracle 漂移？ | failure taxonomy、代表性失败 case、reviewer closeout | 写成 threats / future work，不支撑主 claim |

## 5. 章节大纲草案

### 1 Introduction

- 开场不是“LLM 可以画状态机”，而是“状态机模型只有可执行、可检查、可追溯时才可用于高可信控制系统建模”。
- 说明已有工作已经能生成状态机族模型，但生成后模型的可执行性、反馈闭环和实验复核证据不足。
- 明确本文研究问题：可执行形式化反馈是否能提升 LLM 状态机建模。
- 给出贡献，但全部限定在后续证据已经完成的范围内。

### 2 Background and Task Definition

- 定义输入、输出、状态机组件、支持范围和不支持范围。
- 说明本文的“形式化状态机表示”只是为检查 / 仿真 / 反馈服务，不主张 DSL 本身为核心贡献。
- 定义组件级评价对象：states、transitions、guards、actions、hierarchy、variables / effects、scenario behavior。

### 3 Prior Work Capability Gap

- 用 9 个五绿直接 baseline 建一张 “已有能力 / 反馈类型 / artifact / 可复现性 / 本文差异” 表。
- 明确哪些 claim 已被 prior work 覆盖：NL->STM、RAG、prompt chaining、long-doc FSM、tool feedback、工业 statechart。
- 收敛出本文差异：可执行形式化反馈 + 仿真 + repair evidence chain + agent orchestration 对照。

### 4 Method

- Overview：生成-检查-仿真-修复闭环。
- Representation：可执行状态机表示及其组件抽取。
- Deterministic feedback：parse / semantic / inspect / simulation。
- Repair decision：fix request、accept/reject、FixLog、SL-10-style review；run record 只作为实验复核记录。
- Agent conditions：E1 自建闭环与 E2 成熟 agent skill route，作为实验条件而非 Hybrid 贡献。

### 5 Experimental Protocol

- Sample registry：样本来源、纳入 / 排除标准、代表性与 stress-test 区分。
- Baselines：direct / near / evidence-only；至少 1 个 same-sample approximate baseline。
- Metrics：组件级 human adjudication、deterministic validity、scenario pass、repair convergence、audit completeness。
- Human protocol：至少两名独立标注人、blind coding、agreement、仲裁。
- Run record：provider、model、prompt、raw output、usage、stage trace、eligibility、redaction。

### 6 Results

- RQ1 baseline hard comparison。
- RQ2 消融：无反馈、只有检查、检查+仿真、完整闭环。
- RQ3 E1/E2 对照：质量、稳定性、成本、审计性。
- 所有结果必须含 failure / non-converged / invalid run 的 eligibility 说明。

### 7 Failure Analysis and Case Study

- 选择成功与失败各有代表性的 case。
- 展示一条完整 run record / FixLog / scenario trace。
- 说明哪些问题由检查发现，哪些由仿真发现，哪些只能靠 human adjudication。

### 8 Related Work

- LLM for state-machine / behavior model generation。
- Requirements-to-executable / formal models。
- Agentic feedback / repair for modeling artifacts。
- 本文避免把“无 LLM 的经典 formal methods”贬低为不相关；它们支撑 rigor 背景。

### 9 Threats to Validity and Limitations

- baseline 公平性、closed artifact、provider drift、sample bias、human oracle、LLM assistance、形式化反馈深度有限。
- 明确 Path-2、变量角色、BMC/LTL、深控制系统语义是后续工作。

### 10 Artifact and Conclusion

- artifact 内容：代码、prompt、run records、样本注册表、标注协议、结果表。
- 结论只回到已验证的范围，不写 SOTA / solve / complete verification。

## 6. 反证门：禁止作为核心贡献的 claim

| 禁止 claim | 为什么禁止 | 可替代表述 |
|---|---|---|
| 首个 NL / 文档到状态机生成方法 | 9 个五绿 baseline 已覆盖 | “we study executable feedback for NL-to-state-machine modeling” |
| RAG / few-shot / prompt chaining 是本文核心 novelty | Umple、Structure/Event、FlowFSM、SpecGPT 已覆盖 | “we include structured baselines and focus on executable feedback” |
| 工具反馈 / 自动修复闭环是本文独有 | LLMs for EMP 和 TTool-AI 已有反馈 / 修复先例 | “we integrate deterministic checking and simulation into an auditable loop” |
| 长文档 FSM 抽取是新问题 | FlowFSM、SpecGPT 已覆盖 | “long-document extraction is related; our main setting is control-system requirements with executable feedback” |
| 汽车 / 工业状态图生成是新场景 | Automotive statechart thesis 已覆盖 | “industrial examples motivate the task; novelty is not the domain alone” |
| `fcstm` / LangGraph / Codex / Claude 是学术贡献 | 导师讨论已要求弱化工程名 | “implementation choices supporting the method / experiments” |
| 已完成完整形式化验证 | 当前只是 parse / semantic / inspect / simulation | “executable formal feedback, not complete model checking” |

## 7. 投稿目标与 CCF-A 标准门禁

本稿后续写作按 [venue_readiness_gate.md](./venue_readiness_gate.md) 执行：目标是 **按 CCF-A 论文标准打磨，2026 夏季优先投 CCF-B 期刊**。默认主投 SoSyM regular rolling；如果最终稿更像自动化软工 / tool-supported repair loop，则备投 ASE Journal regular；如果最终稿更像 requirements-to-behavioral-model / requirements validation，则备投 Requirements Engineering Journal regular。

这一定调对章节写法有三个直接约束：

1. **Introduction** 要回答 SoSyM / ASEJ / REJ reviewer 都会问的第一问题：为什么这是一个有学术价值的建模问题，而不是一个 prompt engineering demo。
2. **Experiment** 必须按 A 类审稿强度准备：9 个 direct baseline 阻塞吸收、至少 1 个 same-sample approximate baseline、B0-B5 消融、human adjudication、run record 和 failure taxonomy。
3. **Threats / Artifact** 不能当附录边角料：baseline fairness、sample bias、oracle、provider drift、LLM usage、artifact 可复现性必须在主文或清晰 artifact 中闭合。

当前 foundation 阶段只能说“已建立 readiness gate”，不能说“论文已经达到 CCF-A 标准”。是否达到该级别要在 G5 strong review closeout 时根据完整稿、结果表、artifact 和 C/I/M closeout 判定。

## 8. 投稿前证据门

| Gate | 阻塞问题 | 必需产物 |
|---|---|---|
| Baseline 事实门 | close work 漏读或误述会直接破坏 originality | [`../baselines/SUMMARY.md`](../baselines/SUMMARY.md)、[`../baselines/papers/*.md`](../baselines/papers/) 九篇 direct baseline 反证表、4 个 mandatory closest works（`Structure/Event SMF`、`llms_emp`、`TTool-AI`、`Designing FSMs`） |
| 同构性门 | 不同输入 / 输出 / 预算下的比较会被质疑不公平 | direct / near / evidence-only 分类、same-sample approximate baseline 说明 |
| 样本冻结门 | cherry-pick 风险 | `sample_registry.csv`、纳入 / 排除理由、stress-test 与 main benchmark 区分 |
| Oracle 门 | LLM judge 或单人判断不足 | `human_rubric.md`、`oracle_protocol.md`、`>=2` annotators、agreement / adjudication |
| 可执行性门 | 文本相似不等于状态机可用 | parse / semantic / inspect / simulation 结果与 eligibility filter |
| 消融门 | 无法证明 feedback 贡献 | B0-B5 条件、run record、failure taxonomy |
| 复核门 | reviewer 无法复现或追踪修复 | prompt、raw output、usage、stage trace、scenario、diff、redaction |
| Claim 门 | 摘要 / 引言过度宣称 | [claim_evidence_map.md](./claim_evidence_map.md) 逐句审计 |

## 9. 当前 foundation 允许说什么

当前只能说：

- 已建立第一篇 Path-1 paper 的 foundation、历史资产归档和执行 gate。
- 已确认第一篇主线应从“能否生成状态机”收缩为“可执行形式化反馈与结构化修复决策是否带来模型质量增量”。
- 已识别 9 个五绿 direct baseline 对 novelty 的反证压力。
- 已规划 baseline、sample、oracle、run record、ablation 和 writing 的后续 PR。

当前不能说：

- 方法已经优于 baseline。
- 样本已经冻结。
- 人工 oracle 已完成。
- 消融已经证明 feedback 有效。
- 本文已具备投稿级实验结果。
