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

⚠️ `source_refs` was the wrong field for the *inserted* states, and this module said so with
seven green tests because its fixture gave `FinalWait*` refs and `UnspecifiedInitial` none.
Real contracts do not split that way: all 51 `synthetic_state` entries are `compiler_owned`,
and 23 of them carry refs -- at the source line that *triggered* the insertion, which says
nothing about a declaration. The distinction lives on the segment inserted alongside, in
`metadata.generated_role`, and it resolves 23 of 23 with no ambiguity:

    invalid_source_initial_surrogate   9   InvalidInitial*   presence *is* the defect
    invalid_source_final_surrogate     4   InvalidFinal*     presence *is* the defect
    nested_final_completion_hold      10   FinalWait*        ordinary lowering

So the fixture below carries those partner segments. A fixture that cannot reproduce the shape
it claims to test is how the previous version of this mapping stayed dead code for a whole
generation -- 0 of 1712 lookups resolving, with green tests beside it.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from paper_stm_feedback_loop.discover.nodes import (  # noqa: E402
    exclusion_roles,
    inserted_state_paths,
)

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
        # Real contracts give inserted states no `generated_role` of their own and no
        # transition in the name when the author wrote no entry at all.
        {
            "kind": "synthetic_state",
            "model_refs": ["state:Sys.Outer.UnspecifiedInitial"],
            "origin": "compiler_owned",
            "source_refs": [],
        },
        # Refs, and yet not a declaration: the line is the nested final that triggered it.
        {
            "kind": "synthetic_state",
            "model_refs": ["state:Sys.Outer.FinalWaittr_0005"],
            "origin": "compiler_owned",
            "source_refs": ["src.puml:line:20"],
        },
        {
            "kind": "transition_segment",
            "model_refs": ["fcstm-transition:tr_0005:segment:1"],
            "origin": "compiler_owned",
            "source_refs": ["src.puml:line:20"],
            "metadata": {"generated_role": "nested_final_completion_hold"},
        },
        # Same shape, opposite meaning: the author's initial edge left the child scope.
        {
            "kind": "synthetic_state",
            "model_refs": ["state:Sys.Outer.InvalidInitialtr_0009"],
            "origin": "compiler_owned",
            "source_refs": ["src.puml:line:24"],
        },
        {
            "kind": "transition_segment",
            "model_refs": ["fcstm-transition:tr_0009:segment:1"],
            "origin": "compiler_owned",
            "source_refs": ["src.puml:line:24"],
            "metadata": {"generated_role": "invalid_source_initial_surrogate"},
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
    partner segment says otherwise -- `nested_final_completion_hold`: the author wrote a nested
    final and the projection held its completion.
    """
    assert _roles()["Sys.Outer.FinalWaittr_0005"] == "carrier"


def test_an_invalid_source_surrogate_is_the_defect_and_keeps_its_waiver() -> None:
    """The claim this module retracted once, on the strength of a proxy that agreed by half.

    `InvalidInitialtr_0009` exists because the author's initial edge targets outside the child
    scope -- pyfcstm reports it and inserts this state. Evidence resting on it says exactly
    that, so it must stay admissible. It carries `source_refs`, so the earlier `source_refs`
    test called it a carrier and denied the waiver.
    """
    assert _roles()["Sys.Outer.InvalidInitialtr_0009"] == "omission_surrogate"


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


def test_the_split_among_inserted_states_is_by_partner_role_not_by_refs() -> None:
    """Three inserted states, two roles, and `source_refs` cannot draw the line.

    `FinalWait*` and `InvalidInitial*` are both `synthetic_state`, both `compiler_owned`, both
    with refs -- and they belong in different roles. Keying on `kind` collapses them; keying on
    `source_refs` collapses them the other way. Only the partner segment separates them.
    """
    roles = _roles()
    assert roles["Sys.Outer.FinalWaittr_0005"] == "carrier"
    assert roles["Sys.Outer.InvalidInitialtr_0009"] == "omission_surrogate"
    assert roles["Sys.Outer.UnspecifiedInitial"] == "omission_surrogate"


def test_an_inserted_state_with_no_partner_stays_admissible() -> None:
    """Fails closed toward keeping the evidence, because the other error costs more.

    Losing a finding to a bookkeeping miss reads as "the method did not detect this", which is
    the expensive direction in a measurement whose whole point is what gets detected.
    """
    orphan = {
        "elements": [
            {
                "kind": "synthetic_state",
                "model_refs": ["state:Sys.FinalWaittr_9999"],
                "origin": "compiler_owned",
                "source_refs": ["src.puml:line:1"],
            }
        ]
    }
    assert exclusion_roles(orphan)["Sys.FinalWaittr_9999"] == "omission_surrogate"


def test_a_count_excludes_every_inserted_state_including_the_carriers() -> None:
    """The other question, and it has a different answer -- which is why it has its own home.

    `FinalWait*` is a `carrier` above: evidence about it is inadmissible. Yet the author
    declared no state there, so a count that includes it reports a total the author never
    wrote. One field cannot answer both questions, and reusing the roles for the count is the
    defect this pairing exists to prevent.
    """
    inserted = inserted_state_paths(CONTRACT)
    assert "Sys.Outer.FinalWaittr_0005" in inserted
    assert "Sys.Outer.InvalidInitialtr_0009" in inserted
    assert "Sys.Outer.UnspecifiedInitial" in inserted
    # A lowering of an author-written element is not an inserted state and must stay counted.
    assert not any("R45RouteToken" in path for path in inserted)
