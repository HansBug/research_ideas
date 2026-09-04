# 迭代 1：v3.4 / prompt v8（代码提交 `5668bf602`，2026-09-03 01:12–02:37）

模型 `gpt-5.6-luna`；子集 `subset_v1`（current 201 条 / baseline 100 条）；原始制品在被忽略的 `runs/paper1/judge-calibration-5668bf602/`；两侧 6 次调用全部成功，无 pair 失败；provider 成本合计 $8.54（cost_eligible 全部为真）。逐条对齐见 [current/summary.md](./current/summary.md)、[baseline/summary.md](./baseline/summary.md) 与各自的 `disagreements.md`。

## 与事前登记判据的对照

| 判据 | current | baseline | 门槛 | 结果 |
| :-- | :-- | :-- | :-- | :-- |
| P1 K/N/I 一致率 | 132/201 = 65.7%（冻结 judge 26.9%） | 46/100 = 46.0%（冻结 30.0%） | ≥ 85% | 未达 |
| P2 冻结 N、人工 I 层判 I | D0 层 25/60 = 41.7%；NADC 层 47/50 = 94.0%；合计 73/111 = 65.8% | 6/25 = 24.0% | ≥ 80% | 未达 |
| P3 冻结 I、人工有效层判有效 | I→K 5/8、I→N 6/12，合计 11/20 = 55.0% | I→K 13/20、I→N 11/21，合计 24/41 = 58.5% | ≥ 75% | 未达 |
| P4 K→K 保持 K | 19/30 = 63.3% | 10/15 = 66.7% | ≥ 95% | 未达 |
| P5 五类 defect 一致率 | 65/201 = 32.3%（其中 D2↔D1 混淆 18） | 40/100 = 40.0%（D2↔D1 15） | 信息性 | 记录 |
| P6 方向偏差（新 judge 有效率 − gold 有效率） | 44.3% − 38.3% = +6.0 pp | 67.0% − 68.0% = −1.0 pp | ≤ 5 pp | current 未达 |

## 红旗

1. 分层上新 judge 比冻结 judge 更差的：无（各层一致率均不低于冻结值）。
2. 分歧集中度：无单一 pair 占 40% 以上。
3. baseline 报告被判 `A0_NOT_A_DEFECT_CLAIM`：0 条。
4. 失败 / 覆盖：0 失败，两侧 301 条全部覆盖。
5. 仲裁比例：current 193/201、baseline 72/100，高于 30% 的登记门槛。对照冻结 v3.2 同类数字：current r1 有 375/415 条报告触发过仲裁、baseline r1 有 83/145 条，分歧主要来自 clause 角色/裁决层面，属既有行为而非本版引入；本轮新增的 `defect_class` 冲突在 current r1 只有 7 条、baseline r1 有 10 条。此红旗如实记录，不改登记门槛。

## 分歧模式（读 reason / basis 得出，按影响面排序）

1. **一致性 validator 与作者源基准叠加把有效报告逼成 A0_FALSE_POSITIVE。** 报告说「缺 guard / 缺 effect / 无数据侧表示」，judge 看到作者在 transition label 上写了该内容，就把核心 clause 判 REFUTED；validator 随即禁止 D2/D1，只剩 A0_FALSE_POSITIVE。current 侧 71 条 FP 中只有 5 条与 gold 一致，K→K 掉的 11 条、I→K/I→N 没救回的 9 条大多属此；baseline 侧 19 条 FP 中 1 条一致。人工口径是：这类事实关于载体槽位，永远不是 FP，按 D1 / D0 / NADC 分。
2. **复合主张里一个说过头的分句被当成整条为假。** baseline 的「exit_urban 未定义且无后续」「无到 cruise 的迁移」（实为无条件迁移存在而缺条件）「两个 region」（实为三个、要点是独立性）等，人工按承重关切判 D1/D2，judge 判 A0_FP。这是 baseline I→K/I→N 与 K→K 失分的主因。
3. **把建模偏好当义务。** 完整/对称覆盖、显式自环表示驻留、标识符定义与命名、事件优先级、复合边界迁移复制到子状态、要求在上一层有直连边而嵌套层已实现、NL 提到的行为在结构里已实现却缺字面元素——judge 给 D1/D2，人工 D0。baseline N→I 层 25 条只有 6 条判 I，current N→I/D0 层 60 条只有 25 条判 I，主要在此。
4. **「上电进入 X」的标准实现被判 D2。** `[*] --> Off` 加 `Off --> Operate : start` 对 NL「once powered on the system enters Operate」，current 侧 6 条人工全 D0，judge 全 D2。
5. **事件名 label 与布尔表达式 label 未区分。** 人工对「缺 guard 而 label 是事件名（Closed、Approached、Start Mission）」一律 D0，对「label 是布尔表达式（`x>=25`、`flag=true`）」给 D1；judge 把前者也给成 D1。该区分可直接按 label 文本判定。
6. **relation 阶段**：两条 baseline 正交区域类报告 judge 判 D2 但 NO_MATCH（人工 FULL/PARTIAL），另有少量 gold N 被匹配成 K；样本少，本轮不动 relation 提示词，下一轮观察。

## 对下一轮（v3.5 / prompt v9）的调整

只改提示词，不改子集、gold、判据或 validator：(1) clause 裁决按报告的称职读法，「缺 X」的称职读法是「无单独的 X 载体」，作者以 label 承载时该 clause 判 SUPPORTED，由 defect class 决定是否成缺陷；载体槽位主张永不 A0_FALSE_POSITIVE；(2) 复合/自由文本主张按承重关切判，说过头的分句归 AUXILIARY_CONTEXT，「nearby defect 不能救」限定为不同 locus 或不同修复义务；A0_FALSE_POSITIVE 只留给关切整体被作者源反驳；(3) 义务只能来自 NL 陈述、隐式测试预言、领域必备三源，列举常见建模偏好为 D0，D1 的缺陷读法本身也必须落在三源之一；(4) 事件名 label → D0、布尔表达式 label → D1、方括号 guard 或只关于派生槽位 → NADC；(5) label 文本承载内容但不创造结构（标为 initial 的迁移不是初始伪状态边）；(6) 以派生元素命名描述作者源缺失的报告按缺失本身判；(7) 只以 label 文本承载的 action/effect 缺失保留 D1；(8) 「初始/空闲状态 + start 触发进入运行状态」是「上电进入」的正当实现，D0。
