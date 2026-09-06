# 评审包 — abs-fsm-brake-control / pred_buggy / states (状态)

- ref 实例数：**3**
- pred 实例数：**4**
- Claude annotations：**4**
- gpt-5.5 annotations：**4**

## 待评审材料

### 1) NL 原文（来自 sources/<case>/STM.md §2）

# ABS Brake Control FSM — NL Requirement

来源：`sources/abs-fsm-brake-control/STM.md` §2

The paper implements the single-wheel ABS hydraulic regulator as a
three-state FSM coupled with a PID-based slip controller. Wheel speed and
vehicle speed are used to compute the slip ratio, and the PID output drives
the Stateflow supervisor instead of sending commands directly to the
hydraulic valves.

The FSM contains the states `increase`, `hold`, and `decrease`, where

- `increase` sets `k1=1, k2=0, n=0`,
- `hold` neutralizes both valves with `k1=0, k2=0, n=0`,
- `decrease` sets `k1=0, k2=1, n=500` to release pressure.

The transition guards split the slip-error space into four bands:

- `increase -> hold` when `slp <= 0.01`
- `hold -> increase` when `slp > 0.01`
- `hold -> decrease` when `slp < -0.01`
- `decrease -> hold` when `slp >= -0.01`

This gives a concrete discrete supervisor that maps slip-error thresholds
to inlet-valve, return-valve, and pump actions while the continuous
wheel-slip dynamics remain in the plant model.

### 2) Reference 状态机模型（人工签字 ref，作为 ground-truth）

```
// Reference state machine for the ABS hydraulic regulator (3-state FSM).
//
// states + per-state outputs:
state increase   // outputs k1=1, k2=0, n=0
state hold       // outputs k1=0, k2=0, n=0
state decrease   // outputs k1=0, k2=1, n=500

// transitions (slp = slip-error from PID):
increase -> hold     when [slp <= 0.01]
hold     -> increase when [slp >  0.01]
hold     -> decrease when [slp < -0.01]
decrease -> hold     when [slp >= -0.01]
```

### 3) Predicted 状态机模型（被评对象，本条件下的输出）

```
// MOCK A0_baseline-style buggy prediction:
//   - `hold` renamed to `neutral` (semantic match TP expected)
//   - extra `warning` state not present in ref (FP expected)
state increase   // k1=1, k2=0, n=0
state neutral    // k1=0, k2=0, n=0  ← renamed from hold
state decrease   // k1=0, k2=1, n=500
state warning    // ← extra spurious state

increase -> neutral  when [slp <= 0.01]
neutral  -> increase when [slp >  0.01]
neutral  -> decrease when [slp < -0.01]
decrease -> neutral  when [slp >= -0.01]
```

---

## 使用说明

对每一行，在 **签字** 段勾选 `[x]`（4 选 1）：

- `[ ] 采纳 Claude`
- `[ ] 采纳 gpt-5.5`
- `[ ] 修改 → final_status: ___ （TP/FP/FN）`
- `[ ] 否决（两边都不对）→ final_status: ___`

**自动预勾选规则**：

- ✅ Claude 与 gpt-5.5 **完全一致** → 已默认勾选 `[x] 采纳 Claude`（与 gpt-5.5 等价）。如你不认同请手动改。
- 🔴 两边 **不一致** → 留空 + heading 标 `🔴 需复议`，请你亲自决定。
- 🟡 仅一方有提案 → 留空 + heading 标 `🟡 单票`，请你确认。
- 🔴 两方都未对该行给出意见 → 留空 + heading 标 `🔴 双方未提案`。

勾选默认空 → 该行视为未签字。把对应方框写成 `[x]` 表示采纳。`修改/否决` 时填写 final_status。备注栏可写任何文字。

---

## #1 ✅  ref `s0` ↔ pred `p0`  <!-- row001 -->

- **ref 实例**：`increase`；原文：`state increase — k1=1, k2=0, n=0 (pressurize)`
- **pred 实例**：`increase`；原文：`state increase — pressurize valve`

- **Claude 提案**：**TP（命中）**（match_kind=exact, confidence=0.99）  
  理由：Both are named 'increase' with identical pressurize semantics (k1=1, k2=0, n=0).
- **gpt-5.5 提案**：**TP（命中）**（match_kind=exact, confidence=0.98）  
  理由：Reference state increase sets k1=1, k2=0, n=0 for pressurization, and prediction has the same increase state for pressurizing the valve.

_两个 annotator 一致 → 已默认勾选 “采纳 Claude”（与 gpt-5.5 等价）；如不认同请手动改勾_

**签字**：
- [x] 采纳 Claude
- [ ] 采纳 gpt-5.5
- [ ] 修改 → final_status: ____  （TP/FP/FN）
- [ ] 否决 → final_status: ____
- 备注：

---

## #2 ✅  ref `s1` ↔ pred `p1`  <!-- row002 -->

- **ref 实例**：`hold`；原文：`state hold — k1=0, k2=0, n=0 (neutral)`
- **pred 实例**：`neutral`；原文：`state neutral — both valves shut, n=0 (renamed from hold)`

- **Claude 提案**：**TP（命中）**（match_kind=semantic, confidence=0.90）  
  理由：Pred 'neutral' is a rename of ref 'hold' with the same neutral output semantics (k1=0, k2=0, n=0).
- **gpt-5.5 提案**：**TP（命中）**（match_kind=semantic, confidence=0.97）  
  理由：Reference state hold neutralizes both valves with k1=0, k2=0, n=0, and predicted state neutral has the same neutral valve behavior and is explicitly described as renamed from hold.

_两个 annotator 一致 → 已默认勾选 “采纳 Claude”（与 gpt-5.5 等价）；如不认同请手动改勾_

**签字**：
- [x] 采纳 Claude
- [ ] 采纳 gpt-5.5
- [ ] 修改 → final_status: ____  （TP/FP/FN）
- [ ] 否决 → final_status: ____
- 备注：

---

## #3 ✅  ref `s2` ↔ pred `p2`  <!-- row003 -->

- **ref 实例**：`decrease`；原文：`state decrease — k1=0, k2=1, n=500 (release)`
- **pred 实例**：`decrease`；原文：`state decrease — release k1=0, k2=1, n=500`

- **Claude 提案**：**TP（命中）**（match_kind=exact, confidence=0.99）  
  理由：Both are named 'decrease' with identical release semantics (k1=0, k2=1, n=500).
- **gpt-5.5 提案**：**TP（命中）**（match_kind=exact, confidence=0.99）  
  理由：Reference state decrease releases pressure with k1=0, k2=1, n=500, and prediction has the same decrease state with k1=0, k2=1, n=500.

_两个 annotator 一致 → 已默认勾选 “采纳 Claude”（与 gpt-5.5 等价）；如不认同请手动改勾_

**签字**：
- [x] 采纳 Claude
- [ ] 采纳 gpt-5.5
- [ ] 修改 → final_status: ____  （TP/FP/FN）
- [ ] 否决 → final_status: ____
- 备注：

---

## #4 ✅  ref `∅` ↔ pred `p3`  <!-- row004 -->

- **ref 实例**：（无）
- **pred 实例**：`warning`；原文：`state warning — extra placeholder for fault alarm (not in NL)`

- **Claude 提案**：**FP（假阳）**（match_kind=none, confidence=0.95）  
  理由：Pred state 'warning' has no counterpart in the NL requirement or ref model; it is an extra spurious state.
- **gpt-5.5 提案**：**FP（假阳）**（match_kind=none, confidence=0.99）  
  理由：Predicted state warning is an extra fault-alarm placeholder, while the reference and NL requirement only define increase, hold, and decrease.

_两个 annotator 一致 → 已默认勾选 “采纳 Claude”（与 gpt-5.5 等价）；如不认同请手动改勾_

**签字**：
- [x] 采纳 Claude
- [ ] 采纳 gpt-5.5
- [ ] 修改 → final_status: ____  （TP/FP/FN）
- [ ] 否决 → final_status: ____
- 备注：

---

## Annotator 自报告 summary

- **Claude**：TP=3, FP=1, FN=0；notes：One semantic rename (hold→neutral) accepted as TP; one extra pred-only state flagged as FP.
- **gpt-5.5**：TP=3, FP=1, FN=0；notes：The only semantic rename is hold to neutral; warning is a pred-only state. No cascade rule applies for state classification.
