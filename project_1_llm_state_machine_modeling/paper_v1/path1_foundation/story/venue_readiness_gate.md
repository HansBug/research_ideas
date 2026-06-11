# Path-1 投稿目标与 CCF-A 标准门禁

本文档把 issue [#67](https://github.com/HansBug/research_ideas/issues/67) 的投稿冲刺口径固化为 Path-1 第一篇论文的 **venue readiness 背景与质量门禁**：按 CCF-A 论文标准打磨，2026 夏季优先考虑 fit-first 的 CCF-B rolling journal。

重要边界：**S0a 不冻结最终投稿期刊**。本文档只为后续 S0b / PR-S0-Direction 提供 venue readiness 输入；最终 `target_venue_decision.md`、abstract v0 和投稿路线必须在 [paper_story.md](./paper_story.md)、[terminology_policy.md](./terminology_policy.md)、[claim_evidence_map.md](./claim_evidence_map.md) 与 [paper_outline.md](./paper_outline.md) 的 S0a story gate 通过后再冻结。

## 1. 目标期刊候选池（S0b 输入，不是 S0a 决议）

| 优先级 | 目标出口 | CCF | 当前路线 | Path-1 叙事适配 | S0b 决策状态 |
|---:|---|---:|---|---|---|
| 1 | SoSyM regular rolling | B | 常规滚动投稿；仓库入口见 [SoSyM 2026](../../../../ccf_venues/journal-b-sosym/2026/README.md) | software/system modeling、状态机建模质量、形式化/可执行反馈最贴合 | S0b 待冻结 |
| 2 | Automated Software Engineering Journal regular rolling | B | 常规滚动投稿；仓库入口见 [ASE Journal 2026](../../../../ccf_venues/journal-b-ase/2026/README.md) | 若论文结果更强调 automated modeling、tool-supported repair loop、agentic workflow，则适配 | S0b 待冻结 |
| 3 | Requirements Engineering Journal regular rolling | B | 常规滚动投稿；仓库入口见 [Requirements Engineering 2026](../../../../ccf_venues/journal-b-re/2026/README.md) | 若论文结果更强调 NL requirements representation、validation、requirements-to-behavioral-model，则适配 | S0b 待冻结 |

不作为默认路线的出口：SoSyM Industry 5.0 theme、ASEJ Ex-ASE collection、REJ REFSQ 2026 collection 只能在投稿前人工核验来源资格、编辑意见和主题适配后再考虑；ESE / JSS / IST 只作为 2026-08 之后 story 明显转向 empirical / reliability / general SE 时的延后备选。

## 2. 三种 venue 叙事分流

| 叙事 | 对应出口 | 主文必须强调 | 不满足时的处理 |
|---|---|---|---|
| 建模质量 + 形式化 / 可执行反馈 | SoSyM | 状态机/系统建模问题、machine-checkable representation、模型质量维度、feedback-guided construction | 不硬投 theme；转 regular 或备投 |
| 自动化软工 + 工具支撑修复 | ASE Journal | automation、repair loop、agentic/tool workflow、公平消融、必要实验披露 | 只作为备投；工程框架不写成贡献 |
| 需求到模型 + 验证/追踪 | Requirements Engineering Journal | NL requirements、ambiguity、requirements-to-behavioral-model、human adjudication、traceability | 若需求工程视角不强，不切 REJ |

S0b 选择 venue 时必须优先问：当前证据更支持哪种叙事，而不是先定 venue 再倒推 story。

## 3. CCF-A 标准门禁

下表是后续 S0b-S7 必须满足的写作与实验底线。任何一项未过，都不能在 PR、摘要或引言中声称“已达到投稿级论文质量”。

| 维度 | CCF-A 标准下的最低要求 | 对 Path-1 的具体门禁 | 未通过动作 |
|---|---|---|---|
| Novelty | 正面处理最接近工作，不靠 “first” 类弱 novelty | Structure/Event SMF、LLMs for EMP、TTool-AI、Designing FSMs 必入 Related Work 第一层；禁用“首个 NL→STM / 首个反馈闭环” | 降级 claim；回到 S0a/S1b |
| Baseline | 不只和简单 prompt 比；必须包含外部强对手或明确降级 | 至少 1 个 same-sample approximate baseline 有计划；B0-B5 与 EXT 的预算和层级边界清楚 | 不进入主实验结果写作 |
| 样本 | 防 cherry-pick；样本 frame、排除理由、stress-test 区分清楚 | 优先 9 系统 / 101 需求；若降级至少 `>=6` 系统 / `>=60` 需求并预注册原因 | 不写平均性能 claim |
| Oracle | 主质量结论不能依赖 LLM judge 或单人主观判断 | 至少 2 名独立 human annotator、blind coding、agreement、仲裁；LLM 只可辅助且披露 | 不允许主结果表进入投稿稿 |
| 消融 | 能证明 feedback 边际贡献，而不是只展示最终系统 | B0-B5：direct、structured、no-feedback、diagnostics-only、simulation-feedback、full structured repair | 只能写 diagnostic / pilot |
| 可复现 | reviewer 能追踪关键输入、模型配置、脱敏输出摘要、失败类型和统计口径 | 必要复现信息覆盖模型 / 工具版本、prompt hash、必要脱敏输出摘要、诊断 / 场景轨迹、版本信息与纳入 / 排除规则；不把过程性工程材料写成方法贡献 | artifact gate 不通过 |
| 结果表达 | 不报喜不报忧；失败、振荡、provider error 都要可追踪 | failure taxonomy、non-converged / invalid / provider_error 标记和纳入 / 排除规则 | 降级 claim 或补实验 |
| 威胁分析 | 主动承认 baseline fairness、sample bias、oracle、provider drift、LLM usage | threats 与 risk register 必须逐项闭合 C/I | G5 strong review 不通过 |
| 写作完整性 | 像 CCF-A 稿件一样完整讲 story、方法、实验、威胁、artifact | G4 前 Introduction / Method / Experiments / Results / Threats / Related Work 全章节非空 | 暂停新实验，先补 manuscript |

## 4. S0b 使用本文档的方式

1. S0b 必须先读取 [paper_story.md](./paper_story.md)、[terminology_policy.md](./terminology_policy.md)、[claim_evidence_map.md](./claim_evidence_map.md)、[paper_outline.md](./paper_outline.md) 和本文件，再写 `DIRECTION.md`、`abstract_v0.md`、`target_venue_decision.md`。
2. S0b 的 abstract v0 不得写 result-level improvement claim，除非 G3/G5 结果已经存在；若只是方向冻结，只能写 “we study / we evaluate”。
3. S0b 的 `target_venue_decision.md` 必须说明 SoSyM / ASEJ / REJ 的切换条件，以及哪些 C/I gate 未通过时不得硬投。
4. 后续 PR-S1b / PR-S3 必须先过 baseline 门，再允许 PR-S4 / PR-S5 设计主实验或写主结果。
5. 后续 PR-S5 / PR-S6 必须按 CCF-A 审稿强度做 claim-evidence closeout；若 C/I 未闭合，只能投延后版本，不能为了 2026-07-31 截点硬投。
