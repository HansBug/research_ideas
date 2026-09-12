# Better adjudication prompt dry-run notes（R5.7.5）

> 冻结时间：2026-07-05 02:10:39。本文件记录 prompt v0 在 R5.7.5 constructed answer-key suite 上的预期覆盖方式；它不记录后续 full blind judge 调用。full blind 运行、三方 judge 结果和 deterministic/LLM/scorer 链路以 [../../reports/2026-07-05-07-18-31-r5-7-5-full-blind-adjudication-dry-run.md](../../reports/2026-07-05-07-18-31-r5-7-5-full-blind-adjudication-dry-run.md) 为准。

## 1. constructed answer-key suite 本身不调用真实 LLM

R5.7.5 的 `STM_k` 全部是人工 / 确定性构造的 protocol dry-run candidate；本文件对应的 prompt v0 只冻结输入输出纪律和 expected verdict，不读取 `.env`，不调用 hosted provider，不产生成本、usage 或 repair effectiveness。后续 full blind adjudication 确实调用了 isolated judges，但那些输出只验证评价协议可执行，不是 repair loop 结果。

## 2. 覆盖目标

- `better`：C01、C11。
- `not_better`：C02、C03、C04、C05、C06、C07、C09、C12、C13、C14、C15、C20。
- `partial`：C08、C19。
- `unknown`：C10。
- `stmk_repair_failure`：C17。
- `protocol_or_provenance_invalid`：C18。
- `stress_t1`：C16。

`caveat_t05` 是 scope route，不是 primary verdict；当前由 C14 覆盖。以上分布已按 full blind canonical oracle 反向校准；若旧路径 slug 或早期 PR 讨论与本表不一致，以 [../../pipeline/evaluation/dry_run_examples/r5_7_5_constructed_stmk/suite_index.json](../../pipeline/evaluation/dry_run_examples/r5_7_5_constructed_stmk/suite_index.json)、[../../pipeline/evaluation/dry_run_examples/r5_7_5_blind_adjudication/oracle_answer_key.json](../../pipeline/evaluation/dry_run_examples/r5_7_5_blind_adjudication/oracle_answer_key.json) 和 [../../reports/2026-07-05-07-18-31-r5-7-5-full-blind-adjudication-dry-run.md](../../reports/2026-07-05-07-18-31-r5-7-5-full-blind-adjudication-dry-run.md) 为准。

`scenario_overfitting` 本轮只记录为 `handoff_only_not_covered`，交给 R7 scenario-ledger。

## 3. G2 失败路由补充

R5.7.5 区分两类 G2 attribution 风险：

1. **整体 provenance / ledger 缺失**：如 C18，候选不能被归因到可审计的 `canonical STM_0 -> STM_k` 变化，必须输出 `protocol_or_provenance_invalid`。
2. **局部 change 无 NL/evidence 支撑但 bundle 完整**：如 C13，ledger 存在且候选可审计，但新增 `Untraced Auto Exit` 这类局部变化无证据支撑；此时可继续进入 G3/G5，并以 `not_better` 表示语义上不是改进，而不是把整个 protocol 判为 provenance invalid。
3. **conversion laundering / timed overclaim 在 blind 视角下不可直接判成整体 protocol invalid**：C04 经 blind 校准为 identity / no semantic gain 的 `not_better`，C15 经 blind 校准为 in-scope timer/no-gain 反例的 `not_better`；二者仍保留 laundering / time-caveat 风险标记，但不再承担 `protocol_or_provenance_invalid` 主分支。

这个区分只服务于裁决协议 dry-run，不改变所有 case 的 constructed / non-headline 边界。
