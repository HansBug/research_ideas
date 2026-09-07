# E2 三模型双臂全量实验：事前登记

登记日期：2026-09-07，真实调用之前。依据：[E2 合同 #208](https://github.com/HansBug/research_ideas/pull/208)、[伞 PR #179](https://github.com/HansBug/research_ideas/pull/179)、[E1 四模型交接](../../../../reports/model_readiness_20260906/2026-09-07-06-12-00-four-model-handoff.md)。执行进度留 GitHub，结果另行归档；本登记不预设方法增益的方向。

## 1. 研究范围与运行清单

新增模型严格依次为 Claude Sonnet 5、Qwen3.8-27B、Muse Glimmer-30B。每款 baseline/ours 两臂各 54 pair × 3 round = 162 格，共 324 格；新增总量 **972 格**。Luna 不新跑：只读复用 [canonical v61 ours/baseline 与已有裁定](../../../../final_results/v61_source_divergence_vs_x1v2_baseline/README.md)，不重裁成功历史，不为 A1/A2 新增匹配 full。

每款先执行 `0019/0029/0049`、round 1、两臂共六格，总生成并发 3；完成全部生成检查和 Luna 两读/必要仲裁后，补该款 round 1 其余 102 格，再依次 round 2、3。完成该款 324 格生成及裁定后才进入下一模型。首批协议、配置与源码不变的有效格计入正式结果，E1 smoke 不计入。少报告、零报告、负效果或正常证据降级不构成重采样、换模型或调档位理由。

计划格为下面 54 pair 与 `{Sonnet,Qwen,Muse} × {baseline,ours} × {1,2,3}` 的完整笛卡尔积；pair 顺序除首三格外按编号递增。54 pair 对应 9 个 NL 簇 × 6 个制品，唯一台账 145 条，L0/L1/L2=71/35/39，每臂 expected-round 分母 435。无 expected 的 pair 同样运行并参与 precision。

```text
0000 0001 0002 0003 0004 0005 0006 0007 0009
0010 0011 0012 0013 0014 0015 0016 0017 0019
0020 0021 0022 0023 0024 0025 0026 0027 0029
0030 0031 0032 0033 0034 0035 0036 0037 0039
0040 0041 0042 0043 0044 0045 0046 0047 0049
0050 0051 0052 0053 0054 0055 0056 0057 0059
```

新 ours 使用 P1 当前 12 谓词 `S1-S5/G1-G3/R1-R3/V1`；Luna v61 是原 19 谓词及历史 provider/日期/配置。主分析为每个 backbone 内 baseline/ours 的配对差值；跨模型不是仅改变 backbone 的严格因果对比。A1/A2 的单模型结论不外推到其他模型。

## 2. 输入、源码与身份

输入根为论文目录的 `pipeline/representation/reports/llms_emp_r45_java_60`，生成只读完整公共输入闭包；baseline 读取 NL 与作者 PlantUML，ours 使用当前固定表示、源码追踪与检查。禁止生成端读取 ledger、expected answer、judge 结果、历史 report 或 Luna 中间生成物。原有语义投影不改；禁止额外截断、摘要、compact 或删除输入来规避容量。

| 身份 | 运行前核验值 |
|---|---|
| 上游源码基点 | E1 squash `8aa0d4201588f060e65715240216fcb4e994e50b`；其源为 `2c3d5690ce8796139efd9157681cc447d50d9970` |
| E2 当前路径的完整输入 manifest 集合 | `sha256:71cf9f56071284e22a2db187ee784d98f571f8e26d6a57e504ccb3e024e4f35e` |
| 617 个受跟踪输入文件的相对路径/内容 hash 集合 | `sha256:829b88879f8502fa1ce3792c73e933b29ac2fc18b00e850e47e7c8a096627419` |
| ledger 原文件 SHA-256 | `sha256:b5a38d3d24a51e980e5b9f5afc7c8c66aded59f3b51f16afe67e0deb592d0e36` |
| registry | `four-family-12-core.v1`；`sha256:27e6bee263a37079cb86aa5dfdc904e3ba9711533b6cb1c91e9d911912d7d42d` |
| ours prompt/schema | `sha256:744e7f489591904a08e9919ded9f99ec73c2d55d81225fbd8a9ec18dca8fefe2` |
| baseline prompt | `sha256:17e5067b44442ba07fadeb26ed3612ba21bf762c9bde10b3cb162139817fc2d9` |
| baseline schema 源文件 | `sha256:1cb17cfa946e4841e385b73535ec1c4e74067625616ffb3721cf3a6758fa011a` |
| pyfcstm | `901f30e981c29eb8e304b33d61985652d2e85b2e` |
| judge 协议快照 | `d774d9bd3e4c4fe04735ed1d4ec064be197cfadcd52e21c8226e37175b29b210` |
| judge 全部语义 prompt | `sha256:761309756a872bd52810acca1e667864acbff91e0e1f10540de7c064710a8fda` |
| judge models 源文件 | `sha256:11191938b76f6ca6a2919ec6bf7c05b34ae09359c49b739c73f85dc9f2ba1753` |

manifest 包含绝对 artifact 路径，搬到独立 E2 worktree 会改变 manifest hash；617 文件内容已与 E1 工作区逐文件对拍一致，0000 manifest 去路径/自 hash 后结构相同。不能将旧 A1 路径相关 hash 抄为本轮身份。各调用保存实际 pair hash；最终归档另用相对路径/内容 hash 复核。

实际 source commit 是包含本登记与必要接线的干净、已推送 E2 提交，由启动时 `git rev-parse HEAD` 写入每个生成/judge manifest 和原始调用记录；不伪造文档包含自身 commit 的循环 hash。原生 method 新增 `--rounds 1 --round N`，独立执行指定轮次，round 标签从输入到回执一致；严格 resume 仍冻结 profile/config/source/pairs/round/stream/retry。解除旧 Luna 专用 full gate，但保留显式 live/full 授权。只改调度与记录，不改每格算法或研究 schema。

## 3. 模型与请求配置

以下 baseline/ours 均 stream，英文生成值，temperature/top_p/seed 不新增 override，省略值诚实记 provider/template default。模型公开能力与来源沿用 [E1 benchmark](../../../../reports/model_readiness_20260906/2026-09-07-04-30-00-candidate-benchmarks.md)，不按本轮效果挑选。商业 model ID 来自渠道回报，不冒称独立认证上游 revision。

| 角色/profile | 精确 model / adapter | 推理设置 | context / 输出 |
|---|---|---|---|
| Sonnet `claude-sonnet-5` | `claude-sonnet-5` / anthropic messages | provider default；两臂不显式传 thinking/effort | 1,000,000 / 显式最大 128,000 |
| Qwen `e1-qwen38-27b` | `qwen3.8-27b` / openai chat-completions | 服务模板 low；两臂不另覆盖 | 1,000,000 YaRN / remaining_context，不发送额外 output cap |
| Muse `e1-muse30b` | `muse-glimmer-30b` / openai chat-completions | Muse 模板 high；同一 serving adapter | 131,072 / remaining_context，不发送额外 output cap |
| 唯一新增 judge `gpt-5.6-luna` | `gpt-5.6-luna` / openai-responses | shared runtime 的 none；新六臂相同 | profile 1,050,000 / 128,000；裁定沿用原协议 24,000 请求预算 |

开放模型 profile 中 output 分别为 1,000,000/131,072 是配置占位上界；实际可生成空间为窗口减去完整输入与服务开销，不能当成输入之外的额外窗口。所有生成无人为10K cap；judge 24K 是单独冻结的现有裁定协议，不套用生成端策略。真实 HTTP 参数、usage（reasoning 已包含于 output，不二次相加）、finish/incomplete 和缺失值留审计。

| profile | 不含密钥/价格的 model_config_hash |
|---|---|
| Sonnet | `sha256:b31ee2c0247e9b97bd302e9eb2294f0dc16d059c63a8a203027bc5fb3abfdaf2` |
| Qwen | `sha256:39b399216a2768a161e2b3252c1a04ee1d6f2b4e1691f05e4dbc0b8de29a110a` |
| Muse | `sha256:002bdd8203810f13f037e635ee07964b433f178f05f05ea29bd8a2f85260c2f9` |
| Luna judge | `sha256:60722133534f8179764a454aa0e95645d5c2325da54da2c0831fffb9b7103209` |

`.llmconfig.yml` 为 E2 独立私有快照，权限600、ignored；不使用 `.env`，不发布密钥或私有端点。启动前核对上述 hash，变更必须登记。客户端沿用 Python venv、langchain 1.3.4/core 1.6.2/openai 1.2.2/anthropic 1.4.4、OpenAI SDK 2.41.0、Anthropic SDK 0.117.0、httpx 0.28.1、Pydantic 2.13.4；不升级依赖。

两开放模型固定 E1 独立 conda/TP4/GPU4–7，保护0–3和主环境。Qwen revision `1d4bf0f2ff6012fd82039f2fa52739d0dd7c60c0`；Muse `a4e59da52a7bc87ae7251dd5545c0dd437c44b68`。完整 SGLang0.5.19/XGrammar0.2.1/ATEM、CUDA与YaRN参数见 [E1 复现附录](../../../../reports/model_readiness_20260906/2026-09-07-11-55-00-reproduction.md)；顺序切换共享8100端口，先核对作业归属、在途请求和 model ID，不抢他人GPU。

## 4. 超时、错误与恢复

| 入口 | 请求时限 | 恢复纪律 |
|---|---|---|
| baseline | 显式 SDK timeout=300s，connect/read/write/pool；原 sync runner 无额外整请求 deadline | transport retries=8，SDK retries=0；同请求退避5/20/60/120/240s，尾值重复；schema原地2次，反馈保持原实现 |
| ours | 首字节/read idle300s，单请求deadline600s；原 shared runtime 按结构轮次及重试保留有界 stage/外层预算 | transport retries=8，SDK retries=0；同一退避序列；原有6次structured反馈与一次 provider-only 局部死调用恢复保留 |
| judge | 与 shared runtime 相同；输出24K来自既有裁定协议 | transport retries=8；两次 validity reading、必要 arbitration；不因效果重裁 |

baseline 与多阶段 runtime 共用300s网络空闲界，但 baseline 没有额外600s整请求取消，二者不声称时限完全一致；保留长流，不以整格短墙钟阈值杀任务。发生超时时区分请求空闲/总deadline、provider/队列/tunnel/客户端层；必要对照同一完整payload的本机adapter、本机SSE、远端直连。语义设计、schema/validator/谓词/eligibility 冻结。

provider故障或结构失败保留原件。正常降级（包括证据不支持、内部修订/后端义务未闭合）按既有回执落盘，不丢困难格、不改分母。实质修复先停止受影响新派发，保留版本和失败，针对性回归并提交/push后恢复；不能把不同协议静默混算。只补未完成部分，成功 method 不因 judge失败重跑，成功裁定不因质量重裁；若不能精确复用成功阶段则显式登记，不虚称同请求恢复。

## 5. 独立裁定与统计门

固定 `semantic-judge.two-stage.v3.11`、prompt v11、`validity-readings=2`、`validity-aggregation=arbitration`、`validity-arbitration-trigger=any`、`k-closure=relation_first`、`closure-profile=full`。动态 schema 因报告/expected 的行数而异，每次实际 schema hash写入调用回执，模板源码与语义prompt由§2冻结。新报告全部由当前 Luna 裁定，历史Luna两臂引用原冻结决定。

judge 仅一个受控总池≤16，批次串行，启动前检查所有已有消费者。完成两读及必要仲裁后才计 judged；method完成、HTTP200、CLI退出0或子调用success不能代替。每格发布报告ID集合必须与完整最终裁定集合相等；零报告格也保存原生完整回执。原生 `--report-filter` 只用于补缺失报告，不用于择优。所有fail/missing必须闭合，不能删失或缩小分母。

每模型每臂162格全部裁定后才汇总该完整组正式指标：FULL hit@1=expected-round命中/435；hit@3=任一轮命中/145；hit@all=三轮均命中/145；按L0/L1/L2、轮、NL簇分层。precision=(K+N)/(K+N+I)，同时严格D1/D2-only、K/N/I、报告数/误报数、适用W/执行回执/源码归因。关系优先可能使D0以已知关系进入K，严格口径必须同报。N是台账外有效报告，不冒称去重后的新缺陷数量。

主要效应为同backbone的 ours-baseline 配对差。9个NL簇同步成组重采样10000次，seed=20260907，每次保留簇内六个制品、全部三轮和两臂；给出95%百分位区间及九簇逐一留出敏感性。不得将972格或单份报告当独立样本；round标签不表示共用随机种子。报告负效果、异质性和多指标不确定性，不事后改主要指标，不宣称少量簇上的普遍性、统计等效或因果机制证明。

固定Luna裁定不消除同模型偏好；新结果人工确认数初始为0，后续只按实际确认更新。自动裁定不写成已经人工确认，也不因等待未来签收停止本轮授权交付。历史provider/日期、12/19谓词、两臂请求数/预算差异均进入结果限制。

## 6. 原生命令与原始记录

以下从仓库根执行，`PAPER`为论文路径；设置显式PYTHONPATH指向当前checkout，使用根venv。临时observer仅透传记录HTTP请求原字节、SSE、时序、usage及错误，不修改消息或请求参数；核心命令直接复用native runner，没有新的调度框架。

```bash
PAPER=project_1_llm_state_machine_modeling/paper_stm_issue_discover
export PYTHONPATH=".:$PAPER/method/src:$PAPER/judge/src"
export LLM_CONFIG_FILE="$PWD/.llmconfig.yml"
# A single independent round; first batch shown, then remaining51 and all54 for r2/r3.
venv/bin/python -m paper_stm_method.cli \
  --report-root "$PAPER/pipeline/representation/reports/llms_emp_r45_java_60" \
  --output-dir runs/paper1/e2_20260907/sonnet/ours/r1-first \
  --profile claude-sonnet-5 --ablation none --rounds 1 --round 1 \
  --pair-id 0019 --pair-id 0029 --pair-id 0049 \
  --workers 3 --transport-retries 8 --allow-live --allow-full-live
venv/bin/python "$PAPER/baseline_arm/src/runner.py" \
  --case 0019 --profile claude-sonnet-5 --round 1 --content-language en-US \
  --output-dir runs/paper1/e2_20260907/sonnet/baseline/r1-first/0019-r1 \
  --transport-retries 8 --timeout 300 --stream
# SOURCE points to the native method run root or baseline batch root.
venv/bin/python -m paper_stm_judge.cli \
  --report-root "$PAPER/pipeline/representation/reports/llms_emp_r45_java_60" \
  --ledger "$PAPER/discover_matrix/ledger_v2/ledger.json" \
  --source-format evidence_discovery_release --source-root "$SOURCE" \
  --output-dir runs/paper1/e2_20260907/sonnet/judge/ours/r1-first \
  --run-id "$NEW_JUDGE_ID" --round 1 --pair-id 0019 --pair-id 0029 --pair-id 0049 \
  --profile gpt-5.6-luna --workers 16 --transport-retries 8 --validity-readings 2 \
  --validity-aggregation arbitration --validity-arbitration-trigger any \
  --k-closure relation_first --closure-profile full --allow-live
```

baseline裁定改为 `--source-format x1v2_record` 和对应source根；生成两臂顺序运行，不能每臂另开3workers叠加超额。所有输出隔离到 backbone/arm/round/pair/attempt；已有成功输出不覆盖。原始prompt/raw/SSE/失败及临时脚本仅留 ignored `runs/paper1/e2_20260907/`，另备份并检查hash；仓库只收紧凑冻结决定、来源hash、复算与中文Markdown。raw未入Git不等于可从fresh clone重放全部历史，需另行取得原件。

最终按972唯一格核销所有生成与裁定，离线复算分母/数字/来源；必要测试、最终源CI和范围内C/I/冲突闭合，commit/push并交付报告/PR后结束。E2/#179合并留用户审阅，不自行启动O2、写作或其他实验。
