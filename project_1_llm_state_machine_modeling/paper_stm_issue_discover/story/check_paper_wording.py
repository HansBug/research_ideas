"""Gate: venue-facing paper text must follow the adjudication/dataset wording rule (story/README.md).

Scans the Chinese manuscript and the Overleaf roots/sections for forbidden wording. Exit 1 on any hit.
Usage: python project_1_llm_state_machine_modeling/paper_stm_issue_discover/story/check_paper_wording.py
"""
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PAPER = HERE.parents[0]
FILES = [HERE / 'paper_outline.md'] + sorted((PAPER / 'overleaf').glob('main*.tex')) + sorted((PAPER / 'overleaf' / 'sections').glob('*.tex'))
FORBIDDEN = re.compile(
    r'judge|LLM-as-(a-)?judge|LLM\s+as\s+(a\s+)?judge|评价器|evaluator|自动裁定|裁判|人工确认|human[- ]confirm'
    r'|github\.com|research_ideas|HansBug'
    r'|gpt-5\.6-luna[^。\n]{0,40}(判读|评价|评阅|裁定|adjudicat)',
    re.IGNORECASE)

hits = []
for f in FILES:
    if not f.exists():
        continue
    for no, line in enumerate(f.read_text(encoding='utf-8').splitlines(), 1):
        if line.startswith('%'):  # LaTeX comments are not venue-facing
            continue
        m = FORBIDDEN.search(line)
        if m:
            hits.append(f"{f.relative_to(PAPER)}:{no}: …{line[max(0, m.start()-30):m.end()+30]}…")
if hits:
    print("FORBIDDEN WORDING (see story/README.md 论文对外口径铁律):")
    print('\n'.join(hits))
    sys.exit(1)
print(f"wording gate passed: {sum(1 for f in FILES if f.exists())} files clean")
