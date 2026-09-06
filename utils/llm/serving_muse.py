"""SGLang 0.5.19 launcher with schema-constrained native Muse ATEM tool calls.

Run only inside the model's remote conda environment. The upstream detector
parses required calls natively but supplies no decoding grammar. This adapter
uses XGrammar's existing XML parameter compiler, with Muse's ATEM namespace.
It leaves the model template, reasoning parser and caller schemas unchanged.
"""
import json
import runpy


def muse_structural_tag(tools, tool_choice):
    from xgrammar import Grammar

    choices = []
    for tool in tools:
        function = tool["function"]
        if isinstance(tool_choice, dict) and tool_choice["function"]["name"] != function["name"]:
            continue
        schema = function["parameters"]
        serialized = json.dumps(schema)
        if "<parameter" in serialized or "</parameter>" in serialized:
            raise ValueError("Schema literals conflict with XML grammar namespace conversion")
        grammar = str(Grammar.from_structural_tag(json.dumps({"type": "structural_tag", "format": {
            "type": "json_schema", "json_schema": schema, "style": "minimax_xml"}})))
        # The native compiler has no XML namespace option; convert only its tag literals.
        grammar = grammar.replace("<parameter name=", "<atem:parameter name=").replace("</parameter>", "</atem:parameter>")
        name = function["name"]
        body = {"type": "tag", "begin": '<atem:invoke name="' + name + '">',
                "content": {"type": "grammar", "grammar": grammar}, "end": "</atem:invoke>"}
        choices.append({"type": "sequence", "elements": [
            {"type": "or", "elements": [
                {"type": "const_string", "value": prefix + name + "<|message|>"}
                for prefix in (" to=", "<|start|>assistant to=")]},
            {"type": "regex", "pattern": r"\s*"},
            {"type": "tag", "begin": "<atem:function_calls>", "content": {
                "type": "sequence", "elements": [{"type": "regex", "pattern": r"\s*"}, body,
                                               {"type": "regex", "pattern": r"\s*"}]},
             "end": "</atem:function_calls>"},
            {"type": "regex", "pattern": r"\s*"}]})
    if not choices:
        raise ValueError("A required Muse tool must be present in the supplied tool list")
    return {"type": "structural_tag", "format": {"type": "or", "elements": choices}}


def install():
    from importlib.metadata import version

    from sglang.srt.function_call.muse_glimmer_detector import MuseGlimmerDetector
    from xgrammar import StructuralTag

    if version("sglang") != "0.5.19":
        raise RuntimeError("Revalidate the Muse serving adapter before changing SGLang 0.5.19")

    def get_structural_tag(self, tools=None, tool_choice="auto", thinking_mode=False, parallel_tool_calls=True):
        if not tools or tool_choice in ("auto", "none"):
            return None
        if thinking_mode:
            raise ValueError("Use --reasoning-parser muse to own the reasoning prefix")
        choice = tool_choice if isinstance(tool_choice, str) else tool_choice.model_dump()
        return StructuralTag.model_validate(muse_structural_tag([tool.model_dump() for tool in tools], choice))

    MuseGlimmerDetector.get_structural_tag = get_structural_tag


if __name__ == "__main__":
    install()
    runpy.run_module("sglang.launch_server", run_name="__main__")
