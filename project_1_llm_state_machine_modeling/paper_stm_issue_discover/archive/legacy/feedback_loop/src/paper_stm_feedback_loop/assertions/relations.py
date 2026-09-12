from __future__ import annotations

from .exceptions import UnsupportedEvidence
from .structure import StructureAPI


class RelationAPI:
    """Relation-query facade over frozen structured model facts.

    Parameters: ``structure`` is the current model's ``StructureAPI``.

    Returns: immutable transition records and strict bool predicates for exact
    transition existence and guard overlap.

    Execution: reads only frozen pyfcstm inspect state/transition fields; no
    simulation, BMC, parsing, LLM, or source-trace inference is performed.

    Failure semantics: absent facts return ``False`` rather than exceptions;
    unsupported richer relation policies should be implemented as
    ``UnsupportedEvidence`` by future adapters.

    Evidence limitations: exact identity/path relations are structural model
    evidence only, not semantic equivalence or source attribution.

    Permissions: read-only in-memory inspect access; no arbitrary paths, shell,
    import, environment, network, mutation, or reference/gold data.

    Example: ``transition_exists(source="Root.Idle", event="Root.go",
    target="Root.Done")`` checks one exact transition relation.
    """

    family = "relation"

    def __init__(self, structure: StructureAPI) -> None:
        self.structure = structure

    def transitions(self, **filters):
        return self.structure.transitions(**filters)

    def transition_exists(self, **filters) -> bool:
        return bool(self.transitions(**filters))

    def guards_overlap(self, left_ref: str, right_ref: str) -> bool:
        left = self._transition_by_ref(left_ref)
        right = self._transition_by_ref(right_ref)
        left_guard = left.guard
        right_guard = right.guard
        if left_guard is None or right_guard is None:
            return True
        if str(left_guard).strip() == str(right_guard).strip():
            return True
        raise UnsupportedEvidence(
            "guards_overlap cannot decide non-identical non-empty guards with the "
            "current structured public API"
        )

    def conflicting_targets(self, *, source: str, event: str) -> bool:
        """Return whether one trigger has multiple indistinguishable targets.

        The check returns ``True`` when matching transitions have different
        targets and their guards are empty or identical. Distinct non-empty
        guards are not guessed: the query raises ``UnsupportedEvidence`` because
        this facade cannot prove their overlap. A single target, or no matching
        transition, returns ``False``.
        """

        transitions = self.transitions(source=source, event=event)
        if len({str(item.to_path) for item in transitions}) <= 1:
            return False
        undecidable = False
        for index, left in enumerate(transitions):
            for right in transitions[index + 1 :]:
                if str(left.to_path) == str(right.to_path):
                    continue
                try:
                    if self.guards_overlap(
                        f"transition:{left.transition_index}",
                        f"transition:{right.transition_index}",
                    ):
                        return True
                except UnsupportedEvidence:
                    undecidable = True
        if undecidable:
            raise UnsupportedEvidence(
                "conflicting_targets cannot decide whether all distinct guarded "
                "targets overlap with the current structured public API"
            )
        return False

    def _transition_by_ref(self, ref: str):
        normalized = ref.removeprefix("transition:").removeprefix("T")
        for transition in self.transitions():
            if str(transition.transition_index) == normalized:
                return transition
        raise UnsupportedEvidence(f"unknown transition ref: {ref}")


__all__ = ["RelationAPI"]
