"""Run in the remote Muse env with E1_MUSE_TOKENIZER pointing at its cached snapshot."""
import copy
import importlib.util
import json
import os
from pathlib import Path

import pytest


def test_muse_native_xml_schema_and_stream_parser():
    xgrammar = pytest.importorskip("xgrammar", reason="Requires the remote Muse serving environment")
    pytest.importorskip("sglang", reason="Requires the remote Muse serving environment")
    from sglang.srt.entrypoints.openai.protocol import Tool
    from sglang.srt.function_call.muse_glimmer_detector import MuseGlimmerDetector
    from transformers import AutoTokenizer

    module_path = Path(os.environ.get("E1_MUSE_ADAPTER", Path(__file__).parents[2] / "utils/llm/serving_muse.py"))
    spec = importlib.util.spec_from_file_location("serving_muse", module_path)
    adapter = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(adapter)
    schema = {"type": "object", "additionalProperties": False, "properties": {
        "decisions": {"type": "array", "items": {"type": "object", "additionalProperties": False,
            "properties": {"kind": {"type": "string", "enum": ["unresolved"]}}, "required": ["kind"]}},
        "reason": {"type": "string", "minLength": 1}, "basis": {"type": "string", "minLength": 1}},
        "required": ["reason", "basis"]}
    tools = [{"type": "function", "function": {"name": "Assessment", "description": "Assessment", "parameters": schema}}]
    original = copy.deepcopy(tools)
    tag = adapter.muse_structural_tag(tools, "required")
    assert tools == original
    tokenizer = AutoTokenizer.from_pretrained(os.environ["E1_MUSE_TOKENIZER"], local_files_only=True)
    compiled = xgrammar.GrammarCompiler(xgrammar.TokenizerInfo.from_huggingface(tokenizer)).compile_structural_tag(json.dumps(tag))
    prefix = '<|start|>assistant to=Assessment<|message|><atem:function_calls>\n<atem:invoke name="Assessment">\n'
    suffix = '</atem:invoke>\n</atem:function_calls>'
    params = '<atem:parameter name="decisions">[{"kind":"unresolved"}]</atem:parameter>\n<atem:parameter name="reason">Undecidable</atem:parameter>\n<atem:parameter name="basis">Dossier</atem:parameter>\n'
    valid = prefix + params + suffix
    cases = [(valid, True), (valid.replace('"unresolved"', '"invented"'), False),
             (valid.replace('<atem:parameter name="basis">Dossier</atem:parameter>\n', ''), False),
             (valid.replace('Dossier</atem:parameter>', '</atem:parameter>'), False)]
    for text, expected in cases:
        matcher = xgrammar.GrammarMatcher(compiled)
        accepted = matcher.accept_string(text) and matcher.accept_token(tokenizer.eos_token_id)
        assert accepted is expected
    matcher = xgrammar.GrammarMatcher(compiled)
    assert all(matcher.accept_token(token) for token in tokenizer.encode(valid, add_special_tokens=False))
    for chunk_size in (1, 7, len(valid)):
        parser, calls = MuseGlimmerDetector(), []
        for offset in range(0, len(valid), chunk_size):
            calls.extend(parser.parse_streaming_increment(valid[offset:offset+chunk_size], [Tool.model_validate(tools[0])]).calls)
        calls.extend(parser.finish([Tool.model_validate(tools[0])]).calls)
        assert len(calls) == 1
        assert json.loads(calls[0].parameters) == {"decisions": [{"kind": "unresolved"}], "reason": "Undecidable", "basis": "Dossier"}
    adapter.install()
    assert MuseGlimmerDetector().get_structural_tag([Tool.model_validate(tools[0])], "auto") is None
