# PR-S0-v2 最小协议：模式演化与发现形成的智能体辅助 SLR

## 1. 协议目标

本协议定义 PR-S0-v2 阶段的最小方法边界。它不是最终实现、不是完整 JSON schema、不是 UI 设计，也不是 PRISMA 合规流程；它只规定后续 A2/A3/A4/A5/A6 必须保留的输入、输出、研究者 gate、证据类型和 finding 生命周期。

核心原则：**论文收集、维度模式驱动的论文分析、统计分析和 research finding 形成必须分层；agent 只能在研究者批准的 schema 下辅助执行和提出候选信号，final finding 必须经过研究者裁决。**

## 2. 证据类型

| 类型 | 来源 | 支撑对象 | 禁止误用 |
|---|---|---|---|
| Content evidence / 字段级内容证据 | 目标论文全文、元数据、图表、表格、artifact URL、原文片段、缺失说明 | 字段值、统计分析、candidate/final target-domain findings | 不能用 process log 替代；不能没有 source anchor 就写强主张。 |
| Process evidence / audit trail | 人机交互、schema revision、approval、challenge、adjudication、backfill、prompt/raw log、脱敏记录、时间成本 | method-evaluation findings、可审计性、成本、失败模式 | 不能支撑目标领域研究发现。 |

## 3. 阶段契约

| 阶段 ID | 阶段 | 输入 | 输出 | 必需审计信息 |
|---|---|---|---|---|
| L0 | 主题 / RQ / scope / meta-model 设定 | 研究者问题意识、初始 RQ、领域范围、种子论文 | topic brief、review meta-model、scope boundary | 研究者批准记录、版本、范围排除理由 |
| L1 | scaffold mining / seed probing | 既有 survey / SLR / SMS、种子论文、L0 meta-model | 候选 dimension patterns、finding heuristics、evidence-presentation patterns | 来源、采纳/拒绝理由、不是目标 evidence pool 的声明 |
| L2 | dimension schema 准备与批准 | L0 meta-model、L1 patterns、纳排标准 | researcher-approved dimension schema | 字段定义、取值空间、缺失值语义、证据要求、批准记录 |
| L3 | 论文收集与 overview | 数据库、查询式、候选论文池、L2 schema | search log、screening ledger、全文状态、overview cards | 查询式、命中数、排除理由、全文不可得记录、抽查记录 |
| L4 | 字段级证据抽取与 pattern evolution | 全文 / 元数据、approved schema、overview cards | evidence table、source anchors、uncertainty、revision/backfill log | page/section/quote/table/artifact anchor、字段置信、schema 变更触发原因 |
| L5 | statistical analysis | evidence table、分析协议、coverage proxy 定义 | distribution、frequency、cross-tab、trend、coverage proxy、contradiction signal | 分析协议、字段版本、纳入样本、统计限制 |
| L6 | candidate finding signal 生成 | statistical analysis、finding heuristics、content evidence | candidate finding ledger、support/counter evidence draft、claim strength draft | finding type、supporting evidence、counter-evidence、uncertainty、scope |
| L7 | researcher challenge / final adjudication | candidate ledger、证据链、研究者质疑 | accepted / downgraded / rejected / unresolved findings、challenge log、transparency package | 质疑内容、补证、反例、降级理由、裁决人、时间、残余风险 |

## 3.1 横切过程证据集合

Process evidence 不是新的主流程阶段，也不改变 L0--L7 的阶段编号。它是横切 L0--L7 的审计数据包，记录 meta-model approval、schema approval、schema revision、backfill、statistical protocol、challenge、adjudication、interaction turns、人工修改、成本和脱敏状态。发布或用于 method-evaluation finding 前，必须经过 G6 process evidence boundary gate。

## 4. Dimension pattern lifecycle

Dimension pattern 是本方法的一等制品。每次 schema 变化至少记录：

| 字段 | 含义 |
|---|---|
| `schema_version` | schema 版本号。 |
| `change_trigger` | 新论文类型、抽取失败、研究者发现遗漏、survey-of-surveys pattern、审稿风险等。 |
| `proposed_change` | 新增/删除/合并/拆分字段、取值空间变化、证据要求变化。 |
| `approved_by` | 研究者批准人或裁决记录。 |
| `rationale` | 变更理由。 |
| `impacted_fields` | 受影响字段。 |
| `impacted_papers` | 需要回填或复核的论文。 |
| `backfill_required` | 是否需要回填。 |
| `backfill_status` | not-started / in-progress / completed / waived。 |
| `freeze_reason` | schema 稳定或暂时冻结理由。 |

最小规则：未经研究者批准的 schema revision 不能进入正式抽取；若 schema revision 改变已抽取字段语义，必须记录 impact analysis 和 backfill 状态。

## 5. Statistical analysis 到 finding 的转移规则

统计分析与 research finding 的关系必须满足：

```text
field-level content evidence -> evidence table -> statistical analysis -> candidate finding signal -> challenge/adjudication -> final target-domain finding
```

禁止直接执行：

```text
frequency / distribution / cross-tab -> final finding
```

Candidate finding signal 升级为 final target-domain finding 的最低条件：

1. 支持性 content evidence 可回到 source anchors；
2. counter-evidence / uncertainty 已被检查或显式标为 unresolved；
3. scope 与 claim strength 经研究者确认；
4. 若 schema 或统计协议变化会影响该 finding，必须先完成必要 backfill 或标记 limitation；
5. final 状态由研究者裁决记录确认。

## 6. Human gate contract

| Gate | 位置 | 输入 | 决策类型 | 最小记录 |
|---|---|---|---|---|
| G0 | L0 后 | topic brief、RQ、scope、meta-model | approve / revise / reject | 版本、理由、排除范围 |
| G1 | L2 后 | dimension schema 草案 | approve / revise / reject | 字段、取值、证据要求、批准记录 |
| G2 | L4 中 | schema revision proposal、impact analysis | approve / reject / defer / require backfill | 触发原因、影响论文、回填状态 |
| G3 | L5 前 | statistical analysis protocol | approve / revise | 字段版本、统计方法、限制 |
| G4 | L6/L7 | candidate finding signal 与证据链 | challenge / accept candidate / request counter-evidence | 质疑、补证、反例、主张强度变化 |
| G5 | L7 终段 | 修订后 finding 与证据链 | accept / downgrade / reject / unresolved | final 状态、理由、残余风险 |
| G6 | 横切 L0--L7，并在过程证据发布前 | process evidence 发布包 | approve / redact / restrict | consent、匿名化、脱敏、访问权限 |

## 7. Survey-of-surveys 边界

Survey-of-surveys 在本方法中只承担 scaffold mining / pattern prior 角色：

- 抽取对象：RQ 类型、taxonomy / dimension patterns、finding patterns、evidence-presentation patterns、威胁与局限写法。
- 不抽取对象：目标领域最终结论，不作为目标 SLR corpus 的证据池。
- 禁止主张：不写 PRISMA-compliant tertiary review，不写 complete coverage。
- 可用方式：与 seed-paper probing 并行作为 bootstrapping source；其 pattern 必须经研究者采纳才进入 operative schema。

## 8. Pilot 与学生 process data 边界

| 数据 | 目的 | 不能支撑 |
|---|---|---|
| Pilot run | 验证方法闭环、制品完整性、schema/backfill 可操作性、finding challenge 是否能跑通 | 跨主题泛化、方法优于人工、目标领域最终结论 |
| 硕士生 process data | 评价使用者交互成本、理解难点、审计行为、prompt/edit 过程、失败模式 | 目标领域 SLR finding 的文献证据 |

后续如收集学生数据，必须提前冻结 consent、匿名化、prompt/raw log 脱敏、教学关系隔离、数据保存和访问权限。

## 9. PR-S0-v2 不冻结的内容

1. 完整 JSON schema 细节；由 A2 冻结。
2. 最终 pilot 主题、样本和场景数量；由 A3 冻结。
3. 真实智能体实现、provider 和模型；由 A4 冻结。
4. 指标公式、阈值和统计协议；由 A5 冻结。
5. 相关工作最终写法；由 A6 深化。
6. 真实 LLM 调用；后续若调用必须 `source .env` 并保存 run record。
