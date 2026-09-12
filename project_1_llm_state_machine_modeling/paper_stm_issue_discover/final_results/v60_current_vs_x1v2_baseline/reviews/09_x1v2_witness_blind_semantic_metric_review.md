# Independent X1v2 Blind Witness Semantic And Metric Review

## Scope And Independence

This is an independent, provider-free review of the accepted v2 X1v2 witness
audit in this archive. I did not participate in the primary or secondary
labelling. I made no provider calls and changed no source data, labels, Judge
outputs, reports, or code. The superseded v1 judge-exposed material was
excluded from this review.

The review covers the v2 review packet and its 12 batches, the issue #189 W
definition in `derived/x1v2_witness_level_audit.json`, all 512 frozen X1v2
findings with their source record/NL/PlantUML references, the published W0/W1/W2
labels, and the 162 selected archived `PairJudgeResults` files.

## Method

1. I inspected the packet and every batch for non-null Judge association data,
   including Judge result paths and hashes, validity, expected-relation data,
   and ledger identifiers, before using post-review Judge data for metric
   aggregation.
2. I checked all 512 packet work items against their cited raw method record,
   NL, and PlantUML files. This included recomputing 1,536 SHA-256 values
   (record, NL, and PlantUML for every item) and comparing the copied finding
   fields with the raw `parsed_output.issues[index]` source.
3. I applied the issue #189 definition independently: W0 requires no checkable
   concrete carrier/path; W1 requires a specifically located state,
   transition, guard, action, missing edge, model fragment, or finite path;
   W2 additionally requires an original-X1v2 executable object, terminal
   evaluation receipt, exact evaluated-artifact hash, and terminal result.
   Later Judge facts were not used to create W2 evidence.
4. After the semantic assessment, I recomputed the requested metrics directly
   from the archived selected `PairJudgeResults`. `FULL` uses
   `expected_outcomes[].full_report_ids` only; `partial_report_ids` were not
   used to raise a FULL-hit witness level. L2 is read from
   `reference/ledger.json` item field `L`.

## Blind-Packet Check

The v2 packet has 512 work items; the batches contain 43 items in batches
00--07 and 42 in batches 08--11, totaling 512. Every packet/batch work item
has `judge_association: null`. There are zero non-null Judge result paths,
Judge-result hashes, validity values, expected-relation values, or full/partial
ledger-ID lists. Thus the packet/batches pass the no-Judge-disclosure check.

The archive does retain source-integrity SHA-256 values: one raw-record, one
NL, and one PlantUML hash per item. These are not Judge hashes and are needed
to identify the frozen source inputs. Consequently, the check passes when
“hashes” means Judge hashes; a literal rule forbidding hashes of any kind would
not pass. The archive wording should distinguish those two meanings.

## Semantic Witness Assessment

The published final audit contains 512 W1 labels, zero W0 labels, zero W2
labels, and a non-empty final concrete-location list for every item. All 512
final locations equal the corresponding packet `where` value. All 1,536
referenced source hashes matched their on-disk files. The copied issue and
reason fields match all 512 raw source findings. The copied `where` field
matches 511/512; `0050:r3:0050:r3:baseline_issue_1` changes three source
linefeeds into literal `\\n` text. Its transition remains identifiable, so
this serialization defect does not change its W1 assessment.

For 510 items, the location contains an explicit machine identifier, transition
notation, or code-form carrier. I directly reviewed the two remaining
Chinese-only descriptions against their cited NL and PlantUML:

| Audit key | Independent result | Reason |
| --- | --- | --- |
| `0031:r2:0031:r2:baseline_issue_2` | W1 | “brake-caliper clamping-state feedback return path” is concretely anchored by `ClampingState --> InitialState : Transition Missing Feedback` and the NL feedback-return requirement. |
| `0036:r1:0036:r1:baseline_issue_4` | **W0, not published W1** | The finding and `where` say only “the overall state machine, especially termination/completion modelling.” They name neither a state, transition, guard, action, endpoint, bounded model fragment, nor finite path. `TargetSearch` occurs in the NL/PlantUML, but the finding does not localize the asserted missing completion mechanism to it. Whole-model scope is not a checkable carrier under issue #189. |

Therefore, the assertion that all 512 published W1 labels have finding-specific
concrete localization does **not** hold. The independently supported finding
distribution is `W0/W1/W2 = 1/511/0`, not `0/512/0`.

There are no W2 candidates. Across all 162 original X1v2 method records, the
top-level data comprise generation metadata, inputs, prompts, usage, failures,
and parsed output; there is no executable-object, evaluation-receipt,
evaluated-artifact, runtime, or terminal-result field. The final audit also has
null executable object, receipt, evaluated-artifact hash, and terminal result
for all 512 items. Later Judge results were considered only in the subsequent
metric computation, never as X1v2 W2 evidence.

## Independent Metric Recomputation

The following results use the published final labels, so they test the archive's
claimed metric values exactly. All 162 selected PairJudgeResults were read; all
FULL report IDs resolved to a published witness label.

| Metric | Recomputed result | Result |
| --- | ---: | --- |
| Expected rows | 435 | Pass |
| FULL rows | 211 | Pass |
| FULL-only maximum W (W0/W1/W2) | 0/211/0 | Pass |
| L2 FULL-only maximum W (W0/W1/W2) | 0/46/0 | Pass |
| W2 / all expected rows | 0/435 | Pass |
| Round 1 W0/W1/W2 | 0/173/0 | Pass |
| Round 2 W0/W1/W2 | 0/163/0 | Pass |
| Round 3 W0/W1/W2 | 0/176/0 | Pass |
| `VALID_KNOWN` W0/W1/W2 | 0/276/0 | Pass |
| `VALID_NOVEL` W0/W1/W2 | 0/134/0 | Pass |
| `INVALID` W0/W1/W2 | 0/102/0 | Pass |

The independently identified W0 is `VALID_NOVEL`, round 1, and has no FULL
ledger association. If the semantic correction is applied, the FULL-only,
L2, and W2/all-expected rows above remain unchanged. The finding-level round-1
row becomes `1/172/0`, and the `VALID_NOVEL` cross-tab becomes `1/133/0`.

## Findings And Required Follow-Up

1. **Semantic finding:** `0036:r1:0036:r1:baseline_issue_4` is W0 under the
   archived issue #189 rule, not W1. The accepted v2 semantic distribution and
   its affected round/validity distributions require correction.
2. **Minor packet-fidelity finding:** `0050:r3:0050:r3:baseline_issue_1`
   serializes source linefeeds as literal `\\n` in `where`. This does not alter
   the localization class, but the packet should preserve the source string
   exactly.
3. **Documentation clarity finding:** the source SHA-256 values are present in
   every v2 work item. Documentation should say “no Judge paths or Judge
   hashes,” rather than “no hashes,” unless the source-integrity hashes are
   intentionally removed in a future packet format.

No fixes were applied because the review scope permits only this review file.

## Conclusion And Limitations

**Conclusion: metric pass; semantic acceptance fails.** The requested published
metric counts are reproduced exactly from the selected PairJudgeResults, and
there is no original-run executable witness that could support W2. However,
one of the 512 published W1 labels lacks the concrete localization required by
issue #189. The accepted v2 audit should not be treated as semantically correct
until that W0 correction and its dependent distributions are regenerated.

This review is limited to the frozen archive and a source-based manual
assessment; it does not rerun the original method or Judge. A retrospective
file review can establish that the released packet/batches contain no non-null
Judge data, but cannot prove what information a historical human reviewer may
have accessed outside those files.

## Pane5 Disposition

The semantic finding is accepted. The final v3 audit preserves the two original W1 blind decisions and records a bounded `post_review_correction` for `0036:r1:0036:r1:baseline_issue_4`, with `pane5-main` as adjudicator, this review as the archive-relative independent-review reference, and frozen raw/NL/PlantUML pointers as basis. The final finding-level distribution is `W0/W1/W2 = 1/511/0`; r1 is `1/172/0` and `VALID_NOVEL` is `1/133/0`. The item is not a FULL supporting report, so FULL-only max W remains `0/211/0`, L2 remains `0/46/0`, and `W2/全部 expected` remains `0/435`.

The `0050:r3:0050:r3:baseline_issue_1` packet-fidelity concern was rechecked byte-for-byte. Its raw and packet `issue`/`where`/`finding_reason` strings and their three SHA-256 values are equal; the `\\n` characters are literal bytes already present in the frozen raw source. No packet rewrite was required. The accepted test now asserts this invariant directly.
