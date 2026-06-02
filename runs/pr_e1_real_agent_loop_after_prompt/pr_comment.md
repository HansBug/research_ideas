## PR-E1 baseline real-run evidence update

身份：主 session / PR-E1 runner。

本 comment 汇总当前已产出的真实 `method.loop.run_agent_loop` 运行证据；详细报告见仓库内 `runs/pr_e1_real_agent_loop_after_prompt/`。

| Path | case | config | verdict | status | eligible | failure class | tokens | report |
|---|---|---|---|---|---:|---|---:|---|
| path1 | `path1_cara` | `default` | `not_converged` | `rejected` | ❌ | `design_or_variable_dynamics` | 15830 | `runs/pr_e1_real_agent_loop_after_prompt/pr-e1-path1_cara-default-promptfix2-5e21d64d/report.md` |
| path1 | `path1_cara` | `iter3` | `not_converged` | `rejected` | ❌ | `design_or_variable_dynamics` | 14733 | `runs/pr_e1_real_agent_loop_after_prompt/pr-e1-path1_cara-iter3-promptfix2budget-0a0b1d0b/report.md` |
| path1 | `path1_cara` | `iter8` | `not_converged` | `rejected` | ❌ | `grounding_or_required_element_loss` | 14596 | `runs/pr_e1_real_agent_loop_after_prompt/pr-e1-path1_cara-iter8-promptfix2budget-ad4fab4c/report.md` |
| path2 | `path2_lng_ems` | `default` | `not_converged` | `rejected` | ❌ | `design_or_variable_dynamics` | 18729 | `runs/pr_e1_real_agent_loop_after_prompt/pr-e1-path2_lng_ems-default-promptfix2-992c95ed/report.md` |

### 初步观察

- `default`：0/2 success，rejected=2，budget_exhausted=0，total_tokens=34559。
- `iter3`：0/1 success，rejected=1，budget_exhausted=0，total_tokens=14733。
- `iter8`：0/1 success，rejected=1，budget_exhausted=0，total_tokens=14596。
- 当前证据尚未显示单纯增加 `max_iterations` 足以解决问题；若 run 早停于 `rejected`，瓶颈更可能是 prompt/repair candidate quality 或样本变量语义，而不是迭代预算本身。

### 主要失败模式

- `design_or_variable_dynamics`：3 run(s)。
- `grounding_or_required_element_loss`：1 run(s)。
- `design_or_variable_dynamics` 与变量只读不写、guard 变量永不变化等风险相关，需在样本筛选和 SL-9 prompt 中区分环境输入变量与内部状态变量。
- `grounding_or_required_element_loss` 表示 repair 虽可能通过局部语法/语义检查，但丢失 NL-grounded required elements；这类结果不能因更高预算而算作改善。
