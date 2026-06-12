# baselines/：相关工作与自动化对照入口

## 1. 定位

本目录复刻旧 Path-1 工作区中的 `baselines/` 层级，但在第二篇 agent-based SLR 论文中，baseline 不是 same-sample 模型生成实验，而是**方法学近邻、综述自动化工具和 LLM-assisted SLR 工作的对照空间**。

A0 阶段只维护对照范围、核验口径和总账，不下载 PDF，不生成逐篇深度综述，也不把尚未系统检索的 LLM-assisted SLR 工作写成已覆盖事实。

## 2. 文件说明

| 文件 | 作用 |
|---|---|
| [GUIDE.md](./GUIDE.md) | 规定后续新增自动化综述 / LLM-assisted SLR 对照条目的筛选、核验和写作口径。 |
| [SUMMARY.md](./SUMMARY.md) | A0 对照总账，记录已核验锚点、待 A1 补齐的近邻方向和禁止 claim。 |
| [papers/](./papers/) | 后续逐篇 method / tool 对照短评入口；A0 只保留目录，不强制填充。 |

## 3. 与其他目录的关系

1. 引用元数据优先回到 [../evidence/references.bib](../evidence/references.bib) 与 [../evidence/citation_seed_inventory.md](../evidence/citation_seed_inventory.md)。
2. 对照差异写作必须与 [../story/differential_novelty_matrix.md](../story/differential_novelty_matrix.md) 保持一致。
3. 任何强 novelty claim 必须先过 [../story/claim_evidence_map.md](../story/claim_evidence_map.md)。
