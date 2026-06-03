## path2 / state-transitions-logical-design-for-hybrid-energy-generation-with-renewable-energy-sources-in-lng-ship / default 真实运行结果：Path2 LNG-ship EMS representative NL

### 0. 准确边界与结论

- 运行入口：`method.loop.run_agent_loop(nl, LoopConfig(...))`。
- 是否使用 fake / fixture / hot-start / replay：否；本次使用真实默认入口/显式 PR-E1 探索条件，没有 fake、fixture、hot-start 或 replay。
- final verdict：`not_converged`；record_status：`budget_exhausted`；result_status：`not_converged`。
- main_result_eligible：`false`。
- 一句话结论：`budget`；停止原因：SC-11 budget gate blocked SD-2 revalidation: iter+1=5 >= max_iterations=5。

### 1. 基本信息

| 字段 | 值 |
|---|---|
| Path | `path2` |
| case_id | `state-transitions-logical-design-for-hybrid-energy-generation-with-renewable-energy-sources-in-lng-ship` |
| config_id | `default` |
| 运行入口 | `method.loop.run_agent_loop(nl, LoopConfig(...))` |
| LoopConfig 摘要 | `condition_id=full_staged_v1`, `max_iterations=5`, `llm_max_retries=2`, `scenario_max_retries=2`, `model_review_mode=blocking_major_only`, `repair_review_mode=blocking_major_only` |
| Git commit | `529e3096b4bb0f9c46cd21be461c2ec272e89c53` |
| clean / diff / prompt snapshot | clean=`True`, dirty=`False`, diff_hash=`sha256:2a69ad5797ac568a81bddcef615104303a97261094685f4edd8d4484e889ea09`, prompt_hash=`sha256:ce499624790550d734a59fdd9b6b28f8194710e89c85f739538372d5d8133081` |
| provider/model 脱敏标识 | mode=`real_env`, model=`gpt-5.5`, real_api=`True` |
| source / paper | source=`project_1_llm_state_machine_modeling/sources/state-transitions-logical-design-for-hybrid-energy-generation-with-renewable-energy-sources-in-lng-ship`, paper=`project_1_llm_state_machine_modeling/sources/state-transitions-logical-design-for-hybrid-energy-generation-with-renewable-energy-sources-in-lng-ship/paper.pdf` |
| 样本筛选理由 | issue #14 / PR-D 代表性 Path2 EFSM，变量、guard、12 个状态和非法状态都明确。 |
| 变量参与说明 | `PL/Ppv/Pw/SoC/eng*_Pmax` 是环境输入/容量边界，适合暴露 SD-4 对外部输入变量的处理能力。 |
| run_id | `pr-e1-path2_lng_ems-default-round21compact-92de717a` |
| final verdict/status | verdict=`not_converged`, record=`budget_exhausted`, result=`not_converged` |
| main_result_eligible | `false` |
| final.fcstm 来源 | `{"accepted": true, "final_dsl_hash": "sha256:e81809b0ae1247aa985b29afeaa805e3220ba9027a7d9bfb28607cf1d7a00998", "iteration": 3, "last_rejected_candidate": {"candidate_dsl_hash": "sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855", "iteration": 4, "repair_history_index": 5, "rework_instructions": null, "sl10_decision": null}, "repair_history_index": 4, "selected_source_stage": "SL-7", "sl10_decision": "pass", "source_kind": "repair_candidate"}` |
| FixLog next_action 序列 | `sl9_decision_and_repair, sl10_review, sc11_accept_then_sd2, sl9_decision_and_repair, sl10_review, sc11_accept_then_sd2, sl9_decision_and_repair, sl10_review, sc11_accept_then_sd2, sl9_decision_and_repair, sl10_review, sl9_rework, ... +5` |
| iteration exit_reason 序列 | `candidate_accepted_for_next_full_pass, candidate_accepted_for_next_full_pass, candidate_accepted_for_next_full_pass, candidate_accepted_for_next_full_pass, SC-11 budget gate blocked SD-2 revalidation: iter+1=5 >= max_iterations=5` |
| token/cost/time | tokens=`{'prompt_tokens': 477056, 'completion_tokens': 62158, 'total_tokens': 539212, 'n_calls': 18}`, elapsed=`1566.399s` |
| run record | [`pr-e1-path2_lng_ems-default-round21compact-92de717a.agent_loop.json.gz`](./pr-e1-path2_lng_ems-default-round21compact-92de717a.agent_loop.json.gz) |
| summary/log/final DSL | [`summary.json`](./summary.json), [`checks.json`](./checks.json), [`reproducibility.json`](./reproducibility.json), [`final.fcstm`](./final.fcstm), [`stdout.txt`](./run_logs/stdout.txt), [`stderr.txt`](./run_logs/stderr.txt) |

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
def float LNG_Pmax = 0.0;
def float DG1_Pmax = 0.0;
def float DG2_Pmax = 0.0;
def float DG3_Pmax = 0.0;
def float total_thermal_Pmax = 0.0;
def float requested_generator_power = 0.0;
def float battery_discharge_power = 0.0;
def float battery_charge_power = 0.0;
def float spare_power = 0.0;
def int cut_in_command = 0;
def int cut_out_command = 0;

state LNGShipEMS {
    enter {
        total_thermal_Pmax = LNG_Pmax + eng3_Pmax + DG1_Pmax + DG2_Pmax;
    }

    >> during before {
        total_thermal_Pmax = LNG_Pmax + eng3_Pmax + DG1_Pmax + DG2_Pmax;
    }

    ! * -> ZeroLoadCharge : if [PL == 0.0 && Ppv + Pw > 0.0 && SoC < 0.95];
    ! * -> ZeroLoadSpare : if [PL == 0.0 && Ppv + Pw > 0.0 && SoC >= 0.95];
    ! * -> RESCharge : if [PL > 0.0 && Ppv + Pw >= PL && SoC < 0.95];
    ! * -> RESSpare : if [PL > 0.0 && Ppv + Pw >= PL && SoC >= 0.95];
    ! * -> BatteryDischarge : if [PL > 0.0 && Ppv + Pw < PL && SoC > 0.2 && PL - Ppv - Pw <= total_thermal_Pmax];
    ! * -> LNGChargeMargin : if [PL > 0.0 && Ppv + Pw < PL && SoC <= 0.2 && PL - Ppv - Pw + Pgmax / 5.0 <= LNG_Pmax];
    ! * -> LNGNormal : if [PL > 0.0 && Ppv + Pw < PL && SoC <= 0.2 && PL - Ppv - Pw <= LNG_Pmax];
    ! * -> DG3LNG : if [PL > 0.0 && Ppv + Pw < PL && SoC <= 0.2 && PL - Ppv - Pw > LNG_Pmax && PL - Ppv - Pw <= LNG_Pmax + eng3_Pmax];
    ! * -> DG1AssistCharge : if [PL > 0.0 && Ppv + Pw < PL && SoC <= 0.2 && PL - Ppv - Pw > LNG_Pmax + eng3_Pmax && PL - Ppv - Pw + Pd1max / 10.0 <= LNG_Pmax + eng3_Pmax + DG1_Pmax];
    ! * -> DG2AssistCharge : if [PL > 0.0 && Ppv + Pw < PL && SoC <= 0.2 && PL - Ppv - Pw > LNG_Pmax + eng3_Pmax + DG1_Pmax && PL - Ppv - Pw + Pd1max / 10.0 <= total_thermal_Pmax];
    ! * -> AllThermalBattery : if [PL > 0.0 && Ppv + Pw < PL && PL - Ppv - Pw > total_thermal_Pmax];
    ! * -> IllegalOverloadCompletion : if [PL < 0.0 && PL >= 0.0];

    [*] -> ZeroLoadCharge;

    state ZeroLoadCharge {
        enter {
            requested_generator_power = 0.0;
            battery_discharge_power = 0.0;
            battery_charge_power = Ppv + Pw;
            spare_power = 0.0;
            cut_in_command = 0;
            cut_out_command = 1;
        }
    }

    state ZeroLoadSpare {
        enter {
            requested_generator_power = 0.0;
            battery_discharge_power = 0.0;
            battery_charge_power = 0.0;
            spare_power = Ppv + Pw;
            cut_in_command = 0;
            cut_out_command = 1;
        }
    }

    state RESCharge {
        enter {
            requested_generator_power = 0.0;
            battery_discharge_power = 0.0;
            battery_charge_power = Ppv + Pw - PL;
            spare_power = 0.0;
            cut_in_command = 0;
            cut_out_command = 1;
        }
    }

    state RESSpare {
        enter {
            requested_generator_power = 0.0;
            battery_discharge_power = 0.0;
            battery_charge_power = 0.0;
            spare_power = Ppv + Pw - PL;
            cut_in_command = 0;
            cut_out_command = 1;
        }
    }

    state BatteryDischarge {
        enter {
            requested_generator_power = 0.0;
            battery_discharge_power = PL - Ppv - Pw;
            battery_charge_power = 0.0;
            spare_power = 0.0;
            cut_in_command = 0;
            cut_out_command = 1;
        }
    }

    state LNGChargeMargin {
        enter {
            requested_generator_power = PL - Ppv - Pw + Pgmax / 5.0;
            battery_discharge_power = 0.0;
            battery_charge_power = Pgmax / 5.0;
            spare_power = 0.0;
            cut_in_command = 1;
            cut_out_command = 0;
        }
    }

    state LNGNormal {
        enter {
            requested_generator_power = PL - Ppv - Pw;
            battery_discharge_power = 0.0;
            battery_charge_power = 0.0;
            spare_power = 0.0;
            cut_in_command = 1;
            cut_out_command = 0;
        }
    }

    state DG3LNG {
        enter {
            requested_generator_power = PL - Ppv - Pw;
            battery_discharge_power = 0.0;
            battery_charge_power = 0.0;
            spare_power = 0.0;
            cut_in_command = 1;
            cut_out_command = 0;
        }
    }

    state DG1AssistCharge {
        enter {
            requested_generator_power = PL - Ppv - Pw + Pd1max / 10.0;
            battery_discharge_power = 0.0;
            battery_charge_power = Pd1max / 10.0;
            spare_power = 0.0;
            cut_in_command = 1;
            cut_out_command = 0;
        }
    }

    state DG2AssistCharge {
        enter {
            requested_generator_power = PL - Ppv - Pw + Pd1max / 10.0;
            battery_discharge_power = 0.0;
            battery_charge_power = Pd1max / 10.0;
            spare_power = 0.0;
            cut_in_command = 1;
            cut_out_command = 0;
        }
    }

    state AllThermalBattery {
        enter {
            requested_generator_power = total_thermal_Pmax;
            battery_discharge_power = PL - Ppv - Pw - total_thermal_Pmax;
            battery_charge_power = 0.0;
            spare_power = 0.0;
            cut_in_command = 1;
            cut_out_command = 0;
        }
    }

    state IllegalOverloadCompletion {
        enter {
            requested_generator_power = total_thermal_Pmax;
            battery_discharge_power = PL - Ppv - Pw - total_thermal_Pmax;
            battery_charge_power = 0.0;
            spare_power = 0.0;
            cut_in_command = 1;
            cut_out_command = 0;
        }
    }
}
```

### 4. 全流程真实摘要表

| Stage | 是否 LLM | iteration | 结果 | 获取的信息 / 反馈 | 本阶段做了什么 | DSL 修改 | artifact/log |
|---|---:|---:|---:|---|---|---|---|
| `SC-0` | 否 | - | ✅ | trace/control | 初始化 run state | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round21compact-92de717a.agent_loop.json.gz) |
| `SL-1` | 是 | - | ✅ | LLM calls=1, tokens=17622 | 生成初始 DSL 与 grounding seeds | initial len=5541 | [`record`](./pr-e1-path2_lng_ems-default-round21compact-92de717a.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round21compact-92de717a.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round21compact-92de717a.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ⚠️ | blocking=87, advisory=83, info=0; blocking=51, advisory=81, info=0; blocking=0, advisory=81, info=0; blocking=0, advisory=93, info=0; blocking=1, advisory=131, info=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round21compact-92de717a.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round21compact-92de717a.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=6, tokens=199774 | LLM per-request accept/reject + repair | candidate len=5736,6144,6075,5698,5695,0 | [`record`](./pr-e1-path2_lng_ems-default-round21compact-92de717a.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=5, tokens=122430 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round21compact-92de717a.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round21compact-92de717a.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round21compact-92de717a.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round21compact-92de717a.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ⚠️ | blocking=87, advisory=83, info=0; blocking=51, advisory=81, info=0; blocking=0, advisory=81, info=0; blocking=0, advisory=93, info=0; blocking=1, advisory=131, info=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round21compact-92de717a.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round21compact-92de717a.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=6, tokens=199774 | LLM per-request accept/reject + repair | candidate len=5736,6144,6075,5698,5695,0 | [`record`](./pr-e1-path2_lng_ems-default-round21compact-92de717a.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=5, tokens=122430 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round21compact-92de717a.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round21compact-92de717a.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round21compact-92de717a.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round21compact-92de717a.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=87, advisory=83, info=0; blocking=51, advisory=81, info=0; blocking=0, advisory=81, info=0; blocking=0, advisory=93, info=0; blocking=1, advisory=131, info=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round21compact-92de717a.agent_loop.json.gz) |
| `SL-5` | 是 | 2 | ✅ | LLM calls=5, tokens=127118 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round21compact-92de717a.agent_loop.json.gz) |
| `SD-5A` | 否 | 2 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round21compact-92de717a.agent_loop.json.gz) |
| `SL-5` | 是 | 2 | ✅ | LLM calls=5, tokens=127118 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round21compact-92de717a.agent_loop.json.gz) |
| `SD-5A` | 否 | 2 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round21compact-92de717a.agent_loop.json.gz) |
| `SL-5` | 是 | 2 | ✅ | LLM calls=5, tokens=127118 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round21compact-92de717a.agent_loop.json.gz) |
| `SD-5A` | 否 | 2 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round21compact-92de717a.agent_loop.json.gz) |
| `SC-5F` | 否 | 2 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round21compact-92de717a.agent_loop.json.gz) |
| `SD-6` | 否 | 2 | ⚠️ | ok=False, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round21compact-92de717a.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round21compact-92de717a.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=6, tokens=199774 | LLM per-request accept/reject + repair | candidate len=5736,6144,6075,5698,5695,0 | [`record`](./pr-e1-path2_lng_ems-default-round21compact-92de717a.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=5, tokens=122430 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round21compact-92de717a.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round21compact-92de717a.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round21compact-92de717a.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round21compact-92de717a.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=87, advisory=83, info=0; blocking=51, advisory=81, info=0; blocking=0, advisory=81, info=0; blocking=0, advisory=93, info=0; blocking=1, advisory=131, info=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round21compact-92de717a.agent_loop.json.gz) |
| `SD-5A` | 否 | 2 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round21compact-92de717a.agent_loop.json.gz) |
| `SL-5` | 是 | 2 | ✅ | LLM calls=5, tokens=127118 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round21compact-92de717a.agent_loop.json.gz) |
| `SD-5A` | 否 | 2 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round21compact-92de717a.agent_loop.json.gz) |
| `SL-5` | 是 | 2 | ✅ | LLM calls=5, tokens=127118 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round21compact-92de717a.agent_loop.json.gz) |
| `SD-5A` | 否 | 2 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round21compact-92de717a.agent_loop.json.gz) |
| `SC-5F` | 否 | 2 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round21compact-92de717a.agent_loop.json.gz) |
| `SD-6` | 否 | 2 | ✅ | ok=False, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round21compact-92de717a.agent_loop.json.gz) |
| `SL-7` | 是 | 3 | ✅ | LLM calls=1, tokens=72268 | LLM model review | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round21compact-92de717a.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round21compact-92de717a.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=6, tokens=199774 | LLM per-request accept/reject + repair | candidate len=5736,6144,6075,5698,5695,0 | [`record`](./pr-e1-path2_lng_ems-default-round21compact-92de717a.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=5, tokens=122430 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round21compact-92de717a.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=6, tokens=199774 | LLM per-request accept/reject + repair | candidate len=5736,6144,6075,5698,5695,0 | [`record`](./pr-e1-path2_lng_ems-default-round21compact-92de717a.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=5, tokens=122430 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round21compact-92de717a.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round21compact-92de717a.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round21compact-92de717a.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round21compact-92de717a.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ⚠️ | blocking=87, advisory=83, info=0; blocking=51, advisory=81, info=0; blocking=0, advisory=81, info=0; blocking=0, advisory=93, info=0; blocking=1, advisory=131, info=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round21compact-92de717a.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round21compact-92de717a.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=6, tokens=199774 | LLM per-request accept/reject + repair | candidate len=5736,6144,6075,5698,5695,0 | [`record`](./pr-e1-path2_lng_ems-default-round21compact-92de717a.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round21compact-92de717a.agent_loop.json.gz) |
| `SC-12` | 否 | - | ⚠️ | SC-11 budget gate blocked SD-2 revalidation: iter+1=5 >= max_iterations=5 | 写 final verdict | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round21compact-92de717a.agent_loop.json.gz) |
| `SC-13` | 否 | - | ✅ | trace/control | 写审计 run record | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round21compact-92de717a.agent_loop.json.gz) |

### 5. Iteration / repair / review 摘要

| Iter | selected feedback | repair? | FixRequestBatch | SL-9 | local checks | SL-10 | 回到 SD-2? | verdict/备注 |
|---:|---|---|---|---|---|---|---|---|
| 0 | `SD-4` | yes | fixbatch-0-sha256-0ec5b2793d7 / n=12 | accept=4, reject=8, waiver=8 | ok=False, target=False, regression=False, drift=major, local_stage=SD-10, reason=design_target_unresolved; new_blocking_design_diagnostic; missing_required_grounding | decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none> | yes | candidate_accepted_for_next_full_pass |
| 1 | `SD-4` | yes | fixbatch-1-sha256-74319a5ab0c / n=12 | accept=12, reject=0, waiver=0 | ok=False, target=False, regression=False, drift=major, local_stage=SD-10, reason=missing_required_grounding | decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none> | yes | candidate_accepted_for_next_full_pass |
| 2 | `SD-6` | yes | fixbatch-2-sha256-019672ca0f5 / n=1 | accept=1, reject=0, waiver=0 | ok=False, target=False, regression=False, drift=major, local_stage=SD-10, reason=missing_required_grounding | decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none> | yes | candidate_accepted_for_next_full_pass |
| 3 | `SL-7` | yes | fixbatch-3-sha256-6be8c93fa32 / n=2 | accept=2, reject=0, waiver=0 | ok=False, target=False, regression=True, drift=major, local_stage=SD-10, reason=new_blocking_design_diagnostic; scenario_regression; missing_required_grounding | decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none> | yes | candidate_accepted_for_next_full_pass |
| 4 | `SD-4` | yes | fixbatch-4-sha256-8d0380f4536 / n=1 | accept=0, reject=1, waiver=1 | <none> | decision=None, ok=True, target=True, regression=False, drift=minor, rework=<none> | no | SC-11 budget gate blocked SD-2 revalidation: iter+1=5 >= max_iterations=5 |

### 6. Scenario 明细与逐轮通过情况

#### 6.1 Scenario pass/fail by iteration

口径：`✅` = 该 scenario 在该轮 SD-6 simulation 通过；`❌` = 该轮失败；`⚪` = 该轮未执行或无该 scenario 结果。

| Scenario | Intent | Iter 3 | Iter 4 |
|---|---|---|---|
| `default_init_zero_load_charges_battery` | default-init dispatches to the initial zero-load RES charging mode when PL=0, RES is available, and SoC is below 0.95. | ✅ | ✅ |
| `zero_load_soc_threshold_spare` | explicit-hot-start probes the zero-load SoC boundary: at SoC=0.95 RES production becomes spare power, not battery chargi...<truncated 3 chars> | ✅ | ✅ |
| `res_covers_load_soc_below_threshold` | explicit-hot-start verifies RES covers positive load and charges the battery while SoC is below 0.95. | ✅ | ✅ |
| `res_covers_load_soc_at_threshold_spare` | explicit-hot-start probes the RES-covered SoC boundary: at SoC=0.95 residual renewable power is spare. | ✅ | ✅ |
| `battery_discharge_priority_when_soc_suitable` | explicit-hot-start verifies that when RES is below load and SoC is suitable, the battery supplies the deficit before the...<truncated 11 chars> | ✅ | ✅ |
| `low_soc_lng_charge_margin` | explicit-hot-start verifies the low-SoC LNG-covered branch adds the Pgmax/5 charging margin. | ✅ | ✅ |
| `lng_and_dg_priority_branches` | explicit-hot-start scenarios from thermal modes probe LNG before diesel and DG3 before DG1/DG2 last-priority charging br...<truncated 7 chars> | ✅ | ✅ |
| `dg3_lng_capacity_branch` | explicit-hot-start verifies the next priority branch uses LNG plus engine-3 capacity before DG1/DG2. | ✅ | ✅ |
| `diesel_assist_charge_branches` | explicit-hot-start verifies low-SoC DG1 and DG2 last-priority branches add the Pd1max/10 charging margin. | ✅ | ✅ |
| `dg2_assist_charge_branch` | explicit-hot-start verifies DG2 assist is selected only after LNG, engine-3, and DG1 capacity are insufficient, with Pd1...<truncated 21 chars> | ✅ | ✅ |
| `extreme_demand_uses_all_thermal_and_battery` | explicit-hot-start verifies extreme demand beyond all RES and thermal resources activates all thermal units and covers r...<truncated 35 chars> | ✅ | ✅ |
| `illegal_overload_completion_never_selected` | explicit-hot-start probes the illegal overload-completion corner: even with extreme demand at empty SoC, NL says the ill...<truncated 41 chars> | ❌ | ✅ |
| `forced_reselection_from_zero_load_to_lng_normal` | explicit-hot-start targets the wildcard forced dispatch line: from a zero-load leaf, changed demand with suitable SoC an...<truncated 52 chars> | ✅ | ✅ |
| `forced_reselection_from_thermal_to_res_spare` | explicit-hot-start targets the wildcard forced dispatch line from a different concrete leaf: when RES now covers load an...<truncated 64 chars> | ✅ | ✅ |
| `default_init_forced_selection_to_res_charge` | default-init first dispatches to the initial leaf, then the wildcard forced dispatch guard must re-select RESCharge when...<truncated 55 chars> | ✅ | ✅ |
| `forced_exact_res_cover_boundary_to_res_charge` | explicit-hot-start strengthens the wildcard forced dispatch probe: when Ppv+Pw exactly equals positive PL and SoC is bel...<truncated 52 chars> | ⚪ | ✅ |
| `forced_zero_load_exact_soc_boundary_from_battery` | explicit-hot-start strengthens the wildcard forced dispatch probe: from a battery-discharge leaf, PL=0 with SoC exactly ...<truncated 30 chars> | ⚪ | ✅ |
| `forced_res_spare_exact_cover_and_soc_boundary` | explicit-hot-start targets unreachable-target mutations on the RES coverage and SoC>=0.95 forced guard: exact RES cover ...<truncated 39 chars> | ⚪ | ✅ |
| `forced_all_thermal_from_res_charge_extreme_demand` | explicit-hot-start targets a missing wildcard forced dispatch line from a RES leaf: extreme demand above all thermal res...<truncated 40 chars> | ⚪ | ✅ |

#### 6.2 Scenario definitions

<details><summary>`default_init_zero_load_charges_battery` — default-init dispatches to the initial zero-load RES charging mode when PL=0, RES is available, and SoC is below 0.95.</summary>

| Field | Value |
|---|---|
| description | default-init dispatches to the initial zero-load RES charging mode when PL=0, RES is available, and SoC is below 0.95. |
| initial_state | `<default-init>` |
| initial_vars | `{"PL": 0.0, "Ppv": 6.0, "Pw": 4.0, "SoC": 0.5}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `initial_zero_load_charge` | `0` | `[]` | `LNGShipEMS.ZeroLoadCharge` | `{"battery_charge_power": 10.0, "battery_discharge_power": 0.0, "cut_in_command": 0, "cut_out_command": 1, "requested_generator_power": 0.0, "spare_power": 0.0}` |

</details>

<details><summary>`zero_load_soc_threshold_spare` — explicit-hot-start probes the zero-load SoC boundary: at SoC=0.95 RES production becomes spare power, not battery charging.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start probes the zero-load SoC boundary: at SoC=0.95 RES production becomes spare power, not battery charging. |
| initial_state | `LNGShipEMS.ZeroLoadCharge` |
| initial_vars | `{"PL": 0.0, "Ppv": 7.0, "Pw": 3.0, "SoC": 0.95}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `zero_load_spare_at_soc_095` | `0` | `[]` | `LNGShipEMS.ZeroLoadSpare` | `{"battery_charge_power": 0.0, "battery_discharge_power": 0.0, "cut_in_command": 0, "cut_out_command": 1, "requested_generator_power": 0.0, "spare_power": 10.0}` |

</details>

<details><summary>`res_covers_load_soc_below_threshold` — explicit-hot-start verifies RES covers positive load and charges the battery while SoC is below 0.95.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start verifies RES covers positive load and charges the battery while SoC is below 0.95. |
| initial_state | `LNGShipEMS.ZeroLoadCharge` |
| initial_vars | `{"PL": 8.0, "Ppv": 6.0, "Pw": 4.0, "SoC": 0.94}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `res_charge_below_soc_095` | `0` | `[]` | `LNGShipEMS.RESCharge` | `{"battery_charge_power": 2.0, "battery_discharge_power": 0.0, "cut_in_command": 0, "cut_out_command": 1, "requested_generator_power": 0.0, "spare_power": 0.0}` |

</details>

<details><summary>`res_covers_load_soc_at_threshold_spare` — explicit-hot-start probes the RES-covered SoC boundary: at SoC=0.95 residual renewable power is spare.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start probes the RES-covered SoC boundary: at SoC=0.95 residual renewable power is spare. |
| initial_state | `LNGShipEMS.RESCharge` |
| initial_vars | `{"PL": 8.0, "Ppv": 6.0, "Pw": 4.0, "SoC": 0.95}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `res_spare_at_soc_095` | `0` | `[]` | `LNGShipEMS.RESSpare` | `{"battery_charge_power": 0.0, "battery_discharge_power": 0.0, "cut_in_command": 0, "cut_out_command": 1, "requested_generator_power": 0.0, "spare_power": 2.0}` |

</details>

<details><summary>`battery_discharge_priority_when_soc_suitable` — explicit-hot-start verifies that when RES is below load and SoC is suitable, the battery supplies the deficit before thermal units.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start verifies that when RES is below load and SoC is suitable, the battery supplies the deficit before thermal units. |
| initial_state | `LNGShipEMS.RESSpare` |
| initial_vars | `{"DG1_Pmax": 10.0, "DG2_Pmax": 10.0, "LNG_Pmax": 20.0, "PL": 15.0, "Pgmax": 10.0, "Ppv": 5.0, "Pw": 2.0, "SoC": 0.5, "eng3_Pmax": 10.0, "total_thermal_Pmax": 50.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `battery_supplies_deficit` | `0` | `[]` | `LNGShipEMS.BatteryDischarge` | `{"battery_charge_power": 0.0, "battery_discharge_power": 8.0, "cut_in_command": 0, "cut_out_command": 1, "requested_generator_power": 0.0, "spare_power": 0.0}` |

</details>

<details><summary>`low_soc_lng_charge_margin` — explicit-hot-start verifies the low-SoC LNG-covered branch adds the Pgmax/5 charging margin.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start verifies the low-SoC LNG-covered branch adds the Pgmax/5 charging margin. |
| initial_state | `LNGShipEMS.BatteryDischarge` |
| initial_vars | `{"DG1_Pmax": 10.0, "DG2_Pmax": 10.0, "LNG_Pmax": 25.0, "PL": 30.0, "Pgmax": 25.0, "Ppv": 4.0, "Pw": 6.0, "SoC": 0.2, "eng3_Pmax": 10.0, "total_thermal_Pmax": 55.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `lng_charge_margin_with_low_soc` | `0` | `[]` | `LNGShipEMS.LNGChargeMargin` | `{"battery_charge_power": 5.0, "battery_discharge_power": 0.0, "cut_in_command": 1, "cut_out_command": 0, "requested_generator_power": 25.0, "spare_power": 0.0}` |

</details>

<details><summary>`lng_and_dg_priority_branches` — explicit-hot-start scenarios from thermal modes probe LNG before diesel and DG3 before DG1/DG2 last-priority charging branches.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start scenarios from thermal modes probe LNG before diesel and DG3 before DG1/DG2 last-priority charging branches. |
| initial_state | `LNGShipEMS.LNGChargeMargin` |
| initial_vars | `{"DG1_Pmax": 20.0, "DG2_Pmax": 20.0, "LNG_Pmax": 25.0, "PL": 28.0, "Pgmax": 5.0, "Ppv": 3.0, "Pw": 5.0, "SoC": 0.5, "eng3_Pmax": 15.0, "total_thermal_Pmax": 80.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `lng_normal_covers_deficit` | `0` | `[]` | `LNGShipEMS.LNGNormal` | `{"battery_charge_power": 0.0, "battery_discharge_power": 0.0, "cut_in_command": 1, "cut_out_command": 0, "requested_generator_power": 20.0, "spare_power": 0.0}` |

</details>

<details><summary>`dg3_lng_capacity_branch` — explicit-hot-start verifies the next priority branch uses LNG plus engine-3 capacity before DG1/DG2.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start verifies the next priority branch uses LNG plus engine-3 capacity before DG1/DG2. |
| initial_state | `LNGShipEMS.LNGNormal` |
| initial_vars | `{"DG1_Pmax": 20.0, "DG2_Pmax": 20.0, "LNG_Pmax": 25.0, "PL": 45.0, "Ppv": 4.0, "Pw": 6.0, "SoC": 0.5, "eng3_Pmax": 15.0, "total_thermal_Pmax": 80.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `dg3_lng_covers_deficit` | `0` | `[]` | `LNGShipEMS.DG3LNG` | `{"battery_charge_power": 0.0, "battery_discharge_power": 0.0, "cut_in_command": 1, "cut_out_command": 0, "requested_generator_power": 35.0, "spare_power": 0.0}` |

</details>

<details><summary>`diesel_assist_charge_branches` — explicit-hot-start verifies low-SoC DG1 and DG2 last-priority branches add the Pd1max/10 charging margin.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start verifies low-SoC DG1 and DG2 last-priority branches add the Pd1max/10 charging margin. |
| initial_state | `LNGShipEMS.DG3LNG` |
| initial_vars | `{"DG1_Pmax": 20.0, "DG2_Pmax": 25.0, "LNG_Pmax": 25.0, "PL": 58.0, "Pd1max": 10.0, "Ppv": 4.0, "Pw": 4.0, "SoC": 0.2, "eng3_Pmax": 15.0, "total_thermal_Pmax": 85.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `dg1_assist_charge_margin` | `0` | `[]` | `LNGShipEMS.DG1AssistCharge` | `{"battery_charge_power": 1.0, "battery_discharge_power": 0.0, "cut_in_command": 1, "cut_out_command": 0, "requested_generator_power": 51.0, "spare_power": 0.0}` |

</details>

<details><summary>`dg2_assist_charge_branch` — explicit-hot-start verifies DG2 assist is selected only after LNG, engine-3, and DG1 capacity are insufficient, with Pd1max/10 charge margin.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start verifies DG2 assist is selected only after LNG, engine-3, and DG1 capacity are insufficient, with Pd1max/10 charge margin. |
| initial_state | `LNGShipEMS.DG1AssistCharge` |
| initial_vars | `{"DG1_Pmax": 20.0, "DG2_Pmax": 25.0, "LNG_Pmax": 25.0, "PL": 78.0, "Pd1max": 10.0, "Ppv": 4.0, "Pw": 4.0, "SoC": 0.2, "eng3_Pmax": 15.0, "total_thermal_Pmax": 85.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `dg2_assist_charge_margin` | `0` | `[]` | `LNGShipEMS.DG2AssistCharge` | `{"battery_charge_power": 1.0, "battery_discharge_power": 0.0, "cut_in_command": 1, "cut_out_command": 0, "requested_generator_power": 71.0, "spare_power": 0.0}` |

</details>

<details><summary>`extreme_demand_uses_all_thermal_and_battery` — explicit-hot-start verifies extreme demand beyond all RES and thermal resources activates all thermal units and covers remaining lack by battery discharge.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start verifies extreme demand beyond all RES and thermal resources activates all thermal units and covers remaining lack by battery discharge. |
| initial_state | `LNGShipEMS.DG2AssistCharge` |
| initial_vars | `{"DG1_Pmax": 20.0, "DG2_Pmax": 20.0, "LNG_Pmax": 30.0, "PL": 120.0, "Ppv": 5.0, "Pw": 5.0, "SoC": 0.5, "eng3_Pmax": 20.0, "total_thermal_Pmax": 90.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `all_thermal_plus_battery_deficit` | `0` | `[]` | `LNGShipEMS.AllThermalBattery` | `{"battery_charge_power": 0.0, "battery_discharge_power": 20.0, "cut_in_command": 1, "cut_out_command": 0, "requested_generator_power": 90.0, "spare_power": 0.0}` |

</details>

<details><summary>`illegal_overload_completion_never_selected` — explicit-hot-start probes the illegal overload-completion corner: even with extreme demand at empty SoC, NL says the illegal state shall never occur in practice...<truncated 1 chars></summary>

| Field | Value |
|---|---|
| description | explicit-hot-start probes the illegal overload-completion corner: even with extreme demand at empty SoC, NL says the illegal state shall never occur in practice. |
| initial_state | `LNGShipEMS.AllThermalBattery` |
| initial_vars | `{"DG1_Pmax": 20.0, "DG2_Pmax": 20.0, "LNG_Pmax": 30.0, "PL": 120.0, "Ppv": 5.0, "Pw": 5.0, "SoC": 0.0, "eng3_Pmax": 20.0, "total_thermal_Pmax": 90.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `stay_out_of_illegal_completion` | `0` | `[]` | `LNGShipEMS.AllThermalBattery` | `{"battery_charge_power": 0.0, "battery_discharge_power": 20.0, "cut_in_command": 1, "cut_out_command": 0, "requested_generator_power": 90.0, "spare_power": 0.0}` |

</details>

<details><summary>`forced_reselection_from_zero_load_to_lng_normal` — explicit-hot-start targets the wildcard forced dispatch line: from a zero-load leaf, changed demand with suitable SoC and LNG capacity must force re-selection t...<truncated 12 chars></summary>

| Field | Value |
|---|---|
| description | explicit-hot-start targets the wildcard forced dispatch line: from a zero-load leaf, changed demand with suitable SoC and LNG capacity must force re-selection to LNGNormal. |
| initial_state | `LNGShipEMS.ZeroLoadSpare` |
| initial_vars | `{"DG1_Pmax": 10.0, "DG2_Pmax": 10.0, "LNG_Pmax": 30.0, "PL": 32.0, "Pgmax": 5.0, "Ppv": 4.0, "Pw": 3.0, "SoC": 0.6, "eng3_Pmax": 10.0, "total_thermal_Pmax": 50.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `forced_to_lng_normal_after_demand_change` | `0` | `[]` | `LNGShipEMS.LNGNormal` | `{"battery_charge_power": 0.0, "battery_discharge_power": 0.0, "cut_in_command": 1, "cut_out_command": 0, "requested_generator_power": 25.0, "spare_power": 0.0}` |

</details>

<details><summary>`forced_reselection_from_thermal_to_res_spare` — explicit-hot-start targets the wildcard forced dispatch line from a different concrete leaf: when RES now covers load and SoC is at least 0.95, EMS must force r...<truncated 24 chars></summary>

| Field | Value |
|---|---|
| description | explicit-hot-start targets the wildcard forced dispatch line from a different concrete leaf: when RES now covers load and SoC is at least 0.95, EMS must force re-selection to RESSpare. |
| initial_state | `LNGShipEMS.DG2AssistCharge` |
| initial_vars | `{"DG1_Pmax": 20.0, "DG2_Pmax": 25.0, "LNG_Pmax": 25.0, "PL": 12.0, "Pd1max": 10.0, "Pgmax": 10.0, "Ppv": 9.0, "Pw": 5.0, "SoC": 0.95, "eng3_Pmax": 15.0, "total_thermal_Pmax": 85.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `forced_to_res_spare_after_res_recovers` | `0` | `[]` | `LNGShipEMS.RESSpare` | `{"battery_charge_power": 0.0, "battery_discharge_power": 0.0, "cut_in_command": 0, "cut_out_command": 1, "requested_generator_power": 0.0, "spare_power": 2.0}` |

</details>

<details><summary>`default_init_forced_selection_to_res_charge` — default-init first dispatches to the initial leaf, then the wildcard forced dispatch guard must re-select RESCharge when positive load is covered by RES and SoC...<truncated 15 chars></summary>

| Field | Value |
|---|---|
| description | default-init first dispatches to the initial leaf, then the wildcard forced dispatch guard must re-select RESCharge when positive load is covered by RES and SoC is below 0.95. |
| initial_state | `<default-init>` |
| initial_vars | `{"DG1_Pmax": 10.0, "DG2_Pmax": 10.0, "LNG_Pmax": 20.0, "PL": 8.0, "Pgmax": 10.0, "Ppv": 6.0, "Pw": 4.0, "SoC": 0.5, "eng3_Pmax": 10.0, "total_thermal_Pmax": 50.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `default_initial_leaf_dispatched` | `0` | `[]` | `LNGShipEMS.ZeroLoadCharge` | `{}` |
| 1 `forced_dispatch_selects_res_charge` | `0` | `[]` | `LNGShipEMS.RESCharge` | `{"battery_charge_power": 2.0, "battery_discharge_power": 0.0, "cut_in_command": 0, "cut_out_command": 1, "requested_generator_power": 0.0, "spare_power": 0.0}` |

</details>

<details><summary>`forced_exact_res_cover_boundary_to_res_charge` — explicit-hot-start strengthens the wildcard forced dispatch probe: when Ppv+Pw exactly equals positive PL and SoC is below 0.95, the >= cover boundary must forc...<truncated 12 chars></summary>

| Field | Value |
|---|---|
| description | explicit-hot-start strengthens the wildcard forced dispatch probe: when Ppv+Pw exactly equals positive PL and SoC is below 0.95, the >= cover boundary must force RESCharge. |
| initial_state | `LNGShipEMS.LNGNormal` |
| initial_vars | `{"DG1_Pmax": 10.0, "DG2_Pmax": 10.0, "LNG_Pmax": 20.0, "PL": 10.0, "Pgmax": 10.0, "Ppv": 6.0, "Pw": 4.0, "SoC": 0.94, "eng3_Pmax": 10.0, "total_thermal_Pmax": 50.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `forced_exact_cover_selects_res_charge` | `0` | `[]` | `LNGShipEMS.RESCharge` | `{"battery_charge_power": 0.0, "battery_discharge_power": 0.0, "cut_in_command": 0, "cut_out_command": 1, "requested_generator_power": 0.0, "spare_power": 0.0}` |

</details>

<details><summary>`forced_zero_load_exact_soc_boundary_from_battery` — explicit-hot-start strengthens the wildcard forced dispatch probe: from a battery-discharge leaf, PL=0 with SoC exactly 0.95 must force ZeroLoadSpare.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start strengthens the wildcard forced dispatch probe: from a battery-discharge leaf, PL=0 with SoC exactly 0.95 must force ZeroLoadSpare. |
| initial_state | `LNGShipEMS.BatteryDischarge` |
| initial_vars | `{"DG1_Pmax": 10.0, "DG2_Pmax": 10.0, "LNG_Pmax": 20.0, "PL": 0.0, "Pgmax": 10.0, "Ppv": 8.0, "Pw": 2.0, "SoC": 0.95, "eng3_Pmax": 10.0, "total_thermal_Pmax": 50.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `forced_zero_load_soc_095_selects_spare` | `0` | `[]` | `LNGShipEMS.ZeroLoadSpare` | `{"battery_charge_power": 0.0, "battery_discharge_power": 0.0, "cut_in_command": 0, "cut_out_command": 1, "requested_generator_power": 0.0, "spare_power": 10.0}` |

</details>

<details><summary>`forced_res_spare_exact_cover_and_soc_boundary` — explicit-hot-start targets unreachable-target mutations on the RES coverage and SoC>=0.95 forced guard: exact RES cover with full battery must select RESSpare.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start targets unreachable-target mutations on the RES coverage and SoC>=0.95 forced guard: exact RES cover with full battery must select RESSpare. |
| initial_state | `LNGShipEMS.BatteryDischarge` |
| initial_vars | `{"DG1_Pmax": 10.0, "DG2_Pmax": 10.0, "LNG_Pmax": 20.0, "PL": 10.0, "Pgmax": 10.0, "Ppv": 6.0, "Pw": 4.0, "SoC": 0.95, "eng3_Pmax": 10.0, "total_thermal_Pmax": 50.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `exact_cover_full_soc_forces_res_spare` | `0` | `[]` | `LNGShipEMS.RESSpare` | `{"battery_charge_power": 0.0, "battery_discharge_power": 0.0, "cut_in_command": 0, "cut_out_command": 1, "requested_generator_power": 0.0, "spare_power": 0.0}` |

</details>

<details><summary>`forced_all_thermal_from_res_charge_extreme_demand` — explicit-hot-start targets a missing wildcard forced dispatch line from a RES leaf: extreme demand above all thermal resources must re-select AllThermalBattery.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start targets a missing wildcard forced dispatch line from a RES leaf: extreme demand above all thermal resources must re-select AllThermalBattery. |
| initial_state | `LNGShipEMS.RESCharge` |
| initial_vars | `{"DG1_Pmax": 20.0, "DG2_Pmax": 20.0, "LNG_Pmax": 30.0, "PL": 130.0, "Ppv": 10.0, "Pw": 10.0, "SoC": 0.5, "eng3_Pmax": 20.0, "total_thermal_Pmax": 90.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `extreme_demand_forces_all_thermal` | `0` | `[]` | `LNGShipEMS.AllThermalBattery` | `{"battery_charge_power": 0.0, "battery_discharge_power": 20.0, "cut_in_command": 1, "cut_out_command": 0, "requested_generator_power": 90.0, "spare_power": 0.0}` |

</details>


### 7. Repair / blocking feedback 明细

口径：本节记录 agent-loop 真实进入 repair block 后的证据链：FixRequestBatch、SL-9 per-request accept/reject、candidate diff、local-check evidence、SL-10(NL+FixLog) 审阅，以及完整 FixLog ledger 摘录。

| Repair | iteration | accepted | source | blocking diagnostics | SL-9 decisions | SL-10 / local checks | candidate hash |
|---:|---:|---:|---|---|---|---|---|
| 1 | `0` | ✅ | `SD-4` | W_UNWRITTEN_READ_VAR:var_name=LNG_Pmax, W_UNWRITTEN_READ_VAR:var_name=DG1_Pmax, W_UNWRITTEN_READ_VAR:var_name=total_thermal_Pmax, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.LNGChargeMargin, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.LNGNormal, ... +87 | accept=4, reject=8, waiver=8 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none>; local ok=False, target=False, regression=False, drift=major, local_stage=SD-10, reason=design_target_unresolved; new_blocking_design_diagnostic; missing_required_grounding | `sha256:69829f7850ab3861fd27c07e16b841ea694987f57aaf5930f68e7a8a7f892b2e` |
| 2 | `1` | ✅ | `SD-4` | W_UNWRITTEN_READ_VAR:var_name=LNG_Pmax, W_UNWRITTEN_READ_VAR:var_name=DG1_Pmax, W_UNWRITTEN_READ_VAR:var_name=DG2_Pmax, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.LNGChargeMargin, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.LNGNormal, ... +51 | accept=12, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none>; local ok=False, target=False, regression=False, drift=major, local_stage=SD-10, reason=missing_required_grounding | `sha256:3a69e26a9639a55d35ca176ca3f86c259a1ba8364b6eacf68c65c280891258fd` |
| 3 | `2` | ✅ | `SD-6` | illegal_overload_completion_never_selected | accept=1, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none>; local ok=False, target=False, regression=False, drift=major, local_stage=SD-10, reason=missing_required_grounding | `sha256:b9b293c5f1d54546ed6732d6f5f5fe3410841e17490ca551a584eb572de5aa37` |
| 4 | `3` | ❌ | `SL-7` | 0, 1 | accept=2, reject=0, waiver=0 | SL-10 decision=rework, ok=False, target=False, regression=True, drift=major, rework=Keep the removal of all negative-capacity clamping writes for LNG_Pmax, DG1_Pmax, and DG2_Pmax. Do not reintroduce clamping and do not add meaningless self-assignments to silen...<truncated 314 chars> | `sha256:3708738b7eb83639a2f4da79b0735b2fcc58e757e27910342469683c0aaf3cd2` |
| 5 | `3` | ✅ | `SL-7` | 0, 1 | accept=2, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none>; local ok=False, target=False, regression=True, drift=major, local_stage=SD-10, reason=new_blocking_design_diagnostic; scenario_regression; missing_required_grounding | `sha256:e81809b0ae1247aa985b29afeaa805e3220ba9027a7d9bfb28607cf1d7a00998` |
| 6 | `4` | ❌ | `SD-4` | W_UNWRITTEN_READ_VAR:var_name=DG2_Pmax, W_UNWRITTEN_READ_VAR, W_UNREFERENCED_VAR, W_GUARD_VARS_NEVER_CHANGE, W_VARIABLE_DECLARED_NEVER_USED, ... +1 | accept=0, reject=1, waiver=1 | <none> | `sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |

<details><summary>Repair 1 / iteration `0` / source `SD-4` / accepted=✅</summary>

#### 为什么进入修复

- selected feedback source：`SD-4`；blocking=`True`；pre_scenario=`True`。
- problem_summary：Variable 'LNG_Pmax' is read but never written by any action or transition effect.; Variable 'DG1_Pmax' is read but never written by any action or transition effect.; Variable 'total_thermal_Pmax' is read but never written by any action or transition effect.
- diagnostic ids：`W_UNWRITTEN_READ_VAR:var_name=LNG_Pmax, W_UNWRITTEN_READ_VAR:var_name=DG1_Pmax, W_UNWRITTEN_READ_VAR:var_name=total_thermal_Pmax, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.LNGChargeMargin, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.LNGNormal, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.DG3LNG, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.DG1AssistCharge, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.DG2AssistCharge, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.AllThermalBattery, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.IllegalOverloadCompletion, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadSpare:to_path=LNGShipEMS.LNGChargeMargin, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadSpare:to_path=LNGShipEMS.LNGNormal, ... +80`。
- before_dsl_hash：`sha256:f3ca6b7766b7acea93d3d95bbb5bc36186d7a7c18641c06bf7e6e9682e76a35f`；candidate_dsl_hash：`sha256:69829f7850ab3861fd27c07e16b841ea694987f57aaf5930f68e7a8a7f892b2e`。

#### 错误证据 / diagnostics

- 1. `W_UNWRITTEN_READ_VAR` `W_UNWRITTEN_READ_VAR:var_name=LNG_Pmax` policy=`budgeted_repair`：Variable 'LNG_Pmax' is read but never written by any action or transition effect.；refs=`{"init_value": "0.0", "read_states": ["LNGShipEMS.AllThermalBattery", "LNGShipEMS.BatteryDischarge", "LNGShipEMS.DG1AssistCharge", "LNGShipEMS.DG2AssistCharge", "LNGShipEMS.DG3LNG", "LNGShipEMS.IllegalOverloadCompletion", "LNGShipEMS.LNGChargeMargin", "LNGShipEMS.LNGNormal", "LNGShipEMS.RESCharge", ...<truncated 104 chars>`
- 2. `W_UNWRITTEN_READ_VAR` `W_UNWRITTEN_READ_VAR:var_name=DG1_Pmax` policy=`budgeted_repair`：Variable 'DG1_Pmax' is read but never written by any action or transition effect.；refs=`{"init_value": "0.0", "read_states": ["LNGShipEMS.AllThermalBattery", "LNGShipEMS.BatteryDischarge", "LNGShipEMS.DG1AssistCharge", "LNGShipEMS.DG2AssistCharge", "LNGShipEMS.DG3LNG", "LNGShipEMS.IllegalOverloadCompletion", "LNGShipEMS.LNGChargeMargin", "LNGShipEMS.LNGNormal", "LNGShipEMS.RESCharge", ...<truncated 104 chars>`
- 3. `W_UNWRITTEN_READ_VAR` `W_UNWRITTEN_READ_VAR:var_name=total_thermal_Pmax` policy=`budgeted_repair`：Variable 'total_thermal_Pmax' is read but never written by any action or transition effect.；refs=`{"init_value": "0.0", "read_states": ["LNGShipEMS.AllThermalBattery", "LNGShipEMS.BatteryDischarge", "LNGShipEMS.DG1AssistCharge", "LNGShipEMS.DG2AssistCharge", "LNGShipEMS.DG3LNG", "LNGShipEMS.IllegalOverloadCompletion", "LNGShipEMS.LNGChargeMargin", "LNGShipEMS.LNGNormal", "LNGShipEMS.RESCharge", ...<truncated 114 chars>`
- 4. `W_GUARD_VARS_NEVER_CHANGE` `W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.LNGChargeMargin` policy=`budgeted_repair`：Transition guard reads only variables that are never changed by actions or effects.；refs=`{"from_path": "LNGShipEMS.ZeroLoadCharge", "guard_vars": ["LNG_Pmax", "PL", "Pgmax", "Ppv", "Pw", "SoC"], "to_path": "LNGShipEMS.LNGChargeMargin"}`
- 5. `W_GUARD_VARS_NEVER_CHANGE` `W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.LNGNormal` policy=`budgeted_repair`：Transition guard reads only variables that are never changed by actions or effects.；refs=`{"from_path": "LNGShipEMS.ZeroLoadCharge", "guard_vars": ["LNG_Pmax", "PL", "Ppv", "Pw", "SoC"], "to_path": "LNGShipEMS.LNGNormal"}`
- 6. `W_GUARD_VARS_NEVER_CHANGE` `W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.DG3LNG` policy=`budgeted_repair`：Transition guard reads only variables that are never changed by actions or effects.；refs=`{"from_path": "LNGShipEMS.ZeroLoadCharge", "guard_vars": ["LNG_Pmax", "PL", "Ppv", "Pw", "eng3_Pmax"], "to_path": "LNGShipEMS.DG3LNG"}`
- 7. `W_GUARD_VARS_NEVER_CHANGE` `W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.DG1AssistCharge` policy=`budgeted_repair`：Transition guard reads only variables that are never changed by actions or effects.；refs=`{"from_path": "LNGShipEMS.ZeroLoadCharge", "guard_vars": ["DG1_Pmax", "LNG_Pmax", "PL", "Pd1max", "Ppv", "Pw", "SoC", "eng3_Pmax"], "to_path": "LNGShipEMS.DG1AssistCharge"}`
- 8. `W_GUARD_VARS_NEVER_CHANGE` `W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.DG2AssistCharge` policy=`budgeted_repair`：Transition guard reads only variables that are never changed by actions or effects.；refs=`{"from_path": "LNGShipEMS.ZeroLoadCharge", "guard_vars": ["DG1_Pmax", "LNG_Pmax", "PL", "Pd1max", "Ppv", "Pw", "SoC", "eng3_Pmax", "total_thermal_Pmax"], "to_path": "LNGShipEMS.DG2AssistCharge"}`
- ……另有 `79` 条 evidence 见 run record。

#### 变量角色与上下文提示

- policy：Advisory only. Do not invent writes for external_input_candidate variables unless NL explicitly gives update semantics; add meaningful NL-grounded writes only for internal state variables.
- source：SD-4 diagnostic refs and generic NL external-input rationale

| Variable | role_hint | nl_token_present | diagnostics |
|---|---|---:|---|
| `DG1_Pmax` | `unknown` | ❌ | `W_UNWRITTEN_READ_VAR, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +20` |
| `DG2_Pmax` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_DECLARED_NEVER_USED` |
| `DG3_Pmax` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_DECLARED_NEVER_USED` |
| `LNG_Pmax` | `unknown` | ❌ | `W_UNWRITTEN_READ_VAR, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +56` |
| `PL` | `external_input_candidate` | ✅ | `W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +140` |
| `Pd1max` | `external_input_candidate` | ✅ | `W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +20` |
| `Pgmax` | `external_input_candidate` | ✅ | `W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +20` |
| `Ppv` | `external_input_candidate` | ✅ | `W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +140` |
| `Pw` | `external_input_candidate` | ✅ | `W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +140` |
| `SoC` | `external_input_candidate` | ✅ | `W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +128` |
| `battery_charge_power` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `battery_discharge_power` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `cut_in_command` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `cut_out_command` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `eng3_Pmax` | `external_input_candidate` | ✅ | `W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +32` |
| `requested_generator_power` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `spare_power` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `total_thermal_Pmax` | `unknown` | ❌ | `W_UNWRITTEN_READ_VAR, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +32` |

#### SD-8 FixRequestBatch / 修改请求

- batch_id：`fixbatch-0-sha256-0ec5b2793d7`；source_stage=`SD-4`；legacy_plan_kind=`FixPlan`；requests=`12`。

| request_id | severity | hard | waiver | problem | evidence |
|---|---|---:|---:|---|---|
| `fixreq-0-sd4-0-5a3703670c` | `blocking_warning` | ❌ | ✅ | Variable 'LNG_Pmax' is read but never written by any action or transition effect.; Variable 'DG1_Pmax' is read but never written by any action or transition effect.; Variable 'total_thermal_Pmax' is read but never writte...<truncated 37 chars> | `W_UNWRITTEN_READ_VAR` |
| `fixreq-0-sd4-1-fb9af9e195` | `blocking_warning` | ❌ | ✅ | Variable 'LNG_Pmax' is read but never written by any action or transition effect.; Variable 'DG1_Pmax' is read but never written by any action or transition effect.; Variable 'total_thermal_Pmax' is read but never writte...<truncated 37 chars> | `W_UNWRITTEN_READ_VAR` |
| `fixreq-0-sd4-2-e1d447c2cf` | `blocking_warning` | ❌ | ✅ | Variable 'LNG_Pmax' is read but never written by any action or transition effect.; Variable 'DG1_Pmax' is read but never written by any action or transition effect.; Variable 'total_thermal_Pmax' is read but never writte...<truncated 37 chars> | `W_UNWRITTEN_READ_VAR` |
| `fixreq-0-sd4-3-02f1aabe34` | `blocking_warning` | ❌ | ✅ | Variable 'LNG_Pmax' is read but never written by any action or transition effect.; Variable 'DG1_Pmax' is read but never written by any action or transition effect.; Variable 'total_thermal_Pmax' is read but never writte...<truncated 37 chars> | `W_GUARD_VARS_NEVER_CHANGE` |
| `fixreq-0-sd4-4-92d1571f27` | `blocking_warning` | ❌ | ✅ | Variable 'LNG_Pmax' is read but never written by any action or transition effect.; Variable 'DG1_Pmax' is read but never written by any action or transition effect.; Variable 'total_thermal_Pmax' is read but never writte...<truncated 37 chars> | `W_GUARD_VARS_NEVER_CHANGE` |
| `fixreq-0-sd4-5-4c60938a12` | `blocking_warning` | ❌ | ✅ | Variable 'LNG_Pmax' is read but never written by any action or transition effect.; Variable 'DG1_Pmax' is read but never written by any action or transition effect.; Variable 'total_thermal_Pmax' is read but never writte...<truncated 37 chars> | `W_GUARD_VARS_NEVER_CHANGE` |
| `fixreq-0-sd4-6-4e2c440a32` | `blocking_warning` | ❌ | ✅ | Variable 'LNG_Pmax' is read but never written by any action or transition effect.; Variable 'DG1_Pmax' is read but never written by any action or transition effect.; Variable 'total_thermal_Pmax' is read but never writte...<truncated 37 chars> | `W_GUARD_VARS_NEVER_CHANGE` |
| `fixreq-0-sd4-7-db659ddafa` | `blocking_warning` | ❌ | ✅ | Variable 'LNG_Pmax' is read but never written by any action or transition effect.; Variable 'DG1_Pmax' is read but never written by any action or transition effect.; Variable 'total_thermal_Pmax' is read but never writte...<truncated 37 chars> | `W_GUARD_VARS_NEVER_CHANGE` |
| `fixreq-0-sd4-8-520348d75c` | `blocking_warning` | ❌ | ✅ | Variable 'LNG_Pmax' is read but never written by any action or transition effect.; Variable 'DG1_Pmax' is read but never written by any action or transition effect.; Variable 'total_thermal_Pmax' is read but never writte...<truncated 37 chars> | `W_GUARD_VARS_NEVER_CHANGE` |
| `fixreq-0-sd4-9-08d36a19d4` | `blocking_warning` | ❌ | ✅ | Variable 'LNG_Pmax' is read but never written by any action or transition effect.; Variable 'DG1_Pmax' is read but never written by any action or transition effect.; Variable 'total_thermal_Pmax' is read but never writte...<truncated 37 chars> | `W_GUARD_VARS_NEVER_CHANGE` |
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
- required_preserve_element_ids：`state:ZeroLoadCharge, state:ZeroLoadSpare, state:RESCharge, state:RESSpare, state:BatteryDischarge, state:LNGChargeMargin, state:LNGNormal, state:DG3LNG, state:DG1AssistCharge, state:DG2AssistCharge, state:AllThermalBattery, state:IllegalOverloadCompletion, ... +18`。

#### SL-9 per-request 决策

- accepted_request_ids：`<derived-from-table>`；candidate_len=`5736`。

| request_id | decision | waiver | rework_locked | rationale / intent |
|---|---|---:|---:|---|
| `fixreq-0-sd4-0-5a3703670c` | `reject` | ✅ | ❌ | LNG_Pmax is an NL-grounded external engine/capacity input read by the EMS. The NL gives no internal update law for it, so adding a write would invent plant/environment dynamics or a meaningless self-assignment. |
| `fixreq-0-sd4-1-fb9af9e195` | `reject` | ✅ | ❌ | DG1_Pmax is an external diesel-generator capacity input. The model should read it as part of dispatch selection; no NL-grounded internal update is specified. |
| `fixreq-0-sd4-2-e1d447c2cf` | `accept` | ❌ | ❌ | total_thermal_Pmax can be treated as an internal aggregate derived from thermal capacity inputs. Adding a grounded recalculation is meaningful and avoids a stale initialized aggregate.；intent=Add root enter and composite during-before actions to compute total_thermal_Pmax from LNG, eng3, DG1, and DG2 capacity inputs. |
| `fixreq-0-sd4-3-02f1aabe34` | `reject` | ✅ | ❌ | The LNGChargeMargin guard is intentionally driven by external load, renewable, SoC, and capacity inputs. No safe internal write is specified for those inputs. |
| `fixreq-0-sd4-4-92d1571f27` | `reject` | ✅ | ❌ | The LNGNormal guard depends on external demand/resource/SoC/capacity inputs. Rewriting or deleting it would break required dispatch-state selection. |
| `fixreq-0-sd4-5-4c60938a12` | `reject` | ✅ | ❌ | The DG3LNG guard is based on external demand, renewable contributions, and capacity bounds including eng3_Pmax. No NL-grounded internal update exists. |
| `fixreq-0-sd4-6-4e2c440a32` | `reject` | ✅ | ❌ | The DG1AssistCharge guard preserves the required low-SoC diesel-assist margin branch and is controlled by external inputs/capacity bounds. Inventing writes would be unsafe. |
| `fixreq-0-sd4-7-db659ddafa` | `accept` | ❌ | ❌ | The DG2AssistCharge guard reads total_thermal_Pmax. Making total_thermal_Pmax a computed internal aggregate gives this guard a meaningful written variable while preserving the external capacity inputs.；intent=Recalculate total_thermal_Pmax from thermal capacity inputs before descendant during actions. |
| `fixreq-0-sd4-8-520348d75c` | `accept` | ❌ | ❌ | The AllThermalBattery guard uses total_thermal_Pmax for the all-thermal capacity threshold. Computing that aggregate is NL-grounded by the all-thermal-resource requirement.；intent=Add a meaningful write to total_thermal_Pmax as the sum of available thermal unit capacities. |
| `fixreq-0-sd4-9-08d36a19d4` | `accept` | ❌ | ❌ | The IllegalOverloadCompletion guard also uses total_thermal_Pmax. Recomputing the aggregate addresses the stale internal aggregate without removing the required illegal state.；intent=Compute total_thermal_Pmax from thermal capacity inputs. |
| `fixreq-0-sd4-10-0e1b524be7` | `reject` | ✅ | ❌ | This transition is governed by external demand, renewable, SoC, and LNG/Pgmax capacity inputs. The NL requires dynamic selection from those inputs but provides no internal update law. |
| `fixreq-0-sd4-11-61dfd1c6a0` | `reject` | ✅ | ❌ | This LNGNormal guard is an external-input dispatch guard. Simplifying or adding dummy writes would reduce NL fidelity. |
- repair_rationale：Preserved all twelve required states, forced selection guards, SoC threshold guards, and dispatch output actions.；Did not invent writes for external inputs PL, Ppv, Pw, SoC, LNG_Pmax, DG1_Pmax, or other capacity/load variables.；Added only a grounded internal aggregate update for total_thermal_Pmax, matching the NL requirement that overload branches compare demand against all thermal resources.；Used composite aspect syntax valid for pyfcstm rather than plain composite during.
- diff_summary：`{"summary": "Added LNGShipEMS root enter and >> during before actions that compute total_thermal_Pmax = LNG_Pmax + eng3_Pmax + DG1_Pmax + DG2_Pmax; no states, guards, or dispatch actions were deleted."}`。

#### SL-9 candidate / 最终修改执行方案

```pyfcstm
def float PL = 0.0;
def float Ppv = 0.0;
def float Pw = 0.0;
def float SoC = 0.0;
def float eng3_Pmax = 0.0;
def float Pgmax = 0.0;
def float Pd1max = 0.0;
def float LNG_Pmax = 0.0;
def float DG1_Pmax = 0.0;
def float DG2_Pmax = 0.0;
def float DG3_Pmax = 0.0;
def float total_thermal_Pmax = 0.0;
def float requested_generator_power = 0.0;
def float battery_discharge_power = 0.0;
def float battery_charge_power = 0.0;
def float spare_power = 0.0;
def int cut_in_command = 0;
def int cut_out_command = 0;

state LNGShipEMS {
    enter {
        total_thermal_Pmax = LNG_Pmax + eng3_Pmax + DG1_Pmax + DG2_Pmax;
    }

    >> during before {
        total_thermal_Pmax = LNG_Pmax + eng3_Pmax + DG1_Pmax + DG2_Pmax;
    }

    ! * -> ZeroLoadCharge : if [PL == 0.0 && Ppv + Pw > 0.0 && SoC < 0.95];
    ! * -> ZeroLoadSpare : if [PL == 0.0 && Ppv + Pw > 0.0 && SoC >= 0.95];
    ! * -> RESCharge : if [PL > 0.0 && Ppv + Pw >= PL && SoC < 0.95];
    ! * -> RESSpare : if [PL > 0.0 && Ppv + Pw >= PL && SoC >= 0.95];
    ! * -> BatteryDischarge : if [PL > 0.0 && Ppv + Pw < PL && SoC > 0.2 && PL - Ppv - Pw <= Pgmax];
    ! * -> LNGChargeMargin : if [PL > 0.0 && Ppv + Pw < PL && SoC <= 0.2 && PL - Ppv - Pw + Pgmax / 5.0 <= LNG_Pmax];
    ! * -> LNGNormal : if [PL > 0.0 && Ppv + Pw < PL && SoC > 0.2 && PL - Ppv - Pw <= LNG_Pmax];
    ! * -> DG3LNG : if [PL > 0.0 && Ppv + Pw < PL && PL - Ppv - Pw > LNG_Pmax && PL - Ppv - Pw <= LNG_Pmax + eng3_Pmax];
    ! * -> DG1AssistCharge : if [PL > 0.0 && Ppv + Pw < PL && SoC <= 0.2 && PL - Ppv - Pw > LNG_Pmax + eng3_Pmax && PL - Ppv - Pw + Pd1max / 10.0 <= LNG_Pmax + eng3_Pmax + DG1_Pmax];
    ! * -> DG2AssistCharge : if [PL > 0.0 && Ppv + Pw < PL && SoC <= 0.2 && PL - Ppv - Pw > LNG_Pmax + eng3_Pmax + DG1_Pmax && PL - Ppv - Pw + Pd1max / 10.0 <= total_thermal_Pmax];
    ! * -> AllThermalBattery : if [PL > 0.0 && Ppv + Pw < PL && PL - Ppv - Pw > total_thermal_Pmax && SoC > 0.0];
    ! * -> IllegalOverloadCompletion : if [PL > 0.0 && Ppv + Pw < PL && PL - Ppv - Pw > total_thermal_Pmax && SoC <= 0.0];

    [*] -> ZeroLoadCharge;

    state ZeroLoadCharge {
        enter {
            requested_generator_power = 0.0;
            battery_discharge_power = 0.0;
            battery_charge_power = Ppv + Pw;
            spare_power = 0.0;
            cut_in_command = 0;
            cut_out_command = 1;
        }
    }

    state ZeroLoadSpare {
        enter {
            requested_generator_power = 0.0;
            battery_discharge_power = 0.0;
            battery_charge_power = 0.0;
            spare_power = Ppv + Pw;
            cut_in_command = 0;
            cut_out_command = 1;
        }
    }

    state RESCharge {
        enter {
            requested_generator_power = 0.0;
            battery_discharge_power = 0.0;
            battery_charge_power = Ppv + Pw - PL;
            spare_power = 0.0;
            cut_in_command = 0;
            cut_out_command = 1;
        }
    }

    state RESSpare {
        enter {
            requested_generator_power = 0.0;
            battery_discharge_power = 0.0;
            battery_charge_power = 0.0;
            spare_power = Ppv + Pw - PL;
            cut_in_command = 0;
            cut_out_command = 1;
        }
    }

    state BatteryDischarge {
        enter {
            requested_generator_power = 0.0;
            battery_discharge_power = PL - Ppv - Pw;
            battery_charge_power = 0.0;
            spare_power = 0.0;
            cut_in_command = 0;
            cut_out_command = 1;
        }
    }

    state LNGChargeMargin {
        enter {
            requested_generator_power = PL - Ppv - Pw + Pgmax / 5.0;
            battery_discharge_power = 0.0;
            battery_charge_power = Pgmax / 5.0;
            spare_power = 0.0;
            cut_in_command = 1;
            cut_out_command = 0;
        }
    }

    state LNGNormal {
        enter {
            requested_generator_power = PL - Ppv - Pw;
            battery_discharge_power = 0.0;
            battery_charge_power = 0.0;
            spare_power = 0.0;
            cut_in_command = 1;
            cut_out_command = 0;
        }
    }

    state DG3LNG {
        enter {
            requested_generator_power = PL - Ppv - Pw;
            battery_discharge_power = 0.0;
            battery_charge_power = 0.0;
            spare_power = 0.0;
            cut_in_command = 1;
            cut_out_command = 0;
        }
    }

    state DG1AssistCharge {
        enter {
            requested_generator_power = PL - Ppv - Pw + Pd1max / 10.0;
            battery_discharge_power = 0.0;
            battery_charge_power = Pd1max / 10.0;
            spare_power = 0.0;
            cut_in_command = 1;
            cut_out_command = 0;
        }
    }

    state DG2AssistCharge {
        enter {
            requested_generator_power = PL - Ppv - Pw + Pd1max / 10.0;
            battery_discharge_power = 0.0;
            battery_charge_power = Pd1max / 10.0;
            spare_power = 0.0;
            cut_in_command = 1;
            cut_out_command = 0;
        }
    }

    state AllThermalBattery {
        enter {
            requested_generator_power = total_thermal_Pmax;
            battery_discharge_power = PL - Ppv - Pw - total_thermal_Pmax;
            battery_charge_power = 0.0;
            spare_power = 0.0;
            cut_in_command = 1;
            cut_out_command = 0;
        }
    }

    state IllegalOverloadCompletion {
        enter {
            requested_generator_power = total_thermal_Pmax;
            battery_discharge_power = PL - Ppv - Pw - total_thermal_Pmax;
            battery_charge_power = 0.0;
            spare_power = 0.0;
            cut_in_command = 1;
            cut_out_command = 0;
        }
    }
}
```

#### Candidate diff（before -> candidate）

```diff
--- before.fcstm
+++ candidate.fcstm
@@ -18,6 +18,14 @@
 def int cut_out_command = 0;
 
 state LNGShipEMS {
+    enter {
+        total_thermal_Pmax = LNG_Pmax + eng3_Pmax + DG1_Pmax + DG2_Pmax;
+    }
+
+    >> during before {
+        total_thermal_Pmax = LNG_Pmax + eng3_Pmax + DG1_Pmax + DG2_Pmax;
+    }
+
     ! * -> ZeroLoadCharge : if [PL == 0.0 && Ppv + Pw > 0.0 && SoC < 0.95];
     ! * -> ZeroLoadSpare : if [PL == 0.0 && Ppv + Pw > 0.0 && SoC >= 0.95];
     ! * -> RESCharge : if [PL > 0.0 && Ppv + Pw >= PL && SoC < 0.95];
```

#### SL-10 审查结果

- SL-10 decision=`pass`，ok=`True`，target_resolved=`True`，regression_detected=`False`，drift_risk=`minor`。
- SL-10 review_meta：schema=`SL10RepairReviewOutput.v1`，failure_policy=`fail_closed`，replay_key=`SL-10:sha256:07a63600ee3ac66bfc43c93bda10efde4e748789394e9265435375ab0d049e11`。
  - SL-10 evidence 1: `{"summary": "The accepted SL-9 edits implement the only grounded repairable target: total_thermal_Pmax is now recomputed as LNG_Pmax + eng3_Pmax + DG1_Pmax + DG2_Pmax in the root enter action and in a composite during-before action. This matches the NL requirement that overload/all-thermal branches compare demand against all thermal resources, and it avoids leaving the aggregate at its initialized value."}`
  - SL-10 evidence 2: `{"summary": "All NL-required states, dispatch outputs, SoC threshold guards, zero-load behavior, RES charge/spare behavior, LNG/diesel priority branches, low-SoC charging margins Pgmax/5 and Pd1max/10, AllThermalBattery, and IllegalOverloadCompletion remain present. The DSL diff adds aggregate-update actions only; it does not delete or simplify required states, transitions, guards, or actions."}`
  - SL-10 evidence 3: `{"summary": "The local unresolved W_UNWRITTEN_READ_VAR diagnostics for LNG_Pmax and DG1_Pmax are covered by explicit SL-9 waiver decisions: these are external capacity inputs read by the EMS, and the NL provides no internal update law. Adding dummy writes or invented plant dynamics would violate the request's forbidden edits and reduce NL fidelity."}`
  - SL-10 evidence 4: `{"summary": "The local new diagnostic for DG2_Pmax is not a semantic regression. It arises because the repaired aggregate now correctly includes DG2_Pmax as part of all thermal resources; DG2 is NL-grounded by the references to DGs and DG1/DG2 last-priority operation. DG2_Pmax, like LNG_Pmax and DG1_Pmax, is an external capacity input and should not be internally written without an NL-grounded update law."}`
  - SL-10 evidence 5: `{"summary": "The local missing_required_grounding report for transition:forced_selection_guards is contradicted by the candidate DSL: all twelve forced selection transitions using '! * -> ... : if [...]' are still present and unchanged from the old DSL. This appears to be conservative grounding detection rather than an actual dropped transition obligation."}`
  - SL-10 evidence 6: `{"summary": "The local drift_risk='major' is therefore overridden: the reported issues are either intentionally waived external-input diagnostics or a detector miss on preserved forced transitions. The actual diff is narrowly scoped and NL-grounded, with no detected deletion of required behavior."}`
- local checks evidence：stage=`SD-10`；note=PR-E1 uses local parse/semantic/design/sim checks as SL-10 evidence, not as the final deterministic judge.。
  - local ok=`False`，target_resolved=`False`，regression_detected=`False`，drift_risk=`major`。
  - local_rejection：reason=`design_target_unresolved; new_blocking_design_diagnostic; missing_required_grounding`，rejected_by_stage=`SD-10`。
    - local evidence 1: `design_target_unresolved` {"items": [{"budget_exhausted": false, "budget_remaining": 1, "code": "W_UNWRITTEN_READ_VAR", "instance_key": "W_UNWRITTEN_READ_VAR:var_name=LNG_Pmax", "message": "Variable 'LNG_Pmax' is read but never written by any action or transition effect.", "policy_action": "budgeted_repair", "pyfcstm_severity": "warning", "rationale": "", "refs": {"init_value": "0.0", "read_states": ["LNGShipEMS", "LNGShipEMS.AllThermalBattery", "LNGShipEMS.BatteryDischarge", "LNGShipEMS.DG1AssistCharge", "LNGShipEMS.DG2...<truncated 60449 chars>
    - local evidence 2: `new_blocking_design_diagnostic` {"items": [{"budget_exhausted": false, "budget_remaining": 2, "code": "W_UNWRITTEN_READ_VAR", "instance_key": "W_UNWRITTEN_READ_VAR:var_name=DG2_Pmax", "message": "Variable 'DG2_Pmax' is read but never written by any action or transition effect.", "policy_action": "budgeted_repair", "pyfcstm_severity": "warning", "rationale": "", "refs": {"init_value": "0.0", "read_states": ["LNGShipEMS"], "var_name": "DG2_Pmax"}, "suggested_fix_hints": [{"do_not": ["Do not add a meaningless self-assignment."], ...<truncated 502 chars>
    - local evidence 3: `missing_required_grounding` {"element_ids": ["transition:forced_selection_guards"], "kind": "missing_required_grounding"}

</details>

<details><summary>Repair 2 / iteration `1` / source `SD-4` / accepted=✅</summary>

#### 为什么进入修复

- selected feedback source：`SD-4`；blocking=`True`；pre_scenario=`True`。
- problem_summary：Variable 'LNG_Pmax' is read but never written by any action or transition effect.; Variable 'DG1_Pmax' is read but never written by any action or transition effect.; Variable 'DG2_Pmax' is read but never written by any action or transition effect.
- diagnostic ids：`W_UNWRITTEN_READ_VAR:var_name=LNG_Pmax, W_UNWRITTEN_READ_VAR:var_name=DG1_Pmax, W_UNWRITTEN_READ_VAR:var_name=DG2_Pmax, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.LNGChargeMargin, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.LNGNormal, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.DG3LNG, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.DG1AssistCharge, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadSpare:to_path=LNGShipEMS.LNGChargeMargin, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadSpare:to_path=LNGShipEMS.LNGNormal, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadSpare:to_path=LNGShipEMS.DG3LNG, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadSpare:to_path=LNGShipEMS.DG1AssistCharge, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.RESCharge:to_path=LNGShipEMS.LNGChargeMargin, ... +44`。
- before_dsl_hash：`sha256:69829f7850ab3861fd27c07e16b841ea694987f57aaf5930f68e7a8a7f892b2e`；candidate_dsl_hash：`sha256:3a69e26a9639a55d35ca176ca3f86c259a1ba8364b6eacf68c65c280891258fd`。

#### 错误证据 / diagnostics

- 1. `W_UNWRITTEN_READ_VAR` `W_UNWRITTEN_READ_VAR:var_name=LNG_Pmax` policy=`budgeted_repair`：Variable 'LNG_Pmax' is read but never written by any action or transition effect.；refs=`{"init_value": "0.0", "read_states": ["LNGShipEMS", "LNGShipEMS.AllThermalBattery", "LNGShipEMS.BatteryDischarge", "LNGShipEMS.DG1AssistCharge", "LNGShipEMS.DG2AssistCharge", "LNGShipEMS.DG3LNG", "LNGShipEMS.IllegalOverloadCompletion", "LNGShipEMS.LNGChargeMargin", "LNGShipEMS.LNGNormal", "LNGShipEM...<truncated 118 chars>`
- 2. `W_UNWRITTEN_READ_VAR` `W_UNWRITTEN_READ_VAR:var_name=DG1_Pmax` policy=`budgeted_repair`：Variable 'DG1_Pmax' is read but never written by any action or transition effect.；refs=`{"init_value": "0.0", "read_states": ["LNGShipEMS", "LNGShipEMS.AllThermalBattery", "LNGShipEMS.BatteryDischarge", "LNGShipEMS.DG1AssistCharge", "LNGShipEMS.DG2AssistCharge", "LNGShipEMS.DG3LNG", "LNGShipEMS.IllegalOverloadCompletion", "LNGShipEMS.LNGChargeMargin", "LNGShipEMS.LNGNormal", "LNGShipEM...<truncated 118 chars>`
- 3. `W_UNWRITTEN_READ_VAR` `W_UNWRITTEN_READ_VAR:var_name=DG2_Pmax` policy=`budgeted_repair`：Variable 'DG2_Pmax' is read but never written by any action or transition effect.；refs=`{"init_value": "0.0", "read_states": ["LNGShipEMS"], "var_name": "DG2_Pmax"}`
- 4. `W_GUARD_VARS_NEVER_CHANGE` `W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.LNGChargeMargin` policy=`budgeted_repair`：Transition guard reads only variables that are never changed by actions or effects.；refs=`{"from_path": "LNGShipEMS.ZeroLoadCharge", "guard_vars": ["LNG_Pmax", "PL", "Pgmax", "Ppv", "Pw", "SoC"], "to_path": "LNGShipEMS.LNGChargeMargin"}`
- 5. `W_GUARD_VARS_NEVER_CHANGE` `W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.LNGNormal` policy=`budgeted_repair`：Transition guard reads only variables that are never changed by actions or effects.；refs=`{"from_path": "LNGShipEMS.ZeroLoadCharge", "guard_vars": ["LNG_Pmax", "PL", "Ppv", "Pw", "SoC"], "to_path": "LNGShipEMS.LNGNormal"}`
- 6. `W_GUARD_VARS_NEVER_CHANGE` `W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.DG3LNG` policy=`budgeted_repair`：Transition guard reads only variables that are never changed by actions or effects.；refs=`{"from_path": "LNGShipEMS.ZeroLoadCharge", "guard_vars": ["LNG_Pmax", "PL", "Ppv", "Pw", "eng3_Pmax"], "to_path": "LNGShipEMS.DG3LNG"}`
- 7. `W_GUARD_VARS_NEVER_CHANGE` `W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.DG1AssistCharge` policy=`budgeted_repair`：Transition guard reads only variables that are never changed by actions or effects.；refs=`{"from_path": "LNGShipEMS.ZeroLoadCharge", "guard_vars": ["DG1_Pmax", "LNG_Pmax", "PL", "Pd1max", "Ppv", "Pw", "SoC", "eng3_Pmax"], "to_path": "LNGShipEMS.DG1AssistCharge"}`
- 8. `W_GUARD_VARS_NEVER_CHANGE` `W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadSpare:to_path=LNGShipEMS.LNGChargeMargin` policy=`budgeted_repair`：Transition guard reads only variables that are never changed by actions or effects.；refs=`{"from_path": "LNGShipEMS.ZeroLoadSpare", "guard_vars": ["LNG_Pmax", "PL", "Pgmax", "Ppv", "Pw", "SoC"], "to_path": "LNGShipEMS.LNGChargeMargin"}`
- ……另有 `43` 条 evidence 见 run record。

#### 变量角色与上下文提示

- policy：Advisory only. Do not invent writes for external_input_candidate variables unless NL explicitly gives update semantics; add meaningful NL-grounded writes only for internal state variables.
- source：SD-4 diagnostic refs and generic NL external-input rationale

| Variable | role_hint | nl_token_present | diagnostics |
|---|---|---:|---|
| `DG1_Pmax` | `unknown` | ❌ | `W_UNWRITTEN_READ_VAR, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +8` |
| `DG2_Pmax` | `unknown` | ❌ | `W_UNWRITTEN_READ_VAR` |
| `DG3_Pmax` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_DECLARED_NEVER_USED` |
| `LNG_Pmax` | `unknown` | ❌ | `W_UNWRITTEN_READ_VAR, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +44` |
| `PL` | `external_input_candidate` | ✅ | `W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +104` |
| `Pd1max` | `external_input_candidate` | ✅ | `W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +8` |
| `Pgmax` | `external_input_candidate` | ✅ | `W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +20` |
| `Ppv` | `external_input_candidate` | ✅ | `W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +104` |
| `Pw` | `external_input_candidate` | ✅ | `W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +104` |
| `SoC` | `external_input_candidate` | ✅ | `W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +92` |
| `battery_charge_power` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `battery_discharge_power` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `cut_in_command` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `cut_out_command` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `eng3_Pmax` | `external_input_candidate` | ✅ | `W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +20` |
| `requested_generator_power` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `spare_power` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |

#### SD-8 FixRequestBatch / 修改请求

- batch_id：`fixbatch-1-sha256-74319a5ab0c`；source_stage=`SD-4`；legacy_plan_kind=`FixPlan`；requests=`12`。

| request_id | severity | hard | waiver | problem | evidence |
|---|---|---:|---:|---|---|
| `fixreq-1-sd4-0-51ab52b169` | `blocking_warning` | ❌ | ✅ | Variable 'LNG_Pmax' is read but never written by any action or transition effect.; Variable 'DG1_Pmax' is read but never written by any action or transition effect.; Variable 'DG2_Pmax' is read but never written by any a...<truncated 27 chars> | `W_UNWRITTEN_READ_VAR` |
| `fixreq-1-sd4-1-23a0b3c1fb` | `blocking_warning` | ❌ | ✅ | Variable 'LNG_Pmax' is read but never written by any action or transition effect.; Variable 'DG1_Pmax' is read but never written by any action or transition effect.; Variable 'DG2_Pmax' is read but never written by any a...<truncated 27 chars> | `W_UNWRITTEN_READ_VAR` |
| `fixreq-1-sd4-2-a3718eb9c5` | `blocking_warning` | ❌ | ✅ | Variable 'LNG_Pmax' is read but never written by any action or transition effect.; Variable 'DG1_Pmax' is read but never written by any action or transition effect.; Variable 'DG2_Pmax' is read but never written by any a...<truncated 27 chars> | `W_UNWRITTEN_READ_VAR` |
| `fixreq-1-sd4-3-d8623f9c38` | `blocking_warning` | ❌ | ✅ | Variable 'LNG_Pmax' is read but never written by any action or transition effect.; Variable 'DG1_Pmax' is read but never written by any action or transition effect.; Variable 'DG2_Pmax' is read but never written by any a...<truncated 27 chars> | `W_GUARD_VARS_NEVER_CHANGE` |
| `fixreq-1-sd4-4-ccbdd3e3f3` | `blocking_warning` | ❌ | ✅ | Variable 'LNG_Pmax' is read but never written by any action or transition effect.; Variable 'DG1_Pmax' is read but never written by any action or transition effect.; Variable 'DG2_Pmax' is read but never written by any a...<truncated 27 chars> | `W_GUARD_VARS_NEVER_CHANGE` |
| `fixreq-1-sd4-5-0505c1b735` | `blocking_warning` | ❌ | ✅ | Variable 'LNG_Pmax' is read but never written by any action or transition effect.; Variable 'DG1_Pmax' is read but never written by any action or transition effect.; Variable 'DG2_Pmax' is read but never written by any a...<truncated 27 chars> | `W_GUARD_VARS_NEVER_CHANGE` |
| `fixreq-1-sd4-6-a9ef652319` | `blocking_warning` | ❌ | ✅ | Variable 'LNG_Pmax' is read but never written by any action or transition effect.; Variable 'DG1_Pmax' is read but never written by any action or transition effect.; Variable 'DG2_Pmax' is read but never written by any a...<truncated 27 chars> | `W_GUARD_VARS_NEVER_CHANGE` |
| `fixreq-1-sd4-7-a178c0938d` | `blocking_warning` | ❌ | ✅ | Variable 'LNG_Pmax' is read but never written by any action or transition effect.; Variable 'DG1_Pmax' is read but never written by any action or transition effect.; Variable 'DG2_Pmax' is read but never written by any a...<truncated 27 chars> | `W_GUARD_VARS_NEVER_CHANGE` |
| `fixreq-1-sd4-8-d39be5a665` | `blocking_warning` | ❌ | ✅ | Variable 'LNG_Pmax' is read but never written by any action or transition effect.; Variable 'DG1_Pmax' is read but never written by any action or transition effect.; Variable 'DG2_Pmax' is read but never written by any a...<truncated 27 chars> | `W_GUARD_VARS_NEVER_CHANGE` |
| `fixreq-1-sd4-9-c7fdab2191` | `blocking_warning` | ❌ | ✅ | Variable 'LNG_Pmax' is read but never written by any action or transition effect.; Variable 'DG1_Pmax' is read but never written by any action or transition effect.; Variable 'DG2_Pmax' is read but never written by any a...<truncated 27 chars> | `W_GUARD_VARS_NEVER_CHANGE` |
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
- required_preserve_element_ids：`state:ZeroLoadCharge, state:ZeroLoadSpare, state:RESCharge, state:RESSpare, state:BatteryDischarge, state:LNGChargeMargin, state:LNGNormal, state:DG3LNG, state:DG1AssistCharge, state:DG2AssistCharge, state:AllThermalBattery, state:IllegalOverloadCompletion, ... +18`。

#### SL-9 per-request 决策

- accepted_request_ids：`<derived-from-table>`；candidate_len=`6144`。

| request_id | decision | waiver | rework_locked | rationale / intent |
|---|---|---:|---:|---|
| `fixreq-1-sd4-0-51ab52b169` | `accept` | ❌ | ❌ | LNG_Pmax is an NL-grounded external capacity bound. Instead of inventing plant dynamics, add a bounded-capacity normalization write that only corrects physically invalid negative capacity values and preserves the variable as an external input.；intent=Add NL-grounded nonnegative capacity-bound normalization for LNG_Pmax in root enter and composite during-befo...<truncated 11 chars> |
| `fixreq-1-sd4-1-23a0b3c1fb` | `accept` | ❌ | ❌ | DG1_Pmax is an NL-grounded diesel-generator capacity bound. A minimal nonnegative bound normalization is a meaningful capacity-bound write and avoids a dummy self-assignment.；intent=Add NL-grounded nonnegative capacity-bound normalization for DG1_Pmax in root enter and composite during-before actions. |
| `fixreq-1-sd4-2-a3718eb9c5` | `accept` | ❌ | ❌ | DG2_Pmax is part of the all-thermal aggregate used by overload dispatch. A minimal nonnegative bound normalization is coherent with capacity-bound semantics.；intent=Add NL-grounded nonnegative capacity-bound normalization for DG2_Pmax in root enter and composite during-before actions. |
| `fixreq-1-sd4-3-d8623f9c38` | `accept` | ❌ | ❌ | The LNGChargeMargin guard depends on external demand/resource/SoC inputs and capacity bounds. Preserving the guard is required; the accepted bounded-capacity normalization gives the capacity-bound variable a meaningful write without deleting the guard.；intent=Preserve LNGChargeMargin forced guard and add meaningful capacity-bound normalization writes. |
| `fixreq-1-sd4-4-ccbdd3e3f3` | `accept` | ❌ | ❌ | The LNGNormal guard is required for LNG-priority dispatch. The safe edit is to preserve the guard and add bounded-capacity normalization for LNG_Pmax rather than simplifying external-input logic.；intent=Preserve LNGNormal forced guard and add meaningful capacity-bound normalization writes. |
| `fixreq-1-sd4-5-0505c1b735` | `accept` | ❌ | ❌ | The DG3LNG guard uses LNG and eng3 capacity bounds for the next dispatch priority. The repair keeps the guard and adds meaningful nonnegative normalization for capacity-bound variables.；intent=Preserve DG3LNG forced guard and add meaningful capacity-bound normalization writes. |
| `fixreq-1-sd4-6-a9ef652319` | `accept` | ❌ | ❌ | The DG1AssistCharge guard is NL-required for a low-SoC diesel-assist margin branch. The repair preserves it and adds nonnegative capacity-bound normalization for LNG_Pmax and DG1_Pmax.；intent=Preserve DG1AssistCharge forced guard and add meaningful capacity-bound normalization writes. |
| `fixreq-1-sd4-7-a178c0938d` | `accept` | ❌ | ❌ | The guard is required external-input dispatch selection. The smallest safe repair is to preserve it while adding capacity-bound normalization for LNG_Pmax.；intent=Preserve forced guard and add meaningful capacity-bound normalization writes. |
| `fixreq-1-sd4-8-d39be5a665` | `accept` | ❌ | ❌ | The LNGNormal guard from ZeroLoadSpare is required for dynamic re-selection under changed inputs. The repair preserves it and adds meaningful capacity-bound normalization.；intent=Preserve forced guard and add meaningful capacity-bound normalization writes. |
| `fixreq-1-sd4-9-c7fdab2191` | `accept` | ❌ | ❌ | The DG3LNG guard from ZeroLoadSpare is part of the required priority dispatch selection. The repair preserves it and adds meaningful capacity-bound normalization.；intent=Preserve forced guard and add meaningful capacity-bound normalization writes. |
| `fixreq-1-sd4-10-850c236323` | `accept` | ❌ | ❌ | The DG1AssistCharge guard from ZeroLoadSpare preserves the required later diesel-generator low-SoC margin branch. The edit preserves the guard and adds nonnegative capacity-bound writes.；intent=Preserve forced guard and add meaningful capacity-bound normalization writes. |
| `fixreq-1-sd4-11-a4d12a1c73` | `accept` | ❌ | ❌ | The RESCharge-to-LNGChargeMargin guard is required for re-dispatch when RES no longer covers load and SoC is low. The repair preserves this guard and adds meaningful capacity-bound normalization.；intent=Preserve forced guard and add meaningful capacity-bound normalization writes. |
- repair_rationale：Preserved all twelve NL-required states, forced selection guards, SoC threshold guards, and dispatch output actions.；Added only bounded-capacity normalization writes for LNG_Pmax, DG1_Pmax, and DG2_Pmax; this avoids meaningless self-assignments and does not invent time-varying plant dynamics.；Kept PL, Ppv, Pw, and SoC as external inputs read by the EMS, as required by the NL.；Kept total_thermal_Pmax as an internal aggregate derived from thermal capacity bounds.
- diff_summary：`{"summary": "Added nonnegative capacity-bound normalization for LNG_Pmax, DG1_Pmax, and DG2_Pmax in LNGShipEMS enter and >> during before actions, before recomputing total_thermal_Pmax. No states, forced guards, thresholds, or dispatch actions were removed."}`。

#### SL-9 candidate / 最终修改执行方案

```pyfcstm
def float PL = 0.0;
def float Ppv = 0.0;
def float Pw = 0.0;
def float SoC = 0.0;
def float eng3_Pmax = 0.0;
def float Pgmax = 0.0;
def float Pd1max = 0.0;
def float LNG_Pmax = 0.0;
def float DG1_Pmax = 0.0;
def float DG2_Pmax = 0.0;
def float DG3_Pmax = 0.0;
def float total_thermal_Pmax = 0.0;
def float requested_generator_power = 0.0;
def float battery_discharge_power = 0.0;
def float battery_charge_power = 0.0;
def float spare_power = 0.0;
def int cut_in_command = 0;
def int cut_out_command = 0;

state LNGShipEMS {
    enter {
        if [LNG_Pmax < 0.0] {
            LNG_Pmax = 0.0;
        }
        if [DG1_Pmax < 0.0] {
            DG1_Pmax = 0.0;
        }
        if [DG2_Pmax < 0.0] {
            DG2_Pmax = 0.0;
        }
        total_thermal_Pmax = LNG_Pmax + eng3_Pmax + DG1_Pmax + DG2_Pmax;
    }

    >> during before {
        if [LNG_Pmax < 0.0] {
            LNG_Pmax = 0.0;
        }
        if [DG1_Pmax < 0.0] {
            DG1_Pmax = 0.0;
        }
        if [DG2_Pmax < 0.0] {
            DG2_Pmax = 0.0;
        }
        total_thermal_Pmax = LNG_Pmax + eng3_Pmax + DG1_Pmax + DG2_Pmax;
    }

    ! * -> ZeroLoadCharge : if [PL == 0.0 && Ppv + Pw > 0.0 && SoC < 0.95];
    ! * -> ZeroLoadSpare : if [PL == 0.0 && Ppv + Pw > 0.0 && SoC >= 0.95];
    ! * -> RESCharge : if [PL > 0.0 && Ppv + Pw >= PL && SoC < 0.95];
    ! * -> RESSpare : if [PL > 0.0 && Ppv + Pw >= PL && SoC >= 0.95];
    ! * -> BatteryDischarge : if [PL > 0.0 && Ppv + Pw < PL && SoC > 0.2 && PL - Ppv - Pw <= Pgmax];
    ! * -> LNGChargeMargin : if [PL > 0.0 && Ppv + Pw < PL && SoC <= 0.2 && PL - Ppv - Pw + Pgmax / 5.0 <= LNG_Pmax];
    ! * -> LNGNormal : if [PL > 0.0 && Ppv + Pw < PL && SoC > 0.2 && PL - Ppv - Pw <= LNG_Pmax];
    ! * -> DG3LNG : if [PL > 0.0 && Ppv + Pw < PL && PL - Ppv - Pw > LNG_Pmax && PL - Ppv - Pw <= LNG_Pmax + eng3_Pmax];
    ! * -> DG1AssistCharge : if [PL > 0.0 && Ppv + Pw < PL && SoC <= 0.2 && PL - Ppv - Pw > LNG_Pmax + eng3_Pmax && PL - Ppv - Pw + Pd1max / 10.0 <= LNG_Pmax + eng3_Pmax + DG1_Pmax];
    ! * -> DG2AssistCharge : if [PL > 0.0 && Ppv + Pw < PL && SoC <= 0.2 && PL - Ppv - Pw > LNG_Pmax + eng3_Pmax + DG1_Pmax && PL - Ppv - Pw + Pd1max / 10.0 <= total_thermal_Pmax];
    ! * -> AllThermalBattery : if [PL > 0.0 && Ppv + Pw < PL && PL - Ppv - Pw > total_thermal_Pmax && SoC > 0.0];
    ! * -> IllegalOverloadCompletion : if [PL > 0.0 && Ppv + Pw < PL && PL - Ppv - Pw > total_thermal_Pmax && SoC <= 0.0];

    [*] -> ZeroLoadCharge;

    state ZeroLoadCharge {
        enter {
            requested_generator_power = 0.0;
            battery_discharge_power = 0.0;
            battery_charge_power = Ppv + Pw;
            spare_power = 0.0;
            cut_in_command = 0;
            cut_out_command = 1;
        }
    }

    state ZeroLoadSpare {
        enter {
            requested_generator_power = 0.0;
            battery_discharge_power = 0.0;
            battery_charge_power = 0.0;
            spare_power = Ppv + Pw;
            cut_in_command = 0;
            cut_out_command = 1;
        }
    }

    state RESCharge {
        enter {
            requested_generator_power = 0.0;
            battery_discharge_power = 0.0;
            battery_charge_power = Ppv + Pw - PL;
            spare_power = 0.0;
            cut_in_command = 0;
            cut_out_command = 1;
        }
    }

    state RESSpare {
        enter {
            requested_generator_power = 0.0;
            battery_discharge_power = 0.0;
            battery_charge_power = 0.0;
            spare_power = Ppv + Pw - PL;
            cut_in_command = 0;
            cut_out_command = 1;
        }
    }

    state BatteryDischarge {
        enter {
            requested_generator_power = 0.0;
            battery_discharge_power = PL - Ppv - Pw;
            battery_charge_power = 0.0;
            spare_power = 0.0;
            cut_in_command = 0;
            cut_out_command = 1;
        }
    }

    state LNGChargeMargin {
        enter {
            requested_generator_power = PL - Ppv - Pw + Pgmax / 5.0;
            battery_discharge_power = 0.0;
            battery_charge_power = Pgmax / 5.0;
            spare_power = 0.0;
            cut_in_command = 1;
            cut_out_command = 0;
        }
    }

    state LNGNormal {
        enter {
            requested_generator_power = PL - Ppv - Pw;
            battery_discharge_power = 0.0;
            battery_charge_power = 0.0;
            spare_power = 0.0;
            cut_in_command = 1;
            cut_out_command = 0;
        }
    }

    state DG3LNG {
        enter {
            requested_generator_power = PL - Ppv - Pw;
            battery_discharge_power = 0.0;
            battery_charge_power = 0.0;
            spare_power = 0.0;
            cut_in_command = 1;
            cut_out_command = 0;
        }
    }

    state DG1AssistCharge {
        enter {
            requested_generator_power = PL - Ppv - Pw + Pd1max / 10.0;
            battery_discharge_power = 0.0;
            battery_charge_power = Pd1max / 10.0;
            spare_power = 0.0;
            cut_in_command = 1;
            cut_out_command = 0;
        }
    }

    state DG2AssistCharge {
        enter {
            requested_generator_power = PL - Ppv - Pw + Pd1max / 10.0;
            battery_discharge_power = 0.0;
            battery_charge_power = Pd1max / 10.0;
            spare_power = 0.0;
            cut_in_command = 1;
            cut_out_command = 0;
        }
    }

    state AllThermalBattery {
        enter {
            requested_generator_power = total_thermal_Pmax;
            battery_discharge_power = PL - Ppv - Pw - total_thermal_Pmax;
            battery_charge_power = 0.0;
            spare_power = 0.0;
            cut_in_command = 1;
            cut_out_command = 0;
        }
    }

    state IllegalOverloadCompletion {
        enter {
            requested_generator_power = total_thermal_Pmax;
            battery_discharge_power = PL - Ppv - Pw - total_thermal_Pmax;
            battery_charge_power = 0.0;
            spare_power = 0.0;
            cut_in_command = 1;
            cut_out_command = 0;
        }
    }
}
```

#### Candidate diff（before -> candidate）

```diff
--- before.fcstm
+++ candidate.fcstm
@@ -19,10 +19,28 @@
 
 state LNGShipEMS {
     enter {
+        if [LNG_Pmax < 0.0] {
+            LNG_Pmax = 0.0;
+        }
+        if [DG1_Pmax < 0.0] {
+            DG1_Pmax = 0.0;
+        }
+        if [DG2_Pmax < 0.0] {
+            DG2_Pmax = 0.0;
+        }
         total_thermal_Pmax = LNG_Pmax + eng3_Pmax + DG1_Pmax + DG2_Pmax;
     }
 
     >> during before {
+        if [LNG_Pmax < 0.0] {
+            LNG_Pmax = 0.0;
+        }
+        if [DG1_Pmax < 0.0] {
+            DG1_Pmax = 0.0;
+        }
+        if [DG2_Pmax < 0.0] {
+            DG2_Pmax = 0.0;
+        }
         total_thermal_Pmax = LNG_Pmax + eng3_Pmax + DG1_Pmax + DG2_Pmax;
     }
 
```

#### SL-10 审查结果

- SL-10 decision=`pass`，ok=`True`，target_resolved=`True`，regression_detected=`False`，drift_risk=`minor`。
- SL-10 review_meta：schema=`SL10RepairReviewOutput.v1`，failure_policy=`fail_closed`，replay_key=`SL-10:sha256:478e404479a5c121f591a5d3e0f04460514d4c2700c302dad0b2a8542f37b520`。
  - SL-10 evidence 1: `{"summary": "The current request batch targets W_UNWRITTEN_READ_VAR for LNG_Pmax, DG1_Pmax, and DG2_Pmax and W_GUARD_VARS_NEVER_CHANGE diagnostics involving required dispatch guards. The candidate adds concrete writes for those three capacity-bound variables in LNGShipEMS enter and composite during-before actions by clamping physically invalid negative capacities to 0.0, then recomputes total_thermal_Pmax. This directly addresses the current unwritten-read targets without deleting or simplifying any guard."}`
  - SL-10 evidence 2: `{"summary": "All NL-required structure is preserved: the candidate still declares PL, Ppv, Pw, SoC, eng3_Pmax, Pgmax, Pd1max, LNG_Pmax, DG1_Pmax, DG2_Pmax, total_thermal_Pmax, requested_generator_power, battery_discharge_power, battery_charge_power, spare_power, cut_in_command, and cut_out_command; it still contains all twelve required states; and each state's dispatch output action remains unchanged from the old DSL."}`
  - SL-10 evidence 3: `{"summary": "The forced selection guards required by the NL remain present as twelve unchanged '! * -> ... : if [...]' transitions selecting ZeroLoadCharge, ZeroLoadSpare, RESCharge, RESSpare, BatteryDischarge, LNGChargeMargin, LNGNormal, DG3LNG, DG1AssistCharge, DG2AssistCharge, AllThermalBattery, and IllegalOverloadCompletion based on PL, Ppv, Pw, SoC, capacity, and margin conditions. The SoC < 0.95 and SoC >= 0.95 RES/zero-load thresholds, the Pgmax/5 LNG low-SoC margin, and the Pd1max/10 diesel-assist margin are retained."}`
  - SL-10 evidence 4: `{"summary": "The complete FixLog shows the previous iteration intentionally preserved external-input guards and added total_thermal_Pmax as a grounded internal aggregate. The current candidate builds on that accepted DSL and only adds nonnegative normalization for capacity bounds before the same aggregate calculation. No previously accepted state, transition, guard, or action is removed, so no regression is detected."}`
  - SL-10 evidence 5: `{"summary": "Local deterministic evidence reports failure only for missing_required_grounding on element_id transition:forced_selection_guards, with drift_risk='major'. This is overridden because the DSL text visibly contains the required forced selection mechanism: every dispatch branch is represented by an unchanged forced transition from '*' with the appropriate guard. The local rejection is therefore a grounding-map recognition issue for the aggregate element_id rather than evidence that the NL-required forced selection guards were dropped."}`
  - SL-10 evidence 6: `{"summary": "The added normalization writes introduce minor semantic drift risk because capacity inputs are externally read values, but the edits are bounded to correcting negative capacity bounds to zero and do not invent time-varying plant dynamics for PL, Ppv, Pw, SoC, or capacities. The NL describes these as engine capacity bounds, and nonnegative capacity is consistent with that interpretation."}`
- local checks evidence：stage=`SD-10`；note=PR-E1 uses local parse/semantic/design/sim checks as SL-10 evidence, not as the final deterministic judge.。
  - local ok=`False`，target_resolved=`False`，regression_detected=`False`，drift_risk=`major`。
  - local_rejection：reason=`missing_required_grounding`，rejected_by_stage=`SD-10`。
    - local evidence 1: `missing_required_grounding` {"element_ids": ["transition:forced_selection_guards"], "kind": "missing_required_grounding"}

</details>

<details><summary>Repair 3 / iteration `2` / source `SD-6` / accepted=✅</summary>

#### 为什么进入修复

- selected feedback source：`SD-6`；blocking=`True`；pre_scenario=`False`。
- problem_summary：simulation failed
- diagnostic ids：`illegal_overload_completion_never_selected`。
- before_dsl_hash：`sha256:3a69e26a9639a55d35ca176ca3f86c259a1ba8364b6eacf68c65c280891258fd`；candidate_dsl_hash：`sha256:b9b293c5f1d54546ed6732d6f5f5fe3410841e17490ca551a584eb572de5aa37`。

#### 错误证据 / diagnostics

- 1. `<unknown>` `` policy=``：

#### SD-8 FixRequestBatch / 修改请求

- batch_id：`fixbatch-2-sha256-019672ca0f5`；source_stage=`SD-6`；legacy_plan_kind=`FixPlan`；requests=`1`。

| request_id | severity | hard | waiver | problem | evidence |
|---|---|---:|---:|---|---|
| `fixreq-2-sd6-0-353f1ecda5` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start probes the illegal overload-completion corner: even with extreme demand at empty SoC, NL says the illegal state shall never occur in practice.', 'name': 'illegal_overload_completion_never_selected', 'setup_error': None, 'status': 'fail', 'step_results': [{'_omitted_keys': 1, 'actual_state': 'LNGShipEMS.IllegalOverloadCompletion', 'actual_vars': {'LNG_Pmax': 30.0, 'PL': 120.0, 'Pd1max': 0.0, 'Pgmax': 0.0, 'Ppv': 5.0, 'Pw': 5.0, 'SoC': 0.0, '_omitted_keys': 10, 'eng3_Pmax': 20.0}, 'state_assertion_ok': False, 'status': 'fail', 'step_index': 0, 'step_name': 'stay_out_of_illegal_completion', 'var_assertion_ok': True, 'var_mismatches': {}}]}` |

#### SD-8 legacy fix plan / 修改建议

- recommended_strategy：Use diagnostics as hints; choose the smallest globally consistent repair.；Before returning a candidate, verify every required_preserve_element_id still has a concrete DSL representation.
- forbidden_edits：`Do not delete grounded required elements merely to silence diagnostics., Do not invent internal plant/environment dynamics merely to make external input variables appear written.`。
- required_preserve_element_ids：`state:ZeroLoadCharge, state:ZeroLoadSpare, state:RESCharge, state:RESSpare, state:BatteryDischarge, state:LNGChargeMargin, state:LNGNormal, state:DG3LNG, state:DG1AssistCharge, state:DG2AssistCharge, state:AllThermalBattery, state:IllegalOverloadCompletion, ... +18`。

#### SL-9 per-request 决策

- accepted_request_ids：`<derived-from-table>`；candidate_len=`6075`。

| request_id | decision | waiver | rework_locked | rationale / intent |
|---|---|---:|---:|---|
| `fixreq-2-sd6-0-353f1ecda5` | `accept` | ❌ | ❌ | The simulation evidence shows the model enters IllegalOverloadCompletion for the empty-SoC extreme-demand corner. The NL explicitly says that overload completion is illegal and shall never occur in practice; even when demand exceeds all RES and thermal resources, EMS should activate all thermal generating units and cover the lack by battery discharge. The sm...<truncated 416 chars> |
- repair_rationale：The failing probe has PL - Ppv - Pw greater than total thermal capacity and SoC equal to 0.0. Under the NL, that case should still be handled by activating all thermal units and covering the lack by battery discharge, not by selecting the i...<truncated 24 chars>；All twelve required states, variables, RES/zero-load SoC threshold guards, forced-selection structure, and dispatch output actions are preserved.；The illegal state remains represented as required, but its forced selection guard is impossible, matching the NL statement that the illegal overload completion state shall never occur in practice.
- diff_summary：`{"summary": "Changed the AllThermalBattery forced overload guard to cover all overload cases regardless of SoC, and changed the IllegalOverloadCompletion forced guard to an impossible condition. No required state, variable, RES/zero-load guard, or dispatch output action was deleted."}`。

#### SL-9 candidate / 最终修改执行方案

```pyfcstm
def float PL = 0.0;
def float Ppv = 0.0;
def float Pw = 0.0;
def float SoC = 0.0;
def float eng3_Pmax = 0.0;
def float Pgmax = 0.0;
def float Pd1max = 0.0;
def float LNG_Pmax = 0.0;
def float DG1_Pmax = 0.0;
def float DG2_Pmax = 0.0;
def float DG3_Pmax = 0.0;
def float total_thermal_Pmax = 0.0;
def float requested_generator_power = 0.0;
def float battery_discharge_power = 0.0;
def float battery_charge_power = 0.0;
def float spare_power = 0.0;
def int cut_in_command = 0;
def int cut_out_command = 0;

state LNGShipEMS {
    enter {
        if [LNG_Pmax < 0.0] {
            LNG_Pmax = 0.0;
        }
        if [DG1_Pmax < 0.0] {
            DG1_Pmax = 0.0;
        }
        if [DG2_Pmax < 0.0] {
            DG2_Pmax = 0.0;
        }
        total_thermal_Pmax = LNG_Pmax + eng3_Pmax + DG1_Pmax + DG2_Pmax;
    }

    >> during before {
        if [LNG_Pmax < 0.0] {
            LNG_Pmax = 0.0;
        }
        if [DG1_Pmax < 0.0] {
            DG1_Pmax = 0.0;
        }
        if [DG2_Pmax < 0.0] {
            DG2_Pmax = 0.0;
        }
        total_thermal_Pmax = LNG_Pmax + eng3_Pmax + DG1_Pmax + DG2_Pmax;
    }

    ! * -> ZeroLoadCharge : if [PL == 0.0 && Ppv + Pw > 0.0 && SoC < 0.95];
    ! * -> ZeroLoadSpare : if [PL == 0.0 && Ppv + Pw > 0.0 && SoC >= 0.95];
    ! * -> RESCharge : if [PL > 0.0 && Ppv + Pw >= PL && SoC < 0.95];
    ! * -> RESSpare : if [PL > 0.0 && Ppv + Pw >= PL && SoC >= 0.95];
    ! * -> BatteryDischarge : if [PL > 0.0 && Ppv + Pw < PL && SoC > 0.2 && PL - Ppv - Pw <= Pgmax];
    ! * -> LNGChargeMargin : if [PL > 0.0 && Ppv + Pw < PL && SoC <= 0.2 && PL - Ppv - Pw + Pgmax / 5.0 <= LNG_Pmax];
    ! * -> LNGNormal : if [PL > 0.0 && Ppv + Pw < PL && SoC > 0.2 && PL - Ppv - Pw <= LNG_Pmax];
    ! * -> DG3LNG : if [PL > 0.0 && Ppv + Pw < PL && PL - Ppv - Pw > LNG_Pmax && PL - Ppv - Pw <= LNG_Pmax + eng3_Pmax];
    ! * -> DG1AssistCharge : if [PL > 0.0 && Ppv + Pw < PL && SoC <= 0.2 && PL - Ppv - Pw > LNG_Pmax + eng3_Pmax && PL - Ppv - Pw + Pd1max / 10.0 <= LNG_Pmax + eng3_Pmax + DG1_Pmax];
    ! * -> DG2AssistCharge : if [PL > 0.0 && Ppv + Pw < PL && SoC <= 0.2 && PL - Ppv - Pw > LNG_Pmax + eng3_Pmax + DG1_Pmax && PL - Ppv - Pw + Pd1max / 10.0 <= total_thermal_Pmax];
    ! * -> AllThermalBattery : if [PL > 0.0 && Ppv + Pw < PL && PL - Ppv - Pw > total_thermal_Pmax];
    ! * -> IllegalOverloadCompletion : if [PL < 0.0 && PL >= 0.0];

    [*] -> ZeroLoadCharge;

    state ZeroLoadCharge {
        enter {
            requested_generator_power = 0.0;
            battery_discharge_power = 0.0;
            battery_charge_power = Ppv + Pw;
            spare_power = 0.0;
            cut_in_command = 0;
            cut_out_command = 1;
        }
    }

    state ZeroLoadSpare {
        enter {
            requested_generator_power = 0.0;
            battery_discharge_power = 0.0;
            battery_charge_power = 0.0;
            spare_power = Ppv + Pw;
            cut_in_command = 0;
            cut_out_command = 1;
        }
    }

    state RESCharge {
        enter {
            requested_generator_power = 0.0;
            battery_discharge_power = 0.0;
            battery_charge_power = Ppv + Pw - PL;
            spare_power = 0.0;
            cut_in_command = 0;
            cut_out_command = 1;
        }
    }

    state RESSpare {
        enter {
            requested_generator_power = 0.0;
            battery_discharge_power = 0.0;
            battery_charge_power = 0.0;
            spare_power = Ppv + Pw - PL;
            cut_in_command = 0;
            cut_out_command = 1;
        }
    }

    state BatteryDischarge {
        enter {
            requested_generator_power = 0.0;
            battery_discharge_power = PL - Ppv - Pw;
            battery_charge_power = 0.0;
            spare_power = 0.0;
            cut_in_command = 0;
            cut_out_command = 1;
        }
    }

    state LNGChargeMargin {
        enter {
            requested_generator_power = PL - Ppv - Pw + Pgmax / 5.0;
            battery_discharge_power = 0.0;
            battery_charge_power = Pgmax / 5.0;
            spare_power = 0.0;
            cut_in_command = 1;
            cut_out_command = 0;
        }
    }

    state LNGNormal {
        enter {
            requested_generator_power = PL - Ppv - Pw;
            battery_discharge_power = 0.0;
            battery_charge_power = 0.0;
            spare_power = 0.0;
            cut_in_command = 1;
            cut_out_command = 0;
        }
    }

    state DG3LNG {
        enter {
            requested_generator_power = PL - Ppv - Pw;
            battery_discharge_power = 0.0;
            battery_charge_power = 0.0;
            spare_power = 0.0;
            cut_in_command = 1;
            cut_out_command = 0;
        }
    }

    state DG1AssistCharge {
        enter {
            requested_generator_power = PL - Ppv - Pw + Pd1max / 10.0;
            battery_discharge_power = 0.0;
            battery_charge_power = Pd1max / 10.0;
            spare_power = 0.0;
            cut_in_command = 1;
            cut_out_command = 0;
        }
    }

    state DG2AssistCharge {
        enter {
            requested_generator_power = PL - Ppv - Pw + Pd1max / 10.0;
            battery_discharge_power = 0.0;
            battery_charge_power = Pd1max / 10.0;
            spare_power = 0.0;
            cut_in_command = 1;
            cut_out_command = 0;
        }
    }

    state AllThermalBattery {
        enter {
            requested_generator_power = total_thermal_Pmax;
            battery_discharge_power = PL - Ppv - Pw - total_thermal_Pmax;
            battery_charge_power = 0.0;
            spare_power = 0.0;
            cut_in_command = 1;
            cut_out_command = 0;
        }
    }

    state IllegalOverloadCompletion {
        enter {
            requested_generator_power = total_thermal_Pmax;
            battery_discharge_power = PL - Ppv - Pw - total_thermal_Pmax;
            battery_charge_power = 0.0;
            spare_power = 0.0;
            cut_in_command = 1;
            cut_out_command = 0;
        }
    }
}
```

#### Candidate diff（before -> candidate）

```diff
--- before.fcstm
+++ candidate.fcstm
@@ -54,8 +54,8 @@
     ! * -> DG3LNG : if [PL > 0.0 && Ppv + Pw < PL && PL - Ppv - Pw > LNG_Pmax && PL - Ppv - Pw <= LNG_Pmax + eng3_Pmax];
     ! * -> DG1AssistCharge : if [PL > 0.0 && Ppv + Pw < PL && SoC <= 0.2 && PL - Ppv - Pw > LNG_Pmax + eng3_Pmax && PL - Ppv - Pw + Pd1max / 10.0 <= LNG_Pmax + eng3_Pmax + DG1_Pmax];
     ! * -> DG2AssistCharge : if [PL > 0.0 && Ppv + Pw < PL && SoC <= 0.2 && PL - Ppv - Pw > LNG_Pmax + eng3_Pmax + DG1_Pmax && PL - Ppv - Pw + Pd1max / 10.0 <= total_thermal_Pmax];
-    ! * -> AllThermalBattery : if [PL > 0.0 && Ppv + Pw < PL && PL - Ppv - Pw > total_thermal_Pmax && SoC > 0.0];
-    ! * -> IllegalOverloadCompletion : if [PL > 0.0 && Ppv + Pw < PL && PL - Ppv - Pw > total_thermal_Pmax && SoC <= 0.0];
+    ! * -> AllThermalBattery : if [PL > 0.0 && Ppv + Pw < PL && PL - Ppv - Pw > total_thermal_Pmax];
+    ! * -> IllegalOverloadCompletion : if [PL < 0.0 && PL >= 0.0];
 
     [*] -> ZeroLoadCharge;
 
```

#### SL-10 审查结果

- SL-10 decision=`pass`，ok=`True`，target_resolved=`True`，regression_detected=`False`，drift_risk=`minor`。
- SL-10 review_meta：schema=`SL10RepairReviewOutput.v1`，failure_policy=`fail_closed`，replay_key=`SL-10:sha256:522bc1e5fecfad33cd6a978a97cefa7ca83fadff06eed136e50e7ddc71207b18`。
  - SL-10 evidence 1: `{"summary": "The hard SD-6 simulation target was that the FSM must not select LNGShipEMS.IllegalOverloadCompletion for an extreme overload case with empty SoC. The NL states both that the overload completion state is illegal and shall never occur in practice, and that when demand exceeds all RES and thermal resources the EMS activates all thermal generating units and covers the lack by battery discharge. The candidate directly implements this by removing the SoC > 0.0 restriction from the AllThermalBattery overload guard, so all PL > 0, RES-deficit, deficit > total_thermal_Pmax cases route to AllThermalBattery regardless of SoC."}`
  - SL-10 evidence 2: `{"summary": "The candidate keeps IllegalOverloadCompletion as a concrete required state but changes its forced guard to the impossible condition PL < 0.0 && PL >= 0.0. This preserves the grounded state representation while making it unreachable in normal forced selection, matching the NL statement that the illegal overload-completion state shall never occur in practice."}`
  - SL-10 evidence 3: `{"summary": "The DSL diff is minimal and consistent with SL-9's accepted edit intent: only the AllThermalBattery overload guard and IllegalOverloadCompletion guard changed. No required states, required variables, RES/zero-load SoC threshold guards, low-SoC charging-margin actions, dispatch output actions, or capacity aggregate/normalization actions were deleted."}`
  - SL-10 evidence 4: `{"summary": "The local deterministic check reports rejection reason missing_required_grounding for element transition:forced_selection_guards and assigns major drift risk, but the candidate DSL visibly still contains the forced-selection structure as explicit ! * -> ... guards for all twelve dispatch states. This is the same abstract grounding-label issue previously overridden in the FixLog, not evidence that the forced guards were removed or semantically regressed. The NL and diff therefore justify overriding this local rejection for the next full revalidation pass."}`
  - SL-10 evidence 5: `{"summary": "No new regression is indicated: the requested illegal-overload repair does not weaken renewable coverage behavior, zero-load behavior, LNG-before-diesel priority, DG1/DG2 last-priority branches, Pgmax/5 and Pd1max/10 charging margins, or all-thermal battery-discharge outputs."}`
- local checks evidence：stage=`SD-10`；note=PR-E1 uses local parse/semantic/design/sim checks as SL-10 evidence, not as the final deterministic judge.。
  - local ok=`False`，target_resolved=`False`，regression_detected=`False`，drift_risk=`major`。
  - local_rejection：reason=`missing_required_grounding`，rejected_by_stage=`SD-10`。
    - local evidence 1: `missing_required_grounding` {"element_ids": ["transition:forced_selection_guards"], "kind": "missing_required_grounding"}

</details>

<details><summary>Repair 4 / iteration `3` / source `SL-7` / accepted=❌</summary>

#### 为什么进入修复

- selected feedback source：`SL-7`；blocking=`True`；pre_scenario=`False`。
- problem_summary：model review failed
- diagnostic ids：`0, 1`。
- before_dsl_hash：`sha256:b9b293c5f1d54546ed6732d6f5f5fe3410841e17490ca551a584eb572de5aa37`；candidate_dsl_hash：`sha256:3708738b7eb83639a2f4da79b0735b2fcc58e757e27910342469683c0aaf3cd2`。

#### 错误证据 / diagnostics

- 1. `<unknown>` `` policy=``：Dispatch priority and capacity semantics are only partially faithful: the battery-priority branch is constrained by Pgmax and can be bypassed for suitable SoC, although the NL says batteries are used when SoC is suitable before LNG/diesel priority is applied.
- 2. `<unknown>` `` policy=``：The DSL silently clamps selected external capacity inputs to zero without NL justification, which can mask invalid sensor/capacity data and alter dispatch behavior instead of representing or rejecting unsafe inputs.

#### SD-8 FixRequestBatch / 修改请求

- batch_id：`fixbatch-3-sha256-6be8c93fa32`；source_stage=`SL-7`；legacy_plan_kind=`FixPlan`；requests=`2`。

| request_id | severity | hard | waiver | problem | evidence |
|---|---|---:|---:|---|---|
| `fixreq-3-sl7-0-65d2e7f559` | `review_fail` | ✅ | ❌ | model review failed | `{'category': 'nl_fidelity', 'evidence': ['NL: "When Ppv + Pw is below PL, dispatch follows the stated priority: RES first, batteries when SoC is suitable, LNG before diesel units, and DG1/DG2 only as the last priority."', 'DSL guard: "BatteryDischarge : if [PL > 0.0 && Ppv + Pw < PL && SoC > 0.2 && PL - Ppv - Pw <= Pgmax]"', 'DSL guard: "LNGNormal : if [PL > 0.0 && Ppv + Pw < PL && SoC > 0.2 && PL - Ppv - Pw <= LNG_Pmax]"', 'The NL mentions Pgmax only as a low-SoC charging margin source, not as a battery discharge capacity bound.'], 'severity': 'major', 'summary': 'Dispatch priority and capacity semantics are only partially faithful: the battery-priority branch is constrained by Pgmax and can be bypassed for suitable SoC, although the NL says batteries are used when SoC is suitable before LNG/diesel priority is applied.'}` |
| `fixreq-3-sl7-1-ca4f711799` | `review_fail` | ✅ | ❌ | model review failed | `{'category': 'unsafe_recovery', 'evidence': ['DSL enter/during: "if [LNG_Pmax < 0.0] { LNG_Pmax = 0.0; }"', 'DSL enter/during: "if [DG1_Pmax < 0.0] { DG1_Pmax = 0.0; }"', 'DSL enter/during: "if [DG2_Pmax < 0.0] { DG2_Pmax = 0.0; }"', 'NL does not specify clamping or recovery behavior for negative capacity inputs.'], 'severity': 'major', 'summary': 'The DSL silently clamps selected external capacity inputs to zero without NL justification, which can mask invalid sensor/capacity data and alter dispatch behavior instead of representing or rejecting unsafe inputs.'}` |

#### SD-8 legacy fix plan / 修改建议

- recommended_strategy：Use diagnostics as hints; choose the smallest globally consistent repair.；Before returning a candidate, verify every required_preserve_element_id still has a concrete DSL representation.
- forbidden_edits：`Do not delete grounded required elements merely to silence diagnostics., Do not invent internal plant/environment dynamics merely to make external input variables appear written.`。
- required_preserve_element_ids：`state:ZeroLoadCharge, state:ZeroLoadSpare, state:RESCharge, state:RESSpare, state:BatteryDischarge, state:LNGChargeMargin, state:LNGNormal, state:DG3LNG, state:DG1AssistCharge, state:DG2AssistCharge, state:AllThermalBattery, state:IllegalOverloadCompletion, ... +18`。

#### SL-9 per-request 决策

- accepted_request_ids：`<derived-from-table>`；candidate_len=`5698`。

| request_id | decision | waiver | rework_locked | rationale / intent |
|---|---|---:|---:|---|
| `fixreq-3-sl7-0-65d2e7f559` | `accept` | ❌ | ❌ | The Pgmax bound on the suitable-SoC BatteryDischarge branch is not NL-grounded and allows LNG/diesel branches to bypass the required battery-priority dispatch. The repair removes that bound and makes later thermal dispatch guards low-SoC branches, preserving all twelve states while restoring RES-first, battery-when-suitable, then LNG/diesel priority.；intent=...<truncated 253 chars> |
| `fixreq-3-sl7-1-ca4f711799` | `accept` | ❌ | ❌ | The clamping writes to external capacity inputs are not stated in the NL and can mask unsafe input data. The repair removes the silent negative-capacity normalization while retaining the NL-grounded total_thermal_Pmax aggregate computation from the external capacity bounds.；intent=Remove root enter and during-before clamps that rewrite LNG_Pmax, DG1_Pmax, an...<truncated 103 chars> |
- repair_rationale：Preserved all twelve required states, all required variables, RES and zero-load SoC threshold guards, forced re-selection structure, and dispatch output actions.；Restored battery priority for suitable SoC by making BatteryDischarge cover all nonzero load deficits when SoC > 0.2, without inventing an unsupported battery capacity bound.；Kept LNG/diesel branches for low-SoC dispatch and retained the required Pgmax/5 and Pd1max/10 charging margin behavior.；Removed unsupported silent clamping of external capacity inputs while keeping total_thermal_Pmax as a derived internal aggregate.
- diff_summary：`{"summary": "Removed negative-capacity clamping writes for LNG_Pmax, DG1_Pmax, and DG2_Pmax; kept total_thermal_Pmax recomputation. Removed Pgmax from the suitable-SoC BatteryDischarge guard and constrained LNG/diesel dispatch guards to low-SoC cases so thermal branches do not bypass battery priority. No required state, variable, RES/zero-load guard, forced selection structure, or dispatch output action was deleted."}`。

#### SL-9 candidate / 最终修改执行方案

```pyfcstm
def float PL = 0.0;
def float Ppv = 0.0;
def float Pw = 0.0;
def float SoC = 0.0;
def float eng3_Pmax = 0.0;
def float Pgmax = 0.0;
def float Pd1max = 0.0;
def float LNG_Pmax = 0.0;
def float DG1_Pmax = 0.0;
def float DG2_Pmax = 0.0;
def float DG3_Pmax = 0.0;
def float total_thermal_Pmax = 0.0;
def float requested_generator_power = 0.0;
def float battery_discharge_power = 0.0;
def float battery_charge_power = 0.0;
def float spare_power = 0.0;
def int cut_in_command = 0;
def int cut_out_command = 0;

state LNGShipEMS {
    enter {
        total_thermal_Pmax = LNG_Pmax + eng3_Pmax + DG1_Pmax + DG2_Pmax;
    }

    >> during before {
        total_thermal_Pmax = LNG_Pmax + eng3_Pmax + DG1_Pmax + DG2_Pmax;
    }

    ! * -> ZeroLoadCharge : if [PL == 0.0 && Ppv + Pw > 0.0 && SoC < 0.95];
    ! * -> ZeroLoadSpare : if [PL == 0.0 && Ppv + Pw > 0.0 && SoC >= 0.95];
    ! * -> RESCharge : if [PL > 0.0 && Ppv + Pw >= PL && SoC < 0.95];
    ! * -> RESSpare : if [PL > 0.0 && Ppv + Pw >= PL && SoC >= 0.95];
    ! * -> BatteryDischarge : if [PL > 0.0 && Ppv + Pw < PL && SoC > 0.2];
    ! * -> LNGChargeMargin : if [PL > 0.0 && Ppv + Pw < PL && SoC <= 0.2 && PL - Ppv - Pw + Pgmax / 5.0 <= LNG_Pmax];
    ! * -> LNGNormal : if [PL > 0.0 && Ppv + Pw < PL && SoC <= 0.2 && PL - Ppv - Pw <= LNG_Pmax && PL - Ppv - Pw + Pgmax / 5.0 > LNG_Pmax];
    ! * -> DG3LNG : if [PL > 0.0 && Ppv + Pw < PL && SoC <= 0.2 && PL - Ppv - Pw > LNG_Pmax && PL - Ppv - Pw <= LNG_Pmax + eng3_Pmax];
    ! * -> DG1AssistCharge : if [PL > 0.0 && Ppv + Pw < PL && SoC <= 0.2 && PL - Ppv - Pw > LNG_Pmax + eng3_Pmax && PL - Ppv - Pw + Pd1max / 10.0 <= LNG_Pmax + eng3_Pmax + DG1_Pmax];
    ! * -> DG2AssistCharge : if [PL > 0.0 && Ppv + Pw < PL && SoC <= 0.2 && PL - Ppv - Pw > LNG_Pmax + eng3_Pmax + DG1_Pmax && PL - Ppv - Pw + Pd1max / 10.0 <= total_thermal_Pmax];
    ! * -> AllThermalBattery : if [PL > 0.0 && Ppv + Pw < PL && PL - Ppv - Pw > total_thermal_Pmax];
    ! * -> IllegalOverloadCompletion : if [PL < 0.0 && PL >= 0.0];

    [*] -> ZeroLoadCharge;

    state ZeroLoadCharge {
        enter {
            requested_generator_power = 0.0;
            battery_discharge_power = 0.0;
            battery_charge_power = Ppv + Pw;
            spare_power = 0.0;
            cut_in_command = 0;
            cut_out_command = 1;
        }
    }

    state ZeroLoadSpare {
        enter {
            requested_generator_power = 0.0;
            battery_discharge_power = 0.0;
            battery_charge_power = 0.0;
            spare_power = Ppv + Pw;
            cut_in_command = 0;
            cut_out_command = 1;
        }
    }

    state RESCharge {
        enter {
            requested_generator_power = 0.0;
            battery_discharge_power = 0.0;
            battery_charge_power = Ppv + Pw - PL;
            spare_power = 0.0;
            cut_in_command = 0;
            cut_out_command = 1;
        }
    }

    state RESSpare {
        enter {
            requested_generator_power = 0.0;
            battery_discharge_power = 0.0;
            battery_charge_power = 0.0;
            spare_power = Ppv + Pw - PL;
            cut_in_command = 0;
            cut_out_command = 1;
        }
    }

    state BatteryDischarge {
        enter {
            requested_generator_power = 0.0;
            battery_discharge_power = PL - Ppv - Pw;
            battery_charge_power = 0.0;
            spare_power = 0.0;
            cut_in_command = 0;
            cut_out_command = 1;
        }
    }

    state LNGChargeMargin {
        enter {
            requested_generator_power = PL - Ppv - Pw + Pgmax / 5.0;
            battery_discharge_power = 0.0;
            battery_charge_power = Pgmax / 5.0;
            spare_power = 0.0;
            cut_in_command = 1;
            cut_out_command = 0;
        }
    }

    state LNGNormal {
        enter {
            requested_generator_power = PL - Ppv - Pw;
            battery_discharge_power = 0.0;
            battery_charge_power = 0.0;
            spare_power = 0.0;
            cut_in_command = 1;
            cut_out_command = 0;
        }
    }

    state DG3LNG {
        enter {
            requested_generator_power = PL - Ppv - Pw;
            battery_discharge_power = 0.0;
            battery_charge_power = 0.0;
            spare_power = 0.0;
            cut_in_command = 1;
            cut_out_command = 0;
        }
    }

    state DG1AssistCharge {
        enter {
            requested_generator_power = PL - Ppv - Pw + Pd1max / 10.0;
            battery_discharge_power = 0.0;
            battery_charge_power = Pd1max / 10.0;
            spare_power = 0.0;
            cut_in_command = 1;
            cut_out_command = 0;
        }
    }

    state DG2AssistCharge {
        enter {
            requested_generator_power = PL - Ppv - Pw + Pd1max / 10.0;
            battery_discharge_power = 0.0;
            battery_charge_power = Pd1max / 10.0;
            spare_power = 0.0;
            cut_in_command = 1;
            cut_out_command = 0;
        }
    }

    state AllThermalBattery {
        enter {
            requested_generator_power = total_thermal_Pmax;
            battery_discharge_power = PL - Ppv - Pw - total_thermal_Pmax;
            battery_charge_power = 0.0;
            spare_power = 0.0;
            cut_in_command = 1;
            cut_out_command = 0;
        }
    }

    state IllegalOverloadCompletion {
        enter {
            requested_generator_power = total_thermal_Pmax;
            battery_discharge_power = PL - Ppv - Pw - total_thermal_Pmax;
            battery_charge_power = 0.0;
            spare_power = 0.0;
            cut_in_command = 1;
            cut_out_command = 0;
        }
    }
}
```

#### Candidate diff（before -> candidate）

```diff
--- before.fcstm
+++ candidate.fcstm
@@ -19,28 +19,10 @@
 
 state LNGShipEMS {
     enter {
-        if [LNG_Pmax < 0.0] {
-            LNG_Pmax = 0.0;
-        }
-        if [DG1_Pmax < 0.0] {
-            DG1_Pmax = 0.0;
-        }
-        if [DG2_Pmax < 0.0] {
-            DG2_Pmax = 0.0;
-        }
         total_thermal_Pmax = LNG_Pmax + eng3_Pmax + DG1_Pmax + DG2_Pmax;
     }
 
     >> during before {
-        if [LNG_Pmax < 0.0] {
-            LNG_Pmax = 0.0;
-        }
-        if [DG1_Pmax < 0.0] {
-            DG1_Pmax = 0.0;
-        }
-        if [DG2_Pmax < 0.0] {
-            DG2_Pmax = 0.0;
-        }
         total_thermal_Pmax = LNG_Pmax + eng3_Pmax + DG1_Pmax + DG2_Pmax;
     }
 
@@ -48,10 +30,10 @@
     ! * -> ZeroLoadSpare : if [PL == 0.0 && Ppv + Pw > 0.0 && SoC >= 0.95];
     ! * -> RESCharge : if [PL > 0.0 && Ppv + Pw >= PL && SoC < 0.95];
     ! * -> RESSpare : if [PL > 0.0 && Ppv + Pw >= PL && SoC >= 0.95];
-    ! * -> BatteryDischarge : if [PL > 0.0 && Ppv + Pw < PL && SoC > 0.2 && PL - Ppv - Pw <= Pgmax];
+    ! * -> BatteryDischarge : if [PL > 0.0 && Ppv + Pw < PL && SoC > 0.2];
     ! * -> LNGChargeMargin : if [PL > 0.0 && Ppv + Pw < PL && SoC <= 0.2 && PL - Ppv - Pw + Pgmax / 5.0 <= LNG_Pmax];
-    ! * -> LNGNormal : if [PL > 0.0 && Ppv + Pw < PL && SoC > 0.2 && PL - Ppv - Pw <= LNG_Pmax];
-    ! * -> DG3LNG : if [PL > 0.0 && Ppv + Pw < PL && PL - Ppv - Pw > LNG_Pmax && PL - Ppv - Pw <= LNG_Pmax + eng3_Pmax];
+    ! * -> LNGNormal : if [PL > 0.0 && Ppv + Pw < PL && SoC <= 0.2 && PL - Ppv - Pw <= LNG_Pmax && PL - Ppv - Pw + Pgmax / 5.0 > LNG_Pmax];
+    ! * -> DG3LNG : if [PL > 0.0 && Ppv + Pw < PL && SoC <= 0.2 && PL - Ppv - Pw > LNG_Pmax && PL - Ppv - Pw <= LNG_Pmax + eng3_Pmax];
     ! * -> DG1AssistCharge : if [PL > 0.0 && Ppv + Pw < PL && SoC <= 0.2 && PL - Ppv - Pw > LNG_Pmax + eng3_Pmax && PL - Ppv - Pw + Pd1max / 10.0 <= LNG_Pmax + eng3_Pmax + DG1_Pmax];
     ! * -> DG2AssistCharge : if [PL > 0.0 && Ppv + Pw < PL && SoC <= 0.2 && PL - Ppv - Pw > LNG_Pmax + eng3_Pmax + DG1_Pmax && PL - Ppv - Pw + Pd1max / 10.0 <= total_thermal_Pmax];
     ! * -> AllThermalBattery : if [PL > 0.0 && Ppv + Pw < PL && PL - Ppv - Pw > total_thermal_Pmax];
```

#### SL-10 审查结果

- SL-10 decision=`rework`，ok=`False`，target_resolved=`False`，regression_detected=`True`，drift_risk=`major`。
- SL-10 review_meta：schema=`SL10RepairReviewOutput.v1`，failure_policy=`fail_closed`，replay_key=`SL-10:sha256:6c89b19c07010e6e37a44054ffbd13c2b3aba20734f878adfe24bd46cc8832f3`。
  - SL-10 evidence 1: `{"summary": "The SL-9 edits correctly address the two requested review failures in isolation: the candidate removes the unsupported Pgmax limit from the suitable-SoC BatteryDischarge guard, constrains ordinary LNG/diesel branches to low-SoC dispatch, and removes the NL-unsupported negative-capacity clamping writes for LNG_Pmax, DG1_Pmax, and DG2_Pmax while preserving total_thermal_Pmax."}`
  - SL-10 evidence 2: `{"summary": "However, the candidate introduces a blocking overlap/regression against the NL overload obligation. BatteryDischarge now fires for every nonzero RES deficit when SoC > 0.2, including extreme cases where PL - Ppv - Pw exceeds total_thermal_Pmax. The NL specifically states that if extreme demand exceeds all RES and thermal resources, EMS activates all thermal generating units and covers the lack by battery discharge. That scenario must select AllThermalBattery, not the pure BatteryDischarge state."}`
  - SL-10 evidence 3: `{"summary": "The local deterministic evidence reports scenario_regression with major drift. This is not merely the previously waived conservative missing_required_grounding diagnostic: it is new regression evidence and is consistent with the candidate guard broadening. Therefore the candidate cannot be accepted for the next full top-down revalidation pass."}`
  - SL-10 evidence 4: `{"summary": "The local W_UNWRITTEN_READ_VAR diagnostic for DG2_Pmax should not be repaired by restoring clamping or adding a meaningless self-assignment, because the NL treats capacity bounds as read inputs and the current batch explicitly removed unsafe clamping. The required rework should preserve DG2_Pmax as a read external capacity input and preserve total_thermal_Pmax as the derived aggregate."}`
- SL-10 rework_instructions：Keep the removal of all negative-capacity clamping writes for LNG_Pmax, DG1_Pmax, and DG2_Pmax. Do not reintroduce clamping and do not add meaningless self-assignments to silence W_UNWRITTEN_READ_VAR.；Preserve total_thermal_Pmax = LNG_Pmax + eng3_Pmax + DG1_Pmax + DG2_Pmax in root enter and during-before actions.；Repair the guard overlap/regression by ensuring AllThermalBattery is selected for every overload case where PL > 0, Ppv + Pw < PL, and PL - Ppv - Pw > total_thermal_Pmax, regardless of SoC.；Constrain the suitable-SoC BatteryDischarge guard so it does not capture the extreme overload region reserved for AllThermalBattery; for example, use PL > 0.0 && Ppv + Pw < PL && SoC > 0.2 && PL - Ppv - Pw <= total_thermal_Pmax, or an equivalent mutually exclusive partition that preserves battery priority for non-overload suitable-SoC deficits.；Preserve all twelve required states, the impossible guard representation for IllegalOverloadCompletion, the RES and zero-load SoC threshold guards, the low-SoC Pgmax/5 and Pd1max/10 charging-margin branches, and all dispatch output actions.
- local checks evidence：stage=`SD-10`；note=PR-E1 uses local parse/semantic/design/sim checks as SL-10 evidence, not as the final deterministic judge.。
  - local ok=`False`，target_resolved=`False`，regression_detected=`True`，drift_risk=`major`。
  - local_rejection：reason=`new_blocking_design_diagnostic; scenario_regression; missing_required_grounding`，rejected_by_stage=`SD-10`。
    - local evidence 1: `new_blocking_design_diagnostic` {"items": [{"budget_exhausted": false, "budget_remaining": 1, "code": "W_UNWRITTEN_READ_VAR", "instance_key": "W_UNWRITTEN_READ_VAR:var_name=DG2_Pmax", "message": "Variable 'DG2_Pmax' is read but never written by any action or transition effect.", "policy_action": "budgeted_repair", "pyfcstm_severity": "warning", "rationale": "", "refs": {"init_value": "0.0", "read_states": ["LNGShipEMS"], "var_name": "DG2_Pmax"}, "suggested_fix_hints": [{"do_not": ["Do not add a meaningless self-assignment."], ...<truncated 502 chars>
    - local evidence 2: `scenario_regression` {"kind": "scenario_regression", "sim_feedback": {"n_scenarios": 19, "n_scenarios_passed": 14, "ok": false, "oracle_weak": false, "scenario_results": [{"description": "default-init dispatches to the initial zero-load RES charging mode when PL=0, RES is available, and SoC is below 0.95.", "name": "default_init_zero_load_charges_battery", "setup_error": null, "status": "pass", "step_results": [{"actual_state": "LNGShipEMS.ZeroLoadCharge", "actual_vars": {"DG1_Pmax": 0.0, "DG2_Pmax": 0.0, "DG3_Pmax"...<truncated 17830 chars>
    - local evidence 3: `missing_required_grounding` {"element_ids": ["transition:forced_selection_guards"], "kind": "missing_required_grounding"}

</details>

<details><summary>Repair 5 / iteration `3` / source `SL-7` / accepted=✅</summary>

#### 为什么进入修复

- selected feedback source：`SL-7`；blocking=`True`；pre_scenario=`False`。
- problem_summary：model review failed
- diagnostic ids：`0, 1`。
- before_dsl_hash：`sha256:b9b293c5f1d54546ed6732d6f5f5fe3410841e17490ca551a584eb572de5aa37`；candidate_dsl_hash：`sha256:e81809b0ae1247aa985b29afeaa805e3220ba9027a7d9bfb28607cf1d7a00998`。

#### 错误证据 / diagnostics

- 1. `<unknown>` `` policy=``：Dispatch priority and capacity semantics are only partially faithful: the battery-priority branch is constrained by Pgmax and can be bypassed for suitable SoC, although the NL says batteries are used when SoC is suitable before LNG/diesel priority is applied.
- 2. `<unknown>` `` policy=``：The DSL silently clamps selected external capacity inputs to zero without NL justification, which can mask invalid sensor/capacity data and alter dispatch behavior instead of representing or rejecting unsafe inputs.

#### SD-8 FixRequestBatch / 修改请求

- batch_id：`fixbatch-3-sha256-6be8c93fa32`；source_stage=`SL-7`；legacy_plan_kind=`FixPlan`；requests=`2`。

| request_id | severity | hard | waiver | problem | evidence |
|---|---|---:|---:|---|---|
| `fixreq-3-sl7-0-65d2e7f559` | `review_fail` | ✅ | ❌ | model review failed | `{'category': 'nl_fidelity', 'evidence': ['NL: "When Ppv + Pw is below PL, dispatch follows the stated priority: RES first, batteries when SoC is suitable, LNG before diesel units, and DG1/DG2 only as the last priority."', 'DSL guard: "BatteryDischarge : if [PL > 0.0 && Ppv + Pw < PL && SoC > 0.2 && PL - Ppv - Pw <= Pgmax]"', 'DSL guard: "LNGNormal : if [PL > 0.0 && Ppv + Pw < PL && SoC > 0.2 && PL - Ppv - Pw <= LNG_Pmax]"', 'The NL mentions Pgmax only as a low-SoC charging margin source, not as a battery discharge capacity bound.'], 'severity': 'major', 'summary': 'Dispatch priority and capacity semantics are only partially faithful: the battery-priority branch is constrained by Pgmax and can be bypassed for suitable SoC, although the NL says batteries are used when SoC is suitable before LNG/diesel priority is applied.'}` |
| `fixreq-3-sl7-1-ca4f711799` | `review_fail` | ✅ | ❌ | model review failed | `{'category': 'unsafe_recovery', 'evidence': ['DSL enter/during: "if [LNG_Pmax < 0.0] { LNG_Pmax = 0.0; }"', 'DSL enter/during: "if [DG1_Pmax < 0.0] { DG1_Pmax = 0.0; }"', 'DSL enter/during: "if [DG2_Pmax < 0.0] { DG2_Pmax = 0.0; }"', 'NL does not specify clamping or recovery behavior for negative capacity inputs.'], 'severity': 'major', 'summary': 'The DSL silently clamps selected external capacity inputs to zero without NL justification, which can mask invalid sensor/capacity data and alter dispatch behavior instead of representing or rejecting unsafe inputs.'}` |

#### SD-8 legacy fix plan / 修改建议

- recommended_strategy：Use diagnostics as hints; choose the smallest globally consistent repair.；Before returning a candidate, verify every required_preserve_element_id still has a concrete DSL representation.
- forbidden_edits：`Do not delete grounded required elements merely to silence diagnostics., Do not invent internal plant/environment dynamics merely to make external input variables appear written.`。
- required_preserve_element_ids：`state:ZeroLoadCharge, state:ZeroLoadSpare, state:RESCharge, state:RESSpare, state:BatteryDischarge, state:LNGChargeMargin, state:LNGNormal, state:DG3LNG, state:DG1AssistCharge, state:DG2AssistCharge, state:AllThermalBattery, state:IllegalOverloadCompletion, ... +18`。

#### SL-9 per-request 决策

- accepted_request_ids：`<derived-from-table>`；candidate_len=`5695`。

| request_id | decision | waiver | rework_locked | rationale / intent |
|---|---|---:|---:|---|
| `fixreq-3-sl7-0-65d2e7f559` | `accept` | ❌ | ✅ | The Pgmax capacity bound on suitable-SoC battery discharge is not NL-grounded and allowed LNG/diesel dispatch to bypass the required battery-priority branch. The repair removes Pgmax from that branch, makes BatteryDischarge exclude only the extreme overload region reserved for AllThermalBattery, and keeps thermal dispatch branches in the low-SoC partition so...<truncated 375 chars> |
| `fixreq-3-sl7-1-ca4f711799` | `accept` | ❌ | ✅ | The negative-capacity clamping writes rewrote external capacity inputs without NL support and could mask unsafe input data. The repair removes those clamps and preserves only the grounded internal aggregate total_thermal_Pmax computation from the external capacity bounds.；intent=Remove root enter and during-before clamps for LNG_Pmax, DG1_Pmax, and DG2_Pmax....<truncated 115 chars> |
- repair_rationale：All twelve required states, required variables, RES/zero-load SoC threshold guards, forced-selection guard structure, and dispatch output actions are preserved.；BatteryDischarge no longer uses the unsupported Pgmax limit; it handles suitable-SoC deficits up to total thermal capacity while leaving extreme overload to AllThermalBattery.；AllThermalBattery remains the selected branch for every overload case where demand deficit exceeds total thermal capacity, regardless of SoC, and IllegalOverloadCompletion remains represented only by an impossible guard.；Unsupported silent clamping of external capacity inputs was removed; total_thermal_Pmax remains an internal aggregate recomputed from capacity inputs.；DG2_Pmax remains an external capacity input read by the EMS. No meaningless self-assignment or ungrounded plant dynamics were added merely to silence an unwritten-read warning.
- diff_summary：`{"summary": "Removed negative-capacity clamping for LNG_Pmax, DG1_Pmax, and DG2_Pmax while preserving total_thermal_Pmax recomputation. Removed Pgmax from the suitable-SoC BatteryDischarge guard and constrained BatteryDischarge to non-overload deficits, leaving all overload deficits to AllThermalBattery. Thermal LNG/diesel branches are low-SoC dispatch branches, with Pgmax/5 and Pd1max/10 charging margins preserved. No required state, variable, RES/zero-load guard, forced-selection structure, impossible IllegalOverloadCompletion representation, or dispatch output action was deleted."}`。

#### SL-9 candidate / 最终修改执行方案

```pyfcstm
def float PL = 0.0;
def float Ppv = 0.0;
def float Pw = 0.0;
def float SoC = 0.0;
def float eng3_Pmax = 0.0;
def float Pgmax = 0.0;
def float Pd1max = 0.0;
def float LNG_Pmax = 0.0;
def float DG1_Pmax = 0.0;
def float DG2_Pmax = 0.0;
def float DG3_Pmax = 0.0;
def float total_thermal_Pmax = 0.0;
def float requested_generator_power = 0.0;
def float battery_discharge_power = 0.0;
def float battery_charge_power = 0.0;
def float spare_power = 0.0;
def int cut_in_command = 0;
def int cut_out_command = 0;

state LNGShipEMS {
    enter {
        total_thermal_Pmax = LNG_Pmax + eng3_Pmax + DG1_Pmax + DG2_Pmax;
    }

    >> during before {
        total_thermal_Pmax = LNG_Pmax + eng3_Pmax + DG1_Pmax + DG2_Pmax;
    }

    ! * -> ZeroLoadCharge : if [PL == 0.0 && Ppv + Pw > 0.0 && SoC < 0.95];
    ! * -> ZeroLoadSpare : if [PL == 0.0 && Ppv + Pw > 0.0 && SoC >= 0.95];
    ! * -> RESCharge : if [PL > 0.0 && Ppv + Pw >= PL && SoC < 0.95];
    ! * -> RESSpare : if [PL > 0.0 && Ppv + Pw >= PL && SoC >= 0.95];
    ! * -> BatteryDischarge : if [PL > 0.0 && Ppv + Pw < PL && SoC > 0.2 && PL - Ppv - Pw <= total_thermal_Pmax];
    ! * -> LNGChargeMargin : if [PL > 0.0 && Ppv + Pw < PL && SoC <= 0.2 && PL - Ppv - Pw + Pgmax / 5.0 <= LNG_Pmax];
    ! * -> LNGNormal : if [PL > 0.0 && Ppv + Pw < PL && SoC <= 0.2 && PL - Ppv - Pw <= LNG_Pmax];
    ! * -> DG3LNG : if [PL > 0.0 && Ppv + Pw < PL && SoC <= 0.2 && PL - Ppv - Pw > LNG_Pmax && PL - Ppv - Pw <= LNG_Pmax + eng3_Pmax];
    ! * -> DG1AssistCharge : if [PL > 0.0 && Ppv + Pw < PL && SoC <= 0.2 && PL - Ppv - Pw > LNG_Pmax + eng3_Pmax && PL - Ppv - Pw + Pd1max / 10.0 <= LNG_Pmax + eng3_Pmax + DG1_Pmax];
    ! * -> DG2AssistCharge : if [PL > 0.0 && Ppv + Pw < PL && SoC <= 0.2 && PL - Ppv - Pw > LNG_Pmax + eng3_Pmax + DG1_Pmax && PL - Ppv - Pw + Pd1max / 10.0 <= total_thermal_Pmax];
    ! * -> AllThermalBattery : if [PL > 0.0 && Ppv + Pw < PL && PL - Ppv - Pw > total_thermal_Pmax];
    ! * -> IllegalOverloadCompletion : if [PL < 0.0 && PL >= 0.0];

    [*] -> ZeroLoadCharge;

    state ZeroLoadCharge {
        enter {
            requested_generator_power = 0.0;
            battery_discharge_power = 0.0;
            battery_charge_power = Ppv + Pw;
            spare_power = 0.0;
            cut_in_command = 0;
            cut_out_command = 1;
        }
    }

    state ZeroLoadSpare {
        enter {
            requested_generator_power = 0.0;
            battery_discharge_power = 0.0;
            battery_charge_power = 0.0;
            spare_power = Ppv + Pw;
            cut_in_command = 0;
            cut_out_command = 1;
        }
    }

    state RESCharge {
        enter {
            requested_generator_power = 0.0;
            battery_discharge_power = 0.0;
            battery_charge_power = Ppv + Pw - PL;
            spare_power = 0.0;
            cut_in_command = 0;
            cut_out_command = 1;
        }
    }

    state RESSpare {
        enter {
            requested_generator_power = 0.0;
            battery_discharge_power = 0.0;
            battery_charge_power = 0.0;
            spare_power = Ppv + Pw - PL;
            cut_in_command = 0;
            cut_out_command = 1;
        }
    }

    state BatteryDischarge {
        enter {
            requested_generator_power = 0.0;
            battery_discharge_power = PL - Ppv - Pw;
            battery_charge_power = 0.0;
            spare_power = 0.0;
            cut_in_command = 0;
            cut_out_command = 1;
        }
    }

    state LNGChargeMargin {
        enter {
            requested_generator_power = PL - Ppv - Pw + Pgmax / 5.0;
            battery_discharge_power = 0.0;
            battery_charge_power = Pgmax / 5.0;
            spare_power = 0.0;
            cut_in_command = 1;
            cut_out_command = 0;
        }
    }

    state LNGNormal {
        enter {
            requested_generator_power = PL - Ppv - Pw;
            battery_discharge_power = 0.0;
            battery_charge_power = 0.0;
            spare_power = 0.0;
            cut_in_command = 1;
            cut_out_command = 0;
        }
    }

    state DG3LNG {
        enter {
            requested_generator_power = PL - Ppv - Pw;
            battery_discharge_power = 0.0;
            battery_charge_power = 0.0;
            spare_power = 0.0;
            cut_in_command = 1;
            cut_out_command = 0;
        }
    }

    state DG1AssistCharge {
        enter {
            requested_generator_power = PL - Ppv - Pw + Pd1max / 10.0;
            battery_discharge_power = 0.0;
            battery_charge_power = Pd1max / 10.0;
            spare_power = 0.0;
            cut_in_command = 1;
            cut_out_command = 0;
        }
    }

    state DG2AssistCharge {
        enter {
            requested_generator_power = PL - Ppv - Pw + Pd1max / 10.0;
            battery_discharge_power = 0.0;
            battery_charge_power = Pd1max / 10.0;
            spare_power = 0.0;
            cut_in_command = 1;
            cut_out_command = 0;
        }
    }

    state AllThermalBattery {
        enter {
            requested_generator_power = total_thermal_Pmax;
            battery_discharge_power = PL - Ppv - Pw - total_thermal_Pmax;
            battery_charge_power = 0.0;
            spare_power = 0.0;
            cut_in_command = 1;
            cut_out_command = 0;
        }
    }

    state IllegalOverloadCompletion {
        enter {
            requested_generator_power = total_thermal_Pmax;
            battery_discharge_power = PL - Ppv - Pw - total_thermal_Pmax;
            battery_charge_power = 0.0;
            spare_power = 0.0;
            cut_in_command = 1;
            cut_out_command = 0;
        }
    }
}
```

#### Candidate diff（before -> candidate）

```diff
--- before.fcstm
+++ candidate.fcstm
@@ -19,28 +19,10 @@
 
 state LNGShipEMS {
     enter {
-        if [LNG_Pmax < 0.0] {
-            LNG_Pmax = 0.0;
-        }
-        if [DG1_Pmax < 0.0] {
-            DG1_Pmax = 0.0;
-        }
-        if [DG2_Pmax < 0.0] {
-            DG2_Pmax = 0.0;
-        }
         total_thermal_Pmax = LNG_Pmax + eng3_Pmax + DG1_Pmax + DG2_Pmax;
     }
 
     >> during before {
-        if [LNG_Pmax < 0.0] {
-            LNG_Pmax = 0.0;
-        }
-        if [DG1_Pmax < 0.0] {
-            DG1_Pmax = 0.0;
-        }
-        if [DG2_Pmax < 0.0] {
-            DG2_Pmax = 0.0;
-        }
         total_thermal_Pmax = LNG_Pmax + eng3_Pmax + DG1_Pmax + DG2_Pmax;
     }
 
@@ -48,10 +30,10 @@
     ! * -> ZeroLoadSpare : if [PL == 0.0 && Ppv + Pw > 0.0 && SoC >= 0.95];
     ! * -> RESCharge : if [PL > 0.0 && Ppv + Pw >= PL && SoC < 0.95];
     ! * -> RESSpare : if [PL > 0.0 && Ppv + Pw >= PL && SoC >= 0.95];
-    ! * -> BatteryDischarge : if [PL > 0.0 && Ppv + Pw < PL && SoC > 0.2 && PL - Ppv - Pw <= Pgmax];
+    ! * -> BatteryDischarge : if [PL > 0.0 && Ppv + Pw < PL && SoC > 0.2 && PL - Ppv - Pw <= total_thermal_Pmax];
     ! * -> LNGChargeMargin : if [PL > 0.0 && Ppv + Pw < PL && SoC <= 0.2 && PL - Ppv - Pw + Pgmax / 5.0 <= LNG_Pmax];
-    ! * -> LNGNormal : if [PL > 0.0 && Ppv + Pw < PL && SoC > 0.2 && PL - Ppv - Pw <= LNG_Pmax];
-    ! * -> DG3LNG : if [PL > 0.0 && Ppv + Pw < PL && PL - Ppv - Pw > LNG_Pmax && PL - Ppv - Pw <= LNG_Pmax + eng3_Pmax];
+    ! * -> LNGNormal : if [PL > 0.0 && Ppv + Pw < PL && SoC <= 0.2 && PL - Ppv - Pw <= LNG_Pmax];
+    ! * -> DG3LNG : if [PL > 0.0 && Ppv + Pw < PL && SoC <= 0.2 && PL - Ppv - Pw > LNG_Pmax && PL - Ppv - Pw <= LNG_Pmax + eng3_Pmax];
     ! * -> DG1AssistCharge : if [PL > 0.0 && Ppv + Pw < PL && SoC <= 0.2 && PL - Ppv - Pw > LNG_Pmax + eng3_Pmax && PL - Ppv - Pw + Pd1max / 10.0 <= LNG_Pmax + eng3_Pmax + DG1_Pmax];
     ! * -> DG2AssistCharge : if [PL > 0.0 && Ppv + Pw < PL && SoC <= 0.2 && PL - Ppv - Pw > LNG_Pmax + eng3_Pmax + DG1_Pmax && PL - Ppv - Pw + Pd1max / 10.0 <= total_thermal_Pmax];
     ! * -> AllThermalBattery : if [PL > 0.0 && Ppv + Pw < PL && PL - Ppv - Pw > total_thermal_Pmax];
```

#### SL-10 审查结果

- SL-10 decision=`pass`，ok=`True`，target_resolved=`True`，regression_detected=`False`，drift_risk=`minor`。
- SL-10 review_meta：schema=`SL10RepairReviewOutput.v1`，failure_policy=`fail_closed`，replay_key=`SL-10:sha256:ae410e0133690ffc69d4773a222c0d0f485c66b0d3b5b47e59184d0862180a31`。
  - SL-10 evidence 1: `{"summary": "The accepted SL-9 rework resolves fixreq-3-sl7-0: the candidate removes the NL-unsupported Pgmax bound from the suitable-SoC BatteryDischarge guard and prevents suitable-SoC battery priority from being bypassed by LNG/diesel branches. BatteryDischarge now covers non-overload deficits when SoC > 0.2, while AllThermalBattery covers deficits greater than total_thermal_Pmax regardless of SoC, matching the NL priority rule and the illegal-overload requirement."}`
  - SL-10 evidence 2: `{"summary": "The accepted SL-9 rework resolves fixreq-3-sl7-1: the candidate removes the unsupported negative-capacity clamping writes for LNG_Pmax, DG1_Pmax, and DG2_Pmax while preserving total_thermal_Pmax = LNG_Pmax + eng3_Pmax + DG1_Pmax + DG2_Pmax as an internal aggregate. This is faithful to the NL, which says the EMS reads capacity bounds but does not authorize rewriting invalid external capacity inputs."}`
  - SL-10 evidence 3: `{"summary": "Required grounded elements are preserved in the candidate: all twelve states remain present, including AllThermalBattery and the represented-but-unreachable IllegalOverloadCompletion; required inputs PL, Ppv, Pw, SoC, eng3_Pmax, Pgmax, Pd1max and dispatch outputs remain declared; RES/zero-load SoC threshold guards, low-SoC Pgmax/5 and Pd1max/10 margin actions, forced-selection structure, and dispatch output enter actions remain represented."}`
  - SL-10 evidence 4: `{"summary": "The local rejection reports W_UNWRITTEN_READ_VAR for DG2_Pmax, but this is not a true NL regression: DG2_Pmax is an external capacity input read by the EMS, and the current batch specifically required removal of artificial writes/clamps to external capacity inputs. Adding a self-assignment or invented plant update would violate the request's forbidden-edits rationale and the SL-10 rework instruction."}`
  - SL-10 evidence 5: `{"summary": "The local missing_required_grounding finding for transition:forced_selection_guards is a persistent conservative grounding issue previously overridden in earlier SL-10 passes, and the DSL still contains explicit forced transitions of the form ! * -> state with guards over PL, Ppv, Pw, SoC, and capacity expressions. The candidate did not delete the forced-selection structure."}`
  - SL-10 evidence 6: `{"summary": "The local scenario_regression finding is not accepted as a substantive NL regression for this repair decision. The candidate implements the locked rework instruction that BatteryDischarge must exclude only the extreme overload region and AllThermalBattery must handle every deficit above total thermal capacity. Remaining scenario evidence is weak/oracle-limited per the scenario summary, while the NL and FixLog support the changed priority semantics."}`
- local checks evidence：stage=`SD-10`；note=PR-E1 uses local parse/semantic/design/sim checks as SL-10 evidence, not as the final deterministic judge.。
  - local ok=`False`，target_resolved=`False`，regression_detected=`True`，drift_risk=`major`。
  - local_rejection：reason=`new_blocking_design_diagnostic; scenario_regression; missing_required_grounding`，rejected_by_stage=`SD-10`。
    - local evidence 1: `new_blocking_design_diagnostic` {"items": [{"budget_exhausted": false, "budget_remaining": 1, "code": "W_UNWRITTEN_READ_VAR", "instance_key": "W_UNWRITTEN_READ_VAR:var_name=DG2_Pmax", "message": "Variable 'DG2_Pmax' is read but never written by any action or transition effect.", "policy_action": "budgeted_repair", "pyfcstm_severity": "warning", "rationale": "", "refs": {"init_value": "0.0", "read_states": ["LNGShipEMS"], "var_name": "DG2_Pmax"}, "suggested_fix_hints": [{"do_not": ["Do not add a meaningless self-assignment."], ...<truncated 502 chars>
    - local evidence 2: `scenario_regression` {"kind": "scenario_regression", "sim_feedback": {"n_scenarios": 19, "n_scenarios_passed": 16, "ok": false, "oracle_weak": false, "scenario_results": [{"description": "default-init dispatches to the initial zero-load RES charging mode when PL=0, RES is available, and SoC is below 0.95.", "name": "default_init_zero_load_charges_battery", "setup_error": null, "status": "pass", "step_results": [{"actual_state": "LNGShipEMS.ZeroLoadCharge", "actual_vars": {"DG1_Pmax": 0.0, "DG2_Pmax": 0.0, "DG3_Pmax"...<truncated 17382 chars>
    - local evidence 3: `missing_required_grounding` {"element_ids": ["transition:forced_selection_guards"], "kind": "missing_required_grounding"}

</details>

<details><summary>Repair 6 / iteration `4` / source `SD-4` / accepted=❌</summary>

#### 为什么进入修复

- selected feedback source：`SD-4`；blocking=`True`；pre_scenario=`False`。
- problem_summary：Variable 'DG2_Pmax' is read but never written by any action or transition effect.
- diagnostic ids：`W_UNWRITTEN_READ_VAR:var_name=DG2_Pmax, W_UNWRITTEN_READ_VAR, W_UNREFERENCED_VAR, W_GUARD_VARS_NEVER_CHANGE, W_VARIABLE_DECLARED_NEVER_USED, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT`。
- before_dsl_hash：`sha256:e81809b0ae1247aa985b29afeaa805e3220ba9027a7d9bfb28607cf1d7a00998`；candidate_dsl_hash：`sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

#### 错误证据 / diagnostics

- 1. `W_UNWRITTEN_READ_VAR` `W_UNWRITTEN_READ_VAR:var_name=DG2_Pmax` policy=`budgeted_repair`：Variable 'DG2_Pmax' is read but never written by any action or transition effect.；refs=`{"init_value": "0.0", "read_states": ["LNGShipEMS"], "var_name": "DG2_Pmax"}`

#### 变量角色与上下文提示

- policy：Advisory only. Do not invent writes for external_input_candidate variables unless NL explicitly gives update semantics; add meaningful NL-grounded writes only for internal state variables.
- source：SD-4 diagnostic refs and generic NL external-input rationale

| Variable | role_hint | nl_token_present | diagnostics |
|---|---|---:|---|
| `DG1_Pmax` | `unknown` | ❌ | `W_UNWRITTEN_READ_VAR, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +8` |
| `DG2_Pmax` | `unknown` | ❌ | `W_UNWRITTEN_READ_VAR` |
| `DG3_Pmax` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_DECLARED_NEVER_USED` |
| `LNG_Pmax` | `unknown` | ❌ | `W_UNWRITTEN_READ_VAR, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +44` |
| `PL` | `external_input_candidate` | ✅ | `W_UNWRITTEN_READ_VAR, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +104` |
| `Pd1max` | `external_input_candidate` | ✅ | `W_UNWRITTEN_READ_VAR, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +8` |
| `Pgmax` | `external_input_candidate` | ✅ | `W_UNWRITTEN_READ_VAR, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +8` |
| `Ppv` | `external_input_candidate` | ✅ | `W_UNWRITTEN_READ_VAR, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +92` |
| `Pw` | `external_input_candidate` | ✅ | `W_UNWRITTEN_READ_VAR, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +92` |
| `SoC` | `external_input_candidate` | ✅ | `W_UNWRITTEN_READ_VAR, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +92` |
| `battery_charge_power` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `battery_discharge_power` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `cut_in_command` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `cut_out_command` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `eng3_Pmax` | `external_input_candidate` | ✅ | `W_UNWRITTEN_READ_VAR, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +20` |
| `requested_generator_power` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `spare_power` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |

#### SD-8 FixRequestBatch / 修改请求

- batch_id：`fixbatch-4-sha256-8d0380f4536`；source_stage=`SD-4`；legacy_plan_kind=`FixPlan`；requests=`1`。

| request_id | severity | hard | waiver | problem | evidence |
|---|---|---:|---:|---|---|
| `fixreq-4-sd4-0-2306b0fbad` | `blocking_warning` | ❌ | ✅ | Variable 'DG2_Pmax' is read but never written by any action or transition effect. | `W_UNWRITTEN_READ_VAR` |

#### SD-8 legacy fix plan / 修改建议

- recommended_strategy：Use diagnostics as hints; choose the smallest globally consistent repair.；Before returning a candidate, verify every required_preserve_element_id still has a concrete DSL representation.
- hint 1：The variable is used as input but never updated after its initial definition, so model behavior may be accidentally constant.；`actions=add_write, simplify_guard；do_not=Do not add a meaningless self-assignment.`
- forbidden_edits：`Do not delete grounded required elements merely to silence diagnostics., Do not invent internal plant/environment dynamics merely to make external input variables appear written.`。
- required_preserve_element_ids：`state:ZeroLoadCharge, state:ZeroLoadSpare, state:RESCharge, state:RESSpare, state:BatteryDischarge, state:LNGChargeMargin, state:LNGNormal, state:DG3LNG, state:DG1AssistCharge, state:DG2AssistCharge, state:AllThermalBattery, state:IllegalOverloadCompletion, ... +18`。

#### SL-9 per-request 决策

- accepted_request_ids：`<derived-from-table>`；candidate_len=`0`。

| request_id | decision | waiver | rework_locked | rationale / intent |
|---|---|---:|---:|---|
| `fixreq-4-sd4-0-2306b0fbad` | `reject` | ✅ | ❌ | DG2_Pmax is used as an external generator capacity input in the NL-grounded dispatch partition for DG2/last-priority thermal capacity. The NL says the FSM reads capacity bounds and does not provide any internal update semantics for DG2_Pmax. Adding a write would either be a meaningless self-assignment or an invented plant/environment dynamic, both forbidden ...<truncated 178 chars> |
- repair_rationale：All requests in the batch were rejected because the only requested fix targets an unwritten-read warning on an external input.；The smallest safe action is to waive the warning rather than add an ungrounded write or remove the required capacity read.；Preserving DG2_Pmax in the total thermal capacity expression is necessary for the NL requirement that DG1/DG2 are last-priority thermal units and for the AllThermalBattery overload partition.
- diff_summary：`{"summary": "No DSL edit applied. DG2_Pmax remains an external capacity input read by forced-selection guards through total_thermal_Pmax; no meaningless self-assignment, clamping, literal replacement, or deletion was introduced."}`。

#### SL-9 candidate / 最终修改执行方案

- 本 repair 未记录 candidate_dsl。

#### Candidate diff（before -> candidate）

- 无 candidate DSL，因此无法生成 diff。

#### SL-10 审查结果

- SL-10：`<none>`（旧 record 或本 run 未进入 LLM repair review）。
- legacy repair_review：ok=`True`，target_resolved=`True`，regression_detected=`False`，drift_risk=`minor`。

</details>


#### FixLog ledger

口径：FixLog 是跨 iteration 的 append-only repair 台账，记录 request batch、SL-9 accept/reject、diff/local evidence、SL-10 批示和下一步动作。

| # | iteration | phase | batch | decisions | next_action | candidate | notes |
|---:|---:|---|---|---|---|---|---|
| 1 | `0` | `request_batch` | `fixbatch-0-sha256-0ec5b2793d7` | accept=0, reject=0 | `sl9_decision_and_repair` | `<none>` | SD-8 produced FixRequestBatch; deterministic stage does not decide final repair. |
| 2 | `0` | `sl9_decision` | `fixbatch-0-sha256-0ec5b2793d7` | accept=4, reject=8 | `sl10_review` | `sha256:69829f7850ab3861fd27c07e16b841ea694987f57aaf5930f68e7a8a7f892b2e` | Preserved all twelve required states, forced selection guards, SoC threshold guards, and dispatch output actions., Did not invent writes for external inputs PL, Ppv, Pw, SoC, LNG_Pmax, DG1_Pmax, or other capacity/load variables., Added only a grounded internal aggregate update for total_thermal_Pmax, matching the NL requirement that overload branches compare demand against all thermal resources., ... +1 |
| 3 | `0` | `sl10_review` | `fixbatch-0-sha256-0ec5b2793d7` | accept=4, reject=8 | `sc11_accept_then_sd2` | `sha256:69829f7850ab3861fd27c07e16b841ea694987f57aaf5930f68e7a8a7f892b2e` | <none> |
| 4 | `1` | `request_batch` | `fixbatch-1-sha256-74319a5ab0c` | accept=0, reject=0 | `sl9_decision_and_repair` | `<none>` | SD-8 produced FixRequestBatch; deterministic stage does not decide final repair. |
| 5 | `1` | `sl9_decision` | `fixbatch-1-sha256-74319a5ab0c` | accept=12, reject=0 | `sl10_review` | `sha256:3a69e26a9639a55d35ca176ca3f86c259a1ba8364b6eacf68c65c280891258fd` | Preserved all twelve NL-required states, forced selection guards, SoC threshold guards, and dispatch output actions., Added only bounded-capacity normalization writes for LNG_Pmax, DG1_Pmax, and DG2_Pmax; this avoids meaningless self-assignments and does not invent time-varying plant dynamics., Kept PL, Ppv, Pw, and SoC as external inputs read by the EMS, as required by the NL., ... +1 |
| 6 | `1` | `sl10_review` | `fixbatch-1-sha256-74319a5ab0c` | accept=12, reject=0 | `sc11_accept_then_sd2` | `sha256:3a69e26a9639a55d35ca176ca3f86c259a1ba8364b6eacf68c65c280891258fd` | <none> |
| 7 | `2` | `request_batch` | `fixbatch-2-sha256-019672ca0f5` | accept=0, reject=0 | `sl9_decision_and_repair` | `<none>` | SD-8 produced FixRequestBatch; deterministic stage does not decide final repair. |
| 8 | `2` | `sl9_decision` | `fixbatch-2-sha256-019672ca0f5` | accept=1, reject=0 | `sl10_review` | `sha256:b9b293c5f1d54546ed6732d6f5f5fe3410841e17490ca551a584eb572de5aa37` | The failing probe has PL - Ppv - Pw greater than total thermal capacity and SoC equal to 0.0. Under the NL, that case should still be handled by activating all thermal units and covering the lack by battery discharge, not by selecting the illegal completion state., All twelve required states, variables, RES/zero-load SoC threshold guards, forced-selection structure, and dispatch output actions are preserved., The illegal state remains represented as required, but its forced selection guard is impossible, matching the NL statement that the illegal overload completion state shall never occur in practice. |
| 9 | `2` | `sl10_review` | `fixbatch-2-sha256-019672ca0f5` | accept=1, reject=0 | `sc11_accept_then_sd2` | `sha256:b9b293c5f1d54546ed6732d6f5f5fe3410841e17490ca551a584eb572de5aa37` | <none> |
| 10 | `3` | `request_batch` | `fixbatch-3-sha256-6be8c93fa32` | accept=0, reject=0 | `sl9_decision_and_repair` | `<none>` | SD-8 produced FixRequestBatch; deterministic stage does not decide final repair. |
| 11 | `3` | `sl9_decision` | `fixbatch-3-sha256-6be8c93fa32` | accept=2, reject=0 | `sl10_review` | `sha256:3708738b7eb83639a2f4da79b0735b2fcc58e757e27910342469683c0aaf3cd2` | Preserved all twelve required states, all required variables, RES and zero-load SoC threshold guards, forced re-selection structure, and dispatch output actions., Restored battery priority for suitable SoC by making BatteryDischarge cover all nonzero load deficits when SoC > 0.2, without inventing an unsupported battery capacity bound., Kept LNG/diesel branches for low-SoC dispatch and retained the required Pgmax/5 and Pd1max/10 charging margin behavior., ... +1 |
| 12 | `3` | `sl10_review` | `fixbatch-3-sha256-6be8c93fa32` | accept=2, reject=0 | `sl9_rework` | `sha256:3708738b7eb83639a2f4da79b0735b2fcc58e757e27910342469683c0aaf3cd2` | Keep the removal of all negative-capacity clamping writes for LNG_Pmax, DG1_Pmax, and DG2_Pmax. Do not reintroduce clamping and do not add meaningless self-assignments to silence W_UNWRITTEN_READ_VAR., Preserve total_thermal_Pmax = LNG_Pmax + eng3_Pmax + DG1_Pmax + DG2_Pmax in root enter and during-before actions., Repair the guard overlap/regression by ensuring AllThermalBattery is selected for every overload case where PL > 0, Ppv + Pw < PL, and PL - Ppv - Pw > total_thermal_Pmax, regardless of SoC., ... +2 |
| 13 | `3` | `sl9_rework_decision` | `fixbatch-3-sha256-6be8c93fa32` | accept=2, reject=0 | `sl10_review` | `sha256:e81809b0ae1247aa985b29afeaa805e3220ba9027a7d9bfb28607cf1d7a00998` | All twelve required states, required variables, RES/zero-load SoC threshold guards, forced-selection guard structure, and dispatch output actions are preserved., BatteryDischarge no longer uses the unsupported Pgmax limit; it handles suitable-SoC deficits up to total thermal capacity while leaving extreme overload to AllThermalBattery., AllThermalBattery remains the selected branch for every overload case where demand deficit exceeds total thermal capacity, regardless of SoC, and IllegalOverloadCompletion remains represented only by an impossible guard., ... +3 |
| 14 | `3` | `sl10_rework_review` | `fixbatch-3-sha256-6be8c93fa32` | accept=2, reject=0 | `sc11_accept_then_sd2` | `sha256:e81809b0ae1247aa985b29afeaa805e3220ba9027a7d9bfb28607cf1d7a00998` | <none> |
| 15 | `4` | `request_batch` | `fixbatch-4-sha256-8d0380f4536` | accept=0, reject=0 | `sl9_decision_and_repair` | `<none>` | SD-8 produced FixRequestBatch; deterministic stage does not decide final repair. |
| 16 | `4` | `sl9_decision` | `fixbatch-4-sha256-8d0380f4536` | accept=0, reject=1 | `reject_or_waiver` | `<none>` | All requests in the batch were rejected because the only requested fix targets an unwritten-read warning on an external input., The smallest safe action is to waive the warning rather than add an ungrounded write or remove the required capacity read., Preserving DG2_Pmax in the total thermal capacity expression is necessary for the NL requirement that DG1/DG2 are last-priority thermal units and for the AllThermalBattery overload partition. |
| 17 | `4` | `sl9_all_rejected` | `fixbatch-4-sha256-8d0380f4536` | accept=0, reject=1 | `continue_after_waiver` | `<none>` | sl9_rejected_all_fix_requests:waiver_continue |

### 8. 尝试记录与成本

- `SL-1`：retry_count=`0`，schema_ok=`True`，usage=`{'completion_tokens': 7863, 'model': 'gpt-5.5', 'prompt_tokens': 9759, 'total_tokens': 17622}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-9`：retry_count=`0`，schema_ok=`True`，usage=`{'completion_tokens': 5287, 'model': 'gpt-5.5', 'prompt_tokens': 35637, 'total_tokens': 40924}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-10`：retry_count=`0`，schema_ok=`True`，usage=`{'completion_tokens': 1011, 'model': 'gpt-5.5', 'prompt_tokens': 29333, 'total_tokens': 30344}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-9`：retry_count=`0`，schema_ok=`True`，usage=`{'completion_tokens': 4587, 'model': 'gpt-5.5', 'prompt_tokens': 39596, 'total_tokens': 44183}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-10`：retry_count=`0`，schema_ok=`True`，usage=`{'completion_tokens': 1015, 'model': 'gpt-5.5', 'prompt_tokens': 33593, 'total_tokens': 34608}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'completion_tokens': 4230, 'model': 'gpt-5.5', 'prompt_tokens': 23685, 'total_tokens': 27915}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'completion_tokens': 4337, 'model': 'gpt-5.5', 'prompt_tokens': 19234, 'total_tokens': 23571}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'completion_tokens': 4818, 'model': 'gpt-5.5', 'prompt_tokens': 19586, 'total_tokens': 24404}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-9`：retry_count=`0`，schema_ok=`True`，usage=`{'completion_tokens': 2846, 'model': 'gpt-5.5', 'prompt_tokens': 21292, 'total_tokens': 24138}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-10`：retry_count=`0`，schema_ok=`True`，usage=`{'completion_tokens': 914, 'model': 'gpt-5.5', 'prompt_tokens': 18111, 'total_tokens': 19025}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'completion_tokens': 5435, 'model': 'gpt-5.5', 'prompt_tokens': 20214, 'total_tokens': 25649}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'completion_tokens': 4735, 'model': 'gpt-5.5', 'prompt_tokens': 20844, 'total_tokens': 25579}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-7`：retry_count=`0`，schema_ok=`True`，usage=`{'completion_tokens': 4203, 'model': 'gpt-5.5', 'prompt_tokens': 68066, 'total_tokens': 72268}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-9`：retry_count=`0`，schema_ok=`True`，usage=`{'completion_tokens': 3022, 'model': 'gpt-5.5', 'prompt_tokens': 22472, 'total_tokens': 25494}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-10`：retry_count=`0`，schema_ok=`True`，usage=`{'completion_tokens': 1508, 'model': 'gpt-5.5', 'prompt_tokens': 17294, 'total_tokens': 18802}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-9`：retry_count=`0`，schema_ok=`True`，usage=`{'completion_tokens': 4286, 'model': 'gpt-5.5', 'prompt_tokens': 34647, 'total_tokens': 38932}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-10`：retry_count=`0`，schema_ok=`True`，usage=`{'completion_tokens': 1164, 'model': 'gpt-5.5', 'prompt_tokens': 18487, 'total_tokens': 19651}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-9`：retry_count=`0`，schema_ok=`True`，usage=`{'completion_tokens': 897, 'model': 'gpt-5.5', 'prompt_tokens': 25206, 'total_tokens': 26103}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。

### 9. 最终停止状态与后续含义

- 停止状态：verdict=`not_converged`，record_status=`budget_exhausted`。
- 主要原因分类：`budget`。
- required stages executed：`56/16`，missing=`<none>`。
- repairs：`4/6` accepted；scenario_history=`6`。
- 配置含义：`recommended baseline candidate`；该结果可用于评估默认入口本身。
- 样本含义：若出现 `design_or_variable_dynamics`，应重点审查变量是否仅作为 guard/input 常量而没有事件/动作更新；若出现 pre-scenario parse/semantic 失败，则应先优化 pyfcstm grammar adherence。
