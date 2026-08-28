# 文档引导与中文文风独立审查

审查范围：主入口、`story/*.md`、package README、ledger/X1v2、reports、experiment_design、archive、documentation audit；按 `shuorenhua` 的 docs + README、`minimal + audit-only` 边界审查。

## 复核方法

```bash
rg -n -i --glob '*.md' 'v27(?:-stream)?|v46|v26|feedback[_ -]?loop|59\.8%|70\.3%|47\.9%' project_1_llm_state_machine_modeling/paper_stm_issue_discover
PYTHONPATH=project_1_llm_state_machine_modeling/paper_stm_issue_discover/evaluation/src:project_1_llm_state_machine_modeling/paper_stm_issue_discover \
venv/bin/python -m paper_stm_evaluation.final_results_archive validate \
  --archive-root project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline
```

本地相对 Markdown 链接扫描未发现缺失目标；`scripts/README.md` 所列 10 个 Python script 与实际文件一一对应。主 README、SUMMARY、STATUS、method/Judge/evaluation 与 ledger 的第一屏已说明对象、读者、问题和 current result 入口，中文术语稳定，未见将 legacy X1v2 数字写成 current 结果的情况。

| 严重度 | Finding | Evidence | 处理 |
| --- | --- | --- | --- |
| High | 最终归档 README 修改后未重建 root manifests，导致 authoritative validator 失败。 | validator 报 README manifest mismatch。 | pending: 运行受控 `finalize`，验证 raw/derived/reference 未变。 |
| Medium | `story/blueprint_proposal.md` 指向 compatibility `pipeline/evidence_discovery`。 | current method 在 `method/`。 | pending: 改为 method resources 与 frozen protocol。 |
| Medium | `reports/GUIDE.md` 没有说明只管历史 report，仍把 pipeline 写成通用 current facts。 | reports README 已降级为 historical。 | pending: 添加 historical scope 与 current final archive/evaluation 入口。 |
| Medium | current-facing inventory 以目录聚合，不能逐项证明 historical exceptions。 | `story/blueprint_proposal.md` 是 historical redirect。 | pending: 展开 current files，并提供历史关键词逐文件清单。 |

审查为只读；provider 调用与 billable 调用均为 0。结论：处理以上问题并回读后可作 targeted rereview。

## 2026-08-28 第一次定向复审

reviewer 确认 Markdown 链接为零失效，`scripts/README.md` 与实际脚本一一对应，`pipeline/representation/README.md` 已将 current evaluation 指向 `evaluation/` 和 final archive。唯一中严重度残留是历史关键词总表仍写初稿计数 171，虽然逐文件表已与当前枚举闭合。

处理：`legacy_version_reference_audit.md` 改为最终计数 176，并说明初稿未包含后来新增的 release 审计与复核记录；相应文件均标为 `release/provenance`。

## 2026-08-28 第二次定向复审

reviewer 独立复算得到 `rg=176`、rows=`176`、missing/extra=`0`，并核对汇总审计已写为最终 176。

结论：通过。无剩余高/中严重度 finding；未修改文件，provider 与 billable 调用均为 0。
