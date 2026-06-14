# artifacts: umple-nl-state-machine

## Artifact 结论

| 项 | 当前状态 | 结论 |
|---|---|---|
| PDF | present | 本地 `paper.pdf` 已存在；与源目录 PDF SHA-256 一致。 |
| paper_content.txt | present | 本地全文抽取已存在；与源目录 `paper_content.txt` SHA-256 一致。 |
| BibTeX | present | 本地 `bibtex.bib` 与源目录一致，指向 RUOR item；源目录另记录 DOI。 |
| Code / artifact | not found | 未发现论文专属公开实验仓库、prompt/runner、RAG 检索库、评测脚本或 release。Umple 工具链公开，但不是本 thesis 的实验 artifact。 |
| Dataset / outputs | paper-only | 论文正文给出 5 个系统 requirements、图示和聚合结果表；未公开完整 benchmark bundle、逐次 Llama 3 输出、corrected reference state machines 或下载表。 |
| License / redistribution | blocker | PDF 可公开访问；实验代码/数据未公开，无法确认 license、redistribution、commit 或 DOI artifact。 |
| Conversion readiness | not R2-ready | 只能作为文献证据或手工重建线索；不能直接进入 R2 主 seed 样本。 |

## 已核 artifact 指针

| 类型 | URL / 路径 | 稳定性判断 |
|---|---|---|
| RUOR item | <https://ruor.uottawa.ca/items/b3679a91-5445-45ce-b289-bfddba3010f6> | 稳定论文入口；覆盖 thesis PDF，不覆盖实验 bundle。 |
| PDF download | <https://ruor.uottawa.ca/bitstreams/75cf8d04-a540-4d48-ad54-b8f13b3df2e8/download> | 当前源目录已记录可访问；适合作为论文文件来源。 |
| DOI | <https://doi.org/10.20381/ruor-31249> | 源目录记录的 bibliographic anchor；不覆盖实验 artifact。 |
| Umple toolchain | <https://github.com/umple/umple> | 工具链公开；不是该 thesis 的实验代码。 |
| UmpleOnline | <https://try.umple.org/> | 活网页，可辅助重建部分示例；不能视为 frozen benchmark。 |
| Umple requirements examples | <https://cruise.umple.org/umple/RequirementsExamples.html> | 活文档，源目录指出可近似重建部分示例；需冻结版本和映射说明。 |
| 源目录资源账本 | [ASSETS.md](../../../../baselines/umple/ASSETS.md) | 本次 artifact/license/hash/URL 判断的主要本地证据源。 |

## 本地文件 hash

| 文件 | SHA-256 |
|---|---|
| `paper.pdf` | `b0b4825f4b5710425da41fcc7a12141e40a49b4f6a45cd8db833b714e9c6989b` |
| `paper_content.txt` | `8330d4f66a2855cddfe3c32e3acd75a14d7df0b4b29cf698a99f7125b4f148ab` |
| `bibtex.bib` | `b4280895e3e38ca329626a7878b09ff648ce041773128bd19eaf5e0e1e83f0c8` |

上述 3 个 hash 与源目录 [`baselines/umple/`](../../../../baselines/umple/) 中对应文件一致，说明候选目录当前持有的是同一 thesis 版本。

## R2 blocker

1. 缺少论文专属实验代码、prompt runner、RAG 文档库和评测脚本。
2. 缺少逐次 generated Umple outputs，无法复核 ICP/EUCP/Pass@K/CodeBLEU/Levenshtein 的原始计算。
3. 缺少完整 ground truth / corrected reference state machine bundle；论文图示和 requirements 不等于可机器消费 pair。
4. Umple 官方示例和 UmpleOnline 是活文档，若用于重建必须另行冻结日期、URL、内容 hash 和命名映射。
5. 未确认实验数据/脚本 license 与 redistribution 权限。

## 当前 artifact grade

`SA-3`：论文与 bibliographic 来源稳定，文献证据足够；但可复验 pair 和实验 bundle 缺失，不进 R2 主样本。后续若要使用，应新建 reconstruction run record，而不是把该 thesis 当作已冻结 artifact。
