from pathlib import Path


def test_readme_describes_the_current_public_contract() -> None:
    text = Path("utils/README.md").read_text(encoding="utf-8")
    for required in (
        "LLMConfig",
        "LLMRegistry",
        "AgentApp",
        "AgentSpec",
        "context_rollover",
        "audit_out",
        "result_out",
        "academic_eligible",
        "reasoning_summary",
        "python -m utils.agent.demo",
    ):
        assert required in text
    for forbidden in ("schema_version", "events_out", "RunLimits", "ToolPolicy"):
        assert forbidden not in text
