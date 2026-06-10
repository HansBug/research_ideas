# Path-1 投稿目标与 CCF-A 标准门禁

本文档把 issue [#67](https://github.com/HansBug/research_ideas/issues/67) 的投稿冲刺口径固化到 Path-1 第一篇论文 foundation 中：**按 CCF-A 论文标准打磨，2026 夏季优先投 CCF-B 期刊**。这里的“按 CCF-A 标准”不是指投稿 TSE / TOSEM，而是指用 CCF-A 期刊/会议 reviewer 会挑战的强度来约束 novelty、baseline、实验、oracle、artifact 和写作完整度，然后选择更稳妥、更贴合的 CCF-B rolling 期刊作为第一投。

## 1. 目标期刊优先级

| 优先级 | 目标出口 | CCF | 当前路线 | Path-1 叙事适配 | 决策 |
|---:|---|---:|---|---|---|
| 1 | SoSyM regular rolling | B | 常规滚动投稿；仓库入口见 [SoSyM 2026](../../../../ccf_venues/journal-b-sosym/2026/README.md) | software/system modeling、状态机建模质量、形式化/可执行反馈最贴合 | **默认主投** |
| 2 | Automated Software Engineering Journal regular rolling | B | 常规滚动投稿；仓库入口见 [ASE Journal 2026](../../../../ccf_venues/journal-b-ase/2026/README.md) | 若论文结果更强调 automated modeling、tool-supported repair loop、agentic workflow，则适配 | **第一备投** |
| 3 | Requirements Engineering Journal regular rolling | B | 常规滚动投稿；仓库入口见 [Requirements Engineering 2026](../../../../ccf_venues/journal-b-re/2026/README.md) | 若论文结果更强调 NL requirements representation、validation、requirements-to-behavioral-model，则适配 | **第二备投** |

不作为默认路线的出口：SoSyM Industry 5.0 theme、ASEJ Ex-ASE collection、REJ REFSQ 2026 collection 只能在投稿前人工核验来源资格、编辑意见和主题适配后再考虑；ESE / JSS / IST 只作为 2026-08 之后 story 明显转向 empirical / reliability / general SE 时的延后备选。

## 2. 三种 venue 叙事分流

| 叙事 | 对应出口 | 主文必须强调 | 不满足时的处理 |
|---|---|---|---|
| 建模质量 + 形式化反馈 | SoSyM | 状态机/系统建模问题、可执行表示、模型质量维度、可追溯 feedback-guided construction | 不硬投 SoSyM theme；转 regular 或备投 |
| 自动化软工 + 工具支撑修复 | ASE Journal | automation、repair loop、agentic/tool workflow、公平消融、可复现运行记录 | 只作为备投，不把工程框架写成贡献 |
| 需求到模型 + 验证/追踪 | Requirements Engineering Journal | NL requirements、ambiguity、requirements-to-behavioral-model、human adjudication、traceability | 若需求工程视角不强，不切 REJ |

## 3. CCF-A 标准门禁

下表是后续 S0-S7 必须满足的写作与实验底线。任何一项未过，都不能在 PR、摘要或引言中声称“已达到投稿级论文质量”。

| 维度 | CCF-A 标准下的最低要求 | 对 Path-1 的具体门禁 | 未通过动作 |
|---|---|---|---|
| Novelty | 正面处理最接近工作，不靠“first”类弱 novelty | 逐篇吸收 9 个五绿 direct baseline；禁用“首个 NL→STM / 首个反馈闭环” | 降级 claim；先补 S1a |
| Baseline | 不只和简单 prompt 比；必须包含外部强对手 | `Structure/Event SMF`、`llms_emp`、`TTool-AI`、`Designing FSMs` 必入 closest matrix；至少 1 个 same-sample approximate baseline | 不进入主实验结果写作 |
| 样本 | 防 cherry-pick；样本 frame、排除理由、stress-test 区分清楚 | 优先 9 系统 / 101 需求；若降级至少 `>=6` 系统 / `>=60` 需求并预注册原因 | 不写平均性能 claim |
| Oracle | 主质量结论不能依赖 LLM judge 或单人主观判断 | 至少 2 名独立 human annotator、blind coding、agreement、仲裁；LLM 只可辅助且披露 | 不允许主结果表进入投稿稿 |
| 消融 | 能证明 feedback 边际贡献，而不是只展示最终系统 | B0-B5：direct、structured、no-feedback、parse/metamodel、simulation、full method | 只能写 diagnostic / pilot |
| 可复现 | reviewer 能追踪输入、prompt、raw output、修复、失败和统计 | run record 保存 provider/model/date、prompt hash、raw/redacted output、usage、stage trace、FixLog、eligibility | artifact gate 不通过 |
| 结果表达 | 不报喜不报忧；失败、振荡、provider error 都要可追踪 | failure taxonomy、non-converged / invalid / provider_error eligibility filter | 降级 claim 或补实验 |
| 威胁分析 | 主动承认 baseline fairness、sample bias、oracle、provider drift、LLM usage | threats 与 risk register 必须逐项闭合 C/I | G5 strong review 不通过 |
| 写作完整性 | 像 CCF-A 稿件一样完整讲 story、方法、实验、威胁、artifact | G4 前 Introduction / Method / Experiments / Results / Threats / Related Work 全章节非空 | 暂停新实验，先补 manuscript |

## 4. 本 foundation PR 的直接约束

1. 当前 PR 只能把上述内容写成 **submission strategy / readiness gate**，不能写成“论文已经达到 CCF-A 标准”。
2. 后续 PR-S0 必须产出 `target_venue_decision.md`，明确 SoSyM regular 为默认主投，并列出 ASE Journal / Requirements Engineering Journal 的切换条件。
3. 后续 PR-S1a / PR-S1b 必须先过 baseline 门，再允许 PR-S3 / PR-S4 设计主实验。
4. 后续 PR-S5 / PR-S6 必须按 CCF-A 审稿强度做 claim-evidence closeout；若 C/I 未闭合，只能投延后版本，不能为了 2026-07-31 截点硬投。
