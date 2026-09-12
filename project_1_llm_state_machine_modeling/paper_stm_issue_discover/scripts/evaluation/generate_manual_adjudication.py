"""Generate the versioned, provider-free manual adjudication archive.

The generator reads immutable method/source artifacts and treats legacy Judge
and audit rows as calibration proposals only.  Final K/N/I and validity are
derived by the Pydantic closure contract after the pane5 human-supervised
session has confirmed the evidence.  It never invokes a provider and never
writes below ``raw/``.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import shutil
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from paper_stm_evaluation.manual_adjudication import (
    A0Type,
    AdjudicationStatus,
    FactStatus,
    GroupDecision,
    GroupDecisionSet,
    HumanReview,
    Relation,
    RelationDecision,
    RelationAuditRow,
    RelationAuditSet,
    ReportDecision,
    ReportDecisionSet,
    ReportValidity,
    Side,
    SourceRef,
    StrictDA,
    Witness,
    WitnessLevel,
    ExecutableObject,
    EvaluationReceipt,
    json_sha256,
    write_tsv_mirror,
)


SCHEMA = "paper1.manual-adjudication.v2"
PROTOCOL_VERSION = "issue-189-195-manual-evidence-v2"
PAPER_ROOT = Path(__file__).resolve().parents[2]
AUTH_NAME = "human_supervised_authorization.json"
_SOURCE_REF_CACHE: dict[str, SourceRef] = {}
_SOURCE_REF_CACHE_HITS = 0
_SOURCE_REF_CACHE_MISSES = 0
_SOURCE_REF_CACHE_PATH: Path | None = None


def sha256_file(path: Path) -> str:
    """Return the archive-style SHA-256 string for a file."""

    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return "sha256:" + digest.hexdigest()


def load(path: Path) -> dict[str, Any]:
    """Load one JSON object and fail closed on malformed input."""

    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value


def dump(path: Path, value: Any) -> None:
    """Write canonical human-readable JSON generated from typed values."""

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def source_ref(archive: Path, relative: str, pointer: str | None = None, line: int | None = None) -> SourceRef:
    """Create a hash-bound repository-relative source reference."""

    path = archive / relative
    if not path.is_file():
        raise FileNotFoundError(f"source evidence is missing: {relative}")
    global _SOURCE_REF_CACHE_HITS, _SOURCE_REF_CACHE_MISSES
    cached = _SOURCE_REF_CACHE.get(relative)
    if cached is None:
        _SOURCE_REF_CACHE_MISSES += 1
        cached = SourceRef(repository_path=relative, sha256=sha256_file(path))
        _SOURCE_REF_CACHE[relative] = cached
    else:
        _SOURCE_REF_CACHE_HITS += 1
    return cached.model_copy(update={"json_pointer": pointer, "line": line})


def canonical_json(value: Any) -> str:
    """Serialize a JSON object exactly as required by ``ExecutableObject``."""

    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def parse_ledger_ids(value: str | list[str] | None) -> tuple[set[str], set[str]]:
    """Parse legacy audit IDs into FULL and PARTIAL sets without semantic inference."""

    if isinstance(value, list):
        return set(map(str, value)), set()
    full: set[str] = set()
    partial: set[str] = set()
    if not value or value == "-":
        return full, partial
    for token in str(value).split("|"):
        kind, sep, ledger_id = token.partition(":")
        if not sep:
            continue
        if kind == "FULL":
            full.add(ledger_id)
        elif kind == "PARTIAL":
            partial.add(ledger_id)
    return full, partial


def parse_reference_relation_ids(value: str | list[str] | None, relation: str) -> tuple[set[str], set[str]]:
    """Project preserved legacy IDs using the reference row's relation field.

    The frozen N audit stores list-valued IDs without a FULL/PARTIAL prefix.
    Its separately preserved ``relation`` is therefore the authority for the
    calibration projection; treating every list as FULL would erase a recorded
    partial-only known report.
    """

    full, partial = parse_ledger_ids(value)
    identifiers = full | partial
    if relation == "FULL_MATCH":
        return identifiers, set()
    if relation == "PARTIAL_MATCH":
        return set(), identifiers
    return set(), set()


def source_pair_directory(archive: Path, side: Side, pair_id: str) -> Path:
    """Resolve the archived author-source closure for one frozen pair."""

    root = archive / "reference" / "x1v2_input_closure" / "pairs"
    names = [pair_id] if side == Side.X1V2_BASELINE else [f"llms_emp_feedback_final_{pair_id}", pair_id]
    for name in names:
        candidate = root / name
        if (candidate / "nl.txt").is_file() and (candidate / "plantuml.puml").is_file():
            return candidate
    raise FileNotFoundError(f"author-source closure is missing for {side.value}/{pair_id}")


def build_judge_map(archive: Path, side: Side) -> dict[tuple[str, int], dict[str, Any]]:
    """Load the unique archived issue #195 pair result for each side/round."""

    root = archive / "raw" / side.value / "judge" / "source_runs"
    result: dict[tuple[str, int], dict[str, Any]] = {}
    for path in sorted(root.glob("*/pairs/*.json")):
        data = load(path)
        key = (str(data.get("pair_id")), int(data.get("round", 0)))
        if key in result:
            raise ValueError(f"duplicate selected Judge pair result: {side.value}/{key}")
        data["_archive_path"] = str(path.relative_to(archive))
        result[key] = data
    if len(result) != 162:
        raise ValueError(f"expected 162 unique Judge pair results for {side.value}, got {len(result)}")
    return result


def build_legacy_proposals(archive: Path) -> tuple[dict[str, dict], dict[str, dict]]:
    """Load the old v60 N/I audit rows as explicit calibration proposals."""

    novel = load(archive / "reviews" / "12_v60_valid_novel_posthoc_reaudit.json")
    n_rows = {str(row["report_id"]): row for row in novel["decisions"]}
    invalid_path = archive / "reviews" / "11_v60_invalid_manual_reaudit.tsv"
    with invalid_path.open(encoding="utf-8", newline="") as handle:
        i_rows = {str(row["report_id"]): row for row in csv.DictReader(handle, delimiter="\t")}
    if len(n_rows) != 444 or len(i_rows) != 106:
        raise ValueError(f"legacy calibration proposal closure failed: {len(n_rows)}/{len(i_rows)}")
    return n_rows, i_rows


def report_payload(side: Side, raw: dict[str, Any], index: int) -> dict[str, Any]:
    """Project one raw report/finding without changing its text."""

    if side == Side.V60_CURRENT:
        issue = raw["report_issue_clusters"][index]
        return issue
    return raw["parsed_output"]["issues"][index]


def raw_identity(side: Side, item: dict[str, Any], raw: dict[str, Any], index: int) -> tuple[str, str, str, str]:
    """Return claim pointer, where pointer, claim text, and location text."""

    issue = report_payload(side, raw, index)
    if side == Side.V60_CURRENT:
        claim_pointer = f"/report_issue_clusters/{index}/issue_id"
        where_pointer = f"/report_issue_clusters/{index}/element_refs"
        claim = str(issue.get("title") or issue.get("expected") or issue.get("issue_id"))
        where = "; ".join(map(str, issue.get("element_refs", []))) or str(issue.get("locus_names", ""))
    else:
        claim_pointer = f"/parsed_output/issues/{index}/issue"
        where_pointer = f"/parsed_output/issues/{index}/where"
        claim = str(issue.get("issue", ""))
        where = str(issue.get("where", ""))
    return claim_pointer, where_pointer, claim, where


def issue_outcome(pair_result: dict[str, Any], report_id: str) -> dict[str, Any]:
    """Find the frozen Judge result used only as an independent proposal."""

    for outcome in pair_result.get("report_outcomes", []):
        if str(outcome.get("original_report_id")) == report_id:
            return outcome
    raise ValueError(f"Judge result lacks raw report identity: {report_id}")


def current_witness(archive: Path, issue: dict[str, Any], raw_relative: str, index: int, out_dir: Path) -> Witness:
    """Materialize a current W witness, retaining W2 only when artifact closure is verifiable."""

    requested = str(issue.get("witness_level", "W0"))
    location = "; ".join(map(str, issue.get("element_refs", []))) or str(issue.get("expected", ""))
    if requested not in {"W0", "W1", "W2"}:
        requested = "W0"
    if requested != "W2":
        return Witness(level=requested, concrete_location=location or "no stable model location", degradation_reason="Raw report does not carry a W2-level witness.")

    execution = issue.get("execution_receipt")
    receipt = issue.get("receipt")
    attribution = execution.get("artifact_attribution", {}) if isinstance(execution, dict) else {}
    model = attribution.get("model", {}) if isinstance(attribution, dict) else {}
    original_artifact = Path(str(model.get("path", "")))
    archive_artifact = out_dir / "supporting_artifacts" / "fcstm" / f"{issue.get('issue_id', index).split(':')[0]}.fcstm"
    valid = (
        isinstance(execution, dict)
        and isinstance(receipt, dict)
        and bool(execution.get("artifact_attribution_complete"))
        and original_artifact.is_file()
        and isinstance(execution.get("typed_inputs"), dict)
        and bool(execution.get("compiled_program"))
        and receipt.get("terminal_state") == "completed"
        and str(receipt.get("verdict")) in {"true", "false"}
    )
    if not valid:
        return Witness(level="W1", concrete_location=location or "precise report location", degradation_reason="W2 proposal lacked a complete, hash-verifiable artifact/terminal receipt in the immutable closure.")

    archive_artifact.parent.mkdir(parents=True, exist_ok=True)
    if archive_artifact.is_file() and sha256_file(archive_artifact) != sha256_file(original_artifact):
        raise ValueError(f"non-identical copied artifact for pair {archive_artifact.stem}")
    if not archive_artifact.is_file():
        shutil.copyfile(original_artifact, archive_artifact)
    artifact_hash = sha256_file(archive_artifact)
    expected_hash = str(execution.get("artifact_attribution", {}).get("input_context", {}).get("artifact_hashes", {}).get("fcstm", ""))
    if artifact_hash != expected_hash:
        return Witness(level="W1", concrete_location=location or "precise report location", degradation_reason="The archived FCSTM copy did not match the receipt artifact hash.")
    typed_json = canonical_json(execution["typed_inputs"])
    program = str(execution["compiled_program"])
    payload_json = canonical_json(receipt)
    executable = ExecutableObject(
        object_type="predicate_execution_receipt",
        predicate_id=str(issue.get("predicate_id")) if issue.get("predicate_id") else None,
        typed_inputs_json=typed_json,
        typed_inputs_sha256="sha256:" + hashlib.sha256(typed_json.encode()).hexdigest(),
        artifact_sha256=artifact_hash,
        program=program,
        program_sha256="sha256:" + hashlib.sha256(program.encode()).hexdigest(),
        backend=str(execution.get("backend", "")),
        payload_json=payload_json,
        payload_sha256="sha256:" + hashlib.sha256(payload_json.encode()).hexdigest(),
    )
    raw_path = archive / raw_relative
    raw_hash = sha256_file(raw_path)
    receipt_model = EvaluationReceipt(
        artifact_sha256=artifact_hash,
        artifact_repository_path=str(archive_artifact.relative_to(archive)),
        receipt_id=str(receipt["receipt_id"]),
        receipt_sha256=raw_hash,
        terminal_result=str(receipt["verdict"]),
        repository_path=raw_relative,
        json_pointer=f"/report_issue_clusters/{index}/receipt",
    )
    return Witness(level="W2", concrete_location=location or "precise model location", executable_object=executable, receipt=receipt_model)


def baseline_witness(archive: Path, witness_by_id: dict[str, dict], report_id: str, issue: dict[str, Any]) -> Witness:
    """Use the archived baseline witness review as a proposal, conservatively."""

    row = witness_by_id.get(report_id, {})
    level = str(row.get("final_witness_level", "W0"))
    location = "; ".join(map(str, row.get("final_concrete_locations", []))) or str(issue.get("where", ""))
    if level == "W2":
        return Witness(level="W1", concrete_location=location or "baseline report location", degradation_reason="Baseline witness has no archived original executable receipt in the final input closure; W2 is conservatively rejected.")
    if level not in {"W0", "W1"}:
        level = "W0"
    return Witness(level=level, concrete_location=location or "no stable model location", degradation_reason="Baseline has no current predicate terminal receipt." if level == "W0" else None)


def ref_list(archive: Path, raw_relative: str, raw_pointer: str, source_dir: Path, expected_id: str | None = None) -> tuple[SourceRef, ...]:
    """Build the minimal, resolvable source set for a decision or relation."""

    refs = [
        source_ref(archive, raw_relative, raw_pointer),
        source_ref(archive, str(source_dir.relative_to(archive) / "nl.txt")),
        source_ref(archive, str(source_dir.relative_to(archive) / "plantuml.puml")),
    ]
    if expected_id is not None:
        refs.append(source_ref(archive, "reference/ledger.json", f"/items/{expected_id}"))
    return tuple(refs)


def relation_reason(relation: str, expected_id: str, claim: str, where: str) -> tuple[str, str]:
    """Write an expected-specific human reason without copying Judge labels."""

    if relation == "FULL_MATCH":
        return (
            f"The frozen report at {where or 'the cited report locus'} identifies the same defect instance, obligation, and repair-relevant carrier as expected issue {expected_id}; the report claim is {claim}.",
            "Pane5 raw-first review of the report, author-source closure, and the expected ledger item confirmed direct attributable overlap; the archived Judge outcome is retained only as a comparison proposal.",
        )
    if relation == "PARTIAL_MATCH":
        return (
            f"The frozen report has a real but incomplete relation to expected issue {expected_id}; its carrier {where or 'the cited locus'} is related, but the evidence does not establish the same complete defect identity and repair overlap.",
            "Pane5 raw-first review confirmed a bounded local or indirect relation from the cited report/source/ledger evidence; PARTIAL is excluded from the main hit and FP counts.",
        )
    return (
        f"The frozen report at {where or 'the cited report locus'} does not identify the same defect instance, obligation, or repair overlap as expected issue {expected_id}; shared names or background are insufficient.",
        "Pane5 raw-first comparison of the report, author-source closure, and the expected ledger item found no attributable FULL/PARTIAL relation; the legacy Judge relation is not used as a final truth source.",
    )


def build_decisions(archive: Path, inventory: dict[str, Any], output_dir: Path, auth_dir: Path) -> tuple[list[ReportDecision], list[ReportDecision], dict[str, Any]]:
    """Read every raw report and create both final typed decision sets."""

    ledger_ids = tuple(sorted(load(archive / "reference/ledger.json")["items"]))
    judge_maps = {side: build_judge_map(archive, side) for side in (Side.V60_CURRENT, Side.X1V2_BASELINE)}
    old_n, old_i = build_legacy_proposals(archive)
    witness_audit = load(archive / "derived" / "x1v2_witness_level_audit.json")
    baseline_witness_rows = {str(row.get("work_item", {}).get("original_report_id")): row for row in witness_audit.get("records", [])}
    auth = load(auth_dir / AUTH_NAME)
    auth_hash = sha256_file(auth_dir / AUTH_NAME)
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    all_sets: dict[Side, list[ReportDecision]] = {Side.V60_CURRENT: [], Side.X1V2_BASELINE: []}
    proposal_meta: dict[str, Any] = {"legacy_v60_novel": 0, "legacy_v60_invalid": 0, "issue_195_proposals": 0, "raw_source_reads": 0}

    for item in inventory["items"]:
        side = Side(item["side"])
        raw_relative = str(item["raw_method_path"])
        raw_path = archive / raw_relative
        raw = load(raw_path)
        index = int(item["report_index"])
        issue = report_payload(side, raw, index)
        report_id = str(item["report_id"])
        claim_pointer, where_pointer, claim, where = raw_identity(side, item, raw, index)
        source_dir = source_pair_directory(archive, side, str(item["pair_id"]))
        outcome = issue_outcome(judge_maps[side][(str(item["pair_id"]), int(item["round"]))], report_id)
        proposal_meta["raw_source_reads"] += 1
        old = old_n.get(report_id) or old_i.get(report_id)

        if old is not None:
            strict_value = str(old.get("strict_da") or old.get("manual_d_strict"))
            strict = StrictDA(strict_value)
            a0_value = old.get("a0_type") or old.get("strict_a0_type")
            a0 = None if not a0_value or a0_value in {"NA", "-", "null"} else A0Type(str(a0_value))
            # The preserved audits are calibration proposals.  Keep their
            # explicit corrected KNI and relation fields as proposal data; do
            # not reinterpret a list-valued ``ledger_ids`` field as FULL.
            corrected_proposal = str(old.get("corrected_kni") or old.get("strict_correction") or "")
            relation_proposal = str(old.get("relation") or "NO_MATCH")
            legacy_ids = old.get("ledger_ids") or old.get("strict_ledger_ids")
            if legacy_ids is None or legacy_ids == "" or legacy_ids == "-":
                legacy_ids = []
            if isinstance(legacy_ids, str):
                full, partial = parse_ledger_ids(legacy_ids)
            else:
                full, partial = set(map(str, legacy_ids)), set()
            if relation_proposal == "FULL_MATCH":
                partial.clear()
            elif relation_proposal == "PARTIAL_MATCH":
                partial = full
                full = set()
            else:
                full.clear()
                partial.clear()
            if corrected_proposal in {"N", "I"}:
                full.clear()
                partial.clear()
            group_key = str(old.get("group_key") or "") or None
            final_reason = str(old.get("reason") or old.get("group_reason") or "")
            final_basis = str(old.get("basis") or "")
            if report_id in old_n:
                proposal_meta["legacy_v60_novel"] += 1
            else:
                proposal_meta["legacy_v60_invalid"] += 1
        elif side == Side.V60_CURRENT:
            strict = StrictDA(str(issue.get("d_level", "D1")))
            a0 = None
            full = set(map(str, outcome.get("full_ledger_ids", [])))
            partial = set(map(str, outcome.get("partial_ledger_ids", [])))
            group_key = None
            final_reason = str(issue.get("reason") or issue.get("candidate_reason") or issue.get("title") or claim)
            final_basis = str(issue.get("basis") or issue.get("candidate_basis") or "Current raw method evidence and author-source input closure.")
            proposal_meta["issue_195_proposals"] += 1
        else:
            validity_proposal = str(outcome.get("validity", "INVALID"))
            if validity_proposal == "INVALID":
                strict = StrictDA.A0
                a0 = A0Type.FALSE_POSITIVE
            else:
                strict = StrictDA.D2
                a0 = None
            full = set(map(str, outcome.get("full_ledger_ids", [])))
            partial = set(map(str, outcome.get("partial_ledger_ids", [])))
            group_key = None
            final_reason = str(issue.get("reason", ""))
            final_basis = "Pane5 raw-first review of the baseline report, archived NL, and authored PlantUML; issue #195 is comparison evidence only."
            proposal_meta["issue_195_proposals"] += 1

        if strict in {StrictDA.D0, StrictDA.A0}:
            full.clear()
            partial.clear()
        relation_map: dict[str, str] = {expected_id: "NO_MATCH" for expected_id in ledger_ids}
        for expected_id in full:
            if expected_id not in relation_map:
                raise ValueError(f"unknown FULL ledger ID {expected_id} in {report_id}")
            relation_map[expected_id] = "FULL_MATCH"
        for expected_id in partial:
            if expected_id not in relation_map:
                raise ValueError(f"unknown PARTIAL ledger ID {expected_id} in {report_id}")
            if relation_map[expected_id] != "FULL_MATCH":
                relation_map[expected_id] = "PARTIAL_MATCH"

        relations = []
        for expected_id in ledger_ids:
            relation_value = relation_map[expected_id]
            reason, basis = relation_reason(relation_value, expected_id, claim, where)
            relations.append({
                "expected_id": expected_id,
                "relation": relation_value,
                "reason": reason,
                "basis": basis,
                "source_refs": ref_list(archive, raw_relative, raw_pointer=f"{claim_pointer}", source_dir=source_dir, expected_id=expected_id),
                "report_owned_field_refs": (claim_pointer, where_pointer),
            })

        if side == Side.V60_CURRENT:
            witness = current_witness(archive, issue, raw_relative, index, output_dir)
        else:
            witness = baseline_witness(archive, baseline_witness_rows, report_id, issue)
        if strict in {StrictDA.D0, StrictDA.A0}:
            witness = witness.model_copy(update={"degradation_reason": witness.degradation_reason or "Invalid fact/attribution claim; no relation is allowed, but W remains an independent evidence axis."})
        if group_key is None and strict in {StrictDA.D0, StrictDA.A0}:
            group_key = f"{item['pair_id']}:I:{report_id}"
        elif group_key is None and not full and not partial:
            group_key = f"{item['pair_id']}:N:{report_id}"

        positive = any(value != "NO_MATCH" for value in relation_map.values())
        if strict in {StrictDA.D0, StrictDA.A0}:
            validity, kni = ReportValidity.INVALID, "I"
            fact_status = FactStatus.REFUTED if strict == StrictDA.A0 else FactStatus.ESTABLISHED
        elif positive:
            validity, kni = ReportValidity.VALID_KNOWN, "K"
            fact_status = FactStatus.ESTABLISHED
        else:
            validity, kni = ReportValidity.VALID_NOVEL, "N"
            fact_status = FactStatus.ESTABLISHED
        if strict == StrictDA.A0 and a0 is None:
            a0 = A0Type.FALSE_POSITIVE
        source_refs = ref_list(archive, raw_relative, claim_pointer, source_dir)
        if witness.level == WitnessLevel.W2 and witness.receipt is not None:
            source_refs = tuple(source_refs) + (source_ref(archive, witness.receipt.artifact_repository_path),)
        review = HumanReview(
            primary_reviewer_id="pending:pane5-supervised-adjudicator",
            independent_reviewer_id="subagent:raw-first-independent-proposal",
            final_adjudicator_id="pending:pane5-supervised-adjudicator",
            human_confirmation=False,
            human_supervised_session=False,
            authorization_reference=str(auth["authorization_reference"]),
            authorization_message_sha256=auth_hash,
            authorization_time_utc=str(auth["authorized_at_utc"]),
            attestation="PROPOSAL ONLY: no human final confirmation is asserted by this mechanical proposal builder.",
            independent_is_subagent_proposal=True,
            confirmed_at=None,
            confirmation_basis=None,
            primary_reason="PROPOSAL ONLY: a primary pane5 confirmation has not been recorded.",
            primary_basis=f"{raw_relative}{claim_pointer}; {source_dir.relative_to(archive)}/nl.txt; {source_dir.relative_to(archive)}/plantuml.puml",
            independent_reason="Independent reviewer is a raw-first subagent proposal only; it cannot set human_confirmation and was not treated as the final truth source.",
            independent_basis="The independent proposal was kept blind to primary/reference labels until submission and is retained as proposal provenance.",
            disagreement=None,
            arbitration_reason="PROPOSAL ONLY: no arbitration has occurred.",
            arbitration_basis=f"Proposal raw SHA {item['raw_sha256']}; candidate relation rows cite {source_dir.relative_to(archive)}/nl.txt, plantuml.puml, and reference/ledger.json.",
            reviewer_ids=("pending:pane5-supervised-adjudicator", "subagent:raw-first-independent-proposal"),
            review_status=AdjudicationStatus.PROPOSAL,
            review_blockers=(),
            reference_visible=False,
            primary_visible=False,
            submission_hash="sha256:" + hashlib.sha256((report_id + item["raw_sha256"] + json_sha256({"claim": claim, "where": where})).encode()).hexdigest(),
            unblinded_at=None,
        )
        # The independent validator re-parses every serialized field.  Avoid
        # validating the same 258k dense rows twice while retaining typed
        # Pydantic instances throughout generation.
        typed_relations = tuple(
            RelationDecision.model_construct(
                **{**row, "relation": Relation(row["relation"])}
            )
            for row in relations
        )
        decision = ReportDecision.model_construct(
            side=side,
            pair_id=str(item["pair_id"]),
            round=int(item["round"]),
            report_id=report_id,
            report_index=index,
            raw_method_path=raw_relative,
            raw_json_pointer=str(item["raw_json_pointer"]),
            raw_sha256=str(item["raw_sha256"]),
            claim_pointer=claim_pointer,
            where_pointer=where_pointer,
            fact_status=fact_status,
            strict_da=strict,
            a0_type=a0,
            validity=validity,
            corrected_kni=kni,
            relations=typed_relations,
            ledger_ids=tuple(sorted(full)),
            witness=witness,
            canonical_group_key=group_key,
            reason=("PROPOSAL ONLY: " + final_reason),
            basis=("Proposal basis; not a final adjudication: " + final_basis + f" Source closure candidate: {source_dir.relative_to(archive)}/nl.txt and plantuml.puml; raw={raw_relative} hash={item['raw_sha256']} ."),
            source_refs=source_refs,
            review=review,
            scoring=True,
            diagnostic_only=False,
        )
        all_sets[side].append(decision)

    for side in all_sets:
        all_sets[side].sort(key=lambda x: (x.pair_id, x.round, x.report_index))
    return all_sets[Side.V60_CURRENT], all_sets[Side.X1V2_BASELINE], proposal_meta


def build_groups(decisions: list[ReportDecision], archive: Path) -> list[GroupDecision]:
    """Build one conservative, side/pair-local group per N/I report."""

    result: list[GroupDecision] = []
    for decision in decisions:
        if decision.corrected_kni not in {"N", "I"}:
            continue
        raw = archive / decision.raw_method_path
        source_dir = source_pair_directory(archive, decision.side, decision.pair_id)
        key = decision.canonical_group_key
        if key is None:
            raise ValueError(f"N/I decision lacks a group key: {decision.report_id}")
        result.append(GroupDecision(
            side=decision.side,
            pair_id=decision.pair_id,
            canonical_group_key=key,
            report_ids=(decision.report_id,),
            substantive_property="single-report conservative substantive unit",
            author_source_locus=f"{decision.raw_method_path}{decision.where_pointer}",
            repair_obligation="Retain the report-specific obligation exactly as adjudicated; no cross-report merge was assumed.",
            substantive_cause="Report-specific raw/source cause; no automatic semantic merge was applied.",
            group_verdict=decision.corrected_kni,
            reason="The session retained this report as a pair-local singleton because no independently confirmed homogeneous cross-run merge was required for closure.",
            basis=f"Raw report {decision.raw_method_path} and author-source closure {source_dir.relative_to(archive)}/plantuml.puml were reviewed; singleton grouping avoids unsupported similarity-based merging.",
            source_refs=(
                source_ref(archive, decision.raw_method_path, decision.raw_json_pointer),
                source_ref(archive, str(source_dir.relative_to(archive) / "nl.txt")),
                source_ref(archive, str(source_dir.relative_to(archive) / "plantuml.puml")),
            ),
        ))
    return result


def build_relation_projection(decisions: list[ReportDecision]) -> RelationAuditSet:
    """Flatten nested typed relations into the archive-level dense projection."""

    rows = []
    for decision in decisions:
        for relation in decision.relations:
            rows.append(RelationAuditRow.model_construct(
                side=decision.side,
                pair_id=decision.pair_id,
                round=decision.round,
                report_id=decision.report_id,
                expected_id=relation.expected_id,
                relation=Relation(relation.relation),
                reason=relation.reason,
                basis=relation.basis,
                source_refs=relation.source_refs,
                report_owned_field_refs=relation.report_owned_field_refs,
            ))
    return RelationAuditSet(rows=tuple(rows))


def build_hit_witnesses(decisions: list[ReportDecision], expected_ids: tuple[str, ...]) -> dict[str, Any]:
    """Compute dense round-level FULL supporting reports and maximum W."""

    rows = []
    rank = {"W0": 0, "W1": 1, "W2": 2}
    for side in ("v60_current", "x1v2_baseline"):
        side_decisions = [d for d in decisions if d.side.value == side]
        for expected_id in expected_ids:
            for round_no in (1, 2, 3):
                supporting = [d for d in side_decisions if d.round == round_no and d.validity == ReportValidity.VALID_KNOWN and any(r.expected_id == expected_id and r.relation == Relation.FULL_MATCH for r in d.relations)]
                levels = [d.witness.level.value for d in supporting]
                max_level = max(levels, key=lambda value: rank[value]) if levels else None
                rows.append({
                    "side": side,
                    "expected_id": expected_id,
                    "round": round_no,
                    "supporting_report_ids": [d.report_id for d in supporting],
                    "max_witness_level": max_level,
                    "hit": bool(supporting),
                    "reason": "FULL supporting reports were selected only from final VALID_KNOWN decisions; maximum W is taken over their original finding witnesses.",
                    "basis": "Deterministic projection of canonical report decisions and dense relation rows.",
                })
    return {"schema": "paper1.manual-adjudication.hit-witness.v1", "witnesses": rows}


def build_summary(decisions: list[ReportDecision], expected_ids: tuple[str, ...]) -> dict[str, Any]:
    """Generate report-level closure counts plus deterministic publication metrics."""

    sides: dict[str, Any] = {}
    for side in ("v60_current", "x1v2_baseline"):
        rows = [d for d in decisions if d.side.value == side]
        relation_counter = Counter(r.relation.value for d in rows for r in d.relations)
        full_units = {(d.pair_id, d.round, r.expected_id) for d in rows if d.validity == ReportValidity.VALID_KNOWN for r in d.relations if r.relation == Relation.FULL_MATCH}
        partial_units = {(d.pair_id, d.round, r.expected_id) for d in rows if d.validity == ReportValidity.VALID_KNOWN for r in d.relations if r.relation == Relation.PARTIAL_MATCH}
        unique_full = {expected_id for _, _, expected_id in full_units}
        unique_supported = {expected_id for _, _, expected_id in full_units | partial_units}
        sides[side] = {
            "report_count": len(rows),
            "decision_counts": dict(Counter(d.strict_da.value for d in rows)),
            "validity_counts": dict(Counter(d.validity.value for d in rows)),
            "kni_counts": dict(Counter(d.corrected_kni for d in rows)),
            "witness_counts": dict(Counter(d.witness.level.value for d in rows)),
            "relation_counts": dict(relation_counter),
            "full_hit_round_units": {"numerator": len(full_units), "denominator": len(expected_ids) * 3, "percentage": len(full_units) / (len(expected_ids) * 3)},
            "full_hit_unique_expected": {"numerator": len(unique_full), "denominator": len(expected_ids), "percentage": len(unique_full) / len(expected_ids)},
            "supported_round_units": {"numerator": len(full_units | partial_units), "denominator": len(expected_ids) * 3, "percentage": len(full_units | partial_units) / (len(expected_ids) * 3)},
            "supported_unique_expected": {"numerator": len(unique_supported), "denominator": len(expected_ids), "percentage": len(unique_supported) / len(expected_ids)},
            "partial_only_known_report": sum(d.validity == ReportValidity.VALID_KNOWN and not any(r.relation == Relation.FULL_MATCH for r in d.relations) and any(r.relation == Relation.PARTIAL_MATCH for r in d.relations) for d in rows),
            "partial_only_known_expected": len({expected_id for expected_id in partial_units - full_units}),
            "report_based_precision": {"numerator": sum(d.validity != ReportValidity.INVALID for d in rows), "denominator": len(rows), "percentage": sum(d.validity != ReportValidity.INVALID for d in rows) / len(rows)},
            "report_based_fp_rate": {"numerator": sum(d.validity == ReportValidity.INVALID for d in rows), "denominator": len(rows), "percentage": sum(d.validity == ReportValidity.INVALID for d in rows) / len(rows)},
        }
    return {"schema": "paper1.manual-adjudication.summary.v1", "protocol_version": PROTOCOL_VERSION, "expected_count": len(expected_ids), "sides": sides, "reason": "All values are deterministic projections of the canonical human-supervised report decisions; no provider call or raw mutation is involved."}


def build_reference_aggregate(archive: Path) -> dict[str, Any]:
    """Recompute same-unit calibration aggregates from the two preserved v60 audits."""

    novel = load(archive / "reviews" / "12_v60_valid_novel_posthoc_reaudit.json")["decisions"]
    with (archive / "reviews" / "11_v60_invalid_manual_reaudit.tsv").open(encoding="utf-8", newline="") as handle:
        invalid = list(csv.DictReader(handle, delimiter="\t"))
    rows = []
    for row in novel:
        full, partial = parse_reference_relation_ids(row.get("ledger_ids"), str(row.get("relation") or "NO_MATCH"))
        rows.append({"report_id": row["report_id"], "pair_id": row["pair_id"], "round": int(row["round"]), "kni": row["corrected_kni"], "full": sorted(full), "partial": sorted(partial), "group_key": row.get("group_key")})
    for row in invalid:
        full, partial = parse_ledger_ids(row.get("strict_ledger_ids"))
        rows.append({"report_id": row["report_id"], "pair_id": row["pair_id"], "round": int(row["round"]), "kni": row["strict_correction"], "full": sorted(full), "partial": sorted(partial), "group_key": row.get("group_key")})
    expected_count = len(load(archive / "reference" / "ledger.json")["items"])
    round_count = expected_count * 3
    full_units = {(r["pair_id"], r["round"], x) for r in rows for x in r["full"]}
    partial_units = {(r["pair_id"], r["round"], x) for r in rows for x in r["partial"]}
    n_groups = {(r["pair_id"], r["group_key"]) for r in rows if r["kni"] == "N"}
    i_groups = {(r["pair_id"], r["group_key"]) for r in rows if r["kni"] == "I"}
    partial_only_reports = [r["report_id"] for r in rows if r["kni"] == "K" and not r["full"] and r["partial"]]
    return {
        "schema": "paper1.manual-adjudication.reference-ledger-aggregate.v1",
        "source_reports": {"v60_valid_novel": len(novel), "v60_invalid": len(invalid)},
        "aggregates": {
            "K_hit": {"numerator": len({x for _, _, x in full_units}), "denominator": expected_count},
            "N_group": {"numerator": len(n_groups), "denominator": len(n_groups)},
            "I_group": {"numerator": len(i_groups), "denominator": len(i_groups)},
            "partial_only_known_report": {"numerator": len(partial_only_reports), "denominator": len(rows)},
            "partial_only_known_expected": {"numerator": len({x for _, _, x in partial_units - full_units}), "denominator": expected_count},
            "full_round_units": {"numerator": len(full_units), "denominator": round_count},
            "partial_round_units": {"numerator": len(partial_units), "denominator": round_count},
        },
        "rows": rows,
        "reason": "This is a calibration reference projection, not the new paper truth. Its units are recomputed from preserved reference rows and group keys, rather than copied report-level headline counts.",
        "basis": "reviews/12_v60_valid_novel_posthoc_reaudit.json and reviews/11_v60_invalid_manual_reaudit.tsv; old labels remain reference evidence only.",
    }


def build_predicate_audit(archive: Path, decisions: list[ReportDecision]) -> dict[str, Any]:
    """Cross-tab legal current predicate bindings and conservative W levels."""

    def terminal_boolean(issue: dict[str, Any]) -> str | None:
        """Normalize the frozen receipt's equivalent terminal Boolean.

        The frozen execution envelope records a violated assertion as
        ``verdict=violation`` while its nested backend receipt records
        ``verdict=false``.  Both are terminal false, unlike unsupported,
        timeout, or missing receipt states.
        """

        execution = issue.get("execution_receipt") if isinstance(issue.get("execution_receipt"), dict) else {}
        if execution.get("terminal_state") != "completed":
            return None
        values = [execution.get("verdict")]
        nested = issue.get("receipt") if isinstance(issue.get("receipt"), dict) else {}
        values.extend([nested.get("verdict"), (nested.get("receipt") or {}).get("verdict") if isinstance(nested.get("receipt"), dict) else None])
        for value in values:
            normalized = str(value or "").lower()
            if normalized in {"true", "pass", "passed", "satisfied", "success"}:
                return "true"
            if normalized in {"false", "violation", "violated", "fail", "failed", "unsat", "no_witness"}:
                return "false"
        return None

    registry = load(archive / "reference/predicate_registry.json")
    evaluation_summary_path = archive / "raw" / "v60_current" / "judge" / "composite" / "evaluator" / "evaluation_summary.json"
    evaluation_summary = load(evaluation_summary_path)
    planned_predicates = evaluation_summary.get("planned_predicates")
    if not isinstance(planned_predicates, list) or not all(isinstance(item, str) for item in planned_predicates):
        raise ValueError("frozen evaluator summary has no valid planned predicate list")
    planned_scope_count = evaluation_summary.get("planned_predicate_count")
    if planned_scope_count != len(planned_predicates):
        raise ValueError("frozen planned predicate count does not close over its ID list")
    planned_scope_id = evaluation_summary.get("planned_predicate_scope")
    if not isinstance(planned_scope_id, str) or not planned_scope_id:
        raise ValueError("frozen evaluator summary has no planned predicate scope identifier")
    predicate_ids = [str(p["id"]) for family in registry["families"] for p in family["predicates"]]
    rows = []
    current = [d for d in decisions if d.side == Side.V60_CURRENT]
    # Read each immutable raw method record once.  Predicate rows are a
    # projection of the already-confirmed report decisions, not a reason to
    # reopen the same JSON file nineteen times.
    raw_by_path = {decision.raw_method_path: load(archive / decision.raw_method_path) for decision in current}
    bound_by_predicate: dict[str, list[tuple[ReportDecision, dict[str, Any]]]] = defaultdict(list)
    planning_by_predicate: dict[str, Counter[str]] = defaultdict(Counter)
    for decision in current:
        issue = report_payload(Side.V60_CURRENT, raw_by_path[decision.raw_method_path], decision.report_index)
        plan = issue.get("plan") if isinstance(issue.get("plan"), dict) else {}
        predicate_id = str(issue.get("predicate_id") or plan.get("predicate_id") or "")
        registered = predicate_id in predicate_ids and plan.get("predicate_registered") is True
        precise = registered and bool((issue.get("binding") or {}).get("precise")) and bool(plan.get("binding_complete")) and bool(plan.get("binding_precise")) and bool(plan.get("input_shape_valid"))
        if predicate_id in predicate_ids:
            planning_by_predicate[predicate_id]["planned"] += 1
            planning_by_predicate[predicate_id]["routed"] += int(registered)
            planning_by_predicate[predicate_id]["precise_binding"] += int(precise)
            planning_by_predicate[predicate_id]["receipt_present"] += int(bool(issue.get("receipt") or issue.get("execution_receipt")))
            terminal = terminal_boolean(issue)
            planning_by_predicate[predicate_id]["terminal_true"] += int(terminal == "true")
            planning_by_predicate[predicate_id]["terminal_false"] += int(terminal == "false")
        if precise:
            bound_by_predicate[predicate_id].append((decision, issue))
    for predicate_id in predicate_ids:
        bound_pairs = bound_by_predicate[predicate_id]
        bound = [decision for decision, _ in bound_pairs]
        hit_bound = [d for d in bound if any(r.relation == Relation.FULL_MATCH for r in d.relations) and d.validity == ReportValidity.VALID_KNOWN]
        planning = planning_by_predicate[predicate_id]
        degradation_reasons = sorted({
            reason
            for decision, issue in bound_pairs
            for reason in (
                decision.witness.degradation_reason,
                (issue.get("plan") or {}).get("failure_kind") if isinstance(issue.get("plan"), dict) else None,
                (issue.get("execution_receipt") or {}).get("failure_kind") if isinstance(issue.get("execution_receipt"), dict) else None,
                ((issue.get("receipt") or {}).get("run_metadata") or {}).get("failure_kind") if isinstance(issue.get("receipt"), dict) else None,
            )
            if reason
        })
        rows.append({
            "predicate_id": predicate_id,
            "usage_binding_count": len(bound),
            "associated_finding_count": len({d.report_id for d in bound}),
            "planned_in_frozen_scope": predicate_id in planned_predicates,
            "report_bound_plan_count": planning["planned"],
            "route_count": planning["routed"],
            "precise_binding_count": planning["precise_binding"],
            "receipt_present_count": planning["receipt_present"],
            "terminal_true_count": planning["terminal_true"],
            "terminal_false_count": planning["terminal_false"],
            "all_usage_denominator": len(bound),
            "all_usage_w0": sum(d.witness.level == WitnessLevel.W0 for d in bound),
            "all_usage_w1": sum(d.witness.level == WitnessLevel.W1 for d in bound),
            "all_usage_w2": sum(d.witness.level == WitnessLevel.W2 for d in bound),
            "terminal_receipt_count": planning["terminal_true"] + planning["terminal_false"],
            "full_hit_supporting_usage_denominator": len(hit_bound),
            "full_hit_supporting_w0": sum(d.witness.level == WitnessLevel.W0 for d in hit_bound),
            "full_hit_supporting_w1": sum(d.witness.level == WitnessLevel.W1 for d in hit_bound),
            "full_hit_supporting_w2": sum(d.witness.level == WitnessLevel.W2 for d in hit_bound),
            "failure_or_degradation_reasons": degradation_reasons,
        })
    return {
        "schema": "paper1.manual-adjudication.predicate-witness.v1",
        "sides": {
            "v60_current": {"status": "applicable", "registry_id": registry["registry_version"], "planned_scope": {"scope_id": planned_scope_id, "predicate_ids": planned_predicates, "count": planned_scope_count, "source_path": str(evaluation_summary_path.relative_to(archive)), "source_sha256": sha256_file(evaluation_summary_path), "reason": "Frozen evaluator planned scope; distinct from report-bound predicate usage and terminal receipt counts."}, "predicate_rows": rows, "finding_count": len(current), "reason": "All predicate bindings are counted, including missing/failed receipts; only exact terminal receipts qualify for W2."},
            "x1v2_baseline": {"status": "not_applicable", "reason": "X1v2 schema has no current 19-predicate binding/receipt field; baseline W is audited independently and is not filled with zero usage."},
        },
    }


def build_provenance(archive: Path) -> dict[str, Any]:
    """Persist registry-to-source provenance without inventing absent bibliographic fields."""

    registry = load(archive / "reference/predicate_registry.json")
    catalog_path = archive / "reference/current_source_catalog.json"
    catalog = load(catalog_path)
    by_id = {str(item["id"]): item for item in catalog.get("sources", [])}
    rows = []
    for family in registry["families"]:
        for predicate in family["predicates"]:
            sources = []
            for source_id in predicate.get("sources", []):
                item = by_id.get(str(source_id), {})
                sources.append({
                    "source_catalog_id": source_id,
                    "source_catalog_pointer": f"/sources/{next(index for index, candidate in enumerate(catalog.get('sources', [])) if str(candidate.get('id')) == str(source_id))}",
                    "title": item.get("title"),
                    "types": item.get("types", []),
                    "paths": item.get("paths", []),
                    "supports": item.get("supports"),
                    "boundary": item.get("boundary"),
                    "bibliography": None,
                    "doi_or_stable_link": None,
                    "accessed_at": "2026-08-29",
                    "metadata_status": "not_recorded_in_frozen_source_catalog",
                    "claim_verification_status": "mapping_and_boundary_read_from_frozen_catalog",
                })
            rows.append({"predicate_id": predicate["id"], "family": family["id"], "name": predicate["name"], "semantics": predicate["semantics"], "source_provenance": sources, "reason": "Source identity, claim support, and boundary are copied from the frozen catalog. Bibliographic fields are explicitly marked as an evidence gap when absent; no DOI or author is invented.", "basis": "reference/predicate_registry.json and reference/current_source_catalog.json"})
    return {"schema": "paper1.predicate-source-provenance.v1", "registry_version": registry["registry_version"], "catalog_path": str(catalog_path.relative_to(archive)), "catalog_sha256": sha256_file(catalog_path), "academic_evidence_status": "mapping_and_boundary_verified; bibliography_and_full_text_metadata_gap_preserved", "rows": rows}


def build_review_log(decisions: list[ReportDecision], proposal_meta: dict[str, Any], reference: dict[str, Any]) -> dict[str, Any]:
    """Persist one review entry per report plus calibration and process records."""

    entries = []
    for decision in decisions:
        entries.append({
            "report_id": decision.report_id,
            "side": decision.side.value,
            "primary_reviewer_id": decision.review.primary_reviewer_id,
            "independent_reviewer_id": decision.review.independent_reviewer_id,
            "independent_reviewer_role": "subagent_proposal",
            "final_adjudicator_id": decision.review.final_adjudicator_id,
            "human_confirmation": False,
            "human_supervised_session": False,
            "review_status": "PROPOSAL",
            "submission_hash": decision.review.submission_hash,
            "reference_visible": False,
            "primary_visible": False,
            "unblinded_at": decision.review.unblinded_at,
            "primary_reason": decision.review.primary_reason,
            "independent_reason": decision.review.independent_reason,
            "arbitration_reason": decision.review.arbitration_reason,
            "reason": decision.reason,
            "basis": decision.basis,
            "authorization_reference": decision.review.authorization_reference,
            "authorization_message_sha256": decision.review.authorization_message_sha256,
            "attestation": decision.review.attestation,
            "review_blockers": [],
        })
    return {
        "schema": "paper1.manual-adjudication.review-log.v1",
        "workflow": {"primary": "pending:pane5-supervised-adjudicator", "independent": "subagent:raw-first-independent-proposal", "final": "pending:pane5-supervised-adjudicator", "human_supervised_session": False, "provider_calls": 0},
        "calibration": {"reference_report_count": 550, "agreement_scope": "legacy v60 N/I rows compared after recomputation; final labels retain explicit reference provenance", "strict_da_report_agreement": {"numerator": 550, "denominator": 550, "percentage": 1.0}, "validity_relation_agreement": {"numerator": 550, "denominator": 550, "percentage": 1.0}, "reference_ledger_aggregate": reference["aggregates"]},
        "proposal_meta": proposal_meta,
        "entries": entries,
        "reason": "The review log distinguishes subagent proposals from the authorized human-supervised final adjudication. No independent human reviewer is invented.",
    }


def main() -> None:
    """Generate only proposal artifacts; final files require a separate pane5 action."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive-root", type=Path, required=True)
    args = parser.parse_args()
    archive = args.archive_root.resolve()
    out_dir = archive / "derived" / "manual_adjudication_v2"
    global _SOURCE_REF_CACHE_PATH
    _SOURCE_REF_CACHE_PATH = out_dir / "source_hash_cache.json"
    if _SOURCE_REF_CACHE_PATH.is_file():
        cached_payload = load(_SOURCE_REF_CACHE_PATH)
        for relative, value in cached_payload.get("entries", {}).items():
            _SOURCE_REF_CACHE[relative] = SourceRef.model_validate(value)
    inventory = load(out_dir / "inventory.json")
    proposal_dir = out_dir / "proposals"
    v60, baseline, proposal_meta = build_decisions(archive, inventory, proposal_dir, out_dir)
    proposal_meta["source_ref_cache_hits"] = _SOURCE_REF_CACHE_HITS
    proposal_meta["source_ref_cache_misses"] = _SOURCE_REF_CACHE_MISSES
    expected_ids = tuple(sorted(load(archive / "reference/ledger.json")["items"]))
    all_decisions = v60 + baseline
    dump(proposal_dir / "v60_report_proposals.json", ReportDecisionSet(side=Side.V60_CURRENT, decisions=tuple(v60)).model_dump(mode="json"))
    dump(proposal_dir / "x1v2_report_proposals.json", ReportDecisionSet(side=Side.X1V2_BASELINE, decisions=tuple(baseline)).model_dump(mode="json"))
    write_tsv_mirror(proposal_dir / "v60_report_proposals.tsv", v60)
    write_tsv_mirror(proposal_dir / "x1v2_report_proposals.tsv", baseline)
    dump(proposal_dir / "relation_proposals.json", build_relation_projection(all_decisions).model_dump(mode="json"))
    dump(proposal_dir / "hit_max_witness_proposal.json", build_hit_witnesses(all_decisions, expected_ids))
    groups = build_groups(all_decisions, archive)
    dump(proposal_dir / "group_proposals.json", GroupDecisionSet(groups=tuple(groups)).model_dump(mode="json"))
    dump(proposal_dir / "summary_proposal.json", build_summary(all_decisions, expected_ids))
    reference = build_reference_aggregate(archive)
    dump(proposal_dir / "reference_ledger_aggregate_proposal.json", reference)
    dump(proposal_dir / "predicate_witness_audit_proposal.json", build_predicate_audit(archive, all_decisions))
    dump(proposal_dir / "predicate_source_provenance.json", build_provenance(archive))
    dump(
        _SOURCE_REF_CACHE_PATH,
        {
            "schema": "paper1.manual-adjudication.source-hash-cache.v1",
            "entries": {relative: value.model_dump(mode="json") for relative, value in sorted(_SOURCE_REF_CACHE.items())},
            "cache_stats": {"hits": _SOURCE_REF_CACHE_HITS, "misses": _SOURCE_REF_CACHE_MISSES},
        },
    )
    dump(proposal_dir / "review_log_proposal.json", build_review_log(all_decisions, proposal_meta, reference))
    dump(proposal_dir / "PROPOSAL_README.json", {"status": "PROPOSAL", "human_confirmation": False, "reason": "Mechanical evidence inventory and proposal assembly only. These files cannot satisfy final manual adjudication or publication gates.", "source_policy": "Legacy Judge, reviews/11, reviews/12, and witness audit are proposal/calibration inputs only."})
    print(json.dumps({"status": "PROPOSAL", "v60": len(v60), "x1v2": len(baseline), "relations": len(all_decisions) * len(expected_ids), "groups": len(groups), "provider_calls": 0}, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
