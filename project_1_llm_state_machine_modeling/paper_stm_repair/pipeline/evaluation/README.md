# pipeline/evaluation/ — active evaluation placeholder

> R4/R5.7 的 Better STM evaluation gate、schemas、dry-run examples、constructed `STM_k` bundle 和 blind judge outputs 已整体迁入 cold archive：[../../archive/r5_7_better_stm_snapshot/pipeline/evaluation/](../../archive/r5_7_better_stm_snapshot/pipeline/evaluation/)。

本目录当前只保留 active placeholder。paper1 后续 evaluation 不再从 Better STM / which STM is better gate 继承，而应围绕 source-level issue lifecycle 重建：

```text
candidate issue -> confirmed issue -> repair/change -> source projection -> closure/regression
```

## 当前状态

| 项 | 状态 |
|---|---|
| active evaluation schema | 未定义 |
| source-level closure rubric | 未定义 |
| regression audit protocol | 未定义 |
| LLM / human judge prompt | 未定义 |
| baseline comparison contract | 未定义 |

这些内容必须等 `PR-issue-ledger`、`PR-source-trace`、`PR-loop-io` 和 pilot 产出真实 repair/change evidence 后再冻结。

## 禁止误读

- 不把 archived `EVALUATION_GATE.md` 作为 active gate。
- 不把 archived `better_stm_checklist.schema.json` 或 `can_claim_better_stm` 作为 active endpoint。
- 不把 archived dry-run examples 或 blind judge outputs 写成真实 repair-loop evidence。
- 若未来需要 diagnostic / scenario schema，必须重新定义字段语义和 source-level issue / closure 关系。

## 更新日志

| 时间 | 更新内容 |
|---|---|
| 2026-07-07 23:40:00 | `PR-better-archive` 后重建 placeholder；旧 R4/R5.7 evaluation directory 已冷归档。 |
