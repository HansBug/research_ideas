# artifacts: sefm-llm-state-machine

## Artifact 结论

| 项 | 当前状态 | 结论 |
|---|---|---|
| PDF | present | 本地已有 `paper.pdf`；BibTeX 指向 arXiv:2604.00275 / DOI `10.48550/arXiv.2604.00275`。 |
| paper_content.txt | present | 本地已有全文抽取；Page 1-6 足以支撑 P1/P2/P3/P4 判定。 |
| BibTeX | present | 与源目录 `bibtex.bib` 一致：arXiv preprint, 2026, `cs.SE`。 |
| Code / artifact | usable with risk | 源目录 `ASSETS.md` 已核到 4open hashbang 浏览入口、README/API 文件端点、ZIP 入口、源码、prompt/example 和依赖文件。 |
| Dataset / outputs | usable with risk | 已核到 8 个 reference solutions、`state_machine_descriptions.py`、生成图片和 `Final Detailed F1-Scores.xlsx`。 |
| License / redistribution | citation note | 公开学术 artifact 后续论文引用原作即可；不作为 R2.0 升绿 blocker。 |
| Conversion readiness | pending | 可作为 R2 输入候选，但需先冻结 artifact、本地清单、逐文件 hash 和最小 smoke。 |

## 已核 artifact 指针

| 类型 | URL / 路径 | 稳定性判断 |
|---|---|---|
| arXiv paper | <https://arxiv.org/abs/2604.00275> | 稳定；论文与 DOI 可作为 bibliographic anchor。 |
| DOI | <https://doi.org/10.48550/arXiv.2604.00275> | 稳定；仅覆盖论文，不覆盖实验 artifact。 |
| 4open 浏览器入口 | <https://anonymous.4open.science/#!/r/llm_state_machine_modeling/> | 当前可访问；源目录已记录普通 `/r/...` 路由会误入 API/401，不应作为人工入口。 |
| README API | <https://anonymous.4open.science/api/repo/llm_state_machine_modeling/file/README.md> | 当前可作为 raw fallback；仍是 anonymous artifact 端点。 |
| ZIP 入口 | <https://anonymous.4open.science/api/repo/llm_state_machine_modeling/zip> | 当前可下载；源目录记录 126 个条目、约 3.36 MB，但整包 hash 可能受 ZIP 元数据影响。 |
| 源目录资源账本 | [`ASSETS.md`](../../../../baselines/structure-and-event-driven-frameworks-for-state-machine-modeling-with-large-language-models/ASSETS.md) | 本次 artifact/version/hash/URL 判断的主要本地证据源。 |

## 源目录已记录的关键 hash

| 文件 | 大小 | SHA-256 |
|---|---:|---|
| `README.md` | 5,079 bytes | `4f0d32a869f62179ea19f8cab538ffb56bdb6d5fbc738c03a2302284913fd42c` |
| `.env.example` | 117 bytes | `80dc29155020889aad675a571173b9cef5494eaff1050fd084770435d2cd29c2` |
| `requirements.txt` | 161 bytes | `dab6a3ab49148ef79bbb4daa56173067c80c3fdd04589aa4ed8bfc5fdab7210d` |
| `app.py` | 7,417 bytes | `6998c7b15e7b86d8b9713c4766bccc605b26df81cbc5f6562f61337abdf6b754` |
| `Paper Experiment Resources/Final Detailed F1-Scores.xlsx` | 58,116 bytes | `fe3cb7e44820a1e73dcdc71f8d5218d19c0f75203544aea47d646afacf2a4bbf` |
| `backend/resources/state_machine_descriptions.py` | 20,997 bytes | `013f88e3a7edaa05b02091513e7e7435ead6f8c11bd3f6bc78046fa80871c827` |

## R2 前置检查

1. 下载并冻结 ZIP 到 run record 或 artifact cache，不只依赖远程 4open URL。
2. 生成完整文件清单与逐文件 SHA-256；整包 hash 只作辅助。
3. 记录公开学术 artifact 的引用入口、访问日期和版本 / hash；许可 / 再分发不作为升绿 blocker。
4. 建立最小 smoke：读取 8 个 system descriptions/reference solutions、检查 prompt/example、打开 F1 workbook sheet。
5. 若要复跑，必须记录 API provider、精确 model id、调用日期、temperature、max tokens、依赖版本、Java/Graphviz/Umple 状态和 `.env` redaction。

## 当前 artifact grade

`SA-2`：资源可访问且有代码/数据/结果证据，足以支持冻结和后续 R2 准备；但长期 URL 稳定性、commit/release/DOI 和真实复跑证据不足，暂不升级为 `SA-1`。

## R2.0 registry 口径更新

一手 registry 口径起，本条目不得把 `Reference Solutions/*.txt` 计为 generated `STM_0`。真正可候选的 generated seed 必须来自 4open ZIP 中 `backend/resources/state_machine_descriptions.py` 的 NL 描述与 `Paper Experiment Resources/Final Single Prompt/Claude Sonnet 3.5/SSC7_single_prompt_*.txt` 等作者生成输出的可回溯配对。当前本条目已在 [assets/README.md](./assets/README.md) 下 committed 4open ZIP，并抽取 1 组 SSC7 `NL + Claude Sonnet 3.5 single-prompt generated Umple` pair；该 pair 已通过 raw ZIP hash、ZIP member locator、Python symbol 与文本 hash 回溯，eligible generated seed count 为 1。公开学术 artifact 按引用原作处理后，该 pair 当前为 `final_pool_ready`；但只有 SSC7 具备 generated text output，其余 8 个 NL 不能计为 generated pair，reference solutions 只能作为评价参考。
