# 全量运行：v3.11（第六轮配置）对两侧全部报告（代码提交 `3a1ba5cf1`，2026-09-03 18:56 – 09-04 01:10）

按用户裁定，代码恢复到第六轮配置（prompt v11；relation-first 且 FULL 或 PARTIAL 都把非 FALSE_POSITIVE 报告闭合为 K；任一读数分歧仲裁；闭包 full；仅叠加三项不改语义的确定性归一化），对 v60 current 的 1271 条报告与 X1v2 baseline 的 512 条报告各跑三轮，共 324 个 pair-轮，**0 格失败**。不触碰 `final_results/` 的任何冻结数据；原始制品在被忽略的 `runs/paper1/judge-full-3a1ba5cf1-iter6cfg/`。中途网关返回 Cloudflare 502（22:52–23:21），停机后按缺失格以 `-resume` run-id 补跑，无重复无遗漏。provider 成本 $37.33，2097 次调用（每条报告 1.18 次，批次摊薄生效），每条报告 11.2 万输入 token，86% 的报告经 validity 仲裁，原地修复轮次率 18%。

对比脚本 [compare_full_run.py](../../scripts/compare_full_run.py) 用同一算法从人工的 FULL 关联复算 hit：人工侧得到 310/435 与 227/435，与冻结报告一致，自检通过。逐报告结果在 `current_all_reports.tsv` / `baseline_all_reports.tsv`，分歧台账在 `*_disagreements.tsv`。

## 论文口径下的真实数字

| 侧 | 指标 | judge | 人工终稿 |
| :-- | :-- | --: | --: |
| ours（1271） | K / N / I | 628 / 277 / 366 | 749 / 231 / 291 |
| | report precision | 71.2% | 77.1% |
| | hit@1 FULL（435 单位） | 292 = 67.1% | 310 = 71.3% |
| | hit@3 / hit@all（145 条目） | 119 / 75 | 119 / 86 |
| | 逐报告 K/N/I 一致率 | 957/1271 = 75.3% | — |
| baseline（512） | K / N / I | 293 / 134 / 85 | 312 / 105 / 95 |
| | report precision | 83.4% | 81.4% |
| | hit@1 FULL（435 单位） | 225 = 51.7% | 227 = 52.2% |
| | hit@3 / hit@all | 105 / 47 | 106 / 46 |
| | 逐报告 K/N/I 一致率 | 388/512 = 75.8% | — |

| 差距（ours − baseline） | judge | 人工终稿 |
| :-- | --: | --: |
| hit@1 | **+15.4 pp** | +19.1 pp |
| hit@3 | +14 条目 | +13 条目 |
| hit@all | +28 条目 | +40 条目 |
| report precision | **−12.2 pp** | −4.3 pp |

baseline 侧 judge 与人工几乎重合（hit 差 2 个单位，precision 差 2 pp）；ours 侧 judge 少 121 个 K、多 75 个 I，precision 低 6 pp，hit@1 低 4 pp。差距的故事方向不变（ours 覆盖高、precision 低），但 precision 缺口被放大到三倍。

## 分歧的结构

ours 314 条分歧：N→I/D0 58、K→I/FALSE_POSITIVE 41、K→I/D0 38、I→N/D1 37、K→N/D2 33、K→N/D1 30、I→N/D2 24、K→I/NADC 11、其余 42。baseline 124 条：I→N 36（D2 18、D1 18）、K→N 27、N→I/D0 16、K→I 16（D0 11、FP 5）、N→K 12、I→K 10。

### ours：分歧几乎全部落在「用派生表示说话」的报告上

按报告文本是否含派生表示词（route token、`guard=null`、`triggers=[]`、closed model、运行时场景、inventory、carrier 等）切分（[current_derived_phrasing.md](./current_derived_phrasing.md)）：

| 人工类别 | 措辞 | n | judge K | judge N | judge I（其中 FP / D0） |
| :-- | :-- | --: | --: | --: | --: |
| K | 派生 | 433 | 309（71%） | 50 | 74（40 / 29） |
| K | 作者源 | 316 | 287（**91%**） | 13 | 16（1 / 9） |
| N | 派生 | 211 | 10 | 133 | 68（8 / 58） |
| N | 作者源 | 20 | 0 | **20** | 0 |
| I | 派生 | 269 | 18 | 54 | 197 |
| I | 作者源 | 22 | 4 | 7 | 11 |

作者源措辞的报告上 judge 与人工高度一致（K 保 91%、N 保 100%）；全部系统性分歧集中在派生措辞的 644 条上。典型形态：报告说「UrbanMode 的初始进入是条件的，`guard='R45RouteToken == 12'`」，作者 PlantUML 里是一条普通带标签迁移、守卫只存在于降低表示；judge 按 v11 的作者源原则判 FALSE_POSITIVE，人工透过措辞读到台账里的源级关切（EIS-0029-04）并保留为 K 且 FULL。

### ours：守卫载体族在 gold 里没有统一口径

ours 最大的报告族是谓词驱动的「X 到 Y omits its required guard，观察到 guard=null」，作者源里是事件名标签。judge 对这一族只用一条规则（事件名标签 → D0；布尔表达式标签 → D1）。人工 gold 对同一形态给出了四种等级：0029:r2:15、0049:r3:11、0034:r3:13 判 D1/N；0034:r3:14、0034:r2:22 判 D2/K 并 FULL 到 EIS-0034-02；0044:r3:8、0044:r3:11、0044:r2:1 判 D0/I；0059:r2:9 判 A0/I。同一 pair 0034 内部 D1 与 D2 并存。这一族贡献了 N→I/D0 的 58 行、K→I/D0 的大部分与 I→N 的大部分。

### ours：relation 漏匹配压低 hit

K→N 63 行是 judge 判有效但 NO_MATCH、人工给 FULL 或 PARTIAL：0037:r2:0（正交区域结构，人工 FULL 到 EIS-0037-01）、0019:r1:5（消费者不可达，FULL 到 INS-0019-01）、0053:r3:2（缺 WaterState→MethaneState 迁移，FULL 到 DIFF-0053-01 与 INS-0053-02）。报告与台账条目描述同一缺陷的不同粒度或不同 facet；第六轮那版收紧的 relation（同 locus 同义务才 FULL）判 NO。hit@1 少的 18 个单位与 hit@all 少的 11 个条目主要来自这里；第九轮放宽 PARTIAL 又会把 gold N 大批升 K，两边都不贴人工。

### baseline：人工终审比两条人工轨道都严

baseline 的非 K 重审记录了两条人工轨道的提案（[baseline_tracks_alignment.md](./baseline_tracks_alignment.md)，123 行）：judge 与终审 pane5 的有效/无效一致率 62.6%，与 Track A 69.9%、Track B 67.5%；两轨彼此只有 56.9% 一致；两轨都判有效的 65 行里 pane5 改判无效 21 行，judge 在其中 15 行站轨道一边；pane5 判 D0 51 行，两轨分别 19 与 28。终审把 baseline 的 D1 压成 D0 的倾向，使 baseline 人工 N 偏少、I 偏多；judge 与轨道一致地多判 N，于是 baseline 的 judge precision 反而比人工高 2 pp。

## 两侧 gold 的产生结构不同

baseline gold 是 pane5 在两条彼此分歧的轨道之上终裁；current gold（v4 复审）是 pane5 加一条盲提案的两人链，1271 行里只有 5 行标记分歧且全部沿用此前 pane5 的结论。两侧宽严不同的两处——对 ours 派生措辞的宽容读法、对 baseline D1 的严格压缩——方向都对 ours 有利；judge 用同一规则读两侧时把两处都往回拉了一部分，结果是 hit 差距从 +19.1 缩到 +15.4、precision 差距从 −4.3 扩到 −12.2。

## 效率

1783 条报告、2097 次调用、$37.33；每条报告 1.18 次调用、$0.021、11.2 万输入 token；两侧串行三轮的有效墙钟约 5 小时（不含停机），current 侧一轮约 2 小时 20 分，baseline 一轮约 43 分钟。运行纪律：14 个 pair 在途；网关 502 时按 pid 停 CLI、探针恢复后按缺失格补跑。

## 费用与时长调查（2026-09-04 补）

**费用没有变贵。** 冻结 v3.2 当年跑全量：current 1374 次调用 $39.78（每条报告 $0.031、11.6 万输入 token），baseline 702 次调用 $10.79，合计 **$50.57**；本次 2097 次调用 **$37.33**（每条 $0.021），便宜 26%。「一轮不到 10 刀」对应的是 baseline 单侧（$10.79）或 300 条校准子集的一轮（约 $8）。

**慢在 current 侧的调用形态**，不在网关：

| 侧 / 阶段 | 调用 | 输入 token / 次 | 输出 token / 次 | 平均时长 | 费用占比 |
| :-- | --: | --: | --: | --: | --: |
| current validity 主读 | 564 | 7.7 万 | 8.6 千 | 177 s | 27.5% |
| current validity 仲裁 | 271 | 13.0 万 | 7.6 千 | 164 s | 24.6% |
| current relation 主读 | 416 | 15.2 万 | 5.0 千 | 110 s | 21.0% |
| current relation 仲裁 | 99 | 9.6 万 | 2.7 千 | 61 s | 5.0% |
| baseline 四阶段 | 747 | 4.6–8.8 万 | 1.8–2.9 千 | 40–64 s | 21.9% |

单次时延由输出长度主导：一批 8 条报告的 validity 响应要写 8.6 千 token 的结构化审计，接近 3 分钟；一个 current pair 的链条约 8 次串行调用、20–25 分钟；8 个 worker 跑 54 个 pair 就是一轮 2.5 小时。冻结运行 current 用了 16 个 worker；本次为了和 baseline 同跑控制在 14 个 pair 在途只给了 8 个，再加 30 分钟网关 502 停机，总墙钟约 6 小时。

**可行的提速降本（按风险从低到高）**：① 类别级仲裁触发——仲裁占费用约 30%、86% 的报告都仲裁，离线核对 176 条同类仲裁只改 2 条类别，预计 −25% 费用与时间；② baseline 先跑完再让 current 独占 16 个 worker（冻结运行即如此，32 个在途请求未出事），墙钟 −40%；③ 从提示词里去掉纯溯源制品（source_trace 4.9 万字符、case_report 2.1 万、working_contract、smt / verify facts）而保留 NL、PlantUML、canonical IR、inspection facts，输入 −40–50%，需子集验一轮（比第八轮 B 臂的全砍温和）；④ 精简输出 schema（逐字段句子审计改逐报告摘要、限制 reason 长度），输出 −50% 直接换时延 −40%，但一致性校验依赖句子判定要重设计；⑤ 单读数，−40%，只适合非论文用途。①+②+③ 叠加，全量预计 $18–20、2–2.5 小时。
