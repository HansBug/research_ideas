# CCF venue coverage / gap matrix（2024-2026）

> 检索时间：`2026-06-13 01:20:00`（Asia/Shanghai）
> 范围：以当前 [ccf_venues/01-venue-scope.md](../../../../ccf_venues/01-venue-scope.md) 与 [ccf_venues/SUMMARY.md](../../../../ccf_venues/SUMMARY.md) 的 42 个已建档相关 venue 为基线。
> 本文件只记录 PR-B0 baseline 粗筛 coverage / gap，防止把未扫描区域误写成负证据。

coverage emoji：🔵 = 本轮拿到可复核 title list；🟠 = 只能 coarse title / DBLP / publisher list 或 metadata 不完整；🔴 = 年度未公布、访问受限、DBLP 限流或缺少可复核 paper list。

## 1. 逐 venue coverage

| 批次 | 目录 | Venue | CCF | 2024 | 2025 | 2026 | 本轮处理与风险 |
|---|---|---|---:|---:|---:|---:|---|
| P0-A | [`conf-a-icse`](../../../../ccf_venues/conf-a-icse/README.md) | ICSE | 🏆 | 🟠 | 🟠 | 🔴 | 年度 README / DBLP / proceedings 可作入口，但本轮自动抓取受 DBLP 429/断连和 track 混杂影响，只能作为 title-level gap-aware 粗筛。 |
| P0-A | [`conf-a-fse`](../../../../ccf_venues/conf-a-fse/README.md) | FSE | 🏆 | 🟠 | 🟠 | 🔴 | 年度 README / DBLP / proceedings 可作入口，但本轮自动抓取受 DBLP 429/断连和 track 混杂影响，只能作为 title-level gap-aware 粗筛。 |
| P0-A | [`conf-a-ase`](../../../../ccf_venues/conf-a-ase/README.md) | ASE | 🏆 | 🔵 | 🔵 | 🔴 | DBLP mirror 成功抓取 2024/2025 title；命中多条 LLM4SE 但未见 SLR 自动化直接主会论文；2026 未完整归档。 |
| P0-A | [`conf-a-issta`](../../../../ccf_venues/conf-a-issta/README.md) | ISSTA | 🏆 | 🟠 | 🟠 | 🔴 | 年度 README / DBLP / proceedings 可作入口，但本轮自动抓取受 DBLP 429/断连和 track 混杂影响，只能作为 title-level gap-aware 粗筛。 |
| P0-A | [`journal-a-tse`](../../../../ccf_venues/journal-a-tse/README.md) | TSE | 🏆 | 🟠 | 🟠 | 🔴 | 期刊可经 publisher / DBLP year page 粗枚举 title，但 abstract 与 online-first 年份归属不稳定；本轮未做逐篇 abstract。 |
| P0-A | [`journal-a-tosem`](../../../../ccf_venues/journal-a-tosem/README.md) | TOSEM | 🏆 | 🟠 | 🟠 | 🔴 | 期刊可经 publisher / DBLP year page 粗枚举 title，但 abstract 与 online-first 年份归属不稳定；本轮未做逐篇 abstract。 |
| P0-A | [`conf-b-models`](../../../../ccf_venues/conf-b-models/README.md) | MoDELS | 🥈 | 🟠 | 🟠 | 🔴 | 年度 README / DBLP / proceedings 可作入口，但本轮自动抓取受 DBLP 429/断连和 track 混杂影响，只能作为 title-level gap-aware 粗筛。 |
| P0-A | [`conf-b-re`](../../../../ccf_venues/conf-b-re/README.md) | RE | 🥈 | 🟠 | 🟠 | 🔴 | 年度 README / DBLP / proceedings 可作入口，但本轮自动抓取受 DBLP 429/断连和 track 混杂影响，只能作为 title-level gap-aware 粗筛。 |
| P0-A | [`journal-b-re`](../../../../ccf_venues/journal-b-re/README.md) | Requirements Engineering | 🥈 | 🟠 | 🟠 | 🔴 | 期刊可经 publisher / DBLP year page 粗枚举 title，但 abstract 与 online-first 年份归属不稳定；本轮未做逐篇 abstract。 |
| P0-A | [`journal-b-sosym`](../../../../ccf_venues/journal-b-sosym/README.md) | SoSyM | 🥈 | 🟠 | 🟠 | 🔴 | 期刊可经 publisher / DBLP year page 粗枚举 title，但 abstract 与 online-first 年份归属不稳定；本轮未做逐篇 abstract。 |
| P0-B | [`conf-a-fm`](../../../../ccf_venues/conf-a-fm/README.md) | FM | 🏆 | 🟠 | 🟠 | 🔴 | 年度 README / DBLP / proceedings 可作入口，但本轮自动抓取受 DBLP 429/断连和 track 混杂影响，只能作为 title-level gap-aware 粗筛。 |
| P0-B | [`conf-a-cav`](../../../../ccf_venues/conf-a-cav/README.md) | CAV | 🏆 | 🟠 | 🟠 | 🔴 | 年度 README / DBLP / proceedings 可作入口，但本轮自动抓取受 DBLP 429/断连和 track 混杂影响，只能作为 title-level gap-aware 粗筛。 |
| P0-B | [`conf-b-etaps`](../../../../ccf_venues/conf-b-etaps/README.md) | ETAPS / TACAS | 🥈 | 🟠 | 🟠 | 🔴 | 年度 README / DBLP / proceedings 可作入口，但本轮自动抓取受 DBLP 429/断连和 track 混杂影响，只能作为 title-level gap-aware 粗筛。 |
| P0-B | [`conf-b-vmcai`](../../../../ccf_venues/conf-b-vmcai/README.md) | VMCAI | 🥈 | 🟠 | 🟠 | 🔴 | 年度 README / DBLP / proceedings 可作入口，但本轮自动抓取受 DBLP 429/断连和 track 混杂影响，只能作为 title-level gap-aware 粗筛。 |
| P0-B | [`conf-b-issre`](../../../../ccf_venues/conf-b-issre/README.md) | ISSRE | 🥈 | 🟠 | 🟠 | 🔴 | 年度 README / DBLP / proceedings 可作入口，但本轮自动抓取受 DBLP 429/断连和 track 混杂影响，只能作为 title-level gap-aware 粗筛。 |
| P0-B | [`journal-b-stvr`](../../../../ccf_venues/journal-b-stvr/README.md) | STVR | 🥈 | 🟠 | 🟠 | 🔴 | 期刊可经 publisher / DBLP year page 粗枚举 title，但 abstract 与 online-first 年份归属不稳定；本轮未做逐篇 abstract。 |
| P0-B | [`conf-c-icfem`](../../../../ccf_venues/conf-c-icfem/README.md) | ICFEM | 🥉 | 🟠 | 🟠 | 🔴 | 年度 README / DBLP / proceedings 可作入口，但本轮自动抓取受 DBLP 429/断连和 track 混杂影响，只能作为 title-level gap-aware 粗筛。 |
| P0-B | [`conf-c-spin`](../../../../ccf_venues/conf-c-spin/README.md) | SPIN | 🥉 | 🟠 | 🟠 | 🔴 | 年度 README / DBLP / proceedings 可作入口，但本轮自动抓取受 DBLP 429/断连和 track 混杂影响，只能作为 title-level gap-aware 粗筛。 |
| P0-B | [`conf-c-atva`](../../../../ccf_venues/conf-c-atva/README.md) | ATVA | 🥉 | 🟠 | 🟠 | 🔴 | 年度 README / DBLP / proceedings 可作入口，但本轮自动抓取受 DBLP 429/断连和 track 混杂影响，只能作为 title-level gap-aware 粗筛。 |
| P0-B | [`conf-c-icst`](../../../../ccf_venues/conf-c-icst/README.md) | ICST | 🥉 | 🟠 | 🟠 | 🔴 | 年度 README / DBLP / proceedings 可作入口，但本轮自动抓取受 DBLP 429/断连和 track 混杂影响，只能作为 title-level gap-aware 粗筛。 |
| P0-B | [`conf-c-refsq`](../../../../ccf_venues/conf-c-refsq/README.md) | REFSQ | 🥉 | 🟠 | 🟠 | 🔴 | 年度 README / DBLP / proceedings 可作入口，但本轮自动抓取受 DBLP 429/断连和 track 混杂影响，只能作为 title-level gap-aware 粗筛。 |
| P0-B | [`journal-c-sttt`](../../../../ccf_venues/journal-c-sttt/README.md) | STTT | 🥉 | 🟠 | 🟠 | 🔴 | 期刊可经 publisher / DBLP year page 粗枚举 title，但 abstract 与 online-first 年份归属不稳定；本轮未做逐篇 abstract。 |
| P1 | [`conf-b-saner`](../../../../ccf_venues/conf-b-saner/README.md) | SANER | 🥈 | 🟠 | 🟠 | 🔴 | 年度 README / DBLP / proceedings 可作入口，但本轮自动抓取受 DBLP 429/断连和 track 混杂影响，只能作为 title-level gap-aware 粗筛。 |
| P1 | [`conf-b-icsme`](../../../../ccf_venues/conf-b-icsme/README.md) | ICSME | 🥈 | 🟠 | 🟠 | 🔴 | 年度 README / DBLP / proceedings 可作入口，但本轮自动抓取受 DBLP 429/断连和 track 混杂影响，只能作为 title-level gap-aware 粗筛。 |
| P1 | [`conf-b-icpc`](../../../../ccf_venues/conf-b-icpc/README.md) | ICPC | 🥈 | 🟠 | 🟠 | 🔴 | 年度 README / DBLP / proceedings 可作入口，但本轮自动抓取受 DBLP 429/断连和 track 混杂影响，只能作为 title-level gap-aware 粗筛。 |
| P1 | [`conf-b-esem`](../../../../ccf_venues/conf-b-esem/README.md) | ESEM | 🥈 | 🟠 | 🟠 | 🔴 | 年度 README / DBLP / proceedings 可作入口，但本轮自动抓取受 DBLP 429/断连和 track 混杂影响，只能作为 title-level gap-aware 粗筛。 |
| P1 | [`journal-b-ese`](../../../../ccf_venues/journal-b-ese/README.md) | ESE | 🥈 | 🟠 | 🟠 | 🔴 | 期刊可经 publisher / DBLP year page 粗枚举 title，但 abstract 与 online-first 年份归属不稳定；本轮未做逐篇 abstract。 |
| P1 | [`journal-b-jss`](../../../../ccf_venues/journal-b-jss/README.md) | JSS | 🥈 | 🟠 | 🟠 | 🔴 | 期刊可经 publisher / DBLP year page 粗枚举 title，但 abstract 与 online-first 年份归属不稳定；本轮未做逐篇 abstract。 |
| P1 | [`journal-b-ist`](../../../../ccf_venues/journal-b-ist/README.md) | IST | 🥈 | 🟠 | 🟠 | 🔴 | 期刊可经 publisher / DBLP year page 粗枚举 title，但 abstract 与 online-first 年份归属不稳定；本轮未做逐篇 abstract。 |
| P1 | [`journal-b-scp`](../../../../ccf_venues/journal-b-scp/README.md) | SCP | 🥈 | 🟠 | 🟠 | 🔴 | 期刊可经 publisher / DBLP year page 粗枚举 title，但 abstract 与 online-first 年份归属不稳定；本轮未做逐篇 abstract。 |
| P1 | [`journal-b-jsep`](../../../../ccf_venues/journal-b-jsep/README.md) | JSEP | 🥈 | 🟠 | 🟠 | 🔴 | 期刊可经 publisher / DBLP year page 粗枚举 title，但 abstract 与 online-first 年份归属不稳定；本轮未做逐篇 abstract。 |
| P1 | [`conf-c-qrs`](../../../../ccf_venues/conf-c-qrs/README.md) | QRS | 🥉 | 🟠 | 🟠 | 🔴 | 年度 README / DBLP / proceedings 可作入口，但本轮自动抓取受 DBLP 429/断连和 track 混杂影响，只能作为 title-level gap-aware 粗筛。 |
| P1 | [`conf-c-tase`](../../../../ccf_venues/conf-c-tase/README.md) | TASE | 🥉 | 🟠 | 🟠 | 🔴 | 年度 README / DBLP / proceedings 可作入口，但本轮自动抓取受 DBLP 429/断连和 track 混杂影响，只能作为 title-level gap-aware 粗筛。 |
| P1 | [`journal-c-sqj`](../../../../ccf_venues/journal-c-sqj/README.md) | SQJ | 🥉 | 🟠 | 🟠 | 🔴 | 期刊可经 publisher / DBLP year page 粗枚举 title，但 abstract 与 online-first 年份归属不稳定；本轮未做逐篇 abstract。 |
| P2 | [`conf-c-apsec`](../../../../ccf_venues/conf-c-apsec/README.md) | APSEC | 🥉 | 🟠 | 🟠 | 🔴 | 年度 README / DBLP / proceedings 可作入口，但本轮自动抓取受 DBLP 429/断连和 track 混杂影响，只能作为 title-level gap-aware 粗筛。 |
| P2 | [`conf-c-seke`](../../../../ccf_venues/conf-c-seke/README.md) | SEKE | 🥉 | 🟠 | 🟠 | 🔴 | 年度 README / DBLP / proceedings 可作入口，但本轮自动抓取受 DBLP 429/断连和 track 混杂影响，只能作为 title-level gap-aware 粗筛。 |
| P2 | [`conf-c-ease`](../../../../ccf_venues/conf-c-ease/README.md) | EASE | 🥉 | 🟠 | 🟠 | 🔴 | 年度 README / DBLP / proceedings 可作入口，但本轮自动抓取受 DBLP 429/断连和 track 混杂影响，只能作为 title-level gap-aware 粗筛。 |
| P2 | [`conf-c-msr`](../../../../ccf_venues/conf-c-msr/README.md) | MSR | 🥉 | 🟠 | 🟠 | 🔴 | 年度 README / DBLP / proceedings 可作入口，但本轮自动抓取受 DBLP 429/断连和 track 混杂影响，只能作为 title-level gap-aware 粗筛。 |
| P2 | [`conf-c-rv`](../../../../ccf_venues/conf-c-rv/README.md) | RV | 🥉 | 🟠 | 🟠 | 🔴 | 年度 README / DBLP / proceedings 可作入口，但本轮自动抓取受 DBLP 429/断连和 track 混杂影响，只能作为 title-level gap-aware 粗筛。 |
| P2 | [`journal-b-ase`](../../../../ccf_venues/journal-b-ase/README.md) | Automated Software Engineering Journal | 🥈 | 🟠 | 🟠 | 🔴 | 期刊可经 publisher / DBLP year page 粗枚举 title，但 abstract 与 online-first 年份归属不稳定；本轮未做逐篇 abstract。 |
| P2 | [`conf-b-caise`](../../../../ccf_venues/conf-b-caise/README.md) | CAiSE | 🥈 | 🟠 | 🟠 | 🔴 | 年度 README / DBLP / proceedings 可作入口，但本轮自动抓取受 DBLP 429/断连和 track 混杂影响，只能作为 title-level gap-aware 粗筛。 |
| P2 | [`conf-c-iceccs`](../../../../ccf_venues/conf-c-iceccs/README.md) | ICECCS | 🥉 | 🟠 | 🟠 | 🔴 | 年度 README / DBLP / proceedings 可作入口，但本轮自动抓取受 DBLP 429/断连和 track 混杂影响，只能作为 title-level gap-aware 粗筛。 |

## 2. 本轮 CCF title-level 命中

| 年份 | Venue | 标题 | 来源 | 分层 | D1 | D2 | D3 | D4 | D5 | D6 | D7 | 备注 |
|---:|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 2025 | WSESE@ICSE | On the Difficulties of Conducting and Replicating Systematic Literature Reviews Studies Using LLMs in Software Engineering | [DBLP](https://dblp.org/rec/conf/wsese/FelizardoDCGMGS25) | P1 | 🟢 | 🟡 | 🟡 | 🟡 | 🟠 | 🟢 | 🟡 | CCF-adjacent / ICSE workshop 命中，PDF 未自动获取，已写入 [manual-download-needed.bib](./manual-download-needed.bib)。 |

## 3. 缺口说明

- 本轮 CCF 部分主要是 title-level discovery，不是完整 abstract-level systematic screening。
- 2026 年多数 venue 尚未形成完整 proceedings / DBLP 年度页，统一视为 `year-not-published` 或 `paper-list-unavailable`。
- DBLP / publisher 自动抓取出现 429、断连、track 混杂时，必须保守标为 🟠/🔴；不得把这些缺口写成“无相关论文”。
- 若后续论文需要更强的 CCF 负证据，应另开 PR 对 42 个 venue 的 2024--2026 paper list 做机器可读导出和 abstract 补全。
