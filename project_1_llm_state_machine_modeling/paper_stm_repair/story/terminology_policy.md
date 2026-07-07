# terminology_policy.md — paper1 术语口径

## 1. 推荐术语表

| 中文 | English | 使用口径 |
|---|---|---|
| 原始 / 源层状态机 | raw/source STM | 输入模型和最终评价落点。 |
| 初始源层模型 | raw/source `STM_0` | 给定 `NL` 后已有的状态机制品。 |
| 中间语义执行表示 | intermediate executable semantic representation | 用于 diagnostics / simulation / verification feedback；可由 `fcstm` 承载。 |
| 候选问题 | candidate issue | 工具或 LLM 提示的可疑问题。 |
| 已确认源层行为问题 | confirmed source-level behavioral issue | 经过 `NL + raw/source element + behavior evidence` 确认的问题。 |
| 问题发现 | issue discovery | 产生 candidate issue。 |
| 严格确认 | strict confirmation | 把 candidate issue 判为 confirmed / unconfirmed / unjudgeable。 |
| 问题绑定修复 | issue-grounded repair | repair 必须绑定 `issue_id`。 |
| 源层补丁包 | source-level patch bundle | 可回投到 raw/source 层的 patch / diff / explanation。 |
| 闭合审计 | closure audit | 判断原 issue 是否 closed / partially closed / not closed / over-repaired / unjudgeable。 |
| 回归审计 | regression audit | 判断是否引入新 source-level issue。 |
| 无法投影 | untraceable / unsupported projection | 中间修改无法可靠回到 source 层。 |

## 2. 禁用或降级术语

| 术语 | 当前处理 |
|---|---|
| Better STM | 只允许 historical / superseded / archive-pending / claims-to-avoid。 |
| which STM is better | 不作为 active research question。 |
| relatively better STM | 不作为 headline；必要时只在解释旧框架时出现。 |
| repair target taxonomy | 旧 R5.7 术语；新主线优先写 issue ledger / issue taxonomy。 |
| `fcstm` contribution | 禁止。 |
| conversion gain | 禁止；conversion 只能是 infrastructure。 |
| model runnable = correct | 禁止。 |
| objective metric proves improvement | 禁止；指标最多是 supporting evidence。 |

## 3. 写作替换规则

| 避免写法 | 推荐写法 |
|---|---|
| 生成更好的 `STM_k` | 发现并闭合 source-level behavioral issues，输出 source-level patch bundle 或 final raw/source `STM_k`。 |
| 通过 fcstm 改进模型 | 使用中间可执行语义表示获得工具反馈，并将修复证据回投到 source 层。 |
| folded event 是错误 | folded event 是 candidate symptom，需经 `NL + source + behavior evidence` 确认。 |
| Better STM gate | closure / regression audit。 |
| repair target | confirmed issue / issue_id-bound repair target。 |
| baseline 已定义 | baseline contract 将在 pilot 后冻结。 |

## 4. 中英文一致性

- 首次出现时可写 “已确认源层行为问题（confirmed source-level behavioral issue）”。
- 后续可简写为 “confirmed issue”，但不得省略 source-level 语义。
- “source-level” 保留英文，避免中文“源层”与代码层 / 数据源混淆。
- “closure” 和 “regression” 可保留英文，以便与后续 ledger verdict 对齐。

## 5. 更新日志

| 时间 | 更新内容 |
|---|---|
| 2026-07-07 21:20:00 | 术语从 Better STM / repair target 框架改为 issue discovery / confirmation / repair / closure / regression。 |
