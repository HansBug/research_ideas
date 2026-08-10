# readiness_audit/ — 语料准入审计（结论已固化，不再重跑）

> 🟡 **本目录回答的是「哪些 seed 能用」这个已经答完的问题。** 60 例语料已据此选定并冻结，
> 因此它不参与任何一格实验，只作为**语料选择的证据链**。
>
> | 问题 | 答案 |
> | :-- | :-- |
> | 在运行路径上吗 | 不在。结论固化在 [handoff/](./handoff/)；重跑只为复验证据链 |
> | 它的产出被谁消费 | 语料选择决策；60 例最终形态见 [../representation/reports/llms_emp_r45_java_60/](../representation/reports/llms_emp_r45_java_60/) |
> | 包名 | `paper_stm_repair_smoke`（旧名，且与目录名也不同——本目录原名 `pipeline/smoke/`） |
> | 测试规模 | 8 个（本目录测试最少；主要资产是**已提交的 report**，不是测试） |
> | 调 LLM 吗 | 不。不读 `.env`，不调 provider |
>
> ⚠️ **本目录的「四例」与论文语料无关。** 那是历史 smoke fixture，用于验证转换 / 表示桥 / 评价门
> 接口是否连通；论文语料是 60 例（实验网格 54 例）。两套统计不得混用。
>
> ⚠️ **`*.md` 一律不是事实源。** 所有统计必须能从 `*.json` / `*.jsonl` / `records_index.json` /
> `archive_manifest.json` 复算。

## 0. 定位

本目录是 `paper_stm_issue_discover/` 的 **R5 修正前准备度审计** 工作区，用于在进入 R6 修正循环骨架前，审计 `<NL, STM_0>` 输入能否稳定走到内部可机检 `.fcstm` 表示，并把可进入后续阶段的证据、阻塞原因和交接目标结构化写盘。

R5 只回答：当前 seed 资源池中哪些原装 `STM_0` 能进入内部可机检 `.fcstm` 表示，哪些只能 `partial` / `blocked` / `not_applicable` / `needs_generation` / `missing_asset`，以及这些状态的原因是什么。R5.5 在 R5 事实源之上，只对 `llms-emp-stm-subset` 这一主 seed 池做 60 pair / 10 NL cluster 深度画像、partial 归因、blocked probe 与 R5.6 边界交接。

> 兼容说明：本目录由旧 `pipeline/smoke/` 重命名而来，Python 包名和命令入口暂保留 `paper_stm_repair_smoke`，用于避免破坏既有测试和 run record；新的路径语义以 `readiness_audit/` 为准，后续若重命名包名必须提供迁移测试。

R5 **不是**主实验，不执行 repair / fix loop，不生成 `STM_k`，不调用真实 LLM，不读取 `.env`，不把 conversion / normalization / 表示转换收益计入修正收益。

## 1. 输入来源

### 1.1 选定四例冒烟

⚠️ **路径已漂移，请勿照此重跑。** 生成器 `cli.py` 的 `SELECTED_DIR` 仍指向
[../../selected_seed_examples/](../../selected_seed_examples/)，但该目录在 PR #162 之后已改为
60 个 `llms_emp_feedback_final_NNNN/`，**不再包含下表的四个 `example_id`**。四例输入现居
[../conversion/fixtures/r3_selected_seed_examples/](../conversion/fixtures/r3_selected_seed_examples/)。
因此 `run-selected` 只能复现 committed report，不宜按当前代码重跑；`validate` 亦已报出
index archive 缺失与 R6/R7/R8 handoff 计数不符（该命令只打印 ERROR 并返回 0，不是门禁）。
这属于语料换代后的已知欠账，**不影响任何论文结论**——四例本就不是论文语料。

下表为历史四例的 committed 审计口径，每例消费 committed 上游制品，不在 R5 重写上游事实。

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
readiness_audit/
├── README.md
├── selected_examples/
│   ├── smoke_report.json
│   ├── smoke_summary.md        # human redirect / lightweight entry only
│   └── smoke_records/
│       └── <example_id>.json
├── seed_sweep/
│   ├── sweep_report.json
│   ├── records_index.json
│   ├── audit_records/
│   ├── sweep_summary.md        # human redirect / lightweight entry only
│   ├── blocked_cases.md
│   ├── partial_cases.md
│   └── sampling_analysis.md
├── artifact_archives/
│   ├── archive_manifest.json
│   └── archives/
│       └── <entry_id>_records.zip
├── llms_emp_profile/
│   ├── llms_emp_case_matrix.jsonl
│   ├── llms_emp_cluster_profiles.jsonl
│   ├── llms_emp_cluster_llm_matrix.jsonl
│   ├── llms_emp_partial_attribution_ledger.jsonl
│   ├── llms_emp_blocked_probe.jsonl
│   ├── llms_emp_deep_profile.md
│   ├── llms_emp_blocked_probe.md
│   ├── llms_emp_main_seed_analysis.md
│   └── llms_emp_r56_handoff.md
├── handoff/
│   ├── README.md
│   ├── llms_emp_main_seed_handoff.md  # human redirect only
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

- [./selected_examples/smoke_report.json](./selected_examples/smoke_report.json) 是选定四例 R5 审计机器事实源；[./selected_examples/smoke_records/](./selected_examples/smoke_records/) 保存 per-example 记录。
- [./seed_sweep/sweep_report.json](./seed_sweep/sweep_report.json) 是 seed library 全量摸排机器事实源；[./seed_sweep/records_index.json](./seed_sweep/records_index.json) 是全部 pair / asset record 的索引入口。
- [./artifact_archives/archive_manifest.json](./artifact_archives/archive_manifest.json) 与 [./artifact_archives/archives/](./artifact_archives/archives/) 是高基数明细复验入口；`records_index.json` 中的 `archive_path` 指向这些 zip。
- [./llms_emp_profile/llms_emp_case_matrix.jsonl](./llms_emp_profile/llms_emp_case_matrix.jsonl)、[./llms_emp_profile/llms_emp_cluster_profiles.jsonl](./llms_emp_profile/llms_emp_cluster_profiles.jsonl)、[./llms_emp_profile/llms_emp_cluster_llm_matrix.jsonl](./llms_emp_profile/llms_emp_cluster_llm_matrix.jsonl)、[./llms_emp_profile/llms_emp_partial_attribution_ledger.jsonl](./llms_emp_profile/llms_emp_partial_attribution_ledger.jsonl) 和 [./llms_emp_profile/llms_emp_blocked_probe.jsonl](./llms_emp_profile/llms_emp_blocked_probe.jsonl) 是 `llms-emp` 主 seed 池画像机器事实源。
- [./handoff/](./handoff/) 保存 R5 向 R6/R7/R8 传递的稳定证据；其中 `r5_to_r6_repair_inputs.json`、`r5_to_r7_seed_eligibility.json`、`r5_to_r8_negative_evidence.json` 是机器事实源。
- `*.md` human summary / handoff 文件只做人类入口或 redirect notice，不成为第二事实真源；所有统计必须能从 machine-readable JSON / JSONL / index / archive 复算。

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

每例必须核验：`source_meta.json` 可校验 `nl.txt` 与 `stm0.*`，`trace_verified=true`，`fcstm_meta.json` 可校验 selected `model.fcstm`，selected `model.fcstm` 与 [../representation/reports/fcstm_exports/](../representation/reports/fcstm_exports/) 对应副本一致，R3 canonical、archived R4/R5.7 fixture 和 R4.5 `parse_inspect_report.json` 均存在且 `example_id` 对齐。

R5 发现不一致时，只记录 R5 blocker；不得在 R5 静默修改 selected、conversion、evaluation 或 representation 上游制品。

`run-selected` 中的 `upstream_r4_fixture` 只作为 historical readiness input；当前生成器显式读取 [../../archive/r5_7_better_stm_snapshot/pipeline/evaluation/dry_run_examples/](../../archive/r5_7_better_stm_snapshot/pipeline/evaluation/dry_run_examples/)，不会向 active [../evaluation/](../evaluation/) 写回旧 Better STM gate。

### 5.2 全量摸排规则

`sweep_report.meta` 必须输出 entry 目录数、registry 数、被排除非条目目录和被排除辅助文件。`status_counts_by_pair` / `status_counts_by_asset` 是主事实字段，`primary_entry_status` 是派生汇总。每个 `converted` / `partial` pair record 必须保留 `loss_count`、`loss_categories`、`loss_reason_codes`、`irrecoverable_fields`、`conversion_attribution`、`representation_attribution` 与 `repair_contribution_allowed=false`。

### 5.3 归档 / 交接

`records_index.json` 始终索引所有 record；`archive_manifest.json` 始终存在。明细超过 50 个 record 或 5 MiB 时必须写入 `archives/<entry_id>_records.zip`，archive 内部路径必须稳定，不得依赖临时绝对路径。

[./handoff/](./handoff/) 只传递后续阶段输入：`r5_to_r6_repair_inputs.json` 不得声称已生成 `STM_k`；`r5_to_r7_seed_eligibility.json` 面向资格冻结；`r5_to_r8_negative_evidence.json` 汇总 blocked、missing、not_applicable 和 needs_generation。

## 6. 验收命令

```bash
PYTHONPATH=project_1_llm_state_machine_modeling/paper_stm_issue_discover/pipeline/readiness_audit/src:project_1_llm_state_machine_modeling/paper_stm_issue_discover/pipeline/representation/src:project_1_llm_state_machine_modeling/paper_stm_issue_discover/pipeline/conversion/src \
python -m pytest project_1_llm_state_machine_modeling/paper_stm_issue_discover/pipeline/readiness_audit/tests

PYTHONPATH=project_1_llm_state_machine_modeling/paper_stm_issue_discover/pipeline/readiness_audit/src:project_1_llm_state_machine_modeling/paper_stm_issue_discover/pipeline/representation/src:project_1_llm_state_machine_modeling/paper_stm_issue_discover/pipeline/conversion/src \
python -m paper_stm_repair_smoke.cli run-selected

PYTHONPATH=project_1_llm_state_machine_modeling/paper_stm_issue_discover/pipeline/readiness_audit/src:project_1_llm_state_machine_modeling/paper_stm_issue_discover/pipeline/representation/src:project_1_llm_state_machine_modeling/paper_stm_issue_discover/pipeline/conversion/src \
python -m paper_stm_repair_smoke.cli run-seed-sweep --max-per-pair-seconds 30 --continue-on-error

PYTHONPATH=project_1_llm_state_machine_modeling/paper_stm_issue_discover/pipeline/readiness_audit/src:project_1_llm_state_machine_modeling/paper_stm_issue_discover/pipeline/representation/src:project_1_llm_state_machine_modeling/paper_stm_issue_discover/pipeline/conversion/src \
python -m paper_stm_repair_smoke.cli run-llms-emp-profile

PYTHONPATH=project_1_llm_state_machine_modeling/paper_stm_issue_discover/pipeline/readiness_audit/src \
python -m paper_stm_repair_smoke.cli validate

PYTHONPATH=project_1_llm_state_machine_modeling/paper_stm_issue_discover/pipeline/readiness_audit/src:project_1_llm_state_machine_modeling/paper_stm_issue_discover/pipeline/representation/src:project_1_llm_state_machine_modeling/paper_stm_issue_discover/pipeline/conversion/src \
python -m pytest \
  project_1_llm_state_machine_modeling/paper_stm_issue_discover/pipeline/conversion/tests \
  project_1_llm_state_machine_modeling/paper_stm_issue_discover/pipeline/representation/tests \
  project_1_llm_state_machine_modeling/paper_stm_issue_discover/pipeline/readiness_audit/tests

git diff --check
```

R4/R5.7 evaluation tests 已归档到 [../../archive/r5_7_better_stm_snapshot/pipeline/evaluation/tests/](../../archive/r5_7_better_stm_snapshot/pipeline/evaluation/tests/)；active readiness 复验不再调用旧 Better STM gate tests。

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
