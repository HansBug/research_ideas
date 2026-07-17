from __future__ import annotations

from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
AGENT_LOOP_ROOT = PACKAGE_ROOT.parent
PAPER_ROOT = AGENT_LOOP_ROOT.parent.parent
PROJECT_ROOT = PAPER_ROOT.parent
REPO_ROOT = PROJECT_ROOT.parent
PAIRS_JSONL = PAPER_ROOT / "corpora/seed_library/llms-emp-stm-subset/assets/extracted/pairs.jsonl"
SELECTED_ROOT = PAPER_ROOT / "selected_seed_examples"

LANGUAGES = ("zh-CN", "en-US")
