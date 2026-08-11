# paper1_strategy_asset_map.md — 战略转向后的资产清账地图

## 0. 定位

本文件是 PR-asset-map 的主资产地图，服务于 2026-07-07 导师讨论后的 paper1 战略转向：从 `Better STM / which STM is better` 主框架，转到 **source-level behavioral issue discovery and closure** 主线。

本资产地图只回答三件事：

1. 现有资产现在应当保留、改写、归档，还是只作为历史证据。
2. 后续哪个 `PR-<short-slug>` 应处理它。
3. 如何复验该判断没有遗漏上游事实源或风险关键词。

本文件不移动文件、不重写 story、不修改 runner / prompt / schema / run record，也不报告方法效果。

## 1. 上游事实源与优先级

| source | status | role | 使用纪律 |
|---|---|---|---|
| [#100 umbrella PR](https://github.com/HansBug/research_ideas/pull/100) | open / active | active umbrella truth；后续 `PR-<short-slug>` map 与本 PR 字段合同来源。 | 后续动态进展仍写 #100 body/comment；仓库文件只沉淀长期事实。 |
| [#146 mentor strategic PR](https://github.com/HansBug/research_ideas/pull/146) | merged | strategic source；2026-07-07 导师讨论与会后施工决策来源。 | 覆盖 2026-06-12 Better STM active framework，但保留其“已有模型反馈修正 / 弱化 DSL”背景。 |
| [#145 superseded issue](https://github.com/HansBug/research_ideas/issues/145) + [close comment](https://github.com/HansBug/research_ideas/issues/145#issuecomment-4902595854) | closed / superseded | historical context only；旧 R6 / hot-start / `<NL, STM_0> -> STM_k` 计划。 | 来自 #145 的资产默认只能标 `historical`；若需迁移，必须由 #100 / #146 / 后续新 ledger 重新确认。 |
| [2026-07-07 导师记录](../../../../talks/2026-07-07-导师-paper1发现修正与BetterSTM归档.md) | active strategic record | 当前最高优先级导师讨论落库记录。 | `fcstm` 只作中间语义执行介质；Better STM-facing 资产后续全量归档。 |
| [2026-06-12 导师记录](../../../../talks/2026-06-12-导师-两篇论文转向与模型修正定调.md) | partially superseded | 历史转向来源：从 `NL -> STM` 转到已有模型反馈修正。 | 其中 `<NL, STM_0> -> STM_k / Better STM` active 口径已被 2026-07-07 记录覆盖。 |

## 2. decision 口径

| decision | 含义 | 典型下游 |
|---|---|---|
| `active` | 与 source-level issue lifecycle 主线一致，可保留为当前事实源或基础设施入口。 | 后续 PR 可直接引用，但仍要避免贡献归因漂移。 |
| `update` | 有价值但旧 wording 或结构仍指向 Better STM / generic repair，需要改写。 | `PR-story-reset`、`PR-issue-ledger`、`PR-source-trace`、`PR-loop-io`。 |
| `archive` | 主要服务 Better STM / constructed `STM_k` / adjudication dry-run / repair target framework，留在主路径会误导。 | `PR-better-archive`。 |
| `historical` | 只作为历史证据、PR 施工记录或 superseded 背景保留，不进入 active 方法。 | archive index 或只读 provenance。 |

特殊纪律：conversion / normalization / lowering 可作为 `active` infrastructure，但不能计入 method gain 或 paper1 contribution；folded event / ugly expression 只能是 candidate symptom，不能自动升级为 confirmed source-level issue。

## 3. 资产总账

> 字段按 #100 §4.1 合同保留：`path_or_issue`、`current_role`、`decision`、`reason`、`upstream_pr_or_source`、`downstream_pr`、`required_action`、`link_cleanup_needed`、`verification_command`。本表额外使用 `asset_id`、`asset_type`、`risk_keyword` 方便后续追踪。

| asset_id | path_or_issue | asset_type | current_role | risk_keyword | decision | reason | upstream_pr_or_source | downstream_pr | required_action | link_cleanup_needed | verification_command |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | [#100](https://github.com/HansBug/research_ideas/pull/100) | PR body | active umbrella truth | active map | active | 当前唯一伞 PR，总控 `PR-<short-slug>` map 与验收门。 | #100 | all downstream | 持续在 PR body/comment 同步动态进展；长期事实再落仓库。 | no | `gh pr view 100 --json state,mergeStateStatus,body` |
| A-002 | [#146](https://github.com/HansBug/research_ideas/pull/146) + [2026-07-07 导师记录](../../../../talks/2026-07-07-导师-paper1发现修正与BetterSTM归档.md) | mentor talk / PR | strategic source | Better STM archived; fcstm medium | active | 已合入的战略校准，覆盖旧 Better STM 主框架；对 `PR-issue-ledger` 只提供 confirmed issue 的定义纪律，不提供 issue 数据源。 | #146 | `PR-story-reset` / `PR-better-archive` / `PR-issue-ledger` | 后续 story 与方法协议必须引用此战略来源；后续 story 引用本记录时必须转述为 source-level issue discovery / closure 口径，而非 Better STM 口径。 | yes | `gh pr view 146 --json state,mergedAt`; `rg -n "source-level\|Better STM" ../../../talks/2026-07-07-导师-paper1发现修正与BetterSTM归档.md` |
| A-003 | [#145](https://github.com/HansBug/research_ideas/issues/145) + [close comment](https://github.com/HansBug/research_ideas/issues/145#issuecomment-4902595854) | issue | superseded R6 planning context | hot-start; Better STM; STM_k | historical | 已关闭并标 `[SUPERSEDED]`，不能再作为 active 施工真源。 | #145 close comment | archive index / optional planning reference | 只保留为 historical；若迁移 discipline，必须由新 PR 重新确认。 | no | `gh issue view 145 --json state,title,body,comments` |
| A-004 | [paper_stm_repair root docs](../../../README.md), [SUMMARY.md](../../../SUMMARY.md), [STATUS.md](../../../STATUS.md), [GUIDE.md](../../../GUIDE.md) | root docs | active 入口但仍含 R5.7 / Better STM 旧口径 | Better STM; repair target; STM_k | update | 顶层入口仍直接链接 Better STM gate、R5.7.4/5 dry-run 与旧 R6 修正循环描述。 | #100 / #146 / scan | `PR-story-reset` | 重写为 source-level issue discovery / closure；保留历史 PR 但改为 superseded / archive link。 | yes | `rg -n "Better STM\|STM_k\|repair target\|R5.7" ../../README.md ../../SUMMARY.md ../../STATUS.md ../../GUIDE.md` |
| A-005 | [story/](../../r8_discover_repair_story/story/) | story / outline / claims | 旧 paper story、claim-evidence 与 terminology | Better STM; relatively better STM; repair effectiveness | update | 仍把 `<NL, STM_0> -> STM_k` 与 Better STM 作为中心 evidence framing。 | R5.6 / R5.7 / #146 | `PR-story-reset` | 全面重写 thesis、contribution、claims-to-avoid、terminology 到 issue lifecycle。 | yes | `rg -n "Better STM\|relatively better\|STM_k\|repair target" ../../story` |
| A-006 | [experiment_design/quality_model/](../../r5_7_better_stm_snapshot/experiment_design/quality_model/) | quality model / taxonomy | Better STM definition 与 repair target taxonomy | better_stm_definition; repair_target_taxonomy | archive | 用户明确要求 Better STM-facing 资产全部归档；该目录是旧主框架核心。 | R5.7 / #146 | `PR-better-archive` | 迁入 `archive/r5_7_better_stm_snapshot/` 并保留 path mapping。 | yes | `find ../../archive/r5_7_better_stm_snapshot/experiment_design/quality_model -maxdepth 1 -type f -print` |
| A-007 | [experiment_design/metrics/objective_metric_framework.md](../../r5_7_better_stm_snapshot/experiment_design/metrics/objective_metric_framework.md) | metrics | R5.7 objective metric framework | objective metric; Better STM; Acc | archive | 指标围绕 Better STM 判定与旧 objective score；新 rubric 要等 pilot 后另冻。 | R5.7.3 / #146 | `PR-better-archive`; later `PR-eval-rubric` | 归档；若有可复用 no-regression discipline，后续从 archive 显式迁移。 | yes | `rg -n "Better STM\|objective\|Acc\|closure\|regression" ../../archive/r5_7_better_stm_snapshot/experiment_design/metrics/objective_metric_framework.md` |
| A-008 | [experiment_design/protocols/](../../r5_7_better_stm_snapshot/experiment_design/protocols/) | prompt / schema / protocol | Better adjudication prompt 与 blind output schema | adjudication; judge; rubric | archive | 主要服务 Better STM adjudication dry-run；新 source-level closure judge 需另建。 | R5.7.5 / #146 | `PR-better-archive`; later `PR-eval-rubric` | 归档为 calibration-only，不在主路径作为 active judge prompt。 | yes | `find ../../archive/r5_7_better_stm_snapshot/experiment_design/protocols -maxdepth 1 -type f -name '*adjudication*' -print` |
| A-009 | [experiment_design/better_adjudication_dry_run/](../../r5_7_better_stm_snapshot/experiment_design/better_adjudication_dry_run/) | dry-run cases | 20 个 constructed `STM_k` anti-gaming / blind judge 校准案例 | constructed STM_k; expected better; protocol invalid | archive | constructed cases 不是真实 repair-loop 输出；继续留在主路径会误导 effectiveness。 | R5.7.5 / #146 | `PR-better-archive` | 全量迁入 archive snapshot；保留 suite index 与 leakage / anti-gaming 说明。 | yes | `find ../../archive/r5_7_better_stm_snapshot/experiment_design/better_adjudication_dry_run -maxdepth 1 -type f \| wc -l` |
| A-010 | [experiment_design/repair_target_adjudication/](../../r5_7_better_stm_snapshot/experiment_design/repair_target_adjudication/) | static adjudication | 四例 R5.7.4 static finding | repair target; static adjudication | archive | 只证明 taxonomy / metric consumption 能执行，不产出真实 `STM_k` 或 method result。 | R5.7.4 / #146 | `PR-better-archive` | 归档；可在后续 reference issue work 中只读借鉴风险类型。 | yes | `rg -n "repair target\|Better STM\|valid_run\|STM_k" ../../archive/r5_7_better_stm_snapshot/experiment_design/repair_target_adjudication` |
| A-011 | [experiment_design/evaluation_logic.md](../../r5_7_better_stm_snapshot/experiment_design/evaluation_logic.md), [experiment_design/eligibility/](../../r5_7_better_stm_snapshot/experiment_design/eligibility/), [pipeline/evaluation/schemas/better_stm_checklist.schema.json](../../r5_7_better_stm_snapshot/pipeline/evaluation/schemas/better_stm_checklist.schema.json) | gate / schema | 旧 Better STM gate、eligibility 与 checklist schema | can_claim_better_stm; gate; eligibility | archive | 旧 gate 与新 closure/regression verdict 不同；不能用 `can_claim_better_stm` 当 active endpoint。 | R4 / R5.7 / #146 | `PR-better-archive`; later `PR-eval-rubric` | Better checklist 归档；diagnostic/scenario schema 若迁移须改成 issue lifecycle 字段。 | yes | `rg -n "can_claim_better_stm\|better_stm\|Better STM" ../../archive/r5_7_better_stm_snapshot/pipeline/evaluation/schemas ../../archive/r5_7_better_stm_snapshot/experiment_design/evaluation_logic.md` |
| A-012 | [pipeline/evaluation/dry_run_examples/r5_7_5_constructed_stmk/](../../r5_7_better_stm_snapshot/pipeline/evaluation/dry_run_examples/r5_7_5_constructed_stmk/) and [r5_7_5_blind_adjudication/](../../r5_7_better_stm_snapshot/pipeline/evaluation/dry_run_examples/r5_7_5_blind_adjudication/) | dry-run artifacts / judge outputs | constructed `STM_k` bundle、blind prompt、Claude / Codex / DeepSeek outputs | STM_k; blind adjudication; judge outputs | archive | 大量命中来自 R5.7.5 blind dry-run；只能作 calibration / leakage check。 | R5.7.5 / #146 | `PR-better-archive` | 全量归档；主路径只保留 archive index。 | yes | `find ../../archive/r5_7_better_stm_snapshot/pipeline/evaluation/dry_run_examples -maxdepth 2 -type d -name 'r5_7_5*' -print` |
| A-013 | [reports/2026-07-02...R5.7.1](../../r5_7_better_stm_snapshot/reports/2026-07-02-17-02-42-r5-7-1-evaluation-logic.md), [R5.7.2](../../r5_7_better_stm_snapshot/reports/2026-07-03-02-16-16-r5-7-2-better-stm-target-contract.md), [R5.7.3](../../r5_7_better_stm_snapshot/reports/2026-07-03-21-18-25-r5-7-3-objective-metric-framework.md), [R5.7.4](../../r5_7_better_stm_snapshot/reports/2026-07-03-23-44-12-r5-7-4-static-adjudication-dry-run.md), [R5.7.5 constructed](../../r5_7_better_stm_snapshot/reports/2026-07-05-02-10-39-r5-7-5-constructed-stmk-coverage-dry-run.md), [R5.7.5 blind](../../r5_7_better_stm_snapshot/reports/2026-07-05-07-18-31-r5-7-5-full-blind-adjudication-dry-run.md) | reports | R5.7 reporting chain | Better STM; adjudication; constructed STM_k | archive | 报告是历史证据，但不应作为 active method/eval report 入口。 | R5.7 / #146 | `PR-better-archive` | 归档并在 archive README 说明“不证明 repair effectiveness”。 | yes | `ls ../../archive/r5_7_better_stm_snapshot/reports/*r5-7* ../../archive/r5_7_better_stm_snapshot/reports/*R5-7* 2>/dev/null` |
| A-014 | [pipeline/conversion/](../../../pipeline/conversion/) | conversion infra | raw / PlantUML 到 canonical / recovery / normalization 基础设施 | conversion gain; lowering | active | conversion 是中间表示 infrastructure；已明确不能算 method gain / contribution。 | R3 / R4.5 / #100 | `PR-source-trace` / `PR-loop-io` | 保留；在 story 中明确 attribution boundary，后续 trace 需记录 source hash 与 mapping。 | maybe | `rg -n "conversion gain\|Better STM\|eligibility\|source-level" ../../pipeline/conversion` |
| A-015 | [pipeline/representation/](../../../pipeline/representation/) and [selected_seed_examples/](../../../selected_seed_examples/) | representation / fcstm bundles | `.fcstm` 表示桥、四例 selected smoke bundle | fcstm; lowering; STM_0 | active | 作为 executable medium 保留；不得写成 paper1 contribution 或 repair gain。R5.7.4 adjudication-only standalone bundles 已随 `PR-better-archive` 迁入 [archive snapshot](../../r5_7_better_stm_snapshot/pipeline/representation/reports/)。 | R4.5 / #146 | `PR-source-trace` / `PR-raw-export` | 保留 active R4.5 selected-smoke 输入/转换 bundle；后续若复用 archived `0001/0018`，必须重新登记 source trace 与 attribution。 | maybe | `rg -n "fcstm\|Better STM\|conversion\|r5_7_4_adjudication" ../../pipeline/representation ../../selected_seed_examples` |
| A-016 | [pipeline/readiness_audit/](../../../pipeline/readiness_audit/) | readiness / manifest / handoff | 60-pair matrix、seed sweep、R5/R6/R7 handoff | r5_to_r6; eligibility; repair inputs | update | 仍有旧 R6 / eligibility wording；但 matrix / provenance 对 pilot 与 protocol 很重要。 | R5 / #100 / #146 | `PR-loop-pilot` / `PR-exp-protocol` | 保留 manifest 与 provenance；改写 handoff 到 issue lifecycle，不生成正式 main result eligibility。 | maybe | `rg -n "R6\|Better STM\|repair\|eligibility\|STM_k" ../../pipeline/readiness_audit` |
| A-017 | [corpora/seed_library/](../../../corpora/seed_library/), [corpora/nl_datasets/](../../../corpora/nl_datasets/) | corpus / seed provenance | seed / NL source 当前事实源 | seed; source; llms-emp | active | 与新主线一致：提供 `NL + raw/source STM_0` 来源，不评价方法效果。 | R1-R5 / #100 | `PR-exp-protocol` | 保留；正式样本分母等 protocol 冻结后再定。 | no | `rg -n "Better STM\|STM_k\|repair" ../../corpora/seed_library ../../corpora/nl_datasets` |
| A-018 | [corpora/repair_baselines/](../../../corpora/repair_baselines/) | related work / baseline corpus | repair / generation-era baseline 候选 | baseline; repair baseline | update | baseline 角色需按 issue discovery / known issue repair / black-box 三层重解释。 | R1 / #146 | `PR-baseline-contract` | 暂不冻结；等 pilot 输出后重建 baseline 合同。 | maybe | `rg -n "Better STM\|repair\|baseline\|judge" ../../corpora/repair_baselines` |
| A-019 | [method/](../../../../archive/agent_loop_method/) | shared runtime / agent loop | 现有 agent loop、stage facade、repair prompt、run record | repair_target; pyfcstm contribution | active | 共享 runtime 是后续实现基础；`repair_target` 字段多为实现概念，不等同 R5.7 taxonomy；`pyfcstm` / shared StageId / runtime 能力不能写成 paper1 contribution 或 method gain。 | method infra / #100 | `PR-loop-io` / `PR-discover-confirm` / `PR-repair-runner` | 保留；新增 paper1 overlay 不应重定义 shared StageId。 | no | `rg -n "repair_target\|fcstm.*contribution\|Better STM\|STM_k" ../../../method` |
| A-020 | [eval/](../../../../archive/path1_evaluation/) | legacy eval / judge infra | 早期评审、annotation 与 report 基础设施 | judge; rubric; pyfcstm contribution | historical | 主要服务旧 Path / judge / intrinsic evaluation；不是当前 paper1 active fact source。 | paper_v1 / old sprint | `PR-story-reset` / maybe `PR-eval-rubric` | 只读参考；若复用 judge infra，后续 PR 明确 adapter 与 leakage 规则。 | maybe | `rg -n "judge\|rubric\|pyfcstm\|contribution\|Better STM" ../../../eval` |
| A-021 | [discussions/](../../../../discussions/) | discussion notes | 旧 AI 讨论、pyfcstm 定位、agent-loop sprint 记录 | pyfcstm contribution; Path 1 lift | historical | 讨论材料优先级低于正式导师记录；不能直接作为 active story。 | old discussions / #146 | `PR-story-reset` | 只抽取风险与历史动机，不继承旧 contribution wording。 | maybe | `rg -n "pyfcstm.*contribution\|Better STM\|STM_k\|Path 1\|lift" ../../../discussions` |
| A-022 | [paper_v1/](../../../../archive/path1_path2_guides/) | legacy paper workspace | 早期 Path-1 / Path-2 hard comparison 与 differentiation guides | NL -> STM; pyfcstm contribution; judge | historical | 该目录 README 已标旧工作区；仍含旧贡献和 judge 规划，不能进入 active 主线。 | old path / #100 | `PR-story-reset` / archive index | 在入口保留 historical 标记；新 story 不从这里继承 headline。 | maybe | `rg -n "Better STM\|STM_k\|pyfcstm\|judge\|contribution" ../../../paper_v1` |
| A-023 | [TARGET.md](../../../../../TARGET.md), [CLAUDE.md](../../../../../CLAUDE.md) / [AGENTS.md](../../../../../AGENTS.md) | root docs | project_1 / paper1 相关仓库级导航与规则 | project_1; Path-1/Path-2 framing; repair; pyfcstm | update | `AGENTS.md` 是 `CLAUDE.md` 软链接；只清 project_1 / paper1 相关段落，避免仓库级规则噪声；当前风险主要是旧 Path-1 / Path-2 与 pyfcstm 定位，不是 CLAUDE.md 内存在 Better STM 字面命中。 | root docs / #100 | `PR-story-reset` | 如需更新，只改 `CLAUDE.md`；同步导航到新 story / archive 口径。 | maybe | `cd ../../../../ && readlink -f CLAUDE.md AGENTS.md`; `rg -n "project_1\|Path-1\|Path-2\|STM_k\|paper1\|repair\|pyfcstm" ../../../../TARGET.md ../../../../CLAUDE.md` |
| A-024 | [evidence/](../../../evidence/README.md) and this ledger | evidence index / asset map | 历史审计入口 + 本轮战略清账入口 | asset map; audit | active | 本 PR 新增长期清账事实；不是动态 PR 进度。 | #147 | all downstream | 后续 `PR-story-reset` / `PR-better-archive` 必须先读本 ledger 与 audit。 | no | `test -f ./paper1_strategy_asset_map.md && test -f ../audits/2026-07-07-post-strategy-asset-scan.md` |

## 4. 下游 PR 聚合视图

> `PR-better-archive` 执行后，A-006--A-013 以及 A-015 中的 R5.7.4 adjudication-only 表示 bundle 已改指 cold archive snapshot；这些行的 `decision=archive` 或 archive note 保留为历史决策标签，表示“当前状态为 archived historical”，不再表示待处理。


GitHub `key comments` 只包括改变战略事实、关闭 / supersede 旧源、处理 C/I、或更新 active PR map 的 comment；普通 review chatter 不进入 asset ledger。当前本表只把 #145 close comment 作为独立关键 comment URL，其余长期战略事实回到 #100 / #146 body 与已落库导师记录。

| downstream_pr | should consume | 最小动作 |
|---|---|---|
| `PR-story-reset` | A-004, A-005, A-018, A-021, A-022, A-023 | 重写 story / outline / claims / terminology / root entry，删除 active Better STM headline。 |
| `PR-better-archive` | A-006--A-013, A-015/R5.7.4 adjudication-only bundles, and relevant R5.7 links from A-004/A-005 | 已执行全量迁移到 [../../archive/r5_7_better_stm_snapshot/](../../r5_7_better_stm_snapshot/)，后续只保留 index 与 path mapping。 |
| `PR-issue-ledger` | A-002 as strategic calibration only; A-011 as archive reference only; A-016, A-017 | 新建 candidate / confirmed issue ledger；A-002 只提供“什么可算 confirmed issue”的纪律来源，不从导师记录中抽取 issue 数据，不复用 Better STM verdict。 |
| `PR-source-trace` | A-014, A-015, A-019 | 建立 raw/source ↔ intermediate trace、patch/projection placeholder 与 attribution boundary。 |
| `PR-loop-io` | A-014--A-016, A-019 | 冻结最小 stage IO、run record、failure/partial 状态与 secret redaction。 |
| `PR-discover-confirm` | A-017, A-019; A-011 as archive/negative reference only | 实现 discovery + strict confirmation 时复用 source / runtime 入口；旧 Better STM gate 只作反例，不能作为 active endpoint。 |
| `PR-repair-runner` | A-014, A-015, A-019 | 实现 issue-grounded repair 时保留 conversion / representation / runtime 的非贡献归因，不把修复写成 generic Better STM generation。 |
| `PR-raw-export` | A-014, A-015, A-019 | 未来由独立 post-Confirm semantic-root bundle 全量生成 fresh canonical raw/source `STM_k`；必须保留 accepted change、semantic-root correspondence 与 unsupported export 记录，不采用 textual minimal patch。 |
| `PR-loop-pilot` | A-016, A-017, A-024 | 用 readiness / provenance 与本 ledger 作为 pilot 输入选择和风险清单；pilot 只作 calibration，不作 headline result。 |
| `PR-eval-rubric` | A-007, A-008, A-011, A-012, A-013 as archive references only | 基于 pilot 真实输出重新冻结 closure/regression rubric；旧 prompt 只作反例 / calibration source。 |
| `PR-baseline-contract` | A-018; A-020, A-022 as historical/negative references only | 等 pilot 后冻结三层 baseline；旧 eval / paper_v1 只说明哪些 hard comparison 或 judge 口径不应复用。 |
| `PR-exp-protocol` | A-016, A-017, A-018, A-024 | 正式实验协议只能继承 provenance / baseline corpus / 清账结论；不把 R5/R6 readiness eligibility 当正式主结果分母。 |

## 5. 复验摘要

本 ledger 对应扫描审计：[../audits/2026-07-07-post-strategy-asset-scan.md](../../../evidence/audits/2026-07-07-post-strategy-asset-scan.md)。关键结果：

| scan | lines | unique files | 最高风险集中区 |
|---|---:|---:|---|
| primary risk scan | 10740 pre-write / 10808 post-write | 813 pre-write / 818 post-write | R5.7.5 blind adjudication outputs、R5.7 reports、quality model、repair target adjudication、talks；post-write 增量来自本 PR 新增 ledger / audit 自引用命中。 |
| secondary broad scan | 16510 pre-write / 16565 post-write | 796 pre-write / 801 post-write | R5.7.5 blind manifests、conversion recovery JSON、objective metrics、reports、paper_v1；post-write 增量来自本 PR 新增 ledger / audit 自引用命中。 |

`paper_v1/` 存在并已纳入扫描；`AGENTS.md` 与 `CLAUDE.md` 指向同一真实路径，本 ledger 去重为 A-023。

## 6. 使用规则

1. 后续 PR 若发现本表漏项，应先补本 ledger 或在对应 PR body 明确新增资产来源，不能私自跳过清账。
2. `archive` 决策不等于删除；必须迁入 archive snapshot 并保留原路径映射。
3. `active` conversion / representation 资产只说明基础设施可继续使用，不说明方法有效。
4. `historical` 资产可用于解释“为什么转向”，不能作为 active claim evidence。
5. 任何 PR 若重新使用 Better STM / which STM is better / `can_claim_better_stm`，必须显式说明它只是 archive/calibration 引用，不是 paper1 active headline。

## 7. PR-better-archive 更新记录

| 时间 | 更新内容 |
|---|---|
| 2026-07-07 23:40:00 | A-006--A-013 与 A-015/R5.7.4 adjudication-only bundle 的链接由 active 路径改指 `archive/r5_7_better_stm_snapshot/`；归档决策保留为历史审计标签。 |
