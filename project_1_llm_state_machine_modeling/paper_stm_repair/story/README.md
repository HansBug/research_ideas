# story/ — 主线、边界与 claim gate

## 1. 职责

`story/` 负责把第一篇论文的新主线写成可审阅、可反驳、可继承的 story contract。这里的文档是后续 PR-R7 写论文正文前的事实与写作栅栏，不是最终 manuscript。

## 2. 文件说明

| 文件 | 作用 |
|---|---|
| [paper_story.md](./paper_story.md) | 冻结 thesis、gap、insight、贡献草案、证据需求和禁止 claim。 |
| [task_boundary.md](./task_boundary.md) | 冻结 `<NL, STM_0> -> STM_k` 输入输出、人类角色、seed / repair loop 边界和失败模式。 |
| [terminology_policy.md](./terminology_policy.md) | 冻结 `fcstm` / `pyfcstm` / DSL 弱化策略、推荐表达与禁止表达。 |
| [claim_evidence_map.md](./claim_evidence_map.md) | 将主要 claim 映射到证据需求、当前状态、后续 PR 和安全降级写法。 |
| [paper_outline.md](./paper_outline.md) | 给出论文大纲草案，只冻结结构，不写最终正文。 |

## 3. 硬约束

1. 不把第一篇写成 `NL -> STM` 生成论文。
2. 不把 `fcstm` / `pyfcstm` / DSL 写成论文主贡献。
3. 不声称完整形式化验证、sound model checking 或已证明 correctness。
4. 不把转换器、人工规范化或 seed construction 收益计入 repair-loop 贡献。
5. 不把失败、回滚、振荡、不收敛从结果中消失。
