# `method.handoff_smoke`

PR-3 Path1/Path2 handoff smoke package.

- Runner: [`runner.py`](./runner.py)
- Path1 config: [`configs/path1_representative.json`](./configs/path1_representative.json)
- Path2 config: [`configs/path2_representative.json`](./configs/path2_representative.json)
- Handoff guide: [`docs/PR3_HANDOFF_SMOKE.md`](./docs/PR3_HANDOFF_SMOKE.md)

Run from repository root:

```bash
source .env
PYTHONPATH=project_1_llm_state_machine_modeling \
  venv/bin/python -m method.handoff_smoke.runner --real-llm \
  --out runs/pr3_handoff_smoke \
  --summary runs/pr3_handoff_smoke/summary.json \
  --max-retries 2
```

Real LLM review stages use bounded retry for provider/network errors and invalid JSON/schema output; all attempts are persisted in the run record. This is an infrastructure compatibility smoke only; it does not compute formal Path1/Path2 experiment metrics.
