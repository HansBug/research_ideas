# STM Source Landscape Claim-Evidence Map

## 1. 使用方式

任何 Abstract / Introduction / Conclusion headline claim 必须先查本文件。若证据状态不是 `strong_after_gate`，只能使用限定写法或移到 Discussion / Future Work。

## 2. Claim gate 总表

| Claim | 当前证据 | 状态 | 安全写法 | 禁止写法 |
|---|---|---|---|---|
| `sources/` 已形成大规模控制系统 STM source corpus | 787 篇 / 746 案例 planning baseline；需正式 snapshot 复算 | `pending_snapshot` | “we analyze a curated corpus snapshot of control-system papers” | “largest / complete corpus” |
| corpus 可支撑 benchmark-source landscape | 质量标签、结构标签、角色分布；需 G4/G7/G9 | `careful` | “benchmark-source landscape / evidence-informed benchmark design” | “ready-to-use public benchmark” |
| 本文是 retrospective SMS with audit protocol | issue #85 G1 规划；本 PR 不完成 G1 | `pending_protocol` | “retrospective systematic mapping with audit protocol” | “PRISMA-compliant SLR” |
| D1--D7 related-work 初筛已定位高风险近邻 | 本 PR 69 行矩阵、P0/P1 BibTeX、targeted search audit | `working_evidence` | “plan-stage related-work screening identifies candidates for fulltext verification” | “we have verified all direct competitors” |
| artifact copyright-safe | 本 PR 只提交 metadata/BibTeX/CSV，不提交 PDF/全文；G0 未完成 | `partial` | “this PR follows a metadata-only policy” | “the final artifact is already copyright-safe” |
| LLM pilot / benchmark performance | 当前无真实 LLM pilot | `avoid` | 仅作未来工作或 G10 条件 | “we show LLMs perform…” |

## 3. 当前 PR 不能说什么

- 不能说最终 Related Work 已完成。
- 不能说 P0 都是 verified direct competitors。
- 不能把 `Skip` 行当成最终排除，尤其是 `auto_fulltext_light_review_flag=yes` 的 7 行。
- 不能把 #95 元数据字段当作已核验 bibliographic facts。
