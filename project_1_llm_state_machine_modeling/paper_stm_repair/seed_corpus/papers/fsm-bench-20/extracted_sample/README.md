# FSM-Bench-20 — Local LLM FSM Benchmark

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20516296.svg)](https://doi.org/10.5281/zenodo.20516296)

Reproducible benchmark for evaluating **open-source large language models** on **deterministic finite state machine (FSM)** generation from natural-language requirements using local [Ollama](https://ollama.com) inference.

No paid cloud APIs are required.

---

## Project overview

**FSM-Bench-20** packages twenty software-domain requirement sets, a fixed FSM JSON schema, frozen prompt specifications, automated validators, and an experiment driver for local model comparison.

The repository is the implementation companion to the IST journal submission *FSM-Bench-20: A Reproducible Benchmark for Deterministic Finite State Machine Generation from Natural-Language Requirements Using Local Open-Source LLMs*.

| Item | Value |
|------|-------|
| Benchmark systems | 20 |
| Requirements per system | 12–13 numbered, testable statements |
| Models (campaign) | 6 mandatory + 1 optional (Ollama) |
| Inference | Local only; temperature 0.0; structured JSON output |
| Archived artifact | [10.5281/zenodo.20516296](https://doi.org/10.5281/zenodo.20516296) |

---

## FSM-Bench-20 benchmark

Each system specifies behaviour in English using identifiers `R1`, `R2`, … Models must emit a single JSON object conforming to the FSM schema (states, events, transitions with guards, actions, and requirement references).

Evaluation uses nested quality gates:

| Gate | Criterion |
|------|-----------|
| **G1** | Valid JSON |
| **G2** | Schema-valid FSM with referential closure |
| **G3** | Nested determinism — unique `(source, event)` pairs among G2 passers |

Additional metrics include requirement citation coverage, unsupported/inferred transitions, reachability, and structural size.

See `docs/evaluation_protocol.md` and `docs/dataset.md` for full definitions.

---

## Final benchmark campaign

The **publication freeze** completed **140/140** planned runs (seven models × twenty systems):

| Field | Value |
|-------|-------|
| Manifest run ID | `20260602T195520Z` |
| Finalized (UTC) | `2026-06-02T21:02:56` |
| Structured output | Enabled for all runs |
| Campaign total | 140 runs |

**Frozen headline metrics** (descriptive; do not modify without a new campaign):

| Metric | Rate | Count |
|--------|------|-------|
| G1 — Valid JSON | 98.6% | 138/140 |
| G2 — Schema-valid FSM | 78.6% | 110/140 |
| G3 — Nested deterministic FSM | 31.4% | 44/140 |
| Mean requirement coverage | 69.2% | — |

Run-level outputs (`results/`, `outputs/`, diagnostic `figures/`) are **gitignored** and regeneratable. The v1.0.0 release documents the frozen protocol and metrics; campaign artifacts will be archived on Zenodo in a versioned record associated with the article.

---

## Reproducibility

1. Clone this repository and install Python 3.12+ and Ollama.
2. Pull the model tags listed in `scripts/fsm_benchmark/config.py`.
3. Create local prompt files from `docs/experimental_prompts.md` (prompts are gitignored by policy).
4. Run `./run_all.sh` or the step-by-step commands in `REPRODUCIBILITY.md`.
5. Compare regenerated `results/metrics.csv` against the frozen statistics above.

Full instructions: [`REPRODUCIBILITY.md`](REPRODUCIBILITY.md)

Pre-flight checks:

```bash
python3.12 scripts/validate_integrity.py
python3.12 scripts/check_models.py
```

---

## Repository structure

```text
.
├── dataset/                 # FSM-Bench-20 requirement sets (versioned)
├── benchmark/               # Catalog and gold FSM placeholders
├── docs/                    # Protocol, prompts spec, policies
├── scripts/
│   ├── run_experiment.py    # Generation driver
│   ├── evaluate.py          # Metrics aggregation
│   ├── plot_results.py      # Diagnostic plots (gitignored output)
│   └── fsm_benchmark/       # Core library
├── outputs/                 # Raw/cleaned model outputs (gitignored)
├── results/                 # metrics.csv, manifest, details (gitignored)
├── figures/                 # Diagnostic plots (gitignored)
├── run_all.sh               # End-to-end pipeline
├── REPRODUCIBILITY.md
├── RELEASE_NOTES.md
├── CITATION.cff
└── LICENSE
```

---

## Quick start

```bash
git clone https://github.com/cesar-andress/llm-fsm-local-benchmark.git
cd llm-fsm-local-benchmark

python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

ollama serve   # separate terminal
python3.12 scripts/check_models.py

mkdir -p prompts
# Copy prompt templates per REPRODUCIBILITY.md §5

./run_all.sh
```

Pilot run:

```bash
python3.12 scripts/run_experiment.py \
  --models llama3.1:8b \
  --systems vending_machine atm
```

---

## Citation

If you use this benchmark, cite the Zenodo record and the accompanying paper:

- **DOI:** [10.5281/zenodo.20516296](https://doi.org/10.5281/zenodo.20516296)
- **Metadata:** [`CITATION.cff`](CITATION.cff)

```bibtex
@software{fsm_bench_20_2026,
  author    = {S{\'a}nchez, C{\'e}sar Andr{\'e}s},
  title     = {{FSM-Bench-20}: Local {LLM} Benchmark for Deterministic {FSM} Generation},
  year      = {2026},
  doi       = {10.5281/zenodo.20516296},
  url       = {https://doi.org/10.5281/zenodo.20516296}
}
```

---

## Release history

| Version | Date | Notes |
|---------|------|-------|
| **v1.0.0** | 2026-06-02 | First publication release — 140-run campaign freeze (`20260602T195520Z`) |
| v0.3.0 | 2026-06-02 | Repository hygiene and validation safeguards |
| v0.2.0 | 2026-06-02 | Expanded documentation and policies |
| v0.1.0 | 2026-06-02 | Initial public dataset and experiment framework |

See [`RELEASE_NOTES.md`](RELEASE_NOTES.md) for v1.0.0 scope and artifacts.

---

## Release v1.0.0

**FSM-Bench-20 publication release** used in the *Information and Software Technology* submission.

This tag marks the first archival-quality release of the benchmark **implementation** and documentation:

| Component | Location |
|-----------|----------|
| Benchmark dataset (20 systems) | `dataset/` |
| Prompt specification | `docs/experimental_prompts.md` |
| FSM JSON schema | `scripts/fsm_benchmark/schema.py` |
| Evaluation scripts | `scripts/evaluate.py`, `scripts/fsm_benchmark/` |
| Experiment driver | `scripts/run_experiment.py`, `run_all.sh` |
| Reproducibility guide | `REPRODUCIBILITY.md` |
| Evaluation protocol | `docs/evaluation_protocol.md` |

**Not included in git** (regeneratable; excluded by `.gitignore`):

- `results/` — campaign metrics and per-run details
- `outputs/` — raw and cleaned model JSON
- `figures/` — diagnostic plots

Campaign outputs for the 140-run freeze will be published in a versioned Zenodo record associated with the article. The frozen metrics in this README match manifest `20260602T195520Z`.

---

## Documentation index

| Document | Description |
|----------|-------------|
| `REPRODUCIBILITY.md` | Full reproduction guide |
| `RELEASE_NOTES.md` | v1.0.0 release notes |
| `docs/evaluation_protocol.md` | Research questions and metrics |
| `docs/experimental_prompts.md` | Formal prompt specification |
| `docs/dataset.md` | Dataset schema and catalog |
| `docs/PROJECT_RULES.md` | Repository conventions |
| `docs/RESEARCH_REPOSITORY_POLICY.md` | Artifact placement policy |

---

## License

MIT — see [`LICENSE`](LICENSE). Verify individual model licenses on Ollama before redistributing model weights or derived outputs.
