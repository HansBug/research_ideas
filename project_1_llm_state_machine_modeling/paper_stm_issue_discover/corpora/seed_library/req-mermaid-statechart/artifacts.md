# req-mermaid-statechart artifacts

| 资源 | 状态 | 证据 / 路径 | 说明 |
|---|---|---|---|
| 论文 PDF | 可用 | `paper.pdf` / [源目录](../../../../baselines/req/) | 公开 Chalmers 硕士论文，本目录已复制。 |
| 文本提取 | 可用 | `paper_content.txt` | 源目录已有文本提取，本目录已复制。 |
| BibTeX | 可用 | `bibtex.bib` | 源目录已有 BibTeX，本目录已复制。 |
| 代码 | 未公开 | [`baselines/req/ASSETS.md`](../../../../baselines/req/ASSETS.md) | 未发现公开仓库、训练脚本或评估脚本。 |
| 原始数据 / benchmark | 私有 | Volvo Cars / Car Weaver | 20 个 product functions、人工 statecharts、12 个 expert test cases 与合成扩充数据均未公开。 |
| 输出 statecharts | 未公开 | 论文内示例 / 评估描述 | 无机器可读 Mermaid 输出包或逐样本结果表。 |
| 引用 / 来源说明 | 私有数据未公开 | 无公开下载入口 | 核心问题是工业需求、人工 statecharts 与专家测试未公开，无法形成一手 trace；许可 / 再分发不作为额外升绿阻塞。 |

## R2 使用建议

- 可作为 related work 中“任务高度贴近但 artifact 受限”的代表。
- 不计入 PR-R2 主 seed 可交接下限。
- 若要借鉴其工业任务形态，应另建公开 / 可授权的 synthetic 或 student-written seed，并保留构造 provenance。
