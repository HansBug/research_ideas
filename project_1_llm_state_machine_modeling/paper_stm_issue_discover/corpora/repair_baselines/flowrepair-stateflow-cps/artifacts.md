# FlowRepair — artifacts / resource 盘点

## 1. 一手资源入口

| 资源对象 | 当前判断 |
|---|---|
| 论文本体 | [DOI](https://doi.org/10.1016/j.infsof.2025.108010)；[arXiv](https://arxiv.org/abs/2404.04688)；[arXiv PDF](https://arxiv.org/pdf/2404.04688) |
| 作者代码 / 工具 | 论文给出 GitHub live repository：[StateflowRepairTool](https://github.com/aitorarrietamarcos/StateflowRepairTool) |
| replication package | 论文给出 Zenodo replication package：[zenodo.org/records/10936238](https://zenodo.org/records/10936238) |
| NL / 输入数据 | 无 NL 作为 repair 输入；论文说明 fridge / automated door 等 case study 的 requirements 细节在 replication package 中，需要后续下载核验 |
| STM / 初始模型 | Simulink/Stateflow faulty models；论文称 dataset 包含 3 个 case study / 9 个 faulty Stateflow models，具体模型文件应在 Zenodo/GitHub 中核验 |
| repaired 输出 | plausible patches / partial patches / valid patch 判断；是否提供完整 patch archive 需后续检查 Zenodo 文件结构 |
| 原生 repair case | 有望从 Zenodo/GitHub 对齐 `buggy Stateflow model + tests/oracle + patch`，但需冻结 artifact 版本后才能进入实验复现 |
| 许可 | 待核；需要检查 GitHub 和 Zenodo 的 license 字段 |
| 版本 / commit / hash | 论文写明 evaluation specific version 在 Zenodo；后续若实验使用，必须冻结 Zenodo record、GitHub commit、MATLAB/Simulink/Stateflow 版本 |

## 2. 本地证据容器

本目录中的 `paper.pdf`、`paper_content.txt` 与 `bibtex.bib` 只作为本仓库审计材料，不等同于论文一手公开资源。资源可获取性判断必须以上表的一手入口为准。

## 3. 可复现阻塞

- 需下载并检查 Zenodo replication package，确认是否包含 faulty Stateflow models、passing/failing tests、oracles、patch archives 与 evaluation scripts。
- 需确认 GitHub 仓库当前是否可访问、license 是否允许研究复现、是否能对应论文使用的 Zenodo specific version。
- 复现依赖 MATLAB 2022b、Simulink、Stateflow、Windows 10 等商业 / 平台环境；这会影响本文后续是否能把它作为实验 baseline。
- FlowRepair 不接收 NL，也不输出通用文本 STM；若用于本文，只能经转换层作为 repair-engine / mechanism 近邻，而不能直接与 pyfcstm textual repair loop 比公平结果。
