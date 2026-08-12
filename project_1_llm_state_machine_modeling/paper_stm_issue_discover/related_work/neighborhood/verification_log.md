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

### 4.1 ⚠️ S1 的 OSF 复现包：⭐ 我这边**取不到** —— ⭐⭐ **但关键数字已由 PDF 独立证实，⛔ 本条降级**

A8 称「改走 OSF JSON API 拿到 `03.Data_Extraction.xlsx` —— 86 篇 × 43 字段」。⛔ 主 session 复现失败：

```
https://api.osf.io/v2/nodes/g5by9/                            → 401 Authentication credentials were not provided
https://api.osf.io/v2/nodes/g5by9/files/osfstorage/           → 401
https://files.osf.io/v1/resources/g5by9/providers/osfstorage/ → 403
https://osf.io/g5by9/                                         → 200，⛔ 但只有 4207 字节（SPA 壳）
https://api.osf.io/v2/registrations/g5by9/                    → 404
```

⛔ **这一条要紧**：§3.2 / §3.3 那批形态分布（`Non-agentic 83/86`、`Grammar-constrained 1/86`、`42% 无基线对照`）是本轨**唯一有分母的分布**，⭐ M1 的建议会压在它上面。

⭐⭐ **处置：⛔ 不等 A8，主 session 自己去取 PDF 独立复算。** ⭐ 结果见下面 §4.2 —— ⭐ **那批数字逐条对上，⛔ 本条从 C 降为 M。**

⭐ **仍然成立的部分**：⛔ **候选论文名单**（A8 说从 xlsx 过滤出 30/89 行、人工判后得 23 条）**依赖 xlsx**，⛔ 而 PDF 正文与 122 条参考文献里**没有 86 篇 primary study 名录**。⭐ 故：**分布数字可核，⛔ 名单来源待 A8 澄清。**

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
| Iterative 44 / Single-pass 35 / Pipeline 26 / Tool-augmented 26 | `n=44` `n=35` `n=26` `n=26`；⭐ 组合数 `14 30` `26 9` `2 24` `3 23` | Fig. 21 | ⭐ ✅ |
| Grammar-constrained 仅 1 (1%) | `Grammar-constrained` … `1  (1%)` | Fig. 19 | ⭐ ✅ |
| Metamodel retrieval 仅 1 (1%) | `Metamodel retrieval` … `1 (1%)` | Fig. 18 | ⭐ ✅ |
| 微调 9/86 (10.5%) | `(n=9, 10.5%)` / `No fine-tuning (n=77, 89.5%)` | Fig. 17 | ⭐ ✅ |
| **42% 无基线对照** | ⭐ 正文逐字 `Fig. 38 shows that 36 papers (42%) do not include any baseline at all, evaluating the proposed approach in isolation` | §RQ4 | ⭐ ✅ |
| Model Generation 62/86 | ⭐ 正文逐字 `Model Generation is the most frequently addressed task, appearing in 62 of the 86` | §RQ1 | ⭐ ✅ |
| Post-hoc human review 38 | `Post-Hoc Human Review(n=38)` | Fig. 附录 | ⭐ ✅ |

⛔ **一处 A8 未报、⭐ 而对我们更重要的数**（见下面 §6）。

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

## 5. 更新日志

| 时间 | 动作 |
| :-- | :-- |
| 2026-08-13 | 建档。核 A8 的 12 个标识符（12/12 真）· 核 S2 引用错误（属实）· 验资产工具对 3 个已知真值（3/3 哈希一致）· 核 A8 三个正向 artifact（3/3 非空壳）· ⚠️ OSF 复现包取不到，⭐ 但自取 S1 PDF 独立复算，⭐ 8 个分布数字逐条对上（⛔ 且是图注显式 n/%，非目测）· ⭐⭐ 另挖出 `Model Validation 11/86` 等四个 A8 未报的数 |
