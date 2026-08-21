"""当前注册表的最小契约测试。

这些测试只依赖标准库，迁移期也能运行；后续模块化实现的测试必须继续复用它们。
"""

import json
from pathlib import Path


REGISTRY = Path(__file__).parents[1] / "predicate_registry.json"
PROJECT_ROOT = REGISTRY.parents[2]


def load_registry() -> dict:
    return json.loads(REGISTRY.read_text(encoding="utf-8"))


def test_registry_has_frozen_four_family_shape() -> None:
    data = load_registry()
    predicates = [p for family in data["families"] for p in family["predicates"]]

    assert data["registry_version"] == "four-family-19-core.v1"
    assert data["public_predicate_count"] == 19
    assert len(predicates) == 19
    assert len({p["id"] for p in predicates}) == 19
    assert {f["id"]: len(f["predicates"]) for f in data["families"]} == {
        "structure": 6,
        "topology": 4,
        "trajectory": 4,
        "bounded_verification": 5,
    }


def test_w1_is_a_hit_and_unknown_is_not_a_violation() -> None:
    data = load_registry()

    assert data["w1_is_semantic_hit"] is True
    assert data["unknown_is_violation"] is False
    assert "semantic hit" in data["evidence_levels"]["W1"]
    assert "不计为命中" in data["evidence_levels"]["W0"]


def test_registry_uses_current_source_types() -> None:
    data = load_registry()
    allowed = {"domain", "formal", "technical"}
    predicates = [p for family in data["families"] for p in family["predicates"]]

    assert "source_type_legend" in data
    assert not any("provenance_class" in p for p in predicates)
    assert all(set(p["source_types"]) <= allowed for p in predicates)
    assert all(p["sources"] for p in predicates)


def test_every_source_id_resolves_to_current_catalog() -> None:
    data = load_registry()
    catalog_path = PROJECT_ROOT / data["source_catalog_path"]
    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    source_ids = {source["id"] for source in catalog["sources"]}
    predicates = [p for family in data["families"] for p in family["predicates"]]

    assert catalog["registry_version"] == data["registry_version"]
    assert source_ids
    assert all(set(p["sources"]) <= source_ids for p in predicates)
    assert all(source["paths"] for source in catalog["sources"])
    assert all(source["status"] in {"reviewed_partial", "candidate", "rejected_for_scope"}
               for source in catalog["sources"])
    assert all(
        (PROJECT_ROOT / path).exists()
        for source in catalog["sources"]
        for path in source["paths"]
    )


def test_predicate_source_audit_covers_all_public_predicates() -> None:
    data = load_registry()
    catalog = json.loads(
        (PROJECT_ROOT / data["source_catalog_path"]).read_text(encoding="utf-8")
    )
    predicates = {p["id"] for family in data["families"] for p in family["predicates"]}
    audit = catalog["predicate_audit"]
    allowed = {
        "partial_pass",
        "candidate",
        "w1_only_pending_source",
        "w1_only_no_current_domain_source",
        "w1_only_pending_independent_rule",
        "w1_only_pending_bounded_semantics",
        "w1_only_parallel_sources_only",
    }

    assert set(audit) == predicates
    assert all(item["status"] in allowed for item in audit.values())
    assert all(item["note"] for item in audit.values())


def test_coverage_snapshot_is_explicitly_a_design_mapping() -> None:
    snapshot = load_registry()["coverage_snapshot"]

    assert snapshot["ledger"] == {"expressible": 118, "denominator": 145, "percent": 81.4}
    assert snapshot["ledger_l2"] == {"expressible": 35, "denominator": 39, "percent": 89.7}
    assert snapshot["v27"] == {"expressible": 603, "denominator": 741, "percent": 81.4}
    assert snapshot["status"] == "planned_mapping_not_new_method_measurement"


def test_current_method_entrypoints_repeat_the_frozen_policy() -> None:
    """公共入口不得偏离注册表契约。"""
    paths = [
        PROJECT_ROOT / "pipeline/evidence_discovery/README.md",
        PROJECT_ROOT / "pipeline/evidence_discovery/METHOD_PRINCIPLES.md",
        PROJECT_ROOT / "pipeline/evidence_discovery/REFACTOR_PLAN.md",
        PROJECT_ROOT / "pipeline/evidence_discovery/POLICY_REVIEW.md",
        PROJECT_ROOT / "discover_matrix/docs/protocol/method_provenance_policy.md",
        PROJECT_ROOT / "discover_matrix/docs/protocol/final_output_metrics_policy.md",
        PROJECT_ROOT / "pipeline/README.md",
    ]
    text = "\n".join(path.read_text(encoding="utf-8") for path in paths)

    assert "four-family-19-core.v1" in text
    assert "W1" in text and "semantic_hit" in text
    assert "W0" in text and "coverage gap" in text
    assert "UNKNOWN" in text and "violation" in text
    assert "不得新增谓词或修改" in text or "禁止新增谓词或修改" in text


def test_new_execution_boundaries_are_explicit() -> None:
    """新增硬约束必须在公共方法契约中可见，防止实现阶段静默回退。"""
    principles = (PROJECT_ROOT / "pipeline/evidence_discovery/METHOD_PRINCIPLES.md").read_text(
        encoding="utf-8"
    )
    plan = (PROJECT_ROOT / "pipeline/evidence_discovery/REFACTOR_PLAN.md").read_text(
        encoding="utf-8"
    )
    final_policy = (
        PROJECT_ROOT / "discover_matrix/docs/protocol/final_output_metrics_policy.md"
    ).read_text(encoding="utf-8")

    assert "谓词不支持不是发 issue 的资格门" in principles
    assert "不得调用 Python `inspect`" in principles
    assert "D2/D1/D0" in principles and "只有 D2 与 D1" in principles
    assert "W2/W1/W0" in principles and "确定性逻辑" in principles
    assert "方法不生成、不裁定" in principles and "台账侧属性" in principles
    assert "reason" in principles and "basis" in principles
    assert "utils.agent" in plan and "utils.llm" in plan
    assert "gpt-5.6-luna" in plan and "54 pair" in plan
    assert "audit_bundle" in plan and "编译后的 assertion/formal program" in plan
    assert "provider error" in plan and "不计费" in plan
    assert "后端禁止调用 Python `inspect`" in final_policy
    assert "方法不得生成、裁定或在 release issue 中声称自己的 `l_level`" in final_policy


def test_evidence_discovery_source_has_no_inspect_backend_dependency() -> None:
    """新正式包不得把旧 inspect 后端或 Python inspect 引入运行代码。"""
    source_root = PROJECT_ROOT / "pipeline/evidence_discovery"
    forbidden_fragments = ("import inspect", "from inspect import", "inspect_model(",
                           "inspect_fcstm(", "compact_inspect(")
    violations = []
    for path in source_root.rglob("*.py"):
        if "tests" in path.parts:
            continue
        content = path.read_text(encoding="utf-8")
        for fragment in forbidden_fragments:
            if fragment in content:
                violations.append(f"{path}: {fragment}")
    assert not violations, "new backend inspect dependency: " + "; ".join(violations)


def test_legacy_surface_is_archived_or_explicitly_replay_only() -> None:
    """历史名称只能存在于明确的归档或回放边界之后。"""
    assert not (PROJECT_ROOT / "pipeline/witness_search_prototype").exists()
    assert (PROJECT_ROOT / "pipeline/archive/witness_search_prototype_legacy_20260821").is_dir()

    pointer_targets = {
        "pipeline/archive/witness_search_prototype_legacy_20260821/ARCHIVE_NOTICE.md",
        "story/archive/legacy_20260821/blueprint_proposal.md",
        "related_work/archive/legacy_20260821/CONTINGENCY_L1.md",
        "related_work/archive/legacy_20260821/CONTINGENCY_L2.md",
        "discover_matrix/docs/protocol/archive/legacy_20260821/rules/conditional_activation.md",
        "discover_matrix/docs/protocol/archive/legacy_20260821/rulings/wellformedness_attribution.md",
        "discover_matrix/docs/protocol/archive/legacy_20260821/fused_event_policy.md",
    }
    for target in pointer_targets:
        assert (PROJECT_ROOT / target).exists(), target

    pointer_files = {
        "pipeline/feedback_loop/README.md": ("legacy", "回放"),
        "pipeline/feedback_loop/src/paper_stm_feedback_loop/discover/predicates.py":
            ("legacy", "evidence_discovery"),
        "story/blueprint_proposal.md": ("历史", "archive/legacy_20260821"),
        "related_work/CONTINGENCY_L1.md": ("归档指针", "archive/legacy_20260821"),
        "related_work/CONTINGENCY_L2.md": ("归档指针", "archive/legacy_20260821"),
        "discover_matrix/docs/protocol/rules/conditional_activation.md":
            ("归档指针", "W1"),
        "discover_matrix/docs/protocol/rulings/wellformedness_attribution.md":
            ("归档指针", "当前政策"),
        "discover_matrix/docs/protocol/fused_event_policy.md":
            ("归档指针", "event_cardinality"),
    }
    for relative, markers in pointer_files.items():
        content = (PROJECT_ROOT / relative).read_text(encoding="utf-8")
        assert all(marker in content for marker in markers), relative
