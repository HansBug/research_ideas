"""Compatibility shim for the historical LG-F1 checkpoint/resume entrypoint.

The implementation moved to :mod:`method.experiments.checkpoint_resume` in
LG-M1-C1.  This shim preserves published
``python -m method.pr_lg_f1_resume_experiment`` and import surfaces; new code
should import the function-named module directly.
"""

from __future__ import annotations

from method.experiments.checkpoint_resume import *  # noqa: F401,F403
from method.experiments.checkpoint_resume import main


if __name__ == "__main__":  # pragma: no cover - exercised by CLI smoke tests
    raise SystemExit(main())
