# 事前登记：Judge v3.4 校准（2026-09-03）

本文件在任何一次 v3.4 真实运行之前提交并推送。它登记子集、判据、红旗与迭代政策；运行后的数字只进 `results/`，不改本文件（若确需改判据，另起一节注明日期与理由，不覆盖原文）。

## 子集

由 [scripts/build_calibration_subset.py](./scripts/build_calibration_subset.py) 以 seed 20260903 从冻结归档抽取，见 [subset_v1/summary.md](./subset_v1/summary.md)：

| 侧 | 报告数 | pair 数 | 翻转层（冻结 Judge 类别 ≠ 人工终态） | 稳定层 |
| :-- | --: | --: | --: | --: |
| current | 201 | 49 | 147（N→I 111、N→K 15、I→K 8、I→N 12、K→I 1） | 54（K→K 30、N→N 12、I→I 12） |
| baseline | 100 | 45 | 70（N→I 25、N→K 4、I→K 20、I→N 21） | 30（K→K 15、N→N 8、I→I 7） |

gold 为 current v4 决策表与 baseline v3 组合表（`canonical_class` / `corrected_kni`、`d_tier`、`a0_subtype`/`a0_type`、relation）。baseline 的 K→K 层来自未重审的冻结 v2 K，只检验「仍为 K」。

## 模型与运行方式

- 模型 profile：`gpt-5.6-luna`（与冻结实跑一致）；每侧每轮一次 CLI 调用，`--report-filter` 限定到子集。
- 两次独立 validity 读数 + 仲裁，两次 relation 读数 + 仲裁，与冻结实跑相同的批量与拆分策略。
- 判定口径以 `report_outcomes.validity` 与 `defect_class` 为准；relation 以 `full/partial_ledger_ids` 为准。

## 验收判据（趋势一致，允许抖动）

| # | 判据 | 门槛 | 性质 |
| :-- | :-- | :-- | :-- |
| P1 | 每侧 K/N/I 与 gold 的逐条一致率 | ≥ 85% | 必须 |
| P2 | 冻结 N、人工 I 的层（current `N->I/*`、baseline `N->I`）被判 I 的比例 | ≥ 80% | 必须 |
| P3 | 冻结 I、人工有效的层（`I->K`、`I->N`）被判 K 或 N 的比例 | ≥ 75% | 必须 |
| P4 | `K->K` 层仍为 K（VALID 且至少一条 FULL/PARTIAL） | ≥ 95% | 必须 |
| P5 | 五类 defect_class 逐条一致率；D2↔D1 混淆单独列出 | ≥ 70%（信息性） | 报告 |
| P6 | 方向偏差：每侧「新 Judge 有效率 − gold 有效率」 | 绝对值 ≤ 5 pp | 必须 |

对照基准：同一批行上冻结 v3.2 Judge 的一致率（current 约 27%，baseline 约 30%，因子集刻意偏向翻转层）。

## 红旗（任一出现即在 `results/` 中显式记录并解释）

1. 任一分层上新 Judge 比冻结 Judge 更差。
2. 分歧高度集中于单一 pair（该 pair 占分歧 ≥ 40%）。
3. baseline 报告被判 `A0_NOT_A_DEFECT_CLAIM`（结构性规则不应命中自由文本基线；出现即逐条核对）。
4. 任一 pair 失败落盘（`failures/`）或子集覆盖不足 100%。
5. 仲裁比例 > 30%，提示读数不稳定。

## 迭代政策

- 迭代之间只改提示词 / schema 描述 / 确定性派生，不改子集、gold 或判据；每次迭代新 run-id，全部迭代的 `summary.md` 与 `disagreements.md` 都留在 `results/` 下，不挑选。
- 每次迭代必须先 commit + push 再运行（CLI 也强制干净树）。
- 提示词中禁止出现 pair 编号、台账 ID、臂名称或任何针对单条报告的措辞；每条新增规则须能以通用建模原则表述，由 `test_prompts_carry_no_pair_ledger_or_arm_identifiers` 钉住。
- 接受条件：P1–P4 与 P6 同时满足；P5 只报告。达标后停止调优，剩余分歧作为人工确认阶段的预期负载写入结果说明。

## 效率合格线（2026-09-03 第八轮起追加）

质量判据 P1–P6 不变且仍是首要门；以下效率指标由 [scripts/efficiency_report.py](./scripts/efficiency_report.py) 从调用回执算出，合格即可，不以效率换质量。基线取第七轮（v3.8 / prompt v12，`8313a632f`）实测：301 条报告、814 次调用、每条报告 2.70 次调用、19.0 万输入 token、$0.0315、两侧串行三轮共 93 分钟。

| 指标 | 第七轮实测 | 合格线 |
| :-- | --: | --: |
| 每条报告计费成本 | $0.0315 | ≤ $0.0158（一半） |
| 每条报告输入 token | 19.0 万 | ≤ 6 万 |
| 每条报告请求数 | 2.70 | ≤ 2.0 |
| 一侧三轮墙钟（三轮并行启动） | 28–38 分钟 × 3 串行 | ≤ 40 分钟 |
| 失败格 | 0 | 0 |

第八轮起同一提示词跑两个臂：A 臂沿用全部闭包与全量仲裁触发（质量参照）；B 臂只向模型展示作者源角色（NL、PlantUML、reference_inspection、exact_source_inventory；审计输入与 closure_hash 保留全部制品）并只在 core truth、defect class 或门不一致时仲裁。**采纳 B 臂的条件**：两侧 P1 与 A 臂的差在 ±3 pp 内，K→K 层相差不超过 2 行，全量加权一致率不低于 A 臂超过 2 pp，且效率合格线全部满足；否则采纳 A 臂并单独拆解 B 臂的两项改动。两臂都用同一子集、同一 gold、同一判据，不因效率放宽任何质量判据。
