# PATH1 REF STM 生成任务（case {{CASE_ID}}）

为 case `{{CASE_ID}}` (`{{CASE_NAME}}`, stm_type={{BUCKET}}, domain={{DOMAIN}}) 生成一份**高质量** reference pyfcstm STM，作为 PATH1 sprint **5-component manual eval** 的 ground truth（最终 paper 口径"expert-authored" 由用户 Stage E 签字承担）。

这份 ref 必须：

1. 通过 pyfcstm **四关**：parse / sem / sim_smoke / **static analysis**（无 ERROR）
2. **与扩充版 NL 在 5-component 层面完全对应**（states / transitions / guards / actions / hierarchical_states 五个集合，每个元素都能溯源到 NL 某句 + paper 摘录）
3. 不发明 NL 没有的 state / transition / guard / action / 数值阈值
4. 在原文支持的 pyfcstm primitive 上恰当使用（forced reset、aspect during、abstract action 等仅在 NL 真有该语义时使用）

> **重要**：本任务不需要 scenarios.json，也不需要"运行时全特性覆盖"验证 — PATH1 评测口径是 5-component component-level P/R/F1，不是 sim intrinsic。请把精力放在让 5-component IR 与 NL 一一对应上。

## 🚨 anti-patterns — 必须避免的常见错误（CARA 实测踩过）

以下 5 类是 codex 起草 reference STM 时最常犯的错，会被 `verify_pyfcstm_static.py` 直接判 ERROR / WARN，导致 STATIC_FAIL：

### ❌ A1 — 把 NL fact 编码成 boolean flag 变量

**错误**：看到 NL 写 "sensor readings are stored in a shared buffer" 就 `def int sensor_readings_stored_in_shared_buffer = 0;` + `enter { sensor_readings_stored_in_shared_buffer = 1; }`，但这个 var 没有任何 guard 读它。

**结果**：static analyzer 报 `WARN write_only_var`。如果 case 里有 ≥3 个这样的 var，触发 `high_var_to_state_ratio` WARN。

**正确做法**：用 `enter abstract StoreSensorReadingsInSharedBuffer;` 即可 —— "做了某动作" 应该是 abstract action（外部 handler 注入），**不是** boolean 状态。State variable 只用于 **真的需要被 guard 读取的值**（counter、threshold、mode-tag、external-input value）。

### ❌ A2 — 把 NL event 同时编码成 event + flag（双重编码）

**错误**：NL 写 "caregiver initiates algorithmic pump control"，codex 同时写 `event InitiateAlgorithmicPumpControl;` 和 `def int algorithmic_pump_control_initiated = 0;`，然后在 transition 上 `:: InitiateAlgorithmicPumpControl effect { algorithmic_pump_control_initiated = 1; }`。

**结果**：flag write-only，redundant；static analyzer 报 `WARN write_only_var`。

**正确做法**：**只用 event**（`:: InitiateAlgorithmicPumpControl`），不加 flag。Event-driven transition 已经完整表达"caregiver 触发"语义。flag 仅用于：**该事件触发后某个 LATER guard 需要读它来决定后续行为**。

### ❌ A3 — 把"外部输入"编码成 guard var，但没人写它

**错误**：NL 写 "if pump complication, go to Manual"，codex 写 `def int pump_operation_complication = 0;` + `Autocontrol -> Manual : if [pump_operation_complication == 1]`，但全文没有任何 `pump_operation_complication = 1` 的赋值。

**结果**：static analyzer 报 `ERROR unwritten_read_var`，该 transition 永不触发 → forced transition 死代码。

**正确做法**（任选其一）：
1. **改成 event-driven**：`Autocontrol -> Manual :: PumpComplicationDetected` （让 event 充当触发器）
2. **用 abstract context input**：`def int pump_operation_complication = ?;`（pyfcstm 不直接支持 abstract var，所以一般用 1）
3. **forced fault + event**：`! * -> Manual :: PumpComplicationDetected;`（最贴合 NL 的"any state on fault → Manual"语义）

### ❌ A4 — Forced transition guard 读取永不被写的 var

**错误**：`! * -> Safe : if [emergency_flag == 1];` 但 `emergency_flag` 没有任何 effect 写它。

**结果**：static analyzer 报 `ERROR forced_unreachable`。

**正确做法**：用 event-driven forced transition 表达"任何 state 下接收某 event 就跳"：`! * -> Safe :: EmergencyEvent;`

### ❌ A5 — leaf state 无 outgoing transition（deadlock）

**错误**：`state Wait;` 作为 leaf state，但没有任何 `Wait -> X` transition。模型一旦进入 Wait 就永久卡住。

**结果**：static analyzer 报 `WARN deadlock_state`。

**正确做法**：要么给 Wait 加 outgoing transition（即使只是 `Wait -> NextMode :: SomeEvent`），要么 Wait 本质上是"终态"则将名字改为 `Done` / `Final` / `End` / `Halt` / `Stop`（analyzer 会跳过这些命名约定）。

### ✅ 良好范式 — 什么时候用 var vs event vs abstract action

| NL 语义 | 推荐编码 |
|---|---|
| "caregiver presses button X" / external trigger | **event** (`:: X`) |
| "from any state, on fault X go to Y" | **forced event** (`! * -> Y :: X`) |
| "the controller does X" / "X is logged" / "X is signaled" | **abstract action** (`enter abstract X` / `during abstract X`) |
| "if temperature > 100" / 真正的阈值比较 | **var** + **guard** + **action that writes the var** |
| "mode hierarchy with sub-phases" | **composite state** |
| "counter increments each cycle until threshold" | **var** + **during effect** + **guard on var** |

**核心原则**：var 只用于 **被 guard 读取 + 被某 action 写入** 的成对场景。否则用 event 或 abstract action。

## 必读上下文（逐项 Read，不要跳）

1. **STM.md case section**：`{{STM_PATH}}`
   - 找 `## 条目 N: {{CASE_NAME}}` 段（grep 定位 N，可能不是 1）
   - 重点读该 case 的 §0 识别判定 / §1 原文摘录 / §2 NL 描述 / §3 逐句溯源
2. **扩充版 NL（含 [E] 溯源 markers + provenance 数组）**：`{{EXPANSION_PATH}}`
   - 这是 reference 必须忠实于的英文 NL（也是 baseline 与 our method 共同实验输入）
3. **paper PDF**（必要时核对）：`{{PAPER_PDF}}`
4. **paper_content.txt**（grep 关键词友好）：`{{PAPER_CONTENT}}`
5. **pyfcstm grammar reference**：`{{GRAMMAR_REF_PATH}}` — pyfcstm DSL 完整语法
6. **pyfcstm DSL examples**（强烈推荐都读一遍）：
   - `pyfcstm/editors/jsfcstm/test/fixtures/visual/01-simple-leaf.fcstm`（最简单 flat FSM）
   - `pyfcstm/editors/jsfcstm/test/fixtures/visual/02-nested-hvac.fcstm`（HSM 层次 + sub-state）
   - `pyfcstm/editors/jsfcstm/test/fixtures/visual/06-guard-effect.fcstm`（变量 + 复合数值 guard + effect）
   - `pyfcstm/editors/jsfcstm/test/fixtures/visual/05-forced-expansion.fcstm`（`! forced transition`）
   - `pyfcstm/editors/jsfcstm/test/fixtures/visual/04-many-transitions.fcstm`（多 transition）
7. **PATH1 评测协议**：`{{REPO_ROOT}}/project_1_llm_state_machine_modeling/eval/PROTOCOL.md` — 5-component 抽取与计分规则

## 必须满足的硬约束

1. **5-component 完整性**：
   - **states**: 每个被 NL 明确命名的 mode / phase 都必须在 DSL 里有对应 state；不要遗漏；也不要为了"凑数"加 NL 没提的 helper state
   - **transitions**: 每条 NL 明确描述的 mode 切换都要写成一条 transition（含 src / tgt / event 或 guard）
   - **guards**: NL 中每个数值阈值 / 复合条件都要写成 guard expression（pyfcstm 支持复合算术 + bool）
   - **actions**: NL 中每个明确的 effector 操作 / 变量赋值 / cross-cutting 监控都要写成 entry / exit / do action 或 transition effect
   - **hierarchical_states**: 如果 NL 描述了 mode 内含 sub-phase，必须用 pyfcstm composite state 表达
2. **忠于 NL**：所有 mode / event / variable / threshold 名必须能在 STM §1 原文摘录或 expansion NL 的 provenance 找到对应；**禁止无中生有**
3. **pyfcstm primitive 恰当使用**（不强求堆砌）：
   - 原文有"each cycle / per tick / continuously" 语义 → 可用 `during {...}` 或 `>> during after` aspect
   - 原文有"任意 mode 下 emergency / abort to safe state" 语义 → 用 `! * -> Safe :: Event` forced transition
   - 原文有具名 effector （valve / pump / motor / sensor）→ 用 abstract action 占位（`enter abstract`）
   - **原文不支持的 primitive 不要硬塞**（在 notes 里说明哪个 primitive 未使用 + 原因）
4. **规模匹配**：states 数大致与原文描述相当（不要膨胀到 30+，也不要压缩到 1-2）；优先 6-15 states
5. **必须通过 pyfcstm 验证**：parse → sem → sim_smoke 全 OK + 5-component 自动抽取无异常

## 验证工具（**强制使用 Bash tool 反复调用**）

### Stage 1-4: parse + sem + sim_smoke + **static analysis** （4 关一体）

每次写完 DSL 跑一次：

```bash
cd {{REPO_ROOT}}
source venv/bin/activate
python3 project_1_llm_state_machine_modeling/paper_v1/selection/ref_stms/verify_pyfcstm.py {{OUTPUT_FCSTM}}
```

期望最后一行：`ALL_OK`（含 `STATIC_OK`）。任一阶段失败 → 读错误 → 修复 → 再跑。

**特别注意 STATIC stage**：parse / sem / sim_smoke 全过不代表逻辑正确。静态分析会捕获：

- `ERROR unwritten_read_var`：guard 读了从未被写的 var → 该 transition 永不触发（死代码）
- `ERROR forced_unreachable`：forced transition guard 只读 never-written var → 永不触发
- `WARN write_only_var`：var 被写但无 guard 读 → 大概率是 anti-pattern A1（NL fact 当 flag）
- `WARN high_var_to_state_ratio`：var 数 > 2x state 数 → 大概率是 fact 编码膨胀
- `WARN deadlock_state`：leaf state 无 outgoing → 进入即卡死
- `WARN unreachable_state`：state 无 incoming → 永远进不去

修复 ERROR 是**必须**的（STATIC_FAIL）；WARN 大多数情况也应修复（除非有充分理由保留）。

### 单独跑 static 分析器（debug 用）

```bash
python3 project_1_llm_state_machine_modeling/paper_v1/selection/ref_stms/verify_pyfcstm_static.py {{OUTPUT_FCSTM}}
```

会列出每个 ERROR/WARN 的具体 var/transition 名。

### 迭代上限提到 8 轮

由于现在多了一关 STATIC，建议最多 8 iter（之前 5 iter，加 3 iter 给 STATIC 修复用）。

### Stage 2: 5-component IR 自动抽取

smoke OK 后跑一次：

```bash
python3 project_1_llm_state_machine_modeling/paper_v1/selection/ref_stms/extract_components.py {{CASE_ID}} {{OUTPUT_FCSTM}} {{OUTPUT_COMPONENTS}}
```

期望输出：`EXTRACT_OK {states: N1, transitions: N2, guards: N3, actions: N4, hierarchical_states: N5}`

检查抽取结果合理性：
- `states` 数与你预期一致（如 NL 描述 6 mode，应该 ≈ 6）
- `transitions` 数覆盖了 NL 描述的全部切换
- `guards / actions` 没有大批量丢失

如果抽取数明显偏离预期，回到 DSL 检查是否有 state 没声明、guard 表达式被 parser 当成 action 等问题。

## 输出（必须写到下列文件）

1. **`{{OUTPUT_FCSTM}}`**：最终 pyfcstm DSL（必须通过 parse + sem + sim_smoke）
2. **`{{OUTPUT_COMPONENTS}}`**：5-component IR JSON（由 Stage 2 自动生成；不要手写）
3. **`{{OUTPUT_NOTES}}`**：markdown notes，结构如下：

```markdown
# Codex Draft Notes — Case {{CASE_ID}}

## 1. 设计选择

- mode 列表：[逐个列出，标注每个 mode 名来自 STM §1 摘录 X 或 expansion [En]]
- event 列表：[同上]
- variable 列表：[同上，含类型 + 初值，标注 threshold 来源]
- transition 设计：[关键 transition 列举，标注 guard / effect 的原文出处]
- 5-component IR 抽取计数：{states: N1, transitions: N2, guards: N3, actions: N4, hierarchical: N5}

## 2. pyfcstm primitive 使用情况（仅说明，不强求覆盖 4 个）

- **forced transition `!`**：用 / 未用 — 原文是否有全局 escape 语义
- **aspect `>> during`**：用 / 未用 — 原文是否有 per-tick monitor
- **abstract action**：用 / 未用 — 原文是否有具名 effector
- **multivar arith guard**：用 / 未用 — 原文是否有复合数值 guard

## 3. 与 NL 的对应关系

- expansion NL [E1]: "..." → 对应 DSL `state X` 或 `Y -> Z :: Event`
- expansion NL [E2]: ...
- （列举 5-10 条最关键映射即可）

## 4. 迭代历史

- iter 1: 写出初稿 → verify: PARSE_FAIL line 12 → 修复
- iter 2: PARSE_OK → SEM_FAIL → 修复
- iter 3: ALL_OK → EXTRACT_OK
- ...

## 5. 与 STM.md 表述的偏差（如有）

- 偏差 1: 把 NL 描述的 X 简化为 Y，理由：...
- 偏差 2: ...
- （如无偏差，写"无偏差，DSL 完整覆盖 NL 全部 5-component"）

## 6. 已知 hallucination / 不确定项（必须自我披露）

- 项 1: 引入 `helper_var` 用于内部计数，NL 未明示，但隐含需要
- （如无，写"无 hallucination"）
```

4. **`{{OUTPUT_RESULT}}`**：codex 最终输出的 strict JSON（无 markdown 包裹），schema:

```json
{
  "case_id": "{{CASE_ID}}",
  "status": "OK" | "PARTIAL" | "FAIL",
  "iter_count": <int>,
  "final_verify": "ALL_OK" | "SIM_FAIL: ..." | ...,
  "component_counts": {"states": N1, "transitions": N2, "guards": N3, "actions": N4, "hierarchical_states": N5},
  "primitive_used": {"forced_transition": true|false, "aspect_during": true|false, "abstract_action": true|false, "multivar_arith_guard": true|false},
  "summary": "1 句中文概述：states / transitions / guards / actions / hierarchical 大致内容 + 关键 primitive 使用",
  "hallucinations": [<list of self-disclosed unsupported elements>],
  "intentional_simplifications": [<list of NL details simplified or omitted, with reason>]
}
```

## 输出 strict JSON 到 stdout（不要 markdown 包裹）

最后输出 `{{OUTPUT_RESULT}}` 对应的 JSON 内容（codex agent_message 直接输出此 JSON，外部 shell 会写到文件）。
