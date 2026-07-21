from __future__ import annotations


class UnsupportedEvidence(RuntimeError):
    """Raised by eval evidence functions when the requested public API/fact is unavailable."""
