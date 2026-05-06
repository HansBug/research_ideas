"""Rubric prompt templates for S2-Q1 LLM dim scoring.

Each of the 6 dimensions has its own rubric (5-band scale) + 2-3 anchor
examples. The LLM is asked to fill a strict JSON schema with score, band,
reason, optional defects, and self-reported confidence.

Design source: `designs/v2/RUBRIC_DESIGN.md`.
"""
from __future__ import annotations

from typing import Any


_COMMON_PROLOGUE = """You are a strict, calibrated reviewer of a state-machine artifact.
Score ONLY the requested dimension. Use the rubric below; do NOT improvise new criteria.
You must output a single JSON object that conforms to the schema.

Rubric scale (every dimension):
  1.0 excellent  — flawless on this dimension; can be adopted as-is
  0.7 good       — main aspects correct; minor issues
  0.5 acceptable — fixable with rework; key defects identified
  0.3 weak       — multiple key defects; not usable as-is
  0.0 poor       — complete failure on this dimension

Output schema (strict JSON, no markdown):
{
  "dimension": <dim_name>,
  "score": <float in [0.0, 1.0]>,
  "band": <"excellent"|"good"|"acceptable"|"weak"|"poor">,
  "reason_anchor_id": <one of the anchors below or null>,
  "reason_text": <one short sentence>,
  "specific_defects": [
    {"locator": "<source>:<kind>:<idx>", "snippet": "<short text>", "issue": "<short>"}
  ],
  "confidence": <float in [0.0, 1.0] — your own confidence in this score>
}
"""


_DIM_RUBRICS = {
    "notation_syntax": {
        "what": (
            "Whether the prediction uses canonical state-machine notation that the corresponding "
            "tool can parse, with conventional naming and no syntax errors. This dimension does NOT "
            "judge whether the semantics is correct, only whether the artifact is syntactically well-formed."
        ),
        "rubric_table": [
            ("1.0", "Fully canonical syntax (PlantUML / SysML XML / standard JSON FSM); all elements use conventional names; tool-parseable."),
            ("0.7", "Main syntax compliant; minor non-canonical naming (e.g. dashes vs underscores) or redundant wrappers."),
            ("0.5", "Some syntax errors but human-readable; states/transitions still identifiable; needs editing."),
            ("0.3", "Multiple syntax problems; tool would fail to parse; non-trivial rewrite needed."),
            ("0.0", "Cannot be parsed at all; not a state machine; empty or wrong artifact type."),
        ],
        "anchors": [
            ("uml_anchor_1.0", "llms_emp::GPT-4 act diagram with full @startuml/@enduml, standard keywords, all node types correct → 1.0"),
            ("protocol_anchor_0.7", "psmbench::TCP::deepseek-reasoner — PlantUML body OK but uses 'cond active_open/' instead of canonical '[active_open]' guard → 0.7"),
            ("protocol_anchor_0.3", "psmbench::DCCP::mistral-small3.1 — state name 'CheckDataChecksum true' is action-as-name, key states missing → 0.3"),
        ],
        "pitfalls": [
            "Do NOT give 1.0 just because there are no obvious bugs — naming MUST be conventional.",
            "Pretty formatting does NOT excuse keyword errors (e.g. 'cond X/' is not a valid PlantUML guard).",
            "When ref is absent, you can still evaluate notation independently.",
        ],
    },

    "semantic_completeness": {
        "what": (
            "Whether the prediction covers all key behaviors required by the input requirement "
            "(matched ratio) AND does NOT introduce unsupported extras (harmful_extras). "
            "Focus on 'no missing, no excessive'. trace_ratio is a hard prior — the score should "
            "stay within 0.18+0.78·trace_ratio ± 0.20."
        ),
        "rubric_table": [
            ("1.0", "matched_ratio ≥ 0.85, harmful_extras = 0, every requirement clearly modeled."),
            ("0.7", "matched_ratio ≥ 0.65, harmful_extras ≤ 1, key requirements covered."),
            ("0.5", "matched_ratio ≥ 0.40, missing some key points but main flow recognizable."),
            ("0.3", "matched_ratio < 0.40 or many harmful_extras; most requirements not modeled."),
            ("0.0", "matched_ratio = 0; prediction completely off-topic from input."),
        ],
        "anchors": [
            ("uml_anchor_1.0", "llms_emp::GPT-4 act 5 decisions + 2 prints all 1:1 with input requirements → 1.0"),
            ("protocol_anchor_0.5", "psmbench::TCP::claude-3-7-sonnet covers 7/11 states, missing FIN_WAIT_1/2 + CLOSING + LAST_ACK → 0.5"),
            ("protocol_anchor_0.0", "psmbench::SMTP::mistral-small3.1 only 3 states, F1=0; SMTP needs 11+ → 0.0"),
        ],
        "pitfalls": [
            "Do NOT lower the score just because input_text is short — judge by what input requires, not the word count.",
            "harmful_extras ≠ helpful detail; only count truly invented behavior NOT in input.",
            "trace_ratio is the prior — your score should be within ±0.20 of (0.18 + 0.78·trace_ratio).",
        ],
    },

    "behavioral_consistency": {
        "what": (
            "Whether prediction is behaviorally equivalent to reference (if any). Different "
            "structure can still be semantically equivalent — judge equivalence_strength, not isomorphism. "
            "Watch for contradictions and dependency_breaks (order errors)."
        ),
        "rubric_table": [
            ("1.0", "equivalence_strength ≥ 0.85, no contradictions, no dependency_breaks."),
            ("0.7", "equivalence_strength in [0.60, 0.85), no contradictions; main flow equivalent."),
            ("0.5", "equivalence_strength in [0.40, 0.60), few contradictions; some main-flow gaps or order errors."),
            ("0.3", "contradictions ≥ 2 or main flow reversed."),
            ("0.0", "Completely non-equivalent; or no reference and prediction is internally inconsistent."),
        ],
        "anchors": [
            ("uml_anchor_1.0", "llms_emp::GPT-4o ref act 5 nodes; pred 1:1 mapping no contradictions → 1.0"),
            ("protocol_anchor_0.5", "psmbench::DCCP::deepseek-chat 4 transitions, missing retransmission path; main handshake OK → 0.5"),
            ("uml_anchor_0.3", "llms_emp::GPT-4o seq diagram with multiple reversed transitions (MES→WMS swapped) → 0.3"),
        ],
        "pitfalls": [
            "Different structure ≠ non-equivalent — equivalence_strength comes first.",
            "When ref is absent, MAX score is 0.5 (no equivalence baseline).",
            "If contradiction_count > 0, cap at ≤ 0.5.",
        ],
    },

    "requirement_traceability": {
        "what": (
            "Whether each requirement in the input can be traced to a specific element / transition / "
            "action in the prediction. trace_ratio is HARD evidence — do NOT give a high score on "
            "intuition. This is the strictest dimension."
        ),
        "rubric_table": [
            ("1.0", "100% requirements traced (matched, no partial)."),
            ("0.7", "matched_ratio ≥ 0.70 + partial_ratio < 0.20."),
            ("0.5", "matched_ratio ≥ 0.40, remaining are partial (not missing)."),
            ("0.3", "matched_ratio < 0.40 or missing_ratio > 0.50."),
            ("0.0", "matched_ratio = 0 (nothing traced)."),
        ],
        "anchors": [
            ("uml_anchor_1.0", "llms_emp::GPT-4 act 5 requirements all matched to PlantUML nodes → 1.0"),
            ("protocol_anchor_0.0", "psmbench::TCP::claude — input is RFC chapter heading 'Section 1. Purpose and Scope'; trace_ratio=0; this is input-thin not pred-bad → 0.0"),
            ("uml_anchor_0.5", "ttool-ai::connected_device 5 requirements: 2 matched, 1 partial, 2 missing → 0.5"),
        ],
        "pitfalls": [
            "Do NOT score by gut feeling — this dimension MUST stay close to trace_ratio.",
            "When input_text is thin, score honestly low and tag context_thin in defects.",
            "Sanity bound is tightest here (±0.15).",
        ],
    },

    "pragmatic_clarity": {
        "what": (
            "Whether the prediction is readable for SE/domain experts: meaningful naming, "
            "structure matching requirement size (not over-engineered, not under-engineered), "
            "no generic placeholders like 'state1' / 'event_a'."
        ),
        "rubric_table": [
            ("1.0", "Clear domain-specific naming, structure matches requirement size, no generic placeholders."),
            ("0.7", "Mostly clear naming, few generics (1-2 'state_x'), overall readable."),
            ("0.5", "Multiple generic names / over-engineered (way beyond need) / under-engineered."),
            ("0.3", "Lots of meaningless naming + structure heavily mismatched."),
            ("0.0", "All generic placeholders or completely unreadable."),
        ],
        "anchors": [
            ("uml_anchor_1.0", "ttool-ai::automated_braking states 'BrakeReady' / 'Braking' / 'BrakeReleased' all domain-specific → 1.0"),
            ("protocol_anchor_0.7", "psmbench::TCP::deepseek-reasoner protocol states well-named, but action 'set CheckDataChecksum true' is over-detailed → 0.7"),
            ("hypothetical_anchor_0.3", "Imagined case: 5 states all named 'state0' / 'state1' / ... — generic placeholder flood → 0.3"),
        ],
        "pitfalls": [
            "Quantity != lower clarity. Match complexity to requirement size.",
            "generic_name_count is the strongest signal: -0.05 per generic placeholder.",
        ],
    },

    "evidence_discipline": {
        "what": (
            "Self-discipline of the reviewer: whether all claims have locator + snippet, whether "
            "reason_text stays close to evidence, whether confidence matches actual evidence amount. "
            "This dimension scores the reviewer's own discipline."
        ),
        "rubric_table": [
            ("1.0", "Every claim has locator+snippet; reason_text purely evidence-based; confidence matches evidence."),
            ("0.7", "Main claims have evidence; <20% claims without locator."),
            ("0.5", "Some claims missing locator; reviewer still confident on those."),
            ("0.3", "Most claims unsupported; reasoning ungrounded."),
            ("0.0", "No evidence chain at all."),
        ],
        "anchors": [
            ("uml_anchor_1.0", "All 6 dim issues have locator: 'prediction:relation:5' + actual snippet → 1.0"),
            ("protocol_anchor_0.7", "PSMBench TCP review: notation has evidence; some dims fall back to deterministic; counts as moderate → 0.7"),
        ],
        "pitfalls": [
            "Do NOT give 1.0 even with full locators — also check confidence is reasonable.",
            "When no reference, this dimension is capped at 0.7.",
        ],
    },
}


def _format_rubric_table(rows: list[tuple[str, str]]) -> str:
    return "\n".join(f"  {score}  {desc}" for score, desc in rows)


def _format_anchors(anchors: list[tuple[str, str]]) -> str:
    return "\n".join(f"  - {aid}: {desc}" for aid, desc in anchors)


def _format_pitfalls(pitfalls: list[str]) -> str:
    return "\n".join(f"  - {p}" for p in pitfalls)


def build_rubric_prompt(
    dim_name: str,
    pred_summary: str,
    ref_summary: str | None,
    input_summary: str,
    regime_label: str,
    deterministic_hint: float,
    extra_signals: dict[str, Any] | None = None,
) -> str:
    """Construct the LLM prompt for one dim's rubric scoring.

    `pred_summary` / `ref_summary` / `input_summary` should be already-truncated
    summaries (<1000 chars each) to keep prompt small.
    """
    rubric = _DIM_RUBRICS[dim_name]
    extras = extra_signals or {}

    parts = [_COMMON_PROLOGUE.strip()]
    parts.append(f"\nDimension: {dim_name}\n")
    parts.append(f"What this dimension measures:\n  {rubric['what']}\n")
    parts.append("Rubric (score → criteria):\n" + _format_rubric_table(rubric["rubric_table"]))
    parts.append("\nAnchor examples:\n" + _format_anchors(rubric["anchors"]))
    parts.append("\nPitfalls to avoid:\n" + _format_pitfalls(rubric["pitfalls"]))
    parts.append(f"\nRegime: {regime_label}")
    parts.append(f"Deterministic hint (current heuristic estimate): {deterministic_hint:.3f}")
    if extras:
        parts.append("Auxiliary signals:")
        for k, v in extras.items():
            parts.append(f"  {k} = {v}")
    parts.append(f"\nInput requirement (truncated):\n{input_summary or '(none)'}")
    parts.append(f"\nPrediction artifact (truncated):\n{pred_summary or '(empty)'}")
    if ref_summary:
        parts.append(f"\nReference artifact (truncated):\n{ref_summary}")
    else:
        parts.append("\nReference artifact: (none — score independently)")
    parts.append(
        "\nReturn the JSON now. Be strict: do NOT default to 0.5 to be safe; "
        "use the rubric to pick the most accurate band, and stay close to the "
        "deterministic hint unless evidence clearly justifies otherwise."
    )
    return "\n".join(parts)


DIM_SCORE_JSON_SCHEMA = {
    "type": "object",
    "required": ["dimension", "score", "band", "reason_text", "confidence"],
    "properties": {
        "dimension": {"type": "string"},
        "score": {"type": "number", "minimum": 0.0, "maximum": 1.0},
        "band": {"type": "string", "enum": ["excellent", "good", "acceptable", "weak", "poor"]},
        "reason_anchor_id": {"type": ["string", "null"]},
        "reason_text": {"type": "string"},
        "specific_defects": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "locator": {"type": "string"},
                    "snippet": {"type": "string"},
                    "issue": {"type": "string"},
                },
            },
        },
        "confidence": {"type": "number", "minimum": 0.0, "maximum": 1.0},
    },
}


SUPPORTED_DIMS = tuple(_DIM_RUBRICS.keys())


__all__ = ["build_rubric_prompt", "SUPPORTED_DIMS", "DIM_SCORE_JSON_SCHEMA"]
