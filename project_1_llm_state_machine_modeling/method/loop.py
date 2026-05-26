"""Agent loop driver — orchestrates NL → spec → model → (feedback × repair)*.

Phase E implementation. Wires together the per-stage agents and the four
feedback wrappers behind a single ``run_agent_loop(nl, config)`` entry.

## Design rules (locked-in 2026-05-26 after Phase G v3 review)

1. **Gated cascade** for feedback execution. Order: parse → semantic →
   (sim, judge in parallel within the same iter). If parse fails the
   downstream sources are not run (DSL is unparseable garbage; running sem/sim
   on it is wasted budget). If sem fails sim/judge likewise skipped (model
   can't be built).
2. **Scenarios are frozen** once at the top of the loop. They are NOT
   regenerated each iter — per user decision: model adapts to scenarios,
   not the other way around. This pins the oracle so iterations are
   measuring repair progress on a fixed target.
3. **Cascaded repair** dispatches on the earliest-failing source. The
   repair sub-prompts are focused (only see one diagnostic each).
4. **sim / judge are optional**. Inclusion is governed by
   ``config.feedback_sources`` — used for ablation experiments
   (A0…A4 conditions in the schema).
5. **Early back-out**: when the cascade returns ``all_ok`` the loop exits
   immediately (no further repair). ``status='converged'``.

The function returns an ``AgentLoopResult`` capturing every iteration's
model + feedback + repair so downstream evaluation can reconstruct the
full trajectory.
"""

from __future__ import annotations

from typing import Optional

from method.agents.modeler import generate_model
from method.agents.multistep import run_multistep_modeling
from method.agents.repair import repair_model
from method.agents.scenariogen import generate_scenarios
from method.agents.spec_extractor import extract_spec
from method.feedback.parse import check_parse
from method.feedback.semantic import check_semantic
from method.feedback.sim import check_sim
from method.schema import (
    AgentLoopResult,
    FeedbackBundle,
    IterTrace,
    LoopConfig,
    ModelArtifact,
    TestScenario,
)


def _accumulate_usage(total: dict, step_usage: dict) -> None:
    """Merge token usage from one LLM call into the running total."""
    for k in ("prompt_tokens", "completion_tokens", "total_tokens"):
        total[k] = total.get(k, 0) + int(step_usage.get(k, 0))
    total["n_calls"] = total.get("n_calls", 0) + 1


def _run_cascade(
    dsl: str,
    *,
    feedback_sources: list[str],
    scenarios: Optional[list[TestScenario]],
) -> FeedbackBundle:
    """Run the gated feedback cascade once on a DSL text.

    Order: parse → semantic → (sim, judge). Each source is run only if it
    is enabled in ``feedback_sources`` AND all preceding gating sources
    passed.
    """
    bundle = FeedbackBundle()

    # ---- parse ----
    if "parse" in feedback_sources:
        bundle.parse = check_parse(dsl)
        if not bundle.parse.ok:
            return bundle  # gating: skip downstream

    # ---- semantic ----
    if "semantic" in feedback_sources:
        bundle.semantic = check_semantic(dsl)
        if not bundle.semantic.ok:
            return bundle  # gating: skip downstream

    # ---- sim ----
    if "sim" in feedback_sources and scenarios is not None:
        bundle.sim = check_sim(dsl, scenarios)
        # Do NOT gate judge on sim failure — they are independent signals.

    # ---- judge (Phase H — placeholder, not implemented yet) ----
    if "judge" in feedback_sources:
        # bundle.judge = check_judge(dsl, nl, ...)
        # For Phase E we leave this as None; Phase H will fill it.
        pass

    return bundle


def run_agent_loop(
    nl: str,
    config: Optional[LoopConfig] = None,
    *,
    seed_dsl: Optional[str] = None,
) -> AgentLoopResult:
    """End-to-end agent loop entry.

    Parameters
    ----------
    nl
        Natural-language requirement text.
    config
        ``LoopConfig`` controlling modeling mode, iteration count, and which
        feedback sources are enabled. Defaults to a full A4-style config
        if None (but judge is currently a no-op until Phase H).
    seed_dsl
        Optional pre-built DSL to skip the SpecExtractor + Modeler stages
        and start the iter loop from this text. Used in demos to inject a
        deliberately buggy starting model and watch repair recover.

    Returns
    -------
    AgentLoopResult
        Captures spec, every iteration's (model, feedback, repair), token
        usage totals, and convergence status.
    """
    cfg = config or LoopConfig()
    result = AgentLoopResult(llm_model=cfg.llm_model)

    # ===== Stage 1: SpecExtractor (skipped if seed_dsl provided) =====
    spec = None
    if seed_dsl is None:
        spec, spec_usage = extract_spec(nl, seed=cfg.seed, model=cfg.llm_model)
        _accumulate_usage(result.token_usage, spec_usage)
        result.spec = spec

    # ===== Stage 2: Modeler (skipped if seed_dsl provided) =====
    if seed_dsl is not None:
        current_dsl = seed_dsl
    else:
        modeling_mode = getattr(cfg, "modeling_mode", "multi_step")
        if modeling_mode == "multi_step":
            mr = run_multistep_modeling(nl, seed=cfg.seed, model=cfg.llm_model)
            current_dsl = mr.final_dsl
            _accumulate_usage(result.token_usage, mr.token_usage)
        else:
            artifact, mod_usage = generate_model(
                spec, seed=cfg.seed, model=cfg.llm_model
            )
            current_dsl = artifact.dsl_text
            _accumulate_usage(result.token_usage, mod_usage)

    # ===== Stage 3: ScenarioGen (frozen — once per loop, only if sim enabled) =====
    scenarios: Optional[list[TestScenario]] = None
    if "sim" in cfg.feedback_sources:
        try:
            scenarios, _, sc_usage = generate_scenarios(
                nl, current_dsl, seed=cfg.seed, model=cfg.llm_model
            )
            _accumulate_usage(result.token_usage, sc_usage)
        except Exception as e:
            # scenariogen failure shouldn't kill the whole loop — sim just stays off.
            scenarios = None
            result.error_message = f"scenariogen failed: {type(e).__name__}: {str(e)[:200]}"

    # ===== Stage 4: Iter loop =====
    # If n_iter == 0 we still run the cascade ONCE to populate final_feedback,
    # but skip any repair.
    n_iter = max(cfg.n_iter, 1)
    bundle: Optional[FeedbackBundle] = None
    converged = False

    for it in range(n_iter):
        # ---- run cascade on current DSL ----
        bundle = _run_cascade(
            current_dsl,
            feedback_sources=cfg.feedback_sources,
            scenarios=scenarios,
        )

        # ---- record iter trace ----
        trace = IterTrace(
            iteration=it,
            model=ModelArtifact(
                dsl_text=current_dsl,
                iteration=it,
                produced_by="modeler" if it == 0 else "repair",
            ),
            feedback=bundle,
        )

        # ---- early back-out on convergence ----
        if bundle.all_ok:
            trace.repair_skipped = True
            result.iter_traces.append(trace)
            converged = True
            break

        # ---- repair (skip if this is the last iter — no point producing a DSL
        #      we won't re-verify) ----
        if cfg.n_iter == 0 or it == n_iter - 1:
            result.iter_traces.append(trace)
            break

        try:
            repair_artifact, repair_usage, _target = repair_model(
                current_dsl,
                bundle,
                nl=nl,
                scenarios=scenarios,
                iteration=it + 1,
                seed=cfg.seed,
                model=cfg.llm_model,
            )
            trace.repair = repair_artifact
            _accumulate_usage(result.token_usage, repair_usage)
            current_dsl = repair_artifact.dsl_text
        except Exception as e:
            result.error_message = (
                f"repair failed at iter {it}: {type(e).__name__}: {str(e)[:200]}"
            )
            result.iter_traces.append(trace)
            break

        result.iter_traces.append(trace)

    # ===== Finalize =====
    result.final_dsl = current_dsl
    if result.iter_traces:
        result.final_artifact = result.iter_traces[-1].model
    result.final_feedback = bundle
    if converged:
        result.status = "converged"
    elif cfg.feedback_sources == []:
        result.status = "ok_no_loop"
    elif bundle is not None and bundle.parse is not None and not bundle.parse.ok:
        # Distinguish "never parsed" from "parsed then regressed"
        parse_ever_ok = any(
            t.feedback and t.feedback.parse and t.feedback.parse.ok
            for t in result.iter_traces
        )
        result.status = "not_converged" if parse_ever_ok else "parse_failed_all"
    else:
        result.status = "not_converged"

    return result
