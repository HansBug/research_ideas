# 审稿风险登记表：S0-v2 智能体式系统综述支持方法

## 1. 口径

本文件登记 PR-S0-v2 阶段可预见的审稿风险。C/I/M 在这里表示对论文成立性、证据链或实验可靠性的潜在影响，不等同于普通工程 bug 等级。

术语规则沿用 [../story/terminology_policy.md](../story/terminology_policy.md)：同一文档中，关键术语首次出现写作“中文术语（英文术语 / 缩写）”，后续使用中文主称。本文件首次锚定：软件工程（Software Engineering, SE）、系统综述（Systematic Literature Review, SLR）、维度模式（dimension pattern / extraction schema）、领域发现（target-domain research finding）、过程证据（process evidence / audit trail）和人在回路（human-in-the-loop）。除禁用词检索式、论文名、工具名、路径和固定缩写外，风险描述均使用中文主称。

## 2. 风险表

| ID | 类别 | 风险 | 等级 | 触发条件 | 缓解入口 | 当前状态 |
|---|---|---|---:|---|---|---|
| R1 | 叙事回滑 | 第二篇被写回 `sources/` 语料 / 基准来源全景论文。 | C | 标题、摘要或贡献以文库规模为主贡献。 | [../story/paper_story.md](../story/paper_story.md)、[../story/claim_evidence_map.md](../story/claim_evidence_map.md)。 | PR-S0-v2 已禁止。 |
| R2 | 主张过强 | 正向声称 PRISMA 透明报告框架合规。 | C | 检查清单未闭合却写英文禁用词 `PRISMA-compliant` 或中文“PRISMA 透明报告框架合规”。 | [../story/terminology_policy.md](../story/terminology_policy.md)、[../story/claim_evidence_map.md](../story/claim_evidence_map.md)。 | 已禁止。 |
| R3 | 主张过强 | 正向声称完整覆盖、首次自动化系统综述或首次智能体式系统综述。 | C | 摘要 / 引言出现无证据首创或覆盖声明。 | [../story/differential_novelty_matrix.md](../story/differential_novelty_matrix.md)。 | 已禁止。 |
| R4 | 专家替代误读 | 写成智能体完全替代系统综述专家。 | C | 方法叙事去掉研究者所有权或人工门控。 | [../story/paper_story.md](../story/paper_story.md)、[../story/terminology_policy.md](../story/terminology_policy.md)。 | 已禁止。 |
| R5 | 事实漂移 | 把 PR #97 OPEN / 快照资产写成 `main` 事实。 | C | 引用 438→69→25 或 25 篇全文但不标 OPEN / 快照。 | [../evidence/fact_drift_policy.md](../evidence/fact_drift_policy.md)。 | 已建政策。 |
| R6 | 双头主线 | 一边讲软件工程特定综述元模型，一边讲证据链，却没有用维度模式生命周期与发现形成串起来。 | C | 论点 / 方法图缺少模式演化、统计观察到研究发现的转移、研究者裁决。 | [../story/paper_story.md](../story/paper_story.md)、[../story/protocol.md](../story/protocol.md)。 | S0-v2 主线已收敛，待复审。 |
| R7 | 统计分析被误写成最终发现 | 把频次、分布、交叉表、趋势等统计观察直接写成开放性研究发现。 | C | 出现“统计发现”、英文禁用词 `statistical finding`，或写成统计分析直接证明最终发现。 | [../story/terminology_policy.md](../story/terminology_policy.md)、[../story/claim_evidence_map.md](../story/claim_evidence_map.md)。 | S0-v2 已显式禁止。 |
| R8 | 内容证据 / 过程证据混用 | 用过程证据或学生交互日志支撑领域发现。 | C | 把试运行日志、学生交互、提示日志当作目标领域文献证据。 | [../story/protocol.md](../story/protocol.md)、[evaluation_dimensions_seed.md](./evaluation_dimensions_seed.md)。 | S0-v2 已分层。 |
| R9 | 综述之综述误定位 | 把综述之综述写成目标证据池、完整三级综述或 PRISMA 三级综述。 | C | 综述之综述产出被用于证明目标领域发现，或写完整覆盖。 | [../story/protocol.md](../story/protocol.md)、[../story/claim_evidence_map.md](../story/claim_evidence_map.md)。 | S0-v2 已禁止。 |
| R10 | 人在回路退化 | 人在回路只在末端签字，未贯穿综述元模型、维度模式、修订、统计分析、质疑和裁决。 | C | 方法图只有最后人工审核，缺 G0--G6 人工门控。 | [../story/paper_story.md](../story/paper_story.md)、[../story/protocol.md](../story/protocol.md)。 | S0-v2 已要求多门控。 |
| R11 | 维度模式平铺化 | 维度模式写成一次性字段表，无版本、修订、影响分析和回填。 | C | A2/A3 只给字段清单，不记录模式生命周期。 | [../story/protocol.md](../story/protocol.md)、[evaluation_dimensions_seed.md](./evaluation_dimensions_seed.md)。 | S0-v2 已要求生命周期。 |
| R12 | 试运行过度外推 | 试运行或学生使用数据被写成方法泛化证明。 | C | 试运行结果被写成跨主题有效、优于人工、已证明完整方法。 | [../story/claim_evidence_map.md](../story/claim_evidence_map.md)、[../story/paper_outline.md](../story/paper_outline.md)。 | S0-v2 已降级。 |
| R13 | 学生数据伦理与脱敏风险 | 收集硕士生人机交互数据但未冻结同意、匿名化、脱敏、教学关系隔离和访问权限。 | C | A5/A4 记录原始提示 / 用户数据却无脱敏政策。 | [evaluation_dimensions_seed.md](./evaluation_dimensions_seed.md)、后续伦理 / 数据边界 PR。 | 待 A5。 |
| R14 | 新颖性不足 | 忽略 AgentSLR、LatteReview、EviSearch、LR-Robot、TrialMind、WSESE@ICSE 2025 或综述生成工作。 | I | 相关工作只讲传统系统综述，不讲 B0 强近邻。 | [../story/differential_novelty_matrix.md](../story/differential_novelty_matrix.md)、[../baselines/SUMMARY.md](../baselines/SUMMARY.md)。 | PR-S0-v2 已登记，A6 需深化。 |
| R15 | 综述之综述脚手架循环依赖 | 用综述之综述抽出的模式反过来证明综述之综述本身完整或证明目标领域结论。 | I | 模式先验与目标证据池未隔离。 | [../story/protocol.md](../story/protocol.md)。 | 已列边界，后续脚手架 PR 需审。 |
| R16 | 评价薄弱 | 只有回顾型回放，没有模式演化、发现质疑或过程数据评价。 | I | A3/A5 只复盘已知论文表，不评价 L0--L7。 | [evaluation_dimensions_seed.md](./evaluation_dimensions_seed.md)、[../story/paper_outline.md](../story/paper_outline.md)。 | 待 A3/A5。 |
| R17 | 审计黑箱 | 人工门控没有输入、决策、理由、版本、影响范围、下游动作和成本。 | I | A5 只说人工复核通过。 | [../story/protocol.md](../story/protocol.md)、[evaluation_dimensions_seed.md](./evaluation_dimensions_seed.md)。 | 待 A2/A5。 |
| R18 | 幻觉 / 无证据支撑发现未测 | 没有陷阱论文、金事实 / 银事实或无证据支撑发现检查。 | I | A3/A5 没有针对候选发现的错误集。 | [../dataset_selection/sample_assets.md](../dataset_selection/sample_assets.md)、[evaluation_dimensions_seed.md](./evaluation_dimensions_seed.md)。 | 待 A3。 |
| R19 | 引用蔓延 / 未核验引用扩张 | 用搜索摘要或未核验元数据写相关工作。 | I | 引用种子未分层或 BibTeX 伪造。 | [../evidence/citation_seed_inventory.md](../evidence/citation_seed_inventory.md)。 | 需 A6 审。 |
| R20 | 工程日志冒充贡献 | 把运行日志、提示或智能体框架写成论文新颖性。 | M | 方法过度描述工具实现而非研究问题。 | [../story/paper_story.md](../story/paper_story.md)、A4/A5。 | 后续关注。 |
| R21 | 场景越界 | 把后续场景或“四个真实例子”误写成当前已冻结基准。 | M | A3/A4 直接继承候选场景且无审计计划。 | [../story/paper_outline.md](../story/paper_outline.md)、[../dataset_selection/sample_assets.md](../dataset_selection/sample_assets.md)。 | S0-v2 已声明不冻结。 |
| R22 | 强协议 / 弱证据 | 只把 L0--L7 和 G0--G6 写成流程图，缺少可导出审计制品链、最小闭环样例和评价指标。 | C | 摘要 / 方法声称审计优先，但没有字段证据表、候选发现台账、质疑 / 裁决日志或样例。 | [../story/paper_story.md](../story/paper_story.md)、[../story/protocol.md](../story/protocol.md)、[evaluation_dimensions_seed.md](./evaluation_dimensions_seed.md)。 | 本轮已把审计制品链和最小闭环样例列为后续阻塞性义务。 |
| R23 | 评价错位 | 只报告效率、文本质量或主观满意度，没有把强近邻威胁转成证据锚点、断链、过强主张、回填负担和质疑拦截等指标。 | C | A5 评价指标只看时间、token 或用户满意度。 | [evaluation_dimensions_seed.md](./evaluation_dimensions_seed.md)。 | 本轮已新增 risk-to-metric 口径，A5 需冻结公式和阈值。 |
| R24 | 领域换皮 | 只说软件工程场景不同，但没有用 LLM4STM / LLM4Modeling 等主题展示 SE 文献对象为何需要模式演化和审计链。 | I | 引言只强调领域不同，缺少种子论文 dry-run 或抽取对象差异。 | [../story/paper_story.md](../story/paper_story.md)、[../story/paper_outline.md](../story/paper_outline.md)。 | 本轮要求最小闭环样例优先用 LLM4STM / LLM4Modeling。 |

## 3. 高风险 grep 线索

以下为英文禁用词检索式，仅作为 grep 线索；正文风险名仍应使用中文主称。命中不一定必然错误，但若出现在正向主张、摘要、贡献或结论语境中，应至少列为 I 级；若直接破坏证据边界或导师定调，应列为 C 级。

```bash
grep -R "first agentic\|first automated\|PRISMA-compliant\|complete coverage\|statistical finding\|LLM final\|process evidence supports target\|student data shows\|pilot proves\|tertiary review" project_1_llm_state_machine_modeling/paper_agent_based_slr
```
