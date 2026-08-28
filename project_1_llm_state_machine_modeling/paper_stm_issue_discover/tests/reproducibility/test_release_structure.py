"""Provider-free regression tests for the paper1 release boundary."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


REPOSITORY = Path(__file__).resolve().parents[4]
SCRIPT = REPOSITORY / "project_1_llm_state_machine_modeling/paper_stm_issue_discover/scripts/release/validate_release_structure.py"


def _module():
    """Load the release validator by path without invoking its CLI."""

    specification = importlib.util.spec_from_file_location("release_structure_validator", SCRIPT)
    assert specification and specification.loader
    module = importlib.util.module_from_spec(specification)
    sys.modules[specification.name] = module
    specification.loader.exec_module(module)
    return module


def test_release_validator_preserves_frozen_archive_nodes_resources_and_boundaries() -> None:
    """The committed release structure retains frozen bytes and the 465-node universe."""

    result = _module().validate(REPOSITORY, REPOSITORY / "venv/bin/python")
    assert result.frozen_archive_files_checked == 2671
    assert (result.baseline_node_count, result.current_node_count) == (465, 465)
    assert result.resource_hashes["registry"] == "sha256:38fa2e8060ff822836a3e6437a271998690d36cf60822053316eb21cda2015ca"
    assert result.resource_hashes["judge_protocol"] == "sha256:d774d9bd3e4c4fe04735ed1d4ec064be197cfadcd52e21c8226e37175b29b210"
    assert result.boundary_violations == ()
    assert result.provider_call_count == result.billable_call_count == 0
