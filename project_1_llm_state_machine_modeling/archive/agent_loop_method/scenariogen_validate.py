"""Scenariogen self-validation via mutation-based coverage check.

Phase E v3 (f) — after the scenariogen agent produces a set of scenarios,
we apply the 6 standard pyfcstm mutation types (M1..M6) to the original
DSL and verify that **at least one scenario fails** on each mutated variant.
A mutation type that NO scenario can detect represents a coverage gap that
will prevent the agent loop from catching the corresponding bug class.

Design choices:

* Mutators are **regex-driven and DSL-shape generic** (no state/var name
  hard-coding). They produce a list of variants per mutation type. If the
  mutator finds nothing to mutate, the mutation type is reported as
  ``not_applicable`` rather than failing the coverage check.
* A mutation is **caught** if (a) the variant DSL fails to parse/sem
  (scenarios trivially fail), OR (b) sim on the variant produces strictly
  fewer passing scenarios than on the original.
* The result feeds into ``loop.py`` Stage 3 to decide whether to ask
  scenariogen for a targeted revision.
"""

from __future__ import annotations

import re
from typing import Callable, Optional

from archive.agent_loop_method.feedback.parse import check_parse
from archive.agent_loop_method.feedback.semantic import check_semantic
from archive.agent_loop_method.feedback.sim import check_sim
from archive.agent_loop_method.schema import TestScenario


# ---------------------------------------------------------------------------
# Mutators — each returns 0..N variant DSL strings.
# Generic over state / variable / event names: rely only on syntactic
# shape (`>= N`, `effect { ... }`, `! <src> -> <tgt>`, etc.).
# ---------------------------------------------------------------------------


def _mutate_guard_off_by_one(dsl: str) -> list[str]:
    """M1 — for each `>= N` guard threshold, produce a variant with N-1."""
    variants: list[str] = []
    seen: set[str] = set()
    for m in re.finditer(r"(>=\s*)(\d+)", dsl):
        n = int(m.group(2))
        if n <= 0:
            continue
        variant = dsl[: m.start(2)] + str(n - 1) + dsl[m.end(2) :]
        if variant not in seen:
            seen.add(variant)
            variants.append(variant)
    return variants


def _mutate_wrong_target(dsl: str) -> list[str]:
    """M2 — for each `A -> B` transition, swap B to a different declared state.

    Generic implementation: collect state names declared via `state <Name>`
    and for each transition arrow, propose one variant per alternative
    target. We cap at 1 variant per transition to bound cost.
    """
    # Collect state names (skip `state <root>` since renaming root would
    # break too much; only consider leaf-ish names that appear in arrows)
    arrow_targets = set(re.findall(r"->\s*([A-Za-z_][\w]*)", dsl))
    if len(arrow_targets) < 2:
        return []
    variants: list[str] = []
    seen: set[str] = set()
    for m in re.finditer(r"([A-Za-z_][\w]*)\s*->\s*([A-Za-z_][\w]*)", dsl):
        src, tgt = m.group(1), m.group(2)
        # pick a replacement target != current
        alternatives = [t for t in arrow_targets if t != tgt and t != src]
        if not alternatives:
            continue
        new_tgt = sorted(alternatives)[0]
        variant = dsl[: m.start(2)] + new_tgt + dsl[m.end(2) :]
        if variant not in seen:
            seen.add(variant)
            variants.append(variant)
        if len(variants) >= 3:  # cap
            break
    return variants


def _mutate_unreachable(dsl: str) -> list[str]:
    """M3 — set each `>= N` guard threshold to an unreachable 99999."""
    variants: list[str] = []
    seen: set[str] = set()
    for m in re.finditer(r"(>=\s*)(\d+)", dsl):
        n = int(m.group(2))
        if n >= 99999:
            continue
        variant = dsl[: m.start(2)] + "99999" + dsl[m.end(2) :]
        if variant not in seen:
            seen.add(variant)
            variants.append(variant)
    return variants


def _mutate_missing_forced(dsl: str) -> list[str]:
    """M4 — delete each `! <source> -> <target>` forced transition line."""
    variants: list[str] = []
    seen: set[str] = set()
    lines = dsl.split("\n")
    for i, line in enumerate(lines):
        stripped = line.lstrip()
        if stripped.startswith("!"):
            variant_lines = lines[:i] + lines[i + 1 :]
            variant = "\n".join(variant_lines)
            if variant not in seen:
                seen.add(variant)
                variants.append(variant)
    return variants


def _mutate_missing_effect(dsl: str) -> list[str]:
    """M5 — delete each `effect { ... }` block from a transition."""
    variants: list[str] = []
    seen: set[str] = set()
    pattern = re.compile(r"\s*effect\s*\{[^}]*\}")
    for m in pattern.finditer(dsl):
        variant = dsl[: m.start()] + dsl[m.end() :]
        if variant not in seen:
            seen.add(variant)
            variants.append(variant)
    return variants


def _mutate_wrong_effect_value(dsl: str) -> list[str]:
    """M6 — for each `var = N` inside an effect block, replace N with N+100."""
    variants: list[str] = []
    seen: set[str] = set()
    pattern = re.compile(r"(effect\s*\{[^}]*?[A-Za-z_]\w*\s*=\s*)(\d+)(\s*[;}])")
    for m in pattern.finditer(dsl):
        n = int(m.group(2))
        new_n = n + 100
        variant = dsl[: m.start(2)] + str(new_n) + dsl[m.end(2) :]
        if variant not in seen:
            seen.add(variant)
            variants.append(variant)
    return variants


# Ordered for deterministic reporting.
MUTATORS: dict[str, tuple[Callable[[str], list[str]], str]] = {
    "M1_guard_off_by_one": (
        _mutate_guard_off_by_one,
        "guard `>= N` mistakenly written as `>= N-1` (fires one cycle too early)",
    ),
    "M2_wrong_transition_target": (
        _mutate_wrong_target,
        "transition `A -> B` written as `A -> C` (wrong target state)",
    ),
    "M3_unreachable_target": (
        _mutate_unreachable,
        "guard threshold set far too high (`>= 99999`), target state never reached",
    ),
    "M4_missing_forced_transition": (
        _mutate_missing_forced,
        "forced transition `! ...` line missing (global event ignored)",
    ),
    "M5_missing_effect": (
        _mutate_missing_effect,
        "transition `effect { ... }` block missing (post-transition vars wrong)",
    ),
    "M6_wrong_effect_value": (
        _mutate_wrong_effect_value,
        "effect assigns wrong constant (`var = N` → `var = N+100`)",
    ),
}


# ---------------------------------------------------------------------------
# Validator
# ---------------------------------------------------------------------------


def _passing_scenario_names(dsl: str, scenarios: list[TestScenario]) -> Optional[set[str]]:
    """Return set of scenarios whose final status is 'pass' on this DSL.

    Returns ``None`` if the DSL fails parse/sem (no sim possible).
    """
    p = check_parse(dsl)
    if not p.ok:
        return None
    s = check_semantic(dsl)
    if not s.ok:
        return None
    try:
        sim = check_sim(dsl, scenarios)
    except Exception:
        return None
    return {sr.name for sr in sim.scenario_results if sr.status == "pass"}


def validate_coverage(
    dsl: str,
    scenarios: list[TestScenario],
    *,
    max_variants_per_mutation: int = 3,
) -> dict[str, dict]:
    """Run the 6-mutation coverage check.

    For each mutation type, apply up to ``max_variants_per_mutation`` variants
    and check whether each variant is **caught** by at least one scenario.

    Returns
    -------
    A dict ``{mutation_name: {"status": s, "description": d, "n_variants": k,
    "caught_variants": j}}`` where ``status`` is one of:

    * ``"caught"``           — every variant tested was caught (or at least one
      variant caused parse/sem failure or sim regression vs original)
    * ``"partially_caught"`` — some variants caught, some not
    * ``"missed"``           — variants exist but none was caught
    * ``"not_applicable"``   — no variants could be produced (mutator found
      no syntactic anchor in this DSL — e.g. M1 on a model with no `>= N`)
    """
    baseline_passing = _passing_scenario_names(dsl, scenarios)
    if baseline_passing is None:
        # Original DSL itself is unparseable — abort gracefully; we can't run
        # the coverage check against a broken baseline.
        return {
            name: {
                "status": "not_applicable",
                "description": desc,
                "n_variants": 0,
                "caught_variants": 0,
                "reason": "baseline DSL failed parse/sem",
            }
            for name, (_, desc) in MUTATORS.items()
        }

    out: dict[str, dict] = {}
    for name, (mutator, desc) in MUTATORS.items():
        variants = mutator(dsl)[:max_variants_per_mutation]
        if not variants:
            out[name] = {
                "status": "not_applicable",
                "description": desc,
                "n_variants": 0,
                "caught_variants": 0,
            }
            continue
        caught_count = 0
        for v in variants:
            v_passing = _passing_scenario_names(v, scenarios)
            if v_passing is None:
                # Variant broke parse/sem — trivially caught
                caught_count += 1
                continue
            if not baseline_passing.issubset(v_passing) or v_passing != baseline_passing:
                # At least one previously-passing scenario now fails on the
                # mutated variant. Mutation is caught.
                caught_count += 1
        if caught_count == len(variants):
            status = "caught"
        elif caught_count > 0:
            status = "partially_caught"
        else:
            status = "missed"
        out[name] = {
            "status": status,
            "description": desc,
            "n_variants": len(variants),
            "caught_variants": caught_count,
        }
    return out


def coverage_directive(coverage: dict[str, dict]) -> Optional[str]:
    """Build a targeted revision directive for scenariogen if any mutation
    type is missed. Returns ``None`` if no targeted action is needed."""
    missed = [name for name, info in coverage.items() if info["status"] == "missed"]
    partial = [name for name, info in coverage.items() if info["status"] == "partially_caught"]
    targets = missed + partial
    if not targets:
        return None
    lines = [
        "Your previous scenario set has bug-detection coverage gaps. The "
        "following mutation types applied to the model produced variants "
        "that NONE of your scenarios could detect. Add or strengthen "
        "scenarios so that each listed mutation would cause at least one "
        "scenario to FAIL on the mutated model:",
        "",
    ]
    for name in targets:
        info = coverage[name]
        lines.append(f"- **{name}**: {info['description']}")
    lines.append("")
    lines.append(
        "Specifically: pick the transition / guard / effect / forced-line "
        "implicated by each mutation type and add a scenario whose "
        "expected_state / expected_vars would be wrong if that exact "
        "mutation were present in the model. Preserve all previous "
        "scenarios; only ADD probes targeting the gaps."
    )
    return "\n".join(lines)
