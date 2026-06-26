# R4 evaluation GUIDE

## 0. 工作边界

本 GUIDE 约束 `paper_stm_repair/evaluation/` 下的 R4 评价门产物。R4 的目标是把“什么算问题、什么算场景、什么才允许称为 Better STM”变成可审计草案；它不是正式实验协议，不运行真实 LLM，不读取 `.env`，不执行 repair loop，也不产出论文主结果。

规则事实集中维护在 [EVALUATION_GATE.md](./EVALUATION_GATE.md)，四例 dry-run 说明集中维护在 [DRY_RUNS.md](./DRY_RUNS.md)。不要重新拆出多份平行规则 MD，避免形成第二事实源。

## 1. 维护纪律

1. **不改写 R3 裁决**：R4 只能引用或映射 R3 `status_reason_code`、diagnostic code 与 loss code；不能把 R3 `partial` 写成 `converted`。
2. **不混淆 conversion 与 repair**：R3.1 `main_eligibility_included=466` 只属于 conversion eligibility recovery，不属于 Better STM repair 收益。
3. **不伪造 canonical**：no-canonical 样例只能 blocked / diagnostic-only，不得用 source-text regex、旧 fixture 或人工脑补生成模型级评价输入。
4. **不把 `unknown` 当 `pass`**：Better STM checklist 中任一关键 `unknown` 不能支持 Better STM claim。
5. **不把 `placeholder` oracle 当回归门**：`oracle_type=placeholder` 只能用于字段占位或设计讨论，不能作为 `is_regression_gate=true` 的关键场景。
6. **不写动态 PR 流水账**：review 状态、ready 状态、CI 状态只维护在 GitHub PR body/comment；仓库只保留长期研究规则和可复验制品。
7. **不调用真实 LLM**：R4 所有 fixture 都是静态 dry-run；后续真实调用必须另有 run record、`.env` discipline 与 redaction。
8. **不拆散核心规则**：eligibility、diagnostic、scenario、Better STM、human rubric、metrics plan 均回写 [EVALUATION_GATE.md](./EVALUATION_GATE.md)；四例说明均回写 [DRY_RUNS.md](./DRY_RUNS.md)。

## 2. 新增 dry-run 样例流程

若后续 R7/R8 前需要新增 R4 dry-run 样例，必须按以下顺序：

1. 先确认样例已在一手 seed registry / selected examples 中有 `NL + STM_0` 事实来源。
2. 再读取 R3 conversion report，记录 `status`、`canonical_output_path`、`losses_count`、`blocking_reason`。
3. 生成 `eligibility_decision.json`，先判定 complete / focused / blocked。
4. 生成 `diagnostic_draft.json`，每个 diagnostic 必须有 evidence locator。
5. 生成 `scenario_draft.json`；若只有 placeholder oracle，必须 `is_regression_gate=false`。
6. 生成 `better_stm_checklist.json`；R4 无 repair candidate 时 `can_claim_better_stm=false`。
7. 更新 [DRY_RUNS.md](./DRY_RUNS.md) 的总览与单例详情，并补充或更新测试。

## 3. 验收检查

每轮修改至少运行：

```bash
python -m pytest project_1_llm_state_machine_modeling/paper_stm_repair/evaluation/tests
```

推荐同时抽查：

```bash
python -m json.tool project_1_llm_state_machine_modeling/paper_stm_repair/evaluation/dry_run_examples/llms-emp-gpt4o-hldcs/eligibility_decision.json >/dev/null
```

若测试失败，先判断是否破坏学术证据链：例如 R3 status 不一致、`unknown` 被计为 pass、placeholder oracle 被当作回归门，应按 C/I 修复；纯格式或措辞问题通常为 M。
