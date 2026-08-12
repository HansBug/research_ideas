# 核验日志

⭐ 本文件记录主 session **亲自复核** subagent 产出的每一次动作与结果，⛔ 包括复核**失败**和**复核推翻了 agent 说法**的情形。

⛔ **为什么单开一份。** ⚠️ L2 的教训：一个 Crossref 404 的**假 DOI** 随着一条**已通过对抗裁定**的证据进入了正式结论 —— ⭐ 根因是**裁定层只判意思对不对，不核验引用是否存在**。⭐ 本文件就是那一层缺失的补丁：⛔ 凡是要进 [SUMMARY.md](./SUMMARY.md) 的数字与引用，⭐ 都要在这里留一条可复跑的核验记录。

⭐ **命令一律逐字给出，可复制重跑。**

---

## 1. ⛔ 工具自身的坑（⭐ 先记这个，否则下面的结果读不懂）

### 1.1 ⛔ arXiv API 用 `http` 且不带 UA 会**静默返回空**

初次核验 7 个 arXiv id **全部报「无此 id」**。⛔ 这是**工具坏了**，⛔ 不是 7 条全假。

```bash
# ⛔ 坏的：空响应，退出码仍是 0
curl -s "http://export.arxiv.org/api/query?id_list=2509.24782"        # → 0 字节

# ⭐ 对的：https + UA
curl -sL -A "Mozilla/5.0 (research-check)" \
  "https://export.arxiv.org/api/query?id_list=2509.24782"
```

⚠️⚠️ **这是一个静默失败**：⛔ `curl` 退出码 0、⛔ 无报错、⛔ 只是响应体为空，⭐ 于是任何「解析不到就判不存在」的脚本都会把**全部**条目判成假。

⭐⭐ **判别启发式（⛔ 值得记住）：**⭐ **当一批核验「全灭」时，先怀疑工具，⛔ 再怀疑数据。** ⭐ 真实的伪造是零散的（L2 那次是 183 条里 1 条），⛔ 整齐划一的失败几乎总是工具问题。

### 1.2 ⛔⛔ **DataCite 的 DOI 在 Crossref 上查是「不存在」** —— ⭐ 看起来与伪造一模一样

⭐ 核 `10.5281/zenodo.19819244`（一份 Zenodo 数据集）时，Crossref 返回**查不到**。⛔ 若照搬 L2 那套「Crossref 404 即假 DOI」的判据，⭐ **它会被当成伪造引用**。

⛔ **真相**：⭐ DOI 有多个注册机构。⭐ **Crossref 管学术出版物，DataCite 管数据集 / 软件 / 预印本仓库**（Zenodo · figshare · Dryad · OSF）。⭐ 一个 DataCite DOI **不在 Crossref 库里是正常的**。

```bash
# ⛔ 查 Crossref：查不到
curl -s "https://api.crossref.org/works/10.5281/zenodo.19819244"

# ⭐ 查 DataCite：拿到
curl -sL "https://api.datacite.org/dois/10.5281/zenodo.19819244"
# → Agentic LLM traces for Simulink Model Repair | 2026 | Dataset
```

⭐⭐ **判别规则**：⛔ `10.5281/*`（Zenodo）· `10.6084/*`（figshare）· `10.17605/*`（OSF）· `10.5061/*`（Dryad）**一律走 DataCite**。⭐ 更稳的做法是先打 `https://doi.org/api/handles/<doi>` —— ⭐ 它对**任何**注册机构的 DOI 都能答「这个 handle 存不存在」。

⚠️ ⭐ **这条与 §1.1 是同一类问题**：⛔ **工具的「没找到」被读成事实的「不存在」。** ⭐ 而资产核验里 DataCite DOI 只会越来越多（⭐ replication package 基本都在 Zenodo），⛔ 这个坑迟早会踩。

---

## 2. ⭐ 引用真实性核验

### 2.1 A8 的 12 篇综述 —— ⭐ **12/12 全部真实**

**DOI（Crossref `api.crossref.org/works/<doi>`）：**

| DOI | 结果 | 解析到的标题 | 年 | 刊 |
| :-- | :-: | :-- | :-: | :-- |
| `10.1007/s10664-026-10921-4` | ⭐ OK | Large language models in model-driven engineering: a systematic… | 2026 | Empirical Software Engineering |
| `10.1007/s10270-025-01263-8` | ⭐ OK | On the use of large language models in model-driven engineer… | 2025 | Software and Systems Modeling |
| `10.1002/spe.70029` | ⭐ OK | Generative AI for Requirements Engineering: A Systematic Lit… | **2025** | Software: Practice and Experience |
| `10.1145/3695988` | ⭐ OK | Large Language Models for Software Engineering: A Systematic… | 2024 | ACM TOSEM |
| `10.1145/3712003` | ⭐ OK | LLM-Based Multi-Agent Systems for Software Engineering… | 2025 | ACM TOSEM |

⚠️ **一处年份出入**：A8 把 `10.1002/spe.70029` 记作 **2026**，⭐ Crossref 给 **2025**。⛔ 差异不影响结论，⭐ 但引用时以 Crossref 为准。

**arXiv（`export.arxiv.org/api/query?id_list=<id>`，⭐ https + UA）：**

| id | 结果 | 标题 | 首次提交 |
| :-- | :-: | :-- | :-- |
| `2509.24782` | ⭐ OK | Large language models for behavioral modeling: A literature survey | 2025-09 |
| `2409.06741` | ⭐ OK | Generative AI for Requirements Engineering: A Systematic Literature… | 2024-09 |
| `2509.11446` | ⭐ OK | Large Language Models (LLMs) for Requirements Engineering (RE)… | 2025-09 |
| `2409.02977` | ⭐ OK | Large Language Model-Based Agents for Software Engineering: A Survey | 2024-09 |
| `2607.05031` | ⭐ OK | LLM-Based Test Oracles: Source-of-Authority Taxonomy | 2026-07 |
| `2505.16697` | ⭐ OK | Software Architecture Meets LLMs: A Systematic Literature Review | 2025-05 |
| `2410.17370` | ⭐ OK | On the use of Large Language Models in Model-Driven Engineering | 2024-10 |

### 2.2 ⭐ A8 报的「S2 综述里有一处引用错误」—— ⭐ **属实**

A8 称 S2（behavioral modeling 综述）把 PS12「AI-driven consistency of SysML diagrams」的参考条目**标成了一篇无关的 Unani 医学论文** `arXiv:2310.18361`。

```bash
curl -sL -A "Mozilla/5.0" "https://export.arxiv.org/api/query?id_list=2310.18361"
# → Clinical Decision Support System for Unani Medicine Practitioners（2023-10）
```

⭐ **核实无误。** ⛔ 引用 S2 的 PS12 时不要沿用它的 bib。

### 2.3 ⭐ A8 主动删除两个自己拼出的 DOI —— ⭐ 记功

A8 在自查中发现，它为两条候选**按惯例拼出**了 `10.1145/3652620.…` 与 `10.1016/j.csi.2025.104013`，⛔ 而两者它都没有实际访问过，⭐ 于是全部删除改标「待补」。⭐ 这正是 L2 那次事故要求建立的行为。

### 2.4 ⭐ A3（IEEE Xplore）的 8 个重点 DOI —— ⭐ **8/8 全部真实**

| DOI | 标题（Crossref 解析） |
| :-- | :-- |
| `10.1109/MODELS67397.2025.00014` | MCeT: Behavioral Model Correctness Evaluation using Large… |
| `10.1109/ASEW67777.2025.00033` | On Effectiveness of Formal Model Repair by Large Languag… |
| `10.1109/TSE.2026.3690186` | Process Fragment Recommendation in Process Modeling: Are… |
| `10.1109/IWQoS65803.2025.11143461` | Unleashing the Power of LLM to Infer State Machine From… |
| `10.1109/ETFA65518.2025.11205687` | LLM-based Iterative Refinement of Finite-State Machines… |
| `10.1109/RAMS50514.2026.11424511` | Validating Design Models for Their Application in Model-… |
| `10.1109/SECON68281.2026.11579014` | Poster: Automated Extraction of Protocol State Machines… |
| `10.1109/MODELS-C68889.2025.00079` | Coupling LLMs and Model-Driven Engineering to Support Sy… |

⭐ A3 自陈「98 个引用 DOI 已机械核对全部来自原始响应，零拼造」。⭐ 抽验 8 条全对，⭐ 与自陈一致。

### 2.4b ⭐ A4（语义检索）的 7 个重点标识符 —— ⭐ **7/7 全部真实**

| 标识符 | 注册机构 | 解析到 |
| :-- | :-- | :-- |
| `10.1007/s10270-026-01388-4` | Crossref | On the consistency of state machines, use cases and block diag… |
| `10.1007/s10664-026-10923-2` | Crossref | The impact of critique on LLM-based model generation from natu… |
| ⚠️ `10.5281/zenodo.19819244` | ⭐ **DataCite** | Agentic LLM traces for Simulink Model Repair · 2026 · **Dataset** |
| `arXiv:2607.23425` | arXiv | TLA+-Bench: An Execution-Grounded Benchmark and Dataset for Natu… |
| `arXiv:2511.17977` | arXiv | Synthesizing Precise Protocol Specs from Natural Language for Ef… |
| `arXiv:2602.07032` | arXiv | LLM-FSM: Scaling Large Language Models for Finite-State Reasonin… |
| `arXiv:2510.25890` | arXiv | ATLAS: A Layered Constraint-Guided Framework for Structured Arti… |

⚠️ 第三行就是 §1.2 那个坑的现场。

### 2.5 ⭐ A8 的第二次自我更正（⛔ 关于 MCeT 仓库怎么找到的）

⭐ A8 先说三个正向 artifact 都来自 GitHub 检索，⛔ 复查后更正：`Huawei-TTE/MCeT` **是从 MCeT 论文 PDF 的链接注解里解析出来的**，⛔ 只有后两个来自仓库检索。

⭐⭐ **这个更正让原结论变强**：⭐ GitHub topic 检索的正向命中比原先说的**还要少**，⛔ 于是「**资产要走论文的 replication package，不要指望 GitHub 检索**」这条更成立。

### 2.6 ⭐⭐ 全量核验：⭐ **57 个标识符，⛔ 零伪造**

⭐ 从 21 张卡里机械抽出全部 DOI 与 arXiv id（⭐ 去重后 **57 个：38 DOI + 19 arXiv**），⭐ 复用 L2 的 [`verify_citations.py`](../provenance/tools/verify_citations.py) 跑全量：

```bash
python3 provenance/tools/verify_citations.py --findings /tmp/l3/cites.json --out /tmp/l3/cite_report.json
```

⚠️ ⛔ **报告里的 53 条 `TITLE_MISMATCH` 是假信号** —— ⭐ 我传入的 `title` 字段是**空的**（⭐ 只抽了标识符），⛔ 于是标题相似度恒为 0。⭐ **它们实际全部解析成功且解析到的标题合理。**

⭐ **真正需要看的只有 4 条**，⭐ 逐条查明：

| 标识符 | 判定 | 原因 |
| :-- | :-- | :-- |
| `10.1145/` | ⭐ **我的正则截断** | ⛔ 不是引用，⭐ 是一个被切碎的片段 |
| `10.1007/s10664-026-10923-2.pdf` | ⭐ **我的正则多吃了 `.pdf`** | ⭐ 真正的 DOI `10.1007/s10664-026-10923-2` **已核为真** |
| `10.5281/zenodo.21310317` | ⭐ **确实不存在** | ⭐ handle API 返回 `responseCode 100`（⛔ 不存在）—— ⭐ **与抽卡 agent 的报告一致**：⭐ 论文自陈「resolves on publication」，⛔ 即 DOI **尚未铸造** |
| `10.5281/zenodo.19819245` | ⭐ **真实存在** | ⭐ handle API 返回 `responseCode 1`；⛔ DataCite 取不到内容（⭐ 该记录已被作者删除，⭐ 见 §4.7） |

⭐⭐ **结论：⛔ 57 个标识符里没有一个是编造的。** ⚠️ 两个「解析失败」是**我自己的抽取正则**造成的，⭐ 一个是**尚未铸造的 DOI**，⭐ 一个是**已删除但 handle 仍在的真实记录**。

⚠️ ⛔ **顺带暴露了 L2 那个工具的一处口径缺陷**：⭐ 它把 DataCite 的 DOI 一律走 Crossref 与 handle，⛔ **而不查 DataCite** —— ⭐ 于是 Zenodo 记录会被判 `DOI_NOT_RESOLVED`。⭐ 本轮靠人工补了 DataCite 查询（⭐ 判据见 §1.2）。

### 2.7 ⛔⛔ 抓到一篇**外部论文里的伪造引用**（⭐ 而它是那篇某条批评的唯一依据）

⭐ CoDIT 2026 那篇 SCP 的参考文献 **[7]** 写作 *Revisiting Iterative Self-Verification in LLMs*，⭐ 标识符 `arXiv:2501.01234`。

⛔⛔ **实际访问该 id：⭐ 它是 *Impact of QCD sum rules coupling constants on neutron stars structure*** —— ⭐ 一篇中子星物理论文。

⛔⛔⛔ **而 [7] 正是那篇批评「LLM 迭代自检」的唯一文献依据。** ⚠️ 同文另有两条参考文献带 literal `XXXXXXX` 占位 DOI 且 Crossref 无匹配（⭐ 记强嫌疑待核）。

⭐⭐ **两条含义**：⭐ ① **那篇对迭代自检的批评在文献层面是悬空的**，⛔ 我们不得引它当外部支持；⭐ ② ⚠️ **伪造引用不是只发生在我们这边** —— ⭐ 这反过来说明 [L2 那条纪律](../provenance/)（**裁定层必须核验引用真实性**）是对的，⛔ 而且对**外部论文**也要执行。

### 2.8 ⛔⛔ 又一个静默失败：⭐ `grep` 在 PDF 抽取文本上**静默返回空**

⚠️ 抽卡 agent 报告：⭐ 在 `pdf_extractor` 产出的 `.txt` 上用 `grep` 查词，⛔ **连一个确定存在的常见词都返回空**，⛔ **既不报错也不返回非零退出码**。⭐ 它据此一度写下「零命中」，⛔ 复核时改用 Python 逐串扫描才发现。

⭐⭐ **后续抽卡一律用 Python 扫，⛔ 不要用 `grep` 判「原文有没有提到某词」。** ⭐ 这与 §1.1（arXiv API 静默空响应）、§1.2（DataCite 走 Crossref）是同一族问题。

---

## 3. ⭐ 资产机械核验

⭐ 工具：[`tools/verify_assets.py`](./tools/verify_assets.py)。

### 3.1 ⭐ 对着已知真值验工具（⛔ 先验工具再验数据）

⭐ 拿 `baselines/` 2026-06-10 的**人工**核验记录当真值：

| 仓库 | 本工具 | ⭐ 人工记录（两个月前） | 一致？ |
| :-- | :-- | :-- | :-: |
| `YoussefMaklad/FlowFSM` | `4ab9aa4e2e` · ⛔ **空壳**（2 文件 / 非文档 0） | `4ab9aa4e2e68da63…` · 🟠「只有 README + .gitignore」 | ⭐ ✅ |
| `zebradile/ttool-ai` | `f2c52282cb` · 🟢（54 / 33） | `f2c52282cb7a826c…` · 🟢 | ⭐ ✅ |
| `Paul3246/nl2fsm` | `354f9aacf5` · 🟢（1764 / 664） | `354f9aacf51b5121…` · 🟠 | ⚠️ **分歧** |

⭐ **三个 HEAD 哈希与两个月前的人工记录逐字符相同** —— ⭐ 工具读数正确，⭐ 且这三个仓库两个月未动。

⚠️ **第三行的分歧是设计使然，⛔ 不是 bug**：⭐ 机械判据只回答「**取不取得到**」，⛔ 回答不了「**取到的够不够复现**」。⭐ 人当时判 🟠 的理由是「仅含部分示例和结果文件，**非冻结完整 benchmark**，无 release / license / 依赖锁」。⭐ 故工具的输出字段叫 `suggest` 而非 `verdict`。

### 3.2 ⭐ A8 报的三个「正向 artifact」—— ⭐ 全部属实且非空壳

| 仓库 | HEAD | 文件 / 非文档 | license | 判 |
| :-- | :-- | --: | :-- | :-: |
| `Huawei-TTE/MCeT` | `8b1b65073e` | 288 / **202** | 无 | ⭐ 🟢 |
| `Mohannadcse/AlloySpecRepair` | `4117c56ae2` | 32216 / 32179 ⚠️ 树被截断 | MIT | ⭐ 🟢 |
| `pluto-ms/FSM-Smart-Contract-Generation` | `9dcd83ed53` | 360 / 356 | 无 | ⭐ 🟢 |

---

## 4. ⛔ 复核未通过 / 待澄清

### 4.1 ⭐ S1 的 OSF 复现包：⛔ 初判「取不到」是**我探错了** —— ⭐ **已结，且双方哈希一致**

⛔ **我的错误**：探测时**漏了 query string**。⭐ `g5by9` 是**匿名 view-only 项目**，token 逐字写在 S1 PDF 参考文献第 112 条里。

| 请求 | 状态 |
| :-- | :-: |
| `https://api.osf.io/v2/nodes/g5by9/files/osfstorage/` | ⛔ **401**（我最初只试了这个） |
| ⭐ `…/files/osfstorage/?view_only=5c10c1e56be3480d8d25e017b4276f7a` | ⭐ **200** |
| ⭐ `https://osf.io/download/8vpkj/?view_only=<同上>` | ⭐ **200**，76325 B |
| `https://osf.io/g5by9/`（网页） | ⚠️ 200 但 4207 B **SPA 壳** —— ⭐ 这一条判断是对的 |

⭐⭐ **主 session 独立下载后与 A8 的文件 sha256 完全相同**：

```
5a396fe4e3c1b5e292342469172106349dbfb464da783d0a4b91cb31b1e67279  S1_data_extraction.xlsx  (76325 B)
```

⭐ 结构：sheet `framework`，⚠️ **表头在第 2 行**，89 行有标题、其中 **86 行有 `Publication_Year`**（= 86 篇 primary），⭐ 另 3 行（`P020` `P044` `P083`）是空壳并入行。

⭐⭐ **教训（⛔ 记给后续所有人）：⛔ 401 不等于不可得。** ⭐ 匿名 view-only 链接靠 query string 鉴权，⛔ 掐掉 query string 去探必然 401 —— ⭐ 而这与「需要登录」在状态码上**完全无法区分**。⭐ **凡遇 401/403，先回原文找有没有 token，再下结论。**

### 4.1b ⛔⛔ A8 承认一处表述误导，⭐ 且它改变了证据链

⭐ A8 逐字：「**这是我的表述错误，你复现不了的直接原因在我**」。

⛔ 它用 xlsx 的**列名**（`Autonomy Level` × `Execution Structure`）做了小节标题，⭐ 足以让人以为数字出自那个需要 token 的文件。⭐ **实际的来源分工是**：

| 内容 | 真实来源 | 鉴权 |
| :-- | :-- | :-- |
| ⭐ §3.2 / §3.3 的**聚合数字** | ⭐ **公开 PDF 正文** | ⭐ **无需鉴权** |
| §2.1 的 23 条候选**名单** | xlsx 单元格 | 需 view_only token |

⭐⭐ **这个更正让证据链变强而非变弱**：⭐ 承重数字的主来源是**无鉴权公开 PDF 的正文散文句**，⛔ 比藏在 token 后面的表格更好追。

### 4.2 ⭐⭐ 独立复算：⭐ **S1 的分布数字逐条对上，⛔ 且不是从柱高目测的**

⭐ 主 session 自取 PDF（⛔ 不经 A8）：

```bash
curl -sL -A "Mozilla/5.0" -o S1.pdf "https://wilson008.github.io/papers/2026-llm4mde-sms.pdf"
# http=200  size=1506033  application/pdf
sha256sum S1.pdf
# 98d17a600e95030b9d31866986b33a9e1a198b3c80df968df8841afb6b3a26b9
python -m tools.pdf_extractor -i S1.pdf -o S1.txt -m text   # 49 页
```

⭐⭐ **关键性质：这些数字是图注里的显式 `n` 与 `%`，⛔ 不是柱高。** ⭐ 例如 Fig. 19 的文本层逐字就是 `Grammar-constrained` … `1  (1%)`。⭐ **「目测柱状图」这个风险不成立。**

| A8 报的 | ⭐ PDF 逐字 | 出处 | 对上？ |
| :-- | :-- | :-- | :-: |
| Non-agentic 83 (96.5%) / Agentic 3 (3.5%) | `Non-agentic (n=83, 96.5%)` `Agentic (n=3, 3.5%)` | Fig. 20 | ⭐ ✅ |
| Iterative 44 / Single-pass 35 / Pipeline 26 / Tool-augmented 26 | ⭐ 正文逐字 `iterative execution … appearing in 44 studies, while pipeline and tool-augmented structures are each reported in 26 studies. Single-pass execution appears in 35 studies` | §RQ2 正文 + Fig. 21 | ⭐ ✅ **四个总数** |
| ⛔ 「只用这一种 / 组合」拆分 14-30 / 26-9 / 2-24 / 3-23 | ⚠️ **数字对，⛔ 但哪一半是「只用」是推断** | Fig. 21 图内 | ⛔ **降为 I 级**，见 §4.3 |
| Grammar-constrained 仅 1 (1%) | `Grammar-constrained` … `1  (1%)` | Fig. 19 | ⭐ ✅ |
| Metamodel retrieval 仅 1 (1%) | `Metamodel retrieval` … `1 (1%)` | Fig. 18 | ⭐ ✅ |
| 微调 9/86 (10.5%) | `(n=9, 10.5%)` / `No fine-tuning (n=77, 89.5%)` | Fig. 17 | ⭐ ✅ |
| **42% 无基线对照** | ⭐ 正文逐字 `Fig. 38 shows that 36 papers (42%) do not include any baseline at all, evaluating the proposed approach in isolation` | §RQ4 | ⭐ ✅ |
| Model Generation 62/86 | ⭐ 正文逐字 `Model Generation is the most frequently addressed task, appearing in 62 of the 86` | §RQ1 | ⭐ ✅ |
| Post-hoc human review 38 | `Post-Hoc Human Review(n=38)` | Fig. 附录 | ⭐ ✅ |

⛔ **一处 A8 未报、⭐ 而对我们更重要的数**（见下面 §6）。

### 4.3 ⛔⛔ 我自己在 §4.2 里犯的错：⭐ 把一个推断标成了已核验

⛔ **上一版的 §4.2 把 Fig. 21 的「只用这一种 / 组合」拆分（`14 30` `26 9` `2 24` `3 23`）标成了 ⭐ ✅。** ⛔ **那是错的**，⭐ 由 A8 在答复里主动挂出来。

⭐ **为什么它看起来像已核验**：⭐ 四组数的**和完全对得上** —— $14+30=44$、$26+9=35$、$2+24=26$、$3+23=26$。⭐ 于是「哪两个数配哪一行」是**确定的**。

⛔⛔ **但「哪一个是『只用这一种』、哪一个是『组合』」在正文里没写**，⭐ 只能按图例顺序推。⭐ 推出来的结果虽然合理（⭐ single-pass 多为「只用」、pipeline / tool-augmented 多为「组合」符合直觉），⛔ **但合理不等于已核**。

⭐⭐ **这是一个值得记住的失败形态：⛔ 一致性检查通过 ≠ 语义已确认。** ⭐ 和数对上只证明了**配对**，⛔ 证明不了**标签归属**。⚠️ 而「数字自洽」给人的确定感非常强 —— ⭐ 强到我在写日志时没有停下来问「图例顺序我核过吗」。

⭐ **处置**：该行在本日志与后续所有引用中标 **I 级**，⛔ 不得写成事实句。⭐ 四个**总数**不受影响（⭐ 它们有正文散文句背书）。

### 4.4 ⚠️ S1 自身有一处**源内不一致**（⛔ A8 报，⭐ 属实且须记）

⭐ `Post-Hoc Human Review` 的篇数：⛔ **论文正文说 38，⭐ 而它自己的复现包算出 39。**

⭐ **处置**：⛔ 引用这一格时必须写「**38（正文）/ 39（复现包）**」，⛔ 或者干脆不用这一格。⚠️ 我在上一版日志里单写了 38 并标 ✅ —— ⛔ **那个 ✅ 只证明「A8 抄对了正文」，⛔ 不证明「38 是对的」。**

### 4.5 ⚠️ 一个会撞上的读数陷阱（⭐ A8 提前挡下）

⛔ S1 正文另有一处 `(40%)` **极像**全语料的无基线率，⛔ 但它是 **`Model Generation` 子集**（62 篇里 25 篇）。⭐ 与摘要那句 `36 papers (42%)` **分母不同，不矛盾**。⛔ 引用时不要混。

---

### 4.6 ⚠️ A4 的「37.8% 对标题级扫描不可见」—— ⭐ **方向确认，⛔ 具体数未独立复现**

⭐ A4 报：在它 **296** 条过门候选里，**112 条（37.8%）**的行为模型术语**只在摘要里、标题里一个都没有**，⛔ 于是任何标题级扫描恒不可见。

⭐ 主 session 拿它留的 11 MB 原始 JSON（`/tmp/l3/raw_a4/`）粗算了一遍：**3544 条去重题录 → 粗过两门 1018 条 → 标题无行为词 711 条 = 69.8%**。

⛔⛔ **这两个数不可比，⭐ 我的复算既不证实也不证伪它**：

| | A4 的 37.8% | ⭐ 我的 69.8% |
| :-- | :-- | :-- |
| 分母 | ⭐ **296 条人工过门候选**（逐条读摘要判过） | ⛔ **1018 条粗正则命中**（⛔ 无人工判断） |
| 行为词表 | ⭐ 把 `UML` 算作「L1 可见」 | ⛔ 我把 `UML` **算进了行为词** |
| 假阳性 | ⭐ 已由人工判掉 | ⛔ **大量残留**（⚠️ 摘要里顺带提一句 `workflow` 就命中） |

⭐ **能确定的只有一条：⭐ 无论用哪个口径，⭐ 这个比例都远高于 1/3 —— ⭐ 即「标题级扫描漏掉一大片」这个方向是稳的。**

⛔ **要真正复现 37.8%，必须重做它那 296 条的人工判门** —— ⭐ 那等于把 A4 的活重跑一遍。⚠️ **本轮不做**，⛔ 故该数字在 [SUMMARY.md](./SUMMARY.md) 里标 **S 级（有原始数据支撑但未独立重算）**，⛔ 不标 M。

⚠️ ⭐ **顺带一条方法论**：⛔ 我最初写这段时差点写成「我复算得 69.8%，比 A4 报的还高」—— ⭐ 那是**错的表述**，⛔ 因为它暗示两个数在同一把尺子上。⭐ **不同分母的两个百分比放在一起比较，本身就是一次口径错误。**

---

## 6. ⭐⭐ 主 session 自己从 S1 挖出的、⛔ 比 A8 报的更要紧的四个数

⭐ 全部逐字取自上面那份已核哈希的 PDF。

### 6.1 ⭐⭐ **`Model Validation` 只有 11/86** —— ⭐ 这是我们这个任务的真实分母

⭐ Fig. 2 的 MDE 任务分布（N=86）逐字：

| 任务 | 篇数 |
| :-- | --: |
| Model Generation | **62** |
| Model Completion / Repair | 12 |
| ⭐⭐ **Model Validation** | ⭐⭐ **11** |
| Model Transformation | 10 |
| Code Generation | 5 |
| Model Migration | 3 |
| DSL Engineering | 3 |
| Metamodeling | 1 |

⭐⭐ **这一格是本轨到目前为止最有用的单条事实。** ⭐ 它同时说明两件事：⭐ **我们做的事在 LLM4MDE 里确实是少数派（11/86 ≈ 12.8%）**，⛔ **但不是空白** —— ⚠️ 所以「据我们所知未见」这类话仍然不能随便写（⭐ 与 L1/L2 的既有裁定一致）。

⚠️ **⛔ 注意这 11 篇里有多少是行为模型、多少是类图 / 元模型，S1 没有交叉列出。** ⭐ 那正是 L3 要自己去数的。

### 6.2 ⭐ Model Validation 这一类的**自我披露率反常地高**

⭐ 正文逐字：`Model Validation papers discuss approach limitations in all cases (100%) and also discuss LLM limitations at a comparatively high rate (91%)`。

⭐ 而 `Code Generation` 那一类 `report low reproducibility support (20%)`。⭐ **做验证的人对自己方法的局限更诚实** —— ⭐ 这对我们怎么写 −15.82pp 是个正面信号：⛔ 这一类的读者预期本来就包含「你要讲清局限」。

### 6.3 ⚠️ **成本几乎没人评**：`only 21 papers evaluate the computational or financial cost of their approach, whereas 65 do not`

⚠️ ⭐ 我们手上有一个 **212.6×** 的成本比 —— ⭐ 在一个 **76%（65/86）不谈成本**的领域里，⭐ 这既是可写的差异化，⛔ 也意味着**没有同行数字可比**。

### 6.4 ⭐ 可复现支持 61/86，⛔ 但威胁有效性只有 49/86

⭐ 正文逐字：`61 papers report reproducibility support` · `Threats to validity is provided in 49 papers, meaning that around half of the primary studies still` …

⚠️ ⛔ **「report reproducibility support」是论文自陈，⛔ 不等于我们能取到东西。** ⭐ L3 的资产核验就是要量化这两者之间的差 —— ⭐ 若自陈 71% 而实际可取远低于此，⭐ **那个差本身是一条可写的发现**。

---

### 4.7 ⚠️ 一份**已被作者删除**的资产（⛔ 而我们持有副本）

⭐ `10.5281/zenodo.19819244`（*Agentic LLM traces for Simulink Model Repair*）：

| 查询 | 结果 |
| :-- | :-- |
| handle API | ⭐ `responseCode 1`（存在） |
| DataCite | ⭐ `findable`，⭐ 标题正确，2026，`Dataset` |
| ⛔ **实际访问** | ⛔⛔ **HTTP 410** —— `removal_reason` 逐字 **`test-record`**，`removal_date` **2026-05-03**；⛔ 全部文件 URL 现均 410 |

⭐ **我们持有本地完整副本**（⭐ 10 文件 / **162,663,460 B**，⭐ md5 全部实算）。⛔ **但无法与官方校验和交叉验证** —— ⭐ 那份校验和随记录一起没了。

⭐⭐ **这是一个值得记的资产风险形态**：⛔ **元数据仍然 findable、DOI 仍然解析、⛔ 而内容已经不在了。** ⭐ 任何只查 DOI 是否解析的核验都会把它判成 🟢。

---

## 5. 更新日志

| 时间 | 动作 |
| :-- | :-- |
| 2026-08-13 | 建档。核 A8 的 12 个标识符（12/12 真）· 核 S2 引用错误（属实）· 验资产工具对 3 个已知真值（3/3 哈希一致）· 核 A8 三个正向 artifact（3/3 非空壳）· ⚠️ OSF 复现包取不到，⭐ 但自取 S1 PDF 独立复算，⭐ 8 个分布数字逐条对上（⛔ 且是图注显式 n/%，非目测）· ⭐⭐ 另挖出 `Model Validation 11/86` 等四个 A8 未报的数 |
