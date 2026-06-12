# baseline asset audit：PR-R1 资产审计总账

## 1. 结论摘要

PR-R1 的核心结论是：历史 baseline 并未作废，但它们不再主要承担“直接击败竞品”的角色，而是分层进入新主线：seed source、converter pressure、error taxonomy、limited comparison 和 related-work evidence。

当前最值得进入后续 R2/R3/R6 的高优先级资产是：

1. `structure-and-event-driven-frameworks...`：8 个 reactive-system descriptions、reference solutions、F1 workbook 与 4open artifact，最适合 external same-sample approximate 预演。
2. `llms_emp`：公开 Drive + 本地 parquet，适合抽 STM 子集作为 seed / judge 校准。
3. `ttool-ai`：公开 TTool artifact 与 results，适合作为 tool-feedback / SysML XML 转换压力。
4. `designing-fsm...`：CSV DFSM / trace-oracle repair 近邻，适合修正反馈对照，但不是控制系统真实数据。

不应升级为可运行主对照的资产包括：`req` 私有工业数据、FlowFSM 当前仓库壳、SpecGPT 私有 GT、Pushing Envelope 小样本无 artifact，以及多数 BPMN / TLA+ / LTL / STL / Event-B / PAT / Rebeca / Simulink 近邻。

## 2. R1 资产分层

| 层级 | 条件 | 当前数量 | 代表 | 用途 |
|---|---|---:|---|---|
| A | direct baseline + `ASSETS.md` 已补齐 | 9 | 见 [baseline_candidate_matrix.md](./baseline_candidate_matrix.md) | R2/R3/R6 的主要 prior artifact 候选。 |
| B | 强近邻 / 形式化反馈 / 过程模型 | 若干 | PAT-Agent、Event-B Agent、Rebeca、BPMN benchmark | related work、feedback taxonomy、converter boundary。 |
| C | `sources/` 真实控制系统样本 | 787 篇 | CARA、railway、PLC、UAV、elevator 等 | R2 自建 seed 的主要来源。 |
| D | #93/#94/#96 分支局部资产 | branch-local | S1a 九大 baseline、S0a story、PR #9 sample pool | cite-only / defer-to-R2，不作为 main 事实。 |

## 3. 对论文 story 的影响

1. 不能再把 novelty 写成“没有 LLM 做状态机生成”。九个 direct baseline 已覆盖直接生成、协议 FSM 抽取、SysML/PlantUML/Umple/TTool 等路径。
2. 可以把 novelty 收缩到：给定 `<NL, STM_0>` 后，如何利用结构化诊断、场景/仿真反馈、回归检查、接受/拒绝/回滚协议改善 seed，并记录失败与不收敛。
3. Baseline 的公平比较应降级为 limited / near / evidence-only 分层：只有 artifact 足够、输入输出可归一、预算可冻结时才进入近似对照。
4. 论文应主动报告转换风险：若 improvement 来自格式清洗或人工补字段，不能算修正循环收益。

## 4. Handoff 到后续 PR

| 后续 PR | R1 handoff |
|---|---|
| R2 | 从 `sources/` 与 A 层资产中冻结四例 seed；必须记录为何选 / 不选。 |
| R3 | 根据 [format_conversion_matrix.md](./format_conversion_matrix.md) 冻结最小转换器合同。 |
| R4 | 基于候选资产的缺陷类型冻结诊断 / 场景 / 评价门，而不是从 R5 结果倒推指标。 |
| R6 | 使用 [artifact_availability_ledger.md](./artifact_availability_ledger.md) 判断哪些 prior work 能进入 near-approximate comparison。 |
| R7 | Related Work 按 direct / near / evidence-only / boundary 写作，不做硬排名。 |

## 5. 未闭合风险

1. R1 未逐篇深审 91 篇 baseline 的代码与 artifact，只对高优先级 direct baseline 和部分强近邻做矩阵化重排。
2. R1 未重新联网下载 artifact；活链接仍需在正式实验前冻结。
3. R1 未选择四例样本；任何样本选择必须留给 R2。
4. R1 未实现转换器；任何“可转换”都是风险评估，不是已通过 adapter 测试。
