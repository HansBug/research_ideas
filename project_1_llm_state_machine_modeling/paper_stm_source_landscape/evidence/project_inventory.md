# STM Source Landscape Project Inventory

## 1. Repository map

| 路径 | 作用 | 当前状态 |
|---|---|---|
| [`../`](../) | #85 paper workspace | 本 PR 新建 |
| [`../../sources/`](../../sources/) | 控制系统论文 corpus 与 STM 派生文件 | planning baseline：787 篇、746 正例案例 |
| [`../baselines/`](../baselines/) | #85 related-work / baseline 初筛与下载 handoff | 本 PR 新建 |
| [`../story/`](../story/) | paper story / claim-evidence / outline | 本 PR 新建 |
| [`../experiment_design/`](../experiment_design/) | RQ、execution gate、reviewer risk | 本 PR 新建 |

## 2. Evidence currently available

- `sources/SUMMARY.md` 给出 787 篇论文、746 正例案例、状态机类型 / 时间级别 / 结构标签等 planning baseline。
- issue #85 给出 G0--G10 hard gates、story、RQ/DQ、manuscript architecture。
- issue #95 给出 CCF-A/B 综述候选 438 行、87 篇自动解析全文结构统计、438 行全文下载审计。
- 本 PR 的 [../baselines/data/screening_audit.csv](../baselines/data/screening_audit.csv) 覆盖 #95 438 行候选，并标出 69 行 #85 初筛 slice。

## 3. Missing inputs before manuscript claims

1. Frozen manuscript snapshot commit 与统计复算脚本。
2. G1 retrospective protocol audit：`PROTOCOL.md`、`INCLUSION_TRACE.csv/jsonl`、flow。
3. G2 codebook reliability：blind/double-code、agreement/adjudication log。
4. P0/P1 人工全文下载与核验。
5. 7 条 `auto_fulltext_light_review_flag=yes` 候选的轻量方法节复查。
6. G0 copyright-safe release package 与 contamination check。
