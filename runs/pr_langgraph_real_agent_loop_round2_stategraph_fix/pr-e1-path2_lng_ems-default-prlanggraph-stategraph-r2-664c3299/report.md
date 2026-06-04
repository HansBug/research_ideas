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
| LoopConfig 摘要 | `condition_id=full_staged_v1`, `max_iterations=5`, `llm_max_retries=2`, `scenario_max_retries=2`, `model_review_mode=blocking_major_only`, `repair_review_mode=blocking_major_only` |
| Git commit | `4f64caf598879346189afaac271a5722d526d936` |
| clean / diff / prompt snapshot | clean=`True`, dirty=`False`, diff_hash=`sha256:2a69ad5797ac568a81bddcef615104303a97261094685f4edd8d4484e889ea09`, prompt_hash=`sha256:993dd2a89560dc22cd287bbf50c2cbe6faab9e99a63729d53f02e0d42085b247` |
| provider/model 脱敏标识 | mode=`real_env`, model=`gpt-5.5`, real_api=`True` |
| source / paper | source=`project_1_llm_state_machine_modeling/sources/state-transitions-logical-design-for-hybrid-energy-generation-with-renewable-energy-sources-in-lng-ship`, paper=`project_1_llm_state_machine_modeling/sources/state-transitions-logical-design-for-hybrid-energy-generation-with-renewable-energy-sources-in-lng-ship/paper.pdf` |
| 样本筛选理由 | issue #14 / PR-D 代表性 Path2 EFSM，变量、guard、12 个状态和非法状态都明确；但它可能退化为条件分类式 dispatch，因此更适合作为 FE/BVS 压力测试，是否适合作为 Path2 ref-model 蓝本需看最终 DSL 是否具有 state-dependent mode memory。 |
| 变量参与说明 | `PL/Ppv/Pw/SoC/eng*_Pmax` 是环境输入/容量边界，适合暴露 SD-4 对外部输入变量的处理能力。 |
| run_id | `pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r2-664c3299` |
| final verdict/status | verdict=`success`, record=`success`, result=`converged` |
| main_result_eligible | `false` |
| state_mode_decorative_detected | `true` |
| path2_ref_model_blueprint_eligible | `false`；run_not_main_result_eligible |
| final.fcstm 来源 | `{"final_dsl_hash": "sha256:320beb5058ff8e8e82c3e3219e118f64e4254e10fd6c325031622a0a6953a1d5", "source_kind": "initial_or_unrepaired"}` |
| FixLog next_action 序列 | `<none>` |
| iteration exit_reason 序列 | `full_pass_all_required_feedback_ok` |
| token/cost/time | tokens=`{'completion_chars': 66259, 'completion_tokens': 23950, 'estimated_completion_tokens': 16568, 'estimated_prompt_tokens': 102561, 'estimated_total_tokens': 119129, 'n_calls': 5, 'prompt_chars': 410234, 'prompt_tokens': 112033, 'token_usage_available': True, 'token_usage_unavailable_calls': 0, 'total_tokens': 135983}`, elapsed=`450.258s` |
| run record | [`pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r2-664c3299.agent_loop.json.gz`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r2-664c3299.agent_loop.json.gz) |
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
| `graph_config_hash` | `sha256:2ecf39a258621bb38220988fb434202b7cb28684cbb1e16613a3e42957599fb4` |
| `node_edge_schema_version` | `pr-langgraph.stage-nodes.v1` |
| `checkpoint_backend` | `memory` |
| `checkpoint_backend_type` | `InMemorySaver` |
| `checkpoint_serde` | `pickle` |
| `checkpoint_path_hash` | `sha256:memory` |
| `resumed_from_checkpoint` | `False` |
| `resume_checkpoint_id_hash` | `None` |
| `instrumentation_layer` | `langgraph` |
| `stage_semantics_module` | `method.staged_runtime` |
| `langgraph_node_trace_count` | `6` |
| `langgraph_node_trace_hash` | `sha256:551ce01053da9bba711a382101de4235854e15508f8676d16863cb2b1134067d` |
| `langgraph_compat_ok` | `True` |
| `checkpoint_resume_smoke_scope` | `toy_ledger_langgraph_api_smoke` |
| `real_agent_loop_resume_supported` | `False` |
| `resume_append_only` | `True` |
| `final_trace_delegated_monolithic_runtime` | `False` |
| `final_trace_node_trace_count` | `6` |

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
def float SoC = 1.0;
def float eng3_Pmax = 0.0;
def float Pgmax = 0.0;
def float Pd1max = 0.0;
def float Pd2max = 0.0;
def float Pbatt_dis_max = 0.0;
def float Pbatt_ch_max = 0.0;
def float Pgen_req = 0.0;
def float Pbatt_discharge = 0.0;
def float Pbatt_charge = 0.0;
def float Pspare = 0.0;
def int cmd_LNG_cut_in = 0;
def int cmd_LNG_cut_out = 1;
def int cmd_DG1_cut_in = 0;
def int cmd_DG1_cut_out = 1;
def int cmd_DG2_cut_in = 0;
def int cmd_DG2_cut_out = 1;
def int cmd_load_cut_in = 1;
def int cmd_load_cut_out = 0;

state LNGShipEMS {
    ! * -> ZeroIdle : if [PL <= 0 && Ppv + Pw <= 0];
    ! * -> ZeroLoadCharge : if [PL <= 0 && Ppv + Pw > 0 && SoC < 0.95];
    ! * -> ZeroLoadSpare : if [PL <= 0 && Ppv + Pw > 0 && SoC >= 0.95];
    ! * -> RESCharge : if [PL > 0 && Ppv + Pw >= PL && SoC < 0.95];
    ! * -> RESSpare : if [PL > 0 && Ppv + Pw >= PL && SoC >= 0.95];
    ! * -> BatteryAssist : if [PL > 0 && Ppv + Pw < PL && SoC >= 0.3 && PL - Ppv - Pw <= Pbatt_dis_max];
    ! * -> LNGOnlyNormal : if [PL > 0 && Ppv + Pw < PL && SoC >= 0.3 && PL - Ppv - Pw > Pbatt_dis_max && PL - Ppv - Pw <= eng3_Pmax];
    ! * -> LNGChargeLowSoC : if [PL > 0 && Ppv + Pw < PL && SoC < 0.3 && PL - Ppv - Pw + Pgmax / 5 <= eng3_Pmax];
    ! * -> LNGDG1Normal : if [PL > 0 && Ppv + Pw < PL && SoC >= 0.3 && PL - Ppv - Pw > eng3_Pmax && PL - Ppv - Pw <= eng3_Pmax + Pd1max];
    ! * -> LNGDG1ChargeLowSoC : if [PL > 0 && Ppv + Pw < PL && SoC < 0.3 && PL - Ppv - Pw + Pgmax / 5 > eng3_Pmax && PL - Ppv - Pw + Pd1max / 10 <= eng3_Pmax + Pd1max];
    ! * -> LNGDG1DG2 : if [PL > 0 && Ppv + Pw < PL && ((SoC >= 0.3 && PL - Ppv - Pw > eng3_Pmax + Pd1max && PL - Ppv - Pw <= eng3_Pmax + Pd1max + Pd2max) || (SoC < 0.3 && PL - Ppv - Pw + Pd1max / 10 > eng3_Pmax + Pd1max && PL - Ppv - Pw <= eng3_Pmax + Pd1max + Pd2max))];
    ! * -> IllegalOverloadAllThermalBattery : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > eng3_Pmax + Pd1max + Pd2max];

    [*] -> ZeroIdle;

    state ZeroIdle {
        enter {
            Pgen_req = 0;
            Pbatt_discharge = 0;
            Pbatt_charge = 0;
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

    state ZeroLoadCharge {
        enter {
            Pgen_req = 0;
            Pbatt_discharge = 0;
            Pbatt_charge = Ppv + Pw;
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

    state ZeroLoadSpare {
        enter {
            Pgen_req = 0;
            Pbatt_discharge = 0;
            Pbatt_charge = 0;
            Pspare = Ppv + Pw;
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

    state RESCharge {
        enter {
            Pgen_req = 0;
            Pbatt_discharge = 0;
            Pbatt_charge = Ppv + Pw - PL;
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

    state RESSpare {
        enter {
            Pgen_req = 0;
            Pbatt_discharge = 0;
            Pbatt_charge = 0;
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

    state BatteryAssist {
        enter {
            Pgen_req = 0;
            Pbatt_discharge = PL - Ppv - Pw;
            Pbatt_charge = 0;
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

    state LNGOnlyNormal {
        enter {
            Pgen_req = PL - Ppv - Pw;
            Pbatt_discharge = 0;
            Pbatt_charge = 0;
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

    state LNGChargeLowSoC {
        enter {
            Pgen_req = PL - Ppv - Pw + Pgmax / 5;
            Pbatt_discharge = 0;
            Pbatt_charge = Pgmax / 5;
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

    state LNGDG1Normal {
        enter {
            Pgen_req = PL - Ppv - Pw;
            Pbatt_discharge = 0;
            Pbatt_charge = 0;
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

    state LNGDG1ChargeLowSoC {
        enter {
            Pgen_req = PL - Ppv - Pw + Pd1max / 10;
            Pbatt_discharge = 0;
            Pbatt_charge = Pd1max / 10;
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
            Pbatt_discharge = 0;
            Pbatt_charge = 0;
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

    state IllegalOverloadAllThermalBattery {
        enter {
            Pgen_req = eng3_Pmax + Pd1max + Pd2max;
            Pbatt_discharge = PL - Ppv - Pw - eng3_Pmax - Pd1max - Pd2max;
            Pbatt_charge = 0;
            Pspare = 0;
            cmd_LNG_cut_in = 1;
            cmd_LNG_cut_out = 0;
            cmd_DG1_cut_in = 1;
            cmd_DG1_cut_out = 0;
            cmd_DG2_cut_in = 1;
            cmd_DG2_cut_out = 0;
            cmd_load_cut_in = 0;
            cmd_load_cut_out = 1;
        }
    }
}
```

### 4. 全流程真实摘要表

| Stage | 是否 LLM | iteration | 结果 | 获取的信息 / 反馈 | 本阶段做了什么 | DSL 修改 | artifact/log |
|---|---:|---:|---:|---|---|---|---|
| `SC-0` | 否 | - | ✅ | trace/control | 初始化 run state | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r2-664c3299.agent_loop.json.gz) |
| `SL-1` | 是 | - | ✅ | LLM calls=1, tokens=14312 | 生成初始 DSL 与 grounding seeds | initial len=7453 | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r2-664c3299.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r2-664c3299.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r2-664c3299.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=179, info=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r2-664c3299.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=3, tokens=71263 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r2-664c3299.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r2-664c3299.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=3, tokens=71263 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r2-664c3299.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r2-664c3299.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=3, tokens=71263 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r2-664c3299.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r2-664c3299.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r2-664c3299.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r2-664c3299.agent_loop.json.gz) |
| `SL-7` | 是 | 0 | ✅ | LLM calls=1, tokens=50408 | LLM model review | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r2-664c3299.agent_loop.json.gz) |
| `SC-12` | 否 | - | ✅ | full_pass_all_required_feedback_ok | 写 final verdict | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r2-664c3299.agent_loop.json.gz) |
| `SC-13` | 否 | - | ✅ | trace/control | 写审计 run record | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r2-664c3299.agent_loop.json.gz) |

### 4.1 完整流程日志（stage/control-flow replay ledger）

口径：本节来自 `AgentLoopRunRecord.logs`，与 [`flow_log.json`](./flow_log.json) 一致；用于复现每个 stage 如何进入、得到什么批示、跳转到哪里，以及每次 DSL 产物/候选如何变化。

| # | ts | stage | iter | event | result / jump | DSL evidence |
|---:|---|---|---:|---|---|---|
| 1 | `2026-06-04T16:42:54Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 2 | `2026-06-04T16:42:54Z` | `SC-0` | `-` | `run_start` | {} | <none> |
| 3 | `2026-06-04T16:42:54Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 4 | `2026-06-04T16:42:54Z` | `SL-1` | `-` | `stage_enter` | {"reason": "initial_modeling_adapter_available"} | <none> |
| 5 | `2026-06-04T16:45:18Z` | `SL-1` | `-` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 6 | `2026-06-04T16:45:18Z` | `SL-1` | `-` | `stage_result` | {"jump": "SD-2", "ok": true} | candidate_dsl:len=7453,hash=sha256:320beb5058ff |
| 7 | `2026-06-04T16:45:18Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 8 | `2026-06-04T16:45:18Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 9 | `2026-06-04T16:45:18Z` | `<control>` | `0` | `iteration_enter` | {} | current_hash=sha256:320beb5058ff8e8e82c3e3219e118f64e4254e10fd6c325031622a0a6953a1d5 |
| 10 | `2026-06-04T16:45:18Z` | `<control>` | `0` | `iteration_validation_enter` | {} | dsl:len=7453,hash=sha256:320beb5058ff, current_hash=sha256:320beb5058ff8e8e82c3e3219e118f64e4254e10fd6c325031622a0a6953a1d5 |
| 11 | `2026-06-04T16:45:18Z` | `SD-2` | `0` | `stage_enter` | {"reason": "full_validation_pass"} | <none> |
| 12 | `2026-06-04T16:45:18Z` | `SD-2` | `0` | `stage_result` | {"jump": "SD-3", "ok": true, "status": "StageStatus.OK"} | <none> |
| 13 | `2026-06-04T16:45:18Z` | `SD-3` | `0` | `stage_enter` | {"reason": "SD-2 ok"} | <none> |
| 14 | `2026-06-04T16:45:18Z` | `SD-3` | `0` | `stage_result` | {"jump": "SD-4", "ok": true, "status": "StageStatus.OK"} | <none> |
| 15 | `2026-06-04T16:45:18Z` | `SD-4` | `0` | `stage_enter` | {"reason": "SD-3 ok"} | <none> |
| 16 | `2026-06-04T16:45:18Z` | `SD-4` | `0` | `stage_result` | {"jump": "SL-5", "ok": true, "status": "StageStatus.OK"} | <none> |
| 17 | `2026-06-04T16:45:18Z` | `SL-5` | `0` | `stage_enter` | {"reason": "scenario_set_absent"} | <none> |
| 18 | `2026-06-04T16:46:41Z` | `SL-5` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 19 | `2026-06-04T16:46:42Z` | `SD-5A` | `0` | `stage_result` | {"jump": "SL-5 retry", "ok": false, "status": "StageStatus.ADVISORY"} | <none> |
| 20 | `2026-06-04T16:46:42Z` | `SL-5` | `0` | `stage_enter` | {"reason": "scenario_coverage_gap_retry"} | <none> |
| 21 | `2026-06-04T16:47:48Z` | `SL-5` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 22 | `2026-06-04T16:47:48Z` | `SD-5A` | `0` | `stage_result` | {"jump": "SL-5 retry", "ok": false, "status": "StageStatus.ADVISORY"} | <none> |
| 23 | `2026-06-04T16:47:48Z` | `SL-5` | `0` | `stage_enter` | {"reason": "scenario_coverage_gap_retry"} | <none> |
| 24 | `2026-06-04T16:49:30Z` | `SL-5` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 25 | `2026-06-04T16:49:31Z` | `SD-5A` | `0` | `stage_result` | {"jump": "SC-5F weak_oracle", "ok": false, "status": "StageStatus.ADVISORY"} | <none> |
| 26 | `2026-06-04T16:49:31Z` | `<control>` | `0` | `scenario_coverage_retry_exhausted` | {} | <none> |
| 27 | `2026-06-04T16:49:31Z` | `SC-5F` | `0` | `stage_result` | {"jump": "SD-6", "ok": true} | <none> |
| 28 | `2026-06-04T16:49:31Z` | `SD-6` | `0` | `stage_enter` | {"reason": "scenario_set_ready"} | <none> |
| 29 | `2026-06-04T16:49:31Z` | `SD-6` | `0` | `stage_result` | {"jump": "SL-7", "ok": true, "status": "StageStatus.OK"} | <none> |
| 30 | `2026-06-04T16:49:31Z` | `SL-7` | `0` | `stage_enter` | {"reason": "SD-6 ok"} | <none> |
| 31 | `2026-06-04T16:50:24Z` | `SL-7` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 32 | `2026-06-04T16:50:24Z` | `SL-7` | `0` | `stage_result` | {"jump": "SC-12 success", "ok": true, "status": "StageStatus.OK"} | <none> |
| 33 | `2026-06-04T16:50:24Z` | `SL-7` | `0` | `grounding_update_hints_recorded` | {} | <none> |
| 34 | `2026-06-04T16:50:24Z` | `<control>` | `0` | `iteration_validation_result` | {"jump": "SC-12 success", "selected_feedback": null} | <none> |
| 35 | `2026-06-04T16:50:24Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 36 | `2026-06-04T16:50:24Z` | `SC-12` | `-` | `sc12_verdict` | {"reason": "full_pass_all_required_feedback_ok", "verdict": "success"} | final_dsl:len=7453,hash=sha256:320beb5058ff |
| 37 | `2026-06-04T16:50:24Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 38 | `2026-06-04T16:50:24Z` | `SC-13` | `-` | `run_end` | {"verdict": "success"} | final_dsl:len=7453,hash=sha256:320beb5058ff |
| 39 | `` | `<control>` | `-` | `langgraph_node_trace` | {} | <none> |

### 5. Iteration / repair / review 摘要

| Iter | selected feedback | repair? | FixRequestBatch | SL-9 | local checks | SL-10 | 回到 SD-2? | verdict/备注 |
|---:|---|---|---|---|---|---|---|---|
| 0 | `<none>` | no | <none> | <none> | <none> | <none> | no | full_pass_all_required_feedback_ok |

### 6. Scenario 明细与逐轮通过情况

#### 6.1 Scenario pass/fail by iteration

口径：`✅` = 该 scenario 在该轮 SD-6 simulation 通过；`❌` = 该轮失败；`⚪` = 该轮未执行或无该 scenario 结果。

| Scenario | Intent | Iter 1 |
|---|---|---|
| `default_init_zero_idle` | default-init probe: with zero load and no renewable production, the initial dispatch should land in ZeroIdle with no gen...<truncated 54 chars> | ✅ |
| `zero_load_res_charges_battery_below_full_soc` | explicit-hot-start probe: with PL=0, positive RES, and SoC below 0.95, renewable production should be sent to battery ch...<truncated 7 chars> | ✅ |
| `zero_load_res_spare_at_full_soc_boundary` | explicit-hot-start boundary probe: with PL=0, positive RES, and SoC exactly 0.95, renewable production should become spa...<truncated 30 chars> | ✅ |
| `res_covers_load_charges_battery_below_full_soc` | explicit-hot-start probe: when RES covers positive load and SoC is below 0.95, all load should be served from RES and re...<truncated 35 chars> | ✅ |
| `res_covers_load_spare_at_full_soc_boundary` | explicit-hot-start boundary probe: when RES covers positive load and SoC is exactly 0.95, residual RES should be spare p...<truncated 32 chars> | ✅ |
| `battery_assist_at_soc_and_discharge_capacity_boundary` | explicit-hot-start boundary probe: with RES below load, SoC exactly 0.3, and deficit equal to battery discharge capacity...<truncated 55 chars> | ✅ |
| `lng_only_after_battery_capacity_exceeded` | explicit-hot-start boundary probe: when RES and battery are insufficient but deficit is exactly within LNG capacity, LNG...<truncated 76 chars> | ✅ |
| `low_soc_lng_charge_margin` | explicit-hot-start low-SoC probe: when SoC is below 0.3 and LNG can cover deficit plus Pgmax/5 charging margin, LNG shou...<truncated 42 chars> | ✅ |
| `lng_dg1_normal_after_lng_capacity_exceeded` | explicit-hot-start boundary probe: with suitable SoC and deficit above LNG capacity but within LNG plus DG1, LNG and DG1...<truncated 40 chars> | ✅ |
| `low_soc_lng_dg1_charge_margin` | explicit-hot-start low-SoC probe: when LNG alone cannot cover the low-SoC charging case, DG1 should be added and Pd1max/...<truncated 44 chars> | ✅ |
| `lng_dg1_dg2_last_priority` | explicit-hot-start probe: when RES, battery, LNG, and DG1 are insufficient but deficit is within LNG+DG1+DG2, DG2 should...<truncated 32 chars> | ✅ |
| `illegal_overload_all_thermal_and_battery_lack` | explicit-hot-start overload probe: when extreme demand exceeds all RES and thermal resources, the illegal overload compl...<truncated 108 chars> | ✅ |
| `forced_reclassification_from_default_zero_idle_to_res_charge` | default-init forced-transition probe: after the default initial cycle parks in ZeroIdle, nonzero load fully covered by R...<truncated 84 chars> | ✅ |
| `forced_reclassification_from_default_zero_idle_to_illegal_overload` | default-init forced-transition probe: after the default initial cycle parks in ZeroIdle, extreme demand beyond all RES a...<truncated 98 chars> | ✅ |
| `forced_reclassification_from_res_charge_to_dg2_mode` | explicit-hot-start forced-transition probe: from an already active RESCharge leaf, changed operating conditions requirin...<truncated 80 chars> | ✅ |
| `forced_reclassification_from_overload_to_zero_load_spare` | explicit-hot-start forced-transition probe: from the illegal overload leaf, zero load with positive RES and SoC at least...<truncated 107 chars> | ✅ |

#### 6.2 Scenario definitions

<details><summary>`default_init_zero_idle` — default-init probe: with zero load and no renewable production, the initial dispatch should land in ZeroIdle with no generation, battery power, spare power, or ...<truncated 14 chars></summary>

| Field | Value |
|---|---|
| description | default-init probe: with zero load and no renewable production, the initial dispatch should land in ZeroIdle with no generation, battery power, spare power, or load shedding. |
| initial_state | `<default-init>` |
| initial_vars | `{}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `initial_cycle_enters_zero_idle` | `0` | `[]` | `LNGShipEMS.ZeroIdle` | `{"Pbatt_charge": 0, "Pbatt_discharge": 0, "Pgen_req": 0, "Pspare": 0, "cmd_DG1_cut_in": 0, "cmd_DG1_cut_out": 1, "cmd_DG2_cut_in": 0, "cmd_DG2_cut_out": 1, "cmd_LNG_cut_in": 0, "cmd_LNG_cut_out": 1, "cmd_load_cut_in": 1, "cmd_load_cut_out": 0}` |

</details>

<details><summary>`zero_load_res_charges_battery_below_full_soc` — explicit-hot-start probe: with PL=0, positive RES, and SoC below 0.95, renewable production should be sent to battery charging.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start probe: with PL=0, positive RES, and SoC below 0.95, renewable production should be sent to battery charging. |
| initial_state | `LNGShipEMS.ZeroIdle` |
| initial_vars | `{"PL": 0, "Ppv": 8, "Pw": 2, "SoC": 0.94}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `zero_load_charge_selected` | `0` | `[]` | `LNGShipEMS.ZeroLoadCharge` | `{"Pbatt_charge": 10, "Pbatt_discharge": 0, "Pgen_req": 0, "Pspare": 0, "cmd_DG1_cut_in": 0, "cmd_DG2_cut_in": 0, "cmd_LNG_cut_in": 0, "cmd_load_cut_out": 0}` |

</details>

<details><summary>`zero_load_res_spare_at_full_soc_boundary` — explicit-hot-start boundary probe: with PL=0, positive RES, and SoC exactly 0.95, renewable production should become spare power rather than charging.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start boundary probe: with PL=0, positive RES, and SoC exactly 0.95, renewable production should become spare power rather than charging. |
| initial_state | `LNGShipEMS.ZeroLoadCharge` |
| initial_vars | `{"PL": 0, "Ppv": 8, "Pw": 2, "SoC": 0.95}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `zero_load_spare_selected_at_095` | `0` | `[]` | `LNGShipEMS.ZeroLoadSpare` | `{"Pbatt_charge": 0, "Pbatt_discharge": 0, "Pgen_req": 0, "Pspare": 10, "cmd_DG1_cut_in": 0, "cmd_DG2_cut_in": 0, "cmd_LNG_cut_in": 0, "cmd_load_cut_out": 0}` |

</details>

<details><summary>`res_covers_load_charges_battery_below_full_soc` — explicit-hot-start probe: when RES covers positive load and SoC is below 0.95, all load should be served from RES and residual RES should charge batteries.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start probe: when RES covers positive load and SoC is below 0.95, all load should be served from RES and residual RES should charge batteries. |
| initial_state | `LNGShipEMS.ZeroLoadSpare` |
| initial_vars | `{"PL": 10, "Ppv": 12, "Pw": 3, "SoC": 0.94}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `res_charge_selected_below_095` | `0` | `[]` | `LNGShipEMS.RESCharge` | `{"Pbatt_charge": 5, "Pbatt_discharge": 0, "Pgen_req": 0, "Pspare": 0, "cmd_DG1_cut_in": 0, "cmd_DG2_cut_in": 0, "cmd_LNG_cut_in": 0, "cmd_load_cut_out": 0}` |

</details>

<details><summary>`res_covers_load_spare_at_full_soc_boundary` — explicit-hot-start boundary probe: when RES covers positive load and SoC is exactly 0.95, residual RES should be spare power rather than battery charge.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start boundary probe: when RES covers positive load and SoC is exactly 0.95, residual RES should be spare power rather than battery charge. |
| initial_state | `LNGShipEMS.RESCharge` |
| initial_vars | `{"PL": 10, "Ppv": 12, "Pw": 3, "SoC": 0.95}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `res_spare_selected_at_095` | `0` | `[]` | `LNGShipEMS.RESSpare` | `{"Pbatt_charge": 0, "Pbatt_discharge": 0, "Pgen_req": 0, "Pspare": 5, "cmd_DG1_cut_in": 0, "cmd_DG2_cut_in": 0, "cmd_LNG_cut_in": 0, "cmd_load_cut_out": 0}` |

</details>

<details><summary>`battery_assist_at_soc_and_discharge_capacity_boundary` — explicit-hot-start boundary probe: with RES below load, SoC exactly 0.3, and deficit equal to battery discharge capacity, batteries should cover the deficit bef...<truncated 15 chars></summary>

| Field | Value |
|---|---|
| description | explicit-hot-start boundary probe: with RES below load, SoC exactly 0.3, and deficit equal to battery discharge capacity, batteries should cover the deficit before LNG or DGs. |
| initial_state | `LNGShipEMS.RESSpare` |
| initial_vars | `{"PL": 20, "Pbatt_dis_max": 10, "Pd1max": 20, "Pd2max": 20, "Ppv": 5, "Pw": 5, "SoC": 0.3, "eng3_Pmax": 50}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `battery_assist_selected_at_boundaries` | `0` | `[]` | `LNGShipEMS.BatteryAssist` | `{"Pbatt_charge": 0, "Pbatt_discharge": 10, "Pgen_req": 0, "Pspare": 0, "cmd_DG1_cut_in": 0, "cmd_DG2_cut_in": 0, "cmd_LNG_cut_in": 0, "cmd_load_cut_out": 0}` |

</details>

<details><summary>`lng_only_after_battery_capacity_exceeded` — explicit-hot-start boundary probe: when RES and battery are insufficient but deficit is exactly within LNG capacity, LNG alone should be cut in with requested g...<truncated 36 chars></summary>

| Field | Value |
|---|---|
| description | explicit-hot-start boundary probe: when RES and battery are insufficient but deficit is exactly within LNG capacity, LNG alone should be cut in with requested generator power equal to the deficit. |
| initial_state | `LNGShipEMS.BatteryAssist` |
| initial_vars | `{"PL": 40, "Pbatt_dis_max": 10, "Pd1max": 20, "Pd2max": 20, "Ppv": 10, "Pw": 0, "SoC": 0.3, "eng3_Pmax": 30}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `lng_only_selected_at_eng3_boundary` | `0` | `[]` | `LNGShipEMS.LNGOnlyNormal` | `{"Pbatt_charge": 0, "Pbatt_discharge": 0, "Pgen_req": 30, "Pspare": 0, "cmd_DG1_cut_in": 0, "cmd_DG2_cut_in": 0, "cmd_LNG_cut_in": 1, "cmd_LNG_cut_out": 0, "cmd_load_cut_out": 0}` |

</details>

<details><summary>`low_soc_lng_charge_margin` — explicit-hot-start low-SoC probe: when SoC is below 0.3 and LNG can cover deficit plus Pgmax/5 charging margin, LNG should both serve load and charge the batter...<truncated 2 chars></summary>

| Field | Value |
|---|---|
| description | explicit-hot-start low-SoC probe: when SoC is below 0.3 and LNG can cover deficit plus Pgmax/5 charging margin, LNG should both serve load and charge the battery. |
| initial_state | `LNGShipEMS.LNGOnlyNormal` |
| initial_vars | `{"PL": 40, "Pbatt_dis_max": 10, "Pd1max": 20, "Pd2max": 20, "Pgmax": 50, "Ppv": 10, "Pw": 0, "SoC": 0.29, "eng3_Pmax": 40}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `lng_low_soc_charge_selected` | `0` | `[]` | `LNGShipEMS.LNGChargeLowSoC` | `{"Pbatt_charge": 10, "Pbatt_discharge": 0, "Pgen_req": 40, "Pspare": 0, "cmd_DG1_cut_in": 0, "cmd_DG2_cut_in": 0, "cmd_LNG_cut_in": 1, "cmd_load_cut_out": 0}` |

</details>

<details><summary>`lng_dg1_normal_after_lng_capacity_exceeded` — explicit-hot-start boundary probe: with suitable SoC and deficit above LNG capacity but within LNG plus DG1, LNG and DG1 should be cut in while DG2 remains out.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start boundary probe: with suitable SoC and deficit above LNG capacity but within LNG plus DG1, LNG and DG1 should be cut in while DG2 remains out. |
| initial_state | `LNGShipEMS.LNGChargeLowSoC` |
| initial_vars | `{"PL": 70, "Pbatt_dis_max": 10, "Pd1max": 20, "Pd2max": 30, "Ppv": 10, "Pw": 0, "SoC": 0.3, "eng3_Pmax": 40}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `lng_dg1_selected_at_dg1_boundary` | `0` | `[]` | `LNGShipEMS.LNGDG1Normal` | `{"Pbatt_charge": 0, "Pbatt_discharge": 0, "Pgen_req": 60, "Pspare": 0, "cmd_DG1_cut_in": 1, "cmd_DG1_cut_out": 0, "cmd_DG2_cut_in": 0, "cmd_LNG_cut_in": 1, "cmd_LNG_cut_out": 0, "cmd_load_cut_out": 0}` |

</details>

<details><summary>`low_soc_lng_dg1_charge_margin` — explicit-hot-start low-SoC probe: when LNG alone cannot cover the low-SoC charging case, DG1 should be added and Pd1max/10 should be requested for battery charg...<truncated 4 chars></summary>

| Field | Value |
|---|---|
| description | explicit-hot-start low-SoC probe: when LNG alone cannot cover the low-SoC charging case, DG1 should be added and Pd1max/10 should be requested for battery charging. |
| initial_state | `LNGShipEMS.LNGDG1Normal` |
| initial_vars | `{"PL": 70, "Pbatt_dis_max": 10, "Pd1max": 200, "Pd2max": 30, "Pgmax": 50, "Ppv": 10, "Pw": 0, "SoC": 0.29, "eng3_Pmax": 40}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `lng_dg1_low_soc_charge_selected` | `0` | `[]` | `LNGShipEMS.LNGDG1ChargeLowSoC` | `{"Pbatt_charge": 20, "Pbatt_discharge": 0, "Pgen_req": 80, "Pspare": 0, "cmd_DG1_cut_in": 1, "cmd_DG2_cut_in": 0, "cmd_LNG_cut_in": 1, "cmd_load_cut_out": 0}` |

</details>

<details><summary>`lng_dg1_dg2_last_priority` — explicit-hot-start probe: when RES, battery, LNG, and DG1 are insufficient but deficit is within LNG+DG1+DG2, DG2 should be cut in as the last priority.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start probe: when RES, battery, LNG, and DG1 are insufficient but deficit is within LNG+DG1+DG2, DG2 should be cut in as the last priority. |
| initial_state | `LNGShipEMS.LNGDG1ChargeLowSoC` |
| initial_vars | `{"PL": 100, "Pbatt_dis_max": 10, "Pd1max": 20, "Pd2max": 30, "Ppv": 10, "Pw": 0, "SoC": 0.3, "eng3_Pmax": 40}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `all_thermal_with_dg2_selected` | `0` | `[]` | `LNGShipEMS.LNGDG1DG2` | `{"Pbatt_charge": 0, "Pbatt_discharge": 0, "Pgen_req": 90, "Pspare": 0, "cmd_DG1_cut_in": 1, "cmd_DG2_cut_in": 1, "cmd_DG2_cut_out": 0, "cmd_LNG_cut_in": 1, "cmd_load_cut_out": 0}` |

</details>

<details><summary>`illegal_overload_all_thermal_and_battery_lack` — explicit-hot-start overload probe: when extreme demand exceeds all RES and thermal resources, the illegal overload completion state should activate all thermal ...<truncated 68 chars></summary>

| Field | Value |
|---|---|
| description | explicit-hot-start overload probe: when extreme demand exceeds all RES and thermal resources, the illegal overload completion state should activate all thermal units, cover the remaining lack by battery discharge, and shed load. |
| initial_state | `LNGShipEMS.LNGDG1DG2` |
| initial_vars | `{"PL": 130, "Pbatt_dis_max": 10, "Pd1max": 20, "Pd2max": 30, "Ppv": 10, "Pw": 0, "SoC": 0.3, "eng3_Pmax": 40}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `illegal_overload_selected` | `0` | `[]` | `LNGShipEMS.IllegalOverloadAllThermalBattery` | `{"Pbatt_charge": 0, "Pbatt_discharge": 30, "Pgen_req": 90, "Pspare": 0, "cmd_DG1_cut_in": 1, "cmd_DG2_cut_in": 1, "cmd_LNG_cut_in": 1, "cmd_load_cut_in": 0, "cmd_load_cut_out": 1}` |

</details>

<details><summary>`forced_reclassification_from_default_zero_idle_to_res_charge` — default-init forced-transition probe: after the default initial cycle parks in ZeroIdle, nonzero load fully covered by RES with SoC below 0.95 must be globally ...<truncated 44 chars></summary>

| Field | Value |
|---|---|
| description | default-init forced-transition probe: after the default initial cycle parks in ZeroIdle, nonzero load fully covered by RES with SoC below 0.95 must be globally reclassified to RESCharge on the next cycle. |
| initial_state | `<default-init>` |
| initial_vars | `{"PL": 10, "Ppv": 12, "Pw": 3, "SoC": 0.94}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `default_initial_dispatch_to_zero_idle` | `0` | `[]` | `LNGShipEMS.ZeroIdle` | `{}` |
| 1 `forced_guard_reclassifies_to_res_charge` | `0` | `[]` | `LNGShipEMS.RESCharge` | `{"Pbatt_charge": 5, "Pbatt_discharge": 0, "Pgen_req": 0, "Pspare": 0, "cmd_DG1_cut_in": 0, "cmd_DG1_cut_out": 1, "cmd_DG2_cut_in": 0, "cmd_DG2_cut_out": 1, "cmd_LNG_cut_in": 0, "cmd_LNG_cut_out": 1, "cmd_load_cut_in": 1, "cmd_load_cut_out": 0}` |

</details>

<details><summary>`forced_reclassification_from_default_zero_idle_to_illegal_overload` — default-init forced-transition probe: after the default initial cycle parks in ZeroIdle, extreme demand beyond all RES and thermal capacity must be globally rec...<truncated 58 chars></summary>

| Field | Value |
|---|---|
| description | default-init forced-transition probe: after the default initial cycle parks in ZeroIdle, extreme demand beyond all RES and thermal capacity must be globally reclassified to the illegal overload state on the next cycle. |
| initial_state | `<default-init>` |
| initial_vars | `{"PL": 130, "Pbatt_dis_max": 10, "Pd1max": 20, "Pd2max": 30, "Ppv": 10, "Pw": 0, "SoC": 0.3, "eng3_Pmax": 40}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `default_initial_dispatch_to_zero_idle` | `0` | `[]` | `LNGShipEMS.ZeroIdle` | `{}` |
| 1 `forced_guard_reclassifies_to_illegal_overload` | `0` | `[]` | `LNGShipEMS.IllegalOverloadAllThermalBattery` | `{"Pbatt_charge": 0, "Pbatt_discharge": 30, "Pgen_req": 90, "Pspare": 0, "cmd_DG1_cut_in": 1, "cmd_DG1_cut_out": 0, "cmd_DG2_cut_in": 1, "cmd_DG2_cut_out": 0, "cmd_LNG_cut_in": 1, "cmd_LNG_cut_out": 0, "cmd_load_cut_in": 0, "cmd_load_cut_out": 1}` |

</details>

<details><summary>`forced_reclassification_from_res_charge_to_dg2_mode` — explicit-hot-start forced-transition probe: from an already active RESCharge leaf, changed operating conditions requiring LNG+DG1+DG2 must be globally reclassif...<truncated 40 chars></summary>

| Field | Value |
|---|---|
| description | explicit-hot-start forced-transition probe: from an already active RESCharge leaf, changed operating conditions requiring LNG+DG1+DG2 must be globally reclassified rather than staying in the old mode. |
| initial_state | `LNGShipEMS.RESCharge` |
| initial_vars | `{"PL": 100, "Pbatt_dis_max": 10, "Pd1max": 20, "Pd2max": 30, "Ppv": 10, "Pw": 0, "SoC": 0.3, "eng3_Pmax": 40}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `forced_guard_reclassifies_to_lng_dg1_dg2` | `0` | `[]` | `LNGShipEMS.LNGDG1DG2` | `{"Pbatt_charge": 0, "Pbatt_discharge": 0, "Pgen_req": 90, "Pspare": 0, "cmd_DG1_cut_in": 1, "cmd_DG1_cut_out": 0, "cmd_DG2_cut_in": 1, "cmd_DG2_cut_out": 0, "cmd_LNG_cut_in": 1, "cmd_LNG_cut_out": 0, "cmd_load_cut_in": 1, "cmd_load_cut_out": 0}` |

</details>

<details><summary>`forced_reclassification_from_overload_to_zero_load_spare` — explicit-hot-start forced-transition probe: from the illegal overload leaf, zero load with positive RES and SoC at least 0.95 must be globally reclassified to Z...<truncated 67 chars></summary>

| Field | Value |
|---|---|
| description | explicit-hot-start forced-transition probe: from the illegal overload leaf, zero load with positive RES and SoC at least 0.95 must be globally reclassified to ZeroLoadSpare, proving forced guards recover from any concrete mode. |
| initial_state | `LNGShipEMS.IllegalOverloadAllThermalBattery` |
| initial_vars | `{"PL": 0, "Pbatt_dis_max": 10, "Pd1max": 20, "Pd2max": 30, "Ppv": 8, "Pw": 2, "SoC": 0.95, "eng3_Pmax": 40}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `forced_guard_recovers_to_zero_load_spare` | `0` | `[]` | `LNGShipEMS.ZeroLoadSpare` | `{"Pbatt_charge": 0, "Pbatt_discharge": 0, "Pgen_req": 0, "Pspare": 10, "cmd_DG1_cut_in": 0, "cmd_DG1_cut_out": 1, "cmd_DG2_cut_in": 0, "cmd_DG2_cut_out": 1, "cmd_LNG_cut_in": 0, "cmd_LNG_cut_out": 1, "cmd_load_cut_in": 1, "cmd_load_cut_out": 0}` |

</details>


### 7. Repair / blocking feedback 明细

- 本 run 未进入 `SD-8/SL-9/SL-10` repair block；通常表示流程在 repair 前已成功、被 provider/schema 错误中断，或在 pre-repair 阶段直接退出。

### 8. 尝试记录与成本

- `SL-1`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 5897, 'completion_chars': 19601, 'completion_tokens': 7843, 'elapsed_seconds': 144.0797747040051, 'estimated_completion_tokens': 4901, 'estimated_prompt_tokens': 6646, 'estimated_total_tokens': 11547, 'first_chunk_seconds': 37.796556725981645, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 26582, 'prompt_tokens': 6469, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 14312}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 3434, 'completion_chars': 11909, 'completion_tokens': 4471, 'elapsed_seconds': 82.9552443959983, 'estimated_completion_tokens': 2978, 'estimated_prompt_tokens': 15723, 'estimated_total_tokens': 18701, 'first_chunk_seconds': 23.108589836978354, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 62889, 'prompt_tokens': 16682, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 21153}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 2952, 'completion_chars': 9747, 'completion_tokens': 3471, 'elapsed_seconds': 65.18610518900095, 'estimated_completion_tokens': 2437, 'estimated_prompt_tokens': 18865, 'estimated_total_tokens': 21302, 'first_chunk_seconds': 13.073469503986416, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 75457, 'prompt_tokens': 20235, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 23706}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 4897, 'completion_chars': 17169, 'completion_tokens': 5416, 'elapsed_seconds': 101.7040383759886, 'estimated_completion_tokens': 4293, 'estimated_prompt_tokens': 19565, 'estimated_total_tokens': 23858, 'first_chunk_seconds': 12.399578518001363, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 78260, 'prompt_tokens': 20988, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 26404}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-7`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1712, 'completion_chars': 7833, 'completion_tokens': 2749, 'elapsed_seconds': 52.38402196101379, 'estimated_completion_tokens': 1959, 'estimated_prompt_tokens': 41762, 'estimated_total_tokens': 43721, 'first_chunk_seconds': 21.39768795101554, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 167046, 'prompt_tokens': 47659, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 50408}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。

### 9. 最终停止状态与后续含义

- 停止状态：verdict=`success`，record_status=`success`。
- 主要原因分类：`success_but_weak_oracle_ineligible`。
- required stages executed：`16/12`，missing=`<none>`。
- repairs：`0/0` accepted；scenario_history=`3`。
- 配置含义：`recommended baseline candidate`；该结果可用于评估默认入口本身。
- 主结果/蓝本边界：`main_result_eligible` 只表示该 run 非 provider-invalid 且 trace/schema/secret/final-verdict 口径可进入主结果候选；`path2_ref_model_blueprint_eligible=false` 时，模型仍可作为 FE/BVS 或 dispatch-classifier 压力测试证据，但不得称为 Path2 ref-model 主蓝本。
- 样本含义：若出现 `design_or_variable_dynamics`，应重点审查变量是否仅作为 guard/input 常量而没有事件/动作更新；若出现 pre-scenario parse/semantic 失败，则应先优化 pyfcstm grammar adherence。
