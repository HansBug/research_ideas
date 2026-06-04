## path2 / state-transitions-logical-design-for-hybrid-energy-generation-with-renewable-energy-sources-in-lng-ship / default 真实运行结果：Path2 LNG-ship EMS representative NL

### 0. 准确边界与结论

- 运行入口：`method.loop.run_agent_loop(nl, LoopConfig(...))`。
- 是否使用 fake / fixture / hot-start / replay：否；本次使用真实默认入口/显式 PR-E1 探索条件，没有 fake、fixture、hot-start 或 replay。
- final verdict：`not_converged`；record_status：`rejected`；result_status：`not_converged`。
- main_result_eligible：`false`。
- 一句话结论：`semantic_or_topology`；停止原因：new_blocking_design_diagnostic; scenario_regression; forced_transition_count_drift; missing_required_grounding。

### 1. 基本信息

| 字段 | 值 |
|---|---|
| Path | `path2` |
| case_id | `state-transitions-logical-design-for-hybrid-energy-generation-with-renewable-energy-sources-in-lng-ship` |
| config_id | `default` |
| 运行入口 | `method.loop.run_agent_loop(nl, LoopConfig(...))` |
| LoopConfig 摘要 | `condition_id=full_staged_v1`, `max_iterations=5`, `llm_max_retries=2`, `scenario_max_retries=2`, `model_review_mode=blocking_major_only`, `delta_review_mode=blocking_major_only` |
| Git commit | `024d87ea7ccf963350683efa08337a26a85c7b1d` |
| clean / diff / prompt snapshot | clean=`True`, dirty=`False`, diff_hash=`sha256:2a69ad5797ac568a81bddcef615104303a97261094685f4edd8d4484e889ea09`, prompt_hash=`sha256:0297eca601185761f335df788fe652c9a55156fa8e8100374f7291bbfc86e10b` |
| provider/model 脱敏标识 | mode=`real_env`, model=`gpt-5.5`, real_api=`True` |
| source / paper | source=`project_1_llm_state_machine_modeling/sources/state-transitions-logical-design-for-hybrid-energy-generation-with-renewable-energy-sources-in-lng-ship`, paper=`project_1_llm_state_machine_modeling/sources/state-transitions-logical-design-for-hybrid-energy-generation-with-renewable-energy-sources-in-lng-ship/paper.pdf` |
| 样本筛选理由 | issue #14 / PR-D 代表性 Path2 EFSM，变量、guard、12 个状态和非法状态都明确。 |
| 变量参与说明 | `PL/Ppv/Pw/SoC/eng*_Pmax` 是环境输入/容量边界，适合暴露 SD-4 对外部输入变量的处理能力。 |
| run_id | `pr-e1-path2_lng_ems-default-round14fullevidenceparallel-a78258a0` |
| final verdict/status | verdict=`not_converged`, record=`rejected`, result=`not_converged` |
| main_result_eligible | `false` |
| token/cost/time | tokens=`{'prompt_tokens': 586211, 'completion_tokens': 47560, 'total_tokens': 633771, 'n_calls': 10}`, elapsed=`2242.674s` |
| run record | [`pr-e1-path2_lng_ems-default-round14fullevidenceparallel-a78258a0.agent_loop.json.gz`](./pr-e1-path2_lng_ems-default-round14fullevidenceparallel-a78258a0.agent_loop.json.gz) |
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
def float Pd2max = 0.0;
def float Pbat_Pmax = 0.0;
def float Pgen_req = 0.0;
def float Pbat_discharge = 0.0;
def float Pbat_charge = 0.0;
def float Pspare = 0.0;
def int cut_in_LNG = 0;
def int cut_in_engine3 = 0;
def int cut_in_DG1 = 0;
def int cut_in_DG2 = 0;
def int cut_in_battery = 0;
def int cut_out_load = 0;

state LNGShipEMS {
    ! * -> IdleNoLoad : if [PL == 0 && Ppv + Pw == 0];
    ! * -> ZeroLoadCharge : if [PL == 0 && Ppv + Pw > 0 && SoC < 0.95];
    ! * -> ZeroLoadSpare : if [PL == 0 && Ppv + Pw > 0 && SoC >= 0.95];
    ! * -> RESCoversCharge : if [PL > 0 && Ppv + Pw >= PL && SoC < 0.95];
    ! * -> RESCoversSpare : if [PL > 0 && Ppv + Pw >= PL && SoC >= 0.95];
    ! * -> BatteryAssist : if [PL > 0 && Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw <= Pbat_Pmax];
    ! * -> LNGCoveredLowSoCChargeMargin : if [PL > 0 && Ppv + Pw < PL && SoC < 0.2 && PL - Ppv - Pw <= Pgmax];
    ! * -> LNGCoveredNormal : if [PL > 0 && Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw > Pbat_Pmax && PL - Ppv - Pw <= Pgmax];
    ! * -> LNGAndEngine3Covered : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > Pgmax && PL - Ppv - Pw <= Pgmax + eng3_Pmax];
    ! * -> DG1LowSoCChargeMargin : if [PL > 0 && Ppv + Pw < PL && SoC < 0.2 && PL - Ppv - Pw > Pgmax + eng3_Pmax && PL - Ppv - Pw + Pd1max / 10 <= Pgmax + eng3_Pmax + Pd1max];
    ! * -> DG1CoveredNormal : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > Pgmax + eng3_Pmax && PL - Ppv - Pw <= Pgmax + eng3_Pmax + Pd1max && (SoC >= 0.2 || PL - Ppv - Pw + Pd1max / 10 > Pgmax + eng3_Pmax + Pd1max)];
    ! * -> DG2Covered : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > Pgmax + eng3_Pmax + Pd1max && PL - Ppv - Pw <= Pgmax + eng3_Pmax + Pd1max + Pd2max];
    ! * -> OverloadCompletionIllegal : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > Pgmax + eng3_Pmax + Pd1max + Pd2max];

    [*] -> IdleNoLoad;

    state IdleNoLoad {
        enter {
            Pgen_req = 0.0;
            Pbat_discharge = 0.0;
            Pbat_charge = 0.0;
            Pspare = 0.0;
            cut_in_LNG = 0;
            cut_in_engine3 = 0;
            cut_in_DG1 = 0;
            cut_in_DG2 = 0;
            cut_in_battery = 0;
            cut_out_load = 0;
        }
    }

    state ZeroLoadCharge {
        enter {
            Pgen_req = 0.0;
            Pbat_discharge = 0.0;
            Pbat_charge = Ppv + Pw;
            Pspare = 0.0;
            cut_in_LNG = 0;
            cut_in_engine3 = 0;
            cut_in_DG1 = 0;
            cut_in_DG2 = 0;
            cut_in_battery = 1;
            cut_out_load = 0;
        }
    }

    state ZeroLoadSpare {
        enter {
            Pgen_req = 0.0;
            Pbat_discharge = 0.0;
            Pbat_charge = 0.0;
            Pspare = Ppv + Pw;
            cut_in_LNG = 0;
            cut_in_engine3 = 0;
            cut_in_DG1 = 0;
            cut_in_DG2 = 0;
            cut_in_battery = 0;
            cut_out_load = 0;
        }
    }

    state RESCoversCharge {
        enter {
            Pgen_req = 0.0;
            Pbat_discharge = 0.0;
            Pbat_charge = Ppv + Pw - PL;
            Pspare = 0.0;
            cut_in_LNG = 0;
            cut_in_engine3 = 0;
            cut_in_DG1 = 0;
            cut_in_DG2 = 0;
            cut_in_battery = 1;
            cut_out_load = 0;
        }
    }

    state RESCoversSpare {
        enter {
            Pgen_req = 0.0;
            Pbat_discharge = 0.0;
            Pbat_charge = 0.0;
            Pspare = Ppv + Pw - PL;
            cut_in_LNG = 0;
            cut_in_engine3 = 0;
            cut_in_DG1 = 0;
            cut_in_DG2 = 0;
            cut_in_battery = 0;
            cut_out_load = 0;
        }
    }

    state BatteryAssist {
        enter {
            Pgen_req = 0.0;
            Pbat_discharge = PL - Ppv - Pw;
            Pbat_charge = 0.0;
            Pspare = 0.0;
            cut_in_LNG = 0;
            cut_in_engine3 = 0;
            cut_in_DG1 = 0;
            cut_in_DG2 = 0;
            cut_in_battery = 1;
            cut_out_load = 0;
        }
    }

    state LNGCoveredLowSoCChargeMargin {
        enter {
            Pgen_req = PL - Ppv - Pw + Pgmax / 5;
            Pbat_discharge = 0.0;
            Pbat_charge = Pgmax / 5;
            Pspare = 0.0;
            cut_in_LNG = 1;
            cut_in_engine3 = 0;
            cut_in_DG1 = 0;
            cut_in_DG2 = 0;
            cut_in_battery = 1;
            cut_out_load = 0;
        }
    }

    state LNGCoveredNormal {
        enter {
            Pgen_req = PL - Ppv - Pw;
            Pbat_discharge = 0.0;
            Pbat_charge = 0.0;
            Pspare = 0.0;
            cut_in_LNG = 1;
            cut_in_engine3 = 0;
            cut_in_DG1 = 0;
            cut_in_DG2 = 0;
            cut_in_battery = 0;
            cut_out_load = 0;
        }
    }

    state LNGAndEngine3Covered {
        enter {
            Pgen_req = PL - Ppv - Pw;
            Pbat_discharge = 0.0;
            Pbat_charge = 0.0;
            Pspare = 0.0;
            cut_in_LNG = 1;
            cut_in_engine3 = 1;
            cut_in_DG1 = 0;
            cut_in_DG2 = 0;
            cut_in_battery = 0;
            cut_out_load = 0;
        }
    }

    state DG1LowSoCChargeMargin {
        enter {
            Pgen_req = PL - Ppv - Pw + Pd1max / 10;
            Pbat_discharge = 0.0;
            Pbat_charge = Pd1max / 10;
            Pspare = 0.0;
            cut_in_LNG = 1;
            cut_in_engine3 = 1;
            cut_in_DG1 = 1;
            cut_in_DG2 = 0;
            cut_in_battery = 1;
            cut_out_load = 0;
        }
    }

    state DG1CoveredNormal {
        enter {
            Pgen_req = PL - Ppv - Pw;
            Pbat_discharge = 0.0;
            Pbat_charge = 0.0;
            Pspare = 0.0;
            cut_in_LNG = 1;
            cut_in_engine3 = 1;
            cut_in_DG1 = 1;
            cut_in_DG2 = 0;
            cut_in_battery = 0;
            cut_out_load = 0;
        }
    }

    state DG2Covered {
        enter {
            Pgen_req = PL - Ppv - Pw;
            Pbat_discharge = 0.0;
            Pbat_charge = 0.0;
            Pspare = 0.0;
            cut_in_LNG = 1;
            cut_in_engine3 = 1;
            cut_in_DG1 = 1;
            cut_in_DG2 = 1;
            cut_in_battery = 0;
            cut_out_load = 0;
        }
    }

    state OverloadCompletionIllegal {
        enter {
            Pgen_req = Pgmax + eng3_Pmax + Pd1max + Pd2max;
            Pbat_discharge = PL - Ppv - Pw - Pgmax - eng3_Pmax - Pd1max - Pd2max;
            Pbat_charge = 0.0;
            Pspare = 0.0;
            cut_in_LNG = 1;
            cut_in_engine3 = 1;
            cut_in_DG1 = 1;
            cut_in_DG2 = 1;
            cut_in_battery = 1;
            cut_out_load = 1;
        }
    }
}
```

### 4. 全流程真实摘要表

| Stage | 是否 LLM | iteration | 结果 | 获取的信息 / 反馈 | 本阶段做了什么 | DSL 修改 | artifact/log |
|---|---:|---:|---:|---|---|---|---|
| `SC-0` | 否 | - | ✅ | trace/control | 初始化 run state | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round14fullevidenceparallel-a78258a0.agent_loop.json.gz) |
| `SL-1` | 是 | - | ✅ | LLM calls=1, tokens=15194 | 生成初始 DSL 与 grounding seeds | initial len=6902 | [`record`](./pr-e1-path2_lng_ems-default-round14fullevidenceparallel-a78258a0.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round14fullevidenceparallel-a78258a0.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round14fullevidenceparallel-a78258a0.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ⚠️ | blocking=54, advisory=135, info=0; blocking=54, advisory=135, info=0; blocking=0, advisory=189, info=0; blocking=0, advisory=189, info=0; blocking=0, advisory=189, info=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round14fullevidenceparallel-a78258a0.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixPlan | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round14fullevidenceparallel-a78258a0.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=5, tokens=431547 | LLM repair candidate | candidate len=7059,6902,6873,7339,7041 | [`record`](./pr-e1-path2_lng_ems-default-round14fullevidenceparallel-a78258a0.agent_loop.json.gz) |
| `SD-10` | 否 | 0 | ⚠️ | ok=False, target_resolved=False, drift=major; ok=False, target_resolved=False, drift=major; ok=False, target_resolved=False, drift=major; ok=False, target_resolved=False, drift=maj | 本地 repair review | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round14fullevidenceparallel-a78258a0.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ⚠️ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round14fullevidenceparallel-a78258a0.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round14fullevidenceparallel-a78258a0.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round14fullevidenceparallel-a78258a0.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ⚠️ | blocking=54, advisory=135, info=0; blocking=54, advisory=135, info=0; blocking=0, advisory=189, info=0; blocking=0, advisory=189, info=0; blocking=0, advisory=189, info=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round14fullevidenceparallel-a78258a0.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixPlan | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round14fullevidenceparallel-a78258a0.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=5, tokens=431547 | LLM repair candidate | candidate len=7059,6902,6873,7339,7041 | [`record`](./pr-e1-path2_lng_ems-default-round14fullevidenceparallel-a78258a0.agent_loop.json.gz) |
| `SD-10` | 否 | 0 | ⚠️ | ok=False, target_resolved=False, drift=major; ok=False, target_resolved=False, drift=major; ok=False, target_resolved=False, drift=major; ok=False, target_resolved=False, drift=maj | 本地 repair review | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round14fullevidenceparallel-a78258a0.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ⚠️ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round14fullevidenceparallel-a78258a0.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round14fullevidenceparallel-a78258a0.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round14fullevidenceparallel-a78258a0.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=54, advisory=135, info=0; blocking=54, advisory=135, info=0; blocking=0, advisory=189, info=0; blocking=0, advisory=189, info=0; blocking=0, advisory=189, info=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round14fullevidenceparallel-a78258a0.agent_loop.json.gz) |
| `SL-5` | 是 | 2 | ✅ | LLM calls=1, tokens=22396 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round14fullevidenceparallel-a78258a0.agent_loop.json.gz) |
| `SD-5A` | 否 | 2 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round14fullevidenceparallel-a78258a0.agent_loop.json.gz) |
| `SC-5F` | 否 | 2 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round14fullevidenceparallel-a78258a0.agent_loop.json.gz) |
| `SD-6` | 否 | 2 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round14fullevidenceparallel-a78258a0.agent_loop.json.gz) |
| `SL-7` | 是 | 2 | ✅ | LLM calls=3, tokens=164634 | LLM model review | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round14fullevidenceparallel-a78258a0.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixPlan | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round14fullevidenceparallel-a78258a0.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=5, tokens=431547 | LLM repair candidate | candidate len=7059,6902,6873,7339,7041 | [`record`](./pr-e1-path2_lng_ems-default-round14fullevidenceparallel-a78258a0.agent_loop.json.gz) |
| `SD-10` | 否 | 0 | ⚠️ | ok=False, target_resolved=False, drift=major; ok=False, target_resolved=False, drift=major; ok=False, target_resolved=False, drift=major; ok=False, target_resolved=False, drift=maj | 本地 repair review | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round14fullevidenceparallel-a78258a0.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ⚠️ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round14fullevidenceparallel-a78258a0.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round14fullevidenceparallel-a78258a0.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round14fullevidenceparallel-a78258a0.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=54, advisory=135, info=0; blocking=54, advisory=135, info=0; blocking=0, advisory=189, info=0; blocking=0, advisory=189, info=0; blocking=0, advisory=189, info=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round14fullevidenceparallel-a78258a0.agent_loop.json.gz) |
| `SD-5A` | 否 | 2 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round14fullevidenceparallel-a78258a0.agent_loop.json.gz) |
| `SC-5F` | 否 | 2 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round14fullevidenceparallel-a78258a0.agent_loop.json.gz) |
| `SD-6` | 否 | 2 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round14fullevidenceparallel-a78258a0.agent_loop.json.gz) |
| `SL-7` | 是 | 2 | ✅ | LLM calls=3, tokens=164634 | LLM model review | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round14fullevidenceparallel-a78258a0.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixPlan | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round14fullevidenceparallel-a78258a0.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=5, tokens=431547 | LLM repair candidate | candidate len=7059,6902,6873,7339,7041 | [`record`](./pr-e1-path2_lng_ems-default-round14fullevidenceparallel-a78258a0.agent_loop.json.gz) |
| `SD-10` | 否 | 0 | ⚠️ | ok=False, target_resolved=False, drift=major; ok=False, target_resolved=False, drift=major; ok=False, target_resolved=False, drift=major; ok=False, target_resolved=False, drift=maj | 本地 repair review | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round14fullevidenceparallel-a78258a0.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ⚠️ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round14fullevidenceparallel-a78258a0.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round14fullevidenceparallel-a78258a0.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round14fullevidenceparallel-a78258a0.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=54, advisory=135, info=0; blocking=54, advisory=135, info=0; blocking=0, advisory=189, info=0; blocking=0, advisory=189, info=0; blocking=0, advisory=189, info=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round14fullevidenceparallel-a78258a0.agent_loop.json.gz) |
| `SD-5A` | 否 | 2 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round14fullevidenceparallel-a78258a0.agent_loop.json.gz) |
| `SC-5F` | 否 | 2 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round14fullevidenceparallel-a78258a0.agent_loop.json.gz) |
| `SD-6` | 否 | 2 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round14fullevidenceparallel-a78258a0.agent_loop.json.gz) |
| `SL-7` | 是 | 2 | ✅ | LLM calls=3, tokens=164634 | LLM model review | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round14fullevidenceparallel-a78258a0.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixPlan | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round14fullevidenceparallel-a78258a0.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=5, tokens=431547 | LLM repair candidate | candidate len=7059,6902,6873,7339,7041 | [`record`](./pr-e1-path2_lng_ems-default-round14fullevidenceparallel-a78258a0.agent_loop.json.gz) |
| `SD-10` | 否 | 0 | ⚠️ | ok=False, target_resolved=False, drift=major; ok=False, target_resolved=False, drift=major; ok=False, target_resolved=False, drift=major; ok=False, target_resolved=False, drift=maj | 本地 repair review | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round14fullevidenceparallel-a78258a0.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ⚠️ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round14fullevidenceparallel-a78258a0.agent_loop.json.gz) |
| `SC-12` | 否 | - | ⚠️ | new_blocking_design_diagnostic; scenario_regression; forced_transition_count_drift; missing_required_grounding | 写 final verdict | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round14fullevidenceparallel-a78258a0.agent_loop.json.gz) |
| `SC-13` | 否 | - | ✅ | trace/control | 写审计 run record | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round14fullevidenceparallel-a78258a0.agent_loop.json.gz) |

### 5. Iteration / repair / review 摘要

| Iter | selected feedback | repair? | SD-10 | SL-10B | 回到 SD-2? | verdict/备注 |
|---:|---|---|---|---|---|---|
| 0 | `SD-4` | yes | reject | <none> | no | repair_review_rejected_retry_with_revised_fix_plan |
| 1 | `SD-4` | yes | reject | <none> | no | repair_review_rejected_retry_with_revised_fix_plan |
| 2 | `SL-7` | yes | reject | <none> | no | repair_review_rejected_retry_with_revised_fix_plan |
| 3 | `SL-7` | yes | reject | <none> | no | repair_review_rejected_retry_with_revised_fix_plan |
| 4 | `SL-7` | yes | reject | <none> | no | new_blocking_design_diagnostic; scenario_regression; forced_transition_count_drift; missing_required_grounding |

### 6. Scenario 明细与逐轮通过情况

#### 6.1 Scenario pass/fail by iteration

口径：`✅` = 该 scenario 在该轮 SD-6 simulation 通过；`❌` = 该轮失败；`⚪` = 该轮未执行或无该 scenario 结果。

| Scenario | Intent | Iter 3 | Iter 4 | Iter 5 |
|---|---|---|---|---|
| `default_init_then_zero_load_charge` | default-init probe: first cycle must dispatch to IdleNoLoad, then zero load with RES and SoC below 0.95 must transition ...<truncated 20 chars> | ✅ | ✅ | ✅ |
| `forced_idle_no_load_no_res` | explicit-hot-start probe: from a non-idle operating state, PL=0 with no RES must force IdleNoLoad with all dispatch outp...<truncated 8 chars> | ✅ | ✅ | ✅ |
| `zero_load_spare_soc_boundary` | explicit-hot-start probe: with PL=0 and RES present, SoC exactly 0.95 should route renewable power to spare, not chargin...<truncated 2 chars> | ✅ | ✅ | ✅ |
| `res_covers_charge_below_soc_boundary` | explicit-hot-start probe: when RES covers positive load and SoC is just below 0.95, residual RES must charge the battery...<truncated 1 chars> | ✅ | ✅ | ✅ |
| `res_covers_spare_at_soc_boundary` | explicit-hot-start probe: when RES covers positive load and SoC is exactly 0.95, residual RES must become spare power. | ✅ | ✅ | ✅ |
| `battery_assist_low_deficit_soc_boundary` | explicit-hot-start probe: with RES below load, SoC exactly 0.2 and deficit within battery power, battery assist should c...<truncated 17 chars> | ✅ | ✅ | ✅ |
| `lng_low_soc_charge_margin` | explicit-hot-start probe: low SoC with LNG-capable deficit should include the Pgmax/5 charging margin. | ✅ | ✅ | ✅ |
| `lng_normal_after_battery_limit` | explicit-hot-start probe: normal SoC with deficit above battery limit but within LNG capacity should request LNG only. | ✅ | ✅ | ✅ |
| `lng_and_engine3_capacity_boundary` | explicit-hot-start probe: deficit above LNG capacity but within LNG plus engine3 should cut in LNG and engine3 only. | ✅ | ✅ | ✅ |
| `dg1_low_soc_charge_margin` | explicit-hot-start probe: low SoC diesel-generator branch should add the Pd1max/10 charging margin and cut in DG1. | ✅ | ✅ | ✅ |
| `dg1_normal_and_dg2_last_priority` | explicit-hot-start probe: normal DG1 branch should cover an intermediate deficit, then a separate high deficit hot-start...<truncated 44 chars> | ✅ | ✅ | ✅ |
| `dg2_and_overload_extreme_cases` | explicit-hot-start probe: DG2 should cover demand beyond DG1 capacity, while extreme demand beyond all thermal resources...<truncated 49 chars> | ✅ | ✅ | ✅ |

#### 6.2 Scenario definitions

<details><summary>`default_init_then_zero_load_charge` — default-init probe: first cycle must dispatch to IdleNoLoad, then zero load with RES and SoC below 0.95 must transition to battery charging.</summary>

| Field | Value |
|---|---|
| description | default-init probe: first cycle must dispatch to IdleNoLoad, then zero load with RES and SoC below 0.95 must transition to battery charging. |
| initial_state | `<default-init>` |
| initial_vars | `{"PL": 0.0, "Pbat_Pmax": 5.0, "Pd1max": 10.0, "Pd2max": 10.0, "Pgmax": 10.0, "Ppv": 3.0, "Pw": 2.0, "SoC": 0.94, "eng3_Pmax": 5.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `initial_leaf_is_idle` | `0` | `[]` | `LNGShipEMS.IdleNoLoad` | `{"Pbat_charge": 0.0, "Pbat_discharge": 0.0, "Pgen_req": 0.0, "Pspare": 0.0, "cut_in_battery": 0}` |
| 1 `zero_load_res_charges_battery` | `0` | `[]` | `LNGShipEMS.ZeroLoadCharge` | `{"Pbat_charge": 5.0, "Pbat_discharge": 0.0, "Pgen_req": 0.0, "Pspare": 0.0, "cut_in_DG1": 0, "cut_in_DG2": 0, "cut_in_LNG": 0, "cut_in_battery": 1, "cut_in_engine3": 0}` |

</details>

<details><summary>`forced_idle_no_load_no_res` — explicit-hot-start probe: from a non-idle operating state, PL=0 with no RES must force IdleNoLoad with all dispatch outputs off.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start probe: from a non-idle operating state, PL=0 with no RES must force IdleNoLoad with all dispatch outputs off. |
| initial_state | `LNGShipEMS.RESCoversSpare` |
| initial_vars | `{"PL": 0.0, "Pbat_Pmax": 5.0, "Pd1max": 10.0, "Pd2max": 10.0, "Pgmax": 10.0, "Ppv": 0.0, "Pw": 0.0, "SoC": 0.5, "eng3_Pmax": 5.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `no_load_no_res_idle` | `0` | `[]` | `LNGShipEMS.IdleNoLoad` | `{"Pbat_charge": 0.0, "Pbat_discharge": 0.0, "Pgen_req": 0.0, "Pspare": 0.0, "cut_in_DG1": 0, "cut_in_DG2": 0, "cut_in_LNG": 0, "cut_in_battery": 0, "cut_in_engine3": 0, "cut_out_load": 0}` |

</details>

<details><summary>`zero_load_spare_soc_boundary` — explicit-hot-start probe: with PL=0 and RES present, SoC exactly 0.95 should route renewable power to spare, not charging.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start probe: with PL=0 and RES present, SoC exactly 0.95 should route renewable power to spare, not charging. |
| initial_state | `LNGShipEMS.ZeroLoadCharge` |
| initial_vars | `{"PL": 0.0, "Pbat_Pmax": 5.0, "Pd1max": 10.0, "Pd2max": 10.0, "Pgmax": 10.0, "Ppv": 4.0, "Pw": 1.0, "SoC": 0.95, "eng3_Pmax": 5.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `soc_full_res_to_spare` | `0` | `[]` | `LNGShipEMS.ZeroLoadSpare` | `{"Pbat_charge": 0.0, "Pbat_discharge": 0.0, "Pgen_req": 0.0, "Pspare": 5.0, "cut_in_battery": 0}` |

</details>

<details><summary>`res_covers_charge_below_soc_boundary` — explicit-hot-start probe: when RES covers positive load and SoC is just below 0.95, residual RES must charge the battery.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start probe: when RES covers positive load and SoC is just below 0.95, residual RES must charge the battery. |
| initial_state | `LNGShipEMS.LNGCoveredNormal` |
| initial_vars | `{"PL": 10.0, "Pbat_Pmax": 5.0, "Pd1max": 10.0, "Pd2max": 10.0, "Pgmax": 10.0, "Ppv": 7.0, "Pw": 5.0, "SoC": 0.949, "eng3_Pmax": 5.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `res_surplus_charges` | `0` | `[]` | `LNGShipEMS.RESCoversCharge` | `{"Pbat_charge": 2.0, "Pbat_discharge": 0.0, "Pgen_req": 0.0, "Pspare": 0.0, "cut_in_battery": 1}` |

</details>

<details><summary>`res_covers_spare_at_soc_boundary` — explicit-hot-start probe: when RES covers positive load and SoC is exactly 0.95, residual RES must become spare power.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start probe: when RES covers positive load and SoC is exactly 0.95, residual RES must become spare power. |
| initial_state | `LNGShipEMS.RESCoversCharge` |
| initial_vars | `{"PL": 10.0, "Pbat_Pmax": 5.0, "Pd1max": 10.0, "Pd2max": 10.0, "Pgmax": 10.0, "Ppv": 7.0, "Pw": 5.0, "SoC": 0.95, "eng3_Pmax": 5.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `res_surplus_spare` | `0` | `[]` | `LNGShipEMS.RESCoversSpare` | `{"Pbat_charge": 0.0, "Pbat_discharge": 0.0, "Pgen_req": 0.0, "Pspare": 2.0, "cut_in_battery": 0}` |

</details>

<details><summary>`battery_assist_low_deficit_soc_boundary` — explicit-hot-start probe: with RES below load, SoC exactly 0.2 and deficit within battery power, battery assist should cover the deficit.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start probe: with RES below load, SoC exactly 0.2 and deficit within battery power, battery assist should cover the deficit. |
| initial_state | `LNGShipEMS.IdleNoLoad` |
| initial_vars | `{"PL": 10.0, "Pbat_Pmax": 5.0, "Pd1max": 10.0, "Pd2max": 10.0, "Pgmax": 10.0, "Ppv": 3.0, "Pw": 2.0, "SoC": 0.2, "eng3_Pmax": 5.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `battery_covers_deficit` | `0` | `[]` | `LNGShipEMS.BatteryAssist` | `{"Pbat_charge": 0.0, "Pbat_discharge": 5.0, "Pgen_req": 0.0, "Pspare": 0.0, "cut_in_LNG": 0, "cut_in_battery": 1}` |

</details>

<details><summary>`lng_low_soc_charge_margin` — explicit-hot-start probe: low SoC with LNG-capable deficit should include the Pgmax/5 charging margin.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start probe: low SoC with LNG-capable deficit should include the Pgmax/5 charging margin. |
| initial_state | `LNGShipEMS.BatteryAssist` |
| initial_vars | `{"PL": 15.0, "Pbat_Pmax": 5.0, "Pd1max": 10.0, "Pd2max": 10.0, "Pgmax": 10.0, "Ppv": 4.0, "Pw": 1.0, "SoC": 0.19, "eng3_Pmax": 5.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `lng_margin_charges_battery` | `0` | `[]` | `LNGShipEMS.LNGCoveredLowSoCChargeMargin` | `{"Pbat_charge": 2.0, "Pbat_discharge": 0.0, "Pgen_req": 12.0, "Pspare": 0.0, "cut_in_DG1": 0, "cut_in_DG2": 0, "cut_in_LNG": 1, "cut_in_battery": 1, "cut_in_engine3": 0}` |

</details>

<details><summary>`lng_normal_after_battery_limit` — explicit-hot-start probe: normal SoC with deficit above battery limit but within LNG capacity should request LNG only.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start probe: normal SoC with deficit above battery limit but within LNG capacity should request LNG only. |
| initial_state | `LNGShipEMS.LNGCoveredLowSoCChargeMargin` |
| initial_vars | `{"PL": 15.0, "Pbat_Pmax": 4.0, "Pd1max": 10.0, "Pd2max": 10.0, "Pgmax": 10.0, "Ppv": 4.0, "Pw": 1.0, "SoC": 0.2, "eng3_Pmax": 5.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `lng_only_covers_deficit` | `0` | `[]` | `LNGShipEMS.LNGCoveredNormal` | `{"Pbat_charge": 0.0, "Pbat_discharge": 0.0, "Pgen_req": 10.0, "Pspare": 0.0, "cut_in_DG1": 0, "cut_in_DG2": 0, "cut_in_LNG": 1, "cut_in_battery": 0, "cut_in_engine3": 0}` |

</details>

<details><summary>`lng_and_engine3_capacity_boundary` — explicit-hot-start probe: deficit above LNG capacity but within LNG plus engine3 should cut in LNG and engine3 only.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start probe: deficit above LNG capacity but within LNG plus engine3 should cut in LNG and engine3 only. |
| initial_state | `LNGShipEMS.DG1CoveredNormal` |
| initial_vars | `{"PL": 19.0, "Pbat_Pmax": 4.0, "Pd1max": 10.0, "Pd2max": 10.0, "Pgmax": 10.0, "Ppv": 4.0, "Pw": 1.0, "SoC": 0.5, "eng3_Pmax": 5.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `lng_engine3_cover_deficit` | `0` | `[]` | `LNGShipEMS.LNGAndEngine3Covered` | `{"Pbat_charge": 0.0, "Pbat_discharge": 0.0, "Pgen_req": 14.0, "Pspare": 0.0, "cut_in_DG1": 0, "cut_in_DG2": 0, "cut_in_LNG": 1, "cut_in_battery": 0, "cut_in_engine3": 1}` |

</details>

<details><summary>`dg1_low_soc_charge_margin` — explicit-hot-start probe: low SoC diesel-generator branch should add the Pd1max/10 charging margin and cut in DG1.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start probe: low SoC diesel-generator branch should add the Pd1max/10 charging margin and cut in DG1. |
| initial_state | `LNGShipEMS.LNGAndEngine3Covered` |
| initial_vars | `{"PL": 21.0, "Pbat_Pmax": 4.0, "Pd1max": 10.0, "Pd2max": 10.0, "Pgmax": 10.0, "Ppv": 4.0, "Pw": 1.0, "SoC": 0.19, "eng3_Pmax": 5.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `dg1_margin_charges_battery` | `0` | `[]` | `LNGShipEMS.DG1LowSoCChargeMargin` | `{"Pbat_charge": 1.0, "Pbat_discharge": 0.0, "Pgen_req": 17.0, "Pspare": 0.0, "cut_in_DG1": 1, "cut_in_DG2": 0, "cut_in_LNG": 1, "cut_in_battery": 1, "cut_in_engine3": 1}` |

</details>

<details><summary>`dg1_normal_and_dg2_last_priority` — explicit-hot-start probe: normal DG1 branch should cover an intermediate deficit, then a separate high deficit hot-start origin verifies DG2 as last-priority co...<truncated 4 chars></summary>

| Field | Value |
|---|---|
| description | explicit-hot-start probe: normal DG1 branch should cover an intermediate deficit, then a separate high deficit hot-start origin verifies DG2 as last-priority cover. |
| initial_state | `LNGShipEMS.DG1LowSoCChargeMargin` |
| initial_vars | `{"PL": 21.0, "Pbat_Pmax": 4.0, "Pd1max": 10.0, "Pd2max": 10.0, "Pgmax": 10.0, "Ppv": 4.0, "Pw": 1.0, "SoC": 0.5, "eng3_Pmax": 5.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `dg1_normal_covers_deficit` | `0` | `[]` | `LNGShipEMS.DG1CoveredNormal` | `{"Pbat_charge": 0.0, "Pbat_discharge": 0.0, "Pgen_req": 16.0, "Pspare": 0.0, "cut_in_DG1": 1, "cut_in_DG2": 0, "cut_in_LNG": 1, "cut_in_battery": 0, "cut_in_engine3": 1}` |

</details>

<details><summary>`dg2_and_overload_extreme_cases` — explicit-hot-start probe: DG2 should cover demand beyond DG1 capacity, while extreme demand beyond all thermal resources enters the illegal overload completion ...<truncated 9 chars></summary>

| Field | Value |
|---|---|
| description | explicit-hot-start probe: DG2 should cover demand beyond DG1 capacity, while extreme demand beyond all thermal resources enters the illegal overload completion behavior. |
| initial_state | `LNGShipEMS.OverloadCompletionIllegal` |
| initial_vars | `{"PL": 35.0, "Pbat_Pmax": 4.0, "Pd1max": 10.0, "Pd2max": 10.0, "Pgmax": 10.0, "Ppv": 4.0, "Pw": 1.0, "SoC": 0.5, "eng3_Pmax": 5.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `dg2_covers_after_dg1_limit` | `0` | `[]` | `LNGShipEMS.DG2Covered` | `{"Pbat_charge": 0.0, "Pbat_discharge": 0.0, "Pgen_req": 30.0, "Pspare": 0.0, "cut_in_DG1": 1, "cut_in_DG2": 1, "cut_in_LNG": 1, "cut_in_battery": 0, "cut_in_engine3": 1}` |

</details>


### 7. Repair / blocking feedback 明细

口径：本节只记录 agent-loop 真实进入 repair block 后已有证据；`diff` 基于 run record 中可恢复的 before/candidate DSL 文本生成，若 before DSL 未落盘则明确标注不可恢复。

| Repair | iteration | accepted | source | blocking diagnostics | SD-10 / SL-10B | candidate hash |
|---:|---:|---:|---|---|---|---|
| 1 | `0` | ❌ | `SD-4` | W_UNWRITTEN_READ_VAR:var_name=Pd2max, W_UNWRITTEN_READ_VAR:var_name=Pbat_Pmax, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.IdleNoLoad:to_path=LNGShipEMS.BatteryAssist, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.IdleNoLoad:to_path=LNGShipEMS.LNGCoveredNormal, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.IdleNoLoad:to_path=LNGShipEMS.DG2Covered, ... +53 | SD-10 ok=False, target=False, regression=False, drift=major, reason=missing_required_grounding | `sha256:93caebf626f3e191c1aa3fa4e47d5767b9697dcd6806f3c540cd8eba6fa27c91` |
| 2 | `1` | ❌ | `SD-4` | W_UNWRITTEN_READ_VAR:var_name=Pd2max, W_UNWRITTEN_READ_VAR:var_name=Pbat_Pmax, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.IdleNoLoad:to_path=LNGShipEMS.BatteryAssist, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.IdleNoLoad:to_path=LNGShipEMS.LNGCoveredNormal, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.IdleNoLoad:to_path=LNGShipEMS.DG2Covered, ... +53 | SD-10 ok=False, target=False, regression=False, drift=major, reason=missing_required_grounding | `sha256:180df4cf113445e8e8ed80c4a7699aec96a916a393847d1d19d37639fb3a5a13` |
| 3 | `2` | ❌ | `SL-7` | W_UNWRITTEN_READ_VAR:var_name=Pd2max, W_UNWRITTEN_READ_VAR:var_name=Pbat_Pmax, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.IdleNoLoad:to_path=LNGShipEMS.BatteryAssist, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.IdleNoLoad:to_path=LNGShipEMS.LNGCoveredNormal, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.IdleNoLoad:to_path=LNGShipEMS.DG2Covered, ... +49 | SD-10 ok=False, target=False, regression=True, drift=major, reason=scenario_regression; missing_required_grounding | `sha256:302f510d4d02007c3eb00a902b754fdc37e3d30fe9e1d7e6711f423fe90c9f63` |
| 4 | `3` | ❌ | `SL-7` | W_UNWRITTEN_READ_VAR:var_name=Pd2max, W_UNWRITTEN_READ_VAR:var_name=Pbat_Pmax, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.IdleNoLoad:to_path=LNGShipEMS.BatteryAssist, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.IdleNoLoad:to_path=LNGShipEMS.LNGCoveredNormal, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.IdleNoLoad:to_path=LNGShipEMS.DG2Covered, ... +49 | SD-10 ok=False, target=False, regression=False, drift=major, reason=missing_required_grounding | `sha256:fe8c613b70a699a7b91fc62e878399f1ffd7cd8e9882a089319e4c8115ce959f` |
| 5 | `4` | ❌ | `SL-7` | W_UNWRITTEN_READ_VAR:var_name=Pd2max, W_UNWRITTEN_READ_VAR:var_name=Pbat_Pmax, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.IdleNoLoad:to_path=LNGShipEMS.BatteryAssist, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.IdleNoLoad:to_path=LNGShipEMS.LNGCoveredNormal, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.IdleNoLoad:to_path=LNGShipEMS.DG2Covered, ... +49 | SD-10 ok=False, target=False, regression=True, drift=major, reason=new_blocking_design_diagnostic; scenario_regression; forced_transition_count_drift; missing_required_grounding | `sha256:372f20d03a9f02ee8ffc77cc2d117143e9863993c6619dc4a7cecf3d4bd1110d` |

<details><summary>Repair 1 / iteration `0` / source `SD-4` / accepted=❌</summary>

#### 为什么进入修复

- selected feedback source：`SD-4`；blocking=`True`；pre_scenario=`True`。
- problem_summary：Variable 'Pd2max' is read but never written by any action or transition effect.; Variable 'Pbat_Pmax' is read but never written by any action or transition effect.; Transition guard reads only variables that are never changed by actions or effects.
- diagnostic ids：`W_UNWRITTEN_READ_VAR:var_name=Pd2max, W_UNWRITTEN_READ_VAR:var_name=Pbat_Pmax, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.IdleNoLoad:to_path=LNGShipEMS.BatteryAssist, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.IdleNoLoad:to_path=LNGShipEMS.LNGCoveredNormal, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.IdleNoLoad:to_path=LNGShipEMS.DG2Covered, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.IdleNoLoad:to_path=LNGShipEMS.OverloadCompletionIllegal, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.BatteryAssist, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.LNGCoveredNormal, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.DG2Covered, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.OverloadCompletionIllegal, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadSpare:to_path=LNGShipEMS.BatteryAssist, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadSpare:to_path=LNGShipEMS.LNGCoveredNormal, ... +46`。
- before_dsl_hash：`sha256:180df4cf113445e8e8ed80c4a7699aec96a916a393847d1d19d37639fb3a5a13`；candidate_dsl_hash：`sha256:93caebf626f3e191c1aa3fa4e47d5767b9697dcd6806f3c540cd8eba6fa27c91`。

#### 错误证据 / diagnostics

- 1. `W_UNWRITTEN_READ_VAR` `W_UNWRITTEN_READ_VAR:var_name=Pd2max` policy=`budgeted_repair`：Variable 'Pd2max' is read but never written by any action or transition effect.；refs=`{"init_value": "0.0", "read_states": ["LNGShipEMS.BatteryAssist", "LNGShipEMS.DG1CoveredNormal", "LNGShipEMS.DG1LowSoCChargeMargin", "LNGShipEMS.DG2Covered", "LNGShipEMS.IdleNoLoad", "LNGShipEMS.LNGAndEngine3Covered", "LNGShipEMS.LNGCoveredLowSoCChargeMargin", "LNGShipEMS.LNGCoveredNormal", "LNGShip...<truncated 170 chars>`
- 2. `W_UNWRITTEN_READ_VAR` `W_UNWRITTEN_READ_VAR:var_name=Pbat_Pmax` policy=`budgeted_repair`：Variable 'Pbat_Pmax' is read but never written by any action or transition effect.；refs=`{"init_value": "0.0", "read_states": ["LNGShipEMS.BatteryAssist", "LNGShipEMS.DG1CoveredNormal", "LNGShipEMS.DG1LowSoCChargeMargin", "LNGShipEMS.DG2Covered", "LNGShipEMS.IdleNoLoad", "LNGShipEMS.LNGAndEngine3Covered", "LNGShipEMS.LNGCoveredLowSoCChargeMargin", "LNGShipEMS.LNGCoveredNormal", "LNGShip...<truncated 173 chars>`
- 3. `W_GUARD_VARS_NEVER_CHANGE` `W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.IdleNoLoad:to_path=LNGShipEMS.BatteryAssist` policy=`budgeted_repair`：Transition guard reads only variables that are never changed by actions or effects.；refs=`{"from_path": "LNGShipEMS.IdleNoLoad", "guard_vars": ["PL", "Pbat_Pmax", "Ppv", "Pw", "SoC"], "to_path": "LNGShipEMS.BatteryAssist"}`
- 4. `W_GUARD_VARS_NEVER_CHANGE` `W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.IdleNoLoad:to_path=LNGShipEMS.LNGCoveredNormal` policy=`budgeted_repair`：Transition guard reads only variables that are never changed by actions or effects.；refs=`{"from_path": "LNGShipEMS.IdleNoLoad", "guard_vars": ["PL", "Pbat_Pmax", "Pgmax", "Ppv", "Pw", "SoC"], "to_path": "LNGShipEMS.LNGCoveredNormal"}`
- 5. `W_GUARD_VARS_NEVER_CHANGE` `W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.IdleNoLoad:to_path=LNGShipEMS.DG2Covered` policy=`budgeted_repair`：Transition guard reads only variables that are never changed by actions or effects.；refs=`{"from_path": "LNGShipEMS.IdleNoLoad", "guard_vars": ["PL", "Pd1max", "Pd2max", "Pgmax", "Ppv", "Pw", "eng3_Pmax"], "to_path": "LNGShipEMS.DG2Covered"}`
- 6. `W_GUARD_VARS_NEVER_CHANGE` `W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.IdleNoLoad:to_path=LNGShipEMS.OverloadCompletionIllegal` policy=`budgeted_repair`：Transition guard reads only variables that are never changed by actions or effects.；refs=`{"from_path": "LNGShipEMS.IdleNoLoad", "guard_vars": ["PL", "Pd1max", "Pd2max", "Pgmax", "Ppv", "Pw", "eng3_Pmax"], "to_path": "LNGShipEMS.OverloadCompletionIllegal"}`
- 7. `W_GUARD_VARS_NEVER_CHANGE` `W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.BatteryAssist` policy=`budgeted_repair`：Transition guard reads only variables that are never changed by actions or effects.；refs=`{"from_path": "LNGShipEMS.ZeroLoadCharge", "guard_vars": ["PL", "Pbat_Pmax", "Ppv", "Pw", "SoC"], "to_path": "LNGShipEMS.BatteryAssist"}`
- 8. `W_GUARD_VARS_NEVER_CHANGE` `W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.LNGCoveredNormal` policy=`budgeted_repair`：Transition guard reads only variables that are never changed by actions or effects.；refs=`{"from_path": "LNGShipEMS.ZeroLoadCharge", "guard_vars": ["PL", "Pbat_Pmax", "Pgmax", "Ppv", "Pw", "SoC"], "to_path": "LNGShipEMS.LNGCoveredNormal"}`
- ……另有 `46` 条 evidence 见 run record。

#### 变量角色与上下文提示

- policy：Advisory only. Do not invent writes for external_input_candidate variables unless NL explicitly gives update semantics; add meaningful NL-grounded writes only for internal state variables.
- source：SD-4 diagnostic refs and generic NL external-input rationale

| Variable | role_hint | nl_token_present | diagnostics |
|---|---|---:|---|
| `PL` | `external_input_candidate` | ✅ | `W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +165` |
| `Pbat_Pmax` | `unknown` | ❌ | `W_UNWRITTEN_READ_VAR, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +22` |
| `Pbat_charge` | `unknown` | ❌ | `W_UNREFERENCED_VAR` |
| `Pbat_discharge` | `unknown` | ❌ | `W_UNREFERENCED_VAR` |
| `Pd1max` | `external_input_candidate` | ✅ | `W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +48` |
| `Pd2max` | `unknown` | ❌ | `W_UNWRITTEN_READ_VAR, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +22` |
| `Pgen_req` | `unknown` | ❌ | `W_UNREFERENCED_VAR` |
| `Pgmax` | `external_input_candidate` | ✅ | `W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +87` |
| `Ppv` | `external_input_candidate` | ✅ | `W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +165` |
| `Pspare` | `unknown` | ❌ | `W_UNREFERENCED_VAR` |
| `Pw` | `external_input_candidate` | ✅ | `W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +165` |
| `SoC` | `external_input_candidate` | ✅ | `W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +113` |
| `cut_in_DG1` | `unknown` | ❌ | `W_UNREFERENCED_VAR` |
| `cut_in_DG2` | `unknown` | ❌ | `W_UNREFERENCED_VAR` |
| `cut_in_LNG` | `unknown` | ❌ | `W_UNREFERENCED_VAR` |
| `cut_in_battery` | `unknown` | ❌ | `W_UNREFERENCED_VAR` |
| `cut_in_engine3` | `unknown` | ❌ | `W_UNREFERENCED_VAR` |
| `cut_out_load` | `unknown` | ❌ | `W_UNREFERENCED_VAR` |
| `eng3_Pmax` | `external_input_candidate` | ✅ | `W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +61` |

#### SD-8 fix plan / 修改建议

- recommended_strategy：Use diagnostics as hints; choose the smallest globally consistent repair.；Before returning a candidate, verify every required_preserve_element_id still has a concrete DSL representation.
- hint 1：The variable is used as input but never updated after its initial definition, so model behavior may be accidentally constant.；`actions=add_write, simplify_guard；do_not=Do not add a meaningless self-assignment.`
- hint 2：The variable is used as input but never updated after its initial definition, so model behavior may be accidentally constant.；`actions=add_write, simplify_guard；do_not=Do not add a meaningless self-assignment.`
- hint 3：This guard is controlled only by initial variable values. If those values never change, the transition condition is effectively fixed.；`actions=add_write, simplify_guard；do_not=Do not add a meaningless self-assignment; it does not model a real change., Do not rewrite the guard to a meaningless constant only to silence this diagnostic.`
- hint 4：This guard is controlled only by initial variable values. If those values never change, the transition condition is effectively fixed.；`actions=add_write, simplify_guard；do_not=Do not add a meaningless self-assignment; it does not model a real change., Do not rewrite the guard to a meaningless constant only to silence this diagnostic.`
- hint 5：This guard is controlled only by initial variable values. If those values never change, the transition condition is effectively fixed.；`actions=add_write, simplify_guard；do_not=Do not add a meaningless self-assignment; it does not model a real change., Do not rewrite the guard to a meaningless constant only to silence this diagnostic.`
- hint 6：This guard is controlled only by initial variable values. If those values never change, the transition condition is effectively fixed.；`actions=add_write, simplify_guard；do_not=Do not add a meaningless self-assignment; it does not model a real change., Do not rewrite the guard to a meaningless constant only to silence this diagnostic.`
- forbidden_edits：`Do not delete grounded required elements merely to silence diagnostics., Do not invent internal plant/environment dynamics merely to make external input variables appear written.`。
- required_preserve_element_ids：`state:LNGShipEMS, variable:PL, variable:Ppv, variable:Pw, variable:SoC, variable:eng3_Pmax, variable:Pgmax, variable:Pd1max, variable:Pgen_req, variable:Pbat_discharge, variable:Pbat_charge, variable:Pspare, ... +24`。

#### SL-9 candidate / 最终修改执行方案

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
def float Pgen_req = 0.0;
def float Pbat_discharge = 0.0;
def float Pbat_charge = 0.0;
def float Pspare = 0.0;
def int cut_in_LNG = 0;
def int cut_in_engine3 = 0;
def int cut_in_DG1 = 0;
def int cut_in_DG2 = 0;
def int cut_in_battery = 0;
def int cut_out_load = 0;

state LNGShipEMS {
    >> during before {
        Pbat_Pmax = Pgmax / 5;
        Pd2max = Pd1max;
    }

    ! * -> IdleNoLoad : if [PL == 0 && Ppv + Pw == 0];
    ! * -> ZeroLoadCharge : if [PL == 0 && Ppv + Pw > 0 && SoC < 0.95];
    ! * -> ZeroLoadSpare : if [PL == 0 && Ppv + Pw > 0 && SoC >= 0.95];
    ! * -> RESCoversCharge : if [PL > 0 && Ppv + Pw >= PL && SoC < 0.95];
    ! * -> RESCoversSpare : if [PL > 0 && Ppv + Pw >= PL && SoC >= 0.95];
    ! * -> BatteryAssist : if [PL > 0 && Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw <= Pbat_Pmax];
    ! * -> LNGCoveredLowSoCChargeMargin : if [PL > 0 && Ppv + Pw < PL && SoC < 0.2 && PL - Ppv - Pw <= Pgmax];
    ! * -> LNGCoveredNormal : if [PL > 0 && Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw > Pbat_Pmax && PL - Ppv - Pw <= Pgmax];
    ! * -> LNGAndEngine3Covered : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > Pgmax && PL - Ppv - Pw <= Pgmax + eng3_Pmax];
    ! * -> DG1LowSoCChargeMargin : if [PL > 0 && Ppv + Pw < PL && SoC < 0.2 && PL - Ppv - Pw > Pgmax + eng3_Pmax && PL - Ppv - Pw + Pd1max / 10 <= Pgmax + eng3_Pmax + Pd1max];
    ! * -> DG1CoveredNormal : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > Pgmax + eng3_Pmax && PL - Ppv - Pw <= Pgmax + eng3_Pmax + Pd1max && (SoC >= 0.2 || PL - Ppv - Pw + Pd1max / 10 > Pgmax + eng3_Pmax + Pd1max)];
    ! * -> DG2Covered : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > Pgmax + eng3_Pmax + Pd1max && PL - Ppv - Pw <= Pgmax + eng3_Pmax + Pd1max + Pd2max];
    ! * -> OverloadCompletionIllegal : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > Pgmax + eng3_Pmax + Pd1max + Pd2max];

    [*] -> IdleNoLoad effect {
        Pbat_Pmax = Pgmax / 5;
        Pd2max = Pd1max;
    };

    state IdleNoLoad {
        enter {
            Pgen_req = 0.0;
            Pbat_discharge = 0.0;
            Pbat_charge = 0.0;
            Pspare = 0.0;
            cut_in_LNG = 0;
            cut_in_engine3 = 0;
            cut_in_DG1 = 0;
            cut_in_DG2 = 0;
            cut_in_battery = 0;
            cut_out_load = 0;
        }
    }

    state ZeroLoadCharge {
        enter {
            Pgen_req = 0.0;
            Pbat_discharge = 0.0;
            Pbat_charge = Ppv + Pw;
            Pspare = 0.0;
            cut_in_LNG = 0;
            cut_in_engine3 = 0;
            cut_in_DG1 = 0;
            cut_in_DG2 = 0;
            cut_in_battery = 1;
            cut_out_load = 0;
        }
    }

    state ZeroLoadSpare {
        enter {
            Pgen_req = 0.0;
            Pbat_discharge = 0.0;
            Pbat_charge = 0.0;
            Pspare = Ppv + Pw;
            cut_in_LNG = 0;
            cut_in_engine3 = 0;
            cut_in_DG1 = 0;
            cut_in_DG2 = 0;
            cut_in_battery = 0;
            cut_out_load = 0;
        }
    }

    state RESCoversCharge {
        enter {
            Pgen_req = 0.0;
            Pbat_discharge = 0.0;
            Pbat_charge = Ppv + Pw - PL;
            Pspare = 0.0;
            cut_in_LNG = 0;
            cut_in_engine3 = 0;
            cut_in_DG1 = 0;
            cut_in_DG2 = 0;
            cut_in_battery = 1;
            cut_out_load = 0;
        }
    }

    state RESCoversSpare {
        enter {
            Pgen_req = 0.0;
            Pbat_discharge = 0.0;
            Pbat_charge = 0.0;
            Pspare = Ppv + Pw - PL;
            cut_in_LNG = 0;
            cut_in_engine3 = 0;
            cut_in_DG1 = 0;
            cut_in_DG2 = 0;
            cut_in_battery = 0;
            cut_out_load = 0;
        }
    }

    state BatteryAssist {
        enter {
            Pgen_req = 0.0;
            Pbat_discharge = PL - Ppv - Pw;
            Pbat_charge = 0.0;
            Pspare = 0.0;
            cut_in_LNG = 0;
            cut_in_engine3 = 0;
            cut_in_DG1 = 0;
            cut_in_DG2 = 0;
            cut_in_battery = 1;
            cut_out_load = 0;
        }
    }

    state LNGCoveredLowSoCChargeMargin {
        enter {
            Pgen_req = PL - Ppv - Pw + Pgmax / 5;
            Pbat_discharge = 0.0;
            Pbat_charge = Pgmax / 5;
            Pspare = 0.0;
            cut_in_LNG = 1;
            cut_in_engine3 = 0;
            cut_in_DG1 = 0;
            cut_in_DG2 = 0;
            cut_in_battery = 1;
            cut_out_load = 0;
        }
    }

    state LNGCoveredNormal {
        enter {
            Pgen_req = PL - Ppv - Pw;
            Pbat_discharge = 0.0;
            Pbat_charge = 0.0;
            Pspare = 0.0;
            cut_in_LNG = 1;
            cut_in_engine3 = 0;
            cut_in_DG1 = 0;
            cut_in_DG2 = 0;
            cut_in_battery = 0;
            cut_out_load = 0;
        }
    }

    state LNGAndEngine3Covered {
        enter {
            Pgen_req = PL - Ppv - Pw;
            Pbat_discharge = 0.0;
            Pbat_charge = 0.0;
            Pspare = 0.0;
            cut_in_LNG = 1;
            cut_in_engine3 = 1;
            cut_in_DG1 = 0;
            cut_in_DG2 = 0;
            cut_in_battery = 0;
            cut_out_load = 0;
        }
    }

    state DG1LowSoCChargeMargin {
        enter {
            Pgen_req = PL - Ppv - Pw + Pd1max / 10;
            Pbat_discharge = 0.0;
            Pbat_charge = Pd1max / 10;
            Pspare = 0.0;
            cut_in_LNG = 1;
            cut_in_engine3 = 1;
            cut_in_DG1 = 1;
            cut_in_DG2 = 0;
            cut_in_battery = 1;
            cut_out_load = 0;
        }
    }

    state DG1CoveredNormal {
        enter {
            Pgen_req = PL - Ppv - Pw;
            Pbat_discharge = 0.0;
            Pbat_charge = 0.0;
            Pspare = 0.0;
            cut_in_LNG = 1;
            cut_in_engine3 = 1;
            cut_in_DG1 = 1;
            cut_in_DG2 = 0;
            cut_in_battery = 0;
            cut_out_load = 0;
        }
    }

    state DG2Covered {
        enter {
            Pgen_req = PL - Ppv - Pw;
            Pbat_discharge = 0.0;
            Pbat_charge = 0.0;
            Pspare = 0.0;
            cut_in_LNG = 1;
            cut_in_engine3 = 1;
            cut_in_DG1 = 1;
            cut_in_DG2 = 1;
            cut_in_battery = 0;
            cut_out_load = 0;
        }
    }

    state OverloadCompletionIllegal {
        enter {
            Pgen_req = Pgmax + eng3_Pmax + Pd1max + Pd2max;
            Pbat_discharge = PL - Ppv - Pw - Pgmax - eng3_Pmax - Pd1max - Pd2max;
            Pbat_charge = 0.0;
            Pspare = 0.0;
            cut_in_LNG = 1;
            cut_in_engine3 = 1;
            cut_in_DG1 = 1;
            cut_in_DG2 = 1;
            cut_in_battery = 1;
            cut_out_load = 1;
        }
    }
}
```

#### Candidate diff（before -> candidate）

```diff
--- before.fcstm
+++ candidate.fcstm
@@ -19,6 +19,11 @@
 def int cut_out_load = 0;
 
 state LNGShipEMS {
+    >> during before {
+        Pbat_Pmax = Pgmax / 5;
+        Pd2max = Pd1max;
+    }
+
     ! * -> IdleNoLoad : if [PL == 0 && Ppv + Pw == 0];
     ! * -> ZeroLoadCharge : if [PL == 0 && Ppv + Pw > 0 && SoC < 0.95];
     ! * -> ZeroLoadSpare : if [PL == 0 && Ppv + Pw > 0 && SoC >= 0.95];
@@ -33,7 +38,10 @@
     ! * -> DG2Covered : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > Pgmax + eng3_Pmax + Pd1max && PL - Ppv - Pw <= Pgmax + eng3_Pmax + Pd1max + Pd2max];
     ! * -> OverloadCompletionIllegal : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > Pgmax + eng3_Pmax + Pd1max + Pd2max];
 
-    [*] -> IdleNoLoad;
+    [*] -> IdleNoLoad effect {
+        Pbat_Pmax = Pgmax / 5;
+        Pd2max = Pd1max;
+    };
 
     state IdleNoLoad {
         enter {
```

#### SD-10 / SL-10B 审查结果

- SD-10 ok=`False`，target_resolved=`False`，regression_detected=`False`，drift_risk=`major`。
- local_rejection：reason=`missing_required_grounding`，rejected_by_stage=`SD-10`。
  - local evidence 1: `missing_required_grounding` {"element_ids": ["transition:*->RESCoversCharge", "transition:*->RESCoversSpare", "transition:*->ZeroLoadCharge", "transition:*->ZeroLoadSpare", "transition:*->BatteryAssist", "transition:*->LNGCoveredLowSoCChargeMargin", "transition:*->DG1LowSoCChargeMargin", "transition:*->OverloadCompletionIllegal"], "kind": "missing_required_grounding"}
- SL-10B delta_review：`<none>`（通常是 SD-10 本地审查已拒绝，未进入 LLM delta review）。

</details>

<details><summary>Repair 2 / iteration `1` / source `SD-4` / accepted=❌</summary>

#### 为什么进入修复

- selected feedback source：`SD-4`；blocking=`True`；pre_scenario=`True`。
- problem_summary：Variable 'Pd2max' is read but never written by any action or transition effect.; Variable 'Pbat_Pmax' is read but never written by any action or transition effect.; Transition guard reads only variables that are never changed by actions or effects.
- diagnostic ids：`W_UNWRITTEN_READ_VAR:var_name=Pd2max, W_UNWRITTEN_READ_VAR:var_name=Pbat_Pmax, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.IdleNoLoad:to_path=LNGShipEMS.BatteryAssist, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.IdleNoLoad:to_path=LNGShipEMS.LNGCoveredNormal, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.IdleNoLoad:to_path=LNGShipEMS.DG2Covered, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.IdleNoLoad:to_path=LNGShipEMS.OverloadCompletionIllegal, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.BatteryAssist, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.LNGCoveredNormal, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.DG2Covered, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.OverloadCompletionIllegal, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadSpare:to_path=LNGShipEMS.BatteryAssist, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadSpare:to_path=LNGShipEMS.LNGCoveredNormal, ... +46`。
- before_dsl_hash：`sha256:180df4cf113445e8e8ed80c4a7699aec96a916a393847d1d19d37639fb3a5a13`；candidate_dsl_hash：`sha256:180df4cf113445e8e8ed80c4a7699aec96a916a393847d1d19d37639fb3a5a13`。

#### 错误证据 / diagnostics

- 1. `W_UNWRITTEN_READ_VAR` `W_UNWRITTEN_READ_VAR:var_name=Pd2max` policy=`budgeted_repair`：Variable 'Pd2max' is read but never written by any action or transition effect.；refs=`{"init_value": "0.0", "read_states": ["LNGShipEMS.BatteryAssist", "LNGShipEMS.DG1CoveredNormal", "LNGShipEMS.DG1LowSoCChargeMargin", "LNGShipEMS.DG2Covered", "LNGShipEMS.IdleNoLoad", "LNGShipEMS.LNGAndEngine3Covered", "LNGShipEMS.LNGCoveredLowSoCChargeMargin", "LNGShipEMS.LNGCoveredNormal", "LNGShip...<truncated 170 chars>`
- 2. `W_UNWRITTEN_READ_VAR` `W_UNWRITTEN_READ_VAR:var_name=Pbat_Pmax` policy=`budgeted_repair`：Variable 'Pbat_Pmax' is read but never written by any action or transition effect.；refs=`{"init_value": "0.0", "read_states": ["LNGShipEMS.BatteryAssist", "LNGShipEMS.DG1CoveredNormal", "LNGShipEMS.DG1LowSoCChargeMargin", "LNGShipEMS.DG2Covered", "LNGShipEMS.IdleNoLoad", "LNGShipEMS.LNGAndEngine3Covered", "LNGShipEMS.LNGCoveredLowSoCChargeMargin", "LNGShipEMS.LNGCoveredNormal", "LNGShip...<truncated 173 chars>`
- 3. `W_GUARD_VARS_NEVER_CHANGE` `W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.IdleNoLoad:to_path=LNGShipEMS.BatteryAssist` policy=`budgeted_repair`：Transition guard reads only variables that are never changed by actions or effects.；refs=`{"from_path": "LNGShipEMS.IdleNoLoad", "guard_vars": ["PL", "Pbat_Pmax", "Ppv", "Pw", "SoC"], "to_path": "LNGShipEMS.BatteryAssist"}`
- 4. `W_GUARD_VARS_NEVER_CHANGE` `W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.IdleNoLoad:to_path=LNGShipEMS.LNGCoveredNormal` policy=`budgeted_repair`：Transition guard reads only variables that are never changed by actions or effects.；refs=`{"from_path": "LNGShipEMS.IdleNoLoad", "guard_vars": ["PL", "Pbat_Pmax", "Pgmax", "Ppv", "Pw", "SoC"], "to_path": "LNGShipEMS.LNGCoveredNormal"}`
- 5. `W_GUARD_VARS_NEVER_CHANGE` `W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.IdleNoLoad:to_path=LNGShipEMS.DG2Covered` policy=`budgeted_repair`：Transition guard reads only variables that are never changed by actions or effects.；refs=`{"from_path": "LNGShipEMS.IdleNoLoad", "guard_vars": ["PL", "Pd1max", "Pd2max", "Pgmax", "Ppv", "Pw", "eng3_Pmax"], "to_path": "LNGShipEMS.DG2Covered"}`
- 6. `W_GUARD_VARS_NEVER_CHANGE` `W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.IdleNoLoad:to_path=LNGShipEMS.OverloadCompletionIllegal` policy=`budgeted_repair`：Transition guard reads only variables that are never changed by actions or effects.；refs=`{"from_path": "LNGShipEMS.IdleNoLoad", "guard_vars": ["PL", "Pd1max", "Pd2max", "Pgmax", "Ppv", "Pw", "eng3_Pmax"], "to_path": "LNGShipEMS.OverloadCompletionIllegal"}`
- 7. `W_GUARD_VARS_NEVER_CHANGE` `W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.BatteryAssist` policy=`budgeted_repair`：Transition guard reads only variables that are never changed by actions or effects.；refs=`{"from_path": "LNGShipEMS.ZeroLoadCharge", "guard_vars": ["PL", "Pbat_Pmax", "Ppv", "Pw", "SoC"], "to_path": "LNGShipEMS.BatteryAssist"}`
- 8. `W_GUARD_VARS_NEVER_CHANGE` `W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.LNGCoveredNormal` policy=`budgeted_repair`：Transition guard reads only variables that are never changed by actions or effects.；refs=`{"from_path": "LNGShipEMS.ZeroLoadCharge", "guard_vars": ["PL", "Pbat_Pmax", "Pgmax", "Ppv", "Pw", "SoC"], "to_path": "LNGShipEMS.LNGCoveredNormal"}`
- ……另有 `46` 条 evidence 见 run record。

#### 变量角色与上下文提示

- policy：Advisory only. Do not invent writes for external_input_candidate variables unless NL explicitly gives update semantics; add meaningful NL-grounded writes only for internal state variables.
- source：SD-4 diagnostic refs and generic NL external-input rationale

| Variable | role_hint | nl_token_present | diagnostics |
|---|---|---:|---|
| `PL` | `external_input_candidate` | ✅ | `W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +165` |
| `Pbat_Pmax` | `unknown` | ❌ | `W_UNWRITTEN_READ_VAR, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +22` |
| `Pbat_charge` | `unknown` | ❌ | `W_UNREFERENCED_VAR` |
| `Pbat_discharge` | `unknown` | ❌ | `W_UNREFERENCED_VAR` |
| `Pd1max` | `external_input_candidate` | ✅ | `W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +48` |
| `Pd2max` | `unknown` | ❌ | `W_UNWRITTEN_READ_VAR, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +22` |
| `Pgen_req` | `unknown` | ❌ | `W_UNREFERENCED_VAR` |
| `Pgmax` | `external_input_candidate` | ✅ | `W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +87` |
| `Ppv` | `external_input_candidate` | ✅ | `W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +165` |
| `Pspare` | `unknown` | ❌ | `W_UNREFERENCED_VAR` |
| `Pw` | `external_input_candidate` | ✅ | `W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +165` |
| `SoC` | `external_input_candidate` | ✅ | `W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +113` |
| `cut_in_DG1` | `unknown` | ❌ | `W_UNREFERENCED_VAR` |
| `cut_in_DG2` | `unknown` | ❌ | `W_UNREFERENCED_VAR` |
| `cut_in_LNG` | `unknown` | ❌ | `W_UNREFERENCED_VAR` |
| `cut_in_battery` | `unknown` | ❌ | `W_UNREFERENCED_VAR` |
| `cut_in_engine3` | `unknown` | ❌ | `W_UNREFERENCED_VAR` |
| `cut_out_load` | `unknown` | ❌ | `W_UNREFERENCED_VAR` |
| `eng3_Pmax` | `external_input_candidate` | ✅ | `W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +61` |

#### SD-8 fix plan / 修改建议

- recommended_strategy：Use diagnostics as hints; choose the smallest globally consistent repair.；Before returning a candidate, verify every required_preserve_element_id still has a concrete DSL representation.
- hint 1：The variable is used as input but never updated after its initial definition, so model behavior may be accidentally constant.；`actions=add_write, simplify_guard；do_not=Do not add a meaningless self-assignment.`
- hint 2：The variable is used as input but never updated after its initial definition, so model behavior may be accidentally constant.；`actions=add_write, simplify_guard；do_not=Do not add a meaningless self-assignment.`
- hint 3：This guard is controlled only by initial variable values. If those values never change, the transition condition is effectively fixed.；`actions=add_write, simplify_guard；do_not=Do not add a meaningless self-assignment; it does not model a real change., Do not rewrite the guard to a meaningless constant only to silence this diagnostic.`
- hint 4：This guard is controlled only by initial variable values. If those values never change, the transition condition is effectively fixed.；`actions=add_write, simplify_guard；do_not=Do not add a meaningless self-assignment; it does not model a real change., Do not rewrite the guard to a meaningless constant only to silence this diagnostic.`
- hint 5：This guard is controlled only by initial variable values. If those values never change, the transition condition is effectively fixed.；`actions=add_write, simplify_guard；do_not=Do not add a meaningless self-assignment; it does not model a real change., Do not rewrite the guard to a meaningless constant only to silence this diagnostic.`
- hint 6：This guard is controlled only by initial variable values. If those values never change, the transition condition is effectively fixed.；`actions=add_write, simplify_guard；do_not=Do not add a meaningless self-assignment; it does not model a real change., Do not rewrite the guard to a meaningless constant only to silence this diagnostic.`
- forbidden_edits：`Do not delete grounded required elements merely to silence diagnostics., Do not invent internal plant/environment dynamics merely to make external input variables appear written.`。
- required_preserve_element_ids：`state:LNGShipEMS, variable:PL, variable:Ppv, variable:Pw, variable:SoC, variable:eng3_Pmax, variable:Pgmax, variable:Pd1max, variable:Pgen_req, variable:Pbat_discharge, variable:Pbat_charge, variable:Pspare, ... +24`。

#### SL-9 candidate / 最终修改执行方案

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
def float Pgen_req = 0.0;
def float Pbat_discharge = 0.0;
def float Pbat_charge = 0.0;
def float Pspare = 0.0;
def int cut_in_LNG = 0;
def int cut_in_engine3 = 0;
def int cut_in_DG1 = 0;
def int cut_in_DG2 = 0;
def int cut_in_battery = 0;
def int cut_out_load = 0;

state LNGShipEMS {
    ! * -> IdleNoLoad : if [PL == 0 && Ppv + Pw == 0];
    ! * -> ZeroLoadCharge : if [PL == 0 && Ppv + Pw > 0 && SoC < 0.95];
    ! * -> ZeroLoadSpare : if [PL == 0 && Ppv + Pw > 0 && SoC >= 0.95];
    ! * -> RESCoversCharge : if [PL > 0 && Ppv + Pw >= PL && SoC < 0.95];
    ! * -> RESCoversSpare : if [PL > 0 && Ppv + Pw >= PL && SoC >= 0.95];
    ! * -> BatteryAssist : if [PL > 0 && Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw <= Pbat_Pmax];
    ! * -> LNGCoveredLowSoCChargeMargin : if [PL > 0 && Ppv + Pw < PL && SoC < 0.2 && PL - Ppv - Pw <= Pgmax];
    ! * -> LNGCoveredNormal : if [PL > 0 && Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw > Pbat_Pmax && PL - Ppv - Pw <= Pgmax];
    ! * -> LNGAndEngine3Covered : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > Pgmax && PL - Ppv - Pw <= Pgmax + eng3_Pmax];
    ! * -> DG1LowSoCChargeMargin : if [PL > 0 && Ppv + Pw < PL && SoC < 0.2 && PL - Ppv - Pw > Pgmax + eng3_Pmax && PL - Ppv - Pw + Pd1max / 10 <= Pgmax + eng3_Pmax + Pd1max];
    ! * -> DG1CoveredNormal : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > Pgmax + eng3_Pmax && PL - Ppv - Pw <= Pgmax + eng3_Pmax + Pd1max && (SoC >= 0.2 || PL - Ppv - Pw + Pd1max / 10 > Pgmax + eng3_Pmax + Pd1max)];
    ! * -> DG2Covered : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > Pgmax + eng3_Pmax + Pd1max && PL - Ppv - Pw <= Pgmax + eng3_Pmax + Pd1max + Pd2max];
    ! * -> OverloadCompletionIllegal : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > Pgmax + eng3_Pmax + Pd1max + Pd2max];

    [*] -> IdleNoLoad;

    state IdleNoLoad {
        enter {
            Pgen_req = 0.0;
            Pbat_discharge = 0.0;
            Pbat_charge = 0.0;
            Pspare = 0.0;
            cut_in_LNG = 0;
            cut_in_engine3 = 0;
            cut_in_DG1 = 0;
            cut_in_DG2 = 0;
            cut_in_battery = 0;
            cut_out_load = 0;
        }
    }

    state ZeroLoadCharge {
        enter {
            Pgen_req = 0.0;
            Pbat_discharge = 0.0;
            Pbat_charge = Ppv + Pw;
            Pspare = 0.0;
            cut_in_LNG = 0;
            cut_in_engine3 = 0;
            cut_in_DG1 = 0;
            cut_in_DG2 = 0;
            cut_in_battery = 1;
            cut_out_load = 0;
        }
    }

    state ZeroLoadSpare {
        enter {
            Pgen_req = 0.0;
            Pbat_discharge = 0.0;
            Pbat_charge = 0.0;
            Pspare = Ppv + Pw;
            cut_in_LNG = 0;
            cut_in_engine3 = 0;
            cut_in_DG1 = 0;
            cut_in_DG2 = 0;
            cut_in_battery = 0;
            cut_out_load = 0;
        }
    }

    state RESCoversCharge {
        enter {
            Pgen_req = 0.0;
            Pbat_discharge = 0.0;
            Pbat_charge = Ppv + Pw - PL;
            Pspare = 0.0;
            cut_in_LNG = 0;
            cut_in_engine3 = 0;
            cut_in_DG1 = 0;
            cut_in_DG2 = 0;
            cut_in_battery = 1;
            cut_out_load = 0;
        }
    }

    state RESCoversSpare {
        enter {
            Pgen_req = 0.0;
            Pbat_discharge = 0.0;
            Pbat_charge = 0.0;
            Pspare = Ppv + Pw - PL;
            cut_in_LNG = 0;
            cut_in_engine3 = 0;
            cut_in_DG1 = 0;
            cut_in_DG2 = 0;
            cut_in_battery = 0;
            cut_out_load = 0;
        }
    }

    state BatteryAssist {
        enter {
            Pgen_req = 0.0;
            Pbat_discharge = PL - Ppv - Pw;
            Pbat_charge = 0.0;
            Pspare = 0.0;
            cut_in_LNG = 0;
            cut_in_engine3 = 0;
            cut_in_DG1 = 0;
            cut_in_DG2 = 0;
            cut_in_battery = 1;
            cut_out_load = 0;
        }
    }

    state LNGCoveredLowSoCChargeMargin {
        enter {
            Pgen_req = PL - Ppv - Pw + Pgmax / 5;
            Pbat_discharge = 0.0;
            Pbat_charge = Pgmax / 5;
            Pspare = 0.0;
            cut_in_LNG = 1;
            cut_in_engine3 = 0;
            cut_in_DG1 = 0;
            cut_in_DG2 = 0;
            cut_in_battery = 1;
            cut_out_load = 0;
        }
    }

    state LNGCoveredNormal {
        enter {
            Pgen_req = PL - Ppv - Pw;
            Pbat_discharge = 0.0;
            Pbat_charge = 0.0;
            Pspare = 0.0;
            cut_in_LNG = 1;
            cut_in_engine3 = 0;
            cut_in_DG1 = 0;
            cut_in_DG2 = 0;
            cut_in_battery = 0;
            cut_out_load = 0;
        }
    }

    state LNGAndEngine3Covered {
        enter {
            Pgen_req = PL - Ppv - Pw;
            Pbat_discharge = 0.0;
            Pbat_charge = 0.0;
            Pspare = 0.0;
            cut_in_LNG = 1;
            cut_in_engine3 = 1;
            cut_in_DG1 = 0;
            cut_in_DG2 = 0;
            cut_in_battery = 0;
            cut_out_load = 0;
        }
    }

    state DG1LowSoCChargeMargin {
        enter {
            Pgen_req = PL - Ppv - Pw + Pd1max / 10;
            Pbat_discharge = 0.0;
            Pbat_charge = Pd1max / 10;
            Pspare = 0.0;
            cut_in_LNG = 1;
            cut_in_engine3 = 1;
            cut_in_DG1 = 1;
            cut_in_DG2 = 0;
            cut_in_battery = 1;
            cut_out_load = 0;
        }
    }

    state DG1CoveredNormal {
        enter {
            Pgen_req = PL - Ppv - Pw;
            Pbat_discharge = 0.0;
            Pbat_charge = 0.0;
            Pspare = 0.0;
            cut_in_LNG = 1;
            cut_in_engine3 = 1;
            cut_in_DG1 = 1;
            cut_in_DG2 = 0;
            cut_in_battery = 0;
            cut_out_load = 0;
        }
    }

    state DG2Covered {
        enter {
            Pgen_req = PL - Ppv - Pw;
            Pbat_discharge = 0.0;
            Pbat_charge = 0.0;
            Pspare = 0.0;
            cut_in_LNG = 1;
            cut_in_engine3 = 1;
            cut_in_DG1 = 1;
            cut_in_DG2 = 1;
            cut_in_battery = 0;
            cut_out_load = 0;
        }
    }

    state OverloadCompletionIllegal {
        enter {
            Pgen_req = Pgmax + eng3_Pmax + Pd1max + Pd2max;
            Pbat_discharge = PL - Ppv - Pw - Pgmax - eng3_Pmax - Pd1max - Pd2max;
            Pbat_charge = 0.0;
            Pspare = 0.0;
            cut_in_LNG = 1;
            cut_in_engine3 = 1;
            cut_in_DG1 = 1;
            cut_in_DG2 = 1;
            cut_in_battery = 1;
            cut_out_load = 1;
        }
    }
}
```

#### Candidate diff（before -> candidate）

- before 与 candidate 文本完全一致；无 diff。

#### SD-10 / SL-10B 审查结果

- SD-10 ok=`False`，target_resolved=`False`，regression_detected=`False`，drift_risk=`major`。
- local_rejection：reason=`missing_required_grounding`，rejected_by_stage=`SD-10`。
  - local evidence 1: `missing_required_grounding` {"element_ids": ["transition:*->RESCoversCharge", "transition:*->RESCoversSpare", "transition:*->ZeroLoadCharge", "transition:*->ZeroLoadSpare", "transition:*->BatteryAssist", "transition:*->LNGCoveredLowSoCChargeMargin", "transition:*->DG1LowSoCChargeMargin", "transition:*->OverloadCompletionIllegal"], "kind": "missing_required_grounding"}
- SL-10B delta_review：`<none>`（通常是 SD-10 本地审查已拒绝，未进入 LLM delta review）。

</details>

<details><summary>Repair 3 / iteration `2` / source `SL-7` / accepted=❌</summary>

#### 为什么进入修复

- selected feedback source：`SL-7`；blocking=`True`；pre_scenario=`False`。
- problem_summary：Variable 'Pd2max' is read but never written by any action or transition effect.; Variable 'Pbat_Pmax' is read but never written by any action or transition effect.; Transition guard reads only variables that are never changed by actions or effects.
- diagnostic ids：`W_UNWRITTEN_READ_VAR:var_name=Pd2max, W_UNWRITTEN_READ_VAR:var_name=Pbat_Pmax, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.IdleNoLoad:to_path=LNGShipEMS.BatteryAssist, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.IdleNoLoad:to_path=LNGShipEMS.LNGCoveredNormal, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.IdleNoLoad:to_path=LNGShipEMS.DG2Covered, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.IdleNoLoad:to_path=LNGShipEMS.OverloadCompletionIllegal, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.BatteryAssist, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.LNGCoveredNormal, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.DG2Covered, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.OverloadCompletionIllegal, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadSpare:to_path=LNGShipEMS.BatteryAssist, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadSpare:to_path=LNGShipEMS.LNGCoveredNormal, ... +42`。
- before_dsl_hash：`sha256:180df4cf113445e8e8ed80c4a7699aec96a916a393847d1d19d37639fb3a5a13`；candidate_dsl_hash：`sha256:302f510d4d02007c3eb00a902b754fdc37e3d30fe9e1d7e6711f423fe90c9f63`。

#### 错误证据 / diagnostics

- 1. `W_UNWRITTEN_READ_VAR` `W_UNWRITTEN_READ_VAR:var_name=Pd2max` policy=`budgeted_repair`：Variable 'Pd2max' is read but never written by any action or transition effect.；refs=`{"init_value": "0.0", "read_states": ["LNGShipEMS.BatteryAssist", "LNGShipEMS.DG1CoveredNormal", "LNGShipEMS.DG1LowSoCChargeMargin", "LNGShipEMS.DG2Covered", "LNGShipEMS.IdleNoLoad", "LNGShipEMS.LNGAndEngine3Covered", "LNGShipEMS.LNGCoveredLowSoCChargeMargin", "LNGShipEMS.LNGCoveredNormal", "LNGShip...<truncated 170 chars>`
- 2. `W_UNWRITTEN_READ_VAR` `W_UNWRITTEN_READ_VAR:var_name=Pbat_Pmax` policy=`budgeted_repair`：Variable 'Pbat_Pmax' is read but never written by any action or transition effect.；refs=`{"init_value": "0.0", "read_states": ["LNGShipEMS.BatteryAssist", "LNGShipEMS.DG1CoveredNormal", "LNGShipEMS.DG1LowSoCChargeMargin", "LNGShipEMS.DG2Covered", "LNGShipEMS.IdleNoLoad", "LNGShipEMS.LNGAndEngine3Covered", "LNGShipEMS.LNGCoveredLowSoCChargeMargin", "LNGShipEMS.LNGCoveredNormal", "LNGShip...<truncated 173 chars>`
- 3. `W_GUARD_VARS_NEVER_CHANGE` `W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.IdleNoLoad:to_path=LNGShipEMS.BatteryAssist` policy=`budgeted_repair`：Transition guard reads only variables that are never changed by actions or effects.；refs=`{"from_path": "LNGShipEMS.IdleNoLoad", "guard_vars": ["PL", "Pbat_Pmax", "Ppv", "Pw", "SoC"], "to_path": "LNGShipEMS.BatteryAssist"}`
- 4. `W_GUARD_VARS_NEVER_CHANGE` `W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.IdleNoLoad:to_path=LNGShipEMS.LNGCoveredNormal` policy=`budgeted_repair`：Transition guard reads only variables that are never changed by actions or effects.；refs=`{"from_path": "LNGShipEMS.IdleNoLoad", "guard_vars": ["PL", "Pbat_Pmax", "Pgmax", "Ppv", "Pw", "SoC"], "to_path": "LNGShipEMS.LNGCoveredNormal"}`
- 5. `W_GUARD_VARS_NEVER_CHANGE` `W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.IdleNoLoad:to_path=LNGShipEMS.DG2Covered` policy=`budgeted_repair`：Transition guard reads only variables that are never changed by actions or effects.；refs=`{"from_path": "LNGShipEMS.IdleNoLoad", "guard_vars": ["PL", "Pd1max", "Pd2max", "Pgmax", "Ppv", "Pw", "eng3_Pmax"], "to_path": "LNGShipEMS.DG2Covered"}`
- 6. `W_GUARD_VARS_NEVER_CHANGE` `W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.IdleNoLoad:to_path=LNGShipEMS.OverloadCompletionIllegal` policy=`budgeted_repair`：Transition guard reads only variables that are never changed by actions or effects.；refs=`{"from_path": "LNGShipEMS.IdleNoLoad", "guard_vars": ["PL", "Pd1max", "Pd2max", "Pgmax", "Ppv", "Pw", "eng3_Pmax"], "to_path": "LNGShipEMS.OverloadCompletionIllegal"}`
- 7. `W_GUARD_VARS_NEVER_CHANGE` `W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.BatteryAssist` policy=`budgeted_repair`：Transition guard reads only variables that are never changed by actions or effects.；refs=`{"from_path": "LNGShipEMS.ZeroLoadCharge", "guard_vars": ["PL", "Pbat_Pmax", "Ppv", "Pw", "SoC"], "to_path": "LNGShipEMS.BatteryAssist"}`
- 8. `W_GUARD_VARS_NEVER_CHANGE` `W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.LNGCoveredNormal` policy=`budgeted_repair`：Transition guard reads only variables that are never changed by actions or effects.；refs=`{"from_path": "LNGShipEMS.ZeroLoadCharge", "guard_vars": ["PL", "Pbat_Pmax", "Pgmax", "Ppv", "Pw", "SoC"], "to_path": "LNGShipEMS.LNGCoveredNormal"}`
- ……另有 `46` 条 evidence 见 run record。

#### SD-8 fix plan / 修改建议

- recommended_strategy：Use diagnostics as hints; choose the smallest globally consistent repair.；Before returning a candidate, verify every required_preserve_element_id still has a concrete DSL representation.
- hint 1：The variable is used as input but never updated after its initial definition, so model behavior may be accidentally constant.；`actions=add_write, simplify_guard；do_not=Do not add a meaningless self-assignment.`
- hint 2：The variable is used as input but never updated after its initial definition, so model behavior may be accidentally constant.；`actions=add_write, simplify_guard；do_not=Do not add a meaningless self-assignment.`
- hint 3：This guard is controlled only by initial variable values. If those values never change, the transition condition is effectively fixed.；`actions=add_write, simplify_guard；do_not=Do not add a meaningless self-assignment; it does not model a real change., Do not rewrite the guard to a meaningless constant only to silence this diagnostic.`
- hint 4：This guard is controlled only by initial variable values. If those values never change, the transition condition is effectively fixed.；`actions=add_write, simplify_guard；do_not=Do not add a meaningless self-assignment; it does not model a real change., Do not rewrite the guard to a meaningless constant only to silence this diagnostic.`
- hint 5：This guard is controlled only by initial variable values. If those values never change, the transition condition is effectively fixed.；`actions=add_write, simplify_guard；do_not=Do not add a meaningless self-assignment; it does not model a real change., Do not rewrite the guard to a meaningless constant only to silence this diagnostic.`
- hint 6：This guard is controlled only by initial variable values. If those values never change, the transition condition is effectively fixed.；`actions=add_write, simplify_guard；do_not=Do not add a meaningless self-assignment; it does not model a real change., Do not rewrite the guard to a meaningless constant only to silence this diagnostic.`
- forbidden_edits：`Do not delete grounded required elements merely to silence diagnostics., Do not invent internal plant/environment dynamics merely to make external input variables appear written.`。
- required_preserve_element_ids：`state:LNGShipEMS, variable:PL, variable:Ppv, variable:Pw, variable:SoC, variable:eng3_Pmax, variable:Pgmax, variable:Pd1max, variable:Pgen_req, variable:Pbat_discharge, variable:Pbat_charge, variable:Pspare, ... +24`。

#### SL-9 candidate / 最终修改执行方案

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
def float Pgen_req = 0.0;
def float Pbat_discharge = 0.0;
def float Pbat_charge = 0.0;
def float Pspare = 0.0;
def int cut_in_LNG = 0;
def int cut_in_engine3 = 0;
def int cut_in_DG1 = 0;
def int cut_in_DG2 = 0;
def int cut_in_battery = 0;
def int cut_out_load = 0;

state LNGShipEMS {
    ! * -> IdleNoLoad : if [PL == 0 && Ppv + Pw == 0];
    ! * -> ZeroLoadCharge : if [PL == 0 && Ppv + Pw > 0 && SoC < 0.95];
    ! * -> ZeroLoadSpare : if [PL == 0 && Ppv + Pw > 0 && SoC >= 0.95];
    ! * -> RESCoversCharge : if [PL > 0 && Ppv + Pw >= PL && SoC < 0.95];
    ! * -> RESCoversSpare : if [PL > 0 && Ppv + Pw >= PL && SoC >= 0.95];
    ! * -> BatteryAssist : if [PL > 0 && Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw <= Pbat_Pmax];
    ! * -> LNGCoveredLowSoCChargeMargin : if [PL > 0 && Ppv + Pw < PL && SoC < 0.2 && PL - Ppv - Pw <= Pgmax];
    ! * -> LNGCoveredNormal : if [PL > 0 && Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw > Pbat_Pmax && PL - Ppv - Pw <= Pgmax];
    ! * -> LNGAndEngine3Covered : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > Pgmax && PL - Ppv - Pw <= Pgmax + eng3_Pmax];
    ! * -> DG1LowSoCChargeMargin : if [PL > 0 && Ppv + Pw < PL && SoC < 0.2 && PL - Ppv - Pw > Pgmax + eng3_Pmax && PL - Ppv - Pw + Pd1max / 10 <= Pgmax + eng3_Pmax + Pd1max];
    ! * -> DG1CoveredNormal : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > Pgmax + eng3_Pmax && PL - Ppv - Pw <= Pgmax + eng3_Pmax + Pd1max && (SoC >= 0.2 || PL - Ppv - Pw + Pd1max / 10 > Pgmax + eng3_Pmax + Pd1max)];
    ! * -> DG2Covered : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > Pgmax + eng3_Pmax + Pd1max && PL - Ppv - Pw <= Pgmax + eng3_Pmax + Pd1max + Pd2max];
    ! * -> OverloadCompletionIllegal : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > Pgmax + eng3_Pmax + Pd1max + Pd2max && SoC >= 0.2 && PL - Ppv - Pw - Pgmax - eng3_Pmax - Pd1max - Pd2max <= Pbat_Pmax];

    [*] -> IdleNoLoad;

    pseudo state IdleNoLoad;

    state ZeroLoadCharge {
        enter {
            Pgen_req = 0.0;
            Pbat_discharge = 0.0;
            Pbat_charge = Ppv + Pw;
            Pspare = 0.0;
            cut_in_LNG = 0;
            cut_in_engine3 = 0;
            cut_in_DG1 = 0;
            cut_in_DG2 = 0;
            if [Ppv + Pw > 0] {
                cut_in_battery = 1;
            } else {
                cut_in_battery = 0;
            }
            cut_out_load = 0;
        }
    }

    state ZeroLoadSpare {
        enter {
            Pgen_req = 0.0;
            Pbat_discharge = 0.0;
            Pbat_charge = 0.0;
            Pspare = Ppv + Pw;
            cut_in_LNG = 0;
            cut_in_engine3 = 0;
            cut_in_DG1 = 0;
            cut_in_DG2 = 0;
            cut_in_battery = 0;
            cut_out_load = 0;
        }
    }

    state RESCoversCharge {
        enter {
            Pgen_req = 0.0;
            Pbat_discharge = 0.0;
            Pbat_charge = Ppv + Pw - PL;
            Pspare = 0.0;
            cut_in_LNG = 0;
            cut_in_engine3 = 0;
            cut_in_DG1 = 0;
            cut_in_DG2 = 0;
            cut_in_battery = 1;
            cut_out_load = 0;
        }
    }

    state RESCoversSpare {
        enter {
            Pgen_req = 0.0;
            Pbat_discharge = 0.0;
            Pbat_charge = 0.0;
            Pspare = Ppv + Pw - PL;
            cut_in_LNG = 0;
            cut_in_engine3 = 0;
            cut_in_DG1 = 0;
            cut_in_DG2 = 0;
            cut_in_battery = 0;
            cut_out_load = 0;
        }
    }

    state BatteryAssist {
        enter {
            Pgen_req = 0.0;
            Pbat_discharge = PL - Ppv - Pw;
            Pbat_charge = 0.0;
            Pspare = 0.0;
            cut_in_LNG = 0;
            cut_in_engine3 = 0;
            cut_in_DG1 = 0;
            cut_in_DG2 = 0;
            cut_in_battery = 1;
            cut_out_load = 0;
        }
    }

    state LNGCoveredLowSoCChargeMargin {
        enter {
            Pgen_req = PL - Ppv - Pw + Pgmax / 5;
            Pbat_discharge = 0.0;
            Pbat_charge = Pgmax / 5;
            Pspare = 0.0;
            cut_in_LNG = 1;
            cut_in_engine3 = 0;
            cut_in_DG1 = 0;
            cut_in_DG2 = 0;
            cut_in_battery = 1;
            cut_out_load = 0;
        }
    }

    state LNGCoveredNormal {
        enter {
            Pgen_req = PL - Ppv - Pw;
            Pbat_discharge = 0.0;
            Pbat_charge = 0.0;
            Pspare = 0.0;
            cut_in_LNG = 1;
            cut_in_engine3 = 0;
            cut_in_DG1 = 0;
            cut_in_DG2 = 0;
            cut_in_battery = 0;
            cut_out_load = 0;
        }
    }

    state LNGAndEngine3Covered {
        enter {
            Pgen_req = PL - Ppv - Pw;
            Pbat_discharge = 0.0;
            Pbat_charge = 0.0;
            Pspare = 0.0;
            cut_in_LNG = 1;
            cut_in_engine3 = 1;
            cut_in_DG1 = 0;
            cut_in_DG2 = 0;
            cut_in_battery = 0;
            cut_out_load = 0;
        }
    }

    state DG1LowSoCChargeMargin {
        enter {
            Pgen_req = PL - Ppv - Pw + Pd1max / 10;
            Pbat_discharge = 0.0;
            Pbat_charge = Pd1max / 10;
            Pspare = 0.0;
            cut_in_LNG = 1;
            cut_in_engine3 = 1;
            cut_in_DG1 = 1;
            cut_in_DG2 = 0;
            cut_in_battery = 1;
            cut_out_load = 0;
        }
    }

    state DG1CoveredNormal {
        enter {
            Pgen_req = PL - Ppv - Pw;
            Pbat_discharge = 0.0;
            Pbat_charge = 0.0;
            Pspare = 0.0;
            cut_in_LNG = 1;
            cut_in_engine3 = 1;
            cut_in_DG1 = 1;
            cut_in_DG2 = 0;
            cut_in_battery = 0;
            cut_out_load = 0;
        }
    }

    state DG2Covered {
        enter {
            Pgen_req = PL - Ppv - Pw;
            Pbat_discharge = 0.0;
            Pbat_charge = 0.0;
            Pspare = 0.0;
            cut_in_LNG = 1;
            cut_in_engine3 = 1;
            cut_in_DG1 = 1;
            cut_in_DG2 = 1;
            cut_in_battery = 0;
            cut_out_load = 0;
        }
    }

    state OverloadCompletionIllegal {
        enter {
            Pgen_req = Pgmax + eng3_Pmax + Pd1max + Pd2max;
            Pbat_discharge = PL - Ppv - Pw - Pgmax - eng3_Pmax - Pd1max - Pd2max;
            Pbat_charge = 0.0;
            Pspare = 0.0;
            cut_in_LNG = 1;
            cut_in_engine3 = 1;
            cut_in_DG1 = 1;
            cut_in_DG2 = 1;
            cut_in_battery = 1;
            cut_out_load = 0;
        }
    }

    IdleNoLoad -> ZeroLoadCharge : if [SoC < 0.95];
    IdleNoLoad -> ZeroLoadSpare : if [SoC >= 0.95];
}
```

#### Candidate diff（before -> candidate）

```diff
--- before.fcstm
+++ candidate.fcstm
@@ -31,24 +31,11 @@
     ! * -> DG1LowSoCChargeMargin : if [PL > 0 && Ppv + Pw < PL && SoC < 0.2 && PL - Ppv - Pw > Pgmax + eng3_Pmax && PL - Ppv - Pw + Pd1max / 10 <= Pgmax + eng3_Pmax + Pd1max];
     ! * -> DG1CoveredNormal : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > Pgmax + eng3_Pmax && PL - Ppv - Pw <= Pgmax + eng3_Pmax + Pd1max && (SoC >= 0.2 || PL - Ppv - Pw + Pd1max / 10 > Pgmax + eng3_Pmax + Pd1max)];
     ! * -> DG2Covered : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > Pgmax + eng3_Pmax + Pd1max && PL - Ppv - Pw <= Pgmax + eng3_Pmax + Pd1max + Pd2max];
-    ! * -> OverloadCompletionIllegal : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > Pgmax + eng3_Pmax + Pd1max + Pd2max];
+    ! * -> OverloadCompletionIllegal : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > Pgmax + eng3_Pmax + Pd1max + Pd2max && SoC >= 0.2 && PL - Ppv - Pw - Pgmax - eng3_Pmax - Pd1max - Pd2max <= Pbat_Pmax];
 
     [*] -> IdleNoLoad;
 
-    state IdleNoLoad {
-        enter {
-            Pgen_req = 0.0;
-            Pbat_discharge = 0.0;
-            Pbat_charge = 0.0;
-            Pspare = 0.0;
-            cut_in_LNG = 0;
-            cut_in_engine3 = 0;
-            cut_in_DG1 = 0;
-            cut_in_DG2 = 0;
-            cut_in_battery = 0;
-            cut_out_load = 0;
-        }
-    }
+    pseudo state IdleNoLoad;
 
     state ZeroLoadCharge {
         enter {
@@ -60,7 +47,11 @@
             cut_in_engine3 = 0;
             cut_in_DG1 = 0;
             cut_in_DG2 = 0;
-            cut_in_battery = 1;
+            if [Ppv + Pw > 0] {
+                cut_in_battery = 1;
+            } else {
+                cut_in_battery = 0;
+            }
             cut_out_load = 0;
         }
     }
@@ -226,7 +217,10 @@
             cut_in_DG1 = 1;
             cut_in_DG2 = 1;
             cut_in_battery = 1;
-            cut_out_load = 1;
-        }
-    }
+            cut_out_load = 0;
+        }
+    }
+
+    IdleNoLoad -> ZeroLoadCharge : if [SoC < 0.95];
+    IdleNoLoad -> ZeroLoadSpare : if [SoC >= 0.95];
 }
```

#### SD-10 / SL-10B 审查结果

- SD-10 ok=`False`，target_resolved=`False`，regression_detected=`True`，drift_risk=`major`。
- local_rejection：reason=`scenario_regression; missing_required_grounding`，rejected_by_stage=`SD-10`。
  - local evidence 1: `scenario_regression` {"kind": "scenario_regression", "sim_feedback": {"n_scenarios": 12, "n_scenarios_passed": 10, "ok": false, "oracle_weak": false, "scenario_results": [{"description": "default-init probe: first cycle must dispatch to IdleNoLoad, then zero load with RES and SoC below 0.95 must transition to battery charging.", "name": "default_init_then_zero_load_charge", "setup_error": null, "status": "fail", "step_results": [{"actual_state": "LNGShipEMS.ZeroLoadCharge", "actual_vars": {"PL": 0.0, "Pbat_Pmax": 5....<truncated 10073 chars>
  - local evidence 2: `missing_required_grounding` {"element_ids": ["transition:*->RESCoversCharge", "transition:*->RESCoversSpare", "transition:*->ZeroLoadCharge", "transition:*->ZeroLoadSpare", "transition:*->BatteryAssist", "transition:*->LNGCoveredLowSoCChargeMargin", "transition:*->DG1LowSoCChargeMargin", "transition:*->OverloadCompletionIllegal"], "kind": "missing_required_grounding"}
- SL-10B delta_review：`<none>`（通常是 SD-10 本地审查已拒绝，未进入 LLM delta review）。

</details>

<details><summary>Repair 4 / iteration `3` / source `SL-7` / accepted=❌</summary>

#### 为什么进入修复

- selected feedback source：`SL-7`；blocking=`True`；pre_scenario=`False`。
- problem_summary：Variable 'Pd2max' is read but never written by any action or transition effect.; Variable 'Pbat_Pmax' is read but never written by any action or transition effect.; Transition guard reads only variables that are never changed by actions or effects.
- diagnostic ids：`W_UNWRITTEN_READ_VAR:var_name=Pd2max, W_UNWRITTEN_READ_VAR:var_name=Pbat_Pmax, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.IdleNoLoad:to_path=LNGShipEMS.BatteryAssist, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.IdleNoLoad:to_path=LNGShipEMS.LNGCoveredNormal, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.IdleNoLoad:to_path=LNGShipEMS.DG2Covered, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.IdleNoLoad:to_path=LNGShipEMS.OverloadCompletionIllegal, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.BatteryAssist, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.LNGCoveredNormal, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.DG2Covered, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.OverloadCompletionIllegal, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadSpare:to_path=LNGShipEMS.BatteryAssist, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadSpare:to_path=LNGShipEMS.LNGCoveredNormal, ... +42`。
- before_dsl_hash：`sha256:180df4cf113445e8e8ed80c4a7699aec96a916a393847d1d19d37639fb3a5a13`；candidate_dsl_hash：`sha256:fe8c613b70a699a7b91fc62e878399f1ffd7cd8e9882a089319e4c8115ce959f`。

#### 错误证据 / diagnostics

- 1. `W_UNWRITTEN_READ_VAR` `W_UNWRITTEN_READ_VAR:var_name=Pd2max` policy=`budgeted_repair`：Variable 'Pd2max' is read but never written by any action or transition effect.；refs=`{"init_value": "0.0", "read_states": ["LNGShipEMS.BatteryAssist", "LNGShipEMS.DG1CoveredNormal", "LNGShipEMS.DG1LowSoCChargeMargin", "LNGShipEMS.DG2Covered", "LNGShipEMS.IdleNoLoad", "LNGShipEMS.LNGAndEngine3Covered", "LNGShipEMS.LNGCoveredLowSoCChargeMargin", "LNGShipEMS.LNGCoveredNormal", "LNGShip...<truncated 170 chars>`
- 2. `W_UNWRITTEN_READ_VAR` `W_UNWRITTEN_READ_VAR:var_name=Pbat_Pmax` policy=`budgeted_repair`：Variable 'Pbat_Pmax' is read but never written by any action or transition effect.；refs=`{"init_value": "0.0", "read_states": ["LNGShipEMS.BatteryAssist", "LNGShipEMS.DG1CoveredNormal", "LNGShipEMS.DG1LowSoCChargeMargin", "LNGShipEMS.DG2Covered", "LNGShipEMS.IdleNoLoad", "LNGShipEMS.LNGAndEngine3Covered", "LNGShipEMS.LNGCoveredLowSoCChargeMargin", "LNGShipEMS.LNGCoveredNormal", "LNGShip...<truncated 173 chars>`
- 3. `W_GUARD_VARS_NEVER_CHANGE` `W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.IdleNoLoad:to_path=LNGShipEMS.BatteryAssist` policy=`budgeted_repair`：Transition guard reads only variables that are never changed by actions or effects.；refs=`{"from_path": "LNGShipEMS.IdleNoLoad", "guard_vars": ["PL", "Pbat_Pmax", "Ppv", "Pw", "SoC"], "to_path": "LNGShipEMS.BatteryAssist"}`
- 4. `W_GUARD_VARS_NEVER_CHANGE` `W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.IdleNoLoad:to_path=LNGShipEMS.LNGCoveredNormal` policy=`budgeted_repair`：Transition guard reads only variables that are never changed by actions or effects.；refs=`{"from_path": "LNGShipEMS.IdleNoLoad", "guard_vars": ["PL", "Pbat_Pmax", "Pgmax", "Ppv", "Pw", "SoC"], "to_path": "LNGShipEMS.LNGCoveredNormal"}`
- 5. `W_GUARD_VARS_NEVER_CHANGE` `W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.IdleNoLoad:to_path=LNGShipEMS.DG2Covered` policy=`budgeted_repair`：Transition guard reads only variables that are never changed by actions or effects.；refs=`{"from_path": "LNGShipEMS.IdleNoLoad", "guard_vars": ["PL", "Pd1max", "Pd2max", "Pgmax", "Ppv", "Pw", "eng3_Pmax"], "to_path": "LNGShipEMS.DG2Covered"}`
- 6. `W_GUARD_VARS_NEVER_CHANGE` `W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.IdleNoLoad:to_path=LNGShipEMS.OverloadCompletionIllegal` policy=`budgeted_repair`：Transition guard reads only variables that are never changed by actions or effects.；refs=`{"from_path": "LNGShipEMS.IdleNoLoad", "guard_vars": ["PL", "Pd1max", "Pd2max", "Pgmax", "Ppv", "Pw", "eng3_Pmax"], "to_path": "LNGShipEMS.OverloadCompletionIllegal"}`
- 7. `W_GUARD_VARS_NEVER_CHANGE` `W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.BatteryAssist` policy=`budgeted_repair`：Transition guard reads only variables that are never changed by actions or effects.；refs=`{"from_path": "LNGShipEMS.ZeroLoadCharge", "guard_vars": ["PL", "Pbat_Pmax", "Ppv", "Pw", "SoC"], "to_path": "LNGShipEMS.BatteryAssist"}`
- 8. `W_GUARD_VARS_NEVER_CHANGE` `W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.LNGCoveredNormal` policy=`budgeted_repair`：Transition guard reads only variables that are never changed by actions or effects.；refs=`{"from_path": "LNGShipEMS.ZeroLoadCharge", "guard_vars": ["PL", "Pbat_Pmax", "Pgmax", "Ppv", "Pw", "SoC"], "to_path": "LNGShipEMS.LNGCoveredNormal"}`
- ……另有 `46` 条 evidence 见 run record。

#### SD-8 fix plan / 修改建议

- recommended_strategy：Use diagnostics as hints; choose the smallest globally consistent repair.；Before returning a candidate, verify every required_preserve_element_id still has a concrete DSL representation.
- hint 1：The variable is used as input but never updated after its initial definition, so model behavior may be accidentally constant.；`actions=add_write, simplify_guard；do_not=Do not add a meaningless self-assignment.`
- hint 2：The variable is used as input but never updated after its initial definition, so model behavior may be accidentally constant.；`actions=add_write, simplify_guard；do_not=Do not add a meaningless self-assignment.`
- hint 3：This guard is controlled only by initial variable values. If those values never change, the transition condition is effectively fixed.；`actions=add_write, simplify_guard；do_not=Do not add a meaningless self-assignment; it does not model a real change., Do not rewrite the guard to a meaningless constant only to silence this diagnostic.`
- hint 4：This guard is controlled only by initial variable values. If those values never change, the transition condition is effectively fixed.；`actions=add_write, simplify_guard；do_not=Do not add a meaningless self-assignment; it does not model a real change., Do not rewrite the guard to a meaningless constant only to silence this diagnostic.`
- hint 5：This guard is controlled only by initial variable values. If those values never change, the transition condition is effectively fixed.；`actions=add_write, simplify_guard；do_not=Do not add a meaningless self-assignment; it does not model a real change., Do not rewrite the guard to a meaningless constant only to silence this diagnostic.`
- hint 6：This guard is controlled only by initial variable values. If those values never change, the transition condition is effectively fixed.；`actions=add_write, simplify_guard；do_not=Do not add a meaningless self-assignment; it does not model a real change., Do not rewrite the guard to a meaningless constant only to silence this diagnostic.`
- forbidden_edits：`Do not delete grounded required elements merely to silence diagnostics., Do not invent internal plant/environment dynamics merely to make external input variables appear written.`。
- required_preserve_element_ids：`state:LNGShipEMS, variable:PL, variable:Ppv, variable:Pw, variable:SoC, variable:eng3_Pmax, variable:Pgmax, variable:Pd1max, variable:Pgen_req, variable:Pbat_discharge, variable:Pbat_charge, variable:Pspare, ... +24`。

#### SL-9 candidate / 最终修改执行方案

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
def float Pgen_req = 0.0;
def float Pbat_discharge = 0.0;
def float Pbat_charge = 0.0;
def float Pspare = 0.0;
def int cut_in_LNG = 0;
def int cut_in_engine3 = 0;
def int cut_in_DG1 = 0;
def int cut_in_DG2 = 0;
def int cut_in_battery = 0;
def int cut_out_load = 0;
def int dispatch_enabled = 1;

state LNGShipEMS {
    ! * -> IdleNoLoad : if [dispatch_enabled > 0 && PL == 0 && Ppv + Pw == 0];
    ! * -> ZeroLoadCharge : if [dispatch_enabled > 0 && PL == 0 && Ppv + Pw > 0 && SoC < 0.95];
    ! * -> ZeroLoadSpare : if [dispatch_enabled > 0 && PL == 0 && Ppv + Pw > 0 && SoC >= 0.95];
    ! * -> RESCoversCharge : if [dispatch_enabled > 0 && PL > 0 && Ppv + Pw >= PL && SoC < 0.95];
    ! * -> RESCoversSpare : if [dispatch_enabled > 0 && PL > 0 && Ppv + Pw >= PL && SoC >= 0.95];
    ! * -> BatteryAssist : if [dispatch_enabled > 0 && PL > 0 && Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw <= Pbat_Pmax];
    ! * -> LNGCoveredLowSoCChargeMargin : if [dispatch_enabled > 0 && PL > 0 && Ppv + Pw < PL && SoC < 0.2 && PL - Ppv - Pw <= Pgmax];
    ! * -> LNGCoveredNormal : if [dispatch_enabled > 0 && PL > 0 && Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw > Pbat_Pmax && PL - Ppv - Pw <= Pgmax];
    ! * -> LNGAndEngine3Covered : if [dispatch_enabled > 0 && PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > Pgmax && PL - Ppv - Pw <= Pgmax + eng3_Pmax];
    ! * -> DG1LowSoCChargeMargin : if [dispatch_enabled > 0 && PL > 0 && Ppv + Pw < PL && SoC < 0.2 && PL - Ppv - Pw > Pgmax + eng3_Pmax && PL - Ppv - Pw + Pd1max / 10 <= Pgmax + eng3_Pmax + Pd1max];
    ! * -> DG1CoveredNormal : if [dispatch_enabled > 0 && PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > Pgmax + eng3_Pmax && PL - Ppv - Pw <= Pgmax + eng3_Pmax + Pd1max && (SoC >= 0.2 || PL - Ppv - Pw + Pd1max / 10 > Pgmax + eng3_Pmax + Pd1max)];
    ! * -> DG2Covered : if [dispatch_enabled > 0 && PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > Pgmax + eng3_Pmax + Pd1max && PL - Ppv - Pw <= Pgmax + eng3_Pmax + Pd1max + Pd2max];
    ! * -> OverloadCompletionIllegal : if [dispatch_enabled > 0 && PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > Pgmax + eng3_Pmax + Pd1max + Pd2max];

    [*] -> IdleNoLoad effect { dispatch_enabled = 0; };

    state IdleNoLoad {
        enter {
            Pgen_req = 0.0;
            Pbat_discharge = 0.0;
            Pbat_charge = 0.0;
            Pspare = 0.0;
            cut_in_LNG = 0;
            cut_in_engine3 = 0;
            cut_in_DG1 = 0;
            cut_in_DG2 = 0;
            cut_in_battery = 0;
            cut_out_load = 0;
        }

        during {
            dispatch_enabled = 1;
        }
    }

    state ZeroLoadCharge {
        enter {
            Pgen_req = 0.0;
            Pbat_discharge = 0.0;
            Pbat_charge = Ppv + Pw;
            Pspare = 0.0;
            cut_in_LNG = 0;
            cut_in_engine3 = 0;
            cut_in_DG1 = 0;
            cut_in_DG2 = 0;
            cut_in_battery = 1;
            cut_out_load = 0;
        }
    }

    state ZeroLoadSpare {
        enter {
            Pgen_req = 0.0;
            Pbat_discharge = 0.0;
            Pbat_charge = 0.0;
            Pspare = Ppv + Pw;
            cut_in_LNG = 0;
            cut_in_engine3 = 0;
            cut_in_DG1 = 0;
            cut_in_DG2 = 0;
            cut_in_battery = 0;
            cut_out_load = 0;
        }
    }

    state RESCoversCharge {
        enter {
            Pgen_req = 0.0;
            Pbat_discharge = 0.0;
            Pbat_charge = Ppv + Pw - PL;
            Pspare = 0.0;
            cut_in_LNG = 0;
            cut_in_engine3 = 0;
            cut_in_DG1 = 0;
            cut_in_DG2 = 0;
            cut_in_battery = 1;
            cut_out_load = 0;
        }
    }

    state RESCoversSpare {
        enter {
            Pgen_req = 0.0;
            Pbat_discharge = 0.0;
            Pbat_charge = 0.0;
            Pspare = Ppv + Pw - PL;
            cut_in_LNG = 0;
            cut_in_engine3 = 0;
            cut_in_DG1 = 0;
            cut_in_DG2 = 0;
            cut_in_battery = 0;
            cut_out_load = 0;
        }
    }

    state BatteryAssist {
        enter {
            Pgen_req = 0.0;
            Pbat_discharge = PL - Ppv - Pw;
            Pbat_charge = 0.0;
            Pspare = 0.0;
            cut_in_LNG = 0;
            cut_in_engine3 = 0;
            cut_in_DG1 = 0;
            cut_in_DG2 = 0;
            cut_in_battery = 1;
            cut_out_load = 0;
        }
    }

    state LNGCoveredLowSoCChargeMargin {
        enter {
            Pgen_req = PL - Ppv - Pw + Pgmax / 5;
            Pbat_discharge = 0.0;
            Pbat_charge = Pgmax / 5;
            Pspare = 0.0;
            cut_in_LNG = 1;
            cut_in_engine3 = 0;
            cut_in_DG1 = 0;
            cut_in_DG2 = 0;
            cut_in_battery = 1;
            cut_out_load = 0;
        }
    }

    state LNGCoveredNormal {
        enter {
            Pgen_req = PL - Ppv - Pw;
            Pbat_discharge = 0.0;
            Pbat_charge = 0.0;
            Pspare = 0.0;
            cut_in_LNG = 1;
            cut_in_engine3 = 0;
            cut_in_DG1 = 0;
            cut_in_DG2 = 0;
            cut_in_battery = 0;
            cut_out_load = 0;
        }
    }

    state LNGAndEngine3Covered {
        enter {
            Pgen_req = PL - Ppv - Pw;
            Pbat_discharge = 0.0;
            Pbat_charge = 0.0;
            Pspare = 0.0;
            cut_in_LNG = 1;
            cut_in_engine3 = 1;
            cut_in_DG1 = 0;
            cut_in_DG2 = 0;
            cut_in_battery = 0;
            cut_out_load = 0;
        }
    }

    state DG1LowSoCChargeMargin {
        enter {
            Pgen_req = PL - Ppv - Pw + Pd1max / 10;
            Pbat_discharge = 0.0;
            Pbat_charge = Pd1max / 10;
            Pspare = 0.0;
            cut_in_LNG = 1;
            cut_in_engine3 = 1;
            cut_in_DG1 = 1;
            cut_in_DG2 = 0;
            cut_in_battery = 1;
            cut_out_load = 0;
        }
    }

    state DG1CoveredNormal {
        enter {
            Pgen_req = PL - Ppv - Pw;
            Pbat_discharge = 0.0;
            Pbat_charge = 0.0;
            Pspare = 0.0;
            cut_in_LNG = 1;
            cut_in_engine3 = 1;
            cut_in_DG1 = 1;
            cut_in_DG2 = 0;
            cut_in_battery = 0;
            cut_out_load = 0;
        }
    }

    state DG2Covered {
        enter {
            Pgen_req = PL - Ppv - Pw;
            Pbat_discharge = 0.0;
            Pbat_charge = 0.0;
            Pspare = 0.0;
            cut_in_LNG = 1;
            cut_in_engine3 = 1;
            cut_in_DG1 = 1;
            cut_in_DG2 = 1;
            cut_in_battery = 0;
            cut_out_load = 0;
        }
    }

    state OverloadCompletionIllegal {
        enter {
            Pgen_req = Pgmax + eng3_Pmax + Pd1max + Pd2max;
            Pbat_discharge = PL - Ppv - Pw - Pgmax - eng3_Pmax - Pd1max - Pd2max;
            Pbat_charge = 0.0;
            Pspare = 0.0;
            cut_in_LNG = 1;
            cut_in_engine3 = 1;
            cut_in_DG1 = 1;
            cut_in_DG2 = 1;
            cut_in_battery = 1;
            cut_out_load = 0;
        }
    }
}
```

#### Candidate diff（before -> candidate）

```diff
--- before.fcstm
+++ candidate.fcstm
@@ -17,23 +17,24 @@
 def int cut_in_DG2 = 0;
 def int cut_in_battery = 0;
 def int cut_out_load = 0;
+def int dispatch_enabled = 1;
 
 state LNGShipEMS {
-    ! * -> IdleNoLoad : if [PL == 0 && Ppv + Pw == 0];
-    ! * -> ZeroLoadCharge : if [PL == 0 && Ppv + Pw > 0 && SoC < 0.95];
-    ! * -> ZeroLoadSpare : if [PL == 0 && Ppv + Pw > 0 && SoC >= 0.95];
-    ! * -> RESCoversCharge : if [PL > 0 && Ppv + Pw >= PL && SoC < 0.95];
-    ! * -> RESCoversSpare : if [PL > 0 && Ppv + Pw >= PL && SoC >= 0.95];
-    ! * -> BatteryAssist : if [PL > 0 && Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw <= Pbat_Pmax];
-    ! * -> LNGCoveredLowSoCChargeMargin : if [PL > 0 && Ppv + Pw < PL && SoC < 0.2 && PL - Ppv - Pw <= Pgmax];
-    ! * -> LNGCoveredNormal : if [PL > 0 && Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw > Pbat_Pmax && PL - Ppv - Pw <= Pgmax];
-    ! * -> LNGAndEngine3Covered : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > Pgmax && PL - Ppv - Pw <= Pgmax + eng3_Pmax];
-    ! * -> DG1LowSoCChargeMargin : if [PL > 0 && Ppv + Pw < PL && SoC < 0.2 && PL - Ppv - Pw > Pgmax + eng3_Pmax && PL - Ppv - Pw + Pd1max / 10 <= Pgmax + eng3_Pmax + Pd1max];
-    ! * -> DG1CoveredNormal : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > Pgmax + eng3_Pmax && PL - Ppv - Pw <= Pgmax + eng3_Pmax + Pd1max && (SoC >= 0.2 || PL - Ppv - Pw + Pd1max / 10 > Pgmax + eng3_Pmax + Pd1max)];
-    ! * -> DG2Covered : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > Pgmax + eng3_Pmax + Pd1max && PL - Ppv - Pw <= Pgmax + eng3_Pmax + Pd1max + Pd2max];
-    ! * -> OverloadCompletionIllegal : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > Pgmax + eng3_Pmax + Pd1max + Pd2max];
-
-    [*] -> IdleNoLoad;
+    ! * -> IdleNoLoad : if [dispatch_enabled > 0 && PL == 0 && Ppv + Pw == 0];
+    ! * -> ZeroLoadCharge : if [dispatch_enabled > 0 && PL == 0 && Ppv + Pw > 0 && SoC < 0.95];
+    ! * -> ZeroLoadSpare : if [dispatch_enabled > 0 && PL == 0 && Ppv + Pw > 0 && SoC >= 0.95];
+    ! * -> RESCoversCharge : if [dispatch_enabled > 0 && PL > 0 && Ppv + Pw >= PL && SoC < 0.95];
+    ! * -> RESCoversSpare : if [dispatch_enabled > 0 && PL > 0 && Ppv + Pw >= PL && SoC >= 0.95];
+    ! * -> BatteryAssist : if [dispatch_enabled > 0 && PL > 0 && Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw <= Pbat_Pmax];
+    ! * -> LNGCoveredLowSoCChargeMargin : if [dispatch_enabled > 0 && PL > 0 && Ppv + Pw < PL && SoC < 0.2 && PL - Ppv - Pw <= Pgmax];
+    ! * -> LNGCoveredNormal : if [dispatch_enabled > 0 && PL > 0 && Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw > Pbat_Pmax && PL - Ppv - Pw <= Pgmax];
+    ! * -> LNGAndEngine3Covered : if [dispatch_enabled > 0 && PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > Pgmax && PL - Ppv - Pw <= Pgmax + eng3_Pmax];
+    ! * -> DG1LowSoCChargeMargin : if [dispatch_enabled > 0 && PL > 0 && Ppv + Pw < PL && SoC < 0.2 && PL - Ppv - Pw > Pgmax + eng3_Pmax && PL - Ppv - Pw + Pd1max / 10 <= Pgmax + eng3_Pmax + Pd1max];
+    ! * -> DG1CoveredNormal : if [dispatch_enabled > 0 && PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > Pgmax + eng3_Pmax && PL - Ppv - Pw <= Pgmax + eng3_Pmax + Pd1max && (SoC >= 0.2 || PL - Ppv - Pw + Pd1max / 10 > Pgmax + eng3_Pmax + Pd1max)];
+    ! * -> DG2Covered : if [dispatch_enabled > 0 && PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > Pgmax + eng3_Pmax + Pd1max && PL - Ppv - Pw <= Pgmax + eng3_Pmax + Pd1max + Pd2max];
+    ! * -> OverloadCompletionIllegal : if [dispatch_enabled > 0 && PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > Pgmax + eng3_Pmax + Pd1max + Pd2max];
+
+    [*] -> IdleNoLoad effect { dispatch_enabled = 0; };
 
     state IdleNoLoad {
         enter {
@@ -47,6 +48,10 @@
             cut_in_DG2 = 0;
             cut_in_battery = 0;
             cut_out_load = 0;
+        }
+
+        during {
+            dispatch_enabled = 1;
         }
     }
 
@@ -226,7 +231,7 @@
             cut_in_DG1 = 1;
             cut_in_DG2 = 1;
             cut_in_battery = 1;
-            cut_out_load = 1;
+            cut_out_load = 0;
         }
     }
 }
```

#### SD-10 / SL-10B 审查结果

- SD-10 ok=`False`，target_resolved=`False`，regression_detected=`False`，drift_risk=`major`。
- local_rejection：reason=`missing_required_grounding`，rejected_by_stage=`SD-10`。
  - local evidence 1: `missing_required_grounding` {"element_ids": ["transition:*->RESCoversCharge", "transition:*->RESCoversSpare", "transition:*->ZeroLoadCharge", "transition:*->ZeroLoadSpare", "transition:*->BatteryAssist", "transition:*->LNGCoveredLowSoCChargeMargin", "transition:*->DG1LowSoCChargeMargin", "transition:*->OverloadCompletionIllegal"], "kind": "missing_required_grounding"}
- SL-10B delta_review：`<none>`（通常是 SD-10 本地审查已拒绝，未进入 LLM delta review）。

</details>

<details><summary>Repair 5 / iteration `4` / source `SL-7` / accepted=❌</summary>

#### 为什么进入修复

- selected feedback source：`SL-7`；blocking=`True`；pre_scenario=`False`。
- problem_summary：Variable 'Pd2max' is read but never written by any action or transition effect.; Variable 'Pbat_Pmax' is read but never written by any action or transition effect.; Transition guard reads only variables that are never changed by actions or effects.
- diagnostic ids：`W_UNWRITTEN_READ_VAR:var_name=Pd2max, W_UNWRITTEN_READ_VAR:var_name=Pbat_Pmax, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.IdleNoLoad:to_path=LNGShipEMS.BatteryAssist, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.IdleNoLoad:to_path=LNGShipEMS.LNGCoveredNormal, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.IdleNoLoad:to_path=LNGShipEMS.DG2Covered, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.IdleNoLoad:to_path=LNGShipEMS.OverloadCompletionIllegal, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.BatteryAssist, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.LNGCoveredNormal, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.DG2Covered, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.OverloadCompletionIllegal, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadSpare:to_path=LNGShipEMS.BatteryAssist, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadSpare:to_path=LNGShipEMS.LNGCoveredNormal, ... +42`。
- before_dsl_hash：`sha256:180df4cf113445e8e8ed80c4a7699aec96a916a393847d1d19d37639fb3a5a13`；candidate_dsl_hash：`sha256:372f20d03a9f02ee8ffc77cc2d117143e9863993c6619dc4a7cecf3d4bd1110d`。

#### 错误证据 / diagnostics

- 1. `W_UNWRITTEN_READ_VAR` `W_UNWRITTEN_READ_VAR:var_name=Pd2max` policy=`budgeted_repair`：Variable 'Pd2max' is read but never written by any action or transition effect.；refs=`{"init_value": "0.0", "read_states": ["LNGShipEMS.BatteryAssist", "LNGShipEMS.DG1CoveredNormal", "LNGShipEMS.DG1LowSoCChargeMargin", "LNGShipEMS.DG2Covered", "LNGShipEMS.IdleNoLoad", "LNGShipEMS.LNGAndEngine3Covered", "LNGShipEMS.LNGCoveredLowSoCChargeMargin", "LNGShipEMS.LNGCoveredNormal", "LNGShip...<truncated 170 chars>`
- 2. `W_UNWRITTEN_READ_VAR` `W_UNWRITTEN_READ_VAR:var_name=Pbat_Pmax` policy=`budgeted_repair`：Variable 'Pbat_Pmax' is read but never written by any action or transition effect.；refs=`{"init_value": "0.0", "read_states": ["LNGShipEMS.BatteryAssist", "LNGShipEMS.DG1CoveredNormal", "LNGShipEMS.DG1LowSoCChargeMargin", "LNGShipEMS.DG2Covered", "LNGShipEMS.IdleNoLoad", "LNGShipEMS.LNGAndEngine3Covered", "LNGShipEMS.LNGCoveredLowSoCChargeMargin", "LNGShipEMS.LNGCoveredNormal", "LNGShip...<truncated 173 chars>`
- 3. `W_GUARD_VARS_NEVER_CHANGE` `W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.IdleNoLoad:to_path=LNGShipEMS.BatteryAssist` policy=`budgeted_repair`：Transition guard reads only variables that are never changed by actions or effects.；refs=`{"from_path": "LNGShipEMS.IdleNoLoad", "guard_vars": ["PL", "Pbat_Pmax", "Ppv", "Pw", "SoC"], "to_path": "LNGShipEMS.BatteryAssist"}`
- 4. `W_GUARD_VARS_NEVER_CHANGE` `W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.IdleNoLoad:to_path=LNGShipEMS.LNGCoveredNormal` policy=`budgeted_repair`：Transition guard reads only variables that are never changed by actions or effects.；refs=`{"from_path": "LNGShipEMS.IdleNoLoad", "guard_vars": ["PL", "Pbat_Pmax", "Pgmax", "Ppv", "Pw", "SoC"], "to_path": "LNGShipEMS.LNGCoveredNormal"}`
- 5. `W_GUARD_VARS_NEVER_CHANGE` `W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.IdleNoLoad:to_path=LNGShipEMS.DG2Covered` policy=`budgeted_repair`：Transition guard reads only variables that are never changed by actions or effects.；refs=`{"from_path": "LNGShipEMS.IdleNoLoad", "guard_vars": ["PL", "Pd1max", "Pd2max", "Pgmax", "Ppv", "Pw", "eng3_Pmax"], "to_path": "LNGShipEMS.DG2Covered"}`
- 6. `W_GUARD_VARS_NEVER_CHANGE` `W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.IdleNoLoad:to_path=LNGShipEMS.OverloadCompletionIllegal` policy=`budgeted_repair`：Transition guard reads only variables that are never changed by actions or effects.；refs=`{"from_path": "LNGShipEMS.IdleNoLoad", "guard_vars": ["PL", "Pd1max", "Pd2max", "Pgmax", "Ppv", "Pw", "eng3_Pmax"], "to_path": "LNGShipEMS.OverloadCompletionIllegal"}`
- 7. `W_GUARD_VARS_NEVER_CHANGE` `W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.BatteryAssist` policy=`budgeted_repair`：Transition guard reads only variables that are never changed by actions or effects.；refs=`{"from_path": "LNGShipEMS.ZeroLoadCharge", "guard_vars": ["PL", "Pbat_Pmax", "Ppv", "Pw", "SoC"], "to_path": "LNGShipEMS.BatteryAssist"}`
- 8. `W_GUARD_VARS_NEVER_CHANGE` `W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.LNGCoveredNormal` policy=`budgeted_repair`：Transition guard reads only variables that are never changed by actions or effects.；refs=`{"from_path": "LNGShipEMS.ZeroLoadCharge", "guard_vars": ["PL", "Pbat_Pmax", "Pgmax", "Ppv", "Pw", "SoC"], "to_path": "LNGShipEMS.LNGCoveredNormal"}`
- ……另有 `46` 条 evidence 见 run record。

#### SD-8 fix plan / 修改建议

- recommended_strategy：Use diagnostics as hints; choose the smallest globally consistent repair.；Before returning a candidate, verify every required_preserve_element_id still has a concrete DSL representation.
- hint 1：The variable is used as input but never updated after its initial definition, so model behavior may be accidentally constant.；`actions=add_write, simplify_guard；do_not=Do not add a meaningless self-assignment.`
- hint 2：The variable is used as input but never updated after its initial definition, so model behavior may be accidentally constant.；`actions=add_write, simplify_guard；do_not=Do not add a meaningless self-assignment.`
- hint 3：This guard is controlled only by initial variable values. If those values never change, the transition condition is effectively fixed.；`actions=add_write, simplify_guard；do_not=Do not add a meaningless self-assignment; it does not model a real change., Do not rewrite the guard to a meaningless constant only to silence this diagnostic.`
- hint 4：This guard is controlled only by initial variable values. If those values never change, the transition condition is effectively fixed.；`actions=add_write, simplify_guard；do_not=Do not add a meaningless self-assignment; it does not model a real change., Do not rewrite the guard to a meaningless constant only to silence this diagnostic.`
- hint 5：This guard is controlled only by initial variable values. If those values never change, the transition condition is effectively fixed.；`actions=add_write, simplify_guard；do_not=Do not add a meaningless self-assignment; it does not model a real change., Do not rewrite the guard to a meaningless constant only to silence this diagnostic.`
- hint 6：This guard is controlled only by initial variable values. If those values never change, the transition condition is effectively fixed.；`actions=add_write, simplify_guard；do_not=Do not add a meaningless self-assignment; it does not model a real change., Do not rewrite the guard to a meaningless constant only to silence this diagnostic.`
- forbidden_edits：`Do not delete grounded required elements merely to silence diagnostics., Do not invent internal plant/environment dynamics merely to make external input variables appear written.`。
- required_preserve_element_ids：`state:LNGShipEMS, variable:PL, variable:Ppv, variable:Pw, variable:SoC, variable:eng3_Pmax, variable:Pgmax, variable:Pd1max, variable:Pgen_req, variable:Pbat_discharge, variable:Pbat_charge, variable:Pspare, ... +24`。

#### SL-9 candidate / 最终修改执行方案

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
def float Pgen_req = 0.0;
def float Pbat_discharge = 0.0;
def float Pbat_charge = 0.0;
def float Pspare = 0.0;
def int cut_in_LNG = 0;
def int cut_in_engine3 = 0;
def int cut_in_DG1 = 0;
def int cut_in_DG2 = 0;
def int cut_in_battery = 0;
def int cut_out_load = 0;

state LNGShipEMS {
    ! * -> IdleNoLoad : if [PL == 0 && Ppv + Pw == 0];
    ! * -> ZeroLoadCharge : if [PL == 0 && Ppv + Pw > 0 && SoC < 0.95];
    ! * -> ZeroLoadSpare : if [PL == 0 && Ppv + Pw > 0 && SoC >= 0.95];
    ! * -> RESCoversCharge : if [PL > 0 && Ppv + Pw >= PL && SoC < 0.95];
    ! * -> RESCoversSpare : if [PL > 0 && Ppv + Pw >= PL && SoC >= 0.95];
    ! * -> BatteryAssist : if [PL > 0 && Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw <= Pbat_Pmax];
    ! * -> LNGCoveredLowSoCChargeMargin : if [PL > 0 && Ppv + Pw < PL && SoC < 0.2 && PL - Ppv - Pw + Pgmax / 5 <= Pgmax];
    ! * -> LNGCoveredNormal : if [PL > 0 && Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw > Pbat_Pmax && PL - Ppv - Pw <= Pgmax];
    ! * -> LNGAndEngine3Covered : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > Pgmax && PL - Ppv - Pw <= Pgmax + eng3_Pmax];
    ! * -> DG1LowSoCChargeMargin : if [PL > 0 && Ppv + Pw < PL && SoC < 0.2 && PL - Ppv - Pw > Pgmax + eng3_Pmax && PL - Ppv - Pw + Pd1max / 10 <= Pgmax + eng3_Pmax + Pd1max];
    ! * -> DG1CoveredNormal : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > Pgmax + eng3_Pmax && PL - Ppv - Pw <= Pgmax + eng3_Pmax + Pd1max && (SoC >= 0.2 || PL - Ppv - Pw + Pd1max / 10 > Pgmax + eng3_Pmax + Pd1max)];
    ! * -> DG2Covered : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > Pgmax + eng3_Pmax + Pd1max && PL - Ppv - Pw <= Pgmax + eng3_Pmax + Pd1max + Pd2max];
    ! * -> OverloadCompletionIllegal : if [PL > 0 && PL < 0.0 && Ppv + Pw < PL && PL - Ppv - Pw > Pgmax + eng3_Pmax + Pd1max + Pd2max];

    [*] -> IdleNoLoad;

    state IdleNoLoad {
        enter {
            Pgen_req = 0.0;
            Pbat_discharge = 0.0;
            Pbat_charge = 0.0;
            Pspare = 0.0;
            cut_in_LNG = 0;
            cut_in_engine3 = 0;
            cut_in_DG1 = 0;
            cut_in_DG2 = 0;
            cut_in_battery = 0;
            cut_out_load = 0;
        }
    }

    state ZeroLoadCharge {
        enter {
            Pgen_req = 0.0;
            Pbat_discharge = 0.0;
            Pbat_charge = Ppv + Pw;
            Pspare = 0.0;
            cut_in_LNG = 0;
            cut_in_engine3 = 0;
            cut_in_DG1 = 0;
            cut_in_DG2 = 0;
            cut_in_battery = 1;
            cut_out_load = 0;
        }
    }

    state ZeroLoadSpare {
        enter {
            Pgen_req = 0.0;
            Pbat_discharge = 0.0;
            Pbat_charge = 0.0;
            Pspare = Ppv + Pw;
            cut_in_LNG = 0;
            cut_in_engine3 = 0;
            cut_in_DG1 = 0;
            cut_in_DG2 = 0;
            cut_in_battery = 0;
            cut_out_load = 0;
        }
    }

    state RESCoversCharge {
        enter {
            Pgen_req = 0.0;
            Pbat_discharge = 0.0;
            Pbat_charge = Ppv + Pw - PL;
            Pspare = 0.0;
            cut_in_LNG = 0;
            cut_in_engine3 = 0;
            cut_in_DG1 = 0;
            cut_in_DG2 = 0;
            cut_in_battery = 1;
            cut_out_load = 0;
        }
    }

    state RESCoversSpare {
        enter {
            Pgen_req = 0.0;
            Pbat_discharge = 0.0;
            Pbat_charge = 0.0;
            Pspare = Ppv + Pw - PL;
            cut_in_LNG = 0;
            cut_in_engine3 = 0;
            cut_in_DG1 = 0;
            cut_in_DG2 = 0;
            cut_in_battery = 0;
            cut_out_load = 0;
        }
    }

    state BatteryAssist {
        enter {
            Pgen_req = 0.0;
            Pbat_discharge = PL - Ppv - Pw;
            Pbat_charge = 0.0;
            Pspare = 0.0;
            cut_in_LNG = 0;
            cut_in_engine3 = 0;
            cut_in_DG1 = 0;
            cut_in_DG2 = 0;
            cut_in_battery = 1;
            cut_out_load = 0;
        }
    }

    state LNGCoveredLowSoCChargeMargin {
        enter {
            Pgen_req = PL - Ppv - Pw + Pgmax / 5;
            Pbat_discharge = 0.0;
            Pbat_charge = Pgmax / 5;
            Pspare = 0.0;
            cut_in_LNG = 1;
            cut_in_engine3 = 0;
            cut_in_DG1 = 0;
            cut_in_DG2 = 0;
            cut_in_battery = 1;
            cut_out_load = 0;
        }
    }

    state LNGCoveredNormal {
        enter {
            Pgen_req = PL - Ppv - Pw;
            Pbat_discharge = 0.0;
            Pbat_charge = 0.0;
            Pspare = 0.0;
            cut_in_LNG = 1;
            cut_in_engine3 = 0;
            cut_in_DG1 = 0;
            cut_in_DG2 = 0;
            cut_in_battery = 0;
            cut_out_load = 0;
        }
    }

    state LNGAndEngine3Covered {
        enter {
            Pgen_req = PL - Ppv - Pw;
            Pbat_discharge = 0.0;
            Pbat_charge = 0.0;
            Pspare = 0.0;
            cut_in_LNG = 1;
            cut_in_engine3 = 1;
            cut_in_DG1 = 0;
            cut_in_DG2 = 0;
            cut_in_battery = 0;
            cut_out_load = 0;
        }
    }

    state DG1LowSoCChargeMargin {
        enter {
            Pgen_req = PL - Ppv - Pw + Pd1max / 10;
            Pbat_discharge = 0.0;
            Pbat_charge = Pd1max / 10;
            Pspare = 0.0;
            cut_in_LNG = 1;
            cut_in_engine3 = 1;
            cut_in_DG1 = 1;
            cut_in_DG2 = 0;
            cut_in_battery = 1;
            cut_out_load = 0;
        }
    }

    state DG1CoveredNormal {
        enter {
            Pgen_req = PL - Ppv - Pw;
            Pbat_discharge = 0.0;
            Pbat_charge = 0.0;
            Pspare = 0.0;
            cut_in_LNG = 1;
            cut_in_engine3 = 1;
            cut_in_DG1 = 1;
            cut_in_DG2 = 0;
            cut_in_battery = 0;
            cut_out_load = 0;
        }
    }

    state DG2Covered {
        enter {
            Pgen_req = PL - Ppv - Pw;
            Pbat_discharge = 0.0;
            Pbat_charge = 0.0;
            Pspare = 0.0;
            cut_in_LNG = 1;
            cut_in_engine3 = 1;
            cut_in_DG1 = 1;
            cut_in_DG2 = 1;
            cut_in_battery = 0;
            cut_out_load = 0;
        }
    }

    state OverloadCompletionIllegal {
        enter {
            Pgen_req = Pgmax + eng3_Pmax + Pd1max + Pd2max;
            Pbat_discharge = PL - Ppv - Pw - Pgmax - eng3_Pmax - Pd1max - Pd2max;
            Pbat_charge = 0.0;
            Pspare = 0.0;
            cut_in_LNG = 1;
            cut_in_engine3 = 1;
            cut_in_DG1 = 1;
            cut_in_DG2 = 1;
            cut_in_battery = 1;
            cut_out_load = 0;
        }

        [*] -> CompletionForbidden;
        pseudo state CompletionForbidden;
        CompletionForbidden -> [*];
    }
}
```

#### Candidate diff（before -> candidate）

```diff
--- before.fcstm
+++ candidate.fcstm
@@ -25,13 +25,13 @@
     ! * -> RESCoversCharge : if [PL > 0 && Ppv + Pw >= PL && SoC < 0.95];
     ! * -> RESCoversSpare : if [PL > 0 && Ppv + Pw >= PL && SoC >= 0.95];
     ! * -> BatteryAssist : if [PL > 0 && Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw <= Pbat_Pmax];
-    ! * -> LNGCoveredLowSoCChargeMargin : if [PL > 0 && Ppv + Pw < PL && SoC < 0.2 && PL - Ppv - Pw <= Pgmax];
+    ! * -> LNGCoveredLowSoCChargeMargin : if [PL > 0 && Ppv + Pw < PL && SoC < 0.2 && PL - Ppv - Pw + Pgmax / 5 <= Pgmax];
     ! * -> LNGCoveredNormal : if [PL > 0 && Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw > Pbat_Pmax && PL - Ppv - Pw <= Pgmax];
     ! * -> LNGAndEngine3Covered : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > Pgmax && PL - Ppv - Pw <= Pgmax + eng3_Pmax];
     ! * -> DG1LowSoCChargeMargin : if [PL > 0 && Ppv + Pw < PL && SoC < 0.2 && PL - Ppv - Pw > Pgmax + eng3_Pmax && PL - Ppv - Pw + Pd1max / 10 <= Pgmax + eng3_Pmax + Pd1max];
     ! * -> DG1CoveredNormal : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > Pgmax + eng3_Pmax && PL - Ppv - Pw <= Pgmax + eng3_Pmax + Pd1max && (SoC >= 0.2 || PL - Ppv - Pw + Pd1max / 10 > Pgmax + eng3_Pmax + Pd1max)];
     ! * -> DG2Covered : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > Pgmax + eng3_Pmax + Pd1max && PL - Ppv - Pw <= Pgmax + eng3_Pmax + Pd1max + Pd2max];
-    ! * -> OverloadCompletionIllegal : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > Pgmax + eng3_Pmax + Pd1max + Pd2max];
+    ! * -> OverloadCompletionIllegal : if [PL > 0 && PL < 0.0 && Ppv + Pw < PL && PL - Ppv - Pw > Pgmax + eng3_Pmax + Pd1max + Pd2max];
 
     [*] -> IdleNoLoad;
 
@@ -226,7 +226,11 @@
             cut_in_DG1 = 1;
             cut_in_DG2 = 1;
             cut_in_battery = 1;
-            cut_out_load = 1;
-        }
+            cut_out_load = 0;
+        }
+
+        [*] -> CompletionForbidden;
+        pseudo state CompletionForbidden;
+        CompletionForbidden -> [*];
     }
 }
```

#### SD-10 / SL-10B 审查结果

- SD-10 ok=`False`，target_resolved=`False`，regression_detected=`True`，drift_risk=`major`。
- local_rejection：reason=`new_blocking_design_diagnostic; scenario_regression; forced_transition_count_drift; missing_required_grounding`，rejected_by_stage=`SD-10`。
  - local evidence 1: `new_blocking_design_diagnostic` {"items": [{"budget_exhausted": false, "budget_remaining": 2, "code": "W_GUARD_VARS_NEVER_CHANGE", "instance_key": "W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.OverloadCompletionIllegal.CompletionForbidden:to_path=[*]", "message": "Transition guard reads only variables that are never changed by actions or effects.", "policy_action": "budgeted_repair", "pyfcstm_severity": "warning", "rationale": "", "refs": {"from_path": "LNGShipEMS.OverloadCompletionIllegal.CompletionForbidden", "guard_vars":...<truncated 4518 chars>
  - local evidence 2: `scenario_regression` {"kind": "scenario_regression", "sim_feedback": {"n_scenarios": 12, "n_scenarios_passed": 11, "ok": false, "oracle_weak": false, "scenario_results": [{"description": "default-init probe: first cycle must dispatch to IdleNoLoad, then zero load with RES and SoC below 0.95 must transition to battery charging.", "name": "default_init_then_zero_load_charge", "setup_error": null, "status": "pass", "step_results": [{"actual_state": "LNGShipEMS.IdleNoLoad", "actual_vars": {"PL": 0.0, "Pbat_Pmax": 5.0, "...<truncated 10139 chars>
  - local evidence 3: `forced_transition_count_drift` {"fix_target": "design", "kind": "forced_transition_count_drift", "new": 182, "old": 169}
  - local evidence 4: `missing_required_grounding` {"element_ids": ["transition:*->RESCoversCharge", "transition:*->RESCoversSpare", "transition:*->ZeroLoadCharge", "transition:*->ZeroLoadSpare", "transition:*->BatteryAssist", "transition:*->LNGCoveredLowSoCChargeMargin", "transition:*->DG1LowSoCChargeMargin", "transition:*->OverloadCompletionIllegal"], "kind": "missing_required_grounding"}
- SL-10B delta_review：`<none>`（通常是 SD-10 本地审查已拒绝，未进入 LLM delta review）。

</details>


### 8. 尝试记录与成本

- `SL-1`：retry_count=`0`，schema_ok=`True`，usage=`{'completion_tokens': 8981, 'model': 'gpt-5.5', 'prompt_tokens': 6213, 'total_tokens': 15194}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-9`：retry_count=`0`，schema_ok=`True`，usage=`{'completion_tokens': 4960, 'model': 'gpt-5.5', 'prompt_tokens': 132659, 'total_tokens': 137619}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-9`：retry_count=`0`，schema_ok=`True`，usage=`{'completion_tokens': 3027, 'model': 'gpt-5.5', 'prompt_tokens': 132524, 'total_tokens': 135551}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'completion_tokens': 5744, 'model': 'gpt-5.5', 'prompt_tokens': 16652, 'total_tokens': 22396}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-7`：retry_count=`0`，schema_ok=`True`，usage=`{'completion_tokens': 3692, 'model': 'gpt-5.5', 'prompt_tokens': 51201, 'total_tokens': 54893}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-9`：retry_count=`0`，schema_ok=`True`，usage=`{'completion_tokens': 4727, 'model': 'gpt-5.5', 'prompt_tokens': 46503, 'total_tokens': 51230}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-7`：retry_count=`0`，schema_ok=`True`，usage=`{'completion_tokens': 3008, 'model': 'gpt-5.5', 'prompt_tokens': 51201, 'total_tokens': 54209}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-9`：retry_count=`0`，schema_ok=`True`，usage=`{'completion_tokens': 4708, 'model': 'gpt-5.5', 'prompt_tokens': 51287, 'total_tokens': 55995}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-7`：retry_count=`0`，schema_ok=`True`，usage=`{'completion_tokens': 4331, 'model': 'gpt-5.5', 'prompt_tokens': 51201, 'total_tokens': 55532}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-9`：retry_count=`0`，schema_ok=`True`，usage=`{'completion_tokens': 4382, 'model': 'gpt-5.5', 'prompt_tokens': 46770, 'total_tokens': 51152}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。

### 9. 最终停止状态与后续含义

- 停止状态：verdict=`not_converged`，record_status=`rejected`。
- 主要原因分类：`semantic_or_topology`。
- required stages executed：`52/17`，missing=`SL-10B`。
- repairs：`0/5` accepted；scenario_history=`3`。
- 配置含义：`recommended baseline candidate`；该结果可用于评估默认入口本身。
- 样本含义：若出现 `design_or_variable_dynamics`，应重点审查变量是否仅作为 guard/input 常量而没有事件/动作更新；若出现 pre-scenario parse/semantic 失败，则应先优化 pyfcstm grammar adherence。
