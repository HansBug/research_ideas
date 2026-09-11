# 大纲来源与复算入口

大纲只引用外部文献；内部证据通过本页与 [主张映射](./claim_evidence_map.md) 回查。机器文件固定标签及计数，正式报告解释干预与限制，talk 保存观点来源。写作不改变三者的历史身份。

| 来源键 | 对应内容 | 权威入口与机器字段 |
| --- | --- | --- |
| S0 | 输入、范围、145 条参考问题、规模 | [台账](../discover_matrix/ledger_v2/README.md)、[l_tier.json](../discover_matrix/ledger_v2/l_tier.json)、[结构统计](../discover_matrix/ledger_v2/provenance/corpus_structure.json)、[输入选择](../selected_seed_examples/README.md)；排除 00x8 六制品后为 54 对 |
| S1 | RQ1/RQ2/RQ6、表 6–7、表 12、图 5–6；[plot_bars.py](./figures/plot_bars.py) 断言图中数字与冻结锚点一致；严格覆盖与 D2-only 覆盖由各模型 `cells.json` 与 raw 逐报告重算（分母 435 与 294）；表 12 的回执与 W2 计数取自 `cells.json` 的 predicate_receipts / candidate_evidence，gpt-5.6-luna 用 evaluate_rq3 输出，旧 ID 按 G4→G3、R4→R3、V4→V1 映射 | [E2 正式报告](../reports/2026-09-08-e2-three-backbone-results.md)、[E2 归档](../final_results/e2_20260907/README.md)；各模型 `statistics.json:/metrics/{baseline,ours}`，gpt-5.6-luna 用 `luna_history.json:/statistics/metrics`；层级为 `tiers/L0,L1,L2/hit1`，区间为 `cluster_bootstrap_95pct` |
| S2 | RQ3、表 8、图 7（论文按普通消融表述） | [A1 正式报告](../reports/2026-09-06-19-49-18-a1-no-inspect-v61-results-cn.md)、[results.json](../final_results/a1_no_inspect_vs_v61_20260906/results.json)：`a1/metrics`、`v61/metrics`、`change_localization`；正文夹紧案例为 `0001` 三轮，源状态为 ClampingState / ClampingLoseState |
| S3 | RQ4、表 9–10、图 8；表 10 的阶段产出计数取自 E2 raw 逐格 `stage_outputs.execute_batch` 计数器与 v61 raw method 输出 | [A3 正式报告](../reports/2026-09-10-20-39-37-a3-four-model-results.md)、[四模型汇总](../final_results/a3_open_judge_20260910/four_model_summary.json)：`models/{model}/{a3,full}/metrics`、`comparison`、`human_confirmations` |
| S4 | RQ5、表 11、图 9；核算路径（指定 I / 复用 / 新判）与敏感性分析只留内部记录，论文不写 | [A4 正式报告](../reports/2026-09-10-17-01-11-a4-frozen-full-tail-results.md)、[紧凑核算](../reports/a4_20260910/)；`{model}-accounting.json:/metrics/{a4,full}`、`routes`、`rounds`、`publications`、`source_hashes`；干预由[事前协议](../discover_matrix/docs/generations/a4_20260910/preregistered.md)定义 |
| S5 | 历史 gpt-5.6-luna、W2 与内部表示错误 | [v61 归档](../final_results/v61_source_divergence_vs_x1v2_baseline/README.md)、[结果分析](../discover_matrix/docs/generations/v61/analysis_and_options.md)；W2 根命中 127、含子主张 137、报告 267，三者不可互换 |
| S6 | 方法、谓词范围与来源责任；表 3 的 12 条谓词名称、族、语义、参数取自注册表 `four-family-12-core.v1`，领域来源取自谓词出处库的一手引文定位；S5 为 AST 同一性（`backends/source_static.py`，不用 SMT）；表 2 阶段表与图 2 生命周期（[guidance_lifecycle.mmd](./figures/guidance_lifecycle.mmd)）取自 method 文档 | [method](../method/README.md)、[谓词定义与来源](../related_work/provenance/predicate_provenance.md)、[历史注册表](../related_work/provenance/archive/pre_p1_20260905/README.md)、[模型范围](./model_scope.md)；图 1 与图 2 是明确标注的构造示例，无实验身份 |
| S7 | 文献定位与理论依据；表 1 相关工作比较取自 closest-work 矩阵；第五轮清理后参考文献 60 条，[^iso9646] 替换讲义副本，[^qwen38]/[^muse] 为 Hugging Face 模型卡（2026-09-11 核验可访问） | [closest-work 矩阵](../related_work/closest_work_matrix.md)、[谓词出处库](../related_work/provenance/README.md)、[工具角色](../related_work/neighborhood/tool_roles.md)、[确定性基线调查](https://github.com/HansBug/research_ideas/issues/201) |
| S8 | 导师和用户决策 | [9 月 4 日导师讨论](../../talks/2026-09-04-导师-paper1大纲收口与消融基线口径.md)、[9 月 5 日导师逐字讨论](../../talks/2026-09-05-导师-paper1多模型对照与谓词降幻觉.md)、[9 月 10 日导师聊天：三项技术贡献定稿](../../talks/2026-09-10-导师-paper1三项技术贡献定稿与A4精确率口径.md)、[写作决策与飞书反馈](./outline_feedback.md)、[第五轮 AI 审稿批注决定](./outline_feedback.md#2026-09-11-第五轮-ai-审稿批注形成的写作决定)；9 月 4 日为周五，9 月 5 日为周六；转述、原话和用户后续裁定分别保留；聊天中的 4.2/4.0/2.7/0.9 是口头数字，正文用冻结核算 |

通用指标字段为 `reports`、`K`、`N`、`I`、`hit1/hit3/hitall`、`precision`、`strict/precision`；比例对象包含 numerator、denominator、rate。表 4 的 V 从 K+N 计算，百分点用未舍入比例相减后保留两位。

## 无需模型调用的复验

以下命令在仓库根运行。它们核验冻结归档的计数、来源和对应关系，不新增实验，也不完成独立语义裁定。使用已有 Python 环境；缺依赖时按各归档 README 安装，不读取模型凭据。

```bash
python project_1_llm_state_machine_modeling/paper_stm_issue_discover/discover_matrix/docs/generations/a1_no_inspect_20260906/analyze_a1.py
python project_1_llm_state_machine_modeling/paper_stm_issue_discover/discover_matrix/docs/generations/e2_20260907/analyze_e2.py --check-counterexamples
python project_1_llm_state_machine_modeling/paper_stm_issue_discover/discover_matrix/docs/generations/a3_20260910/verify_archive.py --archive project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/a3_open_judge_20260910 --model qwen --model muse
for model in sonnet luna qwen muse; do
  python "project_1_llm_state_machine_modeling/paper_stm_issue_discover/discover_matrix/docs/generations/a4_20260910/compact_a4.py" "project_1_llm_state_machine_modeling/paper_stm_issue_discover/reports/a4_20260910/$model-accounting.json"
done
```

A3 命令核验 qwen3.8-27b/muse-glimmer-30b 新归档并重新生成四模型汇总，与 claude-sonnet-5/gpt-5.6-luna 冻结结果对照。A4 紧凑核算可复核计数及候选流向；从原始调用重建还需要受限原件，不能把紧凑核算写成原始语义重判。gpt-5.6-luna W2 的逐项复算沿用 [evaluate_rq3.py](../discover_matrix/docs/generations/v61/evaluate_rq3.py)，历史 D0、内部归因错误与人工确认范围见 S5/S8。

## 外部引用如何使用

正文 60 条参考文献沿用已核验文献和官方工具来源，条目只保留正式元数据，不夹工作笔记。任务与邻近工作引用 Wang、Li/Zheng、MCeT、LiSSA、Given–When–Then，具体范围回查 S7 的 closest-work 矩阵；UML 语义、性质模式、FRET、性质生成及经典验证依据回查 S6/S7 的谓词出处库。Stateflow、Sismic、SCXML 用于说明可用执行工具及工程选择，不写成运行过的效果基线。Barr 与 SATE 支持评价构念讨论，不用于声称本项目已完成人工研究；CEGAR 支持抽象风险，不替本实现提供正确性证明。

引用变更时需同时检查题名、作者、年份、DOI/官方链接及正文主张。已有文献题名和来源中的正式拼写不随语言润色改动。新增数字先改权威实验结果及其审计，再同步展示；不能仅手工改论文表格。

## L/W/KNI 分类的文献映射

[issue #189](https://github.com/HansBug/research_ideas/issues/189) §1.3 调研提供 L 与 W 的概念锚点。L0/L1/L2 是本文操作化分类：Torre 等 EASE 2014 的一致性研究及 Knapp/Mossakowski 的多视图一致性支持静态/动态边界；Baier/Katoen 的状态与路径性质支持信息范围区分。Torre 的句法良构性不等同于本文的描述—元素表面对齐，正文未把 L0 当作该文直接定义。

W0/W1/W2 同样是本文分档。Femmer 等 JSS 2017 的 Requirements Smells 支持具体定位和检测机制，模型检查教材支持反例的执行证据角色，CEGAR 支持抽象反例的解释上界。2026-09-11 通过 Crossref 复核新增 Torre/Femmer 的 DOI、刊会、年份与页码；Knapp 的出版社 DOI 与作者稿入口来自 #189 的全文调研。

[issue #195](https://github.com/HansBug/research_ideas/issues/195) 的文献调查以 MCeT §4.2 同根因/新真实问题、SATE IV §2.4/2.7/2.9 相关发现及不完备真值为 K/N/I 依据；三标签是本研究的综合操作化。图 4 跟随产生结果的 `relation_first` 冻结规则（允许有关联的 D0 进入 K），不以当前 validity-first 协议替换历史口径；严格精确率另计 K/N 与 D1/D2 的交集。A4 的核算路径来自 S4，论文不写。

报告五元组 $r=(\varphi,\sigma,\Lambda,\beta,\omega)$、义务映射 $\mathcal{O}$、带来源事实映射 $\mathcal{F}$ 与来源映射 $\pi$ 见正文 §3.1、§3.3，是对方法既有报告字段（claim、citation、source refs、basis、receipt）与来源追踪的抽象记法，不新增实现。FCSTM 正式记法见正文 §3.2；展开既有 S/E/V/Tr/A 简记以表达层次、入口、终止与初始赋值。宏步及状态/变量分离对应 [pyfcstm BMC 语义说明](../../../pyfcstm/docs/source/explanations/bmc_semantics/index.rst)，不改变运行时语义或冻结结果。
