# 2026-07-07 post-strategy asset scan — PR-asset-map 扫描审计报告

## 0. 审计目的

本报告记录 PR-asset-map 的静态扫描证据，用于支撑 [../ledgers/paper1_strategy_asset_map.md](../ledgers/paper1_strategy_asset_map.md) 中的 `active / update / archive / historical` 决策。

审计边界：

- 本报告只做静态扫描、事实源核验和代表性命中归类。
- 不移动文件、不改 runner / prompt / schema / run record、不跑正式实验。
- 不把 R5.7 constructed `STM_k` dry-run 或 blind adjudication 输出写成方法效果。

## 1. 环境与事实源状态

| item | observed result |
|---|---|
| 当前日期 | 2026-07-07 |
| working branch | `paper1/pr-asset-map` |
| upstream base | `paper1/better-stm-repair-loop-umbrella` |
| upstream merge check | `git merge --no-edit origin/paper1/better-stm-repair-loop-umbrella` 返回 `Already up to date.` |
| #147 state | open; base=`paper1/better-stm-repair-loop-umbrella`; head=`paper1/pr-asset-map`; mergeStateStatus=`CLEAN`（扫描前查询） |
| #100 state | open; mergeStateStatus=`CLEAN`（扫描前查询） |
| #146 state | merged |
| #145 state | closed / `[SUPERSEDED]`; close comment: <https://github.com/HansBug/research_ideas/issues/145#issuecomment-4902595854> |
| `paper_v1/` | exists |
| `AGENTS.md` | symlink / same realpath as `CLAUDE.md`；ledger 去重 |

GitHub 动态事实源角色：

| source | role in this audit |
|---|---|
| [#100](https://github.com/HansBug/research_ideas/pull/100) | active umbrella truth；`PR-asset-map` 字段、范围和 downstream map 来源。 |
| [#146](https://github.com/HansBug/research_ideas/pull/146) | strategic source；导师讨论战略校准已合入。 |
| [#145](https://github.com/HansBug/research_ideas/issues/145) + [close comment](https://github.com/HansBug/research_ideas/issues/145#issuecomment-4902595854) | superseded historical context only；不得作为 active R6 source。 |

## 2. 扫描命令

### 2.1 Primary risk scan

```bash
rg -n \
  "Better STM|BetterSTM|which STM is better|STM_k|stmk|repair_target|adjudication|fcstm.*contribution|conversion gain" \
  project_1_llm_state_machine_modeling/paper_stm_repair \
  project_1_llm_state_machine_modeling/method \
  project_1_llm_state_machine_modeling/eval \
  project_1_llm_state_machine_modeling/discussions \
  project_1_llm_state_machine_modeling/talks \
  project_1_llm_state_machine_modeling/paper_v1 \
  TARGET.md CLAUDE.md AGENTS.md
```

Result summary:

| metric | value |
|---|---:|
| pre-write commit | `328907b958639bce5911752c4dd75da96ef2a93a` |
| matched lines | 10740 before writing this ledger/audit; 10808 when re-run after these new evidence files are present |
| unique files | 813 before writing this ledger/audit; 818 when re-run after these new evidence files are present |

### 2.2 Secondary broad scan

```bash
rg -n "better|adjudication|judge|rubric|repair target|closure|regression|raw STM|source-level|patch bundle" \
  project_1_llm_state_machine_modeling/paper_stm_repair \
  project_1_llm_state_machine_modeling/paper_v1
```

Result summary:

| metric | value |
|---|---:|
| pre-write commit | `328907b958639bce5911752c4dd75da96ef2a93a` |
| matched lines | 16510 before writing this ledger/audit; 16565 when re-run after these new evidence files are present |
| unique files | 796 before writing this ledger/audit; 801 when re-run after these new evidence files are present |

## 3. 命中分布摘要

### 3.1 Primary risk scan top groups

| group | matched lines | unique files | interpretation |
|---|---:|---:|---|
| `paper_stm_issue_discover/pipeline/evaluation` | 9593 | 658 | R5.7.5 constructed / blind adjudication artifacts 高度集中，应由 `PR-better-archive` 处理。 |
| `paper_stm_issue_discover/experiment_design/better_adjudication_dry_run` | 114 | 22 | 20 个 constructed cases 与 suite index，archive。 |
| `paper_stm_issue_discover/pipeline/representation` | 113 | 13 | `.fcstm` / converted bundle 可保留为 infrastructure，但需防止 conversion gain。 |
| `project_1_llm_state_machine_modeling/talks` | 89 | 4 | 2026-07-07 记录为 active strategic；2026-06-12 Better STM 口径部分 superseded。 |
| `paper_stm_issue_discover/experiment_design/repair_target_adjudication` | 71 | 5 | R5.7.4 static adjudication，archive。 |
| `paper_stm_issue_discover/experiment_design/metrics` | 69 | 2 | objective metric framework 围绕 Better STM，archive。 |
| `paper_stm_issue_discover/STATUS.md` | 7 | 1 | 顶层状态表仍有 R5.7 / Better STM active-style 行，`PR-story-reset` 必须改写。 |
| `paper_stm_issue_discover/pipeline/readiness_audit` | 67 | 5 | readiness / handoff 有价值但需从旧 R6 wording 改为 issue lifecycle。 |
| `method/` | 26 | 9 | `repair_target` 多为 runtime field；active infra，不等于 R5.7 taxonomy。 |
| `paper_v1/` | 5 | 3 | 旧 Path-1/Path-2 与 pyfcstm contribution wording，historical。 |

### 3.2 Secondary broad scan top groups

| group | matched lines | unique files | interpretation |
|---|---:|---:|---|
| `paper_stm_issue_discover/pipeline/evaluation` | 12209 | 634 | judge manifests / blind outputs / Better checklist 仍为最大旧框架集中区。 |
| `paper_stm_issue_discover/pipeline/conversion` | 3094 | 10 | conversion recovery JSON 命中 broad keywords；可 active，但要保留非 contribution 归因。 |
| `paper_stm_issue_discover/corpora/seed_library` | 141 | 30 | seed provenance active；不支撑 method effectiveness。 |
| `paper_stm_issue_discover/experiment_design/metrics` | 127 | 2 | old objective metrics archive。 |
| `paper_stm_issue_discover/reports/2026-07-05-07-18-31-r5-7-5-full-blind-adjudication-dry-run.md` | 106 | 1 | full blind adjudication report，archive。 |
| `paper_v1/` | 31 | 3 | old judge / pyfcstm / contribution / Path comparison wording，historical。 |

## 4. 代表性命中与判读

| representative hit | risk | asset-map decision |
|---|---|---|
| `paper_v1/README.md` 仍写 “`<NL, STM_0> -> STM_k / Better STM` 的无人化反馈驱动状态机修正任务”。 | 旧主线入口可能被误读为 active。 | A-022 `historical`，由 `PR-story-reset` 防止旧 headline 回流。 |
| `talks/2026-07-07-...md` 明确 “Better STM 不再作为 paper1 active headline evaluation framework”。 | 这是覆盖旧口径的战略锚点。 | A-002 `active`。 |
| `paper_stm_issue_discover/STATUS.md` R5.7.2 / R5.7.4 / R5.7.5 行仍为 active-style 状态表。 | 顶层入口会继续把旧协议当当前状态。 | A-004 `update`；R5.7 资产由 A-006--A-013 `archive`。 |
| `experiment_design/quality_model/better_stm_definition.md` 与 `repair_target_taxonomy.md`。 | 旧 Better STM framework 核心资产。 | A-006 `archive`。 |
| `experiment_design/protocols/better_adjudication_*`。 | blind adjudication prompt/schema 可能被误作 source-level closure judge。 | A-008 `archive`；后续 `PR-eval-rubric` 只读借鉴。 |
| `pipeline/evaluation/dry_run_examples/r5_7_5_*` 下大量 judge outputs。 | constructed `STM_k` 和 LLM judge dry-run 容易被误报成 method effectiveness。 | A-012 `archive`。 |
| `pipeline/conversion/**` 命中 `source-level` / `conversion` / `Better STM`。 | conversion success 可能被误算成 method gain。 | A-014 `active` with attribution boundary。 |
| `pipeline/representation/**` 和 `selected_seed_examples/**`。 | `.fcstm` / lowering 可能被写成 contribution。 | A-015 `active` as intermediate medium only。 |
| `method/**` 命中 `repair_target`。 | runtime field 与 R5.7 taxonomy 同名，可能混淆。 | A-019 `active` shared runtime；后续 `PR-loop-io` 解释字段语义。 |
| `CLAUDE.md` 与 `AGENTS.md` realpath 相同。 | 若逐文件入表会重复仓库级规则资产。 | A-023 去重为同一逻辑资产。 |

## 5. `paper_v1/` 专项记录

`paper_v1/` 当前存在，并在两组扫描中命中：

| scan | matched lines | unique files | files |
|---|---:|---:|---|
| primary | 5 | 3 | `README.md`, `PATH1_HARD_COMPARISON_GUIDE.md`, `PATH2_DIFFERENTIATION_GUIDE.md` |
| secondary | 31 | 3 | `README.md`, `PATH1_HARD_COMPARISON_GUIDE.md`, `PATH2_DIFFERENTIATION_GUIDE.md` |

判读：`paper_v1/` 是旧 Path-1 / Path-2 / hard comparison / pyfcstm contribution / judge 口径工作区。它可作为 historical context，但不能成为当前 story 或 method contribution 真源。

## 6. `CLAUDE.md` / `AGENTS.md` 去重记录

```bash
readlink -f CLAUDE.md
readlink -f AGENTS.md
```

Observed realpath:

```text
/home/zhangshaoang/oo-projects/research_ideas/CLAUDE.md
/home/zhangshaoang/oo-projects/research_ideas/CLAUDE.md
```

结论：`AGENTS.md` 是 `CLAUDE.md` 的软链接。本轮 ledger 不重复建立两个资产行，统一记为 A-023；后续若需修改仓库级规则，只修改 `CLAUDE.md`。

## 7. 审计结论

1. R5.7 / Better STM-facing 资产实际覆盖面很大，尤其集中在 `experiment_design/quality_model`、`experiment_design/protocols`、`experiment_design/better_adjudication_dry_run`、`pipeline/evaluation/dry_run_examples/r5_7_5_*` 和 R5.7 reports；后续必须由 `PR-better-archive` 全量迁入 archive snapshot。
2. 顶层 `paper_stm_issue_discover` root docs 与 `story/` 仍有旧 framing，必须先由 `PR-story-reset` 改成 source-level issue discovery / closure。
3. conversion / representation / readiness / method runtime 仍是后续链路必要基础，但必须加 attribution boundary：它们是 intermediate representation infrastructure，不是 paper1 contribution 或 repair gain。
4. `paper_v1/` 和旧 `discussions/` 是 historical context，不能恢复旧 hard comparison、pyfcstm contribution 或 judge-centric 主线。
5. #145 已关闭为 superseded historical context；后续不得从 #145 body 直接继承 active R6 计划。

## 8. 复验命令清单

```bash
git status --short --branch
git merge --no-edit origin/paper1/better-stm-repair-loop-umbrella

gh pr view 147 --json number,state,baseRefName,headRefName,mergeStateStatus,url
gh pr view 100 --json number,state,mergeStateStatus,url
gh pr view 146 --json number,state,mergedAt,url
gh issue view 145 --json number,state,title,url

rg -n "Better STM|BetterSTM|which STM is better|STM_k|stmk|repair_target|adjudication|fcstm.*contribution|conversion gain" \
  project_1_llm_state_machine_modeling/paper_stm_repair \
  project_1_llm_state_machine_modeling/method \
  project_1_llm_state_machine_modeling/eval \
  project_1_llm_state_machine_modeling/discussions \
  project_1_llm_state_machine_modeling/talks \
  project_1_llm_state_machine_modeling/paper_v1 \
  TARGET.md CLAUDE.md AGENTS.md

rg -n "better|adjudication|judge|rubric|repair target|closure|regression|raw STM|source-level|patch bundle" \
  project_1_llm_state_machine_modeling/paper_stm_repair \
  project_1_llm_state_machine_modeling/paper_v1

readlink -f CLAUDE.md AGENTS.md
```
