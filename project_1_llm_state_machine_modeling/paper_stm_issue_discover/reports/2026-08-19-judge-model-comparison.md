# 2026-08-19 独立语义 Judge 模型对照

本文记录 D1/D2-release semantic judge 在 `gpt-5.6-luna` 与 `gpt-5.6-sol` 上对同一冻结 v26 method/X1v2 输出的对照。两种 judge 都读取同一份 145 条 ledger、同一 pair 的六个 cell；方法侧只读取 `report_issue_clusters` 中 D1/D2，X1v2 侧只读取 `parsed_output.issues`。judge 不是 method graph，其 token、cache、retry 与美元成本不进入 method/X1v2 的 25x 成本倍率。

## 完整结果

Luna 与 Sol 均已完成 54/54 pair。Sol 最初缺失的 `0009`、`0013`、`0056` 均由 provider/upstream failure 引起：`0009` 返回无状态码 `APIError: Upstream service temporarily unavailable`，`0013`、`0056` 的 relay 返回 HTTP 400，但结构化错误体明确为 `Upstream request failed`。修复 provider 分类后，三个 pair 均在同一次 judge 进程内原地重发并取得真实 `status=ok` 裁定；失败 attempt 分别为 4、2、1 次，均记为 `provider_error_retry_exempt`，最终成功 attempt 正常计费。没有使用 Luna 结果补 Sol，也没有把失败伪装成全 miss。

| Judge | 成功 pair | 方法整体 hit@1 | X1v2 整体 hit@1 | 方法 L2 hit@1 | X1v2 L2 hit@1 | 方法 D2×L2 hit@1 | X1v2 D2×L2 hit@1 | 方法 release precision | X1v2 release precision |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| gpt-5.6-sol | 54/54 | 136/435（31.26%） | 179/435（41.15%） | 37/117（31.62%） | 26/117（22.22%） | 29/102（28.43%） | 21/102（20.59%） | 170/305（55.74%） | 185/512（36.13%） |
| gpt-5.6-luna | 54/54 | 134/435（30.80%） | 184/435（42.30%） | 38/117（32.48%） | 21/117（17.95%） | 30/102（29.41%） | 15/102（14.71%） | 161/305（52.79%） | 213/512（41.60%） |

在全部 435 个 ledger-position 上，method hit 标签为 both-hit 124、Luna-only 10、Sol-only 12、both-miss 289，一致率 94.94%；baseline 为 both-hit 166、Luna-only 18、Sol-only 13、both-miss 238，一致率 92.87%。305 条 method emission 的 FP 标签一致率为 88.52%，512 条 baseline emission 为 91.41%；完整 matched-ledger-ID 集合一致率分别为 87.54% 与 89.84%。两个模型的总体趋势一致，但具体 hit/FP 归因仍存在不可忽略差异。

## 可信度抽查与选择

对分歧最大的 `0019` 做了逐项独立语义复核，共检查 4 个 hit 分歧与 9 个 FP 分歧。13 项中 Sol 正确 13 项、Luna 正确 0 项、无两可项 0 项。Luna 的主要错误是把分别覆盖 HighwayMode 与 UrbanMode 的两条不完整 issue 拼成一个完整台账命中，并在同一 JSON 内把同一 baseline issue 同时用于不相容的 ledger 映射；Sol 严格遵守禁止拼接和同处同性质规则。

因此正式主结果采用 `gpt-5.6-sol` 54/54 judge，Luna 只作为低成本敏感性对照。选择依据是完整性已经相同后，Sol 在人工深查分歧上的语义正确性显著更高，而不是因为 Sol 的指标对任一实验臂更有利。两臂始终使用同一个 Sol judge，不能混合两套标签形成 headline。

## 成本边界

Prototype v26 生成成本为 `$4.229658`，同模型 X1v2 生成成本为 `$0.225233`，唯一 method/X1v2 倍率为 `18.78x`。Luna judge 独立审计成本约 `$0.365308`，Sol judge 包含历史尝试和本轮补判的完整独立审计成本为 `$12.284775`，约为 Luna 的 33.63 倍；二者都不进入 18.78x。高配 judge 的费用是评测审计支出，当前选择优先保障标签可信度。

主结果、逐条两臂表和结构化指标见 [2026-08-19-luna-full-x3-v26.md](./2026-08-19-luna-full-x3-v26.md) 及其同名子目录；可提交的完整 54 份 Sol JSON、调用审计与三份补判 retry manifest 见 [judge-sol/](./2026-08-19-luna-full-x3-v26/judge-sol/)。本机 `runs/paper1/luna-full-x3-20260819-v1/` 另保留 method、baseline、Luna 对照及体积更大的原始运行证据。
