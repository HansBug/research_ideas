# R5.7.5 constructed STM_k dry-run evidence bundle

> 生成时间：2026-07-05 02:10:39。本目录是 R5.7.5 constructed `STM_k` 覆盖性 dry-run 的机器 / 半机器 evidence bundle。它不是正式 repair loop 结果目录。

## 1. 定位

本目录用 20 个人工 / 确定性构造的 candidate `STM_k` 测试 Better STM 裁决协议能否覆盖 `better / not_better / partial / unknown / stmk_repair_failure / protocol_or_provenance_invalid / stress_t1` 等路径。

硬纪律：全部 case 均 `headline_eligible=false`、`repair_effectiveness_eligible=false`、`constructed_for_protocol_dry_run=true`、`real_repair_run_id=null`；`.fcstm` 只是内部实验介质；C17 的 `candidate.fcstm` 故意 parse-invalid；`scenario_overfitting` 本轮只记录为 `handoff_only_not_covered`。

## 2. 文件说明

| 文件 / 子路径 | 说明 |
|---|---|
| [suite_index.json](./suite_index.json) | 20 个 constructed case 的主索引、coverage summary 和协议文档链接。 |
| [baseline_preflight.json](./baseline_preflight.json) | baseline 来源预检；0004 为手工 materialized protocol baseline，0009 采用同 cluster 0039 fallback。 |
| [baseline_bundles/](./baseline_bundles/) | 仅收纳 R5.7.5 新增的 0004 manual protocol baseline。 |
| [validate_suite.py](./validate_suite.py) | 本 bundle 的可执行审计入口；只验证 evidence bundle 一致性，不属于 repair method 实现。 |
| `cXX_*/candidate.fcstm` | 构造候选；除 C17 外应可被 pyfcstm parse。 |
| `cXX_*/*.json` | baseline pointer、change ledger、target ledger、adjudication record、expected verdict。 |

## 3. 复验入口

见 report 文末 `[cmd-*]` 命令和 PR 复验日志；最小本地复验命令为：

```bash
python project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/evaluation/dry_run_examples/r5_7_5_constructed_stmk/validate_suite.py --parse
```
