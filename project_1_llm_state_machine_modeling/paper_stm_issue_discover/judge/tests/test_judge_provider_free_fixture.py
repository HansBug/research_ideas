"""Provider-free smoke test shipped with the standalone Semantic Judge release."""

from __future__ import annotations

import sys

import pytest

from paper_stm_judge import cli
from paper_stm_judge.models import FrozenValidityCertificate, ValidityResponse
from paper_stm_judge.protocol import (
    JUDGE_ALGORITHM_VERSION,
    PROMPT_VERSION,
    PROTOCOL_VERSION,
    VALIDITY_SYSTEM_PROMPT,
    verify_snapshot,
)
from paper_stm_judge.scale_audit import _algorithm_source_hash


def test_packaged_protocol_and_neutral_dependencies_load_without_method() -> None:
    """The independent Judge verifies its frozen protocol without importing method code."""

    method_modules_before = {
        name for name in sys.modules if name == "paper_stm_method" or name.startswith("paper_stm_method.")
    }
    verify_snapshot()
    assert _algorithm_source_hash().startswith("sha256:")
    method_modules_after = {
        name for name in sys.modules if name == "paper_stm_method" or name.startswith("paper_stm_method.")
    }
    assert method_modules_after == method_modules_before


def test_release_code_provenance_fails_closed_without_git_or_manifest(monkeypatch) -> None:
    """A source-less Judge cannot begin a live run without verified package provenance."""

    monkeypatch.setattr(cli, "_source_repository_root", lambda: None)
    monkeypatch.setattr(cli, "_release_source_commit", lambda: None)
    with pytest.raises(RuntimeError, match="valid installed release manifest"):
        cli._code_commit()


def test_release_code_provenance_accepts_verified_embedded_manifest(monkeypatch) -> None:
    """A verified installed manifest supplies the exact Judge code commit offline."""

    commit = "a" * 40
    monkeypatch.setattr(cli, "_source_repository_root", lambda: None)
    monkeypatch.setattr(cli, "_release_source_commit", lambda: commit)
    assert cli._code_commit() == commit


def test_v33_closes_d0_and_a0_to_invalid_without_a_scope_exit() -> None:
    """The current prompt makes obligation and author-source truth explicit gates."""

    assert PROTOCOL_VERSION.endswith("issue-189-clarification.v3.3")
    assert JUDGE_ALGORITHM_VERSION == "semantic-judge.two-stage.v3.3"
    assert PROMPT_VERSION == "semantic-judge.two-stage-prompt.v7"
    assert "A true author-source observation without a surviving violated obligation is D0" in VALIDITY_SYSTEM_PROMPT
    assert "Both D0 and A0 therefore become INVALID" in VALIDITY_SYSTEM_PROMPT
    assert "The X1v2 baseline has no such representation-debt subtype" in VALIDITY_SYSTEM_PROMPT
    assert "every other unsupported or false author-source attribution as FALSE_POSITIVE" in VALIDITY_SYSTEM_PROMPT
    assert "cannot invalidate an otherwise author-source-supported D2/D1 defect claim" in VALIDITY_SYSTEM_PROMPT


def test_minimum_evidence_schema_carries_the_d_a_boundary() -> None:
    """Pydantic descriptions enter the provider schema and preserve the D/A contract."""

    response_description = ValidityResponse.model_fields[
        "minimum_evidence_gate"
    ].description
    frozen_description = FrozenValidityCertificate.model_fields[
        "minimum_evidence_gate"
    ].description
    assert response_description is not None
    assert "true of the author-source work product" in response_description
    assert "D0" in response_description and "A0" in response_description
    assert frozen_description is not None
    assert "D0 and A0 are REFUTED" in frozen_description
