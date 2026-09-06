# A1 前置检查信息消融：事前登记

登记日期：2026-09-06，所有真实调用之前。依据：[A1/A2 消融公约](../../protocol/ablation_design_and_parallel_contract.md)、[A1 合同 #205](https://github.com/HansBug/research_ideas/pull/205)、[伞 PR #179](https://github.com/HansBug/research_ideas/pull/179)。用户授权实现、Luna 54×3、Luna judge、结果复算与审计；本登记不以预期方向作为运行或完成门槛。执行进度和 review 留在 PR，事后结果另存，不倒改本节假设。

## 1. 问题、条件与不变量

问题：保留 FCSTM、作者源追踪、普通语义发现和当前 12 条谓词时，前置确定性检查事实及其派生处理对发现覆盖、重复命中稳定性与报告有效率有什么净作用？这不是整个 C1 消融，也不是纯 LLM baseline。

| 条件 | 方法模式 | 正式规模 | 运行身份 |
| --- | --- | --- | --- |
| A1 | `no-inspect` | 54 pair × 3 round = 162 格 | `5ea4f355c03f48aea2cea1668b74057c` |
| 匹配 full | `none` | 同 54×3 | `2893db20b2d846018f189233703bf098` |

本次选择**独立匹配 full**，不等待 E2，也不事后挑选更有利的对照。它供 A1/A2 共用；A2 使用前仍须核对方法语义、输入、模型、配置和轮次。它不是重跑或替换 v61。v61 raw/derived、原 19 条运行身份和所有冻结数字保持不变，仅作历史系统对比；baseline 不修改、不重跑。

A1 关闭 reference inspection、inspection-equivalent、verify、SMT 前置上下文、working-contract 诊断、检查型候选/补充义务/预检/抑制和内部 D 的相关确定性校验。首轮、补全、纠错均使用受限视图；不得从 ModelIR 或另一文件重建同一前置检查。解析、引用和来源定位保留；候选专属的 12 条谓词后端仍可读取模型并产生真实回执。源码分歧、普通契约/语义定位、发布门、去重和独立评测保留。禁用记录为 `disabled_by_ablation`，不冒称 pass 或零诊断。

## 2. 固定输入与身份

工作区相对根：`project_1_llm_state_machine_modeling/paper_stm_issue_discover/`。输入为 `pipeline/representation/reports/llms_emp_r45_java_60`，台账为 `discover_matrix/ledger_v2/ledger.json`。54 pair 属于 9 个 NL 簇，每簇 6 个制品；145 条 expected issues，L0/L1/L2 为 71/35/39，三轮 expected-round 分母为 435。无台账条目的 pair 仍运行并进入报告精度统计。

```text
0000 0001 0002 0003 0004 0005 0006 0007 0009
0010 0011 0012 0013 0014 0015 0016 0017 0019
0020 0021 0022 0023 0024 0025 0026 0027 0029
0030 0031 0032 0033 0034 0035 0036 0037 0039
0040 0041 0042 0043 0044 0045 0046 0047 0049
0050 0051 0052 0053 0054 0055 0056 0057 0059
```

| 身份 | 固定值 |
| --- | --- |
| 输入集合 hash（runner 原算法，包含完整输入 manifest） | `sha256:0e34a96951d2a7ee3da77e572ca42963e1270a1acba9ed50a38e2f03e3599039` |
| ledger SHA-256 | `sha256:b5a38d3d24a51e980e5b9f5afc7c8c66aded59f3b51f16afe67e0deb592d0e36` |
| registry | `four-family-12-core.v1`；`S1-S5 / G1-G3 / R1-R3 / V1` |
| registry hash | `sha256:27e6bee263a37079cb86aa5dfdc904e3ba9711533b6cb1c91e9d911912d7d42d` |
| full prompt/schema hash | `sha256:744e7f489591904a08e9919ded9f99ec73c2d55d81225fbd8a9ec18dca8fefe2` |
| A1 prompt/schema hash | `sha256:3bfdc095985d8b8dcb8194084377239f02079a6dbcb80ef5965c97c88aea6157` |
| 模型配置 hash（不含密钥和价格，含完整 endpoint） | `sha256:a5bb978af02936e60784ad37bb85cb047c89f95eee971a9975c6f3ffc0b292c8` |
| full 行为对拍锚点 | `87e969b291156b98e2762967f0aa1439fbd4ddaa` |
| 公共接线基点 | `f2e415276` |

实际启动使用包含本登记与验收实现的干净、已推送提交，精确 source commit 写入每份 run manifest；两正式条件必须同一方法源码。实际 pair input hashes、依赖版本和 pyfcstm commit 随运行证据保存。方法不读取 ledger、历史报告、裁定或本登记的分析内容。

## 3. 模型、运行与 smoke

- Method 全部 LLM 节点与独立 judge 均使用 `gpt-5.6-luna`，不测试其他模型。当前 adapter 为 `openai-responses`，脱敏 endpoint 引用为 `https://sub2api-new-api.deepghs.org`，region/provider revision 未提供，不虚构固定服务快照；保存实际响应中的 model ID、时间、usage 与错误。
- 配置来自 `.llmconfig.yml`，context 上限 272000、profile output 上限 128000；结构化运行时另有输出预算约束，以实际请求为准。沿用当前有效推理/采样设置，不新增 temperature、seed 或 effort，不把未显式设置的 provider 默认值写成已知数值。两臂使用相同调用配置与现有阶段预算；移除检查信息导致的输入长度和实际调用量差异属于本消融，不另做 token 匹配。
- Streaming 开启；transport retries 8；首字节/read 边界 30 秒、单调用 deadline 300 秒；结构化原地反馈与重试沿用公共 runtime。未改整格失败语义，不用冷启动重采样掩盖 schema 问题。降级、未完成、错误与尝试均保留；失败记录不冒充正常零报告，不缩小计划分母。
- Smoke 固定 `0000/0004/0009/0024/0034`，每条件各 5×1，总计 10 格，不追加泛化 smoke。分别覆盖源码分歧与补全、候选专属 native 谓词、既有表达式绑定风险、D 误读风险、数量约束绑定风险。样本按工程机制选择，不估计总体质量。两臂各 workers=2。
- Smoke A1 ID：`d76b80985d824241a0e97d4da23936b0`；smoke full ID：`7cccfbb62ffb407eba50db5799128b27`。其产物与正式批次物理分离，不导入正式 run，不将 smoke 升格为正式重复。
- 正式 method 每条件 workers=8；两条件合计不超过 16。尽量同一时间窗口运行，保留调用日期和配置 hash；同 round 标签不意味着两臂共享随机数。Judge 分轮/条件组织，每次最多 14 pair workers，全部活跃 judge 合计不超过 14。
- 每 30-60 秒检查确切进程/工具句柄及输出增长。输出静默是检查信号，不据此判进程死亡或重启；沿用 runtime 的调用超时，不另以 30 分钟总墙钟上限终止完整研究批次。

从仓库根使用当前 checkout 的 method/evaluation/judge 与根 `utils` 的显式 PYTHONPATH，解释器为现有仓库 venv；不能加载 sibling 的已安装旧包。正式命令的公共部分如下，分别传入上表模式与 ID：

```bash
python -m paper_stm_method.cli \
  --report-root project_1_llm_state_machine_modeling/paper_stm_issue_discover/pipeline/representation/reports/llms_emp_r45_java_60 \
  --output-dir runs/paper1/a1_no_inspect_20260906/method \
  --profile gpt-5.6-luna --ablation no-inspect \
  --run-id 5ea4f355c03f48aea2cea1668b74057c \
  --rounds 3 --workers 8 --transport-retries 8 --allow-live --allow-full-live
```

Smoke 用独立 `runs/paper1/a1_no_inspect_20260906/smoke`，`--rounds 1 --workers 2`，逐个指定上述五个 `--pair-id`，不用 full-live。任何改变模型/方法/输入/评测口径的修正必须在新的正式调用前追加登记；已产生结果不覆盖。

## 4. 独立裁定与全部结果

Judge 固定 `semantic-judge.two-stage.v3.11`（当前第六轮），协议 hash `d774d9bd3e4c4fe04735ed1d4ec064be197cfadcd52e21c8226e37175b29b210`。使用两次 validity reading、`validity_aggregation=arbitration`、`validity_arbitration_trigger=any`、`k_closure=relation_first`、`closure_profile=full`；两臂相同，均重新裁定，绝不复制 v61 决定。Judge 的完整独立检查上下文不属于 A1 method 输入，不能向发现流程倒灌。

沿用 `paper_stm_judge.cli --source-format evidence_discovery_release`，逐个 source run、round 1/2/3 裁定，输出到独立 ignored `judge/`，不使用 report-filter 挑选有利报告。命令显式指定 Luna、14 workers、上述固定选项及 ledger。自动裁定、agent 审计、用户人工确认分开记录；本次登记时新报告人工确认数为 0，不声称多位人工已裁定新结果。

完整报告以下指标，定义不变：

1. FULL `hit@1`：expected-round 命中 /435；`hit@3`：至少一轮命中 /145；`hit@all`：三轮均命中 /145。逐轮、L0/L1/L2、pair 与 NL 簇分层；8 个无 expected 的 pair 不丢弃。
2. 报告总数、K/N/I、report precision `(K+N)/(K+N+I)`、按 pair 的有效率；D2/D1-only 敏感性按同一固定协议复算。重复有效报告不自动计 I，N 是台账外有效报告而非未经归并的独立缺陷数。
3. W0/W1/W2、完整/unsupported/error/true/false 回执、发布/过滤/绑定未闭合的计数，以及与最终命中的关系；W2 数不替代 hit 或 precision。
4. 完成、失败、降级、未裁定和报告覆盖单列；逐个核销全部计划单元及最终报告。未闭合裁定时不宣称全量 precision，不将困难样本移出分母。

## 5. 事前分析与解释边界

主要比较是当前匹配 full 与 A1 的差值。历史比较固定引用 `final_results/v61_source_divergence_vs_x1v2_baseline`，核对 903 reports、K/N/I=561/198/144、precision=759/903、FULL hit=323/435、130/145、82/145；v61 不是当前 12 条的严格单因素对照，其差异中还包括词表/提示词与服务时间。

假设：检查信息可能增加候选覆盖与重复命中稳定性；移除后 `hit@1/@all` 更可能下降，但幅度未知。precision 和报告数方向不确定：撤掉检查派生候选可能同时减少正确报告与误报，撤掉检查型抑制也可能增加误报。不预设 L1/L2 整层下降，不把历史来源分解或 pass 回执数换算成因果贡献。

全部 lost/gained expected 单元先列清，再沿契约提取、候选产生、绑定/执行、D 筛选、发布归并和独立裁定追踪。保留无法唯一归因的差异，不把随机变化硬归到 inspect，也不把有机制的异常统称偶然性。额外检查既有 0009/0024/0034 风险在两臂的分布；这些只是分析锚点，不为它们增加方法特判或运行预算。

比较以案例内配对和描述性效应为主；不把 435 单元或 162 格当独立样本。附按 9 个 NL 簇成组、两臂同步重采样的 10000 次 bootstrap（seed=20260906），每次保留簇内制品与全部轮次；报告百分位区间及九簇逐一留出敏感性，不将少量簇的区间升级为普遍性或显著性承诺。每轮命中数另列，round 标签不是共同随机种子。

若覆盖下降且精度接近，讨论候选发现/稳定定位的增益；若覆盖接近而稳定性下降，讨论可靠性；若覆盖与精度反向变化，报告取舍；若差异很小或 A1 更好，收窄前置检查的增益主张并分析冗余或干扰。所有结论限定本模型、方法版本与输入集，不宣称整个 C1 或 FCSTM 无效，不要求出现正结果才结束。

## 6. 证据与归档

运行前必须完成实际 prompt/schema、全消费者隔离、候选谓词可执行、默认 full 对拍、worker/resume 与 judge 读取检查；代码和本登记先推送，再启动 smoke。smoke 通过仅表示工程开关和完整性可用，不证明质量等价。

Smoke prompt/raw output、逐格审计、测试 XML 和对拍数据仅留本地 gitignored `runs/paper1/a1_no_inspect_20260906/`；中文分析放论文 `reports/`。正式原件、配置身份、全阶段记录、错误和可复算结果按 generations/final_results 现有规范归档，保存逐文件 hash 和复算命令；私有 judge 执行材料与密钥不进入公开制品。正式批次可以离线核销全部报告与指标，不能只有一张手填结果表。

## 7. 用户澄清与请求层恢复补充（2026-09-06，事后追加）

以上原登记保留，不倒改为事前共识。用户进一步明确：**A1 的研究预期是 hit 大幅下降，尤其 L2；A1 precision 方向未知；precision 大幅下降属于 A2 的理论预期。** 这不是实测结论，也不是取得该方向才结束的门。交付主线是 A1 54×3、Luna judge 与既有 frozen v61 的系统比较；额外 full 仅作附加参考，不是 A1/judge 的前置门，也不启动第三批 full。与 v61 的历史版本差异及解释限制仍逐项保留。

初批与低并发 recovery 暴露了请求控制缺陷：LangChain 对空流的普通 ValueError 未进入已有 transport retry，安装的 Responses 转换器还会丢弃 `response.failed`。因旧日志没有原始 SSE，不能倒推每次事故一定是哪种服务端失败，也不能宣称已证明并发过高。修复只涉及共享请求控制：SDK 解码后的事件在进入 LangChain 前核验失败终态/异常 EOF，保存错误、request/response ID、usage 与事件原因；明确瞬态故障进入原有同请求有界恢复，鉴权/非法请求/真实 schema 错误不得被泛化为可重试网络问题。正常请求、方法 prompt/schema、12 条谓词、发布门及 judge 协议不变。

运行切换先核对确切 PID/子进程与当前格，停止旧 A1 派发并给在途格至多 300 秒排空。旧完整产物、失败回执与未完成审计片段均保留；不能向旧 run 写入新源码身份。新恢复目录另记 source commit、旧来源 hash 和逐格选择清单：成功格原件复用；明确 provider 失败及缺失格才恢复；纯方法诊断不作为重抽样理由。可复用的成功阶段仅在 prompt、schema 和输入一致时重放；失败阶段内已有成功响应也须按同请求验证后重放，不能丢掉已获得的反馈。无法精确复用时必须显式记录，不能伪称同请求恢复或选择更有利输出。统计固定 54×3、145×3 分母，原始与恢复来源、失败和未裁定覆盖单列。

恢复不继续把 workers=2 作为最终措施：使用 8 个独立格 worker 起步（旧 full 的 2 个 pair worker 另计），记录实际在途请求数、首块延迟、重试/限流和成功吞吐；不以 30 分钟硬时限改变方法或盲目增加并发。原子审计数据和恢复脚本留 ignored runs，稳定结果及限制进入中文报告。
