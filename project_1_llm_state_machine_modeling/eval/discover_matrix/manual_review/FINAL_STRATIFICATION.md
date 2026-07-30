# 最终分层：可入 expected issue = 130 条（点值）

Issue [#171](https://github.com/HansBug/research_ideas/issues/171) 裁决点 1 问「154 条候选如何入账」。词法分层只能给出区间 **66 – 144**，因为 `nl_named` 层的判据是「理由里提到 NL」，而那不等于「NL 点名了缺失的那个元素」。本轮把全部需要人工的行逐条判完，**收敛到点值**。

| | 数 |
| --- | ---: |
| 计入问题（基线，主档口径） | 154 |
| **可入 expected issue** | **130** |
| 已审阅但搁置（断言给不出正面判定） | 1 |
| 明确不可入 | 23 |
| 分布 case 数 | 48 |
| **落在台帐无 E1 的 case 上**（裁决点 2 的补录增量） | **30** |

逐行数据：[final_stratification.json](./final_stratification.json)。各批复核原始判定：[nl_review/](./nl_review/)。生成脚本：[../merge_manual_stratification.py](../merge_manual_stratification.py)（24 个测试）。

## 分层结果

| 层 | 条数 | 可入 | 判据 |
| --- | ---: | :-: | --- |
| `nl_named` | 70 | ✓ | NL 点名了那个缺失或错位的元素 |
| `wellformedness` | 36 | ✓ | 无需 oracle，仅凭生成模型自身即可判定 |
| `nl_contradiction` | 13 | ✓ | 与 NL 的显式义务矛盾 |
| `over_specification` | 11 | ✓ | 生成方凭空多出**且**造成可断言的负面后果 |
| `over_specification_benign` | 18 | ✗ | 生成方多出但写不出后果 |
| `reference_only` | 3 | ✗ | 只在参考、NL 未点名——不可归因于生成方 |
| `over_specification_duplicate` | 1 | ✗ | 后果已被同 pair 的另一条承载，计入会双算 |
| `out_of_scope_concurrency` | 1 | ✗ | 主裁定移出范围，见 [nl_review/parent_rulings.json](./nl_review/parent_rulings.json) |
| `uncertain_stratum` | 1 | ✗ | 已审阅但搁置 |

## 复核怎么做的

**四批 NL 复核**（89 条 `nl_named`，按 NL 组分工，每批先把该组 NL 逐句编号再逐条判）：

| 批次 | 条数 | 结果 |
| --- | ---: | --- |
| NL01 + NL08 | 23 | 23 可入，`reference_only` = 0——上界在这两组上是紧的 |
| NL04 + NL10 | 25 | 24 可入 + 1 待有害性判定 |
| NL03 + NL06 | 22 | 15 可入、**7 掉出** |
| NL05 + NL07 + NL09 | 19 | 17 可入；**9 条错分中 7 条从上界层移进下界层** |

**`extra` 有害性判定**（31 条，每条实跑谓词、每条 harmful 附 pinned control）：12 harmful / 18 benign / 1 搁置，其中 2 条与同 pair 的 `problem` 重复。

**批 5**（12 条从未经人工判定的行 + 16 条抽验）：`reference_only` 层查出 **50% 假阴性**（6 条里 3 条误判）；抽验 16 条中 3 条不同意。

## 与预期相反的结果

我原以为复核会**拉低上界**（`nl_named` 里混着不可归因的）。实际两个方向都有，且**下界被推高得更多**：

- **NL05/07/09 批的 9 条错分里有 7 条从 `nl_named` 移进下界层**（3 → `wellformedness`、4 → `nl_contradiction`）。最干净的一例：`0019`#1 / `0029`#1 的理由先引 NL 3，再补了一条 NL 从未陈述的**建模规范**「两个目标互斥、模型必须给出可区分依据」——NL 3 只给了**一个**合并条件覆盖**两个**目标。审阅者自己那句「参考侧靠 cruise 无守卫消歧」就承认了消歧来自参考。它靠更强的理由活下来：同事件、都无守卫、两个目标，仅凭模型自身可判。
- **`reference_only` 层也被高估**：6 条里 3 条误判。`0005`#3 的理由开头是「NL 第 5/6/7/8 句**显式要求**」，触发词「参考独有」来自原句「**不是**参考独有细化」——词法判据把否定读成了肯定。

## 词法判据的三处失效（都有实例）

| 失效 | 实例 |
| --- | --- |
| **命中词出现在否定句里** | 5 条的命中词是理由中的 "NL06"，而那句话写的是「NL06 全文**没有**命名任何触发事件」——NL 沉默，语义与判据恰好相反 |
| **同一词法在两个 verdict 上意义相反** | 「NL 未要求」在 `problem` 上是「参考有、生成方缺」（不可归因），在 `extra` 上是「生成方凭空造」（完全可归因）。首版把 `0049`#4 与 `0056`#3 两条 `extra` 判成不可归因 |
| **同一发现被分到不同层** | `0039`#1 与 `0059`#1 都是「删了 `enter_hwy --> lane_change`」，前者因触发词「参考自身」被判不可入 |

## 主裁定 1 条

`0013`#1 移出范围（`out_of_scope: concurrency`），"计入问题"因此从 154 降为 **153**（按边界规范重判后的口径则从 157 降为 156）。三条独立证据：

1. **与参考共有**：参考（`Dataset.xlsx` 行 57）同样是三个 `--` 正交区各一条 `[*] -->`，所以「三条初始边导致默认进入点不唯一」参考侧也成立，不可归因于生成方。
2. **只在展平后成立**：该缺陷是 FCSTM 把正交区展平成单一状态体后才出现的表象，属正交并发语义，落在 project_1 的问题定义边界外。
3. **断言不可评估**：实测 `initial_target(PumpControl, PumpState)` 返回 **None**（不是 False），该行拿不出可评估的正面断言，而它标了 `predicate_exists=True`。

唯一 gen-only 的残留是行首多余 `--` 造出的空区域 0——无状态、无迁移、无后果。克隆件造成的七个具名状态问题由 `0013`#0 单独承载，不因本条降级而丢失。

⚠️ 这条与 [RESCOPE.md](./RESCOPE.md) 那轮的反向检查冲突（它报「0 条需补 tag」，漏了这条），以本裁定为准。

## 另一条主裁定：拒绝一个被提出的判据

`0044`#1 的复核报告称其断言在 `cycles>=2` 时为 `False`。**实测是 `None`**：

```
occupancy_after(Cruising, Arrived_at_Destination, Stopping, cycles=2) -> None
terminates(scope='InMotion.Stopping')                                 -> None
reaches(Stopping -> [*], 3)                                           -> None
terminates(scope='[*]')                                               -> True
```

`None` 表示无法判定，**不能当 False 用作缺陷证据**；而 `terminates(scope='[*]') = True` 说明整机能终止，那两条无触发完成边并未造成死锁。故降为搁置（不是 benign——无触发完成边本身是良构性可疑形状，只是当前 19 谓词面给不出 False）。

## `extra` 的判据：可归因 ∧ 有害

复核中曾提出 `extra` 的归属取决于对 NL 采**开世界**还是**闭世界**读法。两者都不采纳，理由见 [nl_review/EXTRA_POLICY.md](./nl_review/EXTRA_POLICY.md)：闭世界与原论文「需求模板禁止写元素个数与关系」直接冲突（NL 在设计上不穷举）；开世界会把 `0007`#3 那种「整棵子树无入边的死代码」也放过。

改用**可归因 ∧ 有害**：`extra` 的可归因性无争议（来源唯一），要判的是**是否造成可断言的负面后果**。存在性断言（`state_declared` / `edge_declared`）只证明「造了它」——对 `extra` 那是前提不是缺陷。这个判据**与 NL 的世界假设无关**，只依赖模型自身可判定的后果，与 `wellformedness` 同源。

18 条 benign 的理由值得单独看（它们决定哪些被划掉），三种模式：

- **谓词非判别**：`stays_in` 要求触发被消费，所以正确模型（没有该事件）也返回 False——五条 NL02 钳夹类 extra 全属此类。
- **被同 pair 的 sibling 遮蔽，且有负控**：`0032`#3 的 `AcceleratingState` 不可达，**但 `IdleState` 与 `BrakingState` 也不可达**——系统性，来自 `0032`#1 的缺失 `[*]`。`0043`#2 的 `Region2` 不可达，**但 `Region1` 也不可达**，入口是 converter 的 `UnspecifiedInitial`（在该 pair 的 `attribution_exclusions` 里）。
- **API 主动拒答**：`0006`#4 的 `occupancy_after(..., within_cycles=1)` 抛 `UnsupportedEvidence` 并提示改用 `within_cycles=2`（那里为 True）——`predicate_api.py` 把这个形状点名为**不应发布为 bounded artifact** 的形状。

## 尚未做完的两件事

1. **`nl_contradiction` 层需一次定向复核**（13 行）。抽验显示该层的两个失效模式是：被引的 NL 句落在并发/时间 scope 外（`0047`#0 中招，已改判 `wellformedness`）、以及闭枚举读法被 "three **main** substates" 的 "main" 削弱（`0002`#2、`0043`#0 有此保留）。16 行抽验里**没有一行**属于「只是与参考不一致」。
2. **`wellformedness` 层有两个廉价筛可替代全量重判**：(a) gen puml 含 `--` 且缺陷事实是「多条初始边 / 区域数量 / 区域为空」的 7 行（`0002`#1 `0007`#1 `0007`#2 `0013`#1 `0027`#1 `0036`#1 `0043`#1）——逐行核对该事实是否与参考共有、是否只在展平后成立（`0013`#1 正是这样被抓出来的）；(b) trigger 是行为描述而非目录词的行。目录内的入口类 trigger 本次 6/6 全对。

## 9 条 assertable 需重新实例化（不改计数）

复核发现 9 条的 `assertable` 是纯存在性或 `None` 而实际有后果，修正形式在 [nl_review/extra_harm.json](./nl_review/extra_harm.json) 的 `corrections_to_reviewer_assertable_fields`。另有三处落点问题：`0018`#2 过读了 NL 第 11 句（那句说 containment 不是迁移）、timer-effect 五条的分母混入 2 条 NL 无对应表述的参考边、`0048`#4 实例化在最弱的 `choice1` 上（NL 从未描述它的分支）、`0029`#0 用了 NL 从未陈述的 `containment(AutonomousMode, HighwayMode)`（NL 点名的是 `InitialState`）。

## 一个方法学结论

**`initial_target` 看不到带触发的初始边。** `_initial_child_of` 从单一入口作答即使该入口带触发，所以 `initial_target(root, TurnOn)` 在 `0018` 上返回 True——**正向放过了一个有缺陷的模型**。该族的可用形式是 `event_consumed(source='[*]', ...)`，负控：`0021`（无触发根 `[*]`）返回 True，所以不是恒 False。这是 Issue #171 §7.2 缺口一的实证。
