# 审稿风险登记表：S0-v2 智能体式 SLR 支持方法

## 1. 口径

本文件登记 PR-S0-v2 阶段可预见的审稿风险。C/I/M 在这里表示对论文成立性、证据链或实验可靠性的潜在影响，不等同于普通工程 bug 等级。

## 2. 风险表

| ID | 类别 | 风险 | 等级 | 触发条件 | 缓解入口 | 当前状态 |
|---|---|---|---:|---|---|---|
| R1 | 叙事回滑 | 第二篇被写回 `sources/` 语料 / 基准来源全景论文。 | C | 标题、摘要或贡献以文库规模为主贡献。 | [../story/paper_story.md](../story/paper_story.md)、[../story/claim_evidence_map.md](../story/claim_evidence_map.md)。 | PR-S0-v2 已禁止。 |
| R2 | 主张过强 | 正向声称 PRISMA 合规。 | C | 检查清单未闭合却写 `PRISMA-compliant`。 | [../story/terminology_policy.md](../story/terminology_policy.md)、[../story/claim_evidence_map.md](../story/claim_evidence_map.md)。 | 已禁止。 |
| R3 | 主张过强 | 正向声称完整覆盖、首次自动化 SLR 或首次智能体式 SLR。 | C | 摘要 / 引言出现无证据首创或覆盖声明。 | [../story/differential_novelty_matrix.md](../story/differential_novelty_matrix.md)。 | 已禁止。 |
| R4 | 专家替代误读 | 写成 agent 完全替代 SLR 专家。 | C | 方法叙事去掉研究者所有权或 human gates。 | [../story/paper_story.md](../story/paper_story.md)、[../story/terminology_policy.md](../story/terminology_policy.md)。 | 已禁止。 |
| R5 | 事实漂移 | 把 PR #97 OPEN / snapshot 资产写成 `main` fact。 | C | 引用 438→69→25 或 25 篇全文但不标 OPEN / snapshot。 | [../evidence/fact_drift_policy.md](../evidence/fact_drift_policy.md)。 | 已建政策。 |
| R6 | 双头 story | 一边讲 SE-specific meta-model，一边讲 evidence chain，却没有用 dimension pattern lifecycle 与 finding formation 串起来。 | C | thesis / 方法图缺少 pattern evolution、统计观察到 finding 的转移、human adjudication。 | [../story/paper_story.md](../story/paper_story.md)、[../story/protocol.md](../story/protocol.md)。 | S0-v2 主线已收敛，待复审。 |
| R7 | Statistical analysis 被误写成 final finding | 把频次、分布、交叉表、趋势等统计观察直接写成开放性 research finding。 | C | 出现 `statistical finding`、`statistical analysis proves/reveals final finding` 等正向写法。 | [../story/terminology_policy.md](../story/terminology_policy.md)、[../story/claim_evidence_map.md](../story/claim_evidence_map.md)。 | S0-v2 已显式禁止。 |
| R8 | Content/process evidence 混用 | 用 process evidence / student interaction logs 支撑 target-domain findings。 | C | 把 pilot logs、学生交互、prompt logs 当作目标领域文献证据。 | [../story/protocol.md](../story/protocol.md)、[evaluation_dimensions_seed.md](./evaluation_dimensions_seed.md)。 | S0-v2 已分层。 |
| R9 | Survey-of-surveys 误定位 | 把 survey-of-surveys 写成目标 evidence pool、complete tertiary review 或 PRISMA tertiary review。 | C | survey-of-surveys 产出被用于证明目标领域 finding，或写 complete coverage。 | [../story/protocol.md](../story/protocol.md)、[../story/claim_evidence_map.md](../story/claim_evidence_map.md)。 | S0-v2 已禁止。 |
| R10 | Human-in-the-loop 退化 | human-in-the-loop 只在末端 sign-off，未贯穿 meta-model、schema、revision、analysis、challenge、adjudication。 | C | 方法图只有最后人工审核，缺 G0--G6 gate。 | [../story/paper_story.md](../story/paper_story.md)、[../story/protocol.md](../story/protocol.md)。 | S0-v2 已要求多 gate。 |
| R11 | Dimension pattern 平铺化 | dimension pattern 写成一次性字段表，无 version / revision / impact / backfill。 | C | A2/A3 只给字段清单，不记录 schema lifecycle。 | [../story/protocol.md](../story/protocol.md)、[evaluation_dimensions_seed.md](./evaluation_dimensions_seed.md)。 | S0-v2 已要求 lifecycle。 |
| R12 | Pilot 过度外推 | pilot run 或学生使用数据被写成方法泛化证明。 | C | pilot 结果被写成跨主题有效、优于人工、已证明完整方法。 | [../story/claim_evidence_map.md](../story/claim_evidence_map.md)、[../story/paper_outline.md](../story/paper_outline.md)。 | S0-v2 已降级。 |
| R13 | Student data 伦理与脱敏风险 | 收集硕士生人机交互数据但未冻结 consent、匿名化、脱敏、教学关系隔离和访问权限。 | C | A5/A4 记录 raw prompt/user data 却无 redaction policy。 | [evaluation_dimensions_seed.md](./evaluation_dimensions_seed.md)、后续 ethics/data-boundary PR。 | 待 A5。 |
| R14 | 新颖性不足 | 忽略 AgentSLR、LatteReview、EviSearch、LR-Robot、TrialMind、WSESE@ICSE 2025 或综述生成工作。 | I | 相关工作只讲传统 SLR，不讲 B0 强近邻。 | [../story/differential_novelty_matrix.md](../story/differential_novelty_matrix.md)、[../baselines/SUMMARY.md](../baselines/SUMMARY.md)。 | PR-S0-v2 已登记，A6 需深化。 |
| R15 | Survey-of-surveys bootstrapping 循环依赖 | 用 survey-of-surveys 抽出的 pattern 反过来证明 survey-of-surveys 本身完整或证明目标领域结论。 | I | pattern prior 与 target evidence pool 未隔离。 | [../story/protocol.md](../story/protocol.md)。 | 已列边界，后续 scaffold PR 需审。 |
| R16 | 评价薄弱 | 只有回顾型回放，没有 schema evolution、finding challenge 或 process-data 评价。 | I | A3/A5 只复盘已知论文表，不评价 L0--L7。 | [evaluation_dimensions_seed.md](./evaluation_dimensions_seed.md)、[../story/paper_outline.md](../story/paper_outline.md)。 | 待 A3/A5。 |
| R17 | 审计黑箱 | human gate 没有输入、决策、理由、版本、影响范围、下游动作和成本。 | I | A5 只说人工复核通过。 | [../story/protocol.md](../story/protocol.md)、[evaluation_dimensions_seed.md](./evaluation_dimensions_seed.md)。 | 待 A2/A5。 |
| R18 | 幻觉 / 无证据支撑 finding 未测 | 没有陷阱论文、gold/silver facts 或无证据支撑 finding 检查。 | I | A3/A5 没有针对 candidate finding 的错误集。 | [../dataset_selection/sample_assets.md](../dataset_selection/sample_assets.md)、[evaluation_dimensions_seed.md](./evaluation_dimensions_seed.md)。 | 待 A3。 |
| R19 | 引用蔓延 / 未核验引用扩张 | 用搜索摘要或未核验元数据写 related work。 | I | 引用种子未分层或 BibTeX 伪造。 | [../evidence/citation_seed_inventory.md](../evidence/citation_seed_inventory.md)。 | 需 A6 审。 |
| R20 | 工程日志冒充贡献 | 把 run logs / prompts / agent framework 写成论文新颖性。 | M | 方法过度描述工具实现而非研究问题。 | [../story/paper_story.md](../story/paper_story.md)、A4/A5。 | 后续关注。 |
| R21 | 场景越界 | 把后续场景或“四个真实例子”误写成当前已冻结基准。 | M | A3/A4 直接继承候选场景且无审计计划。 | [../story/paper_outline.md](../story/paper_outline.md)、[../dataset_selection/sample_assets.md](../dataset_selection/sample_assets.md)。 | S0-v2 已声明不冻结。 |

## 3. 高风险 grep 线索

reviewer 可用以下线索快速检查 category mistakes：

```bash
grep -R "first agentic\|first automated\|PRISMA-compliant\|complete coverage\|statistical finding\|LLM final\|process evidence supports target\|student data shows\|pilot proves\|tertiary review" project_1_llm_state_machine_modeling/paper_agent_based_slr
```

命中不一定必然错误，但若出现在正向 claim、摘要、贡献或结论语境中，应至少列为 I 级；若直接破坏证据边界或导师定调，应列为 C 级。
