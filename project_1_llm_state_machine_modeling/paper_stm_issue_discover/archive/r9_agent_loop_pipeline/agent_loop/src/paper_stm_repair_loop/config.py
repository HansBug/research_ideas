from __future__ import annotations

from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
AGENT_LOOP_ROOT = PACKAGE_ROOT.parent
# 归档深度调整（2026-08-11）：本树从 `pipeline/agent_loop/` 迁到
# `archive/r9_agent_loop_pipeline/agent_loop/`，到 paper 根多了一层，故 `.parent` 由 2 个改为 3 个。
# 这是归档允许的唯一机械变换（见 ../../../README.md §3.6）；不改则 PAPER_ROOT 会静默解析到
# `archive/`，PAIRS_JSONL / SELECTED_ROOT 指向不存在的路径而不报错。
PAPER_ROOT = AGENT_LOOP_ROOT.parent.parent.parent
PROJECT_ROOT = PAPER_ROOT.parent
REPO_ROOT = PROJECT_ROOT.parent
PAIRS_JSONL = PAPER_ROOT / "corpora/seed_library/llms-emp-stm-subset/assets/extracted/pairs.jsonl"
SELECTED_ROOT = PAPER_ROOT / "selected_seed_examples"

LANGUAGES = ("zh-CN", "en-US")
