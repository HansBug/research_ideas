# R3.1 PlantUML 转换前规范化与恢复

本目录记录 R3.1 的 PlantUML pre-SCXML normalization / recovery 规则与复验方法。它只服务 conversion eligibility 审计，不是 `<NL, STM_0> -> Better STM` 修复方法本身。

## 工作方式

1. 从 seed library 一手 `pairs.jsonl` 读取 PlantUML `STM_0` 文本。
2. 对原始文本先运行官方 PlantUML `-checkonly` / `-tscxml`。
3. 若原始官方 SCXML 已成功，则作为 naturally-converted profile；normalizer 不改写 canonical。
4. 若原始失败，则生成 run 目录中的 `normalized_candidates/*.puml`，并把 raw hash、normalized hash、规则、行号、before/after 写入 ledger。
5. 对 normalized candidate 再运行官方 PlantUML `-checkonly` / `-tscxml`。
6. 只有官方 SCXML 存在且可被 R3 SCXML adapter 消费时，才可计为 recovered；normalizer 不直接生成 canonical STM。

## 三种恢复率口径

| 口径 | 含义 | 论文主 claim 使用 |
|---|---|---|
| `technical_scxml_pass_all_rules` | 任意规则后通过官方 SCXML，包括高风险规则 | 不可；仅技术上界 |
| `low_risk_scxml_pass` | 仅低/中低风险规则且无 action/guard/hierarchy/concurrency 高风险 loss | 可作为 conservative recovery 上界 |
| `main_eligibility_included` | 通过 low-risk gate、SCXML parser 和分布 gate 的实际可用输入 | 可作为后续 R4/R5 输入集合 |

## 复验命令

```bash
export PLANTUML_JAR=/abs/path/to/plantuml.jar
PYTHONPATH=project_1_llm_state_machine_modeling/paper_stm_repair/conversion/src \
python -m paper_stm_repair_conversion.cli recover-plantuml \
  --run-id r3.1-plantuml-recovery-v0 \
  --created-at 2026-06-25T12:00:00+00:00
```

缺少 Java / PlantUML 时命令必须 loudly fail，并给出下载和环境变量配置建议；不得静默 fallback 到正则 parser 或旧 SCXML fixture。

## 输出

- [../reports/plantuml_recovery_report.json](../reports/plantuml_recovery_report.json)：R3.1 committed 小型恢复报告。
- [../reports/plantuml_recovery_summary.md](../reports/plantuml_recovery_summary.md)：人工阅读摘要。
- [../reports/plantuml_normalization_ledger.jsonl](../reports/plantuml_normalization_ledger.jsonl)：逐变换 ledger。
- `runs/paper_stm_repair/conversion/plantuml_recovery/r3_1_committed/`：normalized candidates 与官方 SCXML run artifact。

## 学术边界

- raw assets、`pairs.jsonl`、selected smoke examples 不得覆盖。
- 高风险规则默认只进入 supplementary / manual-review bucket。
- `fork_join_decl_to_state` 必须标注 `concurrency_degraded=true` 且 `main_eligibility_included=false`。
- LLMS-EMP 的 cross-LLM claim 只有在每个 LLM `eligible_after >= 5` 且 max/min ratio <= 2 时才允许；否则只能写 coverage audit / negative finding。
