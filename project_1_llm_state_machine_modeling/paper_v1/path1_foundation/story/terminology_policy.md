# S0a Terminology Policy：弱化 `fcstm` 名称与贡献边界

## 1. 目的

本文档是 S0a story gate 的术语真源，用来防止第一篇论文从“LLM 状态机建模 + 可执行反馈”误漂移成“提出新 DSL / 新建模语言 / Codex 工作流报告”。

核心原则：

> 论文主文强调 formalized / executable / machine-checkable state-machine representation；`fcstm` / `pyfcstm` 只作为 implementation / artifact / appendix 中的内部原型载体。过程性工程材料不进入 Method / Contribution 主线。

## 2. 术语分层

| 位置 | 推荐术语 | 禁用 / 降级术语 | 说明 |
|---|---|---|---|
| Title | executable feedback; state-machine modeling; control-system requirements | `FCSTM`; `pyfcstm`; `new DSL`; `novel modeling language` | 标题不承担 DSL 说服负担 |
| Abstract | formalized state-machine representation; executable state-machine representation; machine-checkable state-machine model | `we propose FCSTM`; `new DSL`; `first formalism` | 摘要只讲任务、方法机制和证据，不讲内部名称 |
| Contributions | representation substrate; deterministic diagnostics; scenario-level simulation feedback; structured repair decision; baseline-aware evaluation | `FCSTM contribution`; `LangGraph contribution`; `process-material contribution` | 工程资产和过程性工程材料不作为贡献本体 |
| Method | internal DSL; prototype encoding; pyfcstm-backed implementation; deterministic parser / simulator | 把 `fcstm` 写成 paper-level concept | Method 可说明实现，不把实现名升格为 novelty |
| Artifact / Appendix | `pyfcstm` version; DSL grammar; runtime; diagnostics; simulator; supplementary materials | 把 artifact detail 写成主文 novelty | Artifact 只放必要复现材料，避免把过程性工程材料包装成论文方法 |
| Related Work | executable target representation; representation substrate; tool-checkable artifact | 与 UML / SysML / Umple / TTool 进行替代式战争 | 只比较任务、表示能力、反馈信号、评测协议 |
| Threats / Limitations | internal representation may limit expressiveness; mapping from UML/SysML/Umple requires care | 声称 private DSL 已覆盖全部工业状态机语义 | 主动说明表示范围和不可比性 |

## 3. 推荐写法

可用于主文的安全写法：

- “We constrain LLM outputs to a machine-checkable and executable state-machine representation.”
- “The representation acts as an evaluation substrate for deterministic diagnostics and simulation feedback.”
- “Our implementation uses an internal DSL and a deterministic parser/simulator to operationalize the representation.”
- “We evaluate the effect of deterministic diagnostics and scenario-level simulation feedback under frozen samples and human adjudication.”

中文口径：

- “本文把 LLM 输出约束到可解析、可诊断、可仿真的状态机表示。”
- “该表示是 feedback loop 的实验底座，不是本文要求审稿人接受的新建模语言。”
- “内部 DSL 与工具链只作为实现载体，在 artifact / appendix 中披露。”

## 4. 禁止写法与替代写法

| 禁止 / 高风险写法 | 风险 | 替代写法 |
|---|---|---|
| “We propose FCSTM, a new DSL for control-system state machines.” | 引入新 DSL 贡献负担，需证明与 UML / SysML / Stateflow / Umple / TTool 的关系 | “We use a machine-checkable and executable state-machine representation as the target artifact.” |
| “FCSTM is the main contribution of this paper.” | 把论文变成 DSL paper | “The contribution is the feedback-guided modeling workflow enabled by an executable representation.” |
| “Our new modeling language enables formal verification.” | formal overclaim；当前不是 BMC / LTL / theorem proving | “Our prototype enables deterministic parsing, semantic checks, design diagnostics, and scenario-level simulation.” |
| “Process engineering materials are a contribution.” | 过程性工程材料不应进入方法 / 贡献主线；论文主文不主动提 | “If venue or artifact rules require disclosure, keep only necessary reproducibility details outside the method narrative; they are not part of the method or contribution.” |
| “LangGraph / Codex / Claude is our method.” | 工程框架喧宾夺主 | “Agent frameworks are implementation/orchestration conditions over the same modeling substrate.” |
| “Prior work lacks feedback.” | 被 LLMs for EMP / TTool-AI / Designing FSMs 打穿 | “Prior work includes several feedback mechanisms; we position our work around deterministic diagnostics, simulation feedback, and structured repair decisions under a controlled protocol.” |
| “Prior trace repair lacks scenario simulation.” | 柔化 first claim，可能误述 Designing FSMs | “Designing FSMs motivates the need to distinguish oracle/trace repair from scenario-candidate generation plus deterministic simulator execution.” |

## 5. `fcstm` / `pyfcstm` 允许出现的位置

| 文件 / 场景 | 是否允许 | 写法要求 |
|---|---|---|
| `story/paper_story.md` | 仅允许在 naming caveat / artifact 说明中出现 | 必须配套“不是贡献 / internal prototype”说明 |
| `story/claim_evidence_map.md` | 允许作为 forbidden 或 implementation evidence | 不得进入 safe contribution wording |
| `story/paper_outline.md` | 原则上少用 | Method implementation subsection 可用 “internal DSL / pyfcstm-backed prototype” |
| `evidence/project_inventory.md` | 允许 | 作为 repository evidence 和 artifact 入口 |
| `experiment_design/*.md` | 允许 | 作为 deterministic parser / simulator / runtime source，不作为 contribution |
| Abstract / Introduction / Contribution 候选 | 禁止 | 用 machine-checkable / executable state-machine representation 替代 |
| Artifact / Appendix | 允许 | 记录版本、grammar、diagnostics、simulator 和必要复现信息；不把过程性工程材料包装为贡献 |

## 6. grep / 自检策略

S0a 实现和后续写作至少执行两级检查：

1. **硬禁区检查**：title / abstract / contribution 候选、safe wording、claim 正文和 Related Work 差异定位中不得出现：`FCSTM`、`new DSL`、`new modeling language`、`novel formalism`、`process-material contribution`、`first NL-to-STM`、`first feedback loop`。
2. **允许反例检查**：`terminology_policy.md`、`claim_evidence_map.md` forbidden examples、artifact / appendix 说明中允许出现上述词，但必须用于禁用、降级或实现说明，不能形成正向 novelty。

推荐人工核查命令示例：

```bash
grep -RIn "first NL-to-STM\|first feedback loop\|new DSL\|FCSTM\|process-material contribution\|we improve quality\|we show improvement" \
  project_1_llm_state_machine_modeling/paper_v1/path1_foundation/story \
  project_1_llm_state_machine_modeling/paper_v1/path1_foundation/evidence \
  project_1_llm_state_machine_modeling/paper_v1/path1_foundation/experiment_design
```

命中后必须判断命中位置：若在 forbidden examples / policy 中是安全命中；若在 safe wording / contribution / result claim 中则必须修复。

## 7. 与后续 PR 的关系

- **S0b / PR-S0-Direction**：写 `DIRECTION.md`、`abstract_v0.md`、`target_venue_decision.md` 时必须先读取本文档。
- **S1b**：Related Work 必须使用本文档的术语，不把本文包装成 DSL 替代 UML/SysML/Umple。
- **S3/S4**：实验报告可引用 `pyfcstm` 作为实现依赖，但结果表和 RQ 应围绕 diagnostics / simulation / repair decision。
- **S5 manuscript**：任何 abstract / introduction / contribution 改写都必须回查本文档和 [claim_evidence_map.md](./claim_evidence_map.md)。
