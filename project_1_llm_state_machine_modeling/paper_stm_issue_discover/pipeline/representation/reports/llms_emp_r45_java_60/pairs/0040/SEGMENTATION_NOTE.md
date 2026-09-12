# ⚠️ 这份 NL 的分段不能按行切

本 pair 的 `nl.txt` 与 `0000` / `0010` / `0020` / `0030` / `0040` / `0050` 共用同一份规格文本（sha256 `f1c3dc88…`）。**它的编号是坏的**：

- 全部编号挤在**单个物理行**内 —— 按 `splitlines()` 切只能得到 1 段
- 点号有无混用：`1 ` / `2 ` / `5 ` 无点，`3.` / `4.` 有点
- `4when front_distance` 数字紧贴单词；同句内 `> 10` 说明裸数字也会作为数值出现
- 编号 `4` 出现两次（`4when…` 与 `4. transit…`），作者标号为 1,2,3,4,4,5

后果是 `segment_disposition` 只能对整份规格给一个粗粒度裁决，模型无法逐条表态。

## 因此

需求边界由人工标注覆盖，见 [`corpora/nl_segmentation/overrides.json`](../../../../../../corpora/nl_segmentation/overrides.json)。运行时由 `feedback_loop/src/paper_stm_feedback_loop/common/nl_segmentation.py` 的 `resolve_nl_segments()` 按 NL 内容摘要匹配后注入，段 id 前缀为 `NL-M` 而非 `NL-L`，`FrozenDiscoverInputs.nl_segmentation_source` 会记为 `manual_override`。

**不要直接对本目录的 `nl.txt` 按行切分**，那样得到的是 1 段。

`nl.txt` 本身未被修改，仍是作者原文（哈希与 `PUBLICATION_SEAL.json` 一致）；标注只切不改，逐字节拼接可还原原文。

本文件是人工说明，不属于 `PUBLICATION_SEAL.json` 的 `derived_artifact_inventory`。
