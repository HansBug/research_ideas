"""Public assertion environment API.

Ported pure eval capabilities from legacy agent_loop eval_env at source commit
c8c1ccba.  This module re-exports the self-contained runtime implementation and
adds a compact API-doc string that can be exposed to LLM assertion authors.
"""

from __future__ import annotations

from .runtime import EvalAssertResult, EvalEnvironment, FunctionCallRecord, build_eval_environment

ASSERTION_ENVIRONMENT_API_DOCS = """
THE ASSERTION ENVIRONMENT

An assertion is one Python `assert` whose expression calls the predicate its
Requirement names.  The environment contains the predicate vocabulary and a
small set of pure builtins -- nothing else.  There is no `simulate`, no
`fbmcq`, no `states`, no `transitions`, no `transition_exists`, no `path`, no
`topology`.  Those primitives were removed on purpose: hand-assembling a check
out of them let a near-tautological bounded query close a real obligation, and
made it impossible to tell whether a call asked the right question.

WHAT YOU WRITE

    assert occupancy_after(source="R.Idle", trigger="R.go", target="R.Done") is True, "[REQ-001][AST-REQ-001-1] ..."

The arguments are the Requirement's `predicate_bindings`, copied verbatim.
Paths must come from `declared_model_vocabulary`; literal arguments such as
`kind`, `sign`, `phase`, `count` and `bound` take the values listed in the
callable reference.

Combining predicates is allowed and is how a claim over several named elements
is expressed:

    assert all([
        occupancy_after(source="R.A", trigger="R.off", target="R.Final"),
        occupancy_after(source="R.B", trigger="R.off", target="R.Final"),
    ]) is True, "[REQ-002][AST-REQ-002-1] ..."

RETURN CONTRACT

Every predicate returns a strict bool, so you never need to coerce or guard a
call.  A predicate that cannot answer raises instead of returning a value:

- a binding equal to `<undeclared>` -- the NL requires a term the model does not
  declare, so no check exists.  Do not test around it; the absence is the
  finding and the controller records it as a coverage gap.
- a variable that is not observable, or a bounded check that returned no
  terminal verdict.  A non-terminal status is never a False.

EVIDENCE FAMILY

The family is derived from the predicate, never declared by you:
Family S -> `structure`, except `edge_declared` and `guard_distinguishable`
which are `relation`, and `effect_declared` which is `effect`.
Family B -> `simulation`.  Family P -> `fbmcq`.
Declaring a family that disagrees with the predicate is a contract violation,
and the schema accepts no other spelling -- `formal` is the internal name and
is rejected.

Allowed pure builtins: abs, all, any, bool, float, int, iter, len, list, max,
min, round, set, sorted, str, sum, tuple.
""".strip()


def get_assertion_environment_api_docs() -> str:
    """Return readable API documentation for LLM assertion-script authors."""

    return ASSERTION_ENVIRONMENT_API_DOCS

__all__ = [
    "ASSERTION_ENVIRONMENT_API_DOCS",
    "get_assertion_environment_api_docs",
    "EvalAssertResult",
    "EvalEnvironment",
    "FunctionCallRecord",
    "build_eval_environment",
]
