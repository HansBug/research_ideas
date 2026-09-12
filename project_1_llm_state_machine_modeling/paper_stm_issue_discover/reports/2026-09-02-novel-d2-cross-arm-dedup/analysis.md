# 台账外 D2 发现的跨轮与跨臂去重分析（2026-09-02）

本目录保存 [story/paper_outline.md](../../story/paper_outline.md) §5.4 与 §6.2 引用的「台账外 D2」数字的原始数据与分析。它只读取 [v60/current 与 X1v2 baseline 最终归档](../../final_results/v60_current_vs_x1v2_baseline/README.md) v4 层的人工裁定与人工分组，不修改归档，不重跑方法、基线或人工裁定。

## 数据来源与口径

1. 台账外有效报告（`VALID_NOVEL`，K/N/I 中的 N）取自 `derived/manual_adjudication_v4_current_reaudit/current_report_decisions_v4.json`（方法）与 `derived/manual_adjudication_v3_baseline_ni/baseline_report_decisions_v3.json`（基线）；D 档取报告的人工 `d_tier`。
2. 跨轮归并沿用归档中已完成的人工分组（同侧、同对、同义务、同源位置、同根因、同最小修复意图；`current_n_groups_v4.json` 与 `baseline_n_groups_v3.json`）。本分析只取**至少含一条 D2 报告**的组；实际两侧的 D2 组均全部由 D2 报告构成。
3. 跨臂匹配只在两臂都有 D2 组的输入对上进行（`0006`、`0036`、`0057`），判据与臂内分组相同；由 agent 单轮判读并回读该对的 `nl.txt` 与 `plantuml.puml`。⚠️ 这是 agent 判读，不是人工裁定，结论待人工确认。
4. 问题类型与 L 档为分析性归类：类型取闭合集合；L 按论文 §2.2 的定义由义务与根因文本判定，与哪一臂发现无关。同为 agent 单轮判读。

## 结果

| 项目 | 方法 | 基线 |
| --- | ---: | ---: |
| 台账外 D2 报告 | 38 | 50 |
| 跨轮归并后的 D2 组 | 21 | 48 |
| 有 D2 组的输入对 | 7 | 17 |

两臂共享的输入对只有 3 个。跨臂匹配：2 对判为同一问题（`0036` 顶层初始入口断裂；`0057` CA 复合态缺正交分隔），4 对存疑——存疑全部来自方法臂按义务拆组（同一根入口断裂拆成可达性、事件消费者覆盖、触发集合三组）而基线一次陈述的粒度差。并集：严格读法（存疑记异）**67** 组，宽松读法（存疑记同）**63** 组。相对台账中的 98 条 D2，台账外 D2 处于同一量级的下方。

**跨臂匹配表**

| 方法组 | 基线组 | 对 | 判定 | 依据（摘） |
| --- | --- | --- | --- | --- |
| `v60_current:0036:0036|reachability|scope-region1|the-require` | `N-G-0036-S-0036-r1-baseline_issue_3` | 0036 | SAME_ISSUE | Same obligation (regions must be reachable from the model root), same author-source locus (top-level `[*] --> InitialSta |
| `v60_current:0057:0057|region_structure|composite-ca-orthogon` | `N-G-0057-01` | 0057 | SAME_ISSUE | Same obligation (NL3: the active mode of Collision Avoidance must use orthogonal regions permitting concurrent activatio |
| `v60_current:0036:0036|event_consumer_coverage|scope-region1|` | `N-G-0036-S-0036-r1-baseline_issue_3` | 0036 | UNSURE | Root cause and minimal repair are identical to the SAME_ISSUE row (severed top-level entry -> wire it); only the stated  |
| `v60_current:0036:0036|event_consumer_coverage|event-intercep` | `N-G-0036-S-0036-r1-baseline_issue_3` | 0036 | UNSURE | Same as above; the baseline text explicitly names TargetSearch and FormationAdjustment as unreachable, which are exactly |
| `v60_current:0036:0036|trigger_set|transition-flight-attack-s` | `N-G-0036-S-0036-r1-baseline_issue_3` | 0036 | UNSURE | Same as above; the baseline text explicitly names AttackReady and Attack as unreachable, which is exactly the method cla |
| `v60_current:0057:0057|cardinality|composite-ca|the-nl-explic` | `N-G-0057-01` | 0057 | UNSURE | Same locus (CA), same root cause (three ordinary sibling composites, zero declared regions) and same repair (introduce t |

**按类型（组数）**

| issue_type | 方法 | 基线 |
| --- | ---: | ---: |
| `reachability_or_entry` | 4 | 6 |
| `event_consumer_coverage` | 4 | 0 |
| `region_or_concurrency_structure` | 1 | 3 |
| `hierarchy_or_containment` | 0 | 1 |
| `trigger_or_guard_slot` | 2 | 12 |
| `state_action_or_lifecycle` | 9 | 9 |
| `cardinality_or_count` | 1 | 1 |
| `termination_or_dead_end` | 0 | 14 |
| `other` | 0 | 2 |

**按 L（组数）**

| L | 方法 | 基线 |
| --- | ---: | ---: |
| L0 | 2 | 8 |
| L1 | 11 | 24 |
| L2 | 8 | 16 |

## 读法与限制

1. 两臂的 L 分布接近（L2 占比 8/21 对 16/48）。类型上方法独有事件消费者覆盖（4:0），基线独有终止/死端（0:14）与触发/守卫槽位（2:12）。
2. ⚠️ 基线的 14 条终止/死端类里 12 条集中在 `0049`、`0059` 两个输入对，方法在这两对没有任何台账外 D2 组；这一差异含输入对组成差异，不能读成能力差，比率不可直接跨臂比。
3. 跨臂去重的粒度（义务层还是源级缺陷层）决定并集是 67 还是 63，需人工裁定。
4. 本分析不进入 hit、precision 或 W 的任何主指标；它只服务于 §5.4「台账是参考而非全集」的量级陈述。

## 文件

| 文件 | 内容 |
| --- | --- |
| [novel_d2_groups_input.json](./novel_d2_groups_input.json) | 两臂含 D2 的 N 组（69 组）：成员报告、D 档、义务、根因、源位置、报告文本摘录 |
| [cross_arm_matching_and_classification.json](./cross_arm_matching_and_classification.json) | 跨臂匹配（2 同一 + 4 存疑）、并集规则、69 组逐条的类型与 L 归类及依据、汇总计数 |
