# X1v2 baseline non-K v3 protocol freeze

Protocol ID: `issue-189-195-baseline-ni-v3`

This layer re-reviews only the frozen X1v2 baseline reports whose v2 category
was `N` or `I`. The 279 frozen `K` reports are copied into the combined view
without changing their label, evidence, relation rows, hit mapping, or raw
hash. No method, Judge, provider, predicate, prompt, route, or raw artifact is
rerun or edited.

## Decision order

Every report is read in this order:

`author-source fact -> D/A -> validity -> all 145 expected relations -> K/N/I`

The source of truth is the report's full raw `issue`, `where`, `reason`, and
`basis`, the complete pair NL, the complete author PlantUML, and the full
ledger. FCSTM/IR/lowering may corroborate a reading but cannot substitute for
author-source attribution. The raw report pointer and file SHA-256 are retained
for every decision.

## D/A

- `D2`: the burden-bearing author-source fact exists and a specific violated
  obligation is established without a surviving competent counter-reading.
- `D1`: the fact exists and two concrete, source-compatible competent readings
  of the obligation/carrier remain viable. “The reviewer was unsure” is not D1.
- `D0`: the burden-bearing fact exists, but no author obligation is violated or
  the author's design interpretation is justified. It is not an evidence bin.
- `A0`: the burden-bearing author-source fact is false or misattributed.
  Baseline uses `FALSE_POSITIVE`; `NOT_A_DEFECT_CLAIM` is disallowed in this
  layer unless a pane5 exception is explicitly recorded with evidence.

Fact-established/no-duty is `D0`; fact-refuted is `A0`. W, predicate support,
Judge output, missing ledger membership, and backend capability cannot choose
between these classes. There is no `OUT_OF_SCOPE`, `UNKNOWN`, or
`PENDING_REVIEW` final value.

## W and relations

`W0/W1/W2` is an independent evidence axis. W2 requires the baseline finding's
own executable object, terminal receipt, exact artifact hash, and terminal
result. A later Judge or reviewer cannot upgrade W.

For each report, all 145 ledger IDs receive exactly one relation:

- `FULL_MATCH`: the same expected defect instance and obligation;
- `PARTIAL_MATCH`: the same broader obligation/family is supported, but the
  expected instance is not identical;
- `NO_MATCH`: no admissible same-pair relation.

Closure is mechanical: D2/D1 plus any FULL or PARTIAL is `VALID_KNOWN/K`; D2/D1
plus 145 NO rows is `VALID_NOVEL/N`; D0/A0 must have 145 NO rows and is
`INVALID/I`. PARTIAL does not count as the main FULL hit. Expected hits are
deduplicated only at expected-ID level.

## Independent review and adjudication

Track A and Track B are blind raw-first proposals. They must each retain the
full report text, source refs/hashes, D/A proposal, dense relation proposal,
reason, basis, and reviewer identity. The proposal cannot set human
confirmation. Pane5 reads the same evidence after both submissions, resolves
all disagreements, and is the only final adjudicator. A final row is not
published without two distinct independent subagent proposals and pane5
confirmation; high-risk disagreements are explicitly listed in the arbitration
log.

The materializer carries a small, explicit pane5 correction table for
cross-instance positives discovered during source reread.  It resets omitted
ledger IDs to `NO_MATCH`, downgrades family-only matches to `PARTIAL_MATCH`,
and records two source-refuted candidate claims as `D0`/`A0`.  This table is
provider-free, versioned in `build_pane5_register_v3.py`, and applied before
the canonical rebuild; it is intentionally not inferred from a majority vote.

## N grouping

Only final N reports may enter substantive groups. Two reports can merge only
when they are on the same side and pair, name the same normative obligation or
formal property, point to the same source locus or an inseparable modeling
cause, require the same repair-relevant root cause/intent, and lose no
diagnostic information when combined. Cross-round merge is allowed; cross-pair
and cross-side merge is forbidden. Conservative singleton groups are retained
when this evidence is not established and are not advertised as proof that
every report is a distinct defect.

I rows are invalid-claim diagnostic clusters, never substantive defects and
never N groups. Any I clustering is reported separately from precision's true
defect unit.

This operationalization is informed by, but is not claimed as the verbatim
definition of, Ahmed et al. (MCeT, MODELS 2025,
DOI `10.1109/MODELS67397.2025.00014`), Okun, Delaitre & Black (NIST SP
500-297, DOI `10.6028/NIST.SP.500-297`), Pearson et al. (ICSE 2017,
DOI `10.1109/ICSE.2017.62`), Martinez et al. (EMSE 2017,
DOI `10.1007/s10664-016-9470-4`), Porter, Votta & Basili (TSE 1995,
DOI `10.1109/32.391380`), and Klees et al. (CCS 2018,
DOI `10.1145/3243734.3243804`). Those sources motivate equivalent-root-cause,
relatedness, multi-statement fault granularity, semantic/repair equivalence,
true-fault/false-positive distinction, and distinct-bug evaluation units.
The same-pair/same-obligation/same-source-root/same-repair-intent rule is this
project's explicit operationalization, not a claim that one cited paper
proposed the entire protocol.

## Publication units

The combined baseline has 512 raw report rows. Report precision uses raw report
rows. Ledger/group precision uses unique FULL-hit expected IDs plus substantive
N groups plus separately named invalid diagnostic clusters; a sensitivity value
leaves I ungrouped. L2 ledger precision is `not_applicable` because N/I groups
have no natural L2 attribution. `hit@1` is deduplicated expected-round-unit
coverage across all three rounds (`145 x 3` denominator as in the archive),
`hit@3` is an expected ID hit in any of three rounds, and `hit@all` requires
all three rounds. W2-on-hits and
W2/all-expected are separate metrics. Predicate usage is `not_applicable` for
this baseline, not zero.

Every number in the summary/report is generated by
`scripts/evaluation/recompute_baseline_v3_summary.py` from canonical JSON.
