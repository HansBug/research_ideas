from __future__ import annotations

from pathlib import Path

from utils.agent import AgentApp, AgentError, AgentEvent, AgentRunResult, AgentSpec
from utils.agent import __all__ as agent_public
from utils.llm import LLMConfig, LLMRegistry, load_llm_registry
from utils.llm import __all__ as llm_public


def test_public_exports_and_readme_contract_stay_aligned() -> None:
    assert agent_public == ["AgentApp", "AgentError", "AgentEvent", "AgentRunResult", "AgentSpec"]
    assert llm_public == ["LLMConfig", "LLMRegistry", "load_llm_registry"]

    readme = Path("utils/README.md").read_text(encoding="utf-8")
    for required in (
        "from utils.agent import AgentApp, AgentError, AgentEvent, AgentRunResult, AgentSpec",
        "from utils.llm import LLMConfig, LLMRegistry, load_llm_registry",
        "python -m utils.agent.demo",
        "python -m utils.llm validate",
        "model_started",
        "tool_completed",
        "structured_output",
        "academic_eligible",
        "audit_out",
        "result_out",
    ):
        assert required in readme


def test_utils_sources_do_not_import_paper1_modules() -> None:
    source = "\n".join(path.read_text(encoding="utf-8") for path in Path("utils").rglob("*.py"))
    assert "project_1" not in source
    assert "project_ex1" not in source
