"""Compatibility shim for the historical PR-E1 real-run matrix entrypoint.

The implementation moved to :mod:`method.experiments.real_run_matrix` in
LG-M1-C1.  This shim preserves published ``python -m method.pr_e1_real_runs``
and import surfaces; new code should import the function-named module directly.
"""

from __future__ import annotations

from method.experiments.real_run_matrix import *  # noqa: F401,F403
from method.experiments.real_run_matrix import _inject_pr_e1_quality_boundary, main


if __name__ == "__main__":  # pragma: no cover - exercised by CLI smoke tests
    raise SystemExit(main())
