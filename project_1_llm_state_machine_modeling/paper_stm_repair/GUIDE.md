# paper_stm_repair 工作纪律

本文件只保留全局硬规则。顶层轻量总账请读 [SUMMARY.md](./SUMMARY.md)，当前研究状态和关键数字请读 [STATUS.md](./STATUS.md)，目录地图请读 [README.md](./README.md)。[SUMMARY.md](./SUMMARY.md) 只做导航，不替代 [STATUS.md](./STATUS.md) 或 pipeline / corpus / reports 事实源。

## 1. 最高边界

1. 本文主任务是 `<NL, STM_0> -> STM_k / Better STM` 的反馈驱动状态机修正，不是一轮式 `NL -> STM` 生成。
2. `NL -> STM_0` 只作为 seed construction / baseline source / related work，不作为主贡献。
3. `fcstm`、`pyfcstm`、DSL 和转换器都是内部实验载体，不能进入标题、摘要或贡献位。
4. 当前 R5 / R5.7 产物只是修正前准备度审计与评价协议 dry-run：不执行真实修正循环、不生成真实 repair-loop 输出的 `STM_k`、不调用真实 LLM、不读取 `.env`、不产生主实验结果。R5.7.5 constructed `STM_k` 只能作为 protocol dry-run candidate，不得计入 repair effectiveness。
5. conversion、normalization、representation lowering 带来的可解析性改善必须与修正循环收益分开统计。
6. 选定四例只用于冒烟 / 最小连通性自检，不是最终实验集合、不是样本上限。
7. GitHub PR / issue body 和 comment 是流程状态真源；仓库只保存长期研究事实、规则和可复验证据。

## 2. 事实源优先级

| 问题 | 优先事实源 | 辅助入口 |
|---|---|---|
| 顶层导航总账 | [SUMMARY.md](./SUMMARY.md) | [README.md](./README.md) |
| 当前总体状态 | [STATUS.md](./STATUS.md) | [README.md](./README.md) |
| 一手 seed 资格和数量 | [corpora/seed_library/REGISTRY.md](./corpora/seed_library/REGISTRY.md)、单条目 `seed_resource_registry.json` | [corpora/seed_library/SUMMARY.md](./corpora/seed_library/SUMMARY.md) |
| 修正基线 / 近邻 | [corpora/repair_baselines/SUMMARY.md](./corpora/repair_baselines/SUMMARY.md) | 单篇 `baseline_desc.md` |
| 纯 NL 数据源 | [corpora/nl_datasets/SUMMARY.md](./corpora/nl_datasets/SUMMARY.md) | 单条目说明 |
| 原始模型到规范化 JSON | [pipeline/conversion/reports/selected_seed_examples_conversion_report.json](./pipeline/conversion/reports/selected_seed_examples_conversion_report.json)、[pipeline/conversion/reports/plantuml_recovery_report.json](./pipeline/conversion/reports/plantuml_recovery_report.json) | [pipeline/conversion/README.md](./pipeline/conversion/README.md) |
| canonical 到 `.fcstm` | [pipeline/representation/reports/fcstm_export_report.json](./pipeline/representation/reports/fcstm_export_report.json) | [pipeline/representation/README.md](./pipeline/representation/README.md) |
| 评价门规则 | [pipeline/evaluation/EVALUATION_GATE.md](./pipeline/evaluation/EVALUATION_GATE.md) | [pipeline/evaluation/README.md](./pipeline/evaluation/README.md) |
| R5 四例冒烟 | [pipeline/readiness_audit/selected_examples/smoke_report.json](./pipeline/readiness_audit/selected_examples/smoke_report.json) | [reports/2026-06-28-03-42-24-selected-smoke-summary.md](./reports/2026-06-28-03-42-24-selected-smoke-summary.md) |
| R5 全量摸排 | [pipeline/readiness_audit/seed_sweep/sweep_report.json](./pipeline/readiness_audit/seed_sweep/sweep_report.json) | [reports/2026-06-28-04-03-18-seed-readiness-report.md](./reports/2026-06-28-04-03-18-seed-readiness-report.md) |
| R5.5 `llms-emp` 主 seed 池画像 | [pipeline/readiness_audit/llms_emp_profile/llms_emp_case_matrix.jsonl](./pipeline/readiness_audit/llms_emp_profile/llms_emp_case_matrix.jsonl)、[pipeline/readiness_audit/llms_emp_profile/llms_emp_cluster_profiles.jsonl](./pipeline/readiness_audit/llms_emp_profile/llms_emp_cluster_profiles.jsonl) | [reports/2026-06-29-00-03-56-llms-emp-main-seed-profile.md](./reports/2026-06-29-00-03-56-llms-emp-main-seed-profile.md)、[reports/2026-06-28-22-54-39-model-scope-handoff.md](./reports/2026-06-28-22-54-39-model-scope-handoff.md) |
| R5.6 model scope / claim boundary | [story/model_scope.md](./story/model_scope.md)、[experiment_design/scope/r5_6_to_r5_7_handoff_constraints.md](./experiment_design/scope/r5_6_to_r5_7_handoff_constraints.md) | [experiment_design/scope/2026-06-29-17-33-35-r5-5-scope-handoff.md](./experiment_design/scope/2026-06-29-17-33-35-r5-5-scope-handoff.md)、[story/claim_evidence_map.md](./story/claim_evidence_map.md) |
| R5.7.1 evaluation logic / claim boundary | [experiment_design/evaluation_logic.md](./experiment_design/evaluation_logic.md) | [reports/2026-07-02-17-02-42-r5-7-1-evaluation-logic.md](./reports/2026-07-02-17-02-42-r5-7-1-evaluation-logic.md)、[story/claim_evidence_map.md](./story/claim_evidence_map.md) |
| 历史 R0/R1 审计 | [evidence/README.md](./evidence/README.md)、[evidence/SUMMARY.md](./evidence/SUMMARY.md)、[evidence/GUIDE.md](./evidence/GUIDE.md)、[archive/](./archive/) | 不作为当前横向事实源 |

Markdown summary 只做人类入口；数字和资格判断应能回到 JSON、registry 或 ledger 复算。

## 3. 维护规则

### 3.1 seed / baseline / NL 数据不得混用

- `seed_library` 只登记一手 `<NL, STM_0>`、条件 seed、仅流水线或排除证据。
- `repair_baselines` 只登记 `<NL, STM_0> -> STM_k` 相关 baseline / 近邻 / related work。
- `nl_datasets` 只登记纯 NL 来源；只有本项目另行生成并记录 `STM_0` 后才可 crosslink 到 seed。

### 3.2 run record 与 LLM 调用

- 真实 LLM 调用前必须在 shell 中 `source .env`；代码只读 `os.environ`。
- 真实调用必须保留 provider、model id、日期、prompt、raw output、usage、错误、重试和脱敏报告。
- fake / replay / 固化样例不能冒充真实 LLM 结果。
- R5/R5.5 和之前的 dry-run 层均不得读取 `.env` 或调用真实 provider。

### 3.3 转换与表示归因

- PlantUML / Umple 主路径必须优先消费官方结构化导出；不能在官方工具失败时静默 regex 回退。
- normalization 只能发生在转换前，不覆盖一手 raw assets。
- `.fcstm` 只能作为内部可机检表示；任何 lowering / approximation 都必须进入 loss ledger。
- `repair_contribution_allowed=false` 的产物不得用于证明修正收益。

### 3.4 Better STM 主张

只有满足 [experiment_design/quality_model/better_stm_definition.md](./experiment_design/quality_model/better_stm_definition.md) 的五条件，才可把 `STM_k` 计为相对 `STM_0` 的 Better STM。任一条件为 `unknown`、`not_applicable` 或 `fail`，都不能支持 Better STM 主张。

## 4. 禁止写法

| 禁止写法 | 安全写法 |
|---|---|
| “本文提出首个 / 最强 `NL -> STM` 方法” | “本文研究给定初始状态机后的反馈驱动修正任务” |
| “本文提出新 DSL” | “本文使用语义增强、可机检的内部状态机表示支撑诊断与场景反馈” |
| “转换后能 parse，因此模型已被修复” | “转换后进入可机检表示，但转换收益与修正收益分开归因” |
| “四例冒烟证明方法有效” | “四例冒烟证明字段链路和修正前输入准备可复验” |
| “自动修正一定提升质量” | “在预注册评价门下检验是否产生相对更优候选，并报告失败、回滚和不收敛” |


## archive/ 冷归档纪律

1. `archive/` 只保存 cold / deprecated historical snapshots，不作为当前事实源。
2. 引用 archive 时必须同时说明当前事实应回到 `corpora/`、`reports/` 或 `pipeline/`。
3. archive 中非入口 README 的历史 Markdown 应使用 `yyyy-mm-dd-hh-mm-ss-短主题.md` 秒级前缀，并在开头记录原始路径、时间依据 commit、迁入 commit 和当前事实源替代入口。
4. archive README 是稳定入口文件，可以不使用秒级前缀，但必须维护清单、deprecated 标记和来源 commit。

## story/ 写作栅栏纪律

1. `story/README.md` 只做入口和阅读顺序，不吞并 `paper_story.md`、`task_boundary.md`、`terminology_policy.md`、`claim_evidence_map.md`、`paper_outline.md` 的专题职责。
2. story 文件只能把证据转为 paper claim gate，不得替代 `reports/`、`pipeline/`、`corpora/` 或 `experiment_design/` 的事实真源。
3. 每次 scope、eligibility 或 repair-loop 结果冻结后，必须同步检查 story claim 是否需要降级或删除。
4. R5.6 之后，涉及模型族、时间等级、resource role、forbidden extrapolation 或 R5.7 handoff 的写作与协议设计，必须优先读取 [story/model_scope.md](./story/model_scope.md)，并同步检查 [experiment_design/scope/r5_6_to_r5_7_handoff_constraints.md](./experiment_design/scope/r5_6_to_r5_7_handoff_constraints.md)。
5. R5.7.1 之后，涉及 claim 类型、分母、A 层、归因边界、客观指标、failure / partial / unknown / out-of-scope 报告或方法有效性写法时，必须优先读取 [experiment_design/evaluation_logic.md](./experiment_design/evaluation_logic.md)。


## 5. R5.7.5 constructed `STM_k` dry-run 归因纪律

R5.7.5 的 [reports/2026-07-05-02-10-39-r5-7-5-constructed-stmk-coverage-dry-run.md](./reports/2026-07-05-02-10-39-r5-7-5-constructed-stmk-coverage-dry-run.md) 与 [experiment_design/better_adjudication_dry_run/README.md](./experiment_design/better_adjudication_dry_run/README.md) 只证明评价协议覆盖能力，不证明修复方法有效。后续引用这些材料时必须保留：`constructed_for_protocol_dry_run=true`、`headline_eligible=false`、`repair_effectiveness_eligible=false`、`real_repair_run_id=null`。
