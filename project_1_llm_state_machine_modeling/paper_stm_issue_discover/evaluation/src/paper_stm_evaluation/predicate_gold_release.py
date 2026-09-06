"""Provider-free release views and validation for predicate gold v1."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, Field, model_validator

from .predicate_gold import (
    GoldStatus,
    PredicateGoldDataset,
    SourceRef,
    StrictModel,
    canonical_sha256,
    sha256_path,
    write_json,
)
from .predicate_gold_review import (
    HighRiskReviewBatch,
    Pane5ArbitrationBatch,
    TrackAProposalBatch,
    TrackBProposalBatch,
    TrackCReviewBatch,
)

SUMMARY_SCHEMA_VERSION = "paper1.predicate-gold.summary.v1"
MANIFEST_SCHEMA_VERSION = "paper1.predicate-gold.manifest.v1"
REVIEW_SELECTION_SCHEMA_VERSION = "paper1.predicate-gold.active-review-manifest.v1"
FROZEN_PREDICATE_IDS = tuple(
    [f"S{index}" for index in range(1, 7)]
    + [f"G{index}" for index in range(1, 5)]
    + [f"R{index}" for index in range(1, 5)]
    + [f"V{index}" for index in range(1, 6)]
)
TSV_COLUMNS = (
    "ledger_id",
    "pair_id",
    "family",
    "d_tier",
    "l_tier",
    "gold_status",
    "gold_mode",
    "exactness_relation",
    "predicate_ids",
    "selected_property_id",
    "execution_state",
    "execution_verdict",
    "positive_control_status",
    "reviewer_ids",
    "conflict_count",
    "confidence",
    "reason",
    "unsupported_reason",
    "capability_gap",
)


class CrossTabRow(StrictModel):
    """One labeled count in a deterministic summary cross-tabulation."""

    dimensions: dict[str, str] = Field(description="Dimension names and values identifying this count.", min_length=1)
    count: int = Field(description="Number of canonical ledger rows in this cell.", ge=0)


class PredicateUsageRow(StrictModel):
    """Expected predicate usage split by final exact and proxy status."""

    predicate_id: str = Field(description="Frozen predicate ID or EVALUATION_ONLY/UNSUPPORTED bucket.", min_length=1)
    selected_exact_count: int = Field(description="Exact canonical rows selecting this predicate or bucket.", ge=0)
    selected_proxy_count: int = Field(description="Sound-false-proxy canonical rows selecting this predicate or bucket.", ge=0)
    unsupported_count: int = Field(description="Unsupported rows assigned to the UNSUPPORTED bucket.", ge=0)


class PredicateGoldSummary(StrictModel):
    """Mechanically derived aggregate view of the canonical 145-row overlay."""

    schema_version: Literal[SUMMARY_SCHEMA_VERSION] = Field(default=SUMMARY_SCHEMA_VERSION, description="Summary schema version.")
    canonical_path: str = Field(description="Gold-root-relative canonical JSON path used for recomputation.", min_length=1)
    canonical_sha256: str = Field(description="Hash of the exact canonical JSON bytes.", pattern=r"^sha256:[0-9a-f]{64}$")
    total: int = Field(description="Number of canonical current-ledger annotations.", ge=0)
    blocked_execution_count: int = Field(description="Final BLOCKED_EXECUTION count; release requires zero.", ge=0)
    status_counts: dict[str, int] = Field(description="Counts by exact/proxy/unsupported final status.")
    family_counts: dict[str, int] = Field(description="Counts by immutable ledger family.")
    d_tier_counts: dict[str, int] = Field(description="Counts by immutable D tier.")
    l_tier_counts: dict[str, int] = Field(description="Counts by immutable L tier.")
    status_by_family: tuple[CrossTabRow, ...] = Field(description="Status and family cross-tabulation.")
    status_by_d_tier: tuple[CrossTabRow, ...] = Field(description="Status and D-tier cross-tabulation.")
    status_by_l_tier: tuple[CrossTabRow, ...] = Field(description="Status and L-tier cross-tabulation.")
    predicate_usage: tuple[PredicateUsageRow, ...] = Field(description="Selected exact/proxy use of each frozen predicate and non-predicate bucket.")
    evaluation_only_exact_count: int = Field(description="Exact rows implemented by isolated evaluation-only pyfcstm oracles.", ge=0)
    completed_false_count: int = Field(description="Executed exact/proxy rows with terminal Boolean false.", ge=0)
    completed_true_control_count: int = Field(description="Executed exact/proxy rows with a terminal Boolean true positive control.", ge=0)
    replay_match_count: int = Field(description="Executed exact/proxy rows whose saved replay matches.", ge=0)
    track_a_coverage: int = Field(description="Rows containing a Track A opinion.", ge=0)
    track_b_coverage: int = Field(description="Rows containing a Track B opinion.", ge=0)
    track_c_coverage: int = Field(description="Rows containing a Track C opinion.", ge=0)
    high_risk_coverage: int = Field(description="Rows containing an independent fourth high-risk opinion.", ge=0)
    conflict_rows: int = Field(description="Rows retaining at least one cross-track conflict.", ge=0)
    conflict_count: int = Field(description="Total retained conflict records.", ge=0)
    provider_experiment_calls: Literal[0] = Field(description="No provider experiment calls were used.")
    method_reruns: Literal[0] = Field(description="No method reruns were used.")
    judge_reruns: Literal[0] = Field(description="No Judge reruns were used.")
    full_experiment_reruns: Literal[0] = Field(description="No 54x3 reruns were used.")

    @model_validator(mode="after")
    def validate_totals(self) -> PredicateGoldSummary:
        """Require all headline count partitions to close to total."""

        for label, counts in (
            ("status", self.status_counts),
            ("family", self.family_counts),
            ("D tier", self.d_tier_counts),
            ("L tier", self.l_tier_counts),
        ):
            if sum(counts.values()) != self.total:
                raise ValueError(f"{label} counts do not sum to total")
        if self.blocked_execution_count != self.status_counts.get(GoldStatus.BLOCKED_EXECUTION.value, 0):
            raise ValueError("blocked_execution_count does not match status_counts")
        return self


class ManifestFile(StrictModel):
    """One immutable input or release output bound by the gold manifest."""

    role: str = Field(description="Input, canonical, view, receipt, review, protocol, schema, or validator role.", min_length=1)
    repository_path: str = Field(description="Repository-relative path; absolute and temporary paths are forbidden.", min_length=1)
    sha256: str = Field(description="SHA-256 of exact file bytes.", pattern=r"^sha256:[0-9a-f]{64}$")
    size_bytes: int = Field(description="Exact file size in bytes.", ge=0)


class PredicateGoldManifest(StrictModel):
    """Hash manifest binding frozen inputs, canonical data, views, reviews and receipts."""

    schema_version: Literal[MANIFEST_SCHEMA_VERSION] = Field(default=MANIFEST_SCHEMA_VERSION, description="Manifest schema version.")
    generated_at: str = Field(description="UTC manifest generation time supplied by the release command.", min_length=1)
    source_commit: str = Field(description="Main repository commit whose frozen inputs were used.", pattern=r"^[0-9a-f]{40}$")
    pyfcstm_commit: str = Field(description="Pinned pyfcstm commit used by parser/backend receipts.", pattern=r"^[0-9a-f]{40}$")
    supersedes: tuple[str, ...] = Field(description="Older gold overlays superseded by this manifest; empty for v1.")
    files: tuple[ManifestFile, ...] = Field(description="Sorted unique release file inventory.", min_length=1)
    provider_experiment_calls: Literal[0] = Field(description="No provider experiment calls were used.")
    method_reruns: Literal[0] = Field(description="No method reruns were used.")
    judge_reruns: Literal[0] = Field(description="No Judge reruns were used.")
    full_experiment_reruns: Literal[0] = Field(description="No 54x3 reruns were used.")
    manifest_sha256: str = Field(description="Canonical payload digest excluding this field.", pattern=r"^sha256:[0-9a-f]{64}$")

    @model_validator(mode="after")
    def validate_manifest(self) -> PredicateGoldManifest:
        """Require sorted unique paths and a correct canonical payload hash."""

        paths = [item.repository_path for item in self.files]
        if paths != sorted(paths) or len(paths) != len(set(paths)):
            raise ValueError("manifest files must be sorted by unique repository path")
        expected = canonical_sha256(self.model_dump(mode="json", exclude={"manifest_sha256"}))
        if self.manifest_sha256 != expected:
            raise ValueError("manifest_sha256 does not match payload")
        return self


class ReviewSelectionFile(StrictModel):
    """One explicitly selected current review file and its immutable digest."""

    repository_path: str = Field(
        description="Review-root-relative JSON path selected for the current release.",
        min_length=1,
    )
    sha256: str = Field(
        description="SHA-256 of the exact selected review file bytes.",
        pattern=r"^sha256:[0-9a-f]{64}$",
    )


class ActiveReviewManifest(StrictModel):
    """Current review selection that excludes retained superseded attempts."""

    schema_version: Literal[REVIEW_SELECTION_SCHEMA_VERSION] = Field(
        default=REVIEW_SELECTION_SCHEMA_VERSION,
        description="Active review selection schema version.",
    )
    generated_at: str = Field(
        description="UTC time at which the current review selection was sealed.",
        min_length=1,
    )
    track_a: tuple[ReviewSelectionFile, ...] = Field(
        description="Selected blind Track A batch files.",
        min_length=1,
    )
    track_b: tuple[ReviewSelectionFile, ...] = Field(
        description="Selected blind Track B batch files.",
        min_length=1,
    )
    track_c: tuple[ReviewSelectionFile, ...] = Field(
        description="Selected post-proposal Track C batch files.",
        min_length=1,
    )
    high_risk: tuple[ReviewSelectionFile, ...] = Field(
        description="Selected independent fourth-review batch files.",
        min_length=1,
    )
    arbitration: tuple[ReviewSelectionFile, ...] = Field(
        description="Selected pane5 arbitration batch files.",
        min_length=1,
    )
    superseded_review_roots: tuple[str, ...] = Field(
        description="Retained review attempts deliberately excluded from current coverage."
    )
    manifest_sha256: str = Field(
        description="Canonical digest of this manifest excluding this field.",
        pattern=r"^sha256:[0-9a-f]{64}$",
    )

    @model_validator(mode="after")
    def validate_selection(self) -> ActiveReviewManifest:
        """Require sorted unique relative paths and a correct payload digest."""

        selected = (
            *self.track_a,
            *self.track_b,
            *self.track_c,
            *self.high_risk,
            *self.arbitration,
        )
        paths = [item.repository_path for item in selected]
        if len(paths) != len(set(paths)):
            raise ValueError("active review manifest paths must be globally unique")
        for group in (
            self.track_a,
            self.track_b,
            self.track_c,
            self.high_risk,
            self.arbitration,
        ):
            group_paths = [item.repository_path for item in group]
            if group_paths != sorted(group_paths):
                raise ValueError("active review manifest groups must be path-sorted")
        if any(Path(path).is_absolute() or ".." in Path(path).parts for path in paths):
            raise ValueError("active review manifest paths must remain review-root-relative")
        expected = canonical_sha256(self.model_dump(mode="json", exclude={"manifest_sha256"}))
        if self.manifest_sha256 != expected:
            raise ValueError("active review manifest digest does not match payload")
        return self


def _cross_tab(rows: list[tuple[str, str]], first: str, second: str) -> tuple[CrossTabRow, ...]:
    """Create one deterministic two-dimension count table."""

    counts = Counter(rows)
    return tuple(
        CrossTabRow(dimensions={first: left, second: right}, count=count)
        for (left, right), count in sorted(counts.items())
    )


def derive_summary(dataset: PredicateGoldDataset, *, canonical_path: Path, gold_root: Path) -> PredicateGoldSummary:
    """Derive every summary count from canonical annotations."""

    annotations = list(dataset.items.values())
    status_counts = Counter(item.gold_status.value for item in annotations)
    for status in GoldStatus:
        status_counts.setdefault(status.value, 0)

    usage: dict[str, Counter[str]] = defaultdict(Counter)
    for predicate_id in FROZEN_PREDICATE_IDS:
        usage[predicate_id]
    for item in annotations:
        exact = item.gold_status in {GoldStatus.EXACT_FALSE, GoldStatus.COMPOSITE_EXACT_FALSE}
        proxy = item.gold_status == GoldStatus.SOUND_FALSE_PROXY
        if exact and item.gold_property is not None:
            buckets = item.predicate_ids or ("EVALUATION_ONLY",)
            for predicate_id in set(buckets):
                usage[predicate_id]["exact"] += 1
        elif proxy and item.proxy_property is not None:
            buckets = item.proxy_property.predicate_ids or ("EVALUATION_ONLY",)
            for predicate_id in set(buckets):
                usage[predicate_id]["proxy"] += 1
        elif item.gold_status == GoldStatus.UNSUPPORTED_EXACT:
            usage["UNSUPPORTED"]["unsupported"] += 1

    executed = [
        item.execution if item.execution is not None else item.proxy_execution
        for item in annotations
        if item.execution is not None or item.proxy_execution is not None
    ]
    tracks = {
        "A_OBLIGATION": sum(any(op.track.value == "A_OBLIGATION" for op in item.review_opinions) for item in annotations),
        "B_PROPERTY": sum(any(op.track.value == "B_PROPERTY" for op in item.review_opinions) for item in annotations),
        "C_EXECUTION": sum(any(op.track.value == "C_EXECUTION" for op in item.review_opinions) for item in annotations),
        "EXTRA_HIGH_RISK": sum(any(op.track.value == "EXTRA_HIGH_RISK" for op in item.review_opinions) for item in annotations),
    }
    return PredicateGoldSummary(
        canonical_path=canonical_path.resolve().relative_to(gold_root.resolve()).as_posix(),
        canonical_sha256=sha256_path(canonical_path),
        total=len(annotations),
        blocked_execution_count=status_counts[GoldStatus.BLOCKED_EXECUTION.value],
        status_counts=dict(sorted(status_counts.items())),
        family_counts=dict(sorted(Counter(item.family for item in annotations).items())),
        d_tier_counts=dict(sorted(Counter(item.d_tier for item in annotations).items())),
        l_tier_counts=dict(sorted(Counter(item.l_tier for item in annotations).items())),
        status_by_family=_cross_tab([(item.gold_status.value, item.family) for item in annotations], "gold_status", "family"),
        status_by_d_tier=_cross_tab([(item.gold_status.value, item.d_tier) for item in annotations], "gold_status", "d_tier"),
        status_by_l_tier=_cross_tab([(item.gold_status.value, item.l_tier) for item in annotations], "gold_status", "l_tier"),
        predicate_usage=tuple(
            PredicateUsageRow(
                predicate_id=predicate_id,
                selected_exact_count=counts["exact"],
                selected_proxy_count=counts["proxy"],
                unsupported_count=counts["unsupported"],
            )
            for predicate_id, counts in sorted(usage.items())
        ),
        evaluation_only_exact_count=sum(
            item.gold_status in {GoldStatus.EXACT_FALSE, GoldStatus.COMPOSITE_EXACT_FALSE}
            and item.gold_property is not None
            and not item.gold_property.predicate_ids
            for item in annotations
        ),
        completed_false_count=sum(record is not None and record.verdict is False for record in executed),
        completed_true_control_count=sum(item.positive_control is not None and item.positive_control.verdict is True for item in annotations),
        replay_match_count=sum(record is not None and record.replay_status == "REPLAY_MATCH" for record in executed),
        track_a_coverage=tracks["A_OBLIGATION"],
        track_b_coverage=tracks["B_PROPERTY"],
        track_c_coverage=tracks["C_EXECUTION"],
        high_risk_coverage=tracks["EXTRA_HIGH_RISK"],
        conflict_rows=sum(bool(item.conflicts) for item in annotations),
        conflict_count=sum(len(item.conflicts) for item in annotations),
        provider_experiment_calls=dataset.provider_experiment_calls,
        method_reruns=dataset.method_reruns,
        judge_reruns=dataset.judge_reruns,
        full_experiment_reruns=dataset.full_experiment_reruns,
    )


def _tsv_value(value: Any) -> str:
    """Serialize one flat TSV value without losing Boolean or list identity."""

    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (list, tuple)):
        return "|".join(str(item) for item in value)
    return str(value).replace("\t", " ").replace("\r", " ").replace("\n", " ")


def write_tsv(dataset: PredicateGoldDataset, path: Path) -> None:
    """Write the deterministic human-review mirror of canonical JSON."""

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=TSV_COLUMNS, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        for item in sorted(dataset.items.values(), key=lambda row: row.ledger_id):
            selected = item.gold_property or item.proxy_property
            execution = item.execution or item.proxy_execution
            row = {
                "ledger_id": item.ledger_id,
                "pair_id": item.pair_id,
                "family": item.family,
                "d_tier": item.d_tier,
                "l_tier": item.l_tier,
                "gold_status": item.gold_status.value,
                "gold_mode": item.gold_mode.value,
                "exactness_relation": item.exactness_relation.value,
                "predicate_ids": item.predicate_ids if item.predicate_ids else (selected.predicate_ids if selected else ()),
                "selected_property_id": selected.property_id if selected else None,
                "execution_state": execution.state.value if execution else None,
                "execution_verdict": execution.verdict if execution else None,
                "positive_control_status": item.positive_control.status.value if item.positive_control else None,
                "reviewer_ids": item.reviewer_ids,
                "conflict_count": len(item.conflicts),
                "confidence": item.confidence.value,
                "reason": item.reason,
                "unsupported_reason": item.unsupported_reason,
                "capability_gap": item.capability_gap,
            }
            writer.writerow({key: _tsv_value(value) for key, value in row.items()})


def validate_review_batches(
    review_root: Path,
    expected_ids: set[str],
    active_manifest_path: Path,
) -> dict[str, int]:
    """Validate only hash-selected current reviews and exact per-track coverage."""

    manifest = ActiveReviewManifest.model_validate_json(
        active_manifest_path.read_text(encoding="utf-8")
    )
    selections = {
        "track_a_independent": (TrackAProposalBatch, manifest.track_a),
        "track_b_independent": (TrackBProposalBatch, manifest.track_b),
        "track_c_independent": (TrackCReviewBatch, manifest.track_c),
        "high_risk_independent": (HighRiskReviewBatch, manifest.high_risk),
        "arbitration": (Pane5ArbitrationBatch, manifest.arbitration),
    }
    coverage: dict[str, set[str]] = {}
    for directory, (model, selected_files) in selections.items():
        ids: list[str] = []
        for selected in selected_files:
            path = review_root / selected.repository_path
            if not path.is_file() or sha256_path(path) != selected.sha256:
                raise ValueError(
                    f"missing or changed active {directory} review: {selected.repository_path}"
                )
            batch = model.model_validate_json(path.read_text(encoding="utf-8"))
            ids.extend(row.ledger_id for row in batch.rows)
        if len(ids) != len(set(ids)):
            duplicates = sorted(item for item, count in Counter(ids).items() if count > 1)
            raise ValueError(f"{directory} contains duplicate ledger IDs: {duplicates}")
        coverage[directory] = set(ids)
        if coverage[directory] != expected_ids:
            missing = sorted(expected_ids - coverage[directory])
            extra = sorted(coverage[directory] - expected_ids)
            raise ValueError(f"{directory} coverage mismatch; missing={missing}, extra={extra}")
    return {track: len(ids) for track, ids in coverage.items()}


def build_active_review_manifest(
    *,
    review_root: Path,
    generated_at: str,
    track_a_paths: list[Path],
    track_b_paths: list[Path],
    track_c_paths: list[Path],
    high_risk_paths: list[Path],
    arbitration_paths: list[Path],
    superseded_review_roots: list[str],
) -> ActiveReviewManifest:
    """Seal the explicit current review selection without deleting old attempts."""

    def selected(paths: list[Path]) -> tuple[ReviewSelectionFile, ...]:
        records = [
            ReviewSelectionFile(
                repository_path=path.resolve().relative_to(review_root.resolve()).as_posix(),
                sha256=sha256_path(path),
            )
            for path in paths
        ]
        return tuple(sorted(records, key=lambda item: item.repository_path))

    unsigned = {
        "schema_version": REVIEW_SELECTION_SCHEMA_VERSION,
        "generated_at": generated_at,
        "track_a": [item.model_dump(mode="json") for item in selected(track_a_paths)],
        "track_b": [item.model_dump(mode="json") for item in selected(track_b_paths)],
        "track_c": [item.model_dump(mode="json") for item in selected(track_c_paths)],
        "high_risk": [
            item.model_dump(mode="json") for item in selected(high_risk_paths)
        ],
        "arbitration": [
            item.model_dump(mode="json") for item in selected(arbitration_paths)
        ],
        "superseded_review_roots": sorted(set(superseded_review_roots)),
    }
    return ActiveReviewManifest(**unsigned, manifest_sha256=canonical_sha256(unsigned))


def _load_dataset(path: Path) -> PredicateGoldDataset:
    """Load canonical JSON through its full Pydantic contract."""

    return PredicateGoldDataset.model_validate_json(path.read_text(encoding="utf-8"))


def _iter_source_refs(value: Any) -> tuple[SourceRef, ...]:
    """Recursively enumerate every structured SourceRef in a canonical model."""

    refs: list[SourceRef] = []

    def visit(node: Any) -> None:
        if isinstance(node, SourceRef):
            refs.append(node)
        elif isinstance(node, BaseModel):
            for field_value in node.__dict__.values():
                visit(field_value)
        elif isinstance(node, dict):
            for field_value in node.values():
                visit(field_value)
        elif isinstance(node, (list, tuple)):
            for field_value in node:
                visit(field_value)

    visit(value)
    return tuple(refs)


def _resolve_json_pointer(document: Any, pointer: str) -> Any:
    """Resolve an RFC 6901 pointer for release-time evidence validation."""

    if pointer == "":
        return document
    if not pointer.startswith("/"):
        raise ValueError(f"invalid JSON pointer: {pointer}")
    value = document
    for token in pointer[1:].split("/"):
        token = token.replace("~1", "/").replace("~0", "~")
        value = value[int(token)] if isinstance(value, list) else value[token]
    return value


def _validate_source_ref(repo_root: Path, ref: SourceRef) -> None:
    """Validate one referenced file, digest, optional pointer and line range."""

    relative = Path(ref.repository_path)
    if relative.is_absolute() or ".." in relative.parts:
        raise ValueError(f"non-relative source reference: {ref.repository_path}")
    path = repo_root / relative
    if not path.is_file() or sha256_path(path) != ref.sha256:
        raise ValueError(f"missing or changed source evidence: {ref.repository_path}")
    if ref.json_pointer is not None:
        if path.suffix != ".json":
            raise ValueError(
                f"JSON pointer targets a non-JSON file: {ref.repository_path}"
            )
        try:
            _resolve_json_pointer(
                json.loads(path.read_text(encoding="utf-8")), ref.json_pointer
            )
        except (IndexError, KeyError, TypeError, ValueError, json.JSONDecodeError) as error:
            raise ValueError(
                f"invalid source pointer {ref.repository_path}#{ref.json_pointer}"
            ) from error
    if ref.line_start is not None:
        line_count = len(path.read_text(encoding="utf-8").splitlines())
        if ref.line_start > line_count or (
            ref.line_end is not None and ref.line_end > line_count
        ):
            raise ValueError(f"source line exceeds file: {ref.repository_path}")


def _find_repo_root(path: Path) -> Path:
    """Find the enclosing Git worktree without relying on a fixed file depth."""

    for candidate in (path.resolve(), *path.resolve().parents):
        if (candidate / ".git").exists():
            return candidate
    raise ValueError(f"cannot find enclosing Git worktree for {path}")


def validate_release(
    *,
    canonical_path: Path,
    inventory_path: Path,
    tsv_path: Path,
    summary_path: Path,
    schema_path: Path,
    review_root: Path,
    active_review_manifest_path: Path,
) -> PredicateGoldSummary:
    """Validate ledger closure, mirrors, receipts, controls, reviews and hashes."""

    dataset = _load_dataset(canonical_path)
    inventory = json.loads(inventory_path.read_text(encoding="utf-8"))
    expected_ids = {ledger_id for pair in inventory["pairs"] for ledger_id in pair["ledger_ids"]}
    if set(dataset.items) != expected_ids or len(dataset.items) != inventory["ledger_count"]:
        raise ValueError("canonical IDs do not exactly match inventory ledger IDs")
    if dataset.ledger_sha256 != inventory["ledger_sha256"]:
        raise ValueError("canonical ledger hash does not match inventory")
    if dataset.registry_sha256 != inventory["registry_sha256"]:
        raise ValueError("canonical registry hash does not match inventory")
    validate_review_batches(review_root, expected_ids, active_review_manifest_path)
    repo_root = _find_repo_root(canonical_path)

    saved_schema = json.loads(schema_path.read_text(encoding="utf-8"))
    if saved_schema != PredicateGoldDataset.model_json_schema():
        raise ValueError("saved JSON Schema differs from the canonical model")

    for item in dataset.items.values():
        for ref in _iter_source_refs(item):
            _validate_source_ref(repo_root, ref)

    gold_root = canonical_path.parent
    recomputed = derive_summary(dataset, canonical_path=canonical_path, gold_root=gold_root)
    saved = PredicateGoldSummary.model_validate_json(summary_path.read_text(encoding="utf-8"))
    if saved != recomputed:
        raise ValueError("saved summary differs from canonical recomputation")

    temporary_tsv = tsv_path.with_suffix(".recomputed.tmp.tsv")
    write_tsv(dataset, temporary_tsv)
    try:
        if temporary_tsv.read_bytes() != tsv_path.read_bytes():
            raise ValueError("saved TSV differs from canonical recomputation")
    finally:
        temporary_tsv.unlink(missing_ok=True)
    return recomputed


def build_manifest(
    *,
    repo_root: Path,
    paths: list[Path],
    generated_at: str,
    source_commit: str,
    pyfcstm_commit: str,
) -> PredicateGoldManifest:
    """Build a sorted, hash-bound release manifest for explicitly selected files."""

    records = tuple(
        ManifestFile(
            role="predicate_gold_release_artifact",
            repository_path=path.resolve().relative_to(repo_root.resolve()).as_posix(),
            sha256=sha256_path(path),
            size_bytes=path.stat().st_size,
        )
        for path in sorted(set(paths), key=lambda item: item.resolve().relative_to(repo_root.resolve()).as_posix())
    )
    unsigned = {
        "schema_version": MANIFEST_SCHEMA_VERSION,
        "generated_at": generated_at,
        "source_commit": source_commit,
        "pyfcstm_commit": pyfcstm_commit,
        "supersedes": [],
        "files": [item.model_dump(mode="json") for item in records],
        "provider_experiment_calls": 0,
        "method_reruns": 0,
        "judge_reruns": 0,
        "full_experiment_reruns": 0,
    }
    return PredicateGoldManifest(**unsigned, manifest_sha256=canonical_sha256(unsigned))


def collect_release_paths(
    *,
    repo_root: Path,
    canonical_path: Path,
    review_root: Path,
    active_review_manifest_path: Path,
    explicit_paths: list[Path],
    code_roots: list[Path],
) -> list[Path]:
    """Collect current inputs, receipts, controls, reviews, code, and views.

    Historical/rejected review attempts are not swept into the publication
    surface.  The canonical model, active-review manifest, executable issue
    IDs, and explicit horizontal-review/document paths determine membership.
    """

    dataset = _load_dataset(canonical_path)
    gold_root = canonical_path.parent
    selected: set[Path] = {canonical_path.resolve()}
    selected.update(path.resolve() for path in explicit_paths)

    active = ActiveReviewManifest.model_validate_json(
        active_review_manifest_path.read_text(encoding="utf-8")
    )
    review_root_resolved = review_root.resolve()
    superseded_roots = tuple(
        (review_root_resolved / relative).resolve()
        for relative in active.superseded_review_roots
    )

    def include_source_ref(ref: SourceRef) -> bool:
        """Exclude rejected review attempts from the publication manifest."""

        path = (repo_root / ref.repository_path).resolve()
        if review_root_resolved not in path.parents:
            return True
        if any(path == root or root in path.parents for root in superseded_roots):
            return False
        relative = path.relative_to(review_root_resolved)
        return not any("rejected" in part.lower() for part in relative.parts)

    for annotation in dataset.items.values():
        selected.update(
            (repo_root / ref.repository_path).resolve()
            for ref in _iter_source_refs(annotation)
            if include_source_ref(ref)
        )
        if annotation.execution is not None or annotation.proxy_execution is not None:
            receipt_root = gold_root / "receipts" / annotation.ledger_id
            selected.update(path.resolve() for path in receipt_root.rglob("*") if path.is_file())
        if annotation.positive_control is not None:
            control_root = gold_root / "controls" / annotation.ledger_id
            if control_root.is_dir():
                selected.update(path.resolve() for path in control_root.rglob("*") if path.is_file())
            if annotation.positive_control.artifact_path is not None:
                selected.add((repo_root / annotation.positive_control.artifact_path).resolve())

    selected.add(active_review_manifest_path.resolve())
    for entry in (
        *active.track_a,
        *active.track_b,
        *active.track_c,
        *active.high_risk,
        *active.arbitration,
    ):
        selected.add((review_root / entry.repository_path).resolve())

    for code_root in code_roots:
        selected.update(
            path.resolve()
            for path in code_root.glob("predicate_gold*.py")
            if path.is_file()
        )

    invalid = [
        path
        for path in selected
        if not path.is_file()
        or path.is_absolute()
        and repo_root.resolve() not in path.parents
    ]
    if invalid:
        raise ValueError(f"missing or out-of-repository manifest paths: {invalid}")
    return sorted(
        selected,
        key=lambda path: path.relative_to(repo_root.resolve()).as_posix(),
    )


def validate_manifest(*, repo_root: Path, manifest_path: Path) -> PredicateGoldManifest:
    """Validate every release-manifest path, size and digest."""

    manifest = PredicateGoldManifest.model_validate_json(
        manifest_path.read_text(encoding="utf-8")
    )
    for item in manifest.files:
        relative = Path(item.repository_path)
        if relative.is_absolute() or ".." in relative.parts:
            raise ValueError(f"invalid manifest path: {item.repository_path}")
        path = repo_root / relative
        if not path.is_file():
            raise ValueError(f"missing manifest file: {item.repository_path}")
        if path.stat().st_size != item.size_bytes or sha256_path(path) != item.sha256:
            raise ValueError(f"changed manifest file: {item.repository_path}")
    return manifest


def _command_recompute(args: argparse.Namespace) -> int:
    """Write deterministic summary and TSV views from canonical JSON."""

    canonical_path = Path(args.canonical)
    dataset = _load_dataset(canonical_path)
    summary = derive_summary(dataset, canonical_path=canonical_path, gold_root=canonical_path.parent)
    write_json(Path(args.summary), summary.model_dump(mode="json"))
    write_tsv(dataset, Path(args.tsv))
    print(json.dumps({"total": summary.total, "status_counts": summary.status_counts}, sort_keys=True))
    return 0


def _command_validate(args: argparse.Namespace) -> int:
    """Run the complete provider-free canonical release validator."""

    summary = validate_release(
        canonical_path=Path(args.canonical),
        inventory_path=Path(args.inventory),
        tsv_path=Path(args.tsv),
        summary_path=Path(args.summary),
        schema_path=Path(args.schema),
        review_root=Path(args.review_root),
        active_review_manifest_path=Path(args.active_review_manifest),
    )
    print(json.dumps({"result": "PASS", "total": summary.total, "status_counts": summary.status_counts}, sort_keys=True))
    return 0


def _command_manifest(args: argparse.Namespace) -> int:
    """Write a hash-bound release manifest for explicit repository files."""

    manifest = build_manifest(
        repo_root=Path(args.repo_root),
        paths=[Path(path) for path in args.path],
        generated_at=args.generated_at,
        source_commit=args.source_commit,
        pyfcstm_commit=args.pyfcstm_commit,
    )
    write_json(Path(args.output), manifest.model_dump(mode="json"))
    print(
        json.dumps(
            {
                "result": "PASS",
                "files": len(manifest.files),
                "manifest_sha256": manifest.manifest_sha256,
            },
            sort_keys=True,
        )
    )
    return 0


def _command_manifest_auto(args: argparse.Namespace) -> int:
    """Collect and seal the current canonical predicate-gold release surface."""

    repo_root = Path(args.repo_root).resolve()
    paths = collect_release_paths(
        repo_root=repo_root,
        canonical_path=Path(args.canonical),
        review_root=Path(args.review_root),
        active_review_manifest_path=Path(args.active_review_manifest),
        explicit_paths=[Path(path) for path in args.path],
        code_roots=[Path(path) for path in args.code_root],
    )
    manifest = build_manifest(
        repo_root=repo_root,
        paths=paths,
        generated_at=args.generated_at,
        source_commit=args.source_commit,
        pyfcstm_commit=args.pyfcstm_commit,
    )
    write_json(Path(args.output), manifest.model_dump(mode="json"))
    print(
        json.dumps(
            {
                "result": "PASS",
                "files": len(manifest.files),
                "manifest_sha256": manifest.manifest_sha256,
            },
            sort_keys=True,
        )
    )
    return 0


def _command_manifest_validate(args: argparse.Namespace) -> int:
    """Validate all files selected by one release manifest."""

    manifest = validate_manifest(
        repo_root=Path(args.repo_root), manifest_path=Path(args.manifest)
    )
    print(
        json.dumps(
            {"result": "PASS", "files": len(manifest.files)}, sort_keys=True
        )
    )
    return 0


def _command_review_manifest(args: argparse.Namespace) -> int:
    """Write one hash-bound current review selection manifest."""

    manifest = build_active_review_manifest(
        review_root=Path(args.review_root),
        generated_at=args.generated_at,
        track_a_paths=[Path(path) for path in args.track_a],
        track_b_paths=[Path(path) for path in args.track_b],
        track_c_paths=[Path(path) for path in args.track_c],
        high_risk_paths=[Path(path) for path in args.high_risk],
        arbitration_paths=[Path(path) for path in args.arbitration],
        superseded_review_roots=args.superseded_review_root,
    )
    write_json(Path(args.output), manifest.model_dump(mode="json"))
    print(
        json.dumps(
            {
                "result": "PASS",
                "manifest_sha256": manifest.manifest_sha256,
                "selected_files": sum(
                    len(group)
                    for group in (
                        manifest.track_a,
                        manifest.track_b,
                        manifest.track_c,
                        manifest.high_risk,
                        manifest.arbitration,
                    )
                ),
            },
            sort_keys=True,
        )
    )
    return 0


def main() -> int:
    """Run provider-free release recomputation or validation."""

    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    recompute = subparsers.add_parser("recompute", help="derive TSV and summary from canonical JSON")
    recompute.add_argument("--canonical", required=True)
    recompute.add_argument("--summary", required=True)
    recompute.add_argument("--tsv", required=True)
    recompute.set_defaults(handler=_command_recompute)
    validate = subparsers.add_parser("validate", help="validate canonical data, reviews, receipts and mirrors")
    validate.add_argument("--canonical", required=True)
    validate.add_argument("--inventory", required=True)
    validate.add_argument("--summary", required=True)
    validate.add_argument("--tsv", required=True)
    validate.add_argument("--schema", required=True)
    validate.add_argument("--review-root", required=True)
    validate.add_argument("--active-review-manifest", required=True)
    validate.set_defaults(handler=_command_validate)
    review_manifest = subparsers.add_parser(
        "review-manifest",
        help="seal the current review files while retaining superseded attempts",
    )
    review_manifest.add_argument("--review-root", required=True)
    review_manifest.add_argument("--generated-at", required=True)
    review_manifest.add_argument("--track-a", action="append", required=True)
    review_manifest.add_argument("--track-b", action="append", required=True)
    review_manifest.add_argument("--track-c", action="append", required=True)
    review_manifest.add_argument("--high-risk", action="append", required=True)
    review_manifest.add_argument("--arbitration", action="append", required=True)
    review_manifest.add_argument(
        "--superseded-review-root", action="append", default=[]
    )
    review_manifest.add_argument("--output", required=True)
    review_manifest.set_defaults(handler=_command_review_manifest)
    manifest = subparsers.add_parser(
        "manifest", help="seal explicit release files into a repository-relative manifest"
    )
    manifest.add_argument("--repo-root", required=True)
    manifest.add_argument("--generated-at", required=True)
    manifest.add_argument("--source-commit", required=True)
    manifest.add_argument("--pyfcstm-commit", required=True)
    manifest.add_argument("--path", action="append", required=True)
    manifest.add_argument("--output", required=True)
    manifest.set_defaults(handler=_command_manifest)
    manifest_auto = subparsers.add_parser(
        "manifest-auto",
        help="collect and seal the current canonical publication surface",
    )
    manifest_auto.add_argument("--repo-root", required=True)
    manifest_auto.add_argument("--canonical", required=True)
    manifest_auto.add_argument("--review-root", required=True)
    manifest_auto.add_argument("--active-review-manifest", required=True)
    manifest_auto.add_argument("--generated-at", required=True)
    manifest_auto.add_argument("--source-commit", required=True)
    manifest_auto.add_argument("--pyfcstm-commit", required=True)
    manifest_auto.add_argument("--path", action="append", required=True)
    manifest_auto.add_argument("--code-root", action="append", default=[])
    manifest_auto.add_argument("--output", required=True)
    manifest_auto.set_defaults(handler=_command_manifest_auto)
    manifest_validate = subparsers.add_parser(
        "manifest-validate", help="validate every path, size and digest in a manifest"
    )
    manifest_validate.add_argument("--repo-root", required=True)
    manifest_validate.add_argument("--manifest", required=True)
    manifest_validate.set_defaults(handler=_command_manifest_validate)
    args = parser.parse_args()
    return args.handler(args)


if __name__ == "__main__":
    raise SystemExit(main())
