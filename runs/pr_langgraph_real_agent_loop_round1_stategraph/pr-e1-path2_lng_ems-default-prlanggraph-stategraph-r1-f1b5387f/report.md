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
| Git commit | `d6f724e5739a8979f426efed06e33626e6953eed` |
| clean / diff / prompt snapshot | clean=`True`, dirty=`False`, diff_hash=`sha256:2a69ad5797ac568a81bddcef615104303a97261094685f4edd8d4484e889ea09`, prompt_hash=`sha256:993dd2a89560dc22cd287bbf50c2cbe6faab9e99a63729d53f02e0d42085b247` |
| provider/model 脱敏标识 | mode=`real_env`, model=`gpt-5.5`, real_api=`True` |
| source / paper | source=`project_1_llm_state_machine_modeling/sources/state-transitions-logical-design-for-hybrid-energy-generation-with-renewable-energy-sources-in-lng-ship`, paper=`project_1_llm_state_machine_modeling/sources/state-transitions-logical-design-for-hybrid-energy-generation-with-renewable-energy-sources-in-lng-ship/paper.pdf` |
| 样本筛选理由 | issue #14 / PR-D 代表性 Path2 EFSM，变量、guard、12 个状态和非法状态都明确；但它可能退化为条件分类式 dispatch，因此更适合作为 FE/BVS 压力测试，是否适合作为 Path2 ref-model 蓝本需看最终 DSL 是否具有 state-dependent mode memory。 |
| 变量参与说明 | `PL/Ppv/Pw/SoC/eng*_Pmax` 是环境输入/容量边界，适合暴露 SD-4 对外部输入变量的处理能力。 |
| run_id | `pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f` |
| final verdict/status | verdict=`success`, record=`success`, result=`converged` |
| main_result_eligible | `false` |
| state_mode_decorative_detected | `true` |
| path2_ref_model_blueprint_eligible | `false`；run_not_main_result_eligible |
| final.fcstm 来源 | `{"accepted": true, "accepted_after_rework": false, "final_dsl_hash": "sha256:4b52356070e7a51d779df874526281152b5fb3e1dac5b2f71a14dc2af9ccf364", "iteration": 3, "last_rejected_candidate": {"candidate_dsl_hash": "sha256:4c5a6347ae4632bd2b168c1d08eef85bdcfb190e6335c8e955fb8d53d02b8d19", "iteration": 2, "repair_history_index": 2, "rework_instructions": ["SL-10 pass was downgraded because local deterministic evidence reported major drift and SL-10 evidence did not explicitly address the local rejection reason/kind with a structured local_override_rationale.", "For the next SL-9 repair, do not blindly regenerate the same DSL. Either change the candidate so the local major-drift evidence is resolved, or keep the minimal DSL only with explicit repair_rationale mapping each local objection (for example missing_required_grounding, scenario_regression, count_drift, or forced_transition_count_drift) to concrete NL-grounded states/transitions/actions that remain in the candidate. This rationale is required so SL-10 can produce local_override_rationale instead of cycling."], "same_as_final": false, "sl10_decision": "rework"}, "matching_repair_history_indices": [4], "repair_history_index": 4, "selected_source_stage": "SL-7", "sl10_decision": "pass", "source_kind": "repair_candidate"}` |
| FixLog next_action 序列 | `sl9_decision_and_repair, sl10_review, sc11_accept_then_sd2, sl9_decision_and_repair, reject_or_waiver, continue_after_waiver, sl9_decision_and_repair, sl10_review, sl9_rework, sl10_review, sc11_accept_then_sd2, sl9_decision_and_repair, ... +2` |
| iteration exit_reason 序列 | `candidate_accepted_for_next_full_pass, waiver_continue_revealed_downstream_blocking_feedback, candidate_accepted_for_next_full_pass, candidate_accepted_for_next_full_pass, full_pass_all_required_feedback_ok` |
| token/cost/time | tokens=`{'prompt_tokens': 843981, 'completion_tokens': 99686, 'total_tokens': 943667, 'estimated_prompt_tokens': 835132, 'estimated_completion_tokens': 66540, 'estimated_total_tokens': 901672, 'prompt_chars': 3340501, 'completion_chars': 266135, 'n_calls': 21, 'token_usage_available': True, 'token_usage_unavailable_calls': 0}`, elapsed=`1888.78s` |
| run record | [`pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |
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
def float SoC = 0.50;
def float Pgmax = 0.0;
def float eng3_Pmax = 0.0;
def float Pd1max = 0.0;
def float Pd2max = 0.0;
def float Pbat_discharge_Pmax = 0.0;
def float Pgen_req = 0.0;
def float PLNG_req = 0.0;
def float PENG3_req = 0.0;
def float PDG1_req = 0.0;
def float PDG2_req = 0.0;
def float Pbat_discharge = 0.0;
def float Pbat_charge = 0.0;
def float Pspare = 0.0;
def int cutin_LNG = 0;
def int cutout_LNG = 0;
def int cutin_ENG3 = 0;
def int cutout_ENG3 = 0;
def int cutin_DG1 = 0;
def int cutout_DG1 = 0;
def int cutin_DG2 = 0;
def int cutout_DG2 = 0;
def int load_cutout = 0;

state LNGShipEMS {
    ! * -> IllegalOverloadCompletion : if [PL - Ppv - Pw > Pgmax + eng3_Pmax + Pd1max + Pd2max];
    ! * -> ZeroLoad_RES_Charge : if [PL == 0 && Ppv + Pw > 0 && SoC < 0.95];
    ! * -> ZeroLoad_RES_Spare : if [PL == 0 && Ppv + Pw > 0 && SoC >= 0.95];
    ! * -> ZeroLoad_RES_Spare : if [PL == 0 && Ppv + Pw <= 0];
    ! * -> RES_Covers_Load_Charge : if [PL > 0 && Ppv + Pw >= PL && SoC < 0.95];
    ! * -> RES_Covers_Load_Spare : if [PL > 0 && Ppv + Pw >= PL && SoC >= 0.95];
    ! * -> Battery_Discharge_Priority : if [PL > 0 && Ppv + Pw < PL && SoC >= 0.20 && PL - Ppv - Pw <= Pbat_discharge_Pmax];
    ! * -> LNG_Covers_Load_LowSoC_ChargeMargin : if [PL > 0 && Ppv + Pw < PL && SoC < 0.20 && PL - Ppv - Pw + Pgmax / 5 <= Pgmax];
    ! * -> LNG_Covers_Load : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw <= Pgmax && (SoC < 0.20 || PL - Ppv - Pw > Pbat_discharge_Pmax)];
    ! * -> LNG_Engine3_Covers_Load : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > Pgmax && PL - Ppv - Pw <= Pgmax + eng3_Pmax];
    ! * -> DG1_Covers_Load_LowSoC_ChargeMargin : if [PL > 0 && Ppv + Pw < PL && SoC < 0.20 && PL - Ppv - Pw > Pgmax + eng3_Pmax && PL - Ppv - Pw + Pd1max / 10 <= Pgmax + eng3_Pmax + Pd1max];
    ! * -> DG1_Covers_Load : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > Pgmax + eng3_Pmax && PL - Ppv - Pw <= Pgmax + eng3_Pmax + Pd1max];
    ! * -> DG2_Covers_Load_WithOptionalChargeMargin : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > Pgmax + eng3_Pmax + Pd1max && PL - Ppv - Pw <= Pgmax + eng3_Pmax + Pd1max + Pd2max];

    [*] -> ZeroLoad_RES_Charge;

    state ZeroLoad_RES_Charge {
        enter {
            Pgen_req = 0;
            PLNG_req = 0;
            PENG3_req = 0;
            PDG1_req = 0;
            PDG2_req = 0;
            Pbat_discharge = 0;
            Pbat_charge = Ppv + Pw;
            Pspare = 0;
            cutin_LNG = 0;
            cutout_LNG = 1;
            cutin_ENG3 = 0;
            cutout_ENG3 = 1;
            cutin_DG1 = 0;
            cutout_DG1 = 1;
            cutin_DG2 = 0;
            cutout_DG2 = 1;
            load_cutout = 0;
        }
    }

    state ZeroLoad_RES_Spare {
        enter {
            Pgen_req = 0;
            PLNG_req = 0;
            PENG3_req = 0;
            PDG1_req = 0;
            PDG2_req = 0;
            Pbat_discharge = 0;
            Pbat_charge = 0;
            Pspare = Ppv + Pw;
            cutin_LNG = 0;
            cutout_LNG = 1;
            cutin_ENG3 = 0;
            cutout_ENG3 = 1;
            cutin_DG1 = 0;
            cutout_DG1 = 1;
            cutin_DG2 = 0;
            cutout_DG2 = 1;
            load_cutout = 0;
        }
    }

    state RES_Covers_Load_Charge {
        enter {
            Pgen_req = 0;
            PLNG_req = 0;
            PENG3_req = 0;
            PDG1_req = 0;
            PDG2_req = 0;
            Pbat_discharge = 0;
            Pbat_charge = Ppv + Pw - PL;
            Pspare = 0;
            cutin_LNG = 0;
            cutout_LNG = 1;
            cutin_ENG3 = 0;
            cutout_ENG3 = 1;
            cutin_DG1 = 0;
            cutout_DG1 = 1;
            cutin_DG2 = 0;
            cutout_DG2 = 1;
            load_cutout = 0;
        }
    }

    state RES_Covers_Load_Spare {
        enter {
            Pgen_req = 0;
            PLNG_req = 0;
            PENG3_req = 0;
            PDG1_req = 0;
            PDG2_req = 0;
            Pbat_discharge = 0;
            Pbat_charge = 0;
            Pspare = Ppv + Pw - PL;
            cutin_LNG = 0;
            cutout_LNG = 1;
            cutin_ENG3 = 0;
            cutout_ENG3 = 1;
            cutin_DG1 = 0;
            cutout_DG1 = 1;
            cutin_DG2 = 0;
            cutout_DG2 = 1;
            load_cutout = 0;
        }
    }

    state Battery_Discharge_Priority {
        enter {
            Pgen_req = 0;
            PLNG_req = 0;
            PENG3_req = 0;
            PDG1_req = 0;
            PDG2_req = 0;
            Pbat_discharge = PL - Ppv - Pw;
            Pbat_charge = 0;
            Pspare = 0;
            cutin_LNG = 0;
            cutout_LNG = 1;
            cutin_ENG3 = 0;
            cutout_ENG3 = 1;
            cutin_DG1 = 0;
            cutout_DG1 = 1;
            cutin_DG2 = 0;
            cutout_DG2 = 1;
            load_cutout = 0;
        }
    }

    state LNG_Covers_Load {
        enter {
            Pgen_req = PL - Ppv - Pw;
            PLNG_req = PL - Ppv - Pw;
            PENG3_req = 0;
            PDG1_req = 0;
            PDG2_req = 0;
            Pbat_discharge = 0;
            Pbat_charge = 0;
            Pspare = 0;
            cutin_LNG = 1;
            cutout_LNG = 0;
            cutin_ENG3 = 0;
            cutout_ENG3 = 1;
            cutin_DG1 = 0;
            cutout_DG1 = 1;
            cutin_DG2 = 0;
            cutout_DG2 = 1;
            load_cutout = 0;
        }
    }

    state LNG_Covers_Load_LowSoC_ChargeMargin {
        enter {
            Pgen_req = PL - Ppv - Pw + Pgmax / 5;
            PLNG_req = PL - Ppv - Pw + Pgmax / 5;
            PENG3_req = 0;
            PDG1_req = 0;
            PDG2_req = 0;
            Pbat_discharge = 0;
            Pbat_charge = Pgmax / 5;
            Pspare = 0;
            cutin_LNG = 1;
            cutout_LNG = 0;
            cutin_ENG3 = 0;
            cutout_ENG3 = 1;
            cutin_DG1 = 0;
            cutout_DG1 = 1;
            cutin_DG2 = 0;
            cutout_DG2 = 1;
            load_cutout = 0;
        }
    }

    state LNG_Engine3_Covers_Load {
        enter {
            Pgen_req = PL - Ppv - Pw;
            PLNG_req = Pgmax;
            PENG3_req = PL - Ppv - Pw - Pgmax;
            PDG1_req = 0;
            PDG2_req = 0;
            Pbat_discharge = 0;
            Pbat_charge = 0;
            Pspare = 0;
            cutin_LNG = 1;
            cutout_LNG = 0;
            cutin_ENG3 = 1;
            cutout_ENG3 = 0;
            cutin_DG1 = 0;
            cutout_DG1 = 1;
            cutin_DG2 = 0;
            cutout_DG2 = 1;
            load_cutout = 0;
        }
    }

    state DG1_Covers_Load {
        enter {
            Pgen_req = PL - Ppv - Pw;
            PLNG_req = Pgmax;
            PENG3_req = eng3_Pmax;
            PDG1_req = PL - Ppv - Pw - Pgmax - eng3_Pmax;
            PDG2_req = 0;
            Pbat_discharge = 0;
            Pbat_charge = 0;
            Pspare = 0;
            cutin_LNG = 1;
            cutout_LNG = 0;
            cutin_ENG3 = 1;
            cutout_ENG3 = 0;
            cutin_DG1 = 1;
            cutout_DG1 = 0;
            cutin_DG2 = 0;
            cutout_DG2 = 1;
            load_cutout = 0;
        }
    }

    state DG1_Covers_Load_LowSoC_ChargeMargin {
        enter {
            Pgen_req = PL - Ppv - Pw + Pd1max / 10;
            PLNG_req = Pgmax;
            PENG3_req = eng3_Pmax;
            PDG1_req = PL - Ppv - Pw - Pgmax - eng3_Pmax + Pd1max / 10;
            PDG2_req = 0;
            Pbat_discharge = 0;
            Pbat_charge = Pd1max / 10;
            Pspare = 0;
            cutin_LNG = 1;
            cutout_LNG = 0;
            cutin_ENG3 = 1;
            cutout_ENG3 = 0;
            cutin_DG1 = 1;
            cutout_DG1 = 0;
            cutin_DG2 = 0;
            cutout_DG2 = 1;
            load_cutout = 0;
        }
    }

    state DG2_Covers_Load_WithOptionalChargeMargin {
        enter {
            if [SoC < 0.20] {
                Pgen_req = PL - Ppv - Pw + Pd1max / 10;
                PLNG_req = Pgmax;
                PENG3_req = eng3_Pmax;
                PDG1_req = Pd1max;
                PDG2_req = PL - Ppv - Pw - Pgmax - eng3_Pmax - Pd1max + Pd1max / 10;
                Pbat_charge = Pd1max / 10;
            } else {
                Pgen_req = PL - Ppv - Pw;
                PLNG_req = Pgmax;
                PENG3_req = eng3_Pmax;
                PDG1_req = Pd1max;
                PDG2_req = PL - Ppv - Pw - Pgmax - eng3_Pmax - Pd1max;
                Pbat_charge = 0;
            }
            Pbat_discharge = 0;
            Pspare = 0;
            cutin_LNG = 1;
            cutout_LNG = 0;
            cutin_ENG3 = 1;
            cutout_ENG3 = 0;
            cutin_DG1 = 1;
            cutout_DG1 = 0;
            cutin_DG2 = 1;
            cutout_DG2 = 0;
            load_cutout = 0;
        }
    }

    state IllegalOverloadCompletion {
        enter {
            Pgen_req = Pgmax + eng3_Pmax + Pd1max + Pd2max;
            PLNG_req = Pgmax;
            PENG3_req = eng3_Pmax;
            PDG1_req = Pd1max;
            PDG2_req = Pd2max;
            Pbat_discharge = PL - Ppv - Pw - Pgmax - eng3_Pmax - Pd1max - Pd2max;
            Pbat_charge = 0;
            Pspare = 0;
            cutin_LNG = 1;
            cutout_LNG = 0;
            cutin_ENG3 = 1;
            cutout_ENG3 = 0;
            cutin_DG1 = 1;
            cutout_DG1 = 0;
            cutin_DG2 = 1;
            cutout_DG2 = 0;
            load_cutout = 1;
        }
    }
}
```

### 4. 全流程真实摘要表

| Stage | 是否 LLM | iteration | 结果 | 获取的信息 / 反馈 | 本阶段做了什么 | DSL 修改 | artifact/log |
|---|---:|---:|---:|---|---|---|---|
| `SC-0` | 否 | - | ✅ | trace/control | 初始化 run state | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |
| `SL-1` | 是 | - | ✅ | LLM calls=1, tokens=16354 | 生成初始 DSL 与 grounding seeds | initial len=9700 | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ⚠️ | blocking=136, advisory=54, info=0; blocking=50, advisory=138, info=0; blocking=0, advisory=188, info=0; blocking=0, advisory=188, info=0; blocking=0, advisory=188, info=0; blocking | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=5, tokens=295142 | LLM per-request accept/reject + repair | candidate len=9506,0,9589,9484,9548 | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=4, tokens=160081 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ⚠️ | blocking=136, advisory=54, info=0; blocking=50, advisory=138, info=0; blocking=0, advisory=188, info=0; blocking=0, advisory=188, info=0; blocking=0, advisory=188, info=0; blocking | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=5, tokens=295142 | LLM per-request accept/reject + repair | candidate len=9506,0,9589,9484,9548 | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ⚠️ | blocking=136, advisory=54, info=0; blocking=50, advisory=138, info=0; blocking=0, advisory=188, info=0; blocking=0, advisory=188, info=0; blocking=0, advisory=188, info=0; blocking | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |
| `SL-5` | 是 | 1 | ✅ | LLM calls=7, tokens=224139 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |
| `SD-5A` | 否 | 1 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |
| `SL-5` | 是 | 1 | ✅ | LLM calls=7, tokens=224139 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |
| `SD-5A` | 否 | 1 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |
| `SL-5` | 是 | 1 | ✅ | LLM calls=7, tokens=224139 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |
| `SD-5A` | 否 | 1 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |
| `SC-5F` | 否 | 1 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |
| `SD-6` | 否 | 1 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |
| `SL-7` | 是 | 1 | ✅ | LLM calls=4, tokens=247951 | LLM model review | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=136, advisory=54, info=0; blocking=50, advisory=138, info=0; blocking=0, advisory=188, info=0; blocking=0, advisory=188, info=0; blocking=0, advisory=188, info=0; blocking | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |
| `SD-5A` | 否 | 1 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |
| `SC-5F` | 否 | 1 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |
| `SD-6` | 否 | 1 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |
| `SL-7` | 是 | 1 | ✅ | LLM calls=4, tokens=247951 | LLM model review | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=5, tokens=295142 | LLM per-request accept/reject + repair | candidate len=9506,0,9589,9484,9548 | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ⚠️ | LLM calls=4, tokens=160081 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=5, tokens=295142 | LLM per-request accept/reject + repair | candidate len=9506,0,9589,9484,9548 | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=4, tokens=160081 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=136, advisory=54, info=0; blocking=50, advisory=138, info=0; blocking=0, advisory=188, info=0; blocking=0, advisory=188, info=0; blocking=0, advisory=188, info=0; blocking | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |
| `SD-5A` | 否 | 1 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |
| `SL-5` | 是 | 1 | ✅ | LLM calls=7, tokens=224139 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |
| `SD-5A` | 否 | 1 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |
| `SL-5` | 是 | 1 | ✅ | LLM calls=7, tokens=224139 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |
| `SD-5A` | 否 | 1 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |
| `SC-5F` | 否 | 1 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |
| `SD-6` | 否 | 1 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |
| `SL-7` | 是 | 1 | ✅ | LLM calls=4, tokens=247951 | LLM model review | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=5, tokens=295142 | LLM per-request accept/reject + repair | candidate len=9506,0,9589,9484,9548 | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=4, tokens=160081 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=136, advisory=54, info=0; blocking=50, advisory=138, info=0; blocking=0, advisory=188, info=0; blocking=0, advisory=188, info=0; blocking=0, advisory=188, info=0; blocking | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |
| `SD-5A` | 否 | 1 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |
| `SL-5` | 是 | 1 | ✅ | LLM calls=7, tokens=224139 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |
| `SD-5A` | 否 | 1 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |
| `SL-5` | 是 | 1 | ✅ | LLM calls=7, tokens=224139 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |
| `SD-5A` | 否 | 1 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |
| `SC-5F` | 否 | 1 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |
| `SD-6` | 否 | 1 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |
| `SL-7` | 是 | 1 | ✅ | LLM calls=4, tokens=247951 | LLM model review | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |
| `SC-12` | 否 | - | ✅ | full_pass_all_required_feedback_ok | 写 final verdict | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |
| `SC-13` | 否 | - | ✅ | trace/control | 写审计 run record | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r1-f1b5387f.agent_loop.json.gz) |

### 4.1 完整流程日志（stage/control-flow replay ledger）

口径：本节来自 `AgentLoopRunRecord.logs`，与 [`flow_log.json`](./flow_log.json) 一致；用于复现每个 stage 如何进入、得到什么批示、跳转到哪里，以及每次 DSL 产物/候选如何变化。

| # | ts | stage | iter | event | result / jump | DSL evidence |
|---:|---|---|---:|---|---|---|
| 1 | `2026-06-04T14:51:22Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 2 | `2026-06-04T14:51:22Z` | `SC-0` | `-` | `run_start` | {} | <none> |
| 3 | `2026-06-04T14:51:22Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 4 | `2026-06-04T14:51:22Z` | `SL-1` | `-` | `stage_enter` | {"reason": "initial_modeling_adapter_available"} | <none> |
| 5 | `2026-06-04T14:54:23Z` | `SL-1` | `-` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 6 | `2026-06-04T14:54:23Z` | `SL-1` | `-` | `stage_result` | {"jump": "SD-2", "ok": true} | candidate_dsl:len=9700,hash=sha256:3ea5c49f5dbb |
| 7 | `2026-06-04T14:54:23Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 8 | `2026-06-04T14:54:23Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 9 | `2026-06-04T14:54:23Z` | `<control>` | `0` | `iteration_enter` | {} | current_hash=sha256:3ea5c49f5dbb17a8d2f42b1a1b58c7e3f1687ae88f318d7b6099537ae0761375 |
| 10 | `2026-06-04T14:54:23Z` | `<control>` | `0` | `iteration_validation_enter` | {} | dsl:len=9700,hash=sha256:3ea5c49f5dbb, current_hash=sha256:3ea5c49f5dbb17a8d2f42b1a1b58c7e3f1687ae88f318d7b6099537ae0761375 |
| 11 | `2026-06-04T14:54:23Z` | `SD-2` | `0` | `stage_enter` | {"reason": "full_validation_pass"} | <none> |
| 12 | `2026-06-04T14:54:23Z` | `SD-2` | `0` | `stage_result` | {"jump": "SD-3", "ok": true, "status": "StageStatus.OK"} | <none> |
| 13 | `2026-06-04T14:54:23Z` | `SD-3` | `0` | `stage_enter` | {"reason": "SD-2 ok"} | <none> |
| 14 | `2026-06-04T14:54:23Z` | `SD-3` | `0` | `stage_result` | {"jump": "SD-4", "ok": true, "status": "StageStatus.OK"} | <none> |
| 15 | `2026-06-04T14:54:23Z` | `SD-4` | `0` | `stage_enter` | {"reason": "SD-3 ok"} | <none> |
| 16 | `2026-06-04T14:54:23Z` | `SD-4` | `0` | `stage_result` | {"jump": "SD-8", "ok": false, "status": "StageStatus.FAIL"} | <none> |
| 17 | `2026-06-04T14:54:23Z` | `<control>` | `0` | `iteration_validation_result` | {"jump": "SD-8 repair", "selected_feedback": {"blocking": true, "blocking_instance_keys": ["W_UNWRITTEN_READ_VAR:var_name=SoC_full_threshold", "W_UNWRITTEN_READ_VAR:var_name=SoC_low_threshold", "W_UNWRITTEN_READ_VAR:var_name=Pd2max", "W_UNWRITTEN_READ_VAR:var_name=Pbat_discharge_Pmax", "W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoad_RES_Charge:to_path=LNGShipEMS.IllegalOverloadCompletion", "W_GUARD_VARS_NEVE...<truncated 24813 chars> | <none> |
| 18 | `2026-06-04T14:54:23Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 19 | `2026-06-04T14:54:23Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 20 | `2026-06-04T14:54:23Z` | `SD-8` | `0` | `repair_path_enter` | {"jump": "SD-8", "selected_feedback": {"blocking": true, "blocking_instance_keys": ["W_UNWRITTEN_READ_VAR:var_name=SoC_full_threshold", "W_UNWRITTEN_READ_VAR:var_name=SoC_low_threshold", "W_UNWRITTEN_READ_VAR:var_name=Pd2max", "W_UNWRITTEN_READ_VAR:var_name=Pbat_discharge_Pmax", "W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoad_RES_Charge:to_path=LNGShipEMS.IllegalOverloadCompletion", "W_GUARD_VARS_NEVER_CHANG...<truncated 185385 chars> | current_dsl:len=9700,hash=sha256:3ea5c49f5dbb |
| 21 | `2026-06-04T14:54:23Z` | `SD-8` | `0` | `stage_result` | {"jump": "SL-9", "ok": true, "status": "StageStatus.OK"} | <none> |
| 22 | `2026-06-04T14:54:23Z` | `SD-8` | `0` | `fix_request_batch` | {"request_count": 12} | <none> |
| 23 | `2026-06-04T14:54:23Z` | `SL-9` | `0` | `stage_enter` | {"reason": "fix_requests_ready"} | old_dsl:len=9700,hash=sha256:3ea5c49f5dbb |
| 24 | `2026-06-04T14:56:05Z` | `SL-9` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 25 | `2026-06-04T14:56:05Z` | `SL-9` | `0` | `stage_result` | {"accepted_request_ids": ["fixreq-0-sd4-0-8645e8d919", "fixreq-0-sd4-1-c164939c86", "fixreq-0-sd4-5-0e2d9bb0a4", "fixreq-0-sd4-6-eaac899d48", "fixreq-0-sd4-7-5f5369f3e1", "fixreq-0-sd4-8-3a6bedb74b", "fixreq-0-sd4-9-1857623bee", "fixreq-0-sd4-10-7136bcb8d5"], "jump": "SL-10", "ok": true, "rejected_request_ids": ["fixreq-0-sd4-2-5f336aa55b", "fixreq-0-sd4-3-ae21ee3029", "fixreq-0-sd4-4-c43f6045b8", "fixreq-0-sd4-11-2d...<truncated 11 chars> | candidate_dsl:len=9506,hash=sha256:ae74dfc8a541 |
| 26 | `2026-06-04T14:56:06Z` | `SD-10` | `0` | `stage_result` | {"jump": "SL-10", "ok": false, "status": "StageStatus.FAIL"} | <none> |
| 27 | `2026-06-04T14:56:06Z` | `SL-10` | `0` | `stage_enter` | {"reason": "candidate_dsl_and_local_evidence_ready"} | candidate_hash=sha256:ae74dfc8a541f448b34f805ad6dbf46262a2b2b804509e2e7866abecbe67c8aa |
| 28 | `2026-06-04T14:56:35Z` | `SL-10` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 29 | `2026-06-04T14:56:35Z` | `SL-10` | `0` | `stage_result` | {"decision": "pass", "jump": "SC-11", "ok": true} | <none> |
| 30 | `2026-06-04T14:56:35Z` | `SL-10` | `0` | `grounding_update_hints_recorded` | {} | <none> |
| 31 | `2026-06-04T14:56:35Z` | `SC-11` | `0` | `stage_result` | {"jump": "SD-2 next iteration", "ok": true, "reason": "SL-10 accepted candidate; next iteration must restart at SD-2"} | candidate_dsl:len=9506,hash=sha256:ae74dfc8a541 |
| 32 | `2026-06-04T14:56:35Z` | `<control>` | `0` | `iteration_repair_result` | {"accepted": true, "jump": "SD-2 next iteration"} | current_hash=sha256:ae74dfc8a541f448b34f805ad6dbf46262a2b2b804509e2e7866abecbe67c8aa |
| 33 | `2026-06-04T14:56:35Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 34 | `2026-06-04T14:56:35Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 35 | `2026-06-04T14:56:35Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 36 | `2026-06-04T14:56:35Z` | `<control>` | `1` | `iteration_enter` | {} | current_hash=sha256:ae74dfc8a541f448b34f805ad6dbf46262a2b2b804509e2e7866abecbe67c8aa |
| 37 | `2026-06-04T14:56:35Z` | `<control>` | `1` | `iteration_validation_enter` | {} | dsl:len=9506,hash=sha256:ae74dfc8a541, current_hash=sha256:ae74dfc8a541f448b34f805ad6dbf46262a2b2b804509e2e7866abecbe67c8aa |
| 38 | `2026-06-04T14:56:35Z` | `SD-2` | `1` | `stage_enter` | {"reason": "full_validation_pass"} | <none> |
| 39 | `2026-06-04T14:56:35Z` | `SD-2` | `1` | `stage_result` | {"jump": "SD-3", "ok": true, "status": "StageStatus.OK"} | <none> |
| 40 | `2026-06-04T14:56:35Z` | `SD-3` | `1` | `stage_enter` | {"reason": "SD-2 ok"} | <none> |
| 41 | `2026-06-04T14:56:36Z` | `SD-3` | `1` | `stage_result` | {"jump": "SD-4", "ok": true, "status": "StageStatus.OK"} | <none> |
| 42 | `2026-06-04T14:56:36Z` | `SD-4` | `1` | `stage_enter` | {"reason": "SD-3 ok"} | <none> |
| 43 | `2026-06-04T14:56:36Z` | `SD-4` | `1` | `stage_result` | {"jump": "SD-8", "ok": false, "status": "StageStatus.FAIL"} | <none> |
| 44 | `2026-06-04T14:56:36Z` | `<control>` | `1` | `iteration_validation_result` | {"jump": "SD-8 repair", "selected_feedback": {"blocking": true, "blocking_instance_keys": ["W_UNWRITTEN_READ_VAR:var_name=Pd2max", "W_UNWRITTEN_READ_VAR:var_name=Pbat_discharge_Pmax", "W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoad_RES_Charge:to_path=LNGShipEMS.IllegalOverloadCompletion", "W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoad_RES_Charge:to_path=LNGShipEMS.Battery_Discharge_Priority", "W_GU...<truncated 14034 chars> | <none> |
| 45 | `2026-06-04T14:56:36Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 46 | `2026-06-04T14:56:36Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 47 | `2026-06-04T14:56:36Z` | `SD-8` | `1` | `repair_path_enter` | {"jump": "SD-8", "selected_feedback": {"blocking": true, "blocking_instance_keys": ["W_UNWRITTEN_READ_VAR:var_name=Pd2max", "W_UNWRITTEN_READ_VAR:var_name=Pbat_discharge_Pmax", "W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoad_RES_Charge:to_path=LNGShipEMS.IllegalOverloadCompletion", "W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoad_RES_Charge:to_path=LNGShipEMS.Battery_Discharge_Priority", "W_GUARD_VAR...<truncated 278674 chars> | current_dsl:len=9506,hash=sha256:ae74dfc8a541 |
| 48 | `2026-06-04T14:56:36Z` | `SD-8` | `1` | `stage_result` | {"jump": "SL-9", "ok": true, "status": "StageStatus.OK"} | <none> |
| 49 | `2026-06-04T14:56:36Z` | `SD-8` | `1` | `fix_request_batch` | {"request_count": 12} | <none> |
| 50 | `2026-06-04T14:56:36Z` | `SL-9` | `1` | `stage_enter` | {"reason": "fix_requests_ready"} | old_dsl:len=9506,hash=sha256:ae74dfc8a541 |
| 51 | `2026-06-04T14:57:27Z` | `SL-9` | `1` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 52 | `2026-06-04T14:57:27Z` | `SL-9` | `1` | `stage_result` | {"accepted_request_ids": [], "jump": "waiver_continue_or_exit", "ok": false, "rejected_request_ids": ["fixreq-1-sd4-0-f26560796c", "fixreq-1-sd4-1-2efb61e37b", "fixreq-1-sd4-2-005b201e59", "fixreq-1-sd4-3-463b1d2014", "fixreq-1-sd4-4-be03b849c3", "fixreq-1-sd4-5-5da41bd3dc", "fixreq-1-sd4-6-6ab31d0b6d", "fixreq-1-sd4-7-9ba6a1e517", "fixreq-1-sd4-8-3575ef8b3e", "fixreq-1-sd4-9-78b67424f0", "fixreq-1-sd4-10-e2a5930ee7"...<truncated 32 chars> | <none> |
| 53 | `2026-06-04T14:57:27Z` | `SL-9` | `1` | `sl9_all_rejected_waiver_continue` | {"jump": "continue_after_current_stage"} | <none> |
| 54 | `2026-06-04T14:57:27Z` | `<control>` | `1` | `iteration_repair_result` | {"accepted": false, "jump": "waiver_continue"} | current_hash=sha256:ae74dfc8a541f448b34f805ad6dbf46262a2b2b804509e2e7866abecbe67c8aa |
| 55 | `2026-06-04T14:57:27Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 56 | `2026-06-04T14:57:27Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 57 | `2026-06-04T14:57:27Z` | `<control>` | `1` | `waiver_continue_validation_enter` | {"reason": "SL-9 rejected/waived non-hard SD-4 requests; continue downstream without SC-11 DSL edit"} | current_dsl:len=9506,hash=sha256:ae74dfc8a541 |
| 58 | `2026-06-04T14:57:27Z` | `SD-4` | `1` | `stage_result` | {"jump": "SL-5", "ok": true, "reason": "waiver_continue_design_items_marked_non_blocking_for_downstream_validation"} | <none> |
| 59 | `2026-06-04T14:57:27Z` | `SL-5` | `1` | `stage_enter` | {"reason": "scenario_set_absent"} | <none> |
| 60 | `2026-06-04T14:59:10Z` | `SL-5` | `1` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 61 | `2026-06-04T14:59:11Z` | `SD-5A` | `1` | `stage_result` | {"jump": "SL-5 retry", "ok": false, "status": "StageStatus.ADVISORY"} | <none> |
| 62 | `2026-06-04T14:59:11Z` | `SL-5` | `1` | `stage_enter` | {"reason": "scenario_coverage_gap_retry"} | <none> |
| 63 | `2026-06-04T15:00:57Z` | `SL-5` | `1` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 64 | `2026-06-04T15:00:58Z` | `SD-5A` | `1` | `stage_result` | {"jump": "SL-5 retry", "ok": false, "status": "StageStatus.ADVISORY"} | <none> |
| 65 | `2026-06-04T15:00:58Z` | `SL-5` | `1` | `stage_enter` | {"reason": "scenario_coverage_gap_retry"} | <none> |
| 66 | `2026-06-04T15:02:48Z` | `SL-5` | `1` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 67 | `2026-06-04T15:02:49Z` | `SD-5A` | `1` | `stage_result` | {"jump": "SC-5F", "ok": true, "status": "StageStatus.OK"} | <none> |
| 68 | `2026-06-04T15:02:50Z` | `SC-5F` | `1` | `stage_result` | {"jump": "SD-6", "ok": true} | <none> |
| 69 | `2026-06-04T15:02:50Z` | `SD-6` | `1` | `stage_enter` | {"reason": "waiver_continue_scenario_set_ready"} | <none> |
| 70 | `2026-06-04T15:02:50Z` | `SD-6` | `1` | `stage_result` | {"jump": "SL-7", "ok": true, "status": "StageStatus.OK"} | <none> |
| 71 | `2026-06-04T15:02:50Z` | `SL-7` | `1` | `stage_enter` | {"reason": "waiver_continue_SD-6 ok"} | <none> |
| 72 | `2026-06-04T15:03:55Z` | `SL-7` | `1` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 73 | `2026-06-04T15:03:55Z` | `SL-7` | `1` | `stage_result` | {"jump": "SD-8 next iteration", "ok": false} | <none> |
| 74 | `2026-06-04T15:03:55Z` | `SL-7` | `1` | `grounding_update_hints_recorded` | {} | <none> |
| 75 | `2026-06-04T15:03:55Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 76 | `2026-06-04T15:03:55Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 77 | `2026-06-04T15:03:55Z` | `<control>` | `2` | `iteration_enter` | {} | current_hash=sha256:ae74dfc8a541f448b34f805ad6dbf46262a2b2b804509e2e7866abecbe67c8aa |
| 78 | `2026-06-04T15:03:55Z` | `<control>` | `2` | `iteration_validation_enter` | {} | dsl:len=9506,hash=sha256:ae74dfc8a541, current_hash=sha256:ae74dfc8a541f448b34f805ad6dbf46262a2b2b804509e2e7866abecbe67c8aa |
| 79 | `2026-06-04T15:03:55Z` | `SD-2` | `2` | `stage_enter` | {"reason": "full_validation_pass"} | <none> |
| 80 | `2026-06-04T15:03:55Z` | `SD-2` | `2` | `stage_result` | {"jump": "SD-3", "ok": true, "status": "StageStatus.OK"} | <none> |
- ……另有 `112` 条流程日志见 [`flow_log.json`](./flow_log.json) / run record。

### 5. Iteration / repair / review 摘要

| Iter | selected feedback | repair? | FixRequestBatch | SL-9 | local checks | SL-10 | 回到 SD-2? | verdict/备注 |
|---:|---|---|---|---|---|---|---|---|
| 0 | `SD-4` | yes | fixbatch-0-sha256-8829c3d5386 / n=12 | accept=8, reject=4, waiver=4 | ok=False, target=False, regression=False, drift=major, local_stage=SD-10, reason=design_target_unresolved; missing_required_grounding | decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none> | yes | candidate_accepted_for_next_full_pass |
| 1 | `SD-4` | yes | fixbatch-1-sha256-5a45bfc6f1a / n=12 | accept=0, reject=12, waiver=12 | <none> | decision=None, ok=True, target=True, regression=False, drift=minor, rework=<none> | no | waiver_continue_revealed_downstream_blocking_feedback |
| 2 | `SL-7` | yes | fixbatch-2-sha256-2baadc6ec74 / n=4 | accept=4, reject=0, waiver=0 | ok=False, target=False, regression=False, drift=major, local_stage=SD-10, reason=missing_required_grounding | decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none> | yes | candidate_accepted_for_next_full_pass |
| 3 | `SL-7` | yes | fixbatch-3-sha256-b2c527b44d2 / n=2 | accept=2, reject=0, waiver=0 | ok=False, target=False, regression=False, drift=major, local_stage=SD-10, reason=forced_transition_count_drift; missing_required_grounding | decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none> | yes | candidate_accepted_for_next_full_pass |
| 4 | `<none>` | no | <none> | <none> | <none> | <none> | no | full_pass_all_required_feedback_ok |

### 6. Scenario 明细与逐轮通过情况

#### 6.1 Scenario pass/fail by iteration

口径：`✅` = 该 scenario 在该轮 SD-6 simulation 通过；`❌` = 该轮失败；`⚪` = 该轮未执行或无该 scenario 结果。

| Scenario | Intent | Iter 2 | Iter 3 | Iter 4 | Iter 5 |
|---|---|---|---|---|---|
| `default_init_zero_load_res_charge` | default-init: after the first empty cycle, PL=0 with RES available and SoC below 0.95 selects zero-load battery charging...<truncated 28 chars> | ✅ | ✅ | ✅ | ✅ |
| `zero_load_full_soc_res_spare` | explicit-hot-start: PL=0 with RES available and SoC at the 0.95 boundary sends renewable production to spare power inste...<truncated 15 chars> | ✅ | ✅ | ✅ | ✅ |
| `res_covers_load_soc_below_full_charges` | explicit-hot-start: when RES covers positive load and SoC is just below 0.95, demand is served from RES and residual pow...<truncated 23 chars> | ✅ | ✅ | ✅ | ✅ |
| `res_covers_load_soc_full_spare` | explicit-hot-start: when RES covers positive load and SoC is exactly 0.95, residual renewable power is treated as spare. | ✅ | ✅ | ✅ | ✅ |
| `battery_priority_at_low_soc_boundary` | explicit-hot-start: when RES is below load, SoC is exactly the suitable-battery boundary 0.20, and the deficit fits batt...<truncated 55 chars> | ✅ | ✅ | ✅ | ✅ |
| `lng_low_soc_charge_margin` | explicit-hot-start: with low SoC below 0.20 and an LNG-coverable deficit, the LNG branch includes the Pgmax/5 charging m...<truncated 6 chars> | ✅ | ✅ | ✅ | ✅ |
| `lng_normal_covers_deficit_before_diesel` | explicit-hot-start: when battery cannot cover the deficit but LNG capacity can, LNG is cut in before any diesel units. | ✅ | ✅ | ✅ | ✅ |
| `lng_engine3_covers_after_lng_capacity` | explicit-hot-start: when the deficit exceeds LNG capacity but fits LNG plus engine3 capacity, LNG and engine3 are cut in...<truncated 26 chars> | ✅ | ✅ | ✅ | ✅ |
| `dg1_low_soc_charge_margin` | explicit-hot-start: when demand exceeds LNG plus engine3 and SoC is below 0.20, the DG1 low-SoC branch adds the Pd1max/1...<truncated 18 chars> | ✅ | ✅ | ✅ | ✅ |
| `dg1_normal_last_priority_before_dg2` | explicit-hot-start: with suitable SoC, demand beyond LNG plus engine3 but within DG1 capacity cuts in DG1 before DG2. | ✅ | ✅ | ✅ | ✅ |
| `dg2_low_soc_optional_charge_margin` | explicit-hot-start: when demand exceeds LNG, engine3, and DG1 capacity but fits DG2, DG2 is last-priority and low SoC ad...<truncated 40 chars> | ✅ | ✅ | ✅ | ✅ |
| `illegal_overload_activates_all_thermal_and_battery` | explicit-hot-start: for demand beyond RES and all thermal capacity, the illegal overload completion branch activates all...<truncated 66 chars> | ✅ | ✅ | ✅ | ✅ |
| `forced_reclassification_from_illegal_to_res_charge` | explicit-hot-start: a wildcard forced classification must re-evaluate from a concrete illegal-overload leaf to RES-cover...<truncated 96 chars> | ⚪ | ⚪ | ✅ | ✅ |
| `forced_reclassification_from_res_charge_to_illegal` | explicit-hot-start: a wildcard forced classification must also re-evaluate from a normal RES-charge leaf to illegal over...<truncated 108 chars> | ⚪ | ⚪ | ⚪ | ✅ |
| `forced_reclassification_from_dg2_to_zero_load_no_res_spare` | explicit-hot-start: a wildcard forced classification must re-evaluate from a DG2 leaf to the zero-load no-RES spare/idle...<truncated 113 chars> | ⚪ | ⚪ | ⚪ | ✅ |
| `forced_reclassification_from_illegal_to_res_spare` |  | ✅ | ✅ | ⚪ | ⚪ |
| `forced_reclassification_from_zero_load_to_illegal` |  | ✅ | ✅ | ⚪ | ⚪ |
| `forced_reclassification_to_zero_load_charge_from_dg2` |  | ✅ | ✅ | ⚪ | ⚪ |

#### 6.2 Scenario definitions

<details><summary>`default_init_zero_load_res_charge` — default-init: after the first empty cycle, PL=0 with RES available and SoC below 0.95 selects zero-load battery charging and cuts out thermal units.</summary>

| Field | Value |
|---|---|
| description | default-init: after the first empty cycle, PL=0 with RES available and SoC below 0.95 selects zero-load battery charging and cuts out thermal units. |
| initial_state | `<default-init>` |
| initial_vars | `{"PL": 0.0, "Pbat_discharge_Pmax": 5.0, "Pd1max": 10.0, "Pd2max": 10.0, "Pgmax": 10.0, "Ppv": 6.0, "Pw": 4.0, "SoC": 0.5, "eng3_Pmax": 5.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `initial_dispatch_to_zero_load_charge` | `0` | `[]` | `LNGShipEMS.ZeroLoad_RES_Charge` | `{"PDG1_req": 0.0, "PDG2_req": 0.0, "PENG3_req": 0.0, "PLNG_req": 0.0, "Pbat_charge": 10.0, "Pbat_discharge": 0.0, "Pgen_req": 0.0, "Pspare": 0.0, "cutin_DG1": 0, "cutin_DG2": 0, "cutin_ENG3": 0, "cutin_LNG": 0, "cutout_DG1": 1, "cutout_DG2": 1, "cutout_ENG3": 1, "cutout_LNG": 1, "load_cutout": 0}` |

</details>

<details><summary>`zero_load_full_soc_res_spare` — explicit-hot-start: PL=0 with RES available and SoC at the 0.95 boundary sends renewable production to spare power instead of charging.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: PL=0 with RES available and SoC at the 0.95 boundary sends renewable production to spare power instead of charging. |
| initial_state | `LNGShipEMS.ZeroLoad_RES_Charge` |
| initial_vars | `{"PL": 0.0, "Pbat_discharge_Pmax": 5.0, "Pd1max": 10.0, "Pd2max": 10.0, "Pgmax": 10.0, "Ppv": 6.0, "Pw": 4.0, "SoC": 0.95, "eng3_Pmax": 5.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `soc_boundary_routes_res_to_spare` | `0` | `[]` | `LNGShipEMS.ZeroLoad_RES_Spare` | `{"PDG1_req": 0.0, "PDG2_req": 0.0, "PENG3_req": 0.0, "PLNG_req": 0.0, "Pbat_charge": 0.0, "Pbat_discharge": 0.0, "Pgen_req": 0.0, "Pspare": 10.0, "cutin_DG1": 0, "cutin_DG2": 0, "cutin_ENG3": 0, "cutin_LNG": 0, "cutout_DG1": 1, "cutout_DG2": 1, "cutout_ENG3": 1, "cutout_LNG": 1, "load_cutout": 0}` |

</details>

<details><summary>`res_covers_load_soc_below_full_charges` — explicit-hot-start: when RES covers positive load and SoC is just below 0.95, demand is served from RES and residual power charges the battery.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: when RES covers positive load and SoC is just below 0.95, demand is served from RES and residual power charges the battery. |
| initial_state | `LNGShipEMS.ZeroLoad_RES_Spare` |
| initial_vars | `{"PL": 8.0, "Pbat_discharge_Pmax": 5.0, "Pd1max": 10.0, "Pd2max": 10.0, "Pgmax": 10.0, "Ppv": 6.0, "Pw": 4.0, "SoC": 0.94, "eng3_Pmax": 5.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `res_surplus_charges_battery` | `0` | `[]` | `LNGShipEMS.RES_Covers_Load_Charge` | `{"PDG1_req": 0.0, "PDG2_req": 0.0, "PENG3_req": 0.0, "PLNG_req": 0.0, "Pbat_charge": 2.0, "Pbat_discharge": 0.0, "Pgen_req": 0.0, "Pspare": 0.0, "cutin_DG1": 0, "cutin_DG2": 0, "cutin_ENG3": 0, "cutin_LNG": 0, "cutout_DG1": 1, "cutout_DG2": 1, "cutout_ENG3": 1, "cutout_LNG": 1, "load_cutout": 0}` |

</details>

<details><summary>`res_covers_load_soc_full_spare` — explicit-hot-start: when RES covers positive load and SoC is exactly 0.95, residual renewable power is treated as spare.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: when RES covers positive load and SoC is exactly 0.95, residual renewable power is treated as spare. |
| initial_state | `LNGShipEMS.RES_Covers_Load_Charge` |
| initial_vars | `{"PL": 8.0, "Pbat_discharge_Pmax": 5.0, "Pd1max": 10.0, "Pd2max": 10.0, "Pgmax": 10.0, "Ppv": 6.0, "Pw": 4.0, "SoC": 0.95, "eng3_Pmax": 5.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `res_surplus_goes_to_spare_at_full_soc` | `0` | `[]` | `LNGShipEMS.RES_Covers_Load_Spare` | `{"PDG1_req": 0.0, "PDG2_req": 0.0, "PENG3_req": 0.0, "PLNG_req": 0.0, "Pbat_charge": 0.0, "Pbat_discharge": 0.0, "Pgen_req": 0.0, "Pspare": 2.0, "cutin_DG1": 0, "cutin_DG2": 0, "cutin_ENG3": 0, "cutin_LNG": 0, "cutout_DG1": 1, "cutout_DG2": 1, "cutout_ENG3": 1, "cutout_LNG": 1, "load_cutout": 0}` |

</details>

<details><summary>`battery_priority_at_low_soc_boundary` — explicit-hot-start: when RES is below load, SoC is exactly the suitable-battery boundary 0.20, and the deficit fits battery capacity, battery discharge is selec...<truncated 15 chars></summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: when RES is below load, SoC is exactly the suitable-battery boundary 0.20, and the deficit fits battery capacity, battery discharge is selected before LNG. |
| initial_state | `LNGShipEMS.RES_Covers_Load_Spare` |
| initial_vars | `{"PL": 10.0, "Pbat_discharge_Pmax": 7.0, "Pd1max": 10.0, "Pd2max": 10.0, "Pgmax": 10.0, "Ppv": 2.0, "Pw": 1.0, "SoC": 0.2, "eng3_Pmax": 5.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `battery_covers_deficit_at_soc_boundary` | `0` | `[]` | `LNGShipEMS.Battery_Discharge_Priority` | `{"PDG1_req": 0.0, "PDG2_req": 0.0, "PENG3_req": 0.0, "PLNG_req": 0.0, "Pbat_charge": 0.0, "Pbat_discharge": 7.0, "Pgen_req": 0.0, "Pspare": 0.0, "cutin_DG1": 0, "cutin_DG2": 0, "cutin_ENG3": 0, "cutin_LNG": 0, "cutout_DG1": 1, "cutout_DG2": 1, "cutout_ENG3": 1, "cutout_LNG": 1, "load_cutout": 0}` |

</details>

<details><summary>`lng_low_soc_charge_margin` — explicit-hot-start: with low SoC below 0.20 and an LNG-coverable deficit, the LNG branch includes the Pgmax/5 charging margin.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: with low SoC below 0.20 and an LNG-coverable deficit, the LNG branch includes the Pgmax/5 charging margin. |
| initial_state | `LNGShipEMS.Battery_Discharge_Priority` |
| initial_vars | `{"PL": 18.0, "Pbat_discharge_Pmax": 5.0, "Pd1max": 10.0, "Pd2max": 10.0, "Pgmax": 10.0, "Ppv": 6.0, "Pw": 4.0, "SoC": 0.19, "eng3_Pmax": 5.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `lng_supplies_deficit_plus_charge_margin` | `0` | `[]` | `LNGShipEMS.LNG_Covers_Load_LowSoC_ChargeMargin` | `{"PDG1_req": 0.0, "PDG2_req": 0.0, "PENG3_req": 0.0, "PLNG_req": 10.0, "Pbat_charge": 2.0, "Pbat_discharge": 0.0, "Pgen_req": 10.0, "Pspare": 0.0, "cutin_DG1": 0, "cutin_DG2": 0, "cutin_ENG3": 0, "cutin_LNG": 1, "cutout_DG1": 1, "cutout_DG2": 1, "cutout_ENG3": 1, "cutout_LNG": 0, "load_cutout": 0}` |

</details>

<details><summary>`lng_normal_covers_deficit_before_diesel` — explicit-hot-start: when battery cannot cover the deficit but LNG capacity can, LNG is cut in before any diesel units.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: when battery cannot cover the deficit but LNG capacity can, LNG is cut in before any diesel units. |
| initial_state | `LNGShipEMS.LNG_Covers_Load_LowSoC_ChargeMargin` |
| initial_vars | `{"PL": 18.0, "Pbat_discharge_Pmax": 5.0, "Pd1max": 10.0, "Pd2max": 10.0, "Pgmax": 10.0, "Ppv": 6.0, "Pw": 4.0, "SoC": 0.5, "eng3_Pmax": 5.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `lng_only_covers_deficit` | `0` | `[]` | `LNGShipEMS.LNG_Covers_Load` | `{"PDG1_req": 0.0, "PDG2_req": 0.0, "PENG3_req": 0.0, "PLNG_req": 8.0, "Pbat_charge": 0.0, "Pbat_discharge": 0.0, "Pgen_req": 8.0, "Pspare": 0.0, "cutin_DG1": 0, "cutin_DG2": 0, "cutin_ENG3": 0, "cutin_LNG": 1, "cutout_DG1": 1, "cutout_DG2": 1, "cutout_ENG3": 1, "cutout_LNG": 0, "load_cutout": 0}` |

</details>

<details><summary>`lng_engine3_covers_after_lng_capacity` — explicit-hot-start: when the deficit exceeds LNG capacity but fits LNG plus engine3 capacity, LNG and engine3 are cut in while DG1/DG2 remain out.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: when the deficit exceeds LNG capacity but fits LNG plus engine3 capacity, LNG and engine3 are cut in while DG1/DG2 remain out. |
| initial_state | `LNGShipEMS.LNG_Covers_Load` |
| initial_vars | `{"PL": 25.0, "Pbat_discharge_Pmax": 5.0, "Pd1max": 10.0, "Pd2max": 10.0, "Pgmax": 10.0, "Ppv": 6.0, "Pw": 4.0, "SoC": 0.5, "eng3_Pmax": 5.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `engine3_added_after_lng` | `0` | `[]` | `LNGShipEMS.LNG_Engine3_Covers_Load` | `{"PDG1_req": 0.0, "PDG2_req": 0.0, "PENG3_req": 5.0, "PLNG_req": 10.0, "Pbat_charge": 0.0, "Pbat_discharge": 0.0, "Pgen_req": 15.0, "Pspare": 0.0, "cutin_DG1": 0, "cutin_DG2": 0, "cutin_ENG3": 1, "cutin_LNG": 1, "cutout_DG1": 1, "cutout_DG2": 1, "cutout_ENG3": 0, "cutout_LNG": 0, "load_cutout": 0}` |

</details>

<details><summary>`dg1_low_soc_charge_margin` — explicit-hot-start: when demand exceeds LNG plus engine3 and SoC is below 0.20, the DG1 low-SoC branch adds the Pd1max/10 charging margin.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: when demand exceeds LNG plus engine3 and SoC is below 0.20, the DG1 low-SoC branch adds the Pd1max/10 charging margin. |
| initial_state | `LNGShipEMS.LNG_Engine3_Covers_Load` |
| initial_vars | `{"PL": 27.0, "Pbat_discharge_Pmax": 5.0, "Pd1max": 10.0, "Pd2max": 10.0, "Pgmax": 10.0, "Ppv": 6.0, "Pw": 4.0, "SoC": 0.19, "eng3_Pmax": 5.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `dg1_margin_added_for_low_soc` | `0` | `[]` | `LNGShipEMS.DG1_Covers_Load_LowSoC_ChargeMargin` | `{"PDG1_req": 3.0, "PDG2_req": 0.0, "PENG3_req": 5.0, "PLNG_req": 10.0, "Pbat_charge": 1.0, "Pbat_discharge": 0.0, "Pgen_req": 18.0, "Pspare": 0.0, "cutin_DG1": 1, "cutin_DG2": 0, "cutin_ENG3": 1, "cutin_LNG": 1, "cutout_DG1": 0, "cutout_DG2": 1, "cutout_ENG3": 0, "cutout_LNG": 0, "load_cutout": 0}` |

</details>

<details><summary>`dg1_normal_last_priority_before_dg2` — explicit-hot-start: with suitable SoC, demand beyond LNG plus engine3 but within DG1 capacity cuts in DG1 before DG2.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: with suitable SoC, demand beyond LNG plus engine3 but within DG1 capacity cuts in DG1 before DG2. |
| initial_state | `LNGShipEMS.DG1_Covers_Load_LowSoC_ChargeMargin` |
| initial_vars | `{"PL": 30.0, "Pbat_discharge_Pmax": 5.0, "Pd1max": 10.0, "Pd2max": 10.0, "Pgmax": 10.0, "Ppv": 6.0, "Pw": 4.0, "SoC": 0.2, "eng3_Pmax": 5.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `dg1_covers_remaining_deficit` | `0` | `[]` | `LNGShipEMS.DG1_Covers_Load` | `{"PDG1_req": 5.0, "PDG2_req": 0.0, "PENG3_req": 5.0, "PLNG_req": 10.0, "Pbat_charge": 0.0, "Pbat_discharge": 0.0, "Pgen_req": 20.0, "Pspare": 0.0, "cutin_DG1": 1, "cutin_DG2": 0, "cutin_ENG3": 1, "cutin_LNG": 1, "cutout_DG1": 0, "cutout_DG2": 1, "cutout_ENG3": 0, "cutout_LNG": 0, "load_cutout": 0}` |

</details>

<details><summary>`dg2_low_soc_optional_charge_margin` — explicit-hot-start: when demand exceeds LNG, engine3, and DG1 capacity but fits DG2, DG2 is last-priority and low SoC adds the Pd1max/10 optional charge margin.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: when demand exceeds LNG, engine3, and DG1 capacity but fits DG2, DG2 is last-priority and low SoC adds the Pd1max/10 optional charge margin. |
| initial_state | `LNGShipEMS.DG1_Covers_Load` |
| initial_vars | `{"PL": 38.0, "Pbat_discharge_Pmax": 5.0, "Pd1max": 10.0, "Pd2max": 10.0, "Pgmax": 10.0, "Ppv": 6.0, "Pw": 4.0, "SoC": 0.19, "eng3_Pmax": 5.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `dg2_added_with_low_soc_margin` | `0` | `[]` | `LNGShipEMS.DG2_Covers_Load_WithOptionalChargeMargin` | `{"PDG1_req": 10.0, "PDG2_req": 4.0, "PENG3_req": 5.0, "PLNG_req": 10.0, "Pbat_charge": 1.0, "Pbat_discharge": 0.0, "Pgen_req": 29.0, "Pspare": 0.0, "cutin_DG1": 1, "cutin_DG2": 1, "cutin_ENG3": 1, "cutin_LNG": 1, "cutout_DG1": 0, "cutout_DG2": 0, "cutout_ENG3": 0, "cutout_LNG": 0, "load_cutout": 0}` |

</details>

<details><summary>`illegal_overload_activates_all_thermal_and_battery` — explicit-hot-start: for demand beyond RES and all thermal capacity, the illegal overload completion branch activates all thermal units and covers the remaining ...<truncated 26 chars></summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: for demand beyond RES and all thermal capacity, the illegal overload completion branch activates all thermal units and covers the remaining lack by battery discharge. |
| initial_state | `LNGShipEMS.DG2_Covers_Load_WithOptionalChargeMargin` |
| initial_vars | `{"PL": 38.0, "Pbat_discharge_Pmax": 5.0, "Pd1max": 10.0, "Pd2max": 10.0, "Pgmax": 10.0, "Ppv": 0.0, "Pw": 0.0, "SoC": 0.5, "eng3_Pmax": 5.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `thermal_exceeded_battery_covers_lack` | `0` | `[]` | `LNGShipEMS.IllegalOverloadCompletion` | `{"PDG1_req": 10.0, "PDG2_req": 10.0, "PENG3_req": 5.0, "PLNG_req": 10.0, "Pbat_charge": 0.0, "Pbat_discharge": 3.0, "Pgen_req": 35.0, "Pspare": 0.0, "cutin_DG1": 1, "cutin_DG2": 1, "cutin_ENG3": 1, "cutin_LNG": 1, "cutout_DG1": 0, "cutout_DG2": 0, "cutout_ENG3": 0, "cutout_LNG": 0, "load_cutout": 1}` |

</details>

<details><summary>`forced_reclassification_from_illegal_to_res_charge` — explicit-hot-start: a wildcard forced classification must re-evaluate from a concrete illegal-overload leaf to RES-covers-load charge when operating inputs chan...<truncated 56 chars></summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: a wildcard forced classification must re-evaluate from a concrete illegal-overload leaf to RES-covers-load charge when operating inputs change; this fails if the forced transition line is missing. |
| initial_state | `LNGShipEMS.IllegalOverloadCompletion` |
| initial_vars | `{"PDG1_req": 10.0, "PDG2_req": 10.0, "PENG3_req": 5.0, "PL": 8.0, "PLNG_req": 10.0, "Pbat_charge": 0.0, "Pbat_discharge": 3.0, "Pbat_discharge_Pmax": 5.0, "Pd1max": 10.0, "Pd2max": 10.0, "Pgen_req": 35.0, "Pgmax": 10.0, "Ppv": 6.0, "Pspare": 0.0, "Pw": 4.0, "SoC": 0.94, "cutin_DG1": 1, "cutin_DG2": 1, "cutin_ENG3": 1, "cutin_LNG": 1, "cutout_DG1": 0, "cutout_DG2": 0, "cutout_ENG3": 0, "cutout_LNG": 0, "eng3_Pmax": 5.0, "load_cutout": 1}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `forced_guard_reclassifies_to_res_charge` | `0` | `[]` | `LNGShipEMS.RES_Covers_Load_Charge` | `{"PDG1_req": 0.0, "PDG2_req": 0.0, "PENG3_req": 0.0, "PLNG_req": 0.0, "Pbat_charge": 2.0, "Pbat_discharge": 0.0, "Pgen_req": 0.0, "Pspare": 0.0, "cutin_DG1": 0, "cutin_DG2": 0, "cutin_ENG3": 0, "cutin_LNG": 0, "cutout_DG1": 1, "cutout_DG2": 1, "cutout_ENG3": 1, "cutout_LNG": 1, "load_cutout": 0}` |

</details>

<details><summary>`forced_reclassification_from_res_charge_to_illegal` — explicit-hot-start: a wildcard forced classification must also re-evaluate from a normal RES-charge leaf to illegal overload when demand becomes extreme; this f...<truncated 68 chars></summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: a wildcard forced classification must also re-evaluate from a normal RES-charge leaf to illegal overload when demand becomes extreme; this fails if the global forced classifier to illegal overload is missing. |
| initial_state | `LNGShipEMS.RES_Covers_Load_Charge` |
| initial_vars | `{"PDG1_req": 0.0, "PDG2_req": 0.0, "PENG3_req": 0.0, "PL": 42.0, "PLNG_req": 0.0, "Pbat_charge": 2.0, "Pbat_discharge": 0.0, "Pbat_discharge_Pmax": 5.0, "Pd1max": 10.0, "Pd2max": 10.0, "Pgen_req": 0.0, "Pgmax": 10.0, "Ppv": 0.0, "Pspare": 0.0, "Pw": 0.0, "SoC": 0.5, "cutin_DG1": 0, "cutin_DG2": 0, "cutin_ENG3": 0, "cutin_LNG": 0, "cutout_DG1": 1, "cutout_DG2": 1, "cutout_ENG3": 1, "cutout_LNG": 1, "eng3_Pmax": 5.0, "load_cutout": 0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `forced_guard_reclassifies_to_illegal_overload` | `0` | `[]` | `LNGShipEMS.IllegalOverloadCompletion` | `{"PDG1_req": 10.0, "PDG2_req": 10.0, "PENG3_req": 5.0, "PLNG_req": 10.0, "Pbat_charge": 0.0, "Pbat_discharge": 7.0, "Pgen_req": 35.0, "Pspare": 0.0, "cutin_DG1": 1, "cutin_DG2": 1, "cutin_ENG3": 1, "cutin_LNG": 1, "cutout_DG1": 0, "cutout_DG2": 0, "cutout_ENG3": 0, "cutout_LNG": 0, "load_cutout": 1}` |

</details>

<details><summary>`forced_reclassification_from_dg2_to_zero_load_no_res_spare` — explicit-hot-start: a wildcard forced classification must re-evaluate from a DG2 leaf to the zero-load no-RES spare/idle classification; this targets missing fo...<truncated 73 chars></summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: a wildcard forced classification must re-evaluate from a DG2 leaf to the zero-load no-RES spare/idle classification; this targets missing forced transition lines that would leave stale DG2 dispatch outputs active. |
| initial_state | `LNGShipEMS.DG2_Covers_Load_WithOptionalChargeMargin` |
| initial_vars | `{"PDG1_req": 10.0, "PDG2_req": 4.0, "PENG3_req": 5.0, "PL": 0.0, "PLNG_req": 10.0, "Pbat_charge": 1.0, "Pbat_discharge": 0.0, "Pbat_discharge_Pmax": 5.0, "Pd1max": 10.0, "Pd2max": 10.0, "Pgen_req": 29.0, "Pgmax": 10.0, "Ppv": 0.0, "Pspare": 0.0, "Pw": 0.0, "SoC": 0.5, "cutin_DG1": 1, "cutin_DG2": 1, "cutin_ENG3": 1, "cutin_LNG": 1, "cutout_DG1": 0, "cutout_DG2": 0, "cutout_ENG3": 0, "cutout_LNG": 0, "eng3_Pmax": 5.0, "load_cutout": 0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `forced_guard_reclassifies_to_zero_load_no_res_spare` | `0` | `[]` | `LNGShipEMS.ZeroLoad_RES_Spare` | `{"PDG1_req": 0.0, "PDG2_req": 0.0, "PENG3_req": 0.0, "PLNG_req": 0.0, "Pbat_charge": 0.0, "Pbat_discharge": 0.0, "Pgen_req": 0.0, "Pspare": 0.0, "cutin_DG1": 0, "cutin_DG2": 0, "cutin_ENG3": 0, "cutin_LNG": 0, "cutout_DG1": 1, "cutout_DG2": 1, "cutout_ENG3": 1, "cutout_LNG": 1, "load_cutout": 0}` |

</details>


### 7. Repair / blocking feedback 明细

口径：本节记录 agent-loop 真实进入 repair block 后的证据链：FixRequestBatch、SL-9 per-request accept/reject、candidate diff、local-check evidence、SL-10(NL+FixLog) 审阅，以及完整 FixLog ledger 摘录。

| Repair | iteration | accepted | source | blocking diagnostics | SL-9 decisions | SL-10 / local checks | candidate hash |
|---:|---:|---:|---|---|---|---|---|
| 1 | `0` | ✅ | `SD-4` | W_UNWRITTEN_READ_VAR:var_name=SoC_full_threshold, W_UNWRITTEN_READ_VAR:var_name=SoC_low_threshold, W_UNWRITTEN_READ_VAR:var_name=Pd2max, W_UNWRITTEN_READ_VAR:var_name=Pbat_discharge_Pmax, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoad_RES_Charge:to_path=LNGShipEMS.IllegalOverloadCompletion, ... +136 | accept=8, reject=4, waiver=4 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none>; local ok=False, target=False, regression=False, drift=major, local_stage=SD-10, reason=design_target_unresolved; missing_required_grounding | `sha256:ae74dfc8a541f448b34f805ad6dbf46262a2b2b804509e2e7866abecbe67c8aa` |
| 2 | `1` | ❌ | `SD-4` | W_UNWRITTEN_READ_VAR:var_name=Pd2max, W_UNWRITTEN_READ_VAR:var_name=Pbat_discharge_Pmax, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoad_RES_Charge:to_path=LNGShipEMS.IllegalOverloadCompletion, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoad_RES_Charge:to_path=LNGShipEMS.Battery_Discharge_Priority, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoad_RES_Charge:to_path=LNGShipEMS.LNG_Covers_Load, ... +50 | accept=0, reject=12, waiver=12 | <none> | `sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 3 | `2` | ❌ | `SL-7` | 0, 1, 2, 3 | accept=4, reject=0, waiver=0 | SL-10 decision=rework, ok=False, target=True, regression=False, drift=minor, rework=SL-10 pass was downgraded because local deterministic evidence reported major drift and SL-10 evidence did not explicitly address the local rejection reason/kind with a structu...<truncated 678 chars> | `sha256:4c5a6347ae4632bd2b168c1d08eef85bdcfb190e6335c8e955fb8d53d02b8d19` |
| 4 | `2` | ✅ | `SL-7` | 0, 1, 2, 3 | accept=4, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none>; local ok=False, target=False, regression=False, drift=major, local_stage=SD-10, reason=missing_required_grounding | `sha256:27ff012eeca8958395886399d5f506d668adb07be506c45860ce7acb776355e5` |
| 5 | `3` | ✅ | `SL-7` | 0, 1 | accept=2, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none>; local ok=False, target=False, regression=False, drift=major, local_stage=SD-10, reason=forced_transition_count_drift; missing_required_grounding | `sha256:4b52356070e7a51d779df874526281152b5fb3e1dac5b2f71a14dc2af9ccf364` |

<details><summary>Repair 1 / iteration `0` / source `SD-4` / accepted=✅</summary>

#### 为什么进入修复

- selected feedback source：`SD-4`；blocking=`True`；pre_scenario=`True`。
- problem_summary：Variable 'SoC_full_threshold' is read but never written by any action or transition effect.; Variable 'SoC_low_threshold' is read but never written by any action or transition effect.; Variable 'Pd2max' is read but never written by any action or transition effect.
- diagnostic ids：`W_UNWRITTEN_READ_VAR:var_name=SoC_full_threshold, W_UNWRITTEN_READ_VAR:var_name=SoC_low_threshold, W_UNWRITTEN_READ_VAR:var_name=Pd2max, W_UNWRITTEN_READ_VAR:var_name=Pbat_discharge_Pmax, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoad_RES_Charge:to_path=LNGShipEMS.IllegalOverloadCompletion, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoad_RES_Charge:to_path=LNGShipEMS.ZeroLoad_RES_Charge, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoad_RES_Charge:to_path=LNGShipEMS.ZeroLoad_RES_Spare, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoad_RES_Charge:to_path=LNGShipEMS.RES_Covers_Load_Charge, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoad_RES_Charge:to_path=LNGShipEMS.RES_Covers_Load_Spare, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoad_RES_Charge:to_path=LNGShipEMS.Battery_Discharge_Priority, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoad_RES_Charge:to_path=LNGShipEMS.LNG_Covers_Load_LowSoC_ChargeMargin, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoad_RES_Charge:to_path=LNGShipEMS.LNG_Covers_Load, ... +129`。
- before_dsl_hash：`sha256:3ea5c49f5dbb17a8d2f42b1a1b58c7e3f1687ae88f318d7b6099537ae0761375`；candidate_dsl_hash：`sha256:ae74dfc8a541f448b34f805ad6dbf46262a2b2b804509e2e7866abecbe67c8aa`。

#### 错误证据 / diagnostics

- 1. `W_UNWRITTEN_READ_VAR` `W_UNWRITTEN_READ_VAR:var_name=SoC_full_threshold` policy=`budgeted_repair`：Variable 'SoC_full_threshold' is read but never written by any action or transition effect.；refs=`{"init_value": "0.95", "read_states": ["LNGShipEMS.Battery_Discharge_Priority", "LNGShipEMS.DG1_Covers_Load", "LNGShipEMS.DG1_Covers_Load_LowSoC_ChargeMargin", "LNGShipEMS.DG2_Covers_Load_WithOptionalChargeMargin", "LNGShipEMS.IllegalOverloadCompletion", "LNGShipEMS.LNG_Covers_Load", "LNGShipEMS.LNG...<truncated 247 chars>`
- 2. `W_UNWRITTEN_READ_VAR` `W_UNWRITTEN_READ_VAR:var_name=SoC_low_threshold` policy=`budgeted_repair`：Variable 'SoC_low_threshold' is read but never written by any action or transition effect.；refs=`{"init_value": "0.2", "read_states": ["LNGShipEMS.Battery_Discharge_Priority", "LNGShipEMS.DG1_Covers_Load", "LNGShipEMS.DG1_Covers_Load_LowSoC_ChargeMargin", "LNGShipEMS.DG2_Covers_Load_WithOptionalChargeMargin", "LNGShipEMS.IllegalOverloadCompletion", "LNGShipEMS.LNG_Covers_Load", "LNGShipEMS.LNG_...<truncated 245 chars>`
- 3. `W_UNWRITTEN_READ_VAR` `W_UNWRITTEN_READ_VAR:var_name=Pd2max` policy=`budgeted_repair`：Variable 'Pd2max' is read but never written by any action or transition effect.；refs=`{"init_value": "0.0", "read_states": ["LNGShipEMS.Battery_Discharge_Priority", "LNGShipEMS.DG1_Covers_Load", "LNGShipEMS.DG1_Covers_Load_LowSoC_ChargeMargin", "LNGShipEMS.DG2_Covers_Load_WithOptionalChargeMargin", "LNGShipEMS.IllegalOverloadCompletion", "LNGShipEMS.LNG_Covers_Load", "LNGShipEMS.LNG_...<truncated 234 chars>`
- 4. `W_UNWRITTEN_READ_VAR` `W_UNWRITTEN_READ_VAR:var_name=Pbat_discharge_Pmax` policy=`budgeted_repair`：Variable 'Pbat_discharge_Pmax' is read but never written by any action or transition effect.；refs=`{"init_value": "0.0", "read_states": ["LNGShipEMS.Battery_Discharge_Priority", "LNGShipEMS.DG1_Covers_Load", "LNGShipEMS.DG1_Covers_Load_LowSoC_ChargeMargin", "LNGShipEMS.DG2_Covers_Load_WithOptionalChargeMargin", "LNGShipEMS.IllegalOverloadCompletion", "LNGShipEMS.LNG_Covers_Load", "LNGShipEMS.LNG_...<truncated 247 chars>`
- 5. `W_GUARD_VARS_NEVER_CHANGE` `W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoad_RES_Charge:to_path=LNGShipEMS.IllegalOverloadCompletion` policy=`budgeted_repair`：Transition guard reads only variables that are never changed by actions or effects.；refs=`{"from_path": "LNGShipEMS.ZeroLoad_RES_Charge", "guard_vars": ["PL", "Pbat_discharge_Pmax", "Pd1max", "Pd2max", "Pgmax", "Ppv", "Pw", "eng3_Pmax"], "to_path": "LNGShipEMS.IllegalOverloadCompletion"}`
- 6. `W_GUARD_VARS_NEVER_CHANGE` `W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoad_RES_Charge:to_path=LNGShipEMS.ZeroLoad_RES_Charge` policy=`budgeted_repair`：Transition guard reads only variables that are never changed by actions or effects.；refs=`{"from_path": "LNGShipEMS.ZeroLoad_RES_Charge", "guard_vars": ["PL", "Ppv", "Pw", "SoC", "SoC_full_threshold"], "to_path": "LNGShipEMS.ZeroLoad_RES_Charge"}`
- 7. `W_GUARD_VARS_NEVER_CHANGE` `W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoad_RES_Charge:to_path=LNGShipEMS.ZeroLoad_RES_Spare` policy=`budgeted_repair`：Transition guard reads only variables that are never changed by actions or effects.；refs=`{"from_path": "LNGShipEMS.ZeroLoad_RES_Charge", "guard_vars": ["PL", "Ppv", "Pw", "SoC", "SoC_full_threshold"], "to_path": "LNGShipEMS.ZeroLoad_RES_Spare"}`
- 8. `W_GUARD_VARS_NEVER_CHANGE` `W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoad_RES_Charge:to_path=LNGShipEMS.RES_Covers_Load_Charge` policy=`budgeted_repair`：Transition guard reads only variables that are never changed by actions or effects.；refs=`{"from_path": "LNGShipEMS.ZeroLoad_RES_Charge", "guard_vars": ["PL", "Ppv", "Pw", "SoC", "SoC_full_threshold"], "to_path": "LNGShipEMS.RES_Covers_Load_Charge"}`
- ……另有 `128` 条 evidence 见 run record。

#### 变量角色与上下文提示

- policy：Advisory only. Do not invent writes for external_input_candidate variables unless NL explicitly gives update semantics; add meaningful NL-grounded writes only for internal state variables.
- source：SD-4 diagnostic refs and generic NL external-input rationale

| Variable | role_hint | nl_token_present | diagnostics |
|---|---|---:|---|
| `PDG1_req` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `PDG2_req` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `PENG3_req` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `PL` | `external_input_candidate` | ✅ | `W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +140` |
| `PLNG_req` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `Pbat_charge` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `Pbat_discharge` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `Pbat_discharge_Pmax` | `unknown` | ❌ | `W_UNWRITTEN_READ_VAR, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +32` |
| `Pd1max` | `external_input_candidate` | ✅ | `W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +44` |
| `Pd2max` | `unknown` | ❌ | `W_UNWRITTEN_READ_VAR, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +20` |
| `Pgen_req` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `Pgmax` | `external_input_candidate` | ✅ | `W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +80` |
| `Ppv` | `external_input_candidate` | ✅ | `W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +140` |
| `Pspare` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `Pw` | `external_input_candidate` | ✅ | `W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +140` |
| `SoC` | `external_input_candidate` | ✅ | `W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +92` |
| `SoC_full_threshold` | `unknown` | ❌ | `W_UNWRITTEN_READ_VAR, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +44` |
| `SoC_low_threshold` | `unknown` | ❌ | `W_UNWRITTEN_READ_VAR, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +44` |
| `cutin_DG1` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `cutin_DG2` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `cutin_ENG3` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `cutin_LNG` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `cutout_DG1` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `cutout_DG2` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `cutout_ENG3` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `cutout_LNG` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `eng3_Pmax` | `external_input_candidate` | ✅ | `W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +56` |
| `load_cutout` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |

#### SD-8 FixRequestBatch / 修改请求

- batch_id：`fixbatch-0-sha256-8829c3d5386`；source_stage=`SD-4`；legacy_plan_kind=`FixPlan`；requests=`12`。

| request_id | severity | hard | waiver | problem | evidence |
|---|---|---:|---:|---|---|
| `fixreq-0-sd4-0-8645e8d919` | `blocking_warning` | ❌ | ✅ | Variable 'SoC_full_threshold' is read but never written by any action or transition effect.; Variable 'SoC_low_threshold' is read but never written by any action or transition effect.; Variable 'Pd2max' is read but never...<truncated 44 chars> | `W_UNWRITTEN_READ_VAR` |
| `fixreq-0-sd4-1-c164939c86` | `blocking_warning` | ❌ | ✅ | Variable 'SoC_full_threshold' is read but never written by any action or transition effect.; Variable 'SoC_low_threshold' is read but never written by any action or transition effect.; Variable 'Pd2max' is read but never...<truncated 44 chars> | `W_UNWRITTEN_READ_VAR` |
| `fixreq-0-sd4-2-5f336aa55b` | `blocking_warning` | ❌ | ✅ | Variable 'SoC_full_threshold' is read but never written by any action or transition effect.; Variable 'SoC_low_threshold' is read but never written by any action or transition effect.; Variable 'Pd2max' is read but never...<truncated 44 chars> | `W_UNWRITTEN_READ_VAR` |
| `fixreq-0-sd4-3-ae21ee3029` | `blocking_warning` | ❌ | ✅ | Variable 'SoC_full_threshold' is read but never written by any action or transition effect.; Variable 'SoC_low_threshold' is read but never written by any action or transition effect.; Variable 'Pd2max' is read but never...<truncated 44 chars> | `W_UNWRITTEN_READ_VAR` |
| `fixreq-0-sd4-4-c43f6045b8` | `blocking_warning` | ❌ | ✅ | Variable 'SoC_full_threshold' is read but never written by any action or transition effect.; Variable 'SoC_low_threshold' is read but never written by any action or transition effect.; Variable 'Pd2max' is read but never...<truncated 44 chars> | `W_GUARD_VARS_NEVER_CHANGE` |
| `fixreq-0-sd4-5-0e2d9bb0a4` | `blocking_warning` | ❌ | ✅ | Variable 'SoC_full_threshold' is read but never written by any action or transition effect.; Variable 'SoC_low_threshold' is read but never written by any action or transition effect.; Variable 'Pd2max' is read but never...<truncated 44 chars> | `W_GUARD_VARS_NEVER_CHANGE` |
| `fixreq-0-sd4-6-eaac899d48` | `blocking_warning` | ❌ | ✅ | Variable 'SoC_full_threshold' is read but never written by any action or transition effect.; Variable 'SoC_low_threshold' is read but never written by any action or transition effect.; Variable 'Pd2max' is read but never...<truncated 44 chars> | `W_GUARD_VARS_NEVER_CHANGE` |
| `fixreq-0-sd4-7-5f5369f3e1` | `blocking_warning` | ❌ | ✅ | Variable 'SoC_full_threshold' is read but never written by any action or transition effect.; Variable 'SoC_low_threshold' is read but never written by any action or transition effect.; Variable 'Pd2max' is read but never...<truncated 44 chars> | `W_GUARD_VARS_NEVER_CHANGE` |
| `fixreq-0-sd4-8-3a6bedb74b` | `blocking_warning` | ❌ | ✅ | Variable 'SoC_full_threshold' is read but never written by any action or transition effect.; Variable 'SoC_low_threshold' is read but never written by any action or transition effect.; Variable 'Pd2max' is read but never...<truncated 44 chars> | `W_GUARD_VARS_NEVER_CHANGE` |
| `fixreq-0-sd4-9-1857623bee` | `blocking_warning` | ❌ | ✅ | Variable 'SoC_full_threshold' is read but never written by any action or transition effect.; Variable 'SoC_low_threshold' is read but never written by any action or transition effect.; Variable 'Pd2max' is read but never...<truncated 44 chars> | `W_GUARD_VARS_NEVER_CHANGE` |
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
- required_preserve_element_ids：`state:LNGShipEMS, variable:PL, variable:Ppv, variable:Pw, variable:SoC, variable:eng3_Pmax, variable:Pgmax, variable:Pd1max, variable:Pgen_req, variable:Pbat_discharge, variable:Pbat_charge, variable:Pspare, ... +25`。

#### SL-9 per-request 决策

- accepted_request_ids：`<derived-from-table>`；candidate_len=`9506`。

| request_id | decision | waiver | rework_locked | rationale / intent |
|---|---|---:|---:|---|
| `fixreq-0-sd4-0-8645e8d919` | `accept` | ❌ | ❌ | SoC_full_threshold is an NL-grounded constant value of 0.95, not an evolving plant/internal state. The smallest safe edit is to inline the literal 0.95 in guards/actions and remove the unused threshold variable rather than inventing meaningless writes.；intent=Replace SoC_full_threshold reads with literal 0.95, Remove def float SoC_full_threshold |
| `fixreq-0-sd4-1-c164939c86` | `accept` | ❌ | ❌ | SoC_low_threshold is a fixed modeling threshold initialized to 0.20 with no NL update semantics. The smallest safe edit is to inline 0.20 and remove the unused variable rather than inventing an ungrounded write.；intent=Replace SoC_low_threshold reads with literal 0.20, Remove def float SoC_low_threshold |
| `fixreq-0-sd4-2-5f336aa55b` | `reject` | ✅ | ❌ | Pd2max is a diesel-generator capacity bound/external input used to classify dispatch feasibility. The NL gives no runtime update law for it, and adding writes would invent ungrounded plant dynamics. |
| `fixreq-0-sd4-3-ae21ee3029` | `reject` | ✅ | ❌ | Pbat_discharge_Pmax is a battery capacity bound/external input used in dispatch guards. The NL provides no action that updates it, so adding writes would be meaningless and forbidden by the request. |
| `fixreq-0-sd4-4-c43f6045b8` | `reject` | ✅ | ❌ | The IllegalOverloadCompletion guard intentionally reads external demand/resource/capacity inputs. These variables are expected to vary outside the FSM, and no NL-grounded internal update exists. |
| `fixreq-0-sd4-5-0e2d9bb0a4` | `accept` | ❌ | ❌ | The self-classification guard included a fixed SoC full threshold variable. Inlining 0.95 removes the unwritten threshold read while preserving the NL-required zero-load RES charging branch.；intent=Use literal 0.95 in zero-load charging guard |
| `fixreq-0-sd4-6-eaac899d48` | `accept` | ❌ | ❌ | The zero-load spare guard included a fixed SoC full threshold variable. Inlining 0.95 is the minimal safe repair and preserves the NL-required spare-power behavior at full SoC.；intent=Use literal 0.95 in zero-load spare guard |
| `fixreq-0-sd4-7-5f5369f3e1` | `accept` | ❌ | ❌ | The RES-covers-load charging guard included a fixed SoC full threshold variable. Replacing it with 0.95 preserves the required RES charging condition.；intent=Use literal 0.95 in RES covers load charge guard |
| `fixreq-0-sd4-8-3a6bedb74b` | `accept` | ❌ | ❌ | The RES-covers-load spare guard included a fixed SoC full threshold variable. Replacing it with 0.95 preserves the required spare-power condition.；intent=Use literal 0.95 in RES covers load spare guard |
| `fixreq-0-sd4-9-1857623bee` | `accept` | ❌ | ❌ | The battery-priority guard included a fixed low-SoC threshold variable. Replacing it with 0.20 preserves the suitable-SoC battery dispatch branch without adding ungrounded SoC dynamics.；intent=Use literal 0.20 in battery discharge priority guard |
| `fixreq-0-sd4-10-7136bcb8d5` | `accept` | ❌ | ❌ | The LNG low-SoC charging-margin guard included a fixed low-SoC threshold variable. Replacing it with 0.20 preserves the NL-required Pgmax/5 charging margin branch.；intent=Use literal 0.20 in LNG low-SoC margin guard |
| `fixreq-0-sd4-11-2d12815059` | `reject` | ✅ | ❌ | The remaining guard variables for the LNG_Covers_Load transition are external demand, renewable, battery-capacity, and LNG-capacity inputs. There is no safe NL-grounded internal write to add. |
- repair_rationale：Read the FixLog and repair_memory: there are no prior rejected candidates or actionable rework objections to address.；Made the smallest design repair by inlining fixed SoC thresholds instead of adding meaningless self-assignments or invented dynamics.；Preserved all required states, required input/output variables, dispatch actions, cut-in/cut-out commands, zero-load branches, RES charge/spare branches, battery-priority branch, LNG/DG priority branches, low-SoC charge margins, and illegal...<truncated 30 chars>；Rejected/waived remaining never-written guard-variable requests because PL, Ppv, Pw, SoC, Pgmax, eng3_Pmax, Pd1max, Pd2max, and Pbat_discharge_Pmax are NL-described external inputs/capacity bounds for condition classification; the NL provid...<truncated 32 chars>
- diff_summary：`{"summary": "Removed fixed threshold declarations SoC_full_threshold and SoC_low_threshold; replaced their reads with literals 0.95 and 0.20 throughout guards and the DG2 optional charge-margin action. No state or grounded dispatch branch was deleted."}`。

#### SL-9 candidate / 最终修改执行方案

```pyfcstm
def float PL = 0.0;
def float Ppv = 0.0;
def float Pw = 0.0;
def float SoC = 0.50;
def float Pgmax = 0.0;
def float eng3_Pmax = 0.0;
def float Pd1max = 0.0;
def float Pd2max = 0.0;
def float Pbat_discharge_Pmax = 0.0;
def float Pgen_req = 0.0;
def float PLNG_req = 0.0;
def float PENG3_req = 0.0;
def float PDG1_req = 0.0;
def float PDG2_req = 0.0;
def float Pbat_discharge = 0.0;
def float Pbat_charge = 0.0;
def float Pspare = 0.0;
def int cutin_LNG = 0;
def int cutout_LNG = 0;
def int cutin_ENG3 = 0;
def int cutout_ENG3 = 0;
def int cutin_DG1 = 0;
def int cutout_DG1 = 0;
def int cutin_DG2 = 0;
def int cutout_DG2 = 0;
def int load_cutout = 0;

state LNGShipEMS {
    ! * -> IllegalOverloadCompletion : if [PL - Ppv - Pw > Pgmax + eng3_Pmax + Pd1max + Pd2max + Pbat_discharge_Pmax];
    ! * -> ZeroLoad_RES_Charge : if [PL == 0 && Ppv + Pw > 0 && SoC < 0.95];
    ! * -> ZeroLoad_RES_Spare : if [PL == 0 && Ppv + Pw > 0 && SoC >= 0.95];
    ! * -> RES_Covers_Load_Charge : if [PL > 0 && Ppv + Pw >= PL && SoC < 0.95];
    ! * -> RES_Covers_Load_Spare : if [PL > 0 && Ppv + Pw >= PL && SoC >= 0.95];
    ! * -> Battery_Discharge_Priority : if [PL > 0 && Ppv + Pw < PL && SoC >= 0.20 && PL - Ppv - Pw <= Pbat_discharge_Pmax];
    ! * -> LNG_Covers_Load_LowSoC_ChargeMargin : if [PL > 0 && Ppv + Pw < PL && SoC < 0.20 && PL - Ppv - Pw + Pgmax / 5 <= Pgmax];
    ! * -> LNG_Covers_Load : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > Pbat_discharge_Pmax && PL - Ppv - Pw <= Pgmax];
    ! * -> LNG_Engine3_Covers_Load : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > Pgmax && PL - Ppv - Pw <= Pgmax + eng3_Pmax];
    ! * -> DG1_Covers_Load_LowSoC_ChargeMargin : if [PL > 0 && Ppv + Pw < PL && SoC < 0.20 && PL - Ppv - Pw > Pgmax + eng3_Pmax && PL - Ppv - Pw + Pd1max / 10 <= Pgmax + eng3_Pmax + Pd1max];
    ! * -> DG1_Covers_Load : if [PL > 0 && Ppv + Pw < PL && SoC >= 0.20 && PL - Ppv - Pw > Pgmax + eng3_Pmax && PL - Ppv - Pw <= Pgmax + eng3_Pmax + Pd1max];
    ! * -> DG2_Covers_Load_WithOptionalChargeMargin : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > Pgmax + eng3_Pmax + Pd1max && PL - Ppv - Pw <= Pgmax + eng3_Pmax + Pd1max + Pd2max];

    [*] -> ZeroLoad_RES_Charge;

    state ZeroLoad_RES_Charge {
        enter {
            Pgen_req = 0;
            PLNG_req = 0;
            PENG3_req = 0;
            PDG1_req = 0;
            PDG2_req = 0;
            Pbat_discharge = 0;
            Pbat_charge = Ppv + Pw;
            Pspare = 0;
            cutin_LNG = 0;
            cutout_LNG = 1;
            cutin_ENG3 = 0;
            cutout_ENG3 = 1;
            cutin_DG1 = 0;
            cutout_DG1 = 1;
            cutin_DG2 = 0;
            cutout_DG2 = 1;
            load_cutout = 0;
        }
    }

    state ZeroLoad_RES_Spare {
        enter {
            Pgen_req = 0;
            PLNG_req = 0;
            PENG3_req = 0;
            PDG1_req = 0;
            PDG2_req = 0;
            Pbat_discharge = 0;
            Pbat_charge = 0;
            Pspare = Ppv + Pw;
            cutin_LNG = 0;
            cutout_LNG = 1;
            cutin_ENG3 = 0;
            cutout_ENG3 = 1;
            cutin_DG1 = 0;
            cutout_DG1 = 1;
            cutin_DG2 = 0;
            cutout_DG2 = 1;
            load_cutout = 0;
        }
    }

    state RES_Covers_Load_Charge {
        enter {
            Pgen_req = 0;
            PLNG_req = 0;
            PENG3_req = 0;
            PDG1_req = 0;
            PDG2_req = 0;
            Pbat_discharge = 0;
            Pbat_charge = Ppv + Pw - PL;
            Pspare = 0;
            cutin_LNG = 0;
            cutout_LNG = 1;
            cutin_ENG3 = 0;
            cutout_ENG3 = 1;
            cutin_DG1 = 0;
            cutout_DG1 = 1;
            cutin_DG2 = 0;
            cutout_DG2 = 1;
            load_cutout = 0;
        }
    }

    state RES_Covers_Load_Spare {
        enter {
            Pgen_req = 0;
            PLNG_req = 0;
            PENG3_req = 0;
            PDG1_req = 0;
            PDG2_req = 0;
            Pbat_discharge = 0;
            Pbat_charge = 0;
            Pspare = Ppv + Pw - PL;
            cutin_LNG = 0;
            cutout_LNG = 1;
            cutin_ENG3 = 0;
            cutout_ENG3 = 1;
            cutin_DG1 = 0;
            cutout_DG1 = 1;
            cutin_DG2 = 0;
            cutout_DG2 = 1;
            load_cutout = 0;
        }
    }

    state Battery_Discharge_Priority {
        enter {
            Pgen_req = 0;
            PLNG_req = 0;
            PENG3_req = 0;
            PDG1_req = 0;
            PDG2_req = 0;
            Pbat_discharge = PL - Ppv - Pw;
            Pbat_charge = 0;
            Pspare = 0;
            cutin_LNG = 0;
            cutout_LNG = 1;
            cutin_ENG3 = 0;
            cutout_ENG3 = 1;
            cutin_DG1 = 0;
            cutout_DG1 = 1;
            cutin_DG2 = 0;
            cutout_DG2 = 1;
            load_cutout = 0;
        }
    }

    state LNG_Covers_Load {
        enter {
            Pgen_req = PL - Ppv - Pw;
            PLNG_req = PL - Ppv - Pw;
            PENG3_req = 0;
            PDG1_req = 0;
            PDG2_req = 0;
            Pbat_discharge = 0;
            Pbat_charge = 0;
            Pspare = 0;
            cutin_LNG = 1;
            cutout_LNG = 0;
            cutin_ENG3 = 0;
            cutout_ENG3 = 1;
            cutin_DG1 = 0;
            cutout_DG1 = 1;
            cutin_DG2 = 0;
            cutout_DG2 = 1;
            load_cutout = 0;
        }
    }

    state LNG_Covers_Load_LowSoC_ChargeMargin {
        enter {
            Pgen_req = PL - Ppv - Pw + Pgmax / 5;
            PLNG_req = PL - Ppv - Pw + Pgmax / 5;
            PENG3_req = 0;
            PDG1_req = 0;
            PDG2_req = 0;
            Pbat_discharge = 0;
            Pbat_charge = Pgmax / 5;
            Pspare = 0;
            cutin_LNG = 1;
            cutout_LNG = 0;
            cutin_ENG3 = 0;
            cutout_ENG3 = 1;
            cutin_DG1 = 0;
            cutout_DG1 = 1;
            cutin_DG2 = 0;
            cutout_DG2 = 1;
            load_cutout = 0;
        }
    }

    state LNG_Engine3_Covers_Load {
        enter {
            Pgen_req = PL - Ppv - Pw;
            PLNG_req = Pgmax;
            PENG3_req = PL - Ppv - Pw - Pgmax;
            PDG1_req = 0;
            PDG2_req = 0;
            Pbat_discharge = 0;
            Pbat_charge = 0;
            Pspare = 0;
            cutin_LNG = 1;
            cutout_LNG = 0;
            cutin_ENG3 = 1;
            cutout_ENG3 = 0;
            cutin_DG1 = 0;
            cutout_DG1 = 1;
            cutin_DG2 = 0;
            cutout_DG2 = 1;
            load_cutout = 0;
        }
    }

    state DG1_Covers_Load {
        enter {
            Pgen_req = PL - Ppv - Pw;
            PLNG_req = Pgmax;
            PENG3_req = eng3_Pmax;
            PDG1_req = PL - Ppv - Pw - Pgmax - eng3_Pmax;
            PDG2_req = 0;
            Pbat_discharge = 0;
            Pbat_charge = 0;
            Pspare = 0;
            cutin_LNG = 1;
            cutout_LNG = 0;
            cutin_ENG3 = 1;
            cutout_ENG3 = 0;
            cutin_DG1 = 1;
            cutout_DG1 = 0;
            cutin_DG2 = 0;
            cutout_DG2 = 1;
            load_cutout = 0;
        }
    }

    state DG1_Covers_Load_LowSoC_ChargeMargin {
        enter {
            Pgen_req = PL - Ppv - Pw + Pd1max / 10;
            PLNG_req = Pgmax;
            PENG3_req = eng3_Pmax;
            PDG1_req = PL - Ppv - Pw - Pgmax - eng3_Pmax + Pd1max / 10;
            PDG2_req = 0;
            Pbat_discharge = 0;
            Pbat_charge = Pd1max / 10;
            Pspare = 0;
            cutin_LNG = 1;
            cutout_LNG = 0;
            cutin_ENG3 = 1;
            cutout_ENG3 = 0;
            cutin_DG1 = 1;
            cutout_DG1 = 0;
            cutin_DG2 = 0;
            cutout_DG2 = 1;
            load_cutout = 0;
        }
    }

    state DG2_Covers_Load_WithOptionalChargeMargin {
        enter {
            if [SoC < 0.20] {
                Pgen_req = PL - Ppv - Pw + Pd1max / 10;
                PLNG_req = Pgmax;
                PENG3_req = eng3_Pmax;
                PDG1_req = Pd1max;
                PDG2_req = PL - Ppv - Pw - Pgmax - eng3_Pmax - Pd1max + Pd1max / 10;
                Pbat_charge = Pd1max / 10;
            } else {
                Pgen_req = PL - Ppv - Pw;
                PLNG_req = Pgmax;
                PENG3_req = eng3_Pmax;
                PDG1_req = Pd1max;
                PDG2_req = PL - Ppv - Pw - Pgmax - eng3_Pmax - Pd1max;
                Pbat_charge = 0;
            }
            Pbat_discharge = 0;
            Pspare = 0;
            cutin_LNG = 1;
            cutout_LNG = 0;
            cutin_ENG3 = 1;
            cutout_ENG3 = 0;
            cutin_DG1 = 1;
            cutout_DG1 = 0;
            cutin_DG2 = 1;
            cutout_DG2 = 0;
            load_cutout = 0;
        }
    }

    state IllegalOverloadCompletion {
        enter {
            Pgen_req = Pgmax + eng3_Pmax + Pd1max + Pd2max;
            PLNG_req = P
... <truncated 506 chars; see run record>
```

#### Candidate diff（before -> candidate）

```diff
--- before.fcstm
+++ candidate.fcstm
@@ -2,8 +2,6 @@
 def float Ppv = 0.0;
 def float Pw = 0.0;
 def float SoC = 0.50;
-def float SoC_full_threshold = 0.95;
-def float SoC_low_threshold = 0.20;
 def float Pgmax = 0.0;
 def float eng3_Pmax = 0.0;
 def float Pd1max = 0.0;
@@ -29,16 +27,16 @@
 
 state LNGShipEMS {
     ! * -> IllegalOverloadCompletion : if [PL - Ppv - Pw > Pgmax + eng3_Pmax + Pd1max + Pd2max + Pbat_discharge_Pmax];
-    ! * -> ZeroLoad_RES_Charge : if [PL == 0 && Ppv + Pw > 0 && SoC < SoC_full_threshold];
-    ! * -> ZeroLoad_RES_Spare : if [PL == 0 && Ppv + Pw > 0 && SoC >= SoC_full_threshold];
-    ! * -> RES_Covers_Load_Charge : if [PL > 0 && Ppv + Pw >= PL && SoC < SoC_full_threshold];
-    ! * -> RES_Covers_Load_Spare : if [PL > 0 && Ppv + Pw >= PL && SoC >= SoC_full_threshold];
-    ! * -> Battery_Discharge_Priority : if [PL > 0 && Ppv + Pw < PL && SoC >= SoC_low_threshold && PL - Ppv - Pw <= Pbat_discharge_Pmax];
-    ! * -> LNG_Covers_Load_LowSoC_ChargeMargin : if [PL > 0 && Ppv + Pw < PL && SoC < SoC_low_threshold && PL - Ppv - Pw + Pgmax / 5 <= Pgmax];
+    ! * -> ZeroLoad_RES_Charge : if [PL == 0 && Ppv + Pw > 0 && SoC < 0.95];
+    ! * -> ZeroLoad_RES_Spare : if [PL == 0 && Ppv + Pw > 0 && SoC >= 0.95];
+    ! * -> RES_Covers_Load_Charge : if [PL > 0 && Ppv + Pw >= PL && SoC < 0.95];
+    ! * -> RES_Covers_Load_Spare : if [PL > 0 && Ppv + Pw >= PL && SoC >= 0.95];
+    ! * -> Battery_Discharge_Priority : if [PL > 0 && Ppv + Pw < PL && SoC >= 0.20 && PL - Ppv - Pw <= Pbat_discharge_Pmax];
+    ! * -> LNG_Covers_Load_LowSoC_ChargeMargin : if [PL > 0 && Ppv + Pw < PL && SoC < 0.20 && PL - Ppv - Pw + Pgmax / 5 <= Pgmax];
     ! * -> LNG_Covers_Load : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > Pbat_discharge_Pmax && PL - Ppv - Pw <= Pgmax];
     ! * -> LNG_Engine3_Covers_Load : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > Pgmax && PL - Ppv - Pw <= Pgmax + eng3_Pmax];
-    ! * -> DG1_Covers_Load_LowSoC_ChargeMargin : if [PL > 0 && Ppv + Pw < PL && SoC < SoC_low_threshold && PL - Ppv - Pw > Pgmax + eng3_Pmax && PL - Ppv - Pw + Pd1max / 10 <= Pgmax + eng3_Pmax + Pd1max];
-    ! * -> DG1_Covers_Load : if [PL > 0 && Ppv + Pw < PL && SoC >= SoC_low_threshold && PL - Ppv - Pw > Pgmax + eng3_Pmax && PL - Ppv - Pw <= Pgmax + eng3_Pmax + Pd1max];
+    ! * -> DG1_Covers_Load_LowSoC_ChargeMargin : if [PL > 0 && Ppv + Pw < PL && SoC < 0.20 && PL - Ppv - Pw > Pgmax + eng3_Pmax && PL - Ppv - Pw + Pd1max / 10 <= Pgmax + eng3_Pmax + Pd1max];
+    ! * -> DG1_Covers_Load : if [PL > 0 && Ppv + Pw < PL && SoC >= 0.20 && PL - Ppv - Pw > Pgmax + eng3_Pmax && PL - Ppv - Pw <= Pgmax + eng3_Pmax + Pd1max];
     ! * -> DG2_Covers_Load_WithOptionalChargeMargin : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > Pgmax + eng3_Pmax + Pd1max && PL - Ppv - Pw <= Pgmax + eng3_Pmax + Pd1max + Pd2max];
 
     [*] -> ZeroLoad_RES_Charge;
@@ -265,7 +263,7 @@
 
     state DG2_Covers_Load_WithOptionalChargeMargin {
         enter {
-            if [SoC < SoC_low_threshold] {
+            if [SoC < 0.20] {
                 Pgen_req = PL - Ppv - Pw + Pd1max / 10;
                 PLNG_req = Pgmax;
                 PENG3_req = eng3_Pmax;
```

#### SL-10 审查结果

- SL-10 decision=`pass`，ok=`True`，target_resolved=`True`，regression_detected=`False`，drift_risk=`minor`。
- SL-10 review_meta：schema=`SL10RepairReviewOutput.v1`，failure_policy=`fail_closed`，replay_key=`SL-10:sha256:c69427a31932cf912d20a65cc68ca77370b0bfb8bb0493047ced6579b95860e5`。
  - SL-10 evidence 1: `{"summary": "The accepted SL-9 edits are limited to removing the fixed SoC threshold variables and replacing their reads with literals 0.95 and 0.20. This is consistent with the NL: 0.95 is explicitly required as the full-SoC threshold, while the low threshold was an admitted tunable abstraction with no NL-provided update law. The candidate preserves all twelve dispatch states and the required zero-load, RES charge/spare, battery-priority, LNG, DG1/DG2, low-SoC margin, and illegal overload behaviors."}`
  - SL-10 evidence 2: `{"summary": "The SL-9 rejected/waived requests for Pd2max, Pbat_discharge_Pmax, and guard variables are justified by the NL and request constraints: these are external load/resource/capacity inputs or bounds used to classify dispatch feasibility, and the NL does not define internal FSM actions that update them. Adding self-assignments or invented dynamics would violate the forbidden edits."}`
  - SL-10 evidence 3: `{"summary": "The DSL diff does not delete required states, variables, cut-in/cut-out commands, dispatch outputs, or overload behavior. The candidate still returns Pgen_req, Pbat_discharge, Pbat_charge, and Pspare; preserves generator-specific requests; issues cut-in/cut-out commands for LNG, ENG3, DG1, DG2; and uses load_cutout only in the illegal overload completion state as previously modeled."}`
  - SL-10 evidence 4: `{"summary": "Local deterministic evidence reports no regression but flags unresolved design warnings and missing_required_grounding for transition:classify_zero_load and transition:classify_dg_late_priority. Behaviorally, the candidate contains concrete wildcard classification transitions for zero-load charging/spare states and for late diesel priority via DG1/DG2 dispatch guards, so the NL-required obligations remain represented even though the local grounding matcher did not recognize those IDs."}`
- local checks evidence：stage=`SD-10`；note=PR-E1 uses local parse/semantic/design/sim checks as SL-10 evidence, not as the final deterministic judge.。
  - local ok=`False`，target_resolved=`False`，regression_detected=`False`，drift_risk=`major`。
  - local_rejection：reason=`design_target_unresolved; missing_required_grounding`，rejected_by_stage=`SD-10`。
    - local evidence 1: `design_target_unresolved` {"items": [{"budget_exhausted": false, "budget_remaining": 1, "code": "W_UNWRITTEN_READ_VAR", "instance_key": "W_UNWRITTEN_READ_VAR:var_name=Pd2max", "message": "Variable 'Pd2max' is read but never written by any action or transition effect.", "policy_action": "budgeted_repair", "pyfcstm_severity": "warning", "rationale": "", "refs": {"init_value": "0.0", "read_states": ["LNGShipEMS.Battery_Discharge_Priority", "LNGShipEMS.DG1_Covers_Load", "LNGShipEMS.DG1_Covers_Load_LowSoC_ChargeMargin", "LNGS...<truncated 63748 chars>
    - local evidence 2: `missing_required_grounding` {"element_ids": ["transition:classify_zero_load", "transition:classify_dg_late_priority"], "kind": "missing_required_grounding"}

</details>

<details><summary>Repair 2 / iteration `1` / source `SD-4` / accepted=❌</summary>

#### 为什么进入修复

- selected feedback source：`SD-4`；blocking=`True`；pre_scenario=`True`。
- problem_summary：Variable 'Pd2max' is read but never written by any action or transition effect.; Variable 'Pbat_discharge_Pmax' is read but never written by any action or transition effect.; Transition guard reads only variables that are never changed by actions or effects.
- diagnostic ids：`W_UNWRITTEN_READ_VAR:var_name=Pd2max, W_UNWRITTEN_READ_VAR:var_name=Pbat_discharge_Pmax, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoad_RES_Charge:to_path=LNGShipEMS.IllegalOverloadCompletion, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoad_RES_Charge:to_path=LNGShipEMS.Battery_Discharge_Priority, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoad_RES_Charge:to_path=LNGShipEMS.LNG_Covers_Load, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoad_RES_Charge:to_path=LNGShipEMS.DG2_Covers_Load_WithOptionalChargeMargin, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoad_RES_Spare:to_path=LNGShipEMS.IllegalOverloadCompletion, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoad_RES_Spare:to_path=LNGShipEMS.Battery_Discharge_Priority, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoad_RES_Spare:to_path=LNGShipEMS.LNG_Covers_Load, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoad_RES_Spare:to_path=LNGShipEMS.DG2_Covers_Load_WithOptionalChargeMargin, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.RES_Covers_Load_Charge:to_path=LNGShipEMS.IllegalOverloadCompletion, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.RES_Covers_Load_Charge:to_path=LNGShipEMS.Battery_Discharge_Priority, ... +43`。
- before_dsl_hash：`sha256:ae74dfc8a541f448b34f805ad6dbf46262a2b2b804509e2e7866abecbe67c8aa`；candidate_dsl_hash：`sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

#### 错误证据 / diagnostics

- 1. `W_UNWRITTEN_READ_VAR` `W_UNWRITTEN_READ_VAR:var_name=Pd2max` policy=`budgeted_repair`：Variable 'Pd2max' is read but never written by any action or transition effect.；refs=`{"init_value": "0.0", "read_states": ["LNGShipEMS.Battery_Discharge_Priority", "LNGShipEMS.DG1_Covers_Load", "LNGShipEMS.DG1_Covers_Load_LowSoC_ChargeMargin", "LNGShipEMS.DG2_Covers_Load_WithOptionalChargeMargin", "LNGShipEMS.IllegalOverloadCompletion", "LNGShipEMS.LNG_Covers_Load", "LNGShipEMS.LNG_...<truncated 234 chars>`
- 2. `W_UNWRITTEN_READ_VAR` `W_UNWRITTEN_READ_VAR:var_name=Pbat_discharge_Pmax` policy=`budgeted_repair`：Variable 'Pbat_discharge_Pmax' is read but never written by any action or transition effect.；refs=`{"init_value": "0.0", "read_states": ["LNGShipEMS.Battery_Discharge_Priority", "LNGShipEMS.DG1_Covers_Load", "LNGShipEMS.DG1_Covers_Load_LowSoC_ChargeMargin", "LNGShipEMS.DG2_Covers_Load_WithOptionalChargeMargin", "LNGShipEMS.IllegalOverloadCompletion", "LNGShipEMS.LNG_Covers_Load", "LNGShipEMS.LNG_...<truncated 247 chars>`
- 3. `W_GUARD_VARS_NEVER_CHANGE` `W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoad_RES_Charge:to_path=LNGShipEMS.IllegalOverloadCompletion` policy=`budgeted_repair`：Transition guard reads only variables that are never changed by actions or effects.；refs=`{"from_path": "LNGShipEMS.ZeroLoad_RES_Charge", "guard_vars": ["PL", "Pbat_discharge_Pmax", "Pd1max", "Pd2max", "Pgmax", "Ppv", "Pw", "eng3_Pmax"], "to_path": "LNGShipEMS.IllegalOverloadCompletion"}`
- 4. `W_GUARD_VARS_NEVER_CHANGE` `W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoad_RES_Charge:to_path=LNGShipEMS.Battery_Discharge_Priority` policy=`budgeted_repair`：Transition guard reads only variables that are never changed by actions or effects.；refs=`{"from_path": "LNGShipEMS.ZeroLoad_RES_Charge", "guard_vars": ["PL", "Pbat_discharge_Pmax", "Ppv", "Pw", "SoC"], "to_path": "LNGShipEMS.Battery_Discharge_Priority"}`
- 5. `W_GUARD_VARS_NEVER_CHANGE` `W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoad_RES_Charge:to_path=LNGShipEMS.LNG_Covers_Load` policy=`budgeted_repair`：Transition guard reads only variables that are never changed by actions or effects.；refs=`{"from_path": "LNGShipEMS.ZeroLoad_RES_Charge", "guard_vars": ["PL", "Pbat_discharge_Pmax", "Pgmax", "Ppv", "Pw"], "to_path": "LNGShipEMS.LNG_Covers_Load"}`
- 6. `W_GUARD_VARS_NEVER_CHANGE` `W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoad_RES_Charge:to_path=LNGShipEMS.DG2_Covers_Load_WithOptionalChargeMargin` policy=`budgeted_repair`：Transition guard reads only variables that are never changed by actions or effects.；refs=`{"from_path": "LNGShipEMS.ZeroLoad_RES_Charge", "guard_vars": ["PL", "Pd1max", "Pd2max", "Pgmax", "Ppv", "Pw", "eng3_Pmax"], "to_path": "LNGShipEMS.DG2_Covers_Load_WithOptionalChargeMargin"}`
- 7. `W_GUARD_VARS_NEVER_CHANGE` `W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoad_RES_Spare:to_path=LNGShipEMS.IllegalOverloadCompletion` policy=`budgeted_repair`：Transition guard reads only variables that are never changed by actions or effects.；refs=`{"from_path": "LNGShipEMS.ZeroLoad_RES_Spare", "guard_vars": ["PL", "Pbat_discharge_Pmax", "Pd1max", "Pd2max", "Pgmax", "Ppv", "Pw", "eng3_Pmax"], "to_path": "LNGShipEMS.IllegalOverloadCompletion"}`
- 8. `W_GUARD_VARS_NEVER_CHANGE` `W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoad_RES_Spare:to_path=LNGShipEMS.Battery_Discharge_Priority` policy=`budgeted_repair`：Transition guard reads only variables that are never changed by actions or effects.；refs=`{"from_path": "LNGShipEMS.ZeroLoad_RES_Spare", "guard_vars": ["PL", "Pbat_discharge_Pmax", "Ppv", "Pw", "SoC"], "to_path": "LNGShipEMS.Battery_Discharge_Priority"}`
- ……另有 `42` 条 evidence 见 run record。

#### 变量角色与上下文提示

- policy：Advisory only. Do not invent writes for external_input_candidate variables unless NL explicitly gives update semantics; add meaningful NL-grounded writes only for internal state variables.
- source：SD-4 diagnostic refs and generic NL external-input rationale

| Variable | role_hint | nl_token_present | diagnostics |
|---|---|---:|---|
| `PDG1_req` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `PDG2_req` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `PENG3_req` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `PL` | `external_input_candidate` | ✅ | `W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +140` |
| `PLNG_req` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `Pbat_charge` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `Pbat_discharge` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `Pbat_discharge_Pmax` | `unknown` | ❌ | `W_UNWRITTEN_READ_VAR, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +32` |
| `Pd1max` | `external_input_candidate` | ✅ | `W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +44` |
| `Pd2max` | `unknown` | ❌ | `W_UNWRITTEN_READ_VAR, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +20` |
| `Pgen_req` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `Pgmax` | `external_input_candidate` | ✅ | `W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +80` |
| `Ppv` | `external_input_candidate` | ✅ | `W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +140` |
| `Pspare` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `Pw` | `external_input_candidate` | ✅ | `W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +140` |
| `SoC` | `external_input_candidate` | ✅ | `W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +92` |
| `cutin_DG1` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `cutin_DG2` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `cutin_ENG3` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `cutin_LNG` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `cutout_DG1` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `cutout_DG2` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `cutout_ENG3` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `cutout_LNG` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `eng3_Pmax` | `external_input_candidate` | ✅ | `W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, W_GUARD_VARS_NEVER_CHANGE, ... +56` |
| `load_cutout` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |

#### SD-8 FixRequestBatch / 修改请求

- batch_id：`fixbatch-1-sha256-5a45bfc6f1a`；source_stage=`SD-4`；legacy_plan_kind=`FixPlan`；requests=`12`。

| request_id | severity | hard | waiver | problem | evidence |
|---|---|---:|---:|---|---|
| `fixreq-1-sd4-0-f26560796c` | `blocking_warning` | ❌ | ✅ | Variable 'Pd2max' is read but never written by any action or transition effect.; Variable 'Pbat_discharge_Pmax' is read but never written by any action or transition effect.; Transition guard reads only variables that ar...<truncated 38 chars> | `W_UNWRITTEN_READ_VAR` |
| `fixreq-1-sd4-1-2efb61e37b` | `blocking_warning` | ❌ | ✅ | Variable 'Pd2max' is read but never written by any action or transition effect.; Variable 'Pbat_discharge_Pmax' is read but never written by any action or transition effect.; Transition guard reads only variables that ar...<truncated 38 chars> | `W_UNWRITTEN_READ_VAR` |
| `fixreq-1-sd4-2-005b201e59` | `blocking_warning` | ❌ | ✅ | Variable 'Pd2max' is read but never written by any action or transition effect.; Variable 'Pbat_discharge_Pmax' is read but never written by any action or transition effect.; Transition guard reads only variables that ar...<truncated 38 chars> | `W_GUARD_VARS_NEVER_CHANGE` |
| `fixreq-1-sd4-3-463b1d2014` | `blocking_warning` | ❌ | ✅ | Variable 'Pd2max' is read but never written by any action or transition effect.; Variable 'Pbat_discharge_Pmax' is read but never written by any action or transition effect.; Transition guard reads only variables that ar...<truncated 38 chars> | `W_GUARD_VARS_NEVER_CHANGE` |
| `fixreq-1-sd4-4-be03b849c3` | `blocking_warning` | ❌ | ✅ | Variable 'Pd2max' is read but never written by any action or transition effect.; Variable 'Pbat_discharge_Pmax' is read but never written by any action or transition effect.; Transition guard reads only variables that ar...<truncated 38 chars> | `W_GUARD_VARS_NEVER_CHANGE` |
| `fixreq-1-sd4-5-5da41bd3dc` | `blocking_warning` | ❌ | ✅ | Variable 'Pd2max' is read but never written by any action or transition effect.; Variable 'Pbat_discharge_Pmax' is read but never written by any action or transition effect.; Transition guard reads only variables that ar...<truncated 38 chars> | `W_GUARD_VARS_NEVER_CHANGE` |
| `fixreq-1-sd4-6-6ab31d0b6d` | `blocking_warning` | ❌ | ✅ | Variable 'Pd2max' is read but never written by any action or transition effect.; Variable 'Pbat_discharge_Pmax' is read but never written by any action or transition effect.; Transition guard reads only variables that ar...<truncated 38 chars> | `W_GUARD_VARS_NEVER_CHANGE` |
| `fixreq-1-sd4-7-9ba6a1e517` | `blocking_warning` | ❌ | ✅ | Variable 'Pd2max' is read but never written by any action or transition effect.; Variable 'Pbat_discharge_Pmax' is read but never written by any action or transition effect.; Transition guard reads only variables that ar...<truncated 38 chars> | `W_GUARD_VARS_NEVER_CHANGE` |
| `fixreq-1-sd4-8-3575ef8b3e` | `blocking_warning` | ❌ | ✅ | Variable 'Pd2max' is read but never written by any action or transition effect.; Variable 'Pbat_discharge_Pmax' is read but never written by any action or transition effect.; Transition guard reads only variables that ar...<truncated 38 chars> | `W_GUARD_VARS_NEVER_CHANGE` |
| `fixreq-1-sd4-9-78b67424f0` | `blocking_warning` | ❌ | ✅ | Variable 'Pd2max' is read but never written by any action or transition effect.; Variable 'Pbat_discharge_Pmax' is read but never written by any action or transition effect.; Transition guard reads only variables that ar...<truncated 38 chars> | `W_GUARD_VARS_NEVER_CHANGE` |
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
- required_preserve_element_ids：`state:LNGShipEMS, variable:PL, variable:Ppv, variable:Pw, variable:SoC, variable:eng3_Pmax, variable:Pgmax, variable:Pd1max, variable:Pgen_req, variable:Pbat_discharge, variable:Pbat_charge, variable:Pspare, ... +25`。

#### SL-9 per-request 决策

- accepted_request_ids：`<derived-from-table>`；candidate_len=`0`。

| request_id | decision | waiver | rework_locked | rationale / intent |
|---|---|---:|---:|---|
| `fixreq-1-sd4-0-f26560796c` | `reject` | ✅ | ❌ | Pd2max is an NL-grounded diesel-generator capacity bound/external input used to classify dispatch feasibility. The NL gives no FSM action or update law that writes this capacity. Adding a write would invent ungrounded plant dynamics or a meaningless self-assignment, both forbidden. |
| `fixreq-1-sd4-1-2efb61e37b` | `reject` | ✅ | ❌ | Pbat_discharge_Pmax is an NL-grounded battery discharge capacity bound/external input. It is intentionally read by dispatch guards, and the NL provides no internal EMS update semantics for it. A write would be artificial and unsafe. |
| `fixreq-1-sd4-2-005b201e59` | `reject` | ✅ | ❌ | The IllegalOverloadCompletion guard from ZeroLoad_RES_Charge reads external demand, renewable, and capacity inputs: PL, Ppv, Pw, Pgmax, eng3_Pmax, Pd1max, Pd2max, and Pbat_discharge_Pmax. These are exactly the changing operating-condition inputs described by the NL, not internal state variables with FSM update laws. |
| `fixreq-1-sd4-3-463b1d2014` | `reject` | ✅ | ❌ | The Battery_Discharge_Priority guard from ZeroLoad_RES_Charge reads PL, Ppv, Pw, SoC, and Pbat_discharge_Pmax, all of which are NL-described external measurements or capacity bounds. No safe NL-grounded action exists to update them inside the FSM. |
| `fixreq-1-sd4-4-be03b849c3` | `reject` | ✅ | ❌ | The LNG_Covers_Load guard from ZeroLoad_RES_Charge reads external demand/resource/capacity inputs. Replacing those reads or adding writes would reduce NL fidelity because the EMS is supposed to classify changing operating conditions supplied from outside the controller. |
| `fixreq-1-sd4-5-5da41bd3dc` | `reject` | ✅ | ❌ | The DG2 late-priority guard from ZeroLoad_RES_Charge depends on external load, renewable production, and generator capacity bounds. The NL does not provide internal dynamics for these variables; the correct conservative behavior is to keep the guard and waive the never-change warning. |
| `fixreq-1-sd4-6-6ab31d0b6d` | `reject` | ✅ | ❌ | The IllegalOverloadCompletion guard from ZeroLoad_RES_Spare intentionally classifies an extreme external demand/resource/capacity condition. All guard variables are external inputs or capacity bounds, so adding writes would be ungrounded. |
| `fixreq-1-sd4-7-9ba6a1e517` | `reject` | ✅ | ❌ | The Battery_Discharge_Priority guard from ZeroLoad_RES_Spare reads external demand, RES, SoC, and battery capacity inputs. These are not internal FSM variables and should not be updated artificially. |
| `fixreq-1-sd4-8-3575ef8b3e` | `reject` | ✅ | ❌ | The LNG_Covers_Load guard from ZeroLoad_RES_Spare reads external operating-condition inputs. The NL describes the EMS as reading these values, not generating or updating them internally. |
| `fixreq-1-sd4-9-78b67424f0` | `reject` | ✅ | ❌ | The DG2 late-priority guard from ZeroLoad_RES_Spare depends on external demand/resource/capacity bounds. Keeping the guard preserves the required DG1/DG2 last-priority classification; adding writes would invent plant dynamics. |
| `fixreq-1-sd4-10-e2a5930ee7` | `reject` | ✅ | ❌ | The IllegalOverloadCompletion guard from RES_Covers_Load_Charge reads only external inputs and capacity bounds. The overload completion branch is NL-required as an illegal/extreme classification, and there is no safe internal update to add. |
| `fixreq-1-sd4-11-b223c4c43d` | `reject` | ✅ | ❌ | The Battery_Discharge_Priority guard from RES_Covers_Load_Charge reads external PL, Ppv, Pw, SoC, and Pbat_discharge_Pmax. The NL explicitly says the FSM reads these values, so the warning is best waived rather than repaired by ungrounded writes. |
- repair_rationale：All current fix requests target never-written reads or guards over variables that the NL defines as external measurements or capacity bounds: PL, Ppv, Pw, SoC, Pgmax, eng3_Pmax, Pd1max, Pd2max, and Pbat_discharge_Pmax.；The FixLog shows Pd2max and Pbat_discharge_Pmax were previously rejected/waived for the same reason, and no new evidence provides an NL-grounded update law for them.；Adding self-assignments, synthetic command variables, or plant/environment dynamics would violate the request’s forbidden edits and reduce NL fidelity.；The prior local grounding concern for classify_zero_load and classify_dg_late_priority is not a safe basis for altering this batch’s warning targets: the current DSL already has concrete wildcard classification transitions for zero-load cha...<truncated 164 chars>
- diff_summary：`{"summary": "No DSL edit was made. All current requests were rejected/waived because the flagged variables are NL-grounded external inputs or capacity bounds, and no safe NL-grounded internal write exists."}`。

#### SL-9 candidate / 最终修改执行方案

- 本 repair 未记录 candidate_dsl。

#### Candidate diff（before -> candidate）

- 无 candidate DSL，因此无法生成 diff。

#### SL-10 审查结果

- SL-10：`<none>`（旧 record 或本 run 未进入 LLM repair review）。
- legacy repair_review：ok=`True`，target_resolved=`True`，regression_detected=`False`，drift_risk=`minor`。

</details>

<details><summary>Repair 3 / iteration `2` / source `SL-7` / accepted=❌</summary>

#### 为什么进入修复

- selected feedback source：`SL-7`；blocking=`True`；pre_scenario=`False`。
- problem_summary：model review failed
- diagnostic ids：`0, 1, 2, 3`。
- before_dsl_hash：`sha256:ae74dfc8a541f448b34f805ad6dbf46262a2b2b804509e2e7866abecbe67c8aa`；candidate_dsl_hash：`sha256:4c5a6347ae4632bd2b168c1d08eef85bdcfb190e6335c8e955fb8d53d02b8d19`。

#### 错误证据 / diagnostics

- 1. `<unknown>` `` policy=``：The illegal overload branch requests battery discharge beyond the declared battery discharge capacity.
- 2. `<unknown>` `` policy=``：The illegal overload transition does not match the NL condition of demand exceeding all RES and thermal resources and then using battery discharge to cover the lack.
- 3. `<unknown>` `` policy=``：The model leaves the thermal-exceeded but battery-coverable deficit interval without an explicit NL-grounded transition.
- 4. `<unknown>` `` policy=``：The simulation oracle misses the critical overload boundary and therefore gives a false sense of coverage.

#### SD-8 FixRequestBatch / 修改请求

- batch_id：`fixbatch-2-sha256-2baadc6ec74`；source_stage=`SL-7`；legacy_plan_kind=`FixPlan`；requests=`4`。

| request_id | severity | hard | waiver | problem | evidence |
|---|---|---:|---:|---|---|
| `fixreq-2-sl7-0-e56a9044a1` | `review_fail` | ✅ | ❌ | model review failed | `{'category': 'unsafe_recovery', 'evidence': ['Guard: PL - Ppv - Pw > Pgmax + eng3_Pmax + Pd1max + Pd2max + Pbat_discharge_Pmax.', 'Action: Pbat_discharge = PL - Ppv - Pw - Pgmax - eng3_Pmax - Pd1max - Pd2max.', 'Therefore selected IllegalOverloadCompletion always assigns Pbat_discharge > Pbat_discharge_Pmax.'], 'severity': 'major', 'summary': 'The illegal overload branch requests battery discharge beyond the declared battery discharge capacity.'}` |
| `fixreq-2-sl7-1-ef61a52a60` | `review_fail` | ✅ | ❌ | model review failed | `{'category': 'nl_fidelity', 'evidence': ['NL describes overload completion when extreme demand exceeds RES and thermal resources.', 'DSL only enters IllegalOverloadCompletion when demand exceeds RES, thermal resources, and battery discharge capacity.', 'The NL-described thermal-exceeded but battery-coverable region is not represented.'], 'severity': 'major', 'summary': 'The illegal overload transition does not match the NL condition of demand exceeding all RES and thermal resources and then using battery discharge to cover the lack.'}` |
| `fixreq-2-sl7-2-86839a6bcb` | `review_fail` | ✅ | ❌ | model review failed | `{'category': 'coverage_gap', 'evidence': ['DG2 guard ends at deficit <= Pgmax + eng3_Pmax + Pd1max + Pd2max.', 'Illegal overload guard begins only at deficit > Pgmax + eng3_Pmax + Pd1max + Pd2max + Pbat_discharge_Pmax.', 'No transition covers the interval between those bounds.'], 'severity': 'major', 'summary': 'The model leaves the thermal-exceeded but battery-coverable deficit interval without an explicit NL-grounded transition.'}` |
| `fixreq-2-sl7-3-4a91513941` | `review_fail` | ✅ | ❌ | model review failed | `{'category': 'path1_eval_risk', 'evidence': ['sim_summary reports all 15 scenarios passed.', 'The illegal overload scenario only tests demand beyond thermal plus battery capacity.', 'No shown scenario tests demand beyond thermal capacity but within battery discharge capacity.'], 'severity': 'major', 'summary': 'The simulation oracle misses the critical overload boundary and therefore gives a false sense of coverage.'}` |

#### SD-8 legacy fix plan / 修改建议

- recommended_strategy：Use diagnostics as hints; choose the smallest globally consistent repair.；Before returning a candidate, verify every required_preserve_element_id still has a concrete DSL representation.
- forbidden_edits：`Do not delete grounded required elements merely to silence diagnostics., Do not invent internal plant/environment dynamics merely to make external input variables appear written.`。
- required_preserve_element_ids：`state:LNGShipEMS, variable:PL, variable:Ppv, variable:Pw, variable:SoC, variable:eng3_Pmax, variable:Pgmax, variable:Pd1max, variable:Pgen_req, variable:Pbat_discharge, variable:Pbat_charge, variable:Pspare, ... +25`。

#### SL-9 per-request 决策

- accepted_request_ids：`<derived-from-table>`；candidate_len=`9589`。

| request_id | decision | waiver | rework_locked | rationale / intent |
|---|---|---:|---:|---|
| `fixreq-2-sl7-0-e56a9044a1` | `accept` | ❌ | ❌ | The existing IllegalOverloadCompletion guard selected the state only when the remaining deficit exceeded thermal capacity plus battery discharge capacity, so its enter action necessarily assigned Pbat_discharge above Pbat_discharge_Pmax. The smallest safe edit is to restrict this state to the NL-described thermal-exceeded interval that the battery can cover....<truncated 150 chars> |
| `fixreq-2-sl7-1-ef61a52a60` | `accept` | ❌ | ❌ | The NL says the overload completion condition is demand exceeding RES and thermal resources, with the lack covered by battery discharge. The revised guard now starts immediately above total thermal capacity rather than above thermal plus battery capacity.；intent=Make IllegalOverloadCompletion represent the thermal-exceeded battery-discharge branch |
| `fixreq-2-sl7-2-86839a6bcb` | `accept` | ❌ | ❌ | The prior model left the interval thermal < deficit <= thermal + Pbat_discharge_Pmax uncovered. The revised IllegalOverloadCompletion forced transition explicitly covers that interval and preserves the existing DG2 guard up to the thermal bound.；intent=Cover the gap between total thermal capacity and total thermal plus battery discharge capacity |
| `fixreq-2-sl7-3-4a91513941` | `accept` | ❌ | ❌ | Although scenario coverage is external to the DSL, the model defect behind the oracle risk is repaired by adding the missing critical overload boundary behavior. A scenario testing thermal-exceeded but battery-coverable demand would now enter IllegalOverloadCompletion with Pbat_discharge within Pbat_discharge_Pmax.；intent=Repair the model behavior at the ove...<truncated 54 chars> |
- repair_rationale：Addressed the new SL-7 model-review target rather than re-fixing previously waived external-input warnings.；Expected behavior for IllegalOverloadCompletion: deficit exceeds total thermal generation Pgmax + eng3_Pmax + Pd1max + Pd2max, all thermal units are requested, and the remaining lack is covered by battery discharge.；Prior actual behavior: IllegalOverloadCompletion only fired when deficit exceeded total thermal plus Pbat_discharge_Pmax, making Pbat_discharge necessarily greater than Pbat_discharge_Pmax and leaving the thermal-exceeded battery-coverable ...<truncated 19 chars>；The repaired guard covers PL - Ppv - Pw > total thermal and <= total thermal + Pbat_discharge_Pmax, so Pbat_discharge equals the remaining deficit above thermal and remains within the declared battery discharge capacity.；All required variables, twelve required states, zero-load classification transitions, RES charge/spare transitions, battery priority, LNG priority, DG1/DG2 late priority, low-SoC charge margins, cut-in/cut-out commands, and load_cutout beha...<truncated 19 chars>
- diff_summary：`{"summary": "Changed only the IllegalOverloadCompletion forced-transition guard. It now selects the NL-grounded thermal-exceeded but battery-coverable interval instead of selecting only beyond thermal plus battery capacity, eliminating the unsafe battery over-discharge assignment and closing the coverage gap."}`。

#### SL-9 candidate / 最终修改执行方案

```pyfcstm
def float PL = 0.0;
def float Ppv = 0.0;
def float Pw = 0.0;
def float SoC = 0.50;
def float Pgmax = 0.0;
def float eng3_Pmax = 0.0;
def float Pd1max = 0.0;
def float Pd2max = 0.0;
def float Pbat_discharge_Pmax = 0.0;
def float Pgen_req = 0.0;
def float PLNG_req = 0.0;
def float PENG3_req = 0.0;
def float PDG1_req = 0.0;
def float PDG2_req = 0.0;
def float Pbat_discharge = 0.0;
def float Pbat_charge = 0.0;
def float Pspare = 0.0;
def int cutin_LNG = 0;
def int cutout_LNG = 0;
def int cutin_ENG3 = 0;
def int cutout_ENG3 = 0;
def int cutin_DG1 = 0;
def int cutout_DG1 = 0;
def int cutin_DG2 = 0;
def int cutout_DG2 = 0;
def int load_cutout = 0;

state LNGShipEMS {
    ! * -> IllegalOverloadCompletion : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > Pgmax + eng3_Pmax + Pd1max + Pd2max && PL - Ppv - Pw <= Pgmax + eng3_Pmax + Pd1max + Pd2max + Pbat_discharge_Pmax];
    ! * -> ZeroLoad_RES_Charge : if [PL == 0 && Ppv + Pw > 0 && SoC < 0.95];
    ! * -> ZeroLoad_RES_Spare : if [PL == 0 && Ppv + Pw > 0 && SoC >= 0.95];
    ! * -> RES_Covers_Load_Charge : if [PL > 0 && Ppv + Pw >= PL && SoC < 0.95];
    ! * -> RES_Covers_Load_Spare : if [PL > 0 && Ppv + Pw >= PL && SoC >= 0.95];
    ! * -> Battery_Discharge_Priority : if [PL > 0 && Ppv + Pw < PL && SoC >= 0.20 && PL - Ppv - Pw <= Pbat_discharge_Pmax];
    ! * -> LNG_Covers_Load_LowSoC_ChargeMargin : if [PL > 0 && Ppv + Pw < PL && SoC < 0.20 && PL - Ppv - Pw + Pgmax / 5 <= Pgmax];
    ! * -> LNG_Covers_Load : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > Pbat_discharge_Pmax && PL - Ppv - Pw <= Pgmax];
    ! * -> LNG_Engine3_Covers_Load : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > Pgmax && PL - Ppv - Pw <= Pgmax + eng3_Pmax];
    ! * -> DG1_Covers_Load_LowSoC_ChargeMargin : if [PL > 0 && Ppv + Pw < PL && SoC < 0.20 && PL - Ppv - Pw > Pgmax + eng3_Pmax && PL - Ppv - Pw + Pd1max / 10 <= Pgmax + eng3_Pmax + Pd1max];
    ! * -> DG1_Covers_Load : if [PL > 0 && Ppv + Pw < PL && SoC >= 0.20 && PL - Ppv - Pw > Pgmax + eng3_Pmax && PL - Ppv - Pw <= Pgmax + eng3_Pmax + Pd1max];
    ! * -> DG2_Covers_Load_WithOptionalChargeMargin : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > Pgmax + eng3_Pmax + Pd1max && PL - Ppv - Pw <= Pgmax + eng3_Pmax + Pd1max + Pd2max];

    [*] -> ZeroLoad_RES_Charge;

    state ZeroLoad_RES_Charge {
        enter {
            Pgen_req = 0;
            PLNG_req = 0;
            PENG3_req = 0;
            PDG1_req = 0;
            PDG2_req = 0;
            Pbat_discharge = 0;
            Pbat_charge = Ppv + Pw;
            Pspare = 0;
            cutin_LNG = 0;
            cutout_LNG = 1;
            cutin_ENG3 = 0;
            cutout_ENG3 = 1;
            cutin_DG1 = 0;
            cutout_DG1 = 1;
            cutin_DG2 = 0;
            cutout_DG2 = 1;
            load_cutout = 0;
        }
    }

    state ZeroLoad_RES_Spare {
        enter {
            Pgen_req = 0;
            PLNG_req = 0;
            PENG3_req = 0;
            PDG1_req = 0;
            PDG2_req = 0;
            Pbat_discharge = 0;
            Pbat_charge = 0;
            Pspare = Ppv + Pw;
            cutin_LNG = 0;
            cutout_LNG = 1;
            cutin_ENG3 = 0;
            cutout_ENG3 = 1;
            cutin_DG1 = 0;
            cutout_DG1 = 1;
            cutin_DG2 = 0;
            cutout_DG2 = 1;
            load_cutout = 0;
        }
    }

    state RES_Covers_Load_Charge {
        enter {
            Pgen_req = 0;
            PLNG_req = 0;
            PENG3_req = 0;
            PDG1_req = 0;
            PDG2_req = 0;
            Pbat_discharge = 0;
            Pbat_charge = Ppv + Pw - PL;
            Pspare = 0;
            cutin_LNG = 0;
            cutout_LNG = 1;
            cutin_ENG3 = 0;
            cutout_ENG3 = 1;
            cutin_DG1 = 0;
            cutout_DG1 = 1;
            cutin_DG2 = 0;
            cutout_DG2 = 1;
            load_cutout = 0;
        }
    }

    state RES_Covers_Load_Spare {
        enter {
            Pgen_req = 0;
            PLNG_req = 0;
            PENG3_req = 0;
            PDG1_req = 0;
            PDG2_req = 0;
            Pbat_discharge = 0;
            Pbat_charge = 0;
            Pspare = Ppv + Pw - PL;
            cutin_LNG = 0;
            cutout_LNG = 1;
            cutin_ENG3 = 0;
            cutout_ENG3 = 1;
            cutin_DG1 = 0;
            cutout_DG1 = 1;
            cutin_DG2 = 0;
            cutout_DG2 = 1;
            load_cutout = 0;
        }
    }

    state Battery_Discharge_Priority {
        enter {
            Pgen_req = 0;
            PLNG_req = 0;
            PENG3_req = 0;
            PDG1_req = 0;
            PDG2_req = 0;
            Pbat_discharge = PL - Ppv - Pw;
            Pbat_charge = 0;
            Pspare = 0;
            cutin_LNG = 0;
            cutout_LNG = 1;
            cutin_ENG3 = 0;
            cutout_ENG3 = 1;
            cutin_DG1 = 0;
            cutout_DG1 = 1;
            cutin_DG2 = 0;
            cutout_DG2 = 1;
            load_cutout = 0;
        }
    }

    state LNG_Covers_Load {
        enter {
            Pgen_req = PL - Ppv - Pw;
            PLNG_req = PL - Ppv - Pw;
            PENG3_req = 0;
            PDG1_req = 0;
            PDG2_req = 0;
            Pbat_discharge = 0;
            Pbat_charge = 0;
            Pspare = 0;
            cutin_LNG = 1;
            cutout_LNG = 0;
            cutin_ENG3 = 0;
            cutout_ENG3 = 1;
            cutin_DG1 = 0;
            cutout_DG1 = 1;
            cutin_DG2 = 0;
            cutout_DG2 = 1;
            load_cutout = 0;
        }
    }

    state LNG_Covers_Load_LowSoC_ChargeMargin {
        enter {
            Pgen_req = PL - Ppv - Pw + Pgmax / 5;
            PLNG_req = PL - Ppv - Pw + Pgmax / 5;
            PENG3_req = 0;
            PDG1_req = 0;
            PDG2_req = 0;
            Pbat_discharge = 0;
            Pbat_charge = Pgmax / 5;
            Pspare = 0;
            cutin_LNG = 1;
            cutout_LNG = 0;
            cutin_ENG3 = 0;
            cutout_ENG3 = 1;
            cutin_DG1 = 0;
            cutout_DG1 = 1;
            cutin_DG2 = 0;
            cutout_DG2 = 1;
            load_cutout = 0;
        }
    }

    state LNG_Engine3_Covers_Load {
        enter {
            Pgen_req = PL - Ppv - Pw;
            PLNG_req = Pgmax;
            PENG3_req = PL - Ppv - Pw - Pgmax;
            PDG1_req = 0;
            PDG2_req = 0;
            Pbat_discharge = 0;
            Pbat_charge = 0;
            Pspare = 0;
            cutin_LNG = 1;
            cutout_LNG = 0;
            cutin_ENG3 = 1;
            cutout_ENG3 = 0;
            cutin_DG1 = 0;
            cutout_DG1 = 1;
            cutin_DG2 = 0;
            cutout_DG2 = 1;
            load_cutout = 0;
        }
    }

    state DG1_Covers_Load {
        enter {
            Pgen_req = PL - Ppv - Pw;
            PLNG_req = Pgmax;
            PENG3_req = eng3_Pmax;
            PDG1_req = PL - Ppv - Pw - Pgmax - eng3_Pmax;
            PDG2_req = 0;
            Pbat_discharge = 0;
            Pbat_charge = 0;
            Pspare = 0;
            cutin_LNG = 1;
            cutout_LNG = 0;
            cutin_ENG3 = 1;
            cutout_ENG3 = 0;
            cutin_DG1 = 1;
            cutout_DG1 = 0;
            cutin_DG2 = 0;
            cutout_DG2 = 1;
            load_cutout = 0;
        }
    }

    state DG1_Covers_Load_LowSoC_ChargeMargin {
        enter {
            Pgen_req = PL - Ppv - Pw + Pd1max / 10;
            PLNG_req = Pgmax;
            PENG3_req = eng3_Pmax;
            PDG1_req = PL - Ppv - Pw - Pgmax - eng3_Pmax + Pd1max / 10;
            PDG2_req = 0;
            Pbat_discharge = 0;
            Pbat_charge = Pd1max / 10;
            Pspare = 0;
            cutin_LNG = 1;
            cutout_LNG = 0;
            cutin_ENG3 = 1;
            cutout_ENG3 = 0;
            cutin_DG1 = 1;
            cutout_DG1 = 0;
            cutin_DG2 = 0;
            cutout_DG2 = 1;
            load_cutout = 0;
        }
    }

    state DG2_Covers_Load_WithOptionalChargeMargin {
        enter {
            if [SoC < 0.20] {
                Pgen_req = PL - Ppv - Pw + Pd1max / 10;
                PLNG_req = Pgmax;
                PENG3_req = eng3_Pmax;
                PDG1_req = Pd1max;
                PDG2_req = PL - Ppv - Pw - Pgmax - eng3_Pmax - Pd1max + Pd1max / 10;
                Pbat_charge = Pd1max / 10;
            } else {
                Pgen_req = PL - Ppv - Pw;
                PLNG_req = Pgmax;
                PENG3_req = eng3_Pmax;
                PDG1_req = Pd1max;
                PDG2_req = PL - Ppv - Pw - Pgmax - eng3_Pmax - Pd1max;
                Pbat_charge = 0;
            }
            Pbat_discharge = 0;
            Pspare = 0;
            cutin_LNG = 1;
            cutout_LNG = 0;
            cutin_ENG3 = 1;
            cutout_ENG3 = 0;
            cutin_DG1 = 1;
            cutout_DG1 = 0;
            cutin_DG2 = 1;
            cutout_DG2 = 0;
            load_cutout = 0;
        }
    }

    state IllegalOverloadCompletion {
        enter {
... <truncated 589 chars; see run record>
```

#### Candidate diff（before -> candidate）

```diff
--- before.fcstm
+++ candidate.fcstm
@@ -26,7 +26,7 @@
 def int load_cutout = 0;
 
 state LNGShipEMS {
-    ! * -> IllegalOverloadCompletion : if [PL - Ppv - Pw > Pgmax + eng3_Pmax + Pd1max + Pd2max + Pbat_discharge_Pmax];
+    ! * -> IllegalOverloadCompletion : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > Pgmax + eng3_Pmax + Pd1max + Pd2max && PL - Ppv - Pw <= Pgmax + eng3_Pmax + Pd1max + Pd2max + Pbat_discharge_Pmax];
     ! * -> ZeroLoad_RES_Charge : if [PL == 0 && Ppv + Pw > 0 && SoC < 0.95];
     ! * -> ZeroLoad_RES_Spare : if [PL == 0 && Ppv + Pw > 0 && SoC >= 0.95];
     ! * -> RES_Covers_Load_Charge : if [PL > 0 && Ppv + Pw >= PL && SoC < 0.95];
```

#### SL-10 审查结果

- SL-10 decision=`rework`，ok=`False`，target_resolved=`True`，regression_detected=`False`，drift_risk=`minor`。
- SL-10 review_meta：schema=`SL10RepairReviewOutput.v1`，failure_policy=`fail_closed`，replay_key=`SL-10:sha256:9e59928c9b033bbc77538c648da989d31b186fd6c65064395a2aab573ae7678c`。
  - SL-10 evidence 1: `{"summary": "The current SL-9 candidate changes only the IllegalOverloadCompletion forced-transition guard. The old guard selected IllegalOverloadCompletion only when deficit = PL - Ppv - Pw exceeded Pgmax + eng3_Pmax + Pd1max + Pd2max + Pbat_discharge_Pmax, while the enter action assigned Pbat_discharge = deficit - thermal. That necessarily made Pbat_discharge greater than Pbat_discharge_Pmax. The candidate guard now selects the interval deficit > Pgmax + eng3_Pmax + Pd1max + Pd2max and deficit <= Pgmax + eng3_Pmax + Pd1max + Pd2max + Pbat_discharge_Pmax, so the assigned battery discharge is positive and bounded by the declared battery discharge capacity."}`
  - SL-10 evidence 2: `{"summary": "This resolves fixreq-2-sl7-0, fixreq-2-sl7-1, and fixreq-2-sl7-2: the unsafe over-capacity battery-discharge selection is removed; the NL-described thermal-exceeded, battery-coverable overload completion interval is now represented; and the prior gap between total thermal capacity and total thermal plus battery discharge capacity is closed."}`
  - SL-10 evidence 3: `{"summary": "This also resolves fixreq-2-sl7-3 at the model-behavior level. A scenario at the previously missing critical boundary, for example deficit = thermal + Pbat_discharge_Pmax, would now enter IllegalOverloadCompletion, request all thermal units, set Pbat_discharge to the remaining lack within Pbat_discharge_Pmax, set Pbat_charge and Pspare to 0, cut in LNG/ENG3/DG1/DG2, and assert load_cutout."}`
  - SL-10 evidence 4: `{"summary": "The DSL diff does not drop NL-required states, variables, outputs, or command obligations. The twelve dispatch states remain present, including ZeroLoad_RES_Charge, ZeroLoad_RES_Spare, RES charge/spare states, Battery_Discharge_Priority, LNG states, DG1/DG2 late-priority states, and IllegalOverloadCompletion. Required input variables PL, Ppv, Pw, SoC, eng3_Pmax, Pgmax, Pd1max and dispatch outputs Pgen_req, Pbat_discharge, Pbat_charge, Pspare are preserved, along with generator-specific cut-in/cut-out commands and load_cutout."}`
  - SL-10 evidence 5: `{"summary": "The prior FixLog repair_memory objections about unwritten external inputs remain waived for the same NL-grounded reason: PL, Ppv, Pw, SoC, Pgmax, eng3_Pmax, Pd1max, Pd2max, and Pbat_discharge_Pmax are read measurements or capacity bounds used to classify changing operating conditions, and the NL provides no internal FSM update law for them. The current candidate does not attempt the forbidden edit of inventing plant/environment dynamics."}`
- SL-10 rework_instructions：SL-10 pass was downgraded because local deterministic evidence reported major drift and SL-10 evidence did not explicitly address the local rejection reason/kind with a structured local_override_rationale.；For the next SL-9 repair, do not blindly regenerate the same DSL. Either change the candidate so the local major-drift evidence is resolved, or keep the minimal DSL only with explicit repair_rationale mapping each local objection (for example missing_required_grounding, scenario_regression, count_drift, or forced_transition_count_drift) to concrete NL-ground...<truncated 152 chars>
- local checks evidence：stage=`SD-10`；note=PR-E1 uses local parse/semantic/design/sim checks as SL-10 evidence, not as the final deterministic judge.。
  - local ok=`False`，target_resolved=`False`，regression_detected=`True`，drift_risk=`major`。
  - local_rejection：reason=`scenario_regression; missing_required_grounding`，rejected_by_stage=`SD-10`。
    - local evidence 1: `scenario_regression` {"kind": "scenario_regression", "sim_feedback": {"n_scenarios": 15, "n_scenarios_passed": 13, "ok": false, "oracle_weak": false, "scenario_results": [{"description": "default-init: after the first empty cycle, PL=0 with RES available and SoC below 0.95 selects zero-load battery charging and cuts out thermal units.", "name": "default_init_zero_load_res_charge", "setup_error": null, "status": "pass", "step_results": [{"actual_state": "LNGShipEMS.ZeroLoad_RES_Charge", "actual_vars": {"PDG1_req": 0,...<truncated 15270 chars>
    - local evidence 2: `missing_required_grounding` {"element_ids": ["transition:classify_zero_load", "transition:classify_dg_late_priority"], "kind": "missing_required_grounding"}

</details>

<details><summary>Repair 4 / iteration `2` / source `SL-7` / accepted=✅</summary>

#### 为什么进入修复

- selected feedback source：`SL-7`；blocking=`True`；pre_scenario=`False`。
- problem_summary：model review failed
- diagnostic ids：`0, 1, 2, 3`。
- before_dsl_hash：`sha256:ae74dfc8a541f448b34f805ad6dbf46262a2b2b804509e2e7866abecbe67c8aa`；candidate_dsl_hash：`sha256:27ff012eeca8958395886399d5f506d668adb07be506c45860ce7acb776355e5`。

#### 错误证据 / diagnostics

- 1. `<unknown>` `` policy=``：The illegal overload branch requests battery discharge beyond the declared battery discharge capacity.
- 2. `<unknown>` `` policy=``：The illegal overload transition does not match the NL condition of demand exceeding all RES and thermal resources and then using battery discharge to cover the lack.
- 3. `<unknown>` `` policy=``：The model leaves the thermal-exceeded but battery-coverable deficit interval without an explicit NL-grounded transition.
- 4. `<unknown>` `` policy=``：The simulation oracle misses the critical overload boundary and therefore gives a false sense of coverage.

#### SD-8 FixRequestBatch / 修改请求

- batch_id：`fixbatch-2-sha256-2baadc6ec74`；source_stage=`SL-7`；legacy_plan_kind=`FixPlan`；requests=`4`。

| request_id | severity | hard | waiver | problem | evidence |
|---|---|---:|---:|---|---|
| `fixreq-2-sl7-0-e56a9044a1` | `review_fail` | ✅ | ❌ | model review failed | `{'category': 'unsafe_recovery', 'evidence': ['Guard: PL - Ppv - Pw > Pgmax + eng3_Pmax + Pd1max + Pd2max + Pbat_discharge_Pmax.', 'Action: Pbat_discharge = PL - Ppv - Pw - Pgmax - eng3_Pmax - Pd1max - Pd2max.', 'Therefore selected IllegalOverloadCompletion always assigns Pbat_discharge > Pbat_discharge_Pmax.'], 'severity': 'major', 'summary': 'The illegal overload branch requests battery discharge beyond the declared battery discharge capacity.'}` |
| `fixreq-2-sl7-1-ef61a52a60` | `review_fail` | ✅ | ❌ | model review failed | `{'category': 'nl_fidelity', 'evidence': ['NL describes overload completion when extreme demand exceeds RES and thermal resources.', 'DSL only enters IllegalOverloadCompletion when demand exceeds RES, thermal resources, and battery discharge capacity.', 'The NL-described thermal-exceeded but battery-coverable region is not represented.'], 'severity': 'major', 'summary': 'The illegal overload transition does not match the NL condition of demand exceeding all RES and thermal resources and then using battery discharge to cover the lack.'}` |
| `fixreq-2-sl7-2-86839a6bcb` | `review_fail` | ✅ | ❌ | model review failed | `{'category': 'coverage_gap', 'evidence': ['DG2 guard ends at deficit <= Pgmax + eng3_Pmax + Pd1max + Pd2max.', 'Illegal overload guard begins only at deficit > Pgmax + eng3_Pmax + Pd1max + Pd2max + Pbat_discharge_Pmax.', 'No transition covers the interval between those bounds.'], 'severity': 'major', 'summary': 'The model leaves the thermal-exceeded but battery-coverable deficit interval without an explicit NL-grounded transition.'}` |
| `fixreq-2-sl7-3-4a91513941` | `review_fail` | ✅ | ❌ | model review failed | `{'category': 'path1_eval_risk', 'evidence': ['sim_summary reports all 15 scenarios passed.', 'The illegal overload scenario only tests demand beyond thermal plus battery capacity.', 'No shown scenario tests demand beyond thermal capacity but within battery discharge capacity.'], 'severity': 'major', 'summary': 'The simulation oracle misses the critical overload boundary and therefore gives a false sense of coverage.'}` |

#### SD-8 legacy fix plan / 修改建议

- recommended_strategy：Use diagnostics as hints; choose the smallest globally consistent repair.；Before returning a candidate, verify every required_preserve_element_id still has a concrete DSL representation.
- forbidden_edits：`Do not delete grounded required elements merely to silence diagnostics., Do not invent internal plant/environment dynamics merely to make external input variables appear written.`。
- required_preserve_element_ids：`state:LNGShipEMS, variable:PL, variable:Ppv, variable:Pw, variable:SoC, variable:eng3_Pmax, variable:Pgmax, variable:Pd1max, variable:Pgen_req, variable:Pbat_discharge, variable:Pbat_charge, variable:Pspare, ... +25`。

#### SL-9 per-request 决策

- accepted_request_ids：`<derived-from-table>`；candidate_len=`9484`。

| request_id | decision | waiver | rework_locked | rationale / intent |
|---|---|---:|---:|---|
| `fixreq-2-sl7-0-e56a9044a1` | `accept` | ❌ | ✅ | Accepted as rework-locked and still actionable. The original guard made IllegalOverloadCompletion fire only beyond thermal plus battery capacity, so every selected case over-discharged relative to Pbat_discharge_Pmax. The repair changes the overload classifier to the NL-grounded condition that demand deficit exceeds all RES and thermal generation. This remov...<truncated 243 chars> |
| `fixreq-2-sl7-1-ef61a52a60` | `accept` | ❌ | ✅ | The NL says the overload completion condition is demand exceeding RES and thermal resources, with the remaining lack covered by battery discharge. The repaired guard now matches that threshold directly instead of waiting until the deficit exceeds thermal plus battery discharge capacity.；intent=Represent the NL-described thermal-exceeded overload branch expli...<truncated 5 chars> |
| `fixreq-2-sl7-2-86839a6bcb` | `accept` | ❌ | ✅ | The prior model left the interval immediately above total thermal capacity without an explicit overload transition. The repaired wildcard guard covers deficit > Pgmax + eng3_Pmax + Pd1max + Pd2max, closing the thermal-exceeded interval while leaving DG2 dispatch up to the thermal bound unchanged.；intent=Close the coverage gap between total thermal capacity a...<truncated 22 chars> |
| `fixreq-2-sl7-3-4a91513941` | `accept` | ❌ | ✅ | The behavioral defect behind the oracle risk is repaired in the DSL. The local failing scenarios illegal_overload_activates_all_thermal_and_battery and forced_reclassification_from_zero_load_to_illegal both use PL=50, Ppv=0, Pw=0, Pgmax=10, eng3_Pmax=5, Pd1max=10, Pd2max=10, so deficit=50 and thermal=35. The repaired guard is true, entering IllegalOverloadCo...<truncated 261 chars> |
- repair_rationale：Smallest DSL edit: only the first wildcard guard was changed from deficit > thermal + Pbat_discharge_Pmax to deficit > thermal. All variables, all twelve dispatch states, and all enter actions are preserved.；The scenario_regression_repair_brief is addressed. For illegal_overload_activates_all_thermal_and_battery, initial deficit is 50 and thermal capacity is 35, so the repaired guard enters LNGShipEMS.IllegalOverloadCompletion from DG2_Covers_L...<truncated 176 chars>；For forced_reclassification_from_zero_load_to_illegal, the same repaired wildcard forced guard is true from ZeroLoad_RES_Charge, so the model no longer remains in the benign zero-load state under extreme overload variables.；Previously passing scenarios are not regressed because their deficits are either RES/zero-load cases or within battery/LNG/ENG3/DG1/DG2 thermal dispatch bounds. The repaired guard only preempts cases where PL - Ppv - Pw exceeds Pgmax + eng3...<truncated 24 chars>；transition:classify_zero_load remains concretely represented by the two wildcard forced transitions to ZeroLoad_RES_Charge and ZeroLoad_RES_Spare, plus the root initial transition to ZeroLoad_RES_Charge for default zero-load initialization.
- diff_summary：`{"summary": "Changed only the IllegalOverloadCompletion forced-transition guard so overload completion is selected whenever the net demand deficit exceeds total thermal capacity. This closes the thermal-exceeded coverage gap and fixes the local overload reclassification failures while preserving all required states, variables, dispatch outputs, zero-load/RES classifiers, DG late-priority classifiers, and command actions."}`。

#### SL-9 candidate / 最终修改执行方案

```pyfcstm
def float PL = 0.0;
def float Ppv = 0.0;
def float Pw = 0.0;
def float SoC = 0.50;
def float Pgmax = 0.0;
def float eng3_Pmax = 0.0;
def float Pd1max = 0.0;
def float Pd2max = 0.0;
def float Pbat_discharge_Pmax = 0.0;
def float Pgen_req = 0.0;
def float PLNG_req = 0.0;
def float PENG3_req = 0.0;
def float PDG1_req = 0.0;
def float PDG2_req = 0.0;
def float Pbat_discharge = 0.0;
def float Pbat_charge = 0.0;
def float Pspare = 0.0;
def int cutin_LNG = 0;
def int cutout_LNG = 0;
def int cutin_ENG3 = 0;
def int cutout_ENG3 = 0;
def int cutin_DG1 = 0;
def int cutout_DG1 = 0;
def int cutin_DG2 = 0;
def int cutout_DG2 = 0;
def int load_cutout = 0;

state LNGShipEMS {
    ! * -> IllegalOverloadCompletion : if [PL - Ppv - Pw > Pgmax + eng3_Pmax + Pd1max + Pd2max];
    ! * -> ZeroLoad_RES_Charge : if [PL == 0 && Ppv + Pw > 0 && SoC < 0.95];
    ! * -> ZeroLoad_RES_Spare : if [PL == 0 && Ppv + Pw > 0 && SoC >= 0.95];
    ! * -> RES_Covers_Load_Charge : if [PL > 0 && Ppv + Pw >= PL && SoC < 0.95];
    ! * -> RES_Covers_Load_Spare : if [PL > 0 && Ppv + Pw >= PL && SoC >= 0.95];
    ! * -> Battery_Discharge_Priority : if [PL > 0 && Ppv + Pw < PL && SoC >= 0.20 && PL - Ppv - Pw <= Pbat_discharge_Pmax];
    ! * -> LNG_Covers_Load_LowSoC_ChargeMargin : if [PL > 0 && Ppv + Pw < PL && SoC < 0.20 && PL - Ppv - Pw + Pgmax / 5 <= Pgmax];
    ! * -> LNG_Covers_Load : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > Pbat_discharge_Pmax && PL - Ppv - Pw <= Pgmax];
    ! * -> LNG_Engine3_Covers_Load : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > Pgmax && PL - Ppv - Pw <= Pgmax + eng3_Pmax];
    ! * -> DG1_Covers_Load_LowSoC_ChargeMargin : if [PL > 0 && Ppv + Pw < PL && SoC < 0.20 && PL - Ppv - Pw > Pgmax + eng3_Pmax && PL - Ppv - Pw + Pd1max / 10 <= Pgmax + eng3_Pmax + Pd1max];
    ! * -> DG1_Covers_Load : if [PL > 0 && Ppv + Pw < PL && SoC >= 0.20 && PL - Ppv - Pw > Pgmax + eng3_Pmax && PL - Ppv - Pw <= Pgmax + eng3_Pmax + Pd1max];
    ! * -> DG2_Covers_Load_WithOptionalChargeMargin : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > Pgmax + eng3_Pmax + Pd1max && PL - Ppv - Pw <= Pgmax + eng3_Pmax + Pd1max + Pd2max];

    [*] -> ZeroLoad_RES_Charge;

    state ZeroLoad_RES_Charge {
        enter {
            Pgen_req = 0;
            PLNG_req = 0;
            PENG3_req = 0;
            PDG1_req = 0;
            PDG2_req = 0;
            Pbat_discharge = 0;
            Pbat_charge = Ppv + Pw;
            Pspare = 0;
            cutin_LNG = 0;
            cutout_LNG = 1;
            cutin_ENG3 = 0;
            cutout_ENG3 = 1;
            cutin_DG1 = 0;
            cutout_DG1 = 1;
            cutin_DG2 = 0;
            cutout_DG2 = 1;
            load_cutout = 0;
        }
    }

    state ZeroLoad_RES_Spare {
        enter {
            Pgen_req = 0;
            PLNG_req = 0;
            PENG3_req = 0;
            PDG1_req = 0;
            PDG2_req = 0;
            Pbat_discharge = 0;
            Pbat_charge = 0;
            Pspare = Ppv + Pw;
            cutin_LNG = 0;
            cutout_LNG = 1;
            cutin_ENG3 = 0;
            cutout_ENG3 = 1;
            cutin_DG1 = 0;
            cutout_DG1 = 1;
            cutin_DG2 = 0;
            cutout_DG2 = 1;
            load_cutout = 0;
        }
    }

    state RES_Covers_Load_Charge {
        enter {
            Pgen_req = 0;
            PLNG_req = 0;
            PENG3_req = 0;
            PDG1_req = 0;
            PDG2_req = 0;
            Pbat_discharge = 0;
            Pbat_charge = Ppv + Pw - PL;
            Pspare = 0;
            cutin_LNG = 0;
            cutout_LNG = 1;
            cutin_ENG3 = 0;
            cutout_ENG3 = 1;
            cutin_DG1 = 0;
            cutout_DG1 = 1;
            cutin_DG2 = 0;
            cutout_DG2 = 1;
            load_cutout = 0;
        }
    }

    state RES_Covers_Load_Spare {
        enter {
            Pgen_req = 0;
            PLNG_req = 0;
            PENG3_req = 0;
            PDG1_req = 0;
            PDG2_req = 0;
            Pbat_discharge = 0;
            Pbat_charge = 0;
            Pspare = Ppv + Pw - PL;
            cutin_LNG = 0;
            cutout_LNG = 1;
            cutin_ENG3 = 0;
            cutout_ENG3 = 1;
            cutin_DG1 = 0;
            cutout_DG1 = 1;
            cutin_DG2 = 0;
            cutout_DG2 = 1;
            load_cutout = 0;
        }
    }

    state Battery_Discharge_Priority {
        enter {
            Pgen_req = 0;
            PLNG_req = 0;
            PENG3_req = 0;
            PDG1_req = 0;
            PDG2_req = 0;
            Pbat_discharge = PL - Ppv - Pw;
            Pbat_charge = 0;
            Pspare = 0;
            cutin_LNG = 0;
            cutout_LNG = 1;
            cutin_ENG3 = 0;
            cutout_ENG3 = 1;
            cutin_DG1 = 0;
            cutout_DG1 = 1;
            cutin_DG2 = 0;
            cutout_DG2 = 1;
            load_cutout = 0;
        }
    }

    state LNG_Covers_Load {
        enter {
            Pgen_req = PL - Ppv - Pw;
            PLNG_req = PL - Ppv - Pw;
            PENG3_req = 0;
            PDG1_req = 0;
            PDG2_req = 0;
            Pbat_discharge = 0;
            Pbat_charge = 0;
            Pspare = 0;
            cutin_LNG = 1;
            cutout_LNG = 0;
            cutin_ENG3 = 0;
            cutout_ENG3 = 1;
            cutin_DG1 = 0;
            cutout_DG1 = 1;
            cutin_DG2 = 0;
            cutout_DG2 = 1;
            load_cutout = 0;
        }
    }

    state LNG_Covers_Load_LowSoC_ChargeMargin {
        enter {
            Pgen_req = PL - Ppv - Pw + Pgmax / 5;
            PLNG_req = PL - Ppv - Pw + Pgmax / 5;
            PENG3_req = 0;
            PDG1_req = 0;
            PDG2_req = 0;
            Pbat_discharge = 0;
            Pbat_charge = Pgmax / 5;
            Pspare = 0;
            cutin_LNG = 1;
            cutout_LNG = 0;
            cutin_ENG3 = 0;
            cutout_ENG3 = 1;
            cutin_DG1 = 0;
            cutout_DG1 = 1;
            cutin_DG2 = 0;
            cutout_DG2 = 1;
            load_cutout = 0;
        }
    }

    state LNG_Engine3_Covers_Load {
        enter {
            Pgen_req = PL - Ppv - Pw;
            PLNG_req = Pgmax;
            PENG3_req = PL - Ppv - Pw - Pgmax;
            PDG1_req = 0;
            PDG2_req = 0;
            Pbat_discharge = 0;
            Pbat_charge = 0;
            Pspare = 0;
            cutin_LNG = 1;
            cutout_LNG = 0;
            cutin_ENG3 = 1;
            cutout_ENG3 = 0;
            cutin_DG1 = 0;
            cutout_DG1 = 1;
            cutin_DG2 = 0;
            cutout_DG2 = 1;
            load_cutout = 0;
        }
    }

    state DG1_Covers_Load {
        enter {
            Pgen_req = PL - Ppv - Pw;
            PLNG_req = Pgmax;
            PENG3_req = eng3_Pmax;
            PDG1_req = PL - Ppv - Pw - Pgmax - eng3_Pmax;
            PDG2_req = 0;
            Pbat_discharge = 0;
            Pbat_charge = 0;
            Pspare = 0;
            cutin_LNG = 1;
            cutout_LNG = 0;
            cutin_ENG3 = 1;
            cutout_ENG3 = 0;
            cutin_DG1 = 1;
            cutout_DG1 = 0;
            cutin_DG2 = 0;
            cutout_DG2 = 1;
            load_cutout = 0;
        }
    }

    state DG1_Covers_Load_LowSoC_ChargeMargin {
        enter {
            Pgen_req = PL - Ppv - Pw + Pd1max / 10;
            PLNG_req = Pgmax;
            PENG3_req = eng3_Pmax;
            PDG1_req = PL - Ppv - Pw - Pgmax - eng3_Pmax + Pd1max / 10;
            PDG2_req = 0;
            Pbat_discharge = 0;
            Pbat_charge = Pd1max / 10;
            Pspare = 0;
            cutin_LNG = 1;
            cutout_LNG = 0;
            cutin_ENG3 = 1;
            cutout_ENG3 = 0;
            cutin_DG1 = 1;
            cutout_DG1 = 0;
            cutin_DG2 = 0;
            cutout_DG2 = 1;
            load_cutout = 0;
        }
    }

    state DG2_Covers_Load_WithOptionalChargeMargin {
        enter {
            if [SoC < 0.20] {
                Pgen_req = PL - Ppv - Pw + Pd1max / 10;
                PLNG_req = Pgmax;
                PENG3_req = eng3_Pmax;
                PDG1_req = Pd1max;
                PDG2_req = PL - Ppv - Pw - Pgmax - eng3_Pmax - Pd1max + Pd1max / 10;
                Pbat_charge = Pd1max / 10;
            } else {
                Pgen_req = PL - Ppv - Pw;
                PLNG_req = Pgmax;
                PENG3_req = eng3_Pmax;
                PDG1_req = Pd1max;
                PDG2_req = PL - Ppv - Pw - Pgmax - eng3_Pmax - Pd1max;
                Pbat_charge = 0;
            }
            Pbat_discharge = 0;
            Pspare = 0;
            cutin_LNG = 1;
            cutout_LNG = 0;
            cutin_ENG3 = 1;
            cutout_ENG3 = 0;
            cutin_DG1 = 1;
            cutout_DG1 = 0;
            cutin_DG2 = 1;
            cutout_DG2 = 0;
            load_cutout = 0;
        }
    }

    state IllegalOverloadCompletion {
        enter {
            Pgen_req = Pgmax + eng3_Pmax + Pd1max + Pd2max;
            PLNG_req = Pgmax;
            PENG
... <truncated 484 chars; see run record>
```

#### Candidate diff（before -> candidate）

```diff
--- before.fcstm
+++ candidate.fcstm
@@ -26,7 +26,7 @@
 def int load_cutout = 0;
 
 state LNGShipEMS {
-    ! * -> IllegalOverloadCompletion : if [PL - Ppv - Pw > Pgmax + eng3_Pmax + Pd1max + Pd2max + Pbat_discharge_Pmax];
+    ! * -> IllegalOverloadCompletion : if [PL - Ppv - Pw > Pgmax + eng3_Pmax + Pd1max + Pd2max];
     ! * -> ZeroLoad_RES_Charge : if [PL == 0 && Ppv + Pw > 0 && SoC < 0.95];
     ! * -> ZeroLoad_RES_Spare : if [PL == 0 && Ppv + Pw > 0 && SoC >= 0.95];
     ! * -> RES_Covers_Load_Charge : if [PL > 0 && Ppv + Pw >= PL && SoC < 0.95];
```

#### SL-10 审查结果

- SL-10 decision=`pass`，ok=`True`，target_resolved=`True`，regression_detected=`False`，drift_risk=`minor`。
- SL-10 review_meta：schema=`SL10RepairReviewOutput.v1`，failure_policy=`fail_closed`，replay_key=`SL-10:sha256:f1392caef5f67b5a66920d7c2c0392a126143496c5f286e899589cbd9fba6453`。
  - SL-10 evidence 1: `{"summary": "The NL defines IllegalOverloadCompletion for the condition where the net demand deficit exceeds all RES and thermal resources, with all thermal generating units activated and the remaining lack covered by battery discharge. The candidate changes only the IllegalOverloadCompletion wildcard guard from deficit > thermal + Pbat_discharge_Pmax to deficit > thermal, which directly matches that NL condition."}`
  - SL-10 evidence 2: `{"summary": "The SL-9 rework decisions explicitly accept all four rework-locked requests and address the previous local scenario regression. For PL=50, Ppv=0, Pw=0, Pgmax=10, eng3_Pmax=5, Pd1max=10, Pd2max=10, the repaired guard is true because deficit=50 and thermal=35; IllegalOverloadCompletion then requests Pgen_req=35, PLNG_req=10, PENG3_req=5, PDG1_req=10, PDG2_req=10, Pbat_discharge=15, Pbat_charge=0, Pspare=0, cutin commands asserted, and load_cutout=1, matching the repair-memory scenario obligation."}`
  - SL-10 evidence 3: `{"summary": "The candidate resolves the original SL-7 fidelity and coverage findings by closing the missing thermal-exceeded interval. DG2 remains bounded by deficit <= Pgmax + eng3_Pmax + Pd1max + Pd2max, while IllegalOverloadCompletion now begins immediately above that thermal bound, so there is no unrepresented interval between DG2 dispatch and overload completion."}`
  - SL-10 evidence 4: `{"summary": "The DSL diff is minimal and does not drop NL-required structure. All twelve states remain present, including ZeroLoad_RES_Charge, ZeroLoad_RES_Spare, RES_Covers_Load_Charge, RES_Covers_Load_Spare, Battery_Discharge_Priority, LNG_Covers_Load, LNG_Covers_Load_LowSoC_ChargeMargin, LNG_Engine3_Covers_Load, DG1_Covers_Load, DG1_Covers_Load_LowSoC_ChargeMargin, DG2_Covers_Load_WithOptionalChargeMargin, and IllegalOverloadCompletion. Required input variables, dispatch outputs, generator request outputs, cut-in/cut-out commands, and load_cutout are preserved."}`
  - SL-10 evidence 5: `{"summary": "The previously waived external-input warnings remain appropriately waived under the NL: PL, Ppv, Pw, SoC, Pgmax, eng3_Pmax, Pd1max, Pd2max, and Pbat_discharge_Pmax are read measurements or capacity bounds used by the EMS classifier, and the NL does not provide internal FSM update laws for them. The candidate does not introduce forbidden plant/environment dynamics."}`
  - SL-10 evidence 6: `{"summary": "Local deterministic evidence no longer reports the prior scenario_regression; it reports only missing_required_grounding for transition:classify_zero_load and transition:classify_dg_late_priority. SL-9's repair notes map those abstract grounding IDs to concrete wildcard transitions and state actions retained in the candidate."}`
- local checks evidence：stage=`SD-10`；note=PR-E1 uses local parse/semantic/design/sim checks as SL-10 evidence, not as the final deterministic judge.。
  - local ok=`False`，target_resolved=`False`，regression_detected=`False`，drift_risk=`major`。
  - local_rejection：reason=`missing_required_grounding`，rejected_by_stage=`SD-10`。
    - local evidence 1: `missing_required_grounding` {"element_ids": ["transition:classify_zero_load", "transition:classify_dg_late_priority"], "kind": "missing_required_grounding"}

</details>

<details><summary>Repair 5 / iteration `3` / source `SL-7` / accepted=✅</summary>

#### 为什么进入修复

- selected feedback source：`SL-7`；blocking=`True`；pre_scenario=`False`。
- problem_summary：model review failed
- diagnostic ids：`0, 1`。
- before_dsl_hash：`sha256:27ff012eeca8958395886399d5f506d668adb07be506c45860ce7acb776355e5`；candidate_dsl_hash：`sha256:4b52356070e7a51d779df874526281152b5fb3e1dac5b2f71a14dc2af9ccf364`。

#### 错误证据 / diagnostics

- 1. `<unknown>` `` policy=``：The guard partition is incomplete for important operating regions, so the EMS can fail to switch to an NL-grounded power-balance state.
- 2. `<unknown>` `` policy=``：When no guard fires, the FSM has no safe default and may retain stale dispatch and cut-in/cut-out commands.

#### SD-8 FixRequestBatch / 修改请求

- batch_id：`fixbatch-3-sha256-b2c527b44d2`；source_stage=`SL-7`；legacy_plan_kind=`FixPlan`；requests=`2`。

| request_id | severity | hard | waiver | problem | evidence |
|---|---|---:|---:|---|---|
| `fixreq-3-sl7-0-65d2e7f559` | `review_fail` | ✅ | ❌ | model review failed | `{'category': 'coverage_gap', 'evidence': ['PL == 0 && Ppv + Pw == 0 has no explicit hot-running wildcard transition.', 'Low-SoC LNG-coverable deficits can be uncovered when the Pgmax/5 margin does not fit and the deficit is not greater than Pbat_discharge_Pmax.', 'Low-SoC DG1-range deficits can be uncovered when the Pd1max/10 margin does not fit.', 'The NL requires dynamic switching to maintain power balance as resources and demands vary.'], 'severity': 'major', 'summary': 'The guard partition is incomplete for important operating regions, so the EMS can fail to switch to an NL-grounded power-balance state.'}` |
| `fixreq-3-sl7-1-ca4f711799` | `review_fail` | ✅ | ❌ | model review failed | `{'category': 'unsafe_recovery', 'evidence': ['The DSL has no else/default recovery transition for unclassified regions.', 'Prior state outputs can persist after external PL/Ppv/Pw/SoC/capacity changes if no wildcard guard is satisfied.', 'Stale generator, battery, spare-power, or load-cutout commands are unsafe for the EMS power-balance intent.'], 'severity': 'major', 'summary': 'When no guard fires, the FSM has no safe default and may retain stale dispatch and cut-in/cut-out commands.'}` |

#### SD-8 legacy fix plan / 修改建议

- recommended_strategy：Use diagnostics as hints; choose the smallest globally consistent repair.；Before returning a candidate, verify every required_preserve_element_id still has a concrete DSL representation.
- forbidden_edits：`Do not delete grounded required elements merely to silence diagnostics., Do not invent internal plant/environment dynamics merely to make external input variables appear written.`。
- required_preserve_element_ids：`state:LNGShipEMS, variable:PL, variable:Ppv, variable:Pw, variable:SoC, variable:eng3_Pmax, variable:Pgmax, variable:Pd1max, variable:Pgen_req, variable:Pbat_discharge, variable:Pbat_charge, variable:Pspare, ... +25`。

#### SL-9 per-request 决策

- accepted_request_ids：`<derived-from-table>`；candidate_len=`9548`。

| request_id | decision | waiver | rework_locked | rationale / intent |
|---|---|---:|---:|---|
| `fixreq-3-sl7-0-65d2e7f559` | `accept` | ❌ | ❌ | Accepted. The review identifies concrete uncovered classifier regions: PL == 0 with no RES, low-SoC LNG-coverable deficits when the Pgmax/5 charge margin does not fit, and low-SoC DG1-range deficits when the Pd1max/10 margin does not fit. The smallest NL-grounded repair is to complete those guard regions using existing dispatch states and actions rather than...<truncated 398 chars> |
| `fixreq-3-sl7-1-ca4f711799` | `accept` | ❌ | ❌ | Accepted. The stale-output risk is addressed by completing the NL-grounded guard partition for the identified unclassified operating regions. This preserves the wildcard reclassification design so changing external PL/Ppv/Pw/SoC/capacity inputs cause a transition into a state whose enter action rewrites dispatch, battery, spare-power, cut-in/cut-out, and loa...<truncated 159 chars> |
- repair_rationale：The current batch targets model-review coverage and stale-output safety, not the previously waived external-input warnings. PL, Ppv, Pw, SoC, Pgmax, eng3_Pmax, Pd1max, Pd2max, and Pbat_discharge_Pmax remain external measurements/capacity bo...<truncated 38 chars>；For PL == 0 && Ppv + Pw == 0, the added wildcard transition to ZeroLoad_RES_Spare gives a hot-running zero-output reclassification. Its enter action sets generator requests, battery discharge/charge, and spare power to zero and cuts out the...<truncated 57 chars>；For low-SoC LNG-coverable deficits where Pgmax/5 charging margin does not fit, the broadened LNG_Covers_Load guard now catches the fallback case when the deficit is within Pgmax. The existing low-SoC charge-margin guard remains earlier in t...<truncated 74 chars>；For low-SoC DG1-range deficits where Pd1max/10 charging margin does not fit, the broadened DG1_Covers_Load guard now catches the fallback case when the deficit is within Pgmax + eng3_Pmax + Pd1max. The existing DG1 low-SoC margin guard rema...<truncated 58 chars>；Previously passing scenarios are preserved: RES charge/spare, battery priority at SoC 0.20, LNG margin, LNG normal, Engine3, DG1 margin, DG1 normal, DG2 optional margin, and IllegalOverloadCompletion thresholds keep their states and enter a...<truncated 103 chars>
- diff_summary：`{"summary": "Added one zero-load/no-RES wildcard guard and broadened two fallback guards: LNG_Covers_Load now covers low-SoC LNG-feasible cases when the Pgmax/5 margin does not fit, and DG1_Covers_Load now covers low-SoC DG1-feasible cases when the Pd1max/10 margin does not fit. No variables, required states, dispatch actions, zero-load/RES classifiers, DG late-priority classifiers, or illegal overload behavior were removed."}`。

#### SL-9 candidate / 最终修改执行方案

```pyfcstm
def float PL = 0.0;
def float Ppv = 0.0;
def float Pw = 0.0;
def float SoC = 0.50;
def float Pgmax = 0.0;
def float eng3_Pmax = 0.0;
def float Pd1max = 0.0;
def float Pd2max = 0.0;
def float Pbat_discharge_Pmax = 0.0;
def float Pgen_req = 0.0;
def float PLNG_req = 0.0;
def float PENG3_req = 0.0;
def float PDG1_req = 0.0;
def float PDG2_req = 0.0;
def float Pbat_discharge = 0.0;
def float Pbat_charge = 0.0;
def float Pspare = 0.0;
def int cutin_LNG = 0;
def int cutout_LNG = 0;
def int cutin_ENG3 = 0;
def int cutout_ENG3 = 0;
def int cutin_DG1 = 0;
def int cutout_DG1 = 0;
def int cutin_DG2 = 0;
def int cutout_DG2 = 0;
def int load_cutout = 0;

state LNGShipEMS {
    ! * -> IllegalOverloadCompletion : if [PL - Ppv - Pw > Pgmax + eng3_Pmax + Pd1max + Pd2max];
    ! * -> ZeroLoad_RES_Charge : if [PL == 0 && Ppv + Pw > 0 && SoC < 0.95];
    ! * -> ZeroLoad_RES_Spare : if [PL == 0 && Ppv + Pw > 0 && SoC >= 0.95];
    ! * -> ZeroLoad_RES_Spare : if [PL == 0 && Ppv + Pw <= 0];
    ! * -> RES_Covers_Load_Charge : if [PL > 0 && Ppv + Pw >= PL && SoC < 0.95];
    ! * -> RES_Covers_Load_Spare : if [PL > 0 && Ppv + Pw >= PL && SoC >= 0.95];
    ! * -> Battery_Discharge_Priority : if [PL > 0 && Ppv + Pw < PL && SoC >= 0.20 && PL - Ppv - Pw <= Pbat_discharge_Pmax];
    ! * -> LNG_Covers_Load_LowSoC_ChargeMargin : if [PL > 0 && Ppv + Pw < PL && SoC < 0.20 && PL - Ppv - Pw + Pgmax / 5 <= Pgmax];
    ! * -> LNG_Covers_Load : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw <= Pgmax && (SoC < 0.20 || PL - Ppv - Pw > Pbat_discharge_Pmax)];
    ! * -> LNG_Engine3_Covers_Load : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > Pgmax && PL - Ppv - Pw <= Pgmax + eng3_Pmax];
    ! * -> DG1_Covers_Load_LowSoC_ChargeMargin : if [PL > 0 && Ppv + Pw < PL && SoC < 0.20 && PL - Ppv - Pw > Pgmax + eng3_Pmax && PL - Ppv - Pw + Pd1max / 10 <= Pgmax + eng3_Pmax + Pd1max];
    ! * -> DG1_Covers_Load : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > Pgmax + eng3_Pmax && PL - Ppv - Pw <= Pgmax + eng3_Pmax + Pd1max];
    ! * -> DG2_Covers_Load_WithOptionalChargeMargin : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > Pgmax + eng3_Pmax + Pd1max && PL - Ppv - Pw <= Pgmax + eng3_Pmax + Pd1max + Pd2max];

    [*] -> ZeroLoad_RES_Charge;

    state ZeroLoad_RES_Charge {
        enter {
            Pgen_req = 0;
            PLNG_req = 0;
            PENG3_req = 0;
            PDG1_req = 0;
            PDG2_req = 0;
            Pbat_discharge = 0;
            Pbat_charge = Ppv + Pw;
            Pspare = 0;
            cutin_LNG = 0;
            cutout_LNG = 1;
            cutin_ENG3 = 0;
            cutout_ENG3 = 1;
            cutin_DG1 = 0;
            cutout_DG1 = 1;
            cutin_DG2 = 0;
            cutout_DG2 = 1;
            load_cutout = 0;
        }
    }

    state ZeroLoad_RES_Spare {
        enter {
            Pgen_req = 0;
            PLNG_req = 0;
            PENG3_req = 0;
            PDG1_req = 0;
            PDG2_req = 0;
            Pbat_discharge = 0;
            Pbat_charge = 0;
            Pspare = Ppv + Pw;
            cutin_LNG = 0;
            cutout_LNG = 1;
            cutin_ENG3 = 0;
            cutout_ENG3 = 1;
            cutin_DG1 = 0;
            cutout_DG1 = 1;
            cutin_DG2 = 0;
            cutout_DG2 = 1;
            load_cutout = 0;
        }
    }

    state RES_Covers_Load_Charge {
        enter {
            Pgen_req = 0;
            PLNG_req = 0;
            PENG3_req = 0;
            PDG1_req = 0;
            PDG2_req = 0;
            Pbat_discharge = 0;
            Pbat_charge = Ppv + Pw - PL;
            Pspare = 0;
            cutin_LNG = 0;
            cutout_LNG = 1;
            cutin_ENG3 = 0;
            cutout_ENG3 = 1;
            cutin_DG1 = 0;
            cutout_DG1 = 1;
            cutin_DG2 = 0;
            cutout_DG2 = 1;
            load_cutout = 0;
        }
    }

    state RES_Covers_Load_Spare {
        enter {
            Pgen_req = 0;
            PLNG_req = 0;
            PENG3_req = 0;
            PDG1_req = 0;
            PDG2_req = 0;
            Pbat_discharge = 0;
            Pbat_charge = 0;
            Pspare = Ppv + Pw - PL;
            cutin_LNG = 0;
            cutout_LNG = 1;
            cutin_ENG3 = 0;
            cutout_ENG3 = 1;
            cutin_DG1 = 0;
            cutout_DG1 = 1;
            cutin_DG2 = 0;
            cutout_DG2 = 1;
            load_cutout = 0;
        }
    }

    state Battery_Discharge_Priority {
        enter {
            Pgen_req = 0;
            PLNG_req = 0;
            PENG3_req = 0;
            PDG1_req = 0;
            PDG2_req = 0;
            Pbat_discharge = PL - Ppv - Pw;
            Pbat_charge = 0;
            Pspare = 0;
            cutin_LNG = 0;
            cutout_LNG = 1;
            cutin_ENG3 = 0;
            cutout_ENG3 = 1;
            cutin_DG1 = 0;
            cutout_DG1 = 1;
            cutin_DG2 = 0;
            cutout_DG2 = 1;
            load_cutout = 0;
        }
    }

    state LNG_Covers_Load {
        enter {
            Pgen_req = PL - Ppv - Pw;
            PLNG_req = PL - Ppv - Pw;
            PENG3_req = 0;
            PDG1_req = 0;
            PDG2_req = 0;
            Pbat_discharge = 0;
            Pbat_charge = 0;
            Pspare = 0;
            cutin_LNG = 1;
            cutout_LNG = 0;
            cutin_ENG3 = 0;
            cutout_ENG3 = 1;
            cutin_DG1 = 0;
            cutout_DG1 = 1;
            cutin_DG2 = 0;
            cutout_DG2 = 1;
            load_cutout = 0;
        }
    }

    state LNG_Covers_Load_LowSoC_ChargeMargin {
        enter {
            Pgen_req = PL - Ppv - Pw + Pgmax / 5;
            PLNG_req = PL - Ppv - Pw + Pgmax / 5;
            PENG3_req = 0;
            PDG1_req = 0;
            PDG2_req = 0;
            Pbat_discharge = 0;
            Pbat_charge = Pgmax / 5;
            Pspare = 0;
            cutin_LNG = 1;
            cutout_LNG = 0;
            cutin_ENG3 = 0;
            cutout_ENG3 = 1;
            cutin_DG1 = 0;
            cutout_DG1 = 1;
            cutin_DG2 = 0;
            cutout_DG2 = 1;
            load_cutout = 0;
        }
    }

    state LNG_Engine3_Covers_Load {
        enter {
            Pgen_req = PL - Ppv - Pw;
            PLNG_req = Pgmax;
            PENG3_req = PL - Ppv - Pw - Pgmax;
            PDG1_req = 0;
            PDG2_req = 0;
            Pbat_discharge = 0;
            Pbat_charge = 0;
            Pspare = 0;
            cutin_LNG = 1;
            cutout_LNG = 0;
            cutin_ENG3 = 1;
            cutout_ENG3 = 0;
            cutin_DG1 = 0;
            cutout_DG1 = 1;
            cutin_DG2 = 0;
            cutout_DG2 = 1;
            load_cutout = 0;
        }
    }

    state DG1_Covers_Load {
        enter {
            Pgen_req = PL - Ppv - Pw;
            PLNG_req = Pgmax;
            PENG3_req = eng3_Pmax;
            PDG1_req = PL - Ppv - Pw - Pgmax - eng3_Pmax;
            PDG2_req = 0;
            Pbat_discharge = 0;
            Pbat_charge = 0;
            Pspare = 0;
            cutin_LNG = 1;
            cutout_LNG = 0;
            cutin_ENG3 = 1;
            cutout_ENG3 = 0;
            cutin_DG1 = 1;
            cutout_DG1 = 0;
            cutin_DG2 = 0;
            cutout_DG2 = 1;
            load_cutout = 0;
        }
    }

    state DG1_Covers_Load_LowSoC_ChargeMargin {
        enter {
            Pgen_req = PL - Ppv - Pw + Pd1max / 10;
            PLNG_req = Pgmax;
            PENG3_req = eng3_Pmax;
            PDG1_req = PL - Ppv - Pw - Pgmax - eng3_Pmax + Pd1max / 10;
            PDG2_req = 0;
            Pbat_discharge = 0;
            Pbat_charge = Pd1max / 10;
            Pspare = 0;
            cutin_LNG = 1;
            cutout_LNG = 0;
            cutin_ENG3 = 1;
            cutout_ENG3 = 0;
            cutin_DG1 = 1;
            cutout_DG1 = 0;
            cutin_DG2 = 0;
            cutout_DG2 = 1;
            load_cutout = 0;
        }
    }

    state DG2_Covers_Load_WithOptionalChargeMargin {
        enter {
            if [SoC < 0.20] {
                Pgen_req = PL - Ppv - Pw + Pd1max / 10;
                PLNG_req = Pgmax;
                PENG3_req = eng3_Pmax;
                PDG1_req = Pd1max;
                PDG2_req = PL - Ppv - Pw - Pgmax - eng3_Pmax - Pd1max + Pd1max / 10;
                Pbat_charge = Pd1max / 10;
            } else {
                Pgen_req = PL - Ppv - Pw;
                PLNG_req = Pgmax;
                PENG3_req = eng3_Pmax;
                PDG1_req = Pd1max;
                PDG2_req = PL - Ppv - Pw - Pgmax - eng3_Pmax - Pd1max;
                Pbat_charge = 0;
            }
            Pbat_discharge = 0;
            Pspare = 0;
            cutin_LNG = 1;
            cutout_LNG = 0;
            cutin_ENG3 = 1;
            cutout_ENG3 = 0;
            cutin_DG1 = 1;
            cutout_DG1 = 0;
            cutin_DG2 = 1;
            cutout_DG2 = 0;
            load_cutout = 0;
        }
    }

    state IllegalOverloadCompletion {
        enter {
            Pgen_req = Pgmax + eng3_Pmax +
... <truncated 548 chars; see run record>
```

#### Candidate diff（before -> candidate）

```diff
--- before.fcstm
+++ candidate.fcstm
@@ -29,14 +29,15 @@
     ! * -> IllegalOverloadCompletion : if [PL - Ppv - Pw > Pgmax + eng3_Pmax + Pd1max + Pd2max];
     ! * -> ZeroLoad_RES_Charge : if [PL == 0 && Ppv + Pw > 0 && SoC < 0.95];
     ! * -> ZeroLoad_RES_Spare : if [PL == 0 && Ppv + Pw > 0 && SoC >= 0.95];
+    ! * -> ZeroLoad_RES_Spare : if [PL == 0 && Ppv + Pw <= 0];
     ! * -> RES_Covers_Load_Charge : if [PL > 0 && Ppv + Pw >= PL && SoC < 0.95];
     ! * -> RES_Covers_Load_Spare : if [PL > 0 && Ppv + Pw >= PL && SoC >= 0.95];
     ! * -> Battery_Discharge_Priority : if [PL > 0 && Ppv + Pw < PL && SoC >= 0.20 && PL - Ppv - Pw <= Pbat_discharge_Pmax];
     ! * -> LNG_Covers_Load_LowSoC_ChargeMargin : if [PL > 0 && Ppv + Pw < PL && SoC < 0.20 && PL - Ppv - Pw + Pgmax / 5 <= Pgmax];
-    ! * -> LNG_Covers_Load : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > Pbat_discharge_Pmax && PL - Ppv - Pw <= Pgmax];
+    ! * -> LNG_Covers_Load : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw <= Pgmax && (SoC < 0.20 || PL - Ppv - Pw > Pbat_discharge_Pmax)];
     ! * -> LNG_Engine3_Covers_Load : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > Pgmax && PL - Ppv - Pw <= Pgmax + eng3_Pmax];
     ! * -> DG1_Covers_Load_LowSoC_ChargeMargin : if [PL > 0 && Ppv + Pw < PL && SoC < 0.20 && PL - Ppv - Pw > Pgmax + eng3_Pmax && PL - Ppv - Pw + Pd1max / 10 <= Pgmax + eng3_Pmax + Pd1max];
-    ! * -> DG1_Covers_Load : if [PL > 0 && Ppv + Pw < PL && SoC >= 0.20 && PL - Ppv - Pw > Pgmax + eng3_Pmax && PL - Ppv - Pw <= Pgmax + eng3_Pmax + Pd1max];
+    ! * -> DG1_Covers_Load : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > Pgmax + eng3_Pmax && PL - Ppv - Pw <= Pgmax + eng3_Pmax + Pd1max];
     ! * -> DG2_Covers_Load_WithOptionalChargeMargin : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > Pgmax + eng3_Pmax + Pd1max && PL - Ppv - Pw <= Pgmax + eng3_Pmax + Pd1max + Pd2max];
 
     [*] -> ZeroLoad_RES_Charge;
```

#### SL-10 审查结果

- SL-10 decision=`pass`，ok=`True`，target_resolved=`True`，regression_detected=`False`，drift_risk=`minor`。
- SL-10 review_meta：schema=`SL10RepairReviewOutput.v1`，failure_policy=`fail_closed`，replay_key=`SL-10:sha256:cdca2b1f673486883f87161a49b1f99a0e923cfc82c8cafac912b0d1de772f80`。
  - SL-10 evidence 1: `{"summary": "The SL-9 accepted edits directly address the current SL-7 model-review findings. The candidate adds an explicit hot-running zero-load/no-RES classifier for PL == 0 and Ppv + Pw <= 0, so the FSM no longer leaves stale generator, battery, spare-power, cut-in/cut-out, or load_cutout outputs in the zero-demand/no-renewable region. The target state ZeroLoad_RES_Spare has zero generator requests, zero battery discharge/charge, thermal cut-outs asserted, and load_cutout cleared, which is consistent with the NL requirement that when PL = 0 the EMS routes RES to charging/spare according to SoC and otherwise maintains zero dispatch."}`
  - SL-10 evidence 2: `{"summary": "The candidate closes the low-SoC LNG-coverable gap identified in fixreq-3-sl7-0 by preserving the earlier LNG_Covers_Load_LowSoC_ChargeMargin guard for feasible Pgmax/5 charging-margin cases and broadening LNG_Covers_Load to cover low-SoC fallback cases where the margin does not fit but the base deficit is still within Pgmax. This matches the NL priority of RES first, batteries only when SoC is suitable, LNG before diesel, and the explicit Pgmax/5 margin when feasible."}`
  - SL-10 evidence 3: `{"summary": "The candidate closes the low-SoC DG1-range gap by preserving DG1_Covers_Load_LowSoC_ChargeMargin for feasible Pd1max/10 charging-margin cases and broadening DG1_Covers_Load to cover the fallback interval where the deficit is within Pgmax + eng3_Pmax + Pd1max but the margin does not fit. This preserves DG1/DG2 as late-priority resources while preventing unclassified low-SoC DG1-range operation."}`
  - SL-10 evidence 4: `{"summary": "The DSL diff is minimal and does not drop NL-required structure. All required variables, dispatch outputs, generator-specific request outputs, cut-in/cut-out commands, load_cutout, and all twelve states remain present. The accepted IllegalOverloadCompletion behavior from the prior FixLog is preserved: overload begins when net deficit exceeds total thermal capacity, activates all thermal units, uses battery discharge for the remaining lack, and asserts load_cutout."}`
  - SL-10 evidence 5: `{"summary": "The complete FixLog supports acceptance. Earlier external-input warnings were waived because PL, Ppv, Pw, SoC, Pgmax, eng3_Pmax, Pd1max, Pd2max, and Pbat_discharge_Pmax are NL-described measurements/capacity bounds, not variables the EMS should internally write. The current candidate does not revisit or regress those waived issues. The prior iteration's overload scenario regression was repaired and local evidence for this iteration reports no scenario_regression."}`
  - SL-10 evidence 6: `{"summary": "The current local deterministic check reports no regression, but rejects on forced_transition_count_drift and missing_required_grounding. Those local findings are conservative evidence rather than hard NL violations here: the transition-count increase is exactly explained by adding one required wildcard classifier across the existing twelve-state wildcard-reclassification pattern, and the grounding IDs transition:classify_zero_load and transition:classify_dg_late_priority are represented by concrete wildcard guards and state actions retained in the candidate."}`
- local checks evidence：stage=`SD-10`；note=PR-E1 uses local parse/semantic/design/sim checks as SL-10 evidence, not as the final deterministic judge.。
  - local ok=`False`，target_resolved=`False`，regression_detected=`False`，drift_risk=`major`。
  - local_rejection：reason=`forced_transition_count_drift; missing_required_grounding`，rejected_by_stage=`SD-10`。
    - local evidence 1: `forced_transition_count_drift` {"fix_target": "model_review", "kind": "forced_transition_count_drift", "new": 156, "old": 144}
    - local evidence 2: `missing_required_grounding` {"element_ids": ["transition:classify_zero_load", "transition:classify_dg_late_priority"], "kind": "missing_required_grounding"}

</details>


#### FixLog ledger

口径：FixLog 是跨 iteration 的 append-only repair 台账，记录 request batch、SL-9 accept/reject、diff/local evidence、SL-10 批示和下一步动作。

| # | iteration | phase | batch | decisions | next_action | candidate | notes |
|---:|---:|---|---|---|---|---|---|
| 1 | `0` | `request_batch` | `fixbatch-0-sha256-8829c3d5386` | accept=0, reject=0 | `sl9_decision_and_repair` | `<none>` | SD-8 produced FixRequestBatch; deterministic stage does not decide final repair. |
| 2 | `0` | `sl9_decision` | `fixbatch-0-sha256-8829c3d5386` | accept=8, reject=4 | `sl10_review` | `sha256:ae74dfc8a541f448b34f805ad6dbf46262a2b2b804509e2e7866abecbe67c8aa` | Read the FixLog and repair_memory: there are no prior rejected candidates or actionable rework objections to address., Made the smallest design repair by inlining fixed SoC thresholds instead of adding meaningless self-assignments or invented dynamics., Preserved all required states, required input/output variables, dispatch actions, cut-in/cut-out commands, zero-load branches, RES charge/spare branches, battery-priority branch, LNG/DG priority branches, low-SoC charge margins, and illegal overload completion behavior., ... +1 |
| 3 | `0` | `sl10_review` | `fixbatch-0-sha256-8829c3d5386` | accept=8, reject=4 | `sc11_accept_then_sd2` | `sha256:ae74dfc8a541f448b34f805ad6dbf46262a2b2b804509e2e7866abecbe67c8aa` | repair_memory:sl10_evidence, repair_memory:sl10_evidence, repair_memory:sl10_evidence, ... +5 |
| 4 | `1` | `request_batch` | `fixbatch-1-sha256-5a45bfc6f1a` | accept=0, reject=0 | `sl9_decision_and_repair` | `<none>` | SD-8 produced FixRequestBatch; deterministic stage does not decide final repair. |
| 5 | `1` | `sl9_decision` | `fixbatch-1-sha256-5a45bfc6f1a` | accept=0, reject=12 | `reject_or_waiver` | `<none>` | All current fix requests target never-written reads or guards over variables that the NL defines as external measurements or capacity bounds: PL, Ppv, Pw, SoC, Pgmax, eng3_Pmax, Pd1max, Pd2max, and Pbat_discharge_Pmax., The FixLog shows Pd2max and Pbat_discharge_Pmax were previously rejected/waived for the same reason, and no new evidence provides an NL-grounded update law for them., Adding self-assignments, synthetic command variables, or plant/environment dynamics would violate the request’s forbidden edits and reduce NL fidelity., ... +1 |
| 6 | `1` | `sl9_all_rejected` | `fixbatch-1-sha256-5a45bfc6f1a` | accept=0, reject=12 | `continue_after_waiver` | `<none>` | sl9_rejected_all_fix_requests:waiver_continue |
| 7 | `2` | `request_batch` | `fixbatch-2-sha256-2baadc6ec74` | accept=0, reject=0 | `sl9_decision_and_repair` | `<none>` | SD-8 produced FixRequestBatch; deterministic stage does not decide final repair. |
| 8 | `2` | `sl9_decision` | `fixbatch-2-sha256-2baadc6ec74` | accept=4, reject=0 | `sl10_review` | `sha256:4c5a6347ae4632bd2b168c1d08eef85bdcfb190e6335c8e955fb8d53d02b8d19` | Addressed the new SL-7 model-review target rather than re-fixing previously waived external-input warnings., Expected behavior for IllegalOverloadCompletion: deficit exceeds total thermal generation Pgmax + eng3_Pmax + Pd1max + Pd2max, all thermal units are requested, and the remaining lack is covered by battery discharge., Prior actual behavior: IllegalOverloadCompletion only fired when deficit exceeded total thermal plus Pbat_discharge_Pmax, making Pbat_discharge necessarily greater than Pbat_discharge_Pmax and leaving the thermal-exceeded battery-coverable interval uncovered., ... +2 |
| 9 | `2` | `sl10_review` | `fixbatch-2-sha256-2baadc6ec74` | accept=4, reject=0 | `sl9_rework` | `sha256:4c5a6347ae4632bd2b168c1d08eef85bdcfb190e6335c8e955fb8d53d02b8d19` | SL-10 pass was downgraded because local deterministic evidence reported major drift and SL-10 evidence did not explicitly address the local rejection reason/kind with a structured local_override_rationale., For the next SL-9 repair, do not blindly regenerate the same DSL. Either change the candidate so the local major-drift evidence is resolved, or keep the minimal DSL only with explicit repair_rationale mapping each local objection (for example missing_required_grounding, scenario_regression, count_drift, or forced_transition_count_drift) to concrete NL-grounded states/transitions/actions that remain in the candidate. This rationale is required so SL-10 can produce local_override_rationale instead of cycling., repair_memory:SL-10 pass was downgraded because local deterministic evidence reported major drift and SL-10 evidence did not explicitly address the local rejection reason/kind with a structured local_override_rationale., ... +11 |
| 10 | `2` | `sl9_rework_decision` | `fixbatch-2-sha256-2baadc6ec74` | accept=4, reject=0 | `sl10_review` | `sha256:27ff012eeca8958395886399d5f506d668adb07be506c45860ce7acb776355e5` | Smallest DSL edit: only the first wildcard guard was changed from deficit > thermal + Pbat_discharge_Pmax to deficit > thermal. All variables, all twelve dispatch states, and all enter actions are preserved., The scenario_regression_repair_brief is addressed. For illegal_overload_activates_all_thermal_and_battery, initial deficit is 50 and thermal capacity is 35, so the repaired guard enters LNGShipEMS.IllegalOverloadCompletion from DG2_Covers_Load_WithOptionalChargeMargin and its enter action produces the expected thermal requests, Pgen_req=35, Pbat_discharge=15, zero charge/spare, cut-in commands, and load_cutout=1., For forced_reclassification_from_zero_load_to_illegal, the same repaired wildcard forced guard is true from ZeroLoad_RES_Charge, so the model no longer remains in the benign zero-load state under extreme overload variables., ... +5 |
| 11 | `2` | `sl10_rework_review` | `fixbatch-2-sha256-2baadc6ec74` | accept=4, reject=0 | `sc11_accept_then_sd2` | `sha256:27ff012eeca8958395886399d5f506d668adb07be506c45860ce7acb776355e5` | repair_memory:sl10_evidence, repair_memory:sl10_evidence, repair_memory:sl10_evidence, ... +6 |
| 12 | `3` | `request_batch` | `fixbatch-3-sha256-b2c527b44d2` | accept=0, reject=0 | `sl9_decision_and_repair` | `<none>` | SD-8 produced FixRequestBatch; deterministic stage does not decide final repair. |
| 13 | `3` | `sl9_decision` | `fixbatch-3-sha256-b2c527b44d2` | accept=2, reject=0 | `sl10_review` | `sha256:4b52356070e7a51d779df874526281152b5fb3e1dac5b2f71a14dc2af9ccf364` | The current batch targets model-review coverage and stale-output safety, not the previously waived external-input warnings. PL, Ppv, Pw, SoC, Pgmax, eng3_Pmax, Pd1max, Pd2max, and Pbat_discharge_Pmax remain external measurements/capacity bounds and are not artificially written., For PL == 0 && Ppv + Pw == 0, the added wildcard transition to ZeroLoad_RES_Spare gives a hot-running zero-output reclassification. Its enter action sets generator requests, battery discharge/charge, and spare power to zero and cuts out thermal units, so stale prior dispatch commands are cleared., For low-SoC LNG-coverable deficits where Pgmax/5 charging margin does not fit, the broadened LNG_Covers_Load guard now catches the fallback case when the deficit is within Pgmax. The existing low-SoC charge-margin guard remains earlier in the declaration order, so margin behavior is preserved when it is feasible., ... +3 |
| 14 | `3` | `sl10_review` | `fixbatch-3-sha256-b2c527b44d2` | accept=2, reject=0 | `sc11_accept_then_sd2` | `sha256:4b52356070e7a51d779df874526281152b5fb3e1dac5b2f71a14dc2af9ccf364` | repair_memory:sl10_evidence, repair_memory:sl10_evidence, repair_memory:sl10_evidence, ... +7 |

### 8. 尝试记录与成本

- `SL-1`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 7161, 'completion_chars': 23547, 'completion_tokens': 9885, 'elapsed_seconds': 180.52869905099215, 'estimated_completion_tokens': 5887, 'estimated_prompt_tokens': 6646, 'estimated_total_tokens': 12533, 'first_chunk_seconds': 51.49155861100007, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 26582, 'prompt_tokens': 6469, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 16354}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-9`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 5068, 'completion_chars': 15894, 'completion_tokens': 5490, 'elapsed_seconds': 101.6530185080046, 'estimated_completion_tokens': 3974, 'estimated_prompt_tokens': 38957, 'estimated_total_tokens': 42931, 'first_chunk_seconds': 10.531024747004267, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 155828, 'prompt_tokens': 38170, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 43660}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-10`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 898, 'completion_chars': 4023, 'completion_tokens': 1417, 'elapsed_seconds': 29.64908825000748, 'estimated_completion_tokens': 1006, 'estimated_prompt_tokens': 34400, 'estimated_total_tokens': 35406, 'first_chunk_seconds': 13.378518733006786, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 137597, 'prompt_tokens': 32789, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 34206}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-9`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1551, 'completion_chars': 6265, 'completion_tokens': 2588, 'elapsed_seconds': 51.030672360997414, 'estimated_completion_tokens': 1567, 'estimated_prompt_tokens': 55141, 'estimated_total_tokens': 56708, 'first_chunk_seconds': 26.345705668005394, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 220563, 'prompt_tokens': 50777, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 53365}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 4317, 'completion_chars': 13480, 'completion_tokens': 5576, 'elapsed_seconds': 102.83387442199455, 'estimated_completion_tokens': 3370, 'estimated_prompt_tokens': 17461, 'estimated_total_tokens': 20831, 'first_chunk_seconds': 25.212799849003204, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 69844, 'prompt_tokens': 18659, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 24235}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 5126, 'completion_chars': 16123, 'completion_tokens': 5755, 'elapsed_seconds': 106.15618400801031, 'estimated_completion_tokens': 4031, 'estimated_prompt_tokens': 20996, 'estimated_total_tokens': 25027, 'first_chunk_seconds': 15.832818574999692, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 83983, 'prompt_tokens': 23095, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 28850}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 5564, 'completion_chars': 17507, 'completion_tokens': 5891, 'elapsed_seconds': 110.33180209099373, 'estimated_completion_tokens': 4377, 'estimated_prompt_tokens': 21657, 'estimated_total_tokens': 26034, 'first_chunk_seconds': 11.663981107994914, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 86626, 'prompt_tokens': 23904, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 29795}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-7`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1907, 'completion_chars': 8505, 'completion_tokens': 3367, 'elapsed_seconds': 64.99780112400185, 'estimated_completion_tokens': 2127, 'estimated_prompt_tokens': 49290, 'estimated_total_tokens': 51417, 'first_chunk_seconds': 30.579426220007008, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 197158, 'prompt_tokens': 56533, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 59900}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-7`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 2093, 'completion_chars': 9268, 'completion_tokens': 3308, 'elapsed_seconds': 62.64745768500143, 'estimated_completion_tokens': 2317, 'estimated_prompt_tokens': 49483, 'estimated_total_tokens': 51800, 'first_chunk_seconds': 24.94158055599837, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 197929, 'prompt_tokens': 56952, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 60260}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-9`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 4381, 'completion_chars': 13756, 'completion_tokens': 4870, 'elapsed_seconds': 91.15603073699458, 'estimated_completion_tokens': 3439, 'estimated_prompt_tokens': 36344, 'estimated_total_tokens': 39783, 'first_chunk_seconds': 12.203872075988329, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 145375, 'prompt_tokens': 33407, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 38277}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-10`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1181, 'completion_chars': 5077, 'completion_tokens': 2502, 'elapsed_seconds': 47.83005547100038, 'estimated_completion_tokens': 1270, 'estimated_prompt_tokens': 34568, 'estimated_total_tokens': 35838, 'first_chunk_seconds': 26.50897259300109, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 138270, 'prompt_tokens': 32699, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 35201}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-9`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 4672, 'completion_chars': 14911, 'completion_tokens': 5760, 'elapsed_seconds': 107.34575161000248, 'estimated_completion_tokens': 3728, 'estimated_prompt_tokens': 97250, 'estimated_total_tokens': 100978, 'first_chunk_seconds': 25.872782930993708, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 388997, 'prompt_tokens': 85596, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 91356}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-10`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1197, 'completion_chars': 5404, 'completion_tokens': 1957, 'elapsed_seconds': 38.44646516899229, 'estimated_completion_tokens': 1351, 'estimated_prompt_tokens': 57233, 'estimated_total_tokens': 58584, 'first_chunk_seconds': 16.75682480400428, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 228930, 'prompt_tokens': 53526, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 55483}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 5143, 'completion_chars': 15598, 'completion_tokens': 6180, 'elapsed_seconds': 113.98490804700123, 'estimated_completion_tokens': 3900, 'estimated_prompt_tokens': 24712, 'estimated_total_tokens': 28612, 'first_chunk_seconds': 23.751991782992263, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 98847, 'prompt_tokens': 27324, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 33504}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 5763, 'completion_chars': 17428, 'completion_tokens': 6062, 'elapsed_seconds': 111.81846464698901, 'estimated_completion_tokens': 4357, 'estimated_prompt_tokens': 24328, 'estimated_total_tokens': 28685, 'first_chunk_seconds': 8.45909660498728, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 97312, 'prompt_tokens': 26908, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 32970}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-7`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 2569, 'completion_chars': 11222, 'completion_tokens': 4321, 'elapsed_seconds': 85.74137564100965, 'estimated_completion_tokens': 2806, 'estimated_prompt_tokens': 51409, 'estimated_total_tokens': 54215, 'first_chunk_seconds': 39.65298604000418, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 205635, 'prompt_tokens': 58989, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 63310}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-9`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 4509, 'completion_chars': 14038, 'completion_tokens': 5867, 'elapsed_seconds': 109.1716848849901, 'estimated_completion_tokens': 3510, 'estimated_prompt_tokens': 71223, 'estimated_total_tokens': 74733, 'first_chunk_seconds': 27.841769807986566, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 284891, 'prompt_tokens': 62617, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 68484}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-10`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1189, 'completion_chars': 5523, 'completion_tokens': 1598, 'elapsed_seconds': 33.370638665001024, 'estimated_completion_tokens': 1381, 'estimated_prompt_tokens': 35072, 'estimated_total_tokens': 36453, 'first_chunk_seconds': 10.223494840000058, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 140287, 'prompt_tokens': 33593, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 35191}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 6385, 'completion_chars': 19276, 'completion_tokens': 6736, 'elapsed_seconds': 124.01588605598954, 'estimated_completion_tokens': 4819, 'estimated_prompt_tokens': 27294, 'estimated_total_tokens': 32113, 'first_chunk_seconds': 8.944417783990502, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 109176, 'prompt_tokens': 29965, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 36701}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 7024, 'completion_chars': 21152, 'completion_tokens': 7497, 'elapsed_seconds': 137.75287225999637, 'estimated_completion_tokens': 5288, 'estimated_prompt_tokens': 27756, 'estimated_total_tokens': 33044, 'first_chunk_seconds': 11.201633200995275, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 111024, 'prompt_tokens': 30587, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 38084}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-7`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1810, 'completion_chars': 8138, 'completion_tokens': 3059, 'elapsed_seconds': 58.41633775200171, 'estimated_completion_tokens': 2035, 'estimated_prompt_tokens': 53912, 'estimated_total_tokens': 55947, 'first_chunk_seconds': 25.644523604001733, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 215647, 'prompt_tokens': 61422, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 64481}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。

### 9. 最终停止状态与后续含义

- 停止状态：verdict=`success`，record_status=`success`。
- 主要原因分类：`success_but_weak_oracle_ineligible`。
- required stages executed：`65/16`，missing=`<none>`。
- repairs：`3/5` accepted；scenario_history=`10`。
- 配置含义：`recommended baseline candidate`；该结果可用于评估默认入口本身。
- 主结果/蓝本边界：`main_result_eligible` 只表示该 run 非 provider-invalid 且 trace/schema/secret/final-verdict 口径可进入主结果候选；`path2_ref_model_blueprint_eligible=false` 时，模型仍可作为 FE/BVS 或 dispatch-classifier 压力测试证据，但不得称为 Path2 ref-model 主蓝本。
- 样本含义：若出现 `design_or_variable_dynamics`，应重点审查变量是否仅作为 guard/input 常量而没有事件/动作更新；若出现 pre-scenario parse/semantic 失败，则应先优化 pyfcstm grammar adherence。
