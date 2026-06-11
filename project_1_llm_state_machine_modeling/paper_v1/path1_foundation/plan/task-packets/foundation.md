# Path-1 论文奠基 PR 任务包

## 范围

创建一个新 PR，作为 Project 1 第一篇 Path-1 paper 后续工作的 foundation。PR body 和仓库文档必须能让后续 agent / 人类直接沿着它执行 story freeze、baseline selection、sample registry、oracle protocol、experiments、writing 和 submission。

## 允许修改文件

- `project_1_llm_state_machine_modeling/paper_v1/README.md`
- `project_1_llm_state_machine_modeling/paper_v1/path1_foundation/**`
- PR body / PR comments

## 本 PR 不修改文件

- `project_1_llm_state_machine_modeling/method/**`
- `project_1_llm_state_machine_modeling/eval/**`
- `project_1_llm_state_machine_modeling/baselines/**`
- `runs/**`
- 实验代码 / provider 配置 / `.env`

## 必需证据

- PR #9 historical assets：selection、expansion、ref_stms、PATH1_REPORT。
- PR #31 / project_1 talks：导师对 Path-1、E1/E2、Hybrid、Path-2 的定调。
- PR #22 / method docs：当前 agent-loop / skill / run-record 事实。
- issue #67：2026 夏季投稿计划，尤其“按 CCF-A 论文标准打磨，2026 夏季优先投 CCF-B 期刊；主投 SoSyM regular，ASEJ / REJ 作备投”的 venue strategy。
- PR [#94](https://github.com/HansBug/research_ideas/pull/94) / S1a baseline 总账与逐篇文件、PR [#92](https://github.com/HansBug/research_ideas/pull/92)：closest prior work matrix、2025-2026 arXiv baseline / 强近邻再摸排增量、九个 direct baseline 的分层结论。

## 拒收检查

- 不能把 PR #9 selection / expansion / historical early reference drafts 写成当前 paper result。
- 不能把第一篇主线写成 Path-2、Hybrid、DSL、LangGraph、Codex/Claude 主线。
- 不能声明已有主实验 lift / SOTA / same-benchmark win。
- 不能把 LLM-as-Judge 写成主 oracle。
- 不能把 parse/semantic/sim 写成完整 formal verification。
- PR body 必须包含范围、非目标、执行计划、ready gate 和目标 venue/readiness gate，并尽量使用中文；Mermaid 节点也应使用中文，英文只保留必要术语。
- PR #94 / S1a 已完成九个 direct baseline 的逐篇阻塞吸收；后续 S1b/S3 必须消费其逐篇反证、same-sample approximate / near / evidence-only / boundary 分层和四个 mandatory closest works carve-out，不能退回只读旧 SUMMARY 或基于过期 baseline corpus 冻结 competitor。
- 后续 S0b-S7 必须按 [../../story/venue_readiness_gate.md](../../story/venue_readiness_gate.md) 的 CCF-A 标准门禁执行；目标投 B 不等于降低实验和写作标准。

## 验证命令

```bash
git status --short --branch
find project_1_llm_state_machine_modeling/paper_v1/path1_foundation -type f | sort
python - <<'PY'
from pathlib import Path
for p in Path('project_1_llm_state_machine_modeling/paper_v1/path1_foundation').rglob('*.md'):
    text = p.read_text(encoding='utf-8')
    placeholder = '<<<' + 'FOUNDATION-PLACEHOLDER' + '>>>'
    assert placeholder not in text
print('foundation markdown sanity ok')
PY
```

## Review 要求

运行本地多智能体学术 review，重点关注：

1. 论文 story / claim-evidence reviewer。
2. baseline 公平性、样本偏差、oracle 与 review 风险的 skeptical reviewer。
3. PR body 可执行性、验收标准、链接和旧 sprint 残留的 execution verifier。

C/I 问题必须修复后才能 ready；M 问题可以记录为 follow-up。
