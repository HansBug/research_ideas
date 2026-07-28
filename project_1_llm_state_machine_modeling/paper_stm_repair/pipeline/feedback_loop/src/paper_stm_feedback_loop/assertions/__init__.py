"""Assertion execution environment for the feedback loop.

Pure assertion capabilities were ported from the legacy agent_loop eval_env at
source commit c8c1ccba.  This package is self-contained and intentionally does
not import ``paper_stm_repair_loop``.
"""

from __future__ import annotations

from .checker import AssertionCheckResult, AssertionChecker, check_assertion_script
from .environment import (
    EvalAssertResult,
    EvalEnvironment,
    FunctionCallRecord,
    build_eval_environment,
    get_assertion_environment_api_docs,
)
from .exceptions import UndeclaredTerm, UnsupportedEvidence
from .parser import ParsedAssertionScript, parse_assertion_script
from .sealed import InMemorySealedStore, SealedAssertionResult
from .views import FrozenView, UntrackedDependency

__all__ = [
    "AssertionCheckResult",
    "AssertionChecker",
    "EvalAssertResult",
    "EvalEnvironment",
    "FrozenView",
    "InMemorySealedStore",
    "FunctionCallRecord",
    "ParsedAssertionScript",
    "SealedAssertionResult",
    "UntrackedDependency",
    "UndeclaredTerm",
    "UnsupportedEvidence",
    "build_eval_environment",
    "get_assertion_environment_api_docs",
    "check_assertion_script",
    "parse_assertion_script",
]
