# #85 Baseline Related-Work Screening Foundation Task Packet

## 范围

- 新建 `paper_stm_source_landscape/`，与 PR #96 `path1_foundation/` 同构。
- 落地 #95 438 行审计、69 行 D1--D7 初筛、25 条人工下载 BibTeX、7 条 auto-fulltext 复查 gate。
- 建立 story / claim / evidence / experiment / plan 入口。

## 允许修改文件

- `project_1_llm_state_machine_modeling/paper_stm_source_landscape/**`
- PR body / PR comments

## 本 PR 不修改文件

- `sources/` 单篇论文目录。
- 不提交 PDF、全文、长摘录。
- 不运行真实 LLM，不读取 `.env`。

## 拒收检查

1. 出现 带顺序含义的版本化命名 或把 #85 写成 `paper_v1` 后续版本。
2. 缺少 `baselines/data/screening_audit.csv` 或不足 438 行。
3. 缺少 `baselines/data/manual_download_needed.bib` 或 P0/P1 不完整。
4. 缺少 `auto_fulltext_light_review_gate.csv` 或未记录 7 条复查 gate。
5. 把 metadata-only 写成 verified direct competitor。
