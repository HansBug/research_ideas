"""Provider-free smoke test shipped with the standalone Semantic Judge release."""

from __future__ import annotations

import sys

import pytest

from paper_stm_judge import cli
from paper_stm_judge.protocol import verify_snapshot
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
