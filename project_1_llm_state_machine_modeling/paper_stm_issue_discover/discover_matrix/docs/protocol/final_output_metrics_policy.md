# 方法最终输出与评判口径

本文冻结 paper1 issue discovery 方法的最终输出边界、hit、false positive、D/W/L、失败格、去重、成本和双臂比较口径。后续所有正式实验、报告、图表和方法与 X1v2 对比均以本文为唯一入口；修改本文等于修改研究协议，必须在下一轮正式运行之前完成并记录版本，运行后不得为迁就结果修改。

## 0. 优化目标与冲突优先级

方法迭代的目标严格按下列顺序降级排列；当两个改动不能同时满足全部目标时，必须优先保护序号更小的目标，并在消融中报告被牺牲的量，不能为了低优先级指标回退高优先级能力。

| 优先级 | 目标 | 最低验收含义 |
|---:|---|---|
| 1 | 全量 hit 显著高于同模型 X1v2 baseline | 在同一冻结台账、同一 paired eligible 网格和同一人工裁决协议下，方法整体 hit 高于 baseline，且配对差值的 95% 置信区间下界大于 0；全网格保守下界也必须同时报告 |
| 2 | L2 大部分被发现且显著高于 baseline | L2 hit 首先必须超过 50%，目标达到约 60% 或以上；同时在 L2 paired positions 上显著高于 baseline。D2×L2 必须单列，但不能替代完整 L2 或整体目标 |
| 3 | FP 可控且不劣于 baseline | 在同一 paired eligible 网格和同一人工裁决协议下，方法 release-emission precision 不低于 baseline，等价地 FP rate 不高于 baseline；同时报告每格 ledger-unmatched emission 与跨轮 unique-cause FP，防止只靠改变分母掩盖绝对用户负担。目标 precision 为至少 65%，但“不劣于 baseline”是最低硬门 |
| 4 | Prototype 全量生成成本不超过 baseline 的 25x | 只比较同一模型下 `prototype: STM+NL+PlantUML/FCSTM/inspect -> D1/D2 issues` 与 `X1v2: STM+NL -> issues` 的生成 API 成本。人工 judge 是实验后的对账，不属于方法图、没有 token/美元成本、也不参与成本优化。允许个别 pair 或噪点超过 25x，不设单格硬门。若 prototype 总体超过 25x，优先减轻其重复 prompt、提高 cache 命中和减少非 provider retry，不先删除已经证明提高 hit 或控制 FP 的环节 |

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

`D0` 与 `D_UNRESOLVED` 被内部截住不等于删除数据。它们必须保留原始 finding、D 理由、defeater、W/L、执行结果、usage 和 coverage-gap 诊断，用于发现方法为什么没有形成可发布主张；但它们绝不能通过 judge、聚合器或报告脚本间接贡献 hit，也绝不能扩大 FP 分母。

## 2. D、W、L 是三条独立轴

`D` 判断方法自己的缺陷主张是否站得住；台账的 `D` 是 ground truth 对台账条目的裁决。两者对象不同，台账为 `D2` 不蕴含方法 finding 必须为 `D2`，方法 finding 为 `D0` 也不能仅因其语义上碰到一条台账记录而机械升级。

| 方法 D 档 | 含义 | 发布处置 |
|---|---|---|
| `D2` | 存在明确被违反义务，最强反驳不存活 | 发布 |
| `D1` | 存在与事实相容的称职第二读法，两读并立 | 发布，并携带第二读法与不确定性 |
| `D0` | 作者可正当地称其为设计选择，或没有可陈述的被违反义务 | 内部截住 |
| `D_UNRESOLVED` | D 结构化裁决在允许的定向修复后仍未闭合 | 内部截住并登记 coverage gap |

`W` 判断证据是否真实执行并闭合，不能由 LLM 口头指定。`W2` 要求编译后的 assertion 或 formal program 在确切 FCSTM 上真实运行并得到 terminal verdict，同时保存 FCSTM hash、program/assertion hash、后端结果、semantic binding receipt 和必要的 source attribution；`W1` 表示已有可复核定位或静态证据但未形成上述完整执行闭环；`W0` 表示只有自然语言主张或执行失败后的最低兜底。D1/D2 即使只有 W1/W0 仍应发布，W1 是 W2 的兜底，W0 是 W2/W1 均无法闭合时的最后兜底；正式报告必须同时给出发布 issue 的 W 分布，并以提高 W2 占比为目标。

`L` 描述陈述该缺陷所需的推理层次，沿用台账 `L0/L1/L2` 定义。方法输出必须对每条 release issue 保存自己的 `d_level`、`witness_level`、`l_level` 与理由；不得只输出 judge 最终标签而不输出 basis。

## 3. 命中判定

一条台账记录在某个 cell 上命中，当且仅当人工标注者逐条阅读该 cell 的全部 release issue、冻结台账主张及判定所需源材料后，找到至少一条 release issue 与台账记录同时满足“同一位置”和“同一性质”。措辞不同、谓词不同、只报告更根本原因或行为后果不自动否定命中，但必须满足 [hit_criterion.md](./hit_criterion.md) 的语义同一性与禁止项；人工标注所引 supporting release ID 不在该 cell 的 `release_issues` 集合内时，该命中无效。

方法侧人工评测包只允许包含 D1/D2 `report_issue_clusters`。标注者不得读取 D0、D_UNRESOLVED、未聚类 facet 或被 release gate 截住的内容；人工标注完成后可以用 exact-ID 完整性检查确认所引 issue ID 完全属于本次输入集合，但程序不得据此产生、修改或推荐语义标签。

### 3.1 人工裁决唯一真源

正式 hit 与 FP 评测严禁由脚本、LLM judge、关键词规则、字符串匹配、相似度、embedding、分类器或任何自动匹配器完成，也不得让这些工具做候选预筛、标签建议、优先级排序、默认填充或争议裁决。每个台账记录 × cell 的 hit/miss 和每条 release issue 的 ledger-accounted/ledger-unmatched 关系都必须由人工逐条阅读后填写；“没有被自动候选器召回”不能成为 miss 或 FP 的依据。完整操作合同见 [manual_release_evaluation.md](./manual_release_evaluation.md)。

每条人工关系记录至少保存 `pair`、`cell`、`ledger_id`、`release_issue_id`、`hit_shape`、`decision`、自然语言 `reason`、所读材料清单和不确定性说明。一条 release issue 对应多条台账或一条台账由多个 release issue 支持时必须逐一显式记录，不能只留聚合勾选。争议项只能由另一轮独立人工复核或书面仲裁解决，不能交回模型或脚本。

人工标签冻结之后，hit/FP 语义判断已经结束。确定性工具至多校验 exact ID、检查每个应判单元是否齐全、对已冻结人工标签做算术并渲染表格；它们不是 judge，不得读取自由文本理由来改变任何标签，也不得从台账或 release issue 的文本、位置、identifier 或形式关系自动派生、推荐或补全 hit/FP。若无法证明某段工具只消费已经人工签署的离散标签，则它不得接触正式评测数据。

对当前单模型三轮实验：

- `hit@1` = eligible 的“台账记录 × 轮次”命中位数 / eligible 位置数。

- `hit@3` = 每条台账记录三轮中至少命中一次的条目数 / 至少有一轮 eligible 的台账条目数。

- `hit@all` = 每条台账记录的全部 eligible 轮次均命中的条目数 / 至少有一轮 eligible 的台账条目数；报告必须同时给出每条记录实际 eligible 轮次数，不能把两轮可判且两轮全中伪装成固定三轮全中。

按 `D`、`L` 或二者交叉拆分时只改变台账子集，不改变命中判据。整体、L2、D2×L2 必须同时报告，不能只选择提升最大的切片。

## 4. 失败格与 eligibility

固定实验网格中的任何格都不得静默消失。方法 provider/transport failure、在穷尽节点内定向修复后仍无法满足 structured-output contract 的 schema failure，以及人工评测包缺失、人工标注未完成或标注者发生材料泄漏可以使对应判定位不具主结果资格；其它内部超时、执行异常、证书不闭合、预算耗尽、D 修复耗尽和 gate 拒绝必须降级落盘，不得把整格排除。

正式报告必须同时给出两套覆盖读数：

1. 主读数只使用双方均有最终产物且人工标注完整有效的 paired eligible positions，并明确分子、分母、失败 pair/cell、未完成或作废的标注单元与 eligibility rate。

2. 固定全网格保守下界将所有不可判位置按 miss 处理，用于证明排除失败格没有制造表面提升。

方法与 baseline 的显著性比较只能在 paired eligible positions 上进行，并同时报告全网格保守下界。人工标注的每次修订都必须保留版本、修改人、理由和被替代值；不得用后产生的不完整或泄漏标注覆盖已有完整有效的人工裁决。

## 5. False positive 与 precision

FP 只对 release issue 判定。对一个 eligible cell 的每条 release issue，若人工标注者逐条阅读后认定它与冻结台账中的至少一条记录同处同性质，则该 issue 是 ledger-accounted emission；若人工逐条核对全部适用台账记录后仍没有任何记录承载它，则在冻结 benchmark 口径下记为 ledger-unmatched FP。未完成逐条核对不得默认记为 FP。

`precision = ledger-accounted release issue emissions / 全部 release issue emissions`。D0、D_UNRESOLVED、raw finding、重复 facet、coverage gap 和内部诊断均不得进入分子或分母。

每次正式报告必须同时给出两套 FP 计数，二者不得混成一个数：

| 口径 | 去重单元 | 用途 |
|---|---|---|
| release emission FP | 每个 cell 的最终 `report_issue_cluster` | 计算正式 precision，反映一次运行交给用户的负担 |
| unique-cause FP | `(pair, canonical cause key)`，跨轮合并 | 分析方法有多少种不同的错误主张，避免三轮重复把同一原因放大 |

冻结台账不保证是现实缺陷全集，因此 `ledger-unmatched FP` 是 benchmark 操作定义，不自动等于现实中的虚假缺陷。所有 unique-cause FP 还要独立分成“同 pair 内重复未合并”“已有裁决确认不入台账”“证据不足或两读未决”“可能是真实台账漏记”四类；该成分分析作为 validity 附表报告，但不允许事后把有利条目加入冻结台账并回算主 precision。

## 6. 去重边界

方法末端必须先完成 cell 内去重，再进入 judge。第一层使用形式制品和 source certificate 派生的 exact cause key 合并同一技术原因的 facet；第二层只消费 D LLM 显式输出的 `duplicate_of` 关系，并验证 earlier-key、正式 cause 约束与 property signature。确定性代码不得从 claim、reason、obligation 或 identifier 的字符串内容推断语义重复。

跨轮重复不在方法输出阶段合并，因为三轮是独立实验重复；它只在 unique-cause FP 和稳定性分析中合并。若同一 cell 中仍存在语义重复的 release clusters，应记为 dedup failure，并在 emission precision 中保留其真实用户负担。

## 7. Baseline 对比

方法与 X1v2 必须物理分表报告，逐条台账结果也必须分成 `ledger_method.md` 与 `ledger_baseline.md`。方法的最终端点是 D1/D2 `report_issue_clusters`；X1v2 没有 D gate，其最终端点是 `parsed_output.issues`。两臂均由同一冻结人工协议按同处同性质逐条裁决，不得让方法侧读取 baseline 结果，也不得让任一生成 prompt 读取真实台账条目或人工裁决例子。

同模型比较必须报告整体、L2、D2×L2 的 hit@1/hit@3/hit@all、release emission precision、unique-cause FP、eligible rate、失败格、W/D/L 分布和美元成本。旧历史六格 X1v2 网格与当前 Luna 三轮同模型网格必须分开，不得相减或混表。

## 8. Prototype 成本口径

成本边界只覆盖 prototype 从 STM、NL、PlantUML/FCSTM、mapping 注释与 inspect 输入生成 D1/D2 release issues 的全部 LLM 调用。成本直接读取 `.llmconfig.yml` 对应 profile 的 input、output、cache-read、cache-write 美元单价，并与同一模型的 X1v2 issue 生成调用横向比较。除明确 provider/transport failure 且随后实际发起 retry 的前序 attempt 可标为 `provider_error_retry_exempt` 外，prototype 内的 schema repair、定向 D repair、输出超限、本地异常、预算耗尽和其它返工全部计费并保留 usage。

正式 API 成本至少同时报告 prototype issue-generation 成本、X1v2 issue-generation 成本及 `prototype / X1v2` 倍率。用户约束只作用于该倍率，不得超过 `25x`，不要求每个 pair 或每次运行单独低于 `25x`。人工 judge 发生在两臂输出冻结之后，只负责准确、客观地逐条裁定 hit/FP；它不属于方法推理、不调用 provider、不记录 token、不折算美元、不进入倍率，也没有 prompt/cache/retry 优化问题。若总体超限，只优化 prototype 的重复上下文、cache 边界、schema 稳定性与非 provider retry；不得通过漏计 prototype attempt、删除 usage、压缩人工判断材料或改用跨模型价格来满足门。

## 9. 语义纪律与防泄漏

方法运行时的 NL 同义、指代、义务成立、条件作用域、source-element 对应和语义去重必须由具名 LLM 节点明确裁决；正式评测中的 finding-to-ledger 同一性只能由人工逐条裁决。确定性代码只处理 schema、精确 ID、AST、inspect、图、trace、SMT、hash、人工标签后的集合和计数等可完美判定的问题。禁止关键词、substring、正则、连接词、编辑距离、embedding 或 identifier 形状承担文本语义判断。

真实台账 ID、台账 summary/detail、真实 pair 的 judge 结论和 benchmark 特有例子不得进入方法生成 prompt。评测与诊断可以读取冻结台账，但从 benchmark 发现的新表达缺口只有在先获得独立领域来源或公认标准依据、再建立不含真实用例的合成 fixture 与回归测试之后，才允许进入方法设计。

## 10. 历史结果处置

2026-08-19 v26-dnorm 报告曾将 raw `finding_records`（含 D0）作为 judge 输入，并据此报告方法 `226/435` hit 和 `566/953` FP。该边界违反本文第 1 节，故这些数字只能作为“历史 raw-audit 口径”保留，不能作为方法最终效果、论文 headline、与 baseline 的最终比较或下一代的回归基线。

在按 D1/D2 `report_issue_clusters` 完成人工逐条重判并闭合全部 eligibility 之前，任何基于旧 judge 或自动 judge 的 D1/D2 回放数字都只能标为无效调试估计，不得标为最终结果。

2026-08-19 曾误启动 `semantic_judge.py` 对 v26 D1/D2 release issues 做自动重判；该路线随后被本协议明确禁止。其所有 pair JSON、manifest、标签和 hit/FP 数均为无效调试产物，不能进入正式 v26/v27 指标、失败率或论文结论；这次误调用也不属于 prototype issue-generation 成本，不能混入 25x 倍率。v26 严格结果必须从零开始按本节人工协议逐条裁决。
