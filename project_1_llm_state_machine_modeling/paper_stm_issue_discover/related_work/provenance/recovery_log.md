# 伪缺口与付费墙回收：⭐ 10 个目标 9 个取到全文

> ⭐ **它闭合的是 [coverage_audit.md](./coverage_audit.md) 里最damning的一条** —— ⛔ 「一部分自报『未见』其实是工具状态而不是文献状态」。⭐ 回收完成后，那条限制**已解除**（[methodology.md](./methodology.md) §6 局限 #5）。
>
> **档位标记**：全文为【实测】—— ⭐ 每条都有可复现的入口 URL、抽取命令与逐字片段。

## ⭐⭐ 两个伪缺口：**都是工具状态，⛔ 不是文献状态**

### 1 · Dwyer, Avrunin & Corbett, ICSE 1999 —— ⛔ 「需要 OCR」的诊断**本身是错的**

| 项 | 【实测】 |
| :-- | :-- |
| **可用入口** | `https://www.cs.colostate.edu/~france/CS614/Readings/Readings2011/PropPatterns2p411-dwyer.pdf` |
| **抽取** | `pdftotext -layout`，10 页 → **678 行**干净正文 |
| ⛔ **原诊断错在哪** | 该 PDF 是 **PDF 1.2（1999-05-24 创建）带完整文本层** —— ⛔ **不是 CCITT 扫描图，⛔ 不需要 OCR** |
| ⭐ **Table 1 三数核对** | ⭐ **85 / 119 / 555 全部正确**，逐字取自输出第 409 / 410 / 419 行 |

```
 Absence          41    5       12     18      9    85
 Universality    110              5     2      1   119
 Total          438     8      25     29      11 1 555
    Table 1: Totals for Patterns/Scopes (All Data)
```

⭐ 另取到两句可直接引的：「Of the 555 example specifications we collected, **511 (92%) matched one of our patterns**.」「In all, we collected 555 specifications from **at least 35** [different sources]」。

### 2 · Heimdahl & Leveson, IEEE TSE 22(6), 1996 —— ⭐ **路径 + 证书两个问题叠加的误判**

| 项 | 【实测】 |
| :-- | :-- |
| **可用入口** | `http://dslab.konkuk.ac.kr/Class/2012/12SIonSE/Key%20Papers/Completeness%20and%20consistency%20in%20hierarchical%20state-based%20requirements.pdf` —— ⭐ **必须 `curl -k`** |
| **抽取** | `pdftotext -layout`，15 页 → **1148 行** —— ⭐ **与另一路报告的 1148 行逐字吻合** |
| ⛔ **原诊断错在哪** | ⭐ 原报告试的是 **2011 年**那门课的路径（`Class/2011/11SMA/Team_project/Reference/...`，HTTP **401**）；⭐ 正确路径在 **2012 年**那门课下。⚠️ 「`KEY_USAGE_BIT_INCORRECT` 无法取全文」是**路径错 + 证书链**两个问题叠加，⛔ 而只归因给了后者 |

⭐ **它给出的两条可直接引的逐字**：

> 「Robustness with respect to a state-machine description implies the following: 1) **Every state must have a behavior (transition) defined for every possible input.** 2) The logical OR of the conditions on every transition out of any state **must form a tautology**. 3) Every state must have a software behavior (transition) defined in case there is no input for a given period of time (a timeout).」

> ⭐ 直接对应 `event_consumed`：「**If an event is generated but does not trigger any transition, it is likely that this event was generated in error or that transitions triggered by this event are missing from the requirements.**」

## ⭐ 付费墙回收：8 篇里 7 篇取到全文

| # | 论文 | 状态 | ⭐ 破局入口 | ⭐ 它补的谓词 |
| --: | :-- | :-- | :-- | :-- |
| 1 | **Heitmeyer, Jeffords & Labaw, ACM TOSEM 5(3), 1996** | ✅ 全文 **1891 行** | ⭐ CiteSeerX → **Wayback 快照**（NRL preprint，页眉自述将刊于 TOSEM 5(3):231-261） | `event_consumed` · `guard_distinguishable` —— ⭐ **A-7E OFP 真实工业数据**：「The mode transition tables together contain a total of **700 rows** … our tool found **57 Disjointness errors**」 |
| 2 | **Torre et al., UML 一致性规则** | ✅ 全文 ×2（TR 1605 行 + **博士论文 9022 行**） | ⭐ **Carleton Scholaris/DSpace** —— ⚠️ 原建议的 `squall.sce.carleton.ca` **已下线**（DNS 解析到 IP 但 80 端口 filtered，⭐ 这解释了前几路为什么卡住：**URL 是对的，服务器不在公网了**） | `reaches` · `state_declared` · `edge_declared` · `containment` · `initial_target` |
| 3 | **Autili et al., IEEE TSE 2015** | ✅ 全文 **1419 行** | ⭐⭐ **三大聚合器齐报 CLOSED 且三家都错了** —— 破局靠 **OpenAIRE API** 的 `originalId` 数组暴露了 `oai:zenodo.org:14573492`，⛔ 那是 Unpaywall / OpenAlex / Semantic Scholar 都丢掉的字段 | Dwyer 之后最被引的统一模式目录（⭐ 自陈「40 new or extended patterns」） |
| 4 | **Vu, Haxthausen & Peleska, SCP 133(2), 2017** | ✅ 全文 **1753 行** | ⭐ `orbit.dtu.dk` 被 Cloudflare 拦（`Just a moment...`，带 cookie jar / UA / Referer 重试 3 次全败）—— ⭐⭐ **换主机名到 `backend.orbit.dtu.dk/ws/files/<id>/<name>.pdf` 即通**，file ID 相同、无挑战 | `invariant`（互斥进路）· `persists_until`（sequential release）· `terminates`（进路释放） |
| 4b | ⭐ **Vu 的 DTU 博士论文（299 页 / 13126 行）** | ✅ 全文 | 同上 | ⭐ **比论文更适用** —— 带编号的安全不变式目录 `SI-R-1..7` + guard/update 形式的 `SR-*` / `RR-*` 规则。⭐ 逐字一例：「**SI-R-5** Two routes that share the last section **must not** be occupied at the same time」+ 形式化 |
| 5 | **Bögli et al., FormaliSE 2025** | ✅ 全文 **852 行** + ⭐ **原始数据集** | ⭐ 唯一通路是 **Wayback 的 `2id_` 原样回放**（⛔ 作者站从本机 `SSL_ERROR_SYSCALL` ×5；⛔ BORIS 机构库是 Anubis 挑战，且 OpenAlex 确认该记录**本就没有 PDF**） | `invariant` —— ⭐ **89 条 SpaceWire 需求中 32 条天然 INV**，⭐⭐ 且该数字**由三条独立路径互证**：正文 · Fig. 2 轴标 · **从 `data/spacewire.json` 机器重算**（INV 32 / LTL 39 / MTLb 15 / STL 3，和 = 89 ✓） |
| 6 | **Lange & Chaudron 一系** | ✅ 全文 ×5（含博士论文 7886 行） | TU/e `pure.tue.nl`（⚠️ `research.tue.nl/files/...` 是 Cloudflare 403，`repository.tue.nl` 是 503）+ Wayback | `state_declared` · `edge_declared` —— ⭐ **工业 UML 模型缺元素的唯一实证频次线**。⭐ Table 4.2（16 个工业模型）：`CnCD 0.0%–76.2%（均 16.3%）` · `CnSD 30.2%–98.4%（均 60.3%）` · `MnSD 8.7%–78.5%（均 51.0%）`；⭐ EASE04 逐字「it is **alarming** that for most rules the results are tremendously high」 |
| 7 | **Salsa, ASE 2001** | ✅ 全文 **344 行** | `http://www.cs.umd.edu/~rance/publications/papers/ase01.pdf` | `guard_distinguishable` —— ⭐ **教科书级例子**逐字：「If the diagram is in state A, then it may evolve to state B if `x ≤ 4` and it may evolve to C if `x ≥ 4`. Note that in the case when `x = 4` the successor of A could be **either B or C**.」⭐ Ford 动力总成真实数据（KOER：238 条不变式 / 11 条失败；OTM dead code 100/6），⭐ 且逐字「Neither the piece of dead code nor the redundant update that we detected with Salsa **had been found during a rigorous but manual review process by Ford engineers**」 |
| 8 | ⛔ **Lange, Chaudron & Muskens, IEEE Software 2006** | ⛔ **未取到** | ⛔ 8 条入口全败（Unpaywall `is_oa: false` · Semantic Scholar `CLOSED` · IEEE Xplore 直链 HTTP 202 返 0 字节 · TU/e 5 个页面无 deposit · `repository.tue.nl` 503 · Chaudron 主页 Wayback CDX 两轮扫无该文 · ProQuest 付费墙）—— ⭐ 作者从未自存档 | ⭐ **实质不构成缺口**：其内容与已取全文的博士论文 §2.2 + Ch.4 重叠 |

## ⛔⛔ 三处元数据被证伪 —— ⭐ 必须回写，⛔ 不得沿用

⚠️ 这三处都是**我在派活时或 C3 报告里写错的**，⭐ 取件方逐条核实后更正：

| # | ⛔ 原说法 | ⭐ 核实后的事实 | ⛔ 后果 |
| --: | :-- | :-- | :-- |
| 1 | 「**Automated validation of software models**, ASE 2001（Salsa）」，作者含糊，⚠️ 我在派活表里把它排在 Heimdahl / Heitmeyer 一带 | ⭐ **作者是 Steve Sims, Rance Cleaveland, Ken Butts, Scott Ranville**（Reactive Systems + **Ford Motor Company** + New Eagle），⛔ **既不是 Heimdahl 也不是 Heitmeyer**（DBLP `conf/kbse/SimsCBR01`） | ⛔ 引用时若沿用错误作者，⚠️ 审稿人一查即破 |
| 2 | C3 报告：「**Torre et al., JSS 2018**（含 **687→119** 条一致性规则 + **106 位专家验证**）」 | ⛔ **这是把三篇论文的事实混成了一篇**：⭐ TR SCE-15-01 是 **603→116**；⭐ **687→119 在博士论文 / JSS 2018**；⭐ **106 位专家在 SQJ 2022 那支，且验的是 116 条**（逐字：「106 respondents completed the questionnaire, resulting in a response rate of 23.3%」）。⭐ **只有博士论文把三者统一** | ⛔ 引用时必须按篇分开说，⛔ 不得写成「JSS 2018 含 687→119 + 106 专家」 |
| 3 | 我在派活表里写：「Bögli et al., FormaliSE 2025（89 条 SpaceWire 需求中 32 条天然 INV）」，⛔ 未给标题 | ⭐ **真实标题是 "Temporal Logics Meet Real-World Software Requirements: A Reality Check"**（Bögli, Rohani, Studer, Tsigkanos, Kehrer；Bern + Athens） | ⭐ 数字 89/32 **经三路互证成立**，⛔ 但标题必须用真的 |

⭐⭐ **这三条的共同教训**：⛔ **我在派活时写的「论文简称 + 它能补什么」本身就是未经核实的转述** —— ⚠️ 取件方按它去找，⛔ 若不独立核对作者与标题，错误就会原样进证据表。⭐ 本轮取件方**主动核了 DBLP 并更正**，⛔ 这不是它的义务，⭐ 而是它做对的地方。

## ⭐ 三条对后续可复用的取件结论

1. ⛔ **三大聚合器（Unpaywall / OpenAlex / Semantic Scholar）齐报 `CLOSED` 不等于没有开放版。** ⚠️ Autili 那条它们**集体错了** —— ⭐ **OpenAIRE API** 的 `originalId` 数组找到了开放的 Zenodo 副本。⭐ 而「作者机构库」这条路本轮**再次被验证**：Carleton Scholaris 取到 Torre（TR + 博士论文）· TU/e `pure` 取到 Lange 博士论文 · **`backend.orbit.dtu.dk`** 取到两份铁路件。
2. ⛔ **下载后必须 `file` + `pdfinfo` 双查。** ⚠️ 本轮抓到**两类伪 PDF**：DTIC 全站宕机时返回的 **1408 字节维护页**（HTTP 200，`.pdf` 后缀，⭐ 搜索引擎仍把它当有效 PDF 推荐）· Zenodo 的 **763 字节反爬页**。⚠️ 另：`file` 对线性化 PDF 的页数不可靠（把 299 页的博士论文报成 10 页），⭐ **页数以 `pdfinfo` 为准**。
3. ⚠️ **Unpaywall 对占位邮箱直接 HTTP 422**（"Please use your own email address in API calls"）—— ⛔ 若不注意，会被误记成「Unpaywall 无记录」。

## ⭐ 它解除了哪条限制

⛔ [methodology.md](./methodology.md) §6 局限 **#5** 原文：「⛔⛔ **一部分自报「未见」是工具状态而不是文献状态。**」

⭐ **两个已核实的伪缺口现已全部取到全文**，⛔ 且原诊断的错因逐条查清（一个是路径错叠加证书问题、一个是「需要 OCR」的判断本身错）。⭐ 故该限制**解除**；⚠️ **但它留下一条纪律**：

> ⛔ **取件失败必须记下试过的完整入口清单与失败码**，⭐ 而不是只记一句结论。⚠️ 本轮两个伪缺口之所以能被查出，正因为另一路记了「`curl -k`」这个细节；⭐ 而 Lange IEEE Software 2006 之所以能被判为**真缺口**，正因为它的 8 条入口失败原因逐条在册。

## 更新日志

| 时间 | 内容 |
| :-- | :-- |
| 2026-08-12 | 建立。10 个目标 9 个取到全文；两个伪缺口的错因查清；三处元数据被证伪并回写；三条可复用取件结论。 |
