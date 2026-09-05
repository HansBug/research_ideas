# pre-P1 来源与编号记录

本目录保存 2026-09-05 谓词整理前的 `four-family-19-core.v1` 定义与来源审计。当前方法采用 `four-family-12-core.v1`，仅包含连续编号的 12 条；用途、来源与执行边界见[当前审计](../../predicate_provenance.md)。

## 编号映射

映射以原 registry 版本和原 ID 为键。原记录及编号保持原样，数据处理脚本另提供当前编号。

| 原版本中的 ID | 当前版本中的 ID |
| --- | --- |
| S1–S5、G1–G2、R1–R2 | 编号不变 |
| G4 | G3 |
| R4 | R3 |
| V4 | V1 |
| S6、G3、R3、V1、V2、V3、V5 | 已退出，无当前对应项 |

原 G3、R3、V1 与当前同名项的语义不同，不能仅按字符串合并。来源别名 G4-RP1/2 对应当前 G3-RP1/2；原 R4 的 TP1 和原 V4 的 TP4 已存在于来源审计，本轮同步补入当前资源。

映射实现位于 `evaluation/src/paper_stm_evaluation/predicate_id_mapping.py`，统计视图入口为 `scripts/evaluation/predicate_id_view.py`，均相对于论文工作区。视图保留源版本、原 ID 和当前 ID；退出项仍保留历史身份，不删除记录，也不重判 W、D、命中或有效性。

## 冻结结果

v61 ours full 使用原 19 项词表，运行 ID 为 `a7b47d84c3cb4377a8009e5018d5b745`，registry hash 为 `sha256:38fa2e8060ff822836a3e6437a271998690d36cf60822053316eb21cda2015ca`。原始和派生结果、manifest、回执和运行身份原样保留。当前编号只用于冻结归档之外的统计展示，不将 v61 标为当前 12 条运行。

论文的选样沿用归档原规则：`0045` 第 1 轮使用 `raw/v61_current_fill0045/` 中 run `0e450e5c6c9d4841820c7d1fd2a888ea` 的补跑格，原失败格仍保存且没有谓词回执。分别对主运行与补跑运行生成编号视图，保留两个 manifest 与逐格 hash；主运行有 1104 条终止回执，补跑增加 10 条 `pass`，合计仍为 1114 条（541 `violation`、573 `pass`）。这只是既有选样的标签统计，不是新的运行结果。

主运行中旧 S6 另有 6 条 `terminal_state=unsupported`、`predicate_verdict=null` 的非终止回执，`0045` 第 1 轮补跑格再有 1 条，按论文既有选样合计 7 条，终止回执为 0。统计视图保留这些记录；零终止回执不能写成“从未执行”或“没有任何回执”。

本目录原来源审计中的 125 条 source-authority 排除属于前代审计，不能应用为 v61 的新判定。旧 15-pair 和 planned execution 统计同样保留其历史分母。

`evaluation/applicability` 的新视图将旧路线选择表按版本映射到当前集合，并同时保留原路线；`stage_loss` 按 run manifest 的 registry 选择当前 12 条或原协议分母。前代 predicate-gold inventory 读取本目录的 19 条快照；旧 gold 执行请求在当前方法上显式拒绝，避免同名异义，复现须使用原 commit。原 release-refactor 的 hash/node 冻结校验仍保留，其目标是验证旧重构字节不变，不用它认证这次改变了谓词集合的版本。

## 文件与复现

`predicate_registry.json` 是原方法注册表，`method_source_catalog.json` 是原方法来源资源，`current_source_catalog.json` 是原论文侧审计目录。三份 Markdown 原文通过 `git mv` 保留：`predicate_provenance.md`、`CURRENT_SOURCE_AUDIT.md`、`coverage_audit.md`。另保存 `pipeline/evidence_discovery/METHOD_PRINCIPLES.md` 的完整原文，保留旧路由与运行计划。来源审计的相对路径按迁移前的 `related_work/provenance/` 位置解释，方法原则中的相对路径按原 `pipeline/evidence_discovery/` 位置解释；检索过程和旧执行语义均以历史版本为准。

复现原执行语义时，使用整理前 commit `77820dace894ba4a976bd5d5d671cf9354200330` 的独立 worktree，在其中按原 `method/README.md` 安装依赖和运行历史工具。可先执行：

```bash
git show 77820dace894ba4a976bd5d5d671cf9354200330:project_1_llm_state_machine_modeling/paper_stm_issue_discover/method/README.md
```

历史工具按该版本原入口运行，原资源与输入的 hash 用于确认版本；读取既有结果或生成编号视图无需重新执行 method，也无需调用模型。
