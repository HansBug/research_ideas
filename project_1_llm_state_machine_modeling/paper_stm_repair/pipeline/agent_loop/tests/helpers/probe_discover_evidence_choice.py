from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field

REPO_ROOT = Path(__file__).resolve().parents[6]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

TOOL_NAMES: tuple = (
    "query_structure",
    "simulate_concrete",
    "check_fbmcq",
)
DEFAULT_LIMITS: Dict[str, int] = {
    "model_calls": 4,
    "tool_calls": 3,
    "turns": 4,
    "seconds": 180,
}
LIMITATION_MARKERS: Dict[str, tuple] = {
    "bounded": ("bounded", "analysis_bound", "finite bound", "finite horizon"),
    "concrete": (
        "concrete",
        "single execution",
        "one execution",
        "single trace",
        "one trace",
        "simulation trace",
        "execution witness",
    ),
}


@dataclass(frozen=True)
class ProbeCase:
    case_id: str
    proposition: str
    expected_evidence: tuple
    forbidden_evidence: tuple = ()
    required_limitations: tuple = ()


CASES: tuple = (
    ProbeCase(
        case_id="S1",
        proposition="ManualDriving must have exactly three direct child states.",
        expected_evidence=("query_structure",),
        forbidden_evidence=("simulate_concrete", "check_fbmcq"),
    ),
    ProbeCase(
        case_id="S2",
        proposition=(
            "Given state Root.ManualDriving, variables speed=20 and brake=0, "
            "and one autoMode cycle, report what happens concretely."
        ),
        expected_evidence=("simulate_concrete",),
        required_limitations=("concrete",),
    ),
    ProbeCase(
        case_id="S3",
        proposition=(
            "For all valuations and paths, braking and acceleration must never be active "
            "at the same time. The natural-language requirement gives no analysis bound."
        ),
        expected_evidence=("check_fbmcq",),
        required_limitations=("bounded",),
    ),
    ProbeCase(
        case_id="S4",
        proposition=(
            "All completion paths must return to HumanDriving, and the answer must include "
            "a readable concrete trace."
        ),
        expected_evidence=("check_fbmcq", "simulate_concrete"),
        required_limitations=("bounded", "concrete"),
    ),
)

SYSTEM_PROMPT = """
You are an evidence-choice probe for a state-machine discovery agent.
Choose evidence tools by proposition semantics, not by a fixed order and not by a quota.
The three tools have equal status:
- query_structure answers structural topology questions such as direct children, states, and transitions.
- simulate_concrete answers concrete execution questions for specified states, variables, events, or cycles.
- check_fbmcq answers bounded formal model-checking questions for universal, path, valuation, safety, or reachability claims.
Use the smallest adequate evidence set. Do not use runtime evidence to replace a structural truth.
Use simulation only for concrete traces or examples; never claim that one simulation proves a universal property.
Use FBMCQ for universal or all-path claims even when natural language omits an explicit bound, and state the finite analysis bound as a limitation.
For compound requests, combine independent evidence types when needed.
Return the structured decision after reading the evidence you selected.
All visible text must be English.
""".strip()

USER_PROMPT_TEMPLATE = """
Case: {case_id}
Proposition: {proposition}

Decide which evidence is needed. Call only the read-only evidence tools that are necessary, then return the structured decision.
""".strip()


class EvidenceChoiceDecision(BaseModel):
    case_id: str = Field(description="Probe case identifier, one of S1, S2, S3, or S4.")
    proposition: str = Field(description="The proposition being assessed.")
    selected_evidence: List[str] = Field(
        description="Tool names selected as evidence. Use only query_structure, simulate_concrete, and check_fbmcq."
    )
    answer: str = Field(description="Brief English answer grounded in the selected evidence.")
    limitations: List[str] = Field(description="Important limitations of the selected evidence.")
    rationale: str = Field(description="Why this evidence set is adequate and minimal.")


def query_structure(case_id: str = "", question: str = "") -> Dict[str, Any]:
    """Read state-machine topology, direct child states, and transition structure without executing behavior."""

    return {
        "tool": "query_structure",
        "read_only": True,
        "facts": {
            "ManualDriving.direct_children": ["HumanDriving", "AssistedDriving", "FallbackDriving"],
            "ManualDriving.direct_child_count": 3,
            "completion_transition": "CompletionReview -> HumanDriving",
            "known_completion_states": ["CompletionReview", "HumanDriving"],
        },
        "limitations": [
            "Structure queries do not execute cycles.",
            "Structure queries do not prove all valuation-dependent paths.",
        ],
    }


def simulate_concrete(case_id: str = "", question: str = "") -> Dict[str, Any]:
    """Run a deterministic concrete mock trace for specified initial state, variables, events, or cycles."""

    return {
        "tool": "simulate_concrete",
        "read_only": True,
        "traces": {
            "S2": {
                "initial_state": "Root.ManualDriving",
                "initial_vars": {"speed": 20, "brake": 0},
                "cycles": ["Root.autoMode"],
                "after_state": "Root.AutomaticDriving",
                "consumed_event": "Root.autoMode",
            },
            "S4": {
                "path": ["HumanDriving", "AutoDriving", "CompletionReview", "HumanDriving"],
                "readable_trace": "HumanDriving -> AutoDriving -> CompletionReview -> HumanDriving",
            },
        },
        "limitations": [
            "A concrete simulation is one execution witness, not proof for all paths or valuations.",
        ],
    }


def check_fbmcq(case_id: str = "", question: str = "") -> Dict[str, Any]:
    """Run a bounded formal-model-checking mock query for universal safety or all-path reachability claims."""

    return {
        "tool": "check_fbmcq",
        "read_only": True,
        "results": {
            "S3": {
                "property": "not (braking_active and acceleration_active)",
                "quantification": "all bounded valuations and paths",
                "holds": True,
                "analysis_bound": 8,
                "counterexample": None,
            },
            "S4": {
                "property": "all completion paths return to HumanDriving",
                "quantification": "all bounded completion paths",
                "holds": True,
                "analysis_bound": 6,
                "counterexample": None,
            },
        },
        "limitations": [
            "FBMCQ is bounded and cannot by itself provide a human-readable concrete trace.",
        ],
    }


def sha256_text(text: str) -> str:
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


def stable_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def case_by_id(case_id: str) -> ProbeCase:
    for case in CASES:
        if case.case_id == case_id:
            return case
    raise ValueError(f"unknown case: {case_id}")


def user_prompt(case: ProbeCase) -> str:
    return USER_PROMPT_TEMPLATE.format(case_id=case.case_id, proposition=case.proposition)


def tool_prompt_manifest() -> List[Dict[str, str]]:
    return [
        {"name": name, "description": globals()[name].__doc__ or ""}
        for name in TOOL_NAMES
    ]


def assert_english_visible_prompts() -> None:
    texts = [SYSTEM_PROMPT, USER_PROMPT_TEMPLATE]
    texts.extend(item["description"] for item in tool_prompt_manifest())
    schema = EvidenceChoiceDecision.model_json_schema()
    for value in schema.get("properties", {}).values():
        if isinstance(value, dict) and isinstance(value.get("description"), str):
            texts.append(value["description"])
    for text in texts:
        try:
            text.encode("ascii")
        except UnicodeEncodeError as exc:
            raise AssertionError("visible prompts must be ASCII English") from exc


def normalize_selected(decision: Optional[Union[EvidenceChoiceDecision, Dict[str, Any]]]) -> set[str]:
    if decision is None:
        return set()
    values = decision.selected_evidence if isinstance(decision, EvidenceChoiceDecision) else decision.get("selected_evidence", [])
    return {str(item) for item in values if str(item) in TOOL_NAMES}


def tool_call_names(tool_calls: List[Dict[str, Any]]) -> List[str]:
    return [
        str(item.get("name"))
        for item in tool_calls
        if item.get("kind") == "business" and item.get("status") == "completed"
    ]


def usage_cache_summary(usage: List[Dict[str, Any]]) -> Dict[str, Any]:
    totals = {"input_tokens": 0, "output_tokens": 0, "total_tokens": 0, "cache_read": 0, "cache_creation": 0}
    has_any = {key: False for key in totals}
    for item in usage:
        for key in ("input_tokens", "output_tokens", "total_tokens"):
            value = item.get(key)
            if isinstance(value, int):
                totals[key] += value
                has_any[key] = True
        details = item.get("input_token_details") if isinstance(item.get("input_token_details"), dict) else {}
        for key in ("cache_read", "cache_creation"):
            value = details.get(key)
            if isinstance(value, int):
                totals[key] += value
                has_any[key] = True
    return {key: (totals[key] if has_any[key] else None) for key in totals}


def evaluate_rubric(case: ProbeCase, actual_names: List[str], decision: Optional[Union[EvidenceChoiceDecision, Dict[str, Any]]]) -> Dict[str, Any]:
    actual = set(actual_names)
    selected = normalize_selected(decision)
    evidence = actual
    failures: List[str] = []
    if decision is not None and selected != actual:
        unexecuted = sorted(selected - actual)
        undeclared = sorted(actual - selected)
        if unexecuted:
            failures.append(f"declared evidence was not executed: {unexecuted}")
        if undeclared:
            failures.append(f"completed evidence was omitted from the decision: {undeclared}")
    for name in case.expected_evidence:
        if name not in evidence:
            failures.append(f"missing required evidence: {name}")
    for name in case.forbidden_evidence:
        if name in evidence:
            failures.append(f"forbidden evidence for this case: {name}")
    if isinstance(decision, EvidenceChoiceDecision):
        decision_text = " ".join([decision.answer, decision.rationale, *decision.limitations]).lower()
        limitations_text = " ".join(decision.limitations).lower()
    else:
        raw_decision = decision or {}
        decision_text = " ".join(
            str(raw_decision.get(key, ""))
            for key in ("answer", "rationale", "limitations")
        ).lower()
        limitations_text = " ".join(raw_decision.get("limitations", [])).lower()
    if case.case_id == "S2" and "simulate_concrete" in evidence:
        universal_markers = ("proves all", "proves every", "universal proof", "all paths", "all valuations")
        if any(term in decision_text for term in universal_markers) and "not" not in decision_text:
            failures.append("simulation result risks claiming universality")
    for token in case.required_limitations:
        markers = LIMITATION_MARKERS.get(token, (token.lower(),))
        if not any(marker in limitations_text for marker in markers):
            failures.append(f"missing limitation marker: {token}")
    if case.case_id == "S4" and "query_structure" in evidence:
        # Structure is allowed only as extra grounding; the required evidence above remains formal plus simulation.
        pass
    return {
        "passed": not failures,
        "failures": failures,
        "expected_evidence": list(case.expected_evidence),
        "forbidden_evidence": list(case.forbidden_evidence),
    }


def failure_kind(result_status: str, error: Optional[Dict[str, Any]], rubric: Dict[str, Any]) -> str:
    if result_status != "success" or error:
        code = str((error or {}).get("code") or "")
        infrastructure_codes = {
            "audit_write_failed",
            "cancelled",
            "config_error",
            "context_budget_exceeded",
            "provider_error",
        }
        return "infrastructure" if code in infrastructure_codes else "semantic"
    if not rubric.get("passed"):
        return "semantic"
    return "none"


def _load_registry(config_path: Optional[Path] = None) -> Any:
    from utils.llm import load_llm_registry

    return load_llm_registry(config_path)


def build_app(profile: str, limits: Dict[str, int], config_path: Optional[Path] = None) -> Any:
    from utils.agent import AgentApp, AgentSpec

    registry = _load_registry(config_path)
    spec = AgentSpec(
        name="probe-discover-evidence-choice",
        system_prompt=SYSTEM_PROMPT,
        tools=(query_structure, simulate_concrete, check_fbmcq),
        output_schema=EvidenceChoiceDecision,
        limits=limits,
        require_tool_call=True,
        retry_missing_structured_output=True,
    )
    return AgentApp.from_registry(spec, registry, profile=profile)


def run_case(case: ProbeCase, profile: str, limits: Dict[str, int], config_path: Optional[Path] = None) -> Dict[str, Any]:
    app = build_app(profile, limits, config_path)
    prompt = user_prompt(case)
    result = app.run(prompt, renderer="quiet")
    decision = result.output if isinstance(result.output, EvidenceChoiceDecision) else None
    names = tool_call_names(result.tool_calls)
    counts = dict(Counter(names))
    rubric = evaluate_rubric(case, names, decision)
    return {
        "case_id": case.case_id,
        "proposition": case.proposition,
        "profile": profile,
        "configured_model": result.model,
        "observed_model": result.observed_model,
        "adapter": app.adapter_name,
        "prompt_hashes": {
            "system": sha256_text(SYSTEM_PROMPT),
            "user": sha256_text(prompt),
            "tools": sha256_text(stable_json(tool_prompt_manifest())),
            "combined": sha256_text(stable_json({"system": SYSTEM_PROMPT, "user": prompt, "tools": tool_prompt_manifest()})),
        },
        "tool_call_names": names,
        "tool_call_counts": counts,
        "tool_calls": result.tool_calls,
        "structured_decision": decision.model_dump() if decision is not None else None,
        "usage": result.usage,
        "usage_cache_summary": usage_cache_summary(result.usage),
        "limits": limits,
        "limitations": decision.limitations if decision is not None else [],
        "rubric_verdict": rubric,
        "run_status": result.status,
        "error": result.error,
        "failure_kind": failure_kind(result.status, result.error, rubric),
        "model_calls_used": result.model_calls_used,
        "academic_eligible": result.academic_eligible,
    }


def parse_limits(args: argparse.Namespace) -> Dict[str, int]:
    limits = dict(DEFAULT_LIMITS)
    if args.model_calls is not None:
        limits["model_calls"] = args.model_calls
    if args.tool_calls is not None:
        limits["tool_calls"] = args.tool_calls
    if args.turns is not None:
        limits["turns"] = args.turns
    if args.seconds is not None:
        limits["seconds"] = args.seconds
    return limits


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Opt-in replay helper for Discover evidence-choice S1-S4 smoke.")
    parser.add_argument("--run-real", action="store_true", help="Actually call the configured LLM profile.")
    parser.add_argument("--profile", action="append", help="LLM profile from the root .llmconfig.yml. Repeatable.")
    parser.add_argument("--config", type=Path, help="Optional path to .llmconfig.yml.")
    parser.add_argument("--case", choices=[case.case_id for case in CASES], action="append", help="Case id to run. Repeatable.")
    parser.add_argument("--out", type=Path, help="Optional JSONL output path. Defaults to stdout.")
    parser.add_argument("--model-calls", type=int, help="Override model call limit.")
    parser.add_argument("--tool-calls", type=int, help="Override tool call limit.")
    parser.add_argument("--turns", type=int, help="Override turn limit.")
    parser.add_argument("--seconds", type=int, help="Override wall-clock limit in seconds.")
    parser.add_argument("--print-contract", action="store_true", help="Print deterministic case contract without model calls.")
    return parser


def contract_records() -> List[Dict[str, Any]]:
    return [
        {
            "case_id": case.case_id,
            "proposition": case.proposition,
            "expected_evidence": list(case.expected_evidence),
            "forbidden_evidence": list(case.forbidden_evidence),
            "required_limitations": list(case.required_limitations),
        }
        for case in CASES
    ]


def main(argv: Optional[List[str]] = None) -> int:
    assert_english_visible_prompts()
    parser = build_parser()
    args = parser.parse_args(argv)
    selected_cases = [case_by_id(item) for item in (args.case or [case.case_id for case in CASES])]
    if args.print_contract:
        for record in contract_records():
            print(json.dumps(record, ensure_ascii=False, sort_keys=True))
        return 0
    if not args.run_real:
        parser.error("real provider calls are opt-in; pass --run-real or use --print-contract")
    limits = parse_limits(args)
    profiles = args.profile or [_load_registry(args.config).default_name]
    handle = None
    try:
        if args.out is not None:
            if args.out.exists():
                parser.error("--out must not already exist")
            args.out.parent.mkdir(parents=True, exist_ok=True)
            handle = args.out.open("x", encoding="utf-8")
        for profile in profiles:
            for case in selected_cases:
                try:
                    record = run_case(case, profile, limits, args.config)
                except Exception as exc:  # record classified failures as JSONL instead of hiding them
                    error = {
                        "code": str(getattr(exc, "code", "runtime_error")),
                        "type": type(exc).__name__,
                        "message": str(exc),
                    }
                    rubric = {"passed": False, "failures": ["run did not complete"]}
                    record = {
                        "case_id": case.case_id,
                        "proposition": case.proposition,
                        "profile": profile,
                        "limits": limits,
                        "run_status": "failed",
                        "error": error,
                        "failure_kind": failure_kind("failed", error, rubric),
                        "rubric_verdict": rubric,
                    }
                line = json.dumps(record, ensure_ascii=False, sort_keys=True)
                if handle is None:
                    print(line)
                else:
                    handle.write(line + "\n")
                    handle.flush()
    finally:
        if handle is not None:
            handle.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
