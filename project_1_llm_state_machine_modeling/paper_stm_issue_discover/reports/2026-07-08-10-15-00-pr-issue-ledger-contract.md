# PR-issue-ledger source issue ledger v0 合同报告

> 证据引用说明：正文中的方括号引用（如 `[src-*]`、`[clm-*]`、`[cmd-*]`）均指向文末审计附录。这些键是稳定 ASCII key，不按数字顺序重排。

## 1. 定位与问题

本报告冻结 `PR-issue-ledger` 形成的长期合同事实：paper1 当前不再追问 “which STM is better”，而是需要一个能被 discovery、repair、closure 后续阶段共同消费的 **source-level issue ledger v0**。[clm-ledger-position]

该合同只解决一个最小问题：在给定 `NL + raw/source STM_0` 时，如何区分 candidate、confirmed、rejected conversion artifact、out-of-scope 与 insufficient-evidence issue，并给后续 repair runner 一个可审计的 `issue_id` / repair eligibility gate。[clm-status-branches]

本报告不声称已经运行真实 agent loop、不声称已经生成 `STM_final`、不冻结 final metrics / baseline / judge prompt，也不运行 #119 / R2 四个 selected examples。[clm-nonclaims]

## 2. 核心结论

| 结论 | 当前状态 | 证据 |
|---|---|---|
| source-level issue ledger v0 已有机器合同。 | 已落到 JSON Schema。 | [clm-schema] |
| v0 覆盖 6 个合同分支。 | 6 个 synthetic JSON fixture 覆盖 candidate / confirmed / rejected / out-of-scope / insufficient-evidence。 | [clm-fixtures] |
| repair eligibility gate 已显式化。 | 只有 `confirmation_status=confirmed` 且 `downstream_repair_allowed=true` 且 source-level attribution 允许的 issue 可进入 repair。 | [clm-repair-gate] |
| Q11=A 已入账。 | v0 允许 `raw_internal_inconsistency` 作为第二条 confirmed path，但必须在后续真实 raw/NL 与 discovery pilot 中复核。 | [clm-q11] |
| 本 PR 不做真实样本标注。 | fixture 均为 `contract_fixture` 且 `source_model_id=synthetic-*`。 | [clm-no-seed] |

## 3. 合同内容摘要

### 3.1 issue 状态

v0 schema 约束以下 `confirmation_status`：[clm-status-branches]

- `candidate_only`：可疑但不能修；典型 folded event / expression debt 默认停留在这里。
- `confirmed`：可作为后续 repair target；必须通过 `nl_grounded_behavioral_issue` 或 `raw_internal_inconsistency` 两条 evidence path 之一。
- `rejected_conversion_artifact`：问题来自 conversion / lowering / normalization，不是 source-level issue。
- `rejected_other`：已知不是本方法应修的问题，且必须保留非空 reason。
- `out_of_scope`：如 timed / hybrid 语义超出当前 paper1 headline。
- `insufficient_evidence`：NL 或 source evidence 不足，不能确认。

### 3.2 confirmed path

默认 confirmed path 是 `nl_grounded_behavioral_issue`：需要至少一条 `nl_requirement`、至少一条 `source_stm_fragment`，以及至少一条 inspect / simulation / probe / verification 类型的 typed behavior evidence 共同支撑。[clm-nl-path]

第二条 confirmed path 是 `raw_internal_inconsistency`：用于 raw/source STM 自身内部矛盾但不绑定明确 NL 句子的情况。v0 schema 要求 `nl_evidence=[]`、至少两个 source element、至少两个 source STM evidence、`source_internal_consistency_check` typed behavior evidence，并要求 rationale 明确说明 “NL evidence is not required”。[clm-raw-path]

该第二路径只是 v0 合同，不是最终 taxonomy。后续必须结合真实 raw NL 例子和 discovery 能力复核，尤其要防止 folded event / ugly expression 被自动升级为 confirmed issue。[clm-q11]

### 3.3 repair eligibility

后续 `PR-repair-runner` 不应接收泛化目标，只能接收 repair-eligible issue：[clm-repair-gate]

```text
confirmation_status == confirmed
and downstream_repair_allowed == true
and attribution_boundary.source_level_claim_allowed == true
```

非 confirmed issue 必须 `downstream_repair_allowed=false` 且 `confirmation_evidence_path=not_applicable`。[clm-repair-gate]

## 4. 学术风险与禁止主张

1. 不把 ledger / audit / bookkeeping 写成 paper1 贡献；它们只是方法与可复现纪律。[clm-nonclaims]
2. 不把 `fcstm` / `pyfcstm` 写成 paper1 contribution；paper1 贡献仍是 loop + diagnostics / simulation / formal-verification feedback integration。[clm-ledger-position]
3. 不把 folded event / expression debt 自动算作 confirmed behavioral issue。[clm-fixtures]
4. 不把 conversion / lowering artifact 计入 method discovered source-level issue 或 repair gain。[clm-fixtures]
5. 不把 synthetic fixture 写成真实 seed annotation 或真实实验结果。[clm-no-seed]
6. 不在 pilot 前冻结 final metric、baseline contract 或 judge prompt。[clm-nonclaims]

## 5. 后续入口

| 后续工作 | 依赖本合同的方式 |
|---|---|
| `PR-source-trace` | 接管 `source_element_refs` 与 `required_future_trace`，定义 raw/source ↔ intermediate representation trace。 |
| `PR-loop-io` | 将 issue ledger 放入 stage IO / run record 合同。 |
| `PR-discover-confirm` | 产生真实 candidate / confirmed issue ledger。 |
| `PR-repair-runner` | 只能修复 repair-eligible confirmed issue。 |
| `PR-closure-audit` | 以 `issue_id` 为单位判断 closed / partial / not closed / regression / unjudgeable。 |
| `PR-loop-pilot` 之后 | 基于真实 patch bundle / `STM_final` 冻结 final evaluation rubric 与 baseline contract。 |

## 审计附录：证据链与事实源

### A.1 来源考据表

| source path | source creation commit | prefix commit | substantive fact commit 判定理由 | non-prefix revision/migration commit | canonical machine source |
|---|---|---|---|---|---|
| `reports/2026-07-08-10-15-00-pr-issue-ledger-contract.md` | 本 PR 直接新增；可用 `git log --follow -- project_1_llm_state_machine_modeling/paper_stm_repair/reports/2026-07-08-10-15-00-pr-issue-ledger-contract.md` 复查首次提交。 | `2026-07-08 10:15:00 +0800` 为本合同报告冻结时间前缀。 | 本报告总结同一 PR 中新增的 issue lifecycle 文档、schema、fixture 与 pytest gate；不是旧 report 迁移。 | 后续若只修链接或措辞，不改变本报告冻结时间；若修改 schema / fixture 语义，必须新增日志或新报告。 | [source_issue_ledger.schema.json](../pipeline/evaluation/schemas/source_issue_ledger.schema.json), [source_issue_ledger fixtures](../pipeline/evaluation/fixtures/source_issue_ledger/), [test_source_issue_ledger_schema.py](../pipeline/evaluation/tests/test_source_issue_ledger_schema.py) |

> 本节只说明 report 的冻结与来源，不替代下面的 claim-evidence map。

### A.2 上游事实源清单

| 编号 / 引用键 | source_id | 事实源 | 类型 | 用途 | 关键锚点 |
|---|---|---|---|---|---|
| [src-issue-def] | `issue_lifecycle_definition` | [source_level_issue_definition.md](../experiment_design/issue_lifecycle/source_level_issue_definition.md) | `md` | 支撑 candidate / confirmed / rejected / out-of-scope / insufficient-evidence 术语与 Q11=A raw-internal path。 | §2--§6 |
| [src-ledger-contract] | `issue_ledger_contract` | [issue_ledger_contract.md](../experiment_design/issue_lifecycle/issue_ledger_contract.md) | `md` | 支撑字段语义与 repair eligibility gate。 | §3--§5 |
| [src-schema] | `source_issue_schema` | [source_issue_ledger.schema.json](../pipeline/evaluation/schemas/source_issue_ledger.schema.json) | `schema` | 机器可校验字段、enum、if/then gate、evidence path 与 attribution boundary。 | `$defs.issue`, `$defs.*_evidence_item`, `allOf[]` |
| [src-fixtures] | `source_issue_fixtures` | [source_issue_ledger fixtures](../pipeline/evaluation/fixtures/source_issue_ledger/) | `json` | 六个 synthetic contract fixture，覆盖 v0 分支。 | `*.json#/issues[0]` |
| [src-tests] | `source_issue_tests` | [test_source_issue_ledger_schema.py](../pipeline/evaluation/tests/test_source_issue_ledger_schema.py) | `source-code` | schema metaschema、fixture validation、负例 mutation、Markdown link check。 | `test_*` functions |
| [src-q11] | `q11_decision_comment` | [PR #150 Q11=A decision](https://github.com/HansBug/research_ideas/pull/150#issuecomment-4910649191) | `external_reference` | 支撑 raw-internal inconsistency 第二 confirmed path 的用户决策来源。 | comment body: Q11=A |

### A.3 Claim-evidence map

| 编号 / 引用键 | claim_id | 结论 / claim | 类型 | 上游事实源与锚点 | 复验命令 | 置信度 | 限制 / caveat |
|---|---|---|---|---|---|---|---|
| [clm-ledger-position] | ISSUE-LEDGER-C1 | 本合同服务 source-level issue discovery / repair / closure，不服务 Better STM headline。 | decision | [src-issue-def] §1, §4--§6；[src-ledger-contract] §1--§2。 | [cmd-residual-scan] | high | 只说明当前合同定位；不证明方法效果。 |
| [clm-status-branches] | ISSUE-LEDGER-C2 | v0 状态覆盖 candidate / confirmed / rejected conversion artifact / rejected other / out-of-scope / insufficient evidence。 | classification | [src-schema] `confirmation_status` enum；[src-issue-def] §2。 | [cmd-schema-tests] | high | enum 是 v0；后续 pilot 可扩展但不得破坏旧语义。 |
| [clm-schema] | ISSUE-LEDGER-C3 | source issue ledger v0 已有 JSON Schema。 | trace | [src-schema] whole file。 | [cmd-schema-tests] | high | 只是 schema contract，不是 runtime runner。 |
| [clm-fixtures] | ISSUE-LEDGER-C4 | 六个 synthetic fixture 覆盖主要合同分支。 | trace | [src-fixtures] six JSON files；[src-tests] fixture name set assertion。 | [cmd-schema-tests] | high | fixture 是 synthetic contract fixture，不是真实实验结果。 |
| [clm-repair-gate] | ISSUE-LEDGER-C5 | 只有 confirmed + repair_allowed + source-level attribution issue 能进入 repair。 | prohibition | [src-schema] `downstream_repair_allowed` inverse gate；[src-ledger-contract] §4。 | [cmd-schema-tests] | high | 后续 runner 仍需实现消费逻辑。 |
| [clm-nl-path] | ISSUE-LEDGER-C6 | `nl_grounded_behavioral_issue` 需要 NL / source STM / behavior evidence。 | classification | [src-schema] `confirmation_evidence_path=nl_grounded_behavioral_issue` branch；[src-fixtures] `confirmed_guard_mismatch.json`。 | [cmd-schema-tests] | high | behavior evidence 的具体生成由后续 PR 实现。 |
| [clm-raw-path] | ISSUE-LEDGER-C7 | `raw_internal_inconsistency` 作为第二 confirmed path 需要内部冲突证据和 source_internal_consistency_check。 | decision | [src-schema] raw-internal branch；[src-fixtures] `raw_internal_inconsistency_confirmed.json`。 | [cmd-schema-tests] | high | 该 path 是 v0；后续必须用真实 raw/NL 复核。 |
| [clm-q11] | ISSUE-LEDGER-C8 | 用户选择 Q11=A：允许 raw-internal inconsistency，但需后续结合真实样例复核。 | decision | [src-q11]；[src-issue-def] §3.2。 | 人工复验：打开 PR comment 与 definition 文档。 | high | GitHub comment 是流程事实源；长期语义已沉淀到 repo 文档。 |
| [clm-no-seed] | ISSUE-LEDGER-C9 | 本 PR 不标注真实 seed，不运行真实 LLM / repair，也不运行四个 selected examples。 | prohibition | [src-fixtures] `ledger_scope=contract_fixture`, `source_model_id=synthetic-*`；[src-tests] `test_fixtures_are_contract_fixtures_not_seed_or_archive_annotations`。 | [cmd-schema-tests] | high | 后续 pilot 可产生真实 ledger，但必须另有 run record。 |
| [clm-nonclaims] | ISSUE-LEDGER-C10 | 本报告不支持 method effectiveness、final metric、baseline 或 judge prompt claim。 | prohibition | [src-issue-def] §1；[src-ledger-contract] §1--§5；[src-tests] forbidden wording test。 | [cmd-residual-scan] | high | 只适用于本 PR 合同阶段。 |

### A.4 复验命令

| 编号 / 引用键 | 命令 | 用途 |
|---|---|---|
| [cmd-schema-tests] | `python -m pytest project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/evaluation/tests/test_source_issue_ledger_schema.py` | 校验 schema、fixtures、负例 mutation 与 Markdown links。 |
| [cmd-eval-tests] | `python -m pytest project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/evaluation/tests` | 运行 evaluation 测试目录。 |
| [cmd-pipeline-smoke] | `PYTHONPATH=project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/readiness_audit/src:project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/representation/src:project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/conversion/src python -m pytest project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/conversion/tests project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/representation/tests project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/readiness_audit/tests project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/evaluation/tests` | 运行 conversion / representation / readiness / evaluation 组合 smoke。 |
| [cmd-residual-scan] | `rg -n "can_claim_better_stm|which STM is better|blind adjudication|method effectiveness" project_1_llm_state_machine_modeling/paper_stm_repair/experiment_design/issue_lifecycle project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/evaluation project_1_llm_state_machine_modeling/paper_stm_repair/reports/2026-07-08-10-15-00-pr-issue-ledger-contract.md || true` | 检查 active issue-ledger 合同路径中是否混入旧 Better STM endpoint 或方法效果 claim。 |
