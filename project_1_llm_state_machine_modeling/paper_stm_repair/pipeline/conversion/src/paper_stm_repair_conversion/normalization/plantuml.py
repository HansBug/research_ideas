from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, field
from typing import Any

RULES: dict[str, dict[str, Any]] = {
    "PUML.NORM.alias_multiword_endpoint": {
        "semantic_risk": "low_medium",
        "risk_tier": "low_risk",
        "main_eligibility_default": True,
        "description": "对未加引号且含空格的 transition endpoint 生成 PlantUML state alias。",
    },
    "PUML.NORM.alias_quoted_endpoint": {
        "semantic_risk": "low_medium",
        "risk_tier": "low_risk",
        "main_eligibility_default": True,
        "description": "对 quoted transition endpoint 生成 PlantUML state alias，保留显示 label。",
    },
    "PUML.NORM.alias_embedded_pseudostate_marker": {
        "semantic_risk": "high",
        "risk_tier": "high_risk",
        "main_eligibility_default": False,
        "description": "对含有内嵌 [*] 伪状态标记的 endpoint 生成 alias；可能把初始/终止伪状态误降级为普通状态名。",
    },
    "PUML.NORM.transition_when_label": {
        "semantic_risk": "low_medium",
        "risk_tier": "low_risk",
        "main_eligibility_default": True,
        "description": "将 transition target 后的 `when : guard` 伪语法规范化为 PlantUML label，并保留 when 线索。",
    },
    "PUML.NORM.remove_empty_transition_label": {
        "semantic_risk": "low",
        "risk_tier": "low_risk",
        "main_eligibility_default": True,
        "description": "删除 transition 末尾空 label 冒号。",
    },
    "PUML.NORM.alias_bracket_endpoint": {
        "semantic_risk": "low_medium",
        "risk_tier": "low_risk",
        "main_eligibility_default": True,
        "description": "对非 [*] 的 bracket endpoint 生成 PlantUML state alias，保留显示 label。",
    },
    "PUML.NORM.remove_stm_heading": {
        "semantic_risk": "medium",
        "risk_tier": "low_risk",
        "main_eligibility_default": True,
        "description": "注释非 PlantUML 的 stm heading，不改变状态/迁移主体。",
    },
    "PUML.NORM.stm_block_to_state": {
        "semantic_risk": "medium_high",
        "risk_tier": "high_risk",
        "main_eligibility_default": False,
        "description": "将 stm X { 近似转换为 PlantUML state block。",
    },
    "PUML.NORM.comment_orphan_when": {
        "semantic_risk": "high",
        "risk_tier": "high_risk",
        "main_eligibility_default": False,
        "description": "注释无法归属 transition 的 when 行；可能丢失 guard。",
    },
    "PUML.NORM.comment_dependency_arrow": {
        "semantic_risk": "medium_high",
        "risk_tier": "high_risk",
        "main_eligibility_default": False,
        "description": "注释 dependency-like 虚线箭头；可能丢失结构关系。",
    },
    "PUML.NORM.entry_do_exit_rewrite_or_loss": {
        "semantic_risk": "medium_high",
        "risk_tier": "high_risk",
        "main_eligibility_default": False,
        "description": "注释 PlantUML state action 行；可能丢失 entry/do/exit action。",
    },
    "PUML.NORM.fork_join_decl_to_state": {
        "semantic_risk": "high",
        "risk_tier": "high_risk",
        "main_eligibility_default": False,
        "description": "将 fork/join pseudo-state declaration 降级为普通 state declaration。",
    },
}

ARROW_TOKENS = ["-right->", "-left->", "-down->", "-up->", "-->", "->"]
UNSUPPORTED_ARROW_TOKENS = ["<-->", "<->", "<--", "<-", "<..", "..>"]
SIMPLE_ID_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_$.]*$")
STATE_AS_RE = re.compile(r'^\s*state\s+"(?P<label>[^"]+)"\s+as\s+(?P<alias>[A-Za-z_][A-Za-z0-9_]*)')
STM_BLOCK_RE = re.compile(r"^(?P<indent>\s*)stm\s+(?P<name>.+?)\s*\{\s*$", re.IGNORECASE)
STM_HEADING_RE = re.compile(r"^(?P<indent>\s*)stm\s+(?P<name>.+?)\s*$", re.IGNORECASE)
FORK_JOIN_RE = re.compile(r"^(?P<indent>\s*)(?P<kind>fork|join)\s+(?P<name>[A-Za-z_][A-Za-z0-9_]*)\s*$", re.IGNORECASE)
ENTRY_DO_EXIT_RE = re.compile(r"^(?P<indent>\s*)(entry|do|exit)\s*/", re.IGNORECASE)
ORPHAN_WHEN_RE = re.compile(r"^(?P<indent>\s*)when\b", re.IGNORECASE)


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class NormalizationChange:
    rule_id: str
    line: int
    before: str
    after: str
    kind: str
    semantic_risk: str
    risk_tier: str
    main_eligibility_default: bool
    rationale: str
    span: str | None = None
    loss_type: str | None = None
    concurrency_degraded: bool = False
    needs_manual_review: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "rule_id": self.rule_id,
            "line": self.line,
            "span": self.span,
            "before": self.before,
            "after": self.after,
            "kind": self.kind,
            "semantic_risk": self.semantic_risk,
            "risk_tier": self.risk_tier,
            "main_eligibility_default": self.main_eligibility_default,
            "rationale": self.rationale,
            "loss_type": self.loss_type,
            "concurrency_degraded": self.concurrency_degraded,
            "needs_manual_review": self.needs_manual_review,
        }


@dataclass
class NormalizationResult:
    raw_text: str
    normalized_text: str
    changes: list[NormalizationChange] = field(default_factory=list)
    alias_declarations: list[str] = field(default_factory=list)

    @property
    def raw_sha256(self) -> str:
        return sha256_text(self.raw_text)

    @property
    def normalized_sha256(self) -> str:
        return sha256_text(self.normalized_text)

    @property
    def rule_ids(self) -> list[str]:
        return sorted({c.rule_id for c in self.changes})

    @property
    def has_high_risk_loss(self) -> bool:
        return any(c.risk_tier == "high_risk" or not c.main_eligibility_default for c in self.changes)

    @property
    def concurrency_degraded(self) -> bool:
        return any(c.concurrency_degraded for c in self.changes)

    @property
    def low_risk_candidate(self) -> bool:
        return bool(self.changes) and not self.has_high_risk_loss and not self.concurrency_degraded

    @property
    def main_eligibility_default(self) -> bool:
        return self.low_risk_candidate

    def to_metadata(self) -> dict[str, Any]:
        return {
            "raw_sha256": self.raw_sha256,
            "normalized_sha256": self.normalized_sha256,
            "changes_count": len(self.changes),
            "rule_ids": self.rule_ids,
            "has_high_risk_loss": self.has_high_risk_loss,
            "concurrency_degraded": self.concurrency_degraded,
            "low_risk_candidate": self.low_risk_candidate,
            "main_eligibility_default": self.main_eligibility_default,
            "alias_declarations": self.alias_declarations,
        }


def _rule(rule_id: str) -> dict[str, Any]:
    return RULES[rule_id]


def _change(rule_id: str, *, line: int, before: str, after: str, kind: str, rationale: str, span: str | None = None, loss_type: str | None = None, concurrency_degraded: bool = False) -> NormalizationChange:
    meta = _rule(rule_id)
    return NormalizationChange(
        rule_id=rule_id,
        line=line,
        before=before,
        after=after,
        kind=kind,
        semantic_risk=meta["semantic_risk"],
        risk_tier=meta["risk_tier"],
        main_eligibility_default=bool(meta["main_eligibility_default"]),
        rationale=rationale,
        span=span,
        loss_type=loss_type,
        concurrency_degraded=concurrency_degraded,
        needs_manual_review=not bool(meta["main_eligibility_default"]),
    )


def _alias_for(label: str, used: set[str]) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9]+", "_", label.strip().strip('"'))
    cleaned = cleaned.strip("_") or "State"
    if cleaned[0].isdigit():
        cleaned = f"S_{cleaned}"
    base = cleaned[:48]
    digest = hashlib.sha1(label.encode("utf-8")).hexdigest()[:6]
    alias = f"{base}_{digest}"
    alias = re.sub(r"_+", "_", alias)
    while alias in used:
        digest = hashlib.sha1((alias + label).encode("utf-8")).hexdigest()[:6]
        alias = f"{base}_{digest}"
    used.add(alias)
    return alias


def _needs_alias(endpoint: str) -> tuple[bool, str | None]:
    ep = endpoint.strip()
    if not ep or ep in {"[*]", "[ * ]"}:
        return False, None
    if ep.startswith("[") and ep.endswith("]"):
        inner = ep[1:-1].strip()
        if inner == "*" or not inner:
            return False, None
        return True, inner
    if ep.startswith('"') and ep.endswith('"') and len(ep) >= 2:
        return True, ep[1:-1]
    if SIMPLE_ID_RE.match(ep):
        return False, None
    if " " in ep or "-" in ep or "/" in ep:
        return True, ep.strip('"')
    return False, None


def _split_transition(line: str) -> tuple[str, str, str, str, str] | None:
    """Return prefix, source, arrow, target, suffix for simple PlantUML transition lines.

    This is only a line-level normalizer for official-toolchain input. It is not
    used to construct canonical states/transitions.
    """
    if line.lstrip().startswith("'") or any(token in line for token in UNSUPPORTED_ARROW_TOKENS):
        return None
    # Do not treat declaration / action lines as transitions merely because the label contains arrows.
    first_word = line.strip().split(None, 1)[0].lower() if line.strip() else ""
    if first_word in {"state", "note", "title", "skinparam", "hide", "show", "scale", "left", "right", "top", "bottom"}:
        return None
    arrow_pattern = re.compile("|".join(re.escape(token) for token in sorted(ARROW_TOKENS, key=len, reverse=True)))
    occurrences = [(match.start(), match.group(0)) for match in arrow_pattern.finditer(line)]
    # A single source-to-target transition line is the only low-risk syntax
    # repair scope.  Multi-arrow chains such as `A --> [Error] --> B` are
    # semantically ambiguous and must not be collapsed into an endpoint alias.
    if len(occurrences) != 1:
        return None
    idx, arrow = occurrences[0]
    prefix_match = re.match(r"^(\s*)", line)
    prefix = prefix_match.group(1) if prefix_match else ""
    source = line[:idx].strip()
    rest = line[idx + len(arrow):].strip()
    if not source or not rest:
        return None
    if ":" in rest:
        target, label = rest.split(":", 1)
        suffix = " :" + label
    else:
        target, suffix = rest, ""
    target = target.strip()
    # LLM outputs sometimes write `A --> B when : guard`, which is not
    # accepted by official PlantUML.  Treat the trailing `when` as part of
    # the transition label while preserving the guard-like cue for downstream
    # audits.  This remains a pre-SCXML syntax normalization only.
    when_match = re.match(r"^(?P<target>.+?)\s+when\s*$", target, flags=re.IGNORECASE)
    if when_match and suffix.startswith(" :"):
        target = when_match.group("target").strip()
        label = suffix[2:].strip()
        suffix = " : when" + (f" {label}" if label else "")
    if any(token in source for token in ARROW_TOKENS + UNSUPPORTED_ARROW_TOKENS):
        return None
    if any(token in target for token in ARROW_TOKENS + UNSUPPORTED_ARROW_TOKENS):
        return None
    if re.search(r"\bwhen\b", source, flags=re.IGNORECASE) or re.search(r"\bwhen\b", target, flags=re.IGNORECASE):
        return None
    return prefix, source, arrow, target, suffix


def _collect_existing_aliases(lines: list[str]) -> tuple[dict[str, str], set[str]]:
    aliases: dict[str, str] = {}
    used: set[str] = set()
    for line in lines:
        m = STATE_AS_RE.match(line)
        if m:
            aliases[m.group("label")] = m.group("alias")
            used.add(m.group("alias"))
    return aliases, used


def _rewrite_endpoint(endpoint: str, aliases: dict[str, str], used_aliases: set[str], declarations: list[str]) -> tuple[str, str | None, str | None]:
    needs, label = _needs_alias(endpoint)
    if not needs or label is None:
        compact = endpoint.strip()
        if compact in {"[ * ]"}:
            return "[*]", None, None
        return endpoint.strip(), None, None
    if label not in aliases:
        alias = _alias_for(label, used_aliases)
        aliases[label] = alias
        declarations.append(f'state "{label}" as {alias}')
    endpoint_stripped = endpoint.strip()
    if "[*]" in label and label.strip() != "[*]":
        rule_id = "PUML.NORM.alias_embedded_pseudostate_marker"
    elif endpoint_stripped.startswith("[") and endpoint_stripped.endswith("]"):
        rule_id = "PUML.NORM.alias_bracket_endpoint"
    else:
        rule_id = "PUML.NORM.alias_quoted_endpoint" if endpoint_stripped.startswith('"') else "PUML.NORM.alias_multiword_endpoint"
    return aliases[label], rule_id, label


def _select_endpoint_rule(source_rule: str | None, target_rule: str | None) -> str | None:
    rules = [r for r in (source_rule, target_rule) if r]
    if not rules:
        return None
    if "PUML.NORM.alias_embedded_pseudostate_marker" in rules:
        return "PUML.NORM.alias_embedded_pseudostate_marker"
    if "PUML.NORM.alias_bracket_endpoint" in rules:
        return "PUML.NORM.alias_bracket_endpoint"
    return rules[0]


def _select_endpoint_label(
    *,
    source_rule: str | None,
    source_label: str | None,
    target_rule: str | None,
    target_label: str | None,
) -> str:
    if source_rule == "PUML.NORM.alias_embedded_pseudostate_marker" and source_label:
        return source_label
    if target_rule == "PUML.NORM.alias_embedded_pseudostate_marker" and target_label:
        return target_label
    return source_label or target_label or "spacing"


def normalize_plantuml(raw_text: str) -> NormalizationResult:
    raw_lines = raw_text.splitlines()
    aliases, used_aliases = _collect_existing_aliases(raw_lines)
    declarations: list[str] = []
    changes: list[NormalizationChange] = []
    out_lines: list[str] = []

    for idx, raw_line in enumerate(raw_lines, start=1):
        line = raw_line.rstrip("\n")
        stripped = line.strip()
        new_line = line

        if stripped and not stripped.startswith("'"):
            block = STM_BLOCK_RE.match(line)
            heading = STM_HEADING_RE.match(line)
            fork_join = FORK_JOIN_RE.match(line)
            if block:
                label = block.group("name").strip().strip('"')
                alias = _alias_for(label, used_aliases)
                new_line = f'{block.group("indent")}state "{label}" as {alias} {{'
                changes.append(_change(
                    "PUML.NORM.stm_block_to_state",
                    line=idx,
                    before=line,
                    after=new_line,
                    kind="stm_block_to_state",
                    rationale="非 PlantUML stm block 被转换为 PlantUML state block；可能改变层级语义，默认不进主 eligibility。",
                    loss_type="hierarchy",
                ))
            elif heading and stripped.lower() not in {"@startuml", "@enduml"}:
                new_line = f"{heading.group('indent')}' normalization removed non-PlantUML stm heading: {stripped}"
                changes.append(_change(
                    "PUML.NORM.remove_stm_heading",
                    line=idx,
                    before=line,
                    after=new_line,
                    kind="remove_stm_heading",
                    rationale="去除非 PlantUML heading，使后续内容可交由官方 PlantUML 检查。",
                    loss_type="syntax",
                ))
            elif "<.." in line or "..>" in line:
                indent = re.match(r"^(\s*)", line).group(1)
                new_line = f"{indent}' normalization-commented dependency-like arrow: {stripped}"
                changes.append(_change(
                    "PUML.NORM.comment_dependency_arrow",
                    line=idx,
                    before=line,
                    after=new_line,
                    kind="comment_dependency_arrow",
                    rationale="虚线 dependency-like 关系不是可直接消费的状态迁移；注释会丢失结构关系，默认不进主 eligibility。",
                    loss_type="structure",
                ))
            elif ENTRY_DO_EXIT_RE.match(line):
                indent = ENTRY_DO_EXIT_RE.match(line).group("indent")
                new_line = f"{indent}' normalization-commented action: {stripped}"
                changes.append(_change(
                    "PUML.NORM.entry_do_exit_rewrite_or_loss",
                    line=idx,
                    before=line,
                    after=new_line,
                    kind="comment_entry_do_exit",
                    rationale="entry/do/exit action 行被注释，可能丢失动作语义，默认不进主 eligibility。",
                    loss_type="action",
                ))
            elif ORPHAN_WHEN_RE.match(line):
                indent = ORPHAN_WHEN_RE.match(line).group("indent")
                new_line = f"{indent}' normalization-commented orphan guard: {stripped}"
                changes.append(_change(
                    "PUML.NORM.comment_orphan_when",
                    line=idx,
                    before=line,
                    after=new_line,
                    kind="comment_orphan_when",
                    rationale="无法归属到 transition 的 when 行被注释，可能丢失 guard，默认不进主 eligibility。",
                    loss_type="guard",
                ))
            elif fork_join:
                name = fork_join.group("name")
                new_line = f'{fork_join.group("indent")}state "{name}" as {name}'
                used_aliases.add(name)
                changes.append(_change(
                    "PUML.NORM.fork_join_decl_to_state",
                    line=idx,
                    before=line,
                    after=new_line,
                    kind="fork_join_decl_to_state",
                    rationale="fork/join pseudo-state 被降级为普通 state，会改变并发/同步语义，默认不进主 eligibility。",
                    loss_type="semantic",
                    concurrency_degraded=True,
                ))
            else:
                split = _split_transition(line)
                if split:
                    prefix, source, arrow, target, suffix = split
                    new_source, source_rule, source_label = _rewrite_endpoint(source, aliases, used_aliases, declarations)
                    new_target, target_rule, target_label = _rewrite_endpoint(target, aliases, used_aliases, declarations)
                    new_suffix = suffix
                    suffix_rule: str | None = None
                    suffix_label: str | None = None
                    if re.search(r"\s+when\s*:", line, flags=re.IGNORECASE) and suffix.strip().lower().startswith(": when"):
                        suffix_rule = "PUML.NORM.transition_when_label"
                        suffix_label = suffix[2:].strip()
                    elif suffix.strip() == ":":
                        suffix_rule = "PUML.NORM.remove_empty_transition_label"
                        suffix_label = "empty_label"
                        new_suffix = ""
                    spacing_changed = not re.search(r"\s" + re.escape(arrow) + r"\s", line)
                    if source_rule or target_rule or suffix_rule or source != new_source or target != new_target or new_suffix != suffix or spacing_changed:
                        new_line = f"{prefix}{new_source} {arrow} {new_target}{new_suffix}"
                        rule_id = suffix_rule or _select_endpoint_rule(source_rule, target_rule) or "PUML.NORM.alias_multiword_endpoint"
                        label = suffix_label or _select_endpoint_label(
                            source_rule=source_rule,
                            source_label=source_label,
                            target_rule=target_rule,
                            target_label=target_label,
                        )
                        loss_type = "semantic" if rule_id == "PUML.NORM.alias_embedded_pseudostate_marker" else "syntax"
                        if rule_id == "PUML.NORM.transition_when_label":
                            kind = "transition_when_label_normalization"
                            rationale = f"transition 的 `when :` 伪语法被规范化为 PlantUML label `{label}`；保留 guard-like cue，canonical 仍必须来自官方 SCXML。"
                            span = "transition_label"
                        elif rule_id == "PUML.NORM.remove_empty_transition_label":
                            kind = "remove_empty_transition_label"
                            rationale = "transition 末尾空 label 冒号不含可见语义内容，删除以通过 official PlantUML syntax。"
                            span = "transition_label"
                        else:
                            kind = "transition_endpoint_to_alias"
                            rationale = (
                                f"transition endpoint `{label}` 改写为稳定 alias/标准间距；canonical 仍必须来自官方 SCXML。"
                                if rule_id != "PUML.NORM.alias_embedded_pseudostate_marker"
                                else f"transition endpoint `{label}` 含内嵌 [*] 伪状态标记，alias 化可能把初始/终止伪状态语义误读为普通状态名；默认只作 supplementary/manual-review。"
                            )
                            span = "transition_endpoint"
                        changes.append(_change(
                            rule_id,
                            line=idx,
                            before=line,
                            after=new_line,
                            kind=kind,
                            rationale=rationale,
                            span=span,
                            loss_type=loss_type,
                        ))
        out_lines.append(new_line)

    if declarations:
        insert_at = 1 if out_lines and out_lines[0].strip().lower() == "@startuml" else 0
        out_lines[insert_at:insert_at] = declarations
    normalized_text = "\n".join(out_lines) + ("\n" if raw_text.endswith("\n") or raw_text else "")
    return NormalizationResult(raw_text=raw_text, normalized_text=normalized_text, changes=changes, alias_declarations=declarations)


def classify_plantuml_issue(raw_text: str, result: NormalizationResult | None = None) -> str:
    text = raw_text
    if result and "PUML.NORM.alias_embedded_pseudostate_marker" in result.rule_ids:
        return "G_embedded_pseudostate_marker"
    if re.search(r"^\s*stm\s+", text, flags=re.IGNORECASE | re.MULTILINE):
        return "A_non_plantuml_stm_directive"
    if re.search(r"^\s*(entry|do|exit)\s*/", text, flags=re.IGNORECASE | re.MULTILINE):
        return "B_entry_do_exit_action_syntax"
    if re.search(r"(<\.\.|\.\.>|^\s*(fork|join)\s+)", text, flags=re.IGNORECASE | re.MULTILINE):
        return "D_activity_or_pseudostate_syntax_mixed_in_state_diagram"
    if result and "PUML.NORM.alias_quoted_endpoint" in result.rule_ids:
        return "E_quoted_transition_state_names"
    if result and "PUML.NORM.alias_multiword_endpoint" in result.rule_ids:
        return "F_unquoted_state_names_with_spaces"
    if re.search(r'"[^"]+"\s*-+>|-+>\s*"[^"]+"', text):
        return "E_quoted_transition_state_names"
    return "Y_other_or_contextual"
