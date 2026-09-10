# 大纲来源与复算入口

大纲只引用外部文献；内部证据通过本页与 [主张映射](./claim_evidence_map.md) 回查。机器文件固定标签及计数，正式报告解释干预与限制，talk 保存观点来源。写作不改变三者的历史身份。

| 来源键 | 对应内容 | 权威入口与机器字段 |
| --- | --- | --- |
| S0 | 输入、范围、145 条参考问题、规模 | [台账](../discover_matrix/ledger_v2/README.md)、[l_tier.json](../discover_matrix/ledger_v2/l_tier.json)、[结构统计](../discover_matrix/ledger_v2/provenance/corpus_structure.json)、[输入选择](../selected_seed_examples/README.md)；排除 00x8 六制品后为 54 对 |
| S1 | RQ1、表 2、图 2 | [E2 正式报告](../reports/2026-09-08-e2-three-backbone-results.md)、[E2 归档](../final_results/e2_20260907/README.md)；各模型 `statistics.json:/metrics/{baseline,ours}`，Luna 用 `luna_history.json:/statistics/metrics`；层级为 `tiers/L0,L1,L2/hit1`，区间为 `cluster_bootstrap_95pct` |
| S2 | RQ2、表 3 检查事实行 | [A1 正式报告](../reports/2026-09-06-19-49-18-a1-no-inspect-v61-results-cn.md)、[results.json](../final_results/a1_no_inspect_vs_v61_20260906/results.json)：`a1/metrics`、`v61/metrics`、`change_localization`；正文夹紧案例为 `0001` 三轮，源状态为 ClampingState / ClampingLoseState |
| S3 | RQ3、表 3 中间引导行 | [A3 正式报告](../reports/2026-09-10-20-39-37-a3-four-model-results.md)、[四模型汇总](../final_results/a3_open_judge_20260910/four_model_summary.json)：`models/{model}/{a3,full}/metrics`、`comparison`、`human_confirmations` |
| S4 | RQ4、表 3 执行反馈行、标签路径 | [A4 正式报告](../reports/2026-09-10-17-01-11-a4-frozen-full-tail-results.md)、[紧凑核算](../reports/a4_20260910/)；`{model}-accounting.json:/metrics/{a4,full}`、`routes`、`rounds`、`publications`、`source_hashes`；干预由[事前协议](../discover_matrix/docs/generations/a4_20260910/preregistered.md)定义 |
| S5 | 历史 Luna、W2 与内部表示错误 | [v61 归档](../final_results/v61_source_divergence_vs_x1v2_baseline/README.md)、[结果分析](../discover_matrix/docs/generations/v61/analysis_and_options.md)；W2 根命中 127、含子主张 137、报告 267，三者不可互换 |
| S6 | 方法、谓词范围与来源责任 | [method](../method/README.md)、[谓词定义与来源](../related_work/provenance/predicate_provenance.md)、[历史注册表](../related_work/provenance/archive/pre_p1_20260905/README.md)、[模型范围](./model_scope.md)；图 1 是明确标注的构造示例，无实验身份 |
| S7 | 文献定位与理论依据 | [closest-work 矩阵](../related_work/closest_work_matrix.md)、[谓词出处库](../related_work/provenance/README.md)、[工具角色](../related_work/neighborhood/tool_roles.md)、[确定性基线调查](https://github.com/HansBug/research_ideas/issues/201) |
| S8 | 导师和用户决策 | [9 月 4 日导师讨论](../../talks/2026-09-04-导师-paper1大纲收口与消融基线口径.md)、[9 月 5 日导师逐字讨论](../../talks/2026-09-05-导师-paper1多模型对照与谓词降幻觉.md)、[写作决策与飞书反馈](./outline_feedback.md)；9 月 4 日为周五，9 月 5 日为周六；转述、原话和用户后续裁定分别保留 |

通用指标字段为 `reports`、`K`、`N`、`I`、`hit1/hit3/hitall`、`precision`、`strict/precision`；比例对象包含 numerator、denominator、rate。表 3 的 V 从 K+N 计算，百分点用未舍入比例相减后保留两位。

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

A3 命令核验 Qwen/Muse 新归档并重新生成四模型汇总，与 Sonnet/Luna 冻结结果对照。A4 紧凑核算可复核计数及候选流向；从原始调用重建还需要受限原件，不能把紧凑核算写成原始语义重判。Luna W2 的逐项复算沿用 [evaluate_rq3.py](../discover_matrix/docs/generations/v61/evaluate_rq3.py)，历史 D0、内部归因错误与人工确认范围见 S5/S8。

## 外部引用如何使用

大纲的 21 个脚注沿用已核验文献和官方工具来源。任务与邻近工作引用 Wang、Li/Zheng、MCeT、LiSSA、Given–When–Then，具体范围回查 S7 的 closest-work 矩阵；UML 语义、性质模式、FRET、性质生成及经典验证依据回查 S6/S7 的谓词出处库。Stateflow、Sismic、SCXML 用于说明可用执行工具及工程选择，不写成运行过的效果基线。Barr 与 SATE 支持评价构念讨论，不用于声称本项目已完成人工研究；Troya 与 CEGAR 支持转换与抽象风险，不替本实现提供正确性证明。

引用变更时需同时检查题名、作者、年份、DOI/官方链接及正文主张。已有文献题名和来源中的正式拼写不随语言润色改动。新增数字先改权威实验结果及其审计，再同步展示；不能仅手工改论文表格。
