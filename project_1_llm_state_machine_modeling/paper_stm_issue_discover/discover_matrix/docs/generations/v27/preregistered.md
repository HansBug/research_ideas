# v27 大迭代：问题总账、设计计划与验收门

本文是在 v26-dnorm 全量运行之后、v27 实现与正式重跑之前冻结的诊断与计划。它的目的不是围绕某几个 benchmark 条目改 prompt，而是把当前方法在“生成、证成、发布、评判”四层暴露的问题一次收齐，再按领域来源、合成回归、分阶段 smoke 和全量统一评测完成一轮大迭代。

最终统计边界以 [final_output_metrics_policy.md](../../protocol/final_output_metrics_policy.md) 为准。本文中的 v26 严格回放数字用于定位问题，不是新的最终实验结果。

## 0. 本轮唯一优先级

v27 的设计取舍严格按以下顺序进行：第一，全量 release-only hit 必须显著高于同模型 X1v2；第二，L2 必须找出大部分且显著高于 baseline；第三，FP 必须可控，最低不能比 baseline 差；第四，prototype 从 STM+NL+形式制品生成最终 D1/D2 issues 的全量 API 成本不得超过同模型 X1v2 issue-generation 的 25x，允许个别 pair 或噪点超过。不能为了把平均成本或某个 pair 的倍率做漂亮而删掉有 hit 贡献的节点，也不能为了压 FP 回退到整体或 L2 不再显著领先。实验后的人工台账对账不属于 prototype、不调用 provider、不进入该成本分子。

当 prototype issue-generation 总体成本超过 25x 时，整改顺序固定为：压缩/去重各节点重复 prompt 与 dossier，稳定共享前缀以提高 cache read，修 schema 与结构化输出合同以减少非 provider retry，再检查低收益重复 review；只有消融证明某节点既不贡献 hit、也不改善 FP 或 W2 后才允许删除。provider error retry 可按协议豁免重复计费，其它 prototype 生成返工全部计费，因此“减少模型来回返工”本身就是成本控制的一部分。人工 hit/FP 评测不参与这一优化。

## 1. 当前可信起点

旧 v26 报告的 `226/435` 与 `566/953 FP` 把含 D0 的 raw finding 当成最终输出，已经废止。对旧 judge 结果按 D1/D2 final cluster 做过一次诊断性回放，当时得到整体约 `135/435 = 31.03%`、L2 `35/117 = 29.91%`、D2×L2 `28/102 = 27.45%`，以及约 276 个 D1/D2 final clusters、121 个 ledger-unmatched、`56.16%` precision；这些均不是人工逐条裁决，现统一降为无效调试估计，不能作为 v27 起点或任何正式比较。严格 v26 起点必须从 D1/D2 release issues 重新制作盲化人工评测包并逐条裁决。

同一 Luna baseline 的旧自动回放为整体 `154/435 = 35.40%`、L2 `22/117 = 18.80%`、D2×L2 `19/102 = 18.63%`，同样不再视为正式真值。现阶段只能确认方法存在大量 D0 截留与若干表达面缺口，不能在人工严格结果出来前断言方法相对 baseline 的准确差距；v27 仍必须把正确潜力转成 D1/D2 release issue，并在统一人工裁决后证明整体和 L2 显著领先，而不能只修 D2×L2。

## 2. D0 问题的真实构成

旧成功 judge 回放中，有 94 个台账命中位置只得到 D0 或 D_UNRESOLVED 支持，因此按最终口径被正确截住；其中 86 个只由 D0 支持、7 个只由 D_UNRESOLVED 支持、1 个同时由两者支持。台账侧构成为 D2 78 个、D1 16 个，按 D/L 交叉为 D2×L2 45、D2×L0 27、D2×L1 6、D1×L0 9、D1×L1 5、D1×L2 2。

这 94 个位置不能机械恢复。台账 D 是人工 ground truth 对缺陷的裁决，方法 D 是对自己主张与证据的裁决；两者对象不同。v27 的目标是修复“义务确实存在但方法没有把证据送到 D judge”的假性 D0，而不是让 D judge 看见台账 D2 后照抄 D2。

| D0 根因 | 当前表现 | 正确修法 | 不允许的修法 |
|---|---|---|---|
| 隐含 oracle 代替规范义务 | 可达非终态无出边、不可达 component 等形式事实为真，但 dossier 没有 NL 或领域义务证明它在本例中是缺陷 | 由 LLM 抽取 typed response/path/termination obligation，或给出可审计的领域规则适用判断，再把 exact formal fact 与该义务桥接 | “deadlock/unreachable 一律 D2”或按 diagnostic code 硬升档 |
| 只发现行为后果，没找到源义务 | 台账要求失败路径最终到 OperationalState，方法只报中间 deadlock | 在 obligation 层表达“随后、直到、必须继续、最终到达”等 source-to-target 性质，finding 同时保留 root cause 与 consequence | 仅靠同一状态名把 generic deadlock 当成任意响应义务 |
| negative/source certificate 不完整 | 方法说未声明变量、缺 effect、无 consumer，但只证明“当前证据没看到” | 从 canonical source AST、完整 inventory、inspect 与 mapping contract 构造穷尽的 negative certificate | 搜索 NL/代码字符串或把空列表直接当作语义不存在 |
| 方法 finding 与台账不是同一性质 | 例如台账要求特定初始目标，finding 只报缺无条件初始边；台账允许经中间态，finding 却要求直接边 | 保持 D0，不追回；通过人工评测的 same-location/same-property 约束阻止虚假恢复 | 为提高 hit 放宽为“提到同一元素就算” |
| D_UNRESOLVED 未细分 | targeted repair 后只剩统一 unresolved 标签，不知道是证据缺失、结构非法还是两读并立 | 拆成结构化 `missing_normative_basis`、`missing_formal_fact`、`ambiguous_reading`、`schema_repair_exhausted` 等 coverage gap，能降 D1 的降 D1 | 冷启动整格重跑或无差别增加 repair 次数 |

基于上述构成，94 个历史候选位置中合理可恢复的区间是约 35 至 55；其余应继续保持 D0，或在证据不足时保持 unresolved。该区间只用于安排工程优先级，不是人工真值。恢复成功的判据不是 D 标签变高，而是新 release issue 的义务、formal fact、source attribution 和 D rationale 全部闭合，并在盲化人工逐条裁决中命中。

## 3. 除 D0 外的主要缺口

### 3.1 Obligation 与表达面没有覆盖真实控制系统问题形态

在旧成功 judge pair 中至少有 33 条台账记录三轮全漏。按问题形态可归为下表；理论上限是三轮位置数，预期恢复包含生成方差，且各组与 D0 恢复、root-cause 对齐存在重叠，不能直接求和。

| 表达缺口 | 代表台账记录 | 理论上限 | v27 预期净恢复 |
|---|---|---:|---:|
| 复合触发、条件拆分与槽位压缩 | `EIS-0000-02`、`EIS-0020-02`、`EIS-0030-03`、`EIS-0050-01` | 12 | 6–9 |
| 数据/effect/action 的载体、附件与槽位错误 | `EIS-0005-03`、`EIS-0034-03`、`EIS-0034-05`、`EIS-0035-04`、`EIS-0045-01`、`EIS-0056-02` | 18 | 10–14 |
| 初始入口、事件 consumer、可达性与 deadlock | `INS-0002-02`、`EIS-0012-01`、`EIS-0034-02`、`EIS-0040-01`、`EIS-0046-01`、`INS-0046-03` | 18 | 12–16 |
| 精确 target、extra edge 与 hierarchy re-entry | `EIS-0009-01`、`DIFF-0024-04`、`EIS-0024-03`、`EIS-0039-02`、`EIS-0049-01` | 15 | 9–11 |
| Region/正交并发 | `EIS-0026-01`、`DIFF-0053-01` | 6 | 0，明确 out of scope |

这些缺口不能直接按台账条目新增特判。每个拟新增 obligation/operator 必须先在 Typed Obligation Surface 的领域来源审计中证明它来自控制系统实际检查需求或公认标准，再用不含上述真实 ID、名字和措辞的 synthetic fixtures 建立正例、反例、歧义例与 prose non-interference 测试，最后才允许进入 v27 prompt 与 compiler。

### 3.2 根因与后果没有形成一个可发布 issue

当前 discovery 分支经常在形式层找到“无出边、不可达、未消费、目标错误”等后果，但 release cluster 没有把它与 NL 中更具体的响应、终止、模式进入或数据更新义务绑定。反过来，某些 finding 只复述 NL 缺少某边，却没有给出当前 FCSTM 的具体行为后果。这导致一部分真问题被 D0 截住，另一部分虽然 D1/D2 但与台账性质错位。

v27 应把 finding 的最小单位冻结为 `normative obligation + violated formal property + source cause + observable consequence` 四联体。LLM 负责从 NL 与领域规则建立语义义务和 source/formal binding；确定性 compiler 只验证 exact ID、运行 assertion/program 并保存 trace。预计该修复可带来约 8 至 15 个位置，但它与 D0 35–55 的恢复区间高度重叠，不单独累加。

### 3.3 W2 执行面仍有“生成了程序但没有闭环”的损失

W2 的设计方向正确：真实编译、真实运行、terminal verdict、hash 和 semantic receipt 都必须存在。当前短板不是谓词逻辑本身，而是当首选 program 出现非法引用、backend exception、unsupported evidence 或 source attribution 不闭合时，缺少一条受控的二次校正与 sound fallback 路由，容易直接降 W1/W0 或形成 coverage gap。

v27 不向 LLM 暴露一个无限工具箱，而是为每类 typed obligation 冻结一条主 backend 和至多一条 sound fallback。compile/execute 失败时，repair LLM 只读取结构化错误、原 Evidence Program、可用 exact IDs 和 backend contract，输出一次修正版；仍失败则按已知原因降 W1/W0并落盘。所有成功的 W2 必须重新真实运行，不能复用“曾经生成过”的状态。目标是 D1/D2 release issue 中 W2 占比至少 80%，同时所有非 W2 issue 都有结构化降级原因。

### 3.4 去重存在，但评测曾绕过最终去重面

当前方法已有两级 cell 内去重：exact source cause key 合并技术 facet，LLM-C 的 `duplicate_of` 处理语义重复，最终产物是 `report_issue_clusters`。问题不是“完全没有 dedup”，而是旧 semantic judge 直接读 raw `finding_records`，使 dedup 的效果没有进入 FP 分母；此外，现有 96 个跨轮 unique FP cause 中仍可能混有同 cell 未合并重复、已确认不入台账、未决条目和真实台账漏记。

v27 先用新的 D1/D2 final-cluster judge 重算 emission 与 unique-cause 两套 FP，再对 unique causes 做四类成分审计。对于同 cell 重复，修 duplicate relation 或 cause key；对于确认不入台账的过度规定，收紧 obligation applicability；对于未决问题，保持 D1 并明确 alternative reading；对于可能真实台账漏记，只作为 validity 分析，不修改冻结主台账。目标是在不牺牲 hit 的前提下，将 unique-cause ledger-unmatched 数降低 20%–35%，并把 strict benchmark precision 提高到至少 65%。

### 3.5 运行失败与旧自动评测失败曾损失可计资格

v26 方法 162 格中记录了 7 个 local execution timeout、2 个 mixed failure 和 2 个 schema-invalid。按照仓库阶段流水线纪律，local timeout、mixed failure、证书或预算问题都必须降级落盘，不能让整格失败；只有 provider/transport 和穷尽定向修复后的 schema failure 可以使整格无效。

旧 judge 证据中出现过 `0010`、`0022`、`0025`、`0029`、`0032`、`0047`、`0053`、`0055` 八个失败 pair；历史报告只列五个，是因为后续重试中部分 pair 曾成功，以及聚合器按 mtime 可能让较晚失败覆盖较早成功。2026-08-19 新启动的自动 strict judge 又暴露 provider 与双向关系 schema 失败，但根据随后冻结的人工评测纪律，所有自动 judge 标签和失败资格均整体作废。v27 的评测资格只看人工 packet 是否齐全、人工标签是否逐项完成、是否发生材料泄漏；自动 judge 失败不再构成正式分母损失。

### 3.6 D judge 的输入信息和裁决合同仍需增强

D judge 已有 D2/D1/D0 定义、rationale、defeater 和 targeted repair，但目前 dossier 对“规范义务来自哪里”“formal fact 穷尽到什么范围”“source attribution 是否是 negative certificate”表达不够统一，导致台账 D2 对应的真 finding 也可能因证据链断裂落 D0。v27 应给每个 facet 提供同形字段：`normative_basis`、`applicability_reason`、`formal_fact`、`source_certificate`、`strongest_defeater`、`defeater_status`、`alternative_reading`、`recommended_d_level`，并在 prompt 中给出与真实 benchmark 无关的 D2/D1/D0 简例。

D judge 仍然一次处理整格以利用缓存和跨 finding 去重上下文；只有 schema 非法子集进入一次 targeted repair。不得按文本关键词预分 batch，也不得让确定性 validator 判断 alternative reading 是否“语义上成立”。

### 3.7 成本已接近上限，但不是本轮第一优化目标

v26 prototype 的 issue-generation 成本约 `$4.229658`，同模型 X1v2 issue-generation 成本约 `$0.225233`，`prototype / X1v2` 约 `18.78x`。25x 只约束 prototype 从 STM+NL+形式制品生成 D1/D2 issues 的 API 成本；实验后的人工 judge 只做 hit/FP 对账，不属于方法图，不产生 token 或美元成本，也不存在计费优化。用户优先级仍是 hit、FP、prototype 总体成本、再降成本，所以 v27 先保证能力与人工判定闭合，再通过冻结大前缀、整格 D 一次调用、结构化压缩 dossier 和缓存友好节点边界控制 prototype 倍率。

## 4. 大迭代实施顺序

| 阶段 | 输入 | 主要动作 | 输出 | 进入下一阶段的门 |
|---|---|---|---|---|
| P0 评测边界闭合 | v26 records、最终协议 | 只把 D1/D2 clusters 写入盲化人工 packet；逐台账、逐 emission 人工裁决；程序仅校验 exact ID 并做算术 | 可复核的 strict v26 人工基线 | 每个判断有人工理由与 supporting ID；无脚本/LLM 自动标签；旧 headline 不再被任何入口引用为最终结果 |
| P1 失败路径修复 | 11 个方法失败格 | 非 provider/schema 失败改降级；schema 原地反馈；失败 receipt 分类 | 零非许可整格崩溃的 smoke records | synthetic failure tests 全过；每个历史失败形态有回归 fixture |
| P2 领域来源与表达面扩展 | 四类表达缺口、既有 provenance | 对复合条件、action/effect、consumer、target/hierarchy 建立领域依据和 typed obligation | 冻结的 obligation/operator delta | 每个新增项有领域来源、正负/歧义 fixture，prompt 无真实台账内容 |
| P3 root-cause/evidence bridge | NL+PlantUML+FCSTM+inspect、P2 obligations | 生成四联体 finding；补 negative/source certificate；加入一次 program repair 与 sound fallback | D/W dossier 与真实执行证书 | prose non-interference、exact-ID、source attribution 和 W2 execution tests 全过 |
| P4 D 与去重收敛 | 全格 dossier | 统一 D 字段；整格一次裁决；非法子集定向修复；final cluster 去重 | D1/D2 release issues + D0 audit gaps | D 决策全集闭合或结构化 unresolved；同 cell duplicate 审计通过 |
| P5 合成与小型回归 | synthetic suite、历史五 pair smoke | 先跑合成套件，再跑 `0004/0023/0029/0046/0053` 只检查流程与已知能力 | 回归报告、成本估计 | 不因某个真实条目改 prompt；五 pair 无 crash，既有 D1/D2 hit 不回退 |
| P6 全量统一评测 | 冻结 v27、54 pair、三轮、X1v2 | 最大并发生成；冻结后制作人工 packet，从零逐条裁决并生成物理分臂表、逐条 ledger、FP 成分和成本 | 正式 v27 run record、人工标注与报告 | 下节硬门全部满足或如实判定 v27 未达标 |

## 5. 预期提升与目标区间

各修正项高度重叠，尤其 D0 恢复、root-cause 对齐和 obligation 扩展可能命中同一位置。下表的“局部潜力”用于安排优先级，不能逐行相加。

| 提升来源 | 局部潜力/预期 | 是否属于真实能力提升 | 主要风险 |
|---|---:|---|---|
| 恢复有充分义务与证据的 D0/D_UNRESOLVED | +35–55 positions | 是，前提是独立 D 与证据闭合 | 机械升 D 会同时推高 FP |
| 复合条件、effect/action、consumer、target/hierarchy 表达扩展 | +37–50 positions 的局部总潜力 | 是 | 与 D0 和 root-cause 项大量重叠 |
| root cause + consequence 四联体 | +8–15 positions | 是 | 可能把两个不同问题错误合并 |
| 方法 crash 降级与 judge 闭合 | +5–14 positions | 否，属于资格/测量恢复 | 不能写成发现能力贡献 |
| 去重与 applicability 收敛 | FP rate 不高于同网格 baseline；目标 unique FP cause 降 20%–35%、precision 至少 65% | 提升 precision，不直接增加 hit | 收得过紧会损失真 hit，不能破坏优先级 1/2 |
| Region/fork/join | +0 | 否，本轮明确不做 | 作为 limitation 与 W1/W0 边界保留 |

综合净增益采用三档估计，已经扣除主要重叠：

| 场景 | 相对严格诊断起点的净增益 | 预计整体 hit@1 | 相对 Luna X1v2 `154/435` | 解读 |
|---|---:|---:|---:|---|
| 保守 | +48 | 183/435（42.07%） | +29 positions，+6.67pp | 可能领先，但未必满足统计显著门 |
| 中性 | +60 | 195/435（44.83%） | +41 positions，+9.43pp | v27 主设计目标 |
| 乐观 | +70 | 205/435（47.13%） | +51 positions，+11.72pp | 需要 D0 与表达扩展同时稳定生效 |

旧自动回放曾给出 L2 `35/117`、D2×L2 `28/102`，但不再作为严格起点。v27 的最低门仍是完整 L2 超过半数，主目标约 `70/117`；D2×L2 最低超过半数，主目标 `60/102` 以上。这里的“显著领先”不能只看百分点：正式报告必须基于人工标签在 paired eligible positions 上给出配对显著性或按台账条目聚类的置信区间，要求方法相对 baseline 的差值置信区间下界大于 0。

## 6. v27 硬验收门

| 优先级 | 指标 | 硬门 |
|---:|---|---|
| 1 | 整体 release-only hit@1 | 方法显著高于同网格 baseline；工程目标为至少 `190/435` 的全网格保守下界，且 paired 差值的 95% 区间下界大于 0 |
| 2 | L2 | 必须超过半数且显著高于 baseline；最低 `59/117`，目标 `70/117`；D2×L2 至少 `52/102`，目标 `60/102` |
| 3 | FP/precision | 同一 paired eligible 网格下 release emission precision 不低于 baseline、FP rate 不高于 baseline；目标 precision 至少 65%、unique-cause FP 相对 strict v26 诊断下降至少 20%，且不得靠损失优先级 1/2 的 hit 达成 |
| 3 | W2 | D1/D2 release issues 中 W2 占比至少 80%，其余全部有结构化 W1/W0 原因；该门服务于 FP 可控和证据质量，不覆盖整体/L2 hit 门 |
| 4 | 运行与评测资格 | 非 provider/schema 的整格崩溃为 0；人工 packet 与逐项标注完整率目标 100%，任何未完成或作废单元同时报告 eligible 主读数与全网格下界 |
| 4 | Prototype 成本 | 完整网格的 `prototype issue generation / X1v2 issue generation` 不超过 25x；人工 judge 不属于该公式；允许个别 pair/noise 超过，不设单格 25x 门；超限只优化 prototype 的 prompt/cache/retry |
| 学术边界 | 泄漏与语义纪律 | 方法 prompt 无真实台账内容；NL 语义无 deterministic 字符串规则；每个新增 expression 有领域来源和 synthetic contract tests |

若整体 hit、L2 或 paired 显著性未过门，v27 不能以“某个切片大幅领先”宣布成功；若 hit 达标但 FP 比 baseline 差，应保留能力结果并继续做 applicability/dedup 收敛，不通过回退 obligation 表达面来换取表面 precision；若 prototype issue-generation 总体成本超过 25x，先压缩重复上下文、优化缓存边界和减少非 provider retry，不先删除已证明贡献 hit 或 FP 控制的节点。四项只有按优先级同时过门，v27 才算完成。

## 7. 本轮明确不做

1. 不为 `region/fork/join` 新建无领域依据的半实现；它们按已冻结 scope 写入 limitation，必要时以 W1/W0 报告。

2. 不把台账条目、真实 case 名、真实 judge 结论或漏检列表写入生成 prompt。

3. 不用关键词、字符串包含、正则、embedding、编辑距离或 identifier 形状完成 NL 语义、D、去重或 hit 判断。

4. 不把增加 retry 次数当作 schema 或 program 设计修复；每次 repair 必须携带具体结构化错误，并限定一次定向校正。

5. 不再以 raw finding 数、accepted 数或 confirmed 数替代 D1/D2 final release issue 指标。
