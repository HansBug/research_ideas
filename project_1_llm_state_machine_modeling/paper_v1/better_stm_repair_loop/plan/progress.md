# PR-R0 Progress

## 1. 当前阶段

| 字段 | 状态 |
|---|---|
| PR | [#102](https://github.com/HansBug/research_ideas/pull/102) |
| 上游 | [#100](https://github.com/HansBug/research_ideas/pull/100) |
| 分支 | `paper1/r0-story-scope-freeze` |
| 当前阶段 | R0 文档落地与实现后 review 准备 |
| 是否跑四例真实样例 | 否；R0 是文档 / story gate。 |
| 是否调用真实 LLM | 否。 |

## 2. 本轮输入

- [PR #100 body](https://github.com/HansBug/research_ideas/pull/100)
- [PR #99 会后定调 comment](https://github.com/HansBug/research_ideas/pull/99#issuecomment-4689018818)
- [2026-06-12 导师讨论记录](../../../talks/2026-06-12-导师-两篇论文转向与模型修正定调.md)
- PR #102 plan review comments：codex / claude / deepseek 均 C=0/I=0。
- 旧路径结构只读调研：参考 PR #93/#96 `path1_foundation/` 的分层经验，不继承旧 story。

## 3. 已落地产物

| 路径 | 作用 |
|---|---|
| [../README.md](../README.md) | 新主线入口。 |
| [../story/](../story/) | story、task boundary、terminology、claim map、outline。 |
| [../evidence/](../evidence/) | upstream fact ledger 与 legacy inheritance。 |
| [../experiment_design/](../experiment_design/) | RQ 草案、Better STM 定义、评价门原则。 |
| [./README.md](./README.md)、[agent_provenance.md](./agent_provenance.md) | PR 执行记录与 reviewer provenance。 |

## 4. 本地检查计划

实现提交前后至少执行：

```bash
git diff --check
git status --short
rg -n "首个|最强|new DSL|fcstm.*贡献|pyfcstm.*贡献|完整形式化验证|outperform|提升质量" project_1_llm_state_machine_modeling/paper_v1/better_stm_repair_loop project_1_llm_state_machine_modeling/paper_v1/README.md
find project_1_llm_state_machine_modeling/paper_v1/better_stm_repair_loop -type f | sort
```

## 5. Coverage / CI 口径

本 PR 是 docs/story gate，不新增 Python 代码，不应虚构 Codecov delta。coverage proxy 使用：

1. GitHub Actions `feedback-smoke` 状态；
2. `git diff --check`；
3. forbidden wording grep；
4. 实现后三路 reviewer 审查。

## 6. 剩余风险

| 风险 | 当前处理 |
|---|---|
| 旧 `paper_v1/README.md` 导致读者回到 Path-1 hard comparison | 本 PR 顶部增加新主线提示，并在 [../evidence/legacy_asset_inheritance.md](../evidence/legacy_asset_inheritance.md) 记录共存策略。 |
| R0 文件过度定义 R4/R6 评价门 | [../experiment_design/evaluation_gate.md](../experiment_design/evaluation_gate.md) 首段声明其不是 R4 v0。 |
| 后续把分支局部 PR #94/#96 写成 main 事实 | [../evidence/upstream_fact_ledger.md](../evidence/upstream_fact_ledger.md) 明确事实等级。 |
| 结果型 claim 过早出现 | [../story/claim_evidence_map.md](../story/claim_evidence_map.md) 与 grep 自检共同约束。 |
