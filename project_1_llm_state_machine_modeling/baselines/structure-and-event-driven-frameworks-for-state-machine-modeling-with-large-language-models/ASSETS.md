# 资源与复现实验资产 / ASSETS

更新时间：2026-06-10 15:33:00

状态口径：🟢 可直接访问；🟡 部分公开 / 可重建但不完整；🟠 未公开 / 仅论文内描述；🔒 受限私有资产 / 难以公开获取；❓ 入口存在但当前访问异常或未完成逐文件核验。

CCF 口径：🏆 CCF A；🥈 CCF B；🥉 CCF C；⚪ 非 CCF 推荐或不适用；❓ 未核验。

## 1. 资源总览

| 资源类型 | 状态 | URL / 路径 | 说明 |
|---|---|---|---|
| 论文 | 🟢 | [arXiv](https://arxiv.org/abs/2604.00275) / [本地 PDF](./paper.pdf) | 公开预印本；本地已提取 `paper_content.txt`。 |
| arXiv ancillary / 附属文件 | 🟠 | [arXiv abs](https://arxiv.org/abs/2604.00275) / [arXiv API](https://export.arxiv.org/api/query?id_list=2604.00275) | 2026-06-10 核验 arXiv API 仅列出 abs 与 PDF，未发现独立 ancillary artifact / 附属代码数据包；arXiv source 不等同实验代码或数据集。 |
| 实验代码 | 🟢 | [4open 浏览器入口](https://anonymous.4open.science/#!/r/llm_state_machine_modeling/) / [README 浏览器页](https://anonymous.4open.science/#!/r/llm_state_machine_modeling/README.md) / [README API](https://anonymous.4open.science/api/repo/llm_state_machine_modeling/file/README.md) | 2026-06-10 复核：Anonymous Github 的人类浏览入口应使用 `#!/r/...` hashbang 路由；普通 `/r/...` 是服务端重定向入口，会跳到 API 并可能返回 `401 {"error":"not_connected"}`。已核到 `app.py`、`requirements.txt`、`.env.example`、`backend/*_smf/*.py`、`actions/`、`backend/resources/*` 等。该仓库仍是匿名 artifact，不是实名 GitHub / Zenodo release。 |
| 实验结果细则 | 🟢 | [F1 workbook 浏览器页](https://anonymous.4open.science/#!/r/llm_state_machine_modeling/Paper%20Experiment%20Resources/Final%20Detailed%20F1-Scores.xlsx) / [F1 workbook API](https://anonymous.4open.science/api/repo/llm_state_machine_modeling/file/Paper%20Experiment%20Resources%2FFinal%20Detailed%20F1-Scores.xlsx) | 可下载 workbook，2026-06-10 核到大小 58,116 bytes，SHA-256 `fe3cb7e44820a1e73dcdc71f8d5218d19c0f75203544aea47d646afacf2a4bbf`；含 `SinglePrompt`、`StructureDriven`、`EventDriven`、`Hybrid`、`Averages` 五个 sheet，记录 GPT-4o / Claude 3.5 Sonnet 的 TP/FN/FP、precision、recall、F-score 和 image reference。 |
| 数据集 / Benchmark | 🟢 | [Reference Solutions 浏览器页](https://anonymous.4open.science/#!/r/llm_state_machine_modeling/Paper%20Experiment%20Resources/Reference%20Solutions) / [Reference Solutions API](https://anonymous.4open.science/api/repo/llm_state_machine_modeling/files/?path=Paper%20Experiment%20Resources%2FReference%20Solutions&v=) / [state_machine_descriptions.py 浏览器页](https://anonymous.4open.science/#!/r/llm_state_machine_modeling/backend/resources/state_machine_descriptions.py) | 已核到 8 个 reference solutions：`bread-maker`、`chess-clock`、`dishwasher`、`printer`、`spa-manager`、`ssc7`、`thermomix`、`wumple`，每个含 `.txt` 描述与 `.png` 参考状态机；另有 `state_machine_descriptions.py` 汇总实验系统描述。 |
| Artifact / 复现包 | 🟢 | [4open 浏览器入口](https://anonymous.4open.science/#!/r/llm_state_machine_modeling/) / [ZIP 冻结入口](https://anonymous.4open.science/api/repo/llm_state_machine_modeling/zip) | 复现包核心内容已通过浏览器 hashbang 入口和 ZIP 下载入口交叉核验：代码、prompt/example、8 个参考解、生成图片与 F1 workbook 均已核到；ZIP 入口 2026-06-10 可下载 `application/zip`，126 个条目，单次请求大小 3,357,298 bytes。因匿名 artifact 没有 Git commit、release、license 文件快照和正式 DOI，正式实验前仍应冻结本地副本，并优先记录逐文件 hash，而不是只记录整包 hash。 |

## 2. Venue 与 CCF

- **论文**：Structure- and Event-Driven Frameworks for State Machine Modeling with Large Language Models
- **发表 / 版本**：arXiv preprint, 2026, cs.SE
- **CCF 口径**：⚪
- **论文入口**：[arXiv:2604.00275](https://arxiv.org/abs/2604.00275) / [DOI](https://doi.org/10.48550/arXiv.2604.00275)

- **联系 / 申请路径**：论文首页给出 McGill 邮箱 `{samer.abdulkarim, evan.boyd, karl.bridi, alec.tufenkjian, boqi.chen}@mail.mcgill.ca` 与 `gunter.mussbacher@mcgill.ca`；由于当前 4open 浏览器 hashbang 入口、具体文件端点与 ZIP 冻结入口均已可访问，暂不需要邮件。只有在后续确认 license、索取 commit/release，或遇到浏览器入口 / ZIP / 文件端点失效时，才顺着论文给出的这些邮箱询问。

## 3. 实验代码核查

已通过 4open 浏览器 hashbang 页面、具体 API 文件端点和 ZIP 下载入口交叉核到核心源码。目录结构与 README 对齐：根目录含 `app.py`、`requirements.txt`、`.env.example`；`backend/event_driven_smf/`、`backend/simple_linear_smf/`、`backend/merged_simple_linear_smf/`、`backend/merged_event_driven_smf/` 分别存放 strategy 主入口、transition 定义和 actions；`backend/resources/` 存放 prompts、n-shot examples、system descriptions、Umple jar、utility 与 LLM tracker。

关键依赖以 `requirements.txt` 给出：`chainlit==1.2.0`、`openai==1.35.7`、`sherpa-ai==0.4.0`、`mermaid-py`、`aisuite`、`anthropic`、`groq`、`vertexai`、`ecologits`、`graphviz`、`pydantic==2.9.2` 等。`.env.example` 只列 API key 变量名，未暴露 key。

## 4. 4open / Anonymous Github 入口核查

本 artifact 的稳定人类浏览入口不是普通 `/r/...` 路径，而是 Anonymous Github 前端 hashbang 路由。2026-06-10 使用普通 HTTP 请求与 headless Chrome 交叉复核：

| 入口类型 | URL | 当前结论 | 用途 |
|---|---|---|---|
| 浏览器根入口 | [4open 浏览器入口](https://anonymous.4open.science/#!/r/llm_state_machine_modeling/) | headless Chrome 可渲染出 `Anonymous repository`、仓库名、`README.md`、`Paper Experiment Resources`、`Raw`、`Download`、`ZIP` 等 UI 元素，未出现 `not_connected` | 后续人工浏览、截图核验和资源导航的首选入口 |
| README 浏览器页 | [README 浏览器页](https://anonymous.4open.science/#!/r/llm_state_machine_modeling/README.md) | 可通过前端页面阅读 README；同一页面提供 raw/download/zip 操作入口 | 人类复查论文 artifact 说明 |
| 实验资源浏览页 | [Paper Experiment Resources 浏览器页](https://anonymous.4open.science/#!/r/llm_state_machine_modeling/Paper%20Experiment%20Resources) | 可进入实验资源目录；对二进制 workbook 建议配合下载入口核验 | 浏览实验结果、参考解和生成图片目录 |
| ZIP 冻结入口 | [ZIP API](https://anonymous.4open.science/api/repo/llm_state_machine_modeling/zip) | 2026-06-10 可下载 `application/zip`，单次请求 3,357,298 bytes，126 个条目；由于 ZIP 元数据可能导致整包 hash 随请求变化，正式冻结时应保存文件清单与逐文件 hash | 正式实验前冻结 artifact 副本 |
| 普通 `/r/...` 入口 | [普通 r 路由](https://anonymous.4open.science/r/llm_state_machine_modeling/) | HTTP 层会 302 到 `/api/repo/llm_state_machine_modeling/file/`，并可能返回 `401 {"error":"not_connected"}`；这不是 artifact 不存在，而是入口选错 | 不应作为人类浏览入口；只可记录为踩坑 |

2026-06-10 ZIP 抽样核到关键文件 hash：

| 文件 | 大小 | SHA-256 |
|---|---:|---|
| `README.md` | 5,079 bytes | `4f0d32a869f62179ea19f8cab538ffb56bdb6d5fbc738c03a2302284913fd42c` |
| `.env.example` | 117 bytes | `80dc29155020889aad675a571173b9cef5494eaff1050fd084770435d2cd29c2` |
| `requirements.txt` | 161 bytes | `dab6a3ab49148ef79bbb4daa56173067c80c3fdd04589aa4ed8bfc5fdab7210d` |
| `app.py` | 7,417 bytes | `6998c7b15e7b86d8b9713c4766bccc605b26df81cbc5f6562f61337abdf6b754` |
| `Paper Experiment Resources/Final Detailed F1-Scores.xlsx` | 58,116 bytes | `fe3cb7e44820a1e73dcdc71f8d5218d19c0f75203544aea47d646afacf2a4bbf` |
| `backend/resources/state_machine_descriptions.py` | 20,997 bytes | `013f88e3a7edaa05b02091513e7e7435ead6f8c11bd3f6bc78046fa80871c827` |

## 5. 数据集 / Benchmark 核查

论文实验数据的 8 个非结构化反应式系统描述与参考解已在 4open artifact 中核到。`Paper Experiment Resources/Reference Solutions/` 下包含 `bread-maker`、`chess-clock`、`dishwasher`、`printer`、`spa-manager`、`ssc7`、`thermomix`、`wumple` 的 `.txt` 与 `.png`；`backend/resources/state_machine_descriptions.py` 也包含系统描述文本。

需要注意：这些资源可通过 Anonymous Github hashbang 浏览器入口导航，并可通过具体 API 端点下载，但不是带 DOI 的归档数据集；正式 Project 1 对比前应下载冻结，并记录文件清单、关键文件大小与逐文件 SHA-256，避免匿名 artifact 过期或路径变化。

## 6. 实验结果细则核查

已核到可下载 `Final Detailed F1-Scores.xlsx`，含 `SinglePrompt`、`StructureDriven`、`EventDriven`、`Hybrid` 与 `Averages` 五个 sheet。表内按 system/component 记录 TP、FN、FP、precision、recall、F-score 和 image reference，可支撑逐策略、逐模型的结果复核。

同时，`Paper Experiment Resources/Final Single Prompt/`、`Final Structure-Driven/`、`Final Event-Driven/`、`Final Hybrid Approach/` 下按 GPT-4o 与 Claude 3.5 Sonnet 保存生成状态机图片。部分目录可见分片输出，例如 Printer / SSC7 / WUMPLE 在 GPT-4o Event-Driven 下存在 part 文件。

## 7. 对 Project 1 对比实验的可用性

方法任务与 Project 1 最贴近，自由文本到 UML 状态机，且评测维度细到状态机元素。当前 artifact 已能支撑比原先预期更强的复现实验准备：可直接读取 8 个输入 / reference、源码、prompt/example、生成图片和 F1 workbook。主要缺口是匿名 artifact 的长期可获取性、license、精确运行环境和 API/model drift；正式实验前应先冻结 artifact，再决定是否复跑。

## 8. 风险与待复查

1. 普通 [4open r 路由](https://anonymous.4open.science/r/llm_state_machine_modeling/) 会重定向到 `/api/repo/llm_state_machine_modeling/file/` 并返回 `401 {"error":"not_connected"}`；后续应使用 [hashbang 浏览器入口](https://anonymous.4open.science/#!/r/llm_state_machine_modeling/) 作为人类入口，并把具体 API / ZIP 作为 raw fallback 与冻结入口。
2. Anonymous Github artifact 不提供稳定 Git commit、release、Zenodo DOI 或长期归档承诺；正式实验前必须冻结本地副本并记录文件清单与逐文件 hash。整包 ZIP hash 可能受归档元数据影响，不宜作为唯一复现锚点。
3. 当前已核到代码和结果，但尚未真实安装运行；复跑仍需配置 LLM API key、Graphviz、Java、Umple jar 和 provider 依赖，并记录模型 drift。
4. 暂不需要邮件；只有在 artifact 端点失效、需要 license/commit/release、或需要作者确认实验设置时，才顺着论文首页给出的邮箱联系。
