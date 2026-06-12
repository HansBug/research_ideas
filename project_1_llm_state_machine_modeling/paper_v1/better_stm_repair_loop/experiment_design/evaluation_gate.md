# Evaluation Gate Principles

## 1. 本文件不是什么

本文件不是 PR-R4 的评价门 v0，也不定义最终 metric threshold、场景 fixture、人工量表终稿或主实验统计表。它只在 R0 阶段冻结**评价门必须早于真实修正预演**这一顺序原则，避免后续用 R5 预演结果反向污染指标设计。

## 2. 顺序原则

1. R1 先盘点 baseline / prior artifact / code / demo / output format / license / convertibility。
2. R2 再冻结 seed registry 和同一组四例样本。
3. R3 定义最小转换合同和转换归因台账。
4. R4 在真实修正预演前冻结 diagnostics、scenario suite、regression suite、五条件、评价量表草案、主结果纳入规则、指标骨架和统计表结构。
5. R5 才运行无人化修正循环预演。
6. R6 继承 R4 的指标骨架和统计表结构，冻结主实验协议、对照矩阵和降级写法。

## 3. 必须进入评价门的失败模式

| 失败模式 | 后续处理 |
|---|---|
| schema-invalid / parse-invalid | 可写盘审计，但不得进入主结果成功统计。 |
| 新增 blocking diagnostics | 候选拒绝或回滚。 |
| scenario regression | 候选拒绝或降级记录。 |
| NL-grounded semantic drift | 即使其他指标改善，也不得计为 Better STM。 |
| oscillation / timeout / non-convergence | 作为失败模式统计。 |
| provider failure / partial run | 进入 eligibility / exclusion ledger。 |
| manual normalization | 与自动修正结果分开记录。 |

## 4. 对照 / 消融最低集合

R6 至少应处理：

1. 无修正 seed：`STM_0` 直接作为 baseline。
2. 从 `NL` 重新生成：比较 regenerate route 与 repair route。
3. 无结构化反馈自修正：衡量 diagnostics / scenario feedback 的边际作用。
4. 可运行修正 / refinement 近似基线：若 prior artifact 可运行，则纳入；不可运行则记录为 evidence-only。
5. 转换感知分析：区分 converter normalization 与 repair-loop improvement。

## 5. R0 自检

R0 文档中不得写：

- 已经提升质量；
- 已经优于 baseline；
- 已经有最终 metric；
- 已经完成四例真实运行；
- 已经完成主实验评价门。
