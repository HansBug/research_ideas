"""Function-named experiment entrypoints for project 1 method runs.

LG-M1-C1 moves historical ``method.pr_*`` experiment runners into this package
while keeping the old modules as compatibility shims for published reproduction
commands and tests.
"""

__all__ = [
    "checkpoint_resume",
    "real_run_matrix",
    "representative_cases",
]
