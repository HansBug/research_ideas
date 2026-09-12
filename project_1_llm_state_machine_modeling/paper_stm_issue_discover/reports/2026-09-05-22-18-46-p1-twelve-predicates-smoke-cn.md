# P1 十二谓词：本地十格 smoke 结果、风险与后续建议

日期：2026-09-05。本文记录已完成运行的事实与解释，不是主实验、消融结果或新的 hit/precision 评测。十格指原有两格加追加八格。本次中文整理不启动运行、不修改 method，不改变冻结的 v61 结果及运行身份。

正文的 `[src-*]`、`[clm-*]`、`[cmd-*]` 对应文末证据索引。详细审计仅保存在本地 gitignored `runs/`；新 checkout 不包含这些文件。本文是人类可读分析，不替代机器记录。

## 1. 结论与是否重跑

**当前建议：不重跑 v61，不追加泛化 smoke，也不把这三个已知问题作为继续推进 P1 的阻塞项。** 现有证据支持十二谓词版本可以运行，尚未发现编号、分派或同输入后端判定回归；但不能据此声称端到端质量完全不变。[clm-migration][clm-next]

这个建议不是将异常判为无害：0009 的 W2 降级、0034 的数量约束漏报各出现两次；0024 还出现了一次 D 误读正确回执后的漏报。它们有影响后续输出的机制，但当前没有证据表明损失已达到需要重启主实验的规模，也没有隔离 P1 prompt、随机生成和 provider 变化各自的贡献。[clm-losses]

| 后续动作 | 当前建议 | 重新考虑的条件 |
| --- | --- | --- |
| 重跑冻结的 v61 ours full | 不重跑，保持既定冻结边界 | 本次诊断未发现需要改动冻结结果的依据 |
| 再加一批随机 smoke | 暂不增加 | 现有十格已定位具体链路；更多无对照样本仍难回答因果归属 |
| 立即修改三条异常链路 | 可以暂放，保留原始证据 | 某问题持续影响下一项正式实验的核心指标或比较解释时，单独定点处理 |
| 继续论文整理及已约定的后续工作 | 可以继续 | 不把本次 smoke 写成质量等价证明；下一项实验若依赖不同版本的直接性能比较，再在其协议内处理可比性 |

以上是研究推进建议，不是新的实验授权。后续若需要处理，优先使用已保存的三个病例检查具体机制；无需先扩成全量重跑，也不需要为了“再确认一下”反复冷启动。[clm-next]

## 2. 运行身份与范围

三次运行均使用 `gpt-5.6-luna`，配置 adapter 为 `openai-responses`，观测模型标签一致；每批一轮、两个 workers。输入来自论文工作区的 `pipeline/representation/reports/llms_emp_r45_java_60`。运行没有读取 v61 报告作为方法输入，没有调用评测 Judge；方法内的 D 裁决仍是正常流水线的一部分。[src-runs]

| 批次 | Run ID | 时间（2026-09-05 UTC） | 样本与格数 |
| --- | --- | --- | --- |
| 初次 | `30322c29f93a4e0588d2db27c9ec7d8d` | 04:32:14-04:40:54 | 0002、0024，共 2 格 |
| 追加批次 1 | `8f264ec47610400abb965071d08ff84d` | 13:25:38-13:47:27 | 0002、0024、0009、0034，共 4 格 |
| 追加批次 2 | `b732e204f8bf4ff4a3869220789fe4ad` | 13:48:10-14:07:39 | 同上，共 4 格 |

- 初次 source：`71774498d65f3e3a7df5a30fbd7128236756fc1f`；追加 source：`835e299a8927964816cd958a4da6f6c794ee53c1`，均为启动时的干净版本。两者的 method 源码、`utils/`、pyfcstm 无差异。
- pyfcstm：`901f30e981c29eb8e304b33d61985652d2e85b2e`。
- Registry：`four-family-12-core.v1`；hash：`sha256:27e6bee263a37079cb86aa5dfdc904e3ba9711533b6cb1c91e9d911912d7d42d`。
- 运行边界来源：[初次登记](https://github.com/HansBug/research_ideas/pull/203#issuecomment-5549193195)、[追加登记](https://github.com/HansBug/research_ideas/pull/203#issuecomment-5552116591)。

这些身份信息用于解释既有记录，不定义新的运行配置。[src-runs]

## 3. 完成情况与 v61 对照

### 3.1 运行完成不等于每条义务都正确处理

十格全部 completed/eligible，零 cell error、零 audit error、零整格重跑。52 个记录中的阶段调用全部成功；13 次 schema 校验失败在原阶段纠正。追加批次 2 的 0024 grounding 有一次 300 秒 provider timeout，经既有 transport retry 恢复；日志中的 scheduled/recovered 是一次失败及其恢复，不是两次失败。[clm-completion]

| 批次 | 完成格数 | 最终报告 | 保存回执 | 终止 Boolean | Unsupported |
| --- | --- | --- | --- | --- | --- |
| 初次 | 2 | 25 | 54 | 26 | 28 |
| 追加批次 1 | 4 | 36 | 106 | 45 | 61 |
| 追加批次 2 | 4 | 33 | 96 | 44 | 52 |
| 合计 | 10 | 94 | 256 | 115 | 141 |

94 条最终报告包含 29 W2、65 W1；115 条终止回执包含 61 false、54 true。报告数读取 `report_issue_clusters` 和 `stage_outputs.publish.report_issue_count`，不能用中间 `model_output.issues` 或全部 evidence records 的 W2 数代替。[clm-completion]

实际终止执行覆盖 S1-S5、G1/G3、R1-R3、V1，共 11/12；未覆盖 G2。新 G3 在 0009 两次追加运行均返回 true；0034 的三条 R2 检查两次均为 false/true/true，与 v61 对应三轮一致。Unsupported 和 local-progress 诊断仍保留：例如初次 0024 的两条局部进展主张因状态有出边而被拒绝。这不等于整格失败，也不能证明所有义务已处理正确。[clm-migration]

配置口径成本估计：初次 $0.119003，批次 1 $0.294683，批次 2 $0.203394；追加八格合计 $0.498077，不是中转服务实际账单。[src-runs]

### 3.2 同样本的逐格结果

对照 v61 每个样本三轮，八项输入内容 hash 全部相同。Context manifest 仅在 checkout 根路径归一化、移除其派生 hash 后相同；配置的 context/output 上限相同。历史 source 为 `ea6141607037d6daabe7df6826fc7c90dab7a12b`，method 源码与 pre-P1 base `4f74a2b60b3ecfde1ce0a83f466f8ff64f78433c` 一致。[clm-migration]

| 样本 | v61 三轮报告数 | 当前：初次 / 批次 1 / 批次 2 | v61 三轮最终 W2 | 当前最终 W2 |
| --- | --- | --- | --- | --- |
| 0002 | 12 / 10 / 7 | 15 / 8 / 10 | 6 / 6 / 6 | 7 / 6 / 6 |
| 0024 | 8 / 6 / 8 | 10 / 12 / 7 | 2 / 2 / 1 | 2 / 2 / 1 |
| 0009 | 9 / 10 / 11 | 未运行 / 9 / 9 | 2 / 2 / 2 | 未运行 / 1 / 2 |
| 0034 | 10 / 10 / 11 | 未运行 / 7 / 7 | 1 / 1 / 2 | 未运行 / 1 / 1 |

115 条终止回执中，93 条能按样本、版本映射后的谓词、完整 typed inputs 与历史终止回执匹配，93 条全部同判；其余 22 条没有同输入历史记录，不计一致或反转。只归一化 `element_refs` 顺序，未丢弃其他输入字段。这些回执包含重复输入，不是 93 次独立质量试验。[clm-migration]

历史映射先排除退出项，再将旧 G4/R4/V4 映射为新 G3/R3/V1，避免旧同名 G3/R3/V1 混入。另有全量 v61 标签视图：2,436 条回执中 1,114 条终止回执均来自保留项；退出项旧 S6 有七条非终止回执、零终止回执。它只支持“未删除既有终止 witness”，不证明未来生成分布不变。[src-labels][clm-migration]

## 4. 预期波动与实际异常

| 现象 | 证据与机制 | 影响判断 |
| --- | --- | --- |
| 初次报告膨胀未持续 | 0002 从 15 回到 8/10，两条额外 effect 主张消失，六类稳定 W2 问题保留；0024 为 10/12/7，信号被拆成变量变化、独立 guard 与聚合报告重叠的现象并不持续 | 与义务拆分和 grounding 波动相符，未显示统一膨胀；报告数本身不能说明 precision |
| 0009 同一 collision guard 连续 W2 降到 W1 | v61 三轮用可解析的 `dist_to_rear<5 and vel>30`；追加两次分别生成 `dist_to_rear<5 and vel>30 km/h`、`dist_to_rear<5 & vel>30`，均不符合 FCSTM logical-expression grammar | 问题仍发布，但可执行证据丢失。批次 2 的另一个 guard 产生 W2，掩盖了总 W2 数中的损失；不是退出谓词导致的必然降级 |
| 0034 数量约束连续漏报 | v61 三轮均有 InMotion 实际 0、要求 3 个子状态的报告；追加两次契约选 `explicit_named_members`，exact binding 却为 `direct_child_states`，frontier 记录 `owner_candidate_count=0`、unresolved | 前后绑定域不一致导致一条报告缺失；三个单独 containment 报告仍在，不等于一定少一个 ledger hit |
| 0024 批次 2 入口动作漏报 | S4 对 Accelerating/entry/Accelerate 正确返回 false；D 实际收到的 prompt 包含 false、反例和动作不存在的说明，却声称动作存在并作出 not-established/rebutting-survives 裁决 | 正确检测后被语义裁决压掉。缺 source attribution 同时降低 W，但解释不了 D 对事实的反读；v61 三轮均发布此问题，包括一次 W1 |

这四类判断分别由逐项报告清单和原始回执支持；不能将后三项概括为“都是无害偶然性”。[clm-losses]

0024 的精确定位是批次 2、义务 `0024:r1:i12`、契约 `NL-CONTRACT-NL8-ACTION-1`。其 D 输入中的 receipt reason 为 `The exact action is not attached to the native FCSTM entry lifecycle slot.`，且 `verdict=false`。原始 `audit.jsonl` 证明投影没有漏传或反转该事实，错误发生在 D 的解释与裁决。[src-dossier]

源码对比表明：`backends/source_static.py` 的 S4/S5 和 guard parser 未变，`semantics/frontier.py` 的 cardinality-domain 匹配与 fallback 未变，`semantics/workflow.py` 的 D dossier projection 未变；P1 改动了共享 prompt 和 routing。因此可以定位被触发的失败机制，但不能断言这些异常由 P1 新增，也不能因下游代码没变就断言端到端分布没变。[src-code][clm-losses]

另有两项次要现象：批次 1 / 0024 的 W2 报告仍带“Grounding remains unresolved”旧标题；批次 2 / 0002 出现可疑的 owner/self 默认入口 W1 主张。v61 也有相似标题或 scope 模式。其他 action/effect 主张也会出现或消失；这些不是本轮 Judge 裁定的 INVALID，报告数相近不能代替问题集合对照。[src-comparison]

## 5. 对实验解释的边界

当前有依据区分三层结论：[clm-limits]

1. **功能迁移**：没有观察到 ID、分派或匹配 Boolean 判定回归，可以继续使用十二谓词版本；不覆盖全部输入或 G2。
2. **端到端发现质量**：存在影响 W2 和最终报告的具体机制，但十个选定格子无法估计其总体发生率，不能据此证明全局退化或质量等价。
3. **冻结结果**：v61 raw/derived、manifest、metrics 和运行身份不变。本次观察没有改写既有指标，也不是将当前版本冒充为生成 v61 的版本。

本轮未运行评测 Judge 或 ledger mapping。按现有口径，precision 为 `(VALID_KNOWN + VALID_NOVEL) / all reports`；W1、重复和重叠报告不是自动 FP，少一条报告也不自动等于少一个 hit。[src-metrics]

样本有意选取，并非随机抽样；0024/0034 共享列车系统 NL，只是模型表示不同。v61 调用发生于 9 月 3 日 UTC，本次为 9 月 5 日；相同模型标签不保证 provider 快照相同。这不是同期随机化的新旧 A/B 对照。[src-runs][src-comparison]

统计解释检查覆盖 11/11 类常见误推：分别检查分组/聚合、个体外推、选择偏差、控制变量、基率、均值回归、完成者筛选、多重探查、分析路径选择、因果与反向因果。本报告不做显著性检验或因果估计；保留全部十格，按样本展示，未把初次高报告数回落当成改进证明，也未把同判回执当成质量等价证明。分析状态为 `ANALYZED`，不是整体可复现性认证。[clm-limits]

## 6. 其他本地验证记录

移出版本控制的测试与标签产物仍保存在 `runs/20260905_p1_twelve_predicates_checks/`，不因取消跟踪而作废或消失：[src-checks]

- 专项测试 110 passed；全套 417 passed / 14 failed，14 个失败名均在 pre-P1 对照源码复现，不将失败记作通过。其中两项涉及未展开的历史 LFS 制品。
- 独立发布包 74 个文件、1,668,563 bytes；源码 fixture 13 passed，仓库外 release 13 passed / 19 skipped。修正前的 12 passed / 1 failed / 19 skipped 记录也保留；跳过项是既有冻结制品依赖。
- 发布 source `5fc274b8c7a0beb3a379e0515f73562791bb012a` 与 smoke source 的所有发布 `src/` hash 一致；修正的是 fixture 的源码/发布环境边界，不是 runtime。

本次仅迁移、中文整理和取消运行产物跟踪；没有新增测试执行、provider 调用或 method 修改。12 份 checks 文件取消跟踪前后逐份 SHA-256 一致。

## 审计附录：证据链与事实源

### A.1 来源考据表

| source path | source creation commit | prefix commit | substantive fact commit 判定理由 | non-prefix revision/migration commit | canonical machine source |
| --- | --- | --- | --- | --- | --- |
| 原 `runs/20260905_p1_twelve_predicates_smoke/README.md` | `caf5ab825f411884c786ff47c3d92745ce41913d` | `1f852a8b394df697205de3dbeb761383919fe935` | `1f852a8b3` 首次固定完整十格表和三个异常；文件前缀取该提交的北京时间 22:18:46 | 本文件的迁移提交，见 `git log --follow`；中文整理新增第 1 节推进建议，不改运行统计 | 下表三组本地 run 与冻结 v61；原文件历经 `835e299a8` 的两格比较后扩为十格 |

### A.2 上游事实源清单

路径均相对于本文；本地未跟踪文件只在原工作区可读，不应把缺失原始数据的 checkout 当成已复核。

| 引用键 | source_id / 类型 | 事实源、用途与关键锚点 |
| --- | --- | --- |
| `[src-runs]` | `smoke_runs` / json、jsonl | [初次目录](../../../runs/20260905_p1_twelve_predicates_smoke/30322c29f93a4e0588d2db27c9ec7d8d/)、[批次 1](../../../runs/20260905_p1_twelve_predicates_smoke_followup/batch1/8f264ec47610400abb965071d08ff84d/)、[批次 2](../../../runs/20260905_p1_twelve_predicates_smoke_followup/batch2/b732e204f8bf4ff4a3869220789fe4ad/)；`summary.json`、`run_manifest.json`、`method/<pair>/round-1.json`、`llm/` 中的身份、完成、回执、prompt、raw output、usage、错误与重试 |
| `[src-comparison]` | `paired_comparison` / json、source-code | [comparison.json](../../../runs/20260905_p1_twelve_predicates_smoke_followup/comparison.json) 与 [compare.py](../../../runs/20260905_p1_twelve_predicates_smoke_followup/compare.py)；`historical/current/totals`、cell SHA-256、published 清单、matched/unmatched/disagreements；历史来源为 [v61 method](../final_results/v61_source_divergence_vs_x1v2_baseline/raw/v61_current/method/)，限定四个 pair 的三轮 |
| `[src-dossier]` | `s4_d_adjudication` / jsonl | [0024 D 审计](../../../runs/20260905_p1_twelve_predicates_smoke_followup/batch2/b732e204f8bf4ff4a3869220789fe4ad/llm/method/0024/round-1/d-adjudication/cell-attempt-1/audit.jsonl)；context 的 input_text 中义务 `0024:r1:i12`，对照 cell 的 `stage_outputs.d_adjudication.decisions` 和 `report_issue_clusters` |
| `[src-labels]` | `v61_label_views` / json | [主运行标签](../../../runs/20260905_p1_twelve_predicates_checks/v61_main_labels.json)、[0045 补跑标签](../../../runs/20260905_p1_twelve_predicates_checks/v61_fill0045_labels.json)；按原 registry 分辨旧 ID，保留原始回执与 hash，不改 W/D/判定 |
| `[src-code]` | `migration_code` / source-code、git-commit | [source_static.py](../method/src/paper_stm_method/backends/source_static.py)、[frontier.py](../method/src/paper_stm_method/semantics/frontier.py)、[workflow.py](../method/src/paper_stm_method/semantics/workflow.py)；对比 pre-P1 `4f74a2b60` 与运行 source `835e299a8` 的具体分支 |
| `[src-metrics]` | `precision_protocol` / md | [evaluation/README.md](../evaluation/README.md) 的 report-based precision 定义 |
| `[src-checks]` | `functional_checks` / xml、json、md | [本地检查说明](../../../runs/20260905_p1_twelve_predicates_checks/README.md) 及该目录的 pytest XML、发布 manifest；[取消跟踪前 hash](../../../runs/20260905_p1_twelve_predicates_smoke_followup/untracking-before.sha256) 保留逐文件校验依据 |

### A.3 Claim-evidence map

| 引用键 / claim_id | 结论与类型 | 上游事实源与锚点 | 复验命令 | 置信度与限制 |
| --- | --- | --- | --- | --- |
| `[clm-completion]` / `P1-SMOKE-C1` | 十格完成及计数；count | `[src-runs]` summary、cell 发布列表和 llm_calls | `[cmd-compare]`；原始错误人工检查 | high；完成不代表语义正确 |
| `[clm-migration]` / `P1-SMOKE-C2` | 93 条匹配回执同判、未见底层迁移回归；classification | `[src-comparison]` totals/current、`[src-labels]` 终止记录、`[src-code]` | `[cmd-compare]`、`[cmd-code]` | high，限已观察输入；不证明整体等价 |
| `[clm-losses]` / `P1-SMOKE-C3` | 三个具体降级/漏报机制；risk | `[src-comparison]` 中 0009/0034/0024 两批 cell，`[src-dossier]` 义务 i12、`[src-code]` 分支 | 人工复验 typed inputs、frontier checks、D 输入/输出；语义差异不能只用计数自动判定 | high，限病例事实；P1 因果贡献 unknown |
| `[clm-limits]` / `P1-SMOKE-C4` | 未建立质量等价或总体退化；prohibition | `[src-runs]` 选样/时间/未调用 Judge、`[src-metrics]`、C2/C3 | `[cmd-compare]` 并人工核对实验设计 | high，指证据边界，不指真实效应大小 |
| `[clm-next]` / `P1-SMOKE-C5` | 暂不重跑，继续推进，异常定点留存；decision 建议 | C1-C4、用户保持 v61 冻结与避免非必要重跑的边界 | 人工复验第 1 节触发条件；建议不等于运行命令 | medium；若具体异常影响后续关键比较，再单独处理 |

### A.4 复验命令

`[cmd-compare]`：在仓库根只读重算已保存结果，不调用 provider；本地原始数据缺失时不能执行。

```bash
/home/zhangshaoang/oo-projects/research_ideas/venv/bin/python runs/20260905_p1_twelve_predicates_smoke_followup/compare.py
```

`[cmd-code]`：对照实际运行版本，不使用未来 HEAD 冒充本次代码。

```bash
git diff 4f74a2b60b3ecfde1ce0a83f466f8ff64f78433c 835e299a8927964816cd958a4da6f6c794ee53c1 -- project_1_llm_state_machine_modeling/paper_stm_issue_discover/method/src/paper_stm_method/backends/source_static.py project_1_llm_state_machine_modeling/paper_stm_issue_discover/method/src/paper_stm_method/semantics/frontier.py project_1_llm_state_machine_modeling/paper_stm_issue_discover/method/src/paper_stm_method/semantics/workflow.py
```

历史调用记录：Python 解释器同上；`LLM_CONFIG_FILE` 指向 sibling checkout 的 profile 配置，`PYTHONPATH` 明确选择本 checkout 的 method/evaluation/judge/paper、pyfcstm 和仓库根。入口 `python -m paper_stm_method.cli`，公共参数为 `--report-root project_1_llm_state_machine_modeling/paper_stm_issue_discover/pipeline/representation/reports/llms_emp_r45_java_60 --profile gpt-5.6-luna --rounds 1 --workers 2 --allow-live`，各批 output-dir、pair IDs 见第 2 节和 manifest。追加两批还传入初次目录为 `--predecessor-snapshot`，各自使用本地 round 1。曾尝试的 `--rounds 2` 在参数校验阶段被拒，未调用 provider、未初始化输出；接受值为 1/3，随后使用两次独立一轮。此段只保存历史命令事实，不授权重跑。
