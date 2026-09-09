# C2 Sonnet5 15-pair 对照

本目录保存 2026-09-08 完成的 C2 局部对照和此前 raw-inspect-direct stress 原型的 compact 归档。结果只用于解释当前 A2 的 Sonnet5 行为，不替代 E2 的 54 pair x 3 round 全量结果，也不构成总体泛化结论。

## 实验身份

- 15-pair 集合：`0000, 0002, 0004, 0005, 0007, 0009, 0010, 0014, 0015, 0019, 0024, 0029, 0033, 0034, 0054`。
- method：`claude-sonnet-5`；judge：`gpt-5.6-luna`。
- 每个条件使用同一集合的 round-1 输出；四个 method arm 的发布报告组成匿名 union，由同一 Luna v3.11 闭包裁定。
- A2 是当前分支 `--ablation no-predicates`，谓词回执为 0；full 和 baseline 控制格从 pane9 对应的 E2 Sonnet 全量归档复制并校验 hash。
- `broad_contemporary` 是扩大删除条件（full-removal）：删除类型化义务、义务驱动 frontier 和 predicate 机制，保留 C1 模型分析/inspect 和普通自然语言 discovery lenses。

## 结果

| 条件 | reports | valid / invalid | precision | strict precision | FULL hit |
|---|---:|---:|---:|---:|---:|
| full ours | 114 | 108 / 6 | 94.74% | 82.46% | 43/69 (62.32%) |
| baseline | 89 | 71 / 18 | 79.78% | 55.06% | 38/69 (55.07%) |
| A2 no-predicates | 126 | 109 / 17 | 86.51% | 73.02% | 45/69 (65.22%) |
| full-removal / broad | 62 | 54 / 8 | 87.10% | 75.81% | 33/69 (47.83%) |

full 相对 A2 的 precision 差为 `+8.23 pp`，但 A2 多命中 2 个 FULL ledger issue；full 相对 full-removal 的 precision 差为 `+7.64 pp`，同时多命中 10 个。该 15-pair 试验显示了 coverage/precision 取舍，没有证实谓词体系提高 precision。

此前的 raw-inspect-direct stress 原型不是同一集合，只有 12 pair，结果为 full ours `66 reports, 52/14, precision 78.79%, strict 62.12%, FULL 17/30`，raw direct `19 reports, 9/10, precision 47.37%, strict 42.11%, FULL 9/30`。它说明完整结构化链在该定向样本上有明显差异，但只能作为 stress-set 原型。

## 证据文件

- [protocol.json](./protocol.json)：pair、profile、method 定义、judge 协议、输入和限制。
- [audit.json](./audit.json)：Sonnet/Luna usage、调用状态、恢复记录和 provider-free 审计结论。
- [derived/analysis.json](./derived/analysis.json)：四臂逐 pair 和总体裁定、报告、hit 与 precision。
- [derived/paired_sensitivity.json](./derived/paired_sensitivity.json)：按 NL cluster 的探索性区间。
- [derived/mechanisms.json](./derived/mechanisms.json)：谓词关闭和候选发布边界的逐格检查。
- [stress_raw_inspect_direct/analysis.json](./stress_raw_inspect_direct/analysis.json)：12-pair raw-inspect-direct stress 原型。
- [scripts/](./scripts/)：生成/分析/审计脚本快照；provider 原始 wire 和大体量 `llm/` 目录仍位于 `/tmp/c2-sonnet-replication-20260908/` 与 `/tmp/c2-sonnet-targeted-stress-20260908/`，对应 hash 见各 `audit.json`。

离线复算（不调用 provider）：

```bash
python final_results/c2_sonnet15_20260909/scripts/c2_sonnet_replication.py analyze
python final_results/c2_sonnet15_20260909/scripts/audit.py
```

