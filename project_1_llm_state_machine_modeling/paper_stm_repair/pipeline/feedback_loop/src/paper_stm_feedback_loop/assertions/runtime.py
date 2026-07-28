from __future__ import annotations

import copy
import re
import signal
import threading
import traceback
from dataclasses import dataclass, field
from typing import Any, Callable

from .pyfcstm_adapter import check_fcstm, sha256_text
from .pyfcstm_adapter import load_model_for_simulation
from .effects import EffectAPI
from .exceptions import UnsupportedEvidence
from .predicate_api import PREDICATE_FAMILIES, PredicateAPI
from .fbmcq import FBMCQAPI, FBMCQ_FIELDS
from .provenance import SAFE_BUILTINS, AuditReport, audit_expression
from .relations import RelationAPI
from .simulation import (
    CYCLE_FIELDS,
    INIT_FIELDS,
    SIM_FIELDS,
    SIM_METHODS,
    SimulationAPI,
)
from .source_mapping import MAPPING_FIELDS, SourceMappingAPI
from .structure import STRUCTURE_FIELDS, StructureAPI
from .topology import PATH_FIELDS, TOPOLOGY_FIELDS, TopologyAPI
from .views import FrozenView, UntrackedDependency, stable_hash


RESULT_TRUE = "true"
RESULT_FALSE = "false"
RESULT_NON_BOOL = "non_bool"
RESULT_EXCEPTION = "exception"
RESULT_TIMEOUT = "timeout"
RESULT_UNSUPPORTED = "unsupported"
RESULT_UNTRACKED = "untracked_dependency"
RESULT_NO_MODEL_EVIDENCE = "no_model_evidence"
RESULT_REQUIRED_FAMILY_MISSING = "required_family_missing"

ALLOWED_FUNCTION_FAMILIES = frozenset({"structure", "relation", "effect", "simulation", "formal", "mapping"})

TERMINAL_RESULTS = {
    RESULT_TRUE,
    RESULT_FALSE,
    RESULT_NON_BOOL,
    RESULT_EXCEPTION,
    RESULT_TIMEOUT,
    RESULT_UNSUPPORTED,
    RESULT_UNTRACKED,
    RESULT_NO_MODEL_EVIDENCE,
    RESULT_REQUIRED_FAMILY_MISSING,
}


def _view_get(view: Any, key: str) -> Any:
    """Read a field from a frozen view without tripping its access guard.

    ``FrozenView.__getattr__`` raises ``UntrackedDependency`` for unregistered
    fields, which is the correct behaviour for assertion authors but wrong for
    audit-metadata collection: a probe for an optional field must be allowed to
    come back empty.  ``FrozenView.get`` has exactly that contract.
    """

    if view is None:
        return None
    getter = getattr(view, "get", None)
    if callable(getter):
        try:
            return getter(key, None)
        except Exception:
            return None
    return None


def _audit_value(value: Any) -> Any:
    if isinstance(value, FrozenView):
        return value.to_json()
    if isinstance(value, dict):
        return {str(key): _audit_value(item) for key, item in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [_audit_value(item) for item in value]
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    return repr(value)


@dataclass(frozen=True)
class FunctionCallRecord:
    function: str
    family: str
    args_hash: str
    kwargs_hash: str
    status: str
    result_hash: str | None = None
    args: Any = None
    kwargs: dict[str, Any] = field(default_factory=dict)
    result: Any = None
    model_refs: tuple[str, ...] = field(default_factory=tuple)
    exception_type: str | None = None
    exception_message: str | None = None

    def to_json(self) -> dict[str, Any]:
        return self.__dict__.copy()


@dataclass(frozen=True)
class EvalAssertResult:
    """Terminal direct eval result with provenance and call trace."""

    result: str
    match_status: str
    value: bool | None
    assert_text: str
    assert_sha256: str
    reason: str
    audit: dict[str, Any]
    vars_hash_before: str
    vars_hash_after: str
    function_registry_hash: str
    function_call_trace: tuple[FunctionCallRecord, ...] = field(default_factory=tuple)
    actual_function_families: tuple[str, ...] = field(default_factory=tuple)
    required_function_families: tuple[str, ...] = field(default_factory=tuple)
    error: dict[str, Any] | None = None

    @property
    def ok(self) -> bool:
        return self.result == RESULT_TRUE

    def to_json(self) -> dict[str, Any]:
        return {
            "result": self.result,
            "match_status": self.match_status,
            "value": self.value,
            "assert": self.assert_text,
            "assert_sha256": self.assert_sha256,
            "reason": self.reason,
            "audit": self.audit,
            "vars_hash_before": self.vars_hash_before,
            "vars_hash_after": self.vars_hash_after,
            "function_registry_hash": self.function_registry_hash,
            "function_call_trace": [record.to_json() for record in self.function_call_trace],
            "actual_function_families": list(self.actual_function_families),
            "required_function_families": list(self.required_function_families),
            "error": self.error,
        }


class EvalEnvironment:
    """Direct Python assertion eval environment with provenance audit.

    Parameters: ``model_text`` and/or ``inspect`` are the controller-frozen FCSTM
    artifacts.  If ``inspect`` is omitted and ``model_text`` is supplied, the
    environment obtains pyfcstm structured inspect through the existing adapter.
    ``source_mappings`` is the frozen input-bridge/source-trace mapping list.
    ``extra_vars`` may expose additional immutable ``FrozenView`` observations;
    ``extra_functions`` may expose test/runtime pure callables with explicit
    family names from the exact Issue #164 enum
    ``structure/relation/effect/simulation/formal/mapping``.  FBMCQ functions
    are registered as ``formal`` evidence, and source mapping/bound-ref helpers
    are registered as ``mapping`` evidence.  ``bmc_runner`` is a structured FBMCQ
    test seam.

    Returns: ``eval_assert(assert_text, reason, required_function_families=...)``
    returns one ``EvalAssertResult``.  Results distinguish ``true``, ``false``,
    ``non_bool``, ``exception``, ``timeout``, ``unsupported``,
    ``untracked_dependency``, ``no_model_evidence``, and
    ``required_family_missing``.

    Execution: the runtime statically audits the expression AST for registered
    names, dunder attributes, and registered view fields/methods, then executes
    the original positive Python expression via ``eval`` with controlled
    globals/locals.  It does not translate assertions into a JSON predicate DSL.
    Registered evidence functions wrap structure/relation/effect/simulation/
    formal/mapping families and record actual function call traces, hashes, and
    exceptions.  Eval globals expose only a tiny safe builtin set and never expose
    ``open``, ``__import__``, environment, time, random, or network modules.

    Failure semantics: audit failures become ``untracked_dependency`` before
    eval.  Strict bool ``True`` becomes ``true``/``matches``; strict bool
    ``False`` becomes ``false``/``contradicts``.  Other values are ``non_bool``.
    ``UnsupportedEvidence`` becomes ``unsupported``; ``TimeoutError`` or alarm
    expiry becomes ``timeout``; other exceptions become ``exception``.  A bool
    expression with no evidence-producing function calls is ``no_model_evidence``.
    A bool expression whose actual call trace lacks any required family is
    ``required_family_missing`` even if Python returned a bool.

    Evidence limitations: this is a trusted local academic provenance gate, not a malicious-code sandbox.  It verifies sealed dependencies and evidence traces
    for direct eval; it does not claim semantic coverage, source confirmation, or
    global model correctness.

    Permissions: read-only in-memory artifacts and temporary FBMCQ files created
    inside pyfcstm tooling; no Agent-supplied arbitrary paths, imports, shell,
    environment, time/random, network, mutation, or hidden reference/gold data.

    Example: ``env.eval_assert("transition_exists(source='Root.A',
    event='Root.go', target='Root.B')", "check transition",
    required_function_families=["relation"])`` returns one terminal result with
    the relation call trace.
    """

    def __init__(
        self,
        *,
        model_text: str | None = None,
        model_path: str = "<memory>",
        inspect: dict[str, Any] | None = None,
        source_mappings: list[dict[str, Any]] | None = None,
        source_exclusions: list[str] | tuple[str, ...] | None = None,
        coverage_bindings: dict[str, list[str]] | None = None,
        extra_vars: dict[str, Any] | None = None,
        extra_functions: dict[str, tuple[str, Callable[..., Any]]] | None = None,
        timeout_seconds: int | None = None,
        bmc_runner: Callable[..., tuple[str, int]] | None = None,
        formal_verification_enabled: bool = True,
        fbmcq_solver_timeout_ms: int | None = None,
        fbmcq_max_bound: int | None = None,
        fbmcq_process_wall_seconds: float | None = None,
    ) -> None:
        self.model_text = model_text
        self.model_path = model_path
        if inspect is None and model_text is not None:
            checked = check_fcstm(model_text, model_path)
            inspect = checked.get("inspect") if checked.get("inspect_status") == "ok" else {}
        self.inspect = copy.deepcopy(inspect or {})
        self.source_mappings = copy.deepcopy(source_mappings or [])
        self.source_exclusions = tuple(str(item) for item in (source_exclusions or ()))
        self.timeout_seconds = timeout_seconds
        self.call_trace: list[FunctionCallRecord] = []
        self._known_paths_cache: frozenset[str] | None = None

        self.structure = StructureAPI(self.inspect)
        self.relations = RelationAPI(self.structure)
        route_control_prefix = "compiler:route_control:"
        excluded_variables = {
            item.removeprefix(route_control_prefix)
            for item in self.source_exclusions
            if item.startswith(route_control_prefix)
        }
        self.effects = EffectAPI(
            self.structure,
            excluded_variables=excluded_variables,
        )
        inspect_transitions = self.inspect.get("transitions")
        self.simulation = SimulationAPI(
            model_text,
            model_path,
            transitions=(
                inspect_transitions if isinstance(inspect_transitions, list) else None
            ),
            excluded_refs=self.source_exclusions,
        )
        machine = (
            load_model_for_simulation(model_text, model_path)
            if isinstance(model_text, str) and model_text.strip()
            else None
        )
        self.topology_api = (
            TopologyAPI(self.inspect, machine) if machine is not None else None
        )
        self.fbmcq_api = FBMCQAPI(
            model_text,
            timeout_ms=fbmcq_solver_timeout_ms,
            max_bound=fbmcq_max_bound,
            process_wall_seconds=fbmcq_process_wall_seconds,
            bmc_runner=bmc_runner,
        )
        self.mapping = SourceMappingAPI(
            self.source_mappings, bindings=coverage_bindings
        )

        # The evidence surface an assertion may call is the predicate vocabulary
        # of issue #170 and nothing else.  The raw building blocks these
        # predicates are made of -- states/simulate/fbmcq/transition_exists --
        # are deliberately *not* registered: exposing them let the producer
        # hand-assemble a check, and a hand-written bounded query on pair 0006
        # (`init state(X); check exists_always <= 1: active(X)`) was
        # near-tautological, passed, and reported an unanswerable requirement as
        # satisfied.  Building the query here once removes that whole class.
        self.predicates = PredicateAPI(
            structure=self.structure,
            relations=self.relations,
            effects=self.effects,
            simulation=self.simulation,
            topology=self.topology_api,
            formal=self.fbmcq_api if formal_verification_enabled else None,
        )
        functions: dict[str, tuple[str, Callable[..., Any]]] = {
            name: (family, getattr(self.predicates, method))
            for name, (family, method) in PREDICATE_FAMILIES.items()
        }
        if not formal_verification_enabled:
            for name, (family, _m) in PREDICATE_FAMILIES.items():
                if family == "formal":
                    functions.pop(name, None)
        if extra_functions:
            functions.update(extra_functions)
        invalid_registry_families = {
            family for family, _func in functions.values() if family not in ALLOWED_FUNCTION_FAMILIES
        }
        if invalid_registry_families:
            raise ValueError(f"unknown eval function families: {sorted(invalid_registry_families)}")
        self._raw_functions = functions
        self.locals: dict[str, Any] = {}
        for name, (family, func) in functions.items():
            self.locals[name] = self._wrap_function(name, family, func)
        if extra_vars:
            self.locals.update(extra_vars)

        # Comprehensions and generator expressions resolve free names from the
        # globals mapping. Publish the same sealed registry there so an audited
        # expression can call registered helpers inside a comprehension without
        # gaining any additional dependency surface.
        self.globals = {
            "__builtins__": SAFE_BUILTINS.copy(),
            **SAFE_BUILTINS,
            **self.locals,
        }
        self.allowed_names = set(self.locals) | set(SAFE_BUILTINS)
        self.registered_objects = {name: value for name, value in self.locals.items() if isinstance(value, FrozenView)}
        # Derive provenance from the exact public FrozenView contracts. A
        # hand-maintained subset silently rejected valid fields such as
        # ``State.is_leaf`` even though the view and Agent tool documented them.
        self.registered_view_attrs = set().union(
            STRUCTURE_FIELDS,
            INIT_FIELDS,
            CYCLE_FIELDS,
            SIM_FIELDS,
            FBMCQ_FIELDS,
            MAPPING_FIELDS,
            SIM_METHODS,
            {"keys", "items", "values", "get"},
            TOPOLOGY_FIELDS,
            PATH_FIELDS,
        )

    @property
    def function_registry_hash(self) -> str:
        payload = {
            name: {"family": family, "callable": getattr(func, "__qualname__", repr(func))}
            for name, (family, func) in sorted(self._raw_functions.items())
        }
        return stable_hash(payload)

    @property
    def vars_hash(self) -> str:
        return stable_hash(
            {
                "model_sha256": sha256_text(self.model_text or ""),
                "inspect": self.inspect,
                "source_mappings": self.source_mappings,
                "source_exclusions": self.source_exclusions,
                "registered_vars": {
                    key: value.to_json() if isinstance(value, FrozenView) else repr(value)
                    for key, value in sorted(self.locals.items())
                    if key not in self._raw_functions
                },
            }
        )

    def eval_assert(
        self,
        assert_text: str,
        reason: str,
        *,
        required_function_families: list[str] | tuple[str, ...] | None = None,
    ) -> EvalAssertResult:
        if not isinstance(assert_text, str) or not assert_text.strip():
            return self._result(
                RESULT_UNTRACKED,
                assert_text=str(assert_text),
                reason=reason,
                audit=AuditReport(False, sha256_text(str(assert_text)), (), (), ()),
                before=self.vars_hash,
                after=self.vars_hash,
                error={"type": "InvalidAssert", "message": "assert_text must be a non-empty string"},
                required=tuple(required_function_families or ()),
            )
        required = tuple(required_function_families or ())
        invalid_required = [family for family in required if family not in ALLOWED_FUNCTION_FAMILIES]
        if invalid_required:
            before = self.vars_hash
            return self._result(
                RESULT_UNSUPPORTED,
                assert_text=assert_text,
                reason=reason,
                audit=AuditReport(True, sha256_text(assert_text), (), ()),
                before=before,
                after=before,
                error={
                    "type": "InvalidFunctionFamily",
                    "message": "required_function_families must use structure/relation/effect/simulation/formal/mapping",
                    "invalid": invalid_required,
                },
                required=required,
            )
        self.call_trace = []
        before = self.vars_hash
        audit = audit_expression(
            assert_text,
            allowed_names=self.allowed_names,
            registered_objects=self.registered_objects,
            registered_view_attrs=self.registered_view_attrs,
        )
        if not audit.ok:
            return self._result(
                RESULT_UNTRACKED,
                assert_text=assert_text,
                reason=reason,
                audit=audit,
                before=before,
                after=self.vars_hash,
                error={"type": "AuditRejected", "issues": [issue.__dict__ for issue in audit.issues]},
                required=required,
            )
        try:
            value = self._eval_with_timeout(assert_text)
        except TimeoutError as exc:
            return self._result(RESULT_TIMEOUT, assert_text=assert_text, reason=reason, audit=audit, before=before, after=self.vars_hash, error={"type": type(exc).__name__, "message": str(exc), "metadata": copy.deepcopy(getattr(exc, "metadata", None))}, required=required)
        except UnsupportedEvidence as exc:
            return self._result(RESULT_UNSUPPORTED, assert_text=assert_text, reason=reason, audit=audit, before=before, after=self.vars_hash, error={"type": type(exc).__name__, "message": str(exc), "metadata": copy.deepcopy(getattr(exc, "metadata", None))}, required=required)
        except UntrackedDependency as exc:
            return self._result(RESULT_UNTRACKED, assert_text=assert_text, reason=reason, audit=audit, before=before, after=self.vars_hash, error={"type": type(exc).__name__, "message": str(exc)}, required=required)
        except Exception as exc:
            return self._result(RESULT_EXCEPTION, assert_text=assert_text, reason=reason, audit=audit, before=before, after=self.vars_hash, error={"type": type(exc).__name__, "message": str(exc), "traceback": traceback.format_exc(limit=3)}, required=required)

        after = self.vars_hash
        actual_families = tuple(sorted({record.family for record in self.call_trace if record.status == "completed"}))
        missing = tuple(family for family in required if family not in actual_families)
        if not isinstance(value, bool):
            return self._result(RESULT_NON_BOOL, assert_text=assert_text, reason=reason, audit=audit, before=before, after=after, value=None, required=required)
        if not actual_families:
            return self._result(RESULT_NO_MODEL_EVIDENCE, assert_text=assert_text, reason=reason, audit=audit, before=before, after=after, value=value, required=required, error={"type": "NoModelEvidence", "message": "no registered evidence function was called"})
        if missing:
            return self._result(RESULT_REQUIRED_FAMILY_MISSING, assert_text=assert_text, reason=reason, audit=audit, before=before, after=after, value=value, required=required, error={"type": "RequiredFamilyMissing", "missing": list(missing)})
        return self._result(RESULT_TRUE if value is True else RESULT_FALSE, assert_text=assert_text, reason=reason, audit=audit, before=before, after=after, value=value, required=required)

    def _eval_with_timeout(self, assert_text: str) -> Any:
        if not self.timeout_seconds:
            return eval(assert_text, self.globals, self.locals)
        # LangChain executes sync tools in a worker thread. POSIX interval
        # signals are process-main-thread only; attempting to install SIGALRM in
        # that worker would turn every valid assertion into an exception. The
        # outer Agent/tool budget remains active in this path, and the audited
        # expression can call only Controller-registered bounded functions.
        if threading.current_thread() is not threading.main_thread():
            return eval(assert_text, self.globals, self.locals)

        def handler(_signum: int, _frame: Any) -> None:
            raise TimeoutError("direct eval timed out")

        previous = signal.signal(signal.SIGALRM, handler)
        signal.alarm(int(self.timeout_seconds))
        try:
            return eval(assert_text, self.globals, self.locals)
        finally:
            signal.alarm(0)
            signal.signal(signal.SIGALRM, previous)

    def _wrap_function(self, name: str, family: str, func: Callable[..., Any]) -> Callable[..., Any]:
        def wrapped(*args: Any, **kwargs: Any) -> Any:
            if name in PREDICATE_FAMILIES:
                self.predicates.begin_call()
            try:
                value = func(*args, **kwargs)
                self.call_trace.append(
                    FunctionCallRecord(
                        function=name,
                        family=family,
                        args_hash=stable_hash(args),
                        kwargs_hash=stable_hash(kwargs),
                        status="completed",
                        result_hash=stable_hash(value),
                        args=_audit_value(args),
                        kwargs=_audit_value(kwargs),
                        result=_audit_value(value),
                        model_refs=self._model_refs(name, kwargs, value),
                    )
                )
                return value
            except Exception as exc:
                self.call_trace.append(
                    FunctionCallRecord(
                        function=name,
                        family=family,
                        args_hash=stable_hash(args),
                        kwargs_hash=stable_hash(kwargs),
                        status="exception",
                        args=_audit_value(args),
                        kwargs=_audit_value(kwargs),
                        exception_type=type(exc).__name__,
                        exception_message=str(exc),
                    )
                )
                raise

        wrapped.__name__ = name
        return wrapped

    def _model_refs(
        self, name: str, kwargs: dict[str, Any], value: Any
    ) -> tuple[str, ...]:
        """Audit metadata only -- a failure here must never change an outcome.

        The reference set feeds attribution, not evaluation.  Letting an
        exception escape would turn a completed call into an exception record and
        silently change the assertion's verdict, so collection is guarded.
        """

        try:
            return self._collect_model_refs(name, kwargs, value)
        except Exception:
            return ()

    def _collect_model_refs(
        self, name: str, kwargs: dict[str, Any], value: Any
    ) -> tuple[str, ...]:
        # Predicates report their own references: the predicate chose the query,
        # so it is the only thing that knows which elements the answer rests on.
        # Re-deriving them from the function name here would break the moment a
        # predicate changes how it is implemented.
        if name in PREDICATE_FAMILIES:
            return self.predicates.consume_refs()
        return self._collect_legacy_model_refs(name, kwargs, value)

    def _collect_legacy_model_refs(
        self, name: str, kwargs: dict[str, Any], value: Any
    ) -> tuple[str, ...]:
        """Preserve model scope beside compact assertion return values.

        Some public APIs intentionally return compact values, such as
        ``effect_deltas() -> (variable, delta)``. The compact result is useful
        to assertion authors but is insufficient for later source attribution.
        Re-querying the already-frozen inspect facts here records the matching
        transition identity without changing the public API or executing new
        model behavior.
        """

        refs: set[str] = set()
        if name == "simulate":
            return self._simulation_refs(value)
        if name == "fbmcq":
            return self._formal_refs(value)
        effect_functions = {
            "effects",
            "effect_deltas",
            "effect_delta",
            "effect_assigns",
        }
        if name in {
            "transitions",
            "transition_exists",
            "conflicting_targets",
            *effect_functions,
        }:
            filters = {
                key: kwargs[key]
                for key in ("source", "event", "target")
                if isinstance(kwargs.get(key), str)
            }
            # A variable-only effect probe is intentionally model-wide. Do not
            # attach every transition and manufacture source attribution.
            if name in effect_functions and not filters:
                return ()
            try:
                transitions = self.structure.transitions(**filters)
            except Exception:
                transitions = ()
            used_near_miss = False
            if name == "transition_exists" and value is False and not transitions:
                transitions = self._near_miss_transitions(filters)
                used_near_miss = bool(transitions)
            for transition in transitions:
                for key in ("from_path", "to_path", "event"):
                    ref = getattr(transition, key, None)
                    if isinstance(ref, str) and ref:
                        refs.add(ref)
                index = getattr(transition, "transition_index", None)
                if isinstance(index, int):
                    refs.add(f"transition:{index}")
                for variable in self._route_control_variables(transition):
                    if name in effect_functions:
                        # The effect API already dropped this variable from the
                        # answer (see EffectAPI.excluded_variables), so the
                        # result does not rest on it in any way.  Reporting it
                        # as a touched reference made attribution mark the whole
                        # finding `representation_debt`: on pair 0006 the only
                        # effect on the Attack_Complete transition is the
                        # compiler's `R45RouteToken`, so the very query that
                        # proves "no semantic decrement exists" was disqualified
                        # for having looked at the thing it filtered out.  Keep
                        # the audit trail under a distinct kind that attribution
                        # does not read as compiler ownership.
                        refs.add(f"filtered_route_control:{variable}")
                    else:
                        # For relation/topology queries the token's presence is
                        # genuine evidence of converter lowering (a composite
                        # exit split into `-> [*]` plus a token-guarded parent
                        # transition), so it must keep signalling debt.
                        refs.add(f"route_control:{variable}")
                actual_event = getattr(transition, "event", None)
                requested_event = filters.get("event")
                if (
                    used_near_miss
                    and requested_event
                    and isinstance(actual_event, str)
                    and actual_event
                    and actual_event != requested_event
                ):
                    projection_ref = f"compiler:event_projection:{actual_event}"
                    if projection_ref in self.source_exclusions:
                        refs.add(projection_ref)
        return tuple(sorted(refs))

    def _simulation_refs(self, value: Any) -> tuple[str, ...]:
        """Report the path a simulation actually took, not the states it observed.

        A state observation alone is not attribution evidence: knowing the run
        ended in ``Root.Done`` says nothing about whether the path there crossed
        compiler-owned lowering.  Reporting the derived fired transitions puts
        every element of the path into the reference set, so the shared exclusion
        matcher can taint it exactly as it taints a static relation query.

        Two cases need explicit handling rather than an empty result:

        ``ambiguous``  the derivation is not unique and candidates disagree, so
                       an unresolved segment may be tainted.  Reporting only the
                       resolved prefix would present a possibly-dirty path as
                       clean, so a blocking marker is emitted instead.
        ``no_path``    nothing fired.  The injected event being ignored *is* the
                       defect, and it has no path to bind, so the transitions
                       declared for that event are reported as a near miss --
                       the same rule ``_near_miss_transitions`` applies to a
                       failed static query.
        """

        cycles = _view_get(value, "cycles")
        if not isinstance(cycles, (list, tuple)):
            return ()
        refs: set[str] = set()
        ambiguous = False
        for cycle in cycles:
            for item in _view_get(cycle, "path_refs") or ():
                if isinstance(item, str) and item:
                    refs.add(item)
            if _view_get(cycle, "path_taint") == "ambiguous":
                ambiguous = True
            fired = _view_get(cycle, "fired_transitions") or ()
            unconsumed = _view_get(cycle, "unconsumed_events") or ()
            if not fired and unconsumed:
                refs.update(self._ignored_event_refs(unconsumed))
        if ambiguous:
            # Blocks promotion in bind_attribution; see W6 in issue #170.
            refs.add("simulation:path_taint:ambiguous")
        return tuple(sorted(refs))

    def _ignored_event_refs(self, events: Any) -> set[str]:
        """Return the declared carriers of events the runtime never consumed."""

        refs: set[str] = set()
        for event in events:
            if not isinstance(event, str) or not event:
                continue
            refs.add(event)
            try:
                transitions = self.structure.transitions(event=event)
            except Exception:
                continue
            for transition in transitions:
                for key in ("from_path", "to_path"):
                    ref = getattr(transition, key, None)
                    if isinstance(ref, str) and ref and ref != "[*]":
                        refs.add(ref)
                index = getattr(transition, "transition_index", None)
                if isinstance(index, int):
                    refs.add(f"transition:{index}")
        return refs

    def _formal_refs(self, value: Any) -> tuple[str, ...]:
        """Report the model elements a bounded-model-checking answer rests on.

        A refuted property yields a counterexample, and the states on that trace
        are what the answer is about.  An unrefuted reachability query has no
        trace by definition, so only the elements the query itself named can be
        reported -- read back from the canonical query text, the one place they
        are recorded.  Those are marked ``examined_only`` so attribution does not
        read the absence of a counterexample as an exhibited source defect.
        """

        refs: set[str] = set()
        witness = _view_get(value, "witness")
        if witness is not None:
            # A counterexample records the configuration per frame and the events
            # consumed per step; together they are the trace the answer rests on.
            for frame in _view_get(witness, "frames") or ():
                state = _view_get(frame, "state")
                if isinstance(state, str) and state:
                    refs.add(state)
            for step in _view_get(witness, "steps") or ():
                for item in _view_get(step, "consumed_events") or ():
                    if isinstance(item, str) and item:
                        refs.add(item)
            if refs:
                return tuple(sorted(refs))
        query = _view_get(value, "canonical_query")
        if isinstance(query, str) and query:
            known = self._known_model_paths()
            for token in re.findall(r'"([^"]+)"', query):
                if token in known:
                    refs.add(token)
        if refs:
            refs.add("formal:examined_only")
        return tuple(sorted(refs))

    def _known_model_paths(self) -> frozenset[str]:
        """Return declared state and event paths, so query text is not trusted."""

        if self._known_paths_cache is None:
            paths: set[str] = set()
            for key in ("states", "events"):
                for item in self.inspect.get(key, []) or []:
                    if isinstance(item, dict):
                        path = item.get("path")
                        if isinstance(path, str) and path:
                            paths.add(path)
            self._known_paths_cache = frozenset(paths)
        return self._known_paths_cache

    def _near_miss_transitions(
        self, filters: dict[str, str]
    ) -> tuple[FrozenView, ...]:
        """Return the closest actual relation for a failed exact query.

        A negative ``transition_exists`` result otherwise has no model identity
        to bind.  Prefer the same source and trigger so a wrong destination is
        still attributable; then try the remaining two-field projections.  A
        single-field fallback is used only when the query itself supplies fewer
        than three fields.  This records evidence scope, not a semantic guess.
        """

        preferred = (
            ("source", "event"),
            ("source", "target"),
            ("event", "target"),
        )
        candidates = [
            {key: filters[key] for key in keys}
            for keys in preferred
            if all(key in filters for key in keys) and len(keys) < len(filters)
        ]
        if len(filters) <= 2:
            candidates.extend(
                {key: filters[key]}
                for key in ("source", "event", "target")
                if key in filters
            )
        for candidate in candidates:
            try:
                transitions = self.structure.transitions(**candidate)
            except Exception:
                continue
            if transitions:
                return transitions
        return ()

    def _route_control_variables(self, transition: FrozenView) -> tuple[str, ...]:
        """Return excluded compiler route variables referenced by a transition."""

        if not self.source_exclusions:
            return ()
        text = " ".join(
            str(value)
            for value in (
                getattr(transition, "guard", None),
                getattr(transition, "effect", None),
            )
            if value is not None
        )
        if not text:
            return ()
        prefix = "compiler:route_control:"
        return tuple(
            sorted(
                variable
                for exclusion in self.source_exclusions
                if exclusion.startswith(prefix)
                for variable in (exclusion.removeprefix(prefix),)
                if re.search(rf"(?<![A-Za-z0-9_]){re.escape(variable)}(?![A-Za-z0-9_])", text)
            )
        )

    def _result(
        self,
        result: str,
        *,
        assert_text: str,
        reason: str,
        audit: AuditReport,
        before: str,
        after: str,
        value: bool | None = None,
        error: dict[str, Any] | None = None,
        required: tuple[str, ...] = (),
    ) -> EvalAssertResult:
        if result == RESULT_TRUE:
            match = "matches"
        elif result == RESULT_FALSE:
            match = "contradicts"
        else:
            match = "inconclusive"
        return EvalAssertResult(
            result=result,
            match_status=match,
            value=value if isinstance(value, bool) else None,
            assert_text=assert_text,
            assert_sha256=sha256_text(assert_text),
            reason=str(reason),
            audit=audit.to_json(),
            vars_hash_before=before,
            vars_hash_after=after,
            function_registry_hash=self.function_registry_hash,
            function_call_trace=tuple(self.call_trace),
            actual_function_families=tuple(sorted({record.family for record in self.call_trace if record.status == "completed"})),
            required_function_families=required,
            error=error,
        )


def build_eval_environment(**kwargs: Any) -> EvalEnvironment:
    """Construct ``EvalEnvironment`` from controller-frozen artifacts.

    Parameters, returns, execution, failure semantics, limitations, permissions
    and example are identical to ``EvalEnvironment``; this helper exists as a
    stable import target for future Agent-facing ``eval_assert`` wiring.
    Example: ``build_eval_environment(model_text=model).eval_assert("len(states())>0",
    "structure smoke", required_function_families=["structure"])``.
    """

    return EvalEnvironment(**kwargs)


__all__ = [
    "EvalAssertResult",
    "EvalEnvironment",
    "FunctionCallRecord",
    "ALLOWED_FUNCTION_FAMILIES",
    "UnsupportedEvidence",
    "build_eval_environment",
    "RESULT_EXCEPTION",
    "RESULT_FALSE",
    "RESULT_NO_MODEL_EVIDENCE",
    "RESULT_NON_BOOL",
    "RESULT_REQUIRED_FAMILY_MISSING",
    "RESULT_TIMEOUT",
    "RESULT_TRUE",
    "RESULT_UNSUPPORTED",
    "RESULT_UNTRACKED",
]
