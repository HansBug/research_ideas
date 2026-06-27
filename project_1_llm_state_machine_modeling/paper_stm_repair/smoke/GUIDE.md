# R5 smoke / sweep 工作指南

## 0. 最高边界

R5 是 **pre-repair readiness audit**，不是 repair runtime、不是主实验、不是论文结果统计。

任何 R5 产物都必须保留：

- `repair_contribution_allowed=false`
- conversion attribution
- representation attribution
- loss / caveat
- source path 与 hash
- status reason
- handoff target

R5 不能把 parse / inspect 成功解释为语义无损，不能把 R3.1 normalization 解释为 repair gain，也不能把 R4 fixture 的 `allow_repair_loop_smoke=true` 解释为已执行 repair loop。

## 1. 推荐阅读顺序

1. [../README.md](../README.md)：确认 paper1 主线与目录入口。
2. [../GUIDE.md](../GUIDE.md)：确认 `paper_stm_repair/` 顶层边界。
3. [../selected_seed_examples/README.md](../selected_seed_examples/README.md)：确认 selected 四例静态输入与 R4.5 `.fcstm` 快照。
4. [../conversion/README.md](../conversion/README.md) 与 [../conversion/GUIDE.md](../conversion/GUIDE.md)：确认 R3 conversion / canonical / loss 口径。
5. [../evaluation/EVALUATION_GATE.md](../evaluation/EVALUATION_GATE.md) 与 [../evaluation/DRY_RUNS.md](../evaluation/DRY_RUNS.md)：确认 R4 eligibility、diagnostic、scenario、Better STM caveat。
6. [../representation/README.md](../representation/README.md) 与 [../representation/GUIDE.md](../representation/GUIDE.md)：确认 R4.5 `.fcstm` / pyfcstm inspect 口径。
7. [../corpora/seed_library/README.md](../corpora/seed_library/README.md)、[../corpora/seed_library/GUIDE.md](../corpora/seed_library/GUIDE.md)、[../corpora/seed_library/SUMMARY.md](../corpora/seed_library/SUMMARY.md)、[../corpora/seed_library/REGISTRY.md](../corpora/seed_library/REGISTRY.md)：确认 seed library census 输入。

## 2. selected 四例上游路径模板

R5 selected smoke 必须按下表硬编码并核验四例上游路径；不得用目录猜测替代路径合同。

| example_id | selected 输入 | R3 canonical | R4 fixture | R4.5 representation |
|---|---|---|---|---|
| `llms-emp-gpt4o-hldcs` | `../selected_seed_examples/llms-emp-gpt4o-hldcs/README.md`; `nl.txt`; `stm0.puml`; `source_meta.json`; `model.fcstm`; `fcstm_meta.json` | `../conversion/reports/canonical/llms-emp-gpt4o-hldcs.canonical_stm.json` | `../evaluation/dry_run_examples/llms-emp-gpt4o-hldcs/{eligibility_decision,diagnostic_draft,scenario_draft,better_stm_checklist}.json` | `../representation/reports/fcstm_exports/llms-emp-gpt4o-hldcs/{model.fcstm,parse_inspect_report.json,lowering_inventory.json,name_mapping.json}` |
| `sefm-ssc7-umple` | `../selected_seed_examples/sefm-ssc7-umple/README.md`; `nl.txt`; `stm0.ump`; `source_meta.json`; `model.fcstm`; `fcstm_meta.json` | `../conversion/reports/canonical/sefm-ssc7-umple.canonical_stm.json` | `../evaluation/dry_run_examples/sefm-ssc7-umple/{eligibility_decision,diagnostic_draft,scenario_draft,better_stm_checklist}.json` | `../representation/reports/fcstm_exports/sefm-ssc7-umple/{model.fcstm,parse_inspect_report.json,lowering_inventory.json,name_mapping.json}` |
| `llms-emp-deepseek-microwave` | `../selected_seed_examples/llms-emp-deepseek-microwave/README.md`; `nl.txt`; `stm0.puml`; `source_meta.json`; `model.fcstm`; `fcstm_meta.json` | `../conversion/reports/canonical/llms-emp-deepseek-microwave.canonical_stm.json` | `../evaluation/dry_run_examples/llms-emp-deepseek-microwave/{eligibility_decision,diagnostic_draft,scenario_draft,better_stm_checklist}.json` | `../representation/reports/fcstm_exports/llms-emp-deepseek-microwave/{model.fcstm,parse_inspect_report.json,lowering_inventory.json,name_mapping.json}` |
| `llms-emp-kimi-autonomous-collision` | `../selected_seed_examples/llms-emp-kimi-autonomous-collision/README.md`; `nl.txt`; `stm0.puml`; `source_meta.json`; `model.fcstm`; `fcstm_meta.json` | `../conversion/reports/canonical/llms-emp-kimi-autonomous-collision.canonical_stm.json` | `../evaluation/dry_run_examples/llms-emp-kimi-autonomous-collision/{eligibility_decision,diagnostic_draft,scenario_draft,better_stm_checklist}.json` | `../representation/reports/fcstm_exports/llms-emp-kimi-autonomous-collision/{model.fcstm,parse_inspect_report.json,lowering_inventory.json,name_mapping.json}` |

同时还必须读取横向报告：

- R3 selected conversion report: [../conversion/reports/selected_seed_examples_conversion_report.json](../conversion/reports/selected_seed_examples_conversion_report.json)
- R3 selected loss ledger: [../conversion/reports/selected_seed_examples_loss_ledger.jsonl](../conversion/reports/selected_seed_examples_loss_ledger.jsonl)
- R4.5 export report: [../representation/reports/fcstm_export_report.json](../representation/reports/fcstm_export_report.json)
- R4.5 export loss ledger: [../representation/reports/fcstm_export_loss_ledger.jsonl](../representation/reports/fcstm_export_loss_ledger.jsonl)

## 3. selected smoke 一致性定义

每例必须逐项核验：

1. `source_meta.json.nl_sha256` 能校验 selected `nl.txt`。
2. `source_meta.json.stm0_sha256` 能校验 selected `stm0.*`。
3. `source_meta.json.trace_verified=true`。
4. `fcstm_meta.json.selected_fcstm_sha256` 能校验 selected `model.fcstm`。
5. `fcstm_meta.json.synchronized_from_fcstm_sha256` 等于 R4.5 representation export copy 对应 `model.fcstm` hash。
6. selected `model.fcstm` 与 `../representation/reports/fcstm_exports/<example_id>/model.fcstm` 的语义来源一致，不允许手工漂移。
7. R3 canonical path 存在且 example_id 一致。
8. R4 fixture 四件套存在且 example_id 一致。
9. R4.5 `parse_inspect_report.json` 存在，parse / inspect 状态必须直接读取该 committed report，并与横向 `fcstm_export_report.json` 中的 `parse_status` / `inspect_status` 对齐。
10. `repair_contribution_allowed=false`。

R5 发现不一致时，只记录 R5 blocker；不得在 R5 静默修改 selected、conversion、evaluation 或 representation 上游制品。

## 4. seed library sweep 规则

### 4.1 denominator

sweep 必须扫描 [../corpora/seed_library/](../corpora/seed_library/) 当前状态，并在 `sweep_report.meta` 中输出：entry 目录数量、有无 registry 数量、被排除非条目目录、被排除辅助文件。Markdown summary 只能引用 JSON 统计，不手写第二套数量。

### 4.2 status 枚举

| status | 判定规则 |
|---|---|
| `converted` | pair 可定位一手 / 条件 `NL + generated STM_0`，R3/R4.5 后 `.fcstm` parse / inspect 可用。 |
| `partial` | pair 有一手资源并可部分转换，但存在明确 loss、format caveat、切片不足或只能 supplementary。 |
| `blocked` | pair 理论上有一手 `STM_0`，但当前工具链无法转换。 |
| `not_applicable` | 条目没有 generated `STM_0`，或属于 related-only、paper-reconstructable、非目标形式主义。 |
| `needs_generation` | 有 NL + code / pipeline，但作者未发布 generated `STM_0`；R5 不复跑。 |
| `missing_asset` | registry 指向本地一手资源缺失、hash 不匹配或 locator 无法核验。 |

### 4.3 entry-level 聚合

`status_counts_by_pair` / `status_counts_by_asset` 是 JSON 中的主事实字段（概念上可简称 pair status / asset status），`entry_statuses` / `primary_entry_status` 是派生汇总。`primary_entry_status` precedence 固定为：无 registry -> `not_applicable`；asset 缺失 -> `missing_asset`；`pipeline_only` -> `needs_generation`；混合 converted/blocked/partial -> `partial`；全 converted -> `converted`；全 blocked -> `blocked`；其余 -> `partial`。

### 4.4 loss 归因字段

每个 `converted` / `partial` pair record 必须包含 `loss_count`、`loss_categories`、`loss_reason_codes`、`irrecoverable_fields`、`conversion_attribution`、`representation_attribution` 与 `repair_contribution_allowed=false`。

## 5. archive / records_index / manifest 纪律

1. `records_index.json` 始终存在，索引所有 record。
2. `archive_manifest.json` 始终存在，即使本轮没有 archive，也要记录空 archives 与生成上下文。
3. 明细不超过 50 个 record 且总量不超过 5 MiB 时，可以落在 `audit_records/`。
4. 明细超过 50 个 record 或 5 MiB 时，必须写入 `archives/<entry_id>_records.zip`。
5. `records_index.json` 每条至少包含 `record_type`、`record_id`、`entry_id`、`asset_id`、`pair_id`、`status`、`path_on_disk` 或 `path_in_zip`、`sha256`；其中 `record_type` 必须区分 `pair` 与 `asset`，不能只索引 pair 而丢弃资产证据链。
6. `archive_manifest.json` 每个 archive 至少包含 `archive_path`、`sha256`、`record_count`、`schema_version`、`internal_root`、`generation_command`。`archive_path` 统一按仓库根目录相对路径解析。
7. archive 内部路径必须稳定，不得依赖临时绝对路径。

## 6. handoff 规则

- `handoff/r5_to_r6_repair_inputs.json`：只包含可进入 R6 loop skeleton 的候选；不得声称已生成 `STM_k`。
- `handoff/r5_to_r7_seed_eligibility.json`：面向 R7 protocol 冻结，汇总 `converted`、`partial`、`needs_generation` 与 eligibility review 事项。
- `handoff/r5_to_r8_negative_evidence.json`：面向 R8 主实验前的负证据，汇总 `blocked`、`missing_asset`、`not_applicable`、`needs_generation`。

## 7. CLI 工作流

```bash
PYTHONPATH=project_1_llm_state_machine_modeling/paper_stm_repair/smoke/src:project_1_llm_state_machine_modeling/paper_stm_repair/representation/src:project_1_llm_state_machine_modeling/paper_stm_repair/conversion/src \
python -m paper_stm_repair_smoke.cli run-selected

PYTHONPATH=project_1_llm_state_machine_modeling/paper_stm_repair/smoke/src:project_1_llm_state_machine_modeling/paper_stm_repair/representation/src:project_1_llm_state_machine_modeling/paper_stm_repair/conversion/src \
python -m paper_stm_repair_smoke.cli run-seed-sweep --max-per-pair-seconds 30 --continue-on-error

PYTHONPATH=project_1_llm_state_machine_modeling/paper_stm_repair/smoke/src \
python -m paper_stm_repair_smoke.cli validate
```

执行策略：selected 四例只消费 committed R3/R4/R4.5 输出；seed sweep 先做 registry / asset / pair census，再对可定位原装 STM 文本且格式受支持的 pair 尝试转换。单个 pair 超时或失败只影响该 pair / asset 的 status，不阻塞全量 sweep。

`run-seed-sweep` 的 committed census 默认使用 `--continue-on-error`：per-pair tool exception 与 timeout 必须记录为明确 `blocked` reason，不得污染为普通 converter limitation；若要调试工具 bug，可临时使用 `--no-continue-on-error` fail-fast，但该模式不用于 R5 committed census。

## 8. validate 必须检查什么

`validate` 至少检查 selected 四例 record、上游路径、hash、R3/R4/R4.5 example_id、direct `parse_inspect_report.json` 状态、summary 复算、sweep schema、entry / asset / pair denominator、`records_index.json` 全量 payload、archive manifest、handoff 三件套与 sweep 计数一致性、loss 归因字段、`repair_contribution_allowed=false`，并通过 `validate_no_llm_or_env_boundary` 扫描 `smoke/src`、`smoke/tests` 与 indexed payload / handoff，确认不存在 `.env` 读取、真实 provider usage、provider SDK / network client 调用或 LLM runtime 记录。

报告中的 `generation_context` 必须保留生成命令、base commit、工作区 dirty 状态、CLI hash 与 schema hash。由于生成器和产物通常在同一 PR 中提交，`repo_commit` 不能单独作为复现锚点；复验必须同时使用 PR diff + `generator_cli_sha256` + schema hash + machine-readable records。

## 9. 抽样分析

[./seed_library_sweep/sampling_analysis.md](./seed_library_sweep/sampling_analysis.md) 必须覆盖 converted、partial、blocked-or-missing、not_applicable、needs_generation。抽样规则必须与 PR body 一致：每个状态组内按 `status -> entry_id -> pair_id` 排序，每类至少取前 3 条；若该类超过 100 条，再追加中位与末尾各 1 条。若某类为空，必须说明来自 `sweep_report.json` 的机器统计证据。

## 10. 禁止回写

R5 不得修改 [../selected_seed_examples/](../selected_seed_examples/) 的 raw `nl.txt` / `stm0.*`、[../conversion/](../conversion/) committed reports、[../evaluation/](../evaluation/) R4 fixture、[../representation/](../representation/) committed export reports、[../corpora/seed_library/](../corpora/seed_library/) 的一手 assets。若发现上游事实错误，R5 只能在 smoke / sweep record 中标记 blocker，并把后续归属写入 handoff 或 blocked cases。
