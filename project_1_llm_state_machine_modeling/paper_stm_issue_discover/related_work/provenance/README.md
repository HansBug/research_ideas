# `provenance/` — L2 轨产出：19 条谓词的出处三类分级

⭐ 本目录回答一个问题：**我们那 19 条谓词凭什么成立。** ⛔ 它**不**回答「别人做了什么 STM 缺陷发现工作」（那是 L1 的 [../CONTINGENCY_L1.md](../CONTINGENCY_L1.md)），⛔ 也**不**回答「断言这种输出形态凭什么好」（那已由第三类调研 [../assertion_output_form_evidence.md](../assertion_output_form_evidence.md) 答完）。

## ⛔⛔ 先读懂证据轴：是**普遍性**，⛔ 不是**符合性**

〔用户明确裁定 2026-08-12〕**「我们这套谓词逻辑是我们自己定义的啊，我们和某个官方不绝对一致又说明的了什么呢」「只需要那些文献能证明这些所有的谓词逻辑都是常见的、有需求的，因此我们归纳了主流的这些、定义了这套东西」。**

| | 要证明的命题 | 论文里的句子 |
| :-- | :-- | :-- |
| ⛔ **符合性（⛔ 不作这个主张）** | 「谓词 X 的定义**依从**标准 Y §Z」 | 「我们遵循 …」 |
| ⭐ **普遍性（⭐ 唯一主轴）** | 「检查 X 这件事在领域文献与工程实践里**反复出现、确有需求**」 | 「这类检查在 … 中反复出现，我们把主流的这些归纳成一套闭合词表」 |

⚠️ **规范材料（UML / IEC / ISO）仍可引，但只能取存在性事实**：取「该检查是某规范良构性规则里的常规项」是普遍性证据（✅）；取「该规范要求模型满足 X，所以我们的谓词有依据」是符合性论证（⛔）。⛔ **判据是把句子写出来看它承诺了什么 —— 承诺「我们与谁一致」的一律不要。**

⛔ 由此**整条作废**：PSSM 一致性套件专检 · IEC 61131-3 / SFC 线索 · 一手规范取件前置 · 任何引 `pyfcstm` 充当语义权威的写法。

## ⭐ 分类是**三类**，⛔ 不是六级

| 类 | 含义 | ⭐ 论文里怎么说 |
| :-- | :-- | :-- |
| ⭐ **① 有领域证据** | 该检查在真实控制系统的建模实践与领域文献中**反复出现** | 「这类检查在 … 中反复出现，我们把主流的这些归纳成一套闭合词表」 |
| ⭐ **② 元模型定义性** | ⭐ **该检查在定义上就成立，⛔ 不需要外部出处** —— 元模型说这种元素存在，检查「它是否被声明」是定义的直接后果 | 「其判据由元模型定义直接给出」 |
| ⛔ **③ 无外部依据** | 既非①也非② | ⛔ 在 Limitations 明写一句，⛔ 不隐瞒、⛔ 也不删谓词（588 冻结） |

⛔ **三类不是强度序。** ① 与 ② 谁也不高于谁 —— 它们回答的是不同问题（「领域普遍这么查」vs「定义上就成立」）。⛔ 旧的六级 (a)–(f) 与 (d1)/(d2) 记法**一律不再使用**。权威定义：[../../discover_matrix/docs/protocol/method_provenance_policy.md](../../discover_matrix/docs/protocol/method_provenance_policy.md) §一.4。

⭐⭐ **为什么 ② 必须单独成类**：合并会把「**不必挂**」误记成「**挂不上**」。`event_declared` `variable_declared` `state_declared` `edge_declared` `action_declared` `effect_declared` 这 6 条承载 **966 / 1555 = 62.1%** 的已发布支撑 —— 把它们记成「无依据」，等于宣称方法 62% 的产出没有依据，⚠️ 而实际上它们是**由定义支撑的**。

## ① 类证据的形态：存在性 + 多源 + 领域多样，⛔ 不是比例

| 项 | 要求 |
| :-- | :-- |
| **主张形态** | ⭐ **存在性 + 重数**：「该义务在 A、B、C … 等**互相独立的真实系统**中被明确要求」。⛔ **不给任何比例** |
| **下限 / 上限** | ⭐ **≥ 3 个独立来源**为下限；⛔ **无上限**，常见义务 10 个更好 |
| ⭐ **领域多样性** | ⛔ 同等数量下，**覆盖的系统类型越分散越有说服力**。判据：N 个源覆盖 $\min(3, N)$ 个以上不同领域；⛔ 若确实只在单一领域出现，**必须显式说明**并把主张限定到该领域 |
| **准入** | ⛔ 只取**界内**案例：`状态机类型 ∈ {FSM, EFSM, HSM}` ∧ `时间级别 = T0` ∧ 无「并行」标签 |
| **引文** | ⛔ 只取 `### 1. 原文摘录` 节；⛔ 引文自身须含义务性表述 |
| **反证** | ⛔ 仍须报告，⭐ 但性质是**边界说明**（「界内案例 X 明确不要求该义务，故该义务不是普适的」），⛔ 不是比例的分母侧 |

⛔⛔ **为什么不能报比例**：`sources/` 的收录标准（[README](../../../sources/README.md) §3：「文中存在运行模式、状态切换、阶段推进、故障处理、恢复路径…」）**恰恰就是要去测的那些义务本身**。论文之所以在库里，就是因为它有这些东西。⛔ **这是在因变量上做选择**，比例必然虚高且高多少无法估计。

⛔ **「可用池」这个词一词二义，禁止再用**：**787** 是收录总数、**715** 是有提取内容的条目数、**313** 是界内案例数 —— ⭐ 三者都只是**库存量**，⛔ 一个都不是分母。

## ⛔ 两条取证判据（v25 与 §1.4 反面样例的同型错误）

1. ⛔ **列举 ≠ 义务。** 「原文出现了 N 个 X」只支撑「X 这个维度在该领域被显式建模」，⛔ **不支撑任何关于 N 的断言**。要支撑 `cardinality`，引文必须自己说出「恰好 / 唯一 / 必须 / 不得多于」这类话。
2. ⛔ **叙述 ≠ 义务。** 过去时的实验记录（「the battery **was discharged until** its SOC reached …」）虽含 `until`，⛔ 但它描述的是一次实验发生了什么，⛔ 不是系统必须怎样。⭐ 判据：看主语与时态 —— 描述**已发生的运行**的一律不收。

## 目录内容

| 路径 | 是什么 |
| :-- | :-- |
| [SUMMARY.md](./SUMMARY.md) | ⭐ **总账入口** —— 一页结论 + 三类计数 + 四条坏消息 + 元模型级发现 + Q3 定档 + 对 `story/` 的建议 |
| [predicate_provenance.md](./predicate_provenance.md) | ⭐ **19 行出处三类表**（逐条含扣分项） |
| [c3_differentiation.md](./c3_differentiation.md) | ⭐ **Q2 · C-③ 差异化** —— 三要素战况 + 三条已知反例的原文定位。⚠️ 它的「唯一空缺是 (iii)」**已作废** |
| ⭐⭐ [c3_iii_supplement.md](./c3_iii_supplement.md) | ⭐⭐ **C-③ 措辞的最终依据** —— ⛔ 它推翻了「唯一空缺是 (iii)」，⭐ 并给出跨五条线不变、有**六处独立自证**的 gap 陈述 |
| [recovery_log.md](./recovery_log.md) | ⭐ 伪缺口与付费墙回收（10 个目标 9 个全文）+ ⛔ **三处被证伪的元数据** |
| [corpus_scan_findings.md](./corpus_scan_findings.md) | ⭐ 界内语料两轮穷尽扫描的三条发现 |
| [methodology.md](./methodology.md) | ⭐ 四层编制 · 裁定层的失败模式与双向可靠性审计 · 六条方法局限 |
| ⛔ [coverage_audit.md](./coverage_audit.md) | ⛔ **C3 覆盖审计：这轮漏了什么** —— ⚠️ **它推翻了两处 claim 形状，⛔ 引用本目录任何结论前必读** |
| [tools/](./tools/) | 可复现的机械工具，见下 |

### `tools/` 六件

| 工具 | 干什么 | ⛔ 边界 |
| :-- | :-- | :-- |
| [build_inscope_corpus.py](./tools/build_inscope_corpus.py) | 按边界门三条合取筛出 `sources/` 界内条目，**只抽 `### 1. 原文摘录` 节**，按领域轮转分片 | ⛔ 筛法是**准入门**，⛔ 不是任何比例的分母 |
| [verify_quotes.py](./tools/verify_quotes.py) | 核验每条引文是否**逐字**存在于摘录节 | ⛔ **只做定位不做裁定**：它答「这句话在不在那里」，⛔ 不答「它算不算义务」 |
| [aggregate_evidence.py](./tools/aggregate_evidence.py) | 按谓词聚合**独立来源数**与领域覆盖 | ⭐ 计数单位是**互相独立的真实系统**，⛔ 不是条目数；⭐ 标识符按 DOI/arXiv 归一（⚠️ 否则同一篇会被算成多个） |
| [verify_citations.py](./tools/verify_citations.py) | 解析 DOI / arXiv 核验引用真实存在 | ⛔ 只做存在性与题录比对，⛔ 不做内容裁定 |
| [detect_self_citation.py](./tools/detect_self_citation.py) | ⛔ 查「拿本研究自己的材料当独立领域证据」 | ⭐ 分三层：种子语料（剔除）· baseline（标注）· 一般收藏（无问题） |
| [build_provenance_table.py](./tools/build_provenance_table.py) | 生成 19 行三类表 | ⛔ **只吃经过对抗裁定的证据** |

⛔ **钉命令不钉数** —— 下列数字随扩库变化，交付时现跑：

```bash
python related_work/provenance/tools/build_inscope_corpus.py --out-dir /tmp/l2/corpus --shards 12
python related_work/provenance/tools/verify_quotes.py --findings <findings.json>
python related_work/provenance/tools/aggregate_evidence.py --phase-a <findings.json>
```

⚠️ 跑前先确保 submodule 就位，⛔ 否则 `predicate_usage.py`（数字真源）会因空 `pyfcstm/` 目录被当成 namespace package 而报 `ModuleNotFoundError`：

```bash
git submodule update --init --recursive && pip install -e ./pyfcstm
```

## ⛔ 与其它文件的关系

- **上级合同**：伞 PR [#179](https://github.com/HansBug/research_ideas/pull/179) §4.6。⛔ 与 [../CONTINGENCY_L2.md](../CONTINGENCY_L2.md) 冲突时以伞 PR 为准。
- **口径权威**：[../../discover_matrix/docs/protocol/method_provenance_policy.md](../../discover_matrix/docs/protocol/method_provenance_policy.md) §一.3–§一.5。
- **预案**（⛔ 不是结论）：[../CONTINGENCY_L2.md](../CONTINGENCY_L2.md)。⚠️ 它的 §3 整节与 §6.2 / §6.3 **已作废**。
- ⛔ **不写 `GUIDE.md`** —— 伞 PR §4 就是它的 GUIDE，另写一份等于建第二真源。
