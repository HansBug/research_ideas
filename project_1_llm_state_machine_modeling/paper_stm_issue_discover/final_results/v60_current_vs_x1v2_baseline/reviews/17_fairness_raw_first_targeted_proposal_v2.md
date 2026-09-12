# Pane5 fairness/leakage raw-first targeted proposal v2

**身份与状态**：`subagent / independent proposal / fairness-leakage reviewer / RAW-FIRST / NOT FINAL`。
本文件是提交主 session 的独立 proposal，不是 canonical decision，不替代正式 review log。

## Evidence boundary

本 proposal 的实质判定只使用冻结 `raw/v60_current`、冻结 `raw/x1v2_baseline`、作者 NL/PlantUML source closure、source inventory，以及 reviewer projection bytes。没有把 canonical decision、旧 reference label 或后验 Judge adjudication 当作判定依据；没有调用 provider，也没有修改 raw/canonical。

Projection under review:

- `derived/manual_adjudication_v2/reviewer_input_projection.jsonl`, 1783 valid JSONL objects, SHA-256 `sha256:3844375907781b7de1168b0ef8b20e562ab6118941b26a947f11b1905a1f8f40`.
- Current raw archive aggregate: `sha256:b69e7e91ac0f6dbf41a6dd9b5fe8d4e2d559bbe70ea103180c29a737ee826b51`.
- Baseline raw archive aggregate: `sha256:9e8d513aa9ec4237d768816110426d0f2c7314050d4b91083e93b3b4b0a4fdc2`.
- Author source closure manifest: `reference/x1v2_input_closure/manifest.json`, 54 pair entries / 108 source files, SHA-256 `sha256:a68bc45acf1a6dafb42e363358c1a82e0caf4898077a9dcb5e275e21d848db95`.

## Coverage and raw/source symmetry

| surface | coverage/result |
|---|---:|
| projection rows | arm-a 1271; arm-b 512; total 1783 |
| pair tokens | 54 in each arm |
| rounds | 1/2/3 in each arm |
| common Judge report schema | 162 current + 162 baseline, `paper1.semantic-judge.pair-result.v10` |
| method schema | current `evidence-discovery.method_cell.v9`; baseline `x1-baseline-arm/1` |
| source hash pairing | 54/54 pairs have both arms and identical NL/PlantUML hashes |

The source inputs are symmetric by pair: the projection source-hash comparison returned zero bad pairs. This does not make the report extraction metadata symmetric.

## Findings

### F17-FL-PROP-001 — FAIL / C — projection values disclose the producing report pipeline

**Path/line/pointer/hash**

- Projection line 1: `claim_pointer=/report_issue_clusters/0/issue_id`, `where_pointer=/report_issue_clusters/0/element_refs`, and non-empty `report_evidence.element_refs`.
- Projection line 1272: `claim_pointer=/parsed_output/issues/0/issue`, `where_pointer=/parsed_output/issues/0/where`, and `report_evidence.element_refs=[]`.
- Projection SHA-256: `sha256:3844375907781b7de1168b0ef8b20e562ab6118941b26a947f11b1905a1f8f40`.

**Reason**: Although top-level row keys are identical and arm tokens are opaque, pointer roots and reference population identify which extraction schema produced a row. Across all rows, arm-a has non-empty references in `1271/1271`; arm-b has `0/512`. This is a direct side-inference channel.

**Basis**: The 54 source-hash pairs are symmetric, while the report pointers are arm-specific. The difference is introduced after report generation and is not an authored NL/PlantUML fact.

**Recompute command / evidence pointer**:

```bash
PROJ="$ROOT/derived/manual_adjudication_v2/reviewer_input_projection.jsonl"
jq -s 'group_by(.arm_token) | map({arm:.[0].arm_token,rows:length,
  nonempty_element_refs:(map(select((.report_evidence.element_refs|length)>0))|length),
  claim_pointer_roots:(map(.claim_pointer|split("/")[1])|unique),
  where_pointer_roots:(map(.where_pointer|split("/")[1])|unique)})' "$PROJ"
```

**Disposition**: FAIL/C. Do not use the projection for blind double-sided review. Remove `claim_pointer`, `where_pointer`, `element_refs`, `report_index`, and any source-schema discriminator. Retain normalized claim/reason/location only, with opaque archive-relative tokens.

**Repair commit**: none; proposal is read-only.

**Targeted re-review**: recursively compare non-content JSON paths and value domains across randomized arms; require no pointer-root or optional-field discriminator.

### F17-FL-PROP-002 — FAIL / C — pair-round slots are not symmetric

**Path/line/pointer/hash**: projection rows, `#/pair_token`, `#/round`, and `#/report_evidence`; SHA-256 `sha256:3844375907781b7de1168b0ef8b20e562ab6118941b26a947f11b1905a1f8f40`.

**Reason**: The full 54 pair x 3 round universe has 162 slots, but issue-row projection omits empty reports unevenly: arm-a observes 157 and misses 5; arm-b observes 146 and misses 16. Missing rows can reveal the arm or the report-generation behavior.

**Basis**: Both arms contain 54 pair tokens overall, but not the same pair-round key set. This is independent of semantic answer content.

**Recompute command / evidence pointer**:

```bash
PROJ="$ROOT/derived/manual_adjudication_v2/reviewer_input_projection.jsonl"
jq -s '([.[].pair_token]|unique) as $pairs |
  ([range(1;4) as $round | $pairs[] | {pair:.,round:$round}]) as $universe |
  group_by(.arm_token) | map(. as $rows | {arm:$rows[0].arm_token,
  observed:([$rows[]|{pair:.pair_token,round:.round}]|unique|length),
  missing:($universe-([$rows[]|{pair:.pair_token,round:.round}]|unique)|length)})' "$PROJ"
```

**Disposition**: FAIL/C. Emit an explicit neutral empty record for every pair-round, or review a fixed report-slot envelope rather than only non-empty issue rows.

**Repair commit**: none.

**Targeted re-review**: require `observed=162` and `missing=0` for both arms, then rerun the source/pair mapping check.

### F17-FL-PROP-003 — PASS / M — no expected/answer/Judge/predicate/W2 keys in projection payload

**Path/line/pointer/hash**: all 1783 projection objects, especially `#/projected_target`, `#/report_evidence`, and `#/author_source`; projection SHA-256 `sha256:3844375907781b7de1168b0ef8b20e562ab6118941b26a947f11b1905a1f8f40`.

**Reason**: `projected_target` is null in `1783/1783`. Recursive object-key scan returns zero rows containing provider/model/profile/prompt, expected, predicate, witness, execution receipt, semantic adjudication, primary decision, reference label, or canonical decision keys. The report-evidence marker scan returns zero expected/answer/Judge/W2 markers.

**Basis**: Raw current method artifacts still contain predicate receipts and W2 witness data at `raw/v60_current/method/method/0000/round-1.json#/predicate_execution_receipts`, lines around 435, 842, 948, 2005, and 2320; SHA-256 `sha256:2ea7543607b5361ce738fb03c50be7cc7d5b54c61db31a27c3a44b6a2a65bcea`. Those raw artifacts are not in the projection payload.

**Recompute command / evidence pointer**:

```bash
PROJ="$ROOT/derived/manual_adjudication_v2/reviewer_input_projection.jsonl"
jq -s '[.[]|select(.projected_target != null)]|length' "$PROJ"
jq -s '[.[]|select(any(..|objects; has("provider") or has("model") or has("profile") or has("prompt") or has("expected") or has("predicate") or has("witness") or has("execution_receipt") or has("semantic_adjudication") or has("primary_decision") or has("reference_label") or has("canonical_decision"))) ]|length' "$PROJ"
jq -r '[.report_evidence|..|scalars|strings]|join(" ")' "$PROJ" |
  rg -ni --pcre2 '(^|[^[:alpha:]])(expected|predicate|witness|execution_receipt|W[012]|VALID_KNOWN|VALID_NOVEL|VALID_UNKNOWN|FULL|PARTIAL|NONE|primary_decision|reference_label|canonical_decision|answer|gold)([^[:alpha:]]|$)'
```

**Disposition**: PASS for the current projection payload only. Keep current W2/predicate method output and all evaluator/Judge expected-answer surfaces sealed; do not infer that raw archive safety follows from this PASS.

**Repair commit**: none.

**Targeted re-review**: rerun the recursive key/text denylist on every regenerated projection and fixed samples from each arm and round.

### F17-FL-PROP-004 — FAIL / I — frozen raw contains provider/model/prompt disclosure metadata

**Path/line/pointer/hash**

- `raw/x1v2_baseline/method/run1/0000-luna/record.json#/.configured_model`, `#/.observed_model`, `#/.profile`, `#/.prompt_file`, `#/.prompt_sha256`, `#/.provider`, `#/.system_prompt`, `#/.user_prompt`; lines 20, 37, 54-64, 106. SHA-256 `sha256:91718e94c96ae95b9609f04f4fd1c0342fd914074dafaa8e237c5fa717b15828`.
- `raw/v60_current/judge/source_runs/86407845e4d5428ab8334fce3398cf60/run_manifest.json#/model_profile`; line 14. SHA-256 `sha256:322b072337a8aa69b99fc6401c41b7b7aef65424525da6a16bef9020905a56ac`.
- Both sides' Judge pair reports expose `#/model_profile`, `#/prompt_template_hash`, and `#/response_schema_hash` under common schema v10; current sample SHA-256 `sha256:16e96cfee8ed97730efaf6000f89e6539a8114c40ee6fc9e82caa1da1a8d73b2`, baseline sample SHA-256 `sha256:b251d3fb84b4fe0f7a0076cc955992735724e61d4f10c11032b78608127e4023`.

**Reason**: Direct raw exposure lets a reviewer identify model/provider/prompt family and arm-specific run paths. These fields are reproducibility metadata, but they are not fairness-neutral reviewer inputs.

**Recompute command / evidence pointer**:

```bash
find "$ROOT/raw/x1v2_baseline/method" -type f -name record.json -print0 |
  xargs -0 jq -s '[.[]|select((.configured_model!=null) and (.observed_model!=null) and (.profile!=null) and (.provider!=null) and (.system_prompt!=null) and (.user_prompt!=null))]|length'
find "$ROOT/raw/v60_current/judge/source_runs" -type f -path '*/pairs/*.json' -print0 |
  xargs -0 jq -s '[.[]|select(.model_profile!=null)]|length'
```

**Disposition**: FAIL/I for direct raw access. Keep raw identity/prompt metadata in the sealed archive; disclose provider/model strata only post-review in archive-relative methods documentation.

**Repair commit**: none.

**Targeted re-review**: recursively scan the reviewer projection for identity/path fields and verify none are present or arm-dependent.

## Proposal conclusion

**Overall proposal status: FAIL.** Current projection payload has no observed expected/answer/Judge/predicate/W2 backflow, and source hashes map symmetrically across 54 pairs. It remains inadmissible because pointer/reference values and missing pair-round slots disclose the arm-specific report pipeline; direct raw exposure also leaks provider/model/prompt metadata. This is a subagent proposal only, not FINAL.
