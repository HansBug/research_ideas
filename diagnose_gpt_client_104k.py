#!/usr/bin/env python3
"""Direct 104k prompt diagnostic through ``method.gpt_client.chat``.

Run from repository root:

    python diagnose_gpt_client_104k.py

The script intentionally calls the repository's bottom LLM component
``method.gpt_client.chat`` directly, without running agent-loop stages.  It
constructs a SL-5-like request with roughly the same shape as the previously
observed largest provider-5xx request:

- system message: about 23.6k chars
- user message: about 80.4k chars
- total: 104,000 chars by default
- ``response_format={"type": "json_object"}``
- ``max_tokens=None``

For convenience, it loads repo-root ``.env`` into ``os.environ`` before calling
``gpt_client.py``.  The called component itself still reads only process env.
Secrets are never printed; only a short SHA-256 fingerprint of ``LLM_API_KEY``
is displayed.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import time
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = REPO_ROOT / "project_1_llm_state_machine_modeling"


def _load_dotenv(path: Path) -> None:
    """Small .env loader supporting ``export KEY=value`` lines.

    This is deliberately local to the diagnostic script.  It does not change
    ``method.gpt_client``'s contract: the actual LLM component reads
    ``os.environ`` only.
    """

    if not path.exists():
        return
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[len("export ") :].strip()
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip("'").strip('"')
        if key:
            os.environ[key] = value


def _build_messages(target_total_chars: int) -> list[dict[str, str]]:
    """Build a SL-5-like prompt with an exact total character budget."""

    base_system = """
You are SL-5 ScenarioGen for the project-1 agent loop.
Template version: sl5-scenario-generation.v2.
Goal: generate grounded multi-step TestScenario candidates before ScenarioSet freeze.
Output strict JSON with a top-level `scenarios` list. Do not change the DSL.
Use NL + current DSL + inspect JSON + design summary + GroundingMap.
Respect pyfcstm simulation semantics and use before_cycles for default init.
Avoid over-asserting weak or incidental variables.
""".strip()
    system = base_system + (
        "\nScenario generation rule: output JSON only; preserve grounded probes; cover transitions."
        * 260
    )

    nl = "Controller has many states/events/variables; generate grounded test scenarios."
    current_dsl = (
        "state Root { [*] -> S0; "
        + " ".join(f"state S{i}; S{i} -> S{i + 1} :: E{i};" for i in range(25))
        + " state S26; }"
    )
    inspect_json = {
        "root_state_path": "Root",
        "states": [
            {"path": f"Root.S{i}", "children": [], "note": "s" * 100}
            for i in range(30)
        ],
        "transitions": [
            {
                "source": f"Root.S{i}",
                "target": f"Root.S{i + 1}",
                "event": f"E{i}",
                "guard": "x > 0 " * 20,
                "action": "out = out + 1; " * 10,
            }
            for i in range(25)
        ],
        "variables": [
            {"name": f"v{i}", "type": "float", "dataflow": "v" * 80}
            for i in range(30)
        ],
        "events": [{"name": f"E{i}", "detail": "e" * 80} for i in range(30)],
        "actions": [{"state": f"Root.S{i}", "text": "a" * 80} for i in range(30)],
        "diagnostics": [
            {
                "code": "W_X",
                "severity": "warning",
                "message": "m" * 220,
                "refs": {"state": f"Root.S{i % 25}"},
            }
            for i in range(25)
        ],
        "metrics": {"state_count": 30, "transition_count": 25},
        "var_dataflow": {"large": "v" * 6000},
        "reachability_graph": {"large": "r" * 6000},
        "action_ref_graph": {"large": "a" * 4000},
    }
    design_summary = {
        "ok": True,
        "blocking_items": [],
        "advisory_items": [
            {"code": "W_X", "message": "d" * 260, "refs": {"i": i}}
            for i in range(20)
        ],
        "context": "c" * 4000,
    }
    grounding_map = {
        "elements": [
            {
                "element_id": f"state:S{i}",
                "element_kind": "state",
                "element_ref": f"Root.S{i}",
                "source_stage": "SL-1",
                "evidence_text": "state evidence",
                "requiredness": "required",
                "confidence": 0.9,
            }
            for i in range(30)
        ]
    }
    payload = {
        "nl": nl,
        "current_dsl": current_dsl,
        "inspect_json": inspect_json,
        "design_summary": design_summary,
        "grounding_map": grounding_map,
        "coverage_directive": None,
        "previous_scenarios": [],
    }
    user_prefix = (
        "## SL-5 input bundle\n```json\n"
        + json.dumps(payload, ensure_ascii=False, indent=2)
        + "\n```\n\n## DSL under test\n```pyfcstm\n"
        + current_dsl
        + "\n```\n\nGenerate TestScenario candidates. Output JSON only."
    )

    system_len = len(system)
    if system_len >= target_total_chars:
        raise ValueError(
            f"target_total_chars={target_total_chars} is too small; system alone is {system_len}"
        )
    required_user_len = target_total_chars - system_len
    if len(user_prefix) > required_user_len:
        user = user_prefix[:required_user_len]
    else:
        filler = "\nextra evidence line for 104k reproduction."
        user = user_prefix + filler * ((required_user_len - len(user_prefix)) // len(filler) + 1)
        user = user[:required_user_len]

    return [{"role": "system", "content": system}, {"role": "user", "content": user}]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--env-file", default=".env", help="dotenv file to load before calling gpt_client")
    parser.add_argument("--no-env-file", action="store_true", help="do not load .env; use existing process env only")
    parser.add_argument("--target-chars", type=int, default=104_000, help="total message chars to construct")
    parser.add_argument("--dry-run", action="store_true", help="print request metadata without sending the LLM request")
    args = parser.parse_args()

    if not args.no_env_file:
        _load_dotenv(REPO_ROOT / args.env_file)

    sys.path.insert(0, str(PROJECT_ROOT))
    from method.gpt_client import chat  # noqa: PLC0415

    messages = _build_messages(args.target_chars)
    key = os.environ.get("LLM_API_KEY", "")
    metadata = {
        "endpoint": os.environ.get("LLM_ENDPOINT"),
        "model": os.environ.get("LLM_MODEL"),
        "key_sha12": hashlib.sha256(key.encode()).hexdigest()[:12] if key else "",
        "lens": [len(message["content"]) for message in messages],
        "total_chars": sum(len(message["content"]) for message in messages),
        "response_format": {"type": "json_object"},
        "max_tokens": None,
    }
    print(metadata, flush=True)

    if args.dry_run:
        print("DRY_RUN: request not sent", flush=True)
        return 0

    started = time.time()
    try:
        content, usage = chat(
            messages=messages,
            temperature=0.0,
            response_format={"type": "json_object"},
            max_tokens=None,
        )
    except Exception as exc:  # noqa: BLE001 - diagnostic script prints provider error verbatim
        print(
            "ERR",
            "elapsed",
            round(time.time() - started, 2),
            type(exc).__name__,
            str(exc)[:3000],
            flush=True,
        )
        return 1

    print(
        "OK",
        "elapsed",
        round(time.time() - started, 2),
        "usage",
        usage,
        "out_chars",
        len(content),
        flush=True,
    )
    print("content_head", content[:1000].replace("\n", " "), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
