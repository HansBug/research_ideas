# v61（源–语义分歧审计与发布层规则包）对 X1v2 baseline 的全量归档

本目录是 v61 方法在冻结 54 对 × 3 轮协议上的原始运行记录与 judge 判定归档，是 [docs/generations/v61/results.md](../../discover_matrix/docs/generations/v61/results.md) 全量节的数据源。v60 归档见 [v60_current_vs_x1v2_baseline/](../v60_current_vs_x1v2_baseline/)。

## 判定装置

三臂比较全部为 **judge 对 judge**：第六轮配置的语义 judge（gpt-5.6-luna，`semantic-judge.two-stage.v3.11`，relation-first 闭合，两读 + 分歧仲裁），无人工复核。ours v61 由本目录的 judge 输出判定；v60 ours 与 X1v2 baseline 的判定沿用 `runs/paper1/judge-full-3a1ba5cf1-iter6cfg`（同配置全量 judge，其 TSV 摘要在 [judge/calibration/results/full_v3.11_3a1ba5cf1/](../../judge/calibration/results/full_v3.11_3a1ba5cf1/)）。人工冻结终稿的数字（v60 ours 77.1% / 310，baseline 81.4% / 227）只作参照，不与本目录数字混算。

## 目录

| 路径 | 内容 |
|:--|:--|
| `raw/v61_current/method/` | method 全量运行根（提交 `ea6141607`，run id `a7b47d84c3cb4377a8009e5018d5b745`）去掉 `llm/` 调用审计后的完整拷贝：`method/<pair>/round-N.json` 162 格记录（含 stage_outputs、evidence_records、report_issue_clusters）、`audit_bundles/`、`pairs/`、`run_manifest.json`、`summary.json` |
| `raw/v61_current_fill0045/` | `0045` 第 1 轮的重采样运行（提交 `778212b03`，与 ea6141607 仅差文档；run id `0e450e5c6c9d4841820c7d1fd2a888ea`）。原运行里该格在契约抽取阶段 `limit_exceeded: turns limit exceeded` 失败（`raw/v61_current/method/method/0045/round-1.json` 仍保留失败回执）。评测以本目录的重采样格替代 |
| `raw/judge_v3.11_iter6cfg/current-r{1,2,3}/`、`current-r1-fill0045/` | judge 逐对判定（`pairs/<pair>.json`，含两读、仲裁、闭合、report_outcomes 与 expected_outcomes）、适配器审计与运行清单；不含 `llm/` 调用审计 |
| `derived/v61_all_reports.tsv` | 903 条报告的逐条表：谓词、性质、方向、标题、judge K/N/I 与 D/A、FULL / PARTIAL 台账条目、折叠子主张数、模态聚合成员数、作者源引用 |
| `derived/ledger_hits_v61_v60_baseline.tsv` | 145 条台账条目在三臂各轮的 FULL 命中 |
| `derived/evaluate_full_output.txt` | `docs/generations/v61/evaluate_full.py` 的输出（三臂总表与分 L 层） |
| `derived/per_predicate_and_ledger_report.txt`、`derived/ledger_gain_loss_attribution.txt` | 谓词 × 性质表、条目级增减及其在 v60 / v61 各由哪类报告命中 |

## 复算

```bash
venv/bin/python project_1_llm_state_machine_modeling/paper_stm_issue_discover/discover_matrix/docs/generations/v61/evaluate_full.py \
  --judge-root project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v61_source_divergence_vs_x1v2_baseline/raw/judge_v3.11_iter6cfg
```

## 总表（judge 口径）

| 指标 | baseline | v60 ours | v61 ours |
|:--|--:|--:|--:|
| 报告数 / 每格 | 512 / 3.2 | 1271 / 7.8 | 903 / 5.6 |
| K / N / I | 293 / 134 / 85 | 628 / 277 / 366 | 561 / 198 / 144 |
| report precision | 83.4% | 71.2% | 84.1% |
| finding-level precision | 81.1% | 63.4% | 79.3% |
| hit@1 | 225/435 | 292/435 | 323/435 |
| hit@3 / hit@all | 105 / 47 | 119 / 75 | 130 / 82 |
| L0 / L1 / L2 hit@1 | 51% / 69% / 38% | 63% / 55% / 85% | 72% / 70% / 83% |

## 已知限制

- 0045 第 1 轮为运行时限失败后的重采样，非原运行样本；两个记录都保留。
- judge 自身的轮间噪声与人工的偏移（v60 上 precision −5.9 pp、hit 单位 −18）未在本目录内校正。
- 折叠根报告的子主张命中依赖 judge 对多条目 FULL 的判定，相关损失分析见 `derived/ledger_gain_loss_attribution.txt` 与 results.md。
