#!/usr/bin/env python3
"""Full validation of a pyfcstm DSL: parse + sem + sim (smoke) + scenarios.

Usage:  verify_pyfcstm_full.py <path.fcstm> [<scenarios.json>]

Stages:
  1. parse_with_grammar_entry → PARSE_OK
  2. parse_dsl_node_to_state_machine → SEM_OK
  3. SimulationRuntime + cycle() smoke → SIM_OK
  4. (if scenarios.json provided) execute each TestScenario → SCENARIOS_OK / SCENARIOS_FAIL

scenarios.json format (matches method.schema.TestScenario):

  {
    "scenarios": [
      {
        "name": "...",
        "description": "...",
        "initial_state": null | "Path.To.State",
        "initial_vars": {},
        "steps": [
          {"before_cycles": 0, "events": [...]|null, "expected_state": "...", "expected_vars": {...}, "name": "..."}
        ]
      }
    ]
  }

Exit codes:
  0  ALL_OK (all stages including scenarios passed)
  1  PARSE_FAIL
  2  SEM_FAIL
  3  SIM_FAIL (smoke)
  4  SCENARIOS_FAIL (≥1 scenario failed)
  5  scenarios.json missing/invalid
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

if len(sys.argv) < 2:
    print("usage: verify_pyfcstm_full.py <path.fcstm> [<scenarios.json>]", file=sys.stderr)
    sys.exit(99)

fcstm_path = Path(sys.argv[1])
scenarios_path = Path(sys.argv[2]) if len(sys.argv) >= 3 else None

if not fcstm_path.exists():
    print(f"FILE_NOT_FOUND: {fcstm_path}", file=sys.stderr)
    sys.exit(98)

src = fcstm_path.read_text()

# Stage 1: parse
try:
    from pyfcstm.dsl import parse_with_grammar_entry
    ast = parse_with_grammar_entry(src, "state_machine_dsl")
    print("PARSE_OK")
except Exception as e:
    print(f"PARSE_FAIL: {type(e).__name__}: {str(e)[:500]}")
    sys.exit(1)

# Stage 2: semantic
try:
    from pyfcstm.model import parse_dsl_node_to_state_machine
    sm = parse_dsl_node_to_state_machine(ast)
    state_count = "?"
    try:
        state_count = len(list(sm.iter_leaf_states()))
    except Exception:
        pass
    print(f"SEM_OK (leaf_states={state_count})")
except Exception as e:
    print(f"SEM_FAIL: {type(e).__name__}: {str(e)[:500]}")
    sys.exit(2)

# Stage 3: simulation smoke (1 cycle)
try:
    from pyfcstm.simulate import SimulationRuntime
    rt = SimulationRuntime(sm, abstract_error_mode="log")
    rt.cycle(events=[])
    cs_name = getattr(rt.current_state, "name", str(rt.current_state))
    print(f"SIM_OK (current_state={cs_name})")
except Exception as e:
    print(f"SIM_FAIL: {type(e).__name__}: {str(e)[:500]}")
    sys.exit(3)

# Stage 4: scenarios (if provided)
if scenarios_path is None:
    print("ALL_OK (smoke-only — no scenarios provided)")
    sys.exit(0)

if not scenarios_path.exists():
    print(f"SCENARIOS_NOT_FOUND: {scenarios_path}", file=sys.stderr)
    sys.exit(5)

try:
    payload = json.loads(scenarios_path.read_text())
    scenarios_raw = payload.get("scenarios", [])
    if not isinstance(scenarios_raw, list) or len(scenarios_raw) == 0:
        print("SCENARIOS_EMPTY: must contain >=1 scenario", file=sys.stderr)
        sys.exit(5)
except Exception as e:
    print(f"SCENARIOS_JSON_FAIL: {e}", file=sys.stderr)
    sys.exit(5)

# Load TestScenario + run via existing infra
try:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent.parent))
    from method.schema import TestScenario, ScenarioStep
    from method.feedback.sim import _run_one_scenario
except Exception as e:
    print(f"IMPORT_FAIL: {e}", file=sys.stderr)
    sys.exit(5)


def to_scenario(d: dict) -> TestScenario:
    steps = []
    for s in d.get("steps", []):
        steps.append(ScenarioStep(
            before_cycles=int(s.get("before_cycles", 0)),
            events=s.get("events", None),
            expected_state=s.get("expected_state", None),
            expected_vars=s.get("expected_vars", None) or None,
            name=s.get("name", "") or "",
        ))
    return TestScenario(
        name=d.get("name", "") or "",
        description=d.get("description", "") or "",
        initial_state=d.get("initial_state", None),
        initial_vars=d.get("initial_vars", {}) or {},
        steps=steps,
    )


scenarios = [to_scenario(d) for d in scenarios_raw]
print(f"SCENARIOS_LOADED: {len(scenarios)}")

n_pass = 0
n_fail = 0
n_error = 0
failures = []
for sc in scenarios:
    # Re-parse model per scenario (hot-start may mutate runtime state)
    sm_fresh = parse_dsl_node_to_state_machine(parse_with_grammar_entry(src, "state_machine_dsl"))
    result = _run_one_scenario(sm_fresh, sc)
    if result.status == "pass":
        n_pass += 1
        print(f"  ✓ [{sc.name or '<unnamed>'}]")
    elif result.status == "fail":
        n_fail += 1
        bad = [sr for sr in result.step_results if sr.status != "pass"]
        bad_msgs = []
        for sr in bad:
            mismatch = []
            if hasattr(sr, "state_mismatch") and sr.state_mismatch:
                mismatch.append(f"state: expected={sr.state_mismatch.get('expected')}, got={sr.state_mismatch.get('actual')}")
            if hasattr(sr, "var_mismatches") and sr.var_mismatches:
                mismatch.append(f"vars: {sr.var_mismatches}")
            bad_msgs.append(f"step[{sr.step_index}]({sr.step_name}): {'; '.join(mismatch) if mismatch else 'fail'}")
        failures.append({"scenario": sc.name, "bad_steps": bad_msgs})
        print(f"  ✗ [{sc.name or '<unnamed>'}]: {'; '.join(bad_msgs)[:400]}")
    else:
        n_error += 1
        err = result.setup_error or (result.step_results[-1].runtime_error if result.step_results else "unknown")
        failures.append({"scenario": sc.name, "error": str(err)[:300]})
        print(f"  ⚠ [{sc.name or '<unnamed>'}]: ERROR {str(err)[:200]}")

print()
print(f"SCENARIOS_SUMMARY: pass={n_pass} fail={n_fail} error={n_error} total={len(scenarios)}")

if n_fail > 0 or n_error > 0:
    print("SCENARIOS_FAIL")
    print(json.dumps({"failures": failures}, ensure_ascii=False, indent=2))
    sys.exit(4)

# Stage 5: lint (IDE-equivalent warnings — 0 warning gate)
print()
print("LINT_RUNNING...")
import subprocess
lint_path = Path(__file__).resolve().parent / "lint_pyfcstm.py"
lint_proc = subprocess.run(
    [sys.executable, str(lint_path), str(fcstm_path)],
    capture_output=True, text=True, check=False,
)
lint_stdout = lint_proc.stdout
try:
    lint_report = json.loads(lint_stdout)
    n_warns = lint_report.get("total", 0)
    by_code = lint_report.get("by_code", {})
except Exception:
    n_warns = -1
    by_code = {}
    print(f"LINT_FAIL: cannot parse lint output\n{lint_stdout[:500]}", file=sys.stderr)
    sys.exit(6)

print(f"LINT_SUMMARY: warnings={n_warns} by_code={by_code}")
if n_warns > 0:
    print("LINT_FAIL (warnings present — must be 0 for ALL_OK)")
    # Print up to 10 warnings inline for codex to see
    for w in lint_report.get("warnings", [])[:10]:
        print(f"  [{w['code']}] {w.get('message','')}")
    if len(lint_report.get("warnings", [])) > 10:
        print(f"  ... and {len(lint_report['warnings']) - 10} more")
    sys.exit(5)

print("ALL_OK")
sys.exit(0)
