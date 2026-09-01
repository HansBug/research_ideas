# Predicate gold v1 annotation guide

This guide is the operational companion to `predicate_gold_protocol.md`. It
explains how a reviewer handles one pair batch. The protocol owns semantics;
the canonical JSON Schema owns field shape.

## Before review

1. Verify the pair packet hash against `review/input_packets/manifest.json`.
2. Read the complete numbered NL, author PlantUML, current ledger entry and
   provenance embedded in the packet.
3. Confirm that Track A/B visibility flags are all false for planned mapping,
   v60 actual output, peer conclusions and execution results.
4. Do not search the frozen v60 outputs for a convenient predicate or input.

The packet is a review convenience, not a replacement for its hash-bound
source files. A missing or contradictory packet field is resolved against the
author bytes and ledger provenance and recorded as a conflict.

## Track A: recover O

Track A writes one `TrackAProposalRow` per ledger ID. Fill every
`NormalizedObligation` field with one of:

- a source-backed value and locator;
- a formal-semantics value that follows from the identified model element; or
- an explicit statement that the information is absent and must not be
  invented.

Do not write an executable predicate, expected Boolean, status, or O/P
relation. Track A does not see a property. The canonical `ReviewOpinion`
therefore stores `null` for its `proposed_status` and
`proposed_exactness_relation`.

For D1, state each complete alternative, not merely "ambiguous". An
alternative must identify the changed quantifier, connective, timing,
observable, attribution or obligation and cite the author source that permits
it. Adopted and retained readings remain visible after arbitration.

## Track B: compare P with O

Track B reads the blind packet plus the frozen registry/backend, pyfcstm source
and capability audit. It does not read Track A, v60 actual output or execution
results.

For each credible candidate:

1. Write the complete property expression, including quantifier, scope,
   timing, observable and assumptions.
2. Bind every input to one source pointer and stable native object where one
   exists.
3. Decide `EQUIVALENT`, `O_IMPLIES_P`, `P_IMPLIES_O` or `UNRELATED` before
   execution.
4. List every missing dimension. `semantic_gaps=[]` is allowed only for an
   equivalent candidate.
5. Preserve rejected candidates that are tempting but wrong, especially
   direct-edge, guard-agnostic topology, finite-horizon and named-final-state
   shortcuts.

`UNSUPPORTED_EXACT_CANDIDATE` is used after checking all 19 predicates,
auditable non-short-circuit composites and existing pyfcstm-native evaluation
oracles. It is not justified by a missing predicate ID alone.

An executable proposal is not run until its complete row and proposal hash are
saved. Do not edit that proposal after seeing a verdict. A corrected proposal
gets a new ID/hash and retains the rejected predecessor.

## Execution packet

For a candidate that survives semantic preflight:

1. Create a query bound to the proposal hash, exact defective artifact hash,
   typed inputs and pre-registered expected Boolean `false`.
2. Freeze a positive-control artifact and provenance before same-issue
   execution. Its expected Boolean is `true`.
3. Execute only through the evaluation runner and frozen backend, or through a
   physically isolated pyfcstm-native evaluation oracle.
4. For a composite, execute every constituent. Child acceptance values may
   differ; the parent truth function determines the final Boolean.
5. Replay with the saved query and compare terminal state, Boolean,
   counterexample/trace projection, backend identity and artifact bytes.

An error, timeout, unsupported result, invalid input, exception, unknown or
empty result has `verdict=null`. Fix a mechanical problem and issue a new
hash-bound request, or classify the semantic capability as unsupported. Final
canonical data cannot contain `BLOCKED_EXECUTION`.

## Track C: relation and execution review

Track C intentionally sees the frozen A/B proposals. If execution occurred, it
also sees every query, receipt, control, counterexample and replay artifact. It
still cannot see v60 actual predicate/input output.

Check in this order:

1. Is the accepted O supported, including every retained D1 reading?
2. Does O actually imply P? Does P imply O? Do not infer either from `false`.
3. Are all exact names, carriers, states, events, variables, domains, bounds
   and scopes source-bound?
4. Did the defective run finish with Boolean `false`?
5. Is the control a source-justified true case fixed before the defective
   result, and does it avoid empty inventories or unreachable antecedents?
6. Does replay match the semantic projection and exact artifact/code bytes?

For a proposal that fails steps 1-3, execution is not required to establish
unsupported status. If a rejected property was already executed, retain its
receipts as evidence about P and explicitly state that they do not establish
O. The pilot `EIS-0000-01/02` records this boundary.

## Pane5 arbitration

Pane5 reads the author source, Track A/B/C rows and all applicable receipts.
Every disagreement becomes a `ConflictRecord` with complete positions,
additional source refs and an evidence-based resolution. Do not resolve a
conflict by vote or confidence score.

The arbitration fixes:

- the adopted O and retained sensitivity;
- the final relation for the selected P or nearest rejected proxy;
- final status and mode;
- whether any executed receipt is exact/proxy evidence or only provenance for
  a rejected candidate;
- the capability gap and minimum future semantic capability for unsupported
  rows.

Canonical candidates preserve rejected alternatives. When Track C corrects
Track B's implication direction, the canonical candidate stores the corrected
relation and reason; the original Track B row remains immutable in `review/`.

## Batch validation

Each finished batch must pass:

- row and batch payload hashes;
- exact pair/ledger coverage with no duplicates;
- stable `SourceRef` file hashes and pointers/lines;
- exactly four distinct reviewer IDs, one each for Track A, Track B, Track C
  and the fourth high-risk review, with their visibility rules;
- arbitration status/relation equality with canonical fields;
- false/control/replay closure for exact or executed-proxy status;
- no exact property on unsupported rows;
- schema validation after serialization and reload.

Only after all 145 rows close are canonical JSON, TSV, summary, report,
expected-vs-actual matrix and manifest generated. The final release validator
recomputes all mirrors from JSON and checks the method tree contains no gold
path or import.
