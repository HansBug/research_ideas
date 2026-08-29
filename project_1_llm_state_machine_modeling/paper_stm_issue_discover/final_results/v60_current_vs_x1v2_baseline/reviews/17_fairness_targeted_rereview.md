# Pane5 fairness/leakage targeted rereview

**身份与状态**：`subagent / independent proposal / fairness-leakage targeted rereview / post-unblind`。
本文件是供主 session 保存到正式 review log 的独立 proposal，不是 FINAL，不替代 canonical decision。

## Boundary and chronology

1. The blind raw-first proposal was written before canonical access:
   `reviews/17_fairness_raw_first_targeted_proposal.md`, SHA-256
   `sha256:43b41e01788bb28bc8261d606b6c49731ac39a4b9aee4f5adeb23f231035e194`.
2. Only after that signature did this rereview read the canonical audit surfaces needed for unblinding: `derived/manual_adjudication_v2/README.md`, `review_log.json`, `pane5_evidence_reads.json`, `MANIFEST`, `reviewer_projection_audit.json`, `reviewer_input_projection.jsonl`, and `predicate_witness_audit.json`.
3. I did not read canonical decision JSON/TSV contents, old Judge audit, or proposal files under `derived/manual_adjudication_v2/proposals`. No provider was called. Frozen raw, source closure, and canonical decisions were not modified.

The projection changed after the earlier rereview: the current file is now
`sha256:3844375907781b7de1168b0ef8b20e562ab6118941b26a947f11b1905a1f8f40`, not the previously recorded `b2a1f315...a0868b`. The current `reviewer_projection_audit.json` and `MANIFEST` both register the new hash. Findings below are against the current bytes.

## Coverage and controls

| surface | observed coverage |
|---|---:|
| reviewer projection | 1783 valid JSONL objects: arm-a 1271, arm-b 512; each side has 54 pair tokens and rounds 1/2/3 |
| raw method cells | 162 current + 162 baseline = 54 pairs x 3 rounds |
| raw Judge pair reports | 162 current + 162 baseline; common schema `paper1.semantic-judge.pair-result.v10` |
| author source closure | 54 pair inputs, 108 `nl.txt`/`plantuml.puml` files; 216/216 manifest checks |
| provider calls | 0 in the canonical audit; no provider was invoked by this review |

Current raw archive-relative aggregate hashes remain:

- `raw/v60_current`: `sha256:b69e7e91ac0f6dbf41a6dd9b5fe8d4e2d559bbe70ea103180c29a737ee826b51`.
- `raw/x1v2_baseline`: `sha256:9e8d513aa9ec4237d768816110426d0f2c7314050d4b91083e93b3b4b0a4fdc2`.
- `reference/x1v2_input_closure`: `sha256:db22f5bf8cda5bfea4254e87eabfc8982547850bbf583e42d5f42920c141061c`; manifest `sha256:a68bc45acf1a6dafb42e363358c1a82e0caf4898077a9dcb5e275e21d848db95`.

Current audit artifacts:

- `derived/manual_adjudication_v2/reviewer_input_projection.jsonl`: `sha256:3844375907781b7de1168b0ef8b20e562ab6118941b26a947f11b1905a1f8f40`.
- `derived/manual_adjudication_v2/reviewer_projection_audit.json`: `sha256:b8f8fc801c116493b26eff749df185b7e68359cf24d01fd3b80f1044355a8d11`.
- `derived/manual_adjudication_v2/MANIFEST`: current SHA-256 `sha256:b2ac5f689159036150cfe0006bde31848b2ea245cfad85e153b4b57b8c5f0e1a`; generated at `2026-08-29T09:32:33+00:00`, its projection and audit entries match the two hashes above.
- `derived/manual_adjudication_v2/review_log.json`: `sha256:182d0898b0f4dc2b0a351b0bf6550b0bc7341e1f56be2c10740c166635636e30`.

## Findings

### F17-FL-RR-001 — FAIL / I — raw provider/model/prompt metadata is disclosure-sensitive

**Path/line/pointer/hash**

- `raw/x1v2_baseline/method/run1/0000-luna/record.json#/.configured_model`, `#/.observed_model`, `#/.profile`, `#/.prompt_file`, `#/.prompt_sha256`, `#/.provider`, `#/.system_prompt`, `#/.user_prompt`; lines 20, 37, 54-64, 106. SHA-256 `sha256:91718e94c96ae95b9609f04f4fd1c0342fd914074dafaa8e237c5fa717b15828`.
- `raw/v60_current/judge/source_runs/86407845e4d5428ab8334fce3398cf60/run_manifest.json#/model_profile`; line 14. SHA-256 `sha256:322b072337a8aa69b99fc6401c41b7b7aef65424525da6a16bef9020905a56ac`.
- `raw/v60_current/judge/source_runs/77404499c3ac4511a218f0ad3f91c45b/pairs/0000.json#/model_profile`, `#/prompt_template_hash`, `#/response_schema_hash`; lines 10, 13-14. SHA-256 `sha256:16e96cfee8ed97730efaf6000f89e6539a8114c40ee6fc9e82caa1da1a8d73b2`.
- Baseline Judge has the corresponding fields at `raw/x1v2_baseline/judge/source_runs/x1v2-full-r1-rest-05cf0da6/pairs/0000.json`; lines 10, 13-14. SHA-256 `sha256:b251d3fb84b4fe0f7a0076cc955992735724e61d4f10c11032b78608127e4023`.

**Reason**: Direct exposure of the frozen raw archive reveals provider/model/profile, prompt family, source paths, and baseline-specific prompt text. These are arm and generation-pipeline clues even though they are legitimate reproducibility metadata.

**Basis**: All 162 baseline method records contain the six model/provider/prompt fields; all 162 current and 162 baseline Judge pair reports carry `model_profile`; the current archive has 3 Judge run manifests carrying `model_profile`. The latest reviewer projection has zero corresponding object keys, so this finding is about raw direct access, not a claim that the latest projection exposes them.

**Recompute command / evidence pointer**:

```bash
find "$ROOT/raw/x1v2_baseline/method" -type f -name record.json -print0 |
  xargs -0 jq -s '[.[] | select((.configured_model != null) and (.observed_model != null) and (.profile != null) and (.provider != null) and (.system_prompt != null) and (.user_prompt != null))] | length'
find "$ROOT/raw/v60_current/judge/source_runs" -type f -path '*/pairs/*.json' -print0 |
  xargs -0 jq -s '[.[] | select(.model_profile != null)] | length'
```

**Disposition**: Keep raw provenance and prompt bodies only in the sealed reproducibility archive. Use an archive-relative reviewer projection with opaque tokens and no provider, adapter, model, profile, prompt body/file/hash, absolute path, or provider-specific run name. Disclose model/provider strata only in a post-review methods note.

**Repair commit**: none; this subagent review is read-only.

**Targeted re-review**: after any regeneration, recursively scan every projected scalar/key for identity and path metadata, compare exact row shapes across randomized side tokens, and recheck all 1783 rows. Any arm-dependent identity field remains FAIL/I.

### F17-FL-RR-002 — PASS / M — no current-only predicate/W2 backflow in the latest projection

**Path/line/pointer/hash**

- Latest projection lines 1 and 1272 both have `projected_target: null`; all 1783 rows have this value. Projection SHA-256 `sha256:3844375907781b7de1168b0ef8b20e562ab6118941b26a947f11b1905a1f8f40`.
- The raw current method still contains the sealed material at `raw/v60_current/method/method/0000/round-1.json#/predicate_execution_receipts`, with predicate fields around lines 435, 842, 948, 2005, and 2320. SHA-256 `sha256:2ea7543607b5361ce738fb03c50be7cc7d5b54c61db31a27c3a44b6a2a65bcea`.
- `derived/manual_adjudication_v2/reviewer_projection_audit.json#/forbidden_keys` includes predicate, execution, and witness keys; audit line 1 records `provider_calls: 0`, row count 1783, and the current projection hash. SHA-256 `sha256:b8f8fc801c116493b26eff749df185b7e68359cf24d01fd3b80f1044355a8d11`.

**Reason**: The earlier direct `projected_target` leakage is absent from the latest projection. Recursive object-key checks returned zero for predicate, witness, execution, semantic-adjudication, and related metadata. The raw current-only W2/predicate artifacts remain sealed and must not be passed as reviewer input.

**Basis**: The raw archive is asymmetric by design: current method schema `evidence-discovery.method_cell.v9` plus W2/predicate artifacts; baseline method schema `x1-baseline-arm/1` with no isomorphic predicate registry. This asymmetry is not present in the latest projection target because the target is null.

**Recompute command / evidence pointer**:

```bash
PROJ="$ROOT/derived/manual_adjudication_v2/reviewer_input_projection.jsonl"
jq -s '[.[] | select(.projected_target != null)] | length' "$PROJ"
jq -s '[.[] | select(any(.. | objects; has("predicate_id") or has("witness_level") or has("execution_receipt") or has("semantic_adjudication")))] | length' "$PROJ"
```

**Disposition**: PASS for the current projection channel only. Continue sealing `raw/v60_current/method/**`, evaluator summaries, predicate receipts, W2 bundles, and witness ledgers. Do not use this PASS to permit direct raw access; F17-FL-RR-001 still applies.

**Repair commit**: none.

**Targeted re-review**: require the two commands above to return `0`, then repeat the recursive scan over all rows and all three rounds after each projection regeneration.

### F17-FL-RR-003 — PASS / M — no expected/old-answer field leakage in the latest projection

**Path/line/pointer/hash**

- Latest projection lines 1 and 1272 contain only report evidence plus source hashes and opaque row metadata; `projected_target` is null. SHA-256 `sha256:3844375907781b7de1168b0ef8b20e562ab6118941b26a947f11b1905a1f8f40`.
- The raw current evaluator retains answer-bearing structures at `raw/v60_current/judge/composite/evaluator/expected_issue_witness_audit.json#/expected_id`, `#/match_status`, `#/predicate_id`, `#/predicate_logic`, `#/witness_level`; lines 35-36, 47-61, 85-105. SHA-256 `sha256:d422214f1a18804f03f4ea6b9b3a5204b18f99f2430e9647935dea746c70c655`.
- The raw baseline composite retains `expected_count` at `raw/x1v2_baseline/judge/composite-summary.json`; lines 464, 480, 496. SHA-256 `sha256:e74ef49673173736a2ce090b34d05a7ca8033493a51278c580b912b7006aa2e9`.

**Reason**: No expected IDs/counts, expected outcomes, match status, witness tier, `FULL/PARTIAL/NONE`, `VALID_*`, or canonical decision field was found in the latest projection's row objects or `report_evidence`. The same structures remain in raw and are therefore not reviewer input.

**Basis**: Projection key scan returned zero for `expected`, `predicate`, `witness`, `execution_receipt`, `provider`, `profile`, and semantic-decision keys. The only three broad lexical hits in `report_evidence` were the ordinary phrase `closed-model` in source location text, not answer metadata.

**Recompute command / evidence pointer**:

```bash
jq -r '[.report_evidence | .. | scalars | strings] | join(" ")' \
  "$ROOT/derived/manual_adjudication_v2/reviewer_input_projection.jsonl" |
  rg -ni --pcre2 '(^|[^[:alpha:]])(expected|predicate|witness|execution_receipt|W2|VALID_KNOWN|VALID_NOVEL|VALID_UNKNOWN|FULL|PARTIAL|NONE|primary_decision|reference_label|canonical_decision|answer|gold)([^[:alpha:]]|$)'
```

**Disposition**: PASS for the latest reviewer projection; keep raw evaluator/composite surfaces sealed and join expected/reference evidence only after blind review in a separate audit channel.

**Repair commit**: none.

**Targeted re-review**: rerun the recursive answer-key denylist over all 1783 rows and sample pairs `0000`, `0017`, `0033`, `0049`, `0059` in rounds 1/2/3 on each randomized side.

### F17-FL-RR-004 — FAIL / C — projection is still side-inferable from report schema/pointers

**Path/line/pointer/hash**

- Projection line 1 (`arm-a`) has `claim_pointer: /report_issue_clusters/0/issue_id`, `where_pointer: /report_issue_clusters/0/element_refs`, and four `report_evidence.element_refs` values. Projection line 1272 (`arm-b`) has `claim_pointer: /parsed_output/issues/0/issue`, `where_pointer: /parsed_output/issues/0/where`, and `element_refs: []`. Projection SHA-256 `sha256:3844375907781b7de1168b0ef8b20e562ab6118941b26a947f11b1905a1f8f40`.
- Across all rows, arm-a has non-empty `element_refs` in `1271/1271`; arm-b has non-empty `element_refs` in `0/512`. Pointer roots are `report_issue_clusters` for `1271/1271` arm-a rows and `parsed_output` for `512/512` arm-b rows.
- `reviewer_projection_audit.json#/policy/projection_shape` says the allowlist is identical, but the audit only records top-level row keys and does not assert value-level side neutrality. Audit SHA-256 `sha256:b8f8fc801c116493b26eff749df185b7e68359cf24d01fd3b80f1044355a8d11`.

**Reason**: Even with an opaque `arm_token`, these values identify the producing report schema and pipeline. A reviewer can classify a row by pointer root or by whether source element references are populated. This is a direct fairness/leakage failure in the reviewer-visible projection, independent of expected-answer leakage.

**Basis**: Both sides have the same top-level projection schema and 54 pair tokens, but their nested report payload values are not side-neutral. The source NL/PlantUML hashes are symmetric per pair; the discriminator is introduced by report extraction metadata, not by the authored source.

**Recompute command / evidence pointer**:

```bash
PROJ="$ROOT/derived/manual_adjudication_v2/reviewer_input_projection.jsonl"
jq -s 'group_by(.arm_token) | map({arm: .[0].arm_token, rows: length,
  nonempty_element_refs: (map(select((.report_evidence.element_refs|length)>0))|length),
  claim_pointer_roots: (map(.claim_pointer|split("/")[1])|unique),
  where_pointer_roots: (map(.where_pointer|split("/")[1])|unique)})' "$PROJ"
```

**Disposition**: Quarantine the projection for double-sided semantic/fairness review. Regenerate an archive-relative allowlist that removes `claim_pointer`, `where_pointer`, `element_refs`, `report_index`, and any report-schema discriminator; retain only normalized report claim/reason/location, opaque report token, round, pair token, and source hashes. If source references are required, encode them in one identical optionality/value schema for both arms and prove non-invertibility.

**Repair commit**: none; no raw or canonical mutation was made.

**Targeted re-review**: require exact recursive path and value-domain equality for every non-content field across arm tokens, zero pointer-root hits, zero arm-dependent optional fields, 54 pair tokens x 3 rounds per side, and a new projection/audit/MANIFEST hash tuple. This remains FAIL/C until that validator passes.

### F17-FL-RR-005 — PASS / M — provider-free chronology and source closure

**Path/line/pointer/hash**

- `derived/manual_adjudication_v2/review_log.json#/workflow` and `#/entries`: 1783 raw reads, 1783 author-source reads, 0 reference-visible, 0 primary-visible, workflow provider calls 0. SHA-256 `sha256:182d0898b0f4dc2b0a351b0bf6550b0bc7341e1f56be2c10740c166635636e30`.
- `derived/manual_adjudication_v2/pane5_evidence_reads.json#/rows`: 1783 rows with raw/source reads and provider-free audit state. SHA-256 `sha256:04254d908b81526d3ae90e7d22bf53b7ab6a1fccaf1d14716a6acc5b84c0ad66`.
- `reference/x1v2_input_closure/manifest.json#/inputs`: 54 source pairs and 216 source files; manifest SHA-256 `sha256:a68bc45acf1a6dafb42e363358c1a82e0caf4898077a9dcb5e275e21d848db95`.
- Frozen raw aggregate hashes are the two values listed above and were unchanged during this review. `git status --short -- raw reference` returned no changed tracked raw/reference path.

**Reason**: The review chronology, provider-free constraint, pair/round coverage, and source hash closure are independently evidenced. This is a narrow process PASS and does not waive the projection side-inference failure.

**Disposition**: Retain as control evidence; do not use it to release the current projection.

**Repair commit**: none.

**Targeted re-review**: after projection repair, rerun the chronology, provider-call, source-closure, raw-hash, and exact-schema commands.

## Final independent conclusion

**Overall: FAIL.** The latest projection successfully removes the previously observed direct predicate/W2/expected target leakage, and the review process is provider-free with closed source coverage. It is still not admissible for a fairness/leakage-controlled double-sided review because report pointer roots and `element_refs` values identify the arm-specific report pipeline; direct raw exposure also remains unsafe because raw provider/model/prompt metadata is retained. No repair commit was made. This is a `subagent/proposal` for the main session's formal review log, not FINAL.

## Final post-fix targeted rereview (proposal addendum; not FINAL)

This addendum records the current post-fix bytes. It does not change the earlier blind signature, canonical data, frozen raw, or canonical decision files.

### F17-FL-PF-001 — FAIL / C — residual side-inferable projection metadata

**Path/line/pointer/hash**: `derived/manual_adjudication_v2/reviewer_input_projection.jsonl` line 1 has `claim_pointer=/report_issue_clusters/0/issue_id`, `where_pointer=/report_issue_clusters/0/element_refs`, and non-empty `report_evidence.element_refs`; line 1272 has `claim_pointer=/parsed_output/issues/0/issue`, `where_pointer=/parsed_output/issues/0/where`, and `element_refs=[]`. Projection SHA-256 is `sha256:3844375907781b7de1168b0ef8b20e562ab6118941b26a947f11b1905a1f8f40`.

**Reason/basis**: The top-level row schema is identical, and each arm contains 54 pair tokens, but the report extraction pipeline is identifiable from values: arm-a `1271/1271` rows have non-empty element references and pointer root `report_issue_clusters`; arm-b `0/512` rows have non-empty references and pointer root `parsed_output`. Pair-round presence is also unequal because issue rows omit empty reports: arm-a is missing 5 of 162 pair-round slots, arm-b is missing 16. Source NL/PlantUML hashes are symmetric for all 54 pairs, so the discriminator is projection/report metadata rather than authored input.

**Recompute command / evidence pointer**:

```bash
PROJ="$ROOT/derived/manual_adjudication_v2/reviewer_input_projection.jsonl"
jq -s 'group_by(.arm_token) | map({arm: .[0].arm_token, rows: length,
  pairs: (map(.pair_token)|unique|length),
  nonempty_element_refs: (map(select((.report_evidence.element_refs|length)>0))|length),
  claim_pointer_roots: (map(.claim_pointer|split("/")[1])|unique),
  where_pointer_roots: (map(.where_pointer|split("/")[1])|unique)})' "$PROJ"

# Compare the 54 x 3 pair-round key universe with each arm's observed keys.
jq -s '([.[].pair_token] | unique) as $pairs |
  ([range(1;4) as $round | $pairs[] | {pair:.,round:$round}]) as $universe |
  group_by(.arm_token) | map({arm:.[0].arm_token,
  observed:([.[].pair_token as $pair | .[]?] | length)})' "$PROJ"
```

**Disposition**: FAIL/C. Quarantine this projection for double-sided fairness review. Regenerate a fixed archive-relative allowlist that removes `claim_pointer`, `where_pointer`, `element_refs`, `report_index`, and any report-schema discriminator; include explicit empty pair-round records so omission cannot identify a side. Keep only normalized report claim/reason/location, opaque report token, pair/round token, and source hashes.

**Repair commit**: none; no repair was made by this subagent.

**Targeted re-review**: rerun the recursive path/value-domain equality check over all rows, require 162 pair-round slots per randomized side, verify 54 source-hash pairs, and recompute projection/audit/MANIFEST hashes. Any non-uniform metadata or missing slot remains FAIL/C.

### F17-FL-PF-002 — PASS / M — answer-bearing and current-only fields absent from projection

**Path/line/pointer/hash**: all 1783 projection rows are valid objects; `projected_target` is `null` in `1783/1783`. Projection SHA-256 is `sha256:3844375907781b7de1168b0ef8b20e562ab6118941b26a947f11b1905a1f8f40`.

**Reason/basis**: Recursive key scan returned `0` rows containing provider/model/profile/prompt, expected, predicate, witness, execution-receipt, semantic-adjudication, primary-decision, reference-label, or canonical-decision keys. The report-evidence answer-marker scan returned no matches for expected, W0/W1/W2, VALID_*, FULL/PARTIAL/NONE, answer, or gold. Raw current W2/predicate and raw evaluator expected structures remain sealed; this PASS is projection-channel scoped.

**Recompute command / evidence pointer**:

```bash
PROJ="$ROOT/derived/manual_adjudication_v2/reviewer_input_projection.jsonl"
jq -s '[.[] | select(.projected_target != null)] | length' "$PROJ"
jq -s '[.[] | select(any(.. | objects; has("provider") or has("model") or has("profile") or has("prompt") or has("expected") or has("predicate") or has("witness") or has("execution_receipt") or has("semantic_adjudication") or has("primary_decision") or has("reference_label") or has("canonical_decision")))] | length' "$PROJ"
jq -r '[.report_evidence | .. | scalars | strings] | join(" ")' "$PROJ" |
  rg -ni --pcre2 '(^|[^[:alpha:]])(expected|predicate|witness|execution_receipt|W[012]|VALID_KNOWN|VALID_NOVEL|VALID_UNKNOWN|FULL|PARTIAL|NONE|primary_decision|reference_label|canonical_decision|answer|gold)([^[:alpha:]]|$)'
```

**Disposition**: PASS for absence of answer/current-only backflow in the current projection. Continue to deny direct access to raw method W2/predicate artifacts and raw evaluator/composite expected-answer surfaces.

**Repair commit**: none.

**Targeted re-review**: rerun the three commands on all regenerated projection bytes and sample pairs `0000`, `0017`, `0033`, `0049`, `0059` in rounds 1/2/3 for both randomized sides.

### F17-FL-PF-003 — PASS / M — provider-free audit and source side mapping

**Path/line/pointer/hash**: `derived/manual_adjudication_v2/reviewer_projection_audit.json` line 1 reports `provider_calls=0`, `row_count=1783`, arm counts `1271/512`, and projection hash `sha256:3844375907781b7de1168b0ef8b20e562ab6118941b26a947f11b1905a1f8f40`; audit SHA-256 `sha256:b8f8fc801c116493b26eff749df185b7e68359cf24d01fd3b80f1044355a8d11`. `derived/manual_adjudication_v2/MANIFEST` currently records both matching hashes; current MANIFEST SHA-256 is `sha256:1cecbabe2590d2b0e6bf822631ea04a512aad8fb5116abc6a43d90bb48269b94`.

**Reason/basis**: The provider-free workflow is independently recorded, both arms have 54 pair tokens, and source NL/PlantUML hash comparison returned no bad pair. Frozen raw/reference status returned no changed path during this rereview. This control PASS does not waive F17-FL-PF-001 or the raw direct-disclosure finding F17-FL-RR-001.

**Recompute command / evidence pointer**:

```bash
PROJ="$ROOT/derived/manual_adjudication_v2/reviewer_input_projection.jsonl"
jq -e --arg p "$(jq -r '.canonical_files["reviewer_input_projection.jsonl"]' "$ROOT/derived/manual_adjudication_v2/MANIFEST")" \
  '(.projection_sha256 == $p) and (.provider_calls == 0) and (.row_count == 1783)' \
  "$ROOT/derived/manual_adjudication_v2/reviewer_projection_audit.json"
jq -s 'def source: {nl:.author_source.nl_sha256,plantuml:.author_source.plantuml_sha256};
  map({arm:.arm_token,pair:.pair_token,source:(source)}) | group_by(.pair) |
  map(select((map(.arm)|unique|length)!=2 or (map(.source)|unique|length)!=1)) | length' "$PROJ"
git status --short -- "$ROOT/raw" "$ROOT/reference"
```

**Disposition**: PASS for provider-free execution, hash registration, and source side mapping. No repair commit or provider call exists.

**Targeted re-review**: after projection repair, verify provider calls remain zero, raw/reference status remains unchanged, and audit/MANIFEST hashes match the regenerated projection.

## Post-fix proposal conclusion

**Overall: FAIL.** The post-fix projection passes the answer-bearing/current-only leakage and provider-free checks, but fails fairness admissibility because report pointer roots, `element_refs`, and omitted empty pair-round slots reveal arm-specific extraction behavior. The raw archive also remains unsuitable for direct reviewer exposure because it retains provider/model/prompt metadata. This remains a `subagent/proposal`; no canonical data, frozen raw, or repair commit was modified.
