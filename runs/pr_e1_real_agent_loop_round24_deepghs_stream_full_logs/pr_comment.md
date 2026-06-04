## PR-E1 real-run evidence update

身份：主 session / PR-E1 runner。

本 comment 汇总当前已产出的真实 `method.loop.run_agent_loop` 运行证据；详细报告见仓库内 `../runs/pr_e1_real_agent_loop_round24_deepghs_stream_full_logs/`。

| Path | case | config | verdict | status | clean | eligible | failure class | tokens | report |
|---|---|---|---|---|---:|---:|---|---:|---|
| path1 | `path1_abs` | `default` | `success` | `success` | ✅ | ✅ | `success` | 0 | `../runs/pr_e1_real_agent_loop_round24_deepghs_stream_full_logs/pr-e1-path1_abs-default-round24deepghsstream-10ff8337/report.md` |
| path1 | `path1_cara` | `default` | `not_converged` | `rejected` | ✅ | ❌ | `model_review_or_quality` | 0 | `../runs/pr_e1_real_agent_loop_round24_deepghs_stream_full_logs/pr-e1-path1_cara-default-round24deepghsstream-1afcc21e/report.md` |
| path1 | `path1_elevator` | `default` | `success` | `success` | ✅ | ✅ | `success` | 0 | `../runs/pr_e1_real_agent_loop_round24_deepghs_stream_full_logs/pr-e1-path1_elevator-default-round24deepghsstream-019c0d50/report.md` |
| path2 | `path2_lng_ems` | `default` | `success` | `success` | ✅ | ✅ | `success` | 0 | `../runs/pr_e1_real_agent_loop_round24_deepghs_stream_full_logs/pr-e1-path2_lng_ems-default-round24deepghsstream-cd202f61/report.md` |

### 可复现性边界

- clean commit 绑定：4/4 run 的 `reproducibility.json` 记录 dirty=false。
- prompt snapshot hash 种类：1；用于确认同一轮 4 例是否共享同一 prompt/context 版本。
- 每个 run 的 `reproducibility.json` 保存 git commit、dirty flag、diff hash、prompt file hash、runner command/config 与 source/paper path。

### 初步观察

- `default`：3/4 success，rejected=1，budget_exhausted=0，total_tokens=0。
- 主结果候选：当前 3/4 run 可进入 main_result_eligible；其余只能作为 exploratory / infrastructure evidence。

### 主要失败模式

- `success`：3 run(s)。
- `model_review_or_quality`：1 run(s)。

### 样本筛选观察

- 样本覆盖：4 个 case，Path1=3，Path2=1。
- `path1_abs`：失败/成功类别=success，最大 observed iteration_count=1。
- `path1_cara`：失败/成功类别=model_review_or_quality，最大 observed iteration_count=1。
- `path1_elevator`：失败/成功类别=success，最大 observed iteration_count=1。
- `path2_lng_ems`：失败/成功类别=success，最大 observed iteration_count=4。

### Reviewer 追加审查项：禁止样本特判 / benchmark overfit

- 后续三路 reviewer 需显式检查 agent-loop / prompt / deterministic policy 是否包含针对 ABS、CARA、Elevator、LNG EMS 或本 PR 4 个样本的 lexical special-case、case_id 分支、hard-coded hint、结果导向参数。
- 允许的优化必须是普适、可解释、可迁移的机制；例如通过 prompt 要求 LLM 区分外部输入与内部状态，而不是在代码中写样本专用词表。
- 若发现样本特判影响 blocking/advisory、repair target、scenario oracle 或主结论归类，应至少按 I 级处理；若污染 main_result_eligible 或论文结论则按 C 级处理。

### 4 例详细输入 / 输出 / artifact

<details><summary>path1 / path1_abs / default / success</summary>

#### NL 输入（原文）

```text
The paper implements the single-wheel ABS hydraulic regulator as a three-state FSM coupled with a PID-based slip controller. Wheel speed and vehicle speed are used to compute the slip ratio, and the PID output drives the Stateflow supervisor instead of sending commands directly to the hydraulic valves.

The FSM contains the states `increase`, `hold`, and `decrease`, where `increase` sets `k1=1, k2=0, n=0`, `hold` neutralizes both valves with `k1=0, k2=0, n=0`, and `decrease` sets `k1=0, k2=1, n=500` to release pressure.

The transition guards split the slip-error space into four bands: `increase -> hold` when `slp <= 0.01`, `hold -> increase` when `slp > 0.01`, `hold -> decrease` when `slp < -0.01`, and `decrease -> hold` when `slp >= -0.01`.

This gives a concrete discrete supervisor that maps slip-error thresholds to inlet-valve, return-valve, and pump actions while the continuous wheel-slip dynamics remain in the plant model.
```

#### NL 输入中文翻译

```text
论文把单轮 ABS 液压调节器实现为一个三状态 FSM，并与基于滑移率的 PID 控制器耦合。轮速与车速用于计算滑移率，PID 输出驱动 Stateflow 监督器，而不是直接发送液压阀命令。

FSM 包含 `increase`、`hold`、`decrease` 三个状态：`increase` 设置 `k1=1, k2=0, n=0`，`hold` 设置 `k1=0, k2=0, n=0`，`decrease` 设置 `k1=0, k2=1, n=500` 以释放压力。

转移 guard 把滑移误差空间分成四个区间：`increase -> hold` 当 `slp <= 0.01`，`hold -> increase` 当 `slp > 0.01`，`hold -> decrease` 当 `slp < -0.01`，`decrease -> hold` 当 `slp >= -0.01`。

这给出了一个具体的离散监督器，把滑移误差阈值映射为进油阀、回油阀与泵动作，而连续轮胎滑移动力学仍留在被控对象模型中。
```

#### FCSTM 输出

```pyfcstm
def float slp = 0.0;
def int k1 = 0;
def int k2 = 0;
def int n = 0;

state ABSHydraulicRegulator {
    [*] -> increase;

    state increase {
        enter {
            k1 = 1;
            k2 = 0;
            n = 0;
        }
    }

    state hold {
        enter {
            k1 = 0;
            k2 = 0;
            n = 0;
        }
    }

    state decrease {
        enter {
            k1 = 0;
            k2 = 1;
            n = 500;
        }
    }

    increase -> hold : if [slp <= 0.01];
    hold -> increase : if [slp > 0.01];
    hold -> decrease : if [slp < -0.01];
    decrease -> hold : if [slp >= -0.01];
}
```

#### agent-loop 过程与日志路径

| 项 | 值 |
|---|---|
| verdict / status | `success` / `success` |
| failure class | `success` |
| executed stages | `SC-0 -> SL-1 -> SD-2 -> SD-3 -> SD-4 -> SL-5 -> SD-5A -> SC-5F -> SD-6 -> SL-7 -> SC-12 -> SC-13` |
| iter / repairs / accepted / scenarios | `1` / `0` / `0` / `1` |
| token / elapsed | `{'prompt_tokens': 0, 'completion_tokens': 0, 'total_tokens': 0, 'prompt_chars': 103473, 'completion_chars': 20956, 'n_calls': 3}` / `126.162s` |
| full stage table | `../runs/pr_e1_real_agent_loop_round24_deepghs_stream_full_logs/pr-e1-path1_abs-default-round24deepghsstream-10ff8337/report.md` §4 |
| run record | `../runs/pr_e1_real_agent_loop_round24_deepghs_stream_full_logs/pr-e1-path1_abs-default-round24deepghsstream-10ff8337/pr-e1-path1_abs-default-round24deepghsstream-10ff8337.agent_loop.json.gz` |
| logs | `../runs/pr_e1_real_agent_loop_round24_deepghs_stream_full_logs/pr-e1-path1_abs-default-round24deepghsstream-10ff8337/run_logs/stdout.txt`, `../runs/pr_e1_real_agent_loop_round24_deepghs_stream_full_logs/pr-e1-path1_abs-default-round24deepghsstream-10ff8337/run_logs/stderr.txt` |
| checks / repro | `../runs/pr_e1_real_agent_loop_round24_deepghs_stream_full_logs/pr-e1-path1_abs-default-round24deepghsstream-10ff8337/checks.json`, `../runs/pr_e1_real_agent_loop_round24_deepghs_stream_full_logs/pr-e1-path1_abs-default-round24deepghsstream-10ff8337/reproducibility.json` |

#### 全流程摘要表（report §4 摘录）

| Stage | 是否 LLM | iteration | 结果 | 获取的信息 / 反馈 | 本阶段做了什么 | DSL 修改 | artifact/log |
|---|---:|---:|---:|---|---|---|---|
| `SC-0` | 否 | - | ✅ | trace/control | 初始化 run state | 无/见 record | [`record`](./pr-e1-path1_abs-default-round24deepghsstream-10ff8337.agent_loop.json.gz) |
| `SL-1` | 是 | - | ✅ | LLM calls=1, tokens=0 | 生成初始 DSL 与 grounding seeds | initial len=623 | [`record`](./pr-e1-path1_abs-default-round24deepghsstream-10ff8337.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_abs-default-round24deepghsstream-10ff8337.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_abs-default-round24deepghsstream-10ff8337.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=8, info=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_abs-default-round24deepghsstream-10ff8337.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=1, tokens=0 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_abs-default-round24deepghsstream-10ff8337.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_abs-default-round24deepghsstream-10ff8337.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_abs-default-round24deepghsstream-10ff8337.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_abs-default-round24deepghsstream-10ff8337.agent_loop.json.gz) |
| `SL-7` | 是 | 0 | ✅ | LLM calls=1, tokens=0 | LLM model review | 无/见 record | [`record`](./pr-e1-path1_abs-default-round24deepghsstream-10ff8337.agent_loop.json.gz) |
| `SC-12` | 否 | - | ✅ | full_pass_all_required_feedback_ok | 写 final verdict | 无/见 record | [`record`](./pr-e1-path1_abs-default-round24deepghsstream-10ff8337.agent_loop.json.gz) |
| `SC-13` | 否 | - | ✅ | trace/control | 写审计 run record | 无/见 record | [`record`](./pr-e1-path1_abs-default-round24deepghsstream-10ff8337.agent_loop.json.gz) |

### 4.1 完整流程日志（stage/control-flow replay ledger）

口径：本节来自 `AgentLoopRunRecord.logs`，与 [`flow_log.json`](./flow_log.json) 一致；用于复现每个 stage 如何进入、得到什么批示、跳转到哪里，以及每次 DSL 产物/候选如何变化。

| # | ts | stage | iter | event | result / jump | DSL evidence |
|---:|---|---|---:|---|---|---|
| 1 | `2026-06-04T02:44:10Z` | `SC-0` | `-` | `run_start` | {} | <none> |
| 2 | `2026-06-04T02:44:10Z` | `SL-1` | `-` | `stage_enter` | {"reason": "initial_modeling_adapter_available"} | <none> |
| 3 | `2026-06-04T02:44:55Z` | `SL-1` | `-` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 4 | `2026-06-04T02:44:55Z` | `SL-1` | `-` | `stage_result` | {"jump": "SD-2", "ok": true} | candidate_dsl:len=623,hash=sha256:0ff533591cd8 |
| 5 | `2026-06-04T02:44:55Z` | `<control>` | `0` | `iteration_enter` | {} | current_hash=sha256:0ff533591cd822e725a61c9195048564db54f5ec98714e77e86d6a4df8c472a9 |
| 6 | `2026-06-04T02:44:55Z` | `<control>` | `0` | `iteration_validation_enter` | {} | dsl:len=623,hash=sha256:0ff533591cd8, current_hash=sha256:0ff533591cd822e725a61c9195048564db54f5ec98714e77e86d6a4df8c472a9 |
| 7 | `2026-06-04T02:44:55Z` | `SD-2` | `0` | `stage_enter` | {"reason": "full_validation_pass"} | <none> |
| 8 | `2026-06-04T02:44:55Z` | `SD-2` | `0` | `stage_result` | {"jump": "SD-3", "ok": true, "status": "StageStatus.OK"} | <none> |
| 9 | `2026-06-04T02:44:55Z` | `SD-3` | `0` | `stage_enter` | {"reason": "SD-2 ok"} | <none> |
| 10 | `2026-06-04T02:44:55Z` | `SD-3` | `0` | `stage_result` | {"jump": "SD-4", "ok": true, "status": "StageStatus.OK"} | <none> |
| 11 | `2026-06-04T02:44:55Z` | `SD-4` | `0` | `stage_enter` | {"reason": "SD-3 ok"} | <none> |
| 12 | `2026-06-04T02:44:55Z` | `SD-4` | `0` | `stage_result` | {"jump": "SL-5", "ok": true, "status": "StageStatus.OK"} | <none> |
| 13 | `2026-06-04T02:44:55Z` | `SL-5` | `0` | `stage_enter` | {"reason": "scenario_set_absent"} | <none> |
| 14 | `2026-06-04T02:45:36Z` | `SL-5` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 15 | `2026-06-04T02:45:36Z` | `SD-5A` | `0` | `stage_result` | {"jump": "SC-5F", "ok": true, "status": "StageStatus.OK"} | <none> |
| 16 | `2026-06-04T02:45:36Z` | `SC-5F` | `0` | `stage_result` | {"jump": "SD-6", "ok": true} | <none> |
| 17 | `2026-06-04T02:45:36Z` | `SD-6` | `0` | `stage_enter` | {"reason": "scenario_set_ready"} | <none> |
| 18 | `2026-06-04T02:45:36Z` | `SD-6` | `0` | `stage_result` | {"jump": "SL-7", "ok": true, "status": "StageStatus.OK"} | <none> |
| 19 | `2026-06-04T02:45:36Z` | `SL-7` | `0` | `stage_enter` | {"reason": "SD-6 ok"} | <none> |
| 20 | `2026-06-04T02:46:16Z` | `SL-7` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 21 | `2026-06-04T02:46:16Z` | `SL-7` | `0` | `stage_result` | {"jump": "SC-12 success", "ok": true, "status": "StageStatus.OK"} | <none> |
| 22 | `2026-06-04T02:46:16Z` | `SL-7` | `0` | `grounding_update_hints_recorded` | {} | <none> |
| 23 | `2026-06-04T02:46:16Z` | `<control>` | `0` | `iteration_validation_result` | {"jump": "SC-12 success", "selected_feedback": null} | <none> |
| 24 | `2026-06-04T02:46:16Z` | `SC-12` | `-` | `sc12_verdict` | {"reason": "full_pass_all_required_feedback_ok", "verdict": "success"} | final_dsl:len=623,hash=sha256:0ff533591cd8 |
| 25 | `2026-06-04T02:46:16Z` | `SC-13` | `-` | `run_end` | {"verdict": "success"} | final_dsl:len=623,hash=sha256:0ff533591cd8 |

#### Scenario 逐轮通过矩阵（report §6.1 摘录）

口径：`✅` = 该 scenario 在该轮 SD-6 simulation 通过；`❌` = 该轮失败；`⚪` = 该轮未执行或无该 scenario 结果。

| Scenario | Intent | Iter 1 |
|---|---|---|
| `default_init_enters_increase` | default-init verifies the initial transition enters increase and applies the increase valve and pump outputs | ✅ |
| `increase_to_hold_at_positive_boundary` | explicit-hot-start probes increase -> hold exactly at slp=0.01 and checks hold neutralizes both valves | ✅ |
| `increase_stays_above_positive_boundary` | explicit-hot-start no-fire probe verifies increase does not transition to hold when slp is just above 0.01 | ✅ |
| `hold_to_increase_above_positive_boundary` | explicit-hot-start probes hold -> increase when slp is greater than 0.01 and checks increase output commands | ✅ |
| `hold_stays_at_positive_boundary` | explicit-hot-start boundary no-fire probe verifies hold does not transition to increase at slp=0.01 | ✅ |
| `hold_to_decrease_below_negative_boundary` | explicit-hot-start probes hold -> decrease when slp is less than -0.01 and checks pressure-release outputs | ✅ |
| `hold_stays_at_negative_boundary` | explicit-hot-start boundary no-fire probe verifies hold does not transition to decrease at slp=-0.01 | ✅ |
| `decrease_to_hold_at_negative_boundary` | explicit-hot-start probes decrease -> hold exactly at slp=-0.01 and checks hold neutralizes pressure-release outputs | ✅ |
| `decrease_stays_below_negative_boundary` | explicit-hot-start no-fire probe verifies decrease does not transition to hold when slp is just below -0.01 | ✅ |

#### Repair / blocking feedback 概览（report §7 摘录）

- 本 run 未进入 `SD-8/SL-9/SL-10` repair block；通常表示流程在 repair 前已成功、被 provider/schema 错误中断，或在 pre-repair 阶段直接退出。

### 8. 尝试记录与成本

- `SL-1`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 2220, 'completion_chars': 7546, 'completion_tokens': 0, 'elapsed_seconds': 44.84681225499662, 'first_chunk_seconds': 5.093303221001406, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 24733, 'prompt_tokens': 0, 'stream': True, 'total_tokens': 0}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1613, 'completion_chars': 5978, 'completion_tokens': 0, 'elapsed_seconds': 41.132566328000394, 'first_chunk_seconds': 12.516240073993686, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 39413, 'prompt_tokens': 0, 'stream': True, 'total_tokens': 0}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-7`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1639, 'completion_chars': 7432, 'completion_tokens': 0, 'elapsed_seconds': 39.703866252995795, 'first_chunk_seconds': 10.100131073006196, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 39327, 'prompt_tokens': 0, 'stream': True, 'total_tokens': 0}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。

### 9. 最终停止状态与后续含义

- 停止状态：verdict=`success`，record_status=`success`。
- 主要原因分类：`success`。
- required stages executed：`12/12`，missing=`<none>`。
- repairs：`0/0` accepted；scenario_history=`1`。
- 配置含义：`recommended baseline candidate`；该结果可用于评估默认入口本身。
- 样本含义：若出现 `design_or_variable_dynamics`，应重点审查变量是否仅作为 guard/input 常量而没有事件/动作更新；若出现 pre-scenario parse/semantic 失败，则应先优化 pyfcstm grammar adherence。

> 完整 repair 细节、进入修复原因、SD-8 修改建议、SL-9 candidate、before→candidate diff 与 local-check evidence 与 SL-10 审查证据见 `../runs/pr_e1_real_agent_loop_round24_deepghs_stream_full_logs/pr-e1-path1_abs-default-round24deepghsstream-10ff8337/report.md` §7。

</details>

<details><summary>path1 / path1_cara / default / not_converged</summary>

#### NL 输入（原文）

```text
At run time, CARA coordinates the Caregiver Interface, Blood Pressure Monitor, Algorithm, and Pump Monitors around an infusion pump that moves fluid into the patient, while sensor readings are stored in a shared buffer for software access. The pump has manual and autocontrol modes. In manual mode, pump speed is set with the built-in switch and the caregiver sets a default flow rate directly on the pump for manual operation, while in autocontrol mode pump speed is set by a control voltage from an external source. The Algorithm component controls infusion rate and records infusion-related data in log files; patient blood pressure is used to compute the infusion rate, with higher pressure producing a lower flow rate. The Caregiver Interface lets the caregiver modify target blood pressure and initiate or terminate algorithmic pump control, and it also displays and sounds error messages. In the Mode_Control_Algorithm hierarchy, CARA has manual and autocontrol-related mode-control states plus an Ask_StartAC submode; within Ask_StartAC, the setpoint can be changed and pressing StartAC enters AutocontrolInit. During normal autocontrol, CARA controls flow rate only while there are no pump-operation complications. If a pump fault such as fluid-tubing occlusion occurs, the pump activates alarm signals, the caregiver removes the fault, and when CARA was controlling the pump the software releases control. As a cross-component fallback, CA_backManual or any of CB_backManual, CP_backManual, or CC_backManual causes CA_mode to become Manual, making manual operation the shared recovery target.
```

#### NL 输入中文翻译

```text
运行时，CARA 围绕一台向患者输液的输液泵协调 Caregiver Interface、Blood Pressure Monitor、Algorithm 与 Pump Monitors，传感器读数会写入共享缓冲区供软件访问。泵具有手动和自动控制两种模式。手动模式下，泵速由内置开关设置，护理人员直接在泵上设置默认流量；自动控制模式下，泵速由外部控制电压设置。Algorithm 组件控制输液速率并记录输液相关日志；患者血压用于计算输液速率，血压越高流量越低。Caregiver Interface 允许护理人员修改目标血压，并启动或终止算法泵控制，同时显示和发出错误消息。在 Mode_Control_Algorithm 层次中，CARA 具有手动与自动控制相关的模式控制状态以及 Ask_StartAC 子模式；在 Ask_StartAC 中可以修改设定点，按下 StartAC 会进入 AutocontrolInit。正常自动控制期间，只有没有泵操作并发症时 CARA 才控制流量。如果出现输液管堵塞等泵故障，泵会激活报警信号，护理人员排除故障；当 CARA 正在控制泵时，软件会释放控制。作为跨组件回退，CA_backManual 或 CB_backManual、CP_backManual、CC_backManual 中任一事件都会使 CA_mode 变为 Manual，使手动操作成为共享恢复目标。
```

#### FCSTM 输出

```pyfcstm
def float blood_pressure = 0.0;
def float shared_bp_buffer = 0.0;
def float target_bp = 0.0;
def float requested_target_bp = 0.0;
def float flow_rate = 0.0;
def float default_flow_rate = 0.0;
def float manual_switch_speed = 0.0;
def float pump_speed = 0.0;
def float control_voltage = 0.0;
def int CA_mode = 0;
def int software_control = 0;
def int pump_fault = 0;
def int alarm_active = 0;
def int log_count = 0;

state CARA {
    [*] -> Mode_Control_Algorithm;

    state Mode_Control_Algorithm {
        ! * -> Manual :: CA_backManual;
        ! * -> Manual :: CB_backManual;
        ! * -> Manual :: CP_backManual;
        ! * -> Manual :: CC_backManual;
        ! * -> Manual :: TerminateAC;

        [*] -> Manual;

        state Manual {
            enter {
                CA_mode = 0;
                software_control = 0;
                alarm_active = 0;
                pump_fault = 0;
                flow_rate = default_flow_rate;
                pump_speed = manual_switch_speed;
                control_voltage = 0.0;
            }
            during {
                flow_rate = default_flow_rate;
                pump_speed = manual_switch_speed;
            }
        }

        state Ask_StartAC;

        state AutocontrolInit {
            enter {
                CA_mode = 1;
                software_control = 1;
                shared_bp_buffer = blood_pressure;
            }
        }

        state AutocontrolNormal {
            enter {
                CA_mode = 1;
                software_control = 1;
            }
            during {
                shared_bp_buffer = blood_pressure;
                if [pump_fault == 0] {
                    flow_rate = target_bp - blood_pressure;
                    control_voltage = flow_rate;
                    log_count = log_count + 1;
                }
            }
        }

        state PumpFault {
            enter {
                pump_fault = 1;
                alarm_active = 1;
                software_control = 0;
                control_voltage = 0.0;
            }
        }

        Manual -> Ask_StartAC :: InitiateAC;
        Ask_StartAC -> Ask_StartAC :: ChangeSetpoint effect { target_bp = requested_target_bp; };
        Ask_StartAC -> AutocontrolInit :: StartAC;
        AutocontrolInit -> AutocontrolNormal;
        AutocontrolNormal -> PumpFault :: PumpFault;
        PumpFault -> Manual :: FaultRemoved;
    }
}
```

#### agent-loop 过程与日志路径

| 项 | 值 |
|---|---|
| verdict / status | `not_converged` / `rejected` |
| failure class | `model_review_or_quality` |
| executed stages | `SC-0 -> SL-1 -> SD-2 -> SD-3 -> SD-4 -> SL-5 -> SD-5A -> SC-5F -> SD-6 -> SL-7 -> SD-8 -> SL-9 -> SL-10 -> SL-9 -> SL-10 -> SL-9 -> SL-10 -> SL-9 -> SL-10 -> SL-9 -> SL-10 -> SC-12 -> SC-13` |
| iter / repairs / accepted / scenarios | `1` / `5` / `0` / `1` |
| token / elapsed | `{'prompt_tokens': 0, 'completion_tokens': 0, 'total_tokens': 0, 'prompt_chars': 791966, 'completion_chars': 81641, 'n_calls': 13}` / `539.059s` |
| full stage table | `../runs/pr_e1_real_agent_loop_round24_deepghs_stream_full_logs/pr-e1-path1_cara-default-round24deepghsstream-1afcc21e/report.md` §4 |
| run record | `../runs/pr_e1_real_agent_loop_round24_deepghs_stream_full_logs/pr-e1-path1_cara-default-round24deepghsstream-1afcc21e/pr-e1-path1_cara-default-round24deepghsstream-1afcc21e.agent_loop.json.gz` |
| logs | `../runs/pr_e1_real_agent_loop_round24_deepghs_stream_full_logs/pr-e1-path1_cara-default-round24deepghsstream-1afcc21e/run_logs/stdout.txt`, `../runs/pr_e1_real_agent_loop_round24_deepghs_stream_full_logs/pr-e1-path1_cara-default-round24deepghsstream-1afcc21e/run_logs/stderr.txt` |
| checks / repro | `../runs/pr_e1_real_agent_loop_round24_deepghs_stream_full_logs/pr-e1-path1_cara-default-round24deepghsstream-1afcc21e/checks.json`, `../runs/pr_e1_real_agent_loop_round24_deepghs_stream_full_logs/pr-e1-path1_cara-default-round24deepghsstream-1afcc21e/reproducibility.json` |

#### 全流程摘要表（report §4 摘录）

| Stage | 是否 LLM | iteration | 结果 | 获取的信息 / 反馈 | 本阶段做了什么 | DSL 修改 | artifact/log |
|---|---:|---:|---:|---|---|---|---|
| `SC-0` | 否 | - | ✅ | trace/control | 初始化 run state | 无/见 record | [`record`](./pr-e1-path1_cara-default-round24deepghsstream-1afcc21e.agent_loop.json.gz) |
| `SL-1` | 是 | - | ✅ | LLM calls=1, tokens=0 | 生成初始 DSL 与 grounding seeds | initial len=2418 | [`record`](./pr-e1-path1_cara-default-round24deepghsstream-1afcc21e.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_cara-default-round24deepghsstream-1afcc21e.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_cara-default-round24deepghsstream-1afcc21e.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=21, info=1 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_cara-default-round24deepghsstream-1afcc21e.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=1, tokens=0 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-round24deepghsstream-1afcc21e.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-round24deepghsstream-1afcc21e.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_cara-default-round24deepghsstream-1afcc21e.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_cara-default-round24deepghsstream-1afcc21e.agent_loop.json.gz) |
| `SL-7` | 是 | 0 | ✅ | LLM calls=1, tokens=0 | LLM model review | 无/见 record | [`record`](./pr-e1-path1_cara-default-round24deepghsstream-1afcc21e.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path1_cara-default-round24deepghsstream-1afcc21e.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=5, tokens=0 | LLM per-request accept/reject + repair | candidate len=2447,2675,2695,2675,2675 | [`record`](./pr-e1-path1_cara-default-round24deepghsstream-1afcc21e.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=5, tokens=0 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-round24deepghsstream-1afcc21e.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=5, tokens=0 | LLM per-request accept/reject + repair | candidate len=2447,2675,2695,2675,2675 | [`record`](./pr-e1-path1_cara-default-round24deepghsstream-1afcc21e.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ⚠️ | LLM calls=5, tokens=0 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-round24deepghsstream-1afcc21e.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=5, tokens=0 | LLM per-request accept/reject + repair | candidate len=2447,2675,2695,2675,2675 | [`record`](./pr-e1-path1_cara-default-round24deepghsstream-1afcc21e.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ⚠️ | LLM calls=5, tokens=0 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-round24deepghsstream-1afcc21e.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=5, tokens=0 | LLM per-request accept/reject + repair | candidate len=2447,2675,2695,2675,2675 | [`record`](./pr-e1-path1_cara-default-round24deepghsstream-1afcc21e.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ⚠️ | LLM calls=5, tokens=0 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-round24deepghsstream-1afcc21e.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=5, tokens=0 | LLM per-request accept/reject + repair | candidate len=2447,2675,2695,2675,2675 | [`record`](./pr-e1-path1_cara-default-round24deepghsstream-1afcc21e.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ⚠️ | LLM calls=5, tokens=0 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-round24deepghsstream-1afcc21e.agent_loop.json.gz) |
| `SC-12` | 否 | - | ⚠️ | SL-7 model review blocked candidate | 写 final verdict | 无/见 record | [`record`](./pr-e1-path1_cara-default-round24deepghsstream-1afcc21e.agent_loop.json.gz) |
| `SC-13` | 否 | - | ✅ | trace/control | 写审计 run record | 无/见 record | [`record`](./pr-e1-path1_cara-default-round24deepghsstream-1afcc21e.agent_loop.json.gz) |

### 4.1 完整流程日志（stage/control-flow replay ledger）

口径：本节来自 `AgentLoopRunRecord.logs`，与 [`flow_log.json`](./flow_log.json) 一致；用于复现每个 stage 如何进入、得到什么批示、跳转到哪里，以及每次 DSL 产物/候选如何变化。

| # | ts | stage | iter | event | result / jump | DSL evidence |
|---:|---|---|---:|---|---|---|
| 1 | `2026-06-04T02:44:10Z` | `SC-0` | `-` | `run_start` | {} | <none> |
| 2 | `2026-06-04T02:44:10Z` | `SL-1` | `-` | `stage_enter` | {"reason": "initial_modeling_adapter_available"} | <none> |
| 3 | `2026-06-04T02:46:02Z` | `SL-1` | `-` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 4 | `2026-06-04T02:46:02Z` | `SL-1` | `-` | `stage_result` | {"jump": "SD-2", "ok": true} | candidate_dsl:len=2418,hash=sha256:ecb9bdac24ae |
| 5 | `2026-06-04T02:46:02Z` | `<control>` | `0` | `iteration_enter` | {} | current_hash=sha256:ecb9bdac24ae47785ee8d47eeb8a8609d691ab33bf9e24653c21a3c50ce71850 |
| 6 | `2026-06-04T02:46:02Z` | `<control>` | `0` | `iteration_validation_enter` | {} | dsl:len=2418,hash=sha256:ecb9bdac24ae, current_hash=sha256:ecb9bdac24ae47785ee8d47eeb8a8609d691ab33bf9e24653c21a3c50ce71850 |
| 7 | `2026-06-04T02:46:02Z` | `SD-2` | `0` | `stage_enter` | {"reason": "full_validation_pass"} | <none> |
| 8 | `2026-06-04T02:46:02Z` | `SD-2` | `0` | `stage_result` | {"jump": "SD-3", "ok": true, "status": "StageStatus.OK"} | <none> |
| 9 | `2026-06-04T02:46:02Z` | `SD-3` | `0` | `stage_enter` | {"reason": "SD-2 ok"} | <none> |
| 10 | `2026-06-04T02:46:03Z` | `SD-3` | `0` | `stage_result` | {"jump": "SD-4", "ok": true, "status": "StageStatus.OK"} | <none> |
| 11 | `2026-06-04T02:46:03Z` | `SD-4` | `0` | `stage_enter` | {"reason": "SD-3 ok"} | <none> |
| 12 | `2026-06-04T02:46:03Z` | `SD-4` | `0` | `stage_result` | {"jump": "SL-5", "ok": true, "status": "StageStatus.OK"} | <none> |
| 13 | `2026-06-04T02:46:03Z` | `SL-5` | `0` | `stage_enter` | {"reason": "scenario_set_absent"} | <none> |
| 14 | `2026-06-04T02:47:10Z` | `SL-5` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 15 | `2026-06-04T02:47:10Z` | `SD-5A` | `0` | `stage_result` | {"jump": "SC-5F", "ok": true, "status": "StageStatus.OK"} | <none> |
| 16 | `2026-06-04T02:47:10Z` | `SC-5F` | `0` | `stage_result` | {"jump": "SD-6", "ok": true} | <none> |
| 17 | `2026-06-04T02:47:10Z` | `SD-6` | `0` | `stage_enter` | {"reason": "scenario_set_ready"} | <none> |
| 18 | `2026-06-04T02:47:10Z` | `SD-6` | `0` | `stage_result` | {"jump": "SL-7", "ok": true, "status": "StageStatus.OK"} | <none> |
| 19 | `2026-06-04T02:47:10Z` | `SL-7` | `0` | `stage_enter` | {"reason": "SD-6 ok"} | <none> |
| 20 | `2026-06-04T02:48:01Z` | `SL-7` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 21 | `2026-06-04T02:48:01Z` | `SL-7` | `0` | `stage_result` | {"jump": "SD-8", "ok": false, "status": "StageStatus.OK"} | <none> |
| 22 | `2026-06-04T02:48:01Z` | `SL-7` | `0` | `grounding_update_hints_recorded` | {} | <none> |
| 23 | `2026-06-04T02:48:01Z` | `<control>` | `0` | `iteration_validation_result` | {"jump": "SD-8 repair", "selected_feedback": {"blocking": true, "blocking_findings": [{"category": "unsafe_recovery", "evidence": ["NL: \"If a pump fault such as fluid-tubing occlusion occurs, the pump activates alarm signals, the caregiver removes the fault...\"", "DSL: `! * -> Manual :: CP_backManual;` and other forced `*_backManual` transitions target `Manual` from any state.", "DSL: `Manual.enter` sets `alarm_act...<truncated 1338 chars> | <none> |
| 24 | `2026-06-04T02:48:01Z` | `SD-8` | `0` | `repair_path_enter` | {"jump": "SD-8", "selected_feedback": {"blocking": true, "blocking_findings": [{"category": "unsafe_recovery", "evidence": ["NL: \"If a pump fault such as fluid-tubing occlusion occurs, the pump activates alarm signals, the caregiver removes the fault...\"", "DSL: `! * -> Manual :: CP_backManual;` and other forced `*_backManual` transitions target `Manual` from any state.", "DSL: `Manual.enter` sets `alarm_active = 0...<truncated 1331 chars> | current_dsl:len=2418,hash=sha256:ecb9bdac24ae |
| 25 | `2026-06-04T02:48:01Z` | `SD-8` | `0` | `stage_result` | {"jump": "SL-9", "ok": true, "status": "StageStatus.OK"} | <none> |
| 26 | `2026-06-04T02:48:01Z` | `SD-8` | `0` | `fix_request_batch` | {"request_count": 2} | <none> |
| 27 | `2026-06-04T02:48:01Z` | `SL-9` | `0` | `stage_enter` | {"reason": "fix_requests_ready"} | old_dsl:len=2418,hash=sha256:ecb9bdac24ae |
| 28 | `2026-06-04T02:48:29Z` | `SL-9` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 29 | `2026-06-04T02:48:29Z` | `SL-9` | `0` | `stage_result` | {"accepted_request_ids": ["fixreq-0-sl7-0-be1e03bda7", "fixreq-0-sl7-1-23c6ba7ffb"], "jump": "SL-10", "ok": true, "rejected_request_ids": []} | candidate_dsl:len=2447,hash=sha256:0ff4eb8e59c1 |
| 30 | `2026-06-04T02:48:29Z` | `SD-10` | `0` | `stage_result` | {"jump": "SL-10", "ok": false, "status": "StageStatus.FAIL"} | <none> |
| 31 | `2026-06-04T02:48:29Z` | `SL-10` | `0` | `stage_enter` | {"reason": "candidate_dsl_and_local_evidence_ready"} | candidate_hash=sha256:0ff4eb8e59c1879f13730e20b7a84f2fb44173c11e58725f0a10aa7c984190b2 |
| 32 | `2026-06-04T02:49:13Z` | `SL-10` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 33 | `2026-06-04T02:49:13Z` | `SL-10` | `0` | `stage_result` | {"decision": "rework", "jump": "SL-9 rework", "ok": false} | <none> |
| 34 | `2026-06-04T02:49:13Z` | `SL-10` | `0` | `grounding_update_hints_recorded` | {} | <none> |
| 35 | `2026-06-04T02:49:13Z` | `SL-9` | `0` | `stage_enter` | {"reason": "sl10_rework_locked"} | old_dsl:len=2418,hash=sha256:ecb9bdac24ae |
| 36 | `2026-06-04T02:49:45Z` | `SL-9` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 37 | `2026-06-04T02:49:45Z` | `SL-9` | `0` | `stage_result` | {"accepted_request_ids": ["fixreq-0-sl7-0-be1e03bda7", "fixreq-0-sl7-1-23c6ba7ffb"], "jump": "SL-10", "ok": true, "rejected_request_ids": []} | candidate_dsl:len=2675,hash=sha256:0cb3a6242da5 |
| 38 | `2026-06-04T02:49:45Z` | `SD-10` | `0` | `stage_result` | {"jump": "SL-10", "ok": false, "status": "StageStatus.FAIL"} | <none> |
| 39 | `2026-06-04T02:49:45Z` | `SL-10` | `0` | `stage_enter` | {"reason": "candidate_dsl_and_local_evidence_ready"} | candidate_hash=sha256:0cb3a6242da518a08dc9d589109a92d71820925223a1771083859adff4b74c04 |
| 40 | `2026-06-04T02:50:09Z` | `SL-10` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 41 | `2026-06-04T02:50:09Z` | `SL-10` | `0` | `stage_result` | {"decision": "rework", "jump": "SL-9 rework", "ok": false} | <none> |
| 42 | `2026-06-04T02:50:09Z` | `SL-10` | `0` | `grounding_update_hints_recorded` | {} | <none> |
| 43 | `2026-06-04T02:50:09Z` | `SL-9` | `0` | `stage_enter` | {"reason": "sl10_rework_locked"} | old_dsl:len=2418,hash=sha256:ecb9bdac24ae |
| 44 | `2026-06-04T02:50:43Z` | `SL-9` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 45 | `2026-06-04T02:50:43Z` | `SL-9` | `0` | `stage_result` | {"accepted_request_ids": ["fixreq-0-sl7-0-be1e03bda7", "fixreq-0-sl7-1-23c6ba7ffb"], "jump": "SL-10", "ok": true, "rejected_request_ids": []} | candidate_dsl:len=2695,hash=sha256:99b0a326ebee |
| 46 | `2026-06-04T02:50:43Z` | `SD-10` | `0` | `stage_result` | {"jump": "SL-10", "ok": false, "status": "StageStatus.FAIL"} | <none> |
| 47 | `2026-06-04T02:50:43Z` | `SL-10` | `0` | `stage_enter` | {"reason": "candidate_dsl_and_local_evidence_ready"} | candidate_hash=sha256:99b0a326ebeea9465293f0e2db1a3b73061d351cb6e6d73b9fddc25f2ec1a5c7 |
| 48 | `2026-06-04T02:51:10Z` | `SL-10` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 49 | `2026-06-04T02:51:10Z` | `SL-10` | `0` | `stage_result` | {"decision": "rework", "jump": "SL-9 rework", "ok": false} | <none> |
| 50 | `2026-06-04T02:51:10Z` | `SL-9` | `0` | `stage_enter` | {"reason": "sl10_rework_locked"} | old_dsl:len=2418,hash=sha256:ecb9bdac24ae |
| 51 | `2026-06-04T02:51:43Z` | `SL-9` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 52 | `2026-06-04T02:51:43Z` | `SL-9` | `0` | `stage_result` | {"accepted_request_ids": ["fixreq-0-sl7-0-be1e03bda7", "fixreq-0-sl7-1-23c6ba7ffb"], "jump": "SL-10", "ok": true, "rejected_request_ids": []} | candidate_dsl:len=2675,hash=sha256:0cb3a6242da5 |
| 53 | `2026-06-04T02:51:43Z` | `SD-10` | `0` | `stage_result` | {"jump": "SL-10", "ok": false, "status": "StageStatus.FAIL"} | <none> |
| 54 | `2026-06-04T02:51:43Z` | `SL-10` | `0` | `stage_enter` | {"reason": "candidate_dsl_and_local_evidence_ready"} | candidate_hash=sha256:0cb3a6242da518a08dc9d589109a92d71820925223a1771083859adff4b74c04 |
| 55 | `2026-06-04T02:52:07Z` | `SL-10` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 56 | `2026-06-04T02:52:07Z` | `SL-10` | `0` | `stage_result` | {"decision": "rework", "jump": "SL-9 rework", "ok": false} | <none> |
| 57 | `2026-06-04T02:52:07Z` | `SL-9` | `0` | `stage_enter` | {"reason": "sl10_rework_locked"} | old_dsl:len=2418,hash=sha256:ecb9bdac24ae |
| 58 | `2026-06-04T02:52:39Z` | `SL-9` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 59 | `2026-06-04T02:52:39Z` | `SL-9` | `0` | `stage_result` | {"accepted_request_ids": ["fixreq-0-sl7-0-be1e03bda7", "fixreq-0-sl7-1-23c6ba7ffb"], "jump": "SL-10", "ok": true, "rejected_request_ids": []} | candidate_dsl:len=2675,hash=sha256:0cb3a6242da5 |
| 60 | `2026-06-04T02:52:39Z` | `SD-10` | `0` | `stage_result` | {"jump": "SL-10", "ok": false, "status": "StageStatus.FAIL"} | <none> |
| 61 | `2026-06-04T02:52:39Z` | `SL-10` | `0` | `stage_enter` | {"reason": "candidate_dsl_and_local_evidence_ready"} | candidate_hash=sha256:0cb3a6242da518a08dc9d589109a92d71820925223a1771083859adff4b74c04 |
| 62 | `2026-06-04T02:53:09Z` | `SL-10` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 63 | `2026-06-04T02:53:09Z` | `SL-10` | `0` | `stage_result` | {"decision": "rework", "jump": "SC-12 rejected", "ok": false} | <none> |
| 64 | `2026-06-04T02:53:09Z` | `<control>` | `0` | `iteration_repair_result` | {"accepted": false, "jump": "SC-12 or retry"} | current_hash=sha256:ecb9bdac24ae47785ee8d47eeb8a8609d691ab33bf9e24653c21a3c50ce71850 |
| 65 | `2026-06-04T02:53:09Z` | `SC-12` | `-` | `sc12_verdict` | {"reason": "SL-7 model review blocked candidate", "verdict": "not_converged"} | final_dsl:len=2418,hash=sha256:ecb9bdac24ae |
| 66 | `2026-06-04T02:53:09Z` | `SC-13` | `-` | `run_end` | {"verdict":
... <truncated 64 chars in PR comment; see report.md>

#### Scenario 逐轮通过矩阵（report §6.1 摘录）

口径：`✅` = 该 scenario 在该轮 SD-6 simulation 通过；`❌` = 该轮失败；`⚪` = 该轮未执行或无该 scenario 结果。

| Scenario | Intent | Iter 1 |
|---|---|---|
| `default_initial_manual_outputs` | default-init dispatches into Manual and applies manual operation outputs from the caregiver-set default flow and built-i...<truncated 15 chars> | ✅ |
| `initiate_change_start_to_normal_autocontrol` | explicit-hot-start from Manual probes InitiateAC, Ask_StartAC setpoint change, StartAC into AutocontrolInit, and automat...<truncated 37 chars> | ✅ |
| `pump_fault_alarm_release_then_fault_removed_manual` | explicit-hot-start from AutocontrolNormal probes pump fault handling, alarm activation, software-control release, and ca...<truncated 41 chars> | ✅ |
| `forced_ca_backmanual_from_ask_startac` | explicit-hot-start from Ask_StartAC probes CA_backManual as a cross-component fallback to Manual recovery. | ✅ |
| `forced_cb_backmanual_from_autocontrol_normal` | explicit-hot-start from AutocontrolNormal probes CB_backManual as a cross-component fallback to Manual recovery. | ✅ |
| `forced_cp_backmanual_from_pump_fault` | explicit-hot-start from PumpFault probes CP_backManual as a cross-component fallback that clears alarm/fault indicators ...<truncated 19 chars> | ✅ |
| `forced_cc_backmanual_from_autocontrol_init` | explicit-hot-start from AutocontrolInit probes CC_backManual as a cross-component fallback to Manual recovery before nor...<truncated 23 chars> | ✅ |
| `terminate_ac_from_autocontrol_normal` | explicit-hot-start from AutocontrolNormal probes caregiver termination of algorithmic pump control back to Manual. | ✅ |

#### Repair / blocking feedback 概览（report §7 摘录）

口径：本节记录 agent-loop 真实进入 repair block 后的证据链：FixRequestBatch、SL-9 per-request accept/reject、candidate diff、local-check evidence、SL-10(NL+FixLog) 审阅，以及完整 FixLog ledger 摘录。

| Repair | iteration | accepted | source | blocking diagnostics | SL-9 decisions | SL-10 / local checks | candidate hash |
|---:|---:|---:|---|---|---|---|---|
| 1 | `0` | ❌ | `SL-7` | 0, 1 | accept=2, reject=0, waiver=0 | SL-10 decision=rework, ok=False, target=False, regression=True, drift=major, rework=Keep the accepted autocontrol repair: retain `pump_speed = control_voltage` in `AutocontrolNormal.during` after `control_voltage = flow_rate`., Do not restore unconditional `pu...<truncated 265 chars> | `sha256:0ff4eb8e59c1879f13730e20b7a84f2fb44173c11e58725f0a10aa7c984190b2` |
| 2 | `0` | ❌ | `SL-7` | 0, 1 | accept=2, reject=0, waiver=0 | SL-10 decision=rework, ok=False, target=True, regression=False, drift=minor, rework=SL-10 pass was downgraded because local deterministic evidence reported major drift and SL-10 evidence did not explicitly address the local rejection reason/kind with a structu...<truncated 164 chars> | `sha256:0cb3a6242da518a08dc9d589109a92d71820925223a1771083859adff4b74c04` |
| 3 | `0` | ❌ | `SL-7` | 0, 1 | accept=2, reject=0, waiver=0 | SL-10 decision=rework, ok=False, target=True, regression=False, drift=minor, rework=SL-10 pass was downgraded because local deterministic evidence reported major drift and SL-10 evidence did not explicitly address the local rejection reason/kind with a structu...<truncated 164 chars> | `sha256:99b0a326ebeea9465293f0e2db1a3b73061d351cb6e6d73b9fddc25f2ec1a5c7` |
| 4 | `0` | ❌ | `SL-7` | 0, 1 | accept=2, reject=0, waiver=0 | SL-10 decision=rework, ok=False, target=True, regression=False, drift=minor, rework=SL-10 pass was downgraded because local deterministic evidence reported major drift and SL-10 evidence did not explicitly address the local rejection reason/kind with a structu...<truncated 164 chars> | `sha256:0cb3a6242da518a08dc9d589109a92d71820925223a1771083859adff4b74c04` |
| 5 | `0` | ❌ | `SL-7` | 0, 1 | accept=2, reject=0, waiver=0 | SL-10 decision=rework, ok=False, target=True, regression=False, drift=minor, rework=SL-10 pass was downgraded because local deterministic evidence reported major drift and SL-10 evidence did not explicitly address the local rejection reason/kind with a structu...<truncated 164 chars> | `sha256:0cb3a6242da518a08dc9d589109a92d71820925223a1771083859adff4b74c04` |

> 完整 repair 细节、进入修复原因、SD-8 修改建议、SL-9 candidate、before→candidate diff 与 local-check evidence 与 SL-10 审查证据见 `../runs/pr_e1_real_agent_loop_round24_deepghs_stream_full_logs/pr-e1-path1_cara-default-round24deepghsstream-1afcc21e/report.md` §7。

</details>

<details><summary>path1 / path1_elevator / default / success</summary>

#### NL 输入（原文）

```text
The automatic elevator controller is built as a finite-state machine whose state space combines floor states `F1`, `F2`, and `F3` with motion states `MU2`, `MU3`, `MD1`, and `MD2` for upward and downward travel.

In the normal workflow, the system starts from an ideal state on floor 1, chooses either the up or down branch according to floor requests, stops at the requested floor, and then immediately checks the next destination before deciding whether to continue moving.

The controller uses `PS1/PS2/PS3` as floor-request inputs and `S1/S2/S3` as sensing inputs for arrival. From `F1`, `PS2` triggers `MU2` and `PS3` triggers `MU3`. From `F2`, `PS3` triggers `MU3` and `PS1` triggers `MD1`. From `F3`, `PS1` triggers `MD1` and `PS2` triggers `MD2`. Arrival sensors complete motion transitions: `MU2 + S2 -> F2`, `MU3 + S3 -> F3`, `MD1 + S1 -> F1`, and `MD2 + S2 -> F2`.

The `hbrg` output distinguishes upward drive, downward drive, and stop conditions. A reset signal forces the controller back to floor 1 regardless of the outstanding request context.
```

#### NL 输入中文翻译

```text
自动电梯控制器被构建为有限状态机，其状态空间由楼层状态 `F1`、`F2`、`F3` 与上/下行运动状态 `MU2`、`MU3`、`MD1`、`MD2` 组合而成。

正常流程中，系统从 1 楼理想状态开始，根据楼层请求选择上行或下行分支，在请求楼层停止，然后立即检查下一目的地以决定是否继续移动。

控制器使用 `PS1/PS2/PS3` 作为楼层请求输入，使用 `S1/S2/S3` 作为到位传感输入。从 `F1`，`PS2` 触发 `MU2`，`PS3` 触发 `MU3`；从 `F2`，`PS3` 触发 `MU3`，`PS1` 触发 `MD1`；从 `F3`，`PS1` 触发 `MD1`，`PS2` 触发 `MD2`。到位传感器完成运动转移：`MU2 + S2 -> F2`，`MU3 + S3 -> F3`，`MD1 + S1 -> F1`，`MD2 + S2 -> F2`。

`hbrg` 输出区分上行驱动、下行驱动和停止状态。复位信号会无视当前请求上下文，强制控制器回到 1 楼。
```

#### FCSTM 输出

```pyfcstm
def int PS1 = 0;
def int PS2 = 0;
def int PS3 = 0;
def int S1 = 0;
def int S2 = 0;
def int S3 = 0;
def int hbrg = 0;

state AutomaticElevatorController {
    ! * -> F1 :: reset;

    [*] -> F1;

    state F1 {
        enter { hbrg = 0; }
    }

    state F2 {
        enter { hbrg = 0; }
    }

    state F3 {
        enter { hbrg = 0; }
    }

    state MU2 {
        enter { hbrg = 1; }
    }

    state MU3 {
        enter { hbrg = 1; }
    }

    state MD1 {
        enter { hbrg = -1; }
    }

    state MD2 {
        enter { hbrg = -1; }
    }

    F1 -> MU2 : if [PS2 > 0];
    F1 -> MU3 : if [PS3 > 0];
    F2 -> MU3 : if [PS3 > 0];
    F2 -> MD1 : if [PS1 > 0];
    F3 -> MD1 : if [PS1 > 0];
    F3 -> MD2 : if [PS2 > 0];
    MU2 -> F2 : if [S2 > 0];
    MU3 -> F3 : if [S3 > 0];
    MD1 -> F1 : if [S1 > 0];
    MD2 -> F2 : if [S2 > 0];
}
```

#### agent-loop 过程与日志路径

| 项 | 值 |
|---|---|
| verdict / status | `success` / `success` |
| failure class | `success` |
| executed stages | `SC-0 -> SL-1 -> SD-2 -> SD-3 -> SD-4 -> SL-5 -> SD-5A -> SC-5F -> SD-6 -> SL-7 -> SC-12 -> SC-13` |
| iter / repairs / accepted / scenarios | `1` / `0` / `0` / `1` |
| token / elapsed | `{'prompt_tokens': 0, 'completion_tokens': 0, 'total_tokens': 0, 'prompt_chars': 140322, 'completion_chars': 27060, 'n_calls': 3}` / `193.262s` |
| full stage table | `../runs/pr_e1_real_agent_loop_round24_deepghs_stream_full_logs/pr-e1-path1_elevator-default-round24deepghsstream-019c0d50/report.md` §4 |
| run record | `../runs/pr_e1_real_agent_loop_round24_deepghs_stream_full_logs/pr-e1-path1_elevator-default-round24deepghsstream-019c0d50/pr-e1-path1_elevator-default-round24deepghsstream-019c0d50.agent_loop.json.gz` |
| logs | `../runs/pr_e1_real_agent_loop_round24_deepghs_stream_full_logs/pr-e1-path1_elevator-default-round24deepghsstream-019c0d50/run_logs/stdout.txt`, `../runs/pr_e1_real_agent_loop_round24_deepghs_stream_full_logs/pr-e1-path1_elevator-default-round24deepghsstream-019c0d50/run_logs/stderr.txt` |
| checks / repro | `../runs/pr_e1_real_agent_loop_round24_deepghs_stream_full_logs/pr-e1-path1_elevator-default-round24deepghsstream-019c0d50/checks.json`, `../runs/pr_e1_real_agent_loop_round24_deepghs_stream_full_logs/pr-e1-path1_elevator-default-round24deepghsstream-019c0d50/reproducibility.json` |

#### 全流程摘要表（report §4 摘录）

| Stage | 是否 LLM | iteration | 结果 | 获取的信息 / 反馈 | 本阶段做了什么 | DSL 修改 | artifact/log |
|---|---:|---:|---:|---|---|---|---|
| `SC-0` | 否 | - | ✅ | trace/control | 初始化 run state | 无/见 record | [`record`](./pr-e1-path1_elevator-default-round24deepghsstream-019c0d50.agent_loop.json.gz) |
| `SL-1` | 是 | - | ✅ | LLM calls=1, tokens=0 | 生成初始 DSL 与 grounding seeds | initial len=848 | [`record`](./pr-e1-path1_elevator-default-round24deepghsstream-019c0d50.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_elevator-default-round24deepghsstream-019c0d50.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_elevator-default-round24deepghsstream-019c0d50.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=17, info=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_elevator-default-round24deepghsstream-019c0d50.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=1, tokens=0 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_elevator-default-round24deepghsstream-019c0d50.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_elevator-default-round24deepghsstream-019c0d50.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_elevator-default-round24deepghsstream-019c0d50.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_elevator-default-round24deepghsstream-019c0d50.agent_loop.json.gz) |
| `SL-7` | 是 | 0 | ✅ | LLM calls=1, tokens=0 | LLM model review | 无/见 record | [`record`](./pr-e1-path1_elevator-default-round24deepghsstream-019c0d50.agent_loop.json.gz) |
| `SC-12` | 否 | - | ✅ | full_pass_all_required_feedback_ok | 写 final verdict | 无/见 record | [`record`](./pr-e1-path1_elevator-default-round24deepghsstream-019c0d50.agent_loop.json.gz) |
| `SC-13` | 否 | - | ✅ | trace/control | 写审计 run record | 无/见 record | [`record`](./pr-e1-path1_elevator-default-round24deepghsstream-019c0d50.agent_loop.json.gz) |

### 4.1 完整流程日志（stage/control-flow replay ledger）

口径：本节来自 `AgentLoopRunRecord.logs`，与 [`flow_log.json`](./flow_log.json) 一致；用于复现每个 stage 如何进入、得到什么批示、跳转到哪里，以及每次 DSL 产物/候选如何变化。

| # | ts | stage | iter | event | result / jump | DSL evidence |
|---:|---|---|---:|---|---|---|
| 1 | `2026-06-04T02:44:10Z` | `SC-0` | `-` | `run_start` | {} | <none> |
| 2 | `2026-06-04T02:44:10Z` | `SL-1` | `-` | `stage_enter` | {"reason": "initial_modeling_adapter_available"} | <none> |
| 3 | `2026-06-04T02:45:26Z` | `SL-1` | `-` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 4 | `2026-06-04T02:45:26Z` | `SL-1` | `-` | `stage_result` | {"jump": "SD-2", "ok": true} | candidate_dsl:len=848,hash=sha256:76df5e8453da |
| 5 | `2026-06-04T02:45:26Z` | `<control>` | `0` | `iteration_enter` | {} | current_hash=sha256:76df5e8453da8b87b9619f41f32d9080e688f9a48288584c310613d9dbf5e0d7 |
| 6 | `2026-06-04T02:45:26Z` | `<control>` | `0` | `iteration_validation_enter` | {} | dsl:len=848,hash=sha256:76df5e8453da, current_hash=sha256:76df5e8453da8b87b9619f41f32d9080e688f9a48288584c310613d9dbf5e0d7 |
| 7 | `2026-06-04T02:45:26Z` | `SD-2` | `0` | `stage_enter` | {"reason": "full_validation_pass"} | <none> |
| 8 | `2026-06-04T02:45:26Z` | `SD-2` | `0` | `stage_result` | {"jump": "SD-3", "ok": true, "status": "StageStatus.OK"} | <none> |
| 9 | `2026-06-04T02:45:26Z` | `SD-3` | `0` | `stage_enter` | {"reason": "SD-2 ok"} | <none> |
| 10 | `2026-06-04T02:45:26Z` | `SD-3` | `0` | `stage_result` | {"jump": "SD-4", "ok": true, "status": "StageStatus.OK"} | <none> |
| 11 | `2026-06-04T02:45:26Z` | `SD-4` | `0` | `stage_enter` | {"reason": "SD-3 ok"} | <none> |
| 12 | `2026-06-04T02:45:26Z` | `SD-4` | `0` | `stage_result` | {"jump": "SL-5", "ok": true, "status": "StageStatus.OK"} | <none> |
| 13 | `2026-06-04T02:45:26Z` | `SL-5` | `0` | `stage_enter` | {"reason": "scenario_set_absent"} | <none> |
| 14 | `2026-06-04T02:46:40Z` | `SL-5` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 15 | `2026-06-04T02:46:40Z` | `SD-5A` | `0` | `stage_result` | {"jump": "SC-5F", "ok": true, "status": "StageStatus.OK"} | <none> |
| 16 | `2026-06-04T02:46:40Z` | `SC-5F` | `0` | `stage_result` | {"jump": "SD-6", "ok": true} | <none> |
| 17 | `2026-06-04T02:46:40Z` | `SD-6` | `0` | `stage_enter` | {"reason": "scenario_set_ready"} | <none> |
| 18 | `2026-06-04T02:46:40Z` | `SD-6` | `0` | `stage_result` | {"jump": "SL-7", "ok": true, "status": "StageStatus.OK"} | <none> |
| 19 | `2026-06-04T02:46:40Z` | `SL-7` | `0` | `stage_enter` | {"reason": "SD-6 ok"} | <none> |
| 20 | `2026-06-04T02:47:23Z` | `SL-7` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 21 | `2026-06-04T02:47:23Z` | `SL-7` | `0` | `stage_result` | {"jump": "SC-12 success", "ok": true, "status": "StageStatus.OK"} | <none> |
| 22 | `2026-06-04T02:47:23Z` | `SL-7` | `0` | `grounding_update_hints_recorded` | {} | <none> |
| 23 | `2026-06-04T02:47:23Z` | `<control>` | `0` | `iteration_validation_result` | {"jump": "SC-12 success", "selected_feedback": null} | <none> |
| 24 | `2026-06-04T02:47:23Z` | `SC-12` | `-` | `sc12_verdict` | {"reason": "full_pass_all_required_feedback_ok", "verdict": "success"} | final_dsl:len=848,hash=sha256:76df5e8453da |
| 25 | `2026-06-04T02:47:23Z` | `SC-13` | `-` | `run_end` | {"verdict": "success"} | final_dsl:len=848,hash=sha256:76df5e8453da |

#### Scenario 逐轮通过矩阵（report §6.1 摘录）

口径：`✅` = 该 scenario 在该轮 SD-6 simulation 通过；`❌` = 该轮失败；`⚪` = 该轮未执行或无该 scenario 结果。

| Scenario | Intent | Iter 1 |
|---|---|---|
| `default_init_f1_no_request_stays_stopped` | default-init verifies the initial transition lands on floor F1 with stopped hbrg, and with no requests the controller st...<truncated 18 chars> | ✅ |
| `f1_ps2_moves_up_to_f2` | explicit-hot-start probes F1 request PS2 causing upward MU2 drive, then S2 arrival stopping at requested floor F2. | ✅ |
| `f1_ps3_moves_up_to_f3_then_reset` | explicit-hot-start probes F1 request PS3 causing upward MU3 drive, S3 arrival at F3, and reset forcing back to F1 from a...<truncated 13 chars> | ✅ |
| `f2_ps3_moves_up_to_f3` | explicit-hot-start probes F2 request PS3 causing upward MU3 drive and S3 arrival stopping at F3. | ✅ |
| `f2_ps1_moves_down_to_f1` | explicit-hot-start probes F2 request PS1 causing downward MD1 drive and S1 arrival stopping at F1. | ✅ |
| `f3_ps1_moves_down_to_f1` | explicit-hot-start probes F3 request PS1 causing downward MD1 drive and S1 arrival stopping at F1. | ✅ |
| `f3_ps2_moves_down_to_f2` | explicit-hot-start probes F3 request PS2 causing downward MD2 drive and S2 arrival stopping at F2. | ✅ |
| `reset_forces_f1_from_motion_contexts` | explicit-hot-start probes reset forcing F1 from a downward motion state, then from an upward motion state reached after ...<truncated 51 chars> | ✅ |

#### Repair / blocking feedback 概览（report §7 摘录）

- 本 run 未进入 `SD-8/SL-9/SL-10` repair block；通常表示流程在 repair 前已成功、被 provider/schema 错误中断，或在 pre-repair 阶段直接退出。

### 8. 尝试记录与成本

- `SL-1`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 3600, 'completion_chars': 12064, 'completion_tokens': 0, 'elapsed_seconds': 75.97855450499628, 'first_chunk_seconds': 11.14856809999037, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 24850, 'prompt_tokens': 0, 'stream': True, 'total_tokens': 0}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1930, 'completion_chars': 7447, 'completion_tokens': 0, 'elapsed_seconds': 73.65545767900767, 'first_chunk_seconds': 39.231897574005416, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 50995, 'prompt_tokens': 0, 'stream': True, 'total_tokens': 0}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-7`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1794, 'completion_chars': 7549, 'completion_tokens': 0, 'elapsed_seconds': 43.09778998000547, 'first_chunk_seconds': 10.4514122170076, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 64477, 'prompt_tokens': 0, 'stream': True, 'total_tokens': 0}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。

### 9. 最终停止状态与后续含义

- 停止状态：verdict=`success`，record_status=`success`。
- 主要原因分类：`success`。
- required stages executed：`12/12`，missing=`<none>`。
- repairs：`0/0` accepted；scenario_history=`1`。
- 配置含义：`recommended baseline candidate`；该结果可用于评估默认入口本身。
- 样本含义：若出现 `design_or_variable_dynamics`，应重点审查变量是否仅作为 guard/input 常量而没有事件/动作更新；若出现 pre-scenario parse/semantic 失败，则应先优化 pyfcstm grammar adherence。

> 完整 repair 细节、进入修复原因、SD-8 修改建议、SL-9 candidate、before→candidate diff 与 local-check evidence 与 SL-10 审查证据见 `../runs/pr_e1_real_agent_loop_round24_deepghs_stream_full_logs/pr-e1-path1_elevator-default-round24deepghsstream-019c0d50/report.md` §7。

</details>

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
def float Pbatt_Pmax = 0.0;
def float Pgen_req = 0.0;
def float Pbatt_discharge = 0.0;
def float Pbatt_charge = 0.0;
def float Pspare = 0.0;
def int cutin_LNG = 0;
def int cutout_LNG = 0;
def int cutin_DG3 = 0;
def int cutout_DG3 = 0;
def int cutin_DG1 = 0;
def int cutout_DG1 = 0;
def int cutin_DG2 = 0;
def int cutout_DG2 = 0;
def int load_cutout = 0;

state LNGShipEMS {
    ! * -> ZeroLoad_RES_Charge : if [PL == 0 && Ppv + Pw > 0 && SoC < 0.95];
    ! * -> ZeroLoad_RES_Spare : if [PL == 0 && Ppv + Pw > 0 && SoC >= 0.95];
    ! * -> ZeroLoad_NoRES : if [PL == 0 && Ppv + Pw <= 0];
    ! * -> RES_Covers_Charge : if [PL > 0 && Ppv + Pw >= PL && SoC < 0.95];
    ! * -> RES_Covers_Spare : if [PL > 0 && Ppv + Pw >= PL && SoC >= 0.95];
    ! * -> Battery_Assist : if [PL > 0 && Ppv + Pw < PL && SoC > 0.2 && PL - Ppv - Pw <= Pbatt_Pmax];
    ! * -> LNG_Battery_Cover : if [PL > 0 && Ppv + Pw < PL && SoC > 0.2 && PL - Ppv - Pw > Pbatt_Pmax && PL - Ppv - Pw <= Pbatt_Pmax + Pgmax];
    ! * -> LNG_LowSoC_ChargeMargin : if [PL > 0 && Ppv + Pw < PL && SoC <= 0.2 && PL - Ppv - Pw + Pgmax / 5 <= Pgmax];
    ! * -> LNG_DG3_Cover : if [PL > 0 && Ppv + Pw < PL && SoC > 0.2 && PL - Ppv - Pw > Pbatt_Pmax + Pgmax && PL - Ppv - Pw <= Pbatt_Pmax + Pgmax + eng3_Pmax];
    ! * -> DG1_LowSoC_ChargeMargin : if [PL > 0 && Ppv + Pw < PL && SoC <= 0.2 && PL - Ppv - Pw + Pgmax / 5 > Pgmax && PL - Ppv - Pw + Pd1max / 10 <= Pgmax + eng3_Pmax + Pd1max];
    ! * -> DG1_DG2_LastPriority : if [PL > 0 && Ppv + Pw < PL && ((SoC > 0.2 && PL - Ppv - Pw > Pbatt_Pmax + Pgmax + eng3_Pmax && PL - Ppv - Pw <= Pbatt_Pmax + Pgmax + eng3_Pmax + Pd1max + Pd2max) || (SoC <= 0.2 && PL - Ppv - Pw + Pd1max / 10 > Pgmax + eng3_Pmax + Pd1max && PL - Ppv - Pw + Pd1max / 10 <= Pgmax + eng3_Pmax + Pd1max + Pd2max))];
    ! * -> Overload_Illegal : if [PL > 0 && Ppv + Pw < PL && ((SoC > 0.2 && PL - Ppv - Pw > Pbatt_Pmax + Pgmax + eng3_Pmax + Pd1max + Pd2max) || (SoC <= 0.2 && PL - Ppv - Pw + Pd1max / 10 > Pgmax + eng3_Pmax + Pd1max + Pd2max))];

    [*] -> ZeroLoad_NoRES;

    state ZeroLoad_RES_Charge {
        enter {
            Pgen_req = 0;
            Pbatt_discharge = 0;
            Pbatt_charge = Ppv + Pw;
            Pspare = 0;
            cutin_LNG = 0;
            cutout_LNG = 1;
            cutin_DG3 = 0;
            cutout_DG3 = 1;
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
            Pbatt_discharge = 0;
            Pbatt_charge = 0;
            Pspare = Ppv + Pw;
            cutin_LNG = 0;
            cutout_LNG = 1;
            cutin_DG3 = 0;
            cutout_DG3 = 1;
            cutin_DG1 = 0;
            cutout_DG1 = 1;
            cutin_DG2 = 0;
            cutout_DG2 = 1;
            load_cutout = 0;
        }
    }

    state ZeroLoad_NoRES {
        enter {
            Pgen_req = 0;
            Pbatt_discharge = 0;
            Pbatt_charge = 0;
            Pspare = 0;
            cutin_LNG = 0;
            cutout_LNG = 1;
            cutin_DG3 = 0;
            cutout_DG3 = 1;
            cutin_DG1 = 0;
            cutout_DG1 = 1;
            cutin_DG2 = 0;
            cutout_DG2 = 1;
            load_cutout = 0;
        }
    }

    state RES_Covers_Charge {
        enter {
            Pgen_req = 0;
            Pbatt_discharge = 0;
            Pbatt_charge = Ppv + Pw - PL;
            Pspare = 0;
            cutin_LNG = 0;
            cutout_LNG = 1;
            cutin_DG3 = 0;
            cutout_DG3 = 1;
            cutin_DG1 = 0;
            cutout_DG1 = 1;
            cutin_DG2 = 0;
            cutout_DG2 = 1;
            load_cutout = 0;
        }
    }

    state RES_Covers_Spare {
        enter {
            Pgen_req = 0;
            Pbatt_discharge = 0;
            Pbatt_charge = 0;
            Pspare = Ppv + Pw - PL;
            cutin_LNG = 0;
            cutout_LNG = 1;
            cutin_DG3 = 0;
            cutout_DG3 = 1;
            cutin_DG1 = 0;
            cutout_DG1 = 1;
            cutin_DG2 = 0;
            cutout_DG2 = 1;
            load_cutout = 0;
        }
    }

    state Battery_Assist {
        enter {
            Pgen_req = 0;
            Pbatt_discharge = PL - Ppv - Pw;
            Pbatt_charge = 0;
            Pspare = 0;
            cutin_LNG = 0;
            cutout_LNG = 1;
            cutin_DG3 = 0;
            cutout_DG3 = 1;
            cutin_DG1 = 0;
            cutout_DG1 = 1;
            cutin_DG2 = 0;
            cutout_DG2 = 1;
            load_cutout = 0;
        }
    }

    state LNG_Battery_Cover {
        enter {
            Pgen_req = PL - Ppv - Pw - Pbatt_Pmax;
            Pbatt_discharge = Pbatt_Pmax;
            Pbatt_charge = 0;
            Pspare = 0;
            cutin_LNG = 1;
            cutout_LNG = 0;
            cutin_DG3 = 0;
            cutout_DG3 = 1;
            cutin_DG1 = 0;
            cutout_DG1 = 1;
            cutin_DG2 = 0;
            cutout_DG2 = 1;
            load_cutout = 0;
        }
    }

    state LNG_LowSoC_ChargeMargin {
        enter {
            Pgen_req = PL - Ppv - Pw + Pgmax / 5;
            Pbatt_discharge = 0;
            Pbatt_charge = Pgmax / 5;
            Pspare = 0;
            cutin_LNG = 1;
            cutout_LNG = 0;
            cutin_DG3 = 0;
            cutout_DG3 = 1;
            cutin_DG1 = 0;
            cutout_DG1 = 1;
            cutin_DG2 = 0;
            cutout_DG2 = 1;
            load_cutout = 0;
        }
    }

    state LNG_DG3_Cover {
        enter {
            Pgen_req = PL - Ppv - Pw - Pbatt_Pmax;
            Pbatt_discharge = Pbatt_Pmax;
            Pbatt_charge = 0;
            Pspare = 0;
            cutin_LNG = 1;
            cutout_LNG = 0;
            cutin_DG3 = 1;
            cutout_DG3 = 0;
            cutin_DG1 = 0;
            cutout_DG1 = 1;
            cutin_DG2 = 0;
            cutout_DG2 = 1;
            load_cutout = 0;
        }
    }

    state DG1_LowSoC_ChargeMargin {
        enter {
            Pgen_req = PL - Ppv - Pw + Pd1max / 10;
            Pbatt_discharge = 0;
            Pbatt_charge = Pd1max / 10;
            Pspare = 0;
            cutin_LNG = 1;
            cutout_LNG = 0;
            cutin_DG3 = 1;
            cutout_DG3 = 0;
            cutin_DG1 = 1;
            cutout_DG1 = 0;
            cutin_DG2 = 0;
            cutout_DG2 = 1;
            load_cutout = 0;
        }
    }

    state DG1_DG2_LastPriority {
        enter {
            Pgen_req = PL - Ppv - Pw - Pbatt_Pmax;
            Pbatt_discharge = Pbatt_Pmax;
            Pbatt_charge = 0;
            Pspare = 0;
            cutin_LNG = 1;
            cutout_LNG = 0;
            cutin_DG3 = 1;
            cutout_DG3 = 0;
            cutin_DG1 = 1;
            cutout_DG1 = 0;
            cutin_DG2 = 1;
            cutout_DG2 = 0;
            load_cutout = 0;
        }
    }

    state Overload_Illegal {
        enter {
            Pgen_req = Pgmax + eng3_Pmax + Pd1max + Pd2max;
            Pbatt_discharge = PL - Ppv - Pw - Pgmax - eng3_Pmax - Pd1max - Pd2max;
            Pbatt_charge = 0;
            Pspare = 0;
            cutin_LNG = 1;
            cutout_LNG = 0;
            cutin_DG3 = 1;
            cutout_DG3 = 0;
            cutin_DG1 = 1;
            cutout_DG1 = 0;
            cutin_DG2 = 1;
            cutout_DG2 = 0;
            load_cutout = 0;
        }
    }
}
```

#### agent-loop 过程与日志路径

| 项 | 值 |
|---|---|
| verdict / status | `success` / `success` |
| failure class | `success` |
| executed stages | `SC-0 -> SL-1 -> SD-2 -> SD-3 -> SD-4 -> SD-8 -> SL-9 -> SD-4 -> SL-5 -> SD-5A -> SL-5 -> SD-5A -> SC-5F -> SD-6 -> SD-2 -> SD-3 -> SD-4 -> SD-8 -> SL-9 -> SD-4 -> SD-5A -> SC-5F -> SD-6 -> SD-2 -> SD-3 -> SD-4 -> SD-5A -> SC-5F -> SD-6 -> SD-8 -> SL-9 -> SL-10 -> SC-11 -> SD-2 -> SD-3 -> SD-4 -> SD-5A -> SL-5 -> SD-5A -> SL-5 -> SD-5A -> SC-5F -> SD-6 -> SL-7 -> SC-12 -> SC-13` |
| iter / repairs / accepted / scenarios | `4` / `3` / `1` / `7` |
| token / elapsed | `{'prompt_tokens': 0, 'completion_tokens': 0, 'total_tokens': 0, 'prompt_chars': 985090, 'completion_chars': 99603, 'n_calls': 10}` / `707.787s` |
| full stage table | `../runs/pr_e1_real_agent_loop_round24_deepghs_stream_full_logs/pr-e1-path2_lng_ems-default-round24deepghsstream-cd202f61/report.md` §4 |
| run record | `../runs/pr_e1_real_agent_loop_round24_deepghs_stream_full_logs/pr-e1-path2_lng_ems-default-round24deepghsstream-cd202f61/pr-e1-path2_lng_ems-default-round24deepghsstream-cd202f61.agent_loop.json.gz` |
| logs | `../runs/pr_e1_real_agent_loop_round24_deepghs_stream_full_logs/pr-e1-path2_lng_ems-default-round24deepghsstream-cd202f61/run_logs/stdout.txt`, `../runs/pr_e1_real_agent_loop_round24_deepghs_stream_full_logs/pr-e1-path2_lng_ems-default-round24deepghsstream-cd202f61/run_logs/stderr.txt` |
| checks / repro | `../runs/pr_e1_real_agent_loop_round24_deepghs_stream_full_logs/pr-e1-path2_lng_ems-default-round24deepghsstream-cd202f61/checks.json`, `../runs/pr_e1_real_agent_loop_round24_deepghs_stream_full_logs/pr-e1-path2_lng_ems-default-round24deepghsstream-cd202f61/reproducibility.json` |

#### 全流程摘要表（report §4 摘录）

| Stage | 是否 LLM | iteration | 结果 | 获取的信息 / 反馈 | 本阶段做了什么 | DSL 修改 | artifact/log |
|---|---:|---:|---:|---|---|---|---|
| `SC-0` | 否 | - | ✅ | trace/control | 初始化 run state | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round24deepghsstream-cd202f61.agent_loop.json.gz) |
| `SL-1` | 是 | - | ✅ | LLM calls=1, tokens=0 | 生成初始 DSL 与 grounding seeds | initial len=7641 | [`record`](./pr-e1-path2_lng_ems-default-round24deepghsstream-cd202f61.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round24deepghsstream-cd202f61.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round24deepghsstream-cd202f61.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ⚠️ | blocking=61, advisory=118, info=0; blocking=0, advisory=179, info=0; blocking=61, advisory=118, info=0; blocking=0, advisory=179, info=0; blocking=0, advisory=179, info=0; blocking | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round24deepghsstream-cd202f61.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round24deepghsstream-cd202f61.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=3, tokens=0 | LLM per-request accept/reject + repair | candidate len=0,0,7636 | [`record`](./pr-e1-path2_lng_ems-default-round24deepghsstream-cd202f61.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ⚠️ | blocking=61, advisory=118, info=0; blocking=0, advisory=179, info=0; blocking=61, advisory=118, info=0; blocking=0, advisory=179, info=0; blocking=0, advisory=179, info=0; blocking | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round24deepghsstream-cd202f61.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=4, tokens=0 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round24deepghsstream-cd202f61.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round24deepghsstream-cd202f61.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=4, tokens=0 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round24deepghsstream-cd202f61.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round24deepghsstream-cd202f61.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round24deepghsstream-cd202f61.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ⚠️ | ok=False, diag=0; ok=False, diag=0; ok=False, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round24deepghsstream-cd202f61.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round24deepghsstream-cd202f61.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round24deepghsstream-cd202f61.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ⚠️ | blocking=61, advisory=118, info=0; blocking=0, advisory=179, info=0; blocking=61, advisory=118, info=0; blocking=0, advisory=179, info=0; blocking=0, advisory=179, info=0; blocking | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round24deepghsstream-cd202f61.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round24deepghsstream-cd202f61.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=3, tokens=0 | LLM per-request accept/reject + repair | candidate len=0,0,7636 | [`record`](./pr-e1-path2_lng_ems-default-round24deepghsstream-cd202f61.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ⚠️ | blocking=61, advisory=118, info=0; blocking=0, advisory=179, info=0; blocking=61, advisory=118, info=0; blocking=0, advisory=179, info=0; blocking=0, advisory=179, info=0; blocking | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round24deepghsstream-cd202f61.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round24deepghsstream-cd202f61.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round24deepghsstream-cd202f61.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ⚠️ | ok=False, diag=0; ok=False, diag=0; ok=False, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round24deepghsstream-cd202f61.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round24deepghsstream-cd202f61.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round24deepghsstream-cd202f61.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=61, advisory=118, info=0; blocking=0, advisory=179, info=0; blocking=61, advisory=118, info=0; blocking=0, advisory=179, info=0; blocking=0, advisory=179, info=0; blocking | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round24deepghsstream-cd202f61.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round24deepghsstream-cd202f61.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round24deepghsstream-cd202f61.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ⚠️ | ok=False, diag=0; ok=False, diag=0; ok=False, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round24deepghsstream-cd202f61.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round24deepghsstream-cd202f61.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=3, tokens=0 | LLM per-request accept/reject + repair | candidate len=0,0,7636 | [`record`](./pr-e1-path2_lng_ems-default-round24deepghsstream-cd202f61.agent_loop.json.gz) |
| `SL-10` | 是 | 2 | ✅ | LLM calls=1, tokens=0 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round24deepghsstream-cd202f61.agent_loop.json.gz) |
| `SC-11` | 否 | 2 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round24deepghsstream-cd202f61.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round24deepghsstream-cd202f61.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round24deepghsstream-cd202f61.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=61, advisory=118, info=0; blocking=0, advisory=179, info=0; blocking=61, advisory=118, info=0; blocking=0, advisory=179, info=0; blocking=0, advisory=179, info=0; blocking | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round24deepghsstream-cd202f61.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round24deepghsstream-cd202f61.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=4, tokens=0 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round24deepghsstream-cd202f61.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round24deepghsstream-cd202f61.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=4, tokens=0 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round24deepghsstream-cd202f61.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round24deepghsstream-cd202f61.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round24deepghsstream-cd202f61.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=False, diag=0; ok=False, diag=0; ok=False, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round24deepghsstream-cd202f61.agent_loop.json.gz) |
| `SL-7` | 是 | 3 | ✅ | LLM calls=1, tokens=0 | LLM model review | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round24deepghsstream-cd202f61.agent_loop.json.gz) |
| `SC-12` | 否 | - | ✅ | full_pass_all_required_feedback_ok | 写 final verdict | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round24deepghsstream-cd202f61.agent_loop.json.gz) |
| `SC-13` | 否 | - | ✅ | trace/control | 写审计 run record | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round24deepghsstream-cd202f61.agent_loop.json.gz) |

### 4.1 完整流程日志（stage/control-flow replay ledger）

口径：本节来自 `AgentLoopRunRecord.logs`，与 [`flow_log.json`](./flow_log.json) 一致；用于复现每个 stage 如何进入、得到什么批示、跳转到哪里，以及每次 DSL 产物/候选如何变化。

| # | ts | stage | iter | event | result / jump | DSL evidence |
|---:|---|---|---:|---|---|---|
| 1 | `2026-06-04T02:44:10Z` | `SC-0` | `-` | `run_start` | {} | <none> |
| 2 | `2026-06-04T02:44:10Z` | `SL-1` | `-` | `stage_enter` | {"reason": "initial_modeling_adapter_available"} | <none> |
| 3 | `2026-06-04T02:46:37Z` | `SL-1` | `-` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 4 | `2026-06-04T02:46:37Z` | `SL-1` | `-` | `stage_result` | {"jump": "SD-2", "ok": true} | candidate_dsl:len=7641,hash=sha256:97e16b009659 |
| 5 | `2026-06-04T02:46:37Z` | `<control>` | `0` | `iteration_enter` | {} | current_hash=sha256:97e16b0096593bf5c3be671c14a9b339fe08773d840cc5c5f366ea01de706ff9 |
| 6 | `2026-06-04T02:46:37Z` | `<control>` | `0` | `iteration_validation_enter` | {} | dsl:len=7641,hash=sha256:97e16b009659, current_hash=sha256:97e16b0096593bf5c3be671c14a9b339fe08773d840cc5c5f366ea01de706ff9 |
| 7 | `2026-06-04T02:46:37Z` | `SD-2` | `0` | `stage_enter` | {"reason": "full_validation_pass"} | <none> |
| 8 | `2026-06-04T02:46:37Z` | `SD-2` | `0` | `stage_result` | {"jump": "SD-3", "ok": true, "status": "StageStatus.OK"} | <none> |
| 9 | `2026-06-04T02:46:37Z` | `SD-3` | `0` | `stage_enter` | {"reason": "SD-2 ok"} | <none> |
| 10 | `2026-06-04T02:46:37Z` | `SD-3` | `0` | `stage_result` | {"jump": "SD-4", "ok": true, "status": "StageStatus.OK"} | <none> |
| 11 | `2026-06-04T02:46:37Z` | `SD-4` | `0` | `stage_enter` | {"reason": "SD-3 ok"} | <none> |
| 12 | `2026-06-04T02:46:37Z` | `SD-4` | `0` | `stage_result` | {"jump": "SD-8", "ok": false, "status": "StageStatus.FAIL"} | <none> |
| 13 | `2026-06-04T02:46:37Z` | `<control>` | `0` | `iteration_validation_result` | {"jump": "SD-8 repair", "selected_feedback": {"blocking": true, "blocking_instance_keys": ["W_UNWRITTEN_READ_VAR:var_name=Pbatt_Pmax", "W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoad_RES_Charge:to_path=LNGShipEMS.Battery_Assist", "W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoad_RES_Charge:to_path=LNGShipEMS.LNG_Battery_Cover", "W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoad_RES_Charge:to_pat...<truncated 14048 chars> | <none> |
| 14 | `2026-06-04T02:46:37Z` | `SD-8` | `0` | `repair_path_enter` | {"jump": "SD-8", "selected_feedback": {"blocking": true, "blocking_instance_keys": ["W_UNWRITTEN_READ_VAR:var_name=Pbatt_Pmax", "W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoad_RES_Charge:to_path=LNGShipEMS.Battery_Assist", "W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoad_RES_Charge:to_path=LNGShipEMS.LNG_Battery_Cover", "W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoad_RES_Charge:to_path=LNGSh...<truncated 230390 chars> | current_dsl:len=7641,hash=sha256:97e16b009659 |
| 15 | `2026-06-04T02:46:37Z` | `SD-8` | `0` | `stage_result` | {"jump": "SL-9", "ok": true, "status": "StageStatus.OK"} | <none> |
| 16 | `2026-06-04T02:46:37Z` | `SD-8` | `0` | `fix_request_batch` | {"request_count": 12} | <none> |
| 17 | `2026-06-04T02:46:37Z` | `SL-9` | `0` | `stage_enter` | {"reason": "fix_requests_ready"} | old_dsl:len=7641,hash=sha256:97e16b009659 |
| 18 | `2026-06-04T02:47:13Z` | `SL-9` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 19 | `2026-06-04T02:47:13Z` | `SL-9` | `0` | `stage_result` | {"accepted_request_ids": [], "jump": "waiver_continue_or_exit", "ok": false, "rejected_request_ids": ["fixreq-0-sd4-0-7834424f96", "fixreq-0-sd4-1-9f1d2febcb", "fixreq-0-sd4-2-ca9fac2e8b", "fixreq-0-sd4-3-192b451757", "fixreq-0-sd4-4-0561591835", "fixreq-0-sd4-5-8c8ce68b06", "fixreq-0-sd4-6-7bc60c33a1", "fixreq-0-sd4-7-b11d15187f", "fixreq-0-sd4-8-6d3ca72884", "fixreq-0-sd4-9-ad6b820773", "fixreq-0-sd4-10-0fb48e97d1"...<truncated 32 chars> | <none> |
| 20 | `2026-06-04T02:47:13Z` | `SL-9` | `0` | `sl9_all_rejected_waiver_continue` | {"jump": "continue_after_current_stage"} | <none> |
| 21 | `2026-06-04T02:47:13Z` | `<control>` | `0` | `iteration_repair_result` | {"accepted": false, "jump": "waiver_continue"} | current_hash=sha256:97e16b0096593bf5c3be671c14a9b339fe08773d840cc5c5f366ea01de706ff9 |
| 22 | `2026-06-04T02:47:13Z` | `<control>` | `0` | `waiver_continue_validation_enter` | {"reason": "SL-9 rejected/waived non-hard SD-4 requests; continue downstream without SC-11 DSL edit"} | current_dsl:len=7641,hash=sha256:97e16b009659 |
| 23 | `2026-06-04T02:47:13Z` | `SD-4` | `0` | `stage_result` | {"jump": "SL-5", "ok": true, "reason": "waiver_continue_design_items_marked_non_blocking_for_downstream_validation"} | <none> |
| 24 | `2026-06-04T02:47:13Z` | `SL-5` | `0` | `stage_enter` | {"reason": "scenario_set_absent"} | <none> |
| 25 | `2026-06-04T02:48:39Z` | `SL-5` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 26 | `2026-06-04T02:48:39Z` | `SD-5A` | `0` | `stage_result` | {"jump": "SL-5 retry", "ok": f
... <truncated 9514 chars in PR comment; see report.md>

#### Scenario 逐轮通过矩阵（report §6.1 摘录）

口径：`✅` = 该 scenario 在该轮 SD-6 simulation 通过；`❌` = 该轮失败；`⚪` = 该轮未执行或无该 scenario 结果。

| Scenario | Intent | Iter 1 | Iter 2 | Iter 3 | Iter 4 |
|---|---|---|---|---|---|
| `default_init_zero_load_no_res_selection` | default-init probe: with default PL=0 and no RES, EMS should select the zero-load no-renewable branch rather than chargi...<truncated 18 chars> | ❌ | ❌ | ❌ | ✅ |
| `zero_load_res_charge_below_full_soc` | explicit-hot-start probe: when PL=0, RES is available, and SoC is below 0.95, renewable production should charge the bat...<truncated 5 chars> | ✅ | ✅ | ✅ | ✅ |
| `zero_load_res_spare_at_full_soc` | explicit-hot-start SoC boundary probe: when PL=0 and SoC is exactly 0.95, RES production should become spare power, not ...<truncated 15 chars> | ✅ | ✅ | ✅ | ✅ |
| `res_covers_load_charge_below_full_soc` | explicit-hot-start probe: when RES covers nonzero load and SoC is below 0.95, demand is served by RES and only surplus c...<truncated 19 chars> | ✅ | ✅ | ✅ | ✅ |
| `res_covers_load_spare_at_full_soc` | explicit-hot-start SoC boundary probe: when RES covers nonzero load and SoC is exactly 0.95, surplus RES should be spare...<truncated 7 chars> | ✅ | ✅ | ✅ | ✅ |
| `battery_assist_suitable_soc_deficit_boundary` | explicit-hot-start probe: with RES below demand, SoC above the low threshold, and deficit within battery capacity, batte...<truncated 34 chars> | ✅ | ✅ | ✅ | ✅ |
| `lng_battery_cover_after_battery_capacity` | explicit-hot-start probe: when suitable-SoC battery capacity is insufficient but LNG capacity can cover the remaining de...<truncated 39 chars> | ✅ | ✅ | ✅ | ✅ |
| `lng_low_soc_charge_margin_at_threshold` | explicit-hot-start low-SoC boundary probe: at SoC=0.2, LNG-covered operation should include the Pgmax/5 battery charging...<truncated 8 chars> | ✅ | ✅ | ✅ | ✅ |
| `lng_dg3_cover_before_dg1_dg2` | explicit-hot-start priority probe: with suitable SoC and deficit beyond battery plus LNG but within DG3 capacity, LNG an...<truncated 45 chars> | ✅ | ✅ | ✅ | ✅ |
| `dg1_low_soc_pd1_charge_margin` | explicit-hot-start low-SoC diesel-margin probe: when LNG plus DG3 is insufficient at low SoC, DG1 branch should add the ...<truncated 24 chars> | ✅ | ✅ | ✅ | ✅ |
| `dg1_dg2_last_priority_high_soc` | explicit-hot-start priority probe: DG1/DG2 should be used only after RES, battery, LNG, and DG3 capacity are insufficien...<truncated 51 chars> | ✅ | ✅ | ✅ | ✅ |
| `overload_illegal_extreme_demand_outputs` | explicit-hot-start extreme-demand probe: overload completion is illegal in practice, but if selected it should activate ...<truncated 68 chars> | ✅ | ✅ | ✅ | ✅ |
| `forced_reselect_zero_load_no_res_from_active_generation` | explicit-hot-start forced-transition probe: from an active all-thermal state, PL=0 with no RES should globally reselect ...<truncated 104 chars> | ⚪ | ⚪ | ⚪ | ✅ |
| `forced_reselect_overload_to_zero_load_no_res` |  | ✅ | ✅ | ✅ | ⚪ |
| `forced_reselect_zero_load_to_res_covers_charge` |  | ✅ | ✅ | ✅ | ⚪ |

#### Repair / blocking feedback 概览（report §7 摘录）

口径：本节记录 agent-loop 真实进入 repair block 后的证据链：FixRequestBatch、SL-9 per-request accept/reject、candidate diff、local-check evidence、SL-10(NL+FixLog) 审阅，以及完整 FixLog ledger 摘录。

| Repair | iteration | accepted | source | blocking diagnostics | SL-9 decisions | SL-10 / local checks | candidate hash |
|---:|---:|---:|---|---|---|---|---|
| 1 | `0` | ❌ | `SD-4` | W_UNWRITTEN_READ_VAR:var_name=Pbatt_Pmax, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoad_RES_Charge:to_path=LNGShipEMS.Battery_Assist, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoad_RES_Charge:to_path=LNGShipEMS.LNG_Battery_Cover, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoad_RES_Charge:to_path=LNGShipEMS.LNG_DG3_Cover, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoad_RES_Charge:to_path=LNGShipEMS.DG1_DG2_LastPriority, ... +60 | accept=0, reject=12, waiver=12 | <none> | `sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 2 | `1` | ❌ | `SD-4` | W_UNWRITTEN_READ_VAR:var_name=Pbatt_Pmax, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoad_RES_Charge:to_path=LNGShipEMS.Battery_Assist, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoad_RES_Charge:to_path=LNGShipEMS.LNG_Battery_Cover, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoad_RES_Charge:to_path=LNGShipEMS.LNG_DG3_Cover, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoad_RES_Charge:to_path=LNGShipEMS.DG1_DG2_LastPriority, ... +60 | accept=0, reject=12, waiver=12 | <none> | `sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 3 | `2` | ✅ | `SD-6` | default_init_zero_load_no_res_selection | accept=1, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none>; local ok=False, target=False, regression=False, drift=major, local_stage=SD-10, reason=missing_required_grounding | `sha256:1a68d15d91fc5992f0c96a0ac46e11cc296b2bd387b99ec1731302e383d57e2a` |

> 完整 repair 细节、进入修复原因、SD-8 修改建议、SL-9 candidate、before→candidate diff 与 local-check evidence 与 SL-10 审查证据见 `../runs/pr_e1_real_agent_loop_round24_deepghs_stream_full_logs/pr-e1-path2_lng_ems-default-round24deepghsstream-cd202f61/report.md` §7。

</details>
