# `bengtsson02-clocks-dbms-states`

## 条目定位

本目录对应 Johan Bengtsson 的博士论文 *Clocks, DBMs and States in Timed Systems*。它在当前 `UPPAAL` 文库中是最贴近 DBM 本体与实现语义的一篇 thesis 级条目，同时也是一个带内嵌子论文的父路径。

这里的根目录材料仍然是该条目的规范完整版本：

1. `paper.pdf`
2. `paper_content.txt`
3. `bibtex.bib`
4. `README.md`

`paper-a/` 到 `paper-e/` 是从 thesis 中拆出的辅助阅读单元，用于分别进入 DBM、normalization、存储压缩、partial-order reduction 和 `UPPAAL` 工业案例这几条子线；它们不单独计入 `uppaal/SUMMARY.md` 的顶层论文数。

## 子论文导航

当前子目录及作用如下：

1. [paper-a/README.md](./paper-a/README.md)
   - `DBM: Structures, Operations and Implementation`
   - 最接近 DBM 基础操作和实现假设。
2. [paper-b/README.md](./paper-b/README.md)
   - `Reachability Analysis of Timed Automata Containing Constraints on Clock Differences`
   - 最接近 difference constraints 与 normalization 问题。
3. [paper-c/README.md](./paper-c/README.md)
   - `Reducing Memory Usage in Symbolic State-Space Exploration for Timed Systems`
   - 最接近存储压缩、passed list 压力和 `mingraph` 一类问题。
4. [paper-d/README.md](./paper-d/README.md)
   - `Partial Order Reductions for Timed Systems`
   - 偏 local-time semantics 与 partial-order reduction。
5. [paper-e/README.md](./paper-e/README.md)
   - `Automated Verification of an Audio-Control Protocol using UPPAAL`
   - 偏 committed locations 与 `UPPAAL` 工业案例。

## 推荐阅读顺序

如果你的目标是理解 DBM 与 UDBM 语义主线，建议按下面顺序走：

1. 先读本文件。
2. 再读根目录 `bibtex.bib` 和 `paper_content.txt`，掌握 thesis 级背景。
3. 然后按实现路线看：
   - DBM 基础： [paper-a/README.md](./paper-a/README.md)
   - difference constraints / normalization： [paper-b/README.md](./paper-b/README.md)
   - 存储压缩： [paper-c/README.md](./paper-c/README.md)
4. 若还需要更高层的引擎或案例背景，再看 [paper-d/README.md](./paper-d/README.md) 和 [paper-e/README.md](./paper-e/README.md)。

## 处理约束

处理本目录时，默认顺序应为：

1. 先看本 `README.md` 了解 thesis 与子论文结构。
2. 再看根目录 `bibtex.bib` 和 `paper_content.txt`，掌握 thesis 级元信息与全局内容。
3. 如果需要针对某个子问题深入，再进入对应 `paper-*` 子目录。

当前这些 `paper-*` 子目录主要作为 thesis 内嵌论文的辅助阅读单元使用，因此默认复用父目录的 BibTeX 入口；若后续要把其中某篇提升为独立正式条目，再为该子目录单独补 `bibtex.bib`。
