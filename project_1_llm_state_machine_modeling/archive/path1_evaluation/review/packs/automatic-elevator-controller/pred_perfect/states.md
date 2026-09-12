# 评审包 — automatic-elevator-controller / pred_perfect / states (状态)

- ref 实例数：**7**
- pred 实例数：**7**
- Claude annotations：**7**
- gpt-5.5 annotations：**7**

## 待评审材料

### 1) NL 原文（来自 sources/<case>/STM.md §2）

# Automatic Elevator Controller — NL Requirement

来源：`sources/automatic-elevator-controller/STM.md` §2

The automatic elevator controller is built as a finite-state machine whose
state space combines floor states `F1`, `F2`, and `F3` with motion states
`MU2`, `MU3`, `MD1`, and `MD2` for upward and downward travel.

In the normal workflow, the system starts from an ideal state (on floor 1),
chooses either the up or down branch according to floor requests, stops at
the requested floor, and then immediately checks the next destination
before deciding whether to continue moving.

The controller uses `PS1/PS2/PS3` as floor-request inputs and `S1/S2/S3` as
sensing inputs for arrival. Transitions:

- From `F1`: `PS2` triggers `MU2`; `PS3` triggers `MU3`.
- From `F2`: `PS3` triggers `MU3`; `PS1` triggers `MD1`.
- From `F3`: `PS1` triggers `MD1`; `PS2` triggers `MD2`.
- Arrival sensors: `MU2 + S2 -> F2`; `MU3 + S3 -> F3`; `MD1 + S1 -> F1`;
  `MD2 + S2 -> F2`.

The `hbrg` output distinguishes upward drive, downward drive, and stop
conditions. A reset signal forces the controller back to floor 1 regardless
of the outstanding request context.

### 2) Reference 状态机模型（人工签字 ref，作为 ground-truth）

```
// Reference state machine (manual construction) for the automatic
// 3-floor elevator controller. Format-neutral pseudo-syntax for
// annotator context.
//
// states:
state F1   // floor 1 (initial)
state F2   // floor 2
state F3   // floor 3
state MU2  // moving up to F2
state MU3  // moving up to F3
state MD1  // moving down to F1
state MD2  // moving down to F2

// transitions:
F1 -> MU2 on PS2
F1 -> MU3 on PS3
F2 -> MU3 on PS3
F2 -> MD1 on PS1
F3 -> MD1 on PS1
F3 -> MD2 on PS2
MU2 -> F2 on S2
MU3 -> F3 on S3
MD1 -> F1 on S1
MD2 -> F2 on S2

// forced reset (from any state):
* -> F1 on Reset
```

### 3) Predicted 状态机模型（被评对象，本条件下的输出）

```
// MOCK A_full_ours-style prediction: identical to reference.
state F1
state F2
state F3
state MU2
state MU3
state MD1
state MD2

F1 -> MU2 on PS2
F1 -> MU3 on PS3
F2 -> MU3 on PS3
F2 -> MD1 on PS1
F3 -> MD1 on PS1
F3 -> MD2 on PS2
MU2 -> F2 on S2
MU3 -> F3 on S3
MD1 -> F1 on S1
MD2 -> F2 on S2
* -> F1 on Reset
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

- **ref 实例**：`F1`；原文：`state F1 — floor 1 (initial)`
- **pred 实例**：`F1`；原文：`state F1 — floor 1 (initial)`

- **Claude 提案**：**TP（命中）**（match_kind=exact, confidence=1.00）  
  理由：Both name 'F1' as floor 1 initial state.
- **gpt-5.5 提案**：**TP（命中）**（match_kind=exact, confidence=1.00）  
  理由：Reference snippet 'state F1 — floor 1 (initial)' exactly matches prediction snippet 'state F1 — floor 1 (initial)'.

_两个 annotator 一致 → 已默认勾选 “采纳 Claude”（与 gpt-5.5 等价）；如不认同请手动改勾_

**签字**：
- [x] 采纳 Claude
- [ ] 采纳 gpt-5.5
- [ ] 修改 → final_status: ____  （TP/FP/FN）
- [ ] 否决 → final_status: ____
- 备注：

---

## #2 ✅  ref `s1` ↔ pred `p1`  <!-- row002 -->

- **ref 实例**：`F2`；原文：`state F2 — floor 2`
- **pred 实例**：`F2`；原文：`state F2 — floor 2`

- **Claude 提案**：**TP（命中）**（match_kind=exact, confidence=1.00）  
  理由：Both name 'F2' as floor 2 state.
- **gpt-5.5 提案**：**TP（命中）**（match_kind=exact, confidence=1.00）  
  理由：Reference snippet 'state F2 — floor 2' exactly matches prediction snippet 'state F2 — floor 2'.

_两个 annotator 一致 → 已默认勾选 “采纳 Claude”（与 gpt-5.5 等价）；如不认同请手动改勾_

**签字**：
- [x] 采纳 Claude
- [ ] 采纳 gpt-5.5
- [ ] 修改 → final_status: ____  （TP/FP/FN）
- [ ] 否决 → final_status: ____
- 备注：

---

## #3 ✅  ref `s2` ↔ pred `p2`  <!-- row003 -->

- **ref 实例**：`F3`；原文：`state F3 — floor 3`
- **pred 实例**：`F3`；原文：`state F3 — floor 3`

- **Claude 提案**：**TP（命中）**（match_kind=exact, confidence=1.00）  
  理由：Both name 'F3' as floor 3 state.
- **gpt-5.5 提案**：**TP（命中）**（match_kind=exact, confidence=1.00）  
  理由：Reference snippet 'state F3 — floor 3' exactly matches prediction snippet 'state F3 — floor 3'.

_两个 annotator 一致 → 已默认勾选 “采纳 Claude”（与 gpt-5.5 等价）；如不认同请手动改勾_

**签字**：
- [x] 采纳 Claude
- [ ] 采纳 gpt-5.5
- [ ] 修改 → final_status: ____  （TP/FP/FN）
- [ ] 否决 → final_status: ____
- 备注：

---

## #4 ✅  ref `s3` ↔ pred `p3`  <!-- row004 -->

- **ref 实例**：`MU2`；原文：`state MU2 — moving up to floor 2`
- **pred 实例**：`MU2`；原文：`state MU2 — moving up to floor 2`

- **Claude 提案**：**TP（命中）**（match_kind=exact, confidence=1.00）  
  理由：Both name 'MU2' as moving up to floor 2.
- **gpt-5.5 提案**：**TP（命中）**（match_kind=exact, confidence=1.00）  
  理由：Reference snippet 'state MU2 — moving up to floor 2' exactly matches prediction snippet 'state MU2 — moving up to floor 2'.

_两个 annotator 一致 → 已默认勾选 “采纳 Claude”（与 gpt-5.5 等价）；如不认同请手动改勾_

**签字**：
- [x] 采纳 Claude
- [ ] 采纳 gpt-5.5
- [ ] 修改 → final_status: ____  （TP/FP/FN）
- [ ] 否决 → final_status: ____
- 备注：

---

## #5 ✅  ref `s4` ↔ pred `p4`  <!-- row005 -->

- **ref 实例**：`MU3`；原文：`state MU3 — moving up to floor 3`
- **pred 实例**：`MU3`；原文：`state MU3 — moving up to floor 3`

- **Claude 提案**：**TP（命中）**（match_kind=exact, confidence=1.00）  
  理由：Both name 'MU3' as moving up to floor 3.
- **gpt-5.5 提案**：**TP（命中）**（match_kind=exact, confidence=1.00）  
  理由：Reference snippet 'state MU3 — moving up to floor 3' exactly matches prediction snippet 'state MU3 — moving up to floor 3'.

_两个 annotator 一致 → 已默认勾选 “采纳 Claude”（与 gpt-5.5 等价）；如不认同请手动改勾_

**签字**：
- [x] 采纳 Claude
- [ ] 采纳 gpt-5.5
- [ ] 修改 → final_status: ____  （TP/FP/FN）
- [ ] 否决 → final_status: ____
- 备注：

---

## #6 ✅  ref `s5` ↔ pred `p5`  <!-- row006 -->

- **ref 实例**：`MD1`；原文：`state MD1 — moving down to floor 1`
- **pred 实例**：`MD1`；原文：`state MD1 — moving down to floor 1`

- **Claude 提案**：**TP（命中）**（match_kind=exact, confidence=1.00）  
  理由：Both name 'MD1' as moving down to floor 1.
- **gpt-5.5 提案**：**TP（命中）**（match_kind=exact, confidence=1.00）  
  理由：Reference snippet 'state MD1 — moving down to floor 1' exactly matches prediction snippet 'state MD1 — moving down to floor 1'.

_两个 annotator 一致 → 已默认勾选 “采纳 Claude”（与 gpt-5.5 等价）；如不认同请手动改勾_

**签字**：
- [x] 采纳 Claude
- [ ] 采纳 gpt-5.5
- [ ] 修改 → final_status: ____  （TP/FP/FN）
- [ ] 否决 → final_status: ____
- 备注：

---

## #7 ✅  ref `s6` ↔ pred `p6`  <!-- row007 -->

- **ref 实例**：`MD2`；原文：`state MD2 — moving down to floor 2`
- **pred 实例**：`MD2`；原文：`state MD2 — moving down to floor 2`

- **Claude 提案**：**TP（命中）**（match_kind=exact, confidence=1.00）  
  理由：Both name 'MD2' as moving down to floor 2.
- **gpt-5.5 提案**：**TP（命中）**（match_kind=exact, confidence=1.00）  
  理由：Reference snippet 'state MD2 — moving down to floor 2' exactly matches prediction snippet 'state MD2 — moving down to floor 2'.

_两个 annotator 一致 → 已默认勾选 “采纳 Claude”（与 gpt-5.5 等价）；如不认同请手动改勾_

**签字**：
- [x] 采纳 Claude
- [ ] 采纳 gpt-5.5
- [ ] 修改 → final_status: ____  （TP/FP/FN）
- [ ] 否决 → final_status: ____
- 备注：

---

## Annotator 自报告 summary

- **Claude**：TP=7, FP=0, FN=0；notes：Prediction is identical to reference; all 7 states match exactly by name.
- **gpt-5.5**：TP=7, FP=0, FN=0；notes：All predicted states are exact-name matches to the reference states; no cascade rules apply for state classification.
