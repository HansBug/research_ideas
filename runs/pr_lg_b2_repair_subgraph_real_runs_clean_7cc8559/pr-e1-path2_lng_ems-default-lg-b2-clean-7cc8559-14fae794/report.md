## path2 / state-transitions-logical-design-for-hybrid-energy-generation-with-renewable-energy-sources-in-lng-ship / default 真实运行结果：Path2 LNG-ship EMS representative NL

### 0. 准确边界与结论

- 运行入口：`method.loop.run_agent_loop(nl, LoopConfig(...))`。
- 是否使用 fake / fixture / hot-start / replay：否；本次使用真实默认入口/显式 PR-E1 探索条件，没有 fake、fixture、hot-start 或 replay。
- final verdict：`success`；record_status：`success`；result_status：`converged`。
- main_result_eligible：`true`。
- Path2 ref-model blueprint eligible：`false`；reason：state_mode_decorative: final DSL is dominated by root-level forced guard reclassification; valid as FE/BVS or dispatch-classifier stress evidence, but not a Path2 ref-model blueprint。
- 一句话结论：`success`；停止原因：full_pass_all_required_feedback_ok。

### 1. 基本信息

| 字段 | 值 |
|---|---|
| Path | `path2` |
| case_id | `state-transitions-logical-design-for-hybrid-energy-generation-with-renewable-energy-sources-in-lng-ship` |
| config_id | `default` |
| 运行入口 | `method.loop.run_agent_loop(nl, LoopConfig(...))` |
| LoopConfig 摘要 | `condition_id=full_staged_v1`, `max_iterations=5`, `llm_max_retries=2`, `scenario_max_retries=2`, `min_sl10_rework_attempts=1`, `model_review_mode=blocking_major_only`, `repair_review_mode=blocking_major_only` |
| Git commit | `7cc8559b58d7e3df3fc5819d45114d325d207120` |
| clean / diff / prompt snapshot | clean=`True`, dirty=`False`, diff_hash=`sha256:2a69ad5797ac568a81bddcef615104303a97261094685f4edd8d4484e889ea09`, prompt_hash=`sha256:29acd3d1171a37b465f2b9278c85877dcbc5703e2d154247154b0c8cb90d6c8e` |
| provider/model 脱敏标识 | mode=`real_env`, model=`gpt-5.5`, real_api=`True` |
| source / paper | source=`project_1_llm_state_machine_modeling/sources/state-transitions-logical-design-for-hybrid-energy-generation-with-renewable-energy-sources-in-lng-ship`, paper=`project_1_llm_state_machine_modeling/sources/state-transitions-logical-design-for-hybrid-energy-generation-with-renewable-energy-sources-in-lng-ship/paper.pdf` |
| 样本筛选理由 | issue #14 / PR-D 代表性 Path2 EFSM，变量、guard、12 个状态和非法状态都明确；但它可能退化为条件分类式 dispatch，因此更适合作为 FE/BVS 压力测试，是否适合作为 Path2 ref-model 蓝本需看最终 DSL 是否具有 state-dependent mode memory。 |
| 变量参与说明 | `PL/Ppv/Pw/SoC/eng*_Pmax` 是环境输入/容量边界，适合暴露 SD-4 对外部输入变量的处理能力。 |
| run_id | `pr-e1-path2_lng_ems-default-lg-b2-clean-7cc8559-14fae794` |
| final verdict/status | verdict=`success`, record=`success`, result=`converged` |
| main_result_eligible | `true` |
| state_mode_decorative_detected | `true` |
| path2_ref_model_blueprint_eligible | `false`；state_mode_decorative: final DSL is dominated by root-level forced guard reclassification; valid as FE/BVS or dispatch-classifier stress evidence, but not a Path2 ref-model blueprint |
| final.fcstm 来源 | `{"accepted": true, "accepted_after_rework": false, "final_dsl_hash": "sha256:3454c23c9fdabd2846510c8225fe02a330f3f8fec051dee98e1de2f7ebab9fc1", "iteration": 3, "last_rejected_candidate": {"candidate_dsl_hash": "sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855", "iteration": 1, "repair_history_index": 1, "rework_instructions": null, "same_as_final": false, "sl10_decision": null}, "matching_repair_history_indices": [3], "repair_history_index": 3, "selected_source_stage": "SD-4", "sl10_decision": "pass", "source_kind": "repair_candidate"}` |
| SC-11 post-accept validation | attempted=`false`；attempts=`0`；success=`0`；failure=`0` |
| FixLog next_action 序列 | `sl9_decision_and_repair, sl10_review, sc11_accept_then_sd2, sl9_decision_and_repair, reject_or_waiver, continue_after_waiver, sl9_decision_and_repair, sl10_review, sc11_accept_then_sd2, sl9_decision_and_repair, sl10_review, sc11_accept_then_sd2` |
| iteration exit_reason 序列 | `candidate_accepted_for_next_full_pass, waiver_continue_revealed_downstream_blocking_feedback, candidate_accepted_for_next_full_pass, candidate_accepted_for_next_full_pass, full_pass_all_required_feedback_ok` |
| token/cost/time | tokens=`{'prompt_tokens': 476895, 'completion_tokens': 46668, 'total_tokens': 523563, 'estimated_prompt_tokens': 528457, 'estimated_completion_tokens': 31990, 'estimated_total_tokens': 560447, 'prompt_chars': 2113812, 'completion_chars': 127941, 'n_calls': 12, 'token_usage_available': True, 'token_usage_unavailable_calls': 0}`, elapsed=`891.898s` |
| run record | [`pr-e1-path2_lng_ems-default-lg-b2-clean-7cc8559-14fae794.agent_loop.json.gz`](./pr-e1-path2_lng_ems-default-lg-b2-clean-7cc8559-14fae794.agent_loop.json.gz) |
| summary/log/final DSL | [`summary.json`](./summary.json), [`checks.json`](./checks.json), [`reproducibility.json`](./reproducibility.json), [`flow_log.json`](./flow_log.json), [`fix_log.json`](./fix_log.json), [`final.fcstm`](./final.fcstm), [`stdout.txt`](./run_logs/stdout.txt), [`stderr.txt`](./run_logs/stderr.txt) |

### 1.1 LangGraph runtime metadata / checkpoint 口径

| 字段 | 值 |
|---|---|
| `graph_runtime_backend` | `langgraph` |
| `graph_runtime_status` | `enabled` |
| `graph_runtime_backend_version` | `pr-langgraph.stategraph.v1` |
| `langgraph_version` | `1.2.4` |
| `langgraph_checkpoint_version` | `4.1.1` |
| `graph_runtime_id` | `langgraph:pr-langgraph.stategraph.v1` |
| `graph_config_hash` | `sha256:f2038a858061b9644334d6ccc5341e2235414617d5779c8634bdc1fb4d64257b` |
| `node_edge_schema_version` | `pr-langgraph.stage-nodes.v1` |
| `checkpoint_backend` | `memory` |
| `checkpoint_backend_type` | `InMemorySaver` |
| `checkpoint_serde` | `pickle` |
| `checkpoint_path_hash` | `sha256:memory` |
| `resumed_from_checkpoint` | `False` |
| `resume_checkpoint_id_hash` | `None` |
| `instrumentation_layer` | `langgraph` |
| `stage_semantics_module` | `method.staged_runtime` |
| `langgraph_node_trace_count` | `91` |
| `langgraph_node_trace_hash` | `sha256:4c76755b683d4b2185c6b7f5f13ede929f42752710a4f3eddf1cd243a5184e3a` |
| `langgraph_compat_ok` | `True` |
| `checkpoint_resume_smoke_scope` | `toy_ledger_langgraph_api_smoke` |
| `real_agent_loop_resume_supported` | `False` |
| `resume_append_only` | `True` |
| `final_trace_delegated_monolithic_runtime` | `False` |
| `final_trace_node_trace_count` | `91` |

- checkpoint 口径：This smoke validates LangGraph interrupt/resume API shape and append-only ledger behavior on a minimal FixLog-like state only. It is not evidence that an interrupted real agent-loop run can be resumed for main-result statistics.
- 注意：`real_agent_loop_resume_supported=false` 时，只能宣称 LangGraph checkpoint API / toy FixLog-like ledger smoke 通过；不能把它写成真实 agent-loop 中断恢复已用于主结果统计。

### 2. 输入 NL（多行原文）

```text
The LNG-ship EMS manages a ship energy system with PVs, WECs, DGs, LNG, batteries, and time-varying ship loads, issuing cut-in and cut-out commands for generating units and loads. It controls power dispatch between generating units and load demand during changing time periods and operating conditions, dynamically switching states to maintain power balance as resources and demands vary. The FSM reads load demand PL, renewable contributions Ppv and Pw, battery state of charge SoC, and engine capacity bounds such as eng3_Pmax, then returns requested generator power, battery discharge or charging power, and spare power. The twelve finite states are selected by logical transition conditions over demand, generation, capacity, and SoC. When Ppv + Pw covers PL, the EMS serves all ship demand from RES and charges batteries while SoC is below 0.95, or treats residual renewable power as spare once SoC is at least 0.95. When Ppv + Pw is below PL, dispatch follows the stated priority: RES first, batteries when SoC is suitable, LNG before diesel units, and DG1/DG2 only as the last priority. Low-SoC branches add explicit charging margins, including Pgmax/5 in an LNG-covered case and Pd1max/10 in later diesel-generator cases. When PL = 0, RES production is sent to battery charging or to spare power according to SoC thresholds. The overload completion state is illegal: if extreme demand exceeds all RES and thermal resources, EMS activates all thermal generating units, covers the lack by battery discharge, and the state shall never occur in practice.
```

### 2.1 输入 NL 中文翻译

```text
LNG 船 EMS 管理一个包含光伏、波浪能、柴油机、LNG、电池和随时间变化船舶负载的船舶能源系统，并向发电单元与负载发出切入/切出命令。它在变化的时段和运行条件下控制发电单元与负载需求之间的功率调度，随着资源和需求变化动态切换状态以保持功率平衡。FSM 读取负载需求 PL、可再生贡献 Ppv 和 Pw、电池荷电状态 SoC，以及 eng3_Pmax 等发动机容量边界，然后返回请求的发电机功率、电池放电或充电功率以及备用功率。十二个有限状态由需求、发电、容量和 SoC 上的逻辑转移条件选择。当 Ppv + Pw 覆盖 PL 时，EMS 用 RES 满足全部船舶需求，并在 SoC 低于 0.95 时给电池充电，或在 SoC 至少为 0.95 时把剩余可再生功率视为备用功率。当 Ppv + Pw 低于 PL 时，调度遵循优先级：RES 优先，SoC 合适时使用电池，LNG 先于柴油机，DG1/DG2 只作为最后优先级。低 SoC 分支加入明确充电裕量，包括 LNG 覆盖场景中的 Pgmax/5，以及后续柴油发电机场景中的 Pd1max/10。当 PL = 0 时，RES 产出根据 SoC 阈值送往电池充电或备用功率。过载完成状态是非法状态：若极端需求超过全部 RES 与热力资源，EMS 会激活全部热发电单元并用电池放电弥补缺口，该状态实践中不应发生。
```

### 3. 最终产出的 FCSTM DSL

```pyfcstm
def float PL = 0.0;
def float Ppv = 0.0;
def float Pw = 0.0;
def float SoC = 0.0;
def float battery_Pmax = 0.0;
def float Plngmax = 0.0;
def float eng3_Pmax = 0.0;
def float Pgmax = 0.0;
def float Pd1max = 0.0;
def float Pd2max = 0.0;
def float requested_generator_power = 0.0;
def float battery_discharge_power = 0.0;
def float battery_charging_power = 0.0;
def float spare_power = 0.0;
def int cut_in_LNG = 0;
def int cut_out_LNG = 0;
def int cut_in_DG1 = 0;
def int cut_out_DG1 = 0;
def int cut_in_DG2 = 0;
def int cut_out_DG2 = 0;
def int cut_in_DG3 = 0;
def int cut_out_DG3 = 0;
def int cut_in_load = 0;
def int cut_out_load = 0;
def int illegal_overload = 0;

state LNGShipEMS {
    ! * -> ZeroLoadCharge : if [PL == 0 && SoC < 0.95];
    ! * -> ZeroLoadSpare : if [PL == 0 && SoC >= 0.95];
    ! * -> RESCoversCharge : if [PL > 0 && Ppv + Pw >= PL && SoC < 0.95];
    ! * -> RESCoversSpare : if [PL > 0 && Ppv + Pw >= PL && SoC >= 0.95];
    ! * -> BatteryAssist : if [PL > 0 && Ppv + Pw < PL && SoC > 0.20 && PL - Ppv - Pw <= battery_Pmax];
    ! * -> LNGDispatch : if [PL > 0 && Ppv + Pw < PL && SoC > 0.20 && PL - Ppv - Pw > battery_Pmax && PL - Ppv - Pw <= Plngmax];
    ! * -> LNGChargeMargin : if [PL > 0 && Ppv + Pw < PL && SoC <= 0.20 && PL - Ppv - Pw + Pgmax / 5 <= Plngmax];
    ! * -> LNGDG3Dispatch : if [PL > 0 && Ppv + Pw < PL && SoC > 0.20 && PL - Ppv - Pw > Plngmax && PL - Ppv - Pw <= Plngmax + eng3_Pmax];
    ! * -> LNGDG3ChargeMargin : if [PL > 0 && Ppv + Pw < PL && SoC <= 0.20 && PL - Ppv - Pw + Pd1max / 10 > Plngmax && PL - Ppv - Pw + Pd1max / 10 <= Plngmax + eng3_Pmax];
    ! * -> AddDG1LastPriority : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > Plngmax + eng3_Pmax && PL - Ppv - Pw <= Plngmax + eng3_Pmax + Pd1max];
    ! * -> AddDG2LastPriority : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > Plngmax + eng3_Pmax + Pd1max && PL - Ppv - Pw <= Plngmax + eng3_Pmax + Pd1max + Pd2max];
    ! * -> ExtremeOverloadBatteryLack : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > Plngmax + eng3_Pmax + Pd1max + Pd2max];

    [*] -> InitialDispatchSelect;

    pseudo state InitialDispatchSelect;

    state RESCoversCharge {
        enter {
            requested_generator_power = 0.0;
            battery_discharge_power = 0.0;
            battery_charging_power = Ppv + Pw - PL;
            spare_power = 0.0;
            cut_in_LNG = 0;
            cut_out_LNG = 1;
            cut_in_DG1 = 0;
            cut_out_DG1 = 1;
            cut_in_DG2 = 0;
            cut_out_DG2 = 1;
            cut_in_DG3 = 0;
            cut_out_DG3 = 1;
            cut_in_load = 1;
            cut_out_load = 0;
            illegal_overload = 0;
        }
    }

    state RESCoversSpare {
        enter {
            requested_generator_power = 0.0;
            battery_discharge_power = 0.0;
            battery_charging_power = 0.0;
            spare_power = Ppv + Pw - PL;
            cut_in_LNG = 0;
            cut_out_LNG = 1;
            cut_in_DG1 = 0;
            cut_out_DG1 = 1;
            cut_in_DG2 = 0;
            cut_out_DG2 = 1;
            cut_in_DG3 = 0;
            cut_out_DG3 = 1;
            cut_in_load = 1;
            cut_out_load = 0;
            illegal_overload = 0;
        }
    }

    state ZeroLoadCharge {
        enter {
            requested_generator_power = 0.0;
            battery_discharge_power = 0.0;
            battery_charging_power = Ppv + Pw;
            spare_power = 0.0;
            cut_in_LNG = 0;
            cut_out_LNG = 1;
            cut_in_DG1 = 0;
            cut_out_DG1 = 1;
            cut_in_DG2 = 0;
            cut_out_DG2 = 1;
            cut_in_DG3 = 0;
            cut_out_DG3 = 1;
            cut_in_load = 0;
            cut_out_load = 1;
            illegal_overload = 0;
        }
    }

    state ZeroLoadSpare {
        enter {
            requested_generator_power = 0.0;
            battery_discharge_power = 0.0;
            battery_charging_power = 0.0;
            spare_power = Ppv + Pw;
            cut_in_LNG = 0;
            cut_out_LNG = 1;
            cut_in_DG1 = 0;
            cut_out_DG1 = 1;
            cut_in_DG2 = 0;
            cut_out_DG2 = 1;
            cut_in_DG3 = 0;
            cut_out_DG3 = 1;
            cut_in_load = 0;
            cut_out_load = 1;
            illegal_overload = 0;
        }
    }

    state BatteryAssist {
        enter {
            requested_generator_power = 0.0;
            battery_discharge_power = PL - Ppv - Pw;
            battery_charging_power = 0.0;
            spare_power = 0.0;
            cut_in_LNG = 0;
            cut_out_LNG = 1;
            cut_in_DG1 = 0;
            cut_out_DG1 = 1;
            cut_in_DG2 = 0;
            cut_out_DG2 = 1;
            cut_in_DG3 = 0;
            cut_out_DG3 = 1;
            cut_in_load = 1;
            cut_out_load = 0;
            illegal_overload = 0;
        }
    }

    state LNGDispatch {
        enter {
            requested_generator_power = PL - Ppv - Pw;
            battery_discharge_power = 0.0;
            battery_charging_power = 0.0;
            spare_power = 0.0;
            cut_in_LNG = 1;
            cut_out_LNG = 0;
            cut_in_DG1 = 0;
            cut_out_DG1 = 1;
            cut_in_DG2 = 0;
            cut_out_DG2 = 1;
            cut_in_DG3 = 0;
            cut_out_DG3 = 1;
            cut_in_load = 1;
            cut_out_load = 0;
            illegal_overload = 0;
        }
    }

    state LNGChargeMargin {
        enter {
            requested_generator_power = PL - Ppv - Pw + Pgmax / 5;
            battery_discharge_power = 0.0;
            battery_charging_power = Pgmax / 5;
            spare_power = 0.0;
            cut_in_LNG = 1;
            cut_out_LNG = 0;
            cut_in_DG1 = 0;
            cut_out_DG1 = 1;
            cut_in_DG2 = 0;
            cut_out_DG2 = 1;
            cut_in_DG3 = 0;
            cut_out_DG3 = 1;
            cut_in_load = 1;
            cut_out_load = 0;
            illegal_overload = 0;
        }
    }

    state LNGDG3Dispatch {
        enter {
            requested_generator_power = PL - Ppv - Pw;
            battery_discharge_power = 0.0;
            battery_charging_power = 0.0;
            spare_power = 0.0;
            cut_in_LNG = 1;
            cut_out_LNG = 0;
            cut_in_DG1 = 0;
            cut_out_DG1 = 1;
            cut_in_DG2 = 0;
            cut_out_DG2 = 1;
            cut_in_DG3 = 1;
            cut_out_DG3 = 0;
            cut_in_load = 1;
            cut_out_load = 0;
            illegal_overload = 0;
        }
    }

    state LNGDG3ChargeMargin {
        enter {
            requested_generator_power = PL - Ppv - Pw + Pd1max / 10;
            battery_discharge_power = 0.0;
            battery_charging_power = Pd1max / 10;
            spare_power = 0.0;
            cut_in_LNG = 1;
            cut_out_LNG = 0;
            cut_in_DG1 = 0;
            cut_out_DG1 = 1;
            cut_in_DG2 = 0;
            cut_out_DG2 = 1;
            cut_in_DG3 = 1;
            cut_out_DG3 = 0;
            cut_in_load = 1;
            cut_out_load = 0;
            illegal_overload = 0;
        }
    }

    state AddDG1LastPriority {
        enter {
            requested_generator_power = PL - Ppv - Pw;
            battery_discharge_power = 0.0;
            battery_charging_power = 0.0;
            spare_power = 0.0;
            cut_in_LNG = 1;
            cut_out_LNG = 0;
            cut_in_DG1 = 1;
            cut_out_DG1 = 0;
            cut_in_DG2 = 0;
            cut_out_DG2 = 1;
            cut_in_DG3 = 1;
            cut_out_DG3 = 0;
            cut_in_load = 1;
            cut_out_load = 0;
            illegal_overload = 0;
        }
    }

    state AddDG2LastPriority {
        enter {
            requested_generator_power = PL - Ppv - Pw;
            battery_discharge_power = 0.0;
            battery_charging_power = 0.0;
            spare_power = 0.0;
            cut_in_LNG = 1;
            cut_out_LNG = 0;
            cut_in_DG1 = 1;
            cut_out_DG1 = 0;
            cut_in_DG2 = 1;
            cut_out_DG2 = 0;
            cut_in_DG3 = 1;
            cut_out_DG3 = 0;
            cut_in_load = 1;
            cut_out_load = 0;
            illegal_overload = 0;
        }
    }

    state ExtremeOverloadBatteryLack {
        enter {
            requested_generator_power = Plngmax + eng3_Pmax + Pd1max + Pd2max;
            battery_discharge_power = PL - Ppv - Pw - Plngmax - eng3_Pmax - Pd1max - Pd2max;
            battery_charging_power = 0.0;
            spare_power = 0.0;
            cut_in_LNG = 1;
            cut_out_LNG = 0;
            cut_in_DG1 = 1;
            cut_out_DG1 = 0;
            cut_in_DG2 = 1;
            cut_out_DG2 = 0;
            cut_in_DG3 = 1;
            cut_out_DG3 = 0;
            cut_in_load = 1;
            cut_out_load = 0;
            illegal_overload = 1;
        }
    }
}
```

### 4. 全流程真实摘要表

| Stage | 是否 LLM | iteration | 结果 | 获取的信息 / 反馈 | 本阶段做了什么 | DSL 修改 | artifact/log |
|---|---:|---:|---:|---|---|---|---|
| `SC-0` | 否 | - | ✅ | trace/control | 初始化 run state | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b2-clean-7cc8559-14fae794.agent_loop.json.gz) |
| `SL-1` | 是 | - | ✅ | LLM calls=1, tokens=14661 | 生成初始 DSL 与 grounding seeds | initial len=8904 | [`record`](./pr-e1-path2_lng_ems-default-lg-b2-clean-7cc8559-14fae794.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b2-clean-7cc8559-14fae794.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b2-clean-7cc8559-14fae794.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ⚠️ | blocking=100, advisory=86, info=0; blocking=99, advisory=86, info=0; blocking=0, advisory=185, info=0; blocking=0, advisory=185, info=0; blocking=28, advisory=206, info=0; blocking | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b2-clean-7cc8559-14fae794.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b2-clean-7cc8559-14fae794.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=4, tokens=229627 | LLM per-request accept/reject + repair | candidate len=8827,0,10454,8874 | [`record`](./pr-e1-path2_lng_ems-default-lg-b2-clean-7cc8559-14fae794.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=3, tokens=144254 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b2-clean-7cc8559-14fae794.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b2-clean-7cc8559-14fae794.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b2-clean-7cc8559-14fae794.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b2-clean-7cc8559-14fae794.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ⚠️ | blocking=100, advisory=86, info=0; blocking=99, advisory=86, info=0; blocking=0, advisory=185, info=0; blocking=0, advisory=185, info=0; blocking=28, advisory=206, info=0; blocking | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b2-clean-7cc8559-14fae794.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b2-clean-7cc8559-14fae794.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=4, tokens=229627 | LLM per-request accept/reject + repair | candidate len=8827,0,10454,8874 | [`record`](./pr-e1-path2_lng_ems-default-lg-b2-clean-7cc8559-14fae794.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ⚠️ | blocking=100, advisory=86, info=0; blocking=99, advisory=86, info=0; blocking=0, advisory=185, info=0; blocking=0, advisory=185, info=0; blocking=28, advisory=206, info=0; blocking | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b2-clean-7cc8559-14fae794.agent_loop.json.gz) |
| `SL-5` | 是 | 1 | ✅ | LLM calls=3, tokens=73728 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b2-clean-7cc8559-14fae794.agent_loop.json.gz) |
| `SD-5A` | 否 | 1 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b2-clean-7cc8559-14fae794.agent_loop.json.gz) |
| `SL-5` | 是 | 1 | ✅ | LLM calls=3, tokens=73728 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b2-clean-7cc8559-14fae794.agent_loop.json.gz) |
| `SD-5A` | 否 | 1 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b2-clean-7cc8559-14fae794.agent_loop.json.gz) |
| `SC-5F` | 否 | 1 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b2-clean-7cc8559-14fae794.agent_loop.json.gz) |
| `SD-6` | 否 | 1 | ⚠️ | ok=False, diag=0; ok=False, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b2-clean-7cc8559-14fae794.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b2-clean-7cc8559-14fae794.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b2-clean-7cc8559-14fae794.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=100, advisory=86, info=0; blocking=99, advisory=86, info=0; blocking=0, advisory=185, info=0; blocking=0, advisory=185, info=0; blocking=28, advisory=206, info=0; blocking | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b2-clean-7cc8559-14fae794.agent_loop.json.gz) |
| `SD-5A` | 否 | 1 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b2-clean-7cc8559-14fae794.agent_loop.json.gz) |
| `SC-5F` | 否 | 1 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b2-clean-7cc8559-14fae794.agent_loop.json.gz) |
| `SD-6` | 否 | 1 | ⚠️ | ok=False, diag=0; ok=False, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b2-clean-7cc8559-14fae794.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b2-clean-7cc8559-14fae794.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=4, tokens=229627 | LLM per-request accept/reject + repair | candidate len=8827,0,10454,8874 | [`record`](./pr-e1-path2_lng_ems-default-lg-b2-clean-7cc8559-14fae794.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=3, tokens=144254 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b2-clean-7cc8559-14fae794.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b2-clean-7cc8559-14fae794.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b2-clean-7cc8559-14fae794.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b2-clean-7cc8559-14fae794.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ⚠️ | blocking=100, advisory=86, info=0; blocking=99, advisory=86, info=0; blocking=0, advisory=185, info=0; blocking=0, advisory=185, info=0; blocking=28, advisory=206, info=0; blocking | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b2-clean-7cc8559-14fae794.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b2-clean-7cc8559-14fae794.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=4, tokens=229627 | LLM per-request accept/reject + repair | candidate len=8827,0,10454,8874 | [`record`](./pr-e1-path2_lng_ems-default-lg-b2-clean-7cc8559-14fae794.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=3, tokens=144254 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b2-clean-7cc8559-14fae794.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b2-clean-7cc8559-14fae794.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b2-clean-7cc8559-14fae794.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b2-clean-7cc8559-14fae794.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=100, advisory=86, info=0; blocking=99, advisory=86, info=0; blocking=0, advisory=185, info=0; blocking=0, advisory=185, info=0; blocking=28, advisory=206, info=0; blocking | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b2-clean-7cc8559-14fae794.agent_loop.json.gz) |
| `SD-5A` | 否 | 1 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b2-clean-7cc8559-14fae794.agent_loop.json.gz) |
| `SL-5` | 是 | 1 | ✅ | LLM calls=3, tokens=73728 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b2-clean-7cc8559-14fae794.agent_loop.json.gz) |
| `SD-5A` | 否 | 1 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b2-clean-7cc8559-14fae794.agent_loop.json.gz) |
| `SC-5F` | 否 | 1 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b2-clean-7cc8559-14fae794.agent_loop.json.gz) |
| `SD-6` | 否 | 1 | ✅ | ok=False, diag=0; ok=False, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b2-clean-7cc8559-14fae794.agent_loop.json.gz) |
| `SL-7` | 是 | 4 | ✅ | LLM calls=1, tokens=61293 | LLM model review | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b2-clean-7cc8559-14fae794.agent_loop.json.gz) |
| `SC-12` | 否 | - | ✅ | full_pass_all_required_feedback_ok | 写 final verdict | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b2-clean-7cc8559-14fae794.agent_loop.json.gz) |
| `SC-13` | 否 | - | ✅ | trace/control | 写审计 run record | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b2-clean-7cc8559-14fae794.agent_loop.json.gz) |

### 4.1 完整流程日志（stage/control-flow replay ledger）

口径：本节来自 `AgentLoopRunRecord.logs`，与 [`flow_log.json`](./flow_log.json) 一致；用于复现每个 stage 如何进入、得到什么批示、跳转到哪里，以及每次 DSL 产物/候选如何变化。

| # | ts | stage | iter | event | result / jump | DSL evidence |
|---:|---|---|---:|---|---|---|
| 1 | `2026-06-05T17:34:06Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 2 | `2026-06-05T17:34:06Z` | `SC-0` | `-` | `run_start` | {} | <none> |
| 3 | `2026-06-05T17:34:06Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 4 | `2026-06-05T17:34:06Z` | `SL-1` | `-` | `stage_enter` | {"reason": "initial_modeling_adapter_available"} | <none> |
| 5 | `2026-06-05T17:36:35Z` | `SL-1` | `-` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 6 | `2026-06-05T17:36:35Z` | `SL-1` | `-` | `stage_result` | {"jump": "SD-2", "ok": true} | candidate_dsl:len=8904,hash=sha256:99fe6082d065 |
| 7 | `2026-06-05T17:36:35Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 8 | `2026-06-05T17:36:35Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 9 | `2026-06-05T17:36:35Z` | `<control>` | `0` | `iteration_enter` | {} | current_hash=sha256:99fe6082d0658600915be6b8f6a84fe180769746e3be3d660af3442a02f12228 |
| 10 | `2026-06-05T17:36:35Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 11 | `2026-06-05T17:36:35Z` | `<control>` | `0` | `iteration_validation_enter` | {} | dsl:len=8904,hash=sha256:99fe6082d065, current_hash=sha256:99fe6082d0658600915be6b8f6a84fe180769746e3be3d660af3442a02f12228 |
| 12 | `2026-06-05T17:36:35Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 13 | `2026-06-05T17:36:35Z` | `SD-2` | `0` | `stage_enter` | {"reason": "full_validation_pass"} | <none> |
| 14 | `2026-06-05T17:36:35Z` | `SD-2` | `0` | `stage_result` | {"jump": "SD-3", "ok": true, "status": "StageStatus.OK"} | <none> |
| 15 | `2026-06-05T17:36:35Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 16 | `2026-06-05T17:36:35Z` | `SD-3` | `0` | `stage_enter` | {"reason": "SD-2 ok"} | <none> |
| 17 | `2026-06-05T17:36:36Z` | `SD-3` | `0` | `stage_result` | {"jump": "SD-4", "ok": true, "status": "StageStatus.OK"} | <none> |
| 18 | `2026-06-05T17:36:36Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 19 | `2026-06-05T17:36:36Z` | `SD-4` | `0` | `stage_enter` | {"reason": "SD-3 ok"} | <none> |
| 20 | `2026-06-05T17:36:36Z` | `SD-4` | `0` | `stage_result` | {"jump": "SD-8", "ok": false, "status": "StageStatus.FAIL"} | <none> |
| 21 | `2026-06-05T17:36:36Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 22 | `2026-06-05T17:36:36Z` | `<control>` | `0` | `iteration_validation_result` | {"jump": "SD-8 repair", "selected_feedback": {"blocking": true, "blocking_instance_keys": ["W_UNWRITTEN_READ_VAR:var_name=SoC_low_limit", "W_UNWRITTEN_READ_VAR:var_name=battery_Pmax", "W_UNWRITTEN_READ_VAR:var_name=Plngmax", "W_UNWRITTEN_READ_VAR:var_name=Pd2max", "W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.RESCoversCharge:to_path=LNGShipEMS.BatteryAssist", "W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.RESCover...<truncated 18411 chars> | <none> |
| 23 | `2026-06-05T17:36:36Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 24 | `2026-06-05T17:36:36Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 25 | `2026-06-05T17:36:36Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 26 | `2026-06-05T17:36:36Z` | `SD-8` | `0` | `repair_path_enter` | {"jump": "SD-8", "selected_feedback": {"blocking": true, "blocking_instance_keys": ["W_UNWRITTEN_READ_VAR:var_name=SoC_low_limit", "W_UNWRITTEN_READ_VAR:var_name=battery_Pmax", "W_UNWRITTEN_READ_VAR:var_name=Plngmax", "W_UNWRITTEN_READ_VAR:var_name=Pd2max", "W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.RESCoversCharge:to_path=LNGShipEMS.BatteryAssist", "W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.RESCoversCharge...<truncated 166777 chars> | current_dsl:len=8904,hash=sha256:99fe6082d065 |
| 27 | `2026-06-05T17:36:36Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 28 | `2026-06-05T17:36:36Z` | `SD-8` | `0` | `stage_result` | {"jump": "SL-9", "ok": true, "status": "StageStatus.OK"} | <none> |
| 29 | `2026-06-05T17:36:36Z` | `SD-8` | `0` | `fix_request_batch` | {"request_count": 12} | <none> |
| 30 | `2026-06-05T17:36:36Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 31 | `2026-06-05T17:36:36Z` | `SL-9` | `0` | `stage_enter` | {"reason": "fix_requests_ready"} | old_dsl:len=8904,hash=sha256:99fe6082d065 |
| 32 | `2026-06-05T17:38:13Z` | `SL-9` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 33 | `2026-06-05T17:38:13Z` | `SL-9` | `0` | `stage_result` | {"accepted_request_ids": ["fixreq-0-sd4-0-b481b95286"], "jump": "SL-10", "ok": true, "rejected_request_ids": ["fixreq-0-sd4-1-e891b4d9d0", "fixreq-0-sd4-2-313f683f70", "fixreq-0-sd4-3-4f0f4171fd", "fixreq-0-sd4-4-b5b2f5d5ad", "fixreq-0-sd4-5-777856a1ea", "fixreq-0-sd4-6-3bf5386372", "fixreq-0-sd4-7-b77957cc50", "fixreq-0-sd4-8-127bbad309", "fixreq-0-sd4-9-c76ffc05a8", "fixreq-0-sd4-10-c3fd85bfda", "fixreq-0-sd4-11-7c...<truncated 11 chars> | candidate_dsl:len=8827,hash=sha256:e4cf5afd22c7 |
| 34 | `2026-06-05T17:38:13Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 35 | `2026-06-05T17:38:13Z` | `SD-10` | `0` | `stage_result` | {"jump": "SL-10", "ok": false, "status": "StageStatus.FAIL"} | <none> |
| 36 | `2026-06-05T17:38:13Z` | `SL-10` | `0` | `stage_enter` | {"reason": "candidate_dsl_and_local_evidence_ready"} | candidate_hash=sha256:e4cf5afd22c71c13ec6bf27c1372b7fbca62216ddb49195ac0b757d4fe3ed1b9 |
| 37 | `2026-06-05T17:38:35Z` | `SL-10` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 38 | `2026-06-05T17:38:35Z` | `SL-10` | `0` | `stage_result` | {"decision": "pass", "jump": "SC-11", "ok": true} | <none> |
| 39 | `2026-06-05T17:38:35Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 40 | `2026-06-05T17:38:35Z` | `SC-11` | `0` | `stage_result` | {"jump": "SD-2 next iteration", "ok": true, "reason": "SL-10 accepted candidate; next iteration must restart at SD-2"} | candidate_dsl:len=8827,hash=sha256:e4cf5afd22c7 |
| 41 | `2026-06-05T17:38:35Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 42 | `2026-06-05T17:38:35Z` | `<control>` | `0` | `iteration_repair_result` | {"accepted": true, "jump": "SD-2 next iteration"} | current_hash=sha256:e4cf5afd22c71c13ec6bf27c1372b7fbca62216ddb49195ac0b757d4fe3ed1b9 |
| 43 | `2026-06-05T17:38:35Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 44 | `2026-06-05T17:38:35Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 45 | `2026-06-05T17:38:35Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 46 | `2026-06-05T17:38:35Z` | `<control>` | `1` | `iteration_enter` | {} | current_hash=sha256:e4cf5afd22c71c13ec6bf27c1372b7fbca62216ddb49195ac0b757d4fe3ed1b9 |
| 47 | `2026-06-05T17:38:35Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 48 | `2026-06-05T17:38:35Z` | `<control>` | `1` | `iteration_validation_enter` | {} | dsl:len=8827,hash=sha256:e4cf5afd22c7, current_hash=sha256:e4cf5afd22c71c13ec6bf27c1372b7fbca62216ddb49195ac0b757d4fe3ed1b9 |
| 49 | `2026-06-05T17:38:35Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 50 | `2026-06-05T17:38:35Z` | `SD-2` | `1` | `stage_enter` | {"reason": "full_validation_pass"} | <none> |
| 51 | `2026-06-05T17:38:35Z` | `SD-2` | `1` | `stage_result` | {"jump": "SD-3", "ok": true, "status": "StageStatus.OK"} | <none> |
| 52 | `2026-06-05T17:38:35Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 53 | `2026-06-05T17:38:35Z` | `SD-3` | `1` | `stage_enter` | {"reason": "SD-2 ok"} | <none> |
| 54 | `2026-06-05T17:38:35Z` | `SD-3` | `1` | `stage_result` | {"jump": "SD-4", "ok": true, "status": "StageStatus.OK"} | <none> |
| 55 | `2026-06-05T17:38:35Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 56 | `2026-06-05T17:38:35Z` | `SD-4` | `1` | `stage_enter` | {"reason": "SD-3 ok"} | <none> |
| 57 | `2026-06-05T17:38:35Z` | `SD-4` | `1` | `stage_result` | {"jump": "SD-8", "ok": false, "status": "StageStatus.FAIL"} | <none> |
| 58 | `2026-06-05T17:38:35Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 59 | `2026-06-05T17:38:35Z` | `<control>` | `1` | `iteration_validation_result` | {"jump": "SD-8 repair", "selected_feedback": {"blocking": true, "blocking_instance_keys": ["W_UNWRITTEN_READ_VAR:var_name=battery_Pmax", "W_UNWRITTEN_READ_VAR:var_name=Plngmax", "W_UNWRITTEN_READ_VAR:var_name=Pd2max", "W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.RESCoversCharge:to_path=LNGShipEMS.BatteryAssist", "W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.RESCoversCharge:to_path=LNGShipEMS.LNGDispatch", "W_GUA...<truncated 18321 chars> | <none> |
| 60 | `2026-06-05T17:38:35Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 61 | `2026-06-05T17:38:35Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 62 | `2026-06-05T17:38:35Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 63 | `2026-06-05T17:38:35Z` | `SD-8` | `1` | `repair_path_enter` | {"jump": "SD-8", "selected_feedback": {"blocking": true, "blocking_instance_keys": ["W_UNWRITTEN_READ_VAR:var_name=battery_Pmax", "W_UNWRITTEN_READ_VAR:var_name=Plngmax", "W_UNWRITTEN_READ_VAR:var_name=Pd2max", "W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.RESCoversCharge:to_path=LNGShipEMS.BatteryAssist", "W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.RESCoversCharge:to_path=LNGShipEMS.LNGDispatch", "W_GUARD_VARS...<truncated 158679 chars> | current_dsl:len=8827,hash=sha256:e4cf5afd22c7 |
| 64 | `2026-06-05T17:38:35Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 65 | `2026-06-05T17:38:35Z` | `SD-8` | `1` | `stage_result` | {"jump": "SL-9", "ok": true, "status": "StageStatus.OK"} | <none> |
| 66 | `2026-06-05T17:38:35Z` | `SD-8` | `1` | `fix_request_batch` | {"request_count": 12} | <none> |
| 67 | `2026-06-05T17:38:35Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 68 | `2026-06-05T17:38:35Z` | `SL-9` | `1` | `stage_enter` | {"reason": "fix_requests_ready"} | old_dsl:len=8827,hash=sha256:e4cf5afd22c7 |
| 69 | `2026-06-05T17:39:10Z` | `SL-9` | `1` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 70 | `2026-06-05T17:39:10Z` | `SL-9` | `1` | `stage_result` | {"accepted_request_ids": [], "jump": "waiver_continue_or_exit", "ok": false, "rejected_request_ids": ["fixreq-1-sd4-0-75b9296ee2", "fixreq-1-sd4-1-1d359b61ba", "fixreq-1-sd4-2-87428d820c", "fixreq-1-sd4-3-0dca8d0e29", "fixreq-1-sd4-4-9e0c92746d", "fixreq-1-sd4-5-bfdc977592", "fixreq-1-sd4-6-3fedd329d1", "fixreq-1-sd4-7-4453eac848", "fixreq-1-sd4-8-a282748588", "fixreq-1-sd4-9-b735f5be23", "fixreq-1-sd4-10-619e4b70df"...<truncated 32 chars> | <none> |
| 71 | `2026-06-05T17:39:10Z` | `SL-9` | `1` | `sl9_all_rejected_waiver_continue` | {"jump": "continue_after_current_stage"} | <none> |
| 72 | `2026-06-05T17:39:10Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 73 | `2026-06-05T17:39:10Z` | `<control>` | `1` | `iteration_repair_result` | {"accepted": false, "jump": "waiver_continue"} | current_hash=sha256:e4cf5afd22c71c13ec6bf27c1372b7fbca62216ddb49195ac0b757d4fe3ed1b9 |
| 74 | `2026-06-05T17:39:10Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 75 | `2026-06-05T17:39:10Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 76 | `2026-06-05T17:39:10Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 77 | `2026-06-05T17:39:10Z` | `<control>` | `1` | `iteration_validation_enter` | {} | dsl:len=8827,hash=sha256:e4cf5afd22c7, current_hash=sha256:e4cf5afd22c71c13ec6bf27c1372b7fbca62216ddb49195ac0b757d4fe3ed1b9 |
| 78 | `2026-06-05T17:39:10Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 79 | `2026-06-05T17:39:10Z` | `<control>` | `1` | `waiver_continue_validation_enter` | {"reason": "SL-9 rejected/waived non-hard SD-4 requests; continue downstream without SC-11 DSL edit"} | current_dsl:len=8827,hash=sha256:e4cf5afd22c7 |
| 80 | `2026-06-05T17:39:10Z` | `SD-4` | `1` | `stage_result` | {"jump": "SL-5", "ok": true, "reason": "waiver_continue_design_items_marked_non_blocking_for_downstream_validation", "status": "StageStatus.ADVISORY"} | <none> |
- ……另有 `137` 条流程日志见 [`flow_log.json`](./flow_log.json) / run record。

### 5. Iteration / repair / review 摘要

| Iter | selected feedback | repair? | FixRequestBatch | SL-9 | local checks | SL-10 | 回到 SD-2? | verdict/备注 |
|---:|---|---|---|---|---|---|---|---|
| 0 | `SD-4` | yes | fixbatch-0-sha256-874b3e13f39 / n=12 | accept=1, reject=11, waiver=11 | ok=False, target=False, regression=False, drift=none, local_stage=SD-10, reason=design_target_unresolved | decision=pass, ok=True, target=True, regression=False, drift=none, rework=<none> | yes | candidate_accepted_for_next_full_pass |
| 1 | `SD-4` | yes | fixbatch-1-sha256-a1a5d6e0aa8 / n=12 | accept=0, reject=12, waiver=12 | <none> | decision=None, ok=True, target=True, regression=False, drift=minor, rework=<none> | no | waiver_continue_revealed_downstream_blocking_feedback |
| 2 | `SD-6` | yes | fixbatch-2-sha256-83f4e7b3696 / n=1 | accept=1, reject=0, waiver=0 | ok=False, target=False, regression=False, drift=major, local_stage=SD-10, reason=new_blocking_design_diagnostic; forced_transition_count_drift | decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none> | yes | candidate_accepted_for_next_full_pass |
| 3 | `SD-4` | yes | fixbatch-3-sha256-e7904670632 / n=12 | accept=4, reject=8, waiver=8 | ok=True, target=True, regression=False, drift=none, local_stage=SD-10, reason= | decision=pass, ok=True, target=True, regression=False, drift=none, rework=<none> | yes | candidate_accepted_for_next_full_pass |
| 4 | `<none>` | no | <none> | <none> | <none> | <none> | no | full_pass_all_required_feedback_ok |

### 6. Scenario 明细与逐轮通过情况

#### 6.1 Scenario pass/fail by iteration

口径：`✅` = 该 scenario 在该轮 SD-6 simulation 通过；`❌` = 该轮失败；`⚪` = 该轮未执行或无该 scenario 结果。

| Scenario | Intent | Iter 2 | Iter 3 | Iter 5 |
|---|---|---|---|---|
| `default_init_zero_load_charge` | default-init: with PL=0 and SoC below 0.95, the EMS should classify zero load RES into battery charging and cut out ship...<truncated 6 chars> | ❌ | ❌ | ✅ |
| `zero_load_soc_threshold_spare` | explicit-hot-start: at PL=0 and SoC exactly 0.95, RES production should become spare power rather than battery charge. | ✅ | ✅ | ✅ |
| `res_covers_charge_below_soc_threshold` | explicit-hot-start: with positive load covered by RES and SoC below 0.95, demand is served by RES and residual renewable...<truncated 27 chars> | ✅ | ✅ | ✅ |
| `res_covers_spare_at_soc_threshold` | explicit-hot-start: with positive load covered by RES and SoC exactly 0.95, residual renewable power should be reported ...<truncated 9 chars> | ✅ | ✅ | ✅ |
| `battery_assist_at_battery_capacity_boundary` | explicit-hot-start: when RES is short, SoC is suitable, and the deficit exactly equals battery_Pmax, batteries should co...<truncated 38 chars> | ✅ | ✅ | ✅ |
| `lng_dispatch_at_lng_capacity_boundary` | explicit-hot-start: when battery alone is insufficient and the deficit exactly equals LNG capacity, LNG should be cut in...<truncated 21 chars> | ✅ | ✅ | ✅ |
| `lng_charge_margin_low_soc_boundary` | explicit-hot-start: at low SoC exactly 0.20, the LNG-covered branch should add the Pgmax/5 charging margin. | ✅ | ✅ | ✅ |
| `lng_dg3_dispatch_at_eng3_boundary` | explicit-hot-start: when LNG alone is insufficient and the deficit exactly fits LNG plus DG3 capacity, LNG and DG3 shoul...<truncated 25 chars> | ✅ | ✅ | ✅ |
| `lng_dg3_charge_margin_pd1_margin` | explicit-hot-start: in a later low-SoC diesel-generator case, the Pd1max/10 charging margin should be added while using ...<truncated 12 chars> | ✅ | ✅ | ✅ |
| `add_dg1_last_priority_boundary` | explicit-hot-start: when the deficit exceeds LNG plus DG3 but exactly fits after adding DG1, DG1 is cut in and DG2 remai...<truncated 11 chars> | ✅ | ✅ | ✅ |
| `add_dg2_last_priority_boundary` | explicit-hot-start: when the deficit exceeds LNG plus DG3 plus DG1 but exactly fits after adding DG2, both DG1 and DG2 a...<truncated 33 chars> | ✅ | ✅ | ✅ |
| `extreme_overload_all_thermal_and_battery_lack` | explicit-hot-start: for demand exceeding all RES and thermal resources, all thermal units are activated and the remainin...<truncated 69 chars> | ✅ | ✅ | ✅ |
| `forced_reclass_zero_load_charge_from_overload` |  | ✅ | ✅ | ✅ |
| `forced_reclass_lng_dispatch_from_res_spare` |  | ✅ | ✅ | ✅ |

#### 6.2 Scenario definitions

<details><summary>`default_init_zero_load_charge` — default-init: with PL=0 and SoC below 0.95, the EMS should classify zero load RES into battery charging and cut out ship load.</summary>

| Field | Value |
|---|---|
| description | default-init: with PL=0 and SoC below 0.95, the EMS should classify zero load RES into battery charging and cut out ship load. |
| initial_state | `<default-init>` |
| initial_vars | `{"PL": 0.0, "Ppv": 10.0, "Pw": 5.0, "SoC": 0.5}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `zero_load_low_soc_charges_battery` | `0` | `[]` | `LNGShipEMS.ZeroLoadCharge` | `{"battery_charging_power": 15.0, "battery_discharge_power": 0.0, "cut_in_LNG": 0, "cut_in_load": 0, "cut_out_LNG": 1, "cut_out_load": 1, "illegal_overload": 0, "requested_generator_power": 0.0, "spare_power": 0.0}` |

</details>

<details><summary>`zero_load_soc_threshold_spare` — explicit-hot-start: at PL=0 and SoC exactly 0.95, RES production should become spare power rather than battery charge.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: at PL=0 and SoC exactly 0.95, RES production should become spare power rather than battery charge. |
| initial_state | `LNGShipEMS.RESCoversCharge` |
| initial_vars | `{"PL": 0.0, "Ppv": 10.0, "Pw": 5.0, "SoC": 0.95}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `zero_load_full_soc_spare` | `0` | `[]` | `LNGShipEMS.ZeroLoadSpare` | `{"battery_charging_power": 0.0, "battery_discharge_power": 0.0, "cut_in_LNG": 0, "cut_in_load": 0, "cut_out_LNG": 1, "cut_out_load": 1, "illegal_overload": 0, "requested_generator_power": 0.0, "spare_power": 15.0}` |

</details>

<details><summary>`res_covers_charge_below_soc_threshold` — explicit-hot-start: with positive load covered by RES and SoC below 0.95, demand is served by RES and residual renewable power charges the battery.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: with positive load covered by RES and SoC below 0.95, demand is served by RES and residual renewable power charges the battery. |
| initial_state | `LNGShipEMS.ZeroLoadSpare` |
| initial_vars | `{"PL": 40.0, "Ppv": 30.0, "Pw": 20.0, "SoC": 0.94}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `res_surplus_charging` | `0` | `[]` | `LNGShipEMS.RESCoversCharge` | `{"battery_charging_power": 10.0, "battery_discharge_power": 0.0, "cut_in_DG1": 0, "cut_in_DG2": 0, "cut_in_DG3": 0, "cut_in_LNG": 0, "cut_in_load": 1, "cut_out_DG1": 1, "cut_out_DG2": 1, "cut_out_DG3": 1, "cut_out_LNG": 1, "cut_out_load": 0, "illegal_overload": 0, "requested_generator_power": 0.0, "spare_power": 0.0}` |

</details>

<details><summary>`res_covers_spare_at_soc_threshold` — explicit-hot-start: with positive load covered by RES and SoC exactly 0.95, residual renewable power should be reported as spare.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: with positive load covered by RES and SoC exactly 0.95, residual renewable power should be reported as spare. |
| initial_state | `LNGShipEMS.BatteryAssist` |
| initial_vars | `{"PL": 40.0, "Ppv": 30.0, "Pw": 20.0, "SoC": 0.95}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `res_surplus_spare` | `0` | `[]` | `LNGShipEMS.RESCoversSpare` | `{"battery_charging_power": 0.0, "battery_discharge_power": 0.0, "cut_in_DG1": 0, "cut_in_DG2": 0, "cut_in_DG3": 0, "cut_in_LNG": 0, "cut_in_load": 1, "cut_out_DG1": 1, "cut_out_DG2": 1, "cut_out_DG3": 1, "cut_out_LNG": 1, "cut_out_load": 0, "illegal_overload": 0, "requested_generator_power": 0.0, "spare_power": 10.0}` |

</details>

<details><summary>`battery_assist_at_battery_capacity_boundary` — explicit-hot-start: when RES is short, SoC is suitable, and the deficit exactly equals battery_Pmax, batteries should cover the deficit before LNG or diesels.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: when RES is short, SoC is suitable, and the deficit exactly equals battery_Pmax, batteries should cover the deficit before LNG or diesels. |
| initial_state | `LNGShipEMS.LNGDispatch` |
| initial_vars | `{"PL": 100.0, "Pd1max": 20.0, "Pd2max": 20.0, "Plngmax": 60.0, "Ppv": 30.0, "Pw": 20.0, "SoC": 0.5, "battery_Pmax": 50.0, "eng3_Pmax": 20.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `battery_covers_exact_deficit` | `0` | `[]` | `LNGShipEMS.BatteryAssist` | `{"battery_charging_power": 0.0, "battery_discharge_power": 50.0, "cut_in_DG1": 0, "cut_in_DG2": 0, "cut_in_DG3": 0, "cut_in_LNG": 0, "cut_in_load": 1, "cut_out_DG1": 1, "cut_out_DG2": 1, "cut_out_DG3": 1, "cut_out_LNG": 1, "cut_out_load": 0, "illegal_overload": 0, "requested_generator_power": 0.0, "spare_power": 0.0}` |

</details>

<details><summary>`lng_dispatch_at_lng_capacity_boundary` — explicit-hot-start: when battery alone is insufficient and the deficit exactly equals LNG capacity, LNG should be cut in before diesel units.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: when battery alone is insufficient and the deficit exactly equals LNG capacity, LNG should be cut in before diesel units. |
| initial_state | `LNGShipEMS.RESCoversCharge` |
| initial_vars | `{"PL": 110.0, "Pd1max": 20.0, "Pd2max": 20.0, "Plngmax": 60.0, "Ppv": 30.0, "Pw": 20.0, "SoC": 0.5, "battery_Pmax": 50.0, "eng3_Pmax": 20.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `lng_covers_exact_deficit` | `0` | `[]` | `LNGShipEMS.LNGDispatch` | `{"battery_charging_power": 0.0, "battery_discharge_power": 0.0, "cut_in_DG1": 0, "cut_in_DG2": 0, "cut_in_DG3": 0, "cut_in_LNG": 1, "cut_in_load": 1, "cut_out_DG1": 1, "cut_out_DG2": 1, "cut_out_DG3": 1, "cut_out_LNG": 0, "cut_out_load": 0, "illegal_overload": 0, "requested_generator_power": 60.0, "spare_power": 0.0}` |

</details>

<details><summary>`lng_charge_margin_low_soc_boundary` — explicit-hot-start: at low SoC exactly 0.20, the LNG-covered branch should add the Pgmax/5 charging margin.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: at low SoC exactly 0.20, the LNG-covered branch should add the Pgmax/5 charging margin. |
| initial_state | `LNGShipEMS.LNGDG3Dispatch` |
| initial_vars | `{"PL": 100.0, "Pd1max": 20.0, "Pd2max": 20.0, "Pgmax": 50.0, "Plngmax": 60.0, "Ppv": 30.0, "Pw": 20.0, "SoC": 0.2, "battery_Pmax": 50.0, "eng3_Pmax": 20.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `lng_margin_charges_battery` | `0` | `[]` | `LNGShipEMS.LNGChargeMargin` | `{"battery_charging_power": 10.0, "battery_discharge_power": 0.0, "cut_in_DG1": 0, "cut_in_DG2": 0, "cut_in_DG3": 0, "cut_in_LNG": 1, "cut_in_load": 1, "cut_out_DG1": 1, "cut_out_DG2": 1, "cut_out_DG3": 1, "cut_out_LNG": 0, "cut_out_load": 0, "illegal_overload": 0, "requested_generator_power": 60.0, "spare_power": 0.0}` |

</details>

<details><summary>`lng_dg3_dispatch_at_eng3_boundary` — explicit-hot-start: when LNG alone is insufficient and the deficit exactly fits LNG plus DG3 capacity, LNG and DG3 should be used before DG1/DG2.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: when LNG alone is insufficient and the deficit exactly fits LNG plus DG3 capacity, LNG and DG3 should be used before DG1/DG2. |
| initial_state | `LNGShipEMS.LNGChargeMargin` |
| initial_vars | `{"PL": 130.0, "Pd1max": 20.0, "Pd2max": 20.0, "Plngmax": 60.0, "Ppv": 30.0, "Pw": 20.0, "SoC": 0.5, "battery_Pmax": 10.0, "eng3_Pmax": 20.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `lng_and_dg3_cover_exact_deficit` | `0` | `[]` | `LNGShipEMS.LNGDG3Dispatch` | `{"battery_charging_power": 0.0, "battery_discharge_power": 0.0, "cut_in_DG1": 0, "cut_in_DG2": 0, "cut_in_DG3": 1, "cut_in_LNG": 1, "cut_in_load": 1, "cut_out_DG1": 1, "cut_out_DG2": 1, "cut_out_DG3": 0, "cut_out_LNG": 0, "cut_out_load": 0, "illegal_overload": 0, "requested_generator_power": 80.0, "spare_power": 0.0}` |

</details>

<details><summary>`lng_dg3_charge_margin_pd1_margin` — explicit-hot-start: in a later low-SoC diesel-generator case, the Pd1max/10 charging margin should be added while using LNG and DG3.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: in a later low-SoC diesel-generator case, the Pd1max/10 charging margin should be added while using LNG and DG3. |
| initial_state | `LNGShipEMS.AddDG1LastPriority` |
| initial_vars | `{"PL": 120.0, "Pd1max": 100.0, "Pd2max": 20.0, "Plngmax": 60.0, "Ppv": 30.0, "Pw": 20.0, "SoC": 0.2, "battery_Pmax": 10.0, "eng3_Pmax": 20.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `dg3_margin_charges_battery` | `0` | `[]` | `LNGShipEMS.LNGDG3ChargeMargin` | `{"battery_charging_power": 10.0, "battery_discharge_power": 0.0, "cut_in_DG1": 0, "cut_in_DG2": 0, "cut_in_DG3": 1, "cut_in_LNG": 1, "cut_in_load": 1, "cut_out_DG1": 1, "cut_out_DG2": 1, "cut_out_DG3": 0, "cut_out_LNG": 0, "cut_out_load": 0, "illegal_overload": 0, "requested_generator_power": 80.0, "spare_power": 0.0}` |

</details>

<details><summary>`add_dg1_last_priority_boundary` — explicit-hot-start: when the deficit exceeds LNG plus DG3 but exactly fits after adding DG1, DG1 is cut in and DG2 remains cut out.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: when the deficit exceeds LNG plus DG3 but exactly fits after adding DG1, DG1 is cut in and DG2 remains cut out. |
| initial_state | `LNGShipEMS.AddDG2LastPriority` |
| initial_vars | `{"PL": 150.0, "Pd1max": 20.0, "Pd2max": 20.0, "Plngmax": 60.0, "Ppv": 30.0, "Pw": 20.0, "SoC": 0.5, "battery_Pmax": 10.0, "eng3_Pmax": 20.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `dg1_added_before_dg2` | `0` | `[]` | `LNGShipEMS.AddDG1LastPriority` | `{"battery_charging_power": 0.0, "battery_discharge_power": 0.0, "cut_in_DG1": 1, "cut_in_DG2": 0, "cut_in_DG3": 1, "cut_in_LNG": 1, "cut_in_load": 1, "cut_out_DG1": 0, "cut_out_DG2": 1, "cut_out_DG3": 0, "cut_out_LNG": 0, "cut_out_load": 0, "illegal_overload": 0, "requested_generator_power": 100.0, "spare_power": 0.0}` |

</details>

<details><summary>`add_dg2_last_priority_boundary` — explicit-hot-start: when the deficit exceeds LNG plus DG3 plus DG1 but exactly fits after adding DG2, both DG1 and DG2 are cut in as last-priority units.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: when the deficit exceeds LNG plus DG3 plus DG1 but exactly fits after adding DG2, both DG1 and DG2 are cut in as last-priority units. |
| initial_state | `LNGShipEMS.ExtremeOverloadBatteryLack` |
| initial_vars | `{"PL": 170.0, "Pd1max": 20.0, "Pd2max": 20.0, "Plngmax": 60.0, "Ppv": 30.0, "Pw": 20.0, "SoC": 0.5, "battery_Pmax": 10.0, "eng3_Pmax": 20.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `dg2_added_after_dg1` | `0` | `[]` | `LNGShipEMS.AddDG2LastPriority` | `{"battery_charging_power": 0.0, "battery_discharge_power": 0.0, "cut_in_DG1": 1, "cut_in_DG2": 1, "cut_in_DG3": 1, "cut_in_LNG": 1, "cut_in_load": 1, "cut_out_DG1": 0, "cut_out_DG2": 0, "cut_out_DG3": 0, "cut_out_LNG": 0, "cut_out_load": 0, "illegal_overload": 0, "requested_generator_power": 120.0, "spare_power": 0.0}` |

</details>

<details><summary>`extreme_overload_all_thermal_and_battery_lack` — explicit-hot-start: for demand exceeding all RES and thermal resources, all thermal units are activated and the remaining lack is covered by battery discharge i...<truncated 29 chars></summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: for demand exceeding all RES and thermal resources, all thermal units are activated and the remaining lack is covered by battery discharge in the illegal overload state. |
| initial_state | `LNGShipEMS.RESCoversSpare` |
| initial_vars | `{"PL": 180.0, "Pd1max": 20.0, "Pd2max": 20.0, "Plngmax": 60.0, "Ppv": 30.0, "Pw": 20.0, "SoC": 0.5, "battery_Pmax": 10.0, "eng3_Pmax": 20.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `all_thermal_plus_battery_lack` | `0` | `[]` | `LNGShipEMS.ExtremeOverloadBatteryLack` | `{"battery_charging_power": 0.0, "battery_discharge_power": 10.0, "cut_in_DG1": 1, "cut_in_DG2": 1, "cut_in_DG3": 1, "cut_in_LNG": 1, "cut_in_load": 1, "cut_out_DG1": 0, "cut_out_DG2": 0, "cut_out_DG3": 0, "cut_out_LNG": 0, "cut_out_load": 0, "illegal_overload": 1, "requested_generator_power": 120.0, "spare_power": 0.0}` |

</details>


### 7. Repair / blocking feedback 明细

口径：本节记录 agent-loop 真实进入 repair block 后的证据链：FixRequestBatch、SL-9 per-request accept/reject、candidate diff、local-check evidence、SL-10(NL+FixLog) 审阅，以及完整 FixLog ledger 摘录。

| Repair | iteration | accepted | source | blocking diagnostics | SL-9 decisions | SL-10 / local checks | candidate hash |
|---:|---:|---:|---|---|---|---|---|
| 1 | `0` | ✅ | `SD-4` | W_UNWRITTEN_READ_VAR:var_name=SoC_low_limit, W_UNWRITTEN_READ_VAR:var_name=battery_Pmax, W_UNWRITTEN_READ_VAR:var_name=Plngmax, W_UNWRITTEN_READ_VAR:var_name=Pd2max, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.RESCoversCharge:to_path=LNGShipEMS.BatteryAssist, ... +100 | accept=1, reject=11, waiver=11 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=none, rework=<none>; local ok=False, target=False, regression=False, drift=none, local_stage=SD-10, reason=design_target_unresolved | `sha256:e4cf5afd22c71c13ec6bf27c1372b7fbca62216ddb49195ac0b757d4fe3ed1b9` |
| 2 | `1` | ❌ | `SD-4` | W_UNWRITTEN_READ_VAR:var_name=battery_Pmax, W_UNWRITTEN_READ_VAR:var_name=Plngmax, W_UNWRITTEN_READ_VAR:var_name=Pd2max, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.RESCoversCharge:to_path=LNGShipEMS.BatteryAssist, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.RESCoversCharge:to_path=LNGShipEMS.LNGDispatch, ... +99 | accept=0, reject=12, waiver=12 | <none> | `sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 3 | `2` | ✅ | `SD-6` | default_init_zero_load_charge | accept=1, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none>; local ok=False, target=False, regression=False, drift=major, local_stage=SD-10, reason=new_blocking_design_diagnostic; forced_transition_count_drift | `sha256:9121b16d876b7385b65d3cf1f8060acd9e094046ce82de945e480c492432fa20` |
| 4 | `3` | ✅ | `SD-4` | W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.InitialDispatchSelect:to_path=LNGShipEMS.BatteryAssist, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.InitialDispatchSelect:to_path=LNGShipEMS.LNGDispatch, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.InitialDispatchSelect:to_path=LNGShipEMS.LNGChargeMargin, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.InitialDispatchSelect:to_path=LNGShipEMS.LNGDG3Dispatch, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.InitialDispatchSelect:to_path=LNGShipEMS.LNGDG3ChargeMargin, ... +23 | accept=4, reject=8, waiver=8 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=none, rework=<none>; local ok=True, target=True, regression=False, drift=none, local_stage=SD-10, reason= | `sha256:3454c23c9fdabd2846510c8225fe02a330f3f8fec051dee98e1de2f7ebab9fc1` |

<details><summary>Repair 1 / iteration `0` / source `SD-4` / accepted=✅</summary>

#### 为什么进入修复

- selected feedback source：`SD-4`；blocking=`True`；pre_scenario=`True`。
- problem_summary：Variable 'SoC_low_limit' is read but never written by any action or transition effect.; Variable 'battery_Pmax' is read but never written by any action or transition effect.; Variable 'Plngmax' is read but never written by any action or transition effect.
- diagnostic ids：`W_UNWRITTEN_READ_VAR:var_name=SoC_low_limit, W_UNWRITTEN_READ_VAR:var_name=battery_Pmax, W_UNWRITTEN_READ_VAR:var_name=Plngmax, W_UNWRITTEN_READ_VAR:var_name=Pd2max, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.RESCoversCharge:to_path=LNGShipEMS.BatteryAssist, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.RESCoversCharge:to_path=LNGShipEMS.LNGDispatch, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.RESCoversCharge:to_path=LNGShipEMS.LNGChargeMargin, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.RESCoversCharge:to_path=LNGShipEMS.LNGDG3Dispatch, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.RESCoversCharge:to_path=LNGShipEMS.LNGDG3ChargeMargin, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.RESCoversCharge:to_path=LNGShipEMS.AddDG1LastPriority, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.RESCoversCharge:to_path=LNGShipEMS.AddDG2LastPriority, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.RESCoversCharge:to_path=LNGShipEMS.ExtremeOverloadBatteryLack, ... +93`。
- before_dsl_hash：`sha256:99fe6082d0658600915be6b8f6a84fe180769746e3be3d660af3442a02f12228`；candidate_dsl_hash：`sha256:e4cf5afd22c71c13ec6bf27c1372b7fbca62216ddb49195ac0b757d4fe3ed1b9`。

#### 错误证据 / diagnostics

- 1. `W_UNWRITTEN_READ_VAR` `W_UNWRITTEN_READ_VAR:var_name=SoC_low_limit` policy=`budgeted_repair`：Variable 'SoC_low_limit' is read but never written by any action or transition effect.；refs=`{"init_value": "0.2", "read_states": ["LNGShipEMS.AddDG1LastPriority", "LNGShipEMS.AddDG2LastPriority", "LNGShipEMS.BatteryAssist", "LNGShipEMS.ExtremeOverloadBatteryLack", "LNGShipEMS.LNGChargeMargin", "LNGShipEMS.LNGDG3ChargeMargin", "LNGShipEMS.LNGDG3Dispatch", "LNGShipEMS.LNGDispatch", "LNGShipE...<truncated 136 chars>`
- 2. `W_UNWRITTEN_READ_VAR` `W_UNWRITTEN_READ_VAR:var_name=battery_Pmax` policy=`budgeted_repair`：Variable 'battery_Pmax' is read but never written by any action or transition effect.；refs=`{"init_value": "0.0", "read_states": ["LNGShipEMS.AddDG1LastPriority", "LNGShipEMS.AddDG2LastPriority", "LNGShipEMS.BatteryAssist", "LNGShipEMS.ExtremeOverloadBatteryLack", "LNGShipEMS.LNGChargeMargin", "LNGShipEMS.LNGDG3ChargeMargin", "LNGShipEMS.LNGDG3Dispatch", "LNGShipEMS.LNGDispatch", "LNGShipE...<truncated 135 chars>`
- 3. `W_UNWRITTEN_READ_VAR` `W_UNWRITTEN_READ_VAR:var_name=Plngmax` policy=`budgeted_repair`：Variable 'Plngmax' is read but never written by any action or transition effect.；refs=`{"init_value": "0.0", "read_states": ["LNGShipEMS.AddDG1LastPriority", "LNGShipEMS.AddDG2LastPriority", "LNGShipEMS.BatteryAssist", "LNGShipEMS.ExtremeOverloadBatteryLack", "LNGShipEMS.LNGChargeMargin", "LNGShipEMS.LNGDG3ChargeMargin", "LNGShipEMS.LNGDG3Dispatch", "LNGShipEMS.LNGDispatch", "LNGShipE...<truncated 130 chars>`
- 4. `W_UNWRITTEN_READ_VAR` `W_UNWRITTEN_READ_VAR:var_name=Pd2max` policy=`budgeted_repair`：Variable 'Pd2max' is read but never written by any action or transition effect.；refs=`{"init_value": "0.0", "read_states": ["LNGShipEMS.AddDG1LastPriority", "LNGShipEMS.AddDG2LastPriority", "LNGShipEMS.BatteryAssist", "LNGShipEMS.ExtremeOverloadBatteryLack", "LNGShipEMS.LNGChargeMargin", "LNGShipEMS.LNGDG3ChargeMargin", "LNGShipEMS.LNGDG3Dispatch", "LNGShipEMS.LNGDispatch", "LNGShipE...<truncated 129 chars>`
- 5. `W_GUARD_VARS_NEVER_CHANGE` `W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.RESCoversCharge:to_path=LNGShipEMS.BatteryAssist` policy=`budgeted_repair`：Transition guard reads only variables that are never changed by actions or effects.；refs=`{"from_path": "LNGShipEMS.RESCoversCharge", "guard_vars": ["PL", "Ppv", "Pw", "SoC", "SoC_low_limit", "battery_Pmax"], "to_path": "LNGShipEMS.BatteryAssist"}`
- 6. `W_GUARD_VARS_NEVER_CHANGE` `W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.RESCoversCharge:to_path=LNGShipEMS.LNGDispatch` policy=`budgeted_repair`：Transition guard reads only variables that are never changed by actions or effects.；refs=`{"from_path": "LNGShipEMS.RESCoversCharge", "guard_vars": ["PL", "Plngmax", "Ppv", "Pw", "SoC", "SoC_low_limit", "battery_Pmax"], "to_path": "LNGShipEMS.LNGDispatch"}`
- 7. `W_GUARD_VARS_NEVER_CHANGE` `W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.RESCoversCharge:to_path=LNGShipEMS.LNGChargeMargin` policy=`budgeted_repair`：Transition guard reads only variables that are never changed by actions or effects.；refs=`{"from_path": "LNGShipEMS.RESCoversCharge", "guard_vars": ["PL", "Pgmax", "Plngmax", "Ppv", "Pw", "SoC", "SoC_low_limit"], "to_path": "LNGShipEMS.LNGChargeMargin"}`
- 8. `W_GUARD_VARS_NEVER_CHANGE` `W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.RESCoversCharge:to_path=LNGShipEMS.LNGDG3Dispatch` policy=`budgeted_repair`：Transition guard reads only variables that are never changed by actions or effects.；refs=`{"from_path": "LNGShipEMS.RESCoversCharge", "guard_vars": ["PL", "Plngmax", "Ppv", "Pw", "SoC", "SoC_low_limit", "eng3_Pmax"], "to_path": "LNGShipEMS.LNGDG3Dispatch"}`
- ……另有 `92` 条 evidence 见 run record。

#### 变量角色与上下文提示

- policy：Advisory only. Do not invent writes for external_input_candidate variables unless NL explicitly gives update semantics; add meaningful NL-grounded writes only for internal state variables.
- source：SD-4 diagnostic refs and generic NL external-input rationale

| Variable | role_hint | nl_token_present | diagnostics |
|---|---|---:|---|
| `PL` | `external_input_candidate` | ✅ | `W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +140` |
| `Pd1max` | `external_input_candidate` | ✅ | `W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +44` |
| `Pd2max` | `unknown` | ❌ | `W_UNWRITTEN_READ_VAR, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +20` |
| `Pgmax` | `external_input_candidate` | ✅ | `W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +8` |
| `Plngmax` | `unknown` | ❌ | `W_UNWRITTEN_READ_VAR, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +80` |
| `Ppv` | `external_input_candidate` | ✅ | `W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +116` |
| `Pw` | `external_input_candidate` | ✅ | `W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +116` |
| `SoC` | `external_input_candidate` | ✅ | `W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +104` |
| `SoC_low_limit` | `unknown` | ❌ | `W_UNWRITTEN_READ_VAR, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +56` |
| `battery_Pmax` | `unknown` | ❌ | `W_UNWRITTEN_READ_VAR, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +20` |
| `battery_charging_power` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `battery_discharge_power` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `cut_in_DG1` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `cut_in_DG2` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `cut_in_DG3` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `cut_in_LNG` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `cut_in_load` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `cut_out_DG1` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `cut_out_DG2` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `cut_out_DG3` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `cut_out_LNG` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `cut_out_load` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `eng3_Pmax` | `external_input_candidate` | ✅ | `W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +56` |
| `illegal_overload` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `requested_generator_power` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `spare_power` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |

#### SD-8 FixRequestBatch / 修改请求

- batch_id：`fixbatch-0-sha256-874b3e13f39`；source_stage=`SD-4`；legacy_plan_kind=`FixPlan`；requests=`12`。

| request_id | severity | hard | waiver | problem | evidence |
|---|---|---:|---:|---|---|
| `fixreq-0-sd4-0-b481b95286` | `blocking_warning` | ❌ | ✅ | Variable 'SoC_low_limit' is read but never written by any action or transition effect.; Variable 'battery_Pmax' is read but never written by any action or transition effect.; Variable 'Plngmax' is read but never written ...<truncated 35 chars> | `W_UNWRITTEN_READ_VAR` |
| `fixreq-0-sd4-1-e891b4d9d0` | `blocking_warning` | ❌ | ✅ | Variable 'SoC_low_limit' is read but never written by any action or transition effect.; Variable 'battery_Pmax' is read but never written by any action or transition effect.; Variable 'Plngmax' is read but never written ...<truncated 35 chars> | `W_UNWRITTEN_READ_VAR` |
| `fixreq-0-sd4-2-313f683f70` | `blocking_warning` | ❌ | ✅ | Variable 'SoC_low_limit' is read but never written by any action or transition effect.; Variable 'battery_Pmax' is read but never written by any action or transition effect.; Variable 'Plngmax' is read but never written ...<truncated 35 chars> | `W_UNWRITTEN_READ_VAR` |
| `fixreq-0-sd4-3-4f0f4171fd` | `blocking_warning` | ❌ | ✅ | Variable 'SoC_low_limit' is read but never written by any action or transition effect.; Variable 'battery_Pmax' is read but never written by any action or transition effect.; Variable 'Plngmax' is read but never written ...<truncated 35 chars> | `W_UNWRITTEN_READ_VAR` |
| `fixreq-0-sd4-4-b5b2f5d5ad` | `blocking_warning` | ❌ | ✅ | Variable 'SoC_low_limit' is read but never written by any action or transition effect.; Variable 'battery_Pmax' is read but never written by any action or transition effect.; Variable 'Plngmax' is read but never written ...<truncated 35 chars> | `W_GUARD_VARS_NEVER_CHANGE` |
| `fixreq-0-sd4-5-777856a1ea` | `blocking_warning` | ❌ | ✅ | Variable 'SoC_low_limit' is read but never written by any action or transition effect.; Variable 'battery_Pmax' is read but never written by any action or transition effect.; Variable 'Plngmax' is read but never written ...<truncated 35 chars> | `W_GUARD_VARS_NEVER_CHANGE` |
| `fixreq-0-sd4-6-3bf5386372` | `blocking_warning` | ❌ | ✅ | Variable 'SoC_low_limit' is read but never written by any action or transition effect.; Variable 'battery_Pmax' is read but never written by any action or transition effect.; Variable 'Plngmax' is read but never written ...<truncated 35 chars> | `W_GUARD_VARS_NEVER_CHANGE` |
| `fixreq-0-sd4-7-b77957cc50` | `blocking_warning` | ❌ | ✅ | Variable 'SoC_low_limit' is read but never written by any action or transition effect.; Variable 'battery_Pmax' is read but never written by any action or transition effect.; Variable 'Plngmax' is read but never written ...<truncated 35 chars> | `W_GUARD_VARS_NEVER_CHANGE` |
| `fixreq-0-sd4-8-127bbad309` | `blocking_warning` | ❌ | ✅ | Variable 'SoC_low_limit' is read but never written by any action or transition effect.; Variable 'battery_Pmax' is read but never written by any action or transition effect.; Variable 'Plngmax' is read but never written ...<truncated 35 chars> | `W_GUARD_VARS_NEVER_CHANGE` |
| `fixreq-0-sd4-9-c76ffc05a8` | `blocking_warning` | ❌ | ✅ | Variable 'SoC_low_limit' is read but never written by any action or transition effect.; Variable 'battery_Pmax' is read but never written by any action or transition effect.; Variable 'Plngmax' is read but never written ...<truncated 35 chars> | `W_GUARD_VARS_NEVER_CHANGE` |
- ……另有 `2` 个 request 见 run record。

#### SD-8 legacy fix plan / 修改建议

- recommended_strategy：Use diagnostics as hints; choose the smallest globally consistent repair.；Before returning a candidate, verify every required_preserve_element_id still has a concrete DSL representation.
- hint 1：The variable is used as input but never updated after its initial definition, so model behavior may be accidentally constant.；`actions=add_write, simplify_guard；do_not=Do not add a meaningless self-assignment.`
- hint 2：The variable is used as input but never updated after its initial definition, so model behavior may be accidentally constant.；`actions=add_write, simplify_guard；do_not=Do not add a meaningless self-assignment.`
- hint 3：The variable is used as input but never updated after its initial definition, so model behavior may be accidentally constant.；`actions=add_write, simplify_guard；do_not=Do not add a meaningless self-assignment.`
- hint 4：The variable is used as input but never updated after its initial definition, so model behavior may be accidentally constant.；`actions=add_write, simplify_guard；do_not=Do not add a meaningless self-assignment.`
- hint 5：This guard is controlled only by initial variable values. If those values never change, the transition condition is effectively fixed.；`actions=add_write, simplify_guard；do_not=Do not add a meaningless self-assignment; it does not model a real change., Do not rewrite the guard to a meaningless constant only to silence this diagnostic.`
- hint 6：This guard is controlled only by initial variable values. If those values never change, the transition condition is effectively fixed.；`actions=add_write, simplify_guard；do_not=Do not add a meaningless self-assignment; it does not model a real change., Do not rewrite the guard to a meaningless constant only to silence this diagnostic.`
- forbidden_edits：`Do not delete grounded required elements merely to silence diagnostics., Do not invent internal plant/environment dynamics merely to make external input variables appear written.`。
- required_preserve_element_ids：`state:RESCoversCharge, state:RESCoversSpare, state:ZeroLoadCharge, state:ZeroLoadSpare, state:BatteryAssist, state:LNGDispatch, state:LNGChargeMargin, state:LNGDG3Dispatch, state:LNGDG3ChargeMargin, state:AddDG1LastPriority, state:AddDG2LastPriority, state:ExtremeOverloadBatteryLack, ... +20`。

#### SL-9 per-request 决策

- accepted_request_ids：`<derived-from-table>`；candidate_len=`8827`。

| request_id | decision | waiver | rework_locked | rationale / intent |
|---|---|---:|---:|---|
| `fixreq-0-sd4-0-b481b95286` | `accept` | ❌ | ❌ | SoC_low_limit is a fixed modeling threshold, not an NL-described time-varying input. The smallest safe repair is to inline its initialized value 0.20 in the guards and remove the unwritten variable declaration, as suggested by the diagnostic.；intent=Replace SoC_low_limit guard reads with literal 0.20, Remove def float SoC_low_limit |
| `fixreq-0-sd4-1-e891b4d9d0` | `reject` | ✅ | ❌ | battery_Pmax is a capacity/input bound used to classify demand coverage. The NL does not provide runtime update semantics for it, and adding writes would invent plant dynamics. |
| `fixreq-0-sd4-2-313f683f70` | `reject` | ✅ | ❌ | Plngmax is a generator capacity/input bound. The NL requires dispatch against capacity bounds but does not define an internal update, so writing it would be ungrounded. |
| `fixreq-0-sd4-3-4f0f4171fd` | `reject` | ✅ | ❌ | Pd2max is a diesel-generator capacity/input bound. It should remain externally supplied/read-only in this dispatch classifier because no NL update rule is provided. |
| `fixreq-0-sd4-4-b5b2f5d5ad` | `reject` | ✅ | ❌ | The BatteryAssist guard is intentionally driven by external/time-varying inputs PL, Ppv, Pw, SoC and capacity battery_Pmax. Adding dummy writes would violate the forbidden edits. |
| `fixreq-0-sd4-5-777856a1ea` | `reject` | ✅ | ❌ | The LNGDispatch guard is an NL-grounded condition over demand, renewable generation, SoC, battery capacity and LNG capacity. These are external inputs/capacity bounds, not internal FSM state updates. |
| `fixreq-0-sd4-6-3bf5386372` | `reject` | ✅ | ❌ | The LNGChargeMargin guard is NL-grounded and depends on demand, renewables, SoC, Pgmax and LNG capacity. No safe internal write is specified by the NL. |
| `fixreq-0-sd4-7-b77957cc50` | `reject` | ✅ | ❌ | The LNGDG3Dispatch guard reads external demand/resource values and capacity bounds including eng3_Pmax. It should not be altered solely to silence never-change diagnostics. |
| `fixreq-0-sd4-8-127bbad309` | `reject` | ✅ | ❌ | The LNGDG3ChargeMargin guard is a required low-SoC/capacity branch. Its variables are external inputs or capacity parameters, and the NL gives no update equations. |
| `fixreq-0-sd4-9-c76ffc05a8` | `reject` | ✅ | ❌ | The AddDG1LastPriority guard implements the required last-priority DG1 branch over demand and capacity inputs. Simplifying or adding writes would reduce NL fidelity. |
| `fixreq-0-sd4-10-c3fd85bfda` | `reject` | ✅ | ❌ | The AddDG2LastPriority guard implements the required last-priority DG2 branch over demand and capacity inputs. These are intentionally externally supplied. |
| `fixreq-0-sd4-11-7c66d4691d` | `reject` | ✅ | ❌ | The ExtremeOverloadBatteryLack guard is required by the overload requirement and is driven by external demand/resource/capacity values. No safe edit is available without inventing dynamics. |
- repair_rationale：Accepted only the safe constant-threshold repair: SoC_low_limit had no independent NL-required variable identity and was initialized to 0.20, so inlining preserves behavior while removing an unwritten-read warning.；Preserved all twelve required finite states and all required output actions, cut-in/cut-out commands, and dispatch guards including RES cover, zero-load, battery assist, LNG, DG3, DG1/DG2 last-priority, and extreme overload branches.；Rejected/waived capacity/input write requests for battery_Pmax, Plngmax, Pd2max and guard-never-change warnings because PL, Ppv, Pw, SoC and capacity bounds are NL-described external inputs or capacity parameters. Adding artificial writes w...<truncated 77 chars>；The candidate remains a guard-driven condition-classification FSM using forced guard transitions to dynamically select dispatch states from current external inputs.
- diff_summary：`{"summary": "Removed the SoC_low_limit declaration and replaced all SoC_low_limit guard references with the literal threshold 0.20. No states, dispatch actions, capacity variables, output variables, or required guards were deleted."}`。

#### SL-9 candidate / 最终修改执行方案

```pyfcstm
def float PL = 0.0;
def float Ppv = 0.0;
def float Pw = 0.0;
def float SoC = 0.0;
def float battery_Pmax = 0.0;
def float Plngmax = 0.0;
def float eng3_Pmax = 0.0;
def float Pgmax = 0.0;
def float Pd1max = 0.0;
def float Pd2max = 0.0;
def float requested_generator_power = 0.0;
def float battery_discharge_power = 0.0;
def float battery_charging_power = 0.0;
def float spare_power = 0.0;
def int cut_in_LNG = 0;
def int cut_out_LNG = 0;
def int cut_in_DG1 = 0;
def int cut_out_DG1 = 0;
def int cut_in_DG2 = 0;
def int cut_out_DG2 = 0;
def int cut_in_DG3 = 0;
def int cut_out_DG3 = 0;
def int cut_in_load = 0;
def int cut_out_load = 0;
def int illegal_overload = 0;

state LNGShipEMS {
    ! * -> ZeroLoadCharge : if [PL == 0 && SoC < 0.95];
    ! * -> ZeroLoadSpare : if [PL == 0 && SoC >= 0.95];
    ! * -> RESCoversCharge : if [PL > 0 && Ppv + Pw >= PL && SoC < 0.95];
    ! * -> RESCoversSpare : if [PL > 0 && Ppv + Pw >= PL && SoC >= 0.95];
    ! * -> BatteryAssist : if [PL > 0 && Ppv + Pw < PL && SoC > 0.20 && PL - Ppv - Pw <= battery_Pmax];
    ! * -> LNGDispatch : if [PL > 0 && Ppv + Pw < PL && SoC > 0.20 && PL - Ppv - Pw > battery_Pmax && PL - Ppv - Pw <= Plngmax];
    ! * -> LNGChargeMargin : if [PL > 0 && Ppv + Pw < PL && SoC <= 0.20 && PL - Ppv - Pw + Pgmax / 5 <= Plngmax];
    ! * -> LNGDG3Dispatch : if [PL > 0 && Ppv + Pw < PL && SoC > 0.20 && PL - Ppv - Pw > Plngmax && PL - Ppv - Pw <= Plngmax + eng3_Pmax];
    ! * -> LNGDG3ChargeMargin : if [PL > 0 && Ppv + Pw < PL && SoC <= 0.20 && PL - Ppv - Pw + Pd1max / 10 > Plngmax && PL - Ppv - Pw + Pd1max / 10 <= Plngmax + eng3_Pmax];
    ! * -> AddDG1LastPriority : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > Plngmax + eng3_Pmax && PL - Ppv - Pw <= Plngmax + eng3_Pmax + Pd1max];
    ! * -> AddDG2LastPriority : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > Plngmax + eng3_Pmax + Pd1max && PL - Ppv - Pw <= Plngmax + eng3_Pmax + Pd1max + Pd2max];
    ! * -> ExtremeOverloadBatteryLack : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > Plngmax + eng3_Pmax + Pd1max + Pd2max];

    [*] -> RESCoversCharge;

    state RESCoversCharge {
        enter {
            requested_generator_power = 0.0;
            battery_discharge_power = 0.0;
            battery_charging_power = Ppv + Pw - PL;
            spare_power = 0.0;
            cut_in_LNG = 0;
            cut_out_LNG = 1;
            cut_in_DG1 = 0;
            cut_out_DG1 = 1;
            cut_in_DG2 = 0;
            cut_out_DG2 = 1;
            cut_in_DG3 = 0;
            cut_out_DG3 = 1;
            cut_in_load = 1;
            cut_out_load = 0;
            illegal_overload = 0;
        }
    }

    state RESCoversSpare {
        enter {
            requested_generator_power = 0.0;
            battery_discharge_power = 0.0;
            battery_charging_power = 0.0;
            spare_power = Ppv + Pw - PL;
            cut_in_LNG = 0;
            cut_out_LNG = 1;
            cut_in_DG1 = 0;
            cut_out_DG1 = 1;
            cut_in_DG2 = 0;
            cut_out_DG2 = 1;
            cut_in_DG3 = 0;
            cut_out_DG3 = 1;
            cut_in_load = 1;
            cut_out_load = 0;
            illegal_overload = 0;
        }
    }

    state ZeroLoadCharge {
        enter {
            requested_generator_power = 0.0;
            battery_discharge_power = 0.0;
            battery_charging_power = Ppv + Pw;
            spare_power = 0.0;
            cut_in_LNG = 0;
            cut_out_LNG = 1;
            cut_in_DG1 = 0;
            cut_out_DG1 = 1;
            cut_in_DG2 = 0;
            cut_out_DG2 = 1;
            cut_in_DG3 = 0;
            cut_out_DG3 = 1;
            cut_in_load = 0;
            cut_out_load = 1;
            illegal_overload = 0;
        }
    }

    state ZeroLoadSpare {
        enter {
            requested_generator_power = 0.0;
            battery_discharge_power = 0.0;
            battery_charging_power = 0.0;
            spare_power = Ppv + Pw;
            cut_in_LNG = 0;
            cut_out_LNG = 1;
            cut_in_DG1 = 0;
            cut_out_DG1 = 1;
            cut_in_DG2 = 0;
            cut_out_DG2 = 1;
            cut_in_DG3 = 0;
            cut_out_DG3 = 1;
            cut_in_load = 0;
            cut_out_load = 1;
            illegal_overload = 0;
        }
    }

    state BatteryAssist {
        enter {
            requested_generator_power = 0.0;
            battery_discharge_power = PL - Ppv - Pw;
            battery_charging_power = 0.0;
            spare_power = 0.0;
            cut_in_LNG = 0;
            cut_out_LNG = 1;
            cut_in_DG1 = 0;
            cut_out_DG1 = 1;
            cut_in_DG2 = 0;
            cut_out_DG2 = 1;
            cut_in_DG3 = 0;
            cut_out_DG3 = 1;
            cut_in_load = 1;
            cut_out_load = 0;
            illegal_overload = 0;
        }
    }

    state LNGDispatch {
        enter {
            requested_generator_power = PL - Ppv - Pw;
            battery_discharge_power = 0.0;
            battery_charging_power = 0.0;
            spare_power = 0.0;
            cut_in_LNG = 1;
            cut_out_LNG = 0;
            cut_in_DG1 = 0;
            cut_out_DG1 = 1;
            cut_in_DG2 = 0;
            cut_out_DG2 = 1;
            cut_in_DG3 = 0;
            cut_out_DG3 = 1;
            cut_in_load = 1;
            cut_out_load = 0;
            illegal_overload = 0;
        }
    }

    state LNGChargeMargin {
        enter {
            requested_generator_power = PL - Ppv - Pw + Pgmax / 5;
            battery_discharge_power = 0.0;
            battery_charging_power = Pgmax / 5;
            spare_power = 0.0;
            cut_in_LNG = 1;
            cut_out_LNG = 0;
            cut_in_DG1 = 0;
            cut_out_DG1 = 1;
            cut_in_DG2 = 0;
            cut_out_DG2 = 1;
            cut_in_DG3 = 0;
            cut_out_DG3 = 1;
            cut_in_load = 1;
            cut_out_load = 0;
            illegal_overload = 0;
        }
    }

    state LNGDG3Dispatch {
        enter {
            requested_generator_power = PL - Ppv - Pw;
            battery_discharge_power = 0.0;
            battery_charging_power = 0.0;
            spare_power = 0.0;
            cut_in_LNG = 1;
            cut_out_LNG = 0;
            cut_in_DG1 = 0;
            cut_out_DG1 = 1;
            cut_in_DG2 = 0;
            cut_out_DG2 = 1;
            cut_in_DG3 = 1;
            cut_out_DG3 = 0;
            cut_in_load = 1;
            cut_out_load = 0;
            illegal_overload = 0;
        }
    }

    state LNGDG3ChargeMargin {
        enter {
            requested_generator_power = PL - Ppv - Pw + Pd1max / 10;
            battery_discharge_power = 0.0;
            battery_charging_power = Pd1max / 10;
            spare_power = 0.0;
            cut_in_LNG = 1;
            cut_out_LNG = 0;
            cut_in_DG1 = 0;
            cut_out_DG1 = 1;
            cut_in_DG2 = 0;
            cut_out_DG2 = 1;
            cut_in_DG3 = 1;
            cut_out_DG3 = 0;
            cut_in_load = 1;
            cut_out_load = 0;
            illegal_overload = 0;
        }
    }

    state AddDG1LastPriority {
        enter {
            requested_generator_power = PL - Ppv - Pw;
            battery_discharge_power = 0.0;
            battery_charging_power = 0.0;
            spare_power = 0.0;
            cut_in_LNG = 1;
            cut_out_LNG = 0;
            cut_in_DG1 = 1;
            cut_out_DG1 = 0;
            cut_in_DG2 = 0;
            cut_out_DG2 = 1;
            cut_in_DG3 = 1;
            cut_out_DG3 = 0;
            cut_in_load = 1;
            cut_out_load = 0;
            illegal_overload = 0;
        }
    }

    state AddDG2LastPriority {
        enter {
            requested_generator_power = PL - Ppv - Pw;
            battery_discharge_power = 0.0;
            battery_charging_power = 0.0;
            spare_power = 0.0;
            cut_in_LNG = 1;
            cut_out_LNG = 0;
            cut_in_DG1 = 1;
            cut_out_DG1 = 0;
            cut_in_DG2 = 1;
            cut_out_DG2 = 0;
            cut_in_DG3 = 1;
            cut_out_DG3 = 0;
            cut_in_load = 1;
            cut_out_load = 0;
            illegal_overload = 0;
        }
    }

    state ExtremeOverloadBatteryLack {
        enter {
            requested_generator_power = Plngmax + eng3_Pmax + Pd1max + Pd2max;
            battery_discharge_power = PL - Ppv - Pw - Plngmax - eng3_Pmax - Pd1max - Pd2max;
            battery_charging_power = 0.0;
            spare_power = 0.0;
            cut_in_LNG = 1;
            cut_out_LNG = 0;
            cut_in_DG1 = 1;
            cut_out_DG1 = 0;
            cut_in_DG2 = 1;
            cut_out_DG2 = 0;
            cut_in_DG3 = 1;
            cut_out_DG3 = 0;
            cut_in_load = 1;
            cut_out_load = 0;
            illegal_overload = 1;
        }
    }
}
```

#### Candidate diff（before -> candidate）

```diff
--- before.fcstm
+++ candidate.fcstm
@@ -2,7 +2,6 @@
 def float Ppv = 0.0;
 def float Pw = 0.0;
 def float SoC = 0.0;
-def float SoC_low_limit = 0.20;
 def float battery_Pmax = 0.0;
 def float Plngmax = 0.0;
 def float eng3_Pmax = 0.0;
@@ -30,11 +29,11 @@
     ! * -> ZeroLoadSpare : if [PL == 0 && SoC >= 0.95];
     ! * -> RESCoversCharge : if [PL > 0 && Ppv + Pw >= PL && SoC < 0.95];
     ! * -> RESCoversSpare : if [PL > 0 && Ppv + Pw >= PL && SoC >= 0.95];
-    ! * -> BatteryAssist : if [PL > 0 && Ppv + Pw < PL && SoC > SoC_low_limit && PL - Ppv - Pw <= battery_Pmax];
-    ! * -> LNGDispatch : if [PL > 0 && Ppv + Pw < PL && SoC > SoC_low_limit && PL - Ppv - Pw > battery_Pmax && PL - Ppv - Pw <= Plngmax];
-    ! * -> LNGChargeMargin : if [PL > 0 && Ppv + Pw < PL && SoC <= SoC_low_limit && PL - Ppv - Pw + Pgmax / 5 <= Plngmax];
-    ! * -> LNGDG3Dispatch : if [PL > 0 && Ppv + Pw < PL && SoC > SoC_low_limit && PL - Ppv - Pw > Plngmax && PL - Ppv - Pw <= Plngmax + eng3_Pmax];
-    ! * -> LNGDG3ChargeMargin : if [PL > 0 && Ppv + Pw < PL && SoC <= SoC_low_limit && PL - Ppv - Pw + Pd1max / 10 > Plngmax && PL - Ppv - Pw + Pd1max / 10 <= Plngmax + eng3_Pmax];
+    ! * -> BatteryAssist : if [PL > 0 && Ppv + Pw < PL && SoC > 0.20 && PL - Ppv - Pw <= battery_Pmax];
+    ! * -> LNGDispatch : if [PL > 0 && Ppv + Pw < PL && SoC > 0.20 && PL - Ppv - Pw > battery_Pmax && PL - Ppv - Pw <= Plngmax];
+    ! * -> LNGChargeMargin : if [PL > 0 && Ppv + Pw < PL && SoC <= 0.20 && PL - Ppv - Pw + Pgmax / 5 <= Plngmax];
+    ! * -> LNGDG3Dispatch : if [PL > 0 && Ppv + Pw < PL && SoC > 0.20 && PL - Ppv - Pw > Plngmax && PL - Ppv - Pw <= Plngmax + eng3_Pmax];
+    ! * -> LNGDG3ChargeMargin : if [PL > 0 && Ppv + Pw < PL && SoC <= 0.20 && PL - Ppv - Pw + Pd1max / 10 > Plngmax && PL - Ppv - Pw + Pd1max / 10 <= Plngmax + eng3_Pmax];
     ! * -> AddDG1LastPriority : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > Plngmax + eng3_Pmax && PL - Ppv - Pw <= Plngmax + eng3_Pmax + Pd1max];
     ! * -> AddDG2LastPriority : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > Plngmax + eng3_Pmax + Pd1max && PL - Ppv - Pw <= Plngmax + eng3_Pmax + Pd1max + Pd2max];
     ! * -> ExtremeOverloadBatteryLack : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > Plngmax + eng3_Pmax + Pd1max + Pd2max];
```

#### SL-10 审查结果

- SL-10 decision=`pass`，ok=`True`，target_resolved=`True`，regression_detected=`False`，drift_risk=`none`。
- SL-10 review_meta：schema=`SL10RepairReviewOutput.v1`，failure_policy=`fail_closed`，replay_key=`SL-10:sha256:8bdb2e2ea93df5c6fdd42b889f9a7b8aa19bddea409e0bf98f1481e68706bc9b`。
  - SL-10 evidence 1: `{"summary": "The only accepted edit removes the non-NL variable SoC_low_limit and replaces its guard reads with the initialized literal 0.20. This preserves the same low-SoC threshold behavior while resolving that unwritten-read request without deleting any NL-required state, output, guard, or dispatch branch."}`
  - SL-10 evidence 2: `{"summary": "The candidate DSL preserves all twelve required finite states: RESCoversCharge, RESCoversSpare, ZeroLoadCharge, ZeroLoadSpare, BatteryAssist, LNGDispatch, LNGChargeMargin, LNGDG3Dispatch, LNGDG3ChargeMargin, AddDG1LastPriority, AddDG2LastPriority, and ExtremeOverloadBatteryLack."}`
  - SL-10 evidence 3: `{"summary": "The candidate continues to implement the NL dispatch priorities and outputs: RES coverage charges or creates spare based on SoC 0.95; zero-load sends RES to battery or spare; deficit cases use battery, LNG, DG3, DG1/DG2 last-priority branches; low-SoC charging margins Pgmax/5 and Pd1max/10 remain; extreme overload activates all thermal units and covers the lack by battery discharge with illegal_overload marked."}`
  - SL-10 evidence 4: `{"summary": "The SL-9 decisions correctly waived the remaining non-hard design warnings for battery_Pmax, Plngmax, Pd2max, and guard-never-change diagnostics because the NL describes PL, Ppv, Pw, SoC, and capacity bounds as read inputs/parameters for dispatch classification, not internal FSM variables with specified update equations."}`
  - SL-10 evidence 5: `{"summary": "The DSL diff is narrow and non-regressive: it only deletes def float SoC_low_limit and substitutes 0.20 in guards; no required preserve element, cut-in/cut-out command, capacity variable used by dispatch, output action, or required guard was removed."}`
- local checks evidence：stage=`SD-10`；note=PR-E1 uses local parse/semantic/design/sim checks as SL-10 evidence, not as the final deterministic judge.。
  - local ok=`False`，target_resolved=`False`，regression_detected=`False`，drift_risk=`none`。
  - local_rejection：reason=`design_target_unresolved`，rejected_by_stage=`SD-10`。
    - local evidence 1: `design_target_unresolved` {"items": [{"budget_exhausted": false, "budget_remaining": 1, "code": "W_UNWRITTEN_READ_VAR", "instance_key": "W_UNWRITTEN_READ_VAR:var_name=battery_Pmax", "message": "Variable 'battery_Pmax' is read but never written by any action or transition effect.", "policy_action": "budgeted_repair", "pyfcstm_severity": "warning", "rationale": "", "refs": {"init_value": "0.0", "read_states": ["LNGShipEMS.AddDG1LastPriority", "LNGShipEMS.AddDG2LastPriority", "LNGShipEMS.BatteryAssist", "LNGShipEMS.ExtremeO...<truncated 121878 chars>

</details>

<details><summary>Repair 2 / iteration `1` / source `SD-4` / accepted=❌</summary>

#### 为什么进入修复

- selected feedback source：`SD-4`；blocking=`True`；pre_scenario=`True`。
- problem_summary：Variable 'battery_Pmax' is read but never written by any action or transition effect.; Variable 'Plngmax' is read but never written by any action or transition effect.; Variable 'Pd2max' is read but never written by any action or transition effect.
- diagnostic ids：`W_UNWRITTEN_READ_VAR:var_name=battery_Pmax, W_UNWRITTEN_READ_VAR:var_name=Plngmax, W_UNWRITTEN_READ_VAR:var_name=Pd2max, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.RESCoversCharge:to_path=LNGShipEMS.BatteryAssist, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.RESCoversCharge:to_path=LNGShipEMS.LNGDispatch, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.RESCoversCharge:to_path=LNGShipEMS.LNGChargeMargin, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.RESCoversCharge:to_path=LNGShipEMS.LNGDG3Dispatch, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.RESCoversCharge:to_path=LNGShipEMS.LNGDG3ChargeMargin, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.RESCoversCharge:to_path=LNGShipEMS.AddDG1LastPriority, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.RESCoversCharge:to_path=LNGShipEMS.AddDG2LastPriority, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.RESCoversCharge:to_path=LNGShipEMS.ExtremeOverloadBatteryLack, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.RESCoversSpare:to_path=LNGShipEMS.BatteryAssist, ... +92`。
- before_dsl_hash：`sha256:e4cf5afd22c71c13ec6bf27c1372b7fbca62216ddb49195ac0b757d4fe3ed1b9`；candidate_dsl_hash：`sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

#### 错误证据 / diagnostics

- 1. `W_UNWRITTEN_READ_VAR` `W_UNWRITTEN_READ_VAR:var_name=battery_Pmax` policy=`budgeted_repair`：Variable 'battery_Pmax' is read but never written by any action or transition effect.；refs=`{"init_value": "0.0", "read_states": ["LNGShipEMS.AddDG1LastPriority", "LNGShipEMS.AddDG2LastPriority", "LNGShipEMS.BatteryAssist", "LNGShipEMS.ExtremeOverloadBatteryLack", "LNGShipEMS.LNGChargeMargin", "LNGShipEMS.LNGDG3ChargeMargin", "LNGShipEMS.LNGDG3Dispatch", "LNGShipEMS.LNGDispatch", "LNGShipE...<truncated 135 chars>`
- 2. `W_UNWRITTEN_READ_VAR` `W_UNWRITTEN_READ_VAR:var_name=Plngmax` policy=`budgeted_repair`：Variable 'Plngmax' is read but never written by any action or transition effect.；refs=`{"init_value": "0.0", "read_states": ["LNGShipEMS.AddDG1LastPriority", "LNGShipEMS.AddDG2LastPriority", "LNGShipEMS.BatteryAssist", "LNGShipEMS.ExtremeOverloadBatteryLack", "LNGShipEMS.LNGChargeMargin", "LNGShipEMS.LNGDG3ChargeMargin", "LNGShipEMS.LNGDG3Dispatch", "LNGShipEMS.LNGDispatch", "LNGShipE...<truncated 130 chars>`
- 3. `W_UNWRITTEN_READ_VAR` `W_UNWRITTEN_READ_VAR:var_name=Pd2max` policy=`budgeted_repair`：Variable 'Pd2max' is read but never written by any action or transition effect.；refs=`{"init_value": "0.0", "read_states": ["LNGShipEMS.AddDG1LastPriority", "LNGShipEMS.AddDG2LastPriority", "LNGShipEMS.BatteryAssist", "LNGShipEMS.ExtremeOverloadBatteryLack", "LNGShipEMS.LNGChargeMargin", "LNGShipEMS.LNGDG3ChargeMargin", "LNGShipEMS.LNGDG3Dispatch", "LNGShipEMS.LNGDispatch", "LNGShipE...<truncated 129 chars>`
- 4. `W_GUARD_VARS_NEVER_CHANGE` `W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.RESCoversCharge:to_path=LNGShipEMS.BatteryAssist` policy=`budgeted_repair`：Transition guard reads only variables that are never changed by actions or effects.；refs=`{"from_path": "LNGShipEMS.RESCoversCharge", "guard_vars": ["PL", "Ppv", "Pw", "SoC", "battery_Pmax"], "to_path": "LNGShipEMS.BatteryAssist"}`
- 5. `W_GUARD_VARS_NEVER_CHANGE` `W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.RESCoversCharge:to_path=LNGShipEMS.LNGDispatch` policy=`budgeted_repair`：Transition guard reads only variables that are never changed by actions or effects.；refs=`{"from_path": "LNGShipEMS.RESCoversCharge", "guard_vars": ["PL", "Plngmax", "Ppv", "Pw", "SoC", "battery_Pmax"], "to_path": "LNGShipEMS.LNGDispatch"}`
- 6. `W_GUARD_VARS_NEVER_CHANGE` `W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.RESCoversCharge:to_path=LNGShipEMS.LNGChargeMargin` policy=`budgeted_repair`：Transition guard reads only variables that are never changed by actions or effects.；refs=`{"from_path": "LNGShipEMS.RESCoversCharge", "guard_vars": ["PL", "Pgmax", "Plngmax", "Ppv", "Pw", "SoC"], "to_path": "LNGShipEMS.LNGChargeMargin"}`
- 7. `W_GUARD_VARS_NEVER_CHANGE` `W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.RESCoversCharge:to_path=LNGShipEMS.LNGDG3Dispatch` policy=`budgeted_repair`：Transition guard reads only variables that are never changed by actions or effects.；refs=`{"from_path": "LNGShipEMS.RESCoversCharge", "guard_vars": ["PL", "Plngmax", "Ppv", "Pw", "SoC", "eng3_Pmax"], "to_path": "LNGShipEMS.LNGDG3Dispatch"}`
- 8. `W_GUARD_VARS_NEVER_CHANGE` `W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.RESCoversCharge:to_path=LNGShipEMS.LNGDG3ChargeMargin` policy=`budgeted_repair`：Transition guard reads only variables that are never changed by actions or effects.；refs=`{"from_path": "LNGShipEMS.RESCoversCharge", "guard_vars": ["PL", "Pd1max", "Plngmax", "Ppv", "Pw", "SoC", "eng3_Pmax"], "to_path": "LNGShipEMS.LNGDG3ChargeMargin"}`
- ……另有 `91` 条 evidence 见 run record。

#### 变量角色与上下文提示

- policy：Advisory only. Do not invent writes for external_input_candidate variables unless NL explicitly gives update semantics; add meaningful NL-grounded writes only for internal state variables.
- source：SD-4 diagnostic refs and generic NL external-input rationale

| Variable | role_hint | nl_token_present | diagnostics |
|---|---|---:|---|
| `PL` | `external_input_candidate` | ✅ | `W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +140` |
| `Pd1max` | `external_input_candidate` | ✅ | `W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +44` |
| `Pd2max` | `unknown` | ❌ | `W_UNWRITTEN_READ_VAR, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +20` |
| `Pgmax` | `external_input_candidate` | ✅ | `W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +8` |
| `Plngmax` | `unknown` | ❌ | `W_UNWRITTEN_READ_VAR, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +80` |
| `Ppv` | `external_input_candidate` | ✅ | `W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +116` |
| `Pw` | `external_input_candidate` | ✅ | `W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +116` |
| `SoC` | `external_input_candidate` | ✅ | `W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +104` |
| `battery_Pmax` | `unknown` | ❌ | `W_UNWRITTEN_READ_VAR, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +20` |
| `battery_charging_power` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `battery_discharge_power` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `cut_in_DG1` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `cut_in_DG2` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `cut_in_DG3` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `cut_in_LNG` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `cut_in_load` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `cut_out_DG1` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `cut_out_DG2` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `cut_out_DG3` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `cut_out_LNG` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `cut_out_load` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `eng3_Pmax` | `external_input_candidate` | ✅ | `W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +56` |
| `illegal_overload` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `requested_generator_power` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `spare_power` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |

#### SD-8 FixRequestBatch / 修改请求

- batch_id：`fixbatch-1-sha256-a1a5d6e0aa8`；source_stage=`SD-4`；legacy_plan_kind=`FixPlan`；requests=`12`。

| request_id | severity | hard | waiver | problem | evidence |
|---|---|---:|---:|---|---|
| `fixreq-1-sd4-0-75b9296ee2` | `blocking_warning` | ❌ | ✅ | Variable 'battery_Pmax' is read but never written by any action or transition effect.; Variable 'Plngmax' is read but never written by any action or transition effect.; Variable 'Pd2max' is read but never written by any ...<truncated 28 chars> | `W_UNWRITTEN_READ_VAR` |
| `fixreq-1-sd4-1-1d359b61ba` | `blocking_warning` | ❌ | ✅ | Variable 'battery_Pmax' is read but never written by any action or transition effect.; Variable 'Plngmax' is read but never written by any action or transition effect.; Variable 'Pd2max' is read but never written by any ...<truncated 28 chars> | `W_UNWRITTEN_READ_VAR` |
| `fixreq-1-sd4-2-87428d820c` | `blocking_warning` | ❌ | ✅ | Variable 'battery_Pmax' is read but never written by any action or transition effect.; Variable 'Plngmax' is read but never written by any action or transition effect.; Variable 'Pd2max' is read but never written by any ...<truncated 28 chars> | `W_UNWRITTEN_READ_VAR` |
| `fixreq-1-sd4-3-0dca8d0e29` | `blocking_warning` | ❌ | ✅ | Variable 'battery_Pmax' is read but never written by any action or transition effect.; Variable 'Plngmax' is read but never written by any action or transition effect.; Variable 'Pd2max' is read but never written by any ...<truncated 28 chars> | `W_GUARD_VARS_NEVER_CHANGE` |
| `fixreq-1-sd4-4-9e0c92746d` | `blocking_warning` | ❌ | ✅ | Variable 'battery_Pmax' is read but never written by any action or transition effect.; Variable 'Plngmax' is read but never written by any action or transition effect.; Variable 'Pd2max' is read but never written by any ...<truncated 28 chars> | `W_GUARD_VARS_NEVER_CHANGE` |
| `fixreq-1-sd4-5-bfdc977592` | `blocking_warning` | ❌ | ✅ | Variable 'battery_Pmax' is read but never written by any action or transition effect.; Variable 'Plngmax' is read but never written by any action or transition effect.; Variable 'Pd2max' is read but never written by any ...<truncated 28 chars> | `W_GUARD_VARS_NEVER_CHANGE` |
| `fixreq-1-sd4-6-3fedd329d1` | `blocking_warning` | ❌ | ✅ | Variable 'battery_Pmax' is read but never written by any action or transition effect.; Variable 'Plngmax' is read but never written by any action or transition effect.; Variable 'Pd2max' is read but never written by any ...<truncated 28 chars> | `W_GUARD_VARS_NEVER_CHANGE` |
| `fixreq-1-sd4-7-4453eac848` | `blocking_warning` | ❌ | ✅ | Variable 'battery_Pmax' is read but never written by any action or transition effect.; Variable 'Plngmax' is read but never written by any action or transition effect.; Variable 'Pd2max' is read but never written by any ...<truncated 28 chars> | `W_GUARD_VARS_NEVER_CHANGE` |
| `fixreq-1-sd4-8-a282748588` | `blocking_warning` | ❌ | ✅ | Variable 'battery_Pmax' is read but never written by any action or transition effect.; Variable 'Plngmax' is read but never written by any action or transition effect.; Variable 'Pd2max' is read but never written by any ...<truncated 28 chars> | `W_GUARD_VARS_NEVER_CHANGE` |
| `fixreq-1-sd4-9-b735f5be23` | `blocking_warning` | ❌ | ✅ | Variable 'battery_Pmax' is read but never written by any action or transition effect.; Variable 'Plngmax' is read but never written by any action or transition effect.; Variable 'Pd2max' is read but never written by any ...<truncated 28 chars> | `W_GUARD_VARS_NEVER_CHANGE` |
- ……另有 `2` 个 request 见 run record。

#### SD-8 legacy fix plan / 修改建议

- recommended_strategy：Use diagnostics as hints; choose the smallest globally consistent repair.；Before returning a candidate, verify every required_preserve_element_id still has a concrete DSL representation.
- hint 1：The variable is used as input but never updated after its initial definition, so model behavior may be accidentally constant.；`actions=add_write, simplify_guard；do_not=Do not add a meaningless self-assignment.`
- hint 2：The variable is used as input but never updated after its initial definition, so model behavior may be accidentally constant.；`actions=add_write, simplify_guard；do_not=Do not add a meaningless self-assignment.`
- hint 3：The variable is used as input but never updated after its initial definition, so model behavior may be accidentally constant.；`actions=add_write, simplify_guard；do_not=Do not add a meaningless self-assignment.`
- hint 4：This guard is controlled only by initial variable values. If those values never change, the transition condition is effectively fixed.；`actions=add_write, simplify_guard；do_not=Do not add a meaningless self-assignment; it does not model a real change., Do not rewrite the guard to a meaningless constant only to silence this diagnostic.`
- hint 5：This guard is controlled only by initial variable values. If those values never change, the transition condition is effectively fixed.；`actions=add_write, simplify_guard；do_not=Do not add a meaningless self-assignment; it does not model a real change., Do not rewrite the guard to a meaningless constant only to silence this diagnostic.`
- hint 6：This guard is controlled only by initial variable values. If those values never change, the transition condition is effectively fixed.；`actions=add_write, simplify_guard；do_not=Do not add a meaningless self-assignment; it does not model a real change., Do not rewrite the guard to a meaningless constant only to silence this diagnostic.`
- forbidden_edits：`Do not delete grounded required elements merely to silence diagnostics., Do not invent internal plant/environment dynamics merely to make external input variables appear written.`。
- required_preserve_element_ids：`state:RESCoversCharge, state:RESCoversSpare, state:ZeroLoadCharge, state:ZeroLoadSpare, state:BatteryAssist, state:LNGDispatch, state:LNGChargeMargin, state:LNGDG3Dispatch, state:LNGDG3ChargeMargin, state:AddDG1LastPriority, state:AddDG2LastPriority, state:ExtremeOverloadBatteryLack, ... +20`。

#### SL-9 per-request 决策

- accepted_request_ids：`<derived-from-table>`；candidate_len=`0`。

| request_id | decision | waiver | rework_locked | rationale / intent |
|---|---|---:|---:|---|
| `fixreq-1-sd4-0-75b9296ee2` | `reject` | ✅ | ❌ | battery_Pmax is an NL-grounded capacity/input bound used to classify whether battery assist can cover the residual demand. The NL says the FSM reads capacity bounds and does not define an internal update rule. Adding a write would invent plant dynamics, and this same issue was already waived in FixLog with no new evidence. |
| `fixreq-1-sd4-1-1d359b61ba` | `reject` | ✅ | ❌ | Plngmax is an externally supplied LNG capacity bound. It is intentionally read by dispatch guards and actions; the NL provides no meaningful FSM-side update. The prior FixLog already waived this warning, and the new batch provides no new evidence requiring a DSL change. |
| `fixreq-1-sd4-2-87428d820c` | `reject` | ✅ | ❌ | Pd2max is an externally supplied diesel-generator capacity bound used in the DG2 last-priority and extreme-overload branches. Writing it internally would be ungrounded. This request repeats a previously waived issue without new evidence. |
| `fixreq-1-sd4-3-0dca8d0e29` | `reject` | ✅ | ❌ | The BatteryAssist guard is intentionally controlled by external/time-varying inputs PL, Ppv, Pw, SoC and the capacity bound battery_Pmax. The NL explicitly says the FSM reads these values as inputs. Adding dummy writes or simplifying the guard would reduce NL fidelity, and the same warning was previously waived. |
| `fixreq-1-sd4-4-9e0c92746d` | `reject` | ✅ | ❌ | The LNGDispatch guard implements the NL dispatch condition over residual demand, battery capacity, SoC, and LNG capacity. All guard variables are external inputs or capacity parameters with no NL update semantics. Prior SL-10 override treated this as an audit-only local objection. |
| `fixreq-1-sd4-5-bfdc977592` | `reject` | ✅ | ❌ | The LNGChargeMargin guard is required for the low-SoC branch with Pgmax/5 charging margin. Its variables are NL-grounded demand/resource/capacity inputs. No safe internal write exists, and changing the guard would risk deleting a required branch. |
| `fixreq-1-sd4-6-3fedd329d1` | `reject` | ✅ | ❌ | The LNGDG3Dispatch guard uses residual demand and engine/LNG capacity bounds including eng3_Pmax, matching the NL requirement to use capacity bounds for dispatch. The guard-never-change warning is conservative for this input-classification FSM and was previously waived. |
| `fixreq-1-sd4-7-4453eac848` | `reject` | ✅ | ❌ | The LNGDG3ChargeMargin guard is an NL-required low-SoC diesel-generator charging-margin branch using Pd1max/10 and capacity bounds. Adding writes to external inputs would invent dynamics, while simplifying the guard would reduce coverage. |
| `fixreq-1-sd4-8-a282748588` | `reject` | ✅ | ❌ | The AddDG1LastPriority guard implements the required last-priority DG1 dispatch branch. Its variables are demand, renewable contributions, and capacity bounds read from the environment/system configuration. No NL-grounded repair exists beyond waiver. |
| `fixreq-1-sd4-9-b735f5be23` | `reject` | ✅ | ❌ | The AddDG2LastPriority guard implements the required last-priority DG2 branch and depends on externally supplied capacity bounds including Pd2max. A dummy write or constant rewrite is forbidden and would degrade the model. |
| `fixreq-1-sd4-10-619e4b70df` | `reject` | ✅ | ❌ | The ExtremeOverloadBatteryLack guard is required by the overload requirement: when demand exceeds all RES and thermal resources, all thermal units are activated and the lack is covered by battery discharge. Its guard variables are external inputs/capacity bounds, and the prior ledger already waived the warning. |
| `fixreq-1-sd4-11-0313b6d425` | `reject` | ✅ | ❌ | The RESCoversSpare-to-BatteryAssist guard is another instance of the same NL-grounded dynamic dispatch classification over external demand/resource/SoC/capacity inputs. No new hard evidence or scenario regression reopens the prior waiver. |
- repair_rationale：All current requests repeat design warnings already rejected/waived in the FixLog and explicitly overridden by SL-10 as audit-only local objections.；The variables battery_Pmax, Plngmax, Pd2max, PL, Ppv, Pw, SoC, Pgmax, eng3_Pmax, and Pd1max are NL-grounded external inputs or capacity bounds used by a guard-driven dispatch classifier. The NL says the FSM reads these values; it does not d...<truncated 32 chars>；The smallest safe action is therefore no DSL edit. Adding writes would violate the forbidden edit against inventing plant/environment dynamics, while simplifying/removing guards would break required states and dispatch branches.；Because every current request is rejected/waived and no request is accepted, the SL-9 contract requires candidate_dsl to remain empty rather than returning an unchanged DSL candidate.
- diff_summary：`{"summary": "No DSL edit produced. All twelve requests are waived/rejected as repeated external-input/capacity-bound warnings with no new actionable evidence."}`。

#### SL-9 candidate / 最终修改执行方案

- 本 repair 未记录 candidate_dsl。

#### Candidate diff（before -> candidate）

- 无 candidate DSL，因此无法生成 diff。

#### SL-10 审查结果

- SL-10：`<none>`（旧 record 或本 run 未进入 LLM repair review）。
- legacy repair_review：ok=`True`，target_resolved=`True`，regression_detected=`False`，drift_risk=`minor`。

</details>

<details><summary>Repair 3 / iteration `2` / source `SD-6` / accepted=✅</summary>

#### 为什么进入修复

- selected feedback source：`SD-6`；blocking=`True`；pre_scenario=`False`。
- problem_summary：simulation failed
- diagnostic ids：`default_init_zero_load_charge`。
- before_dsl_hash：`sha256:e4cf5afd22c71c13ec6bf27c1372b7fbca62216ddb49195ac0b757d4fe3ed1b9`；candidate_dsl_hash：`sha256:9121b16d876b7385b65d3cf1f8060acd9e094046ce82de945e480c492432fa20`。

#### 错误证据 / diagnostics

- 1. `<unknown>` `` policy=``：

#### SD-8 FixRequestBatch / 修改请求

- batch_id：`fixbatch-2-sha256-83f4e7b3696`；source_stage=`SD-6`；legacy_plan_kind=`FixPlan`；requests=`1`。

| request_id | severity | hard | waiver | problem | evidence |
|---|---|---:|---:|---|---|
| `fixreq-2-sd6-0-99efbfa439` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'default-init: with PL=0 and SoC below 0.95, the EMS should classify zero load RES into battery charging and cut out ship load.', 'name': 'default_init_zero_load_charge', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'default-init: with PL=0 and SoC below 0.95, the EMS should classify zero load RES into battery charging and cut out ship load.', 'failing_steps': [{'actual_state': 'LNGShipEMS.RESCoversCharge', 'actual_vars_focus': {'battery_charging_power': 15.0, 'battery_discharge_power': 0.0, 'cut_in_LNG': 0, 'cut_in_load': 1, 'cut_out_LNG': 1, 'cut_out_load': 0, 'requested_generator_power': 0.0, 'spare_power': 0.0}, 'before_cycles': 0, 'events': [], 'expected_state': 'LNGShipEMS.ZeroLoadCharge', 'expected_vars': {'battery_charging_power': 15.0, 'battery_discharge_power': 0.0, 'cut_in_LNG': 0, 'cut_in_load': 0, 'cut_out_LNG': 1, 'cut_out_load': 1, 'requested_generator_power': 0.0, 'spare_power': 0.0}, 'runtime_error': '', 'state_assertion_ok': False, 'step_index': 0, 'step_name': 'zero_load_low_soc_charges_battery', 'var_assertion_ok': False, 'var_mismatches': {'cut_in_load': {'actual': 1, 'expected': 0}, 'cut_out_load': {'actual': 0, 'expected': 1}}}], 'initial_state': None, 'initial_vars': {'PL': 0.0, 'Ppv': 10.0, 'Pw': 5.0, 'SoC': 0.5}, 'scenario_name': 'default_init_zero_load_charge', 'status': 'fail'}, 'setup_error': None, 'status': 'fail', 'step_results': [{'actual_state': 'LNGShipEMS.RESCoversCharge', 'actual_vars': {'PL': 0.0, 'Pd1max': 0.0, 'Pd2max': 0.0, 'Pgmax': 0.0, 'Plngmax': 0.0, 'Ppv': 10.0, 'Pw': 5.0, 'SoC': 0.5, 'battery_Pmax': 0.0, 'battery_charging_power': 15.0, 'battery_discharge_power': 0.0, 'cut_in_DG1': 0, 'cut_in_DG2': 0, 'cut_in_DG3': 0, 'cut_in_LNG': 0, 'cut_in_load': 1, 'cut_out_DG1': 1, 'cut_out_DG2': 1, 'cut_out_DG3': 1, 'cut_out_LNG': 1, 'cut_out_load': 0, 'eng3_Pmax': 0.0, 'illegal_overload': 0, 'requested_generator_power': 0.0, 'spare_power': 0.0}, 'runtime_error': None, 'state_assertion_ok': False, 'status': 'fail', 'step_index': 0, 'step_name': 'zero_load_low_soc_charges_battery', 'var_assertion_ok': False, 'var_mismatches': {'cut_in_load': {'actual': 1, 'expected': 0}, 'cut_out_load': {'actual': 0, 'expected': 1}}}]}` |

#### SD-8 legacy fix plan / 修改建议

- recommended_strategy：Use diagnostics as hints; choose the smallest globally consistent repair.；Before returning a candidate, verify every required_preserve_element_id still has a concrete DSL representation.
- forbidden_edits：`Do not delete grounded required elements merely to silence diagnostics., Do not invent internal plant/environment dynamics merely to make external input variables appear written.`。
- required_preserve_element_ids：`state:RESCoversCharge, state:RESCoversSpare, state:ZeroLoadCharge, state:ZeroLoadSpare, state:BatteryAssist, state:LNGDispatch, state:LNGChargeMargin, state:LNGDG3Dispatch, state:LNGDG3ChargeMargin, state:AddDG1LastPriority, state:AddDG2LastPriority, state:ExtremeOverloadBatteryLack, ... +20`。

#### SL-9 per-request 决策

- accepted_request_ids：`<derived-from-table>`；candidate_len=`10454`。

| request_id | decision | waiver | rework_locked | rationale / intent |
|---|---|---:|---:|---|
| `fixreq-2-sd6-0-99efbfa439` | `accept` | ❌ | ❌ | The failing scenario default_init_zero_load_charge initializes PL=0.0, Ppv=10.0, Pw=5.0, SoC=0.5 and expects the first default-init cycle to classify into LNGShipEMS.ZeroLoadCharge with cut_in_load=0 and cut_out_load=1. The actual state was LNGShipEMS.RESCoversCharge because the root initial transition was hardwired to RESCoversCharge before the guard-driven...<truncated 610 chars> |
- repair_rationale：Accepted fixreq-2-sd6-0-99efbfa439 because it is new hard simulation evidence, not a previously waived local-only warning.；Scenario default_init_zero_load_charge expected LNGShipEMS.ZeroLoadCharge for PL=0.0, Ppv=10.0, Pw=5.0, SoC=0.5, with battery_charging_power=15.0, cut_in_load=0, and cut_out_load=1. The actual run entered LNGShipEMS.RESCoversCharge, which c...<truncated 81 chars>；The edit preserves the existing ZeroLoadCharge state action that already sets requested_generator_power=0.0, battery_discharge_power=0.0, battery_charging_power=Ppv+Pw, spare_power=0.0, cut_in_load=0, cut_out_load=1, cut_in_LNG=0, and cut_o...<truncated 9 chars>；The root initial transition now routes through a pseudo selector with the same guarded classification rules as the existing forced dynamic transitions. This fixes first-cycle default-init classification without deleting or weakening the exi...<truncated 72 chars>；All required preserve elements remain represented: the twelve finite states, the required variables and outputs, the RES cover guards, zero-load guards, dispatch priority guards, and the ExtremeOverloadBatteryLack guard/action are retained.
- diff_summary：`{"summary": "Changed the root initial transition from a fixed [*] -> RESCoversCharge to [*] -> InitialDispatchSelect, added pseudo state InitialDispatchSelect, and added guarded outgoing transitions from that pseudo state to the same twelve dispatch states using the existing NL-grounded classification conditions. No variables, required states, state actions, forced dynamic transitions, or dispatch outputs were removed."}`。

#### SL-9 candidate / 最终修改执行方案

```pyfcstm
def float PL = 0.0;
def float Ppv = 0.0;
def float Pw = 0.0;
def float SoC = 0.0;
def float battery_Pmax = 0.0;
def float Plngmax = 0.0;
def float eng3_Pmax = 0.0;
def float Pgmax = 0.0;
def float Pd1max = 0.0;
def float Pd2max = 0.0;
def float requested_generator_power = 0.0;
def float battery_discharge_power = 0.0;
def float battery_charging_power = 0.0;
def float spare_power = 0.0;
def int cut_in_LNG = 0;
def int cut_out_LNG = 0;
def int cut_in_DG1 = 0;
def int cut_out_DG1 = 0;
def int cut_in_DG2 = 0;
def int cut_out_DG2 = 0;
def int cut_in_DG3 = 0;
def int cut_out_DG3 = 0;
def int cut_in_load = 0;
def int cut_out_load = 0;
def int illegal_overload = 0;

state LNGShipEMS {
    ! * -> ZeroLoadCharge : if [PL == 0 && SoC < 0.95];
    ! * -> ZeroLoadSpare : if [PL == 0 && SoC >= 0.95];
    ! * -> RESCoversCharge : if [PL > 0 && Ppv + Pw >= PL && SoC < 0.95];
    ! * -> RESCoversSpare : if [PL > 0 && Ppv + Pw >= PL && SoC >= 0.95];
    ! * -> BatteryAssist : if [PL > 0 && Ppv + Pw < PL && SoC > 0.20 && PL - Ppv - Pw <= battery_Pmax];
    ! * -> LNGDispatch : if [PL > 0 && Ppv + Pw < PL && SoC > 0.20 && PL - Ppv - Pw > battery_Pmax && PL - Ppv - Pw <= Plngmax];
    ! * -> LNGChargeMargin : if [PL > 0 && Ppv + Pw < PL && SoC <= 0.20 && PL - Ppv - Pw + Pgmax / 5 <= Plngmax];
    ! * -> LNGDG3Dispatch : if [PL > 0 && Ppv + Pw < PL && SoC > 0.20 && PL - Ppv - Pw > Plngmax && PL - Ppv - Pw <= Plngmax + eng3_Pmax];
    ! * -> LNGDG3ChargeMargin : if [PL > 0 && Ppv + Pw < PL && SoC <= 0.20 && PL - Ppv - Pw + Pd1max / 10 > Plngmax && PL - Ppv - Pw + Pd1max / 10 <= Plngmax + eng3_Pmax];
    ! * -> AddDG1LastPriority : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > Plngmax + eng3_Pmax && PL - Ppv - Pw <= Plngmax + eng3_Pmax + Pd1max];
    ! * -> AddDG2LastPriority : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > Plngmax + eng3_Pmax + Pd1max && PL - Ppv - Pw <= Plngmax + eng3_Pmax + Pd1max + Pd2max];
    ! * -> ExtremeOverloadBatteryLack : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > Plngmax + eng3_Pmax + Pd1max + Pd2max];

    [*] -> InitialDispatchSelect;

    pseudo state InitialDispatchSelect;

    state RESCoversCharge {
        enter {
            requested_generator_power = 0.0;
            battery_discharge_power = 0.0;
            battery_charging_power = Ppv + Pw - PL;
            spare_power = 0.0;
            cut_in_LNG = 0;
            cut_out_LNG = 1;
            cut_in_DG1 = 0;
            cut_out_DG1 = 1;
            cut_in_DG2 = 0;
            cut_out_DG2 = 1;
            cut_in_DG3 = 0;
            cut_out_DG3 = 1;
            cut_in_load = 1;
            cut_out_load = 0;
            illegal_overload = 0;
        }
    }

    state RESCoversSpare {
        enter {
            requested_generator_power = 0.0;
            battery_discharge_power = 0.0;
            battery_charging_power = 0.0;
            spare_power = Ppv + Pw - PL;
            cut_in_LNG = 0;
            cut_out_LNG = 1;
            cut_in_DG1 = 0;
            cut_out_DG1 = 1;
            cut_in_DG2 = 0;
            cut_out_DG2 = 1;
            cut_in_DG3 = 0;
            cut_out_DG3 = 1;
            cut_in_load = 1;
            cut_out_load = 0;
            illegal_overload = 0;
        }
    }

    state ZeroLoadCharge {
        enter {
            requested_generator_power = 0.0;
            battery_discharge_power = 0.0;
            battery_charging_power = Ppv + Pw;
            spare_power = 0.0;
            cut_in_LNG = 0;
            cut_out_LNG = 1;
            cut_in_DG1 = 0;
            cut_out_DG1 = 1;
            cut_in_DG2 = 0;
            cut_out_DG2 = 1;
            cut_in_DG3 = 0;
            cut_out_DG3 = 1;
            cut_in_load = 0;
            cut_out_load = 1;
            illegal_overload = 0;
        }
    }

    state ZeroLoadSpare {
        enter {
            requested_generator_power = 0.0;
            battery_discharge_power = 0.0;
            battery_charging_power = 0.0;
            spare_power = Ppv + Pw;
            cut_in_LNG = 0;
            cut_out_LNG = 1;
            cut_in_DG1 = 0;
            cut_out_DG1 = 1;
            cut_in_DG2 = 0;
            cut_out_DG2 = 1;
            cut_in_DG3 = 0;
            cut_out_DG3 = 1;
            cut_in_load = 0;
            cut_out_load = 1;
            illegal_overload = 0;
        }
    }

    state BatteryAssist {
        enter {
            requested_generator_power = 0.0;
            battery_discharge_power = PL - Ppv - Pw;
            battery_charging_power = 0.0;
            spare_power = 0.0;
            cut_in_LNG = 0;
            cut_out_LNG = 1;
            cut_in_DG1 = 0;
            cut_out_DG1 = 1;
            cut_in_DG2 = 0;
            cut_out_DG2 = 1;
            cut_in_DG3 = 0;
            cut_out_DG3 = 1;
            cut_in_load = 1;
            cut_out_load = 0;
            illegal_overload = 0;
        }
    }

    state LNGDispatch {
        enter {
            requested_generator_power = PL - Ppv - Pw;
            battery_discharge_power = 0.0;
            battery_charging_power = 0.0;
            spare_power = 0.0;
            cut_in_LNG = 1;
            cut_out_LNG = 0;
            cut_in_DG1 = 0;
            cut_out_DG1 = 1;
            cut_in_DG2 = 0;
            cut_out_DG2 = 1;
            cut_in_DG3 = 0;
            cut_out_DG3 = 1;
            cut_in_load = 1;
            cut_out_load = 0;
            illegal_overload = 0;
        }
    }

    state LNGChargeMargin {
        enter {
            requested_generator_power = PL - Ppv - Pw + Pgmax / 5;
            battery_discharge_power = 0.0;
            battery_charging_power = Pgmax / 5;
            spare_power = 0.0;
            cut_in_LNG = 1;
            cut_out_LNG = 0;
            cut_in_DG1 = 0;
            cut_out_DG1 = 1;
            cut_in_DG2 = 0;
            cut_out_DG2 = 1;
            cut_in_DG3 = 0;
            cut_out_DG3 = 1;
            cut_in_load = 1;
            cut_out_load = 0;
            illegal_overload = 0;
        }
    }

    state LNGDG3Dispatch {
        enter {
            requested_generator_power = PL - Ppv - Pw;
            battery_discharge_power = 0.0;
            battery_charging_power = 0.0;
            spare_power = 0.0;
            cut_in_LNG = 1;
            cut_out_LNG = 0;
            cut_in_DG1 = 0;
            cut_out_DG1 = 1;
            cut_in_DG2 = 0;
            cut_out_DG2 = 1;
            cut_in_DG3 = 1;
            cut_out_DG3 = 0;
            cut_in_load = 1;
            cut_out_load = 0;
            illegal_overload = 0;
        }
    }

    state LNGDG3ChargeMargin {
        enter {
            requested_generator_power = PL - Ppv - Pw + Pd1max / 10;
            battery_discharge_power = 0.0;
            battery_charging_power = Pd1max / 10;
            spare_power = 0.0;
            cut_in_LNG = 1;
            cut_out_LNG = 0;
            cut_in_DG1 = 0;
            cut_out_DG1 = 1;
            cut_in_DG2 = 0;
            cut_out_DG2 = 1;
            cut_in_DG3 = 1;
            cut_out_DG3 = 0;
            cut_in_load = 1;
            cut_out_load = 0;
            illegal_overload = 0;
        }
    }

    state AddDG1LastPriority {
        enter {
            requested_generator_power = PL - Ppv - Pw;
            battery_discharge_power = 0.0;
            battery_charging_power = 0.0;
            spare_power = 0.0;
            cut_in_LNG = 1;
            cut_out_LNG = 0;
            cut_in_DG1 = 1;
            cut_out_DG1 = 0;
            cut_in_DG2 = 0;
            cut_out_DG2 = 1;
            cut_in_DG3 = 1;
            cut_out_DG3 = 0;
            cut_in_load = 1;
            cut_out_load = 0;
            illegal_overload = 0;
        }
    }

    state AddDG2LastPriority {
        enter {
            requested_generator_power = PL - Ppv - Pw;
            battery_discharge_power = 0.0;
            battery_charging_power = 0.0;
            spare_power = 0.0;
            cut_in_LNG = 1;
            cut_out_LNG = 0;
            cut_in_DG1 = 1;
            cut_out_DG1 = 0;
            cut_in_DG2 = 1;
            cut_out_DG2 = 0;
            cut_in_DG3 = 1;
            cut_out_DG3 = 0;
            cut_in_load = 1;
            cut_out_load = 0;
            illegal_overload = 0;
        }
    }

    state ExtremeOverloadBatteryLack {
        enter {
            requested_generator_power = Plngmax + eng3_Pmax + Pd1max + Pd2max;
            battery_discharge_power = PL - Ppv - Pw - Plngmax - eng3_Pmax - Pd1max - Pd2max;
            battery_charging_power = 0.0;
            spare_power = 0.0;
            cut_in_LNG = 1;
            cut_out_LNG = 0;
            cut_in_DG1 = 1;
            cut_out_DG1 = 0;
            cut_in_DG2 = 1;
            cut_out_DG2 = 0;
            cut_in_DG3 = 1;
            cut_out_DG3 = 0;
            cut_in_load = 1;
            cut_out_load = 0;
            illegal_overload = 1;
        }
    }

    InitialDispatchSelect -> ZeroLoadCharge : if [PL == 0 && SoC < 0.95];
    InitialDispatchSelect -> ZeroLoadSpare : if [PL
... <truncated 1454 chars; see run record>
```

#### Candidate diff（before -> candidate）

```diff
--- before.fcstm
+++ candidate.fcstm
@@ -38,7 +38,9 @@
     ! * -> AddDG2LastPriority : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > Plngmax + eng3_Pmax + Pd1max && PL - Ppv - Pw <= Plngmax + eng3_Pmax + Pd1max + Pd2max];
     ! * -> ExtremeOverloadBatteryLack : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > Plngmax + eng3_Pmax + Pd1max + Pd2max];
 
-    [*] -> RESCoversCharge;
+    [*] -> InitialDispatchSelect;
+
+    pseudo state InitialDispatchSelect;
 
     state RESCoversCharge {
         enter {
@@ -279,4 +281,17 @@
             illegal_overload = 1;
         }
     }
+
+    InitialDispatchSelect -> ZeroLoadCharge : if [PL == 0 && SoC < 0.95];
+    InitialDispatchSelect -> ZeroLoadSpare : if [PL == 0 && SoC >= 0.95];
+    InitialDispatchSelect -> RESCoversCharge : if [PL > 0 && Ppv + Pw >= PL && SoC < 0.95];
+    InitialDispatchSelect -> RESCoversSpare : if [PL > 0 && Ppv + Pw >= PL && SoC >= 0.95];
+    InitialDispatchSelect -> BatteryAssist : if [PL > 0 && Ppv + Pw < PL && SoC > 0.20 && PL - Ppv - Pw <= battery_Pmax];
+    InitialDispatchSelect -> LNGDispatch : if [PL > 0 && Ppv + Pw < PL && SoC > 0.20 && PL - Ppv - Pw > battery_Pmax && PL - Ppv - Pw <= Plngmax];
+    InitialDispatchSelect -> LNGChargeMargin : if [PL > 0 && Ppv + Pw < PL && SoC <= 0.20 && PL - Ppv - Pw + Pgmax / 5 <= Plngmax];
+    InitialDispatchSelect -> LNGDG3Dispatch : if [PL > 0 && Ppv + Pw < PL && SoC > 0.20 && PL - Ppv - Pw > Plngmax && PL - Ppv - Pw <= Plngmax + eng3_Pmax];
+    InitialDispatchSelect -> LNGDG3ChargeMargin : if [PL > 0 && Ppv + Pw < PL && SoC <= 0.20 && PL - Ppv - Pw + Pd1max / 10 > Plngmax && PL - Ppv - Pw + Pd1max / 10 <= Plngmax + eng3_Pmax];
+    InitialDispatchSelect -> AddDG1LastPriority : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > Plngmax + eng3_Pmax && PL - Ppv - Pw <= Plngmax + eng3_Pmax + Pd1max];
+    InitialDispatchSelect -> AddDG2LastPriority : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > Plngmax + eng3_Pmax + Pd1max && PL - Ppv - Pw <= Plngmax + eng3_Pmax + Pd1max + Pd2max];
+    InitialDispatchSelect -> ExtremeOverloadBatteryLack : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > Plngmax + eng3_Pmax + Pd1max + Pd2max];
 }
```

#### SL-10 审查结果

- SL-10 decision=`pass`，ok=`True`，target_resolved=`True`，regression_detected=`False`，drift_risk=`minor`。
- SL-10 review_meta：schema=`SL10RepairReviewOutput.v1`，failure_policy=`fail_closed`，replay_key=`SL-10:sha256:b8a1f1dbbefb05f12811f8236baf919ab70a5d9019fa8b71802caada526a1e73`。
  - SL-10 evidence 1: `{"summary": "The hard simulation request fixreq-2-sd6-0-99efbfa439 is substantively resolved by the candidate DSL. The failing scenario default_init_zero_load_charge initialized PL=0.0, Ppv=10.0, Pw=5.0, SoC=0.5 and expected LNGShipEMS.ZeroLoadCharge with requested_generator_power=0.0, battery_discharge_power=0.0, battery_charging_power=15.0, spare_power=0.0, cut_in_load=0, cut_out_load=1, cut_in_LNG=0, and cut_out_LNG=1. The old DSL entered RESCoversCharge because the root initial transition was hardwired to RESCoversCharge, producing the right charging power but wrong load cut commands. The candidate replaces that fixed initial target with InitialDispatchSelect and routes PL == 0 && SoC < ...<truncated 80 chars>`
  - SL-10 evidence 2: `{"summary": "The DSL diff is targeted: [*] -> RESCoversCharge is changed to [*] -> InitialDispatchSelect, a pseudo selector is added, and twelve guarded outgoing selector transitions mirror the existing dispatch classification guards. No NL-required output variables, capacity/input variables, cut-in/cut-out commands, state actions, forced dynamic transitions, or dispatch states are removed."}`
  - SL-10 evidence 3: `{"summary": "The NL requires twelve finite dispatch states selected by logical conditions over demand, renewable generation, capacity, and SoC. The candidate preserves all twelve required finite states: RESCoversCharge, RESCoversSpare, ZeroLoadCharge, ZeroLoadSpare, BatteryAssist, LNGDispatch, LNGChargeMargin, LNGDG3Dispatch, LNGDG3ChargeMargin, AddDG1LastPriority, AddDG2LastPriority, and ExtremeOverloadBatteryLack. The added InitialDispatchSelect is a pseudo routing state rather than a replacement for or deletion of any required finite state."}`
  - SL-10 evidence 4: `{"summary": "The candidate preserves NL dispatch fidelity: zero-load branches route RES to charging or spare by SoC threshold; RES-covered nonzero load branches charge or spare by SoC 0.95; deficit branches maintain RES-first, battery-when-suitable, LNG-before-diesel, DG1/DG2-last-priority behavior; low-SoC charging margins Pgmax/5 and Pd1max/10 remain; and the extreme overload branch still activates all thermal units, discharges the battery lack, and marks illegal_overload."}`
  - SL-10 evidence 5: `{"summary": "The complete FixLog shows that earlier local design warnings about unwritten external inputs/capacity bounds and guard variables that never change were deliberately waived and then overridden by SL-10 because the NL describes PL, Ppv, Pw, SoC, battery_Pmax, Plngmax, Pgmax, Pd1max, Pd2max, and eng3_Pmax as read inputs or capacity bounds, not internally updated plant dynamics. The current accepted SL-9 edit does not reopen those waived issues by adding dummy writes or simplifying required guards."}`
  - SL-10 evidence 6: `{"summary": "Local deterministic evidence reports no scenario regression and no semantic runtime error, but rejects on new InitialDispatchSelect guard-never-change diagnostics and forced_transition_count_drift. Those are structural/design objections arising from the intentional pseudo selector, not evidence that the hard simulation scenario remains behaviorally wrong."}`
- local checks evidence：stage=`SD-10`；note=PR-E1 uses local parse/semantic/design/sim checks as SL-10 evidence, not as the final deterministic judge.。
  - local ok=`False`，target_resolved=`False`，regression_detected=`False`，drift_risk=`major`。
  - local_rejection：reason=`new_blocking_design_diagnostic; forced_transition_count_drift`，rejected_by_stage=`SD-10`。
    - local evidence 1: `new_blocking_design_diagnostic` {"items": [{"budget_exhausted": false, "budget_remaining": 2, "code": "W_GUARD_VARS_NEVER_CHANGE", "instance_key": "W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.InitialDispatchSelect:to_path=LNGShipEMS.BatteryAssist", "message": "Transition guard reads only variables that are never changed by actions or effects.", "policy_action": "budgeted_repair", "pyfcstm_severity": "warning", "rationale": "", "refs": {"from_path": "LNGShipEMS.InitialDispatchSelect", "guard_vars": ["PL", "Ppv", "Pw", "SoC",...<truncated 33836 chars>
    - local evidence 2: `forced_transition_count_drift` {"fix_target": "sim", "kind": "forced_transition_count_drift", "new": 156, "old": 144}

</details>

<details><summary>Repair 4 / iteration `3` / source `SD-4` / accepted=✅</summary>

#### 为什么进入修复

- selected feedback source：`SD-4`；blocking=`True`；pre_scenario=`False`。
- problem_summary：Transition guard reads only variables that are never changed by actions or effects.; Transition guard reads only variables that are never changed by actions or effects.; Transition guard reads only variables that are never changed by actions or effects.
- diagnostic ids：`W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.InitialDispatchSelect:to_path=LNGShipEMS.BatteryAssist, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.InitialDispatchSelect:to_path=LNGShipEMS.LNGDispatch, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.InitialDispatchSelect:to_path=LNGShipEMS.LNGChargeMargin, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.InitialDispatchSelect:to_path=LNGShipEMS.LNGDG3Dispatch, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.InitialDispatchSelect:to_path=LNGShipEMS.LNGDG3ChargeMargin, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.InitialDispatchSelect:to_path=LNGShipEMS.AddDG1LastPriority, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.InitialDispatchSelect:to_path=LNGShipEMS.AddDG2LastPriority, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.InitialDispatchSelect:to_path=LNGShipEMS.ExtremeOverloadBatteryLack, W_FORCED_OVERRIDES_NORMAL:from_path=LNGShipEMS.InitialDispatchSelect:to_path=LNGShipEMS.ZeroLoadCharge, W_FORCED_OVERRIDES_NORMAL:from_path=LNGShipEMS.InitialDispatchSelect:to_path=LNGShipEMS.ZeroLoadSpare, W_FORCED_OVERRIDES_NORMAL:from_path=LNGShipEMS.InitialDispatchSelect:to_path=LNGShipEMS.RESCoversCharge, W_FORCED_OVERRIDES_NORMAL:from_path=LNGShipEMS.InitialDispatchSelect:to_path=LNGShipEMS.RESCoversSpare, ... +16`。
- before_dsl_hash：`sha256:9121b16d876b7385b65d3cf1f8060acd9e094046ce82de945e480c492432fa20`；candidate_dsl_hash：`sha256:3454c23c9fdabd2846510c8225fe02a330f3f8fec051dee98e1de2f7ebab9fc1`。

#### 错误证据 / diagnostics

- 1. `W_GUARD_VARS_NEVER_CHANGE` `W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.InitialDispatchSelect:to_path=LNGShipEMS.BatteryAssist` policy=`budgeted_repair`：Transition guard reads only variables that are never changed by actions or effects.；refs=`{"from_path": "LNGShipEMS.InitialDispatchSelect", "guard_vars": ["PL", "Ppv", "Pw", "SoC", "battery_Pmax"], "to_path": "LNGShipEMS.BatteryAssist"}`
- 2. `W_GUARD_VARS_NEVER_CHANGE` `W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.InitialDispatchSelect:to_path=LNGShipEMS.LNGDispatch` policy=`budgeted_repair`：Transition guard reads only variables that are never changed by actions or effects.；refs=`{"from_path": "LNGShipEMS.InitialDispatchSelect", "guard_vars": ["PL", "Plngmax", "Ppv", "Pw", "SoC", "battery_Pmax"], "to_path": "LNGShipEMS.LNGDispatch"}`
- 3. `W_GUARD_VARS_NEVER_CHANGE` `W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.InitialDispatchSelect:to_path=LNGShipEMS.LNGChargeMargin` policy=`budgeted_repair`：Transition guard reads only variables that are never changed by actions or effects.；refs=`{"from_path": "LNGShipEMS.InitialDispatchSelect", "guard_vars": ["PL", "Pgmax", "Plngmax", "Ppv", "Pw", "SoC"], "to_path": "LNGShipEMS.LNGChargeMargin"}`
- 4. `W_GUARD_VARS_NEVER_CHANGE` `W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.InitialDispatchSelect:to_path=LNGShipEMS.LNGDG3Dispatch` policy=`budgeted_repair`：Transition guard reads only variables that are never changed by actions or effects.；refs=`{"from_path": "LNGShipEMS.InitialDispatchSelect", "guard_vars": ["PL", "Plngmax", "Ppv", "Pw", "SoC", "eng3_Pmax"], "to_path": "LNGShipEMS.LNGDG3Dispatch"}`
- 5. `W_GUARD_VARS_NEVER_CHANGE` `W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.InitialDispatchSelect:to_path=LNGShipEMS.LNGDG3ChargeMargin` policy=`budgeted_repair`：Transition guard reads only variables that are never changed by actions or effects.；refs=`{"from_path": "LNGShipEMS.InitialDispatchSelect", "guard_vars": ["PL", "Pd1max", "Plngmax", "Ppv", "Pw", "SoC", "eng3_Pmax"], "to_path": "LNGShipEMS.LNGDG3ChargeMargin"}`
- 6. `W_GUARD_VARS_NEVER_CHANGE` `W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.InitialDispatchSelect:to_path=LNGShipEMS.AddDG1LastPriority` policy=`budgeted_repair`：Transition guard reads only variables that are never changed by actions or effects.；refs=`{"from_path": "LNGShipEMS.InitialDispatchSelect", "guard_vars": ["PL", "Pd1max", "Plngmax", "Ppv", "Pw", "eng3_Pmax"], "to_path": "LNGShipEMS.AddDG1LastPriority"}`
- 7. `W_GUARD_VARS_NEVER_CHANGE` `W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.InitialDispatchSelect:to_path=LNGShipEMS.AddDG2LastPriority` policy=`budgeted_repair`：Transition guard reads only variables that are never changed by actions or effects.；refs=`{"from_path": "LNGShipEMS.InitialDispatchSelect", "guard_vars": ["PL", "Pd1max", "Pd2max", "Plngmax", "Ppv", "Pw", "eng3_Pmax"], "to_path": "LNGShipEMS.AddDG2LastPriority"}`
- 8. `W_GUARD_VARS_NEVER_CHANGE` `W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.InitialDispatchSelect:to_path=LNGShipEMS.ExtremeOverloadBatteryLack` policy=`budgeted_repair`：Transition guard reads only variables that are never changed by actions or effects.；refs=`{"from_path": "LNGShipEMS.InitialDispatchSelect", "guard_vars": ["PL", "Pd1max", "Pd2max", "Plngmax", "Ppv", "Pw", "eng3_Pmax"], "to_path": "LNGShipEMS.ExtremeOverloadBatteryLack"}`
- ……另有 `20` 条 evidence 见 run record。

#### 变量角色与上下文提示

- policy：Advisory only. Do not invent writes for external_input_candidate variables unless NL explicitly gives update semantics; add meaningful NL-grounded writes only for internal state variables.
- source：SD-4 diagnostic refs and generic NL external-input rationale

| Variable | role_hint | nl_token_present | diagnostics |
|---|---|---:|---|
| `PL` | `external_input_candidate` | ✅ | `W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +164` |
| `Pd1max` | `external_input_candidate` | ✅ | `W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +52` |
| `Pd2max` | `unknown` | ❌ | `W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_UNWRITTEN_READ_VAR, ... +24` |
| `Pgmax` | `external_input_candidate` | ✅ | `W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_UNWRITTEN_READ_VAR, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +10` |
| `Plngmax` | `unknown` | ❌ | `W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +94` |
| `Ppv` | `external_input_candidate` | ✅ | `W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +136` |
| `Pw` | `external_input_candidate` | ✅ | `W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +136` |
| `SoC` | `external_input_candidate` | ✅ | `W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +122` |
| `battery_Pmax` | `unknown` | ❌ | `W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_UNWRITTEN_READ_VAR, ... +24` |
| `battery_charging_power` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `battery_discharge_power` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `cut_in_DG1` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `cut_in_DG2` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `cut_in_DG3` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `cut_in_LNG` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `cut_in_load` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `cut_out_DG1` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `cut_out_DG2` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `cut_out_DG3` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `cut_out_LNG` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `cut_out_load` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `eng3_Pmax` | `external_input_candidate` | ✅ | `W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +66` |
| `illegal_overload` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `requested_generator_power` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `spare_power` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |

#### SD-8 FixRequestBatch / 修改请求

- batch_id：`fixbatch-3-sha256-e7904670632`；source_stage=`SD-4`；legacy_plan_kind=`FixPlan`；requests=`12`。

| request_id | severity | hard | waiver | problem | evidence |
|---|---|---:|---:|---|---|
| `fixreq-3-sd4-0-502dbe08a4` | `blocking_warning` | ❌ | ✅ | Transition guard reads only variables that are never changed by actions or effects.; Transition guard reads only variables that are never changed by actions or effects.; Transition guard reads only variables that are nev...<truncated 33 chars> | `W_GUARD_VARS_NEVER_CHANGE` |
| `fixreq-3-sd4-1-96e5e838f6` | `blocking_warning` | ❌ | ✅ | Transition guard reads only variables that are never changed by actions or effects.; Transition guard reads only variables that are never changed by actions or effects.; Transition guard reads only variables that are nev...<truncated 33 chars> | `W_GUARD_VARS_NEVER_CHANGE` |
| `fixreq-3-sd4-2-486171d502` | `blocking_warning` | ❌ | ✅ | Transition guard reads only variables that are never changed by actions or effects.; Transition guard reads only variables that are never changed by actions or effects.; Transition guard reads only variables that are nev...<truncated 33 chars> | `W_GUARD_VARS_NEVER_CHANGE` |
| `fixreq-3-sd4-3-e85a7caa19` | `blocking_warning` | ❌ | ✅ | Transition guard reads only variables that are never changed by actions or effects.; Transition guard reads only variables that are never changed by actions or effects.; Transition guard reads only variables that are nev...<truncated 33 chars> | `W_GUARD_VARS_NEVER_CHANGE` |
| `fixreq-3-sd4-4-c6b9366c5e` | `blocking_warning` | ❌ | ✅ | Transition guard reads only variables that are never changed by actions or effects.; Transition guard reads only variables that are never changed by actions or effects.; Transition guard reads only variables that are nev...<truncated 33 chars> | `W_GUARD_VARS_NEVER_CHANGE` |
| `fixreq-3-sd4-5-2a0b43e661` | `blocking_warning` | ❌ | ✅ | Transition guard reads only variables that are never changed by actions or effects.; Transition guard reads only variables that are never changed by actions or effects.; Transition guard reads only variables that are nev...<truncated 33 chars> | `W_GUARD_VARS_NEVER_CHANGE` |
| `fixreq-3-sd4-6-9d762c747f` | `blocking_warning` | ❌ | ✅ | Transition guard reads only variables that are never changed by actions or effects.; Transition guard reads only variables that are never changed by actions or effects.; Transition guard reads only variables that are nev...<truncated 33 chars> | `W_GUARD_VARS_NEVER_CHANGE` |
| `fixreq-3-sd4-7-2d8613d0a3` | `blocking_warning` | ❌ | ✅ | Transition guard reads only variables that are never changed by actions or effects.; Transition guard reads only variables that are never changed by actions or effects.; Transition guard reads only variables that are nev...<truncated 33 chars> | `W_GUARD_VARS_NEVER_CHANGE` |
| `fixreq-3-sd4-8-564fa1e0a7` | `blocking_warning` | ❌ | ✅ | Transition guard reads only variables that are never changed by actions or effects.; Transition guard reads only variables that are never changed by actions or effects.; Transition guard reads only variables that are nev...<truncated 33 chars> | `W_FORCED_OVERRIDES_NORMAL` |
| `fixreq-3-sd4-9-5825deca1a` | `blocking_warning` | ❌ | ✅ | Transition guard reads only variables that are never changed by actions or effects.; Transition guard reads only variables that are never changed by actions or effects.; Transition guard reads only variables that are nev...<truncated 33 chars> | `W_FORCED_OVERRIDES_NORMAL` |
- ……另有 `2` 个 request 见 run record。

#### SD-8 legacy fix plan / 修改建议

- recommended_strategy：Use diagnostics as hints; choose the smallest globally consistent repair.；Before returning a candidate, verify every required_preserve_element_id still has a concrete DSL representation.
- hint 1：This guard is controlled only by initial variable values. If those values never change, the transition condition is effectively fixed.；`actions=add_write, simplify_guard；do_not=Do not add a meaningless self-assignment; it does not model a real change., Do not rewrite the guard to a meaningless constant only to silence this diagnostic.`
- hint 2：This guard is controlled only by initial variable values. If those values never change, the transition condition is effectively fixed.；`actions=add_write, simplify_guard；do_not=Do not add a meaningless self-assignment; it does not model a real change., Do not rewrite the guard to a meaningless constant only to silence this diagnostic.`
- hint 3：This guard is controlled only by initial variable values. If those values never change, the transition condition is effectively fixed.；`actions=add_write, simplify_guard；do_not=Do not add a meaningless self-assignment; it does not model a real change., Do not rewrite the guard to a meaningless constant only to silence this diagnostic.`
- hint 4：This guard is controlled only by initial variable values. If those values never change, the transition condition is effectively fixed.；`actions=add_write, simplify_guard；do_not=Do not add a meaningless self-assignment; it does not model a real change., Do not rewrite the guard to a meaningless constant only to silence this diagnostic.`
- hint 5：This guard is controlled only by initial variable values. If those values never change, the transition condition is effectively fixed.；`actions=add_write, simplify_guard；do_not=Do not add a meaningless self-assignment; it does not model a real change., Do not rewrite the guard to a meaningless constant only to silence this diagnostic.`
- hint 6：This guard is controlled only by initial variable values. If those values never change, the transition condition is effectively fixed.；`actions=add_write, simplify_guard；do_not=Do not add a meaningless self-assignment; it does not model a real change., Do not rewrite the guard to a meaningless constant only to silence this diagnostic.`
- forbidden_edits：`Do not delete grounded required elements merely to silence diagnostics., Do not invent internal plant/environment dynamics merely to make external input variables appear written.`。
- required_preserve_element_ids：`state:RESCoversCharge, state:RESCoversSpare, state:ZeroLoadCharge, state:ZeroLoadSpare, state:BatteryAssist, state:LNGDispatch, state:LNGChargeMargin, state:LNGDG3Dispatch, state:LNGDG3ChargeMargin, state:AddDG1LastPriority, state:AddDG2LastPriority, state:ExtremeOverloadBatteryLack, ... +20`。

#### SL-9 per-request 决策

- accepted_request_ids：`<derived-from-table>`；candidate_len=`8874`。

| request_id | decision | waiver | rework_locked | rationale / intent |
|---|---|---:|---:|---|
| `fixreq-3-sd4-0-502dbe08a4` | `reject` | ✅ | ❌ | The BatteryAssist guard reads PL, Ppv, Pw, SoC, and battery_Pmax, which are NL-grounded external/time-varying inputs or capacity bounds. The FixLog already waived this warning class, and the current batch provides no new hard evidence requiring invented internal writes or guard simplification. |
| `fixreq-3-sd4-1-96e5e838f6` | `reject` | ✅ | ❌ | The LNGDispatch guard is an NL-required dispatch classifier over external demand, renewable inputs, SoC, battery capacity, and LNG capacity. Adding writes would invent plant dynamics; simplifying the guard would weaken required dispatch logic. This repeats the previously waived external-input warning class. |
| `fixreq-3-sd4-2-486171d502` | `reject` | ✅ | ❌ | The LNGChargeMargin guard preserves the NL-required low-SoC Pgmax/5 charging-margin branch. Its variables are external inputs or capacity bounds, so no meaningful DSL write is grounded in the NL. |
| `fixreq-3-sd4-3-e85a7caa19` | `reject` | ✅ | ❌ | The LNGDG3Dispatch guard uses residual demand and eng3_Pmax/LNG capacity bounds exactly as required by the NL. This is a guard-driven input-classification FSM; no internal update rule is provided. |
| `fixreq-3-sd4-4-c6b9366c5e` | `reject` | ✅ | ❌ | The LNGDG3ChargeMargin guard preserves the NL-required low-SoC Pd1max/10 charging-margin branch. The guard variables are external inputs/capacity bounds and should not be dummy-written. |
| `fixreq-3-sd4-5-2a0b43e661` | `reject` | ✅ | ❌ | The AddDG1LastPriority guard implements the required DG1 last-priority branch over demand, renewable generation, and capacity bounds. No new evidence justifies changing or weakening it. |
| `fixreq-3-sd4-6-9d762c747f` | `reject` | ✅ | ❌ | The AddDG2LastPriority guard implements the required DG2 last-priority branch. Its variables are external inputs/capacity bounds; adding writes or simplifying the predicate would reduce NL fidelity. |
| `fixreq-3-sd4-7-2d8613d0a3` | `reject` | ✅ | ❌ | The ExtremeOverloadBatteryLack guard is required by the overload requirement and depends on external demand, renewable inputs, and thermal capacity bounds. This warning class was previously waived and remains audit-only. |
| `fixreq-3-sd4-8-564fa1e0a7` | `accept` | ❌ | ❌ | The forced transition expanded from ! * already provides InitialDispatchSelect -> ZeroLoadCharge under the same guard. Keeping the explicit normal selector transition is redundant and causes W_FORCED_OVERRIDES_NORMAL. Removing the normal selector transitions preserves dynamic forced dispatch and the prior default-init fix because InitialDispatchSelect is sti...<truncated 202 chars> |
| `fixreq-3-sd4-9-5825deca1a` | `accept` | ❌ | ❌ | The forced transition expanded from ! * already provides InitialDispatchSelect -> ZeroLoadSpare under the same guard. The normal selector transition duplicates it, so removing the normal selector transitions is the smallest coherent fix.；intent=Remove redundant normal InitialDispatchSelect guarded transitions and rely on existing forced dispatch transitions |
| `fixreq-3-sd4-10-6d6713a1a0` | `accept` | ❌ | ❌ | The forced transition expanded from ! * already provides InitialDispatchSelect -> RESCoversCharge under the same guard. Removing the duplicate normal selector transition resolves the forced-overrides-normal warning without changing the grounded state action.；intent=Remove redundant normal InitialDispatchSelect guarded transitions and rely on existing forced ...<truncated 20 chars> |
| `fixreq-3-sd4-11-3468485031` | `accept` | ❌ | ❌ | The forced transition expanded from ! * already provides InitialDispatchSelect -> RESCoversSpare under the same guard. Removing the duplicate normal selector transition resolves the warning while preserving the required RES-spare branch.；intent=Remove redundant normal InitialDispatchSelect guarded transitions and rely on existing forced dispatch transitions |
- repair_rationale：The current hard actionable design issue is duplicate normal selector transitions: root-level ! * forced guarded transitions already expand to InitialDispatchSelect for the same targets and guards.；The smallest safe edit is to remove the explicit normal InitialDispatchSelect guarded transitions and retain the forced guarded dispatch transitions, which preserve dynamic switching and still cover the pseudo selector during initialization...<truncated 1 chars>；The guard-never-change requests are rejected/waived because PL, Ppv, Pw, SoC, battery_Pmax, Plngmax, Pgmax, Pd1max, Pd2max, and eng3_Pmax are NL-grounded external inputs or capacity bounds. No dummy writes or ungrounded plant dynamics were ...<truncated 6 chars>；All twelve required finite dispatch states, output assignments, cut-in/cut-out commands, low-SoC margins Pgmax/5 and Pd1max/10, and the extreme overload battery-lack branch are preserved.；This preserves the previous non-regressive frontier: the initial transition still enters InitialDispatchSelect, and dispatch selection remains governed by the same NL-grounded forced conditions rather than reverting to a fixed RESCoversChar...<truncated 17 chars>
- diff_summary：`{"summary": "Removed the twelve explicit normal InitialDispatchSelect guarded transitions because they duplicate the existing root-level forced guarded dispatch transitions. Kept the pseudo InitialDispatchSelect, all forced dispatch transitions, all twelve required dispatch states, all variables, and all state enter actions."}`。

#### SL-9 candidate / 最终修改执行方案

```pyfcstm
def float PL = 0.0;
def float Ppv = 0.0;
def float Pw = 0.0;
def float SoC = 0.0;
def float battery_Pmax = 0.0;
def float Plngmax = 0.0;
def float eng3_Pmax = 0.0;
def float Pgmax = 0.0;
def float Pd1max = 0.0;
def float Pd2max = 0.0;
def float requested_generator_power = 0.0;
def float battery_discharge_power = 0.0;
def float battery_charging_power = 0.0;
def float spare_power = 0.0;
def int cut_in_LNG = 0;
def int cut_out_LNG = 0;
def int cut_in_DG1 = 0;
def int cut_out_DG1 = 0;
def int cut_in_DG2 = 0;
def int cut_out_DG2 = 0;
def int cut_in_DG3 = 0;
def int cut_out_DG3 = 0;
def int cut_in_load = 0;
def int cut_out_load = 0;
def int illegal_overload = 0;

state LNGShipEMS {
    ! * -> ZeroLoadCharge : if [PL == 0 && SoC < 0.95];
    ! * -> ZeroLoadSpare : if [PL == 0 && SoC >= 0.95];
    ! * -> RESCoversCharge : if [PL > 0 && Ppv + Pw >= PL && SoC < 0.95];
    ! * -> RESCoversSpare : if [PL > 0 && Ppv + Pw >= PL && SoC >= 0.95];
    ! * -> BatteryAssist : if [PL > 0 && Ppv + Pw < PL && SoC > 0.20 && PL - Ppv - Pw <= battery_Pmax];
    ! * -> LNGDispatch : if [PL > 0 && Ppv + Pw < PL && SoC > 0.20 && PL - Ppv - Pw > battery_Pmax && PL - Ppv - Pw <= Plngmax];
    ! * -> LNGChargeMargin : if [PL > 0 && Ppv + Pw < PL && SoC <= 0.20 && PL - Ppv - Pw + Pgmax / 5 <= Plngmax];
    ! * -> LNGDG3Dispatch : if [PL > 0 && Ppv + Pw < PL && SoC > 0.20 && PL - Ppv - Pw > Plngmax && PL - Ppv - Pw <= Plngmax + eng3_Pmax];
    ! * -> LNGDG3ChargeMargin : if [PL > 0 && Ppv + Pw < PL && SoC <= 0.20 && PL - Ppv - Pw + Pd1max / 10 > Plngmax && PL - Ppv - Pw + Pd1max / 10 <= Plngmax + eng3_Pmax];
    ! * -> AddDG1LastPriority : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > Plngmax + eng3_Pmax && PL - Ppv - Pw <= Plngmax + eng3_Pmax + Pd1max];
    ! * -> AddDG2LastPriority : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > Plngmax + eng3_Pmax + Pd1max && PL - Ppv - Pw <= Plngmax + eng3_Pmax + Pd1max + Pd2max];
    ! * -> ExtremeOverloadBatteryLack : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > Plngmax + eng3_Pmax + Pd1max + Pd2max];

    [*] -> InitialDispatchSelect;

    pseudo state InitialDispatchSelect;

    state RESCoversCharge {
        enter {
            requested_generator_power = 0.0;
            battery_discharge_power = 0.0;
            battery_charging_power = Ppv + Pw - PL;
            spare_power = 0.0;
            cut_in_LNG = 0;
            cut_out_LNG = 1;
            cut_in_DG1 = 0;
            cut_out_DG1 = 1;
            cut_in_DG2 = 0;
            cut_out_DG2 = 1;
            cut_in_DG3 = 0;
            cut_out_DG3 = 1;
            cut_in_load = 1;
            cut_out_load = 0;
            illegal_overload = 0;
        }
    }

    state RESCoversSpare {
        enter {
            requested_generator_power = 0.0;
            battery_discharge_power = 0.0;
            battery_charging_power = 0.0;
            spare_power = Ppv + Pw - PL;
            cut_in_LNG = 0;
            cut_out_LNG = 1;
            cut_in_DG1 = 0;
            cut_out_DG1 = 1;
            cut_in_DG2 = 0;
            cut_out_DG2 = 1;
            cut_in_DG3 = 0;
            cut_out_DG3 = 1;
            cut_in_load = 1;
            cut_out_load = 0;
            illegal_overload = 0;
        }
    }

    state ZeroLoadCharge {
        enter {
            requested_generator_power = 0.0;
            battery_discharge_power = 0.0;
            battery_charging_power = Ppv + Pw;
            spare_power = 0.0;
            cut_in_LNG = 0;
            cut_out_LNG = 1;
            cut_in_DG1 = 0;
            cut_out_DG1 = 1;
            cut_in_DG2 = 0;
            cut_out_DG2 = 1;
            cut_in_DG3 = 0;
            cut_out_DG3 = 1;
            cut_in_load = 0;
            cut_out_load = 1;
            illegal_overload = 0;
        }
    }

    state ZeroLoadSpare {
        enter {
            requested_generator_power = 0.0;
            battery_discharge_power = 0.0;
            battery_charging_power = 0.0;
            spare_power = Ppv + Pw;
            cut_in_LNG = 0;
            cut_out_LNG = 1;
            cut_in_DG1 = 0;
            cut_out_DG1 = 1;
            cut_in_DG2 = 0;
            cut_out_DG2 = 1;
            cut_in_DG3 = 0;
            cut_out_DG3 = 1;
            cut_in_load = 0;
            cut_out_load = 1;
            illegal_overload = 0;
        }
    }

    state BatteryAssist {
        enter {
            requested_generator_power = 0.0;
            battery_discharge_power = PL - Ppv - Pw;
            battery_charging_power = 0.0;
            spare_power = 0.0;
            cut_in_LNG = 0;
            cut_out_LNG = 1;
            cut_in_DG1 = 0;
            cut_out_DG1 = 1;
            cut_in_DG2 = 0;
            cut_out_DG2 = 1;
            cut_in_DG3 = 0;
            cut_out_DG3 = 1;
            cut_in_load = 1;
            cut_out_load = 0;
            illegal_overload = 0;
        }
    }

    state LNGDispatch {
        enter {
            requested_generator_power = PL - Ppv - Pw;
            battery_discharge_power = 0.0;
            battery_charging_power = 0.0;
            spare_power = 0.0;
            cut_in_LNG = 1;
            cut_out_LNG = 0;
            cut_in_DG1 = 0;
            cut_out_DG1 = 1;
            cut_in_DG2 = 0;
            cut_out_DG2 = 1;
            cut_in_DG3 = 0;
            cut_out_DG3 = 1;
            cut_in_load = 1;
            cut_out_load = 0;
            illegal_overload = 0;
        }
    }

    state LNGChargeMargin {
        enter {
            requested_generator_power = PL - Ppv - Pw + Pgmax / 5;
            battery_discharge_power = 0.0;
            battery_charging_power = Pgmax / 5;
            spare_power = 0.0;
            cut_in_LNG = 1;
            cut_out_LNG = 0;
            cut_in_DG1 = 0;
            cut_out_DG1 = 1;
            cut_in_DG2 = 0;
            cut_out_DG2 = 1;
            cut_in_DG3 = 0;
            cut_out_DG3 = 1;
            cut_in_load = 1;
            cut_out_load = 0;
            illegal_overload = 0;
        }
    }

    state LNGDG3Dispatch {
        enter {
            requested_generator_power = PL - Ppv - Pw;
            battery_discharge_power = 0.0;
            battery_charging_power = 0.0;
            spare_power = 0.0;
            cut_in_LNG = 1;
            cut_out_LNG = 0;
            cut_in_DG1 = 0;
            cut_out_DG1 = 1;
            cut_in_DG2 = 0;
            cut_out_DG2 = 1;
            cut_in_DG3 = 1;
            cut_out_DG3 = 0;
            cut_in_load = 1;
            cut_out_load = 0;
            illegal_overload = 0;
        }
    }

    state LNGDG3ChargeMargin {
        enter {
            requested_generator_power = PL - Ppv - Pw + Pd1max / 10;
            battery_discharge_power = 0.0;
            battery_charging_power = Pd1max / 10;
            spare_power = 0.0;
            cut_in_LNG = 1;
            cut_out_LNG = 0;
            cut_in_DG1 = 0;
            cut_out_DG1 = 1;
            cut_in_DG2 = 0;
            cut_out_DG2 = 1;
            cut_in_DG3 = 1;
            cut_out_DG3 = 0;
            cut_in_load = 1;
            cut_out_load = 0;
            illegal_overload = 0;
        }
    }

    state AddDG1LastPriority {
        enter {
            requested_generator_power = PL - Ppv - Pw;
            battery_discharge_power = 0.0;
            battery_charging_power = 0.0;
            spare_power = 0.0;
            cut_in_LNG = 1;
            cut_out_LNG = 0;
            cut_in_DG1 = 1;
            cut_out_DG1 = 0;
            cut_in_DG2 = 0;
            cut_out_DG2 = 1;
            cut_in_DG3 = 1;
            cut_out_DG3 = 0;
            cut_in_load = 1;
            cut_out_load = 0;
            illegal_overload = 0;
        }
    }

    state AddDG2LastPriority {
        enter {
            requested_generator_power = PL - Ppv - Pw;
            battery_discharge_power = 0.0;
            battery_charging_power = 0.0;
            spare_power = 0.0;
            cut_in_LNG = 1;
            cut_out_LNG = 0;
            cut_in_DG1 = 1;
            cut_out_DG1 = 0;
            cut_in_DG2 = 1;
            cut_out_DG2 = 0;
            cut_in_DG3 = 1;
            cut_out_DG3 = 0;
            cut_in_load = 1;
            cut_out_load = 0;
            illegal_overload = 0;
        }
    }

    state ExtremeOverloadBatteryLack {
        enter {
            requested_generator_power = Plngmax + eng3_Pmax + Pd1max + Pd2max;
            battery_discharge_power = PL - Ppv - Pw - Plngmax - eng3_Pmax - Pd1max - Pd2max;
            battery_charging_power = 0.0;
            spare_power = 0.0;
            cut_in_LNG = 1;
            cut_out_LNG = 0;
            cut_in_DG1 = 1;
            cut_out_DG1 = 0;
            cut_in_DG2 = 1;
            cut_out_DG2 = 0;
            cut_in_DG3 = 1;
            cut_out_DG3 = 0;
            cut_in_load = 1;
            cut_out_load = 0;
            illegal_overload = 1;
        }
    }
}
```

#### Candidate diff（before -> candidate）

```diff
--- before.fcstm
+++ candidate.fcstm
@@ -281,17 +281,4 @@
             illegal_overload = 1;
         }
     }
-
-    InitialDispatchSelect -> ZeroLoadCharge : if [PL == 0 && SoC < 0.95];
-    InitialDispatchSelect -> ZeroLoadSpare : if [PL == 0 && SoC >= 0.95];
-    InitialDispatchSelect -> RESCoversCharge : if [PL > 0 && Ppv + Pw >= PL && SoC < 0.95];
-    InitialDispatchSelect -> RESCoversSpare : if [PL > 0 && Ppv + Pw >= PL && SoC >= 0.95];
-    InitialDispatchSelect -> BatteryAssist : if [PL > 0 && Ppv + Pw < PL && SoC > 0.20 && PL - Ppv - Pw <= battery_Pmax];
-    InitialDispatchSelect -> LNGDispatch : if [PL > 0 && Ppv + Pw < PL && SoC > 0.20 && PL - Ppv - Pw > battery_Pmax && PL - Ppv - Pw <= Plngmax];
-    InitialDispatchSelect -> LNGChargeMargin : if [PL > 0 && Ppv + Pw < PL && SoC <= 0.20 && PL - Ppv - Pw + Pgmax / 5 <= Plngmax];
-    InitialDispatchSelect -> LNGDG3Dispatch : if [PL > 0 && Ppv + Pw < PL && SoC > 0.20 && PL - Ppv - Pw > Plngmax && PL - Ppv - Pw <= Plngmax + eng3_Pmax];
-    InitialDispatchSelect -> LNGDG3ChargeMargin : if [PL > 0 && Ppv + Pw < PL && SoC <= 0.20 && PL - Ppv - Pw + Pd1max / 10 > Plngmax && PL - Ppv - Pw + Pd1max / 10 <= Plngmax + eng3_Pmax];
-    InitialDispatchSelect -> AddDG1LastPriority : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > Plngmax + eng3_Pmax && PL - Ppv - Pw <= Plngmax + eng3_Pmax + Pd1max];
-    InitialDispatchSelect -> AddDG2LastPriority : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > Plngmax + eng3_Pmax + Pd1max && PL - Ppv - Pw <= Plngmax + eng3_Pmax + Pd1max + Pd2max];
-    InitialDispatchSelect -> ExtremeOverloadBatteryLack : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > Plngmax + eng3_Pmax + Pd1max + Pd2max];
 }
```

#### SL-10 审查结果

- SL-10 decision=`pass`，ok=`True`，target_resolved=`True`，regression_detected=`False`，drift_risk=`none`。
- SL-10 review_meta：schema=`SL10RepairReviewOutput.v1`，failure_policy=`fail_closed`，replay_key=`SL-10:sha256:d685a6542ec9edae6777f5d88efaa8a8077ccef9eb96fb7f37a53ab73e131c17`。
  - SL-10 evidence 1: `{"summary": "The candidate resolves the current actionable design requests fixreq-3-sd4-8 through fixreq-3-sd4-11 by removing the twelve explicit normal InitialDispatchSelect guarded transitions that duplicated the existing root-level forced guarded dispatch transitions. This directly addresses W_FORCED_OVERRIDES_NORMAL while preserving the prior default-initialization repair: [*] still enters the pseudo InitialDispatchSelect, and the retained ! * forced dispatch transitions still classify the initial and later operating condition using the same NL-grounded guards."}`
  - SL-10 evidence 2: `{"summary": "The SL-9 decisions correctly reject/waive fixreq-3-sd4-0 through fixreq-3-sd4-7 because those W_GUARD_VARS_NEVER_CHANGE diagnostics concern PL, Ppv, Pw, SoC, battery_Pmax, Plngmax, Pgmax, Pd1max, Pd2max, and eng3_Pmax, which the NL describes as read inputs or capacity bounds. The complete FixLog repeatedly records that adding dummy writes or simplifying these guards would invent plant dynamics or weaken the required dispatch classification, and the prior SL-10 repair_memory marked these objections audit-only unless new hard regression evidence appears."}`
  - SL-10 evidence 3: `{"summary": "The DSL diff is narrow and non-regressive: it removes only redundant normal selector transitions. It keeps all variables, all output assignments, all cut-in/cut-out commands, all state enter actions, the pseudo InitialDispatchSelect, and all twelve NL-required finite dispatch states: RESCoversCharge, RESCoversSpare, ZeroLoadCharge, ZeroLoadSpare, BatteryAssist, LNGDispatch, LNGChargeMargin, LNGDG3Dispatch, LNGDG3ChargeMargin, AddDG1LastPriority, AddDG2LastPriority, and ExtremeOverloadBatteryLack."}`
  - SL-10 evidence 4: `{"summary": "NL fidelity is preserved. The retained guards and actions still cover zero-load charging/spare behavior by SoC threshold, RES-covered charging/spare behavior by SoC 0.95, RES-first deficit dispatch, battery assist when SoC/capacity allow, LNG before diesel, DG1/DG2 as last priority, low-SoC charging margins Pgmax/5 and Pd1max/10, and the illegal extreme-overload battery-lack branch with all thermal units active."}`
  - SL-10 evidence 5: `{"summary": "Local deterministic evidence is now clean: SD-10 ran with status OK, repair_review_feedback.ok=true, target_resolved=true, regression_detected=false, drift_risk=none, and no local_rejection. This confirms the duplicate-transition edit removed the previously reported forced override issue without introducing the earlier transition-count drift or simulation/design regressions."}`
  - SL-10 evidence 6: `{"summary": "Scenario evidence remains acceptable: the scenario set reports no coverage gap or weak oracle, and the prior hard scenario default_init_zero_load_charge remains protected by the InitialDispatchSelect plus forced dispatch mechanism rather than reverting to the old fixed RESCoversCharge initial state."}`
- local checks evidence：stage=`SD-10`；note=PR-E1 uses local parse/semantic/design/sim checks as SL-10 evidence, not as the final deterministic judge.。
  - local ok=`True`，target_resolved=`True`，regression_detected=`False`，drift_risk=`none`。

</details>


#### FixLog ledger

口径：FixLog 是跨 iteration 的 append-only repair 台账，记录 request batch、SL-9 accept/reject、diff/local evidence、SL-10 批示和下一步动作。

| # | iteration | phase | batch | decisions | next_action | candidate | notes |
|---:|---:|---|---|---|---|---|---|
| 1 | `0` | `request_batch` | `fixbatch-0-sha256-874b3e13f39` | accept=0, reject=0 | `sl9_decision_and_repair` | `<none>` | SD-8 produced FixRequestBatch; deterministic stage does not decide final repair. |
| 2 | `0` | `sl9_decision` | `fixbatch-0-sha256-874b3e13f39` | accept=1, reject=11 | `sl10_review` | `sha256:e4cf5afd22c71c13ec6bf27c1372b7fbca62216ddb49195ac0b757d4fe3ed1b9` | Accepted only the safe constant-threshold repair: SoC_low_limit had no independent NL-required variable identity and was initialized to 0.20, so inlining preserves behavior while removing an unwritten-read warning., Preserved all twelve required finite states and all required output actions, cut-in/cut-out commands, and dispatch guards including RES cover, zero-load, battery assist, LNG, DG3, DG1/DG2 last-priority, and extreme overload branches., Rejected/waived capacity/input write requests for battery_Pmax, Plngmax, Pd2max and guard-never-change warnings because PL, Ppv, Pw, SoC and capacity bounds are NL-described external inputs or capacity parameters. Adding artificial writes would violate the repair instruction not to invent plant/environment dynamics., ... +1 |
| 3 | `0` | `sl10_review` | `fixbatch-0-sha256-874b3e13f39` | accept=1, reject=11 | `sc11_accept_then_sd2` | `sha256:e4cf5afd22c71c13ec6bf27c1372b7fbca62216ddb49195ac0b757d4fe3ed1b9` | repair_memory:sl10_evidence, repair_memory:sl10_evidence, repair_memory:sl10_evidence, ... +2 |
| 4 | `1` | `request_batch` | `fixbatch-1-sha256-a1a5d6e0aa8` | accept=0, reject=0 | `sl9_decision_and_repair` | `<none>` | SD-8 produced FixRequestBatch; deterministic stage does not decide final repair. |
| 5 | `1` | `sl9_decision` | `fixbatch-1-sha256-a1a5d6e0aa8` | accept=0, reject=12 | `reject_or_waiver` | `<none>` | All current requests repeat design warnings already rejected/waived in the FixLog and explicitly overridden by SL-10 as audit-only local objections., The variables battery_Pmax, Plngmax, Pd2max, PL, Ppv, Pw, SoC, Pgmax, eng3_Pmax, and Pd1max are NL-grounded external inputs or capacity bounds used by a guard-driven dispatch classifier. The NL says the FSM reads these values; it does not define internal update equations., The smallest safe action is therefore no DSL edit. Adding writes would violate the forbidden edit against inventing plant/environment dynamics, while simplifying/removing guards would break required states and dispatch branches., ... +1 |
| 6 | `1` | `sl9_all_rejected` | `fixbatch-1-sha256-a1a5d6e0aa8` | accept=0, reject=12 | `continue_after_waiver` | `<none>` | sl9_rejected_all_fix_requests:waiver_continue |
| 7 | `2` | `request_batch` | `fixbatch-2-sha256-83f4e7b3696` | accept=0, reject=0 | `sl9_decision_and_repair` | `<none>` | SD-8 produced FixRequestBatch; deterministic stage does not decide final repair. |
| 8 | `2` | `sl9_decision` | `fixbatch-2-sha256-83f4e7b3696` | accept=1, reject=0 | `sl10_review` | `sha256:9121b16d876b7385b65d3cf1f8060acd9e094046ce82de945e480c492432fa20` | Accepted fixreq-2-sd6-0-99efbfa439 because it is new hard simulation evidence, not a previously waived local-only warning., Scenario default_init_zero_load_charge expected LNGShipEMS.ZeroLoadCharge for PL=0.0, Ppv=10.0, Pw=5.0, SoC=0.5, with battery_charging_power=15.0, cut_in_load=0, and cut_out_load=1. The actual run entered LNGShipEMS.RESCoversCharge, which computed the charging power correctly but used load cut commands for nonzero load., The edit preserves the existing ZeroLoadCharge state action that already sets requested_generator_power=0.0, battery_discharge_power=0.0, battery_charging_power=Ppv+Pw, spare_power=0.0, cut_in_load=0, cut_out_load=1, cut_in_LNG=0, and cut_out_LNG=1., ... +3 |
| 9 | `2` | `sl10_review` | `fixbatch-2-sha256-83f4e7b3696` | accept=1, reject=0 | `sc11_accept_then_sd2` | `sha256:9121b16d876b7385b65d3cf1f8060acd9e094046ce82de945e480c492432fa20` | repair_memory:sl10_evidence, repair_memory:sl10_evidence, repair_memory:sl10_evidence, ... +3 |
| 10 | `3` | `request_batch` | `fixbatch-3-sha256-e7904670632` | accept=0, reject=0 | `sl9_decision_and_repair` | `<none>` | SD-8 produced FixRequestBatch; deterministic stage does not decide final repair. |
| 11 | `3` | `sl9_decision` | `fixbatch-3-sha256-e7904670632` | accept=4, reject=8 | `sl10_review` | `sha256:3454c23c9fdabd2846510c8225fe02a330f3f8fec051dee98e1de2f7ebab9fc1` | The current hard actionable design issue is duplicate normal selector transitions: root-level ! * forced guarded transitions already expand to InitialDispatchSelect for the same targets and guards., The smallest safe edit is to remove the explicit normal InitialDispatchSelect guarded transitions and retain the forced guarded dispatch transitions, which preserve dynamic switching and still cover the pseudo selector during initialization., The guard-never-change requests are rejected/waived because PL, Ppv, Pw, SoC, battery_Pmax, Plngmax, Pgmax, Pd1max, Pd2max, and eng3_Pmax are NL-grounded external inputs or capacity bounds. No dummy writes or ungrounded plant dynamics were added., ... +2 |
| 12 | `3` | `sl10_review` | `fixbatch-3-sha256-e7904670632` | accept=4, reject=8 | `sc11_accept_then_sd2` | `sha256:3454c23c9fdabd2846510c8225fe02a330f3f8fec051dee98e1de2f7ebab9fc1` | repair_memory:sl10_evidence, repair_memory:sl10_evidence, repair_memory:sl10_evidence, ... +5 |

### 8. 尝试记录与成本

- `SL-1`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 6119, 'completion_chars': 20642, 'completion_tokens': 8192, 'elapsed_seconds': 149.4792092090065, 'estimated_completion_tokens': 5161, 'estimated_prompt_tokens': 6646, 'estimated_total_tokens': 11807, 'first_chunk_seconds': 39.22668391899788, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 26582, 'prompt_tokens': 6469, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 14661}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-9`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 4436, 'completion_chars': 14657, 'completion_tokens': 5213, 'elapsed_seconds': 96.81402189799701, 'estimated_completion_tokens': 3665, 'estimated_prompt_tokens': 39062, 'estimated_total_tokens': 42727, 'first_chunk_seconds': 16.8828085080022, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 156246, 'prompt_tokens': 37790, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 43003}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-10`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 795, 'completion_chars': 3688, 'completion_tokens': 1065, 'elapsed_seconds': 21.874743404012406, 'estimated_completion_tokens': 922, 'estimated_prompt_tokens': 33517, 'estimated_total_tokens': 34439, 'first_chunk_seconds': 7.503487183013931, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 134068, 'prompt_tokens': 31253, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 32318}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-9`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1520, 'completion_chars': 6344, 'completion_tokens': 1660, 'elapsed_seconds': 33.97766434398363, 'estimated_completion_tokens': 1586, 'estimated_prompt_tokens': 64938, 'estimated_total_tokens': 66524, 'first_chunk_seconds': 6.520508372981567, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 259750, 'prompt_tokens': 56506, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 58166}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 2943, 'completion_chars': 8843, 'completion_tokens': 4299, 'elapsed_seconds': 79.38124557197443, 'estimated_completion_tokens': 2211, 'estimated_prompt_tokens': 15945, 'estimated_total_tokens': 18156, 'first_chunk_seconds': 26.334571906976635, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 63777, 'prompt_tokens': 16788, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 21087}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 4851, 'completion_chars': 16055, 'completion_tokens': 5370, 'elapsed_seconds': 98.9163181509939, 'estimated_completion_tokens': 4014, 'estimated_prompt_tokens': 19504, 'estimated_total_tokens': 23518, 'first_chunk_seconds': 11.516240499011474, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 78015, 'prompt_tokens': 21030, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 26400}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-9`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 4350, 'completion_chars': 13878, 'completion_tokens': 5217, 'elapsed_seconds': 97.0383703779953, 'estimated_completion_tokens': 3470, 'estimated_prompt_tokens': 44347, 'estimated_total_tokens': 47817, 'first_chunk_seconds': 18.165060080995318, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 177387, 'prompt_tokens': 37677, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 42894}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-10`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1305, 'completion_chars': 6297, 'completion_tokens': 1690, 'elapsed_seconds': 33.02723402099218, 'estimated_completion_tokens': 1575, 'estimated_prompt_tokens': 42266, 'estimated_total_tokens': 43841, 'first_chunk_seconds': 9.291065564000746, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 169062, 'prompt_tokens': 36418, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 38108}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-9`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 4682, 'completion_chars': 16260, 'completion_tokens': 6122, 'elapsed_seconds': 116.15714990900597, 'estimated_completion_tokens': 4065, 'estimated_prompt_tokens': 97719, 'estimated_total_tokens': 101784, 'first_chunk_seconds': 31.956291943992255, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 390875, 'prompt_tokens': 79442, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 85564}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-10`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 688, 'completion_chars': 3097, 'completion_tokens': 862, 'elapsed_seconds': 19.465339963004226, 'estimated_completion_tokens': 775, 'estimated_prompt_tokens': 92460, 'estimated_total_tokens': 93235, 'first_chunk_seconds': 6.978245175007032, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 369838, 'prompt_tokens': 72966, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 73828}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 3093, 'completion_chars': 9305, 'completion_tokens': 4130, 'elapsed_seconds': 76.5010898479959, 'estimated_completion_tokens': 2327, 'estimated_prompt_tokens': 20456, 'estimated_total_tokens': 22783, 'first_chunk_seconds': 21.7747458179947, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 81824, 'prompt_tokens': 22111, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 26241}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-7`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1923, 'completion_chars': 8875, 'completion_tokens': 2848, 'elapsed_seconds': 56.064656035014195, 'estimated_completion_tokens': 2219, 'estimated_prompt_tokens': 51597, 'estimated_total_tokens': 53816, 'first_chunk_seconds': 19.181266047991812, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 206388, 'prompt_tokens': 58445, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 61293}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。

### 9. 最终停止状态与后续含义

- 停止状态：verdict=`success`，record_status=`success`。
- 主要原因分类：`success`。
- required stages executed：`49/14`，missing=`<none>`。
- repairs：`3/4` accepted；scenario_history=`5`。
- 配置含义：`recommended baseline candidate`；该结果可用于评估默认入口本身。
- 主结果/蓝本边界：`main_result_eligible` 只表示该 run 非 provider-invalid 且 trace/schema/secret/final-verdict 口径可进入主结果候选；`path2_ref_model_blueprint_eligible=false` 时，模型仍可作为 FE/BVS 或 dispatch-classifier 压力测试证据，但不得称为 Path2 ref-model 主蓝本。
- 样本含义：若出现 `design_or_variable_dynamics`，应重点审查变量是否仅作为 guard/input 常量而没有事件/动作更新；若出现 pre-scenario parse/semantic 失败，则应先优化 pyfcstm grammar adherence。
