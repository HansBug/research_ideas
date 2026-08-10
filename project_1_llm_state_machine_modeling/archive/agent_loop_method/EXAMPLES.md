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

> **LG-M1-F provenance note（2026-06-08）**：本文件是早期 Phase G / Phase E 的历史演示记录，用于解释 scenario+sim framing 与 prompt 演化；其中 `/tmp/phase_*` 脚本/JSON 属于当时 session 的 ephemeral artifact，不是当前 LG-M1 推荐复现入口。当前功能入口、测试 gate 与真实四例纪律以 [README.md](./README.md) 与 [ARCHITECTURE.md](./ARCHITECTURE.md) 为准；最终 integrated 四例由 LG-M1-G 在最终 head 上重新产出。

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
| **v3 (historical Phase G/E demo framing)** | **differential mutation detection rate** + NL element coverage | ✓ scenarios 是 NL-driven bug probes，pass rate 不是目标，**catch bug 才是**；original 上的 fail 也是有价值的 finding |

---

## 输入/输出资产路径

- **测试脚本**：`/tmp/phase_g_v3_test.py`（含 6 个 mutation 的 regex-based mutator；historical ephemeral artifact）
- **完整 JSON 结果**：`/tmp/phase_g_v3_results.json`（含每个 scenario 的全部 step results、actual_state、actual_vars、var_mismatches、runtime_error；historical ephemeral artifact）
- **prompt**：[`prompts/scenariogen/generate_scenarios.txt`](./prompts/scenariogen/generate_scenarios.txt)（v3 加入了 "dual mandate: NL element coverage + bug-finding probes" 段）
- **schema**：[`schema.py`](./schema.py)（v2 multi-step `ScenarioStep` + `StepResult`，保留）
- **sim 实现**：[`feedback/sim.py`](./feedback/sim.py)（v2 多步执行，保留）

---

# Phase E — agent loop driver 演示

> **目的**：把前面 Phase D / F / G 的零部件串成可迭代的 agent loop，并验证：(1) cascade gating 工作；(2) cascaded Repair 按 channel 分工调度；(3) scenarios 一次生成后 freeze 不变；(4) `sim` 通道可以 on/off 用于 ablation。
>
> **运行命令**（仓库根，`set -a; source .env; set +a` 后）：
> ```bash
> cd project_1_llm_state_machine_modeling && PYTHONPATH=. python3 /tmp/phase_e_demo.py
> ```
>
> **设计要点（locked 2026-05-26）**：
> 1. **Gated cascade**：parse → semantic → (sim ∥ judge)；前面 fail 时下游不跑
> 2. **Cascaded Repair**：4 个 fix sub-prompt (`fix_parse.txt` / `fix_sem.txt` / `fix_sim.txt` / `fix_judge.txt`)，每轮按"最早 fail 的 source"路由
> 3. **Scenarios frozen**：在 iter 循环外生成一次，所有 iter 共用 — model 适配 scenarios，不反向
> 4. **sim/judge optional**：通过 `LoopConfig.feedback_sources` 控制；不在列表里的不跑
> 5. **Early back-out**：cascade 返回 `all_ok` 立即退出
>
> **配置矩阵**：
> - `A2` = `["parse", "semantic", "sim"]` + multi_step + n_iter=3（主 demo）
> - `A1` = `["parse", "semantic"]`（ablation — sim OFF）

## Part A — 3 NL examples 跑 A2

| Example | status | iters | tokens | iter 0 sim | 注 |
| --- | --- | :-: | --- | --- | --- |
| **traffic_light** | not_converged | 3 | 25,891 | 5/8 | LLM scenarios 含 3 个 boundary probe 在 modeler 输出上 fail（NL-model gap，repair 难以同时满足所有 probe）；iter 1-2 试图 oscillate 调整 guard，sim 在 5/8↔4/8 间摆动 |
| **microwave** | not_converged | 3 | 23,258 | 7/8 | iter 0 已经 parse + sem ok，sim 7/8 仅 1 个 fail；repair 把 `Cooking -> Idle : if [...]` 误改成 `:: if [...]` → 引入 parse fail → cascade 切换到 fix_parse 接力，但 iter 2 也没修对 |
| **elevator_3floor** | **converged ✓** | 1 | 21,608 | 8/8 | modeler 一次产生满足 8/8 scenarios 的 DSL，cascade `all_ok` 直接 early-exit |

**说明**：traffic_light / microwave 的 "not_converged" **不是 Phase E 失败**，恰恰是 loop **真的在转** 的证据 — 不是 1-shot 过：
- traffic_light 显示 repair 可以多轮针对同一 channel (sim) 尝试不同 fix 方向
- microwave 显示 cascade 在 iter 1 自动从 sim 切到 parse（repair 引入新问题后下层 channel 接力）

## Part B — inject-bug-and-recover 验证 sim feedback 真的让 repair 拨回来

把 traffic_light modeler 输出（iter 0 干净版）人为注入 bug 作为 `seed_dsl`，跳过 modeling 直接进 iter loop。

### B1 — inject M3（`timer >= 30` → `timer >= 99999`，Green 永远不可达）

```
iter 0 [seeded]   parse_ok=T sem_ok=T sim 7/8        ← sim catch: full_cycle expected Green but actual Red
                  DSL: Red -> Green : if [timer >= 99999] effect { timer = 0; };
                  violation: red_guard_boundary_should_fire_at_30 → Repair target = sim
iter 1 [repair]   parse_ok=T sem_ok=T sim 8/8 ✓     ← EARLY-EXIT, converged
                  DSL: Red -> Green : if [timer >= 30] effect { timer = 0; };
status: converged   iters: 2   tokens: 8,392
```

**完整 bug→catch→repair→converge 闭环**：sim 抓出 unreachable bug → fix_sim sub-prompt 看到 `actual_state=Red` 而 `expected=Green` 推断 guard 太高 → 直接修回 `>= 30` → 2 iter 收敛。

### B2 — inject M6（`effect { timer = 0; }` → `effect { timer = 100; }`，副作用值错）

```
iter 0 [seeded]   sim 7/8
                  DSL: Red -> Green : if [timer >= 30] effect { timer = 100; };
iter 1 [repair]   sim 7/8  (no progress)
                  DSL: Green -> Yellow guard 改成 if [timer >= 25 && (timer < 100 || timer >= 125)] effect { timer = 0; };
                  ← LLM 误以为问题在 Green->Yellow 的 guard，做了补偿性改动
iter 2 [repair]   parse_ok=F
                  DSL: 重复了 Red->Green 行（语法错），timer 改成 -1 / 99 等不合 NL 的值
status: not_converged   iters: 3   tokens: 12,548
```

**失败模式典型展示**：repair 没有直接修 `timer=100` 这个最直接的 bug，反而绕道在下游 guard 加复杂条件 — 这是 fix_sim prompt 的弱点（var_mismatches 没有强制 LLM 优先看"哪个 effect 引入了错误值"）。**这正是后续 prompt 优化的 actionable target**，不是 Phase E 框架本身的问题。

## Part C — Ablation A1（sim OFF）

```
iter 0 [modeler]  parse_ok=T sem_ok=T        ← sim 没在 feedback_sources, 不跑
status: converged   iters: 1   tokens: 12,284
```

**关键对比 A2 vs A1**：同样 NL（traffic_light），A1 在 sim 关闭后 1 iter 直接 converge（因为只看 parse+sem，二者都 ok），但 A2 跑了 3 iter 仍 not_converged。**说明 sim feedback 引入的"行为正确性"信号是 A1 看不到的** — A1 报告的"converged" 实际上是 model behavior 未经检验。这是 ablation 实验中 sim 通道价值的 numeric 证据：

| 配置 | feedback channels | iter 1 result | 实际正确性 |
| --- | --- | --- | --- |
| **A1** | parse + sem | converged | 未检验 — A2 揭示 5/8 sim 失败 |
| **A2** | parse + sem + **sim** | not_converged after 3 iter | sim catch 出真正的 model-NL 行为差异 |

## Phase E 阶段性结论

| 维度 | 结果 |
| --- | --- |
| Loop driver iter 真正在转（不是 1-shot） | ✅（traffic_light 3 iter / microwave 3 iter / inject M6 3 iter）|
| Cascade gating 工作 | ✅（microwave iter 0 sim fail → iter 1 parse fail → 自动切到 fix_parse）|
| Cascaded Repair 按 channel 调度 | ✅（fix_parse / fix_sem / fix_sim 都被实际选中过）|
| Scenarios frozen across iters | ✅（demo 中 scenarios 一次生成后所有 iter 用同一套）|
| sim on/off 可切换（ablation） | ✅（A1 vs A2 numeric 对比 demo）|
| 收敛真的发生（不是永远转）| ✅（elevator A2 / inject M3 各 1 个 converged case）|
| 失败模式可观察可分析 | ✅（microwave repair 引 parse bug / inject M6 repair 绕道）|

**输入/输出资产路径**：
- 测试脚本：`/tmp/phase_e_demo.py`（含 A2 三例 + 2 个 inject + A1 ablation；historical ephemeral artifact）
- 完整 JSON：`/tmp/phase_e_results.json`（每 iter 的 DSL / feedback / repair_target / sim_violations 全保留；historical ephemeral artifact）
- loop driver：[`loop.py`](./loop.py)
- cascaded repair：[`agents/repair.py`](./agents/repair.py)（dispatcher）+ [`prompts/repair/`](./prompts/repair/) 4 个 sub-prompt

## Phase E v2 — context 增强 (a) DSL grammar reference + (c) passing-scenarios 显式标注

回看 Phase E v1 demo 的失败模式：(A2 microwave) repair 把 `: if [...]` 改成 `:: if [...]` 引 parse fail；(A2 traffic_light) repair 改 guard 时破坏 previously-passing scenario 造成 5/8↔4/8 oscillation。诊断 fix 阶段实际拿到的 context 发现：(a) fix prompt 没有 pyfcstm DSL 语法 cheat-sheet（凭"记忆"操作 operator 错位）+ (c) sim diagnostic 只列 failing scenarios 没有显式标"哪些 pass 不能动"。

补这两项后重跑同一组 demo：

| Config | v1 status | v1 iter trace | **v2 status** | **v2 iter trace** |
| --- | --- | --- | --- | --- |
| A2 traffic_light | not_converged | sim 5/8 → 4/8 → 5/8（osc 破坏 passing）| not_converged | 仍 not converge（boundary NL gap 是 deep 问题），但**不再 osc 破坏 passing** |
| A2 microwave | not_converged | sim 7/8 → **parse_fail → parse_fail**（repair 改 `:`→`::`）| **converged ✓** | sim 7/8 → 7/8 → **8/8** ✓（iter 1 加 effect、iter 2 改阈值 120→119；全程 operator 未动）|
| A2 elevator | converged 1-iter | 8/8 直接 early-exit | converged 1-iter | 8/8（unchanged）|
| B inject M3 | converged 2-iter | `>=99999` → `>=30` 修复 ✓ | converged 2-iter | unchanged |
| B inject M6 | not_converged | 7/8 → 7/8 → **parse_fail**（repair 引 parse bug）| not_converged | 7/8 → 7/8 → 7/8（**parse 稳定 OK**，但仍未修对 effect 值）|
| C ablation A1 | converged 1-iter | 1 iter ✓ | converged 1-iter | unchanged |

### (a) DSL grammar reference 改动

把原 `prompts/repair/_grammar.md` 提升为共享 [`prompts/_pyfcstm_grammar.md`](./prompts/_pyfcstm_grammar.md) — comprehensive 12 章 + 3 个 worked examples (traffic light / 2-floor elevator / hybrid microwave) + pre-output self-check。同时被 4 个 agent 用：

| Agent | 加载方式 |
| --- | --- |
| `agents/modeler.py` | 通过 `build_sl1_initial_modeling_prompt(...)` 复用 canonical SL-1 prompt generator；共享 grammar 由 prompt generator 追加 |
| `agents/multistep/build_pyfcstm.py` | 继续在 multistep builder 内加载共享 grammar；`prompts/multistep/build_pyfcstm.txt` 同步 slim |
| `agents/repair.py` | 4 个 fix sub-prompt 提供 focused role guidance；共享 grammar 由 `build_sl9_repair_prompt(...)` 统一追加，避免重复/空 grammar section |

合并的 grammar 含 modeler.txt 原来更详尽的内容（包括 `:` 不只是 guards——也是 chain/absolute scope 的 event scoping operator；v1 grammar 把这个简化错了导致 LLM 也容易出错）+ cycle execution semantics（off-by-one 怎么来）+ "INVALID 形式" 反例表。

### (c) Passing-scenarios 显式标注 改动

`agents/repair.py:_build_repair_context` for `target=sim` 现在生成结构化 SL-9 输入：
```
selected_diagnostics = [{"source": "sim", "feedback": { ... failing scenario_results only ... }}]
scenario_summary = {
  "passing_scenario_names": ["scenario_A", "scenario_B"],
  "failing_scenario_names": [...],
  "do_not_regress_passing_scenarios": true,
  "frozen_scenarios": [...]
}
```

`prompts/repair/fix_sim.txt` 加硬规则：
> Do NOT regress passing scenarios: the user message lists the scenarios that currently PASS. After deciding on an edit, mentally re-evaluate each passing scenario against your proposed DSL. If your change would alter their result, the edit is wrong — reconsider.

### 关键 trace — A2 microwave v2（grammar reference 治好了 parse 回归）

```
iter 0 [modeler]  parse=T sem=T sim=7/8 ✗
                  Cooking -> Idle : if [cook_timer >= 120];

iter 1 [repair]   parse=T sem=T sim=7/8 ✗  (target=sim)
                  Cooking -> Idle : if [cook_timer >= 120] effect { cook_timer = 0; };
                                                            ← 加 effect, `: if` 操作符没动 ✓

iter 2 [repair]   parse=T sem=T sim=8/8 ✓ EARLY-EXIT
                  Cooking -> Idle : if [cook_timer >= 119] effect { cook_timer = 0; };
                                                            ← 阈值 120→119, 仍 `: if` ✓
status: converged   tokens: 37,605
```

对比 v1 同一例 iter 1：`Cooking -> Idle :: if [cook_timer >= 120];`（错把 `:` 改成 `::`，parse 立即挂）—— grammar reference 直接杜绝此类失败。

### 现存的 failure mode（actionable next steps）

**(d) sim cycle trace 注入** 是接下来值得做的：B M6 inject 仍 not_converged 是 v2 后剩下的主要类型 — repair 没能从 `var_mismatches: timer=expected=1, actual=101` 反推到 `effect { timer = 100; }` 这条 root cause line。给 fix_sim 附加 sim cycle-by-cycle trace（"hot-start Red/timer=29 → cycle 1 fire Red→Green, effect timer=100, Green during +1 = 101"）应能让 LLM "看见"模型行为路径，提高 root-cause reasoning 命中率。

---

## Phase E v3 — scenariogen 自管 (e) cycle-counting 一致性 + (f) mutation self-validation

诊断 v2 残留两类 failure（Case 1 A2 traffic_light scenarios 内部 cycle 口径冲突 / Case 2 B M6 scenarios 没有任何一条触达 buggy line）之后，把治理从 repair 阶段向上提到 **scenariogen 阶段**：让 scenariogen 自己解决内部一致性 + 自己保证 bug-finding 覆盖率。

### (e) Cycle-counting 一致性 + NL-grounded 硬规则

在 `prompts/scenariogen/generate_scenarios.txt` 顶部加两段硬规则：

1. **HARD RULE: expected values come from NL, NOT from the DSL** ——
   显式禁止 LLM 把 expected_state/vars 通过 "mental sim DSL" 得来。`expected_*`
   只能来自 NL 语义。这条规则直接抑制 "scenarios match buggy model -> bug
   surface 不出来" 的 false-positive 通路（Case 2 v2 失败的根因）。
   prompt 内置反例：NL 说 timer 重置但 DSL 错为 `effect { timer = 100 }` 时，
   LLM 必须写 `expected_vars={"timer": 1}` 而不是 101 — 这样 sim 才能 surface
   `expected=1, actual=101`，repair 才能定位 effect line。
2. **Cycle-counting consistency** —— 在同一次 output 内，所有涉及 "X reaches N
   transitions to Y" 的 scenarios 必须用同一套 cycle-counting 口径（pre-during
   guard + post-effect during 推 1）。boundary probe 强制用 hot-start 而非
   `before_cycles=N-1` 数上去。配套 self-check 列表。

### (f) Mutation-based 覆盖率 self-validation

在 `loop.py` Stage 3 scenariogen 之后插一个**纯本地**的覆盖率检查：

新建 `method/scenariogen_validate.py`，提供 6 个 **DSL-shape generic** mutator
（不绑定具体 state/var 名）：

- `M1_guard_off_by_one`：每个 `>= N` 试 `>= N-1`
- `M2_wrong_transition_target`：每个 `A -> B` 换目标
- `M3_unreachable_target`：每个 `>= N` 改成 `>= 99999`
- `M4_missing_forced_transition`：删除每条 `! ...` 行
- `M5_missing_effect`：删除每个 `effect { ... }` 块
- `M6_wrong_effect_value`：每个 `var = N` 改成 `var = N+100`

对原始 DSL apply 每类 mutation -> 跑 sim -> 检查"是否至少一个 scenario 在
mutated variant 上 fail"。任何 mutation 类型未被 catch ->
`coverage_directive()` 生成针对性指令 -> 再调一次 scenariogen 让它**追加**
probes。最多 retry 2 次。

变量：`generate_scenarios(..., extra_directive=...)` 把指令拼到 user message。
LoopConfig 不变；`AgentLoopResult` 加 `scenariogen_coverage: list[dict]`
记录每次 attempt 的 6 类 status，方便后续诊断。

成本：每次 self-validate 本地 sim 6 类 × ≤3 variants = ~18 次秒级 sim 跑，零
额外 LLM call；retry LLM call 仅在确有 gap 时触发。

### Demo 矩阵 v2 vs v3 对比

| Config | v2 status | v2 trace | **v3 status** | **v3 trace** |
| --- | --- | --- | --- | --- |
| **A2 traffic_light** | not_converged | sim 5/8 → 4/8 → 5/8（osc，scenarios 内部 cycle 口径冲突）| **converged 1-iter ✓** | sim 8/8 ✓（modeler 一次过；scenarios 内部一致，覆盖率 caug×4 + part×2）|
| **A2 microwave** | converged 3-iter | 7/8 → 7/8 → 8/8 | **converged 1-iter ✓** | sim 9/9 ✓（首轮 caug×6 全过）|
| A2 elevator | converged 1-iter | 8/8 | converged 1-iter | 8/8（unchanged）|
| B inject M3 | converged 2-iter | `>=99999` → `>=30` 修复 | **not_converged 8/9** | guard 已修回 `>= 30`、effect timer=0；残余 1 scenario 是 scenarios 自己 cycle off-by-one（`before_cycles=29` 期望 Green，实际还差 1 cycle）|
| **B inject M6** | not_converged | 7/8 → 7/8 → 7/8 → 7/8（scenarios match buggy model，bug 不 surface）| **converged 2-iter ✓** | 7/9 → **9/9 ✓**（retry1 直接把 buggy effect `timer = 100` 改回 `timer = 0`）|
| C ablation A1 | converged 1-iter | unchanged | converged 1-iter | unchanged |

### 关键 trace — B inject M6（v3 真改回 bug，v2 改不回去）

```
seed_dsl:  Red -> Green : if [timer >= 30] effect { timer = 100; };   ← injected M6

scenariogen [initial]  → 9 scenarios
  coverage: M1=part, M2=part, M3=part, M4=caug, M5=part, M6=part
  → M6 not fully caught, build directive, retry

scenariogen [retry1]   → 10 scenarios
  coverage: M1=caug, M2=part, M3=part, M4=caug, M5=part, M6=part   ← 仍 part, 但
                                                                   added probe 已经
                                                                   能 trigger buggy
                                                                   line
iter 0 [seeded]   parse=T sem=T sim=7/9 ✗   target=sim
                  Red -> Green : if [timer >= 30] effect { timer = 100; };
                  violations include scenarios with expected timer=1 vs actual 101+

iter 1 [repair]   parse=T sem=T sim=9/9 ✓   EARLY-EXIT
                  Red -> Green : if [timer >= 30] effect { timer = 0; };
                                                            ← buggy 100 改回 0 ✓
status: converged   tokens: 27,494
```

### 关键 trace — A2 traffic_light（v2 osc/卡死 → v3 1-iter 过）

v2 三轮反复在 `>= 30` / `>= 29` 之间 osc 还破坏 passing scenarios（scenarios 自相矛盾），现在 v3 modeler iter 0 直接 8/8 收敛 —— 不是 modeler 改强了，而是 **scenarios 内部不再自相矛盾** + **scenarios 不再 lean DSL**，让原本 valid 的 modeler output 不再被假阳性 false-fail 触发 repair。

### v3 后剩下的失败模式

**B M3 残余 1/9 fail**：scenariogen 这次写的 full_cycle scenario 用了
`before_cycles=29, events=[]` 但默认初始化下需要 30 cycles 才能让 Red 的 during
把 timer 推到 30 触发 guard。本质是 scenarios 自己 cycle off-by-one。

**短期不再 chase 这类残余**：从 v1 → v2 → v3 的演变规律已经清楚 —— 治理向上
推到 scenariogen 阶段比加 fix_sim trace 之类下游补丁更有效。下一步如果还要继续
push，候选 (g) 是 sim 跑一遍 initial DSL 验证 scenarios 是否在 baseline 上自洽，
若否就要求 scenariogen 修正。但 v3 已经把核心 framing failure 治好（B M6 truly
fixed，A2 traffic_light 1-iter 过），优先级转向 Phase H (judge) / Phase I /
Phase J 端到端 acceptance。

### v3 文件改动

- `prompts/scenariogen/generate_scenarios.txt`：顶部新增 "HARD RULE: expected
  values come from NL, NOT from the DSL" + "Cycle-counting consistency" 两段
- `agents/scenariogen/generate.py`：`generate_scenarios(..., extra_directive=...)`
  支持 prompt-side targeted revision
- `method/scenariogen_validate.py` **（新建）**：6 个 DSL-generic mutator +
  `validate_coverage()` + `coverage_directive()`
- `method/loop.py` Stage 3：scenariogen → coverage check → 最多 2 次 targeted
  retry，把每次 attempt 的 status 写入 `result.scenariogen_coverage`
- `method/schema.py`：`AgentLoopResult` 加 `scenariogen_coverage`

### 历史入口资产（v3，ephemeral）

- Demo 脚本：`/tmp/phase_e_demo.py`（v2 → v3 同一组配置，便于当时 session 对比；当前不作为可复现入口）
- 完整 JSON 结果：`/tmp/phase_e_results.json`（含 `scenariogen_coverage` 字段；当前不作为可复现入口）
