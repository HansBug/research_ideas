# A2 整个谓词机制消融：完整结果与原因审计

> 结论冻结于 2026-09-06 20:24:24 CST。正文 `[src-*]`、`[clm-*]`、`[cmd-*]` 对应文末审计附录。机器真源是本批 final_results；本文是解释入口。材料为冻结 A2/v61 实验记录，统计解释状态 ANALYZED；A2 新结果人工确认数为 0。[src-archive][src-provenance]

## 1. A2 没有出现预期的精度下降

A2 关闭整个谓词定义引导、路由、类型化参数绑定、编译、执行和回执过滤，保留自然语言需求、作者 PlantUML、FCSTM、前置检查、两路 grounding、普通语义定位、内部 D 筛选与发布归并。它仍能使用前置检查支持的语义候选，因此不是纯 LLM baseline。full 只引用冻结 v61 及已有裁定，本批没有新增 full 调用。[src-contract][src-prereg]

162/162 个唯一 pair-round、942/942 份报告全部裁定，435 个 expected-round 无缺失。A2 的平均 hit 与 precision 接近 v61，均略高；三轮并集覆盖略低，三轮稳定命中略高。四项九簇配对 bootstrap 区间全部跨零，当前记录不支持“撤掉谓词后精度下降”的预期，也不足以证明两种方法等效或 A2 更优。[clm-complete][clm-main][clm-uncertainty]

这里估计的是用户指定的历史对比。v61 是原 19 谓词运行，A2 来自当前 12 谓词软件基线，源码、prompt/schema、provider 和调用时间存在差异；默认 full 的软件行为对拍通过，不会把这两批随机实验变成严格单因素对照。[clm-scope]

## 2. 完整分母与主结果

唯一台账有 145 条，L0/L1/L2 分别为 71/35/39；54 个制品来自九个自然语言需求簇，每簇六个制品，各跑三轮。FULL `hit@1` 是三轮命中单元数 /435，`hit@3` 是至少一轮命中的条目数 /145，`hit@all` 是三轮均命中的条目数 /145。它们不是报告排序的 top-k。K/N/I 沿用冻结裁定的已知有效、台账外有效、无效报告分类；precision=(K+N)/全部发布报告数。N 包含重叠主张，不能直接读作独立新缺陷数。[src-ledger][src-analysis][clm-denominators]

主结果及 A2 减 v61 的差值如下；pp 表示百分点。[clm-main]

| 指标 | frozen v61 | A2 | 差值 |
| --- | --- | --- | --- |
| FULL hit@1 | 323/435，74.25% | 328/435，75.40% | +1.15 pp |
| FULL hit@3 | 130/145，89.66% | 127/145，87.59% | -2.07 pp |
| FULL hit@all | 82/145，56.55% | 92/145，63.45% | +6.90 pp |
| report precision | 759/903，84.05% | 800/942，84.93% | +0.87 pp |
| K / N / I | 561 / 198 / 144 | 582 / 218 / 142 | +21 / +20 / -2 |
| 发布报告数 | 903 | 942 | +39，+4.32% |

命中次数为 0/1/2/3 的台账条目分布，v61 是 15/19/29/82，A2 是 18/18/17/92。A2 在更少的独立条目上形成更多重复命中，故并集下降与稳定命中上升可以同时发生；不能把任一指标单独称为全面覆盖改善。[clm-repeat]

### 2.1 三个层级没有共同下降

表内均为 FULL 命中分子/固定分母。[clm-levels]

| 层级 | v61 hit@1 | A2 hit@1 | v61 hit@3 | A2 hit@3 | v61 hit@all | A2 hit@all |
| --- | --- | --- | --- | --- | --- | --- |
| L0 | 153/213 | 154/213 | 64/71 | 60/71 | 36/71 | 43/71 |
| L1 | 73/105 | 74/105 | 30/35 | 30/35 | 18/35 | 18/35 |
| L2 | 97/117 | 100/117 | 36/39 | 37/39 | 28/39 | 31/39 |

L2 hit@1 为 85.47% 对 82.91%，净多三个命中单元；L0 并集少四条，贡献了总体并集下降。该结果没有呈现 A1 的 L2 大幅损失模式。A1 的已冻结结果是 50/117，但两项消融及历史 full 之间的混杂仍须保留，不能由这三个数分配模块贡献比例。[clm-levels][src-a1][clm-scope]

### 2.2 轮次与需求簇差异大于总体净差值

三轮完整结果如下。[clm-rounds]

| round | v61 报告数 | A2 报告数 | v61 hit /145 | A2 hit /145 | v61 precision | A2 precision |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 325 | 300 | 113 | 106 | 283/325，87.08% | 256/300，85.33% |
| 2 | 287 | 316 | 98 | 104 | 227/287，79.09% | 273/316，86.39% |
| 3 | 291 | 326 | 112 | 118 | 249/291，85.57% | 271/326，83.13% |

第一轮 hit 净少七个，后两轮各多六个；precision 只在第二轮上升。round 标签不是共同随机种子，不能视为固定随机性的逐调用配对。[clm-rounds][src-prereg]

九簇的固定分母与 hit@1 如下；簇号沿台账身份，缺少 NL04 是固定语料选择。[clm-clusters]

| NL 簇 / hash | v61 命中 | A2 命中 | 差值 pp |
| --- | --- | --- | --- |
| NL01 / 3110cbcf，列车控制 | 60/78 | 55/78 | -6.41 |
| NL02 / abb20a21，基础制动 | 12/12 | 12/12 | 0.00 |
| NL03 / a01c022f，无人机集群 | 24/45 | 26/45 | +4.44 |
| NL05 / b7425c44，自动驾驶模式 | 66/93 | 70/93 | +4.30 |
| NL06 / a391765d，泵控制 | 44/57 | 47/57 | +5.26 |
| NL07 / 49854d04，碰撞避免 | 27/39 | 36/39 | +23.08 |
| NL08 / f1c3dc88，高层驾驶模块 | 47/60 | 39/60 | -13.33 |
| NL09 / 9fe426ba，混合动力车辆 | 11/15 | 10/15 | -6.67 |
| NL10 / 934e19bd，微波炉 | 32/36 | 33/36 | +2.78 |

五簇上升、三簇下降、一簇不变。去掉 NL07 后总体 hit 差值变为 -1.01 pp，说明 +1.15 pp 不能当作跨需求簇一致的增益。[clm-clusters][clm-uncertainty]

## 3. 严格口径与配对敏感性

### 3.1 D1/D2-only 仍没有精度大幅下降

严格口径只把外部 D1/D2 且非 INVALID 的报告计入有效分子；precision 分母仍保留全部发布报告，hit 只保留这些报告的 FULL 支持。它是同一批冻结裁定的敏感性视图，不是重新裁定。[clm-strict]

| 指标 | frozen v61 | A2 | 差值 pp |
| --- | --- | --- | --- |
| strict precision | 678/903，75.08% | 706/942，74.95% | -0.14 |
| strict hit@1 | 294/435，67.59% | 295/435，67.82% | +0.23 |
| strict hit@3 | 126/145，86.90% | 124/145，85.52% | -1.38 |
| strict hit@all | 65/145，44.83% | 74/145，51.03% | +6.21 |

主口径中，A2 有 94 份 D0 报告因正向台账关系归入 K，v61 有 81 份。严格视图排除它们后，precision 的微小正差变为微小负差。外部 D2/D1/D0/A0_FALSE_POSITIVE/A0_NOT_A_DEFECT_CLAIM 分布，A2 为 503/203/188/38/10，v61 为 505/173/158/52/15；内部 D 与这些外部标签属于不同判读阶段。[clm-strict][src-analysis]

### 3.2 四项九簇区间全部跨零

按事前计划，以九个 NL 簇成对重采样 10000 次，seed=20260906，保留各簇六个制品及三轮。表内是 A2 减 v61 的百分点差值；区间为各指标的描述性 95% 百分位区间，未作为四项联合显著性检验。[clm-uncertainty]

| 指标 | 点差值 | 95% 区间 | 逐簇留出差值范围 |
| --- | --- | --- | --- |
| hit@1 | +1.15 | [-5.17, +8.04] | [-1.01, +3.47] |
| hit@3 | -2.07 | [-5.76, +2.63] | [-3.17, 0.00] |
| hit@all | +6.90 | [-5.42, +19.69] | [+3.03, +11.20] |
| precision | +0.87 | [-4.05, +4.95] | [+0.005, +3.140] |

每项都有 10000 个可定义 replicate。簇数少且存在版本与调用条件混杂，区间跨零不能证明零效应；留出结果也不能升级为消除 provider 差异的检验。[clm-uncertainty]

### 3.3 Provider 分段的精度方向不同

按 A2 method 的站点来源划分，每段与 v61 完全相同的 pair-round 子集比较。旧站点是 `gpt-5.6-luna` profile，新站点是 `aizzz-luna-eval`；这张表不按 judge 站点分组。[clm-provider]

| Method 分段 | 格数 | v61 hit | A2 hit | v61 precision | A2 precision |
| --- | --- | --- | --- | --- | --- |
| 旧站点保留结果 | 37 | 91/111 | 91/111 | 187/222，84.23% | 244/271，90.04% |
| 新 Luna-only 站点 | 125 | 232/324 | 237/324 | 572/681，83.99% | 556/671，82.86% |

新站点段 precision 低 1.13 pp，旧站点段高 5.80 pp。分配由完成顺序和已登记的故障切换决定，未随机化；样本、时间和恢复历史共同变化，不能把差异归为站点质量。[clm-provider]

## 4. 净多五次命中背后有 83 次身份变化

全部 44 gained、39 lost expected-round 已追到两臂原始候选、内部 D、发布归并和外部裁定，共核验 279 个原始 evidence ID 引用。L0 为 24 gained/23 lost，L1 为 13/12，L2 为 7/4。以下列出能解释不同环节的实例，完整 83 行见机器审计表；类别是 agent 对阶段事实的解释，不能相加为互斥的因果贡献。[clm-changes]

| 实例 | 核对到的阶段事实 | 能说明什么 |
| --- | --- | --- |
| EIS-0057-01，r2 gained | v61 仅提取 cardinality/region 合同，未形成 operating-scope 激活候选；A2 发布 scope 不可达并获 FULL | 存在合同及候选覆盖差异，不只是执行过滤 |
| EIS-0056-02，r3 lost | 两臂都提取并绑定 variable_delta；A2 以空 effects 不足以判定为由留 D_UNRESOLVED，v61 使用缺计数变量与空 effect 形成 D2/W1 报告 | 损失发生在已绑定义务的内部判读，两臂相关报告均无 W2 |
| EIS-0050-01，r1 lost | 原始 D 响应把 takeover 候选的语义填到 initial-trigger ID，另一个 ID 得到 containment 的 unresolved 内容；ID 缺失修补没有纠正已有内容错位 | 精确 ID 覆盖不保证语义对应，详见 C004 |
| INS-0057-01，r2 lost | 初始迁移带 trigger 的 title/expected/observed 两臂逐字相同；v61 D2/K，A2 D0/I | 外部规范解释改变，不能说 A2 没发现该结构事实 |
| DIFF-0053-01 gained 与 INS-0053-02 lost，r3 | 两臂均发布两条缺边，也都把全局 stub 折入初始入口报告；外部对单边缺失能否覆盖全局互不可达/零行为的 FULL 边界不同 | 总 hit 不变仍可掩盖台账身份交换 |
| EIS-0049-01，r3 lost | 两臂都发布缺 HighwayMode→FinishState；v61 将它 FULL 匹配子级高速退出条件混用，A2 区分为不同义务 | 相近已发布核心的关系范围差异，不是候选漏检 |
| EIS-0056-01，r3 gained | A2 发布 route-token macro closure 缺口；外部 D0，但 relation-first 按端点 facet 计 K/FULL | 严格口径不保留此 gain，不能读成完整非确定性冲突已被指出 |

### 4.1 报告增量由候选与归并共同构成

以下是最终选定 method 原件的机械计数；W0/W1/W2 与 D 均为方法内部状态。[clm-stages]

| 环节 | v61 | A2 |
| --- | --- | --- |
| evidence records | 1863 | 1828 |
| D2 / D1 / D0 / D_UNRESOLVED | 1289 / 107 / 212 / 255 | 1368 / 60 / 120 / 280 |
| W0 / W1 / W2 | 227 / 1259 / 377 | 217 / 1611 / 0 |
| 发布门后、去重前 | 1396 | 1428 |
| exact dedup 减少 | 153 | 101 |
| 根因折叠减少 | 154 | 188 |
| guard modality 归并减少 | 186 | 197 |
| 最终报告 | 903 | 942 |
| 含 D_UNRESOLVED 的格 | 96 | 117 |
| W1 且 D_UNRESOLVED 的 evidence | 22 | 63 |

报告差额满足 `+32 +52 -34 -11 = +39`：发布前多 32，exact 去重少减 52，折叠多减 34，guard 归并多减 11。这是账面恒等式，不是“谓词避免多少误报”的因果分解。最终所有格 completed，也不代表其内部每条义务闭合。[clm-stages]

A2 的 63 条 W1/unresolved 中，state_action 有 24 条、effect 八条、transition_endpoints 十条、variable_delta 一条。普通精确绑定后仍可能因语义证据不足而不发布。六个正常零报告格是 0021:r2、0031:r1、0041:r1、0041:r3、0051:r3、0055:r1，均保留并完成裁定；它们不包括被 provider 错误替换的旧 0009:r2。[clm-stages][clm-complete]

### 4.2 两臂都存在需要讨论的裁定内容风险

同一 pair-round 内，有 269 组报告的 title/expected/observed 三字段逐字相同，其中 96 组 KNI/D/A 分类组合不同，46 组 FULL 目标集合不同。其他字段、报告批次、provider、调用时间可能不同，所以这不是相同请求的重复实验，也不是 judge 错误率估计。[clm-judge]

六个独立案例保留原报告和标签：[clm-cases]

- C001，0003：同样的 PoweredOff→Operate 事实，因为“上电”是否要求无条件初始进入的解释不同，得到 D0/I 与 D2/N。
- C002，0006:r1：十份报告为 1 K/9 N/0 I，其中 event-locus 与 scope-locus 报告重复描述相同不可达消费者。九份 N 不能读作九个独立新缺陷。
- C003，0002：grounding 从功能要求推导更强的无条件入口义务；外部 D0 仍可能因 FULL 关系归 K，主口径和严格口径会分离。
- C004，0050:r1：原始 provider action 已存在 D 内容与义务 ID 错位；不是收集器把正确内容映射错。语义对应不能靠词法近似 validator 保证。
- C005，A2 0009:r2：FULL 理由声称某聚合报告明确列出 FinishState/dist_to_exit 出口，完整序列化报告并未包含这些内容。两条 hit 各有其他 FULL 支持，不能直接净扣两个命中。
- C006，历史 v61 0054:r3：四条件聚合报告没有 EmergencyStopping 或 obstacle，FULL 理由却称其明确报告该出口缺 trigger；VU-0054-01 的历史 hit 只有这一份 FULL 支持。原输入回执 hash 与从 committed method 重建的四份报告均已核对。

这些事实支持讨论语义裁定边界与内容-ID 对应，但没有授权改标签、重标台账或重跑质量较差的结果。对称保留 v61 与 A2 的反例，不能只修一臂后继续相减。[clm-cases][clm-scope]

## 5. 来源、核验与下一步讨论边界

Method 使用三段冻结来源：`fc5801981` 的 20 格/155 报告、`282e40cf4` 的 17 格/116 报告、`ed64788ed` 的 125 格/671 报告。前两段为旧站点，新段为 `https://api.aizzz.xyz/v1` 的 `aizzz-luna-eval`，模型均登记为 `gpt-5.6-luna`。judge 保留旧站点七格/51 报告，新站点完成 155 格/891 报告，后续原生 CLI 使用 16 workers、批次串行、既有 transport retries=8；没有按质量重裁。[clm-provenance]

三段机制审计分别覆盖 207、188、1367 处上下文，共 1762 处，均标记 `partial=true`；它们包含旧 0009:r2 的 provider 降级尝试，不能把 163 份历史格记录读成 163 个最终样本，也不能声称检查了全部 `.part` 请求。最终选择表排除该 HTTP 520 零报告 predecessor，但保留其原件、hash 和原因。[clm-provenance]

逐格核验覆盖 942 份报告的 adapter 投影、输入 hash、匿名 ID 解码及最终 metric 重算。A2 与 v61 每格投递的证据文档全部字段、expected issues 字段一致，共 2106 次文档投递；报告内容和外层 closure 元数据并未宣称相同。归档保存 648 份输入文件、method/judge 结构化原件、切换与错误索引；原始流及完整历史 v61 judge 输入只在 ignored runs。远端能复算裁定算术和 A2 投影，不能重读所有历史输入或复现 API 随机输出。[clm-verification]

统计解释已按 11 类常见误推断核查：报告了分簇和 provider 分段，未从簇均值推个体因果；未按效果选择 provider 或剔除未完成样本；明确 precision/命中分母和重复报告；未把极端子组改善当回归均值之外的收益；保留全部指标、严格视图、事前及运行中追加规则；不以四项未校正区间宣称联合显著性；版本及时间混杂限制因果解释，调用顺序不能单独识别作用方向。固定九簇的样本选择和运行中恢复仍限制外推，核查不等于消除了偏差。[clm-stat-limits]

当前可用于下一步讨论的判断是：前置检查保留时，撤掉整个谓词机制没有产生预期的总体质量下降；执行证据的缺失与缺陷报告质量的变化必须分开论证。现有候选重叠、内部语义未闭合、发布归并和外部关系边界，都可能抵消或遮蔽机制差异。需要先决定哪些结论已有足够证据、哪些需要人工确认，再讨论是否调整方法或评测；本次归档只冻结已有结果，不把这些讨论方向写成已确定的修正任务。[clm-main][clm-stages][clm-cases][clm-scope]

## 审计附录：证据链与事实源

### A.1 来源考据表

| source path | source creation commit | prefix commit | substantive fact commit 判定理由 | non-prefix revision/migration commit | canonical machine source |
| --- | --- | --- | --- | --- | --- |
| 本报告 | 本文件的首次新增提交，见 [cmd-history] | 同首次新增提交；时间前缀为完整结果冻结时刻 | 首次写入 162/942 完整结果、83 条变化审计及解释限制 | 无迁移 | [本批归档](../final_results/a2_no_predicates_vs_v61_20260906/README.md) |
| A2 method 原件 | `fc5801981` / `282e40cf4` / `ed64788ed` 为运行源码，不是本报告创建提交 | 不适用 | 三段冻结选择与实际 source_provenance | 无原件改写 | `raw/source_runs/*/method/*/round-*.json` |
| v61 对照 | 主源码 `ea6141607`，0045:r1 补格源码 `778212b03` | 不适用 | 按历史归档既定选择引用 162 格及既有裁定 | 无 | [v61](../final_results/v61_source_divergence_vs_x1v2_baseline/README.md) |

### A.2 上游事实源清单

下表以 `A=final_results/a2_no_predicates_vs_v61_20260906` 表示论文内归档路径。

| 编号 / 引用键 | source_id | 事实源 | 类型 | 用途 | 关键锚点 |
| --- | --- | --- | --- | --- | --- |
| [src-archive] | archive | [归档与复算](../final_results/a2_no_predicates_vs_v61_20260906/README.md) | md | 原件布局与远端边界 | 内容/离线复验/来源边界 |
| [src-analysis] | analysis | [analysis.json](../final_results/a2_no_predicates_vs_v61_20260906/derived/analysis.json) | json | 全部分母、指标、分层、变化、敏感性 | `/a2`、`/v61`、`/changes`、`/paired_uncertainty` |
| [src-ledger] | ledger | [冻结台账](../final_results/a2_no_predicates_vs_v61_20260906/raw/ledger.json) | json | 唯一 145 条及 L/NL 身份 | `/items/*/{L,pair,pair_context}` |
| [src-change] | change_audit | [change_audit.json](../final_results/a2_no_predicates_vs_v61_20260906/derived/change_audit.json) | json | 83 条原始阶段追踪 | `/rows`；ledger_id + round |
| [src-case] | case_audit | [case_audit.json](../final_results/a2_no_predicates_vs_v61_20260906/derived/case_audit.json) | json | 六案例事实、解释与限制 | `/cases`；case_id + evidence_pointers |
| [src-method] | method_raw | [method 原件](../final_results/a2_no_predicates_vs_v61_20260906/raw/source_runs/) | json | 候选、D/W、发布与来源 | `*/method/*/round-*.json`；`evidence_records`、`stage_outputs/publish` |
| [src-judge] | judge_raw | [judge 原件](../final_results/a2_no_predicates_vs_v61_20260906/raw/judge/) | json | 原输入、匿名映射和原裁定 | `*/{inputs,pairs}/*.json` |
| [src-input-audit] | input_audit | [judge_input_audit.json](../final_results/a2_no_predicates_vs_v61_20260906/derived/judge_input_audit.json) | json | 输入文档完整字段核验 | `/rows/*/{fingerprints,a2_input_sha256,v61_input_sha256}` |
| [src-provenance] | provenance | [provenance.json](../final_results/a2_no_predicates_vs_v61_20260906/provenance.json) · [manifest](../final_results/a2_no_predicates_vs_v61_20260906/archive_manifest.json) · [checks](../final_results/a2_no_predicates_vs_v61_20260906/raw/checks/) · [transport](../final_results/a2_no_predicates_vs_v61_20260906/raw/transport_audit.json) | json | 来源、选择、恢复、核验范围与文件 hash | source_roots、predecessor_attempts、included_files、checked_contexts、partial、traces |
| [src-v61] | v61 | [冻结 v61](../final_results/v61_source_divergence_vs_x1v2_baseline/README.md) | json/md | 全量历史对照和 C006 原件 | `raw/v61_current`、`raw/v61_current_fill0045`、`raw/judge_v3.11_iter6cfg/current-r*/pairs` |
| [src-code] | analysis_code | [analyze.py](../discover_matrix/docs/generations/a2_no_predicates_20260906/analyze.py) · [archive.py](../discover_matrix/docs/generations/a2_no_predicates_20260906/archive.py) | source-code | 固定选择、原指标复用与归档校验 | quality、load_selection、paired_uncertainty、judge_input_audit、validate |
| [src-prereg] | preregistration | [登记及追加规则](../discover_matrix/docs/generations/a2_no_predicates_20260906/preregistered.md) | md | 事前假设与运行中偏离 | §2/§5/§9/§11/§13 |
| [src-contract] | ablation_contract | [A1/A2 公约](../discover_matrix/docs/protocol/ablation_design_and_parallel_contract.md) | md | 保留/关闭边界 | §3.2/§4/§5/§6 |
| [src-a1] | sibling_a1 | [A1 冻结结果](https://github.com/HansBug/research_ideas/blob/de60df54ecb2d071f6bdccb6012326ea869cd152/project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/a1_no_inspect_vs_v61_20260906/results.json) | git-commit/json | 仅供两项消融结果对照讨论 | A1 L2=50/117；不参与 A2 计算 |

### A.3 Claim-evidence map

| 编号 / 引用键 | claim_id | 结论 / claim | 类型 | 上游事实源与锚点 | 复验命令 | 置信度 | 限制 / caveat |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [clm-complete] | A2-COMPLETE | 162 格、942 报告、435 expected-round 完整 | count | [src-analysis] `/a2/coverage`；[src-judge] 原件 | [cmd-recompute]、[cmd-projection] | high | completed 不代表内部义务全部闭合 |
| [clm-denominators] | A2-DENOM | 145 台账、九簇、KNI 与 FULL 定义 | classification | [src-ledger] `/items`；[src-code] quality | [cmd-recompute] | high | N 不是独立新缺陷数 |
| [clm-main] | A2-MAIN | 主结果与 +39 报告；未见预期精度下降 | count | [src-analysis] `/a2/metrics`、`/v61/metrics` | [cmd-recompute] | high | 只描述冻结裁定，不证明等效或因果 |
| [clm-repeat] | A2-REPEAT | 0/1/2/3 次命中分布与并集/稳定性分离 | count | [src-analysis] 两臂 `/expected` 按 ledger_id 求和 | [cmd-recompute] | high | 不是对每次差异的因果归因 |
| [clm-levels] | A2-LEVELS | 三层 hit 全表，L0 并集少四条 | count | [src-analysis] 两臂 `/metrics/tiers` | [cmd-recompute] | high | 层级内仍有异质性 |
| [clm-rounds] | A2-ROUNDS | 三轮方向不一致 | count | [src-analysis] 两臂 `/per_round` | [cmd-recompute] | high | 非共同随机种子 |
| [clm-clusters] | A2-CLUSTERS | 五升三降一平及 NL07 留出翻转 | count | [src-analysis] `/per_cluster`、`/paired_uncertainty`；[src-ledger] NL 身份 | [cmd-recompute] | high | 只含九个固定需求簇 |
| [clm-strict] | A2-STRICT | 严格口径及 D0-to-K 分离 | count | [src-analysis] `/metrics/strict`、`/reports` 的 d_tier/validity | [cmd-recompute] | high | 冻结标签的敏感性，不是改标 |
| [clm-uncertainty] | A2-UNCERTAINTY | 四区间跨零、逐簇留出范围 | count | [src-analysis] `/paired_uncertainty` | [cmd-recompute] | high | 描述性区间；未作等效或联合显著性检验 |
| [clm-provider] | A2-PROVIDER | 两个 method 站点段精度方向不同 | count | [src-analysis] `/provider_paired_sensitivity` | [cmd-recompute] | high | 完成顺序选段，不识别 provider 效应 |
| [clm-changes] | A2-CHANGES | 44 gained、39 lost、279 引用和阶段定位 | trace | [src-change] `/rows`；[src-analysis] `/changes` | [cmd-change]；解释人工复验 | medium | agent 判读；阶段事实不构成互斥因果类别 |
| [clm-stages] | A2-STAGES | D/W、去重归并、unresolved 和正常零报告 | count | [src-method] evidence_records、stage_outputs/publish；[src-v61] 同字段 | [cmd-stages] | high | 数量恒等式不是误报过滤效应 |
| [clm-judge] | A2-JUDGE-TEXT | 269 组相同三字段，96 分类变化、46 FULL 变化 | count | [src-analysis] `/shared_report_text_audit` | [cmd-recompute] | high | 其他字段可不同，不估计 judge 错误率 |
| [clm-cases] | A2-CASES | 六案例及双臂关系内容风险 | trace | [src-case] case_id 与原始指针；C006 另见 [src-v61] | [cmd-projection]；原件语义人工复验 | medium | agent 解释，不是人工重裁；历史完整输入仅本地 |
| [clm-provenance] | A2-PROVENANCE | 三来源、两站点、1762 partial 上下文与旧格保留 | trace | [src-provenance] checks、selection、predecessor；[src-method] manifest | [cmd-archive]、[cmd-stages] | high | 不把 partial 写成全流审计 |
| [clm-verification] | A2-VERIFY | 报告投影与指标闭合；2106 文档投递字段核验 | trace | [src-input-audit] `/rows`；[src-judge] serialized_input_hash；[src-provenance] input_files | [cmd-archive]、[cmd-projection] | high | v61 输入全内容不在远端；live 随机输出不可复现 |
| [clm-scope] | A2-SCOPE | 历史对比；保留标签，停止于已有结果分析 | risk/prohibition | [src-prereg] §9/§13；[src-contract]；[src-case] boundary | 人工复验源码身份与登记 | high | 不证明两种被关闭机制各自的作用 |
| [clm-stat-limits] | A2-STAT-LIMITS | 11 类推断风险已检查且限制保留 | risk | [src-analysis] 完整分母/分层/敏感性；[src-prereg] 选择与追加规则 | [cmd-recompute]；人工复验解释 | medium | 检查不能消除固定样本、历史对照与恢复混杂 |

### A.4 复验命令

在仓库根按归档 README 设置 `P`、`G`、`PYTHONPATH`。[cmd-archive] 为 `venv/bin/python "$G/archive.py" validate`；[cmd-recompute] 为归档 README 的完整离线重算代码块，逐项比较主/严格指标、分层、变化及 bootstrap。

[cmd-projection]：校验全部 A2 报告投影、输入回执、匿名映射和每格指标。

```python
from pathlib import Path
import json
from paper_stm_judge.models import PairJudgeResult
from paper_stm_judge.artifacts import adapt_evidence_discovery_release, stable_model_hash
from paper_stm_judge.metrics import compute_semantic_metrics, decode_outcomes
import archive
root = archive.DESTINATION.resolve()
r = json.loads((root / 'derived/analysis.json').read_text())
cells = {(c['pair_id'], c['round']): c for c in r['a2']['cells']}
seen, reports = set(), 0
for path in sorted((root / 'raw/judge').glob('*/pairs/*.json')):
    p = PairJudgeResult.model_validate_json(path.read_text())
    key = p.pair_id, p.round
    assert key not in seen
    seen.add(key)
    c = cells[key]
    source = root / 'raw/source_runs' / c['run_id'] / 'method' / p.pair_id / f'round-{p.round}.json'
    projected, audit, rnd, pid = adapt_evidence_discovery_release(source, p.adapter_audit.expected_id_map)
    value = json.loads((path.parent.parent / 'inputs' / path.name).read_text())
    assert (pid, rnd) == key and audit.report_id_map == p.adapter_audit.report_id_map
    assert [v.model_dump(mode='json') for v in projected] == value['reports']
    assert stable_model_hash(value) == p.serialized_input_hash
    assert compute_semantic_metrics(p.final_reading) == p.metrics
    assert decode_outcomes(p.final_reading, p.adapter_audit) == (p.report_outcomes, p.expected_outcomes)
    reports += len(p.report_outcomes)
assert len(seen) == 162 and reports == 942
```

[cmd-stages] 与 [cmd-change]：先执行以下 Python，按归档身份定位两臂 method 原件；统计内部阶段并核验全部审计引用。

```python
from collections import Counter
import json
import archive
a = archive.analyze
root = archive.DESTINATION.resolve()
r = a.read(root / 'derived/analysis.json')
records = {}
for arm in ('a2', 'v61'):
    records[arm] = {}
    for c in r[arm]['cells']:
        if arm == 'a2':
            base = root / 'raw/source_runs' / c['run_id']
        else:
            name = 'v61_current_fill0045' if c['run_id'] == '0e450e5c6c9d4841820c7d1fd2a888ea' else 'v61_current/method'
            base = root.parent / 'v61_source_divergence_vs_x1v2_baseline/raw' / name
        records[arm][c['pair_id'], c['round']] = a.read(base / 'method' / c['pair_id'] / f"round-{c['round']}.json")
    cells = list(records[arm].values())
    ev = [e for c in cells for e in c['evidence_records']]
    pub = [c['stage_outputs']['publish'] for c in cells]
    counts = {k: sum(p.get(k, 0) for p in pub) for k in ('pre_dedup_release_count', 'folded_issue_count', 'guard_modality_aggregated_count', 'report_issue_count')}
    counts['exact_dedup_removed'] = counts['pre_dedup_release_count'] - sum(counts[k] for k in ('folded_issue_count', 'guard_modality_aggregated_count', 'report_issue_count'))
    print(arm, len(ev), Counter(e['d_level'] for e in ev), Counter(e['witness_level'] for e in ev), counts)
    print('unresolved_cells', sum(any(e['d_level'] == 'D_UNRESOLVED' for e in c['evidence_records']) for c in cells))
    print('W1_unresolved', Counter(e['property'] for e in ev if e['witness_level'] == 'W1' and e['d_level'] == 'D_UNRESOLVED'))
    print('zero_reports', [(c['pair_id'], c['round']) for c in cells if not c['report_issue_clusters']])
rows = a.read(root / 'derived/change_audit.json')['rows']
changes = {(c['ledger_id'], c['round']): c for c in r['changes']}
assert len(rows) == len({(c['ledger_id'], c['round']) for c in rows}) == len(changes) == 83
refs = 0
for row in rows:
    change = changes[row['ledger_id'], row['round']]
    assert row['change'] == change['change']
    for arm in records:
        ids = {e['issue_id'] for e in records[arm][change['pair_id'], row['round']]['evidence_records']}
        assert set(row[f'{arm}_evidence_ids']) <= ids
        refs += len(row[f'{arm}_evidence_ids'])
assert refs == 279
print('changes', Counter(c['change'] for c in changes.values()), 'verified_references', refs)
```

[cmd-history]：`git log --diff-filter=A --format='%H %aI %s' -- "$P/reports/2026-09-06-20-24-24-a2-no-predicates-v61-results-cn.md"`。这是本报告的创建提交定位，不与运行源码或此前审计提交混用。
