# R3.1 PlantUML 转换前规范化与恢复

本目录记录 R3.1 的 PlantUML pre-SCXML normalization / recovery 规则与复验方法。它只服务 conversion eligibility 审计，不是 source-level issue discovery / repair / closure 方法本身。

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
| `main_eligibility_included` | 通过 low-risk gate、SCXML parser、source-level semantic preservation audit 和分布 gate 的实际可用输入 | 可作为后续 R4/R5 输入集合 |

## 复验命令

```bash
export PLANTUML_JAR=/abs/path/to/plantuml.jar
PYTHONPATH=project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/conversion/src \
python -m paper_stm_repair_conversion.cli recover-plantuml \
  --run-id r3.1-plantuml-recovery-v0 \
  --created-at 2026-06-25T12:00:00+00:00
```

缺少 Java / PlantUML 时命令必须 loudly fail，并给出下载和环境变量配置建议；不得静默 fallback 到正则 parser 或旧 SCXML fixture。

## 输出

- [../reports/plantuml_recovery_report.json](../reports/plantuml_recovery_report.json)：R3.1 committed 小型恢复报告。
- [../reports/plantuml_recovery_summary.md](../reports/plantuml_recovery_summary.md)：人工阅读摘要。
- [../reports/plantuml_normalization_ledger.jsonl](../reports/plantuml_normalization_ledger.jsonl)：逐变换 ledger。
- [../artifacts/README.md](../artifacts/README.md)：conversion artifacts 总入口。
- [../artifacts/plantuml_recovery/r3_1_committed/README.md](../artifacts/plantuml_recovery/r3_1_committed/README.md)：全量 raw / normalized candidates 与官方 SCXML archive 使用指南。
- [../artifacts/plantuml_recovery/r3_1_committed/workdir.zip](../artifacts/plantuml_recovery/r3_1_committed/workdir.zip)：normalized candidates 与官方 SCXML 的全量高基数 archive；report 里的 candidate / SCXML path 是 zip member path。

不要提交解压后的 `workdir/`；如需人工检查，按 artifact README 解压到 `/tmp` 或本地临时目录。

## 学术边界

- raw assets、`pairs.jsonl`、selected smoke examples 不得覆盖。
- 高风险规则默认只进入 supplementary / manual-review bucket。
- 主 eligibility 必须通过 source-level semantic preservation audit；该 audit 只能支撑“结构签名保持”表述，不能写成无条件严格语义等价。
- transition endpoint 若含内嵌 `[*]`（如 `Closed [*]`、`Final [*]`），必须视为伪状态标记语义歧义；即使 alias 后官方 SCXML 可导出，也只能作为 supplementary / manual-review，不得进入主 eligibility。
- `fork_join_decl_to_state` 必须标注 `concurrency_degraded=true` 且 `main_eligibility_included=false`。
- LLMS-EMP 的 cross-LLM claim 只有在每个 LLM `eligible_after >= 5` 且 max/min ratio <= 2 时才允许；否则只能写 coverage audit / negative finding。
