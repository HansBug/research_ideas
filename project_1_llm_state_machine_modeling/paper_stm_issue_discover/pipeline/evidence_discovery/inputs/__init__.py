"""Input loading, typed context closure, and deterministic source-model parsing."""

from .loaders import FROZEN_PAIR_IDS, load_pair, load_pairs
from .context import (
    CanonicalSourceIR,
    ContextManifest,
    ExactSourceInventory,
    InspectionEquivalentFacts,
    NumberedNLSegment,
    SMTFacts,
    VerificationFacts,
)
from .models import ModelIR, PairInput, Transition, parse_fcstm

__all__ = [
    "FROZEN_PAIR_IDS",
    "ModelIR",
    "PairInput",
    "Transition",
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
