# 资源与复现实验资产 / ASSETS

更新时间：2026-06-10 13:23:56

状态口径：🟢 可直接访问；🟡 部分公开 / 可重建但不完整；🟠 未公开 / 仅论文内描述；🔒 受限私有资产 / 难以公开获取；❓ 入口存在但当前访问异常或未完成逐文件核验。

CCF 口径：🏆 CCF A；🥈 CCF B；🥉 CCF C；⚪ 非 CCF 推荐或不适用；❓ 未核验。

## 1. 资源总览

| 资源类型 | 状态 | URL / 路径 | 说明 |
|---|---|---|---|
| 论文 | 🟢 | [arXiv](https://arxiv.org/abs/2510.14348) / [本地 PDF](./paper.pdf) | 公开预印本；本地已提取 `paper_content.txt`。 |
| arXiv ancillary / 附属文件 | 🟠 | [arXiv abs](https://arxiv.org/abs/2510.14348) / [arXiv API](https://export.arxiv.org/api/query?id_list=2510.14348) | 2026-06-10 核验 arXiv API 仅列出 abs 与 PDF，未发现独立 ancillary artifact / 附属代码数据包；arXiv source 不等同实验代码或数据集。 |
| 实验代码 | 🟠 | 未发现公开仓库 | 论文说明实现了 SpecGPT，但正文和参考文献未提供项目主页或源码。 |
| 实验结果细则 | 🟠 | 论文内表格 | 状态/转移抽取的 precision、recall、F1 见论文；未发现可下载逐转移结果或模型输出。 |
| 公开输入规格 | 🟡 | [3GPP TS 24.501](https://www.3gpp.org/dynareport/24501.htm)、[TS 38.413](https://www.3gpp.org/dynareport/38413.htm)、[TS 29.244](https://www.3gpp.org/dynareport/29244.htm) | 3GPP 输入规格官方公开，但 dynareport 是活入口；复现必须锁定论文使用的 Release 17 具体版本。 |
| Benchmark / GT | 🟠 | 未公开 | 作者手工构建的 NAS/NGAP/PFCP Release 17 ground truth 未公开；论文未提供公开申请表、Zenodo / OSF / Figshare / Drive 或补充材料。 |
| Artifact / 复现包 | 🟠 | 无 | 没有公开复现包；需要自行下载 3GPP 规格并重建 chunking、prompt、ensemble 和 GT。 |

## 2. Venue 与 CCF

- **论文**：Automated Extraction of Protocol State Machines from 3GPP Specifications with Domain-Informed Prompts and LLM Ensembles
- **发表 / 版本**：arXiv preprint, 2025, cs.NI
- **CCF 口径**：⚪
- **论文入口**：[arXiv:2510.14348](https://arxiv.org/abs/2510.14348)

- **联系 / 申请路径**：论文首页给出作者邮箱 `1152461073@qq.com`、`fengrunhan@pmlabs.com.cn`、`tahobo@sina.com`、`itsyz@foxmail.com`、`yjcsu@126.com`、`qiuhang_ndsc@163.com`（PDF 文本抽取中空格异常，按邮箱格式归一）、`liuqi@pmlabs.com.cn`；若需要 Release 17 ground truth、SpecGPT 代码或逐转移结果，只能通过作者 / 机构渠道询问，不能写成已有公开 benchmark。

## 3. 实验代码核查

未核到 SpecGPT 源码。复现需要自行实现 3GPP 文档清洗、section window、状态/条件/动作抽取、JSON 后处理和多数投票。

## 4. 数据集 / Benchmark 核查

输入是官方 3GPP dynareport 入口；ground truth 是作者投入超过 210 人时构建并交叉验证的 NAS/NGAP/PFCP 状态机数据集，但未公开。这里必须区分“公开输入规格”和“公开 benchmark”：只有前者可直接访问，后者需要自行重建或联系作者询问。

## 5. 实验结果细则核查

论文报告 NAS ensemble transition F1 约 91.14%、PFCP-all F1 约 87.80%、NGAP-all F1 约 69.31%，并指出直接 prompt baseline F1 约 14.87%；无下载结果表。

## 6. 对 Project 1 对比实验的可用性

适合借鉴长规格切分、领域提示、pseudo-state 清理和多模型 ensemble；对 Project 1 可作为长文档 FSM 抽取 baseline，但不是控制系统需求直接数据源。

## 7. 风险与待复查

1. 3GPP 标准页是活文档，复现必须锁定 Release 17 具体版本，不能只记录 dynareport 入口页。
2. 缺源码和 GT，使端到端复现实验成本很高；如需原 GT，只能通过论文作者邮箱或机构渠道询问，不应声称已有公开 benchmark。
3. 若只引用论文表格，不能声称拥有可公开 benchmark。
