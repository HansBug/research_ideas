# Discover 默认作者 feedback-final 选择池 60 资源

本目录是 `paper_stm_repair_loop.inputs.load_pair()` 的默认 FCSTM 资源集合。它不再维护四例 smoke 子集，也不提供 manual、compat 或临时旁路；目录中的 60 个子目录与默认 [`pairs.jsonl`](../corpora/seed_library/llms-emp-stm-subset/assets/extracted/pairs.jsonl) 一一对应。

## 资源合同

每个 `llms_emp_feedback_final_NNNN/` 目录固定包含：

- `nl.txt`：作者 workbook 中对应行的 requirement description；
- `stm0.puml`：按作者 feedback-final 选择策略得到的 PlantUML；58 例取 Phase-II semantic checking 输出，`0054/0055` 因没有 checking 输出而回退 Phase-I generation；
- `model.fcstm`：Issue #161 Java frontend 与 R4.5 表示桥生成的 FCSTM working artifact；
- `source_meta.json`：默认 pair、workbook cell、Phase-I/Phase-II lineage、source hash 与审阅入口；
- `fcstm_meta.json`：FCSTM hash、canonical/case report/source trace/working contract/parse-inspect/publication seal 绑定。

目录名、`source_meta.json.pair_id` 和 `pairs.jsonl.pair_id` 必须相同。`load_pair()` 读取 `pairs.jsonl` 的 NL 与 PlantUML，并读取本目录的 `model.fcstm`；不得把 report 目录、manual identity 或 custom mode 当作默认输入替代品。pair schema 中 `generation_context=author_phase_ii_checking_feedback` 与 `stm0_role=author_feedback_final_plantuml` 是池级标签；逐例实际来源以 `selected_stage`、`selected_stage_column` 和 `is_phase_i_fallback` 为准，`0054/0055` 的 `attribution` 必须明确禁止将其写成作者 checking 或本研究 Repair 的产物。

## 学术边界

- 60 例均允许 attribution-scoped source-static Discover；这不等于 whole-model behavior equivalence、simulation eligibility 或最终主结果 eligibility。
- `model.fcstm` 是 representation conversion，不是 Repair 输出；`repair_contribution_allowed=false`。
- confirmed source issue 必须回到 positive source trace、原 PlantUML fragment 与 NL/typed evidence；compiler-owned element 不得升级为作者缺陷。
- 每例 `closure_claim_allowed=false`。不支持的 initial、concurrency、opaque label/body、lifecycle 等语义继续由 working contract capability exclusion 约束。
- 58 例 Phase-II 作者 checking/regeneration 的收益不能归因给本研究 Discover/Repair/Confirm；`0054/0055` 是 Phase-I fallback，不得写成作者 feedback 修复后的输出。

## 审阅入口

- [60 组三元组索引](../pipeline/representation/reports/llms_emp_r45_java_60/PAIR_INDEX.md)
- [60 行人工/LLM审阅总账](../pipeline/representation/reports/llms_emp_r45_java_60/MANUAL_REVIEW.md)
- [R4.5 汇总](../pipeline/representation/reports/llms_emp_r45_java_60/SUMMARY.md)
- [publication seal](../pipeline/representation/reports/llms_emp_r45_java_60/PUBLICATION_SEAL.json)
- [Issue #161 技术报告](../reports/2026-07-19-issue-161-plantuml-java-frontend.md)

## 最小验收

1. 默认 `pairs.jsonl` 恰好包含 60 个唯一 pair ID。
2. 本目录恰好包含 60 个 pair 子目录，不允许额外 manual/compat 目录。
3. 每例 NL、PlantUML、FCSTM hash 与 `source_meta.json` / `fcstm_meta.json` 一致。
4. 每例 meta 引用的 case report、source trace、working contract、canonical、parse-inspect、三元审阅页和 publication seal 均存在且 hash 闭合。
5. 在未修改的 PR-discover `load_pair()` 上 60/60 加载成功，`raw_source_format=plantuml`，且 `raw_source` / `fcstm` 分别等于当前 selected PlantUML / R4.5 FCSTM。
