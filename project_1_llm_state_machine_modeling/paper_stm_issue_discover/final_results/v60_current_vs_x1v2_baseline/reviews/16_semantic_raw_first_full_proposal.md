# Semantic raw-first full proposal

## Status

- Role: `subagent:semantic-raw-first-full`
- Review status: `PROPOSAL`
- This file is an independent semantic proposal, not a canonical decision and
  not human adjudication.
- Blind boundary: before this proposal is submitted, only frozen raw method
  records/reports, author NL and PlantUML source artifacts, source hashes, and
  the semantic protocol are admissible. Canonical decisions, old reference
  labels, primary decisions, and other reviewer conclusions are prohibited.
- Provider calls: `0`.
- Method/Judge/rejudge/experiment calls: `0`.
- Frozen raw and canonical files are not modified by this review.

## Intended coverage

The raw inventory contains `1271` v60/current report records from `162` method
cells and `512` X1v2 baseline finding records from `162` method cells. This
proposal is being built from those raw records and the corresponding author
source artifacts. Every row is retained by stable raw path plus JSON pointer;
semantic labels are only added after the source claim and cited source locus
have been read. A row without sufficient source evidence remains explicitly
`EVIDENCE_GAP` in this proposal and is not silently converted into a final
`D0`, `A0`, `INVALID`, or `NO_MATCH` decision.

The proposal does not use raw method self-reported `d_level`,
`semantic_adjudication`, Judge output, expected-ledger labels, or historical
audit labels as final truth. Raw fields may be cited as the report's claim and
location, but the candidate fact/D-A/W assessment must be justified against
the author source and this protocol.

## Protocol boundary used for the blind read

- Author-source fact is checked before obligation: `D2`, `D1`, `D0`, or `A0`.
- `A0` is only `FALSE_POSITIVE` or current-only
  `NOT_A_DEFECT_CLAIM`; baseline cannot use the latter subtype.
- `W0/W1/W2` is an independent evidence axis. `W2` requires an exact artifact,
  typed executable input, terminal true/false result, receipt, and artifact
  hash on the evaluated artifact.
- Validity and expected relation are separate axes. Positive relations are
  withheld in the blind proposal unless they can be established from an
  admissible source-only obligation; no final K/N/I is assigned here.
- This proposal must not be interpreted as a replacement for the human
  adjudication session.

## Raw inventory evidence

Provider-free inventory commands and their outputs:

```bash
find final_results/v60_current_vs_x1v2_baseline/raw/v60_current/method/method \
  -mindepth 2 -maxdepth 2 -name 'round-*.json' | wc -l
# 162

find final_results/v60_current_vs_x1v2_baseline/raw/x1v2_baseline/method \
  -mindepth 3 -maxdepth 3 -name record.json | wc -l
# 162

# Raw report counts, obtained by enumerating the arrays rather than hardcoding:
# v60/current = 1271; X1v2 baseline = 512.
```

The row-level raw/source evidence index is generated from frozen inputs only
and is not a canonical result. Its command and digest are recorded here before
unblind:

- current raw index: `/tmp/paper1_v60_raw_semantic_index.tsv`, `1271` rows,
  SHA-256 `2814ea75e867d3a2b0c221d8162f085fb425f8d502883e0397dfc6ff704ae074`.
- baseline raw index: `/tmp/paper1_x1v2_raw_semantic_index.tsv`, `512` rows,
  SHA-256 `8e286e1561f8558b84fa44ddaf007f5c45dc7ed788fd547fdbf0110c5cc56b34`.
- source closure inventory: `108` NL/PlantUML files under
  `reference/x1v2_input_closure/pairs/`.

## Blind submission attestation

At the point this proposal is persisted, no canonical FINAL, primary decision,
old reference label, or other reviewer conclusion has been read for this
review. The later unblind comparison must record a separate timestamp and hash;
it may not rewrite this blind proposal's evidence or labels.

The full row-level proposal supplement retains those identity fields for all
`1783` raw records. Source-specific semantic candidates were actually read for
`28/1783` records: `16` current and `12` baseline. Each of those 28 records has
an independent candidate fact/D-A/W assessment, a dedicated reason and basis,
and source line references. The remaining `1755` records stay explicitly
`READ_SOURCE_PENDING_SEMANTIC` with an evidence gap. Missing evidence is never
converted into a final label.

All 28 candidate relation axes remain `WITHHELD_BLIND`; no expected-ledger
label is submitted in this proposal. The per-record blind submission hashes
and batch hash are stored in the JSON. The JSON was persisted before any
canonical/reference unblind read.

### Source-read candidate coverage

| side | stable IDs | candidate D/A | W | source evidence read |
|---|---|---|---|---|
| current | `v60:0014:r1:issue:0`, `v60:0014:r1:issue:1`, `v60:0014:r1:issue:4`, `v60:0014:r3:issue:1` | `D2`, `D1`, `D0`, `A0/NOT_A_DEFECT_CLAIM` | `W1` each | `0014/nl.txt:1,8-10`; `0014/plantuml.puml:2-4,7,14-17` |
| current | `v60:0023:r1:issue:0`, `v60:0023:r1:issue:5`, `v60:0023:r1:issue:6` | `D1`, `D2`, `D2` | `W1` each | `0023/nl.txt:1-5`; `0023/plantuml.puml:3-11` |
| current | `v60:0029:r1:issue:5`, `v60:0029:r1:issue:9`, `v60:0029:r1:issue:28`, `v60:0029:r1:issue:30` | `D2`, `D1`, `D2`, `D2` | `W1` each | `0029/nl.txt:1-6`; `0029/plantuml.puml:2-17,40-44` |
| current | `v60:0049:r2:issue:0`, `v60:0049:r2:issue:6`, `v60:0049:r2:issue:30` | `D2`, `D2`, `A0/FALSE_POSITIVE` | `W2`, `W1`, `W2` | `0049/nl.txt:1-6`; `0049/plantuml.puml:2-16,33-43` |
| current | `v60:0053:r1:issue:0`, `v60:0053:r1:issue:1` | `D2`, `D2` | `W2` each | `0053/nl.txt:2-5`; `0053/plantuml.puml:3-18` |
| baseline | `x1v2:0014:r1:issue:0`, `x1v2:0014:r1:issue:2`, `x1v2:0014:r1:issue:3` | `D1`, `D1`, `D2` | `W1` each | `0014/nl.txt:2-10`; `0014/plantuml.puml:7,14-27` |
| baseline | `x1v2:0023:r1:issue:0`, `x1v2:0023:r1:issue:1` | `D2`, `D2` | `W1` each | `0023/nl.txt:1-5`; `0023/plantuml.puml:3-11` |
| baseline | `x1v2:0029:r1:issue:1`, `x1v2:0029:r1:issue:2`, `x1v2:0029:r1:issue:6` | `D2`, `D2`, `D0` | `W1` each | `0029/nl.txt:3-6,12-13`; `0029/plantuml.puml:10-17,31-34` |
| baseline | `x1v2:0049:r1:issue:0`, `x1v2:0049:r1:issue:2` | `D2`, `A0/FALSE_POSITIVE` | `W1` each | `0049/nl.txt:7-10`; `0049/plantuml.puml:19-30` |
| baseline | `x1v2:0053:r1:issue:0`, `x1v2:0053:r1:issue:1` | `D0`, `D2` | `W1` each | `0053/nl.txt:1-5`; `0053/plantuml.puml:5-18` |

## Shuorenhua audit

Scene: `docs/status`; level: `minimal`; scope: `audit-only`.

Protected spans retained: `1271`, `512`, `162`, `PROPOSAL`, `D2/D1/D0/A0`,
`W0/W1/W2`, `FULL_MATCH/PARTIAL_MATCH/NO_MATCH`, `VALID_KNOWN/VALID_NOVEL/INVALID`,
paths, JSON pointers, hashes, and command names. Pass 1 checked that no
proposal/inventory language is presented as FINAL. Pass 2 will occur after the
raw-first proposal body is complete and will only remove residual narrator or
template language without changing technical spans.

Pass 1 checked protected spans and the distinction between raw inventory,
source-read proposal, and final adjudication. Pass 2 removed residual narrator
phrasing while preserving every path, pointer, hash, count, enum, and coverage
qualification.

submitted_at: `2026-08-29T09:48:47Z`
batch_submission_hash: `sha256:3f8e0b1022b3436ea15ffe082d6ba19e2cd8e97b10741b9dfb28022df59db63e`
proposal_json_sha256: `sha256:b7ebe7109109b648223a44bd38bcb01a6ad6471d246c084c13bda03f5b01d48a`
