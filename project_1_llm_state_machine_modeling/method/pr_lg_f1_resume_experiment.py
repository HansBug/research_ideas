"""Compatibility shim for the historical LG-F1 checkpoint/resume entrypoint.

The implementation moved to :mod:`method.experiments.checkpoint_resume` in
LG-M1-C1.  This shim preserves published
``python -m method.pr_lg_f1_resume_experiment`` and import surfaces; new code
should import the function-named module directly.
"""

from __future__ import annotations

import sys
from pathlib import Path

if __package__ and __package__.startswith("project_1_llm_state_machine_modeling."):
    # Preserve repo-root package execution such as
    # ``python -m project_1_llm_state_machine_modeling.method.<legacy_module>``.
    # The moved implementations still use absolute ``method.*`` imports for the
    # historical ``PYTHONPATH=project_1_llm_state_machine_modeling`` workflow,
    # so package-mode shims must add the project package root explicitly.
    # This bootstrap does not read ``.env`` and does not touch provider config.
    _PROJECT_ROOT = Path(__file__).resolve().parents[1]
    if str(_PROJECT_ROOT) not in sys.path:
        sys.path.insert(0, str(_PROJECT_ROOT))

from method.experiments.checkpoint_resume import *  # noqa: F401,F403
from method.experiments.checkpoint_resume import main


if __name__ == "__main__":  # pragma: no cover - exercised by CLI smoke tests
    raise SystemExit(main())
