# Predicate gold v1 fourth-review addendum

## Status

This addendum extends the frozen
`paper1.obligation-equivalent-predicate-gold.v1` review contract. It does not
change the obligation, exactness, execution, control, or leakage rules in
`predicate_gold_protocol.md`, whose review-input bytes remain fixed at
`sha256:6d91c5d8d439b398764529f955da44a7adc1569becfb32e132479902863dab57`.

The addendum exists because the final release requires one additional opinion
for every ledger ID. Keeping it separate preserves the hashes already sealed
by Track A, Track B, and Track C.

## Fourth Opinion

After A/B/C are sealed, a fourth reviewer reads the same author NL,
PlantUML/FCSTM, ledger item, property proposal, backend semantics, and, where
applicable, defective receipt, positive control, counterexample, and replay.
The reviewer also sees the sealed A/B/C opinions. Frozen v60 actual
predicate/input output remains hidden.

For each issue, the fourth reviewer independently checks:

1. whether normalized `O` preserves source quantifier, scope, timing, RTC
   semantics, observation, assumptions, and retained `D1` readings;
2. whether the stated `O <=> P`, `O => P`, `P => O`, or unrelated direction is
   justified independently of the Boolean result;
3. whether every typed input is source-provenanced and non-invented;
4. whether completed false, positive control, counterexample, replay, vacuity,
   and contamination checks close for an executed property;
5. whether composite, evaluation-only, bounded, termination, concurrency,
   pseudostate/RTC, proxy, unsupported, and missing-control boundaries remain
   conservative.

Each opinion binds the exact A/B/C row hashes, normalized-obligation hash,
property-proposal hash, and reviewed `SourceRef` records in `input_sha256`.
The opinion payload and batch have separate canonical hashes. The fourth
reviewer must be different from the A, B, and C reviewers for that issue.

## Arbitration And Release

Agreement among reviewers is corroborating evidence, not a vote. Every
disagreement and retained sensitivity remains visible to pane5. Pane5 decides
the final status and implication direction from source and semantic evidence,
then binds all four opinion hashes in the arbitration row.

The active review manifest and canonical annotation require exactly one
Track A, Track B, Track C, and fourth opinion from four distinct reviewer IDs.
`BLOCKED_EXECUTION` remains forbidden. This addendum does not authorize a
method, Judge, provider, or 54x3 rerun and does not allow gold data into method
runtime, prompts, routing, registry, or package data.
