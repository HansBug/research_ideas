from __future__ import annotations

import hashlib
import re
import subprocess
from pathlib import Path

from paper_stm_repair_loop import inputs


_HEX_64 = re.compile(r"^[0-9a-f]{64}$")


def _git(repo: Path, *args: str) -> str:
    return subprocess.run(
        ["git", *args],
        cwd=repo,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def _git_bytes(repo: Path, *args: str) -> bytes:
    return subprocess.run(
        ["git", *args],
        cwd=repo,
        check=True,
        capture_output=True,
    ).stdout


def _init_repo(repo: Path) -> str:
    _git(repo, "init")
    _git(repo, "config", "user.email", "test@example.invalid")
    _git(repo, "config", "user.name", "Provenance Test")
    (repo / "src.py").write_text("print('tracked')\n", encoding="utf-8")
    _git(repo, "add", "src.py")
    _git(repo, "commit", "-m", "init")
    return _git(repo, "rev-parse", "HEAD")


def test_code_provenance_records_sorted_non_run_untracked_without_run_outputs(tmp_path, monkeypatch):
    repo = tmp_path / "repo"
    repo.mkdir()
    commit = _init_repo(repo)
    (repo / "runs").mkdir()
    (repo / "runs" / "run-output.json").write_text("{}\n", encoding="utf-8")
    (repo / "zeta.txt").write_text("z\n", encoding="utf-8")
    (repo / "alpha name.txt").write_text("a\n", encoding="utf-8")
    (repo / "line\nbreak.txt").write_text("safe\n", encoding="utf-8")
    (repo / "linked.txt").symlink_to("zeta.txt")

    monkeypatch.setattr(inputs, "REPO_ROOT", repo)

    provenance = inputs._code_provenance()

    assert provenance["status"] == "completed"
    assert provenance["git_commit"] == commit
    assert provenance["tracked_worktree_dirty"] is False
    assert provenance["tracked_dirty_paths"] == []
    assert provenance["tracked_dirty_count"] == 0
    assert provenance["tracked_dirty_paths_sha256"] == inputs._hash_paths([])
    assert provenance["canonical_git_diff_binary_head_sha256"] == hashlib.sha256(
        b""
    ).hexdigest()
    assert provenance["canonical_git_diff_binary_head_empty"] is True
    assert provenance["reproducible_tracked_head"] == commit
    assert provenance["code_state_reproducible"] is False
    assert provenance["reproducible_code_head"] is None
    assert provenance["untracked_run_outputs_excluded"] is True
    assert provenance["excluded_pathspecs"] == ["runs/**"]
    assert provenance["non_run_untracked_paths"] == [
        "alpha name.txt",
        "line\nbreak.txt",
        "linked.txt",
        "zeta.txt",
    ]
    assert provenance["non_run_untracked_count"] == 4
    assert provenance["non_run_untracked_paths_sha256"] == inputs._hash_paths(
        ["alpha name.txt", "line\nbreak.txt", "linked.txt", "zeta.txt"]
    )
    assert _HEX_64.match(provenance["non_run_untracked_paths_sha256"])
    manifest = provenance["non_run_untracked_content_manifest"]
    assert [item["path"] for item in manifest] == provenance["non_run_untracked_paths"]
    assert manifest[0] == {
        "path": "alpha name.txt",
        "file_type": "regular_file",
        "git_mode": "100644",
        "lstat_mode_octal": "0644",
        "size_bytes": 2,
        "content_sha256": hashlib.sha256(b"a\n").hexdigest(),
        "symlink_target": None,
    }
    linked = {item["path"]: item for item in manifest}["linked.txt"]
    assert linked["file_type"] == "symlink"
    assert linked["git_mode"] == "120000"
    assert linked["content_sha256"] == hashlib.sha256(b"zeta.txt").hexdigest()
    assert linked["symlink_target"] == "zeta.txt"
    assert provenance["non_run_untracked_content_manifest_sha256"] == inputs._hash_json(
        manifest
    )
    assert provenance["non_run_untracked_content_complete"] is True

    old_manifest_sha = provenance["non_run_untracked_content_manifest_sha256"]
    (repo / "alpha name.txt").write_text("changed\n", encoding="utf-8")
    changed = inputs._code_provenance()
    assert changed["non_run_untracked_paths_sha256"] == provenance[
        "non_run_untracked_paths_sha256"
    ]
    assert changed["non_run_untracked_content_manifest_sha256"] != old_manifest_sha


def test_code_provenance_ignores_only_runs_untracked_when_code_clean(tmp_path, monkeypatch):
    repo = tmp_path / "repo"
    repo.mkdir()
    commit = _init_repo(repo)
    (repo / "runs" / "paper1").mkdir(parents=True)
    (repo / "runs" / "paper1" / "manifest.json").write_text("{}\n", encoding="utf-8")

    monkeypatch.setattr(inputs, "REPO_ROOT", repo)

    provenance = inputs._code_provenance()

    assert provenance["status"] == "completed"
    assert provenance["tracked_worktree_dirty"] is False
    assert provenance["tracked_dirty_paths"] == []
    assert provenance["tracked_dirty_count"] == 0
    assert provenance["tracked_dirty_paths_sha256"] == inputs._hash_paths([])
    assert provenance["canonical_git_diff_binary_head_sha256"] == hashlib.sha256(
        b""
    ).hexdigest()
    assert provenance["canonical_git_diff_binary_head_empty"] is True
    assert provenance["reproducible_tracked_head"] == commit
    assert provenance["code_state_reproducible"] is True
    assert provenance["reproducible_code_head"] == commit
    assert provenance["non_run_untracked_paths"] == []
    assert provenance["non_run_untracked_count"] == 0
    assert provenance["non_run_untracked_paths_sha256"] == inputs._hash_paths([])
    assert provenance["non_run_untracked_content_manifest"] == []
    assert provenance["non_run_untracked_content_manifest_sha256"] == inputs._hash_json([])
    assert provenance["non_run_untracked_content_complete"] is True


def test_code_provenance_marks_only_non_run_tracked_dirty(tmp_path, monkeypatch):
    repo = tmp_path / "repo"
    repo.mkdir()
    _init_repo(repo)
    (repo / "runs").mkdir()
    (repo / "runs" / "run-output.json").write_text("{}\n", encoding="utf-8")
    (repo / "src.py").write_text("print('dirty')\n", encoding="utf-8")

    monkeypatch.setattr(inputs, "REPO_ROOT", repo)

    provenance = inputs._code_provenance()

    assert provenance["status"] == "completed"
    assert provenance["tracked_worktree_dirty"] is True
    assert provenance["tracked_dirty_paths"] == ["src.py"]
    assert provenance["tracked_dirty_count"] == 1
    assert provenance["tracked_dirty_paths_sha256"] == inputs._hash_paths(["src.py"])
    canonical_diff = _git_bytes(
        repo, "diff", "--binary", "HEAD", "--", ".", ":(exclude)runs/**"
    )
    assert _HEX_64.match(provenance["canonical_git_diff_binary_head_sha256"])
    assert provenance["canonical_git_diff_binary_head_sha256"] == hashlib.sha256(
        canonical_diff
    ).hexdigest()
    assert provenance["canonical_git_diff_binary_head_sha256"] != hashlib.sha256(
        b""
    ).hexdigest()
    assert provenance["canonical_git_diff_binary_head_empty"] is False
    assert provenance["reproducible_tracked_head"] is None
    assert provenance["code_state_reproducible"] is False
    assert provenance["reproducible_code_head"] is None
    assert provenance["non_run_untracked_paths"] == []
    assert provenance["non_run_untracked_count"] == 0
    assert provenance["non_run_untracked_paths_sha256"] == inputs._hash_paths([])


def test_code_provenance_excludes_tracked_runs_diff_from_clean_claim(tmp_path, monkeypatch):
    repo = tmp_path / "repo"
    repo.mkdir()
    commit = _init_repo(repo)
    (repo / "runs" / "paper1").mkdir(parents=True)
    (repo / "runs" / "paper1" / "tracked.json").write_text("{}\n", encoding="utf-8")
    _git(repo, "add", "runs/paper1/tracked.json")
    _git(repo, "commit", "-m", "add tracked run output")
    commit = _git(repo, "rev-parse", "HEAD")
    (repo / "runs" / "paper1" / "tracked.json").write_text(
        "{\"dirty\": true}\n", encoding="utf-8"
    )

    monkeypatch.setattr(inputs, "REPO_ROOT", repo)

    provenance = inputs._code_provenance()

    assert provenance["status"] == "completed"
    assert provenance["git_commit"] == commit
    assert provenance["tracked_worktree_dirty"] is False
    assert provenance["tracked_dirty_paths"] == []
    assert provenance["tracked_dirty_count"] == 0
    assert provenance["tracked_dirty_paths_sha256"] == inputs._hash_paths([])
    assert provenance["canonical_git_diff_binary_head_sha256"] == hashlib.sha256(
        b""
    ).hexdigest()
    assert provenance["canonical_git_diff_binary_head_empty"] is True
    assert provenance["reproducible_tracked_head"] == commit
    assert provenance["code_state_reproducible"] is True
    assert provenance["reproducible_code_head"] == commit


def test_code_provenance_unavailable_branch_keeps_stable_fields(tmp_path, monkeypatch):
    bad_repo = tmp_path / "not-a-repo"
    bad_repo.mkdir()
    monkeypatch.setattr(inputs, "REPO_ROOT", bad_repo)

    provenance = inputs._code_provenance()

    assert provenance == {
        "status": "unavailable",
        "git_commit": None,
        "git_branch": None,
        "tracked_worktree_dirty": None,
        "tracked_dirty_paths": [],
        "tracked_dirty_count": None,
        "tracked_dirty_paths_sha256": None,
        "canonical_git_diff_binary_head_sha256": None,
        "canonical_git_diff_binary_head_empty": None,
        "reproducible_tracked_head": None,
        "code_state_reproducible": None,
        "reproducible_code_head": None,
        "non_run_untracked_paths": [],
        "non_run_untracked_count": None,
        "non_run_untracked_paths_sha256": None,
        "non_run_untracked_content_manifest": [],
        "non_run_untracked_content_manifest_sha256": None,
        "non_run_untracked_content_complete": None,
        "untracked_run_outputs_excluded": True,
        "excluded_pathspecs": ["runs/**"],
        "reason": "CalledProcessError",
    }
