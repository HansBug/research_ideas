# LLMS-EMP expected issue set — 审计数据

本 gist 是 **expected issue set** 的机读面。逐 pair 可读台帐在**另一个 gist**，见对应 issue 正文的入口表。

## 文件

| 文件 | 内容 |
| --- | --- |
| `expected_issue_set.json` | **主档**：129 条记录，每条含自然语言描述、归因层、缺陷方向、断言组（primary / negative_control / corroborating，各带实测值）、同质组、上游关联 |
| `index.tsv` | 逐 pair 一行的机读索引：条数、可自动验收数、须人工数、层分布、方向分布、旧台帐 E1 数、是否进入 8 格运行 |
| `ledger_coverage.json` | issue #166 的 47 条逐条对照本集合的结果（`binding_match` / `same_pair_only` / `unaccounted`）|
| `final_stratification.json` | 154 行分层逐行数据，含判定来源与主裁定 |
| `defect_classification.json` | 缺陷方向 × 谓词族交叉分类 |
| `reconcile.json` | 交叉一致性检查结果：多个独立来源报同一批数，任何不一致都会阻断发布 |
| `predcov_*` | 谓词覆盖复跑：五批原始判定 + 独立复跑结果 + 方法与已知坑 |
| `loopaudit_*` | 8 格运行审计：逐格命中/漏检、归因重放、prompt 审计、范畴裁定 |
| `nlreview_*` | NL 复核各批原始判定、`extra` 有害性判定、主裁定、`extra` 归属政策 |

## 计数口径（混用会算错）

| 口径 | 含义 |
| --- | --- |
| **记录条数** | 一条 expected issue 一条记录（129）|
| **同质组** | 同 pair 上主谓词与元素集合完全相同者视为同一缺陷。**命中率的分子与分母都应按同质组计**，否则把一个缺陷报成三条的模型会虚高 |
| **可自动验收** | 主断言实测返回 `False`（115 条）|
| **须人工判定** | 19 个封闭谓词表述不出（14 条）|

## 断言组的三种角色

`primary` 陈述缺陷（须实测 `False`）；`negative_control` 证明主断言不是恒假（**须实测 `True`**）；`corroborating` 补第二个后果。标为 `recovered_unverified` 的是从复核者散文里恢复、但未能自动求值的表达式 —— 记录在案以便人工核对，**不计入证据**。
