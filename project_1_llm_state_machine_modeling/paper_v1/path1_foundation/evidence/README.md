# evidence/：证据资产与相关工作入口

本目录维护第一篇 Path-1 paper 的仓库证据索引和 baseline / related-work 对齐矩阵。它负责回答“哪些已有材料可以支撑论文，哪些仍只是候选或计划”。

## 文件说明

| 文件 | 作用 |
|---|---|
| [project_inventory.md](./project_inventory.md) | 盘点 method、eval、baselines、sources、talks、runs 和当前 foundation 的证据资产与缺口。 |
| [baseline_and_related_work_matrix.md](./baseline_and_related_work_matrix.md) | 将已读 baseline / related work 压缩为 direct / near / evidence-only / background，并给出后续可执行 baseline contract。 |

## 使用顺序

1. 做 paper planning 或写 related work 前，先读 [project_inventory.md](./project_inventory.md)。
2. 选择 baseline 或设计实验对照前，读 [baseline_and_related_work_matrix.md](./baseline_and_related_work_matrix.md)。
3. 如果要新增 related work claim，必须回到对应 baseline 单篇目录核验 `bibtex.bib` / `DESC.md` / 原文提取物。

## 学术约束

- 本目录只登记证据和计划，不提供新实验数字。
- baseline 可复现程度必须如实标注；不可复现工作只能作为 evidence-only comparison 或 related work。
- 不能用“artifact 不可用”直接贬低 prior work；应说明输出表示、输入上下文、任务设定或复现条件不匹配。
