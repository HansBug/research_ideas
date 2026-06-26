from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Dict, Iterable, Optional

from pyfcstm.utils import sequence_safe, to_identifier

KEYWORD_SAFE_FOR = ["python", "java"]

# FCSTM lexer emits these words/tokens before ID, so using them literally in
# state/event/variable positions can fail parse even when they are valid Python
# or Java identifiers. Keep this local list conservative and record every
# adjustment in name_mapping.json.
FCSTM_RESERVED_IDENTIFIERS = {
    "import", "def", "event", "as", "named", "pseudo", "state",
    "enter", "exit", "during", "before", "after", "abstract", "ref",
    "effect", "if", "else", "int", "float", "pi", "E", "tau",
    "and", "or", "not", "True", "true", "TRUE", "False", "false",
    "FALSE", "sin", "cos", "tan", "asin", "acos", "atan", "sinh",
    "cosh", "tanh", "asinh", "acosh", "atanh", "sqrt", "cbrt",
    "exp", "log", "log10", "log2", "log1p", "abs", "ceil",
    "floor", "round", "trunc", "sign",
}


def fcstm_keyword_safe(identifier: str) -> tuple[str, bool]:
    adjusted = False
    while identifier in FCSTM_RESERVED_IDENTIFIERS:
        identifier += "_"
        adjusted = True
    return identifier, adjusted


@dataclass
class NameMappingRow:
    raw_text: str
    canonical_ref: Optional[str]
    emitted_identifier: str
    emitted_path: str
    object_type: str
    generated_reason: str
    named_text: Optional[str]
    tool_function: str
    tool_parameters: Dict[str, Any]
    collision_group: Optional[str]
    suffix_policy: str
    is_dsl_keyword_adjusted: bool

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class NameRegistry:
    """Stable pyfcstm identifier registry backed by pyfcstm utility functions."""

    def __init__(self) -> None:
        self._used_by_scope: Dict[str, Dict[str, int]] = {}
        self.rows: list[NameMappingRow] = []

    @staticmethod
    def base_identifier(raw_text: str) -> str:
        ident = to_identifier(raw_text, strict_mode=True, keyword_safe_for=KEYWORD_SAFE_FOR)
        if not ident:
            ident = "_empty"
        return ident

    @staticmethod
    def sequence_identifier(segments: Iterable[str]) -> str:
        # sequence_safe intentionally uses double underscores between normalized
        # segments; feeding it through to_identifier gives a pyfcstm-compatible
        # single-token identifier while preserving a stable segment order.
        raw = sequence_safe(list(segments))
        ident = to_identifier(raw, strict_mode=True, keyword_safe_for=KEYWORD_SAFE_FOR)
        if not ident:
            ident = "_empty"
        return ident

    def reserve(
        self,
        *,
        raw_text: str,
        canonical_ref: Optional[str],
        object_type: str,
        scope: str,
        emitted_path: Optional[str] = None,
        generated_reason: str = "raw_identifier",
        named_text: Optional[str] = None,
        use_sequence: Optional[Iterable[str]] = None,
    ) -> str:
        if use_sequence is None:
            base = self.base_identifier(raw_text)
            tool_function = "pyfcstm.utils.to_identifier"
            tool_parameters: Dict[str, Any] = {
                "strict_mode": True,
                "keyword_safe_for": KEYWORD_SAFE_FOR,
            }
        else:
            segments = list(use_sequence)
            base = self.sequence_identifier(segments)
            tool_function = "pyfcstm.utils.sequence_safe|pyfcstm.utils.to_identifier"
            tool_parameters = {
                "sequence_segments": segments,
                "to_identifier.strict_mode": True,
                "to_identifier.keyword_safe_for": KEYWORD_SAFE_FOR,
            }

        base, dsl_keyword_adjusted = fcstm_keyword_safe(base)

        scope_used = self._used_by_scope.setdefault(scope, {})
        count = scope_used.get(base, 0)
        scope_used[base] = count + 1
        if count:
            emitted = f"{base}_{count + 1}"
            suffix_policy = "stable_scope_collision_suffix_1_based"
            collision_group = f"{scope}:{base}"
        else:
            emitted = base
            suffix_policy = "none"
            collision_group = None

        is_keyword_adjusted = dsl_keyword_adjusted
        path = emitted_path or (f"{scope}.{emitted}" if scope else emitted)
        self.rows.append(
            NameMappingRow(
                raw_text=raw_text,
                canonical_ref=canonical_ref,
                emitted_identifier=emitted,
                emitted_path=path,
                object_type=object_type,
                generated_reason=generated_reason,
                named_text=raw_text if named_text is None else named_text,
                tool_function=tool_function,
                tool_parameters=tool_parameters,
                collision_group=collision_group,
                suffix_policy=suffix_policy,
                is_dsl_keyword_adjusted=is_keyword_adjusted,
            )
        )
        return emitted

    def to_jsonable(self) -> Dict[str, Any]:
        return {
            "schema_version": "r4_5.name_mapping.v0",
            "items": [row.to_dict() for row in self.rows],
        }
