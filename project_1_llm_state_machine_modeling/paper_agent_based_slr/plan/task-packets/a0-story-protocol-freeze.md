# PR-A0 任务包：主线与协议冻结

## 1. 范围

本 PR 是 PR [#101](https://github.com/HansBug/research_ideas/pull/101) 下的 PR-0 / PR-A0，负责在 `project_1_llm_state_machine_modeling/paper_agent_based_slr/` 中落地第二篇 agent-based SLR 论文的 story、协议、术语、claim gate、事实漂移政策、相关工作边界、评价维度种子和 reviewer risk register。

## 2. 允许修改文件

- `project_1_llm_state_machine_modeling/paper_agent_based_slr/**`
- PR #103 body / comments

## 3. 本 PR 不修改

| 路径或资产 | 不修改理由 |
|---|---|
| `project_1_llm_state_machine_modeling/method/**` | A0 只冻结论文 story 与协议，不改 agent-loop / runtime 代码。 |
| `project_1_llm_state_machine_modeling/eval/**` | A0 不实现评价脚本，A5 才冻结指标和统计协议。 |
| `project_1_llm_state_machine_modeling/sources/**` | A0 只把 `sources/` 登记为候选场景，不改既有文库。 |
| `runs/**` | A0 不运行真实 LLM 或真实场景，因此不新增 run record。 |
| `.env` | A0 不触发 provider 调用，也不改本地密钥配置。 |
| PR #97 分支资产 | A0 只按 OPEN / snapshot / 分支局部证据引用，不复制未合入资产。 |

## 4. 必需证据

- PR [#101](https://github.com/HansBug/research_ideas/pull/101)：第二篇 agent-based SLR umbrella contract。
- PR [#99 comment](https://github.com/HansBug/research_ideas/pull/99#issuecomment-4689018818)：2026-06-12 会后定调。
- [2026-06-12 导师讨论记录](../../../talks/2026-06-12-导师-两篇论文转向与模型修正定调.md)：已合入正式导师讨论文库。
- PR [#97](https://github.com/HansBug/research_ideas/pull/97)：OPEN / 未合入 / snapshot evidence。
- PR [#96](https://github.com/HansBug/research_ideas/pull/96)：旧 Path-1 路径结构参考。

## 5. 拒收检查

- 不能把第二篇写回 `sources` corpus / dataset / mapping paper。
- 不能写 agent 完全替代 SLR 专家。
- 不能写 PRISMA-compliant，除非后续 checklist 真闭合。
- 不能写 complete coverage 或 first automated SLR。
- 不能把 PR #97 OPEN / 未合入资产写成 `main` fact。
- 不能创建 `foundation/` 子路径层。
- 不能冻结 A5 才该负责的指标公式、阈值或统计协议。
- 不能运行真实 LLM；如后续真实运行必须 `source .env` 并保留 run record。

## 6. 验证命令

```bash
git status --short --branch
find project_1_llm_state_machine_modeling/paper_agent_based_slr -maxdepth 4 -type f | sort
python - <<'PY'
from pathlib import Path
root = Path('project_1_llm_state_machine_modeling/paper_agent_based_slr')
required = [
    root / 'README.md',
    root / 'story' / 'README.md',
    root / 'story' / 'paper_story.md',
    root / 'story' / 'protocol.md',
    root / 'story' / 'terminology_policy.md',
    root / 'story' / 'claim_evidence_map.md',
    root / 'story' / 'differential_novelty_matrix.md',
    root / 'story' / 'paper_outline.md',
    root / 'evidence' / 'README.md',
    root / 'evidence' / 'project_inventory.md',
    root / 'evidence' / 'fact_drift_policy.md',
    root / 'evidence' / 'citation_seed_inventory.md',
    root / 'evidence' / 'references.bib',
    root / 'baselines' / 'README.md',
    root / 'baselines' / 'GUIDE.md',
    root / 'baselines' / 'SUMMARY.md',
    root / 'baselines' / 'papers' / '.gitkeep',
    root / 'dataset_selection' / 'README.md',
    root / 'dataset_selection' / 'sample_assets.md',
    root / 'experiment_design' / 'README.md',
    root / 'experiment_design' / 'evaluation_dimensions_seed.md',
    root / 'experiment_design' / 'reviewer_risk_register.md',
    root / 'plan' / 'README.md',
    root / 'plan' / 'progress.md',
    root / 'plan' / 'task-packets' / 'a0-story-protocol-freeze.md',
]
missing = [str(p) for p in required if not p.exists()]
assert not missing, missing
assert not (root / 'foundation').exists(), 'must not create foundation/ layer'
assert (root / 'baselines').exists(), 'must keep old Path-1 baselines layer'
assert (root / 'dataset_selection').exists(), 'must keep old Path-1 dataset_selection layer'
for p in root.rglob('*.md'):
    text = p.read_text(encoding='utf-8')
    if 'PR #97' in text:
        assert any(mark in text for mark in ['OPEN', '未合入', 'snapshot', '分支局部']), p
    bad_terms = [
        'PRISMA' + '-compliant',
        'first automated' + ' SLR',
        'complete' + ' coverage',
        '完全' + '替代',
        '替代 SLR' + ' 专家',
    ]
    allowed_context = ['禁止', '不声称', '不得', '避免', '不能', '风险', '待核验', '边界']
    for bad in bad_terms:
        if bad in text:
            lines = [line for line in text.splitlines() if bad in line]
            assert all(any(flag in line for flag in allowed_context) for line in lines), (p, bad, lines)
needles = ['SLR', 'SMS', 'PRISMA', 'ASReview', 'RobotReviewer', 'systematic review automation', 'LLM-assisted']
novelty = (root / 'story' / 'differential_novelty_matrix.md').read_text(encoding='utf-8')
missing_needles = [n for n in needles if n not in novelty]
assert not missing_needles, missing_needles
print('paper_agent_based_slr A0 sanity ok')
PY
```

## 7. Review 要求

三路 reviewer 必须检查：

1. 与 PR #101 / 导师定调一致。
2. 路径结构符合用户要求，无 `foundation/` 子层。
3. A0 不跑四个真实例子，且不触发真实 LLM。
4. PR #97 事实漂移政策可执行。
5. terminology / claim / novelty / risk / evidence 文档能指导 A1-A5。
6. 旧 Path-1 的 `baselines/` 与 `dataset_selection/` 层级已在本工作区保留，但 A0 只登记相关工作锚点和候选场景，不冻结真实 benchmark。
7. C/I 必须修复；M 可 follow-up。

## 8. A1 接力 gate

A1 启动前必须先做 PR #97 snapshot 等值断言，避免 A0 记录的 `b8b7e72dbb1d5d2b7b09a6b9d1b40268c2f1a727` 因 PR #97 更新而漂移。建议使用：

```bash
gh pr view 97 --repo HansBug/research_ideas --json state,headRefOid
python - <<'PY'
from pathlib import Path
import json
import subprocess
root = Path('project_1_llm_state_machine_modeling/paper_agent_based_slr')
expected = 'b8b7e72dbb1d5d2b7b09a6b9d1b40268c2f1a727'
actual = json.loads(subprocess.check_output([
    'gh', 'pr', 'view', '97', '--repo', 'HansBug/research_ideas', '--json', 'headRefOid'
]))['headRefOid']
assert actual == expected, (actual, expected)
for rel in ['evidence/fact_drift_policy.md', 'story/claim_evidence_map.md']:
    text = (root / rel).read_text(encoding='utf-8')
    assert expected in text, rel
print('PR #97 snapshot equality gate ok')
PY
```

若断言失败，A1 必须先更新 [../../evidence/fact_drift_policy.md](../../evidence/fact_drift_policy.md)、[../../story/claim_evidence_map.md](../../story/claim_evidence_map.md) 与 [../../evidence/project_inventory.md](../../evidence/project_inventory.md)，再继续资产盘点。
