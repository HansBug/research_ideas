# 资源与复现实验资产 / ASSETS

更新时间：2026-06-10 13:08:00

状态口径：🟢 可直接访问；🟡 部分公开 / 可重建但不完整；🟠 未公开 / 仅论文内描述；🔒 受限私有资产 / 难以公开获取；❓ 入口存在但当前访问异常或未完成逐文件核验。

CCF 口径：🏆 CCF A；🥈 CCF B；🥉 CCF C；⚪ 非 CCF 推荐或不适用；❓ 未核验。

## 1. 资源总览

| 资源类型 | 状态 | URL / 路径 | 说明 |
|---|---|---|---|
| 论文 | 🟢 | [ACL Anthology](https://aclanthology.org/2025.ranlp-1.137/) / [本地 PDF](./paper.pdf) | 公开论文页与 PDF；本轮未发现 ACL Anthology supplementary、GitHub、OSF、Zenodo 或独立数据包入口。 |
| 实验代码 | 🟠 | 未发现公开仓库 | 未核到 paper-specific code。 |
| 实验结果细则 | 🟠 | 论文内表格 | 没有独立结果 workbook、生成输出包或 supplementary；结果主要在论文正文表格与 SME 反馈中。 |
| 数据集 / Benchmark | 🟠 | 无独立下载页 | 实验围绕 air purifier 与 vacuum 两个 MBSE 题项；题项和结果主要在论文中，没有标准 benchmark 包。 |
| Artifact / 复现包 | 🟠 | 无 | 需要手工重建 prompt、local LLM、temperature 设置和 SME 评分。 |

## 2. Venue 与 CCF

- **论文**：Pushing the (Generative) Envelope: Measuring the Effect of Prompt Technique and Temperature on the Generation of Model-based Systems Engineering Artifacts
- **发表 / 版本**：RANLP 2025
- **CCF 口径**：⚪
- **论文入口**：[ACL Anthology](https://aclanthology.org/2025.ranlp-1.137/) / [DOI](https://doi.org/10.26615/978-954-452-098-4-137)

## 3. 实验代码核查

没有公开实验脚本；ACL Anthology 页面仅核到论文 PDF，未发现独立 supplementary / code / dataset 附件。论文方法是本地 LLM 在不同 prompt technique 和 temperature 下重复生成 SysML v2 requirements list 与 state machine diagrams。

## 4. 数据集 / Benchmark 核查

只有两个题项，air purifier 与 vacuum；没有标准 benchmark 包。

## 5. 实验结果细则核查

论文内报告 prompt technique 和 temperature 对 requirements list / state machine diagram 生成质量的影响，使用 METEOR 与 SME 反馈；无逐次输出文件。

## 6. 对 Project 1 对比实验的可用性

可作为 prompt / temperature 敏感性和本地模型可用性的参考，不应作为强可复跑 baseline。

## 7. 风险与待复查

1. 样本极小，外推性弱。
2. 无代码、数据包、supplementary 和可下载结果细则，后续对比需要完全重建。
3. RANLP 不在当前 CCF 推荐目录口径内。
