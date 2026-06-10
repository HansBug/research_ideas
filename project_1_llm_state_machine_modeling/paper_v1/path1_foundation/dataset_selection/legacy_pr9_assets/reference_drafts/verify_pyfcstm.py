#!/usr/bin/env python3
"""Validate a pyfcstm DSL file: parse → sem → sim → static analysis.

Usage:  verify_pyfcstm.py <path.fcstm> [--no-static]

Output (single line per stage; exit code reflects last failure):
  PARSE_OK
  SEM_OK
  SIM_OK
  STATIC_OK (or full STATIC report on failure)
  ALL_OK (final line on full pass)

On failure:
  PARSE_FAIL: <error>     (exit 1)
  SEM_FAIL: <error>       (exit 2)
  SIM_FAIL: <error>       (exit 3)
  STATIC_FAIL: see report (exit 4) — logical dead-code detected
"""
import sys
from pathlib import Path

if len(sys.argv) < 2 or len(sys.argv) > 3:
    print("usage: verify_pyfcstm.py <path.fcstm> [--no-static]", file=sys.stderr)
    sys.exit(99)
SKIP_STATIC = "--no-static" in sys.argv

path = Path(sys.argv[1])
if not path.exists():
    print(f"FILE_NOT_FOUND: {path}", file=sys.stderr)
    sys.exit(98)

src = path.read_text()

# Stage 1: parse
try:
    from pyfcstm.dsl import parse_with_grammar_entry
    ast = parse_with_grammar_entry(src, "state_machine_dsl")
    print("PARSE_OK")
except Exception as e:
    print(f"PARSE_FAIL: {e}")
    sys.exit(1)

# Stage 2: semantic
try:
    from pyfcstm.model import parse_dsl_node_to_state_machine
    sm = parse_dsl_node_to_state_machine(ast)
    print(f"SEM_OK (states={len(list(sm.iter_leaf_states())) if hasattr(sm,'iter_leaf_states') else '?'})")
except Exception as e:
    print(f"SEM_FAIL: {type(e).__name__}: {e}")
    sys.exit(2)

# Stage 3: simulation cycle
try:
    from pyfcstm.simulate import SimulationRuntime
    rt = SimulationRuntime(sm)
    rt.cycle(events=[])
    print(f"SIM_OK (current_state={rt.current_state.name if hasattr(rt.current_state,'name') else rt.current_state})")
except Exception as e:
    print(f"SIM_FAIL: {type(e).__name__}: {e}")
    sys.exit(3)

# Stage 4: static analysis — catches logical dead-code parse/sem/sim_smoke miss
#   (unwritten-read vars, forced-unreachable, deadlock states, write-only var bloat)
if not SKIP_STATIC:
    import subprocess as _sp
    static_path = Path(__file__).parent / "verify_pyfcstm_static.py"
    if static_path.exists():
        res = _sp.run([sys.executable, str(static_path), str(path)],
                      capture_output=True, text=True, timeout=60)
        out = res.stdout
        if res.returncode == 0:
            for ln in out.splitlines():
                if ln.startswith("STATIC_SUMMARY"):
                    print(ln)
                    break
            print("STATIC_OK")
        else:
            print(out, end="")
            print(f"STATIC_FAIL: see report above (re-run "
                  f"`{static_path.name}` to see full diagnostics)")
            sys.exit(4)
    else:
        print("STATIC_SKIP (analyzer not present)")

print("ALL_OK")
