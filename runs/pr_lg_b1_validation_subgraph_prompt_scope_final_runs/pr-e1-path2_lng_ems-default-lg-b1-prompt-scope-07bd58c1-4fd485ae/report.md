## path2 / state-transitions-logical-design-for-hybrid-energy-generation-with-renewable-energy-sources-in-lng-ship / default 真实运行结果：Path2 LNG-ship EMS representative NL

### 0. 准确边界与结论

- 运行入口：`method.loop.run_agent_loop(nl, LoopConfig(...))`。
- 是否使用 fake / fixture / hot-start / replay：否；本次使用真实默认入口/显式 PR-E1 探索条件，没有 fake、fixture、hot-start 或 replay。
- final verdict：`success`；record_status：`success`；result_status：`converged`。
- main_result_eligible：`false`。
- Path2 ref-model blueprint eligible：`false`；reason：run_not_main_result_eligible。
- 一句话结论：`success_but_weak_oracle_ineligible`；停止原因：full_pass_all_required_feedback_ok。

### 1. 基本信息

| 字段 | 值 |
|---|---|
| Path | `path2` |
| case_id | `state-transitions-logical-design-for-hybrid-energy-generation-with-renewable-energy-sources-in-lng-ship` |
| config_id | `default` |
| 运行入口 | `method.loop.run_agent_loop(nl, LoopConfig(...))` |
| LoopConfig 摘要 | `condition_id=full_staged_v1`, `max_iterations=5`, `llm_max_retries=2`, `scenario_max_retries=2`, `min_sl10_rework_attempts=1`, `model_review_mode=blocking_major_only`, `repair_review_mode=blocking_major_only` |
| Git commit | `07bd58c155b512bef419dbaadb50f6e43c3ce544` |
| clean / diff / prompt snapshot | clean=`True`, dirty=`False`, diff_hash=`sha256:2a69ad5797ac568a81bddcef615104303a97261094685f4edd8d4484e889ea09`, prompt_hash=`sha256:29acd3d1171a37b465f2b9278c85877dcbc5703e2d154247154b0c8cb90d6c8e` |
| provider/model 脱敏标识 | mode=`real_env`, model=`gpt-5.5`, real_api=`True` |
| source / paper | source=`project_1_llm_state_machine_modeling/sources/state-transitions-logical-design-for-hybrid-energy-generation-with-renewable-energy-sources-in-lng-ship`, paper=`project_1_llm_state_machine_modeling/sources/state-transitions-logical-design-for-hybrid-energy-generation-with-renewable-energy-sources-in-lng-ship/paper.pdf` |
| 样本筛选理由 | issue #14 / PR-D 代表性 Path2 EFSM，变量、guard、12 个状态和非法状态都明确；但它可能退化为条件分类式 dispatch，因此更适合作为 FE/BVS 压力测试，是否适合作为 Path2 ref-model 蓝本需看最终 DSL 是否具有 state-dependent mode memory。 |
| 变量参与说明 | `PL/Ppv/Pw/SoC/eng*_Pmax` 是环境输入/容量边界，适合暴露 SD-4 对外部输入变量的处理能力。 |
| run_id | `pr-e1-path2_lng_ems-default-lg-b1-prompt-scope-07bd58c1-4fd485ae` |
| final verdict/status | verdict=`success`, record=`success`, result=`converged` |
| main_result_eligible | `false` |
| state_mode_decorative_detected | `true` |
| path2_ref_model_blueprint_eligible | `false`；run_not_main_result_eligible |
| final.fcstm 来源 | `{"final_dsl_hash": "sha256:c3b33abde7296af28e4d0495e1ec9ba95e3746ead6202a7d179de197bda7b236", "source_kind": "initial_or_unrepaired"}` |
| SC-11 post-accept validation | attempted=`false`；attempts=`0`；success=`0`；failure=`0` |
| FixLog next_action 序列 | `<none>` |
| iteration exit_reason 序列 | `full_pass_all_required_feedback_ok` |
| token/cost/time | tokens=`{'prompt_tokens': 128170, 'completion_tokens': 25247, 'total_tokens': 153417, 'estimated_prompt_tokens': 116927, 'estimated_completion_tokens': 18261, 'estimated_total_tokens': 135188, 'prompt_chars': 467702, 'completion_chars': 73036, 'n_calls': 5, 'token_usage_available': True, 'token_usage_unavailable_calls': 0}`, elapsed=`481.091s` |
| run record | [`pr-e1-path2_lng_ems-default-lg-b1-prompt-scope-07bd58c1-4fd485ae.agent_loop.json.gz`](./pr-e1-path2_lng_ems-default-lg-b1-prompt-scope-07bd58c1-4fd485ae.agent_loop.json.gz) |
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
| `graph_config_hash` | `sha256:b223e9c007f0e6bf994a73422bf90924144b919a3d25259b4c0d3253d303baaa` |
| `node_edge_schema_version` | `pr-langgraph.stage-nodes.v1` |
| `checkpoint_backend` | `memory` |
| `checkpoint_backend_type` | `InMemorySaver` |
| `checkpoint_serde` | `pickle` |
| `checkpoint_path_hash` | `sha256:memory` |
| `resumed_from_checkpoint` | `False` |
| `resume_checkpoint_id_hash` | `None` |
| `instrumentation_layer` | `langgraph` |
| `stage_semantics_module` | `method.staged_runtime` |
| `langgraph_node_trace_count` | `20` |
| `langgraph_node_trace_hash` | `sha256:0275a55617f1fbea9405e3ae8b4ef64da7b526ab57d2e353aebdb2200aa99d67` |
| `langgraph_compat_ok` | `True` |
| `checkpoint_resume_smoke_scope` | `toy_ledger_langgraph_api_smoke` |
| `real_agent_loop_resume_supported` | `False` |
| `resume_append_only` | `True` |
| `final_trace_delegated_monolithic_runtime` | `False` |
| `final_trace_node_trace_count` | `20` |

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
def float eng3_Pmax = 0.0;
def float Pgmax = 0.0;
def float Pd1max = 0.0;
def float Pd2max = 0.0;
def float requested_generator_power = 0.0;
def float battery_discharge_power = 0.0;
def float battery_charging_power = 0.0;
def float spare_power = 0.0;
def int cmd_LNG_cutin = 0;
def int cmd_LNG_cutout = 1;
def int cmd_DG1_cutin = 0;
def int cmd_DG1_cutout = 1;
def int cmd_DG2_cutin = 0;
def int cmd_DG2_cutout = 1;
def int cmd_load_cutin = 0;
def int cmd_load_cutout = 1;
def int illegal_overload = 0;

state LNGShipEMS {
    ! * -> ZeroLoadNoRES : if [PL == 0 && Ppv + Pw <= 0];
    ! * -> ZeroLoadCharge : if [PL == 0 && Ppv + Pw > 0 && SoC < 0.95];
    ! * -> ZeroLoadSpare : if [PL == 0 && Ppv + Pw > 0 && SoC >= 0.95];
    ! * -> RESCoverCharge : if [PL > 0 && Ppv + Pw >= PL && SoC < 0.95];
    ! * -> RESCoverSpare : if [PL > 0 && Ppv + Pw >= PL && SoC >= 0.95];
    ! * -> BatteryDischarge : if [PL > 0 && Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw <= Pgmax];
    ! * -> LNGCoverLowSoCCharge : if [PL > 0 && Ppv + Pw < PL && SoC < 0.2 && PL - Ppv - Pw <= eng3_Pmax];
    ! * -> LNGCover : if [PL > 0 && Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw > Pgmax && PL - Ppv - Pw <= eng3_Pmax];
    ! * -> LNGDG1LowSoCCharge : if [PL > 0 && Ppv + Pw < PL && SoC < 0.2 && PL - Ppv - Pw > eng3_Pmax && PL - Ppv - Pw <= eng3_Pmax + Pd1max];
    ! * -> LNGDG1 : if [PL > 0 && Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw > eng3_Pmax && PL - Ppv - Pw <= eng3_Pmax + Pd1max];
    ! * -> LNGDG1DG2 : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > eng3_Pmax + Pd1max && PL - Ppv - Pw <= eng3_Pmax + Pd1max + Pd2max];
    ! * -> ExtremeOverloadBatterySupport : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > eng3_Pmax + Pd1max + Pd2max];

    [*] -> ZeroLoadNoRES;

    state ZeroLoadNoRES {
        during {
            requested_generator_power = 0.0;
            battery_discharge_power = 0.0;
            battery_charging_power = 0.0;
            spare_power = 0.0;
            cmd_LNG_cutin = 0;
            cmd_LNG_cutout = 1;
            cmd_DG1_cutin = 0;
            cmd_DG1_cutout = 1;
            cmd_DG2_cutin = 0;
            cmd_DG2_cutout = 1;
            cmd_load_cutin = 0;
            cmd_load_cutout = 1;
            illegal_overload = 0;
        }
    }

    state ZeroLoadCharge {
        during {
            requested_generator_power = 0.0;
            battery_discharge_power = 0.0;
            battery_charging_power = Ppv + Pw;
            spare_power = 0.0;
            cmd_LNG_cutin = 0;
            cmd_LNG_cutout = 1;
            cmd_DG1_cutin = 0;
            cmd_DG1_cutout = 1;
            cmd_DG2_cutin = 0;
            cmd_DG2_cutout = 1;
            cmd_load_cutin = 0;
            cmd_load_cutout = 1;
            illegal_overload = 0;
        }
    }

    state ZeroLoadSpare {
        during {
            requested_generator_power = 0.0;
            battery_discharge_power = 0.0;
            battery_charging_power = 0.0;
            spare_power = Ppv + Pw;
            cmd_LNG_cutin = 0;
            cmd_LNG_cutout = 1;
            cmd_DG1_cutin = 0;
            cmd_DG1_cutout = 1;
            cmd_DG2_cutin = 0;
            cmd_DG2_cutout = 1;
            cmd_load_cutin = 0;
            cmd_load_cutout = 1;
            illegal_overload = 0;
        }
    }

    state RESCoverCharge {
        during {
            requested_generator_power = 0.0;
            battery_discharge_power = 0.0;
            battery_charging_power = Ppv + Pw - PL;
            spare_power = 0.0;
            cmd_LNG_cutin = 0;
            cmd_LNG_cutout = 1;
            cmd_DG1_cutin = 0;
            cmd_DG1_cutout = 1;
            cmd_DG2_cutin = 0;
            cmd_DG2_cutout = 1;
            cmd_load_cutin = 1;
            cmd_load_cutout = 0;
            illegal_overload = 0;
        }
    }

    state RESCoverSpare {
        during {
            requested_generator_power = 0.0;
            battery_discharge_power = 0.0;
            battery_charging_power = 0.0;
            spare_power = Ppv + Pw - PL;
            cmd_LNG_cutin = 0;
            cmd_LNG_cutout = 1;
            cmd_DG1_cutin = 0;
            cmd_DG1_cutout = 1;
            cmd_DG2_cutin = 0;
            cmd_DG2_cutout = 1;
            cmd_load_cutin = 1;
            cmd_load_cutout = 0;
            illegal_overload = 0;
        }
    }

    state BatteryDischarge {
        during {
            requested_generator_power = 0.0;
            battery_discharge_power = PL - Ppv - Pw;
            battery_charging_power = 0.0;
            spare_power = 0.0;
            cmd_LNG_cutin = 0;
            cmd_LNG_cutout = 1;
            cmd_DG1_cutin = 0;
            cmd_DG1_cutout = 1;
            cmd_DG2_cutin = 0;
            cmd_DG2_cutout = 1;
            cmd_load_cutin = 1;
            cmd_load_cutout = 0;
            illegal_overload = 0;
        }
    }

    state LNGCoverLowSoCCharge {
        during {
            requested_generator_power = PL - Ppv - Pw + Pgmax / 5;
            battery_discharge_power = 0.0;
            battery_charging_power = Pgmax / 5;
            spare_power = 0.0;
            cmd_LNG_cutin = 1;
            cmd_LNG_cutout = 0;
            cmd_DG1_cutin = 0;
            cmd_DG1_cutout = 1;
            cmd_DG2_cutin = 0;
            cmd_DG2_cutout = 1;
            cmd_load_cutin = 1;
            cmd_load_cutout = 0;
            illegal_overload = 0;
        }
    }

    state LNGCover {
        during {
            requested_generator_power = PL - Ppv - Pw;
            battery_discharge_power = 0.0;
            battery_charging_power = 0.0;
            spare_power = 0.0;
            cmd_LNG_cutin = 1;
            cmd_LNG_cutout = 0;
            cmd_DG1_cutin = 0;
            cmd_DG1_cutout = 1;
            cmd_DG2_cutin = 0;
            cmd_DG2_cutout = 1;
            cmd_load_cutin = 1;
            cmd_load_cutout = 0;
            illegal_overload = 0;
        }
    }

    state LNGDG1LowSoCCharge {
        during {
            requested_generator_power = PL - Ppv - Pw + Pd1max / 10;
            battery_discharge_power = 0.0;
            battery_charging_power = Pd1max / 10;
            spare_power = 0.0;
            cmd_LNG_cutin = 1;
            cmd_LNG_cutout = 0;
            cmd_DG1_cutin = 1;
            cmd_DG1_cutout = 0;
            cmd_DG2_cutin = 0;
            cmd_DG2_cutout = 1;
            cmd_load_cutin = 1;
            cmd_load_cutout = 0;
            illegal_overload = 0;
        }
    }

    state LNGDG1 {
        during {
            requested_generator_power = PL - Ppv - Pw;
            battery_discharge_power = 0.0;
            battery_charging_power = 0.0;
            spare_power = 0.0;
            cmd_LNG_cutin = 1;
            cmd_LNG_cutout = 0;
            cmd_DG1_cutin = 1;
            cmd_DG1_cutout = 0;
            cmd_DG2_cutin = 0;
            cmd_DG2_cutout = 1;
            cmd_load_cutin = 1;
            cmd_load_cutout = 0;
            illegal_overload = 0;
        }
    }

    state LNGDG1DG2 {
        during {
            requested_generator_power = PL - Ppv - Pw;
            battery_discharge_power = 0.0;
            battery_charging_power = 0.0;
            spare_power = 0.0;
            cmd_LNG_cutin = 1;
            cmd_LNG_cutout = 0;
            cmd_DG1_cutin = 1;
            cmd_DG1_cutout = 0;
            cmd_DG2_cutin = 1;
            cmd_DG2_cutout = 0;
            cmd_load_cutin = 1;
            cmd_load_cutout = 0;
            illegal_overload = 0;
        }
    }

    state ExtremeOverloadBatterySupport {
        during {
            requested_generator_power = eng3_Pmax + Pd1max + Pd2max;
            battery_discharge_power = PL - Ppv - Pw - eng3_Pmax - Pd1max - Pd2max;
            battery_charging_power = 0.0;
            spare_power = 0.0;
            cmd_LNG_cutin = 1;
            cmd_LNG_cutout = 0;
            cmd_DG1_cutin = 1;
            cmd_DG1_cutout = 0;
            cmd_DG2_cutin = 1;
            cmd_DG2_cutout = 0;
            cmd_load_cutin = 1;
            cmd_load_cutout = 0;
            illegal_overload = 1;
        }
    }
}
```

### 4. 全流程真实摘要表

| Stage | 是否 LLM | iteration | 结果 | 获取的信息 / 反馈 | 本阶段做了什么 | DSL 修改 | artifact/log |
|---|---:|---:|---:|---|---|---|---|
| `SC-0` | 否 | - | ✅ | trace/control | 初始化 run state | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-prompt-scope-07bd58c1-4fd485ae.agent_loop.json.gz) |
| `SL-1` | 是 | - | ✅ | LLM calls=1, tokens=14684 | 生成初始 DSL 与 grounding seeds | initial len=8162 | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-prompt-scope-07bd58c1-4fd485ae.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-prompt-scope-07bd58c1-4fd485ae.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-prompt-scope-07bd58c1-4fd485ae.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=320, info=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-prompt-scope-07bd58c1-4fd485ae.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=3, tokens=72016 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-prompt-scope-07bd58c1-4fd485ae.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-prompt-scope-07bd58c1-4fd485ae.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=3, tokens=72016 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-prompt-scope-07bd58c1-4fd485ae.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-prompt-scope-07bd58c1-4fd485ae.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=3, tokens=72016 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-prompt-scope-07bd58c1-4fd485ae.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-prompt-scope-07bd58c1-4fd485ae.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-prompt-scope-07bd58c1-4fd485ae.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-prompt-scope-07bd58c1-4fd485ae.agent_loop.json.gz) |
| `SL-7` | 是 | 0 | ✅ | LLM calls=1, tokens=66717 | LLM model review | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-prompt-scope-07bd58c1-4fd485ae.agent_loop.json.gz) |
| `SC-12` | 否 | - | ✅ | full_pass_all_required_feedback_ok | 写 final verdict | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-prompt-scope-07bd58c1-4fd485ae.agent_loop.json.gz) |
| `SC-13` | 否 | - | ✅ | trace/control | 写审计 run record | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-prompt-scope-07bd58c1-4fd485ae.agent_loop.json.gz) |

### 4.1 完整流程日志（stage/control-flow replay ledger）

口径：本节来自 `AgentLoopRunRecord.logs`，与 [`flow_log.json`](./flow_log.json) 一致；用于复现每个 stage 如何进入、得到什么批示、跳转到哪里，以及每次 DSL 产物/候选如何变化。

| # | ts | stage | iter | event | result / jump | DSL evidence |
|---:|---|---|---:|---|---|---|
| 1 | `2026-06-05T14:38:49Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 2 | `2026-06-05T14:38:49Z` | `SC-0` | `-` | `run_start` | {} | <none> |
| 3 | `2026-06-05T14:38:49Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 4 | `2026-06-05T14:38:49Z` | `SL-1` | `-` | `stage_enter` | {"reason": "initial_modeling_adapter_available"} | <none> |
| 5 | `2026-06-05T14:41:22Z` | `SL-1` | `-` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 6 | `2026-06-05T14:41:22Z` | `SL-1` | `-` | `stage_result` | {"jump": "SD-2", "ok": true} | candidate_dsl:len=8162,hash=sha256:c3b33abde729 |
| 7 | `2026-06-05T14:41:22Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 8 | `2026-06-05T14:41:22Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 9 | `2026-06-05T14:41:22Z` | `<control>` | `0` | `iteration_enter` | {} | current_hash=sha256:c3b33abde7296af28e4d0495e1ec9ba95e3746ead6202a7d179de197bda7b236 |
| 10 | `2026-06-05T14:41:22Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 11 | `2026-06-05T14:41:22Z` | `<control>` | `0` | `iteration_validation_enter` | {} | dsl:len=8162,hash=sha256:c3b33abde729, current_hash=sha256:c3b33abde7296af28e4d0495e1ec9ba95e3746ead6202a7d179de197bda7b236 |
| 12 | `2026-06-05T14:41:22Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 13 | `2026-06-05T14:41:22Z` | `SD-2` | `0` | `stage_enter` | {"reason": "full_validation_pass"} | <none> |
| 14 | `2026-06-05T14:41:22Z` | `SD-2` | `0` | `stage_result` | {"jump": "SD-3", "ok": true, "status": "StageStatus.OK"} | <none> |
| 15 | `2026-06-05T14:41:22Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 16 | `2026-06-05T14:41:22Z` | `SD-3` | `0` | `stage_enter` | {"reason": "SD-2 ok"} | <none> |
| 17 | `2026-06-05T14:41:22Z` | `SD-3` | `0` | `stage_result` | {"jump": "SD-4", "ok": true, "status": "StageStatus.OK"} | <none> |
| 18 | `2026-06-05T14:41:22Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 19 | `2026-06-05T14:41:22Z` | `SD-4` | `0` | `stage_enter` | {"reason": "SD-3 ok"} | <none> |
| 20 | `2026-06-05T14:41:22Z` | `SD-4` | `0` | `stage_result` | {"jump": "SL-5", "ok": true, "status": "StageStatus.OK"} | <none> |
| 21 | `2026-06-05T14:41:22Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 22 | `2026-06-05T14:41:22Z` | `SL-5` | `0` | `stage_enter` | {"reason": "scenario_set_absent"} | <none> |
| 23 | `2026-06-05T14:42:52Z` | `SL-5` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 24 | `2026-06-05T14:42:52Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 25 | `2026-06-05T14:42:53Z` | `SD-5A` | `0` | `stage_result` | {"jump": "SL-5 retry", "ok": false, "status": "StageStatus.ADVISORY"} | <none> |
| 26 | `2026-06-05T14:42:53Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 27 | `2026-06-05T14:42:53Z` | `SL-5` | `0` | `stage_enter` | {"reason": "scenario_coverage_gap_retry"} | <none> |
| 28 | `2026-06-05T14:44:19Z` | `SL-5` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 29 | `2026-06-05T14:44:19Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 30 | `2026-06-05T14:44:20Z` | `SD-5A` | `0` | `stage_result` | {"jump": "SL-5 retry", "ok": false, "status": "StageStatus.ADVISORY"} | <none> |
| 31 | `2026-06-05T14:44:20Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 32 | `2026-06-05T14:44:20Z` | `SL-5` | `0` | `stage_enter` | {"reason": "scenario_coverage_gap_retry"} | <none> |
| 33 | `2026-06-05T14:46:00Z` | `SL-5` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 34 | `2026-06-05T14:46:00Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 35 | `2026-06-05T14:46:01Z` | `SD-5A` | `0` | `stage_result` | {"jump": "SC-5F weak_oracle", "ok": false, "status": "StageStatus.ADVISORY"} | <none> |
| 36 | `2026-06-05T14:46:01Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 37 | `2026-06-05T14:46:01Z` | `<control>` | `0` | `scenario_coverage_retry_exhausted` | {} | <none> |
| 38 | `2026-06-05T14:46:01Z` | `SC-5F` | `0` | `stage_result` | {"jump": "SD-6", "ok": true, "reason": null} | <none> |
| 39 | `2026-06-05T14:46:01Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 40 | `2026-06-05T14:46:01Z` | `SD-6` | `0` | `stage_enter` | {"reason": "scenario_set_ready"} | <none> |
| 41 | `2026-06-05T14:46:01Z` | `SD-6` | `0` | `stage_result` | {"jump": "SL-7", "ok": true, "status": "StageStatus.OK"} | <none> |
| 42 | `2026-06-05T14:46:01Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 43 | `2026-06-05T14:46:01Z` | `SL-7` | `0` | `stage_enter` | {"reason": "SD-6 ok"} | <none> |
| 44 | `2026-06-05T14:46:49Z` | `SL-7` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 45 | `2026-06-05T14:46:49Z` | `SL-7` | `0` | `stage_result` | {"jump": "SC-12 success", "ok": true, "status": "StageStatus.OK"} | <none> |
| 46 | `2026-06-05T14:46:49Z` | `SL-7` | `0` | `grounding_update_hints_recorded` | {} | <none> |
| 47 | `2026-06-05T14:46:49Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 48 | `2026-06-05T14:46:49Z` | `<control>` | `0` | `iteration_validation_result` | {"jump": "SC-12 success", "selected_feedback": null} | <none> |
| 49 | `2026-06-05T14:46:49Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 50 | `2026-06-05T14:46:49Z` | `SC-12` | `-` | `sc12_verdict` | {"reason": "full_pass_all_required_feedback_ok", "verdict": "success"} | final_dsl:len=8162,hash=sha256:c3b33abde729 |
| 51 | `2026-06-05T14:46:49Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 52 | `2026-06-05T14:46:49Z` | `SC-13` | `-` | `run_end` | {"verdict": "success"} | final_dsl:len=8162,hash=sha256:c3b33abde729 |
| 53 | `` | `<control>` | `-` | `langgraph_node_trace` | {} | <none> |
| 54 | `` | `<control>` | `-` | `lg_d1_operator_log_artifacts` | {} | <none> |

### 5. Iteration / repair / review 摘要

| Iter | selected feedback | repair? | FixRequestBatch | SL-9 | local checks | SL-10 | 回到 SD-2? | verdict/备注 |
|---:|---|---|---|---|---|---|---|---|
| 0 | `<none>` | no | <none> | <none> | <none> | <none> | no | full_pass_all_required_feedback_ok |

### 6. Scenario 明细与逐轮通过情况

#### 6.1 Scenario pass/fail by iteration

口径：`✅` = 该 scenario 在该轮 SD-6 simulation 通过；`❌` = 该轮失败；`⚪` = 该轮未执行或无该 scenario 结果。

| Scenario | Intent | Iter 1 |
|---|---|---|
| `default_init_zero_load_no_res` | default-init dispatch with PL=0 and no RES should select ZeroLoadNoRES and cut out loads/generators. | ✅ |
| `zero_load_res_charges_battery_below_full_soc` | explicit-hot-start wildcard classification: with PL=0, RES>0, and SoC below 0.95, RES should charge the battery. | ✅ |
| `zero_load_res_spare_at_full_soc_boundary` | explicit-hot-start SoC boundary probe: with PL=0, RES>0, and SoC exactly 0.95, RES should be spare, not battery charge. | ✅ |
| `res_covers_load_charges_battery_below_full_soc` | explicit-hot-start SoC below-boundary probe: when RES covers positive PL and SoC is below 0.95, residual RES should char...<truncated 13 chars> | ✅ |
| `res_covers_load_spare_at_full_soc_boundary` | explicit-hot-start SoC boundary probe: when RES covers positive PL and SoC is exactly 0.95, residual RES should become s...<truncated 11 chars> | ✅ |
| `battery_discharge_at_suitable_soc_and_pgmax_boundary` | explicit-hot-start SoC suitability and capacity boundary probe: with SoC exactly 0.2 and deficit within Pgmax, batteries...<truncated 37 chars> | ✅ |
| `lng_cover_low_soc_adds_pgmax_charging_margin` | explicit-hot-start low-SoC probe: when deficit is LNG-coverable and SoC is below 0.2, LNG should cover load plus Pgmax/5...<truncated 17 chars> | ✅ |
| `lng_cover_without_battery_when_deficit_exceeds_pgmax` | explicit-hot-start priority probe: with suitable SoC but deficit greater than Pgmax and within LNG capacity, LNG should ...<truncated 26 chars> | ✅ |
| `lng_dg1_low_soc_adds_pd1_charging_margin` | explicit-hot-start diesel low-SoC probe: when LNG alone cannot cover and SoC is below 0.2, LNG+DG1 should cover load plu...<truncated 28 chars> | ✅ |
| `lng_dg1_at_suitable_soc_without_charging_margin` | explicit-hot-start SoC suitability boundary probe: with SoC exactly 0.2 and deficit needing DG1 but not DG2, LNG+DG1 sho...<truncated 46 chars> | ✅ |
| `lng_dg1_dg2_last_priority_within_all_thermal_capacity` | explicit-hot-start last-priority probe: when deficit exceeds LNG+DG1 but is within LNG+DG1+DG2, all thermal units should...<truncated 43 chars> | ✅ |
| `extreme_overload_uses_all_thermal_and_battery_support` | explicit-hot-start overload probe: when demand exceeds all RES and thermal resources, all thermal units should activate ...<truncated 85 chars> | ✅ |
| `forced_reclassification_from_zero_load_to_res_cover_spare` | explicit-hot-start forced-transition probe: from ZeroLoadNoRES, global guard classification must switch to RESCoverSpare...<truncated 65 chars> | ✅ |
| `forced_reclassification_from_zero_load_to_extreme_overload` | explicit-hot-start forced-transition probe: from ZeroLoadNoRES, global guard classification must switch to overload supp...<truncated 55 chars> | ✅ |
| `forced_reclassification_from_res_cover_to_battery_discharge` | explicit-hot-start forced-transition missing-line probe: from RESCoverCharge, changed demand with RES below PL and suita...<truncated 53 chars> | ✅ |
| `forced_reclassification_from_extreme_overload_to_zero_load_charge` | explicit-hot-start forced-transition missing-line probe: from ExtremeOverloadBatterySupport, zero load with RES and SoC ...<truncated 54 chars> | ✅ |

#### 6.2 Scenario definitions

<details><summary>`default_init_zero_load_no_res` — default-init dispatch with PL=0 and no RES should select ZeroLoadNoRES and cut out loads/generators.</summary>

| Field | Value |
|---|---|
| description | default-init dispatch with PL=0 and no RES should select ZeroLoadNoRES and cut out loads/generators. |
| initial_state | `<default-init>` |
| initial_vars | `{}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `initial_dispatch_no_load_no_res` | `0` | `[]` | `LNGShipEMS.ZeroLoadNoRES` | `{"battery_charging_power": 0.0, "battery_discharge_power": 0.0, "cmd_DG1_cutin": 0, "cmd_DG2_cutin": 0, "cmd_LNG_cutin": 0, "cmd_load_cutout": 1, "illegal_overload": 0, "requested_generator_power": 0.0, "spare_power": 0.0}` |

</details>

<details><summary>`zero_load_res_charges_battery_below_full_soc` — explicit-hot-start wildcard classification: with PL=0, RES>0, and SoC below 0.95, RES should charge the battery.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start wildcard classification: with PL=0, RES>0, and SoC below 0.95, RES should charge the battery. |
| initial_state | `LNGShipEMS.RESCoverSpare` |
| initial_vars | `{"PL": 0.0, "Ppv": 5.0, "Pw": 3.0, "SoC": 0.94}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `zero_load_charge_selected` | `0` | `[]` | `LNGShipEMS.ZeroLoadCharge` | `{"battery_charging_power": 8.0, "battery_discharge_power": 0.0, "cmd_load_cutout": 1, "illegal_overload": 0, "requested_generator_power": 0.0, "spare_power": 0.0}` |

</details>

<details><summary>`zero_load_res_spare_at_full_soc_boundary` — explicit-hot-start SoC boundary probe: with PL=0, RES>0, and SoC exactly 0.95, RES should be spare, not battery charge.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start SoC boundary probe: with PL=0, RES>0, and SoC exactly 0.95, RES should be spare, not battery charge. |
| initial_state | `LNGShipEMS.ZeroLoadCharge` |
| initial_vars | `{"PL": 0.0, "Ppv": 5.0, "Pw": 3.0, "SoC": 0.95}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `zero_load_spare_selected` | `0` | `[]` | `LNGShipEMS.ZeroLoadSpare` | `{"battery_charging_power": 0.0, "battery_discharge_power": 0.0, "cmd_load_cutout": 1, "illegal_overload": 0, "requested_generator_power": 0.0, "spare_power": 8.0}` |

</details>

<details><summary>`res_covers_load_charges_battery_below_full_soc` — explicit-hot-start SoC below-boundary probe: when RES covers positive PL and SoC is below 0.95, residual RES should charge batteries.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start SoC below-boundary probe: when RES covers positive PL and SoC is below 0.95, residual RES should charge batteries. |
| initial_state | `LNGShipEMS.LNGCover` |
| initial_vars | `{"PL": 10.0, "Ppv": 7.0, "Pw": 5.0, "SoC": 0.94}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `res_cover_charge_selected` | `0` | `[]` | `LNGShipEMS.RESCoverCharge` | `{"battery_charging_power": 2.0, "battery_discharge_power": 0.0, "cmd_DG1_cutin": 0, "cmd_DG2_cutin": 0, "cmd_LNG_cutin": 0, "cmd_load_cutin": 1, "illegal_overload": 0, "requested_generator_power": 0.0, "spare_power": 0.0}` |

</details>

<details><summary>`res_covers_load_spare_at_full_soc_boundary` — explicit-hot-start SoC boundary probe: when RES covers positive PL and SoC is exactly 0.95, residual RES should become spare power.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start SoC boundary probe: when RES covers positive PL and SoC is exactly 0.95, residual RES should become spare power. |
| initial_state | `LNGShipEMS.RESCoverCharge` |
| initial_vars | `{"PL": 10.0, "Ppv": 7.0, "Pw": 5.0, "SoC": 0.95}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `res_cover_spare_selected` | `0` | `[]` | `LNGShipEMS.RESCoverSpare` | `{"battery_charging_power": 0.0, "battery_discharge_power": 0.0, "cmd_DG1_cutin": 0, "cmd_DG2_cutin": 0, "cmd_LNG_cutin": 0, "cmd_load_cutin": 1, "illegal_overload": 0, "requested_generator_power": 0.0, "spare_power": 2.0}` |

</details>

<details><summary>`battery_discharge_at_suitable_soc_and_pgmax_boundary` — explicit-hot-start SoC suitability and capacity boundary probe: with SoC exactly 0.2 and deficit within Pgmax, batteries should cover the deficit before LNG.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start SoC suitability and capacity boundary probe: with SoC exactly 0.2 and deficit within Pgmax, batteries should cover the deficit before LNG. |
| initial_state | `LNGShipEMS.LNGCoverLowSoCCharge` |
| initial_vars | `{"PL": 10.0, "Pd1max": 5.0, "Pd2max": 8.0, "Pgmax": 7.0, "Ppv": 2.0, "Pw": 1.0, "SoC": 0.2, "eng3_Pmax": 12.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `battery_discharge_selected` | `0` | `[]` | `LNGShipEMS.BatteryDischarge` | `{"battery_charging_power": 0.0, "battery_discharge_power": 7.0, "cmd_DG1_cutin": 0, "cmd_DG2_cutin": 0, "cmd_LNG_cutin": 0, "cmd_load_cutin": 1, "illegal_overload": 0, "requested_generator_power": 0.0, "spare_power": 0.0}` |

</details>

<details><summary>`lng_cover_low_soc_adds_pgmax_charging_margin` — explicit-hot-start low-SoC probe: when deficit is LNG-coverable and SoC is below 0.2, LNG should cover load plus Pgmax/5 charging margin.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start low-SoC probe: when deficit is LNG-coverable and SoC is below 0.2, LNG should cover load plus Pgmax/5 charging margin. |
| initial_state | `LNGShipEMS.BatteryDischarge` |
| initial_vars | `{"PL": 10.0, "Pd1max": 5.0, "Pd2max": 8.0, "Pgmax": 10.0, "Ppv": 2.0, "Pw": 1.0, "SoC": 0.19, "eng3_Pmax": 7.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `lng_low_soc_charge_selected` | `0` | `[]` | `LNGShipEMS.LNGCoverLowSoCCharge` | `{"battery_charging_power": 2.0, "battery_discharge_power": 0.0, "cmd_DG1_cutin": 0, "cmd_DG2_cutin": 0, "cmd_LNG_cutin": 1, "cmd_load_cutin": 1, "illegal_overload": 0, "requested_generator_power": 9.0, "spare_power": 0.0}` |

</details>

<details><summary>`lng_cover_without_battery_when_deficit_exceeds_pgmax` — explicit-hot-start priority probe: with suitable SoC but deficit greater than Pgmax and within LNG capacity, LNG should cover before diesel units.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start priority probe: with suitable SoC but deficit greater than Pgmax and within LNG capacity, LNG should cover before diesel units. |
| initial_state | `LNGShipEMS.LNGDG1` |
| initial_vars | `{"PL": 15.0, "Pd1max": 5.0, "Pd2max": 8.0, "Pgmax": 10.0, "Ppv": 2.0, "Pw": 1.0, "SoC": 0.2, "eng3_Pmax": 12.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `lng_cover_selected` | `0` | `[]` | `LNGShipEMS.LNGCover` | `{"battery_charging_power": 0.0, "battery_discharge_power": 0.0, "cmd_DG1_cutin": 0, "cmd_DG2_cutin": 0, "cmd_LNG_cutin": 1, "cmd_load_cutin": 1, "illegal_overload": 0, "requested_generator_power": 12.0, "spare_power": 0.0}` |

</details>

<details><summary>`lng_dg1_low_soc_adds_pd1_charging_margin` — explicit-hot-start diesel low-SoC probe: when LNG alone cannot cover and SoC is below 0.2, LNG+DG1 should cover load plus Pd1max/10 charging margin.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start diesel low-SoC probe: when LNG alone cannot cover and SoC is below 0.2, LNG+DG1 should cover load plus Pd1max/10 charging margin. |
| initial_state | `LNGShipEMS.LNGCover` |
| initial_vars | `{"PL": 18.0, "Pd1max": 5.0, "Pd2max": 8.0, "Pgmax": 10.0, "Ppv": 2.0, "Pw": 1.0, "SoC": 0.19, "eng3_Pmax": 12.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `lng_dg1_low_soc_charge_selected` | `0` | `[]` | `LNGShipEMS.LNGDG1LowSoCCharge` | `{"battery_charging_power": 0.5, "battery_discharge_power": 0.0, "cmd_DG1_cutin": 1, "cmd_DG2_cutin": 0, "cmd_LNG_cutin": 1, "cmd_load_cutin": 1, "illegal_overload": 0, "requested_generator_power": 15.5, "spare_power": 0.0}` |

</details>

<details><summary>`lng_dg1_at_suitable_soc_without_charging_margin` — explicit-hot-start SoC suitability boundary probe: with SoC exactly 0.2 and deficit needing DG1 but not DG2, LNG+DG1 should serve the deficit without charging m...<truncated 6 chars></summary>

| Field | Value |
|---|---|
| description | explicit-hot-start SoC suitability boundary probe: with SoC exactly 0.2 and deficit needing DG1 but not DG2, LNG+DG1 should serve the deficit without charging margin. |
| initial_state | `LNGShipEMS.LNGDG1LowSoCCharge` |
| initial_vars | `{"PL": 18.0, "Pd1max": 5.0, "Pd2max": 8.0, "Pgmax": 10.0, "Ppv": 2.0, "Pw": 1.0, "SoC": 0.2, "eng3_Pmax": 12.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `lng_dg1_selected` | `0` | `[]` | `LNGShipEMS.LNGDG1` | `{"battery_charging_power": 0.0, "battery_discharge_power": 0.0, "cmd_DG1_cutin": 1, "cmd_DG2_cutin": 0, "cmd_LNG_cutin": 1, "cmd_load_cutin": 1, "illegal_overload": 0, "requested_generator_power": 15.0, "spare_power": 0.0}` |

</details>

<details><summary>`lng_dg1_dg2_last_priority_within_all_thermal_capacity` — explicit-hot-start last-priority probe: when deficit exceeds LNG+DG1 but is within LNG+DG1+DG2, all thermal units should cut in and no battery discharge is need...<truncated 3 chars></summary>

| Field | Value |
|---|---|
| description | explicit-hot-start last-priority probe: when deficit exceeds LNG+DG1 but is within LNG+DG1+DG2, all thermal units should cut in and no battery discharge is needed. |
| initial_state | `LNGShipEMS.ExtremeOverloadBatterySupport` |
| initial_vars | `{"PL": 23.0, "Pd1max": 5.0, "Pd2max": 8.0, "Pgmax": 10.0, "Ppv": 2.0, "Pw": 1.0, "SoC": 0.5, "eng3_Pmax": 12.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `lng_dg1_dg2_selected` | `0` | `[]` | `LNGShipEMS.LNGDG1DG2` | `{"battery_charging_power": 0.0, "battery_discharge_power": 0.0, "cmd_DG1_cutin": 1, "cmd_DG2_cutin": 1, "cmd_LNG_cutin": 1, "cmd_load_cutin": 1, "illegal_overload": 0, "requested_generator_power": 20.0, "spare_power": 0.0}` |

</details>

<details><summary>`extreme_overload_uses_all_thermal_and_battery_support` — explicit-hot-start overload probe: when demand exceeds all RES and thermal resources, all thermal units should activate and remaining lack should be battery dis...<truncated 45 chars></summary>

| Field | Value |
|---|---|
| description | explicit-hot-start overload probe: when demand exceeds all RES and thermal resources, all thermal units should activate and remaining lack should be battery discharge in the illegal overload support state. |
| initial_state | `LNGShipEMS.LNGDG1DG2` |
| initial_vars | `{"PL": 33.0, "Pd1max": 5.0, "Pd2max": 8.0, "Pgmax": 10.0, "Ppv": 2.0, "Pw": 1.0, "SoC": 0.5, "eng3_Pmax": 12.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `extreme_overload_support_selected` | `0` | `[]` | `LNGShipEMS.ExtremeOverloadBatterySupport` | `{"battery_charging_power": 0.0, "battery_discharge_power": 5.0, "cmd_DG1_cutin": 1, "cmd_DG2_cutin": 1, "cmd_LNG_cutin": 1, "cmd_load_cutin": 1, "illegal_overload": 1, "requested_generator_power": 25.0, "spare_power": 0.0}` |

</details>

<details><summary>`forced_reclassification_from_zero_load_to_res_cover_spare` — explicit-hot-start forced-transition probe: from ZeroLoadNoRES, global guard classification must switch to RESCoverSpare when RES covers positive load and SoC i...<truncated 25 chars></summary>

| Field | Value |
|---|---|
| description | explicit-hot-start forced-transition probe: from ZeroLoadNoRES, global guard classification must switch to RESCoverSpare when RES covers positive load and SoC is exactly full threshold. |
| initial_state | `LNGShipEMS.ZeroLoadNoRES` |
| initial_vars | `{"PL": 10.0, "Pd1max": 5.0, "Pd2max": 8.0, "Pgmax": 10.0, "Ppv": 15.0, "Pw": 0.0, "SoC": 0.95, "eng3_Pmax": 12.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `forced_guard_selects_res_cover_spare` | `0` | `[]` | `LNGShipEMS.RESCoverSpare` | `{"battery_charging_power": 0.0, "battery_discharge_power": 0.0, "cmd_DG1_cutin": 0, "cmd_DG2_cutin": 0, "cmd_LNG_cutin": 0, "cmd_load_cutin": 1, "cmd_load_cutout": 0, "illegal_overload": 0, "requested_generator_power": 0.0, "spare_power": 5.0}` |

</details>

<details><summary>`forced_reclassification_from_zero_load_to_extreme_overload` — explicit-hot-start forced-transition probe: from ZeroLoadNoRES, global guard classification must switch to overload support when demand exceeds RES plus all the...<truncated 15 chars></summary>

| Field | Value |
|---|---|
| description | explicit-hot-start forced-transition probe: from ZeroLoadNoRES, global guard classification must switch to overload support when demand exceeds RES plus all thermal resources. |
| initial_state | `LNGShipEMS.ZeroLoadNoRES` |
| initial_vars | `{"PL": 33.0, "Pd1max": 5.0, "Pd2max": 8.0, "Pgmax": 10.0, "Ppv": 2.0, "Pw": 1.0, "SoC": 0.5, "eng3_Pmax": 12.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `forced_guard_selects_extreme_overload` | `0` | `[]` | `LNGShipEMS.ExtremeOverloadBatterySupport` | `{"battery_charging_power": 0.0, "battery_discharge_power": 5.0, "cmd_DG1_cutin": 1, "cmd_DG2_cutin": 1, "cmd_LNG_cutin": 1, "cmd_load_cutin": 1, "cmd_load_cutout": 0, "illegal_overload": 1, "requested_generator_power": 25.0, "spare_power": 0.0}` |

</details>

<details><summary>`forced_reclassification_from_res_cover_to_battery_discharge` — explicit-hot-start forced-transition missing-line probe: from RESCoverCharge, changed demand with RES below PL and suitable SoC must globally reclassify to Batt...<truncated 13 chars></summary>

| Field | Value |
|---|---|
| description | explicit-hot-start forced-transition missing-line probe: from RESCoverCharge, changed demand with RES below PL and suitable SoC must globally reclassify to BatteryDischarge. |
| initial_state | `LNGShipEMS.RESCoverCharge` |
| initial_vars | `{"PL": 10.0, "Pd1max": 5.0, "Pd2max": 8.0, "Pgmax": 7.0, "Ppv": 2.0, "Pw": 1.0, "SoC": 0.2, "eng3_Pmax": 12.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `global_guard_selects_battery_discharge` | `0` | `[]` | `LNGShipEMS.BatteryDischarge` | `{"battery_charging_power": 0.0, "battery_discharge_power": 7.0, "cmd_DG1_cutin": 0, "cmd_DG2_cutin": 0, "cmd_LNG_cutin": 0, "cmd_load_cutin": 1, "cmd_load_cutout": 0, "illegal_overload": 0, "requested_generator_power": 0.0, "spare_power": 0.0}` |

</details>

<details><summary>`forced_reclassification_from_extreme_overload_to_zero_load_charge` — explicit-hot-start forced-transition missing-line probe: from ExtremeOverloadBatterySupport, zero load with RES and SoC below 0.95 must globally reclassify to Z...<truncated 14 chars></summary>

| Field | Value |
|---|---|
| description | explicit-hot-start forced-transition missing-line probe: from ExtremeOverloadBatterySupport, zero load with RES and SoC below 0.95 must globally reclassify to ZeroLoadCharge. |
| initial_state | `LNGShipEMS.ExtremeOverloadBatterySupport` |
| initial_vars | `{"PL": 0.0, "Pd1max": 5.0, "Pd2max": 8.0, "Pgmax": 10.0, "Ppv": 4.0, "Pw": 6.0, "SoC": 0.94, "eng3_Pmax": 12.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `global_guard_selects_zero_load_charge` | `0` | `[]` | `LNGShipEMS.ZeroLoadCharge` | `{"battery_charging_power": 10.0, "battery_discharge_power": 0.0, "cmd_DG1_cutin": 0, "cmd_DG2_cutin": 0, "cmd_LNG_cutin": 0, "cmd_load_cutin": 0, "cmd_load_cutout": 1, "illegal_overload": 0, "requested_generator_power": 0.0, "spare_power": 0.0}` |

</details>


### 7. Repair / blocking feedback 明细

- 本 run 未进入 `SD-8/SL-9/SL-10` repair block；通常表示流程在 repair 前已成功、被 provider/schema 错误中断，或在 pre-repair 阶段直接退出。

### 8. 尝试记录与成本

- `SL-1`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 6142, 'completion_chars': 20820, 'completion_tokens': 8215, 'elapsed_seconds': 152.5634076879942, 'estimated_completion_tokens': 5205, 'estimated_prompt_tokens': 6646, 'estimated_total_tokens': 11851, 'first_chunk_seconds': 41.80550393500016, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 26582, 'prompt_tokens': 6469, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 14684}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 3565, 'completion_chars': 12162, 'completion_tokens': 4602, 'elapsed_seconds': 89.97811380799976, 'estimated_completion_tokens': 3041, 'estimated_prompt_tokens': 15622, 'estimated_total_tokens': 18663, 'first_chunk_seconds': 25.738196175021585, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 62488, 'prompt_tokens': 16488, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 21090}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 4237, 'completion_chars': 14517, 'completion_tokens': 4658, 'elapsed_seconds': 86.4473202250083, 'estimated_completion_tokens': 3630, 'estimated_prompt_tokens': 18828, 'estimated_total_tokens': 22458, 'first_chunk_seconds': 10.27077630898566, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 75309, 'prompt_tokens': 20172, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 24830}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 4913, 'completion_chars': 16872, 'completion_tokens': 5252, 'elapsed_seconds': 99.88783190000686, 'estimated_completion_tokens': 4218, 'estimated_prompt_tokens': 19416, 'estimated_total_tokens': 23634, 'first_chunk_seconds': 10.78901525400579, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 77664, 'prompt_tokens': 20844, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 26096}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-7`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1898, 'completion_chars': 8665, 'completion_tokens': 2520, 'elapsed_seconds': 47.987880693981424, 'estimated_completion_tokens': 2167, 'estimated_prompt_tokens': 56415, 'estimated_total_tokens': 58582, 'first_chunk_seconds': 13.998346330976347, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 225659, 'prompt_tokens': 64197, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 66717}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。

### 9. 最终停止状态与后续含义

- 停止状态：verdict=`success`，record_status=`success`。
- 主要原因分类：`success_but_weak_oracle_ineligible`。
- required stages executed：`16/12`，missing=`<none>`。
- repairs：`0/0` accepted；scenario_history=`3`。
- 配置含义：`recommended baseline candidate`；该结果可用于评估默认入口本身。
- 主结果/蓝本边界：`main_result_eligible` 只表示该 run 非 provider-invalid 且 trace/schema/secret/final-verdict 口径可进入主结果候选；`path2_ref_model_blueprint_eligible=false` 时，模型仍可作为 FE/BVS 或 dispatch-classifier 压力测试证据，但不得称为 Path2 ref-model 主蓝本。
- 样本含义：若出现 `design_or_variable_dynamics`，应重点审查变量是否仅作为 guard/input 常量而没有事件/动作更新；若出现 pre-scenario parse/semantic 失败，则应先优化 pyfcstm grammar adherence。
