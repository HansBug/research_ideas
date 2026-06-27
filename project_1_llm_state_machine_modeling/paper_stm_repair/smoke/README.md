# R5 deterministic smoke 与 seed library readiness audit

## 0. 定位

本目录是 `paper_stm_repair/` 的 **R5 pre-repair readiness audit** 工作区，用于在进入 R6 修正循环骨架前，审计 `<NL, STM_0>` 输入能否稳定走到内部可机检 `.fcstm` 表示，并把可进入后续阶段的证据、阻塞原因和 handoff 目标结构化写盘。

R5 只回答：当前 seed 资源池中哪些原装 `STM_0` 能进入内部可机检 `.fcstm` 表示，哪些只能 `partial` / `blocked` / `not_applicable` / `needs_generation` / `missing_asset`，以及这些状态的原因是什么。

R5 **不是**主实验，不执行 repair / fix loop，不生成 `STM_k`，不调用真实 LLM，不读取 `.env`，不把 conversion / normalization / representation gain 计入 repair gain。

## 1. 输入来源

### 1.1 selected 四例 smoke

selected 四例来自 [../selected_seed_examples/](../selected_seed_examples/)，每例必须消费 committed 上游制品，不在 R5 重写上游事实。

| example_id | 原始格式 | R5 审计重点 |
|---|---|---|
| `llms-emp-gpt4o-hldcs` | PlantUML | `nl.txt` / `stm0.puml` / `model.fcstm` / `fcstm_meta.json` / R3 canonical / R4 fixture / R4.5 report 是否一致。 |
| `sefm-ssc7-umple` | Umple | 同上，并保留 R3 timing loss 与 R4 focused caveat。 |
| `llms-emp-deepseek-microwave` | PlantUML | 同上，并保留 R3.1 pre-SCXML normalization replay caveat；raw `stm0.puml` 不得覆盖。 |
| `llms-emp-kimi-autonomous-collision` | PlantUML | 同上，并保留 condition-like label / event 降级 caveat。 |

### 1.2 seed library sweep

seed library sweep 读取 [../corpora/seed_library/](../corpora/seed_library/) 的当前条目目录、`seed_resource_registry.json`、assets 与 pairs，做 entry / asset / pair 级 census。

R5 sweep 只处理 deterministic、本地可核验的一手资源：

- 有作者一手 `NL + generated STM_0`：尝试或裁决转换状态。
- `pipeline_only` / `NL+code` 但无作者 generated `STM_0`：记为 `needs_generation`，R5 不复跑生成。
- related-only、paper-reconstructable、无 generated STM、非目标形式主义：记为 `not_applicable`。
- 本地资源缺失或 hash / locator 无法核验：记为 `missing_asset`。

## 2. 目录结构

```text
smoke/
├── README.md
├── GUIDE.md
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
│   ├── audit_records/
│   ├── records_index.json
│   ├── archives/
│   │   └── <entry_id>_records.zip
│   └── archive_manifest.json
├── handoff/
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

- [./selected_examples/smoke_report.json](./selected_examples/smoke_report.json) 是 selected 四例 R5 审计事实源。
- [./seed_library_sweep/sweep_report.json](./seed_library_sweep/sweep_report.json) 是 seed library 全量摸排事实源。
- [./seed_library_sweep/records_index.json](./seed_library_sweep/records_index.json) 与 [./seed_library_sweep/archive_manifest.json](./seed_library_sweep/archive_manifest.json) 是高基数明细复验入口。
- [./handoff/](./handoff/) 保存 R5 向 R6/R7/R8 传递的稳定证据。

Markdown summary 只做人类入口，不成为第二事实真源；所有统计必须能从 machine-readable JSON 复算。

每次生成的 report 还会写入 `generation_context`，包含生成命令、当前 base commit、工作区 dirty 状态、`cli.py` sha256 与 schema sha256。由于 R5 产物通常与生成器在同一个 PR 中提交，`repo_commit` 只表示生成时的 base commit；精确复验应同时使用 PR diff、`generator_cli_sha256`、schema hash 与 `records_index.json` / `archive_manifest.json`。

## 4. 状态口径

| 状态 | 含义 | 是否失败 | 默认 handoff_target |
|---|---|---:|---|
| `converted` | 一手 / 条件 `NL + generated STM_0` 可定位，且能走到 `.fcstm` parse / inspect。 | 否 | `r6_candidate` / `r7_eligibility_review` |
| `partial` | 有一手资源并能部分转换，但存在语义 loss、切片不足、格式 caveat 或只适合作 supplementary。 | 否，但需风险入账 | `r7_eligibility_review` |
| `blocked` | 理论上有一手 `STM_0`，但当前工具链无法完成转换。 | 是 | `r8_negative_evidence` / `converter_followup` |
| `not_applicable` | related-only、paper-reconstructable、无 generated `STM_0`、非目标形式主义等。 | 否 | `related_work_or_excluded` |
| `needs_generation` | 有 NL + code / pipeline，但作者未发布 generated `STM_0`，需本项目另行复跑。 | 否，R5 不生成 | `followup_seed_generation_pr_required_before_r7_or_excluded_by_r7` |
| `missing_asset` | registry 指向的一手资源本地缺失或 hash / locator 无法核验。 | 是 | `asset_repair_required` |

`pipeline_only` 不是 R5 census status；registry 中 `pipeline_only` / `NL+code` 条目在 R5 统一落为 `needs_generation`，并保留原始 `resource_role`。

> selected 四例当前不预期出现 `pass`：若 22 项 R5 contract checks 全部通过但上游 R3/R4/R4.5 已记录 loss / caveat，则应保持 `partial`。这是一种 pre-repair readiness 事实，而不是 R5 smoke 失败。

## 5. 验收命令

```bash
PYTHONPATH=project_1_llm_state_machine_modeling/paper_stm_repair/smoke/src:project_1_llm_state_machine_modeling/paper_stm_repair/representation/src:project_1_llm_state_machine_modeling/paper_stm_repair/conversion/src \
python -m pytest project_1_llm_state_machine_modeling/paper_stm_repair/smoke/tests

PYTHONPATH=project_1_llm_state_machine_modeling/paper_stm_repair/smoke/src:project_1_llm_state_machine_modeling/paper_stm_repair/representation/src:project_1_llm_state_machine_modeling/paper_stm_repair/conversion/src \
python -m paper_stm_repair_smoke.cli run-selected

PYTHONPATH=project_1_llm_state_machine_modeling/paper_stm_repair/smoke/src:project_1_llm_state_machine_modeling/paper_stm_repair/representation/src:project_1_llm_state_machine_modeling/paper_stm_repair/conversion/src \
python -m paper_stm_repair_smoke.cli run-seed-sweep --max-per-pair-seconds 30 --continue-on-error

PYTHONPATH=project_1_llm_state_machine_modeling/paper_stm_repair/smoke/src \
python -m paper_stm_repair_smoke.cli validate

PYTHONPATH=project_1_llm_state_machine_modeling/paper_stm_repair/smoke/src:project_1_llm_state_machine_modeling/paper_stm_repair/representation/src:project_1_llm_state_machine_modeling/paper_stm_repair/conversion/src \
python -m pytest \
  project_1_llm_state_machine_modeling/paper_stm_repair/conversion/tests \
  project_1_llm_state_machine_modeling/paper_stm_repair/evaluation/tests \
  project_1_llm_state_machine_modeling/paper_stm_repair/representation/tests

git diff --check
```

`run-seed-sweep` 默认采用 `--continue-on-error` 语义：单个 pair 的 tool exception / timeout 会进入该 pair record，不中断全量摸排；如需调试工具 bug，可使用 `--no-continue-on-error` 让异常 fail-fast。

## 6. 禁止事项

1. 不运行 repair / fix loop。
2. 不生成 `STM_k`。
3. 不调用真实 LLM，不读取 `.env`。
4. 不把 old `method/` agent loop 冒充为 paper1 新修正循环。
5. 不把 conversion / normalization / representation gain 计入 repair gain。
6. 不把 selected 四例或 seed sweep 结果写成主实验结果。
7. 不把 `pipeline_only`、paper-reconstructable、related-only 条目冒充为作者一手 generated seed。
8. 不把 Markdown summary 当作事实源。
