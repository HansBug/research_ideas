# v60/current 与 X1v2 baseline 最终结果归档

本目录保存 Paper 1 的两组冻结实验制品及其离线复算结果：`v60_current` 与 `x1v2_baseline`。它是论文结果、复核和交班的稳定数据入口；`runs/` 中的原始运行目录只保留为 provenance，不是复算的唯一依赖。

归档不重写 method 或 Judge 制品，也不包含 provider 请求/响应流、缓存、密钥、锁文件、`.part` 文件或 launcher 日志。保留的结构化 JSON 足以重算报告中的 hit、K/N/I、cluster、W、谓词使用和成本资格指标。筛选规则及原因见 [archive_manifest.json](archive_manifest.json)。

## 目录

- `raw/v60_current/`：v60 的 method、Judge composite、composite 选择的 Judge source runs 及其独立 manifest。
- `raw/x1v2_baseline/`：X1v2 的 162 个 method record、冻结 Judge composite、其 source runs 和 corrected method-cost audit。
- `reference/`：145 条 ledger、冻结 19 谓词 registry 和 source catalog。
- `reference/x1v2_input_closure/.gitattributes`：冻结输入闭包的 `nl.txt` 与 `plantuml.puml` 保留原始字节和 manifest-bound SHA-256；其中的 source 尾随空格不参与可编辑文本的 whitespace 检查。
- `derived/recomputed_summary.json`：只读取本目录 `raw/`、`reference/` 与已完成的 X1v2 人工 W 审计重新计算的机器可读主汇总。
- `derived/x1v2_witness_level_audit.json`、`x1v2_full_hit_max_witness_audit.json`：512 条 baseline finding 的双审 W0/W1/W2 记录，以及 435 条 expected row 的 FULL-only max-W 聚合。
- `derived/x1v2_witness_review_packet.json`、`x1v2_witness_review_batches/`、`x1v2_witness_review_decisions/`、`x1v2_witness_adjudications.json`：Judge-blinded 审阅全集、互斥批次、两次独立 decision，以及 pane5 的分歧裁决和受限 post-review correction。审阅包不含 Judge 路径、hash、validity、expected relation 或 ledger ID；这些关联仅在双审结束后附入最终审计。
- `derived/superseded_judge_exposed_witness_review_v1/`：首轮暴露 Judge 关联的审阅材料。它只保留 provenance，不进入最终复算、报告或验收。
- `archive_manifest.json`、`raw/*/archive_manifest.json`：原始审计面及其 SHA-256 清单。
- `publication_manifest.json`：报告和 review 写入后生成的全目录 SHA-256 清单。
- `report/`：最终中文实验报告。
- `reviews/`：事实、完整性、学术语义和文风保真审查记录。

字段语义、分母与已知数据缺口见 [SCHEMA.md](SCHEMA.md)。

## 离线复算

从仓库根执行下列命令。该命令只读取归档 JSON，不调用 provider，也不会修改 method/Judge 原始制品：

```bash
PYTHONPATH=project_1_llm_state_machine_modeling/paper_stm_issue_discover \
python3 -m pipeline.evidence_discovery.reporting.final_results_archive validate \
  --archive-root project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline
```

在报告和 reviews 全部完成后，再执行：

```bash
PYTHONPATH=project_1_llm_state_machine_modeling/paper_stm_issue_discover \
python3 -m pipeline.evidence_discovery.reporting.final_results_archive finalize \
  --archive-root project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline
```

人工审计完成后，可先用 `recompute` 刷新其机器汇总和 side manifest：

```bash
PYTHONPATH=project_1_llm_state_machine_modeling/paper_stm_issue_discover \
python3 -m pipeline.evidence_discovery.reporting.final_results_archive recompute \
  --archive-root project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline
```

`finalize` 重建顶层 `archive_manifest.json` 并更新 `publication_manifest.json`，将报告和 review 与 raw/derived/reference 一并纳入哈希清单。随后再次运行 `validate`；它会检查 manifest/summary/provenance schema、归档内映射和 Markdown 本地链接、全部发布文件的 SHA-256，并重新生成 `recomputed_summary.json` 进行逐值比较。

## 不可变性与限制

两侧 Judge 都使用 commit `05cf0da6f7d9fcf1de26c349b586fc71c268f1c5` 和 issue #195 的 two-stage v3.2 口径。v60 method commit 为 `66b5d71aecd73f6eeddac082037f7c34e04da057`；X1v2 的 legacy record schema 没有顶层 source-commit summary，相关缺口在 baseline manifest 和报告中保留。

X1v2 没有同构的 19 谓词 registry 或 terminal receipt schema，因此 predicate usage 不适用；这不影响 W 轴。归档以 Judge-blinded 两轮独立逐条回溯审计覆盖 512 条冻结 finding，得到 `W0/W1/W2 = 1/511/0`。两轮标签没有 W 级分歧；独立语义审查发现一条共同误标，受限 post-review correction 将其从 W1 裁为 W0。W2 为零是审计结果，不是缺失值或 schema 默认值。v60 Judge 的已记录成本也不具有完整成本资格：1,374 个逻辑调用中有 10 个应计费调用缺少可定价 usage。不得用估算值补齐。
