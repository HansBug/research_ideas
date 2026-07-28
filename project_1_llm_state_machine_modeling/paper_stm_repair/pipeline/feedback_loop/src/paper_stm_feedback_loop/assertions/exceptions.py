from __future__ import annotations


class UnsupportedEvidence(RuntimeError):
    """Raised by eval evidence functions when the requested public API/fact is unavailable."""


class UndeclaredTerm(UnsupportedEvidence):
    """The claim binds a term the model declares nowhere.

    Distinct from its parent because the two mean opposite things to the
    controller.  An ordinary refusal says *this query cannot decide the claim* --
    the producer should write a different one.  This one says *the model has no
    such element*, which for a requirement drawn from the NL is not a gap in the
    checking, it is the defect: pair 0006's NL requires the swarm count to drop
    after an attack and the model declares no variable that could drop.

    Carrying it as a type rather than a message keeps the controller off string
    matching against exception text, which the repository's integration rules
    forbid for exactly the reason that it silently stops working when the
    wording changes.
    """

    def __init__(self, message: str, *, bindings: tuple[str, ...] = ()) -> None:
        super().__init__(message)
        #: The binding names that were `<undeclared>`, for the evidence record.
        self.bindings = bindings
