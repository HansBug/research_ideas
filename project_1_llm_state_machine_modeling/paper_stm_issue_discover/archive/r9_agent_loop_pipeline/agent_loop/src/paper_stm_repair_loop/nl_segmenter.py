from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass


SEGMENTER_VERSION = "paper1.nl_segmenter.v1"
_TITLE_RE = re.compile(r"^\s{0,3}#{1,6}\s+")
_LIST_RE = re.compile(r"^\s{0,3}(?:[-*+]\s+|\d+[.)]\s+)")
_TERMINATORS = frozenset(".?!。！？")


@dataclass(frozen=True)
class SegmenterResult:
    raw_sha256: str
    normalized_text: str
    normalized_sha256: str
    segmenter_version: str
    offset_map: list[int]
    segments: list[dict[str, object]]


def segment_nl(raw_text: str, *, language: str = "en-US") -> SegmenterResult:
    normalized, offset_map = normalize_crlf_with_offset_map(raw_text)
    spans = _candidate_spans(normalized)
    segments: list[dict[str, object]] = []
    for ordinal, (start, end, kind) in enumerate(spans, start=1):
        text = normalized[start:end]
        segments.append(
            {
                "segment_id": f"SEG-NL-{ordinal:03d}",
                "source_role": "nl",
                "text": text,
                "start_offset": start,
                "end_offset": end,
                "raw_start_offset": offset_map[start],
                "raw_end_offset": offset_map[end],
                "sha256": sha256_text(text),
                "language": language,
                "segmenter_version": SEGMENTER_VERSION,
                "segment_kind": kind,
                "ordinal": ordinal,
            }
        )
    _assert_non_whitespace_coverage(normalized, [(start, end) for start, end, _ in spans])
    return SegmenterResult(
        raw_sha256=sha256_text(raw_text),
        normalized_text=normalized,
        normalized_sha256=sha256_text(normalized),
        segmenter_version=SEGMENTER_VERSION,
        offset_map=offset_map,
        segments=segments,
    )


def normalize_crlf_with_offset_map(raw_text: str) -> tuple[str, list[int]]:
    chars: list[str] = []
    boundaries: list[int] = [0]
    raw_index = 0
    while raw_index < len(raw_text):
        if raw_text.startswith("\r\n", raw_index):
            chars.append("\n")
            raw_index += 2
            boundaries.append(raw_index)
            continue
        chars.append(raw_text[raw_index])
        raw_index += 1
        boundaries.append(raw_index)
    return "".join(chars), boundaries


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _candidate_spans(text: str) -> list[tuple[int, int, str]]:
    lines = _line_spans(text)
    spans: list[tuple[int, int, str]] = []
    prose_start: int | None = None
    prose_end: int | None = None

    def flush_prose() -> None:
        nonlocal prose_start, prose_end
        if prose_start is None or prose_end is None:
            return
        spans.extend(_split_prose(text, prose_start, prose_end))
        prose_start = None
        prose_end = None

    for start, end in lines:
        line = text[start:end]
        stripped_start = start + len(line) - len(line.lstrip())
        stripped_end = start + len(line.rstrip())
        if stripped_start >= stripped_end:
            flush_prose()
            continue
        if _TITLE_RE.match(line):
            flush_prose()
            spans.append((stripped_start, stripped_end, "title"))
            continue
        if _LIST_RE.match(line):
            flush_prose()
            spans.append((stripped_start, stripped_end, "list_item"))
            continue
        if prose_start is None:
            prose_start = stripped_start
        prose_end = stripped_end
    flush_prose()
    return sorted(spans, key=lambda item: item[0])


def _line_spans(text: str) -> list[tuple[int, int]]:
    spans: list[tuple[int, int]] = []
    start = 0
    for index, char in enumerate(text):
        if char == "\n":
            spans.append((start, index))
            start = index + 1
    spans.append((start, len(text)))
    return spans


def _split_prose(text: str, start: int, end: int) -> list[tuple[int, int, str]]:
    spans: list[tuple[int, int, str]] = []
    cursor = start
    segment_start = _skip_whitespace(text, cursor, end)
    index = segment_start
    while index < end:
        if text[index] in _TERMINATORS:
            segment_end = index + 1
            spans.append((segment_start, segment_end, "prose"))
            segment_start = _skip_whitespace(text, segment_end, end)
            index = segment_start
            continue
        index += 1
    if segment_start < end:
        spans.append((segment_start, end, "prose"))
    return spans


def _skip_whitespace(text: str, start: int, end: int) -> int:
    cursor = start
    while cursor < end and text[cursor].isspace():
        cursor += 1
    return cursor


def _assert_non_whitespace_coverage(text: str, spans: list[tuple[int, int]]) -> None:
    for index, char in enumerate(text):
        if char.isspace():
            continue
        if not any(start <= index < end for start, end in spans):
            raise AssertionError(f"non-whitespace character at normalized offset {index} is uncovered")
