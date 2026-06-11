# #85 Related Work / Baseline Screening

本目录是 #85 STM source landscape paper 的 related-work / baseline 专项盘点入口。它对应 PR #96 中 `path1_foundation/baselines/` 的职责，但对象从 Path-1 direct baselines 变为 #85 的 benchmark-source landscape / LLM4MDE / MDE/MBSE/RE/CPS mapping 近邻。

## 1. 文件职责

| 文件 / 目录 | 职责 |
|---|---|
| [GUIDE.md](./GUIDE.md) | D1--D7 字段合同、证据等级、升级/降级规则、review gate |
| [SUMMARY.md](./SUMMARY.md) | 69 行 #85 初筛矩阵总账；row-level D1--D7 初筛真源 |
| [DOWNLOAD_AUDIT.md](./DOWNLOAD_AUDIT.md) | #95 下载/自动解析事实与本 PR 获取边界 |
| [MANUAL_DOWNLOAD_REQUESTS.md](./MANUAL_DOWNLOAD_REQUESTS.md) | 25 条 P0/P1 用户人工下载队列 |
| [EXCLUDED_CANDIDATES_SUMMARY.md](./EXCLUDED_CANDIDATES_SUMMARY.md) | 未进入主矩阵或暂 Skip 候选的排除 reason 与复查 gate |
| [data/](./data/) | 机器可审计 CSV、input snapshot、BibTeX handoff、targeted search audit |

## 2. 当前状态

- #95 输入候选：438 行。
- #85 初筛 slice：69 行。
- P0/P1 人工下载：25 条。
- `auto_fulltext_light_review_flag=yes`：7 条，复查前不得最终排除。
