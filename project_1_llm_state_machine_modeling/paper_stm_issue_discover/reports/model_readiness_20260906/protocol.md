# Model access and serving measurement protocol

Registered: 2026-09-06. Research boundary: #179 E1. This protocol measures inference infrastructure and compatibility, not Paper1 discovery effectiveness. Formal baseline/ours comparisons belong to E2. Model selection remains open until the survey and measurements are reviewed.

## Questions And Evidence

1. Which current commercial and sub-100B-total open models provide relevant, sourced public evidence for requirement interpretation, source grounding, logical/code reasoning and structured output?
2. Which interfaces work through the unmodified `utils.llm` profile registry and model factory? Which official LangChain integrations would require future implementation?
3. Can recommended open models be served on the allocated hardware, forwarded locally, and sustain declared concurrent request loads with usable structured outputs?

The primary public benchmark dimensions are instruction/constraint following, long-context understanding and retrieval, coding/reasoning, tool argument accuracy, and hallucination/factuality where reported. Exact benchmark editions, task definitions, inference budgets, harnesses and source dates accompany each number. A missing value stays missing. Agentic repository-repair scores are indirect proxies, not measurements of state-machine defect discovery. A single overall leaderboard score cannot decide the selection.

## Candidate And Search Policy

Commercial coverage includes the user-requested Luna, Gemini Flash candidates, Sonnet and latest Haiku. Open coverage includes at least five current strong models from official publishers; the cutoff is total parameters below 100B, with active parameters reported separately. Official weight variants and licenses are identified explicitly. The attempted deployment shortlist is chosen from this survey before using any formal Paper1 outcome. Model substitutions and their reasons must be recorded before that model's probes.

Recent LLM4SE paper window: 2026-03-06 through 2026-09-06 inclusive. Search arXiv and bibliographic sources for software engineering, program analysis, requirements, testing, verification, model/state-machine analysis and LLM evaluations. Record queries, dates, screening/exclusion reasons and deduplicated paper identifiers. Extract actually evaluated models and their roles from the paper, not from abstracts or related-work mentions. Frequencies use the included, examined papers as denominator; the sample is not claimed to represent all LLM4SE publications.

## Remote And Privacy Boundaries

Use only the allocated four H200 devices, indexed 0-3. Preserve devices 4-7, existing tmux work areas 0/1 and other remote sessions. Downloads, installation and serving execute visibly in newly allocated areas numbered 2 or higher of the designated tmux session. Weights, data, caches and environments reside on the designated shared storage. Servers bind to remote loopback and are accessed via local SSH forwarding. Inventory precedes mutation; existing processes are never stopped to free resources.

All publishable commands use `REMOTE_NODE`, `SHARED_STORAGE`, `LOCAL_ENDPOINT` and credential placeholders. No supplied private URL, node address, credential, personal username or private absolute path is published. Private configuration remains permission-restricted and untracked. Original probe evidence is sanitized before tracked artifacts are produced. Official public-source URLs are retained.

## Measurements

- Record model ID and weight revision, total/active parameters, weight format, serving engine/version, tokenizer/chat template, generation/thinking controls, context/output limits, tensor parallelism, GPU allocation, startup result and peak allocated memory where available.
- API probes exercise ordinary generation, schema/JSON output, streaming with usage, and tool arguments where applicable. Record requested and response model IDs separately; a gateway echo is not independent proof of upstream model identity.
- Exercise the current profile registry and factory, then isolated official native adapters where accessible. Production adapter/method source and pinned dependencies are not edited. Unsupported features remain documented failures.
- Smoke uses one fixed synthetic state-machine issue task and one existing non-ledger method input selected before inference. Each final recommended profile is attempted through minimal baseline and current-method paths. Preserve transport failures, schema errors, internal degradation, prompts, raw responses, usage and outcomes; do not score against the defect ledger or tune on historical answers.
- Serving load: warm up each configuration, then test concurrency 1, 2, 4 and 8, with at least twice as many requests as the concurrency level. Use a fixed approximately 2K-token task-relevant prompt and 256-token output cap for the comparable capacity sweep. Record actual input/output tokens because tokenizers differ. Follow with a longer approximately 16K-token structured-input probe at concurrency 1 and 4 where supported. Identify any actual deviations explicitly.
- Report successful/failed request counts, batch wall time, aggregate output tokens/s, requests/s, per-request latency distribution, time to first token and inter-token latency where streaming permits. Report finish reasons, truncation and schema/task validity separately. Throughput counts generated tokens, including exposed reasoning where supplied, with the accounting rule stated.
- Distinguish cold startup, warmup and steady-state timings. Preserve individual observations. A short sweep estimates tested capacity; it does not establish a production SLO or maximum safe concurrency. OOM, unsupported architecture, dependency, network and timeout failures are retained.
- The probe task is: requirements say a pump may start only with the safety interlock closed, and must stop on an emergency event; the supplied transition starts on `start` without the interlock guard. Return JSON containing `issue`, `source_transition`, `missing_guard`, and `counterexample`. The expected example is deterministic and never enters Paper1's formal results.

## Acceptance And Handoff

Deliver sourced comparison tables, dated literature evidence, adapter capability results, deployment attempts and measurements, a role-anonymized advisor talk, and a 2+2 recommendation with exact configuration references. Every recommended open model must have an attempted deployment and recorded load-test outcome. Distinguish verified, failed and untested paths. Successful API health checks alone do not establish method compatibility. Unresolved blockers remain visible in E1 and constrain E2; no E2 or O2 run begins here.

Before publishing: inspect every tracked artifact for secrets, supplied private endpoints, node addresses, private paths and participant usernames; verify numerical aggregates against raw observations and trace source links. Run checks appropriate to changed documents and evidence. A1/A2 remain Luna-only and historical v61 records remain frozen.
