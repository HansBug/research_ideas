# `method/` 端到端例子 — Phase G v3 (bug-finding scenarios)

> **目的**：展示 method 端到端能力（multistep modeling → scenariogen → sim feedback），并通过 **6 类 mutation 的 differential detection matrix** 验证 sim feedback 抓 bug 的能力。
>
> **核心定位（v3 修正）**：scenario+sim 阶段的意义是 **发现错误供 agent loop 修复**，因此 scenarios 是 **bug 探针** 而非"匹配 sim 行为的镜像"。LLM 在 prompt 引导下同时承担两个目标：
> - **NL 元素覆盖**（每个 state / event / transition / variable 都被探到）
> - **bug-finding probes**（guard 边界、错误目标、错误副作用、forced 路径、no-fire 保持 等）
>
> **运行命令**（仓库根、`set -a; source .env; set +a` 后）：
> ```bash
> cd project_1_llm_state_machine_modeling && PYTHONPATH=. python3 /tmp/phase_g_v3_test.py
> ```
>
> **运行环境**：via env `LLM_MODEL`，`temperature=0`，`seed=42`。LLM 非完全 deterministic — 同种子重跑可能有微小差异。
>
> **生成日期**：2026-05-26（Phase G v3 节点）

---

## Part A — 3 个 NL 控制系统：LLM scenarios 同时满足"覆盖 + 探 bug"

每例：NL → 6 步 MTI multistep modeling → 1 步 scenariogen → sim feedback 在 original 模型上跑。

### Example A1 — 交通灯（guard-driven cyclic + global reset）

**输入 NL**：

> The traffic light controller has three states: Red, Yellow, Green. The system starts in Red.
> When the timer reaches 30 in Red, it transitions to Green and resets the timer.
> When the timer reaches 25 in Green, it transitions to Yellow and resets the timer.
> When the timer reaches 5 in Yellow, it transitions back to Red and resets the timer.
> The timer increments by 1 every cycle while the controller is in any state.
> A reset signal forces the controller back to Red from any state.

**生成的 DSL**（model_tokens=9814）：

```
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

**LLM 生成的 8 个 scenarios**（sc_tokens=5774）：

| # | scenario | 类型 | init | 关键 checkpoint |
| --- | --- | --- | --- | --- |
| 1 | `default_initialization_enters_red` | init-cov | default-init | `Red/timer=1` (cycle 1) → `Red/timer=5` (after 3 more cycles) |
| 2 | `red_guard_boundary_probe` | **guard 边界** | `Red/timer=28` | `timer=29` 不应 fire；后续应 fire 到 Green |
| 3 | `green_guard_boundary_probe` | **guard 边界** | `Green/timer=23` | `timer=24` 不应 fire；后续应 fire 到 Yellow |
| 4 | `yellow_guard_boundary_probe` | **guard 边界** | `Yellow/timer=3` | `timer=4` 不应 fire；后续应 fire 到 Red |
| 5 | `full_cycle_through_all_states` | path-cov | default-init | 30 cycles → Green → 24 cycles → Yellow → 4 cycles → Red |
| 6 | `reset_forces_red_from_green` | **forced-event** | `Green/timer=12` | Reset → Red/timer=1 → 持续 increment |
| 7 | `reset_forces_red_from_yellow` | **forced-event** | `Yellow/timer=4` | Reset 中断 pending transition → Red/timer=1 |
| 8 | `no_fire_below_all_thresholds` | **no-fire probe** | `Green/timer=10` | 5 cycles 后仍 Green/timer=16；events=None 不前进 |

**sim 在 original 上的结果：5/8 pass，3 个 boundary probe FAIL**

⚠️ **3 个 boundary probe 的 fail 不是 bug，是 LLM scenarios 抓出的"NL-model 语义 gap"**：

- NL 字面："When the timer reaches 30, it transitions to Green"（"到达 30 时就转")
- model 写法：`Red -> Green : if [timer >= 30]`，pyfcstm 在 cycle 开头按 pre-during vars 评估 guard，导致 `timer=29` (pre-during) 的 cycle 内 `during` 把它推到 30 但 guard 已用 29 判断为 false，下一 cycle (timer=30 pre-during) 才 fire
- 实际行为：transition 比 NL 字面 phrasing **晚 1 个 cycle**
- 这是 **agent loop 应该捕捉并修复的语义不一致**（要么把 NL 解读成"达到 31 才转"，要么把 model guard 改成 `>= 29`，要么把 evaluation 顺序换成 post-during）

这正好印证 **scenarios 作为 NL-grounded 探针** 的价值 — 不需要写错就能 surface 出 modeler 阶段未察觉的语义 gap。

### Example A2 — 微波炉（hybrid event-/guard-driven + 状态保留）

**输入 NL**：8 行 NL（Idle/Ready/Cooking/Paused 4 状态，door_closed/start_pressed/door_open/reset 4 事件，cook_timer 累加 + 到 120 自动归位 Idle）

**生成的 DSL**（model_tokens=10932）：

```
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

**LLM 生成的 8 个 scenarios**（sc_tokens=5197），覆盖：default-init / Idle→Ready / Ready→Cooking / Cooking 计时器 / Cooking 边界 119 不 fire+120 fire / 暂停-恢复保留 timer / forced reset from Ready / forced reset from Paused。**sim 结果：8/8 pass**。

> 微波炉 model 的 guard `cook_timer >= 120` + `during cook_timer += 1` 与 LLM scenario `init cook_timer=120` 直接 fire 一致 — 没有 1-cycle gap。LLM 学会了**针对不同 guard 类型选择合适的 hot-start 值**（traffic light 用 `timer=N-1` + 等 during 推；microwave 直接 hot-start 在 N=120）。

### Example A3 — 三层电梯（multi-state path + 多源 forced）

**输入 NL**：3 楼电梯，4 motion state（MU2/MU3/MD1/MD2），floor-request 事件 PS1/PS2/PS3 触发 motion，arrival 传感器 S1/S2/S3 完成路径，全局 Reset。

**生成的 DSL**（model_tokens=12597）：

```
state ElevatorController {
    [*] -> F1;

    ! * -> F1 :: Reset;

    state F1; state F2; state F3;
    state MU2; state MU3; state MD1; state MD2;

    F1 -> MU2 :: PS2;   F1 -> MU3 :: PS3;
    F2 -> MU3 :: PS3;   F2 -> MD1 :: PS1;
    F3 -> MD1 :: PS1;   F3 -> MD2 :: PS2;
    MU2 -> F2 :: S2;    MU3 -> F3 :: S3;
    MD1 -> F1 :: S1;    MD2 -> F2 :: S2;
}
```

**LLM 生成的 8 个 scenarios**（sc_tokens=6213）：default-init + 6 条 floor-motion-floor path（覆盖全部 6 个 floor 转 motion 转换、全部 4 个 motion-to-floor arrival）+ 1 个 reset_forces_f1_from_multiple_states（从 F3 / motion 状态各 reset 一次，多源覆盖）。**sim 结果：8/8 pass**。

---

## Part B — Differential Mutation Detection（核心评估）

把 Part A 的 traffic_light **LLM-generated 8 scenarios** 直接拿来，跑在 **1 个 original + 6 个 mutation variants** 上，看每个 mutation 是否被 scenarios catch。

### 6 个 mutation 设计（按 LLM 常见 bug 类型）

| ID | Mutation | DSL 修改 | 期望被哪类 probe 捕捉 |
| --- | --- | --- | --- |
| **M0** | original | (no change) | (baseline, 3 个 boundary probes 已 fail surface NL-model gap) |
| **M1** | guard off-by-one | `timer >= 30` → `timer >= 29` (1 cycle 提早) | guard boundary probe + full-cycle path |
| **M2** | wrong target state | `Red -> Green` → `Red -> Yellow` (跳过 Green) | full-cycle path（应到 Green 实到 Yellow） |
| **M3** | unreachable target | `timer >= 30` → `timer >= 99999` (Green 永远不可达) | full-cycle path（应到 Green 实留 Red） |
| **M4** | missing forced reset | 删除 `! * -> Red :: Reset` | 2 个 forced-event probe（应 caught 为 `LookupError` 运行时错误） |
| **M5** | missing effect reset | `Red -> Green effect{timer=0;}` 去 effect | full-cycle path（timer 不 reset，下游 timer 偏移） |
| **M6** | wrong effect value | `effect{timer=0}` → `effect{timer=100}` (副作用值错) | full-cycle path（timer=101 而非 1） |

### Differential Detection Matrix

`✓` = pass，`✗` = fail，`E` = runtime error。每列是 1 个 model variant，每行是 LLM 写的 1 个 scenario。

| scenario | M0 | M1 | M2 | M3 | M4 | M5 | M6 |
| --- | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| `default_initialization_enters_red` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| `red_guard_boundary_probe` | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ |
| `green_guard_boundary_probe` | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| `yellow_guard_boundary_probe` | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| `full_cycle_through_all_states` | ✓ | ✗ | ✗ | ✗ | ✓ | ✗ | ✗ |
| `reset_forces_red_from_green` | ✓ | ✓ | ✓ | ✓ | **E** | ✓ | ✓ |
| `reset_forces_red_from_yellow` | ✓ | ✓ | ✓ | ✓ | **E** | ✓ | ✓ |
| `no_fire_below_all_thresholds` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |

### Per-mutation detection（≥1 个**新增** violation = caught ✓）

| Mutation | new violations (M0→Mx) | total violations | 结果 | 哪个 scenario 抓到 |
| --- | :-: | :-: | :-: | --- |
| **M1** guard off-by-one | 1 | 3 | ✓ caught | `full_cycle_through_all_states` step 0 vars timer=2≠1（提早 1 cycle fire，残留 1 step during） |
| **M2** wrong target state | 1 | 4 | ✓ caught | `full_cycle_through_all_states` step 0 state Yellow≠Green |
| **M3** unreachable target | 1 | 4 | ✓ caught | `full_cycle_through_all_states` step 0 state Red≠Green & timer=31≠1 |
| **M4** missing forced reset | 2 | 5 | ✓ caught | `reset_forces_red_from_green` + `reset_forces_red_from_yellow` 双双 **LookupError: Cannot resolve event path 'TrafficLightController.Reset'** |
| **M5** missing effect reset | 1 | 4 | ✓ caught | `full_cycle_through_all_states` step 0 timer=31≠1（effect 没 reset，timer 累积到 Green） |
| **M6** wrong effect value | 1 | 4 | ✓ caught | `full_cycle_through_all_states` step 0 timer=101≠1（effect 值改成 100，during +1 = 101） |

**结论：6/6 mutations 全部被 LLM 自动生成的 scenarios 捕捉到**，且每个 mutation 的 "discriminating scenario"（在 original 上 pass 但在 buggy variant 上 fail/error）能直接告诉 agent loop 哪类 bug：

- 状态错误 (M2/M3) → state assertion mismatch
- 副作用错误 (M5/M6) → var_mismatches 中的 specific var 与 expected/actual
- 路径缺失 (M4) → runtime LookupError（事件路径不存在 = 模型缺 transition）
- 边界 timing (M1) → var_mismatches `timer=2` 而非 1（提早 1 cycle 后还多 during 一次）

这种**分类化、可机读的 violation 信号**正是 Repair agent 在下游 loop 需要消费的 feedback。

---

## Part C — Original 上的 5/8 pass 解读：sim feedback 的"bonus" 价值

3 个 guard_boundary_probe scenario 在 **all variants（包括 M0 original）** 上都 fail。这不是 LLM 写错，而是 LLM 的 NL-literal phrasing（"when timer reaches N transitions"）和 pyfcstm `if [timer >= N]` + pre-during 评估顺序的**真实语义 gap**。

```
hot-start: Red, timer=28
  step 0 [threshold_minus_one_stays_red]: bc=0 events=[]
    expect: Red, timer=29   (LLM expectation: during +1 = 29, 29 < 30 还在 Red ✓)
    actual: Red, timer=29   ✓ PASS

  step 1 [threshold_reached_transitions_green]: bc=0 events=[]
    expect: Green, timer=1  (LLM: after during +1 = 30, 30 >= 30 应 fire Red->Green, effect timer=0, Green during +1)
    actual: Red, timer=30   ✗ FAIL
    解释: pyfcstm 在 cycle 开头用 pre-during timer=29 评估 guard, 29 < 30 不 fire, during 推到 30, 留在 Red
```

这种**模型行为与 NL 字面意图之间的细微差** — 是 LLM 写代码时无意识引入的 off-by-one — sim 通过让 LLM 用 NL 语言写 scenario 自然 surface 出来。**这是 v3 prompt design 的意外收获**：不只检测 mutation，还能检测 modeler 自己引入的 NL-model gap，给 agent loop 提供 repair 机会。

---

## Token usage 总结

| Example | model_tokens | scenariogen_tokens | scenarios | sim pass/total |
| --- | --- | --- | --- | --- |
| traffic_light | 9,814 | 5,774 | 8 | 5/8 (3 个 NL-model gap fail) |
| microwave | 10,932 | 5,197 | 8 | 8/8 |
| elevator_3floor | 12,597 | 6,213 | 8 | 8/8 |

**Part B differential**: 1 套 LLM scenarios × 6 mutations = **6/6 全部被 catch**。

---

## v3 vs v1/v2 对比（叙事演变）

| 版本 | 主要 metric | 评估理念 |
| --- | --- | --- |
| v1 (initial) | "scenarios 在 original 上的 pass rate" | ❌ 把"匹配 sim"当成功，把 LLM cycle off-by-one 当 noise |
| v2 (sched refactor) | 同 v1 + multi-step schema | ❌ prompt 教 LLM cycle semantics 让 scenarios 100% pass — scenarios 变成 sim 行为镜像 |
| **v3 (current)** | **differential mutation detection rate** + NL element coverage | ✓ scenarios 是 NL-driven bug probes，pass rate 不是目标，**catch bug 才是**；original 上的 fail 也是有价值的 finding |

---

## 输入/输出资产路径

- **测试脚本**：`/tmp/phase_g_v3_test.py`（含 6 个 mutation 的 regex-based mutator）
- **完整 JSON 结果**：`/tmp/phase_g_v3_results.json`（含每个 scenario 的全部 step results、actual_state、actual_vars、var_mismatches、runtime_error）
- **prompt**：[`prompts/scenariogen/generate_scenarios.txt`](./prompts/scenariogen/generate_scenarios.txt)（v3 加入了 "dual mandate: NL element coverage + bug-finding probes" 段）
- **schema**：[`schema.py`](./schema.py)（v2 multi-step `ScenarioStep` + `StepResult`，保留）
- **sim 实现**：[`feedback/sim.py`](./feedback/sim.py)（v2 多步执行，保留）
