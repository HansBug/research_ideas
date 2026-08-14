# #85 基线相关工作初筛基础任务包

## 范围

- 新建 `paper_stm_source_landscape/`，采用 PR #96 论文工作区的六层分工思路。
- 落地 #95 438 行审计、69 行 D1--D7 初筛、25 条人工下载 BibTeX、21 条自动全文复查门禁。
- 建立论文主线 / 声明 / 证据 / 实验 / 计划入口。

## 允许修改文件

- `project_1_llm_state_machine_modeling/paper_stm_source_landscape/**`
- PR body / PR comments

## 本 PR 不修改文件

- `sources/` 单篇论文目录。
- 按单论文文库规范提交 `paper.pdf` 与 `paper_content.txt`；不在 PR comment / 论文正文中复制长段原文。
- 不运行真实 LLM，不读取 `.env`。

## 拒收检查

1. 出现带顺序含义的版本化命名，或把 #85 写成 `paper_v1` 后续版本。
2. 缺少 `baselines/data/screening_audit.csv` 或不足 438 行。
3. 缺少 `baselines/data/manual_download_needed.bib` 或 P0/P1 不完整。
4. 缺少 `auto_fulltext_light_review_gate.csv` 或未记录 21 条复查门禁。
5. 把仅元数据判断写成已核验直接近邻。


## 补充范围：P0/P1 全文级 baseline

用户已提供 P0/P1 本地私有 PDF，本 PR 将原“下载队列”升级为 paper 内部 `survey_baseline_library/`：提交单篇 `paper.pdf`、`paper_content.txt`、`bibtex.bib`、`fulltext_review.md` 四件套，并同步 receipt、短哈希、页码定位、短转述、D1--D7 全文级评分。
