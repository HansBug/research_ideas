from __future__ import annotations

import copy
import signal
import threading
import traceback
from dataclasses import dataclass, field
from typing import Any, Callable

from .pyfcstm_adapter import check_fcstm, sha256_text
from .pyfcstm_adapter import load_model_for_simulation
from .effects import EffectAPI
from .exceptions import UnsupportedEvidence
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
        self.timeout_seconds = timeout_seconds
        self.call_trace: list[FunctionCallRecord] = []

        self.structure = StructureAPI(self.inspect)
        self.relations = RelationAPI(self.structure)
        self.effects = EffectAPI(self.structure)
        self.simulation = SimulationAPI(model_text, model_path)
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

        functions: dict[str, tuple[str, Callable[..., Any]]] = {
            "states": ("structure", self.structure.states),
            "events": ("structure", self.structure.events),
            "variables": ("structure", self.structure.variables),
            "initial_child": ("structure", self.structure.initial_child),
            "transitions": ("relation", self.relations.transitions),
            "transition_exists": ("relation", self.relations.transition_exists),
            "guards_overlap": ("relation", self.relations.guards_overlap),
            "effects": ("effect", self.effects.effects),
            "effect_delta": ("effect", self.effects.effect_delta),
            "effect_deltas": ("effect", self.effects.effect_deltas),
            "simulate": ("simulation", self.simulation.simulate),
            "mapped_source_refs": ("mapping", self.mapping.mapped_source_refs),
            "mapped_fcstm_refs": ("mapping", self.mapping.mapped_fcstm_refs),
            "bound_model_refs": ("mapping", self.mapping.bound_model_refs),
        }
        if self.topology_api is not None:
            functions.update(
                {
                    "topology": ("structure", self.topology_api.topology),
                    "path": ("structure", self.topology_api.path),
                }
            )
        if formal_verification_enabled:
            functions["fbmcq"] = ("formal", self.fbmcq_api.fbmcq)
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
