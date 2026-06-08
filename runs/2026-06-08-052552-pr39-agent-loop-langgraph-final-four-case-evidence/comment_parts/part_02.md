## 四例真实运行 evidence（20f104e8，part 2/3）

身份：主 session / LG-M1-G runner。

本条为 PR #77 在最新 head `20f104e8` 上重跑 ABS / CARA / Elevator / LNG 四例的 evidence 分片；完整 artifact 目录：`runs/2026-06-08-052552-pr39-agent-loop-langgraph-final-four-case-evidence`。

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
    ! * -> F1 : Reset;

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
| SC-11 post-accept validation | `⚪ 0` |
| executed stages | `SC-0 -> SL-1 -> SD-2 -> SD-3 -> SD-4 -> SL-5 -> SD-5A -> SC-5F -> SD-6 -> SL-7 -> SC-12 -> SC-13` |
| iter / repairs / accepted / scenarios | `1` / `0` / `0` / `1` |
| token / elapsed | `{'prompt_tokens': 27092, 'completion_tokens': 7164, 'total_tokens': 34256, 'estimated_prompt_tokens': 26327, 'estimated_completion_tokens': 5546, 'estimated_total_tokens': 31873, 'prompt_chars': 105302, 'completion_chars': 22178, 'n_calls': 3, 'token_usage_available': True, 'token_usage_unavailable_calls': 0}` / `144.075s` |
| full stage table | `runs/2026-06-08-052552-pr39-agent-loop-langgraph-final-four-case-evidence/path1-elevator-agent-loop-success/report.md` §4 |
| run record | `runs/2026-06-08-052552-pr39-agent-loop-langgraph-final-four-case-evidence/path1-elevator-agent-loop-success/pr-e1-path1_elevator-default-lg_m1_g_signature_gate_20f104e8-d5b14175.agent_loop.json.gz` |
| logs | `runs/2026-06-08-052552-pr39-agent-loop-langgraph-final-four-case-evidence/path1-elevator-agent-loop-success/run_logs/stdout.txt`, `runs/2026-06-08-052552-pr39-agent-loop-langgraph-final-four-case-evidence/path1-elevator-agent-loop-success/run_logs/stderr.txt` |
| checks / repro | `runs/2026-06-08-052552-pr39-agent-loop-langgraph-final-four-case-evidence/path1-elevator-agent-loop-success/checks.json`, `runs/2026-06-08-052552-pr39-agent-loop-langgraph-final-four-case-evidence/path1-elevator-agent-loop-success/reproducibility.json` |

#### LangGraph runtime metadata 摘要（report §1.1 摘录）

| 字段 | 值 |
|---|---|
| `graph_runtime_backend` | `langgraph` |
| `graph_runtime_status` | `enabled` |
| `graph_runtime_backend_version` | `pr-langgraph.stategraph.v1` |
| `langgraph_version` | `1.2.4` |
| `langgraph_checkpoint_version` | `4.1.1` |
| `graph_runtime_id` | `langgraph:pr-langgraph.stategraph.v1` |
| `graph_config_hash` | `sha256:9341198a81a116688f6f98b2882ff9a29a3a8bcd62cf964751b73148587e3eba` |
| `node_edge_schema_version` | `pr-langgraph.stage-nodes.v1` |
| `checkpoint_backend` | `memory` |
| `checkpoint_backend_type` | `InMemorySaver` |
| `checkpoint_serde` | `pickle` |
| `checkpoint_path_hash` | `sha256:memory` |
| `resumed_from_checkpoint` | `False` |
| `resume_checkpoint_id_hash` | `None` |
| `instrumentation_layer` | `langgraph` |
| `stage_semantics_module` | `method.staged_runtime` |
| `langgraph_node_trace_count` | `16` |
| `langgraph_node_trace_hash` | `sha256:fb96b701bb9df74ebe9108c05996a7d6f6a443a5ae41b9e57d2ce16d3307f474` |
| `langgraph_compat_ok` | `True` |
| `checkpoint_resume_smoke_scope` | `toy_ledger_langgraph_api_smoke` |
| `real_agent_loop_resume_supported` | `False` |
| `resume_append_only` | `True` |
| `final_trace_delegated_monolithic_runtime` | `False` |
| `final_trace_node_trace_count` | `16` |

- checkpoint 口径：This smoke validates LangGraph interrupt/resume API shape and append-only ledger behavior on a minimal FixLog-like state only. It is not evidence that an interrupted real agent-loop run can be resumed for main-result statistics.
- 注意：`real_agent_loop_resume_supported=false` 时，只能宣称 LangGraph checkpoint API / toy FixLog-like ledger smoke 通过；不能把它写成真实 agent-loop 中断恢复已用于主结果统计。

#### 全流程摘要表（report §4 摘录）

| Stage | 是否 LLM | iteration | 结果 | 获取的信息 / 反馈 | 本阶段做了什么 | DSL 修改 | artifact/log |
|---|---:|---:|---:|---|---|---|---|
| `SC-0` | 否 | - | ✅ | trace/control | 初始化 run state | 无/见 record | [`record`](../path1-elevator-agent-loop-success/pr-e1-path1_elevator-default-lg_m1_g_signature_gate_20f104e8-d5b14175.agent_loop.json.gz) |
| `SL-1` | 是 | - | ✅ | LLM calls=1, tokens=9575 | 生成初始 DSL 与 grounding seeds | initial len=658 | [`record`](../path1-elevator-agent-loop-success/pr-e1-path1_elevator-default-lg_m1_g_signature_gate_20f104e8-d5b14175.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](../path1-elevator-agent-loop-success/pr-e1-path1_elevator-default-lg_m1_g_signature_gate_20f104e8-d5b14175.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](../path1-elevator-agent-loop-success/pr-e1-path1_elevator-default-lg_m1_g_signature_gate_20f104e8-d5b14175.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=1, info=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](../path1-elevator-agent-loop-success/pr-e1-path1_elevator-default-lg_m1_g_signature_gate_20f104e8-d5b14175.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=1, tokens=14097 | 生成模型测试 scenario | 无/见 record | [`record`](../path1-elevator-agent-loop-success/pr-e1-path1_elevator-default-lg_m1_g_signature_gate_20f104e8-d5b14175.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](../path1-elevator-agent-loop-success/pr-e1-path1_elevator-default-lg_m1_g_signature_gate_20f104e8-d5b14175.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](../path1-elevator-agent-loop-success/pr-e1-path1_elevator-default-lg_m1_g_signature_gate_20f104e8-d5b14175.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](../path1-elevator-agent-loop-success/pr-e1-path1_elevator-default-lg_m1_g_signature_gate_20f104e8-d5b14175.agent_loop.json.gz) |
| `SL-7` | 是 | 0 | ✅ | LLM calls=1, tokens=10584 | LLM model review | 无/见 record | [`record`](../path1-elevator-agent-loop-success/pr-e1-path1_elevator-default-lg_m1_g_signature_gate_20f104e8-d5b14175.agent_loop.json.gz) |
| `SC-12` | 否 | - | ✅ | full_pass_all_required_feedback_ok | 写 final verdict | 无/见 record | [`record`](../path1-elevator-agent-loop-success/pr-e1-path1_elevator-default-lg_m1_g_signature_gate_20f104e8-d5b14175.agent_loop.json.gz) |
| `SC-13` | 否 | - | ✅ | trace/control | 写审计 run record | 无/见 record | [`record`](../path1-elevator-agent-loop-success/pr-e1-path1_elevator-default-lg_m1_g_signature_gate_20f104e8-d5b14175.agent_loop.json.gz) |

### 4.1 完整流程日志（stage/control-flow replay ledger）

口径：本节来自 `AgentLoopRunRecord.logs`，与 [`flow_log.json`](./flow_log.json) 一致；用于复现每个 stage 如何进入、得到什么批示、跳转到哪里，以及每次 DSL 产物/候选如何变化。

| # | ts | stage | iter | event | result / jump | DSL evidence |
|---:|---|---|---:|---|---|---|
| 1 | `2026-06-07T21:25:53Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 2 | `2026-06-07T21:25:53Z` | `SC-0` | `-` | `run_start` | {} | <none> |
| 3 | `2026-06-07T21:25:53Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 4 | `2026-06-07T21:25:53Z` | `SL-1` | `-` | `lg_d2_envelope_enter` | {} | <none> |
| 5 | `2026-06-07T21:25:53Z` | `SL-1` | `-` | `stage_enter` | {"reason": "initial_modeling_adapter_available"} | <none> |
| 6 | `2026-06-07T21:26:56Z` | `SL-1` | `-` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 7 | `2026-06-07T21:26:56Z` | `SL-1` | `-` | `stage_result` | {"jump": "SD-2", "ok": true} | candidate_dsl:len=658,hash=sha256:6b02aa0b651f |
| 8 | `2026-06-07T21:26:56Z` | `SL-1` | `-` | `lg_d2_envelope_exit` | {} | <none> |
| 9 | `2026-06-07T21:26:56Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 10 | `2026-06-07T21:26:56Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 11 | `2026-06-07T21:26:56Z` | `<control>` | `0` | `iteration_enter` | {} | current_hash=sha256:6b02aa0b651f657a4b69e59da1e30c6ba2bed44ab0b8f429babbf3112ad83754 |
| 12 | `2026-06-07T21:26:56Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 13 | `2026-06-07T21:26:56Z` | `<control>` | `0` | `iteration_validation_enter` | {} | dsl:len=658,hash=sha256:6b02aa0b651f, current_hash=sha256:6b02aa0b651f657a4b69e59da1e30c6ba2bed44ab0b8f429babbf3112ad83754 |
| 14 | `2026-06-07T21:26:56Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 15 | `2026-06-07T21:26:56Z` | `SD-2` | `0` | `stage_enter` | {"reason": "full_validation_pass"} | <none> |
| 16 | `2026-06-07T21:26:56Z` | `SD-2` | `0` | `stage_result` | {"jump": "SD-3", "ok": true, "status": "StageStatus.OK"} | <none> |
| 17 | `2026-06-07T21:26:56Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 18 | `2026-06-07T21:26:56Z` | `SD-3` | `0` | `stage_enter` | {"reason": "SD-2 ok"} | <none> |
| 19 | `2026-06-07T21:26:56Z` | `SD-3` | `0` | `stage_result` | {"jump": "SD-4", "ok": true, "status": "StageStatus.OK"} | <none> |
| 20 | `2026-06-07T21:26:56Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 21 | `2026-06-07T21:26:56Z` | `SD-4` | `0` | `stage_enter` | {"reason": "SD-3 ok"} | <none> |
| 22 | `2026-06-07T21:26:56Z` | `SD-4` | `0` | `stage_result` | {"jump": "SL-5", "ok": true, "status": "StageStatus.OK"} | <none> |
| 23 | `2026-06-07T21:26:56Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 24 | `2026-06-07T21:26:56Z` | `SL-5` | `0` | `stage_enter` | {"reason": "scenario_set_absent"} | <none> |
| 25 | `2026-06-07T21:26:56Z` | `SL-5` | `0` | `lg_d2_envelope_enter` | {} | <none> |
| 26 | `2026-06-07T21:27:48Z` | `SL-5` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 27 | `2026-06-07T21:27:48Z` | `SL-5` | `0` | `lg_d2_envelope_exit` | {} | <none> |
| 28 | `2026-06-07T21:27:48Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 29 | `2026-06-07T21:27:48Z` | `SD-5A` | `0` | `stage_result` | {"jump": "SC-5F", "ok": true, "status": "StageStatus.OK"} | <none> |
| 30 | `2026-06-07T21:27:48Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 31 | `2026-06-07T21:27:48Z` | `SC-5F` | `0` | `stage_result` | {"jump": "SD-6", "ok": true, "reason": null} | <none> |
| 32 | `2026-06-07T21:27:48Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 33 | `2026-06-07T21:27:48Z` | `SD-6` | `0` | `stage_enter` | {"reason": "scenario_set_ready"} | <none> |
| 34 | `2026-06-07T21:27:48Z` | `SD-6` | `0` | `lg_e2_send_parallel_result` | {} | <none> |
| 35 | `2026-06-07T21:27:48Z` | `SD-6` | `0` | `stage_result` | {"jump": "SL-7", "ok": true, "status": "StageStatus.OK"} | <none> |
| 36 | `2026-06-07T21:27:48Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 37 | `2026-06-07T21:27:48Z` | `SL-7` | `0` | `stage_enter` | {"reason": "SD-6 ok"} | <none> |
| 38 | `2026-06-07T21:27:48Z` | `SL-7` | `0` | `lg_d2_envelope_enter` | {} | <none> |
| 39 | `2026-06-07T21:28:17Z` | `SL-7` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 40 | `2026-06-07T21:28:17Z` | `SL-7` | `0` | `lg_d2_envelope_exit` | {} | <none> |
| 41 | `2026-06-07T21:28:17Z` | `SL-7` | `0` | `stage_result` | {"jump": "SC-12 success", "ok": true, "status": "StageStatus.OK"} | <none> |
| 42 | `2026-06-07T21:28:17Z` | `SL-7` | `0` | `grounding_update_hints_recorded` | {} | <none> |
| 43 | `2026-06-07T21:28:17Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 44 | `2026-06-07T21:28:17Z` | `<control>` | `0` | `iteration_validation_result` | {"jump": "SC-12 success", "selected_feedback": null} | <none> |
| 45 | `2026-06-07T21:28:17Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 46 | `2026-06-07T21:28:17Z` | `SC-12` | `-` | `sc12_verdict` | {"reason": "full_pass_all_required_feedback_ok", "verdict": "success"} | final_dsl:len=658,hash=sha256:6b02aa0b651f |
| 47 | `2026-06-07T21:28:17Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 48 | `2026-06-07T21:28:17Z` | `SC-13` | `-` | `run_end` | {"verdict": "success"} | final_dsl:len=658,hash=sha256:6b02aa0b651f |
| 49 | `` | `<control>` | `-` | `lg_c1_graph_state_readiness` | {} | <none> |
| 50 | `` | `<control>` | `-` | `langgraph_node_trace` | {} | <none> |
| 51 | `` | `<control>` | `-` | `lg_e3_toolnode_wrapper_trace` | {} | <none> |
| 52 | `` | `<control>` | `-` | `lg_e2_send_parallel_trace` | {} | <none> |
| 53 | `` | `<control>` | `-` | `lg_d1_operator_log_artifacts` | {} | <none> |
| 54 | `` | `<control>` | `-` | `lg_c1_graph_state_readiness` | {} | <none> |
| 55 | `` | `<control>` | `-` | `pr_e1_quality_boundary` | {} | <none> |

#### Scenario 逐轮通过矩阵（report §6.1 摘录）

口径：`✅` = 该 scenario 在该轮 SD-6 simulation 通过；`❌` = 该轮失败；`⚪` = 该轮未执行或无该 scenario 结果。

| Scenario | Intent | Iter 1 |
|---|---|---|
| `default_init_f1_and_up_to_f2_then_f3` | default-init dispatches to F1 stopped, then PS2 drives upward to MU2, S2 arrives at F2, PS3 drives upward to MU3, and S3...<truncated 15 chars> | ✅ |
| `f1_direct_to_f3_then_down_to_f1` | explicit-hot-start from F1 checks PS3 selects MU3, arrival at F3 stops, then PS1 selects MD1 and S1 returns to F1. | ✅ |
| `f2_request_down_to_f1` | explicit-hot-start from F2 checks PS1 selects downward MD1 and S1 arrival stops at F1. | ✅ |
| `f3_request_down_to_f2` | explicit-hot-start from F3 checks PS2 selects downward MD2 and S2 arrival stops at F2. | ✅ |
| `immediate_next_destination_after_f2_stop` | explicit-hot-start in MU2 verifies arrival at F2 stops, then the next-cycle PS1 request is immediately checked and start...<truncated 6 chars> | ✅ |
| `reset_from_upward_motion_to_f1` | explicit-hot-start from upward motion MU3 checks Reset forces the controller back to F1 with stop output. | ✅ |
| `reset_from_downward_motion_to_f1` | explicit-hot-start from downward motion MD2 checks Reset forces the controller back to F1 with stop output. | ✅ |
| `reset_from_floor_context_to_f1` | explicit-hot-start from floor F3 checks Reset forces floor contexts as well as motion contexts back to F1 with stop outp...<truncated 3 chars> | ✅ |
| `no_request_holds_floor_state` | explicit-hot-start from F2 checks an empty cycle with no request or arrival event leaves the elevator stopped at the sam...<truncated 8 chars> | ✅ |

#### Repair / blocking feedback 概览（report §7 摘录）

- 本 run 未进入 `SD-8/SL-9/SL-10` repair block；通常表示流程在 repair 前已成功、被 provider/schema 错误中断，或在 pre-repair 阶段直接退出。

### 8. 尝试记录与成本

- `SL-1`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 2611, 'completion_chars': 9326, 'completion_tokens': 3133, 'elapsed_seconds': 62.313252235006075, 'estimated_completion_tokens': 2332, 'estimated_prompt_tokens': 6523, 'estimated_total_tokens': 8855, 'first_chunk_seconds': 15.145741614047438, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 26089, 'prompt_tokens': 6442, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 9575}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 2138, 'completion_chars': 8527, 'completion_tokens': 2660, 'elapsed_seconds': 52.202931402018294, 'estimated_completion_tokens': 2132, 'estimated_prompt_tokens': 11129, 'estimated_total_tokens': 13261, 'first_chunk_seconds': 13.38903169304831, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 44515, 'prompt_tokens': 11437, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 14097}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-7`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1000, 'completion_chars': 4325, 'completion_tokens': 1371, 'elapsed_seconds': 28.38900795398513, 'estimated_completion_tokens': 1082, 'estimated_prompt_tokens': 8675, 'estimated_total_tokens': 9757, 'first_chunk_seconds': 10.097893744998146, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 34698, 'prompt_tokens': 9213, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 10584}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。

### 9. 最终停止状态与后续含义

- 停止状态：verdict=`success`，record_status=`success`。
- 主要原因分类：`success`。
- required stages executed：`12/12`，missing=`<none>`。
- repairs：`0/0` accepted；scenario_history=`1`。
- 配置含义：`recommended baseline candidate`；该结果可用于评估默认入口本身。
- 主结果/蓝本边界：`main_result_eligible` 只表示该 run 非 provider-invalid 且 trace/schema/secret/final-verdict 口径可进入主结果候选；`path2_ref_model_blueprint_eligible=false` 时，模型仍可作为 FE/BVS 或 dispatch-classifier 压力测试证据，但不得称为 Path2 ref-model 主蓝本。
- 样本含义：若出现 `design_or_variable_dynamics`，应重点审查变量是否仅作为 guard/input 常量而没有事件/动作更新；若出现 pre-scenario parse/semantic 失败，则应先优化 pyfcstm grammar adherence。

> 完整 repair 细节、进入修复原因、SD-8 修改建议、SL-9 candidate、before→candidate diff 与 local-check evidence 与 SL-10 审查证据见 `runs/2026-06-08-052552-pr39-agent-loop-langgraph-final-four-case-evidence/path1-elevator-agent-loop-success/report.md` §7。

</details>
