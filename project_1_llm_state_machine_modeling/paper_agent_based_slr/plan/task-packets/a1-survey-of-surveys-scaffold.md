# PR-A1 任务包：综述之综述脚手架文库

## 1. 目标

本任务包对应 PR-A1：在 [../../survey_of_surveys/](../../survey_of_surveys/) 建立综述之综述脚手架文库，验证它能通过真实 dry-run 抽取 RQ、维度、finding、证据呈现、validity 和报告结构模式，并能管理 schema 回修与人工下载失败路径。

## 2. 背景事实

1. 上游 PR #101 已把 Paper2 后续流程重构为 A1 文库奠基 → A2a 核心样本 → A2b 完整文库 → A3 schema / contract。
2. PR #129 已关闭不合并；旧 LLM4STM 种子盘点不再是 A1。
3. A1 不运行真实大语言模型，不读取 `.env`，不跑四个真实例子。
4. A1 必须证明 GUIDE / schema 能指导真实样例，而不是只写空结构。

## 3. 允许修改范围

- [../../survey_of_surveys/](../../survey_of_surveys/)
- [../../README.md](../../README.md)
- [../progress.md](../progress.md)
- 本任务包
- 必要时同步 [../../evidence/project_inventory.md](../../evidence/project_inventory.md)、[../../evidence/citation_seed_inventory.md](../../evidence/citation_seed_inventory.md)、[../../evidence/references.bib](../../evidence/references.bib)

## 4. 不在本 PR 中修改

- 不修改运行时代码。
- 不冻结 A3 schema / validator。
- 不做 100+ 完整文库。
- 不把 survey_of_surveys 样本写成目标领域 evidence pool。
- 不把 metadata-only 条目写成已读全文；当前历史 metadata-only 条目已补齐全文并完成证据升级。

## 5. 必须交付

- [x] `survey_of_surveys/README.md`
- [x] `survey_of_surveys/GUIDE.md`
- [x] `survey_of_surveys/SUMMARY.md`
- [x] `survey_of_surveys/search/README.md`
- [x] `survey_of_surveys/search/search-log.md`
- [x] `survey_of_surveys/search/candidate-pool.md`
- [x] `survey_of_surveys/search/manual-download-needed.bib`
- [x] `survey_of_surveys/patterns/README.md`
- [x] `survey_of_surveys/patterns/pattern-field-schema.md`
- [x] `出版形态`、`期刊/会议/预印本`、`CCF 官方大类`、`CCF 官方等级`、`CCF 复核状态` 字段已同步到 SUMMARY、candidate-pool 和单篇 review。
- [x] 至少 3 篇全文文本级 dry-run；本轮累计完成 19 篇全文文本级（初始 9 篇 + #95 十篇）。
- [x] 至少 1 个 manual-download / metadata-only 失败路径；本轮历史 3 篇已完成“下载失败 → 用户补 PDF → 全文升级 → active 清零”闭环。
- [x] #95 十篇现代维度锚点已建立单篇目录、BibTeX、metadata、PDF 和 `paper_content.txt`。
- [x] #95 十篇现代维度锚点已完成一篇一 subagent 全文 `review.md` 并回填 SUMMARY；roadmap / proposal 条目已机器可读排除出统计池。
- [x] A1-M0--M6 元维度字段已写入 GUIDE、schema、SUMMARY、candidate-pool 和 19 篇单篇 review。
- [x] issue #95 十篇来源审计已写入 `survey_of_surveys/search/issue95-selection-audit.md`。
- [x] `survey_of_surveys/SUMMARY.md` 已按长期文库总账重构：统一论文主表按年份降序排列，不再按 PR 批次拆分。
- [x] `survey_of_surveys/SUMMARY.md` 与 `survey_of_surveys/GUIDE.md` 已明确主统计池、方法学参考池、schema seed / boundary pool 三类证据池标准。
- [x] `survey_of_surveys/SUMMARY.md` 已包含 19 篇 × A1-M0--M6 逐篇覆盖矩阵，作为后续 A2a/A2b 接力的 SUMMARY 级总账视图。
- [x] `survey_of_surveys/SUMMARY.md` 统一主表已包含 `CCF 复核状态` 独立列，避免 CCF A/B/C 字面值脱离“本地缓存；官方待人工复核”口径。
- [x] `survey_of_surveys/SUMMARY.md` 已恢复结构化“schema 修订 / 回填日志”，并同步 GUIDE / schema 的回修入口。

## 6. 拒收检查

1. 如果 `SUMMARY.md` 声称完整 tertiary review、PRISMA 合规或目标 evidence pool，应拒收。
2. 如果 active metadata-only 条目进入已采纳 pattern，应拒收；已经补齐全文并重写 review / metadata 的历史条目不再视为 metadata-only。
3. 如果 schema 回修没有记录触发条目、受影响字段和回填状态，应拒收。
4. 如果 `plan/progress.md` 仍停留在旧 PR-S0 当前阶段，应拒收。
5. 如果 `SUMMARY.md`、`search/candidate-pool.md` 或单篇 `review.md` 缺少出版形态、venue 短名链接、CCF 官方大类、CCF 官方等级、CCF 复核状态字段，应拒收。
6. 如果新增 #95 十篇锚点未明确阅读状态，或把 roadmap / vision 条目当成 SLR/SMS 已采纳 pattern，应拒收。
7. 如果 GUIDE / schema / SUMMARY 未同步 A1-M0--M6 元维度，或单篇 review 只写六类 pattern 不写 A1-M0--M6，应拒收。
8. 如果 `SUMMARY.md` 主论文表仍按“初始 dry-run”“#95 十篇”“本轮新增”等 PR 批次拆分，而不是一个长期统一主表，应拒收。
9. 如果 `SUMMARY.md` 没有明确主统计池、方法学参考池、schema seed / boundary pool 的进入标准，或把 roadmap / proposal / guideline 与完成型 SLR/SMS/MLR 统计池混算，应拒收。
10. 如果 `SUMMARY.md` 没有提供 19 篇 × A1-M0--M6 的逐篇覆盖矩阵，应拒收。
11. 如果 `SUMMARY.md` 统一主表只有 `CCF 等级` 字面值而没有 `CCF 复核状态` 独立列，应拒收。
12. 如果 `SUMMARY.md` 没有结构化“schema 修订 / 回填日志”，或该日志缺少时间、触发条目、受影响字段、修订内容、回填状态和冻结理由，应拒收。

## 7. dry-run 验收

A1 dry-run 必须满足：

- 至少 2 类综述类型。
- 至少 1 篇高等级来源；同时区分高等级来源与 CCF 官方等级，不能把非 CCF venue 写成 CCF A/B/C。
- 至少 1 篇非顶级来源。
- 至少 1 篇非 LLM4SE 的 SE 子领域。
- 六类 pattern 中至少 4 类被实际填充。
- 至少 1 个“不适用 / 证据不足”降级记录。
- schema 缺口已回修或明确留给 A2a/A2b。

当前验收记录见 [../../survey_of_surveys/SUMMARY.md](../../survey_of_surveys/SUMMARY.md) §1、§3、§4、§5、§6、§7、§7.1、§8，其中 §3 是统一年份降序主表，§4 是证据池 / 统计池解释，§5 是 A1-M0--M6 定义，§6 是逐篇覆盖矩阵，§7 是 pattern 总结，§7.1 是 schema 修订 / 回填日志，§8 是风险。

## 8. 验证命令

```bash
git diff --check
python - <<'PY'
from pathlib import Path
root = Path('project_1_llm_state_machine_modeling/paper_agent_based_slr/survey_of_surveys')
required = [
    'README.md', 'GUIDE.md', 'SUMMARY.md',
    'search/README.md', 'search/search-log.md', 'search/candidate-pool.md', 'search/manual-download-needed.bib',
    'papers/.gitkeep', 'patterns/README.md', 'patterns/pattern-field-schema.md',
]
missing = [p for p in required if not (root / p).exists()]
if missing:
    raise SystemExit(f'missing files: {missing}')
reviews = list((root / 'papers').glob('*/review.md'))
texts = list((root / 'papers').glob('*/paper_content.txt'))
metas = list((root / 'papers').glob('*/metadata.json'))
pdfs = list((root / 'papers').glob('*/paper.pdf'))
if len(reviews) != 19 or len(metas) != 19 or len(texts) != 19 or len(pdfs) != 19:
    raise SystemExit(f'unexpected dry-run asset counts: reviews={len(reviews)}, metas={len(metas)}, pdfs={len(pdfs)}, texts={len(texts)}')
for f in reviews:
    t = f.read_text(encoding='utf-8')
    for marker in ['出版形态', '期刊/会议/预印本', 'CCF 官方大类', 'CCF 官方等级', 'CCF 复核状态', 'A1-M0', 'A1-M6']:
        if marker not in t:
            raise SystemExit(f'{f} missing {marker}')
print('survey_of_surveys A1 skeleton and dry-run assets ok')
PY
rg -n "首次自动化|PRISMA-compliant|完整覆盖|替代专家|100\+ 篇完整文库完成" project_1_llm_state_machine_modeling/paper_agent_based_slr/survey_of_surveys || true
```

SUMMARY 总账结构返工复验：

```bash
python - <<'PY'
from pathlib import Path
import re
root = Path('project_1_llm_state_machine_modeling/paper_agent_based_slr/survey_of_surveys')
summary = (root / 'SUMMARY.md').read_text(encoding='utf-8')
for bad in ['### 5.1 A1 初始 dry-run', '### 5.2 #95 十篇现代维度锚点', 'A1 初始 dry-run 与失败路径', '#95 十篇现代维度锚点']:
    if bad in summary:
        raise SystemExit(f'batch table residue: {bad}')
sec = re.search(r'## 3\. 统一论文总表.*?(?=\n## 4\.)', summary, re.S).group(0)
years = [int(m.group(1)) for m in re.finditer(r'\| 🟢 \| (\d{4}) \|', sec)]
if len(years) != 19 or years != sorted(years, reverse=True):
    raise SystemExit(f'unexpected year order: {years}')
mat = re.search(r'## 6\. A1-M0--M6 逐篇覆盖矩阵.*?(?=\n## 7\.)', summary, re.S).group(0)
rows = [line for line in mat.splitlines() if line.startswith('| [')]
if len(rows) != 19:
    raise SystemExit(f'unexpected matrix rows: {len(rows)}')
table_header = re.search(r'## 3\. 统一论文总表.*?(?=\n\|---)', summary, re.S).group(0)
if 'CCF 复核状态' not in table_header:
    raise SystemExit('SUMMARY main table missing CCF 复核状态')
schema_log = re.search(r'### 7\.1 schema 修订 / 回填日志.*?(?=\n## 8\.)', summary, re.S).group(0)
for col in ['触发条目', '受影响字段', '修订内容', '回填状态', '冻结理由']:
    if col not in schema_log:
        raise SystemExit(f'schema log missing {col}')
manual = (root / 'search/manual-download-needed.bib').read_text(encoding='utf-8')
active = [line for line in manual.splitlines() if line.lstrip().startswith('@')]
counts = (
    len(list((root / 'papers').glob('*/review.md'))),
    len(list((root / 'papers').glob('*/metadata.json'))),
    len(list((root / 'papers').glob('*/paper.pdf'))),
    len(list((root / 'papers').glob('*/paper_content.txt'))),
    len(active),
)
if counts != (19, 19, 19, 19, 0):
    raise SystemExit(f'unexpected asset counts: {counts}')
for d in (root / 'papers').iterdir():
    if d.is_dir():
        txt = (d / 'review.md').read_text(encoding='utf-8')
        if not all(f'A1-M{i}' in txt for i in range(7)):
            raise SystemExit(f'{d} missing A1-M0--M6')
print('summary long-term ledger structure ok')
PY
```

## 9. 完成标准

- 本任务包、[../progress.md](../progress.md) 和 [../../README.md](../../README.md) 已同步。
- 三路 reviewer 对实现阶段给出 0C/0I 或所有 C/I 已修复。
- 文档链接检查、强主张 grep、文件存在性检查通过。

## 10. 后续接力

A2a 应从本目录 19 篇全文文本级种子出发扩展到 30--50 篇核心样本；当前没有 active manual-download-needed 条目，下一步重点是图表视觉核对、页码 / 表号证据锚定和继续补齐现代高等级 SE SLR/SMS/survey。
