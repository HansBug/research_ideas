"""Standalone provider-free smoke test shipped with the method release."""

from __future__ import annotations

from pathlib import Path

from paper_stm_method.inputs import parse_fcstm
from paper_stm_method.registry import load_registry
from paper_stm_method.orchestration import runner


def test_packaged_resources_and_synthetic_fcstm_fixture_load_without_provider() -> None:
    """The released package loads its registry and a minimal FCSTM fixture offline."""

    registry = load_registry()
    source = (Path(__file__).parent / "fixtures" / "minimal.fcstm").read_text(
        encoding="utf-8"
    )
    model = parse_fcstm(source)

    assert registry.registry_hash == "sha256:38fa2e8060ff822836a3e6437a271998690d36cf60822053316eb21cda2015ca"
    assert {state.name for state in model.states} >= {"Root", "Idle", "Active"}


def test_release_provenance_fallback_requires_an_explicit_manifest_commit(monkeypatch) -> None:
    """An extracted package stays fail-closed unless its release commit is explicit."""

    monkeypatch.setattr(runner, "_git_source_provenance", lambda: None)
    monkeypatch.delenv("PAPER_STM_RELEASE_SOURCE_COMMIT", raising=False)
    assert runner._source_provenance()["source_commit"] == "unknown"

    monkeypatch.setenv("PAPER_STM_RELEASE_SOURCE_COMMIT", "a" * 40)
    provenance = runner._source_provenance()
    assert provenance["source_commit"] == "a" * 40
    assert provenance["source_branch"] == "release-package"
    assert provenance["source_dirty"] is False
