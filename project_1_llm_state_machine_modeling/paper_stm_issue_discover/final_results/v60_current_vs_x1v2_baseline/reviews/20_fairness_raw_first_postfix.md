# Raw-first fairness review: postfix

> Historical-status notice, added after targeted repair. The two `FAIL`
> snapshots below preserve the pre-fix evidence for the original
> `location_text` leak and the subsequent `claim_text` leak. They are not the
> release status. Both projection-only defects were repaired in
> `scripts/evaluation/build_reviewer_projection.py`, covered by the
> provider-free regression fixture, and independently rechecked against the
> current projection in [22_fairness_projection_rereview.md](22_fairness_projection_rereview.md).
> `FAIR-20-001` is therefore `FIXED`; the current targeted verdict is `PASS`.

**身份**：`subagent:fairness-raw-first-reviewer`。本文件是独立的 proposal-only review，不是最终人工裁定。

**时间**：`2026-08-29T18:26:19+08:00`

**结论**：`FAIL`。

## Declared Inputs

本 reviewer 只读取了以下输入：

1. `derived/manual_adjudication_v2/reviewer_input_projection.jsonl`；
2. `derived/manual_adjudication_v2/reviewer_projection_audit.json`；
3. `discover_matrix/docs/protocol/semantic_judge_protocol.md` 第 `1-110` 行。

未读取 canonical decisions、旧 labels/reviews、`review_log`、pane5、任何 unblind mapping、`inventory.json` 或 raw 直连文件；未调用 provider，未修改 frozen raw 或 canonical data。

## Evidence

- 投影文件为 `2642` JSONL rows，SHA-256 为
  `sha256:1d9b879cab647246ad1e35e8be37dc544aa88a09095120f4ab35ea98be05ef82`，与 audit 的
  `projection_sha256` 相同；audit 记录 `provider_calls=0`。
- audit 的声明计数为 `projected_report_count=1783`、`padded_slot_count=859`、`row_count=2642`，满足
  `1783 + 859 = 2642`；两 arm 均为 `1321` rows。
- 以 `(pair_token, round, slot)` 分组得到 `1321` slot groups；每一组恰为 `arm-a` 和 `arm-b` 各一行，没有缺 arm 或重复 arm。两侧同 slot 的 NL 和 PlantUML SHA-256 均一致。
- `462` slot 两侧均有非空 report evidence；`859` slot 恰有一侧三项 report evidence
  (`claim_text`、`reason_text`、`location_text`) 全空，没有双方均空的 slot。这与 padding 声明一致。
- 空 evidence 分布为 `arm-a=50`、`arm-b=809`；非空 evidence 分别为 `1271` 与 `512`。
  这只说明投影保留了冻结输出的真实存在/缺失，不是 semantic label；protocol 第 `104-106` 行要求 padding 不成为 finding、分母或 semantic label。
- 所有投影行只有共同 allowlist 字段：`arm_token`、`pair_token`、`review_key`、`round`、`slot`、
  `author_source`、`report_evidence`、`redactions_applied`、`projection_sha256`、`schema`。
  `redactions_applied=true` 为 `2642/2642`。
- 递归 key scan 没有 audit 禁止的 expected/label/provider/model/W2 字段；文本 scan 发现 `0` 条 raw path、JSON pointer、provider/model identifier、W0/W1/W2、predicate、receipt、terminal-result、
  `VALID_KNOWN`、`VALID_NOVEL`、`INVALID`、relation 或 D/A label 值。此项符合 protocol 第 `101-105` 行对 expected、旧 Judge、W、D/A、validity、relation 和 K/N/I 不进入投影的要求。
- `pair_token` 全部符合 `pair-[0-9a-f]{20}`；report evidence 的 `review_key` 使用
  `report-[0-9a-f]{20}`，空 evidence 使用 `slot-[0-9a-f]{20}`。在未读任何解盲映射的前提下，
  token 本身不含 arm 名或原始 pair 数字。

## Findings

### FAIR-20-001 [I] `location_text` exposes a reversible arm/pair signal

**路径**：`derived/manual_adjudication_v2/reviewer_input_projection.jsonl`，字段
`report_evidence.location_text`；例如 `arm-a`、`pair-243e337b9f5a065def28`、round `1`、slot `0`
的 `location_text` 包含 `state:llms_emp_feedback_final_0000:line:2`。

**Reason**：`69` 条投影行（`23` 个 opaque pair token）含
`llms_emp_feedback_final_####`；计数全部归属 `arm-a`，`arm-b=0`。protocol 第 `93-99` 行的
映射表将 `llms_emp_feedback_final_<pair>` 明确关联 v60/current，而第 `104-105` 行又规定
`element_refs` 不进入盲审输入。该可观察命名既能把 opaque pair token 复原为原始四位 pair
标识，也能将 `arm-a` 与 current 一侧关联，破坏 raw-first blind 的 side secrecy。

**Evidence / command**：

```bash
jq -s 'map({arm:.arm_token,pair:.pair_token,location:(.report_evidence.location_text // "")})
  | {count:([.[] | select(.location|test("llms_emp_feedback_final_[0-9]{4}"))]|length),
     by_arm:([.[] | select(.location|test("llms_emp_feedback_final_[0-9]{4}"))|.arm]
       | group_by(.) | map({arm:.[0],count:length}))}' \
  derived/manual_adjudication_v2/reviewer_input_projection.jsonl
# count=69; by_arm=[{arm:"arm-a",count:69}]
```

**Disposition**：`fix-required`。投影生成应将 source-specific root token 从
`location_text` 去除或替换为 arm-neutral opaque locus token，同时保留状态/transition/event 的
可审计定位信息；修复后必须重建投影 hash/audit，并让独立 reviewer 在不读取旧 proposal 的条件下
重新复核。

### FAIR-20-002 [M] padding denominator rule is declared, not observable in raw-first input

**路径**：`reviewer_projection_audit.json` 的 `policy.projection_shape` 和
`padded_slot_count`；protocol 第 `104-106` 行。

**Reason**：输入层可确认 `859` 个空 evidence padding slot 补齐成相同的 `1321` rows/arm，且
policy 明说 padding 不产生 semantic decision。投影特意不携带 scoring/denominator 字段，因此
在本 reviewer 被限制的输入范围内，无法独立证明后续聚合没有把 padding 计入分母。

**Disposition**：`accepted-with-scope`。这不是对当前 input projection 的失败；其下游执行应由
不读取本 proposal 的 numeric/artifact reviewer 从 canonical recompute 独立验证。

## Result

投影的共同 allowlist、slot 成对、author-source 对称、expected/label/provider/W2/raw-path 去除和
文件 hash 闭合均通过；但 FAIR-20-001 是影响 blind fairness 的 I 级泄漏，因此本 review 为
`FAIL`。无修复 commit，targeted rereview 尚未通过。

## Post-fix targeted rereview

- Date: `2026-08-29` (Asia/Shanghai)
- Reviewer identity: independent leakage/fairness subagent, proposal-only. This is not a final human adjudication and makes no canonical-data change.
- Declared inputs: only `derived/manual_adjudication_v2/reviewer_input_projection.jsonl`, `derived/manual_adjudication_v2/reviewer_projection_audit.json`, and `discover_matrix/docs/protocol/semantic_judge_protocol.md` lines 1--110. No raw records, canonical decisions, labels, old reviews, review log, unblind mapping, inventory, or provider were read or used.
- Result: **FAIL**

### Exact evidence

- `sha256sum derived/manual_adjudication_v2/reviewer_input_projection.jsonl` returned `c5c4740293c5e78514016d6211676edfe5e76bd941344a2903662a093a74b68f`, matching `projection_sha256` in the projection audit.
- Projection audit declares `row_count=2642`, `arm-a=1321`, `arm-b=1321`, `projected_report_count=1783`, `padded_slot_count=859`, and `provider_calls=0`.
- A provider-free `jq -s` structural scan found: 2642 rows; 1321 rows per arm; 2642 unique review keys; 1321 `(pair_token, round, slot)` groups; zero malformed arm pairs; zero within-slot NL/PlantUML hash mismatches; 462 slots with no empty report-evidence row; 859 slots with exactly one empty row; and zero slots with two empty rows.
- The same scan found `redactions_applied=true` for 2642/2642 rows, and `location_text` present, string-typed, and exactly empty for 2642/2642 rows. Opaque pair and review-key shape checks also returned zero violations.
- Exact scans returned zero projected expected IDs, relation labels, validity labels, D/A labels, W labels, predicate/receipt/terminal strings, provider/model identifiers, raw paths, or JSON-pointer-like artifact paths. This is consistent with the allowlist and exclusions in `semantic_judge_protocol.md` lines 83--96.
- The protocol states that `claim_text` is normalized prose that must not carry a producer schema, ID, or pointer (line 84), that `location_text` is fixed empty (line 86), and that padding is neither a semantic label nor a denominator member (lines 91--96). This review verifies the projection-layer padding construction only; downstream recomputation is outside the declared input boundary.

### Finding

- **FAIR-20-001 [I] - fix-required.** Producer/pair identity remains in `report_evidence.claim_text` after the location-field repair.
  - **Reason:** `13` claim rows match `llms_emp_feedback_final_[0-9]{4}`; all `13` are in `arm-a`, across `7` opaque pair tokens. No matching string occurs in `reason_text`.
  - **Basis:** a provider-free JSONL scan reports `claim_producer_id_rows=13`, `reason_producer_id_rows=0`, and `by_arm=[{arm:"arm-a",count:13}]`. Example projected claim: `llms_emp_feedback_final_0000 initial entry to HumanDrivingMode is conditional`.
  - **Protocol impact:** this violates the line-84 prohibition on producer schema/ID/pointer in `claim_text`, makes the arm distinguishable, and therefore leaves raw-first reviewer input asymmetric even though every `location_text` field is empty.
  - **Disposition:** repair the projection normalization to remove producer/pair identifiers from claim prose, rebuild the projection/audit, and repeat this restricted review. No repair commit is available to this read-only reviewer.

### Targeted rereview disposition

`FAIR-20-001 = FAIL / fix-required`. Structural slot symmetry, source-hash symmetry, location removal, forbidden metadata exclusion, no-provider declaration, and projection-layer padding construction pass. The residual claim-text identity leak prevents an overall PASS.
