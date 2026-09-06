# 全量 x3 独立语义审计报告

本报告比较 gpt-5.6-luna 下的新方法 v27-stream 与 X1v2 baseline，运行矩阵为 54 个非 NL04 pair、每臂每 pair 三轮；命中由独立 gpt-5.6-luna 语义评审依据同一位置与同一性质判定，不使用关键词、字符串包含、编辑距离、embedding 或其他词法捷径。

## 方法侧覆盖

| 子集 | 条目数 | hit@1 | hit@3 | hit@all |
|---|---|---|---|---|
| 整体 | 145 | 276/435 | 107/145 | 76/145 |
| L2 | 39 | 81/117 | 35/39 | 20/39 |
| D2×L2 | 34 | 68/102 | 30/34 | 17/34 |

## X1v2 baseline 覆盖

| 子集 | 条目数 | hit@1 | hit@3 | hit@all |
|---|---|---|---|---|
| 整体 | 145 | 177/435 | 79/145 | 37/145 |
| L2 | 39 | 27/117 | 13/39 | 5/39 |
| D2×L2 | 34 | 21/102 | 11/34 | 3/34 |

## 相对差值

| 子集 | hit@1 方法−baseline | hit@3 方法−baseline | hit@all 方法−baseline |
|---|---:|---:|---:|
| 整体 | +22.76 个百分点 | +19.31 个百分点 | +26.90 个百分点 |
| L2 | +46.15 个百分点 | +56.41 个百分点 | +38.46 个百分点 |
| D2×L2 | +46.08 个百分点 | +55.88 个百分点 | +41.18 个百分点 |

方法在 435 个整体位置上命中 276 个，较 X1v2 多 99 个位置；三轮至少命中一次的台账条目为 107/145，较 X1v2 多 28 条。L2 的 hit@3 为 35/39，D2×L2 的 hit@3 为 30/34，均达到大部分覆盖且明显超过 baseline。

## 质量、错误与成本

方法侧 finding 的 W/D/L 分布、accepted/confirmed 数、schema/provider/local failure 数以及每次 attempt 的计费明细见 `metrics.json`；provider retry exemption 只统计 `billing_disposition=provider_error_retry_exempt`，所有其他 attempt 都计费。方法生成成本为 `$6.633537`，baseline 生成成本为 `$0.225233`，唯一成本倍率为 `29.45x`。独立 judge 审计成本为 `$0.664040`，只作研究支出审计，不进入该倍率。

## 逐条台账对照

方法与 baseline 的逐条台账表物理分开，分别见 `ledger_method.md` 与 `ledger_baseline.md`；每个单元格是三轮中该轮的语义命中结果。正式结果要求 judge 对全部 pair 给出完整裁定，不能用全 miss 代替失败。

## 末端发布面与 FP

方法三轮共形成 1,897 个 report cluster，其中 D0 1,010 个仅保留内部审计；真正进入最终输出和 hit/FP 统计的 D1/D2 release issue 为 881 个，其中 D2 697 个、D1 184 个，W2 635 个、W1 246 个。D0 没有进入 judge 输入、hit 分子或 FP 分母。

方法 release emission 为 881 条，其中 ledger-accounted 403 条、ledger-unmatched FP 478 条，precision 为 45.74%；X1v2 emission 为 512 条，其中 ledger-accounted 213 条、FP 299 条，precision 为 41.60%。方法 precision 高于 baseline 4.14 个百分点，FP rate 低于 baseline 4.14 个百分点，但方法因为发布更多 issue，绝对 FP 数比 baseline 多 179 条；该绝对负担是下一轮优先压缩项，不能被 precision 改善掩盖。

跨三轮按 `(pair, emitted_id)` 合并后，方法 unique-cause FP 为 363 个，X1v2 为 171 个；该读数只用于重复主张分析，不替代正式 release-emission precision。

## 运行与计费审计

方法矩阵为 162/162 格 `completed`，每个观测均为 `streaming=true`；共 757 次 LLM call、762 个 attempt。5 次 provider error 都在同一请求上下文中重发并标记 `provider_error_retry_exempt`，21 次 structured validation failure 按普通 attempt 计费；没有 provider/schema 整格失败。独立 Luna judge 为 54/54 `status=ok`，6 份 worker manifest 齐全，judge 成本单独审计且不进入方法倍率。

方法 issue-generation 成本为 `$6.633537`，X1v2 成本为 `$0.225233`，同模型倍率为 `29.45x`；本轮按用户最新指令优先保 hit、L2 和 FP，成本超过 25x 先记录为后续压缩项，不以降低质量为代价返工。成本价格直接来自配置的 input/output/cache-read/cache-write 四项价格。

## 可复现边界

原始完整运行目录位于本机 `runs/paper1/luna-full-x3-20260820-v27-stream/`（方法）和 `runs/paper1/luna-full-x3-20260819-v1/`（X1v2），最终审计目录保存每个 raw record 的 SHA-256、状态、失败分类和紧凑审计摘要路径；原始 raw prompt/response 体积过大且包含重复中间阶段，不复制进 git。
