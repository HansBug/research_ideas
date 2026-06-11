# S0b Target Venue Decision：投稿路线冻结

本文档是 PR-S0 / S0b 的**投稿路线决策产物**，用于把 S0a 已冻结的论文 story 落到可执行的 venue strategy 上。它不重构 story，不倒推贡献，不新增结果 claim。

## 1. 单一真源关系

| 文件 | 角色 | 本文如何使用 |
|---|---|---|
| [story/paper_story.md](./story/paper_story.md) | S0a story 真源 | thesis、gap、method insight、贡献边界和 forbidden claims 的上游依据 |
| [story/terminology_policy.md](./story/terminology_policy.md) | 术语真源 | 约束 `fcstm` / `pyfcstm` 只能作为 implementation / artifact，不得写成新 DSL 或论文贡献 |
| [story/claim_evidence_map.md](./story/claim_evidence_map.md) | claim gate 真源 | 判断哪些句子只能写成研究问题，哪些必须等 G3/G5 证据后才能升级为结果 claim |
| [story/venue_readiness_gate.md](./story/venue_readiness_gate.md) | venue 背景输入 | 提供 SoSyM / ASE Journal / Requirements Engineering Journal 候选池、叙事分流和 CCF-A reviewer 强度门禁；**不是最终 venue 决议** |
| 本文档 | S0b 决策产物 | 冻结当前主投 / 备投路线、切换条件、不得硬投条件和后续 PR 使用口径 |
| [ccf_a_readiness_checklist.md](./ccf_a_readiness_checklist.md) | S0b 派生 checklist | 从本文档与 [story/venue_readiness_gate.md](./story/venue_readiness_gate.md) 派生可执行自查项；**不制造第二套 venue 事实源** |

结论先行：**当前默认主投 SoSyM regular rolling；ASE Journal 与 Requirements Engineering Journal 作为备选路线；全稿按 CCF-A reviewer 强度打磨，但这不等于把目标 venue 升级为 CCF-A。**

## 2. 当前冻结决策

| 排序 | Venue | 当前定位 | 决策 |
|---:|---|---|---|
| 1 | SoSyM regular rolling | software / system modeling、状态机建模质量、可机检 / 可执行建模反馈最贴合 | **默认主投** |
| 2 | Automated Software Engineering Journal regular rolling | automated modeling、tool-supported workflow、repair / feedback loop、agentic workflow 视角较强 | **备投 1** |
| 3 | Requirements Engineering Journal regular rolling | NL requirements representation、requirements-to-behavioral-model、需求验证和 traceability 视角较强 | **备投 2** |

该排序服务于当前 S0a story：

> 自然语言控制系统需求 → 可机检且可执行的状态机表示 → deterministic diagnostics → scenario-level simulation feedback → structured repair decision → baseline-aware controlled evaluation。

因此，venue 选择不能反向把论文改写成：

- 新 DSL / 新建模语言论文；
- Codex / LangGraph / agent workflow 报告；
- 完整形式化验证或 model checking 论文；
- 单纯 requirements engineering survey；
- 只有结果提升承诺、但缺少 baseline / oracle / artifact 支撑的经验论文。

## 3. 为什么默认主投 SoSyM

SoSyM regular rolling 当前最贴合本文的主线，原因是：

1. **研究对象是状态机 / 系统建模质量**：论文核心不是 prompt 技巧，而是让 LLM 输出落到可解析、可诊断、可仿真的状态机表示，并评估这种表示如何承载 feedback。
2. **方法边界更接近 modeling artifact + feedback**：diagnostics、scenario-level simulation、structured repair decision 都围绕建模制品质量展开，而不是围绕通用 coding-agent 能力展开。
3. **S0a 已弱化 `fcstm` / `pyfcstm`**：本文不要求审稿人接受一个新 DSL；SoSyM 路线可以把内部表示放在 implementation / artifact 层面，把主文重心放在 executable modeling substrate 与质量评价上。
4. **baseline 风险更可控**：Structure/Event SMF、LLMs for EMP、TTool-AI、Designing FSMs 可以作为 Related Work 第一层和 baseline-aware protocol 的核心约束；SoSyM 叙事允许正面处理 UML / SysML / TTool / FSM-family prior work，而不需要把本文包装成“首个”。
5. **结果尚未冻结**：当前没有 G3/G5 主实验数字，不适合先按“自动化性能提升”或“需求工程验证效果”强行改写 venue 叙事。

SoSyM 版本的安全主线应是：

> We study executable feedback for LLM-based state-machine modeling from control-system requirements.

而不是：

- “We propose FCSTM, a new DSL ...”；
- “We are the first NL-to-STM method ...”；
- “We improve generated state machines by X% ...”；
- “We formally verify generated models ...”。

## 4. ASE Journal 切换条件

若后续 S3 / S4 / S5 的证据显示论文更像自动化软工工作，可以从 SoSyM 切到 ASE Journal。切换必须同时满足：

1. **自动化闭环证据成为主卖点**：B0-B5 / EXT 消融能清楚说明 diagnostics、simulation feedback、structured repair decision 对质量、稳定性或失败模式有可防守边际。
2. **tool-supported workflow 不是工程堆栈报告**：Method 能压缩为清晰的 feedback-guided modeling workflow，而不是 LangGraph / Codex / provider 配置说明。
3. **external baseline 不缺位**：至少一个 same-sample approximate baseline 或清晰的 near / evidence-only carve-out 能支撑自动化路线的公平性。
4. **oracle 可防守**：主结果依赖 human component adjudication、agreement 与仲裁，而不是 LLM judge 或单人主观判断。
5. **写作能正面承认 closest works**：Structure/Event SMF、LLMs for EMP、TTool-AI、Designing FSMs 都在 Related Work 第一层，且没有 soft first claim 回潮。

不得切 ASE Journal 的条件：

- 主实验只有内部 smoke / pilot，没有冻结样本与 human oracle；
- 只能展示 agent-loop 工程可运行，不能展示可评价的 modeling / repair 边际；
- 把 Codex / Claude / LangGraph / prompt chain 写成论文贡献；
- 用不可比较的 external baseline 强行排名；
- 结果不足时仍写 “we improve / outperform / solve”。

## 5. Requirements Engineering Journal 切换条件

若后续证据显示论文更适合需求工程视角，可以转 Requirements Engineering Journal。切换必须同时满足：

1. **需求到行为模型的研究问题更突出**：论文主线聚焦 NL control requirements 的歧义、状态 / 事件 / guard / action 抽取、requirements-to-behavioral-model traceability。
2. **human adjudication 与 traceability 成为核心证据**：人工 component-level 裁决、需求片段到模型元素映射、scenario relevance 判断比自动化 pipeline 本身更重要。
3. **样本选择能解释需求工程价值**：9 系统 / 101 需求或预注册降级样本能覆盖需求风格、歧义、恢复路径和状态机组件难点。
4. **Related Work 扩展到 RE 语境**：除了四个 mandatory closest works，还需要补足 requirements-to-model、controlled natural language、requirements validation 等背景。

不得切 Requirements Engineering Journal 的条件：

- 论文主要证据是 runtime / toolchain / engineering implementation；
- 需求 traceability、human protocol、ambiguity 分析不足；
- 只是把同一篇 SoSyM / ASEJ 稿换标题，不补 RE reviewer 关心的问题；
- 为迎合 REJ 而弱化 mandatory closest LLM-to-state-machine works。

## 6. 不得硬投条件

无论最终选择 SoSyM、ASE Journal 还是 Requirements Engineering Journal，只要出现以下任一情况，都不得为了时间节点硬投：

| Gate | 不得硬投触发条件 | 必须动作 |
|---|---|---|
| Novelty | Abstract / Introduction 暗示 `first NL-to-STM`、`first feedback loop`、prior work only draws diagrams、prior work lacks feedback | 回到 [story/claim_evidence_map.md](./story/claim_evidence_map.md) 降级 claim，并让 S1b / S5 重写 |
| Mandatory closest works | Structure/Event SMF、LLMs for EMP、TTool-AI、Designing FSMs 未进入 Related Work 第一层 | 暂停投稿，先补 S1b |
| Baseline | 主结果只有 internal ablation，没有 external same-sample approximate 计划或合理降级说明 | 降级为 protocol / diagnostic study，或补 S3 |
| Sample | 使用 cherry-picked 成功样本、historical Top-15 或 stress-test 样本写平均性能 claim | 回到 S2 冻结 sample registry 与排除规则 |
| Oracle | 主质量结论依赖 LLM judge 或单作者判断 | 回到 S2 建立 human adjudication、agreement 与仲裁 |
| Claim-evidence | 在 G3/G5 前写 improvement / superiority / repair stability 结果 claim | 删除或改成 “we study / we evaluate / whether ...” |
| Artifact | reviewer 无法理解输入、输出、模型配置、prompt / tool setting、失败类型和统计口径 | 补 artifact package 与脱敏材料；不要把过程性工程材料写成 contribution |
| Threats | baseline fairness、sample bias、oracle、provider drift、LLM usage 未正面处理 | 补 threats 与 limitation；必要时降级 claim |
| Writing | `fcstm` / `pyfcstm` / new DSL / engineering workflow 在标题、摘要或贡献中回潮 | 按 [story/terminology_policy.md](./story/terminology_policy.md) 改写 |

## 7. 后续 PR 使用规则

| 后续 PR | 必须继承的 venue 口径 |
|---|---|
| S1b Related Work | 以 SoSyM 主线组织 closest works；同时保留 ASEJ / REJ 切换所需的自动化与需求工程线索 |
| S2 Sample / Oracle | 样本、rubric、human adjudication 必须服务 SoSyM 主线的 modeling quality claim，并保留 REJ 所需 traceability 信息 |
| S3 Baseline / Ablation | 至少尝试 same-sample approximate baseline；若不可行，必须中性记录 near / evidence-only 降级理由 |
| S4 Run / Analysis | 结果表必须区分 diagnostics、simulation feedback、repair decision 的边际；不能只汇报 full loop 胜率 |
| S5 Manuscript | 默认按 SoSyM regular 组织标题、摘要、Introduction、Method、Experiments 与 Threats；只有触发 §4 或 §5 条件才切 venue |
| S6 Submission QA | 使用 [ccf_a_readiness_checklist.md](./ccf_a_readiness_checklist.md) 做 CCF-A reviewer 强度自查；不把 CCF-A 自查误写成目标 venue |

## 8. 当前未决项

1. 最终标题仍待 S5 根据真实结果压缩；当前不得主打 `FCSTM` / `pyfcstm`。
2. 是否从 SoSyM 切 ASEJ / REJ，必须等 S2-S4 证据闭合后再判断。
3. 主结果 claim 仍是 Evidence-needed；G3/G5 前只能写研究问题和评估计划。
4. CCF-A readiness 只是质量门禁；当前目标路线仍是 fit-first 的 CCF-B rolling journal。
