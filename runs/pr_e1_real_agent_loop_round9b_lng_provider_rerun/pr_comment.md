## PR-E1 Round9B LNG provider-failure 同配置重跑 evidence update

身份：主 session / PR-E1 runner。

这是对 Round9 `path2_lng_ems` 因 `SL-5 provider_error / 502 Bad gateway` 被截断后的同配置重跑。根据已写入 PR body 的 provider/network 上游故障无效原则，Round9 LNG 原始 provider-error run 不进入模型质量/收敛统计；本 comment 使用 Round9B 作为 LNG 的有效方法证据。

### 0. 结论

- 运行配置：`.env` real provider，`config_id=default` / `condition_id=full_staged_v1`，resolved `max_iterations=5`，`llm_max_retries=2`，`scenario_max_retries=2`。
- 本次不再是 provider/network failure：`verdict=not_converged`，`record_status=rejected`，`primary_failure_class=design_or_variable_dynamics`。
- observed `iteration_count=5`，`repair_count=5`，`accepted_repair_count=0`，说明 LNG 与 ABS 一样进入满血修复预算后仍被 SD-4/SD-10 阻断。
- NFRR v3 粗评：T1 diagnostic。模型生成了 12 状态级 EMS 骨架、guard/action 较丰富，但 FE 被 external-input/guard-variable 动态阻断，BVS/SL-7 未触达，不能作为 Path2 ref-model 蓝本。

### 1. 更新后的 LNG 根因

Round9B 证明 LNG 的主要失败不应归因于 provider 502，而是与 ABS 类似：

| 根因 | 证据 | 严重性 |
|---|---|---|
| 外部输入 / 环境输入角色未形成可审计 waiver/role ledger | `PL/Ppv/Pw/SoC/eng3_Pmax/Pgmax/Pd1max` 等均是 EMS 读取的环境/容量输入，但 SD-4/SD-10 仍围绕只读 guard/action 变量反复阻断 | I |
| SL-9 在 RevisedFixPlan 下无法把“只读输入 + 输出 dispatch action”转化为可接受模型边界 | 5 轮 SL-9/SD-10，无 accepted repair | I |
| BVS/SL-7 未触达 | `scenario_history_count=0`，missing `SL-5/SD-6/SL-7/SL-10B` | I |

因此下一轮修复不只针对 ABS，而应普适解决“控制器/监督器读取 plant/sensor/environment/load/capacity 输入，但不写这些输入”的角色记录与 waiver 问题，并继续修 SL-5 default-init oracle。

---

## PR-E1 real-run evidence update

身份：主 session / PR-E1 runner。

本 comment 汇总当前已产出的真实 `method.loop.run_agent_loop` 运行证据；详细报告见仓库内 `runs/pr_e1_real_agent_loop_round9b_lng_provider_rerun/`。

| Path | case | config | verdict | status | clean | eligible | failure class | tokens | report |
|---|---|---|---|---|---:|---:|---|---:|---|
| path2 | `path2_lng_ems` | `default` | `not_converged` | `rejected` | ✅ | ❌ | `design_or_variable_dynamics` | 117104 | `runs/pr_e1_real_agent_loop_round9b_lng_provider_rerun/pr-e1-path2_lng_ems-default-round9blngrerun-7d025aae/report.md` |

### 可复现性边界

- clean commit 绑定：1/1 run 的 `reproducibility.json` 记录 dirty=false。
- prompt snapshot hash 种类：1；用于确认同一轮 4 例是否共享同一 prompt/context 版本。
- 每个 run 的 `reproducibility.json` 保存 git commit、dirty flag、diff hash、prompt file hash、runner command/config 与 source/paper path。

### 初步观察

- `default`：0/1 success，rejected=1，budget_exhausted=0，total_tokens=117104。
- Q1/max_iterations：当前证据未产生 success；若 run 早停于 `rejected`，瓶颈更可能是 prompt/repair candidate quality 或样本变量语义，而不是单纯迭代预算。
- Q1/scenario-review 维度：当前矩阵尚未进入 SL-5/SD-6/SL-7/SL-10B，因此 `scenario_max_retries`、`model_review_mode`、`delta_review_mode` 仍属于未回答问题。
- 主结果候选：当前 0/1 run 可进入 main_result_eligible；其余只能作为 exploratory / infrastructure evidence。

### 主要失败模式

- `design_or_variable_dynamics`：1 run(s)。
- `design_or_variable_dynamics` 与变量只读不写、guard 变量永不变化等风险相关，需在样本筛选和 SL-9 prompt 中区分环境输入变量与内部状态变量。

### 样本筛选观察

- 样本覆盖：1 个 case，Path1=0，Path2=1。
- `path2_lng_ems`：失败/成功类别=design_or_variable_dynamics，最大 observed iteration_count=5。
- 实证筛选更新：若论文变量主要是外部传感/环境输入，应在样本记录中明确“只读输入”身份；若模型需要内部状态变量，则必须有 NL-grounded write/action，否则容易被 SD-4 阻断。

### Reviewer 追加审查项：禁止样本特判 / benchmark overfit

- 后续三路 reviewer 需显式检查 agent-loop / prompt / deterministic policy 是否包含针对 ABS、CARA、Elevator、LNG EMS 或本 PR 4 个样本的 lexical special-case、case_id 分支、hard-coded hint、结果导向参数。
- 允许的优化必须是普适、可解释、可迁移的机制；例如通过 prompt 要求 LLM 区分外部输入与内部状态，而不是在代码中写样本专用词表。
- 若发现样本特判影响 blocking/advisory、repair target、scenario oracle 或主结论归类，应至少按 I 级处理；若污染 main_result_eligible 或论文结论则按 C 级处理。

### 4 例详细输入 / 输出 / artifact

<details><summary>path2 / path2_lng_ems / default / not_converged</summary>

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
def float requested_generator_power = 0.0;
def float battery_power = 0.0;
def float spare_power = 0.0;

state EMS {
    [*] -> ZeroLoadCharge;

    state ZeroLoadCharge {
        enter {
            battery_power = Ppv + Pw;
            spare_power = 0.0;
        }
    }

    state ZeroLoadSpare {
        enter {
            battery_power = 0.0;
            spare_power = Ppv + Pw;
        }
    }

    state RESCoverCharge {
        enter {
            requested_generator_power = 0.0;
            battery_power = (Ppv + Pw) - PL;
            spare_power = 0.0;
        }
    }

    state RESCoverSpare {
        enter {
            requested_generator_power = 0.0;
            battery_power = 0.0;
            spare_power = (Ppv + Pw) - PL;
        }
    }

    state BatteryAssist;

    state LNGSupply {
        enter {
            requested_generator_power = PL - (Ppv + Pw);
        }
    }

    state LNGSupplyLowSoCChargeMargin {
        enter {
            requested_generator_power = (PL - (Ppv + Pw)) + (Pgmax / 5.0);
        }
    }

    state Diesel1Supply;

    state Diesel1LowSoCChargeMargin {
        enter {
            requested_generator_power = (PL - (Ppv + Pw)) + (Pd1max / 10.0);
        }
    }

    state Diesel2Supply;

    state Diesel2LowSoCChargeMargin {
        enter {
            requested_generator_power = (PL - (Ppv + Pw)) + (Pd1max / 10.0);
        }
    }

    state OverloadCompletion {
        enter {
            battery_power = PL;
        }
    }

    ZeroLoadCharge -> ZeroLoadSpare : if [PL == 0.0 && SoC >= 0.95];
    ZeroLoadSpare -> ZeroLoadCharge : if [PL == 0.0 && SoC < 0.95];

    ZeroLoadCharge -> RESCoverCharge : if [PL > 0.0 && (Ppv + Pw) >= PL && SoC < 0.95];
    ZeroLoadCharge -> RESCoverSpare : if [PL > 0.0 && (Ppv + Pw) >= PL && SoC >= 0.95];
    ZeroLoadSpare -> RESCoverCharge : if [PL > 0.0 && (Ppv + Pw) >= PL && SoC < 0.95];
    ZeroLoadSpare -> RESCoverSpare : if [PL > 0.0 && (Ppv + Pw) >= PL && SoC >= 0.95];

    RESCoverCharge -> BatteryAssist : if [(Ppv + Pw) < PL && SoC > 0.20];
    RESCoverSpare -> BatteryAssist : if [(Ppv + Pw) < PL && SoC > 0.20];

    BatteryAssist -> LNGSupply : if [SoC >= 0.20 && PL <= eng3_Pmax];
    BatteryAssist -> LNGSupplyLowSoCChargeMargin : if [SoC < 0.20 && PL <= eng3_Pmax];

    LNGSupply -> Diesel1Supply : if [PL > eng3_Pmax];
    LNGSupplyLowSoCChargeMargin -> Diesel1LowSoCChargeMargin : if [PL > eng3_Pmax];

    Diesel1Supply -> Diesel2Supply : if [PL > eng3_Pmax + Pd1max];
    Diesel1LowSoCChargeMargin -> Diesel2LowSoCChargeMargin : if [PL > eng3_Pmax + Pd1max];

    Diesel2Supply -> OverloadCompletion : if [PL > eng3_Pmax + Pd1max + Pgmax];
    Diesel2LowSoCChargeMargin -> OverloadCompletion : if [PL > eng3_Pmax + Pd1max + Pgmax];

    RESCoverCharge -> ZeroLoadCharge : if [PL == 0.0 && SoC < 0.95];
    RESCoverSpare -> ZeroLoadSpare : if [PL == 0.0 && SoC >= 0.95];
}
```

#### agent-loop 过程与日志路径

| 项 | 值 |
|---|---|
| verdict / status | `not_converged` / `rejected` |
| failure class | `design_or_variable_dynamics` |
| executed stages | `SC-0 -> SL-1 -> SD-2 -> SD-3 -> SD-4 -> SD-8 -> SL-9 -> SD-10 -> SC-11 -> SD-2 -> SD-3 -> SD-4 -> SD-8 -> SL-9 -> SD-10 -> SC-11 -> SD-2 -> SD-3 -> SD-4 -> SD-8 -> SL-9 -> SD-10 -> SC-11 -> SD-2 -> SD-3 -> SD-4 -> SD-8 -> SL-9 -> SD-10 -> SC-11 -> SD-2 -> SD-3 -> SD-4 -> SD-8 -> SL-9 -> SD-10 -> SC-11 -> SC-12 -> SC-13` |
| iter / repairs / accepted / scenarios | `5` / `5` / `0` / `0` |
| token / elapsed | `{'prompt_tokens': 109995, 'completion_tokens': 7109, 'total_tokens': 117104, 'n_calls': 6}` / `422.19s` |
| full stage table | `runs/pr_e1_real_agent_loop_round9b_lng_provider_rerun/pr-e1-path2_lng_ems-default-round9blngrerun-7d025aae/report.md` §4 |
| run record | `runs/pr_e1_real_agent_loop_round9b_lng_provider_rerun/pr-e1-path2_lng_ems-default-round9blngrerun-7d025aae/pr-e1-path2_lng_ems-default-round9blngrerun-7d025aae.agent_loop.json.gz` |
| logs | `runs/pr_e1_real_agent_loop_round9b_lng_provider_rerun/pr-e1-path2_lng_ems-default-round9blngrerun-7d025aae/run_logs/stdout.txt`, `runs/pr_e1_real_agent_loop_round9b_lng_provider_rerun/pr-e1-path2_lng_ems-default-round9blngrerun-7d025aae/run_logs/stderr.txt` |
| checks / repro | `runs/pr_e1_real_agent_loop_round9b_lng_provider_rerun/pr-e1-path2_lng_ems-default-round9blngrerun-7d025aae/checks.json`, `runs/pr_e1_real_agent_loop_round9b_lng_provider_rerun/pr-e1-path2_lng_ems-default-round9blngrerun-7d025aae/reproducibility.json` |

</details>
