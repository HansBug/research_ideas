# story/ — 论文主线真源

## 1. 职责

`story/` 是第一篇新主线的写作与学术口径真源。它回答：这篇论文研究什么、不研究什么、如何命名、哪些 claim 能写、哪些 claim 必须禁止。

## 2. 文件职责

| 文件 | 职责 |
|---|---|
| [paper_story.md](./paper_story.md) | thesis、gap、technical challenge、method insight、贡献方向、证据需求和 reviewer 风险。 |
| [task_boundary.md](./task_boundary.md) | `<NL, STM_0> -> STM_k` 的输入输出、方法内外范围、人类角色、停止 / 回滚边界。 |
| [terminology_policy.md](./terminology_policy.md) | `fcstm` / `pyfcstm` / DSL 弱化策略、推荐用语、禁止用语和自检方式。 |
| [claim_evidence_map.md](./claim_evidence_map.md) | claim 与证据的对应关系、当前证据状态、降级写法和禁止 claim。 |
| [paper_outline.md](./paper_outline.md) | 论文大纲草案；只冻结结构和写作约束，不写最终正文。 |

## 3. 高优先级约束

1. 第一篇不再主打 `NL -> STM` 生成，而是 `<NL, STM_0> -> STM_k / Better STM` 修正任务。
2. `NL -> STM_0` 只作为 seed construction / baseline source / related work，不作为主贡献。
3. 修正运行内部是无人化循环；人类可参与 benchmark、reference/adjudication 和最终审计。
4. `fcstm` / `pyfcstm` / DSL 只作实现载体，不进标题、摘要或贡献位。
5. 所有结果型 claim 必须等待 R4/R6 评价门和主实验结果；R0 只冻结可检验 story。

## 4. 上游事实源

- [PR #100](https://github.com/HansBug/research_ideas/pull/100)
- [PR #99 会后定调 comment](https://github.com/HansBug/research_ideas/pull/99#issuecomment-4689018818)
- [2026-06-12 导师讨论记录](../../../talks/2026-06-12-导师-两篇论文转向与模型修正定调.md)
- [project_1 talks SUMMARY](../../../talks/SUMMARY.md)
