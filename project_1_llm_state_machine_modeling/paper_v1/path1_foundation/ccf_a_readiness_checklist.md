# S0b CCF-A Readiness Checklist

本文档是 PR-S0 / S0b 的**派生自查表**：它把 [story/venue_readiness_gate.md](./story/venue_readiness_gate.md) 的 CCF-A reviewer 强度门禁、[target_venue_decision.md](./target_venue_decision.md) 的投稿路线决策，以及 S0a 的 [paper_story.md](./story/paper_story.md)、[terminology_policy.md](./story/terminology_policy.md)、[claim_evidence_map.md](./story/claim_evidence_map.md) 压缩成后续 PR 可执行的 checklist。

边界：

- [story/venue_readiness_gate.md](./story/venue_readiness_gate.md) 是 venue readiness 背景输入，不是最终投稿决议。
- [target_venue_decision.md](./target_venue_decision.md) 是 S0b venue 决策产物。
- 本文档只做 CCF-A reviewer 强度自查，不制造第二套 venue 事实源。
- CCF-A 是质量门禁和审稿强度，不等于本文目标 venue 升级为 CCF-A。
- checklist 的“通过”只能说明当前文档 / 实验准备满足投稿前门禁；不能自动产生结果 claim。

## 1. 状态口径

| 状态 | 含义 | 使用规则 |
|---|---|---|
| `TODO` | 尚未完成或尚未审查 | 后续 PR 必须补证或说明降级原因 |
| `PARTIAL` | 有初步文档 / 计划，但证据未闭合 | 不能支撑强 claim；只能进入 planning / limitation |
| `PASS` | 已有可审计证据，且与 S0a/S0b 真源一致 | 可作为对应 gate 通过依据 |
| `BLOCKED` | 缺少外部条件或需人工决策 | 不得绕过；必须在 PR / manuscript 中显式记录 |

本表初始状态以 S0b 文档冻结为准，默认不把尚未运行的实验写成 `PASS`。`PARTIAL` / `TODO` 在 S0b 阶段是正常的诚实状态，不自动构成缺陷；只有到对应 owner 阶段（如 S1b/S2/S3/S4/S5/S6）结束后仍无法闭合，才升级为 gate failure 或 claim 降级依据。

## 2. Novelty 与 story gate

| ID | 检查项 | 当前状态 | 证据 / 来源 | 不通过时动作 |
|---|---|---|---|---|
| N1 | Thesis 是否围绕 executable feedback for LLM-based state-machine modeling，而不是 `first NL-to-STM` | PARTIAL | [story/paper_story.md](./story/paper_story.md)、[target_venue_decision.md](./target_venue_decision.md) | 回到 S0a story gate 重写 |
| N2 | Abstract / Introduction 是否没有 `first feedback loop`、`first trace repair`、prior work only draws diagrams 等 soft first claim | TODO | [story/claim_evidence_map.md](./story/claim_evidence_map.md) | S5 写作前 grep + 人工 review |
| N3 | `fcstm` / `pyfcstm` 是否只作为 implementation / artifact，不作为新 DSL 或贡献 | PARTIAL | [story/terminology_policy.md](./story/terminology_policy.md) | 修改标题、摘要、贡献和 Method wording |
| N4 | Formal wording 是否限定为 deterministic diagnostics / executable simulation，而不是 complete verification | PARTIAL | [story/claim_evidence_map.md](./story/claim_evidence_map.md)、[story/terminology_policy.md](./story/terminology_policy.md) | 删除 model checking / theorem proving / certification 过度表述 |
| N5 | Contributions 是否都带有 baseline carve-out 和 evidence-needed 状态 | TODO | [story/claim_evidence_map.md](./story/claim_evidence_map.md) | 未闭合前不进入 final manuscript claim |

## 3. Mandatory closest works gate

四个 mandatory closest works 必须进入 Related Work 第一层，并在 Method / Experiment / Claim wording 中持续作为反证约束。

| Work | 必须承认的已覆盖能力 | 本文安全边际 | 当前状态 | 后续 owner |
|---|---|---|---|---|
| Structure/Event SMF | same-task NL → UML state machine、structured / event-driven prompting、组件级评价 | executable representation 作为 diagnostics / simulation / repair decision 的实验底座 | PARTIAL | S1b / S3 / S5 |
| LLMs for EMP | SysML behavior model generation、rule/manual checking feedback、regeneration | 区分 deterministic diagnostics、scenario simulation feedback 与 structured repair decision 的组合 | PARTIAL | S1b / S3 / S5 |
| TTool-AI | NL → SysML / TTool、JSON / syntax / constraint tool feedback、公开 artifact | 不争 MBSE tool feedback 首创；只评估本任务下的可执行反馈链路 | PARTIAL | S1b / S3 / S5 |
| Designing FSMs | oracle / distinguishing / checking-sequence、trace / fault-model repair | 不争 trace repair 首创；聚焦 scenario candidates + deterministic simulator execution + structured fix decision | PARTIAL | S1b / S3 / S5 |

通过标准：四者不仅出现在参考文献或 Related Work 末段，而是每个 relevant claim 都能说明“它们已经覆盖什么、本文只保留什么边际”。

## 4. Baseline gate

| ID | 检查项 | 当前状态 | 最低验收标准 | 不通过时动作 |
|---|---|---|---|---|
| B1 | 是否至少规划 1 个 external same-sample approximate baseline | PARTIAL | 优先 Structure/Event SMF；备选 LLMs for EMP STM 子集 | 若不可行，主 claim 降级为 protocol / diagnostic study |
| B2 | 是否冻结 B0-B5 / EXT 的预算、反馈轮数、模型、输入上下文和 human budget | TODO | S3 前形成 budget table | 不进入主实验结果写作 |
| B3 | near / evidence-only work 是否中性描述，不写成 prior work weakness | PARTIAL | [evidence/baseline_and_related_work_matrix.md](./evidence/baseline_and_related_work_matrix.md) 保持分层 | S1b / S5 修改措辞 |
| B4 | post-hoc 评价与 in-loop feedback 是否分开 | TODO | 实验表明确 feedback source 是否进入下一轮 prompt | 不得声称 tool feedback 边际 |
| B5 | baseline normalization 是否说明 adapter / output mapping 对评分对象的影响 | TODO | S3 记录 mapping protocol 与不可比边界 | 不得横向排名 |

## 5. Sample 与 oracle gate

| ID | 检查项 | 当前状态 | 最低验收标准 | 不通过时动作 |
|---|---|---|---|---|
| S1 | main sample 是否优先 9 系统 / 101 需求，或有预注册降级理由 | TODO | S2 冻结 sample registry、排除规则、stress-test 与 main sample 区分 | 不写平均性能 claim |
| S2 | 是否避免只用 historical Top-15、成功样本或 reference-ready 样本 | TODO | historical / stress-test assets 与主样本分开 | 回到 S2 重建样本 frame |
| S3 | 主质量 oracle 是否由至少 2 名独立 human annotator 支撑 | TODO | blind component-level adjudication、agreement、仲裁 | LLM judge / 单人判断不得进入主结果 |
| S4 | scenario relevance 与 trace 解释是否有人类复核机制 | TODO | rubric 明确哪些 scenario 可用于质量判断 | simulation 结果只能作辅助证据 |
| S5 | 样本、oracle、baseline budget 是否在实验前冻结 | TODO | S2/S3 gate 通过后才能跑主实验 | 后跑规则不能反向解释结果 |

## 6. Claim-evidence gate

| ID | 检查项 | 当前状态 | 允许进入 manuscript 的条件 | 不通过时动作 |
|---|---|---|---|---|
| C1 | 结果型 improvement / superiority claim 是否已有主实验和 human adjudication 支撑 | TODO | G3/G5 结果闭合后才能升级 | G3/G5 前只能写 “we study / whether / evaluate” |
| C2 | 每个 contribution 是否能映射到 [story/claim_evidence_map.md](./story/claim_evidence_map.md) 的 safe wording | PARTIAL | Contribution 表逐条有 status、baseline coverage、evidence_needed | 未映射则删除或降级 |
| C3 | Agent orchestration 是否只作为 experimental condition，不作为独立贡献 | PARTIAL | E1/E2 写成 condition / RQ dimension | 删除 Hybrid method contribution 口径 |
| C4 | 过程性工程材料是否未进入 Method / Contribution 主线 | PARTIAL | 只保留对 artifact / reproducibility 必要的信息 | 删除“工程留痕即可信度贡献”的写法 |
| C5 | Claim 与 target venue 是否一致，且 venue 未反向扭曲 story | PARTIAL | [target_venue_decision.md](./target_venue_decision.md) §7 对后续 PR 有约束 | 回到 S0b 重审 venue route |

## 7. Artifact 与 reproducibility gate

| ID | 检查项 | 当前状态 | 最低验收标准 | 不通过时动作 |
|---|---|---|---|---|
| A1 | reviewer 是否能追踪输入需求、输出模型、诊断、scenario、repair decision 与统计口径 | TODO | artifact package 提供必要脱敏输入 / 输出摘要、版本与说明 | artifact gate 不通过，不硬投 |
| A2 | 模型、provider、prompt / tool setting 是否足以复核实验条件 | TODO | 记录模型 ID、关键配置、prompt 摘要或 hash、工具版本 | 不写可复现性强 claim |
| A3 | 失败类型是否有 taxonomy，而不是只展示成功案例 | TODO | invalid、non-converged、provider error、weak-oracle 等类别有纳入 / 排除规则 | 降级结果 claim |
| A4 | 内部表示 / parser / simulator 的能力边界是否披露 | TODO | artifact / appendix 说明 grammar subset、unsupported constructs、mapping limitation | 避免 DSL / verification overclaim |
| A5 | artifact 说明是否没有把工程过程包装成学术贡献 | PARTIAL | artifact 是复核材料，不是 Method 主线 | 回查 [story/terminology_policy.md](./story/terminology_policy.md) |

## 8. Threats 与 limitation gate

| ID | 检查项 | 当前状态 | 必须覆盖的 threat | 不通过时动作 |
|---|---|---|---|---|
| T1 | baseline fairness | TODO | same-sample approximate / near / evidence-only 分层、adapter 和预算差异 | 不得写直接胜出 prior work |
| T2 | sample bias | TODO | 系统覆盖、需求类型、排除理由、stress-test 分离 | 降级泛化 claim |
| T3 | oracle reliability | TODO | annotator、agreement、仲裁、LLM 辅助披露 | 主结果不得进入投稿稿 |
| T4 | provider drift / model availability | TODO | 模型版本、日期、不可复现风险 | 限定结果有效范围 |
| T5 | representation expressiveness | TODO | 不支持并行 region、完整 timed automata、LTL/BMC 等边界 | 不写 complete verification |
| T6 | LLM usage risk | TODO | 生成、评审、修复、辅助判断分别披露 | 补 LLM usage / disclosure 段落 |
| T7 | venue fit risk | PARTIAL | SoSyM / Automated Software Engineering Journal / Requirements Engineering Journal 切换条件与不得硬投条件 | 不为截点硬投 |

## 9. Writing gate

| ID | 检查项 | 当前状态 | grep / 人工检查建议 | 不通过时动作 |
|---|---|---|---|---|
| W1 | 标题 / 摘要不出现 `FCSTM`、`pyfcstm`、`new DSL`、`first NL-to-STM`、`first feedback loop` | TODO | 搜索 `FCSTM\|pyfcstm\|new DSL\|first NL-to-STM\|first feedback loop\|first trace repair` 并人工判断上下文 | 改成 executable / machine-checkable representation |
| W2 | Abstract v0 只写方向和研究问题，不写结果提升 | TODO | 搜索 `improve\|outperform\|show that` 并人工判断 | 改成 `we study / evaluate / investigate whether` |
| W3 | Related Work 第一层先处理四个 mandatory closest works | TODO | 搜索四个 work 名称是否集中出现在第一层 | S1b 重排章节 |
| W4 | Method 不主动讲工程过程材料 | TODO | 检查 Method heading 与 contribution bullets | 移到 artifact / appendix 或删除 |
| W5 | CCF-A readiness 不被误写成 CCF-A venue target | PARTIAL | 搜索 `CCF-A` 附近是否有 “目标投稿” | 改成 reviewer 强度 / 质量门禁 |
| W6 | 中英文术语一致 | PARTIAL | `machine-checkable`、`executable representation`、`deterministic diagnostics` 一致使用 | 统一术语表 |

## 10. LLM usage / disclosure gate

| ID | 检查项 | 当前状态 | 最低披露要求 | 不通过时动作 |
|---|---|---|---|---|
| L1 | LLM 在生成模型、生成 scenario、提出 repair、辅助 review 中的角色是否分开说明 | TODO | Method / Experiment / Limitations 分别说明 LLM 参与点 | 不得让 reader 误以为全 deterministic |
| L2 | LLM judge 是否没有作为主 oracle | TODO | LLM 只能辅助 triage / second-look，主结论依赖 human adjudication | 删除或降级 LLM judge 结论 |
| L3 | 使用 LLM 写作或辅助分析是否按 venue policy 披露 | TODO | S6 submission QA 按目标 venue 要求填写 disclosure | 投稿前补 disclosure |
| L4 | provider drift 与模型版本风险是否进入 threats | TODO | 记录模型版本、日期、provider 变化风险 | 限定结论有效范围 |

## 11. 投稿前 stop/go 判定

| 判定 | 条件 | 动作 |
|---|---|---|
| Go SoSyM regular | Novelty、mandatory closest works、baseline、sample/oracle、claim-evidence、artifact、threats、writing、LLM disclosure 无未闭合 C/I；论文主线仍以 modeling artifact quality 和 executable feedback 为核心 | 准备 SoSyM regular 投稿包 |
| Switch to Automated Software Engineering Journal | 自动化闭环、tool-supported workflow 和 ablation 边际成为最强证据；同时 baseline / oracle / artifact gate 闭合 | 按 ASE Journal 叙事重写 abstract / intro |
| Switch to REJ | requirements-to-behavioral-model、traceability、human adjudication 和需求歧义分析成为最强证据 | 扩展 RE related work 与 traceability 证据 |
| Hold | 任一 C 级 gate 未闭合，或多个 I 级 gate 只能靠措辞掩盖 | 不硬投，回到对应 S1b/S2/S3/S4/S5 修复 |

## 12. 当前 S0b 结论

- 当前默认主投仍为 SoSyM regular rolling。
- 当前 CCF-A readiness 只达到 checklist 初始化，不代表论文已满足 CCF-A 稿件质量。
- S2/S3/S4/S5 都必须继承本 checklist；任何结果型 claim 在 evidence 闭合前都不得升级。
- 如果后续证据不支持 SoSyM 主线，应按 [target_venue_decision.md](./target_venue_decision.md) 的切换条件转 ASE Journal 或 Requirements Engineering Journal，而不是在同一 story 中硬塞不匹配叙事。
