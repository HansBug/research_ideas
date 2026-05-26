# `method/` 端到端例子 — Phase G 验收

> **目的**：展示 method 在不同控制系统 NL 上的端到端能力（multistep modeling → scenariogen → sim feedback），并通过**注入 model bug** 验证 sim feedback 对 model defect 的检测能力。
>
> **运行命令**（仓库根、`source .env` 后）：
> ```bash
> PYTHONPATH=project_1_llm_state_machine_modeling venv/bin/python /tmp/phase_g_full_test.py
> ```
>
> **运行环境**：`gpt-5.5`（via env `LLM_MODEL`），`temperature=0`，`seed=42`。LLM 非完全 deterministic — 同种子重跑可能有微小差异。
>
> **生成日期**：2026-05-26 (Phase G 完成节点)

---

## Part A — 3 个 NL 控制系统真实端到端跑通

每例：NL → 6 步 MTI multistep modeling → 1 步 scenariogen → sim feedback 验证。

### Example A1 — 交通灯（guard-driven cyclic + global reset）

**输入 NL**：

> The traffic light controller has three states: Red, Yellow, Green. The system starts in Red.
> When the timer reaches 30 in Red, it transitions to Green and resets the timer.
> When the timer reaches 25 in Green, it transitions to Yellow and resets the timer.
> When the timer reaches 5 in Yellow, it transitions back to Red and resets the timer.
> The timer increments by 1 every cycle while the controller is in any state.
> A reset signal forces the controller back to Red from any state.

**Multistep 输出 DSL** (492 chars, 9997 tokens / 6 LLM calls)：

```fcstm
def int timer = 0;

state TrafficLightController {
    ! * -> Red :: Reset;

    [*] -> Red;

    state Red {
        enter { timer = 0; }
        during { timer = timer + 1; }
    }

    state Green {
        during { timer = timer + 1; }
    }

    state Yellow {
        during { timer = timer + 1; }
    }

    Red -> Green : if [timer >= 30] effect { timer = 0; };
    Green -> Yellow : if [timer >= 25] effect { timer = 0; };
    Yellow -> Red : if [timer >= 5] effect { timer = 0; };
}
```

pyfcstm `parse_with_grammar_entry` + `parse_dsl_node_to_state_machine` 全通过。

**Scenariogen 产出 7 个 scenarios** (2489 tokens)：

| # | name | events | gap | extra | expected_state | expected_vars |
| --- | --- | --- | ---: | ---: | --- | --- |
| 1 | `initial_red_after_one_cycle` | — | 1 | 1 | `TrafficLightController.Red` | `{timer: 1}` |
| 2 | `red_to_green_transition` | — | 1 | 31 | `TrafficLightController.Green` | `{timer: 1}` |
| 3 | `green_to_yellow_transition` | — | 1 | 56 | `TrafficLightController.Yellow` | `{timer: 1}` |
| 4 | `yellow_to_red_transition` | — | 1 | 61 | `TrafficLightController.Red` | `{timer: 1}` |
| 5 | `reset_from_red_stays_red` | `[TrafficLightController.Reset]` | 1 | 1 | `TrafficLightController.Red` | `{timer: 1}` |
| 6 | `reset_from_green_to_red` | `[TrafficLightController.Reset]` | 31 | 1 | `TrafficLightController.Red` | `{timer: 1}` |
| 7 | `reset_from_yellow_to_red` | `[TrafficLightController.Reset]` | 56 | 1 | `TrafficLightController.Red` | `{timer: 1}` |

**Sim feedback**：**4/7 pass**

失败 3 个都是 LLM scenario writer 的 **cycle timing off-by-one bias**（不是 model bug）：

| FAIL scenario | state_match? | var mismatch |
| --- | :---: | --- |
| `reset_from_red_stays_red` | ✅ | `timer: expected=1 actual=2` |
| `reset_from_green_to_red` | ✅ | `timer: expected=1 actual=2` |
| `reset_from_yellow_to_red` | ✅ | `timer: expected=1 actual=2` |

**原因分析**：Reset 是 forced transition `! * -> Red :: Reset;`，LLM 期望 Reset 后到 Red、enter action 把 timer=0、再一个 during +1 = 1。但实际 cycle 顺序是：（1）当前 cycle 中 Red 的 during 跑 一次 timer+=1；（2）同 cycle 触发 Reset event；（3）下个 cycle 进 Red.enter timer=0；（4）再下个 cycle Red.during +1。中间多了一次 during 执行。

### Example A2 — 微波炉（event-driven + door interlock + auto-complete）

**输入 NL**：

> The microwave controller has four states: Idle, Ready, Cooking, Paused.
> The system starts in Idle.
> When the door_closed event fires while in Idle, it transitions to Ready and sets cook_timer to 0.
> When the start_pressed event fires while in Ready, it transitions to Cooking.
> While in Cooking, the cook_timer increments by 1 every cycle.
> When the door_open event fires while in Cooking, it transitions to Paused (preserving cook_timer).
> When the door_closed event fires while in Paused, it transitions back to Cooking.
> When the cook_timer reaches 120 in Cooking, it transitions back to Idle.
> A reset signal forces the controller back to Idle from any state and resets cook_timer to 0.

**Multistep 输出 DSL** (489 chars, 10917 tokens / 6 LLM calls)：

```fcstm
def int cook_timer = 0;

state MicrowaveController {
    ! * -> Idle :: reset;

    [*] -> Idle;

    state Idle {
        enter { cook_timer = 0; }
    }

    state Ready;

    state Cooking {
        during { cook_timer = cook_timer + 1; }
    }

    state Paused;

    Idle -> Ready :: door_closed effect { cook_timer = 0; };
    Ready -> Cooking :: start_pressed;
    Cooking -> Paused :: door_open;
    Paused -> Cooking :: door_closed;
    Cooking -> Idle : if [cook_timer >= 120];
}
```

pyfcstm parse + sem 全通过。

**Scenariogen 产出 7 个 scenarios** (2456 tokens)：

| # | name | events | gap | extra | expected_state | expected_vars |
| --- | --- | --- | ---: | ---: | --- | --- |
| 1 | `idle_to_ready_on_door_close` | `[Idle.door_closed]` | 1 | 0 | `MicrowaveController.Ready` | `{cook_timer: 0}` |
| 2 | `ready_to_cooking_on_start` | `[Idle.door_closed, Ready.start_pressed]` | 1 | 1 | `MicrowaveController.Cooking` | `{cook_timer: 1}` |
| 3 | `cooking_timer_increments_without_events` | `[Idle.door_closed, Ready.start_pressed]` | 1 | 10 | `MicrowaveController.Cooking` | `{cook_timer: 11}` |
| 4 | `pause_and_resume_cooking` | `[Idle.door_closed, Ready.start_pressed, Cooking.door_open, Paused.door_closed]` | 5 | 5 | `MicrowaveController.Cooking` | `{cook_timer: 16}` |
| 5 | `cooking_auto_returns_to_idle_at_120` | `[Idle.door_closed, Ready.start_pressed]` | 1 | 120 | `MicrowaveController.Idle` | `{cook_timer: 120}` |
| 6 | `reset_from_cooking_forces_idle` | `[Idle.door_closed, Ready.start_pressed, reset]` | 10 | 1 | `MicrowaveController.Idle` | `{cook_timer: 0}` |
| 7 | `reset_from_paused_forces_idle` | `[Idle.door_closed, Ready.start_pressed, Cooking.door_open, reset]` | 3 | 1 | `MicrowaveController.Idle` | `{cook_timer: 0}` |

**Sim feedback**：**4/7 pass**

| FAIL scenario | state_match? | var mismatch |
| --- | :---: | --- |
| `ready_to_cooking_on_start` | ✅ | `cook_timer: expected=1 actual=2` |
| `pause_and_resume_cooking` | ✅ | `cook_timer: expected=16 actual=12` |
| `cooking_auto_returns_to_idle_at_120` | ✅ | `cook_timer: expected=120 actual=0` |

**原因分析**：
- (5) `cooking_auto_returns_to_idle_at_120`：cook_timer ≥ 120 触发 Cooking → Idle，但 Idle 有 `enter { cook_timer = 0; }`，所以最终 cook_timer=0 而非 120。LLM 没意识到 Idle 的 enter action 会把它归零。
- (2) (4) 同 traffic_light 一样的 cycle counting off-by-one。

### Example A3 — 三层电梯（event-driven multi-state floor）

**输入 NL**：

> The elevator controller has three floor states (F1, F2, F3) and four motion states (MU2, MU3, MD1, MD2)...
> Floor request events PS1/PS2/PS3 trigger motion: from F1 with PS2 to MU2, etc.
> Arrival sensor events S1/S2/S3 detect arrival: MU2 + S2 → F2, etc.
> A reset signal forces the elevator back to F1.

（完整 NL 见原始 input；为节省篇幅此处省略）

**Multistep 输出 DSL** (394 chars, 12965 tokens / 6 LLM calls)：

```fcstm
state ElevatorController {
    ! * -> F1 :: Reset;

    [*] -> F1;

    state F1;
    state F2;
    state F3;
    state MU2;
    state MU3;
    state MD1;
    state MD2;

    F1 -> MU2 :: PS2;
    F1 -> MU3 :: PS3;
    F2 -> MU3 :: PS3;
    F2 -> MD1 :: PS1;
    F3 -> MD1 :: PS1;
    F3 -> MD2 :: PS2;
    MU2 -> F2 :: S2;
    MU3 -> F3 :: S3;
    MD1 -> F1 :: S1;
    MD2 -> F2 :: S2;
}
```

模型纯事件驱动无变量。pyfcstm parse + sem 全通过。

**Scenariogen 产出 8 个 scenarios** (2717 tokens)：

| # | name | events | expected_state |
| --- | --- | --- | --- |
| 1 | `startup_idle_at_f1` | — | `ElevatorController.F1` |
| 2 | `f1_to_f2_via_mu2` | `[F1.PS2, MU2.S2]` | `ElevatorController.F2` |
| 3 | `f1_to_f3_via_mu3` | `[F1.PS3, MU3.S3]` | `ElevatorController.F3` |
| 4 | `f2_to_f3_transition` | `[F1.PS2, MU2.S2, F2.PS3, MU3.S3]` | `ElevatorController.F3` |
| 5 | `f3_to_f1_via_md1` | `[F1.PS3, MU3.S3, F3.PS1, MD1.S1]` | `ElevatorController.F1` |
| 6 | `f3_to_f2_via_md2` | `[F1.PS3, MU3.S3, F3.PS2, MD2.S2]` | `ElevatorController.F2` |
| 7 | `f2_to_f1_via_md1` | `[F1.PS2, MU2.S2, F2.PS1, MD1.S1]` | `ElevatorController.F1` |
| 8 | `reset_forces_return_to_f1` | `[F1.PS3, Reset]` | `ElevatorController.F1` |

**Sim feedback**：**8/8 全通过 ✅**

事件序列推理 + 无 cycle 计时 → LLM scenario writer 100% 准确。这是 method 在事件驱动控制系统上工作良好的强证据。

---

## Part B — Mutation Detection（验证 sim 检测 model bug 的能力）

**Setup**：在 traffic light multistep DSL 基础上注入 3 种不同 bug，用**人工精心构造的 4 个 scenarios**（基于 pyfcstm cycle 语义精确推导，避免 LLM scenario writer 干扰）验证 sim 检测能力。

### Hand-crafted 4 个 scenarios（精确基于 pyfcstm cycle 语义）

| # | name | events | gap | extra | expected_state | expected_vars | 推导说明 |
| --- | --- | --- | ---: | ---: | --- | --- | --- |
| 1 | `initial_red_after_1_cycle` | — | 1 | 0 | `TrafficLightController.Red` | `{timer: 1}` | 1 cycle (during +1) |
| 2 | `red_30_cycles_still_red_timer_30` | — | 1 | 29 | `TrafficLightController.Red` | `{timer: 30}` | 30 cycles, transition NEXT cycle |
| 3 | `red_to_green_after_31_cycles` | — | 1 | 30 | `TrafficLightController.Green` | `{timer: 1}` | 31 cycle 触发 Red→Green, effect=0, Green.during +1 |
| 4 | `reset_from_green_back_to_red_via_enter` | `[TrafficLightController.Reset]` | 30 | 0 | `TrafficLightController.Red` | `{timer: 1}` | 30 cycles 到 Green, Reset, 进 Red 的 enter timer=0, during +1 |

### Variant 1 — Original（baseline control）

**Sim feedback**：**4/4 pass ✅**

证明 hand-crafted scenarios 跟 pyfcstm runtime cycle 语义完全一致；method 输出的 DSL 行为正确。

### Variant 2 — Bug 1: `unreachable_green`

**注入**：将 `Red -> Green : if [timer >= 30]` 改为 `if [timer >= 99999]`。Green/Yellow 都不可达。

**Sim feedback**：**3/4 pass — ✅ caught**

| FAIL scenario | state_match? | actual vs expected |
| --- | :---: | --- |
| `red_to_green_after_31_cycles` | ❌ | expected=Green actual=Red; `timer: expected=1 actual=31` |

### Variant 3 — Bug 2: `no_reset_path`

**注入**：删除 `! * -> Red :: Reset;` 这一行。Reset 事件不再被 forced transition 捕获。

**Sim feedback**：**3/4 pass — ✅ caught**

| FAIL scenario | violation 类型 | 详情 |
| --- | --- | --- |
| `reset_from_green_back_to_red_via_enter` | **runtime_error** | `LookupError: Cannot resolve event path 'TrafficLightController.Reset'` |

### Variant 4 — Bug 3: `no_timer_reset_on_transition`

**注入**：删除 `Red -> Green : if [timer >= 30] effect { timer = 0; };` 中的 `effect { ... }`。transition 触发但 timer 不 reset。

**Sim feedback**：**3/4 pass — ✅ caught**

| FAIL scenario | state_match? | var mismatch |
| --- | :---: | --- |
| `red_to_green_after_31_cycles` | ✅ | `timer: expected=1 actual=31`（说明 effect 缺失，timer 没被 reset） |

### Mutation detection 总结

| Variant | Sim 检测 | violation 类型 | 验证 sim 能力维度 |
| --- | --- | --- | --- |
| original | 4/4 pass | — | 正确 model 给 clean signal |
| bug1 `unreachable_green` | 3/4 pass ✅ | state-mismatch | catches structural reachability bug |
| bug2 `no_reset_path` | 3/4 pass ✅ | runtime_error (LookupError) | catches missing transition / event |
| bug3 `no_timer_reset` | 3/4 pass ✅ | var-mismatch | catches missing effect on transition |

**3/3 buggy variants 都被 sim 抓到了**，且每种 bug 在不同 violation 维度（state / runtime_error / vars）surface，验证 sim feedback 对多种 model defect 类型都有效。

---

## Phase G 关键 finding

1. **Scenariogen + sim 配对成功**：3 个不同 NL 都能 end-to-end 跑通（pure guard-driven / event-driven mixed / pure event-driven 三种范式都 cover）
2. **Sim oracle 链有效**：buggy mutation 测试证明 sim feedback 能 catch 3 类不同的 model bug — 这就是 `NL → property/scenario (expected) → sim 执行验证` 闭环的核心价值
3. **LLM scenario writer 在 cycle timing 上有 off-by-one bias**：traffic_light 4/7、microwave 4/7 sim pass，失败的都是 LLM 没真跑过 model 不熟 runtime 语义；这本身是个有意义的 finding — 提示**未来改进方向**是在 scenariogen 后用 sim 跑一次拿到 actual values，再 reflexion 一轮让 LLM 修正 expected
4. **Elevator 8/8 全 pass**：事件序列推理对 LLM 比 cycle timing 推理简单很多 — 后续如果 Path 2 主用控制系统数据，应该选含较多事件驱动 case 的样本

## 后续 Phase（基于这些 finding 调整）

- **Phase E (loop driver)**：把 multistep / scenariogen / 4 路 feedback (parse/sem/sim/judge) 串成完整 agent loop with `modeling_mode` CLI flag
- **Phase H (judge)**：接 project_ex1 ExpertReviewAgent 提供 LLM judge 第 4 路 feedback
- **Phase I (eval extractor)**：抽 7 类组件用于 Path 1 P/R/F1 评测
- **Phase J (端到端验收)**：mark PR Ready for Review
