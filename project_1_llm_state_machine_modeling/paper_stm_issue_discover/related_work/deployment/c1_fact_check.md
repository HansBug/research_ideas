# C1 · 事实核验报告

> ⭐ 本文件是 N1a 层 3 的**独立事实核验**产出。⛔ 只做查证，⛔ 不评价结论好坏、⛔ 不提改进建议。⭐ 核验日期 **2026-08-13**。⛔ 本文件**未修改**其他任何文件。
>
> ⭐ 证据级别口径沿用 [counterarguments.md](./counterarguments.md) §0：**M** = 我方亲自取一手原文逐字比对 · **S** = 官方页面但经工具摘要 · **I** = 仅见搜索摘要或二手。⛔ 本文件下所有 ✅ 判定均为 **M**，⛔ 每条附可复算入口。

## 0. 一句话结论

⭐ 核了约 **180 条断言**（⭐ 法规 / 标准条文与逐字引文 **92** 条 · ⭐ 题录与 DOI / arXiv 元数据 **75** 条 · ⭐ 跨文件一致性与算术 **12** 条）。⭐⭐ **任务点名的 P0 八条法规 clause 与逐字原文，⭐ 全部一字不差命中**，⛔ 一条编造都没有；⭐ 三处 clause 编号纠错（DO-178C §7.2.7、ISO/SAE 21434 Clause 7/15、保密法实施条例 786 号）**全部证实为正确纠错**。⛔ 但**确认错误 15 条**（⛔ 其中 3 条会直接影响 [SUMMARY.md](./SUMMARY.md) 的承重结论）、⚠️ **存疑未决 6 条**、⛔ **跨文件矛盾 5 处**（⭐ 4 处已裁定、⚠️ 1 处不存在）。

⛔⛔ **最严重的三条**：① **counterarguments §3 那条 ICSE'26 Angermeir 的 DOI 是死链**（⛔ doi.org 404、⛔ Crossref 无记录、⛔ DBLP 只有 CoRR），⛔ 而它是 SUMMARY §3「替代动机」的主引文；② **SUMMARY §2.1 反证 2 把 Anthropic 的 "can **only** be processed" 删成 "can be processed" 并标为「官方逐字」**；③ **SUMMARY §6 与 mde §0 把全库分母 3,740 条 / 43 venue-年份 记在 MDE/RE 一侧**，⛔ 而该侧实为 **1,455 条 / 31 venue-年份**——⛔ 这把「该侧未见有证据力」这句话的分母虚增约 **2.6 倍**。

---

## 1. ⛔ 确认错误

### 1.1 ⛔⛔ counterarguments §3 材料 ① · Angermeir 的 DOI `10.1145/3744916.3773207` 是死链，⛔ 且录用状态无任何登记机构确认

**原文怎么写的**（[counterarguments.md](./counterarguments.md) §3 表格第 ① 行）：「⭐⭐ **Angermeir et al., ICSE 2026**（[arXiv:2510.25506](https://arxiv.org/abs/2510.25506)，DOI [10.1145/3744916.3773207](https://doi.org/10.1145/3744916.3773207)，**M**）」。⭐ [SUMMARY.md](./SUMMARY.md) §3 与 §5 建议 1 都把它当作「⭐ ICSE'26 Angermeir」这一既成事实引用。

**实际是什么**：

| 查证入口 | 结果 |
| :-- | :-- |
| `curl -H "Accept: application/vnd.citationstyles.csl+json" https://doi.org/10.1145/3744916.3773207` | ⛔ **HTTP 404**（`Error: DOI Not Found`） |
| 同上，⭐ 会议卷 DOI `https://doi.org/10.1145/3744916` | ⛔ **HTTP 404** |
| `api.crossref.org/works?query.bibliographic=Reflections+on+the+Reproducibility+of+Commercial+LLM+Performance...` | ⛔ 无任何匹配条目 |
| `api.crossref.org/works?query.author=Angermeir&filter=from-pub-date:2026-01-01` | ⛔ 共 4 条，⛔ **无一条是本文**（均为 JSS / IST / JORS） |
| `api.crossref.org/prefixes/10.1145/works?filter=container-title:Proceedings of the IEEE/ACM 48th International Conference on Software Engineering` | ⭐ ICSE 2026 已注册条目的前缀是 **`10.1145/3786580` / `3786582`**（⭐ ICSE-SEIP 2026 是 `3786583`），⛔ **不是 `3744916`** |
| `dblp.uni-trier.de/search/publ/api?q=Reproducibility+Commercial+LLM+Performance...` | ⛔ 仅 **1** 条，type = `Informal and Other Publications`，venue = **CoRR 2025**，doi = `10.48550/ARXIV.2510.25506` |
| `dblp.uni-trier.de/db/conf/icse/icse2026.html` | ⛔ **404**（ICSE 2026 主会 proceedings 尚未进 DBLP） |
| `conf.researchr.org/search/icse-2026/...`（⭐ 三种检索词） | ⛔ 零结果（⚠️ ⛔ 该检索页可能是 JS 渲染，⛔ 零结果不作证据） |

⭐ **错误的来源不在 subagent，⛔ 在预印本自身**：⭐ 我下载 `arxiv.org/pdf/2510.25506v3` 并提取，⭐ 其 camera-ready ACM 版权块逐字印着「ICSE '26, Rio de Janeiro, Brazil」「ACM ISBN 979-8-4007-2025-3/2026/04」「https://doi.org/10.1145/3744916.3773207」「48th International Conference on Software Engineering (ICSE '26), April 12–18, 2026」。⛔ 也就是说那串 DOI 是**上游预分配但从未注册**的。

**影响哪个结论**：⛔ 论文若照抄该 DOI，⛔ 读者点击得到 `DOI Not Found`。⛔ 且 counterarguments 给它标 **M**（⭐ 一手逐字），⛔ 而「ICSE 2026 已录用」这一点**没有任何登记机构佐证**——⛔ 按 [mde_re_venue_scan.md](./mde_re_venue_scan.md) §4.2 自己立下的规矩（⛔「页眉的可信度为零」「⭐ 判『是否 preprint』必须以 DBLP 为准」），⛔ 这条恰恰不满足该规矩。⚠️ ⛔ 注意本条**只否证 DOI 与登记状态**：⭐ 该文的**全部内容断言我逐字核过、全部成立**（见 §3.3）。

### 1.2 ⛔⛔ SUMMARY §2.1 反证 2 · Anthropic 引文删去了 "only"，⛔ 却标为「官方逐字」

**原文怎么写的**（[SUMMARY.md](./SUMMARY.md) §2.1 反证表第 2 行）：「⛔ **Anthropic 官方逐字**：「ITAR data **can** be processed in Claude via AWS Bedrock」」。

**实际是什么**（⭐ `curl https://support.claude.com/en/articles/13756069-public-sector-faqs` 剥标签后逐字）：

> ITAR data **can only** be processed in Claude via AWS Bedrock, which is IL5 accredited.

⛔ 被删掉的是 **`only`** 这个限定词，⛔ 而且**删在句中且未加省略号**。⭐ [regulatory_ledger.md](./regulatory_ledger.md) §2.1 与 §2.6 引的是**完整正确**的版本——⛔ 所以这是 SUMMARY 在压缩时引入的失真，⛔ 不是原始调研的错。

**影响哪个结论**：⛔ 方向上使反证读起来比原文更宽（⛔「可以处理」vs⛔「只能经 Bedrock 处理」）。⭐ 该反证要驳的命题（⛔「必须私域部署」）仍然成立，⛔ 但**「官方逐字」这个标签是假的**，⛔ 且这类删改正是 [talks/GUIDE.md](../../../../talks/GUIDE.md) §9 与仓库 §3.5 要抓的东西。

### 1.3 ⛔⛔ SUMMARY §6 与 §4 第 3 条 · 把全库分母记在 MDE/RE 一侧

**原文怎么写的**：

- [SUMMARY.md](./SUMMARY.md) §6 覆盖边界表：「⭐ **MDE / RE** | ⭐ 9 venue · **43 venue-年份** · **3,740 条题录**（⭐ DBLP 权威分母，⭐ 摘要获取 94.2%）| ⭐ 这一侧的「未见」**有证据力**」
- [SUMMARY.md](./SUMMARY.md) §4 第 3 条：「⛔ **3,740 条题录只有 2 篇写出这条因果**」
- [mde_re_venue_scan.md](./mde_re_venue_scan.md) §0：「⭐ **在 MDE / RE 的 9 个 venue、43 个 venue-年份、3,740 条题录里**…」

**实际是什么**（⭐ 由 mde 自己的 §1.1 / §1.2 逐格加总，⭐ 我复算）：

| 侧 | venue-年份 | 题录 |
| :-- | --: | --: |
| ⭐ MDE / RE（MODELS / MODELS-C / RE / REFSQ / SLE / MODELSWARD / STAF / SoSyM / REJ） | **31** | **1,455** |
| ⭐ SE 期刊侧（TSE / TOSEM / EMSE，⛔ **不是 MDE/RE venue**） | **12** | **2,285** |
| 合计 | **43** | **3,740** |

⭐ 复算过程：MDE/RE venue-年份 = MODELS 3 + MODELS-C 3 + RE 3 + REFSQ 4 + SLE 4 + MODELSWARD 4 + STAF 2 + SoSyM 4 + REJ 4 = **31**；题录 = 83 + 405 + 187 + 99 + 71 + 188 + 43 + 309 + 70 = **1,455**。⭐ 1,455 + 2,285 = 3,740 ✅ 与 mde §1.1「MDE / RE 侧小计：1,455 条题录」、§1.2「SE 期刊侧小计：2,285 条题录」、「全部合计…3,740」**完全一致**——⛔ 所以 mde 的 §1 是对的，⛔ 错的是它自己的 §0 与 SUMMARY。

**影响哪个结论**：⛔ 直接影响 SUMMARY §6 那句「⭐ 这一侧的「未见」**有证据力**」的分量——⛔ 分母被虚增约 **2.6 倍**。⛔ 且 §4 第 3 条的「3,740 条题录只有 2 篇」在算术上不成立：⛔ 那 2 篇命中在 MDE/RE 的 1,455 条里，⛔ 而 SE 期刊侧的 2,285 条**另有 37 条触发部署/保密信号、6 条被判承重**（mde §1.2 与 §2.6）。

### 1.4 ⛔ mde §1.1 「137 条 LLM 信号题录」与自己的逐 venue 列不符（⛔ 列加总为 126）

**原文怎么写的**（[mde_re_venue_scan.md](./mde_re_venue_scan.md) §1.1 末行）：「⭐ **MDE / RE 侧小计：1,455 条题录，137 条 LLM 信号题录，摘要获取 129/137（94.2%）。**」⭐ §5.1 第 2 条重复：「⛔ MDE / RE 侧的 LLM 论文摘要覆盖率是 **129/137（94.2%）**」。

**实际是什么**：⭐ 逐 venue「LLM 题录」列加总 = MODELS (2+3+2) + MODELS-C (4+14+14) + RE (3+11+18) + REFSQ (0+1+7+2) + SLE (1+1+0+1) + MODELSWARD (1+4+3+9) + STAF (1+11) + SoSyM (3+3+1+1) + REJ (0+0+2+3) = 7 + 32 + 32 + 10 + 3 + 17 + 12 + 8 + 5 = **126**。⛔ 与 137 差 **11**。⭐ 题录总数列加总为 1,455 ✅ 无误，⛔ 只有 LLM 列不闭合。

**影响哪个结论**：⛔ 「94.2% 摘要获取率」这个用来支撑「⭐ 这一侧的零命中不是工具失灵」的数字，⛔ 其分母无法从表内复算。⛔ 按仓库 §2.4「统计数字必须与表格真实内容一致」，⛔ 这是口径不闭合。

### 1.5 ⛔ se_motivation_survey §2.2 把 arXiv:2511.11125 说成 ABB 的工作

**原文怎么写的**（[se_motivation_survey.md](./se_motivation_survey.md) §2.2 首句）：「⭐ [arXiv:2511.11125](https://arxiv.org/abs/2511.11125)（**ABB** RAPID 机器人程序修改）把保密句放在方法节的模型选型段」。

**实际是什么**（⭐ `curl https://arxiv.org/html/2511.11125v1` 逐字）：

> Salim Fares OrcID: 0009-0003-3138-3518 **Affiliation: University of Passau, Passau, Germany** email: salim.fares@uni-passau.de and Steffen Herbold OrcID: 0000-0001-9765-2803 **Affiliation: University of Passau, Passau, Germany**

⭐ 论文研究的是 **ABB 的 RAPID 语言**（⭐ 正文逐字：「domain-specific languages like **ABB's RAPID Programming Language** (RAPID) are the norm in this domain」），⛔ 但**作者与单位都是 University of Passau**，⛔ 与 ABB 无归属关系。

**影响哪个结论**：⛔ 同一文件 §3.3 把 **ABB 的 Spec2Control**（Koziolek et al.）立为「⛔ 反例」——⛔ 于是读者会读成「⛔ ABB 自己一边用本地 Llama 70B（§2.2）、⛔ 一边用 Azure GPT-5（§3.3）」，⛔ 这个自相矛盾的印象是错的。⛔ 该表格行本身写的是「Fares & Herbold」✅ 正确，⛔ 只有 §2.2 的叙述层出错。

### 1.6 ⛔ se_motivation_survey §1.2 给 arXiv:2406.07737 印了错误作者

**原文怎么写的**（[se_motivation_survey.md](./se_motivation_survey.md) §1.2 表格）：「**Sun, Chen, Bissyandé et al.（作者名待核）**, *The Future of AI-Driven Software Engineering*」。

**实际是什么**（⭐ `curl https://arxiv.org/abs/2406.07737`）：作者为 **Valerio Terragni, Annie Vella, Partha Roop, Kelly Blincoe**。⭐ arXiv comments 亦确认「Published in ACM Transactions on Software Engineering…」→ ⭐ TOSEM 归属 ✅ 成立。

**影响哪个结论**：⛔ 三位被印出的作者与本文无关。⭐ 缓解因素：⭐ 该格与 §References [10] 都标了「⛔ 作者待核」，⛔ 但错误姓名仍以事实形态印在表里。⭐ 顺带核清：⭐ §6.3 待核项 6、7 均可结案——⭐ 2406.07737 = Terragni / Vella / Roop / Blincoe；⭐ 2312.08055 = **June Sallou, Thomas Durieux, Annibale Panichella** ✅（⛔ 原文猜测正确）。

### 1.7 ⛔ SUMMARY §6 与 small_model_papers §6.2 项 18 把 arXiv:2607.03691 的题名写错

**原文怎么写的**：

- [SUMMARY.md](./SUMMARY.md) §6：「⭐ [arXiv:2607.03691](https://arxiv.org/abs/2607.03691) *Don't Blame the Large Language Model*（⛔ 可能主张脚手架才是主因…）」
- [small_model_papers.md](./small_model_papers.md) §6.2 项 18：「⛔ **arXiv:2607.03691, *Don't Blame the Large Language Model: How Scaffolding Evolution Shapes Coding Agent Quality***」

**实际是什么**（⭐ `curl https://arxiv.org/abs/2607.03691`）：题名为 *Don't Blame the Large Language Model: How **Agent Harness** Evolution Shapes Coding Ag…*；⭐ 作者 **Oussama Ben Sghaier, Hao Li, Bram Adams, Ahm[ed E. Hassan]**。⛔ 副题的关键词是 **Agent Harness**，⛔ 不是 `Scaffolding`。

**影响哪个结论**：⛔ 该条被 SUMMARY §6 与 small_model_papers §6.3 第 6 条列为「⛔ 必须补读的反方证据」，⛔ 而写错的正是决定它是否真的反方的那个词（⭐ agent harness ≠ scaffolding，⛔ 后者才是本调研的核心概念）。⛔ 按错题名检索会找不到，⛔ 或找到别的东西。

### 1.8 ⛔⛔ counterarguments §7.2 说 VDA ISA 目录「不公开 / 需注册、⛔ 一律不引条文内容」——⛔ 事实相反，⛔ 且与 regulatory_ledger §2.7 直接冲突

⭐ 本条是**跨文件矛盾**，⭐ 裁定见 §4.3；⛔ 之所以列在「确认错误」，⭐ 是因为我已亲自把 counterarguments 那一格证伪。

**两处逐字原文**：

- [counterarguments.md](./counterarguments.md) §7.2 表格末行：「BMB17 / GJB 系列 · 军工审查标准 · **VDA ISA 目录** · NSA "Raise the Bar" | ⛔ **不公开 / 需资质 / 需注册** | ⛔ 一律不引条文内容」
- [regulatory_ledger.md](./regulatory_ledger.md) §2.7：「**版本事实（🟢 官方 XLSX 已下载逐格核验）**：⭐ 当前生效目录是 **VDA ISA 6.0.3**（文件 `isa6-en.xlsx`…）」＋ ⭐ 其后整张 🟢 表逐字引控制项文本。

**实际是什么**：⭐ `curl https://portal.enx.com/en-US/TISAX/downloads/` **无需登录即返回 200**，⭐ 页面直接挂 `/isa2027-en.xlsx`、`/isa6-en.xlsx`、`/isa2027-en_redline.xlsx`、`/isa6-en_redline.xlsx` 四个链接。⭐ 我 `curl` 下载两份（244,910 B / 265,000 B，均 `Microsoft Excel 2007+`），⭐ 解 `xl/sharedStrings.xml` 后**逐条比对了 ledger 引的全部七条控制项文本，⭐ 七条全部一字不差**（⭐ 明细见 §3.2）。

**影响哪个结论**：⛔ counterarguments 因此把 §1.2「⛔ 别用 TISAX」一栏的论据来源写成不可得，⛔ 而实际上它是本轮**唯一逐字点名 AI 工具**的成文依据，⛔ 且可自由核验。⛔ 两处并存会让后续 agent 无法判断该不该引。

### 1.9 ⛔ verification_log §V2 把 Stroebl 归到「自我批判」机制下

**原文怎么写的**（[verification_log.md](./verification_log.md) §V2 干预类型表）：「⛔ **自我批判**（Huang / Stroebl / ⛔ 我们现在的 loop） | ⛔ 让模型判断自己的产出对不对 | ⛔ **更差**」。⭐ [SUMMARY.md](./SUMMARY.md) §3.2 第 2 条同构：「⛔ **自我批判**（让模型判断自己对不对）⛔ 对弱模型更差」。

**实际是什么**（⭐ `curl https://arxiv.org/abs/2411.17501` 摘要逐字）：题名为 **The Limits of Inference Scaling Through Resampling**；机制是**验证器不完美、假阳性率非零，从而给重采样式 inference scaling 设上界**：

> we show that this approach is fundamentally limited **when verifiers are imperfect and have a non-zero probability of producing false positives**. Resampling cannot decrease this probability, so it imposes an upper bound to the accuracy of resampling-based inference scaling, regardless of compute budget.

⭐ counterarguments §6 引的那句「no amount of inference scaling of weaker models can enable them to match the single-sample accuracy of a sufficiently strong model」**逐字属实** ✅。⛔ 但它的机制是**外部验证器的假阳性**，⛔ 不是「模型判断自己对不对」。⛔ 另：「⛔ 不可能性定理」是本仓库自造的标签（⭐ 与 [discover_matrix/docs/findings/README.md](../../discover_matrix/docs/findings/README.md) 的用法一致），⛔ 原文无此词。

**影响哪个结论**：⛔ V2 那张表的整个论证结构是「⭐ 自我批判对弱模型更差 / ⭐ 多阶段分解对弱模型更好」，⛔ 而 Stroebl 被用作左栏的第二支柱。⛔ 归错机制后，⛔ 左栏实际只剩 Huang 一篇支撑。⛔ 且我们的方法不是「重采样 + 不完美验证器」，⛔ 所以它对我们的适用性需另行论证，⛔ 不能直接搬。

### 1.10 ⛔ regulatory_ledger 对 IS.D.OR.200(a)(13) 的逐字引文有未标注的句中删除

**原文怎么写的**（[regulatory_ledger.md](./regulatory_ledger.md) §1.1 表与 §2.7c 表，⭐ 均标 🟢）：「"…**protects the confidentiality of any information that the organisation may have received from other organisations**, according to its level of sensitivity."」

**实际是什么**（⭐ `curl https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32022R1645` 剥标签后逐字）：

> (13) protects, **without prejudice to applicable incident reporting requirements,** the confidentiality of any information that the organisation may have received from other organisations, according to its level of sensitivity.

⛔ 被删的是 `without prejudice to applicable incident reporting requirements,`，⛔ 且删在句中、⛔ 未加省略号（⭐ 句首那个「…」只覆盖前文）。

**影响哪个结论**：⭐ 保密义务本身不变，⛔ 但该文件第 7 行自己声明「⭐ 凡标 🟢 的引文**均逐字取自** preview PDF 的正文范围」——⛔ 这条不满足自己的声明。⭐ 同族三条（IS.D.OR.205(a)、IS.D.OR.235(a)、21.A.239A）我逐字核过，⭐ **全部一字不差** ✅。

### 1.11 ⛔ 六个文件都把 60.4% / 76.2% / −15.82pp 当作已定数字，⛔ 而其出处自己写着分母可能变

**原文怎么写的**（⭐ 出现在 [README.md](./README.md) §一条前提、[SUMMARY.md](./SUMMARY.md) §2.4、[counterarguments.md](./counterarguments.md) §0、[verification_log.md](./verification_log.md) §V1、[mde_re_venue_scan.md](./mde_re_venue_scan.md) §6、[small_model_papers.md](./small_model_papers.md) §2 策略 B，⛔ 无一处带限定）：「⛔ 主臂 `hit@1` **60.4%** 而朴素基线 **76.2%**（⛔ Δ = −15.82pp）」。

**实际是什么**：⭐ 数字本身**可复算且吻合** ✅ —— [baseline_arm/docs/generations/x1v2/verdicts.md](../../baseline_arm/docs/generations/x1v2/verdicts.md) 第 47 行：「`hit@1` | **448/588 = 76.2%** | 443/588 = 75.3% | 355/588 = 60.4% | **+93 位 / +15.8pp**」；⭐ 93 / 588 = 15.816% → 15.82pp ✅。⛔ **但被引的另一份出处带一条被全部六个文件丢掉的限定** —— [discover_matrix/docs/findings/route_selection_and_v47_plan.md](../../discover_matrix/docs/findings/route_selection_and_v47_plan.md) 第 83 行逐字：

> ⛔ **台账正在全量人工重标（54 份工作单、33–49 人时）。⛔ 在它完成前不要锁定选题——76.2% / 60.4% 的分母本身可能变。**

**影响哪个结论**：⛔ 这个差值是 counterarguments §0「⛔ 第二致命的一刀」、verification_log §V1 比较 A/B 拆分、SUMMARY §2.4 的共同基座。⛔ 六份文件把「⭐ 可能变的数」写成「⛔ 已定的数」，⛔ 属于方向性松紧不一致（⭐ 对我方不利的数字写满、⛔ 但它自带的松动限定被省掉）。

### 1.12 ⛔ se_motivation_survey 在两处已被裁定的事实上仍是旧版

⭐ 明细与逐字对照见 §4.1 与 §4.2。⛔ 简言之：⭐ [mde_re_venue_scan.md](./mde_re_venue_scan.md) §4.1 / §4.2 已把 **Falcão & Canedo 一手来源找到**、把 **2511.11125 与 2412.02789 的录用状态查清**，⛔ 并明写了「⭐ 对 [se_motivation_survey.md](./se_motivation_survey.md) 的回写建议」，⛔ 但 se_motivation_survey **未回写**，⛔ 仍在正文与 §References 里印着「⛔ 不得引用」「⛔ 未见录用证据」「⛔ 录用状态待核验」。⛔ 我已独立复核，⭐ mde 全对。

### 1.13 ⛔ counterarguments §2.2 ③ 把 arXiv:2409.03454 说成软件工程数据，⛔ 未交代它是机器翻译研究

**原文怎么写的**（[counterarguments.md](./counterarguments.md) §2.2 第 3 步）：「⭐ [arXiv:2409.03454](https://arxiv.org/abs/2409.03454)（Vieira et al.）在**一家软件行业公司的内部私域数据**上证明：Llama 3 8B Instruct 用 **1k / 2k 样本微调时性能比未微调 baseline 更差**，需到 207k 才大幅改善。」

**实际是什么**（⭐ arXiv 摘要逐字）：题名 *How Much Data is Enough Data? Fine-Tuning Large Language Models for **In-House Translation***；⛔ 任务是**机器翻译**，⛔ 用的是 translation memories（TMs），⛔ 五个语向（英→巴葡 / 捷 / 德 / 芬 / 韩），⛔ 指标 BLEU / chrF++ / TER / COMET。⭐ 数字断言 ✅ 逐字属实：「there is a performance deterioration in comparison with the baseline model when fine-tuning on only **1k and 2k** examples; however, we observe a substantial improvement as the training dataset size increases」，⭐ 且「TMs **from a specific organisation in the software sector**」——⭐ 所以「软件行业公司」这一半站得住。

**影响哪个结论**：⛔ 该条被用来论证「⭐ 我们这个 SE 任务上，⛔ 工业客户手上恰恰是 1k–2k 这个量级，⛔ 所以微调的前提不成立」。⛔ 而证据来自 MT 任务的 TM 数据，⛔ 跨任务外推需要额外论证，⛔ 而这一点未写。⛔ 审稿人打开原文就会看到 `Translation`。

### 1.14 ⛔ mde_re_venue_scan 内部对 Text2VQL 与 Chou et al. 的判定自相矛盾（⛔ 装饰 vs 未判定）

**两处逐字原文**：

- §0：「⛔⛔ **两篇都读到了全文，⛔ 两篇都是装饰。**」；§2.2 字段表：「判定 | ⛔ **装饰**」；§2.3 字段表：「判定 | ⛔ **装饰**（⭐ 但比 §2.2 强半档…）」
- §3.2 末行：「⛔ **净命中：MDE / RE 侧 17 − 12 = 5 条**，⭐ 即 §2.1（装饰）、**§2.2 与 §2.3（未判定）**、§2.4 与 §2.5（非保密动机）。」

⛔ 且 §2.2 与 §2.3 的小节标题都带 **⏳**（⭐ 该文件其他处用 ⏳ 表示未完成），⛔ 与「⭐ 读到什么程度：**全文**」及「判定：装饰」冲突。

**影响哪个结论**：⛔ 「MDE/RE 侧承重 = 0」这条结论的构成方式取决于这两篇算「装饰」还是「未判定」——⛔ 前者是**已判定为非承重**，⛔ 后者是**尚未判定**，⛔ 两者对「零命中有多硬」的含义完全不同。

### 1.15 ⛔ regulatory_ledger §2.2b 对《汽车数据安全管理若干规定》第三条的概括过强，⛔ 且漏掉一条反向事实

**原文怎么写的**（[regulatory_ledger.md](./regulatory_ledger.md) §2.2b 表与 §3.2 表）：「⛔ **不覆盖**：⛔ 枚举六项**全部是运行期数据**，⛔ 无一项是设计/需求文档」。

**实际是什么**（⭐ `curl https://www.cac.gov.cn/2021-08/20/c_1631049984897667.htm` 逐字）：

- ⛔ 第（六）项是**开放式兜底**，⛔ 不是运行期数据：「（六）国家网信部门和国务院发展改革、工业和信息化、公安、交通运输等有关部门确定的其他可能危害国家安全、公共利益或者个人、组织合法权益的数据。」
- ⛔ **更要紧的是同条第一款**：「本规定所称汽车数据，包括汽车**设计**、生产、销售、使用、运维等过程中的涉及个人信息数据和重要数据。」——⛔ 即该规定的**数据范围明文含设计阶段**。

**影响哪个结论**：⛔ 「⛔ 无一项是设计/需求文档」这句在**重要数据枚举**层面大体成立，⛔ 但在**规定的适用范围**层面不成立。⭐ 方向上这条**对本 story 有利**（⭐ 立法者的汽车数据概念确实涵盖设计阶段），⛔ 而台账把它省掉了——⛔ 按仓库「方向性松紧要一致」，⛔ 漏掉有利事实与夸大有利事实同属失真。

---

## 2. ⚠️ 存疑未决

| # | 对象 | ⛔ 为什么核不动 |
| :-: | :-- | :-- |
| **1** | ⛔ **Angermeir 是否真被 ICSE 2026 录用** | ⭐ 唯一支撑是预印本自身的 camera-ready ACM 版权块（⭐ 含真实 ISBN `979-8-4007-2025-3/2026/04`、⭐ 已填 DOI、⭐「ICSE '26, Rio de Janeiro」），⛔ 但 Crossref / DBLP / researchr 检索全部零结果，⛔ ACM DL 对本环境 403。⛔ **不能裁定为已录用，⛔ 也不能裁定为未录用。** ⭐ 与 §1.1 是同一件事的另一半 |
| **2** | ⛔ **DoD GenAI.mil 三条新闻稿的逐字引文**（⭐ war.gov Release 4354916 / 4366573 / 4401775） | ⛔ `curl` 与 WebFetch **均返回 HTTP 403**（⛔ 疑 WAF）。⛔ 「Security is paramount…certified for CUI and IL5」「Google Cloud's Gemini for Government」「xAI…IL5」「OpenAI…3 million Department personnel」四句**一句都没能取到一手**。⚠️ ⛔ 而 [SUMMARY.md](./SUMMARY.md) §2.1 反证 1 与 §2.2 的整条「⛔ 最致命的一击」都压在它上面。⛔ 按仓库规范只能记「⛔ 入口已定位 / 访问异常」，⛔ **不得据此断言事实不存在**，⛔ 也**不得据此把它当已核验** |
| **3** | ⛔ **counterarguments §4.2 把 arXiv:2512.20328 称为 `FeatureSHAP`** | ⭐ 该 ID 确实存在，⛔ 但题名是 *Toward Explaining Large Language Models in Software Engineering Tasks*（⭐ 作者 Antonio Vitale, Khai-Nguyen Nguyen, Denys Po…），⛔ 元数据里没有 `FeatureSHAP`。⛔ 系统名可能在正文，⛔ 本轮未开正文，⛔ 无法确认这是同一个东西 |
| **4** | ⛔ **GB/T 22239-2019 的全部条款号** | ⭐ ledger 已自标 🟡 并写明「⚠️ ⛔ 正式引用前必须人工在 openstd 官方预览页复核一次」。⛔ 我未尝试（⛔ openstd 为 JS 渲染页）。⛔ **该自陈本身是准确的**，⛔ 本条只是确认它仍未闭环 |
| **5** | ⛔ **付费墙内条文** | ⭐ IEC 62443-4-1 §5.9.1/§5.9.2、⭐ IEC 81001-5-1 §5.1.2/§4.1.5、⭐ ISO 26262-8 §5.4.3 与 Clause 11、⭐ ISO/SAE 21434 Clause 7 与 Annex C、⭐ ISO/IEC TR 5469 §10.3.5、⭐ DO-178C §7.2.7 正文。⭐ 我**逐一确认了它们的目录标题 / 页码位置**（⭐ 见 §3.1），⛔ 正文确实不在 preview 内。⭐ **ledger 对这些一律标 🔴 且不据标题推断内容 —— 这个处理是正确的**，⛔ 本条不构成问题 |
| **6** | ⛔ **VerIbmc / Konstantinou / Sepidband 等 2026 preprint 的 venue** | ⭐ arXiv 元数据无 journal-ref；⭐ small_model_papers §6.2 已把它们列为待核。⭐ 顺带查清一条：⭐ [arXiv:2606.04739](https://arxiv.org/abs/2606.04739)（⭐ Kaniewski et al., Revisiting Vul-RAG）**arXiv comments 写着「Accepted at AI&CCPS 2026 workshop」**——⛔ counterarguments §7.3 项 9 把它整条标 **I**，⭐ 现在至少录用状态可升级；⛔ 但「0.30 平台期」这个数字仍未核（⛔ 未开正文） |

---

## 3. ✅ 已核无误

### 3.1 法规 / 标准（⭐ 92 条断言，⛔ 除 §1.10 / §1.15 与下列「引文精度小瑕」外全部命中）

⭐ **P0 指定八条 —— ⭐ 全部逐字一致，⛔ 无一条编造**：

1. ⭐ **IEC 61508-1:2010 §1.2 m)** ✅ 逐字命中（⭐ 并顺带核对 §1.2 k) / l) 与 NOTE 5「see ISO/IEC/TR 19791 and IEC 62443 series」✅）。⭐ 入口：`curl https://cdn.standards.iteh.ai/samples/14795/b305f26083da4dcb915a95166796f773/IEC-61508-1-2010.pdf` → `python -m tools.pdf_extractor -m text` → `grep "security polic"`
2. ⭐ **EN 50716:2023 Introduction** ✅ 逐字命中三句全文（⭐ 并核对封面 Supersedes 六项清单、⭐ CENELEC 批准 2023-10-30、⭐ dop 2024-10-30、⭐ **dow 2026-10-30** ✅）。⭐ 入口：NSAI 样张 `https://i2.saiglobal.com/mpc2v/preview/1412600409546.pdf?sku=1348800_SAIG_NSAI_NSAI_3361513`
3. ⭐ **ISO/SAE 21434:2021 §1 Scope** ✅ 「This document does not prescribe specific technology or solutions related to cybersecurity.」逐字命中；⭐ **Clause 7 = Distributed cybersecurity activities / Clause 15 = Threat analysis and risk assessment methods** ✅ —— ⭐ ledger §1.4 的编号纠错**证实正确**；⭐ Clause 7 的 Introduction 描述亦逐字命中
4. ⭐ **ISO 26262-8:2018 §5.1 a)/b)/c) + §5.2 NOTE 1 + NOTE 2** ✅ 全部逐字命中；⭐ 另核 §1 Scope 的支持过程枚举**恰为 12 项**、⭐ 无一项涉保密 ✅
5. ⭐ **DFARS 252.204-7012 (a) `Technical information` 定义** ✅ 逐字命中（⭐ 另核 `Controlled technical information`、`Covered defense information` 两条定义 ✅、⭐ 条款标题 `(MAY 2024)` ✅、⭐ 页面 `DFARS Change 5/7/2026` ✅、⭐ (b)(2)(ii)(D) 全文 ✅）
6. ⭐ **NIST SP 800-171 Rev 2 §3.1.20 DISCUSSION** ✅ 逐字命中，⭐ 含 "…including accessing cloud services (e.g., infrastructure as a service, platform as a service, or **software as a service**) from organizational systems." ✅；⭐ 另核 §3.1.3 与其 DISCUSSION ✅、⭐ §3.1.22 DISCUSSION「systems that are controlled by the organization」✅
7. ⭐ **保守国家秘密法（2024 第二次修订）第三十一条(三)** ✅ 逐字命中「使用非涉密信息系统、非涉密信息设备存储或者处理国家秘密」；⭐ 另核第二十九条 ✅、第三十条 ✅、第三十六条 ✅、第六十四条 ✅、第六十五条（2024-05-01 施行）✅。⚠️ ⭐ 附一条对 counterarguments §1.2 ① 有利的核实：⭐ 第三十一条(一)(二) 都带「未按照国家保密规定和标准采取有效保密措施」这个前提，⛔ **而(三)没有** —— ⭐ 故「⛔ 无条件禁止」这个判断成立 ✅
8. ⭐ **ITAR 22 CFR §120.54(b)(1)(i)+(ii)** ✅ 两个构成要件逐字命中；⭐ 另核 (a)(5) 五项 ✅、(b)(2) ✅、(c) ✅。⭐ 入口：`curl "https://www.ecfr.gov/api/versioner/v1/full/2026-08-01/title-22.xml?part=120&section=120.54"`

⭐ **另核对并全部命中的（⛔ 按族）**：

| 族 | 已逐字核对且命中 |
| :-- | :-- |
| ⭐ 美国出口管制 | ⭐ EAR §734.18(a)(5) / **(b) end-to-end encryption 定义** / (c) ✅ 全部逐字；⭐ ITAR **§120.50(a)(6)**「The release of previously encrypted technical data as described in § 120.56(a)(3) and (4)」✅ 与 **§120.56(a)(4)**「The use of access information to cause technical data outside of the United States to be in unencrypted form」✅ —— ⭐ counterarguments §1.2 ④ 的条号链**成立** |
| ⭐ 美国国防供应链 | ⭐ DFARS **252.204-7021 (NOV 2025)** 标题与 `[90 FR 43575, Sept. 10, 2025]` ✅、(d)(2) 逐字 ✅；⭐ **32 CFR 170.16(c)(2)**「An OSA **may use** a cloud environment…(i) FedRAMP Authorized at the FedRAMP Moderate (or higher) baseline…**or** (ii)…equivalent」✅ 逐字；⭐ **NARA CUI Registry / Controlled Technical Information** 的 Examples 全句 ✅ 逐字 + Banner `CUI//SP-CTI` ✅ |
| ⭐ **FedRAMP 实况** | ⭐⭐ **OpenAI `ChatGPT Enterprise and API Platform`**：⭐ Package ID `FR2533155773` ✅、⭐ Status `FedRAMP Certified` ✅、⭐ **As of 1/9/2026** ✅、⭐ Type `20x` / Path `Program` / **Class `Class C (Moderate)`** ✅、⭐ Certified Since `1/9/2026` ✅ —— ⭐ ledger §2.6 与 SUMMARY §2.1 反证 3 **完全属实**；⚠️ ⭐ 并**结清 counterarguments §7.3 项 2 的存疑**：⭐「Class C」这些字段标签是 2026 站点的**真实术语**，⛔ 不是转述失真 |
| ⭐ 欧盟 | ⭐ **EU 2022/1645**：⭐ 通过日 2022-07-14 ✅、⭐ OJ L 248, 26.9.2022 ✅、⭐ **It shall apply from 16 October 2025** ✅、⭐ 21.A.239A 与 21.A.139A 插入方式 ✅、⭐ IS.D.OR.205(a) 逐字 ✅、⭐ IS.D.OR.235(a) 逐字 ✅（⛔ (a)(13) 见 §1.10） |
| ⭐ **EASA** | ⭐⭐ **NPA 2025-07(A) 两句逐字全中**：⭐「…to ensure human oversight at development time when using generative AI techniques by avoiding the double development and verification with AI tools.」✅ 与 ⭐「While generative AI tools and general-purpose models are not yet fully covered, the current proposal creates a flexible foundation for adaptation as technology evolves.」✅；⭐ 文件确为 16 页 NPA、⭐ 自陈「The **non-binding** and modular nature of the proposed DS」✅ —— ⭐ ledger「⛔ 征求意见稿、⛔ 非生效规章、⛔ 出现在范围排除说明段」三条限定**全部准确**。⭐ 入口：`curl https://www.easa.europa.eu/en/downloads/142702/en`（⚠️ ⛔ 直接 `grep "double development"` 会漏，⛔ PDF 内断词作 `doub le`） |
| ⭐ 中国出口管制 | ⭐ 出口管制法第二条一/二/三款 ✅、第四条 ✅、第十二条第三款三类风险 ✅；⭐⭐ **禁止出口限制出口技术目录 `203912X`**：⭐ 序号 **71**、⭐ 位于**限制出口部分**（⭐ 该部分自文本第 226 行起，⭐ 条目在第 952 行）、⭐ 第 5 项逐字「无人机飞行控制系统（自主导航、路径及避障规划等相关的算法及软件）」✅ —— ⭐ **ledger §2.1b 的跨代理裁定完全正确**；⭐ 机械复核「工业控制 / 嵌入式 / 状态机 / 工业软件」四词命中 **0 / 0 / 0 / 0** ✅ |
| ⭐ 中国数据 / 网络 | ⭐⭐ **网络安全法 2025 修正**：⭐ 「根据 **2025 年 10 月 28 日**…决定修正」✅、⭐ **现行第三十九条 = CIIO 境内存储** ✅ 逐字、⭐ **新第三十七条 = 采购网络产品和服务的国家安全审查** ✅ 逐字 —— ⭐ ledger 的条号纠错**证实正确**；⭐ **自 2026 年 1 月 1 日起施行**经[中国人大网决定全文](http://www.npc.gov.cn/npc/c2/c30834/202510/t20251028_449048.html)与[中国政府网](https://www.gov.cn/yaowen/liebiao/202510/content_7046194.htm)核实 ✅（⚠️ ⛔ cac.gov.cn 合并文本页本身不含该日期）；⭐ 令 16 号第二条 ✅ / 第三条 ✅ / **第五条末款「前款所称向境外提供的个人信息，不包括重要数据」** ✅ / 第七条 ✅ + ⭐ 施行日 = 公布之日 2024-03-22 ✅；⭐ 汽车数据规定第三条六项 ✅（⛔ 概括问题见 §1.15）、⭐ 第十一条「重要数据应当依法在境内存储」✅ |
| ⭐ 中国保密族 | ⭐ **保密法实施条例 = 国务院令第 786 号**（⭐ 2024-07-10 修订公布 / 2024-09-01 施行）✅ —— ⭐ ledger 对「788 号」的纠错**证实正确**；⭐ 第三十三条 ✅ / 第四十一条 ✅ 逐字；⭐⭐ **武器装备科研生产单位保密资质管理办法**：⭐ 标题用「**资质**」✅（⭐ 纠错正确）、⭐ 第五条「分为一级、二级**两个**等级」✅（⭐「三级改两级」正确）、⭐ 第六条三句 ✅ 逐字、⭐ 第十一条(五)(六) ✅ 逐字、⭐ 第二十条「审查标准和评分标准…**另行制定**」✅、⭐ 第五十六条「自 **2025 年 7 月 1 日**起施行。⭐ 2016 年 6 月 1 日施行的《武器装备科研生产单位保密**资格**认定办法》（国保发〔2016〕15 号）同时废止」✅ |
| ⭐ 中国生成式 AI | ⭐ 暂行办法第二条第三款 ✅ / 第十一条 ✅ / 第二十条 ✅ 全部逐字；⭐⭐ **政务领域人工智能大模型部署应用指引**两句逐字全中：⭐「需采用市场上成熟，并已完成网信部门备案的模型产品和服务」+「⭐ 在保障安全和不泄露国家秘密、工作秘密和敏感信息等的前提下，**充分利用互联网算力和模型资源**」✅、⭐「严格落实『**涉密不上网、上网不涉密**』…防止国家秘密、工作秘密和敏感信息等输入非涉密人工智能大模型」✅ |
| ⭐ 功能安全其余各本 | ⭐ ISO 26262-6 §5.2 NOTE 2 ✅ 逐字（含 "**can**"）；⭐ ISO/IEC TR 5469:2024 §1 Scope 第三项「use of AI systems to design and develop safety related functions」✅ 逐字；⭐ IEC 62443-4-1 §1 Scope 两句 ✅ 逐字 + ⭐ §5.9 `SM-7: Development environment security`（p.23）/ §5.11 `SM-9`（p.24）/ §5.12 `SM-10`（p.24）目录标题 ✅ + ⭐ §5.8 `SM-6: File integrity` 相邻位置 ✅；⭐ IEC 62304:2006 Introduction 自陈免责 ✅ 逐字；⭐ EN 50128:2011 §1.8 ✅ 逐字 |
| ⭐ **DO-178C / FAA** | ⭐⭐ **§7.2.7 = `Archive, Retrieval, and Release`** ✅ 在 FAA 官方 138 页对照文档中**四处独立出现**，⛔ 全部作此名 —— ⭐ ledger §1.7 的纠错**证实正确**，⛔ 「Protection against Unauthorized Changes」确非该条标题；⭐ 七词机械检索结果：`security` **0** / `confidential` **0** / `cloud` **0** / `unauthorized` **0** / `third part` **0** / `disclos` **0** / `proprietar` **0** ✅ —— ⭐ **七个 0 全部复现** |
| ⭐ **VDA ISA / TISAX** | ⭐ 见 §3.2 |
| ⭐ ISO/IEC 27001:2022 | ⭐ A.5.23 是 VDA ISA 1.3.3 的对标项 ✅ —— ⭐ 我在 `isa2027-en.xlsx` 的 1.3.3 目标段旁读到逐字对标行「ISO 27001:2022: **A.5.23**」✅ |

⚠️ **四处「引文精度小瑕」**（⛔ 不改变含义，⛔ 但该文件声明 🟢 = 逐字，⭐ 故如实记录）：

1. ⭐ ISO 26262-8 §5.1 c)：⭐ 官方为「to identify the work products to be exchanged for distributed developments **of an item and its elements**」，⛔ ledger 截到 `developments` 即止，⛔ 未加省略号。
2. ⭐ 出口管制法第十二条第三款：⛔ ledger 的版本是**压缩改写**（⛔「清单之外的货物、技术和服务…得到通知」），⭐ 官方为「出口管制清单所列管制物项以及临时管制物项之外的货物、技术和服务…得到**国家出口管制管理部门**通知，**相关货物、技术和服务**可能存在以下风险的，应当向**国家出口管制管理部门**申请许可」。
3. ⭐ 政务指引章节号：⛔ ledger 写「三、(一) 规范部署」，⭐ 实际结构是「三、规范部署 /（一）合理选择实施路径」。
4. ⭐ ISO 26262-8 §5.2 NOTE 2、⭐ IS.D.OR.235(a)、⭐ 保密法第三十条：⛔ 均在句末截断而未标省略号（⭐ 截断处都是完整句，⛔ 影响最小）。

### 3.2 ⭐⭐ VDA ISA / TISAX —— ⭐ 七条控制项文本逐格核过，⭐ 七条全中

⭐ 我 `curl` 下载官方 XLSX（⛔ **无需登录**）并解 `xl/sharedStrings.xml` 后逐条比对：

| 条目 | 结果 |
| :-- | :-- |
| ⭐ Glossary `Cloud/external IT service`（ISA2027） | ✅ 逐字：「Cloud services, such as **AI tools ( e.g., AI chatbots, AI agents)**, hosting, web services such as anti-virus dashboards, SIEM services provided by external companies, etc.」 |
| ⭐ 1.3.3（must） | ✅ 逐字全中，⭐ 含两个子项与「+ The external IT services have been harmonized with the protection need of the processed information assets.」 |
| ⭐ 1.3.3 Objective | ✅ 逐字：「This is particularly common with IT services available online at little to no cost, as users may be able to obtain these services without following proper approval processes that consider information security.」 |
| ⭐ 6.1.1（very high） | ✅ 逐字：「…demonstrated by a third party audit (**an adequate TISAX label or equivalent**) or an adequate supplier audit covering agreed and applicable customer requirements. If an audit was not conducted, a **risk-based decision must be made by the organization's management**…A record of this decision exists. (C, I, A)」 |
| ⭐ 5.1.2（very high） | ✅ 逐字：「Information is transported or transferred in **content-encrypted form**. (C)」 |
| ⭐ 5.3.4（must） | ✅ 逐字 |
| ⭐ 6.1.2（must） | ✅ 逐字：「Valid non-disclosure agreements are concluded **prior to** forwarding sensitive information.」 |

⭐ **机械对拍复现**：`isa6-en.xlsx` 中 `\bAI\b` / `artificial intelligence` / `machine learning` / `\bLLM\b` → **0 / 0 / 0 / 0** ✅；`isa2027-en.xlsx` → **3 / 0 / 0 / 0**，⭐ 而那 3 次 `AI` **全部落在同一个 Glossary 单元格内**（⭐ "AI tools"、"AI chatbots"、"AI agents"）—— ⭐ 故 ledger 的「⭐ 仅命中 **1** 次」按**单元格**计 ✅ 成立，⛔ 按词次计应为 3，⛔ 口径需注明。

⭐ **版本事实亦全部复现**：⭐ `isa6-en.xlsx` 内部版本戳确为 **`6.0.3 | 2023-04-12`** ✅，⭐ 而 ENX 下载页把同一文件标为「ISA 6.0.3 (English) ISA **2024-04-25**」✅ —— ⭐ **ledger 记录的这处不一致真实存在，⭐ 且它选择如实记录而非弥合，⭐ 处理正确**；⭐ `isa2027-en.xlsx` 内含 `2026-07-01` ✅，⭐ ENX 页逐字「ISA2027 will be the basis of TISAX Assessments ordered from 2027」「assessments ordered before **2027-01-01** can still be performed with ISA6」✅ —— ⭐ ledger 的「⭐ 2026-07-01 发布 / ⭐ 适用于 2027-01-01 起下单」✅ 准确。⚠️ ⛔ 一处新事实：⭐ ENX 的 redline 说明写的是「between ISA2027 and **ISA 6.0.1**」，⛔ 与下载项标注的 6.0.3 不同名，⛔ 无实质影响。

### 3.3 ⭐⭐ Angermeir 的内容断言 —— ⭐ 全部逐字命中

⭐ 入口：`curl https://arxiv.org/pdf/2510.25506v3` → `pdf_extractor -m text`。

| 断言 | 结果 |
| :-- | :-- |
| ⭐ 85 篇 → 18 篇 → 5 篇 → **0 篇完全复现** | ✅ 摘要逐字：「we studied the **85 articles**…published at ICSE 2024 and ASE 2024. Of the 85 articles, **18** provided research artefacts and used OpenAI models…Of the 18 studies, only **five** were sufficiently complete and executable. For **none of the five** studies, we were able to fully reproduce the results. Two studies seemed to be partially reproducible, and three studies did not seem to be reproducible.」 |
| ⭐ 「唯一 LLM 特异的失败因素是模型弃用」 | ✅ 逐字：「**The only factor directly linked to LLMs was the usage of deprecated models, an issue exclusive to commercial models.**」 |
| ⭐ 「开源模型被弃用的门槛更高」 | ✅ 逐字：「the hurdles towards deprecation for open source models are higher, and such models do not frequently get discontinued as opposed to commercial models.」 |
| ⭐ 「逐字推荐开源模型作缓解」 | ✅ 逐字：「One way of dealing with model deprecation of commercial providers could hence be the comparison with open-source models.」 |
| ⭐ 「43 of 85 articles compared multiple LLMs」 | ✅ 逐字；⭐ 且 counterarguments §4.1 与 §7.3 项 12 的自我提醒**正确**：⛔ 原文确实**没写 42/85**。⚠️ ⭐ 另注：⭐ 原文另有一句「half of the 85 articles did **not perform a comparison with open source models**」——⛔ 那是**另一个量**，⛔ 不可与 43/85 混用 |

⚠️ ⛔ **一处措辞压缩**：[SUMMARY.md](./SUMMARY.md) §3 表写「⛔ **85 篇 0 篇完全复现**」。⭐ 字面为真（⛔ 85 篇里确实 0 篇被完全复现），⛔ 但那个 0 的**实际分母是 5 篇被尝试**；⭐ counterarguments §3 把链条 85→18→5→0 写全 ✅。

### 3.4 ⭐⭐ Abdulkarim（arXiv:2604.00275）—— ⭐ 全部命中，⭐ 且**结清了 small_model_papers 的第 14 项待核**

⭐ 入口：`curl https://arxiv.org/pdf/2604.00275` → `pdf_extractor -m text`。

| 断言 | 结果 |
| :-- | :-- |
| ⭐ 作者 / 单位 / 日期 | ✅ Samer Abdulkarim, Evan Boyd, Karl Bridi, Alec Tufenkjian, **Boqi Chen**, **Gunter Mussbacher**；⭐ 首页逐字「†Electrical and Computer Engineering, **McGill University**, Montreal, Canada」✅；⭐ Submitted **31 Mar 2026** ✅；⛔ 无 journal-ref / DOI → ⭐ preprint 判定 ✅ |
| ⭐ **Claude 3.5 Sonnet 四个 $F_1$**：0.7029 / 0.5026 / 0.3052 / 0.6336 | ✅ 全中（**Table VI**，⭐ 文件行 816–822） |
| ⭐ **GPT-4o 四个 $F_1$**：0.5431 / 0.6260 / 0.3735 / 0.6559 | ✅ 全中（**Table IV**，⭐ 文件行 715–721） |
| ⭐ Table IV = GPT-4o overall / Table VI = Claude overall | ✅ 表号与内容对应正确 |
| ⭐ 「may interfere with the inherent step-by-step reasoning process of reasoning LLMs」 | ✅ 逐字（⭐ 行 823–826） |
| ⭐ 「the strict post-processor module for HTML tables may suppress valid LLM outputs that are not fully compliant, hence influencing the final result」 | ✅ 逐字（⭐ 行 858–860） |
| ⭐ 精度换召回：0.7130→0.6562 / 0.4501→0.6268 | ✅ 全中（Table IV） |
| ⭐ n = 8、来自本科建模课 | ✅ 逐字「of eight examples is a limitation. While these examples vary in complexity, they come from an undergraduate modelling course」 |
| ⭐ Claude 3.5 Sonnet 被作者归为 reasoning | ✅ 逐字「one **reasoning-focused** LLM (Claude 3.5 Sonnet) and one non-reasoning LLM (GPT-4o)」—— ⭐ 两处文件对此的「⛔ 自造口径、⛔ 不得引作定律」限定**准确** |
| ⭐⭐ **shot 数「自相矛盾」是否真实** | ✅ **真实存在，⭐ 该待核项可结案**。⛔ 两处逐字并列如下 |

⭐ 两处逐字（⭐ 依仓库 §3.8 回原文）：

- ⭐ 框架定义节（⭐ 行 219–220）：「**Single-Prompt Baseline** is a generation strategy with a **2-shot** technique in which the full task is provided to the LLM in a single step.」
- ⭐ 实验设置节（⭐ 行 497–501）：「We use a **2-shot** prompting strategy by selecting two examples from a pool of three state machines…**for our multi-step generation strategies**. **For our single-prompt strategy we employ 3-shot prompting**, adding another ground truth state machine, ChessClock, to our pool, **aiming to improve upon the baseline accuracy**.」

⭐ **裁定**：⛔ 两处对**同一个策略**（Single-Prompt Baseline）给出 **2-shot / 3-shot** 两个数，⛔ 矛盾成立。⭐ 因此 [small_model_papers.md](./small_model_papers.md) §4.1 限定 2「⭐ 基线被有意加强」按**实验设置节**成立（⭐ 原文自陈 "aiming to improve upon the baseline accuracy"），⛔ 而框架定义节与之冲突。⭐ 该文件把它标为「⛔ 待核验」是恰当的谨慎，⛔ 现在可以定案。

### 3.5 ⭐ 题录与元数据（⭐ 75 条）

⭐ **21 个 DOI 经 Crossref content negotiation 全部解析成功（⛔ Angermeir 那条除外，⭐ 见 §1.1）**，⭐ 且标题 / venue / 页码与文件所写一致：

| DOI | 核实要点 |
| :-- | :-- |
| ⭐ `10.1145/3786583.3786869` | ⭐⭐ **Fares & Herbold, ICSE-SEIP 2026, pp. 248–258** ✅ —— ⭐ mde §4.2 完全正确 |
| ⭐ `10.1145/3701625.3701675` | ⭐⭐ **Falcão / Canedo, SBQS 2024, pp. 373–382, 2024-11-05** ✅ —— ⭐ mde §4.1 完全正确 |
| ⭐ `10.1109/SANER64311.2025.00070` | ⭐ Caumartin 等 6 人，**SANER 2025, pp. 681–692** ✅ |
| ⭐ `10.1145/3773287` | ⭐ Zhong 等 7 人，TOSEM ✅（⚠️ ⭐ Crossref issued = **2026-07-11**，pp. 1–41；⛔ 两份文件均标 2025，⭐ 属 online-first 与正式卷期的差异，⛔ 引用时宜注明） |
| ⭐ `10.1007/978-3-032-21423-2_23` | ⭐ Chou / Aydemir / Dalpiaz，**REFSQ 2026 LNCS, pp. 336–351** ✅ |
| ⭐ `10.1109/MODELS-C68889.2025.00061` | ⭐ Hachm 等，**pp. 421–431** ✅ |
| ⭐ `10.1145/3640310.3674091` | ⭐ Text2VQL，**MODELS 2024, pp. 13–24** ✅ |
| ⭐ `10.1109/MODELS-C68889.2025.00082` | ⭐ *LLM-enabled Instance Model Generation*，pp. 586–595 ✅ |
| ⭐ `10.1145/3715754` | ⭐ *Demystifying LLM-Based Software Engineering Agents*，**PACMSE, pp. 801–824** ✅ |
| ⭐ `10.1145/3639476.3639764` | ⭐ *Breaking the Silence*，**pp. 102–106** ✅ |
| ⭐ `10.1145/3697010` | ⭐ *An Empirical Study of the Non-Determinism of ChatGPT in Code Generation*，TOSEM ✅ —— ⭐ counterarguments「⛔ arXiv 初版题名不同，⭐ 引用用 TOSEM 定名」✅ 处理正确 |
| ⭐ `10.1145/3771933` · `10.1145/3796239` · `10.1145/3733599` · `10.1109/TSE.2025.3553363` · `10.1109/TSE.2025.3625121` · `10.1109/TSE.2025.3632508` · `10.1109/TSE.2025.3581062` | ✅ 标题与 venue 全部吻合（⭐ TSE 三条页码分别 1455–1471 / 155–170 / 86–99；⭐ RepairLLaMA 2366–2380） |
| ⭐ `10.1145/3658644.3690283` | ⭐ CCS 2024 Klemmer 等 13 人，pp. 2726–2740 ✅ |
| ⭐ `10.1109/SANER60148.2024.00041` | ⭐ Karmarkar 等 4 人，**SANER 2024, pp. 337–348** ✅ —— ⭐ 与 se_motivation_survey §References [16] 完全一致 |
| ⭐ `10.1109/RE.2017.29` · `10.1007/978-3-642-29044-2` · `10.5281/zenodo.12742459` · `10.1145/3708035.3736091` · `10.1145/3695988` · `10.1007/s10664-026-10919-y` | ✅ 全部解析且题名吻合（⭐ PURE / Wohlin 2012 / Text2VQL artifact / PEARC'25 / Hou TOSEM SLR / Falcão EMSE 2026） |

⭐ **42 个 arXiv ID 全部存在且题名吻合**（⛔ 例外仅 §1.7 的 2607.03691）。⭐ 其中有独立价值的元数据核实：

| arXiv | 核实要点 |
| :-- | :-- |
| ⭐ **2510.21443** | ⭐ 作者 Zadenoori, De Martino, Dabrowski, **Xavier Franch, Alessio Ferrari**；⛔ 无 comments / journal-ref；⛔ DBLP 仅 `Informal and Other Publications` / **CoRR 2025** → ⭐⭐ **「纯 preprint」判定证实** ✅（⭐ mde §4.2 与 verification_log §V1 均正确） |
| ⭐ **2511.11125** | ⭐ comments 逐字「Submitted to…ICSE…SEIP 2026」；⭐ HTML 页眉逐字「DOI: **XXXXXXX.XXXXXXX** Conference: The **48th** International Conference on Software Engineering – Software Engineering in Practice; April 12–18, **2025**; Rio De **Janieiro**, BR ISBN: **978-1-4503-XXXX-X/2018/06**」+「**2018©**, 2018」→ ⭐⭐ **mde §4.2 对该页眉的全部描述逐项证实** ✅；⭐ 且「48th + Rio + April 12–18 对应的是 ICSE **2026**」经 Angermeir camera-ready（⭐「48th International Conference on Software Engineering (ICSE '26), April 12–18, 2026…Rio de Janeiro」）与 Crossref 容器名（⭐「IEEE/ACM **48th** International Conference on Software Engineering」）**双重印证** ✅ |
| ⭐ 2312.08055 | ⭐ 作者 June Sallou, Thomas Durieux, Annibale Panichella；⭐ comments「Accepted at the ICSE'24 conference, NIER track」✅ —— ⭐ counterarguments「⭐ 标题、作者、年份、venue 全部属实」✅ |
| ⭐ 2508.15503 | ⭐ 作者含 **Sebastian Baltes, Florian Angermeir**…；⭐ comments「86 pages, 4 tables, **accepted in Empirical Software Engineering**」✅ —— ⭐「EMSE 已接收」✅ |
| ⭐ 2604.24678 | ⚠️ ⭐ comments「**Accepted at EASE'26**」——⛔ se_motivation_survey 标「⚠️ arXiv preprint」已过期 |
| ⭐ 2606.04739 | ⚠️ ⭐ comments「**Accepted at AI&CCPS 2026 workshop**」；⭐ 题名实为 *Revisiting Vul-RAG: **Reproducibility and Replicability** of RAG-based Vulnerability D…* |
| ⭐ 2509.12395 | ⭐ 作者 Yash Mundhra, Max Valk, **Maliheh Izadi**；⭐ comments 确认 ASE 2025 ✅ |
| ⭐ 2510.23055 | ⭐ 作者含 **Alessio Ferrari** ✅ |
| ⭐ 2512.12063 / 2410.23657 / 2509.15283 / 2402.16480 / 2311.00889 / 2510.04519 / 2405.06371 / 2405.12195 / 2503.22587 / 2509.11446 / 2505.16590 / 2412.02789 | ✅ 作者、录用自述、题名全部与文件所写一致 |
| ⭐ 2305.02301 / 2305.07766 / 2310.10508 / 2408.03680 / 2405.00732 / 2409.03454 / 2510.18787 / 2308.08747 / 2509.20758 / 2307.09009 / 2209.11515 / 2206.01962 / 2411.17501 / 2601.01954 / 2601.09695 / 2601.19239 / 2604.05481 / 2606.16886 / 2503.17998 | ✅ 全部存在、题名与作者吻合；⭐ 其中 2305.02301「Accepted to Findings of ACL 2023」✅、⭐ 2310.10508「Accepted in 22nd International Conference on Mining Software Repositories」= MSR 2025 ✅、⭐ 2408.03680「Accepted by FSE 2025」✅、⭐ 2509.20758「Accepted by ICLR 2026」✅、⭐ 2510.18787 EASE ✅、⭐ 2601.01954「To be published at The 3rd ACM International Conference…」= FORGE 2026 ✅ |

⭐ **另核对并全中的两条内容断言**：

1. ⭐⭐ **arXiv:2404.06371（Ferrari / Abualhaija / Arora）—— ⭐ counterarguments §2.2 ② 三个要点全部逐字命中**（⭐ 我下载 PDF 提取后逐行读，⭐ 因为摘要页看不到这些）：⭐「In our evaluation, we did not use a manually defined ground truth for two reasons: **(a) more than one diagram exists that satisfies the same requirements; (b) existing ground truths are limited**」✅；⭐「A1 inspected and scored 15 of the diagrams produced by A2, and vice versa—**a total of 30 models were cross-evaluated**」✅；⭐「computed through a **square-weighted Cohen's Kappa** [34], led to **κ=0.67**, indicating substantial agreement」✅。⚠️ ⭐ 一处需注明：⭐ 该文做的是**需求 → UML 序列图**，⛔ 不是类图或状态机。
2. ⭐ **arXiv:2411.17501（Stroebl）逐字句属实** ✅：⭐「Therefore, **no amount of inference scaling of weaker models can enable them to match the single-sample accuracy of a sufficiently strong model.**」（⛔ 机制归类问题见 §1.9）

### 3.6 ⭐ 内部引用与内部数字

⭐ 五条跨目录相对路径**全部存在** ✅：[route_selection_and_v47_plan.md](../../discover_matrix/docs/findings/route_selection_and_v47_plan.md)、[x1v2/verdicts.md](../../baseline_arm/docs/generations/x1v2/verdicts.md)、[assertion_output_form_evidence.md](../assertion_output_form_evidence.md)、[../../story/](../../story/)、[ground_truth_limitations.md](../../discover_matrix/docs/protocol/ground_truth_limitations.md)。

⭐ **SUMMARY §6 的「🟢 151 / 🟡 36 / 🔴 37 / ⚪ 12」与 regulatory_ledger 的 emoji 实数完全一致** ✅（⭐ `python3 -c "t=open('regulatory_ledger.md').read(); [print(e,t.count(e)) for e in ['🟢','🟡','🔴','⚪']]"` → 151 / 36 / 37 / 12）。⚠️ ⛔ 但请注意口径：⭐ 这是 **emoji 出现次数**，⛔ 不等于「条法规」——⛔ 同一条款在总览表与分节表各出现一次即计两次。

⭐ **mde §1.1 题录总数列加总 = 1,455** ✅ 与自陈一致（⛔ LLM 列不闭合，⭐ 见 §1.4）。

⭐ **60.4% / 76.2% / 93 位 / 15.82pp 四个数互相闭合** ✅（⛔ 限定缺失见 §1.11）。⭐ **79% token** 亦在 [discover_matrix/docs/findings/README.md](../../discover_matrix/docs/findings/README.md) 中标为 **M 级**（⭐ 读 `telemetry`）✅。

---

## 4. 跨文件矛盾裁定

> ⛔ 依仓库 [CLAUDE.md](../../../../CLAUDE.md) §3.8：⭐ 每条都回原文取两处**完整逐字**，⛔ 再裁定；⛔ 并区分「⛔ **不存在**」（⛔ 指控本身不成立）与「⭐ **已消解**」（⭐ 曾经成立过）。

### 4.1 ⭐ arXiv:2511.11125 的录用状态 —— ⭐ **矛盾真实存在，⭐ mde 正确，⛔ se_motivation_survey 未回写**

**两处逐字原文**：

- [se_motivation_survey.md](./se_motivation_survey.md) §1.2 表第 30 行 venue 格：「⚠️ **arXiv preprint**；作者自述「Submitted to ICSE SEIP 2026」，⛔ **未见录用证据**」；⭐ 同文件 §6.3 待核项 4：「⛔ [2511.11125](https://arxiv.org/abs/2511.11125)（RAPID）是否真被 ICSE SEIP 2026 录用 | ⛔ arXiv comments 只说「Submitted」；⛔ 页眉的「48th ICSE, April 2025, Rio」是**未改的模板串**，⛔ 不可当录用证据」
- [mde_re_venue_scan.md](./mde_re_venue_scan.md) §4.2 表第 3 行：「**2511.11125**（RAPID Programs） | ⭐ **已正式录用** | **ICSE-SEIP 2026**, pp. 248–258, DOI `10.1145/3786583.3786869`，DBLP `conf/icse-seip/FaresH26` | ⭐ DBLP 会议条目 + ACM proceedings DOI 同族」

**裁定：⭐ mde 正确。** ⭐ `curl -H "Accept: application/vnd.citationstyles.csl+json" https://doi.org/10.1145/3786583.3786869` 返回 **HTTP 200**，⭐ 内容为：title = *Utilizing LLMs for Industrial Process Automation: A Case Study on Modifying RAPID Programs*；container = *Proceedings of the IEEE/ACM **48th** International Conference on Software Engineering: **Software Engineering in Practice***；page = **248-258**；issued = **2026-04-12**；author = **Fares Salim; Herbold Steffen**。⭐ 全部字段吻合。

⭐ **性质：不是「已消解」，是「已定位但未回写」。** ⛔ mde §4.2 末尾已明写「⭐ 对 [se_motivation_survey.md](./se_motivation_survey.md) 的回写建议…⛔ 第 30 行 Fares & Herbold 那条应从「未见录用证据」改为 **ICSE-SEIP 2026 已录用**」，⛔ 但 se_motivation_survey 文本未动。⛔ 于是仓库里同时存在两个相反陈述。

⭐ **顺带裁定同一表内的第三行**：⭐ **arXiv:2412.02789** —— se_motivation_survey §1.2 与 §References [4] 写「⚠️ arXiv preprint（2024-12-03）；⛔ 录用状态待核验」，⭐ mde §4.2 写「⭐ **已正式录用** … SANER 2025, pp. 681–692」。⭐ **mde 正确**：`10.1109/SANER64311.2025.00070` 解析为 SANER 2025，pp. 681–692，⭐ 作者六人全中。⛔ 同属未回写。

### 4.2 ⭐⭐ Falcão & Canedo 是否可引 —— ⭐ **矛盾真实存在，⭐ mde 正确，⛔ se_motivation_survey 未回写**

**两处逐字原文**：

- [se_motivation_survey.md](./se_motivation_survey.md) §4 表末行：「⛔⛔ **仅见二手引用（一篇 *Behaviour & Information Technology* 文章中的转述）；⛔ 未找到一手来源、⛔ 未确认标题与 venue、⛔ 未读任何原文。⛔ 全条待核验，⛔ 不得引用**」；⭐ 同文件 §References [20]：「⛔ **待核验，不得引用。** Falcão, ?, Canedo, E. D.（?）(2024). *（标题未知）* …⛔ 未找到一手来源、⛔ 未确认标题、venue、DOI **或其是否真实存在**。」；⭐ §6.3 待核项 1 优先级标「⛔ **最高**」
- [mde_re_venue_scan.md](./mde_re_venue_scan.md) §4.1 标题：「⭐⭐ Falcão & Canedo「78 人调查」：⭐ **一手来源找到了，⛔ 前一轮的「查无一手」应当撤销**」；⭐ 其完整题录：「Falcão, Fabiano Damasceno Sousa; Canedo, Edna Dias. *Investigating Software Development Teams Members' Perceptions of Data Privacy in the Use of Large Language Models (LLMs)*. In **Proceedings of the XXIII Brazilian Symposium on Software Quality (SBQS 2024)**…ACM, pp. **373–382**. DOI [10.1145/3701625.3701675]」

**裁定：⭐ mde 正确，⭐ 该论文真实存在。** ⭐ `curl -H "Accept: application/vnd.citationstyles.csl+json" https://doi.org/10.1145/3701625.3701675` 返回 **HTTP 200**：title = *Investigating Software Development Teams Members' Perceptions of Data Privacy in the Use of Large Language Models (LLMs)*；container = *Proceedings of the XXIII Brazilian Symposium on Software Quality*；page = **373-382**；issued = **2024-11-05**；author = **Falcão Fabiano Damasceno Sousa; Canedo Edna Dias**。⭐ 与 mde 所写**逐字段吻合**。⭐ 我另独立核实同一对作者的后续工作 `10.1007/s10664-026-10919-y`（⭐ EMSE 2026）亦存在 ✅。

⭐ **性质：已定位但未回写。** ⛔ se_motivation_survey 仍在最高优先级待核项里印着「⛔ 未确认…**或其是否真实存在**」与「⛔ 不得引用」。

### 4.3 ⭐⭐ VDA ISA 目录是否可得、⛔ 其条文能否引 —— ⭐ **矛盾真实存在，⭐ regulatory_ledger 正确，⛔ counterarguments 错**

**两处逐字原文**：

- [regulatory_ledger.md](./regulatory_ledger.md) §2.7：「**版本事实（🟢 官方 XLSX 已下载逐格核验）**：⭐ 当前生效目录是 **VDA ISA 6.0.3**（文件 `isa6-en.xlsx`，ENX 下载页标注 2024-04-25…）」；⭐ 同节 §4.2 检索链路表：「TISAX / VDA ISA | `portal.enx.com` 官方 XLSX | ⭐ 下载 `isa6-en.xlsx` 与 `isa2027-en.xlsx`，⭐ 解 `sharedStrings.xml` 逐格比对」
- [counterarguments.md](./counterarguments.md) §7.2 表末行：「BMB17 / GJB 系列 · 军工审查标准 · **VDA ISA 目录** · NSA "Raise the Bar" | ⛔ **不公开 / 需资质 / 需注册** | ⛔ 一律不引条文内容」

**裁定：⭐ regulatory_ledger 正确。** ⭐ 复算入口与结果：`curl -sSL https://portal.enx.com/en-US/TISAX/downloads/` → **HTTP 200**，⛔ 无鉴权、⛔ 无 CAPTCHA，⭐ 页面直接列出 `/isa2027-en.xlsx`、`/isa6-en.xlsx`、`/isa2027-en_redline.xlsx`、`/isa6-en_redline.xlsx`；⭐ `curl https://portal.enx.com/isa2027-en.xlsx` 与 `.../isa6-en.xlsx` 均 **HTTP 200**（⭐ 244,910 B / 265,000 B）。⭐ 我据此逐条比对了 ledger 引的**七条**控制项文本，⭐ **七条全部一字不差**（⭐ 明细见 §3.2）。

⛔ **性质：counterarguments 那一格是错的（⛔ 不是「已消解」，⛔ 是从一开始就不成立）。** ⚠️ ⭐ 需分清两件事：⭐ counterarguments §1.2「⛔ 别用 TISAX 禁止用云」这一**结论**（⛔ 无禁令、⛔ 反向证据成立）与 ledger §2.7「⭐ 不是禁止，⭐ 是准入摩擦」**完全一致**，⛔ 二者不冲突；⛔ 冲突只在 §7.2 那句「⛔ 不公开 / 一律不引条文内容」的**可得性判断**上。

### 4.4 ⭐ mde 内部：Text2VQL / Chou et al. 是「装饰」还是「未判定」 —— ⭐ **矛盾真实存在（⛔ 同一文件内）**

⭐ 两处逐字原文与影响见 §1.14。⭐ **裁定：无法从文件本身消解**，⛔ 因为两处都是该文件的自陈，⛔ 且指向互斥的两种状态。⭐ 从证据看，⭐ §2.2 / §2.3 确实都写了「⭐ 读到什么程度：**全文**」并给出了我方独立复算的词频表，⭐ 故「装饰」这一侧的证据链更完整；⛔ 但 §3.2 的净命中拆分与标题的 ⏳ 必须与之对齐，⛔ 否则「MDE/RE 侧承重 = 0」的构成方式说不清。

### 4.5 ⚠️ 「ledger 说 ISA 可引 vs counterarguments 说 IEC 62443 不可引」 —— ⛔ **指控不存在**

⭐ 我在扫描时怀疑这两处冲突，⛔ 回原文后判定**不存在**，⭐ 如实记录以免后人重复怀疑：

- [regulatory_ledger.md](./regulatory_ledger.md) §1.5b 明写「⛔ **条文未核验。** §5.9.1（Requirement）与 §5.9.2（Rationale and supplemental guidance）的正文落在付费墙内…⛔ **不得写成「IEC 62443-4-1 要求不得把设计数据发给第三方」**」
- [counterarguments.md](./counterarguments.md) §1.2 末段：「⭐ IEC 62443-3-3:2013 范围确含 zones/conduits 与 security levels，⛔ **但全文付费（CHF 380）未取得**，⛔ 不得引用任何条文编号或条文内容」

⛔ 两处说的是**不同的分册**（4-1 vs 3-3），⭐ 且**结论方向一致**（⛔ 都要求不引条文内容）。⭐ 我另核实：⭐ IEC 62443-4-1 preview 中 §5.9 / §5.11 / §5.12 的**目录标题与页码确实可见**（⭐ p.23–24），⛔ 条文正文确实不在 —— ⭐ 故 ledger 的「🟢 目录 / 🔴 条文」双标是准确的分级，⛔ 不是自相矛盾。

---

## 5. 核验方法与访问受限记录

### 5.1 ⭐ 方法

| 环节 | 做法 |
| :-- | :-- |
| ⭐ 法规原文 | ⭐ eCFR 官方 **versioner XML API**（`/api/versioner/v1/full/2026-08-01/title-NN.xml?part=..&section=..`）；⛔ `renderer/v1/content/enhanced` 端点返回 **0 字节**，⛔ 已弃用改走 versioner。⭐ acquisition.gov / eur-lex CELEX / npc.gov.cn / gov.cn / cac.gov.cn / gjbmj.gov.cn / mofcom / most.gov.cn 直 `curl` + 剥标签 + 多编码解码（utf-8 → gb18030） |
| ⭐ 标准 preview | ⭐ iTeh CDN 与 NSAI 样张 `curl` 下载 → `python -m tools.pdf_extractor -m text` → `grep` |
| ⭐ 题录 | ⭐ **Crossref content negotiation**（`Accept: application/vnd.citationstyles.csl+json` 打 `doi.org`）作为 DOI 存活性与字段的判据；⭐ **DBLP 官方镜像** `dblp.uni-trier.de/search/publ/api?format=json` 判 preprint / 正式发表；⭐ arXiv `abs` 页正则抽 title / authors / dateline / comments / journal-ref |
| ⭐ 论文内容断言 | ⭐ 下载 `arxiv.org/pdf/<id>` → `pdf_extractor -m text` → 逐行读，⛔ **不用摘要页代替正文**（⭐ Ferrari 的 κ=0.67 与 Abdulkarim 的 shot 数矛盾都只在正文里） |
| ⭐ XLSX | ⭐ `zipfile` 解 `xl/sharedStrings.xml` → 剥 XML → `html.unescape` → 逐串比对 |
| ⛔ 裁定 | ⛔ 全部由我亲自读原文完成；⛔ 机械检索只用于**定位**。⛔ 凡「两处说法相反」类指控，⭐ 一律先把两处完整段落取出（`grep -n` 定位 + 读上下文）再判 |

### 5.2 ⛔ 访问受限记录（⛔ 不得据此断言事实不存在）

| 目标 | 异常 | 影响 |
| :-- | :-- | :-- |
| ⛔ **`www.war.gov`**（⭐ GenAI.mil 三条新闻稿） | ⛔ **HTTP 403**，⛔ `curl`（含桌面 UA）与 WebFetch 均被拒 | ⛔ SUMMARY §2.1 反证 1 与 ledger §2.6「⛔ 最致命的一击」表的**四句逐字引文全部未能一手核实**（⭐ 见 §2 项 2） |
| ⛔ **ACM DL**（`dl.acm.org`） | ⛔ 未尝试（⭐ 三份文件均已记录其 403） | ⛔ Angermeir 的 ICSE'26 归属无法从出版方侧确认 |
| ⛔ `conf.researchr.org/search/icse-2026/*` | ⚠️ ⛔ 返回 200 但**零结果且无结果容器**，⛔ 疑 JS 渲染 | ⛔ 零结果**不作为**「未录用」的证据 |
| ⛔ `www.cac.gov.cn/2025-10/28/c_1766116893531860.htm`（⭐ 我推测的决定页 URL） | ⛔ **404** | ⭐ 已改由中国人大网决定全文与中国政府网转载核实 2026-01-01 施行 ✅ |
| ⛔ `openstd.samr.gov.cn`（GB/T 22239-2019） | ⛔ 未尝试（⛔ JS 渲染页，⭐ ledger 已自陈） | ⛔ 该族条款号仍为 🟡，⛔ 需人工复核 |
| ⛔ 各标准付费墙正文 | ⛔ preview 之外 | ⭐ 见 §2 项 5；⭐ ledger 对此的 🔴 标注**处理正确**，⛔ 无需改动 |

### 5.3 ⭐ 一条方法论提醒（⭐ 本轮实际栽过）

⭐ 在 EASA PDF 上 `grep "double development"` 得到 **0 命中**，⛔ 差点据此判定「⛔ 该引文不存在」。⭐ 实际 PDF 文本层把它断成 **`doub le development`**（⛔ 跨行连字或字距导致的空格插入）。⭐ 正确做法是先 `re.sub(r'\s+',' ',t)` 归一再查，⛔ 或按短语两端各查一半。⭐ 这与 [mde_re_venue_scan.md](./mde_re_venue_scan.md) §5.2 记录的合字（`conﬁdentiality`）陷阱是同一类问题：⛔ **凡在 PDF 文本上做「出现 0 次」断言，⛔ 必须先做空白归一 + 合字归一 + 去跨行连字符三步。**
