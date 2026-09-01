# Paper1 相关工作入口

本目录维护 Paper1 当前主张的外部文献边界。它不替代论文集，也不替代冻结结果。当前论文只以[closest-work 矩阵](./closest_work_matrix.md)和[谓词来源审计](./provenance/predicate_provenance.md)作为相关工作与来源的入口；两份文件均记录截至 2026-09-01 的检索范围、全文状态和未完成事项。

| 路径 | 当前用途 | 不能作为 |
| --- | --- | --- |
| [closest_work_matrix.md](./closest_work_matrix.md) | 对照需求-模型分析、LLM 建模、状态机补全、可执行证据、溯源与评测可靠性 | 现有工作的穷尽清单，或数值基线 |
| [provenance/predicate_provenance.md](./provenance/predicate_provenance.md) | 四族 19 个谓词的语义、来源职责、后端与边界审计 | 运行时谓词资格或缺陷覆盖 |
| [provenance/README.md](./provenance/README.md) | 19 谓词来源档案的状态和更新边界 | 完整书目已闭合的宣称 |
| [assertion_output_form_evidence.md](./assertion_output_form_evidence.md) | 历史检索材料，可为回执、判定器与输出形态提供候选文献 | 当前 C1/C2、新颖性或论文结论的事实源 |
| [landscape/story_suggestions.md](./landscape/story_suggestions.md) | 历史故事候选与检索线索 | 当前贡献、RQ 或结果结论 |
| [provenance/c3_differentiation.md](./provenance/c3_differentiation.md) 与 [c3_iii_supplement.md](./provenance/c3_iii_supplement.md) | 已弃用三贡献路线的检索留档 | 当前第三项贡献或活动论文定位 |
| [archive/legacy_20260821/](./archive/legacy_20260821/) | 历史 L1/L2 预案 | 当前来源政策或结论 |

R1 的当前故事只有 C1（确定性模型信息增强）和 C2（有来源映射的可执行证据升级）。方法可由具有作者源属追踪、规则相关能力约定、FCSTM 投影和失败关闭边界的适配器，在声明的源语言子集上实例化；PlantUML 是本论文的案例研究语言。覆盖率、精确率、W-on-hits、成本和失败形态属于评测与讨论，不是第三项技术贡献。现有工作可能与其中任一侧面重叠；写作时须以矩阵中的共同核心、具体差异、直接反证和最低防守措辞为准。

本目录不宣称检索已经穷尽。访问受限、缺少正式 BibTeX 或未核对全文原句的材料保留为 `TODO-CITATION`，不会被写成论文承重引文。历史材料中的旧 C-①/②/③、L1/L2/L4、早期 RQ 或数值只在其历史语境内成立。
