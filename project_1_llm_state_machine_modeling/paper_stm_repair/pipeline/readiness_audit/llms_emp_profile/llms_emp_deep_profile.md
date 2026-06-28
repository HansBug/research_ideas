# Migration notice: `llms_emp_deep_profile.md`

> 本文件是旧 pipeline 路径下的 human-facing Markdown 入口。R5.5.1 路径重构已将完整阅读结论迁移到 `paper_stm_repair/reports/`；本文件只保留 redirect notice，避免形成第二事实源。

## Canonical human-facing report

- [reports/2026-06-29-00-03-56-llms-emp-main-seed-profile.md](../../../reports/2026-06-29-00-03-56-llms-emp-main-seed-profile.md)

## Canonical machine source(s)

- [llms_emp_case_matrix.jsonl](./llms_emp_case_matrix.jsonl)
- [llms_emp_cluster_profiles.jsonl](./llms_emp_cluster_profiles.jsonl)
- [llms_emp_cluster_llm_matrix.jsonl](./llms_emp_cluster_llm_matrix.jsonl)
- [llms_emp_partial_attribution_ledger.jsonl](./llms_emp_partial_attribution_ledger.jsonl)
- [llms_emp_blocked_probe.jsonl](./llms_emp_blocked_probe.jsonl)

## 迁移说明

旧深度画像完整结论表、10×6 LLM 矩阵与行为特征矩阵已迁移到 canonical main seed profile report；当前 machine counts 为 cases=60 / clusters=10 / partial=41 / blocked=3 / status={'blocked': 3, 'converted': 16, 'partial': 41}。
