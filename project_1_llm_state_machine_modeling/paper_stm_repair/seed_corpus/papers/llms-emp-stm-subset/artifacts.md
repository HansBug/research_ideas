# artifacts: llms-emp-stm-subset

| 项 | 当前状态 | 证据 / 稳定性 | R2 影响 |
|---|---|---|---|
| PDF | present | `paper.pdf`，SHA-256 `238ab5965a2c2e4127330e3101486e199a9a4e1fb185c380bcc20aac72a2643c`；论文页 DOI URL 为 `https://dl.acm.org/doi/10.1145/3755881.3755926`。 | 可作为全文证据源。 |
| paper_content.txt | present | `paper_content.txt`，SHA-256 `2cc4fbb56737da224790f95640bdcd78b6ee3ed2e85ffdb9025718c1780bb62f`；与源 baseline 行数一致，为 1189 行。 | 可作为证据指针主来源。 |
| BibTeX | present | `bibtex.bib`，SHA-256 `42d75cba2de1d935d87bd5ed43a423c77fd1ce61d40d6d03488a975b61442e5f`；DOI `10.1145/3755881.3755926`。 | 元数据可用。 |
| Code / artifact | absent | 源 `ASSETS.md` 明确未发现公开生成脚本或模型调用脚本；论文正文也未给出 GitHub/Zenodo 代码入口。 | 不能复现作者 pipeline；R2 需自建 prompt/RAG/checker/regeneration。 |
| Dataset / outputs | usable | 论文脚注与正文给出 Google Drive：`https://drive.google.com/drive/folders/10eo8KDqlBlkQZxPpPCB7R3-aBQZ7Rsm6?usp=drive_link`；源 `ASSETS.md` 记录本仓库 parquet 冻结：raw samples 107 行 SHA-256 `69e5123174f976bf7504eaa334e0670da22b2e0c67329c57539b3866dfe5b045`，complete samples 98 行 SHA-256 `d8c0dca59c650149c7c16e433fc54440fc72509c82d57676ca6238f2182fdf2e`，human-review 192 行 SHA-256 `7b54b06ead32e0a5b6c6d4f2244d11a8e2439c64ad421f01a1b8a9175f16a427`。 | STM 数据级 seed 可用；正式统计应以本地冻结文件和 eligibility filter 为准。 |
| License / redistribution | partial | 论文正文 `paper_content.txt:113-115` 声明论文为 Creative Commons Attribution 4.0 International License；允许读取材料未定位数据集单独 license。 | 论文可引用；数据二次分发需后续人工核验。 |
| URL stability | mixed | ACM DOI 稳定；Google Drive 文件夹入口可用性和内容可能漂移，源 `ASSETS.md` 也将其列为需复查风险。 | R2 run record 必须记录下载/抽取日期、hash、行数与来源 URL。 |
| Conversion readiness | ready-with-filter | 论文 Table 2 有 36 个 STM；数据集同时包含 ACT/SD，需要按 model type 过滤。 | 可进入后续 converter 设计，但本轮不定义转换器。 |

## 资产结论

`SA-2`。论文、全文、BibTeX、公开数据入口和本地 parquet 冻结足以支持 R2 的 STM seed 抽取与审计；但缺失作者原始 pipeline 代码，数据集 license 未在本轮允许材料中定位，Drive 内容也存在漂移风险。因此该候选应作为“数据/结果可用”的 seed，而不是“完整复现实验包”。

## R2 使用建议

1. 优先从本地冻结 parquet 抽取 STM 行，并记录 raw/complete/human-review hash。
2. 将 ACT/SD 明确排除，不进入 STM repair seed 统计。
3. 对每个抽取样例保留需求文本、参考 PlantUML STM、原始模型类型、来源 case、hash、抽取脚本版本和 eligibility 结果。
4. 若需要复现 Phase-II repair，需要新建本项目自己的 prompt、PlantUML/SysML checker 与 feedback loop，不能声称使用作者实现。
