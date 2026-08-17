"""Read an adjudicated issue's Requirements from run records on either side of the change.

`AdjudicatedIssue.requirement_id` became `requirement_ids` when the adjudicator was allowed
to group several Requirements under one defect (issue #175). The matrix runs these scripts
read span that change -- v11-v18 are written the old way and are the baseline the new runs
are measured against -- so every reader has to accept both spellings or the comparison
cannot be made at all.

Kept as one function rather than copied into each script: the fallback is the kind of thing
that drifts once it exists in four places, and a reader that silently returns `()` where
another returns `("REQ-001",)` would show up as a phantom change in the numbers.
"""

from __future__ import annotations

from typing import Any, Mapping


def requirement_ids_of(issue: Mapping[str, Any]) -> tuple[str, ...]:
    """Every Requirement this issue speaks for, oldest record format included.

    A merged issue names more than one. A record predating the merge change names exactly
    one under the singular key. A malformed record naming neither returns empty rather than
    raising -- these are audit scripts over historical data, and one bad entry should not
    stop the sweep that would have reported it.
    """
    plural = issue.get("requirement_ids")
    if plural:
        return tuple(str(item) for item in plural)
    single = issue.get("requirement_id")
    return (str(single),) if single else ()


def requirement_label(issue: Mapping[str, Any]) -> str:
    """One cell of a table: the Requirements joined, or `-` when there are none.

    Merged issues render as `REQ-006A + REQ-006B` so a reader of the report can see at a
    glance that the row covers more than one Requirement without opening the record.
    """
    ids = requirement_ids_of(issue)
    return " + ".join(ids) if ids else "-"
