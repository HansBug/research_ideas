# R5 确定性冒烟与 seed library 准备度审计

## 0. 定位

本目录是 `paper_stm_repair/` 的 **R5 修正前准备度审计** 工作区，用于在进入 R6 修正循环骨架前，审计 `<NL, STM_0>` 输入能否稳定走到内部可机检 `.fcstm` 表示，并把可进入后续阶段的证据、阻塞原因和交接目标结构化写盘。

R5 只回答：当前 seed 资源池中哪些原装 `STM_0` 能进入内部可机检 `.fcstm` 表示，哪些只能 `partial` / `blocked` / `not_applicable` / `needs_generation` / `missing_asset`，以及这些状态的原因是什么。

R5 **不是**主实验，不执行 repair / fix loop，不生成 `STM_k`，不调用真实 LLM，不读取 `.env`，不把 conversion / normalization / 表示转换收益计入修正收益。

## 1. 输入来源

### 1.1 选定四例冒烟

选定四例来自 [../../selected_seed_examples/](../../selected_seed_examples/)，每例必须消费 committed 上游制品，不在 R5 重写上游事实。

| example_id | 原始格式 | R5 审计重点 |
|---|---|---|
| `llms-emp-gpt4o-hldcs` | PlantUML | `nl.txt` / `stm0.puml` / `model.fcstm` / `fcstm_meta.json` / R3 canonical / R4 固化样例 / R4.5 report 是否一致。 |
| `sefm-ssc7-umple` | Umple | 同上，并保留 R3 timing loss 与 R4 focused caveat。 |
| `llms-emp-deepseek-microwave` | PlantUML | 同上，并保留 R3.1 pre-SCXML normalization replay caveat；raw `stm0.puml` 不得覆盖。 |
| `llms-emp-kimi-autonomous-collision` | PlantUML | 同上，并保留 condition-like label / event 降级 caveat。 |

### 1.2 seed library sweep

seed library sweep 读取 [../../corpora/seed_library/](../../corpora/seed_library/) 的当前条目目录、`seed_resource_registry.json`、assets 与 pairs，做 entry / asset / pair 级 census。

R5 sweep 只处理 deterministic、本地可核验的一手资源：

- 有作者一手 `NL + generated STM_0`：尝试或裁决转换状态。
- `pipeline_only` / `NL+code` 但无作者 generated `STM_0`：记为 `needs_generation`，R5 不复跑生成。
- related-only、paper-reconstructable、无 generated STM、非目标形式主义：记为 `not_applicable`。
- 本地资源缺失或 hash / locator 无法核验：记为 `missing_asset`。

## 2. 目录结构

```text
smoke/
├── README.md
├── selected_examples/
│   ├── smoke_report.json
│   ├── smoke_summary.md
│   └── smoke_records/
│       └── <example_id>.json
├── seed_library_sweep/
│   ├── sweep_report.json
│   ├── sweep_summary.md
│   ├── blocked_cases.md
│   ├── partial_cases.md
│   ├── sampling_analysis.md
│   ├── llms_emp_main_seed_analysis.md
│   ├── audit_records/
│   ├── records_index.json
│   ├── archives/
│   │   └── <entry_id>_records.zip
│   └── archive_manifest.json
├── handoff/
│   ├── README.md
│   ├── llms_emp_main_seed_handoff.md
│   ├── r5_to_r6_repair_inputs.json
│   ├── r5_to_r7_seed_eligibility.json
│   └── r5_to_r8_negative_evidence.json
├── schemas/
│   ├── selected_smoke_report.schema.json
│   └── seed_sweep_report.schema.json
├── src/paper_stm_repair_smoke/
│   └── cli.py
└── tests/
    └── test_r5_smoke_contract.py
```

## 3. 输出职责

- [./selected_examples/smoke_report.json](./selected_examples/smoke_report.json) 是 选定四例 R5 审计事实源。
- [./seed_library_sweep/sweep_report.json](./seed_library_sweep/sweep_report.json) 是 seed library 全量摸排事实源。
- [./seed_library_sweep/records_index.json](./seed_library_sweep/records_index.json) 与 [./seed_library_sweep/archive_manifest.json](./seed_library_sweep/archive_manifest.json) 是高基数明细复验入口。
- [./seed_library_sweep/llms_emp_main_seed_analysis.md](./seed_library_sweep/llms_emp_main_seed_analysis.md) 是 R5 后对 `llms-emp-stm-subset` 主实验 seed 方向的长期归纳，含 60 case 状态表、问题谱系与 R6/R7 建议。
- [./handoff/](./handoff/) 保存 R5 向 R6/R7/R8 传递的稳定证据，其中 [./handoff/llms_emp_main_seed_handoff.md](./handoff/llms_emp_main_seed_handoff.md) 固化 `llms-emp-stm-subset` 优先路线。

Markdown summary 只做人类入口，不成为第二事实真源；所有统计必须能从 machine-readable JSON 复算。

每次生成的 report 还会写入 `generation_context`，包含生成命令、当前 base commit、工作区 dirty 状态、`cli.py` sha256 与 schema sha256。由于 R5 产物通常与生成器在同一个 PR 中提交，`repo_commit` 只表示生成时的 base commit；精确复验应同时使用 PR diff、`generator_cli_sha256`、schema hash 与 `records_index.json` / `archive_manifest.json`。

## 4. 状态口径

| 状态 | 含义 | 是否失败 | 默认交接目标 |
|---|---|---:|---|
| `converted` | 一手 / 条件 `NL + generated STM_0` 可定位，且能走到 `.fcstm` parse / inspect。 | 否 | `r6_candidate` / `r7_eligibility_review` |
| `partial` | 有一手资源并能部分转换，但存在语义 loss、切片不足、格式 caveat 或只适合作 supplementary。 | 否，但需风险入账 | `r7_eligibility_review` |
| `blocked` | 理论上有一手 `STM_0`，但当前工具链无法完成转换。 | 是 | `r8_negative_evidence` / `converter_followup` |
| `not_applicable` | related-only、paper-reconstructable、无 generated `STM_0`、非目标形式主义等。 | 否 | `related_work_or_excluded` |
| `needs_generation` | 有 NL + code / pipeline，但作者未发布 generated `STM_0`，需本项目另行复跑。 | 否，R5 不生成 | `followup_seed_generation_pr_required_before_r7_or_excluded_by_r7` |
| `missing_asset` | registry 指向的一手资源本地缺失或 hash / locator 无法核验。 | 是 | `asset_repair_required` |

`pipeline_only` 不是 R5 census status；registry 中 `pipeline_only` / `NL+code` 条目在 R5 统一落为 `needs_generation`，并保留原始 `resource_role`。

> 选定四例当前不预期出现 `pass`：若 22 项 R5 contract checks 全部通过但上游 R3/R4/R4.5 已记录 loss / caveat，则应保持 `partial`。这是一种修正前准备度事实，而不是 R5 冒烟失败。

## 5. 一致性与归因纪律

### 5.1 四例冒烟一致性

每例必须核验：`source_meta.json` 可校验 `nl.txt` 与 `stm0.*`，`trace_verified=true`，`fcstm_meta.json` 可校验 selected `model.fcstm`，selected `model.fcstm` 与 [../representation/reports/fcstm_exports/](../representation/reports/fcstm_exports/) 对应副本一致，R3 canonical、R4 固化样例和 R4.5 `parse_inspect_report.json` 均存在且 `example_id` 对齐。

R5 发现不一致时，只记录 R5 blocker；不得在 R5 静默修改 selected、conversion、evaluation 或 representation 上游制品。

### 5.2 全量摸排规则

`sweep_report.meta` 必须输出 entry 目录数、registry 数、被排除非条目目录和被排除辅助文件。`status_counts_by_pair` / `status_counts_by_asset` 是主事实字段，`primary_entry_status` 是派生汇总。每个 `converted` / `partial` pair record 必须保留 `loss_count`、`loss_categories`、`loss_reason_codes`、`irrecoverable_fields`、`conversion_attribution`、`representation_attribution` 与 `repair_contribution_allowed=false`。

### 5.3 归档 / 交接

`records_index.json` 始终索引所有 record；`archive_manifest.json` 始终存在。明细超过 50 个 record 或 5 MiB 时必须写入 `archives/<entry_id>_records.zip`，archive 内部路径必须稳定，不得依赖临时绝对路径。

[./handoff/](./handoff/) 只传递后续阶段输入：`r5_to_r6_repair_inputs.json` 不得声称已生成 `STM_k`；`r5_to_r7_seed_eligibility.json` 面向资格冻结；`r5_to_r8_negative_evidence.json` 汇总 blocked、missing、not_applicable 和 needs_generation。

## 6. 验收命令

```bash
PYTHONPATH=project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/smoke/src:project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/representation/src:project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/conversion/src \
python -m pytest project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/smoke/tests

PYTHONPATH=project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/smoke/src:project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/representation/src:project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/conversion/src \
python -m paper_stm_repair_smoke.cli run-selected

PYTHONPATH=project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/smoke/src:project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/representation/src:project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/conversion/src \
python -m paper_stm_repair_smoke.cli run-seed-sweep --max-per-pair-seconds 30 --continue-on-error

PYTHONPATH=project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/smoke/src \
python -m paper_stm_repair_smoke.cli validate

PYTHONPATH=project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/smoke/src:project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/representation/src:project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/conversion/src \
python -m pytest \
  project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/conversion/tests \
  project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/evaluation/tests \
  project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/representation/tests

git diff --check
```

`run-seed-sweep` 默认采用 `--continue-on-error` 语义：单个 pair 的 tool exception / timeout 会进入该 pair record，不中断全量摸排；如需调试工具 bug，可使用 `--no-continue-on-error` 让异常 fail-fast。

## 7. 禁止事项

1. 不运行 repair / fix loop。
2. 不生成 `STM_k`。
3. 不调用真实 LLM，不读取 `.env`。
4. 不把 old `method/` agent loop 冒充为 paper1 新修正循环。
5. 不把 conversion / normalization / 表示转换收益计入修正收益。
6. 不把 选定四例或 seed sweep 结果写成主实验结果。
7. 不把 `pipeline_only`、paper-reconstructable、related-only 条目冒充为作者一手 generated seed。
8. 不把 Markdown summary 当作事实源。
