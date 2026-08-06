"""Whether an excluded element carries author information is recorded, not guessed from its name.

`attribution_exclusions` is a flat list of strings, so the layer that reads it cannot tell two
very different things apart: the *lowering* of something the author wrote, and a *stand-in* the
projection inserted because the author wrote nothing. Evidence resting on the first says
nothing about the author -- it looked at a representation artefact. Evidence resting on the
second says the author omitted something, which is the defect itself.

The contract already records which is which. Every element carries `source_refs`, and across
1712 entries in sixty pairs the split is exact: lowerings (`transition_segment`,
`opaque_event_projection`, `route_control_variable`, `state_body_text`, `transition_macro_root`)
have refs into the source; fail-closed stand-ins (`synthetic_state`, `synthetic_transition`)
have none; the root wrapper has none and no semantics either. Flattening to strings threw that
away, and the layer downstream replaced it with a leaf-name table.

That table is wrong in both directions, which is the specific reason this cannot stay a
substring match. `FinalWait` names a lowering of a nested final the author *did* write, so
waiving it excuses evidence that should have been excluded. `InvalidInitialtr_*` names a
stand-in for an initial target the author got wrong -- the defect itself -- and is absent from
the table, so it never gets the waiver it deserves. One over-permissive, one over-strict, from
one list of two strings.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from paper_stm_feedback_loop.discover.nodes import exclusion_roles  # noqa: E402

CONTRACT = {
    "elements": [
        {
            "kind": "route_control_variable",
            "model_refs": ["Sys.R45RouteToken"],
            "source_refs": ["src.puml:line:12"],
        },
        {
            "kind": "opaque_event_projection",
            "model_refs": ["Sys.combined_event"],
            "source_refs": ["src.puml:line:9"],
        },
        {
            "kind": "synthetic_state",
            "model_refs": ["Sys.Outer.UnspecifiedInitial"],
            "source_refs": [],
            "metadata": {"generated_role": "missing_source_initial_fail_closed"},
        },
        {
            "kind": "synthetic_state",
            "model_refs": ["Sys.Outer.FinalWaittr_0005"],
            "source_refs": ["src.puml:line:20"],
            "metadata": {"generated_role": "nested_plantuml_final_completion_hold"},
        },
        {"kind": "root_wrapper", "model_refs": ["Sys"], "source_refs": []},
    ]
}


def _roles() -> dict[str, str]:
    return exclusion_roles(CONTRACT)


def test_a_lowering_of_something_the_author_wrote_is_a_carrier() -> None:
    roles = _roles()
    assert roles["Sys.R45RouteToken"] == "carrier"
    assert roles["Sys.combined_event"] == "carrier"


def test_a_fail_closed_stand_in_is_an_omission_surrogate() -> None:
    assert _roles()["Sys.Outer.UnspecifiedInitial"] == "omission_surrogate"


def test_the_leaf_name_table_got_this_one_backwards() -> None:
    """`FinalWait*` is a lowering, so waiving it excuses evidence that should be excluded.

    The old table matched it as an omission placeholder on the strength of its name. Its
    `source_refs` say otherwise: the author wrote a nested final and the projection lowered it.
    """
    assert _roles()["Sys.Outer.FinalWaittr_0005"] == "carrier"


def test_the_root_wrapper_is_neither() -> None:
    """It is a name the projection adds with no semantics; treating it as debt blocks work."""
    assert _roles()["Sys"] == "naming_wrapper"


def test_an_element_with_no_model_ref_is_skipped_rather_than_guessed() -> None:
    """Some contract entries describe source text and name no model element.

    Inventing a key for them would put roles under paths that never appear in evidence, which
    reads as coverage the mapping does not have.
    """
    roles = exclusion_roles({"elements": [{"kind": "state_body_text", "source_refs": ["x"]}]})
    assert roles == {}


def test_a_missing_contract_yields_nothing_rather_than_a_default() -> None:
    """A checkout without the contract must not silently classify everything as carrier.

    An empty mapping makes callers fall back to their previous behaviour; a default would
    quietly change every verdict.
    """
    assert exclusion_roles({}) == {}
    assert exclusion_roles(None) == {}


def test_the_split_is_by_source_refs_not_by_kind() -> None:
    """Two `synthetic_state` entries land in different roles, decided by their refs.

    Keying on `kind` would put both in one bucket and reproduce the table's error one level up.
    """
    roles = _roles()
    assert roles["Sys.Outer.UnspecifiedInitial"] != roles["Sys.Outer.FinalWaittr_0005"]
