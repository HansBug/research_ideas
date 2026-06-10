# 资源与复现实验资产 / ASSETS

更新时间：2026-06-10 13:08:00

状态口径：🟢 可直接访问；🟡 部分公开 / 可重建但不完整；🟠 未公开 / 仅论文内描述；🔒 受限私有资产 / 难以公开获取；❓ 入口存在但当前访问异常或未完成逐文件核验。

CCF 口径：🏆 CCF A；🥈 CCF B；🥉 CCF C；⚪ 非 CCF 推荐或不适用；❓ 未核验。

## 1. 资源总览

| 资源类型 | 状态 | URL / 路径 | 说明 |
|---|---|---|---|
| 论文 | 🟢 | [arXiv](https://arxiv.org/abs/2604.00275) / [本地 PDF](./paper.pdf) | 公开预印本；本地已提取 `paper_content.txt`。 |
| 实验代码 | 🟠 | 未发现实名 GitHub / Zenodo 仓库 | 正文只给匿名 4open 工件入口；当前无法确认源码可访问。 |
| 实验结果细则 | 🟠 | 论文内表格 | 未找到可下载逐样本结果文件；precision / recall / F1 细节主要在论文表格中。 |
| 数据集 / Benchmark | ❓ | [anonymous.4open.science/r/llm_state_machine_modeling](https://anonymous.4open.science/r/llm_state_machine_modeling/) | 论文称工件在线可得，实验含 8 个 non-structured reactive-system descriptions 与专家参考状态机；本轮 CLI 访问 `api/repo/.../file/` 返回 403 Forbidden。 |
| Artifact / 复现包 | ❓ | [4open artifact](https://anonymous.4open.science/r/llm_state_machine_modeling/) | 入口存在但 CLI 当前返回 403 Forbidden，未证实可下载；需浏览器登录 / 匿名评审连接态、等待工件公开或联系作者。 |

## 2. Venue 与 CCF

- **论文**：Structure- and Event-Driven Frameworks for State Machine Modeling with Large Language Models
- **发表 / 版本**：arXiv preprint, 2026, cs.SE
- **CCF 口径**：⚪
- **论文入口**：[arXiv:2604.00275](https://arxiv.org/abs/2604.00275) / [DOI](https://doi.org/10.48550/arXiv.2604.00275)

## 3. 实验代码核查

未核到可运行源码。论文方法可依据文本重实现四条 pipeline：single-prompt、structure-driven、event-driven 和 hybrid，但这不是作者 artifact 复现。

## 4. 数据集 / Benchmark 核查

论文实验数据是 8 个非结构化反应式系统描述及其参考 UML 状态机；当前可见信息不足以直接下载这些描述和 ground truth；4open 入口更像匿名评审门禁 / 认证态资源，不能写成已公开 benchmark。

## 5. 实验结果细则核查

论文给出了按 states / transitions / guards / actions / hierarchy / parallel / history 等槽位的 precision、recall、F1；未核到逐样本输出文件。

## 6. 对 Project 1 对比实验的可用性

方法任务与 Project 1 最贴近，自由文本到 UML 状态机，且评测维度细到状态机元素。当前主要价值是方法结构和评测维度借鉴；若 artifact 放开，可成为高优先级可复现 baseline。

## 7. 风险与待复查

1. 4open 入口当前 CLI 核验为 403 Forbidden，不能把数据或代码写成已公开可用。
2. 匿名工件可能随审稿状态变化，后续应定期复查；若需要用于复现实验，应通过作者邮箱或 McGill 团队页面询问 artifact 公开计划。
3. 若自行重实现，需要在 run record 中明确与原始实现不同。
