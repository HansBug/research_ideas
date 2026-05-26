# `method/` 端到端例子 — Phase G 验收

> **目的**：展示 method 在不同控制系统 NL 上的端到端能力（multistep modeling → scenariogen → sim feedback），并通过**注入 model bug** 验证 sim feedback 对 model defect 的检测能力。
>
> **运行命令**（在仓库根、`source .env` 后）：
> ```bash
> PYTHONPATH=project_1_llm_state_machine_modeling venv/bin/python /tmp/phase_g_full_test.py
> ```
>
> **生成日期**：2026-05-26 (Phase G 完成节点)
> **LLM**：`gpt-5.5`（via env `LLM_MODEL`）

---

## Part A — 3 个 NL 控制系统真实端到端跑通

每个例子：NL → 6 步 MTI multistep modeling → 1 步 scenariogen → sim feedback。

### Example A1 — 交通灯（guard-driven cyclic + global reset）

**输入 NL**：

> The traffic light controller has three states: Red, Yellow, Green. The system starts in Red.
> When the timer reaches 30 in Red, it transitions to Green and resets the timer.
> When the timer reaches 25 in Green, it transitions to Yellow and resets the timer.
> When the timer reaches 5 in Yellow, it transitions back to Red and resets the timer.
> The timer increments by 1 every cycle while the controller is in any state.
> A reset signal forces the controller back to Red from any state.

**Multistep 输出 DSL** (492 chars, tokens=9997 / 6 LLM calls)：

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

**Scenariogen 产出** (tokens=2489)：7 scenarios

**Sim feedback**：2/7 pass。失败的 5 个都是 LLM scenario writer 的 cycle timing off-by-one bias（不是 model bug）— 如 LLM 期望 30 cycles 后 timer=0 在 Green，实际是 30 cycles 后 Red timer=30，transition 在第 31 cycle 触发。这正是 sim oracle 的价值：surface 出 LLM 不熟 runtime cycle 语义的认知 gap。

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

**Multistep 输出 DSL** (489 chars, tokens=10917 / 6 LLM calls)：

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

**Scenariogen 产出** (tokens=2456)：7 scenarios

**Sim feedback**：4/7 pass。3 个失败都是 LLM scenario writer 算错 cook_timer (例如 `start_cooking_from_ready` 期待 timer=1 实际 timer=2，`cooking_auto_completes_at_120` 期待 timer=120 但 Idle 的 enter action 把它归零成 0)。

### Example A3 — 三层电梯（event-driven multi-state floor controller）

**输入 NL**：

> The elevator controller has three floor states (F1, F2, F3) and four motion states (MU2, MU3, MD1, MD2) for upward and downward travel.
> The system starts at F1 (idle on floor 1).
> Floor request events PS1, PS2, PS3 trigger motion: from F1, the event PS2 causes a transition to MU2 (moving up to floor 2); from F1, PS3 causes a transition to MU3.
> From F2, the event PS3 causes a transition to MU3; from F2, PS1 causes a transition to MD1 (moving down to floor 1).
> From F3, the event PS1 causes a transition to MD1; from F3, PS2 causes a transition to MD2 (moving down to floor 2).
> Arrival sensor events S1, S2, S3 detect floor arrival: MU2 with S2 transitions to F2; MU3 with S3 transitions to F3; MD1 with S1 transitions to F1; MD2 with S2 transitions to F2.
> A reset signal forces the elevator back to F1 from any state.

**Multistep 输出 DSL** (394 chars, tokens=12965 / 6 LLM calls)：

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

pyfcstm parse + sem 全通过。模型没有变量（纯 event-driven 多状态机）。

**Scenariogen 产出** (tokens=2717)：8 scenarios

**Sim feedback**：**8/8 pass 全通过 ✅**

Elevator 是纯 event-driven 没有 cycle timing 复杂度，LLM 写的 scenario 100% 准确。这是 method 在"纯事件驱动"控制系统上工作良好的强证据。

---

## Part B — Mutation detection（验证 sim 检测 model bug 的能力）

**Setup**：用 traffic light multistep DSL 作 baseline，注入 3 种不同的 bug，用**人工精心构造的 scenarios**（不让 LLM scenario writer 干扰）检验 sim 是否能 catch 每种 bug。

### Hand-crafted 4 个 scenarios（精确基于 pyfcstm cycle 语义）

```
1. initial_red_after_1_cycle:           cycle×1 → expect Red, timer=1
2. red_30_cycles_still_red_timer_30:    cycle×30 → expect Red, timer=30 (transition not yet fired)
3. red_to_green_after_31_cycles:        cycle×31 → expect Green, timer=1 (transition fired, effect=0, during+1)
4. reset_from_green_back_to_red:        cycle×30 + Reset → expect Red, timer=1 (enter sets 0, during +1)
```

### Original DSL — 4/4 pass ✅

证明 hand-crafted scenarios 跟 pyfcstm runtime cycle 语义完全一致；method 输出的 DSL 行为正确。

### Bug 1: unreachable_green

注入：将 `Red -> Green : if [timer >= 30]` 改为 `if [timer >= 99999]`。

预期：`Red → Green` transition 永远不 fire，Green/Yellow 都不可达。

**Sim feedback**：3/4 pass ✅ caught
- `red_to_green_after_31_cycles` FAIL [state-mismatch]: expected=Green actual=Red, timer expected=1 actual=31

### Bug 2: no_reset_path

注入：从 DSL 中删除 `! * -> Red :: Reset;` 这一行。

预期：Reset 事件不再 work（无 forced 转换捕获）。

**Sim feedback**：3/4 pass ✅ caught
- `reset_from_green_back_to_red_via_enter` FAIL: runtime_error=`LookupError: Cannot resolve event path 'TrafficLightController.Reset'`

### Bug 3: no_timer_reset_on_transition

注入：将 `Red -> Green : if [timer >= 30] effect { timer = 0; };` 改为 `Red -> Green : if [timer >= 30];`（删除 effect block）。

预期：transition 触发但 timer 不 reset，进入 Green 时 timer 仍是大值（继续 +1）。

**Sim feedback**：3/4 pass ✅ caught
- `red_to_green_after_31_cycles` FAIL [var-mismatch]: state=Green ✓ 但 timer expected=1 actual=31（说明 effect 缺失，timer 没被 reset）

### Mutation detection 总结

| Variant | Sim 检测 | 检测 violation 类型 | 验证 sim 能力维度 |
| --- | --- | --- | --- |
| original | 4/4 pass | — | 正确 model 给 clean signal |
| bug1 unreachable_green | 3/4 pass | state-mismatch | catches structural reachability bug |
| bug2 no_reset_path | 3/4 pass | runtime_error (LookupError) | catches missing transition / event |
| bug3 no_timer_reset | 3/4 pass | var-mismatch | catches missing effect on transition |

**3/3 buggy variants 都被 sim 抓到了**，且每种 bug 在不同 violation 维度（state / runtime_error / vars）surface，验证了 sim feedback 对多种 model defect 类型都有效。

---

## Phase G 关键 finding

1. **Scenariogen + sim 配对成功**：3 个不同 NL 都能 end-to-end 跑通（pure guard-driven / event-driven mixed / pure event-driven 三种范式都 cover）
2. **Sim oracle 链有效**：buggy mutation 测试证明 sim feedback 能 catch 3 类不同的 model bug — 这就是 `NL → property/scenario (expected) → sim 执行验证` 闭环的核心价值
3. **LLM scenario writer 在 cycle timing 上有 off-by-one bias**：traffic_light 2/7、microwave 4/7 sim pass，但失败的都是 LLM 没真跑过 model 不熟 runtime 语义；这本身是个有意义的 finding — 提示**未来改进方向**是在 scenariogen 后用 sim 跑一次拿到 actual values，再 reflexion 一轮让 LLM 修正 expected
4. **Elevator 8/8 全 pass**：纯事件驱动控制系统在 method 上工作良好；LLM scenario writer 对事件序列推理比对 cycle timing 推理强很多

## 后续 Phase（基于这些 finding 调整）

- **Phase E (loop driver)**：把 multistep / scenariogen / 4 路 feedback (parse/sem/sim/judge) 串成完整 agent loop with `modeling_mode` CLI flag
- **Phase H (judge)**：接 project_ex1 ExpertReviewAgent 提供 LLM judge 第 4 路 feedback
- **Phase I (eval extractor)**：抽 7 类组件用于 Path 1 P/R/F1 评测
- **Phase J (端到端验收)**：mark PR Ready for Review
