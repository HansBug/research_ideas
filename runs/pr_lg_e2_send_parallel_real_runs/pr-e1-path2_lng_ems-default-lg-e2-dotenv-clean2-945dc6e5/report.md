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
| Git commit | `93e4aa88d1e85c708aab022ca299b8f4fc343ae5` |
| clean / diff / prompt snapshot | clean=`True`, dirty=`False`, diff_hash=`sha256:2a69ad5797ac568a81bddcef615104303a97261094685f4edd8d4484e889ea09`, prompt_hash=`sha256:29acd3d1171a37b465f2b9278c85877dcbc5703e2d154247154b0c8cb90d6c8e` |
| provider/model 脱敏标识 | mode=`real_env`, model=`gpt-5.5`, real_api=`True` |
| source / paper | source=`project_1_llm_state_machine_modeling/sources/state-transitions-logical-design-for-hybrid-energy-generation-with-renewable-energy-sources-in-lng-ship`, paper=`project_1_llm_state_machine_modeling/sources/state-transitions-logical-design-for-hybrid-energy-generation-with-renewable-energy-sources-in-lng-ship/paper.pdf` |
| 样本筛选理由 | issue #14 / PR-D 代表性 Path2 EFSM，变量、guard、12 个状态和非法状态都明确；但它可能退化为条件分类式 dispatch，因此更适合作为 FE/BVS 压力测试，是否适合作为 Path2 ref-model 蓝本需看最终 DSL 是否具有 state-dependent mode memory。 |
| 变量参与说明 | `PL/Ppv/Pw/SoC/eng*_Pmax` 是环境输入/容量边界，适合暴露 SD-4 对外部输入变量的处理能力。 |
| run_id | `pr-e1-path2_lng_ems-default-lg-e2-dotenv-clean2-945dc6e5` |
| final verdict/status | verdict=`success`, record=`success`, result=`converged` |
| main_result_eligible | `true` |
| state_mode_decorative_detected | `true` |
| path2_ref_model_blueprint_eligible | `false`；state_mode_decorative: final DSL is dominated by root-level forced guard reclassification; valid as FE/BVS or dispatch-classifier stress evidence, but not a Path2 ref-model blueprint |
| final.fcstm 来源 | `{"accepted": true, "accepted_after_rework": false, "final_dsl_hash": "sha256:a94551f062423d91b55b99075201100b6caf098b41ba33f7779df2d3ca5a111a", "iteration": 1, "matching_repair_history_indices": [0, 1], "repair_history_index": 1, "selected_source_stage": "SD-4", "sl10_decision": "pass", "source_kind": "repair_candidate"}` |
| SC-11 post-accept validation | attempted=`false`；attempts=`0`；success=`0`；failure=`0` |
| FixLog next_action 序列 | `sl9_decision_and_repair, sl10_review, sc11_accept_then_sd2, sl9_decision_and_repair, sl10_review, sc11_accept_then_sd2` |
| iteration exit_reason 序列 | `candidate_accepted_for_next_full_pass, candidate_accepted_for_next_full_pass, full_pass_all_required_feedback_ok` |
| token/cost/time | tokens=`{'prompt_tokens': 291841, 'completion_tokens': 33541, 'total_tokens': 325382, 'estimated_prompt_tokens': 300427, 'estimated_completion_tokens': 23394, 'estimated_total_tokens': 323821, 'prompt_chars': 1201695, 'completion_chars': 93561, 'n_calls': 8, 'token_usage_available': True, 'token_usage_unavailable_calls': 0}`, elapsed=`664.304s` |
| run record | [`pr-e1-path2_lng_ems-default-lg-e2-dotenv-clean2-945dc6e5.agent_loop.json.gz`](./pr-e1-path2_lng_ems-default-lg-e2-dotenv-clean2-945dc6e5.agent_loop.json.gz) |
| summary/log/final DSL | [`summary.json`](./summary.json), [`checks.json`](./checks.json), [`reproducibility.json`](./reproducibility.json), [`flow_log.json`](./flow_log.json), [`fix_log.json`](./fix_log.json), [`final.fcstm`](./final.fcstm), [`stdout.txt`](./run_logs/stdout.txt), [`stderr.txt`](./run_logs/stderr.txt) |

### 1.1 LangGraph runtime metadata / checkpoint 口径

| 字段 | 值 |
|---|---|
| `graph_runtime_backend` | `langgraph` |
| `graph_runtime_status` | `enabled` |
| `graph_runtime_backend_version` | `pr-langgraph.stategraph.v1` |
| `langgraph_version` | `1.1.6` |
| `langgraph_checkpoint_version` | `4.0.1` |
| `graph_runtime_id` | `langgraph:pr-langgraph.stategraph.v1` |
| `graph_config_hash` | `sha256:c30f60349ac9c3b6f4a6c3dcceb3696e6f553ab11d7c93de8ac2ed969306ce7f` |
| `node_edge_schema_version` | `pr-langgraph.stage-nodes.v1` |
| `checkpoint_backend` | `memory` |
| `checkpoint_backend_type` | `InMemorySaver` |
| `checkpoint_serde` | `pickle` |
| `checkpoint_path_hash` | `sha256:memory` |
| `resumed_from_checkpoint` | `False` |
| `resume_checkpoint_id_hash` | `None` |
| `instrumentation_layer` | `langgraph` |
| `stage_semantics_module` | `method.staged_runtime` |
| `langgraph_node_trace_count` | `50` |
| `langgraph_node_trace_hash` | `sha256:c95b8b7d8f7ca4463610743df96a0426603274ad00e5a67b6b2c5eaa14a209bc` |
| `langgraph_compat_ok` | `True` |
| `checkpoint_resume_smoke_scope` | `toy_ledger_langgraph_api_smoke` |
| `real_agent_loop_resume_supported` | `False` |
| `resume_append_only` | `True` |
| `final_trace_delegated_monolithic_runtime` | `False` |
| `final_trace_node_trace_count` | `50` |

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
def float SoC = 0.5;
def float eng3_Pmax = 0.0;
def float Pd1max = 0.0;
def float Pd2max = 0.0;
def float Pbdismax = 0.0;
def float Pgmax = 0.0;
def float Pg_req = 0.0;
def float Pbd_req = 0.0;
def float Pbc_req = 0.0;
def float spare_power = 0.0;
def int cmd_LNG_cut_in = 0;
def int cmd_LNG_cut_out = 1;
def int cmd_DG1_cut_in = 0;
def int cmd_DG1_cut_out = 1;
def int cmd_DG2_cut_in = 0;
def int cmd_DG2_cut_out = 1;
def int cmd_load_cut_in = 1;
def int cmd_load_cut_out = 0;

state LNGShipEMS {
    ! * -> ZeroLoadCharge : if [PL == 0.0 && Ppv + Pw > 0.0 && SoC < 0.95];
    ! * -> ZeroLoadSpare : if [PL == 0.0 && Ppv + Pw > 0.0 && SoC >= 0.95];
    ! * -> ResCoversCharge : if [PL > 0.0 && Ppv + Pw >= PL && SoC < 0.95];
    ! * -> ResCoversSpare : if [PL > 0.0 && Ppv + Pw >= PL && SoC >= 0.95];
    ! * -> BatteryOnly : if [PL > 0.0 && Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw <= Pbdismax];
    ! * -> BatteryLng : if [PL > 0.0 && Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw > Pbdismax && PL - Ppv - Pw <= Pbdismax + eng3_Pmax];
    ! * -> BatteryLngDg1 : if [PL > 0.0 && Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw > Pbdismax + eng3_Pmax && PL - Ppv - Pw <= Pbdismax + eng3_Pmax + Pd1max];
    ! * -> AllThermalNormalSoc : if [PL > 0.0 && Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw > Pbdismax + eng3_Pmax + Pd1max && PL - Ppv - Pw <= Pbdismax + eng3_Pmax + Pd1max + Pd2max];
    ! * -> LngChargeLowSoc : if [PL > 0.0 && Ppv + Pw < PL && SoC < 0.2 && PL - Ppv - Pw + Pgmax / 5.0 <= eng3_Pmax];
    ! * -> LngDg1ChargeLowSoc : if [PL > 0.0 && Ppv + Pw < PL && SoC < 0.2 && PL - Ppv - Pw + Pgmax / 5.0 > eng3_Pmax && PL - Ppv - Pw + Pd1max / 10.0 <= eng3_Pmax + Pd1max];
    ! * -> LngDg1Dg2ChargeLowSoc : if [PL > 0.0 && Ppv + Pw < PL && SoC < 0.2 && PL - Ppv - Pw + Pd1max / 10.0 > eng3_Pmax + Pd1max && PL - Ppv - Pw + Pd1max / 10.0 <= eng3_Pmax + Pd1max + Pd2max];
    ! * -> OverloadCompletionIllegal : if [PL > 0.0 && Ppv + Pw < PL && ((SoC >= 0.2 && PL - Ppv - Pw > Pbdismax + eng3_Pmax + Pd1max + Pd2max) || (SoC < 0.2 && PL - Ppv - Pw + Pd1max / 10.0 > eng3_Pmax + Pd1max + Pd2max))];

    [*] -> ZeroLoadCharge;

    state ZeroLoadCharge {
        during {
            Pg_req = 0.0;
            Pbd_req = 0.0;
            Pbc_req = Ppv + Pw;
            spare_power = 0.0;
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

    state ZeroLoadSpare {
        during {
            Pg_req = 0.0;
            Pbd_req = 0.0;
            Pbc_req = 0.0;
            spare_power = Ppv + Pw;
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

    state ResCoversCharge {
        during {
            Pg_req = 0.0;
            Pbd_req = 0.0;
            Pbc_req = Ppv + Pw - PL;
            spare_power = 0.0;
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

    state ResCoversSpare {
        during {
            Pg_req = 0.0;
            Pbd_req = 0.0;
            Pbc_req = 0.0;
            spare_power = Ppv + Pw - PL;
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

    state BatteryOnly {
        during {
            Pg_req = 0.0;
            Pbd_req = PL - Ppv - Pw;
            Pbc_req = 0.0;
            spare_power = 0.0;
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

    state BatteryLng {
        during {
            Pg_req = PL - Ppv - Pw - Pbdismax;
            Pbd_req = Pbdismax;
            Pbc_req = 0.0;
            spare_power = 0.0;
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

    state BatteryLngDg1 {
        during {
            Pg_req = PL - Ppv - Pw - Pbdismax;
            Pbd_req = Pbdismax;
            Pbc_req = 0.0;
            spare_power = 0.0;
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

    state AllThermalNormalSoc {
        during {
            Pg_req = PL - Ppv - Pw - Pbdismax;
            Pbd_req = Pbdismax;
            Pbc_req = 0.0;
            spare_power = 0.0;
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

    state LngChargeLowSoc {
        during {
            Pg_req = PL - Ppv - Pw + Pgmax / 5.0;
            Pbd_req = 0.0;
            Pbc_req = Pgmax / 5.0;
            spare_power = 0.0;
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

    state LngDg1ChargeLowSoc {
        during {
            Pg_req = PL - Ppv - Pw + Pd1max / 10.0;
            Pbd_req = 0.0;
            Pbc_req = Pd1max / 10.0;
            spare_power = 0.0;
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

    state LngDg1Dg2ChargeLowSoc {
        during {
            Pg_req = PL - Ppv - Pw + Pd1max / 10.0;
            Pbd_req = 0.0;
            Pbc_req = Pd1max / 10.0;
            spare_power = 0.0;
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

    state OverloadCompletionIllegal {
        during {
            Pg_req = eng3_Pmax + Pd1max + Pd2max;
            Pbd_req = PL - Ppv - Pw - eng3_Pmax - Pd1max - Pd2max;
            Pbc_req = 0.0;
            spare_power = 0.0;
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

### 4. 全流程真实摘要表

| Stage | 是否 LLM | iteration | 结果 | 获取的信息 / 反馈 | 本阶段做了什么 | DSL 修改 | artifact/log |
|---|---:|---:|---:|---|---|---|---|
| `SC-0` | 否 | - | ✅ | trace/control | 初始化 run state | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e2-dotenv-clean2-945dc6e5.agent_loop.json.gz) |
| `SL-1` | 是 | - | ✅ | LLM calls=1, tokens=14747 | 生成初始 DSL 与 grounding seeds | initial len=7711 | [`record`](./pr-e1-path2_lng_ems-default-lg-e2-dotenv-clean2-945dc6e5.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e2-dotenv-clean2-945dc6e5.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e2-dotenv-clean2-945dc6e5.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ⚠️ | blocking=74, advisory=228, info=0; blocking=74, advisory=228, info=0; blocking=0, advisory=302, info=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e2-dotenv-clean2-945dc6e5.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e2-dotenv-clean2-945dc6e5.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=2, tokens=106200 | LLM per-request accept/reject + repair | candidate len=7711,7711 | [`record`](./pr-e1-path2_lng_ems-default-lg-e2-dotenv-clean2-945dc6e5.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=2, tokens=85070 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e2-dotenv-clean2-945dc6e5.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e2-dotenv-clean2-945dc6e5.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e2-dotenv-clean2-945dc6e5.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e2-dotenv-clean2-945dc6e5.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ⚠️ | blocking=74, advisory=228, info=0; blocking=74, advisory=228, info=0; blocking=0, advisory=302, info=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e2-dotenv-clean2-945dc6e5.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e2-dotenv-clean2-945dc6e5.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=2, tokens=106200 | LLM per-request accept/reject + repair | candidate len=7711,7711 | [`record`](./pr-e1-path2_lng_ems-default-lg-e2-dotenv-clean2-945dc6e5.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=2, tokens=85070 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e2-dotenv-clean2-945dc6e5.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e2-dotenv-clean2-945dc6e5.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e2-dotenv-clean2-945dc6e5.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e2-dotenv-clean2-945dc6e5.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=74, advisory=228, info=0; blocking=74, advisory=228, info=0; blocking=0, advisory=302, info=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e2-dotenv-clean2-945dc6e5.agent_loop.json.gz) |
| `SL-5` | 是 | 2 | ✅ | LLM calls=2, tokens=48413 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e2-dotenv-clean2-945dc6e5.agent_loop.json.gz) |
| `SD-5A` | 否 | 2 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e2-dotenv-clean2-945dc6e5.agent_loop.json.gz) |
| `SL-5` | 是 | 2 | ✅ | LLM calls=2, tokens=48413 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e2-dotenv-clean2-945dc6e5.agent_loop.json.gz) |
| `SD-5A` | 否 | 2 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e2-dotenv-clean2-945dc6e5.agent_loop.json.gz) |
| `SC-5F` | 否 | 2 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e2-dotenv-clean2-945dc6e5.agent_loop.json.gz) |
| `SD-6` | 否 | 2 | ✅ | ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e2-dotenv-clean2-945dc6e5.agent_loop.json.gz) |
| `SL-7` | 是 | 2 | ✅ | LLM calls=1, tokens=70952 | LLM model review | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e2-dotenv-clean2-945dc6e5.agent_loop.json.gz) |
| `SC-12` | 否 | - | ✅ | full_pass_all_required_feedback_ok | 写 final verdict | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e2-dotenv-clean2-945dc6e5.agent_loop.json.gz) |
| `SC-13` | 否 | - | ✅ | trace/control | 写审计 run record | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e2-dotenv-clean2-945dc6e5.agent_loop.json.gz) |

### 4.1 完整流程日志（stage/control-flow replay ledger）

口径：本节来自 `AgentLoopRunRecord.logs`，与 [`flow_log.json`](./flow_log.json) 一致；用于复现每个 stage 如何进入、得到什么批示、跳转到哪里，以及每次 DSL 产物/候选如何变化。

| # | ts | stage | iter | event | result / jump | DSL evidence |
|---:|---|---|---:|---|---|---|
| 1 | `2026-06-06T08:05:29Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 2 | `2026-06-06T08:05:29Z` | `SC-0` | `-` | `run_start` | {} | <none> |
| 3 | `2026-06-06T08:05:29Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 4 | `2026-06-06T08:05:29Z` | `SL-1` | `-` | `stage_enter` | {"reason": "initial_modeling_adapter_available"} | <none> |
| 5 | `2026-06-06T08:08:05Z` | `SL-1` | `-` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 6 | `2026-06-06T08:08:05Z` | `SL-1` | `-` | `stage_result` | {"jump": "SD-2", "ok": true} | candidate_dsl:len=7711,hash=sha256:a94551f06242 |
| 7 | `2026-06-06T08:08:05Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 8 | `2026-06-06T08:08:05Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 9 | `2026-06-06T08:08:05Z` | `<control>` | `0` | `iteration_enter` | {} | current_hash=sha256:a94551f062423d91b55b99075201100b6caf098b41ba33f7779df2d3ca5a111a |
| 10 | `2026-06-06T08:08:05Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 11 | `2026-06-06T08:08:05Z` | `<control>` | `0` | `iteration_validation_enter` | {} | dsl:len=7711,hash=sha256:a94551f06242, current_hash=sha256:a94551f062423d91b55b99075201100b6caf098b41ba33f7779df2d3ca5a111a |
| 12 | `2026-06-06T08:08:05Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 13 | `2026-06-06T08:08:05Z` | `SD-2` | `0` | `stage_enter` | {"reason": "full_validation_pass"} | <none> |
| 14 | `2026-06-06T08:08:05Z` | `SD-2` | `0` | `stage_result` | {"jump": "SD-3", "ok": true, "status": "StageStatus.OK"} | <none> |
| 15 | `2026-06-06T08:08:05Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 16 | `2026-06-06T08:08:05Z` | `SD-3` | `0` | `stage_enter` | {"reason": "SD-2 ok"} | <none> |
| 17 | `2026-06-06T08:08:05Z` | `SD-3` | `0` | `stage_result` | {"jump": "SD-4", "ok": true, "status": "StageStatus.OK"} | <none> |
| 18 | `2026-06-06T08:08:05Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 19 | `2026-06-06T08:08:05Z` | `SD-4` | `0` | `stage_enter` | {"reason": "SD-3 ok"} | <none> |
| 20 | `2026-06-06T08:08:06Z` | `SD-4` | `0` | `stage_result` | {"jump": "SD-8", "ok": false, "status": "StageStatus.FAIL"} | <none> |
| 21 | `2026-06-06T08:08:06Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 22 | `2026-06-06T08:08:06Z` | `<control>` | `0` | `iteration_validation_result` | {"jump": "SD-8 repair", "selected_feedback": {"blocking": true, "blocking_instance_keys": ["W_UNWRITTEN_READ_VAR:var_name=Pd2max", "W_UNWRITTEN_READ_VAR:var_name=Pbdismax", "W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.BatteryOnly", "W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.BatteryLng", "W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoad...<truncated 19863 chars> | <none> |
| 23 | `2026-06-06T08:08:06Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 24 | `2026-06-06T08:08:06Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 25 | `2026-06-06T08:08:06Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 26 | `2026-06-06T08:08:06Z` | `SD-8` | `0` | `repair_path_enter` | {"jump": "SD-8", "selected_feedback": {"blocking": true, "blocking_instance_keys": ["W_UNWRITTEN_READ_VAR:var_name=Pd2max", "W_UNWRITTEN_READ_VAR:var_name=Pbdismax", "W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.BatteryOnly", "W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.BatteryLng", "W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:...<truncated 248320 chars> | current_dsl:len=7711,hash=sha256:a94551f06242 |
| 27 | `2026-06-06T08:08:06Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 28 | `2026-06-06T08:08:06Z` | `SD-8` | `0` | `stage_result` | {"jump": "SL-9", "ok": true, "status": "StageStatus.OK"} | <none> |
| 29 | `2026-06-06T08:08:06Z` | `SD-8` | `0` | `fix_request_batch` | {"request_count": 12} | <none> |
| 30 | `2026-06-06T08:08:06Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 31 | `2026-06-06T08:08:06Z` | `SL-9` | `0` | `stage_enter` | {"reason": "fix_requests_ready"} | old_dsl:len=7711,hash=sha256:a94551f06242 |
| 32 | `2026-06-06T08:09:44Z` | `SL-9` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 33 | `2026-06-06T08:09:44Z` | `SL-9` | `0` | `stage_result` | {"accepted_request_ids": ["fixreq-0-sd4-0-004a2744db", "fixreq-0-sd4-1-ac19caf402", "fixreq-0-sd4-2-a85904e5ae", "fixreq-0-sd4-3-63111cf4c5", "fixreq-0-sd4-4-1c37eb99a0", "fixreq-0-sd4-5-684ca59bf4", "fixreq-0-sd4-6-53b0ac9354", "fixreq-0-sd4-7-7996b67982", "fixreq-0-sd4-8-eb7c8ae12b", "fixreq-0-sd4-9-3c1a198645", "fixreq-0-sd4-10-7e80c093d6", "fixreq-0-sd4-11-2b935a4955"], "jump": "SL-10", "ok": true, "rejected_requ...<truncated 13 chars> | candidate_dsl:len=7711,hash=sha256:a94551f06242 |
| 34 | `2026-06-06T08:09:44Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 35 | `2026-06-06T08:09:45Z` | `SD-10` | `0` | `stage_result` | {"jump": "SL-10", "ok": false, "status": "StageStatus.FAIL"} | <none> |
| 36 | `2026-06-06T08:09:45Z` | `SL-10` | `0` | `stage_enter` | {"reason": "candidate_dsl_and_local_evidence_ready"} | candidate_hash=sha256:a94551f062423d91b55b99075201100b6caf098b41ba33f7779df2d3ca5a111a |
| 37 | `2026-06-06T08:10:04Z` | `SL-10` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 38 | `2026-06-06T08:10:04Z` | `SL-10` | `0` | `stage_result` | {"decision": "pass", "jump": "SC-11", "ok": true} | <none> |
| 39 | `2026-06-06T08:10:04Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 40 | `2026-06-06T08:10:04Z` | `SC-11` | `0` | `stage_result` | {"jump": "SD-2 next iteration", "ok": true, "reason": "SL-10 accepted candidate; next iteration must restart at SD-2"} | candidate_dsl:len=7711,hash=sha256:a94551f06242 |
| 41 | `2026-06-06T08:10:04Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 42 | `2026-06-06T08:10:04Z` | `<control>` | `0` | `iteration_repair_result` | {"accepted": true, "jump": "SD-2 next iteration"} | current_hash=sha256:a94551f062423d91b55b99075201100b6caf098b41ba33f7779df2d3ca5a111a |
| 43 | `2026-06-06T08:10:04Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 44 | `2026-06-06T08:10:04Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 45 | `2026-06-06T08:10:04Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 46 | `2026-06-06T08:10:05Z` | `<control>` | `1` | `iteration_enter` | {} | current_hash=sha256:a94551f062423d91b55b99075201100b6caf098b41ba33f7779df2d3ca5a111a |
| 47 | `2026-06-06T08:10:05Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 48 | `2026-06-06T08:10:05Z` | `<control>` | `1` | `iteration_validation_enter` | {} | dsl:len=7711,hash=sha256:a94551f06242, current_hash=sha256:a94551f062423d91b55b99075201100b6caf098b41ba33f7779df2d3ca5a111a |
| 49 | `2026-06-06T08:10:05Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 50 | `2026-06-06T08:10:05Z` | `SD-2` | `1` | `stage_enter` | {"reason": "full_validation_pass"} | <none> |
| 51 | `2026-06-06T08:10:05Z` | `SD-2` | `1` | `stage_result` | {"jump": "SD-3", "ok": true, "status": "StageStatus.OK"} | <none> |
| 52 | `2026-06-06T08:10:05Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 53 | `2026-06-06T08:10:05Z` | `SD-3` | `1` | `stage_enter` | {"reason": "SD-2 ok"} | <none> |
| 54 | `2026-06-06T08:10:05Z` | `SD-3` | `1` | `stage_result` | {"jump": "SD-4", "ok": true, "status": "StageStatus.OK"} | <none> |
| 55 | `2026-06-06T08:10:05Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 56 | `2026-06-06T08:10:05Z` | `SD-4` | `1` | `stage_enter` | {"reason": "SD-3 ok"} | <none> |
| 57 | `2026-06-06T08:10:05Z` | `SD-4` | `1` | `stage_result` | {"jump": "SD-8", "ok": false, "status": "StageStatus.FAIL"} | <none> |
| 58 | `2026-06-06T08:10:05Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 59 | `2026-06-06T08:10:05Z` | `<control>` | `1` | `iteration_validation_result` | {"jump": "SD-8 repair", "selected_feedback": {"blocking": true, "blocking_instance_keys": ["W_UNWRITTEN_READ_VAR:var_name=Pd2max", "W_UNWRITTEN_READ_VAR:var_name=Pbdismax", "W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.BatteryOnly", "W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.BatteryLng", "W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoad...<truncated 19863 chars> | <none> |
| 60 | `2026-06-06T08:10:05Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 61 | `2026-06-06T08:10:05Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 62 | `2026-06-06T08:10:05Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 63 | `2026-06-06T08:10:05Z` | `SD-8` | `1` | `repair_path_enter` | {"jump": "SD-8", "selected_feedback": {"blocking": true, "blocking_instance_keys": ["W_UNWRITTEN_READ_VAR:var_name=Pd2max", "W_UNWRITTEN_READ_VAR:var_name=Pbdismax", "W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.BatteryOnly", "W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.BatteryLng", "W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:...<truncated 248320 chars> | current_dsl:len=7711,hash=sha256:a94551f06242 |
| 64 | `2026-06-06T08:10:05Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 65 | `2026-06-06T08:10:06Z` | `SD-8` | `1` | `stage_result` | {"jump": "SL-9", "ok": true, "status": "StageStatus.OK"} | <none> |
| 66 | `2026-06-06T08:10:06Z` | `SD-8` | `1` | `fix_request_batch` | {"request_count": 12} | <none> |
| 67 | `2026-06-06T08:10:06Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 68 | `2026-06-06T08:10:06Z` | `SL-9` | `1` | `stage_enter` | {"reason": "fix_requests_ready"} | old_dsl:len=7711,hash=sha256:a94551f06242 |
| 69 | `2026-06-06T08:11:38Z` | `SL-9` | `1` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 70 | `2026-06-06T08:11:38Z` | `SL-9` | `1` | `stage_result` | {"accepted_request_ids": ["fixreq-1-sd4-0-f26560796c", "fixreq-1-sd4-1-c951ee247d", "fixreq-1-sd4-2-71428c35ee", "fixreq-1-sd4-3-a578ad8034", "fixreq-1-sd4-4-f1a79d5d37", "fixreq-1-sd4-5-0d78ca18de", "fixreq-1-sd4-6-8a19f87ff5", "fixreq-1-sd4-7-968c971cfc", "fixreq-1-sd4-8-f5dda30df3", "fixreq-1-sd4-9-eafff4b184", "fixreq-1-sd4-10-93c5d5ba5a", "fixreq-1-sd4-11-e5f31116bc"], "jump": "SL-10", "ok": true, "rejected_requ...<truncated 13 chars> | candidate_dsl:len=7711,hash=sha256:a94551f06242 |
| 71 | `2026-06-06T08:11:38Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 72 | `2026-06-06T08:11:39Z` | `SD-10` | `1` | `stage_result` | {"jump": "SL-10", "ok": true, "status": "StageStatus.OK"} | <none> |
| 73 | `2026-06-06T08:11:39Z` | `SL-10` | `1` | `stage_enter` | {"reason": "candidate_dsl_and_local_evidence_ready"} | candidate_hash=sha256:a94551f062423d91b55b99075201100b6caf098b41ba33f7779df2d3ca5a111a |
| 74 | `2026-06-06T08:11:54Z` | `SL-10` | `1` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 75 | `2026-06-06T08:11:54Z` | `SL-10` | `1` | `stage_result` | {"decision": "pass", "jump": "SC-11", "ok": true} | <none> |
| 76 | `2026-06-06T08:11:54Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 77 | `2026-06-06T08:11:54Z` | `SC-11` | `1` | `stage_result` | {"jump": "SD-2 next iteration", "ok": true, "reason": "SL-10 accepted candidate; next iteration must restart at SD-2"} | candidate_dsl:len=7711,hash=sha256:a94551f06242 |
| 78 | `2026-06-06T08:11:54Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 79 | `2026-06-06T08:11:54Z` | `<control>` | `1` | `iteration_repair_result` | {"accepted": true, "jump": "SD-2 next iteration"} | current_hash=sha256:a94551f062423d91b55b99075201100b6caf098b41ba33f7779df2d3ca5a111a |
| 80 | `2026-06-06T08:11:54Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
- ……另有 `48` 条流程日志见 [`flow_log.json`](./flow_log.json) / run record。

### 5. Iteration / repair / review 摘要

| Iter | selected feedback | repair? | FixRequestBatch | SL-9 | local checks | SL-10 | 回到 SD-2? | verdict/备注 |
|---:|---|---|---|---|---|---|---|---|
| 0 | `SD-4` | yes | fixbatch-0-sha256-002b698f3f7 / n=12 | accept=12, reject=0, waiver=0 | ok=False, target=False, regression=False, drift=none, local_stage=SD-10, reason=design_target_unresolved | decision=pass, ok=True, target=True, regression=False, drift=none, rework=<none> | yes | candidate_accepted_for_next_full_pass |
| 1 | `SD-4` | yes | fixbatch-1-sha256-002b698f3f7 / n=12 | accept=12, reject=0, waiver=0 | ok=True, target=True, regression=False, drift=none, local_stage=SD-10, reason= | decision=pass, ok=True, target=True, regression=False, drift=none, rework=<none> | yes | candidate_accepted_for_next_full_pass |
| 2 | `<none>` | no | <none> | <none> | <none> | <none> | no | full_pass_all_required_feedback_ok |

### 6. Scenario 明细与逐轮通过情况

#### 6.1 Scenario pass/fail by iteration

口径：`✅` = 该 scenario 在该轮 SD-6 simulation 通过；`❌` = 该轮失败；`⚪` = 该轮未执行或无该 scenario 结果。

| Scenario | Intent | Iter 3 |
|---|---|---|
| `default_init_zero_load_charge` | default-init dispatches to the zero-load charging mode when PL is zero and renewable production is available below the 0...<truncated 18 chars> | ✅ |
| `zero_load_soc_boundary_spare` | explicit-hot-start probes the SoC=0.95 boundary for PL=0, where renewable production should become spare power rather th...<truncated 20 chars> | ✅ |
| `res_covers_charge_below_soc_boundary` | explicit-hot-start probes RES covering positive load with SoC just below 0.95, expecting residual renewable power to cha...<truncated 16 chars> | ✅ |
| `res_covers_soc_boundary_spare` | explicit-hot-start probes RES covering positive load at SoC=0.95, expecting residual renewable power to be reported as s...<truncated 5 chars> | ✅ |
| `battery_only_soc_and_capacity_boundary` | explicit-hot-start probes suitable SoC at exactly 0.2 and deficit exactly equal to battery discharge capacity, expecting...<truncated 23 chars> | ✅ |
| `battery_lng_capacity_boundary` | explicit-hot-start probes deficit above battery capacity but exactly covered by battery plus LNG, expecting LNG cut-in a...<truncated 20 chars> | ✅ |
| `battery_lng_dg1_capacity_boundary` | explicit-hot-start probes deficit above battery plus LNG but exactly covered after DG1, expecting DG1 cut-in while DG2 r...<truncated 11 chars> | ✅ |
| `all_thermal_normal_soc_capacity_boundary` | explicit-hot-start probes normal-SoC deficit above battery plus LNG plus DG1 but exactly covered once DG2 is added. | ✅ |
| `low_soc_lng_charge_margin` | explicit-hot-start probes low SoC below 0.2 where LNG can cover load plus the Pgmax/5 charging margin. | ✅ |
| `low_soc_lng_dg1_pd1_margin` | explicit-hot-start probes low SoC where LNG alone cannot cover the charging margin and DG1 is added using the Pd1max/10 ...<truncated 7 chars> | ✅ |
| `low_soc_lng_dg1_dg2_pd1_margin` | explicit-hot-start probes low SoC where DG2 is last-priority and needed to cover the Pd1max/10 charging-margin branch. | ✅ |
| `overload_illegal_all_thermal_and_battery_lack` | explicit-hot-start probes the admitted illegal overload-completion branch: extreme demand exceeds RES and thermal resour...<truncated 81 chars> | ✅ |
| `forced_zero_load_charge_from_thermal_leaf` | explicit-hot-start targets the wildcard forced reclassification rule: from an unrelated thermal leaf, PL=0 with RES and ...<truncated 76 chars> | ✅ |

#### 6.2 Scenario definitions

<details><summary>`default_init_zero_load_charge` — default-init dispatches to the zero-load charging mode when PL is zero and renewable production is available below the 0.95 SoC threshold.</summary>

| Field | Value |
|---|---|
| description | default-init dispatches to the zero-load charging mode when PL is zero and renewable production is available below the 0.95 SoC threshold. |
| initial_state | `<default-init>` |
| initial_vars | `{"PL": 0.0, "Ppv": 30.0, "Pw": 10.0, "SoC": 0.94}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `initial_dispatch_to_zero_load_charge` | `0` | `[]` | `LNGShipEMS.ZeroLoadCharge` | `{"Pbc_req": 40.0, "Pbd_req": 0.0, "Pg_req": 0.0, "cmd_DG1_cut_out": 1, "cmd_DG2_cut_out": 1, "cmd_LNG_cut_out": 1, "cmd_load_cut_in": 1, "cmd_load_cut_out": 0, "spare_power": 0.0}` |

</details>

<details><summary>`zero_load_soc_boundary_spare` — explicit-hot-start probes the SoC=0.95 boundary for PL=0, where renewable production should become spare power rather than battery charging.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start probes the SoC=0.95 boundary for PL=0, where renewable production should become spare power rather than battery charging. |
| initial_state | `LNGShipEMS.ZeroLoadCharge` |
| initial_vars | `{"PL": 0.0, "Ppv": 30.0, "Pw": 10.0, "SoC": 0.95}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `source_state_before_reclassification` | `0` | `[]` | `LNGShipEMS.ZeroLoadCharge` | `{}` |
| 1 `zero_load_spare_selected_at_soc_threshold` | `0` | `[]` | `LNGShipEMS.ZeroLoadSpare` | `{"Pbc_req": 0.0, "Pbd_req": 0.0, "Pg_req": 0.0, "cmd_DG1_cut_out": 1, "cmd_DG2_cut_out": 1, "cmd_LNG_cut_out": 1, "cmd_load_cut_in": 1, "cmd_load_cut_out": 0, "spare_power": 40.0}` |

</details>

<details><summary>`res_covers_charge_below_soc_boundary` — explicit-hot-start probes RES covering positive load with SoC just below 0.95, expecting residual renewable power to charge the battery.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start probes RES covering positive load with SoC just below 0.95, expecting residual renewable power to charge the battery. |
| initial_state | `LNGShipEMS.ZeroLoadSpare` |
| initial_vars | `{"PL": 50.0, "Ppv": 40.0, "Pw": 20.0, "SoC": 0.94}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `source_state_before_res_covering_load` | `0` | `[]` | `LNGShipEMS.ZeroLoadSpare` | `{}` |
| 1 `residual_res_charges_battery` | `0` | `[]` | `LNGShipEMS.ResCoversCharge` | `{"Pbc_req": 10.0, "Pbd_req": 0.0, "Pg_req": 0.0, "cmd_DG1_cut_out": 1, "cmd_DG2_cut_out": 1, "cmd_LNG_cut_out": 1, "cmd_load_cut_in": 1, "cmd_load_cut_out": 0, "spare_power": 0.0}` |

</details>

<details><summary>`res_covers_soc_boundary_spare` — explicit-hot-start probes RES covering positive load at SoC=0.95, expecting residual renewable power to be reported as spare.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start probes RES covering positive load at SoC=0.95, expecting residual renewable power to be reported as spare. |
| initial_state | `LNGShipEMS.ResCoversCharge` |
| initial_vars | `{"PL": 50.0, "Ppv": 40.0, "Pw": 20.0, "SoC": 0.95}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `source_state_before_soc_boundary` | `0` | `[]` | `LNGShipEMS.ResCoversCharge` | `{}` |
| 1 `residual_res_becomes_spare` | `0` | `[]` | `LNGShipEMS.ResCoversSpare` | `{"Pbc_req": 0.0, "Pbd_req": 0.0, "Pg_req": 0.0, "cmd_DG1_cut_out": 1, "cmd_DG2_cut_out": 1, "cmd_LNG_cut_out": 1, "cmd_load_cut_in": 1, "cmd_load_cut_out": 0, "spare_power": 10.0}` |

</details>

<details><summary>`battery_only_soc_and_capacity_boundary` — explicit-hot-start probes suitable SoC at exactly 0.2 and deficit exactly equal to battery discharge capacity, expecting battery-only dispatch.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start probes suitable SoC at exactly 0.2 and deficit exactly equal to battery discharge capacity, expecting battery-only dispatch. |
| initial_state | `LNGShipEMS.ResCoversSpare` |
| initial_vars | `{"PL": 80.0, "Pbdismax": 50.0, "Ppv": 20.0, "Pw": 10.0, "SoC": 0.2}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `source_state_before_battery_priority` | `0` | `[]` | `LNGShipEMS.ResCoversSpare` | `{}` |
| 1 `battery_only_covers_deficit` | `0` | `[]` | `LNGShipEMS.BatteryOnly` | `{"Pbc_req": 0.0, "Pbd_req": 50.0, "Pg_req": 0.0, "cmd_DG1_cut_out": 1, "cmd_DG2_cut_out": 1, "cmd_LNG_cut_out": 1, "cmd_load_cut_in": 1, "cmd_load_cut_out": 0, "spare_power": 0.0}` |

</details>

<details><summary>`battery_lng_capacity_boundary` — explicit-hot-start probes deficit above battery capacity but exactly covered by battery plus LNG, expecting LNG cut-in and no diesel cut-in.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start probes deficit above battery capacity but exactly covered by battery plus LNG, expecting LNG cut-in and no diesel cut-in. |
| initial_state | `LNGShipEMS.BatteryOnly` |
| initial_vars | `{"PL": 110.0, "Pbdismax": 50.0, "Ppv": 20.0, "Pw": 10.0, "SoC": 0.5, "eng3_Pmax": 30.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `source_state_before_lng_priority` | `0` | `[]` | `LNGShipEMS.BatteryOnly` | `{}` |
| 1 `lng_added_after_battery` | `0` | `[]` | `LNGShipEMS.BatteryLng` | `{"Pbc_req": 0.0, "Pbd_req": 50.0, "Pg_req": 30.0, "cmd_DG1_cut_out": 1, "cmd_DG2_cut_out": 1, "cmd_LNG_cut_in": 1, "cmd_LNG_cut_out": 0, "cmd_load_cut_in": 1, "cmd_load_cut_out": 0, "spare_power": 0.0}` |

</details>

<details><summary>`battery_lng_dg1_capacity_boundary` — explicit-hot-start probes deficit above battery plus LNG but exactly covered after DG1, expecting DG1 cut-in while DG2 remains out.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start probes deficit above battery plus LNG but exactly covered after DG1, expecting DG1 cut-in while DG2 remains out. |
| initial_state | `LNGShipEMS.BatteryLng` |
| initial_vars | `{"PL": 140.0, "Pbdismax": 50.0, "Pd1max": 30.0, "Ppv": 20.0, "Pw": 10.0, "SoC": 0.5, "eng3_Pmax": 30.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `source_state_before_dg1_priority` | `0` | `[]` | `LNGShipEMS.BatteryLng` | `{}` |
| 1 `dg1_added_after_lng` | `0` | `[]` | `LNGShipEMS.BatteryLngDg1` | `{"Pbc_req": 0.0, "Pbd_req": 50.0, "Pg_req": 60.0, "cmd_DG1_cut_in": 1, "cmd_DG1_cut_out": 0, "cmd_DG2_cut_out": 1, "cmd_LNG_cut_in": 1, "cmd_LNG_cut_out": 0, "cmd_load_cut_in": 1, "cmd_load_cut_out": 0, "spare_power": 0.0}` |

</details>

<details><summary>`all_thermal_normal_soc_capacity_boundary` — explicit-hot-start probes normal-SoC deficit above battery plus LNG plus DG1 but exactly covered once DG2 is added.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start probes normal-SoC deficit above battery plus LNG plus DG1 but exactly covered once DG2 is added. |
| initial_state | `LNGShipEMS.BatteryLngDg1` |
| initial_vars | `{"PL": 170.0, "Pbdismax": 50.0, "Pd1max": 30.0, "Pd2max": 30.0, "Ppv": 20.0, "Pw": 10.0, "SoC": 0.5, "eng3_Pmax": 30.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `source_state_before_dg2_priority` | `0` | `[]` | `LNGShipEMS.BatteryLngDg1` | `{}` |
| 1 `all_thermal_units_active` | `0` | `[]` | `LNGShipEMS.AllThermalNormalSoc` | `{"Pbc_req": 0.0, "Pbd_req": 50.0, "Pg_req": 90.0, "cmd_DG1_cut_in": 1, "cmd_DG1_cut_out": 0, "cmd_DG2_cut_in": 1, "cmd_DG2_cut_out": 0, "cmd_LNG_cut_in": 1, "cmd_LNG_cut_out": 0, "cmd_load_cut_in": 1, "cmd_load_cut_out": 0, "spare_power": 0.0}` |

</details>

<details><summary>`low_soc_lng_charge_margin` — explicit-hot-start probes low SoC below 0.2 where LNG can cover load plus the Pgmax/5 charging margin.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start probes low SoC below 0.2 where LNG can cover load plus the Pgmax/5 charging margin. |
| initial_state | `LNGShipEMS.AllThermalNormalSoc` |
| initial_vars | `{"PL": 110.0, "Pgmax": 50.0, "Ppv": 20.0, "Pw": 10.0, "SoC": 0.19, "eng3_Pmax": 90.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `source_state_before_low_soc_lng_charge` | `0` | `[]` | `LNGShipEMS.AllThermalNormalSoc` | `{}` |
| 1 `lng_covers_load_and_pgmax_margin` | `0` | `[]` | `LNGShipEMS.LngChargeLowSoc` | `{"Pbc_req": 10.0, "Pbd_req": 0.0, "Pg_req": 90.0, "cmd_DG1_cut_out": 1, "cmd_DG2_cut_out": 1, "cmd_LNG_cut_in": 1, "cmd_LNG_cut_out": 0, "cmd_load_cut_in": 1, "cmd_load_cut_out": 0, "spare_power": 0.0}` |

</details>

<details><summary>`low_soc_lng_dg1_pd1_margin` — explicit-hot-start probes low SoC where LNG alone cannot cover the charging margin and DG1 is added using the Pd1max/10 margin.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start probes low SoC where LNG alone cannot cover the charging margin and DG1 is added using the Pd1max/10 margin. |
| initial_state | `LNGShipEMS.LngChargeLowSoc` |
| initial_vars | `{"PL": 130.0, "Pd1max": 20.0, "Pgmax": 50.0, "Ppv": 20.0, "Pw": 10.0, "SoC": 0.19, "eng3_Pmax": 90.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `source_state_before_low_soc_dg1` | `0` | `[]` | `LNGShipEMS.LngChargeLowSoc` | `{}` |
| 1 `lng_and_dg1_cover_pd1_margin` | `0` | `[]` | `LNGShipEMS.LngDg1ChargeLowSoc` | `{"Pbc_req": 2.0, "Pbd_req": 0.0, "Pg_req": 102.0, "cmd_DG1_cut_in": 1, "cmd_DG1_cut_out": 0, "cmd_DG2_cut_out": 1, "cmd_LNG_cut_in": 1, "cmd_LNG_cut_out": 0, "cmd_load_cut_in": 1, "cmd_load_cut_out": 0, "spare_power": 0.0}` |

</details>

<details><summary>`low_soc_lng_dg1_dg2_pd1_margin` — explicit-hot-start probes low SoC where DG2 is last-priority and needed to cover the Pd1max/10 charging-margin branch.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start probes low SoC where DG2 is last-priority and needed to cover the Pd1max/10 charging-margin branch. |
| initial_state | `LNGShipEMS.LngDg1ChargeLowSoc` |
| initial_vars | `{"PL": 155.0, "Pd1max": 20.0, "Pd2max": 20.0, "Pgmax": 50.0, "Ppv": 20.0, "Pw": 10.0, "SoC": 0.19, "eng3_Pmax": 90.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `source_state_before_low_soc_dg2` | `0` | `[]` | `LNGShipEMS.LngDg1ChargeLowSoc` | `{}` |
| 1 `dg2_added_for_low_soc_margin` | `0` | `[]` | `LNGShipEMS.LngDg1Dg2ChargeLowSoc` | `{"Pbc_req": 2.0, "Pbd_req": 0.0, "Pg_req": 127.0, "cmd_DG1_cut_in": 1, "cmd_DG1_cut_out": 0, "cmd_DG2_cut_in": 1, "cmd_DG2_cut_out": 0, "cmd_LNG_cut_in": 1, "cmd_LNG_cut_out": 0, "cmd_load_cut_in": 1, "cmd_load_cut_out": 0, "spare_power": 0.0}` |

</details>

<details><summary>`overload_illegal_all_thermal_and_battery_lack` — explicit-hot-start probes the admitted illegal overload-completion branch: extreme demand exceeds RES and thermal resources, so all thermal units are active and...<truncated 41 chars></summary>

| Field | Value |
|---|---|
| description | explicit-hot-start probes the admitted illegal overload-completion branch: extreme demand exceeds RES and thermal resources, so all thermal units are active and the remaining lack is battery discharge. |
| initial_state | `LNGShipEMS.LngDg1Dg2ChargeLowSoc` |
| initial_vars | `{"PL": 170.0, "Pbdismax": 50.0, "Pd1max": 30.0, "Pd2max": 20.0, "Ppv": 20.0, "Pw": 10.0, "SoC": 0.5, "eng3_Pmax": 30.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `source_state_before_illegal_overload` | `0` | `[]` | `LNGShipEMS.LngDg1Dg2ChargeLowSoc` | `{}` |
| 1 `illegal_overload_completion_outputs` | `0` | `[]` | `LNGShipEMS.OverloadCompletionIllegal` | `{"Pbc_req": 0.0, "Pbd_req": 60.0, "Pg_req": 80.0, "cmd_DG1_cut_in": 1, "cmd_DG1_cut_out": 0, "cmd_DG2_cut_in": 1, "cmd_DG2_cut_out": 0, "cmd_LNG_cut_in": 1, "cmd_LNG_cut_out": 0, "cmd_load_cut_in": 1, "cmd_load_cut_out": 0, "spare_power": 0.0}` |

</details>

<details><summary>`forced_zero_load_charge_from_thermal_leaf` — explicit-hot-start targets the wildcard forced reclassification rule: from an unrelated thermal leaf, PL=0 with RES and SoC below 0.95 must force ZeroLoadCharge...<truncated 36 chars></summary>

| Field | Value |
|---|---|
| description | explicit-hot-start targets the wildcard forced reclassification rule: from an unrelated thermal leaf, PL=0 with RES and SoC below 0.95 must force ZeroLoadCharge rather than remain in the old mode. |
| initial_state | `LNGShipEMS.AllThermalNormalSoc` |
| initial_vars | `{"PL": 0.0, "Pbdismax": 50.0, "Pd1max": 30.0, "Pd2max": 30.0, "Ppv": 5.0, "Pw": 15.0, "SoC": 0.5, "eng3_Pmax": 30.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `source_state_before_forced_zero_load_reclassification` | `0` | `[]` | `LNGShipEMS.AllThermalNormalSoc` | `{}` |
| 1 `forced_transition_to_zero_load_charge` | `0` | `[]` | `LNGShipEMS.ZeroLoadCharge` | `{"Pbc_req": 20.0, "Pbd_req": 0.0, "Pg_req": 0.0, "cmd_DG1_cut_in": 0, "cmd_DG1_cut_out": 1, "cmd_DG2_cut_in": 0, "cmd_DG2_cut_out": 1, "cmd_LNG_cut_in": 0, "cmd_LNG_cut_out": 1, "cmd_load_cut_in": 1, "cmd_load_cut_out": 0, "spare_power": 0.0}` |

</details>


### 7. Repair / blocking feedback 明细

口径：本节记录 agent-loop 真实进入 repair block 后的证据链：FixRequestBatch、SL-9 per-request accept/reject、candidate diff、local-check evidence、SL-10(NL+FixLog) 审阅，以及完整 FixLog ledger 摘录。

| Repair | iteration | accepted | source | blocking diagnostics | SL-9 decisions | SL-10 / local checks | candidate hash |
|---:|---:|---:|---|---|---|---|---|
| 1 | `0` | ✅ | `SD-4` | W_UNWRITTEN_READ_VAR:var_name=Pd2max, W_UNWRITTEN_READ_VAR:var_name=Pbdismax, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.BatteryOnly, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.BatteryLng, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.BatteryLngDg1, ... +74 | accept=12, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=none, rework=<none>; local ok=False, target=False, regression=False, drift=none, local_stage=SD-10, reason=design_target_unresolved | `sha256:a94551f062423d91b55b99075201100b6caf098b41ba33f7779df2d3ca5a111a` |
| 2 | `1` | ✅ | `SD-4` | W_UNWRITTEN_READ_VAR:var_name=Pd2max, W_UNWRITTEN_READ_VAR:var_name=Pbdismax, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.BatteryOnly, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.BatteryLng, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.BatteryLngDg1, ... +74 | accept=12, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=none, rework=<none>; local ok=True, target=True, regression=False, drift=none, local_stage=SD-10, reason= | `sha256:a94551f062423d91b55b99075201100b6caf098b41ba33f7779df2d3ca5a111a` |

<details><summary>Repair 1 / iteration `0` / source `SD-4` / accepted=✅</summary>

#### 为什么进入修复

- selected feedback source：`SD-4`；blocking=`True`；pre_scenario=`True`。
- problem_summary：Variable 'Pd2max' is read but never written by any action or transition effect.; Variable 'Pbdismax' is read but never written by any action or transition effect.; Transition guard reads only variables that are never changed by actions or effects.
- diagnostic ids：`W_UNWRITTEN_READ_VAR:var_name=Pd2max, W_UNWRITTEN_READ_VAR:var_name=Pbdismax, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.BatteryOnly, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.BatteryLng, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.BatteryLngDg1, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.AllThermalNormalSoc, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.LngDg1Dg2ChargeLowSoc, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.OverloadCompletionIllegal, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadSpare:to_path=LNGShipEMS.BatteryOnly, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadSpare:to_path=LNGShipEMS.BatteryLng, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadSpare:to_path=LNGShipEMS.BatteryLngDg1, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadSpare:to_path=LNGShipEMS.AllThermalNormalSoc, ... +67`。
- before_dsl_hash：`sha256:a94551f062423d91b55b99075201100b6caf098b41ba33f7779df2d3ca5a111a`；candidate_dsl_hash：`sha256:a94551f062423d91b55b99075201100b6caf098b41ba33f7779df2d3ca5a111a`。

#### 错误证据 / diagnostics

- 1. `W_UNWRITTEN_READ_VAR` `W_UNWRITTEN_READ_VAR:var_name=Pd2max` policy=`budgeted_repair`：Variable 'Pd2max' is read but never written by any action or transition effect.；refs=`{"init_value": "0.0", "read_states": ["LNGShipEMS.AllThermalNormalSoc", "LNGShipEMS.BatteryLng", "LNGShipEMS.BatteryLngDg1", "LNGShipEMS.BatteryOnly", "LNGShipEMS.LngChargeLowSoc", "LNGShipEMS.LngDg1ChargeLowSoc", "LNGShipEMS.LngDg1Dg2ChargeLowSoc", "LNGShipEMS.OverloadCompletionIllegal", "LNGShipEM...<truncated 128 chars>`
- 2. `W_UNWRITTEN_READ_VAR` `W_UNWRITTEN_READ_VAR:var_name=Pbdismax` policy=`budgeted_repair`：Variable 'Pbdismax' is read but never written by any action or transition effect.；refs=`{"init_value": "0.0", "read_states": ["LNGShipEMS.AllThermalNormalSoc", "LNGShipEMS.BatteryLng", "LNGShipEMS.BatteryLngDg1", "LNGShipEMS.BatteryOnly", "LNGShipEMS.LngChargeLowSoc", "LNGShipEMS.LngDg1ChargeLowSoc", "LNGShipEMS.LngDg1Dg2ChargeLowSoc", "LNGShipEMS.OverloadCompletionIllegal", "LNGShipEM...<truncated 130 chars>`
- 3. `W_GUARD_VARS_NEVER_CHANGE` `W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.BatteryOnly` policy=`budgeted_repair`：Transition guard reads only variables that are never changed by actions or effects.；refs=`{"from_path": "LNGShipEMS.ZeroLoadCharge", "guard_vars": ["PL", "Pbdismax", "Ppv", "Pw", "SoC"], "to_path": "LNGShipEMS.BatteryOnly"}`
- 4. `W_GUARD_VARS_NEVER_CHANGE` `W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.BatteryLng` policy=`budgeted_repair`：Transition guard reads only variables that are never changed by actions or effects.；refs=`{"from_path": "LNGShipEMS.ZeroLoadCharge", "guard_vars": ["PL", "Pbdismax", "Ppv", "Pw", "SoC", "eng3_Pmax"], "to_path": "LNGShipEMS.BatteryLng"}`
- 5. `W_GUARD_VARS_NEVER_CHANGE` `W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.BatteryLngDg1` policy=`budgeted_repair`：Transition guard reads only variables that are never changed by actions or effects.；refs=`{"from_path": "LNGShipEMS.ZeroLoadCharge", "guard_vars": ["PL", "Pbdismax", "Pd1max", "Ppv", "Pw", "SoC", "eng3_Pmax"], "to_path": "LNGShipEMS.BatteryLngDg1"}`
- 6. `W_GUARD_VARS_NEVER_CHANGE` `W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.AllThermalNormalSoc` policy=`budgeted_repair`：Transition guard reads only variables that are never changed by actions or effects.；refs=`{"from_path": "LNGShipEMS.ZeroLoadCharge", "guard_vars": ["PL", "Pbdismax", "Pd1max", "Pd2max", "Ppv", "Pw", "SoC", "eng3_Pmax"], "to_path": "LNGShipEMS.AllThermalNormalSoc"}`
- 7. `W_GUARD_VARS_NEVER_CHANGE` `W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.LngDg1Dg2ChargeLowSoc` policy=`budgeted_repair`：Transition guard reads only variables that are never changed by actions or effects.；refs=`{"from_path": "LNGShipEMS.ZeroLoadCharge", "guard_vars": ["PL", "Pd1max", "Pd2max", "Ppv", "Pw", "SoC", "eng3_Pmax"], "to_path": "LNGShipEMS.LngDg1Dg2ChargeLowSoc"}`
- 8. `W_GUARD_VARS_NEVER_CHANGE` `W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.OverloadCompletionIllegal` policy=`budgeted_repair`：Transition guard reads only variables that are never changed by actions or effects.；refs=`{"from_path": "LNGShipEMS.ZeroLoadCharge", "guard_vars": ["PL", "Pbdismax", "Pd1max", "Pd2max", "Ppv", "Pw", "SoC", "eng3_Pmax"], "to_path": "LNGShipEMS.OverloadCompletionIllegal"}`
- ……另有 `66` 条 evidence 见 run record。

#### 变量角色与上下文提示

- policy：Advisory only. Do not invent writes for external_input_candidate variables unless NL explicitly gives update semantics; add meaningful NL-grounded writes only for internal state variables.
- source：SD-4 diagnostic refs and generic NL external-input rationale

| Variable | role_hint | nl_token_present | diagnostics |
|---|---|---:|---|
| `PL` | `external_input_candidate` | ✅ | `W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +140` |
| `Pbc_req` | `unknown` | ❌ | `W_DURING_CONST_ASSIGN, W_DURING_CONST_ASSIGN, W_DURING_CONST_ASSIGN, W_DURING_CONST_ASSIGN, W_DURING_CONST_ASSIGN, ... +4` |
| `Pbd_req` | `unknown` | ❌ | `W_DURING_CONST_ASSIGN, W_DURING_CONST_ASSIGN, W_DURING_CONST_ASSIGN, W_DURING_CONST_ASSIGN, W_DURING_CONST_ASSIGN, ... +4` |
| `Pbdismax` | `unknown` | ❌ | `W_UNWRITTEN_READ_VAR, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +56` |
| `Pd1max` | `external_input_candidate` | ✅ | `W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +56` |
| `Pd2max` | `unknown` | ❌ | `W_UNWRITTEN_READ_VAR, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +32` |
| `Pg_req` | `unknown` | ❌ | `W_DURING_CONST_ASSIGN, W_DURING_CONST_ASSIGN, W_DURING_CONST_ASSIGN, W_DURING_CONST_ASSIGN, W_DURING_CONST_ASSIGN, ... +2` |
| `Pgmax` | `external_input_candidate` | ✅ | `W_UNWRITTEN_READ_VAR, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +20` |
| `Ppv` | `external_input_candidate` | ✅ | `W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +140` |
| `Pw` | `external_input_candidate` | ✅ | `W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +140` |
| `SoC` | `external_input_candidate` | ✅ | `W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +140` |
| `cmd_DG1_cut_in` | `unknown` | ❌ | `W_DURING_CONST_ASSIGN, W_DURING_CONST_ASSIGN, W_DURING_CONST_ASSIGN, W_DURING_CONST_ASSIGN, W_DURING_CONST_ASSIGN, ... +9` |
| `cmd_DG1_cut_out` | `unknown` | ❌ | `W_DURING_CONST_ASSIGN, W_DURING_CONST_ASSIGN, W_DURING_CONST_ASSIGN, W_DURING_CONST_ASSIGN, W_DURING_CONST_ASSIGN, ... +9` |
| `cmd_DG2_cut_in` | `unknown` | ❌ | `W_DURING_CONST_ASSIGN, W_DURING_CONST_ASSIGN, W_DURING_CONST_ASSIGN, W_DURING_CONST_ASSIGN, W_DURING_CONST_ASSIGN, ... +9` |
| `cmd_DG2_cut_out` | `unknown` | ❌ | `W_DURING_CONST_ASSIGN, W_DURING_CONST_ASSIGN, W_DURING_CONST_ASSIGN, W_DURING_CONST_ASSIGN, W_DURING_CONST_ASSIGN, ... +9` |
| `cmd_LNG_cut_in` | `unknown` | ❌ | `W_DURING_CONST_ASSIGN, W_DURING_CONST_ASSIGN, W_DURING_CONST_ASSIGN, W_DURING_CONST_ASSIGN, W_DURING_CONST_ASSIGN, ... +9` |
| `cmd_LNG_cut_out` | `unknown` | ❌ | `W_DURING_CONST_ASSIGN, W_DURING_CONST_ASSIGN, W_DURING_CONST_ASSIGN, W_DURING_CONST_ASSIGN, W_DURING_CONST_ASSIGN, ... +9` |
| `cmd_load_cut_in` | `unknown` | ❌ | `W_DURING_CONST_ASSIGN, W_DURING_CONST_ASSIGN, W_DURING_CONST_ASSIGN, W_DURING_CONST_ASSIGN, W_DURING_CONST_ASSIGN, ... +9` |
| `cmd_load_cut_out` | `unknown` | ❌ | `W_DURING_CONST_ASSIGN, W_DURING_CONST_ASSIGN, W_DURING_CONST_ASSIGN, W_DURING_CONST_ASSIGN, W_DURING_CONST_ASSIGN, ... +9` |
| `eng3_Pmax` | `external_input_candidate` | ✅ | `W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +80` |
| `spare_power` | `unknown` | ❌ | `W_DURING_CONST_ASSIGN, W_DURING_CONST_ASSIGN, W_DURING_CONST_ASSIGN, W_DURING_CONST_ASSIGN, W_DURING_CONST_ASSIGN, ... +7` |

#### SD-8 FixRequestBatch / 修改请求

- batch_id：`fixbatch-0-sha256-002b698f3f7`；source_stage=`SD-4`；legacy_plan_kind=`FixPlan`；requests=`12`。

| request_id | severity | hard | waiver | problem | evidence |
|---|---|---:|---:|---|---|
| `fixreq-0-sd4-0-004a2744db` | `blocking_warning` | ❌ | ✅ | Variable 'Pd2max' is read but never written by any action or transition effect.; Variable 'Pbdismax' is read but never written by any action or transition effect.; Transition guard reads only variables that are never cha...<truncated 27 chars> | `W_UNWRITTEN_READ_VAR` |
| `fixreq-0-sd4-1-ac19caf402` | `blocking_warning` | ❌ | ✅ | Variable 'Pd2max' is read but never written by any action or transition effect.; Variable 'Pbdismax' is read but never written by any action or transition effect.; Transition guard reads only variables that are never cha...<truncated 27 chars> | `W_UNWRITTEN_READ_VAR` |
| `fixreq-0-sd4-2-a85904e5ae` | `blocking_warning` | ❌ | ✅ | Variable 'Pd2max' is read but never written by any action or transition effect.; Variable 'Pbdismax' is read but never written by any action or transition effect.; Transition guard reads only variables that are never cha...<truncated 27 chars> | `W_GUARD_VARS_NEVER_CHANGE` |
| `fixreq-0-sd4-3-63111cf4c5` | `blocking_warning` | ❌ | ✅ | Variable 'Pd2max' is read but never written by any action or transition effect.; Variable 'Pbdismax' is read but never written by any action or transition effect.; Transition guard reads only variables that are never cha...<truncated 27 chars> | `W_GUARD_VARS_NEVER_CHANGE` |
| `fixreq-0-sd4-4-1c37eb99a0` | `blocking_warning` | ❌ | ✅ | Variable 'Pd2max' is read but never written by any action or transition effect.; Variable 'Pbdismax' is read but never written by any action or transition effect.; Transition guard reads only variables that are never cha...<truncated 27 chars> | `W_GUARD_VARS_NEVER_CHANGE` |
| `fixreq-0-sd4-5-684ca59bf4` | `blocking_warning` | ❌ | ✅ | Variable 'Pd2max' is read but never written by any action or transition effect.; Variable 'Pbdismax' is read but never written by any action or transition effect.; Transition guard reads only variables that are never cha...<truncated 27 chars> | `W_GUARD_VARS_NEVER_CHANGE` |
| `fixreq-0-sd4-6-53b0ac9354` | `blocking_warning` | ❌ | ✅ | Variable 'Pd2max' is read but never written by any action or transition effect.; Variable 'Pbdismax' is read but never written by any action or transition effect.; Transition guard reads only variables that are never cha...<truncated 27 chars> | `W_GUARD_VARS_NEVER_CHANGE` |
| `fixreq-0-sd4-7-7996b67982` | `blocking_warning` | ❌ | ✅ | Variable 'Pd2max' is read but never written by any action or transition effect.; Variable 'Pbdismax' is read but never written by any action or transition effect.; Transition guard reads only variables that are never cha...<truncated 27 chars> | `W_GUARD_VARS_NEVER_CHANGE` |
| `fixreq-0-sd4-8-eb7c8ae12b` | `blocking_warning` | ❌ | ✅ | Variable 'Pd2max' is read but never written by any action or transition effect.; Variable 'Pbdismax' is read but never written by any action or transition effect.; Transition guard reads only variables that are never cha...<truncated 27 chars> | `W_GUARD_VARS_NEVER_CHANGE` |
| `fixreq-0-sd4-9-3c1a198645` | `blocking_warning` | ❌ | ✅ | Variable 'Pd2max' is read but never written by any action or transition effect.; Variable 'Pbdismax' is read but never written by any action or transition effect.; Transition guard reads only variables that are never cha...<truncated 27 chars> | `W_GUARD_VARS_NEVER_CHANGE` |
- ……另有 `2` 个 request 见 run record。

#### SD-8 legacy fix plan / 修改建议

- recommended_strategy：Use diagnostics as hints; choose the smallest globally consistent repair.；Before returning a candidate, verify every required_preserve_element_id still has a concrete DSL representation.
- hint 1：The variable is used as input but never updated after its initial definition, so model behavior may be accidentally constant.；`actions=add_write, simplify_guard；do_not=Do not add a meaningless self-assignment.`
- hint 2：The variable is used as input but never updated after its initial definition, so model behavior may be accidentally constant.；`actions=add_write, simplify_guard；do_not=Do not add a meaningless self-assignment.`
- hint 3：This guard is controlled only by initial variable values. If those values never change, the transition condition is effectively fixed.；`actions=add_write, simplify_guard；do_not=Do not add a meaningless self-assignment; it does not model a real change., Do not rewrite the guard to a meaningless constant only to silence this diagnostic.`
- hint 4：This guard is controlled only by initial variable values. If those values never change, the transition condition is effectively fixed.；`actions=add_write, simplify_guard；do_not=Do not add a meaningless self-assignment; it does not model a real change., Do not rewrite the guard to a meaningless constant only to silence this diagnostic.`
- hint 5：This guard is controlled only by initial variable values. If those values never change, the transition condition is effectively fixed.；`actions=add_write, simplify_guard；do_not=Do not add a meaningless self-assignment; it does not model a real change., Do not rewrite the guard to a meaningless constant only to silence this diagnostic.`
- hint 6：This guard is controlled only by initial variable values. If those values never change, the transition condition is effectively fixed.；`actions=add_write, simplify_guard；do_not=Do not add a meaningless self-assignment; it does not model a real change., Do not rewrite the guard to a meaningless constant only to silence this diagnostic.`
- forbidden_edits：`Do not delete grounded required elements merely to silence diagnostics., Do not invent internal plant/environment dynamics merely to make external input variables appear written.`。
- required_preserve_element_ids：`state:ZeroLoadCharge, state:ZeroLoadSpare, state:ResCoversCharge, state:ResCoversSpare, state:BatteryOnly, state:BatteryLng, state:BatteryLngDg1, state:AllThermalNormalSoc, state:LngChargeLowSoc, state:LngDg1ChargeLowSoc, state:LngDg1Dg2ChargeLowSoc, state:OverloadCompletionIllegal, ... +19`。

#### SL-9 per-request 决策

- accepted_request_ids：`<derived-from-table>`；candidate_len=`7711`。

| request_id | decision | waiver | rework_locked | rationale / intent |
|---|---|---:|---:|---|
| `fixreq-0-sd4-0-004a2744db` | `accept` | ❌ | ❌ | Pd2max is an external DG2 capacity bound used to classify dispatch branches. The NL says the FSM reads capacity bounds/resources; it does not define EMS-internal dynamics that update DG2 capacity. A DSL write would be a meaningless self-assignment or invented plant dynamics, so the safe repair is conservative preservation with explicit grounding rationale.；i...<truncated 99 chars> |
| `fixreq-0-sd4-1-ac19caf402` | `accept` | ❌ | ❌ | Pbdismax is an external battery-discharge capacity bound needed by the NL priority logic. The NL does not specify EMS-internal update semantics for this bound. Adding a write would be ungrounded, so the safe repair is conservative preservation with explicit grounding rationale.；intent=Preserve Pbdismax as an external input/read-only capacity bound; do not in...<truncated 21 chars> |
| `fixreq-0-sd4-2-a85904e5ae` | `accept` | ❌ | ❌ | The BatteryOnly selection guard reads PL, Ppv, Pw, SoC, and Pbdismax, all of which are external demand/resource/battery-condition inputs in the NL. The guard is the required logical state selector and should not be simplified or replaced by invented updates.；intent=Preserve BatteryOnly guard as an external-input logical selector. |
| `fixreq-0-sd4-3-63111cf4c5` | `accept` | ❌ | ❌ | The BatteryLng guard encodes the NL priority of RES, suitable battery discharge, then LNG before diesel using external inputs and capacity bounds. No NL-grounded internal writes exist for these inputs.；intent=Preserve BatteryLng guard as an external-input logical selector. |
| `fixreq-0-sd4-4-1c37eb99a0` | `accept` | ❌ | ❌ | The BatteryLngDg1 guard is required to represent the later priority branch where DG1 is used after battery and LNG capacity are insufficient. Its variables are external inputs/capacity bounds, so adding writes would be ungrounded.；intent=Preserve BatteryLngDg1 guard as an external-input logical selector. |
| `fixreq-0-sd4-5-684ca59bf4` | `accept` | ❌ | ❌ | The AllThermalNormalSoc guard uses external demand, renewable, battery, and thermal-capacity values to select the all-thermal normal-SoC branch. This is a required NL branch and should remain condition-driven.；intent=Preserve AllThermalNormalSoc guard as an external-input logical selector. |
| `fixreq-0-sd4-6-53b0ac9354` | `accept` | ❌ | ❌ | The LngDg1Dg2ChargeLowSoc guard represents the NL low-SoC diesel-generator case with Pd1max/10 charging margin and DG2 last priority. The read variables are external conditions/capacity bounds; internal writes would invent dynamics.；intent=Preserve LngDg1Dg2ChargeLowSoc guard as an external-input logical selector. |
| `fixreq-0-sd4-7-7996b67982` | `accept` | ❌ | ❌ | The OverloadCompletionIllegal guard is required by the NL to represent the illegal overload-completion branch where all thermal units are active and remaining lack is covered by battery discharge. Its inputs are external operating conditions/capacity bounds.；intent=Preserve OverloadCompletionIllegal guard as an external-input logical selector. |
| `fixreq-0-sd4-8-eb7c8ae12b` | `accept` | ❌ | ❌ | The ZeroLoadSpare-to-BatteryOnly expanded forced guard warning is another instance of the same external-input classifier. PL/Ppv/Pw/SoC/Pbdismax are read from the environment/resources and are not EMS-internal state variables.；intent=Preserve forced transition expansion behavior and external-input guard. |
| `fixreq-0-sd4-9-3c1a198645` | `accept` | ❌ | ❌ | The ZeroLoadSpare-to-BatteryLng expanded guard is NL-grounded dispatch selection over external demand/resource/capacity inputs. Adding writes would be meaningless and forbidden by the request guidance.；intent=Preserve forced transition expansion behavior and external-input guard. |
| `fixreq-0-sd4-10-7e80c093d6` | `accept` | ❌ | ❌ | The ZeroLoadSpare-to-BatteryLngDg1 expanded guard represents a required priority branch selected by current external operating conditions. No safe DSL edit exists that would make these inputs internally written without violating the NL.；intent=Preserve forced transition expansion behavior and external-input guard. |
| `fixreq-0-sd4-11-2b935a4955` | `accept` | ❌ | ❌ | The ZeroLoadSpare-to-AllThermalNormalSoc expanded guard is a required all-thermal branch selected by external load/resource/capacity values. It should remain guarded by those inputs.；intent=Preserve forced transition expansion behavior and external-input guard. |
- repair_rationale：No textual DSL edit is the smallest safe repair. The selected diagnostics are W_UNWRITTEN_READ_VAR and W_GUARD_VARS_NEVER_CHANGE on variables that the NL defines as read inputs: PL, Ppv, Pw, SoC, engine/generator capacity bounds, and batter...<truncated 21 chars>；The NL requires the twelve states to be selected by logical transition conditions over demand, generation, capacity, and SoC. Replacing those guards with constants or removing them would delete required behavior.；Adding writes to Pd2max, Pbdismax, PL, Ppv, Pw, SoC, eng3_Pmax, or Pd1max would invent plant/environment dynamics that the NL does not provide and is specifically forbidden by the repair request guidance.；All required preserved states, variables, and key selection transitions remain represented. The model remains a guarded condition-classifier EMS over externally supplied operating conditions and writes only EMS outputs/commands.
- diff_summary：`{"summary": "No DSL text changed. The repair is a conservative design-level acceptance/grounding response: preserve external-input guards and read-only capacity bounds rather than adding ungrounded writes or deleting required twelve-state dispatch logic."}`。

#### SL-9 candidate / 最终修改执行方案

```pyfcstm
def float PL = 0.0;
def float Ppv = 0.0;
def float Pw = 0.0;
def float SoC = 0.5;
def float eng3_Pmax = 0.0;
def float Pd1max = 0.0;
def float Pd2max = 0.0;
def float Pbdismax = 0.0;
def float Pgmax = 0.0;
def float Pg_req = 0.0;
def float Pbd_req = 0.0;
def float Pbc_req = 0.0;
def float spare_power = 0.0;
def int cmd_LNG_cut_in = 0;
def int cmd_LNG_cut_out = 1;
def int cmd_DG1_cut_in = 0;
def int cmd_DG1_cut_out = 1;
def int cmd_DG2_cut_in = 0;
def int cmd_DG2_cut_out = 1;
def int cmd_load_cut_in = 1;
def int cmd_load_cut_out = 0;

state LNGShipEMS {
    ! * -> ZeroLoadCharge : if [PL == 0.0 && Ppv + Pw > 0.0 && SoC < 0.95];
    ! * -> ZeroLoadSpare : if [PL == 0.0 && Ppv + Pw > 0.0 && SoC >= 0.95];
    ! * -> ResCoversCharge : if [PL > 0.0 && Ppv + Pw >= PL && SoC < 0.95];
    ! * -> ResCoversSpare : if [PL > 0.0 && Ppv + Pw >= PL && SoC >= 0.95];
    ! * -> BatteryOnly : if [PL > 0.0 && Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw <= Pbdismax];
    ! * -> BatteryLng : if [PL > 0.0 && Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw > Pbdismax && PL - Ppv - Pw <= Pbdismax + eng3_Pmax];
    ! * -> BatteryLngDg1 : if [PL > 0.0 && Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw > Pbdismax + eng3_Pmax && PL - Ppv - Pw <= Pbdismax + eng3_Pmax + Pd1max];
    ! * -> AllThermalNormalSoc : if [PL > 0.0 && Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw > Pbdismax + eng3_Pmax + Pd1max && PL - Ppv - Pw <= Pbdismax + eng3_Pmax + Pd1max + Pd2max];
    ! * -> LngChargeLowSoc : if [PL > 0.0 && Ppv + Pw < PL && SoC < 0.2 && PL - Ppv - Pw + Pgmax / 5.0 <= eng3_Pmax];
    ! * -> LngDg1ChargeLowSoc : if [PL > 0.0 && Ppv + Pw < PL && SoC < 0.2 && PL - Ppv - Pw + Pgmax / 5.0 > eng3_Pmax && PL - Ppv - Pw + Pd1max / 10.0 <= eng3_Pmax + Pd1max];
    ! * -> LngDg1Dg2ChargeLowSoc : if [PL > 0.0 && Ppv + Pw < PL && SoC < 0.2 && PL - Ppv - Pw + Pd1max / 10.0 > eng3_Pmax + Pd1max && PL - Ppv - Pw + Pd1max / 10.0 <= eng3_Pmax + Pd1max + Pd2max];
    ! * -> OverloadCompletionIllegal : if [PL > 0.0 && Ppv + Pw < PL && ((SoC >= 0.2 && PL - Ppv - Pw > Pbdismax + eng3_Pmax + Pd1max + Pd2max) || (SoC < 0.2 && PL - Ppv - Pw + Pd1max / 10.0 > eng3_Pmax + Pd1max + Pd2max))];

    [*] -> ZeroLoadCharge;

    state ZeroLoadCharge {
        during {
            Pg_req = 0.0;
            Pbd_req = 0.0;
            Pbc_req = Ppv + Pw;
            spare_power = 0.0;
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

    state ZeroLoadSpare {
        during {
            Pg_req = 0.0;
            Pbd_req = 0.0;
            Pbc_req = 0.0;
            spare_power = Ppv + Pw;
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

    state ResCoversCharge {
        during {
            Pg_req = 0.0;
            Pbd_req = 0.0;
            Pbc_req = Ppv + Pw - PL;
            spare_power = 0.0;
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

    state ResCoversSpare {
        during {
            Pg_req = 0.0;
            Pbd_req = 0.0;
            Pbc_req = 0.0;
            spare_power = Ppv + Pw - PL;
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

    state BatteryOnly {
        during {
            Pg_req = 0.0;
            Pbd_req = PL - Ppv - Pw;
            Pbc_req = 0.0;
            spare_power = 0.0;
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

    state BatteryLng {
        during {
            Pg_req = PL - Ppv - Pw - Pbdismax;
            Pbd_req = Pbdismax;
            Pbc_req = 0.0;
            spare_power = 0.0;
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

    state BatteryLngDg1 {
        during {
            Pg_req = PL - Ppv - Pw - Pbdismax;
            Pbd_req = Pbdismax;
            Pbc_req = 0.0;
            spare_power = 0.0;
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

    state AllThermalNormalSoc {
        during {
            Pg_req = PL - Ppv - Pw - Pbdismax;
            Pbd_req = Pbdismax;
            Pbc_req = 0.0;
            spare_power = 0.0;
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

    state LngChargeLowSoc {
        during {
            Pg_req = PL - Ppv - Pw + Pgmax / 5.0;
            Pbd_req = 0.0;
            Pbc_req = Pgmax / 5.0;
            spare_power = 0.0;
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

    state LngDg1ChargeLowSoc {
        during {
            Pg_req = PL - Ppv - Pw + Pd1max / 10.0;
            Pbd_req = 0.0;
            Pbc_req = Pd1max / 10.0;
            spare_power = 0.0;
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

    state LngDg1Dg2ChargeLowSoc {
        during {
            Pg_req = PL - Ppv - Pw + Pd1max / 10.0;
            Pbd_req = 0.0;
            Pbc_req = Pd1max / 10.0;
            spare_power = 0.0;
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

    state OverloadCompletionIllegal {
        during {
            Pg_req = eng3_Pmax + Pd1max + Pd2max;
            Pbd_req = PL - Ppv - Pw - eng3_Pmax - Pd1max - Pd2max;
            Pbc_req = 0.0;
            spare_power = 0.0;
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

- SL-10 decision=`pass`，ok=`True`，target_resolved=`True`，regression_detected=`False`，drift_risk=`none`。
- SL-10 review_meta：schema=`SL10RepairReviewOutput.v1`，failure_policy=`fail_closed`，replay_key=`SL-10:sha256:050cf8abaed8e3fad8c74e903d0f355751ba310a8ff9223574165b674bd7e03f`。
  - SL-10 evidence 1: `{"summary": "The NL defines this EMS as a condition-classification FSM that reads external load demand PL, renewable inputs Ppv and Pw, SoC, and engine/generator capacity bounds, then selects one of twelve logical dispatch states. The candidate preserves all twelve required states, the required variables, the required forced selection guards, and the required dispatch actions/commands."}`
  - SL-10 evidence 2: `{"summary": "The complete FixLog shows SL-9 accepted all 12 design requests by preserving the existing DSL, with the repeated rationale that Pd2max, Pbdismax, PL, Ppv, Pw, SoC, eng3_Pmax, Pd1max, and related quantities are external operating-condition or capacity inputs. The request guidance itself forbade inventing internal plant/environment dynamics merely to make external input variables appear written."}`
  - SL-10 evidence 3: `{"summary": "The DSL diff is intentionally empty. That is acceptable here because the diagnostics are non-hard, waiver-allowed design warnings, and textual edits such as self-assignments, constant guard simplification, or deleting guards would reduce NL fidelity by damaging the required twelve-state logical selector behavior."}`
  - SL-10 evidence 4: `{"summary": "No regression is indicated: local evidence reports regression_detected=false and drift_risk=none, and there are no scenario failures in the pre-scenario summary. The candidate also retains the overload illegal state behavior, low-SoC charging margins Pgmax/5 and Pd1max/10, RES charging/spare behavior, battery/LNG/DG priority branches, and cut-in/cut-out command assignments."}`
- local checks evidence：stage=`SD-10`；note=PR-E1 uses local parse/semantic/design/sim checks as SL-10 evidence, not as the final deterministic judge.。
  - local ok=`False`，target_resolved=`False`，regression_detected=`False`，drift_risk=`none`。
  - local_rejection：reason=`design_target_unresolved`，rejected_by_stage=`SD-10`。
    - local evidence 1: `design_target_unresolved` {"items": [{"budget_exhausted": false, "budget_remaining": 1, "code": "W_UNWRITTEN_READ_VAR", "instance_key": "W_UNWRITTEN_READ_VAR:var_name=Pd2max", "message": "Variable 'Pd2max' is read but never written by any action or transition effect.", "policy_action": "budgeted_repair", "pyfcstm_severity": "warning", "rationale": "", "refs": {"init_value": "0.0", "read_states": ["LNGShipEMS.AllThermalNormalSoc", "LNGShipEMS.BatteryLng", "LNGShipEMS.BatteryLngDg1", "LNGShipEMS.BatteryOnly", "LNGShipEMS.L...<truncated 91271 chars>

</details>

<details><summary>Repair 2 / iteration `1` / source `SD-4` / accepted=✅</summary>

#### 为什么进入修复

- selected feedback source：`SD-4`；blocking=`True`；pre_scenario=`True`。
- problem_summary：Variable 'Pd2max' is read but never written by any action or transition effect.; Variable 'Pbdismax' is read but never written by any action or transition effect.; Transition guard reads only variables that are never changed by actions or effects.
- diagnostic ids：`W_UNWRITTEN_READ_VAR:var_name=Pd2max, W_UNWRITTEN_READ_VAR:var_name=Pbdismax, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.BatteryOnly, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.BatteryLng, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.BatteryLngDg1, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.AllThermalNormalSoc, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.LngDg1Dg2ChargeLowSoc, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.OverloadCompletionIllegal, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadSpare:to_path=LNGShipEMS.BatteryOnly, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadSpare:to_path=LNGShipEMS.BatteryLng, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadSpare:to_path=LNGShipEMS.BatteryLngDg1, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadSpare:to_path=LNGShipEMS.AllThermalNormalSoc, ... +67`。
- before_dsl_hash：`sha256:a94551f062423d91b55b99075201100b6caf098b41ba33f7779df2d3ca5a111a`；candidate_dsl_hash：`sha256:a94551f062423d91b55b99075201100b6caf098b41ba33f7779df2d3ca5a111a`。

#### 错误证据 / diagnostics

- 1. `W_UNWRITTEN_READ_VAR` `W_UNWRITTEN_READ_VAR:var_name=Pd2max` policy=`budgeted_repair`：Variable 'Pd2max' is read but never written by any action or transition effect.；refs=`{"init_value": "0.0", "read_states": ["LNGShipEMS.AllThermalNormalSoc", "LNGShipEMS.BatteryLng", "LNGShipEMS.BatteryLngDg1", "LNGShipEMS.BatteryOnly", "LNGShipEMS.LngChargeLowSoc", "LNGShipEMS.LngDg1ChargeLowSoc", "LNGShipEMS.LngDg1Dg2ChargeLowSoc", "LNGShipEMS.OverloadCompletionIllegal", "LNGShipEM...<truncated 128 chars>`
- 2. `W_UNWRITTEN_READ_VAR` `W_UNWRITTEN_READ_VAR:var_name=Pbdismax` policy=`budgeted_repair`：Variable 'Pbdismax' is read but never written by any action or transition effect.；refs=`{"init_value": "0.0", "read_states": ["LNGShipEMS.AllThermalNormalSoc", "LNGShipEMS.BatteryLng", "LNGShipEMS.BatteryLngDg1", "LNGShipEMS.BatteryOnly", "LNGShipEMS.LngChargeLowSoc", "LNGShipEMS.LngDg1ChargeLowSoc", "LNGShipEMS.LngDg1Dg2ChargeLowSoc", "LNGShipEMS.OverloadCompletionIllegal", "LNGShipEM...<truncated 130 chars>`
- 3. `W_GUARD_VARS_NEVER_CHANGE` `W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.BatteryOnly` policy=`budgeted_repair`：Transition guard reads only variables that are never changed by actions or effects.；refs=`{"from_path": "LNGShipEMS.ZeroLoadCharge", "guard_vars": ["PL", "Pbdismax", "Ppv", "Pw", "SoC"], "to_path": "LNGShipEMS.BatteryOnly"}`
- 4. `W_GUARD_VARS_NEVER_CHANGE` `W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.BatteryLng` policy=`budgeted_repair`：Transition guard reads only variables that are never changed by actions or effects.；refs=`{"from_path": "LNGShipEMS.ZeroLoadCharge", "guard_vars": ["PL", "Pbdismax", "Ppv", "Pw", "SoC", "eng3_Pmax"], "to_path": "LNGShipEMS.BatteryLng"}`
- 5. `W_GUARD_VARS_NEVER_CHANGE` `W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.BatteryLngDg1` policy=`budgeted_repair`：Transition guard reads only variables that are never changed by actions or effects.；refs=`{"from_path": "LNGShipEMS.ZeroLoadCharge", "guard_vars": ["PL", "Pbdismax", "Pd1max", "Ppv", "Pw", "SoC", "eng3_Pmax"], "to_path": "LNGShipEMS.BatteryLngDg1"}`
- 6. `W_GUARD_VARS_NEVER_CHANGE` `W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.AllThermalNormalSoc` policy=`budgeted_repair`：Transition guard reads only variables that are never changed by actions or effects.；refs=`{"from_path": "LNGShipEMS.ZeroLoadCharge", "guard_vars": ["PL", "Pbdismax", "Pd1max", "Pd2max", "Ppv", "Pw", "SoC", "eng3_Pmax"], "to_path": "LNGShipEMS.AllThermalNormalSoc"}`
- 7. `W_GUARD_VARS_NEVER_CHANGE` `W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.LngDg1Dg2ChargeLowSoc` policy=`budgeted_repair`：Transition guard reads only variables that are never changed by actions or effects.；refs=`{"from_path": "LNGShipEMS.ZeroLoadCharge", "guard_vars": ["PL", "Pd1max", "Pd2max", "Ppv", "Pw", "SoC", "eng3_Pmax"], "to_path": "LNGShipEMS.LngDg1Dg2ChargeLowSoc"}`
- 8. `W_GUARD_VARS_NEVER_CHANGE` `W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.OverloadCompletionIllegal` policy=`budgeted_repair`：Transition guard reads only variables that are never changed by actions or effects.；refs=`{"from_path": "LNGShipEMS.ZeroLoadCharge", "guard_vars": ["PL", "Pbdismax", "Pd1max", "Pd2max", "Ppv", "Pw", "SoC", "eng3_Pmax"], "to_path": "LNGShipEMS.OverloadCompletionIllegal"}`
- ……另有 `66` 条 evidence 见 run record。

#### 变量角色与上下文提示

- policy：Advisory only. Do not invent writes for external_input_candidate variables unless NL explicitly gives update semantics; add meaningful NL-grounded writes only for internal state variables.
- source：SD-4 diagnostic refs and generic NL external-input rationale

| Variable | role_hint | nl_token_present | diagnostics |
|---|---|---:|---|
| `PL` | `external_input_candidate` | ✅ | `W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +140` |
| `Pbc_req` | `unknown` | ❌ | `W_DURING_CONST_ASSIGN, W_DURING_CONST_ASSIGN, W_DURING_CONST_ASSIGN, W_DURING_CONST_ASSIGN, W_DURING_CONST_ASSIGN, ... +4` |
| `Pbd_req` | `unknown` | ❌ | `W_DURING_CONST_ASSIGN, W_DURING_CONST_ASSIGN, W_DURING_CONST_ASSIGN, W_DURING_CONST_ASSIGN, W_DURING_CONST_ASSIGN, ... +4` |
| `Pbdismax` | `unknown` | ❌ | `W_UNWRITTEN_READ_VAR, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +56` |
| `Pd1max` | `external_input_candidate` | ✅ | `W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +56` |
| `Pd2max` | `unknown` | ❌ | `W_UNWRITTEN_READ_VAR, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +32` |
| `Pg_req` | `unknown` | ❌ | `W_DURING_CONST_ASSIGN, W_DURING_CONST_ASSIGN, W_DURING_CONST_ASSIGN, W_DURING_CONST_ASSIGN, W_DURING_CONST_ASSIGN, ... +2` |
| `Pgmax` | `external_input_candidate` | ✅ | `W_UNWRITTEN_READ_VAR, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +20` |
| `Ppv` | `external_input_candidate` | ✅ | `W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +140` |
| `Pw` | `external_input_candidate` | ✅ | `W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +140` |
| `SoC` | `external_input_candidate` | ✅ | `W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +140` |
| `cmd_DG1_cut_in` | `unknown` | ❌ | `W_DURING_CONST_ASSIGN, W_DURING_CONST_ASSIGN, W_DURING_CONST_ASSIGN, W_DURING_CONST_ASSIGN, W_DURING_CONST_ASSIGN, ... +9` |
| `cmd_DG1_cut_out` | `unknown` | ❌ | `W_DURING_CONST_ASSIGN, W_DURING_CONST_ASSIGN, W_DURING_CONST_ASSIGN, W_DURING_CONST_ASSIGN, W_DURING_CONST_ASSIGN, ... +9` |
| `cmd_DG2_cut_in` | `unknown` | ❌ | `W_DURING_CONST_ASSIGN, W_DURING_CONST_ASSIGN, W_DURING_CONST_ASSIGN, W_DURING_CONST_ASSIGN, W_DURING_CONST_ASSIGN, ... +9` |
| `cmd_DG2_cut_out` | `unknown` | ❌ | `W_DURING_CONST_ASSIGN, W_DURING_CONST_ASSIGN, W_DURING_CONST_ASSIGN, W_DURING_CONST_ASSIGN, W_DURING_CONST_ASSIGN, ... +9` |
| `cmd_LNG_cut_in` | `unknown` | ❌ | `W_DURING_CONST_ASSIGN, W_DURING_CONST_ASSIGN, W_DURING_CONST_ASSIGN, W_DURING_CONST_ASSIGN, W_DURING_CONST_ASSIGN, ... +9` |
| `cmd_LNG_cut_out` | `unknown` | ❌ | `W_DURING_CONST_ASSIGN, W_DURING_CONST_ASSIGN, W_DURING_CONST_ASSIGN, W_DURING_CONST_ASSIGN, W_DURING_CONST_ASSIGN, ... +9` |
| `cmd_load_cut_in` | `unknown` | ❌ | `W_DURING_CONST_ASSIGN, W_DURING_CONST_ASSIGN, W_DURING_CONST_ASSIGN, W_DURING_CONST_ASSIGN, W_DURING_CONST_ASSIGN, ... +9` |
| `cmd_load_cut_out` | `unknown` | ❌ | `W_DURING_CONST_ASSIGN, W_DURING_CONST_ASSIGN, W_DURING_CONST_ASSIGN, W_DURING_CONST_ASSIGN, W_DURING_CONST_ASSIGN, ... +9` |
| `eng3_Pmax` | `external_input_candidate` | ✅ | `W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +80` |
| `spare_power` | `unknown` | ❌ | `W_DURING_CONST_ASSIGN, W_DURING_CONST_ASSIGN, W_DURING_CONST_ASSIGN, W_DURING_CONST_ASSIGN, W_DURING_CONST_ASSIGN, ... +7` |

#### SD-8 FixRequestBatch / 修改请求

- batch_id：`fixbatch-1-sha256-002b698f3f7`；source_stage=`SD-4`；legacy_plan_kind=`FixPlan`；requests=`12`。

| request_id | severity | hard | waiver | problem | evidence |
|---|---|---:|---:|---|---|
| `fixreq-1-sd4-0-f26560796c` | `blocking_warning` | ❌ | ✅ | Variable 'Pd2max' is read but never written by any action or transition effect.; Variable 'Pbdismax' is read but never written by any action or transition effect.; Transition guard reads only variables that are never cha...<truncated 27 chars> | `W_UNWRITTEN_READ_VAR` |
| `fixreq-1-sd4-1-c951ee247d` | `blocking_warning` | ❌ | ✅ | Variable 'Pd2max' is read but never written by any action or transition effect.; Variable 'Pbdismax' is read but never written by any action or transition effect.; Transition guard reads only variables that are never cha...<truncated 27 chars> | `W_UNWRITTEN_READ_VAR` |
| `fixreq-1-sd4-2-71428c35ee` | `blocking_warning` | ❌ | ✅ | Variable 'Pd2max' is read but never written by any action or transition effect.; Variable 'Pbdismax' is read but never written by any action or transition effect.; Transition guard reads only variables that are never cha...<truncated 27 chars> | `W_GUARD_VARS_NEVER_CHANGE` |
| `fixreq-1-sd4-3-a578ad8034` | `blocking_warning` | ❌ | ✅ | Variable 'Pd2max' is read but never written by any action or transition effect.; Variable 'Pbdismax' is read but never written by any action or transition effect.; Transition guard reads only variables that are never cha...<truncated 27 chars> | `W_GUARD_VARS_NEVER_CHANGE` |
| `fixreq-1-sd4-4-f1a79d5d37` | `blocking_warning` | ❌ | ✅ | Variable 'Pd2max' is read but never written by any action or transition effect.; Variable 'Pbdismax' is read but never written by any action or transition effect.; Transition guard reads only variables that are never cha...<truncated 27 chars> | `W_GUARD_VARS_NEVER_CHANGE` |
| `fixreq-1-sd4-5-0d78ca18de` | `blocking_warning` | ❌ | ✅ | Variable 'Pd2max' is read but never written by any action or transition effect.; Variable 'Pbdismax' is read but never written by any action or transition effect.; Transition guard reads only variables that are never cha...<truncated 27 chars> | `W_GUARD_VARS_NEVER_CHANGE` |
| `fixreq-1-sd4-6-8a19f87ff5` | `blocking_warning` | ❌ | ✅ | Variable 'Pd2max' is read but never written by any action or transition effect.; Variable 'Pbdismax' is read but never written by any action or transition effect.; Transition guard reads only variables that are never cha...<truncated 27 chars> | `W_GUARD_VARS_NEVER_CHANGE` |
| `fixreq-1-sd4-7-968c971cfc` | `blocking_warning` | ❌ | ✅ | Variable 'Pd2max' is read but never written by any action or transition effect.; Variable 'Pbdismax' is read but never written by any action or transition effect.; Transition guard reads only variables that are never cha...<truncated 27 chars> | `W_GUARD_VARS_NEVER_CHANGE` |
| `fixreq-1-sd4-8-f5dda30df3` | `blocking_warning` | ❌ | ✅ | Variable 'Pd2max' is read but never written by any action or transition effect.; Variable 'Pbdismax' is read but never written by any action or transition effect.; Transition guard reads only variables that are never cha...<truncated 27 chars> | `W_GUARD_VARS_NEVER_CHANGE` |
| `fixreq-1-sd4-9-eafff4b184` | `blocking_warning` | ❌ | ✅ | Variable 'Pd2max' is read but never written by any action or transition effect.; Variable 'Pbdismax' is read but never written by any action or transition effect.; Transition guard reads only variables that are never cha...<truncated 27 chars> | `W_GUARD_VARS_NEVER_CHANGE` |
- ……另有 `2` 个 request 见 run record。

#### SD-8 legacy fix plan / 修改建议

- recommended_strategy：Use diagnostics as hints; choose the smallest globally consistent repair.；Before returning a candidate, verify every required_preserve_element_id still has a concrete DSL representation.
- hint 1：The variable is used as input but never updated after its initial definition, so model behavior may be accidentally constant.；`actions=add_write, simplify_guard；do_not=Do not add a meaningless self-assignment.`
- hint 2：The variable is used as input but never updated after its initial definition, so model behavior may be accidentally constant.；`actions=add_write, simplify_guard；do_not=Do not add a meaningless self-assignment.`
- hint 3：This guard is controlled only by initial variable values. If those values never change, the transition condition is effectively fixed.；`actions=add_write, simplify_guard；do_not=Do not add a meaningless self-assignment; it does not model a real change., Do not rewrite the guard to a meaningless constant only to silence this diagnostic.`
- hint 4：This guard is controlled only by initial variable values. If those values never change, the transition condition is effectively fixed.；`actions=add_write, simplify_guard；do_not=Do not add a meaningless self-assignment; it does not model a real change., Do not rewrite the guard to a meaningless constant only to silence this diagnostic.`
- hint 5：This guard is controlled only by initial variable values. If those values never change, the transition condition is effectively fixed.；`actions=add_write, simplify_guard；do_not=Do not add a meaningless self-assignment; it does not model a real change., Do not rewrite the guard to a meaningless constant only to silence this diagnostic.`
- hint 6：This guard is controlled only by initial variable values. If those values never change, the transition condition is effectively fixed.；`actions=add_write, simplify_guard；do_not=Do not add a meaningless self-assignment; it does not model a real change., Do not rewrite the guard to a meaningless constant only to silence this diagnostic.`
- forbidden_edits：`Do not delete grounded required elements merely to silence diagnostics., Do not invent internal plant/environment dynamics merely to make external input variables appear written.`。
- required_preserve_element_ids：`state:ZeroLoadCharge, state:ZeroLoadSpare, state:ResCoversCharge, state:ResCoversSpare, state:BatteryOnly, state:BatteryLng, state:BatteryLngDg1, state:AllThermalNormalSoc, state:LngChargeLowSoc, state:LngDg1ChargeLowSoc, state:LngDg1Dg2ChargeLowSoc, state:OverloadCompletionIllegal, ... +19`。

#### SL-9 per-request 决策

- accepted_request_ids：`<derived-from-table>`；candidate_len=`7711`。

| request_id | decision | waiver | rework_locked | rationale / intent |
|---|---|---:|---:|---|
| `fixreq-1-sd4-0-f26560796c` | `accept` | ❌ | ❌ | Pd2max is an externally read DG2 capacity bound required by the NL's capacity-based dispatch selection. The FixLog shows the same local warning was already overridden by SL-10 because adding an EMS-internal write would invent plant/capacity dynamics or create a meaningless self-assignment.；intent=Preserve Pd2max as a read-only external capacity input and kee...<truncated 35 chars> |
| `fixreq-1-sd4-1-c951ee247d` | `accept` | ❌ | ❌ | Pbdismax is an externally read battery discharge capacity bound needed for the battery-priority and overload branch guards. The NL says the FSM reads capacity bounds; it does not define internal updates to those bounds.；intent=Preserve Pbdismax as a read-only external capacity input and avoid ungrounded writes. |
| `fixreq-1-sd4-2-71428c35ee` | `accept` | ❌ | ❌ | The BatteryOnly selection guard over PL, Ppv, Pw, SoC, and Pbdismax is a required logical condition over external load/resource/SoC/capacity inputs. Simplifying or rewriting it would damage the twelve-state classifier required by the NL.；intent=Preserve BatteryOnly guard as an external-input logical state selector. |
| `fixreq-1-sd4-3-a578ad8034` | `accept` | ❌ | ❌ | The BatteryLng guard implements the required priority order RES first, suitable battery discharge, then LNG before diesel, using external demand/resource and capacity values. No NL-grounded internal update exists for those inputs.；intent=Preserve BatteryLng guard and dispatch behavior. |
| `fixreq-1-sd4-4-f1a79d5d37` | `accept` | ❌ | ❌ | The BatteryLngDg1 guard is needed for the branch where battery and LNG capacity are insufficient and DG1 is introduced before DG2. Its variables are external operating conditions and capacity bounds.；intent=Preserve BatteryLngDg1 guard as an NL-grounded capacity selector. |
| `fixreq-1-sd4-5-0d78ca18de` | `accept` | ❌ | ❌ | The AllThermalNormalSoc guard selects the branch using all thermal units at normal SoC, based on external demand, renewable contribution, battery capacity, and thermal capacity. Deleting or constant-folding it would violate the NL.；intent=Preserve AllThermalNormalSoc guard and output actions. |
| `fixreq-1-sd4-6-8a19f87ff5` | `accept` | ❌ | ❌ | The LngDg1Dg2ChargeLowSoc guard represents the required low-SoC diesel-generator branch with the Pd1max/10 charging margin and DG2 as last priority. The warning arises because pyfcstm cannot know these are external inputs.；intent=Preserve LngDg1Dg2ChargeLowSoc low-SoC guard. |
| `fixreq-1-sd4-7-968c971cfc` | `accept` | ❌ | ❌ | The OverloadCompletionIllegal guard is required by the NL to represent the illegal overload completion case where all thermal units are active and the remaining lack is battery discharge. It must remain condition-selected by external operating inputs.；intent=Preserve OverloadCompletionIllegal guard and actions. |
| `fixreq-1-sd4-8-f5dda30df3` | `accept` | ❌ | ❌ | The ZeroLoadSpare-to-BatteryOnly warning is an expanded instance of the global forced transition classifier. The guard remains correct because it reads external load, renewable, SoC, and battery capacity values.；intent=Preserve forced transition classifier behavior. |
| `fixreq-1-sd4-9-eafff4b184` | `accept` | ❌ | ❌ | The ZeroLoadSpare-to-BatteryLng warning is also an expanded forced-transition guard over external EMS inputs. Adding writes would invent plant dynamics and removing the guard would remove a required dispatch branch.；intent=Preserve external-input BatteryLng forced-selection guard. |
| `fixreq-1-sd4-10-93c5d5ba5a` | `accept` | ❌ | ❌ | The ZeroLoadSpare-to-BatteryLngDg1 expanded guard is required for the DG1 branch after RES, battery, and LNG priority checks. Its guard variables are external conditions or capacity bounds.；intent=Preserve external-input BatteryLngDg1 forced-selection guard. |
| `fixreq-1-sd4-11-e5f31116bc` | `accept` | ❌ | ❌ | The ZeroLoadSpare-to-AllThermalNormalSoc expanded guard is a required all-thermal selection condition. It should remain guarded by externally supplied demand/resource/capacity values rather than by invented internal writes.；intent=Preserve external-input AllThermalNormalSoc forced-selection guard. |
- repair_rationale：The smallest safe edit is intentionally no DSL text change. The current model already represents the NL-required twelve states, required external input variables, required output variables/commands, RES charge/spare behavior, battery/LNG/DG...<truncated 102 chars>；The selected warnings are W_UNWRITTEN_READ_VAR for Pd2max and Pbdismax and W_GUARD_VARS_NEVER_CHANGE for forced classifier guards. The NL explicitly says the FSM reads PL, Ppv, Pw, SoC, and capacity bounds; it does not specify EMS-internal ...<truncated 34 chars>；Adding writes to Pd2max, Pbdismax, PL, Ppv, Pw, SoC, eng3_Pmax, or Pd1max would violate the request's forbidden edits by inventing plant/environment dynamics. Self-assignments would be meaningless. Simplifying guards to constants or deletin...<truncated 108 chars>；The FixLog was read completely: iteration 0 made the same conservative decision, SD-10 local warnings were explicitly overridden by SL-10, and repair_memory contains no new actionable rework guidance or regression evidence. Therefore the un...<truncated 100 chars>
- diff_summary：`{"summary": "No textual DSL edit. Preserve the existing NL-grounded condition-classifier FSM and treat the warned read-only capacity/demand/resource variables as external inputs rather than inventing ungrounded writes."}`。

#### SL-9 candidate / 最终修改执行方案

```pyfcstm
def float PL = 0.0;
def float Ppv = 0.0;
def float Pw = 0.0;
def float SoC = 0.5;
def float eng3_Pmax = 0.0;
def float Pd1max = 0.0;
def float Pd2max = 0.0;
def float Pbdismax = 0.0;
def float Pgmax = 0.0;
def float Pg_req = 0.0;
def float Pbd_req = 0.0;
def float Pbc_req = 0.0;
def float spare_power = 0.0;
def int cmd_LNG_cut_in = 0;
def int cmd_LNG_cut_out = 1;
def int cmd_DG1_cut_in = 0;
def int cmd_DG1_cut_out = 1;
def int cmd_DG2_cut_in = 0;
def int cmd_DG2_cut_out = 1;
def int cmd_load_cut_in = 1;
def int cmd_load_cut_out = 0;

state LNGShipEMS {
    ! * -> ZeroLoadCharge : if [PL == 0.0 && Ppv + Pw > 0.0 && SoC < 0.95];
    ! * -> ZeroLoadSpare : if [PL == 0.0 && Ppv + Pw > 0.0 && SoC >= 0.95];
    ! * -> ResCoversCharge : if [PL > 0.0 && Ppv + Pw >= PL && SoC < 0.95];
    ! * -> ResCoversSpare : if [PL > 0.0 && Ppv + Pw >= PL && SoC >= 0.95];
    ! * -> BatteryOnly : if [PL > 0.0 && Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw <= Pbdismax];
    ! * -> BatteryLng : if [PL > 0.0 && Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw > Pbdismax && PL - Ppv - Pw <= Pbdismax + eng3_Pmax];
    ! * -> BatteryLngDg1 : if [PL > 0.0 && Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw > Pbdismax + eng3_Pmax && PL - Ppv - Pw <= Pbdismax + eng3_Pmax + Pd1max];
    ! * -> AllThermalNormalSoc : if [PL > 0.0 && Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw > Pbdismax + eng3_Pmax + Pd1max && PL - Ppv - Pw <= Pbdismax + eng3_Pmax + Pd1max + Pd2max];
    ! * -> LngChargeLowSoc : if [PL > 0.0 && Ppv + Pw < PL && SoC < 0.2 && PL - Ppv - Pw + Pgmax / 5.0 <= eng3_Pmax];
    ! * -> LngDg1ChargeLowSoc : if [PL > 0.0 && Ppv + Pw < PL && SoC < 0.2 && PL - Ppv - Pw + Pgmax / 5.0 > eng3_Pmax && PL - Ppv - Pw + Pd1max / 10.0 <= eng3_Pmax + Pd1max];
    ! * -> LngDg1Dg2ChargeLowSoc : if [PL > 0.0 && Ppv + Pw < PL && SoC < 0.2 && PL - Ppv - Pw + Pd1max / 10.0 > eng3_Pmax + Pd1max && PL - Ppv - Pw + Pd1max / 10.0 <= eng3_Pmax + Pd1max + Pd2max];
    ! * -> OverloadCompletionIllegal : if [PL > 0.0 && Ppv + Pw < PL && ((SoC >= 0.2 && PL - Ppv - Pw > Pbdismax + eng3_Pmax + Pd1max + Pd2max) || (SoC < 0.2 && PL - Ppv - Pw + Pd1max / 10.0 > eng3_Pmax + Pd1max + Pd2max))];

    [*] -> ZeroLoadCharge;

    state ZeroLoadCharge {
        during {
            Pg_req = 0.0;
            Pbd_req = 0.0;
            Pbc_req = Ppv + Pw;
            spare_power = 0.0;
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

    state ZeroLoadSpare {
        during {
            Pg_req = 0.0;
            Pbd_req = 0.0;
            Pbc_req = 0.0;
            spare_power = Ppv + Pw;
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

    state ResCoversCharge {
        during {
            Pg_req = 0.0;
            Pbd_req = 0.0;
            Pbc_req = Ppv + Pw - PL;
            spare_power = 0.0;
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

    state ResCoversSpare {
        during {
            Pg_req = 0.0;
            Pbd_req = 0.0;
            Pbc_req = 0.0;
            spare_power = Ppv + Pw - PL;
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

    state BatteryOnly {
        during {
            Pg_req = 0.0;
            Pbd_req = PL - Ppv - Pw;
            Pbc_req = 0.0;
            spare_power = 0.0;
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

    state BatteryLng {
        during {
            Pg_req = PL - Ppv - Pw - Pbdismax;
            Pbd_req = Pbdismax;
            Pbc_req = 0.0;
            spare_power = 0.0;
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

    state BatteryLngDg1 {
        during {
            Pg_req = PL - Ppv - Pw - Pbdismax;
            Pbd_req = Pbdismax;
            Pbc_req = 0.0;
            spare_power = 0.0;
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

    state AllThermalNormalSoc {
        during {
            Pg_req = PL - Ppv - Pw - Pbdismax;
            Pbd_req = Pbdismax;
            Pbc_req = 0.0;
            spare_power = 0.0;
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

    state LngChargeLowSoc {
        during {
            Pg_req = PL - Ppv - Pw + Pgmax / 5.0;
            Pbd_req = 0.0;
            Pbc_req = Pgmax / 5.0;
            spare_power = 0.0;
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

    state LngDg1ChargeLowSoc {
        during {
            Pg_req = PL - Ppv - Pw + Pd1max / 10.0;
            Pbd_req = 0.0;
            Pbc_req = Pd1max / 10.0;
            spare_power = 0.0;
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

    state LngDg1Dg2ChargeLowSoc {
        during {
            Pg_req = PL - Ppv - Pw + Pd1max / 10.0;
            Pbd_req = 0.0;
            Pbc_req = Pd1max / 10.0;
            spare_power = 0.0;
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

    state OverloadCompletionIllegal {
        during {
            Pg_req = eng3_Pmax + Pd1max + Pd2max;
            Pbd_req = PL - Ppv - Pw - eng3_Pmax - Pd1max - Pd2max;
            Pbc_req = 0.0;
            spare_power = 0.0;
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

- SL-10 decision=`pass`，ok=`True`，target_resolved=`True`，regression_detected=`False`，drift_risk=`none`。
- SL-10 review_meta：schema=`SL10RepairReviewOutput.v1`，failure_policy=`fail_closed`，replay_key=`SL-10:sha256:b708226a24b1b5b6b8b02a0e081b9d131e462a7629ea50420b9756a8aa80fdf4`。
  - SL-10 evidence 1: `{"summary": "The NL defines a twelve-state EMS condition-classifier that reads external load, renewable, SoC, and capacity-bound inputs, then selects dispatch states over those values. The candidate preserves all twelve required states, the required variables, the forced logical selection guards, the RES charge/spare cases, battery/LNG/DG priority branches, low-SoC Pgmax/5 and Pd1max/10 charging margins, and the illegal overload completion behavior."}`
  - SL-10 evidence 2: `{"summary": "The complete FixLog shows iteration 0 already accepted and explicitly overrode the same local design warnings because Pd2max, Pbdismax, PL, Ppv, Pw, SoC, eng3_Pmax, Pd1max, and related quantities are external inputs/capacity bounds. The current SL-9 decisions follow that remembered guidance and do not repeat an unsafe repair attempt."}`
  - SL-10 evidence 3: `{"summary": "The DSL diff is intentionally empty. For these non-hard design warnings, no textual edit is the smallest NL-faithful repair: adding writes would invent forbidden plant/environment dynamics or meaningless self-assignments, while simplifying/removing guards would delete required logical transition conditions over demand, generation, capacity, and SoC."}`
  - SL-10 evidence 4: `{"summary": "Current local deterministic evidence is now OK: target_resolved=true, regression_detected=false, drift_risk=none, and local_rejection=null. There are no scenario regressions or actionable local repair items in this bundle."}`
- local checks evidence：stage=`SD-10`；note=PR-E1 uses local parse/semantic/design/sim checks as SL-10 evidence, not as the final deterministic judge.。
  - local ok=`True`，target_resolved=`True`，regression_detected=`False`，drift_risk=`none`。

</details>


#### FixLog ledger

口径：FixLog 是跨 iteration 的 append-only repair 台账，记录 request batch、SL-9 accept/reject、diff/local evidence、SL-10 批示和下一步动作。

| # | iteration | phase | batch | decisions | next_action | candidate | notes |
|---:|---:|---|---|---|---|---|---|
| 1 | `0` | `request_batch` | `fixbatch-0-sha256-002b698f3f7` | accept=0, reject=0 | `sl9_decision_and_repair` | `<none>` | SD-8 produced FixRequestBatch; deterministic stage does not decide final repair. |
| 2 | `0` | `sl9_decision` | `fixbatch-0-sha256-002b698f3f7` | accept=12, reject=0 | `sl10_review` | `sha256:a94551f062423d91b55b99075201100b6caf098b41ba33f7779df2d3ca5a111a` | No textual DSL edit is the smallest safe repair. The selected diagnostics are W_UNWRITTEN_READ_VAR and W_GUARD_VARS_NEVER_CHANGE on variables that the NL defines as read inputs: PL, Ppv, Pw, SoC, engine/generator capacity bounds, and battery-discharge capacity., The NL requires the twelve states to be selected by logical transition conditions over demand, generation, capacity, and SoC. Replacing those guards with constants or removing them would delete required behavior., Adding writes to Pd2max, Pbdismax, PL, Ppv, Pw, SoC, eng3_Pmax, or Pd1max would invent plant/environment dynamics that the NL does not provide and is specifically forbidden by the repair request guidance., ... +1 |
| 3 | `0` | `sl10_review` | `fixbatch-0-sha256-002b698f3f7` | accept=12, reject=0 | `sc11_accept_then_sd2` | `sha256:a94551f062423d91b55b99075201100b6caf098b41ba33f7779df2d3ca5a111a` | repair_memory:sl10_evidence, repair_memory:sl10_evidence, repair_memory:sl10_evidence, ... +1 |
| 4 | `1` | `request_batch` | `fixbatch-1-sha256-002b698f3f7` | accept=0, reject=0 | `sl9_decision_and_repair` | `<none>` | SD-8 produced FixRequestBatch; deterministic stage does not decide final repair. |
| 5 | `1` | `sl9_decision` | `fixbatch-1-sha256-002b698f3f7` | accept=12, reject=0 | `sl10_review` | `sha256:a94551f062423d91b55b99075201100b6caf098b41ba33f7779df2d3ca5a111a` | The smallest safe edit is intentionally no DSL text change. The current model already represents the NL-required twelve states, required external input variables, required output variables/commands, RES charge/spare behavior, battery/LNG/DG priority branches, low-SoC Pgmax/5 and Pd1max/10 margins, and the illegal overload completion branch., The selected warnings are W_UNWRITTEN_READ_VAR for Pd2max and Pbdismax and W_GUARD_VARS_NEVER_CHANGE for forced classifier guards. The NL explicitly says the FSM reads PL, Ppv, Pw, SoC, and capacity bounds; it does not specify EMS-internal dynamics that update those inputs., Adding writes to Pd2max, Pbdismax, PL, Ppv, Pw, SoC, eng3_Pmax, or Pd1max would violate the request's forbidden edits by inventing plant/environment dynamics. Self-assignments would be meaningless. Simplifying guards to constants or deleting guards would remove the required logical transition conditions over demand, generation, capacity, and SoC., ... +1 |
| 6 | `1` | `sl10_review` | `fixbatch-1-sha256-002b698f3f7` | accept=12, reject=0 | `sc11_accept_then_sd2` | `sha256:a94551f062423d91b55b99075201100b6caf098b41ba33f7779df2d3ca5a111a` | repair_memory:sl10_evidence, repair_memory:sl10_evidence, repair_memory:sl10_evidence, ... +3 |

### 8. 尝试记录与成本

- `SL-1`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 5917, 'completion_chars': 19264, 'completion_tokens': 8278, 'elapsed_seconds': 155.29144283896312, 'estimated_completion_tokens': 4816, 'estimated_prompt_tokens': 6646, 'estimated_total_tokens': 11462, 'first_chunk_seconds': 48.88157189101912, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 26582, 'prompt_tokens': 6469, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 14747}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-9`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 4622, 'completion_chars': 15259, 'completion_tokens': 5141, 'elapsed_seconds': 97.3904900199268, 'estimated_completion_tokens': 3815, 'estimated_prompt_tokens': 39730, 'estimated_total_tokens': 43545, 'first_chunk_seconds': 15.001094941049814, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 158918, 'prompt_tokens': 38558, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 43699}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-10`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 643, 'completion_chars': 3047, 'completion_tokens': 793, 'elapsed_seconds': 19.53328513703309, 'estimated_completion_tokens': 762, 'estimated_prompt_tokens': 34706, 'estimated_total_tokens': 35468, 'first_chunk_seconds': 8.04570565209724, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 138824, 'prompt_tokens': 32528, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 33321}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-9`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 4658, 'completion_chars': 15326, 'completion_tokens': 4768, 'elapsed_seconds': 91.81609997618943, 'estimated_completion_tokens': 3832, 'estimated_prompt_tokens': 66044, 'estimated_total_tokens': 69876, 'first_chunk_seconds': 7.856945262057707, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 264175, 'prompt_tokens': 57733, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 62501}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-10`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 501, 'completion_chars': 2333, 'completion_tokens': 630, 'elapsed_seconds': 15.182519532041624, 'estimated_completion_tokens': 584, 'estimated_prompt_tokens': 60486, 'estimated_total_tokens': 61070, 'first_chunk_seconds': 6.519473797176033, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 241941, 'prompt_tokens': 51119, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 51749}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 4273, 'completion_chars': 14614, 'completion_tokens': 6048, 'elapsed_seconds': 111.84456596709788, 'estimated_completion_tokens': 3654, 'estimated_prompt_tokens': 15229, 'estimated_total_tokens': 18883, 'first_chunk_seconds': 39.7146058450453, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 60916, 'prompt_tokens': 16417, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 22465}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 4692, 'completion_chars': 16061, 'completion_tokens': 5139, 'elapsed_seconds': 96.32099589891732, 'estimated_completion_tokens': 4016, 'estimated_prompt_tokens': 19048, 'estimated_total_tokens': 23064, 'first_chunk_seconds': 13.295704493997619, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 76189, 'prompt_tokens': 20809, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 25948}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-7`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1707, 'completion_chars': 7657, 'completion_tokens': 2744, 'elapsed_seconds': 58.37844968610443, 'estimated_completion_tokens': 1915, 'estimated_prompt_tokens': 58538, 'estimated_total_tokens': 60453, 'first_chunk_seconds': 30.39848018810153, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 234150, 'prompt_tokens': 68208, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 70952}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。

### 9. 最终停止状态与后续含义

- 停止状态：verdict=`success`，record_status=`success`。
- 主要原因分类：`success`。
- required stages executed：`28/16`，missing=`<none>`。
- repairs：`2/2` accepted；scenario_history=`2`。
- 配置含义：`recommended baseline candidate`；该结果可用于评估默认入口本身。
- 主结果/蓝本边界：`main_result_eligible` 只表示该 run 非 provider-invalid 且 trace/schema/secret/final-verdict 口径可进入主结果候选；`path2_ref_model_blueprint_eligible=false` 时，模型仍可作为 FE/BVS 或 dispatch-classifier 压力测试证据，但不得称为 Path2 ref-model 主蓝本。
- 样本含义：若出现 `design_or_variable_dynamics`，应重点审查变量是否仅作为 guard/input 常量而没有事件/动作更新；若出现 pre-scenario parse/semantic 失败，则应先优化 pyfcstm grammar adherence。
