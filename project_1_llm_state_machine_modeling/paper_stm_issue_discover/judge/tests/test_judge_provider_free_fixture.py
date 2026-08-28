"""Provider-free smoke test shipped with the standalone Semantic Judge release."""

from __future__ import annotations

import sys

from paper_stm_judge.protocol import verify_snapshot
from paper_stm_judge.scale_audit import _algorithm_source_hash


def test_packaged_protocol_and_neutral_dependencies_load_without_method() -> None:
    """The independent Judge verifies its frozen protocol without importing method code."""

    method_modules_before = {
        name for name in sys.modules if name == "paper_stm_method" or name.startswith("paper_stm_method.")
    }
    verify_snapshot()
    assert _algorithm_source_hash().startswith("sha256:")
    method_modules_after = {
        name for name in sys.modules if name == "paper_stm_method" or name.startswith("paper_stm_method.")
    }
    assert method_modules_after == method_modules_before
