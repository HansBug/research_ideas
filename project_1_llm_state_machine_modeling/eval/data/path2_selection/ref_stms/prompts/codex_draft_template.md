# REF STM 生成任务（case {{CASE_ID}}）

为 case `{{CASE_ID}}` (`{{CASE_NAME}}`, bucket={{BUCKET}}, domain={{DOMAIN}}) 生成一份**高质量** reference pyfcstm STM，作为 PATH2 实验的人工签字 ref（最终 paper 口径"expert-authored"）。这份 ref 必须：

1. 通过 pyfcstm 三关 (parse / sem / sim smoke)
2. **必须自带一组 scenarios，覆盖 NL 里描述的全部关键特性**（每条 mode 切换 / guard / 数值阈值 / fault 路径 / per-cycle 行为都要至少有 1 个 scenario 覆盖到，且 scenario 必须实际 pass）
3. 与原文 NL 语义一致
4. 在原文支持的 C-axis 上恰当使用 pyfcstm grounding feature

**关键设计**：scenario 不只是 smoke。每个 scenario 必须**显式断言 expected_state + expected_vars**，逐步走过 NL 描述的真实场景。scenario fail 时，codex 必须判断是 model 写错还是 scenario 写错（误解 NL），相应修复。

## 必读上下文（请逐项 Read，不要跳）

1. **STM.md case section**：`{{STM_PATH}}`
   - 找 `## 条目 N: {{CASE_NAME}}` 段（grep 定位 N，可能不是 1）
   - 重点读该 case 的 §0 识别判定 / §1 原文摘录 / §2 NL 描述 / §3 逐句溯源
2. **expansion NL（含 [E] 溯源 markers + provenance 数组）**：`{{EXPANSION_PATH}}`
   - 这是 reference 必须忠实于的英文 NL — 含 inline `[E1] [E2]` 标记 + provenance 字段
3. **paper PDF**（必要时核对）：`{{PAPER_PDF}}`
4. **paper_content.txt**（grep 关键词友好）：`{{PAPER_CONTENT}}`
5. **pyfcstm grammar reference**：`{{GRAMMAR_REF_PATH}}` — pyfcstm DSL 完整语法
6. **pyfcstm DSL examples（强烈推荐都读一遍）**：
   - `pyfcstm/editors/jsfcstm/test/fixtures/visual/01-simple-leaf.fcstm`（最简单 flat FSM 模板）
   - `pyfcstm/editors/jsfcstm/test/fixtures/visual/02-nested-hvac.fcstm`（层次状态 + sub-state）
   - `pyfcstm/editors/jsfcstm/test/fixtures/visual/06-guard-effect.fcstm`（变量 + 复合数值 guard + effect）
   - `pyfcstm/editors/jsfcstm/test/fixtures/visual/05-forced-expansion.fcstm`（`! forced transition`）
   - `pyfcstm/editors/jsfcstm/test/fixtures/visual/04-many-transitions.fcstm`（多 transition）

## 必须满足的硬约束

1. **忠于原文**：所有 mode / event / variable / threshold 名必须能在 STM §1 原文摘录或 expansion NL provenance 找到对应；**禁止无中生有**
2. **🚫 零 warning 零 error**（与 IDE 等价的 lint gate）：
   - **禁止 write_only_variable**（dead assignment）：一个 var 在 enter/during/exit/effect 中被赋值但没有任何地方读它（不在任何 guard 表达式 / 其他 effect RHS 中出现）→ **不要声明它**。如果是"我用变量记录我进了哪个 state"这种装饰性 indicator，**直接用 mode 名 + abstract action 代替**，不要靠 var 存指示位
   - **禁止 unused_variable**：声明了但全文一次都不读不写 → 删
   - **禁止 unused_event**：state 上声明了 event 但没有任何 transition 用它 → 删
   - **禁止 dead_transition**：source 状态不可达 / guard 写成 false 字面量 → 删
   - **禁止 unreachable_state**：从 `[*] -> X` 初始链出发 BFS 走不到的 state → 删
   - **判定方式**：`verify_pyfcstm_full.py` 内嵌 Stage 5 lint，**lint 必须输出 `warnings=0` 才算 ALL_OK**
3. **变量的设计原则**：每个 `def TYPE x = ...;` 都必须有**实质用途**之一：
   - (a) 在某条 transition 的 guard 中被读取（决定迁移）
   - (b) 在另一个 effect 中被读取作为右值（用于运算）
   - 单纯写值不读 → **不要声明**。原文里的"状态指示"用 mode 名 + abstract action 表达，不要靠 indicator var
4. **C-axis grounding 恰当使用**（不强行堆砌）：
   - **C1 (周期执行)**：原文若有"each cycle / per tick / continuously / 持续 / 周期"语义 → 用 `during {...}` action 或 `>> during after` aspect。**注意**：`during` 里的 effect 也必须有读者，不能是 write-only！
   - **C2 (数值守卫)**：原文若有 ≥2 个变量 + 复合算术比较 → 用 Expr IR 多变量算术 guard。变量必须真的参与判定
   - **C3 (forced fault)**：原文若有全局 fault 语义 → 用 `! * -> Error :: Event`
   - **C4 (硬件 effector)**：原文若有具名 sensor / actuator → 用 `enter abstract` / `during abstract` / `exit abstract` 占位（这是 grounding 硬件，**不是用 var 来 mock 硬件状态**）
   - **原文不支持的 C-axis 不要硬塞**
5. **规模匹配**：states 6-15；变量数应该**很少**（典型 0-5 个），仅当真有 numerical/computed 状态时才用 var；事件只声明实际被 transition 用到的
6. **必须通过 pyfcstm 完整验证**：parse → sem → sim → scenarios all-pass → lint 0-warning，全过才 ALL_OK

## 验证工具（**强制使用 Bash tool 反复调用**）

### Stage 1: smoke 验证（parse + sem + sim 一次 cycle 不死锁 + 0 warning）

每次写完 DSL，先跑 smoke：

```bash
cd /home/zhangshaoang/oo-projects/research_ideas-2
source venv/bin/activate
python3 project_1_llm_state_machine_modeling/eval/data/path2_selection/ref_stms/verify_pyfcstm_full.py {{OUTPUT_FCSTM}}
```

期望最后两行：`LINT_SUMMARY: warnings=0 by_code={}` + `ALL_OK`

任一阶段失败 → 读错误 → 修复 → 再跑（max 5 iter）。**lint 失败的常见原因**：
- `write_only_variable`：声明的 var 写了但没读 → 删掉该 var，把"状态指示"挪到 mode 名 / abstract action
- `unused_event`：声明的 event 没用 → 删
- `unused_variable`：完全没用 → 删
- `unreachable_state` / `dead_transition`：去掉孤立 state / 重写 init transition 让它可达

### Stage 2: 必须生成 scenarios.json + 跑 NL 全特性覆盖验证

写完 smoke-OK 的 DSL 后，**必须**生成 `{{OUTPUT_SCENARIOS}}` 文件，**列出覆盖 NL 全部关键特性的 scenarios**，然后跑：

```bash
python3 project_1_llm_state_machine_modeling/eval/data/path2_selection/ref_stms/verify_pyfcstm_full.py {{OUTPUT_FCSTM}} {{OUTPUT_SCENARIOS}}
```

期望最后一行：`ALL_OK`

**scenarios.json schema**（必须严格遵守）：

```json
{
  "scenarios": [
    {
      "name": "<short identifier, snake_case>",
      "description": "<1 句中文，说明该 scenario 测的是 NL 里哪个特性 + 对应 NL 段落>",
      "initial_state": null,
      "initial_vars": {},
      "steps": [
        {
          "before_cycles": 0,
          "events": ["SomeEvent"],
          "expected_state": "Path.To.State",
          "expected_vars": {"var_name": 5},
          "name": "<short step label>"
        }
      ]
    }
  ]
}
```

字段说明（必读）：

- **`initial_state`**：`null` 表示从默认 `[*] -> X` 初始进入；否则是 hot-start 状态（用全路径 `Path.To.State`）
- **`initial_vars`**：hot-start 变量预设；为空时用默认初值
- **`steps[].before_cycles`**：在本 step 执行 event 之前先跑 N 个空 cycle（让计时 / 累加器自然推进）
- **`steps[].events`**：
  - `null` → 跳过本 step 的 cycle（不调 cycle()）
  - `[]` → 跑一次空 cycle (`runtime.cycle()` 无 event)
  - `["E1", "E2"]` → 跑一次 cycle 同时注入多个 event (`runtime.cycle(events=["E1","E2"])`)
- **`steps[].expected_state`**：完整路径如 `Plant.Running.Phase1`；不检查就 `null`
- **`steps[].expected_vars`**：检查的变量列表（未列的变量不检查）；不检查就 `null`

**event 路径写法**（重要）：event 是定义在 state 上的，运行时 `cycle(events=["X"])` 中 X 可以是简名或完整路径。若简名重名，用完整路径 `Mode.SubMode.X`。从 STM.md §1 摘录确认 event 是定义在哪个 state 上的。

### scenarios 必须覆盖（最低要求）

1. **每个关键 mode** 至少 1 个 scenario 验证进入条件
2. **每个数值 guard** 至少 1 个 scenario 验证 guard 阈值边界（before / after threshold 各 1 个 step 更好）
3. **每个 fault path**（若 NL 有）至少 1 个 scenario 验证 fault event 触发 + 切到 ErrorHandler
4. **每个 per-cycle 行为**（若 NL 有）至少 1 个 scenario 跑 ≥3 个 cycle 验证变量持续更新
5. **每个具名 effector**（若用 abstract action）至少 1 个 scenario 触达 entry / exit 调用

最少 **≥3 个 scenarios**，典型 5-10 个，规模适配 case 复杂度。

### 迭代

scenarios 跑下来 fail → **诊断**是 model 错还是 scenario 错：

- model 漏 transition / guard 错 / event 路径错 → 修复 DSL
- scenario 误解 NL（如把"5 帧检测到 3 次"写成 `before_cycles: 5` 但应该是 `before_cycles: 4`）→ 修 scenario
- 两者都对但 scenario 设的 expected 错 → 修 expected

**Max 5 iter combined**（smoke + scenarios 总共 5 轮）。最后所有 scenarios 必须 pass。

## 输出（必须写到下列文件）

1. **`{{OUTPUT_FCSTM}}`**：最终 pyfcstm DSL（必须三关全过；若 5 iter 仍卡，输出当前最佳尝试）
2. **`{{OUTPUT_SCENARIOS}}`**：NL 全特性覆盖的 scenarios.json（必须所有 scenarios pass）
3. **`{{OUTPUT_NOTES}}`**：markdown notes，结构如下：

```markdown
# Codex Draft Notes — Case {{CASE_ID}}

## 1. 设计选择

- mode 列表：[逐个列出，标注每个 mode 名来自 STM §1 摘录 X 或 expansion [En]]
- event 列表：[同上]
- variable 列表：[同上，含类型 + 初值，标注 threshold 来源]
- transition 设计：[关键 transition 列举，标注 guard / effect 的原文出处]

## 2. C-axis grounding 使用情况

- **C1 (周期执行)**: 用 / 未用 — 在哪个 state 使用 `during {}` / `>> during` aspect，原因
- **C2 (数值守卫)**: 用 / 未用 — 哪条 transition 用复合数值 guard，变量+阈值都来自原文哪里
- **C3 (forced fault)**: 用 / 未用 — 是否用 `! * -> Error`，原文支持/不支持的依据
- **C4 (硬件)**: 用 / 未用 — 哪些 abstract action 对应原文哪个 effector

## 3. 与 NL 的对应关系

- expansion NL [E1]: "..." → 对应 DSL `state X` 或 `Y -> Z :: Event`
- expansion NL [E2]: ...
- ...

## 4. 迭代历史

- iter 1: 写出初稿 → verify: PARSE_FAIL line 12 (Unexpected token `do`) → 修复（改为 `during`）
- iter 2: PARSE_OK → SEM_FAIL (undefined var `tmax`) → 修复（添加 `def float tmax = 80.0;`）
- iter 3: PARSE_OK → SEM_OK → SIM_OK → ALL_OK

## 5. 与 STM.md 表述的偏差（如有）

[如果你为了让 DSL 合法或更清晰而对 NL 做了任何重述，在这里坦诚说明]
```

## Codex agent_message 输出（最终 JSON，无 markdown fence）

```json
{
  "case_id": "{{CASE_ID}}",
  "iterations": <int>,
  "final_validation": {
    "parse": "OK" | "FAIL",
    "sem": "OK" | "FAIL",
    "sim": "OK" | "FAIL",
    "scenarios_total": <int>,
    "scenarios_pass": <int>,
    "scenarios_fail": <int>,
    "scenarios_error": <int>,
    "states_count": <int>
  },
  "scenario_coverage_summary": {
    "modes_covered": <int>,
    "guards_covered": <int>,
    "fault_paths_covered": <int>,
    "per_cycle_behaviors_covered": <int>,
    "effectors_covered": <int>
  },
  "c_axis_used": {
    "C1": true | false,
    "C2": true | false,
    "C3": true | false,
    "C4": true | false
  },
  "design_summary": "1-2 句中文",
  "files_written": ["{{OUTPUT_FCSTM}}", "{{OUTPUT_SCENARIOS}}", "{{OUTPUT_NOTES}}"]
}
```

输出**仅** JSON，无前后缀文字，无 ```code fence```。

## 评审纪律

1. **JSON only**：最终 agent_message 仅一个 JSON object
2. **绝不发明事实**：所有 mode / event / var 名拿不准就别用 — 退而求其次用通用名（`State1`, `State2`），但要在 notes 里坦诚
3. **不堆砌 C-axis**：原文没有的就 false，不要为了 "看起来 4 个 axis 都用上" 硬加
4. **三关必须过**：实在过不了，输出最佳尝试 + 详细诊断 — 后续 claude 评审 + 用户 audit 阶段会处理
