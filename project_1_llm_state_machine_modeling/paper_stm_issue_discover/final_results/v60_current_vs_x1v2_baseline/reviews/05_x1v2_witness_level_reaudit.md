# X1v2 W0/W1/W2 回溯审计决策

## 结论

X1v2 的 predicate usage 不适用，但 W 轴适用。对冻结的 162 个 method record 中全部 512 条 arm-generated finding 进行了两轮独立、Judge-blinded 逐条审阅。两轮标签没有 W 级分歧；独立语义复核发现一条共同误标，pane5 以受限 post-review correction 将 `0036:r1:0036:r1:baseline_issue_4` 从 W1 裁为 W0。最终 finding-level `W0/W1/W2 = 1/511/0`。435 条 expected row 均已在双审后关联；211 个 `FULL` row 的 max-W 为 `W2/W1/W0 = 0/211/0`，L2 的 46 个 `FULL` row 为 `0/46/0`，`W2/全部 expected = 0/435`。

## 采用的定义

- W0：散文主张没有足够具体、可核对的模型元素或路径定位，也没有经过求值的可执行对象。
- W1：finding 明确定位 state、transition、guard、action、模型片段、缺失边或有限路径，但没有该方法产生且在精确制品上实际终止求值的对象。
- W2：除明确可执行对象外，还需要 X1v2 运行期的 evaluation receipt、精确 artifact hash 和 terminal true/false 或等价确定性结果。

X1v2 的 single-prompt/no-tools 架构只能推出“不属于 W2”，不能推出“只能 W0”。具体定位的 finding 可以是 W1。issue #189 中旧有“无工具所以 W0”的表述与其 W1 定义之间存在这个逻辑缺口；本归档按三档定义本身解释并修正本地报告，不修改外部 GitHub issue。

## 流程与边界

每条审阅单元是 `(pair_id, round, original_report_id)`。主审和复审分别读取原始 `issue`、`where`、`reason`、对应 hash-verified NL、PlantUML 与 source hash；两次 decision 文件分别保存在 `derived/x1v2_witness_review_decisions/primary/` 和 `secondary/`。`paper1.x1v2-witness-review-packet.v2` 不含 Judge 路径、hash、validity、expected relation 或 ledger ID。Judge validity、expected relation、later Judge inspection facts、current predicate/backend 都在双审结束后才用于关联或聚合，不能决定 baseline W，也不能事后制造 baseline W2。

两次审阅覆盖均为 `512/512`，两轮均判全部 finding 为 W1，没有 W-level 分歧，因此 [adjudication log](../derived/x1v2_witness_adjudications.json) 的 `adjudications` 为空。每个 W1 都保留由 reviewer 从冻结原文和 source closure 识别的具体 carrier、端点、动作、guard、模型片段或有限路径；没有 finding 具有 X1v2 自身的 executable object、evaluation receipt、evaluated artifact hash 与 terminal result 四件套，因此没有 W2。

## 事后独立复核与裁定

[独立语义审查](09_x1v2_witness_blind_semantic_metric_review.md) 在不使用 Judge linkage 的条件下，重新检查 raw `record.json#/parsed_output/issues/3`、blind packet 与 pair `0036` 的 NL/PlantUML，发现 `0036:r1:0036:r1:baseline_issue_4` 的 `where` 只有“整体状态机，特别是终止/完成相关建模”。它没有给出 state、transition、source/target、guard、action、有限路径或其他可核对 carrier。NL/PlantUML 中出现的对象不能替 finding 反向补足定位。因此该 finding 符合 W0，不符合 W1；它也没有 X1v2 运行期 executable witness，所以不能是 W2。

两份 blind decision 保留为原始 W1，不被改写。最终 audit 和 [adjudication log](../derived/x1v2_witness_adjudications.json) 增加 `post_review_correction`，其中保存独立 review 路径、共同原标签、最终标签、pane5 裁定者、专属 reason/basis 与原始 source pointer。该机制只接受这一个 allowlist key，验证器要求 review 路径为 archive 内存在的 `reviews/` 文件，并且该 review 正文点名同一 audit key。该 finding 是 `VALID_NOVEL` 且不在任何 `full_report_ids` 中，故修正只改变 finding-level、r1 和 `VALID_NOVEL` 分层，不改变 211 个 FULL hit、L2 FULL hit 或 `W2/全部 expected`。

`0050:r3:0050:r3:baseline_issue_1` 的 packet-fidelity 复核也已完成：其 `issue`、`where` 与 `finding_reason` 和 raw `/parsed_output/issues/0` 字节相同，`where` 中的 `\\n` 是 frozen source 的字面量，不是 packet 把真实换行序列化为文本。该结论由 [聚焦回归](../../../pipeline/evidence_discovery/tests/test_x1v2_witness_audit.py) 强制检查。

先前包含 `judge_association` 的 v1 审阅包、两轮决策、audit 和聚合已完整保存在 [superseded directory](../derived/superseded_judge_exposed_witness_review_v1/)。它们不会进入最终复算或报告。v1 的标签不用于支持 v2 的任何判断；接受的 v2 结论只来自其 label-free packet、两份独立 decision、事后独立语义 review 和上述受限裁定。

## 可复算性与限制

审计输入、逐条审阅、finding-level audit 和 FULL-hit aggregation 都已归档。`final_results_archive validate` 重新核对 162 个 record、54 个输入闭包、512 条双审 record、435 条 expected row、`full_report_ids` 和全部 SHA-256。审计未运行 method、Judge 或 provider，未修改 raw artifact、19 个谓词、registry、prompt、route 或 issue #195。
