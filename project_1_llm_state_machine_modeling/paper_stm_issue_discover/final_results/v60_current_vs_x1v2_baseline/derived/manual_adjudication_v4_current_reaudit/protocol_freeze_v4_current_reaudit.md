# v60/current re-audit v4 protocol freeze

Protocol ID: `issue-189-195-current-reaudit-v4`.

This is a source-first evaluation-layer revalidation. The fixed order is:

`author source and report fact -> D2/D1/D0/A0 -> all expected relations -> K/N/I -> N grouping -> metrics`.

The 1271 current raw reports and 162 method cells are immutable inputs. Current
v2 is retained as the prior pane5-confirmed source-first evidence chain. v4
re-reads its recorded evidence pointers and verifies raw/source/relation
identity; it makes no new semantic inference and no production calls.

## D/A and K/N/I

- `D2`: the burden-bearing author-source fact and a specific violated duty are
  established without a surviving competent source-compatible reading.
- `D1`: the fact is established and two complete, competent,
  source-compatible readings remain viable, with an effect on duty or
  attribution. Reviewer uncertainty alone is not D1.
- `D0`: the fact is established but no source-backed duty is violated or the
  design interpretation is justified.
- `A0`: the claimed fact or attribution does not hold in the complete author
  artifact. `FALSE_POSITIVE` is ordinary; `NOT_A_DEFECT_CLAIM` is only for a
  current method-owned representation/analysis claim that is not an author
  defect claim.

For each report, all 145 ledger IDs are classified. D2/D1 with any FULL or
PARTIAL relation is K; D2/D1 with all NO rows is N; D0/A0 is I with all NO
rows. PARTIAL contributes supported coverage but not the main hit. W and
predicate availability never substitute for these decisions.

The canonical field projection is also closed: D2/D1 require an established
source fact and normative violation; D0 requires an established source fact
with no established violation; A0 requires a refuted source fact and no
established violation. Thus `normative_violation_status=ESTABLISHED` is never
used as a proxy for factual validity, and A0 cannot carry an established duty.

## Grouping and academic boundary

Only final N reports are substantively grouped. A group requires the same
side, pair, normative obligation/property, source locus or inseparable
modeling cause, repair-relevant root cause, and minimum repair intent. Round
may vary; pair and side may not. I clusters are invalid-claim diagnostics, not
distinct defects and not a substantive grouped-precision denominator.

This operationalization is informed by Porter, Votta & Basili (IEEE TSE 1995,
DOI `10.1109/32.391380`), Klees et al. (CCS 2018, DOI
`10.1145/3243734.3243804`), Okun, Delaitre & Black (NIST SP 500-297, DOI
`10.6028/NIST.SP.500-297`), Ahmed et al. (MODELS 2025, DOI
`10.1109/MODELS67397.2025.00014`), Pearson et al. (ICSE 2017, DOI
`10.1109/ICSE.2017.62`), and Martinez et al. (EMSE 2017, DOI
`10.1007/s10664-016-9470-4`). IEEE 1044-2009, Goodenough et al., Barr et
al., Zave & Jackson, Massey et al., and Pollock support the disposition,
oracle, requirements, and alternative-interpretation boundaries. No cited
paper is claimed to define this complete project protocol verbatim.

## Execution boundary

Provider calls, method reruns, Judge reruns, 15x1, 54x3, and experiment input
changes are all zero. Raw, reference, v60/current, method, Judge, predicate
registry, v2, and baseline v3 are not modified. The baseline v3 layer is the
frozen comparison reference; only the combined comparison layer reads it.
