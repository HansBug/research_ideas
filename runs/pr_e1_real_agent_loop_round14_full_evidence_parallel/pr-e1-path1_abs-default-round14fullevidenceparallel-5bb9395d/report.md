## path1 / abs-fsm-brake-control / default 真实运行结果：Path1 ABS three-state brake supervisor

### 0. 准确边界与结论

- 运行入口：`method.loop.run_agent_loop(nl, LoopConfig(...))`。
- 是否使用 fake / fixture / hot-start / replay：否；本次使用真实默认入口/显式 PR-E1 探索条件，没有 fake、fixture、hot-start 或 replay。
- final verdict：`success`；record_status：`success`；result_status：`converged`。
- main_result_eligible：`true`。
- 一句话结论：`success`；停止原因：full_pass_all_required_feedback_ok。

### 1. 基本信息

| 字段 | 值 |
|---|---|
| Path | `path1` |
| case_id | `abs-fsm-brake-control` |
| config_id | `default` |
| 运行入口 | `method.loop.run_agent_loop(nl, LoopConfig(...))` |
| LoopConfig 摘要 | `condition_id=full_staged_v1`, `max_iterations=5`, `llm_max_retries=2`, `scenario_max_retries=2`, `model_review_mode=blocking_major_only`, `delta_review_mode=blocking_major_only` |
| Git commit | `024d87ea7ccf963350683efa08337a26a85c7b1d` |
| clean / diff / prompt snapshot | clean=`True`, dirty=`False`, diff_hash=`sha256:2a69ad5797ac568a81bddcef615104303a97261094685f4edd8d4484e889ea09`, prompt_hash=`sha256:0297eca601185761f335df788fe652c9a55156fa8e8100374f7291bbfc86e10b` |
| provider/model 脱敏标识 | mode=`real_env`, model=`gpt-5.5`, real_api=`True` |
| source / paper | source=`project_1_llm_state_machine_modeling/sources/abs-fsm-brake-control`, paper=`project_1_llm_state_machine_modeling/sources/abs-fsm-brake-control/paper.pdf` |
| 样本筛选理由 | 三态、guard、state action 均明确，适合检验 parse/semantic/design/sim 是否能走到后段。 |
| 变量参与说明 | `slp` 是 guard 变量；`k1/k2/n` 是状态动作输出，变量不是纯吉祥物。 |
| run_id | `pr-e1-path1_abs-default-round14fullevidenceparallel-5bb9395d` |
| final verdict/status | verdict=`success`, record=`success`, result=`converged` |
| main_result_eligible | `true` |
| token/cost/time | tokens=`{'prompt_tokens': 28726, 'completion_tokens': 6475, 'total_tokens': 35201, 'n_calls': 3}`, elapsed=`162.149s` |
| run record | [`pr-e1-path1_abs-default-round14fullevidenceparallel-5bb9395d.agent_loop.json.gz`](./pr-e1-path1_abs-default-round14fullevidenceparallel-5bb9395d.agent_loop.json.gz) |
| summary/log/final DSL | [`summary.json`](./summary.json), [`checks.json`](./checks.json), [`reproducibility.json`](./reproducibility.json), [`final.fcstm`](./final.fcstm), [`stdout.txt`](./run_logs/stdout.txt), [`stderr.txt`](./run_logs/stderr.txt) |

### 2. 输入 NL（多行原文）

```text
The paper implements the single-wheel ABS hydraulic regulator as a three-state FSM coupled with a PID-based slip controller. Wheel speed and vehicle speed are used to compute the slip ratio, and the PID output drives the Stateflow supervisor instead of sending commands directly to the hydraulic valves.

The FSM contains the states `increase`, `hold`, and `decrease`, where `increase` sets `k1=1, k2=0, n=0`, `hold` neutralizes both valves with `k1=0, k2=0, n=0`, and `decrease` sets `k1=0, k2=1, n=500` to release pressure.

The transition guards split the slip-error space into four bands: `increase -> hold` when `slp <= 0.01`, `hold -> increase` when `slp > 0.01`, `hold -> decrease` when `slp < -0.01`, and `decrease -> hold` when `slp >= -0.01`.

This gives a concrete discrete supervisor that maps slip-error thresholds to inlet-valve, return-valve, and pump actions while the continuous wheel-slip dynamics remain in the plant model.
```

### 2.1 输入 NL 中文翻译

```text
论文把单轮 ABS 液压调节器实现为一个三状态 FSM，并与基于滑移率的 PID 控制器耦合。轮速与车速用于计算滑移率，PID 输出驱动 Stateflow 监督器，而不是直接发送液压阀命令。

FSM 包含 `increase`、`hold`、`decrease` 三个状态：`increase` 设置 `k1=1, k2=0, n=0`，`hold` 设置 `k1=0, k2=0, n=0`，`decrease` 设置 `k1=0, k2=1, n=500` 以释放压力。

转移 guard 把滑移误差空间分成四个区间：`increase -> hold` 当 `slp <= 0.01`，`hold -> increase` 当 `slp > 0.01`，`hold -> decrease` 当 `slp < -0.01`，`decrease -> hold` 当 `slp >= -0.01`。

这给出了一个具体的离散监督器，把滑移误差阈值映射为进油阀、回油阀与泵动作，而连续轮胎滑移动力学仍留在被控对象模型中。
```

### 3. 最终产出的 FCSTM DSL

```pyfcstm
def float slp = 0.0;
def int k1 = 0;
def int k2 = 0;
def int n = 0;

state System {
    [*] -> increase;

    state increase {
        during {
            k1 = 1;
            k2 = 0;
            n = 0;
        }
    }

    state hold {
        during {
            k1 = 0;
            k2 = 0;
            n = 0;
        }
    }

    state decrease {
        during {
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

### 4. 全流程真实摘要表

| Stage | 是否 LLM | iteration | 结果 | 获取的信息 / 反馈 | 本阶段做了什么 | DSL 修改 | artifact/log |
|---|---:|---:|---:|---|---|---|---|
| `SC-0` | 否 | - | ✅ | trace/control | 初始化 run state | 无/见 record | [`record`](./pr-e1-path1_abs-default-round14fullevidenceparallel-5bb9395d.agent_loop.json.gz) |
| `SL-1` | 是 | - | ✅ | LLM calls=1, tokens=8203 | 生成初始 DSL 与 grounding seeds | initial len=611 | [`record`](./pr-e1-path1_abs-default-round14fullevidenceparallel-5bb9395d.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_abs-default-round14fullevidenceparallel-5bb9395d.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_abs-default-round14fullevidenceparallel-5bb9395d.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=17, info=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_abs-default-round14fullevidenceparallel-5bb9395d.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=1, tokens=12794 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_abs-default-round14fullevidenceparallel-5bb9395d.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_abs-default-round14fullevidenceparallel-5bb9395d.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_abs-default-round14fullevidenceparallel-5bb9395d.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_abs-default-round14fullevidenceparallel-5bb9395d.agent_loop.json.gz) |
| `SL-7` | 是 | 0 | ✅ | LLM calls=1, tokens=14204 | LLM model review | 无/见 record | [`record`](./pr-e1-path1_abs-default-round14fullevidenceparallel-5bb9395d.agent_loop.json.gz) |
| `SC-12` | 否 | - | ✅ | full_pass_all_required_feedback_ok | 写 final verdict | 无/见 record | [`record`](./pr-e1-path1_abs-default-round14fullevidenceparallel-5bb9395d.agent_loop.json.gz) |
| `SC-13` | 否 | - | ✅ | trace/control | 写审计 run record | 无/见 record | [`record`](./pr-e1-path1_abs-default-round14fullevidenceparallel-5bb9395d.agent_loop.json.gz) |

### 5. Iteration / repair / review 摘要

| Iter | selected feedback | repair? | SD-10 | SL-10B | 回到 SD-2? | verdict/备注 |
|---:|---|---|---|---|---|---|
| 0 | `<none>` | no | <none> | <none> | no | full_pass_all_required_feedback_ok |

### 6. Scenario 明细与逐轮通过情况

#### 6.1 Scenario pass/fail by iteration

口径：`✅` = 该 scenario 在该轮 SD-6 simulation 通过；`❌` = 该轮失败；`⚪` = 该轮未执行或无该 scenario 结果。

| Scenario | Intent | Iter 1 |
|---|---|---|
| `default_init_increase_then_hold_at_upper_boundary` | default-init dispatches to increase and, with slp exactly 0.01, the next cycle takes increase -> hold while checking bot...<truncated 24 chars> | ✅ |
| `increase_no_hold_above_upper_boundary` | explicit-hot-start in increase with slp just above 0.01 should not satisfy increase -> hold and should keep increase out...<truncated 12 chars> | ✅ |
| `hold_to_increase_above_upper_boundary` | explicit-hot-start in hold with slp greater than 0.01 should take hold -> increase and command inlet pressure increase. | ✅ |
| `hold_stays_at_upper_boundary` | explicit-hot-start in hold with slp exactly 0.01 should not take hold -> increase because that guard is strictly greater...<truncated 11 chars> | ✅ |
| `hold_to_decrease_below_lower_boundary` | explicit-hot-start in hold with slp less than -0.01 should take hold -> decrease and command pressure release. | ✅ |
| `hold_stays_at_lower_boundary` | explicit-hot-start in hold with slp exactly -0.01 should not take hold -> decrease because that guard is strictly less t...<truncated 10 chars> | ✅ |
| `decrease_to_hold_at_lower_boundary` | explicit-hot-start in decrease with slp exactly -0.01 should take decrease -> hold because the recovery guard is inclusi...<truncated 3 chars> | ✅ |
| `decrease_stays_below_lower_boundary` | explicit-hot-start in decrease with slp just below -0.01 should not satisfy decrease -> hold and should keep release-pre...<truncated 21 chars> | ✅ |

#### 6.2 Scenario definitions

<details><summary>`default_init_increase_then_hold_at_upper_boundary` — default-init dispatches to increase and, with slp exactly 0.01, the next cycle takes increase -> hold while checking both states' valve outputs.</summary>

| Field | Value |
|---|---|
| description | default-init dispatches to increase and, with slp exactly 0.01, the next cycle takes increase -> hold while checking both states' valve outputs. |
| initial_state | `<default-init>` |
| initial_vars | `{"slp": 0.01}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `initial_dispatch_to_increase` | `0` | `[]` | `System.increase` | `{"k1": 1, "k2": 0, "n": 0}` |
| 1 `increase_to_hold_at_slp_0_01` | `0` | `[]` | `System.hold` | `{"k1": 0, "k2": 0, "n": 0}` |

</details>

<details><summary>`increase_no_hold_above_upper_boundary` — explicit-hot-start in increase with slp just above 0.01 should not satisfy increase -> hold and should keep increase outputs active.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start in increase with slp just above 0.01 should not satisfy increase -> hold and should keep increase outputs active. |
| initial_state | `System.increase` |
| initial_vars | `{"slp": 0.0101}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `stay_in_increase_above_0_01` | `0` | `[]` | `System.increase` | `{"k1": 1, "k2": 0, "n": 0}` |

</details>

<details><summary>`hold_to_increase_above_upper_boundary` — explicit-hot-start in hold with slp greater than 0.01 should take hold -> increase and command inlet pressure increase.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start in hold with slp greater than 0.01 should take hold -> increase and command inlet pressure increase. |
| initial_state | `System.hold` |
| initial_vars | `{"slp": 0.0101}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `hold_to_increase_when_slp_gt_0_01` | `0` | `[]` | `System.increase` | `{"k1": 1, "k2": 0, "n": 0}` |

</details>

<details><summary>`hold_stays_at_upper_boundary` — explicit-hot-start in hold with slp exactly 0.01 should not take hold -> increase because that guard is strictly greater than 0.01.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start in hold with slp exactly 0.01 should not take hold -> increase because that guard is strictly greater than 0.01. |
| initial_state | `System.hold` |
| initial_vars | `{"slp": 0.01}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `hold_no_fire_at_slp_0_01` | `0` | `[]` | `System.hold` | `{"k1": 0, "k2": 0, "n": 0}` |

</details>

<details><summary>`hold_to_decrease_below_lower_boundary` — explicit-hot-start in hold with slp less than -0.01 should take hold -> decrease and command pressure release.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start in hold with slp less than -0.01 should take hold -> decrease and command pressure release. |
| initial_state | `System.hold` |
| initial_vars | `{"slp": -0.0101}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `hold_to_decrease_when_slp_lt_minus_0_01` | `0` | `[]` | `System.decrease` | `{"k1": 0, "k2": 1, "n": 500}` |

</details>

<details><summary>`hold_stays_at_lower_boundary` — explicit-hot-start in hold with slp exactly -0.01 should not take hold -> decrease because that guard is strictly less than -0.01.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start in hold with slp exactly -0.01 should not take hold -> decrease because that guard is strictly less than -0.01. |
| initial_state | `System.hold` |
| initial_vars | `{"slp": -0.01}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `hold_no_fire_at_slp_minus_0_01` | `0` | `[]` | `System.hold` | `{"k1": 0, "k2": 0, "n": 0}` |

</details>

<details><summary>`decrease_to_hold_at_lower_boundary` — explicit-hot-start in decrease with slp exactly -0.01 should take decrease -> hold because the recovery guard is inclusive.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start in decrease with slp exactly -0.01 should take decrease -> hold because the recovery guard is inclusive. |
| initial_state | `System.decrease` |
| initial_vars | `{"slp": -0.01}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `decrease_to_hold_when_slp_ge_minus_0_01` | `0` | `[]` | `System.hold` | `{"k1": 0, "k2": 0, "n": 0}` |

</details>

<details><summary>`decrease_stays_below_lower_boundary` — explicit-hot-start in decrease with slp just below -0.01 should not satisfy decrease -> hold and should keep release-pressure outputs active.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start in decrease with slp just below -0.01 should not satisfy decrease -> hold and should keep release-pressure outputs active. |
| initial_state | `System.decrease` |
| initial_vars | `{"slp": -0.0101}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `stay_in_decrease_below_minus_0_01` | `0` | `[]` | `System.decrease` | `{"k1": 0, "k2": 1, "n": 500}` |

</details>


### 7. Repair / blocking feedback 明细

- 本 run 未进入 `SD-8/SL-9/SD-10` repair block；通常表示流程在 repair 前已成功、被 provider/schema 错误中断，或在 pre-repair 阶段直接退出。

### 8. 尝试记录与成本

- `SL-1`：retry_count=`0`，schema_ok=`True`，usage=`{'completion_tokens': 2066, 'model': 'gpt-5.5', 'prompt_tokens': 6137, 'total_tokens': 8203}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'completion_tokens': 2407, 'model': 'gpt-5.5', 'prompt_tokens': 10387, 'total_tokens': 12794}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-7`：retry_count=`0`，schema_ok=`True`，usage=`{'completion_tokens': 2002, 'model': 'gpt-5.5', 'prompt_tokens': 12202, 'total_tokens': 14204}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。

### 9. 最终停止状态与后续含义

- 停止状态：verdict=`success`，record_status=`success`。
- 主要原因分类：`success`。
- required stages executed：`12/17`，missing=`SD-8, SL-9, SD-10, SL-10B, SC-11`。
- repairs：`0/0` accepted；scenario_history=`1`。
- 配置含义：`recommended baseline candidate`；该结果可用于评估默认入口本身。
- 样本含义：若出现 `design_or_variable_dynamics`，应重点审查变量是否仅作为 guard/input 常量而没有事件/动作更新；若出现 pre-scenario parse/semantic 失败，则应先优化 pyfcstm grammar adherence。
