# #85 相关工作与基线初筛

本目录是 #85 状态机来源景观论文的相关工作 / 基线专项盘点入口。它对应 PR #96 论文工作区中 `baselines/` 层的职责，但对象从 Path-1 直接基线变为 #85 的基准来源景观、LLM4MDE、MDE/MBSE/RE/CPS 映射近邻。

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
- 自动全文轻量复查标记为 `yes`：7 条，复查前不得最终排除。
- 定向直接近邻起点审计：19 条，包含命中、零命中与访问受限记录；后续 G3 仍需补全人工 / 带凭证检索。
- 438 行全量审计中，只有进入 69 行矩阵的候选要求完整 D1--D7 证据字段；未入选行保留筛选结论和排除理由。

## 3. 人工下载与核验闭环

P0/P1 不只保留 BibTeX；[MANUAL_DOWNLOAD_REQUESTS.md](./MANUAL_DOWNLOAD_REQUESTS.md) 还维护 request-level ledger，用于记录 `request_id`、访问路线、阻塞 gate、用户响应、人工核验状态、最终验证状态和版权提示。后续全文核验必须同步更新该 ledger 与机器矩阵。
