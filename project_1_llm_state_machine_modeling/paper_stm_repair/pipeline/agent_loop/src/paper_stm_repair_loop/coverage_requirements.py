from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Iterable

from .schemas.coverage import CoverageRequirement, InputSegment


COVERAGE_REQUIREMENT_VERSION = "paper1.coverage_requirements.v3"


@dataclass(frozen=True)
class CueRule:
    dimension: str
    patterns: tuple[str, ...]
    family_options: tuple[tuple[str, ...], ...]


_META_ONLY = re.compile(
    r"^(?:\d+\s+)?(?:this\s+)?(?:state\s+machine\s+)?model\s+"
    r"(?:describes|represents|shows|presents)\b",
    re.IGNORECASE,
)
_LEADING_ORDINAL = re.compile(r"^\s*\d+(?:[.)]\s*|\s+)")
_CLAUSE_BOUNDARY = re.compile(
    r";|；|,(?=\s*(?:during\s+which|where(?:by|in)?|while|whereas|and\s+(?:it|the|this|that|they|he|she)\b))"
    r"|\band\b(?=\s+(?:it|the|this|that|they|he|she)\b)"
    r"|(?<![\w.])\d{1,3}[.)]?\s*(?=(?:when|if|unless|upon|after|before|transit(?:ion|s|ed|ing)?|enter|move|return|switch|reach|go|open|close|stop|start|activate|deactivate)\b)"
    r"|，(?=(?:期间|其中|同时|而|并且|且))|(?:并且|且)(?=(?:系统|模型|控制器|它|其))",
    re.IGNORECASE,
)

_RULES: tuple[CueRule, ...] = (
    CueRule("structure", (r"\b(?:sub[- ]?states?|regions?|areas?|phases?|modes?|branches?|hierarch(?:y|ical))\b", r"(?:子状态|区域|阶段|模式|分支|层次)"), (("structure",),)),
    CueRule(
        "cardinality",
        (
            r"\b(?:zero|one|two|three|four|five|six|seven|eight|nine|ten|multiple|different)\b",
            r"\b(?:at\s+least|at\s+most|exactly|no\s+more\s+than|no\s+fewer\s+than)\b",
            r"\b\d+\s+(?:different\s+)?(?:states?|sub[- ]?states?|regions?|areas?|phases?|modes?|branches?|events?|transitions?|variables?|paths?)\b",
            r"(?:至少|至多|恰好|不同|多个|不少于|不多于|[零一二三四五六七八九十]+个)",
        ),
        (("structure",),),
    ),
    CueRule("initialization", (r"\b(?:initially|initial|starts?|begins?|at\s+startup|on\s+startup)\b", r"(?:初始|初始化|启动时|开始时)"), (("structure",), ("simulation",))),
    CueRule("transition", (r"\b(?:transit(?:s|ed|ing)?|transitions?|enters?|moves?|returns?|switches?|reaches?|goes?|opens?|closes?|stops?|starts?|activates?|deactivates?)\b", r"(?:转移|进入|移动到|返回|切换|到达|打开|关闭|停止|启动|激活|停用)"), (("relation",), ("simulation",), ("formal",))),
    CueRule("condition", (r"\b(?:when|if|unless|upon|whenever|provided\s+that|under)\b", r"(?:当|如果|若|除非|一旦|条件为|收到|发生时)"), (("relation",), ("simulation",), ("formal",), ("effect",))),
    CueRule("effect", (r"\b(?:decreases?|decrements?|increases?|increments?|updates?|sets?|assigns?|resets?|adds?|removes?)\b", r"(?:减少|递减|增加|递增|更新|设置|赋值|重置|添加|移除)"), (("effect",),)),
    CueRule("ordering", (r"\b(?:after|before|then|following|once|subsequently)\b", r"(?:之后|以前|之前|随后|然后|完成后|一旦)"), (("relation",), ("effect",), ("simulation",), ("formal",))),
    CueRule("continuity", (r"\b(?:continuously|always|remains?|stays?|keeps?|continues?|until)\b", r"(?:持续|始终|保持|一直|继续|直到)"), (("simulation",), ("formal",))),
    CueRule("completion", (r"\b(?:complete|completed|completion|finish|finished|terminate|terminated|abort|cancel)\b", r"(?:完成|结束|终止|中止|取消)"), (("relation",), ("effect",), ("simulation",), ("formal",))),
    CueRule("forbidden_behavior", (r"\b(?:must\s+not|shall\s+not|never|cannot|only|forbidden|prohibited)\b", r"(?:不得|禁止|绝不|只能|仅允许|不允许)"), (("relation",), ("formal",))),
    CueRule("timing", (r"\b(?:within\s+\d+|timeout|deadline|delay|\d+\s*(?:ms|milliseconds?|s|seconds?|minutes?))\b", r"(?:超时|截止|延迟|\d+\s*(?:毫秒|秒|分钟)内?)"), (("simulation",), ("formal",))),
)


def build_coverage_requirements(
    segments: Iterable[InputSegment],
) -> tuple[CoverageRequirement, ...]:
    requirements: list[CoverageRequirement] = []
    for segment in segments:
        if _META_ONLY.search(segment.text.strip()):
            continue
        ordinal_prefix = _LEADING_ORDINAL.match(segment.text)
        content_start = ordinal_prefix.end() if ordinal_prefix else 0
        for clause_ordinal, (clause_start, clause_end) in enumerate(
            _clause_spans(segment.text, start=content_start), start=1
        ):
            clause_text = segment.text[clause_start:clause_end]
            clause_id = f"CLAUSE-{segment.segment_id.removeprefix('SEG-NL-')}-{clause_ordinal:02d}"
            requirement_ordinal = 1
            requirements.append(
                _requirement(
                    segment,
                    clause_id=clause_id,
                    clause_text=clause_text,
                    clause_start=clause_start,
                    clause_end=clause_end,
                    dimension="behavior",
                    cue_start=clause_start,
                    cue_end=clause_end,
                    cue_text=clause_text,
                    family_options=(("structure",), ("relation",), ("effect",), ("simulation",), ("formal",)),
                    ordinal=requirement_ordinal,
                    derivation="deterministic_clause_coverage_v2",
                )
            )
            for rule in _RULES:
                for cue_start, cue_end, cue_text in _all_matches(
                    rule.patterns, segment.text, start=clause_start, end=clause_end
                ):
                    requirement_ordinal += 1
                    requirements.append(
                        _requirement(
                            segment,
                            clause_id=clause_id,
                            clause_text=clause_text,
                            clause_start=clause_start,
                            clause_end=clause_end,
                            dimension=rule.dimension,
                            cue_start=cue_start,
                            cue_end=cue_end,
                            cue_text=cue_text,
                            family_options=rule.family_options,
                            ordinal=requirement_ordinal,
                            derivation="deterministic_lexical_cue_v2",
                        )
                    )
    return tuple(requirements)


def _requirement(
    segment: InputSegment,
    *,
    clause_id: str,
    clause_text: str,
    clause_start: int,
    clause_end: int,
    dimension: str,
    cue_start: int,
    cue_end: int,
    cue_text: str,
    family_options: tuple[tuple[str, ...], ...],
    ordinal: int,
    derivation: str,
) -> CoverageRequirement:
    return CoverageRequirement(
        requirement_id=(
            f"REQ-{clause_id.removeprefix('CLAUSE-')}-"
            f"{dimension.upper().replace('_', '-')}-{ordinal:02d}"
        ),
        segment_id=segment.segment_id,
        clause_id=clause_id,
        clause_text=clause_text,
        clause_start_offset=segment.start_offset + clause_start,
        clause_end_offset=segment.start_offset + clause_end,
        dimension=dimension,
        cue_text=cue_text,
        cue_start_offset=segment.start_offset + cue_start,
        cue_end_offset=segment.start_offset + cue_end,
        required_function_family_options=[list(option) for option in family_options],
        derivation=derivation,
        rationale=(
            f"Controller clause {clause_id} requires explicit {dimension} evidence for {cue_text!r}."
        ),
    )


def _clause_spans(text: str, *, start: int) -> list[tuple[int, int]]:
    spans: list[tuple[int, int]] = []
    cursor = start
    for match in _CLAUSE_BOUNDARY.finditer(text, start):
        end = match.start()
        if text[cursor:end].strip():
            left = cursor + len(text[cursor:end]) - len(text[cursor:end].lstrip())
            right = cursor + len(text[cursor:end].rstrip())
            spans.append((left, right))
        cursor = match.end()
    if text[cursor:].strip():
        left = cursor + len(text[cursor:]) - len(text[cursor:].lstrip())
        right = cursor + len(text[cursor:].rstrip())
        spans.append((left, right))
    return spans


def _all_matches(
    patterns: tuple[str, ...], text: str, *, start: int, end: int
) -> tuple[tuple[int, int, str], ...]:
    found: dict[tuple[int, int], str] = {}
    view = text[start:end]
    for pattern in patterns:
        for match in re.finditer(pattern, view, re.IGNORECASE):
            found[(start + match.start(), start + match.end())] = match.group(0)
    return tuple(
        (cue_start, cue_end, found[(cue_start, cue_end)])
        for cue_start, cue_end in sorted(found)
    )


__all__ = [
    "COVERAGE_REQUIREMENT_VERSION",
    "build_coverage_requirements",
]
