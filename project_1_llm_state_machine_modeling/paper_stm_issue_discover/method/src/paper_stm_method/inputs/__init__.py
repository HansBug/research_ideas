"""Method-facing compatibility exports for neutral frozen STM artifacts.

The implementation lives in :mod:`utils.stm_artifacts` so the Semantic Judge
can consume the same read-only closure without importing method logic.
"""

from utils.stm_artifacts import (
    CanonicalConcurrentRegion,
    CanonicalSourceIR,
    ContextManifest,
    ExactSourceInventory,
    FROZEN_PAIR_IDS,
    InspectionEquivalentFacts,
    ModelIR,
    NumberedNLSegment,
    PairInput,
    SMTFacts,
    Transition,
    VerificationFacts,
    load_pair,
    load_pairs,
    parse_fcstm,
)

__all__ = [
    "FROZEN_PAIR_IDS",
    "ModelIR",
    "PairInput",
    "Transition",
    "CanonicalConcurrentRegion",
    "CanonicalSourceIR",
    "ContextManifest",
    "ExactSourceInventory",
    "InspectionEquivalentFacts",
    "NumberedNLSegment",
    "SMTFacts",
    "VerificationFacts",
    "load_pair",
    "load_pairs",
    "parse_fcstm",
]
