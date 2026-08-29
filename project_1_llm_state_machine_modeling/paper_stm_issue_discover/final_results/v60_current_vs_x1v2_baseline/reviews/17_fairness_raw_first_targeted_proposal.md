# Pane5 fairness/leakage raw-first targeted proposal
**身份与状态**：`subagent / independent proposal / fairness-leakage reviewer / BLIND`。
本文件是独立审查提案，不是 FINAL，不替代主 session 的正式 review log，也不构成 canonical decision。

**执行边界**：本轮在本文件写入并封存前只读取了冻结 `raw/v60_current`、冻结 `raw/x1v2_baseline`、作者 NL/PlantUML source closure 及其 manifest。没有读取 canonical decisions、旧 reference labels、`derived/manual_adjudication_v2`、旧 Judge audit 或任何 proposal；没有调用 provider；没有修改 frozen raw、canonical decision 或 source closure。

## Scope and coverage

| surface | observed coverage |
|---|---:|
| current method cells | 162 files = 54 pairs x 3 rounds; schema `evidence-discovery.method_cell.v9` |
| baseline method records | 162 files = 54 pairs x 3 rounds; schema `x1-baseline-arm/1` |
| current Judge pair reports | 162 files = 54 pairs x 3 rounds; schema `paper1.semantic-judge.pair-result.v10` |
| baseline Judge pair reports | 162 files = 54 pairs x 3 rounds; schema `paper1.semantic-judge.pair-result.v10` |
| current Judge run manifests | 3; all carry `model_profile` |
| author source closure | 108 pair directories, 108 `nl.txt`, 108 `plantuml.puml`; manifest has 108 pair entries / 216 file entries |

Archive-relative aggregate hashes, using sorted relative paths and per-file SHA-256 lines (excluding `**/llm/**`, `*.lock`, `*.part`, and `launcher.log` as specified by the raw archive manifests):

- `raw/v60_current`: `sha256:b69e7e91ac0f6dbf41a6dd9b5fe8d4e2d559bbe70ea103180c29a737ee826b51` (1509 files including archive manifest; 1508 manifest-listed files, 0 manifest mismatches).
- `raw/x1v2_baseline`: `sha256:9e8d513aa9ec4237d768816110426d0f2c7314050d4b91083e93b3b4b0a4fdc2` (843 files including archive manifest; 842 manifest-listed files, 0 manifest mismatches).
- `reference/x1v2_input_closure`: `sha256:db22f5bf8cda5bfea4254e87eabfc8982547850bbf583e42d5f42920c141061c`; manifest byte check: 216/216 files, 0 mismatch.

## Shuorenhua review protocol

This is a `docs/status` audit artifact, so the conservative `audit-only` mode applies. Protected spans were recorded before interpretation: field names, schema IDs, paths, pair/round counts, hashes, model/provider/prompt metadata, command strings, status values, and numeric totals. They are quoted only as evidence and are not normalized or rewritten.

First-pass issue list:

1. Provider/model/profile and prompt metadata are present in reviewer-adjacent raw records.
2. Current-only predicate, witness-level, expected, and evaluator-derived fields are present in the raw archive.
3. Expected/old-answer semantics are present in composite/evaluator surfaces on both sides.
4. No direct `manual_adjudication`, `primary_decision`, `reference_label`, or `canonical_decision` marker was found in the scanned raw sides; this is a lexical control only, not proof of semantic isolation.
5. Source closure and side/round/pair schema coverage are byte-closed and structurally symmetric.

Fidelity reread: every claim below is traceable to a listed raw path, JSON pointer, line, and file hash; no new label or source identity is inferred from absence of a marker. The distinction between archive-for-reproducibility and reviewer-visible projection is preserved. Residual audit: the second pass re-scanned the same raw scope for lexical decision markers and checked that the proposed projection removes identity, expected/old-answer, and current-only evidence fields without removing report payload or source hashes. No additional finding was added after that residual pass.

## Independent findings and controls

### F17-FL-001 — FAIL / I — provider, model, prompt, and path metadata leakage

**Raw evidence and pointers**

- `raw/x1v2_baseline/method/run1/0000-luna/record.json#/.configured_model`, `#/.observed_model`, `#/.profile`, `#/.prompt_file`, `#/.prompt_sha256`, `#/.provider`, `#/.system_prompt`, `#/.user_prompt`; lines 20, 37, 54-64, and 106. File SHA-256: `sha256:91718e94c96ae95b9609f04f4fd1c0342fd914074dafaa8e237c5fa717b15828`.
- The same six-field presence check returned `162/162` baseline records. The input object in that file also exposes absolute author-source paths and hashes at lines 26-33.
- `raw/v60_current/judge/source_runs/86407845e4d5428ab8334fce3398cf60/run_manifest.json#/model_profile`; line 14, with pair/round selection at lines 15-71. File SHA-256: `sha256:322b072337a8aa69b99fc6401c41b7b7aef65424525da6a16bef9020905a56ac`.
- `raw/v60_current/judge/source_runs/77404499c3ac4511a218f0ad3f91c45b/pairs/0000.json#/model_profile`, `#/prompt_template_hash`, `#/response_schema_hash`; lines 10, 13-14. File SHA-256: `sha256:16e96cfee8ed97730efaf6000f89e6539a8114c40ee6fc9e82caa1da1a8d73b2`.
- Baseline Judge has the same reviewer-adjacent identity fields at `raw/x1v2_baseline/judge/source_runs/x1v2-full-r1-rest-05cf0da6/pairs/0000.json#/model_profile`, `#/prompt_template_hash`, and `#/response_schema_hash`; lines 10, 13-14. File SHA-256: `sha256:b251d3fb84b4fe0f7a0076cc955992735724e61d4f10c11032b78608127e4023`.

**Reason**: A reviewer receiving these raw records can identify model/profile/provider, distinguish the baseline arm from current, infer prompt/template family, and use path naming as an arm/source hint. The baseline additionally exposes the complete prompt body. This is a fairness/leakage failure even if the metadata is useful for reproducibility.

**Basis**: Raw counts show all 162 baseline method records carry the six metadata fields; all 162 current and all 162 baseline Judge pair reports carry `model_profile`; all 3 current run manifests carry it. This is an observed archive property, not an inference from a canonical label.

**Recompute command / evidence pointer**:

```bash
find "$ROOT/raw/x1v2_baseline/method" -type f -name record.json -print0 |
  xargs -0 jq -s '[.[] | select((.configured_model != null) and (.observed_model != null) and (.profile != null) and (.provider != null) and (.system_prompt != null) and (.user_prompt != null))] | length'
find "$ROOT/raw/v60_current/judge/source_runs" -type f -path '*/pairs/*.json' -print0 |
  xargs -0 jq -s '[.[] | select(.model_profile != null)] | length'
```

**Disposition**: Keep identity/prompt detail in a sealed non-reviewer reproducibility manifest. Generate an archive-relative reviewer projection containing only opaque `run_token`, `side` (randomized), opaque `pair_id`, `round`, report payload, and author-source hash. Remove provider, adapter, configured/observed model, profile, model profile, prompt body/file/hash, schema/template identity, absolute paths, and provider-specific run names from reviewer-visible JSON. Disclose the existence of model/provider stratification only in a post-review methods note, not per item.

**Repair commit**: none; this review is read-only and no repair was authorized.

**Targeted re-review**: after projection generation, validate the denylist over every projected file, compare side/round/pair coverage, and run a fresh provider-free blind leakage scan before any canonical unblinding. Re-review this finding against the projection manifest hash and a random sample of 10 projected records per side.

### F17-FL-002 — FAIL / I — current-only predicate/W2/evaluator material can backflow into the double-sided reviewer input

**Raw evidence and pointers**

- `raw/v60_current/method/method/0000/round-1.json#/predicate_execution_receipts`; sample receipt schema at line 435 and W2 witness at line 948. The same file contains `#/.../predicate_verdict` at lines 842 and 2214, `#/.../witness_level` at lines 948 and 2320, `#/.../expected` at lines 458 and 2322, and a W2 audit bundle at line 2005. File SHA-256: `sha256:2ea7543607b5361ce738fb03c50be7cc7d5b54c61db31a27c3a44b6a2a65bcea`.
- Across all current method cells: predicate receipts `162/162`, 2,461 receipts total; report issue clusters in `157/162`, 1,271 clusters total; witness values include W2 (1,229 receipt values); predicate verdicts include `false` (629) and `unsupported` (1,224).
- `raw/v60_current/judge/composite/evaluator/evaluation_summary.json#/l2_expected_count`, `#/full_hit_count`, `#/supported_count`, and `#/witness_levels`; lines 35, 44, 55, and 1029-1037. File SHA-256: `sha256:ddb5b5d8a33dc2c5a1e1f1c7df4e784547445fe6e39fe513933283623343cbeb`.
- `raw/v60_current/judge/composite/evaluator/expected_issue_witness_audit.json#/expected_id`, `#/match_status`, `#/predicate_id`, `#/predicate_logic`, `#/witness_level`; lines 34-36, 47-61, and 85-105. File SHA-256: `sha256:d422214f1a18804f03f4ea6b9b3a5204b18f99f2430e9647935dea746c70c655`.
- `raw/v60_current/judge/composite/evaluator/stage_loss.json#/judge_boundary`, `#/w2_finding_coverage`, and `#/witness_levels`; lines 5, 199-202, and 239-242. File SHA-256: `sha256:95efd43ed8f682e177a75cc7ccc710460bfaabb882eda328d3bb6303a31523a1`.

**Reason**: The current-side raw archive physically co-locates semantic report material with current-only executable predicates, witness levels, expected text, and evaluator aggregation. These fields can reveal which obligations were selected, how they were classified, and which witness tier was reached. They are not a side-neutral report payload. The method context declares evaluation ground truth forbidden at lines 151-156, but that declaration does not remove the evaluation-shaped fields from the stored output.

**Basis**: The counts and pointers above are obtained from frozen current raw bytes. The finding is about reviewer-input eligibility and information-flow risk; blind review does not claim that a canonical reviewer actually consumed these fields.

**Recompute command / evidence pointer**:

```bash
find "$ROOT/raw/v60_current/method/method" -type f -name 'round-*.json' -print0 |
  xargs -0 jq -s '{cells:length,receipt_cells:(map(select((.predicate_execution_receipts|length)>0))|length),receipts:(map(.predicate_execution_receipts|length)|add),clusters:(map(.report_issue_clusters|length)|add),w2:([.[].predicate_execution_receipts[]?.witness_level]|map(select(.=="W2"))|length)}'
rg -ni --pcre2 'expected_issue|expected_count|full_hit_count|\bFULL\b|\bPARTIAL\b|\bNONE\b|\bW[012]\b|predicate_execution|predicate_logic|w2_' "$ROOT/raw/v60_current/method" "$ROOT/raw/v60_current/judge/composite"
```

**Disposition**: Exclude `raw/v60_current/method/**`, `judge/composite/evaluator/**`, evaluator summaries, W2 bundles, predicate receipts, and witness ledgers from the reviewer projection. Reviewer-visible current and baseline inputs must be report payload only, with an explicit schema denylist rejecting `predicate_*`, `witness_level`, `W0/W1/W2`, `expected*`, `match_status`, `FULL/PARTIAL/NONE`, and evaluator metric keys. Preserve these artifacts in an audit-only sealed archive for reproducibility.

**Repair commit**: none; no raw or canonical mutation performed.

**Targeted re-review**: run the denylist and JSON-pointer scan on the generated projection, verify zero current-only fields in both sides, then sample every round for pairs `0000`, `0017`, `0033`, `0049`, and `0059`. Any hit remains FAIL/I.

### F17-FL-003 — FAIL / I — expected and old-answer semantics are present in raw composite/evaluator surfaces

**Raw evidence and pointers**

- `raw/v60_current/judge/composite/evaluator/expected_issue_witness_audit.json#/expected_id` and `#/match_status`; lines 35-36 and 47-48. Same file hash: `sha256:d422214f1a18804f03f4ea6b9b3a5204b18f99f2430e9647935dea746c70c655`.
- `raw/v60_current/judge/composite/evaluator/evaluation_summary.json#/l2_expected_count` and `#/full_hit_count`; lines 35 and 44. Same file hash: `sha256:ddb5b5d8a33dc2c5a1e1f1c7df4e784547445fe6e39fe513933283623343cbeb`.
- `raw/x1v2_baseline/judge/composite-summary.json` includes per-pair `expected_count` at lines 464, 480, 496, and subsequent pair entries; file SHA-256: `sha256:e74ef49673173736a2ce090b34d05a7ca8033493a51278c580b912b7006aa2e9`.
- Both side pair-result files expose `#/expected_outcomes` and `#/final_reading/expected_assessments` under the common v10 schema. Current sample hash: `sha256:16e96cfee8ed97730efaf6000f89e6539a8114c40ee6fc9e82caa1da1a8d73b2`; baseline sample hash: `sha256:b251d3fb84b4fe0f7a0076cc955992735724e61d4f10c11032b78608127e4023`.

**Reason**: `expected_id`, `expected_count`, `match_status`, `FULL/PARTIAL/NONE`, and expected-assessment structures are answer-bearing or answer-adjacent fields. A lexical scan finding no `reference_label` or `canonical_decision` string does not make these fields safe: the semantic label is encoded by field/value structure.

**Basis**: The pointers are raw JSON structures and the paired report schema is common on both sides. This is a projection boundary finding, not a claim that the original authored NL/PlantUML contains labels.

**Recompute command / evidence pointer**:

```bash
rg -ni --pcre2 'expected_id|expected_count|full_hit_count|supported_count|\bFULL\b|\bPARTIAL\b|\bNONE\b|VALID_KNOWN|VALID_NOVEL|\bINVALID\b|expected_outcomes|expected_assessments|match_status' \
  "$ROOT/raw/v60_current" "$ROOT/raw/x1v2_baseline"
```

**Disposition**: Do not pass composite summaries, evaluator files, `expected_outcomes`, expected assessments, expected IDs, or old-answer match labels to semantic/fairness reviewers. The reviewer projection should retain only the authored report payload and source-reference hashes. A sealed evaluator-to-report join may be used after blind review, keyed by an opaque projection token and held outside the reviewer input.

**Repair commit**: none; read-only proposal only.

**Targeted re-review**: after projection, run the complete answer-marker/JSON-key denylist over both sides and perform a byte-level diff of the projection schema. Re-review all 54 pair IDs x 3 rounds for zero answer-bearing fields.

### F17-FL-004 — PASS / M — source closure and structural coverage controls

**Evidence and pointers**

- `reference/x1v2_input_closure/manifest.json#/inputs`; lines 1-15 show the byte-checked NL/PlantUML basis and source paths. File SHA-256: `sha256:a68bc45acf1a6dafb42e363358c1a82e0caf4898077a9dcb5e275e21d848db95`.
- `reference/x1v2_input_closure`: aggregate hash `sha256:db22f5bf8cda5bfea4254e87eabfc8982547850bbf583e42d5f42920c141061c`; 216/216 manifest file checks passed.
- Both method and Judge sides independently recomputed to 162 files, 54 pair IDs, and rounds 1/2/3. Both Judge report sets parse as `paper1.semantic-judge.pair-result.v10`.
- Raw lexical scan returned zero matches for `manual_adjudication`, `primary_decision`, `reference_label`, and `canonical_decision` across both raw sides.

**Reason**: Source closure is complete and the two sides have matching file/pair/round/schema coverage at the report-container level. No direct forbidden-decision marker was observed in this raw scope.

**Basis**: `jq` schema/coverage aggregation, manifest hash comparison, `sha256sum`, and the marker scan above. The PASS is limited to closure and structure; it does not override F17-FL-001 through F17-FL-003.

**Disposition**: Preserve the closure manifest and hashes in the sealed archive. Expose only archive-relative source hashes and opaque reviewer pointers in the reviewer projection.

**Repair commit**: none.

**Targeted re-review**: confirm 54/54 pair coverage and 3/3 rounds per side after projection, then rerun source hash closure and the marker scan.

## Blind proposal conclusion

**Overall proposal status: FAIL / reviewer projection not yet admissible.** The raw source closure and report-container schema are structurally usable, but the archive is not safe to expose directly to a fairness/leakage reviewer. F17-FL-001, F17-FL-002, and F17-FL-003 remain proposed FAIL/I until an archive-relative reviewer projection is generated and passes the targeted re-review gates. This file is intentionally a subagent proposal and must be submitted to the main session for the formal review log.
