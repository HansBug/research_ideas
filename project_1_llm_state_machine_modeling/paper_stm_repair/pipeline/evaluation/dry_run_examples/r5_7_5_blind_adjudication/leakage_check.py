#!/usr/bin/env python3
from __future__ import annotations
import argparse, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FORBIDDEN = [
    r"primary_expected_verdict", r"expected_verdict", r"target_closure_expected",
    r"oracle_answer", r"hidden_oracle", r"source_case_id", r"source_slug",
    r"expected_better", r"expected_not_better", r"expected_partial", r"expected_unknown",
    r"protocol_invalid_conversion_laundering", r"text_similarity_misuse", r"hierarchy_loss",
    r"stmk_repair_failure_invalid_candidate", r"outside headline", r"T1 stress marker", r"stress_ticks", r"clm-c[0-9][0-9]-expected", r"src-c[0-9][0-9]-"
]
SKIP_NAMES = {"oracle_answer_key.json", "leakage_check.py", "score_blind_outputs.py", "run_blind_judge.py"}
SKIP_DIRS = {"judge_outputs"}

def scan_path(path: Path) -> list[tuple[str,str]]:
    findings=[]
    for p in path.rglob('*'):
        rel = p.relative_to(ROOT)
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

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--path', default=str(ROOT/'blind_inputs'))
    args=ap.parse_args()
    findings=scan_path(Path(args.path))
    if findings:
        for f, why in findings:
            print(f"LEAK\t{f}\t{why}")
        raise SystemExit(1)
    print('r5.7.5-blind-leakage-check-ok')
if __name__=='__main__': main()
