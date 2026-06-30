#!/usr/bin/env python3
from __future__ import annotations
import argparse, concurrent.futures, os, subprocess, textwrap, time
from pathlib import Path

def find_repo_root(start: Path) -> Path:
    """Locate the repository root without assuming a local clone directory name."""
    cur = start.resolve()
    for candidate in [cur, *cur.parents]:
        if (candidate / '.git').exists() and (candidate / 'project_1_llm_state_machine_modeling').exists():
            return candidate
    raise RuntimeError(f'Cannot locate repository root from {start}')


def codex_home() -> Path:
    return Path(os.environ.get('CODEX_HOME', Path.home() / '.codex')).expanduser()


def first_existing(paths: list[Path]) -> str:
    for p in paths:
        if p.exists():
            return str(p)
    return f'MISSING: {paths[0]}'


def resolve_subagent_runner() -> str:
    explicit = os.environ.get('SUB_AGENTS_RUNNER')
    if explicit:
        return explicit
    runner = codex_home() / 'skills/sub-agents/scripts/run_subagent.py'
    if runner.exists():
        return str(runner)
    raise RuntimeError('Cannot locate sub-agents runner; set SUB_AGENTS_RUNNER or install the sub-agents skill')


def resolve_autoresearch_skill() -> str:
    explicit = os.environ.get('OMX_AUTORESEARCH_SKILL')
    if explicit:
        return explicit
    candidates = sorted((codex_home() / 'plugins/cache').glob('oh-my-codex-local/oh-my-codex/*/skills/autoresearch/SKILL.md'))
    if candidates:
        return str(candidates[-1])
    return 'MISSING: oh-my-codex autoresearch skill not found under CODEX_HOME/plugins/cache'


ROOT = find_repo_root(Path(__file__).resolve())
AUDIT_DIR = Path(__file__).resolve().parent
PAPERS_DIR = ROOT / 'project_1_llm_state_machine_modeling/paper_agent_based_slr/survey_of_surveys/papers'
RESULTS_DIR = AUDIT_DIR / 'results'
LOGS_DIR = AUDIT_DIR / 'logs'
PROMPTS_DIR = AUDIT_DIR / 'prompts'
SUBAGENT_RUNNER = resolve_subagent_runner()

SKILLS = [
    first_existing([codex_home() / 'skills/ai-research-writing-skill/SKILL.md']),
    first_existing([codex_home() / 'skills/ai-research-writing-skill/references/paper-story.md']),
    first_existing([codex_home() / 'skills/ai-research-writing-skill/references/reviewer-guidelines.md']),
    first_existing([codex_home() / 'skills/ai-research-writing-skill/references/reviewer-self-review.md']),
    first_existing([codex_home() / 'skills/research-planning/SKILL.md']),
    first_existing([codex_home() / 'skills/research-planning/references/planning-prompts.md']),
    resolve_autoresearch_skill(),
]

COMMON_INPUTS = [
    'project_1_llm_state_machine_modeling/paper_agent_based_slr/survey_of_surveys/README.md',
    'project_1_llm_state_machine_modeling/paper_agent_based_slr/survey_of_surveys/GUIDE.md',
    'project_1_llm_state_machine_modeling/paper_agent_based_slr/survey_of_surveys/SUMMARY.md',
    'project_1_llm_state_machine_modeling/paper_agent_based_slr/survey_of_surveys/patterns/pattern-field-schema.md',
    'project_1_llm_state_machine_modeling/paper_agent_based_slr/story/paper_story.md',
]

AGENT_CMDS = {
    # Prefer stable sub-agents runner for codex/claude. DeepSeek has a custom CLI, so it stays direct.
    'codex': lambda prompt, cwd: ['python', SUBAGENT_RUNNER, '--agent', 'codex-reviewer', '--prompt', prompt, '--cwd', str(cwd), '--timeout', '1800000'],
    'claude': lambda prompt, cwd: ['python', SUBAGENT_RUNNER, '--agent', 'claude-reviewer', '--prompt', prompt, '--cwd', str(cwd), '--timeout', '2400000'],
    'deepseek': lambda prompt, cwd: ['codex-deepseek', 'exec', '--dangerously-bypass-approvals-and-sandbox', '-C', str(cwd), prompt],
}


def build_prompt(slug: str, agent: str) -> str:
    paper_dir = f'project_1_llm_state_machine_modeling/paper_agent_based_slr/survey_of_surveys/papers/{slug}'
    result = f'project_1_llm_state_machine_modeling/paper_agent_based_slr/survey_of_surveys/audits/a1dt-19x3/results/{slug}__{agent}.md'
    skill_list = '\n'.join(f'- `{p}`' for p in SKILLS)
    common_list = '\n'.join(f'- `{p}`' for p in COMMON_INPUTS)
    return textwrap.dedent(f'''
    你是 PR #135 的 `{agent}` 学术 reviewer。请只审计单篇论文 `{slug}`，不要开启 sub-subagent，不要修改仓库文件，不要 push，不要 gh comment。

    你的任务是对该论文进行全文级学术审计，判断当前 `review.md` 中“维度树复原”是否完整、准确、可追溯，尤其检查树是否过小、是否把通用 6 个 leaf 接口误当成原文 schema、是否遗漏原文 RQ / extraction form / taxonomy / coding scheme / roadmap figure / evidence table / finding path / quality / validity / artifact 字段。

    必须使用并体现以下技能口径；你需要自行读取这些 SKILL.md / reference 文件后再审计；若某路径以 `MISSING:` 开头，应在审计中如实记录环境缺失，不得假装已读取：
    {skill_list}

    必须读取以下文库级规则和 story：
    {common_list}

    必须读取该单篇的以下文件；`paper_content.txt` 必须尽可能全文阅读，不允许只看摘要或 grep 几个词：
    - `{paper_dir}/bibtex.bib`
    - `{paper_dir}/metadata.json`
    - `{paper_dir}/paper_content.txt`
    - `{paper_dir}/review.md`
    - 必要时核对 `{paper_dir}/paper.pdf` 的页码、图表或表格；如果无法视觉核对，必须说明。

    输出必须写入：`{result}`。请在最终回答中只简要说明写入路径和 C/I/M 摘要。

    审计报告必须使用中文，并包含以下结构：

    # {slug} · {agent} 全文审计报告

    ## 1. 审计身份与输入
    - reviewer 身份：{agent}
    - 是否读取 `$ai-research-writing-skill`：是/否 + 读取路径
    - 是否读取 `$research-planning`：是/否 + 读取路径
    - 是否读取 `$oh-my-codex:autoresearch`：是/否 + 读取路径
    - 是否完整阅读 `paper_content.txt`：是/否 + 简述覆盖范围
    - 是否核对 `paper.pdf`：是/否 + 原因

    ## 2. 原文真实结构复原
    - 原文 RQ / 目标 / 贡献声明
    - 原文方法流程、检索 / 纳排 / 数据抽取 / 编码 / 统计 / finding 形成方式
    - 原文显式 extraction form、classification schema、taxonomy、coding scheme、模型、图表、roadmap 或 quality rubric
    - 原文如何从字段 / 统计观察形成 conclusion / finding / gap / recommendation

    ## 3. 当前 `review.md` 维度树审计
    | 检查项 | 结论 | 证据 / 理由 | 严重度 |
    |---|---|---|---|
    | 根节点是否准确 |  |  | C/I/M/通过 |
    | 主干分支是否覆盖原文 schema |  |  | C/I/M/通过 |
    | 叶子维度是否足够具体 |  |  | C/I/M/通过 |
    | 取值空间是否可执行 |  |  | C/I/M/通过 |
    | 关系边是否缺失 |  |  | C/I/M/通过 |
    | 统计用途 / 分母是否正确 |  |  | C/I/M/通过 |
    | 候选 finding 路径是否完整 |  |  | C/I/M/通过 |
    | A.1--A.4 证据链是否足够 |  |  | C/I/M/通过 |
    | 是否存在可能误导 A2a 的强主张 |  |  | C/I/M/通过 |

    ## 4. 建议维度树骨架
    给出你认为更忠实于原文的维度树，至少包含：根节点、主干分支、叶子维度、每个叶子的候选取值空间、是否可统计、缺失值语义、证据来源定位。若当前 review 已足够，请说明为什么。

    ## 5. 必须补充 / 修正清单
    | 修复项 | 建议修改位置 | 具体修改建议 | 证据来源 | 严重度 |
    |---|---|---|---|---|

    ## 6. C/I/M 结论
    - C：直接破坏 Paper2 学术目标、证据链或后续 A2a/A2b 可靠性的问题。
    - I：会实质影响维度树可用性、原文 schema 复原、证据可审计性的问题。
    - M：不阻塞的清晰度或维护性建议。
    - 最终建议：READY / NEEDS FIX。

    审计原则：
    - 不允许为凑完整而臆造原文没有的字段。
    - 不允许把 roadmap / vision / proposal 写成完成型统计 finding。
    - 不允许把 `not_verified` 或泛定位证据升级成可统计结论。
    - 如果当前树只是通用接口而非原文 schema，必须指出并给出最小修复方案。
    - C/I 必须说明对 Paper2 学术目标或证据链的影响。
    ''').strip()


def run_one(slug: str, agent: str, timeout: int) -> tuple[str, str, int, str]:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    PROMPTS_DIR.mkdir(parents=True, exist_ok=True)
    prompt = build_prompt(slug, agent)
    (PROMPTS_DIR / f'{slug}__{agent}.prompt.md').write_text(prompt)
    cmd = AGENT_CMDS[agent](prompt, ROOT)
    log = LOGS_DIR / f'{slug}__{agent}.log'
    start = time.time()
    try:
        cp = subprocess.run(cmd, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=timeout)
        out = cp.stdout
        code = cp.returncode
    except subprocess.TimeoutExpired as e:
        out = (e.stdout or '') + f'\n\n[TIMEOUT after {timeout}s]\n'
        code = 124
    log.write_text(out)
    result_path = RESULTS_DIR / f'{slug}__{agent}.md'
    if not result_path.exists():
        result_path.write_text('# 审计未生成结果文件\n\n该 agent 未按要求写入结果文件；原始输出见日志。\n')
    return slug, agent, code, f'{time.time()-start:.1f}s'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--agents', default='codex,claude,deepseek')
    ap.add_argument('--slugs', default='')
    ap.add_argument('--max-workers', type=int, default=3)
    ap.add_argument('--timeout', type=int, default=1800)
    ap.add_argument('--skip-existing', action='store_true', help='Skip tasks whose result file already exists and is non-trivial')
    args = ap.parse_args()
    agents = [a.strip() for a in args.agents.split(',') if a.strip()]
    if args.slugs:
        slugs = [s.strip() for s in args.slugs.split(',') if s.strip()]
    else:
        slugs = sorted(p.name for p in PAPERS_DIR.iterdir() if p.is_dir())
    tasks = [(s,a) for s in slugs for a in agents]
    if args.skip_existing:
        filtered=[]
        for s,a in tasks:
            rp = RESULTS_DIR / f'{s}__{a}.md'
            if rp.exists() and rp.stat().st_size > 1000 and '审计未生成结果文件' not in rp.read_text(errors='ignore')[:200]:
                print(f'SKIP {s} {a} existing {rp.stat().st_size} bytes', flush=True)
            else:
                filtered.append((s,a))
        tasks = filtered
    print(f'running {len(tasks)} tasks with max_workers={args.max_workers}')
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.max_workers) as ex:
        futs = [ex.submit(run_one, s, a, args.timeout) for s,a in tasks]
        for fut in concurrent.futures.as_completed(futs):
            print('DONE', *fut.result(), flush=True)

if __name__ == '__main__':
    main()
