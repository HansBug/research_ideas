# PAT-Agent: Autoformalization for Model Checking — artifacts / resource 盘点

## 1. 一手资源入口

| 资源对象 | 当前判断 |
|---|---|
| 论文本体 | [arXiv](http://arxiv.org/abs/2509.23675) |
| 作者代码 / 工具 | [GitHub PAT-Agent](https://github.com/ZuoXinyue/PAT-Agent) |
| NL / 输入数据 | 仓库含 Datasets / Experiments_Demo 等线索 |
| STM / repair case / 输出 | 有 formal-model repair pipeline，但非 STM `<NL, STM_0>` pair |
| 许可 | 待核 |
| 版本 / commit / hash | 需冻结 commit |

## 2. 本地证据容器

本目录中的 `paper.pdf`、`paper_content.txt` 与 `bibtex.bib` 只作为本仓库审计材料，不等同于论文一手公开资源。资源可获取性判断必须以上表的一手入口为准。

## 3. 可复现阻塞

- 若代码、数据、许可或版本为待核，后续不得把该条目写成可直接复跑 baseline。
- 若目标工件不是 STM family，后续只能作为异构 related work / 方法近邻使用。
- 若 repair 依赖 oracle、专家、人机选择或私有数据，实验对比时必须降级为条件对照或 related work；若缺少 NL 或 `NL -> STM_0` 关系，不得称为本文 baseline。
