# `llm_as_judge_methods_corpus/` GUIDE

## 1. 检索策略

### 1.1 推荐数据库 / 入口

- arXiv `cs.CL` / `cs.AI` / `cs.SE`
- OpenReview（NeurIPS / ICLR）
- ACL Anthology（EMNLP / ACL / NAACL findings）
- Google Scholar（兜底，引用次数 > 100 优先）

### 1.2 关键词簇构造

- 主词：`LLM-as-Judge`, `LLM as evaluator`, `LLM judge`, `auto evaluation language models`
- 修饰：`rubric`, `verbalized confidence`, `position bias`, `pairwise preference`, `RLAIF`, `fine-grained evaluation`
- Cross-domain 扩展：加 `code review`, `model evaluation`, `software engineering artifact`

### 1.3 扩词逻辑

- 找到一篇高命中（如 G-Eval）→ 看其 Related Work + 引用它的论文
- 反向追踪：哪些 paper cite 了 G-Eval / MT-Bench 这种 anchor paper

## 2. 筛选标准

### 2.1 收录

满足 README §3.1 三条硬条件：核心议题 + 方法贡献 + 评测范式。

### 2.2 降优先级

1. 与 7 篇 anchor paper（G-Eval / MT-Bench / Constitutional AI / Tian / Self-Consistency / Prometheus / JudgeLM）方法重复度 ≥ 80%
2. 评判对象与 SE artifact 完全无关（如纯 dialogue benchmark），且方法学无新颖性
3. 仅是某专域 LLM judge（如 medical），无可迁移方法学

### 2.3 排除

1. 未公开（无 arXiv / 无 venue 版本）
2. 评判对象为图像 / 多模态而非语言 artifact
3. 只用 LLM scoring 一次（无 method 创新）

## 3. 单论文目录约束

每篇必须包含：

- `paper.pdf`（PDF 原文）
- `paper_content.txt`（用 `tools/pdf_extractor.py` 抽取）
- `bibtex.bib`（论文引用）
- `DESC.md`（按 [DESC_GUIDE.md](./DESC_GUIDE.md) 写）

## 4. 工作流程

### 4.1 标准添加流程

1. 确认论文符合 §2.1 收录条件
2. 创建 `<paper-slug>/`
3. 放 `paper.pdf`（从 arXiv / OpenReview 直链下载）
4. 用 `python -m tools.pdf_extractor -i .../paper.pdf -o .../paper_content.txt -m text`
5. 若 text 模式异常 → 切 `-m ocr`
6. 写 `bibtex.bib`
7. 全文读 `paper_content.txt`，按 [DESC_GUIDE.md](./DESC_GUIDE.md) 写 `DESC.md`
8. 回填 [SUMMARY.md](./SUMMARY.md) 的论文清单

### 4.2 失败重试

- 同一篇 PDF 下载失败 → 5 天后再试
- arXiv 取不到 → 尝试 OpenReview / venue site
- 全失败 → 在 [SUMMARY.md](./SUMMARY.md) 失败记录区写明，标 `⏳ 待获取`

## 5. 一致性检查

### 5.1 SUMMARY 与目录同步

每次添加后必须更新 [SUMMARY.md](./SUMMARY.md) 的论文清单 + 当前收录概况

### 5.2 默认时间格式

更新日志使用 `yyyy-mm-dd hh:mm`（保留到分钟），可从 `git log` 回填

### 5.3 关键词簇压缩

[SUMMARY.md](./SUMMARY.md) 检索关键词簇章节默认每节 ≤ 10 行，**整合更新**而非追加；超 10 行时优先合并 / 删减历史 entry
