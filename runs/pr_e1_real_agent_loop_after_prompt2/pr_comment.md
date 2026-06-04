## PR-E1 real-run evidence update

身份：主 session / PR-E1 runner。

本 comment 汇总当前已产出的真实 `method.loop.run_agent_loop` 运行证据；详细报告见仓库内 `runs/pr_e1_real_agent_loop_after_prompt2/`。

| Path | case | config | verdict | status | eligible | failure class | tokens | report |
|---|---|---|---|---|---:|---|---:|---|
| path2 | `path2_lng_ems` | `default` | `not_converged` | `rejected` | ❌ | `design_or_variable_dynamics` | 32838 | `runs/pr_e1_real_agent_loop_after_prompt2/pr-e1-path2_lng_ems-default-promptfix3-84c81104/report.md` |

### 初步观察

- `default`：0/1 success，rejected=1，budget_exhausted=0，total_tokens=32838。
- 当前证据尚未显示单纯增加 `max_iterations` 足以解决问题；若 run 早停于 `rejected`，瓶颈更可能是 prompt/repair candidate quality 或样本变量语义，而不是迭代预算本身。

### 主要失败模式

- `design_or_variable_dynamics`：1 run(s)。
- `design_or_variable_dynamics` 与变量只读不写、guard 变量永不变化等风险相关，需在样本筛选和 SL-9 prompt 中区分环境输入变量与内部状态变量。
