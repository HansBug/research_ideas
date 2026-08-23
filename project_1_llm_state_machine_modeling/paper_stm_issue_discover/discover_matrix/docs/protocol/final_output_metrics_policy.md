# 方法最终输出与评判口径

> **迁移边界（2026-08-21）**：本文冻结的是迁移前 `feedback_loop`/旧单体实现及 v26/v27
> 历史运行的最终输出和成本审计口径。文中的 `prototype`、旧谓词和旧成本字段均是历史
> 名称，不能解释为当前正式方法。当前方法契约唯一以 [`pipeline/evidence_discovery/`](../../../pipeline/evidence_discovery/)
> 的 `four-family-19-core.v1`、W1/W2/W0 规则和重构计划为准；新代码迁移完成前，本文数字
> 不构成新四族实现的实测结果。

本文冻结 issue discovery 方法的最终输出边界、D/W/L、失败格、去重和成本。现行 hit、
Supported Rate、Semantic FP/Precision、novel、ledger-unmatched 与统一 Judge 输入规则唯一
引用 [issue #195 同步入口](./semantic_judge_protocol.md)；本文不得建立第二套语义定义。

## 0. 优化目标与冲突优先级

方法迭代的目标严格按下列顺序降级排列；当两个改动不能同时满足全部目标时，必须优先保护序号更小的目标，并在消融中报告被牺牲的量，不能为了低优先级指标回退高优先级能力。

| 优先级 | 目标 | 最低验收含义 |
|---:|---|---|
| 1 | 全量 hit 显著高于同模型 X1v2 baseline | 在同一冻结台账、同一 paired eligible 网格和同一独立 judge 下，方法整体 hit 高于 baseline，且配对差值的 95% 置信区间下界大于 0；全网格保守下界也必须同时报告 |
| 2 | L2 大部分被发现且显著高于 baseline | L2 hit 首先必须超过 50%，目标达到约 60% 或以上；同时在 L2 paired positions 上显著高于 baseline。D2×L2 必须单列，但不能替代完整 L2 或整体目标 |
| 3 | Semantic FP 可控且不劣于 baseline | 在同一 paired eligible 网格和同一冻结 Judge 下，方法 raw-report Semantic Precision 不低于 baseline；只有 `INVALID` 是 Semantic FP，同时独立报告 ledger-unmatched、cluster precision 与 redundancy。目标 precision 为至少 65%，但“不劣于 baseline”是最低硬门 |
| 4 | 历史实现生成成本不超过 baseline 的 25x | 使用同模型价格，只按历史 `issue-generation / X1v2 issue-generation` 计算；独立 semantic judge 不属于方法图，单独审计但不进入分子或倍率。允许个别 pair 或噪点超过 25x，不设单格硬门。若总体超过 25x，优先减轻历史实现的重复 prompt、提高 cache 命中和减少非 provider retry，不先删除已经证明提高 hit 或控制 FP 的环节 |

上述次序也定义停止条件：只有 1 与 2 均满足后，才允许以不损失其显著性的方式继续压 FP；只有 1、2、3 均满足后，才进一步追求低于 25x 上限的成本优化。25x 仍是完整正式实验的硬上限，不是可以用“质量优先”无限突破的软建议。

## 1. 唯一最终输出边界

方法内部可以产生 raw candidate、finding facet、执行证书、D 裁决、coverage gap 和 report cluster，但只有下面定义的 release issue 才是方法末端产物：

```text
release_issues(cell) = {
  issue in record.report_issue_clusters
  where issue.d_level in {D2, D1}
}
```

`finding_records` 是内部审计面，不是最终输出；`accepted_issues` 和 `confirmed_issues` 是过程状态或证据强度子集，也不是独立统计分母；`report_issue_clusters` 是完成语义去重后的报告面；其中仅 `D2` 与 `D1` cluster 进入 release issue。

| 对象 | 是否对外发布 | 是否进入 hit | 是否进入 FP/precision | 是否保留审计 |
|---|---:|---:|---:|---:|
| raw candidate / finding facet | 否 | 否 | 否 | 是 |
| `D0` finding / cluster | 否 | 否 | 否 | 是 |
| `D_UNRESOLVED` finding / cluster | 否 | 否 | 否 | 是 |
| `D1` report issue cluster | 是 | 是 | 是 | 是 |
| `D2` report issue cluster | 是 | 是 | 是 | 是 |

`D0` 与 `D_UNRESOLVED` 被内部截住不等于删除数据。它们必须保留原始 finding、D 理由、defeater、W、台账侧 L（如评测关联存在）、执行结果、usage 和 coverage-gap 诊断，用于发现方法为什么没有形成可发布主张；但它们绝不能通过 judge、聚合器或报告脚本间接贡献 hit，也绝不能扩大 FP 分母。若 D 语义契约在一次有界定向修复后仍不成立，方法必须写入一个 `d_fallback=true` 的结构化 D0 决策，在 `d_validation_errors` 与 `d_fallback_reason` 中保留失败原因；只有 provider/schema 整格失败等无法形成任何 D 决策的逃生路径才使用 `D_UNRESOLVED`。

## 2. D、W、L 是三条独立轴

`D` 判断方法自己的缺陷主张是否站得住；台账的 `D` 是 ground truth 对台账条目的裁决。两者对象不同，台账为 `D2` 不蕴含方法 finding 必须为 `D2`，方法 finding 为 `D0` 也不能仅因其语义上碰到一条台账记录而机械升级。

| 方法 D 档 | 含义 | 发布处置 |
|---|---|---|
| `D2` | 存在明确被违反义务，最强反驳不存活 | 发布 |
| `D1` | 存在与事实相容的称职第二读法，两读并立 | 发布，并携带第二读法与不确定性 |
| `D0` | 作者可正当地称其为设计选择，或没有可陈述的被违反义务 | 内部截住 |
| `D_UNRESOLVED` | D 结构化裁决在允许的定向修复后仍未闭合 | 内部截住并登记 coverage gap |

`W` 判断证据是否真实执行并闭合，不能由 LLM 口头指定。`W2` 要求编译后的 assertion 或 formal program 在确切 FCSTM 上真实运行并得到 terminal verdict，同时保存 FCSTM hash、program/assertion hash、后端结果、semantic binding receipt 和必要的 source attribution；`W1` 表示需求义务与模型元素已经精确绑定、可以复核定位，但没有适用的 sound 谓词或后端。W0/W1/W2 均不进入独立 Judge 的 validity 或 match gate；具体、artifact-compatible 的 W1/free-text 发布报告可以 `FULL_MATCH`。正式报告必须给出 W0/W1/W2 与 method diagnostic 分布，但不能据此机械决定 hit 或 FP。

`L` 描述陈述该缺陷所需的推理层次，沿用台账 `L0/L1/L2` 定义。`L` 是台账侧属性，
方法不得生成、裁定或在 release issue 中声称自己的 `l_level`；评测时仅读取冻结台账
的 L 字段并按台账分母切片。方法必须对每条 release issue 保存自己的 `d_level`、
`witness_level`、非空 `reason`/`basis` 与来源依据，不得只输出 judge 最终标签而不解释
如何得到该结果。

## 3. 命中判定

一条台账记录在某个 cell 上命中，当且仅当至少存在一条最终分类为 `VALID_KNOWN` 的
release report，且它与该 expected 的 relation 为 `FULL_MATCH`。FULL 采用 issue #195 的
适度宽语义，不要求 locus/property/scope/direction 或 taxonomy 逐字段复刻；同一根因的
直接可归因症状、独立可行动 facet，以及能消除或实质缓解 expected 核心违反的修复重叠
均可 FULL。真实但不足以唯一归因的关系为 `PARTIAL_MATCH`，只贡献 Supported Rate。

方法侧 Judge 输入只允许读取 D1/D2 `report_issue_clusters` 的最终发布语义内容。D/W/L、
谓词族、内部 dossier 和历史结果不得进入 `UnifiedJudgeInput`。X1v2 与方法报告均通过
同一 arm-neutral adapter contract、公共 artifact closure、prompt/schema/model/retry/
arbitration/metrics 入口；聚合器机械验证全部 report 与 expected ID closure。

对当前单模型三轮实验：

- `hit@1` = eligible 的“台账记录 × 轮次”命中位数 / eligible 位置数。

- `hit@3` = 每条台账记录三轮中至少命中一次的条目数 / 至少有一轮 eligible 的台账条目数。

- `hit@all` = 每条台账记录的全部 eligible 轮次均命中的条目数 / 至少有一轮 eligible 的台账条目数；报告必须同时给出每条记录实际 eligible 轮次数，不能把两轮可判且两轮全中伪装成固定三轮全中。

按 `D`、`L` 或二者交叉拆分时只改变台账子集，不改变命中判据。整体、L2、D2×L2 必须同时报告，不能只选择提升最大的切片。

### 3.1 冻结 Judge 与迭代复用

本阶段统一使用 `gpt-5.6-luna`。Judge cost 不参与优化，不能裁剪 prompt、artifact、双读、
reason/basis 或仲裁来降本。protocol snapshot、prompt、Pydantic schema、artifact builder、
model profile、validator、retry、仲裁或 metrics 中任何影响语义的改动都必须升 Judge 版本，
并使旧分数失去直接可比资格。版本冻结后 baseline 可复用；新 method 输出必须使用同一
冻结版本评测。论文 headline 只能来自同一 snapshot 和同一冻结 Judge 下双方完整重判。

## 4. 失败格与 eligibility

固定实验网格中的任何格都不得静默消失。方法 provider/transport failure、在穷尽节点内定向修复后仍无法满足 structured-output contract 的 schema failure 可以使对应方法格不具主结果资格；其它内部超时、执行异常、证书不闭合、预算耗尽、D 修复耗尽和 gate 拒绝必须降级落盘，不得把整格排除。独立 Judge 不允许留下未裁判位置：provider/transport failure 必须原地重发；pair-wide structured output 经定向反馈仍无法闭合时，必须转入逐 report/逐 relation 的原子 Judge，直到核心真值与 FULL/PARTIAL/NO closure 全部终态。不得把 Judge failure 伪装成 miss、FP、保守下界或排除格。

方法、feedback CLI 与 semantic judge 的默认 transport retry 上限统一为 8，并允许正式运行通过 CLI 显式覆盖。每个 attempt、错误类型、等待和最终状态都必须进入 run record；只有明确 provider/transport failure 且随后确实发起下一次同请求重发的前序 attempt 才适用计费豁免。提高 retry 上限只用于吸收上游波动，不得使 schema validation、内容返工、D repair 或本地执行错误获得 provider 豁免，也不得以冷启动整格重跑替代原地 retry。

正式报告必须同时给出两套覆盖读数：

1. 主读数使用双方均有最终产物且 judge 已完成真实语义裁定的 paired eligible positions，并明确分子、分母、方法失败 pair/cell 与 eligibility rate；judge 自身必须覆盖全部待评位置。

2. 固定全网格保守下界将所有不可判位置按 miss 处理，用于证明排除失败格没有制造表面提升。

方法与 baseline 的显著性比较只能在 paired eligible positions 上进行，并同时报告全网格保守下界。不得将后产生的失败 judge 文件覆盖同一 pair 已存在且通过完整 shape contract 的成功 judge 文件；选择规则是“最新成功结果优先，失败 receipt 只用于审计和继续原地恢复，不能进入最终指标”。

## 5. Semantic FP、precision 与 unmatched

Semantic FP 只对 D2/D1 最终发布报告判定，且只有 `INVALID` 进入 Semantic FP。
`VALID_NOVEL` 是经公共制品审计成立、但对全部 expected 均为 NO 的真实台账外问题；
它不贡献 hit，也不算 FP。`VALID_KNOWN` 至少有一个 FULL/PARTIAL；是否 hit 只由 FULL 决定。

```text
raw-report Semantic Precision
= (VALID_KNOWN + VALID_NOVEL) / 全部已裁定发布报告

Ledger-Unmatched
= 只有 PARTIAL 的 VALID_KNOWN + VALID_NOVEL + INVALID
```

每次正式报告必须分开给出：raw K/N/I、Semantic FP、raw-report Semantic Precision、
valid novel、Ledger-Unmatched、root-cause-cluster precision 和 redundancy rate。不同 report
若属于同一 actionable root cause，重复只进入 redundancy；不得把重复 valid finding 算 FP。
D0、D_UNRESOLVED、raw finding、coverage gap 和内部诊断不进入这些发布报告分母。

## 6. 去重边界

方法末端必须先完成 cell 内去重，再进入 judge。第一层使用形式制品和 source certificate 派生的 exact cause key 合并同一技术原因的 facet；第二层只消费 D LLM 显式输出的 `duplicate_of` 关系，并验证 earlier-key、正式 cause 约束与 property signature。确定性代码不得从 claim、reason、obligation 或 identifier 的字符串内容推断语义重复。

跨轮重复不在方法输出阶段合并，因为三轮是独立实验重复；它只在 unique-cause FP 和稳定性分析中合并。若同一 cell 中仍存在语义重复的 release clusters，应记为 dedup failure，并在 emission precision 中保留其真实用户负担。

## 7. Baseline 对比

方法与 X1v2 必须物理分表报告，逐条台账结果也必须分成 `ledger_method.md` 与 `ledger_baseline.md`。方法的最终端点是 D1/D2 `report_issue_clusters`；X1v2 没有 D gate，其最终端点是 `parsed_output.issues`。两臂适配后必须进入同一 `UnifiedJudgeInput`、公共 artifact closure、prompt/schema/model/retry/仲裁/metrics 路径；不得让方法侧读取 baseline 结果，也不得让任一生成 prompt 读取真实台账条目或 Judge 例子。

同模型比较必须报告整体、L2、D2×L2 的 hit@1/hit@3/hit@all、Supported Rate、K/N/I、Semantic FP、raw-report 与 root-cause-cluster precision、valid novel、Ledger-Unmatched、redundancy、eligible rate、失败格、W/D/L 分布和美元成本。不同 Judge protocol/version 的历史网格必须分开，不得相减或混表。

## 8. 成本口径

成本直接读取 `.llmconfig.yml` 对应 profile 的 input、output、cache-read、cache-write 美元单价，同一模型内横向比较。除明确 provider/transport failure 且随后实际发起 retry 的前序 attempt 可标为 `provider_error_retry_exempt` 外，schema repair、定向 D repair、输出超限、本地异常、预算耗尽和其它返工全部计费并保留 usage。

正式成本至少同时报告：历史 issue-generation 成本、X1v2 issue-generation 成本、历史实现相对 X1v2 的倍率，以及独立 judge 的 usage/cost 审计。用户的 `25x` 约束在本文中只适用于历史运行，不能直接迁移为新 `evidence_discovery` 实现的成本结论；新实现必须另建带版本和运行记录的成本字段。不得把 judge 的 input、output、cache-read、cache-write、retry 或美元成本并入历史方法分子；judge 的独立审计也不得被遗漏或伪装成 method cost。不要求每个 pair 或每次运行单独低于 `25x`。若历史总体超限，先做历史实现的 prompt 去重/压缩、稳定 schema 以减少非 provider retry，并最大化稳定前缀的 cache 利用；不得通过漏计 retry、删除 usage 或改用跨模型价格来满足门。

## 9. 语义纪律与防泄漏

NL 同义、指代、义务成立、条件作用域、source-element 对应、finding-to-ledger 同一性和语义去重必须由 LLM 明确裁决；确定性代码只处理 schema、精确 ID、自有 AST/源位置算法、图、trace、SMT、hash、集合和计数等可完美判定的问题。后端禁止调用 Python `inspect` 或旧 `inspect_*` 后端；需要类似能力时必须使用仓库内有版本、输入输出明确且经过测试的独立算法。禁止关键词、substring、正则、连接词、编辑距离、embedding 或 identifier 形状承担文本语义判断。

真实台账 ID、台账 summary/detail、真实 pair 的 judge 结论和 benchmark 特有例子不得进入方法生成 prompt。评测与诊断可以读取冻结台账，但从 benchmark 发现的新表达缺口只有在先获得独立领域来源或公认标准依据、再建立不含真实用例的合成 fixture 与回归测试之后，才允许进入方法设计。

## 10. 历史结果处置

2026-08-19 v26-dnorm 报告曾将 raw `finding_records`（含 D0）作为 judge 输入，并据此报告方法 `226/435` hit 和 `566/953` FP。该边界违反本文第 1 节，故这些数字只能作为“历史 raw-audit 口径”保留，不能作为方法最终效果、论文 headline、与 baseline 的最终比较或下一代的回归基线。

新 judge 已于 2026-08-19 按 D1/D2 `report_issue_clusters` 完成 Sol 54/54 正式重跑；当前唯一正式结果见 [2026-08-19-luna-full-x3-v26.md](../../../reports/2026-08-19-luna-full-x3-v26.md) 及其同名目录。此前基于旧 judge 的 D1/D2 回放数字继续只作为预重算或诊断估计保留，不得标为最终结果。
