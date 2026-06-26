# 术语策略：S0-v2 智能体辅助 SLR 论文

## 1. 目的

本文术语容易与传统 SLR、系统映射研究、PRISMA 报告、自动筛选工具、LLM 生成综述文本和通用 agentic workflow 混淆。本文件冻结 PR-S0-v2 阶段的术语口径，后续写摘要、引言、方法、协议、评价或 PR comment 时应优先遵守。

## 2. 核心术语

| 术语 | 推荐口径 | 避免误读 |
|---|---|---|
| 研究者引导的智能体式 SLR/SMS 支持方法 | 面向 SE SLR/SMS 的方法：研究者定义问题框架、批准 schema、解释统计、质疑候选 finding 并裁决 final finding；agent 只辅助执行和生成候选信号。 | 不等于端到端无人自动 SLR，也不等于自动写综述。 |
| Review meta-model scaffold / 综述元模型脚手架 | 帮助研究者声明 topic、RQ、scope、对象、关系、证据类型和 finding 类型的可配置模板。 | 不是作者预设的通用软件工程本体，也不是 LLM 自动生成的最终模型。 |
| Topic-specific review meta-model / 主题特定综述元模型 | 研究者针对具体 SLR/SMS 主题实例化后的工作模型。 | 不等于可直接执行的抽取字段表；还需要投影为 dimension schema。 |
| Dimension pattern / extraction schema / 维度模式 | meta-model 在单篇论文分析任务上的字段化、树状/类型化、可版本化投影，包括字段、取值空间、证据要求、缺失值语义和 backfill 规则。 | 不是一次性平铺字段表，也不是 prompt 中的隐含 checklist。 |
| Pattern-evolving / 模式演化 | dimension schema 随 seed papers、survey-of-surveys scaffold、抽取失败、新类别和研究者理解深化而修订，并保留版本、影响范围和 backfill 状态。 | 不表示 agent 可以绕过研究者自行改 schema。 |
| Survey-of-surveys scaffold | 从既有 SE / AI4SE / MDE / LLM4SE survey、SLR、SMS 中低成本抽取 dimension / finding / evidence-presentation patterns。 | 不是目标 SLR corpus，不进入 target-domain finding evidence pool，不是 PRISMA tertiary review。 |
| Seed-paper probing | 用少量种子论文压力测试候选 dimension schema 是否可执行。 | 不代表完整 corpus 结论，也不决定最终 meta-model。 |
| Overview card | 对候选论文的初步元信息、范围、全文状态和粗粒度相关性记录。 | 不等于字段级 evidence object，也不支撑 final finding。 |
| Field-level content evidence / 字段级内容证据 | 来自目标论文原文或元数据的可定位证据：section/page/quote/table/figure/artifact URL/缺失原因/不确定说明。 | 不是普通摘要，不是 process log。 |
| Evidence table / 字段证据表 | 在 researcher-approved dimension schema 下抽取得到的字段值与 source anchors。 | 不等于 final finding，也不等于统计结论。 |
| Statistical analysis / 统计分析 | 对字段证据表做频次、分布、交叉表、趋势、覆盖率、矛盾信号等描述性/归纳性分析。 | 不是 final research finding。 |
| Statistical output / statistical observation / 统计观察 | statistical analysis 的输出，如分布表、趋势或覆盖代理。 | 避免写成 statistical finding；若使用“finding”一词必须注明不是 research finding。 |
| Finding heuristic / finding pattern | 指导 agent 从统计观察和 content evidence 中提出 candidate finding signals 的启发式，如 gap、trend、consensus、contradiction、maturity。 | 不保证 finding 为真。 |
| Candidate finding signal / 候选发现信号 | agent 基于统计观察、finding heuristic 和 content evidence 提出的待审计线索。 | 不是 final finding，不应进入摘要或结论。 |
| Target-domain research finding / 目标领域研究发现 | 基于目标论文 content evidence、统计分析、反向证据、不确定性和研究者裁决形成的领域主张。 | 不能由 process evidence 或 agent 输出直接支撑。 |
| Method-evaluation finding / 方法评估发现 | 基于 pilot、学生过程数据、交互日志、成本、审计记录形成的关于方法本身的发现。 | 不能当作目标领域文献证据。 |
| Process evidence / audit trail / 过程证据 | 人机交互、schema revision、approval、challenge、adjudication、backfill、prompt/raw log、脱敏和成本记录。 | 只能支撑方法评估，不支撑 target-domain findings。 |
| Researcher challenge | 研究者围绕 candidate finding 提出证据不足、反例、范围过宽、主张过强或 schema 不适配等质疑。 | 不是简单“人工通过”。 |
| Final adjudication | 研究者将 candidate finding 裁决为 accepted / downgraded / rejected / unresolved。 | 不是 agent 自动决定。 |
| Transparency package | claim-evidence map、排除理由、schema revision、audit log、类 PRISMA 材料等透明制品。 | 不等于自动生成最终论文，也不等于 PRISMA 合规。 |

## 3. Finding 与分析状态

| 状态 | 定义 | 可写入论文的位置 |
|---|---|---|
| Statistical observation | 字段表上的统计观察，例如某类方法占比、artifact availability 覆盖率。 | 结果表、分析材料；不能直接写成最终研究发现。 |
| Candidate finding signal | agent 提出的可能 finding 线索。 | 方法、案例、审计过程；不能写成结论。 |
| Challenged finding | 已被研究者质疑并要求补证、反例或降级。 | 质疑日志、错误分析。 |
| Downgraded finding | 原主张过强，被缩小范围或降低强度。 | 结果/讨论中可写，但必须说明降级理由。 |
| Accepted target-domain finding | 经 content evidence、counter-evidence 与研究者裁决接受。 | 可作为目标领域研究发现。 |
| Unresolved finding | 证据不足或冲突过大，暂不进入强结论。 | 局限、后续工作、未解决台账。 |
| Method-evaluation finding | 关于方法可用性、成本、审计性、失败模式的发现。 | 方法评估结果；不能混入领域 finding。 |

## 4. Human gate 术语

Human gate 不是一句“人工审核”，必须至少包含：input artifact、decision type、rationale、versioned change、impact scope、downstream action、actor / timestamp、eligibility consequence。

| Gate | 推荐名称 | 作用 |
|---|---|---|
| G0 | meta-model approval | 批准 topic/RQ/scope/meta-model。 |
| G1 | dimension schema approval | 批准可执行抽取 schema。 |
| G2 | schema revision / backfill gate | 批准 schema 变更、影响分析和回填策略。 |
| G3 | statistical-analysis protocol gate | 批准统计分析输入版本、方法和限制。 |
| G4 | candidate finding challenge gate | 质疑候选 finding 的证据、反例、范围和主张强度。 |
| G5 | final adjudication gate | 裁决 accepted / downgraded / rejected / unresolved。 |
| G6 | process evidence boundary gate | 审批日志、脱敏、consent、发布边界。 |

## 5. PRISMA 与 survey-of-surveys 术语

| 术语 | 使用规则 |
|---|---|
| PRISMA-compliant | 禁止在检查清单未闭合前作为正向主张。 |
| PRISMA-style / 类 PRISMA | 可用于透明材料、flow、排除理由台账；必须说明不是合规声明。 |
| PRISMA-informed | 可用于说明受透明报告思想启发。 |
| Survey-of-surveys | 只作为 scaffold mining / pattern prior；不写 complete coverage，不写 tertiary review。 |
| Target SLR evidence pool | 目标领域 SLR 的论文证据池；不包含 survey-of-surveys scaffold，除非该 survey 本身是目标 corpus 的纳入论文并按相同规则处理。 |

## 6. 禁止或高风险写法

| 写法 | 处理 |
|---|---|
| 智能体完全替代 SLR 专家 | 禁止主张。 |
| 端到端无人自动产出合格 SLR | 禁止主张。 |
| first automated SLR / first agentic SLR | 禁止主张。 |
| PRISMA-compliant | 未完成检查清单前禁止作为正向主张。 |
| complete coverage | 禁止；只能写 coverage proxy。 |
| LLM defines the review meta-model | 改为“LLM 可建议，研究者负责实例化和批准”。 |
| LLM/agent produces final findings | 改为“agent produces candidate finding signals; researcher adjudicates final findings”。 |
| statistical analysis shows final finding | 改为“statistical observation motivates candidate finding; final finding requires evidence audit”。 |
| process evidence supports target-domain finding | 禁止；process evidence 只支持 method-evaluation findings。 |
| survey-of-surveys proves target-domain finding | 禁止；它只提供 pattern scaffold。 |
| pilot proves generalization | 禁止；pilot 只验证 closure / feasibility / artifact completeness。 |
| student logs show field state | 禁止；学生日志只能评价方法过程。 |
| researcher merely validates final report | 改为“researcher owns meta-model, schema, challenge, adjudication and process boundary”。 |

## 7. 中文写作要求

正式 Markdown 说明以中文为主。必要英文术语可以作为锚点保留，但应配中文解释；不要整段英文堆叠。论文后续英文稿另行维护，不在 PR-S0-v2 阶段生成。

## 8. PR #97 术语口径

PR #97 当前必须称为 OPEN / 未合入 / snapshot / 分支局部证据。除非后续 PR #97 merge 并按 [../evidence/fact_drift_policy.md](../evidence/fact_drift_policy.md) 更新，否则不得称为 `main` 已合入资产。
