## PR-E1 baseline real-run evidence update

身份：主 session / PR-E1 runner。

本 comment 汇总当前已产出的真实 `method.loop.run_agent_loop` 运行证据；详细报告见仓库内 `runs/pr_e1_real_agent_loop/`。

| Path | case | config | verdict | status | eligible | failure class | tokens | report |
|---|---|---|---|---|---:|---|---:|---|
| path1 | `path1_cara` | `default` | `not_converged` | `rejected` | ❌ | `semantic_or_topology` | 14630 | `runs/pr_e1_real_agent_loop/pr-e1-path1_cara-default-baseline0-873fbcc4/report.md` |
| path2 | `path2_lng_ems` | `default` | `provider_error` | `error` | ❌ | `provider_or_retry` | 6703 | `runs/pr_e1_real_agent_loop/pr-e1-path2_lng_ems-default-baseline0-d0319027/report.md` |

### 初步观察

- `default`：0/2 success，rejected=1，budget_exhausted=0，total_tokens=21333。
- 当前证据尚未显示单纯增加 `max_iterations` 足以解决问题；若 run 早停于 `rejected`，瓶颈更可能是 prompt/repair candidate quality 或样本变量语义，而不是迭代预算本身。

### 主要失败模式

- `provider_or_retry`：1 run(s)。
- `semantic_or_topology`：1 run(s)。
- parse/semantic/topology 类问题说明 pyfcstm grammar 与层次路径约束仍需更强 prompt 约束或 repair context。
