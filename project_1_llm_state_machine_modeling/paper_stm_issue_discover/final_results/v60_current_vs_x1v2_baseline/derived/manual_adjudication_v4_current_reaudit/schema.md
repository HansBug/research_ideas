# Current re-audit v4 schema

The production materializer is
`scripts/evaluation/build_current_reaudit_v4.py`. Its canonical models are
Pydantic models with `extra="forbid"`; every model and field has a semantic
description. The JSON files are canonical data and the TSV files are fixed
column mirrors.

## Decision row

`CanonicalDecision` contains the side, pair, round, stable report ID, raw
method path and JSON pointer, raw SHA-256, source-reference digest, exact raw
claim fields, final reason/basis, source elements, factual and normative
statuses, D/A tier, A0 subtype, all 145 `ExpectedRelation` rows, W and
predicate evidence, K/N/I and validity projections, review chain, arbitration
pointer, confidence, timestamp, and evidence digest.

`ExpectedRelation` has exactly one expected ledger ID, one of
`FULL_MATCH`, `PARTIAL_MATCH`, or `NO_MATCH`, an expected-specific reason and
basis, resolvable source refs, and report-owned field refs. Relation rows are
dense: every decision contains every ID in `reference/ledger.json`.

`ReviewChain` preserves the blind independent proposal hash, primary and
independent reason/basis, blind event sequence, pane5 confirmation, explicit
disagreement text, and final arbitration facts. The independent proposal is
review evidence only; it is not silently promoted to a human label.

## Mechanical invariants

1. `D0` and `A0` require `INVALID/I`, `normative_violation_status=NOT_ESTABLISHED`, and all 145 relations `NO_MATCH`; `A0` additionally requires `factual_status=REFUTED`.
2. `D2` or `D1` plus at least one FULL/PARTIAL requires `VALID_KNOWN/K`.
3. `D2` or `D1` plus 145 NO rows requires `VALID_NOVEL/N`.
4. `A0` requires `FALSE_POSITIVE` or `NOT_A_DEFECT_CLAIM`; the latter is
   current-only and must be source-backed.
5. W0/W1/W2 and predicate binding/contribution markers are independent fields
   and cannot alter D/A, relations, validity, or K/N/I. The retained
   `contribution` Boolean is the legacy `coverage_class=semantic_hit` marker;
   it is not a terminal-false execution count. The summary's 12/19 terminal
   receipt and 8/19 report-bound predicate metrics are distinct-ID counts; the
   row-level 825/1271 and 303/825 ratios are separate diagnostics.
6. Every final-N report appears in exactly one N group; groups never cross
   side or pair. I clusters never enter substantive N group counts.

`current_i_diagnostic_clusters_v4.json` uses Pydantic-described cluster,
source-reference and assertion models. It maps all 291 I reports exactly once
to 189 same-pair diagnostic IDs and structurally marks every ID as
`substantive_defect=false` and `grouped_precision_unit=false`.

## Inventory and review coverage

`inventory_v4.json` is directly generated from
`raw/v60_current/method/method/*/round-*.json`. It records all 162 cell paths,
including cells with zero reports, and all 1271 report pointers. The v2
inventory and decision IDs are a cross-check, not the raw enumeration source.

The current v4 layer has 1271/1271 decision rows, 1271/1271 dense closures,
1271/1271 rows with at least two recorded reviewers, and 1271 pane5
arbitration pointers. The five disagreements are retained rather than hidden.
