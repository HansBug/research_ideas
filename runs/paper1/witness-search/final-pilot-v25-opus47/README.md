# v25 五格审计副本

本目录是 `fivecase-v25-basis-contract` 的不可变审计副本，profile 为 `claude-opus-4-7`，方法版本为 `v25-basis-contract`。五份 `*-record.json` 保存完整的输入摘要、LLM prompt/raw/parsed output、call id、usage、配置价格、执行 receipt、source causality certificate、semantic-binding receipt、D/W/L、accepted/confirmed 和 provenance audit；`manifest.json` 给出每份 record 的 SHA-256。目录内的 JSON 是证据真源，汇总数字和解释见 `ALIGNMENT_AUDIT.md` 与仓库中的 `pipeline/witness_search_prototype/PILOT_REPORT.md`。

本副本只表示五格 pilot，不是完整 benchmark。保守人工对齐为 Overall `18/21`、L2 `9/11`；五格 accepted report 为 `51`，strict confirmed report 为 `13`，方法成本为 `$3.385336`，同模型 X1v2 成本复核倍率为 `16.47×`。历史 X1v2 六格网格在这五个 pair 上的 unique hit 为 `14/21`、L2 为 `5/11`；同日 cost-only baseline 只提供逐格 emitted 数和成本，尚未完成环外逐格 hit matching。这些数字没有环外 blind judge 和运行时 baseline record 资格标记，不能写成整体 precision、显著性或 54-pair 结论。

复核命令：

```bash
sha256sum 0004-opus47-record.json 0023-opus47-record.json 0053-opus47-record.json 0046-opus47-record.json 0029-opus47-record.json
python -m json.tool manifest.json >/dev/null
```

任何 JSON 改动都必须同步更新 `manifest.json`；不得把 prompt 中的真实台账答案、X1v2 命中或人工 matching 结论回灌到 runtime 输入。
