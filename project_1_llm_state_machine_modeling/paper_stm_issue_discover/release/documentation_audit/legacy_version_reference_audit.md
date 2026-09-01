# 历史版本引用审计

本审计覆盖 `paper_stm_issue_discover/` 内所有 Markdown 中 `v27`、`v27-stream`、`v46`、`v26`、`feedback_loop` 与 legacy X1v2 数字的引用。枚举命令如下；审查单位是命中文件与其职责，不以 grep 数量代替语义判断。最终机械枚举为 176 个命中文件，逐文件分类、允许原因和当前边界见 [legacy_version_reference_rows.md](./legacy_version_reference_rows.md)。初稿的 171 个计数未包含后来新增的 release 审计与复核记录；这些记录均标为 `release/provenance`。

```bash
rg -n -i --glob '*.md' 'v27(?:-stream)?|v46|v26' project_1_llm_state_machine_modeling/paper_stm_issue_discover
```

## 判定规则

| 路径或模式 | 分类 | 允许保留历史版本名的理由 | 默认入口要求 |
| --- | --- | --- | --- |
| `README.md`、`SUMMARY.md`、`STATUS.md`、`story/*.md`（`blueprint_proposal.md` 除外）、`method/README.md`、`judge/README.md`、`evaluation/README.md`、`pipeline/README.md`、`scripts/README.md` | current/public | 仅在“非 current result”限制句或到历史索引的链接中出现 | 主叙事、命令和结果只指向 v60/current 与 X1v2 final archive |
| `story/blueprint_proposal.md` | historical/redirect | 指向早期提案的归档副本 | 当前谓词与方法边界指向 `method/` 和冻结 protocol |
| `archive/**` 与 `story/archive/**` | historical/archive | 文件本身保存冻结时期的代码、协议、报告或叙事 | 不得从 current 导航把它作为方法、结果或默认复算入口 |
| `reports/**` | historical/report | 保存日期化研究报告和旧 Judge/运行记录 | 目录入口明确指向 final archive；数字只按原报告的历史协议理解 |
| `baseline_arm/**` | historical/provenance | 保存 X1v2 的早期设计、prompt、判定与分析 | 目录入口明确说明 current baseline 在 final archive |
| `discover_matrix/docs/generations/**` | historical/preregistered | 保存代次登记和过程记录 | 不定义 current headline 或 current Judge 指标 |
| `discover_matrix/docs/protocol/**` 与 `judge/**/semantic_judge_issue_195.snapshot.md` | frozen-protocol | 版本名与规则的当时冻结语境不可改写 | current 文档可引用定义，但结果须回 final archive |
| `discover_matrix/docs/findings/**`、`discover_matrix/ledger_v2/provenance/**`、`evidence/**` | provenance | 保存 ledger、人工审计、来源和历史诊断依据 | 不作为 current result 或 method 运行入口 |
| `related_work/**`、`corpora/**` | provenance | 保存文献、输入和来源调研的历史关系 | 不以其旧统计描述 current 实验 |
| `experiment_design/**`、`PENDING_DECISIONS.md`、`TODO.md` | historical planning | 保存过去的候选实验和决策背景 | 文件首段已明确不是 current instruction 或执行授权 |
| `pipeline/archive/**`、`pipeline/conversion/**`、`pipeline/evaluation/**` | compatibility/provenance | 保存输入准备、兼容模块或旧过程材料 | 新方法、Judge 和评测入口分别为 `method/`、`judge/`、`evaluation/` |
| `release/**`、`release_validation/**`、`final_results/**` | release provenance / frozen result | 保留实验 commit、内部 RC 或冻结制品的来源关系 | v60/current 与 X1v2 数字以 final archive 的 raw/derived/report 为准 |

## current-facing 复核

下列 current/public 文件已逐项复核。若出现历史版本名，其作用仅为限制跨代次比较或链接唯一历史索引，而不是陈述 current 方法、结果或默认入口：

| 文件 | 结果 |
| --- | --- |
| [README.md](../../README.md) | 通过；current 结果仅链接 final archive |
| [SUMMARY.md](../../SUMMARY.md) | 通过；仅提供 current 索引与历史 archive 指针 |
| [STATUS.md](../../STATUS.md) | 通过；历史数字只作为禁止混用的说明 |
| [story/README.md](../../story/README.md)、[paper_story.md](../../story/paper_story.md)、[paper_outline.md](../../story/paper_outline.md)、[claim_evidence_map.md](../../story/claim_evidence_map.md)、[terminology_policy.md](../../story/terminology_policy.md)、[model_scope.md](../../story/model_scope.md) | 通过；方法与 claim 以 v60/current 叙述，历史只作不可比性说明 |
| [blueprint_proposal.md](../../story/blueprint_proposal.md) | historical/redirect；只指向归档提案，当前方法入口为 `method/` |
| [method/](../../method/README.md)、[judge/](../../judge/README.md)、[evaluation/](../../evaluation/README.md) | 通过；只描述现行包边界和冻结实验引用 |
| [pipeline/](../../pipeline/README.md) 与 [scripts/](../../scripts/README.md) | 通过；只作当前基础设施或薄入口导航 |
| [discover_matrix/](../../discover_matrix/README.md) 与 [ledger_v2/](../../discover_matrix/ledger_v2/README.md) | 通过；ledger 是事实源，current result 指向 final archive |
| [reports/](../../reports/README.md) 与 [experiment_design/](../../experiment_design/README.md) | 通过；入口已降级为 historical/provenance |

旧 X1v2 `59.8%/70.3%/47.9%` 仅保留在明确标为 historical/superseded 的 [X1V2_RESULTS.md](../../discover_matrix/ledger_v2/X1V2_RESULTS.md)、实验历史索引和审计限制句中，并且每一处均指向 current final report。`pipeline/feedback_loop/` 与 `pipeline/feedback_loop/README.md` 已从 current-facing 文档链接中清除；历史命中仅允许存在于 provenance 或 archive 资料中。
