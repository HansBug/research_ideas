# Pane5 fairness/leakage raw-first targeted proposal v3

**身份与状态**：`subagent / independent proposal / fairness-leakage reviewer / RAW-FIRST / NOT FINAL`。
本文件只供主 session 进入正式 review log，不是 canonical decision，也不构成 FINAL。

## Boundary

本轮只读取冻结 `raw/v60_current`、冻结 `raw/x1v2_baseline`、作者 NL/PlantUML source closure，以及当前 reviewer projection。没有读取 canonical decision、reference label、manual adjudication decision、旧 Judge audit 或 proposal；没有调用 provider；没有修改 raw、source closure 或 canonical data。

审查对象为 `derived/manual_adjudication_v2/reviewer_input_projection.jsonl`，当前 SHA-256：
`sha256:299eaa144026f64b166a9f79e7e522496a441eed7f9057bcba3925b06a10b95e`。

## Coverage

| check | result |
|---|---:|
| JSONL | 2642 valid objects; 0 empty lines |
| randomized arms | arm-a 1321; arm-b 1321 |
| pair coverage | 54 pair tokens in each arm |
| round coverage | rounds 1/2/3 in each arm; 162/162 pair-round slots each |
| slot grid | 1321 distinct `(pair, round, slot)` rows per arm; 0 duplicates; 0 pair-round slot-set mismatch |
| projection schemas | one identical top-level, author-source, and report-evidence key shape |
| source pairing | 54 pairs, 0 hash-pair mismatch for NL/PlantUML |
| frozen input status | no changed raw/reference path observed |

The raw archives remain byte-identified by their frozen manifests:

- `raw/v60_current/archive_manifest.json`: `sha256:8c2105dd7025f360500709e25ac9b483b907fdd91a3c39144798158ca1a25ba0`.
- `raw/x1v2_baseline/archive_manifest.json`: `sha256:8e9fa28071ba4acbbc0483c5ba84029ac69e7d0a618311ec85f7992081b374d0`.
- source closure manifest: `reference/x1v2_input_closure/manifest.json`, `sha256:a68bc45acf1a6dafb42e363358c1a82e0caf4898077a9dcb5e275e21d848db95`; 108/108 source-file hashes matched.

## Findings

### F17-FL-PROP3-001 — PASS / M — side, pair, round, and slot mapping is symmetric

**Path/pointer/hash**: every row of `derived/manual_adjudication_v2/reviewer_input_projection.jsonl`; fields `#/arm_token`, `#/pair_token`, `#/round`, `#/slot`, `#/schema`; SHA-256 `sha256:299eaa144026f64b166a9f79e7e522496a441eed7f9057bcba3925b06a10b95e`.

**Reason/basis**: Both arm tokens use the same row shape, source shape, report-evidence shape, pair universe, round universe, and per-pair-round slot set. The previous pointer/reference metadata is absent: zero rows have `claim_pointer`, `where_pointer`, `report_index`, or `element_refs` keys. Empty report payloads differ by arm (50 versus 809), but each side occupies the same fixed slot grid; this is report-result occupancy, not an arm-name or pipeline-schema discriminator.

**Recompute command / evidence pointer**:

```bash
PROJ="$ROOT/derived/manual_adjudication_v2/reviewer_input_projection.jsonl"
jq -s '([.[].pair_token]|unique) as $pairs |
  ([range(1;4) as $round|$pairs[]|{pair:.,round:$round}]) as $universe |
  group_by(.arm_token)|map(. as $rows|{arm:$rows[0].arm_token,
  rows:length,pairs:([$rows[].pair_token]|unique|length),
  observed:([$rows[]|{pair:.pair_token,round:.round}]|unique|length),
  missing:($universe-([$rows[]|{pair:.pair_token,round:.round}]|unique)|length),
  slot_pairs:([$rows[]|[.pair_token,.round,.slot]]|unique|length),
  duplicate_slot_pairs:([$rows[]|[.pair_token,.round,.slot]]|group_by(.)|map(select(length>1))|length)})' "$PROJ"
jq -s 'group_by([.pair_token,.round])|
  map({arms:(group_by(.arm_token)|map({slots:(map(.slot)|sort)}))})|
  map(select((.arms|length)!=2 or (.arms[0].slots != .arms[1].slots)))|length' "$PROJ"
```

**Disposition**: retain the fixed slot envelope and opaque arm tokens. The differing blank-row totals should be documented as report occupancy only; do not attach an arm identity to them before review closure.

**Repair commit**: none.

**Targeted re-review**: rerun both commands after every projection regeneration; require two arms, 54 pairs, 162 observed pair-rounds, equal slot sets, and zero duplicate slots.

### F17-FL-PROP3-002 — PASS / M — no expected/answer, later-Judge, predicate, or W2 backflow in projection

**Path/pointer/hash**: every projection row, especially `#/projected_target`, `#/report_evidence`, and nested object keys; SHA-256 `sha256:299eaa144026f64b166a9f79e7e522496a441eed7f9057bcba3925b06a10b95e`.

**Reason/basis**: All `2642/2642` `projected_target` values are null. Recursive key scans returned zero for `expected`, `predicate`, `witness`, `execution_receipt`, `semantic_adjudication`, `judge`, `final_reading`, `expected_outcomes`, `expected_assessments`, `match_status`, `W2`, `predicate_id`, and `predicate_logic`. The report-evidence text scan also returned zero answer/Judge/W2 markers. This establishes that current-only method predicate/W2 and later Judge structures present in frozen raw did not enter the projection.

**Recompute command / evidence pointer**:

```bash
PROJ="$ROOT/derived/manual_adjudication_v2/reviewer_input_projection.jsonl"
jq -s '[.[]|select(.projected_target!=null)]|length' "$PROJ"
for key in expected predicate witness execution_receipt semantic_adjudication judge \
  final_reading expected_outcomes expected_assessments match_status W2 predicate_id predicate_logic; do
  printf '%s ' "$key"
  jq -s "[.[]|select(any(..|objects;has(\"$key\")))]|length" "$PROJ"
done
jq -r '[.report_evidence|..|scalars|strings]|join(" ")' "$PROJ" |
  rg -ni --pcre2 '(^|[^[:alpha:]])(expected|predicate|witness|execution_receipt|judge|W[012]|VALID_KNOWN|VALID_NOVEL|VALID_UNKNOWN|FULL|PARTIAL|NONE|primary_decision|reference_label|canonical_decision|answer|gold)([^[:alpha:]]|$)'
```

**Disposition**: keep the recursive denylist as a release gate. Current raw W2/predicate and later Judge/evaluator surfaces must remain sealed and out of reviewer input.

**Repair commit**: none.

**Targeted re-review**: require every count above to remain zero, with all 2642 rows scanned, after every regeneration.

### F17-FL-PROP3-003 — PASS / M — provider/model/prompt provenance is excluded from projection

**Path/pointer/hash**: projection root and all nested objects; SHA-256 `sha256:299eaa144026f64b166a9f79e7e522496a441eed7f9057bcba3925b06a10b95e`.

**Reason/basis**: Recursive projection scans returned zero for `provider`, `model`, `profile`, `prompt`, `model_profile`, `prompt_template_hash`, `response_schema_hash`, and `raw_attempt_json`. This is necessary because frozen raw does retain identity/prompt metadata: all 162 baseline method records carry configured/observed model, profile, provider, and prompt bodies; 162 current and 162 baseline Judge pair reports carry `model_profile`.

**Recompute command / evidence pointer**:

```bash
PROJ="$ROOT/derived/manual_adjudication_v2/reviewer_input_projection.jsonl"
for key in provider model profile prompt model_profile prompt_template_hash response_schema_hash raw_attempt_json; do
  printf '%s ' "$key"
  jq -s "[.[]|select(any(..|objects;has(\"$key\")))]|length" "$PROJ"
done
find "$ROOT/raw/x1v2_baseline/method" -type f -name record.json -print0 |
  xargs -0 jq -s '[.[]|select((.configured_model!=null) and (.observed_model!=null) and (.profile!=null) and (.provider!=null) and (.system_prompt!=null) and (.user_prompt!=null))]|length'
```

**Disposition**: PASS for projection eligibility. Keep raw provenance/prompt bodies sealed, and disclose provider/model information only after blind review in an archive-relative methods channel.

**Repair commit**: none.

**Targeted re-review**: require zero projection hits for the identity denylist. Any direct raw-to-reviewer handoff remains FAIL/I regardless of this projection PASS.

### F17-FL-PROP3-004 — PASS / M — author source pairing is side-neutral

**Path/pointer/hash**: `#/author_source/nl_sha256`, `#/author_source/plantuml_sha256`, `#/pair_token`; projection SHA-256 `sha256:299eaa144026f64b166a9f79e7e522496a441eed7f9057bcba3925b06a10b95e`.

**Reason/basis**: Each of the 54 pair tokens has both arms and the same author NL/PlantUML source hashes. The source closure contains 108 files and hash verification found zero mismatch.

**Recompute command / evidence pointer**:

```bash
PROJ="$ROOT/derived/manual_adjudication_v2/reviewer_input_projection.jsonl"
jq -s 'def src:{nl:.author_source.nl_sha256,plantuml:.author_source.plantuml_sha256};
  map({arm:.arm_token,pair:.pair_token,src:(src)})|group_by(.pair)|
  {pairs:length,bad:(map(select((map(.arm)|unique|length)!=2 or
  (map(.src)|unique|length)!=1))|length)}' "$PROJ"
```

**Disposition**: retain source hashes and the same author source payload for both arms.

**Repair commit**: none.

**Targeted re-review**: require 54 pairs and zero bad source-hash groups after each projection change.

## Provider-call scope

No provider was called by this independent raw-first review. A workflow-wide `provider_calls=0` assertion is intentionally not made here because its audit proof is outside the permitted raw-first evidence boundary. This is a scope limitation, not evidence of a provider call.

## Proposal conclusion

**Overall proposal status: PASS.** The current reviewer projection is side/pair/round/slot symmetric and contains no observed expected/answer, later-Judge, predicate/W2, or provider/model/prompt leakage. The conclusion is limited to reviewer-input eligibility under the raw-first evidence boundary; frozen raw must remain sealed rather than passed directly to reviewers. No raw or canonical data was modified.
