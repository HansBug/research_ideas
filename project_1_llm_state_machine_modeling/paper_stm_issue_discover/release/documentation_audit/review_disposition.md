# 独立审查处理记录

本记录只处理本次文档、导航、历史归档和离线校验问题。所有 reviewer 都只读原始代码、冻结制品与 Git history，未调用 provider。

| Review | Finding | 严重度 | Disposition | 处理依据 |
| --- | --- | --- | --- | --- |
| 01 numeric | root manifests 未覆盖改写后的 archive README | High | fixed; rereview passed | 仅以 `paper_stm_evaluation.final_results_archive finalize` 更新受控 manifest；当前 2907-file validator 与 raw/derived/reference 2655 项对拍均通过。 |
| 02 architecture | `pipeline/evidence_discovery` 被写为 current method | High | fixed; rereview passed | README 收缩为 compatibility 导航，默认链接 `method/`、`judge/`、`evaluation/` 与 final_results。 |
| 02 architecture | conversion/representation 指向旧 feedback loop | High | fixed; rereview passed | 两份 README 改为 input preparation/provenance 并指向 `archive/legacy/feedback_loop/`。 |
| 02 architecture | Judge validity 顺序不准确 | Medium | fixed; rereview passed | 改为 `FrozenValidityCertificate.core_truth`、relation、backend materialization 的真实顺序。 |
| 02 architecture | pipeline/evaluation 与 blueprint 指向旧 current paths | Medium | fixed; rereview passed | 前者降为 historical v0 schema，后者改指 `method/`、registry 和 frozen protocol。 |
| 02 architecture | compatibility README 仍展开 current method / evaluation 所有权 | Medium | fixed; rereview passed | `pipeline/evidence_discovery` 收缩；representation 明确为冻结输入/provenance，current evaluation 指向 `evaluation/` 与 final archive。 |
| 03 history | v46 source tree 与 retained subset 混淆 | Medium | fixed; rereview passed | inventory 分列 478-file source tree 和 157-file current subset，并给 commit restore 方法。 |
| 03 history | v60/X1v2 inventory anchor 早于 W audit | Medium | fixed; rereview passed | source commit 改为覆盖 2671-file archive 的 `d31a8d171...`。 |
| 04 documentation | reports GUIDE 无 historical scope | Medium | fixed; rereview passed | 开头限定历史 report，current facts 指向 final archive/evaluation。 |
| 04 documentation | inventory 未逐文件标注 | Medium | fixed; rereview passed | current files明细和最终 176-file legacy reference rows 已新增并与机械枚举闭合。 |

目标 rereview：01 在 finalize/validate 后核对 manifest；02 复核 package 与 pipeline 路径；03 复核 inventory 的 tree/commit 数；04 复核默认阅读路径、逐文件列表和文风。以上目标均已完成，当前 v4 发布面另经 current/fair-comparison validator 复核。
