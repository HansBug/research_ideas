# 运行审计

方法矩阵固定为 54 个 pair × 3 轮，共 162 格；三轮各 54 格均存在 `record.json`，顶层原始状态均为 `completed`，aggregate 将 `completed` 归一为 eligible `ok`，没有缺格或整格失败。

方法观测共 757 次，全部记录 `streaming=true`，使用 `openai-responses` adapter；总 attempt 为 762。5 次 `provider_response` 失败均在同一调用上下文中产生下一次重发，因此前序 attempt 的 billing disposition 是 `provider_error_retry_exempt`；21 次 `structured_validation` 失败没有 provider 豁免并正常计费。没有 provider/schema 整格失败，所有失败诊断仍保存在 raw record。

独立 Luna semantic judge 使用 6 个并行 worker，54/54 pair 生成 `status=ok` judgement，6/6 worker manifest 已保存。judge 只接收 D1/D2 `report_issue_clusters` 和 baseline `parsed_output.issues`，不读取 D0 作为命中或 FP 证据；judge 成本为 `$0.664040`，不进入方法成本倍率。

方法 issue-generation 成本为 `$6.633537`，输入、输出、cache-read、cache-write 四类价格取自 `.llmconfig.yml` 对应 profile 的已记录价格卡；X1v2 成本为 `$0.225233`，倍率为 `29.45x`。每格成本、call、attempt、provider 豁免数和 raw record 路径见 `metrics.json` 的 `method_quality.per_pair`、`baseline_quality.per_pair` 与 `audit_index`。

完整原始 prompt、response、stage record 和 token usage 保留在 `runs/paper1/luna-full-x3-20260820-v27-stream/`；本目录只提交去密钥的 judge 语义裁定、汇总、逐条台账和审计 manifest。
