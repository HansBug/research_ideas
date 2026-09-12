# 独立 Raw 审查

审查者为未参与本次 live run 的只读 subagent。审查直接读取 `raw/method/b3502e6aa068493596472f98f57f9b49/`、`raw/judge/e3e95eb94f6c45289d7b32b7b865ccfb/` 和永久 v60 15-pair x 3 raw artifacts；未调用 provider，未修改文件，也未将当前 comparison 汇总作为数字来源。

## 检查范围与结论

- method 为 15/15 `completed`，Judge 为 15/15 PairJudgeResult；固定 pair 与一轮 scope 均正确。
- 15 个 method `pair_input_hashes` 均与 v60 三轮对应 cell 相等。Judge protocol 为 `github-issue-195.d774d9bd3e4c.issue-189-clarification.v3.2`，SHA-256 为 `d774d9bd3e4c4fe04735ed1d4ec064be197cfadcd52e21c8226e37175b29b210`。
- 所有 FULL/PARTIAL report ID 均可解析至 Judge report outcome 和 method evidence record；143 个 report outcome、60 个 expected outcome 均有非空 reason 和 basis。
- 独立计数得到 overall FULL `49/60`、L2 FULL `23/24`、K/N/I `92/48/3`、semantic precision `140/143`；FULL-hit max-W2/W1/W0 为 `34/15/0`，共同分母为 49。
- 精确 typed terminal carrier 交集为 104，matched same-input terminal verdict flips 为 0。before-only/after-only 分别为 109/26；one-sided carrier 仅反映独立 candidate/route surface，未计入 same-input flip。
- v60 三轮的 overall FULL 为 `43/60`、`44/60`、`45/60`；L2 FULL 为 `22/24`、`22/24`、`20/24`；semantic precision 为 `128/139`、`131/143`、`137/144`。新 run 高于这三轮的 hit 与 precision 包络，但这不是 refactor 改进的因果证据；结合零 matched flip、输入闭包和资源/协议不变量，它也不构成结构回退证据。

## 审查发现与处理

审查初稿将 `W2/全部 expected` 错算为仅 FULL hit 的 W2，得到 `34/60`；正式口径为每个 expected row 的 FULL 或 PARTIAL supporting reports 的最高 W，因此正确结果是 `39/60 (65.00%)`。初稿还把包含计划外 `R2` 的 11 个全部 terminal predicates 写成计划 12 谓词 usage；正确计划内 usage 为 `10/12`，未使用 `S6`、`V1`，全部 terminal distinct predicates 仍为 11。主会话已在 evaluator/reporting 中修正分母与展示，并保留 `R2` 作为非计划 receipt，不删除原始数据。

随后主会话发现 v60 子集的 stage-loss 派生器错误地读取了 full composite 的 54-pair 行。修正后 builder 接受只读 pair/round subset，并优先使用 archive-local Judge `source_runs`；重建产物为 45 cells、180 expected rows，所有派生路径均为仓库相对路径。live 前的 `validation_manifest_pre_reporting_scope_correction.json` 保留为审计快照；当前 `validation_manifest.json`、reference 和两次输入闭包检查已在相同 raw cells/config 下重新闭合。该修正不改变 method/Judge 原始制品、fixed pair、run id、prompt、registry、输入 SHA-256 或任何 provider 调用。

这些是 reporting aggregation scope 问题，不是 method、Judge、registry、predicate 或 raw artifact 的语义变化。更正后没有 high-severity 未解决发现。
