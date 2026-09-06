# 评审包 — automatic-elevator-controller / pred_buggy / transitions (迁移)

- ref 实例数：**11**
- pred 实例数：**10**
- Claude annotations：**12**
- gpt-5.5 annotations：**12**

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
// MOCK A0_baseline-style buggy prediction:
//   - missing MD2 (FN expected)
//   - MU2 renamed to `going_up_2` (semantic match TP expected)
//   - extra `maintenance` state not present in ref (FP expected)

state F1
state F2
state F3
state going_up_2  // ← MU2 renamed
state MU3
state MD1
state maintenance  // ← extra spurious state, not in ref

F1 -> going_up_2 on PS2
F1 -> MU3 on PS3
F2 -> MU3 on PS3
F2 -> MD1 on PS1
F3 -> MD1 on PS1
// (no F3 -> MD2 transition because MD2 is missing)
going_up_2 -> F2 on S2
MU3 -> F3 on S3
MD1 -> F1 on S1
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
- **pred 实例**：原文：`F1 -> going_up_2 on PS2 (renamed-target counterpart of F1->MU2)`

- **Claude 提案**：**TP（命中）**（match_kind=semantic, confidence=0.90）  
  理由：F1->MU2 on PS2 matches F1->going_up_2 on PS2 via renamed target state (MU2≡going_up_2).
- **gpt-5.5 提案**：**TP（命中）**（match_kind=semantic, confidence=0.98）  
  理由：Reference 'F1 -> MU2 on PS2' matches prediction 'F1 -> going_up_2 on PS2' because going_up_2 is the renamed counterpart of MU2 with the same source, event, and motion-to-floor-2 purpose.

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
  理由：F1->MU3 on PS3 matches exactly.
- **gpt-5.5 提案**：**TP（命中）**（match_kind=exact, confidence=1.00）  
  理由：Reference 'F1 -> MU3 on PS3' exactly matches prediction 'F1 -> MU3 on PS3'.

_两个 annotator 一致 → 已默认勾选 “采纳 Claude”（与 gpt-5.5 等价）；如不认同请手动改勾_

**签字**：
- [x] 采纳 Claude
- [ ] 采纳 gpt-5.5
- [ ] 修改 → final_status: ____  （TP/FP/FN）
- [ ] 否决 → final_status: ____
- 备注：

---

## #3 ✅  ref `t10` ↔ pred `q9`  <!-- row003 -->

- **ref 实例**：原文：`* -> F1 on Reset (forced reset)`
- **pred 实例**：原文：`* -> F1 on Reset`

- **Claude 提案**：**TP（命中）**（match_kind=exact, confidence=1.00）  
  理由：Forced reset * -> F1 on Reset matches exactly.
- **gpt-5.5 提案**：**TP（命中）**（match_kind=exact, confidence=1.00）  
  理由：Reference forced reset '* -> F1 on Reset' exactly matches prediction '* -> F1 on Reset'.

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
  理由：F2->MU3 on PS3 matches exactly.
- **gpt-5.5 提案**：**TP（命中）**（match_kind=exact, confidence=1.00）  
  理由：Reference 'F2 -> MU3 on PS3' exactly matches prediction 'F2 -> MU3 on PS3'.

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
  理由：F2->MD1 on PS1 matches exactly.
- **gpt-5.5 提案**：**TP（命中）**（match_kind=exact, confidence=1.00）  
  理由：Reference 'F2 -> MD1 on PS1' exactly matches prediction 'F2 -> MD1 on PS1'.

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
  理由：F3->MD1 on PS1 matches exactly.
- **gpt-5.5 提案**：**TP（命中）**（match_kind=exact, confidence=1.00）  
  理由：Reference 'F3 -> MD1 on PS1' exactly matches prediction 'F3 -> MD1 on PS1'.

_两个 annotator 一致 → 已默认勾选 “采纳 Claude”（与 gpt-5.5 等价）；如不认同请手动改勾_

**签字**：
- [x] 采纳 Claude
- [ ] 采纳 gpt-5.5
- [ ] 修改 → final_status: ____  （TP/FP/FN）
- [ ] 否决 → final_status: ____
- 备注：

---

## #7 ✅  ref `t6` ↔ pred `q5`  <!-- row007 -->

- **ref 实例**：原文：`MU2 -> F2 on S2`
- **pred 实例**：原文：`going_up_2 -> F2 on S2 (renamed-source counterpart of MU2->F2)`

- **Claude 提案**：**TP（命中）**（match_kind=semantic, confidence=0.90）  
  理由：MU2->F2 on S2 matches going_up_2->F2 on S2 via renamed source state.
- **gpt-5.5 提案**：**TP（命中）**（match_kind=semantic, confidence=0.98）  
  理由：Reference 'MU2 -> F2 on S2' matches prediction 'going_up_2 -> F2 on S2' because going_up_2 is the renamed counterpart of MU2 and the arrival sensor S2 leads to F2 in both.

_两个 annotator 一致 → 已默认勾选 “采纳 Claude”（与 gpt-5.5 等价）；如不认同请手动改勾_

**签字**：
- [x] 采纳 Claude
- [ ] 采纳 gpt-5.5
- [ ] 修改 → final_status: ____  （TP/FP/FN）
- [ ] 否决 → final_status: ____
- 备注：

---

## #8 ✅  ref `t7` ↔ pred `q6`  <!-- row008 -->

- **ref 实例**：原文：`MU3 -> F3 on S3`
- **pred 实例**：原文：`MU3 -> F3 on S3`

- **Claude 提案**：**TP（命中）**（match_kind=exact, confidence=1.00）  
  理由：MU3->F3 on S3 matches exactly.
- **gpt-5.5 提案**：**TP（命中）**（match_kind=exact, confidence=1.00）  
  理由：Reference 'MU3 -> F3 on S3' exactly matches prediction 'MU3 -> F3 on S3'.

_两个 annotator 一致 → 已默认勾选 “采纳 Claude”（与 gpt-5.5 等价）；如不认同请手动改勾_

**签字**：
- [x] 采纳 Claude
- [ ] 采纳 gpt-5.5
- [ ] 修改 → final_status: ____  （TP/FP/FN）
- [ ] 否决 → final_status: ____
- 备注：

---

## #9 ✅  ref `t8` ↔ pred `q7`  <!-- row009 -->

- **ref 实例**：原文：`MD1 -> F1 on S1`
- **pred 实例**：原文：`MD1 -> F1 on S1`

- **Claude 提案**：**TP（命中）**（match_kind=exact, confidence=1.00）  
  理由：MD1->F1 on S1 matches exactly.
- **gpt-5.5 提案**：**TP（命中）**（match_kind=exact, confidence=1.00）  
  理由：Reference 'MD1 -> F1 on S1' exactly matches prediction 'MD1 -> F1 on S1'.

_两个 annotator 一致 → 已默认勾选 “采纳 Claude”（与 gpt-5.5 等价）；如不认同请手动改勾_

**签字**：
- [x] 采纳 Claude
- [ ] 采纳 gpt-5.5
- [ ] 修改 → final_status: ____  （TP/FP/FN）
- [ ] 否决 → final_status: ____
- 备注：

---

## #10 ✅  ref `t5` ↔ pred `∅`  <!-- row010 -->

- **ref 实例**：原文：`F3 -> MD2 on PS2`
- **pred 实例**：（无）

- **Claude 提案**：**FN（漏报）**（match_kind=none, confidence=1.00）  
  理由：F3->MD2 on PS2 has no counterpart in pred since MD2 state is missing.
- **gpt-5.5 提案**：**FN（漏报）**（match_kind=none, confidence=1.00）  
  理由：Reference transition 'F3 -> MD2 on PS2' has no predicted equivalent because the prediction omits the F3-to-MD2 request transition.

_两个 annotator 一致 → 已默认勾选 “采纳 Claude”（与 gpt-5.5 等价）；如不认同请手动改勾_

**签字**：
- [x] 采纳 Claude
- [ ] 采纳 gpt-5.5
- [ ] 修改 → final_status: ____  （TP/FP/FN）
- [ ] 否决 → final_status: ____
- 备注：

---

## #11 ✅  ref `t9` ↔ pred `∅`  <!-- row011 -->

- **ref 实例**：原文：`MD2 -> F2 on S2`
- **pred 实例**：（无）

- **Claude 提案**：**FN（漏报）**（match_kind=none, confidence=1.00）  
  理由：MD2->F2 on S2 has no counterpart in pred since MD2 state is missing.
- **gpt-5.5 提案**：**FN（漏报）**（match_kind=none, confidence=1.00）  
  理由：Reference transition 'MD2 -> F2 on S2' has no predicted equivalent because the prediction omits the MD2 moving-down-to-floor-2 state and its arrival transition.

_两个 annotator 一致 → 已默认勾选 “采纳 Claude”（与 gpt-5.5 等价）；如不认同请手动改勾_

**签字**：
- [x] 采纳 Claude
- [ ] 采纳 gpt-5.5
- [ ] 修改 → final_status: ____  （TP/FP/FN）
- [ ] 否决 → final_status: ____
- 备注：

---

## #12 ✅  ref `∅` ↔ pred `q8`  <!-- row012 -->

- **ref 实例**：（无）
- **pred 实例**：原文：`F2 -> maintenance on Fault (spurious — cascades FP through maintenance FP state)`

- **Claude 提案**：**FP（假阳）**（match_kind=cascade, confidence=1.00）  
  理由：F2->maintenance on Fault is FP via cascade through the FP target state 'maintenance' which has no ref counterpart.
- **gpt-5.5 提案**：**FP（假阳）**（match_kind=cascade, confidence=1.00）  
  理由：Prediction 'F2 -> maintenance on Fault' is FP by cascade because its target 'maintenance' is a pred-only FP state not present in the reference model.

_两个 annotator 一致 → 已默认勾选 “采纳 Claude”（与 gpt-5.5 等价）；如不认同请手动改勾_

**签字**：
- [x] 采纳 Claude
- [ ] 采纳 gpt-5.5
- [ ] 修改 → final_status: ____  （TP/FP/FN）
- [ ] 否决 → final_status: ____
- 备注：

---

## Annotator 自报告 summary

- **Claude**：TP=9, FP=1, FN=2；notes：Cascade FP triggered by spurious 'maintenance' state on q8; two FN transitions cascade from the missing MD2 state in pred.
- **gpt-5.5**：TP=9, FP=1, FN=2；notes：The renamed state going_up_2 is treated as a semantic match for MU2, so its incident transitions are TPs. The spurious transition to maintenance is a cascade FP because maintenance is a pred-only state.
