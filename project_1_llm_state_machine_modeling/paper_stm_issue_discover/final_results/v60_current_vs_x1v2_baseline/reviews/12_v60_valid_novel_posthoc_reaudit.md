# v60 `VALID_NOVEL` post-hoc 复核记录

本文件记录对冻结 v60 Judge 中 444 条 `VALID_NOVEL` report 的复核结果。它不改写 Judge 输出，也不替代正式实验指标。逐条证据见 [`12_v60_valid_novel_posthoc_reaudit.json`](./12_v60_valid_novel_posthoc_reaudit.json)。

## 口径

- #189 P2：判断作者 PlantUML 源，不把编译器生成的 FCSTM 路由当成作者缺陷。
- #189 D/A 边界：承重事实不成立于作者源时走 A0；事实成立但没有违反可定位义务时走 D0。
- #195：同一根因、直接归因症状或 repair overlap 可以构成 `FULL`。
- 方法自报的 D 只留作来源字段，不参与本次分类。

## 全量机械统计

| 项目 | 数量 | 性质 |
|---|---:|---|
| `VALID_NOVEL` report | 444 | exact mechanical |
| pair | 46 | exact mechanical |
| pair-round 精确 phrase-key cluster | 419 | exact mechanical |
| same-pair 跨轮精确文本 key | 396 | exact mechanical |
| `(pair, property, actionable locus)` | 256 | exact mechanical |
| 方法自报 D2/D1 | 405/39 | exact mechanical，不作 verdict |
| 原子/可操作 facet | 约 242 | estimate |
| 全局 repair-root 上界 | 约 163–173 | 12-pair 人工样本外推 |

最后两行不是 444 条全量精确计数。12 个已审 pair 的 135 个 carrier group 合并为约 42–52 个 pair-local repair root；这里只保留估计范围。

## 保守 INVALID 下界

45 条 report、31 个 carrier group 已按现行协议确认不能保留为有效 source-defect report。

| 分类 | report |
|---|---:|
| A0 / `NOT_A_DEFECT_CLAIM`：compiler-owned `R45RouteToken` 初始路由 | 26 |
| A0 / `NOT_A_DEFECT_CLAIM`：unresolved grounding/frontier，不是 source-defect claim | 10 |
| A0 / `NOT_A_DEFECT_CLAIM`：delegated runtime scenario，没有形成作者源缺陷主张 | 6 |
| D0：certificate-only termination overclaim | 3 |

这 45 条逐项给出了 report ID、pair/round、原始 claim、Judge reason/basis、source refs 和审计依据，见 JSON 的 `confirmed_invalid_lower_bound.items`。

只应用这 45 条纠错时，v60 report-level precision 从 `1165/1271 = 91.66%` 变为 `1120/1271 = 88.12%`。这是 post-hoc sensitivity，不是冻结主结果。42 条 A0 的正式 subtype 都是 `NOT_A_DEFECT_CLAIM`；`compiler route`、`unresolved grounding` 和 `delegated scenario` 只是技术机制，不是额外 A0 类别。

## Ledger 关系候选

11 条 report、10 个 carrier group 是高可信 `FULL`/same-repair-root 候选。

| ledger | report | 关系依据 |
|---|---:|---|
| `EIS-0014-01` | 4 | 缺少 root initial 直接造成 InMotion/EmergencyStopping 及事件消费者不可达 |
| `EIS-0029-01` | 1 | AutonomousMode owner-local entry 缺失是层次丢失的直接 facet |
| `EIS-0043-02` | 2 | Region2 与消费者不可达来自 ledger 已记的 region entry 错位 |
| `VU-0040-01` | 1 | Power On consumer 不可达是 triggered root initial 的直接症状 |
| `EIS-0057-01` | 1 | CA 无默认子入口使三路 collision consumer 不可达 |
| `EIS-0039-02` | 1 | 修正 parent-scoped mode edge 的 source 同时修复缺失的 UrbanMode→HighwayMode 关系 |
| `EIS-0056-02` | 1 | 两者都要求把 Decrease UAV Count 从 guard 槽移到 effect |

这些关系仍需第二位 reviewer 签字。当前没有证据表明它们会增加 hit@3；目标 expected 已在其他 round 命中。它们可能改变 round-level `FULL` 和 K/N 归属。

## 人工样本

人工源文件检查已经确认几类 P2 风险：

- pair `0016` 的作者源直接写了 Interception Detected、Task Assignment Received 和 UAV-count decrease；7 条额外报告攻击的是 route-token lowering。
- pair `0059` 的作者源已经写了方括号 guard；24 条 `guard=null`/guard-disjointness 报告不能据此判作者源有缺陷。
- train signal-to-guard 家族筛出 58 条 D0 候选。NL 把 `Closed/SendDeparted`、`Reached Cruising/Cruise` 等写成触发信号，报告另加了独立 guard 义务。这一族尚未完成第二人逐条审阅。
- pair `0005` 的 11 条 endpoint 报告要求 composite-direct edge；作者源由复合态内的活动子状态提供相同行为。这一族仍是 D0 candidate，不计入 45 条下界。
- 自报 D1 中，pair `0006`、`0017`、`0056`、`0057` 的 9 条 region/cardinality report 有两个具体、结构相容的读法，可作为 genuine D1 下界。

## 敏感性范围

`114–202` 是当前筛查得到的 N→I candidate range，不是全量定稿。

| 情景 | K/N/I | precision |
|---|---:|---:|
| frozen | `721/444/106` | `1165/1271 = 91.66%` |
| 45 条确认 INVALID + 11 条关系候选 | `732/388/151` | `1120/1271 = 88.12%` |
| candidate invalid=114 | `732/319/220` | `1051/1271 = 82.69%` |
| candidate invalid=202 | `732/231/308` | `963/1271 = 75.77%` |

关系候选只做 N→K，不改变 precision。区间两端依赖尚未完成第二审的 D0/P2 family，不可写成正式实验事实。

## 与 INVALID 全量复审的组合读法

[`11_v60_invalid_manual_reaudit.md`](./11_v60_invalid_manual_reaudit.md) 已对冻结的 106 条 I
逐条复审。两个审计层互不重叠，因此可给出下列组合敏感性，但仍不得改写冻结主指标：

| 组合情景 | K/N/I | 性质 |
|---|---:|---|
| frozen v3.2 | `721/444/106` | 冻结机器输出 |
| 仅应用 I strict 复审 | `729/456/86` | 106 条 I 的完整人工复审 |
| 再应用 45 条 confirmed N→I | `729/411/131` | I 完整复审 + N 保守确认下界 |
| 再应用 11 条 pending N→K | `740/400/131` | 另含尚待第二 reviewer 的 relation 候选 |

最后一行的 11 条仍是候选，不能写成已确认修正；`114–202` 的 N→I 区间也不能与本表
混成一个新的“正式结果”。

## 历史条目

backend 或 predicate 不支持只影响 W，不能提供 D 的 scope 出口。原来标为 concurrency 的条目现按作者源重新判断；详细 provisional 状态见 JSON。

pair `0008` 和 `0018` 的 timing 项统一标为 `PENDING_D2_D1_D0_READJUDICATION`。本文件不再使用 `OUT_OF_SCOPE_CURRENT`。
