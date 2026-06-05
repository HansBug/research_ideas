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
| Git commit | `587af294f48e3b174169d015f59c390061347841` |
| clean / diff / prompt snapshot | clean=`True`, dirty=`False`, diff_hash=`sha256:2a69ad5797ac568a81bddcef615104303a97261094685f4edd8d4484e889ea09`, prompt_hash=`sha256:29acd3d1171a37b465f2b9278c85877dcbc5703e2d154247154b0c8cb90d6c8e` |
| provider/model 脱敏标识 | mode=`real_env`, model=`gpt-5.5`, real_api=`True` |
| source / paper | source=`project_1_llm_state_machine_modeling/sources/state-transitions-logical-design-for-hybrid-energy-generation-with-renewable-energy-sources-in-lng-ship`, paper=`project_1_llm_state_machine_modeling/sources/state-transitions-logical-design-for-hybrid-energy-generation-with-renewable-energy-sources-in-lng-ship/paper.pdf` |
| 样本筛选理由 | issue #14 / PR-D 代表性 Path2 EFSM，变量、guard、12 个状态和非法状态都明确；但它可能退化为条件分类式 dispatch，因此更适合作为 FE/BVS 压力测试，是否适合作为 Path2 ref-model 蓝本需看最终 DSL 是否具有 state-dependent mode memory。 |
| 变量参与说明 | `PL/Ppv/Pw/SoC/eng*_Pmax` 是环境输入/容量边界，适合暴露 SD-4 对外部输入变量的处理能力。 |
| run_id | `pr-e1-path2_lng_ems-default-lg-e3-toolnode-20260605T192811Z-8bcd6d7c` |
| final verdict/status | verdict=`success`, record=`success`, result=`converged` |
| main_result_eligible | `true` |
| state_mode_decorative_detected | `true` |
| path2_ref_model_blueprint_eligible | `false`；state_mode_decorative: final DSL is dominated by root-level forced guard reclassification; valid as FE/BVS or dispatch-classifier stress evidence, but not a Path2 ref-model blueprint |
| final.fcstm 来源 | `{"accepted": true, "accepted_after_rework": false, "final_dsl_hash": "sha256:fea8ed50cc9bf814763d6cfb0bfa81ebc61727c81131b056e604e37f0532444a", "iteration": 3, "last_rejected_candidate": {"candidate_dsl_hash": "sha256:c8b827039409fe5fe49d7ec4b5b17f7209511b042640bb00aec28e3bd9495720", "iteration": 0, "repair_history_index": 0, "rework_instructions": ["SL-10 pass was downgraded because local deterministic evidence reported major drift and SL-10 evidence did not explicitly address the local rejection reason/kind with a structured local_override_rationale.", "For the next SL-9 repair, do not blindly regenerate the same DSL. Either change the candidate so the local major-drift evidence is resolved, or keep the minimal DSL only with explicit repair_rationale mapping each local objection (for example missing_required_grounding, scenario_regression, count_drift, or forced_transition_count_drift) to concrete NL-grounded states/transitions/actions that remain in the candidate. This rationale is required so SL-10 can produce local_override_rationale instead of cycling."], "same_as_final": false, "sl10_decision": "rework"}, "matching_repair_history_indices": [4], "repair_history_index": 4, "selected_source_stage": "SL-7", "sl10_decision": "pass", "source_kind": "repair_candidate"}` |
| SC-11 post-accept validation | attempted=`false`；attempts=`0`；success=`0`；failure=`0` |
| FixLog next_action 序列 | `sl9_decision_and_repair, sl10_review, sl9_rework, sl10_review, sc11_accept_then_sd2, sl9_decision_and_repair, sl10_review, sc11_accept_then_sd2, sl9_decision_and_repair, sl10_review, sc11_accept_then_sd2, sl9_decision_and_repair, ... +2` |
| iteration exit_reason 序列 | `candidate_accepted_for_next_full_pass, candidate_accepted_for_next_full_pass, candidate_accepted_for_next_full_pass, candidate_accepted_for_next_full_pass, full_pass_all_required_feedback_ok` |
| token/cost/time | tokens=`{'prompt_tokens': 1076111, 'completion_tokens': 75174, 'total_tokens': 1151285, 'estimated_prompt_tokens': 1204140, 'estimated_completion_tokens': 50610, 'estimated_total_tokens': 1254750, 'prompt_chars': 4816531, 'completion_chars': 202409, 'n_calls': 19, 'token_usage_available': True, 'token_usage_unavailable_calls': 0}`, elapsed=`1437.684s` |
| run record | [`pr-e1-path2_lng_ems-default-lg-e3-toolnode-20260605T192811Z-8bcd6d7c.agent_loop.json.gz`](./pr-e1-path2_lng_ems-default-lg-e3-toolnode-20260605T192811Z-8bcd6d7c.agent_loop.json.gz) |
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
| `graph_config_hash` | `sha256:4679e0bc8eebdb9d9c099c5cb10dfd6751581ffef0695a61dd87ea1b58055906` |
| `node_edge_schema_version` | `pr-langgraph.stage-nodes.v1` |
| `checkpoint_backend` | `memory` |
| `checkpoint_backend_type` | `InMemorySaver` |
| `checkpoint_serde` | `pickle` |
| `checkpoint_path_hash` | `sha256:memory` |
| `resumed_from_checkpoint` | `False` |
| `resume_checkpoint_id_hash` | `None` |
| `instrumentation_layer` | `langgraph` |
| `stage_semantics_module` | `method.staged_runtime` |
| `langgraph_node_trace_count` | `98` |
| `langgraph_node_trace_hash` | `sha256:d781d8630d593810ed66b116f85501056a394e477dd72cea9c2fd4bd3a90ef26` |
| `langgraph_compat_ok` | `True` |
| `checkpoint_resume_smoke_scope` | `toy_ledger_langgraph_api_smoke` |
| `real_agent_loop_resume_supported` | `False` |
| `resume_append_only` | `True` |
| `final_trace_delegated_monolithic_runtime` | `False` |
| `final_trace_node_trace_count` | `98` |

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
def float Pgmax = 0.0;
def float Pd1max = 0.0;
def float eng3_Pmax = 0.0;
def float Pbatmax = 0.0;
def float Pgen_req = 0.0;
def float Pbat_discharge = 0.0;
def float Pbat_charge = 0.0;
def float Pspare = 0.0;
def int cmd_generation_cut = 0;
def int cmd_load_cut = 0;
def int cmd_LNG_cut_in = 0;
def int cmd_LNG_cut_out = 0;
def int cmd_DG1_cut_in = 0;
def int cmd_DG1_cut_out = 0;
def int cmd_DG2_cut_in = 0;
def int cmd_DG2_cut_out = 0;
def int cmd_load_cut_in = 0;
def int cmd_load_cut_out = 0;
def int illegal_overload_state = 0;

state LNGShipEMS {
    ! * -> ZeroLoadCharge : if [PL == 0 && Ppv + Pw > 0 && SoC < 0.95];
    ! * -> ZeroLoadSpare : if [PL == 0 && (Ppv + Pw <= 0 || SoC >= 0.95)];
    ! * -> RESCoversCharge : if [PL > 0 && Ppv + Pw >= PL && SoC < 0.95];
    ! * -> RESCoversSpare : if [PL > 0 && Ppv + Pw >= PL && SoC >= 0.95];
    ! * -> RESBatteryDischarge : if [PL > 0 && Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw <= Pbatmax];
    ! * -> LNGOnly : if [PL > 0 && Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw > Pbatmax && PL - Ppv - Pw <= Pgmax];
    ! * -> LNGBatteryAssist : if [PL > 0 && Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw > Pgmax && PL - Ppv - Pw <= Pgmax + Pbatmax];
    ! * -> LNGDG1 : if [PL > 0 && Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw > Pgmax + Pbatmax && PL - Ppv - Pw <= Pgmax + Pd1max];
    ! * -> LNGDG1DG2 : if [PL > 0 && Ppv + Pw < PL && ((SoC >= 0.2 && PL - Ppv - Pw > Pgmax + Pd1max && PL - Ppv - Pw <= Pgmax + Pd1max + eng3_Pmax) || (SoC < 0.2 && PL - Ppv - Pw + Pd1max / 10 > Pgmax + Pd1max + eng3_Pmax && PL - Ppv - Pw <= Pgmax + Pd1max + eng3_Pmax))];
    ! * -> LowSoCLNGChargeMargin : if [PL > 0 && Ppv + Pw < PL && SoC < 0.2 && PL - Ppv - Pw + Pgmax / 5 <= Pgmax];
    ! * -> LowSoCDGChargeMargin : if [PL > 0 && Ppv + Pw < PL && SoC < 0.2 && PL - Ppv - Pw + Pgmax / 5 > Pgmax && PL - Ppv - Pw + Pd1max / 10 <= Pgmax + Pd1max + eng3_Pmax];
    ! * -> AllThermalBatteryLack : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > Pgmax + Pd1max + eng3_Pmax];

    [*] -> ZeroLoadCharge;

    state ZeroLoadCharge {
        enter {
            Pgen_req = 0;
            Pbat_discharge = 0;
            Pbat_charge = Ppv + Pw;
            Pspare = 0;
            cmd_generation_cut = 0;
            cmd_load_cut = 1;
            cmd_LNG_cut_in = 0;
            cmd_LNG_cut_out = 1;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 0;
            cmd_load_cut_out = 1;
        }
    }

    state ZeroLoadSpare {
        enter {
            Pgen_req = 0;
            Pbat_discharge = 0;
            Pbat_charge = 0;
            Pspare = Ppv + Pw;
            cmd_generation_cut = 0;
            cmd_load_cut = 1;
            cmd_LNG_cut_in = 0;
            cmd_LNG_cut_out = 1;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 0;
            cmd_load_cut_out = 1;
        }
    }

    state RESCoversCharge {
        enter {
            Pgen_req = 0;
            Pbat_discharge = 0;
            Pbat_charge = Ppv + Pw - PL;
            Pspare = 0;
            cmd_generation_cut = 0;
            cmd_load_cut = 0;
            cmd_LNG_cut_in = 0;
            cmd_LNG_cut_out = 1;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state RESCoversSpare {
        enter {
            Pgen_req = 0;
            Pbat_discharge = 0;
            Pbat_charge = 0;
            Pspare = Ppv + Pw - PL;
            cmd_generation_cut = 0;
            cmd_load_cut = 0;
            cmd_LNG_cut_in = 0;
            cmd_LNG_cut_out = 1;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state RESBatteryDischarge {
        enter {
            Pgen_req = 0;
            Pbat_discharge = PL - Ppv - Pw;
            Pbat_charge = 0;
            Pspare = 0;
            cmd_generation_cut = 0;
            cmd_load_cut = 0;
            cmd_LNG_cut_in = 0;
            cmd_LNG_cut_out = 1;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state LNGOnly {
        enter {
            Pgen_req = PL - Ppv - Pw;
            Pbat_discharge = 0;
            Pbat_charge = 0;
            Pspare = 0;
            cmd_generation_cut = 1;
            cmd_load_cut = 0;
            cmd_LNG_cut_in = 1;
            cmd_LNG_cut_out = 0;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state LNGBatteryAssist {
        enter {
            Pgen_req = Pgmax;
            Pbat_discharge = PL - Ppv - Pw - Pgmax;
            Pbat_charge = 0;
            Pspare = 0;
            cmd_generation_cut = 1;
            cmd_load_cut = 0;
            cmd_LNG_cut_in = 1;
            cmd_LNG_cut_out = 0;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state LNGDG1 {
        enter {
            Pgen_req = PL - Ppv - Pw;
            Pbat_discharge = 0;
            Pbat_charge = 0;
            Pspare = 0;
            cmd_generation_cut = 1;
            cmd_load_cut = 0;
            cmd_LNG_cut_in = 1;
            cmd_LNG_cut_out = 0;
            cmd_DG1_cut_in = 1;
            cmd_DG1_cut_out = 0;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state LNGDG1DG2 {
        enter {
            Pgen_req = PL - Ppv - Pw;
            Pbat_discharge = 0;
            Pbat_charge = 0;
            Pspare = 0;
            cmd_generation_cut = 1;
            cmd_load_cut = 0;
            cmd_LNG_cut_in = 1;
            cmd_LNG_cut_out = 0;
            cmd_DG1_cut_in = 1;
            cmd_DG1_cut_out = 0;
            cmd_DG2_cut_in = 1;
            cmd_DG2_cut_out = 0;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state LowSoCLNGChargeMargin {
        enter {
            Pgen_req = PL - Ppv - Pw + Pgmax / 5;
            Pbat_discharge = 0;
            Pbat_charge = Pgmax / 5;
            Pspare = 0;
            cmd_generation_cut = 1;
            cmd_load_cut = 0;
            cmd_LNG_cut_in = 1;
            cmd_LNG_cut_out = 0;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state LowSoCDGChargeMargin {
        enter {
            Pgen_req = PL - Ppv - Pw + Pd1max / 10;
            Pbat_discharge = 0;
            Pbat_charge = Pd1max / 10;
            Pspare = 0;
            cmd_generation_cut = 1;
            cmd_load_cut = 0;
            cmd_LNG_cut_in = 1;
            cmd_LNG_cut_out = 0;
            cmd_DG1_cut_in = 1;
            cmd_DG1_cut_out = 0;
            if [PL - Ppv - Pw + Pd1max / 10 > Pgmax + Pd1max] {
                cmd_DG2_cut_in = 1;
                cmd_DG2_cut_out = 0;
            } else {
                cmd_DG2_cut_in = 0;
                cmd_DG2_cut_out = 1;
            }
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state AllThermalBatteryLack {
        enter {
            illegal_overload_state = 1;
            Pgen_req = Pgmax + Pd1max + eng3_Pmax;
            if [SoC >= 0.2 && PL - Ppv - Pw - Pgmax - Pd1max - eng3_Pmax <= Pbatmax] {
                Pbat_discharge = PL - Ppv - Pw - Pgmax - Pd1max - eng3_Pmax;
            } else if [SoC >= 0.2] {
                Pbat_discharge = Pbatmax;
            } else {
                Pbat_discharge = 0;
            }
            Pbat_charge = 0;
            Pspare = 0;
            cmd_generation_cut = 1;
            cmd_load_cut = 1;
            cmd_LNG_cut_in = 1;
            cmd_LNG_cut_out = 0;
            cmd_DG1_cut_in = 1;
            cmd_DG1_cut_out = 0;
            cmd_DG2_cut_in = 1;
            cmd_DG2_cut_out = 0;
            cmd_load_cut_in = 0;
            cmd_load_cut_out = 1;
        }
        exit {
            illegal_overload_state = 0;
        }
    }
}
```

### 4. 全流程真实摘要表

| Stage | 是否 LLM | iteration | 结果 | 获取的信息 / 反馈 | 本阶段做了什么 | DSL 修改 | artifact/log |
|---|---:|---:|---:|---|---|---|---|
| `SC-0` | 否 | - | ✅ | trace/control | 初始化 run state | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e3-toolnode-20260605T192811Z-8bcd6d7c.agent_loop.json.gz) |
| `SL-1` | 是 | - | ✅ | LLM calls=1, tokens=14424 | 生成初始 DSL 与 grounding seeds | initial len=7343 | [`record`](./pr-e1-path2_lng_ems-default-lg-e3-toolnode-20260605T192811Z-8bcd6d7c.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e3-toolnode-20260605T192811Z-8bcd6d7c.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e3-toolnode-20260605T192811Z-8bcd6d7c.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ⚠️ | blocking=49, advisory=127, info=0; blocking=49, advisory=131, info=0; blocking=0, advisory=180, info=0; blocking=0, advisory=182, info=0; blocking=0, advisory=182, info=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e3-toolnode-20260605T192811Z-8bcd6d7c.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e3-toolnode-20260605T192811Z-8bcd6d7c.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=5, tokens=549223 | LLM per-request accept/reject + repair | candidate len=7343,8193,8193,8575,8893 | [`record`](./pr-e1-path2_lng_ems-default-lg-e3-toolnode-20260605T192811Z-8bcd6d7c.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ⚠️ | LLM calls=5, tokens=258364 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e3-toolnode-20260605T192811Z-8bcd6d7c.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=5, tokens=549223 | LLM per-request accept/reject + repair | candidate len=7343,8193,8193,8575,8893 | [`record`](./pr-e1-path2_lng_ems-default-lg-e3-toolnode-20260605T192811Z-8bcd6d7c.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=5, tokens=258364 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e3-toolnode-20260605T192811Z-8bcd6d7c.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e3-toolnode-20260605T192811Z-8bcd6d7c.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e3-toolnode-20260605T192811Z-8bcd6d7c.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e3-toolnode-20260605T192811Z-8bcd6d7c.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ⚠️ | blocking=49, advisory=127, info=0; blocking=49, advisory=131, info=0; blocking=0, advisory=180, info=0; blocking=0, advisory=182, info=0; blocking=0, advisory=182, info=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e3-toolnode-20260605T192811Z-8bcd6d7c.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e3-toolnode-20260605T192811Z-8bcd6d7c.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=5, tokens=549223 | LLM per-request accept/reject + repair | candidate len=7343,8193,8193,8575,8893 | [`record`](./pr-e1-path2_lng_ems-default-lg-e3-toolnode-20260605T192811Z-8bcd6d7c.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=5, tokens=258364 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e3-toolnode-20260605T192811Z-8bcd6d7c.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e3-toolnode-20260605T192811Z-8bcd6d7c.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e3-toolnode-20260605T192811Z-8bcd6d7c.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e3-toolnode-20260605T192811Z-8bcd6d7c.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=49, advisory=127, info=0; blocking=49, advisory=131, info=0; blocking=0, advisory=180, info=0; blocking=0, advisory=182, info=0; blocking=0, advisory=182, info=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e3-toolnode-20260605T192811Z-8bcd6d7c.agent_loop.json.gz) |
| `SL-5` | 是 | 2 | ✅ | LLM calls=5, tokens=146647 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e3-toolnode-20260605T192811Z-8bcd6d7c.agent_loop.json.gz) |
| `SD-5A` | 否 | 2 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e3-toolnode-20260605T192811Z-8bcd6d7c.agent_loop.json.gz) |
| `SL-5` | 是 | 2 | ✅ | LLM calls=5, tokens=146647 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e3-toolnode-20260605T192811Z-8bcd6d7c.agent_loop.json.gz) |
| `SD-5A` | 否 | 2 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e3-toolnode-20260605T192811Z-8bcd6d7c.agent_loop.json.gz) |
| `SL-5` | 是 | 2 | ✅ | LLM calls=5, tokens=146647 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e3-toolnode-20260605T192811Z-8bcd6d7c.agent_loop.json.gz) |
| `SD-5A` | 否 | 2 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e3-toolnode-20260605T192811Z-8bcd6d7c.agent_loop.json.gz) |
| `SC-5F` | 否 | 2 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e3-toolnode-20260605T192811Z-8bcd6d7c.agent_loop.json.gz) |
| `SD-6` | 否 | 2 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e3-toolnode-20260605T192811Z-8bcd6d7c.agent_loop.json.gz) |
| `SL-7` | 是 | 2 | ✅ | LLM calls=3, tokens=182627 | LLM model review | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e3-toolnode-20260605T192811Z-8bcd6d7c.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e3-toolnode-20260605T192811Z-8bcd6d7c.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=5, tokens=549223 | LLM per-request accept/reject + repair | candidate len=7343,8193,8193,8575,8893 | [`record`](./pr-e1-path2_lng_ems-default-lg-e3-toolnode-20260605T192811Z-8bcd6d7c.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=5, tokens=258364 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e3-toolnode-20260605T192811Z-8bcd6d7c.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e3-toolnode-20260605T192811Z-8bcd6d7c.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e3-toolnode-20260605T192811Z-8bcd6d7c.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e3-toolnode-20260605T192811Z-8bcd6d7c.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=49, advisory=127, info=0; blocking=49, advisory=131, info=0; blocking=0, advisory=180, info=0; blocking=0, advisory=182, info=0; blocking=0, advisory=182, info=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e3-toolnode-20260605T192811Z-8bcd6d7c.agent_loop.json.gz) |
| `SD-5A` | 否 | 2 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e3-toolnode-20260605T192811Z-8bcd6d7c.agent_loop.json.gz) |
| `SL-5` | 是 | 2 | ✅ | LLM calls=5, tokens=146647 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e3-toolnode-20260605T192811Z-8bcd6d7c.agent_loop.json.gz) |
| `SD-5A` | 否 | 2 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e3-toolnode-20260605T192811Z-8bcd6d7c.agent_loop.json.gz) |
| `SC-5F` | 否 | 2 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e3-toolnode-20260605T192811Z-8bcd6d7c.agent_loop.json.gz) |
| `SD-6` | 否 | 2 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e3-toolnode-20260605T192811Z-8bcd6d7c.agent_loop.json.gz) |
| `SL-7` | 是 | 2 | ✅ | LLM calls=3, tokens=182627 | LLM model review | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e3-toolnode-20260605T192811Z-8bcd6d7c.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e3-toolnode-20260605T192811Z-8bcd6d7c.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=5, tokens=549223 | LLM per-request accept/reject + repair | candidate len=7343,8193,8193,8575,8893 | [`record`](./pr-e1-path2_lng_ems-default-lg-e3-toolnode-20260605T192811Z-8bcd6d7c.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=5, tokens=258364 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e3-toolnode-20260605T192811Z-8bcd6d7c.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e3-toolnode-20260605T192811Z-8bcd6d7c.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e3-toolnode-20260605T192811Z-8bcd6d7c.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e3-toolnode-20260605T192811Z-8bcd6d7c.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=49, advisory=127, info=0; blocking=49, advisory=131, info=0; blocking=0, advisory=180, info=0; blocking=0, advisory=182, info=0; blocking=0, advisory=182, info=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e3-toolnode-20260605T192811Z-8bcd6d7c.agent_loop.json.gz) |
| `SD-5A` | 否 | 2 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e3-toolnode-20260605T192811Z-8bcd6d7c.agent_loop.json.gz) |
| `SL-5` | 是 | 2 | ✅ | LLM calls=5, tokens=146647 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e3-toolnode-20260605T192811Z-8bcd6d7c.agent_loop.json.gz) |
| `SD-5A` | 否 | 2 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e3-toolnode-20260605T192811Z-8bcd6d7c.agent_loop.json.gz) |
| `SC-5F` | 否 | 2 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e3-toolnode-20260605T192811Z-8bcd6d7c.agent_loop.json.gz) |
| `SD-6` | 否 | 2 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e3-toolnode-20260605T192811Z-8bcd6d7c.agent_loop.json.gz) |
| `SL-7` | 是 | 2 | ✅ | LLM calls=3, tokens=182627 | LLM model review | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e3-toolnode-20260605T192811Z-8bcd6d7c.agent_loop.json.gz) |
| `SC-12` | 否 | - | ✅ | full_pass_all_required_feedback_ok | 写 final verdict | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e3-toolnode-20260605T192811Z-8bcd6d7c.agent_loop.json.gz) |
| `SC-13` | 否 | - | ✅ | trace/control | 写审计 run record | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e3-toolnode-20260605T192811Z-8bcd6d7c.agent_loop.json.gz) |

### 4.1 完整流程日志（stage/control-flow replay ledger）

口径：本节来自 `AgentLoopRunRecord.logs`，与 [`flow_log.json`](./flow_log.json) 一致；用于复现每个 stage 如何进入、得到什么批示、跳转到哪里，以及每次 DSL 产物/候选如何变化。

| # | ts | stage | iter | event | result / jump | DSL evidence |
|---:|---|---|---:|---|---|---|
| 1 | `2026-06-05T19:28:12Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 2 | `2026-06-05T19:28:12Z` | `SC-0` | `-` | `run_start` | {} | <none> |
| 3 | `2026-06-05T19:28:12Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 4 | `2026-06-05T19:28:12Z` | `SL-1` | `-` | `stage_enter` | {"reason": "initial_modeling_adapter_available"} | <none> |
| 5 | `2026-06-05T19:30:37Z` | `SL-1` | `-` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 6 | `2026-06-05T19:30:37Z` | `SL-1` | `-` | `stage_result` | {"jump": "SD-2", "ok": true} | candidate_dsl:len=7343,hash=sha256:c8b827039409 |
| 7 | `2026-06-05T19:30:37Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 8 | `2026-06-05T19:30:37Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 9 | `2026-06-05T19:30:37Z` | `<control>` | `0` | `iteration_enter` | {} | current_hash=sha256:c8b827039409fe5fe49d7ec4b5b17f7209511b042640bb00aec28e3bd9495720 |
| 10 | `2026-06-05T19:30:37Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 11 | `2026-06-05T19:30:37Z` | `<control>` | `0` | `iteration_validation_enter` | {} | dsl:len=7343,hash=sha256:c8b827039409, current_hash=sha256:c8b827039409fe5fe49d7ec4b5b17f7209511b042640bb00aec28e3bd9495720 |
| 12 | `2026-06-05T19:30:37Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 13 | `2026-06-05T19:30:37Z` | `SD-2` | `0` | `stage_enter` | {"reason": "full_validation_pass"} | <none> |
| 14 | `2026-06-05T19:30:37Z` | `SD-2` | `0` | `stage_result` | {"jump": "SD-3", "ok": true, "status": "StageStatus.OK"} | <none> |
| 15 | `2026-06-05T19:30:37Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 16 | `2026-06-05T19:30:37Z` | `SD-3` | `0` | `stage_enter` | {"reason": "SD-2 ok"} | <none> |
| 17 | `2026-06-05T19:30:38Z` | `SD-3` | `0` | `stage_result` | {"jump": "SD-4", "ok": true, "status": "StageStatus.OK"} | <none> |
| 18 | `2026-06-05T19:30:38Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 19 | `2026-06-05T19:30:38Z` | `SD-4` | `0` | `stage_enter` | {"reason": "SD-3 ok"} | <none> |
| 20 | `2026-06-05T19:30:38Z` | `SD-4` | `0` | `stage_result` | {"jump": "SD-8", "ok": false, "status": "StageStatus.FAIL"} | <none> |
| 21 | `2026-06-05T19:30:38Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 22 | `2026-06-05T19:30:38Z` | `<control>` | `0` | `iteration_validation_result` | {"jump": "SD-8 repair", "selected_feedback": {"blocking": true, "blocking_instance_keys": ["W_UNWRITTEN_READ_VAR:var_name=Pbatmax", "W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.RESBatteryDischarge", "W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.LNGOnly", "W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.LNGBattery...<truncated 12242 chars> | <none> |
| 23 | `2026-06-05T19:30:38Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 24 | `2026-06-05T19:30:38Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 25 | `2026-06-05T19:30:38Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 26 | `2026-06-05T19:30:38Z` | `SD-8` | `0` | `repair_path_enter` | {"jump": "SD-8", "selected_feedback": {"blocking": true, "blocking_instance_keys": ["W_UNWRITTEN_READ_VAR:var_name=Pbatmax", "W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.RESBatteryDischarge", "W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.LNGOnly", "W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.LNGBatteryAssist"...<truncated 256770 chars> | current_dsl:len=7343,hash=sha256:c8b827039409 |
| 27 | `2026-06-05T19:30:38Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 28 | `2026-06-05T19:30:38Z` | `SD-8` | `0` | `stage_result` | {"jump": "SL-9", "ok": true, "status": "StageStatus.OK"} | <none> |
| 29 | `2026-06-05T19:30:38Z` | `SD-8` | `0` | `fix_request_batch` | {"request_count": 12} | <none> |
| 30 | `2026-06-05T19:30:38Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 31 | `2026-06-05T19:30:38Z` | `SL-9` | `0` | `stage_enter` | {"reason": "fix_requests_ready"} | old_dsl:len=7343,hash=sha256:c8b827039409 |
| 32 | `2026-06-05T19:32:20Z` | `SL-9` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 33 | `2026-06-05T19:32:20Z` | `SL-9` | `0` | `stage_result` | {"accepted_request_ids": ["fixreq-0-sd4-0-b906b8138a", "fixreq-0-sd4-1-52d9783dbe", "fixreq-0-sd4-2-c803effc60", "fixreq-0-sd4-3-ce18e2751a", "fixreq-0-sd4-4-bf8c00283b", "fixreq-0-sd4-5-95a78853f9", "fixreq-0-sd4-6-5f2d337ede", "fixreq-0-sd4-7-cc0aa94e0f", "fixreq-0-sd4-8-12d7b1109d", "fixreq-0-sd4-9-2b6c71218f", "fixreq-0-sd4-10-6d13a0b4ed", "fixreq-0-sd4-11-6a2efdf143"], "jump": "SL-10", "ok": true, "rejected_requ...<truncated 13 chars> | candidate_dsl:len=7343,hash=sha256:c8b827039409 |
| 34 | `2026-06-05T19:32:20Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 35 | `2026-06-05T19:32:21Z` | `SD-10` | `0` | `stage_result` | {"jump": "SL-10", "ok": false, "status": "StageStatus.FAIL"} | <none> |
| 36 | `2026-06-05T19:32:21Z` | `SL-10` | `0` | `stage_enter` | {"reason": "candidate_dsl_and_local_evidence_ready"} | candidate_hash=sha256:c8b827039409fe5fe49d7ec4b5b17f7209511b042640bb00aec28e3bd9495720 |
| 37 | `2026-06-05T19:32:51Z` | `SL-10` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 38 | `2026-06-05T19:32:51Z` | `SL-10` | `0` | `stage_result` | {"decision": "rework", "jump": "SL-9 rework", "ok": false} | <none> |
| 39 | `2026-06-05T19:32:51Z` | `SL-10` | `0` | `grounding_update_hints_recorded` | {} | <none> |
| 40 | `2026-06-05T19:32:51Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 41 | `2026-06-05T19:32:51Z` | `SL-9` | `0` | `stage_enter` | {"reason": "sl10_rework_locked"} | old_dsl:len=7343,hash=sha256:c8b827039409 |
| 42 | `2026-06-05T19:34:28Z` | `SL-9` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 43 | `2026-06-05T19:34:28Z` | `SL-9` | `0` | `stage_result` | {"accepted_request_ids": ["fixreq-0-sd4-0-b906b8138a", "fixreq-0-sd4-1-52d9783dbe", "fixreq-0-sd4-2-c803effc60", "fixreq-0-sd4-3-ce18e2751a", "fixreq-0-sd4-4-bf8c00283b", "fixreq-0-sd4-5-95a78853f9", "fixreq-0-sd4-6-5f2d337ede", "fixreq-0-sd4-7-cc0aa94e0f", "fixreq-0-sd4-8-12d7b1109d", "fixreq-0-sd4-9-2b6c71218f", "fixreq-0-sd4-10-6d13a0b4ed", "fixreq-0-sd4-11-6a2efdf143"], "jump": "SL-10", "ok": true, "rejected_requ...<truncated 13 chars> | candidate_dsl:len=8193,hash=sha256:942ea1f43a93 |
| 44 | `2026-06-05T19:34:28Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 45 | `2026-06-05T19:34:29Z` | `SD-10` | `0` | `stage_result` | {"jump": "SL-10", "ok": false, "status": "StageStatus.FAIL"} | <none> |
| 46 | `2026-06-05T19:34:29Z` | `SL-10` | `0` | `stage_enter` | {"reason": "candidate_dsl_and_local_evidence_ready"} | candidate_hash=sha256:942ea1f43a9376d06509746a7e409cc8c830ac52275db43c84b69211068dfa22 |
| 47 | `2026-06-05T19:35:01Z` | `SL-10` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 48 | `2026-06-05T19:35:01Z` | `SL-10` | `0` | `stage_result` | {"decision": "pass", "jump": "SC-11", "ok": true} | <none> |
| 49 | `2026-06-05T19:35:01Z` | `SL-10` | `0` | `grounding_update_hints_recorded` | {} | <none> |
| 50 | `2026-06-05T19:35:01Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 51 | `2026-06-05T19:35:01Z` | `SC-11` | `0` | `stage_result` | {"jump": "SD-2 next iteration", "ok": true, "reason": "SL-10 accepted candidate; next iteration must restart at SD-2"} | candidate_dsl:len=8193,hash=sha256:942ea1f43a93 |
| 52 | `2026-06-05T19:35:01Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 53 | `2026-06-05T19:35:01Z` | `<control>` | `0` | `iteration_repair_result` | {"accepted": true, "jump": "SD-2 next iteration"} | current_hash=sha256:942ea1f43a9376d06509746a7e409cc8c830ac52275db43c84b69211068dfa22 |
| 54 | `2026-06-05T19:35:01Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 55 | `2026-06-05T19:35:01Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 56 | `2026-06-05T19:35:01Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 57 | `2026-06-05T19:35:01Z` | `<control>` | `1` | `iteration_enter` | {} | current_hash=sha256:942ea1f43a9376d06509746a7e409cc8c830ac52275db43c84b69211068dfa22 |
| 58 | `2026-06-05T19:35:01Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 59 | `2026-06-05T19:35:01Z` | `<control>` | `1` | `iteration_validation_enter` | {} | dsl:len=8193,hash=sha256:942ea1f43a93, current_hash=sha256:942ea1f43a9376d06509746a7e409cc8c830ac52275db43c84b69211068dfa22 |
| 60 | `2026-06-05T19:35:01Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 61 | `2026-06-05T19:35:01Z` | `SD-2` | `1` | `stage_enter` | {"reason": "full_validation_pass"} | <none> |
| 62 | `2026-06-05T19:35:01Z` | `SD-2` | `1` | `stage_result` | {"jump": "SD-3", "ok": true, "status": "StageStatus.OK"} | <none> |
| 63 | `2026-06-05T19:35:01Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 64 | `2026-06-05T19:35:01Z` | `SD-3` | `1` | `stage_enter` | {"reason": "SD-2 ok"} | <none> |
| 65 | `2026-06-05T19:35:01Z` | `SD-3` | `1` | `stage_result` | {"jump": "SD-4", "ok": true, "status": "StageStatus.OK"} | <none> |
| 66 | `2026-06-05T19:35:01Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 67 | `2026-06-05T19:35:01Z` | `SD-4` | `1` | `stage_enter` | {"reason": "SD-3 ok"} | <none> |
| 68 | `2026-06-05T19:35:02Z` | `SD-4` | `1` | `stage_result` | {"jump": "SD-8", "ok": false, "status": "StageStatus.FAIL"} | <none> |
| 69 | `2026-06-05T19:35:02Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 70 | `2026-06-05T19:35:02Z` | `<control>` | `1` | `iteration_validation_result` | {"jump": "SD-8 repair", "selected_feedback": {"blocking": true, "blocking_instance_keys": ["W_UNWRITTEN_READ_VAR:var_name=Pbatmax", "W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.RESBatteryDischarge", "W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.LNGOnly", "W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.LNGBattery...<truncated 12436 chars> | <none> |
| 71 | `2026-06-05T19:35:02Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 72 | `2026-06-05T19:35:02Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 73 | `2026-06-05T19:35:02Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 74 | `2026-06-05T19:35:02Z` | `SD-8` | `1` | `repair_path_enter` | {"jump": "SD-8", "selected_feedback": {"blocking": true, "blocking_instance_keys": ["W_UNWRITTEN_READ_VAR:var_name=Pbatmax", "W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.RESBatteryDischarge", "W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.LNGOnly", "W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.LNGBatteryAssist"...<truncated 257640 chars> | current_dsl:len=8193,hash=sha256:942ea1f43a93 |
| 75 | `2026-06-05T19:35:02Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 76 | `2026-06-05T19:35:02Z` | `SD-8` | `1` | `stage_result` | {"jump": "SL-9", "ok": true, "status": "StageStatus.OK"} | <none> |
| 77 | `2026-06-05T19:35:02Z` | `SD-8` | `1` | `fix_request_batch` | {"request_count": 12} | <none> |
| 78 | `2026-06-05T19:35:02Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 79 | `2026-06-05T19:35:02Z` | `SL-9` | `1` | `stage_enter` | {"reason": "fix_requests_ready"} | old_dsl:len=8193,hash=sha256:942ea1f43a93 |
| 80 | `2026-06-05T19:36:33Z` | `SL-9` | `1` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
- ……另有 `172` 条流程日志见 [`flow_log.json`](./flow_log.json) / run record。

### 5. Iteration / repair / review 摘要

| Iter | selected feedback | repair? | FixRequestBatch | SL-9 | local checks | SL-10 | 回到 SD-2? | verdict/备注 |
|---:|---|---|---|---|---|---|---|---|
| 0 | `SD-4` | yes | fixbatch-0-sha256-defea594a84 / n=12 | accept=12, reject=0, waiver=0 | ok=False, target=False, regression=False, drift=major, local_stage=SD-10, reason=design_target_unresolved; missing_required_grounding | decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none> | yes | candidate_accepted_for_next_full_pass |
| 1 | `SD-4` | yes | fixbatch-1-sha256-4686297540a / n=12 | accept=12, reject=0, waiver=0 | ok=False, target=False, regression=False, drift=major, local_stage=SD-10, reason=missing_required_grounding | decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none> | yes | candidate_accepted_for_next_full_pass |
| 2 | `SL-7` | yes | fixbatch-2-sha256-d21d7baa580 / n=2 | accept=2, reject=0, waiver=0 | ok=False, target=False, regression=False, drift=major, local_stage=SD-10, reason=missing_required_grounding | decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none> | yes | candidate_accepted_for_next_full_pass |
| 3 | `SL-7` | yes | fixbatch-3-sha256-5bb8c5e25f4 / n=1 | accept=1, reject=0, waiver=0 | ok=False, target=False, regression=False, drift=major, local_stage=SD-10, reason=missing_required_grounding | decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none> | yes | candidate_accepted_for_next_full_pass |
| 4 | `<none>` | no | <none> | <none> | <none> | <none> | no | full_pass_all_required_feedback_ok |

### 6. Scenario 明细与逐轮通过情况

#### 6.1 Scenario pass/fail by iteration

口径：`✅` = 该 scenario 在该轮 SD-6 simulation 通过；`❌` = 该轮失败；`⚪` = 该轮未执行或无该 scenario 结果。

| Scenario | Intent | Iter 3 | Iter 4 | Iter 5 |
|---|---|---|---|---|
| `default_init_zero_load_charge` | default-init dispatches to the zero-load charging branch when PL=0, RES is present, and SoC is below 0.95. | ✅ | ✅ | ✅ |
| `zero_load_soc_full_spare_boundary` | explicit-hot-start probes the SoC=0.95 boundary for PL=0, where RES should become spare rather than battery charge. | ✅ | ✅ | ✅ |
| `res_covers_charge_below_soc_boundary` | explicit-hot-start probes RES covering positive load with SoC just below 0.95, expecting surplus RES to charge batteries...<truncated 1 chars> | ✅ | ✅ | ✅ |
| `res_covers_spare_at_soc_boundary` | explicit-hot-start probes RES covering positive load at SoC=0.95, expecting residual RES to be spare power. | ✅ | ✅ | ✅ |
| `battery_discharge_at_soc_and_capacity_boundary` | explicit-hot-start probes deficit dispatch at SoC=0.2 and deficit exactly equal to Pbatmax, expecting battery-only suppo...<truncated 13 chars> | ✅ | ✅ | ✅ |
| `lng_only_after_battery_insufficient` | explicit-hot-start asserts RESBatteryDischarge as an origin, then probes LNG-only dispatch when battery is insufficient ...<truncated 36 chars> | ✅ | ✅ | ✅ |
| `lng_battery_assist_when_lng_capacity_short` | explicit-hot-start asserts LNGOnly as an origin, then probes LNG plus battery assist when deficit exceeds Pgmax but fits...<truncated 15 chars> | ✅ | ✅ | ✅ |
| `lng_dg1_last_priority_branch` | explicit-hot-start asserts LNGBatteryAssist as an origin, then probes diesel DG1 cut-in only after LNG and battery prior...<truncated 21 chars> | ✅ | ✅ | ✅ |
| `lng_dg1_dg2_capacity_branch` | explicit-hot-start asserts LNGDG1 as an origin, then probes DG2 cut-in when deficit exceeds LNG+DG1 capacity but fits th...<truncated 24 chars> | ✅ | ✅ | ✅ |
| `low_soc_lng_charge_margin_boundary` | explicit-hot-start asserts LNGDG1DG2 as an origin, then probes low-SoC LNG charging margin at the exact Pgmax/5 covered ...<truncated 9 chars> | ✅ | ✅ | ✅ |
| `low_soc_dg_charge_margin_dg2_capable_branch` | explicit-hot-start asserts LowSoCLNGChargeMargin as an origin, then probes a low-SoC diesel margin case high enough to r...<truncated 56 chars> | ⚪ | ⚪ | ✅ |
| `extreme_demand_all_thermal_battery_lack` | explicit-hot-start asserts LowSoCDGChargeMargin as an origin, then probes extreme demand where all thermal units are act...<truncated 84 chars> | ✅ | ✅ | ✅ |
| `low_soc_dg_charge_margin_branch` |  | ✅ | ✅ | ✅ |
| `forced_reclassification_from_res_charge_to_lng_only` |  | ✅ | ✅ | ✅ |
| `forced_reclassification_from_all_thermal_to_zero_load_charge` |  | ✅ | ✅ | ✅ |
| `forced_reclassification_from_all_thermal_to_res_covers_spare` |  | ✅ | ✅ | ✅ |

#### 6.2 Scenario definitions

<details><summary>`default_init_zero_load_charge` — default-init dispatches to the zero-load charging branch when PL=0, RES is present, and SoC is below 0.95.</summary>

| Field | Value |
|---|---|
| description | default-init dispatches to the zero-load charging branch when PL=0, RES is present, and SoC is below 0.95. |
| initial_state | `<default-init>` |
| initial_vars | `{"PL": 0.0, "Ppv": 3.0, "Pw": 2.0, "SoC": 0.5}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `zero_load_res_charges_battery` | `0` | `[]` | `LNGShipEMS.ZeroLoadCharge` | `{"Pbat_charge": 5.0, "Pbat_discharge": 0.0, "Pgen_req": 0.0, "Pspare": 0.0, "cmd_DG1_cut_in": 0, "cmd_DG1_cut_out": 1, "cmd_DG2_cut_in": 0, "cmd_DG2_cut_out": 1, "cmd_LNG_cut_in": 0, "cmd_LNG_cut_out": 1, "cmd_generation_cut": 0, "cmd_load_cut": 1, "cmd_load_cut_in": 0, "cmd_load_cut_out": 1}` |

</details>

<details><summary>`zero_load_soc_full_spare_boundary` — explicit-hot-start probes the SoC=0.95 boundary for PL=0, where RES should become spare rather than battery charge.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start probes the SoC=0.95 boundary for PL=0, where RES should become spare rather than battery charge. |
| initial_state | `LNGShipEMS.ZeroLoadCharge` |
| initial_vars | `{"PL": 0.0, "Ppv": 4.0, "Pw": 1.0, "SoC": 0.95}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `origin_zero_load_charge_leaf_covered` | `0` | `[]` | `LNGShipEMS.ZeroLoadCharge` | `{}` |
| 1 `zero_load_full_soc_goes_spare` | `0` | `[]` | `LNGShipEMS.ZeroLoadSpare` | `{"Pbat_charge": 0.0, "Pbat_discharge": 0.0, "Pgen_req": 0.0, "Pspare": 5.0, "cmd_DG1_cut_in": 0, "cmd_DG1_cut_out": 1, "cmd_DG2_cut_in": 0, "cmd_DG2_cut_out": 1, "cmd_LNG_cut_in": 0, "cmd_LNG_cut_out": 1, "cmd_generation_cut": 0, "cmd_load_cut": 1, "cmd_load_cut_in": 0, "cmd_load_cut_out": 1}` |

</details>

<details><summary>`res_covers_charge_below_soc_boundary` — explicit-hot-start probes RES covering positive load with SoC just below 0.95, expecting surplus RES to charge batteries.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start probes RES covering positive load with SoC just below 0.95, expecting surplus RES to charge batteries. |
| initial_state | `LNGShipEMS.ZeroLoadSpare` |
| initial_vars | `{"PL": 10.0, "Ppv": 7.0, "Pw": 5.0, "SoC": 0.94}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `origin_zero_load_spare_leaf_covered` | `0` | `[]` | `LNGShipEMS.ZeroLoadSpare` | `{}` |
| 1 `res_surplus_charges_battery` | `0` | `[]` | `LNGShipEMS.RESCoversCharge` | `{"Pbat_charge": 2.0, "Pbat_discharge": 0.0, "Pgen_req": 0.0, "Pspare": 0.0, "cmd_DG1_cut_in": 0, "cmd_DG1_cut_out": 1, "cmd_DG2_cut_in": 0, "cmd_DG2_cut_out": 1, "cmd_LNG_cut_in": 0, "cmd_LNG_cut_out": 1, "cmd_generation_cut": 0, "cmd_load_cut": 0, "cmd_load_cut_in": 1, "cmd_load_cut_out": 0}` |

</details>

<details><summary>`res_covers_spare_at_soc_boundary` — explicit-hot-start probes RES covering positive load at SoC=0.95, expecting residual RES to be spare power.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start probes RES covering positive load at SoC=0.95, expecting residual RES to be spare power. |
| initial_state | `LNGShipEMS.RESCoversCharge` |
| initial_vars | `{"PL": 10.0, "Ppv": 7.0, "Pw": 5.0, "SoC": 0.95}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `origin_res_covers_charge_leaf_covered` | `0` | `[]` | `LNGShipEMS.RESCoversCharge` | `{}` |
| 1 `res_surplus_becomes_spare` | `0` | `[]` | `LNGShipEMS.RESCoversSpare` | `{"Pbat_charge": 0.0, "Pbat_discharge": 0.0, "Pgen_req": 0.0, "Pspare": 2.0, "cmd_DG1_cut_in": 0, "cmd_DG1_cut_out": 1, "cmd_DG2_cut_in": 0, "cmd_DG2_cut_out": 1, "cmd_LNG_cut_in": 0, "cmd_LNG_cut_out": 1, "cmd_generation_cut": 0, "cmd_load_cut": 0, "cmd_load_cut_in": 1, "cmd_load_cut_out": 0}` |

</details>

<details><summary>`battery_discharge_at_soc_and_capacity_boundary` — explicit-hot-start probes deficit dispatch at SoC=0.2 and deficit exactly equal to Pbatmax, expecting battery-only support after RES.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start probes deficit dispatch at SoC=0.2 and deficit exactly equal to Pbatmax, expecting battery-only support after RES. |
| initial_state | `LNGShipEMS.RESCoversSpare` |
| initial_vars | `{"PL": 15.0, "Pbatmax": 10.0, "Pd1max": 15.0, "Pgmax": 20.0, "Ppv": 2.0, "Pw": 3.0, "SoC": 0.2, "eng3_Pmax": 10.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `origin_res_covers_spare_leaf_covered` | `0` | `[]` | `LNGShipEMS.RESCoversSpare` | `{}` |
| 1 `battery_covers_remaining_deficit` | `0` | `[]` | `LNGShipEMS.RESBatteryDischarge` | `{"Pbat_charge": 0.0, "Pbat_discharge": 10.0, "Pgen_req": 0.0, "Pspare": 0.0, "cmd_DG1_cut_in": 0, "cmd_DG1_cut_out": 1, "cmd_DG2_cut_in": 0, "cmd_DG2_cut_out": 1, "cmd_LNG_cut_in": 0, "cmd_LNG_cut_out": 1, "cmd_generation_cut": 0, "cmd_load_cut": 0, "cmd_load_cut_in": 1, "cmd_load_cut_out": 0}` |

</details>

<details><summary>`lng_only_after_battery_insufficient` — explicit-hot-start asserts RESBatteryDischarge as an origin, then probes LNG-only dispatch when battery is insufficient and LNG capacity covers the deficit.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start asserts RESBatteryDischarge as an origin, then probes LNG-only dispatch when battery is insufficient and LNG capacity covers the deficit. |
| initial_state | `LNGShipEMS.RESBatteryDischarge` |
| initial_vars | `{"PL": 20.0, "Pbatmax": 10.0, "Pd1max": 15.0, "Pgmax": 15.0, "Ppv": 2.0, "Pw": 3.0, "SoC": 0.5, "eng3_Pmax": 10.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `origin_state_covered` | `0` | `[]` | `LNGShipEMS.RESBatteryDischarge` | `{}` |
| 1 `lng_covers_deficit` | `0` | `[]` | `LNGShipEMS.LNGOnly` | `{"Pbat_charge": 0.0, "Pbat_discharge": 0.0, "Pgen_req": 15.0, "Pspare": 0.0, "cmd_DG1_cut_in": 0, "cmd_DG1_cut_out": 1, "cmd_DG2_cut_in": 0, "cmd_DG2_cut_out": 1, "cmd_LNG_cut_in": 1, "cmd_LNG_cut_out": 0, "cmd_generation_cut": 1, "cmd_load_cut": 0, "cmd_load_cut_in": 1, "cmd_load_cut_out": 0}` |

</details>

<details><summary>`lng_battery_assist_when_lng_capacity_short` — explicit-hot-start asserts LNGOnly as an origin, then probes LNG plus battery assist when deficit exceeds Pgmax but fits Pgmax+Pbatmax.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start asserts LNGOnly as an origin, then probes LNG plus battery assist when deficit exceeds Pgmax but fits Pgmax+Pbatmax. |
| initial_state | `LNGShipEMS.LNGOnly` |
| initial_vars | `{"PL": 35.0, "Pbatmax": 10.0, "Pd1max": 20.0, "Pgmax": 20.0, "Ppv": 5.0, "Pw": 5.0, "SoC": 0.5, "eng3_Pmax": 10.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `origin_state_covered` | `0` | `[]` | `LNGShipEMS.LNGOnly` | `{}` |
| 1 `lng_at_max_battery_supplies_lack` | `0` | `[]` | `LNGShipEMS.LNGBatteryAssist` | `{"Pbat_charge": 0.0, "Pbat_discharge": 5.0, "Pgen_req": 20.0, "Pspare": 0.0, "cmd_DG1_cut_in": 0, "cmd_DG1_cut_out": 1, "cmd_DG2_cut_in": 0, "cmd_DG2_cut_out": 1, "cmd_LNG_cut_in": 1, "cmd_LNG_cut_out": 0, "cmd_generation_cut": 1, "cmd_load_cut": 0, "cmd_load_cut_in": 1, "cmd_load_cut_out": 0}` |

</details>

<details><summary>`lng_dg1_last_priority_branch` — explicit-hot-start asserts LNGBatteryAssist as an origin, then probes diesel DG1 cut-in only after LNG and battery priority are insufficient.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start asserts LNGBatteryAssist as an origin, then probes diesel DG1 cut-in only after LNG and battery priority are insufficient. |
| initial_state | `LNGShipEMS.LNGBatteryAssist` |
| initial_vars | `{"PL": 40.0, "Pbatmax": 5.0, "Pd1max": 15.0, "Pgmax": 20.0, "Ppv": 5.0, "Pw": 5.0, "SoC": 0.5, "eng3_Pmax": 10.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `origin_state_covered` | `0` | `[]` | `LNGShipEMS.LNGBatteryAssist` | `{}` |
| 1 `dg1_cuts_in_after_lng_priority` | `0` | `[]` | `LNGShipEMS.LNGDG1` | `{"Pbat_charge": 0.0, "Pbat_discharge": 0.0, "Pgen_req": 30.0, "Pspare": 0.0, "cmd_DG1_cut_in": 1, "cmd_DG1_cut_out": 0, "cmd_DG2_cut_in": 0, "cmd_DG2_cut_out": 1, "cmd_LNG_cut_in": 1, "cmd_LNG_cut_out": 0, "cmd_generation_cut": 1, "cmd_load_cut": 0, "cmd_load_cut_in": 1, "cmd_load_cut_out": 0}` |

</details>

<details><summary>`lng_dg1_dg2_capacity_branch` — explicit-hot-start asserts LNGDG1 as an origin, then probes DG2 cut-in when deficit exceeds LNG+DG1 capacity but fits the added eng3_Pmax bound.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start asserts LNGDG1 as an origin, then probes DG2 cut-in when deficit exceeds LNG+DG1 capacity but fits the added eng3_Pmax bound. |
| initial_state | `LNGShipEMS.LNGDG1` |
| initial_vars | `{"PL": 50.0, "Pbatmax": 5.0, "Pd1max": 15.0, "Pgmax": 20.0, "Ppv": 5.0, "Pw": 5.0, "SoC": 0.5, "eng3_Pmax": 10.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `origin_state_covered` | `0` | `[]` | `LNGShipEMS.LNGDG1` | `{}` |
| 1 `dg2_cuts_in_for_higher_deficit` | `0` | `[]` | `LNGShipEMS.LNGDG1DG2` | `{"Pbat_charge": 0.0, "Pbat_discharge": 0.0, "Pgen_req": 40.0, "Pspare": 0.0, "cmd_DG1_cut_in": 1, "cmd_DG1_cut_out": 0, "cmd_DG2_cut_in": 1, "cmd_DG2_cut_out": 0, "cmd_LNG_cut_in": 1, "cmd_LNG_cut_out": 0, "cmd_generation_cut": 1, "cmd_load_cut": 0, "cmd_load_cut_in": 1, "cmd_load_cut_out": 0}` |

</details>

<details><summary>`low_soc_lng_charge_margin_boundary` — explicit-hot-start asserts LNGDG1DG2 as an origin, then probes low-SoC LNG charging margin at the exact Pgmax/5 covered boundary.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start asserts LNGDG1DG2 as an origin, then probes low-SoC LNG charging margin at the exact Pgmax/5 covered boundary. |
| initial_state | `LNGShipEMS.LNGDG1DG2` |
| initial_vars | `{"PL": 18.0, "Pbatmax": 10.0, "Pd1max": 10.0, "Pgmax": 15.0, "Ppv": 3.0, "Pw": 3.0, "SoC": 0.19, "eng3_Pmax": 10.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `origin_state_covered` | `0` | `[]` | `LNGShipEMS.LNGDG1DG2` | `{}` |
| 1 `lng_margin_charges_battery` | `0` | `[]` | `LNGShipEMS.LowSoCLNGChargeMargin` | `{"Pbat_charge": 3.0, "Pbat_discharge": 0.0, "Pgen_req": 15.0, "Pspare": 0.0, "cmd_DG1_cut_in": 0, "cmd_DG1_cut_out": 1, "cmd_DG2_cut_in": 0, "cmd_DG2_cut_out": 1, "cmd_LNG_cut_in": 1, "cmd_LNG_cut_out": 0, "cmd_generation_cut": 1, "cmd_load_cut": 0, "cmd_load_cut_in": 1, "cmd_load_cut_out": 0}` |

</details>

<details><summary>`low_soc_dg_charge_margin_dg2_capable_branch` — explicit-hot-start asserts LowSoCLNGChargeMargin as an origin, then probes a low-SoC diesel margin case high enough to require DG2 while still feasible within t...<truncated 16 chars></summary>

| Field | Value |
|---|---|
| description | explicit-hot-start asserts LowSoCLNGChargeMargin as an origin, then probes a low-SoC diesel margin case high enough to require DG2 while still feasible within thermal capacity. |
| initial_state | `LNGShipEMS.LowSoCLNGChargeMargin` |
| initial_vars | `{"PL": 41.0, "Pbatmax": 10.0, "Pd1max": 10.0, "Pgmax": 20.0, "Ppv": 3.0, "Pw": 2.0, "SoC": 0.19, "eng3_Pmax": 10.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `origin_state_covered` | `0` | `[]` | `LNGShipEMS.LowSoCLNGChargeMargin` | `{}` |
| 1 `dg_margin_charges_battery_and_dg2_cuts_in` | `0` | `[]` | `LNGShipEMS.LowSoCDGChargeMargin` | `{"Pbat_charge": 1.0, "Pbat_discharge": 0.0, "Pgen_req": 37.0, "Pspare": 0.0, "cmd_DG1_cut_in": 1, "cmd_DG1_cut_out": 0, "cmd_DG2_cut_in": 1, "cmd_DG2_cut_out": 0, "cmd_LNG_cut_in": 1, "cmd_LNG_cut_out": 0, "cmd_generation_cut": 1, "cmd_load_cut": 0, "cmd_load_cut_in": 1, "cmd_load_cut_out": 0}` |

</details>

<details><summary>`extreme_demand_all_thermal_battery_lack` — explicit-hot-start asserts LowSoCDGChargeMargin as an origin, then probes extreme demand where all thermal units are active, remaining lack is battery discharge...<truncated 44 chars></summary>

| Field | Value |
|---|---|
| description | explicit-hot-start asserts LowSoCDGChargeMargin as an origin, then probes extreme demand where all thermal units are active, remaining lack is battery discharge, and the illegal overload marker is raised. |
| initial_state | `LNGShipEMS.LowSoCDGChargeMargin` |
| initial_vars | `{"PL": 60.0, "Pbatmax": 10.0, "Pd1max": 15.0, "Pgmax": 20.0, "Ppv": 5.0, "Pw": 5.0, "SoC": 0.5, "eng3_Pmax": 10.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `origin_state_covered` | `0` | `[]` | `LNGShipEMS.LowSoCDGChargeMargin` | `{}` |
| 1 `all_thermal_active_battery_covers_lack` | `0` | `[]` | `LNGShipEMS.AllThermalBatteryLack` | `{"Pbat_charge": 0.0, "Pbat_discharge": 5.0, "Pgen_req": 45.0, "Pspare": 0.0, "cmd_DG1_cut_in": 1, "cmd_DG1_cut_out": 0, "cmd_DG2_cut_in": 1, "cmd_DG2_cut_out": 0, "cmd_LNG_cut_in": 1, "cmd_LNG_cut_out": 0, "cmd_generation_cut": 1, "cmd_load_cut": 1, "cmd_load_cut_in": 0, "cmd_load_cut_out": 1, "illegal_overload_state": 1}` |

</details>


### 7. Repair / blocking feedback 明细

口径：本节记录 agent-loop 真实进入 repair block 后的证据链：FixRequestBatch、SL-9 per-request accept/reject、candidate diff、local-check evidence、SL-10(NL+FixLog) 审阅，以及完整 FixLog ledger 摘录。

| Repair | iteration | accepted | source | blocking diagnostics | SL-9 decisions | SL-10 / local checks | candidate hash |
|---:|---:|---:|---|---|---|---|---|
| 1 | `0` | ❌ | `SD-4` | W_UNWRITTEN_READ_VAR:var_name=Pbatmax, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.RESBatteryDischarge, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.LNGOnly, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.LNGBatteryAssist, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.LNGDG1, ... +48 | accept=12, reject=0, waiver=0 | SL-10 decision=rework, ok=False, target=True, regression=False, drift=minor, rework=SL-10 pass was downgraded because local deterministic evidence reported major drift and SL-10 evidence did not explicitly address the local rejection reason/kind with a structu...<truncated 684 chars> | `sha256:c8b827039409fe5fe49d7ec4b5b17f7209511b042640bb00aec28e3bd9495720` |
| 2 | `0` | ✅ | `SD-4` | W_UNWRITTEN_READ_VAR:var_name=Pbatmax, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.RESBatteryDischarge, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.LNGOnly, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.LNGBatteryAssist, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.LNGDG1, ... +48 | accept=12, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none>; local ok=False, target=False, regression=False, drift=major, local_stage=SD-10, reason=design_target_unresolved; missing_required_grounding | `sha256:942ea1f43a9376d06509746a7e409cc8c830ac52275db43c84b69211068dfa22` |
| 3 | `1` | ✅ | `SD-4` | W_UNWRITTEN_READ_VAR:var_name=Pbatmax, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.RESBatteryDischarge, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.LNGOnly, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.LNGBatteryAssist, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.LNGDG1, ... +48 | accept=12, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none>; local ok=False, target=False, regression=False, drift=major, local_stage=SD-10, reason=missing_required_grounding | `sha256:942ea1f43a9376d06509746a7e409cc8c830ac52275db43c84b69211068dfa22` |
| 4 | `2` | ✅ | `SL-7` | 0, 1 | accept=2, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none>; local ok=False, target=False, regression=False, drift=major, local_stage=SD-10, reason=missing_required_grounding | `sha256:022a18b5cb4d9bbc9bd9f5dbcb9d53df8e63bd2d505d481bcff8d876d1a5a99c` |
| 5 | `3` | ✅ | `SL-7` | 0 | accept=1, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none>; local ok=False, target=False, regression=False, drift=major, local_stage=SD-10, reason=missing_required_grounding | `sha256:fea8ed50cc9bf814763d6cfb0bfa81ebc61727c81131b056e604e37f0532444a` |

<details><summary>Repair 1 / iteration `0` / source `SD-4` / accepted=❌</summary>

#### 为什么进入修复

- selected feedback source：`SD-4`；blocking=`True`；pre_scenario=`True`。
- problem_summary：Variable 'Pbatmax' is read but never written by any action or transition effect.; Transition guard reads only variables that are never changed by actions or effects.; Transition guard reads only variables that are never changed by actions or effects.
- diagnostic ids：`W_UNWRITTEN_READ_VAR:var_name=Pbatmax, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.RESBatteryDischarge, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.LNGOnly, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.LNGBatteryAssist, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.LNGDG1, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadSpare:to_path=LNGShipEMS.RESBatteryDischarge, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadSpare:to_path=LNGShipEMS.LNGOnly, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadSpare:to_path=LNGShipEMS.LNGBatteryAssist, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadSpare:to_path=LNGShipEMS.LNGDG1, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.RESCoversCharge:to_path=LNGShipEMS.RESBatteryDischarge, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.RESCoversCharge:to_path=LNGShipEMS.LNGOnly, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.RESCoversCharge:to_path=LNGShipEMS.LNGBatteryAssist, ... +41`。
- before_dsl_hash：`sha256:c8b827039409fe5fe49d7ec4b5b17f7209511b042640bb00aec28e3bd9495720`；candidate_dsl_hash：`sha256:c8b827039409fe5fe49d7ec4b5b17f7209511b042640bb00aec28e3bd9495720`。

#### 错误证据 / diagnostics

- 1. `W_UNWRITTEN_READ_VAR` `W_UNWRITTEN_READ_VAR:var_name=Pbatmax` policy=`budgeted_repair`：Variable 'Pbatmax' is read but never written by any action or transition effect.；refs=`{"init_value": "0.0", "read_states": ["LNGShipEMS.AllThermalBatteryLack", "LNGShipEMS.LNGBatteryAssist", "LNGShipEMS.LNGDG1", "LNGShipEMS.LNGDG1DG2", "LNGShipEMS.LNGOnly", "LNGShipEMS.LowSoCDGChargeMargin", "LNGShipEMS.LowSoCLNGChargeMargin", "LNGShipEMS.RESBatteryDischarge", "LNGShipEMS.RESCoversCh...<truncated 116 chars>`
- 2. `W_GUARD_VARS_NEVER_CHANGE` `W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.RESBatteryDischarge` policy=`budgeted_repair`：Transition guard reads only variables that are never changed by actions or effects.；refs=`{"from_path": "LNGShipEMS.ZeroLoadCharge", "guard_vars": ["PL", "Pbatmax", "Ppv", "Pw", "SoC"], "to_path": "LNGShipEMS.RESBatteryDischarge"}`
- 3. `W_GUARD_VARS_NEVER_CHANGE` `W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.LNGOnly` policy=`budgeted_repair`：Transition guard reads only variables that are never changed by actions or effects.；refs=`{"from_path": "LNGShipEMS.ZeroLoadCharge", "guard_vars": ["PL", "Pbatmax", "Pgmax", "Ppv", "Pw", "SoC"], "to_path": "LNGShipEMS.LNGOnly"}`
- 4. `W_GUARD_VARS_NEVER_CHANGE` `W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.LNGBatteryAssist` policy=`budgeted_repair`：Transition guard reads only variables that are never changed by actions or effects.；refs=`{"from_path": "LNGShipEMS.ZeroLoadCharge", "guard_vars": ["PL", "Pbatmax", "Pgmax", "Ppv", "Pw", "SoC"], "to_path": "LNGShipEMS.LNGBatteryAssist"}`
- 5. `W_GUARD_VARS_NEVER_CHANGE` `W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.LNGDG1` policy=`budgeted_repair`：Transition guard reads only variables that are never changed by actions or effects.；refs=`{"from_path": "LNGShipEMS.ZeroLoadCharge", "guard_vars": ["PL", "Pbatmax", "Pd1max", "Pgmax", "Ppv", "Pw", "SoC"], "to_path": "LNGShipEMS.LNGDG1"}`
- 6. `W_GUARD_VARS_NEVER_CHANGE` `W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadSpare:to_path=LNGShipEMS.RESBatteryDischarge` policy=`budgeted_repair`：Transition guard reads only variables that are never changed by actions or effects.；refs=`{"from_path": "LNGShipEMS.ZeroLoadSpare", "guard_vars": ["PL", "Pbatmax", "Ppv", "Pw", "SoC"], "to_path": "LNGShipEMS.RESBatteryDischarge"}`
- 7. `W_GUARD_VARS_NEVER_CHANGE` `W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadSpare:to_path=LNGShipEMS.LNGOnly` policy=`budgeted_repair`：Transition guard reads only variables that are never changed by actions or effects.；refs=`{"from_path": "LNGShipEMS.ZeroLoadSpare", "guard_vars": ["PL", "Pbatmax", "Pgmax", "Ppv", "Pw", "SoC"], "to_path": "LNGShipEMS.LNGOnly"}`
- 8. `W_GUARD_VARS_NEVER_CHANGE` `W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadSpare:to_path=LNGShipEMS.LNGBatteryAssist` policy=`budgeted_repair`：Transition guard reads only variables that are never changed by actions or effects.；refs=`{"from_path": "LNGShipEMS.ZeroLoadSpare", "guard_vars": ["PL", "Pbatmax", "Pgmax", "Ppv", "Pw", "SoC"], "to_path": "LNGShipEMS.LNGBatteryAssist"}`
- ……另有 `41` 条 evidence 见 run record。

#### 变量角色与上下文提示

- policy：Advisory only. Do not invent writes for external_input_candidate variables unless NL explicitly gives update semantics; add meaningful NL-grounded writes only for internal state variables.
- source：SD-4 diagnostic refs and generic NL external-input rationale

| Variable | role_hint | nl_token_present | diagnostics |
|---|---|---:|---|
| `PL` | `external_input_candidate` | ✅ | `W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +140` |
| `Pbat_charge` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `Pbat_discharge` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `Pbatmax` | `unknown` | ❌ | `W_UNWRITTEN_READ_VAR, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +44` |
| `Pd1max` | `external_input_candidate` | ✅ | `W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +44` |
| `Pgen_req` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `Pgmax` | `external_input_candidate` | ✅ | `W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +80` |
| `Ppv` | `external_input_candidate` | ✅ | `W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +140` |
| `Pspare` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `Pw` | `external_input_candidate` | ✅ | `W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +140` |
| `SoC` | `external_input_candidate` | ✅ | `W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +128` |
| `cmd_DG1_cut_in` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `cmd_DG1_cut_out` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `cmd_DG2_cut_in` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `cmd_DG2_cut_out` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `cmd_LNG_cut_in` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `cmd_LNG_cut_out` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `cmd_load_cut_in` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `cmd_load_cut_out` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `eng3_Pmax` | `external_input_candidate` | ✅ | `W_UNWRITTEN_READ_VAR, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +20` |

#### SD-8 FixRequestBatch / 修改请求

- batch_id：`fixbatch-0-sha256-defea594a84`；source_stage=`SD-4`；legacy_plan_kind=`FixPlan`；requests=`12`。

| request_id | severity | hard | waiver | problem | evidence |
|---|---|---:|---:|---|---|
| `fixreq-0-sd4-0-b906b8138a` | `blocking_warning` | ❌ | ✅ | Variable 'Pbatmax' is read but never written by any action or transition effect.; Transition guard reads only variables that are never changed by actions or effects.; Transition guard reads only variables that are never ...<truncated 30 chars> | `W_UNWRITTEN_READ_VAR` |
| `fixreq-0-sd4-1-52d9783dbe` | `blocking_warning` | ❌ | ✅ | Variable 'Pbatmax' is read but never written by any action or transition effect.; Transition guard reads only variables that are never changed by actions or effects.; Transition guard reads only variables that are never ...<truncated 30 chars> | `W_GUARD_VARS_NEVER_CHANGE` |
| `fixreq-0-sd4-2-c803effc60` | `blocking_warning` | ❌ | ✅ | Variable 'Pbatmax' is read but never written by any action or transition effect.; Transition guard reads only variables that are never changed by actions or effects.; Transition guard reads only variables that are never ...<truncated 30 chars> | `W_GUARD_VARS_NEVER_CHANGE` |
| `fixreq-0-sd4-3-ce18e2751a` | `blocking_warning` | ❌ | ✅ | Variable 'Pbatmax' is read but never written by any action or transition effect.; Transition guard reads only variables that are never changed by actions or effects.; Transition guard reads only variables that are never ...<truncated 30 chars> | `W_GUARD_VARS_NEVER_CHANGE` |
| `fixreq-0-sd4-4-bf8c00283b` | `blocking_warning` | ❌ | ✅ | Variable 'Pbatmax' is read but never written by any action or transition effect.; Transition guard reads only variables that are never changed by actions or effects.; Transition guard reads only variables that are never ...<truncated 30 chars> | `W_GUARD_VARS_NEVER_CHANGE` |
| `fixreq-0-sd4-5-95a78853f9` | `blocking_warning` | ❌ | ✅ | Variable 'Pbatmax' is read but never written by any action or transition effect.; Transition guard reads only variables that are never changed by actions or effects.; Transition guard reads only variables that are never ...<truncated 30 chars> | `W_GUARD_VARS_NEVER_CHANGE` |
| `fixreq-0-sd4-6-5f2d337ede` | `blocking_warning` | ❌ | ✅ | Variable 'Pbatmax' is read but never written by any action or transition effect.; Transition guard reads only variables that are never changed by actions or effects.; Transition guard reads only variables that are never ...<truncated 30 chars> | `W_GUARD_VARS_NEVER_CHANGE` |
| `fixreq-0-sd4-7-cc0aa94e0f` | `blocking_warning` | ❌ | ✅ | Variable 'Pbatmax' is read but never written by any action or transition effect.; Transition guard reads only variables that are never changed by actions or effects.; Transition guard reads only variables that are never ...<truncated 30 chars> | `W_GUARD_VARS_NEVER_CHANGE` |
| `fixreq-0-sd4-8-12d7b1109d` | `blocking_warning` | ❌ | ✅ | Variable 'Pbatmax' is read but never written by any action or transition effect.; Transition guard reads only variables that are never changed by actions or effects.; Transition guard reads only variables that are never ...<truncated 30 chars> | `W_GUARD_VARS_NEVER_CHANGE` |
| `fixreq-0-sd4-9-2b6c71218f` | `blocking_warning` | ❌ | ✅ | Variable 'Pbatmax' is read but never written by any action or transition effect.; Transition guard reads only variables that are never changed by actions or effects.; Transition guard reads only variables that are never ...<truncated 30 chars> | `W_GUARD_VARS_NEVER_CHANGE` |
- ……另有 `2` 个 request 见 run record。

#### SD-8 legacy fix plan / 修改建议

- recommended_strategy：Use diagnostics as hints; choose the smallest globally consistent repair.；Before returning a candidate, verify every required_preserve_element_id still has a concrete DSL representation.
- hint 1：The variable is used as input but never updated after its initial definition, so model behavior may be accidentally constant.；`actions=add_write, simplify_guard；do_not=Do not add a meaningless self-assignment.`
- hint 2：This guard is controlled only by initial variable values. If those values never change, the transition condition is effectively fixed.；`actions=add_write, simplify_guard；do_not=Do not add a meaningless self-assignment; it does not model a real change., Do not rewrite the guard to a meaningless constant only to silence this diagnostic.`
- hint 3：This guard is controlled only by initial variable values. If those values never change, the transition condition is effectively fixed.；`actions=add_write, simplify_guard；do_not=Do not add a meaningless self-assignment; it does not model a real change., Do not rewrite the guard to a meaningless constant only to silence this diagnostic.`
- hint 4：This guard is controlled only by initial variable values. If those values never change, the transition condition is effectively fixed.；`actions=add_write, simplify_guard；do_not=Do not add a meaningless self-assignment; it does not model a real change., Do not rewrite the guard to a meaningless constant only to silence this diagnostic.`
- hint 5：This guard is controlled only by initial variable values. If those values never change, the transition condition is effectively fixed.；`actions=add_write, simplify_guard；do_not=Do not add a meaningless self-assignment; it does not model a real change., Do not rewrite the guard to a meaningless constant only to silence this diagnostic.`
- hint 6：This guard is controlled only by initial variable values. If those values never change, the transition condition is effectively fixed.；`actions=add_write, simplify_guard；do_not=Do not add a meaningless self-assignment; it does not model a real change., Do not rewrite the guard to a meaningless constant only to silence this diagnostic.`
- forbidden_edits：`Do not delete grounded required elements merely to silence diagnostics., Do not invent internal plant/environment dynamics merely to make external input variables appear written.`。
- required_preserve_element_ids：`state:ZeroLoadCharge, state:ZeroLoadSpare, state:RESCoversCharge, state:RESCoversSpare, state:RESBatteryDischarge, state:LNGOnly, state:LNGBatteryAssist, state:LNGDG1, state:LNGDG1DG2, state:LowSoCLNGChargeMargin, state:LowSoCDGChargeMargin, state:AllThermalBatteryLack, ... +17`。

#### SL-9 per-request 决策

- accepted_request_ids：`<derived-from-table>`；candidate_len=`7343`。

| request_id | decision | waiver | rework_locked | rationale / intent |
|---|---|---:|---:|---|
| `fixreq-0-sd4-0-b906b8138a` | `accept` | ❌ | ❌ | Pbatmax is a capacity/input bound used to classify dispatch branches. The NL says the FSM reads load, renewable, SoC, and capacity-bound inputs; it does not define internal update dynamics for Pbatmax. Adding a synthetic write or self-assignment would be ungrounded and explicitly forbidden.；intent=Preserve Pbatmax as an external capacity input and keep NL-gr...<truncated 24 chars> |
| `fixreq-0-sd4-1-52d9783dbe` | `accept` | ❌ | ❌ | The RESBatteryDischarge guard reads only external/environment inputs: PL, Ppv, Pw, SoC, and Pbatmax. These are the logical transition conditions required by the NL for demand, RES, SoC, and battery capacity selection.；intent=Preserve the guard-driven classifier; do not invent input-update dynamics. |
| `fixreq-0-sd4-2-c803effc60` | `accept` | ❌ | ❌ | The LNGOnly guard is intentionally controlled by external load/resource/capacity inputs. The NL requires state selection by logical conditions over demand, generation, capacity, and SoC.；intent=Preserve NL-grounded LNG-only capacity guard. |
| `fixreq-0-sd4-3-ce18e2751a` | `accept` | ❌ | ❌ | The LNGBatteryAssist guard uses external inputs and capacity bounds to decide when LNG plus battery discharge is required. No NL-grounded internal write exists for these variables.；intent=Preserve NL-grounded LNG plus battery assist guard. |
| `fixreq-0-sd4-4-bf8c00283b` | `accept` | ❌ | ❌ | The LNGDG1 guard depends on external demand/resource/capacity inputs to model DG1 as a later-priority generator. Changing these reads to internal writes would be unfaithful.；intent=Preserve NL-grounded DG1 priority guard. |
| `fixreq-0-sd4-5-95a78853f9` | `accept` | ❌ | ❌ | The selected transition from ZeroLoadSpare to RESBatteryDischarge is part of the same guard-driven reclassification over external ship conditions. The inputs are intentionally read-only inside this dispatch FSM.；intent=Preserve external-input guard semantics. |
| `fixreq-0-sd4-6-5f2d337ede` | `accept` | ❌ | ❌ | The transition to LNGOnly is controlled by external operating conditions and capacity bounds. The DSL should not fabricate plant dynamics solely to silence W_GUARD_VARS_NEVER_CHANGE.；intent=Keep LNGOnly guard unchanged as NL-grounded input classification. |
| `fixreq-0-sd4-7-cc0aa94e0f` | `accept` | ❌ | ❌ | The transition to LNGBatteryAssist correctly reads external load, RES, SoC, and capacity inputs. No safe NL-grounded write is available.；intent=Keep LNGBatteryAssist guard unchanged. |
| `fixreq-0-sd4-8-12d7b1109d` | `accept` | ❌ | ❌ | The transition to LNGDG1 encodes the stated priority order and capacity comparison using external inputs. Synthetic writes would reduce NL fidelity.；intent=Keep LNGDG1 guard unchanged. |
| `fixreq-0-sd4-9-2b6c71218f` | `accept` | ❌ | ❌ | The RESCoversCharge to RESBatteryDischarge reclassification is intentionally driven by changing external demand/resource/SoC values supplied to the FSM.；intent=Preserve guard-driven external input reclassification. |
| `fixreq-0-sd4-10-6d13a0b4ed` | `accept` | ❌ | ❌ | The RESCoversCharge to LNGOnly reclassification depends on externally read operating conditions. The safe repair is to preserve the NL-grounded guard rather than adding meaningless writes.；intent=Preserve LNGOnly external-input guard. |
| `fixreq-0-sd4-11-6a2efdf143` | `accept` | ❌ | ❌ | The RESCoversCharge to LNGBatteryAssist reclassification is part of the required twelve-state dispatch selection. It uses external inputs by design.；intent=Preserve LNGBatteryAssist external-input guard. |
- repair_rationale：No code edit is the smallest safe repair: the selected diagnostics are design warnings caused by external input variables being read in guards but not written by the EMS model.；The NL explicitly describes PL, Ppv, Pw, SoC, and capacity bounds such as eng3_Pmax as values the FSM reads. Pbatmax, Pgmax, and Pd1max are capacity/input bounds used to choose dispatch branches; the NL does not provide internal update equa...<truncated 15 chars>；Adding dummy writes, self-assignments, input counters, or fabricated plant dynamics would violate the repair rule for W_UNWRITTEN_READ_VAR and W_GUARD_VARS_NEVER_CHANGE.；All twelve required states, the zero-load, RES-covered, deficit-priority, low-SoC margin, and all-thermal battery-lack branches are preserved.；The unchanged guard-driven classifier remains parseable and faithful to the NL requirement that states are selected by logical transition conditions over demand, generation, capacity, and SoC.
- diff_summary：`{"summary": "No DSL text changed. Accepted repair is conservative preservation with explicit external-input grounding for Pbatmax and the guard variables rather than inventing ungrounded writes."}`。

#### SL-9 candidate / 最终修改执行方案

```pyfcstm
def float PL = 0.0;
def float Ppv = 0.0;
def float Pw = 0.0;
def float SoC = 0.0;
def float Pgmax = 0.0;
def float Pd1max = 0.0;
def float eng3_Pmax = 0.0;
def float Pbatmax = 0.0;
def float Pgen_req = 0.0;
def float Pbat_discharge = 0.0;
def float Pbat_charge = 0.0;
def float Pspare = 0.0;
def int cmd_LNG_cut_in = 0;
def int cmd_LNG_cut_out = 0;
def int cmd_DG1_cut_in = 0;
def int cmd_DG1_cut_out = 0;
def int cmd_DG2_cut_in = 0;
def int cmd_DG2_cut_out = 0;
def int cmd_load_cut_in = 0;
def int cmd_load_cut_out = 0;

state LNGShipEMS {
    ! * -> ZeroLoadCharge : if [PL == 0 && Ppv + Pw > 0 && SoC < 0.95];
    ! * -> ZeroLoadSpare : if [PL == 0 && (Ppv + Pw <= 0 || SoC >= 0.95)];
    ! * -> RESCoversCharge : if [PL > 0 && Ppv + Pw >= PL && SoC < 0.95];
    ! * -> RESCoversSpare : if [PL > 0 && Ppv + Pw >= PL && SoC >= 0.95];
    ! * -> RESBatteryDischarge : if [PL > 0 && Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw <= Pbatmax];
    ! * -> LNGOnly : if [PL > 0 && Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw > Pbatmax && PL - Ppv - Pw <= Pgmax];
    ! * -> LNGBatteryAssist : if [PL > 0 && Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw > Pgmax && PL - Ppv - Pw <= Pgmax + Pbatmax];
    ! * -> LNGDG1 : if [PL > 0 && Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw > Pgmax + Pbatmax && PL - Ppv - Pw <= Pgmax + Pd1max];
    ! * -> LNGDG1DG2 : if [PL > 0 && Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw > Pgmax + Pd1max && PL - Ppv - Pw <= Pgmax + Pd1max + eng3_Pmax];
    ! * -> LowSoCLNGChargeMargin : if [PL > 0 && Ppv + Pw < PL && SoC < 0.2 && PL - Ppv - Pw + Pgmax / 5 <= Pgmax];
    ! * -> LowSoCDGChargeMargin : if [PL > 0 && Ppv + Pw < PL && SoC < 0.2 && PL - Ppv - Pw + Pgmax / 5 > Pgmax && PL - Ppv - Pw + Pd1max / 10 <= Pgmax + Pd1max];
    ! * -> AllThermalBatteryLack : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > Pgmax + Pd1max + eng3_Pmax];

    [*] -> ZeroLoadCharge;

    state ZeroLoadCharge {
        enter {
            Pgen_req = 0;
            Pbat_discharge = 0;
            Pbat_charge = Ppv + Pw;
            Pspare = 0;
            cmd_LNG_cut_in = 0;
            cmd_LNG_cut_out = 1;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 0;
            cmd_load_cut_out = 1;
        }
    }

    state ZeroLoadSpare {
        enter {
            Pgen_req = 0;
            Pbat_discharge = 0;
            Pbat_charge = 0;
            Pspare = Ppv + Pw;
            cmd_LNG_cut_in = 0;
            cmd_LNG_cut_out = 1;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 0;
            cmd_load_cut_out = 1;
        }
    }

    state RESCoversCharge {
        enter {
            Pgen_req = 0;
            Pbat_discharge = 0;
            Pbat_charge = Ppv + Pw - PL;
            Pspare = 0;
            cmd_LNG_cut_in = 0;
            cmd_LNG_cut_out = 1;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state RESCoversSpare {
        enter {
            Pgen_req = 0;
            Pbat_discharge = 0;
            Pbat_charge = 0;
            Pspare = Ppv + Pw - PL;
            cmd_LNG_cut_in = 0;
            cmd_LNG_cut_out = 1;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state RESBatteryDischarge {
        enter {
            Pgen_req = 0;
            Pbat_discharge = PL - Ppv - Pw;
            Pbat_charge = 0;
            Pspare = 0;
            cmd_LNG_cut_in = 0;
            cmd_LNG_cut_out = 1;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state LNGOnly {
        enter {
            Pgen_req = PL - Ppv - Pw;
            Pbat_discharge = 0;
            Pbat_charge = 0;
            Pspare = 0;
            cmd_LNG_cut_in = 1;
            cmd_LNG_cut_out = 0;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state LNGBatteryAssist {
        enter {
            Pgen_req = Pgmax;
            Pbat_discharge = PL - Ppv - Pw - Pgmax;
            Pbat_charge = 0;
            Pspare = 0;
            cmd_LNG_cut_in = 1;
            cmd_LNG_cut_out = 0;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state LNGDG1 {
        enter {
            Pgen_req = PL - Ppv - Pw;
            Pbat_discharge = 0;
            Pbat_charge = 0;
            Pspare = 0;
            cmd_LNG_cut_in = 1;
            cmd_LNG_cut_out = 0;
            cmd_DG1_cut_in = 1;
            cmd_DG1_cut_out = 0;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state LNGDG1DG2 {
        enter {
            Pgen_req = PL - Ppv - Pw;
            Pbat_discharge = 0;
            Pbat_charge = 0;
            Pspare = 0;
            cmd_LNG_cut_in = 1;
            cmd_LNG_cut_out = 0;
            cmd_DG1_cut_in = 1;
            cmd_DG1_cut_out = 0;
            cmd_DG2_cut_in = 1;
            cmd_DG2_cut_out = 0;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state LowSoCLNGChargeMargin {
        enter {
            Pgen_req = PL - Ppv - Pw + Pgmax / 5;
            Pbat_discharge = 0;
            Pbat_charge = Pgmax / 5;
            Pspare = 0;
            cmd_LNG_cut_in = 1;
            cmd_LNG_cut_out = 0;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state LowSoCDGChargeMargin {
        enter {
            Pgen_req = PL - Ppv - Pw + Pd1max / 10;
            Pbat_discharge = 0;
            Pbat_charge = Pd1max / 10;
            Pspare = 0;
            cmd_LNG_cut_in = 1;
            cmd_LNG_cut_out = 0;
            cmd_DG1_cut_in = 1;
            cmd_DG1_cut_out = 0;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state AllThermalBatteryLack {
        enter {
            Pgen_req = Pgmax + Pd1max + eng3_Pmax;
            Pbat_discharge = PL - Ppv - Pw - Pgmax - Pd1max - eng3_Pmax;
            Pbat_charge = 0;
            Pspare = 0;
            cmd_LNG_cut_in = 1;
            cmd_LNG_cut_out = 0;
            cmd_DG1_cut_in = 1;
            cmd_DG1_cut_out = 0;
            cmd_DG2_cut_in = 1;
            cmd_DG2_cut_out = 0;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }
}
```

#### Candidate diff（before -> candidate）

- before 与 candidate 文本完全一致；无 diff。

#### SL-10 审查结果

- SL-10 decision=`rework`，ok=`False`，target_resolved=`True`，regression_detected=`False`，drift_risk=`minor`。
- SL-10 review_meta：schema=`SL10RepairReviewOutput.v1`，failure_policy=`fail_closed`，replay_key=`SL-10:sha256:4aef0ac156cb758bc8f6dde0894098841447d89f2f95ad479f308b226daf165a`。
  - SL-10 evidence 1: `{"summary": "The NL explicitly characterizes PL, Ppv, Pw, SoC, and capacity bounds as inputs read by the EMS for guard-driven state selection. The FixLog and all SL-9 decisions consistently explain that Pbatmax/Pgmax/Pd1max/eng3_Pmax are external capacity inputs, not internally evolved plant variables. Therefore the W_UNWRITTEN_READ_VAR and W_GUARD_VARS_NEVER_CHANGE diagnostics are conservative local design warnings, not NL-fidelity defects."}`
  - SL-10 evidence 2: `{"summary": "The candidate DSL preserves all twelve NL-required dispatch states and their guards/actions: zero-load charging/spare handling, RES-covered charge/spare handling, RES+battery discharge, LNG-only, LNG+battery assist, LNG+DG1, LNG+DG1+DG2, low-SoC LNG charging margin with Pgmax/5, low-SoC DG charging margin with Pd1max/10, and all-thermal plus battery-lack overload handling."}`
  - SL-10 evidence 3: `{"summary": "The DSL diff is intentionally empty. Given the request hints and forbidden edits, no-edit preservation is the smallest NL-faithful repair: adding synthetic writes, self-assignments, or fabricated environment dynamics would directly conflict with the request guidance and with the NL's external-input classifier model."}`
  - SL-10 evidence 4: `{"summary": "The local missing_required_grounding report names variable:cmd_generation_cut, variable:cmd_load_cut, transition:select_deficit_priority, and transition:select_low_soc_margins. The candidate DSL represents the command obligation with concrete cut-in/cut-out variables for LNG, DG1, DG2, and load commands, and represents the deficit-priority and low-SoC margin obligations through the corresponding guarded transitions rather than explicit transition labels. This is a grounding-name/matcher issue, not a behavioral omission."}`
- SL-10 rework_instructions：SL-10 pass was downgraded because local deterministic evidence reported major drift and SL-10 evidence did not explicitly address the local rejection reason/kind with a structured local_override_rationale.；For the next SL-9 repair, do not blindly regenerate the same DSL. Either change the candidate so the local major-drift evidence is resolved, or keep the minimal DSL only with explicit repair_rationale mapping each local objection (for example missing_required_grounding, scenario_regression, count_drift, or forced_transition_count_drift) to concrete NL-ground...<truncated 152 chars>
- local checks evidence：stage=`SD-10`；note=PR-E1 uses local parse/semantic/design/sim checks as SL-10 evidence, not as the final deterministic judge.。
  - local ok=`False`，target_resolved=`False`，regression_detected=`False`，drift_risk=`major`。
  - local_rejection：reason=`design_target_unresolved; missing_required_grounding`，rejected_by_stage=`SD-10`。
    - local evidence 1: `design_target_unresolved` {"items": [{"budget_exhausted": false, "budget_remaining": 1, "code": "W_UNWRITTEN_READ_VAR", "instance_key": "W_UNWRITTEN_READ_VAR:var_name=Pbatmax", "message": "Variable 'Pbatmax' is read but never written by any action or transition effect.", "policy_action": "budgeted_repair", "pyfcstm_severity": "warning", "rationale": "", "refs": {"init_value": "0.0", "read_states": ["LNGShipEMS.AllThermalBatteryLack", "LNGShipEMS.LNGBatteryAssist", "LNGShipEMS.LNGDG1", "LNGShipEMS.LNGDG1DG2", "LNGShipEMS....<truncated 59126 chars>
    - local evidence 2: `missing_required_grounding` {"element_ids": ["variable:cmd_generation_cut", "variable:cmd_load_cut", "transition:select_deficit_priority", "transition:select_low_soc_margins"], "kind": "missing_required_grounding"}

</details>

<details><summary>Repair 2 / iteration `0` / source `SD-4` / accepted=✅</summary>

#### 为什么进入修复

- selected feedback source：`SD-4`；blocking=`True`；pre_scenario=`True`。
- problem_summary：Variable 'Pbatmax' is read but never written by any action or transition effect.; Transition guard reads only variables that are never changed by actions or effects.; Transition guard reads only variables that are never changed by actions or effects.
- diagnostic ids：`W_UNWRITTEN_READ_VAR:var_name=Pbatmax, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.RESBatteryDischarge, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.LNGOnly, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.LNGBatteryAssist, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.LNGDG1, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadSpare:to_path=LNGShipEMS.RESBatteryDischarge, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadSpare:to_path=LNGShipEMS.LNGOnly, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadSpare:to_path=LNGShipEMS.LNGBatteryAssist, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadSpare:to_path=LNGShipEMS.LNGDG1, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.RESCoversCharge:to_path=LNGShipEMS.RESBatteryDischarge, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.RESCoversCharge:to_path=LNGShipEMS.LNGOnly, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.RESCoversCharge:to_path=LNGShipEMS.LNGBatteryAssist, ... +41`。
- before_dsl_hash：`sha256:c8b827039409fe5fe49d7ec4b5b17f7209511b042640bb00aec28e3bd9495720`；candidate_dsl_hash：`sha256:942ea1f43a9376d06509746a7e409cc8c830ac52275db43c84b69211068dfa22`。

#### 错误证据 / diagnostics

- 1. `W_UNWRITTEN_READ_VAR` `W_UNWRITTEN_READ_VAR:var_name=Pbatmax` policy=`budgeted_repair`：Variable 'Pbatmax' is read but never written by any action or transition effect.；refs=`{"init_value": "0.0", "read_states": ["LNGShipEMS.AllThermalBatteryLack", "LNGShipEMS.LNGBatteryAssist", "LNGShipEMS.LNGDG1", "LNGShipEMS.LNGDG1DG2", "LNGShipEMS.LNGOnly", "LNGShipEMS.LowSoCDGChargeMargin", "LNGShipEMS.LowSoCLNGChargeMargin", "LNGShipEMS.RESBatteryDischarge", "LNGShipEMS.RESCoversCh...<truncated 116 chars>`
- 2. `W_GUARD_VARS_NEVER_CHANGE` `W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.RESBatteryDischarge` policy=`budgeted_repair`：Transition guard reads only variables that are never changed by actions or effects.；refs=`{"from_path": "LNGShipEMS.ZeroLoadCharge", "guard_vars": ["PL", "Pbatmax", "Ppv", "Pw", "SoC"], "to_path": "LNGShipEMS.RESBatteryDischarge"}`
- 3. `W_GUARD_VARS_NEVER_CHANGE` `W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.LNGOnly` policy=`budgeted_repair`：Transition guard reads only variables that are never changed by actions or effects.；refs=`{"from_path": "LNGShipEMS.ZeroLoadCharge", "guard_vars": ["PL", "Pbatmax", "Pgmax", "Ppv", "Pw", "SoC"], "to_path": "LNGShipEMS.LNGOnly"}`
- 4. `W_GUARD_VARS_NEVER_CHANGE` `W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.LNGBatteryAssist` policy=`budgeted_repair`：Transition guard reads only variables that are never changed by actions or effects.；refs=`{"from_path": "LNGShipEMS.ZeroLoadCharge", "guard_vars": ["PL", "Pbatmax", "Pgmax", "Ppv", "Pw", "SoC"], "to_path": "LNGShipEMS.LNGBatteryAssist"}`
- 5. `W_GUARD_VARS_NEVER_CHANGE` `W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.LNGDG1` policy=`budgeted_repair`：Transition guard reads only variables that are never changed by actions or effects.；refs=`{"from_path": "LNGShipEMS.ZeroLoadCharge", "guard_vars": ["PL", "Pbatmax", "Pd1max", "Pgmax", "Ppv", "Pw", "SoC"], "to_path": "LNGShipEMS.LNGDG1"}`
- 6. `W_GUARD_VARS_NEVER_CHANGE` `W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadSpare:to_path=LNGShipEMS.RESBatteryDischarge` policy=`budgeted_repair`：Transition guard reads only variables that are never changed by actions or effects.；refs=`{"from_path": "LNGShipEMS.ZeroLoadSpare", "guard_vars": ["PL", "Pbatmax", "Ppv", "Pw", "SoC"], "to_path": "LNGShipEMS.RESBatteryDischarge"}`
- 7. `W_GUARD_VARS_NEVER_CHANGE` `W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadSpare:to_path=LNGShipEMS.LNGOnly` policy=`budgeted_repair`：Transition guard reads only variables that are never changed by actions or effects.；refs=`{"from_path": "LNGShipEMS.ZeroLoadSpare", "guard_vars": ["PL", "Pbatmax", "Pgmax", "Ppv", "Pw", "SoC"], "to_path": "LNGShipEMS.LNGOnly"}`
- 8. `W_GUARD_VARS_NEVER_CHANGE` `W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadSpare:to_path=LNGShipEMS.LNGBatteryAssist` policy=`budgeted_repair`：Transition guard reads only variables that are never changed by actions or effects.；refs=`{"from_path": "LNGShipEMS.ZeroLoadSpare", "guard_vars": ["PL", "Pbatmax", "Pgmax", "Ppv", "Pw", "SoC"], "to_path": "LNGShipEMS.LNGBatteryAssist"}`
- ……另有 `41` 条 evidence 见 run record。

#### 变量角色与上下文提示

- policy：Advisory only. Do not invent writes for external_input_candidate variables unless NL explicitly gives update semantics; add meaningful NL-grounded writes only for internal state variables.
- source：SD-4 diagnostic refs and generic NL external-input rationale

| Variable | role_hint | nl_token_present | diagnostics |
|---|---|---:|---|
| `PL` | `external_input_candidate` | ✅ | `W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +140` |
| `Pbat_charge` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `Pbat_discharge` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `Pbatmax` | `unknown` | ❌ | `W_UNWRITTEN_READ_VAR, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +44` |
| `Pd1max` | `external_input_candidate` | ✅ | `W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +44` |
| `Pgen_req` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `Pgmax` | `external_input_candidate` | ✅ | `W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +80` |
| `Ppv` | `external_input_candidate` | ✅ | `W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +140` |
| `Pspare` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `Pw` | `external_input_candidate` | ✅ | `W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +140` |
| `SoC` | `external_input_candidate` | ✅ | `W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +128` |
| `cmd_DG1_cut_in` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `cmd_DG1_cut_out` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `cmd_DG2_cut_in` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `cmd_DG2_cut_out` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `cmd_LNG_cut_in` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `cmd_LNG_cut_out` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `cmd_load_cut_in` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `cmd_load_cut_out` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `eng3_Pmax` | `external_input_candidate` | ✅ | `W_UNWRITTEN_READ_VAR, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +20` |

#### SD-8 FixRequestBatch / 修改请求

- batch_id：`fixbatch-0-sha256-defea594a84`；source_stage=`SD-4`；legacy_plan_kind=`FixPlan`；requests=`12`。

| request_id | severity | hard | waiver | problem | evidence |
|---|---|---:|---:|---|---|
| `fixreq-0-sd4-0-b906b8138a` | `blocking_warning` | ❌ | ✅ | Variable 'Pbatmax' is read but never written by any action or transition effect.; Transition guard reads only variables that are never changed by actions or effects.; Transition guard reads only variables that are never ...<truncated 30 chars> | `W_UNWRITTEN_READ_VAR` |
| `fixreq-0-sd4-1-52d9783dbe` | `blocking_warning` | ❌ | ✅ | Variable 'Pbatmax' is read but never written by any action or transition effect.; Transition guard reads only variables that are never changed by actions or effects.; Transition guard reads only variables that are never ...<truncated 30 chars> | `W_GUARD_VARS_NEVER_CHANGE` |
| `fixreq-0-sd4-2-c803effc60` | `blocking_warning` | ❌ | ✅ | Variable 'Pbatmax' is read but never written by any action or transition effect.; Transition guard reads only variables that are never changed by actions or effects.; Transition guard reads only variables that are never ...<truncated 30 chars> | `W_GUARD_VARS_NEVER_CHANGE` |
| `fixreq-0-sd4-3-ce18e2751a` | `blocking_warning` | ❌ | ✅ | Variable 'Pbatmax' is read but never written by any action or transition effect.; Transition guard reads only variables that are never changed by actions or effects.; Transition guard reads only variables that are never ...<truncated 30 chars> | `W_GUARD_VARS_NEVER_CHANGE` |
| `fixreq-0-sd4-4-bf8c00283b` | `blocking_warning` | ❌ | ✅ | Variable 'Pbatmax' is read but never written by any action or transition effect.; Transition guard reads only variables that are never changed by actions or effects.; Transition guard reads only variables that are never ...<truncated 30 chars> | `W_GUARD_VARS_NEVER_CHANGE` |
| `fixreq-0-sd4-5-95a78853f9` | `blocking_warning` | ❌ | ✅ | Variable 'Pbatmax' is read but never written by any action or transition effect.; Transition guard reads only variables that are never changed by actions or effects.; Transition guard reads only variables that are never ...<truncated 30 chars> | `W_GUARD_VARS_NEVER_CHANGE` |
| `fixreq-0-sd4-6-5f2d337ede` | `blocking_warning` | ❌ | ✅ | Variable 'Pbatmax' is read but never written by any action or transition effect.; Transition guard reads only variables that are never changed by actions or effects.; Transition guard reads only variables that are never ...<truncated 30 chars> | `W_GUARD_VARS_NEVER_CHANGE` |
| `fixreq-0-sd4-7-cc0aa94e0f` | `blocking_warning` | ❌ | ✅ | Variable 'Pbatmax' is read but never written by any action or transition effect.; Transition guard reads only variables that are never changed by actions or effects.; Transition guard reads only variables that are never ...<truncated 30 chars> | `W_GUARD_VARS_NEVER_CHANGE` |
| `fixreq-0-sd4-8-12d7b1109d` | `blocking_warning` | ❌ | ✅ | Variable 'Pbatmax' is read but never written by any action or transition effect.; Transition guard reads only variables that are never changed by actions or effects.; Transition guard reads only variables that are never ...<truncated 30 chars> | `W_GUARD_VARS_NEVER_CHANGE` |
| `fixreq-0-sd4-9-2b6c71218f` | `blocking_warning` | ❌ | ✅ | Variable 'Pbatmax' is read but never written by any action or transition effect.; Transition guard reads only variables that are never changed by actions or effects.; Transition guard reads only variables that are never ...<truncated 30 chars> | `W_GUARD_VARS_NEVER_CHANGE` |
- ……另有 `2` 个 request 见 run record。

#### SD-8 legacy fix plan / 修改建议

- recommended_strategy：Use diagnostics as hints; choose the smallest globally consistent repair.；Before returning a candidate, verify every required_preserve_element_id still has a concrete DSL representation.
- hint 1：The variable is used as input but never updated after its initial definition, so model behavior may be accidentally constant.；`actions=add_write, simplify_guard；do_not=Do not add a meaningless self-assignment.`
- hint 2：This guard is controlled only by initial variable values. If those values never change, the transition condition is effectively fixed.；`actions=add_write, simplify_guard；do_not=Do not add a meaningless self-assignment; it does not model a real change., Do not rewrite the guard to a meaningless constant only to silence this diagnostic.`
- hint 3：This guard is controlled only by initial variable values. If those values never change, the transition condition is effectively fixed.；`actions=add_write, simplify_guard；do_not=Do not add a meaningless self-assignment; it does not model a real change., Do not rewrite the guard to a meaningless constant only to silence this diagnostic.`
- hint 4：This guard is controlled only by initial variable values. If those values never change, the transition condition is effectively fixed.；`actions=add_write, simplify_guard；do_not=Do not add a meaningless self-assignment; it does not model a real change., Do not rewrite the guard to a meaningless constant only to silence this diagnostic.`
- hint 5：This guard is controlled only by initial variable values. If those values never change, the transition condition is effectively fixed.；`actions=add_write, simplify_guard；do_not=Do not add a meaningless self-assignment; it does not model a real change., Do not rewrite the guard to a meaningless constant only to silence this diagnostic.`
- hint 6：This guard is controlled only by initial variable values. If those values never change, the transition condition is effectively fixed.；`actions=add_write, simplify_guard；do_not=Do not add a meaningless self-assignment; it does not model a real change., Do not rewrite the guard to a meaningless constant only to silence this diagnostic.`
- forbidden_edits：`Do not delete grounded required elements merely to silence diagnostics., Do not invent internal plant/environment dynamics merely to make external input variables appear written.`。
- required_preserve_element_ids：`state:ZeroLoadCharge, state:ZeroLoadSpare, state:RESCoversCharge, state:RESCoversSpare, state:RESBatteryDischarge, state:LNGOnly, state:LNGBatteryAssist, state:LNGDG1, state:LNGDG1DG2, state:LowSoCLNGChargeMargin, state:LowSoCDGChargeMargin, state:AllThermalBatteryLack, ... +17`。

#### SL-9 per-request 决策

- accepted_request_ids：`<derived-from-table>`；candidate_len=`8193`。

| request_id | decision | waiver | rework_locked | rationale / intent |
|---|---|---:|---:|---|
| `fixreq-0-sd4-0-b906b8138a` | `accept` | ❌ | ✅ | Pbatmax is an NL-grounded external battery capacity input used in dispatch guards. The safe DSL edit does not fabricate internal writes for Pbatmax; it only restores missing aggregate command grounding requested by the local evidence.；intent=Preserve Pbatmax as a read-only external capacity input., Add NL-grounded aggregate command variables for generation/l...<truncated 17 chars> |
| `fixreq-0-sd4-1-52d9783dbe` | `accept` | ❌ | ✅ | The RESBatteryDischarge guard is intentionally controlled by external load, renewable, SoC, and battery-capacity inputs. No ungrounded input dynamics are added.；intent=Preserve external-input guard behavior., Add aggregate command outputs without changing dispatch selection. |
| `fixreq-0-sd4-2-c803effc60` | `accept` | ❌ | ✅ | The LNGOnly guard is NL-grounded as a capacity/demand classifier. The repair preserves it and adds missing command grounding.；intent=Keep LNGOnly guard unchanged., Represent aggregate generation/load cut commands explicitly. |
| `fixreq-0-sd4-3-ce18e2751a` | `accept` | ❌ | ✅ | The LNGBatteryAssist guard uses external demand/resource/capacity inputs as required by the NL. The edit is limited to grounded command outputs.；intent=Keep LNGBatteryAssist guard unchanged., Add aggregate command variables. |
| `fixreq-0-sd4-4-bf8c00283b` | `accept` | ❌ | ✅ | The LNGDG1 guard encodes the stated priority order using external inputs. It is preserved; the repair adds explicit aggregate command variables.；intent=Keep DG1 priority guard unchanged., Restore cmd_generation_cut and cmd_load_cut grounding. |
| `fixreq-0-sd4-5-95a78853f9` | `accept` | ❌ | ✅ | The transition to RESBatteryDischarge remains a guard-driven reclassification over external ship conditions. The edit does not alter this behavior.；intent=Preserve guard-driven reclassification., Add aggregate command assignments in state entry actions. |
| `fixreq-0-sd4-6-5f2d337ede` | `accept` | ❌ | ✅ | The transition to LNGOnly remains controlled by external conditions and capacity bounds. The repair avoids fabricated writes.；intent=Keep LNGOnly external-input guard., Add grounded aggregate commands. |
| `fixreq-0-sd4-7-cc0aa94e0f` | `accept` | ❌ | ✅ | The transition to LNGBatteryAssist is NL-grounded and read-only with respect to external inputs. Only command grounding is added.；intent=Keep LNGBatteryAssist guard unchanged., Add cmd_generation_cut and cmd_load_cut outputs. |
| `fixreq-0-sd4-8-12d7b1109d` | `accept` | ❌ | ✅ | The transition to LNGDG1 encodes diesel-generator priority and capacity comparison. The edit preserves it.；intent=Preserve LNGDG1 guard., Add aggregate command grounding. |
| `fixreq-0-sd4-9-2b6c71218f` | `accept` | ❌ | ✅ | The RESCoversCharge to RESBatteryDischarge reclassification remains driven by external operating inputs. The edit is local to command outputs.；intent=Preserve external-input transition logic., Add aggregate command variables. |
| `fixreq-0-sd4-10-6d13a0b4ed` | `accept` | ❌ | ✅ | The RESCoversCharge to LNGOnly guard remains NL-grounded. No artificial writes are introduced.；intent=Preserve LNGOnly guard., Restore missing aggregate command grounding. |
| `fixreq-0-sd4-11-6a2efdf143` | `accept` | ❌ | ✅ | The RESCoversCharge to LNGBatteryAssist transition remains part of the required twelve-state dispatch selection. The repair adds only grounded aggregate command outputs.；intent=Preserve LNGBatteryAssist guard., Add aggregate command variables and assignments. |
- repair_rationale：Accepted all requests because the selected warnings concern NL-grounded external inputs used by a guard-driven dispatch classifier; rejecting or deleting those guards would violate the NL.；Smallest DSL text change: add the required aggregate variables cmd_generation_cut and cmd_load_cut and assign them consistently from the already-grounded concrete cut-in/cut-out command actions.；The design_target_unresolved warning for Pbatmax is intentionally not repaired with a write because Pbatmax is an external battery capacity bound. Adding a self-assignment or fabricated capacity dynamics is explicitly forbidden and not NL-g...<truncated 8 chars>；The missing_required_grounding item variable:cmd_generation_cut is now directly represented by def int cmd_generation_cut and state entry assignments: 0 when no thermal generator is commanded, 1 when LNG/DG thermal generation is commanded.；The missing_required_grounding item variable:cmd_load_cut is now directly represented by def int cmd_load_cut and state entry assignments: 1 in zero-load cut-out states, 0 when load is served.
- diff_summary：`{"summary": "Added aggregate command variables cmd_generation_cut and cmd_load_cut plus grounded assignments in each state entry action. Preserved all twelve states, all forced guard transitions, and all dispatch power formulas; no fabricated writes were added for external input variables such as Pbatmax."}`。

#### SL-9 candidate / 最终修改执行方案

```pyfcstm
def float PL = 0.0;
def float Ppv = 0.0;
def float Pw = 0.0;
def float SoC = 0.0;
def float Pgmax = 0.0;
def float Pd1max = 0.0;
def float eng3_Pmax = 0.0;
def float Pbatmax = 0.0;
def float Pgen_req = 0.0;
def float Pbat_discharge = 0.0;
def float Pbat_charge = 0.0;
def float Pspare = 0.0;
def int cmd_generation_cut = 0;
def int cmd_load_cut = 0;
def int cmd_LNG_cut_in = 0;
def int cmd_LNG_cut_out = 0;
def int cmd_DG1_cut_in = 0;
def int cmd_DG1_cut_out = 0;
def int cmd_DG2_cut_in = 0;
def int cmd_DG2_cut_out = 0;
def int cmd_load_cut_in = 0;
def int cmd_load_cut_out = 0;

state LNGShipEMS {
    ! * -> ZeroLoadCharge : if [PL == 0 && Ppv + Pw > 0 && SoC < 0.95];
    ! * -> ZeroLoadSpare : if [PL == 0 && (Ppv + Pw <= 0 || SoC >= 0.95)];
    ! * -> RESCoversCharge : if [PL > 0 && Ppv + Pw >= PL && SoC < 0.95];
    ! * -> RESCoversSpare : if [PL > 0 && Ppv + Pw >= PL && SoC >= 0.95];
    ! * -> RESBatteryDischarge : if [PL > 0 && Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw <= Pbatmax];
    ! * -> LNGOnly : if [PL > 0 && Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw > Pbatmax && PL - Ppv - Pw <= Pgmax];
    ! * -> LNGBatteryAssist : if [PL > 0 && Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw > Pgmax && PL - Ppv - Pw <= Pgmax + Pbatmax];
    ! * -> LNGDG1 : if [PL > 0 && Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw > Pgmax + Pbatmax && PL - Ppv - Pw <= Pgmax + Pd1max];
    ! * -> LNGDG1DG2 : if [PL > 0 && Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw > Pgmax + Pd1max && PL - Ppv - Pw <= Pgmax + Pd1max + eng3_Pmax];
    ! * -> LowSoCLNGChargeMargin : if [PL > 0 && Ppv + Pw < PL && SoC < 0.2 && PL - Ppv - Pw + Pgmax / 5 <= Pgmax];
    ! * -> LowSoCDGChargeMargin : if [PL > 0 && Ppv + Pw < PL && SoC < 0.2 && PL - Ppv - Pw + Pgmax / 5 > Pgmax && PL - Ppv - Pw + Pd1max / 10 <= Pgmax + Pd1max];
    ! * -> AllThermalBatteryLack : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > Pgmax + Pd1max + eng3_Pmax];

    [*] -> ZeroLoadCharge;

    state ZeroLoadCharge {
        enter {
            Pgen_req = 0;
            Pbat_discharge = 0;
            Pbat_charge = Ppv + Pw;
            Pspare = 0;
            cmd_generation_cut = 0;
            cmd_load_cut = 1;
            cmd_LNG_cut_in = 0;
            cmd_LNG_cut_out = 1;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 0;
            cmd_load_cut_out = 1;
        }
    }

    state ZeroLoadSpare {
        enter {
            Pgen_req = 0;
            Pbat_discharge = 0;
            Pbat_charge = 0;
            Pspare = Ppv + Pw;
            cmd_generation_cut = 0;
            cmd_load_cut = 1;
            cmd_LNG_cut_in = 0;
            cmd_LNG_cut_out = 1;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 0;
            cmd_load_cut_out = 1;
        }
    }

    state RESCoversCharge {
        enter {
            Pgen_req = 0;
            Pbat_discharge = 0;
            Pbat_charge = Ppv + Pw - PL;
            Pspare = 0;
            cmd_generation_cut = 0;
            cmd_load_cut = 0;
            cmd_LNG_cut_in = 0;
            cmd_LNG_cut_out = 1;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state RESCoversSpare {
        enter {
            Pgen_req = 0;
            Pbat_discharge = 0;
            Pbat_charge = 0;
            Pspare = Ppv + Pw - PL;
            cmd_generation_cut = 0;
            cmd_load_cut = 0;
            cmd_LNG_cut_in = 0;
            cmd_LNG_cut_out = 1;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state RESBatteryDischarge {
        enter {
            Pgen_req = 0;
            Pbat_discharge = PL - Ppv - Pw;
            Pbat_charge = 0;
            Pspare = 0;
            cmd_generation_cut = 0;
            cmd_load_cut = 0;
            cmd_LNG_cut_in = 0;
            cmd_LNG_cut_out = 1;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state LNGOnly {
        enter {
            Pgen_req = PL - Ppv - Pw;
            Pbat_discharge = 0;
            Pbat_charge = 0;
            Pspare = 0;
            cmd_generation_cut = 1;
            cmd_load_cut = 0;
            cmd_LNG_cut_in = 1;
            cmd_LNG_cut_out = 0;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state LNGBatteryAssist {
        enter {
            Pgen_req = Pgmax;
            Pbat_discharge = PL - Ppv - Pw - Pgmax;
            Pbat_charge = 0;
            Pspare = 0;
            cmd_generation_cut = 1;
            cmd_load_cut = 0;
            cmd_LNG_cut_in = 1;
            cmd_LNG_cut_out = 0;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state LNGDG1 {
        enter {
            Pgen_req = PL - Ppv - Pw;
            Pbat_discharge = 0;
            Pbat_charge = 0;
            Pspare = 0;
            cmd_generation_cut = 1;
            cmd_load_cut = 0;
            cmd_LNG_cut_in = 1;
            cmd_LNG_cut_out = 0;
            cmd_DG1_cut_in = 1;
            cmd_DG1_cut_out = 0;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state LNGDG1DG2 {
        enter {
            Pgen_req = PL - Ppv - Pw;
            Pbat_discharge = 0;
            Pbat_charge = 0;
            Pspare = 0;
            cmd_generation_cut = 1;
            cmd_load_cut = 0;
            cmd_LNG_cut_in = 1;
            cmd_LNG_cut_out = 0;
            cmd_DG1_cut_in = 1;
            cmd_DG1_cut_out = 0;
            cmd_DG2_cut_in = 1;
            cmd_DG2_cut_out = 0;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state LowSoCLNGChargeMargin {
        enter {
            Pgen_req = PL - Ppv - Pw + Pgmax / 5;
            Pbat_discharge = 0;
            Pbat_charge = Pgmax / 5;
            Pspare = 0;
            cmd_generation_cut = 1;
            cmd_load_cut = 0;
            cmd_LNG_cut_in = 1;
            cmd_LNG_cut_out = 0;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state LowSoCDGChargeMargin {
        enter {
            Pgen_req = PL - Ppv - Pw + Pd1max / 10;
            Pbat_discharge = 0;
            Pbat_charge = Pd1max / 10;
            Pspare = 0;
            cmd_generation_cut = 1;
            cmd_load_cut = 0;
            cmd_LNG_cut_in = 1;
            cmd_LNG_cut_out = 0;
            cmd_DG1_cut_in = 1;
            cmd_DG1_cut_out = 0;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state AllThermalBatteryLack {
        enter {
            Pgen_req = Pgmax + Pd1max + eng3_Pmax;
            Pbat_discharge = PL - Ppv - Pw - Pgmax - Pd1max - eng3_Pmax;
            Pbat_charge = 0;
            Pspare = 0;
            cmd_generation_cut = 1;
            cmd_load_cut = 0;
            cmd_LNG_cut_in = 1;
            cmd_LNG_cut_out = 0;
            cmd_DG1_cut_in = 1;
            cmd_DG1_cut_out = 0;
            cmd_DG2_cut_in = 1;
            cmd_DG2_cut_out = 0;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }
}
```

#### Candidate diff（before -> candidate）

```diff
--- before.fcstm
+++ candidate.fcstm
@@ -10,6 +10,8 @@
 def float Pbat_discharge = 0.0;
 def float Pbat_charge = 0.0;
 def float Pspare = 0.0;
+def int cmd_generation_cut = 0;
+def int cmd_load_cut = 0;
 def int cmd_LNG_cut_in = 0;
 def int cmd_LNG_cut_out = 0;
 def int cmd_DG1_cut_in = 0;
@@ -41,6 +43,8 @@
             Pbat_discharge = 0;
             Pbat_charge = Ppv + Pw;
             Pspare = 0;
+            cmd_generation_cut = 0;
+            cmd_load_cut = 1;
             cmd_LNG_cut_in = 0;
             cmd_LNG_cut_out = 1;
             cmd_DG1_cut_in = 0;
@@ -58,6 +62,8 @@
             Pbat_discharge = 0;
             Pbat_charge = 0;
             Pspare = Ppv + Pw;
+            cmd_generation_cut = 0;
+            cmd_load_cut = 1;
             cmd_LNG_cut_in = 0;
             cmd_LNG_cut_out = 1;
             cmd_DG1_cut_in = 0;
@@ -75,6 +81,8 @@
             Pbat_discharge = 0;
             Pbat_charge = Ppv + Pw - PL;
             Pspare = 0;
+            cmd_generation_cut = 0;
+            cmd_load_cut = 0;
             cmd_LNG_cut_in = 0;
             cmd_LNG_cut_out = 1;
             cmd_DG1_cut_in = 0;
@@ -92,6 +100,8 @@
             Pbat_discharge = 0;
             Pbat_charge = 0;
             Pspare = Ppv + Pw - PL;
+            cmd_generation_cut = 0;
+            cmd_load_cut = 0;
             cmd_LNG_cut_in = 0;
             cmd_LNG_cut_out = 1;
             cmd_DG1_cut_in = 0;
@@ -109,6 +119,8 @@
             Pbat_discharge = PL - Ppv - Pw;
             Pbat_charge = 0;
             Pspare = 0;
+            cmd_generation_cut = 0;
+            cmd_load_cut = 0;
             cmd_LNG_cut_in = 0;
             cmd_LNG_cut_out = 1;
             cmd_DG1_cut_in = 0;
@@ -126,6 +138,8 @@
             Pbat_discharge = 0;
             Pbat_charge = 0;
             Pspare = 0;
+            cmd_generation_cut = 1;
+            cmd_load_cut = 0;
             cmd_LNG_cut_in = 1;
             cmd_LNG_cut_out = 0;
             cmd_DG1_cut_in = 0;
@@ -143,6 +157,8 @@
             Pbat_discharge = PL - Ppv - Pw - Pgmax;
             Pbat_charge = 0;
             Pspare = 0;
+            cmd_generation_cut = 1;
+            cmd_load_cut = 0;
             cmd_LNG_cut_in = 1;
             cmd_LNG_cut_out = 0;
             cmd_DG1_cut_in = 0;
@@ -160,6 +176,8 @@
             Pbat_discharge = 0;
             Pbat_charge = 0;
             Pspare = 0;
+            cmd_generation_cut = 1;
+            cmd_load_cut = 0;
             cmd_LNG_cut_in = 1;
             cmd_LNG_cut_out = 0;
             cmd_DG1_cut_in = 1;
@@ -177,6 +195,8 @@
             Pbat_discharge = 0;
             Pbat_charge = 0;
             Pspare = 0;
+            cmd_generation_cut = 1;
+            cmd_load_cut = 0;
             cmd_LNG_cut_in = 1;
             cmd_LNG_cut_out = 0;
             cmd_DG1_cut_in = 1;
@@ -194,6 +214,8 @@
             Pbat_discharge = 0;
             Pbat_charge = Pgmax / 5;
             Pspare = 0;
+            cmd_generation_cut = 1;
+            cmd_load_cut = 0;
             cmd_LNG_cut_in = 1;
             cmd_LNG_cut_out = 0;
             cmd_DG1_cut_in = 0;
@@ -211,6 +233,8 @@
             Pbat_discharge = 0;
             Pbat_charge = Pd1max / 10;
             Pspare = 0;
+            cmd_generation_cut = 1;
+            cmd_load_cut = 0;
             cmd_LNG_cut_in = 1;
             cmd_LNG_cut_out = 0;
             cmd_DG1_cut_in = 1;
@@ -228,6 +252,8 @@
             Pbat_discharge = PL - Ppv - Pw - Pgmax - Pd1max - eng3_Pmax;
             Pbat_charge = 0;
             Pspare = 0;
+            cmd_generation_cut = 1;
+            cmd_load_cut = 0;
             cmd_LNG_cut_in = 1;
             cmd_LNG_cut_out = 0;
             cmd_DG1_cut_in = 1;
```

#### SL-10 审查结果

- SL-10 decision=`pass`，ok=`True`，target_resolved=`True`，regression_detected=`False`，drift_risk=`minor`。
- SL-10 review_meta：schema=`SL10RepairReviewOutput.v1`，failure_policy=`fail_closed`，replay_key=`SL-10:sha256:c208d24c471663951f24acdaf7eb2a0f916a0a20fc7248cfdda3079ed08f2a22`。
  - SL-10 evidence 1: `{"summary": "The candidate preserves all twelve NL-required dispatch states and their existing guard/action semantics: zero-load charge/spare, RES-covers charge/spare, RES plus battery discharge, LNG-only, LNG plus battery assist, LNG plus DG1, LNG plus DG1 plus DG2, low-SoC LNG charging margin using Pgmax/5, low-SoC DG charging margin using Pd1max/10, and all-thermal plus battery-lack overload handling."}`
  - SL-10 evidence 2: `{"summary": "The DSL diff is narrow and NL-grounded: it adds def int cmd_generation_cut and def int cmd_load_cut plus assignments in every state entry action, while preserving the existing concrete cut-in/cut-out command variables for LNG, DG1, DG2, and loads. No dispatch guard, state count, power formula, or thermal/battery priority behavior was removed or weakened."}`
  - SL-10 evidence 3: `{"summary": "All SL-9 per-request decisions accept the warning repairs by preserving PL, Ppv, Pw, SoC, Pbatmax, Pgmax, Pd1max, and eng3_Pmax as external inputs/capacity bounds. This follows the NL, which says the FSM reads load, renewable, SoC, and capacity bounds and selects states by logical conditions over those inputs; it does not define internal plant dynamics that would write these inputs."}`
  - SL-10 evidence 4: `{"summary": "The complete FixLog and repair_memory show the prior rework objection was not a behavior regression but insufficient SL-10 override rationale for local major drift. The current candidate also implements the actionable local-only edit requested in that memory by adding direct aggregate command variables, while preserving the non-regressive frontier behavior."}`
  - SL-10 evidence 5: `{"summary": "The local check still reports design_target_unresolved and missing_required_grounding with major drift, but no scenario_regression is reported. The remaining deterministic objections are conservative/matcher objections against an NL-faithful external-input classifier and abstract transition grounding, not evidence that a required NL state, action, guard, or scenario obligation was dropped."}`
  - SL-10 evidence 6: `{"candidate_dsl_hash": "sha256:942ea1f43a9376d06509746a7e409cc8c830ac52275db43c84b69211068dfa22", "covered_local_objection_kinds": ["design_target_unresolved", "missing_required_grounding"], "kind": "local_major_drift_override_audit", "local_check_evidence_hash": "sha256:4bd87a8498f1d1c2b7b488113a672deaa717241141349868873590ddf47aea49", "local_override_rationale_count": 6, "local_override_rationale_hash": "sha256:771ff70d03daeb8acd93020b19b928891ced2337e8d8e551b4d3a54b08c5490f", "local_rejection_evidence_hash": "sha256:ec532d7f9d59bc024273b7a8a36278b233615ec0db6f4682916a3ad5766fa896", "local_rejection_reason": "design_target_unresolved; missing_required_grounding", "missing_local_objection_k...<truncated 350 chars>`
- local checks evidence：stage=`SD-10`；note=PR-E1 uses local parse/semantic/design/sim checks as SL-10 evidence, not as the final deterministic judge.。
  - local ok=`False`，target_resolved=`False`，regression_detected=`False`，drift_risk=`major`。
  - local_rejection：reason=`design_target_unresolved; missing_required_grounding`，rejected_by_stage=`SD-10`。
    - local evidence 1: `design_target_unresolved` {"items": [{"budget_exhausted": false, "budget_remaining": 1, "code": "W_UNWRITTEN_READ_VAR", "instance_key": "W_UNWRITTEN_READ_VAR:var_name=Pbatmax", "message": "Variable 'Pbatmax' is read but never written by any action or transition effect.", "policy_action": "budgeted_repair", "pyfcstm_severity": "warning", "rationale": "", "refs": {"init_value": "0.0", "read_states": ["LNGShipEMS.AllThermalBatteryLack", "LNGShipEMS.LNGBatteryAssist", "LNGShipEMS.LNGDG1", "LNGShipEMS.LNGDG1DG2", "LNGShipEMS....<truncated 59126 chars>
    - local evidence 2: `missing_required_grounding` {"element_ids": ["variable:cmd_generation_cut", "variable:cmd_load_cut", "transition:select_deficit_priority", "transition:select_low_soc_margins"], "kind": "missing_required_grounding"}

</details>

<details><summary>Repair 3 / iteration `1` / source `SD-4` / accepted=✅</summary>

#### 为什么进入修复

- selected feedback source：`SD-4`；blocking=`True`；pre_scenario=`True`。
- problem_summary：Variable 'Pbatmax' is read but never written by any action or transition effect.; Transition guard reads only variables that are never changed by actions or effects.; Transition guard reads only variables that are never changed by actions or effects.
- diagnostic ids：`W_UNWRITTEN_READ_VAR:var_name=Pbatmax, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.RESBatteryDischarge, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.LNGOnly, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.LNGBatteryAssist, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.LNGDG1, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadSpare:to_path=LNGShipEMS.RESBatteryDischarge, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadSpare:to_path=LNGShipEMS.LNGOnly, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadSpare:to_path=LNGShipEMS.LNGBatteryAssist, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadSpare:to_path=LNGShipEMS.LNGDG1, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.RESCoversCharge:to_path=LNGShipEMS.RESBatteryDischarge, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.RESCoversCharge:to_path=LNGShipEMS.LNGOnly, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.RESCoversCharge:to_path=LNGShipEMS.LNGBatteryAssist, ... +41`。
- before_dsl_hash：`sha256:942ea1f43a9376d06509746a7e409cc8c830ac52275db43c84b69211068dfa22`；candidate_dsl_hash：`sha256:942ea1f43a9376d06509746a7e409cc8c830ac52275db43c84b69211068dfa22`。

#### 错误证据 / diagnostics

- 1. `W_UNWRITTEN_READ_VAR` `W_UNWRITTEN_READ_VAR:var_name=Pbatmax` policy=`budgeted_repair`：Variable 'Pbatmax' is read but never written by any action or transition effect.；refs=`{"init_value": "0.0", "read_states": ["LNGShipEMS.AllThermalBatteryLack", "LNGShipEMS.LNGBatteryAssist", "LNGShipEMS.LNGDG1", "LNGShipEMS.LNGDG1DG2", "LNGShipEMS.LNGOnly", "LNGShipEMS.LowSoCDGChargeMargin", "LNGShipEMS.LowSoCLNGChargeMargin", "LNGShipEMS.RESBatteryDischarge", "LNGShipEMS.RESCoversCh...<truncated 116 chars>`
- 2. `W_GUARD_VARS_NEVER_CHANGE` `W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.RESBatteryDischarge` policy=`budgeted_repair`：Transition guard reads only variables that are never changed by actions or effects.；refs=`{"from_path": "LNGShipEMS.ZeroLoadCharge", "guard_vars": ["PL", "Pbatmax", "Ppv", "Pw", "SoC"], "to_path": "LNGShipEMS.RESBatteryDischarge"}`
- 3. `W_GUARD_VARS_NEVER_CHANGE` `W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.LNGOnly` policy=`budgeted_repair`：Transition guard reads only variables that are never changed by actions or effects.；refs=`{"from_path": "LNGShipEMS.ZeroLoadCharge", "guard_vars": ["PL", "Pbatmax", "Pgmax", "Ppv", "Pw", "SoC"], "to_path": "LNGShipEMS.LNGOnly"}`
- 4. `W_GUARD_VARS_NEVER_CHANGE` `W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.LNGBatteryAssist` policy=`budgeted_repair`：Transition guard reads only variables that are never changed by actions or effects.；refs=`{"from_path": "LNGShipEMS.ZeroLoadCharge", "guard_vars": ["PL", "Pbatmax", "Pgmax", "Ppv", "Pw", "SoC"], "to_path": "LNGShipEMS.LNGBatteryAssist"}`
- 5. `W_GUARD_VARS_NEVER_CHANGE` `W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.LNGDG1` policy=`budgeted_repair`：Transition guard reads only variables that are never changed by actions or effects.；refs=`{"from_path": "LNGShipEMS.ZeroLoadCharge", "guard_vars": ["PL", "Pbatmax", "Pd1max", "Pgmax", "Ppv", "Pw", "SoC"], "to_path": "LNGShipEMS.LNGDG1"}`
- 6. `W_GUARD_VARS_NEVER_CHANGE` `W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadSpare:to_path=LNGShipEMS.RESBatteryDischarge` policy=`budgeted_repair`：Transition guard reads only variables that are never changed by actions or effects.；refs=`{"from_path": "LNGShipEMS.ZeroLoadSpare", "guard_vars": ["PL", "Pbatmax", "Ppv", "Pw", "SoC"], "to_path": "LNGShipEMS.RESBatteryDischarge"}`
- 7. `W_GUARD_VARS_NEVER_CHANGE` `W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadSpare:to_path=LNGShipEMS.LNGOnly` policy=`budgeted_repair`：Transition guard reads only variables that are never changed by actions or effects.；refs=`{"from_path": "LNGShipEMS.ZeroLoadSpare", "guard_vars": ["PL", "Pbatmax", "Pgmax", "Ppv", "Pw", "SoC"], "to_path": "LNGShipEMS.LNGOnly"}`
- 8. `W_GUARD_VARS_NEVER_CHANGE` `W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadSpare:to_path=LNGShipEMS.LNGBatteryAssist` policy=`budgeted_repair`：Transition guard reads only variables that are never changed by actions or effects.；refs=`{"from_path": "LNGShipEMS.ZeroLoadSpare", "guard_vars": ["PL", "Pbatmax", "Pgmax", "Ppv", "Pw", "SoC"], "to_path": "LNGShipEMS.LNGBatteryAssist"}`
- ……另有 `41` 条 evidence 见 run record。

#### 变量角色与上下文提示

- policy：Advisory only. Do not invent writes for external_input_candidate variables unless NL explicitly gives update semantics; add meaningful NL-grounded writes only for internal state variables.
- source：SD-4 diagnostic refs and generic NL external-input rationale

| Variable | role_hint | nl_token_present | diagnostics |
|---|---|---:|---|
| `PL` | `external_input_candidate` | ✅ | `W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +140` |
| `Pbat_charge` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `Pbat_discharge` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `Pbatmax` | `unknown` | ❌ | `W_UNWRITTEN_READ_VAR, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +44` |
| `Pd1max` | `external_input_candidate` | ✅ | `W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +44` |
| `Pgen_req` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `Pgmax` | `external_input_candidate` | ✅ | `W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +80` |
| `Ppv` | `external_input_candidate` | ✅ | `W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +140` |
| `Pspare` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `Pw` | `external_input_candidate` | ✅ | `W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +140` |
| `SoC` | `external_input_candidate` | ✅ | `W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +128` |
| `cmd_DG1_cut_in` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `cmd_DG1_cut_out` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `cmd_DG2_cut_in` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `cmd_DG2_cut_out` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `cmd_LNG_cut_in` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `cmd_LNG_cut_out` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `cmd_generation_cut` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `cmd_load_cut` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `cmd_load_cut_in` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `cmd_load_cut_out` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `eng3_Pmax` | `external_input_candidate` | ✅ | `W_UNWRITTEN_READ_VAR, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +20` |

#### SD-8 FixRequestBatch / 修改请求

- batch_id：`fixbatch-1-sha256-4686297540a`；source_stage=`SD-4`；legacy_plan_kind=`FixPlan`；requests=`12`。

| request_id | severity | hard | waiver | problem | evidence |
|---|---|---:|---:|---|---|
| `fixreq-1-sd4-0-ee0165aae2` | `blocking_warning` | ❌ | ✅ | Variable 'Pbatmax' is read but never written by any action or transition effect.; Transition guard reads only variables that are never changed by actions or effects.; Transition guard reads only variables that are never ...<truncated 30 chars> | `W_UNWRITTEN_READ_VAR` |
| `fixreq-1-sd4-1-401c0a6419` | `blocking_warning` | ❌ | ✅ | Variable 'Pbatmax' is read but never written by any action or transition effect.; Transition guard reads only variables that are never changed by actions or effects.; Transition guard reads only variables that are never ...<truncated 30 chars> | `W_GUARD_VARS_NEVER_CHANGE` |
| `fixreq-1-sd4-2-0f3f4b8d5f` | `blocking_warning` | ❌ | ✅ | Variable 'Pbatmax' is read but never written by any action or transition effect.; Transition guard reads only variables that are never changed by actions or effects.; Transition guard reads only variables that are never ...<truncated 30 chars> | `W_GUARD_VARS_NEVER_CHANGE` |
| `fixreq-1-sd4-3-d6f0b92185` | `blocking_warning` | ❌ | ✅ | Variable 'Pbatmax' is read but never written by any action or transition effect.; Transition guard reads only variables that are never changed by actions or effects.; Transition guard reads only variables that are never ...<truncated 30 chars> | `W_GUARD_VARS_NEVER_CHANGE` |
| `fixreq-1-sd4-4-0eab567340` | `blocking_warning` | ❌ | ✅ | Variable 'Pbatmax' is read but never written by any action or transition effect.; Transition guard reads only variables that are never changed by actions or effects.; Transition guard reads only variables that are never ...<truncated 30 chars> | `W_GUARD_VARS_NEVER_CHANGE` |
| `fixreq-1-sd4-5-c98274b9b8` | `blocking_warning` | ❌ | ✅ | Variable 'Pbatmax' is read but never written by any action or transition effect.; Transition guard reads only variables that are never changed by actions or effects.; Transition guard reads only variables that are never ...<truncated 30 chars> | `W_GUARD_VARS_NEVER_CHANGE` |
| `fixreq-1-sd4-6-ef59e1a304` | `blocking_warning` | ❌ | ✅ | Variable 'Pbatmax' is read but never written by any action or transition effect.; Transition guard reads only variables that are never changed by actions or effects.; Transition guard reads only variables that are never ...<truncated 30 chars> | `W_GUARD_VARS_NEVER_CHANGE` |
| `fixreq-1-sd4-7-accddd8d40` | `blocking_warning` | ❌ | ✅ | Variable 'Pbatmax' is read but never written by any action or transition effect.; Transition guard reads only variables that are never changed by actions or effects.; Transition guard reads only variables that are never ...<truncated 30 chars> | `W_GUARD_VARS_NEVER_CHANGE` |
| `fixreq-1-sd4-8-7988f601ed` | `blocking_warning` | ❌ | ✅ | Variable 'Pbatmax' is read but never written by any action or transition effect.; Transition guard reads only variables that are never changed by actions or effects.; Transition guard reads only variables that are never ...<truncated 30 chars> | `W_GUARD_VARS_NEVER_CHANGE` |
| `fixreq-1-sd4-9-cd4b9656e7` | `blocking_warning` | ❌ | ✅ | Variable 'Pbatmax' is read but never written by any action or transition effect.; Transition guard reads only variables that are never changed by actions or effects.; Transition guard reads only variables that are never ...<truncated 30 chars> | `W_GUARD_VARS_NEVER_CHANGE` |
- ……另有 `2` 个 request 见 run record。

#### SD-8 legacy fix plan / 修改建议

- recommended_strategy：Use diagnostics as hints; choose the smallest globally consistent repair.；Before returning a candidate, verify every required_preserve_element_id still has a concrete DSL representation.
- hint 1：The variable is used as input but never updated after its initial definition, so model behavior may be accidentally constant.；`actions=add_write, simplify_guard；do_not=Do not add a meaningless self-assignment.`
- hint 2：This guard is controlled only by initial variable values. If those values never change, the transition condition is effectively fixed.；`actions=add_write, simplify_guard；do_not=Do not add a meaningless self-assignment; it does not model a real change., Do not rewrite the guard to a meaningless constant only to silence this diagnostic.`
- hint 3：This guard is controlled only by initial variable values. If those values never change, the transition condition is effectively fixed.；`actions=add_write, simplify_guard；do_not=Do not add a meaningless self-assignment; it does not model a real change., Do not rewrite the guard to a meaningless constant only to silence this diagnostic.`
- hint 4：This guard is controlled only by initial variable values. If those values never change, the transition condition is effectively fixed.；`actions=add_write, simplify_guard；do_not=Do not add a meaningless self-assignment; it does not model a real change., Do not rewrite the guard to a meaningless constant only to silence this diagnostic.`
- hint 5：This guard is controlled only by initial variable values. If those values never change, the transition condition is effectively fixed.；`actions=add_write, simplify_guard；do_not=Do not add a meaningless self-assignment; it does not model a real change., Do not rewrite the guard to a meaningless constant only to silence this diagnostic.`
- hint 6：This guard is controlled only by initial variable values. If those values never change, the transition condition is effectively fixed.；`actions=add_write, simplify_guard；do_not=Do not add a meaningless self-assignment; it does not model a real change., Do not rewrite the guard to a meaningless constant only to silence this diagnostic.`
- forbidden_edits：`Do not delete grounded required elements merely to silence diagnostics., Do not invent internal plant/environment dynamics merely to make external input variables appear written.`。
- required_preserve_element_ids：`state:ZeroLoadCharge, state:ZeroLoadSpare, state:RESCoversCharge, state:RESCoversSpare, state:RESBatteryDischarge, state:LNGOnly, state:LNGBatteryAssist, state:LNGDG1, state:LNGDG1DG2, state:LowSoCLNGChargeMargin, state:LowSoCDGChargeMargin, state:AllThermalBatteryLack, ... +17`。

#### SL-9 per-request 决策

- accepted_request_ids：`<derived-from-table>`；candidate_len=`8193`。

| request_id | decision | waiver | rework_locked | rationale / intent |
|---|---|---:|---:|---|
| `fixreq-1-sd4-0-ee0165aae2` | `accept` | ❌ | ❌ | Pbatmax is an NL-grounded external battery-capacity input used to classify dispatch branches. The NL says the EMS reads load, renewable, SoC, and capacity-bound inputs; it gives no internal dynamics that would write Pbatmax. A synthetic write or self-assignment would be ungrounded and forbidden.；intent=Preserve Pbatmax as read-only external input, Preserve t...<truncated 74 chars> |
| `fixreq-1-sd4-1-401c0a6419` | `accept` | ❌ | ❌ | The RESBatteryDischarge guard is intentionally controlled by external operating inputs PL, Ppv, Pw, SoC, and Pbatmax. This matches the NL requirement that states are selected by logical conditions over demand, generation, capacity, and SoC.；intent=Keep the NL-grounded RES plus battery discharge guard unchanged |
| `fixreq-1-sd4-2-0f3f4b8d5f` | `accept` | ❌ | ❌ | The LNGOnly guard depends on externally supplied demand/resource/capacity values and represents the LNG-before-diesel dispatch branch. No NL-grounded internal write exists for these guard inputs.；intent=Keep the LNGOnly capacity guard unchanged |
| `fixreq-1-sd4-3-d6f0b92185` | `accept` | ❌ | ❌ | The LNGBatteryAssist guard uses external load, renewable, SoC, battery, and LNG capacity inputs to choose LNG plus battery discharge. This is required by the NL and should not be replaced with fabricated state updates.；intent=Keep the LNG plus battery assist guard unchanged |
| `fixreq-1-sd4-4-0eab567340` | `accept` | ❌ | ❌ | The LNGDG1 guard encodes the stated priority order and diesel-generator capacity threshold using external inputs. Adding artificial writes would reduce NL fidelity.；intent=Preserve the DG1 priority guard |
| `fixreq-1-sd4-5-c98274b9b8` | `accept` | ❌ | ❌ | The transition to RESBatteryDischarge from ZeroLoadSpare remains a guard-driven reclassification over externally changing ship conditions. The EMS reads these inputs rather than evolving them internally.；intent=Preserve external-input guard semantics |
| `fixreq-1-sd4-6-ef59e1a304` | `accept` | ❌ | ❌ | The transition to LNGOnly is controlled by external operating conditions and capacity bounds as required by the NL. No safe internal update is available.；intent=Keep LNGOnly guard unchanged |
| `fixreq-1-sd4-7-accddd8d40` | `accept` | ❌ | ❌ | The transition to LNGBatteryAssist correctly reads external load, RES, SoC, and capacity inputs. It should remain a classifier guard rather than introduce ungrounded plant dynamics.；intent=Keep LNGBatteryAssist guard unchanged |
| `fixreq-1-sd4-8-7988f601ed` | `accept` | ❌ | ❌ | The transition to LNGDG1 represents diesel-generator priority and capacity comparison over external inputs. The NL does not require the EMS to write those inputs.；intent=Preserve LNGDG1 guard |
| `fixreq-1-sd4-9-cd4b9656e7` | `accept` | ❌ | ❌ | The RESCoversCharge to RESBatteryDischarge reclassification is intentionally driven by externally supplied demand, renewable, SoC, and battery-capacity values.；intent=Preserve external-input transition logic |
| `fixreq-1-sd4-10-fb7834716d` | `accept` | ❌ | ❌ | The RESCoversCharge to LNGOnly guard is NL-grounded as a demand/capacity classifier and should not be simplified to a constant or modified with meaningless writes.；intent=Preserve LNGOnly external-input guard |
| `fixreq-1-sd4-11-6815e5b14f` | `accept` | ❌ | ❌ | The RESCoversCharge to LNGBatteryAssist transition is part of the twelve-state dispatch selection over external inputs. The current DSL already preserves the required command grounding.；intent=Preserve LNGBatteryAssist guard and aggregate command outputs |
- repair_rationale：Smallest safe edit is conservative preservation of the current DSL. The current candidate is the previously SL-10-accepted candidate hash and already contains the aggregate variables cmd_generation_cut and cmd_load_cut plus assignments in e...<truncated 101 chars>；The new batch repeats W_UNWRITTEN_READ_VAR and W_GUARD_VARS_NEVER_CHANGE on external-input classifier variables. PL, Ppv, Pw, SoC, Pbatmax, Pgmax, Pd1max, and eng3_Pmax are read inputs/capacity bounds per the NL, not EMS-internal state vari...<truncated 94 chars>；Preserved all twelve required dispatch states: zero-load charge/spare, RES-covers charge/spare, RESBatteryDischarge, LNGOnly, LNGBatteryAssist, LNGDG1, LNGDG1DG2, LowSoCLNGChargeMargin, LowSoCDGChargeMargin, and AllThermalBatteryLack.；Preserved transition:select_deficit_priority as the concrete forced guards to RESBatteryDischarge, LNGOnly, LNGBatteryAssist, LNGDG1, and LNGDG1DG2, encoding RES first, battery when SoC/capacity allows, LNG before diesel, and DG1/DG2 last.；Preserved transition:select_low_soc_margins as the concrete forced guards to LowSoCLNGChargeMargin and LowSoCDGChargeMargin, with entry actions using Pgmax / 5 and Pd1max / 10 charging margins.
- diff_summary：`{"summary": "No DSL text changed from the current candidate. Preserves the SL-10-accepted aggregate command variables and all twelve NL-grounded guard-driven dispatch branches; avoids ungrounded writes to external input/capacity variables."}`。

#### SL-9 candidate / 最终修改执行方案

```pyfcstm
def float PL = 0.0;
def float Ppv = 0.0;
def float Pw = 0.0;
def float SoC = 0.0;
def float Pgmax = 0.0;
def float Pd1max = 0.0;
def float eng3_Pmax = 0.0;
def float Pbatmax = 0.0;
def float Pgen_req = 0.0;
def float Pbat_discharge = 0.0;
def float Pbat_charge = 0.0;
def float Pspare = 0.0;
def int cmd_generation_cut = 0;
def int cmd_load_cut = 0;
def int cmd_LNG_cut_in = 0;
def int cmd_LNG_cut_out = 0;
def int cmd_DG1_cut_in = 0;
def int cmd_DG1_cut_out = 0;
def int cmd_DG2_cut_in = 0;
def int cmd_DG2_cut_out = 0;
def int cmd_load_cut_in = 0;
def int cmd_load_cut_out = 0;

state LNGShipEMS {
    ! * -> ZeroLoadCharge : if [PL == 0 && Ppv + Pw > 0 && SoC < 0.95];
    ! * -> ZeroLoadSpare : if [PL == 0 && (Ppv + Pw <= 0 || SoC >= 0.95)];
    ! * -> RESCoversCharge : if [PL > 0 && Ppv + Pw >= PL && SoC < 0.95];
    ! * -> RESCoversSpare : if [PL > 0 && Ppv + Pw >= PL && SoC >= 0.95];
    ! * -> RESBatteryDischarge : if [PL > 0 && Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw <= Pbatmax];
    ! * -> LNGOnly : if [PL > 0 && Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw > Pbatmax && PL - Ppv - Pw <= Pgmax];
    ! * -> LNGBatteryAssist : if [PL > 0 && Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw > Pgmax && PL - Ppv - Pw <= Pgmax + Pbatmax];
    ! * -> LNGDG1 : if [PL > 0 && Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw > Pgmax + Pbatmax && PL - Ppv - Pw <= Pgmax + Pd1max];
    ! * -> LNGDG1DG2 : if [PL > 0 && Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw > Pgmax + Pd1max && PL - Ppv - Pw <= Pgmax + Pd1max + eng3_Pmax];
    ! * -> LowSoCLNGChargeMargin : if [PL > 0 && Ppv + Pw < PL && SoC < 0.2 && PL - Ppv - Pw + Pgmax / 5 <= Pgmax];
    ! * -> LowSoCDGChargeMargin : if [PL > 0 && Ppv + Pw < PL && SoC < 0.2 && PL - Ppv - Pw + Pgmax / 5 > Pgmax && PL - Ppv - Pw + Pd1max / 10 <= Pgmax + Pd1max];
    ! * -> AllThermalBatteryLack : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > Pgmax + Pd1max + eng3_Pmax];

    [*] -> ZeroLoadCharge;

    state ZeroLoadCharge {
        enter {
            Pgen_req = 0;
            Pbat_discharge = 0;
            Pbat_charge = Ppv + Pw;
            Pspare = 0;
            cmd_generation_cut = 0;
            cmd_load_cut = 1;
            cmd_LNG_cut_in = 0;
            cmd_LNG_cut_out = 1;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 0;
            cmd_load_cut_out = 1;
        }
    }

    state ZeroLoadSpare {
        enter {
            Pgen_req = 0;
            Pbat_discharge = 0;
            Pbat_charge = 0;
            Pspare = Ppv + Pw;
            cmd_generation_cut = 0;
            cmd_load_cut = 1;
            cmd_LNG_cut_in = 0;
            cmd_LNG_cut_out = 1;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 0;
            cmd_load_cut_out = 1;
        }
    }

    state RESCoversCharge {
        enter {
            Pgen_req = 0;
            Pbat_discharge = 0;
            Pbat_charge = Ppv + Pw - PL;
            Pspare = 0;
            cmd_generation_cut = 0;
            cmd_load_cut = 0;
            cmd_LNG_cut_in = 0;
            cmd_LNG_cut_out = 1;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state RESCoversSpare {
        enter {
            Pgen_req = 0;
            Pbat_discharge = 0;
            Pbat_charge = 0;
            Pspare = Ppv + Pw - PL;
            cmd_generation_cut = 0;
            cmd_load_cut = 0;
            cmd_LNG_cut_in = 0;
            cmd_LNG_cut_out = 1;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state RESBatteryDischarge {
        enter {
            Pgen_req = 0;
            Pbat_discharge = PL - Ppv - Pw;
            Pbat_charge = 0;
            Pspare = 0;
            cmd_generation_cut = 0;
            cmd_load_cut = 0;
            cmd_LNG_cut_in = 0;
            cmd_LNG_cut_out = 1;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state LNGOnly {
        enter {
            Pgen_req = PL - Ppv - Pw;
            Pbat_discharge = 0;
            Pbat_charge = 0;
            Pspare = 0;
            cmd_generation_cut = 1;
            cmd_load_cut = 0;
            cmd_LNG_cut_in = 1;
            cmd_LNG_cut_out = 0;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state LNGBatteryAssist {
        enter {
            Pgen_req = Pgmax;
            Pbat_discharge = PL - Ppv - Pw - Pgmax;
            Pbat_charge = 0;
            Pspare = 0;
            cmd_generation_cut = 1;
            cmd_load_cut = 0;
            cmd_LNG_cut_in = 1;
            cmd_LNG_cut_out = 0;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state LNGDG1 {
        enter {
            Pgen_req = PL - Ppv - Pw;
            Pbat_discharge = 0;
            Pbat_charge = 0;
            Pspare = 0;
            cmd_generation_cut = 1;
            cmd_load_cut = 0;
            cmd_LNG_cut_in = 1;
            cmd_LNG_cut_out = 0;
            cmd_DG1_cut_in = 1;
            cmd_DG1_cut_out = 0;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state LNGDG1DG2 {
        enter {
            Pgen_req = PL - Ppv - Pw;
            Pbat_discharge = 0;
            Pbat_charge = 0;
            Pspare = 0;
            cmd_generation_cut = 1;
            cmd_load_cut = 0;
            cmd_LNG_cut_in = 1;
            cmd_LNG_cut_out = 0;
            cmd_DG1_cut_in = 1;
            cmd_DG1_cut_out = 0;
            cmd_DG2_cut_in = 1;
            cmd_DG2_cut_out = 0;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state LowSoCLNGChargeMargin {
        enter {
            Pgen_req = PL - Ppv - Pw + Pgmax / 5;
            Pbat_discharge = 0;
            Pbat_charge = Pgmax / 5;
            Pspare = 0;
            cmd_generation_cut = 1;
            cmd_load_cut = 0;
            cmd_LNG_cut_in = 1;
            cmd_LNG_cut_out = 0;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state LowSoCDGChargeMargin {
        enter {
            Pgen_req = PL - Ppv - Pw + Pd1max / 10;
            Pbat_discharge = 0;
            Pbat_charge = Pd1max / 10;
            Pspare = 0;
            cmd_generation_cut = 1;
            cmd_load_cut = 0;
            cmd_LNG_cut_in = 1;
            cmd_LNG_cut_out = 0;
            cmd_DG1_cut_in = 1;
            cmd_DG1_cut_out = 0;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state AllThermalBatteryLack {
        enter {
            Pgen_req = Pgmax + Pd1max + eng3_Pmax;
            Pbat_discharge = PL - Ppv - Pw - Pgmax - Pd1max - eng3_Pmax;
            Pbat_charge = 0;
            Pspare = 0;
            cmd_generation_cut = 1;
            cmd_load_cut = 0;
            cmd_LNG_cut_in = 1;
            cmd_LNG_cut_out = 0;
            cmd_DG1_cut_in = 1;
            cmd_DG1_cut_out = 0;
            cmd_DG2_cut_in = 1;
            cmd_DG2_cut_out = 0;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }
}
```

#### Candidate diff（before -> candidate）

- before 与 candidate 文本完全一致；无 diff。

#### SL-10 审查结果

- SL-10 decision=`pass`，ok=`True`，target_resolved=`True`，regression_detected=`False`，drift_risk=`minor`。
- SL-10 review_meta：schema=`SL10RepairReviewOutput.v1`，failure_policy=`fail_closed`，replay_key=`SL-10:sha256:43ac823192e60bcc9a7db439c54a115bf9d352ed67606f51fb0689f376bd0c89`。
  - SL-10 evidence 1: `{"summary": "The NL defines this EMS as a guard-driven dispatch classifier that reads PL, Ppv, Pw, SoC, and capacity bounds such as eng3_Pmax and selects twelve states by logical conditions over demand, generation, capacity, and SoC. The SL-9 decisions correctly preserve Pbatmax, Pgmax, Pd1max, eng3_Pmax, PL, Ppv, Pw, and SoC as external inputs rather than adding ungrounded writes or self-assignments."}`
  - SL-10 evidence 2: `{"summary": "The candidate DSL is unchanged from the previously SL-10-accepted hash sha256:942ea1f43a9376d06509746a7e409cc8c830ac52275db43c84b69211068dfa22. It preserves all twelve NL-required states and their dispatch actions: zero-load charge/spare, RES-covers charge/spare, RESBatteryDischarge, LNGOnly, LNGBatteryAssist, LNGDG1, LNGDG1DG2, LowSoCLNGChargeMargin, LowSoCDGChargeMargin, and AllThermalBatteryLack."}`
  - SL-10 evidence 3: `{"summary": "The DSL preserves the required low-SoC charging margins: LowSoCLNGChargeMargin uses Pbat_charge = Pgmax / 5 and LowSoCDGChargeMargin uses Pbat_charge = Pd1max / 10. It also preserves the extreme overload behavior by activating LNG, DG1, and DG2 and covering the remaining lack with Pbat_discharge in AllThermalBatteryLack."}`
  - SL-10 evidence 4: `{"summary": "The DSL preserves command obligations at both aggregate and concrete levels: cmd_generation_cut and cmd_load_cut are declared and assigned in every state, and concrete cut-in/cut-out variables exist for LNG, DG1, DG2, and load commands. Thus the current local missing_required_grounding report for cmd_generation_cut and cmd_load_cut is contradicted by direct DSL declarations and assignments."}`
  - SL-10 evidence 5: `{"summary": "The FixLog shows the prior rework objection was resolved in iteration 0 by adding aggregate command variables and by providing explicit SL-10 override rationale for remaining local matcher objections. The current batch repeats the same non-hard design-warning family and the current DSL is the already accepted frontier; repair_memory marks the earlier local objection as overridden by SL-10 and audit-only unless new hard evidence or a real regression appears."}`
  - SL-10 evidence 6: `{"summary": "Local deterministic evidence still reports missing_required_grounding with major drift, but it reports no scenario_regression and no DSL behavioral regression. Given the NL, FixLog, SL-9 decisions, and the DSL itself, the remaining local rejection is a grounding-name/matcher limitation for abstract transition ids rather than a dropped state, guard, action, variable, or scenario obligation."}`
- local checks evidence：stage=`SD-10`；note=PR-E1 uses local parse/semantic/design/sim checks as SL-10 evidence, not as the final deterministic judge.。
  - local ok=`False`，target_resolved=`False`，regression_detected=`False`，drift_risk=`major`。
  - local_rejection：reason=`missing_required_grounding`，rejected_by_stage=`SD-10`。
    - local evidence 1: `missing_required_grounding` {"element_ids": ["variable:cmd_generation_cut", "variable:cmd_load_cut", "transition:select_deficit_priority", "transition:select_low_soc_margins"], "kind": "missing_required_grounding"}

</details>

<details><summary>Repair 4 / iteration `2` / source `SL-7` / accepted=✅</summary>

#### 为什么进入修复

- selected feedback source：`SL-7`；blocking=`True`；pre_scenario=`False`。
- problem_summary：model review failed
- diagnostic ids：`0, 1`。
- before_dsl_hash：`sha256:942ea1f43a9376d06509746a7e409cc8c830ac52275db43c84b69211068dfa22`；candidate_dsl_hash：`sha256:022a18b5cb4d9bbc9bd9f5dbcb9d53df8e63bd2d505d481bcff8d876d1a5a99c`。

#### 错误证据 / diagnostics

- 1. `<unknown>` `` policy=``：The illegal overload completion state is modeled as a normal reachable dispatch state rather than as an explicitly marked exceptional/diagnostic/fail-safe condition.
- 2. `<unknown>` `` policy=``：The overload branch may command unbounded battery discharge for residual lack while not cutting load, making the recovery semantics unsafe.

#### SD-8 FixRequestBatch / 修改请求

- batch_id：`fixbatch-2-sha256-d21d7baa580`；source_stage=`SL-7`；legacy_plan_kind=`FixPlan`；requests=`2`。

| request_id | severity | hard | waiver | problem | evidence |
|---|---|---:|---:|---|---|
| `fixreq-2-sl7-0-e56a9044a1` | `review_fail` | ✅ | ❌ | model review failed | `{'category': 'nl_fidelity', 'evidence': ['NL: "The overload completion state is illegal" and "the state shall never occur in practice."', 'DSL: `! * -> AllThermalBatteryLack` makes the state normally reachable under an extreme-demand guard.', 'DSL `AllThermalBatteryLack` has no diagnostic/illegal marker and keeps load service active.'], 'severity': 'major', 'summary': 'The illegal overload completion state is modeled as a normal reachable dispatch state rather than as an explicitly marked exceptional/diagnostic/fail-safe condition.'}` |
| `fixreq-2-sl7-1-ef61a52a60` | `review_fail` | ✅ | ❌ | model review failed | `{'category': 'unsafe_recovery', 'evidence': ['DSL action: `Pbat_discharge = PL - Ppv - Pw - Pgmax - Pd1max - eng3_Pmax`.', 'No guard limits that discharge by `Pbatmax` or SoC.', 'DSL sets `cmd_load_cut = 0`, `cmd_load_cut_in = 1`, and `cmd_load_cut_out = 0` in `AllThermalBatteryLack`.'], 'severity': 'major', 'summary': 'The overload branch may command unbounded battery discharge for residual lack while not cutting load, making the recovery semantics unsafe.'}` |

#### SD-8 legacy fix plan / 修改建议

- recommended_strategy：Use diagnostics as hints; choose the smallest globally consistent repair.；Before returning a candidate, verify every required_preserve_element_id still has a concrete DSL representation.
- forbidden_edits：`Do not delete grounded required elements merely to silence diagnostics., Do not invent internal plant/environment dynamics merely to make external input variables appear written.`。
- required_preserve_element_ids：`state:ZeroLoadCharge, state:ZeroLoadSpare, state:RESCoversCharge, state:RESCoversSpare, state:RESBatteryDischarge, state:LNGOnly, state:LNGBatteryAssist, state:LNGDG1, state:LNGDG1DG2, state:LowSoCLNGChargeMargin, state:LowSoCDGChargeMargin, state:AllThermalBatteryLack, ... +17`。

#### SL-9 per-request 决策

- accepted_request_ids：`<derived-from-table>`；candidate_len=`8575`。

| request_id | decision | waiver | rework_locked | rationale / intent |
|---|---|---:|---:|---|
| `fixreq-2-sl7-0-e56a9044a1` | `accept` | ❌ | ❌ | The NL says the overload completion state is illegal and shall never occur in practice, but the current DSL treated AllThermalBatteryLack as an ordinary load-serving dispatch state. The repair preserves the required state and selection transition while explicitly marking entry to that state with a diagnostic illegal-overload flag and using fail-safe load cut...<truncated 283 chars> |
| `fixreq-2-sl7-1-ef61a52a60` | `accept` | ❌ | ❌ | The overload branch commanded the full residual lack as battery discharge with no capacity or SoC limit while keeping load served. The repair keeps all thermal units active, but bounds battery discharge by Pbatmax and SoC using NL-grounded battery-capacity and SoC inputs, and commands load cut in the exceptional overload branch to avoid unsafe recovery seman...<truncated 174 chars> |
- repair_rationale：Accepted both new SL-7 model-review requests because they provide new hard NL-fidelity and unsafe-recovery evidence about AllThermalBatteryLack, distinct from the previously waived local matcher warnings.；Preserved all twelve required dispatch states and all required guard-driven selection structure, including transition:select_all_thermal_battery_lack as the forced guard to AllThermalBatteryLack.；Added `illegal_overload_state` as a concrete diagnostic marker for the NL statement that the overload completion state is illegal and shall never occur in practice.；Changed only the exceptional overload state's recovery actions: all thermal generators remain active, battery discharge is bounded by SoC and Pbatmax, and load cut is commanded as fail-safe behavior instead of normal load service.；Preserved the prior SL-10-accepted command grounding: `cmd_generation_cut` and `cmd_load_cut` remain declared and assigned, and the concrete LNG/DG/load cut-in/cut-out commands are preserved.
- diff_summary：`{"summary": "Added diagnostic variable `illegal_overload_state`; marked `AllThermalBatteryLack` on entry and cleared it on exit; bounded overload `Pbat_discharge` by `Pbatmax` and SoC; changed overload load commands to fail-safe load cut while preserving all twelve states, all selection guards, and normal dispatch branches."}`。

#### SL-9 candidate / 最终修改执行方案

```pyfcstm
def float PL = 0.0;
def float Ppv = 0.0;
def float Pw = 0.0;
def float SoC = 0.0;
def float Pgmax = 0.0;
def float Pd1max = 0.0;
def float eng3_Pmax = 0.0;
def float Pbatmax = 0.0;
def float Pgen_req = 0.0;
def float Pbat_discharge = 0.0;
def float Pbat_charge = 0.0;
def float Pspare = 0.0;
def int cmd_generation_cut = 0;
def int cmd_load_cut = 0;
def int cmd_LNG_cut_in = 0;
def int cmd_LNG_cut_out = 0;
def int cmd_DG1_cut_in = 0;
def int cmd_DG1_cut_out = 0;
def int cmd_DG2_cut_in = 0;
def int cmd_DG2_cut_out = 0;
def int cmd_load_cut_in = 0;
def int cmd_load_cut_out = 0;
def int illegal_overload_state = 0;

state LNGShipEMS {
    ! * -> ZeroLoadCharge : if [PL == 0 && Ppv + Pw > 0 && SoC < 0.95];
    ! * -> ZeroLoadSpare : if [PL == 0 && (Ppv + Pw <= 0 || SoC >= 0.95)];
    ! * -> RESCoversCharge : if [PL > 0 && Ppv + Pw >= PL && SoC < 0.95];
    ! * -> RESCoversSpare : if [PL > 0 && Ppv + Pw >= PL && SoC >= 0.95];
    ! * -> RESBatteryDischarge : if [PL > 0 && Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw <= Pbatmax];
    ! * -> LNGOnly : if [PL > 0 && Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw > Pbatmax && PL - Ppv - Pw <= Pgmax];
    ! * -> LNGBatteryAssist : if [PL > 0 && Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw > Pgmax && PL - Ppv - Pw <= Pgmax + Pbatmax];
    ! * -> LNGDG1 : if [PL > 0 && Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw > Pgmax + Pbatmax && PL - Ppv - Pw <= Pgmax + Pd1max];
    ! * -> LNGDG1DG2 : if [PL > 0 && Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw > Pgmax + Pd1max && PL - Ppv - Pw <= Pgmax + Pd1max + eng3_Pmax];
    ! * -> LowSoCLNGChargeMargin : if [PL > 0 && Ppv + Pw < PL && SoC < 0.2 && PL - Ppv - Pw + Pgmax / 5 <= Pgmax];
    ! * -> LowSoCDGChargeMargin : if [PL > 0 && Ppv + Pw < PL && SoC < 0.2 && PL - Ppv - Pw + Pgmax / 5 > Pgmax && PL - Ppv - Pw + Pd1max / 10 <= Pgmax + Pd1max];
    ! * -> AllThermalBatteryLack : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > Pgmax + Pd1max + eng3_Pmax];

    [*] -> ZeroLoadCharge;

    state ZeroLoadCharge {
        enter {
            Pgen_req = 0;
            Pbat_discharge = 0;
            Pbat_charge = Ppv + Pw;
            Pspare = 0;
            cmd_generation_cut = 0;
            cmd_load_cut = 1;
            cmd_LNG_cut_in = 0;
            cmd_LNG_cut_out = 1;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 0;
            cmd_load_cut_out = 1;
        }
    }

    state ZeroLoadSpare {
        enter {
            Pgen_req = 0;
            Pbat_discharge = 0;
            Pbat_charge = 0;
            Pspare = Ppv + Pw;
            cmd_generation_cut = 0;
            cmd_load_cut = 1;
            cmd_LNG_cut_in = 0;
            cmd_LNG_cut_out = 1;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 0;
            cmd_load_cut_out = 1;
        }
    }

    state RESCoversCharge {
        enter {
            Pgen_req = 0;
            Pbat_discharge = 0;
            Pbat_charge = Ppv + Pw - PL;
            Pspare = 0;
            cmd_generation_cut = 0;
            cmd_load_cut = 0;
            cmd_LNG_cut_in = 0;
            cmd_LNG_cut_out = 1;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state RESCoversSpare {
        enter {
            Pgen_req = 0;
            Pbat_discharge = 0;
            Pbat_charge = 0;
            Pspare = Ppv + Pw - PL;
            cmd_generation_cut = 0;
            cmd_load_cut = 0;
            cmd_LNG_cut_in = 0;
            cmd_LNG_cut_out = 1;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state RESBatteryDischarge {
        enter {
            Pgen_req = 0;
            Pbat_discharge = PL - Ppv - Pw;
            Pbat_charge = 0;
            Pspare = 0;
            cmd_generation_cut = 0;
            cmd_load_cut = 0;
            cmd_LNG_cut_in = 0;
            cmd_LNG_cut_out = 1;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state LNGOnly {
        enter {
            Pgen_req = PL - Ppv - Pw;
            Pbat_discharge = 0;
            Pbat_charge = 0;
            Pspare = 0;
            cmd_generation_cut = 1;
            cmd_load_cut = 0;
            cmd_LNG_cut_in = 1;
            cmd_LNG_cut_out = 0;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state LNGBatteryAssist {
        enter {
            Pgen_req = Pgmax;
            Pbat_discharge = PL - Ppv - Pw - Pgmax;
            Pbat_charge = 0;
            Pspare = 0;
            cmd_generation_cut = 1;
            cmd_load_cut = 0;
            cmd_LNG_cut_in = 1;
            cmd_LNG_cut_out = 0;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state LNGDG1 {
        enter {
            Pgen_req = PL - Ppv - Pw;
            Pbat_discharge = 0;
            Pbat_charge = 0;
            Pspare = 0;
            cmd_generation_cut = 1;
            cmd_load_cut = 0;
            cmd_LNG_cut_in = 1;
            cmd_LNG_cut_out = 0;
            cmd_DG1_cut_in = 1;
            cmd_DG1_cut_out = 0;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state LNGDG1DG2 {
        enter {
            Pgen_req = PL - Ppv - Pw;
            Pbat_discharge = 0;
            Pbat_charge = 0;
            Pspare = 0;
            cmd_generation_cut = 1;
            cmd_load_cut = 0;
            cmd_LNG_cut_in = 1;
            cmd_LNG_cut_out = 0;
            cmd_DG1_cut_in = 1;
            cmd_DG1_cut_out = 0;
            cmd_DG2_cut_in = 1;
            cmd_DG2_cut_out = 0;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state LowSoCLNGChargeMargin {
        enter {
            Pgen_req = PL - Ppv - Pw + Pgmax / 5;
            Pbat_discharge = 0;
            Pbat_charge = Pgmax / 5;
            Pspare = 0;
            cmd_generation_cut = 1;
            cmd_load_cut = 0;
            cmd_LNG_cut_in = 1;
            cmd_LNG_cut_out = 0;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state LowSoCDGChargeMargin {
        enter {
            Pgen_req = PL - Ppv - Pw + Pd1max / 10;
            Pbat_discharge = 0;
            Pbat_charge = Pd1max / 10;
            Pspare = 0;
            cmd_generation_cut = 1;
            cmd_load_cut = 0;
            cmd_LNG_cut_in = 1;
            cmd_LNG_cut_out = 0;
            cmd_DG1_cut_in = 1;
            cmd_DG1_cut_out = 0;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state AllThermalBatteryLack {
        enter {
            illegal_overload_state = 1;
            Pgen_req = Pgmax + Pd1max + eng3_Pmax;
            if [SoC >= 0.2 && PL - Ppv - Pw - Pgmax - Pd1max - eng3_Pmax <= Pbatmax] {
                Pbat_discharge = PL - Ppv - Pw - Pgmax - Pd1max - eng3_Pmax;
            } else if [SoC >= 0.2] {
                Pbat_discharge = Pbatmax;
            } else {
                Pbat_discharge = 0;
            }
            Pbat_charge = 0;
            Pspare = 0;
            cmd_generation_cut = 1;
            cmd_load_cut = 1;
            cmd_LNG_cut_in = 1;
            cmd_LNG_cut_out = 0;
            cmd_DG1_cut_in = 1;
            cmd_DG1_cut_out = 0;
            cmd_DG2_cut_in = 1;
            cmd_DG2_cut_out = 0;
            cmd_load_cut_in = 0;
            cmd_load_cut_out = 1;
        }
        exit {
            illegal_overload_state = 0;
        }
    }
}
```

#### Candidate diff（before -> candidate）

```diff
--- before.fcstm
+++ candidate.fcstm
@@ -20,6 +20,7 @@
 def int cmd_DG2_cut_out = 0;
 def int cmd_load_cut_in = 0;
 def int cmd_load_cut_out = 0;
+def int illegal_overload_state = 0;
 
 state LNGShipEMS {
     ! * -> ZeroLoadCharge : if [PL == 0 && Ppv + Pw > 0 && SoC < 0.95];
@@ -248,20 +249,30 @@
 
     state AllThermalBatteryLack {
         enter {
+            illegal_overload_state = 1;
             Pgen_req = Pgmax + Pd1max + eng3_Pmax;
-            Pbat_discharge = PL - Ppv - Pw - Pgmax - Pd1max - eng3_Pmax;
-            Pbat_charge = 0;
-            Pspare = 0;
-            cmd_generation_cut = 1;
-            cmd_load_cut = 0;
+            if [SoC >= 0.2 && PL - Ppv - Pw - Pgmax - Pd1max - eng3_Pmax <= Pbatmax] {
+                Pbat_discharge = PL - Ppv - Pw - Pgmax - Pd1max - eng3_Pmax;
+            } else if [SoC >= 0.2] {
+                Pbat_discharge = Pbatmax;
+            } else {
+                Pbat_discharge = 0;
+            }
+            Pbat_charge = 0;
+            Pspare = 0;
+            cmd_generation_cut = 1;
+            cmd_load_cut = 1;
             cmd_LNG_cut_in = 1;
             cmd_LNG_cut_out = 0;
             cmd_DG1_cut_in = 1;
             cmd_DG1_cut_out = 0;
             cmd_DG2_cut_in = 1;
             cmd_DG2_cut_out = 0;
-            cmd_load_cut_in = 1;
-            cmd_load_cut_out = 0;
+            cmd_load_cut_in = 0;
+            cmd_load_cut_out = 1;
+        }
+        exit {
+            illegal_overload_state = 0;
         }
     }
 }
```

#### SL-10 审查结果

- SL-10 decision=`pass`，ok=`True`，target_resolved=`True`，regression_detected=`False`，drift_risk=`minor`。
- SL-10 review_meta：schema=`SL10RepairReviewOutput.v1`，failure_policy=`fail_closed`，replay_key=`SL-10:sha256:1806365278f2025e72a2446ed5a7898a81a01f631836ac3eb40408c978ffea00`。
  - SL-10 evidence 1: `{"summary": "The current SL-7 hard requests target two new overload defects: AllThermalBatteryLack was previously modeled as an ordinary reachable load-serving dispatch state, and its battery discharge was unbounded while load service remained commanded. The candidate directly addresses both: it adds `illegal_overload_state`, sets it on entry to AllThermalBatteryLack and clears it on exit, preserves all thermal generation activation, bounds overload `Pbat_discharge` by `Pbatmax` and SoC, and changes the exceptional overload branch to load-cut fail-safe commands."}`
  - SL-10 evidence 2: `{"summary": "The repair is narrow and NL-grounded. The DSL diff only adds the diagnostic illegal-overload marker and modifies AllThermalBatteryLack entry/exit behavior. It preserves all twelve NL-required states, all guard-driven selection transitions, normal dispatch power formulas, low-SoC charging margins `Pgmax / 5` and `Pd1max / 10`, aggregate command variables, and concrete LNG/DG/load cut-in/cut-out command coverage."}`
  - SL-10 evidence 3: `{"summary": "The NL states that the overload completion state is illegal and shall never occur in practice, while still describing the fail-safe physical response as all thermal units active with battery lack coverage. The candidate now treats this branch as exceptional/diagnostic instead of normal load service, which resolves the NL-fidelity objection without deleting the required AllThermalBatteryLack state or its selection guard."}`
  - SL-10 evidence 4: `{"summary": "The complete FixLog shows that prior local deterministic objections for `cmd_generation_cut`, `cmd_load_cut`, `select_deficit_priority`, and `select_low_soc_margins` were already audited and overridden by SL-10 after aggregate command variables were added and abstract transition requirements were mapped to concrete guarded selections. The current candidate is based on that accepted frontier and does not regress those representations."}`
  - SL-10 evidence 5: `{"summary": "Local deterministic evidence still reports `missing_required_grounding` with major drift and no scenario regression. The reported missing variables are visibly present in the candidate DSL as `def int cmd_generation_cut = 0;` and `def int cmd_load_cut = 0;` with state-entry assignments. The reported transition ids are abstract grounding ids represented by concrete forced guards to the deficit-priority and low-SoC margin states rather than literal transition labels."}`
  - SL-10 evidence 6: `{"candidate_dsl_hash": "sha256:022a18b5cb4d9bbc9bd9f5dbcb9d53df8e63bd2d505d481bcff8d876d1a5a99c", "covered_local_objection_kinds": ["missing_required_grounding"], "kind": "local_major_drift_override_audit", "local_check_evidence_hash": "sha256:0b04c4bd77aa912e9cbe68ebf7a67afb4d74dc4c67cf27671e8cba88b74e4b2a", "local_override_rationale_count": 5, "local_override_rationale_hash": "sha256:623da8590f0bc6e13c6653c8f3bbff850b25fd6fd83bc5a415aeba7a419c33d1", "local_rejection_evidence_hash": "sha256:b87991e3f44b38a0983a9046c9013e43ed0adc4c41e61c01dba9b25b9d4b84c6", "local_rejection_reason": "missing_required_grounding", "missing_local_objection_kinds": [], "policy": "SL-10 may override conservative ...<truncated 296 chars>`
- local checks evidence：stage=`SD-10`；note=PR-E1 uses local parse/semantic/design/sim checks as SL-10 evidence, not as the final deterministic judge.。
  - local ok=`False`，target_resolved=`False`，regression_detected=`False`，drift_risk=`major`。
  - local_rejection：reason=`missing_required_grounding`，rejected_by_stage=`SD-10`。
    - local evidence 1: `missing_required_grounding` {"element_ids": ["variable:cmd_generation_cut", "variable:cmd_load_cut", "transition:select_deficit_priority", "transition:select_low_soc_margins"], "kind": "missing_required_grounding"}

</details>

<details><summary>Repair 5 / iteration `3` / source `SL-7` / accepted=✅</summary>

#### 为什么进入修复

- selected feedback source：`SL-7`；blocking=`True`；pre_scenario=`False`。
- problem_summary：model review failed
- diagnostic ids：`0`。
- before_dsl_hash：`sha256:022a18b5cb4d9bbc9bd9f5dbcb9d53df8e63bd2d505d481bcff8d876d1a5a99c`；candidate_dsl_hash：`sha256:fea8ed50cc9bf814763d6cfb0bfa81ebc61727c81131b056e604e37f0532444a`。

#### 错误证据 / diagnostics

- 1. `<unknown>` `` policy=``：The DSL fails NL fidelity because low-SoC high-deficit conditions that should follow thermal dispatch priority can be left without a selected state, violating the requirement to dynamically switch states over demand, generation, capacity, and SoC to maintain power balance.

#### SD-8 FixRequestBatch / 修改请求

- batch_id：`fixbatch-3-sha256-5bb8c5e25f4`；source_stage=`SL-7`；legacy_plan_kind=`FixPlan`；requests=`1`。

| request_id | severity | hard | waiver | problem | evidence |
|---|---|---:|---:|---|---|
| `fixreq-3-sl7-0-65d2e7f559` | `review_fail` | ✅ | ❌ | model review failed | `{'category': 'nl_fidelity', 'evidence': ['NL requires state selection by logical conditions over demand, generation, capacity, and SoC and dispatch priority through LNG and DG1/DG2 when RES is below load.', 'DSL `LNGDG1DG2` requires `SoC >= 0.2`, excluding low-SoC cases.', 'DSL low-SoC guards stop at `Pgmax + Pd1max` capacity with charging margins and do not include an `eng3_Pmax`/DG2 low-SoC branch.', 'DSL overload guard only triggers when deficit is greater than `Pgmax + Pd1max + eng3_Pmax`, leaving low-SoC deficits between the low-DG margin bound and all-thermal overload unhandled.'], 'severity': 'major', 'summary': 'The DSL fails NL fidelity because low-SoC high-deficit conditions that should follow thermal dispatch priority can be left without a selected state, violating the requirement to dynamically switch states over demand, generation, capacity, and SoC to maintain power balance.'}` |

#### SD-8 legacy fix plan / 修改建议

- recommended_strategy：Use diagnostics as hints; choose the smallest globally consistent repair.；Before returning a candidate, verify every required_preserve_element_id still has a concrete DSL representation.
- forbidden_edits：`Do not delete grounded required elements merely to silence diagnostics., Do not invent internal plant/environment dynamics merely to make external input variables appear written.`。
- required_preserve_element_ids：`state:ZeroLoadCharge, state:ZeroLoadSpare, state:RESCoversCharge, state:RESCoversSpare, state:RESBatteryDischarge, state:LNGOnly, state:LNGBatteryAssist, state:LNGDG1, state:LNGDG1DG2, state:LowSoCLNGChargeMargin, state:LowSoCDGChargeMargin, state:AllThermalBatteryLack, ... +17`。

#### SL-9 per-request 决策

- accepted_request_ids：`<derived-from-table>`；candidate_len=`8893`。

| request_id | decision | waiver | rework_locked | rationale / intent |
|---|---|---:|---:|---|
| `fixreq-3-sl7-0-65d2e7f559` | `accept` | ❌ | ❌ | The request provides new hard NL-fidelity evidence: low-SoC high-deficit cases below the all-thermal overload bound can currently miss every forced selection guard. I accepted it and made the smallest dispatch-coverage edit by extending the low-SoC diesel margin branch through the DG2/eng3 capacity range, and by allowing LNGDG1DG2 to cover the remaining low-...<truncated 463 chars> |
- repair_rationale：Accepted the new SL-7 model-review request because it identifies a real guard-coverage gap, not a previously waived local matcher warning: for SoC < 0.2 and deficit above the former LowSoCDGChargeMargin upper bound but not above Pgmax + Pd1...<truncated 44 chars>；Preserved the latest non-regressive behavior and all required grounded elements: all twelve states, external inputs PL/Ppv/Pw/SoC/Pbatmax/Pgmax/Pd1max/eng3_Pmax, aggregate command variables, low-SoC margin states, and the exceptional AllThe...<truncated 37 chars>；The low-SoC gap is closed in two minimal edits: LowSoCDGChargeMargin now extends its Pd1max/10 charging-margin logic through the DG2/eng3 capacity range when the margin fits; LNGDG1DG2 now covers low-SoC high-deficit cases up to all thermal...<truncated 69 chars>；LowSoCDGChargeMargin now conditionally cuts in DG2 when the low-SoC diesel-margin dispatch needs eng3_Pmax capacity, directly addressing the evidence that there was no eng3/DG2 low-SoC branch.；No writes were added to external demand/resource/capacity inputs. The remembered W_UNWRITTEN_READ_VAR and W_GUARD_VARS_NEVER_CHANGE objections remain audit-only local warnings: the NL describes a guard-driven EMS classifier that reads chang...<truncated 99 chars>
- diff_summary：`{"summary": "Extended low-SoC high-deficit dispatch coverage without adding or deleting states: LowSoCDGChargeMargin guard now allows Pd1max/10 charging margin through Pgmax + Pd1max + eng3_Pmax and conditionally commands DG2 cut-in; LNGDG1DG2 guard now also covers low-SoC all-thermal-capable deficits when the Pd1max/10 charge margin cannot fit. All prior overload diagnostics, command variables, and required twelve-state structure are preserved."}`。

#### SL-9 candidate / 最终修改执行方案

```pyfcstm
def float PL = 0.0;
def float Ppv = 0.0;
def float Pw = 0.0;
def float SoC = 0.0;
def float Pgmax = 0.0;
def float Pd1max = 0.0;
def float eng3_Pmax = 0.0;
def float Pbatmax = 0.0;
def float Pgen_req = 0.0;
def float Pbat_discharge = 0.0;
def float Pbat_charge = 0.0;
def float Pspare = 0.0;
def int cmd_generation_cut = 0;
def int cmd_load_cut = 0;
def int cmd_LNG_cut_in = 0;
def int cmd_LNG_cut_out = 0;
def int cmd_DG1_cut_in = 0;
def int cmd_DG1_cut_out = 0;
def int cmd_DG2_cut_in = 0;
def int cmd_DG2_cut_out = 0;
def int cmd_load_cut_in = 0;
def int cmd_load_cut_out = 0;
def int illegal_overload_state = 0;

state LNGShipEMS {
    ! * -> ZeroLoadCharge : if [PL == 0 && Ppv + Pw > 0 && SoC < 0.95];
    ! * -> ZeroLoadSpare : if [PL == 0 && (Ppv + Pw <= 0 || SoC >= 0.95)];
    ! * -> RESCoversCharge : if [PL > 0 && Ppv + Pw >= PL && SoC < 0.95];
    ! * -> RESCoversSpare : if [PL > 0 && Ppv + Pw >= PL && SoC >= 0.95];
    ! * -> RESBatteryDischarge : if [PL > 0 && Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw <= Pbatmax];
    ! * -> LNGOnly : if [PL > 0 && Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw > Pbatmax && PL - Ppv - Pw <= Pgmax];
    ! * -> LNGBatteryAssist : if [PL > 0 && Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw > Pgmax && PL - Ppv - Pw <= Pgmax + Pbatmax];
    ! * -> LNGDG1 : if [PL > 0 && Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw > Pgmax + Pbatmax && PL - Ppv - Pw <= Pgmax + Pd1max];
    ! * -> LNGDG1DG2 : if [PL > 0 && Ppv + Pw < PL && ((SoC >= 0.2 && PL - Ppv - Pw > Pgmax + Pd1max && PL - Ppv - Pw <= Pgmax + Pd1max + eng3_Pmax) || (SoC < 0.2 && PL - Ppv - Pw + Pd1max / 10 > Pgmax + Pd1max + eng3_Pmax && PL - Ppv - Pw <= Pgmax + Pd1max + eng3_Pmax))];
    ! * -> LowSoCLNGChargeMargin : if [PL > 0 && Ppv + Pw < PL && SoC < 0.2 && PL - Ppv - Pw + Pgmax / 5 <= Pgmax];
    ! * -> LowSoCDGChargeMargin : if [PL > 0 && Ppv + Pw < PL && SoC < 0.2 && PL - Ppv - Pw + Pgmax / 5 > Pgmax && PL - Ppv - Pw + Pd1max / 10 <= Pgmax + Pd1max + eng3_Pmax];
    ! * -> AllThermalBatteryLack : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > Pgmax + Pd1max + eng3_Pmax];

    [*] -> ZeroLoadCharge;

    state ZeroLoadCharge {
        enter {
            Pgen_req = 0;
            Pbat_discharge = 0;
            Pbat_charge = Ppv + Pw;
            Pspare = 0;
            cmd_generation_cut = 0;
            cmd_load_cut = 1;
            cmd_LNG_cut_in = 0;
            cmd_LNG_cut_out = 1;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 0;
            cmd_load_cut_out = 1;
        }
    }

    state ZeroLoadSpare {
        enter {
            Pgen_req = 0;
            Pbat_discharge = 0;
            Pbat_charge = 0;
            Pspare = Ppv + Pw;
            cmd_generation_cut = 0;
            cmd_load_cut = 1;
            cmd_LNG_cut_in = 0;
            cmd_LNG_cut_out = 1;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 0;
            cmd_load_cut_out = 1;
        }
    }

    state RESCoversCharge {
        enter {
            Pgen_req = 0;
            Pbat_discharge = 0;
            Pbat_charge = Ppv + Pw - PL;
            Pspare = 0;
            cmd_generation_cut = 0;
            cmd_load_cut = 0;
            cmd_LNG_cut_in = 0;
            cmd_LNG_cut_out = 1;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state RESCoversSpare {
        enter {
            Pgen_req = 0;
            Pbat_discharge = 0;
            Pbat_charge = 0;
            Pspare = Ppv + Pw - PL;
            cmd_generation_cut = 0;
            cmd_load_cut = 0;
            cmd_LNG_cut_in = 0;
            cmd_LNG_cut_out = 1;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state RESBatteryDischarge {
        enter {
            Pgen_req = 0;
            Pbat_discharge = PL - Ppv - Pw;
            Pbat_charge = 0;
            Pspare = 0;
            cmd_generation_cut = 0;
            cmd_load_cut = 0;
            cmd_LNG_cut_in = 0;
            cmd_LNG_cut_out = 1;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state LNGOnly {
        enter {
            Pgen_req = PL - Ppv - Pw;
            Pbat_discharge = 0;
            Pbat_charge = 0;
            Pspare = 0;
            cmd_generation_cut = 1;
            cmd_load_cut = 0;
            cmd_LNG_cut_in = 1;
            cmd_LNG_cut_out = 0;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state LNGBatteryAssist {
        enter {
            Pgen_req = Pgmax;
            Pbat_discharge = PL - Ppv - Pw - Pgmax;
            Pbat_charge = 0;
            Pspare = 0;
            cmd_generation_cut = 1;
            cmd_load_cut = 0;
            cmd_LNG_cut_in = 1;
            cmd_LNG_cut_out = 0;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state LNGDG1 {
        enter {
            Pgen_req = PL - Ppv - Pw;
            Pbat_discharge = 0;
            Pbat_charge = 0;
            Pspare = 0;
            cmd_generation_cut = 1;
            cmd_load_cut = 0;
            cmd_LNG_cut_in = 1;
            cmd_LNG_cut_out = 0;
            cmd_DG1_cut_in = 1;
            cmd_DG1_cut_out = 0;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state LNGDG1DG2 {
        enter {
            Pgen_req = PL - Ppv - Pw;
            Pbat_discharge = 0;
            Pbat_charge = 0;
            Pspare = 0;
            cmd_generation_cut = 1;
            cmd_load_cut = 0;
            cmd_LNG_cut_in = 1;
            cmd_LNG_cut_out = 0;
            cmd_DG1_cut_in = 1;
            cmd_DG1_cut_out = 0;
            cmd_DG2_cut_in = 1;
            cmd_DG2_cut_out = 0;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state LowSoCLNGChargeMargin {
        enter {
            Pgen_req = PL - Ppv - Pw + Pgmax / 5;
            Pbat_discharge = 0;
            Pbat_charge = Pgmax / 5;
            Pspare = 0;
            cmd_generation_cut = 1;
            cmd_load_cut = 0;
            cmd_LNG_cut_in = 1;
            cmd_LNG_cut_out = 0;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state LowSoCDGChargeMargin {
        enter {
            Pgen_req = PL - Ppv - Pw + Pd1max / 10;
            Pbat_discharge = 0;
            Pbat_charge = Pd1max / 10;
            Pspare = 0;
            cmd_generation_cut = 1;
            cmd_load_cut = 0;
            cmd_LNG_cut_in = 1;
            cmd_LNG_cut_out = 0;
            cmd_DG1_cut_in = 1;
            cmd_DG1_cut_out = 0;
            if [PL - Ppv - Pw + Pd1max / 10 > Pgmax + Pd1max] {
                cmd_DG2_cut_in = 1;
                cmd_DG2_cut_out = 0;
            } else {
                cmd_DG2_cut_in = 0;
                cmd_DG2_cut_out = 1;
            }
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state AllThermalBatteryLack {
        enter {
            illegal_overload_state = 1;
            Pgen_req = Pgmax + Pd1max + eng3_Pmax;
            if [SoC >= 0.2 && PL - Ppv - Pw - Pgmax - Pd1max - eng3_Pmax <= Pbatmax] {
                Pbat_discharge = PL - Ppv - Pw - Pgmax - Pd1max - eng3_Pmax;
            } else if [SoC >= 0.2] {
                Pbat_discharge = Pbatmax;
            } else {
                Pbat_discharge = 0;
            }
            Pbat_charge = 0;
            Pspare = 0;
            cmd_generation_cut = 1;
            cmd_load_cut = 1;
            cmd_LNG_cut_in = 1;
            cmd_LNG_cut_out = 0;
            cmd_DG1_cut_in = 1;
            cmd_DG1_cut_out = 0;
            cmd_DG2_cut_in = 1;
            cmd_DG2_cut_out = 0;
            cmd_load_cut_in = 0;
            cmd_load_cut_out = 1;
        }
        exit {
            illegal_overload_state = 0;
        }
    }
}
```

#### Candidate diff（before -> candidate）

```diff
--- before.fcstm
+++ candidate.fcstm
@@ -31,9 +31,9 @@
     ! * -> LNGOnly : if [PL > 0 && Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw > Pbatmax && PL - Ppv - Pw <= Pgmax];
     ! * -> LNGBatteryAssist : if [PL > 0 && Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw > Pgmax && PL - Ppv - Pw <= Pgmax + Pbatmax];
     ! * -> LNGDG1 : if [PL > 0 && Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw > Pgmax + Pbatmax && PL - Ppv - Pw <= Pgmax + Pd1max];
-    ! * -> LNGDG1DG2 : if [PL > 0 && Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw > Pgmax + Pd1max && PL - Ppv - Pw <= Pgmax + Pd1max + eng3_Pmax];
+    ! * -> LNGDG1DG2 : if [PL > 0 && Ppv + Pw < PL && ((SoC >= 0.2 && PL - Ppv - Pw > Pgmax + Pd1max && PL - Ppv - Pw <= Pgmax + Pd1max + eng3_Pmax) || (SoC < 0.2 && PL - Ppv - Pw + Pd1max / 10 > Pgmax + Pd1max + eng3_Pmax && PL - Ppv - Pw <= Pgmax + Pd1max + eng3_Pmax))];
     ! * -> LowSoCLNGChargeMargin : if [PL > 0 && Ppv + Pw < PL && SoC < 0.2 && PL - Ppv - Pw + Pgmax / 5 <= Pgmax];
-    ! * -> LowSoCDGChargeMargin : if [PL > 0 && Ppv + Pw < PL && SoC < 0.2 && PL - Ppv - Pw + Pgmax / 5 > Pgmax && PL - Ppv - Pw + Pd1max / 10 <= Pgmax + Pd1max];
+    ! * -> LowSoCDGChargeMargin : if [PL > 0 && Ppv + Pw < PL && SoC < 0.2 && PL - Ppv - Pw + Pgmax / 5 > Pgmax && PL - Ppv - Pw + Pd1max / 10 <= Pgmax + Pd1max + eng3_Pmax];
     ! * -> AllThermalBatteryLack : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > Pgmax + Pd1max + eng3_Pmax];
 
     [*] -> ZeroLoadCharge;
@@ -240,8 +240,13 @@
             cmd_LNG_cut_out = 0;
             cmd_DG1_cut_in = 1;
             cmd_DG1_cut_out = 0;
-            cmd_DG2_cut_in = 0;
-            cmd_DG2_cut_out = 1;
+            if [PL - Ppv - Pw + Pd1max / 10 > Pgmax + Pd1max] {
+                cmd_DG2_cut_in = 1;
+                cmd_DG2_cut_out = 0;
+            } else {
+                cmd_DG2_cut_in = 0;
+                cmd_DG2_cut_out = 1;
+            }
             cmd_load_cut_in = 1;
             cmd_load_cut_out = 0;
         }
```

#### SL-10 审查结果

- SL-10 decision=`pass`，ok=`True`，target_resolved=`True`，regression_detected=`False`，drift_risk=`minor`。
- SL-10 review_meta：schema=`SL10RepairReviewOutput.v1`，failure_policy=`fail_closed`，replay_key=`SL-10:sha256:638041dedd0d91572af2852d301ba9f0df8be71eb5f77c1d2ba80c1fed12e8b0`。
  - SL-10 evidence 1: `{"summary": "The SL-7 hard request identified a real NL-fidelity gap: for SoC < 0.2 and deficits above the former LowSoCDGChargeMargin upper bound but not above Pgmax + Pd1max + eng3_Pmax, no forced selection guard necessarily applied. The candidate directly addresses that gap by extending LowSoCDGChargeMargin through the DG2/eng3 capacity range when the Pd1max/10 margin fits, and by extending LNGDG1DG2 to cover the remaining low-SoC all-thermal-capable cases where the charging margin cannot fit."}`
  - SL-10 evidence 2: `{"summary": "The candidate preserves the NL-required twelve-state structure: ZeroLoadCharge, ZeroLoadSpare, RESCoversCharge, RESCoversSpare, RESBatteryDischarge, LNGOnly, LNGBatteryAssist, LNGDG1, LNGDG1DG2, LowSoCLNGChargeMargin, LowSoCDGChargeMargin, and AllThermalBatteryLack are all still present."}`
  - SL-10 evidence 3: `{"summary": "The low-SoC dispatch coverage is now continuous for PL > 0, RES below load, and SoC < 0.2: LowSoCLNGChargeMargin covers cases where deficit + Pgmax/5 fits within Pgmax; LowSoCDGChargeMargin covers cases where the LNG margin does not fit but deficit + Pd1max/10 fits within Pgmax + Pd1max + eng3_Pmax; LNGDG1DG2 covers all-thermal-capable cases where the Pd1max/10 charge margin cannot fit; and AllThermalBatteryLack covers deficits above total thermal capacity."}`
  - SL-10 evidence 4: `{"summary": "The candidate preserves the NL-required explicit low-SoC charging margins: LowSoCLNGChargeMargin still uses Pbat_charge = Pgmax / 5, and LowSoCDGChargeMargin still uses Pbat_charge = Pd1max / 10. The LowSoCDGChargeMargin entry action now conditionally cuts in DG2 when the margin case requires capacity beyond Pgmax + Pd1max, which directly addresses the request evidence that no eng3/DG2 low-SoC branch existed."}`
  - SL-10 evidence 5: `{"summary": "The candidate preserves prior accepted overload repairs from the FixLog: AllThermalBatteryLack remains present, marks illegal_overload_state on entry, keeps all thermal units active, bounds battery discharge by SoC and Pbatmax, commands fail-safe load cut in that exceptional branch, and clears the diagnostic flag on exit."}`
  - SL-10 evidence 6: `{"summary": "The candidate preserves command obligations at both aggregate and concrete levels: cmd_generation_cut and cmd_load_cut remain declared and assigned in every state, and concrete LNG, DG1, DG2, and load cut-in/cut-out command variables remain present and assigned."}`
- local checks evidence：stage=`SD-10`；note=PR-E1 uses local parse/semantic/design/sim checks as SL-10 evidence, not as the final deterministic judge.。
  - local ok=`False`，target_resolved=`False`，regression_detected=`False`，drift_risk=`major`。
  - local_rejection：reason=`missing_required_grounding`，rejected_by_stage=`SD-10`。
    - local evidence 1: `missing_required_grounding` {"element_ids": ["variable:cmd_generation_cut", "variable:cmd_load_cut", "transition:select_deficit_priority", "transition:select_low_soc_margins"], "kind": "missing_required_grounding"}

</details>


#### FixLog ledger

口径：FixLog 是跨 iteration 的 append-only repair 台账，记录 request batch、SL-9 accept/reject、diff/local evidence、SL-10 批示和下一步动作。

| # | iteration | phase | batch | decisions | next_action | candidate | notes |
|---:|---:|---|---|---|---|---|---|
| 1 | `0` | `request_batch` | `fixbatch-0-sha256-defea594a84` | accept=0, reject=0 | `sl9_decision_and_repair` | `<none>` | SD-8 produced FixRequestBatch; deterministic stage does not decide final repair. |
| 2 | `0` | `sl9_decision` | `fixbatch-0-sha256-defea594a84` | accept=12, reject=0 | `sl10_review` | `sha256:c8b827039409fe5fe49d7ec4b5b17f7209511b042640bb00aec28e3bd9495720` | No code edit is the smallest safe repair: the selected diagnostics are design warnings caused by external input variables being read in guards but not written by the EMS model., The NL explicitly describes PL, Ppv, Pw, SoC, and capacity bounds such as eng3_Pmax as values the FSM reads. Pbatmax, Pgmax, and Pd1max are capacity/input bounds used to choose dispatch branches; the NL does not provide internal update equations for them., Adding dummy writes, self-assignments, input counters, or fabricated plant dynamics would violate the repair rule for W_UNWRITTEN_READ_VAR and W_GUARD_VARS_NEVER_CHANGE., ... +2 |
| 3 | `0` | `sl10_review` | `fixbatch-0-sha256-defea594a84` | accept=12, reject=0 | `sl9_rework` | `sha256:c8b827039409fe5fe49d7ec4b5b17f7209511b042640bb00aec28e3bd9495720` | SL-10 pass was downgraded because local deterministic evidence reported major drift and SL-10 evidence did not explicitly address the local rejection reason/kind with a structured local_override_rationale., For the next SL-9 repair, do not blindly regenerate the same DSL. Either change the candidate so the local major-drift evidence is resolved, or keep the minimal DSL only with explicit repair_rationale mapping each local objection (for example missing_required_grounding, scenario_regression, count_drift, or forced_transition_count_drift) to concrete NL-grounded states/transitions/actions that remain in the candidate. This rationale is required so SL-10 can produce local_override_rationale instead of cycling., repair_memory:SL-10 pass was downgraded because local deterministic evidence reported major drift and SL-10 evidence did not explicitly address the local rejection reason/kind with a structured local_override_rationale., ... +10 |
| 4 | `0` | `sl9_rework_decision` | `fixbatch-0-sha256-defea594a84` | accept=12, reject=0 | `sl10_review` | `sha256:942ea1f43a9376d06509746a7e409cc8c830ac52275db43c84b69211068dfa22` | Accepted all requests because the selected warnings concern NL-grounded external inputs used by a guard-driven dispatch classifier; rejecting or deleting those guards would violate the NL., Smallest DSL text change: add the required aggregate variables cmd_generation_cut and cmd_load_cut and assign them consistently from the already-grounded concrete cut-in/cut-out command actions., The design_target_unresolved warning for Pbatmax is intentionally not repaired with a write because Pbatmax is an external battery capacity bound. Adding a self-assignment or fabricated capacity dynamics is explicitly forbidden and not NL-grounded., ... +6 |
| 5 | `0` | `sl10_rework_review` | `fixbatch-0-sha256-defea594a84` | accept=12, reject=0 | `sc11_accept_then_sd2` | `sha256:942ea1f43a9376d06509746a7e409cc8c830ac52275db43c84b69211068dfa22` | repair_memory:sl10_evidence, repair_memory:sl10_evidence, repair_memory:sl10_evidence, ... +5 |
| 6 | `1` | `request_batch` | `fixbatch-1-sha256-4686297540a` | accept=0, reject=0 | `sl9_decision_and_repair` | `<none>` | SD-8 produced FixRequestBatch; deterministic stage does not decide final repair. |
| 7 | `1` | `sl9_decision` | `fixbatch-1-sha256-4686297540a` | accept=12, reject=0 | `sl10_review` | `sha256:942ea1f43a9376d06509746a7e409cc8c830ac52275db43c84b69211068dfa22` | Smallest safe edit is conservative preservation of the current DSL. The current candidate is the previously SL-10-accepted candidate hash and already contains the aggregate variables cmd_generation_cut and cmd_load_cut plus assignments in every state, resolving the earlier local missing_required_grounding concern without changing behavior., The new batch repeats W_UNWRITTEN_READ_VAR and W_GUARD_VARS_NEVER_CHANGE on external-input classifier variables. PL, Ppv, Pw, SoC, Pbatmax, Pgmax, Pd1max, and eng3_Pmax are read inputs/capacity bounds per the NL, not EMS-internal state variables. Adding writes would invent plant/environment dynamics and violate the request guidance., Preserved all twelve required dispatch states: zero-load charge/spare, RES-covers charge/spare, RESBatteryDischarge, LNGOnly, LNGBatteryAssist, LNGDG1, LNGDG1DG2, LowSoCLNGChargeMargin, LowSoCDGChargeMargin, and AllThermalBatteryLack., ... +3 |
| 8 | `1` | `sl10_review` | `fixbatch-1-sha256-4686297540a` | accept=12, reject=0 | `sc11_accept_then_sd2` | `sha256:942ea1f43a9376d06509746a7e409cc8c830ac52275db43c84b69211068dfa22` | repair_memory:sl10_evidence, repair_memory:sl10_evidence, repair_memory:sl10_evidence, ... +7 |
| 9 | `2` | `request_batch` | `fixbatch-2-sha256-d21d7baa580` | accept=0, reject=0 | `sl9_decision_and_repair` | `<none>` | SD-8 produced FixRequestBatch; deterministic stage does not decide final repair. |
| 10 | `2` | `sl9_decision` | `fixbatch-2-sha256-d21d7baa580` | accept=2, reject=0 | `sl10_review` | `sha256:022a18b5cb4d9bbc9bd9f5dbcb9d53df8e63bd2d505d481bcff8d876d1a5a99c` | Accepted both new SL-7 model-review requests because they provide new hard NL-fidelity and unsafe-recovery evidence about AllThermalBatteryLack, distinct from the previously waived local matcher warnings., Preserved all twelve required dispatch states and all required guard-driven selection structure, including transition:select_all_thermal_battery_lack as the forced guard to AllThermalBatteryLack., Added `illegal_overload_state` as a concrete diagnostic marker for the NL statement that the overload completion state is illegal and shall never occur in practice., ... +3 |
| 11 | `2` | `sl10_review` | `fixbatch-2-sha256-d21d7baa580` | accept=2, reject=0 | `sc11_accept_then_sd2` | `sha256:022a18b5cb4d9bbc9bd9f5dbcb9d53df8e63bd2d505d481bcff8d876d1a5a99c` | repair_memory:sl10_evidence, repair_memory:sl10_evidence, repair_memory:sl10_evidence, ... +5 |
| 12 | `3` | `request_batch` | `fixbatch-3-sha256-5bb8c5e25f4` | accept=0, reject=0 | `sl9_decision_and_repair` | `<none>` | SD-8 produced FixRequestBatch; deterministic stage does not decide final repair. |
| 13 | `3` | `sl9_decision` | `fixbatch-3-sha256-5bb8c5e25f4` | accept=1, reject=0 | `sl10_review` | `sha256:fea8ed50cc9bf814763d6cfb0bfa81ebc61727c81131b056e604e37f0532444a` | Accepted the new SL-7 model-review request because it identifies a real guard-coverage gap, not a previously waived local matcher warning: for SoC < 0.2 and deficit above the former LowSoCDGChargeMargin upper bound but not above Pgmax + Pd1max + eng3_Pmax, no state could be selected., Preserved the latest non-regressive behavior and all required grounded elements: all twelve states, external inputs PL/Ppv/Pw/SoC/Pbatmax/Pgmax/Pd1max/eng3_Pmax, aggregate command variables, low-SoC margin states, and the exceptional AllThermalBatteryLack state remain present., The low-SoC gap is closed in two minimal edits: LowSoCDGChargeMargin now extends its Pd1max/10 charging-margin logic through the DG2/eng3 capacity range when the margin fits; LNGDG1DG2 now covers low-SoC high-deficit cases up to all thermal capacity when adding the margin would exceed total thermal capacity., ... +3 |
| 14 | `3` | `sl10_review` | `fixbatch-3-sha256-5bb8c5e25f4` | accept=1, reject=0 | `sc11_accept_then_sd2` | `sha256:fea8ed50cc9bf814763d6cfb0bfa81ebc61727c81131b056e604e37f0532444a` | repair_memory:sl10_evidence, repair_memory:sl10_evidence, repair_memory:sl10_evidence, ... +6 |

### 8. 尝试记录与成本

- `SL-1`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 5533, 'completion_chars': 18210, 'completion_tokens': 7955, 'elapsed_seconds': 145.08284196199384, 'estimated_completion_tokens': 4553, 'estimated_prompt_tokens': 6646, 'estimated_total_tokens': 11199, 'first_chunk_seconds': 45.3880784289795, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 26582, 'prompt_tokens': 6469, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 14424}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-9`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 4221, 'completion_chars': 13920, 'completion_tokens': 5467, 'elapsed_seconds': 101.89256283800933, 'estimated_completion_tokens': 3480, 'estimated_prompt_tokens': 39299, 'estimated_total_tokens': 42779, 'first_chunk_seconds': 24.5487888980133, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 157193, 'prompt_tokens': 37292, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 42759}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-10`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1015, 'completion_chars': 4625, 'completion_tokens': 1534, 'elapsed_seconds': 30.634822491003433, 'estimated_completion_tokens': 1157, 'estimated_prompt_tokens': 34562, 'estimated_total_tokens': 35719, 'first_chunk_seconds': 12.275712100992678, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 138248, 'prompt_tokens': 31827, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 33361}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-9`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 4610, 'completion_chars': 15837, 'completion_tokens': 5129, 'elapsed_seconds': 96.66979183699004, 'estimated_completion_tokens': 3960, 'estimated_prompt_tokens': 127449, 'estimated_total_tokens': 131409, 'first_chunk_seconds': 13.520582388009643, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 509794, 'prompt_tokens': 113160, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 118289}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-10`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1103, 'completion_chars': 5146, 'completion_tokens': 1613, 'elapsed_seconds': 32.24456599698169, 'estimated_completion_tokens': 1287, 'estimated_prompt_tokens': 81993, 'estimated_total_tokens': 83280, 'first_chunk_seconds': 15.581589199980954, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 327970, 'prompt_tokens': 77469, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 79082}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-9`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 4628, 'completion_chars': 15530, 'completion_tokens': 4803, 'elapsed_seconds': 90.7337909140042, 'estimated_completion_tokens': 3883, 'estimated_prompt_tokens': 185946, 'estimated_total_tokens': 189829, 'first_chunk_seconds': 7.241451107984176, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 743782, 'prompt_tokens': 144403, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 149206}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-10`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1153, 'completion_chars': 5079, 'completion_tokens': 1326, 'elapsed_seconds': 28.376745796995237, 'estimated_completion_tokens': 1270, 'estimated_prompt_tokens': 79008, 'estimated_total_tokens': 80278, 'first_chunk_seconds': 8.660555798996938, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 316030, 'prompt_tokens': 65285, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 66611}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 3870, 'completion_chars': 12938, 'completion_tokens': 5421, 'elapsed_seconds': 99.60169419500744, 'estimated_completion_tokens': 3235, 'estimated_prompt_tokens': 17825, 'estimated_total_tokens': 21060, 'first_chunk_seconds': 29.82171646799543, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 71300, 'prompt_tokens': 19051, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 24472}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 3029, 'completion_chars': 9338, 'completion_tokens': 3548, 'elapsed_seconds': 66.56837784100208, 'estimated_completion_tokens': 2335, 'estimated_prompt_tokens': 21225, 'estimated_total_tokens': 23560, 'first_chunk_seconds': 11.961939176981105, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 84897, 'prompt_tokens': 23040, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 26588}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 3684, 'completion_chars': 11420, 'completion_tokens': 4062, 'elapsed_seconds': 75.18245884298813, 'estimated_completion_tokens': 2855, 'estimated_prompt_tokens': 21571, 'estimated_total_tokens': 24426, 'first_chunk_seconds': 8.813019250985235, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 86282, 'prompt_tokens': 23433, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 27495}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-7`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 2047, 'completion_chars': 8761, 'completion_tokens': 3846, 'elapsed_seconds': 71.68122501901235, 'estimated_completion_tokens': 2191, 'estimated_prompt_tokens': 46787, 'estimated_total_tokens': 48978, 'first_chunk_seconds': 34.638783863018034, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 187146, 'prompt_tokens': 53889, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 57735}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-9`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 3725, 'completion_chars': 12080, 'completion_tokens': 4966, 'elapsed_seconds': 93.81077065202408, 'estimated_completion_tokens': 3020, 'estimated_prompt_tokens': 167652, 'estimated_total_tokens': 170672, 'first_chunk_seconds': 26.605657995009096, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 670606, 'prompt_tokens': 127679, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 132645}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-10`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1037, 'completion_chars': 4918, 'completion_tokens': 1342, 'elapsed_seconds': 26.739997040014714, 'estimated_completion_tokens': 1230, 'estimated_prompt_tokens': 62023, 'estimated_total_tokens': 63253, 'first_chunk_seconds': 9.116892652004026, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 248092, 'prompt_tokens': 51297, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 52639}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 3759, 'completion_chars': 11746, 'completion_tokens': 4189, 'elapsed_seconds': 82.8817868779879, 'estimated_completion_tokens': 2937, 'estimated_prompt_tokens': 24885, 'estimated_total_tokens': 27822, 'first_chunk_seconds': 15.11647721598274, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 99539, 'prompt_tokens': 27121, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 31310}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-7`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 2200, 'completion_chars': 9362, 'completion_tokens': 3228, 'elapsed_seconds': 60.83706069199252, 'estimated_completion_tokens': 2341, 'estimated_prompt_tokens': 49970, 'estimated_total_tokens': 52311, 'first_chunk_seconds': 21.184930005983915, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 199879, 'prompt_tokens': 57228, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 60456}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-9`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 4003, 'completion_chars': 12815, 'completion_tokens': 5035, 'elapsed_seconds': 96.10194571100874, 'estimated_completion_tokens': 3204, 'estimated_prompt_tokens': 130982, 'estimated_total_tokens': 134186, 'first_chunk_seconds': 23.908172739000292, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 523925, 'prompt_tokens': 101289, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 106324}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-10`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1271, 'completion_chars': 5563, 'completion_tokens': 1601, 'elapsed_seconds': 31.4299864229979, 'estimated_completion_tokens': 1391, 'estimated_prompt_tokens': 25422, 'estimated_total_tokens': 26813, 'first_chunk_seconds': 8.477692799002398, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 101688, 'prompt_tokens': 25070, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 26671}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 4885, 'completion_chars': 16403, 'completion_tokens': 6958, 'elapsed_seconds': 127.46316564100562, 'estimated_completion_tokens': 4101, 'estimated_prompt_tokens': 27346, 'estimated_total_tokens': 31447, 'first_chunk_seconds': 39.44680727500236, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 109384, 'prompt_tokens': 29824, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 36782}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-7`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1956, 'completion_chars': 8718, 'completion_tokens': 3151, 'elapsed_seconds': 59.454387625999516, 'estimated_completion_tokens': 2180, 'estimated_prompt_tokens': 53549, 'estimated_total_tokens': 55729, 'first_chunk_seconds': 24.158722168998793, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 214194, 'prompt_tokens': 61285, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 64436}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。

### 9. 最终停止状态与后续含义

- 停止状态：verdict=`success`，record_status=`success`。
- 主要原因分类：`success`。
- required stages executed：`58/16`，missing=`<none>`。
- repairs：`4/5` accepted；scenario_history=`7`。
- 配置含义：`recommended baseline candidate`；该结果可用于评估默认入口本身。
- 主结果/蓝本边界：`main_result_eligible` 只表示该 run 非 provider-invalid 且 trace/schema/secret/final-verdict 口径可进入主结果候选；`path2_ref_model_blueprint_eligible=false` 时，模型仍可作为 FE/BVS 或 dispatch-classifier 压力测试证据，但不得称为 Path2 ref-model 主蓝本。
- 样本含义：若出现 `design_or_variable_dynamics`，应重点审查变量是否仅作为 guard/input 常量而没有事件/动作更新；若出现 pre-scenario parse/semantic 失败，则应先优化 pyfcstm grammar adherence。
