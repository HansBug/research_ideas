# A1 前置检查信息消融：完整结果、v61 对照与原因审计

> 冻结时间：2026-09-06 19:49:18 +08:00。正文引用键对应文末 A.1-A.4。机器事实源为本次归档；本报告不修改 method、judge 标签或冻结 v61。

## Material Passport

Origin Skill: experiment-agent；Origin Mode: validate；Origin Date: 2026-09-06；Verification Status: ANALYZED；Version Label: a1_no_inspect_v61_v1。全量自动裁定和 agent 离线审计已完成；新结果人工确认数为 **0**。离线算术可复算，不等于已独立重做随机 API 实验或语义裁定。[src-results][src-arithmetic]

## 1. 结果回答了什么

**实测符合“A1 hit 大幅下降，尤其 L2”的研究预期。** 相比冻结 v61，A1 总 hit@1 下降 20.69 个百分点，L2 hit@1 下降 40.17 个百分点，L2 三轮均命中率下降 46.15 个百分点。下降不只是剩余 provider 失败造成的漏裁：162 格、814 份报告已全部核销；在多个案例中，检查派生候选本身已消失。但本次是用户指定的历史对比，保留词表版本、provider/时间和恢复历史差异，不能把全部差值解释成严格单因素因果效应。[clm-main][clm-mechanism][clm-limits]

**precision 不给出同样明确的方向性结论。** 主口径从 84.05% 到 80.34%，但九簇配对区间跨零；D1/D2-only 严格口径反而从 75.08% 到 77.40%。这与“A1 precision 原先未知”一致，不支持把 A1 写成精度暴跌，也不证明精度等价。L1 的平均命中略升，亦如实保留。[clm-precision][clm-tiers]

A1 关闭前置检查事实及其派生生产/消费链，保留 FCSTM、源码追踪、普通契约和语义发现、12 条谓词与真实执行回执。它不是整个 C1 消融、纯 LLM baseline 或谓词 subset 消融。原登记中的匹配 full 计划和较弱假设没有倒改；§7 追加记录用户对主线及预期的澄清。本报告不使用额外 full，也不要求新 full 才能交付。[src-contract][src-registration]

## 2. 完整性、来源与运行边界

| 核销项 | 最终事实 |
| --- | --- |
| 固定样本 | 54 pair、9 个 NL 簇、每簇 6 个制品，三轮共 162 格 |
| 台账分母 | 唯一 ledger 的 145 条；L0/L1/L2 为 71/35/39；expected-round 为 435 |
| A1 method | 162/162 eligible，814 reports；160 completed、2 completed_with_diagnostics |
| A1 judge | 162 个唯一格、814/814 reports；未裁定报告 0，未完成 judge 格 0 |
| frozen v61 | 162 格、903 reports；原始及派生结果不重跑、不改写 |
| 输入对拍 | 162 格 method input hash 字典相同；2,106 份 judge 完整 evidence document 与 expected 投影逐项相同；324 份 serialized-input 回执对上原始输入 |
| 独立判定协议 | 162 格协议及 prompt hash 与 v61 相同；外层 closure basis/hash 在 162 格不同，如实保留 |
| method 信息隔离 | 162 格、816 trace/header、917 次已记录渲染请求、1,733 处上下文，包括 8 个 D 纠错 header，检查受限视图 |

以上是逐格/逐报告核销，不以总数相同替代 ID 集合相等，不把 method 完成、子批 success 或仲裁未结束当作 judged。[clm-coverage][clm-inputs]

正式 method 的冻结来源相对于本地 `runs/paper1/a1_no_inspect_20260906/`：[src-sources]

| 来源段 | 采用格数 | 方法源码 |
| --- | ---: | --- |
| `recovery_method/f195753fa9a642ec897162adc04d4539` | 111 | `9c7c99504` |
| `transport_recovery/0ee98d4d7abe48188ffb0dcabaa8fe65` | 8 | `d2e6843e6` |
| `transport_recovery/2ec6e2045f5d414080508df7272a3da7` | 43 | `7fb300640` |

这 8 个正式恢复格不等于另一次 provider-evaluation 的 8 个诊断样本；后者没有导入。冻结选择后，method 不再生成或替换。[src-sources][src-registration]

最终 judge 来源：[src-sources]

| Run ID | 完整格数 | 源码 | Profile |
| --- | ---: | --- | --- |
| `a1-0ee98d4d-reuse-r1` | 18 | `d2e6843e6` | `gpt-5.6-luna`，旧站点 |
| `a1-aizzz-probe-0047-r1` | 1 | `7fb300640` | `aizzz-luna-eval` |
| `a1-aizzz-main-r1b` | 34 | `7fb300640` | 同上 |
| `a1-aizzz-main-r2` | 53 | `546e7055d` | 同上 |
| `a1-aizzz-main-r3` | 54 | `cff08a09a` | 同上 |
| `a1-aizzz-fill-r1-0059` | 1 | `bbf1dd36f` | 同上 |
| `a1-aizzz-fill-r2-0032` | 1 | `bbf1dd36f` | 同上 |

新站点为 `https://api.aizzz.xyz/v1`，仍只使用 `gpt-5.6-luna`；最终旧/新站点分别 18/144 格，独立保存 endpoint/config fingerprint、source/run 身份。`0047/r1` 的历史 run 名虽含 probe，实际裁定的是冻结正式 method。后续主批是原生 CLI、总 workers=16、三轮串行，没有三轮各开 16，也没有在线恢复包装。共享配置未修改。[src-registration][src-sources]

`0059/r1` 曾在 provider 调用前被旧 adapter 拒绝；`0032/r2` 的原生主批只有超时失败、没有成功裁定，原始两路 validity 共 36 次 APITimeout 尝试均封存。两格随后仅补未完成 judge，独立 run，不重抽完成标签；`0032/r2` 的新旧序列化输入字节相同。新站点也出现 timeout、stream_read_error 与原生拆批恢复，不能写“零重试”或“零故障”。[src-cases][src-sources]

## 3. 主指标与分层

FULL `hit@1` 为三轮 expected-round 命中 /435，不是首轮或第一条报告；`hit@3` 为至少一轮命中 /145，`hit@all` 为三轮都命中 /145。precision 为 `(K+N)/(K+N+I)`，全体发布报告都进入分母；N 不是独立新缺陷数。[src-registration][clm-main]

| 指标 | v61 | A1 | A1 - v61 |
| --- | ---: | ---: | ---: |
| hit@1 | 323/435 = 74.25% | 233/435 = 53.56% | -20.69 pp |
| hit@3 | 130/145 = 89.66% | 91/145 = 62.76% | -26.90 pp |
| hit@all | 82/145 = 56.55% | 65/145 = 44.83% | -11.72 pp |
| report precision | 759/903 = 84.05% | 654/814 = 80.34% | -3.71 pp |
| K | 561 | 392 | -169 |
| N | 198 | 262 | +64 |
| I | 144 | 160 | +16 |
| 全部报告 | 903 | 814 | -89 |

分层完整结果：[clm-tiers]

| 层级 | hit@1：v61 → A1 | hit@3：v61 → A1 | hit@all：v61 → A1 |
| --- | --- | --- | --- |
| L0 | 153/213 → 107/213；71.83% → 50.23% | 64/71 → 39/71；90.14% → 54.93% | 36/71 → 33/71；50.70% → 46.48% |
| L1 | 73/105 → 76/105；69.52% → 72.38% | 30/35 → 29/35；85.71% → 82.86% | 18/35 → 22/35；51.43% → 62.86% |
| L2 | 97/117 → 50/117；82.91% → 42.74% | 36/39 → 23/39；92.31% → 58.97% | 28/39 → 10/39；71.79% → 25.64% |

| 轮次 | 总命中：v61 → A1（/145） | L0（/71） | L1（/35） | L2（/39） |
| --- | ---: | ---: | ---: | ---: |
| r1 | 113 → 77 | 54 → 37 | 26 → 24 | 33 → 16 |
| r2 | 98 → 84 | 47 → 36 | 21 → 28 | 30 → 20 |
| r3 | 112 → 72 | 52 → 34 | 26 → 24 | 34 → 14 |

L2 不只单次覆盖下降：三轮稳定命中的台账条目由 28 条变为 10 条。L0 也有明显损失；L1 的小幅平均增长不能扩大为“所有层都改善/恶化”。报告数只下降约一成，而命中损失更大，说明问题不只是少输出了若干报告，输出的性质组成也变了。[clm-tiers][clm-mechanism]

## 4. 变化在哪里

### 4.1 候选、执行与报告组成

以下均为来源记录直接计数；candidate、finding evidence 与最终 report 是不同层级，不能互换为“真实缺陷数”。[clm-mechanism]

| 数量 | v61 | A1 |
| --- | ---: | ---: |
| 全部候选 | 2,436 | 1,953 |
| finding evidence | 1,863 | 1,578 |
| 谓词 true 后不作为 finding 的候选 | 573 | 375 |
| domain-invariant 候选 | 59 | 0 |
| deadlock 候选 / 发布报告 | 99 / 69 | 1 / 0 |
| reachability 候选 / 发布报告 | 125 / 61 | 38 / 27 |
| trigger_set 发布报告 | 125 | 57 |
| guard 发布报告 | 100 | 183 |
| state_action 发布报告 | 75 | 114 |
| 根报告 W0 / W1 / W2 | 0 / 636 / 267 | 0 / 645 / 169 |

A1 仍有 324 条 completed-false、375 条 completed-true、1,253 条 unsupported 和 1 条 backend error 回执；没有把 unsupported/error 伪造为 false。保留谓词不意味着必然能生成并绑定足够好的候选：没有前置事实支持时，一些行为问题在到达谓词前已经缺席。相反，普通语义路径仍会提出更多 guard/action 主张，未必命中既有台账。[src-local-audit][clm-mechanism]

例如 guard 的 K/N/I 从 29/56/15 变为 39/97/47，增加了有效报告也增加了误报；state_action 从 40/30/5 变为 42/63/9。W1 有效报告为 538 → 522，W2 为 221 → 132。这是输出组成变化，不是“A1 只是在原报告集合上均匀删减”。W2 不直接等于 L2，也不把其数量下降当成独立精度结论。[src-results][clm-precision]

### 4.2 全部命中变化核销

两臂共同命中 196 个 expected-round；v61 独有 127 个，A1 独有 37 个，合计 164 条变化，净损失 90。分层如下。[src-changes]

| 层级 | 丢失 | 新增 | 净变化 |
| --- | ---: | ---: | ---: |
| L0 | 63 | 17 | -46 |
| L1 | 9 | 12 | +3 |
| L2 | 55 | 8 | -47 |
| 合计 | 127 | 37 | -90 |

逐项沿获胜侧支持报告的根性质，在另一侧查候选、finding、发布和 FULL 关系；164 条都保留原报告 ID、候选 ID、来源及定位。该定位是**根性质层面的机械核销，不是语义唯一归因**：一条报告可支持多个台账，其他性质或 folded subclaim 也能覆盖同一问题。[clm-localization]

| 另一侧的定位 | 丢失单元中的 A1 | 新增单元中的 v61 |
| --- | ---: | ---: |
| 无支持根性质的候选 | 72 | 5 |
| 有候选，无该性质 finding | 2 | 2 |
| 有 finding，无该性质发布报告 | 8 | 9 |
| 有该性质报告，但未 FULL 命中 | 45 | 21 |

55 条 L2 丢失中，46 条落在“无该根性质候选”、1 条在“finding 未发布”、8 条在“已有该性质报告但未 FULL 命中”。因此候选发现阶段存在明确缺口；不能将 55 条全部归咎于 judge，也不能把 46/55 当作可识别的 inspect 因果贡献率。[clm-localization]

### 4.3 机制案例与不能忽略的反例

| 案例 | 核验事实 | 能支持的解释 |
| --- | --- | --- |
| `0001` 三轮 | v61 对 ClampingState、ClampingLoseState 两项 L2 死端均 FULL 命中；A1 六个 expected-round 均未命中，且无 deadlock 报告 | 前置死端候选入口消失有直接证据；旧 V4 仍保留为当前 V1，不是因为删除了死锁谓词 |
| `0046/r3` | A1 唯一 deadlock 候选是一般进展义务，绑定未闭合、无 enabled frontier，unsupported/unknown，未发布 | “谓词存在”不能替代可执行候选；不是后端执行得出无缺陷 |
| `0016/r2` | Search 共享状态报告的 claim/expected/observed 逐字相同，v61 I，A1 D2/K；evidence/source_refs 不同 | 此项 gained hit 不来自新生成的核心主张；存在语义裁定分歧，但不能证明纯随机或 endpoint 因果 |
| `0039/r2` | 两臂 initial-entry 报告都带 FinishState 终止 folded subclaim；v61 对两项行为台账为 PARTIAL，A1 为 FULL，且 A1 主报告 D0 | 不能只凭报告标题认定关系越界；新增命中包含关系覆盖口径的实际裁定差异，并非新发现该行为 |
| `0034/r1` | `issue:27/R0016` 的关系复读/仲裁声称报告列出 InMotion→Cruising/Approaching，实际列举没有这两条；仲裁 basis 与理由相矛盾 | 这是具体 judge 证据引用风险；原决定保留。同一台账还有 issue:0/26 的 FULL 支持，该可疑关联不是命中的唯一支撑 |

以上逐项记录来源锚点；不是按审计观点重裁。全量精确文本核对共有 121 组 claim/expected/observed 相同匹配，只有 3 组除匿名 ID 外全部 CandidateReport 字段相同；20 组 K/N/I 标签不同，其中 16 组有效/无效翻转。16 组均还存在其他报告字段差异，批上下文、provider、时间亦未固定，不能把它们直接估计为“随机 judge 噪声率”。[src-cases][clm-judge-risk]

## 5. 精度与稳健性

严格口径只把有效 D1/D2 报告计入有效分子和命中支持，发布报告分母不变。主口径仍按原冻结协议，不能用严格口径替换它。[clm-precision]

| 严格指标 | v61 | A1 | 差值 |
| --- | ---: | ---: | ---: |
| precision | 678/903 = 75.08% | 630/814 = 77.40% | +2.31 pp |
| hit@1 | 294/435 = 67.59% | 212/435 = 48.74% | -18.85 pp |
| hit@3 | 126/145 = 86.90% | 88/145 = 60.69% | -26.21 pp |
| hit@all | 65/145 = 44.83% | 52/145 = 35.86% | -8.97 pp |

有效 D0 报告从 81 变为 24；所以主 precision 的下降包含了有效 D0 组成的变化，不能直接解释成所有证据强度下都变差。与此同时，严格 hit 仍明显下降，覆盖差异不依赖把 D0 算作有效这一点。[clm-precision]

按原登记，以 9 个 NL 簇为整体、两臂配对抽样，保留簇内全部制品和轮次；10,000 次，seed=20260906。下表是差值的百分位 95% 区间，只有 9 簇，作为描述性敏感性，不提供 p 值、独立 435 单元检验或一般化承诺。[clm-uncertainty]

| A1 - v61 | 点差值（pp） | 簇配对区间（pp） |
| --- | ---: | --- |
| hit@1 | -20.69 | [-36.00, -9.22] |
| hit@3 | -26.90 | [-43.64, -13.85] |
| hit@all | -11.72 | [-26.23, -2.07] |
| L2 hit@1 | -40.17 | [-84.13, -14.07] |
| L2 hit@3 | -33.33 | [-78.57, -5.00] |
| L2 hit@all | -46.15 | [-85.71, -23.08] |
| precision | -3.71 | [-11.80, +3.29] |

9 簇中 7 簇总 hit@1 下降、2 簇略升；有 L2 台账的 8 簇，其 L2 hit@1 全部下降。逐簇留出时总 hit@1 差值仍为 -26.90 至 -17.33 pp，L2 为 -58.97 至 -29.29 pp；总 precision 可变为正值。故覆盖方向不由某一簇独自决定，但精度不宜给出确定方向。完整逐簇数值保存在 comparison，未选择性报告有利簇。[clm-uncertainty]

## 6. 历史偏离与可解释边界

1. **版本与站点不是严格匹配。** 当前 A1 为 12 谓词，v61 保存 19 谓词历史身份；旧 ID 映射只在统计/记录侧，method 不引入别名。judge 模型名称及协议相同不意味着同一个服务快照。完整 evidence 相同也不等于完整请求相同：报告内容、批次、匿名 ID、closure basis 和调用时间仍可能不同。[clm-limits]
2. **初批恢复不是完美遵守登记。** 原始 A1/full 大量空流后曾启动独立冷恢复；书面追加晚于实际启动。不能把这一段改写成原地重试或事前无偏设计。后续采用按 fingerprint 核验的成功阶段复用和 provider 失败恢复；`0033/r3` 从历史诊断格接续后重算了受变化输入影响的下游 D，不是整格原样复用。全部历史保留；最终冻结选择之后没有再替换 method。[src-registration][src-cases]
3. **两格 provider 诊断不能抹掉。** `0057/r3`（2 报告）、`0059/r1`（7 报告）各有 grounding lens 的 stream_read_error；均保留并完整 judge。它们所对应的台账合计只有 6 个 expected-round、其中 1 个 L2；就这两格直接可能改变的命中而言，最多覆盖整体 1.38 pp、L2 0.85 pp，解释不了观测到的全部下降。这个上限不约束全部历史恢复影响。另有 `0059/r3` 的 G2 backend error/blocked receipt，不能写成布尔结果或全部后端成功。[src-local-audit][clm-limits]
4. **自动 judge 有具体误读。** 保留所有冻结决定和审计反例，不能把观察到的关系越界默默修成更有利结果。新结果人工确认仍为 0；121 组核心文本匹配也不是同输入随机复测。[clm-judge-risk]
5. **full 不变的证据是软件对拍。** 七个固定 fixture 的旧 full、新默认、显式 none 的请求及决策对拍通过；扩展回归在旧/新源码都存在同样 13 个失败，没有新增失败。它支持本次开关不改变默认 full 的既定路径，不证明 12 谓词与 v61 的随机输出等价，也不需要重跑 v61。[src-smoke]

上述限制影响“精确效应能否全归因于 inspect”的强度，不改变这批已冻结结果的算术事实。当前最稳妥的实质解释是：**前置检查及其派生候选对行为问题的发现覆盖与重复命中具有明显支持作用；保留谓词验证本身，不能补偿缺失的候选入口。** precision 则应报告双口径及不确定性。此处不扩展到所有模型、整个 C1 或 A2 的结论。[clm-mechanism][clm-limits]

## 7. 统计解释自检与后续边界

依 ARS validate 检查 11/11 类统计陷阱；这不是“无偏证明”，整体解释等级为 CAUTION。[src-results][src-registration]

| 检查 | 本次处理 |
| --- | --- |
| Simpson 聚合反转 | 检查层级和九簇；公开 L1 微增及各簇异质性 |
| 生态谬误 | 不把簇级结果推出单个制品必然变化 |
| Berkson 选择偏差 | 54 pair 固定，不声称代表所有状态机总体 |
| Collider 条件化 | 不按后验成功率、有效率或报告量筛格 |
| 基率忽略 | 145 台账、各层分母、全部报告数同时保留 |
| 向均值回归 | 非按极端质量选样；仍披露历史非同期对照 |
| 幸存者偏差 | 162 格全判、所有报告纳入；冷恢复历史不隐去 |
| 多重搜索效应 | 所有登记主指标和方向都报告，不据区间跨零与否筛结论 |
| 分析路径自由度 | 原登记及追加澄清保留；严格口径不替换主口径 |
| 相关误当因果 | 机制案例与历史总差值分开；不作纯单因素贡献率 |
| 反向因果 | 开关先于生成和 judge；预期不作为完成或重跑门 |

交付到本次完整裁定、离线核销和结果归档为止，不自动启动方法修正、新 full、更多重复或质量重裁。原始失败、prompt、usage、响应流及恢复工具只保存在 ignored runs；公开归档足以复算冻结标签的算术，但不具备所有私有请求的远端重放条件。[clm-archive]

## 审计附录：证据链与事实源

### A.1 来源考据表

| source path | source creation commit | prefix commit | substantive fact commit 判定理由 | non-prefix revision/migration commit | canonical machine source |
| --- | --- | --- | --- | --- | --- |
| 本报告，非迁移 | 本文件首建提交，见 git log --follow | 2026-09-06 19:49:18 +08:00 结果冻结；分析源码 bbf1dd36f | 新增最终全量结果及分析，不将运行源码冒充文档创建提交 | 无 | final_results/a1_no_inspect_vs_v61_20260906/results.json |

### A.2 上游事实源清单

| 编号 / 引用键 | source_id | 事实源 | 类型 | 用途 | 关键锚点 |
| --- | --- | --- | --- | --- | --- |
| [src-results] | frozen_outcomes | [results.json](../final_results/a1_no_inspect_vs_v61_20260906/results.json) | json | 全量指标、逐报告裁定、逐格及台账支持 | /a1、/v61、/comparison |
| [src-sources] | provenance | [source_manifest.json](../final_results/a1_no_inspect_vs_v61_20260906/source_manifest.json) | json | 方法选择、judge 身份、失败和原件 hash | /method_selection、/a1_judge_sources、/unselected_judge_failures |
| [src-changes] | all_changes | [results.json](../final_results/a1_no_inspect_vs_v61_20260906/results.json) | json | 全部 164 条变化及支持 ID | /comparison/lost、/comparison/gained、/change_localization |
| [src-arithmetic] | arithmetic | [analyze_a1.py](../discover_matrix/docs/generations/a1_no_inspect_20260906/analyze_a1.py) | source-code | 全分母、逐格报告、指标与区间复算 | validate、calculate、compare |
| [src-registration] | registration | [原登记及 §7 追加](../discover_matrix/docs/generations/a1_no_inspect_20260906/preregistered.md) | md | 预期历史、来源、控制、恢复和完成门 | §1-§7.2 |
| [src-contract] | ablation_contract | [A1/A2 公约](../discover_matrix/docs/protocol/ablation_design_and_parallel_contract.md) | md | 关闭/保留边界，full 对拍 | §3.1、§5.1；主对照按用户追加澄清 |
| [src-smoke] | software_checks | [已有 smoke 报告](./2026-09-06-04-10-13-a1-smoke.md) | md | 七个 full 对拍及既有测试失败边界 | §3-§4、src-smoke-tests、cmd-full-compare |
| [src-local-audit] | local_audit | [本地 source_audit.json](../../../runs/paper1/a1_no_inspect_20260906/analysis/source_audit.json)、[method_context_audit.json](../../../runs/paper1/a1_no_inspect_20260906/analysis/method_context_audit.json)、[change_audit.json](../../../runs/paper1/a1_no_inspect_20260906/analysis/change_audit.json) | json，本地 ignored | 全阶段、回执、实际上下文与变化细节 | source_manifest.local_audit_hashes；远端只见 hash 和摘要 |
| [src-cases] | case_notes | [本地 case_notes.md](../../../runs/paper1/a1_no_inspect_20260906/analysis/case_notes.md) | md，本地 ignored | 具体 report/判读/仲裁反例与补裁依据 | 0034/r1、0001、0046/r3、0033/r3、0039/r2、0016/r2；hash 见 source_manifest |

### A.3 Claim-evidence map

| 编号 / 引用键 | claim_id | 结论 / claim | 类型 | 上游事实源与锚点 | 复验命令 | 置信度 | 限制 / caveat |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [clm-main] | A1-C1 | hit 大幅下降，K/N/I 全量核销 | count | src-results:/a1/metrics、/v61/metrics | cmd-a1 | high | 冻结 judge 结果，不是人工真值 |
| [clm-tiers] | A1-C2 | L2 覆盖/稳定性明显下降，L1 不全降 | count | src-results:metrics/tiers、per_round | cmd-a1 | high | 本样本和历史对照 |
| [clm-coverage] | A1-C3 | 162 格、814 报告无漏裁 | count | src-results:/a1/coverage、cells、reports、expected、judge_cell_sources | cmd-a1；cmd-source | high | 子批 success 不算完成 |
| [clm-inputs] | A1-C4 | 同证据文档和协议，closure 外壳不相同 | trace | src-results:/input_audit、/context_audit；src-local-audit | cmd-source | high | 远端摘要非私有输入重放 |
| [clm-mechanism] | A1-C5 | 候选入口缺失有机制证据，输出组成变化 | narrative | src-results:/method_stage_totals、reports；src-cases:0001、0046/r3 | cmd-a1；cmd-source；人工复验原件 | medium | 非全体效应唯一归因；未人工确认 |
| [clm-localization] | A1-C6 | 全部 164 条变化作根性质定位 | classification | src-results:/change_localization；src-local-audit:change_audit.rows | cmd-changes | high | 分类可复算，不等于语义等价 |
| [clm-precision] | A1-C7 | precision 方向依口径/簇组成，不能断言等价或暴跌 | narrative | src-results:metrics/precision、strict、reports、comparison | cmd-a1 | medium | 不确定性与 D0 组成已公开 |
| [clm-uncertainty] | A1-C8 | 簇级区间与逐簇留出方向 | count | src-results:/comparison/cluster_bootstrap_95pct、leave_one_cluster_out_delta_pp | cmd-a1 | high | 9 簇、探索性区间，非因果/总体显著性 |
| [clm-judge-risk] | A1-C9 | 存在核心文本裁定分歧和关系理由越界 | risk | src-results:/same_core_text_matches；src-cases:0034/r1 | cmd-source；人工复验原始输入/仲裁 | medium | 自动/agent 审计，未重裁；非噪声率估计 |
| [clm-limits] | A1-C10 | 历史版本、站点、恢复限制因果解释 | risk | src-registration:§7；src-sources；src-cases:0033/r3 | cmd-source；人工复验恢复链 | medium | 两格直接命中上限不是总恢复影响上限 |
| [clm-archive] | A1-C11 | 原件本地保留，公开算术可复算，不新增实验 | decision | src-sources:/raw_policy、raw_hashes、local_audit_hashes | cmd-a1；cmd-ignore | high | 无远端完整私有请求重放 |

### A.4 复验命令

以下从仓库根运行。`[cmd-a1]` 只需标准库；其余使用现有 venv，并要求本地 ignored 审计仍在。`$P`、`$B` 是本节专用相对路径变量，不承载凭据。

```bash
P=project_1_llm_state_machine_modeling/paper_stm_issue_discover
B=runs/paper1/a1_no_inspect_20260906

# [cmd-a1] 已保存判定的完整算术复算；不调用 provider
python "$P/discover_matrix/docs/generations/a1_no_inspect_20260906/analyze_a1.py"

# [cmd-source] 原件、序列化输入与 evidence 核验；仅写本地复验副本
env PYTHONPATH="$P/method/src:$P/judge/src:$P/evaluation/src:." \
  python "$B/checks/verify_a1_sources.py" \
  --a1 "$B/analysis/a1/analysis.json" --v61 "$B/analysis/v61/analysis.json" \
  --output "$B/analysis/source_audit-recheck.json"

# [cmd-changes] 全部变化的机械定位；不修改冻结标签
python "$B/checks/analyze_changes.py" \
  --a1 "$B/analysis/a1/analysis.json" --v61 "$B/analysis/v61/analysis.json" \
  --comparison "$B/analysis/comparison.json" --ledger "$P/discover_matrix/ledger_v2/ledger.json" \
  --output "$B/analysis/change_audit-recheck.json"

# [cmd-ignore] 本批原始审计不进入跟踪集合
git check-ignore "$B/analysis/case_notes.md" "$B/analysis/source_audit.json"
git ls-files "$B"
```
