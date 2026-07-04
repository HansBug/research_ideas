# Better adjudication prompt dry-run notes（R5.7.5）

> 冻结时间：2026-07-05 02:10:39。本文件记录 prompt v0 在 R5.7.5 constructed suite 上的预期覆盖方式，不记录真实 LLM 调用。

## 1. 本轮不调用真实 LLM

R5.7.5 的 `STM_k` 全部是人工 / 确定性构造的 protocol dry-run candidate；prompt v0 只冻结输入输出纪律和 expected verdict，不读取 `.env`，不调用 hosted provider，不产生成本、usage 或 repair effectiveness。

## 2. 覆盖目标

- `better`：C01、C08、C11。
- `not_better`：C03、C05、C06、C07、C09、C13、C20。
- `partial`：C02、C14、C19。
- `unknown`：C10、C12。
- `stmk_repair_failure`：C17。
- `protocol_or_provenance_invalid`：C04、C15、C18。
- `stress_t1`：C16。

`scenario_overfitting` 本轮只记录为 `handoff_only_not_covered`，交给 R7 scenario-ledger。
