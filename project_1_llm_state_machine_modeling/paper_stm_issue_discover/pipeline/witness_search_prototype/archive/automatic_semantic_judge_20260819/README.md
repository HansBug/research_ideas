# 已停用：2026-08-19 自动语义评测路线

本目录保留一次已停用的自动语义 judge 与聚合器源码，只用于解释历史调试产物和失败原因，不得重新运行、修改后复活或用于任何正式 hit/FP 统计。

## 为什么停用

该路线让 LLM 自动判断 release issue 与台账是否同处同性质，并由脚本派生 hit 与 false positive；这违反当前冻结纪律：最终运行结果对照台账的 hit/FP 必须全人工逐条阅读和裁决，严禁脚本或 LLM judge 进行语义匹配、候选推荐或争议处理。

2026-08-19 已产生的 `runs/paper1/v27-strict-v26-20260819/` 全部 JSON、manifest、hit/FP 标签与自动评测失败均为无效调试证据，不进入 v26/v27 正式结果。其 provider 调用也不是 prototype 的 `STM+NL+形式制品 -> issues` 推理，不进入 25x 成本倍率。

## 正式替代

正式评测以 [manual_release_evaluation.md](../../../../discover_matrix/docs/protocol/manual_release_evaluation.md) 为唯一协议：方法侧只判 D1/D2 `report_issue_clusters`，X1v2 侧只判最终 `parsed_output.issues`，所有对应关系和 FP 成分均由人工逐条填写理由。确定性工具至多在人工标签冻结后检查 exact ID 和做算术，不能产生或改变语义标签。

## 复活边界

本路线无复活入口。若未来研究要比较自动 judge 与人工 judge，只能作为独立的 judge-methodology 研究，在不替代 paper1 人工真值的前提下另开实验与协议；不得把本目录代码重新接回 paper1 主评测链。
