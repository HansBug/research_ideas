# 术语策略：智能体辅助 SLR 论文

## 1. 目的

本文术语容易与传统 SLR、系统映射研究（systematic mapping）、PRISMA 报告、自动筛选工具、LLM 生成综述文本混淆。本文件冻结 PR-S0 阶段的术语口径，后续写摘要、引言、方法、协议、评价或 PR comment 时应优先遵守。

## 2. 推荐术语

| 术语 | 推荐口径 | 避免误读 |
|---|---|---|
| 智能体辅助 SLR（agent-based SLR） | 将 SLR / 系统映射研究的多个环节组织成智能体执行或辅助的工作流，并设置人工审计门。 | 不等于端到端无人自动 SLR。 |
| 研究者引导的智能体式 SLR 支持工作流（researcher-guided agentic SLR support workflow） | 研究者基于综述元模型脚手架裁剪并实例化主题特定综述元模型，再让智能体在该框架下提出候选研究发现并接受审计。 | 不等于系统自动定义最终研究结论。 |
| 综述元模型脚手架（review meta-model scaffold） | 帮助研究者声明 / 裁剪综述对象、关系、证据字段、研究发现类型和范围约束的可配置模板。 | 不是 UML/MDE 意义上的完整元模型；不是作者预设的通用软件工程本体。 |
| 主题特定综述元模型（topic-specific review meta-model） | 研究者针对具体 SLR/SMS 主题实例化后的工作模型。 | 不是 LLM 自动最终决定的 schema。 |
| 研究者批准的可执行 schema（researcher-approved executable schema） | 由系统辅助生成、经研究者确认后供智能体执行的字段和约束。 | 不是自动编译出的不可审计黑箱规则。 |
| 证据对象（evidence object） | 从论文中抽取、带来源锚点的可复核证据单元。 | 不是普通摘要或模型自由总结。 |
| 研究发现模式脚手架（finding pattern scaffold） | 约束候选研究发现类型、结构和证据要求的模式集合。 | 不保证研究发现为真，只约束候选研究发现如何生成和审计。 |
| 候选研究发现（candidate finding） | 智能体基于证据对象和研究发现模式提出、等待审计的研究发现。 | 不能直接写成最终研究发现。 |
| 最终研究发现（final finding） | 研究者接受主张强度、范围、支持性 / 反向证据后确认的研究发现。 | 不是 LLM 输出后的默认状态。 |
| 研究者审计（researcher audit） | 研究者对 schema、证据链、候选研究发现、主张强度的显式审计。 | 不等于最后润色报告。 |
| 研究者质疑闭环（researcher challenge loop） | 研究者对候选研究发现发起质疑，系统补证、找反例、修订或降级的闭环。 | 不要求 PR-S0 实现 UI，但必须作为方法闭环。 |
| 主张强度（claim strength） | 研究发现的主张强度等级，由证据与研究者审计决定。 | 不是 LLM confidence。 |
| 智能体执行的工作流（agent-executed workflow） | 智能体执行或辅助检索、筛选、抽取、编码、研究发现提出、证据链构建、报告投影。 | 不等于单个 prompt 或单次 LLM response。 |
| 人工审计门（human audit gate） | 人类在协议批准、元模型批准、证据审计、研究发现审计、最终主张复核中的显式审计节点。 | 不等于人工全文重做所有 SLR 环节。 |
| SLR | 围绕明确 RQ 系统识别、筛选、评价、抽取和综合证据的方法。 | 不等于普通叙事综述。 |
| 系统映射研究（systematic mapping） | 更偏分类、taxonomy、覆盖分布和领域结构刻画。 | 不等于完整效果综合或 meta-analysis。 |
| 证据包（evidence package） | 围绕候选研究发现组织的可复核证据制品，包括证据对象、来源锚点、支持性 / 反向证据、编码决策、质疑日志、修订历史和最终状态。 | 不等于普通运行日志。 |
| 可追踪性（traceability） | 每个报告级主张能追溯到论文、检索、筛选、抽取、编码、证据定位与审计状态。 | 不等于只在文末放参考文献。 |
| 来源追溯（provenance） | 记录数据、全文、元数据、查询、运行、人工审计的来源和版本。 | 不等同于最终主张正确性。 |
| 可审计性（auditability） | 第三方能复查流程、证据链、分歧、失败与修正。 | 不等于完全自动验证正确。 |
| 事实准确性（factuality） | 抽取字段、引用、venue、DOI、结论与来源事实一致。 | 不等于研究问题已被完整回答。 |
| 幻觉（hallucination） | 生成不存在论文、错误引用、错误事实或无证据主张的问题统称。 | 应进一步分类，不要只泛泛写幻觉。 |
| 无证据支撑的主张（unsupported claim） | 没有可定位来源、抽取记录或审计状态支撑的主张。 | 可能不是编造，但仍不可进入强结论。 |
| 金事实（gold fact） | 人工高置信核验或官方来源确认的事实锚点。 | 不等于完整真值机。 |
| 银事实（silver fact） | 由可信元数据、全文证据或半自动核验形成但仍需抽检的事实。 | 不等于可无条件作为最终真值。 |
| 覆盖代理（coverage proxy） | 已知条目召回、种子论文恢复、数据库重叠等覆盖代理。 | 禁止把它写成真实召回率或完整覆盖。 |

## 3. 研究发现生命周期术语

| 术语 | 推荐口径 | 避免误读 |
|---|---|---|
| 候选（candidate） | 处于候选状态、待审计的研究发现或主张。 | 不是最终结论。 |
| 已质疑（challenged） | 研究者已对证据、范围或主张强度提出质疑。 | 不是失败；只是进入复核。 |
| 已修订（revised） | 系统在质疑后补证、找反例或收窄范围。 | 不是自动升级为最终研究发现。 |
| 已降级（downgraded） | 研究发现不能支撑原始强度，需弱化主张或缩小范围。 | 不是无价值；只是不能写强主张。 |
| 已接受（accepted） | 研究者认可该研究发现及其证据链。 | 只有此状态才可写成最终研究发现。 |
| 未解决（unresolved） | 证据不足或冲突过大，暂不进入结论。 | 不是错误；是审计结果的一种。 |

## 4. PRISMA 相关术语

| 术语 | 使用规则 |
|---|---|
| PRISMA-compliant | 禁止在检查清单未闭合前作为正向主张；只能出现在禁止主张或风险语境中。 |
| PRISMA-style | 可用于描述类似 PRISMA flow、排除理由台账、透明报告材料，但必须说明不是合规声明。 |
| PRISMA-informed | 可用于说明设计受 PRISMA 透明报告思想启发，但不替代检查清单。 |

## 5. 禁止或高风险写法

| 写法 | 处理 |
|---|---|
| 智能体完全替代 SLR 专家 | 禁止主张。 |
| 端到端无人自动产出合格 SLR | 禁止主张。 |
| `first automated SLR` | 禁止主张；已有 ASReview、RobotReviewer、综述自动化等相关工作。 |
| `complete coverage` | 禁止主张；只能报告覆盖代理。 |
| `PRISMA-compliant` | 未完成检查清单前禁止作为正向主张。 |
| `sources/` 语料论文 | 禁止作为第二篇主线；只能作为案例、场景或证据来源。 |
| PR #97 已合入资产 | 禁止，除非 PR #97 状态变化并经 [fact_drift_policy.md](../evidence/fact_drift_policy.md) 更新。 |
| AgentSLR / LatteReview / EviSearch / LR-Robot / TrialMind / WSESE@ICSE 2025 | 必须正面对齐的强近邻，不能写成与本文无关或仅做背景。 |
| `LLM defines the review meta-model` | 改为“系统可以建议，研究者负责实例化和批准”。 |
| `generated findings` | 若无审计，必须写“候选研究发现”。 |
| `final findings produced by agents` | 禁止；最终研究发现必须经过研究者审计。 |
| `automated report generation as contribution` | 降级为下游报告呈现。 |
| `evidence chain proves truth` | 改为“证据链支持、挑战或限定某个研究发现”。 |
| `researcher merely validates final report` | 改为“研究者拥有元模型并审计研究发现”。 |

## 6. 中文写作要求

正式 Markdown 说明以中文为主。必要英文术语可以保留，但应配中文解释；不要整段英文堆叠。论文后续英文稿另行维护，不在 PR-S0 阶段生成。

## 7. PR #97 术语口径

PR #97 当前必须称为 OPEN / 未合入 / 快照 / 分支局部证据。除非后续 PR #97 merge 并按 [fact_drift_policy.md](../evidence/fact_drift_policy.md) 更新，否则不得称为 `main` 已合入资产。
