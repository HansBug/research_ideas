# Predicate gold v1 academic horizontal re-review v2

Reviewer ID: `codex:predicate-gold-v1-academic-horizontal-r2`

Review scope: modified `predicate_gold_protocol.md` and `academic_claim_to_source_matrix.json` v1.2.0 only, with v1 horizontal review retained as the historical baseline. No item-level review, v60 actual output, execution verdict, method, Judge, provider, or execution pipeline was read or invoked.

## Inputs

| Input | SHA-256 |
| --- | --- |
| `predicate_gold_protocol.md` | `6d91c5d8d439b398764529f955da44a7adc1569becfb32e132479902863dab57` |
| `academic_claim_to_source_matrix.json` v1.2.0 | `c3c89f25e22edff64fad331e628d6a1679780518593d64d17b63c98e707d9a98` |
| Historical `academic_review_v1.json` | `60562450b294fff233541912f1603b1fae9dc8b06b415d67875e32004944cbc6` |
| Historical `academic_review_v1.md` | `407355fa77bcc7401db3855e6007498a0eff5124efee3d0ac116ae810695d305` |

The v1 content hash remains `0ab6f037dad25aa272e4b6f98ff904373a240c8a8f6f36829698a37004b9165f`; its historical verdict remains `FAIL`.

## Verdict

`PASS_WITH_LIMITATIONS`

All 12 named literature claims pass. Claim IDs are unique; the 10 required-topic groups cover exactly the same 12 claims; the protocol source table and matrix agree; all rows contain a primary/formal source, DOI or stable URL, locator, verified quotation, non-support boundary, and project-operationalization boundary. There are zero `NEEDS_SOURCE` rows and zero high-severity failures.

The limitation is correctly scoped: three-track review, pane5, implication labels, status taxonomy, and positive-control construction remain project-engineered controls. Their independent effectiveness is not measured or claimed. That limitation does not turn named literature coverage into FAIL.

## Claim review

| Claim | Verdict | Locator and quote result |
| --- | --- | --- |
| `PG-REQ-DWYER-1999` | PASS | IEEE Xplore Abstract; pattern-based presentation, codification, and reuse quote verified; no body-page claim |
| `PG-REQ-FRET-2020` | PASS | Sections 1-3, PDF pp. 1-5; six-field quote and Sections 2-3 formula/trace semantics verified |
| `PG-ORACLE-BARR-2015` | PASS | Section 2.3, Definitions 2.6-2.8, printed p. 510; ground-truth and implication directions verified |
| `PG-VACUITY-BEER-2001` | PASS | IBM Research Abstract; unsatisfiable-precondition vacuity quote verified; no page inferred |
| `PG-MBT-TRETMANS-2008` | PASS | Abstract and Section 1, pp. 1-2; model-validity and testing-incompleteness text verified |
| `PG-UML-INITIAL-2017` | PASS | UML 2.5.1 clauses 14.2.3.2, 14.2.3.7, 14.5.6.7; pp. 307, 312, 350; all structural/variation-point boundaries verified |
| `PG-UML-RTC-2017` | PASS | Clause 14.2.3.9.1, pp. 316-317; one-at-a-time dispatch, stable RTC, discard, and orthogonal consumption verified |
| `PG-UML-COMPLETION-2017` | PASS | Clauses 14.2.3.2, 14.2.3.6-7, 14.2.3.9.1, 14.5.2.1/5; pp. 307, 312-313, 316, 346; four stored quotes and adjacent no-exit/abort text verified |
| `PG-REFINEMENT-ABADI-LAMPORT-1991` | PASS | SRC Report 29, Section 2.4, printed p. 11/PDF p. 17; corrected `iff` quote verified |
| `PG-TRACE-HAREL-NAAMAD-1996` | PASS | Section 2, pp. 298-299; run/status/step and environmental-stimulus semantics verified |
| `PG-BMC-BIERE-1999` | PASS | Sections 1 and 6, pp. 194/205; explicit k and no-completeness-bound limitation verified |
| `PG-CEX-CLARKE-2000` | PASS | Section 1, pp. 154-155; spurious abstract counterexample/concrete trace boundary verified |

## V1 closure

| V1 finding | Status | Closure evidence |
| --- | --- | --- |
| `H-ACADEMIC-001` project controls incorrectly gated literature coverage | RESOLVED | Matrix now separates named source coverage, operationalization disclosure, and validation; protocol explicitly disclaims measured effectiveness and ground-truth recovery |
| `H-ACADEMIC-002` UML completion/termination row missing | RESOLVED | `PG-UML-COMPLETION-2017` supplies exact normative locators, quotes, bounded claims, and a pyfcstm non-equivalence boundary |
| `H-ACADEMIC-003` Abadi locator/quote false | RESOLVED | Corrected to Section 2.4, printed p. 11/PDF p. 17, with source wording `iff` |

## Overall logic

The `PASS_WITH_LIMITATIONS` result is coherent:

1. `named_source_coverage=PASS`: all 12 bounded claims pass the primary-source gate.
2. `project_operationalization_disclosure=PASS`: controls are explicitly identified as project choices and are not attributed to cited sources.
3. `operationalization_validation=NOT_CLAIMED`: no measured-effectiveness, guaranteed-error-detection, or ground-truth-recovery claim is made.
4. The lack of an independent effectiveness study remains a method limitation, not a citation failure.

No high-severity FAIL remains.

## Non-blocking note

For even more direct support of the sentence about an ordinary State with no outgoing Transition, a later matrix revision may add UML clause 14.2.3.3, p. 307: ordinary State and FinalState are stable Vertices, and a Vertex may be the source/target of any number of Transitions. The current FinalState special-kind and metamodel-constraint evidence is sufficient for PASS. This note does not affect release or canonical item data.

Review content hash: `4228d4290171fda57b9ebc597b327719c6576487e725d5dcd553f332a43fa179` (SHA-256 over canonical JSON after deleting `review_hash.value`).
