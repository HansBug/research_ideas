# #85 相关工作与基线初筛

本目录是 #85 状态机来源景观论文的相关工作 / 基线专项盘点入口。它对应 PR #96 中 `path1_foundation/baselines/` 的职责，但对象从 Path-1 直接基线变为 #85 的基准来源景观、LLM4MDE、MDE/MBSE/RE/CPS 映射近邻。

## 1. 文件职责

| 文件 / 目录 | 职责 |
|---|---|
| [GUIDE.md](./GUIDE.md) | D1--D7 字段合同、证据等级、升级/降级规则、审查门禁 |
| [SUMMARY.md](./SUMMARY.md) | 69 行 #85 初筛矩阵总账；逐行 D1--D7 初筛真源 |
| [DOWNLOAD_AUDIT.md](./DOWNLOAD_AUDIT.md) | #95 下载 / 自动解析事实与本 PR 获取边界 |
| [MANUAL_DOWNLOAD_REQUESTS.md](./MANUAL_DOWNLOAD_REQUESTS.md) | 25 条 P0/P1 用户人工下载队列 |
| [EXCLUDED_CANDIDATES_SUMMARY.md](./EXCLUDED_CANDIDATES_SUMMARY.md) | 未进入主矩阵或暂缓候选的排除理由与复查门禁 |
| [data/](./data/) | 机器可审计 CSV、输入快照、BibTeX 交接、定向检索审计 |

## 2. 当前状态

- #95 输入候选：438 行。
- #85 初筛子集：69 行。
- P0/P1 人工下载：25 条。
- `auto_fulltext_light_review_flag=yes`：7 条，复查前不得最终排除。
