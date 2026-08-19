# D1/D2 最终输出人工评测协议

本文规定 paper1 的正式 hit 与 false positive 评测方式。评测发生在 prototype 与 X1v2 的全部输出冻结之后，只负责把最终 issues 与冻结台账逐条对账；它不是 `STM+NL -> issues` 方法的一部分，不调用 LLM provider，不产生 token 或美元成本，也不进入 25x 成本倍率。

## 1. 唯一判定对象

方法侧只判 `report_issue_clusters` 中 `d_level in {D1, D2}` 的 release issues；`D0`、`D_UNRESOLVED`、raw finding、accepted 中间态和 confirmed 子集均不得进入人工评测包。X1v2 侧只判每格最终 `parsed_output.issues`。两臂使用同一人工判据，但物理分表保存结果。

## 2. 严禁自动语义判定

每个 hit/miss、ledger-accounted/ledger-unmatched、duplicate、grounded-extra、boundary 和 fabricated 判断都必须由标注者逐条阅读完整材料后作出。禁止运行脚本或 LLM judge 来匹配台账与 issue；禁止关键词、正则、substring、编辑距离、embedding、分类器、字符串规则或形式元素重叠自动给标签；也禁止自动工具做候选预筛、推荐、排序、默认填充或争议仲裁。

文件查看、exact-ID 完整性检查和人工标签冻结后的纯算术不是语义判定，但任何工具都不得从 issue/台账的文本、identifier、位置或形式关系中产生或改变标签。正式结果的语义真源只能是人工标注记录。

## 3. 人工阅读材料

每个 cell 必须读取：该 pair 的冻结台账完整条目、该 cell 的全部最终 issues、NL 原文、PlantUML STM、带语义映射注释的 FCSTM STM code、inspect 结果，以及 issue 自带的 claim、location、obligation、D/W/L、source attribution 与执行证据。不得只看标题、状态名重叠或摘要；若材料不足以裁决，标为 `unresolved` 并写明缺什么，不能自动按 miss 或 FP 处理。

为降低臂别偏倚，正式 packet 使用中性 cell alias，标注阶段不展示 method/baseline 身份、成本、历史命中率、代次目标、D0 缺口清单或此前裁决。标注完成并冻结后才恢复 arm/run 映射。任何标注者若读到被禁止的历史答案或臂别信息，该批标注作废并重新人工判定。

## 4. Hit 判据

每个“台账条目 × cell”必须独立判定。只有至少一条该 cell 的最终 issue 与台账同时满足“同一位置”和“同一性质”，且符合只含合成例子的 [hit_criterion_for_judges.md](../judges/hit_criterion_for_judges.md) 中直接、合取项、正向对偶或更根本原因形态，才记为 hit。元素重叠、更弱命题、反向蕴含、把多条不完整 issue 拼接后才成立或只报告相邻后果均不构成 hit。含真实历史实例的维护版 `hit_criterion.md` 不得进入盲化 packet 或标注者白名单。

每个 hit 必须写出 supporting release issue ID、命中形态和一条完整的语义蕴含理由；每个 miss 必须说明是无相关 issue、位置不同、性质不同、方向相反、命题更弱还是证据不足。禁止只保存绿色勾或布尔值。

## 5. FP 判据

每条最终 issue 都必须独立判定。若它至少人工命中一条冻结台账记录，则是 `ledger-accounted`；只有逐条核对后确认没有任何台账条目承载同处同性质主张，才是 benchmark 口径的 `ledger-unmatched`。未完成核对、只因自动候选为空或只因措辞不同，均不得记为 FP。

`ledger-unmatched` 不自动等于现实中的虚假问题。它还必须人工分类为：同 cell 重复未合并、已有裁决确认不入台账、证据不足或两读未决、可能是真实台账漏记、paper1 scope boundary。该成分分析不修改冻结台账，也不事后回算主 precision。

## 6. 每条人工记录的最低字段

| 字段 | 要求 |
|---|---|
| `pair`、`cell_alias` | 精确定位人工判定单元 |
| `ledger_id` | hit/miss 所针对的冻结台账条目；issue 侧判断无对应时为 `null` |
| `release_issue_id` | supporting 或被判 issue 的最终 ID；不得引用 D0/raw finding |
| `decision` | `hit`、`miss`、`ledger-accounted`、`ledger-unmatched` 或 `unresolved` |
| `hit_shape` | 仅 hit 填 `direct/conjunct/dual/implies` |
| `reason` | 人工自然语言理由，必须说明同处同性质或不成立的具体环节 |
| `materials_read` | 实际读取的 NL、PlantUML、FCSTM、inspect、ledger 与 record 路径 |
| `uncertainty` | 最强相反读法及其处置；无则写 `none` |
| `annotator`、`decided_at` | 标注者与时间 |

## 7. 完整性与仲裁

每个 eligible cell 的全部台账条目和全部最终 issues 都必须有人工记录。一个 issue 命中多条台账或一条台账由多个 issues 支持时逐一列出关系，不能压成无依据的聚合计数。争议项由第二次独立人工阅读复核；仍不一致时保留双方理由并书面仲裁。任何自动模型或脚本均不得参与仲裁。

## 8. 与成本的边界

25x 只计算同模型下 `prototype issue-generation / X1v2 issue-generation` 的 input、output、cache-read、cache-write 美元成本。人工评测不纳入该公式，不记录 token，不折算 API 美元，也不为降低成本而删减材料、缩短理由、合并判断或减少复核。评测环节唯一优化目标是准确、客观、完整和可审计。
