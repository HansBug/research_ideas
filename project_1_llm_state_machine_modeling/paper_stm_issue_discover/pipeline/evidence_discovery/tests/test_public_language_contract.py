"""Provider-free checks for the public method language contract."""

from __future__ import annotations

import importlib
import json
import pkgutil
import re
from pathlib import Path
from types import ModuleType
from typing import Any

from pydantic import BaseModel

from pipeline import evidence_discovery
from pipeline.evidence_discovery.inputs import load_pair
from pipeline.evidence_discovery.inputs.context import prompt_context_payload

METHOD_ROOT = Path(evidence_discovery.__file__).resolve().parent
METHOD_SOURCE_ROOT = (
    METHOD_ROOT.parents[1] / "method/src/paper_stm_method"
)
REPORT_ROOT = METHOD_ROOT.parent / "representation/reports/llms_emp_r45_java_60"
HAN_TEXT = re.compile(r"[\u3400-\u9fff]")
INTERNAL_ALIAS_PATTERNS = (
    re.compile(r"(?i)(?<![A-Za-z0-9])paper[ _-]*[0-9]+(?![A-Za-z0-9])"),
    re.compile(r"(?i)(?<![A-Za-z0-9])[xy][0-9]+v[0-9]+(?![A-Za-z0-9])"),
    re.compile(r"(?i)(?<![A-Za-z0-9.])v[0-9]{2,}(?![A-Za-z0-9.])"),
    re.compile(r"(?i)\b(?:issue|pr|pull[ _-]?request)\s*#\s*[0-9]+\b"),
    re.compile(r"(?i)\b(?:six|five|three)[ _-]pair(?:s|[ _-]set)?\b"),
)


def _public_modules() -> list[ModuleType]:
    modules: list[ModuleType] = [importlib.import_module("paper_stm_method")]
    for module_info in pkgutil.walk_packages(
        [str(METHOD_SOURCE_ROOT)], "paper_stm_method."
    ):
        if ".tests" in module_info.name:
            continue
        modules.append(importlib.import_module(module_info.name))
    for shared_module in (
        "utils.stm_artifacts",
        "utils.stm_artifacts.context",
        "utils.stm_artifacts.fcstm_native_projection",
        "utils.stm_artifacts.loaders",
        "utils.stm_artifacts.models",
        "utils.structured_runtime",
    ):
        modules.append(importlib.import_module(shared_module))
    return modules


def _method_models(modules: list[ModuleType]) -> list[type[BaseModel]]:
    models: dict[tuple[str, str], type[BaseModel]] = {}
    for module in modules:
        for value in vars(module).values():
            if (
                isinstance(value, type)
                and issubclass(value, BaseModel)
                and value is not BaseModel
                and value.__module__.startswith(
                    ("paper_stm_method", "utils.stm_artifacts", "utils.structured_runtime")
                )
            ):
                models[(value.__module__, value.__qualname__)] = value
    return [models[key] for key in sorted(models)]


def _internal_aliases(text: str) -> list[str]:
    return [match.group(0) for pattern in INTERNAL_ALIAS_PATTERNS for match in pattern.finditer(text)]


def _description_values(value: Any) -> list[str]:
    descriptions: list[str] = []
    if isinstance(value, dict):
        for key, nested in value.items():
            if key == "description" and isinstance(nested, str):
                descriptions.append(nested)
            descriptions.extend(_description_values(nested))
    elif isinstance(value, list):
        for nested in value:
            descriptions.extend(_description_values(nested))
    return descriptions


def test_production_source_and_registry_use_public_english_terminology() -> None:
    violations: list[str] = []
    for path in sorted((*METHOD_SOURCE_ROOT.rglob("*.py"), *METHOD_SOURCE_ROOT.rglob("*.json"))):
        # Archive labels and provenance identifiers are not method public language.
        if (
            "tests" in path.parts
            or "reporting" in path.parts
            or path.name == "current_source_catalog.json"
        ):
            continue
        text = path.read_text(encoding="utf-8")
        if HAN_TEXT.search(text):
            violations.append(f"{path.relative_to(METHOD_SOURCE_ROOT)}: contains Han text")
        aliases = _internal_aliases(text)
        if aliases:
            violations.append(
                f"{path.relative_to(METHOD_SOURCE_ROOT)}: internal aliases {sorted(set(aliases))}"
            )
    assert not violations, "public method language violations:\n" + "\n".join(violations)


def test_active_method_documents_do_not_expose_internal_aliases() -> None:
    violations: list[str] = []
    for path in (METHOD_ROOT / "METHOD_PRINCIPLES.md", METHOD_ROOT / "README.md"):
        aliases = _internal_aliases(path.read_text(encoding="utf-8"))
        if aliases:
            violations.append(f"{path.name}: internal aliases {sorted(set(aliases))}")
    assert not violations, "public method documentation violations:\n" + "\n".join(violations)


def test_runtime_prompt_constants_require_english_public_output() -> None:
    prompt_rows: list[tuple[str, str]] = []
    for module in _public_modules():
        for name, value in vars(module).items():
            if "PROMPT" in name and isinstance(value, str) and "prompt" not in name.lower().removesuffix("_prompt"):
                prompt_rows.append((f"{module.__name__}.{name}", value))

    assert prompt_rows
    violations: list[str] = []
    generated_output_prompts = 0
    for name, prompt in prompt_rows:
        if HAN_TEXT.search(prompt):
            violations.append(f"{name}: contains Han text")
        aliases = _internal_aliases(prompt)
        if aliases:
            violations.append(f"{name}: internal aliases {sorted(set(aliases))}")
        if "SYSTEM_PROMPT" in name:
            generated_output_prompts += 1
            if "in English" not in prompt:
                violations.append(f"{name}: missing English-output instruction")
    assert generated_output_prompts >= 3
    assert not violations, "runtime prompt language violations:\n" + "\n".join(violations)


def test_real_provider_contexts_do_not_expose_internal_aliases() -> None:
    violations: list[str] = []
    for pair_id in ("0000", "0029", "0046", "0053"):
        pair = load_pair(REPORT_ROOT / "pairs" / pair_id)
        for stage in (
            "nl_contract_extraction",
            "discovery_grounding",
            "d_adjudication",
        ):
            serialized = json.dumps(
                prompt_context_payload(pair, stage=stage),
                ensure_ascii=False,
                sort_keys=True,
            )
            aliases = _internal_aliases(serialized)
            if aliases:
                violations.append(
                    f"{pair_id}/{stage}: internal aliases {sorted(set(aliases))}"
                )
    assert not violations, "provider context language violations:\n" + "\n".join(
        violations
    )


def test_all_method_models_project_english_docstrings_and_field_descriptions() -> None:
    models = _method_models(_public_modules())
    assert len(models) >= 90
    violations: list[str] = []
    for model in models:
        model_name = f"{model.__module__}.{model.__qualname__}"
        docstring = model.__dict__.get("__doc__")
        if not isinstance(docstring, str) or not docstring.strip():
            violations.append(f"{model_name}: missing explicit class docstring")
        elif HAN_TEXT.search(docstring) or _internal_aliases(docstring):
            violations.append(f"{model_name}: non-public class docstring")

        for field_name, field in model.model_fields.items():
            description = field.description
            if not isinstance(description, str) or not description.strip():
                violations.append(f"{model_name}.{field_name}: missing Field description")
            elif HAN_TEXT.search(description) or _internal_aliases(description):
                violations.append(f"{model_name}.{field_name}: non-public Field description")

        schema = model.model_json_schema()
        if not schema.get("description"):
            violations.append(f"{model_name}: class docstring missing from model_json_schema()")
        for description in _description_values(schema):
            if HAN_TEXT.search(description) or _internal_aliases(description):
                violations.append(f"{model_name}: non-public runtime schema description")
                break

        serialized_schema = json.dumps(schema, ensure_ascii=False, sort_keys=True)
        if HAN_TEXT.search(serialized_schema) or _internal_aliases(serialized_schema):
            violations.append(f"{model_name}: non-public provider schema projection")

    assert not violations, "Pydantic public-language violations:\n" + "\n".join(violations)


def test_method_principles_freeze_the_public_language_contract() -> None:
    principles = (METHOD_ROOT / "METHOD_PRINCIPLES.md").read_text(encoding="utf-8")
    for required in (
        "Public implementation language",
        "provider prompts",
        "Pydantic class docstrings",
        "production class/function/variable names",
        "generated explanations",
        "deterministic audit prose",
        "Exact source quotations",
        "must be English",
        "Provider-free tests",
    ):
        assert required in principles
