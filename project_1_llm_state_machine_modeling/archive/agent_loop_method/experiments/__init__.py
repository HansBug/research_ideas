"""Function-named experiment entrypoints for project 1 method runs.

LG-M1-C1 moves historical ``archive.agent_loop_method.pr_*`` experiment runners into this package
while keeping the old modules as compatibility shims for published reproduction
commands and tests.
"""

__all__ = [
    "ablation",
    "checkpoint_resume",
    "real_run_matrix",
    "representative_cases",
]

# Deterministic ablation experiment package is available as archive.agent_loop_method.experiments.ablation.
