# `behrmann03-real-time-data-structures`

## 条目定位

本目录对应 Gerd Behrmann 的博士论文 *Data Structures and Algorithms for the Analysis of Real Time Systems*。它在当前 `UPPAAL` 理论与技术文库中既是一个 thesis 级总入口，也是一个带内嵌子论文的父路径。

这里的根目录材料仍然是该条目的规范完整版本：

1. `paper.pdf`
2. `paper_content.txt`
3. `bibtex.bib`
4. `README.md`

`paper-intro/` 与 `paper-a/` 到 `paper-f/` 是从 thesis 中拆出的辅助阅读单元，用于定向进入不同主题；它们不单独计入 [../SUMMARY.md](../SUMMARY.md) 的顶层论文数。

## 子论文导航

当前子目录及作用如下：

1. [paper-intro/README.md](./paper-intro/README.md)
   - thesis introduction、overall framing、data-structure overview、`The Making of Uppaal`。
   - 建议作为进入这篇 thesis 的第一站。
2. [paper-a/README.md](./paper-a/README.md)
   - `Verification of Large State/Event Systems using Compositionality and Dependency Analysis`
   - 更偏 pre-timed 的符号验证背景。
3. [paper-b/README.md](./paper-b/README.md)
   - `Verification of Hierarchical State/Event Systems using Reusability and Compositionality`
   - 层次化 state/event systems 与 compositionality 背景。
4. [paper-c/README.md](./paper-c/README.md)
   - `Efficient Timed Reachability Analysis using Clock Difference Diagrams`
   - 与非凸 symbolic set、CDD、federation 替代表示最直接相关。
5. [paper-d/README.md](./paper-d/README.md)
   - `Minimum-Cost Reachability for Priced Timed Automata`
   - priced timed automata 路线的理论起点。
6. [paper-e/README.md](./paper-e/README.md)
   - `Efficient Guiding Towards Cost-Optimality in Uppaal`
   - 从 priced 分析走向 `UPPAAL` 引擎中的代价引导搜索。
7. [paper-f/README.md](./paper-f/README.md)
   - `As Cheap as Possible: Efficient Cost-Optimal Reachability for Priced Timed Automata`
   - priced zones / facets 路线的进一步展开。

## 推荐阅读顺序

如果只是想快速判断这篇 thesis 在 `UPPAAL` 理论与技术文库里的价值，建议按下面顺序走：

1. 先读本文件。
2. 再读 [paper-intro/README.md](./paper-intro/README.md)。
3. 然后按主题选择：
   - CDD / 非凸 symbolic set：继续看 [paper-c/README.md](./paper-c/README.md)
   - priced timed automata：继续看 [paper-d/README.md](./paper-d/README.md) -> [paper-e/README.md](./paper-e/README.md) -> [paper-f/README.md](./paper-f/README.md)
   - 作者更早的符号验证背景：看 [paper-a/README.md](./paper-a/README.md) 和 [paper-b/README.md](./paper-b/README.md)

## 处理约束

处理本目录时，默认顺序应为：

1. 先看本 `README.md` 了解 thesis 与子论文结构。
2. 再看根目录 `bibtex.bib` 和 `paper_content.txt`，掌握 thesis 级元信息与全局内容。
3. 如果需要针对某个子方向深入，再进入对应 `paper-*` 子目录。

当前这些 `paper-*` 子目录主要作为 thesis 内嵌论文的辅助阅读单元使用，因此默认复用父目录的 BibTeX 入口；若后续要把其中某篇提升为独立正式条目，再为该子目录单独补 `bibtex.bib`。
