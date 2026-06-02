"""SL-1 prompt generator: initial pyfcstm modeling."""

from __future__ import annotations

from typing import Any

from method.stages.sl_prompt_common import (
    PROMPTS_ROOT,
    fenced_json,
    load_grammar_digest,
    message_pack,
    parse_json_response,
    read_text_required,
    strip_fence,
)

MODEL_PROMPT_PATH = PROMPTS_ROOT / "modeler.txt"


def _load_modeler_guidance() -> str:
    """Load legacy modeler guidance without its raw-DSL output contract.

    ``modeler.txt`` predates PR-1B and was written for a direct "return DSL
    only" wrapper.  SL-1 needs the same generation rules but a different final
    response contract: JSON containing ``candidate_dsl`` and
    ``grounding_seeds``.  Keeping the old output-only rule in the same system
    message makes the prompt self-contradictory, so this adapter deliberately
    strips the legacy example/output section and rewrites rule 2.
    """
    base = read_text_required(MODEL_PROMPT_PATH, label="Modeler prompt")
    guidance = base.split("## Example", 1)[0].strip()
    guidance = guidance.replace(
        "the agent-specific generation rules and example below.",
        "the agent-specific generation rules below.",
    )
    guidance = guidance.replace(
        "2. **Output ONLY the pyfcstm DSL code**, nothing else. No prose, no markdown\n"
        "   code fences, no explanatory comments.",
        "2. **Construct a complete pyfcstm DSL candidate**. The outer SL-1 JSON\n"
        "   schema below controls the final response format; put the DSL text in\n"
        "   `candidate_dsl` and do not emit raw DSL outside that JSON object.",
    )
    return guidance


def build_sl1_initial_modeling_prompt(
    *,
    nl: str,
    spec_json: dict[str, Any] | None = None,
    upstream_lists: dict[str, Any] | None = None,
    pyfcstm_grammar_digest: str | None = None,
    prompt_template_version: str = "sl1-initial-modeling.v1",
) -> list[dict[str, str]]:
    """Build the SL-1 message pack without calling any LLM provider."""
    base_prompt = _load_modeler_guidance()
    grammar = load_grammar_digest(pyfcstm_grammar_digest)
    system = f"""
You are SL-1 Initial Modeling for the project-1 agent loop.
Template version: {prompt_template_version}.

Goal: produce an initial pyfcstm DSL candidate and grounding seeds from NL,
SpecJson and/or upstream modeler lists.  You are a prompt-only stage consumer:
do not claim that parse/semantic/design checks have already passed.

{base_prompt}

## Output schema (STRICT JSON)
Output JSON only, no Markdown fences and no prose:
{{
  "candidate_dsl": "complete pyfcstm DSL text",
  "grounding_seeds": [
    {{
      "element_id": "stable id such as state:Idle",
      "element_kind": "state|event|variable|transition|guard|action|hierarchical_state",
      "element_ref": "model reference/path",
      "source_stage": "SL-1",
      "evidence_text": "short NL/spec evidence",
      "requiredness": "required|optional|speculative|unknown",
      "confidence": 0.0
    }}
  ],
  "assumptions": ["optional uncertainty notes"]
}}

Hard constraints:
- `candidate_dsl` must be complete pyfcstm DSL, not a diff.
- Preserve NL-grounded required states/events/variables/transitions.
- Do not invent behavior beyond NL/SpecJson/upstream lists.
- Include grounding seeds for all required model elements you can identify.
- Stay inside the currently parseable pyfcstm subset: declare variables only as
  `def int` or `def float`; encode boolean-like flags as int 0/1; do not emit
  `def bool`, `true`, `false`, `!flag`, C-style inline comments, or unknown
  helper calls such as `ComputeRate(...)`, `max(...)` or `min(...)` in numeric
  expressions. Also do not copy `//` or `/* ... */` comments from examples into
  the DSL output.
- Inside lifecycle action blocks, conditionals must be `if [expr] {{ ... }}` /
  `else if [expr] {{ ... }}`, never `if (expr)`. Use ordinary assignments such
  as `x = x + 1;`; do not use `+=`, `-=`, `*=`, or `/=`.
- Treat NL trigger names (button press, reset, fault, back-to-manual, cut-in/out)
  as events by default: encode them with `:: EventName`. Do not make undeclared
  event names into guard variables or OR several event names inside `[A || B]`;
  use separate event transitions unless the NL explicitly says these are input
  variables.
- Use plain `during {{ ... }}` only on leaf states; if a state has nested
  children, use `>> during before/after {{ ... }}` or move the action to leaves.
- For root-level forced transitions, target a state resolvable in that scope;
  if a fallback target is nested, either place the forced transition in the
  enclosing composite scope or introduce an NL-grounded root-level fallback
  state. Do not target an unqualified nested leaf from the root. If a global
  fallback target is nested, either place the forced transition in the enclosing
  composite or introduce a root-level fallback state grounded in the NL.
- Before output, self-check parse-critical syntax: one top-level state, every
  composite has an initial transition, no event+guard on the same transition,
  guards use `: if [...]`, forced transitions have no effect block, and no DSL
  comments are present.

## pyfcstm grammar digest
{grammar}
"""
    input_payload = {
        "nl": nl,
        "spec_json": spec_json or {},
        "upstream_lists": upstream_lists or {},
    }
    user = f"""
## SL-1 input bundle
{fenced_json(input_payload)}

Generate the initial model. Output JSON only following the schema above.
"""
    return message_pack(system, user)


def parse_sl1_initial_modeling_response(content: str) -> dict[str, Any]:
    """Parse a fake/fixture SL-1 response.

    Existing wrappers may still receive legacy raw DSL from older prompts; this
    parser is intentionally strict for PR-1B tests while wrappers can keep their
    own backward-compatible fallback.
    """
    parsed = parse_json_response(content, context="SL-1")
    if not isinstance(parsed.get("candidate_dsl"), str) or not parsed["candidate_dsl"].strip():
        raise ValueError("SL-1 candidate_dsl must be a non-empty string")
    seeds = parsed.get("grounding_seeds", [])
    if not isinstance(seeds, list):
        raise ValueError("SL-1 grounding_seeds must be a list")
    return parsed


def extract_candidate_dsl_or_legacy(content: str) -> str:
    """Extract DSL from new JSON response or legacy raw/fenced DSL response."""
    try:
        parsed = parse_sl1_initial_modeling_response(content)
    except ValueError:
        return strip_fence(content)
    return parsed["candidate_dsl"].strip()
