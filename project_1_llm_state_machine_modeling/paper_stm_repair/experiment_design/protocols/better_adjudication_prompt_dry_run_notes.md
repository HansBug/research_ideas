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

## 3. G2 失败路由补充

R5.7.5 区分两类 G2 attribution 风险：

1. **整体 provenance / ledger 缺失**：如 C04/C15/C18，候选不能被归因到可审计的 `canonical STM_0 -> STM_k` 变化，必须输出 `protocol_or_provenance_invalid`。
2. **局部 change 无 NL/evidence 支撑但 bundle 完整**：如 C13，ledger 存在且候选可审计，但新增 `Untraced Auto Exit` 这类局部变化无证据支撑；此时可继续进入 G3/G5，并以 `not_better` 表示语义上不是改进，而不是把整个 protocol 判为 provenance invalid。

这个区分只服务于裁决协议 dry-run，不改变所有 case 的 constructed / non-headline 边界。
