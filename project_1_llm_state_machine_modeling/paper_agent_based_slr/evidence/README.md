# evidence/：证据资产、事实漂移与引用入口

本目录维护第二篇智能体辅助 SLR 论文的证据资产总账。当前 S0/A1 阶段，它只登记证据层级、可复用入口和 A1 资产边界，不复制 PR #97 的全文文库，也不构造最终 benchmark 场景。

## 文件说明

| 文件 | 作用 |
|---|---|
| [project_inventory.md](./project_inventory.md) | 盘点 `main` 已合入事实、PR #97 快照、历史评论、待构造证据和资产角色。 |
| [a1_asset_inventory.md](./a1_asset_inventory.md) | PR-A1 专用资产登记：资产层级、公开性、允许 / 禁止用途、统计资格、漂移触发和 A2/A3/A5a 交接。 |
| [fact_drift_policy.md](./fact_drift_policy.md) | 规定 `main` 事实、PR #97 快照、历史评论、待构造证据的引用格式、复核触发和漂移处理规则。 |
| [citation_seed_inventory.md](./citation_seed_inventory.md) | 维护 S0/A1 相关工作 citation seed、核验状态与来源优先级。 |
| [references.bib](./references.bib) | 保存已通过 DOI / 出版页元数据核验的 BibTeX 种子；完整 references 仍由 A1 / 写作 PR 继续扩展。 |

## 使用规则

1. 引用 PR #97 前必须先读 [fact_drift_policy.md](./fact_drift_policy.md)。
2. [project_inventory.md](./project_inventory.md) 只登记资产角色，不把未合入资产升级成事实真源。
3. [citation_seed_inventory.md](./citation_seed_inventory.md) 中 `待核验` 的条目不能用于正文强主张。
4. 已核验 BibTeX 种子集中放在 [references.bib](./references.bib)；若后续使用正文引用，仍需结合原文阅读和 Related Work 写作上下文复核。
5. 若后续 PR #97 merge 或 head SHA 变化，必须同步更新本目录。
