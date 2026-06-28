# paper_stm_repair 工作纪律

本文件只保留全局硬规则。当前研究状态请读 [STATUS.md](./STATUS.md)，目录地图请读 [README.md](./README.md)。

## 1. 最高边界

1. 本文主任务是 `<NL, STM_0> -> STM_k / Better STM` 的反馈驱动状态机修正，不是一轮式 `NL -> STM` 生成。
2. `NL -> STM_0` 只作为 seed construction / baseline source / related work，不作为主贡献。
3. `fcstm`、`pyfcstm`、DSL 和转换器都是内部实验载体，不能进入标题、摘要或贡献位。
4. 当前 R5 产物只是修正前准备度审计：不执行修正循环、不生成 `STM_k`、不调用真实 LLM、不读取 `.env`、不产生主实验结果。
5. conversion、normalization、representation lowering 带来的可解析性改善必须与修正循环收益分开统计。
6. 选定四例只用于冒烟 / 最小连通性自检，不是最终实验集合、不是样本上限。
7. GitHub PR / issue body 和 comment 是流程状态真源；仓库只保存长期研究事实、规则和可复验证据。

## 2. 事实源优先级

| 问题 | 优先事实源 | 辅助入口 |
|---|---|---|
| 当前总体状态 | [STATUS.md](./STATUS.md) | [README.md](./README.md) |
| 一手 seed 资格和数量 | [corpora/seed_library/REGISTRY.md](./corpora/seed_library/REGISTRY.md)、单条目 `seed_resource_registry.json` | [corpora/seed_library/SUMMARY.md](./corpora/seed_library/SUMMARY.md) |
| 修正基线 / 近邻 | [corpora/repair_baselines/SUMMARY.md](./corpora/repair_baselines/SUMMARY.md) | 单篇 `baseline_desc.md` |
| 纯 NL 数据源 | [corpora/nl_datasets/SUMMARY.md](./corpora/nl_datasets/SUMMARY.md) | 单条目说明 |
| 原始模型到规范化 JSON | [pipeline/conversion/reports/selected_seed_examples_conversion_report.json](./pipeline/conversion/reports/selected_seed_examples_conversion_report.json)、[pipeline/conversion/reports/plantuml_recovery_report.json](./pipeline/conversion/reports/plantuml_recovery_report.json) | [pipeline/conversion/README.md](./pipeline/conversion/README.md) |
| canonical 到 `.fcstm` | [pipeline/representation/reports/fcstm_export_report.json](./pipeline/representation/reports/fcstm_export_report.json) | [pipeline/representation/README.md](./pipeline/representation/README.md) |
| 评价门规则 | [pipeline/evaluation/EVALUATION_GATE.md](./pipeline/evaluation/EVALUATION_GATE.md) | [pipeline/evaluation/README.md](./pipeline/evaluation/README.md) |
| R5 四例冒烟 | [pipeline/smoke/selected_examples/smoke_report.json](./pipeline/smoke/selected_examples/smoke_report.json) | [pipeline/smoke/selected_examples/smoke_summary.md](./pipeline/smoke/selected_examples/smoke_summary.md) |
| R5 全量摸排 | [pipeline/smoke/seed_library_sweep/sweep_report.json](./pipeline/smoke/seed_library_sweep/sweep_report.json) | [pipeline/smoke/seed_library_sweep/sweep_summary.md](./pipeline/smoke/seed_library_sweep/sweep_summary.md) |
| 历史 R0/R1 审计 | [evidence/README.md](./evidence/README.md)、[archive/](./archive/) | 不作为当前横向事实源 |

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
- R5 和之前的 dry-run 层均不得读取 `.env` 或调用真实 provider。

### 3.3 转换与表示归因

- PlantUML / Umple 主路径必须优先消费官方结构化导出；不能在官方工具失败时静默 regex 回退。
- normalization 只能发生在转换前，不覆盖一手 raw assets。
- `.fcstm` 只能作为内部可机检表示；任何 lowering / approximation 都必须进入 loss ledger。
- `repair_contribution_allowed=false` 的产物不得用于证明修正收益。

### 3.4 Better STM 主张

只有满足 [experiment_design/better_stm_definition.md](./experiment_design/better_stm_definition.md) 的五条件，才可把 `STM_k` 计为相对 `STM_0` 的 Better STM。任一条件为 `unknown`、`not_applicable` 或 `fail`，都不能支持 Better STM 主张。

## 4. 禁止写法

| 禁止写法 | 安全写法 |
|---|---|
| “本文提出首个 / 最强 `NL -> STM` 方法” | “本文研究给定初始状态机后的反馈驱动修正任务” |
| “本文提出新 DSL” | “本文使用语义增强、可机检的内部状态机表示支撑诊断与场景反馈” |
| “转换后能 parse，因此模型已被修复” | “转换后进入可机检表示，但转换收益与修正收益分开归因” |
| “四例冒烟证明方法有效” | “四例冒烟证明字段链路和修正前输入准备可复验” |
| “自动修正一定提升质量” | “在预注册评价门下检验是否产生相对更优候选，并报告失败、回滚和不收敛” |
