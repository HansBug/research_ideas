# PR-B0 强化任务包：全文级 baseline review 与总账升级

## 1. 范围

本任务包服务 PR [#105](https://github.com/HansBug/research_ideas/pull/105)。原 PR-B0 已完成 LLM-based SLR / agentic literature-review 近邻 baseline 的粗筛和 25 篇 P0/P1 建库；本强化迭代把它升级为可支撑 paper2 CCF A 类写作的全文证据级 baseline 文库。

## 2. 允许修改文件

- `project_1_llm_state_machine_modeling/paper_agent_based_slr/baselines/**`
- `project_1_llm_state_machine_modeling/paper_agent_based_slr/plan/**`
- PR #105 body / comments

## 3. 非目标

| 非目标 | 说明 |
|---|---|
| 不实现 agent 工作流 | 本 PR 只做 related work / baseline 文库。 |
| 不运行真实 LLM | 只有读论文和写文档；若后续真实 LLM 调用必须 `source .env` 并记录 run record。 |
| 不声称完成正式 SLR | 当前是 baseline review，不是 PRISMA 完整系统综述。 |
| 不绕过付费墙 | WSESE / IEEE 等闭源 PDF 只记录人工下载需求。 |

## 4. 输入证据

- [baselines/search/arxiv-query-results.jsonl](../../baselines/search/arxiv-query-results.jsonl)：34 篇候选元数据。
- [baselines/papers/](../../baselines/papers/)：P0/P1/P2 本地 PDF、文本、BibTeX 与 review。
- [baselines/GUIDE.md](../../baselines/GUIDE.md)：全文 review 模板和 D1-D7 标准。
- [baselines/SUMMARY.md](../../baselines/SUMMARY.md)：总账和 story 定调。

## 5. 执行计划

1. 更新 [../../baselines/GUIDE.md](../../baselines/GUIDE.md)，固化全文 `review.md` 模板、D1-D7 全文评分规则和 `SUMMARY.md` 描述性主表要求。
2. 把 9 篇 P2 重要 arXiv 背景候选补成本地目录，确保 `paper.pdf`、`paper_content.txt`、`bibtex.bib`、`review.md` 齐全。
3. 对每篇本地论文按 `bibtex.bib -> paper_content.txt -> paper.pdf` 信息流全文阅读并重写 `review.md`。
4. 重构 [../../baselines/SUMMARY.md](../../baselines/SUMMARY.md)：主表必须含输入、输出、方法、阶段、人审/审计、实验/指标、发现、D1-D7、paper2 作用。
5. 更新 [../progress.md](../progress.md) 的 B0 强化记录、验证命令和 capability-use audit。
6. push 后启动 codex / claude / deepseek 三路 review，要求从学术准确性、事实可追溯性、CCF A 级 story 支撑性角度强对抗审查。
7. 按 `$ai-research-writing-skill` 主张-证据口径补强快速结论卡片 / SUMMARY 字段：单篇 `review.md` 必须显式包含作者/venue/出版状态、研究脉络、引用角色、LLM/agent 角色、证据溯源粒度、威胁/支持 paper2 主张、paper2 应避免的主张、baseline 可用性、可复现资产/阻塞项；SUMMARY 必须新增对应主张-证据与可用性总表。
8. 继续吸收字段体系审稿意见：单篇 `review.md` 快速卡片必须拆出 `受影响主张 ID`、`威胁类型`、`不覆盖阶段`、`人类角色`、`审计时机`、`主张追踪状态`、`决策日志状态`、`审计导出性`、`模型/API 设置`、`提示词状态`、`温度/重复/随机种子`、`代码状态`、`数据状态`、`许可状态`、`运行可行性`、`关键结果锚点`、`数值使用许可`；[../../baselines/SUMMARY.md](../../baselines/SUMMARY.md) 对应拆成主张绑定、审计/provenance、可复现资产三张表，避免泛化字段支撑 CCF-A 级写作。


## 6. 拒收检查

- 任一本地论文缺 `paper.pdf` / `paper_content.txt` / `bibtex.bib` / `review.md`。
- P0/P1 `review.md` 仍只有 title/abstract 粗筛式描述。
- `SUMMARY.md` 主表只有 D1-D7，没有输入、输出、方法、阶段、审计、实验、发现等描述性列。
- 把 arXiv 写成 peer-reviewed / CCF 事实。
- 写出“首次自动化 SLR / 首次 agentic SLR / 完整覆盖 / PRISMA 合规”等 unsupported claim。
- WSESE@ICSE 2025 这类拿不到 PDF 的论文被写成已全文核验。
- 单篇 `review.md` 快速结论卡片缺少主张-证据 / baseline 可用性字段，或 `分层` 写成“全文建议 P0/P1”导致与 SUMMARY 总账冲突。
- 单篇 `review.md` 把 expert gold、human evaluation、运行中人工审计、claim-to-source、decision log 混成一个字段，导致 paper2 差异化无法判断。
- `SUMMARY.md` 只写“代码/数据/提示词/许可待复核”这类泛化阻塞项，不能区分代码状态、数据状态、许可状态和运行可行性。
- `SUMMARY.md` 写入 AUC、F1、accuracy、cost、win-rate、time saving 等数字，但没有 `关键结果锚点` / `数值使用许可`，导致正式写作时证据链断点。
- `review.md` 或 `SUMMARY.md` 仅因正文出现 `code`、`dataset`、`GitHub Copilot`、`benchmark dataset` 等普通词，就写成“声称有代码/数据”；代码/数据状态必须来自明确 artifact / data availability 语句。
- 准备把某篇 work 当作可运行 baseline 时，没有记录 artifact claim、URL 状态、license、local clone/download 状态、smoke 结果或阻塞原因。
- 计划把某个 baseline 结论写入 CCF A 类正文 / rebuttal 时，没有记录方法假设、可比性边界、负面证据、failure modes、metric limitations、伦理/IRB/data/copyright flag、claim strength 与 source/number anchor。

## 7. 验证命令

```bash
source venv/bin/activate
python - <<'PY'
from pathlib import Path
root = Path('project_1_llm_state_machine_modeling/paper_agent_based_slr/baselines')
missing = []
for d in sorted(p for p in (root / 'papers').iterdir() if p.is_dir()):
    for name in ['paper.pdf', 'paper_content.txt', 'bibtex.bib', 'review.md']:
        if not (d / name).exists():
            missing.append(str(d / name))
assert not missing, missing
summary = (root / 'SUMMARY.md').read_text(encoding='utf-8')
for col in ['输入', '输出', '方法', '覆盖阶段', '审计', '实验', '主要发现', '受影响主张 ID', '威胁类型', '不覆盖阶段', '主张追踪状态', '运行可行性', '数值使用许可']:
    assert col in summary, col
for p in (root / 'papers').iterdir():
    if p.is_dir():
        review = (p / 'review.md').read_text(encoding='utf-8')
        for col in ['作者 / venue / 出版状态', '研究脉络', '引用角色', 'LLM/agent 角色', '证据溯源粒度', '不覆盖阶段', '人类角色', '审计时机', '主张追踪状态', '决策日志状态', '审计导出性', '模型/API 设置', '提示词状态', '温度/重复/随机种子', '关键结果锚点', '数值使用许可', '受影响主张 ID', '威胁类型', '威胁的 paper2 主张', '支持的 paper2 主张', 'paper2 应避免的主张', 'baseline 可用性', '代码状态', '数据状态', '许可状态', '运行可行性', '可复现资产 / 阻塞项']:
            assert col in review, (p.name, col)
        assert '全文建议 P0' not in review and '全文建议 P1' not in review, p.name
        assert '声称有/正文出现 GitHub 或 code 线索' not in review, p.name
        assert '声称有/正文出现 dataset 或 data availability 线索' not in review, p.name
assert '声称有/正文出现 GitHub 或 code 线索' not in summary
assert '声称有/正文出现 dataset 或 data availability 线索' not in summary
for bad in ['first automated SLR', 'first agentic SLR', 'complete coverage', 'PRISMA' + '-compliant']:
    assert bad not in summary, bad
print('B0 fulltext baseline sanity ok')
PY

git diff --check
# 若 paper_content.txt 由 PDF 提取产生行尾空白 / NUL，必须先清理或在 GUIDE 中显式调整 gate；不得把失败命令记为通过。
```

## 8. Review gate

三路 reviewer 必须检查：

1. 每篇 review 是否真正基于全文证据，而不是模板化扩写。
2. D1-D7 是否被全文证据支持。
3. SUMMARY 主表是否能让读者一眼看到输入、输出、方法、实验、审计和 paper2 作用。
4. SUMMARY 主表是否已经拆出主张 ID、威胁类型、阶段边界、人类角色、审计时机、主张追踪、决策日志、代码/数据/许可/提示词、运行可行性和数值使用许可，而不是只靠 D1-D7 或泛化阻塞项。
5. 是否充分承认强 baseline，避免虚假 novelty。
6. 是否保留人工下载 / coverage gap / arXiv 未审稿等风险。
