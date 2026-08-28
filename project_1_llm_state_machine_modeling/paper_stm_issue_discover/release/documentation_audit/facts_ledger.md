# 文档事实账本

本账本列出本轮说明文字的受保护事实及其主证据。数字、版本、commit、run ID、hash、路径、命令、枚举、主体和因果关系在 shuorenhua 改写中均不得改变。

| 事实组 | 固定事实 | 主证据 |
| --- | --- | --- |
| 当前结果宇宙 | 54 pair、3 round、145 expected、435 round-level expected；L2 为 39 expected、117 rows | [recomputed summary](../../final_results/v60_current_vs_x1v2_baseline/derived/recomputed_summary.json) |
| v60/current | method 66b5d71aecd73f6eeddac082037f7c34e04da057；run 915d56e45a634c27aa03866f03818c6d；Judge 05cf0da6f7d9fcf1de26c349b586fc71c268f1c5；profile gpt-5.6-luna | [recomputed summary](../../final_results/v60_current_vs_x1v2_baseline/derived/recomputed_summary.json) |
| 冻结 hashes | registry sha256:38fa2e8060ff822836a3e6437a271998690d36cf60822053316eb21cda2015ca；prompt/schema sha256:daddf099896d47092b83f08fba907fd1c3f84a3e699bccf890e120d2a286d861；input sha256:c89b1aca38bf6104c94de4735d0b682165c01d6092cf2a595fb826a36210fc10；run contract sha256:4375f6071b04d230c7998368c42a36f5d784ae8938085646f0a297239e50cd3d；Judge protocol SHA d774d9bd3e4c4fe04735ed1d4ec064be197cfadcd52e21c8226e37175b29b210 | [v60 method manifest](../../final_results/v60_current_vs_x1v2_baseline/raw/v60_current/method/run_manifest.json)、[Judge snapshot](../../judge/src/paper_stm_judge/resources/semantic_judge_issue_195.snapshot.md) |
| 主指标 | current overall FULL 306/435 = 70.34%，L2 104/117 = 88.89%，hit@3 118/145 = 81.38%，hit@all 84/145 = 57.93%，precision 1165/1271 = 91.66%；baseline 相应为 211/435 = 48.51%、46/117 = 39.32%、104/145 = 71.72%、37/145 = 25.52%、410/512 = 80.08% | [正式报告](../../final_results/v60_current_vs_x1v2_baseline/report/v60_current_vs_x1v2_baseline_cn.md) |
| W | current FULL-hit max-W2/W1/W0=211/95/0，分母 306；baseline=0/211/0，分母 211。baseline finding-level W0/W1/W2=1/511/0，分母 512；W 与谓词体系不绑定 | [expected witness audit](../../final_results/v60_current_vs_x1v2_baseline/raw/v60_current/judge/composite/evaluator/expected_issue_witness_audit.json)、[X1v2 W audit](../../final_results/v60_current_vs_x1v2_baseline/derived/x1v2_witness_level_audit.json) |
| Judge / evaluation 语义 | FULL/PARTIAL/NONE 是 expected relation；VALID_KNOWN/VALID_NOVEL/INVALID 是 report validity；仅 INVALID 进入 semantic FP。D 是方法内裁定，L 仅属 ledger | [issue #195 snapshot](../../judge/src/paper_stm_judge/resources/semantic_judge_issue_195.snapshot.md)、[正式报告](../../final_results/v60_current_vs_x1v2_baseline/report/v60_current_vs_x1v2_baseline_cn.md) |
| 谓词与 W2 | current 有四族 19 谓词；full-scale-15 的计划分母为 15、真实 terminal receipt 覆盖 12。谓词不是问题发现准入门；W2 需要精确制品、typed input、backend terminal true/false 与完整 receipt | [registry](../../method/src/paper_stm_method/resources/predicate_registry.json)、[正式报告](../../final_results/v60_current_vs_x1v2_baseline/report/v60_current_vs_x1v2_baseline_cn.md)、[runner](../../method/src/paper_stm_method/orchestration/runner.py) |
| 输入与边界 | author PlantUML 与 canonical source IR 用于作者源定位；FCSTM 用于闭合模型执行；inspection/native facts 是确定性库存与验证事实；working contract 与 source trace 分别提供映射资格和归因。结果不外推到时钟、不变式、正交 region/并发、hybrid、无界时序、其他模型或其他 ledger | [runner](../../method/src/paper_stm_method/orchestration/runner.py)、[正式报告](../../final_results/v60_current_vs_x1v2_baseline/report/v60_current_vs_x1v2_baseline_cn.md) |
| 历史数字 | legacy X1v2 59.8%/70.3%/47.9% 属旧 Judge、两生成模型臂和不同网格，不能进入 current 结果表 | [legacy X1v2 result](../../discover_matrix/ledger_v2/X1V2_RESULTS.md)、[experiment history](../../archive/experiment_history/README.md) |

本账本不是第二份实验结果来源。写作或复算时应回到表中主证据。
