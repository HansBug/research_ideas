#!/usr/bin/env python3
"""Fail-closed readiness gate for the Paper1 R1 publication surface.

The repository owns stable research facts. Reviewer results, blind-search
payloads, and PR-body snapshots live outside the repository and must be passed
explicitly with ``--review-evidence``. This checker never runs a provider,
method, Judge, or benchmark.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any

import jsonschema


CURRENT = {
    *(f"S{i}" for i in range(1, 7)),
    *(f"G{i}" for i in range(1, 5)),
    *(f"R{i}" for i in range(1, 5)),
    *(f"V{i}" for i in range(1, 6)),
}
LEGACY = {
    "occupancy_after", "reaches", "event_consumed", "terminates",
    "variable_delta_after", "stays_in", "persists_until", "invariant",
    "response_within", "event_declared", "variable_declared", "initial_target",
    "state_declared", "containment", "action_declared", "cardinality",
    "edge_declared", "guard_distinguishable", "effect_declared",
}
REQUIRED_ROLES = {
    "predicate_evidence", "unblind_novelty_disposition", "closest_work_fulltext",
    "method_soundness", "paper_outline", "fact_link_test", "adversarial_claim",
    "language_shuorenhua", "experiment_gate",
}
BASE_COMMIT = "537971a3f"
REQUIRED_STATIC_PATHS = (
    "README.md", "story/README.md", "story/paper_story.md", "story/paper_outline.md",
    "story/claim_evidence_map.md", "story/model_scope.md", "story/terminology_policy.md",
    "story/paper_result_inventory.md", "story/experiment_dependent_gates.json",
    "story/experiment_dependent_gates.schema.json", "related_work/README.md",
    "related_work/assertion_output_form_evidence.md", "related_work/closest_work_matrix.md",
    "related_work/provenance/README.md", "related_work/provenance/SUMMARY.md",
    "related_work/provenance/CURRENT_SOURCE_AUDIT.md",
    "related_work/provenance/predicate_provenance.md",
    "related_work/provenance/current_source_catalog.json",
    "related_work/provenance/tools/check_r1_readiness.py",
    "method/src/paper_stm_method/compiler/soundness.py",
    "method/src/paper_stm_method/resources/predicate_registry.json",
    "method/tests/test_provider_free_fixture.py",
)
ROLE_REQUIRED_PATHS = {
    "predicate_evidence": {
        "related_work/provenance/predicate_provenance.md",
        "related_work/provenance/current_source_catalog.json",
    },
    "unblind_novelty_disposition": {
        "related_work/closest_work_matrix.md", "story/claim_evidence_map.md",
    },
    "closest_work_fulltext": {"related_work/closest_work_matrix.md"},
    "method_soundness": {
        "method/src/paper_stm_method/compiler/soundness.py",
        "method/tests/test_provider_free_fixture.py",
        "related_work/provenance/predicate_provenance.md",
    },
    "paper_outline": {
        "story/paper_outline.md", "story/paper_result_inventory.md", "story/paper_story.md",
    },
    "fact_link_test": set(REQUIRED_STATIC_PATHS),
    "adversarial_claim": {
        "story/claim_evidence_map.md", "story/paper_story.md",
        "story/paper_outline.md", "related_work/closest_work_matrix.md",
    },
    "language_shuorenhua": {"story/paper_outline.md", "story/terminology_policy.md"},
    "experiment_gate": {
        "story/experiment_dependent_gates.json",
        "story/experiment_dependent_gates.schema.json", "story/paper_outline.md",
        "story/claim_evidence_map.md",
    },
}
STATUS = {"QUALIFIED_EXTERNAL", "DEFINITIONAL_METHOD_OWNED_NA"}
METHOD_STATUS = {"SPECIFIED_AND_TESTED", "NOT_APPLICABLE_WITH_RATIONALE"}
INSTANCE_STATUS = {"SOURCE_BOUND", "NOT_APPLICABLE_WITH_RATIONALE"}
IMPLEMENTATION = {
    "EXACT", "IMPLEMENTATION_SUBSET", "SOUND_TRUE_PROXY", "SOUND_FALSE_PROXY",
    "RESOLVED_CLAIM_EXCLUSION",
}
POLARITIES = {"true", "false", "unknown", "failure"}
WITNESS_CEILINGS = {"W0", "W1", "W2", "NOT_APPLICABLE"}
PUBLICATION_ELIGIBILITY = {"ELIGIBLE", "CONDITIONAL", "INELIGIBLE"}
EXPERIMENT_ID = re.compile(r"TODO-EXPERIMENT-[0-9]{2}")
FOOTNOTE_REF = re.compile(r"(?<!\^)\[\^([A-Za-z0-9_-]+)\](?!:)")
FOOTNOTE_DEF = re.compile(r"^\[\^([A-Za-z0-9_-]+)\]:", re.MULTILINE)
PREDICATE_ID = re.compile(r"(?<![A-Za-z0-9_])([SGRV][1-9])(?![A-Za-z0-9_])")
REQUIRED_HUMAN_AUDIT_FIELDS = (
    "**现行精确命题。**",
    "**义务与出处。**",
    "**方法、实例与 W2。**",
    "**执行、极性与发表。**",
)
REQUIRED_INVENTORY_MARKERS = (
    "9 个在用自然语言簇",
    "310/435=71.26%",
    "105/117=89.74%",
    "119/145=82.07%",
    "86/145=59.31%",
    "37/39=94.87%",
    "337/435=77.47%",
    "1271",
    "980/1271=77.10%",
    "0/113/197",
    "12/19",
    "749/231/291",
    "721/259/120/171",
    "D0 `120`",
    "compiler-owned `38`",
    "conservative substantive N groups",
    "825/1271=64.91%",
    "$7.18277320",
    "G2 publication exclusion",
    "V4 exclusion",
)
BLOCKED = re.compile(
    r"TODO-CITATION|待核验|source-status\s*=\s*candidate|"
    r"默认禁止.{0,40}first|最低防守措辞|19 个谓词.{0,40}未完成学术资格"
)
REPO = "HansBug/research_ideas"
PR_NUMBERS = {"r1": 197, "umbrella": 179}
# These are UTF-8 hashes of the bodies fetched at R1 task start and after the
# only permitted contract edit. They make the permitted PR-body delta concrete:
# the initial #197 body is anchored, #179 is byte-for-byte unchanged, and #197
# may finish only at the reviewed replacement body.
TASK_START_BODY_SHA256 = {
    "r1": "311f3964e06b57f6ec0c60ed4cf279f3e7b5d776da8e2063d5b331a0e2ba356e",
    "umbrella": "cdc946bd8f17f7fa9f0d5597f2f7ee25b6612833215b6e80d0de5f21e9a76652",
}
PERMITTED_FINAL_BODY_SHA256 = {
    "r1": "ccdd700b9af21a3317661f253bc44b1fcdbc39f9c2be24c93ad2d335d15f4370",
    "umbrella": "cdc946bd8f17f7fa9f0d5597f2f7ee25b6612833215b6e80d0de5f21e9a76652",
}
BUNDLE_SCHEMA_VERSION = "paper1.r1-final-review.v1"
BLIND_PACKET_SCHEMA_VERSION = "paper1.r1-blind-packet.v1"
BLIND_RECORD_SCHEMA_VERSION = "paper1.r1-blind-search-record.v1"
CANONICAL_CURRENT_RAW = (
    "final_results/v60_current_vs_x1v2_baseline/raw/v60_current/method/method"
)
# These filters describe audited claim exclusions. They do not reclassify the
# frozen runtime data. G2 excludes its completed W2 false receipts; V4 excludes
# both terminal polarities because a topology leaf probe establishes neither a
# universal progress proof nor a universal deadlock counterexample.
IMPACT_RECEIPT_FILTERS = {
    "G2": {"predicate_verdict": {"false"}},
    "V4": {"predicate_verdict": {"true", "false"}},
}


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_path(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def is_nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def jcs_bytes(value: Any) -> bytes:
    """Return RFC 8785-compatible bytes for the JSON types used by R1.

    R1 review payloads contain strings, integers, booleans, nulls, arrays, and
    objects. Floats are deliberately rejected so a Python-vs-ECMAScript number
    serializer cannot alter a review hash. R1 object keys are ASCII, for which
    Python's lexicographic ordering equals RFC 8785's UTF-16 ordering.
    """

    def render(item: Any) -> str:
        if item is None:
            return "null"
        if item is True:
            return "true"
        if item is False:
            return "false"
        if isinstance(item, int) and not isinstance(item, bool):
            return str(item)
        if isinstance(item, float):
            raise ValueError("JCS review payloads may not contain floating-point values")
        if isinstance(item, str):
            return json.dumps(item, ensure_ascii=False, separators=(",", ":"))
        if isinstance(item, list):
            return "[" + ",".join(render(entry) for entry in item) + "]"
        if isinstance(item, dict):
            if not all(isinstance(key, str) for key in item):
                raise ValueError("JCS object keys must be strings")
            return "{" + ",".join(
                render(key) + ":" + render(item[key]) for key in sorted(item)
            ) + "}"
        raise ValueError(f"unsupported JCS type: {type(item).__name__}")

    return render(value).encode("utf-8")


def jcs_sha256(value: Any) -> str:
    return sha256_bytes(jcs_bytes(value))


def add_error(errors: list[str], message: str) -> None:
    errors.append(message)


def check_footnotes(path: Path, errors: list[str]) -> None:
    text = path.read_text(encoding="utf-8")
    refs = FOOTNOTE_REF.findall(text)
    definitions = FOOTNOTE_DEF.findall(text)
    missing = sorted(set(refs) - set(definitions))
    orphan = sorted(set(definitions) - set(refs))
    duplicate = sorted({key for key in definitions if definitions.count(key) != 1})
    if missing:
        add_error(errors, f"{path.name}: footnote definitions missing for {missing}")
    if orphan:
        add_error(errors, f"{path.name}: orphan footnote definitions {orphan}")
    if duplicate:
        add_error(errors, f"{path.name}: duplicate footnote definitions {duplicate}")


def strip_protected_markdown(text: str) -> str:
    """Remove code, URLs, and bibliography from the terminology scan."""
    def blank(match: re.Match[str]) -> str:
        return " " * len(match.group(0))

    text = re.sub(r"```.*?```", blank, text, flags=re.DOTALL)
    text = re.sub(r"`[^`]*`", blank, text)
    text = re.sub(r"https?://\S+", blank, text)
    text = re.sub(r"\]\([^)]*\)", blank, text)
    return re.sub(r"^\[\^[^\]]+\]:.*$", blank, text, flags=re.MULTILINE)


def parse_term_policy(path: Path, errors: list[str]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    header_seen = False
    fields = ("term_id", "chinese", "english", "abbreviation", "first", "later", "exceptions")
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if cells[0] == "term_id":
            header_seen = True
            continue
        if cells[0].startswith("---"):
            continue
        if len(cells) != 7:
            add_error(errors, f"terminology policy malformed row: {line}")
            continue
        if any(not cell for cell in cells[:6]):
            add_error(errors, f"terminology policy contains empty required cell: {line}")
            continue
        rows.append(dict(zip(fields, cells, strict=True)))
    if not header_seen or not rows:
        add_error(errors, "terminology policy has no parseable seven-column term table")
    if len({row["term_id"] for row in rows}) != len(rows):
        add_error(errors, "terminology policy contains duplicate term_id")
    return rows


def check_terminology(paper_root: Path, errors: list[str]) -> None:
    terms = parse_term_policy(paper_root / "story/terminology_policy.md", errors)
    text = (paper_root / "story/paper_outline.md").read_text(encoding="utf-8")
    anchors = set(re.findall(r'<a id="([A-Za-z0-9_-]+)"></a>', text))
    checked = strip_protected_markdown(text)
    for term in terms:
        anchor = term["first"].strip("`")
        if anchor not in anchors:
            add_error(errors, f"terminology {term['term_id']}: first-occurrence anchor {anchor!r} is absent")
            continue
        first = checked.index(f'<a id="{anchor}"></a>')
        english = re.escape(term["english"])
        before = checked[:first]
        after = checked[first:]
        if re.search(english, before, re.IGNORECASE):
            add_error(errors, f"terminology {term['term_id']}: English full form occurs before declared anchor")
        occurrences = []
        for occurrence in re.finditer(english, after, re.IGNORECASE):
            start, end = occurrence.span()
            # Do not count a registered term merely because it is a suffix of
            # a longer, separately registered term, such as ``state machine``
            # inside ``finite control state machine``.
            nested = any(
                other["term_id"] != term["term_id"]
                and any(
                    full.start() <= start and end <= full.end()
                    for full in re.finditer(re.escape(other["english"]), after, re.IGNORECASE)
                )
                for other in terms
            )
            if not nested:
                occurrences.append(occurrence)
        if not occurrences:
            add_error(errors, f"terminology {term['term_id']}: English full form absent at declared anchor")
        elif len(occurrences) > 1:
            add_error(errors, f"terminology {term['term_id']}: English full form repeats outside protected spans")


def check_catalog(paper_root: Path, errors: list[str]) -> None:
    catalog = load_json(paper_root / "related_work/provenance/current_source_catalog.json")
    audit = catalog.get("r1_citation_audit")
    if not isinstance(audit, dict):
        add_error(errors, "source catalog lacks r1_citation_audit")
        return
    chronology = audit.get("chronology")
    chronology_keys = {
        "legacy_source_review", "source_unit_expansion", "typed_surface_remapping",
        "four_family_registry_freeze", "native_witness_execution", "r1_publication_audit_base",
        "leakage_disposition",
    }
    if not isinstance(chronology, dict) or set(chronology) != chronology_keys or not all(
        is_nonempty_string(chronology[key]) for key in chronology_keys
    ):
        add_error(errors, "catalog chronology/leakage metadata is incomplete")

    source_types: dict[str, set[str]] = {
        row["id"]: set(row.get("types", []))
        for row in catalog.get("sources", [])
        if isinstance(row, dict) and is_nonempty_string(row.get("id"))
        and isinstance(row.get("types"), list)
        and all(is_nonempty_string(source_type) for source_type in row["types"])
    }
    source_ids = set(source_types)
    academic_source_ids = {
        source_id for source_id, types in source_types.items()
        if types & {"domain", "formal"}
    }
    if "publication_eligibility_profiles" in audit:
        add_error(errors, "catalog must store publication eligibility directly on each predicate")

    rows = audit.get("predicate_audits")
    if not isinstance(rows, list):
        add_error(errors, "catalog predicate audits is not an array")
        return
    ids = [row.get("predicate_id") for row in rows if isinstance(row, dict)]
    if set(ids) != CURRENT or len(ids) != len(CURRENT):
        add_error(errors, f"catalog current predicate keyset is not exact: {sorted(set(ids) ^ CURRENT)}")
    expected_keys = {
        "predicate_id", "academic_qualification_status", "method_semantics_status",
        "instance_authority_status", "implementation_relation", "source_ids",
        "status_evidence", "publication_eligibility_by_polarity", "impact",
    }
    for row in rows:
        if not isinstance(row, dict) or set(row) != expected_keys:
            add_error(errors, f"catalog predicate audit has invalid keys: {row.get('predicate_id') if isinstance(row, dict) else row!r}")
            continue
        pid = row["predicate_id"]
        if row["academic_qualification_status"] not in STATUS:
            add_error(errors, f"{pid}: academic qualification is not closed")
        if row["method_semantics_status"] not in METHOD_STATUS:
            add_error(errors, f"{pid}: method semantics is not closed")
        if row["instance_authority_status"] not in INSTANCE_STATUS:
            add_error(errors, f"{pid}: instance authority is not closed")
        if row["implementation_relation"] not in IMPLEMENTATION:
            add_error(errors, f"{pid}: implementation relation is not closed")
        refs = row["source_ids"]
        if not isinstance(refs, list) or not refs or not set(refs) <= source_ids:
            add_error(errors, f"{pid}: source-ID closure is broken")
        evidence = row["status_evidence"]
        if not isinstance(evidence, dict) or set(evidence) != {"academic", "method", "instance"}:
            add_error(errors, f"{pid}: status evidence must have academic/method/instance objects")
        else:
            for responsibility, item in evidence.items():
                if not isinstance(item, dict) or set(item) != {"evidence_refs", "rationale"}:
                    add_error(errors, f"{pid}: {responsibility} evidence has invalid shape")
                    continue
                if not isinstance(item["evidence_refs"], list) or not item["evidence_refs"] or not is_nonempty_string(item["rationale"]):
                    add_error(errors, f"{pid}: {responsibility} evidence is empty")
            academic = evidence.get("academic", {})
            academic_refs = academic.get("evidence_refs", []) if isinstance(academic, dict) else []
            if (
                row["academic_qualification_status"] == "QUALIFIED_EXTERNAL"
                and not set(academic_refs) & academic_source_ids
            ):
                add_error(errors, f"{pid}: academic qualification lacks a domain/formal external source")
            if not any(
                isinstance(ref, str)
                and ref.startswith("related_work/provenance/predicate_provenance.md#quote-")
                for ref in academic_refs
            ):
                add_error(errors, f"{pid}: academic qualification lacks a primary-text quote anchor")
            instance = evidence.get("instance", {})
            instance_refs = instance.get("evidence_refs", []) if isinstance(instance, dict) else []
            required_instance_refs = {
                "pipeline/evidence_discovery/METHOD_PRINCIPLES.md#source-bound-instance-authority",
                "method/src/paper_stm_method/semantics/obligations.py",
                "method/src/paper_stm_method/evidence/receipts.py",
            }
            if row["instance_authority_status"] == "SOURCE_BOUND" and not required_instance_refs <= set(instance_refs):
                add_error(errors, f"{pid}: source-bound instance authority lacks binding/receipt contract refs")
            if any(
                isinstance(ref, str)
                and ref.startswith("related_work/provenance/predicate_provenance.md#")
                and "#quote-" not in ref
                for ref in [*academic_refs, *instance_refs]
            ):
                add_error(errors, f"{pid}: status evidence self-references a predicate heading instead of its authority")
        eligibility = row["publication_eligibility_by_polarity"]
        if not isinstance(eligibility, dict) or set(eligibility) != POLARITIES:
            add_error(errors, f"{pid}: publication eligibility lacks exact polarity keys")
        else:
            for polarity, item in eligibility.items():
                expected = {
                    "runtime_witness_ceiling", "publication_eligibility", "claim_scope", "evidence_refs",
                }
                if not isinstance(item, dict) or set(item) != expected:
                    add_error(errors, f"{pid}/{polarity}: publication eligibility has invalid object shape")
                    continue
                if item["runtime_witness_ceiling"] not in WITNESS_CEILINGS:
                    add_error(errors, f"{pid}/{polarity}: publication eligibility has invalid witness ceiling")
                if item["publication_eligibility"] not in PUBLICATION_ELIGIBILITY:
                    add_error(errors, f"{pid}/{polarity}: publication eligibility has invalid status")
                if not is_nonempty_string(item["claim_scope"]) or not isinstance(item["evidence_refs"], list) or not item["evidence_refs"]:
                    add_error(errors, f"{pid}/{polarity}: publication eligibility has empty scope/evidence")
                if polarity in {"unknown", "failure"} and (
                    item["runtime_witness_ceiling"] == "W2" or item["publication_eligibility"] != "INELIGIBLE"
                ):
                    add_error(errors, f"{pid}/{polarity}: unknown/failure is illegally publishable")
            true_item = eligibility.get("true", {})
            false_item = eligibility.get("false", {})
            if row["implementation_relation"] in {"EXACT", "IMPLEMENTATION_SUBSET"}:
                for polarity, item in (("true", true_item), ("false", false_item)):
                    if item.get("runtime_witness_ceiling") != "W2" or item.get("publication_eligibility") != "ELIGIBLE":
                        add_error(errors, f"{pid}/{polarity}: exact/subset relation requires W2-eligible terminal receipt")
            elif row["implementation_relation"] == "SOUND_TRUE_PROXY":
                if true_item.get("runtime_witness_ceiling") != "W2" or true_item.get("publication_eligibility") != "ELIGIBLE":
                    add_error(errors, f"{pid}/true: true proxy requires a W2-eligible terminal receipt")
                if false_item.get("runtime_witness_ceiling") == "W2" or false_item.get("publication_eligibility") != "INELIGIBLE":
                    add_error(errors, f"{pid}/false: true proxy may not publish a false terminal conclusion")
            elif row["implementation_relation"] == "SOUND_FALSE_PROXY":
                if false_item.get("runtime_witness_ceiling") != "W2" or false_item.get("publication_eligibility") != "ELIGIBLE":
                    add_error(errors, f"{pid}/false: false proxy requires a W2-eligible counterexample")
                if true_item.get("runtime_witness_ceiling") == "W2" or true_item.get("publication_eligibility") != "INELIGIBLE":
                    add_error(errors, f"{pid}/true: false proxy may not publish a true terminal conclusion")
            elif row["implementation_relation"] == "RESOLVED_CLAIM_EXCLUSION":
                for polarity, item in (("true", true_item), ("false", false_item)):
                    if item.get("publication_eligibility") != "INELIGIBLE":
                        add_error(errors, f"{pid}/{polarity}: claim exclusion must exclude both terminal polarities")
        impact = row["impact"]
        if not isinstance(impact, dict) or set(impact) != {"receipt_ids", "count"} or not isinstance(impact["count"], int) or impact["count"] < 0 or not isinstance(impact["receipt_ids"], list):
            add_error(errors, f"{pid}: impact object has invalid shape")
        elif (
            impact["count"] != len(impact["receipt_ids"])
            or any(not is_nonempty_string(receipt_id) for receipt_id in impact["receipt_ids"])
            or len(set(impact["receipt_ids"])) != len(impact["receipt_ids"])
        ):
            add_error(errors, f"{pid}: impact count or receipt identifier list is invalid")
    check_canonical_receipt_impacts(paper_root, rows, errors)


def check_canonical_receipt_impacts(
    paper_root: Path, rows: list[Any], errors: list[str]
) -> None:
    """Bind claim-exclusion receipt IDs to the immutable current raw archive."""

    raw_root = paper_root / CANONICAL_CURRENT_RAW
    if not raw_root.is_dir():
        add_error(errors, f"canonical current raw archive is missing: {CANONICAL_CURRENT_RAW}")
        return
    receipts: list[dict[str, Any]] = []
    incomplete_authority: dict[str, set[str]] = {}
    for raw_path in sorted(raw_root.glob("*/round-*.json")):
        try:
            payload = load_json(raw_path)
        except (OSError, json.JSONDecodeError) as exc:
            add_error(errors, f"cannot read canonical raw receipt file {raw_path}: {exc}")
            continue
        entries = payload.get("predicate_execution_receipts")
        evidence_records = payload.get("evidence_records")
        if not isinstance(entries, list):
            add_error(errors, f"canonical raw receipt file has no receipt array: {raw_path}")
            continue
        if not isinstance(evidence_records, list):
            add_error(errors, f"canonical raw receipt file has no evidence-record array: {raw_path}")
            continue
        evidence_by_obligation = {
            evidence.get("obligation_id"): evidence
            for evidence in evidence_records
            if isinstance(evidence, dict) and is_nonempty_string(evidence.get("obligation_id"))
        }
        for entry in entries:
            if not isinstance(entry, dict):
                add_error(errors, f"canonical raw receipt is not an object: {raw_path}")
                continue
            backend_result = entry.get("backend_result")
            receipt_id = backend_result.get("receipt_id") if isinstance(backend_result, dict) else None
            if not is_nonempty_string(receipt_id):
                add_error(errors, f"canonical raw receipt has no receipt ID: {raw_path}")
                continue
            receipts.append({
                "receipt_id": receipt_id,
                "predicate_id": entry.get("predicate_id"),
                "predicate_verdict": entry.get("predicate_verdict"),
                "witness_level": entry.get("witness_level"),
                "terminal_state": entry.get("terminal_state"),
                "execution_status": entry.get("execution_status"),
                "typed_inputs": entry.get("typed_inputs"),
                "artifact_attribution_complete": entry.get("artifact_attribution_complete"),
                "artifact_attribution": entry.get("artifact_attribution"),
            })
            # Historical raw receipts predate the current instance-authority
            # schema. Their publication-grade false findings must therefore
            # close through the same-payload evidence record, never through a
            # model hash alone.
            if entry.get("witness_level") == "W2" and entry.get("predicate_verdict") == "false":
                obligation_id = entry.get("obligation_id")
                evidence = evidence_by_obligation.get(obligation_id)
                execution_receipt = evidence.get("execution_receipt") if isinstance(evidence, dict) else None
                evidence_backend = execution_receipt.get("backend_result") if isinstance(execution_receipt, dict) else None
                matching_receipt = (
                    isinstance(evidence_backend, dict)
                    and evidence_backend.get("receipt_id") == receipt_id
                )
                binding = evidence.get("binding") if isinstance(evidence, dict) else None
                quote = evidence.get("requirement_quote") if isinstance(evidence, dict) else None
                source_refs = evidence.get("source_refs") if isinstance(evidence, dict) else None
                element_refs = binding.get("element_refs") if isinstance(binding, dict) else None
                authority_complete = (
                    matching_receipt
                    and is_nonempty_string(quote)
                    and isinstance(source_refs, list)
                    and bool(source_refs)
                    and all(is_nonempty_string(ref) for ref in source_refs)
                    and isinstance(binding, dict)
                    and binding.get("precise") is True
                    and isinstance(element_refs, list)
                    and bool(element_refs)
                    and all(is_nonempty_string(ref) for ref in element_refs)
                )
                if not authority_complete:
                    predicate_id = entry.get("predicate_id")
                    if not is_nonempty_string(predicate_id):
                        add_error(errors, f"{receipt_id}: historical W2 false receipt has no predicate ID")
                    else:
                        incomplete_authority.setdefault(predicate_id, set()).add(receipt_id)
    receipt_ids = [receipt["receipt_id"] for receipt in receipts]
    if len(receipt_ids) != len(set(receipt_ids)):
        add_error(errors, "canonical raw archive contains duplicate receipt IDs")
        return
    for receipt in receipts:
        if receipt["witness_level"] != "W2":
            continue
        attribution = receipt["artifact_attribution"]
        if (
            not isinstance(receipt["typed_inputs"], dict)
            or receipt["artifact_attribution_complete"] is not True
            or not isinstance(attribution, dict)
            or not {"requirement", "model", "plan", "receipt"} <= set(attribution)
        ):
            add_error(errors, f"{receipt['receipt_id']}: W2 receipt lacks typed binding or complete source attribution")
    for row in rows:
        if not isinstance(row, dict) or row.get("implementation_relation") != "RESOLVED_CLAIM_EXCLUSION":
            continue
        predicate_id = row.get("predicate_id")
        filters = IMPACT_RECEIPT_FILTERS.get(predicate_id)
        if filters is None:
            add_error(errors, f"{predicate_id}: claim exclusion has no audited canonical-receipt filter")
            continue
        expected = {
            receipt["receipt_id"]
            for receipt in receipts
            if receipt["predicate_id"] == predicate_id
            and receipt["witness_level"] == "W2"
            and receipt["terminal_state"] == "completed"
            and receipt["execution_status"] == "executed"
            and all(receipt.get(field) in values for field, values in filters.items())
        }
        actual = set(row.get("impact", {}).get("receipt_ids", []))
        if actual != expected:
            add_error(
                errors,
                f"{predicate_id}: canonical claim-exclusion receipt IDs differ: "
                f"missing={sorted(expected - actual)}, extra={sorted(actual - expected)}",
            )
    catalog = load_json(paper_root / "related_work/provenance/current_source_catalog.json")
    audit = catalog.get("r1_citation_audit") if isinstance(catalog, dict) else None
    authority_audit = audit.get("historical_source_authority_exclusion") if isinstance(audit, dict) else None
    required_authority_keys = {
        "audit_basis", "runtime_effect", "publication_rule", "eligible_false_w2_count",
        "excluded_false_w2_count", "excluded_by_predicate",
    }
    if not isinstance(authority_audit, dict) or set(authority_audit) != required_authority_keys:
        add_error(errors, "catalog lacks exact historical source-authority exclusion metadata")
        return
    groups = authority_audit.get("excluded_by_predicate")
    expected_incomplete: dict[str, set[str]] = {}
    if not isinstance(groups, list):
        add_error(errors, "historical source-authority exclusions are not an array")
    else:
        for group in groups:
            if not isinstance(group, dict) or set(group) != {"predicate_id", "receipt_ids", "count"}:
                add_error(errors, "historical source-authority exclusion has invalid shape")
                continue
            predicate_id = group.get("predicate_id")
            receipt_ids = group.get("receipt_ids")
            if (
                not is_nonempty_string(predicate_id)
                or not isinstance(receipt_ids, list)
                or group.get("count") != len(receipt_ids)
                or not receipt_ids
                or len(set(receipt_ids)) != len(receipt_ids)
                or any(not is_nonempty_string(receipt_id) for receipt_id in receipt_ids)
            ):
                add_error(errors, "historical source-authority exclusion has invalid IDs/count")
                continue
            expected_incomplete[predicate_id] = set(receipt_ids)
    if expected_incomplete != incomplete_authority:
        add_error(
            errors,
            "historical source-authority exclusions differ from raw evidence records: "
            f"expected={sorted((key, sorted(value)) for key, value in expected_incomplete.items())}, "
            f"actual={sorted((key, sorted(value)) for key, value in incomplete_authority.items())}",
        )
    excluded_count = sum(len(receipt_ids) for receipt_ids in expected_incomplete.values())
    false_w2_count = sum(
        receipt["witness_level"] == "W2" and receipt["predicate_verdict"] == "false"
        for receipt in receipts
    )
    if (
        authority_audit.get("excluded_false_w2_count") != excluded_count
        or not isinstance(authority_audit.get("eligible_false_w2_count"), int)
        or authority_audit["eligible_false_w2_count"] + excluded_count != false_w2_count
    ):
        add_error(errors, "historical source-authority totals do not close over false W2 receipts")


def frozen_predicate_semantics(paper_root: Path, errors: list[str]) -> dict[str, str]:
    """Load the immutable registry only to verify the human audit quotes it exactly."""

    registry_path = paper_root / "method/src/paper_stm_method/resources/predicate_registry.json"
    try:
        registry = load_json(registry_path)
    except (OSError, json.JSONDecodeError) as exc:
        add_error(errors, f"cannot read frozen predicate registry: {exc}")
        return {}
    semantics: dict[str, str] = {}
    for family in registry.get("families", []):
        if not isinstance(family, dict):
            continue
        for predicate in family.get("predicates", []):
            if not isinstance(predicate, dict):
                continue
            predicate_id = predicate.get("id")
            proposition = predicate.get("semantics")
            if isinstance(predicate_id, str) and is_nonempty_string(proposition):
                semantics[predicate_id] = proposition
    if set(semantics) != CURRENT:
        add_error(errors, "frozen predicate registry keyset is not exact")
    return semantics


def check_crosswalk(paper_root: Path, errors: list[str]) -> None:
    path = paper_root / "related_work/provenance/predicate_provenance.md"
    text = path.read_text(encoding="utf-8")
    found = re.search(r"## 双向 legacy/current crosswalk\n\n(?P<table>\| legacy ID.*?)(?=\n\n上表覆盖)", text, re.DOTALL)
    if not found:
        add_error(errors, "predicate provenance has no parseable legacy/current crosswalk")
        return
    legacy_seen: set[str] = set()
    current_seen: set[str] = set()
    mapping = {"direct_reuse", "split", "merge_derived", "method_owned_comparison"}
    terminal = {"newly_added", "retired", "not_carried", "not_a_predicate"}
    for line in found.group("table").splitlines()[2:]:
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) != 5:
            add_error(errors, f"malformed crosswalk row: {line}")
            continue
        legacy_ids = set(re.findall(r"`([a-z_]+)`", cells[0]))
        current_ids = set(PREDICATE_ID.findall(cells[1]))
        relation = cells[2].strip("`")
        rationale = cells[3]
        evidence = cells[4]
        if not rationale or not re.search(r"承接|当前|未|不", rationale):
            add_error(errors, f"crosswalk row lacks a semantic-delta rationale: {line}")
        if not re.search(r"(?:ST|TP|TR|BV|G4-RP)\d|source-unit", evidence) or not re.search(
            r"[0-9a-f]{7,40}|`[^`]+(?:\.md|\.json|\.py)`", evidence
        ):
            add_error(errors, f"crosswalk row lacks source-unit and commit/path evidence: {line}")
        if relation in mapping:
            if not legacy_ids or not current_ids:
                add_error(errors, f"mapping edge must have both endpoint sets: {line}")
        elif relation in terminal:
            if bool(legacy_ids) == bool(current_ids):
                add_error(errors, f"terminal disposition must have exactly one endpoint: {line}")
        else:
            add_error(errors, f"invalid crosswalk relation {relation!r}")
        if not legacy_ids <= LEGACY or not current_ids <= CURRENT:
            add_error(errors, f"crosswalk has unknown predicate key: {line}")
        legacy_seen |= legacy_ids
        current_seen |= current_ids
    if legacy_seen != LEGACY:
        add_error(errors, f"predicate crosswalk legacy keyset is not exact: {sorted(legacy_seen ^ LEGACY)}")
    if current_seen != CURRENT:
        add_error(errors, f"predicate crosswalk current keyset is not exact: {sorted(current_seen ^ CURRENT)}")

    sections = re.findall(r"^### ([SGRV]\d) `[^`]+`\n(?P<body>.*?)(?=^### |^## |\Z)", text, re.MULTILINE | re.DOTALL)
    section_ids = {pid for pid, _ in sections}
    if section_ids != CURRENT or len(sections) != len(CURRENT):
        add_error(errors, f"predicate provenance sections are not exact: {sorted(section_ids ^ CURRENT)}")
    semantics = frozen_predicate_semantics(paper_root, errors)
    for pid, body in sections:
        for label in REQUIRED_HUMAN_AUDIT_FIELDS:
            if label not in body:
                add_error(errors, f"{pid}: human audit lacks {label}")
        if not re.search(r"\[.*?\^[-A-Za-z0-9_]+", body):
            add_error(errors, f"{pid}: human audit has no source citation")
        proposition = semantics.get(pid)
        if proposition and proposition not in body:
            add_error(errors, f"{pid}: human audit does not reproduce the frozen registry proposition exactly")
        if "一手全文定位。" not in body or "#quote-" not in body:
            add_error(errors, f"{pid}: human audit lacks a predicate-level primary-text quote anchor")
        if "全文逐字" not in body or "chronology/leakage" not in body:
            add_error(errors, f"{pid}: human audit lacks full-text quotation or chronology/leakage field")


def check_experiment_gate(paper_root: Path, errors: list[str]) -> set[str]:
    data = load_json(paper_root / "story/experiment_dependent_gates.json")
    schema = load_json(paper_root / "story/experiment_dependent_gates.schema.json")
    try:
        jsonschema.Draft202012Validator(schema).validate(data)
    except jsonschema.ValidationError as exc:
        add_error(errors, f"experiment gate schema validation failed: {exc.message}")
        return set()
    if data.get("schema_version") != schema.get("schema_version"):
        add_error(errors, "experiment gate schema/data version mismatch")
    records = data.get("records", [])
    ids = [row.get("id") for row in records if isinstance(row, dict)]
    if len(ids) != len(set(ids)):
        add_error(errors, "experiment gate IDs are not unique")
    claims = (paper_root / "story/claim_evidence_map.md").read_text(encoding="utf-8")
    outline = (paper_root / "story/paper_outline.md").read_text(encoding="utf-8")
    for record in records:
        if not isinstance(record, dict):
            continue
        rid = record["id"]
        if record["blocks_r1_ready"]:
            add_error(errors, f"{rid}: blocks_r1_ready must be false for R1 READY")
        for claim in record["affected_claims"]:
            if claim not in claims:
                add_error(errors, f"{rid}: affected claim is not closed in claim map: {claim}")
        for rq in record["affected_rqs"]:
            if rq not in outline:
                add_error(errors, f"{rid}: affected RQ is not closed in outline: {rq}")
        for anchor in record["outline_locations"]:
            if f'id="{anchor}"' not in outline:
                add_error(errors, f"{rid}: outline location is not an anchor: {anchor}")
    return {entry for entry in ids if isinstance(entry, str)}


def check_experiment_mentions(paper_root: Path, valid_ids: set[str], errors: list[str]) -> None:
    outline = paper_root / "story/paper_outline.md"
    for path in (
        outline,
        paper_root / "story/paper_story.md",
        paper_root / "story/claim_evidence_map.md",
    ):
        present = set(EXPERIMENT_ID.findall(path.read_text(encoding="utf-8")))
        unknown = present - valid_ids
        if unknown:
            add_error(errors, f"{path.name}: unknown TODO-EXPERIMENT IDs {sorted(unknown)}")
    outline_text = outline.read_text(encoding="utf-8")
    for experiment_id in valid_ids:
        if experiment_id not in outline_text:
            add_error(errors, f"{experiment_id}: experiment record is not cited by the canonical outline")


def check_inventory(paper_root: Path, errors: list[str]) -> None:
    text = (paper_root / "story/paper_result_inventory.md").read_text(encoding="utf-8")
    dispositions = set(re.findall(r"`(included_in_main|included_in_appendix|excluded_with_reason)`", text))
    if dispositions != {"included_in_main", "included_in_appendix", "excluded_with_reason"}:
        add_error(errors, "paper result inventory lacks all three dispositions")
    rows = [line for line in text.splitlines() if line.startswith("|")][2:]
    if len(rows) < 8:
        add_error(errors, "paper result inventory does not dispose required metric groups")
    for row in rows:
        if not re.search(r"`(included_in_main|included_in_appendix|excluded_with_reason)`", row):
            add_error(errors, f"paper result inventory row has no disposition: {row}")
    missing = [marker for marker in REQUIRED_INVENTORY_MARKERS if marker not in text]
    if missing:
        add_error(errors, f"paper result inventory is missing required metric groups: {missing}")


def repository_relative_paper_path(paper_root: Path) -> str:
    repository_root = Path(subprocess.check_output(
        ["git", "-C", str(paper_root), "rev-parse", "--show-toplevel"], text=True
    ).strip()).resolve()
    return paper_root.resolve().relative_to(repository_root).as_posix()


def parse_git_changed_paths(paper_root: Path, base: str) -> set[str]:
    output = subprocess.check_output(
        ["git", "-C", str(paper_root), "diff", "--name-only", f"{base}..HEAD"], text=True
    )
    prefix = repository_relative_paper_path(paper_root).rstrip("/") + "/"
    return {
        line[len(prefix):]
        for line in output.splitlines()
        if line.startswith(prefix) and line[len(prefix):]
    }


def check_static_surface(
    paper_root: Path, errors: list[str], *, base_commit: str = BASE_COMMIT
) -> dict[str, str]:
    paths = set(REQUIRED_STATIC_PATHS)
    try:
        paths |= parse_git_changed_paths(paper_root, base_commit)
    except subprocess.CalledProcessError as exc:
        add_error(errors, f"unable to enumerate R1 changed paths: {exc}")
    raw_root = paper_root / CANONICAL_CURRENT_RAW
    if not raw_root.is_dir():
        add_error(errors, f"canonical current raw archive is missing: {CANONICAL_CURRENT_RAW}")
    else:
        paths |= {
            raw_path.relative_to(paper_root).as_posix()
            for raw_path in raw_root.glob("*/round-*.json")
            if raw_path.is_file()
        }
    path_hashes: dict[str, str] = {}
    for rel in sorted(paths):
        path = paper_root / rel
        if not path.is_file():
            add_error(errors, f"missing required current-facing path: {rel}")
            continue
        path_hashes[rel] = sha256_path(path)
        if rel.endswith((".md", ".json")) and BLOCKED.search(path.read_text(encoding="utf-8")):
            add_error(errors, f"{rel}: blocked residual marker")
    check_catalog(paper_root, errors)
    check_crosswalk(paper_root, errors)
    for citation_path in (
        paper_root / "story/paper_outline.md",
        paper_root / "related_work/provenance/predicate_provenance.md",
    ):
        check_footnotes(citation_path, errors)
    check_terminology(paper_root, errors)
    experiment_ids = check_experiment_gate(paper_root, errors)
    check_experiment_mentions(paper_root, experiment_ids, errors)
    check_inventory(paper_root, errors)
    return path_hashes


def check_blind_payload(bundle: dict[str, Any], errors: list[str]) -> set[str]:
    packet = bundle.get("blind_packet")
    record = bundle.get("blind_search_record")
    if not isinstance(packet, dict) or not isinstance(record, dict):
        add_error(errors, "review bundle lacks complete blind packet/raw record payloads")
        return set()
    expected_packet = {
        "schema_version", "task_inclusion_fields", "cutoff", "databases", "search_protocol",
        "comparison_only_fields", "withheld_fields",
    }
    inclusion = {
        "free_form_nl_input", "pre_existing_fixed_stm_input",
        "localized_requirement_relevant_issues", "implemented_and_evaluated_on_stm",
    }
    comparison = {"source_attribution", "native_stm_semantics", "replay_receipt"}
    withheld = {"candidate_claim", "paper_conclusion", "closest_work_matrix", "goal_prompt", "author_disposition"}
    if set(packet) != expected_packet or packet.get("schema_version") != BLIND_PACKET_SCHEMA_VERSION:
        add_error(errors, "blind packet has invalid exact allowlist/schema version")
    if not isinstance(packet.get("task_inclusion_fields"), dict) or set(packet["task_inclusion_fields"]) != inclusion:
        add_error(errors, "blind packet inclusion field keyset is not exact")
    if not isinstance(packet.get("comparison_only_fields"), dict) or set(packet["comparison_only_fields"]) != comparison:
        add_error(errors, "blind packet comparison-only field keyset is not exact")
    if set(packet.get("withheld_fields", [])) != withheld or len(packet.get("withheld_fields", [])) != len(withheld):
        add_error(errors, "blind packet withheld denylist is not exact")
    if packet.get("cutoff") != "2026-09-02" or not isinstance(packet.get("databases"), list) or not packet["databases"] or not is_nonempty_string(packet.get("search_protocol")):
        add_error(errors, "blind packet cutoff/search protocol/databases are incomplete")
    if bundle.get("blind_packet_jcs_sha256") != jcs_sha256(packet):
        add_error(errors, "blind packet JCS SHA-256 mismatch")

    expected_record = {
        "schema_version", "base_commit", "reviewer_identity", "blind_packet_sha256",
        "queries", "search_trace", "raw_candidates", "raw_findings",
    }
    if set(record) != expected_record or record.get("schema_version") != BLIND_RECORD_SCHEMA_VERSION:
        add_error(errors, "blind raw record has invalid exact allowlist/schema version")
    if not is_nonempty_string(record.get("base_commit")) or not is_nonempty_string(record.get("reviewer_identity")):
        add_error(errors, "blind raw record lacks base commit/reviewer identity")
    if record.get("blind_packet_sha256") != bundle.get("blind_packet_jcs_sha256"):
        add_error(errors, "blind raw record does not bind the blind packet hash")
    for field in ("queries", "search_trace", "raw_candidates", "raw_findings"):
        if not isinstance(record.get(field), list) or not record[field]:
            add_error(errors, f"blind raw record {field} must be a nonempty array")
    raw_ids: set[str] = set()
    for candidate in record.get("raw_candidates", []):
        expected_candidate = {"candidate_id", *inclusion}
        if not isinstance(candidate, dict) or set(candidate) != expected_candidate:
            add_error(errors, "blind raw candidate lacks stable ID/four-field judgment")
            continue
        candidate_id = candidate["candidate_id"]
        if not is_nonempty_string(candidate_id) or candidate_id in raw_ids:
            add_error(errors, "blind raw candidate IDs are missing or duplicate")
        raw_ids.add(candidate_id)
        if any(not isinstance(candidate[field], bool) for field in inclusion):
            add_error(errors, f"blind raw candidate {candidate_id!r} has non-Boolean inclusion judgment")
    if bundle.get("blind_search_record_jcs_sha256") != jcs_sha256(record):
        add_error(errors, "blind raw record JCS SHA-256 mismatch")
    return raw_ids


def check_pr_snapshot(name: str, snapshot: Any, errors: list[str], live_bodies: dict[str, str] | None) -> None:
    expected = {"repo", "number", "url", "fetched_at", "body", "body_sha256"}
    if not isinstance(snapshot, dict) or set(snapshot) != expected:
        add_error(errors, f"{name} PR snapshot has invalid shape")
        return
    if snapshot["repo"] != REPO or snapshot["number"] != PR_NUMBERS[name] or not is_nonempty_string(snapshot["url"]) or not is_nonempty_string(snapshot["fetched_at"]):
        add_error(errors, f"{name} PR snapshot has wrong repository/number/metadata")
    if not isinstance(snapshot["body"], str) or snapshot["body_sha256"] != sha256_bytes(snapshot["body"].encode("utf-8")):
        add_error(errors, f"{name} PR snapshot body hash mismatch")
    if live_bodies is not None:
        live = live_bodies.get(name)
        if not isinstance(live, str) or live != snapshot.get("body"):
            add_error(errors, f"{name} PR live body differs from final snapshot")


def github_bodies() -> dict[str, str]:
    bodies: dict[str, str] = {}
    for name, number in PR_NUMBERS.items():
        raw = subprocess.check_output(
            ["gh", "api", f"repos/{REPO}/pulls/{number}"], text=True, stderr=subprocess.STDOUT
        )
        body = json.loads(raw).get("body")
        if not isinstance(body, str):
            raise ValueError(f"PR #{number} body is missing or not a string")
        bodies[name] = body
    return bodies


def review_input_hash(reviewed_paths: list[str], path_hashes: dict[str, str]) -> str | None:
    if len(reviewed_paths) != len(set(reviewed_paths)) or any(
        not isinstance(path, str) or path not in path_hashes for path in reviewed_paths
    ):
        return None
    return jcs_sha256({path: path_hashes[path] for path in sorted(reviewed_paths)})


def check_review_bundle(
    paper_root: Path,
    review_path: Path | None,
    static_hashes: dict[str, str],
    errors: list[str],
    *,
    base_commit: str = BASE_COMMIT,
    live_bodies: dict[str, str] | None = None,
    task_start_body_hashes: dict[str, str] = TASK_START_BODY_SHA256,
    permitted_final_body_hashes: dict[str, str] = PERMITTED_FINAL_BODY_SHA256,
) -> None:
    if review_path is None or not review_path.is_file():
        add_error(errors, "missing external final review evidence")
        return
    bundle = load_json(review_path)
    expected = {
        "schema_version", "head", "base_commit", "results", "path_hashes", "pr_initial_snapshots",
        "pr_final_snapshots", "blind_packet", "blind_packet_jcs_sha256", "blind_search_record",
        "blind_search_record_jcs_sha256", "blind_candidate_keyset", "final_dispositions",
        "later_discovered_candidates", "final_disposition_keyset", "union_proof", "experiment_reviews",
    }
    if not isinstance(bundle, dict) or set(bundle) != expected or bundle.get("schema_version") != BUNDLE_SCHEMA_VERSION:
        add_error(errors, "review bundle has invalid exact schema")
        return
    head = subprocess.check_output(["git", "-C", str(paper_root), "rev-parse", "HEAD"], text=True).strip()
    if bundle["head"] != head:
        add_error(errors, "review bundle HEAD is stale")
    if bundle["base_commit"] != base_commit:
        add_error(errors, f"review bundle base commit is not {base_commit}")

    path_hashes = bundle["path_hashes"]
    if not isinstance(path_hashes, dict):
        add_error(errors, "review bundle path_hashes is not an object")
    else:
        if set(path_hashes) != set(static_hashes):
            missing = sorted(set(static_hashes) - set(path_hashes))
            extra = sorted(set(path_hashes) - set(static_hashes))
            add_error(errors, f"review bundle path coverage is not exact: missing={missing}, extra={extra}")
        for rel, digest in static_hashes.items():
            supplied = path_hashes.get(rel)
            if not isinstance(supplied, str) or not re.fullmatch(r"[0-9a-f]{64}", supplied) or supplied != digest:
                add_error(errors, f"review bundle has stale/missing path hash: {rel}")

    results = bundle["results"]
    if not isinstance(results, list):
        add_error(errors, "review bundle results is not an array")
    else:
        roles = [item.get("role") for item in results if isinstance(item, dict)]
        if set(roles) != REQUIRED_ROLES or len(roles) != len(REQUIRED_ROLES):
            add_error(errors, "review bundle role set is not exact")
        reviewed_union: set[str] = set()
        for result in results:
            expected_result = {"role", "reviewer_identity", "status", "critical", "important", "input_hash", "reviewed_paths", "findings"}
            if not isinstance(result, dict) or set(result) != expected_result:
                add_error(errors, "review bundle result has invalid shape")
                continue
            if result["status"] != "PASS" or result["critical"] != 0 or result["important"] != 0:
                add_error(errors, f"review role is not a clean PASS: {result['role']}")
            if not is_nonempty_string(result["reviewer_identity"]) or not isinstance(result["input_hash"], str):
                add_error(errors, f"review role lacks identity/input hash: {result['role']}")
            reviewed_paths = result["reviewed_paths"]
            if not isinstance(reviewed_paths, list) or not reviewed_paths or not isinstance(result["findings"], list):
                add_error(errors, f"review role lacks paths/findings: {result['role']}")
                continue
            expected_input = review_input_hash(reviewed_paths, static_hashes)
            if expected_input is None or result["input_hash"] != expected_input:
                add_error(errors, f"review role has stale/invalid input hash: {result['role']}")
            role = result["role"]
            reviewed_set = set(reviewed_paths)
            reviewed_union |= reviewed_set
            required_paths = ROLE_REQUIRED_PATHS.get(role, set())
            if not required_paths <= reviewed_set:
                add_error(errors, f"review role lacks required path coverage: {role}")
            if role == "fact_link_test" and not set(static_hashes) <= reviewed_set:
                add_error(errors, "fact/link/test reviewer must cover every static payload")
            if role == "method_soundness":
                raw_paths = {
                    path for path in static_hashes
                    if path.startswith(CANONICAL_CURRENT_RAW + "/")
                }
                if not raw_paths <= reviewed_set:
                    add_error(errors, "method/soundness reviewer must cover every consumed raw receipt payload")
            if role == "predicate_evidence":
                expected_finding = {"predicate_id", "status", "evidence"}
                if any(
                    not isinstance(finding, dict) or set(finding) != expected_finding
                    or finding.get("status") != "PASS"
                    or not is_nonempty_string(finding.get("predicate_id"))
                    or not is_nonempty_string(finding.get("evidence"))
                    for finding in result["findings"]
                ):
                    add_error(errors, "predicate evidence findings have invalid shape/status")
            elif any(
                not isinstance(finding, dict)
                or set(finding) != {"finding_id", "disposition", "evidence"}
                or finding.get("disposition") not in {"accepted", "rejected", "fixed"}
                or not is_nonempty_string(finding.get("finding_id"))
                or not is_nonempty_string(finding.get("evidence"))
                for finding in result["findings"]
            ):
                add_error(errors, f"review findings have invalid disposition shape: {role}")
        if not set(static_hashes) <= reviewed_union:
            add_error(errors, "review roles do not collectively cover every hashed path")
        predicate = next((item for item in results if isinstance(item, dict) and item.get("role") == "predicate_evidence"), None)
        if not isinstance(predicate, dict) or len(predicate.get("findings", [])) != 19:
            add_error(errors, "predicate evidence review must contain exactly 19 predicate dispositions")
        elif {item.get("predicate_id") for item in predicate["findings"] if isinstance(item, dict)} != CURRENT:
            add_error(errors, "predicate evidence review does not cover exact current keyset")

    blind_ids = check_blind_payload(bundle, errors)
    claimed_blind = bundle["blind_candidate_keyset"]
    final_ids = bundle["final_disposition_keyset"]
    dispositions = bundle["final_dispositions"]
    later = bundle["later_discovered_candidates"]
    if not isinstance(claimed_blind, list) or set(claimed_blind) != blind_ids or len(claimed_blind) != len(blind_ids):
        add_error(errors, "self-reported blind keyset does not equal raw candidate derivation")
    if not isinstance(dispositions, list) or not isinstance(final_ids, list):
        add_error(errors, "final candidate dispositions/keyset have invalid shape")
    else:
        disposition_ids = {item.get("candidate_id") for item in dispositions if isinstance(item, dict)}
        valid = {"candidate_id", "disposition", "evidence"}
        if any(not isinstance(item, dict) or set(item) != valid or item.get("disposition") not in {"accepted", "rejected"} or not is_nonempty_string(item.get("evidence")) for item in dispositions):
            add_error(errors, "final candidate disposition is incomplete")
        if set(final_ids) != disposition_ids or len(final_ids) != len(disposition_ids):
            add_error(errors, "final disposition keyset does not equal disposition objects")
        if not blind_ids <= disposition_ids:
            add_error(errors, "a blind candidate lacks a final disposition")
    later_ids: set[str] = set()
    if not isinstance(later, list):
        add_error(errors, "later-discovered candidates is not an array")
    else:
        expected_later = {"candidate_id", "discovery_phase", "query_or_citation_provenance", "discovered_at"}
        for item in later:
            if not isinstance(item, dict) or set(item) != expected_later or item.get("discovery_phase") not in {"unblind_fulltext", "snowballing", "review_challenge"} or not all(is_nonempty_string(item.get(key)) for key in expected_later):
                add_error(errors, "later-discovered candidate lacks required provenance")
                continue
            later_ids.add(item["candidate_id"])
        if later_ids & blind_ids:
            add_error(errors, "later-discovered candidate reuses blind candidate ID")
    if set(final_ids) != blind_ids | later_ids:
        add_error(errors, "final disposition set is not blind/later candidate union")
    if bundle["union_proof"] != {"blind_plus_later_equals_final": True}:
        add_error(errors, "review bundle lacks explicit candidate-union proof")

    experiment = bundle["experiment_reviews"]
    records = {item["id"]: item for item in load_json(paper_root / "story/experiment_dependent_gates.json").get("records", []) if isinstance(item, dict)}
    if not isinstance(experiment, list) or {item.get("id") for item in experiment if isinstance(item, dict)} != set(records):
        add_error(errors, "experiment review IDs do not exactly match experiment gate records")
    else:
        for item in experiment:
            if not isinstance(item, dict) or set(item) != {"id", "jcs_sha256", "status", "qualification"} or item["status"] != "PASS" or not is_nonempty_string(item["qualification"]):
                add_error(errors, "experiment review is incomplete")
            elif item["jcs_sha256"] != jcs_sha256(records[item["id"]]):
                add_error(errors, f"experiment review JCS hash is stale: {item['id']}")

    snapshots = bundle["pr_final_snapshots"]
    initial = bundle["pr_initial_snapshots"]
    if not isinstance(snapshots, dict) or set(snapshots) != set(PR_NUMBERS) or not isinstance(initial, dict) or set(initial) != set(PR_NUMBERS):
        add_error(errors, "review bundle PR snapshots are incomplete")
    else:
        for name in PR_NUMBERS:
            check_pr_snapshot(name, initial[name], errors, None)
            check_pr_snapshot(name, snapshots[name], errors, live_bodies)
        for name in PR_NUMBERS:
            if initial[name].get("body_sha256") != task_start_body_hashes.get(name):
                add_error(errors, f"{name} PR task-start body snapshot differs from the anchored body")
            if snapshots[name].get("body_sha256") != permitted_final_body_hashes.get(name):
                add_error(errors, f"{name} PR final body is outside the permitted R1 contract edit")


def run(
    paper_root: Path,
    review_evidence: Path | None,
    *,
    base_commit: str = BASE_COMMIT,
    github_body_loader: Any = github_bodies,
    task_start_body_hashes: dict[str, str] = TASK_START_BODY_SHA256,
    permitted_final_body_hashes: dict[str, str] = PERMITTED_FINAL_BODY_SHA256,
) -> dict[str, Any]:
    errors: list[str] = []
    hashes = check_static_surface(paper_root, errors, base_commit=base_commit)
    live_bodies: dict[str, str] | None = None
    if review_evidence is not None and review_evidence.is_file():
        try:
            live_bodies = github_body_loader()
        except Exception as exc:  # API/network/auth failures are fail-closed.
            add_error(errors, f"unable to retrieve live GitHub PR bodies: {exc}")
    check_review_bundle(
        paper_root, review_evidence, hashes, errors,
        base_commit=base_commit, live_bodies=live_bodies,
        task_start_body_hashes=task_start_body_hashes,
        permitted_final_body_hashes=permitted_final_body_hashes,
    )
    return {
        "ready": not errors,
        "head": subprocess.check_output(["git", "-C", str(paper_root), "rev-parse", "HEAD"], text=True).strip(),
        "current_keyset": sorted(CURRENT),
        "legacy_keyset": sorted(LEGACY),
        "unresolved": sum("unresolved" in item.lower() for item in errors),
        "stale_review": sum("stale" in item.lower() or "missing external" in item.lower() for item in errors),
        "citation_errors": sum("footnote" in item.lower() or "citation" in item.lower() for item in errors),
        "language_errors": sum("terminology" in item.lower() for item in errors),
        "experiment_gate_errors": sum("experiment" in item.lower() for item in errors),
        "errors": errors,
    }


def self_test() -> int:
    """Run isolated positive and negative fixtures without GitHub or providers."""

    source_paper = Path(__file__).resolve().parents[3]

    def git(repository: Path, *args: str) -> str:
        return subprocess.check_output(["git", "-C", str(repository), *args], text=True).strip()

    def run_git(repository: Path, *args: str) -> None:
        subprocess.run(
            ["git", "-C", str(repository), *args], check=True,
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )

    def experiment_record() -> dict[str, Any]:
        return {
            "id": "TODO-EXPERIMENT-01",
            "necessity_proof": {
                "literature": "No prior paper can estimate this controlled adapter effect.",
                "logic": "The claim compares two executions, so it requires observations.",
                "code_audit": "The current code has no paired adapter condition.",
                "existing_artifacts": "The frozen archive contains only the existing condition.",
            },
            "hypothesis": "A declared second adapter changes the observed reporting behavior.",
            "object": "A separately implemented state-machine-language adapter.",
            "control": "The existing PlantUML adapter under the frozen protocol.",
            "unit": "A source-requirement input pair.",
            "denominator": "All eligible input pairs under the preregistered protocol.",
            "metric": "FULL hit@1 and report validity precision.",
            "affected_claims": ["CLM-C1"],
            "affected_rqs": ["RQ1"],
            "outline_locations": ["outline-9"],
            "forbidden_pre_experiment_claims": ["No cross-language empirical effect is claimed before the experiment."],
            "temporary_writable_conclusion": "The current PlantUML case study does not estimate another adapter's effect.",
            "blocks_r1_ready": False,
            "blocks_paper_submission": True,
        }

    def write_impact_archive_fixture(paper: Path) -> None:
        catalog = load_json(paper / "related_work/provenance/current_source_catalog.json")
        entries: list[dict[str, Any]] = []
        evidence_records: list[dict[str, Any]] = []
        v4_true_receipts = {
            "0033:r2:i9:receipt", "0033:r2:i10:receipt", "0033:r2:i11:receipt",
            "0033:r3:i9:receipt", "0033:r3:i10:receipt", "0033:r3:i11:receipt",
        }

        def append_false_w2(
            predicate_id: str, receipt_id: str, *, authority_complete: bool
        ) -> None:
            obligation_id = receipt_id.removesuffix(":receipt")
            entries.append({
                "predicate_id": predicate_id,
                "obligation_id": obligation_id,
                "predicate_verdict": "false",
                "witness_level": "W2",
                "terminal_state": "completed",
                "execution_status": "executed",
                "backend_result": {"receipt_id": receipt_id},
                "typed_inputs": {"predicate_id": predicate_id},
                "artifact_attribution_complete": True,
                "artifact_attribution": {
                    "requirement": {}, "model": {}, "plan": {}, "receipt": {},
                },
            })
            evidence_records.append({
                "obligation_id": obligation_id,
                "requirement_quote": "Fixture requirement.",
                "source_refs": ["fixture:nl:1"] if authority_complete else [],
                "binding": {
                    "precise": authority_complete,
                    "element_refs": ["fixture:state:1"] if authority_complete else [],
                },
                "execution_receipt": {"backend_result": {"receipt_id": receipt_id}},
            })

        for audit in catalog["r1_citation_audit"]["predicate_audits"]:
            predicate_id = audit["predicate_id"]
            if predicate_id not in IMPACT_RECEIPT_FILTERS:
                continue
            for receipt_id in audit["impact"]["receipt_ids"]:
                if receipt_id in v4_true_receipts:
                    entries.append({
                        "predicate_id": predicate_id,
                        "obligation_id": receipt_id.removesuffix(":receipt"),
                        "predicate_verdict": "true",
                        "witness_level": "W2",
                        "terminal_state": "completed",
                        "execution_status": "executed",
                        "backend_result": {"receipt_id": receipt_id},
                        "typed_inputs": {"predicate_id": predicate_id},
                        "artifact_attribution_complete": True,
                        "artifact_attribution": {
                            "requirement": {}, "model": {}, "plan": {}, "receipt": {},
                        },
                    })
                else:
                    append_false_w2(predicate_id, receipt_id, authority_complete=True)
        for group in catalog["r1_citation_audit"]["historical_source_authority_exclusion"]["excluded_by_predicate"]:
            for receipt_id in group["receipt_ids"]:
                append_false_w2(group["predicate_id"], receipt_id, authority_complete=False)
        # The isolated fixture keeps the same 627-false-W2 arithmetic as the
        # real archive: 125 excluded historical records and 502 complete ones.
        # Eighty-four complete records are already present as G2/V4 impacts.
        for index in range(418):
            append_false_w2(
                "S1", f"fixture:eligible:{index}:receipt", authority_complete=True
            )
        if {entry["backend_result"]["receipt_id"] for entry in entries if entry["predicate_id"] == "G2"} != {
            "0020:r3:i1:receipt", "0020:r3:i5:receipt",
        }:
            raise AssertionError("fixture requires the complete G2 claim-exclusion receipt set")
        raw_path = paper / CANONICAL_CURRENT_RAW / "fixture" / "round-3.json"
        raw_path.parent.mkdir(parents=True, exist_ok=True)
        raw_path.write_text(
            json.dumps({
                "predicate_execution_receipts": entries,
                "evidence_records": evidence_records,
            }, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    def prepare_fixture(with_experiment: bool = False) -> tuple[tempfile.TemporaryDirectory[str], Path, str]:
        temporary = tempfile.TemporaryDirectory(prefix="paper1-r1-readiness-")
        repository = Path(temporary.name) / "repository"
        paper = repository / "paper"
        paper.mkdir(parents=True)
        for relative in REQUIRED_STATIC_PATHS:
            source = source_paper / relative
            target = paper / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
        write_impact_archive_fixture(paper)
        if with_experiment:
            gate = paper / "story/experiment_dependent_gates.json"
            gate.write_text(json.dumps({
                "schema_version": "paper1.experiment-dependent-gates.v1",
                "records": [experiment_record()],
            }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            outline = paper / "story/paper_outline.md"
            outline.write_text(
                outline.read_text(encoding="utf-8")
                + "\n\n<a id=\"outline-self-test-experiment\"></a>\n"
                + "本隔离 fixture 引用 `TODO-EXPERIMENT-01`，仅用于检查实验合同闭合。\n",
                encoding="utf-8",
            )
        run_git(repository, "init", "-q")
        run_git(repository, "config", "user.email", "readiness@example.invalid")
        run_git(repository, "config", "user.name", "R1 readiness self-test")
        run_git(repository, "add", ".")
        run_git(repository, "commit", "-qm", "fixture base")
        base = git(repository, "rev-parse", "HEAD")
        readme = paper / "README.md"
        readme.write_text(readme.read_text(encoding="utf-8") + "\n", encoding="utf-8")
        run_git(repository, "add", "paper/README.md")
        run_git(repository, "commit", "-qm", "fixture review surface")
        return temporary, paper, base

    def snapshot(number: int, body: str) -> dict[str, Any]:
        return {
            "repo": REPO,
            "number": number,
            "url": f"https://github.com/{REPO}/pull/{number}",
            "fetched_at": "2026-09-02T00:00:00+08:00",
            "body": body,
            "body_sha256": sha256_bytes(body.encode("utf-8")),
        }

    def build_bundle(paper: Path, base: str) -> dict[str, Any]:
        errors: list[str] = []
        hashes = check_static_surface(paper, errors, base_commit=base)
        assert not errors, errors
        packet = {
            "schema_version": BLIND_PACKET_SCHEMA_VERSION,
            "task_inclusion_fields": {
                "free_form_nl_input": "boolean",
                "pre_existing_fixed_stm_input": "boolean",
                "localized_requirement_relevant_issues": "boolean",
                "implemented_and_evaluated_on_stm": "boolean",
            },
            "cutoff": "2026-09-02",
            "databases": ["OpenAlex", "Crossref"],
            "search_protocol": "Use the four inclusion fields and retain exact query traces.",
            "comparison_only_fields": {
                "source_attribution": "compare",
                "native_stm_semantics": "compare",
                "replay_receipt": "compare",
            },
            "withheld_fields": [
                "candidate_claim", "paper_conclusion", "closest_work_matrix", "goal_prompt", "author_disposition",
            ],
        }
        record = {
            "schema_version": BLIND_RECORD_SCHEMA_VERSION,
            "base_commit": base,
            "reviewer_identity": "isolated-search-reviewer",
            "blind_packet_sha256": jcs_sha256(packet),
            "queries": ["(requirements) AND (state machine) AND (issue discovery)"],
            "search_trace": ["OpenAlex and Crossref fixture trace"],
            "raw_candidates": [{
                "candidate_id": "BLIND-01",
                "free_form_nl_input": True,
                "pre_existing_fixed_stm_input": True,
                "localized_requirement_relevant_issues": True,
                "implemented_and_evaluated_on_stm": True,
            }],
            "raw_findings": ["Fixture candidate retained for unblind disposition."],
        }
        results: list[dict[str, Any]] = []
        raw_paths = {
            path for path in hashes
            if path.startswith(CANONICAL_CURRENT_RAW + "/")
        }
        for role in sorted(REQUIRED_ROLES):
            reviewed_set = set(ROLE_REQUIRED_PATHS[role])
            if role == "fact_link_test":
                reviewed_set |= set(hashes)
            if role == "method_soundness":
                reviewed_set |= raw_paths
            reviewed_paths = sorted(reviewed_set)
            if role == "predicate_evidence":
                findings: list[dict[str, str]] = [{
                    "predicate_id": predicate_id,
                    "status": "PASS",
                    "evidence": "Fixture row reviewed against the copied audit.",
                } for predicate_id in sorted(CURRENT)]
            else:
                findings = [{
                    "finding_id": f"{role}-fixture",
                    "disposition": "fixed",
                    "evidence": "Fixture reviewer found no remaining C/I issue.",
                }]
            results.append({
                "role": role,
                "reviewer_identity": f"fixture-{role}-reviewer",
                "status": "PASS",
                "critical": 0,
                "important": 0,
                "input_hash": review_input_hash(reviewed_paths, hashes),
                "reviewed_paths": reviewed_paths,
                "findings": findings,
            })
        final_r1 = "This is the sole active R1 contract; the old contract is superseded. V3 uses steps."
        umbrella = "Umbrella body remains unchanged."
        records = load_json(paper / "story/experiment_dependent_gates.json")["records"]
        return {
            "schema_version": BUNDLE_SCHEMA_VERSION,
            "head": git(paper, "rev-parse", "HEAD"),
            "base_commit": base,
            "results": results,
            "path_hashes": hashes,
            "pr_initial_snapshots": {
                "r1": snapshot(197, final_r1),
                "umbrella": snapshot(179, umbrella),
            },
            "pr_final_snapshots": {
                "r1": snapshot(197, final_r1),
                "umbrella": snapshot(179, umbrella),
            },
            "blind_packet": packet,
            "blind_packet_jcs_sha256": jcs_sha256(packet),
            "blind_search_record": record,
            "blind_search_record_jcs_sha256": jcs_sha256(record),
            "blind_candidate_keyset": ["BLIND-01"],
            "final_dispositions": [
                {"candidate_id": "BLIND-01", "disposition": "rejected", "evidence": "Fixture full-text disposition."},
                {"candidate_id": "LATER-01", "disposition": "rejected", "evidence": "Fixture snowballing disposition."},
            ],
            "later_discovered_candidates": [{
                "candidate_id": "LATER-01",
                "discovery_phase": "snowballing",
                "query_or_citation_provenance": "Fixture backward citation trace.",
                "discovered_at": "2026-09-02T00:00:00+08:00",
            }],
            "final_disposition_keyset": ["BLIND-01", "LATER-01"],
            "union_proof": {"blind_plus_later_equals_final": True},
            "experiment_reviews": [{
                "id": entry["id"],
                "jcs_sha256": jcs_sha256(entry),
                "status": "PASS",
                "qualification": "Fixture record meets the experiment-only contract.",
            } for entry in records],
        }

    def execute_bundle(paper: Path, base: str, bundle: dict[str, Any], live: dict[str, str] | None = None) -> dict[str, Any]:
        evidence = paper.parent / "review-evidence.json"
        evidence.write_text(json.dumps(bundle, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        final = bundle["pr_final_snapshots"]
        live_bodies = live or {name: final[name]["body"] for name in PR_NUMBERS}
        return run(
            paper, evidence, base_commit=base,
            github_body_loader=lambda: live_bodies,
            task_start_body_hashes={
                name: bundle["pr_initial_snapshots"][name]["body_sha256"]
                for name in PR_NUMBERS
            },
            permitted_final_body_hashes={
                name: bundle["pr_final_snapshots"][name]["body_sha256"]
                for name in PR_NUMBERS
            },
        )

    def clone(value: Any) -> Any:
        return json.loads(json.dumps(value))

    def assert_bundle_rejected(
        label: str, mutate: Any, *, with_experiment: bool = False
    ) -> None:
        temporary, paper, base = prepare_fixture(with_experiment=with_experiment)
        try:
            bundle = build_bundle(paper, base)
            live = {name: bundle["pr_final_snapshots"][name]["body"] for name in PR_NUMBERS}
            mutate(bundle)
            result = execute_bundle(paper, base, bundle, live)
            assert not result["ready"], f"{label} was accepted"
        finally:
            temporary.cleanup()

    def assert_static_rejected(
        label: str, mutate: Any, *, with_experiment: bool = False
    ) -> None:
        temporary, paper, base = prepare_fixture(with_experiment=with_experiment)
        try:
            mutate(paper)
            errors: list[str] = []
            check_static_surface(paper, errors, base_commit=base)
            assert errors, f"{label} was accepted"
        finally:
            temporary.cleanup()

    def change_catalog(paper: Path, mutate: Any) -> None:
        path = paper / "related_work/provenance/current_source_catalog.json"
        catalog = load_json(path)
        mutate(catalog)
        path.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    def change_experiment_gate(paper: Path, mutate: Any) -> None:
        path = paper / "story/experiment_dependent_gates.json"
        data = load_json(path)
        mutate(data)
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    def replace_text(path: Path, old: str, new: str) -> None:
        text = path.read_text(encoding="utf-8")
        assert old in text
        path.write_text(text.replace(old, new, 1), encoding="utf-8")

    assert jcs_sha256({"x": "y"}) == jcs_sha256(json.loads(jcs_bytes({"x": "y"})))
    assert FOOTNOTE_REF.findall("Claim.[^one]\n\n[^one]: Ref.") == ["one"]
    assert EXPERIMENT_ID.fullmatch("TODO-EXPERIMENT-01")
    assert not EXPERIMENT_ID.fullmatch("TODO-EXPERIMENT-1")
    assert set(PREDICATE_ID.findall("S3、G3，V5")) == {"S3", "G3", "V5"}
    assert len(CURRENT) == len(LEGACY) == 19
    assert "natural language" not in strip_protected_markdown(
        "`natural language` https://example.invalid/natural-language\n[^ref]: natural language"
    )

    temporary, paper, base = prepare_fixture()
    try:
        golden = build_bundle(paper, base)
        assert execute_bundle(paper, base, golden)["ready"]
    finally:
        temporary.cleanup()
    temporary, paper, base = prepare_fixture(with_experiment=True)
    try:
        nonempty_experiment = build_bundle(paper, base)
        assert execute_bundle(paper, base, nonempty_experiment)["ready"]
    finally:
        temporary.cleanup()

    assert_static_rejected("missing_current_row", lambda root: replace_text(
        root / "related_work/provenance/predicate_provenance.md", "### S1 `element_exists`", "### S7 `element_exists`",
    ))
    assert_static_rejected("duplicate_current_row", lambda root: replace_text(
        root / "related_work/provenance/predicate_provenance.md", "### S2 `transition_exists`", "### S1 `transition_exists`",
    ))
    assert_static_rejected("nullable_crosswalk_endpoint", lambda root: replace_text(
        root / "related_work/provenance/predicate_provenance.md", "| -- | S3 | `newly_added`", "| `state_declared` | S3 | `newly_added`",
    ))
    assert_static_rejected("unknown_enum", lambda root: change_catalog(root, lambda catalog: catalog["r1_citation_audit"]["predicate_audits"][0].update({"implementation_relation": "UNKNOWN_ENUM"})))
    assert_static_rejected("unresolved_status", lambda root: change_catalog(root, lambda catalog: catalog["r1_citation_audit"]["predicate_audits"][0].update({"implementation_relation": "UNRESOLVED"})))
    assert_static_rejected("method_only_academic_evidence", lambda root: change_catalog(root, lambda catalog: catalog["r1_citation_audit"]["predicate_audits"][0]["status_evidence"]["academic"].update({"evidence_refs": ["method/src/paper_stm_method/compiler/soundness.py"]})))
    assert_static_rejected("technical_source_cannot_close_academic_qualification", lambda root: change_catalog(root, lambda catalog: catalog["r1_citation_audit"]["predicate_audits"][0]["status_evidence"]["academic"].update({"evidence_refs": ["ST8"]})))
    assert_static_rejected("predicate_heading_cannot_close_academic_qualification", lambda root: change_catalog(root, lambda catalog: catalog["r1_citation_audit"]["predicate_audits"][0]["status_evidence"]["academic"].update({"evidence_refs": ["ST1", "related_work/provenance/predicate_provenance.md#s1-element_exists"]})))
    assert_static_rejected("self_referential_instance_authority", lambda root: change_catalog(root, lambda catalog: catalog["r1_citation_audit"]["predicate_audits"][0]["status_evidence"]["instance"].update({"evidence_refs": ["related_work/provenance/predicate_provenance.md#s1-element_exists"]})))
    assert_static_rejected("broken_source_id", lambda root: change_catalog(root, lambda catalog: catalog["r1_citation_audit"]["predicate_audits"][0].update({"source_ids": ["NOT_A_SOURCE"]})))
    assert_static_rejected("impact_count_mismatch", lambda root: change_catalog(root, lambda catalog: catalog["r1_citation_audit"]["predicate_audits"][0]["impact"].update({"count": 1})))
    def omit_g2_i5(catalog: dict[str, Any]) -> None:
        g2 = next(row for row in catalog["r1_citation_audit"]["predicate_audits"] if row["predicate_id"] == "G2")
        g2["impact"]["receipt_ids"] = ["0020:r3:i1:receipt"]
        g2["impact"]["count"] = 1
    assert_static_rejected("g2_impact_receipt_omission", lambda root: change_catalog(root, omit_g2_i5))
    assert_static_rejected("illegal_polarity", lambda root: change_catalog(root, lambda catalog: catalog["r1_citation_audit"]["predicate_audits"][14]["publication_eligibility_by_polarity"]["unknown"].update({"runtime_witness_ceiling": "W2", "publication_eligibility": "ELIGIBLE"})))
    assert_static_rejected("broken_footnote", lambda root: replace_text(root / "story/paper_outline.md", "[^fair]:", "[^fair-broken]:"))
    assert_static_rejected("predicate_broken_footnote", lambda root: replace_text(root / "related_work/provenance/predicate_provenance.md", "[^uml251]:", "[^uml251-broken]:"))
    assert_static_rejected("orphan_footnote", lambda root: (root / "story/paper_outline.md").write_text((root / "story/paper_outline.md").read_text(encoding="utf-8") + "\n[^orphan]: Orphan fixture reference.\n", encoding="utf-8"))
    assert_static_rejected("duplicate_footnote", lambda root: (root / "story/paper_outline.md").write_text((root / "story/paper_outline.md").read_text(encoding="utf-8") + "\n[^fair]: Duplicate fixture reference.\n", encoding="utf-8"))
    assert_static_rejected("terminology_repeat", lambda root: (root / "story/paper_outline.md").write_text((root / "story/paper_outline.md").read_text(encoding="utf-8") + "\nnatural language\n", encoding="utf-8"))
    assert_static_rejected("terminology_missing_anchor", lambda root: replace_text(root / "story/terminology_policy.md", "`outline-0`", "`outline-missing`"))
    assert_static_rejected("terminology_before_anchor", lambda root: (root / "story/paper_outline.md").write_text("natural language\n" + (root / "story/paper_outline.md").read_text(encoding="utf-8"), encoding="utf-8"))
    assert_static_rejected("experiment_schema", lambda root: change_experiment_gate(root, lambda data: data.update({"unexpected": True})))
    assert_static_rejected("experiment_schema_version", lambda root: change_experiment_gate(root, lambda data: data.update({"schema_version": "wrong"})))
    assert_static_rejected("experiment_empty_required_string", lambda root: change_experiment_gate(root, lambda data: data["records"][0].update({"hypothesis": ""})), with_experiment=True)
    assert_static_rejected("experiment_wrong_type", lambda root: change_experiment_gate(root, lambda data: data["records"][0].update({"blocks_r1_ready": "false"})), with_experiment=True)
    assert_static_rejected("experiment_extra_record_field", lambda root: change_experiment_gate(root, lambda data: data["records"][0].update({"unexpected": True})), with_experiment=True)
    assert_static_rejected("experiment_extra_nested_field", lambda root: change_experiment_gate(root, lambda data: data["records"][0]["necessity_proof"].update({"unexpected": True})), with_experiment=True)
    assert_static_rejected("experiment_claim_not_closed", lambda root: change_experiment_gate(root, lambda data: data["records"][0].update({"affected_claims": ["CLM-MISSING"]})), with_experiment=True)
    assert_static_rejected("experiment_outline_id_not_closed", lambda root: (root / "story/paper_outline.md").write_text(
        (root / "story/paper_outline.md").read_text(encoding="utf-8").replace(
            "TODO-EXPERIMENT-01", "TODO-EXPERIMENT-MISSING"
        ), encoding="utf-8"
    ), with_experiment=True)

    temporary, paper, base = prepare_fixture()
    try:
        assert not run(paper, None, base_commit=base)["ready"]
    finally:
        temporary.cleanup()
    assert_bundle_rejected("jcs_hash_tamper", lambda bundle: bundle.update({"blind_packet_jcs_sha256": "0" * 64}))
    assert_bundle_rejected("missing_blind_raw_payload", lambda bundle: bundle.pop("blind_search_record"))
    assert_bundle_rejected("missing_role", lambda bundle: bundle["results"].pop())
    assert_bundle_rejected("duplicate_role", lambda bundle: bundle["results"].__setitem__(0, {**bundle["results"][0], "role": bundle["results"][1]["role"]}))
    assert_bundle_rejected("missing_required_path", lambda bundle: bundle["results"].__setitem__(0, {**bundle["results"][0], "reviewed_paths": ["story/paper_outline.md"], "input_hash": review_input_hash(["story/paper_outline.md"], bundle["path_hashes"])}))
    def omit_raw_soundness_path(bundle: dict[str, Any]) -> None:
        result = next(item for item in bundle["results"] if item["role"] == "method_soundness")
        raw_path = next(path for path in result["reviewed_paths"] if path.startswith(CANONICAL_CURRENT_RAW + "/"))
        result["reviewed_paths"].remove(raw_path)
        result["input_hash"] = review_input_hash(result["reviewed_paths"], bundle["path_hashes"])
    assert_bundle_rejected("missing_raw_soundness_path", omit_raw_soundness_path)
    assert_bundle_rejected("forbidden_blind_field", lambda bundle: bundle["blind_packet"].update({"candidate_claim": "forbidden"}))
    assert_bundle_rejected("raw_keyset_mismatch", lambda bundle: bundle.update({"blind_candidate_keyset": []}))
    assert_bundle_rejected("blind_candidate_omission", lambda bundle: (bundle["final_dispositions"].pop(0), bundle.update({"final_disposition_keyset": ["LATER-01"]})))
    assert_bundle_rejected("later_candidate_without_provenance", lambda bundle: bundle["later_discovered_candidates"][0].pop("discovered_at"))
    assert_bundle_rejected("candidate_union_mismatch", lambda bundle: bundle.update({"final_disposition_keyset": ["BLIND-01"]}))
    assert_bundle_rejected("stale_head", lambda bundle: bundle.update({"head": "0" * 40}))
    assert_bundle_rejected("stale_path_hash", lambda bundle: bundle["path_hashes"].update({"README.md": "0" * 64}))
    assert_bundle_rejected("pr_snapshot_live_body_drift", lambda bundle: bundle["pr_final_snapshots"]["r1"].update({"body": "changed", "body_sha256": sha256_bytes(b"changed")}))
    assert_bundle_rejected("unallowed_r1_body_diff", lambda bundle: bundle["pr_final_snapshots"]["r1"].update({"body": "This is the sole active R1 contract; the old contract is superseded. V3 uses steps. Extra change.", "body_sha256": sha256_bytes(b"This is the sole active R1 contract; the old contract is superseded. V3 uses steps. Extra change.")}))
    assert_bundle_rejected("predicate_review_not_19", lambda bundle: next(result for result in bundle["results"] if result["role"] == "predicate_evidence")["findings"].pop())
    assert_bundle_rejected("experiment_record_jcs_tamper", lambda bundle: bundle["experiment_reviews"][0].update({"jcs_sha256": "0" * 64}), with_experiment=True)

    print(json.dumps({
        "self_test": "passed",
        "golden": {"current": 19, "legacy": 19, "roles": 9, "nonempty_experiment": True},
        "fail_closed_cases": 40,
    }))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--paper-root", type=Path)
    parser.add_argument("--review-evidence", type=Path)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        return self_test()
    if args.paper_root is None:
        parser.error("--paper-root is required unless --self-test is used")
    result = run(args.paper_root.resolve(), args.review_evidence)
    print(json.dumps(result, ensure_ascii=False, indent=2) if args.json else result)
    return 0 if result["ready"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
