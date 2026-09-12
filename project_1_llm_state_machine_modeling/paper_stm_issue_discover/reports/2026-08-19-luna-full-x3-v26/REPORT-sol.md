# 全量 x3 独立语义审计报告

本报告比较 gpt-5.6-luna 下的新方法 v26-dnorm 与 X1v2 baseline，运行矩阵为 54 个非 NL04 pair、每臂每 pair 三轮；命中由独立 gpt-5.6-sol 语义评审依据同一位置与同一性质判定，不使用关键词、字符串包含、编辑距离、embedding 或其他词法捷径。

## 方法侧覆盖

| 子集 | 条目数 | hit@1 | hit@3 | hit@all |
|---|---|---|---|---|
| 整体 | 145 | 136/435 | 70/145 | 19/145 |
| L2 | 39 | 37/117 | 21/39 | 3/39 |
| D2×L2 | 34 | 29/102 | 17/34 | 2/34 |

## X1v2 baseline 覆盖

| 子集 | 条目数 | hit@1 | hit@3 | hit@all |
|---|---|---|---|---|
| 整体 | 145 | 179/435 | 80/145 | 40/145 |
| L2 | 39 | 26/117 | 13/39 | 5/39 |
| D2×L2 | 34 | 21/102 | 10/34 | 4/34 |

## 质量、错误与成本

方法侧 finding 的 W/D/L 分布、accepted/confirmed 数、schema/provider/local failure 数以及每次 attempt 的计费明细见 `metrics.json`；provider retry exemption 只统计 `billing_disposition=provider_error_retry_exempt`，所有其他 attempt 都计费。方法生成成本为 `$4.229658`，baseline 生成成本为 `$0.225233`，唯一成本倍率为 `18.78x`。独立 judge 审计成本为 `$12.284775`，只作研究支出审计，不进入该倍率。

## 逐条台账对照

方法与 baseline 的逐条台账表物理分开，分别见 `ledger_method.md` 与 `ledger_baseline.md`；每个单元格是三轮中该轮的语义命中结果。正式结果要求 judge 对全部 pair 给出完整裁定，不能用全 miss 代替失败。

## 可复现边界

原始完整运行目录位于本机 `runs/paper1/luna-full-x3-20260819-v1/`，本目录的 `audit_index.json` 保存每个 raw record 的 SHA-256、状态、失败分类和紧凑审计摘要路径；原始 raw prompt/response 体积过大且包含重复中间阶段，不复制进 git。
