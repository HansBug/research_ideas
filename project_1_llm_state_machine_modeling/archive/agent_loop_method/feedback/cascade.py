"""Function-named gated feedback cascade helpers.

This module preserves the small deterministic feedback-cascade contract that
used to live inside the deprecated A0-A4 legacy loop.  It is *not* an agent-loop
entrypoint; it only materializes feedback bundles and stage metadata for tests,
ablation utilities, and future deterministic contract checks.
"""

from __future__ import annotations

from typing import Optional

from archive.agent_loop_method.feedback.parse import check_parse
from archive.agent_loop_method.feedback.semantic import check_semantic
from archive.agent_loop_method.feedback.sim import check_sim
from archive.agent_loop_method.schema import FeedbackBundle, SimFeedback, StageResultMeta, TestScenario
from archive.agent_loop_method.stages.ids import FEEDBACK_SOURCE_TO_STAGE_ID, STAGE_SPECS_BY_ID, StageStatus


def make_feedback_stage_meta(
    source: str,
    *,
    ok: bool,
    status: StageStatus | str | None = None,
    stage_error: str | None = None,
    output_validation_error: str | None = None,
) -> StageResultMeta | None:
    """Build canonical stage metadata for a known feedback source."""
    stage_id = FEEDBACK_SOURCE_TO_STAGE_ID.get(source)
    if stage_id is None:
        return None
    spec = STAGE_SPECS_BY_ID[stage_id]
    resolved_status = status or (StageStatus.OK if ok else StageStatus.FAIL)
    return StageResultMeta(
        stage_id=stage_id,
        stage_kind=spec.kind,
        enabled=True,
        ran=True,
        status=resolved_status,
        ok=ok,
        stage_error=stage_error,
        output_validation_error=output_validation_error,
    )


def record_feedback_stage_meta(bundle: FeedbackBundle, source: str, feedback: object) -> None:
    """Attach canonical stage metadata to a bundle and compatible feedback."""
    meta = make_feedback_stage_meta(source, ok=bool(getattr(feedback, "ok", False)))
    if meta is None:
        return
    bundle.stage_results.append(meta)
    if hasattr(feedback, "meta"):
        setattr(feedback, "meta", meta)


def run_feedback_cascade(
    dsl: str,
    *,
    feedback_sources: list[str],
    scenarios: Optional[list[TestScenario]],
) -> FeedbackBundle:
    """Run the deterministic gated feedback cascade once on DSL text.

    Order: parse -> semantic -> sim -> judge placeholder.  Each source is run
    only when it is enabled and all preceding gating sources have passed.
    Enabled-but-missing signals remain explicit in ``FeedbackBundle`` so strict
    contract checks cannot accidentally converge.
    """
    bundle = FeedbackBundle(enabled_sources=list(feedback_sources))

    if "parse" in feedback_sources:
        bundle.parse = check_parse(dsl)
        record_feedback_stage_meta(bundle, "parse", bundle.parse)
        if not bundle.parse.ok:
            return bundle

    if "semantic" in feedback_sources:
        bundle.semantic = check_semantic(dsl)
        record_feedback_stage_meta(bundle, "semantic", bundle.semantic)
        if not bundle.semantic.ok:
            return bundle

    if "sim" in feedback_sources and scenarios is not None:
        bundle.sim = check_sim(dsl, scenarios)
        record_feedback_stage_meta(bundle, "sim", bundle.sim)
    elif "sim" in feedback_sources and scenarios is None:
        setup_error = "scenario generation unavailable for enabled sim feedback"
        bundle.sim = SimFeedback(ok=False, setup_error=setup_error)
        meta = make_feedback_stage_meta(
            "sim",
            ok=False,
            status=StageStatus.ERROR,
            stage_error=setup_error,
        )
        if meta is not None:
            bundle.stage_results.append(meta)

    if "judge" in feedback_sources:
        # Judge remains intentionally absent here; strict FeedbackBundle
        # semantics report enabled-but-missing judge as non-converged.
        pass

    return bundle
