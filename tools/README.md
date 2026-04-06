# `tools/` README

## 1. 路径定位

`tools/` 用于存放本仓库内可复用的脚本、命令行工具和配套工作流说明。

当前这里既服务于论文全文提取，也服务于 `frontier_index/` 下的年度论文索引构建。

## 2. 当前工具清单

1. [pdf_extractor.py](./pdf_extractor.py)
   - 从单篇 `paper.pdf` 提取 `paper_content.txt`。
   - 适用于正式论文集路径中的全文整理阶段。
2. [ccf_se_index_builder.py](./ccf_se_index_builder.py)
   - 批量生成当前 `CCF_SE_A_B_C.md` 保留的 `CCF` 软件工程高相关 venue 年度索引。
   - 输出年度 `README.md`、`verification.json`、`metadata/*.json`、`venues/*.md`。
3. [ccf_se_classifier.py](./ccf_se_classifier.py)
   - 在已有年度元数据之上，对未终判条目做启发式初判，并保留已经直接写回 `metadata/*.json` 的人工终判。
   - 批量回填 `macro_area / se_inclusion_decision / se_primary_path / se_primary_label / se_secondary_paths / se_decision_basis / classification_source / manual_review_status`。
   - 同时重写年度 `README.md` 与 `venues/*.md`，把年度页收敛成“年度总览 + venue 导航”，把逐篇论文名录落到对应 venue 页。
4. [ccf_se_index_workflow.md](./ccf_se_index_workflow.md)
   - 说明 `ccf_se_index_builder.py` 的标准工作流、复核方式、分类补录阶段与缓存约束。

## 3. 标准工作流

### 3.1 构建 `CCF` 年度索引

在仓库根目录执行：

```bash
python -m tools.ccf_se_index_builder --year 2025
```

默认会写入：

```text
frontier_index/ccf_history/2025/
├── README.md
├── verification.json
├── metadata/
└── venues/
```

推荐顺序：

1. 先运行构建器生成当前保留子集结果。
2. 再检查 `verification.json` 是否全部 `ok`。
3. 再运行分类器回填软工判定与 `x.x.x` 路径：

```bash
python -m tools.ccf_se_classifier --year 2025
```

4. 若发现 venue 边界、重名覆盖、字段缺失或分类规则问题，优先改脚本并重跑，不手工补半成品。
5. 若需要把分类结果提升为可接受的终判，直接逐篇把人工复核结果写回 `frontier_index/ccf_history/<year>/metadata/*.json`，再重跑分类器。
6. 最后再回写 `frontier_index/` 入口文档中的统计和说明。

### 3.2 提取单篇论文全文

当某篇论文已经进入正式文库阶段时，优先使用：

```bash
python -m tools.pdf_extractor -i path/to/paper.pdf -o path/to/paper_content.txt -m text
```

若文字模式提取明显异常，再切换为：

```bash
python -m tools.pdf_extractor -i path/to/paper.pdf -o path/to/paper_content.txt -m ocr
```

## 4. 使用约束

1. `ccf_se_index_builder.py` 的缓存位于仓库根目录 `.cache/ccf_se_index/<year>/`，不属于年度索引正式内容，也不应提交入库。
2. 年度索引默认应视为“可重建产物”，发现规则问题时优先修脚本；若是逐篇边界裁决，则直接回写 `metadata/*.json` 中的终判字段。
3. 当前 `ccf_se_index_builder.py` 的职责是生成**基础元数据层 + 年度总页/venue 页骨架**；`ccf_se_classifier.py` 的职责是“启发式初判 + 保留已写回终判 + 年度页/venue 页重渲染”。
4. 若某个年份的 `metadata/*.json` 已全部写回人工终判，则 `ccf_se_classifier.py` 会直接保留这些终判结果并重渲染，不再依赖启发式分类输出。
5. 仅靠规则脚本不能保证“绝对正确”；逐篇人工复核完成前，`classification_source != 人工复核` 的条目都只能视为初判。
6. venue 级规范统一使用 [../frontier_index/CCF_SE_A_B_C.md](../frontier_index/CCF_SE_A_B_C.md) 中的 `软工归属级别` 与 `氛围 A 🔥 / B 🟢 / C 🟡`；若要表达跟踪优先级，直接用 `氛围`，同档再看 `软工归属级别`，不要在年度页另造第二套 venue 分级。
7. 逐篇论文层面继续沿用 `initial_screening / pdf_followup`，并按 `🟢 -> 🟡 -> ⏳ -> ⚪` 排序，不再额外发明 `A/B/C/D`。
8. `pdf_extractor.py` 主要服务正式论文集路径，不应把 `frontier_index/` 直接当全文文库来批量提取。
