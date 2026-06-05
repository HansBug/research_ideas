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
| LoopConfig 摘要 | `condition_id=full_staged_v1`, `max_iterations=5`, `llm_max_retries=2`, `scenario_max_retries=2`, `model_review_mode=blocking_major_only`, `repair_review_mode=blocking_major_only` |
| Git commit | `4304eb65692c6576b81986b4f1208ed818c4be26` |
| clean / diff / prompt snapshot | clean=`True`, dirty=`False`, diff_hash=`sha256:2a69ad5797ac568a81bddcef615104303a97261094685f4edd8d4484e889ea09`, prompt_hash=`sha256:e2cfdd7ab1fd43540a75a5216158706cc6809d0eb975e3731e90124b8a1ff158` |
| provider/model 脱敏标识 | mode=`real_env`, model=`gpt-5.5`, real_api=`True` |
| source / paper | source=`project_1_llm_state_machine_modeling/sources/state-transitions-logical-design-for-hybrid-energy-generation-with-renewable-energy-sources-in-lng-ship`, paper=`project_1_llm_state_machine_modeling/sources/state-transitions-logical-design-for-hybrid-energy-generation-with-renewable-energy-sources-in-lng-ship/paper.pdf` |
| 样本筛选理由 | issue #14 / PR-D 代表性 Path2 EFSM，变量、guard、12 个状态和非法状态都明确；但它可能退化为条件分类式 dispatch，因此更适合作为 FE/BVS 压力测试，是否适合作为 Path2 ref-model 蓝本需看最终 DSL 是否具有 state-dependent mode memory。 |
| 变量参与说明 | `PL/Ppv/Pw/SoC/eng*_Pmax` 是环境输入/容量边界，适合暴露 SD-4 对外部输入变量的处理能力。 |
| run_id | `pr-e1-path2_lng_ems-default-lg-b1-waiver-4304eb65-79654f17` |
| final verdict/status | verdict=`success`, record=`success`, result=`converged` |
| main_result_eligible | `true` |
| state_mode_decorative_detected | `true` |
| path2_ref_model_blueprint_eligible | `false`；state_mode_decorative: final DSL is dominated by root-level forced guard reclassification; valid as FE/BVS or dispatch-classifier stress evidence, but not a Path2 ref-model blueprint |
| final.fcstm 来源 | `{"final_dsl_hash": "sha256:1d80d7eae005c34773c326cd018af9662fe914a8c85b7fe6f64489b305335edf", "source_kind": "initial_or_unrepaired"}` |
| FixLog next_action 序列 | `<none>` |
| iteration exit_reason 序列 | `full_pass_all_required_feedback_ok` |
| token/cost/time | tokens=`{'prompt_tokens': 95801, 'completion_tokens': 17963, 'total_tokens': 113764, 'estimated_prompt_tokens': 86746, 'estimated_completion_tokens': 11306, 'estimated_total_tokens': 98052, 'prompt_chars': 346978, 'completion_chars': 45221, 'n_calls': 4, 'token_usage_available': True, 'token_usage_unavailable_calls': 0}`, elapsed=`335.857s` |
| run record | [`pr-e1-path2_lng_ems-default-lg-b1-waiver-4304eb65-79654f17.agent_loop.json.gz`](./pr-e1-path2_lng_ems-default-lg-b1-waiver-4304eb65-79654f17.agent_loop.json.gz) |
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
| `graph_config_hash` | `sha256:a314e7cff8c31f79129c7ed4d04607277cccf133bb12ac7ce1cd1898aededeb7` |
| `node_edge_schema_version` | `pr-langgraph.stage-nodes.v1` |
| `checkpoint_backend` | `memory` |
| `checkpoint_backend_type` | `InMemorySaver` |
| `checkpoint_serde` | `pickle` |
| `checkpoint_path_hash` | `sha256:memory` |
| `resumed_from_checkpoint` | `False` |
| `resume_checkpoint_id_hash` | `None` |
| `instrumentation_layer` | `langgraph` |
| `stage_semantics_module` | `method.staged_runtime` |
| `langgraph_node_trace_count` | `18` |
| `langgraph_node_trace_hash` | `sha256:550677296248593e992beaec225ade90d235784e83d89c1794dbc8f3f908dbf5` |
| `langgraph_compat_ok` | `True` |
| `checkpoint_resume_smoke_scope` | `toy_ledger_langgraph_api_smoke` |
| `real_agent_loop_resume_supported` | `False` |
| `resume_append_only` | `True` |
| `final_trace_delegated_monolithic_runtime` | `False` |
| `final_trace_node_trace_count` | `18` |

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
def float Pbat_Pmax = 0.0;
def float Pg_req = 0.0;
def float Pbat_discharge = 0.0;
def float Pbat_charge = 0.0;
def float Pspare = 0.0;
def int cmd_LNG = 0;
def int cmd_DG1 = 0;
def int cmd_DG2 = 0;
def int cmd_load_cutin = 0;
def int cmd_load_cutout = 0;

state LNGShipEMS {
    ! * -> ZeroLoadCharge : if [PL == 0 && SoC < 0.95];
    ! * -> ZeroLoadSpare : if [PL == 0 && SoC >= 0.95];
    ! * -> RESCoversCharge : if [PL > 0 && Ppv + Pw >= PL && SoC < 0.95];
    ! * -> RESCoversSpare : if [PL > 0 && Ppv + Pw >= PL && SoC >= 0.95];
    ! * -> BatteryDischarge : if [PL > 0 && Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw <= Pbat_Pmax];
    ! * -> LNGWithChargeMargin : if [PL > 0 && Ppv + Pw < PL && SoC < 0.2 && PL - Ppv - Pw + Pgmax / 5 <= eng3_Pmax];
    ! * -> LNGOnly : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw <= eng3_Pmax && (SoC < 0.2 || PL - Ppv - Pw > Pbat_Pmax) && (SoC >= 0.2 || PL - Ppv - Pw + Pgmax / 5 > eng3_Pmax)];
    ! * -> LNGBattery : if [PL > 0 && Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw > eng3_Pmax && PL - Ppv - Pw <= eng3_Pmax + Pbat_Pmax];
    ! * -> LNGDG1WithChargeMargin : if [PL > 0 && Ppv + Pw < PL && SoC < 0.2 && PL - Ppv - Pw > eng3_Pmax && PL - Ppv - Pw + Pd1max / 10 <= eng3_Pmax + Pd1max];
    ! * -> LNGDG1 : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > eng3_Pmax && PL - Ppv - Pw <= eng3_Pmax + Pd1max && (SoC >= 0.2 || PL - Ppv - Pw + Pd1max / 10 > eng3_Pmax + Pd1max) && (SoC < 0.2 || PL - Ppv - Pw > eng3_Pmax + Pbat_Pmax)];
    ! * -> AllThermal : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > eng3_Pmax + Pd1max && PL - Ppv - Pw <= eng3_Pmax + Pd1max + Pd2max];
    ! * -> OverloadBatteryCover : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > eng3_Pmax + Pd1max + Pd2max];

    [*] -> ZeroLoadCharge;

    state ZeroLoadCharge {
        during {
            Pg_req = 0.0;
            Pbat_discharge = 0.0;
            Pbat_charge = Ppv + Pw;
            Pspare = 0.0;
            cmd_LNG = 0;
            cmd_DG1 = 0;
            cmd_DG2 = 0;
            cmd_load_cutin = 1;
            cmd_load_cutout = 0;
        }
    }

    state ZeroLoadSpare {
        during {
            Pg_req = 0.0;
            Pbat_discharge = 0.0;
            Pbat_charge = 0.0;
            Pspare = Ppv + Pw;
            cmd_LNG = 0;
            cmd_DG1 = 0;
            cmd_DG2 = 0;
            cmd_load_cutin = 1;
            cmd_load_cutout = 0;
        }
    }

    state RESCoversCharge {
        during {
            Pg_req = 0.0;
            Pbat_discharge = 0.0;
            Pbat_charge = Ppv + Pw - PL;
            Pspare = 0.0;
            cmd_LNG = 0;
            cmd_DG1 = 0;
            cmd_DG2 = 0;
            cmd_load_cutin = 1;
            cmd_load_cutout = 0;
        }
    }

    state RESCoversSpare {
        during {
            Pg_req = 0.0;
            Pbat_discharge = 0.0;
            Pbat_charge = 0.0;
            Pspare = Ppv + Pw - PL;
            cmd_LNG = 0;
            cmd_DG1 = 0;
            cmd_DG2 = 0;
            cmd_load_cutin = 1;
            cmd_load_cutout = 0;
        }
    }

    state BatteryDischarge {
        during {
            Pg_req = 0.0;
            Pbat_discharge = PL - Ppv - Pw;
            Pbat_charge = 0.0;
            Pspare = 0.0;
            cmd_LNG = 0;
            cmd_DG1 = 0;
            cmd_DG2 = 0;
            cmd_load_cutin = 1;
            cmd_load_cutout = 0;
        }
    }

    state LNGWithChargeMargin {
        during {
            Pg_req = PL - Ppv - Pw + Pgmax / 5;
            Pbat_discharge = 0.0;
            Pbat_charge = Pgmax / 5;
            Pspare = 0.0;
            cmd_LNG = 1;
            cmd_DG1 = 0;
            cmd_DG2 = 0;
            cmd_load_cutin = 1;
            cmd_load_cutout = 0;
        }
    }

    state LNGOnly {
        during {
            Pg_req = PL - Ppv - Pw;
            Pbat_discharge = 0.0;
            Pbat_charge = 0.0;
            Pspare = 0.0;
            cmd_LNG = 1;
            cmd_DG1 = 0;
            cmd_DG2 = 0;
            cmd_load_cutin = 1;
            cmd_load_cutout = 0;
        }
    }

    state LNGBattery {
        during {
            Pg_req = eng3_Pmax;
            Pbat_discharge = PL - Ppv - Pw - eng3_Pmax;
            Pbat_charge = 0.0;
            Pspare = 0.0;
            cmd_LNG = 1;
            cmd_DG1 = 0;
            cmd_DG2 = 0;
            cmd_load_cutin = 1;
            cmd_load_cutout = 0;
        }
    }

    state LNGDG1WithChargeMargin {
        during {
            Pg_req = PL - Ppv - Pw + Pd1max / 10;
            Pbat_discharge = 0.0;
            Pbat_charge = Pd1max / 10;
            Pspare = 0.0;
            cmd_LNG = 1;
            cmd_DG1 = 1;
            cmd_DG2 = 0;
            cmd_load_cutin = 1;
            cmd_load_cutout = 0;
        }
    }

    state LNGDG1 {
        during {
            Pg_req = PL - Ppv - Pw;
            Pbat_discharge = 0.0;
            Pbat_charge = 0.0;
            Pspare = 0.0;
            cmd_LNG = 1;
            cmd_DG1 = 1;
            cmd_DG2 = 0;
            cmd_load_cutin = 1;
            cmd_load_cutout = 0;
        }
    }

    state AllThermal {
        during {
            Pg_req = PL - Ppv - Pw;
            Pbat_discharge = 0.0;
            Pbat_charge = 0.0;
            Pspare = 0.0;
            cmd_LNG = 1;
            cmd_DG1 = 1;
            cmd_DG2 = 1;
            cmd_load_cutin = 1;
            cmd_load_cutout = 0;
        }
    }

    state OverloadBatteryCover {
        during {
            Pg_req = eng3_Pmax + Pd1max + Pd2max;
            Pbat_discharge = PL - Ppv - Pw - eng3_Pmax - Pd1max - Pd2max;
            Pbat_charge = 0.0;
            Pspare = 0.0;
            cmd_LNG = 1;
            cmd_DG1 = 1;
            cmd_DG2 = 1;
            cmd_load_cutin = 1;
            cmd_load_cutout = 0;
        }
    }
}

```

### 4. 全流程真实摘要表

| Stage | 是否 LLM | iteration | 结果 | 获取的信息 / 反馈 | 本阶段做了什么 | DSL 修改 | artifact/log |
|---|---:|---:|---:|---|---|---|---|
| `SC-0` | 否 | - | ✅ | trace/control | 初始化 run state | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-waiver-4304eb65-79654f17.agent_loop.json.gz) |
| `SL-1` | 是 | - | ✅ | LLM calls=1, tokens=14139 | 生成初始 DSL 与 grounding seeds | initial len=5979 | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-waiver-4304eb65-79654f17.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-waiver-4304eb65-79654f17.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-waiver-4304eb65-79654f17.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=263, info=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-waiver-4304eb65-79654f17.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=2, tokens=42603 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-waiver-4304eb65-79654f17.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-waiver-4304eb65-79654f17.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=2, tokens=42603 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-waiver-4304eb65-79654f17.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-waiver-4304eb65-79654f17.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-waiver-4304eb65-79654f17.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-waiver-4304eb65-79654f17.agent_loop.json.gz) |
| `SL-7` | 是 | 0 | ✅ | LLM calls=1, tokens=57022 | LLM model review | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-waiver-4304eb65-79654f17.agent_loop.json.gz) |
| `SC-12` | 否 | - | ✅ | full_pass_all_required_feedback_ok | 写 final verdict | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-waiver-4304eb65-79654f17.agent_loop.json.gz) |
| `SC-13` | 否 | - | ✅ | trace/control | 写审计 run record | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-waiver-4304eb65-79654f17.agent_loop.json.gz) |

### 4.1 完整流程日志（stage/control-flow replay ledger）

口径：本节来自 `AgentLoopRunRecord.logs`，与 [`flow_log.json`](./flow_log.json) 一致；用于复现每个 stage 如何进入、得到什么批示、跳转到哪里，以及每次 DSL 产物/候选如何变化。

| # | ts | stage | iter | event | result / jump | DSL evidence |
|---:|---|---|---:|---|---|---|
| 1 | `2026-06-05T10:34:52Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 2 | `2026-06-05T10:34:52Z` | `SC-0` | `-` | `run_start` | {} | <none> |
| 3 | `2026-06-05T10:34:52Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 4 | `2026-06-05T10:34:52Z` | `SL-1` | `-` | `stage_enter` | {"reason": "initial_modeling_adapter_available"} | <none> |
| 5 | `2026-06-05T10:37:12Z` | `SL-1` | `-` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 6 | `2026-06-05T10:37:12Z` | `SL-1` | `-` | `stage_result` | {"jump": "SD-2", "ok": true} | candidate_dsl:len=5979,hash=sha256:1d80d7eae005 |
| 7 | `2026-06-05T10:37:12Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 8 | `2026-06-05T10:37:12Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 9 | `2026-06-05T10:37:12Z` | `<control>` | `0` | `iteration_enter` | {} | current_hash=sha256:1d80d7eae005c34773c326cd018af9662fe914a8c85b7fe6f64489b305335edf |
| 10 | `2026-06-05T10:37:12Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 11 | `2026-06-05T10:37:12Z` | `<control>` | `0` | `iteration_validation_enter` | {} | dsl:len=5979,hash=sha256:1d80d7eae005, current_hash=sha256:1d80d7eae005c34773c326cd018af9662fe914a8c85b7fe6f64489b305335edf |
| 12 | `2026-06-05T10:37:12Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 13 | `2026-06-05T10:37:12Z` | `SD-2` | `0` | `stage_enter` | {"reason": "full_validation_pass"} | <none> |
| 14 | `2026-06-05T10:37:12Z` | `SD-2` | `0` | `stage_result` | {"jump": "SD-3", "ok": true, "status": "StageStatus.OK"} | <none> |
| 15 | `2026-06-05T10:37:12Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 16 | `2026-06-05T10:37:12Z` | `SD-3` | `0` | `stage_enter` | {"reason": "SD-2 ok"} | <none> |
| 17 | `2026-06-05T10:37:12Z` | `SD-3` | `0` | `stage_result` | {"jump": "SD-4", "ok": true, "status": "StageStatus.OK"} | <none> |
| 18 | `2026-06-05T10:37:12Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 19 | `2026-06-05T10:37:12Z` | `SD-4` | `0` | `stage_enter` | {"reason": "SD-3 ok"} | <none> |
| 20 | `2026-06-05T10:37:12Z` | `SD-4` | `0` | `stage_result` | {"jump": "SL-5", "ok": true, "status": "StageStatus.OK"} | <none> |
| 21 | `2026-06-05T10:37:12Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 22 | `2026-06-05T10:37:12Z` | `SL-5` | `0` | `stage_enter` | {"reason": "scenario_set_absent"} | <none> |
| 23 | `2026-06-05T10:38:42Z` | `SL-5` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 24 | `2026-06-05T10:38:42Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 25 | `2026-06-05T10:38:42Z` | `SD-5A` | `0` | `stage_result` | {"jump": "SL-5 retry", "ok": false, "status": "StageStatus.ADVISORY"} | <none> |
| 26 | `2026-06-05T10:38:42Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 27 | `2026-06-05T10:38:42Z` | `SL-5` | `0` | `stage_enter` | {"reason": "scenario_coverage_gap_retry"} | <none> |
| 28 | `2026-06-05T10:39:38Z` | `SL-5` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 29 | `2026-06-05T10:39:38Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 30 | `2026-06-05T10:39:38Z` | `SD-5A` | `0` | `stage_result` | {"jump": "SC-5F", "ok": true, "status": "StageStatus.OK"} | <none> |
| 31 | `2026-06-05T10:39:38Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 32 | `2026-06-05T10:39:38Z` | `SC-5F` | `0` | `stage_result` | {"jump": "SD-6", "ok": true, "reason": null} | <none> |
| 33 | `2026-06-05T10:39:38Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 34 | `2026-06-05T10:39:38Z` | `SD-6` | `0` | `stage_enter` | {"reason": "scenario_set_ready"} | <none> |
| 35 | `2026-06-05T10:39:38Z` | `SD-6` | `0` | `stage_result` | {"jump": "SL-7", "ok": true, "status": "StageStatus.OK"} | <none> |
| 36 | `2026-06-05T10:39:38Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 37 | `2026-06-05T10:39:38Z` | `SL-7` | `0` | `stage_enter` | {"reason": "SD-6 ok"} | <none> |
| 38 | `2026-06-05T10:40:27Z` | `SL-7` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 39 | `2026-06-05T10:40:27Z` | `SL-7` | `0` | `stage_result` | {"jump": "SC-12 success", "ok": true, "status": "StageStatus.OK"} | <none> |
| 40 | `2026-06-05T10:40:27Z` | `SL-7` | `0` | `grounding_update_hints_recorded` | {} | <none> |
| 41 | `2026-06-05T10:40:27Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 42 | `2026-06-05T10:40:27Z` | `<control>` | `0` | `iteration_validation_result` | {"jump": "SC-12 success", "selected_feedback": null} | <none> |
| 43 | `2026-06-05T10:40:27Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 44 | `2026-06-05T10:40:27Z` | `SC-12` | `-` | `sc12_verdict` | {"reason": "full_pass_all_required_feedback_ok", "verdict": "success"} | final_dsl:len=5979,hash=sha256:1d80d7eae005 |
| 45 | `2026-06-05T10:40:27Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 46 | `2026-06-05T10:40:27Z` | `SC-13` | `-` | `run_end` | {"verdict": "success"} | final_dsl:len=5979,hash=sha256:1d80d7eae005 |
| 47 | `` | `<control>` | `-` | `langgraph_node_trace` | {} | <none> |
| 48 | `` | `<control>` | `-` | `lg_d1_operator_log_artifacts` | {} | <none> |

### 5. Iteration / repair / review 摘要

| Iter | selected feedback | repair? | FixRequestBatch | SL-9 | local checks | SL-10 | 回到 SD-2? | verdict/备注 |
|---:|---|---|---|---|---|---|---|---|
| 0 | `<none>` | no | <none> | <none> | <none> | <none> | no | full_pass_all_required_feedback_ok |

### 6. Scenario 明细与逐轮通过情况

#### 6.1 Scenario pass/fail by iteration

口径：`✅` = 该 scenario 在该轮 SD-6 simulation 通过；`❌` = 该轮失败；`⚪` = 该轮未执行或无该 scenario 结果。

| Scenario | Intent | Iter 1 |
|---|---|---|
| `default_init_zero_load_charge` | default-init: with default PL=0 and SoC below 0.95, EMS initializes/selects zero-load battery charging from available RE...<truncated 2 chars> | ✅ |
| `zero_load_soc_full_spare_boundary` | explicit-hot-start: at the SoC=0.95 boundary with PL=0, RES production should go to spare rather than battery charging. | ✅ |
| `res_covers_charge_below_full_soc` | explicit-hot-start: when renewable power exceeds load and SoC is below 0.95, all load is RES-served and residual RES cha...<truncated 17 chars> | ✅ |
| `res_covers_spare_at_full_soc_boundary` | explicit-hot-start: at SoC=0.95 with renewable power exceeding load, residual RES should be treated as spare power. | ✅ |
| `battery_discharge_at_low_soc_boundary` | explicit-hot-start: when RES is below load, SoC exactly 0.2 is suitable for battery use and deficit within battery capac...<truncated 18 chars> | ✅ |
| `low_soc_lng_charge_margin` | explicit-hot-start: with SoC below 0.2, LNG should cover the RES deficit plus the Pgmax/5 charging margin when within LN...<truncated 11 chars> | ✅ |
| `lng_only_when_battery_capacity_insufficient` | explicit-hot-start: with suitable SoC but battery capacity insufficient and LNG capacity enough, LNG alone should be cut...<truncated 18 chars> | ✅ |
| `lng_battery_when_deficit_exceeds_lng` | explicit-hot-start: with suitable SoC and deficit above LNG capacity but within LNG plus battery capacity, dispatch LNG ...<truncated 22 chars> | ✅ |
| `low_soc_lng_dg1_charge_margin` | explicit-hot-start: with low SoC and deficit above LNG, LNG plus DG1 should include the Pd1max/10 charging margin when w...<truncated 15 chars> | ✅ |
| `lng_dg1_without_battery_or_margin` | explicit-hot-start: when deficit exceeds LNG and battery contribution is not enough, but fits LNG plus DG1, DG1 is cut i...<truncated 14 chars> | ✅ |
| `all_thermal_dg2_last_priority` | explicit-hot-start: when deficit exceeds LNG plus DG1 but is within LNG plus DG1 plus DG2, all thermal units including D...<truncated 14 chars> | ✅ |
| `overload_battery_cover_extreme_demand` | explicit-hot-start: for extreme demand beyond all RES and thermal resources, all thermal units are activated and remaini...<truncated 40 chars> | ✅ |
| `forced_reselect_to_zero_load_charge_from_overload` | explicit-hot-start: from a nonzero dispatch leaf, the global forced guard for PL=0 and SoC<0.95 must reselect ZeroLoadCh...<truncated 53 chars> | ✅ |

#### 6.2 Scenario definitions

<details><summary>`default_init_zero_load_charge` — default-init: with default PL=0 and SoC below 0.95, EMS initializes/selects zero-load battery charging from available RES.</summary>

| Field | Value |
|---|---|
| description | default-init: with default PL=0 and SoC below 0.95, EMS initializes/selects zero-load battery charging from available RES. |
| initial_state | `<default-init>` |
| initial_vars | `{"Ppv": 12.0, "Pw": 8.0, "SoC": 0.5}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `zero_load_charge_selected` | `0` | `[]` | `LNGShipEMS.ZeroLoadCharge` | `{"Pbat_charge": 20.0, "Pbat_discharge": 0.0, "Pg_req": 0.0, "Pspare": 0.0, "cmd_DG1": 0, "cmd_DG2": 0, "cmd_LNG": 0, "cmd_load_cutin": 1}` |

</details>

<details><summary>`zero_load_soc_full_spare_boundary` — explicit-hot-start: at the SoC=0.95 boundary with PL=0, RES production should go to spare rather than battery charging.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: at the SoC=0.95 boundary with PL=0, RES production should go to spare rather than battery charging. |
| initial_state | `LNGShipEMS.ZeroLoadCharge` |
| initial_vars | `{"PL": 0.0, "Ppv": 30.0, "Pw": 20.0, "SoC": 0.95}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `zero_load_spare_selected` | `0` | `[]` | `LNGShipEMS.ZeroLoadSpare` | `{"Pbat_charge": 0.0, "Pbat_discharge": 0.0, "Pg_req": 0.0, "Pspare": 50.0, "cmd_DG1": 0, "cmd_DG2": 0, "cmd_LNG": 0, "cmd_load_cutin": 1}` |

</details>

<details><summary>`res_covers_charge_below_full_soc` — explicit-hot-start: when renewable power exceeds load and SoC is below 0.95, all load is RES-served and residual RES charges the battery.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: when renewable power exceeds load and SoC is below 0.95, all load is RES-served and residual RES charges the battery. |
| initial_state | `LNGShipEMS.ZeroLoadSpare` |
| initial_vars | `{"PL": 100.0, "Ppv": 70.0, "Pw": 50.0, "SoC": 0.94}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `res_covers_charge_selected` | `0` | `[]` | `LNGShipEMS.RESCoversCharge` | `{"Pbat_charge": 20.0, "Pbat_discharge": 0.0, "Pg_req": 0.0, "Pspare": 0.0, "cmd_DG1": 0, "cmd_DG2": 0, "cmd_LNG": 0, "cmd_load_cutin": 1}` |

</details>

<details><summary>`res_covers_spare_at_full_soc_boundary` — explicit-hot-start: at SoC=0.95 with renewable power exceeding load, residual RES should be treated as spare power.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: at SoC=0.95 with renewable power exceeding load, residual RES should be treated as spare power. |
| initial_state | `LNGShipEMS.RESCoversCharge` |
| initial_vars | `{"PL": 100.0, "Ppv": 70.0, "Pw": 50.0, "SoC": 0.95}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `res_covers_spare_selected` | `0` | `[]` | `LNGShipEMS.RESCoversSpare` | `{"Pbat_charge": 0.0, "Pbat_discharge": 0.0, "Pg_req": 0.0, "Pspare": 20.0, "cmd_DG1": 0, "cmd_DG2": 0, "cmd_LNG": 0, "cmd_load_cutin": 1}` |

</details>

<details><summary>`battery_discharge_at_low_soc_boundary` — explicit-hot-start: when RES is below load, SoC exactly 0.2 is suitable for battery use and deficit within battery capacity is discharged.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: when RES is below load, SoC exactly 0.2 is suitable for battery use and deficit within battery capacity is discharged. |
| initial_state | `LNGShipEMS.RESCoversSpare` |
| initial_vars | `{"PL": 100.0, "Pbat_Pmax": 30.0, "Ppv": 40.0, "Pw": 30.0, "SoC": 0.2}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `battery_discharge_selected` | `0` | `[]` | `LNGShipEMS.BatteryDischarge` | `{"Pbat_charge": 0.0, "Pbat_discharge": 30.0, "Pg_req": 0.0, "Pspare": 0.0, "cmd_DG1": 0, "cmd_DG2": 0, "cmd_LNG": 0, "cmd_load_cutin": 1}` |

</details>

<details><summary>`low_soc_lng_charge_margin` — explicit-hot-start: with SoC below 0.2, LNG should cover the RES deficit plus the Pgmax/5 charging margin when within LNG capacity.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: with SoC below 0.2, LNG should cover the RES deficit plus the Pgmax/5 charging margin when within LNG capacity. |
| initial_state | `LNGShipEMS.BatteryDischarge` |
| initial_vars | `{"PL": 100.0, "Pgmax": 100.0, "Ppv": 10.0, "Pw": 10.0, "SoC": 0.19, "eng3_Pmax": 100.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `lng_with_charge_margin_selected` | `0` | `[]` | `LNGShipEMS.LNGWithChargeMargin` | `{"Pbat_charge": 20.0, "Pbat_discharge": 0.0, "Pg_req": 100.0, "Pspare": 0.0, "cmd_DG1": 0, "cmd_DG2": 0, "cmd_LNG": 1, "cmd_load_cutin": 1}` |

</details>

<details><summary>`lng_only_when_battery_capacity_insufficient` — explicit-hot-start: with suitable SoC but battery capacity insufficient and LNG capacity enough, LNG alone should be cut in before diesel.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: with suitable SoC but battery capacity insufficient and LNG capacity enough, LNG alone should be cut in before diesel. |
| initial_state | `LNGShipEMS.LNGWithChargeMargin` |
| initial_vars | `{"PL": 100.0, "Pbat_Pmax": 50.0, "Pgmax": 100.0, "Ppv": 0.0, "Pw": 0.0, "SoC": 0.2, "eng3_Pmax": 120.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `lng_only_selected` | `0` | `[]` | `LNGShipEMS.LNGOnly` | `{"Pbat_charge": 0.0, "Pbat_discharge": 0.0, "Pg_req": 100.0, "Pspare": 0.0, "cmd_DG1": 0, "cmd_DG2": 0, "cmd_LNG": 1, "cmd_load_cutin": 1}` |

</details>

<details><summary>`lng_battery_when_deficit_exceeds_lng` — explicit-hot-start: with suitable SoC and deficit above LNG capacity but within LNG plus battery capacity, dispatch LNG and battery discharge.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: with suitable SoC and deficit above LNG capacity but within LNG plus battery capacity, dispatch LNG and battery discharge. |
| initial_state | `LNGShipEMS.LNGOnly` |
| initial_vars | `{"PL": 130.0, "Pbat_Pmax": 50.0, "Ppv": 0.0, "Pw": 0.0, "SoC": 0.2, "eng3_Pmax": 100.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `lng_battery_selected` | `0` | `[]` | `LNGShipEMS.LNGBattery` | `{"Pbat_charge": 0.0, "Pbat_discharge": 30.0, "Pg_req": 100.0, "Pspare": 0.0, "cmd_DG1": 0, "cmd_DG2": 0, "cmd_LNG": 1, "cmd_load_cutin": 1}` |

</details>

<details><summary>`low_soc_lng_dg1_charge_margin` — explicit-hot-start: with low SoC and deficit above LNG, LNG plus DG1 should include the Pd1max/10 charging margin when within capacity.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: with low SoC and deficit above LNG, LNG plus DG1 should include the Pd1max/10 charging margin when within capacity. |
| initial_state | `LNGShipEMS.LNGBattery` |
| initial_vars | `{"PL": 120.0, "Pbat_Pmax": 10.0, "Pd1max": 50.0, "Ppv": 0.0, "Pw": 0.0, "SoC": 0.19, "eng3_Pmax": 100.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `lng_dg1_charge_margin_selected` | `0` | `[]` | `LNGShipEMS.LNGDG1WithChargeMargin` | `{"Pbat_charge": 5.0, "Pbat_discharge": 0.0, "Pg_req": 125.0, "Pspare": 0.0, "cmd_DG1": 1, "cmd_DG2": 0, "cmd_LNG": 1, "cmd_load_cutin": 1}` |

</details>

<details><summary>`lng_dg1_without_battery_or_margin` — explicit-hot-start: when deficit exceeds LNG and battery contribution is not enough, but fits LNG plus DG1, DG1 is cut in without DG2.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: when deficit exceeds LNG and battery contribution is not enough, but fits LNG plus DG1, DG1 is cut in without DG2. |
| initial_state | `LNGShipEMS.LNGDG1WithChargeMargin` |
| initial_vars | `{"PL": 140.0, "Pbat_Pmax": 20.0, "Pd1max": 50.0, "Ppv": 0.0, "Pw": 0.0, "SoC": 0.2, "eng3_Pmax": 100.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `lng_dg1_selected` | `0` | `[]` | `LNGShipEMS.LNGDG1` | `{"Pbat_charge": 0.0, "Pbat_discharge": 0.0, "Pg_req": 140.0, "Pspare": 0.0, "cmd_DG1": 1, "cmd_DG2": 0, "cmd_LNG": 1, "cmd_load_cutin": 1}` |

</details>

<details><summary>`all_thermal_dg2_last_priority` — explicit-hot-start: when deficit exceeds LNG plus DG1 but is within LNG plus DG1 plus DG2, all thermal units including DG2 are cut in.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: when deficit exceeds LNG plus DG1 but is within LNG plus DG1 plus DG2, all thermal units including DG2 are cut in. |
| initial_state | `LNGShipEMS.LNGDG1` |
| initial_vars | `{"PL": 180.0, "Pbat_Pmax": 20.0, "Pd1max": 50.0, "Pd2max": 80.0, "Ppv": 0.0, "Pw": 0.0, "SoC": 0.5, "eng3_Pmax": 100.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `all_thermal_selected` | `0` | `[]` | `LNGShipEMS.AllThermal` | `{"Pbat_charge": 0.0, "Pbat_discharge": 0.0, "Pg_req": 180.0, "Pspare": 0.0, "cmd_DG1": 1, "cmd_DG2": 1, "cmd_LNG": 1, "cmd_load_cutin": 1}` |

</details>

<details><summary>`overload_battery_cover_extreme_demand` — explicit-hot-start: for extreme demand beyond all RES and thermal resources, all thermal units are activated and remaining lack is covered by battery discharge.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: for extreme demand beyond all RES and thermal resources, all thermal units are activated and remaining lack is covered by battery discharge. |
| initial_state | `LNGShipEMS.AllThermal` |
| initial_vars | `{"PL": 250.0, "Pbat_Pmax": 100.0, "Pd1max": 50.0, "Pd2max": 80.0, "Ppv": 0.0, "Pw": 0.0, "SoC": 0.5, "eng3_Pmax": 100.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `overload_battery_cover_selected` | `0` | `[]` | `LNGShipEMS.OverloadBatteryCover` | `{"Pbat_charge": 0.0, "Pbat_discharge": 20.0, "Pg_req": 230.0, "Pspare": 0.0, "cmd_DG1": 1, "cmd_DG2": 1, "cmd_LNG": 1, "cmd_load_cutin": 1}` |

</details>

<details><summary>`forced_reselect_to_zero_load_charge_from_overload` — explicit-hot-start: from a nonzero dispatch leaf, the global forced guard for PL=0 and SoC<0.95 must reselect ZeroLoadCharge rather than remaining in the old ov...<truncated 13 chars></summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: from a nonzero dispatch leaf, the global forced guard for PL=0 and SoC<0.95 must reselect ZeroLoadCharge rather than remaining in the old overload state. |
| initial_state | `LNGShipEMS.OverloadBatteryCover` |
| initial_vars | `{"PL": 0.0, "Pbat_Pmax": 100.0, "Pd1max": 50.0, "Pd2max": 80.0, "Ppv": 15.0, "Pw": 5.0, "SoC": 0.5, "eng3_Pmax": 100.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `forced_zero_load_charge_reselected` | `0` | `[]` | `LNGShipEMS.ZeroLoadCharge` | `{"Pbat_charge": 20.0, "Pbat_discharge": 0.0, "Pg_req": 0.0, "Pspare": 0.0, "cmd_DG1": 0, "cmd_DG2": 0, "cmd_LNG": 0, "cmd_load_cutin": 1}` |

</details>


### 7. Repair / blocking feedback 明细

- 本 run 未进入 `SD-8/SL-9/SL-10` repair block；通常表示流程在 repair 前已成功、被 provider/schema 错误中断，或在 pre-repair 阶段直接退出。

### 8. 尝试记录与成本

- `SL-1`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 5321, 'completion_chars': 17659, 'completion_tokens': 7670, 'elapsed_seconds': 140.1158511620015, 'estimated_completion_tokens': 4415, 'estimated_prompt_tokens': 6646, 'estimated_total_tokens': 11061, 'first_chunk_seconds': 44.29359240701888, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 26582, 'prompt_tokens': 6469, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 14139}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 3304, 'completion_chars': 10919, 'completion_tokens': 4813, 'elapsed_seconds': 89.09077987799537, 'estimated_completion_tokens': 2730, 'estimated_prompt_tokens': 14774, 'estimated_total_tokens': 17504, 'first_chunk_seconds': 29.67595773699577, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 59094, 'prompt_tokens': 15709, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 20522}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 2552, 'completion_chars': 7732, 'completion_tokens': 2949, 'elapsed_seconds': 55.14282820900553, 'estimated_completion_tokens': 1933, 'estimated_prompt_tokens': 17668, 'estimated_total_tokens': 19601, 'first_chunk_seconds': 9.124066238000523, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 70672, 'prompt_tokens': 19132, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 22081}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-7`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 2012, 'completion_chars': 8911, 'completion_tokens': 2531, 'elapsed_seconds': 48.449066289991606, 'estimated_completion_tokens': 2228, 'estimated_prompt_tokens': 47658, 'estimated_total_tokens': 49886, 'first_chunk_seconds': 12.166396329994313, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 190630, 'prompt_tokens': 54491, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 57022}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。

### 9. 最终停止状态与后续含义

- 停止状态：verdict=`success`，record_status=`success`。
- 主要原因分类：`success`。
- required stages executed：`14/12`，missing=`<none>`。
- repairs：`0/0` accepted；scenario_history=`2`。
- 配置含义：`recommended baseline candidate`；该结果可用于评估默认入口本身。
- 主结果/蓝本边界：`main_result_eligible` 只表示该 run 非 provider-invalid 且 trace/schema/secret/final-verdict 口径可进入主结果候选；`path2_ref_model_blueprint_eligible=false` 时，模型仍可作为 FE/BVS 或 dispatch-classifier 压力测试证据，但不得称为 Path2 ref-model 主蓝本。
- 样本含义：若出现 `design_or_variable_dynamics`，应重点审查变量是否仅作为 guard/input 常量而没有事件/动作更新；若出现 pre-scenario parse/semantic 失败，则应先优化 pyfcstm grammar adherence。
