# 评审包 — abs-fsm-brake-control / pred_buggy / transitions (迁移)

- ref 实例数：**4**
- pred 实例数：**5**
- Claude annotations：**5**
- gpt-5.5 annotations：**6**

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

## #1 🟡 单票  ref `t0` ↔ pred `q0`  <!-- row001 -->

- **ref 实例**：原文：`increase -> hold when [slp <= 0.01]`
- **pred 实例**：原文：`increase -> neutral when [slp < 0.01]  (was <=, off-by-boundary)`

- **Claude 提案**：**TP（命中）**（match_kind=semantic, confidence=0.75）  
  理由：Both transitions go from increase to the neutral/hold state on a slip-below-threshold guard; guard boundary differs (< vs <=) but purpose matches.
- **gpt-5.5 提案**：（未提及）

_⚠️ 仅 Claude 给了提案，另一方缺失；请确认_

**签字**：
- [x] 采纳 Claude
- [ ] 采纳 gpt-5.5
- [ ] 修改 → final_status: ____  （TP/FP/FN）
- [ ] 否决 → final_status: ____
- 备注：

---

## #2 ✅  ref `t1` ↔ pred `q1`  <!-- row002 -->

- **ref 实例**：原文：`hold -> increase when [slp > 0.01]`
- **pred 实例**：原文：`neutral -> increase when [slp > 0.01]`

- **Claude 提案**：**TP（命中）**（match_kind=semantic, confidence=0.95）  
  理由：neutral->increase with slp>0.01 matches ref hold->increase with same guard (hold renamed to neutral).
- **gpt-5.5 提案**：**TP（命中）**（match_kind=semantic, confidence=0.95）  
  理由：Reference 'hold -> increase when [slp > 0.01]' matches prediction 'neutral -> increase when [slp > 0.01]' because 'neutral' is the renamed hold state with the same valve-neutral role.

_两个 annotator 一致 → 已默认勾选 “采纳 Claude”（与 gpt-5.5 等价）；如不认同请手动改勾_

**签字**：
- [x] 采纳 Claude
- [ ] 采纳 gpt-5.5
- [ ] 修改 → final_status: ____  （TP/FP/FN）
- [ ] 否决 → final_status: ____
- 备注：

---

## #3 ✅  ref `t2` ↔ pred `q2`  <!-- row003 -->

- **ref 实例**：原文：`hold -> decrease when [slp < -0.01]`
- **pred 实例**：原文：`neutral -> decrease when [slp < -0.01]`

- **Claude 提案**：**TP（命中）**（match_kind=semantic, confidence=0.95）  
  理由：neutral->decrease with slp<-0.01 matches ref hold->decrease with identical guard under hold->neutral renaming.
- **gpt-5.5 提案**：**TP（命中）**（match_kind=semantic, confidence=0.95）  
  理由：Reference 'hold -> decrease when [slp < -0.01]' matches prediction 'neutral -> decrease when [slp < -0.01]' because 'neutral' semantically corresponds to hold and the guard is unchanged.

_两个 annotator 一致 → 已默认勾选 “采纳 Claude”（与 gpt-5.5 等价）；如不认同请手动改勾_

**签字**：
- [x] 采纳 Claude
- [ ] 采纳 gpt-5.5
- [ ] 修改 → final_status: ____  （TP/FP/FN）
- [ ] 否决 → final_status: ____
- 备注：

---

## #4 ✅  ref `t3` ↔ pred `q3`  <!-- row004 -->

- **ref 实例**：原文：`decrease -> hold when [slp >= -0.01]`
- **pred 实例**：原文：`decrease -> neutral when [slp >= -0.01]`

- **Claude 提案**：**TP（命中）**（match_kind=semantic, confidence=0.95）  
  理由：decrease->neutral with slp>=-0.01 matches ref decrease->hold with identical guard under hold->neutral renaming.
- **gpt-5.5 提案**：**TP（命中）**（match_kind=semantic, confidence=0.95）  
  理由：Reference 'decrease -> hold when [slp >= -0.01]' matches prediction 'decrease -> neutral when [slp >= -0.01]' because 'neutral' semantically corresponds to hold and the guard is unchanged.

_两个 annotator 一致 → 已默认勾选 “采纳 Claude”（与 gpt-5.5 等价）；如不认同请手动改勾_

**签字**：
- [x] 采纳 Claude
- [ ] 采纳 gpt-5.5
- [ ] 修改 → final_status: ____  （TP/FP/FN）
- [ ] 否决 → final_status: ____
- 备注：

---

## #5 🟡 单票  ref `t0` ↔ pred `∅`  <!-- row005 -->

- **ref 实例**：原文：`increase -> hold when [slp <= 0.01]`
- **pred 实例**：（无）

- **Claude 提案**：（未提及）
- **gpt-5.5 提案**：**FN（漏报）**（match_kind=none, confidence=0.86）  
  理由：Reference transition 'increase -> hold when [slp <= 0.01]' has no equivalent prediction because q0 uses the boundary-excluding guard 'slp < 0.01'.

_⚠️ 仅 gpt-5.5 给了提案，另一方缺失；请确认_

**签字**：
- [ ] 采纳 Claude
- [x] 采纳 gpt-5.5
- [ ] 修改 → final_status: ____  （TP/FP/FN）
- [ ] 否决 → final_status: ____
- 备注：

---

## #6 🟡 单票  ref `∅` ↔ pred `q0`  <!-- row006 -->

- **ref 实例**：（无）
- **pred 实例**：原文：`increase -> neutral when [slp < 0.01]  (was <=, off-by-boundary)`

- **Claude 提案**：（未提及）
- **gpt-5.5 提案**：**FP（假阳）**（match_kind=none, confidence=0.86）  
  理由：Prediction 'increase -> neutral when [slp < 0.01]' is not equivalent to reference t0 because it excludes the required boundary case 'slp <= 0.01'.

_⚠️ 仅 gpt-5.5 给了提案，另一方缺失；请确认_

**签字**：
- [ ] 采纳 Claude
- [x] 采纳 gpt-5.5
- [ ] 修改 → final_status: ____  （TP/FP/FN）
- [ ] 否决 → final_status: ____
- 备注：

---

## #7 ✅  ref `∅` ↔ pred `q4`  <!-- row007 -->

- **ref 实例**：（无）
- **pred 实例**：原文：`decrease -> increase when [slp > 0.05] (spurious shortcut)`

- **Claude 提案**：**FP（假阳）**（match_kind=none, confidence=0.95）  
  理由：Spurious decrease->increase shortcut with guard slp>0.05 has no equivalent in the ref model.
- **gpt-5.5 提案**：**FP（假阳）**（match_kind=none, confidence=0.98）  
  理由：Prediction 'decrease -> increase when [slp > 0.05]' is a spurious shortcut with no corresponding reference transition.

_两个 annotator 一致 → 已默认勾选 “采纳 Claude”（与 gpt-5.5 等价）；如不认同请手动改勾_

**签字**：
- [x] 采纳 Claude
- [ ] 采纳 gpt-5.5
- [ ] 修改 → final_status: ____  （TP/FP/FN）
- [ ] 否决 → final_status: ____
- 备注：

---

## Annotator 自报告 summary

- **Claude**：TP=4, FP=1, FN=0；notes：hold is renamed to neutral throughout pred, yielding four semantic-match TPs; q4 is an extra spurious transition (FP). q0 has a boundary-off guard (< vs <=) but is still treated as a semantic TP at the transition level — the guard discrepancy would be flagged under the guards component_kind.
- **gpt-5.5**：TP=3, FP=2, FN=1；notes：The renamed state 'neutral' is treated as a semantic match for 'hold'. No cascade transition FP is triggered because the pred-only state 'warning' is not used by any predicted transition.
