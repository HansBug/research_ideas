#!/usr/bin/env python3
"""Validate a pyfcstm DSL file: parse → sem → sim.

Usage:  verify_pyfcstm.py <path.fcstm>

Output (single line per stage; exit code reflects last failure):
  PARSE_OK
  SEM_OK
  SIM_OK
  ALL_OK (final line on full pass)

On failure:
  PARSE_FAIL: <error>
  SEM_FAIL:   <error>
  SIM_FAIL:   <error>
"""
import sys
from pathlib import Path

if len(sys.argv) != 2:
    print("usage: verify_pyfcstm.py <path.fcstm>", file=sys.stderr)
    sys.exit(99)

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

print("ALL_OK")
