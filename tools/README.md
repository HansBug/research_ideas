# `tools/` README

## 1. 路径定位

`tools/` 用于存放本仓库内可复用的脚本、命令行工具和配套工作流说明。

当前这里既服务于论文全文提取，也服务于 `frontier_index/` 下的年度论文索引构建。

## 2. 当前工具清单

1. [pdf_extractor.py](./pdf_extractor.py)
   - 从单篇 `paper.pdf` 提取 `paper_content.txt`。
   - 适用于正式论文集路径中的全文整理阶段。
2. [ccf_se_index_builder.py](./ccf_se_index_builder.py)
   - 批量生成 `CCF` 软件工程/系统软件/程序设计语言方向年度索引。
   - 输出年度 `README.md`、`verification.json`、`metadata/*.json`、`bib/*.bib`。
3. [ccf_se_index_workflow.md](./ccf_se_index_workflow.md)
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
├── bib/
└── _cache/
```

推荐顺序：

1. 先运行构建器生成全量结果。
2. 再检查 `verification.json` 是否全部 `ok`。
3. 再按 `frontier_index/SOFTWARE_ENGINEERING_FIELD_TREE.md` 与 `frontier_index/CCF_SE_A_B_C.md` 补录 `macro_area / se_inclusion_decision / se_primary_path / se_decision_basis` 等分类字段。
4. 若发现 venue 边界、重名覆盖、字段缺失等问题，优先改脚本并重跑，不手工补半成品。
5. 最后再回写 `frontier_index/` 入口文档中的统计和说明。

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

1. `ccf_se_index_builder.py` 的 `_cache/` 不应随意删除，否则重跑会显著变慢。
2. 年度索引默认应视为“可重建产物”，发现规则问题时优先修脚本，不优先手工改生成文件。
3. 当前构建器的职责是生成**基础元数据层**；软工/非软工终判与 `x.x.x` 路径回填属于后续分类补录阶段。
4. `pdf_extractor.py` 主要服务正式论文集路径，不应把 `frontier_index/` 直接当全文文库来批量提取。
