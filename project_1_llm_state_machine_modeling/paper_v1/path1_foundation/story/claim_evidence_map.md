# Path-1 Claim-Evidence Map

## 1. 使用方式

本文件是 S0a 后的 claim gate。任何进入 Abstract / Introduction / Contribution / Related Work 差异定位的 claim，必须在本文件中有对应状态、证据来源、baseline carve-out 和 safe wording。

状态口径：

- **Foundation-supported**：当前 foundation 可支持的任务边界、方法基础设施、历史资产索引或计划性表述；可进入 planning / method overview，不等于结果 claim。
- **Evidence-needed**：方向可保留，但必须等待 frozen sample、human adjudication、ablation、external baseline 或 artifact 证据；不能写成当前完成事实。
- **Manuscript-supported**：主实验、human adjudication、baseline 对齐和 artifact 完成后才可升级的结果型 claim。
- **Forbidden**：当前证据不支持、被 S1a baseline 打穿或与导师定调冲突，禁止进入论文主线。

硬规则：依赖 frozen sample、human adjudication、ablation、external baseline 或实验数字的句子，在 G3/G5 通过前只能是 **Evidence-needed**，不能作为 Abstract / Introduction 的 ready wording。

## 2. Mandatory closest works carve-out

四个 mandatory closest works 是每条 contribution 的默认反证入口：

| Baseline | 已覆盖能力 | 对 claim 的硬约束 |
|---|---|---|
| Structure/Event SMF | same-task NL -> UML state machine / structured prompt / 事件和结构化建模 | 禁止 “first NL-to-state-machine”；本文只能主张 executable / diagnostic / simulation substrate 的边际 |
| LLMs for EMP | SysML behavior model generation、rule/manual checking feedback、regeneration、human review | 禁止 “first behavior-model feedback loop”；本文只能区分 deterministic diagnostics + scenario simulation + structured repair decision 的组合 |
| TTool-AI | NL -> SysML/TTool、JSON / syntax / constraint tool feedback、artifact | 禁止 “first tool feedback”；本文只能把 diagnostics 当闭环组件，并承认 TTool/TTool-AI 先例 |
| Designing FSMs | synthetic NL -> CSV DFSM/Mealy、oracle / distinguishing / checking-sequence repair | 禁止 “first trace/oracle repair”；本文只能强调 scenario candidates + deterministic simulator execution + structured fix decision |

## 3. Contribution claim gate

| Contribution claim | status | baseline_coverage | marginal_claim | forbidden_softened_claims | evidence_source | evidence_needed | safe wording |
|---|---|---|---|---|---|---|---|
| C1：把 LLM 输出约束为 machine-checkable / executable state-machine representation 作为 feedback evaluation substrate | Foundation-supported | Structure/Event SMF 已覆盖 NL -> UML SM；LLMs for EMP / TTool-AI / Umple 覆盖 SysML / TTool / Umple 等目标表示 | 本文边际不是“生成状态机”，而是让目标表示服务 deterministic diagnostics、scenario simulation 和 repair decision 的受控评估 | “first NL-to-STM”；“we propose a new DSL / FCSTM as the contribution” | [paper_story.md](./paper_story.md)、[terminology_policy.md](./terminology_policy.md)、method parser/simulator docs | representation definition、语法子集、component extraction、limitations、artifact version | “We constrain LLM outputs to a machine-checkable and executable state-machine representation that supports deterministic diagnostics and simulation.” |
| C2：deterministic diagnostics feedback 进入建模 / 修复闭环 | Evidence-needed | TTool-AI 已有 syntax/constraint tool feedback；LLMs for EMP 已有 rule/manual checking feedback；Umple 可做 compile / syntax 评测 | 本文边际是把 parse / semantic / inspect diagnostics 作为可审计反馈信号，与 simulation / repair decision 共同进入受控消融 | “first deterministic diagnostics loop”；“prior tools only draw diagrams” | method stage API、diagnostic docs、retained examples | B2/B3/B5 消融、diagnostic taxonomy、失败/修复案例、external closest-work positioning | “We evaluate deterministic diagnostics as one feedback source in a controlled modeling loop.” |
| C3：scenario-level simulation feedback 作为行为证据 | Evidence-needed | Designing FSMs 已有 oracle / trace repair；TTool-AI 有 TTool simulation / verification 背景但主要不是 LLM loop 的 scenario feedback；LLMs for EMP 把 simulation trace 作为未来方向 | 本文边际是 LLM 生成 scenario candidates + deterministic simulator execution + pass/fail / trace 反馈，而不是 trace repair 首创 | “first scenario-based feedback”；“prior trace repair lacks simulation feedback” | method simulator、scenario stage、four-case retained evidence | B4/B5 消融、scenario freeze policy、trace examples、human adjudication 与 failure taxonomy | “We study scenario-level simulation feedback produced by deterministic execution of LLM-generated scenario candidates.” |
| C4：structured repair decision 记录 fix request / accept-reject / diff / FixLog | Evidence-needed | Designing FSMs 已有 fault-model / oracle repair；LLMs for EMP / TTool-AI 有 regeneration / auto-correction 先例 | 本文边际是把修复请求、接受/拒绝、diff、FixLog 和回归检查组织成可审计数据流 | “first repair loop”；“prior work lacks structured repair” | method run record / FixLog design、PR #31 E1 evidence | repair trace、eligibility filter、non-converged 样本、ablation 与 manual review | “We structure repair decisions and regression checks so that feedback-driven changes can be audited and evaluated.” |
| C5：baseline-aware controlled evaluation protocol | Foundation-supported | 九个 direct baseline 已覆盖多种任务/表示/反馈/评测；不同 artifact/GT/prompt/code 可得性不一 | 本文边际是按 same-sample approximate / near / evidence-only / boundary 分层，避免不可比横向排名 | “same benchmark beats all prior work”；“missing code is prior weakness” | [../baselines/SUMMARY.md](../baselines/SUMMARY.md)、[../evidence/baseline_and_related_work_matrix.md](../evidence/baseline_and_related_work_matrix.md) | frozen samples、human protocol、EXT baseline、budget table、artifact package | “We use a baseline-aware evaluation protocol that separates same-sample approximate, near, evidence-only, and boundary comparisons.” |
| C6：E1/E2 agent orchestration condition 分析 | Evidence-needed | Prior work 已覆盖 prompt chaining、agentic flow、tool feedback；Codex/Claude/skill 本身不是贡献 | E1/E2 只分析同一底座在不同 agent orchestration 下的质量、稳定性、成本和失败模式 | “Hybrid method contribution”；“Codex/Claude is the method” | PR #31 导师讨论、method run records | E1/E2 comparable runs、cost/quality/stability analysis、threats | “Agent orchestration is treated as an experimental condition rather than a standalone contribution.” |

## 4. General claim status table

| Claim | 状态 | 当前证据 | 进入 manuscript 还需什么 | 允许写法 |
|---|---|---|---|---|
| 本研究面向 NL 控制系统需求到状态机模型生成任务。 | Foundation-supported | project_1 定位、导师讨论、Path-1 foundation | 正式 manuscript 中定义输入输出和范围 | “we study NL-to-state-machine modeling for control-system requirements” |
| 当前方法底座已有可解析、可执行的状态机表示和 deterministic feedback infrastructure。 | Foundation-supported | [../../../method/README.md](../../../method/README.md)、[../../../method/STATUS.md](../../../method/STATUS.md) | 弱化 `fcstm` 名称，说明 representation 能力而非 DSL novelty | “our prototype operationalizes a machine-checkable and executable representation” |
| 本方法提升了 LLM 状态机建模质量。 | Evidence-needed | 当前只有方法基础设施和代表性 run evidence | 主实验、baseline 对比、human adjudication、统计表 | 结果出来前只能写研究问题：“whether feedback affects...” |
| 本文通过 frozen benchmark、human adjudication、ablation 和 recent baselines 完成评估。 | Evidence-needed | 当前只有计划和 S1a baseline 总账 | G2 sample/oracle freeze、G3 main experiment、G5 review closeout | 只能写 “we will evaluate / the protocol requires...” |
| 本稿当前投稿策略是按 CCF-A 标准打磨并优先投 CCF-B rolling journal。 | Foundation-supported | issue #67、[venue_readiness_gate.md](./venue_readiness_gate.md) | S0b 产出 `target_venue_decision.md` | “the readiness gate targets CCF-A review rigor while preserving a fit-first CCF-B route” |
| 本稿已经达到 CCF-A 论文标准或投稿级质量。 | Evidence-needed | 当前只有 readiness gate | G3/G4/G5/G6 全部通过 | G5 前禁止写成完成事实 |
| PR #9 提供了可复用的 historical sample / stress-test assets。 | Foundation-supported | [../dataset_selection/sample_assets.md](../dataset_selection/sample_assets.md) | 正式 sample registry 重核 | “historical candidate/stress-test assets” |

## 5. Forbidden claims

| Forbidden claim | 为什么禁止 | 替代写法 |
|---|---|---|
| 本文是首个 NL / 文档到状态机生成方法。 | 九个 direct baseline 已覆盖 FSM、UML/SysML state machine、Umple、Mermaid、TTool、protocol FSM 等路线 | “we study executable feedback for NL-to-state-machine modeling” |
| 本文是首个将 feedback loop 用于 LLM 状态机 / 行为模型生成的方法。 | Designing FSMs、LLMs for EMP、TTool-AI 已有 oracle / rule feedback / tool feedback / repair loop | “we integrate deterministic diagnostics and scenario-level simulation feedback under a controlled protocol” |
| 近期 baseline 只是画图，没有结构化输出或专家评估。 | CSV DFSM、Umple、PlantUML/SysML、TTool JSON/XML、3GPP transition tuple、专家 reference / F1 / Likert 均已存在 | 写具体 task / feedback / artifact 差异 |
| 本文 novelty 是 RAG / few-shot / prompt chaining / agent 编排本身。 | 多个 baseline 已覆盖这些技术 | 只作为条件、baseline 或 implementation detail |
| 我们在同一 benchmark 上超过所有 prior work。 | 当前没有 strict same benchmark | 使用 strict / approximate / near / evidence-only 分类 |
| Formal feedback 等于完整形式化验证 / model checking。 | 当前主要是 parse / semantic / inspect / simulation | “deterministic diagnostics and executable simulation feedback” |
| LLM-as-Judge 是主 oracle。 | 正式 protocol 必须 human adjudication 为主 | LLM 只可辅助且必须披露 |
| E1/E2 构成 Hybrid 方法贡献。 | 导师讨论已明确不主打 Hybrid | agent orchestration conditions / RQ dimension |
| PR #9 selection / expansion / early refs 是当前 paper result。 | PR #9 是 historical sprint evidence | stress-test / historical assets，正式复核后再用 |
| `fcstm` / `pyfcstm` 是 paper-level 新概念。 | 导师建议弱化命名，避免 DSL 说服负担 | internal DSL / prototype encoding / implementation artifact |
| run record / audit trail 是 contribution。 | 它支撑复核、打假和排障，不是 novelty | reproducibility / artifact support |

## 6. Abstract / Introduction guardrails

### Foundation 阶段可以写

- “We study whether executable feedback helps LLM-based state-machine modeling from control-system requirements.”
- “The current protocol separates deterministic diagnostics, scenario-level simulation feedback, structured repair decisions, and baseline-aware evaluation.”
- “The evaluation will use frozen samples, human adjudication, ablations, and closest-work baseline positioning.”

### G3/G5 之前不能写

- “We improve model quality.”
- “We outperform prior work.”
- “Our feedback loop is the first of its kind.”
- “The method is verified / formally correct.”
- “The artifact is submission-ready.”

## 7. 更新规则

1. 后续新增 claim 时，必须先放入本文件再进 paper draft。
2. 如果 S1b/S3 对某个 external baseline 的可复现性判断改变，必须同步更新 `baseline_coverage` 与 safe wording。
3. 如果实验结果不支持某个 Evidence-needed claim，优先降级或删除 claim，而不是补强措辞。
4. reviewer 提出 C/I 级 novelty 或 factual issue 时，必须在本文件新增 forbidden / weakened claim 记录。
