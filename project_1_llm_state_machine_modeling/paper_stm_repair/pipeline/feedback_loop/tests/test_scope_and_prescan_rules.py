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
    assert "do not bind it to the root" in text.lower()


def test_the_rule_gives_the_reason_rather_than_only_the_prohibition() -> None:
    """A prohibition without its reason gets argued with; this one has to survive revision.

    On `0000-gpt` the splitter reached the root binding while retreating from a different
    gate over three rounds. A rule it understands is one it will not retreat into.
    """
    text = prompts.REQUIREMENT_SPLITTER_PROMPT
    start = text.lower().find("do not bind it to the root")
    window = text[max(0, start - 500) : start + 900]
    assert "already" in window and "true" in window.lower(), window[:200]
    assert "one Requirement per" in window


def test_the_scope_rule_does_not_name_any_defect() -> None:
    """The line between a structural rule and an oracle hint.

    It may say that root bindings are weak in general. It may not say what is wrong with any
    particular model, or which pair the rule was written for.
    """
    text = prompts.REQUIREMENT_SPLITTER_PROMPT
    start = text.lower().find("do not bind it to the root")
    window = text[max(0, start - 500) : start + 900]
    for leak in ("power_off", "0000", "auto_final", "FinalState", "EIS-"):
        assert leak.lower() not in window.lower(), f"scope rule leaks {leak!r}"


def test_named_substates_are_scanned_before_splitting_begins() -> None:
    text = prompts.REQUIREMENT_SPLITTER_PROMPT
    assert "Before you split" in text
    assert "declared_model_vocabulary" in text


def test_the_prescan_makes_the_resulting_requirement_non_optional() -> None:
    """The failure mode was omission, so the obligation has to be stated as one.

    Specifically it must not be waivable on the grounds that the same state already appears
    in some other Requirement's bindings -- that is how it went missing.
    """
    text = prompts.REQUIREMENT_SPLITTER_PROMPT
    start = text.find("Before you split")
    window = text[start : start + 1200]
    assert "state_declared" in window
    assert "another Requirement" in window


def test_the_prescan_still_defers_to_the_deterministic_step_2_gate() -> None:
    """A last segment already in the vocabulary is step 2's business, not step 4's."""
    text = prompts.REQUIREMENT_SPLITTER_PROMPT
    start = text.find("Before you split")
    window = text[start : start + 1200]
    assert "last segment" in window


def test_shared_elements_must_name_the_defect_not_a_common_binding() -> None:
    text = prompts.RESULT_ADJUDICATOR_PROMPT
    assert "merely bind to" in text
    assert "would fixing that one place" in text.lower()
