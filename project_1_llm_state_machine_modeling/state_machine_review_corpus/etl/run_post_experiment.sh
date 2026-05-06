#!/usr/bin/env bash
# Post-experiment pipeline: analyze → chart → upload → assemble PR comment.
set -euo pipefail

cd "$(dirname "$0")/.."

# 1) Compute alignment metrics
python3 etl/compute_alignment_metrics.py \
  --baseline etl/out/experiment_baseline_result.jsonl \
  --new etl/out/experiment_new_result.jsonl \
  --output-json etl/out/experiment_alignment.json

# 2) Build charts
python3 etl/build_experiment_charts.py
python3 etl/build_dimension_charts.py

# 3) Upload charts (returns 5 ![filename](URL) lines per success)
cd etl/out/charts
GH_SESSION_TOKEN="${GH_SESSION_TOKEN:?GH_SESSION_TOKEN required}" \
  GH_TOKEN="$(gh auth token --user HansBug)" \
  gh image upload \
    10_score_distribution.png \
    11_alignment_scatter.png \
    12_judgement_triage.png \
    13_per_paper.png \
    14_dimension_comparison.png \
    15_proxy_metrics.png \
    16_psmbench_ranking_crosscheck.png \
  > /tmp/uploaded_chart_urls.txt 2>&1 || true

# 4) Build image-URL JSON map from upload output
python3 - <<'PY'
import json, re, pathlib
text = pathlib.Path("/tmp/uploaded_chart_urls.txt").read_text()
m = re.findall(r"!\[([^\]]+)\]\(([^)]+)\)", text)
mapping = dict(m)
out = pathlib.Path("/home/zhangshaoang/oo-projects/research_ideas/project_1_llm_state_machine_modeling/state_machine_review_corpus/etl/out/chart_urls.json")
out.write_text(json.dumps(mapping, indent=2))
print("chart URLs:", json.dumps(mapping, indent=2))
PY

# 5) Assemble PR comment
cd /home/zhangshaoang/oo-projects/research_ideas/project_1_llm_state_machine_modeling/state_machine_review_corpus
python3 etl/assemble_pr_comment.py \
  --alignment-json etl/out/experiment_alignment.json \
  --images-json etl/out/chart_urls.json \
  --commit-sha "${COMMIT_SHA:-TBD}" \
  --output /tmp/pr_comment_reviewer_experiment.md

echo "==== PR COMMENT READY: /tmp/pr_comment_reviewer_experiment.md ===="
wc -l /tmp/pr_comment_reviewer_experiment.md
