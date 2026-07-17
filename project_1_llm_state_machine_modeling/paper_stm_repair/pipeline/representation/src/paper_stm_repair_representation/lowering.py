from __future__ import annotations

import json
import shutil
from dataclasses import dataclass, field, fields, is_dataclass
from pathlib import Path
from typing import Any, Dict, Optional

from pyfcstm.diagnostics.inspect import inspect_model
from pyfcstm.model.load import load_state_machine_from_text

from .pyfcstm_names import NameRegistry


def repo_root_from_file() -> Path:
    cur = Path(__file__).resolve()
    for parent in [cur, *cur.parents]:
        if (parent / ".git").exists() and (parent / "project_1_llm_state_machine_modeling").exists():
            return parent
    raise RuntimeError("repository root not found")


REPO_ROOT = repo_root_from_file()
PAPER_ROOT = REPO_ROOT / "project_1_llm_state_machine_modeling/paper_stm_repair"
PIPELINE_ROOT = PAPER_ROOT / "pipeline"
CONVERSION_REPORTS = PIPELINE_ROOT / "conversion/reports"
CANONICAL_DIR = CONVERSION_REPORTS / "canonical"

BLOCKED_NO_CANONICAL = "R45.BLOCKED.no_canonical_from_r3"
BLOCKED_TTOOL = "R45.BLOCKED.ttool_unresolved_endpoint_inventory_only"
LOSS_CROSS_SCOPE = "R45.LOSS.cross_scope_transition_unrepresentable"
LOSS_PARENT_TARGET = "R45.LOSS.composite_target_lowered_to_initial_child"
LOSS_BOOL_DEFAULT = "R45.LOSS.bool_guard_variable_default_zero"
LOSS_TIMING_EVENT = "R45.LOSS.timing_event_without_clock_semantics"
LOSS_INITIAL_INFERRED = "R45.LOSS.initial_inferred_from_source_order_or_start_state"
LOSS_CONDITION_EVENT = "R45.LOSS.condition_like_label_lowered_as_event"


@dataclass
class RenderedTransition:
    transition_id: str
    scope: str
    line: Optional[str]
    status: str
    reason_code: str
    source: str
    target: str
    event: Optional[str]
    guard: Optional[str]
    action: Optional[str]
    relay_identifier: Optional[str] = None
    loss_notes: list[str] = field(default_factory=list)


def _schema_safe(obj: Any) -> Any:
    """Recursively convert pyfcstm inspection objects into JSON-safe values.

    pyfcstm diagnostics now embed structured dataclasses such as ``Span``.
    Downstream R4.5 reports need those fields preserved as schema data rather
    than collapsed through ``str(diagnostic)`` or left as unserializable Python
    objects.
    """

    if obj is None or isinstance(obj, (str, int, float, bool)):
        return obj
    if is_dataclass(obj) and not isinstance(obj, type):
        return {field.name: _schema_safe(getattr(obj, field.name)) for field in fields(obj)}
    if isinstance(obj, dict):
        return {str(key): _schema_safe(value) for key, value in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_schema_safe(value) for value in obj]
    if isinstance(obj, set):
        return [_schema_safe(value) for value in sorted(obj, key=repr)]
    if isinstance(obj, Path):
        return display_path(obj)
    if hasattr(obj, "__dict__"):
        return {str(key): _schema_safe(value) for key, value in vars(obj).items()}
    return str(obj)


def _json_dumps(obj: Any) -> str:
    return json.dumps(_schema_safe(obj), ensure_ascii=False, indent=2, sort_keys=True)


def dsl_string(text: str) -> str:
    return json.dumps(text, ensure_ascii=False)


def load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(_json_dumps(data) + "\n", encoding="utf-8")


def display_path(path: Path) -> str:
    resolved = path.resolve()
    try:
        return str(resolved.relative_to(REPO_ROOT))
    except ValueError:
        return str(resolved)


def sha256_file(path: Path) -> str:
    import hashlib

    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_path_for(example_id: str) -> Path:
    return CANONICAL_DIR / f"{example_id}.canonical_stm.json"


def fcstm_metrics_from_parse_report(parse_report: Dict[str, Any]) -> Dict[str, Any]:
    metrics = parse_report.get("metrics") or {}
    if parse_report.get("parse_status") != "ok":
        return {
            "fcstm_parse_status": parse_report.get("parse_status"),
            "fcstm_inspect_status": parse_report.get("inspect_status"),
        }
    return {
        "fcstm_parse_status": parse_report.get("parse_status"),
        "fcstm_inspect_status": parse_report.get("inspect_status"),
        "fcstm_states_leaf": metrics.get("n_states_leaf"),
        "fcstm_states_composite": metrics.get("n_states_composite"),
        "fcstm_states_pseudo": metrics.get("n_states_pseudo"),
        "fcstm_transitions_normal": metrics.get("n_transitions_normal"),
        "fcstm_transitions_forced": metrics.get("n_transitions_forced"),
        "fcstm_events": metrics.get("n_events"),
        "fcstm_variables": metrics.get("n_variables"),
        "fcstm_max_hierarchy_depth": metrics.get("max_hierarchy_depth"),
    }


def source_traceability_from_conversion_item(
    *,
    example_id: str,
    conversion_item: Dict[str, Any],
    selected_example_dir: Path,
    source_nl_path: Path,
    source_stm0_path: Optional[Path],
    source_meta_path: Path,
) -> Dict[str, Any]:
    return {
        "example_id": example_id,
        "upstream_r3_status": conversion_item.get("status"),
        "upstream_r3_status_reason_code": conversion_item.get("status_reason_code"),
        "upstream_source_format": conversion_item.get("source_format"),
        "upstream_conversion_source": conversion_item.get("conversion_source"),
        "upstream_source_nl_path": conversion_item.get("source_nl_path"),
        "upstream_source_stm0_path": conversion_item.get("source_stm0_path"),
        "upstream_source_meta_path": conversion_item.get("source_meta_path"),
        "selected_example_dir": display_path(selected_example_dir),
        "source_nl_path": display_path(source_nl_path),
        "source_stm0_path": display_path(source_stm0_path) if source_stm0_path else None,
        "source_meta_path": display_path(source_meta_path),
        "canonical_output_path": conversion_item.get("canonical_output_path"),
        "canonical_output_sha256": conversion_item.get("canonical_output_sha256"),
        "source_sha256": conversion_item.get("source_sha256"),
        "raw_locator": conversion_item.get("raw_locator"),
        "r3_1_normalization_replay_used": any(
            diag.get("code") == "R3.R31.NORMALIZED_SCXML_REPLAY_USED"
            for diag in conversion_item.get("diagnostics", [])
        ),
        "repair_contribution_allowed": False,
        "attribution": "representation_lowering_not_repair",
    }


def is_condition_like_event_label(raw_event: Optional[str]) -> bool:
    """Return whether a PlantUML/SCXML event label looks like a condition.

    R3 obtains PlantUML canonical models through official SCXML export.  In
    that structured export, labels such as ``dist_to_front<25 && extra_lane=true``
    or ``Front Distance > 10`` arrive as SCXML ``event`` attributes rather than
    as guard expressions.  R4.5 must preserve them as named events for
    traceability, but it also has to record the semantic caveat explicitly so
    later repair/evaluation stages do not mistake the emitted event for a
    recovered pyfcstm guard.
    """

    if not raw_event:
        return False
    text = raw_event.strip()
    condition_tokens = ("&&", "||", "<=", ">=", "==", "!=", "<", ">")
    if any(token in text for token in condition_tokens):
        return True
    lowered = text.lower()
    return "=true" in lowered or "=false" in lowered


class CanonicalModelView:
    def __init__(self, doc: Dict[str, Any]) -> None:
        self.doc = doc
        self.example_id = doc["example_id"]
        self.seed_id = doc["seed_id"]
        self.model = doc["model"]
        self.states: list[Dict[str, Any]] = list(self.model.get("states", []))
        self.transitions: list[Dict[str, Any]] = list(self.model.get("transitions", []))
        self.state_by_id = {s["id"]: s for s in self.states}
        self.children: Dict[Optional[str], list[Dict[str, Any]]] = {}
        for state in self.states:
            self.children.setdefault(state.get("parent"), []).append(state)
        self.parent_by_id = {s["id"]: s.get("parent") for s in self.states}

    def state_kind(self, state_id: str) -> str:
        return self.state_by_id.get(state_id, {}).get("kind", "unknown")

    def state_parent(self, state_id: str) -> Optional[str]:
        return self.parent_by_id.get(state_id)

    def direct_children(self, state_id: Optional[str]) -> list[Dict[str, Any]]:
        return self.children.get(state_id, [])

    def is_composite(self, state_id: str) -> bool:
        return self.state_kind(state_id) == "composite" or bool(self.direct_children(state_id))

    def is_pseudo_like(self, state_id: str) -> bool:
        state = self.state_by_id.get(state_id, {})
        kind = state.get("kind")
        label = str(state.get("label") or state_id)
        # SCXML exports from PlantUML/Umple often encode initial pseudostates as
        # ordinary states named ``start*``. Treat only nodes with an outgoing
        # transition as pseudo-like so ordinary domain states named Start are not
        # silently changed.
        has_outgoing = any(t.get("source") == state_id for t in self.transitions)
        return kind in {"initial", "choice"} or (label.startswith("start") and has_outgoing)

    def state_raw_label(self, state_id: str) -> str:
        state = self.state_by_id[state_id]
        return state.get("label") or state.get("id") or state_id

    def composite_ids(self) -> list[Optional[str]]:
        ids: list[Optional[str]] = [None]
        ids.extend(s["id"] for s in self.states if self.is_composite(s["id"]))
        return ids

    def initial_for_scope(self, scope_id: Optional[str]) -> tuple[Optional[str], str, str]:
        children = self.direct_children(scope_id)
        child_ids = {s["id"] for s in children}
        if scope_id is None:
            for init in self.model.get("initial_states", []):
                if init in child_ids:
                    return init, "explicit_canonical_initial_states", "R45.INIT.explicit_root"
        # SCXML-derived start-like state is the most common per-composite signal.
        if scope_id is not None:
            expected = f"start{scope_id.split('::')[-1].split('.')[-1]}"
            for state in children:
                if state["id"] == expected or state.get("label") == expected:
                    return state["id"], "scoped_start_state_name", "R45.INIT.scoped_start_state_name"
            for transition in self.transitions:
                if transition.get("scope") == scope_id and transition.get("source") in child_ids:
                    source = transition["source"]
                    if source.lower().startswith("start"):
                        return source, "scoped_start_transition_source", "R45.INIT.scoped_start_transition_source"
        if children:
            return children[0]["id"], "source_order_inference", LOSS_INITIAL_INFERRED
        return None, "no_child", "R45.INIT.no_child_blocked"

    def path_parts(self, state_id: str) -> list[str]:
        parts = [state_id]
        parent = self.state_parent(state_id)
        while parent is not None:
            parts.append(parent)
            parent = self.state_parent(parent)
        return list(reversed(parts))


def map_guard(raw_guard: Optional[str], emitted_vars: Optional[Dict[str, str]] = None) -> tuple[Optional[str], list[str], str, str]:
    if raw_guard is None:
        return None, [], "none", "R45.GUARD.none"
    guard = raw_guard.strip()
    if not guard:
        return None, [], "empty", "R45.GUARD.empty"
    emitted_vars = emitted_vars or {}
    if guard.startswith("!") and guard[1:].replace("_", "").isalnum():
        raw_var = NameRegistry.base_identifier(guard[1:])
        emitted_var = emitted_vars.get(raw_var, raw_var)
        return f"{emitted_var} == 0", [raw_var], "negated_bool_as_int_zero", "R45.GUARD.negated_bool_supported"
    if guard.replace("_", "").isalnum():
        raw_var = NameRegistry.base_identifier(guard)
        emitted_var = emitted_vars.get(raw_var, raw_var)
        return f"{emitted_var} > 0", [raw_var], "bool_as_int_positive", "R45.GUARD.bool_supported"
    return None, [], "unsupported_complex_expression", "R45.GUARD.unsupported_complex_expression"


def action_identifier(registry: NameRegistry, raw_action: str, scope: str, canonical_ref: str) -> str:
    clean = raw_action.strip().rstrip(";")
    return registry.reserve(
        raw_text=clean,
        canonical_ref=canonical_ref,
        object_type="action_flag",
        scope="variables",
        emitted_path=f"def.{NameRegistry.base_identifier('act_' + clean)}",
        generated_reason="transition_action_flag",
        use_sequence=["act", clean],
    )


def abstract_action_identifier(registry: NameRegistry, raw_action: str, canonical_ref: str) -> str:
    clean = raw_action.strip().rstrip(";")
    return registry.reserve(
        raw_text=clean,
        canonical_ref=canonical_ref,
        object_type="abstract_action",
        scope="abstract_actions",
        emitted_path=f"abstract.{NameRegistry.base_identifier(clean)}",
        generated_reason="entry_action_abstract",
    )


def inspect_fcstm(source: str, path: Path) -> Dict[str, Any]:
    try:
        machine = load_state_machine_from_text(source, path=path)
        report = inspect_model(machine)
        return {
            "schema_version": "r4_5.parse_inspect_report.v0",
            "parse_status": "ok",
            "inspect_status": "ok",
            "metrics": _schema_safe(report.metrics),
            "states": _schema_safe(report.states),
            "transitions": _schema_safe(report.transitions),
            "events": _schema_safe(report.events),
            "variables": _schema_safe(report.variables),
            "diagnostics": _schema_safe(getattr(report, "diagnostics", [])),
        }
    except Exception as exc:  # pragma: no cover - exercised via reports when failing
        return {
            "schema_version": "r4_5.parse_inspect_report.v0",
            "parse_status": "error",
            "inspect_status": "not_run",
            "error_type": type(exc).__name__,
            "error_message": str(exc),
        }


class FCSTMExporter:
    def __init__(self, canonical_doc: Dict[str, Any]) -> None:
        self.view = CanonicalModelView(canonical_doc)
        self.registry = NameRegistry()
        self.loss_rows: list[Dict[str, Any]] = []
        self.state_id_map: Dict[str, str] = {}
        self.event_map: Dict[tuple[str, str], str] = {}
        self.guard_vars: Dict[str, str] = {}
        self.action_flags: Dict[str, str] = {}
        self.abstract_actions: Dict[str, str] = {}
        self.rendered_transitions: list[RenderedTransition] = []
        self.initial_records: list[Dict[str, Any]] = []

    @property
    def root_id(self) -> str:
        return self.state_id_map["__root__"]

    def add_loss(self, *, reason_code: str, severity: str, message: str, canonical_ref: Optional[str], affected_item_id: Optional[str], loss_type: str, repair_contribution_allowed: bool = False, extra: Optional[Dict[str, Any]] = None) -> None:
        row = {
            "schema_version": "r4_5.fcstm_export_loss_ledger.v0",
            "example_id": self.view.example_id,
            "loss_id": f"{self.view.example_id}:{reason_code}:{len(self.loss_rows)+1:04d}",
            "reason_code": reason_code,
            "severity": severity,
            "loss_type": loss_type,
            "message": message,
            "canonical_ref": canonical_ref,
            "affected_item_id": affected_item_id,
            "repair_contribution_allowed": repair_contribution_allowed,
            "attribution": "representation_lowering_not_repair",
        }
        if extra:
            row["extra"] = extra
        self.loss_rows.append(row)

    def reserve_names(self) -> None:
        root_raw = self.view.model.get("name") or self.view.example_id
        root = self.registry.reserve(
            raw_text=root_raw,
            canonical_ref=f"canonical:{self.view.example_id}:model.name",
            object_type="root_state",
            scope="root",
            emitted_path=NameRegistry.base_identifier(root_raw),
            generated_reason="root_wrapper_state",
        )
        self.state_id_map["__root__"] = root
        for state in self.view.states:
            parent = state.get("parent") or "__root__"
            scope = self.state_id_map.get(parent, NameRegistry.base_identifier(str(parent)))
            ident = self.registry.reserve(
                raw_text=state.get("label") or state["id"],
                canonical_ref=state.get("raw_ref") or f"canonical:{self.view.example_id}:state:{state['id']}",
                object_type="pseudo_state" if self.view.is_pseudo_like(state["id"]) else "state",
                scope=scope,
                generated_reason="canonical_state_identifier",
            )
            self.state_id_map[state["id"]] = ident

    def event_scope_for_transition(self, transition: Dict[str, Any]) -> str:
        if transition.get("scope"):
            return transition["scope"]
        source = transition.get("source")
        target = transition.get("target")
        if source in self.view.state_by_id and self.view.is_composite(source):
            source_children = {s["id"] for s in self.view.direct_children(source)}
            if target in source_children:
                return source
        parent = self.view.state_parent(source) if source in self.view.state_by_id else None
        return parent or "__root__"

    def event_identifier(self, raw_event: str, scope: str, transition_id: str) -> str:
        key = (scope, raw_event)
        if key not in self.event_map:
            scope_name = self.state_id_map.get(scope, self.root_id if scope == "__root__" else NameRegistry.base_identifier(scope))
            ident = self.registry.reserve(
                raw_text=raw_event,
                canonical_ref=f"canonical:{self.view.example_id}:event:{transition_id}",
                object_type="event",
                scope=scope_name,
                emitted_path=f"{scope_name}.{NameRegistry.base_identifier(raw_event)}",
                generated_reason="transition_event_declaration",
            )
            self.event_map[key] = ident
        return self.event_map[key]

    def record_condition_like_event_loss(self, transition: Dict[str, Any], event_ident: Optional[str]) -> None:
        raw_event = transition.get("event")
        if not raw_event or not is_condition_like_event_label(raw_event):
            return
        loss_id = f"{self.view.example_id}:{LOSS_CONDITION_EVENT}:{transition.get('id')}"
        if any(row["loss_id"] == loss_id for row in self.loss_rows):
            return
        self.loss_rows.append({
            "schema_version": "r4_5.fcstm_export_loss_ledger.v0",
            "example_id": self.view.example_id,
            "loss_id": loss_id,
            "reason_code": LOSS_CONDITION_EVENT,
            "severity": "known_semantic_approximation",
            "loss_type": "condition_label_as_event",
            "message": "Official PlantUML/SCXML export exposed a condition-like transition label as an event; R4.5 preserves it as a named event and does not claim recovered guard semantics.",
            "canonical_ref": transition.get("raw_ref"),
            "affected_item_id": transition.get("id"),
            "repair_contribution_allowed": False,
            "attribution": "representation_lowering_not_repair",
            "extra": {
                "raw_event": raw_event,
                "emitted_event": event_ident,
                "source_format": self.view.doc.get("source_format"),
                "conversion_source": self.view.doc.get("metadata", {}).get("conversion_source"),
                "guard_field": transition.get("guard"),
                "rationale": "PlantUML labels with comparison/logical syntax are kept as trigger labels because R3 canonical did not prove they are executable guards.",
            },
        })

    def declare_guard_vars(self, raw_guard: Optional[str], transition: Dict[str, Any]) -> Optional[str]:
        mapped, vars_, _, code = map_guard(raw_guard, self.guard_vars)
        if mapped is None and raw_guard:
            self.add_loss(
                reason_code=code,
                severity="blocking_transition",
                message=f"Unsupported guard expression {raw_guard!r}; transition will not be emitted.",
                canonical_ref=transition.get("raw_ref"),
                affected_item_id=transition.get("id"),
                loss_type="guard_expression",
                extra={"raw_guard": raw_guard},
            )
            return None
        for var in vars_:
            if var not in self.guard_vars:
                emitted = self.registry.reserve(
                    raw_text=var,
                    canonical_ref=f"canonical:{self.view.example_id}:guard:{transition.get('id')}",
                    object_type="guard_variable",
                    scope="variables",
                    emitted_path=f"def.{NameRegistry.base_identifier(var)}",
                    generated_reason="bool_guard_int_variable",
                )
                self.guard_vars[var] = emitted
                self.add_loss(
                    reason_code=LOSS_BOOL_DEFAULT,
                    severity="known_semantic_approximation",
                    message=f"Boolean-like guard variable {emitted} is declared as int with default 0; raw undefined/init semantics are not recovered in R4.5.",
                    canonical_ref=transition.get("raw_ref"),
                    affected_item_id=transition.get("id"),
                    loss_type="variable_default",
                    extra={"raw_variable": var, "emitted_variable": emitted, "default_value": 0, "raw_guard": raw_guard},
                )
        mapped, _, _, _ = map_guard(raw_guard, self.guard_vars)
        return mapped

    def effect_for_action(self, action: Optional[str], transition: Dict[str, Any]) -> tuple[str, Optional[str]]:
        if not action:
            return "", None
        if action not in self.action_flags:
            self.action_flags[action] = action_identifier(self.registry, action, "variables", transition.get("raw_ref") or transition["id"])
        return f" effect {{ {self.action_flags[action]} = 1; }}", self.action_flags[action]

    def transition_scope_parent(self, source: str, target: str, scope: str) -> Optional[str]:
        source_parent = self.view.state_parent(source) if source in self.view.state_by_id else None
        target_parent = self.view.state_parent(target) if target in self.view.state_by_id else None
        if scope == "__root__":
            return None
        return scope if source_parent == scope or target_parent == scope else source_parent

    def _scope_children_ids(self, scope: str) -> set[str]:
        return {s["id"] for s in self.view.direct_children(None if scope == "__root__" else scope)}

    def nearest_child_under_scope(self, state_id: str, scope: str) -> Optional[str]:
        """Return the direct child of ``scope`` that contains ``state_id``."""

        child_ids = self._scope_children_ids(scope)
        current: Optional[str] = state_id
        while current is not None:
            if current in child_ids:
                return current
            current = self.view.state_parent(current)
        return None

    def choose_render_scope_and_endpoints(self, source: str, target: str, transition: Dict[str, Any]) -> tuple[str, str, str, list[Dict[str, Any]]]:
        """Choose a pyfcstm sibling scope without flattening hierarchy.

        pyfcstm transition endpoints are short identifiers resolved within the
        state body where the transition is declared.  When R3 canonical carries
        a nested SCXML transition that exits a sub-composite, R4.5 lifts the
        endpoint to the nearest direct child of the render scope and records the
        representation approximation in the loss ledger.
        """

        notes: list[Dict[str, Any]] = []
        source_parent = self.view.state_parent(source) or "__root__"
        target_parent = self.view.state_parent(target) or "__root__"

        # The normal case: source and target are siblings in the transition scope.
        declared_scope = transition.get("scope") or source_parent
        if declared_scope and declared_scope != "__root__":
            child_ids = self._scope_children_ids(declared_scope)
            if source in child_ids and target in child_ids:
                return declared_scope, source, target, notes

        if source_parent == target_parent:
            return source_parent, source, target, notes

        # Target is an ancestor of the source.  Re-enter the ancestor through its
        # initial direct child in the ancestor's parent scope.
        ancestors = set()
        cur: Optional[str] = source
        while cur is not None:
            ancestors.add(cur)
            cur = self.view.state_parent(cur)
        if target in ancestors:
            render_scope = target
            source_endpoint = self.nearest_child_under_scope(source, render_scope)
            initial, method, code = self.view.initial_for_scope(target)
            target_endpoint = initial
            if source_endpoint and target_endpoint:
                notes.append({
                    "reason_code": LOSS_PARENT_TARGET,
                    "loss_type": "ancestor_target_reentry",
                    "message": f"Transition target ancestor {target!r} is represented as re-entry to initial child {target_endpoint!r} inside the ancestor scope.",
                    "extra": {"target_ancestor": target, "lowered_target": target_endpoint, "derivation_method": method, "derivation_code": code},
                })
                return render_scope, source_endpoint, target_endpoint, notes

        # Nested source exits to a state in an ancestor scope.  Declare the
        # transition at that ancestor scope from the nearest composite child.
        render_scope = target_parent
        source_endpoint = self.nearest_child_under_scope(source, render_scope)
        if source_endpoint and target in self._scope_children_ids(render_scope):
            if source_endpoint != source:
                notes.append({
                    "reason_code": "R45.LOSS.source_lifted_to_composite_boundary",
                    "loss_type": "source_scope_lift",
                    "message": f"Nested source {source!r} is represented by composite boundary {source_endpoint!r} in scope {render_scope!r}.",
                    "extra": {"raw_source": source, "lifted_source": source_endpoint, "render_scope": render_scope},
                })
            return render_scope, source_endpoint, target, notes

        # Source in ancestor scope entering a target nested inside a child
        # composite.  Prefer targeting the composite child itself; pyfcstm can
        # enter its own [*] child.
        render_scope = source_parent
        target_endpoint = self.nearest_child_under_scope(target, render_scope)
        if source in self._scope_children_ids(render_scope) and target_endpoint:
            if target_endpoint != target:
                notes.append({
                    "reason_code": "R45.LOSS.target_lifted_to_composite_boundary",
                    "loss_type": "target_scope_lift",
                    "message": f"Nested target {target!r} is represented by composite boundary {target_endpoint!r} in scope {render_scope!r}.",
                    "extra": {"raw_target": target, "lifted_target": target_endpoint, "render_scope": render_scope},
                })
            return render_scope, source, target_endpoint, notes

        return declared_scope or source_parent, source, target, notes

    def can_render_in_scope(self, source: str, target: str, render_scope: str) -> bool:
        child_ids = self._scope_children_ids(render_scope)
        return source in child_ids and target in child_ids

    def render_transition(self, transition: Dict[str, Any]) -> None:
        source = transition.get("source")
        target = transition.get("target")
        if source not in self.view.state_by_id or target not in self.view.state_by_id:
            self.rendered_transitions.append(RenderedTransition(transition["id"], "", None, "blocked", "R45.BLOCKED.unresolved_endpoint", source, target, transition.get("event"), transition.get("guard"), transition.get("action")))
            self.add_loss(reason_code="R45.BLOCKED.unresolved_endpoint", severity="blocking_transition", message="Transition endpoint is unresolved in R3 canonical inventory.", canonical_ref=transition.get("raw_ref"), affected_item_id=transition.get("id"), loss_type="reference", extra={"source": source, "target": target})
            return
        mapped_guard = self.declare_guard_vars(transition.get("guard"), transition)
        if transition.get("guard") and mapped_guard is None:
            self.rendered_transitions.append(RenderedTransition(transition["id"], "", None, "blocked", "R45.BLOCKED.unsupported_guard", source, target, transition.get("event"), transition.get("guard"), transition.get("action")))
            return
        effect, action_flag = self.effect_for_action(transition.get("action"), transition)
        event = transition.get("event")

        # A transition attached to a composite source and targeting one of its
        # direct children means "from anywhere inside this composite, exit/enter
        # that child" in the SCXML-derived canonical view. pyfcstm's native
        # representation for that pattern is a forced transition inside the
        # composite scope.  This preserves hierarchy without inventing a normal
        # stoppable relay state.
        if self.view.is_composite(source) and target in self._scope_children_ids(source):
            event_ident = self.event_identifier(event, source, transition["id"]) if event else None
            self.record_condition_like_event_loss(transition, event_ident)
            if effect:
                self.add_loss(reason_code="R45.LOSS.forced_transition_effect_not_supported", severity="blocking_transition", message="pyfcstm forced transitions do not support effect blocks; transition action prevents forced composite lowering.", canonical_ref=transition.get("raw_ref"), affected_item_id=transition["id"], loss_type="transition_action", extra={"action": transition.get("action")})
                self.rendered_transitions.append(RenderedTransition(transition["id"], source, None, "blocked", "R45.BLOCKED.forced_effect", source, target, event, transition.get("guard"), transition.get("action")))
                return
            to_id = self.state_id_map[target]
            if mapped_guard:
                line = f"! * -> {to_id} : if [{mapped_guard}];"
            elif event_ident:
                line = f"! * -> {to_id} : {event_ident};"
            else:
                line = f"! * -> {to_id};"
            self.rendered_transitions.append(RenderedTransition(transition["id"], source, line, "emitted", "R45.TRANSITION.composite_forced", source, target, event, transition.get("guard"), transition.get("action")))
            return

        render_scope, source2, target2, scope_notes = self.choose_render_scope_and_endpoints(source, target, transition)
        for note in scope_notes:
            self.add_loss(
                reason_code=note["reason_code"],
                severity="known_semantic_approximation",
                message=note["message"],
                canonical_ref=transition.get("raw_ref"),
                affected_item_id=transition["id"],
                loss_type=note["loss_type"],
                extra=note.get("extra"),
            )
        event_scope = render_scope if event else "__root__"
        event_ident = self.event_identifier(event, event_scope, transition["id"]) if event else None
        self.record_condition_like_event_loss(transition, event_ident)

        if not self.can_render_in_scope(source2, target2, render_scope):
            self.add_loss(reason_code=LOSS_CROSS_SCOPE, severity="blocking_transition", message="Transition cannot be represented without flattening because source and target are not siblings in the selected pyfcstm scope.", canonical_ref=transition.get("raw_ref"), affected_item_id=transition["id"], loss_type="cross_scope_reference", extra={"source": source, "target": target, "chosen_source": source2, "chosen_target": target2, "render_scope": render_scope, "source_parent": self.view.state_parent(source), "target_parent": self.view.state_parent(target2)})
            self.rendered_transitions.append(RenderedTransition(transition["id"], render_scope, None, "blocked", LOSS_CROSS_SCOPE, source2, target2, event, transition.get("guard"), transition.get("action")))
            return

        src_id = self.state_id_map[source2]
        tgt_id = self.state_id_map[target2]
        if event_ident and mapped_guard:
            relay = self.registry.reserve(
                raw_text=f"{source} {event} {transition.get('guard')} {target2}",
                canonical_ref=transition.get("raw_ref") or transition["id"],
                object_type="pseudo_relay",
                scope=self.state_id_map.get(render_scope, self.root_id),
                generated_reason="event_guard_pseudo_relay",
                use_sequence=[source, event, transition.get("guard") or "guard", target2, "relay"],
            )
            first = f"{src_id} -> {relay} : {event_ident};"
            second = f"{relay} -> {tgt_id} : if [{mapped_guard}]{effect};"
            line = first + "\n" + second
            self.rendered_transitions.append(RenderedTransition(transition["id"], render_scope, line, "emitted", "R45.TRANSITION.event_guard_pseudo_relay", source, target2, event, transition.get("guard"), transition.get("action"), relay_identifier=relay))
            return
        if event_ident:
            line = f"{src_id} -> {tgt_id} : {event_ident}{effect};"
        elif mapped_guard:
            line = f"{src_id} -> {tgt_id} : if [{mapped_guard}]{effect};"
        else:
            line = f"{src_id} -> {tgt_id}{effect};"
        self.rendered_transitions.append(RenderedTransition(transition["id"], render_scope, line, "emitted", "R45.TRANSITION.direct", source, target2, event, transition.get("guard"), transition.get("action")))

    def build_inventory(self) -> Dict[str, Any]:
        events = []
        for (scope, raw_event), event_id in sorted(self.event_map.items()):
            events.append({"raw_event": raw_event, "scope": scope, "emitted_identifier": event_id, "declaration_path": f"{self.state_id_map.get(scope, self.root_id)}.{event_id}", "status": "declared"})
        guards = []
        for t in self.view.transitions:
            if t.get("guard"):
                mapped, vars_, strategy, code = map_guard(t.get("guard"), self.guard_vars)
                guards.append({"transition_id": t["id"], "raw_guard": t.get("guard"), "mapped_expression": mapped, "declared_variables": [self.guard_vars.get(v, v) for v in vars_], "raw_variables": vars_, "strategy": strategy, "reason_code": code, "supported": mapped is not None})
        actions = []
        for t in self.view.transitions:
            if t.get("action"):
                actions.append({"transition_id": t["id"], "raw_action": t.get("action"), "lowering": "transition_action_flag", "emitted_flag": self.action_flags.get(t.get("action")), "status": "mapped" if t.get("action") in self.action_flags else "not_emitted"})
        references = []
        for rt in self.rendered_transitions:
            references.append(_schema_safe(rt))
        hierarchy = []
        for state in self.view.states:
            hierarchy.append({"state_id": state["id"], "parent": state.get("parent"), "emitted_identifier": self.state_id_map.get(state["id"]), "kind": state.get("kind"), "status": "preserved" if state.get("parent") is not None or self.view.is_composite(state["id"]) else "top_level_child"})
        timing = []
        for t in self.view.transitions:
            event = t.get("event") or ""
            if "timeout" in event.lower() or self.view.model.get("timing_level") not in {"none", "unknown"}:
                timing.append({"transition_id": t["id"], "raw_event": t.get("event"), "raw_guard": t.get("guard"), "timing_level": self.view.model.get("timing_level"), "lowering": "event_only_no_clock_recovery", "reason_code": LOSS_TIMING_EVENT if event else "R45.TIMING.inventory_only"})
        return {
            "schema_version": "r4_5.lowering_inventory.v0",
            "example_id": self.view.example_id,
            "seed_id": self.view.seed_id,
            "source_status": self.view.doc.get("status"),
            "counts": {
                "canonical_states": len(self.view.states),
                "canonical_transitions": len(self.view.transitions),
                "events_declared": len(events),
                "guards": len(guards),
                "actions": len(actions),
                "references": len(references),
                "composite_initials": len(self.initial_records),
                "hierarchy_items": len(hierarchy),
                "timing_items": len(timing),
            },
            "events": events,
            "guards": guards,
            "actions": actions,
            "references": references,
            "initial_final": self.initial_records,
            "timing": timing,
            "hierarchy": hierarchy,
            "blocked_supplementary": [],
        }

    def render_scope(self, scope_id: Optional[str], indent: int = 0) -> list[str]:
        lines: list[str] = []
        pad = " " * indent
        if scope_id is None:
            name = self.root_id
            raw = self.view.model.get("name") or self.view.example_id
            lines.append(f"state {name} named {dsl_string(raw)} {{")
            body_indent = indent + 4
        else:
            state = self.view.state_by_id[scope_id]
            name = self.state_id_map[scope_id]
            raw = state.get("label") or scope_id
            is_pseudo = self.view.is_pseudo_like(scope_id)
            keyword = "pseudo state" if is_pseudo else "state"
            if self.view.is_composite(scope_id):
                lines.append(f"{pad}{keyword} {name} named {dsl_string(raw)} {{")
                body_indent = indent + 4
            else:
                lines.append(f"{pad}{keyword} {name} named {dsl_string(raw)};")
                return lines

        body_pad = " " * body_indent
        initial, method, code = self.view.initial_for_scope(None if scope_id is None else scope_id)
        if initial and initial in self.state_id_map:
            lines.append(f"{body_pad}[*] -> {self.state_id_map[initial]};")
            self.initial_records.append({"scope": "__root__" if scope_id is None else scope_id, "target": initial, "emitted_target": self.state_id_map[initial], "derivation_method": method, "reason_code": code, "status": "emitted"})
            if code == LOSS_INITIAL_INFERRED:
                self.add_loss(reason_code=LOSS_INITIAL_INFERRED, severity="known_semantic_approximation", message="Composite/root initial child was inferred from source order because R3 canonical did not provide an explicit initial marker.", canonical_ref=f"canonical:{self.view.example_id}:scope:{scope_id or '__root__'}", affected_item_id=scope_id or "__root__", loss_type="initial_lowering", extra={"target": initial, "derivation_method": method})
        else:
            self.initial_records.append({"scope": "__root__" if scope_id is None else scope_id, "target": None, "emitted_target": None, "derivation_method": method, "reason_code": code, "status": "blocked"})

        # Declare events owned by this scope.
        lookup_scope = "__root__" if scope_id is None else scope_id
        for (event_scope, raw_event), event_id in sorted(self.event_map.items()):
            if event_scope == lookup_scope:
                lines.append(f"{body_pad}event {event_id} named {dsl_string(raw_event)};")

        # Render child states.
        for child in self.view.direct_children(scope_id):
            lines.extend(self.render_scope(child["id"], body_indent))

        # Render synthetic relays before transitions that use them.
        relay_by_scope = [rt for rt in self.rendered_transitions if rt.scope == lookup_scope and rt.relay_identifier]
        for rt in relay_by_scope:
            raw = f"{rt.source} {rt.event} [{rt.guard}] -> {rt.target}"
            lines.append(f"{body_pad}pseudo state {rt.relay_identifier} named {dsl_string(raw)};")

        for rt in self.rendered_transitions:
            if rt.scope == lookup_scope and rt.line:
                for line in rt.line.splitlines():
                    lines.append(f"{body_pad}{line}")
        lines.append(f"{pad}}}")
        return lines

    def export(self) -> Dict[str, Any]:
        self.reserve_names()
        if self.view.example_id == "ttool-automatedbraking-xml":
            return self.export_blocked(BLOCKED_TTOOL, "TTool canonical remains inventory-only because R3 endpoints are unresolved; R4.5 must not fabricate fcstm transitions.")
        for transition in self.view.transitions:
            self.render_transition(transition)
        lines: list[str] = []
        for var in sorted(set(self.guard_vars.values())):
            lines.append(f"def int {var} = 0;")
        for flag in sorted(set(self.action_flags.values())):
            lines.append(f"def int {flag} = 0;")
        if lines:
            lines.append("")
        lines.extend(self.render_scope(None, 0))
        fcstm = "\n".join(lines) + "\n"
        inventory = self.build_inventory()
        blocked = [_schema_safe(rt) for rt in self.rendered_transitions if rt.status == "blocked"]
        status = "converted" if not blocked else "partial"
        return {
            "status": status,
            "status_reason_code": "R45.STATUS.converted" if status == "converted" else "R45.STATUS.partial_cross_scope_losses",
            "fcstm": fcstm,
            "name_mapping": self.registry.to_jsonable(),
            "lowering_inventory": inventory,
            "loss_rows": self.loss_rows,
            "blocked_transitions": blocked,
        }

    def export_blocked(self, reason_code: str, message: str) -> Dict[str, Any]:
        inventory = {
            "schema_version": "r4_5.lowering_inventory.v0",
            "example_id": self.view.example_id,
            "seed_id": self.view.seed_id,
            "source_status": self.view.doc.get("status"),
            "counts": {"canonical_states": len(self.view.states), "canonical_transitions": len(self.view.transitions), "events_declared": 0, "guards": sum(1 for t in self.view.transitions if t.get("guard")), "actions": sum(1 for t in self.view.transitions if t.get("action")), "references": len(self.view.transitions), "composite_initials": len([s for s in self.view.states if s.get("kind") == "composite"]), "hierarchy_items": len(self.view.states), "timing_items": len(self.view.transitions)},
            "events": [],
            "guards": [{"transition_id": t["id"], "raw_guard": t.get("guard"), "supported": False, "reason_code": reason_code} for t in self.view.transitions if t.get("guard")],
            "actions": [],
            "references": [{"transition_id": t["id"], "source": t.get("source"), "target": t.get("target"), "scope": t.get("scope"), "status": "blocked", "reason_code": reason_code} for t in self.view.transitions],
            "initial_final": [{"scope": s["id"], "status": "blocked", "reason_code": reason_code} for s in self.view.states if s.get("kind") == "composite"],
            "timing": [{"transition_id": t["id"], "status": "blocked", "reason_code": reason_code} for t in self.view.transitions],
            "hierarchy": [{"state_id": s["id"], "parent": s.get("parent"), "kind": s.get("kind"), "status": "inventory_only"} for s in self.view.states],
            "blocked_supplementary": [{"reason_code": reason_code, "message": message, "states": len(self.view.states), "transitions": len(self.view.transitions)}],
        }
        self.add_loss(reason_code=reason_code, severity="model_blocking", message=message, canonical_ref=f"canonical:{self.view.example_id}", affected_item_id=self.view.example_id, loss_type="model_blocked")
        return {"status": "blocked", "status_reason_code": reason_code, "fcstm": None, "name_mapping": self.registry.to_jsonable(), "lowering_inventory": inventory, "loss_rows": self.loss_rows, "blocked_transitions": []}


def export_example(example_id: str, conversion_item: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    path = canonical_path_for(example_id)
    if not path.exists():
        return {
            "example_id": example_id,
            "seed_id": conversion_item.get("seed_id") if conversion_item else example_id,
            "status": "blocked",
            "status_reason_code": BLOCKED_NO_CANONICAL,
            "fcstm": None,
            "name_mapping": {"schema_version": "r4_5.name_mapping.v0", "items": []},
            "lowering_inventory": {
                "schema_version": "r4_5.lowering_inventory.v0",
                "example_id": example_id,
                "seed_id": conversion_item.get("seed_id") if conversion_item else example_id,
                "source_status": conversion_item.get("status") if conversion_item else "missing",
                "counts": {"canonical_states": 0, "canonical_transitions": 0, "events_declared": 0, "guards": 0, "actions": 0, "references": 0, "composite_initials": 0, "hierarchy_items": 0, "timing_items": 0},
                "events": [], "guards": [], "actions": [], "references": [], "initial_final": [], "timing": [], "hierarchy": [],
                "blocked_supplementary": [{"reason_code": BLOCKED_NO_CANONICAL, "message": "R3 did not produce trusted canonical STM JSON; R4.5 does not replace the sample or fabricate a model."}],
            },
            "loss_rows": [{"schema_version": "r4_5.fcstm_export_loss_ledger.v0", "example_id": example_id, "loss_id": f"{example_id}:{BLOCKED_NO_CANONICAL}:0001", "reason_code": BLOCKED_NO_CANONICAL, "severity": "model_blocking", "loss_type": "no_canonical", "message": "R3 canonical output is absent; no .fcstm emitted.", "canonical_ref": None, "affected_item_id": example_id, "repair_contribution_allowed": False, "attribution": "representation_lowering_not_repair"}],
            "blocked_transitions": [],
        }
    doc = load_json(path)
    result = FCSTMExporter(doc).export()
    result["example_id"] = example_id
    result["seed_id"] = doc["seed_id"]
    return result


def export_selected(reports_dir: Path, conversion_reports_dir: Path = CONVERSION_REPORTS) -> Dict[str, Any]:
    reports_dir = reports_dir.resolve()
    conversion_reports_dir = conversion_reports_dir.resolve()
    conversion_report = load_json(conversion_reports_dir / "selected_seed_examples_conversion_report.json")
    items = []
    all_inventories = []
    all_losses = []
    for item in conversion_report["items"]:
        example_id = item["example_id"]
        result = export_example(example_id, item)
        example_dir = reports_dir / "fcstm_exports" / example_id
        example_dir.mkdir(parents=True, exist_ok=True)
        if result.get("fcstm"):
            fcstm_path = example_dir / "model.fcstm"
            fcstm_path.write_text(result["fcstm"], encoding="utf-8")
            parse_report = inspect_fcstm(result["fcstm"], fcstm_path)
            write_json(example_dir / "parse_inspect_report.json", parse_report)
        else:
            parse_report = {"schema_version": "r4_5.parse_inspect_report.v0", "parse_status": "not_run", "inspect_status": "not_run", "reason_code": result["status_reason_code"]}
            write_json(example_dir / "parse_inspect_report.json", parse_report)
        result["lowering_inventory"]["counts"].update(fcstm_metrics_from_parse_report(parse_report))
        source_locator = item.get("source_locator")
        selected_example_dir = PAPER_ROOT / "selected_seed_examples" / example_id
        source_nl_path = selected_example_dir / "nl.txt"
        source_stm0_path = PAPER_ROOT / source_locator if source_locator else None
        source_meta_path = selected_example_dir / "source_meta.json"
        source_traceability = source_traceability_from_conversion_item(
            example_id=example_id,
            conversion_item=item,
            selected_example_dir=selected_example_dir,
            source_nl_path=source_nl_path,
            source_stm0_path=source_stm0_path,
            source_meta_path=source_meta_path,
        )
        result["lowering_inventory"]["source_traceability"] = source_traceability
        write_json(example_dir / "name_mapping.json", result["name_mapping"])
        write_json(example_dir / "lowering_inventory.json", result["lowering_inventory"])
        all_inventories.append(result["lowering_inventory"])
        all_losses.extend(result["loss_rows"])
        items.append({
            "example_id": example_id,
            "seed_id": result.get("seed_id"),
            "upstream_r3_status": source_traceability["upstream_r3_status"],
            "upstream_r3_status_reason_code": source_traceability["upstream_r3_status_reason_code"],
            "upstream_source_format": source_traceability["upstream_source_format"],
            "upstream_conversion_source": source_traceability["upstream_conversion_source"],
            "upstream_source_nl_path": source_traceability["upstream_source_nl_path"],
            "upstream_source_stm0_path": source_traceability["upstream_source_stm0_path"],
            "upstream_source_meta_path": source_traceability["upstream_source_meta_path"],
            "status": result["status"],
            "status_reason_code": result["status_reason_code"],
            "fcstm_path": display_path(example_dir / "model.fcstm") if result.get("fcstm") else None,
            "name_mapping_path": display_path(example_dir / "name_mapping.json"),
            "lowering_inventory_path": display_path(example_dir / "lowering_inventory.json"),
            "parse_inspect_report_path": display_path(example_dir / "parse_inspect_report.json"),
            "source_nl_path": source_traceability["source_nl_path"],
            "source_stm0_path": source_traceability["source_stm0_path"],
            "source_meta_path": source_traceability["source_meta_path"],
            "canonical_output_path": source_traceability["canonical_output_path"],
            "parse_status": parse_report.get("parse_status"),
            "inspect_status": parse_report.get("inspect_status"),
            "blocked_transitions_count": len(result.get("blocked_transitions", [])),
            "loss_count": len(result.get("loss_rows", [])),
            "repair_contribution_allowed": False,
            "attribution": "representation_lowering_not_repair",
        })
    report = {"schema_version": "r4_5.fcstm_export_report.v0", "run_id": "committed-r4-5", "items": items, "summary": {"examples": len(items), "converted": sum(1 for i in items if i["status"] == "converted"), "partial": sum(1 for i in items if i["status"] == "partial"), "blocked": sum(1 for i in items if i["status"] == "blocked")}}
    write_json(reports_dir / "fcstm_export_report.json", report)
    write_json(reports_dir / "lowering_inventory.json", {"schema_version": "r4_5.lowering_inventory_bundle.v0", "items": all_inventories})
    with (reports_dir / "fcstm_export_loss_ledger.jsonl").open("w", encoding="utf-8") as f:
        for row in all_losses:
            f.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
    return report


def sync_selected_fcstm_snapshots(
    *,
    reports_dir: Path = PIPELINE_ROOT / "representation/reports",
    selected_dir: Path = PAPER_ROOT / "selected_seed_examples",
) -> Dict[str, Any]:
    """Copy R4.5 ``model.fcstm`` exports into selected smoke examples.

    The selected seed example directories are the handoff surface consumed by
    downstream smoke stages.  They should be self-contained enough for a human
    or R5 script to see the upstream NL, raw ``STM_0`` and the current R4.5
    pyfcstm snapshot together.  The snapshot is still a derived representation
    artifact; this function keeps that attribution explicit in
    ``fcstm_meta.json`` and refuses to invent files for non-converted examples.
    """

    reports_dir = reports_dir.resolve()
    selected_dir = selected_dir.resolve()
    report_path = reports_dir / "fcstm_export_report.json"
    report = load_json(report_path)
    items = []
    for item in report["items"]:
        example_id = item["example_id"]
        example_dir = selected_dir / example_id
        example_dir.mkdir(parents=True, exist_ok=True)
        src_fcstm = REPO_ROOT / item["fcstm_path"] if not Path(item["fcstm_path"]).is_absolute() else Path(item["fcstm_path"])
        dst_fcstm = example_dir / "model.fcstm"
        if item.get("status") != "converted" or item.get("parse_status") != "ok" or item.get("inspect_status") != "ok":
            raise RuntimeError(f"{example_id}: only converted parse/inspect-ok examples may be synchronized")
        if not src_fcstm.is_file():
            raise FileNotFoundError(src_fcstm)
        shutil.copyfile(src_fcstm, dst_fcstm)
        src_hash = sha256_file(src_fcstm)
        dst_hash = sha256_file(dst_fcstm)
        meta = {
            "schema_version": "selected_seed_examples.fcstm_snapshot.v0",
            "example_id": example_id,
            "artifact_role": "r4_5_smoke_converted_fcstm_snapshot",
            "artifact_status": item["status"],
            "parse_status": item["parse_status"],
            "inspect_status": item["inspect_status"],
            "repair_contribution_allowed": False,
            "attribution": "representation_lowering_not_repair",
            "selected_example_dir": display_path(example_dir),
            "selected_fcstm_path": display_path(dst_fcstm),
            "selected_fcstm_sha256": dst_hash,
            "synchronized_from_fcstm_path": item["fcstm_path"],
            "synchronized_from_fcstm_sha256": src_hash,
            "synchronized_from_report_path": display_path(report_path),
            "lowering_inventory_path": item["lowering_inventory_path"],
            "name_mapping_path": item["name_mapping_path"],
            "parse_inspect_report_path": item["parse_inspect_report_path"],
            "source_nl_path": item["source_nl_path"],
            "source_stm0_path": item["source_stm0_path"],
            "source_meta_path": item["source_meta_path"],
            "canonical_output_path": item["canonical_output_path"],
            "upstream_source_format": item["upstream_source_format"],
            "upstream_conversion_source": item["upstream_conversion_source"],
            "upstream_r3_status": item["upstream_r3_status"],
            "upstream_r3_status_reason_code": item["upstream_r3_status_reason_code"],
            "loss_count": item["loss_count"],
            "sync_policy": "This file is a committed smoke convenience snapshot copied from pipeline/representation/reports/fcstm_exports/<example_id>/model.fcstm. Regenerate R4.5 first, then resync this copy; do not edit it by hand.",
        }
        write_json(example_dir / "fcstm_meta.json", meta)
        items.append(
            {
                "example_id": example_id,
                "selected_fcstm_path": meta["selected_fcstm_path"],
                "selected_fcstm_sha256": dst_hash,
                "synchronized_from_fcstm_path": item["fcstm_path"],
                "synchronized_from_fcstm_sha256": src_hash,
                "status": "synced",
            }
        )
    return {
        "schema_version": "selected_seed_examples.fcstm_snapshot_sync.v0",
        "summary": {"examples": len(items), "synced": len(items)},
        "items": items,
    }
