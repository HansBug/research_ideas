## PR-E1 real-run evidence update

身份：主 session / PR-E1 runner。

本 comment 汇总当前已产出的真实 `method.loop.run_agent_loop` 运行证据；详细报告见仓库内 `../runs/pr_langgraph_real_agent_loop_round1_stategraph/`。

| Path | case | config | verdict | status | clean | eligible | path2 blueprint | failure class | token usage | report |
|---|---|---|---|---|---:|---:|---|---|---|---|
| path1 | `path1_abs` | `default` | `success` | `success` | ✅ | ✅ | ⚪ | `success` | 33129 | `../runs/pr_langgraph_real_agent_loop_round1_stategraph/pr-e1-path1_abs-default-prlanggraph-stategraph-r1-fb795195/report.md` |
| path1 | `path1_cara` | `default` | `success` | `success` | ✅ | ❌ | ⚪ | `success_but_weak_oracle_ineligible` | 618025 | `../runs/pr_langgraph_real_agent_loop_round1_stategraph/pr-e1-path1_cara-default-prlanggraph-stategraph-r1-06cfac95/report.md` |
| path1 | `path1_elevator` | `default` | `success` | `success` | ✅ | ✅ | ⚪ | `success` | 33592 | `../runs/pr_langgraph_real_agent_loop_round1_stategraph/pr-e1-path1_elevator-default-prlanggraph-stategraph-r1-0cdc09ec/report.md` |
| path2 | `path2_lng_ems` | `default` | `success` | `success` | ✅ | ❌ | ❌ | `success_but_weak_oracle_ineligible` | 943667 | `../runs/pr_langgraph_real_agent_loop_round1_stategraph/pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f/report.md` |

### 可复现性边界

- clean commit 绑定：4/4 run 的 `reproducibility.json` 记录 dirty=false。
- prompt snapshot hash 种类：1；用于确认同一轮 4 例是否共享同一 prompt/context 版本。
- 每个 run 的 `reproducibility.json` 保存 git commit、dirty flag、diff hash、prompt file hash、runner command/config 与 source/paper path。

### 初步观察

- `default`：4/4 success，rejected=0，budget_exhausted=0，total_tokens=1628413。
- 主结果候选：当前 2/4 个非 infrastructure run 可进入 main_result_eligible；provider/network invalid=0 个，只能作为 infrastructure evidence。

### 主结果候选 vs Path2 ref-model 蓝本边界

- Path2 run-validity：0/1 个 Path2 run 的 `main_result_eligible=true`；这只表示 run/schema/secret/trace/final verdict 可进入主结果候选。
- Path2 blueprint-validity：0/1 个 Path2 run 当前可作为 `path2_ref_model_blueprint_eligible=true`；该字段比 `main_result_eligible` 更严格。
- `path2_lng_ems`：main_result_eligible=`false`，path2_ref_model_blueprint_eligible=`false`，state_mode_decorative=`true`；reason=run_not_main_result_eligible
- 解释：`path2_ref_model_blueprint_eligible=false` 不会把有效 run 改成 provider invalid；它只禁止把 state-mode-decorative / 条件分类式模型宣传为 Path2 ref-model 主蓝本。

### 主要失败模式

- `success`：2 run(s)。
- `success_but_weak_oracle_ineligible`：2 run(s)。

### 样本筛选观察

- 样本覆盖：4 个 case，Path1=3，Path2=1。
- `path1_abs`：失败/成功类别=success，最大 observed iteration_count=1。
- `path1_cara`：失败/成功类别=success_but_weak_oracle_ineligible，最大 observed iteration_count=3。
- `path1_elevator`：失败/成功类别=success，最大 observed iteration_count=1。
- `path2_lng_ems`：失败/成功类别=success_but_weak_oracle_ineligible，最大 observed iteration_count=5。
- 实证筛选更新：外部输入变量（plant/sensor/environment read-only）与内部状态变量必须分开标注；只读外部输入可接受，但不能被误写成‘变量参与充分’。
- 实证筛选更新：纯输出变量（只写不读）可用于 Path1 行为展示，但需要 admitted-abstraction / output-only 说明；不应拿来证明变量驱动控制流。
- 实证筛选更新：若最终 DSL 的状态主要由无记忆 `! *` 条件重选，状态只是分类标签，应标为 state_mode_decorative；可作 FE/BVS 压力测试，不宜作为 Path2 state-machine ref-model 主蓝本。

### Reviewer 追加审查项：禁止样本特判 / benchmark overfit

- 后续三路 reviewer 需显式检查 agent-loop / prompt / deterministic policy 是否包含针对 ABS、CARA、Elevator、LNG EMS 或本 PR 4 个样本的 lexical special-case、case_id 分支、hard-coded hint、结果导向参数。
- 允许的优化必须是普适、可解释、可迁移的机制；例如通过 prompt 要求 LLM 区分外部输入与内部状态，而不是在代码中写样本专用词表。
- 若发现样本特判影响 blocking/advisory、repair target、scenario oracle 或主结论归类，应至少按 I 级处理；若污染 main_result_eligible 或论文结论则按 C 级处理。

### 4 例详细输入 / 输出 / artifact

<details><summary>path1 / path1_abs / default / success</summary>

#### NL 输入（原文）

```text
The paper implements the single-wheel ABS hydraulic regulator as a three-state FSM coupled with a PID-based slip controller. Wheel speed and vehicle speed are used to compute the slip ratio, and the PID output drives the Stateflow supervisor instead of sending commands directly to the hydraulic valves.

The FSM contains the states `increase`, `hold`, and `decrease`, where `increase` sets `k1=1, k2=0, n=0`, `hold` neutralizes both valves with `k1=0, k2=0, n=0`, and `decrease` sets `k1=0, k2=1, n=500` to release pressure.

The transition guards split the slip-error space into four bands: `increase -> hold` when `slp <= 0.01`, `hold -> increase` when `slp > 0.01`, `hold -> decrease` when `slp < -0.01`, and `decrease -> hold` when `slp >= -0.01`.

This gives a concrete discrete supervisor that maps slip-error thresholds to inlet-valve, return-valve, and pump actions while the continuous wheel-slip dynamics remain in the plant model.
```

#### NL 输入中文翻译

```text
论文把单轮 ABS 液压调节器实现为一个三状态 FSM，并与基于滑移率的 PID 控制器耦合。轮速与车速用于计算滑移率，PID 输出驱动 Stateflow 监督器，而不是直接发送液压阀命令。

FSM 包含 `increase`、`hold`、`decrease` 三个状态：`increase` 设置 `k1=1, k2=0, n=0`，`hold` 设置 `k1=0, k2=0, n=0`，`decrease` 设置 `k1=0, k2=1, n=500` 以释放压力。

转移 guard 把滑移误差空间分成四个区间：`increase -> hold` 当 `slp <= 0.01`，`hold -> increase` 当 `slp > 0.01`，`hold -> decrease` 当 `slp < -0.01`，`decrease -> hold` 当 `slp >= -0.01`。

这给出了一个具体的离散监督器，把滑移误差阈值映射为进油阀、回油阀与泵动作，而连续轮胎滑移动力学仍留在被控对象模型中。
```

#### FCSTM 输出

```pyfcstm
def float slp = 0.0;
def int k1 = 0;
def int k2 = 0;
def int n = 0;

state SingleWheelABSHydraulicRegulator {
    [*] -> increase;

    state increase {
        enter {
            k1 = 1;
            k2 = 0;
            n = 0;
        }
    }

    state hold {
        enter {
            k1 = 0;
            k2 = 0;
            n = 0;
        }
    }

    state decrease {
        enter {
            k1 = 0;
            k2 = 1;
            n = 500;
        }
    }

    increase -> hold : if [slp <= 0.01];
    hold -> increase : if [slp > 0.01];
    hold -> decrease : if [slp < -0.01];
    decrease -> hold : if [slp >= -0.01];
}
```

#### agent-loop 过程与日志路径

| 项 | 值 |
|---|---|
| verdict / status | `success` / `success` |
| failure class | `success` |
| main_result_eligible | `true` |
| path2_ref_model_blueprint | `n/a`；not_applicable_to_path1 |
| state_mode_decorative | `false` |
| executed stages | `SC-0 -> SL-1 -> SD-2 -> SD-3 -> SD-4 -> SL-5 -> SD-5A -> SC-5F -> SD-6 -> SL-7 -> SC-12 -> SC-13` |
| iter / repairs / accepted / scenarios | `1` / `0` / `0` / `1` |
| token / elapsed | `{'prompt_tokens': 27170, 'completion_tokens': 5959, 'total_tokens': 33129, 'estimated_prompt_tokens': 26480, 'estimated_completion_tokens': 3970, 'estimated_total_tokens': 30450, 'prompt_chars': 105916, 'completion_chars': 15875, 'n_calls': 3, 'token_usage_available': True, 'token_usage_unavailable_calls': 0}` / `117.224s` |
| full stage table | `../runs/pr_langgraph_real_agent_loop_round1_stategraph/pr-e1-path1_abs-default-prlanggraph-stategraph-r1-fb795195/report.md` §4 |
| run record | `../runs/pr_langgraph_real_agent_loop_round1_stategraph/pr-e1-path1_abs-default-prlanggraph-stategraph-r1-fb795195/pr-e1-path1_abs-default-prlanggraph-stategraph-r1-fb795195.agent_loop.json.gz` |
| logs | `../runs/pr_langgraph_real_agent_loop_round1_stategraph/pr-e1-path1_abs-default-prlanggraph-stategraph-r1-fb795195/run_logs/stdout.txt`, `../runs/pr_langgraph_real_agent_loop_round1_stategraph/pr-e1-path1_abs-default-prlanggraph-stategraph-r1-fb795195/run_logs/stderr.txt` |
| checks / repro | `../runs/pr_langgraph_real_agent_loop_round1_stategraph/pr-e1-path1_abs-default-prlanggraph-stategraph-r1-fb795195/checks.json`, `../runs/pr_langgraph_real_agent_loop_round1_stategraph/pr-e1-path1_abs-default-prlanggraph-stategraph-r1-fb795195/reproducibility.json` |

#### 全流程摘要表（report §4 摘录）

| Stage | 是否 LLM | iteration | 结果 | 获取的信息 / 反馈 | 本阶段做了什么 | DSL 修改 | artifact/log |
|---|---:|---:|---:|---|---|---|---|
| `SC-0` | 否 | - | ✅ | trace/control | 初始化 run state | 无/见 record | [`record`](./pr-e1-path1_abs-default-prlanggraph-stategraph-r1-fb795195.agent_loop.json.gz) |
| `SL-1` | 是 | - | ✅ | LLM calls=1, tokens=9116 | 生成初始 DSL 与 grounding seeds | initial len=634 | [`record`](./pr-e1-path1_abs-default-prlanggraph-stategraph-r1-fb795195.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_abs-default-prlanggraph-stategraph-r1-fb795195.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_abs-default-prlanggraph-stategraph-r1-fb795195.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=8, info=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_abs-default-prlanggraph-stategraph-r1-fb795195.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=1, tokens=11912 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_abs-default-prlanggraph-stategraph-r1-fb795195.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_abs-default-prlanggraph-stategraph-r1-fb795195.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_abs-default-prlanggraph-stategraph-r1-fb795195.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_abs-default-prlanggraph-stategraph-r1-fb795195.agent_loop.json.gz) |
| `SL-7` | 是 | 0 | ✅ | LLM calls=1, tokens=12101 | LLM model review | 无/见 record | [`record`](./pr-e1-path1_abs-default-prlanggraph-stategraph-r1-fb795195.agent_loop.json.gz) |
| `SC-12` | 否 | - | ✅ | full_pass_all_required_feedback_ok | 写 final verdict | 无/见 record | [`record`](./pr-e1-path1_abs-default-prlanggraph-stategraph-r1-fb795195.agent_loop.json.gz) |
| `SC-13` | 否 | - | ✅ | trace/control | 写审计 run record | 无/见 record | [`record`](./pr-e1-path1_abs-default-prlanggraph-stategraph-r1-fb795195.agent_loop.json.gz) |

### 4.1 完整流程日志（stage/control-flow replay ledger）

口径：本节来自 `AgentLoopRunRecord.logs`，与 [`flow_log.json`](./flow_log.json) 一致；用于复现每个 stage 如何进入、得到什么批示、跳转到哪里，以及每次 DSL 产物/候选如何变化。

| # | ts | stage | iter | event | result / jump | DSL evidence |
|---:|---|---|---:|---|---|---|
| 1 | `2026-06-04T14:51:22Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 2 | `2026-06-04T14:51:22Z` | `SC-0` | `-` | `run_start` | {} | <none> |
| 3 | `2026-06-04T14:51:22Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 4 | `2026-06-04T14:51:22Z` | `SL-1` | `-` | `stage_enter` | {"reason": "initial_modeling_adapter_available"} | <none> |
| 5 | `2026-06-04T14:52:14Z` | `SL-1` | `-` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 6 | `2026-06-04T14:52:14Z` | `SL-1` | `-` | `stage_result` | {"jump": "SD-2", "ok": true} | candidate_dsl:len=634,hash=sha256:5a3dc31a6a97 |
| 7 | `2026-06-04T14:52:14Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 8 | `2026-06-04T14:52:14Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 9 | `2026-06-04T14:52:14Z` | `<control>` | `0` | `iteration_enter` | {} | current_hash=sha256:5a3dc31a6a9720ad0701d515d530f63a006e9ee655c5d5284ff63f179cdf6726 |
| 10 | `2026-06-04T14:52:14Z` | `<control>` | `0` | `iteration_validation_enter` | {} | dsl:len=634,hash=sha256:5a3dc31a6a97, current_hash=sha256:5a3dc31a6a9720ad0701d515d530f63a006e9ee655c5d5284ff63f179cdf6726 |
| 11 | `2026-06-04T14:52:14Z` | `SD-2` | `0` | `stage_enter` | {"reason": "full_validation_pass"} | <none> |
| 12 | `2026-06-04T14:52:14Z` | `SD-2` | `0` | `stage_result` | {"jump": "SD-3", "ok": true, "status": "StageStatus.OK"} | <none> |
| 13 | `2026-06-04T14:52:14Z` | `SD-3` | `0` | `stage_enter` | {"reason": "SD-2 ok"} | <none> |
| 14 | `2026-06-04T14:52:14Z` | `SD-3` | `0` | `stage_result` | {"jump": "SD-4", "ok": true, "status": "StageStatus.OK"} | <none> |
| 15 | `2026-06-04T14:52:14Z` | `SD-4` | `0` | `stage_enter` | {"reason": "SD-3 ok"} | <none> |
| 16 | `2026-06-04T14:52:14Z` | `SD-4` | `0` | `stage_result` | {"jump": "SL-5", "ok": true, "status": "StageStatus.OK"} | <none> |
| 17 | `2026-06-04T14:52:14Z` | `SL-5` | `0` | `stage_enter` | {"reason": "scenario_set_absent"} | <none> |
| 18 | `2026-06-04T14:52:46Z` | `SL-5` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 19 | `2026-06-04T14:52:47Z` | `SD-5A` | `0` | `stage_result` | {"jump": "SC-5F", "ok": true, "status": "StageStatus.OK"} | <none> |
| 20 | `2026-06-04T14:52:47Z` | `SC-5F` | `0` | `stage_result` | {"jump": "SD-6", "ok": true} | <none> |
| 21 | `2026-06-04T14:52:47Z` | `SD-6` | `0` | `stage_enter` | {"reason": "scenario_set_ready"} | <none> |
| 22 | `2026-06-04T14:52:47Z` | `SD-6` | `0` | `stage_result` | {"jump": "SL-7", "ok": true, "status": "StageStatus.OK"} | <none> |
| 23 | `2026-06-04T14:52:47Z` | `SL-7` | `0` | `stage_enter` | {"reason": "SD-6 ok"} | <none> |
| 24 | `2026-06-04T14:53:19Z` | `SL-7` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 25 | `2026-06-04T14:53:19Z` | `SL-7` | `0` | `stage_result` | {"jump": "SC-12 success", "ok": true, "status": "StageStatus.OK"} | <none> |
| 26 | `2026-06-04T14:53:19Z` | `SL-7` | `0` | `grounding_update_hints_recorded` | {} | <none> |
| 27 | `2026-06-04T14:53:19Z` | `<control>` | `0` | `iteration_validation_result` | {"jump": "SC-12 success", "selected_feedback": null} | <none> |
| 28 | `2026-06-04T14:53:19Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 29 | `2026-06-04T14:53:19Z` | `SC-12` | `-` | `sc12_verdict` | {"reason": "full_pass_all_required_feedback_ok", "verdict": "success"} | final_dsl:len=634,hash=sha256:5a3dc31a6a97 |
| 30 | `2026-06-04T14:53:19Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 31 | `2026-06-04T14:53:19Z` | `SC-13` | `-` | `run_end` | {"verdict": "success"} | final_dsl:len=634,hash=sha256:5a3dc31a6a97 |
| 32 | `` | `<control>` | `-` | `langgraph_node_trace` | {} | <none> |

#### Scenario 逐轮通过矩阵（report §6.1 摘录）

口径：`✅` = 该 scenario 在该轮 SD-6 simulation 通过；`❌` = 该轮失败；`⚪` = 该轮未执行或无该 scenario 结果。

| Scenario | Intent | Iter 1 |
|---|---|---|
| `default_init_enters_increase` | default-init probe: first empty cycle dispatches the initial transition to increase and asserts inlet-valve command outp...<truncated 4 chars> | ✅ |
| `increase_to_hold_at_upper_boundary` | explicit-hot-start probe: increase must transition to hold exactly at slp=0.01 and neutralize both valves. | ✅ |
| `increase_no_hold_above_upper_boundary` | explicit-hot-start no-fire probe: increase must stay increase when slp is just above 0.01. | ✅ |
| `hold_to_increase_above_upper_boundary` | explicit-hot-start probe: hold must transition to increase only when slp is greater than 0.01 and set increase outputs. | ✅ |
| `hold_no_increase_at_upper_boundary` | explicit-hot-start no-fire boundary probe: hold must not transition to increase at slp=0.01 because that guard is strict...<truncated 14 chars> | ✅ |
| `hold_to_decrease_below_lower_boundary` | explicit-hot-start probe: hold must transition to decrease when slp is below -0.01 and command pressure release. | ✅ |
| `hold_no_decrease_at_lower_boundary` | explicit-hot-start no-fire boundary probe: hold must not transition to decrease at slp=-0.01 because that guard is stric...<truncated 12 chars> | ✅ |
| `decrease_to_hold_at_lower_boundary` | explicit-hot-start probe: decrease must transition back to hold exactly at slp=-0.01 and neutralize valves and pump. | ✅ |
| `decrease_no_hold_below_lower_boundary` | explicit-hot-start no-fire probe: decrease must stay decrease when slp remains below -0.01. | ✅ |

#### Repair / blocking feedback 概览（report §7 摘录）

- 本 run 未进入 `SD-8/SL-9/SL-10` repair block；通常表示流程在 repair 前已成功、被 provider/schema 错误中断，或在 pre-repair 阶段直接退出。

### 8. 尝试记录与成本

- `SL-1`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 2155, 'completion_chars': 7176, 'completion_tokens': 2723, 'elapsed_seconds': 51.60875358400517, 'estimated_completion_tokens': 1794, 'estimated_prompt_tokens': 6493, 'estimated_total_tokens': 8287, 'first_chunk_seconds': 13.164385498996126, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 25972, 'prompt_tokens': 6393, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 9116}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1144, 'completion_chars': 4142, 'completion_tokens': 1663, 'elapsed_seconds': 32.24296004200005, 'estimated_completion_tokens': 1036, 'estimated_prompt_tokens': 10041, 'estimated_total_tokens': 11077, 'first_chunk_seconds': 11.768933896004455, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 40163, 'prompt_tokens': 10249, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 11912}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-7`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1054, 'completion_chars': 4557, 'completion_tokens': 1573, 'elapsed_seconds': 32.29304820399557, 'estimated_completion_tokens': 1140, 'estimated_prompt_tokens': 9946, 'estimated_total_tokens': 11086, 'first_chunk_seconds': 11.940170136003871, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 39781, 'prompt_tokens': 10528, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 12101}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。

### 9. 最终停止状态与后续含义

- 停止状态：verdict=`success`，record_status=`success`。
- 主要原因分类：`success`。
- required stages executed：`12/12`，missing=`<none>`。
- repairs：`0/0` accepted；scenario_history=`1`。
- 配置含义：`recommended baseline candidate`；该结果可用于评估默认入口本身。
- 主结果/蓝本边界：`main_result_eligible` 只表示该 run 非 provider-invalid 且 trace/schema/secret/final-verdict 口径可进入主结果候选；`path2_ref_model_blueprint_eligible=false` 时，模型仍可作为 FE/BVS 或 dispatch-classifier 压力测试证据，但不得称为 Path2 ref-model 主蓝本。
- 样本含义：若出现 `design_or_variable_dynamics`，应重点审查变量是否仅作为 guard/input 常量而没有事件/动作更新；若出现 pre-scenario parse/semantic 失败，则应先优化 pyfcstm grammar adherence。

> 完整 repair 细节、进入修复原因、SD-8 修改建议、SL-9 candidate、before→candidate diff 与 local-check evidence 与 SL-10 审查证据见 `../runs/pr_langgraph_real_agent_loop_round1_stategraph/pr-e1-path1_abs-default-prlanggraph-stategraph-r1-fb795195/report.md` §7。

</details>

<details><summary>path1 / path1_cara / default / success</summary>

#### NL 输入（原文）

```text
At run time, CARA coordinates the Caregiver Interface, Blood Pressure Monitor, Algorithm, and Pump Monitors around an infusion pump that moves fluid into the patient, while sensor readings are stored in a shared buffer for software access. The pump has manual and autocontrol modes. In manual mode, pump speed is set with the built-in switch and the caregiver sets a default flow rate directly on the pump for manual operation, while in autocontrol mode pump speed is set by a control voltage from an external source. The Algorithm component controls infusion rate and records infusion-related data in log files; patient blood pressure is used to compute the infusion rate, with higher pressure producing a lower flow rate. The Caregiver Interface lets the caregiver modify target blood pressure and initiate or terminate algorithmic pump control, and it also displays and sounds error messages. In the Mode_Control_Algorithm hierarchy, CARA has manual and autocontrol-related mode-control states plus an Ask_StartAC submode; within Ask_StartAC, the setpoint can be changed and pressing StartAC enters AutocontrolInit. During normal autocontrol, CARA controls flow rate only while there are no pump-operation complications. If a pump fault such as fluid-tubing occlusion occurs, the pump activates alarm signals, the caregiver removes the fault, and when CARA was controlling the pump the software releases control. As a cross-component fallback, CA_backManual or any of CB_backManual, CP_backManual, or CC_backManual causes CA_mode to become Manual, making manual operation the shared recovery target.
```

#### NL 输入中文翻译

```text
运行时，CARA 围绕一台向患者输液的输液泵协调 Caregiver Interface、Blood Pressure Monitor、Algorithm 与 Pump Monitors，传感器读数会写入共享缓冲区供软件访问。泵具有手动和自动控制两种模式。手动模式下，泵速由内置开关设置，护理人员直接在泵上设置默认流量；自动控制模式下，泵速由外部控制电压设置。Algorithm 组件控制输液速率并记录输液相关日志；患者血压用于计算输液速率，血压越高流量越低。Caregiver Interface 允许护理人员修改目标血压，并启动或终止算法泵控制，同时显示和发出错误消息。在 Mode_Control_Algorithm 层次中，CARA 具有手动与自动控制相关的模式控制状态以及 Ask_StartAC 子模式；在 Ask_StartAC 中可以修改设定点，按下 StartAC 会进入 AutocontrolInit。正常自动控制期间，只有没有泵操作并发症时 CARA 才控制流量。如果出现输液管堵塞等泵故障，泵会激活报警信号，护理人员排除故障；当 CARA 正在控制泵时，软件会释放控制。作为跨组件回退，CA_backManual 或 CB_backManual、CP_backManual、CC_backManual 中任一事件都会使 CA_mode 变为 Manual，使手动操作成为共享恢复目标。
```

#### FCSTM 输出

```pyfcstm
def int CA_mode = 0;
def int software_control = 0;
def int pump_fault = 0;
def int alarm_signal = 0;
def int log_count = 0;
def float built_in_switch = 0.0;
def float default_flow_rate = 0.0;
def float control_voltage = 0.0;
def float pump_speed = 0.0;
def float blood_pressure = 0.0;
def float target_blood_pressure = 0.0;
def float setpoint = 0.0;
def float infusion_rate = 0.0;
def float flow_rate = 0.0;
def float shared_buffer = 0.0;

state CARA {
    [*] -> Mode_Control_Algorithm;

    state Mode_Control_Algorithm {
        ! * -> Manual :: CA_backManual;
        ! * -> Manual :: CB_backManual;
        ! * -> Manual :: CP_backManual;
        ! * -> Manual :: CC_backManual;

        [*] -> Manual;

        state Manual {
            enter {
                CA_mode = 0;
                software_control = 0;
                alarm_signal = 0;
                pump_fault = 0;
            }
            during {
                shared_buffer = blood_pressure;
                pump_speed = built_in_switch;
                flow_rate = default_flow_rate;
            }
        }

        state Ask_StartAC {
            enter {
                CA_mode = 0;
                software_control = 0;
            }
            during {
                shared_buffer = blood_pressure;
            }
        }

        state AutocontrolInit {
            enter {
                CA_mode = 1;
                software_control = 1;
                alarm_signal = 0;
                pump_speed = control_voltage;
            }
            during {
                shared_buffer = blood_pressure;
                log_count = log_count + 1;
            }
        }

        state AutocontrolNormal {
            during {
                shared_buffer = blood_pressure;
                infusion_rate = target_blood_pressure - blood_pressure;
                flow_rate = infusion_rate;
                pump_speed = control_voltage;
                log_count = log_count + 1;
            }
        }

        state PumpFault {
            enter {
                alarm_signal = 1;
                software_control = 0;
                CA_mode = 0;
            }
            during {
                shared_buffer = blood_pressure;
            }
        }

        Manual -> Ask_StartAC : InitiateAC;
        Ask_StartAC -> Ask_StartAC : ChangeSetpoint effect {
            target_blood_pressure = setpoint;
        };
        Ask_StartAC -> AutocontrolInit : StartAC;
        AutocontrolInit -> Manual : TerminateAC;
        AutocontrolInit -> AutocontrolNormal;
        AutocontrolNormal -> Manual : TerminateAC;
        AutocontrolNormal -> AutocontrolNormal : PumpFaultDetected effect {
            pump_fault = 1;
        };
        AutocontrolNormal -> PumpFault : if [pump_fault > 0];
        PumpFault -> Manual : FaultRemoved effect {
            pump_fault = 0;
        };
    }
}
```

#### agent-loop 过程与日志路径

| 项 | 值 |
|---|---|
| verdict / status | `success` / `success` |
| failure class | `success_but_weak_oracle_ineligible` |
| main_result_eligible | `false` |
| path2_ref_model_blueprint | `n/a`；not_applicable_to_path1 |
| state_mode_decorative | `false` |
| executed stages | `SC-0 -> SL-1 -> SD-2 -> SD-3 -> SD-4 -> SD-8 -> SL-9 -> SL-10 -> SL-9 -> SL-10 -> SC-11 -> SD-2 -> SD-3 -> SD-4 -> SL-5 -> SD-5A -> SL-5 -> SD-5A -> SL-5 -> SD-5A -> SC-5F -> SD-6 -> SD-8 -> SL-9 -> SL-10 -> SL-9 -> SL-10 -> SC-11 -> SD-2 -> SD-3 -> SD-4 -> SD-5A -> SL-5 -> SD-5A -> SL-5 -> SD-5A -> SC-5F -> SD-6 -> SL-7 -> SC-12 -> SC-13` |
| iter / repairs / accepted / scenarios | `3` / `4` / `2` / `6` |
| token / elapsed | `{'prompt_tokens': 570304, 'completion_tokens': 47721, 'total_tokens': 618025, 'estimated_prompt_tokens': 628617, 'estimated_completion_tokens': 39016, 'estimated_total_tokens': 667633, 'prompt_chars': 2514450, 'completion_chars': 156043, 'n_calls': 15, 'token_usage_available': True, 'token_usage_unavailable_calls': 0}` / `923.086s` |
| full stage table | `../runs/pr_langgraph_real_agent_loop_round1_stategraph/pr-e1-path1_cara-default-prlanggraph-stategraph-r1-06cfac95/report.md` §4 |
| run record | `../runs/pr_langgraph_real_agent_loop_round1_stategraph/pr-e1-path1_cara-default-prlanggraph-stategraph-r1-06cfac95/pr-e1-path1_cara-default-prlanggraph-stategraph-r1-06cfac95.agent_loop.json.gz` |
| logs | `../runs/pr_langgraph_real_agent_loop_round1_stategraph/pr-e1-path1_cara-default-prlanggraph-stategraph-r1-06cfac95/run_logs/stdout.txt`, `../runs/pr_langgraph_real_agent_loop_round1_stategraph/pr-e1-path1_cara-default-prlanggraph-stategraph-r1-06cfac95/run_logs/stderr.txt` |
| checks / repro | `../runs/pr_langgraph_real_agent_loop_round1_stategraph/pr-e1-path1_cara-default-prlanggraph-stategraph-r1-06cfac95/checks.json`, `../runs/pr_langgraph_real_agent_loop_round1_stategraph/pr-e1-path1_cara-default-prlanggraph-stategraph-r1-06cfac95/reproducibility.json` |

#### 全流程摘要表（report §4 摘录）

| Stage | 是否 LLM | iteration | 结果 | 获取的信息 / 反馈 | 本阶段做了什么 | DSL 修改 | artifact/log |
|---|---:|---:|---:|---|---|---|---|
| `SC-0` | 否 | - | ✅ | trace/control | 初始化 run state | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r1-06cfac95.agent_loop.json.gz) |
| `SL-1` | 是 | - | ✅ | LLM calls=1, tokens=12360 | 生成初始 DSL 与 grounding seeds | initial len=2671 | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r1-06cfac95.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r1-06cfac95.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r1-06cfac95.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ⚠️ | blocking=2, advisory=21, info=1; blocking=0, advisory=21, info=1; blocking=0, advisory=21, info=1 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r1-06cfac95.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r1-06cfac95.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=4, tokens=261638 | LLM per-request accept/reject + repair | candidate len=2818,2886,2879,2879 | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r1-06cfac95.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ⚠️ | LLM calls=4, tokens=198137 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r1-06cfac95.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=4, tokens=261638 | LLM per-request accept/reject + repair | candidate len=2818,2886,2879,2879 | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r1-06cfac95.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=4, tokens=198137 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r1-06cfac95.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r1-06cfac95.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r1-06cfac95.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r1-06cfac95.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=2, advisory=21, info=1; blocking=0, advisory=21, info=1; blocking=0, advisory=21, info=1 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r1-06cfac95.agent_loop.json.gz) |
| `SL-5` | 是 | 1 | ✅ | LLM calls=5, tokens=122555 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r1-06cfac95.agent_loop.json.gz) |
| `SD-5A` | 否 | 1 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r1-06cfac95.agent_loop.json.gz) |
| `SL-5` | 是 | 1 | ✅ | LLM calls=5, tokens=122555 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r1-06cfac95.agent_loop.json.gz) |
| `SD-5A` | 否 | 1 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r1-06cfac95.agent_loop.json.gz) |
| `SL-5` | 是 | 1 | ✅ | LLM calls=5, tokens=122555 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r1-06cfac95.agent_loop.json.gz) |
| `SD-5A` | 否 | 1 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r1-06cfac95.agent_loop.json.gz) |
| `SC-5F` | 否 | 1 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r1-06cfac95.agent_loop.json.gz) |
| `SD-6` | 否 | 1 | ⚠️ | ok=False, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r1-06cfac95.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r1-06cfac95.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=4, tokens=261638 | LLM per-request accept/reject + repair | candidate len=2818,2886,2879,2879 | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r1-06cfac95.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=4, tokens=198137 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r1-06cfac95.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=4, tokens=261638 | LLM per-request accept/reject + repair | candidate len=2818,2886,2879,2879 | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r1-06cfac95.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=4, tokens=198137 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r1-06cfac95.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r1-06cfac95.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r1-06cfac95.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r1-06cfac95.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=2, advisory=21, info=1; blocking=0, advisory=21, info=1; blocking=0, advisory=21, info=1 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r1-06cfac95.agent_loop.json.gz) |
| `SD-5A` | 否 | 1 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r1-06cfac95.agent_loop.json.gz) |
| `SL-5` | 是 | 1 | ✅ | LLM calls=5, tokens=122555 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r1-06cfac95.agent_loop.json.gz) |
| `SD-5A` | 否 | 1 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r1-06cfac95.agent_loop.json.gz) |
| `SL-5` | 是 | 1 | ✅ | LLM calls=5, tokens=122555 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r1-06cfac95.agent_loop.json.gz) |
| `SD-5A` | 否 | 1 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r1-06cfac95.agent_loop.json.gz) |
| `SC-5F` | 否 | 1 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r1-06cfac95.agent_loop.json.gz) |
| `SD-6` | 否 | 1 | ✅ | ok=False, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r1-06cfac95.agent_loop.json.gz) |
| `SL-7` | 是 | 2 | ✅ | LLM calls=1, tokens=23335 | LLM model review | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r1-06cfac95.agent_loop.json.gz) |
| `SC-12` | 否 | - | ✅ | full_pass_all_required_feedback_ok | 写 final verdict | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r1-06cfac95.agent_loop.json.gz) |
| `SC-13` | 否 | - | ✅ | trace/control | 写审计 run record | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r1-06cfac95.agent_loop.json.gz) |

### 4.1 完整流程日志（stage/control-flow replay ledger）

口径：本节来自 `AgentLoopRunRecord.logs`，与 [`flow_log.json`](./flow_log.json) 一致；用于复现每个 stage 如何进入、得到什么批示、跳转到哪里，以及每次 DSL 产物/候选如何变化。

| # | ts | stage | iter | event | result / jump | DSL evidence |
|---:|---|---|---:|---|---|---|
| 1 | `2026-06-04T14:51:22Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 2 | `2026-06-04T14:51:22Z` | `SC-0` | `-` | `run_start` | {} | <none> |
| 3 | `2026-06-04T14:51:22Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 4 | `2026-06-04T14:51:22Z` | `SL-1` | `-` | `stage_enter` | {"reason": "initial_modeling_adapter_available"} | <none> |
| 5 | `2026-06-04T14:53:11Z` | `SL-1` | `-` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 6 | `2026-06-04T14:53:11Z` | `SL-1` | `-` | `stage_result` | {"jump": "SD-2", "ok": true} | candidate_dsl:len=2671,hash=sha256:d4eb38ad6318 |
| 7 | `2026-06-04T14:53:11Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 8 | `2026-06-04T14:53:11Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 9 | `2026-06-04T14:53:11Z` | `<control>` | `0` | `iteration_enter` | {} | current_hash=sha256:d4eb38ad63180890b8e61400bf55e7d4196c2463ce14ff69ac1a6b88542836c9 |
| 10 | `2026-06-04T14:53:11Z` | `<control>` | `0` | `iteration_validation_enter` | {} | dsl:len=2671,hash=sha256:d4eb38ad6318, current_hash=sha256:d4eb38ad63180890b8e61400bf55e7d4196c2463ce14ff69ac1a6b88542836c9 |
| 11 | `2026-06-04T14:53:11Z` | `SD-2` | `0` | `stage_enter` | {"reason": "full_validation_pass"} | <none> |
| 12 | `2026-06-04T14:53:12Z` | `SD-2` | `0` | `stage_result` | {"jump": "SD-3", "ok": true, "status": "StageStatus.OK"} | <none> |
| 13 | `2026-06-04T14:53:12Z` | `SD-3` | `0` | `stage_enter` | {"reason": "SD-2 ok"} | <none> |
| 14 | `2026-06-04T14:53:12Z` | `SD-3` | `0` | `stage_result` | {"jump": "SD-4", "ok": true, "status": "StageStatus.OK"} | <none> |
| 15 | `2026-06-04T14:53:12Z` | `SD-4` | `0` | `stage_enter` | {"reason": "SD-3 ok"} | <none> |
| 16 | `2026-06-04T14:53:12Z` | `SD-4` | `0` | `stage_result` | {"jump": "SD-8", "ok": false, "status": "StageStatus.FAIL"} | <none> |
| 17 | `2026-06-04T14:53:12Z` | `<control>` | `0` | `iteration_validation_result` | {"jump": "SD-8 repair", "selected_feedback": {"blocking": true, "blocking_instance_keys": ["W_UNWRITTEN_READ_VAR:var_name=pump_fault", "W_GUARD_VARS_NEVER_CHANGE:from_path=CARA.Mode_Control_Algorithm.AutocontrolNormal:to_path=CARA.Mode_Control_Algorithm.PumpFault"], "diagnostic_codes": ["W_UNWRITTEN_READ_VAR", "W_GUARD_VARS_NEVER_CHANGE", "W_HIGH_VAR_TO_LEAF_RATIO", "W_UNREFERENCED_VAR", "W_UNREFERENCED_VAR", "W_UNRE...<truncated 1024 chars> | <none> |
| 18 | `2026-06-04T14:53:12Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 19 | `2026-06-04T14:53:12Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 20 | `2026-06-04T14:53:12Z` | `SD-8` | `0` | `repair_path_enter` | {"jump": "SD-8", "selected_feedback": {"blocking": true, "blocking_instance_keys": ["W_UNWRITTEN_READ_VAR:var_name=pump_fault", "W_GUARD_VARS_NEVER_CHANGE:from_path=CARA.Mode_Control_Algorithm.AutocontrolNormal:to_path=CARA.Mode_Control_Algorithm.PumpFault"], "diagnostic_codes": ["W_UNWRITTEN_READ_VAR", "W_GUARD_VARS_NEVER_CHANGE", "W_HIGH_VAR_TO_LEAF_RATIO", "W_UNREFERENCED_VAR", "W_UNREFERENCED_VAR", "W_UNREFERENCE...<truncated 5329 chars> | current_dsl:len=2671,hash=sha256:d4eb38ad6318 |
| 21 | `2026-06-04T14:53:12Z` | `SD-8` | `0` | `stage_result` | {"jump": "SL-9", "ok": true, "status": "StageStatus.OK"} | <none> |
| 22 | `2026-06-04T14:53:12Z` | `SD-8` | `0` | `fix_request_batch` | {"request_count": 2} | <none> |
| 23 | `2026-06-04T14:53:12Z` | `SL-9` | `0` | `stage_enter` | {"reason": "fix_requests_ready"} | old_dsl:len=2671,hash=sha256:d4eb38ad6318 |
| 24 | `2026-06-04T14:53:47Z` | `SL-9` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 25 | `2026-06-04T14:53:47Z` | `SL-9` | `0` | `stage_result` | {"accepted_request_ids": ["fixreq-0-sd4-0-6e7fd24414", "fixreq-0-sd4-1-8e1eb9dac6"], "jump": "SL-10", "ok": true, "rejected_request_ids": []} | candidate_dsl:len=2818,hash=sha256:ee75f9b6f572 |
| 26 | `2026-06-04T14:53:47Z` | `SD-10` | `0` | `stage_result` | {"jump": "SL-10", "ok": false, "status": "StageStatus.FAIL"} | <none> |
| 27 | `2026-06-04T14:53:47Z` | `SL-10` | `0` | `stage_enter` | {"reason": "candidate_dsl_and_local_evidence_ready"} | candidate_hash=sha256:ee75f9b6f572d19faae19a0550300c64df2254d41a6031cc0bb8ee6c440c8d16 |
| 28 | `2026-06-04T14:54:07Z` | `SL-10` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 29 | `2026-06-04T14:54:07Z` | `SL-10` | `0` | `stage_result` | {"decision": "rework", "jump": "SL-9 rework", "ok": false} | <none> |
| 30 | `2026-06-04T14:54:07Z` | `SL-10` | `0` | `grounding_update_hints_recorded` | {} | <none> |
| 31 | `2026-06-04T14:54:07Z` | `SL-9` | `0` | `stage_enter` | {"reason": "sl10_rework_locked"} | old_dsl:len=2671,hash=sha256:d4eb38ad6318 |
| 32 | `2026-06-04T14:54:49Z` | `SL-9` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 33 | `2026-06-04T14:54:49Z` | `SL-9` | `0` | `stage_result` | {"accepted_request_ids": ["fixreq-0-sd4-0-6e7fd24414", "fixreq-0-sd4-1-8e1eb9dac6"], "jump": "SL-10", "ok": true, "rejected_request_ids": []} | candidate_dsl:len=2886,hash=sha256:3d3419eeddd7 |
| 34 | `2026-06-04T14:54:49Z` | `SD-10` | `0` | `stage_result` | {"jump": "SL-10", "ok": false, "status": "StageStatus.FAIL"} | <none> |
| 35 | `2026-06-04T14:54:49Z` | `SL-10` | `0` | `stage_enter` | {"reason": "candidate_dsl_and_local_evidence_ready"} | candidate_hash=sha256:3d3419eeddd77f91e940999a2aae1ec708a42f4ef4a1b1cfb02f335fe51a6f63 |
| 36 | `2026-06-04T14:55:14Z` | `SL-10` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 37 | `2026-06-04T14:55:14Z` | `SL-10` | `0` | `stage_result` | {"decision": "pass", "jump": "SC-11", "ok": true} | <none> |
| 38 | `2026-06-04T14:55:14Z` | `SL-10` | `0` | `grounding_update_hints_recorded` | {} | <none> |
| 39 | `2026-06-04T14:55:14Z` | `SC-11` | `0` | `stage_result` | {"jump": "SD-2 next iteration", "ok": true, "reason": "SL-10 accepted candidate; next iteration must restart at SD-2"} | candidate_dsl:len=2886,hash=sha256:3d3419eeddd7 |
| 40 | `2026-06-04T14:55:14Z` | `<control>` | `0` | `iteration_repair_result` | {"accepted": true, "jump": "SD-2 next iteration"} | current_hash=sha256:3d3419eeddd77f91e940999a2aae1ec708a42f4ef4a1b1cfb02f335fe51a6f63 |
| 41 | `2026-06-04T14:55:14Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 42 | `2026-06-04T14:55:14Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 43 | `2026-06-04T14:55:14Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 44 | `2026-06-04T14:55:14Z` | `<control>` | `1` | `iteration_enter` | {} | current_hash=sha256:3d3419eed
... <truncated 5656 chars in PR comment; see report.md>

#### Scenario 逐轮通过矩阵（report §6.1 摘录）

口径：`✅` = 该 scenario 在该轮 SD-6 simulation 通过；`❌` = 该轮失败；`⚪` = 该轮未执行或无该 scenario 结果。

| Scenario | Intent | Iter 2 | Iter 3 |
|---|---|---|---|
| `effect_mutation_change_setpoint_exact_persistence` | explicit-hot-start probe: ChangeSetpoint's transition effect must copy setpoint exactly, not omit the effect or assign a...<truncated 75 chars> | ⚪ | ✅ |
| `effect_mutation_pumpfaultdetected_exact_flag` | explicit-hot-start probe: PumpFaultDetected's transition effect must set pump_fault exactly to 1 before the separate pos...<truncated 41 chars> | ⚪ | ✅ |
| `effect_mutation_faultremoved_recovery_outputs` | explicit-hot-start probe: FaultRemoved recovery to Manual must leave the fault flag exactly cleared and restore manual o...<truncated 80 chars> | ⚪ | ✅ |
| `default_init_startac_then_terminate_from_init` | default-init probe: first empty cycle must dispatch to Manual, InitiateAC must enter Ask_StartAC, StartAC must enter Aut...<truncated 74 chars> | ⚪ | ✅ |
| `normal_idle_then_terminate_to_manual` | explicit-hot-start probe: AutocontrolNormal with no pump fault must stay in normal autocontrol and compute commanded flo...<truncated 48 chars> | ⚪ | ✅ |
| `all_backmanual_forced_recovery_events` | explicit-hot-start probe: each cross-component BackManual forced event must work from a concrete non-Manual leaf and lan...<truncated 34 chars> | ⚪ | ✅ |
| `default_init_manual_mode_outputs` |  | ✅ | ⚪ |
| `initiate_change_setpoint_start_autocontrol` |  | ⚪ | ⚪ |
| `autocontrol_normal_lower_pressure_higher_flow` |  | ✅ | ⚪ |
| `autocontrol_normal_higher_pressure_lower_flow` |  | ✅ | ⚪ |
| `pump_fault_detected_then_alarm_state` |  | ⚪ | ⚪ |
| `fault_removed_returns_manual_and_clears_fault` |  | ⚪ | ⚪ |
| `terminate_ac_from_init_returns_manual` |  | ⚪ | ⚪ |
| `terminate_ac_from_normal_returns_manual` |  | ⚪ | ⚪ |
| `forced_backmanual_from_ask_and_init` |  | ⚪ | ⚪ |
| `forced_backmanual_from_normal_and_fault` |  | ⚪ | ⚪ |
| `atomic_startac_target_and_entry_effects` |  | ⚪ | ⚪ |
| `atomic_change_setpoint_effect_value` |  | ⚪ | ⚪ |
| `atomic_fault_detection_effect_and_guard_target` |  | ⚪ | ⚪ |
| `atomic_forced_backmanual_each_event` |  | ⚪ | ⚪ |
| `atomic_fault_removed_clears_exact_fault_flag` |  | ⚪ | ⚪ |
| `atomic_initiateac_exact_ask_target` |  | ⚪ | ⚪ |
| `atomic_autocontrolinit_advances_exact_normal_target` |  | ✅ | ⚪ |
| `atomic_forced_backmanual_from_fault_clears_alarm_fault` |  | ✅ | ⚪ |
| `atomic_terminate_normal_manual_enter_effects_from_dirty_flags` |  | ⚪ | ⚪ |

#### Repair / blocking feedback 概览（report §7 摘录）

口径：本节记录 agent-loop 真实进入 repair block 后的证据链：FixRequestBatch、SL-9 per-request accept/reject、candidate diff、local-check evidence、SL-10(NL+FixLog) 审阅，以及完整 FixLog ledger 摘录。

| Repair | iteration | accepted | source | blocking diagnostics | SL-9 decisions | SL-10 / local checks | candidate hash |
|---:|---:|---:|---|---|---|---|---|
| 1 | `0` | ❌ | `SD-4` | W_UNWRITTEN_READ_VAR:var_name=pump_fault, W_GUARD_VARS_NEVER_CHANGE:from_path=CARA.Mode_Control_Algorithm.AutocontrolNormal:to_path=CARA.Mode_Control_Algorithm.PumpFault, W_UNWRITTEN_READ_VAR, W_GUARD_VARS_NEVER_CHANGE, W_HIGH_VAR_TO_LEAF_RATIO, ... +3 | accept=2, reject=0, waiver=0 | SL-10 decision=rework, ok=False, target=True, regression=False, drift=minor, rework=SL-10 pass was downgraded because local deterministic evidence reported major drift and SL-10 evidence did not explicitly address the local rejection reason/kind with a structu...<truncated 658 chars> | `sha256:ee75f9b6f572d19faae19a0550300c64df2254d41a6031cc0bb8ee6c440c8d16` |
| 2 | `0` | ✅ | `SD-4` | W_UNWRITTEN_READ_VAR:var_name=pump_fault, W_GUARD_VARS_NEVER_CHANGE:from_path=CARA.Mode_Control_Algorithm.AutocontrolNormal:to_path=CARA.Mode_Control_Algorithm.PumpFault, W_UNWRITTEN_READ_VAR, W_GUARD_VARS_NEVER_CHANGE, W_HIGH_VAR_TO_LEAF_RATIO, ... +3 | accept=2, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none>; local ok=False, target=False, regression=False, drift=major, local_stage=SD-10, reason=missing_required_grounding | `sha256:3d3419eeddd77f91e940999a2aae1ec708a42f4ef4a1b1cfb02f335fe51a6f63` |
| 3 | `1` | ❌ | `SD-6` | initiate_change_setpoint_start_autocontrol, pump_fault_detected_then_alarm_state, fault_removed_returns_manual_and_clears_fault, terminate_ac_from_init_returns_manual, terminate_ac_from_normal_returns_manual, ... +9 | accept=12, reject=0, waiver=0 | SL-10 decision=rework, ok=False, target=False, regression=True, drift=major, rework=Fix `terminate_ac_from_init_returns_manual`: dispatching `CARA.Mode_Control_Algorithm.TerminateAC` from hot-start state `CARA.Mode_Control_Algorithm.AutocontrolInit` must trans...<truncated 1022 chars> | `sha256:a079cfeba8dad62d9eebafabd0d4dbd560bd5f622a0c5534ba7a5cbc79f0c49d` |
| 4 | `1` | ✅ | `SD-6` | initiate_change_setpoint_start_autocontrol, pump_fault_detected_then_alarm_state, fault_removed_returns_manual_and_clears_fault, terminate_ac_from_init_returns_manual, terminate_ac_from_normal_returns_manual, ... +9 | accept=12, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none>; local ok=False, target=False, regression=False, drift=major, local_stage=SD-10, reason=missing_required_grounding | `sha256:ee24d33cefd4c6a306c51cba43096280ff0d137f9dad2ee9e56a34647b35b3a3` |

> 完整 repair 细节、进入修复原因、SD-8 修改建议、SL-9 candidate、before→candidate diff 与 local-check evidence 与 SL-10 审查证据见 `../runs/pr_langgraph_real_agent_loop_round1_stategraph/pr-e1-path1_cara-default-prlanggraph-stategraph-r1-06cfac95/report.md` §7。

</details>

<details><summary>path1 / path1_elevator / default / success</summary>

#### NL 输入（原文）

```text
The automatic elevator controller is built as a finite-state machine whose state space combines floor states `F1`, `F2`, and `F3` with motion states `MU2`, `MU3`, `MD1`, and `MD2` for upward and downward travel.

In the normal workflow, the system starts from an ideal state on floor 1, chooses either the up or down branch according to floor requests, stops at the requested floor, and then immediately checks the next destination before deciding whether to continue moving.

The controller uses `PS1/PS2/PS3` as floor-request inputs and `S1/S2/S3` as sensing inputs for arrival. From `F1`, `PS2` triggers `MU2` and `PS3` triggers `MU3`. From `F2`, `PS3` triggers `MU3` and `PS1` triggers `MD1`. From `F3`, `PS1` triggers `MD1` and `PS2` triggers `MD2`. Arrival sensors complete motion transitions: `MU2 + S2 -> F2`, `MU3 + S3 -> F3`, `MD1 + S1 -> F1`, and `MD2 + S2 -> F2`.

The `hbrg` output distinguishes upward drive, downward drive, and stop conditions. A reset signal forces the controller back to floor 1 regardless of the outstanding request context.
```

#### NL 输入中文翻译

```text
自动电梯控制器被构建为有限状态机，其状态空间由楼层状态 `F1`、`F2`、`F3` 与上/下行运动状态 `MU2`、`MU3`、`MD1`、`MD2` 组合而成。

正常流程中，系统从 1 楼理想状态开始，根据楼层请求选择上行或下行分支，在请求楼层停止，然后立即检查下一目的地以决定是否继续移动。

控制器使用 `PS1/PS2/PS3` 作为楼层请求输入，使用 `S1/S2/S3` 作为到位传感输入。从 `F1`，`PS2` 触发 `MU2`，`PS3` 触发 `MU3`；从 `F2`，`PS3` 触发 `MU3`，`PS1` 触发 `MD1`；从 `F3`，`PS1` 触发 `MD1`，`PS2` 触发 `MD2`。到位传感器完成运动转移：`MU2 + S2 -> F2`，`MU3 + S3 -> F3`，`MD1 + S1 -> F1`，`MD2 + S2 -> F2`。

`hbrg` 输出区分上行驱动、下行驱动和停止状态。复位信号会无视当前请求上下文，强制控制器回到 1 楼。
```

#### FCSTM 输出

```pyfcstm
def int hbrg = 0;

state AutomaticElevatorController {
    ! * -> F1 : reset;

    [*] -> F1;

    state F1 {
        enter { hbrg = 0; }
    }

    state F2 {
        enter { hbrg = 0; }
    }

    state F3 {
        enter { hbrg = 0; }
    }

    state MU2 {
        enter { hbrg = 1; }
    }

    state MU3 {
        enter { hbrg = 1; }
    }

    state MD1 {
        enter { hbrg = -1; }
    }

    state MD2 {
        enter { hbrg = -1; }
    }

    F1 -> MU2 : PS2;
    F1 -> MU3 : PS3;
    F2 -> MU3 : PS3;
    F2 -> MD1 : PS1;
    F3 -> MD1 : PS1;
    F3 -> MD2 : PS2;
    MU2 -> F2 : S2;
    MU3 -> F3 : S3;
    MD1 -> F1 : S1;
    MD2 -> F2 : S2;
}
```

#### agent-loop 过程与日志路径

| 项 | 值 |
|---|---|
| verdict / status | `success` / `success` |
| failure class | `success` |
| main_result_eligible | `true` |
| path2_ref_model_blueprint | `n/a`；not_applicable_to_path1 |
| state_mode_decorative | `false` |
| executed stages | `SC-0 -> SL-1 -> SD-2 -> SD-3 -> SD-4 -> SL-5 -> SD-5A -> SC-5F -> SD-6 -> SL-7 -> SC-12 -> SC-13` |
| iter / repairs / accepted / scenarios | `1` / `0` / `0` / `1` |
| token / elapsed | `{'prompt_tokens': 26597, 'completion_tokens': 6995, 'total_tokens': 33592, 'estimated_prompt_tokens': 25982, 'estimated_completion_tokens': 4933, 'estimated_total_tokens': 30915, 'prompt_chars': 103923, 'completion_chars': 19726, 'n_calls': 3, 'token_usage_available': True, 'token_usage_unavailable_calls': 0}` / `136.835s` |
| full stage table | `../runs/pr_langgraph_real_agent_loop_round1_stategraph/pr-e1-path1_elevator-default-prlanggraph-stategraph-r1-0cdc09ec/report.md` §4 |
| run record | `../runs/pr_langgraph_real_agent_loop_round1_stategraph/pr-e1-path1_elevator-default-prlanggraph-stategraph-r1-0cdc09ec/pr-e1-path1_elevator-default-prlanggraph-stategraph-r1-0cdc09ec.agent_loop.json.gz` |
| logs | `../runs/pr_langgraph_real_agent_loop_round1_stategraph/pr-e1-path1_elevator-default-prlanggraph-stategraph-r1-0cdc09ec/run_logs/stdout.txt`, `../runs/pr_langgraph_real_agent_loop_round1_stategraph/pr-e1-path1_elevator-default-prlanggraph-stategraph-r1-0cdc09ec/run_logs/stderr.txt` |
| checks / repro | `../runs/pr_langgraph_real_agent_loop_round1_stategraph/pr-e1-path1_elevator-default-prlanggraph-stategraph-r1-0cdc09ec/checks.json`, `../runs/pr_langgraph_real_agent_loop_round1_stategraph/pr-e1-path1_elevator-default-prlanggraph-stategraph-r1-0cdc09ec/reproducibility.json` |

#### 全流程摘要表（report §4 摘录）

| Stage | 是否 LLM | iteration | 结果 | 获取的信息 / 反馈 | 本阶段做了什么 | DSL 修改 | artifact/log |
|---|---:|---:|---:|---|---|---|---|
| `SC-0` | 否 | - | ✅ | trace/control | 初始化 run state | 无/见 record | [`record`](./pr-e1-path1_elevator-default-prlanggraph-stategraph-r1-0cdc09ec.agent_loop.json.gz) |
| `SL-1` | 是 | - | ✅ | LLM calls=1, tokens=9477 | 生成初始 DSL 与 grounding seeds | initial len=658 | [`record`](./pr-e1-path1_elevator-default-prlanggraph-stategraph-r1-0cdc09ec.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_elevator-default-prlanggraph-stategraph-r1-0cdc09ec.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_elevator-default-prlanggraph-stategraph-r1-0cdc09ec.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=1, info=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_elevator-default-prlanggraph-stategraph-r1-0cdc09ec.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=1, tokens=13458 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_elevator-default-prlanggraph-stategraph-r1-0cdc09ec.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_elevator-default-prlanggraph-stategraph-r1-0cdc09ec.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_elevator-default-prlanggraph-stategraph-r1-0cdc09ec.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_elevator-default-prlanggraph-stategraph-r1-0cdc09ec.agent_loop.json.gz) |
| `SL-7` | 是 | 0 | ✅ | LLM calls=1, tokens=10657 | LLM model review | 无/见 record | [`record`](./pr-e1-path1_elevator-default-prlanggraph-stategraph-r1-0cdc09ec.agent_loop.json.gz) |
| `SC-12` | 否 | - | ✅ | full_pass_all_required_feedback_ok | 写 final verdict | 无/见 record | [`record`](./pr-e1-path1_elevator-default-prlanggraph-stategraph-r1-0cdc09ec.agent_loop.json.gz) |
| `SC-13` | 否 | - | ✅ | trace/control | 写审计 run record | 无/见 record | [`record`](./pr-e1-path1_elevator-default-prlanggraph-stategraph-r1-0cdc09ec.agent_loop.json.gz) |

### 4.1 完整流程日志（stage/control-flow replay ledger）

口径：本节来自 `AgentLoopRunRecord.logs`，与 [`flow_log.json`](./flow_log.json) 一致；用于复现每个 stage 如何进入、得到什么批示、跳转到哪里，以及每次 DSL 产物/候选如何变化。

| # | ts | stage | iter | event | result / jump | DSL evidence |
|---:|---|---|---:|---|---|---|
| 1 | `2026-06-04T14:51:22Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 2 | `2026-06-04T14:51:22Z` | `SC-0` | `-` | `run_start` | {} | <none> |
| 3 | `2026-06-04T14:51:22Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 4 | `2026-06-04T14:51:22Z` | `SL-1` | `-` | `stage_enter` | {"reason": "initial_modeling_adapter_available"} | <none> |
| 5 | `2026-06-04T14:52:19Z` | `SL-1` | `-` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 6 | `2026-06-04T14:52:19Z` | `SL-1` | `-` | `stage_result` | {"jump": "SD-2", "ok": true} | candidate_dsl:len=658,hash=sha256:af4349932f7d |
| 7 | `2026-06-04T14:52:19Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 8 | `2026-06-04T14:52:19Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 9 | `2026-06-04T14:52:19Z` | `<control>` | `0` | `iteration_enter` | {} | current_hash=sha256:af4349932f7d9a422bdef8ed68324cf3dc251ecf6e13aec401bb37d00c313d1a |
| 10 | `2026-06-04T14:52:19Z` | `<control>` | `0` | `iteration_validation_enter` | {} | dsl:len=658,hash=sha256:af4349932f7d, current_hash=sha256:af4349932f7d9a422bdef8ed68324cf3dc251ecf6e13aec401bb37d00c313d1a |
| 11 | `2026-06-04T14:52:19Z` | `SD-2` | `0` | `stage_enter` | {"reason": "full_validation_pass"} | <none> |
| 12 | `2026-06-04T14:52:20Z` | `SD-2` | `0` | `stage_result` | {"jump": "SD-3", "ok": true, "status": "StageStatus.OK"} | <none> |
| 13 | `2026-06-04T14:52:20Z` | `SD-3` | `0` | `stage_enter` | {"reason": "SD-2 ok"} | <none> |
| 14 | `2026-06-04T14:52:20Z` | `SD-3` | `0` | `stage_result` | {"jump": "SD-4", "ok": true, "status": "StageStatus.OK"} | <none> |
| 15 | `2026-06-04T14:52:20Z` | `SD-4` | `0` | `stage_enter` | {"reason": "SD-3 ok"} | <none> |
| 16 | `2026-06-04T14:52:20Z` | `SD-4` | `0` | `stage_result` | {"jump": "SL-5", "ok": true, "status": "StageStatus.OK"} | <none> |
| 17 | `2026-06-04T14:52:20Z` | `SL-5` | `0` | `stage_enter` | {"reason": "scenario_set_absent"} | <none> |
| 18 | `2026-06-04T14:53:02Z` | `SL-5` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 19 | `2026-06-04T14:53:02Z` | `SD-5A` | `0` | `stage_result` | {"jump": "SC-5F", "ok": true, "status": "StageStatus.OK"} | <none> |
| 20 | `2026-06-04T14:53:02Z` | `SC-5F` | `0` | `stage_result` | {"jump": "SD-6", "ok": true} | <none> |
| 21 | `2026-06-04T14:53:02Z` | `SD-6` | `0` | `stage_enter` | {"reason": "scenario_set_ready"} | <none> |
| 22 | `2026-06-04T14:53:02Z` | `SD-6` | `0` | `stage_result` | {"jump": "SL-7", "ok": true, "status": "StageStatus.OK"} | <none> |
| 23 | `2026-06-04T14:53:02Z` | `SL-7` | `0` | `stage_enter` | {"reason": "SD-6 ok"} | <none> |
| 24 | `2026-06-04T14:53:38Z` | `SL-7` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 25 | `2026-06-04T14:53:38Z` | `SL-7` | `0` | `stage_result` | {"jump": "SC-12 success", "ok": true, "status": "StageStatus.OK"} | <none> |
| 26 | `2026-06-04T14:53:38Z` | `SL-7` | `0` | `grounding_update_hints_recorded` | {} | <none> |
| 27 | `2026-06-04T14:53:38Z` | `<control>` | `0` | `iteration_validation_result` | {"jump": "SC-12 success", "selected_feedback": null} | <none> |
| 28 | `2026-06-04T14:53:38Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 29 | `2026-06-04T14:53:38Z` | `SC-12` | `-` | `sc12_verdict` | {"reason": "full_pass_all_required_feedback_ok", "verdict": "success"} | final_dsl:len=658,hash=sha256:af4349932f7d |
| 30 | `2026-06-04T14:53:38Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 31 | `2026-06-04T14:53:38Z` | `SC-13` | `-` | `run_end` | {"verdict": "success"} | final_dsl:len=658,hash=sha256:af4349932f7d |
| 32 | `` | `<control>` | `-` | `langgraph_node_trace` | {} | <none> |

#### Scenario 逐轮通过矩阵（report §6.1 摘录）

口径：`✅` = 该 scenario 在该轮 SD-6 simulation 通过；`❌` = 该轮失败；`⚪` = 该轮未执行或无该 scenario 结果。

| Scenario | Intent | Iter 1 |
|---|---|---|
| `default_init_f1_stop_and_sensor_no_fire` | default-init verifies initial dispatch to floor 1 with stop hbrg, then an arrival sensor alone does not move the control...<truncated 12 chars> | ✅ |
| `f1_ps2_mu2_arrive_f2_continue_mu3` | explicit-hot-start probes F1 request to floor 2, MU2 arrival at F2, then immediate next request from F2 upward to MU3. | ✅ |
| `f1_ps3_mu3_arrive_f3_then_md2_to_f2` | explicit-hot-start probes direct travel from F1 to F3, arrival stop at F3, then request for floor 2 drives downward thro...<truncated 14 chars> | ✅ |
| `f2_ps1_md1_arrive_f1` | explicit-hot-start probes the F2 request for floor 1 downward branch and S1 arrival back to F1 stop. | ✅ |
| `f3_ps1_md1_arrive_f1` | explicit-hot-start probes the distinct F3 request for floor 1 transition to MD1 and S1 arrival at F1. | ✅ |
| `reset_from_up_motion_forces_f1` | explicit-hot-start verifies reset from an upward motion state forces floor 1 stop regardless of current travel context. | ✅ |
| `reset_from_down_motion_forces_f1` | explicit-hot-start verifies reset from a downward motion state forces floor 1 stop regardless of current travel context. | ✅ |
| `reset_from_floor_context_forces_f1` | explicit-hot-start verifies reset from a non-F1 floor context also forces floor 1 stop. | ✅ |

#### Repair / blocking feedback 概览（report §7 摘录）

- 本 run 未进入 `SD-8/SL-9/SL-10` repair block；通常表示流程在 repair 前已成功、被 provider/schema 错误中断，或在 pre-repair 阶段直接退出。

### 8. 尝试记录与成本

- `SL-1`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 2520, 'completion_chars': 9336, 'completion_tokens': 3039, 'elapsed_seconds': 57.22732620999159, 'estimated_completion_tokens': 2334, 'estimated_prompt_tokens': 6523, 'estimated_total_tokens': 8857, 'first_chunk_seconds': 13.315957890998106, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 26089, 'prompt_tokens': 6438, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 9477}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1277, 'completion_chars': 4909, 'completion_tokens': 2100, 'elapsed_seconds': 42.07691753900144, 'estimated_completion_tokens': 1228, 'estimated_prompt_tokens': 11134, 'estimated_total_tokens': 12362, 'first_chunk_seconds': 18.981963789003203, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 44534, 'prompt_tokens': 11358, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 13458}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-7`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1337, 'completion_chars': 5481, 'completion_tokens': 1856, 'elapsed_seconds': 36.43822399499186, 'estimated_completion_tokens': 1371, 'estimated_prompt_tokens': 8325, 'estimated_total_tokens': 9696, 'first_chunk_seconds': 12.30122371399193, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 33300, 'prompt_tokens': 8801, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 10657}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。

### 9. 最终停止状态与后续含义

- 停止状态：verdict=`success`，record_status=`success`。
- 主要原因分类：`success`。
- required stages executed：`12/12`，missing=`<none>`。
- repairs：`0/0` accepted；scenario_history=`1`。
- 配置含义：`recommended baseline candidate`；该结果可用于评估默认入口本身。
- 主结果/蓝本边界：`main_result_eligible` 只表示该 run 非 provider-invalid 且 trace/schema/secret/final-verdict 口径可进入主结果候选；`path2_ref_model_blueprint_eligible=false` 时，模型仍可作为 FE/BVS 或 dispatch-classifier 压力测试证据，但不得称为 Path2 ref-model 主蓝本。
- 样本含义：若出现 `design_or_variable_dynamics`，应重点审查变量是否仅作为 guard/input 常量而没有事件/动作更新；若出现 pre-scenario parse/semantic 失败，则应先优化 pyfcstm grammar adherence。

> 完整 repair 细节、进入修复原因、SD-8 修改建议、SL-9 candidate、before→candidate diff 与 local-check evidence 与 SL-10 审查证据见 `../runs/pr_langgraph_real_agent_loop_round1_stategraph/pr-e1-path1_elevator-default-prlanggraph-stategraph-r1-0cdc09ec/report.md` §7。

</details>

<details><summary>path2 / path2_lng_ems / default / success</summary>

#### NL 输入（原文）

```text
The LNG-ship EMS manages a ship energy system with PVs, WECs, DGs, LNG, batteries, and time-varying ship loads, issuing cut-in and cut-out commands for generating units and loads. It controls power dispatch between generating units and load demand during changing time periods and operating conditions, dynamically switching states to maintain power balance as resources and demands vary. The FSM reads load demand PL, renewable contributions Ppv and Pw, battery state of charge SoC, and engine capacity bounds such as eng3_Pmax, then returns requested generator power, battery discharge or charging power, and spare power. The twelve finite states are selected by logical transition conditions over demand, generation, capacity, and SoC. When Ppv + Pw covers PL, the EMS serves all ship demand from RES and charges batteries while SoC is below 0.95, or treats residual renewable power as spare once SoC is at least 0.95. When Ppv + Pw is below PL, dispatch follows the stated priority: RES first, batteries when SoC is suitable, LNG before diesel units, and DG1/DG2 only as the last priority. Low-SoC branches add explicit charging margins, including Pgmax/5 in an LNG-covered case and Pd1max/10 in later diesel-generator cases. When PL = 0, RES production is sent to battery charging or to spare power according to SoC thresholds. The overload completion state is illegal: if extreme demand exceeds all RES and thermal resources, EMS activates all thermal generating units, covers the lack by battery discharge, and the state shall never occur in practice.
```

#### NL 输入中文翻译

```text
LNG 船 EMS 管理一个包含光伏、波浪能、柴油机、LNG、电池和随时间变化船舶负载的船舶能源系统，并向发电单元与负载发出切入/切出命令。它在变化的时段和运行条件下控制发电单元与负载需求之间的功率调度，随着资源和需求变化动态切换状态以保持功率平衡。FSM 读取负载需求 PL、可再生贡献 Ppv 和 Pw、电池荷电状态 SoC，以及 eng3_Pmax 等发动机容量边界，然后返回请求的发电机功率、电池放电或充电功率以及备用功率。十二个有限状态由需求、发电、容量和 SoC 上的逻辑转移条件选择。当 Ppv + Pw 覆盖 PL 时，EMS 用 RES 满足全部船舶需求，并在 SoC 低于 0.95 时给电池充电，或在 SoC 至少为 0.95 时把剩余可再生功率视为备用功率。当 Ppv + Pw 低于 PL 时，调度遵循优先级：RES 优先，SoC 合适时使用电池，LNG 先于柴油机，DG1/DG2 只作为最后优先级。低 SoC 分支加入明确充电裕量，包括 LNG 覆盖场景中的 Pgmax/5，以及后续柴油发电机场景中的 Pd1max/10。当 PL = 0 时，RES 产出根据 SoC 阈值送往电池充电或备用功率。过载完成状态是非法状态：若极端需求超过全部 RES 与热力资源，EMS 会激活全部热发电单元并用电池放电弥补缺口，该状态实践中不应发生。
```

#### FCSTM 输出

```pyfcstm
def float PL = 0.0;
def float Ppv = 0.0;
def float Pw = 0.0;
def float SoC = 0.50;
def float Pgmax = 0.0;
def float eng3_Pmax = 0.0;
def float Pd1max = 0.0;
def float Pd2max = 0.0;
def float Pbat_discharge_Pmax = 0.0;
def float Pgen_req = 0.0;
def float PLNG_req = 0.0;
def float PENG3_req = 0.0;
def float PDG1_req = 0.0;
def float PDG2_req = 0.0;
def float Pbat_discharge = 0.0;
def float Pbat_charge = 0.0;
def float Pspare = 0.0;
def int cutin_LNG = 0;
def int cutout_LNG = 0;
def int cutin_ENG3 = 0;
def int cutout_ENG3 = 0;
def int cutin_DG1 = 0;
def int cutout_DG1 = 0;
def int cutin_DG2 = 0;
def int cutout_DG2 = 0;
def int load_cutout = 0;

state LNGShipEMS {
    ! * -> IllegalOverloadCompletion : if [PL - Ppv - Pw > Pgmax + eng3_Pmax + Pd1max + Pd2max];
    ! * -> ZeroLoad_RES_Charge : if [PL == 0 && Ppv + Pw > 0 && SoC < 0.95];
    ! * -> ZeroLoad_RES_Spare : if [PL == 0 && Ppv + Pw > 0 && SoC >= 0.95];
    ! * -> ZeroLoad_RES_Spare : if [PL == 0 && Ppv + Pw <= 0];
    ! * -> RES_Covers_Load_Charge : if [PL > 0 && Ppv + Pw >= PL && SoC < 0.95];
    ! * -> RES_Covers_Load_Spare : if [PL > 0 && Ppv + Pw >= PL && SoC >= 0.95];
    ! * -> Battery_Discharge_Priority : if [PL > 0 && Ppv + Pw < PL && SoC >= 0.20 && PL - Ppv - Pw <= Pbat_discharge_Pmax];
    ! * -> LNG_Covers_Load_LowSoC_ChargeMargin : if [PL > 0 && Ppv + Pw < PL && SoC < 0.20 && PL - Ppv - Pw + Pgmax / 5 <= Pgmax];
    ! * -> LNG_Covers_Load : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw <= Pgmax && (SoC < 0.20 || PL - Ppv - Pw > Pbat_discharge_Pmax)];
    ! * -> LNG_Engine3_Covers_Load : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > Pgmax && PL - Ppv - Pw <= Pgmax + eng3_Pmax];
    ! * -> DG1_Covers_Load_LowSoC_ChargeMargin : if [PL > 0 && Ppv + Pw < PL && SoC < 0.20 && PL - Ppv - Pw > Pgmax + eng3_Pmax && PL - Ppv - Pw + Pd1max / 10 <= Pgmax + eng3_Pmax + Pd1max];
    ! * -> DG1_Covers_Load : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > Pgmax + eng3_Pmax && PL - Ppv - Pw <= Pgmax + eng3_Pmax + Pd1max];
    ! * -> DG2_Covers_Load_WithOptionalChargeMargin : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > Pgmax + eng3_Pmax + Pd1max && PL - Ppv - Pw <= Pgmax + eng3_Pmax + Pd1max + Pd2max];

    [*] -> ZeroLoad_RES_Charge;

    state ZeroLoad_RES_Charge {
        enter {
            Pgen_req = 0;
            PLNG_req = 0;
            PENG3_req = 0;
            PDG1_req = 0;
            PDG2_req = 0;
            Pbat_discharge = 0;
            Pbat_charge = Ppv + Pw;
            Pspare = 0;
            cutin_LNG = 0;
            cutout_LNG = 1;
            cutin_ENG3 = 0;
            cutout_ENG3 = 1;
            cutin_DG1 = 0;
            cutout_DG1 = 1;
            cutin_DG2 = 0;
            cutout_DG2 = 1;
            load_cutout = 0;
        }
    }

    state ZeroLoad_RES_Spare {
        enter {
            Pgen_req = 0;
            PLNG_req = 0;
            PENG3_req = 0;
            PDG1_req = 0;
            PDG2_req = 0;
            Pbat_discharge = 0;
            Pbat_charge = 0;
            Pspare = Ppv + Pw;
            cutin_LNG = 0;
            cutout_LNG = 1;
            cutin_ENG3 = 0;
            cutout_ENG3 = 1;
            cutin_DG1 = 0;
            cutout_DG1 = 1;
            cutin_DG2 = 0;
            cutout_DG2 = 1;
            load_cutout = 0;
        }
    }

    state RES_Covers_Load_Charge {
        enter {
            Pgen_req = 0;
            PLNG_req = 0;
            PENG3_req = 0;
            PDG1_req = 0;
            PDG2_req = 0;
            Pbat_discharge = 0;
            Pbat_charge = Ppv + Pw - PL;
            Pspare = 0;
            cutin_LNG = 0;
            cutout_LNG = 1;
            cutin_ENG3 = 0;
            cutout_ENG3 = 1;
            cutin_DG1 = 0;
            cutout_DG1 = 1;
            cutin_DG2 = 0;
            cutout_DG2 = 1;
            load_cutout = 0;
        }
    }

    state RES_Covers_Load_Spare {
        enter {
            Pgen_req = 0;
            PLNG_req = 0;
            PENG3_req = 0;
            PDG1_req = 0;
            PDG2_req = 0;
            Pbat_discharge = 0;
            Pbat_charge = 0;
            Pspare = Ppv + Pw - PL;
            cutin_LNG = 0;
            cutout_LNG = 1;
            cutin_ENG3 = 0;
            cutout_ENG3 = 1;
            cutin_DG1 = 0;
            cutout_DG1 = 1;
            cutin_DG2 = 0;
            cutout_DG2 = 1;
            load_cutout = 0;
        }
    }

    state Battery_Discharge_Priority {
        enter {
            Pgen_req = 0;
            PLNG_req = 0;
            PENG3_req = 0;
            PDG1_req = 0;
            PDG2_req = 0;
            Pbat_discharge = PL - Ppv - Pw;
            Pbat_charge = 0;
            Pspare = 0;
            cutin_LNG = 0;
            cutout_LNG = 1;
            cutin_ENG3 = 0;
            cutout_ENG3 = 1;
            cutin_DG1 = 0;
            cutout_DG1 = 1;
            cutin_DG2 = 0;
            cutout_DG2 = 1;
            load_cutout = 0;
        }
    }

    state LNG_Covers_Load {
        enter {
            Pgen_req = PL - Ppv - Pw;
            PLNG_req = PL - Ppv - Pw;
            PENG3_req = 0;
            PDG1_req = 0;
            PDG2_req = 0;
            Pbat_discharge = 0;
            Pbat_charge = 0;
            Pspare = 0;
            cutin_LNG = 1;
            cutout_LNG = 0;
            cutin_ENG3 = 0;
            cutout_ENG3 = 1;
            cutin_DG1 = 0;
            cutout_DG1 = 1;
            cutin_DG2 = 0;
            cutout_DG2 = 1;
            load_cutout = 0;
        }
    }

    state LNG_Covers_Load_LowSoC_ChargeMargin {
        enter {
            Pgen_req = PL - Ppv - Pw + Pgmax / 5;
            PLNG_req = PL - Ppv - Pw + Pgmax / 5;
            PENG3_req = 0;
            PDG1_req = 0;
            PDG2_req = 0;
            Pbat_discharge = 0;
            Pbat_charge = Pgmax / 5;
            Pspare = 0;
            cutin_LNG = 1;
            cutout_LNG = 0;
            cutin_ENG3 = 0;
            cutout_ENG3 = 1;
            cutin_DG1 = 0;
            cutout_DG1 = 1;
            cutin_DG2 = 0;
            cutout_DG2 = 1;
            load_cutout = 0;
        }
    }

    state LNG_Engine3_Covers_Load {
        enter {
            Pgen_req = PL - Ppv - Pw;
            PLNG_req = Pgmax;
            PENG3_req = PL - Ppv - Pw - Pgmax;
            PDG1_req = 0;
            PDG2_req = 0;
            Pbat_discharge = 0;
            Pbat_charge = 0;
            Pspare = 0;
            cutin_LNG = 1;
            cutout_LNG = 0;
            cutin_ENG3 = 1;
            cutout_ENG3 = 0;
            cutin_DG1 = 0;
            cutout_DG1 = 1;
            cutin_DG2 = 0;
            cutout_DG2 = 1;
            load_cutout = 0;
        }
    }

    state DG1_Covers_Load {
        enter {
            Pgen_req = PL - Ppv - Pw;
            PLNG_req = Pgmax;
            PENG3_req = eng3_Pmax;
            PDG1_req = PL - Ppv - Pw - Pgmax - eng3_Pmax;
            PDG2_req = 0;
            Pbat_discharge = 0;
            Pbat_charge = 0;
            Pspare = 0;
            cutin_LNG = 1;
            cutout_LNG = 0;
            cutin_ENG3 = 1;
            cutout_ENG3 = 0;
            cutin_DG1 = 1;
            cutout_DG1 = 0;
            cutin_DG2 = 0;
            cutout_DG2 = 1;
            load_cutout = 0;
        }
    }

    state DG1_Covers_Load_LowSoC_ChargeMargin {
        enter {
            Pgen_req = PL - Ppv - Pw + Pd1max / 10;
            PLNG_req = Pgmax;
            PENG3_req = eng3_Pmax;
            PDG1_req = PL - Ppv - Pw - Pgmax - eng3_Pmax + Pd1max / 10;
            PDG2_req = 0;
            Pbat_discharge = 0;
            Pbat_charge = Pd1max / 10;
            Pspare = 0;
            cutin_LNG = 1;
            cutout_LNG = 0;
            cutin_ENG3 = 1;
            cutout_ENG3 = 0;
            cutin_DG1 = 1;
            cutout_DG1 = 0;
            cutin_DG2 = 0;
            cutout_DG2 = 1;
            load_cutout = 0;
        }
    }

    state DG2_Covers_Load_WithOptionalChargeMargin {
        enter {
            if [SoC < 0.20] {
                Pgen_req = PL - Ppv - Pw + Pd1max / 10;
                PLNG_req = Pgmax;
                PENG3_req = eng3_Pmax;
                PDG1_req = Pd1max;
                PDG2_req = PL - Ppv - Pw - Pgmax - eng3_Pmax - Pd1max + Pd1max / 10;
                Pbat_charge = Pd1max / 10;
            } else {
                Pgen_req = PL - Ppv - Pw;
                PLNG_req = Pgmax;
                PENG3_req = eng3_Pmax;
                PDG1_req = Pd1max;
                PDG2_req = PL - Ppv - Pw - Pgmax - eng3_Pmax - Pd1max;
                Pbat_charge = 0;
            }
            Pbat_discharge = 0;
            Pspare = 0;
            cutin_LNG = 1;
            cutout_LNG = 0;
            cutin_ENG3 = 1;
            cutout_ENG3 = 0;
            cutin_DG1 = 1;
            cutout_DG1 = 0;
            cutin_DG2 = 1;
            cutout_DG2 = 0;
            load_cutout = 0;
        }
    }

    state IllegalOverloadCompletion {
        enter {
            Pgen_req = Pgmax + eng3_Pmax + Pd1max + Pd2max;
            PLNG_req = Pgmax;
            PENG3_req = eng3_Pmax;
            PDG1_req = Pd1max;
            PDG2_req = Pd2max;
            Pbat_discharge = PL - Ppv - Pw - Pgmax - eng3_Pmax - Pd1max - Pd2max;
            Pbat_charge = 0;
            Pspare = 0;
            cutin_LNG = 1;
            cutout_LNG = 0;
            cutin_ENG3 = 1;
            cutout_ENG3 = 0;
            cutin_DG1 = 1;
            cutout_DG1 = 0;
            cutin_DG2 = 1;
            cutout_DG2 = 0;
            load_cutout = 1;
        }
    }
}
```

#### agent-loop 过程与日志路径

| 项 | 值 |
|---|---|
| verdict / status | `success` / `success` |
| failure class | `success_but_weak_oracle_ineligible` |
| main_result_eligible | `false` |
| path2_ref_model_blueprint | `false`；run_not_main_result_eligible |
| state_mode_decorative | `true` |
| executed stages | `SC-0 -> SL-1 -> SD-2 -> SD-3 -> SD-4 -> SD-8 -> SL-9 -> SL-10 -> SC-11 -> SD-2 -> SD-3 -> SD-4 -> SD-8 -> SL-9 -> SD-4 -> SL-5 -> SD-5A -> SL-5 -> SD-5A -> SL-5 -> SD-5A -> SC-5F -> SD-6 -> SL-7 -> SD-2 -> SD-3 -> SD-4 -> SD-5A -> SC-5F -> SD-6 -> SL-7 -> SD-8 -> SL-9 -> SL-10 -> SL-9 -> SL-10 -> SC-11 -> SD-2 -> SD-3 -> SD-4 -> SD-5A -> SL-5 -> SD-5A -> SL-5 -> SD-5A -> SC-5F -> SD-6 -> SL-7 -> SD-8 -> SL-9 -> SL-10 -> SC-11 -> SD-2 -> SD-3 -> SD-4 -> SD-5A -> SL-5 -> SD-5A -> SL-5 -> SD-5A -> SC-5F -> SD-6 -> SL-7 -> SC-12 -> SC-13` |
| iter / repairs / accepted / scenarios | `5` / `5` / `3` / `10` |
| token / elapsed | `{'prompt_tokens': 843981, 'completion_tokens': 99686, 'total_tokens': 943667, 'estimated_prompt_tokens': 835132, 'estimated_completion_tokens': 66540, 'estimated_total_tokens': 901672, 'prompt_chars': 3340501, 'completion_chars': 266135, 'n_calls': 21, 'token_usage_available': True, 'token_usage_unavailable_calls': 0}` / `1888.78s` |
| full stage table | `../runs/pr_langgraph_real_agent_loop_round1_stategraph/pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f/report.md` §4 |
| run record | `../runs/pr_langgraph_real_agent_loop_round1_stategraph/pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f/pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz` |
| logs | `../runs/pr_langgraph_real_agent_loop_round1_stategraph/pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f/run_logs/stdout.txt`, `../runs/pr_langgraph_real_agent_loop_round1_stategraph/pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f/run_logs/stderr.txt` |
| checks / repro | `../runs/pr_langgraph_real_agent_loop_round1_stategraph/pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f/checks.json`, `../runs/pr_langgraph_real_agent_loop_round1_stategraph/pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f/reproducibility.json` |

#### 全流程摘要表（report §4 摘录）

| Stage | 是否 LLM | iteration | 结果 | 获取的信息 / 反馈 | 本阶段做了什么 | DSL 修改 | artifact/log |
|---|---:|---:|---:|---|---|---|---|
| `SC-0` | 否 | - | ✅ | trace/control | 初始化 run state | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |
| `SL-1` | 是 | - | ✅ | LLM calls=1, tokens=16354 | 生成初始 DSL 与 grounding seeds | initial len=9700 | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ⚠️ | blocking=136, advisory=54, info=0; blocking=50, advisory=138, info=0; blocking=0, advisory=188, info=0; blocking=0, advisory=188, info=0; blocking=0, advisory=188, info=0; blocking | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=5, tokens=295142 | LLM per-request accept/reject + repair | candidate len=9506,0,9589,9484,9548 | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=4, tokens=160081 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ⚠️ | blocking=136, advisory=54, info=0; blocking=50, advisory=138, info=0; blocking=0, advisory=188, info=0; blocking=0, advisory=188, info=0; blocking=0, advisory=188, info=0; blocking | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=5, tokens=295142 | LLM per-request accept/reject + repair | candidate len=9506,0,9589,9484,9548 | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ⚠️ | blocking=136, advisory=54, info=0; blocking=50, advisory=138, info=0; blocking=0, advisory=188, info=0; blocking=0, advisory=188, info=0; blocking=0, advisory=188, info=0; blocking | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |
| `SL-5` | 是 | 1 | ✅ | LLM calls=7, tokens=224139 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |
| `SD-5A` | 否 | 1 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |
| `SL-5` | 是 | 1 | ✅ | LLM calls=7, tokens=224139 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |
| `SD-5A` | 否 | 1 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |
| `SL-5` | 是 | 1 | ✅ | LLM calls=7, tokens=224139 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |
| `SD-5A` | 否 | 1 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |
| `SC-5F` | 否 | 1 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |
| `SD-6` | 否 | 1 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |
| `SL-7` | 是 | 1 | ✅ | LLM calls=4, tokens=247951 | LLM model review | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=136, advisory=54, info=0; blocking=50, advisory=138, info=0; blocking=0, advisory=188, info=0; blocking=0, advisory=188, info=0; blocking=0, advisory=188, info=0; blocking | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |
| `SD-5A` | 否 | 1 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |
| `SC-5F` | 否 | 1 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |
| `SD-6` | 否 | 1 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |
| `SL-7` | 是 | 1 | ✅ | LLM calls=4, tokens=247951 | LLM model review | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=5, tokens=295142 | LLM per-request accept/reject + repair | candidate len=9506,0,9589,9484,9548 | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ⚠️ | LLM calls=4, tokens=160081 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=5, tokens=295142 | LLM per-request accept/reject + repair | candidate len=9506,0,9589,9484,9548 | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=4, tokens=160081 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=136, advisory=54, info=0; blocking=50, advisory=138, info=0; blocking=0, advisory=188, info=0; blocking=0, advisory=188, info=0; blocking=0, advisory=188, info=0; blocking | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |
| `SD-5A` | 否 | 1 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |
| `SL-5` | 是 | 1 | ✅ | LLM calls=7, tokens=224139 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |
| `SD-5A` | 否 | 1 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |
| `SL-5` | 是 | 1 | ✅ | LLM calls=7, tokens=224139 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |
| `SD-5A` | 否 | 1 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |
| `SC-5F` | 否 | 1 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |
| `SD-6` | 否 | 1 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |
| `SL-7` | 是 | 1 | ✅ | LLM calls=4, tokens=247951 | LLM model review | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=5, tokens=295142 | LLM per-request accept/reject + repair | candidate len=9506,0,9589,9484,9548 | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=4, tokens=160081 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=136, advisory=54, info=0; blocking=50, advisory=138, info=0; blocking=0, advisory=188, info=0; blocking=0, advisory=188, info=0; blocking=0, advisory=188, info=0; blocking | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |
| `SD-5A` | 否 | 1 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |
| `SL-5` | 是 | 1 | ✅ | LLM calls=7, tokens=224139 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |
| `SD-5A` | 否 | 1 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |
| `SL-5` | 是 | 1 | ✅ | LLM calls=7, tokens=224139 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |
| `SD-5A` | 否 | 1 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |
| `SC-5F` | 否 | 1 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |
| `SD-6` | 否 | 1 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |
| `SL-7` | 是 | 1 | ✅ | LLM calls=4, tokens=247951 | LLM model review | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |
| `SC-12` | 否 | - | ✅ | full_pass_all_required_feedback_ok | 写 final verdict | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |
| `SC-13` | 否 | - | ✅ | trace/control | 写审计 run record | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |

### 4.1 完整流程日志（stage/control-flow replay ledger）

口径：本节来自 `AgentLoopRunRecord.logs`，与 [`flow_log.json`](./flow_log.json) 一致；用于复现每个 stage 如何进入、得到什么批示、跳转到哪里，以及每次 DSL 产物/候选如何变化。

| # | ts | stage | iter | event | result / jump | DSL evidence |
|---:|---|---|---:|---|---|---|
| 1 | `2026-06-04T14:51:22Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 2 | `2026-06-04T14:51:22Z` | `SC-0` | `-` | `run_start` | {} | <none> |
| 3 | `2026-06-04T14:51:22Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 4 | `2026-06-04T14:51:22Z` | `SL-1` | `-` | `stage_enter` | {"reason": "initial_modeling_adapter_available"} | <none> |
| 5 | `2026-06-04T14:54:23Z` | `SL-1` | `-` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 6 | `2026-06-04T14:54:23Z` | `SL-1` | `-` | `stage_result` | {"jump": "SD-2", "ok": true} | candidate_dsl:len=9700,hash=sha256:3ea5c49f5dbb |
| 7 | `2026-06-04T14:54:23Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
... <truncated 12087 chars in PR comment; see report.md>

#### Scenario 逐轮通过矩阵（report §6.1 摘录）

口径：`✅` = 该 scenario 在该轮 SD-6 simulation 通过；`❌` = 该轮失败；`⚪` = 该轮未执行或无该 scenario 结果。

| Scenario | Intent | Iter 2 | Iter 3 | Iter 4 | Iter 5 |
|---|---|---|---|---|---|
| `default_init_zero_load_res_charge` | default-init: after the first empty cycle, PL=0 with RES available and SoC below 0.95 selects zero-load battery charging...<truncated 28 chars> | ✅ | ✅ | ✅ | ✅ |
| `zero_load_full_soc_res_spare` | explicit-hot-start: PL=0 with RES available and SoC at the 0.95 boundary sends renewable production to spare power inste...<truncated 15 chars> | ✅ | ✅ | ✅ | ✅ |
| `res_covers_load_soc_below_full_charges` | explicit-hot-start: when RES covers positive load and SoC is just below 0.95, demand is served from RES and residual pow...<truncated 23 chars> | ✅ | ✅ | ✅ | ✅ |
| `res_covers_load_soc_full_spare` | explicit-hot-start: when RES covers positive load and SoC is exactly 0.95, residual renewable power is treated as spare. | ✅ | ✅ | ✅ | ✅ |
| `battery_priority_at_low_soc_boundary` | explicit-hot-start: when RES is below load, SoC is exactly the suitable-battery boundary 0.20, and the deficit fits batt...<truncated 55 chars> | ✅ | ✅ | ✅ | ✅ |
| `lng_low_soc_charge_margin` | explicit-hot-start: with low SoC below 0.20 and an LNG-coverable deficit, the LNG branch includes the Pgmax/5 charging m...<truncated 6 chars> | ✅ | ✅ | ✅ | ✅ |
| `lng_normal_covers_deficit_before_diesel` | explicit-hot-start: when battery cannot cover the deficit but LNG capacity can, LNG is cut in before any diesel units. | ✅ | ✅ | ✅ | ✅ |
| `lng_engine3_covers_after_lng_capacity` | explicit-hot-start: when the deficit exceeds LNG capacity but fits LNG plus engine3 capacity, LNG and engine3 are cut in...<truncated 26 chars> | ✅ | ✅ | ✅ | ✅ |
| `dg1_low_soc_charge_margin` | explicit-hot-start: when demand exceeds LNG plus engine3 and SoC is below 0.20, the DG1 low-SoC branch adds the Pd1max/1...<truncated 18 chars> | ✅ | ✅ | ✅ | ✅ |
| `dg1_normal_last_priority_before_dg2` | explicit-hot-start: with suitable SoC, demand beyond LNG plus engine3 but within DG1 capacity cuts in DG1 before DG2. | ✅ | ✅ | ✅ | ✅ |
| `dg2_low_soc_optional_charge_margin` | explicit-hot-start: when demand exceeds LNG, engine3, and DG1 capacity but fits DG2, DG2 is last-priority and low SoC ad...<truncated 40 chars> | ✅ | ✅ | ✅ | ✅ |
| `illegal_overload_activates_all_thermal_and_battery` | explicit-hot-start: for demand beyond RES and all thermal capacity, the illegal overload completion branch activates all...<truncated 66 chars> | ✅ | ✅ | ✅ | ✅ |
| `forced_reclassification_from_illegal_to_res_charge` | explicit-hot-start: a wildcard forced classification must re-evaluate from a concrete illegal-overload leaf to RES-cover...<truncated 96 chars> | ⚪ | ⚪ | ✅ | ✅ |
| `forced_reclassification_from_res_charge_to_illegal` | explicit-hot-start: a wildcard forced classification must also re-evaluate from a normal RES-charge leaf to illegal over...<truncated 108 chars> | ⚪ | ⚪ | ⚪ | ✅ |
| `forced_reclassification_from_dg2_to_zero_load_no_res_spare` | explicit-hot-start: a wildcard forced classification must re-evaluate from a DG2 leaf to the zero-load no-RES spare/idle...<truncated 113 chars> | ⚪ | ⚪ | ⚪ | ✅ |
| `forced_reclassification_from_illegal_to_res_spare` |  | ✅ | ✅ | ⚪ | ⚪ |
| `forced_reclassification_from_zero_load_to_illegal` |  | ✅ | ✅ | ⚪ | ⚪ |
| `forced_reclassification_to_zero_load_charge_from_dg2` |  | ✅ | ✅ | ⚪ | ⚪ |

#### Repair / blocking feedback 概览（report §7 摘录）

口径：本节记录 agent-loop 真实进入 repair block 后的证据链：FixRequestBatch、SL-9 per-request accept/reject、candidate diff、local-check evidence、SL-10(NL+FixLog) 审阅，以及完整 FixLog ledger 摘录。

| Repair | iteration | accepted | source | blocking diagnostics | SL-9 decisions | SL-10 / local checks | candidate hash |
|---:|---:|---:|---|---|---|---|---|
| 1 | `0` | ✅ | `SD-4` | W_UNWRITTEN_READ_VAR:var_name=SoC_full_threshold, W_UNWRITTEN_READ_VAR:var_name=SoC_low_threshold, W_UNWRITTEN_READ_VAR:var_name=Pd2max, W_UNWRITTEN_READ_VAR:var_name=Pbat_discharge_Pmax, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoad_RES_Charge:to_path=LNGShipEMS.IllegalOverloadCompletion, ... +136 | accept=8, reject=4, waiver=4 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none>; local ok=False, target=False, regression=False, drift=major, local_stage=SD-10, reason=design_target_unresolved; missing_required_grounding | `sha256:ae74dfc8a541f448b34f805ad6dbf46262a2b2b804509e2e7866abecbe67c8aa` |
| 2 | `1` | ❌ | `SD-4` | W_UNWRITTEN_READ_VAR:var_name=Pd2max, W_UNWRITTEN_READ_VAR:var_name=Pbat_discharge_Pmax, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoad_RES_Charge:to_path=LNGShipEMS.IllegalOverloadCompletion, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoad_RES_Charge:to_path=LNGShipEMS.Battery_Discharge_Priority, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoad_RES_Charge:to_path=LNGShipEMS.LNG_Covers_Load, ... +50 | accept=0, reject=12, waiver=12 | <none> | `sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 3 | `2` | ❌ | `SL-7` | 0, 1, 2, 3 | accept=4, reject=0, waiver=0 | SL-10 decision=rework, ok=False, target=True, regression=False, drift=minor, rework=SL-10 pass was downgraded because local deterministic evidence reported major drift and SL-10 evidence did not explicitly address the local rejection reason/kind with a structu...<truncated 678 chars> | `sha256:4c5a6347ae4632bd2b168c1d08eef85bdcfb190e6335c8e955fb8d53d02b8d19` |
| 4 | `2` | ✅ | `SL-7` | 0, 1, 2, 3 | accept=4, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none>; local ok=False, target=False, regression=False, drift=major, local_stage=SD-10, reason=missing_required_grounding | `sha256:27ff012eeca8958395886399d5f506d668adb07be506c45860ce7acb776355e5` |
| 5 | `3` | ✅ | `SL-7` | 0, 1 | accept=2, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none>; local ok=False, target=False, regression=False, drift=major, local_stage=SD-10, reason=forced_transition_count_drift; missing_required_grounding | `sha256:4b52356070e7a51d779df874526281152b5fb3e1dac5b2f71a14dc2af9ccf364` |

> 完整 repair 细节、进入修复原因、SD-8 修改建议、SL-9 candidate、before→candidate diff 与 local-check evidence 与 SL-10 审查证据见 `../runs/pr_langgraph_real_agent_loop_round1_stategraph/pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f/report.md` §7。

</details>
