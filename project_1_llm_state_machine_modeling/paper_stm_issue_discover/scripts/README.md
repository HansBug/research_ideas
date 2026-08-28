# Paper1 Scripts

All commands below are thin adapters. They contain no method, Judge, or
evaluation business logic. Provider use and write targets are stated per
command; no script may rewrite frozen run or final-results artifacts.

| Script | Purpose | Provider | Writes | Example |
| --- | --- | --- | --- | --- |
| `release/build_method_release.py` | Copy the clean-tree method allowlist and emit per-file hashes | No | New empty release directory | `python scripts/release/build_method_release.py --output /tmp/paper-stm-method-release` |
| `method/replay.py` | Recompute W-state replay from immutable method artifacts | No | Caller-supplied new replay directory | `python scripts/method/replay.py --help` |
| `method/route_replay.py` | Recompute deterministic primary routes from saved artifacts | No | Caller-supplied new replay directory | `python scripts/method/route_replay.py --help` |
| `method/frontier_replay.py` | Recompute typed frontier from saved artifacts | No | Caller-supplied new replay directory | `python scripts/method/frontier_replay.py --help` |
| `method/execution_probe_replay.py` | Recompute deterministic execution probes | No | Caller-supplied new replay directory | `python scripts/method/execution_probe_replay.py --help` |
| `method/structural_rebind_replay.py` | Rebind saved structural candidates with current typed logic | No | Caller-supplied new replay directory | `python scripts/method/structural_rebind_replay.py --help` |
| `method/native_projection_audit.py` | Audit native pyfcstm projection and input closure | No | Explicit output JSON | `python scripts/method/native_projection_audit.py --help` |

Run these adapters from a repository checkout with the official method source
and root `utils/` available on `PYTHONPATH`. The method release allowlist
excludes this whole `scripts/` directory and every replay library module.
