"""Compatibility shim for the historical PR-D representative entrypoint.

The implementation moved to :mod:`method.experiments.representative_cases` in
LG-M1-C1.  This shim preserves published ``python -m method.pr_d_representative``
and import surfaces; new code should import the function-named module directly.
"""

from __future__ import annotations

from method.experiments.representative_cases import *  # noqa: F401,F403
from method.experiments.representative_cases import _schema_validation_error, main


if __name__ == "__main__":  # pragma: no cover - exercised by CLI smoke tests
    raise SystemExit(main())
