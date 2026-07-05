#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FORBIDDEN = [
    r"primary_expected_verdict", r"expected_verdict", r"target_closure_expected",
    r"oracle_answer", r"hidden_oracle", r"source_case_id", r"source_slug",
    r"expected_better", r"expected_not_better", r"expected_partial", r"expected_unknown",
    r"protocol_invalid_conversion_laundering", r"text_similarity_misuse", r"hierarchy_loss",
    r"stmk_repair_failure_invalid_candidate", r"outside headline", r"T1 stress marker", r"stress_ticks", r"clm-c[0-9][0-9]-expected", r"src-c[0-9][0-9]-",
    r"semantic_evidence_status", r"target_closure_expected", r"target_family",
    r"strict better should", r"strict semantic gain", r"insufficient_for_strict", r"insufficient_traceability",
    r"t05_counter_abstraction_without_lifecycle",
    r"constructed_candidate_with_local_ledgers", r"normalization_only_artifact",
    r"observed_domain_features", r"declared_extra_method_claims",
    r"candidate_semantics_observed_by_carrier",
    r"candidate_counter_update_lifecycle_not_present_in_carrier",
    r"candidate_hash_matches_constructed_case",
]
# These terms are allowed in the per-case NL/STM payload, but not in the reusable
# prompt prefix before the "# Blind case input" marker.
PROMPT_FORBIDDEN = [
    r"SendDeparted", r"Send Arrived", r"Entry/Accelerate", r"do/Send",
    r"HighwayMode", r"UrbanMode", r"dist_to_front", r"extra_lane",
    r"arrival_sequence", r"departure_sequence",
    r"constructed_candidate_with_local_ledgers", r"normalization_only_artifact",
    r"candidate_counter_update_lifecycle_not_present_in_carrier",
]
PROMPT = ROOT.parents[3] / "experiment_design/protocols/better_adjudication_blind_prompt_v0.md"
SKIP_NAMES = {"oracle_answer_key.json", "leakage_check.py", "score_blind_outputs.py", "run_blind_judge.py", "build_final_run_manifest.py"}
SKIP_DIRS = {"judge_outputs"}


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def prompt_prefix(text: str) -> str:
    marker = "# Blind case input"
    return text.split(marker, 1)[0] if marker in text else text


def scan_path(path: Path) -> list[tuple[str,str]]:
    findings=[]
    base = path.resolve()
    for p in path.rglob('*'):
        try:
            rel = p.resolve().relative_to(ROOT)
        except ValueError:
            rel = p.resolve().relative_to(base.parent)
        if any(part in SKIP_DIRS for part in rel.parts):
            continue
        if p.name in SKIP_NAMES:
            continue
        rels = str(rel)
        for pat in FORBIDDEN:
            if re.search(pat, rels, flags=re.I):
                findings.append((rels, f"path matches {pat}"))
        if p.is_file():
            try:
                text=p.read_text(encoding='utf-8')
            except UnicodeDecodeError:
                continue
            for pat in FORBIDDEN:
                if re.search(pat, text, flags=re.I):
                    findings.append((rels, f"content matches {pat}"))
    return findings


def scan_prompt_template() -> list[tuple[str, str]]:
    findings=[]
    text = PROMPT.read_text(encoding='utf-8')
    for pat in PROMPT_FORBIDDEN:
        if re.search(pat, text, flags=re.I):
            findings.append((str(PROMPT.relative_to(ROOT.parents[3])), f"prompt content matches {pat}"))
    return findings


def scan_judge_prompt_prefixes(judge: str | None = None) -> list[tuple[str, str]]:
    findings: list[tuple[str, str]] = []
    # run_blind_judge.py builds prompt as template + "\n\n# Blind case input".
    expected_prefix = PROMPT.read_text(encoding='utf-8') + "\n\n"
    expected_hash = sha256_text(expected_prefix)
    out_root = ROOT / 'judge_outputs'
    if judge:
        roots = [out_root / judge]
    elif out_root.exists():
        roots = [p for p in out_root.iterdir() if p.is_dir() and not p.name.startswith('legacy_')]
    else:
        roots = []
    for root in roots:
        if not root.exists():
            findings.append((str(root.relative_to(ROOT)), 'judge output directory missing'))
            continue
        for prompt_path in root.glob('B*/prompt.txt'):
            text = prompt_path.read_text(encoding='utf-8')
            prefix = prompt_prefix(text)
            rel = str(prompt_path.relative_to(ROOT))
            if sha256_text(prefix) != expected_hash:
                findings.append((rel, 'prompt prefix hash differs from current blind prompt template'))
            for pat in PROMPT_FORBIDDEN:
                if re.search(pat, prefix, flags=re.I):
                    findings.append((rel, f"prompt prefix matches {pat}"))
    return findings


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--path', default=str(ROOT/'blind_inputs'))
    ap.add_argument('--scan-prompt', action='store_true', default=True)
    ap.add_argument('--scan-judge-prompts', action='store_true')
    ap.add_argument('--judge', default=None, help='When scanning judge prompts, restrict to this judge output directory name.')
    args=ap.parse_args()
    findings=scan_path(Path(args.path))
    if args.scan_prompt:
        findings.extend(scan_prompt_template())
    if args.scan_judge_prompts:
        findings.extend(scan_judge_prompt_prefixes(args.judge))
    if findings:
        for f, why in findings:
            print(f"LEAK\t{f}\t{why}")
        raise SystemExit(1)
    print('r5.7.5-blind-leakage-check-ok')
if __name__=='__main__': main()
