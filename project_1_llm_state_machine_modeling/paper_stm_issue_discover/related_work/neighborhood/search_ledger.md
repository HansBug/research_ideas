# L3 检索台账

⭐ 本文件是**覆盖面的证据**，⛔ 不是候选清单（那在 [SUMMARY.md](./SUMMARY.md) 与 [cards/](./cards/)）。⭐ 它回答两个问题：**我们查了哪些门** · ⛔ **哪些门没查、为什么**。

---

## 0. ⛔ 三态口径（⭐ 全库统一）

| 记法 | 含义 |
| :-- | :-- |
| `n` | 跑了，命中 n 条 |
| `0` | ⭐ **跑了，0 命中** |
| `— 没跑` | ⛔ 本轮未对该组合发出任何查询 |
| ⚠️ **访问异常** | ⛔ WAF / 403 / 429 / CAPTCHA / SPA 壳 / 配额耗尽 —— ⛔⛔ **不得写成 0 命中，⛔ 也不得据此断言该方向为空** |

⭐ 逐条可复跑的查询串在各路的原始台账里（⭐ 主 session 保留于 `/tmp/l3/search/A*_*.md`）；⭐ 本文件只汇总口径与结论。

---

## 1. ⭐ 九路的门与结果

| 路 | 门 | 入口实际走通的 | 查询数 | 题录池 | ⭐ 过两条硬门 | 状态 |
| :-- | :-- | :-- | --: | --: | --: | :-- |
| ⭐ **A1** | arXiv 全量 | arXiv API（⭐ 只用 `abs:`） | 42 | **8930** | **110** | ✅ |
| ⭐ **A2** | **ACM DL** | ⛔ 网页端 Cloudflare 403；⭐⭐ 走 **Crossref `member:320` 全量机械扫** | **105** | ⭐⭐ **191804** | **67**（+78 附录） | ✅ |
| ⭐ **A3** | **IEEE Xplore** | ⭐⭐ **内部 REST API** `POST ieeexplore.ieee.org/rest/search` | **82** | **2384** | **105** | ✅ |
| ⭐ **A4** | 语义检索 | ⚠️ arXiv `abs:` 字段（⛔ OpenAlex 与 S2 双双配额阻断） | **60** | 3475 | **296** | ✅ |
| ⭐ **A5** | 新兴 venue + 漏检四刊 | ⭐ DBLP `stream:` × `year:` **全普查** | 65 格 | **4109** | **12** | ✅ |
| ⭐ **A6** | 本地三库 | 本地 | 14 | **1557** | **38** | ✅ |
| ⭐ **A7** | 引文追踪 | ⚠️ Crossref 后向为主（⛔ OpenCitations 前向 19 个种子返回 0） | 102 | **3644** | **172** | ✅ |
| ⭐ **A8** | 综述驱动 | ⭐ 12 篇综述 + OSF 复现包 | — | — | **37** | ✅ |
| ⭐ **A9** | 工业自动化 / 协议（⭐ 补位） | Xplore REST + DBLP `stream:` + S2 | **158** | **6795** | **86** | ✅ |

⭐ **八路合并去重后 631 条**（⭐ 工具：[`tools/merge_candidates.py`](./tools/merge_candidates.py)）。

### 1.1 ⭐⭐ 重叠分布本身是一条结论

| 被几路捞到 | 条数 |
| :-: | --: |
| 1 | **495** |
| 2 | 90 |
| 3 | 25 |
| 4 | 12 |
| 5 | 3 |
| 6 | 4 |
| 7 | 1 |
| 8 | **1** |

⭐⭐ **八路里只有 1 篇被全部捞到，⭐ 而 495 篇（78%）只有一路捞到。** ⛔ 各路的覆盖**几乎不重叠**。

⭐ **两个推论**：⭐ ① 并行多门是值的，⛔ 不是冗余；⭐ ② **任何单一入口都会漏掉绝大部分** —— ⚠️ 这也反过来解释了 L1 的盲区：⛔ 它只走了 DBLP + OpenAlex 两道门。

---

## 2. ⛔⛔ 访问异常（⭐ 逐条如实登记，⛔ 这些不是 0 命中）

| 入口 | 症状（逐字） | 影响 |
| :-- | :-- | :-- |
| **IEEE Xplore 网页端** | ⚠️ HTTP **200 / 37 KB 但零题录**；剥 `<script>` 后正文只剩 740 字符页脚导航；页面含 Akamai `<APM_DO_NOT_TOUCH>` | ⛔ SPA 壳 + 反爬，⭐ 已换内部 REST API |
| **OpenAlex** | ⛔ `{"error":"Rate limit exceeded","message":"Insufficient budget. This request costs $0.001 but you only have $0.0007 remaining"}`，`retryAfter: 22877` | ⛔⛔ **A3 全程 0 次成功；A4 第 8 个查询起硬 429，33/40 未发出** —— ⚠️ 已改按次计费，免费额约 **10 次/日** |
| **Semantic Scholar** | ⛔ 无 API key 时穷尽 12 次退避（12s→90s）仍 429 | ⛔ **A4 的 19/20 查询未跑通** |
| **DBLP** | ⛔ 前若干组正常，之后**静默 429**（⛔ 空响应体 → `JSONDecodeError: Expecting value: line 1 column 1`） | ⚠️ 部分组未完成 |
| **OSF 网页** | ⚠️ `https://osf.io/g5by9/` 返回 200 ⛔ 但只有 4207 B（SPA 壳） | ⭐ 已改走 API + `?view_only=` token |

---

## 3. ⛔⛔ 会**静默出错**的工具陷阱（⭐ 本轮实测，⛔ 全部不报错）

⭐ 这一节比命中数更重要 —— ⛔ 它决定后续谁能复现我们的覆盖面。

### 3.1 检索侧

| # | 陷阱 | 后果 |
| :-: | :-- | :-- |
| **S1** | ⛔ **DBLP 的 `h` 参数在 `toc:` facet 下封顶 100** | ⛔ 请求 1000 返回 **200 但只给 100 条**，不报错（⭐ L1 移交） |
| **S2** | ⛔ **DBLP 默认对标题做全词 AND** | ⛔ 长查询串必 0 —— ⭐ 那是**工具性零** |
| **S3** | ⛔ **IEEE / Wiley 在 OpenAlex 里按 early-access 年计年** | ⛔ 年份窗会漏（⭐ L1 移交） |
| **S4** | ⛔ **Xplore 的无字段 `queryText` 比字段限定更窄** | ⛔ 10 组自由文本**全部 0 new**；`activity diagram` 与 `Stateflow` 返回 0，⭐ 而同方向字段限定式有 1 和 16 —— ⛔ **这类 0 全是伪影** |
| **S5** | ⛔ **Xplore 跨字段 AND（`Document Title` × `Abstract`）差 117 倍** | ⛔ 1 条 vs 117 条，不报错。⭐ 正确口径 `All Metadata` × `All Metadata` |
| **S6** | ⛔⛔ **只用单数 `"LLM"` 会系统性漏检** | ⭐ 加上 `"LLMs"` 复数 / `"language models"` / `"foundation model"` / 具体模型名后**净补 167 条题录 / 20 条过门候选，含一篇 TSE 2026** |
| **S7** | ⛔ **arXiv 的 `all:` 字段返回与查询词无关的结果** | ⚠️ 实测 `all:UPPAAL AND all:"large language model"` 返回 3 条，⛔ 逐条查摘要**均不含 UPPAAL 也不含 timed automata**。⭐ 只用 `abs:` |
| **S8** | ⛔ **arXiv 无括号时 OR/AND 优先级不按直觉** | ⚠️ 一条查询膨胀到 22304 条 |
| **S9** | ⛔ **Crossref 不支持布尔 AND** | ⚠️ `query.bibliographic` 是模糊排序，名义 total 在 4 万–39 万量级，⭐ 只能扫 ranked top-50 |
| **S10** | ⛔ **两个语义污染词** | ⚠️ `"model inference"`（458 条里 95%+ 是 LLM serving 推理优化）· `"workflow"`（1390 条里几乎全是 LLM agent workflow） |
| **S11** | ⛔ **IEEE 匿名视角索引覆盖不全** | ⚠️ `"Abstract":"large language model"` 全库 2023–2026 只有 **6184**（⛔ 真实量级远高于此）；⭐ 实证：一篇 ISSREW 2024 在 IEEE 三格都没出来，靠 Crossref 捞到 |
| **S12** | ⛔⛔ **ACM DL 网页端是 Cloudflare 交互式挑战** | ⚠️ 5 条内容路径全 **403 + `Just a moment`**；⭐ 而 `robots.txt` 返回 200 —— ⭐ **证明主机可达，403 是 bot 挑战不是站点故障** |
| **S13** | ⛔⛔ **OpenAlex 的 publisher 过滤只看得到 ACM 的 17%** | ⚠️ 实测 **32423 vs Crossref 的 191804** —— ⛔ **漏掉约 83%**。⭐ 应改用 DOI 前缀 `10.1145` |
| **S14** | ⛔ **Crossref 的 ACM 摘要覆盖率只有 17%** | ⚠️ 连 ICSE / ASE 正会论文都是空的 —— ⛔ **基于摘要的门在 Crossref 上根本跑不起来**，⭐ 须另接摘要源 |
| **S15** | ⛔ **Crossref 的 `query.title` / `query.bibliographic` 是 dismax OR 相关度检索，⛔ 不是短语匹配** | ⚠️ `query.title=state machine` 报 5304 条 = 「标题含 state **或** machine 的任意组合」按相关度排 —— ⛔ **总报告数不能读成命中数** |
| **S16** | ⛔⛔ **`\b` 收尾的 LLM 正则会打掉全部复数** | ⚠️ ⭐ **A2 自己写出来的 bug**：`\b(llm\|large language model\|foundation model)\b` 让 `Large Language Models` / `Foundation Models` 一律不匹配。⛔ **实测吃掉 47 条候选**，修正后「仅 LLM 词」池从 8579 涨到 11489 |
| **S17** | ⛔⛔ **arXiv 429 限流被抓取器记成「0 条返回」并照常写盘** | ⚠️ ⭐ **A1 自己踩的**：⛔ 4 个查询产生过**假零**，已删重跑 |
| **S18** | ⛔ **`all:"Event B"` / `all:Alloy` 这类单词化的形式方法名会退化成词项 AND** | ⚠️ 返回量虚高**一到两个数量级** |
| **S19** | ⛔⛔ **DBLP 的 `h` 封顶 100 对*所有* publ API 查询成立，⛔ 不只 `toc:`** | ⚠️ ⭐ A5 实测：⛔ `h=1000` **静默返回 100**，⭐ 而 `@total` 报的是对的 —— ⭐ 必须逐格核 `fetched == total` |
| **S20** | ⛔⛔ **DBLP 的 `journals/cep` 与 `journals/isatrans` stream key 根本不存在** | ⛔ 空查询也 `total=0` —— ⭐ **Control Engineering Practice 与 ISA Transactions 实际未被覆盖**，⛔ 那 6 个 0 **不得当事实读** |
| **S21** | ⛔ **arXiv API 必须 `https://` + `curl -L`** | ⚠️ ⭐ A9 独立复现了主 session 踩过的坑：⛔ `http://export.arxiv.org` 返回 **301 + size=0**，⭐ 第一次被误判成「ID 不存在」 |
| **S22** | ⭐ **Xplore 的 `"Publication Title"` 字段可用且高效**（⭐ 正面经验） | ⭐ 用「场地 × 宽 LLM 词」而非窄主题词，⭐ 能在场地内拿到接近全召回的小池子（⭐ ETFA 三年仅 89 条，⭐ 可逐条人读） |
| **S23** | ⛔⛔ **OpenCitations 的前向引文对 2025–26 论文大面积返回 0** | ⚠️ ⭐ A7 实测：⛔ **19 个种子返回 0**，⭐ 而那些恰是最相关的近年工作 —— ⭐⭐ **那是覆盖为零，⛔ 不是「无人引用」** |

### 3.2 本地与核验侧

| # | 陷阱 | 后果 |
| :-: | :-- | :-- |
| **V1** | ⛔ **`grep -ril 'LLM' sources/*/` 返回 132，⭐ 而真实是 2** | ⚠️ 命中落在**我们自己写的 `DESC.md` 评述**里，不是论文内容。⭐ 收紧到只扫 `paper_content.txt` 且 ≥3 次 → **787 → 2**。⛔ **差两个量级** |
| **V2** | ⛔ **`baselines/SUMMARY.md` 四张论文表列布局不一致** | ⚠️ 只有第 1 段有 Venue / 链接列 —— ⛔ 统一 `awk -F'\|'` 会**把年份读成输入** |
| **V3** | ⛔ **机械抽 DOI 会抽到错的那个** | ⚠️ 实测三例：`pat-agent` 首命中是 **2009 年 PAT 工具原论文**的 DOI；`clarifystl` 首命中是 PDF 里的 ACM 占位串 `doi.org/XXXXXXX.XXXXXXX`；另一篇首命中为空 |
| **V4** | ⛔⛔ **arXiv API 用 `http` 且不带 UA 静默返回空体，退出码仍 0** | ⛔ 任何「解析不到即判不存在」的脚本会把**全部**条目判成假（⭐ 主 session 实际踩过，⭐ 详见 [verification_log.md](./verification_log.md) §1.1） |
| **V5** | ⛔⛔ **DataCite 的 DOI 在 Crossref 上查是「不存在」** | ⛔ Zenodo / figshare / OSF / Dryad 的 DOI 走 **DataCite** —— ⭐ 照搬「Crossref 404 即假 DOI」会把真资产判成伪造（⭐ 详见 `verification_log.md` §1.2） |
| **V6** | ⛔ **匿名 view-only 链接掐掉 query string 必 401** | ⛔ 而 401 与「需要登录」**在状态码上无法区分** —— ⭐ 主 session 因此误判 OSF 复现包不可得 |

⭐⭐ **这 27 条里有 24 条是本轮新踩出来的**（⛔ 只有 1–3 是 L1 移交）；⚠️ ⭐ **其中 2 条（#22 #23）是 agent 自己写的代码里的 bug，⭐ 由它们自己查出并如实上报**。⭐ 它们的共同形态是：⛔ **工具的「没找到」被读成事实的「不存在」。**

---

## 4. ⛔ 本轮**没跑**的（⭐ 如实登记，⛔ 不得当成覆盖过）

| 门 | 状态 | 说明 |
| :-- | :-- | :-- |
| **ACM DL 原生界面** | ⛔ **被 Cloudflare 挡死** | ⭐ 但**已由 Crossref `member:320` 全量机械扫 191804 条题录替代**，⭐ 覆盖比原生界面检索更完整（⭐ 见 S19：⛔ OpenAlex 的 publisher 过滤只看得到 17%） |
| **Scopus · Web of Science** | ⛔ **没跑** | ⛔ 需机构订阅 |
| **OpenAlex 完整轮** | ⚠️ **配额阻断** | ⛔ A3 全程 0 次成功、A4 33/40 未发出。⭐ L1 已独立做过一轮 OpenAlex，故损失有限 |
| **Semantic Scholar 完整轮** | ⚠️ **配额阻断** | ⛔ A4 的 19/20 未跑通 |
| **Google Scholar** | ⛔ **没跑** | ⛔ 无稳定程序化入口 |

---

## 5. 更新日志

| 时间 | 动作 |
| :-- | :-- |
| 2026-08-13 | 建档。⭐ **九路全部完成**，⭐ 合并去重 **631** 条。⭐ 记 **27 条**静默陷阱（⛔ 其中 3 条是 agent 自己代码里的 bug 并自查上报）与 5 类访问异常。⛔ 登记 3 类实际未覆盖：Scopus/WoS · OpenAlex/S2 配额 · **CEP 与 ISA Transactions（DBLP stream key 不存在）** |
