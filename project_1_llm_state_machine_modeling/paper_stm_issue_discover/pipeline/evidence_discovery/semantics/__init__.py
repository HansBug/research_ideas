"""Requirement binding and method-owned D/W adjudication."""

from .adjudication import DAdjudicationResponse, SemanticAdjudication, adjudicate_disposition
from .binding import BindingResult, bind_candidate, resolve_transition_ref
from .obligations import CandidateIssue, MethodResponse
from .workflow import (
    ContextBudgetReceipt,
    CONTRACT_SYSTEM_PROMPT,
    D_SYSTEM_PROMPT,
    MODEL_GROUNDING_SYSTEM_PROMPT,
    SOURCE_GROUNDING_SYSTEM_PROMPT,
    GroundingResponse,
    NLContract,
    NLContractResponse,
    StageReceipt,
    assemble_method_response,
    build_contract_prompt,
    build_d_adjudication_prompt,
    build_d_correction_prompt,
    build_grounding_prompt,
    build_method_prompt,
    fallback_contracts,
    fallback_grounding,
    fallback_d_adjudication,
)

__all__ = [
    "BindingResult",
    "CandidateIssue",
    "ContextBudgetReceipt",
    "MethodResponse",
    "SemanticAdjudication",
    "DAdjudicationResponse",
    "NLContract",
    "NLContractResponse",
    "GroundingResponse",
    "StageReceipt",
    "CONTRACT_SYSTEM_PROMPT",
    "D_SYSTEM_PROMPT",
    "SOURCE_GROUNDING_SYSTEM_PROMPT",
    "MODEL_GROUNDING_SYSTEM_PROMPT",
    "assemble_method_response",
    "build_contract_prompt",
    "build_d_adjudication_prompt",
    "build_d_correction_prompt",
    "build_grounding_prompt",
    "adjudicate_disposition",
    "bind_candidate",
    "resolve_transition_ref",
    "build_method_prompt",
    "fallback_contracts",
    "fallback_grounding",
    "fallback_d_adjudication",
]
