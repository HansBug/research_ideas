# `archive.agent_loop_method.handoff_smoke`

> **LG-M1-F provenance note（2026-06-08）**：本目录是 historical PR-3 handoff smoke artifact，用于证明 Path1/Path2 当时能接入 agent-loop infrastructure。下面的 `source .env` / `--real-llm` 命令只适用于显式 handoff smoke 或后续真实 provider 验证；它不是 LG-M1-F docs/provenance gate，也不代表当前 tests-only 验收需要 provider。当前推荐 method 入口见 [../README.md](../README.md)。

PR-3 Path1/Path2 handoff smoke package.

- Runner: [`runner.py`](./runner.py)
- Path1 config: [`configs/path1_representative.json`](./configs/path1_representative.json)
- Path2 config: [`configs/path2_representative.json`](./configs/path2_representative.json)
- Handoff guide: [`docs/PR3_HANDOFF_SMOKE.md`](./docs/PR3_HANDOFF_SMOKE.md)

Run from repository root:

```bash
source .env
PYTHONPATH=project_1_llm_state_machine_modeling \
  venv/bin/python -m archive.agent_loop_method.handoff_smoke.runner --real-llm \
  --out runs/pr3_handoff_smoke \
  --summary runs/pr3_handoff_smoke/summary.json \
  --max-retries 2
```

Real LLM review stages use bounded retry for provider/network errors and invalid JSON/schema output; all attempts are persisted in the run record. This is an infrastructure compatibility smoke only; it does not compute formal Path1/Path2 experiment metrics.
