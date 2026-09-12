# 评审包 — automatic-elevator-controller / pred_perfect / transitions (迁移)

- ref 实例数：**11**
- pred 实例数：**11**
- Claude annotations：**11**
- gpt-5.5 annotations：**11**

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

## #1 ✅  ref `t0` ↔ pred `q0`  <!-- row001 -->

- **ref 实例**：原文：`F1 -> MU2 on PS2`
- **pred 实例**：原文：`F1 -> MU2 on PS2`

- **Claude 提案**：**TP（命中）**（match_kind=exact, confidence=1.00）  
  理由：Exact match: F1 -> MU2 on PS2.
- **gpt-5.5 提案**：**TP（命中）**（match_kind=exact, confidence=1.00）  
  理由：Reference transition "F1 -> MU2 on PS2" exactly matches predicted transition "F1 -> MU2 on PS2" with the same source, target, and event.

_两个 annotator 一致 → 已默认勾选 “采纳 Claude”（与 gpt-5.5 等价）；如不认同请手动改勾_

**签字**：
- [x] 采纳 Claude
- [ ] 采纳 gpt-5.5
- [ ] 修改 → final_status: ____  （TP/FP/FN）
- [ ] 否决 → final_status: ____
- 备注：

---

## #2 ✅  ref `t1` ↔ pred `q1`  <!-- row002 -->

- **ref 实例**：原文：`F1 -> MU3 on PS3`
- **pred 实例**：原文：`F1 -> MU3 on PS3`

- **Claude 提案**：**TP（命中）**（match_kind=exact, confidence=1.00）  
  理由：Exact match: F1 -> MU3 on PS3.
- **gpt-5.5 提案**：**TP（命中）**（match_kind=exact, confidence=1.00）  
  理由：Reference transition "F1 -> MU3 on PS3" exactly matches predicted transition "F1 -> MU3 on PS3" with the same source, target, and event.

_两个 annotator 一致 → 已默认勾选 “采纳 Claude”（与 gpt-5.5 等价）；如不认同请手动改勾_

**签字**：
- [x] 采纳 Claude
- [ ] 采纳 gpt-5.5
- [ ] 修改 → final_status: ____  （TP/FP/FN）
- [ ] 否决 → final_status: ____
- 备注：

---

## #3 ✅  ref `t10` ↔ pred `q10`  <!-- row003 -->

- **ref 实例**：原文：`* -> F1 on Reset (forced reset)`
- **pred 实例**：原文：`* -> F1 on Reset (forced reset)`

- **Claude 提案**：**TP（命中）**（match_kind=exact, confidence=1.00）  
  理由：Exact match: forced reset * -> F1 on Reset.
- **gpt-5.5 提案**：**TP（命中）**（match_kind=exact, confidence=1.00）  
  理由：Reference forced reset transition "* -> F1 on Reset (forced reset)" exactly matches predicted forced reset transition "* -> F1 on Reset (forced reset)".

_两个 annotator 一致 → 已默认勾选 “采纳 Claude”（与 gpt-5.5 等价）；如不认同请手动改勾_

**签字**：
- [x] 采纳 Claude
- [ ] 采纳 gpt-5.5
- [ ] 修改 → final_status: ____  （TP/FP/FN）
- [ ] 否决 → final_status: ____
- 备注：

---

## #4 ✅  ref `t2` ↔ pred `q2`  <!-- row004 -->

- **ref 实例**：原文：`F2 -> MU3 on PS3`
- **pred 实例**：原文：`F2 -> MU3 on PS3`

- **Claude 提案**：**TP（命中）**（match_kind=exact, confidence=1.00）  
  理由：Exact match: F2 -> MU3 on PS3.
- **gpt-5.5 提案**：**TP（命中）**（match_kind=exact, confidence=1.00）  
  理由：Reference transition "F2 -> MU3 on PS3" exactly matches predicted transition "F2 -> MU3 on PS3" with the same source, target, and event.

_两个 annotator 一致 → 已默认勾选 “采纳 Claude”（与 gpt-5.5 等价）；如不认同请手动改勾_

**签字**：
- [x] 采纳 Claude
- [ ] 采纳 gpt-5.5
- [ ] 修改 → final_status: ____  （TP/FP/FN）
- [ ] 否决 → final_status: ____
- 备注：

---

## #5 ✅  ref `t3` ↔ pred `q3`  <!-- row005 -->

- **ref 实例**：原文：`F2 -> MD1 on PS1`
- **pred 实例**：原文：`F2 -> MD1 on PS1`

- **Claude 提案**：**TP（命中）**（match_kind=exact, confidence=1.00）  
  理由：Exact match: F2 -> MD1 on PS1.
- **gpt-5.5 提案**：**TP（命中）**（match_kind=exact, confidence=1.00）  
  理由：Reference transition "F2 -> MD1 on PS1" exactly matches predicted transition "F2 -> MD1 on PS1" with the same source, target, and event.

_两个 annotator 一致 → 已默认勾选 “采纳 Claude”（与 gpt-5.5 等价）；如不认同请手动改勾_

**签字**：
- [x] 采纳 Claude
- [ ] 采纳 gpt-5.5
- [ ] 修改 → final_status: ____  （TP/FP/FN）
- [ ] 否决 → final_status: ____
- 备注：

---

## #6 ✅  ref `t4` ↔ pred `q4`  <!-- row006 -->

- **ref 实例**：原文：`F3 -> MD1 on PS1`
- **pred 实例**：原文：`F3 -> MD1 on PS1`

- **Claude 提案**：**TP（命中）**（match_kind=exact, confidence=1.00）  
  理由：Exact match: F3 -> MD1 on PS1.
- **gpt-5.5 提案**：**TP（命中）**（match_kind=exact, confidence=1.00）  
  理由：Reference transition "F3 -> MD1 on PS1" exactly matches predicted transition "F3 -> MD1 on PS1" with the same source, target, and event.

_两个 annotator 一致 → 已默认勾选 “采纳 Claude”（与 gpt-5.5 等价）；如不认同请手动改勾_

**签字**：
- [x] 采纳 Claude
- [ ] 采纳 gpt-5.5
- [ ] 修改 → final_status: ____  （TP/FP/FN）
- [ ] 否决 → final_status: ____
- 备注：

---

## #7 ✅  ref `t5` ↔ pred `q5`  <!-- row007 -->

- **ref 实例**：原文：`F3 -> MD2 on PS2`
- **pred 实例**：原文：`F3 -> MD2 on PS2`

- **Claude 提案**：**TP（命中）**（match_kind=exact, confidence=1.00）  
  理由：Exact match: F3 -> MD2 on PS2.
- **gpt-5.5 提案**：**TP（命中）**（match_kind=exact, confidence=1.00）  
  理由：Reference transition "F3 -> MD2 on PS2" exactly matches predicted transition "F3 -> MD2 on PS2" with the same source, target, and event.

_两个 annotator 一致 → 已默认勾选 “采纳 Claude”（与 gpt-5.5 等价）；如不认同请手动改勾_

**签字**：
- [x] 采纳 Claude
- [ ] 采纳 gpt-5.5
- [ ] 修改 → final_status: ____  （TP/FP/FN）
- [ ] 否决 → final_status: ____
- 备注：

---

## #8 ✅  ref `t6` ↔ pred `q6`  <!-- row008 -->

- **ref 实例**：原文：`MU2 -> F2 on S2`
- **pred 实例**：原文：`MU2 -> F2 on S2`

- **Claude 提案**：**TP（命中）**（match_kind=exact, confidence=1.00）  
  理由：Exact match: MU2 -> F2 on S2.
- **gpt-5.5 提案**：**TP（命中）**（match_kind=exact, confidence=1.00）  
  理由：Reference transition "MU2 -> F2 on S2" exactly matches predicted transition "MU2 -> F2 on S2" with the same source, target, and event.

_两个 annotator 一致 → 已默认勾选 “采纳 Claude”（与 gpt-5.5 等价）；如不认同请手动改勾_

**签字**：
- [x] 采纳 Claude
- [ ] 采纳 gpt-5.5
- [ ] 修改 → final_status: ____  （TP/FP/FN）
- [ ] 否决 → final_status: ____
- 备注：

---

## #9 ✅  ref `t7` ↔ pred `q7`  <!-- row009 -->

- **ref 实例**：原文：`MU3 -> F3 on S3`
- **pred 实例**：原文：`MU3 -> F3 on S3`

- **Claude 提案**：**TP（命中）**（match_kind=exact, confidence=1.00）  
  理由：Exact match: MU3 -> F3 on S3.
- **gpt-5.5 提案**：**TP（命中）**（match_kind=exact, confidence=1.00）  
  理由：Reference transition "MU3 -> F3 on S3" exactly matches predicted transition "MU3 -> F3 on S3" with the same source, target, and event.

_两个 annotator 一致 → 已默认勾选 “采纳 Claude”（与 gpt-5.5 等价）；如不认同请手动改勾_

**签字**：
- [x] 采纳 Claude
- [ ] 采纳 gpt-5.5
- [ ] 修改 → final_status: ____  （TP/FP/FN）
- [ ] 否决 → final_status: ____
- 备注：

---

## #10 ✅  ref `t8` ↔ pred `q8`  <!-- row010 -->

- **ref 实例**：原文：`MD1 -> F1 on S1`
- **pred 实例**：原文：`MD1 -> F1 on S1`

- **Claude 提案**：**TP（命中）**（match_kind=exact, confidence=1.00）  
  理由：Exact match: MD1 -> F1 on S1.
- **gpt-5.5 提案**：**TP（命中）**（match_kind=exact, confidence=1.00）  
  理由：Reference transition "MD1 -> F1 on S1" exactly matches predicted transition "MD1 -> F1 on S1" with the same source, target, and event.

_两个 annotator 一致 → 已默认勾选 “采纳 Claude”（与 gpt-5.5 等价）；如不认同请手动改勾_

**签字**：
- [x] 采纳 Claude
- [ ] 采纳 gpt-5.5
- [ ] 修改 → final_status: ____  （TP/FP/FN）
- [ ] 否决 → final_status: ____
- 备注：

---

## #11 ✅  ref `t9` ↔ pred `q9`  <!-- row011 -->

- **ref 实例**：原文：`MD2 -> F2 on S2`
- **pred 实例**：原文：`MD2 -> F2 on S2`

- **Claude 提案**：**TP（命中）**（match_kind=exact, confidence=1.00）  
  理由：Exact match: MD2 -> F2 on S2.
- **gpt-5.5 提案**：**TP（命中）**（match_kind=exact, confidence=1.00）  
  理由：Reference transition "MD2 -> F2 on S2" exactly matches predicted transition "MD2 -> F2 on S2" with the same source, target, and event.

_两个 annotator 一致 → 已默认勾选 “采纳 Claude”（与 gpt-5.5 等价）；如不认同请手动改勾_

**签字**：
- [x] 采纳 Claude
- [ ] 采纳 gpt-5.5
- [ ] 修改 → final_status: ____  （TP/FP/FN）
- [ ] 否决 → final_status: ____
- 备注：

---

## Annotator 自报告 summary

- **Claude**：TP=11, FP=0, FN=0；notes：Prediction is identical to reference; all 11 transitions match exactly.
- **gpt-5.5**：TP=11, FP=0, FN=0；notes：All predicted transitions exactly match the reference transitions; no cascade rules are triggered.
