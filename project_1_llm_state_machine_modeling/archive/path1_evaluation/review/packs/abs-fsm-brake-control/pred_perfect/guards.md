# 评审包 — abs-fsm-brake-control / pred_perfect / guards (守卫)

- ref 实例数：**4**
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
// MOCK A_full_ours-style prediction: identical to reference.
state increase   // k1=1, k2=0, n=0
state hold       // k1=0, k2=0, n=0
state decrease   // k1=0, k2=1, n=500

increase -> hold     when [slp <= 0.01]
hold     -> increase when [slp >  0.01]
hold     -> decrease when [slp < -0.01]
decrease -> hold     when [slp >= -0.01]
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

## #1 ✅  ref `g0` ↔ pred `r0`  <!-- row001 -->

- **ref 实例**：`slp <= 0.01`；原文：`guard [slp <= 0.01] on increase -> hold`
- **pred 实例**：`slp <= 0.01`；原文：`guard [slp <= 0.01] on increase -> hold`

- **Claude 提案**：**TP（命中）**（match_kind=exact, confidence=1.00）  
  理由：Both guards have identical expression 'slp <= 0.01' on the increase -> hold transition.
- **gpt-5.5 提案**：**TP（命中）**（match_kind=exact, confidence=1.00）  
  理由：Both snippets specify guard [slp <= 0.01] on the increase -> hold transition.

_两个 annotator 一致 → 已默认勾选 “采纳 Claude”（与 gpt-5.5 等价）；如不认同请手动改勾_

**签字**：
- [x] 采纳 Claude
- [ ] 采纳 gpt-5.5
- [ ] 修改 → final_status: ____  （TP/FP/FN）
- [ ] 否决 → final_status: ____
- 备注：

---

## #2 ✅  ref `g1` ↔ pred `r1`  <!-- row002 -->

- **ref 实例**：`slp > 0.01`；原文：`guard [slp > 0.01] on hold -> increase`
- **pred 实例**：`slp > 0.01`；原文：`guard [slp > 0.01] on hold -> increase`

- **Claude 提案**：**TP（命中）**（match_kind=exact, confidence=1.00）  
  理由：Both guards have identical expression 'slp > 0.01' on the hold -> increase transition.
- **gpt-5.5 提案**：**TP（命中）**（match_kind=exact, confidence=1.00）  
  理由：Both snippets specify guard [slp > 0.01] on the hold -> increase transition.

_两个 annotator 一致 → 已默认勾选 “采纳 Claude”（与 gpt-5.5 等价）；如不认同请手动改勾_

**签字**：
- [x] 采纳 Claude
- [ ] 采纳 gpt-5.5
- [ ] 修改 → final_status: ____  （TP/FP/FN）
- [ ] 否决 → final_status: ____
- 备注：

---

## #3 ✅  ref `g2` ↔ pred `r2`  <!-- row003 -->

- **ref 实例**：`slp < -0.01`；原文：`guard [slp < -0.01] on hold -> decrease`
- **pred 实例**：`slp < -0.01`；原文：`guard [slp < -0.01] on hold -> decrease`

- **Claude 提案**：**TP（命中）**（match_kind=exact, confidence=1.00）  
  理由：Both guards have identical expression 'slp < -0.01' on the hold -> decrease transition.
- **gpt-5.5 提案**：**TP（命中）**（match_kind=exact, confidence=1.00）  
  理由：Both snippets specify guard [slp < -0.01] on the hold -> decrease transition.

_两个 annotator 一致 → 已默认勾选 “采纳 Claude”（与 gpt-5.5 等价）；如不认同请手动改勾_

**签字**：
- [x] 采纳 Claude
- [ ] 采纳 gpt-5.5
- [ ] 修改 → final_status: ____  （TP/FP/FN）
- [ ] 否决 → final_status: ____
- 备注：

---

## #4 ✅  ref `g3` ↔ pred `r3`  <!-- row004 -->

- **ref 实例**：`slp >= -0.01`；原文：`guard [slp >= -0.01] on decrease -> hold`
- **pred 实例**：`slp >= -0.01`；原文：`guard [slp >= -0.01] on decrease -> hold`

- **Claude 提案**：**TP（命中）**（match_kind=exact, confidence=1.00）  
  理由：Both guards have identical expression 'slp >= -0.01' on the decrease -> hold transition.
- **gpt-5.5 提案**：**TP（命中）**（match_kind=exact, confidence=1.00）  
  理由：Both snippets specify guard [slp >= -0.01] on the decrease -> hold transition.

_两个 annotator 一致 → 已默认勾选 “采纳 Claude”（与 gpt-5.5 等价）；如不认同请手动改勾_

**签字**：
- [x] 采纳 Claude
- [ ] 采纳 gpt-5.5
- [ ] 修改 → final_status: ____  （TP/FP/FN）
- [ ] 否决 → final_status: ____
- 备注：

---

## Annotator 自报告 summary

- **Claude**：TP=4, FP=0, FN=0；notes：Prediction is identical to reference; all four guards match exactly.
- **gpt-5.5**：TP=4, FP=0, FN=0；notes：All predicted guards exactly match the reference guard expressions and transition contexts; no cascade cases apply.
