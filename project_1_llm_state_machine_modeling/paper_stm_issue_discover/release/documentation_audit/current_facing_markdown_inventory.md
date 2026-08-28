# 当前阅读路径清单

本清单按文件而不是目录标注默认阅读路径。`current/public` 只能叙述 v60/current、X1v2 baseline、当前包边界和复现入口；出现旧版本名时只能用于不可比性限制或历史索引。完整历史关键词逐文件审计见 [legacy_version_reference_rows.md](./legacy_version_reference_rows.md)。

| 文件 | 分类 | 职责与边界 |
| --- | --- | --- |
| `README.md` | current/public | 项目定位、当前方法与结果入口 |
| `SUMMARY.md` | current/public | 当前阅读索引 |
| `STATUS.md` | current/public | 当前冻结结果、release refactor 与文档状态 |
| `GUIDE.md` | current/public | 当前工作区的稳定维护约束 |
| `story/README.md` | current/public | 当前论文叙事的入口 |
| `story/paper_story.md` | current/public | v60 的研究问题、流程与限制 |
| `story/paper_outline.md` | current/public | 当前论文结构 |
| `story/claim_evidence_map.md` | current/public | 当前 claim 与冻结证据的映射 |
| `story/terminology_policy.md` | current/public | 当前术语与边界 |
| `story/model_scope.md` | current/public | 当前可外推范围与排除项 |
| `story/blueprint_proposal.md` | historical/redirect | 指向已归档早期提案；不进入当前方法或结果叙事 |
| `method/README.md` | current/public | 当前 method 包、输入闭包、W/D、安装和 CLI |
| `judge/README.md` | current/public | 当前 issue #195 Judge、两阶段隔离和 CLI |
| `evaluation/README.md` | current/public | 当前离线指标所有权与归档复算 |
| `pipeline/README.md` | current/public | 输入准备与兼容 namespace 导航 |
| `pipeline/evidence_discovery/README.md` | compatibility/provenance | 旧 import 与测试兼容；权威方法为 `method/` |
| `pipeline/conversion/README.md` | provenance | 冻结输入准备和转换工具 |
| `pipeline/representation/README.md` | provenance | FCSTM 表示准备和输入 provenance |
| `pipeline/evaluation/README.md` | historical/provenance | v0 schema 与 fixture，不是当前评测 |
| `scripts/README.md` | current/public | 薄 CLI 的用途、读写边界和 provider 状态 |
| `discover_matrix/README.md` | current/ledger | 145 条 ledger 的入口，结果链接 final archive |
| `discover_matrix/ledger_v2/README.md` | current/ledger | 当前 ledger 与 provenance |
| `discover_matrix/ledger_v2/X1V2_RESULTS.md` | historical/provenance | legacy X1v2 数字的迁移说明，指向 current final report |
| `final_results/v60_current_vs_x1v2_baseline/README.md` | current/result | 当前唯一的实验事实源和冻结结果归档 |
| `archive/README.md` | historical/archive | 历史路线与唯一实验历史索引 |
| `archive/experiment_history/README.md` | historical/archive | v46、v27 与 v60 的可比性和保存策略 |
| `reports/README.md` | historical/report | 日期化旧报告的索引 |
| `reports/SUMMARY.md` | historical/report | 历史报告摘要 |
| `reports/GUIDE.md` | historical/report | 仅适用于历史报告的维护规则 |
| `experiment_design/README.md` | provenance | 已保留的实验设计材料 |
| `experiment_design/GUIDE.md` | provenance | 历史设计与 provenance 的维护限制 |
| `baseline_arm/README.md` | historical/provenance | baseline 设计资料，current result 指向 final archive |

以下目录只按其明确职责保留历史版本名，不进入默认 current 路径：`archive/**` 为 historical/archive，`reports/**` 为 historical/report，`discover_matrix/docs/protocol/**` 和 Judge protocol resource 为 frozen-protocol，`discover_matrix/docs/generations/**` 为 historical/preregistered，`related_work/**`、`corpora/**`、`evidence/**` 与 ledger provenance 为 provenance，`release/**`、`release_validation/**` 为 release provenance。
