# A1-ext 三模型无检视事实消融：覆盖、分层与报告有效比例

> 结论冻结：2026-09-12 10:17:38（Asia/Shanghai），即[冻结归档](../final_results/a1_ext_20260911/README.md) `results.json` 的 `frozen_at`。本报告解释 Claude Sonnet 5、Qwen3.8-27B、Muse Glimmer-30B 三个固定配置在 `no-inspect` 条件下的完整结果，并与 gpt-5.6-luna 的 [A1 归档](../final_results/a1_no_inspect_vs_v61_20260906/README.md)并列为四模型对照。面向导师讨论的学术解释见 [A1-ext talk](../../talks/2026-09-12-实验-A1ext三模型无检视事实消融与论文叙事.md)。正文稳定引用键指向文末证据链；机器判定优先于本文。

## Material Passport

| 项 | 值 |
| --- | --- |
| 事前登记 | [preregistered.md](../discover_matrix/docs/generations/a1_ext_20260911/preregistered.md)，提交 `7ef78e604`，先于任何真实调用推送 |
| 合同 | [伞 PR #179](https://github.com/HansBug/research_ideas/pull/179) §4.8、子 PR [#213](https://github.com/HansBug/research_ideas/pull/213) |
| 网格 | 冻结 54 pair × 3 round，每模型 162 格，三模型 486 格；`00x8` 系列永久排除 |
| 台账 | 145 条，L0/L1/L2 为 71/35/39，expected-round 435；ledger `sha256:b5a38d3d…` |
| 干预 | `--ablation no-inspect --rounds 3`，method 协议、prompt、12 谓词与 A1 [#205](https://github.com/HansBug/research_ideas/pull/205) 相同 |
| 对照 | E2 [#208](https://github.com/HansBug/research_ideas/pull/208) 同模型冻结 Full ours，只读；Luna 对照为 A1 归档的 v61 Full |
| judge | `gpt-5.6-luna`，协议 `v3.11`，两读加必要仲裁，`relation_first`，`full` closure，aizzz 通道，24 workers；与 A1 的 `judge_aizzz` 批次同一提供方 |
| 完成度 | 三模型 486/486 格 method eligible、486/486 格 judge completed、1964 份报告全部裁定，pending=0；新增人工确认 0 |
| 归档 | [final_results/a1_ext_20260911](../final_results/a1_ext_20260911/README.md)，`results.json` 8.9 MB，可 provider-free 复算 |

## 1. 结果回答了什么

**四个固定模型配置上，关闭检视事实后固定台账的覆盖都明确下降，行为层（L2）是主要受损层。** 三个新模型的 hit@1 分别下降 20.69、24.60、16.32 个百分点（pp），与 Luna A1 的 −20.69 pp 同向；L2 hit@1 下降 46.15、42.74、26.50 pp，Luna 为 −40.17 pp。四模型 L2 三轮均命中的台账条目从 22/20/19/28 降到 4/3/7/10。九个 NL 簇的配对 bootstrap 区间在 hit@1、hit@3、hit@all 和 L2 hit@1 上全部不跨零。这把 A1 单模型的结论从“在 gpt-5.6-luna 上”扩展到四个配置的方向一致性，但仍是同模型历史配对比较，不是严格单因素因果估计。[clm-main] [clm-coverage] [clm-ci] [clm-limits]

**报告有效比例的变化依模型而异。** 普通 precision 在 Sonnet、Muse 上下降 5.27、7.84 pp，九簇区间不跨零；在 Qwen、Luna 上下降 3.34、3.71 pp，区间跨零。strict precision 三个新模型区间全部跨零，Luna 归档为 +2.31 pp。因此结论应写成“覆盖一致下降，有效比例方向依模型”，不能写成“四模型精度统一下降”。[clm-main] [clm-ci]

**下降集中在需要结构事实的台账类。** 意外终止（unintended_terminal）类的 FULL 命中从 48/37/42/52 降到 12/3/9/8，触发类从 64/59/60/66 降到 18/31/24/26，全局或 pair 级条目从 95/82/77/95 降到 43/25/47/51；效果、状态类命中在多数模型上持平或略升。候选层面，带谓词候选与 W2 候选在三模型上都少了一半以上。三组来源可核查的案例与这些计数相容：死端状态与带触发的初始边在四模型的无检视条件下全部零命中，而不可达类命中在 Qwen、Muse 的无检视条件下反而增加。[clm-content] [clm-funnel] [clm-case-deadend] [clm-case-initial] [clm-case-unreachable]

## 2. 干预：no-inspect 关闭什么、保留什么

检视事实（inspection）指方法在 LLM 发现之前由确定性工具对作者状态机计算出的结构与拓扑事实，例如某状态无出边、某初始边带触发、某状态从初始配置不可达，以及由这些事实派生的检查型候选、补充义务、预检和抑制。`no-inspect` 按 A1 冻结协议关闭 reference inspection、inspection-equivalent、verify、SMT 前置上下文、working-contract 诊断、检查型候选与补充义务、预检与抑制，以及内部 D 判定中依赖这些事实的确定性校验；首轮、补全与纠错阶段均使用受限视图，不得从模型中间表示或其它文件重建同一事实。保留 FCSTM 编译与作者源追踪、普通契约提取与语义发现、12 条谓词的真实执行回执、确定性发布与去重。它不是整个 C-1 的消融，也不是纯 LLM 基线或谓词子集消融。[src-prereg] [clm-design]

| 环节 | Full | no-inspect |
| --- | --- | --- |
| 确定性检视事实及其派生候选、补充义务、预检、抑制 | 生产并注入发现与复核 | 关闭 |
| 内部 D 中依赖检视事实的确定性校验 | 保留 | 关闭 |
| 契约提取、补全、两路语义发现、前沿扩充、语义复核与修订 | 保留 | 保留（受限视图） |
| 12 条谓词的绑定、编译与真实执行 | 保留 | 保留；候选专属谓词后端仍可读取模型 |
| 确定性发布、真值拦截、去重 | 保留 | 保留 |
| 独立外部 judge | 保留 | 保留 |

三模型使用与 A1 相同的方法源码路径，只把模型换成各自的冻结 profile：`claude-sonnet-5`（Anthropic 直连）、`e1-qwen38-27b`（远程 GPU 4-7 SGLang TP4，权重 `1d4bf0f2…`，1M YaRN，reasoning effort low）、`e1-muse30b`（同一组卡，权重 `a4e59da5…`，131072 上下文）。开放模型 profile 沿用 E1/A3 的 `remaining_context` 输出预算模式。事前假设为 H1 覆盖与 L2 下降、H2 L0/L1 变化小于 L2、H3 精确率方向不预设；结果不以符合假设为准入条件。[src-prereg] [clm-design]

## 3. 完整性、来源与运行边界

### 3.1 逐格核销

| 核销项 | Sonnet | Muse | Qwen |
| --- | --- | --- | --- |
| method run | `10ed3f53…`，24 workers，12:48:20 至 13:32:05 UTC | `6ea657d7…`，24 workers，12:41:28 至 13:30:13 UTC | `1dc566e6…`，24 workers，13:55:41 至 16:38:49 UTC；另 5 格隔离恢复 |
| method 格 | 162/162 eligible；122 completed、40 带 d_adjudication 诊断 | 162/162 eligible，162 completed | 162/162 eligible；154 completed、3 带诊断、5 格由隔离恢复替换 |
| 发布报告 | 536 | 690 | 738 |
| judge 格 | 162/162，三轮各 54 | 162/162；r3 为 53 格主 run 加 1 格重采样 | 162/162，三轮各 54 |
| judge run（轮:run:rc） | r1 `dec87ac9`:0、r2 `c29e2173`:0、r3 `fa959dd1`:0 | r1 `ace3c21d`:0、r2 `c387e3c6`:0、r3 `076b9593`:1（0059 失败）、r3 `89b5f767`:0（0059 重采样） | r1 `b8e05369`:0、r2 `f19ef4a5`:0、r3 `df8f1b6a`:0 |
| judge 用时 | 26 / 28 / 29 分钟 | 55 / 61 / 68 分钟，重采样 30 分钟 | 40 / 35 / 41 分钟 |

所有格的 method 源码提交均为 `7ef78e604`，分支 `paper1/a1-ext`，运行前 tracked worktree 干净。judge 来源 `judge_source/<model>/method/*/round-*.json` 逐文件 hash 记入 `source_manifest.json`，judge 输出逐文件 hash 同表；`results.json` 的 486 格与 1964 份报告经 `analyze_a1_ext.py` 逐格、逐报告、逐 expected-round 闭合。[src-results] [src-source] [clm-sources]

### 3.2 provider 故障、恢复与排除

| 事故 | 处置 | 是否进入统计 |
| --- | --- | --- |
| I-1 Sonnet 首次启动 162/162 格 Anthropic 403（tmux 会话缺代理环境） | 整 run 移出，脚本导出代理后以新 run 重启 | 否 |
| I-3 旧编排器未被挂起，起了重复的 Muse r2 judge run `71922e9b`（约 7 分钟、3/54 pair） | 杀掉并移至 `judge/_aborted`，合法 run `c387e3c6` 完整 | 否 |
| I-4、I-5 本机到 GPU 节点的 8100 隧道两次中断（约 14:41 至 14:54、约 15:02 至 15:14 UTC） | 隧道重建并改为不依赖 ControlMaster 的专用连接；在途请求由 method 的 transport retry 吸收 | Qwen 5 格因重试耗尽落为 provider 失败（4 格 `Connection error`/`provider_timeout`、1 格由 10 次 `provider_timeout` 诱发 `limit_exceeded`），按登记以同一 profile 单格隔离重跑一次并替换，原失败回执保留 |
| I-6 Muse r3 judge 在 pair 0059 上第二读连续 6 轮给出校验器拒绝的同一组合（D1 与核心子句 REFUTED 并存），`turns limit exceeded` | 非 provider 故障；按 v61 与 A4 先例以同一冻结代码重采样一次，成功；原失败 run 保留 | 重采样格进入统计，原失败保留为审计 |
| I-7 编排器在启动 Qwen r3 judge 后过早写 DONE | 人工接管，judge 独立会话不受影响 | 无影响 |

完整时间线与根因见归档内 [INCIDENTS.md](../final_results/a1_ext_20260911/INCIDENTS.md)。上述处置全部在事前登记 §3 的失败处理口径内；不能把本次写成“零重试、零故障”。Qwen 的 328 条 transport retry 记录绝大多数来自两次隧道中断，Sonnet 为 0，Muse 为 8。[src-incidents] [clm-sources]

### 3.3 判定装置

每份发布报告由 `gpt-5.6-luna` 独立完成两次有效性阅读，分歧时进入必要仲裁，再按 `relation_first` 协议在隔离步骤判定与台账条目的 FULL/PARTIAL 关系。有效性步骤只读报告、NL、作者源与允许的制品事实，不读 ledger、方法内部标签、执行 verdict 或 Full 裁定。三模型分别产生 528/678/732 份有效性仲裁凭证、145/193/178 次关系仲裁、891/976/1080 次 judge 结构化调用，judge 侧输入 token 合计约 3.15 亿。judge 与方法中的 Luna 即使同名也是不同角色和调用；“独立”指材料与流程隔离，不代表人工金标准。本次新增人工确认为 0，机器可复算指冻结标签的算术可复算。[clm-eval]

### 3.4 与 Full 对照的历史差异

Full 来自 E2 冻结归档：Sonnet 源 `839cfb793`/`f52507d1a`，Qwen `839cfb793`，Muse `3b9068928`，运行于 2026-09-07 前后，method 最多 16 workers，Sonnet 有 51 格、Qwen 3 格带诊断；本次 no-inspect 于 2026-09-11 运行，24 workers，源 `7ef78e604`。两批的服务、日期、随机性未同步，Full 与 no-inspect 的方法源码也不是同一提交；本文不声称二者的默认路径逐字节等价。judge 提供方均为 gpt-5.6-luna，E2 走 sub2api 通道，本次走 aizzz 通道。上述差异限定“差值可全部归因于检视事实”的强度，不改变冻结计数。[src-e2] [clm-limits]

## 4. 主指标与分层

hit@1 为三轮 expected-round 的 FULL 命中数除以 435，同一台账条目在同轮多次报告只计一次，PARTIAL 不计；hit@3 为至少一轮命中除以 145，hit@all 为三轮均命中除以 145。普通 precision 为 (K+N)/R，全部发布报告进入分母；strict precision 只把有效且外部 D1/D2 的报告计入分子。K 为有 FULL 或 PARTIAL 关系的有效报告，N 为无关系的有效报告，I 为无效报告；N 不是独立新缺陷数。指标算术逐字复用 A1 的 `analyze_a1.calculate`。[clm-eval] [src-code]

表 1：各模型三轮 pooled 主表。[clm-main]

| 模型 | 条件 | 报告 R | K/N/I | 普通 precision | strict precision | hit@1 | strict hit@1 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Claude Sonnet 5 | Full | 823 | 536/183/104 | 719/823（87.36%） | 650/823（78.98%） | 291/435（66.90%） | 270/435（62.07%） |
| Claude Sonnet 5 | no-inspect | 536 | 280/160/96 | 440/536（82.09%） | 410/536（76.49%） | 201/435（46.21%） | 184/435（42.30%） |
| Muse Glimmer-30B | Full | 910 | 544/229/137 | 773/910（84.95%） | 712/910（78.24%） | 322/435（74.02%） | 301/435（69.20%） |
| Muse Glimmer-30B | no-inspect | 690 | 345/187/158 | 532/690（77.10%） | 500/690（72.46%） | 215/435（49.43%） | 202/435（46.44%） |
| Qwen3.8-27B | Full | 958 | 599/256/103 | 855/958（89.25%） | 781/958（81.52%） | 311/435（71.49%） | 295/435（67.82%） |
| Qwen3.8-27B | no-inspect | 738 | 386/248/104 | 634/738（85.91%） | 606/738（82.11%） | 240/435（55.17%） | 223/435（51.26%） |
| gpt-5.6-luna（A1 归档） | Full v61 | 903 | 561/198/144 | 759/903（84.05%） | 678/903（75.08%） | 323/435（74.25%） | 294/435（67.59%） |
| gpt-5.6-luna（A1 归档） | no-inspect | 814 | 392/262/160 | 654/814（80.34%） | 630/814（77.40%） | 233/435（53.56%） | 212/435（48.74%） |

表 2：no-inspect 减 Full 的差值。pp 为百分点。[clm-main]

| 模型 | 有效报告 Full → no-inspect | 相对变化 | ΔI | Δ普通 pp | Δstrict pp | Δhit@1 pp | Δstrict hit@1 pp |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Claude Sonnet 5 | 719 → 440 | −38.80% | −8 | −5.27 | −2.49 | −20.69 | −19.77 |
| Muse Glimmer-30B | 773 → 532 | −31.18% | +21 | −7.84 | −5.78 | −24.60 | −22.76 |
| Qwen3.8-27B | 855 → 634 | −25.85% | +1 | −3.34 | +0.59 | −16.32 | −16.55 |
| gpt-5.6-luna | 759 → 654 | −13.83% | +16 | −3.71 | +2.31 | −20.69 | −18.85 |

三个新模型的有效报告合计从 2347 降至 1606（−31.57%），无效报告从 344 变为 358（+14）；四模型等权 hit@1 从 71.67% 降至 51.09%（−20.57 pp），L2 hit@1 从 73.94% 降至 35.04%（−38.90 pp）。Sonnet 的 I 绝对数下降而 precision 仍下降，是因为有效报告减少得更多；Muse 的 I 上升 21。这些合计描述两批报告的组成变化，没有逐条语义配对，不能称为“若干有效报告转成了无效”。[clm-main]

事后描述性对照：E2 同模型直接发现基线的 hit@1 为 Sonnet 241/435（55.40%）、Muse 247/435（56.78%）、Qwen 225/435（51.72%），L2 hit@1 为 56/117、39/117、49/117；no-inspect 的 hit@1 在 Sonnet、Muse 上低于基线 9.19、7.35 pp，Qwen 高于基线 3.45 pp，L2 hit@1 在三模型上都不高于基线。这一比较未在事前登记中列为主指标，基线运行条件与 Full 相同地属于历史批次，只用于说明关闭检视事实后完整方法相对直接发现的行为层覆盖增益在这三个配置上不再出现。[clm-baseline] [src-e2]

表 3：逐轮结果，每行 54 格，hit 分母 145。[clm-rounds]

| 模型 | 条件 | 轮次 | 报告 | K/N/I | precision | hit |
| --- | --- | --- | --- | --- | --- | --- |
| Claude Sonnet 5 | Full | 1 | 283 | 174/79/30 | 253/283（89.40%） | 92/145（63.45%） |
| Claude Sonnet 5 | Full | 2 | 265 | 169/60/36 | 229/265（86.42%） | 99/145（68.28%） |
| Claude Sonnet 5 | Full | 3 | 275 | 193/44/38 | 237/275（86.18%） | 100/145（68.97%） |
| Claude Sonnet 5 | no-inspect | 1 | 167 | 94/44/29 | 138/167（82.63%） | 64/145（44.14%） |
| Claude Sonnet 5 | no-inspect | 2 | 203 | 104/65/34 | 169/203（83.25%） | 77/145（53.10%） |
| Claude Sonnet 5 | no-inspect | 3 | 166 | 82/51/33 | 133/166（80.12%） | 60/145（41.38%） |
| Muse Glimmer-30B | Full | 1 | 315 | 193/77/45 | 270/315（85.71%） | 108/145（74.48%） |
| Muse Glimmer-30B | Full | 2 | 310 | 179/83/48 | 262/310（84.52%） | 109/145（75.17%） |
| Muse Glimmer-30B | Full | 3 | 285 | 172/69/44 | 241/285（84.56%） | 105/145（72.41%） |
| Muse Glimmer-30B | no-inspect | 1 | 246 | 123/72/51 | 195/246（79.27%） | 72/145（49.66%） |
| Muse Glimmer-30B | no-inspect | 2 | 216 | 105/56/55 | 161/216（74.54%） | 73/145（50.34%） |
| Muse Glimmer-30B | no-inspect | 3 | 228 | 117/59/52 | 176/228（77.19%） | 70/145（48.28%） |
| Qwen3.8-27B | Full | 1 | 315 | 201/84/30 | 285/315（90.48%） | 100/145（68.97%） |
| Qwen3.8-27B | Full | 2 | 327 | 192/94/41 | 286/327（87.46%） | 103/145（71.03%） |
| Qwen3.8-27B | Full | 3 | 316 | 206/78/32 | 284/316（89.87%） | 108/145（74.48%） |
| Qwen3.8-27B | no-inspect | 1 | 245 | 136/73/36 | 209/245（85.31%） | 80/145（55.17%） |
| Qwen3.8-27B | no-inspect | 2 | 246 | 128/90/28 | 218/246（88.62%） | 84/145（57.93%） |
| Qwen3.8-27B | no-inspect | 3 | 247 | 122/85/40 | 207/247（83.81%） | 76/145（52.41%） |
| gpt-5.6-luna | Full v61 | 1 | 325 | 207/76/42 | 283/325（87.08%） | 113/145（77.93%） |
| gpt-5.6-luna | Full v61 | 2 | 287 | 166/61/60 | 227/287（79.09%） | 98/145（67.59%） |
| gpt-5.6-luna | Full v61 | 3 | 291 | 188/61/42 | 249/291（85.57%） | 112/145（77.24%） |
| gpt-5.6-luna | no-inspect | 1 | 294 | 132/97/65 | 229/294（77.89%） | 77/145（53.10%） |
| gpt-5.6-luna | no-inspect | 2 | 277 | 135/91/51 | 226/277（81.59%） | 84/145（57.93%） |
| gpt-5.6-luna | no-inspect | 3 | 243 | 125/74/44 | 199/243（81.89%） | 72/145（49.66%） |

四模型十二组逐轮 hit 全部低于同轮 Full（12/12）。三个新模型的逐轮 Δhit 为 Sonnet −19.31/−15.17/−27.59、Muse −24.83/−24.83/−24.14、Qwen −13.79/−13.10/−22.07 pp，Luna 为 −24.83/−9.66/−27.59 pp；Muse 三轮幅度最一致。轮次一致性说明结论不由单次重复独自造成，同一 NL 的相关性仍在统计解释中保留。[clm-rounds]

表 4：跨轮覆盖与 L 分层。hit@3、hit@all 分母 145；L0/L1/L2 的 hit@1 分母为 213/105/117，L2 hit@3、hit@all 分母 39。[clm-coverage]

| 模型 | 条件 | hit@3 | hit@all | L0 hit@1 | L1 hit@1 | L2 hit@1 | L2 hit@3 | L2 hit@all |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Claude Sonnet 5 | Full | 122/145（84.14%） | 69/145（47.59%） | 133/213（62.44%） | 65/105（61.90%） | 93/117（79.49%） | 39/39（100.00%） | 22/39（56.41%） |
| Claude Sonnet 5 | no-inspect | 98/145（67.59%） | 33/145（22.76%） | 97/213（45.54%） | 65/105（61.90%） | 39/117（33.33%） | 24/39（61.54%） | 4/39（10.26%） |
| Muse Glimmer-30B | Full | 124/145（85.52%） | 88/145（60.69%） | 165/213（77.46%） | 79/105（75.24%） | 78/117（66.67%） | 32/39（82.05%） | 20/39（51.28%） |
| Muse Glimmer-30B | no-inspect | 92/145（63.45%） | 51/145（35.17%） | 118/213（55.40%） | 69/105（65.71%） | 28/117（23.93%） | 16/39（41.03%） | 3/39（7.69%） |
| Qwen3.8-27B | Full | 125/145（86.21%） | 81/145（55.86%） | 165/213（77.46%） | 68/105（64.76%） | 78/117（66.67%） | 34/39（87.18%） | 19/39（48.72%） |
| Qwen3.8-27B | no-inspect | 103/145（71.03%） | 53/145（36.55%） | 120/213（56.34%） | 73/105（69.52%） | 47/117（40.17%） | 22/39（56.41%） | 7/39（17.95%） |
| gpt-5.6-luna | Full v61 | 130/145（89.66%） | 82/145（56.55%） | 153/213（71.83%） | 73/105（69.52%） | 97/117（82.91%） | 36/39（92.31%） | 28/39（71.79%） |
| gpt-5.6-luna | no-inspect | 91/145（62.76%） | 65/145（44.83%） | 107/213（50.23%） | 76/105（72.38%） | 50/117（42.74%） | 23/39（58.97%） | 10/39（25.64%） |

L2 的损失不只是单次覆盖下降：三轮稳定命中的 L2 条目在四模型上从 22/20/19/28 降到 4/3/7/10。L0 也在四模型上下降 16.90 至 22.07 pp。L1 的变化小且方向不一：Sonnet 持平，Muse −9.52 pp，Qwen +4.76 pp，Luna +2.86 pp；不能把 L1 写成任何统一方向。[clm-coverage]

## 5. 变化在哪里

### 5.1 命中单元集合的迁移

表 5：以“台账 ID × 轮次”为单位的命中集合交、差。差集刻画台账覆盖迁移，不是报告的语义一一配对。[clm-coverage]

| 模型 | 共有 | Full 独有 | no-inspect 独有 | Full 独有按 L0/L1/L2 | no-inspect 独有按 L0/L1/L2 |
| --- | --- | --- | --- | --- | --- |
| Claude Sonnet 5 | 145 | 146 | 56 | 69/16/61 | 33/16/7 |
| Muse Glimmer-30B | 188 | 134 | 27 | 58/17/59 | 11/7/9 |
| Qwen3.8-27B | 194 | 117 | 46 | 60/12/45 | 15/17/14 |
| gpt-5.6-luna | 196 | 127 | 37 | 63/9/55 | 17/12/8 |

每个模型的 Full 独有命中都多于 no-inspect 独有，而 no-inspect 独有的 L2 单元只有 7/9/14/8 个。no-inspect 存在 Full 没有命中的单元，所以 no-inspect 报告集不是 Full 的严格子集；第 5.4 节第三个案例是这类增益的一个来源可核查的例子。[clm-coverage]

### 5.2 按台账轴的内容分层

表 6：按冻结台账轴筛选后的 FULL 命中，分母为 3 轮乘该类条目数，每格为 Full → no-inspect。`defect_element` 与 `defect_logic_kind` 是不同轴，跨轴不可相加；`None` 表示该轴上无取值，在元素轴上对应全局或 pair 级条目。[clm-content] [src-ledger]

| 轴 / 取值 | 条目数 | 分母 | Sonnet | Muse | Qwen | Luna |
| --- | --- | --- | --- | --- | --- | --- |
| element = None（全局或 pair 级） | 41 | 123 | 95 → 43 | 82 → 25 | 77 → 47 | 95 → 51 |
| element = trigger | 25 | 75 | 64 → 18 | 59 → 31 | 60 → 24 | 66 → 26 |
| element = transition | 38 | 114 | 61 → 58 | 75 → 64 | 76 → 76 | 77 → 58 |
| element = effect | 18 | 54 | 30 → 37 | 50 → 47 | 48 → 45 | 43 → 51 |
| element = state | 17 | 51 | 29 → 34 | 45 → 41 | 38 → 39 | 28 → 35 |
| element = guard | 4 | 12 | 11 → 10 | 11 → 7 | 11 → 9 | 12 → 12 |
| element = region | 2 | 6 | 1 → 1 | 0 → 0 | 1 → 0 | 2 → 0 |
| logic = unintended_terminal | 19 | 57 | 48 → 12 | 37 → 3 | 42 → 9 | 52 → 8 |
| logic = unreachable | 8 | 24 | 21 → 8 | 19 → 4 | 16 → 17 | 17 → 16 |
| logic = nondeterminism | 5 | 15 | 12 → 11 | 11 → 8 | 8 → 8 | 12 → 11 |
| logic = nontermination | 5 | 15 | 10 → 9 | 9 → 8 | 7 → 9 | 10 → 11 |
| logic = hierarchy_entry | 2 | 6 | 1 → 2 | 3 → 0 | 2 → 1 | 2 → 2 |

意外终止类在四模型上损失最重：19 条条目的 57 个 expected-round 中，Full 命中 37 至 52 个，no-inspect 只剩 3 至 12 个。触发类与全局或 pair 级条目也在四模型上同向大幅下降。效果与状态类在多数模型上持平或略升，说明普通语义路径仍会提出这两类主张。不可达类出现模型分歧：Sonnet、Muse 下降，Qwen、Luna 几乎不变。这些是探索性分层，没有多重检验校正，也没有为每类条目建立独立因果对照。[clm-content] [clm-limits]

### 5.3 候选、证据资格与执行组成

表 7：从方法原件直接计数的候选与发布组成。候选指进入绑定与执行前的全部生成主张；W0/W1/W2 为方法的证据资格，分别表示缺少足够定位、有具体来源支撑但无合格执行确认、满足身份与绑定资格的机械执行证据；`executable_evidence`、`semantic_hit`、`coverage_gap`、`execution_degraded` 为候选的覆盖类。W 等级与外部 D 等级、L 等级均无一一对应。Full 一侧来自 E2 `cells.json` 的 `candidate_evidence`。[clm-funnel]

| 模型 | 条件 | 候选 | 带谓词候选 | 候选 W0/W1/W2 | executable_evidence / coverage_gap | 发布 | 发布 W1/W2 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Claude Sonnet 5 | Full | 1894 | 779 | 421/1218/255 | 255 / 421 | 823 | 646/177 |
| Claude Sonnet 5 | no-inspect | 1427 | 433 | 431/906/90 | 90 / 431 | 536 | 488/48 |
| Muse Glimmer-30B | Full | 1793 | 744 | 172/1170/451 | 451 / 172 | 910 | 629/281 |
| Muse Glimmer-30B | no-inspect | 1482 | 454 | 175/1083/224 | 224 / 175 | 690 | 576/114 |
| Qwen3.8-27B | Full | 2090 | 837 | 455/1250/385 | 385 / 455 | 958 | 705/253 |
| Qwen3.8-27B | no-inspect | 1661 | 572 | 443/980/238 | 238 / 443 | 738 | 586/152 |

三模型的候选总数下降 17% 至 25%，带谓词候选下降 32% 至 44%，W2 候选下降 38% 至 65%，发布报告中的 W2 从 177/281/253 降到 48/114/152。这与 A1 单模型观察一致：保留谓词并不等于能生成并绑定足够多的可执行候选，没有前置事实时部分行为主张在到达谓词前就已缺席。W0 候选数几乎不变，说明覆盖缺口的量级没有因关闭检视而放大。这些是组成变化，不是“在原候选集合上均匀删减”。[clm-funnel]

### 5.4 三个来源可核查的案例

按分析目的选取三组同模型、同 pair、同轮次的 Full/no-inspect 对照，不是随机抽样，不估计各机制占比。作者源 NL/STM 与冻结报告原文均经本次 AI 逐条核对；报告 ID、裁定与理由在 `results.json`。[clm-case-deadend] [clm-case-initial] [clm-case-unreachable] [src-inputs]

**案例一：列车控制的两个死端状态在四模型无检视条件下全部零命中。** pair `0004` 的 NL 第 2、3 句要求列车到站后进入 `Stopping`、检测到障碍时进入 `EmergencyStopping`；作者 STM 第 29、30 行写出 `InMotion --> Stopping : Arrived/Stop, Send Arrived` 与 `InMotion --> EmergencyStopping : Obstacle Detected`，第 37 行 `state Stopping` 与第 32 至 35 行 `EmergencyStopping` 都没有任何出边，根层也没有成组出边或终止符。台账 `INS-0004-01`、`INS-0004-02`（L2，unintended_terminal）记录这两处死端。Full 的 Sonnet r1 以 `0004:r1:issue:2`、`issue:3` 两份 K/D2、W2、谓词 V1 报告命中两项；Muse Full r1 的 `issue:3`（K/D2，V1）与 `issue:4`（K/D1，V1，W2）同样命中。no-inspect 的 Sonnet r1 只发布两份关于 `DoorsClosing` 局部初始目标的报告（均命中 `EIS-0004-01`），Muse r1 发布 5 份，其中 3 份为效果信号、触发与入口动作名的“不匹配”主张（均 I），没有任何死端主张。四模型上这两项在 Full 中三轮全部命中，在 no-inspect 中三轮全部未命中。这与死端候选入口来自检视事实的解释一致，单例不能分辨缺失发生在义务、候选还是复核环节。[clm-case-deadend]

**案例二：带触发的初始边在四模型无检视条件下全部零命中。** pair `0040` 的 NL 第 3 句为 “when power on, the system turn into human driving mode”；作者 STM 第 2 行 `[*] --> HumanDriving : Power On` 把触发事件挂在根层唯一初始边上，第 7 行 `[*] --> AutoInitial : Enter Autonomous Mode` 对复合态默认入口做了同样处理。台账 `VU-0040-01`（根层）与 `EIS-0040-03`（复合态）均为 L0 trigger 类。Full 的 Qwen r1 用 `issue:1`、`issue:5`（K/D2）命中根层条目、`issue:4`（K/D2）命中复合态条目；Luna Full r1 用 `issue:1`、`issue:8`（K/D2，后者 S3、W2）与 `issue:5`、`issue:6`（K/D0）分别命中。no-inspect 的 Qwen r1 只发布一份 N/D2 报告，主张 `AutoFinal` 到 `HumanDriving` 缺少直接迁移（S2）；Luna r1 发布两份 N 报告，分别是守卫缺失（S5，W2）与返回触发不匹配（S3，W2）。两项台账在四模型 Full 中三轮全命中、no-inspect 三轮全未命中。带触发的初始边是典型的确定性结构事实，可观察的现象是缺少该事实时四个模型都没有把它作为缺陷提出。[clm-case-initial]

**案例三：泵控子态不可达在 Qwen、Muse 的无检视条件下反而更常命中。** pair `0002` 的 NL 第 2 至 5 句点名 `PumpControl` 下的三个子态 `PumpState`、`WaterState`、`MethaneState`；作者 STM 第 5 行 `[*] --> InitialState` 让复合态的初始边进入一个未另行声明的 `InitialState`，三个子态各有局部初始边，但没有任何从 `PumpControl` 层进入它们的迁移。台账 `EIS-0002-02`（L2，unreachable）记录三个子态不可达。Full 的 Qwen 三轮均未命中，Muse 命中 r1、r2；no-inspect 的 Qwen 在 r2、r3 以 S2 谓词报告 “No transition from PumpState to WaterState exists in the closed model” 等命中，Muse 三轮以 “Missing PumpControl to WaterState transition” 等命中。这里普通语义路径直接从 NL 点名的子态出发核对迁移存在性，并由 S2 执行给出 W2 证据；它与表 6 中不可达类在 Qwen、Luna 上不降的结果一致，说明并非所有拓扑类问题都依赖检视事实。作者制品用 `--` 分隔的区结构涉及并发语义，不在本方法的断言对象内，本例只用于说明命中来源，不对区语义作任何判断。[clm-case-unreachable]

## 6. 精度与稳健性

strict 口径只把有效且外部 D1/D2 的报告计入分子，分母不变；主口径仍按原冻结协议，不用 strict 替换。三个新模型的 strict precision 差值为 −2.49、−5.78、+0.59 pp，Luna 为 +2.31 pp；strict hit@1 与普通 hit@1 同向下降 19.77、22.76、16.55 pp。有效 D0 报告在 Sonnet 从 69 变为 30，Muse 从 61 变为 32，Qwen 从 74 变为 28，因此普通 precision 的下降包含有效 D0 组成的变化，不能直接解释为所有证据强度下都变差；覆盖差异不依赖把 D0 计为有效这一点。[clm-main] [clm-ci]

表 8：九个 NL 簇的配对 bootstrap 95% 百分位区间，差值为 no-inspect 减 Full，单位 pp；seed 20260906，10000 次，保留簇内全部制品与轮次。前五列复用 A1 的 `compare`，后两列为同一重采样方案对 strict 口径的扩展。[clm-ci] [src-code]

| 模型 | Δhit@1 | Δhit@3 | Δhit@all | ΔL2 hit@1 | Δprecision | Δstrict precision | Δstrict hit@1 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Claude Sonnet 5 | [−31.63, −13.04] | [−25.58, −9.09] | [−39.42, −14.79] | [−69.17, −30.86] | [−7.69, −2.66] | [−6.83, +2.48] | [−29.08, −12.20] |
| Muse Glimmer-30B | [−30.95, −19.17] | [−28.00, −13.85] | [−33.98, −18.38] | [−68.25, −23.15] | [−15.02, −1.42] | [−14.11, +1.88] | [−29.08, −16.67] |
| Qwen3.8-27B | [−26.44, −6.98] | [−28.21, −4.52] | [−32.12, −6.88] | [−65.43, −3.14] | [−9.31, +1.27] | [−4.09, +4.94] | [−24.65, −8.39] |
| gpt-5.6-luna（A1 归档） | [−36.00, −9.22] | [−43.64, −13.85] | [−26.23, −2.07] | [−84.13, −14.07] | [−11.80, +3.29] | 归档未含 | 归档未含 |

表 9：逐簇差值与留一簇敏感性。[clm-ci]

| 模型 | 逐簇 Δhit@1 为负的簇数 | 逐簇 Δhit@1 范围 | 留一簇 Δhit@1 范围 | 留一簇 Δprecision 范围 |
| --- | --- | --- | --- | --- |
| Claude Sonnet 5 | 9/9 | [−75.00, −2.22] | [−23.39, −18.25] | [−5.72, −4.19] |
| Muse Glimmer-30B | 8/9 | [−46.15, 0.00] | [−25.66, −22.47] | [−10.59, −5.87] |
| Qwen3.8-27B | 8/9 | [−33.33, +2.15] | [−21.35, −13.73] | [−4.92, −1.89] |

覆盖下降的方向比精度下降更一致：三模型 hit@1、hit@3、hit@all、L2 hit@1 和 strict hit@1 的区间全部不跨零，逐簇差值仅 Muse、Qwen 各有一簇为零或略升，留一簇后 Δhit@1 仍全部为负。精度上 Sonnet、Muse 的普通 precision 区间不跨零，Qwen 跨零；三模型 strict precision 区间全部跨零。Qwen 留一簇 Δprecision 全部为负而 bootstrap 区间跨零，说明只有 9 个簇时区间对簇权重敏感，不宜给出确定方向。区间只反映这九簇组成的敏感性，不消除历史运行差异；未计算 p 值或多重检验校正，不补造。[clm-ci] [clm-limits]

## 7. 历史偏离与可解释边界

1. **对照不是同批运行。** Full 来自 2026-09-07 至 09-08 的 E2，本次 no-inspect 于 09-11 运行，方法源码相隔多次提交，judge 通道由 sub2api 换为 aizzz，并发由 16 换为 24。差值不能全归因于检视事实。[clm-limits]
2. **provider 故障与恢复如实保留。** Qwen 5 格隔离恢复、Muse 1 格 judge 重采样、Sonnet 一次整 run 排除、两次隧道中断，处置均在事前登记口径内，逐条见 INCIDENTS.md；不能写成“零重试、零故障”。[src-incidents]
3. **自动 judge 有具体误读风险。** 三模型合计 1938 份有效性仲裁凭证，本次新增人工确认为 0；Muse 0059 r3 的第二读在一个报告上连续六轮坚持校验器拒绝的组合，暴露评审端 prompt 对该互斥关系引导不足，已登记为待修。[clm-eval] [clm-limits]
4. **Sonnet 的 40 格带 d_adjudication 诊断。** 内部 D 结构化输出及其一次定向修复未闭合全部义务，剩余单元保留为未解决；这些格全部 eligible 并进入统计，E2 Full 的 Sonnet 也有 51 格同类诊断。[clm-sources]
5. **A1 原登记的 Luna 匹配 full 与本次无关。** Luna 的对照沿用 A1 归档口径（v61 Full），未为本次新增任何 Luna 运行。[src-a1]

## 8. 统计解释自检

| 检查 | 本次处理 |
| --- | --- |
| Simpson 聚合反转 | 检查层级与九簇；L1 的模型间方向不一与各簇异质性均公开 |
| 生态谬误 | 不把簇级差值推出单个制品必然变化 |
| Berkson 选择偏差 | 54 pair 固定，不声称代表所有状态机总体 |
| Collider 条件化 | 不按后验成功率、有效率或报告量筛格 |
| 基率忽略 | 145 台账、各层分母、全部报告数同时保留 |
| 向均值回归 | 非按极端质量选样；披露历史非同期对照 |
| 幸存者偏差 | 486 格全判、所有报告纳入；失败尝试与恢复历史不隐去 |
| 多重搜索效应 | 全部登记主指标和方向都报告，不据区间跨零与否筛结论 |
| 分析路径自由度 | 指标算术复用 A1 分析器；strict 口径不替换主口径 |
| 相关误当因果 | 案例与内容分层和总差值分开；不作纯单因素贡献率 |
| 反向因果 | 开关先于生成和 judge；预期不作为完成或重跑门 |

整体解释等级为 CAUTION：计数与区间为机械可复算事实，机制解释为与计数相容的推断。[clm-limits]

## 9. 结论

事前 H1 预期覆盖与 L2 下降：三个新模型的 hit@1、hit@3、hit@all、L2 hit@1 与 strict hit@1 全部下降且九簇区间不跨零，逐轮 9/9 组同向，与 Luna A1 的方向一致。H1 获得四模型一致的支持。H2 预期 L0/L1 变化小于 L2：四模型 L2 下降 26.50 至 46.15 pp，L0 下降 16.90 至 22.07 pp，L1 在 −9.52 至 +4.76 pp 之间，与预期相符。H3 不预设精确率方向：普通 precision 在 Sonnet、Muse 上区间不跨零地下降，在 Qwen、Luna 上跨零，strict precision 三个新模型区间全部跨零。[clm-main] [clm-coverage] [clm-ci]

学术上应写为：**在四个固定模型配置、同一批 54 个输入对与三轮重复上，关闭检视事实一致减少固定台账的覆盖，损失集中在行为层与依赖结构事实的台账类，报告有效比例的变化依模型而异。** 不应写成“四模型精度统一下降”，也不应写成“检视事实是行为覆盖的唯一来源”，因为 no-inspect 在不可达类与部分效果、状态类条目上仍有命中甚至增益。这支持 C-1 的贡献从“在 gpt-5.6-luna 上”升为四配置的方向一致性；是否据此改写 RQ3、C-1 与摘要由 O2 线程裁定，本报告不改论文正文。[clm-main] [clm-content] [clm-limits]

## 审计附录：证据链与事实源

### A.1 来源考据表

| source path | source creation commit | prefix commit | substantive fact commit 判定理由 | non-prefix revision/migration commit | canonical machine source |
| --- | --- | --- | --- | --- | --- |
| 本报告 | 本文件首次提交，见 `[cmd-history]` | 同首次提交；2026-09-12 10:17:38 CST 冻结 | 首次整合三模型 no-inspect 与 Luna A1 的四模型对照 | 无迁移 | 下列 results |
| `final_results/a1_ext_20260911/results.json` | 与本报告同一 PR 首次提交 | 不适用 | 三模型两臂冻结标签、配对比较与 strict 扩展 | 本报告未修改 | [results][src-results] |
| `final_results/a1_no_inspect_vs_v61_20260906/results.json` | `de60df54e` | 不适用 | Luna A1 与 v61 冻结标签 | 本报告未修改，只读引用 | [A1 results][src-a1] |

### A.2 上游事实源清单

| 引用键 | 事实源 | 类型 | 用途 | 关键锚点 |
| --- | --- | --- | --- | --- |
| [src-prereg] | [事前登记](../discover_matrix/docs/generations/a1_ext_20260911/preregistered.md) | md | 干预、假设、身份、并发、失败处理 | §1 至 §5 |
| [src-results] | [results.json](../final_results/a1_ext_20260911/results.json) | json | 三模型两臂逐报告标签、metrics、per_round、content、funnel、call_audit、judge_runs、comparison | `/models/{sonnet,muse,qwen}/{a1ext,full,comparison}` |
| [src-source] | [source_manifest.json](../final_results/a1_ext_20260911/source_manifest.json) | json | method run manifest、恢复 run、judge_source MANIFEST、原件 hash 与排除项 | `/method_runs`、`/isolated_recovery_runs`、`/raw_index` |
| [src-incidents] | [INCIDENTS.md](../final_results/a1_ext_20260911/INCIDENTS.md)、[RUN_RECORD.md](../final_results/a1_ext_20260911/RUN_RECORD.md) | md | 事故 I-1 至 I-7 与 run 清单 | 全文 |
| [src-e2] | [E2 入口](../final_results/e2_20260907/README.md)、各模型 `cells.json` | md/json | 同模型 Full ours 报告、候选与源提交 | `cells[arm=ours]` |
| [src-a1] | [A1 归档](../final_results/a1_no_inspect_vs_v61_20260906/README.md) | md/json | Luna 四模型对照行与其 CI | `/a1`、`/v61`、`/comparison` |
| [src-ledger] | [ledger.json](../discover_matrix/ledger_v2/ledger.json) | json | 145 条分母、L 与轴 | `/items/*/{pair,L,axes,pair_context}` |
| [src-inputs] | [0004](../selected_seed_examples/llms_emp_feedback_final_0004/nl.txt)、[0040](../selected_seed_examples/llms_emp_feedback_final_0040/nl.txt)、[0002](../selected_seed_examples/llms_emp_feedback_final_0002/nl.txt) 的 NL 与同目录 `stm0.puml` | txt/puml | 三个案例的作者源 | 见 A.4 hash |
| [src-code] | [a1ext_common.py](../discover_matrix/docs/generations/a1_ext_20260911/a1ext_common.py)、[analyze_a1_ext.py](../discover_matrix/docs/generations/a1_ext_20260911/analyze_a1_ext.py)、[analyze_a1.py](../discover_matrix/docs/generations/a1_no_inspect_20260906/analyze_a1.py) | source-code | 指标算术、校验与表格导出 | `calculate`、`compare`、`strict_cluster_bootstrap`、`tables` |

### A.3 Claim-evidence map

| 引用键 | claim | 类型 | 上游事实源与锚点 | 复验命令 | 置信度 | 限制 |
| --- | --- | --- | --- | --- | --- | --- |
| <a id="clm-design"></a>[clm-design] | no-inspect 关闭检视事实链、保留 FCSTM/谓词/发布/外部 judge | classification | [src-prereg] §2；A1 协议 | 人工对照 | high | 组合干预，非等预算 |
| <a id="clm-sources"></a>[clm-sources] | 486 格 method、486 格 judge 闭合；恢复与排除项 | trace | [src-source]、[src-incidents]、[src-results] coverage | [cmd-verify] | high | 原件仅本地 |
| <a id="clm-eval"></a>[clm-eval] | 两读加仲裁、K/N/I、strict、hit 定义 | classification | [src-prereg] §2；[src-code] | [cmd-verify] | high | 自动标签，人工确认 0 |
| <a id="clm-main"></a>[clm-main] | 表 1、表 2 与四模型合计 | count | [src-results] metrics | [cmd-tables] | high | 三轮 pooled；计数差非语义迁移 |
| <a id="clm-rounds"></a>[clm-rounds] | 表 3 与 12/12 同向 | count | [src-results] per_round | [cmd-tables] | high | 轮次相关 |
| <a id="clm-coverage"></a>[clm-coverage] | 表 4、表 5 | count | [src-results] metrics.tiers、comparison.lost/gained | [cmd-tables] | high | 集合键为 ID×轮次 |
| <a id="clm-content"></a>[clm-content] | 表 6 各类命中变化 | count / 解释 medium | [src-results] content；[src-ledger] axes | [cmd-tables] | high（计数） | 探索性，无校正 |
| <a id="clm-funnel"></a>[clm-funnel] | 表 7 候选与 W 组成 | count | [src-results] funnel | [cmd-tables] | high | 组成变化，非因果 |
| <a id="clm-case-deadend"></a>[clm-case-deadend] | 0004 两死端四模型 Full 3/3、no-inspect 0/3 | trace | [src-results] reports；[src-inputs] 0004 | [cmd-cases] | high（样例） | 不分辨缺失环节 |
| <a id="clm-case-initial"></a>[clm-case-initial] | 0040 两带触发初始边四模型 Full 3/3、no-inspect 0/3 | trace | 同上；[src-inputs] 0040 | [cmd-cases] | high（样例） | 同上 |
| <a id="clm-case-unreachable"></a>[clm-case-unreachable] | 0002 不可达在 Qwen/Muse no-inspect 命中更多 | trace | 同上；[src-inputs] 0002 | [cmd-cases] | high（样例） | 区语义不作判断 |
| <a id="clm-baseline"></a>[clm-baseline] | no-inspect 对 E2 基线的 hit@1 与 L2 hit@1 | count（事后） | [src-e2] `cells[arm=baseline]`；[src-code] `calculate` | [cmd-baseline] | high（计数）/ 事后 | 未事前登记；历史批次 |
| <a id="clm-ci"></a>[clm-ci] | 表 8、表 9 区间与方向 | count/risk | [src-results] comparison | [cmd-verify] [cmd-tables] | high | 九簇，无 p 值 |
| <a id="clm-limits"></a>[clm-limits] | 历史配置、provider、judge 与组合干预边界 | risk | [src-prereg]、[src-e2]、[src-incidents] | 人工对照 | medium | 不削弱冻结计数 |

### A.4 复验命令

均从仓库根执行，无 provider 调用。

<a id="cmd-verify"></a>**[cmd-verify]：归档 hash、闭合与全部指标复算**

```bash
python project_1_llm_state_machine_modeling/paper_stm_issue_discover/discover_matrix/docs/generations/a1_ext_20260911/analyze_a1_ext.py
python -m pytest -q project_1_llm_state_machine_modeling/paper_stm_issue_discover/discover_matrix/docs/generations/a1_ext_20260911/test_analyze_a1_ext.py
```

<a id="cmd-tables"></a>**[cmd-tables]：本文表 1 至表 9 与运行审计表**

```bash
python project_1_llm_state_machine_modeling/paper_stm_issue_discover/discover_matrix/docs/generations/a1_ext_20260911/analyze_a1_ext.py --tables
```

<a id="cmd-cases"></a>**[cmd-cases]：三个案例的全格报告与命中**

```python
import json
from pathlib import Path
p = Path('project_1_llm_state_machine_modeling/paper_stm_issue_discover')
d = json.loads((p / 'final_results/a1_ext_20260911/results.json').read_text())
luna = json.loads((p / 'final_results/a1_no_inspect_vs_v61_20260906/results.json').read_text())
cases = [('sonnet', '0004', 1, ['INS-0004-01', 'INS-0004-02']), ('muse', '0004', 1, ['INS-0004-01', 'INS-0004-02']),
         ('qwen', '0040', 1, ['VU-0040-01', 'EIS-0040-03']), ('luna', '0040', 1, ['VU-0040-01', 'EIS-0040-03']),
         ('qwen', '0002', 2, ['EIS-0002-02']), ('muse', '0002', 2, ['EIS-0002-02'])]
for model, pair, rnd, ids in cases:
    for arm in ('full', 'a1ext'):
        src = (luna['v61'] if arm == 'full' else luna['a1'])['reports'] if model == 'luna' else d['models'][model][arm]['reports']
        rows = [r for r in src if r['pair_id'] == pair and r['round'] == rnd]
        hits = sorted({e for r in rows if r['validity'] == 'VALID_KNOWN' for e in r['full_ledger_ids'] if e in ids})
        print(model, pair, rnd, arm, len(rows), 'reports; hits', hits)
        for r in rows:
            print('  ', r['original_report_id'], r['validity'], r['d_tier'], r['full_ledger_ids'], r.get('predicate_id'), r.get('witness_level'), (r.get('title') or r['reason'])[:100])
```

案例作者源 SHA-256（`sha256sum` 于 `selected_seed_examples/llms_emp_feedback_final_<pair>/`）：

| pair | nl.txt | stm0.puml |
| --- | --- | --- |
| 0004 | `3110cbcf15bfb507f0326965970888eada5541b791b5fa661698dfc74e82c2ce` | `188bebba5631b87c315e966d8cd0f993630182d74f9b9bd677e1452198e458cb` |
| 0040 | `f1c3dc88371b8256352e7ab6ee7eb42424de6e11dfde70d185f224dd1d05a7a8` | `7a96af160f5a1c2a7e4ee172c5bdb24ea8008542b6be9fba5a5d5d77ae28a7e4` |
| 0002 | `a391765dba935d89e6d2467c97b218c0136d106ea9c00bac91e6525e28ac04f1` | `3a8e81a4a5a1e54e3994af300fcbd1913073547b8069288bbe57e61d989c3d43` |

<a id="cmd-baseline"></a>**[cmd-baseline]：E2 基线臂与 ours 臂的 hit@1、L2 hit@1 重算**

```python
import json, sys
sys.path.insert(0, 'project_1_llm_state_machine_modeling/paper_stm_issue_discover/discover_matrix/docs/generations/a1_ext_20260911')
from a1ext_common import calculate, ledger_items
items = ledger_items()
for model in ('sonnet', 'muse', 'qwen'):
    cells = json.load(open(f'project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/e2_20260907/{model}/cells.json'))['cells']
    for arm in ('baseline', 'ours'):
        reports = [{**r, 'pair_id': c['pair'], 'round': int(c['round'])} for c in cells if c['arm'] == arm for r in c['reports']]
        m = calculate(reports, items)
        print(model, arm, m['hit1'], m['tiers']['L2']['hit1'], m['precision'])
```

<a id="cmd-history"></a>**[cmd-history]：冻结与后续修改考据**

```bash
git log --follow --date=iso -- project_1_llm_state_machine_modeling/paper_stm_issue_discover/reports/2026-09-12-10-17-38-a1-ext-three-model-no-inspect-results.md
```

**运行原件边界。** 方法与 judge 的原始 prompt、响应流、usage 与恢复工具只保存在 gitignored `runs/paper1/a1_ext_20260911/`，`source_manifest.json` 记录其 975 个原件的 SHA-256；公开归档足以复算全部冻结标签的算术，但 fresh clone 不能重放私有请求。费用只保存声明费率与用量口径，不推算未记录费用。

[src-prereg]: ../discover_matrix/docs/generations/a1_ext_20260911/preregistered.md
[src-results]: ../final_results/a1_ext_20260911/results.json
[src-source]: ../final_results/a1_ext_20260911/source_manifest.json
[src-incidents]: ../final_results/a1_ext_20260911/INCIDENTS.md
[src-e2]: ../final_results/e2_20260907/README.md
[src-a1]: ../final_results/a1_no_inspect_vs_v61_20260906/README.md
[src-ledger]: ../discover_matrix/ledger_v2/ledger.json
[src-inputs]: ../selected_seed_examples/README.md
[src-code]: ../discover_matrix/docs/generations/a1_ext_20260911/analyze_a1_ext.py
[clm-design]: #clm-design
[clm-sources]: #clm-sources
[clm-eval]: #clm-eval
[clm-main]: #clm-main
[clm-rounds]: #clm-rounds
[clm-coverage]: #clm-coverage
[clm-content]: #clm-content
[clm-funnel]: #clm-funnel
[clm-case-deadend]: #clm-case-deadend
[clm-case-initial]: #clm-case-initial
[clm-case-unreachable]: #clm-case-unreachable
[clm-baseline]: #clm-baseline
[clm-ci]: #clm-ci
[clm-limits]: #clm-limits
[cmd-verify]: #cmd-verify
[cmd-tables]: #cmd-tables
[cmd-cases]: #cmd-cases
[cmd-baseline]: #cmd-baseline
[cmd-history]: #cmd-history
