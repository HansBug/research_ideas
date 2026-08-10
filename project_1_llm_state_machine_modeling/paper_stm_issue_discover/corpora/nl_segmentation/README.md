# 自然语言规格的需求边界标注

## 为什么存在

Discover 的 `nl_segments` 决定 `segment_disposition` 的键空间，也就决定了模型能答多细：**一段一个裁决**。当前实现按物理换行切分（`feedback_loop/…/discover/nodes.py`），这对语料里 10 份 NL 中的 9 份是正确的 —— 它们一行写一条编号需求。

第 10 份不是。`f1c3dc88…`（被 pair `0000` / `0010` / `0020` / `0030` / `0040` / `0050` 共用）把全部需求写在一行里，按行切只能得到 1 段，模型只能对整份规格给一个粗粒度裁决。

**这不是分段算法能修的。** 那份规格：

| 异常 | 实况 |
| :-- | :-- |
| 编号不在行首 | 全部挤在单个物理行内 |
| 点号有无混用 | `1 ` / `2 ` / `5 ` 无点，`3.` / `4.` 有点 |
| 数字紧贴单词 | `4when front_distance`，无分隔符 |
| 同句内有裸数值 | `> 10` —— 所以「裸数字即编号」的规则必然误报 |
| 编号重复 | `4` 出现两次，作者标号为 `1,2,3,4,4,5`，缺 `6` |

「这份规格有几条需求」在机器层面没有唯一答案。所以边界由人工标注一次，作为**数据**而不是代码。

## 收录范围

只标注**规格自身编号无法机器判定**的那些。其余规格继续走按行切分，不在本文件中出现 —— 标注文件里有一条就说明那一条需要人工介入，这本身是信息。

当前收录 **1 份 / 10 份**。逐份判定见 [PROVENANCE.md](./PROVENANCE.md)。

## 边界声明：这不是 oracle 泄漏

标注回答的是「**这份规格分成几条需求**」，那是散文的属性。它不回答「模型有什么缺陷」：

- 不引用任何状态机元素、路径或标识符
- 不引用 expected issue、不引用参考模型
- 判据只有一条 —— 原文里作者自己写下的编号标记

`feedback_loop/tests/test_nl_segmentation_override.py::test_annotation_names_no_model_elements` 用断言守住这条：标注内容里出现 `llms_emp_feedback_final_`、`state:`、`macro:`、`compiler:` 等任一标识即失败。

## 标注协议

1. **只切不改。** 段文本是原文的逐字切片，切点取作者编号标记的起始偏移。原文的 `4when` 保持原样，不「顺手」补成 `4 when` —— 一旦改字就不是作者原文了。
2. **覆盖必须完整。** 所有段拼接后（忽略空白差异）必须还原原文。这条由 `resolve_nl_segments()` 在每次加载时校验，不通过直接 raise。它同时补回了上一代 pipeline 有、当前实现遗失的 `_assert_non_whitespace_coverage`。
3. **按内容摘要索引。** 键是 `nl_sha256` 的前 12 位，值里存全长哈希。一份 NL 被 6 个 pair 共用，按摘要索引保证 6 个 pair 拿到同一份边界，也不会漏标某个 pair。全长哈希不匹配时**回退到按行切**而不是报错 —— 标注写给的是另一份文本时，粗分段好过用错文本的边界。
4. **歧义显式记录。** 无法由机器消解的判断（如那两个重复的 `4` 算一条还是两条）写进 `annotation_basis`，说明选了哪种读法与理由。
5. **段 id 用 `NL-M` 前缀。** 与按行切的 `NL-L` 区分，任何下游看到就知道这份分段经过人工标注，不必回查配置。

## 文件

| 文件 | 内容 |
| :-- | :-- |
| [overrides.json](./overrides.json) | 标注本体 |
| [PROVENANCE.md](./PROVENANCE.md) | 10 份 NL 的逐份判定，含未标注的 9 份为什么不需要 |

## 运行时如何生效

`feedback_loop/src/paper_stm_feedback_loop/common/nl_segmentation.py` 的 `resolve_nl_segments()` 按内容摘要查表，命中则用标注、否则按行切。`discover/nodes.py` 的 `prepare` 是 `nl_segments` 的唯一产地，所以改这一处，splitter payload、`segment_disposition` 校验与全部下游自动跟上。

`FrozenDiscoverInputs.nl_segmentation_source` 记录走了哪条路（`manual_override` / `line_split`），进 run record。

## 与 `pairs/` 的关系

受影响的 6 个 pair 目录下各有一份 `SEGMENTATION_NOTE.md`，指回本目录。那些 note 是人工说明，**不属于** `PUBLICATION_SEAL.json` 的 `derived_artifact_inventory`；`nl.txt` 本身未被修改，哈希仍与封条一致。

## 相关

- [issue #173](https://github.com/HansBug/research_ideas/issues/173) §6 —— 这个问题是怎么被发现的，以及为什么两个现有分段算法都不可用
