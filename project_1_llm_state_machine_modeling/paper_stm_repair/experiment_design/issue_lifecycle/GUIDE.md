# issue_lifecycle/GUIDE.md — source-level issue ledger 维护规范

## 1. 阅读顺序

维护本目录时默认先读：

1. [../README.md](../README.md)：确认 experiment design 当前只维护 source-level issue lifecycle scaffold。
2. [README.md](./README.md)：确认本目录职责。
3. [source_level_issue_definition.md](./source_level_issue_definition.md)：确认术语和确认路径。
4. [issue_ledger_contract.md](./issue_ledger_contract.md)：确认字段和后续接口。
5. [../../pipeline/evaluation/schemas/source_issue_ledger.schema.json](../../pipeline/evaluation/schemas/source_issue_ledger.schema.json)：确认 machine-checkable 合同。
6. [../../pipeline/evaluation/fixtures/source_issue_ledger/](../../pipeline/evaluation/fixtures/source_issue_ledger/)：确认 committed fixtures。

## 2. 必须保持的边界

1. `candidate_only` 不等于 method success，不允许进入 repair。
2. `confirmed` 只能通过两条 v0 路径：
   - `nl_grounded_behavioral_issue`：必须至少包含 `nl_requirement`、`source_stm_fragment` 与 inspect/simulation/probe/verification 类型的 behavior evidence；
   - `raw_internal_inconsistency`。
3. `raw_internal_inconsistency` 的 `nl_evidence` 必须为空；它必须有至少两个 raw/source 冲突元素、至少两个 source STM evidence、typed internal-consistency evidence 和说明 `NL evidence is not required` 的 rationale。
4. `raw_internal_inconsistency` 后续必须在真实 raw NL / discovery pilot 中复核，不得在本目录写成 final taxonomy。
5. conversion / lowering / normalization artifact 必须 rejected 或 attribution-bounded，不得计入 source-level issue。
6. folded event / expression debt 默认只是 candidate，除非另有 source-level behavior evidence。
7. final metrics、baseline、judge prompt 必须等 pilot 后由后续 PR 冻结。

## 3. fixture 维护规则

- 每个 JSON fixture 必须通过 schema。
- 每个 fixture 应覆盖一个核心分支，不要把一个 fixture 写成小实验。
- JSON fixture 是机器事实源；文档 fixture README 只解释人类语境。
- 新增 `confirmed` fixture 时，必须明确 `confirmation_evidence_path`。
- 非 confirmed fixture 必须 `downstream_repair_allowed=false`。

## 4. review 重点

Reviewer 应优先检查：

1. 是否把 Better STM / constructed `STM_k` / blind judge 写回 active protocol。
2. 是否把 `fcstm` 或 ledger/audit 写成 contribution。
3. 是否把 expression debt 自动 confirmed。
4. 是否把 conversion artifact 当 source-level issue。
5. 是否缺少 schema-enforced `nl_requirement` / `source_stm_fragment` / typed behavior evidence。
6. 是否没有说明为什么 `raw_internal_inconsistency` 不需要 NL evidence。
7. 是否提前冻结 final metric / baseline。

## 5. 更新日志

| 时间 | 更新内容 |
|---|---|
| 2026-07-08 09:52:31 | 初始化 issue lifecycle 维护规范。 |
