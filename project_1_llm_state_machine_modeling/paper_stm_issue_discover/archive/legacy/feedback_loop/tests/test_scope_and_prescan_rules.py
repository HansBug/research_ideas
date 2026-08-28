"""Two splitter rules aimed at the largest source of run-to-run variance.

Three identical rounds moved 6 of 8 cells, and the movement was traced to one decision:
which model element the splitter binds a Requirement to. The binding is not unique -- a
sentence that never says which running mode it applies to can be written against the root,
against each mode, or against the pseudo-initial, and all three are syntactically legal. Only
some of them can fail on a defective model.

**Scope choice.** On `0000-gpt` round 1 the splitter bound `source` to the root, and
`occupancy_after(<root>, FinalState, Power_Off)` came back True -- because that edge really
does exist at root level. The defect is that no *running* state has a power-off exit, and only
a binding at a running state can see it. Rounds 2 and 3 split per mode and found it. A
root-level binding is satisfiable by almost any edge already in the model, so it tends to
pass regardless of whether the model is right; forbidding it removes an evasion, not an
answer. Nothing here names a defect, so no oracle leaks.

**Pre-scan.** The step-4 rule for a substate the specification names by name fired on two of
four opportunities. When it fired it was precise -- it refused to bind `auto_final` to the
similarly-named `FinalWaittr_0005` sibling. The failures were omissions, not mistakes, so the
fix is to make the check the first thing done rather than a branch reachable late in a
four-step procedure.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from paper_stm_feedback_loop.discover import prompts  # noqa: E402


def test_binding_an_unscoped_sentence_to_the_root_is_forbidden() -> None:
    text = prompts.REQUIREMENT_SPLITTER_PROMPT
    assert "does not say which" in text
    # "root state", not "root": the prompt elsewhere requires a `<root>.<name>` prefix on
    # every proposed path, and a bare "do not bind the root" reads as forbidding that prefix.
    assert "do not bind it to the root state" in text.lower()


def test_the_rule_gives_the_reason_rather_than_only_the_prohibition() -> None:
    """A prohibition without its reason gets argued with; this one has to survive revision.

    On `0000-gpt` the splitter reached the root binding while retreating from a different
    gate over three rounds. A rule it understands is one it will not retreat into.
    """
    text = prompts.REQUIREMENT_SPLITTER_PROMPT
    start = text.lower().find("do not bind it to the root state")
    window = text[max(0, start - 700) : start + 1400]
    # The reason has to be the real one. An earlier draft said a root binding "is satisfied
    # by any edge of that shape already present anywhere in the machine", which is not what
    # `occupancy_after` does -- it simulates from the bound configuration. A model that reads
    # the predicate's own field_spec can refute that, and then discounts the whole rule.
    assert "starts at the root" in window
    assert "power-on" in window
    assert "direct children of the root" in window


def test_the_scope_rule_does_not_name_any_defect() -> None:
    """The line between a structural rule and an oracle hint.

    It may say that root bindings are weak in general. It may not say what is wrong with any
    particular model, or which pair the rule was written for. The first draft failed this
    for a reason no identifier grep would catch: its example sentence was pair 0000's own
    ("on shutdown the system reaches the final state") and its recipe -- one Requirement per
    running mode -- is that pair's expected defect decomposed. So the check is on the shape,
    normalised, not on identifiers.
    """
    text = prompts.REQUIREMENT_SPLITTER_PROMPT
    start = text.lower().find("do not bind it to the root state")
    window = text[max(0, start - 700) : start + 1400]
    flat = window.lower().replace("_", " ")
    for leak in ("power off", "shutdown", "final state", "auto final", "0000", "eis-"):
        assert leak not in flat, f"scope rule leaks {leak!r}"


def test_named_substates_are_scanned_before_step_three_is_chosen() -> None:
    """Placed at the step 3 decision rather than at the very top.

    The first draft opened the prompt with it, which meant asking the model to consult the
    vocabulary before it had read how the vocabulary is used -- and a misjudged proposal
    there costs a revision round, with a repeat costing the cell.
    """
    text = prompts.REQUIREMENT_SPLITTER_PROMPT
    assert "Before you settle on step 3" in text
    assert "declared_model_vocabulary" in text


def test_the_prescan_makes_the_resulting_requirement_non_optional() -> None:
    """The failure mode was omission, so the obligation has to be stated as one.

    Specifically it must not be waivable on the grounds that the same state already appears
    in some other Requirement's bindings -- that is how it went missing.
    """
    text = prompts.REQUIREMENT_SPLITTER_PROMPT
    start = text.find("Before you settle on step 3")
    window = text[start : start + 2000]
    assert "state_declared" in window
    assert "another Requirement" in window


def test_the_prescan_still_defers_to_the_deterministic_step_2_gate() -> None:
    """A last segment already in the vocabulary is step 2's business, not step 4's.

    The comparison is spelled out as the gate performs it, because a near-match the model
    argues itself into is refused after the fact and costs a round.
    """
    text = prompts.REQUIREMENT_SPLITTER_PROMPT
    start = text.find("Before you settle on step 3")
    window = text[start : start + 2000]
    assert "last segment" in window
    assert "same comparison a deterministic gate runs" in window


def test_the_prescan_fixes_the_path_shape_the_hit_criterion_needs() -> None:
    """Without this the rule can fire perfectly and still be scored as a miss.

    `round_variance.py` matches a published issue to a ledger entry on element overlap and
    requires at least two elements in common. `<parent>.<name>` yields the parent and the
    name; a bare `<root>.<name>` yields one, and the run reads as a miss.
    """
    text = prompts.REQUIREMENT_SPLITTER_PROMPT
    start = text.find("Before you settle on step 3")
    window = text[start : start + 2000]
    assert "<parent>.<name>" in window
    assert "replacing each space with" in window


def test_the_prescan_gives_way_to_step_one_for_termination() -> None:
    """"the final state" is a pseudo-state, and proposing a name for it invents a defect."""
    text = prompts.REQUIREMENT_SPLITTER_PROMPT
    start = text.find("Before you settle on step 3")
    window = text[start : start + 2000]
    assert "termination itself" in window
    assert "step 1" in window


def test_the_prescan_pins_the_predicate_kind() -> None:
    """`leaf` is also False for a state that exists as a composite -- a weaker claim."""
    text = prompts.REQUIREMENT_SPLITTER_PROMPT
    start = text.find("Before you settle on step 3")
    window = text[start : start + 2000]
    assert 'kind="any"' in window


def test_the_scope_rule_exempts_the_predicates_whose_subject_is_the_root() -> None:
    """Twelve ledger assertions bind the bare root under these and are right to.

    `initial_target(composite=<root>, ...)`, `containment(parent=<root>, ...)` and
    `cardinality(scope=<root>, ...)` ask what the model declares about itself. The prompt
    says so two steps earlier; a scope rule that contradicted it would leave the splitter
    arguing with itself across revisions.
    """
    text = prompts.REQUIREMENT_SPLITTER_PROMPT
    start = text.lower().find("do not bind it to the root state")
    window = text[start : start + 1400]
    for exempt in ("containment", "initial_target", "cardinality"):
        assert exempt in window, f"scope rule must exempt {exempt}"


def test_shared_elements_must_name_the_defect_not_a_common_binding() -> None:
    text = prompts.RESULT_ADJUDICATOR_PROMPT
    assert "merely bind to" in text
    assert "would fixing that one place" in text.lower()
