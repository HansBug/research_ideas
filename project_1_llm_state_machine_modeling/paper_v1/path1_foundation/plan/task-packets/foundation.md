# Task Packet: Path-1 Paper Foundation PR

## Scope

创建一个新 PR，作为 Project 1 第一篇 Path-1 paper 后续工作的 foundation。PR body 和仓库文档必须能让后续 agent / 人类直接沿着它执行 story freeze、baseline selection、sample registry、oracle protocol、experiments、writing 和 submission。

## Files allowed to edit

- `project_1_llm_state_machine_modeling/paper_v1/README.md`
- `project_1_llm_state_machine_modeling/paper_v1/path1_foundation/**`
- PR body / PR comments

## Files not edited in this PR

- `project_1_llm_state_machine_modeling/method/**`
- `project_1_llm_state_machine_modeling/eval/**`
- `project_1_llm_state_machine_modeling/baselines/**`
- `runs/**`
- 实验代码 / provider 配置 / `.env`

## Required evidence

- PR #9 historical assets：selection、expansion、ref_stms、PATH1_REPORT。
- PR #31 / project_1 talks：导师对 Path-1、E1/E2、Hybrid、Path-2 的定调。
- PR #22 / method docs：当前 agent-loop / skill / run-record 事实。
- issue #67：2026 夏季投稿计划。
- baselines SUMMARY：closest prior work matrix。

## Rejection checks

- 不能把 PR #9 selection / expansion / historical early reference drafts 写成当前 paper result。
- 不能把第一篇主线写成 Path-2、Hybrid、DSL、LangGraph、Codex/Claude 主线。
- 不能声明已有主实验 lift / SOTA / same-benchmark win。
- 不能把 LLM-as-Judge 写成主 oracle。
- 不能把 parse/semantic/sim 写成完整 formal verification。
- PR body 必须包含范围、非目标、执行计划和 ready gate。

## Validation commands

```bash
git status --short --branch
find project_1_llm_state_machine_modeling/paper_v1/path1_foundation -type f | sort
python - <<'PY'
from pathlib import Path
for p in Path('project_1_llm_state_machine_modeling/paper_v1/path1_foundation').rglob('*.md'):
    text = p.read_text(encoding='utf-8')
    assert '<<<FOUNDATION-PLACEHOLDER>>>' not in text
print('foundation markdown sanity ok')
PY
```

## Review requirements

Run local multi-agent review with academic focus:

1. Story / claim-evidence reviewer。
2. Skeptical reviewer for baseline fairness, sample bias, oracle and review risk。
3. Execution verifier for PR body executability, acceptance criteria, links and old-sprint residue。

C/I issues must be fixed before ready; M issues can be recorded as follow-up。
