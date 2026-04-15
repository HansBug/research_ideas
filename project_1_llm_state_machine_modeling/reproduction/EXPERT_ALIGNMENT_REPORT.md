# Expert Review Alignment Report

## 1. Scope

This file records the final alignment experiments for the standalone [`expert_review`](./expert_review/) agent against real human expert scores from the TTool-AI baseline dataset.

Alignment target:

- Keep the external interface unchanged: `prompt`, `input`, `pred-output`, optional `ref-output`
- Keep the review flow LLM-first
- Do not add hidden baseline-specific dispatch inside the agent
- Use the published human scores from [`results.ods`](./data/raw/ttool-ai/results.ods)
- Produce final structured results in [`alignment_reviews.parquet`](./results/ttool/expert_alignment/paper_rubric_v5/alignment_reviews.parquet) and [`alignment_summary.json`](./results/ttool/expert_alignment/paper_rubric_v5/alignment_summary.json)

Final chosen prompt variant:

- `paper_rubric_v5`

Key agent-side changes kept in the final version:

- streaming fallback for `airouter` JSON responses
- compact precomputed context instead of huge raw dumps
- exact state/block name extraction from parsed artifact payloads
- generic semantic-grounding calibration for behavior models
- generic architecture-grounding calibration plus LLM/heuristic stability blend for architecture-like models
- retry on malformed or unusable LLM JSON

## 2. Reproduction Commands

Full alignment run:

```bash
venv/bin/python project_1_llm_state_machine_modeling/reproduction/align_ttool_expert_review.py \
  --prompt-variant paper_rubric_v5
```

Main outputs:

- Summary: [`alignment_summary.json`](./results/ttool/expert_alignment/paper_rubric_v5/alignment_summary.json)
- Row-level table: [`alignment_reviews.parquet`](./results/ttool/expert_alignment/paper_rubric_v5/alignment_reviews.parquet)
- Per-sample cached request/result payloads: [`cache/`](./results/ttool/expert_alignment/paper_rubric_v5/cache/)

Representative replay command using the exact stored request for one sample:

```bash
PYTHONPATH=project_1_llm_state_machine_modeling/reproduction venv/bin/python - <<'PY'
import json
from pathlib import Path
from expert_review import review_artifacts

payload = json.loads(
    Path(
        "project_1_llm_state_machine_modeling/reproduction/results/ttool/"
        "expert_alignment/paper_rubric_v5/cache/automated_braking__System1__bd.json"
    ).read_text(encoding="utf-8")
)
request = payload["request"]
result = review_artifacts(
    prompt=request["prompt"],
    input_text=request["input_text"],
    pred_output=request["pred_output"],
    ref_output=request["ref_output"],
)
print({
    "overall_score_100": round(result.overall_score * 100, 4),
    "dimension_scores": {item.dimension_name: item.score for item in result.dimension_results},
    "notes": result.notes[:4],
})
PY
```

Another replay command for a low-score state-machine case:

```bash
PYTHONPATH=project_1_llm_state_machine_modeling/reproduction venv/bin/python - <<'PY'
import json
from pathlib import Path
from expert_review import review_artifacts

payload = json.loads(
    Path(
        "project_1_llm_state_machine_modeling/reproduction/results/ttool/"
        "expert_alignment/paper_rubric_v5/cache/platooning__Platoon5__smd.json"
    ).read_text(encoding="utf-8")
)
request = payload["request"]
result = review_artifacts(
    prompt=request["prompt"],
    input_text=request["input_text"],
    pred_output=request["pred_output"],
    ref_output=request["ref_output"],
)
print({
    "overall_score_100": round(result.overall_score * 100, 4),
    "dimension_scores": {item.dimension_name: item.score for item in result.dimension_results},
    "notes": result.notes[:4],
})
PY
```

## 3. Final Metrics

From [`alignment_summary.json`](./results/ttool/expert_alignment/paper_rubric_v5/alignment_summary.json):

| scope | reviews | human_mean | pred_mean | MAE | RMSE | Pearson | Spearman | within_5 | within_10 | within_15 |
|:--|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| overall | 30 | 72.10 | 69.04 | 11.98 | 15.22 | 0.662 | 0.594 | 0.333 | 0.567 | 0.700 |
| bd | 15 | 81.20 | 78.27 | 13.04 | 16.21 | 0.523 | 0.287 | 0.333 | 0.400 | 0.600 |
| smd | 15 | 63.00 | 59.81 | 10.92 | 14.16 | 0.631 | 0.560 | 0.267 | 0.733 | 0.800 |

Per-case average absolute error:

| case_id | avg_absolute_error |
|:--|--:|
| automated_braking | 9.56 |
| platooning | 12.49 |
| space_based_system | 13.89 |

Interpretation:

- `automated_braking` is the best-aligned case family overall.
- `smd` is now materially better than the earlier iterations and ended with lower `MAE` than `bd`.
- The hardest remaining family is `space_based_system`, especially some over-scored block diagrams and under-scored high-quality state machines.

## 4. Full Final Result Table

From [`alignment_reviews.parquet`](./results/ttool/expert_alignment/paper_rubric_v5/alignment_reviews.parquet):

| case_id            | variant_name   | artifact_type   |   human_score_100 |   predicted_score_100 |   absolute_error |
|:-------------------|:---------------|:----------------|------------------:|----------------------:|-----------------:|
| automated_braking  | System1        | bd              |                85 |               87.5077 |           2.5077 |
| automated_braking  | System1        | smd             |                65 |               56      |           9      |
| automated_braking  | System2        | bd              |               100 |               83.2103 |          16.7897 |
| automated_braking  | System2        | smd             |                45 |               73.8    |          28.8    |
| automated_braking  | System3        | bd              |                95 |               86.0466 |           8.9534 |
| automated_braking  | System3        | smd             |                30 |               38.2    |           8.2    |
| automated_braking  | System4        | bd              |                45 |               41.6974 |           3.3026 |
| automated_braking  | System4        | smd             |                30 |               39.6    |           9.6    |
| automated_braking  | System5        | bd              |                90 |               90.4466 |           0.4466 |
| automated_braking  | System5        | smd             |                70 |               62      |           8      |
| platooning         | Platoon1       | bd              |               100 |               89.9    |          10.1    |
| platooning         | Platoon1       | smd             |                85 |               70      |          15      |
| platooning         | Platoon2       | bd              |                75 |               62      |          13      |
| platooning         | Platoon2       | smd             |                75 |               72.2    |           2.8    |
| platooning         | Platoon3       | bd              |                75 |               61      |          14      |
| platooning         | Platoon3       | smd             |                65 |               56      |           9      |
| platooning         | Platoon4       | bd              |                90 |               71.6211 |          18.3789 |
| platooning         | Platoon4       | smd             |                70 |               73.6    |           3.6    |
| platooning         | Platoon5       | bd              |                75 |               43      |          32      |
| platooning         | Platoon5       | smd             |                40 |               47      |           7      |
| space_based_system | System1        | bd              |                88 |               90.125  |           2.125  |
| space_based_system | System1        | smd             |                70 |               70.8    |           0.8    |
| space_based_system | System2        | bd              |                60 |               89.35   |          29.35   |
| space_based_system | System2        | smd             |                75 |               57      |          18      |
| space_based_system | System3        | bd              |                70 |               89.975  |          19.975  |
| space_based_system | System3        | smd             |                65 |               56      |           9      |
| space_based_system | System4        | bd              |                75 |               96.4    |          21.4    |
| space_based_system | System4        | smd             |                70 |               68      |           2      |
| space_based_system | System5        | bd              |                95 |               91.75   |           3.25   |
| space_based_system | System5        | smd             |                90 |               57      |          33      |

## 5. Representative Examples

### Example A: High-Quality Block Diagram Close to Human Score

Cached sample:

- [`automated_braking__System1__bd.json`](./results/ttool/expert_alignment/paper_rubric_v5/cache/automated_braking__System1__bd.json)

Human vs agent:

- Human expert: `85`
- Agent: `87.5077`

Real agent output summary:

```json
{
  "overall_score_100": 87.5077,
  "dimension_scores": {
    "notation_syntax": 0.75,
    "semantic_completeness": 0.65,
    "behavioral_consistency": 0.7,
    "requirement_traceability": 0.68,
    "pragmatic_clarity": 0.65
  },
  "notes": [
    "No reference output was available, so scoring was done directly against the input architecture and requirements.",
    "Assessment prioritized architecture-level adequacy, but explicit safety, security, and timing requirements still had to be traceable to earn higher scores.",
    "Applied generic architecture-grounding boost because the model contains many requirement-grounded block names and explicit interactions.",
    "Applied architecture stability blend: llm_weight=0.25, heuristic_weight=0.75."
  ]
}
```

Why this is aligned:

- The agent gave substantial credit for the core ECU → CSC → communication/broadcast chain.
- It still deducted for missing safety/privacy/timing architecture, which matches the human reviewers’ non-perfect score rather than giving a near-100 score.

### Example B: Weak Block Diagram Close to Human Score

Cached sample:

- [`automated_braking__System4__bd.json`](./results/ttool/expert_alignment/paper_rubric_v5/cache/automated_braking__System4__bd.json)

Human vs agent:

- Human expert: `45`
- Agent: `41.6974`

Real agent output summary:

```json
{
  "overall_score_100": 41.6974,
  "dimension_scores": {
    "notation_syntax": 0.8,
    "semantic_completeness": 0.16,
    "behavioral_consistency": 0.12,
    "requirement_traceability": 0.27,
    "pragmatic_clarity": 0.32
  },
  "notes": [
    "No reference output was available, so scoring is based directly on the input description and the requested architecture-level review task.",
    "High-level architecture credit was given for the presence of several core subsystems, but heavy deductions were applied because the main interaction story is not actually connected in the model.",
    "Applied generic architecture penalty because the model contains many blocks but almost no explicit interactions.",
    "Applied architecture stability blend: llm_weight=0.75, heuristic_weight=0.25."
  ]
}
```

Why this is aligned:

- The agent did not over-punish mere block presence, but it strongly penalized the lack of exchanges.
- That is very close to the human grading pattern for this case.

### Example C: Good State-Machine Set with Moderate Remaining Gap

Cached sample:

- [`platooning__Platoon1__smd.json`](./results/ttool/expert_alignment/paper_rubric_v5/cache/platooning__Platoon1__smd.json)

Human vs agent:

- Human expert: `85`
- Agent: `70`

Real agent output summary:

```json
{
  "overall_score_100": 70.0,
  "dimension_scores": {
    "notation_syntax": 0.78,
    "semantic_completeness": 0.74,
    "behavioral_consistency": 0.68,
    "requirement_traceability": 0.73,
    "pragmatic_clarity": 0.57
  },
  "notes": [
    "No reference model was available, so scoring is against the input requirements only.",
    "The advanced platoon-splitting feature appears optional from the wording; it was not treated as a primary missing behavior driver.",
    "Applied generic semantic-grounding boost because the model contains many domain-specific state names and comparatively few placeholder states."
  ]
}
```

Why this is only partially aligned:

- The agent correctly recognized this as a clearly stronger-than-average behavior model.
- It still stayed below the human score because it kept deducting for under-modeled causal details and weaker guard/timing logic.

### Example D: Low-Quality State-Machine Set Pulled Down After Final Fixes

Cached sample:

- [`platooning__Platoon5__smd.json`](./results/ttool/expert_alignment/paper_rubric_v5/cache/platooning__Platoon5__smd.json)

Human vs agent:

- Human expert: `40`
- Agent: `47`

Real agent output summary:

```json
{
  "overall_score_100": 47.0,
  "dimension_scores": {
    "notation_syntax": 0.79,
    "semantic_completeness": 0.41,
    "behavioral_consistency": 0.36,
    "requirement_traceability": 0.48,
    "pragmatic_clarity": 0.63
  },
  "notes": [
    "No reference model was available, so scoring is a standalone expert review against the textual requirements.",
    "Timing details were not treated as syntax issues, but their absence still reduces completeness and traceability because they are explicitly required behavior here."
  ]
}
```

Why this improved over earlier iterations:

- Earlier versions over-scored this case because they were misled by polluted pseudo-state extraction.
- After switching to exact parsed state-name extraction, the agent treated it as a shallow behavior model instead of a rich one.

## 6. What Worked

- `airouter` streaming fallback removed empty-response failures and made LLM-first review stable enough for repeated runs.
- Compact review context prevented the earlier giant-prompt failure mode.
- Exact state/block name extraction fixed false semantic boosts caused by generic text scraping.
- Generic behavior-model calibration improved high-vs-low separation for `smd`.
- Generic architecture calibration plus LLM/heuristic blending greatly improved `bd` alignment, especially for obviously good and obviously weak block diagrams.

## 7. Remaining Gaps

Largest remaining errors:

- `space_based_system / System5 / smd`: human `90`, agent `57`
- `space_based_system / System2 / bd`: human `60`, agent `89.35`
- `space_based_system / System4 / bd`: human `75`, agent `96.4`
- `platooning / Platoon5 / bd`: human `75`, agent `43`
- `automated_braking / System2 / smd`: human `45`, agent `73.8`

Observed failure modes:

- Some `space_based_system` block diagrams still get over-rewarded for architecture coverage even when the human graders were more conservative.
- Some strong `space_based_system` state-machine sets are still under-scored because the agent keeps treating missing detailed behavioral evidence as more important than the human experts did.
- `automated_braking / System2 / smd` remains a persistent false positive.

Practical conclusion:

- The current version is no longer a naive over-scoring reviewer.
- For `automated_braking` it is already strongly aligned.
- For `platooning` it is reasonably aligned with some remaining behavior-side conservatism.
- For `space_based_system` it is usable but not yet as tightly aligned as the other two families.

## 8. Final File Pointers

- Final summary: [`alignment_summary.json`](./results/ttool/expert_alignment/paper_rubric_v5/alignment_summary.json)
- Final row table: [`alignment_reviews.parquet`](./results/ttool/expert_alignment/paper_rubric_v5/alignment_reviews.parquet)
- Final per-sample caches: [`cache/`](./results/ttool/expert_alignment/paper_rubric_v5/cache/)
- Alignment runner: [`align_ttool_expert_review.py`](./align_ttool_expert_review.py)
- Standalone agent: [`expert_review/expert_review_agent.py`](./expert_review/expert_review_agent.py)
