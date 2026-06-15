# Generating SysML Behavior Models via Large Language Models: an Empirical Study — artifacts / resource 盘点

## 1. 一手资源入口

| 资源对象 | 当前判断 |
|---|---|
| 论文本体 | [ACM DOI](https://dl.acm.org/doi/10.1145/3755881.3755926) |
| 作者代码 / 工具 | 未发现完整 generation/repair pipeline 源码 |
| NL / 输入数据 | 论文给 [Google Drive](https://drive.google.com/drive/folders/10eo8KDqlBlkQZxPpPCB7R3-aBQZ7Rsm6?usp=drive_link) |
| STM / repair case / 输出 | 公开数据/结果较强，但 STM 子集、初始/反馈输出需切片 |
| 许可 | 待核 |
| 版本 / commit / hash | Drive 需冻结下载日期/文件清单 |

## 2. 本地证据容器

本目录中的 `paper.pdf`、`paper_content.txt` 与 `bibtex.bib` 只作为本仓库审计材料，不等同于论文一手公开资源。资源可获取性判断必须以上表的一手入口为准。

## 3. 可复现阻塞

- 若代码、数据、许可或版本为待核，后续不得把该条目写成可直接复跑 baseline。
- 若目标工件不是 STM family，后续只能作为异构 related work / 方法近邻使用。
- 若 repair 依赖 oracle、专家、人机选择或私有数据，实验对比时必须降级为条件 baseline 或 related work。
