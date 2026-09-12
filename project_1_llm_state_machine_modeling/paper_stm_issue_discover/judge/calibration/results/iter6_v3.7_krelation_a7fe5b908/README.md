# 迭代 6：v3.7 / prompt v11 + relation-first K 闭合实验（代码提交 `a7fe5b908`，2026-09-03 09:41–11:55）

本轮只改一处确定性派生：加 `--k-closure relation_first` 开关，让 validity 判为 D0 / NOT_A_DEFECT_CLAIM 的报告也进入 relation 阶段，任何正向台账关联（FULL 或 PARTIAL）把它闭合为 K；FALSE_POSITIVE 不进入。提示词、两读加仲裁、子集、gold、判据与迭代 4 相同。动机是用户对人工实践的描述：先判是否 hit，只对未命中的报告再分 N / I。原始制品在被忽略的 `runs/paper1/judge-calibration-a7fe5b908-krelation/`；provider 成本 current 三轮约 $5.8、baseline 三轮 $2.25。1 格失败（current r3 的 0047，机理见下）。

## 与事前登记判据的对照

| 判据 | current（迭代 5 → 6） | baseline（迭代 5 → 6） | 门槛 |
| :-- | :-- | :-- | :-- |
| P1 K/N/I 一致率 | 69.0% → **68.0%**（136/200） | 57.6% → **58.0%**（58/100） | ≥ 85% |
| P2 冻结 N、人工 I 层判 I | 67.3% → 58.6% | 36.0% → 36.0% | ≥ 80% |
| P3 冻结 I、人工有效层判有效 | 68.4% → 80.0%（16/20） | 75.0% → 75.0% | ≥ 75% |
| P4 K→K 保持 K | 65.5% → **86.2%**（25/29） | 73.3% → **86.7%**（13/15） | ≥ 95% |
| P5 五类 defect 一致率 | 46.7% → 46.5% | 53.5% → 45.0% | 信息性 |
| P6 方向偏差（有效率 judge − gold） | +12.7 → **+20.0 pp**（58.0% 对 38.0%） | +7.1 → +4.0 pp | ≤ 5 pp |

六轮同行趋势见 [../iterations_summary.md](../iterations_summary.md)（current 192 行、baseline 99 行）。v3.8 起 K 是 relation-first 闭合的输出，可以来自 D0 + FULL，P4 按类别 K 计。

## 全量加权：新 judge 首次追平冻结 judge

子集刻意偏向翻转层，所以还按各层在冻结全量里的份额加权（[scripts/population_weighted.py](../../scripts/population_weighted.py)，输出在 [current/population_weighted.md](./current/population_weighted.md) 与 [baseline/population_weighted.md](./baseline/population_weighted.md)）：

| 侧 | 全量 n | 冻结 v3.2 与 gold 一致 | 新 judge 加权估计 | 迭代 5 的估计 |
| :-- | --: | --: | --: | --: |
| current | 1271 | 80.6% | **80.3%** | 70.6% |
| baseline | 512 | 71.3% | **72.6%** | 66.4% |

投影到全量的 K/N/I：current gold 749/231/291，冻结 721/444/106，新 judge 689/303/279；baseline gold 312/105/95，冻结 276/134/102，新 judge 288/108/116。追平的来源全在 K→K 层：relation-first 让 D0 + 正向关联的报告留 K，两侧 K→K 从 65–73% 升到 86–88%，而该层占 current 全量 57%、baseline 54%。剩余偏差方向明确：current 少 60 个 K、多 72 个 N；baseline 少 24 个 K、多 21 个 I。

## FULL 与 PARTIAL 哪个该升 K

relation-first 实际改判的行很少，但方向可辨：

| 侧 | D0 / NADC + FULL → K | 其中 gold K | D0 / NADC + PARTIAL → K | 其中 gold K |
| :-- | --: | --: | --: | --: |
| current | 4 | 3 | 3 | 1 |
| baseline | 2 | 2 | 1 | 0 |

FULL 升 K 6 行对 5 行，PARTIAL 升 K 4 行对 1 行。把 PARTIAL 改回只记 support 的离线模拟：current 136 → 137，baseline 58 → 58。这与论文指标里 hit 只算 FULL 一致，v3.8 采用「D0 / NADC 只有 FULL 才升 K；D2 / D1 沿用 FULL 或 PARTIAL 都算 K」。

## 剩余分歧的结构（两侧合并读 reason / basis 之后）

1. **judge 过度有效化（current 36 行、baseline 16 行 gold I 被判 N）。** current 的 36 行里 D1 19、D2 17。逐条读 judge 理由后，D2 的 14 行（前两轮）里 8 行落在提示词已经写明为 D0 的情形而 judge 仍判缺陷：启动经 PoweredOff / Off 再由 start 进入工作态（0003 两轮、0012、0032、0052），事件名标签旁「缺独立守卫」（0044），初始边带守卫违反 UML 良构性（0016、0032，gold 判 NADC）。D1 的行几乎都写着「a second competent reading survives」且 judge 自己承认另一读法与源兼容——组合态行为由子态迁移实现（0005 两条）、NL 要求的动作写成标签文字（0016 r1）、事件名标签（0014 两条）。人工把「非缺陷读法至少同样忠实」判 D0。
2. **FALSE_POSITIVE 过度使用。** baseline judge 判 FP 11 次，gold 只有 2 条 FP，11 次里对 1 次，错的 10 条里 gold D2 5、D1 3；3 条还是 gold K，relation-first 不接纳 FP 所以直接丢 K。current 判 FP 25 次，其中 14 条 gold 为 NADC、3 条 D0（类别仍是 I，不伤 K/N/I），但 3 条 gold D2 被丢。gold 的判词给了判据：「the cited source fact is present, 所以是 D0 不是 A0」——人工锚定报告**引用位置上的事实**是否存在，judge 把复合报告里错误的框架陈述（区域计数、包含关系、「未声明」）当承重事实否决。
3. **relation 漏匹配。** judge 判有效但 NO_MATCH、gold 为 FULL / PARTIAL 的 K 行：current 7、baseline 4。逐条读 relation 理由：人工把同一根因的下游症状（0014 r1 issue 14：根初始缺失导致 InMotion 不可达，对台账的根初始缺失）、修法重合的同位置缺失（0045 / 0055：计时器与烹饪时间都是「模型里零变量零 effect」，台账正文虽把计时器划为界外，人工仍判 FULL）、同一区域独立性问题的不同迁移集（0037）都算 FULL 或 PARTIAL，而 v11 把「直接可归因症状」「修复消除或实质缓解」从 FULL 定义里删掉了。回看第三 → 第四轮（唯一只改 relation 的一次）：current 漏匹配 4 → 12（gold FULL 的 4 → 10），过匹配只 10 → 7，是净损失。
4. **D0 ↔ D1 的双向噪声。** baseline gold N 被判 I 的 11 行里 5 行是 judge D0 / gold D1，与上面 judge D1 / gold D0 的 8 行方向相反，且 gold_reason 显示两条人工轨道自身在这些行上分裂（A D1 / B D0）。同一类报告在 gold 里也跨 pair 不一致：NL 要求的数量减少写成标签文字，0056 r1 判 D1 / K（有 FULL 匹配），0016 r1 判 D0 / I（无匹配）；AutoFinal 嵌套与 Autonomous 的区分，current 0040 判 D0，baseline 0040 判 D1；三个区域建成子状态，0036 判 D0、0016 / 0047 判 D1 / K。人工的 D 层级实际上跟着 relation 走：有命中就留有效层，没命中的边界报告多落 D0 / I。这部分不可由提示词消除，是人工确认阶段的预期负载。

## 失败格 0047 的机理与修法

current r3 的 0047 是单报告 relation 批次（只有一条有效报告，三条预期）。模型六次都把回答拆成 item0 / item1 / item2、每个 item 对应一条预期且 report_id 相同；第一次还把 schema_version 写成原子响应的版本。后端只能报 item1 / item2 为多余输入，五次失败签名相同，属结构性死路（CLAUDE.md §10 / §12），不是采样。v3.8 加确定性归一化 `_merge_split_singleton_items`：单报告批次里多个 item 指向同一报告时，按 expected_id 合并 decisions、按批次预期顺序重排为一个 item0；同一 expected_id 出现互斥 match、出现别的报告 id 或缺预期位置时不合并、照常报错。配套测试 `test_singleton_relation_batch_split_per_expected_is_merged_into_item0`。迭代 5 的三格失败是同一族。

## 由本轮导出的 v3.8 / prompt v12

确定性派生：relation-first 成为默认闭合（`--k-closure validity_first` 保留 v3.2 顺序），D0 / NADC 只有 FULL 才升 K，PARTIAL 只记 support；单报告批次的按预期拆分 item 归一化合并。提示词九处：FALSE_POSITIVE 锚定引用位置上的事实；D1 要求缺陷读法至少与设计读法同样忠实；嵌套层实现、启动经 Off / Idle 再 start、事件名标签旁缺守卫、NL 动作写成标签或状态体文字、UML 记法良构性抱怨改为范畴式 D0；契约或预期记录的缺项归 NADC；relation 的 FULL / PARTIAL / NO 定义恢复 v10。每条规则都以通用建模原则表述，不含 pair、台账或臂标识（由 `test_prompts_carry_no_pair_ledger_or_arm_identifiers` 钉住）。第七轮实跑 v3.8 验证。
