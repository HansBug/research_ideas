# 资源与复现实验资产 / ASSETS

更新时间：2026-06-10 11:32:00

状态口径：🟢 可直接访问；🟡 部分公开 / 可重建但不完整；🟠 未公开 / 仅论文内描述；🔒 受限私有资产 / 难以公开获取；❓ 入口存在但当前访问异常或未完成逐文件核验。

CCF 口径：🏆 CCF A；🥈 CCF B；🥉 CCF C；⚪ 非 CCF 推荐或不适用；❓ 未核验。

## 1. 资源总览

| 资源类型 | 状态 | URL / 路径 | 说明 |
|---|---|---|---|
| 论文 | 🟢 | [RUOR item](https://ruor.uottawa.ca/items/b3679a91-5445-45ce-b289-bfddba3010f6) / [PDF](https://ruor.uottawa.ca/bitstreams/75cf8d04-a540-4d48-ad54-b8f13b3df2e8/download) / [本地 PDF](./paper.pdf) | 公开硕士论文。 |
| 实验代码 | 🟠 | 未发现论文专属仓库；相关工具为 [umple/umple](https://github.com/umple/umple) 与 [umple/umpleonline](https://github.com/umple/umpleonline) | Umple 工具链公开，但不是该 thesis 的实验代码。 |
| 实验结果细则 | 🟠 | 论文内实验章节 | Zero-shot / One-shot / RAG 的 ICP、EUCP、Pass@K、CodeBLEU、Levenshtein 等结果只在论文中呈现。 |
| 数据集 / Benchmark | 🟡 | [Umple Requirements Examples](https://cruise.umple.org/umple/RequirementsExamples.html) | 五个系统例子可从 Umple 手册/示例重建，但论文 benchmark 组合、RAG 文档库和运行输出未独立打包。 |
| Artifact / 复现包 | 🟠 | 无 | 需要自行搭建 Llama 3 8B、Nomic embeddings、示例库和评测脚本。 |

## 2. Venue 与 CCF

- **论文**：Exploring How Well Llama3 can Generate State Machines Represented in Umple
- **发表 / 版本**：Master's Thesis, University of Ottawa, 2025
- **CCF 口径**：⚪
- **论文入口**：[RUOR item](https://ruor.uottawa.ca/items/b3679a91-5445-45ce-b289-bfddba3010f6) / [DOI](https://doi.org/10.20381/ruor-31249)

## 3. 实验代码核查

论文没有公开实验脚本。可复用的是 Umple 编译器/在线平台本身，而不是 thesis pipeline。

## 4. 数据集 / Benchmark 核查

测试系统包括 Blackjack、Course Section、Credit Card Transaction、Driver License 和 Hotel Stay；需求和 Umple 代码可参考 Umple 官方示例，但需要人工整理为论文格式。

## 5. 实验结果细则核查

论文内报告三种 prompting/RAG 设置的编译有效性、pass@k、CodeBLEU 和编辑距离；未提供下载表。

## 6. 对 Project 1 对比实验的可用性

适合借鉴短需求到状态机 DSL 代码生成和 RAG 选例设计；控制系统复杂性、层次/守卫/时间约束覆盖有限。

## 7. 风险与待复查

1. Umple 手册是活文档，复现实验需要冻结具体版本。
2. 相关仓库是工具链，不等价于论文实验 artifact。
3. 小样本示例可能被模型训练数据污染。
