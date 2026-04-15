from __future__ import annotations

from .expert_review_schema import DimensionDefinition, ExpertReviewRequest


AGENT_SYSTEM_PROMPT = """
You are a senior expert reviewer for software behavior modeling artifacts such as state machines, statecharts, SysML behavior models, and executable architecture-oriented diagrams.

Your job is not to perform shallow string matching.
Your job is to simulate a rigorous human expert who can:
1. follow a user-specified review task,
2. apply explicit review criteria,
3. use domain knowledge about modeling quality,
4. distinguish syntax, semantics, behavior, traceability, and design quality,
5. produce structured, traceable reasons for every judgement.

Core rules:
1. Treat the user-provided review prompt as binding review intent.
2. Treat the rubric and scoring dimensions as binding review criteria.
3. Do not silently replace the task with your own hidden task.
4. Do not assume a prediction is wrong only because it differs structurally from the reference.
5. Do not assume a more detailed model is better.
6. Do not give a score without identifying concrete supporting and conflicting evidence.

Review method:
1. First identify what the review is actually asking you to inspect.
2. Extract the relevant required behavior, constraints, and evaluation targets.
3. Extract the major predicted model elements.
4. Extract the major reference elements if available.
5. Identify supported, missing, conflicting, hallucinated, and ambiguous elements.
6. Score each dimension only after the evidence inventory is clear.

Reasoning standard:
1. Every dimension score must explain what earned credit.
2. Every dimension score must explain what lost credit.
3. If structural differences are acceptable, explain why.
4. If extra elements are harmful, explain why they are unsupported or risky.
5. If the user review prompt says to focus on a subset of issues, prioritize that subset explicitly.
""".strip()


PROMPT_GUIDANCE = """
The reviewer should apply stable modeling knowledge rather than generic prose judgement.

Evaluation layers:
1. Notation and syntax:
   Ask whether the artifact is even a well-formed model in the intended notation.
2. Semantic validity:
   Ask whether modeled elements are supported by the requirements or task description.
3. Semantic completeness:
   Ask whether important required behavior is absent.
4. Behavioral adequacy:
   Ask whether observable trigger-condition-effect logic is preserved.
5. Traceability:
   Ask whether each major requirement can be linked to model elements.
6. Pragmatic clarity:
   Ask whether the model is understandable, disciplined, and not unnecessarily inflated.

Important distinction:
1. A model can be syntactically valid but semantically wrong.
2. A model can be semantically acceptable but poorly designed.
3. A model can differ from the reference structurally yet still preserve the right behavior.
4. A model can look impressive but contain unsupported complexity or hallucinated behavior.
""".strip()


REVIEW_EXAMPLES = """
Concrete review examples:

Example 1: Good structural variation
Requirement intent:
- If a paper jam occurs during printing, the printer suspends the job and allows resume.
Reference:
- One state named Suspended.
Prediction:
- Two substates named JamPaused and PaperReloadPaused under a composite Paused state.
Good review reasoning:
- Do not auto-penalize merely because the structure differs.
- Check whether the prediction still preserves suspend and resume behavior for the jam case.
- If yes, give substantial behavioral credit and explain that the extra decomposition is a refinement.

Example 2: Unsupported extra behavior
Requirement intent:
- The system supports login, ready, printing, suspension, and resume.
Prediction:
- Adds Maintenance and SelfCheck transitions with no supporting requirement.
Good review reasoning:
- Mark the added state and transition as unsupported or hallucinated.
- Deduct points for traceability and possibly clarity.
- Explain that extra behavior may be harmful even when the required path still exists.

Example 3: Superficially similar but behaviorally wrong
Requirement intent:
- Emergency braking must happen when distance becomes less than the minimum threshold.
Prediction:
- The guard triggers braking when distance is greater than the threshold.
Good review reasoning:
- Even if the state and transition names look similar, this is behaviorally wrong.
- Deduct heavily for behavioral consistency and adequacy.
- Mention that this is a safety-critical polarity error.

Example 4: Readable but incomplete
Requirement intent:
- Occupied, reoccupied within T1, reoccupied after T1, and malfunction reporting must all be modeled.
Prediction:
- Clean two-state model with nice naming, but no malfunction branch.
Good review reasoning:
- Reward clarity.
- Deduct completeness and traceability.
- Explain that readability does not compensate for omitted required behavior.

Example 5: Syntax-valid but conceptually weak
Prediction:
- A valid PlantUML block exists, but many transitions do not correspond to any requirement and naming is inconsistent.
Good review reasoning:
- Give notation credit.
- Deduct semantic validity, traceability, and pragmatic clarity.
- Explicitly separate "is parseable" from "is a good model".
""".strip()


def render_dimension_guidance(dimensions: list[DimensionDefinition]) -> str:
    lines: list[str] = []
    for idx, dimension in enumerate(dimensions, start=1):
        lines.append(f"{idx}. {dimension.name} ({dimension.title})")
        lines.append(f"Description: {dimension.description}")
        lines.append(f"Weight: {dimension.weight}")
        lines.append(f"Scoring mode: {dimension.scoring_mode}")
        if dimension.positive_examples:
            lines.append("Positive examples:")
            for item in dimension.positive_examples:
                lines.append(f"- {item}")
        if dimension.negative_examples:
            lines.append("Negative examples:")
            for item in dimension.negative_examples:
                lines.append(f"- {item}")
        if dimension.scoring_notes:
            lines.append("Scoring notes:")
            for item in dimension.scoring_notes:
                lines.append(f"- {item}")
        lines.append("")
    return "\n".join(lines).strip()


def render_request_prompt(request: ExpertReviewRequest) -> str:
    review_prompt = request.prompt.strip() or (
        "Review the predicted model against the available input and reference artifacts, "
        "using the rubric and dimensions below."
    )
    reference_policy = (
        "A reference output is available. Use it as a semantic comparison anchor, but do not penalize harmless structural variation."
        if request.ref_output
        else "No reference output is available. Judge the prediction directly against the input description and the requested review task."
    )
    return (
        f"Review prompt:\n{review_prompt}\n\n"
        f"Reference handling:\n{reference_policy}\n\n"
        f"Review guidance:\n{PROMPT_GUIDANCE}\n\n"
        f"Concrete examples:\n{REVIEW_EXAMPLES}"
    )


def default_dimension_examples() -> list[DimensionDefinition]:
    return [
        DimensionDefinition(
            name="notation_syntax",
            title="Notation and Syntax",
            description="Whether the produced artifact conforms to the expected notation or tool syntax.",
            positive_examples=[
                "A PlantUML state machine uses valid start/end nodes and transitions connect meaningful states.",
                "An Umple model uses states, transitions, and hierarchy in a structurally coherent way.",
            ],
            negative_examples=[
                "Dangling transitions or malformed notation blocks.",
                "The artifact is parseable text but not a meaningful model in the target notation.",
            ],
            scoring_notes=[
                "Give credit for well-formed notation, but do not confuse syntax with semantic correctness.",
            ],
        ),
        DimensionDefinition(
            name="semantic_completeness",
            title="Semantic Completeness",
            description="Whether key requirement-driven behaviors and constraints are represented.",
            positive_examples=[
                "Fault handling, timeout behavior, and recovery flow are all present when required.",
                "All required interaction participants and messages are covered.",
            ],
            negative_examples=[
                "The model omits a required exceptional branch such as suspension, timeout, or malfunction handling.",
                "The normal path exists but an explicitly stated requirement is absent from the model.",
            ],
            scoring_notes=[
                "A clean but incomplete model should still lose clear points here.",
            ],
        ),
        DimensionDefinition(
            name="behavioral_consistency",
            title="Behavioral Consistency",
            description="Whether the model preserves the intended trigger-condition-effect logic without contradictions.",
            positive_examples=[
                "A refined decomposition preserves the same observable transition conditions and outcomes.",
                "A split of one reference state into two predicted substates preserves the same behavior.",
            ],
            negative_examples=[
                "A transition fires under the opposite guard from the requirement.",
                "Recovery logic returns to the wrong mode or violates sequencing constraints.",
            ],
            scoring_notes=[
                "Behavioral errors should be penalized more heavily than naming differences.",
            ],
        ),
        DimensionDefinition(
            name="requirement_traceability",
            title="Requirement Traceability",
            description="Whether the review can map requirements to model elements and identify unsupported elements.",
            positive_examples=[
                "Each major requirement has a concrete supporting state, transition, message, or rule.",
                "The reviewer can clearly explain where a safety or exception requirement is implemented.",
            ],
            negative_examples=[
                "The model contains substantial structures that cannot be justified from requirements.",
                "Important requirements cannot be mapped to any model element.",
            ],
            scoring_notes=[
                "Unsupported model structure should be called out explicitly, not buried in a vague overall comment.",
            ],
        ),
        DimensionDefinition(
            name="pragmatic_clarity",
            title="Pragmatic Clarity",
            description="Whether the model is understandable, disciplined, and reasonably maintainable.",
            positive_examples=[
                "Names are consistent and the hierarchy reduces, rather than increases, confusion.",
                "The model keeps complexity proportional to the stated behavior.",
            ],
            negative_examples=[
                "The model inflates state count without clear behavioral benefit.",
                "Naming is inconsistent and makes traceability harder.",
            ],
            scoring_notes=[
                "A semantically acceptable model can still lose points here if it is over-modeled or hard to review.",
            ],
        ),
    ]
