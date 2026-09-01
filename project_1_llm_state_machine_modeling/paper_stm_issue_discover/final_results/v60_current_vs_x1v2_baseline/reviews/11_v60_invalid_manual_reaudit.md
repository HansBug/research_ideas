# v60 INVALID Manual Reaudit

## Outcome

This review audits all 106 reports labelled `INVALID` by the frozen v60
Semantic Judge. The item-level audit is
[11_v60_invalid_manual_reaudit.tsv](11_v60_invalid_manual_reaudit.tsv).

The strict report-core result is:

| Unit | D2 | D1 | D0 | A0 | Total |
| --- | ---: | ---: | ---: | ---: | ---: |
| Reports | 5 | 15 | 10 | 76 | 106 |
| Report clusters | 5 | 15 | 9 | 56 | 85 |

The strict K/N/I correction is `K/N/I = 8/12/86`. Thus 20 frozen INVALID
reports are judged valid under a source-attributed issue #189 reading: eight
match the ledger and twelve are novel. The principal corrections are the
pair-0009 urban-exit report, the pair-0011/0021 signal-failure ambiguity,
pair-0023's zero-behavior PumpControl, three pair-0029 hierarchy/termination
reports, ten free-text-condition versus typed-guard reports in pairs 0039 and
0049, pair-0043 cardinality, and pair-0053 owner-level entry.

## Strict And Moderate Readings

The strict column evaluates the indispensable core of the published report.
It does not repair a false runtime or mechanism claim by substituting a nearby
true statement. A0 has exactly the two issue #189 exits:

| A0 type | Reports | Clusters |
| --- | ---: | ---: |
| `FALSE_POSITIVE` | 52 | 38 |
| `NOT_A_DEFECT_CLAIM` | 24 | 18 |
| Total | 76 | 56 |

The following four labels are explanatory mechanisms, not additional A0
taxonomy values:

| A0 mechanism | Reports | Clusters |
| --- | ---: | ---: |
| `false_source_or_structural_claim` | 17 | 17 |
| `lowering_or_typed_carrier_misattribution` | 24 | 18 |
| `unsupported_or_refuted_runtime_claim` | 33 | 20 |
| `overbroad_representation_claim` | 2 | 1 |
| Total | 76 | 56 |

The moderate column changes a result only when the same report contains an
independently diagnostic author-source facet at the same locus. It recovers
four additional reports in two clusters:

- `0015:r2:issue:9` and `0015:r2:issue:10`: narrow the overbroad "no data-side
  representation" core to missing declared cooking-time/timer variable,
  action, or effect carriers. The result is D1 and known against
  `EIS-0015-01` (the timer-only report is a partial relation).
- `0025:r2:issue:5` and `0025:r3:issue:1`: retain the independently stated
  omission of the NL zero-time condition while rejecting the false runtime
  post-state core. The result is D1 and known against `EIS-0025-01`.

The moderate result is `D2/D1/D0/A0 = 5/19/10/72` and
`K/N/I = 12/12/82`, or 24 valid reports in 22 report clusters. It is a
sensitivity result, not a replacement for the strict result.

## Grouping Rule

Reports are merged only within a pair when they identify the same author-source
locus or owner, property and violation, and repair obligation. Cross-round
rephrasings are merged; different endpoint obligations are not merged merely
because a method mechanism is shared. This produces 85 report clusters.

There is no unique occurrence count hidden behind that number. The ledger
separates the three pair-0023 terminal leaves as `INS-0023-01/02/03`, while its
provenance asks that their shared zero-behavior cause be checked as one group;
the later `INS-0053-02` convention explicitly merges an analogous three-leaf
family. If pair 0023's three leaves and pair 0037's two collision leaves are
split by occurrence, the count is 88. The primary 85 therefore denotes
repair/property-oriented report clusters, not an ontologically unique number
of defects.

## TSV Contract

Every row preserves the frozen label in `frozen_v3_2`, records strict and
moderate D/K/N/I results separately, and carries the official strict A0 type,
an explanatory mechanism, ledger relation, grouping key, reason, basis, and
source locators. Locator prefixes resolve as follows:

- `judge:<report-id>`: the unique `report_outcomes` record with that ID under
  `../raw/v60_current/judge/source_runs/*/pairs/*.json`.
- `method:<pair>/r<round>#<report-id>`: the matching `evidence_records` item in
  `../raw/v60_current/method/method/<pair>/round-<round>.json`.
- `source:<pair>/nl.txt` and `source:<pair>/plantuml.puml`:
  `../../../pipeline/representation/reports/llms_emp_r45_java_60/pairs/<pair>/`.

`K`, `N`, and `I` mean corrected `VALID_KNOWN`, corrected `VALID_NOVEL`, and
retained `INVALID`. `FULL:` and `PARTIAL:` qualify ledger relations. A0 follows
the issue #189 attribution boundary: a fact absent from author source or a
claim about FCSTM/lowering rather than author source cannot convict the authored
model. A construct unsupported by the current backend is not an A0 or scope
exit; it is still adjudicated D2/D1/D0 and only its W level may degrade. D0
records a true author-source fact without a violated obligation; D1 retains a
grounded issue reading and a compatible second reading; D2 has a grounded
violated obligation with no surviving rebuttal.

## Frozen-Result Boundary

This is a retrospective review overlay. It does **not** rewrite or supersede
the published `semantic-judge.two-stage.v3.2` output, whose protocol is
`github-issue-195.d774d9bd3e4c.issue-189-clarification.v3.2`. All 106 rows keep
`frozen_v3_2=I`; raw Judge files, derived aggregates, reports, metrics, prompts,
registries, and publication manifests are unchanged. Any future corrected
metric must opt into this review explicitly and state whether it uses the
strict or moderate column.

## Self-Check

The following checks were run after construction:

- TSV rows: `106` data rows plus one header.
- Column shape: all rows have 16 fields.
- ID closure: exact set equality with the 106 frozen v60 `INVALID` report IDs;
  no missing, extra, or duplicate IDs.
- Strict counts: `D2/D1/D0/A0 = 5/15/10/76` and `K/N/I = 8/12/86`.
- Moderate counts: `D2/D1/D0/A0 = 5/19/10/72` and `K/N/I = 12/12/82`.
- Distinct `group_key` values: `85`.
- Official A0 types: `FALSE_POSITIVE / NOT_A_DEFECT_CLAIM = 52/24`.
- Explanatory A0 mechanism sum: `17 + 24 + 33 + 2 = 76`.

No method, Judge, provider, or model execution was rerun for this audit.
