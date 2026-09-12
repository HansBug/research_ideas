# System Architects Are not Alone Anymore: Automatic System Modeling with AI — artifacts / resource 盘点

## 1. 一手资源入口

| 资源对象 | 当前判断 |
|---|---|
| 论文本体 | [HAL](https://telecom-paris.hal.science/hal-04483279) / [DOI](https://doi.org/10.5220/0012320100003645) |
| 作者代码 / 工具 | 作者 artifact [GitHub zebradile/ttool-ai](https://github.com/zebradile/ttool-ai) |
| NL / 输入数据 | 仓库含 `.desc` specs、TTool `.xml`、`results.ods` |
| STM / repair case / 输出 | 可从 artifact 中切片 SMD，但需分离 BD/IBD/SMD |
| 许可 | 待核 |
| 版本 / commit / hash | 需冻结 commit |

## 2. 本地证据容器

本目录中的 `paper.pdf`、`paper_content.txt` 与 `bibtex.bib` 只作为本仓库审计材料，不等同于论文一手公开资源。资源可获取性判断必须以上表的一手入口为准。

## 3. 可复现阻塞

- 若代码、数据、许可或版本为待核，后续不得把该条目写成可直接复跑 baseline。
- 若目标工件不是 STM family，后续只能作为异构 related work / 方法近邻使用。
- 若 repair 依赖 oracle、专家、人机选择或私有数据，实验对比时必须降级为条件对照或 related work；若缺少 NL 或 `NL -> STM_0` 关系，不得称为本文 baseline。
