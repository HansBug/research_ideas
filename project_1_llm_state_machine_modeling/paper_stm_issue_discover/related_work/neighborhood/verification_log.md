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

### 4.1 ⛔⛔ S1 的 OSF 复现包：⭐ 我这边**取不到**

A8 称「改走 OSF JSON API 拿到 `03.Data_Extraction.xlsx` —— 86 篇 × 43 字段」。⛔ 主 session 复现失败：

```
https://api.osf.io/v2/nodes/g5by9/                            → 401 Authentication credentials were not provided
https://api.osf.io/v2/nodes/g5by9/files/osfstorage/           → 401
https://files.osf.io/v1/resources/g5by9/providers/osfstorage/ → 403
https://osf.io/g5by9/                                         → 200，⛔ 但只有 4207 字节（SPA 壳）
https://api.osf.io/v2/registrations/g5by9/                    → 404
```

⛔ **这一条要紧**：§3.2 / §3.3 那批形态分布（`Non-agentic 83/86`、`Grammar-constrained 1/86`、`42% 无基线对照`）是本轨**唯一有分母的分布**，⭐ M1 的建议会压在它上面。

⭐ **处置**：已向 A8 追问确切请求路径、数字究竟读自 xlsx 单元格还是 PDF 图注、以及文件是否还在盘上（要 `sha256sum`）。⛔ **在澄清之前，§3.2 / §3.3 的数字一律标「来源受限、待复核」，⛔ 不得写成事实句。**

⚠️ **一个必须排除的可能**：⛔ 若那些数字是从 PDF **柱状图里目测**的，则它们不可靠 —— ⭐ 目测柱高与读单元格是两个证据级别。

---

## 5. 更新日志

| 时间 | 动作 |
| :-- | :-- |
| 2026-08-13 | 建档。核 A8 的 12 个标识符（12/12 真）· 核 S2 引用错误（属实）· 验资产工具对 3 个已知真值（3/3 哈希一致）· 核 A8 三个正向 artifact（3/3 非空壳）· ⛔ **OSF 复现包复现失败，已追问** |
