# artifacts: llms-emp-stm-subset

| 项 | 当前状态 | 证据 / 稳定性 | R2 影响 |
|---|---|---|---|
| PDF | present | `paper.pdf`，SHA-256 `238ab5965a2c2e4127330e3101486e199a9a4e1fb185c380bcc20aac72a2643c`；论文页 DOI URL 为 `https://dl.acm.org/doi/10.1145/3755881.3755926`。 | 可作为全文证据源。 |
| paper_content.txt | present | `paper_content.txt`，SHA-256 `2cc4fbb56737da224790f95640bdcd78b6ee3ed2e85ffdb9025718c1780bb62f`；与源 baseline 行数一致，为 1189 行。 | 可作为证据指针主来源。 |
| BibTeX | present | `bibtex.bib`，SHA-256 `42d75cba2de1d935d87bd5ed43a423c77fd1ce61d40d6d03488a975b61442e5f`；DOI `10.1145/3755881.3755926`。 | 元数据可用。 |
| Code / artifact | absent | 源 `ASSETS.md` 明确未发现公开生成脚本或模型调用脚本；论文正文也未给出 GitHub/Zenodo 代码入口。 | 不能复现作者 pipeline；R2 需自建 prompt/RAG/checker/regeneration。只冻结初始/指定版本 `STM_0`，不得把作者后续 human review / feedback 结果当作本方法的改进输入或收益。 |
| Dataset / outputs | usable | 论文脚注与正文给出 Google Drive：`https://drive.google.com/drive/folders/10eo8KDqlBlkQZxPpPCB7R3-aBQZ7Rsm6?usp=drive_link`；R2.0 当前一手事实源为 `assets/raw/drive_download/Experiment Results.xlsx` 与 `assets/raw/drive_download/Dataset.xlsx`，并已抽取 `assets/extracted/pairs.jsonl`。旧 `ASSETS.md` / parquet 只作历史审计线索，不作为当前事实源。 | STM 数据级 seed 可用；正式统计应以 workbook hash、sheet 行数、抽取日期和 eligibility filter 为准。 |
| License / redistribution | citation note | 论文正文 `paper_content.txt:113-115` 声明论文为 Creative Commons Attribution 4.0 International License；Drive 数据作为公开学术资源使用时引用原作。 | 不作为 R2.0 升绿 blocker；核心风险转为 reference/checking 列泄漏隔离。 |
| URL stability | mixed | ACM DOI 稳定；Google Drive 文件夹入口可用性和内容可能漂移，源 `ASSETS.md` 也将其列为需复查风险。 | R2 run record 必须记录下载/抽取日期、hash、行数与来源 URL。 |
| Conversion readiness | ready-with-filter | 论文 Table 2 有 36 个 STM；数据集同时包含 ACT/SD，需要按 model type 过滤。 | 可进入后续 converter 设计，但本轮不定义转换器。 |

## 资产结论

`SA-2 / R2.0 final_pool_ready`。论文、全文、BibTeX、公开数据入口和已下载 Drive workbook 足以支持 R2 的 STM seed 抽取与审计；但缺失作者原始 pipeline 代码，Drive 内容也存在漂移风险。因此该候选应作为“数据/结果可用”的 seed，而不是“完整复现实验包”。

## R2 使用建议

1. 优先从 `assets/raw/drive_download/Experiment Results.xlsx` 的 `STM Results` sheet 抽取 STM 行，并记录 workbook hash、sheet 行数和抽取脚本版本。
2. 将 ACT/SD 明确排除，不进入 STM repair seed 统计。
3. 对每个抽取样例保留需求文本、`Generation PlantUML`、reference PlantUML hash、原始模型类型、来源 case、hash、抽取脚本版本和 eligibility 结果；reference 按 canonical case 为 10 个，但 exact unique reference PlantUML 文本为 11，因一条需求存在两个 reference 文本变体。
4. 若需要复现 Phase-II repair，需要新建本项目自己的 prompt、PlantUML/SysML checker 与 feedback loop，不能声称使用作者实现。
5. Issue #161 的 converter 最终验收可消费作者 workbook 中已存在的 Phase-II final 60 作为独立压力集；该用途不等于复现作者 pipeline，也不改变 Phase-I seed 的实验归因边界。
