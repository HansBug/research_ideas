"""Public assertion environment API.

Ported pure eval capabilities from legacy agent_loop eval_env at source commit
c8c1ccba.  This module re-exports the self-contained runtime implementation and
adds a compact API-doc string that can be exposed to LLM assertion authors.
"""

from __future__ import annotations

from .runtime import EvalAssertResult, EvalEnvironment, FunctionCallRecord, build_eval_environment

ASSERTION_ENVIRONMENT_API_DOCS = """
ASSERTION EXECUTION CONTRACT
- AssertionScript has one shared Python prefix and independent assertion expressions.
- At execution, each item becomes: <full prefix> then `assert (<expression>), <literal failure_message>` in a fresh namespace.
- The terminal expression must evaluate to a strict `bool`. Exceptions, unsupported/inconclusive formal results, and non-bool values are invalid; only strict False is a contradiction.
- Every expression must call the evidence family declared by evidence_family. Do not return a constant or rely only on prefix-computed constants.
- Helpers are read-only and return tuples, scalars, or frozen attribute views. No imports, paths, mutation, network, hidden cases, or gold data.

EVIDENCE SELECTION
- A structural requirement may use structure/relation/effect/topology facts.
- A requirement that states runtime behavior under a condition or event must include simulation or FBMCQ evidence; static transition existence alone is only complementary evidence.
- A cold-start simulation covers only one initialization path. For a state-agnostic behavior claim, use explicit hot-start initialization for relevant state(s), or use FBMCQ for a bounded universal/counterexample claim and state its bound.
- Use hot-start simulation for a named state/mode and inspect the event in consumed_events plus the resulting state/effect.

STRUCTURE / RELATION
Evidence-family mapping: states/events/variables/initial_child are ``structure``;
transitions/transition_exists/guards_overlap are ``relation``. The declared
evidence_family must match the family of the function actually called.
states(*, parent=None, recursive=True, name=None, path=None, within=None, kind=None, exact=False) -> tuple[state]
  state fields include path, name, parent_path, is_leaf, is_composite, is_pseudo, substates, initial_targets.
events(*, name=None, path=None, within=None, scope=None, declared=None, used=None, exact=False) -> tuple[event]
variables(*, name=None, path=None, within=None, type=None, read_in=None, written_in=None, exact=False) -> tuple[variable]
transitions(*, source=None, event=None, target=None, forced=None, within=None, has_event=None, has_guard=None, has_effect=None, self_loop=None, source_within=None, target_within=None, exact=False) -> tuple[transition]
  transition fields include from_path, to_path, event, guard, effect, is_forced, transition_index.
transition_exists(*, source=None, event=None, target=None, within=None, exact=False) -> bool
initial_child(state: str) -> str | None
guards_overlap(left_ref: str, right_ref: str) -> bool; both refs must identify unambiguous transitions.

EFFECT
effects(*, source=None, event=None, target=None, variable=None) -> tuple[transition carrying effects]
effect_deltas(*, source=None, event=None, target=None) -> tuple[(variable, numeric_delta)]
effect_delta(*, source=None, event=None, target=None, variable: str) -> number | None; requires one unambiguous transition.
Prefer `any(delta < 0 for _, delta in effect_deltas(...))` when NL constrains an effect but not a variable name.

SIMULATION
simulate(*, cycles: list[list[str]], initial_state: str | None = None, initial_vars: dict[str, number] | None = None) -> simulation
  simulation fields: cycles, final, requested_initialization, effective_initialization, model_sha256.
  each cycle/final fields: index, is_ended, active_states, variables, input_events, consumed_events, unconsumed_events, fired_transitions, limitations; method is_active(state).
  ``initial_vars`` keys must be the exact declaration names accepted by pyfcstm (for example ``"counter"``), not qualified state-machine paths. This is different from the result view: ``cycle.variables`` is a mapping-like frozen view keyed by complete variable path, so use cycle.variables["Root.counter"], never cycle.variables[0]. active_states, consumed_events, and unconsumed_events are tuples of complete event/state paths.
  Cold start: include an explicit leading [] cycle when initialization must run, and put an initialization-triggering event in a later cycle; this is a finite initial-path witness, not a global claim. Hot start: supply exact initial_state and every declared variable in initial_vars using declaration names, then place the causal event in cycle 0. Check event membership in consumed_events plus resulting state/effect; never assume an event is consumed exactly once in hierarchical execution.

BOUNDED FORMAL CHECKING
fbmcq(query: str) -> formal observation with fields canonical_query, status, holds, bound, formal_property_kind, formal_bound, assumption_basis, witness, replay_status, limitations.
  Use a complete pyfcstm FBMCQ query such as `check reach <= 5: active("Root.Done");` or an appropriate response/invariant query. `.holds is True` is the terminal bool pattern. Choose a finite bound justified by the NL or model scale; bounded evidence is stronger than sampled simulation for its declared horizon but does not establish unbounded correctness. Parse/solver/replay uncertainty raises invalid rather than False.

TOPOLOGY
topology() -> view with initial_closure, unreachable_leaves, strongly_connected_components, dead_ends, root_exit_reachable, topological_finite, topological_inevitable_terminator, guard_agnostic, limitations.
path(source: str, target: str, avoid: tuple[str, ...] = (), max_hops: int | None = None) -> view with exists, nodes, hop_count, transition_refs, source_macro_refs, compiler_owned_nodes, guard_agnostic, limitations.
Topology is guard-agnostic structural evidence; do not overclaim behavioral inevitability when limitations say otherwise.

SOURCE MAPPING
mapped_source_refs(fcstm_ref: str) -> tuple[str, ...]
mapped_fcstm_refs(source_ref: str) -> tuple[str, ...]
bound_model_refs(coverage_unit_id: str, fact_kind: str | None = None) -> tuple[str, ...]
Mapping evidence alone cannot confirm an issue; source attribution is applied deterministically after assertion acceptance.

Allowed pure builtins: abs, all, any, bool, float, int, iter, len, list, max, min, round, set, sorted, str, sum, tuple.
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
