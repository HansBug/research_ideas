# Academic Targeted Review, Postfix

## Verdict

`FAIL` with one `I` finding. This is a provider-free, read-only
`subagent` proposal. It reviews only the following materials:

- `related_work/provenance/CURRENT_SOURCE_AUDIT.md`;
- `related_work/provenance/predicate_provenance.md`;
- `derived/manual_adjudication_v2/predicate_source_provenance.json`;
- `discover_matrix/docs/protocol/semantic_judge_protocol.md`.

It does not read report decisions, `review_log`, legacy labels, or frozen raw,
and it does not create a human attestation or change a canonical decision.
Provider calls and raw modifications: `0`.

## Evidence Summary

- The provenance JSON has `19` predicate rows and `57` source-provenance
  edges, exactly three per predicate. Every edge has a nonempty catalog ID,
  title, `supports`, and `boundary`; its claim status is
  `mapping_and_boundary_read_from_frozen_catalog`.
- The same `57/57` edges have
  `metadata_status=not_recorded_in_frozen_source_catalog`; all lack
  `bibliography` and `doi_or_stable_link`. All retain an `accessed_at` date.
  The JSON's top-level status is
  `mapping_and_boundary_verified; bibliography_and_full_text_metadata_gap_preserved`.
- `predicate_provenance.md:16-20` and `CURRENT_SOURCE_AUDIT.md:3-9` correctly
  state that mapping/supports/boundary evidence is not complete bibliography,
  DOI, or full-text verification, and prohibit manufacturing metadata from
  titles or paths.
- `semantic_judge_protocol.md:59-74` correctly separates manual v2 as the
  paper's human-supervised publication layer from v3.3 and legacy Judge
  headline material. It says the manual v2 JSON and provider-free recompute,
  not Judge output, are the result source. No issue was found in that boundary
  within the reviewed files.

## Findings

### ACAD-20-001 [I] “All records verified” overstates the recorded verification scope

**Evidence pointers:**

- `related_work/provenance/CURRENT_SOURCE_AUDIT.md:3-9` limits available
  evidence to source-ID mapping plus recorded support/boundary fields and
  explicitly preserves bibliography/full-text metadata gaps.
- `related_work/provenance/CURRENT_SOURCE_AUDIT.md:20` then says “所有记录都已完成核验”,
  without preserving that scope in the same sentence.
- `derived/manual_adjudication_v2/predicate_source_provenance.json#/academic_evidence_status`
  limits the status to mapping/boundary verification with a bibliography and
  full-text metadata gap.
- `derived/manual_adjudication_v2/predicate_source_provenance.json#/rows/*/source_provenance/*/claim_verification_status`
  is `mapping_and_boundary_read_from_frozen_catalog` for `57/57` edges, not
  an independent bibliographic or full-text verification status.
- `derived/manual_adjudication_v2/predicate_source_provenance.json#/rows/*/source_provenance/*/metadata_status`
  is `not_recorded_in_frozen_source_catalog` for `57/57` edges; bibliography
  and DOI/stable-link fields are empty for all `57` edges.

**Reason:** “所有记录都已完成核验” can reasonably be read as a complete
academic-source verification claim, while the available structured evidence
only verifies the frozen catalog's mapping and its recorded support/boundary
text. The preceding disclosure is sound, but the unqualified statement at
line 20 weakens it and invites a stronger claim than the JSON can support.

**Minimal conservative remedy:** replace the unqualified sentence with a
scope-qualified statement, for example: “所有记录均已完成 source-ID、catalog
中 `supports`/`boundary` 字段及其路径的核对；这不是完整书目、DOI 或全文逐字核验，也不推导可靠性等级。” Do not invent citations, DOI, authors, venue, or full-text conclusions. Preserve the existing `null`/gap fields.

**Disposition:** `open; documentation-only repair required`.

**Repair commit:** `not available`.

**Targeted rereview:** `NOT RUN`; recheck this one sentence against the same
JSON status and gap counts after repair.

## Passing Checks

### Bibliography and DOI disclosure: PASS

`CURRENT_SOURCE_AUDIT.md:3-9` and `predicate_provenance.md:16-20` do not
convert missing metadata into citations. Their claims match the JSON: zero
nonempty bibliography fields, zero nonempty DOI/stable-link fields, and
`57/57` explicit metadata-gap statuses. No bibliography was inferred from a
title, path, or source type in this review.

### v3.3 and manual v2 result-source boundary: PASS

`semantic_judge_protocol.md:19-38` identifies `semantic-judge.two-stage.v3.3`
as the implementation/protocol discussion. `semantic_judge_protocol.md:61-74`
then states that the paper's final release is manual v2, that Judge output is
not renamed as manual truth, and that the v3.3 protocol plus old headlines are
historical Judge-tool material rather than the new manual result source. This
is an adequate source-boundary disclosure in the reviewed protocol; it does
not claim that v3.3 generated manual v2 truth.

## Reproduction Commands

All commands are provider-free and read only the four reviewed files.

```bash
ROOT=project_1_llm_state_machine_modeling/paper_stm_issue_discover

jq '{academic_evidence_status, rows:(.rows|length),
  edges:([.rows[].source_provenance[]]|length),
  metadata_statuses:([.rows[].source_provenance[].metadata_status]|group_by(.)|map({status:.[0],count:length})),
  claim_statuses:([.rows[].source_provenance[].claim_verification_status]|group_by(.)|map({status:.[0],count:length})),
  missing_bibliography:([.rows[].source_provenance[]|select((.bibliography//"")=="")]|length),
  missing_doi_or_link:([.rows[].source_provenance[]|select((.doi_or_stable_link//"")=="")]|length),
  missing_accessed_at:([.rows[].source_provenance[]|select((.accessed_at//"")=="")]|length)}' \
  "$ROOT/final_results/v60_current_vs_x1v2_baseline/derived/manual_adjudication_v2/predicate_source_provenance.json"

rg -n -i '完成.*核验|完整书目|DOI|全文|metadata|gap|v3\.3|历史 Judge|人工.*真值|manual_adjudication_v2' \
  "$ROOT/related_work/provenance/CURRENT_SOURCE_AUDIT.md" \
  "$ROOT/related_work/provenance/predicate_provenance.md" \
  "$ROOT/discover_matrix/docs/protocol/semantic_judge_protocol.md"
```

## Input Hashes

- `CURRENT_SOURCE_AUDIT.md`:
  `sha256:95dc952b9ed725a807c8e36f8d82bce9961586b8593743fa8ccbbabd263a44ac`
- `predicate_provenance.md`:
  `sha256:72e5bb4991326179555c766dee06d39ee2f2025e2666956dd85bae149cc042f3`
- `predicate_source_provenance.json`:
  `sha256:409ee4d67540c3de78fc2260308db5692eac95be8d4494b350b6fe47887b5a14`
- `semantic_judge_protocol.md`:
  `sha256:2b18b607408288e3ebb2521ef34bd0a49b2c05ea814e68d672d5cd177d94fbd8`
## Post-fix targeted rereview (2026-08-29)

**Verdict: PASS (proposal only).** This targeted rereview was performed by an
independent subagent as a proposal, without provider calls and without changes
to frozen raw artifacts or canonical decisions. It inspected only the four
materials named in the rereview request.

### Disposition

| Finding | Severity | Post-fix disposition | Targeted rereview result |
|---|---|---|---|
| `ACAD-20-001` | I | Fixed in working tree | PASS |

`ACAD-20-001` previously required the provenance audit to stop implying that a
source-ID/catalog check was a complete bibliography, DOI, stable-link, or
full-text verification. The corrected scope now does so explicitly:

- `related_work/provenance/CURRENT_SOURCE_AUDIT.md:20-22` limits the audit to
  source-ID mapping, `supports`, and `boundary`, and excludes bibliography,
  DOI, stable-link, and full-text verification. Lines 5-8 preserve the
  `bibliography_and_full_text_metadata_gap` rather than reconstructing missing
  metadata from titles or paths.
- `related_work/provenance/predicate_provenance.md:16-20` states the same
  source-ID mapping/support/boundary scope and directs missing metadata to the
  explicit evidence-gap record.
- `derived/manual_adjudication_v2/predicate_source_provenance.json` has 19
  predicate rows and 57 `source_provenance` edges. Every edge has
  `claim_verification_status =
  "mapping_and_boundary_read_from_frozen_catalog"` and
  `metadata_status = "not_recorded_in_frozen_source_catalog"`; bibliography
  and DOI/stable-link are null for all 57 edges, while `accessed_at` is present
  for all 57. This preserves, rather than conceals, the 57 bibliography/DOI
  evidence gaps.
- `discover_matrix/docs/protocol/semantic_judge_protocol.md:19` identifies
  `semantic-judge.two-stage.v3.3` as the implementation/protocol version.
  Lines 59-74 separately identify manual v2 as the paper-result source and
  state that v3.3 and old headline results remain historical Judge-tool
  material, not a source of new manual truth.

### Reproduction

Provider-free evidence commands used for this targeted rereview:

```bash
rg -n 'source-ID|supports|boundary|bibliograph|DOI|stable|v3\.3|manual v2' \
  related_work/provenance/CURRENT_SOURCE_AUDIT.md \
  related_work/provenance/predicate_provenance.md \
  discover_matrix/docs/protocol/semantic_judge_protocol.md

jq '{predicate_rows:(.rows|length),source_edges:([.rows[]|.source_provenance[]]|length),claim_statuses:([.rows[]|.source_provenance[]|.claim_verification_status]|group_by(.)|map({status:.[0],count:length})),metadata_statuses:([.rows[]|.source_provenance[]|.metadata_status]|group_by(.)|map({status:.[0],count:length})),missing_bibliography:([.rows[]|.source_provenance[]|select(.bibliography==null)]|length),missing_doi_or_stable_link:([.rows[]|.source_provenance[]|select(.doi_or_stable_link==null)]|length),missing_access_date:([.rows[]|.source_provenance[]|select(.accessed_at==null or .accessed_at=="")]|length)}' \
  derived/manual_adjudication_v2/predicate_source_provenance.json
```

No new citation was invented, no human attestation is claimed, and this review
does not assess or certify canonical decisions.
