# Predicate gold v1 academic horizontal review

Reviewer ID: `codex:predicate-gold-v1-academic-horizontal-r1`

Role: independent Academic horizontal reviewer. I did not participate in Track A/B/C, pane5, or item-level labeling. I did not inspect item-level reviews, v60 actual outputs, or execution verdicts, and did not invoke a method, Judge, provider, or execution pipeline.

Reviewed at: `2026-08-30T22:02:26Z`

## Inputs

| Path | SHA-256 |
| --- | --- |
| `predicate_gold_v1/predicate_gold_protocol.md` | `3762ebf1a108c6e61e565c5e320de388c081f2ae50619863e089e2f680a70a57` |
| `predicate_gold_v1/academic_claim_to_source_matrix.json` | `e28ddaf84c5807190313ecd7903676cc43d478b89ead80b1a1f2a1a33d104896` |
| `predicate_gold_v1/annotation_guide.md` | `69dca2d51f5d76322e3158330cb32c5ff4dff3069ee9b4bd874e95e899dd7c1e` |
| `predicate_gold_v1/predicate_semantics_capability_audit.md` | `977ef848a12595662a7d2934477b276085def7ffc69c6b18c29c24e989903631` |

Repository commit observed: `8f23b639626857de2011812ca955990911472ba6`.

Primary-source checks used original papers, the official OMG standard, publisher or author-institution records, author-hosted primary reports, and institutional-repository copies. Blogs and search-result snippets were not used as evidence.

## Overall verdict

`FAIL`

Ten of the eleven claim rows pass. `PG-REFINEMENT-ABADI-LAMPORT-1991` fails because its recorded section and page locator is wrong, although the underlying claim is supported at the correct location. The protocol also relies on a material UML FinalState/no-outgoing/whole-machine termination distinction that has no claim-to-source row.

The matrix's separate reason for failing overall literature coverage is not sound: three-track review, pane5, positive controls, the four relation labels, and the status taxonomy are explicitly disclosed project operationalizations. The literature need not prescribe those controls verbatim. Their effectiveness may remain an unvalidated project-method limitation, but that fact alone must not turn otherwise bounded primary-source coverage into FAIL.

## Claim results

| Claim | Verdict | Verified evidence | Non-support boundary |
| --- | --- | --- | --- |
| `PG-REQ-DWYER-1999` | PASS | DOI `10.1145/302405.302672`; IEEE Xplore Abstract: "pattern-based approach to the presentation, codification and reuse" | No registry completeness, universal precision order, or item-level O/P result |
| `PG-REQ-FRET-2020` | PASS | CEUR-WS Vol. 2584, Sections 2-3, PDF pp. 2-5: "parsed into six sequential fields"; trace/formula verifier described in Section 3 | No guarantee of unstated intent, corpus completeness, or this review workflow |
| `PG-ORACLE-BARR-2015` | PASS | DOI `10.1109/TSE.2014.2372785`; Section 2.3, Definitions 2.6-2.8, printed p. 510: soundness/completeness are opposite implications | No O/P enum, reviewer-independence, pane5, or ground-truth recovery guarantee |
| `PG-VACUITY-BEER-2001` | PASS | DOI `10.1023/A:1008779610539`; IBM Research Abstract: "trivially valid because the pre-condition ... is not satisfiable" | No validation of repaired-artifact controls or universal vacuity detection |
| `PG-MBT-TRETMANS-2008` | PASS | DOI `10.1007/978-3-540-78917-8_1`; Section 1, p. 2: "If this model is valid ... all these tests are also provably valid" and testing cannot show absence | No equivalence between ioco and project O/P or certification of FCSTM conversion |
| `PG-UML-INITIAL-2017` | PASS | OMG UML 2.5.1, clauses 14.2.3.2/14.2.3.7/14.5.6.7, pp. 307/312/350: at-most-one outgoing, no trigger/guard, and no defined approach without initial | No intended issue-specific initial state or automatic transfer to pyfcstm |
| `PG-UML-RTC-2017` | PASS | OMG UML 2.5.1, clause 14.2.3.9.1, pp. 316-317: events processed "one at a time" and consumed after orthogonal transitions finish | No defined event-pool order or equality with a project receipt field |
| `PG-REFINEMENT-ABADI-LAMPORT-1991` | **FAIL (HIGH)** | DOI `10.1016/0304-3975(91)90224-P`; evidence is in SRC Report 29, **Section 2.4, printed p. 11, PDF p. 17**, not Sections 1.1-1.2 / pp. 1-3; the stored quote also changes source "iff every" to "if every" | One-way behavioral inclusion is not equivalence and does not erase observable, stuttering, timing, fairness, or profile differences |
| `PG-TRACE-HAREL-NAAMAD-1996` | PASS | DOI `10.1145/235321.235322`; Section 2, pp. 298-299: a run is statuses linked by steps under environmental stimuli | STATEMATE semantics do not transfer wholesale to UML/PlantUML/pyfcstm |
| `PG-BMC-BIERE-1999` | PASS | DOI `10.1007/3-540-49059-0_14`; Sections 1 and 6, pp. 194/205: k is maximal counterexample length; without a maximal bound only absence at that k is shown | No arbitrary-k unbounded proof or automatic encoding fidelity |
| `PG-CEX-CLARKE-2000` | PASS | DOI `10.1007/10722167_15`; Section 1, pp. 154-155: an abstract counterexample may be spurious if it lacks an actual concrete trace | Replay alone does not prove O/P equivalence, attribution, or parser fidelity |

## High-severity findings

### H-ACADEMIC-001: project controls are misused as a literature-coverage fail condition

The matrix's `decision_rule.overall_pass`, `ACADEMIC-GAP-001/002`, and `verdict.reason` require separate literature or validation for the exact three-track/pane5/positive-control design before academic coverage can pass. That conflicts with the protocol's correct disclosure at lines 28-32 and 228-232: these are project-engineered controls, not claims that a cited paper prescribed the workflow.

Fix: separate bounded claim provenance from project-method validation. Retain an explicit limitation that control effectiveness is not externally established, and avoid claims that the controls materially improve validity, detect every binding error, or recover ground truth unless validated.

Canonical item impact: **No**. This changes the academic release verdict and method-validity wording, not item predicates or labels.

### H-ACADEMIC-002: UML completion/termination evidence is missing

Protocol lines 65-67, 97-99, and 122-123 distinguish a named leaf, FinalState, a no-outgoing state, and whole-machine `terminated()`, but neither UML claim row covers that boundary.

Add a bounded `PG-UML-TERMINATION-2017` row using OMG UML 2.5.1:

- Clause 14.2.3.3, p. 307: ordinary State and FinalState are stable vertices.
- Clause 14.2.3.6, p. 312: "FinalState is a special kind of State signifying that the enclosing Region has completed."
- Clause 14.2.3.7, pp. 312-313: "Entering a terminate Pseudostate implies that the execution of the StateMachine is terminated immediately."
- Clauses 14.5.2.1/14.5.2.5, p. 346: top-level region completion conditions and FinalState's no-outgoing constraint.

Non-support boundary: OMG does not establish that pyfcstm `terminated()` is equivalent to UML terminate or top-level FinalState completion. That requires a backend mapping certificate.

Canonical item impact: **Potentially yes** for rows whose O or P observes completion/termination. This horizontal review did not inspect rows, so the affected set is unknown.

### H-ACADEMIC-003: Abadi-Lamport locator is false

The claim is substantively supported, but the matrix and protocol table point to the wrong report location. Correct both to SRC Research Report 29, Section 2.4, printed p. 11 (PDF p. 17). The matrix's quote says "if every" while the source says "iff every"; correct that text and keep the journal DOI and report pagination source explicit.

Canonical item impact: **No**. This is a provenance correction; the bounded implication/inclusion use remains supported.

## Boundary conclusions

- There is no cited or project-imposed universal "most precise predicate" definition. The protocol explicitly rejects a fixed `S < G < R < V` ranking. PASS.
- `O <=> P` is clearly disclosed as project operationalization under fixed semantics, scope, observations, and assumptions. The false-proxy direction `O => P`, hence `not P => not O`, is correct. PASS.
- Vacuity support is correctly limited to antecedent failure; a positive control is not treated as literature-proven equivalence evidence. PASS, subject to not claiming universal control effectiveness.
- Bounded counterexample evidence is not promoted to an unbounded proof without an independently justified completeness bound. PASS.
- Concrete replay/counterexample validity is kept separate from O/P equivalence and source attribution. PASS.
- UML initial and RTC claims are proposition-specific and do not claim wholesale semantic equivalence with STATEMATE, ioco/LTS, or FCSTM. PASS.
- The capability audit is an internal source-level contract audit, not a literature-derived family ranking. Academic provenance PASS; backend accuracy was outside scope.

Review content hash: `0ab6f037dad25aa272e4b6f98ff904373a240c8a8f6f36829698a37004b9165f` (SHA-256 over canonical JSON after deleting `review_hash.value`).
