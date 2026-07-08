# issue_lifecycle/ — source-level issue ledger 合同入口

本目录定义 paper1 当前主线中的最小 issue lifecycle 合同：从可疑问题 `candidate issue` 到 `confirmed source-level behavioral issue`，再到后续 `issue-grounded repair` 可以消费的 `issue_id`。

本目录是 `PR-issue-ledger` 的长期方法文档入口，不记录 PR 进度、review 状态或 CI 状态。

## 1. 当前合同一句话

给定 `NL + raw/source STM_0`，本合同只回答：

```text
哪些问题只是 candidate？哪些问题能 confirmed？哪些问题必须 rejected / out-of-scope / insufficient evidence？
```

本合同不运行 LLM、不执行 repair、不生成 `STM_final`、不冻结 final metric / baseline / judge prompt。

## 2. 核心文件

| 文件 | 职责 |
|---|---|
| [source_level_issue_definition.md](./source_level_issue_definition.md) | 定义 candidate、confirmed、rejected、out-of-scope、insufficient evidence，以及 `raw_internal_inconsistency` 第二确认路径。 |
| [issue_ledger_contract.md](./issue_ledger_contract.md) | 说明 JSON ledger 字段、状态机口径、repair eligibility gate 与后续 PR 接口。 |
| [GUIDE.md](./GUIDE.md) | 后续 agent / reviewer 如何维护本合同。 |
| [fixtures/README.md](./fixtures/README.md) | 人类可读 fixture 目录说明。 |

机器可校验事实源位于 [../../pipeline/evaluation/schemas/source_issue_ledger.schema.json](../../pipeline/evaluation/schemas/source_issue_ledger.schema.json) 与 [../../pipeline/evaluation/fixtures/source_issue_ledger/](../../pipeline/evaluation/fixtures/source_issue_ledger/)。

## 3. JSON fixture 与文档 fixture 的分工

- JSON fixture 是唯一 machine-verifiable 事实源。
- 本目录下的 `fixtures/*/README.md` 只做人类可读 narrative，不增加字段、不覆盖 JSON。
- 若二者冲突，以 JSON fixture + schema + pytest 为准，并同步修正文档。

## 4. 与后续 PR 的接口

| 后续 PR | 如何消费本合同 |
|---|---|
| `PR-source-trace` | 接管 `source_element_refs` 和 `required_future_trace`，定义 raw/source ↔ intermediate trace。 |
| `PR-loop-io` | 将本 ledger 放入 stage IO / run record 合同。 |
| `PR-discover-confirm` | 产生 candidate / confirmed issue ledger。 |
| `PR-repair-runner` | 只能修复 `confirmation_status=confirmed` 且 `downstream_repair_allowed=true` 的 issue。 |
| `PR-closure-audit` | 用 issue ledger 判断 repair 后 closure / regression。 |

## 5. 禁止误读

- 本合同不是 Better STM / which STM is better 判定。
- 本合同不是 final metric、baseline contract 或 judge prompt。
- `raw_internal_inconsistency` 是 v0 合同路径，后续必须结合真实 raw NL 例子、真实 discovery 能力和 pilot 输出复核。
- folded event / ugly expression 不自动 confirmed。
- conversion / lowering / normalization artifact 不计入 source-level issue 或 method gain。

## 6. 更新日志

| 时间 | 更新内容 |
|---|---|
| 2026-07-08 09:52:31 | 初始化 `PR-issue-ledger` issue lifecycle 合同入口、schema/fixture 指针与后续 PR 接口。 |
