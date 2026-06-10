# 资源与复现实验资产 / ASSETS

更新时间：2026-06-10 13:08:00

状态口径：🟢 可直接访问；🟡 部分公开 / 可重建但不完整；🟠 未公开 / 仅论文内描述；🔒 受限私有资产 / 难以公开获取；❓ 入口存在但当前访问异常或未完成逐文件核验。

CCF 口径：🏆 CCF A；🥈 CCF B；🥉 CCF C；⚪ 非 CCF 推荐或不适用；❓ 未核验。

## 1. 资源总览

| 资源类型 | 状态 | URL / 路径 | 说明 |
|---|---|---|---|
| 论文 | 🟢 | [HAL](https://telecom-paris.hal.science/hal-04483279) / [DOI](https://doi.org/10.5220/0012320100003645) / [本地 PDF](./paper.pdf) | 公开作者版与 DOI。 |
| 实验代码 | 🟡 | [zebradile/ttool-ai](https://github.com/zebradile/ttool-ai) / [TTool-AI page](https://ttool.telecom-paris.fr/ttoolai.html) | 仓库主要是实验工件，不是完整 TTool 源码；default branch `main`，HEAD `f2c52282cb7a826c31e7ab512356d42230c6d321`；复现需安装 TTool 并配置 OpenAI key。 |
| 实验结果细则 | 🟢 | [results.ods](https://github.com/zebradile/ttool-ai/blob/main/results.ods) / [raw pinned](https://raw.githubusercontent.com/zebradile/ttool-ai/f2c52282cb7a826c31e7ab512356d42230c6d321/results.ods) | 公开 OpenDocument Spreadsheet，包含时间与质量评分结果；本轮 raw header content-length 14893 bytes，ETag `5f2861a7687b8ef281f20149bf3f167068704d3d03aca60cc18d7dc4110f72e6`。 |
| 数据集 / Benchmark | 🟢 | [platooning](https://github.com/zebradile/ttool-ai/tree/main/platooning)、[spacebasedsystem](https://github.com/zebradile/ttool-ai/tree/main/spacebasedsystem)、[AutomatedBraking](https://github.com/zebradile/ttool-ai/tree/main/AutomatedBraking) | 公开系统规范 `.md` / `.desc` 与 TTool `.xml` 模型；另有 DPS、SNCS、attacktrees、incoherencies 补充工件。 |
| Artifact / 复现包 | 🟢 | [GitHub repo](https://github.com/zebradile/ttool-ai) | README 给出查看模型和复现实验步骤；结果会因 ChatGPT 随机性和版本漂移变化。 |

## 2. Venue 与 CCF

- **论文**：System Architects Are not Alone Anymore: Automatic System Modeling with AI
- **发表 / 版本**：MODELSWARD 2024
- **CCF 口径**：⚪
- **论文入口**：[HAL](https://telecom-paris.hal.science/hal-04483279) / [DOI](https://doi.org/10.5220/0012320100003645)

## 3. 实验代码核查

TTool-AI 能力在 TTool 工具中；该仓库主要公开实验输入、AI 生成模型、结果表和复现说明。严格来说是 artifact repo，而不是独立 Python/Java 框架源码。本轮核验到 GitHub default branch `main`，HEAD `f2c52282cb7a826c31e7ab512356d42230c6d321`；根目录含 `AutomatedBraking`、`DPS`、`SNCS_complementaryEvaluation`、`attacktrees`、`incoherencies`、`platooning`、`spacebasedsystem` 和 `results.ods`。

## 4. 数据集 / Benchmark 核查

核心三个系统是 platooning、spacebasedsystem、AutomatedBraking；每个目录包含自然语言系统规范和生成的 TTool XML 模型。仓库还含 `incoherencies`、`SNCS_complementaryEvaluation`、`attacktrees` 等扩展工件。

## 5. 实验结果细则核查

`results.ods` 是公开结果细则，README 说明质量分数与 master-level students 对比，并解释如何用 TTool 打开模型和重新调用 AI。复现还需要 TTool 安装、OpenAI key 和具体模型配置；TTool-AI 页面给出 `OPENAIKey` / `OPENAIModel` 等配置入口。

## 6. 对 Project 1 对比实验的可用性

这是最强的可复现实验资产之一，适合做 tool-assisted / feedback-loop baseline，对比自然语言到 SysML 块图+状态机联合生成。

## 7. 风险与待复查

1. 复现依赖 TTool nightly/版本和 OpenAI 模型，存在 provider drift。
2. README 明确结果受 ChatGPT 随机性影响，应将公开 XML/ODS 作为冻结 artifact，而非期望重跑完全一致。
3. 仓库非完整源码，若要改造 baseline 需要研究 TTool 本体；正式实验应固定 HEAD `f2c52282cb7a826c31e7ab512356d42230c6d321` 与 `results.ods` ETag。
