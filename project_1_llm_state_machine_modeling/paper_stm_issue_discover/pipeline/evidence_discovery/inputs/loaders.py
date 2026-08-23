from __future__ import annotations

import hashlib
import json
import os
import tempfile
from pathlib import Path

from .models import PairInput, parse_fcstm
from .context import (
    _canonical_source_ir,
    build_context_manifest,
    build_exact_source_inventory,
    build_inspection_equivalent_facts,
    build_numbered_nl_segments,
    build_smt_facts,
    build_verification_facts,
    build_artifact_ref,
    file_artifact,
    generated_artifact,
    StructuredArtifact,
)
from .provenance import sha256_file


FROZEN_PAIR_IDS = tuple(
    f"{number:04d}"
    for number in range(60)
    if number not in {8, 18, 28, 38, 48, 58}
)


def load_pair(pair_dir: str | Path) -> PairInput:
    """Load one frozen pair with the complete method input closure.

    ``nl.txt``, ``plantuml.puml`` and ``fcstm.fcstm`` are necessary but not
    sufficient.  A formal method run also needs the published canonical source
    IR, mapping/working contract, source trace, reference inspection digest,
    and case identity record.  Missing closure artifacts fail here with an
    actionable list instead of silently reducing the method to a small prompt.
    """

    directory = Path(pair_dir).expanduser().resolve()
    pair_id = directory.name
    if pair_id not in FROZEN_PAIR_IDS:
        raise ValueError(f"pair is outside the frozen 54-pair protocol: {pair_id}")
    nl_path = directory / "nl.txt"
    fcstm_path = directory / "fcstm.fcstm"
    plantuml_path = directory / "plantuml.puml"
    report_root = directory.parent.parent
    artifact_stem = f"llms_emp_feedback_final_{pair_id}"
    canonical_path = report_root / "canonical" / f"{artifact_stem}.json"
    inspection_path = report_root / "parse_inspect" / f"{artifact_stem}.json"
    source_trace_path = report_root / "source_traces" / f"{artifact_stem}.json"
    working_contract_path = report_root / "working_contracts" / f"{artifact_stem}.json"
    case_report_path = report_root / "case_reports" / f"{artifact_stem}.json"
    required = {
        "nl.txt": nl_path,
        "plantuml.puml": plantuml_path,
        "fcstm.fcstm": fcstm_path,
        "canonical source IR": canonical_path,
        "reference inspection facts": inspection_path,
        "source trace": source_trace_path,
        "working contract/mapping": working_contract_path,
        "case report": case_report_path,
    }
    missing = [name for name, path in required.items() if not path.is_file()]
    if missing:
        raise FileNotFoundError(
            f"pair {pair_id} has an incomplete method input closure; missing: {', '.join(missing)}"
        )
    nl_text = nl_path.read_text(encoding="utf-8")
    fcstm_text = fcstm_path.read_text(encoding="utf-8")
    plantuml_text = plantuml_path.read_text(encoding="utf-8")
    canonical_payload = _read_json_object(canonical_path)
    inspection_payload = _read_json_object(inspection_path)
    source_trace_payload = _read_json_object(source_trace_path)
    working_contract_payload = _read_json_object(working_contract_path)
    case_report_payload = _read_json_object(case_report_path)

    model = parse_fcstm(fcstm_text)
    hashes = {
        "nl": sha256_file(nl_path),
        "fcstm": sha256_file(fcstm_path),
        "plantuml": sha256_file(plantuml_path),
        "canonical": sha256_file(canonical_path),
        "parse_inspect": sha256_file(inspection_path),
        "source_trace": sha256_file(source_trace_path),
        "working_contract": sha256_file(working_contract_path),
        "case_report": sha256_file(case_report_path),
    }
    canonical = _canonical_source_ir(canonical_payload)
    source_inventory = build_exact_source_inventory(canonical, hashes["canonical"])
    inspection_facts = build_inspection_equivalent_facts(model, hashes["fcstm"])
    verify_facts = build_verification_facts(model, inspection_facts)
    smt_facts = build_smt_facts(model)

    canonical_ref = build_artifact_ref(
        role="canonical_source_ir",
        source_role="author_source",
        path=canonical_path,
        sha256=hashes["canonical"],
        schema_version=canonical.schema_version,
        algorithm_version=canonical.adapter,
        producer="representation.canonical_source_ir",
        reason="Canonical author-source IR is needed for exact source identities and source localization.",
        basis="published representation canonical artifact",
    )
    source_inventory_artifact = generated_artifact(
        role="source_inventory",
        source_role="author_source",
        path=directory / "generated-evidence-discovery" / "source-inventory.json",
        payload=source_inventory,
        schema_version=source_inventory.schema_version,
        algorithm_version=source_inventory.algorithm_version,
        producer="evidence_discovery.inputs.context",
        reason="Exact source/transition inventory is required by source grounding.",
        basis="canonical source IR projection",
    )
    _persist_generated_artifact(source_inventory_artifact)
    inspection_artifact = file_artifact(
        role="reference_inspection_facts",
        source_role="deterministic_facts",
        path=inspection_path,
        payload=inspection_payload,
        sha256=hashes["parse_inspect"],
        schema_version=str(inspection_payload.get("schema_version") or "representation.parse-inspect-facts.v1"),
        algorithm_version="representation-fact-export.v1",
        producer="representation.parse_inspect.fact_export",
        reason="The frozen inspection-derived structured facts are retained as read-only context.",
        basis="published representation parse_inspect artifact; no legacy inspector is called",
    )
    working_artifact = file_artifact(
        role="working_contract",
        source_role="mapping",
        path=working_contract_path,
        payload=working_contract_payload,
        sha256=hashes["working_contract"],
        schema_version=str(working_contract_payload.get("schema_version") or "working-contract.unknown"),
        algorithm_version="representation.working-contract-export.v2",
        producer="representation.working_contract",
        reason="Working contract supplies exact mapping, ownership, eligibility, and diagnostic boundaries.",
        basis="published working contract artifact",
    )
    source_trace_artifact = file_artifact(
        role="source_trace",
        source_role="provenance",
        path=source_trace_path,
        payload=source_trace_payload,
        sha256=hashes["source_trace"],
        schema_version=str(source_trace_payload.get("schema_version") or "source-trace.unknown"),
        algorithm_version="representation.source-trace-export.v1",
        producer="representation.source_trace",
        reason="Source trace supplies attribution links and explicit closure boundaries.",
        basis="published source trace artifact",
    )
    case_artifact = file_artifact(
        role="case_report",
        source_role="provenance",
        path=case_report_path,
        payload=case_report_payload,
        sha256=hashes["case_report"],
        schema_version=str(case_report_payload.get("schema_version") or "representation.case-report.v1"),
        algorithm_version="representation.case-report-export.v1",
        producer="representation.case_report",
        reason="Case report records exact artifact identity and mapping metadata without method evaluation answers.",
        basis="published case report artifact",
    )
    inspection_equivalent_artifact = generated_artifact(
        role="inspection_equivalent_facts",
        source_role="deterministic_facts",
        path=directory / "generated-evidence-discovery" / "inspection-equivalent-facts.json",
        payload=inspection_facts,
        schema_version=inspection_facts.schema_version,
        algorithm_version=inspection_facts.algorithm_version,
        producer="evidence_discovery.inputs.context",
        reason="Owned inspection-equivalent facts preserve the required inventory and diagnostic role without calling forbidden inspection APIs.",
        basis=inspection_facts.basis,
    )
    _persist_generated_artifact(inspection_equivalent_artifact)
    verify_artifact = generated_artifact(
        role="verify_facts",
        source_role="deterministic_facts",
        path=directory / "generated-evidence-discovery" / "verify-facts.json",
        payload=verify_facts,
        schema_version=verify_facts.schema_version,
        algorithm_version=verify_facts.algorithm_version,
        producer="evidence_discovery.inputs.context",
        reason="Finite verification facts are supplied to grounding and remain distinct from execution receipts.",
        basis=verify_facts.basis,
    )
    _persist_generated_artifact(verify_artifact)
    smt_artifact = generated_artifact(
        role="smt_facts",
        source_role="deterministic_facts",
        path=directory / "generated-evidence-discovery" / "smt-facts.json",
        payload=smt_facts,
        schema_version=smt_facts.schema_version,
        algorithm_version=smt_facts.algorithm_version,
        producer="evidence_discovery.inputs.context",
        reason="Normalized formal inputs are supplied with an explicit no-solver boundary.",
        basis=smt_facts.basis,
    )
    _persist_generated_artifact(smt_artifact)
    artifacts = (
        build_artifact_ref(
            role="natural_language",
            source_role="author_source",
            path=nl_path,
            sha256=hashes["nl"],
            schema_version="text/plain.v1",
            algorithm_version="exact-file.v1",
            producer="representation.pair",
            reason="Numbered natural-language obligations are the source contract input.",
            basis="published pair nl.txt",
        ),
        build_artifact_ref(
            role="plantuml_source",
            source_role="author_source",
            path=plantuml_path,
            sha256=hashes["plantuml"],
            schema_version="text/plantuml.v1",
            algorithm_version="exact-file.v1",
            producer="representation.pair",
            reason="PlantUML is supplied for author-source localization only.",
            basis="published pair plantuml.puml",
        ),
        build_artifact_ref(
            role="fcstm_model",
            source_role="closed_model",
            path=fcstm_path,
            sha256=hashes["fcstm"],
            schema_version="text/fcstm.v1",
            algorithm_version=model.algorithm_version,
            producer="evidence_discovery.inputs.models",
            reason="FCSTM is the closed model used for exact binding and backend execution.",
            basis="owned FCSTM parser",
        ),
        canonical_ref,
        source_inventory_artifact.ref,
        working_artifact.ref,
        source_trace_artifact.ref,
        case_artifact.ref,
        inspection_artifact.ref,
        inspection_equivalent_artifact.ref,
        verify_artifact.ref,
        smt_artifact.ref,
    )
    manifest = build_context_manifest(pair_id=pair_id, artifacts=artifacts)
    return PairInput(
        pair_id=pair_id,
        pair_dir=directory,
        nl_text=nl_text,
        fcstm_text=fcstm_text,
        plantuml_text=plantuml_text,
        model=model,
        hashes=hashes,
        nl_segments=build_numbered_nl_segments(nl_text),
        canonical_source_ir=canonical,
        exact_source_inventory=source_inventory,
        working_contract=working_artifact,
        source_trace=source_trace_artifact,
        case_report=case_artifact,
        reference_inspection=inspection_artifact,
        inspection_facts=inspection_facts,
        verify_facts=verify_facts,
        smt_facts=smt_facts,
        context_manifest=manifest,
    )


def _read_json_object(path: Path) -> dict:
    """Read one published JSON object without interpreting diagnostic prose."""

    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object artifact: {path}")
    return value


def _persist_generated_artifact(artifact: StructuredArtifact) -> None:
    """Atomically materialize a generated fact at the manifest-recorded path."""

    path = Path(artifact.ref.path)
    path.parent.mkdir(parents=True, exist_ok=True)
    serialized = json.dumps(
        artifact.payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    digest = "sha256:" + hashlib.sha256(serialized.encode("utf-8")).hexdigest()
    if digest != artifact.ref.sha256:
        raise ValueError(f"generated artifact hash mismatch before write: {path}")
    fd, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(serialized)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def load_pairs(report_root: str | Path) -> tuple[PairInput, ...]:
    root = Path(report_root).expanduser().resolve()
    pairs_root = root / "pairs"
    pairs = tuple(load_pair(pairs_root / pair_id) for pair_id in FROZEN_PAIR_IDS)
    if len(pairs) != 54:
        raise RuntimeError(f"frozen pair count mismatch: {len(pairs)}")
    return pairs
