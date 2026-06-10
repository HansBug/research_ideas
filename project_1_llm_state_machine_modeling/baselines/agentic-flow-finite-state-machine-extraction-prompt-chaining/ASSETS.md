# 资源与复现实验资产 / ASSETS

更新时间：2026-06-10 11:32:00

状态口径：🟢 可直接访问；🟡 部分公开 / 可重建但不完整；🟠 未公开 / 仅论文内描述；🔒 受限私有资产 / 难以公开获取；❓ 入口存在但当前访问异常或未完成逐文件核验。

CCF 口径：🏆 CCF A；🥈 CCF B；🥉 CCF C；⚪ 非 CCF 推荐或不适用；❓ 未核验。

## 1. 资源总览

| 资源类型 | 状态 | URL / 路径 | 说明 |
|---|---|---|---|
| 论文 | 🟢 | [arXiv](https://arxiv.org/abs/2507.11222) / [本地 PDF](./paper.pdf) | 公开预印本；本地已提取 `paper_content.txt`。 |
| 实验代码 | 🟠 | [YoussefMaklad/FlowFSM](https://github.com/YoussefMaklad/FlowFSM) | 仓库为 paper-specific 入口，但当前只有 `README.md` 和 `.gitignore`；README 写明 source code will be shared later。 |
| 实验结果细则 | 🟠 | 论文内 Table I | FTP / RTSP 的 TP、FP、FN、precision、recall、F1 仅见论文表；未发现可下载逐转移结果。 |
| 数据集 / Benchmark | 🟡 | [RFC 959 FTP](https://www.rfc-editor.org/rfc/rfc959) | 输入 RFC 是公开文档；RTSP 具体 RFC 版本正文未明确锁定，ground truth / rulebook / chunk 未公开。 |
| Artifact / 复现包 | 🟠 | [GitHub repo shell](https://github.com/YoussefMaklad/FlowFSM) | 入口存在但没有源码、数据或结果包；目前不能直接复现实验。 |

## 2. Venue 与 CCF

- **论文**：An Agentic Flow for Finite State Machine Extraction using Prompt Chaining
- **发表 / 版本**：arXiv preprint, 2025, cs.CL
- **CCF 口径**：⚪
- **论文入口**：[arXiv:2507.11222](https://arxiv.org/abs/2507.11222)

## 3. 实验代码核查

论文称基于 CrewAI 组织 RFC processing、context retrieval 与 stepwise FSM extraction；当前 GitHub 只保留即将开放源码的说明。

## 4. 数据集 / Benchmark 核查

公开可追溯输入主要是 RFC 文档，论文实验覆盖 FTP 与 RTSP；作者用于计算 TP/FP/FN 的人工 ground truth 和抽取结果未公开。

## 5. 实验结果细则核查

论文报告 FTP precision 83.33%、recall 88.24%、F1 85.71%；RTSP precision 81.82%、recall 85.71%、F1 83.72%。这些是论文内结果，不是可下载结果文件。

## 6. 对 Project 1 对比实验的可用性

适合借鉴 long-document protocol FSM extraction、prompt chaining 和 rulebook 中间表示；不适合直接作为控制系统需求 benchmark。

## 7. 风险与待复查

1. 仓库壳不能支撑复现实验。
2. RTSP 输入版本和 ground truth 未冻结，重建时存在口径漂移。
3. 协议 FSM 与控制系统状态机同构但领域差异大，baseline 对比需单独解释。
