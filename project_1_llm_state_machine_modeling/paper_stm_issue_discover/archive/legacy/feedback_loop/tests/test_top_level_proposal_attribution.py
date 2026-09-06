"""Whether a missing-name finding can be published must not depend on how deep the name is.

A step-4 proposal binds a path the model does not declare, so no trace entry covers it. The
claim it makes -- "this scope declares no element by that name" -- is about the scope, which
the author did write, so attribution walks up to the nearest declared ancestor.

The walk works for a nested name and fails for a top-level one, and the reason is an artefact
of how traces are recorded rather than anything about the model. The frozen traces carry
`state:` and `macro:*` entries; across all sixty pairs there is no entry for the machine root,
none for events, none for variables. So `<root>.Missing` has exactly one proper prefix, that
prefix is the root, nothing covers it, and the walk returns empty -- while `<root>.Outer.Missing`
finds `<root>.Outer` on its first step and is published.

Measured on one generation, that accounts for thirteen of forty-three refusals -- roughly a
third -- and among them the one record that this pair's ledger says was found and then lost.
Two byte-identical claims, one publishable and one not, distinguished by a naming convention
in the specification's prose.

The fallback keeps the same reasoning one step further out. "This scope declares no element
named X" is witnessed by the elements the scope *does* declare, so when the prefix walk runs
out, the anchor becomes the declared siblings under that prefix. That is the same inference
the nested case makes; it only has to be spelled separately because the machine root is a
naming wrapper the projection adds and the author never wrote.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from paper_stm_feedback_loop.discover.nodes import _declared_ancestor_refs  # noqa: E402

#: A frozen trace shaped like the corpus: entries for declared states, none for the root.
ENTRIES = [
    {
        "intermediate_elements": ["state:Sys.Outer"],
        "source_elements": ["source:state:Outer"],
        "attribution_boundary": {"source_level_claim_allowed": True},
    },
    {
        "intermediate_elements": ["state:Sys.Beside"],
        "source_elements": ["source:state:Beside"],
        "attribution_boundary": {"source_level_claim_allowed": True},
    },
    {
        "intermediate_elements": ["state:Sys.Outer.Inner"],
        "source_elements": ["source:state:Inner"],
        "attribution_boundary": {"source_level_claim_allowed": True},
    },
]


def _refs(state: str) -> tuple[str, ...]:
    return _declared_ancestor_refs(
        "AST-X-1", "state_declared", (("state", state),), ENTRIES
    )


def test_a_nested_proposed_name_attributes_to_its_declared_parent() -> None:
    """The case that already worked, kept as the reference point."""
    assert _refs("Sys.Outer.Missing") == ("source:state:Outer",)


def test_a_top_level_proposed_name_also_attributes() -> None:
    """The case that returned empty, and the whole point of the change.

    `Sys` is the projection's naming wrapper -- no trace entry covers it and none ever will.
    The claim is still about a scope the author wrote elements into, so the witnesses are
    those elements.
    """
    refs = _refs("Sys.Missing")
    assert refs, "a top-level proposal must be attributable"
    assert "source:state:Outer" in refs
    assert "source:state:Beside" in refs


def test_the_fallback_uses_direct_children_only() -> None:
    """A grandchild is not a witness that its grandparent declares no such name.

    `Sys.Outer.Inner` sits under `Sys.Outer`, not under `Sys`, so it says nothing about what
    `Sys` does or does not contain.
    """
    assert "source:state:Inner" not in _refs("Sys.Missing")


def test_depth_no_longer_decides_publishability() -> None:
    """Stated as the invariant rather than as two separate expectations.

    This is the property the change exists to establish: two claims of the same shape, made
    about scopes the author wrote, must both be answerable.
    """
    assert bool(_refs("Sys.Missing")) == bool(_refs("Sys.Outer.Missing"))


def test_a_name_under_an_undeclared_scope_stays_unattributable() -> None:
    """The fallback must not become "always attributable".

    Nothing in the trace declares anything under `Sys.Ghost`, so there is no witness and the
    honest answer is still that this cannot be attributed.
    """
    assert _refs("Sys.Ghost.Missing") == ()


def test_behavioural_claims_are_still_excluded() -> None:
    """A run through a state that does not exist is not made author-owned by its siblings."""
    assert _declared_ancestor_refs(
        "AST-X-1", "occupancy_after", (("target", "Sys.Missing"),), ENTRIES
    ) == ()


def test_an_entry_the_boundary_disallows_is_not_a_witness() -> None:
    """The fallback inherits the same boundary filter as the walk it extends."""
    blocked = [
        {
            "intermediate_elements": ["state:Sys.Outer"],
            "source_elements": ["source:state:Outer"],
            "attribution_boundary": {
                "source_level_claim_allowed": True,
                "conversion_or_lowering_related": True,
            },
        }
    ]
    assert _declared_ancestor_refs(
        "AST-X-1", "state_declared", (("state", "Sys.Missing"),), blocked
    ) == ()
