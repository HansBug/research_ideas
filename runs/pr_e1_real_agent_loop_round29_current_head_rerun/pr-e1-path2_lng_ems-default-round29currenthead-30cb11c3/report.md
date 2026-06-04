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
| Git commit | `4605f0473152018e556332ce4349f6efbc7e1d75` |
| clean / diff / prompt snapshot | clean=`True`, dirty=`False`, diff_hash=`sha256:2a69ad5797ac568a81bddcef615104303a97261094685f4edd8d4484e889ea09`, prompt_hash=`sha256:993dd2a89560dc22cd287bbf50c2cbe6faab9e99a63729d53f02e0d42085b247` |
| provider/model 脱敏标识 | mode=`real_env`, model=`gpt-5.5`, real_api=`True` |
| source / paper | source=`project_1_llm_state_machine_modeling/sources/state-transitions-logical-design-for-hybrid-energy-generation-with-renewable-energy-sources-in-lng-ship`, paper=`project_1_llm_state_machine_modeling/sources/state-transitions-logical-design-for-hybrid-energy-generation-with-renewable-energy-sources-in-lng-ship/paper.pdf` |
| 样本筛选理由 | issue #14 / PR-D 代表性 Path2 EFSM，变量、guard、12 个状态和非法状态都明确；但它可能退化为条件分类式 dispatch，因此更适合作为 FE/BVS 压力测试，是否适合作为 Path2 ref-model 蓝本需看最终 DSL 是否具有 state-dependent mode memory。 |
| 变量参与说明 | `PL/Ppv/Pw/SoC/eng*_Pmax` 是环境输入/容量边界，适合暴露 SD-4 对外部输入变量的处理能力。 |
| run_id | `pr-e1-path2_lng_ems-default-round29currenthead-30cb11c3` |
| final verdict/status | verdict=`success`, record=`success`, result=`converged` |
| main_result_eligible | `false` |
| state_mode_decorative_detected | `false` |
| path2_ref_model_blueprint_eligible | `false`；run_not_main_result_eligible |
| final.fcstm 来源 | `{"accepted": true, "accepted_after_rework": false, "final_dsl_hash": "sha256:68ddc851c3efde1e421625c439cb0b4d3f522b929c9a90d9cd77dcf3cd76d501", "iteration": 2, "last_rejected_candidate": {"candidate_dsl_hash": "sha256:0aac73439d9e4fa4e943fc2d2cead8b9851b5b7084ee281ee912e5eb12f35388", "iteration": 2, "repair_history_index": 6, "rework_instructions": ["Restore concrete guarded inbound transitions from normal dispatch states to OverloadBatteryLack for the strengthened overload condition: PL > 0, Ppv + Pw < PL, PL - Ppv - Pw > LNG_Pmax + eng3_Pmax + DG1_Pmax + DG2_Pmax, SoC >= 0.2, and residual lack <= batt_Pmax. Do not rely on an OverloadBatteryLack self-loop to ground this guard.", "Keep overload_illegal as an explicit illegal-state marker, but make it coexist with the required emergency dispatch path. OverloadBatteryLack.enter may set overload_illegal = 1, and/or the restored inbound transitions may set overload_illegal = 1 in an effect block if the DSL supports effects.", "Preserve action:OverloadBatteryLackDispatch exactly for the scenario/NL emergency branch: Pgen_req = LNG_Pmax + eng3_Pmax + DG1_Pmax + DG2_Pmax; Pbatt_discharge = PL - Ppv - Pw - LNG_Pmax - eng3_Pmax - DG1_Pmax - DG2_Pmax; Pbatt_charge = 0; Pspare = 0; all LNG/eng3/DG1/DG2 cut-in commands enabled; cmd_load_cut_in = 1 and cmd_load_cut_out = 0.", "Specifically repair the failed scenario wrong_target_probe_lng_to_overload_lack: from LNGCoversDeficit under PL=220, Ppv=10, Pw=10, SoC=0.5, batt_Pmax=100, LNG_Pmax=80, eng3_Pmax=30, DG1_Pmax=30, DG2_Pmax=20, one step must transition to OverloadBatteryLack and produce Pgen_req=160 and Pbatt_discharge=40 with the expected thermal/load commands.", "Do not remove the required OverloadBatteryLack state or its dispatch action. Do not leave it unreachable from the root entry path. Do not add only a self-loop to mask grounding.", "Keep the RESCoversCharge and RESCoversSpare guarded transitions intact: PL > 0 && Ppv + Pw >= PL && SoC < 0.95 must select RESCoversCharge with residual renewable battery charging, and PL > 0 && Ppv + Pw >= PL && SoC >= 0.95 must select RESCoversSpare with residual renewable spare power.", "In the SL-9 rationale, explicitly explain how the restored reachable overload path is still marked illegal/non-normal according to the NL, while preserving the required emergency dispatch behavior and prior scenario expectations."], "same_as_final": false, "sl10_decision": "rework"}, "matching_repair_history_indices": [7], "repair_history_index": 7, "selected_source_stage": "SL-7", "sl10_decision": "pass", "source_kind": "repair_candidate"}` |
| FixLog next_action 序列 | `sl9_decision_and_repair, sl10_review, sl9_rework, sl10_review, sl9_rework, sl10_review, sl9_rework, sl10_review, sl9_rework, sl10_review, sc11_accept_then_sd2, sl9_decision_and_repair, ... +7` |
| iteration exit_reason 序列 | `candidate_accepted_for_next_full_pass, candidate_accepted_for_next_full_pass, candidate_accepted_for_next_full_pass, full_pass_all_required_feedback_ok` |
| token/cost/time | tokens=`{'prompt_tokens': 1326269, 'completion_tokens': 138985, 'total_tokens': 1465254, 'estimated_prompt_tokens': 1302960, 'estimated_completion_tokens': 92759, 'estimated_total_tokens': 1395719, 'prompt_chars': 5211793, 'completion_chars': 370983, 'n_calls': 30, 'token_usage_available': True, 'token_usage_unavailable_calls': 0}`, elapsed=`2698.39s` |
| run record | [`pr-e1-path2_lng_ems-default-round29currenthead-30cb11c3.agent_loop.json.gz`](./pr-e1-path2_lng_ems-default-round29currenthead-30cb11c3.agent_loop.json.gz) |
| summary/log/final DSL | [`summary.json`](./summary.json), [`checks.json`](./checks.json), [`reproducibility.json`](./reproducibility.json), [`flow_log.json`](./flow_log.json), [`fix_log.json`](./fix_log.json), [`final.fcstm`](./final.fcstm), [`stdout.txt`](./run_logs/stdout.txt), [`stderr.txt`](./run_logs/stderr.txt) |

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
def float batt_Pmax = 0.0;
def float LNG_Pmax = 0.0;
def float eng3_Pmax = 0.0;
def float DG1_Pmax = 0.0;
def float DG2_Pmax = 0.0;
def float Pgmax = 0.0;
def float Pd1max = 0.0;
def float Pgen_req = 0.0;
def float Pbatt_discharge = 0.0;
def float Pbatt_charge = 0.0;
def float Pspare = 0.0;
def int cmd_LNG_cut_in = 0;
def int cmd_LNG_cut_out = 1;
def int cmd_eng3_cut_in = 0;
def int cmd_eng3_cut_out = 1;
def int cmd_DG1_cut_in = 0;
def int cmd_DG1_cut_out = 1;
def int cmd_DG2_cut_in = 0;
def int cmd_DG2_cut_out = 1;
def int cmd_load_cut_in = 1;
def int cmd_load_cut_out = 0;
def int overload_illegal = 0;

state LNGShipEMS {
    ! * -> ZeroLoadCharge : if [PL == 0 && Ppv + Pw > 0 && SoC < 0.95];
    ! * -> ZeroLoadSpare : if [PL == 0 && SoC >= 0.95];
    ! * -> RESBatteryDischarge : if [PL > 0 && Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw <= batt_Pmax];
    ! * -> LNGLowSoCChargeMargin : if [PL > 0 && Ppv + Pw < PL && SoC < 0.2 && PL - Ppv - Pw + Pgmax / 5 <= LNG_Pmax];
    ! * -> LNGCoversDeficit : if [PL > 0 && Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw > batt_Pmax && PL - Ppv - Pw <= LNG_Pmax];
    ! * -> LNGEng3LowSoCChargeMargin : if [PL > 0 && Ppv + Pw < PL && SoC < 0.2 && PL - Ppv - Pw + Pgmax / 5 > LNG_Pmax && PL - Ppv - Pw + Pd1max / 10 <= LNG_Pmax + eng3_Pmax];
    ! * -> LNGEng3CoversDeficit : if [PL > 0 && Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw > LNG_Pmax && PL - Ppv - Pw <= LNG_Pmax + eng3_Pmax];
    ! * -> LNGEng3DG1LowSoCChargeMargin : if [PL > 0 && Ppv + Pw < PL && SoC < 0.2 && PL - Ppv - Pw + Pd1max / 10 > LNG_Pmax + eng3_Pmax && PL - Ppv - Pw + Pd1max / 10 <= LNG_Pmax + eng3_Pmax + DG1_Pmax];
    ! * -> LNGEng3DG1CoversDeficit : if [PL > 0 && Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw > LNG_Pmax + eng3_Pmax && PL - Ppv - Pw <= LNG_Pmax + eng3_Pmax + DG1_Pmax];
    ! * -> AllThermalWithinCapacity : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > LNG_Pmax + eng3_Pmax + DG1_Pmax && PL - Ppv - Pw <= LNG_Pmax + eng3_Pmax + DG1_Pmax + DG2_Pmax];

    [*] -> ZeroLoadCharge;

    state ZeroLoadCharge {
        during {
            Pgen_req = 0.0;
            Pbatt_discharge = 0.0;
            Pbatt_charge = Ppv + Pw;
            Pspare = 0.0;
            cmd_LNG_cut_in = 0;
            cmd_LNG_cut_out = 1;
            cmd_eng3_cut_in = 0;
            cmd_eng3_cut_out = 1;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 0;
            cmd_load_cut_out = 1;
        }
    }

    state ZeroLoadSpare {
        during {
            Pgen_req = 0.0;
            Pbatt_discharge = 0.0;
            Pbatt_charge = 0.0;
            Pspare = Ppv + Pw;
            cmd_LNG_cut_in = 0;
            cmd_LNG_cut_out = 1;
            cmd_eng3_cut_in = 0;
            cmd_eng3_cut_out = 1;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 0;
            cmd_load_cut_out = 1;
        }
    }

    state RESCoversCharge {
        during {
            Pgen_req = 0.0;
            Pbatt_discharge = 0.0;
            Pbatt_charge = Ppv + Pw - PL;
            Pspare = 0.0;
            cmd_LNG_cut_in = 0;
            cmd_LNG_cut_out = 1;
            cmd_eng3_cut_in = 0;
            cmd_eng3_cut_out = 1;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state RESCoversSpare {
        during {
            Pgen_req = 0.0;
            Pbatt_discharge = 0.0;
            Pbatt_charge = 0.0;
            Pspare = Ppv + Pw - PL;
            cmd_LNG_cut_in = 0;
            cmd_LNG_cut_out = 1;
            cmd_eng3_cut_in = 0;
            cmd_eng3_cut_out = 1;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state RESBatteryDischarge {
        during {
            Pgen_req = 0.0;
            Pbatt_discharge = PL - Ppv - Pw;
            Pbatt_charge = 0.0;
            Pspare = 0.0;
            cmd_LNG_cut_in = 0;
            cmd_LNG_cut_out = 1;
            cmd_eng3_cut_in = 0;
            cmd_eng3_cut_out = 1;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state LNGLowSoCChargeMargin {
        during {
            Pgen_req = PL - Ppv - Pw + Pgmax / 5;
            Pbatt_discharge = 0.0;
            Pbatt_charge = Pgmax / 5;
            Pspare = 0.0;
            cmd_LNG_cut_in = 1;
            cmd_LNG_cut_out = 0;
            cmd_eng3_cut_in = 0;
            cmd_eng3_cut_out = 1;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state LNGCoversDeficit {
        during {
            Pgen_req = PL - Ppv - Pw;
            Pbatt_discharge = 0.0;
            Pbatt_charge = 0.0;
            Pspare = 0.0;
            cmd_LNG_cut_in = 1;
            cmd_LNG_cut_out = 0;
            cmd_eng3_cut_in = 0;
            cmd_eng3_cut_out = 1;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state LNGEng3LowSoCChargeMargin {
        during {
            Pgen_req = PL - Ppv - Pw + Pd1max / 10;
            Pbatt_discharge = 0.0;
            Pbatt_charge = Pd1max / 10;
            Pspare = 0.0;
            cmd_LNG_cut_in = 1;
            cmd_LNG_cut_out = 0;
            cmd_eng3_cut_in = 1;
            cmd_eng3_cut_out = 0;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state LNGEng3CoversDeficit {
        during {
            Pgen_req = PL - Ppv - Pw;
            Pbatt_discharge = 0.0;
            Pbatt_charge = 0.0;
            Pspare = 0.0;
            cmd_LNG_cut_in = 1;
            cmd_LNG_cut_out = 0;
            cmd_eng3_cut_in = 1;
            cmd_eng3_cut_out = 0;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state LNGEng3DG1LowSoCChargeMargin {
        during {
            Pgen_req = PL - Ppv - Pw + Pd1max / 10;
            Pbatt_discharge = 0.0;
            Pbatt_charge = Pd1max / 10;
            Pspare = 0.0;
            cmd_LNG_cut_in = 1;
            cmd_LNG_cut_out = 0;
            cmd_eng3_cut_in = 1;
            cmd_eng3_cut_out = 0;
            cmd_DG1_cut_in = 1;
            cmd_DG1_cut_out = 0;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state LNGEng3DG1CoversDeficit {
        during {
            Pgen_req = PL - Ppv - Pw;
            Pbatt_discharge = 0.0;
            Pbatt_charge = 0.0;
            Pspare = 0.0;
            cmd_LNG_cut_in = 1;
            cmd_LNG_cut_out = 0;
            cmd_eng3_cut_in = 1;
            cmd_eng3_cut_out = 0;
            cmd_DG1_cut_in = 1;
            cmd_DG1_cut_out = 0;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state AllThermalWithinCapacity {
        during {
            Pgen_req = PL - Ppv - Pw;
            Pbatt_discharge = 0.0;
            Pbatt_charge = 0.0;
            Pspare = 0.0;
            cmd_LNG_cut_in = 1;
            cmd_LNG_cut_out = 0;
            cmd_eng3_cut_in = 1;
            cmd_eng3_cut_out = 0;
            cmd_DG1_cut_in = 1;
            cmd_DG1_cut_out = 0;
            cmd_DG2_cut_in = 1;
            cmd_DG2_cut_out = 0;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state OverloadBatteryLack {
        enter { overload_illegal = 1; }
        during {
            Pgen_req = LNG_Pmax + eng3_Pmax + DG1_Pmax + DG2_Pmax;
            Pbatt_discharge = PL - Ppv - Pw - LNG_Pmax - eng3_Pmax - DG1_Pmax - DG2_Pmax;
            Pbatt_charge = 0.0;
            Pspare = 0.0;
            cmd_LNG_cut_in = 1;
            cmd_LNG_cut_out = 0;
            cmd_eng3_cut_in = 1;
            cmd_eng3_cut_out = 0;
            cmd_DG1_cut_in = 1;
            cmd_DG1_cut_out = 0;
            cmd_DG2_cut_in = 1;
            cmd_DG2_cut_out = 0;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    ZeroLoadCharge -> RESCoversCharge : if [PL > 0 && Ppv + Pw >= PL && SoC < 0.95];
    ZeroLoadSpare -> RESCoversCharge : if [PL > 0 && Ppv + Pw >= PL && SoC < 0.95];
    RESCoversCharge -> RESCoversCharge : if [PL > 0 && Ppv + Pw >= PL && SoC < 0.95];
    RESCoversSpare -> RESCoversCharge : if [PL > 0 && Ppv + Pw >= PL && SoC < 0.95];
    RESBatteryDischarge -> RESCoversCharge : if [PL > 0 && Ppv + Pw >= PL && SoC < 0.95];
    LNGLowSoCChargeMargin -> RESCoversCharge : if [PL > 0 && Ppv + Pw >= PL && SoC < 0.95];
    LNGCoversDeficit -> RESCoversCharge : if [PL > 0 && Ppv + Pw >= PL && SoC < 0.95];
    LNGEng3LowSoCChargeMargin -> RESCoversCharge : if [PL > 0 && Ppv + Pw >= PL && SoC < 0.95];
    LNGEng3CoversDeficit -> RESCoversCharge : if [PL > 0 && Ppv + Pw >= PL && SoC < 0.95];
    LNGEng3DG1LowSoCChargeMargin -> RESCoversCharge : if [PL > 0 && Ppv + Pw >= PL && SoC < 0.95];
    LNGEng3DG1CoversDeficit -> RESCoversCharge : if [PL > 0 && Ppv + Pw >= PL && SoC < 0.95];
    AllThermalWithinCapacity -> RESCoversCharge : if [PL > 0 && Ppv + Pw >= PL && SoC < 0.95];
    OverloadBatteryLack -> RESCoversCharge : if [PL > 0 && Ppv + Pw >= PL && SoC < 0.95];

    ZeroLoadCharge -> RESCoversSpare : if [PL > 0 && Ppv + Pw >= PL && SoC >= 0.95];
    ZeroLoadSpare -> RESCoversSpare : if [PL > 0 && Ppv + Pw >= PL && SoC >= 0.95];
    RESCoversCharge -> RESCoversSpare : if [PL > 0 && Ppv + Pw >= PL && SoC >= 0.95];
    RESCoversSpare -> RESCoversSpare : if [PL > 0 && Ppv + Pw >= PL && SoC >= 0.95];
    RESBatteryDischarge -> RESCoversSpare : if [PL > 0 && Ppv + Pw >= PL && SoC >= 0.95];
    LNGLowSoCChargeMargin -> RESCoversSpare : if [PL > 0 && Ppv + Pw >= PL && SoC >= 0.95];
    LNGCoversDeficit -> RESCoversSpare : if [PL > 0 && Ppv + Pw >= PL && SoC >= 0.95];
    LNGEng3LowSoCChargeMargin -> RESCoversSpare : if [PL > 0 && Ppv + Pw >= PL && SoC >= 0.95];
    LNGEng3CoversDeficit -> RESCoversSpare : if [PL > 0 && Ppv + Pw >= PL && SoC >= 0.95];
    LNGEng3DG1LowSoCChargeMargin -> RESCoversSpare : if [PL > 0 && Ppv + Pw >= PL && SoC >= 0.95];
    LNGEng3DG1CoversDeficit -> RESCoversSpare : if [PL > 0 && Ppv + Pw >= PL && SoC >= 0.95];
    AllThermalWithinCapacity -> RESCoversSpare : if [PL > 0 && Ppv + Pw >= PL && SoC >= 0.95];
    OverloadBatteryLack -> RESCoversSpare : if [PL > 0 && Ppv + Pw >= PL && SoC >= 0.95];

    ZeroLoadCharge -> OverloadBatteryLack : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > LNG_Pmax + eng3_Pmax + DG1_Pmax + DG2_Pmax && SoC >= 0.2 && PL - Ppv - Pw - LNG_Pmax - eng3_Pmax - DG1_Pmax - DG2_Pmax <= batt_Pmax];
    ZeroLoadSpare -> OverloadBatteryLack : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > LNG_Pmax + eng3_Pmax + DG1_Pmax + DG2_Pmax && SoC >= 0.2 && PL - Ppv - Pw - LNG_Pmax - eng3_Pmax - DG1_Pmax - DG2_Pmax <= batt_Pmax];
    RESCoversCharge -> OverloadBatteryLack : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > LNG_Pmax + eng3_Pmax + DG1_Pmax + DG2_Pmax && SoC >= 0.2 && PL - Ppv - Pw - LNG_Pmax - eng3_Pmax - DG1_Pmax - DG2_Pmax <= batt_Pmax];
    RESCoversSpare -> OverloadBatteryLack : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > LNG_Pmax + eng3_Pmax + DG1_Pmax + DG2_Pmax && SoC >= 0.2 && PL - Ppv - Pw - LNG_Pmax - eng3_Pmax - DG1_Pmax - DG2_Pmax <= batt_Pmax];
    RESBatteryDischarge -> OverloadBatteryLack : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > LNG_Pmax + eng3_Pmax + DG1_Pmax + DG2_Pmax && SoC >= 0.2 && PL - Ppv - Pw - LNG_Pmax - eng3_Pmax - DG1_Pmax - DG2_Pmax <= batt_Pmax];
    LNGLowSoCChargeMargin -> OverloadBatteryLack : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > LNG_Pmax + eng3_Pmax + DG1_Pmax + DG2_Pmax && SoC >= 0.2 && PL - Ppv - Pw - LNG_Pmax - eng3_Pmax - DG1_Pmax - DG2_Pmax <= batt_Pmax];
    LNGCoversDeficit -> OverloadBatteryLack : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > LNG_Pmax + eng3_Pmax + DG1_Pmax + DG2_Pmax && SoC >= 0.2 && PL - Ppv - Pw - LNG_Pmax - eng3_Pmax - DG1_Pmax - DG2_Pmax <= batt_Pmax];
    LNGEng3LowSoCChargeMargin -> OverloadBatteryLack : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > LNG_Pmax + eng3_Pmax + DG1_Pmax + DG2_Pmax && SoC >= 0.2 && PL - Ppv - Pw - LNG_Pmax - eng3_Pmax - DG1_Pmax - DG2_Pmax <= batt_Pmax];
    LNGEng3CoversDeficit -> OverloadBatteryLack : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > LNG_Pmax + eng3_Pmax + DG1_Pmax + DG2_Pmax && SoC >= 0.2 && PL - Ppv - Pw - LNG_Pmax - eng3_Pmax - DG1_Pmax - DG2_Pmax <= batt_Pmax];
    LNGEng3DG1LowSoCChargeMargin -> OverloadBatteryLack : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > LNG_Pmax + eng3_Pmax + DG1_Pmax + DG2_Pmax && SoC >= 0.2 && PL - Ppv - Pw - LNG_Pmax - eng3_Pmax - DG1_Pmax - DG2_Pmax <= batt_Pmax];
    LNGEng3DG1CoversDeficit -> OverloadBatteryLack : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > LNG_Pmax + eng3_Pmax + DG1_Pmax + DG2_Pmax && SoC >= 0.2 && PL - Ppv - Pw - LNG_Pmax - eng3_Pmax - DG1_Pmax - DG2_Pmax <= batt_Pmax];
    AllThermalWithinCapacity -> OverloadBatteryLack : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > LNG_Pmax + eng3_Pmax + DG1_Pmax + DG2_Pmax && SoC >= 0.2 && PL - Ppv - Pw - LNG_Pmax - eng3_Pmax - DG1_Pmax - DG2_Pmax <= batt_Pmax];
    OverloadBatteryLack -> OverloadBatteryLack : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > LNG_Pmax + eng3_Pmax + DG1_Pmax + DG2_Pmax && SoC >= 0.2 && PL - Ppv - Pw - LNG_Pmax - eng3_Pmax - DG1_Pmax - DG2_Pmax <= batt_Pmax];
}
```

### 4. 全流程真实摘要表

| Stage | 是否 LLM | iteration | 结果 | 获取的信息 / 反馈 | 本阶段做了什么 | DSL 修改 | artifact/log |
|---|---:|---:|---:|---|---|---|---|
| `SC-0` | 否 | - | ✅ | trace/control | 初始化 run state | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round29currenthead-30cb11c3.agent_loop.json.gz) |
| `SL-1` | 是 | - | ✅ | LLM calls=1, tokens=14318 | 生成初始 DSL 与 grounding seeds | initial len=8619 | [`record`](./pr-e1-path2_lng_ems-default-round29currenthead-30cb11c3.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round29currenthead-30cb11c3.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round29currenthead-30cb11c3.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=336, info=0; blocking=0, advisory=336, info=0; blocking=0, advisory=374, info=0; blocking=0, advisory=376, info=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round29currenthead-30cb11c3.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=9, tokens=294505 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round29currenthead-30cb11c3.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round29currenthead-30cb11c3.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=9, tokens=294505 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round29currenthead-30cb11c3.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round29currenthead-30cb11c3.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=9, tokens=294505 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round29currenthead-30cb11c3.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round29currenthead-30cb11c3.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round29currenthead-30cb11c3.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round29currenthead-30cb11c3.agent_loop.json.gz) |
| `SL-7` | 是 | 0 | ✅ | LLM calls=4, tokens=326501 | LLM model review | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round29currenthead-30cb11c3.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round29currenthead-30cb11c3.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=8, tokens=442910 | LLM per-request accept/reject + repair | candidate len=8708,8708,9110,8708,13269,14405,11731,14475 | [`record`](./pr-e1-path2_lng_ems-default-round29currenthead-30cb11c3.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ⚠️ | LLM calls=8, tokens=387020 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round29currenthead-30cb11c3.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=8, tokens=442910 | LLM per-request accept/reject + repair | candidate len=8708,8708,9110,8708,13269,14405,11731,14475 | [`record`](./pr-e1-path2_lng_ems-default-round29currenthead-30cb11c3.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ⚠️ | LLM calls=8, tokens=387020 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round29currenthead-30cb11c3.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=8, tokens=442910 | LLM per-request accept/reject + repair | candidate len=8708,8708,9110,8708,13269,14405,11731,14475 | [`record`](./pr-e1-path2_lng_ems-default-round29currenthead-30cb11c3.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ⚠️ | LLM calls=8, tokens=387020 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round29currenthead-30cb11c3.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=8, tokens=442910 | LLM per-request accept/reject + repair | candidate len=8708,8708,9110,8708,13269,14405,11731,14475 | [`record`](./pr-e1-path2_lng_ems-default-round29currenthead-30cb11c3.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ⚠️ | LLM calls=8, tokens=387020 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round29currenthead-30cb11c3.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=8, tokens=442910 | LLM per-request accept/reject + repair | candidate len=8708,8708,9110,8708,13269,14405,11731,14475 | [`record`](./pr-e1-path2_lng_ems-default-round29currenthead-30cb11c3.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=8, tokens=387020 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round29currenthead-30cb11c3.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round29currenthead-30cb11c3.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round29currenthead-30cb11c3.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round29currenthead-30cb11c3.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=336, info=0; blocking=0, advisory=336, info=0; blocking=0, advisory=374, info=0; blocking=0, advisory=376, info=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round29currenthead-30cb11c3.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round29currenthead-30cb11c3.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=9, tokens=294505 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round29currenthead-30cb11c3.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round29currenthead-30cb11c3.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=9, tokens=294505 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round29currenthead-30cb11c3.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round29currenthead-30cb11c3.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round29currenthead-30cb11c3.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round29currenthead-30cb11c3.agent_loop.json.gz) |
| `SL-7` | 是 | 0 | ✅ | LLM calls=4, tokens=326501 | LLM model review | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round29currenthead-30cb11c3.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round29currenthead-30cb11c3.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=8, tokens=442910 | LLM per-request accept/reject + repair | candidate len=8708,8708,9110,8708,13269,14405,11731,14475 | [`record`](./pr-e1-path2_lng_ems-default-round29currenthead-30cb11c3.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=8, tokens=387020 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round29currenthead-30cb11c3.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round29currenthead-30cb11c3.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round29currenthead-30cb11c3.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round29currenthead-30cb11c3.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=336, info=0; blocking=0, advisory=336, info=0; blocking=0, advisory=374, info=0; blocking=0, advisory=376, info=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round29currenthead-30cb11c3.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round29currenthead-30cb11c3.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=9, tokens=294505 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round29currenthead-30cb11c3.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round29currenthead-30cb11c3.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=9, tokens=294505 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round29currenthead-30cb11c3.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round29currenthead-30cb11c3.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round29currenthead-30cb11c3.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round29currenthead-30cb11c3.agent_loop.json.gz) |
| `SL-7` | 是 | 0 | ✅ | LLM calls=4, tokens=326501 | LLM model review | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round29currenthead-30cb11c3.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round29currenthead-30cb11c3.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=8, tokens=442910 | LLM per-request accept/reject + repair | candidate len=8708,8708,9110,8708,13269,14405,11731,14475 | [`record`](./pr-e1-path2_lng_ems-default-round29currenthead-30cb11c3.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=8, tokens=387020 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round29currenthead-30cb11c3.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=8, tokens=442910 | LLM per-request accept/reject + repair | candidate len=8708,8708,9110,8708,13269,14405,11731,14475 | [`record`](./pr-e1-path2_lng_ems-default-round29currenthead-30cb11c3.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=8, tokens=387020 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round29currenthead-30cb11c3.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round29currenthead-30cb11c3.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round29currenthead-30cb11c3.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round29currenthead-30cb11c3.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=336, info=0; blocking=0, advisory=336, info=0; blocking=0, advisory=374, info=0; blocking=0, advisory=376, info=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round29currenthead-30cb11c3.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round29currenthead-30cb11c3.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=9, tokens=294505 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round29currenthead-30cb11c3.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round29currenthead-30cb11c3.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=9, tokens=294505 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round29currenthead-30cb11c3.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round29currenthead-30cb11c3.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round29currenthead-30cb11c3.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round29currenthead-30cb11c3.agent_loop.json.gz) |
| `SL-7` | 是 | 0 | ✅ | LLM calls=4, tokens=326501 | LLM model review | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round29currenthead-30cb11c3.agent_loop.json.gz) |
| `SC-12` | 否 | - | ✅ | full_pass_all_required_feedback_ok | 写 final verdict | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round29currenthead-30cb11c3.agent_loop.json.gz) |
| `SC-13` | 否 | - | ✅ | trace/control | 写审计 run record | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round29currenthead-30cb11c3.agent_loop.json.gz) |

### 4.1 完整流程日志（stage/control-flow replay ledger）

口径：本节来自 `AgentLoopRunRecord.logs`，与 [`flow_log.json`](./flow_log.json) 一致；用于复现每个 stage 如何进入、得到什么批示、跳转到哪里，以及每次 DSL 产物/候选如何变化。

| # | ts | stage | iter | event | result / jump | DSL evidence |
|---:|---|---|---:|---|---|---|
| 1 | `2026-06-04T08:37:21Z` | `SC-0` | `-` | `run_start` | {} | <none> |
| 2 | `2026-06-04T08:37:21Z` | `SL-1` | `-` | `stage_enter` | {"reason": "initial_modeling_adapter_available"} | <none> |
| 3 | `2026-06-04T08:39:45Z` | `SL-1` | `-` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 4 | `2026-06-04T08:39:45Z` | `SL-1` | `-` | `stage_result` | {"jump": "SD-2", "ok": true} | candidate_dsl:len=8619,hash=sha256:01c5a57aa106 |
| 5 | `2026-06-04T08:39:45Z` | `<control>` | `0` | `iteration_enter` | {} | current_hash=sha256:01c5a57aa10618b447f8a2a830a9d8e06062db2bafb5fe2ac26d66485929c533 |
| 6 | `2026-06-04T08:39:45Z` | `<control>` | `0` | `iteration_validation_enter` | {} | dsl:len=8619,hash=sha256:01c5a57aa106, current_hash=sha256:01c5a57aa10618b447f8a2a830a9d8e06062db2bafb5fe2ac26d66485929c533 |
| 7 | `2026-06-04T08:39:45Z` | `SD-2` | `0` | `stage_enter` | {"reason": "full_validation_pass"} | <none> |
| 8 | `2026-06-04T08:39:45Z` | `SD-2` | `0` | `stage_result` | {"jump": "SD-3", "ok": true, "status": "StageStatus.OK"} | <none> |
| 9 | `2026-06-04T08:39:45Z` | `SD-3` | `0` | `stage_enter` | {"reason": "SD-2 ok"} | <none> |
| 10 | `2026-06-04T08:39:45Z` | `SD-3` | `0` | `stage_result` | {"jump": "SD-4", "ok": true, "status": "StageStatus.OK"} | <none> |
| 11 | `2026-06-04T08:39:45Z` | `SD-4` | `0` | `stage_enter` | {"reason": "SD-3 ok"} | <none> |
| 12 | `2026-06-04T08:39:45Z` | `SD-4` | `0` | `stage_result` | {"jump": "SL-5", "ok": true, "status": "StageStatus.OK"} | <none> |
| 13 | `2026-06-04T08:39:45Z` | `SL-5` | `0` | `stage_enter` | {"reason": "scenario_set_absent"} | <none> |
| 14 | `2026-06-04T08:41:08Z` | `SL-5` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 15 | `2026-06-04T08:41:09Z` | `SD-5A` | `0` | `stage_result` | {"jump": "SL-5 retry", "ok": false, "status": "StageStatus.ADVISORY"} | <none> |
| 16 | `2026-06-04T08:41:09Z` | `SL-5` | `0` | `stage_enter` | {"reason": "scenario_coverage_gap_retry"} | <none> |
| 17 | `2026-06-04T08:42:39Z` | `SL-5` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 18 | `2026-06-04T08:42:40Z` | `SD-5A` | `0` | `stage_result` | {"jump": "SL-5 retry", "ok": false, "status": "StageStatus.ADVISORY"} | <none> |
| 19 | `2026-06-04T08:42:40Z` | `SL-5` | `0` | `stage_enter` | {"reason": "scenario_coverage_gap_retry"} | <none> |
| 20 | `2026-06-04T08:44:26Z` | `SL-5` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 21 | `2026-06-04T08:44:27Z` | `SD-5A` | `0` | `stage_result` | {"jump": "SC-5F", "ok": true, "status": "StageStatus.OK"} | <none> |
| 22 | `2026-06-04T08:44:27Z` | `SC-5F` | `0` | `stage_result` | {"jump": "SD-6", "ok": true} | <none> |
| 23 | `2026-06-04T08:44:27Z` | `SD-6` | `0` | `stage_enter` | {"reason": "scenario_set_ready"} | <none> |
| 24 | `2026-06-04T08:44:27Z` | `SD-6` | `0` | `stage_result` | {"jump": "SL-7", "ok": true, "status": "StageStatus.OK"} | <none> |
| 25 | `2026-06-04T08:44:27Z` | `SL-7` | `0` | `stage_enter` | {"reason": "SD-6 ok"} | <none> |
| 26 | `2026-06-04T08:45:29Z` | `SL-7` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 27 | `2026-06-04T08:45:29Z` | `SL-7` | `0` | `stage_result` | {"jump": "SD-8", "ok": false, "status": "StageStatus.OK"} | <none> |
| 28 | `2026-06-04T08:45:29Z` | `SL-7` | `0` | `grounding_update_hints_recorded` | {} | <none> |
| 29 | `2026-06-04T08:45:29Z` | `<control>` | `0` | `iteration_validation_result` | {"jump": "SD-8 repair", "selected_feedback": {"blocking": true, "blocking_findings": [{"category": "unsafe_recovery", "evidence": ["NL: \"The overload completion state is illegal... the state shall never occur in practice.\"", "DSL forced transition reaches `OverloadBatteryLack` whenever demand exceeds all RES and thermal resources.", "`OverloadBatteryLack` sets `cmd_load_cut_in = 1`, `cmd_load_cut_out = 0`, and comp...<truncated 606 chars> | <none> |
| 30 | `2026-06-04T08:45:29Z` | `SD-8` | `0` | `repair_path_enter` | {"jump": "SD-8", "selected_feedback": {"blocking": true, "blocking_findings": [{"category": "unsafe_recovery", "evidence": ["NL: \"The overload completion state is illegal... the state shall never occur in practice.\"", "DSL forced transition reaches `OverloadBatteryLack` whenever demand exceeds all RES and thermal resources.", "`OverloadBatteryLack` sets `cmd_load_cut_in = 1`, `cmd_load_cut_out = 0`, and computes `P...<truncated 599 chars> | current_dsl:len=8619,hash=sha256:01c5a57aa106 |
| 31 | `2026-06-04T08:45:29Z` | `SD-8` | `0` | `stage_result` | {"jump": "SL-9", "ok": true, "status": "StageStatus.OK"} | <none> |
| 32 | `2026-06-04T08:45:29Z` | `SD-8` | `0` | `fix_request_batch` | {"request_count": 1} | <none> |
| 33 | `2026-06-04T08:45:29Z` | `SL-9` | `0` | `stage_enter` | {"reason": "fix_requests_ready"} | old_dsl:len=8619,hash=sha256:01c5a57aa106 |
| 34 | `2026-06-04T08:46:47Z` | `SL-9` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 35 | `2026-06-04T08:46:47Z` | `SL-9` | `0` | `stage_result` | {"accepted_request_ids": ["fixreq-0-sl7-0-be1e03bda7"], "jump": "SL-10", "ok": true, "rejected_request_ids": []} | candidate_dsl:len=8708,hash=sha256:c4422351d34d |
| 36 | `2026-06-04T08:46:48Z` | `SD-10` | `0` | `stage_result` | {"jump": "SL-10", "ok": false, "status": "StageStatus.FAIL"} | <none> |
| 37 | `2026-06-04T08:46:48Z` | `SL-10` | `0` | `stage_enter` | {"reason": "candidate_dsl_and_local_evidence_ready"} | candidate_hash=sha256:c4422351d34de68230c5a6f4f43ae04421c7e963fa641dd7ca3c3377d63d966a |
| 38 | `2026-06-04T08:47:16Z` | `SL-10` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 39 | `2026-06-04T08:47:16Z` | `SL-10` | `0` | `stage_result` | {"decision": "rework", "jump": "SL-9 rework", "ok": false} | <none> |
| 40 | `2026-06-04T08:47:16Z` | `SL-10` | `0` | `grounding_update_hints_recorded` | {} | <none> |
| 41 | `2026-06-04T08:47:16Z` | `SL-9` | `0` | `stage_enter` | {"reason": "sl10_rework_locked"} | old_dsl:len=8619,hash=sha256:01c5a57aa106 |
| 42 | `2026-06-04T08:48:37Z` | `SL-9` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 43 | `2026-06-04T08:48:37Z` | `SL-9` | `0` | `stage_result` | {"accepted_request_ids": ["fixreq-0-sl7-0-be1e03bda7"], "jump": "SL-10", "ok": true, "rejected_request_ids": []} | candidate_dsl:len=8708,hash=sha256:a3d167d8c7d3 |
| 44 | `2026-06-04T08:48:38Z` | `SD-10` | `0` | `stage_result` | {"jump": "SL-10", "ok": false, "status": "StageStatus.FAIL"} | <none> |
| 45 | `2026-06-04T08:48:38Z` | `SL-10` | `0` | `stage_enter` | {"reason": "candidate_dsl_and_local_evidence_ready"} | candidate_hash=sha256:a3d167d8c7d32fd212b403f7d77af2d6db6d5c6d03fe6f1bbf42cc671ee351be |
| 46 | `2026-06-04T08:49:15Z` | `SL-10` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 47 | `2026-06-04T08:49:15Z` | `SL-10` | `0` | `stage_result` | {"decision": "rework", "jump": "SL-9 rework", "ok": false} | <none> |
| 48 | `2026-06-04T08:49:15Z` | `SL-10` | `0` | `grounding_update_hints_recorded` | {} | <none> |
| 49 | `2026-06-04T08:49:15Z` | `SL-9` | `0` | `stage_enter` | {"reason": "sl10_rework_locked"} | old_dsl:len=8619,hash=sha256:01c5a57aa106 |
| 50 | `2026-06-04T08:50:54Z` | `SL-9` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 51 | `2026-06-04T08:50:54Z` | `SL-9` | `0` | `stage_result` | {"accepted_request_ids": ["fixreq-0-sl7-0-be1e03bda7"], "jump": "SL-10", "ok": true, "rejected_request_ids": []} | candidate_dsl:len=9110,hash=sha256:fa9a662af2c9 |
| 52 | `2026-06-04T08:50:55Z` | `SD-10` | `0` | `stage_result` | {"jump": "SL-10", "ok": false, "status": "StageStatus.FAIL"} | <none> |
| 53 | `2026-06-04T08:50:55Z` | `SL-10` | `0` | `stage_enter` | {"reason": "candidate_dsl_and_local_evidence_ready"} | candidate_hash=sha256:fa9a662af2c91e5cca5f3f32570c28a50c1745f2db60dc535a9ee953a9402ac3 |
| 54 | `2026-06-04T08:51:38Z` | `SL-10` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 55 | `2026-06-04T08:51:38Z` | `SL-10` | `0` | `stage_result` | {"decision": "rework", "jump": "SL-9 rework", "ok": false} | <none> |
| 56 | `2026-06-04T08:51:38Z` | `SL-10` | `0` | `grounding_update_hints_recorded` | {} | <none> |
| 57 | `2026-06-04T08:51:38Z` | `SL-9` | `0` | `stage_enter` | {"reason": "sl10_rework_locked"} | old_dsl:len=8619,hash=sha256:01c5a57aa106 |
| 58 | `2026-06-04T08:53:28Z` | `SL-9` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 59 | `2026-06-04T08:53:28Z` | `SL-9` | `0` | `stage_result` | {"accepted_request_ids": ["fixreq-0-sl7-0-be1e03bda7"], "jump": "SL-10", "ok": true, "rejected_request_ids": []} | candidate_dsl:len=8708,hash=sha256:a3d167d8c7d3 |
| 60 | `2026-06-04T08:53:28Z` | `SD-10` | `0` | `stage_result` | {"jump": "SL-10", "ok": false, "status": "StageStatus.FAIL"} | <none> |
| 61 | `2026-06-04T08:53:28Z` | `SL-10` | `0` | `stage_enter` | {"reason": "candidate_dsl_and_local_evidence_ready"} | candidate_hash=sha256:a3d167d8c7d32fd212b403f7d77af2d6db6d5c6d03fe6f1bbf42cc671ee351be |
| 62 | `2026-06-04T08:54:02Z` | `SL-10` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 63 | `2026-06-04T08:54:02Z` | `SL-10` | `0` | `stage_result` | {"decision": "rework", "jump": "SL-9 rework", "ok": false} | <none> |
| 64 | `2026-06-04T08:54:02Z` | `SL-10` | `0` | `grounding_update_hints_recorded` | {} | <none> |
| 65 | `2026-06-04T08:54:02Z` | `SL-9` | `0` | `stage_enter` | {"reason": "sl10_rework_locked"} | old_dsl:len=8619,hash=sha256:01c5a57aa106 |
| 66 | `2026-06-04T08:56:10Z` | `SL-9` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 67 | `2026-06-04T08:56:10Z` | `SL-9` | `0` | `stage_result` | {"accepted_request_ids": ["fixreq-0-sl7-0-be1e03bda7"], "jump": "SL-10", "ok": true, "rejected_request_ids": []} | candidate_dsl:len=13269,hash=sha256:813b635ee381 |
| 68 | `2026-06-04T08:56:10Z` | `SD-10` | `0` | `stage_result` | {"jump": "SL-10", "ok": false, "status": "StageStatus.FAIL"} | <none> |
| 69 | `2026-06-04T08:56:10Z` | `SL-10` | `0` | `stage_enter` | {"reason": "candidate_dsl_and_local_evidence_ready"} | candidate_hash=sha256:813b635ee38132f66b9e8cd1fbf754f73d5598598eca4acef2ded16fddad4376 |
| 70 | `2026-06-04T08:56:43Z` | `SL-10` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 71 | `2026-06-04T08:56:43Z` | `SL-10` | `0` | `stage_result` | {"decision": "pass", "jump": "SC-11", "ok": true} | <none> |
| 72 | `2026-06-04T08:56:43Z` | `SL-10` | `0` | `grounding_update_hints_recorded` | {} | <none> |
| 73 | `2026-06-04T08:56:43Z` | `SC-11` | `0` | `stage_result` | {"jump": "SD-2 next iteration", "ok": true, "reason": "SL-10 accepted candidate; next iteration must restart at SD-2"} | candidate_dsl:len=13269,hash=sha256:813b635ee381 |
| 74 | `2026-06-04T08:56:43Z` | `<control>` | `0` | `iteration_repair_result` | {"accepted": true, "jump": "SD-2 next iteration"} | current_hash=sha256:813b635ee38132f66b9e8cd1fbf754f73d5598598eca4acef2ded16fddad4376 |
| 75 | `2026-06-04T08:56:43Z` | `<control>` | `1` | `iteration_enter` | {} | current_hash=sha256:813b635ee38132f66b9e8cd1fbf754f73d5598598eca4acef2ded16fddad4376 |
| 76 | `2026-06-04T08:56:43Z` | `<control>` | `1` | `iteration_validation_enter` | {} | dsl:len=13269,hash=sha256:813b635ee381, current_hash=sha256:813b635ee38132f66b9e8cd1fbf754f73d5598598eca4acef2ded16fddad4376 |
| 77 | `2026-06-04T08:56:43Z` | `SD-2` | `1` | `stage_enter` | {"reason": "full_validation_pass"} | <none> |
| 78 | `2026-06-04T08:56:43Z` | `SD-2` | `1` | `stage_result` | {"jump": "SD-3", "ok": true, "status": "StageStatus.OK"} | <none> |
| 79 | `2026-06-04T08:56:43Z` | `SD-3` | `1` | `stage_enter` | {"reason": "SD-2 ok"} | <none> |
| 80 | `2026-06-04T08:56:43Z` | `SD-3` | `1` | `stage_result` | {"jump": "SD-4", "ok": true, "status": "StageStatus.OK"} | <none> |
- ……另有 `105` 条流程日志见 [`flow_log.json`](./flow_log.json) / run record。

### 5. Iteration / repair / review 摘要

| Iter | selected feedback | repair? | FixRequestBatch | SL-9 | local checks | SL-10 | 回到 SD-2? | verdict/备注 |
|---:|---|---|---|---|---|---|---|---|
| 0 | `SL-7` | yes | fixbatch-0-sha256-081cf0a961f / n=1 | accept=1, reject=0, waiver=0 | ok=False, target=False, regression=False, drift=major, local_stage=SD-10, reason=forced_transition_count_drift; missing_required_grounding | decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none> | yes | candidate_accepted_for_next_full_pass |
| 1 | `SL-7` | yes | fixbatch-1-sha256-00855f2776f / n=3 | accept=3, reject=0, waiver=0 | ok=False, target=False, regression=False, drift=major, local_stage=SD-10, reason=forced_transition_count_drift; missing_required_grounding | decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none> | yes | candidate_accepted_for_next_full_pass |
| 2 | `SL-7` | yes | fixbatch-2-sha256-29c6b5ff10b / n=2 | accept=2, reject=0, waiver=0 | ok=False, target=False, regression=False, drift=major, local_stage=SD-10, reason=missing_required_grounding | decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none> | yes | candidate_accepted_for_next_full_pass |
| 3 | `<none>` | no | <none> | <none> | <none> | <none> | no | full_pass_all_required_feedback_ok |

### 6. Scenario 明细与逐轮通过情况

#### 6.1 Scenario pass/fail by iteration

口径：`✅` = 该 scenario 在该轮 SD-6 simulation 通过；`❌` = 该轮失败；`⚪` = 该轮未执行或无该 scenario 结果。

| Scenario | Intent | Iter 1 | Iter 2 | Iter 3 | Iter 4 |
|---|---|---|---|---|---|
| `wrong_target_probe_thermal_to_zero_load_spare` | explicit-hot-start: from a concrete thermal leaf, PL=0 with SoC at 0.95 must target ZeroLoadSpare, catching wrong-target...<truncated 44 chars> | ⚪ | ⚪ | ✅ | ✅ |
| `wrong_target_probe_zero_load_to_lng_low_soc_margin` | explicit-hot-start: from ZeroLoadCharge, low SoC and a deficit plus Pgmax/5 exactly within LNG capacity must target LNGL...<truncated 18 chars> | ⚪ | ⚪ | ✅ | ✅ |
| `wrong_target_probe_zero_load_spare_to_lng_eng3_low_soc_margin` | explicit-hot-start: from ZeroLoadSpare, low SoC with LNG margin over LNG capacity but Pd1max/10 margin within LNG+eng3 m...<truncated 37 chars> | ⚪ | ⚪ | ✅ | ✅ |
| `wrong_target_probe_res_spare_to_dg1_low_soc_margin` | explicit-hot-start: from RESCoversSpare, low SoC with deficit plus Pd1max/10 within LNG+eng3+DG1 must target LNGEng3DG1L...<truncated 35 chars> | ⚪ | ⚪ | ✅ | ✅ |
| `wrong_target_probe_overload_to_dg1_suitable_soc` | explicit-hot-start: from OverloadBatteryLack, suitable-SoC deficit above LNG+eng3 but within LNG+eng3+DG1 must target LN...<truncated 52 chars> | ⚪ | ⚪ | ✅ | ✅ |
| `wrong_target_probe_res_charge_to_all_thermal` | explicit-hot-start: from RESCoversCharge, suitable-SoC deficit above LNG+eng3+DG1 but exactly within all thermal capacit...<truncated 39 chars> | ⚪ | ⚪ | ✅ | ✅ |
| `wrong_target_probe_lng_to_overload_lack` | explicit-hot-start: from LNGCoversDeficit, extreme demand above all thermal capacity but within battery lack coverage mu...<truncated 30 chars> | ⚪ | ⚪ | ✅ | ✅ |
| `wrong_target_probe_battery_to_lng_eng3_suitable_soc` | explicit-hot-start: from RESBatteryDischarge, suitable-SoC deficit above LNG alone but exactly within LNG+eng3 must targ...<truncated 24 chars> | ⚪ | ⚪ | ✅ | ✅ |
| `default_init_zero_load_charge_dispatch` | default-init: first cycle must dispatch the root initial transition to ZeroLoadCharge and charge batteries from RES when...<truncated 28 chars> | ⚪ | ⚪ | ⚪ | ✅ |
| `missing_forced_probe_battery_to_zero_load_charge` | explicit-hot-start: from RESBatteryDischarge, a zero-load low-SoC condition must be globally reselected to ZeroLoadCharg...<truncated 72 chars> | ⚪ | ⚪ | ⚪ | ✅ |
| `boundary_soc_095_res_cover_spare` | explicit-hot-start: at the exact SoC=0.95 RES-covered threshold, the EMS must treat residual renewable power as spare, c...<truncated 55 chars> | ⚪ | ⚪ | ⚪ | ✅ |
| `boundary_battery_deficit_equals_batt_pmax` | explicit-hot-start: with suitable SoC and deficit exactly equal to batt_Pmax, the EMS must use battery discharge rather ...<truncated 71 chars> | ⚪ | ⚪ | ⚪ | ✅ |
| `unreachable_target_probe_res_cover_charge` | explicit-hot-start: RES covers a positive load with SoC just below 0.95, so EMS must target RESCoversCharge; catches wro...<truncated 64 chars> | ⚪ | ⚪ | ⚪ | ✅ |
| `unreachable_target_probe_overload_lack_boundary` | explicit-hot-start: from RESBatteryDischarge, extreme demand exceeding all thermal resources with battery lack exactly e...<truncated 110 chars> | ⚪ | ⚪ | ⚪ | ✅ |
| `default_init_zero_load_res_charges_battery` |  | ✅ | ✅ | ⚪ | ⚪ |
| `zero_load_full_soc_spare_boundary` |  | ✅ | ✅ | ⚪ | ⚪ |
| `res_covers_charge_below_full_soc` |  | ✅ | ✅ | ⚪ | ⚪ |
| `res_covers_spare_at_full_soc_boundary` |  | ✅ | ✅ | ⚪ | ⚪ |
| `battery_discharge_when_deficit_within_battery_capacity` |  | ✅ | ✅ | ⚪ | ⚪ |
| `lng_low_soc_pgmax_margin_within_capacity` |  | ✅ | ✅ | ⚪ | ⚪ |
| `lng_covers_deficit_after_battery_insufficient` |  | ✅ | ✅ | ⚪ | ⚪ |
| `lng_eng3_low_soc_pd1_margin` |  | ✅ | ✅ | ⚪ | ⚪ |
| `lng_eng3_covers_deficit_at_capacity_boundary` |  | ✅ | ✅ | ⚪ | ⚪ |
| `lng_eng3_dg1_low_soc_pd1_margin` |  | ✅ | ✅ | ⚪ | ⚪ |
| `all_thermal_within_capacity_uses_dg2_last` |  | ✅ | ✅ | ⚪ | ⚪ |
| `overload_activates_all_thermal_and_battery_lack` |  | ✅ | ✅ | ⚪ | ⚪ |
| `forced_reselection_from_overload_to_res_spare` |  | ✅ | ✅ | ⚪ | ⚪ |
| `forced_reselection_to_zero_load_charge_from_thermal` |  | ✅ | ✅ | ⚪ | ⚪ |
| `forced_reselection_to_lng_from_res_spare` |  | ✅ | ✅ | ⚪ | ⚪ |
| `wrong_target_probe_zero_load_to_res_charge` |  | ⚪ | ✅ | ⚪ | ⚪ |
| `wrong_target_probe_zero_load_to_res_spare` |  | ⚪ | ✅ | ⚪ | ⚪ |
| `wrong_target_probe_thermal_to_battery_discharge` |  | ⚪ | ✅ | ⚪ | ⚪ |
| `wrong_target_probe_overload_to_res_charge` |  | ⚪ | ✅ | ⚪ | ⚪ |
| `wrong_target_probe_res_charge_to_overload_lack` |  | ⚪ | ✅ | ⚪ | ⚪ |

#### 6.2 Scenario definitions

<details><summary>`wrong_target_probe_thermal_to_zero_load_spare` — explicit-hot-start: from a concrete thermal leaf, PL=0 with SoC at 0.95 must target ZeroLoadSpare, catching wrong-target mutations of the zero-load full-SoC bra...<truncated 4 chars></summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: from a concrete thermal leaf, PL=0 with SoC at 0.95 must target ZeroLoadSpare, catching wrong-target mutations of the zero-load full-SoC branch. |
| initial_state | `LNGShipEMS.AllThermalWithinCapacity` |
| initial_vars | `{"DG1_Pmax": 30.0, "DG2_Pmax": 20.0, "LNG_Pmax": 80.0, "PL": 0.0, "Ppv": 12.0, "Pw": 8.0, "SoC": 0.95, "batt_Pmax": 50.0, "eng3_Pmax": 30.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `thermal_retargets_to_zero_load_spare` | `0` | `[]` | `LNGShipEMS.ZeroLoadSpare` | `{"Pbatt_charge": 0.0, "Pbatt_discharge": 0.0, "Pgen_req": 0.0, "Pspare": 20.0, "cmd_DG1_cut_in": 0, "cmd_DG1_cut_out": 1, "cmd_DG2_cut_in": 0, "cmd_DG2_cut_out": 1, "cmd_LNG_cut_in": 0, "cmd_LNG_cut_out": 1, "cmd_eng3_cut_in": 0, "cmd_eng3_cut_out": 1, "cmd_load_cut_in": 0, "cmd_load_cut_out": 1}` |

</details>

<details><summary>`wrong_target_probe_zero_load_to_lng_low_soc_margin` — explicit-hot-start: from ZeroLoadCharge, low SoC and a deficit plus Pgmax/5 exactly within LNG capacity must target LNGLowSoCChargeMargin.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: from ZeroLoadCharge, low SoC and a deficit plus Pgmax/5 exactly within LNG capacity must target LNGLowSoCChargeMargin. |
| initial_state | `LNGShipEMS.ZeroLoadCharge` |
| initial_vars | `{"DG1_Pmax": 40.0, "DG2_Pmax": 40.0, "LNG_Pmax": 90.0, "PL": 100.0, "Pd1max": 100.0, "Pgmax": 50.0, "Ppv": 10.0, "Pw": 10.0, "SoC": 0.19, "batt_Pmax": 50.0, "eng3_Pmax": 40.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `zero_load_retargets_to_lng_low_soc_margin` | `0` | `[]` | `LNGShipEMS.LNGLowSoCChargeMargin` | `{"Pbatt_charge": 10.0, "Pbatt_discharge": 0.0, "Pgen_req": 90.0, "Pspare": 0.0, "cmd_DG1_cut_in": 0, "cmd_DG1_cut_out": 1, "cmd_DG2_cut_in": 0, "cmd_DG2_cut_out": 1, "cmd_LNG_cut_in": 1, "cmd_LNG_cut_out": 0, "cmd_eng3_cut_in": 0, "cmd_eng3_cut_out": 1, "cmd_load_cut_in": 1, "cmd_load_cut_out": 0}` |

</details>

<details><summary>`wrong_target_probe_zero_load_spare_to_lng_eng3_low_soc_margin` — explicit-hot-start: from ZeroLoadSpare, low SoC with LNG margin over LNG capacity but Pd1max/10 margin within LNG+eng3 must target LNGEng3LowSoCChargeMargin.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: from ZeroLoadSpare, low SoC with LNG margin over LNG capacity but Pd1max/10 margin within LNG+eng3 must target LNGEng3LowSoCChargeMargin. |
| initial_state | `LNGShipEMS.ZeroLoadSpare` |
| initial_vars | `{"DG1_Pmax": 40.0, "DG2_Pmax": 40.0, "LNG_Pmax": 90.0, "PL": 120.0, "Pd1max": 100.0, "Pgmax": 50.0, "Ppv": 10.0, "Pw": 10.0, "SoC": 0.19, "batt_Pmax": 20.0, "eng3_Pmax": 20.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `zero_load_spare_retargets_to_lng_eng3_low_soc` | `0` | `[]` | `LNGShipEMS.LNGEng3LowSoCChargeMargin` | `{"Pbatt_charge": 10.0, "Pbatt_discharge": 0.0, "Pgen_req": 110.0, "Pspare": 0.0, "cmd_DG1_cut_in": 0, "cmd_DG1_cut_out": 1, "cmd_DG2_cut_in": 0, "cmd_DG2_cut_out": 1, "cmd_LNG_cut_in": 1, "cmd_LNG_cut_out": 0, "cmd_eng3_cut_in": 1, "cmd_eng3_cut_out": 0, "cmd_load_cut_in": 1, "cmd_load_cut_out": 0}` |

</details>

<details><summary>`wrong_target_probe_res_spare_to_dg1_low_soc_margin` — explicit-hot-start: from RESCoversSpare, low SoC with deficit plus Pd1max/10 within LNG+eng3+DG1 must target LNGEng3DG1LowSoCChargeMargin and keep DG2 out.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: from RESCoversSpare, low SoC with deficit plus Pd1max/10 within LNG+eng3+DG1 must target LNGEng3DG1LowSoCChargeMargin and keep DG2 out. |
| initial_state | `LNGShipEMS.RESCoversSpare` |
| initial_vars | `{"DG1_Pmax": 40.0, "DG2_Pmax": 40.0, "LNG_Pmax": 80.0, "PL": 140.0, "Pd1max": 100.0, "Pgmax": 50.0, "Ppv": 10.0, "Pw": 10.0, "SoC": 0.19, "batt_Pmax": 20.0, "eng3_Pmax": 30.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `res_spare_retargets_to_dg1_low_soc_margin` | `0` | `[]` | `LNGShipEMS.LNGEng3DG1LowSoCChargeMargin` | `{"Pbatt_charge": 10.0, "Pbatt_discharge": 0.0, "Pgen_req": 130.0, "Pspare": 0.0, "cmd_DG1_cut_in": 1, "cmd_DG1_cut_out": 0, "cmd_DG2_cut_in": 0, "cmd_DG2_cut_out": 1, "cmd_LNG_cut_in": 1, "cmd_LNG_cut_out": 0, "cmd_eng3_cut_in": 1, "cmd_eng3_cut_out": 0, "cmd_load_cut_in": 1, "cmd_load_cut_out": 0}` |

</details>

<details><summary>`wrong_target_probe_overload_to_dg1_suitable_soc` — explicit-hot-start: from OverloadBatteryLack, suitable-SoC deficit above LNG+eng3 but within LNG+eng3+DG1 must target LNGEng3DG1CoversDeficit, not AllThermalWit...<truncated 12 chars></summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: from OverloadBatteryLack, suitable-SoC deficit above LNG+eng3 but within LNG+eng3+DG1 must target LNGEng3DG1CoversDeficit, not AllThermalWithinCapacity. |
| initial_state | `LNGShipEMS.OverloadBatteryLack` |
| initial_vars | `{"DG1_Pmax": 40.0, "DG2_Pmax": 40.0, "LNG_Pmax": 80.0, "PL": 150.0, "Pd1max": 100.0, "Pgmax": 50.0, "Ppv": 10.0, "Pw": 10.0, "SoC": 0.2, "batt_Pmax": 20.0, "eng3_Pmax": 30.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `overload_retargets_to_dg1_only_covers` | `0` | `[]` | `LNGShipEMS.LNGEng3DG1CoversDeficit` | `{"Pbatt_charge": 0.0, "Pbatt_discharge": 0.0, "Pgen_req": 130.0, "Pspare": 0.0, "cmd_DG1_cut_in": 1, "cmd_DG1_cut_out": 0, "cmd_DG2_cut_in": 0, "cmd_DG2_cut_out": 1, "cmd_LNG_cut_in": 1, "cmd_LNG_cut_out": 0, "cmd_eng3_cut_in": 1, "cmd_eng3_cut_out": 0, "cmd_load_cut_in": 1, "cmd_load_cut_out": 0}` |

</details>

<details><summary>`wrong_target_probe_res_charge_to_all_thermal` — explicit-hot-start: from RESCoversCharge, suitable-SoC deficit above LNG+eng3+DG1 but exactly within all thermal capacity must target AllThermalWithinCapacity.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: from RESCoversCharge, suitable-SoC deficit above LNG+eng3+DG1 but exactly within all thermal capacity must target AllThermalWithinCapacity. |
| initial_state | `LNGShipEMS.RESCoversCharge` |
| initial_vars | `{"DG1_Pmax": 30.0, "DG2_Pmax": 20.0, "LNG_Pmax": 80.0, "PL": 180.0, "Ppv": 10.0, "Pw": 10.0, "SoC": 0.5, "batt_Pmax": 50.0, "eng3_Pmax": 30.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `res_charge_retargets_to_all_thermal` | `0` | `[]` | `LNGShipEMS.AllThermalWithinCapacity` | `{"Pbatt_charge": 0.0, "Pbatt_discharge": 0.0, "Pgen_req": 160.0, "Pspare": 0.0, "cmd_DG1_cut_in": 1, "cmd_DG1_cut_out": 0, "cmd_DG2_cut_in": 1, "cmd_DG2_cut_out": 0, "cmd_LNG_cut_in": 1, "cmd_LNG_cut_out": 0, "cmd_eng3_cut_in": 1, "cmd_eng3_cut_out": 0, "cmd_load_cut_in": 1, "cmd_load_cut_out": 0}` |

</details>

<details><summary>`wrong_target_probe_lng_to_overload_lack` — explicit-hot-start: from LNGCoversDeficit, extreme demand above all thermal capacity but within battery lack coverage must target OverloadBatteryLack.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: from LNGCoversDeficit, extreme demand above all thermal capacity but within battery lack coverage must target OverloadBatteryLack. |
| initial_state | `LNGShipEMS.LNGCoversDeficit` |
| initial_vars | `{"DG1_Pmax": 30.0, "DG2_Pmax": 20.0, "LNG_Pmax": 80.0, "PL": 220.0, "Ppv": 10.0, "Pw": 10.0, "SoC": 0.5, "batt_Pmax": 100.0, "eng3_Pmax": 30.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `lng_retargets_to_overload_lack` | `0` | `[]` | `LNGShipEMS.OverloadBatteryLack` | `{"Pbatt_charge": 0.0, "Pbatt_discharge": 40.0, "Pgen_req": 160.0, "Pspare": 0.0, "cmd_DG1_cut_in": 1, "cmd_DG1_cut_out": 0, "cmd_DG2_cut_in": 1, "cmd_DG2_cut_out": 0, "cmd_LNG_cut_in": 1, "cmd_LNG_cut_out": 0, "cmd_eng3_cut_in": 1, "cmd_eng3_cut_out": 0, "cmd_load_cut_in": 1, "cmd_load_cut_out": 0, "overload_illegal": 1}` |

</details>

<details><summary>`wrong_target_probe_battery_to_lng_eng3_suitable_soc` — explicit-hot-start: from RESBatteryDischarge, suitable-SoC deficit above LNG alone but exactly within LNG+eng3 must target LNGEng3CoversDeficit.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: from RESBatteryDischarge, suitable-SoC deficit above LNG alone but exactly within LNG+eng3 must target LNGEng3CoversDeficit. |
| initial_state | `LNGShipEMS.RESBatteryDischarge` |
| initial_vars | `{"DG1_Pmax": 40.0, "DG2_Pmax": 40.0, "LNG_Pmax": 80.0, "PL": 120.0, "Ppv": 10.0, "Pw": 10.0, "SoC": 0.2, "batt_Pmax": 20.0, "eng3_Pmax": 20.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `battery_retargets_to_lng_eng3_covers` | `0` | `[]` | `LNGShipEMS.LNGEng3CoversDeficit` | `{"Pbatt_charge": 0.0, "Pbatt_discharge": 0.0, "Pgen_req": 100.0, "Pspare": 0.0, "cmd_DG1_cut_in": 0, "cmd_DG1_cut_out": 1, "cmd_DG2_cut_in": 0, "cmd_DG2_cut_out": 1, "cmd_LNG_cut_in": 1, "cmd_LNG_cut_out": 0, "cmd_eng3_cut_in": 1, "cmd_eng3_cut_out": 0, "cmd_load_cut_in": 1, "cmd_load_cut_out": 0}` |

</details>

<details><summary>`default_init_zero_load_charge_dispatch` — default-init: first cycle must dispatch the root initial transition to ZeroLoadCharge and charge batteries from RES when PL=0 and SoC is below 0.95.</summary>

| Field | Value |
|---|---|
| description | default-init: first cycle must dispatch the root initial transition to ZeroLoadCharge and charge batteries from RES when PL=0 and SoC is below 0.95. |
| initial_state | `<default-init>` |
| initial_vars | `{"DG1_Pmax": 30.0, "DG2_Pmax": 20.0, "LNG_Pmax": 80.0, "PL": 0.0, "Ppv": 12.0, "Pw": 8.0, "SoC": 0.5, "batt_Pmax": 50.0, "eng3_Pmax": 30.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `initial_leaf_zero_load_charge` | `0` | `[]` | `LNGShipEMS.ZeroLoadCharge` | `{"Pbatt_charge": 20.0, "Pbatt_discharge": 0.0, "Pgen_req": 0.0, "Pspare": 0.0, "cmd_DG1_cut_in": 0, "cmd_DG1_cut_out": 1, "cmd_DG2_cut_in": 0, "cmd_DG2_cut_out": 1, "cmd_LNG_cut_in": 0, "cmd_LNG_cut_out": 1, "cmd_eng3_cut_in": 0, "cmd_eng3_cut_out": 1, "cmd_load_cut_in": 0, "cmd_load_cut_out": 1}` |

</details>

<details><summary>`missing_forced_probe_battery_to_zero_load_charge` — explicit-hot-start: from RESBatteryDischarge, a zero-load low-SoC condition must be globally reselected to ZeroLoadCharge, exposing deletion of the wildcard for...<truncated 32 chars></summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: from RESBatteryDischarge, a zero-load low-SoC condition must be globally reselected to ZeroLoadCharge, exposing deletion of the wildcard forced zero-load charge transition. |
| initial_state | `LNGShipEMS.RESBatteryDischarge` |
| initial_vars | `{"DG1_Pmax": 30.0, "DG2_Pmax": 20.0, "LNG_Pmax": 80.0, "PL": 0.0, "Ppv": 12.0, "Pw": 8.0, "SoC": 0.94, "batt_Pmax": 50.0, "eng3_Pmax": 30.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `forced_reselects_zero_load_charge` | `0` | `[]` | `LNGShipEMS.ZeroLoadCharge` | `{"Pbatt_charge": 20.0, "Pbatt_discharge": 0.0, "Pgen_req": 0.0, "Pspare": 0.0, "cmd_DG1_cut_in": 0, "cmd_DG1_cut_out": 1, "cmd_DG2_cut_in": 0, "cmd_DG2_cut_out": 1, "cmd_LNG_cut_in": 0, "cmd_LNG_cut_out": 1, "cmd_eng3_cut_in": 0, "cmd_eng3_cut_out": 1, "cmd_load_cut_in": 0, "cmd_load_cut_out": 1}` |

</details>

<details><summary>`boundary_soc_095_res_cover_spare` — explicit-hot-start: at the exact SoC=0.95 RES-covered threshold, the EMS must treat residual renewable power as spare, catching high-threshold or unreachable-ta...<truncated 15 chars></summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: at the exact SoC=0.95 RES-covered threshold, the EMS must treat residual renewable power as spare, catching high-threshold or unreachable-target mutations. |
| initial_state | `LNGShipEMS.LNGEng3CoversDeficit` |
| initial_vars | `{"DG1_Pmax": 30.0, "DG2_Pmax": 20.0, "LNG_Pmax": 80.0, "PL": 90.0, "Ppv": 60.0, "Pw": 40.0, "SoC": 0.95, "batt_Pmax": 50.0, "eng3_Pmax": 30.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `exact_soc_threshold_reselects_res_spare` | `0` | `[]` | `LNGShipEMS.RESCoversSpare` | `{"Pbatt_charge": 0.0, "Pbatt_discharge": 0.0, "Pgen_req": 0.0, "Pspare": 10.0, "cmd_DG1_cut_in": 0, "cmd_DG1_cut_out": 1, "cmd_DG2_cut_in": 0, "cmd_DG2_cut_out": 1, "cmd_LNG_cut_in": 0, "cmd_LNG_cut_out": 1, "cmd_eng3_cut_in": 0, "cmd_eng3_cut_out": 1, "cmd_load_cut_in": 1, "cmd_load_cut_out": 0}` |

</details>

<details><summary>`boundary_battery_deficit_equals_batt_pmax` — explicit-hot-start: with suitable SoC and deficit exactly equal to batt_Pmax, the EMS must use battery discharge rather than LNG, catching capacity-threshold an...<truncated 31 chars></summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: with suitable SoC and deficit exactly equal to batt_Pmax, the EMS must use battery discharge rather than LNG, catching capacity-threshold and unreachable-target mutations. |
| initial_state | `LNGShipEMS.LNGCoversDeficit` |
| initial_vars | `{"DG1_Pmax": 30.0, "DG2_Pmax": 20.0, "LNG_Pmax": 80.0, "PL": 70.0, "Ppv": 10.0, "Pw": 10.0, "SoC": 0.2, "batt_Pmax": 50.0, "eng3_Pmax": 30.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `exact_battery_capacity_reselects_battery_discharge` | `0` | `[]` | `LNGShipEMS.RESBatteryDischarge` | `{"Pbatt_charge": 0.0, "Pbatt_discharge": 50.0, "Pgen_req": 0.0, "Pspare": 0.0, "cmd_DG1_cut_in": 0, "cmd_DG1_cut_out": 1, "cmd_DG2_cut_in": 0, "cmd_DG2_cut_out": 1, "cmd_LNG_cut_in": 0, "cmd_LNG_cut_out": 1, "cmd_eng3_cut_in": 0, "cmd_eng3_cut_out": 1, "cmd_load_cut_in": 1, "cmd_load_cut_out": 0}` |

</details>

<details><summary>`unreachable_target_probe_res_cover_charge` — explicit-hot-start: RES covers a positive load with SoC just below 0.95, so EMS must target RESCoversCharge; catches wrong-target and guard-too-high mutations o...<truncated 24 chars></summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: RES covers a positive load with SoC just below 0.95, so EMS must target RESCoversCharge; catches wrong-target and guard-too-high mutations on the RES charge branch. |
| initial_state | `LNGShipEMS.AllThermalWithinCapacity` |
| initial_vars | `{"DG1_Pmax": 30.0, "DG2_Pmax": 20.0, "LNG_Pmax": 80.0, "PL": 90.0, "Ppv": 60.0, "Pw": 40.0, "SoC": 0.94, "batt_Pmax": 50.0, "eng3_Pmax": 30.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `res_surplus_charges_battery` | `0` | `[]` | `LNGShipEMS.RESCoversCharge` | `{"Pbatt_charge": 10.0, "Pbatt_discharge": 0.0, "Pgen_req": 0.0, "Pspare": 0.0, "cmd_DG1_cut_in": 0, "cmd_DG1_cut_out": 1, "cmd_DG2_cut_in": 0, "cmd_DG2_cut_out": 1, "cmd_LNG_cut_in": 0, "cmd_LNG_cut_out": 1, "cmd_eng3_cut_in": 0, "cmd_eng3_cut_out": 1, "cmd_load_cut_in": 1, "cmd_load_cut_out": 0}` |

</details>

<details><summary>`unreachable_target_probe_overload_lack_boundary` — explicit-hot-start: from RESBatteryDischarge, extreme demand exceeding all thermal resources with battery lack exactly equal to batt_Pmax must target OverloadBa...<truncated 70 chars></summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: from RESBatteryDischarge, extreme demand exceeding all thermal resources with battery lack exactly equal to batt_Pmax must target OverloadBatteryLack; catches guard-too-high and wrong-target overload mutations. |
| initial_state | `LNGShipEMS.RESBatteryDischarge` |
| initial_vars | `{"DG1_Pmax": 30.0, "DG2_Pmax": 20.0, "LNG_Pmax": 80.0, "PL": 220.0, "Ppv": 10.0, "Pw": 10.0, "SoC": 0.2, "batt_Pmax": 40.0, "eng3_Pmax": 30.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `overload_lack_equals_battery_capacity` | `0` | `[]` | `LNGShipEMS.OverloadBatteryLack` | `{"Pbatt_charge": 0.0, "Pbatt_discharge": 40.0, "Pgen_req": 160.0, "Pspare": 0.0, "cmd_DG1_cut_in": 1, "cmd_DG1_cut_out": 0, "cmd_DG2_cut_in": 1, "cmd_DG2_cut_out": 0, "cmd_LNG_cut_in": 1, "cmd_LNG_cut_out": 0, "cmd_eng3_cut_in": 1, "cmd_eng3_cut_out": 0, "cmd_load_cut_in": 1, "cmd_load_cut_out": 0, "overload_illegal": 1}` |

</details>


### 7. Repair / blocking feedback 明细

口径：本节记录 agent-loop 真实进入 repair block 后的证据链：FixRequestBatch、SL-9 per-request accept/reject、candidate diff、local-check evidence、SL-10(NL+FixLog) 审阅，以及完整 FixLog ledger 摘录。

| Repair | iteration | accepted | source | blocking diagnostics | SL-9 decisions | SL-10 / local checks | candidate hash |
|---:|---:|---:|---|---|---|---|---|
| 1 | `0` | ❌ | `SL-7` | 0 | accept=1, reject=0, waiver=0 | SL-10 decision=rework, ok=False, target=True, regression=False, drift=minor, rework=SL-10 pass was downgraded because local deterministic evidence reported major drift and SL-10 evidence did not explicitly address the local rejection reason/kind with a structu...<truncated 678 chars> | `sha256:c4422351d34de68230c5a6f4f43ae04421c7e963fa641dd7ca3c3377d63d966a` |
| 2 | `0` | ❌ | `SL-7` | 0 | accept=1, reject=0, waiver=0 | SL-10 decision=rework, ok=False, target=True, regression=False, drift=minor, rework=SL-10 pass was downgraded because local deterministic evidence reported major drift and SL-10 evidence did not explicitly address the local rejection reason/kind with a structu...<truncated 658 chars> | `sha256:a3d167d8c7d32fd212b403f7d77af2d6db6d5c6d03fe6f1bbf42cc671ee351be` |
| 3 | `0` | ❌ | `SL-7` | 0 | accept=1, reject=0, waiver=0 | SL-10 decision=rework, ok=False, target=True, regression=False, drift=minor, rework=SL-10 pass was downgraded because local deterministic evidence reported major drift and SL-10 evidence did not explicitly address the local rejection reason/kind with a structu...<truncated 690 chars> | `sha256:fa9a662af2c91e5cca5f3f32570c28a50c1745f2db60dc535a9ee953a9402ac3` |
| 4 | `0` | ❌ | `SL-7` | 0 | accept=1, reject=0, waiver=0 | SL-10 decision=rework, ok=False, target=True, regression=False, drift=minor, rework=SL-10 pass was downgraded because local deterministic evidence reported major drift and SL-10 evidence did not explicitly address the local rejection reason/kind with a structu...<truncated 658 chars> | `sha256:a3d167d8c7d32fd212b403f7d77af2d6db6d5c6d03fe6f1bbf42cc671ee351be` |
| 5 | `0` | ✅ | `SL-7` | 0 | accept=1, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none>; local ok=False, target=False, regression=False, drift=major, local_stage=SD-10, reason=forced_transition_count_drift; missing_required_grounding | `sha256:813b635ee38132f66b9e8cd1fbf754f73d5598598eca4acef2ded16fddad4376` |
| 6 | `1` | ✅ | `SL-7` | 0, 1, 2 | accept=3, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none>; local ok=False, target=False, regression=False, drift=major, local_stage=SD-10, reason=forced_transition_count_drift; missing_required_grounding | `sha256:ad6bb952e971dcc754c511a5baf3833ec55994c5a265657833e894faa5829c16` |
| 7 | `2` | ❌ | `SL-7` | 0, 1 | accept=2, reject=0, waiver=0 | SL-10 decision=rework, ok=False, target=False, regression=True, drift=major, rework=Restore concrete guarded inbound transitions from normal dispatch states to OverloadBatteryLack for the strengthened overload condition: PL > 0, Ppv + Pw < PL, PL - Ppv - Pw > ...<truncated 628 chars> | `sha256:0aac73439d9e4fa4e943fc2d2cead8b9851b5b7084ee281ee912e5eb12f35388` |
| 8 | `2` | ✅ | `SL-7` | 0, 1 | accept=2, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none>; local ok=False, target=False, regression=False, drift=major, local_stage=SD-10, reason=missing_required_grounding | `sha256:68ddc851c3efde1e421625c439cb0b4d3f522b929c9a90d9cd77dcf3cd76d501` |

<details><summary>Repair 1 / iteration `0` / source `SL-7` / accepted=❌</summary>

#### 为什么进入修复

- selected feedback source：`SL-7`；blocking=`True`；pre_scenario=`False`。
- problem_summary：model review failed
- diagnostic ids：`0`。
- before_dsl_hash：`sha256:01c5a57aa10618b447f8a2a830a9d8e06062db2bafb5fe2ac26d66485929c533`；candidate_dsl_hash：`sha256:c4422351d34de68230c5a6f4f43ae04421c7e963fa641dd7ca3c3377d63d966a`。

#### 错误证据 / diagnostics

- 1. `<unknown>` `` policy=``：The illegal overload state is treated as an ordinary reachable recovery/dispatch state and can command continued load service plus battery discharge without suitability or capacity guards.

#### SD-8 FixRequestBatch / 修改请求

- batch_id：`fixbatch-0-sha256-081cf0a961f`；source_stage=`SL-7`；legacy_plan_kind=`FixPlan`；requests=`1`。

| request_id | severity | hard | waiver | problem | evidence |
|---|---|---:|---:|---|---|
| `fixreq-0-sl7-0-be1e03bda7` | `review_fail` | ✅ | ❌ | model review failed | `{'category': 'unsafe_recovery', 'evidence': ['NL: "The overload completion state is illegal... the state shall never occur in practice."', 'DSL forced transition reaches `OverloadBatteryLack` whenever demand exceeds all RES and thermal resources.', '`OverloadBatteryLack` sets `cmd_load_cut_in = 1`, `cmd_load_cut_out = 0`, and computes `Pbatt_discharge` from the remaining lack without checking `SoC` or `batt_Pmax`.', 'sim_summary includes a passing overload scenario, showing this branch is accepted as normal behavior rather than flagged as illegal.'], 'severity': 'major', 'summary': 'The illegal overload state is treated as an ordinary reachable recovery/dispatch state and can command continued load service plus battery discharge without suitability or capacity guards.'}` |

#### SD-8 legacy fix plan / 修改建议

- recommended_strategy：Use diagnostics as hints; choose the smallest globally consistent repair.；Before returning a candidate, verify every required_preserve_element_id still has a concrete DSL representation.
- forbidden_edits：`Do not delete grounded required elements merely to silence diagnostics., Do not invent internal plant/environment dynamics merely to make external input variables appear written.`。
- required_preserve_element_ids：`state:ZeroLoadCharge, state:ZeroLoadSpare, state:RESCoversCharge, state:RESCoversSpare, state:RESBatteryDischarge, state:LNGLowSoCChargeMargin, state:LNGCoversDeficit, state:LNGEng3LowSoCChargeMargin, state:LNGEng3CoversDeficit, state:LNGEng3DG1LowSoCChargeMargin, state:AllThermalWithinCapacity, state:OverloadBatteryLack, ... +18`。

#### SL-9 per-request 决策

- accepted_request_ids：`<derived-from-table>`；candidate_len=`8708`。

| request_id | decision | waiver | rework_locked | rationale / intent |
|---|---|---:|---:|---|
| `fixreq-0-sl7-0-be1e03bda7` | `accept` | ❌ | ❌ | The review evidence is valid: the overload branch was reachable for any demand above RES plus thermal capacity and commanded normal load service while computing unbounded battery discharge. The smallest safe repair preserves the required OverloadBatteryLack state, guard, and dispatch action, but constrains entry to cases where battery discharge is actually s...<truncated 385 chars> |
- repair_rationale：Accepted the single hard SL-7 model-review request because the overload branch was NL-grounded but unsafe as an ordinary dispatch/recovery state.；Preserved all twelve required states, including OverloadBatteryLack, and preserved required variables, RES guard branches, the overload guard, and the overload dispatch action that activates all thermal units and computes battery lack disch...<truncated 5 chars>；The OverloadBatteryLack guard now additionally requires SoC >= 0.2 and the residual lack after all thermal resources to be within batt_Pmax, resolving the evidence that battery discharge was unbounded and not suitability-guarded.；The OverloadBatteryLack state now commands load cut-out rather than continued normal load cut-in, so the illegal overload condition is no longer modeled as ordinary accepted load service.；No external input dynamics were invented; PL, Ppv, Pw, SoC, and capacity bounds remain externally read classification inputs.
- diff_summary：`{"summary": "Changed only the overload branch: added battery suitability/capacity constraints to the forced OverloadBatteryLack guard, and changed OverloadBatteryLack load commands from cmd_load_cut_in=1/cmd_load_cut_out=0 to cmd_load_cut_in=0/cmd_load_cut_out=1. All other states, variables, guards, and dispatch actions are preserved."}`。

#### SL-9 candidate / 最终修改执行方案

```pyfcstm
def float PL = 0.0;
def float Ppv = 0.0;
def float Pw = 0.0;
def float SoC = 0.5;
def float batt_Pmax = 0.0;
def float LNG_Pmax = 0.0;
def float eng3_Pmax = 0.0;
def float DG1_Pmax = 0.0;
def float DG2_Pmax = 0.0;
def float Pgmax = 0.0;
def float Pd1max = 0.0;
def float Pgen_req = 0.0;
def float Pbatt_discharge = 0.0;
def float Pbatt_charge = 0.0;
def float Pspare = 0.0;
def int cmd_LNG_cut_in = 0;
def int cmd_LNG_cut_out = 1;
def int cmd_eng3_cut_in = 0;
def int cmd_eng3_cut_out = 1;
def int cmd_DG1_cut_in = 0;
def int cmd_DG1_cut_out = 1;
def int cmd_DG2_cut_in = 0;
def int cmd_DG2_cut_out = 1;
def int cmd_load_cut_in = 1;
def int cmd_load_cut_out = 0;

state LNGShipEMS {
    ! * -> ZeroLoadCharge : if [PL == 0 && Ppv + Pw > 0 && SoC < 0.95];
    ! * -> ZeroLoadSpare : if [PL == 0 && SoC >= 0.95];
    ! * -> RESCoversCharge : if [PL > 0 && Ppv + Pw >= PL && SoC < 0.95];
    ! * -> RESCoversSpare : if [PL > 0 && Ppv + Pw >= PL && SoC >= 0.95];
    ! * -> RESBatteryDischarge : if [PL > 0 && Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw <= batt_Pmax];
    ! * -> LNGLowSoCChargeMargin : if [PL > 0 && Ppv + Pw < PL && SoC < 0.2 && PL - Ppv - Pw + Pgmax / 5 <= LNG_Pmax];
    ! * -> LNGCoversDeficit : if [PL > 0 && Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw > batt_Pmax && PL - Ppv - Pw <= LNG_Pmax];
    ! * -> LNGEng3LowSoCChargeMargin : if [PL > 0 && Ppv + Pw < PL && SoC < 0.2 && PL - Ppv - Pw + Pgmax / 5 > LNG_Pmax && PL - Ppv - Pw + Pd1max / 10 <= LNG_Pmax + eng3_Pmax];
    ! * -> LNGEng3CoversDeficit : if [PL > 0 && Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw > LNG_Pmax && PL - Ppv - Pw <= LNG_Pmax + eng3_Pmax];
    ! * -> LNGEng3DG1LowSoCChargeMargin : if [PL > 0 && Ppv + Pw < PL && SoC < 0.2 && PL - Ppv - Pw + Pd1max / 10 > LNG_Pmax + eng3_Pmax && PL - Ppv - Pw + Pd1max / 10 <= LNG_Pmax + eng3_Pmax + DG1_Pmax];
    ! * -> AllThermalWithinCapacity : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > LNG_Pmax + eng3_Pmax && PL - Ppv - Pw <= LNG_Pmax + eng3_Pmax + DG1_Pmax + DG2_Pmax];
    ! * -> OverloadBatteryLack : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > LNG_Pmax + eng3_Pmax + DG1_Pmax + DG2_Pmax && SoC >= 0.2 && PL - Ppv - Pw - LNG_Pmax - eng3_Pmax - DG1_Pmax - DG2_Pmax <= batt_Pmax];

    [*] -> ZeroLoadCharge;

    state ZeroLoadCharge {
        during {
            Pgen_req = 0.0;
            Pbatt_discharge = 0.0;
            Pbatt_charge = Ppv + Pw;
            Pspare = 0.0;
            cmd_LNG_cut_in = 0;
            cmd_LNG_cut_out = 1;
            cmd_eng3_cut_in = 0;
            cmd_eng3_cut_out = 1;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 0;
            cmd_load_cut_out = 1;
        }
    }

    state ZeroLoadSpare {
        during {
            Pgen_req = 0.0;
            Pbatt_discharge = 0.0;
            Pbatt_charge = 0.0;
            Pspare = Ppv + Pw;
            cmd_LNG_cut_in = 0;
            cmd_LNG_cut_out = 1;
            cmd_eng3_cut_in = 0;
            cmd_eng3_cut_out = 1;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 0;
            cmd_load_cut_out = 1;
        }
    }

    state RESCoversCharge {
        during {
            Pgen_req = 0.0;
            Pbatt_discharge = 0.0;
            Pbatt_charge = Ppv + Pw - PL;
            Pspare = 0.0;
            cmd_LNG_cut_in = 0;
            cmd_LNG_cut_out = 1;
            cmd_eng3_cut_in = 0;
            cmd_eng3_cut_out = 1;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state RESCoversSpare {
        during {
            Pgen_req = 0.0;
            Pbatt_discharge = 0.0;
            Pbatt_charge = 0.0;
            Pspare = Ppv + Pw - PL;
            cmd_LNG_cut_in = 0;
            cmd_LNG_cut_out = 1;
            cmd_eng3_cut_in = 0;
            cmd_eng3_cut_out = 1;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state RESBatteryDischarge {
        during {
            Pgen_req = 0.0;
            Pbatt_discharge = PL - Ppv - Pw;
            Pbatt_charge = 0.0;
            Pspare = 0.0;
            cmd_LNG_cut_in = 0;
            cmd_LNG_cut_out = 1;
            cmd_eng3_cut_in = 0;
            cmd_eng3_cut_out = 1;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state LNGLowSoCChargeMargin {
        during {
            Pgen_req = PL - Ppv - Pw + Pgmax / 5;
            Pbatt_discharge = 0.0;
            Pbatt_charge = Pgmax / 5;
            Pspare = 0.0;
            cmd_LNG_cut_in = 1;
            cmd_LNG_cut_out = 0;
            cmd_eng3_cut_in = 0;
            cmd_eng3_cut_out = 1;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state LNGCoversDeficit {
        during {
            Pgen_req = PL - Ppv - Pw;
            Pbatt_discharge = 0.0;
            Pbatt_charge = 0.0;
            Pspare = 0.0;
            cmd_LNG_cut_in = 1;
            cmd_LNG_cut_out = 0;
            cmd_eng3_cut_in = 0;
            cmd_eng3_cut_out = 1;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state LNGEng3LowSoCChargeMargin {
        during {
            Pgen_req = PL - Ppv - Pw + Pd1max / 10;
            Pbatt_discharge = 0.0;
            Pbatt_charge = Pd1max / 10;
            Pspare = 0.0;
            cmd_LNG_cut_in = 1;
            cmd_LNG_cut_out = 0;
            cmd_eng3_cut_in = 1;
            cmd_eng3_cut_out = 0;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state LNGEng3CoversDeficit {
        during {
            Pgen_req = PL - Ppv - Pw;
            Pbatt_discharge = 0.0;
            Pbatt_charge = 0.0;
            Pspare = 0.0;
            cmd_LNG_cut_in = 1;
            cmd_LNG_cut_out = 0;
            cmd_eng3_cut_in = 1;
            cmd_eng3_cut_out = 0;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state LNGEng3DG1LowSoCChargeMargin {
        during {
            Pgen_req = PL - Ppv - Pw + Pd1max / 10;
            Pbatt_discharge = 0.0;
            Pbatt_charge = Pd1max / 10;
            Pspare = 0.0;
            cmd_LNG_cut_in = 1;
            cmd_LNG_cut_out = 0;
            cmd_eng3_cut_in = 1;
            cmd_eng3_cut_out = 0;
            cmd_DG1_cut_in = 1;
            cmd_DG1_cut_out = 0;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state AllThermalWithinCapacity {
        during {
            Pgen_req = PL - Ppv - Pw;
            Pbatt_discharge = 0.0;
            Pbatt_charge = 0.0;
            Pspare = 0.0;
            cmd_LNG_cut_in = 1;
            cmd_LNG_cut_out = 0;
            cmd_eng3_cut_in = 1;
            cmd_eng3_cut_out = 0;
            cmd_DG1_cut_in = 1;
            cmd_DG1_cut_out = 0;
            cmd_DG2_cut_in = 1;
            cmd_DG2_cut_out = 0;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state OverloadBatteryLack {
        during {
            Pgen_req = LNG_Pmax + eng3_Pmax + DG1_Pmax + DG2_Pmax;
            Pbatt_discharge = PL - Ppv - Pw - LNG_Pmax - eng3_Pmax - DG1_Pmax - DG2_Pmax;
            Pbatt_charge = 0.0;
            Pspare = 0.0;
            cmd_LNG_cut_in = 1;
            cmd_LNG_cut_out = 0;
            cmd_eng3_cut_in = 1;
            cmd_eng3_cut_out = 0;
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

#### Candidate diff（before -> candidate）

```diff
--- before.fcstm
+++ candidate.fcstm
@@ -36,7 +36,7 @@
     ! * -> LNGEng3CoversDeficit : if [PL > 0 && Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw > LNG_Pmax && PL - Ppv - Pw <= LNG_Pmax + eng3_Pmax];
     ! * -> LNGEng3DG1LowSoCChargeMargin : if [PL > 0 && Ppv + Pw < PL && SoC < 0.2 && PL - Ppv - Pw + Pd1max / 10 > LNG_Pmax + eng3_Pmax && PL - Ppv - Pw + Pd1max / 10 <= LNG_Pmax + eng3_Pmax + DG1_Pmax];
     ! * -> AllThermalWithinCapacity : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > LNG_Pmax + eng3_Pmax && PL - Ppv - Pw <= LNG_Pmax + eng3_Pmax + DG1_Pmax + DG2_Pmax];
-    ! * -> OverloadBatteryLack : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > LNG_Pmax + eng3_Pmax + DG1_Pmax + DG2_Pmax];
+    ! * -> OverloadBatteryLack : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > LNG_Pmax + eng3_Pmax + DG1_Pmax + DG2_Pmax && SoC >= 0.2 && PL - Ppv - Pw - LNG_Pmax - eng3_Pmax - DG1_Pmax - DG2_Pmax <= batt_Pmax];
 
     [*] -> ZeroLoadCharge;
 
@@ -263,8 +263,8 @@
             cmd_DG1_cut_out = 0;
             cmd_DG2_cut_in = 1;
             cmd_DG2_cut_out = 0;
-            cmd_load_cut_in = 1;
-            cmd_load_cut_out = 0;
+            cmd_load_cut_in = 0;
+            cmd_load_cut_out = 1;
         }
     }
 }
```

#### SL-10 审查结果

- SL-10 decision=`rework`，ok=`False`，target_resolved=`True`，regression_detected=`False`，drift_risk=`minor`。
- SL-10 review_meta：schema=`SL10RepairReviewOutput.v1`，failure_policy=`fail_closed`，replay_key=`SL-10:sha256:46645da8755987c4005593abc2356eb58dc32edcae456a4514457b0178c77abf`。
  - SL-10 evidence 1: `{"summary": "The single hard SL-7 request targeted unsafe_recovery: OverloadBatteryLack was reachable whenever demand exceeded RES plus thermal capacity, commanded normal load service, and computed unbounded battery discharge without SoC or batt_Pmax suitability. SL-9 accepted that request and made a narrow diff limited to the overload branch: the OverloadBatteryLack guard now requires SoC >= 0.2 and residual lack after all thermal resources <= batt_Pmax, and the state now commands cmd_load_cut_in = 0 / cmd_load_cut_out = 1 instead of ordinary load service. This directly addresses the unsafe battery-discharge and ordinary-service objections while preserving the required OverloadBatteryLack s...<truncated 82 chars>`
  - SL-10 evidence 2: `{"summary": "The NL states both that extreme demand activates all thermal generating units and covers the lack by battery discharge, and that the overload completion state is illegal and shall never occur in practice. The candidate still activates LNG, eng3, DG1, and DG2, sets Pgen_req to total thermal capacity, computes Pbatt_discharge as the residual lack, and preserves the OverloadBatteryLack state/guard/action. The added SoC/batt_Pmax constraints and load cut-out command are consistent with treating this as an illegal/emergency branch rather than normal accepted load service."}`
  - SL-10 evidence 3: `{"summary": "The diff summary and DSL show no deletion of NL-required states, variables, RES guards, or dispatch outputs. All twelve required states remain present; required inputs PL, Ppv, Pw, SoC, eng3_Pmax, Pgmax, and Pd1max remain; required outputs Pgen_req, Pbatt_discharge, Pbatt_charge, and Pspare remain; and required generator cut-in commands remain. All non-overload scenarios in local simulation still pass, supporting that the repair did not disturb the normal dispatch priority branches."}`
- SL-10 rework_instructions：SL-10 pass was downgraded because local deterministic evidence reported major drift and SL-10 evidence did not explicitly address the local rejection reason/kind with a structured local_override_rationale.；For the next SL-9 repair, do not blindly regenerate the same DSL. Either change the candidate so the local major-drift evidence is resolved, or keep the minimal DSL only with explicit repair_rationale mapping each local objection (for example missing_required_grounding, scenario_regression, count_drift, or forced_transition_count_drift) to concrete NL-ground...<truncated 152 chars>
- local checks evidence：stage=`SD-10`；note=PR-E1 uses local parse/semantic/design/sim checks as SL-10 evidence, not as the final deterministic judge.。
  - local ok=`False`，target_resolved=`False`，regression_detected=`True`，drift_risk=`major`。
  - local_rejection：reason=`scenario_regression; missing_required_grounding`，rejected_by_stage=`SD-10`。
    - local evidence 1: `scenario_regression` {"kind": "scenario_regression", "sim_feedback": {"n_scenarios": 15, "n_scenarios_passed": 14, "ok": false, "oracle_weak": false, "scenario_results": [{"description": "default-init: with zero load, renewable production, and SoC below 0.95, the initial dispatch should land in ZeroLoadCharge and send RES power to battery charging.", "name": "default_init_zero_load_res_charges_battery", "setup_error": null, "status": "pass", "step_results": [{"actual_state": "LNGShipEMS.ZeroLoadCharge", "actual_vars...<truncated 15054 chars>
    - local evidence 2: `missing_required_grounding` {"element_ids": ["guard:RESCoversCharge", "guard:RESCoversSpare", "guard:OverloadBatteryLack"], "kind": "missing_required_grounding"}

</details>

<details><summary>Repair 2 / iteration `0` / source `SL-7` / accepted=❌</summary>

#### 为什么进入修复

- selected feedback source：`SL-7`；blocking=`True`；pre_scenario=`False`。
- problem_summary：model review failed
- diagnostic ids：`0`。
- before_dsl_hash：`sha256:01c5a57aa10618b447f8a2a830a9d8e06062db2bafb5fe2ac26d66485929c533`；candidate_dsl_hash：`sha256:a3d167d8c7d32fd212b403f7d77af2d6db6d5c6d03fe6f1bbf42cc671ee351be`。

#### 错误证据 / diagnostics

- 1. `<unknown>` `` policy=``：The illegal overload state is treated as an ordinary reachable recovery/dispatch state and can command continued load service plus battery discharge without suitability or capacity guards.

#### SD-8 FixRequestBatch / 修改请求

- batch_id：`fixbatch-0-sha256-081cf0a961f`；source_stage=`SL-7`；legacy_plan_kind=`FixPlan`；requests=`1`。

| request_id | severity | hard | waiver | problem | evidence |
|---|---|---:|---:|---|---|
| `fixreq-0-sl7-0-be1e03bda7` | `review_fail` | ✅ | ❌ | model review failed | `{'category': 'unsafe_recovery', 'evidence': ['NL: "The overload completion state is illegal... the state shall never occur in practice."', 'DSL forced transition reaches `OverloadBatteryLack` whenever demand exceeds all RES and thermal resources.', '`OverloadBatteryLack` sets `cmd_load_cut_in = 1`, `cmd_load_cut_out = 0`, and computes `Pbatt_discharge` from the remaining lack without checking `SoC` or `batt_Pmax`.', 'sim_summary includes a passing overload scenario, showing this branch is accepted as normal behavior rather than flagged as illegal.'], 'severity': 'major', 'summary': 'The illegal overload state is treated as an ordinary reachable recovery/dispatch state and can command continued load service plus battery discharge without suitability or capacity guards.'}` |

#### SD-8 legacy fix plan / 修改建议

- recommended_strategy：Use diagnostics as hints; choose the smallest globally consistent repair.；Before returning a candidate, verify every required_preserve_element_id still has a concrete DSL representation.
- forbidden_edits：`Do not delete grounded required elements merely to silence diagnostics., Do not invent internal plant/environment dynamics merely to make external input variables appear written.`。
- required_preserve_element_ids：`state:ZeroLoadCharge, state:ZeroLoadSpare, state:RESCoversCharge, state:RESCoversSpare, state:RESBatteryDischarge, state:LNGLowSoCChargeMargin, state:LNGCoversDeficit, state:LNGEng3LowSoCChargeMargin, state:LNGEng3CoversDeficit, state:LNGEng3DG1LowSoCChargeMargin, state:AllThermalWithinCapacity, state:OverloadBatteryLack, ... +18`。

#### SL-9 per-request 决策

- accepted_request_ids：`<derived-from-table>`；candidate_len=`8708`。

| request_id | decision | waiver | rework_locked | rationale / intent |
|---|---|---:|---:|---|
| `fixreq-0-sl7-0-be1e03bda7` | `accept` | ❌ | ✅ | Accepted because the SL-7 unsafe_recovery finding is valid: the original OverloadBatteryLack branch was reachable for any demand above RES plus thermal capacity and computed battery discharge without SoC or batt_Pmax suitability. The rework evidence also shows the prior candidate regressed the scenario overload_activates_all_thermal_and_battery_lack only by ...<truncated 685 chars> |
- repair_rationale：Primary failing scenario addressed: overload_activates_all_thermal_and_battery_lack, step overload_battery_lack_above_total_capacity. Expected state LNGShipEMS.OverloadBatteryLack matched the prior actual state, and expected Pgen_req = 160....<truncated 287 chars>；The SL-7 unsafe_recovery target is still repaired by making the OverloadBatteryLack guard require SoC >= 0.2 and the residual lack after LNG, eng3, DG1, and DG2 to be <= batt_Pmax. Thus the overload battery discharge action remains NL-groun...<truncated 86 chars>；This is not the previously rejected candidate hash in substance: the previous candidate changed both the overload guard and the overload load commands, causing the local scenario regression. This candidate keeps the guard-safety repair but ...<truncated 45 chars>；Missing-required-grounding objection mapping: guard:RESCoversCharge is concretely represented by the forced transition to RESCoversCharge with guard PL > 0 && Ppv + Pw >= PL && SoC < 0.95, and its state action charges residual RES.；Missing-required-grounding objection mapping: guard:RESCoversSpare is concretely represented by the forced transition to RESCoversSpare with guard PL > 0 && Ppv + Pw >= PL && SoC >= 0.95, and its state action sends residual RES to Pspare.
- diff_summary：`{"summary": "Changed only the OverloadBatteryLack forced-transition guard from the original DSL by adding SoC >= 0.2 and residual lack <= batt_Pmax. Preserved all twelve states, all variables, RESCoversCharge/RESCoversSpare guards, and the OverloadBatteryLack dispatch actions including all thermal cut-in, battery residual discharge, and load cut-in/load cut-out commands."}`。

#### SL-9 candidate / 最终修改执行方案

```pyfcstm
def float PL = 0.0;
def float Ppv = 0.0;
def float Pw = 0.0;
def float SoC = 0.5;
def float batt_Pmax = 0.0;
def float LNG_Pmax = 0.0;
def float eng3_Pmax = 0.0;
def float DG1_Pmax = 0.0;
def float DG2_Pmax = 0.0;
def float Pgmax = 0.0;
def float Pd1max = 0.0;
def float Pgen_req = 0.0;
def float Pbatt_discharge = 0.0;
def float Pbatt_charge = 0.0;
def float Pspare = 0.0;
def int cmd_LNG_cut_in = 0;
def int cmd_LNG_cut_out = 1;
def int cmd_eng3_cut_in = 0;
def int cmd_eng3_cut_out = 1;
def int cmd_DG1_cut_in = 0;
def int cmd_DG1_cut_out = 1;
def int cmd_DG2_cut_in = 0;
def int cmd_DG2_cut_out = 1;
def int cmd_load_cut_in = 1;
def int cmd_load_cut_out = 0;

state LNGShipEMS {
    ! * -> ZeroLoadCharge : if [PL == 0 && Ppv + Pw > 0 && SoC < 0.95];
    ! * -> ZeroLoadSpare : if [PL == 0 && SoC >= 0.95];
    ! * -> RESCoversCharge : if [PL > 0 && Ppv + Pw >= PL && SoC < 0.95];
    ! * -> RESCoversSpare : if [PL > 0 && Ppv + Pw >= PL && SoC >= 0.95];
    ! * -> RESBatteryDischarge : if [PL > 0 && Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw <= batt_Pmax];
    ! * -> LNGLowSoCChargeMargin : if [PL > 0 && Ppv + Pw < PL && SoC < 0.2 && PL - Ppv - Pw + Pgmax / 5 <= LNG_Pmax];
    ! * -> LNGCoversDeficit : if [PL > 0 && Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw > batt_Pmax && PL - Ppv - Pw <= LNG_Pmax];
    ! * -> LNGEng3LowSoCChargeMargin : if [PL > 0 && Ppv + Pw < PL && SoC < 0.2 && PL - Ppv - Pw + Pgmax / 5 > LNG_Pmax && PL - Ppv - Pw + Pd1max / 10 <= LNG_Pmax + eng3_Pmax];
    ! * -> LNGEng3CoversDeficit : if [PL > 0 && Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw > LNG_Pmax && PL - Ppv - Pw <= LNG_Pmax + eng3_Pmax];
    ! * -> LNGEng3DG1LowSoCChargeMargin : if [PL > 0 && Ppv + Pw < PL && SoC < 0.2 && PL - Ppv - Pw + Pd1max / 10 > LNG_Pmax + eng3_Pmax && PL - Ppv - Pw + Pd1max / 10 <= LNG_Pmax + eng3_Pmax + DG1_Pmax];
    ! * -> AllThermalWithinCapacity : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > LNG_Pmax + eng3_Pmax && PL - Ppv - Pw <= LNG_Pmax + eng3_Pmax + DG1_Pmax + DG2_Pmax];
    ! * -> OverloadBatteryLack : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > LNG_Pmax + eng3_Pmax + DG1_Pmax + DG2_Pmax && SoC >= 0.2 && PL - Ppv - Pw - LNG_Pmax - eng3_Pmax - DG1_Pmax - DG2_Pmax <= batt_Pmax];

    [*] -> ZeroLoadCharge;

    state ZeroLoadCharge {
        during {
            Pgen_req = 0.0;
            Pbatt_discharge = 0.0;
            Pbatt_charge = Ppv + Pw;
            Pspare = 0.0;
            cmd_LNG_cut_in = 0;
            cmd_LNG_cut_out = 1;
            cmd_eng3_cut_in = 0;
            cmd_eng3_cut_out = 1;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 0;
            cmd_load_cut_out = 1;
        }
    }

    state ZeroLoadSpare {
        during {
            Pgen_req = 0.0;
            Pbatt_discharge = 0.0;
            Pbatt_charge = 0.0;
            Pspare = Ppv + Pw;
            cmd_LNG_cut_in = 0;
            cmd_LNG_cut_out = 1;
            cmd_eng3_cut_in = 0;
            cmd_eng3_cut_out = 1;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 0;
            cmd_load_cut_out = 1;
        }
    }

    state RESCoversCharge {
        during {
            Pgen_req = 0.0;
            Pbatt_discharge = 0.0;
            Pbatt_charge = Ppv + Pw - PL;
            Pspare = 0.0;
            cmd_LNG_cut_in = 0;
            cmd_LNG_cut_out = 1;
            cmd_eng3_cut_in = 0;
            cmd_eng3_cut_out = 1;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state RESCoversSpare {
        during {
            Pgen_req = 0.0;
            Pbatt_discharge = 0.0;
            Pbatt_charge = 0.0;
            Pspare = Ppv + Pw - PL;
            cmd_LNG_cut_in = 0;
            cmd_LNG_cut_out = 1;
            cmd_eng3_cut_in = 0;
            cmd_eng3_cut_out = 1;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state RESBatteryDischarge {
        during {
            Pgen_req = 0.0;
            Pbatt_discharge = PL - Ppv - Pw;
            Pbatt_charge = 0.0;
            Pspare = 0.0;
            cmd_LNG_cut_in = 0;
            cmd_LNG_cut_out = 1;
            cmd_eng3_cut_in = 0;
            cmd_eng3_cut_out = 1;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state LNGLowSoCChargeMargin {
        during {
            Pgen_req = PL - Ppv - Pw + Pgmax / 5;
            Pbatt_discharge = 0.0;
            Pbatt_charge = Pgmax / 5;
            Pspare = 0.0;
            cmd_LNG_cut_in = 1;
            cmd_LNG_cut_out = 0;
            cmd_eng3_cut_in = 0;
            cmd_eng3_cut_out = 1;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state LNGCoversDeficit {
        during {
            Pgen_req = PL - Ppv - Pw;
            Pbatt_discharge = 0.0;
            Pbatt_charge = 0.0;
            Pspare = 0.0;
            cmd_LNG_cut_in = 1;
            cmd_LNG_cut_out = 0;
            cmd_eng3_cut_in = 0;
            cmd_eng3_cut_out = 1;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state LNGEng3LowSoCChargeMargin {
        during {
            Pgen_req = PL - Ppv - Pw + Pd1max / 10;
            Pbatt_discharge = 0.0;
            Pbatt_charge = Pd1max / 10;
            Pspare = 0.0;
            cmd_LNG_cut_in = 1;
            cmd_LNG_cut_out = 0;
            cmd_eng3_cut_in = 1;
            cmd_eng3_cut_out = 0;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state LNGEng3CoversDeficit {
        during {
            Pgen_req = PL - Ppv - Pw;
            Pbatt_discharge = 0.0;
            Pbatt_charge = 0.0;
            Pspare = 0.0;
            cmd_LNG_cut_in = 1;
            cmd_LNG_cut_out = 0;
            cmd_eng3_cut_in = 1;
            cmd_eng3_cut_out = 0;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state LNGEng3DG1LowSoCChargeMargin {
        during {
            Pgen_req = PL - Ppv - Pw + Pd1max / 10;
            Pbatt_discharge = 0.0;
            Pbatt_charge = Pd1max / 10;
            Pspare = 0.0;
            cmd_LNG_cut_in = 1;
            cmd_LNG_cut_out = 0;
            cmd_eng3_cut_in = 1;
            cmd_eng3_cut_out = 0;
            cmd_DG1_cut_in = 1;
            cmd_DG1_cut_out = 0;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state AllThermalWithinCapacity {
        during {
            Pgen_req = PL - Ppv - Pw;
            Pbatt_discharge = 0.0;
            Pbatt_charge = 0.0;
            Pspare = 0.0;
            cmd_LNG_cut_in = 1;
            cmd_LNG_cut_out = 0;
            cmd_eng3_cut_in = 1;
            cmd_eng3_cut_out = 0;
            cmd_DG1_cut_in = 1;
            cmd_DG1_cut_out = 0;
            cmd_DG2_cut_in = 1;
            cmd_DG2_cut_out = 0;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state OverloadBatteryLack {
        during {
            Pgen_req = LNG_Pmax + eng3_Pmax + DG1_Pmax + DG2_Pmax;
            Pbatt_discharge = PL - Ppv - Pw - LNG_Pmax - eng3_Pmax - DG1_Pmax - DG2_Pmax;
            Pbatt_charge = 0.0;
            Pspare = 0.0;
            cmd_LNG_cut_in = 1;
            cmd_LNG_cut_out = 0;
            cmd_eng3_cut_in = 1;
            cmd_eng3_cut_out = 0;
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
@@ -36,7 +36,7 @@
     ! * -> LNGEng3CoversDeficit : if [PL > 0 && Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw > LNG_Pmax && PL - Ppv - Pw <= LNG_Pmax + eng3_Pmax];
     ! * -> LNGEng3DG1LowSoCChargeMargin : if [PL > 0 && Ppv + Pw < PL && SoC < 0.2 && PL - Ppv - Pw + Pd1max / 10 > LNG_Pmax + eng3_Pmax && PL - Ppv - Pw + Pd1max / 10 <= LNG_Pmax + eng3_Pmax + DG1_Pmax];
     ! * -> AllThermalWithinCapacity : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > LNG_Pmax + eng3_Pmax && PL - Ppv - Pw <= LNG_Pmax + eng3_Pmax + DG1_Pmax + DG2_Pmax];
-    ! * -> OverloadBatteryLack : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > LNG_Pmax + eng3_Pmax + DG1_Pmax + DG2_Pmax];
+    ! * -> OverloadBatteryLack : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > LNG_Pmax + eng3_Pmax + DG1_Pmax + DG2_Pmax && SoC >= 0.2 && PL - Ppv - Pw - LNG_Pmax - eng3_Pmax - DG1_Pmax - DG2_Pmax <= batt_Pmax];
 
     [*] -> ZeroLoadCharge;
 
```

#### SL-10 审查结果

- SL-10 decision=`rework`，ok=`False`，target_resolved=`True`，regression_detected=`False`，drift_risk=`minor`。
- SL-10 review_meta：schema=`SL10RepairReviewOutput.v1`，failure_policy=`fail_closed`，replay_key=`SL-10:sha256:bc21e8b6c32ebc0e27688150ebbf9977733df920e5e7dc24be46e32c10cb04a8`。
  - SL-10 evidence 1: `{"summary": "The hard SL-7 request identified unsafe_recovery in the original OverloadBatteryLack branch: it entered whenever demand exceeded RES plus thermal capacity and computed battery discharge without SoC or batt_Pmax suitability. The current candidate makes a narrow DSL edit to the OverloadBatteryLack forced-transition guard by adding `SoC >= 0.2` and residual lack `PL - Ppv - Pw - LNG_Pmax - eng3_Pmax - DG1_Pmax - DG2_Pmax <= batt_Pmax`. This directly addresses the unbounded and suitability-unguarded battery discharge part of the hard finding while preserving the NL-required overload dispatch action."}`
  - SL-10 evidence 2: `{"summary": "The candidate preserves the NL-required overload behavior: when extreme demand exceeds RES plus all thermal resources, it activates LNG, eng3, DG1, and DG2, sets `Pgen_req` to total thermal capacity, and covers the remaining lack by `Pbatt_discharge`. It also preserves the local scenario obligation restored by SL-9 rework: `cmd_load_cut_in = 1` and `cmd_load_cut_out = 0` in OverloadBatteryLack. This resolves the previous scenario regression in `overload_activates_all_thermal_and_battery_lack`, where the only mismatch was the prior candidate's load cut-out commands."}`
  - SL-10 evidence 3: `{"summary": "The diff summary and DSL show no deletion of required states, inputs, outputs, commands, or normal dispatch branches. All twelve states remain; required inputs `PL`, `Ppv`, `Pw`, `SoC`, `eng3_Pmax`, `Pgmax`, and `Pd1max` remain; required outputs `Pgen_req`, `Pbatt_discharge`, `Pbatt_charge`, and `Pspare` remain; and generator cut-in commands remain. The RESCoversCharge and RESCoversSpare guards are unchanged from the original DSL."}`
  - SL-10 evidence 4: `{"summary": "The complete FixLog and repair_memory show the prior candidate hash `sha256:c442...` was rejected because it caused a local scenario regression by changing OverloadBatteryLack load commands to cut-out. The current candidate has a different hash `sha256:a3d167...`, keeps the guard-safety repair, restores the scenario-required load commands, and includes SL-9 notes explicitly mapping the local missing-grounding objections to concrete forced-transition guards."}`
- SL-10 rework_instructions：SL-10 pass was downgraded because local deterministic evidence reported major drift and SL-10 evidence did not explicitly address the local rejection reason/kind with a structured local_override_rationale.；For the next SL-9 repair, do not blindly regenerate the same DSL. Either change the candidate so the local major-drift evidence is resolved, or keep the minimal DSL only with explicit repair_rationale mapping each local objection (for example missing_required_grounding, scenario_regression, count_drift, or forced_transition_count_drift) to concrete NL-ground...<truncated 152 chars>
- local checks evidence：stage=`SD-10`；note=PR-E1 uses local parse/semantic/design/sim checks as SL-10 evidence, not as the final deterministic judge.。
  - local ok=`False`，target_resolved=`False`，regression_detected=`False`，drift_risk=`major`。
  - local_rejection：reason=`missing_required_grounding`，rejected_by_stage=`SD-10`。
    - local evidence 1: `missing_required_grounding` {"element_ids": ["guard:RESCoversCharge", "guard:RESCoversSpare", "guard:OverloadBatteryLack"], "kind": "missing_required_grounding"}

</details>

<details><summary>Repair 3 / iteration `0` / source `SL-7` / accepted=❌</summary>

#### 为什么进入修复

- selected feedback source：`SL-7`；blocking=`True`；pre_scenario=`False`。
- problem_summary：model review failed
- diagnostic ids：`0`。
- before_dsl_hash：`sha256:01c5a57aa10618b447f8a2a830a9d8e06062db2bafb5fe2ac26d66485929c533`；candidate_dsl_hash：`sha256:fa9a662af2c91e5cca5f3f32570c28a50c1745f2db60dc535a9ee953a9402ac3`。

#### 错误证据 / diagnostics

- 1. `<unknown>` `` policy=``：The illegal overload state is treated as an ordinary reachable recovery/dispatch state and can command continued load service plus battery discharge without suitability or capacity guards.

#### SD-8 FixRequestBatch / 修改请求

- batch_id：`fixbatch-0-sha256-081cf0a961f`；source_stage=`SL-7`；legacy_plan_kind=`FixPlan`；requests=`1`。

| request_id | severity | hard | waiver | problem | evidence |
|---|---|---:|---:|---|---|
| `fixreq-0-sl7-0-be1e03bda7` | `review_fail` | ✅ | ❌ | model review failed | `{'category': 'unsafe_recovery', 'evidence': ['NL: "The overload completion state is illegal... the state shall never occur in practice."', 'DSL forced transition reaches `OverloadBatteryLack` whenever demand exceeds all RES and thermal resources.', '`OverloadBatteryLack` sets `cmd_load_cut_in = 1`, `cmd_load_cut_out = 0`, and computes `Pbatt_discharge` from the remaining lack without checking `SoC` or `batt_Pmax`.', 'sim_summary includes a passing overload scenario, showing this branch is accepted as normal behavior rather than flagged as illegal.'], 'severity': 'major', 'summary': 'The illegal overload state is treated as an ordinary reachable recovery/dispatch state and can command continued load service plus battery discharge without suitability or capacity guards.'}` |

#### SD-8 legacy fix plan / 修改建议

- recommended_strategy：Use diagnostics as hints; choose the smallest globally consistent repair.；Before returning a candidate, verify every required_preserve_element_id still has a concrete DSL representation.
- forbidden_edits：`Do not delete grounded required elements merely to silence diagnostics., Do not invent internal plant/environment dynamics merely to make external input variables appear written.`。
- required_preserve_element_ids：`state:ZeroLoadCharge, state:ZeroLoadSpare, state:RESCoversCharge, state:RESCoversSpare, state:RESBatteryDischarge, state:LNGLowSoCChargeMargin, state:LNGCoversDeficit, state:LNGEng3LowSoCChargeMargin, state:LNGEng3CoversDeficit, state:LNGEng3DG1LowSoCChargeMargin, state:AllThermalWithinCapacity, state:OverloadBatteryLack, ... +18`。

#### SL-9 per-request 决策

- accepted_request_ids：`<derived-from-table>`；candidate_len=`9110`。

| request_id | decision | waiver | rework_locked | rationale / intent |
|---|---|---:|---:|---|
| `fixreq-0-sl7-0-be1e03bda7` | `accept` | ❌ | ✅ | Accepted. The request is rework-locked and the SL-7 unsafe_recovery finding is valid: the original OverloadBatteryLack transition allowed any residual demand above total thermal capacity to enter a branch that computed battery discharge without SoC or batt_Pmax suitability. This repair keeps the scenario-required and NL-grounded overload dispatch actions, in...<truncated 1112 chars> |
- repair_rationale：Primary SL-7 unsafe_recovery gap: original OverloadBatteryLack entered whenever PL - Ppv - Pw exceeded LNG_Pmax + eng3_Pmax + DG1_Pmax + DG2_Pmax and then computed Pbatt_discharge without checking SoC or batt_Pmax. The repaired forced guard...<truncated 97 chars>；Scenario regression brief: in overload_activates_all_thermal_and_battery_lack, step overload_battery_lack_above_total_capacity, the expected and actual state were both LNGShipEMS.OverloadBatteryLack; Pgen_req = 160.0, Pbatt_discharge = 40.0...<truncated 281 chars>；Missing grounding mapping: guard:RESCoversCharge is represented twice concretely: the wildcard forced transition to RESCoversCharge with guard PL > 0 && Ppv + Pw >= PL && SoC < 0.95, and the added local guarded self-transition with the same...<truncated 99 chars>；Missing grounding mapping: guard:RESCoversSpare is represented twice concretely: the wildcard forced transition to RESCoversSpare with guard PL > 0 && Ppv + Pw >= PL && SoC >= 0.95, and the added local guarded self-transition with the same ...<truncated 85 chars>；Missing grounding mapping: guard:OverloadBatteryLack is represented twice concretely: the wildcard forced transition to OverloadBatteryLack and the added local guarded self-transition, both requiring demand above RES plus all thermal capaci...<truncated 225 chars>
- diff_summary：`{"summary": "Changed the OverloadBatteryLack forced-transition guard by adding SoC >= 0.2 and residual battery-lack <= batt_Pmax. Preserved all twelve states, variables, dispatch outputs, generator/load commands, and overload actions. Added three explicit guarded self-transitions for RESCoversCharge, RESCoversSpare, and OverloadBatteryLack to resolve missing guard grounding without changing dispatch behavior."}`。

#### SL-9 candidate / 最终修改执行方案

```pyfcstm
def float PL = 0.0;
def float Ppv = 0.0;
def float Pw = 0.0;
def float SoC = 0.5;
def float batt_Pmax = 0.0;
def float LNG_Pmax = 0.0;
def float eng3_Pmax = 0.0;
def float DG1_Pmax = 0.0;
def float DG2_Pmax = 0.0;
def float Pgmax = 0.0;
def float Pd1max = 0.0;
def float Pgen_req = 0.0;
def float Pbatt_discharge = 0.0;
def float Pbatt_charge = 0.0;
def float Pspare = 0.0;
def int cmd_LNG_cut_in = 0;
def int cmd_LNG_cut_out = 1;
def int cmd_eng3_cut_in = 0;
def int cmd_eng3_cut_out = 1;
def int cmd_DG1_cut_in = 0;
def int cmd_DG1_cut_out = 1;
def int cmd_DG2_cut_in = 0;
def int cmd_DG2_cut_out = 1;
def int cmd_load_cut_in = 1;
def int cmd_load_cut_out = 0;

state LNGShipEMS {
    ! * -> ZeroLoadCharge : if [PL == 0 && Ppv + Pw > 0 && SoC < 0.95];
    ! * -> ZeroLoadSpare : if [PL == 0 && SoC >= 0.95];
    ! * -> RESCoversCharge : if [PL > 0 && Ppv + Pw >= PL && SoC < 0.95];
    ! * -> RESCoversSpare : if [PL > 0 && Ppv + Pw >= PL && SoC >= 0.95];
    ! * -> RESBatteryDischarge : if [PL > 0 && Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw <= batt_Pmax];
    ! * -> LNGLowSoCChargeMargin : if [PL > 0 && Ppv + Pw < PL && SoC < 0.2 && PL - Ppv - Pw + Pgmax / 5 <= LNG_Pmax];
    ! * -> LNGCoversDeficit : if [PL > 0 && Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw > batt_Pmax && PL - Ppv - Pw <= LNG_Pmax];
    ! * -> LNGEng3LowSoCChargeMargin : if [PL > 0 && Ppv + Pw < PL && SoC < 0.2 && PL - Ppv - Pw + Pgmax / 5 > LNG_Pmax && PL - Ppv - Pw + Pd1max / 10 <= LNG_Pmax + eng3_Pmax];
    ! * -> LNGEng3CoversDeficit : if [PL > 0 && Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw > LNG_Pmax && PL - Ppv - Pw <= LNG_Pmax + eng3_Pmax];
    ! * -> LNGEng3DG1LowSoCChargeMargin : if [PL > 0 && Ppv + Pw < PL && SoC < 0.2 && PL - Ppv - Pw + Pd1max / 10 > LNG_Pmax + eng3_Pmax && PL - Ppv - Pw + Pd1max / 10 <= LNG_Pmax + eng3_Pmax + DG1_Pmax];
    ! * -> AllThermalWithinCapacity : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > LNG_Pmax + eng3_Pmax && PL - Ppv - Pw <= LNG_Pmax + eng3_Pmax + DG1_Pmax + DG2_Pmax];
    ! * -> OverloadBatteryLack : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > LNG_Pmax + eng3_Pmax + DG1_Pmax + DG2_Pmax && SoC >= 0.2 && PL - Ppv - Pw - LNG_Pmax - eng3_Pmax - DG1_Pmax - DG2_Pmax <= batt_Pmax];

    [*] -> ZeroLoadCharge;

    state ZeroLoadCharge {
        during {
            Pgen_req = 0.0;
            Pbatt_discharge = 0.0;
            Pbatt_charge = Ppv + Pw;
            Pspare = 0.0;
            cmd_LNG_cut_in = 0;
            cmd_LNG_cut_out = 1;
            cmd_eng3_cut_in = 0;
            cmd_eng3_cut_out = 1;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 0;
            cmd_load_cut_out = 1;
        }
    }

    state ZeroLoadSpare {
        during {
            Pgen_req = 0.0;
            Pbatt_discharge = 0.0;
            Pbatt_charge = 0.0;
            Pspare = Ppv + Pw;
            cmd_LNG_cut_in = 0;
            cmd_LNG_cut_out = 1;
            cmd_eng3_cut_in = 0;
            cmd_eng3_cut_out = 1;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 0;
            cmd_load_cut_out = 1;
        }
    }

    state RESCoversCharge {
        during {
            Pgen_req = 0.0;
            Pbatt_discharge = 0.0;
            Pbatt_charge = Ppv + Pw - PL;
            Pspare = 0.0;
            cmd_LNG_cut_in = 0;
            cmd_LNG_cut_out = 1;
            cmd_eng3_cut_in = 0;
            cmd_eng3_cut_out = 1;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state RESCoversSpare {
        during {
            Pgen_req = 0.0;
            Pbatt_discharge = 0.0;
            Pbatt_charge = 0.0;
            Pspare = Ppv + Pw - PL;
            cmd_LNG_cut_in = 0;
            cmd_LNG_cut_out = 1;
            cmd_eng3_cut_in = 0;
            cmd_eng3_cut_out = 1;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state RESBatteryDischarge {
        during {
            Pgen_req = 0.0;
            Pbatt_discharge = PL - Ppv - Pw;
            Pbatt_charge = 0.0;
            Pspare = 0.0;
            cmd_LNG_cut_in = 0;
            cmd_LNG_cut_out = 1;
            cmd_eng3_cut_in = 0;
            cmd_eng3_cut_out = 1;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state LNGLowSoCChargeMargin {
        during {
            Pgen_req = PL - Ppv - Pw + Pgmax / 5;
            Pbatt_discharge = 0.0;
            Pbatt_charge = Pgmax / 5;
            Pspare = 0.0;
            cmd_LNG_cut_in = 1;
            cmd_LNG_cut_out = 0;
            cmd_eng3_cut_in = 0;
            cmd_eng3_cut_out = 1;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state LNGCoversDeficit {
        during {
            Pgen_req = PL - Ppv - Pw;
            Pbatt_discharge = 0.0;
            Pbatt_charge = 0.0;
            Pspare = 0.0;
            cmd_LNG_cut_in = 1;
            cmd_LNG_cut_out = 0;
            cmd_eng3_cut_in = 0;
            cmd_eng3_cut_out = 1;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state LNGEng3LowSoCChargeMargin {
        during {
            Pgen_req = PL - Ppv - Pw + Pd1max / 10;
            Pbatt_discharge = 0.0;
            Pbatt_charge = Pd1max / 10;
            Pspare = 0.0;
            cmd_LNG_cut_in = 1;
            cmd_LNG_cut_out = 0;
            cmd_eng3_cut_in = 1;
            cmd_eng3_cut_out = 0;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state LNGEng3CoversDeficit {
        during {
            Pgen_req = PL - Ppv - Pw;
            Pbatt_discharge = 0.0;
            Pbatt_charge = 0.0;
            Pspare = 0.0;
            cmd_LNG_cut_in = 1;
            cmd_LNG_cut_out = 0;
            cmd_eng3_cut_in = 1;
            cmd_eng3_cut_out = 0;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state LNGEng3DG1LowSoCChargeMargin {
        during {
            Pgen_req = PL - Ppv - Pw + Pd1max / 10;
            Pbatt_discharge = 0.0;
            Pbatt_charge = Pd1max / 10;
            Pspare = 0.0;
            cmd_LNG_cut_in = 1;
            cmd_LNG_cut_out = 0;
            cmd_eng3_cut_in = 1;
            cmd_eng3_cut_out = 0;
            cmd_DG1_cut_in = 1;
            cmd_DG1_cut_out = 0;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state AllThermalWithinCapacity {
        during {
            Pgen_req = PL - Ppv - Pw;
            Pbatt_discharge = 0.0;
            Pbatt_charge = 0.0;
            Pspare = 0.0;
            cmd_LNG_cut_in = 1;
            cmd_LNG_cut_out = 0;
            cmd_eng3_cut_in = 1;
            cmd_eng3_cut_out = 0;
            cmd_DG1_cut_in = 1;
            cmd_DG1_cut_out = 0;
            cmd_DG2_cut_in = 1;
            cmd_DG2_cut_out = 0;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state OverloadBatteryLack {
        during {
            Pgen_req = LNG_Pmax + eng3_Pmax + DG1_Pmax + DG2_Pmax;
            Pbatt_discharge = PL - Ppv - Pw - LNG_Pmax - eng3_Pmax - DG1_Pmax - DG2_Pmax;
            Pbatt_charge = 0.0;
            Pspare = 0.0;
            cmd_LNG_cut_in = 1;
            cmd_LNG_cut_out = 0;
            cmd_eng3_cut_in = 1;
            cmd_eng3_cut_out = 0;
            cmd_DG1_cut_in = 1;
            cmd_DG1_cut_out = 0;
            cmd_DG2_cut_in = 1;
            cmd_DG2_cut_out = 0;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    RESCoversCharge -> RESCoversCharge : if [PL > 0 && Ppv + Pw >= PL && SoC < 0.95];
    RESCoversSpare -> RESCoversSpare : if [PL > 0 && Ppv + Pw >= PL && SoC >= 0.95];
    OverloadBatteryLack -> OverloadBatteryLack : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > LNG_Pmax + eng3_Pmax + DG
... <truncated 110 chars; see run record>
```

#### Candidate diff（before -> candidate）

```diff
--- before.fcstm
+++ candidate.fcstm
@@ -36,7 +36,7 @@
     ! * -> LNGEng3CoversDeficit : if [PL > 0 && Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw > LNG_Pmax && PL - Ppv - Pw <= LNG_Pmax + eng3_Pmax];
     ! * -> LNGEng3DG1LowSoCChargeMargin : if [PL > 0 && Ppv + Pw < PL && SoC < 0.2 && PL - Ppv - Pw + Pd1max / 10 > LNG_Pmax + eng3_Pmax && PL - Ppv - Pw + Pd1max / 10 <= LNG_Pmax + eng3_Pmax + DG1_Pmax];
     ! * -> AllThermalWithinCapacity : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > LNG_Pmax + eng3_Pmax && PL - Ppv - Pw <= LNG_Pmax + eng3_Pmax + DG1_Pmax + DG2_Pmax];
-    ! * -> OverloadBatteryLack : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > LNG_Pmax + eng3_Pmax + DG1_Pmax + DG2_Pmax];
+    ! * -> OverloadBatteryLack : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > LNG_Pmax + eng3_Pmax + DG1_Pmax + DG2_Pmax && SoC >= 0.2 && PL - Ppv - Pw - LNG_Pmax - eng3_Pmax - DG1_Pmax - DG2_Pmax <= batt_Pmax];
 
     [*] -> ZeroLoadCharge;
 
@@ -267,4 +267,8 @@
             cmd_load_cut_out = 0;
         }
     }
+
+    RESCoversCharge -> RESCoversCharge : if [PL > 0 && Ppv + Pw >= PL && SoC < 0.95];
+    RESCoversSpare -> RESCoversSpare : if [PL > 0 && Ppv + Pw >= PL && SoC >= 0.95];
+    OverloadBatteryLack -> OverloadBatteryLack : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > LNG_Pmax + eng3_Pmax + DG1_Pmax + DG2_Pmax && SoC >= 0.2 && PL - Ppv - Pw - LNG_Pmax - eng3_Pmax - DG1_Pmax - DG2_Pmax <= batt_Pmax];
 }
```

#### SL-10 审查结果

- SL-10 decision=`rework`，ok=`False`，target_resolved=`True`，regression_detected=`False`，drift_risk=`minor`。
- SL-10 review_meta：schema=`SL10RepairReviewOutput.v1`，failure_policy=`fail_closed`，replay_key=`SL-10:sha256:0fcca63113b67c6c2bad702856ec9a55fec401734bb08a99d562e25164a934c9`。
  - SL-10 evidence 1: `{"summary": "The hard SL-7 unsafe_recovery finding is substantively repaired. In the old DSL, OverloadBatteryLack was entered whenever demand exceeded RES plus total thermal capacity and then computed Pbatt_discharge without checking battery suitability or discharge capacity. The candidate preserves the NL-required overload dispatch action but strengthens the OverloadBatteryLack forced-transition guard with SoC >= 0.2 and residual lack <= batt_Pmax, so the branch no longer permits unbounded or low-SoC battery discharge."}`
  - SL-10 evidence 2: `{"summary": "The candidate preserves the NL-required overload behavior: when extreme demand exceeds RES plus all thermal resources and the residual lack is battery-coverable, it activates LNG, eng3, DG1, and DG2, sets Pgen_req to total thermal capacity, sets Pbatt_discharge to the remaining lack, and leaves cmd_load_cut_in = 1 / cmd_load_cut_out = 0. This resolves the prior scenario regression in overload_activates_all_thermal_and_battery_lack, where the earlier rejected candidate had changed only the load commands to cut-out."}`
  - SL-10 evidence 3: `{"summary": "The diff does not drop NL-required states, inputs, outputs, dispatch branches, or command variables. All twelve states remain, including ZeroLoadCharge, ZeroLoadSpare, RESCoversCharge, RESCoversSpare, RESBatteryDischarge, LNG and diesel priority states, AllThermalWithinCapacity, and OverloadBatteryLack. Required variables PL, Ppv, Pw, SoC, eng3_Pmax, Pgmax, Pd1max, Pgen_req, Pbatt_discharge, Pbatt_charge, Pspare, and generator/load command flags remain present."}`
  - SL-10 evidence 4: `{"summary": "The RES coverage obligations remain represented: RESCoversCharge is selected under PL > 0 && Ppv + Pw >= PL && SoC < 0.95 and charges residual renewable power; RESCoversSpare is selected under PL > 0 && Ppv + Pw >= PL && SoC >= 0.95 and sends residual renewable power to Pspare. These match the NL requirements for renewable coverage below and at/above the 0.95 SoC threshold."}`
  - SL-10 evidence 5: `{"summary": "The complete FixLog and repair_memory were considered. The first rejected candidate hash c442... caused a scenario regression by changing overload load commands to cut-out. The later candidate a3d... restored the scenario-required commands but local evidence still reported missing guard grounding. The current candidate has a new hash fa9a..., keeps the safety guard repair, preserves the restored load commands, and attempts to make the three required guard elements explicit with same-guard self-transitions while retaining the existing wildcard forced classification transitions."}`
- SL-10 rework_instructions：SL-10 pass was downgraded because local deterministic evidence reported major drift and SL-10 evidence did not explicitly address the local rejection reason/kind with a structured local_override_rationale.；For the next SL-9 repair, do not blindly regenerate the same DSL. Either change the candidate so the local major-drift evidence is resolved, or keep the minimal DSL only with explicit repair_rationale mapping each local objection (for example missing_required_grounding, scenario_regression, count_drift, or forced_transition_count_drift) to concrete NL-ground...<truncated 152 chars>
- local checks evidence：stage=`SD-10`；note=PR-E1 uses local parse/semantic/design/sim checks as SL-10 evidence, not as the final deterministic judge.。
  - local ok=`False`，target_resolved=`False`，regression_detected=`False`，drift_risk=`major`。
  - local_rejection：reason=`new_blocking_design_diagnostic; missing_required_grounding`，rejected_by_stage=`SD-10`。
    - local evidence 1: `new_blocking_design_diagnostic` {"items": [{"budget_exhausted": false, "budget_remaining": 2, "code": "W_FORCED_OVERRIDES_NORMAL", "instance_key": "W_FORCED_OVERRIDES_NORMAL:from_path=LNGShipEMS.RESCoversCharge:to_path=LNGShipEMS.RESCoversCharge", "message": "Forced transition 'LNGShipEMS.RESCoversCharge' -> 'LNGShipEMS.RESCoversCharge' duplicates a normal transition.", "policy_action": "requires_policy_classification", "pyfcstm_severity": "warning", "rationale": "", "refs": {"forced_span": null, "from_path": "LNGShipEMS.RESCo...<truncated 3105 chars>
    - local evidence 2: `missing_required_grounding` {"element_ids": ["guard:RESCoversCharge", "guard:RESCoversSpare", "guard:OverloadBatteryLack"], "kind": "missing_required_grounding"}

</details>

<details><summary>Repair 4 / iteration `0` / source `SL-7` / accepted=❌</summary>

#### 为什么进入修复

- selected feedback source：`SL-7`；blocking=`True`；pre_scenario=`False`。
- problem_summary：model review failed
- diagnostic ids：`0`。
- before_dsl_hash：`sha256:01c5a57aa10618b447f8a2a830a9d8e06062db2bafb5fe2ac26d66485929c533`；candidate_dsl_hash：`sha256:a3d167d8c7d32fd212b403f7d77af2d6db6d5c6d03fe6f1bbf42cc671ee351be`。

#### 错误证据 / diagnostics

- 1. `<unknown>` `` policy=``：The illegal overload state is treated as an ordinary reachable recovery/dispatch state and can command continued load service plus battery discharge without suitability or capacity guards.

#### SD-8 FixRequestBatch / 修改请求

- batch_id：`fixbatch-0-sha256-081cf0a961f`；source_stage=`SL-7`；legacy_plan_kind=`FixPlan`；requests=`1`。

| request_id | severity | hard | waiver | problem | evidence |
|---|---|---:|---:|---|---|
| `fixreq-0-sl7-0-be1e03bda7` | `review_fail` | ✅ | ❌ | model review failed | `{'category': 'unsafe_recovery', 'evidence': ['NL: "The overload completion state is illegal... the state shall never occur in practice."', 'DSL forced transition reaches `OverloadBatteryLack` whenever demand exceeds all RES and thermal resources.', '`OverloadBatteryLack` sets `cmd_load_cut_in = 1`, `cmd_load_cut_out = 0`, and computes `Pbatt_discharge` from the remaining lack without checking `SoC` or `batt_Pmax`.', 'sim_summary includes a passing overload scenario, showing this branch is accepted as normal behavior rather than flagged as illegal.'], 'severity': 'major', 'summary': 'The illegal overload state is treated as an ordinary reachable recovery/dispatch state and can command continued load service plus battery discharge without suitability or capacity guards.'}` |

#### SD-8 legacy fix plan / 修改建议

- recommended_strategy：Use diagnostics as hints; choose the smallest globally consistent repair.；Before returning a candidate, verify every required_preserve_element_id still has a concrete DSL representation.
- forbidden_edits：`Do not delete grounded required elements merely to silence diagnostics., Do not invent internal plant/environment dynamics merely to make external input variables appear written.`。
- required_preserve_element_ids：`state:ZeroLoadCharge, state:ZeroLoadSpare, state:RESCoversCharge, state:RESCoversSpare, state:RESBatteryDischarge, state:LNGLowSoCChargeMargin, state:LNGCoversDeficit, state:LNGEng3LowSoCChargeMargin, state:LNGEng3CoversDeficit, state:LNGEng3DG1LowSoCChargeMargin, state:AllThermalWithinCapacity, state:OverloadBatteryLack, ... +18`。

#### SL-9 per-request 决策

- accepted_request_ids：`<derived-from-table>`；candidate_len=`8708`。

| request_id | decision | waiver | rework_locked | rationale / intent |
|---|---|---:|---:|---|
| `fixreq-0-sl7-0-be1e03bda7` | `accept` | ❌ | ✅ | Accepted. The request is rework-locked and the SL-7 unsafe_recovery finding remains valid: the original OverloadBatteryLack branch was entered for any demand above RES plus total thermal capacity and computed battery discharge without SoC or batt_Pmax suitability. The smallest safe DSL edit is to keep the NL-required overload dispatch action and scenario-req...<truncated 856 chars> |
- repair_rationale：Primary SL-7 repair: OverloadBatteryLack is still the NL-required branch for extreme demand above RES plus all thermal resources, but its forced guard now also requires SoC >= 0.2 and residual lack after all thermal capacity <= batt_Pmax. T...<truncated 118 chars>；Scenario regression repair: for overload_activates_all_thermal_and_battery_lack, the expected and actual state were already LNGShipEMS.OverloadBatteryLack and the power outputs/generator cut-ins matched. The previously rejected c442 candida...<truncated 211 chars>；Latest local design objection repair: the prior fa9a candidate added normal guarded self-transitions for RESCoversCharge, RESCoversSpare, and OverloadBatteryLack, which created W_FORCED_OVERRIDES_NORMAL because each self-transition duplicat...<truncated 149 chars>；Required grounding local_override mapping: guard:RESCoversCharge is concretely represented by the wildcard forced transition `! * -> RESCoversCharge : if [PL > 0 && Ppv + Pw >= PL && SoC < 0.95];`, and the state action charges residual RES ...<truncated 35 chars>；Required grounding local_override mapping: guard:RESCoversSpare is concretely represented by the wildcard forced transition `! * -> RESCoversSpare : if [PL > 0 && Ppv + Pw >= PL && SoC >= 0.95];`, and the state action sends residual RES to ...<truncated 25 chars>
- diff_summary：`{"summary": "Compared with the original DSL, only the OverloadBatteryLack forced-transition guard is strengthened with SoC >= 0.2 and residual battery-lack <= batt_Pmax. Overload load commands remain cmd_load_cut_in = 1 and cmd_load_cut_out = 0. The prior rejected self-transition grounding workaround is not included, avoiding W_FORCED_OVERRIDES_NORMAL while preserving all twelve states and required dispatch actions."}`。

#### SL-9 candidate / 最终修改执行方案

```pyfcstm
def float PL = 0.0;
def float Ppv = 0.0;
def float Pw = 0.0;
def float SoC = 0.5;
def float batt_Pmax = 0.0;
def float LNG_Pmax = 0.0;
def float eng3_Pmax = 0.0;
def float DG1_Pmax = 0.0;
def float DG2_Pmax = 0.0;
def float Pgmax = 0.0;
def float Pd1max = 0.0;
def float Pgen_req = 0.0;
def float Pbatt_discharge = 0.0;
def float Pbatt_charge = 0.0;
def float Pspare = 0.0;
def int cmd_LNG_cut_in = 0;
def int cmd_LNG_cut_out = 1;
def int cmd_eng3_cut_in = 0;
def int cmd_eng3_cut_out = 1;
def int cmd_DG1_cut_in = 0;
def int cmd_DG1_cut_out = 1;
def int cmd_DG2_cut_in = 0;
def int cmd_DG2_cut_out = 1;
def int cmd_load_cut_in = 1;
def int cmd_load_cut_out = 0;

state LNGShipEMS {
    ! * -> ZeroLoadCharge : if [PL == 0 && Ppv + Pw > 0 && SoC < 0.95];
    ! * -> ZeroLoadSpare : if [PL == 0 && SoC >= 0.95];
    ! * -> RESCoversCharge : if [PL > 0 && Ppv + Pw >= PL && SoC < 0.95];
    ! * -> RESCoversSpare : if [PL > 0 && Ppv + Pw >= PL && SoC >= 0.95];
    ! * -> RESBatteryDischarge : if [PL > 0 && Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw <= batt_Pmax];
    ! * -> LNGLowSoCChargeMargin : if [PL > 0 && Ppv + Pw < PL && SoC < 0.2 && PL - Ppv - Pw + Pgmax / 5 <= LNG_Pmax];
    ! * -> LNGCoversDeficit : if [PL > 0 && Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw > batt_Pmax && PL - Ppv - Pw <= LNG_Pmax];
    ! * -> LNGEng3LowSoCChargeMargin : if [PL > 0 && Ppv + Pw < PL && SoC < 0.2 && PL - Ppv - Pw + Pgmax / 5 > LNG_Pmax && PL - Ppv - Pw + Pd1max / 10 <= LNG_Pmax + eng3_Pmax];
    ! * -> LNGEng3CoversDeficit : if [PL > 0 && Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw > LNG_Pmax && PL - Ppv - Pw <= LNG_Pmax + eng3_Pmax];
    ! * -> LNGEng3DG1LowSoCChargeMargin : if [PL > 0 && Ppv + Pw < PL && SoC < 0.2 && PL - Ppv - Pw + Pd1max / 10 > LNG_Pmax + eng3_Pmax && PL - Ppv - Pw + Pd1max / 10 <= LNG_Pmax + eng3_Pmax + DG1_Pmax];
    ! * -> AllThermalWithinCapacity : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > LNG_Pmax + eng3_Pmax && PL - Ppv - Pw <= LNG_Pmax + eng3_Pmax + DG1_Pmax + DG2_Pmax];
    ! * -> OverloadBatteryLack : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > LNG_Pmax + eng3_Pmax + DG1_Pmax + DG2_Pmax && SoC >= 0.2 && PL - Ppv - Pw - LNG_Pmax - eng3_Pmax - DG1_Pmax - DG2_Pmax <= batt_Pmax];

    [*] -> ZeroLoadCharge;

    state ZeroLoadCharge {
        during {
            Pgen_req = 0.0;
            Pbatt_discharge = 0.0;
            Pbatt_charge = Ppv + Pw;
            Pspare = 0.0;
            cmd_LNG_cut_in = 0;
            cmd_LNG_cut_out = 1;
            cmd_eng3_cut_in = 0;
            cmd_eng3_cut_out = 1;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 0;
            cmd_load_cut_out = 1;
        }
    }

    state ZeroLoadSpare {
        during {
            Pgen_req = 0.0;
            Pbatt_discharge = 0.0;
            Pbatt_charge = 0.0;
            Pspare = Ppv + Pw;
            cmd_LNG_cut_in = 0;
            cmd_LNG_cut_out = 1;
            cmd_eng3_cut_in = 0;
            cmd_eng3_cut_out = 1;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 0;
            cmd_load_cut_out = 1;
        }
    }

    state RESCoversCharge {
        during {
            Pgen_req = 0.0;
            Pbatt_discharge = 0.0;
            Pbatt_charge = Ppv + Pw - PL;
            Pspare = 0.0;
            cmd_LNG_cut_in = 0;
            cmd_LNG_cut_out = 1;
            cmd_eng3_cut_in = 0;
            cmd_eng3_cut_out = 1;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state RESCoversSpare {
        during {
            Pgen_req = 0.0;
            Pbatt_discharge = 0.0;
            Pbatt_charge = 0.0;
            Pspare = Ppv + Pw - PL;
            cmd_LNG_cut_in = 0;
            cmd_LNG_cut_out = 1;
            cmd_eng3_cut_in = 0;
            cmd_eng3_cut_out = 1;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state RESBatteryDischarge {
        during {
            Pgen_req = 0.0;
            Pbatt_discharge = PL - Ppv - Pw;
            Pbatt_charge = 0.0;
            Pspare = 0.0;
            cmd_LNG_cut_in = 0;
            cmd_LNG_cut_out = 1;
            cmd_eng3_cut_in = 0;
            cmd_eng3_cut_out = 1;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state LNGLowSoCChargeMargin {
        during {
            Pgen_req = PL - Ppv - Pw + Pgmax / 5;
            Pbatt_discharge = 0.0;
            Pbatt_charge = Pgmax / 5;
            Pspare = 0.0;
            cmd_LNG_cut_in = 1;
            cmd_LNG_cut_out = 0;
            cmd_eng3_cut_in = 0;
            cmd_eng3_cut_out = 1;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state LNGCoversDeficit {
        during {
            Pgen_req = PL - Ppv - Pw;
            Pbatt_discharge = 0.0;
            Pbatt_charge = 0.0;
            Pspare = 0.0;
            cmd_LNG_cut_in = 1;
            cmd_LNG_cut_out = 0;
            cmd_eng3_cut_in = 0;
            cmd_eng3_cut_out = 1;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state LNGEng3LowSoCChargeMargin {
        during {
            Pgen_req = PL - Ppv - Pw + Pd1max / 10;
            Pbatt_discharge = 0.0;
            Pbatt_charge = Pd1max / 10;
            Pspare = 0.0;
            cmd_LNG_cut_in = 1;
            cmd_LNG_cut_out = 0;
            cmd_eng3_cut_in = 1;
            cmd_eng3_cut_out = 0;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state LNGEng3CoversDeficit {
        during {
            Pgen_req = PL - Ppv - Pw;
            Pbatt_discharge = 0.0;
            Pbatt_charge = 0.0;
            Pspare = 0.0;
            cmd_LNG_cut_in = 1;
            cmd_LNG_cut_out = 0;
            cmd_eng3_cut_in = 1;
            cmd_eng3_cut_out = 0;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state LNGEng3DG1LowSoCChargeMargin {
        during {
            Pgen_req = PL - Ppv - Pw + Pd1max / 10;
            Pbatt_discharge = 0.0;
            Pbatt_charge = Pd1max / 10;
            Pspare = 0.0;
            cmd_LNG_cut_in = 1;
            cmd_LNG_cut_out = 0;
            cmd_eng3_cut_in = 1;
            cmd_eng3_cut_out = 0;
            cmd_DG1_cut_in = 1;
            cmd_DG1_cut_out = 0;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state AllThermalWithinCapacity {
        during {
            Pgen_req = PL - Ppv - Pw;
            Pbatt_discharge = 0.0;
            Pbatt_charge = 0.0;
            Pspare = 0.0;
            cmd_LNG_cut_in = 1;
            cmd_LNG_cut_out = 0;
            cmd_eng3_cut_in = 1;
            cmd_eng3_cut_out = 0;
            cmd_DG1_cut_in = 1;
            cmd_DG1_cut_out = 0;
            cmd_DG2_cut_in = 1;
            cmd_DG2_cut_out = 0;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state OverloadBatteryLack {
        during {
            Pgen_req = LNG_Pmax + eng3_Pmax + DG1_Pmax + DG2_Pmax;
            Pbatt_discharge = PL - Ppv - Pw - LNG_Pmax - eng3_Pmax - DG1_Pmax - DG2_Pmax;
            Pbatt_charge = 0.0;
            Pspare = 0.0;
            cmd_LNG_cut_in = 1;
            cmd_LNG_cut_out = 0;
            cmd_eng3_cut_in = 1;
            cmd_eng3_cut_out = 0;
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
@@ -36,7 +36,7 @@
     ! * -> LNGEng3CoversDeficit : if [PL > 0 && Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw > LNG_Pmax && PL - Ppv - Pw <= LNG_Pmax + eng3_Pmax];
     ! * -> LNGEng3DG1LowSoCChargeMargin : if [PL > 0 && Ppv + Pw < PL && SoC < 0.2 && PL - Ppv - Pw + Pd1max / 10 > LNG_Pmax + eng3_Pmax && PL - Ppv - Pw + Pd1max / 10 <= LNG_Pmax + eng3_Pmax + DG1_Pmax];
     ! * -> AllThermalWithinCapacity : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > LNG_Pmax + eng3_Pmax && PL - Ppv - Pw <= LNG_Pmax + eng3_Pmax + DG1_Pmax + DG2_Pmax];
-    ! * -> OverloadBatteryLack : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > LNG_Pmax + eng3_Pmax + DG1_Pmax + DG2_Pmax];
+    ! * -> OverloadBatteryLack : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > LNG_Pmax + eng3_Pmax + DG1_Pmax + DG2_Pmax && SoC >= 0.2 && PL - Ppv - Pw - LNG_Pmax - eng3_Pmax - DG1_Pmax - DG2_Pmax <= batt_Pmax];
 
     [*] -> ZeroLoadCharge;
 
```

#### SL-10 审查结果

- SL-10 decision=`rework`，ok=`False`，target_resolved=`True`，regression_detected=`False`，drift_risk=`minor`。
- SL-10 review_meta：schema=`SL10RepairReviewOutput.v1`，failure_policy=`fail_closed`，replay_key=`SL-10:sha256:9a9e3169311232ee43f471e50cb1ddd2df6fb707126c7d6db54a119ade5ef5e5`。
  - SL-10 evidence 1: `{"summary": "The hard SL-7 unsafe_recovery request is substantively addressed by the candidate DSL. In the old DSL, OverloadBatteryLack was selected whenever PL - Ppv - Pw exceeded total thermal capacity and then computed Pbatt_discharge without SoC or batt_Pmax limits. The candidate strengthens only the OverloadBatteryLack forced-transition guard with SoC >= 0.2 and residual lack <= batt_Pmax, so the overload battery-discharge action is no longer entered without suitability and capacity checks."}`
  - SL-10 evidence 2: `{"summary": "The candidate preserves the NL-required overload dispatch behavior for the coverable overload case: OverloadBatteryLack still activates LNG, eng3, DG1, and DG2; sets Pgen_req to LNG_Pmax + eng3_Pmax + DG1_Pmax + DG2_Pmax; computes Pbatt_discharge as the residual lack; and keeps cmd_load_cut_in = 1 / cmd_load_cut_out = 0. This resolves the earlier scenario regression in overload_activates_all_thermal_and_battery_lack, where the c442 candidate had incorrectly changed the load commands to cut-out."}`
  - SL-10 evidence 3: `{"summary": "The diff is narrow and does not drop NL-required states, variables, guards, commands, or dispatch actions. All twelve required states remain, including ZeroLoadCharge, ZeroLoadSpare, RESCoversCharge, RESCoversSpare, RESBatteryDischarge, LNG priority states, diesel priority states, AllThermalWithinCapacity, and OverloadBatteryLack. Required inputs PL, Ppv, Pw, SoC, eng3_Pmax, Pgmax, Pd1max and required outputs Pgen_req, Pbatt_discharge, Pbatt_charge, Pspare and generator/load command flags remain present."}`
  - SL-10 evidence 4: `{"summary": "The RES coverage obligations remain represented exactly in the candidate DSL: RESCoversCharge is selected by the forced guard PL > 0 && Ppv + Pw >= PL && SoC < 0.95 and charges residual renewable power; RESCoversSpare is selected by PL > 0 && Ppv + Pw >= PL && SoC >= 0.95 and sends residual renewable power to Pspare. These match the NL threshold obligations for renewable coverage below and at/above SoC 0.95."}`
  - SL-10 evidence 5: `{"summary": "The complete FixLog and repair_memory were considered. The first rejected c442 candidate caused scenario_regression by changing OverloadBatteryLack load commands. The fa9a candidate attempted to add explicit self-transition guard grounding but introduced W_FORCED_OVERRIDES_NORMAL duplicate forced/normal diagnostics. The current candidate intentionally returns to the narrow a3d DSL edit, removes the redundant self-transitions, preserves the scenario-required load commands, and supplies explicit SL-9 rationale mapping each missing guard grounding id to concrete wildcard forced guarded transitions."}`
- SL-10 rework_instructions：SL-10 pass was downgraded because local deterministic evidence reported major drift and SL-10 evidence did not explicitly address the local rejection reason/kind with a structured local_override_rationale.；For the next SL-9 repair, do not blindly regenerate the same DSL. Either change the candidate so the local major-drift evidence is resolved, or keep the minimal DSL only with explicit repair_rationale mapping each local objection (for example missing_required_grounding, scenario_regression, count_drift, or forced_transition_count_drift) to concrete NL-ground...<truncated 152 chars>
- local checks evidence：stage=`SD-10`；note=PR-E1 uses local parse/semantic/design/sim checks as SL-10 evidence, not as the final deterministic judge.。
  - local ok=`False`，target_resolved=`False`，regression_detected=`False`，drift_risk=`major`。
  - local_rejection：reason=`missing_required_grounding`，rejected_by_stage=`SD-10`。
    - local evidence 1: `missing_required_grounding` {"element_ids": ["guard:RESCoversCharge", "guard:RESCoversSpare", "guard:OverloadBatteryLack"], "kind": "missing_required_grounding"}

</details>

<details><summary>Repair 5 / iteration `0` / source `SL-7` / accepted=✅</summary>

#### 为什么进入修复

- selected feedback source：`SL-7`；blocking=`True`；pre_scenario=`False`。
- problem_summary：model review failed
- diagnostic ids：`0`。
- before_dsl_hash：`sha256:01c5a57aa10618b447f8a2a830a9d8e06062db2bafb5fe2ac26d66485929c533`；candidate_dsl_hash：`sha256:813b635ee38132f66b9e8cd1fbf754f73d5598598eca4acef2ded16fddad4376`。

#### 错误证据 / diagnostics

- 1. `<unknown>` `` policy=``：The illegal overload state is treated as an ordinary reachable recovery/dispatch state and can command continued load service plus battery discharge without suitability or capacity guards.

#### SD-8 FixRequestBatch / 修改请求

- batch_id：`fixbatch-0-sha256-081cf0a961f`；source_stage=`SL-7`；legacy_plan_kind=`FixPlan`；requests=`1`。

| request_id | severity | hard | waiver | problem | evidence |
|---|---|---:|---:|---|---|
| `fixreq-0-sl7-0-be1e03bda7` | `review_fail` | ✅ | ❌ | model review failed | `{'category': 'unsafe_recovery', 'evidence': ['NL: "The overload completion state is illegal... the state shall never occur in practice."', 'DSL forced transition reaches `OverloadBatteryLack` whenever demand exceeds all RES and thermal resources.', '`OverloadBatteryLack` sets `cmd_load_cut_in = 1`, `cmd_load_cut_out = 0`, and computes `Pbatt_discharge` from the remaining lack without checking `SoC` or `batt_Pmax`.', 'sim_summary includes a passing overload scenario, showing this branch is accepted as normal behavior rather than flagged as illegal.'], 'severity': 'major', 'summary': 'The illegal overload state is treated as an ordinary reachable recovery/dispatch state and can command continued load service plus battery discharge without suitability or capacity guards.'}` |

#### SD-8 legacy fix plan / 修改建议

- recommended_strategy：Use diagnostics as hints; choose the smallest globally consistent repair.；Before returning a candidate, verify every required_preserve_element_id still has a concrete DSL representation.
- forbidden_edits：`Do not delete grounded required elements merely to silence diagnostics., Do not invent internal plant/environment dynamics merely to make external input variables appear written.`。
- required_preserve_element_ids：`state:ZeroLoadCharge, state:ZeroLoadSpare, state:RESCoversCharge, state:RESCoversSpare, state:RESBatteryDischarge, state:LNGLowSoCChargeMargin, state:LNGCoversDeficit, state:LNGEng3LowSoCChargeMargin, state:LNGEng3CoversDeficit, state:LNGEng3DG1LowSoCChargeMargin, state:AllThermalWithinCapacity, state:OverloadBatteryLack, ... +18`。

#### SL-9 per-request 决策

- accepted_request_ids：`<derived-from-table>`；candidate_len=`13269`。

| request_id | decision | waiver | rework_locked | rationale / intent |
|---|---|---:|---:|---|
| `fixreq-0-sl7-0-be1e03bda7` | `accept` | ❌ | ✅ | Accepted because the request is rework-locked and the SL-7 unsafe_recovery finding is valid. The original OverloadBatteryLack branch computed battery discharge for any residual demand above RES plus all thermal capacity without checking SoC or batt_Pmax. The repair strengthens the OverloadBatteryLack condition with SoC >= 0.2 and residual lack <= batt_Pmax w...<truncated 1176 chars> |
- repair_rationale：Primary SL-7 unsafe_recovery repair: OverloadBatteryLack is no longer selected solely because demand exceeds RES plus all thermal capacity. Its concrete guard now also requires SoC >= 0.2 and residual lack after LNG, eng3, DG1, and DG2 to b...<truncated 81 chars>；Scenario regression repair: the prior c442 candidate failed overload_activates_all_thermal_and_battery_lack because expected cmd_load_cut_in = 1 and cmd_load_cut_out = 0 but actual values were 0 and 1. This candidate preserves cmd_load_cut_...<truncated 148 chars>；Missing grounding repair for guard:RESCoversCharge: the guard PL > 0 && Ppv + Pw >= PL && SoC < 0.95 is now represented by explicit normal guarded transitions from every concrete state to RESCoversCharge; the state action remains Pbatt_char...<truncated 19 chars>；Missing grounding repair for guard:RESCoversSpare: the guard PL > 0 && Ppv + Pw >= PL && SoC >= 0.95 is now represented by explicit normal guarded transitions from every concrete state to RESCoversSpare; the state action remains Pspare = Pp...<truncated 12 chars>；Missing grounding repair for guard:OverloadBatteryLack: the overload guard is now represented by explicit normal guarded transitions from every concrete state to OverloadBatteryLack, including the new SoC and batt_Pmax suitability condition...<truncated 59 chars>
- diff_summary：`{"summary": "Strengthened the OverloadBatteryLack selection condition with SoC >= 0.2 and residual lack <= batt_Pmax while preserving overload dispatch/load commands. Replaced the wildcard forced transitions for RESCoversCharge, RESCoversSpare, and OverloadBatteryLack with explicit guarded transitions from all twelve concrete states to those targets, giving the three required guard elements concrete normal-transition grounding without duplicating forced and normal transitions."}`。

#### SL-9 candidate / 最终修改执行方案

```pyfcstm
def float PL = 0.0;
def float Ppv = 0.0;
def float Pw = 0.0;
def float SoC = 0.5;
def float batt_Pmax = 0.0;
def float LNG_Pmax = 0.0;
def float eng3_Pmax = 0.0;
def float DG1_Pmax = 0.0;
def float DG2_Pmax = 0.0;
def float Pgmax = 0.0;
def float Pd1max = 0.0;
def float Pgen_req = 0.0;
def float Pbatt_discharge = 0.0;
def float Pbatt_charge = 0.0;
def float Pspare = 0.0;
def int cmd_LNG_cut_in = 0;
def int cmd_LNG_cut_out = 1;
def int cmd_eng3_cut_in = 0;
def int cmd_eng3_cut_out = 1;
def int cmd_DG1_cut_in = 0;
def int cmd_DG1_cut_out = 1;
def int cmd_DG2_cut_in = 0;
def int cmd_DG2_cut_out = 1;
def int cmd_load_cut_in = 1;
def int cmd_load_cut_out = 0;

state LNGShipEMS {
    ! * -> ZeroLoadCharge : if [PL == 0 && Ppv + Pw > 0 && SoC < 0.95];
    ! * -> ZeroLoadSpare : if [PL == 0 && SoC >= 0.95];
    ! * -> RESBatteryDischarge : if [PL > 0 && Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw <= batt_Pmax];
    ! * -> LNGLowSoCChargeMargin : if [PL > 0 && Ppv + Pw < PL && SoC < 0.2 && PL - Ppv - Pw + Pgmax / 5 <= LNG_Pmax];
    ! * -> LNGCoversDeficit : if [PL > 0 && Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw > batt_Pmax && PL - Ppv - Pw <= LNG_Pmax];
    ! * -> LNGEng3LowSoCChargeMargin : if [PL > 0 && Ppv + Pw < PL && SoC < 0.2 && PL - Ppv - Pw + Pgmax / 5 > LNG_Pmax && PL - Ppv - Pw + Pd1max / 10 <= LNG_Pmax + eng3_Pmax];
    ! * -> LNGEng3CoversDeficit : if [PL > 0 && Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw > LNG_Pmax && PL - Ppv - Pw <= LNG_Pmax + eng3_Pmax];
    ! * -> LNGEng3DG1LowSoCChargeMargin : if [PL > 0 && Ppv + Pw < PL && SoC < 0.2 && PL - Ppv - Pw + Pd1max / 10 > LNG_Pmax + eng3_Pmax && PL - Ppv - Pw + Pd1max / 10 <= LNG_Pmax + eng3_Pmax + DG1_Pmax];
    ! * -> AllThermalWithinCapacity : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > LNG_Pmax + eng3_Pmax && PL - Ppv - Pw <= LNG_Pmax + eng3_Pmax + DG1_Pmax + DG2_Pmax];

    [*] -> ZeroLoadCharge;

    state ZeroLoadCharge {
        during {
            Pgen_req = 0.0;
            Pbatt_discharge = 0.0;
            Pbatt_charge = Ppv + Pw;
            Pspare = 0.0;
            cmd_LNG_cut_in = 0;
            cmd_LNG_cut_out = 1;
            cmd_eng3_cut_in = 0;
            cmd_eng3_cut_out = 1;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 0;
            cmd_load_cut_out = 1;
        }
    }

    state ZeroLoadSpare {
        during {
            Pgen_req = 0.0;
            Pbatt_discharge = 0.0;
            Pbatt_charge = 0.0;
            Pspare = Ppv + Pw;
            cmd_LNG_cut_in = 0;
            cmd_LNG_cut_out = 1;
            cmd_eng3_cut_in = 0;
            cmd_eng3_cut_out = 1;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 0;
            cmd_load_cut_out = 1;
        }
    }

    state RESCoversCharge {
        during {
            Pgen_req = 0.0;
            Pbatt_discharge = 0.0;
            Pbatt_charge = Ppv + Pw - PL;
            Pspare = 0.0;
            cmd_LNG_cut_in = 0;
            cmd_LNG_cut_out = 1;
            cmd_eng3_cut_in = 0;
            cmd_eng3_cut_out = 1;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state RESCoversSpare {
        during {
            Pgen_req = 0.0;
            Pbatt_discharge = 0.0;
            Pbatt_charge = 0.0;
            Pspare = Ppv + Pw - PL;
            cmd_LNG_cut_in = 0;
            cmd_LNG_cut_out = 1;
            cmd_eng3_cut_in = 0;
            cmd_eng3_cut_out = 1;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state RESBatteryDischarge {
        during {
            Pgen_req = 0.0;
            Pbatt_discharge = PL - Ppv - Pw;
            Pbatt_charge = 0.0;
            Pspare = 0.0;
            cmd_LNG_cut_in = 0;
            cmd_LNG_cut_out = 1;
            cmd_eng3_cut_in = 0;
            cmd_eng3_cut_out = 1;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state LNGLowSoCChargeMargin {
        during {
            Pgen_req = PL - Ppv - Pw + Pgmax / 5;
            Pbatt_discharge = 0.0;
            Pbatt_charge = Pgmax / 5;
            Pspare = 0.0;
            cmd_LNG_cut_in = 1;
            cmd_LNG_cut_out = 0;
            cmd_eng3_cut_in = 0;
            cmd_eng3_cut_out = 1;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state LNGCoversDeficit {
        during {
            Pgen_req = PL - Ppv - Pw;
            Pbatt_discharge = 0.0;
            Pbatt_charge = 0.0;
            Pspare = 0.0;
            cmd_LNG_cut_in = 1;
            cmd_LNG_cut_out = 0;
            cmd_eng3_cut_in = 0;
            cmd_eng3_cut_out = 1;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state LNGEng3LowSoCChargeMargin {
        during {
            Pgen_req = PL - Ppv - Pw + Pd1max / 10;
            Pbatt_discharge = 0.0;
            Pbatt_charge = Pd1max / 10;
            Pspare = 0.0;
            cmd_LNG_cut_in = 1;
            cmd_LNG_cut_out = 0;
            cmd_eng3_cut_in = 1;
            cmd_eng3_cut_out = 0;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state LNGEng3CoversDeficit {
        during {
            Pgen_req = PL - Ppv - Pw;
            Pbatt_discharge = 0.0;
            Pbatt_charge = 0.0;
            Pspare = 0.0;
            cmd_LNG_cut_in = 1;
            cmd_LNG_cut_out = 0;
            cmd_eng3_cut_in = 1;
            cmd_eng3_cut_out = 0;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state LNGEng3DG1LowSoCChargeMargin {
        during {
            Pgen_req = PL - Ppv - Pw + Pd1max / 10;
            Pbatt_discharge = 0.0;
            Pbatt_charge = Pd1max / 10;
            Pspare = 0.0;
            cmd_LNG_cut_in = 1;
            cmd_LNG_cut_out = 0;
            cmd_eng3_cut_in = 1;
            cmd_eng3_cut_out = 0;
            cmd_DG1_cut_in = 1;
            cmd_DG1_cut_out = 0;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state AllThermalWithinCapacity {
        during {
            Pgen_req = PL - Ppv - Pw;
            Pbatt_discharge = 0.0;
            Pbatt_charge = 0.0;
            Pspare = 0.0;
            cmd_LNG_cut_in = 1;
            cmd_LNG_cut_out = 0;
            cmd_eng3_cut_in = 1;
            cmd_eng3_cut_out = 0;
            cmd_DG1_cut_in = 1;
            cmd_DG1_cut_out = 0;
            cmd_DG2_cut_in = 1;
            cmd_DG2_cut_out = 0;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state OverloadBatteryLack {
        during {
            Pgen_req = LNG_Pmax + eng3_Pmax + DG1_Pmax + DG2_Pmax;
            Pbatt_discharge = PL - Ppv - Pw - LNG_Pmax - eng3_Pmax - DG1_Pmax - DG2_Pmax;
            Pbatt_charge = 0.0;
            Pspare = 0.0;
            cmd_LNG_cut_in = 1;
            cmd_LNG_cut_out = 0;
            cmd_eng3_cut_in = 1;
            cmd_eng3_cut_out = 0;
            cmd_DG1_cut_in = 1;
            cmd_DG1_cut_out = 0;
            cmd_DG2_cut_in = 1;
            cmd_DG2_cut_out = 0;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    ZeroLoadCharge -> RESCoversCharge : if [PL > 0 && Ppv + Pw >= PL && SoC < 0.95];
    ZeroLoadSpare -> RESCoversCharge : if [PL > 0 && Ppv + Pw >= PL && SoC < 0.95];
    RESCoversCharge -> RESCoversCharge : if [PL > 0 && Ppv + Pw >= PL && SoC < 0.95];
    RESCoversSpare -> RESCoversCharge : if [PL > 0 && Ppv + Pw >= PL && SoC < 0.95];
    RESBatteryDischarge -> RESCoversCharge : if [PL > 0 && Ppv + Pw >= PL && SoC < 0.95];
    LNGLowSoCChargeMargin -> RESCoversCharge : if [PL > 0 && Ppv + Pw >= PL && SoC < 0.95];
    LNGCoversDeficit -> RESCoversCharge : if [PL > 0 && Ppv + Pw >= PL && SoC < 0.95];
    LNGEng3LowSoCChargeMargin -> RESCoversCha
... <truncated 4269 chars; see run record>
```

#### Candidate diff（before -> candidate）

```diff
--- before.fcstm
+++ candidate.fcstm
@@ -27,8 +27,6 @@
 state LNGShipEMS {
     ! * -> ZeroLoadCharge : if [PL == 0 && Ppv + Pw > 0 && SoC < 0.95];
     ! * -> ZeroLoadSpare : if [PL == 0 && SoC >= 0.95];
-    ! * -> RESCoversCharge : if [PL > 0 && Ppv + Pw >= PL && SoC < 0.95];
-    ! * -> RESCoversSpare : if [PL > 0 && Ppv + Pw >= PL && SoC >= 0.95];
     ! * -> RESBatteryDischarge : if [PL > 0 && Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw <= batt_Pmax];
     ! * -> LNGLowSoCChargeMargin : if [PL > 0 && Ppv + Pw < PL && SoC < 0.2 && PL - Ppv - Pw + Pgmax / 5 <= LNG_Pmax];
     ! * -> LNGCoversDeficit : if [PL > 0 && Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw > batt_Pmax && PL - Ppv - Pw <= LNG_Pmax];
@@ -36,7 +34,6 @@
     ! * -> LNGEng3CoversDeficit : if [PL > 0 && Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw > LNG_Pmax && PL - Ppv - Pw <= LNG_Pmax + eng3_Pmax];
     ! * -> LNGEng3DG1LowSoCChargeMargin : if [PL > 0 && Ppv + Pw < PL && SoC < 0.2 && PL - Ppv - Pw + Pd1max / 10 > LNG_Pmax + eng3_Pmax && PL - Ppv - Pw + Pd1max / 10 <= LNG_Pmax + eng3_Pmax + DG1_Pmax];
     ! * -> AllThermalWithinCapacity : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > LNG_Pmax + eng3_Pmax && PL - Ppv - Pw <= LNG_Pmax + eng3_Pmax + DG1_Pmax + DG2_Pmax];
-    ! * -> OverloadBatteryLack : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > LNG_Pmax + eng3_Pmax + DG1_Pmax + DG2_Pmax];
 
     [*] -> ZeroLoadCharge;
 
@@ -267,4 +264,43 @@
             cmd_load_cut_out = 0;
         }
     }
+
+    ZeroLoadCharge -> RESCoversCharge : if [PL > 0 && Ppv + Pw >= PL && SoC < 0.95];
+    ZeroLoadSpare -> RESCoversCharge : if [PL > 0 && Ppv + Pw >= PL && SoC < 0.95];
+    RESCoversCharge -> RESCoversCharge : if [PL > 0 && Ppv + Pw >= PL && SoC < 0.95];
+    RESCoversSpare -> RESCoversCharge : if [PL > 0 && Ppv + Pw >= PL && SoC < 0.95];
+    RESBatteryDischarge -> RESCoversCharge : if [PL > 0 && Ppv + Pw >= PL && SoC < 0.95];
+    LNGLowSoCChargeMargin -> RESCoversCharge : if [PL > 0 && Ppv + Pw >= PL && SoC < 0.95];
+    LNGCoversDeficit -> RESCoversCharge : if [PL > 0 && Ppv + Pw >= PL && SoC < 0.95];
+    LNGEng3LowSoCChargeMargin -> RESCoversCharge : if [PL > 0 && Ppv + Pw >= PL && SoC < 0.95];
+    LNGEng3CoversDeficit -> RESCoversCharge : if [PL > 0 && Ppv + Pw >= PL && SoC < 0.95];
+    LNGEng3DG1LowSoCChargeMargin -> RESCoversCharge : if [PL > 0 && Ppv + Pw >= PL && SoC < 0.95];
+    AllThermalWithinCapacity -> RESCoversCharge : if [PL > 0 && Ppv + Pw >= PL && SoC < 0.95];
+    OverloadBatteryLack -> RESCoversCharge : if [PL > 0 && Ppv + Pw >= PL && SoC < 0.95];
+
+    ZeroLoadCharge -> RESCoversSpare : if [PL > 0 && Ppv + Pw >= PL && SoC >= 0.95];
+    ZeroLoadSpare -> RESCoversSpare : if [PL > 0 && Ppv + Pw >= PL && SoC >= 0.95];
+    RESCoversCharge -> RESCoversSpare : if [PL > 0 && Ppv + Pw >= PL && SoC >= 0.95];
+    RESCoversSpare -> RESCoversSpare : if [PL > 0 && Ppv + Pw >= PL && SoC >= 0.95];
+    RESBatteryDischarge -> RESCoversSpare : if [PL > 0 && Ppv + Pw >= PL && SoC >= 0.95];
+    LNGLowSoCChargeMargin -> RESCoversSpare : if [PL > 0 && Ppv + Pw >= PL && SoC >= 0.95];
+    LNGCoversDeficit -> RESCoversSpare : if [PL > 0 && Ppv + Pw >= PL && SoC >= 0.95];
+    LNGEng3LowSoCChargeMargin -> RESCoversSpare : if [PL > 0 && Ppv + Pw >= PL && SoC >= 0.95];
+    LNGEng3CoversDeficit -> RESCoversSpare : if [PL > 0 && Ppv + Pw >= PL && SoC >= 0.95];
+    LNGEng3DG1LowSoCChargeMargin -> RESCoversSpare : if [PL > 0 && Ppv + Pw >= PL && SoC >= 0.95];
+    AllThermalWithinCapacity -> RESCoversSpare : if [PL > 0 && Ppv + Pw >= PL && SoC >= 0.95];
+    OverloadBatteryLack -> RESCoversSpare : if [PL > 0 && Ppv + Pw >= PL && SoC >= 0.95];
+
+    ZeroLoadCharge -> OverloadBatteryLack : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > LNG_Pmax + eng3_Pmax + DG1_Pmax + DG2_Pmax && SoC >= 0.2 && PL - Ppv - Pw - LNG_Pmax - eng3_Pmax - DG1_Pmax - DG2_Pmax <= batt_Pmax];
+    ZeroLoadSpare -> OverloadBatteryLack : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > LNG_Pmax + eng3_Pmax + DG1_Pmax + DG2_Pmax && SoC >= 0.2 && PL - Ppv - Pw - LNG_Pmax - eng3_Pmax - DG1_Pmax - DG2_Pmax <= batt_Pmax];
+    RESCoversCharge -> OverloadBatteryLack : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > LNG_Pmax + eng3_Pmax + DG1_Pmax + DG2_Pmax && SoC >= 0.2 && PL - Ppv - Pw - LNG_Pmax - eng3_Pmax - DG1_Pmax - DG2_Pmax <= batt_Pmax];
+    RESCoversSpare -> OverloadBatteryLack : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > LNG_Pmax + eng3_Pmax + DG1_Pmax + DG2_Pmax && SoC >= 0.2 && PL - Ppv - Pw - LNG_Pmax - eng3_Pmax - DG1_Pmax - DG2_Pmax <= batt_Pmax];
+    RESBatteryDischarge -> OverloadBatteryLack : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > LNG_Pmax + eng3_Pmax + DG1_Pmax + DG2_Pmax && SoC >= 0.2 && PL - Ppv - Pw - LNG_Pmax - eng3_Pmax - DG1_Pmax - DG2_Pmax <= batt_Pmax];
+    LNGLowSoCChargeMargin -> OverloadBatteryLack : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > LNG_Pmax + eng3_Pmax + DG1_Pmax + DG2_Pmax && SoC >= 0.2 && PL - Ppv - Pw - LNG_Pmax - eng3_Pmax - DG1_Pmax - DG2_Pmax <= batt_Pmax];
+    LNGCoversDeficit -> OverloadBatteryLack : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > LNG_Pmax + eng3_Pmax + DG1_Pmax + DG2_Pmax && SoC >= 0.2 && PL - Ppv - Pw - LNG_Pmax - eng3_Pmax - DG1_Pmax - DG2_Pmax <= batt_Pmax];
+    LNGEng3LowSoCChargeMargin -> OverloadBatteryLack : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > LNG_Pmax + eng3_Pmax + DG1_Pmax + DG2_Pmax && SoC >= 0.2 && PL - Ppv - Pw - LNG_Pmax - eng3_Pmax - DG1_Pmax - DG2_Pmax <= batt_Pmax];
+    LNGEng3CoversDeficit -> OverloadBatteryLack : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > LNG_Pmax + eng3_Pmax + DG1_Pmax + DG2_Pmax && SoC >= 0.2 && PL - Ppv - Pw - LNG_Pmax - eng3_Pmax - DG1_Pmax - DG2_Pmax <= batt_Pmax];
+    LNGEng3DG1LowSoCChargeMargin -> OverloadBatteryLack : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > LNG_Pmax + eng3_Pmax + DG1_Pmax + DG2_Pmax && SoC >= 0.2 && PL - Ppv - Pw - LNG_Pmax - eng3_Pmax - DG1_Pmax - DG2_Pmax <= batt_Pmax];
+    AllThermalWithinCapacity -> OverloadBatteryLack : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > LNG_Pmax + eng3_Pmax + DG1_Pmax + DG2_Pmax && SoC >= 0.2 && PL - Ppv - Pw - LNG_Pmax - eng3_Pmax - DG1_Pmax - DG2_Pmax <= batt_Pmax];
+    OverloadBatteryLack -> OverloadBatteryLack : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > LNG_Pmax + eng3_Pmax + DG1_Pmax + DG2_Pmax && SoC >= 0.2 && PL - Ppv - Pw - LNG_Pmax - eng3_Pmax - DG1_Pmax - DG2_Pmax <= batt_Pmax];
 }
```

#### SL-10 审查结果

- SL-10 decision=`pass`，ok=`True`，target_resolved=`True`，regression_detected=`False`，drift_risk=`minor`。
- SL-10 review_meta：schema=`SL10RepairReviewOutput.v1`，failure_policy=`fail_closed`，replay_key=`SL-10:sha256:753963f18ed29c053d482a154773f6fd1da16bdcb730feb9e4c73b787a53c45c`。
  - SL-10 evidence 1: `{"summary": "The hard NL/SL-7 target was unsafe recovery in OverloadBatteryLack: the original model entered the overload branch whenever demand exceeded RES plus all thermal capacity and computed Pbatt_discharge without SoC or batt_Pmax limits. The candidate strengthens every OverloadBatteryLack selection condition with SoC >= 0.2 and residual lack <= batt_Pmax, so the overload battery discharge action is no longer unbounded or entered without battery suitability/capacity checks."}`
  - SL-10 evidence 2: `{"summary": "The candidate preserves the NL-required overload dispatch behavior for the coverable emergency case: OverloadBatteryLack remains present, activates LNG, eng3, DG1, and DG2, sets Pgen_req to total thermal capacity, computes Pbatt_discharge as the residual lack, and preserves cmd_load_cut_in = 1 / cmd_load_cut_out = 0. This directly addresses the earlier scenario_regression in overload_activates_all_thermal_and_battery_lack where only load commands had mismatched expected 1/0 versus actual 0/1."}`
  - SL-10 evidence 3: `{"summary": "No NL-required states, variables, outputs, or dispatch actions are dropped. All twelve required states remain, including ZeroLoadCharge, ZeroLoadSpare, RESCoversCharge, RESCoversSpare, RESBatteryDischarge, LNG priority states, diesel priority states, AllThermalWithinCapacity, and OverloadBatteryLack. Required inputs PL, Ppv, Pw, SoC, eng3_Pmax, Pgmax, Pd1max and required outputs Pgen_req, Pbatt_discharge, Pbatt_charge, Pspare plus generator/load command flags remain present."}`
  - SL-10 evidence 4: `{"summary": "The FixLog repair_memory was followed. The rejected c442 candidate regressed overload load commands; this candidate preserves the scenario-required load commands. The fa9a candidate added normal self-transitions while keeping wildcard forced transitions and caused W_FORCED_OVERRIDES_NORMAL duplicate forced/normal diagnostics; this candidate avoids that by replacing, not duplicating, the three affected wildcard forced classifiers with explicit guarded normal transitions from all concrete states. The repeated a3d hash objection is also addressed by a new candidate hash and a substantive DSL change."}`
  - SL-10 evidence 5: `{"summary": "The local deterministic check reports no scenario_regression for the current candidate. Its remaining objections are forced_transition_count_drift and missing_required_grounding, not a behavioral scenario failure."}`
- local checks evidence：stage=`SD-10`；note=PR-E1 uses local parse/semantic/design/sim checks as SL-10 evidence, not as the final deterministic judge.。
  - local ok=`False`，target_resolved=`False`，regression_detected=`False`，drift_risk=`major`。
  - local_rejection：reason=`forced_transition_count_drift; missing_required_grounding`，rejected_by_stage=`SD-10`。
    - local evidence 1: `forced_transition_count_drift` {"fix_target": "model_review", "kind": "forced_transition_count_drift", "new": 108, "old": 144}
    - local evidence 2: `missing_required_grounding` {"element_ids": ["guard:RESCoversCharge", "guard:RESCoversSpare", "guard:OverloadBatteryLack"], "kind": "missing_required_grounding"}

</details>

<details><summary>Repair 6 / iteration `1` / source `SL-7` / accepted=✅</summary>

#### 为什么进入修复

- selected feedback source：`SL-7`；blocking=`True`；pre_scenario=`False`。
- problem_summary：model review failed
- diagnostic ids：`0, 1, 2`。
- before_dsl_hash：`sha256:813b635ee38132f66b9e8cd1fbf754f73d5598598eca4acef2ded16fddad4376`；candidate_dsl_hash：`sha256:ad6bb952e971dcc754c511a5baf3833ec55994c5a265657833e894faa5829c16`。

#### 错误证据 / diagnostics

- 1. `<unknown>` `` policy=``：Thermal-unit priority is not faithfully modeled: DG2 is cut in for all deficits above LNG+eng3 capacity, including cases where DG1 alone would satisfy the deficit.
- 2. `<unknown>` `` policy=``：The illegal overload completion state is reachable and treated as a passing operational state rather than being prevented, isolated, or explicitly marked as illegal.
- 3. `<unknown>` `` policy=``：NFRR quality is capped at approximately T2 because the candidate has material NL-fidelity and safety/illegal-state gaps despite broad component presence and passing scenarios.

#### SD-8 FixRequestBatch / 修改请求

- batch_id：`fixbatch-1-sha256-00855f2776f`；source_stage=`SL-7`；legacy_plan_kind=`FixPlan`；requests=`3`。

| request_id | severity | hard | waiver | problem | evidence |
|---|---|---:|---:|---|---|
| `fixreq-1-sl7-0-3096823055` | `review_fail` | ✅ | ❌ | model review failed | `{'category': 'nl_fidelity', 'evidence': ['NL: "LNG before diesel units, and DG1/DG2 only as the last priority."', 'No DG1-only suitable-SoC state or guard is present.', 'AllThermalWithinCapacity guard covers the entire range up to LNG+eng3+DG1+DG2.', 'AllThermalWithinCapacity action sets both `cmd_DG1_cut_in = 1` and `cmd_DG2_cut_in = 1`.'], 'severity': 'major', 'summary': 'Thermal-unit priority is not faithfully modeled: DG2 is cut in for all deficits above LNG+eng3 capacity, including cases where DG1 alone would satisfy the deficit.'}` |
| `fixreq-1-sl7-1-f1f2c62158` | `review_fail` | ✅ | ❌ | model review failed | `{'category': 'unsafe_recovery', 'evidence': ['NL: "The overload completion state is illegal" and "the state shall never occur in practice."', 'DSL defines reachable transitions to `OverloadBatteryLack` from every modeled state.', '`OverloadBatteryLack` has normal dispatch actions and keeps load cut in.', 'Simulation validates `OverloadBatteryLack` as a passing expected scenario.'], 'severity': 'major', 'summary': 'The illegal overload completion state is reachable and treated as a passing operational state rather than being prevented, isolated, or explicitly marked as illegal.'}` |
| `fixreq-1-sl7-2-2d6f65a397` | `review_fail` | ✅ | ❌ | model review failed | `{'category': 'nfrr_quality_cap', 'evidence': ['Missing DG1-only branch violates dispatch-priority coverage.', 'Reachable overload state conflicts with illegal-state wording in the NL.', 'five_component_summary is empty, and the simulation oracle validates rather than challenges the illegal overload branch.'], 'severity': 'major', 'summary': 'NFRR quality is capped at approximately T2 because the candidate has material NL-fidelity and safety/illegal-state gaps despite broad component presence and passing scenarios.'}` |

#### SD-8 legacy fix plan / 修改建议

- recommended_strategy：Use diagnostics as hints; choose the smallest globally consistent repair.；Before returning a candidate, verify every required_preserve_element_id still has a concrete DSL representation.
- forbidden_edits：`Do not delete grounded required elements merely to silence diagnostics., Do not invent internal plant/environment dynamics merely to make external input variables appear written.`。
- required_preserve_element_ids：`state:ZeroLoadCharge, state:ZeroLoadSpare, state:RESCoversCharge, state:RESCoversSpare, state:RESBatteryDischarge, state:LNGLowSoCChargeMargin, state:LNGCoversDeficit, state:LNGEng3LowSoCChargeMargin, state:LNGEng3CoversDeficit, state:LNGEng3DG1LowSoCChargeMargin, state:AllThermalWithinCapacity, state:OverloadBatteryLack, ... +18`。

#### SL-9 per-request 决策

- accepted_request_ids：`<derived-from-table>`；candidate_len=`14405`。

| request_id | decision | waiver | rework_locked | rationale / intent |
|---|---|---:|---:|---|
| `fixreq-1-sl7-0-3096823055` | `accept` | ❌ | ❌ | Accepted. The review evidence is valid: the prior dispatch cut in DG2 for all demand above LNG+eng3 capacity, even when DG1 alone could satisfy the remaining deficit. The repair adds an explicit DG1-only suitable-SoC branch and narrows AllThermalWithinCapacity to only the range where DG2 is actually needed.；intent=Add a DG1-only suitable-SoC dispatch state.,...<truncated 176 chars> |
| `fixreq-1-sl7-1-f1f2c62158` | `accept` | ❌ | ❌ | Accepted. The unsafe-recovery evidence is valid. The overload branch must not be a normal unconstrained completion path. The repair preserves the NL-grounded overload action for the coverable emergency case but keeps the prior safety strengthening: OverloadBatteryLack is selected only when SoC is suitable and the residual lack is within batt_Pmax.；intent=Kee...<truncated 256 chars> |
| `fixreq-1-sl7-2-2d6f65a397` | `accept` | ❌ | ❌ | Accepted. The NFRR quality cap is caused by the same material NL-fidelity and safety gaps. The repair addresses both root causes with minimal NL-grounded structural edits while preserving all required states, variables, RES guards, overload dispatch action, and existing normal guard grounding for RESCoversCharge, RESCoversSpare, and OverloadBatteryLack.；inte...<truncated 215 chars> |
- repair_rationale：Thermal priority repair: LNGEng3DG1CoversDeficit is added for the suitable-SoC range where LNG plus eng3 plus DG1 can satisfy the deficit. Its action cuts in LNG, eng3, and DG1 while keeping DG2 cut out, so DG2 is no longer used prematurely...<truncated 1 chars>；AllThermalWithinCapacity is narrowed to deficits greater than LNG_Pmax + eng3_Pmax + DG1_Pmax and within LNG_Pmax + eng3_Pmax + DG1_Pmax + DG2_Pmax, so DG2 is reserved for the final thermal-capacity priority tier.；Unsafe overload repair is preserved: every OverloadBatteryLack normal guard requires demand above total thermal capacity, SoC >= 0.2, and residual lack <= batt_Pmax. This prevents unbounded or low-SoC battery-discharge entry while preservin...<truncated 90 chars>；Required grounding retained: guard:RESCoversCharge remains concretely represented by normal guarded transitions to RESCoversCharge with PL > 0 && Ppv + Pw >= PL && SoC < 0.95 and the state charges residual renewable power.；Required grounding retained: guard:RESCoversSpare remains concretely represented by normal guarded transitions to RESCoversSpare with PL > 0 && Ppv + Pw >= PL && SoC >= 0.95 and the state sends residual renewable power to Pspare.
- diff_summary：`{"summary": "Added a DG1-only suitable-SoC dispatch state and forced classifier; narrowed AllThermalWithinCapacity to only cases requiring DG2; preserved strengthened OverloadBatteryLack guards with SoC and batt_Pmax limits; added the new state as a source for the existing concrete RES coverage and overload normal guard transitions while preserving all required variables, existing required states, RES actions, overload dispatch action, and load-service commands."}`。

#### SL-9 candidate / 最终修改执行方案

```pyfcstm
def float PL = 0.0;
def float Ppv = 0.0;
def float Pw = 0.0;
def float SoC = 0.5;
def float batt_Pmax = 0.0;
def float LNG_Pmax = 0.0;
def float eng3_Pmax = 0.0;
def float DG1_Pmax = 0.0;
def float DG2_Pmax = 0.0;
def float Pgmax = 0.0;
def float Pd1max = 0.0;
def float Pgen_req = 0.0;
def float Pbatt_discharge = 0.0;
def float Pbatt_charge = 0.0;
def float Pspare = 0.0;
def int cmd_LNG_cut_in = 0;
def int cmd_LNG_cut_out = 1;
def int cmd_eng3_cut_in = 0;
def int cmd_eng3_cut_out = 1;
def int cmd_DG1_cut_in = 0;
def int cmd_DG1_cut_out = 1;
def int cmd_DG2_cut_in = 0;
def int cmd_DG2_cut_out = 1;
def int cmd_load_cut_in = 1;
def int cmd_load_cut_out = 0;

state LNGShipEMS {
    ! * -> ZeroLoadCharge : if [PL == 0 && Ppv + Pw > 0 && SoC < 0.95];
    ! * -> ZeroLoadSpare : if [PL == 0 && SoC >= 0.95];
    ! * -> RESBatteryDischarge : if [PL > 0 && Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw <= batt_Pmax];
    ! * -> LNGLowSoCChargeMargin : if [PL > 0 && Ppv + Pw < PL && SoC < 0.2 && PL - Ppv - Pw + Pgmax / 5 <= LNG_Pmax];
    ! * -> LNGCoversDeficit : if [PL > 0 && Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw > batt_Pmax && PL - Ppv - Pw <= LNG_Pmax];
    ! * -> LNGEng3LowSoCChargeMargin : if [PL > 0 && Ppv + Pw < PL && SoC < 0.2 && PL - Ppv - Pw + Pgmax / 5 > LNG_Pmax && PL - Ppv - Pw + Pd1max / 10 <= LNG_Pmax + eng3_Pmax];
    ! * -> LNGEng3CoversDeficit : if [PL > 0 && Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw > LNG_Pmax && PL - Ppv - Pw <= LNG_Pmax + eng3_Pmax];
    ! * -> LNGEng3DG1LowSoCChargeMargin : if [PL > 0 && Ppv + Pw < PL && SoC < 0.2 && PL - Ppv - Pw + Pd1max / 10 > LNG_Pmax + eng3_Pmax && PL - Ppv - Pw + Pd1max / 10 <= LNG_Pmax + eng3_Pmax + DG1_Pmax];
    ! * -> LNGEng3DG1CoversDeficit : if [PL > 0 && Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw > LNG_Pmax + eng3_Pmax && PL - Ppv - Pw <= LNG_Pmax + eng3_Pmax + DG1_Pmax];
    ! * -> AllThermalWithinCapacity : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > LNG_Pmax + eng3_Pmax + DG1_Pmax && PL - Ppv - Pw <= LNG_Pmax + eng3_Pmax + DG1_Pmax + DG2_Pmax];

    [*] -> ZeroLoadCharge;

    state ZeroLoadCharge {
        during {
            Pgen_req = 0.0;
            Pbatt_discharge = 0.0;
            Pbatt_charge = Ppv + Pw;
            Pspare = 0.0;
            cmd_LNG_cut_in = 0;
            cmd_LNG_cut_out = 1;
            cmd_eng3_cut_in = 0;
            cmd_eng3_cut_out = 1;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 0;
            cmd_load_cut_out = 1;
        }
    }

    state ZeroLoadSpare {
        during {
            Pgen_req = 0.0;
            Pbatt_discharge = 0.0;
            Pbatt_charge = 0.0;
            Pspare = Ppv + Pw;
            cmd_LNG_cut_in = 0;
            cmd_LNG_cut_out = 1;
            cmd_eng3_cut_in = 0;
            cmd_eng3_cut_out = 1;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 0;
            cmd_load_cut_out = 1;
        }
    }

    state RESCoversCharge {
        during {
            Pgen_req = 0.0;
            Pbatt_discharge = 0.0;
            Pbatt_charge = Ppv + Pw - PL;
            Pspare = 0.0;
            cmd_LNG_cut_in = 0;
            cmd_LNG_cut_out = 1;
            cmd_eng3_cut_in = 0;
            cmd_eng3_cut_out = 1;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state RESCoversSpare {
        during {
            Pgen_req = 0.0;
            Pbatt_discharge = 0.0;
            Pbatt_charge = 0.0;
            Pspare = Ppv + Pw - PL;
            cmd_LNG_cut_in = 0;
            cmd_LNG_cut_out = 1;
            cmd_eng3_cut_in = 0;
            cmd_eng3_cut_out = 1;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state RESBatteryDischarge {
        during {
            Pgen_req = 0.0;
            Pbatt_discharge = PL - Ppv - Pw;
            Pbatt_charge = 0.0;
            Pspare = 0.0;
            cmd_LNG_cut_in = 0;
            cmd_LNG_cut_out = 1;
            cmd_eng3_cut_in = 0;
            cmd_eng3_cut_out = 1;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state LNGLowSoCChargeMargin {
        during {
            Pgen_req = PL - Ppv - Pw + Pgmax / 5;
            Pbatt_discharge = 0.0;
            Pbatt_charge = Pgmax / 5;
            Pspare = 0.0;
            cmd_LNG_cut_in = 1;
            cmd_LNG_cut_out = 0;
            cmd_eng3_cut_in = 0;
            cmd_eng3_cut_out = 1;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state LNGCoversDeficit {
        during {
            Pgen_req = PL - Ppv - Pw;
            Pbatt_discharge = 0.0;
            Pbatt_charge = 0.0;
            Pspare = 0.0;
            cmd_LNG_cut_in = 1;
            cmd_LNG_cut_out = 0;
            cmd_eng3_cut_in = 0;
            cmd_eng3_cut_out = 1;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state LNGEng3LowSoCChargeMargin {
        during {
            Pgen_req = PL - Ppv - Pw + Pd1max / 10;
            Pbatt_discharge = 0.0;
            Pbatt_charge = Pd1max / 10;
            Pspare = 0.0;
            cmd_LNG_cut_in = 1;
            cmd_LNG_cut_out = 0;
            cmd_eng3_cut_in = 1;
            cmd_eng3_cut_out = 0;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state LNGEng3CoversDeficit {
        during {
            Pgen_req = PL - Ppv - Pw;
            Pbatt_discharge = 0.0;
            Pbatt_charge = 0.0;
            Pspare = 0.0;
            cmd_LNG_cut_in = 1;
            cmd_LNG_cut_out = 0;
            cmd_eng3_cut_in = 1;
            cmd_eng3_cut_out = 0;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state LNGEng3DG1LowSoCChargeMargin {
        during {
            Pgen_req = PL - Ppv - Pw + Pd1max / 10;
            Pbatt_discharge = 0.0;
            Pbatt_charge = Pd1max / 10;
            Pspare = 0.0;
            cmd_LNG_cut_in = 1;
            cmd_LNG_cut_out = 0;
            cmd_eng3_cut_in = 1;
            cmd_eng3_cut_out = 0;
            cmd_DG1_cut_in = 1;
            cmd_DG1_cut_out = 0;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state LNGEng3DG1CoversDeficit {
        during {
            Pgen_req = PL - Ppv - Pw;
            Pbatt_discharge = 0.0;
            Pbatt_charge = 0.0;
            Pspare = 0.0;
            cmd_LNG_cut_in = 1;
            cmd_LNG_cut_out = 0;
            cmd_eng3_cut_in = 1;
            cmd_eng3_cut_out = 0;
            cmd_DG1_cut_in = 1;
            cmd_DG1_cut_out = 0;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state AllThermalWithinCapacity {
        during {
            Pgen_req = PL - Ppv - Pw;
            Pbatt_discharge = 0.0;
            Pbatt_charge = 0.0;
            Pspare = 0.0;
            cmd_LNG_cut_in = 1;
            cmd_LNG_cut_out = 0;
            cmd_eng3_cut_in = 1;
            cmd_eng3_cut_out = 0;
            cmd_DG1_cut_in = 1;
            cmd_DG1_cut_out = 0;
            cmd_DG2_cut_in = 1;
            cmd_DG2_cut_out = 0;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state OverloadBatteryLack {
        during {
            Pgen_req = LNG_Pmax + eng3_Pmax + DG1_Pmax + DG2_Pmax;
            Pbatt_discharge = PL - Ppv - Pw - LNG_Pmax - eng3_Pmax - DG1_Pmax - DG2_Pmax;
            Pbatt_charge = 0.0;
            Pspare = 0.0;
            cmd_LNG_cut_in = 1;
            cmd_LNG_cut_out = 0;
            cmd_eng3_cut_in = 1;
            cmd_eng3_cut_out = 0;
            cmd_DG1_cut_in = 1;
            cmd_DG1_cut_out = 0;
            cmd_DG2_cut_in = 1;
            cmd_DG2_cut_out = 0;
            cmd_load_cut
... <truncated 5405 chars; see run record>
```

#### Candidate diff（before -> candidate）

```diff
--- before.fcstm
+++ candidate.fcstm
@@ -33,7 +33,8 @@
     ! * -> LNGEng3LowSoCChargeMargin : if [PL > 0 && Ppv + Pw < PL && SoC < 0.2 && PL - Ppv - Pw + Pgmax / 5 > LNG_Pmax && PL - Ppv - Pw + Pd1max / 10 <= LNG_Pmax + eng3_Pmax];
     ! * -> LNGEng3CoversDeficit : if [PL > 0 && Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw > LNG_Pmax && PL - Ppv - Pw <= LNG_Pmax + eng3_Pmax];
     ! * -> LNGEng3DG1LowSoCChargeMargin : if [PL > 0 && Ppv + Pw < PL && SoC < 0.2 && PL - Ppv - Pw + Pd1max / 10 > LNG_Pmax + eng3_Pmax && PL - Ppv - Pw + Pd1max / 10 <= LNG_Pmax + eng3_Pmax + DG1_Pmax];
-    ! * -> AllThermalWithinCapacity : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > LNG_Pmax + eng3_Pmax && PL - Ppv - Pw <= LNG_Pmax + eng3_Pmax + DG1_Pmax + DG2_Pmax];
+    ! * -> LNGEng3DG1CoversDeficit : if [PL > 0 && Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw > LNG_Pmax + eng3_Pmax && PL - Ppv - Pw <= LNG_Pmax + eng3_Pmax + DG1_Pmax];
+    ! * -> AllThermalWithinCapacity : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > LNG_Pmax + eng3_Pmax + DG1_Pmax && PL - Ppv - Pw <= LNG_Pmax + eng3_Pmax + DG1_Pmax + DG2_Pmax];
 
     [*] -> ZeroLoadCharge;
 
@@ -213,6 +214,25 @@
             Pgen_req = PL - Ppv - Pw + Pd1max / 10;
             Pbatt_discharge = 0.0;
             Pbatt_charge = Pd1max / 10;
+            Pspare = 0.0;
+            cmd_LNG_cut_in = 1;
+            cmd_LNG_cut_out = 0;
+            cmd_eng3_cut_in = 1;
+            cmd_eng3_cut_out = 0;
+            cmd_DG1_cut_in = 1;
+            cmd_DG1_cut_out = 0;
+            cmd_DG2_cut_in = 0;
+            cmd_DG2_cut_out = 1;
+            cmd_load_cut_in = 1;
+            cmd_load_cut_out = 0;
+        }
+    }
+
+    state LNGEng3DG1CoversDeficit {
+        during {
+            Pgen_req = PL - Ppv - Pw;
+            Pbatt_discharge = 0.0;
+            Pbatt_charge = 0.0;
             Pspare = 0.0;
             cmd_LNG_cut_in = 1;
             cmd_LNG_cut_out = 0;
@@ -275,6 +295,7 @@
     LNGEng3LowSoCChargeMargin -> RESCoversCharge : if [PL > 0 && Ppv + Pw >= PL && SoC < 0.95];
     LNGEng3CoversDeficit -> RESCoversCharge : if [PL > 0 && Ppv + Pw >= PL && SoC < 0.95];
     LNGEng3DG1LowSoCChargeMargin -> RESCoversCharge : if [PL > 0 && Ppv + Pw >= PL && SoC < 0.95];
+    LNGEng3DG1CoversDeficit -> RESCoversCharge : if [PL > 0 && Ppv + Pw >= PL && SoC < 0.95];
     AllThermalWithinCapacity -> RESCoversCharge : if [PL > 0 && Ppv + Pw >= PL && SoC < 0.95];
     OverloadBatteryLack -> RESCoversCharge : if [PL > 0 && Ppv + Pw >= PL && SoC < 0.95];
 
@@ -288,6 +309,7 @@
     LNGEng3LowSoCChargeMargin -> RESCoversSpare : if [PL > 0 && Ppv + Pw >= PL && SoC >= 0.95];
     LNGEng3CoversDeficit -> RESCoversSpare : if [PL > 0 && Ppv + Pw >= PL && SoC >= 0.95];
     LNGEng3DG1LowSoCChargeMargin -> RESCoversSpare : if [PL > 0 && Ppv + Pw >= PL && SoC >= 0.95];
+    LNGEng3DG1CoversDeficit -> RESCoversSpare : if [PL > 0 && Ppv + Pw >= PL && SoC >= 0.95];
     AllThermalWithinCapacity -> RESCoversSpare : if [PL > 0 && Ppv + Pw >= PL && SoC >= 0.95];
     OverloadBatteryLack -> RESCoversSpare : if [PL > 0 && Ppv + Pw >= PL && SoC >= 0.95];
 
@@ -301,6 +323,7 @@
     LNGEng3LowSoCChargeMargin -> OverloadBatteryLack : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > LNG_Pmax + eng3_Pmax + DG1_Pmax + DG2_Pmax && SoC >= 0.2 && PL - Ppv - Pw - LNG_Pmax - eng3_Pmax - DG1_Pmax - DG2_Pmax <= batt_Pmax];
     LNGEng3CoversDeficit -> OverloadBatteryLack : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > LNG_Pmax + eng3_Pmax + DG1_Pmax + DG2_Pmax && SoC >= 0.2 && PL - Ppv - Pw - LNG_Pmax - eng3_Pmax - DG1_Pmax - DG2_Pmax <= batt_Pmax];
     LNGEng3DG1LowSoCChargeMargin -> OverloadBatteryLack : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > LNG_Pmax + eng3_Pmax + DG1_Pmax + DG2_Pmax && SoC >= 0.2 && PL - Ppv - Pw - LNG_Pmax - eng3_Pmax - DG1_Pmax - DG2_Pmax <= batt_Pmax];
+    LNGEng3DG1CoversDeficit -> OverloadBatteryLack : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > LNG_Pmax + eng3_Pmax + DG1_Pmax + DG2_Pmax && SoC >= 0.2 && PL - Ppv - Pw - LNG_Pmax - eng3_Pmax - DG1_Pmax - DG2_Pmax <= batt_Pmax];
     AllThermalWithinCapacity -> OverloadBatteryLack : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > LNG_Pmax + eng3_Pmax + DG1_Pmax + DG2_Pmax && SoC >= 0.2 && PL - Ppv - Pw - LNG_Pmax - eng3_Pmax - DG1_Pmax - DG2_Pmax <= batt_Pmax];
     OverloadBatteryLack -> OverloadBatteryLack : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > LNG_Pmax + eng3_Pmax + DG1_Pmax + DG2_Pmax && SoC >= 0.2 && PL - Ppv - Pw - LNG_Pmax - eng3_Pmax - DG1_Pmax - DG2_Pmax <= batt_Pmax];
 }
```

#### SL-10 审查结果

- SL-10 decision=`pass`，ok=`True`，target_resolved=`True`，regression_detected=`False`，drift_risk=`minor`。
- SL-10 review_meta：schema=`SL10RepairReviewOutput.v1`，failure_policy=`fail_closed`，replay_key=`SL-10:sha256:bd5ed2b8ea0d63a5bd35826e33b378dda19ae2de4e1114c786660d04c9b06fe9`。
  - SL-10 evidence 1: `{"summary": "The SL-7 thermal-priority hard block is substantively resolved. The NL requires dispatch priority of RES first, batteries when suitable, LNG before diesel units, and DG1/DG2 only as last priority. The old DSL sent every suitable-SoC deficit above LNG+eng3 directly to AllThermalWithinCapacity and cut in both DG1 and DG2, even when DG1 alone could cover the remaining deficit. The candidate adds LNGEng3DG1CoversDeficit for PL > 0, RES below load, SoC >= 0.2, and deficit within LNG_Pmax + eng3_Pmax + DG1_Pmax; its action cuts in LNG, eng3, and DG1 while keeping DG2 cut out. AllThermalWithinCapacity is narrowed to deficits greater than LNG+eng3+DG1 and within LNG+eng3+DG1+DG2, so DG2...<truncated 47 chars>`
  - SL-10 evidence 2: `{"summary": "The unsafe overload hard block remains repaired from prior accepted work. The candidate preserves the strengthened OverloadBatteryLack transition condition requiring demand above RES plus all thermal capacity, SoC >= 0.2, and residual lack <= batt_Pmax. This prevents the old unsafe behavior where the overload branch computed Pbatt_discharge without SoC suitability or battery discharge capacity limits."}`
  - SL-10 evidence 3: `{"summary": "The NL-required overload dispatch action is preserved for the coverable emergency case: OverloadBatteryLack still activates LNG, eng3, DG1, and DG2; sets Pgen_req to LNG_Pmax + eng3_Pmax + DG1_Pmax + DG2_Pmax; computes Pbatt_discharge as the remaining lack; sets Pbatt_charge = 0 and Pspare = 0; and preserves cmd_load_cut_in = 1 / cmd_load_cut_out = 0. This also preserves the prior scenario-regression fix where an earlier rejected candidate had incorrectly changed overload load commands to cut-out."}`
  - SL-10 evidence 4: `{"summary": "The NFRR quality-cap root causes identified in the request batch are addressed: missing DG1-only priority coverage is repaired, and overload reachability is constrained by battery suitability and capacity. The candidate also preserves the required states and variables from the grounding map, including ZeroLoadCharge, ZeroLoadSpare, RESCoversCharge, RESCoversSpare, RESBatteryDischarge, low-SoC charge-margin states, LNG/eng3 states, AllThermalWithinCapacity, OverloadBatteryLack, PL, Ppv, Pw, SoC, eng3_Pmax, Pgmax, Pd1max, Pgen_req, Pbatt_discharge, Pbatt_charge, Pspare, and generator/load command flags."}`
  - SL-10 evidence 5: `{"summary": "The RES coverage obligations remain represented. RESCoversCharge is selected by normal guarded transitions under PL > 0 && Ppv + Pw >= PL && SoC < 0.95 and charges residual renewable power with Pbatt_charge = Ppv + Pw - PL. RESCoversSpare is selected under PL > 0 && Ppv + Pw >= PL && SoC >= 0.95 and sends residual renewable power to Pspare = Ppv + Pw - PL."}`
  - SL-10 evidence 6: `{"summary": "The complete FixLog and repair_memory were considered. Earlier candidates failed or required rework because c442 regressed overload load commands, fa9a introduced duplicate forced/normal self-transitions, and a3d relied on wildcard forced guard mappings that local checks still reported as missing grounding. The currently reviewed candidate builds on the previously accepted 813-style structure with concrete normal guard transitions and adds the DG1-only branch plus corresponding RES/overload transition sources, avoiding the known overload-command regression and avoiding the duplicate forced/normal self-transition pattern."}`
- local checks evidence：stage=`SD-10`；note=PR-E1 uses local parse/semantic/design/sim checks as SL-10 evidence, not as the final deterministic judge.。
  - local ok=`False`，target_resolved=`False`，regression_detected=`False`，drift_risk=`major`。
  - local_rejection：reason=`forced_transition_count_drift; missing_required_grounding`，rejected_by_stage=`SD-10`。
    - local evidence 1: `forced_transition_count_drift` {"fix_target": "model_review", "kind": "forced_transition_count_drift", "new": 130, "old": 108}
    - local evidence 2: `missing_required_grounding` {"element_ids": ["guard:RESCoversCharge", "guard:RESCoversSpare", "guard:OverloadBatteryLack"], "kind": "missing_required_grounding"}

</details>

<details><summary>Repair 7 / iteration `2` / source `SL-7` / accepted=❌</summary>

#### 为什么进入修复

- selected feedback source：`SL-7`；blocking=`True`；pre_scenario=`False`。
- problem_summary：model review failed
- diagnostic ids：`0, 1`。
- before_dsl_hash：`sha256:ad6bb952e971dcc754c511a5baf3833ec55994c5a265657833e894faa5829c16`；candidate_dsl_hash：`sha256:0aac73439d9e4fa4e943fc2d2cead8b9851b5b7084ee281ee912e5eb12f35388`。

#### 错误证据 / diagnostics

- 1. `<unknown>` `` policy=``：The illegal overload completion state is reachable and validated as normal behavior, contrary to the NL statement that it is illegal and shall never occur in practice.
- 2. `<unknown>` `` policy=``：Illegal-state semantics are not preserved: the DSL treats OverloadBatteryLack as an ordinary reachable EMS state.

#### SD-8 FixRequestBatch / 修改请求

- batch_id：`fixbatch-2-sha256-29c6b5ff10b`；source_stage=`SL-7`；legacy_plan_kind=`FixPlan`；requests=`2`。

| request_id | severity | hard | waiver | problem | evidence |
|---|---|---:|---:|---|---|
| `fixreq-2-sl7-0-e56a9044a1` | `review_fail` | ✅ | ❌ | model review failed | `{'category': 'unsafe_recovery', 'evidence': ['NL: "The overload completion state is illegal" and "the state shall never occur in practice."', 'DSL has state OverloadBatteryLack with operational during actions.', 'DSL includes transitions from all main states to OverloadBatteryLack under overload guards.', 'sim_summary includes a passing scenario that targets OverloadBatteryLack.'], 'severity': 'major', 'summary': 'The illegal overload completion state is reachable and validated as normal behavior, contrary to the NL statement that it is illegal and shall never occur in practice.'}` |
| `fixreq-2-sl7-1-ef61a52a60` | `review_fail` | ✅ | ❌ | model review failed | `{'category': 'nl_fidelity', 'evidence': ['OverloadBatteryLack has ordinary output assignments and command settings.', 'cmd_load_cut_in remains 1 and cmd_load_cut_out remains 0 in OverloadBatteryLack.', 'There is no explicit error, assertion, unreachable marker, or recovery separation for the illegal state.'], 'severity': 'major', 'summary': 'Illegal-state semantics are not preserved: the DSL treats OverloadBatteryLack as an ordinary reachable EMS state.'}` |

#### SD-8 legacy fix plan / 修改建议

- recommended_strategy：Use diagnostics as hints; choose the smallest globally consistent repair.；Before returning a candidate, verify every required_preserve_element_id still has a concrete DSL representation.
- forbidden_edits：`Do not delete grounded required elements merely to silence diagnostics., Do not invent internal plant/environment dynamics merely to make external input variables appear written.`。
- required_preserve_element_ids：`state:ZeroLoadCharge, state:ZeroLoadSpare, state:RESCoversCharge, state:RESCoversSpare, state:RESBatteryDischarge, state:LNGLowSoCChargeMargin, state:LNGCoversDeficit, state:LNGEng3LowSoCChargeMargin, state:LNGEng3CoversDeficit, state:LNGEng3DG1LowSoCChargeMargin, state:AllThermalWithinCapacity, state:OverloadBatteryLack, ... +18`。

#### SL-9 per-request 决策

- accepted_request_ids：`<derived-from-table>`；candidate_len=`11731`。

| request_id | decision | waiver | rework_locked | rationale / intent |
|---|---|---:|---:|---|
| `fixreq-2-sl7-0-e56a9044a1` | `accept` | ❌ | ❌ | Accepted. The review evidence is valid: the current model still permits normal operational transitions from concrete EMS states into OverloadBatteryLack, which contradicts the NL statement that the overload completion state is illegal and shall never occur in practice. The repair preserves the required OverloadBatteryLack state and dispatch action, but remov...<truncated 528 chars> |
| `fixreq-2-sl7-1-ef61a52a60` | `accept` | ❌ | ❌ | Accepted. Illegal-state semantics were not explicit: OverloadBatteryLack looked like an ordinary dispatch state with normal commands. The repair makes it a preserved but non-operational illegal marker state: no main dispatch state transitions into it, and entry sets overload_illegal = 1. The existing dispatch assignments remain only as the preserved grounded...<truncated 312 chars> |
- repair_rationale：Both current hard requests are accepted because the SL-7 evidence identifies a real NL-fidelity gap: OverloadBatteryLack was treated as a normal reachable dispatch state even though the NL calls the overload completion state illegal and say...<truncated 35 chars>；Smallest safe edit: remove all ordinary incoming transitions from concrete EMS dispatch states to OverloadBatteryLack. This directly addresses the evidence item that the DSL included transitions from all main states to the illegal state.；Preservation: state:OverloadBatteryLack and action:OverloadBatteryLackDispatch are not deleted. The state still contains the all-thermal cut-in, total thermal Pgen_req, residual Pbatt_discharge, Pbatt_charge = 0, Pspare = 0, and load-servic...<truncated 89 chars>；Illegal-state semantics: added def int overload_illegal = 0 and OverloadBatteryLack.enter sets overload_illegal = 1, giving an explicit marker that entering this state is illegal rather than an ordinary completion path.；guard:OverloadBatteryLack remains concretely represented by the strengthened guard on OverloadBatteryLack -> OverloadBatteryLack. It includes demand above RES plus all thermal capacity, SoC >= 0.2, and residual lack <= batt_Pmax. This prese...<truncated 106 chars>
- diff_summary：`{"summary": "Added overload_illegal marker and OverloadBatteryLack.enter action; removed normal incoming transitions from all concrete dispatch states to OverloadBatteryLack; preserved OverloadBatteryLack dispatch actions and represented the overload guard as a non-operational self-guard on the illegal state while keeping RESCoversCharge and RESCoversSpare guard transitions intact."}`。

#### SL-9 candidate / 最终修改执行方案

```pyfcstm
def float PL = 0.0;
def float Ppv = 0.0;
def float Pw = 0.0;
def float SoC = 0.5;
def float batt_Pmax = 0.0;
def float LNG_Pmax = 0.0;
def float eng3_Pmax = 0.0;
def float DG1_Pmax = 0.0;
def float DG2_Pmax = 0.0;
def float Pgmax = 0.0;
def float Pd1max = 0.0;
def float Pgen_req = 0.0;
def float Pbatt_discharge = 0.0;
def float Pbatt_charge = 0.0;
def float Pspare = 0.0;
def int cmd_LNG_cut_in = 0;
def int cmd_LNG_cut_out = 1;
def int cmd_eng3_cut_in = 0;
def int cmd_eng3_cut_out = 1;
def int cmd_DG1_cut_in = 0;
def int cmd_DG1_cut_out = 1;
def int cmd_DG2_cut_in = 0;
def int cmd_DG2_cut_out = 1;
def int cmd_load_cut_in = 1;
def int cmd_load_cut_out = 0;
def int overload_illegal = 0;

state LNGShipEMS {
    ! * -> ZeroLoadCharge : if [PL == 0 && Ppv + Pw > 0 && SoC < 0.95];
    ! * -> ZeroLoadSpare : if [PL == 0 && SoC >= 0.95];
    ! * -> RESBatteryDischarge : if [PL > 0 && Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw <= batt_Pmax];
    ! * -> LNGLowSoCChargeMargin : if [PL > 0 && Ppv + Pw < PL && SoC < 0.2 && PL - Ppv - Pw + Pgmax / 5 <= LNG_Pmax];
    ! * -> LNGCoversDeficit : if [PL > 0 && Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw > batt_Pmax && PL - Ppv - Pw <= LNG_Pmax];
    ! * -> LNGEng3LowSoCChargeMargin : if [PL > 0 && Ppv + Pw < PL && SoC < 0.2 && PL - Ppv - Pw + Pgmax / 5 > LNG_Pmax && PL - Ppv - Pw + Pd1max / 10 <= LNG_Pmax + eng3_Pmax];
    ! * -> LNGEng3CoversDeficit : if [PL > 0 && Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw > LNG_Pmax && PL - Ppv - Pw <= LNG_Pmax + eng3_Pmax];
    ! * -> LNGEng3DG1LowSoCChargeMargin : if [PL > 0 && Ppv + Pw < PL && SoC < 0.2 && PL - Ppv - Pw + Pd1max / 10 > LNG_Pmax + eng3_Pmax && PL - Ppv - Pw + Pd1max / 10 <= LNG_Pmax + eng3_Pmax + DG1_Pmax];
    ! * -> LNGEng3DG1CoversDeficit : if [PL > 0 && Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw > LNG_Pmax + eng3_Pmax && PL - Ppv - Pw <= LNG_Pmax + eng3_Pmax + DG1_Pmax];
    ! * -> AllThermalWithinCapacity : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > LNG_Pmax + eng3_Pmax + DG1_Pmax && PL - Ppv - Pw <= LNG_Pmax + eng3_Pmax + DG1_Pmax + DG2_Pmax];

    [*] -> ZeroLoadCharge;

    state ZeroLoadCharge {
        during {
            Pgen_req = 0.0;
            Pbatt_discharge = 0.0;
            Pbatt_charge = Ppv + Pw;
            Pspare = 0.0;
            cmd_LNG_cut_in = 0;
            cmd_LNG_cut_out = 1;
            cmd_eng3_cut_in = 0;
            cmd_eng3_cut_out = 1;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 0;
            cmd_load_cut_out = 1;
        }
    }

    state ZeroLoadSpare {
        during {
            Pgen_req = 0.0;
            Pbatt_discharge = 0.0;
            Pbatt_charge = 0.0;
            Pspare = Ppv + Pw;
            cmd_LNG_cut_in = 0;
            cmd_LNG_cut_out = 1;
            cmd_eng3_cut_in = 0;
            cmd_eng3_cut_out = 1;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 0;
            cmd_load_cut_out = 1;
        }
    }

    state RESCoversCharge {
        during {
            Pgen_req = 0.0;
            Pbatt_discharge = 0.0;
            Pbatt_charge = Ppv + Pw - PL;
            Pspare = 0.0;
            cmd_LNG_cut_in = 0;
            cmd_LNG_cut_out = 1;
            cmd_eng3_cut_in = 0;
            cmd_eng3_cut_out = 1;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state RESCoversSpare {
        during {
            Pgen_req = 0.0;
            Pbatt_discharge = 0.0;
            Pbatt_charge = 0.0;
            Pspare = Ppv + Pw - PL;
            cmd_LNG_cut_in = 0;
            cmd_LNG_cut_out = 1;
            cmd_eng3_cut_in = 0;
            cmd_eng3_cut_out = 1;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state RESBatteryDischarge {
        during {
            Pgen_req = 0.0;
            Pbatt_discharge = PL - Ppv - Pw;
            Pbatt_charge = 0.0;
            Pspare = 0.0;
            cmd_LNG_cut_in = 0;
            cmd_LNG_cut_out = 1;
            cmd_eng3_cut_in = 0;
            cmd_eng3_cut_out = 1;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state LNGLowSoCChargeMargin {
        during {
            Pgen_req = PL - Ppv - Pw + Pgmax / 5;
            Pbatt_discharge = 0.0;
            Pbatt_charge = Pgmax / 5;
            Pspare = 0.0;
            cmd_LNG_cut_in = 1;
            cmd_LNG_cut_out = 0;
            cmd_eng3_cut_in = 0;
            cmd_eng3_cut_out = 1;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state LNGCoversDeficit {
        during {
            Pgen_req = PL - Ppv - Pw;
            Pbatt_discharge = 0.0;
            Pbatt_charge = 0.0;
            Pspare = 0.0;
            cmd_LNG_cut_in = 1;
            cmd_LNG_cut_out = 0;
            cmd_eng3_cut_in = 0;
            cmd_eng3_cut_out = 1;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state LNGEng3LowSoCChargeMargin {
        during {
            Pgen_req = PL - Ppv - Pw + Pd1max / 10;
            Pbatt_discharge = 0.0;
            Pbatt_charge = Pd1max / 10;
            Pspare = 0.0;
            cmd_LNG_cut_in = 1;
            cmd_LNG_cut_out = 0;
            cmd_eng3_cut_in = 1;
            cmd_eng3_cut_out = 0;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state LNGEng3CoversDeficit {
        during {
            Pgen_req = PL - Ppv - Pw;
            Pbatt_discharge = 0.0;
            Pbatt_charge = 0.0;
            Pspare = 0.0;
            cmd_LNG_cut_in = 1;
            cmd_LNG_cut_out = 0;
            cmd_eng3_cut_in = 1;
            cmd_eng3_cut_out = 0;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state LNGEng3DG1LowSoCChargeMargin {
        during {
            Pgen_req = PL - Ppv - Pw + Pd1max / 10;
            Pbatt_discharge = 0.0;
            Pbatt_charge = Pd1max / 10;
            Pspare = 0.0;
            cmd_LNG_cut_in = 1;
            cmd_LNG_cut_out = 0;
            cmd_eng3_cut_in = 1;
            cmd_eng3_cut_out = 0;
            cmd_DG1_cut_in = 1;
            cmd_DG1_cut_out = 0;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state LNGEng3DG1CoversDeficit {
        during {
            Pgen_req = PL - Ppv - Pw;
            Pbatt_discharge = 0.0;
            Pbatt_charge = 0.0;
            Pspare = 0.0;
            cmd_LNG_cut_in = 1;
            cmd_LNG_cut_out = 0;
            cmd_eng3_cut_in = 1;
            cmd_eng3_cut_out = 0;
            cmd_DG1_cut_in = 1;
            cmd_DG1_cut_out = 0;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state AllThermalWithinCapacity {
        during {
            Pgen_req = PL - Ppv - Pw;
            Pbatt_discharge = 0.0;
            Pbatt_charge = 0.0;
            Pspare = 0.0;
            cmd_LNG_cut_in = 1;
            cmd_LNG_cut_out = 0;
            cmd_eng3_cut_in = 1;
            cmd_eng3_cut_out = 0;
            cmd_DG1_cut_in = 1;
            cmd_DG1_cut_out = 0;
            cmd_DG2_cut_in = 1;
            cmd_DG2_cut_out = 0;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state OverloadBatteryLack {
        enter {
            overload_illegal = 1;
        }
        during {
            Pgen_req = LNG_Pmax + eng3_Pmax + DG1_Pmax + DG2_Pmax;
            Pbatt_discharge = PL - Ppv - Pw - LNG_Pmax - eng3_Pmax - DG1_Pmax - DG2_Pmax;
            Pbatt_charge = 0.0;
            Pspare = 0.0;
            cmd_LNG_cut_in = 1;
            cmd_LNG_cut_out = 0;
            cmd_eng3_cut_in = 1;
            cmd_eng3_cut_out = 0;
            cmd_DG1_cut_in = 1;
            cmd_DG1_cut_out = 0;
... <truncated 2731 chars; see run record>
```

#### Candidate diff（before -> candidate）

```diff
--- before.fcstm
+++ candidate.fcstm
@@ -23,6 +23,7 @@
 def int cmd_DG2_cut_out = 1;
 def int cmd_load_cut_in = 1;
 def int cmd_load_cut_out = 0;
+def int overload_illegal = 0;
 
 state LNGShipEMS {
     ! * -> ZeroLoadCharge : if [PL == 0 && Ppv + Pw > 0 && SoC < 0.95];
@@ -267,6 +268,9 @@
     }
 
     state OverloadBatteryLack {
+        enter {
+            overload_illegal = 1;
+        }
         during {
             Pgen_req = LNG_Pmax + eng3_Pmax + DG1_Pmax + DG2_Pmax;
             Pbatt_discharge = PL - Ppv - Pw - LNG_Pmax - eng3_Pmax - DG1_Pmax - DG2_Pmax;
@@ -313,17 +317,5 @@
     AllThermalWithinCapacity -> RESCoversSpare : if [PL > 0 && Ppv + Pw >= PL && SoC >= 0.95];
     OverloadBatteryLack -> RESCoversSpare : if [PL > 0 && Ppv + Pw >= PL && SoC >= 0.95];
 
-    ZeroLoadCharge -> OverloadBatteryLack : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > LNG_Pmax + eng3_Pmax + DG1_Pmax + DG2_Pmax && SoC >= 0.2 && PL - Ppv - Pw - LNG_Pmax - eng3_Pmax - DG1_Pmax - DG2_Pmax <= batt_Pmax];
-    ZeroLoadSpare -> OverloadBatteryLack : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > LNG_Pmax + eng3_Pmax + DG1_Pmax + DG2_Pmax && SoC >= 0.2 && PL - Ppv - Pw - LNG_Pmax - eng3_Pmax - DG1_Pmax - DG2_Pmax <= batt_Pmax];
-    RESCoversCharge -> OverloadBatteryLack : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > LNG_Pmax + eng3_Pmax + DG1_Pmax + DG2_Pmax && SoC >= 0.2 && PL - Ppv - Pw - LNG_Pmax - eng3_Pmax - DG1_Pmax - DG2_Pmax <= batt_Pmax];
-    RESCoversSpare -> OverloadBatteryLack : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > LNG_Pmax + eng3_Pmax + DG1_Pmax + DG2_Pmax && SoC >= 0.2 && PL - Ppv - Pw - LNG_Pmax - eng3_Pmax - DG1_Pmax - DG2_Pmax <= batt_Pmax];
-    RESBatteryDischarge -> OverloadBatteryLack : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > LNG_Pmax + eng3_Pmax + DG1_Pmax + DG2_Pmax && SoC >= 0.2 && PL - Ppv - Pw - LNG_Pmax - eng3_Pmax - DG1_Pmax - DG2_Pmax <= batt_Pmax];
-    LNGLowSoCChargeMargin -> OverloadBatteryLack : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > LNG_Pmax + eng3_Pmax + DG1_Pmax + DG2_Pmax && SoC >= 0.2 && PL - Ppv - Pw - LNG_Pmax - eng3_Pmax - DG1_Pmax - DG2_Pmax <= batt_Pmax];
-    LNGCoversDeficit -> OverloadBatteryLack : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > LNG_Pmax + eng3_Pmax + DG1_Pmax + DG2_Pmax && SoC >= 0.2 && PL - Ppv - Pw - LNG_Pmax - eng3_Pmax - DG1_Pmax - DG2_Pmax <= batt_Pmax];
-    LNGEng3LowSoCChargeMargin -> OverloadBatteryLack : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > LNG_Pmax + eng3_Pmax + DG1_Pmax + DG2_Pmax && SoC >= 0.2 && PL - Ppv - Pw - LNG_Pmax - eng3_Pmax - DG1_Pmax - DG2_Pmax <= batt_Pmax];
-    LNGEng3CoversDeficit -> OverloadBatteryLack : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > LNG_Pmax + eng3_Pmax + DG1_Pmax + DG2_Pmax && SoC >= 0.2 && PL - Ppv - Pw - LNG_Pmax - eng3_Pmax - DG1_Pmax - DG2_Pmax <= batt_Pmax];
-    LNGEng3DG1LowSoCChargeMargin -> OverloadBatteryLack : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > LNG_Pmax + eng3_Pmax + DG1_Pmax + DG2_Pmax && SoC >= 0.2 && PL - Ppv - Pw - LNG_Pmax - eng3_Pmax - DG1_Pmax - DG2_Pmax <= batt_Pmax];
-    LNGEng3DG1CoversDeficit -> OverloadBatteryLack : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > LNG_Pmax + eng3_Pmax + DG1_Pmax + DG2_Pmax && SoC >= 0.2 && PL - Ppv - Pw - LNG_Pmax - eng3_Pmax - DG1_Pmax - DG2_Pmax <= batt_Pmax];
-    AllThermalWithinCapacity -> OverloadBatteryLack : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > LNG_Pmax + eng3_Pmax + DG1_Pmax + DG2_Pmax && SoC >= 0.2 && PL - Ppv - Pw - LNG_Pmax - eng3_Pmax - DG1_Pmax - DG2_Pmax <= batt_Pmax];
     OverloadBatteryLack -> OverloadBatteryLack : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > LNG_Pmax + eng3_Pmax + DG1_Pmax + DG2_Pmax && SoC >= 0.2 && PL - Ppv - Pw - LNG_Pmax - eng3_Pmax - DG1_Pmax - DG2_Pmax <= batt_Pmax];
 }
```

#### SL-10 审查结果

- SL-10 decision=`rework`，ok=`False`，target_resolved=`False`，regression_detected=`True`，drift_risk=`major`。
- SL-10 review_meta：schema=`SL10RepairReviewOutput.v1`，failure_policy=`fail_closed`，replay_key=`SL-10:sha256:c2d9af26d222c27e84c384bab0a064dc6824b63329ac5d9d132ded44c80f9f5a`。
  - SL-10 evidence 1: `{"summary": "The candidate partially addresses the SL-7 illegal-state concern by adding overload_illegal and removing normal incoming transitions to OverloadBatteryLack, but it over-corrects and drops an NL-required overload behavior. The NL requires that when extreme demand exceeds RES and thermal resources, the EMS activates all thermal generating units and covers the lack by battery discharge, while also treating that completion state as illegal/should-not-occur in practice. Making OverloadBatteryLack unreachable removes the runtime dispatch path for that stated emergency branch."}`
  - SL-10 evidence 2: `{"summary": "Local deterministic evidence reports a real scenario regression, not merely conservative grounding drift. Scenario wrong_target_probe_lng_to_overload_lack starts in LNGCoversDeficit with PL=220, Ppv=10, Pw=10, SoC=0.5, batt_Pmax=100, LNG_Pmax=80, eng3_Pmax=30, DG1_Pmax=30, DG2_Pmax=20. Expected step 0 target is LNGShipEMS.OverloadBatteryLack with Pgen_req=160, Pbatt_discharge=40, Pbatt_charge=0, Pspare=0, all thermal cut-in commands set to 1/0, and cmd_load_cut_in=1/cmd_load_cut_out=0. Actual state remains LNGShipEMS.LNGCoversDeficit, so the overload dispatch action is not reached."}`
  - SL-10 evidence 3: `{"summary": "The new W_UNREACHABLE_STATE diagnostic is directly caused by the DSL diff: all normal incoming transitions from concrete dispatch states to OverloadBatteryLack were removed, leaving only an OverloadBatteryLack self-loop. Because the state is required by the grounding map and its dispatch action is required, this is not an acceptable dead-state representation."}`
  - SL-10 evidence 4: `{"summary": "The FixLog repair memory shows prior acceptable direction: preserve OverloadBatteryLack dispatch, preserve cmd_load_cut_in=1/cmd_load_cut_out=0, and constrain overload selection with SoC >= 0.2 and residual lack <= batt_Pmax. The current candidate preserves the commands but regresses reachability and therefore breaks the previously passing overload scenario obligation."}`
  - SL-10 evidence 5: `{"summary": "The candidate also continues to trigger missing_required_grounding for guard:RESCoversCharge, guard:RESCoversSpare, and guard:OverloadBatteryLack. RES guards appear textually present, but the overload guard is now only a self-loop on an unreachable state, which is not sufficient concrete runtime grounding for the required overload branch."}`
- SL-10 rework_instructions：Restore concrete guarded inbound transitions from normal dispatch states to OverloadBatteryLack for the strengthened overload condition: PL > 0, Ppv + Pw < PL, PL - Ppv - Pw > LNG_Pmax + eng3_Pmax + DG1_Pmax + DG2_Pmax, SoC >= 0.2, and residual lack <= batt_Pmax. Do not rely on an OverloadBatteryLack self-loop to ground this guard.；Keep overload_illegal as an explicit illegal-state marker, but make it coexist with the required emergency dispatch path. OverloadBatteryLack.enter may set overload_illegal = 1, and/or the restored inbound transitions may set overload_illegal = 1 in an effect block if the DSL supports effects.；Preserve action:OverloadBatteryLackDispatch exactly for the scenario/NL emergency branch: Pgen_req = LNG_Pmax + eng3_Pmax + DG1_Pmax + DG2_Pmax; Pbatt_discharge = PL - Ppv - Pw - LNG_Pmax - eng3_Pmax - DG1_Pmax - DG2_Pmax; Pbatt_charge = 0; Pspare = 0; all LNG/eng3/DG1/DG2 cut-in commands enabled; cmd_load_cut_in = 1 and cmd_load_cut_out = 0.；Specifically repair the failed scenario wrong_target_probe_lng_to_overload_lack: from LNGCoversDeficit under PL=220, Ppv=10, Pw=10, SoC=0.5, batt_Pmax=100, LNG_Pmax=80, eng3_Pmax=30, DG1_Pmax=30, DG2_Pmax=20, one step must transition to OverloadBatteryLack and produce Pgen_req=160 and Pbatt_discharge=40 with the expected thermal/load commands.；Do not remove the required OverloadBatteryLack state or its dispatch action. Do not leave it unreachable from the root entry path. Do not add only a self-loop to mask grounding.；Keep the RESCoversCharge and RESCoversSpare guarded transitions intact: PL > 0 && Ppv + Pw >= PL && SoC < 0.95 must select RESCoversCharge with residual renewable battery charging, and PL > 0 && Ppv + Pw >= PL && SoC >= 0.95 must select RESCoversSpare with residual renewable spare power.
- local checks evidence：stage=`SD-10`；note=PR-E1 uses local parse/semantic/design/sim checks as SL-10 evidence, not as the final deterministic judge.。
  - local ok=`False`，target_resolved=`False`，regression_detected=`True`，drift_risk=`major`。
  - local_rejection：reason=`new_blocking_design_diagnostic; scenario_regression; missing_required_grounding`，rejected_by_stage=`SD-10`。
    - local evidence 1: `new_blocking_design_diagnostic` {"items": [{"budget_exhausted": false, "budget_remaining": 2, "code": "W_UNREACHABLE_STATE", "instance_key": "W_UNREACHABLE_STATE:state_path=LNGShipEMS.OverloadBatteryLack", "message": "State 'LNGShipEMS.OverloadBatteryLack' is unreachable from the root entry path.", "policy_action": "budgeted_repair", "pyfcstm_severity": "warning", "rationale": "", "refs": {"state_path": "LNGShipEMS.OverloadBatteryLack"}, "suggested_fix_hints": [{"do_not": ["Do not add a self-loop to mask the unreachability."],...<truncated 491 chars>
    - local evidence 2: `scenario_regression` {"kind": "scenario_regression", "sim_feedback": {"n_scenarios": 8, "n_scenarios_passed": 7, "ok": false, "oracle_weak": false, "scenario_results": [{"description": "explicit-hot-start: from a concrete thermal leaf, PL=0 with SoC at 0.95 must target ZeroLoadSpare, catching wrong-target mutations of the zero-load full-SoC branch.", "name": "wrong_target_probe_thermal_to_zero_load_spare", "setup_error": null, "status": "pass", "step_results": [{"actual_state": "LNGShipEMS.ZeroLoadSpare", "actual_va...<truncated 8497 chars>
    - local evidence 3: `missing_required_grounding` {"element_ids": ["guard:RESCoversCharge", "guard:RESCoversSpare", "guard:OverloadBatteryLack"], "kind": "missing_required_grounding"}

</details>

<details><summary>Repair 8 / iteration `2` / source `SL-7` / accepted=✅</summary>

#### 为什么进入修复

- selected feedback source：`SL-7`；blocking=`True`；pre_scenario=`False`。
- problem_summary：model review failed
- diagnostic ids：`0, 1`。
- before_dsl_hash：`sha256:ad6bb952e971dcc754c511a5baf3833ec55994c5a265657833e894faa5829c16`；candidate_dsl_hash：`sha256:68ddc851c3efde1e421625c439cb0b4d3f522b929c9a90d9cd77dcf3cd76d501`。

#### 错误证据 / diagnostics

- 1. `<unknown>` `` policy=``：The illegal overload completion state is reachable and validated as normal behavior, contrary to the NL statement that it is illegal and shall never occur in practice.
- 2. `<unknown>` `` policy=``：Illegal-state semantics are not preserved: the DSL treats OverloadBatteryLack as an ordinary reachable EMS state.

#### SD-8 FixRequestBatch / 修改请求

- batch_id：`fixbatch-2-sha256-29c6b5ff10b`；source_stage=`SL-7`；legacy_plan_kind=`FixPlan`；requests=`2`。

| request_id | severity | hard | waiver | problem | evidence |
|---|---|---:|---:|---|---|
| `fixreq-2-sl7-0-e56a9044a1` | `review_fail` | ✅ | ❌ | model review failed | `{'category': 'unsafe_recovery', 'evidence': ['NL: "The overload completion state is illegal" and "the state shall never occur in practice."', 'DSL has state OverloadBatteryLack with operational during actions.', 'DSL includes transitions from all main states to OverloadBatteryLack under overload guards.', 'sim_summary includes a passing scenario that targets OverloadBatteryLack.'], 'severity': 'major', 'summary': 'The illegal overload completion state is reachable and validated as normal behavior, contrary to the NL statement that it is illegal and shall never occur in practice.'}` |
| `fixreq-2-sl7-1-ef61a52a60` | `review_fail` | ✅ | ❌ | model review failed | `{'category': 'nl_fidelity', 'evidence': ['OverloadBatteryLack has ordinary output assignments and command settings.', 'cmd_load_cut_in remains 1 and cmd_load_cut_out remains 0 in OverloadBatteryLack.', 'There is no explicit error, assertion, unreachable marker, or recovery separation for the illegal state.'], 'severity': 'major', 'summary': 'Illegal-state semantics are not preserved: the DSL treats OverloadBatteryLack as an ordinary reachable EMS state.'}` |

#### SD-8 legacy fix plan / 修改建议

- recommended_strategy：Use diagnostics as hints; choose the smallest globally consistent repair.；Before returning a candidate, verify every required_preserve_element_id still has a concrete DSL representation.
- forbidden_edits：`Do not delete grounded required elements merely to silence diagnostics., Do not invent internal plant/environment dynamics merely to make external input variables appear written.`。
- required_preserve_element_ids：`state:ZeroLoadCharge, state:ZeroLoadSpare, state:RESCoversCharge, state:RESCoversSpare, state:RESBatteryDischarge, state:LNGLowSoCChargeMargin, state:LNGCoversDeficit, state:LNGEng3LowSoCChargeMargin, state:LNGEng3CoversDeficit, state:LNGEng3DG1LowSoCChargeMargin, state:AllThermalWithinCapacity, state:OverloadBatteryLack, ... +18`。

#### SL-9 per-request 决策

- accepted_request_ids：`<derived-from-table>`；candidate_len=`14475`。

| request_id | decision | waiver | rework_locked | rationale / intent |
|---|---|---:|---:|---|
| `fixreq-2-sl7-0-e56a9044a1` | `accept` | ❌ | ✅ | Accepted. The SL-7 evidence is valid and the request is rework-locked. The smallest safe repair is not to remove the overload emergency branch, because FixLog/SL-10 shows that made OverloadBatteryLack unreachable and regressed wrong_target_probe_lng_to_overload_lack. Instead, the repair preserves concrete guarded inbound transitions to OverloadBatteryLack un...<truncated 471 chars> |
| `fixreq-2-sl7-1-ef61a52a60` | `accept` | ❌ | ✅ | Accepted. The illegal-state semantics were not explicit in the DSL. The repair adds a concrete marker variable and entry action for OverloadBatteryLack while preserving the NL-required all-thermal plus battery-lack dispatch action and the required load-service commands. This addresses the missing explicit illegal marker without repeating the prior rejected u...<truncated 223 chars> |
- repair_rationale：Both hard requests are accepted because the NL explicitly says OverloadBatteryLack is illegal/shall not occur in practice, while also requiring a concrete emergency dispatch behavior if extreme demand exceeds RES and all thermal resources.；The latest repair_memory was followed: the prior rejected 0aac candidate removed inbound transitions and caused W_UNREACHABLE_STATE plus scenario regression. This candidate restores/keeps concrete guarded inbound transitions to OverloadBatt...<truncated 64 chars>；Failed scenario wrong_target_probe_lng_to_overload_lack is repaired: from LNGCoversDeficit with PL=220, Ppv=10, Pw=10, SoC=0.5, batt_Pmax=100, LNG_Pmax=80, eng3_Pmax=30, DG1_Pmax=30, DG2_Pmax=20, the strengthened overload guard is true beca...<truncated 188 chars>；The overload path is still marked illegal/non-normal by the added overload_illegal variable and OverloadBatteryLack.enter action. This preserves the required emergency dispatch action while making the illegal semantics explicit rather than ...<truncated 50 chars>；guard:RESCoversCharge remains concretely represented by guarded normal transitions to RESCoversCharge with PL > 0 && Ppv + Pw >= PL && SoC < 0.95, and RESCoversCharge charges residual renewable power.
- diff_summary：`{"summary": "Added overload_illegal declaration and OverloadBatteryLack enter marker while preserving/restoring the strengthened concrete inbound overload guards, RES coverage guards, and the required OverloadBatteryLack dispatch action."}`。

#### SL-9 candidate / 最终修改执行方案

```pyfcstm
def float PL = 0.0;
def float Ppv = 0.0;
def float Pw = 0.0;
def float SoC = 0.5;
def float batt_Pmax = 0.0;
def float LNG_Pmax = 0.0;
def float eng3_Pmax = 0.0;
def float DG1_Pmax = 0.0;
def float DG2_Pmax = 0.0;
def float Pgmax = 0.0;
def float Pd1max = 0.0;
def float Pgen_req = 0.0;
def float Pbatt_discharge = 0.0;
def float Pbatt_charge = 0.0;
def float Pspare = 0.0;
def int cmd_LNG_cut_in = 0;
def int cmd_LNG_cut_out = 1;
def int cmd_eng3_cut_in = 0;
def int cmd_eng3_cut_out = 1;
def int cmd_DG1_cut_in = 0;
def int cmd_DG1_cut_out = 1;
def int cmd_DG2_cut_in = 0;
def int cmd_DG2_cut_out = 1;
def int cmd_load_cut_in = 1;
def int cmd_load_cut_out = 0;
def int overload_illegal = 0;

state LNGShipEMS {
    ! * -> ZeroLoadCharge : if [PL == 0 && Ppv + Pw > 0 && SoC < 0.95];
    ! * -> ZeroLoadSpare : if [PL == 0 && SoC >= 0.95];
    ! * -> RESBatteryDischarge : if [PL > 0 && Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw <= batt_Pmax];
    ! * -> LNGLowSoCChargeMargin : if [PL > 0 && Ppv + Pw < PL && SoC < 0.2 && PL - Ppv - Pw + Pgmax / 5 <= LNG_Pmax];
    ! * -> LNGCoversDeficit : if [PL > 0 && Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw > batt_Pmax && PL - Ppv - Pw <= LNG_Pmax];
    ! * -> LNGEng3LowSoCChargeMargin : if [PL > 0 && Ppv + Pw < PL && SoC < 0.2 && PL - Ppv - Pw + Pgmax / 5 > LNG_Pmax && PL - Ppv - Pw + Pd1max / 10 <= LNG_Pmax + eng3_Pmax];
    ! * -> LNGEng3CoversDeficit : if [PL > 0 && Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw > LNG_Pmax && PL - Ppv - Pw <= LNG_Pmax + eng3_Pmax];
    ! * -> LNGEng3DG1LowSoCChargeMargin : if [PL > 0 && Ppv + Pw < PL && SoC < 0.2 && PL - Ppv - Pw + Pd1max / 10 > LNG_Pmax + eng3_Pmax && PL - Ppv - Pw + Pd1max / 10 <= LNG_Pmax + eng3_Pmax + DG1_Pmax];
    ! * -> LNGEng3DG1CoversDeficit : if [PL > 0 && Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw > LNG_Pmax + eng3_Pmax && PL - Ppv - Pw <= LNG_Pmax + eng3_Pmax + DG1_Pmax];
    ! * -> AllThermalWithinCapacity : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > LNG_Pmax + eng3_Pmax + DG1_Pmax && PL - Ppv - Pw <= LNG_Pmax + eng3_Pmax + DG1_Pmax + DG2_Pmax];

    [*] -> ZeroLoadCharge;

    state ZeroLoadCharge {
        during {
            Pgen_req = 0.0;
            Pbatt_discharge = 0.0;
            Pbatt_charge = Ppv + Pw;
            Pspare = 0.0;
            cmd_LNG_cut_in = 0;
            cmd_LNG_cut_out = 1;
            cmd_eng3_cut_in = 0;
            cmd_eng3_cut_out = 1;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 0;
            cmd_load_cut_out = 1;
        }
    }

    state ZeroLoadSpare {
        during {
            Pgen_req = 0.0;
            Pbatt_discharge = 0.0;
            Pbatt_charge = 0.0;
            Pspare = Ppv + Pw;
            cmd_LNG_cut_in = 0;
            cmd_LNG_cut_out = 1;
            cmd_eng3_cut_in = 0;
            cmd_eng3_cut_out = 1;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 0;
            cmd_load_cut_out = 1;
        }
    }

    state RESCoversCharge {
        during {
            Pgen_req = 0.0;
            Pbatt_discharge = 0.0;
            Pbatt_charge = Ppv + Pw - PL;
            Pspare = 0.0;
            cmd_LNG_cut_in = 0;
            cmd_LNG_cut_out = 1;
            cmd_eng3_cut_in = 0;
            cmd_eng3_cut_out = 1;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state RESCoversSpare {
        during {
            Pgen_req = 0.0;
            Pbatt_discharge = 0.0;
            Pbatt_charge = 0.0;
            Pspare = Ppv + Pw - PL;
            cmd_LNG_cut_in = 0;
            cmd_LNG_cut_out = 1;
            cmd_eng3_cut_in = 0;
            cmd_eng3_cut_out = 1;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state RESBatteryDischarge {
        during {
            Pgen_req = 0.0;
            Pbatt_discharge = PL - Ppv - Pw;
            Pbatt_charge = 0.0;
            Pspare = 0.0;
            cmd_LNG_cut_in = 0;
            cmd_LNG_cut_out = 1;
            cmd_eng3_cut_in = 0;
            cmd_eng3_cut_out = 1;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state LNGLowSoCChargeMargin {
        during {
            Pgen_req = PL - Ppv - Pw + Pgmax / 5;
            Pbatt_discharge = 0.0;
            Pbatt_charge = Pgmax / 5;
            Pspare = 0.0;
            cmd_LNG_cut_in = 1;
            cmd_LNG_cut_out = 0;
            cmd_eng3_cut_in = 0;
            cmd_eng3_cut_out = 1;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state LNGCoversDeficit {
        during {
            Pgen_req = PL - Ppv - Pw;
            Pbatt_discharge = 0.0;
            Pbatt_charge = 0.0;
            Pspare = 0.0;
            cmd_LNG_cut_in = 1;
            cmd_LNG_cut_out = 0;
            cmd_eng3_cut_in = 0;
            cmd_eng3_cut_out = 1;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state LNGEng3LowSoCChargeMargin {
        during {
            Pgen_req = PL - Ppv - Pw + Pd1max / 10;
            Pbatt_discharge = 0.0;
            Pbatt_charge = Pd1max / 10;
            Pspare = 0.0;
            cmd_LNG_cut_in = 1;
            cmd_LNG_cut_out = 0;
            cmd_eng3_cut_in = 1;
            cmd_eng3_cut_out = 0;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state LNGEng3CoversDeficit {
        during {
            Pgen_req = PL - Ppv - Pw;
            Pbatt_discharge = 0.0;
            Pbatt_charge = 0.0;
            Pspare = 0.0;
            cmd_LNG_cut_in = 1;
            cmd_LNG_cut_out = 0;
            cmd_eng3_cut_in = 1;
            cmd_eng3_cut_out = 0;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state LNGEng3DG1LowSoCChargeMargin {
        during {
            Pgen_req = PL - Ppv - Pw + Pd1max / 10;
            Pbatt_discharge = 0.0;
            Pbatt_charge = Pd1max / 10;
            Pspare = 0.0;
            cmd_LNG_cut_in = 1;
            cmd_LNG_cut_out = 0;
            cmd_eng3_cut_in = 1;
            cmd_eng3_cut_out = 0;
            cmd_DG1_cut_in = 1;
            cmd_DG1_cut_out = 0;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state LNGEng3DG1CoversDeficit {
        during {
            Pgen_req = PL - Ppv - Pw;
            Pbatt_discharge = 0.0;
            Pbatt_charge = 0.0;
            Pspare = 0.0;
            cmd_LNG_cut_in = 1;
            cmd_LNG_cut_out = 0;
            cmd_eng3_cut_in = 1;
            cmd_eng3_cut_out = 0;
            cmd_DG1_cut_in = 1;
            cmd_DG1_cut_out = 0;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state AllThermalWithinCapacity {
        during {
            Pgen_req = PL - Ppv - Pw;
            Pbatt_discharge = 0.0;
            Pbatt_charge = 0.0;
            Pspare = 0.0;
            cmd_LNG_cut_in = 1;
            cmd_LNG_cut_out = 0;
            cmd_eng3_cut_in = 1;
            cmd_eng3_cut_out = 0;
            cmd_DG1_cut_in = 1;
            cmd_DG1_cut_out = 0;
            cmd_DG2_cut_in = 1;
            cmd_DG2_cut_out = 0;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state OverloadBatteryLack {
        enter { overload_illegal = 1; }
        during {
            Pgen_req = LNG_Pmax + eng3_Pmax + DG1_Pmax + DG2_Pmax;
            Pbatt_discharge = PL - Ppv - Pw - LNG_Pmax - eng3_Pmax - DG1_Pmax - DG2_Pmax;
            Pbatt_charge = 0.0;
            Pspare = 0.0;
            cmd_LNG_cut_in = 1;
            cmd_LNG_cut_out = 0;
            cmd_eng3_cut_in = 1;
            cmd_eng3_cut_out = 0;
            cmd_DG1_cut_in = 1;
            cmd_DG1_cut_out = 0;
            cmd_DG2
... <truncated 5475 chars; see run record>
```

#### Candidate diff（before -> candidate）

```diff
--- before.fcstm
+++ candidate.fcstm
@@ -23,6 +23,7 @@
 def int cmd_DG2_cut_out = 1;
 def int cmd_load_cut_in = 1;
 def int cmd_load_cut_out = 0;
+def int overload_illegal = 0;
 
 state LNGShipEMS {
     ! * -> ZeroLoadCharge : if [PL == 0 && Ppv + Pw > 0 && SoC < 0.95];
@@ -267,6 +268,7 @@
     }
 
     state OverloadBatteryLack {
+        enter { overload_illegal = 1; }
         during {
             Pgen_req = LNG_Pmax + eng3_Pmax + DG1_Pmax + DG2_Pmax;
             Pbatt_discharge = PL - Ppv - Pw - LNG_Pmax - eng3_Pmax - DG1_Pmax - DG2_Pmax;
```

#### SL-10 审查结果

- SL-10 decision=`pass`，ok=`True`，target_resolved=`True`，regression_detected=`False`，drift_risk=`minor`。
- SL-10 review_meta：schema=`SL10RepairReviewOutput.v1`，failure_policy=`fail_closed`，replay_key=`SL-10:sha256:d5d5532ef4c54de622550014bd7d06e2c543cac6e4c0f7de0ab3a2f2e4d29db5`。
  - SL-10 evidence 1: `{"summary": "The candidate resolves the current hard SL-7/SL-9 targets by adding an explicit illegal-state marker, `def int overload_illegal = 0`, and `OverloadBatteryLack.enter { overload_illegal = 1; }`, while preserving the NL-required emergency overload dispatch. This addresses the review finding that OverloadBatteryLack previously looked like an unmarked ordinary EMS completion state."}`
  - SL-10 evidence 2: `{"summary": "The candidate follows the complete FixLog and latest repair_memory. The prior rejected 0aac candidate removed normal inbound transitions to OverloadBatteryLack, caused W_UNREACHABLE_STATE, and regressed scenario `wrong_target_probe_lng_to_overload_lack`. The current candidate restores the concrete inbound overload transitions from all dispatch states, including `LNGCoversDeficit -> OverloadBatteryLack`, under the strengthened condition requiring PL > 0, RES below load, demand above all thermal capacity, SoC >= 0.2, and residual lack <= batt_Pmax."}`
  - SL-10 evidence 3: `{"summary": "The candidate preserves `action:OverloadBatteryLackDispatch`: Pgen_req is set to LNG_Pmax + eng3_Pmax + DG1_Pmax + DG2_Pmax, Pbatt_discharge is the residual lack, Pbatt_charge = 0, Pspare = 0, all LNG/eng3/DG1/DG2 cut-in commands are enabled, and cmd_load_cut_in = 1 / cmd_load_cut_out = 0. This maintains the NL obligation that extreme demand activates all thermal units and covers the lack by battery discharge, while the added marker makes the state illegal/non-normal."}`
  - SL-10 evidence 4: `{"summary": "The local deterministic evidence no longer reports the previous scenario regression or unreachable-state diagnostic. Its only current rejection is `missing_required_grounding` for `guard:RESCoversCharge`, `guard:RESCoversSpare`, and `guard:OverloadBatteryLack`. The DSL text contains concrete guarded transitions for all three guard classes: RES charge under `PL > 0 && Ppv + Pw >= PL && SoC < 0.95`, RES spare under `PL > 0 && Ppv + Pw >= PL && SoC >= 0.95`, and overload under the strengthened battery-suitable overload condition."}`
  - SL-10 evidence 5: `{"summary": "No NL-required states, variables, or actions are dropped. The twelve operating states from the grounding map remain, including RES coverage states, low-SoC charge-margin states, LNG/eng3/DG1/DG2 priority states, AllThermalWithinCapacity, and OverloadBatteryLack. Required inputs and outputs, including PL, Ppv, Pw, SoC, eng3_Pmax, Pgmax, Pd1max, Pgen_req, Pbatt_discharge, Pbatt_charge, Pspare, and generator/load command flags, remain present."}`
- local checks evidence：stage=`SD-10`；note=PR-E1 uses local parse/semantic/design/sim checks as SL-10 evidence, not as the final deterministic judge.。
  - local ok=`False`，target_resolved=`False`，regression_detected=`False`，drift_risk=`major`。
  - local_rejection：reason=`missing_required_grounding`，rejected_by_stage=`SD-10`。
    - local evidence 1: `missing_required_grounding` {"element_ids": ["guard:RESCoversCharge", "guard:RESCoversSpare", "guard:OverloadBatteryLack"], "kind": "missing_required_grounding"}

</details>


#### FixLog ledger

口径：FixLog 是跨 iteration 的 append-only repair 台账，记录 request batch、SL-9 accept/reject、diff/local evidence、SL-10 批示和下一步动作。

| # | iteration | phase | batch | decisions | next_action | candidate | notes |
|---:|---:|---|---|---|---|---|---|
| 1 | `0` | `request_batch` | `fixbatch-0-sha256-081cf0a961f` | accept=0, reject=0 | `sl9_decision_and_repair` | `<none>` | SD-8 produced FixRequestBatch; deterministic stage does not decide final repair. |
| 2 | `0` | `sl9_decision` | `fixbatch-0-sha256-081cf0a961f` | accept=1, reject=0 | `sl10_review` | `sha256:c4422351d34de68230c5a6f4f43ae04421c7e963fa641dd7ca3c3377d63d966a` | Accepted the single hard SL-7 model-review request because the overload branch was NL-grounded but unsafe as an ordinary dispatch/recovery state., Preserved all twelve required states, including OverloadBatteryLack, and preserved required variables, RES guard branches, the overload guard, and the overload dispatch action that activates all thermal units and computes battery lack discharge., The OverloadBatteryLack guard now additionally requires SoC >= 0.2 and the residual lack after all thermal resources to be within batt_Pmax, resolving the evidence that battery discharge was unbounded and not suitability-guarded., ... +2 |
| 3 | `0` | `sl10_review` | `fixbatch-0-sha256-081cf0a961f` | accept=1, reject=0 | `sl9_rework` | `sha256:c4422351d34de68230c5a6f4f43ae04421c7e963fa641dd7ca3c3377d63d966a` | SL-10 pass was downgraded because local deterministic evidence reported major drift and SL-10 evidence did not explicitly address the local rejection reason/kind with a structured local_override_rationale., For the next SL-9 repair, do not blindly regenerate the same DSL. Either change the candidate so the local major-drift evidence is resolved, or keep the minimal DSL only with explicit repair_rationale mapping each local objection (for example missing_required_grounding, scenario_regression, count_drift, or forced_transition_count_drift) to concrete NL-grounded states/transitions/actions that remain in the candidate. This rationale is required so SL-10 can produce local_override_rationale instead of cycling., repair_memory:SL-10 pass was downgraded because local deterministic evidence reported major drift and SL-10 evidence did not explicitly address the local rejection reason/kind with a structured local_override_rationale., ... +8 |
| 4 | `0` | `sl9_rework_decision` | `fixbatch-0-sha256-081cf0a961f` | accept=1, reject=0 | `sl10_review` | `sha256:a3d167d8c7d32fd212b403f7d77af2d6db6d5c6d03fe6f1bbf42cc671ee351be` | Primary failing scenario addressed: overload_activates_all_thermal_and_battery_lack, step overload_battery_lack_above_total_capacity. Expected state LNGShipEMS.OverloadBatteryLack matched the prior actual state, and expected Pgen_req = 160.0, Pbatt_discharge = 40.0, Pbatt_charge = 0.0, Pspare = 0.0, and all generator cut-in commands already matched. The only mismatch was cmd_load_cut_in expected 1 vs actual 0 and cmd_load_cut_out expected 0 vs actual 1; this candidate restores the OverloadBatteryLack load commands to 1/0., The SL-7 unsafe_recovery target is still repaired by making the OverloadBatteryLack guard require SoC >= 0.2 and the residual lack after LNG, eng3, DG1, and DG2 to be <= batt_Pmax. Thus the overload battery discharge action remains NL-grounded but is no longer unbounded or entered without battery suitability/capacity checks., This is not the previously rejected candidate hash in substance: the previous candidate changed both the overload guard and the overload load commands, causing the local scenario regression. This candidate keeps the guard-safety repair but restores the scenario-required load commands., ... +5 |
| 5 | `0` | `sl10_rework_review` | `fixbatch-0-sha256-081cf0a961f` | accept=1, reject=0 | `sl9_rework` | `sha256:a3d167d8c7d32fd212b403f7d77af2d6db6d5c6d03fe6f1bbf42cc671ee351be` | SL-10 pass was downgraded because local deterministic evidence reported major drift and SL-10 evidence did not explicitly address the local rejection reason/kind with a structured local_override_rationale., For the next SL-9 repair, do not blindly regenerate the same DSL. Either change the candidate so the local major-drift evidence is resolved, or keep the minimal DSL only with explicit repair_rationale mapping each local objection (for example missing_required_grounding, scenario_regression, count_drift, or forced_transition_count_drift) to concrete NL-grounded states/transitions/actions that remain in the candidate. This rationale is required so SL-10 can produce local_override_rationale instead of cycling., repair_memory:SL-10 pass was downgraded because local deterministic evidence reported major drift and SL-10 evidence did not explicitly address the local rejection reason/kind with a structured local_override_rationale., ... +9 |
| 6 | `0` | `sl9_rework_decision` | `fixbatch-0-sha256-081cf0a961f` | accept=1, reject=0 | `sl10_review` | `sha256:fa9a662af2c91e5cca5f3f32570c28a50c1745f2db60dc535a9ee953a9402ac3` | Primary SL-7 unsafe_recovery gap: original OverloadBatteryLack entered whenever PL - Ppv - Pw exceeded LNG_Pmax + eng3_Pmax + DG1_Pmax + DG2_Pmax and then computed Pbatt_discharge without checking SoC or batt_Pmax. The repaired forced guard now additionally requires SoC >= 0.2 and residual lack after all thermal resources <= batt_Pmax., Scenario regression brief: in overload_activates_all_thermal_and_battery_lack, step overload_battery_lack_above_total_capacity, the expected and actual state were both LNGShipEMS.OverloadBatteryLack; Pgen_req = 160.0, Pbatt_discharge = 40.0, Pbatt_charge = 0.0, Pspare = 0.0, and all generator cut-in commands matched. The prior regression was cmd_load_cut_in expected 1 vs actual 0 and cmd_load_cut_out expected 0 vs actual 1. This candidate preserves cmd_load_cut_in = 1 and cmd_load_cut_out = 0 in OverloadBatteryLack., Missing grounding mapping: guard:RESCoversCharge is represented twice concretely: the wildcard forced transition to RESCoversCharge with guard PL > 0 && Ppv + Pw >= PL && SoC < 0.95, and the added local guarded self-transition with the same condition. Its state action charges residual renewable power through Pbatt_charge = Ppv + Pw - PL., ... +4 |
| 7 | `0` | `sl10_rework_review` | `fixbatch-0-sha256-081cf0a961f` | accept=1, reject=0 | `sl9_rework` | `sha256:fa9a662af2c91e5cca5f3f32570c28a50c1745f2db60dc535a9ee953a9402ac3` | SL-10 pass was downgraded because local deterministic evidence reported major drift and SL-10 evidence did not explicitly address the local rejection reason/kind with a structured local_override_rationale., For the next SL-9 repair, do not blindly regenerate the same DSL. Either change the candidate so the local major-drift evidence is resolved, or keep the minimal DSL only with explicit repair_rationale mapping each local objection (for example missing_required_grounding, scenario_regression, count_drift, or forced_transition_count_drift) to concrete NL-grounded states/transitions/actions that remain in the candidate. This rationale is required so SL-10 can produce local_override_rationale instead of cycling., repair_memory:SL-10 pass was downgraded because local deterministic evidence reported major drift and SL-10 evidence did not explicitly address the local rejection reason/kind with a structured local_override_rationale., ... +10 |
| 8 | `0` | `sl9_rework_decision` | `fixbatch-0-sha256-081cf0a961f` | accept=1, reject=0 | `sl10_review` | `sha256:a3d167d8c7d32fd212b403f7d77af2d6db6d5c6d03fe6f1bbf42cc671ee351be` | Primary SL-7 repair: OverloadBatteryLack is still the NL-required branch for extreme demand above RES plus all thermal resources, but its forced guard now also requires SoC >= 0.2 and residual lack after all thermal capacity <= batt_Pmax. This resolves the unsafe unbounded/unsuitable battery discharge evidence without deleting the overload state or action., Scenario regression repair: for overload_activates_all_thermal_and_battery_lack, the expected and actual state were already LNGShipEMS.OverloadBatteryLack and the power outputs/generator cut-ins matched. The previously rejected c442 candidate only failed because it changed cmd_load_cut_in to 0 and cmd_load_cut_out to 1. This candidate preserves cmd_load_cut_in = 1 and cmd_load_cut_out = 0, matching the scenario and NL overload-dispatch obligation., Latest local design objection repair: the prior fa9a candidate added normal guarded self-transitions for RESCoversCharge, RESCoversSpare, and OverloadBatteryLack, which created W_FORCED_OVERRIDES_NORMAL because each self-transition duplicated an expanded wildcard forced transition. Those self-transitions are intentionally removed here; no forced/normal duplicate self-transition remains., ... +6 |
| 9 | `0` | `sl10_rework_review` | `fixbatch-0-sha256-081cf0a961f` | accept=1, reject=0 | `sl9_rework` | `sha256:a3d167d8c7d32fd212b403f7d77af2d6db6d5c6d03fe6f1bbf42cc671ee351be` | SL-10 pass was downgraded because local deterministic evidence reported major drift and SL-10 evidence did not explicitly address the local rejection reason/kind with a structured local_override_rationale., For the next SL-9 repair, do not blindly regenerate the same DSL. Either change the candidate so the local major-drift evidence is resolved, or keep the minimal DSL only with explicit repair_rationale mapping each local objection (for example missing_required_grounding, scenario_regression, count_drift, or forced_transition_count_drift) to concrete NL-grounded states/transitions/actions that remain in the candidate. This rationale is required so SL-10 can produce local_override_rationale instead of cycling., repair_memory:SL-10 pass was downgraded because local deterministic evidence reported major drift and SL-10 evidence did not explicitly address the local rejection reason/kind with a structured local_override_rationale., ... +11 |
| 10 | `0` | `sl9_rework_decision` | `fixbatch-0-sha256-081cf0a961f` | accept=1, reject=0 | `sl10_review` | `sha256:813b635ee38132f66b9e8cd1fbf754f73d5598598eca4acef2ded16fddad4376` | Primary SL-7 unsafe_recovery repair: OverloadBatteryLack is no longer selected solely because demand exceeds RES plus all thermal capacity. Its concrete guard now also requires SoC >= 0.2 and residual lack after LNG, eng3, DG1, and DG2 to be <= batt_Pmax, so the battery discharge action is suitable and capacity-bounded., Scenario regression repair: the prior c442 candidate failed overload_activates_all_thermal_and_battery_lack because expected cmd_load_cut_in = 1 and cmd_load_cut_out = 0 but actual values were 0 and 1. This candidate preserves cmd_load_cut_in = 1 and cmd_load_cut_out = 0 in OverloadBatteryLack, while retaining Pgen_req as total thermal capacity and Pbatt_discharge as the residual lack., Missing grounding repair for guard:RESCoversCharge: the guard PL > 0 && Ppv + Pw >= PL && SoC < 0.95 is now represented by explicit normal guarded transitions from every concrete state to RESCoversCharge; the state action remains Pbatt_charge = Ppv + Pw - PL., ... +5 |
| 11 | `0` | `sl10_rework_review` | `fixbatch-0-sha256-081cf0a961f` | accept=1, reject=0 | `sc11_accept_then_sd2` | `sha256:813b635ee38132f66b9e8cd1fbf754f73d5598598eca4acef2ded16fddad4376` | repair_memory:sl10_evidence, repair_memory:sl10_evidence, repair_memory:sl10_evidence, ... +6 |
| 12 | `1` | `request_batch` | `fixbatch-1-sha256-00855f2776f` | accept=0, reject=0 | `sl9_decision_and_repair` | `<none>` | SD-8 produced FixRequestBatch; deterministic stage does not decide final repair. |
| 13 | `1` | `sl9_decision` | `fixbatch-1-sha256-00855f2776f` | accept=3, reject=0 | `sl10_review` | `sha256:ad6bb952e971dcc754c511a5baf3833ec55994c5a265657833e894faa5829c16` | Thermal priority repair: LNGEng3DG1CoversDeficit is added for the suitable-SoC range where LNG plus eng3 plus DG1 can satisfy the deficit. Its action cuts in LNG, eng3, and DG1 while keeping DG2 cut out, so DG2 is no longer used prematurely., AllThermalWithinCapacity is narrowed to deficits greater than LNG_Pmax + eng3_Pmax + DG1_Pmax and within LNG_Pmax + eng3_Pmax + DG1_Pmax + DG2_Pmax, so DG2 is reserved for the final thermal-capacity priority tier., Unsafe overload repair is preserved: every OverloadBatteryLack normal guard requires demand above total thermal capacity, SoC >= 0.2, and residual lack <= batt_Pmax. This prevents unbounded or low-SoC battery-discharge entry while preserving the NL-required all-thermal plus battery-lack dispatch for the coverable emergency case., ... +4 |
| 14 | `1` | `sl10_review` | `fixbatch-1-sha256-00855f2776f` | accept=3, reject=0 | `sc11_accept_then_sd2` | `sha256:ad6bb952e971dcc754c511a5baf3833ec55994c5a265657833e894faa5829c16` | repair_memory:sl10_evidence, repair_memory:sl10_evidence, repair_memory:sl10_evidence, ... +10 |
| 15 | `2` | `request_batch` | `fixbatch-2-sha256-29c6b5ff10b` | accept=0, reject=0 | `sl9_decision_and_repair` | `<none>` | SD-8 produced FixRequestBatch; deterministic stage does not decide final repair. |
| 16 | `2` | `sl9_decision` | `fixbatch-2-sha256-29c6b5ff10b` | accept=2, reject=0 | `sl10_review` | `sha256:0aac73439d9e4fa4e943fc2d2cead8b9851b5b7084ee281ee912e5eb12f35388` | Both current hard requests are accepted because the SL-7 evidence identifies a real NL-fidelity gap: OverloadBatteryLack was treated as a normal reachable dispatch state even though the NL calls the overload completion state illegal and says it shall never occur in practice., Smallest safe edit: remove all ordinary incoming transitions from concrete EMS dispatch states to OverloadBatteryLack. This directly addresses the evidence item that the DSL included transitions from all main states to the illegal state., Preservation: state:OverloadBatteryLack and action:OverloadBatteryLackDispatch are not deleted. The state still contains the all-thermal cut-in, total thermal Pgen_req, residual Pbatt_discharge, Pbatt_charge = 0, Pspare = 0, and load-service command assignments required by prior grounding and prior scenario-regression evidence., ... +5 |
| 17 | `2` | `sl10_review` | `fixbatch-2-sha256-29c6b5ff10b` | accept=2, reject=0 | `sl9_rework` | `sha256:0aac73439d9e4fa4e943fc2d2cead8b9851b5b7084ee281ee912e5eb12f35388` | Restore concrete guarded inbound transitions from normal dispatch states to OverloadBatteryLack for the strengthened overload condition: PL > 0, Ppv + Pw < PL, PL - Ppv - Pw > LNG_Pmax + eng3_Pmax + DG1_Pmax + DG2_Pmax, SoC >= 0.2, and residual lack <= batt_Pmax. Do not rely on an OverloadBatteryLack self-loop to ground this guard., Keep overload_illegal as an explicit illegal-state marker, but make it coexist with the required emergency dispatch path. OverloadBatteryLack.enter may set overload_illegal = 1, and/or the restored inbound transitions may set overload_illegal = 1 in an effect block if the DSL supports effects., Preserve action:OverloadBatteryLackDispatch exactly for the scenario/NL emergency branch: Pgen_req = LNG_Pmax + eng3_Pmax + DG1_Pmax + DG2_Pmax; Pbatt_discharge = PL - Ppv - Pw - LNG_Pmax - eng3_Pmax - DG1_Pmax - DG2_Pmax; Pbatt_charge = 0; Pspare = 0; all LNG/eng3/DG1/DG2 cut-in commands enabled; cmd_load_cut_in = 1 and cmd_load_cut_out = 0., ... +23 |
| 18 | `2` | `sl9_rework_decision` | `fixbatch-2-sha256-29c6b5ff10b` | accept=2, reject=0 | `sl10_review` | `sha256:68ddc851c3efde1e421625c439cb0b4d3f522b929c9a90d9cd77dcf3cd76d501` | Both hard requests are accepted because the NL explicitly says OverloadBatteryLack is illegal/shall not occur in practice, while also requiring a concrete emergency dispatch behavior if extreme demand exceeds RES and all thermal resources., The latest repair_memory was followed: the prior rejected 0aac candidate removed inbound transitions and caused W_UNREACHABLE_STATE plus scenario regression. This candidate restores/keeps concrete guarded inbound transitions to OverloadBatteryLack from normal dispatch states, including LNGCoversDeficit., Failed scenario wrong_target_probe_lng_to_overload_lack is repaired: from LNGCoversDeficit with PL=220, Ppv=10, Pw=10, SoC=0.5, batt_Pmax=100, LNG_Pmax=80, eng3_Pmax=30, DG1_Pmax=30, DG2_Pmax=20, the strengthened overload guard is true because residual lack is 40 and <= batt_Pmax, so the step reaches OverloadBatteryLack and its during action yields Pgen_req=160 and Pbatt_discharge=40 with all thermal cut-in commands enabled., ... +6 |
| 19 | `2` | `sl10_rework_review` | `fixbatch-2-sha256-29c6b5ff10b` | accept=2, reject=0 | `sc11_accept_then_sd2` | `sha256:68ddc851c3efde1e421625c439cb0b4d3f522b929c9a90d9cd77dcf3cd76d501` | repair_memory:sl10_evidence, repair_memory:sl10_evidence, repair_memory:sl10_evidence, ... +6 |

### 8. 尝试记录与成本

- `SL-1`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 6034, 'completion_chars': 19660, 'completion_tokens': 7849, 'elapsed_seconds': 144.20197636100056, 'estimated_completion_tokens': 4915, 'estimated_prompt_tokens': 6646, 'estimated_total_tokens': 11561, 'first_chunk_seconds': 37.71874422200199, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 26582, 'prompt_tokens': 6469, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 14318}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 2940, 'completion_chars': 8746, 'completion_tokens': 4440, 'elapsed_seconds': 82.52503877600248, 'estimated_completion_tokens': 2187, 'estimated_prompt_tokens': 15294, 'estimated_total_tokens': 17481, 'first_chunk_seconds': 29.525380576000316, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 61173, 'prompt_tokens': 16395, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 20835}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 4436, 'completion_chars': 14391, 'completion_tokens': 4823, 'elapsed_seconds': 89.75620464800159, 'estimated_completion_tokens': 3598, 'estimated_prompt_tokens': 18747, 'estimated_total_tokens': 22345, 'first_chunk_seconds': 10.626282922006794, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 74986, 'prompt_tokens': 20568, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 25391}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 5253, 'completion_chars': 17035, 'completion_tokens': 5772, 'elapsed_seconds': 106.2840038669965, 'estimated_completion_tokens': 4259, 'estimated_prompt_tokens': 19056, 'estimated_total_tokens': 23315, 'first_chunk_seconds': 12.186040100001264, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 76223, 'prompt_tokens': 20950, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 26722}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-7`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 2212, 'completion_chars': 9520, 'completion_tokens': 3249, 'elapsed_seconds': 61.95522297199932, 'estimated_completion_tokens': 2380, 'estimated_prompt_tokens': 59173, 'estimated_total_tokens': 61553, 'first_chunk_seconds': 22.352824656001758, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 236690, 'prompt_tokens': 68190, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 71439}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-9`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 3675, 'completion_chars': 11322, 'completion_tokens': 4194, 'elapsed_seconds': 77.96097745200677, 'estimated_completion_tokens': 2831, 'estimated_prompt_tokens': 22131, 'estimated_total_tokens': 24962, 'first_chunk_seconds': 13.374315641005524, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 88523, 'prompt_tokens': 23399, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 27593}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-10`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 889, 'completion_chars': 4003, 'completion_tokens': 1408, 'elapsed_seconds': 27.797078966003028, 'estimated_completion_tokens': 1001, 'estimated_prompt_tokens': 33379, 'estimated_total_tokens': 34380, 'first_chunk_seconds': 11.841624986001989, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 133514, 'prompt_tokens': 36048, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 37456}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-9`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 4076, 'completion_chars': 12919, 'completion_tokens': 4327, 'elapsed_seconds': 81.75838585299789, 'estimated_completion_tokens': 3230, 'estimated_prompt_tokens': 74338, 'estimated_total_tokens': 77568, 'first_chunk_seconds': 8.103534027002752, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 297352, 'prompt_tokens': 65434, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 69761}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-10`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1057, 'completion_chars': 4507, 'completion_tokens': 1854, 'elapsed_seconds': 37.212924839986954, 'estimated_completion_tokens': 1127, 'estimated_prompt_tokens': 127629, 'estimated_total_tokens': 128756, 'first_chunk_seconds': 19.48519117498654, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 510516, 'prompt_tokens': 116732, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 118586}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-9`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 4375, 'completion_chars': 13927, 'completion_tokens': 5315, 'elapsed_seconds': 98.83744705200661, 'estimated_completion_tokens': 3482, 'estimated_prompt_tokens': 77775, 'estimated_total_tokens': 81257, 'first_chunk_seconds': 22.004061622006702, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 311097, 'prompt_tokens': 69068, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 74383}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-10`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1270, 'completion_chars': 5905, 'completion_tokens': 2231, 'elapsed_seconds': 42.784635914998944, 'estimated_completion_tokens': 1477, 'estimated_prompt_tokens': 31931, 'estimated_total_tokens': 33408, 'first_chunk_seconds': 21.338460417988244, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 127721, 'prompt_tokens': 31391, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 33622}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-9`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 4234, 'completion_chars': 13878, 'completion_tokens': 5915, 'elapsed_seconds': 109.88422764200368, 'estimated_completion_tokens': 3470, 'estimated_prompt_tokens': 55741, 'estimated_total_tokens': 59211, 'first_chunk_seconds': 36.20560360100353, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 222964, 'prompt_tokens': 49772, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 55687}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-10`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1217, 'completion_chars': 5226, 'completion_tokens': 1736, 'elapsed_seconds': 33.71212828499847, 'estimated_completion_tokens': 1307, 'estimated_prompt_tokens': 39606, 'estimated_total_tokens': 40913, 'first_chunk_seconds': 12.157604866995825, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 158424, 'prompt_tokens': 37328, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 39064}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-9`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 6025, 'completion_chars': 18098, 'completion_tokens': 6906, 'elapsed_seconds': 127.4673887520039, 'estimated_completion_tokens': 4525, 'estimated_prompt_tokens': 56361, 'estimated_total_tokens': 60886, 'first_chunk_seconds': 20.57960187799472, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 225442, 'prompt_tokens': 51253, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 58159}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-10`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1136, 'completion_chars': 5353, 'completion_tokens': 1655, 'elapsed_seconds': 32.275823862000834, 'estimated_completion_tokens': 1339, 'estimated_prompt_tokens': 44574, 'estimated_total_tokens': 45913, 'first_chunk_seconds': 12.31007142100134, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 178293, 'prompt_tokens': 42595, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 44250}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 6382, 'completion_chars': 20753, 'completion_tokens': 6781, 'elapsed_seconds': 124.90989689801063, 'estimated_completion_tokens': 5189, 'estimated_prompt_tokens': 25169, 'estimated_total_tokens': 30358, 'first_chunk_seconds': 9.940885412011994, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 100673, 'prompt_tokens': 27735, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 34516}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 5250, 'completion_chars': 15690, 'completion_tokens': 5621, 'elapsed_seconds': 105.17894840201188, 'estimated_completion_tokens': 3923, 'estimated_prompt_tokens': 26098, 'estimated_total_tokens': 30021, 'first_chunk_seconds': 10.707727695000358, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 104391, 'prompt_tokens': 28864, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 34485}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-7`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 2334, 'completion_chars': 10098, 'completion_tokens': 3371, 'elapsed_seconds': 66.89931456900376, 'estimated_completion_tokens': 2525, 'estimated_prompt_tokens': 65745, 'estimated_total_tokens': 68270, 'first_chunk_seconds': 23.154317220003577, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 262977, 'prompt_tokens': 75948, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 79319}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-9`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 6553, 'completion_chars': 19438, 'completion_tokens': 8108, 'elapsed_seconds': 151.7917189909931, 'estimated_completion_tokens': 4860, 'estimated_prompt_tokens': 39535, 'estimated_total_tokens': 44395, 'first_chunk_seconds': 33.956181400993955, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 158139, 'prompt_tokens': 38159, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 46267}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-10`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1568, 'completion_chars': 7075, 'completion_tokens': 2605, 'elapsed_seconds': 50.15339380101068, 'estimated_completion_tokens': 1769, 'estimated_prompt_tokens': 33999, 'estimated_total_tokens': 35768, 'first_chunk_seconds': 24.11814887500077, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 135993, 'prompt_tokens': 34234, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 36839}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`1`，schema_ok=`True`，usage=`{'chunk_count': 8490, 'completion_chars': 27601, 'completion_tokens': 8994, 'elapsed_seconds': 164.21511394999106, 'estimated_completion_tokens': 6901, 'estimated_prompt_tokens': 29732, 'estimated_total_tokens': 36633, 'first_chunk_seconds': 13.87508365100075, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 118928, 'prompt_tokens': 32841, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 41835}`，attempts=`2`。
  - attempt 0: error_kind=`provider_error`，model=`gpt-5.5`。
  - attempt 1: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 3389, 'completion_chars': 10533, 'completion_tokens': 4752, 'elapsed_seconds': 88.60857203799242, 'estimated_completion_tokens': 2634, 'estimated_prompt_tokens': 30765, 'estimated_total_tokens': 33399, 'first_chunk_seconds': 31.3158702130022, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 123059, 'prompt_tokens': 34125, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 38877}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-7`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1736, 'completion_chars': 8014, 'completion_tokens': 3291, 'elapsed_seconds': 63.053251641002134, 'estimated_completion_tokens': 2004, 'estimated_prompt_tokens': 72104, 'estimated_total_tokens': 74108, 'first_chunk_seconds': 32.313256648005336, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 288413, 'prompt_tokens': 83504, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 86795}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-9`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 5414, 'completion_chars': 17046, 'completion_tokens': 6963, 'elapsed_seconds': 128.06108672599657, 'estimated_completion_tokens': 4262, 'estimated_prompt_tokens': 34117, 'estimated_total_tokens': 38379, 'first_chunk_seconds': 31.885456638992764, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 136467, 'prompt_tokens': 34085, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 41048}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-10`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1156, 'completion_chars': 4662, 'completion_tokens': 2028, 'elapsed_seconds': 39.935350806001225, 'estimated_completion_tokens': 1166, 'estimated_prompt_tokens': 29010, 'estimated_total_tokens': 30176, 'first_chunk_seconds': 20.406283984993934, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 116040, 'prompt_tokens': 30398, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 32426}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-9`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 6544, 'completion_chars': 19449, 'completion_tokens': 8008, 'elapsed_seconds': 147.38654031400802, 'estimated_completion_tokens': 4863, 'estimated_prompt_tokens': 64722, 'estimated_total_tokens': 69585, 'first_chunk_seconds': 31.018435386009514, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 258888, 'prompt_tokens': 62004, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 70012}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-10`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1090, 'completion_chars': 4570, 'completion_tokens': 1565, 'elapsed_seconds': 30.90969413598941, 'estimated_completion_tokens': 1143, 'estimated_prompt_tokens': 41816, 'estimated_total_tokens': 42959, 'first_chunk_seconds': 11.25861992398859, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 167262, 'prompt_tokens': 43212, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 44777}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 4981, 'completion_chars': 15686, 'completion_tokens': 5831, 'elapsed_seconds': 109.5300425789901, 'estimated_completion_tokens': 3922, 'estimated_prompt_tokens': 26343, 'estimated_total_tokens': 30265, 'first_chunk_seconds': 20.364415433999966, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 105372, 'prompt_tokens': 29139, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 34970}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 5812, 'completion_chars': 18419, 'completion_tokens': 6167, 'elapsed_seconds': 114.18346094300796, 'estimated_completion_tokens': 4605, 'estimated_prompt_tokens': 27607, 'estimated_total_tokens': 32212, 'first_chunk_seconds': 9.71695251800702, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 110426, 'prompt_tokens': 30707, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 36874}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-7`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1525, 'completion_chars': 7459, 'completion_tokens': 3226, 'elapsed_seconds': 61.53880252499948, 'estimated_completion_tokens': 1865, 'estimated_prompt_tokens': 73817, 'estimated_total_tokens': 75682, 'first_chunk_seconds': 34.105476010998245, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 295265, 'prompt_tokens': 85722, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 88948}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。

### 9. 最终停止状态与后续含义

- 停止状态：verdict=`success`，record_status=`success`。
- 主要原因分类：`success_but_weak_oracle_ineligible`。
- required stages executed：`71/16`，missing=`<none>`。
- repairs：`3/8` accepted；scenario_history=`12`。
- 配置含义：`recommended baseline candidate`；该结果可用于评估默认入口本身。
- 主结果/蓝本边界：`main_result_eligible` 只表示该 run 非 provider-invalid 且 trace/schema/secret/final-verdict 口径可进入主结果候选；`path2_ref_model_blueprint_eligible=false` 时，模型仍可作为 FE/BVS 或 dispatch-classifier 压力测试证据，但不得称为 Path2 ref-model 主蓝本。
- 样本含义：若出现 `design_or_variable_dynamics`，应重点审查变量是否仅作为 guard/input 常量而没有事件/动作更新；若出现 pre-scenario parse/semantic 失败，则应先优化 pyfcstm grammar adherence。
