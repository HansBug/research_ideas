# STATUS.md — 当前状态

> 本文件只记录**长期研究事实**的完成状态。⛔ PR 进度、review 状态、CI、子 PR 排期一律以 GitHub PR / issue 为准，本文件不维护。⛔ 数字不在此定义。⭐ **当前口径的唯一来源**是 [discover_matrix/ledger_v2/](./discover_matrix/ledger_v2/)：台账 145 条见 `ledger.json`，X1v2 结果见 `X1V2_RESULTS.md`。⚠️ 旧的 v46 全量报告 [../talks/2026-08-10-实验-v46全量矩阵双侧结论.md](../talks/2026-08-10-实验-v46全量矩阵双侧结论.md) **是历史记录**，其数字建立在已归档的第一版台账上，⛔ 不得作为当前数字来源引用。

⚠️ 下表中出现的「报告 §N」一律指那份 **v46 历史报告**，⛔ 只用于指路它记录的**方法性事实**（谓词词表、证据链形态、表示债务分类等，这些不随台账换代而失效）；⛔ **它里面的任何覆盖率数字都不是当前口径**。

## 1. 当前阶段

**一次完整的全量运行、同模型 X1v2 运行和 v27-stream 的 54/54 Luna 语义判定均已完成；当前工作重心转入结果归档与论文写作。**

方法实现、语料、缺陷台账、双侧 raw run、54 份 Luna judgement 与调用审计均已就位；旧 v26 judge 错把包含 D0 的 raw finding 当成最终输出，故旧 `226/435` 与 `566/953 FP` 只能作为历史 raw-audit 数字保留。当前正式结果只读取 D1/D2 final clusters，完整报告、逐条双臂分表与 54 份 Luna judgement 见 [2026-08-20-luna-full-x3-v27-stream/REPORT-luna.md](./reports/2026-08-20-luna-full-x3-v27-stream/REPORT-luna.md) 及其同名目录；v26 报告仍保留为历史对照。最终输出、hit、FP、失败格、去重和成本的唯一口径已冻结在 [final_output_metrics_policy.md](./discover_matrix/docs/protocol/final_output_metrics_policy.md)，v27 的问题总账与大迭代计划见 [preregistered.md](./discover_matrix/docs/generations/v27/preregistered.md)。

论文口径已按 2026-08-07 / 08-08 导师定调收窄为 **issue discover 单独成篇**，repair 另立后续论文。

## 2. 已完成事实

| 类别 | 状态 | 入口 |
| :-- | :-- | :-- |
| 论文口径收窄（discover 单独成篇、**三条** contribution） | 已完成 | [README.md](./README.md) §2、[story/paper_story.md](./story/paper_story.md) §7「Contributions」⚠️ 此前本行写「两条」且链接指向归档版，均已更正（2026-08-11，PR #180） |
| 建模对象边界（$M = (S, E, V, Tr, A)$，不含时钟 / 不变式 / 正交区） | 已完成，先验可判 | [story/model_scope.md](./story/model_scope.md)、[discover_matrix/docs/protocol/nl_scope_rule.md](./discover_matrix/docs/protocol/nl_scope_rule.md) |
| 方法出处口径（按领域资料归纳表述；hold-out 永久移除） | 口径已完成，工程落地未完成（见 §3） | [discover_matrix/docs/protocol/method_provenance_policy.md](./discover_matrix/docs/protocol/method_provenance_policy.md) |
| 语料（60 pair，逐 pair 溯源元数据含行列与 SHA-256） | 已完成 | [selected_seed_examples/](./selected_seed_examples/) |
| ⭐ **缺陷台账（第二版，145 条 = `D2` 98 + `D1` 47，每条逐条落定 `L0`/`L1`/`L2`）** | **已完成，零欠账** | [discover_matrix/ledger_v2/ledger.json](./discover_matrix/ledger_v2/ledger.json)；已知缺口见 [ground_truth_limitations.md](./discover_matrix/docs/protocol/ground_truth_limitations.md) |
| ⭐ **台账的完整证据链**（第一版台账 126 条 · 60 份逐 pair 复审 · 54 份工作单含全部人工裁决与逐条 meta review · 三方 D 档判读包 · 去重台账） | **已完成，且与台账放在同一目录下** | [discover_matrix/ledger_v2/provenance/](./discover_matrix/ledger_v2/provenance/)；台账每条的 `worksheet` 字段直接指向对应工作单 |
| ⛔ 第一版台账（126 条；扣 `00x8` 的 27 条后 99 条进入重标，能力分母 98 条） | **已由第二版取代**；⛔ 不再是任何分母，仅作证据链保留 | [discover_matrix/ledger_v2/provenance/expected_issue_set.json](./discover_matrix/ledger_v2/provenance/expected_issue_set.json) |
| ⭐ **X1v2 基线在第二版台账上的精确命中** | **已完成**（145 × 6 = 870 位；56 条为本轮逐格人工新判） | [discover_matrix/ledger_v2/X1V2_RESULTS.md](./discover_matrix/ledger_v2/X1V2_RESULTS.md) |
| ⭐ **Luna v27-stream 与 X1v2 同台账全量 x3 运行** | 已完成 54/54 pair 的 D1/D2-release Luna 对账；方法整体 hit@1=`276/435`、hit@3=`107/145`，L2 hit@3=`35/39`，D2×L2 hit@3=`30/34`，均高于同模型 X1v2；v26 保留为历史对照 | [reports/2026-08-20-luna-full-x3-v27-stream/REPORT-luna.md](./reports/2026-08-20-luna-full-x3-v27-stream/REPORT-luna.md)、[reports/2026-08-19-judge-model-comparison.md](./reports/2026-08-19-judge-model-comparison.md)、[final_output_metrics_policy.md](./discover_matrix/docs/protocol/final_output_metrics_policy.md) |
| 闭合谓词词表（19 个，三族） | 已冻结 | 报告 §4.3；实现在 [pipeline/feedback_loop/](./pipeline/feedback_loop/) |
| 方法实现（八阶段 + 定向反馈循环） | 已完成并跑通全量 | [pipeline/feedback_loop/](./pipeline/feedback_loop/) |
| ⛔ 主臂 v46 全量实验（$54 \times 2 \times 3 = 324$ 格） | 已完成，但**建立在第一版台账上、已整体归档**；⭐ **已裁定不在第二版台账上重测**（2026-08-17 用户裁定），故它不再是欠账，也不进当前结论 | [archive/r10_ledger_v1_and_v46/v46/](./archive/r10_ledger_v1_and_v46/v46/) |
| 命中判定（独立语义 judge） | 已完成：同一 Sol judge 同时评估 v26 与 X1v2 并覆盖 54/54 pair；judge 的 token/cache/retry/美元只做独立审计，不计入 method 成本倍率；Luna 保留为同输入对照 | [reports/2026-08-19-judge-model-comparison.md](./reports/2026-08-19-judge-model-comparison.md)、[discover_matrix/docs/protocol/final_output_metrics_policy.md](./discover_matrix/docs/protocol/final_output_metrics_policy.md) |
| 多报侧五类裁定（逐簇判据 + 逐组合并理由） | 已完成 | 报告 §7；口径 [discover_matrix/docs/protocol/unexpected_taxonomy.md](./discover_matrix/docs/protocol/unexpected_taxonomy.md) |
| 表示债务的识别、子类划分与量化 | 已完成 | 报告 §7.5；[discover_matrix/docs/findings/representation_debt.md](./discover_matrix/docs/findings/representation_debt.md) |
| 覆盖侧上界性的量化（不具判别力的谓词那条通道） | 已完成 | 报告 §6.2 |
| 证据链（逐节点记录、逐次 LLM 调用记录、内容哈希、判定与产物分离） | 已完成 | 报告 §5.2 |
| 事前登记（历代判据、达标档位、回归红旗） | 已完成并保留 | [discover_matrix/](./discover_matrix/) 历代材料索引 |
| story 文库改写为 discover 口径 | 已完成 | [story/](./story/) |

## 3. 尚未完成事实

### 3.1 ⛔ 必须补的对照与审计（审稿人会直接问，且都不需要重跑全量网格）

| 项 | 为什么必须 | 状态 |
| :-- | :-- | :-- |
| **朴素基线** | 同一 gpt-5.6-luna profile、同一 54-pair、同一三轮矩阵的 X1v2 raw 运行已完成；v27 方法与 baseline 已由同一 Luna judge 按最终发布边界完成 paired comparison | 已完成；结果见 [2026-08-20-luna-full-x3-v27-stream/REPORT-luna.md](./reports/2026-08-20-luna-full-x3-v27-stream/REPORT-luna.md)，judge sensitivity 历史对照见 [2026-08-19-judge-model-comparison.md](./reports/2026-08-19-judge-model-comparison.md)，边界见 [final_output_metrics_policy.md](./discover_matrix/docs/protocol/final_output_metrics_policy.md) |
| 循环各阶段的消融 | 八个阶段哪些是必要的，尤其两个审查阶段与静态预检；它们合计占算力大头却没有单独的收益证据 | 未做 |
| 表示债务的第二判定者 | 占比最大的一块靠人工回读作者源认定，该步不可机械复现且目前单人判定 | 未做 |
| 台账撰写过程的交代 | 台账是能力分母。必须写清谁标的、何时标的、**是否在看过方法产出之后标的**、与命中判定是否同一人 | 未做 |
| 命中形态的构成 | 四种等价形态中「蕴含更根本的原因」最宽；若相当比例靠最宽那一档，该数的性质就变了 | 未做 |
| 拒答文案的回灌量 | 同一机制在方法一节是设计优点、在结果一节是上界成因，尚未量化 | 未做 |
| 命中位按「实际由哪一族断言支撑」重算 | 当前族归属来自台账侧标注，与产出侧构成不一致；重算需要逐位判据带结构化 issue 引用，而当前判据是自由文本 | 未做，且**受阻于记录格式欠账** |
| 规则的领域出处注释补齐 | 方法出处口径的 R1 要求每条规则挂可查证外部依据；词表尚未逐条挂钩 | 部分完成 |
| 有界模型检查用量的成因查清 | 三个候选原因指向相反的行动。判别方法：人工通读需求文本找出全部响应性 / 持续性义务，再看两侧各表达了多少 | 未做。⛔ 在此之前论文不得主张该族必要，也不得据零使用把 `response_within` 退役 |

### 3.2 方法侧待改进（影响下一代次，不阻塞写作）

| 项 | 依据 |
| :-- | :-- |
| 补一条**模型驱动的巡检入口** | 合式性层显著偏低，零命中里该层占比最高。⚠️ 但零命中里另有一部分在需求驱动层，补入口解决不了，需另行定位 |
| 收断言侧的过度规定 | 去重后占比最大。⚠️ 成因至少两种（提示侧抽取倾向 / 证据包字段缺失），先拆开成因再动手 |
| 补中间表示的损失 | 三个子类看起来是可修的编译实现问题（析取触发可保留成多个事件、守卫里的量可保留成变量声明），不需要放弃可执行语义 |
| 降低方差 | 相当一部分记录处在「能找到但找不稳」 |
| 收需求集规模 | 断言转换与需求拆分两阶段合计占节点耗时大头且随需求条数线性增长，既是算力主要去向也是降级主要来源 |
| 统计回归防护面的规模 | [story/claim_evidence_map.md](./story/claim_evidence_map.md) C13 目前只能写成方法性质 |

### 3.3 写作侧

| 项 | 状态 |
| :-- | :-- |
| 章节结构与 RQ 定义 | 章节结构已完成（十节骨架，§编号已冻结），见 [story/paper_outline.md](./story/paper_outline.md)；⚠️ **RQ 定义仍未定稿**（`TODO-O3`） |
| 正文 | 未开始 |
| 投稿目标 venue | 未定，见根目录 [ccf_venues/](../../ccf_venues/) |

## 4. 当前可声称与不可声称

### 可以声称

1. 本文研究「给定需求与一份从它生成的状态机模型，自动发现不符合之处」这一任务，**不含修复**。
2. 已给出 19 谓词的闭合词表与一套需求义务到断言的转换方法，并在全量语料上跑通。
3. 一次完整全量运行（方法与 X1v2 各 162 格）及 Luna 54/54 D1/D2 final-cluster judge 已完成并保留 raw record、usage、错误、reason 与 hash；旧 raw-finding judge 只作诊断证据。
4. 覆盖率数字**只能作为上界**，且必须与算力代价一起给。
5. 未被台账认领的产出可逐条裁定成五类，其中按条目计最大的一块是评审入口的编译损失。
6. 可执行语义是必要的（两套口径），但**有界模型检查的必要性本实验无法判定**。
7. 能力缺口与稳定性缺口是两个独立问题，且体量相当。

### 不可声称

1. 不可声称本文做修复，或对修复效果有任何承诺。
2. 不可声称覆盖率的点估计或区间估计。
3. 不可把 Luna 本轮相对 X1v2 的结果外推为跨模型、跨台账或跨版本的普遍提升。
4. 不可声称台账是缺陷全集，也不可把无台账记录的 pair 读作「这些模型无缺陷」。
5. 不可声称某个执行模型更适合这项任务。
6. 不可声称多报侧的「误报率」。
7. 不可声称回归防护面的规模（未测）。
8. 不可声称谓词选型建议（须先做词表消融）。
9. 不可声称「这些模型没有并发 / 时间问题」。
10. 不可声称独立 semantic judge 没有测量误差；当前裁定保留完整输入、输出、理由和模型对照，具有可审计性，但仍是非确定性的 LLM 语义判断。

## 5. 当前最高风险

| 风险 | 后果 |
| :-- | :-- |
| **最终输出边界曾被绕过** | 旧 judge 读取 raw finding 并纳入 D0，导致 hit 与 FP 同时虚高；若任何报告继续引用旧 headline，会直接破坏方法与 baseline 的可比性 |
| **对照的外推边界** | 当前运行只覆盖 gpt-5.6-luna、54 个 eligible pair 和 v27-stream/X1v2 两臂；Sol sensitivity 重判已闭合，但仍需避免跨生成模型泛化，并补充消融 |
| **正式 headline 仍依赖单一 Luna judge** | Sol/Luna 54/54 sensitivity 对照已有 hit/FP 一致率，且 `0019` 分歧已逐项复核，但当前 v27 headline 使用 Luna judge，仍需把 judge 误差列为测量有效性威胁 |
| **台账既是分母又是自家产物**，且标注过程未交代 | 若时序上晚于方法产出，覆盖率就不是覆盖率 |
| 覆盖率被写成点估计 | 已知扣除项只给上界方向，写成点估计等于宣称一个不掌握的下界 |
| 多报侧只报一套分母 | 两套给出**相反**的主要矛盾，只报一套会把整改资源投错地方 |
| repair 口径回流 | 历史文档与仍在原地的 repair 期资产会诱导后续 agent 把 closure / regression 写回主线 |
| 把「发现了多少」当成贡献 | 贡献是断言体系；净增量只有极少数条且不稳定，当卖点会立刻被反驳 |
| 规则出处注释未补齐 | 「方法源自领域资料」目前是主张而非可核验事实，投稿前的出处审计会卡住 |

## 6. 相对上一版改了什么、为什么

| 改动 | 为什么 |
| :-- | :-- |
| 当前阶段从「方法合同已讨论、阶段 Agent 即将纵向实现」改为「全量实验已完成，转入补对照与写作」 | 旧版写于实现之前；324 格全量实验已完成 |
| 删除「Discover Agent 未实现」「Repair Agent 未实现」「Confirm Agent 未实现」「deterministic loop controller 未实现」「pilot 未完成」等全部条目 | Discover 已实现并跑通全量；Repair / Confirm 已随论文收窄移出本文范围 |
| 删除「不可声称真实 repair loop 已经运行」「不可声称 final metrics 已冻结」等 repair 期禁令 | 前者已不适用（repair 不在本文），后者已被更强的口径取代（数字已产出，问题变成怎么写） |
| §3 拆成「必须补的对照与审计」「方法侧待改进」「写作侧」三块，并把朴素基线更新为已完成、把 judge 失败与消融列为残余风险 | 旧版的未完成表全是「某个 Agent 未实现」，与当前真实缺口完全不同 |
| §4 可声称 / 不可声称全面重写，新增上界、无对照、两套分母、回归防护未测等条 | 旧版的声称清单围绕 asset map 与 issue ledger v0，已无对应 |
| §5 风险表重写，保留「旧 wording 回流」一条并改为 repair 口径回流 | 该风险机制没变，只是防的对象从 Better STM 换成 repair |
| **保留**：「不把中间表示能力写成贡献」「不把 ledger / audit 写成主贡献」 | 两条禁令与新口径一致，且仍是真实风险 |
| 删除全部 GitHub PR / issue 链接（`#100` / `#152` 等动态施工入口） | 仓库根 §9：动态流程状态只维护在 GitHub，仓库文件不做第二流程真源 |
