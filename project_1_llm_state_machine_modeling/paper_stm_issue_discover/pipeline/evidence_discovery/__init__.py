"""Deprecated compatibility namespace for the relocated current method.

No business logic remains here.  It keeps historical internal imports and test
node IDs working while the authoritative package is ``paper_stm_method``.
This namespace is excluded from the public method release allowlist.
"""

from __future__ import annotations

import sys
from importlib import import_module
from pathlib import Path

_PAPER_ROOT = Path(__file__).resolve().parents[2]
_METHOD_SOURCE = _PAPER_ROOT / "method" / "src"
_EVALUATION_SOURCE = _PAPER_ROOT / "evaluation" / "src"
for _source in (_METHOD_SOURCE, _EVALUATION_SOURCE):
    if str(_source) not in sys.path:
        sys.path.insert(0, str(_source))

from paper_stm_method import REGISTRY_VERSION

# Resolve historical imports to the already-loaded authoritative modules.  A
# bare __path__ bridge would execute the same Pydantic classes twice, which
# changes warning and class identity behaviour without adding compatibility.
_COMPATIBLE_MODULES = (
    "backends",
    "backends.bounded_verification",
    "backends.fcstm_native",
    "backends.source_static",
    "backends.topology",
    "backends.trajectory",
    "cli",
    "compiler",
    "compiler.inputs",
    "compiler.lowering",
    "compiler.plans",
    "compiler.soundness",
    "evidence",
    "evidence.audit_bundle",
    "evidence.receipts",
    "evidence.source_attribution",
    "evidence.witness_levels",
    "inputs",
    "inputs.context",
    "inputs.fcstm_native_projection",
    "inputs.loaders",
    "inputs.models",
    "inputs.native_projection_audit",
    "inputs.provenance",
    "orchestration",
    "orchestration.contracts",
    "orchestration.runner",
    "orchestration.runtime",
    "registry",
    "registry.loader",
    "registry.model",
    "registry.validation",
    "semantics",
    "semantics.adjudication",
    "semantics.binding",
    "semantics.domain_invariants",
    "semantics.frontier",
    "semantics.obligations",
    "semantics.predicate_routing",
    "semantics.source_transition_closure",
    "semantics.workflow",
)
for _module_suffix in _COMPATIBLE_MODULES:
    _module = sys.modules.setdefault(
        f"{__name__}.{_module_suffix}",
        import_module(f"paper_stm_method.{_module_suffix}"),
    )
    _parent_name, _, _attribute = _module_suffix.rpartition(".")
    _parent = (
        sys.modules[__name__]
        if not _parent_name
        else sys.modules[f"{__name__}.{_parent_name}"]
    )
    setattr(_parent, _attribute or _module_suffix, _module)

__path__ = [str(Path(__file__).resolve().parent), str(_METHOD_SOURCE / "paper_stm_method")]
__all__ = ["REGISTRY_VERSION"]
