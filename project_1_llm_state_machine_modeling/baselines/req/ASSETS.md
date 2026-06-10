# 资源与复现实验资产 / ASSETS

更新时间：2026-06-10 11:32:00

状态口径：🟢 可直接访问；🟡 部分公开 / 可重建但不完整；🟠 未公开 / 仅论文内描述；🔒 受限私有资产 / 难以公开获取；❓ 入口存在但当前访问异常或未完成逐文件核验。

CCF 口径：🏆 CCF A；🥈 CCF B；🥉 CCF C；⚪ 非 CCF 推荐或不适用；❓ 未核验。

## 1. 资源总览

| 资源类型 | 状态 | URL / 路径 | 说明 |
|---|---|---|---|
| 论文 | 🟢 | [Chalmers ODR PDF](https://odr.chalmers.se/bitstreams/7c06ef2c-d1ae-40b4-b13c-a35087077bce/download) / [本地 PDF](./paper.pdf) | 公开硕士论文。 |
| 实验代码 | 🟠 | 未发现公开仓库 | 论文使用 Azure OpenAI、W&B 等工具链，但未提供代码或训练脚本。 |
| 实验结果细则 | 🟠 | 论文内结果章节 | 定量评估和专家评审结果只在论文中呈现；未发现可下载 workbook。 |
| 数据集 / Benchmark | 🔒 | 无公开入口 | 主数据来自 Volvo Cars / Car Weaver 的 20 个 product function requirements 与人工 statecharts；合成数据用于扩充和微调，均未公开。 |
| Artifact / 复现包 | 🟠 | 无 | 缺代码、训练数据、微调配置和专家评分原始表，不能直接复现。 |

## 2. Venue 与 CCF

- **论文**：Automated Statechart Generation from Natural Language Requirements Using AI Techniques in Automotive Software Engineering
- **发表 / 版本**：Master's Thesis, Chalmers University of Technology / University of Gothenburg, 2025
- **CCF 口径**：⚪
- **论文入口**：[Chalmers ODR PDF](https://odr.chalmers.se/bitstreams/7c06ef2c-d1ae-40b4-b13c-a35087077bce/download)

## 3. 实验代码核查

没有论文专属开源实现。方法链路包括需求预处理、合成数据生成、GPT-3.5/GPT-4/GPT-4o 微调或调用、Mermaid.js statechart 输出和专家评估。

## 4. 数据集 / Benchmark 核查

最关键资产是 Volvo Cars 内部 Car Weaver 需求和对应 statecharts，外部不可下载。论文提到 20 个 product functions，并用合成数据弥补样本不足。

## 5. 实验结果细则核查

实验结果包括功能正确性、可理解性、与需求对齐等论文内指标和专家评审；没有公开逐样本结果细则。

## 6. 对 Project 1 对比实验的可用性

任务与 Project 1 的 `NL requirements -> statechart` 高度贴近，特别适合做 related direct baseline 叙述；但不适合做可复跑对比基准。

## 7. 风险与待复查

1. 工业私有数据不可公开，无法复现原始训练/评估。
2. Azure OpenAI 微调和模型版本会漂移。
3. 若后续用作对比，只能重建类似任务，不能声称复现其原数据。
