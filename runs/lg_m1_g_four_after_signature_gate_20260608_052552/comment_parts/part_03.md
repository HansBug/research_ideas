## 四例真实运行 evidence（20f104e8，part 3/3）

身份：主 session / LG-M1-G runner。

本条为 PR #77 在最新 head `20f104e8` 上重跑 ABS / CARA / Elevator / LNG 四例的 evidence 分片；完整 artifact 目录：`runs/lg_m1_g_four_after_signature_gate_20260608_052552`。

<details><summary>path2 / path2_lng_ems / default / success</summary>

#### NL 输入（原文）

```text
The LNG-ship EMS manages a ship energy system with PVs, WECs, DGs, LNG, batteries, and time-varying ship loads, issuing cut-in and cut-out commands for generating units and loads. It controls power dispatch between generating units and load demand during changing time periods and operating conditions, dynamically switching states to maintain power balance as resources and demands vary. The FSM reads load demand PL, renewable contributions Ppv and Pw, battery state of charge SoC, and engine capacity bounds such as eng3_Pmax, then returns requested generator power, battery discharge or charging power, and spare power. The twelve finite states are selected by logical transition conditions over demand, generation, capacity, and SoC. When Ppv + Pw covers PL, the EMS serves all ship demand from RES and charges batteries while SoC is below 0.95, or treats residual renewable power as spare once SoC is at least 0.95. When Ppv + Pw is below PL, dispatch follows the stated priority: RES first, batteries when SoC is suitable, LNG before diesel units, and DG1/DG2 only as the last priority. Low-SoC branches add explicit charging margins, including Pgmax/5 in an LNG-covered case and Pd1max/10 in later diesel-generator cases. When PL = 0, RES production is sent to battery charging or to spare power according to SoC thresholds. The overload completion state is illegal: if extreme demand exceeds all RES and thermal resources, EMS activates all thermal generating units, covers the lack by battery discharge, and the state shall never occur in practice.
```

#### NL 输入中文翻译

```text
LNG 船 EMS 管理一个包含光伏、波浪能、柴油机、LNG、电池和随时间变化船舶负载的船舶能源系统，并向发电单元与负载发出切入/切出命令。它在变化的时段和运行条件下控制发电单元与负载需求之间的功率调度，随着资源和需求变化动态切换状态以保持功率平衡。FSM 读取负载需求 PL、可再生贡献 Ppv 和 Pw、电池荷电状态 SoC，以及 eng3_Pmax 等发动机容量边界，然后返回请求的发电机功率、电池放电或充电功率以及备用功率。十二个有限状态由需求、发电、容量和 SoC 上的逻辑转移条件选择。当 Ppv + Pw 覆盖 PL 时，EMS 用 RES 满足全部船舶需求，并在 SoC 低于 0.95 时给电池充电，或在 SoC 至少为 0.95 时把剩余可再生功率视为备用功率。当 Ppv + Pw 低于 PL 时，调度遵循优先级：RES 优先，SoC 合适时使用电池，LNG 先于柴油机，DG1/DG2 只作为最后优先级。低 SoC 分支加入明确充电裕量，包括 LNG 覆盖场景中的 Pgmax/5，以及后续柴油发电机场景中的 Pd1max/10。当 PL = 0 时，RES 产出根据 SoC 阈值送往电池充电或备用功率。过载完成状态是非法状态：若极端需求超过全部 RES 与热力资源，EMS 会激活全部热发电单元并用电池放电弥补缺口，该状态实践中不应发生。
```

#### FCSTM 输出

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
def float Plng_req = 0.0;
def float Pd1_req = 0.0;
def float Pd2_req = 0.0;
def float Pbat_dis = 0.0;
def float Pbat_ch = 0.0;
def float spare_power = 0.0;
def int cut_in_LNG = 0;
def int cut_out_LNG = 0;
def int cut_in_DG1 = 0;
def int cut_out_DG1 = 0;
def int cut_in_DG2 = 0;
def int cut_out_DG2 = 0;
def int cut_in_loads = 0;
def int cut_out_loads = 0;

state LNGShipEMS {
    ! * -> ZeroLoadCharge : if [PL == 0 && SoC < 0.95];
    ! * -> ZeroLoadSpare : if [PL == 0 && SoC >= 0.95];
    ! * -> ResCoversCharge : if [PL > 0 && Ppv + Pw >= PL && SoC < 0.95];
    ! * -> ResCoversSpare : if [PL > 0 && Ppv + Pw >= PL && SoC >= 0.95];
    ! * -> BatteryDischarge : if [Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw <= Pbat_Pmax];
    ! * -> LngWithBattery : if [Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw > Pbat_Pmax && PL - Ppv - Pw - Pbat_Pmax <= eng3_Pmax];
    ! * -> LngLowSocCharge : if [Ppv + Pw < PL && SoC < 0.2 && PL - Ppv - Pw + Pgmax / 5 <= eng3_Pmax];
    ! * -> Dg1WithBattery : if [Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw - Pbat_Pmax > eng3_Pmax && PL - Ppv - Pw - Pbat_Pmax - eng3_Pmax <= Pd1max];
    ! * -> Dg1LowSocCharge : if [Ppv + Pw < PL && SoC < 0.2 && PL - Ppv - Pw + Pd1max / 10 > eng3_Pmax && PL - Ppv - Pw + Pd1max / 10 - eng3_Pmax <= Pd1max];
    ! * -> Dg2WithBattery : if [Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw - Pbat_Pmax - eng3_Pmax > Pd1max && PL - Ppv - Pw - Pbat_Pmax - eng3_Pmax - Pd1max <= Pd2max];
    ! * -> Dg2LowSocCharge : if [Ppv + Pw < PL && SoC < 0.2 && PL - Ppv - Pw + Pd1max / 10 - eng3_Pmax > Pd1max && PL - Ppv - Pw + Pd1max / 10 - eng3_Pmax - Pd1max <= Pd2max];
    ! * -> OverloadCompletionIllegal : if [PL > Ppv + Pw + eng3_Pmax + Pd1max + Pd2max];

    [*] -> ZeroLoadCharge;

    state ZeroLoadCharge {
        enter {
            Plng_req = 0.0;
            Pd1_req = 0.0;
            Pd2_req = 0.0;
            Pbat_dis = 0.0;
            Pbat_ch = Ppv + Pw;
            spare_power = 0.0;
            cut_in_LNG = 0;
            cut_out_LNG = 1;
            cut_in_DG1 = 0;
            cut_out_DG1 = 1;
            cut_in_DG2 = 0;
            cut_out_DG2 = 1;
            cut_in_loads = 0;
            cut_out_loads = 1;
        }
    }

    state ZeroLoadSpare {
        enter {
            Plng_req = 0.0;
            Pd1_req = 0.0;
            Pd2_req = 0.0;
            Pbat_dis = 0.0;
            Pbat_ch = 0.0;
            spare_power = Ppv + Pw;
            cut_in_LNG = 0;
            cut_out_LNG = 1;
            cut_in_DG1 = 0;
            cut_out_DG1 = 1;
            cut_in_DG2 = 0;
            cut_out_DG2 = 1;
            cut_in_loads = 0;
            cut_out_loads = 1;
        }
    }

    state ResCoversCharge {
        enter {
            Plng_req = 0.0;
            Pd1_req = 0.0;
            Pd2_req = 0.0;
            Pbat_dis = 0.0;
            Pbat_ch = Ppv + Pw - PL;
            spare_power = 0.0;
            cut_in_LNG = 0;
            cut_out_LNG = 1;
            cut_in_DG1 = 0;
            cut_out_DG1 = 1;
            cut_in_DG2 = 0;
            cut_out_DG2 = 1;
            cut_in_loads = 1;
            cut_out_loads = 0;
        }
    }

    state ResCoversSpare {
        enter {
            Plng_req = 0.0;
            Pd1_req = 0.0;
            Pd2_req = 0.0;
            Pbat_dis = 0.0;
            Pbat_ch = 0.0;
            spare_power = Ppv + Pw - PL;
            cut_in_LNG = 0;
            cut_out_LNG = 1;
            cut_in_DG1 = 0;
            cut_out_DG1 = 1;
            cut_in_DG2 = 0;
            cut_out_DG2 = 1;
            cut_in_loads = 1;
            cut_out_loads = 0;
        }
    }

    state BatteryDischarge {
        enter {
            Plng_req = 0.0;
            Pd1_req = 0.0;
            Pd2_req = 0.0;
            Pbat_dis = PL - Ppv - Pw;
            Pbat_ch = 0.0;
            spare_power = 0.0;
            cut_in_LNG = 0;
            cut_out_LNG = 1;
            cut_in_DG1 = 0;
            cut_out_DG1 = 1;
            cut_in_DG2 = 0;
            cut_out_DG2 = 1;
            cut_in_loads = 1;
            cut_out_loads = 0;
        }
    }

    state LngWithBattery {
        enter {
            Plng_req = PL - Ppv - Pw - Pbat_Pmax;
            Pd1_req = 0.0;
            Pd2_req = 0.0;
            Pbat_dis = Pbat_Pmax;
            Pbat_ch = 0.0;
            spare_power = 0.0;
            cut_in_LNG = 1;
            cut_out_LNG = 0;
            cut_in_DG1 = 0;
            cut_out_DG1 = 1;
            cut_in_DG2 = 0;
            cut_out_DG2 = 1;
            cut_in_loads = 1;
            cut_out_loads = 0;
        }
    }

    state LngLowSocCharge {
        enter {
            Plng_req = PL - Ppv - Pw + Pgmax / 5;
            Pd1_req = 0.0;
            Pd2_req = 0.0;
            Pbat_dis = 0.0;
            Pbat_ch = Pgmax / 5;
            spare_power = 0.0;
            cut_in_LNG = 1;
            cut_out_LNG = 0;
            cut_in_DG1 = 0;
            cut_out_DG1 = 1;
            cut_in_DG2 = 0;
            cut_out_DG2 = 1;
            cut_in_loads = 1;
            cut_out_loads = 0;
        }
    }

    state Dg1WithBattery {
        enter {
            Plng_req = eng3_Pmax;
            Pd1_req = PL - Ppv - Pw - Pbat_Pmax - eng3_Pmax;
            Pd2_req = 0.0;
            Pbat_dis = Pbat_Pmax;
            Pbat_ch = 0.0;
            spare_power = 0.0;
            cut_in_LNG = 1;
            cut_out_LNG = 0;
            cut_in_DG1 = 1;
            cut_out_DG1 = 0;
            cut_in_DG2 = 0;
            cut_out_DG2 = 1;
            cut_in_loads = 1;
            cut_out_loads = 0;
        }
    }

    state Dg1LowSocCharge {
        enter {
            Plng_req = eng3_Pmax;
            Pd1_req = PL - Ppv - Pw + Pd1max / 10 - eng3_Pmax;
            Pd2_req = 0.0;
            Pbat_dis = 0.0;
            Pbat_ch = Pd1max / 10;
            spare_power = 0.0;
            cut_in_LNG = 1;
            cut_out_LNG = 0;
            cut_in_DG1 = 1;
            cut_out_DG1 = 0;
            cut_in_DG2 = 0;
            cut_out_DG2 = 1;
            cut_in_loads = 1;
            cut_out_loads = 0;
        }
    }

    state Dg2WithBattery {
        enter {
            Plng_req = eng3_Pmax;
            Pd1_req = Pd1max;
            Pd2_req = PL - Ppv - Pw - Pbat_Pmax - eng3_Pmax - Pd1max;
            Pbat_dis = Pbat_Pmax;
            Pbat_ch = 0.0;
            spare_power = 0.0;
            cut_in_LNG = 1;
            cut_out_LNG = 0;
            cut_in_DG1 = 1;
            cut_out_DG1 = 0;
            cut_in_DG2 = 1;
            cut_out_DG2 = 0;
            cut_in_loads = 1;
            cut_out_loads = 0;
        }
    }

    state Dg2LowSocCharge {
        enter {
            Plng_req = eng3_Pmax;
            Pd1_req = Pd1max;
            Pd2_req = PL - Ppv - Pw + Pd1max / 10 - eng3_Pmax - Pd1max;
            Pbat_dis = 0.0;
            Pbat_ch = Pd1max / 10;
            spare_power = 0.0;
            cut_in_LNG = 1;
            cut_out_LNG = 0;
            cut_in_DG1 = 1;
            cut_out_DG1 = 0;
            cut_in_DG2 = 1;
            cut_out_DG2 = 0;
            cut_in_loads = 1;
            cut_out_loads = 0;
        }
    }

    state OverloadCompletionIllegal {
        enter {
            Plng_req = eng3_Pmax;
            Pd1_req = Pd1max;
            Pd2_req = Pd2max;
            Pbat_dis = PL - Ppv - Pw - eng3_Pmax - Pd1max - Pd2max;
            Pbat_ch = 0.0;
            spare_power = 0.0;
            cut_in_LNG = 1;
            cut_out_LNG = 0;
            cut_in_DG1 = 1;
            cut_out_DG1 = 0;
            cut_in_DG2 = 1;
            cut_out_DG2 = 0;
            cut_in_loads = 1;
            cut_out_loads = 0;
        }
    }
}
```

#### agent-loop 过程与日志路径

| 项 | 值 |
|---|---|
| verdict / status | `success` / `success` |
| failure class | `success` |
| main_result_eligible | `true` |
| path2_ref_model_blueprint | `false`；state_mode_decorative: final DSL is dominated by root-level forced guard reclassification; valid as FE/BVS or dispatch-classifier stress evidence, but not a Path2 ref-model blueprint |
| state_mode_decorative | `true` |
| SC-11 post-accept validation | `✅ 1/1; ❌ 0` |
| executed stages | `SC-0 -> SL-1 -> SD-2 -> SD-3 -> SD-4 -> SL-5 -> SD-5A -> SL-5 -> SD-5A -> SL-5 -> SD-5A -> SC-5F -> SD-6 -> SL-7 -> SD-8 -> SL-9 -> SL-10 -> SC-11 -> SD-2 -> SD-3 -> SD-4 -> SD-5A -> SL-5 -> SD-5A -> SC-5F -> SD-6 -> SD-8 -> SL-9 -> SD-6 -> SL-7 -> SD-2 -> SD-3 -> SD-4 -> SD-5A -> SC-5F -> SD-6 -> SD-8 -> SL-9 -> SD-6 -> SL-7 -> SD-2 -> SD-3 -> SD-4 -> SD-5A -> SC-5F -> SD-6 -> SD-8 -> SL-9 -> SD-6 -> SL-7 -> SD-2 -> SD-3 -> SD-4 -> SD-5A -> SC-5F -> SD-6 -> SD-8 -> SL-9 -> SL-10 -> SC-11 -> SD-2 -> SD-3 -> SD-4 -> SD-5A -> SL-5 -> SD-5A -> SC-5F -> SD-6 -> SL-7 -> SC-12 -> SC-13` |
| iter / repairs / accepted / scenarios | `5` / `5` / `2` / `14` |
| token / elapsed | `{'prompt_tokens': 800496, 'completion_tokens': 62324, 'total_tokens': 862820, 'estimated_prompt_tokens': 753833, 'estimated_completion_tokens': 42541, 'estimated_total_tokens': 796374, 'prompt_chars': 3015303, 'completion_chars': 170144, 'n_calls': 18, 'token_usage_available': True, 'token_usage_unavailable_calls': 0}` / `1252.863s` |
| full stage table | `runs/lg_m1_g_four_after_signature_gate_20260608_052552/pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f/report.md` §4 |
| run record | `runs/lg_m1_g_four_after_signature_gate_20260608_052552/pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f/pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f.agent_loop.json.gz` |
| logs | `runs/lg_m1_g_four_after_signature_gate_20260608_052552/pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f/run_logs/stdout.txt`, `runs/lg_m1_g_four_after_signature_gate_20260608_052552/pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f/run_logs/stderr.txt` |
| checks / repro | `runs/lg_m1_g_four_after_signature_gate_20260608_052552/pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f/checks.json`, `runs/lg_m1_g_four_after_signature_gate_20260608_052552/pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f/reproducibility.json` |

#### LangGraph runtime metadata 摘要（report §1.1 摘录）

| 字段 | 值 |
|---|---|
| `graph_runtime_backend` | `langgraph` |
| `graph_runtime_status` | `enabled` |
| `graph_runtime_backend_version` | `pr-langgraph.stategraph.v1` |
| `langgraph_version` | `1.2.4` |
| `langgraph_checkpoint_version` | `4.1.1` |
| `graph_runtime_id` | `langgraph:pr-langgraph.stategraph.v1` |
| `graph_config_hash` | `sha256:811174be19c7d2f84070f5d6b9601ca160abd0b7f67d61dbfcd0121079d4cba9` |
| `node_edge_schema_version` | `pr-langgraph.stage-nodes.v1` |
| `checkpoint_backend` | `memory` |
| `checkpoint_backend_type` | `InMemorySaver` |
| `checkpoint_serde` | `pickle` |
| `checkpoint_path_hash` | `sha256:memory` |
| `resumed_from_checkpoint` | `False` |
| `resume_checkpoint_id_hash` | `None` |
| `instrumentation_layer` | `langgraph` |
| `stage_semantics_module` | `method.staged_runtime` |
| `langgraph_node_trace_count` | `135` |
| `langgraph_node_trace_hash` | `sha256:4e163fb20d847cd0f4cfa67d5d9dea6697aed9028afbb1338fac7383d14defdf` |
| `langgraph_compat_ok` | `True` |
| `checkpoint_resume_smoke_scope` | `toy_ledger_langgraph_api_smoke` |
| `real_agent_loop_resume_supported` | `False` |
| `resume_append_only` | `True` |
| `final_trace_delegated_monolithic_runtime` | `False` |
| `final_trace_node_trace_count` | `135` |

- checkpoint 口径：This smoke validates LangGraph interrupt/resume API shape and append-only ledger behavior on a minimal FixLog-like state only. It is not evidence that an interrupted real agent-loop run can be resumed for main-result statistics.
- 注意：`real_agent_loop_resume_supported=false` 时，只能宣称 LangGraph checkpoint API / toy FixLog-like ledger smoke 通过；不能把它写成真实 agent-loop 中断恢复已用于主结果统计。

#### 全流程摘要表（report §4 摘录）

| Stage | 是否 LLM | iteration | 结果 | 获取的信息 / 反馈 | 本阶段做了什么 | DSL 修改 | artifact/log |
|---|---:|---:|---:|---|---|---|---|
| `SC-0` | 否 | - | ✅ | trace/control | 初始化 run state | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f.agent_loop.json.gz) |
| `SL-1` | 是 | - | ✅ | LLM calls=1, tokens=15141 | 生成初始 DSL 与 grounding seeds | initial len=7852 | [`record`](./pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=181, info=0; blocking=0, advisory=180, info=0; blocking=0, advisory=180, info=0; blocking=0, advisory=180, info=0; blocking=0, advisory=180, info=0; blocking=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=5, tokens=146283 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=5, tokens=146283 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=5, tokens=146283 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=True, diag=0; ok=False, diag=0; ok=True, diag=0; ok=False, diag=0; ok=True, diag=0; ok=False, diag=0; ok=True, diag=0; ok=False, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f.agent_loop.json.gz) |
| `SL-7` | 是 | 0 | ✅ | LLM calls=5, tokens=285883 | LLM model review | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=5, tokens=362186 | LLM per-request accept/reject + repair | candidate len=7944,0,0,0,7852 | [`record`](./pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=2, tokens=53327 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=181, info=0; blocking=0, advisory=180, info=0; blocking=0, advisory=180, info=0; blocking=0, advisory=180, info=0; blocking=0, advisory=180, info=0; blocking=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=5, tokens=146283 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ⚠️ | ok=True, diag=0; ok=False, diag=0; ok=True, diag=0; ok=False, diag=0; ok=True, diag=0; ok=False, diag=0; ok=True, diag=0; ok=False, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=5, tokens=362186 | LLM per-request accept/reject + repair | candidate len=7944,0,0,0,7852 | [`record`](./pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ⚠️ | ok=True, diag=0; ok=False, diag=0; ok=True, diag=0; ok=False, diag=0; ok=True, diag=0; ok=False, diag=0; ok=True, diag=0; ok=False, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f.agent_loop.json.gz) |
| `SL-7` | 是 | 0 | ✅ | LLM calls=5, tokens=285883 | LLM model review | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=181, info=0; blocking=0, advisory=180, info=0; blocking=0, advisory=180, info=0; blocking=0, advisory=180, info=0; blocking=0, advisory=180, info=0; blocking=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ⚠️ | ok=True, diag=0; ok=False, diag=0; ok=True, diag=0; ok=False, diag=0; ok=True, diag=0; ok=False, diag=0; ok=True, diag=0; ok=False, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=5, tokens=362186 | LLM per-request accept/reject + repair | candidate len=7944,0,0,0,7852 | [`record`](./pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ⚠️ | ok=True, diag=0; ok=False, diag=0; ok=True, diag=0; ok=False, diag=0; ok=True, diag=0; ok=False, diag=0; ok=True, diag=0; ok=False, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f.agent_loop.json.gz) |
| `SL-7` | 是 | 0 | ✅ | LLM calls=5, tokens=285883 | LLM model review | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=181, info=0; blocking=0, advisory=180, info=0; blocking=0, advisory=180, info=0; blocking=0, advisory=180, info=0; blocking=0, advisory=180, info=0; blocking=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ⚠️ | ok=True, diag=0; ok=False, diag=0; ok=True, diag=0; ok=False, diag=0; ok=True, diag=0; ok=False, diag=0; ok=True, diag=0; ok=False, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=5, tokens=362186 | LLM per-request accept/reject + repair | candidate len=7944,0,0,0,7852 | [`record`](./pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ⚠️ | ok=True, diag=0; ok=False, diag=0; ok=True, diag=0; ok=False, diag=0; ok=True, diag=0; ok=False, diag=0; ok=True, diag=0; ok=False, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f.agent_loop.json.gz) |
| `SL-7` | 是 | 0 | ✅ | LLM calls=5, tokens=285883 | LLM model review | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=181, info=0; blocking=0, advisory=180, info=0; blocking=0, advisory=180, info=0; blocking=0, advisory=180, info=0; blocking=0, advisory=180, info=0; blocking=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ⚠️ | ok=True, diag=0; ok=False, diag=0; ok=True, diag=0; ok=False, diag=0; ok=True, diag=0; ok=False, diag=0; ok=True, diag=0; ok=False, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=5, tokens=362186 | LLM per-request accept/reject + repair | candidate len=7944,0,0,0,7852 | [`record`](./pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=2, tokens=53327 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=T
... <truncated 12275 chars in PR comment; see report.md>

#### Scenario 逐轮通过矩阵（report §6.1 摘录）

口径：`✅` = 该 scenario 在该轮 SD-6 simulation 通过；`❌` = 该轮失败；`⚪` = 该轮未执行或无该 scenario 结果。

| Scenario | Intent | Iter 1 | Iter 2 | Iter 3 | Iter 4 | Iter 5 |
|---|---|---|---|---|---|---|
| `default_init_zero_load_charge` | default-init: with PL=0 and SoC below 0.95, EMS should initialize/classify to ZeroLoadCharge and route renewable product...<truncated 24 chars> | ✅ | ✅ | ✅ | ✅ | ✅ |
| `zero_load_soc_threshold_spare` | explicit-hot-start: at the exact SoC 0.95 threshold with PL=0, EMS should send renewable production to spare power rathe...<truncated 16 chars> | ✅ | ✅ | ✅ | ✅ | ✅ |
| `res_covers_charge_below_soc_threshold` | explicit-hot-start: with positive load covered by renewables and SoC just below 0.95, EMS should serve load from RES and...<truncated 38 chars> | ✅ | ✅ | ✅ | ✅ | ✅ |
| `res_covers_spare_at_soc_threshold` | explicit-hot-start: with positive load covered by renewables and SoC at 0.95, EMS should treat residual renewable power ...<truncated 9 chars> | ✅ | ✅ | ✅ | ✅ | ✅ |
| `battery_discharge_at_soc_suitable_boundary` | explicit-hot-start: when RES is below demand, SoC is exactly 0.2, and deficit fits battery capacity, EMS should use batt...<truncated 19 chars> | ✅ | ✅ | ✅ | ✅ | ✅ |
| `lng_with_battery_priority_before_diesel` | explicit-hot-start: with suitable SoC, battery capacity insufficient, and remaining deficit within LNG capacity, EMS sho...<truncated 32 chars> | ✅ | ✅ | ✅ | ✅ | ✅ |
| `lng_low_soc_charge_margin` | explicit-hot-start: with low SoC below 0.2, EMS should avoid battery discharge and add the Pgmax/5 charging margin in th...<truncated 19 chars> | ✅ | ✅ | ✅ | ✅ | ✅ |
| `dg1_with_battery_after_lng_capacity` | explicit-hot-start: with suitable SoC, battery and LNG insufficient but DG1 capacity sufficient, EMS should cut in DG1 w...<truncated 21 chars> | ✅ | ✅ | ✅ | ✅ | ✅ |
| `dg1_low_soc_pd1_margin` | explicit-hot-start: with low SoC, LNG capacity insufficient, and DG1 sufficient after Pd1max/10 margin, EMS should charg...<truncated 22 chars> | ✅ | ✅ | ✅ | ✅ | ✅ |
| `dg2_with_battery_last_priority` | explicit-hot-start: with suitable SoC, battery, LNG, and DG1 insufficient but DG2 sufficient, EMS should cut in DG2 as t...<truncated 27 chars> | ✅ | ✅ | ✅ | ✅ | ✅ |
| `dg2_low_soc_pd1_margin` | explicit-hot-start: with low SoC and demand extending beyond LNG and DG1 after the Pd1max/10 charging margin, EMS should...<truncated 32 chars> | ✅ | ✅ | ✅ | ✅ | ✅ |
| `overload_completion_illegal_extreme_demand` | explicit-hot-start: for extreme demand exceeding all RES and thermal resources, the illegal overload-completion case sho...<truncated 88 chars> | ✅ | ❌ | ❌ | ❌ | ✅ |
| `forced_reclassification_from_zero_spare_to_battery_discharge` | explicit-hot-start: from a concrete ZeroLoadSpare leaf, changing operating conditions to RES-below-load with suitable So...<truncated 131 chars> | ✅ | ✅ | ✅ | ✅ | ✅ |
| `forced_reclassification_from_overload_to_res_spare` | explicit-hot-start: from the concrete illegal overload leaf, a later RES-covered high-SoC condition must be reclassified...<truncated 114 chars> | ✅ | ✅ | ✅ | ✅ | ✅ |
| `forced_reclassification_from_dg2_to_zero_load_charge` | explicit-hot-start: from a concrete Dg2WithBattery leaf, changing to PL=0 with SoC below 0.95 must use the wildcard forc...<truncated 140 chars> | ✅ | ✅ | ✅ | ✅ | ✅ |

#### Repair / blocking feedback 概览（report §7 摘录）

口径：本节记录 agent-loop 真实进入 repair block 后的证据链：FixRequestBatch、SL-9 per-request accept/reject、candidate diff、local-check evidence、SL-10(NL+FixLog) 审阅，以及完整 FixLog ledger 摘录。

| Repair | iteration | accepted | source | blocking diagnostics | SL-9 decisions | SL-10 / local checks | candidate hash |
|---:|---:|---:|---|---|---|---|---|
| 1 | `0` | ✅ | `SL-7` | 0 | accept=1, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none>; local ok=False, target=False, regression=True, drift=minor, local_stage=SD-10, reason=scenario_regression | `sha256:86b140b2c984f57a4a6b8ab1b608ad4875ee49a90e6e5ce5c4a2de7347e7b05d` |
| 2 | `1` | ❌ | `SD-6` | overload_completion_illegal_extreme_demand | accept=0, reject=1, waiver=0 | <none> | `sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 3 | `2` | ❌ | `SD-6` | overload_completion_illegal_extreme_demand | accept=0, reject=1, waiver=0 | <none> | `sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 4 | `3` | ❌ | `SD-6` | overload_completion_illegal_extreme_demand | accept=0, reject=1, waiver=0 | <none> | `sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 5 | `4` | ✅ | `SD-6` | overload_completion_illegal_extreme_demand | accept=1, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=none, rework=<none>; local ok=True, target=True, regression=False, drift=none, local_stage=SD-10, reason= | `sha256:5f773338ae6e3d85f4e4dc198016f6f241f6ec3d2d6e8f2aa8e3c871035ba195` |

> 完整 repair 细节、进入修复原因、SD-8 修改建议、SL-9 candidate、before→candidate diff 与 local-check evidence 与 SL-10 审查证据见 `runs/lg_m1_g_four_after_signature_gate_20260608_052552/pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f/report.md` §7。

</details>
