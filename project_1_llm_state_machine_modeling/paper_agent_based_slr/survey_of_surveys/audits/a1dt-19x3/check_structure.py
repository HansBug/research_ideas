#!/usr/bin/env python3
"""A1-DT 结构门禁。

该脚本只检查 PR-A1-DT 的确定性结构合同，不判断论文内容真假。
内容真实性仍需回到单篇原文、A.1--A.4 审计附录和人工 / reviewer 审计。
"""
from __future__ import annotations
import csv
import re
import sys
from pathlib import Path

def find_repo_root(start: Path) -> Path:
    """Locate the repository root without assuming a local clone directory name."""
    cur = start.resolve()
    for candidate in [cur, *cur.parents]:
        if (candidate / '.git').exists() and (candidate / 'project_1_llm_state_machine_modeling').exists():
            return candidate
    raise SystemExit(f'cannot locate repository root from {start}')


ROOT = find_repo_root(Path(__file__).resolve())
BASE = ROOT / 'project_1_llm_state_machine_modeling/paper_agent_based_slr/survey_of_surveys'
BATCH = BASE / 'audits/a1dt-19x3'
PAPERS = BASE / 'papers'
REQUIRED_REVIEW_MARKERS = [
    '## 维度树复原',
    '### 原文 schema 主树（19×3 审计后返修）',
    '#### 三路审计综合返修结论',
    '#### 审计返修口径',
    '#### 通用接口投影',
    '## 审计附录：证据链与结论-证据映射',
    '### A.1 论文与本地文件来源',
    '### A.2 维度树证据账本',
    '### A.3 结论-证据映射',
    '### A.4 本地复验命令与人工核验清单',
]
REQUIRED_AUDIT_AGENTS = ['codex', 'claude', 'deepseek']
FORBIDDEN_PLACEHOLDERS = ['审计未生成结果文件']


def fail(errors: list[str], msg: str) -> None:
    errors.append(msg)


def check_tasks(errors: list[str]) -> list[str]:
    task_path = BATCH / 'TASKS.tsv'
    if not task_path.exists():
        fail(errors, f'missing {task_path}')
        return []
    rows = list(csv.DictReader(task_path.open(encoding='utf-8'), delimiter='\t'))
    if len(rows) != 57:
        fail(errors, f'TASKS.tsv row count should be 57, got {len(rows)}')
    slugs = sorted({r.get('slug','') for r in rows})
    if len(slugs) != 19:
        fail(errors, f'TASKS.tsv slug count should be 19, got {len(slugs)}')
    for r in rows:
        slug, agent, status, rel = r.get('slug'), r.get('agent'), r.get('status'), r.get('result_path')
        if agent not in REQUIRED_AUDIT_AGENTS:
            fail(errors, f'{slug}: unexpected agent {agent}')
        if status != 'completed':
            fail(errors, f'{slug} {agent}: status should be completed, got {status}')
        rp = BATCH / rel
        if not rp.exists() or rp.stat().st_size <= 1000:
            fail(errors, f'{slug} {agent}: result missing or too small: {rp}')
        else:
            txt = rp.read_text(encoding='utf-8', errors='ignore')
            for ph in FORBIDDEN_PLACEHOLDERS:
                if ph in txt[:500]:
                    fail(errors, f'{slug} {agent}: placeholder result {ph}')
            if '## 6. C/I/M 结论' not in txt and '## 6. C/I/M' not in txt:
                fail(errors, f'{slug} {agent}: missing C/I/M conclusion section')
    return slugs


def check_review(slug: str, errors: list[str]) -> None:
    d = PAPERS / slug
    for name in ['bibtex.bib', 'metadata.json', 'paper.pdf', 'paper_content.txt', 'review.md']:
        if not (d / name).exists():
            fail(errors, f'{slug}: missing {name}')
    review = d / 'review.md'
    if not review.exists():
        return
    txt = review.read_text(encoding='utf-8', errors='ignore')
    for marker in REQUIRED_REVIEW_MARKERS:
        if marker not in txt:
            fail(errors, f'{slug}: missing marker {marker}')
    for agent in REQUIRED_AUDIT_AGENTS:
        link = f'../../audits/a1dt-19x3/results/{slug}__{agent}.md'
        if link not in txt:
            fail(errors, f'{slug}: missing audit link {link}')
    if '[clm-' + slug + '-a1dt-19x3-repair]' not in txt:
        fail(errors, f'{slug}: missing a1dt-19x3 repair claim')
    if '所有节点在本 PR 仍为 `schema_seed`' not in txt:
        fail(errors, f'{slug}: missing schema_seed downgrade sentence')
    if '不得进入当前 SUMMARY 定量统计' not in txt:
        fail(errors, f'{slug}: missing no-summary-stat downgrade sentence')
    if '通用接口只能作为跨论文投影' not in txt and '通用接口只做投影' not in txt:
        fail(errors, f'{slug}: missing common-interface downgrade sentence')
    # 审计附录正式表头应保持中文优先，不应回退成英文机器字段表头。
    for header in [
        '| 来源标识 | 文件或链接 | 类型 | 用途 | 可核验性 | 备注 |',
        '| 证据标识 | 引用键 | 来源标识 | 来源文件 | 原文页码 | 原文章节 |',
        '| 引用键 | 结论标识 | 结论内容 | 结论类型 | 支撑对象标识 |',
        '| 检查标识 | 复验对象 | 命令或人工核验动作 | 通过条件 | 当前状态 |',
    ]:
        if header not in txt:
            fail(errors, f'{slug}: missing Chinese audit table header prefix: {header}')
    # 若 A.3 中出现 statistical_synthesis，必须只是说明禁止或后续条件，不应作为允许用途单元格。
    a3 = txt.split('### A.3 结论-证据映射', 1)[-1].split('### A.4', 1)[0]
    bad = re.findall(r'\|[^\n]*\|\s*statistical_synthesis\s*\|[^\n]*\|\s*false\s*\|', a3)
    if bad:
        fail(errors, f'{slug}: A.3 appears to allow statistical_synthesis in current A1-DT')


def main() -> int:
    errors: list[str] = []
    for rel in ['README.md', 'GUIDE.md', 'SUMMARY.md', 'patterns/pattern-field-schema.md', 'audits/README.md', 'audits/a1dt-19x3/README.md', 'audits/a1dt-19x3/SUMMARY.md', 'audits/a1dt-19x3/run_audit.py']:
        if not (BASE / rel).exists():
            fail(errors, f'missing {rel}')
    slugs = check_tasks(errors)
    actual_slugs = sorted(p.name for p in PAPERS.iterdir() if p.is_dir())
    if len(actual_slugs) != 19:
        fail(errors, f'paper directory count should be 19, got {len(actual_slugs)}')
    if slugs and slugs != actual_slugs:
        fail(errors, f'TASKS slugs differ from paper dirs: tasks={slugs}, dirs={actual_slugs}')
    for slug in actual_slugs:
        check_review(slug, errors)

    logs = list((BATCH / 'logs').glob('*.log'))
    if len(logs) != 57:
        fail(errors, f'audit log count should be 57, got {len(logs)}')
    # SUMMARY 必须回链单篇维度树与 A1-DT 归纳。
    sm = (BASE / 'SUMMARY.md').read_text(encoding='utf-8', errors='ignore') if (BASE / 'SUMMARY.md').exists() else ''
    for marker in ['维度树模式总览', 'SUMMARY 结论-证据映射', '[sum-A1DT-tree-types]', '[sum-A1DT-statistical-pool]', '[sum-A1DT-boundary-anchor]']:
        if marker not in sm:
            fail(errors, f'SUMMARY missing {marker}')
    if errors:
        print('A1-DT structure check FAILED:')
        for e in errors:
            print('-', e)
        return 1
    print('A1-DT structure check passed: 19 papers, 57 audits, review anchors, downgrade rules and SUMMARY links are structurally present.')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
