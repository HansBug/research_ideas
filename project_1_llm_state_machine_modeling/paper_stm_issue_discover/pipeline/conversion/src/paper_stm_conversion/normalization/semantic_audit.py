from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from dataclasses import dataclass
from typing import Any

from .plantuml import _split_transition

STATE_ALIAS_RE = re.compile(r'^\s*state\s+"(?P<label>[^"]+)"\s+as\s+(?P<alias>[A-Za-z_][A-Za-z0-9_]*)\s*$')
STATE_ALIAS_BLOCK_RE = re.compile(r'^\s*state\s+"(?P<label>[^"]+)"\s+as\s+(?P<alias>[A-Za-z_][A-Za-z0-9_]*)\s*\{\s*$')
STATE_BLOCK_RE = re.compile(r"^\s*state\s+(?P<name>.+?)\s*\{\s*$")
STATE_DECL_RE = re.compile(r"^\s*state\s+(?P<name>.+?)\s*$")


def sha256_json(data: Any) -> str:
    return hashlib.sha256(json.dumps(data, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class PlantumlSemanticSignature:
    transitions: list[tuple[str, str, str, str]]
    state_notes: list[tuple[str, str]]
    state_declarations: list[str]
    structural_lines: list[str]
    ignored_lines: list[str]
    alias_map: dict[str, str]

    def to_dict(self) -> dict[str, Any]:
        return {
            "transitions": [list(row) for row in self.transitions],
            "state_notes": [list(row) for row in self.state_notes],
            "state_declarations": self.state_declarations,
            "structural_lines": self.structural_lines,
            "ignored_lines": self.ignored_lines,
            "alias_map": self.alias_map,
        }

    def counts(self) -> dict[str, int]:
        return {
            "transitions": len(self.transitions),
            "state_notes": len(self.state_notes),
            "state_declarations": len(self.state_declarations),
            "structural_lines": len(self.structural_lines),
            "ignored_lines": len(self.ignored_lines),
            "aliases": len(self.alias_map),
        }

    @property
    def digest(self) -> str:
        comparable = {
            "transitions": self.transitions,
            "state_notes": self.state_notes,
            "state_declarations": self.state_declarations,
            "structural_lines": self.structural_lines,
        }
        return sha256_json(comparable)


def _normalize_space(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip())


def _strip_quotes(text: str) -> str:
    text = text.strip()
    if len(text) >= 2 and text[0] == '"' and text[-1] == '"':
        return text[1:-1].strip()
    return text


def _clean_endpoint(endpoint: str, alias_to_label: dict[str, str]) -> str:
    endpoint = endpoint.strip()
    if endpoint.startswith("[") and endpoint.endswith("]") and endpoint != "[*]":
        endpoint = endpoint[1:-1].strip()
    endpoint = _strip_quotes(endpoint)
    return alias_to_label.get(endpoint, endpoint)


def _collect_aliases(lines: list[str]) -> dict[str, str]:
    aliases: dict[str, str] = {}
    for line in lines:
        match = STATE_ALIAS_RE.match(line) or STATE_ALIAS_BLOCK_RE.match(line)
        if match:
            aliases[match.group("alias")] = match.group("label")
    return aliases


def _is_intro_or_closing(line: str) -> bool:
    lowered = line.strip().lower()
    return lowered in {"@startuml", "@enduml", "{", "}"}


def _is_normalization_comment(line: str) -> bool:
    stripped = line.lstrip()
    return stripped.startswith("'") and "normalization" in stripped


def _state_name_from_decl(line: str, alias_to_label: dict[str, str]) -> str | None:
    alias_match = STATE_ALIAS_RE.match(line) or STATE_ALIAS_BLOCK_RE.match(line)
    if alias_match:
        return alias_match.group("label")
    match = STATE_BLOCK_RE.match(line) or STATE_DECL_RE.match(line)
    if not match:
        return None
    name = match.group("name").strip()
    # Exclude declarations with inline stereotypes/attributes that this light
    # signature cannot safely canonicalize. They remain structural lines.
    if ":" in name:
        return None
    if name.endswith("{"):
        name = name[:-1].strip()
    return _clean_endpoint(name, alias_to_label)


def plantuml_semantic_signature(
    text: str,
    *,
    introduced_alias_declarations: set[str] | None = None,
    allow_stm_heading_removal: bool = False,
) -> PlantumlSemanticSignature:
    """Build a conservative PlantUML state-diagram signature for audit only.

    The signature is intentionally not used as the canonical model converter.
    Canonical STM extraction still comes from official PlantUML SCXML.  This
    helper checks whether the pre-SCXML normalizer preserved the source-level
    transition/state-note structure after expanding aliases introduced by the
    normalizer.
    """

    lines = text.splitlines()
    introduced = introduced_alias_declarations or set()
    alias_to_label = _collect_aliases(lines)
    transitions: list[tuple[str, str, str, str]] = []
    state_notes: list[tuple[str, str]] = []
    state_declarations: list[str] = []
    structural_lines: list[str] = []
    ignored_lines: list[str] = []

    for line_no, raw_line in enumerate(lines, start=1):
        line = raw_line.strip()
        if not line:
            continue
        if _is_intro_or_closing(line):
            ignored_lines.append(f"{line_no}:uml_delimiter")
            continue
        if _is_normalization_comment(line):
            ignored_lines.append(f"{line_no}:normalization_comment")
            continue
        if allow_stm_heading_removal and re.match(r"^stm\s+.+$", line, flags=re.IGNORECASE) and "{" not in line:
            ignored_lines.append(f"{line_no}:non_plantuml_stm_heading")
            continue
        if raw_line in introduced or line in introduced:
            ignored_lines.append(f"{line_no}:introduced_alias_declaration")
            continue

        state_name = _state_name_from_decl(raw_line, alias_to_label)
        if state_name is not None:
            state_declarations.append(_normalize_space(state_name))
            continue

        split = _split_transition(raw_line)
        if split:
            _, source, arrow, target, suffix = split
            label = suffix[2:] if suffix.startswith(" :") else suffix
            transitions.append((
                _normalize_space(_clean_endpoint(source, alias_to_label)),
                _normalize_space(arrow),
                _normalize_space(_clean_endpoint(target, alias_to_label)),
                _normalize_space(label),
            ))
            continue

        if ":" in raw_line and not raw_line.lstrip().startswith("'"):
            left, right = raw_line.split(":", 1)
            state_notes.append((
                _normalize_space(_clean_endpoint(left, alias_to_label)),
                _normalize_space(right),
            ))
            continue

        structural_lines.append(_normalize_space(raw_line))

    return PlantumlSemanticSignature(
        transitions=sorted(transitions),
        state_notes=sorted(state_notes),
        state_declarations=sorted(state_declarations),
        structural_lines=sorted(structural_lines),
        ignored_lines=ignored_lines,
        alias_map=dict(sorted(alias_to_label.items())),
    )


def _list_diff(left: list[Any], right: list[Any], *, limit: int = 20) -> dict[str, Any]:
    left_counter = Counter(map(json.dumps, left))
    right_counter = Counter(map(json.dumps, right))
    missing = []
    added = []
    for encoded, count in sorted((left_counter - right_counter).items()):
        missing.extend(json.loads(encoded) for _ in range(count))
    for encoded, count in sorted((right_counter - left_counter).items()):
        added.extend(json.loads(encoded) for _ in range(count))
    return {
        "missing_count": len(missing),
        "added_count": len(added),
        "missing_examples": missing[:limit],
        "added_examples": added[:limit],
    }


def audit_plantuml_semantic_preservation(
    raw_text: str,
    normalized_text: str,
    *,
    introduced_alias_declarations: list[str] | None = None,
    rule_ids: list[str] | None = None,
) -> dict[str, Any]:
    introduced = set(introduced_alias_declarations or [])
    raw_sig = plantuml_semantic_signature(
        raw_text,
        allow_stm_heading_removal=True,
    )
    normalized_sig = plantuml_semantic_signature(
        normalized_text,
        introduced_alias_declarations=introduced,
        allow_stm_heading_removal=True,
    )
    diffs = {
        "transitions": _list_diff(raw_sig.transitions, normalized_sig.transitions),
        "state_notes": _list_diff(raw_sig.state_notes, normalized_sig.state_notes),
        "state_declarations": _list_diff(raw_sig.state_declarations, normalized_sig.state_declarations),
        "structural_lines": _list_diff(raw_sig.structural_lines, normalized_sig.structural_lines),
    }
    pass_bool = all(
        part["missing_count"] == 0 and part["added_count"] == 0
        for part in diffs.values()
    )
    return {
        "audit_version": "r3.1.plantuml_semantic_preservation.v0",
        "scope": "source-level PlantUML raw-vs-normalized signature; canonical STM still comes from official PlantUML SCXML",
        "status": "pass" if pass_bool else "fail",
        "pass": pass_bool,
        "rule_ids": sorted(rule_ids or []),
        "raw_signature_sha256": raw_sig.digest,
        "normalized_signature_sha256": normalized_sig.digest,
        "raw_counts": raw_sig.counts(),
        "normalized_counts": normalized_sig.counts(),
        "introduced_alias_count": len(introduced),
        "differences": diffs,
        "limitations": [
            "This is a conservative source-level structural audit, not a theorem-level semantic equivalence proof.",
            "Official PlantUML SCXML remains the only canonical conversion source.",
            "High-risk normalization rules are blocked from main eligibility unless this audit and rule policy both allow inclusion.",
        ],
    }
