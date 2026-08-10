# TarTar: A Timed Automata Repair Tool — artifacts / resource 盘点

## 1. 一手资源入口

| 资源对象 | 当前判断 |
|---|---|
| 论文本体 | [https://doi.org/10.1007/978-3-030-53288-8_25](https://doi.org/10.1007/978-3-030-53288-8_25) |
| 作者代码 / 工具 | https://github.com/sen-uni-kn/TarTar |
| NL / 输入数据 | 无可用于本文 `<NL, STM_0>` 的原生 NL requirements pair |
| STM / repair case / 输出 | 论文、GitHub/TarTar 入口可得；无 NL/STM pair。 |
| 许可 | 待按一手仓库 / 出版页二次核验；本地 PDF 不等同于 artifact license |
| 版本 / commit / hash | 待冻结；若进入实验对照必须记录 commit / release / 下载日期 |

## 2. 本地证据容器

本目录中的 `paper.pdf`、`paper_content.txt` 与 `bibtex.bib` 只作为本仓库审计材料，不等同于论文一手公开资源。资源可获取性判断必须以上表的一手入口为准。

## 3. 可复现阻塞

- 若代码、数据、许可或版本为待核，后续不得把该条目写成可直接复跑 baseline。
- 若目标工件不是本文 STM family，后续只能作为异构 related work / 方法近邻使用。
- 若 repair 依赖 oracle、专家、人机选择或私有数据，实验对比时必须降级为条件对照或 related work；若缺少 NL 或 `NL -> STM_0` 关系，不得称为本文 baseline。
