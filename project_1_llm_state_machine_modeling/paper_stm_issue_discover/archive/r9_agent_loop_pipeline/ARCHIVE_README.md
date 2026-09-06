# R9 单 Agent discover 实现快照（cold archive）· 复活导引

> **Cold archive / deprecated historical snapshot / 代码完整可跑。** 本目录保存 paper1 的**上一版 discover 实现**——一个顶层 Discover Agent 加 11 个工具的单 Agent 编排，包名 `paper_stm_repair_loop`。它已被 [../legacy/feedback_loop/](../legacy/feedback_loop/) 取代，不在运行路径上，论文的任何数字都不来自这里。
>
> ⚠️ **不要把归档理由读成「这版是失败品」。** 当前实现的断言语义与求值环境（`assertions/`）就是从这里移植出去的，见 §2。归档是因为**编排范式换了**，不是因为代码不能用。
>
> ⚠️ **本文件是归档时新写的复活导引，不是冻结原件。** 冻结原件是 [agent_loop/README.md](./agent_loop/README.md)（27 KB 的完整设计记录）。那份**未做内容修订**，其中的命令路径已过时——先读本文件 §4 与 §6，再读它。
>
> 上级入口：[../README.md](../README.md)。

## 0. 归档来源与时间考据

| 字段 | 值 |
| :-- | :-- |
| 原路径 | `paper_stm_issue_discover/pipeline/agent_loop/` |
| 现路径 | `paper_stm_issue_discover/archive/r9_agent_loop_pipeline/agent_loop/` |
| 归档时间 | 2026-08-11 |
| 归档动作 | `git mv pipeline/agent_loop archive/r9_agent_loop_pipeline/agent_loop` |
| 归档依据 | 用户明确裁定「归档」；前提是 `feedback_loop` 与 `discover_matrix` 对本树**零 import**（见 §5.1 复验命令） |
| 文件数 | **219 个被跟踪文件**（另有 5 个 `.pytest_cache/` 产物被 `.gitignore` 第 1004 行的通用 `.pytest_cache/` 规则忽略，合计 224）；其中 Python 92 个、约 29.4k 行 |
| 内容变换 | 219 个文件**全部为 rename，blob 哈希逐一比对完全一致**；此外只做了归档允许的机械变换：4 处路径深度重算 ＋ 8 条相对链接深度重算（逐条列在 §6） |
| 内容冻结点 | 最后一次实质改动见 `git log -- <原路径>`：`28c00131`（Markdown 不折行）、`df7ae9e5`（文档树化）、`35eba126`（`paper_stm_repair` 更名） |
| 当前事实源替代入口 | [../legacy/feedback_loop/](../legacy/feedback_loop/)；实验数字回 [../../discover_matrix/](../../discover_matrix/) |

### 0.1 ⛔ 与另外两个同名物的区分

仓库里有三个东西名字都带 "agent loop"，**互不相同**，不要混：

| 对象 | 是什么 | 状态 |
| :-- | :-- | :-- |
| **本目录** `archive/r9_agent_loop_pipeline/` | paper1 的**单 Agent discover 实现**，包 `paper_stm_repair_loop`；输入 `<NL, STM_0>`，输出 issue 台账 | 本次归档 |
| [../../../archive/agent_loop_method/](../../../archive/agent_loop_method/) | project_1 层的 **16-stage LangGraph 建模 loop**（`SC-0 -> ... -> SC-13`），做的是 NL **→ STM 生成**，服务 Path-1/Path-2 | 更早已归档 |
| [../legacy/feedback_loop/](../legacy/feedback_loop/) | 本快照的后续历史 discover 实现，包 `paper_stm_feedback_loop` | historical |

判据：**包名**。`paper_stm_repair_loop` = 本目录；`paper_stm_feedback_loop` = 当前实现；`archive.agent_loop_method.*` = project_1 层的旧建模 loop。

## 1. 这是什么

给定 A 阶段冻结的 `<NL, raw/source STM_0, fcstm STM_0>`，在 FCSTM 中间语义层上探索行为义务、发现 source-level 行为问题，并把问题、通过项、执行证据与覆盖审查写进不可变运行记录。**只读**，不改 `STM_0`，不做 Repair / Confirm。

一次 attempt 只有一个顶层 Discover Agent：

```text
冻结输入 -> Controller 机械分段 + coverage rows + SourceFact inventory
  -> 单次 Discover Agent run
       -> 双向探索（NL -> model 与 model -> NL/source）
       -> 注册 CoverageUnit / Root / 断言计划 -> 逐条 eval_assert
       -> 调 review_discovery_coverage（内含两个隔离 reviewer：语义覆盖 + 对抗性漏报）
       -> 按审查意见补查、修订、重跑、再审
  -> Controller 复验并发布 discover_completed -> 确定性生成 loops/discover.md
```

目录构成：

| 路径 | 内容 |
| :-- | :-- |
| [agent_loop/src/paper_stm_repair_loop/](./agent_loop/src/paper_stm_repair_loop/) | 实现主体。`controller.py` / `discover.py` / `records.py` / `renderer.py` / `inputs.py` / `nl_segmenter.py` / `source_inventory.py` / `assertion_policy.py` / `coverage_requirements.py` / `pyfcstm_adapter.py` |
| `src/.../tools/` | **20 个 Agent 工具**：`eval_assert` / `query_model` / `run_scenarios` / `verify_properties` / `check_fcstm` / `inspect_model` / `observe_trace` / `review_discovery_coverage` / `register_coverage_plan` / `revise_assertion` / `lookup_source_trace` 等 |
| `src/.../eval_env/` | **断言求值环境**：`runtime.py` / `simulation.py` / `structure.py` / `topology.py` / `relations.py` / `effects.py` / `fbmcq.py` / `source_mapping.py` / `provenance.py` / `views.py`。⭐ 这是被移植走的那部分，见 §2 |
| `src/.../schemas/` | 10 个 pydantic 契约：`assertions` / `coverage` / `coverage_review` / `discovery` / `inspect` / `records` / `roots` / `tool_reason` / `tools` |
| `src/.../prompts/` | Discover Agent 与两个 reviewer 的 system prompt |
| [agent_loop/tests/](./agent_loop/tests/) | 30 个测试文件、**266 个测试**；另有 `tests/helpers/` 两个 probe 脚本 |
| [agent_loop/fixtures/discover_capability/](./agent_loop/fixtures/discover_capability/) | ⭐ **D01–D12 缺陷能力 fixture** ＋ `_schema.json`，见 §3 |
| [agent_loop/fixtures/discover_integrated/](./agent_loop/fixtures/discover_integrated/) | 两个端到端样例：`0000_hldcs_manual_identity`（人工 FCSTM identity 工程样例）与 `0006_uav` |

## 2. 为什么停用

**因为编排范式换了，不是因为它做得差。** 当前实现在五个维度上做了不同选择：

| 维度 | 本目录（旧） | [../legacy/feedback_loop/](../legacy/feedback_loop/)（后续历史实现） |
| :-- | :-- | :-- |
| 编排 | 一个顶层 Agent + 工具集，**Agent 自行决定调用顺序** | **确定性 LangGraph StateGraph**，阶段固定 |
| 审查 | Agent 主动调 `review_discovery_coverage` | 每个生产阶段配一个审查者，**路由强制打回** |
| 断言来源 | Agent **自由撰写**表达式，注册门禁事后拒绝 | **先验闭合的 19 谓词词表** |
| 输入根 | [../../selected_seed_examples/](../../selected_seed_examples/)（`load_pair()`） | `pipeline/representation/reports/llms_emp_r45_java_60/` |
| 失败语义 | 门禁拒绝**可导致整次 attempt 终止** | **降级落盘**，带结构化诊断（仓库根 CLAUDE.md §10） |

后三条正是换掉它的实质理由：自由撰写的断言无法形成可复算的判据；整格终止会让缺陷最硬的样本从被测集里消失。

### 2.1 ⚠️ 从这里移植走、现在仍在生产中的东西

**这是本目录不能被当成废弃物的直接原因。** 当前实现的 `assertions/` 包整体移植自本目录的 `eval_env/`，源提交 **`c8c1ccba`**，移植后自包含、不 import `paper_stm_repair_loop`：

| 当前文件 | 移植自 | 移植时的改动 |
| :-- | :-- | :-- |
| `feedback_loop/.../assertions/__init__.py` | 本目录 `eval_env/` | 纯断言能力整体搬运 |
| `.../assertions/parser.py` | `eval_env/` 的断言脚本执行语义 | 改为要求「前缀 ＋ 末尾 assert」形状 |
| `.../assertions/environment.py` | `eval_env/` 的纯求值能力 | 重导出自包含 runtime，另加可暴露给 LLM 的 API 文档串 |
| `.../assertions/checker.py` | `eval_env/` 的求值思路 | 自包含重写 |
| `.../assertions/sealed.py` | `eval_env/` 的断言结果语义 | 适配前缀 ＋ 末尾 assert 脚本 |

此外 `feedback_loop/fixtures/manual_0000_identity/` 由本目录的 `fixtures/discover_integrated/0000_hldcs_manual_identity/` 复制而来（记录在那份 fixture 的 `provenance.json` 的 `copied_from` 字段）。

## 3. ⭐ 里面哪些内容仍然有价值、什么时候该取回来

| 内容 | 精确路径 | 什么时候取 |
| :-- | :-- | :-- |
| **D01–D12 缺陷能力 fixture** ＋ `_schema.json` | [agent_loop/fixtures/discover_capability/](./agent_loop/fixtures/discover_capability/) | 需要一组**按缺陷类型组织**的最小可复现样例时。12 类：错目标 / 缺事件处理 / 缺结构 / 缺 effect / 局部退出误作全局终止 / 目标冲突 / 初态或扇出错 / 越权额外行为 / 领域不匹配 / 深层 setup 无事件 / 提前完成 / 精确同一性归因。⚠️ 这套 taxonomy 与当前台账的 EIS 编号**不是同一套口径**，取用前先对齐 |
| **两个隔离 reviewer 的 prompt 设计** | `agent_loop/src/paper_stm_repair_loop/prompts/discover.py` | 设计新审查者时。语义覆盖 reviewer 与对抗性漏报 reviewer 无工具、无 gold、无模型修改权限，只审冻结输入与台账——这条隔离纪律仍然成立 |
| **20 个工具的边界划分** | `agent_loop/src/paper_stm_repair_loop/tools/` | 讨论「哪些能力该给 Agent、哪些该由确定性阶段做」时的对照物 |
| **Controller 的失败关闭式校验清单** | `agent_loop/src/paper_stm_repair_loop/controller.py`；叙述见 [agent_loop/README.md](./agent_loop/README.md) §2 | 它列了 Controller **不做**什么（不预设 taxonomy、不预测问题位置、不生成 gold、不把 conversion 差异自动判为 source issue、不用正集 inventory 冒充「缺失已发现」）——这五条是防自证的纪律，仍然有效 |
| **`eval_env/` 中未被移植的部分** | `agent_loop/src/paper_stm_repair_loop/eval_env/`：`fbmcq.py` / `topology.py` / `source_mapping.py` / `views.py` | 当前 `assertions/` 只搬了纯求值部分。有界模型检查（FBMCQ）、拓扑查询、source 映射、视图投影都还在这里 |
| 单 Agent 与固定图的架构对照 | [agent_loop/README.md](./agent_loop/README.md) §0 | 论文 §Method 需要论证「为什么不用自主 agent」时 |

⛔ **不得从本目录取任何实验数字**，也不得把这里的表述当成当前方法口径——[agent_loop/README.md](./agent_loop/README.md) 里「paper1 核心贡献是 feedback-driven loop」「Repair / Confirm 后续阶段」等说法均已被 2026-08 的收窄定调作废。

## 4. ⚠️ 必要时怎么复活

### 4.1 依赖

| 依赖 | 说明 |
| :-- | :-- |
| Python | 3.10（归档时实测环境 3.10.1） |
| `pyfcstm` | 仓库根 git submodule。`git submodule update --init --recursive` 后 `pip install -e ./pyfcstm` |
| `pydantic` / `typing_extensions` | 见仓库根 [../../../../requirements.txt](../../../../requirements.txt) |
| `langchain_core` / `langchain_anthropic` | 仅真实 provider 调用路径需要 |
| `utils.agent` / `utils.llm` | 仓库根的 `utils/` 包，需把**仓库根**放进 `PYTHONPATH`。⚠️ 跑测试时**不需要**：[agent_loop/tests/conftest.py](./agent_loop/tests/conftest.py) 在 `utils.agent` / `utils.llm` 不可 import 时自动装 stub |
| `pytest` | 测试 |

### 4.2 凭据配置（⛔ 这一条最容易踩）

**不要 `source .env`。仓库没有 `.env`，运行时也刻意拒绝从环境变量取凭据。**

配置真源是仓库根的 **`.llmconfig.yml`**（`600` 权限、不入库）。切换模型靠 `--profile <名字>`，不靠改环境变量。自检：

```bash
python -m utils.llm list        # 看有哪些 profile
python -m utils.llm validate    # 校验
```

⚠️ **永远不要 `cat .llmconfig.yml`**——里面是明文凭据。另注意：[agent_loop/README.md](./agent_loop/README.md) 是冻结原件，其中若出现 `source .env` 的说法，以本节为准（详见仓库根 CLAUDE.md §5.1，该误述已实际造成过一次事故）。

### 4.3 确切命令

`make` 目标定义在**仓库根 `Makefile`**（本目录没有自己的 `Makefile`），归档时已同步改到新路径，可直接用：

```bash
# 跑测试（266 个）
make legacy-discover-test

# 人工 identity 工程样例（真实 provider）
make legacy-discover-demo DISCOVER_PROFILE=<profile>

# 正式 pair
make legacy-discover-pair DISCOVER_PAIR=llms_emp_feedback_final_0000 DISCOVER_PROFILE=<profile>
```

⛔ **无前缀的 `make discover-*` 已转发给 [../legacy/feedback_loop/](../legacy/feedback_loop/)**，跑不到本目录。必须带 `legacy-` 前缀。

不用 `make` 时的等价调用（**在仓库根执行**——`tests/test_discover_cli.py` 里有仓库根相对路径常量，换目录会 `FileNotFoundError`）：

```bash
export LEGACY=project_1_llm_state_machine_modeling/paper_stm_issue_discover/archive/r9_agent_loop_pipeline/agent_loop
PYTHONPATH=$LEGACY/src:project_1_llm_state_machine_modeling:$PWD python -m pytest -q $LEGACY/tests
PYTHONPATH=$LEGACY/src:project_1_llm_state_machine_modeling:$PWD python -m paper_stm_repair_loop.discover --help
```

### 4.4 已知会失败的测试

归档时实测 **`1 failed, 265 passed`**，归档前在原路径实测同样是 `1 failed, 265 passed`——**同一个测试、同一个哈希差**，与归档无关。

| 测试 | 现象 | 原因 |
| :-- | :-- | :-- |
| `tests/test_discover_cli.py::test_manual_identity_source_meta_binds_current_formal_manifest_and_seal` | `conversion_manifest_sha256` 期望 `cbe9e89d…`，实得 `5658012f…` | fixture 里冻结的哈希绑定的是 `pipeline/representation/reports/llms_emp_r45_java_60/manifest.json`，该 manifest 在本树停止维护后被重新生成过。**这是归档前就存在的文档腐烂，不是搬迁引入的**；要复活须重新封一次 seal |

⚠️ **跑测试前先确认 `PYTHONPATH` 与 CWD**：不设 `PYTHONPATH` 会得到 **23 个 collection error**（`ModuleNotFoundError: paper_stm_repair_loop`），因为 [../../pipeline/conftest.py](../../pipeline/conftest.py) **刻意不把本树的 `src` 加进 `sys.path`**；不在仓库根跑会额外多 4 个失败。

## 5. 哪些东西还被现役代码引用着

### 5.1 运行时：零引用（已复验）

```bash
grep -rnE "^\s*(from|import)\s+paper_stm_repair_loop" --include=*.py \
  project_1_llm_state_machine_modeling/paper_stm_issue_discover/pipeline/feedback_loop \
  project_1_llm_state_machine_modeling/paper_stm_issue_discover/discover_matrix
# 无输出 = 零 import
```

现役代码里提到 `agent_loop` 的地方只有 docstring（说明「从 legacy agent_loop 移植而来」，见 §2.1），不构成依赖。

### 5.2 ⛔ 待修：归档产生了 4 条死链，落在本轮不可改的文件里

归档时 `pipeline/` 与 `pipeline/feedback_loop/` 正被另一个 agent 改动（包更名），故本轮**未触碰**这两个目录。它们里有 4 条指向本树旧路径的 Markdown 链接，搬迁后已成死链，**需要后续一并修**：

下表只给**链接目标**（`(...)` 里那一段），不写完整链接语法——写全会让死链扫描器把本文件也算成有死链。

| 文件 | 行 | 现在的链接目标 | 应改成的链接目标 |
| :-- | --: | :-- | :-- |
| `pipeline/README.md` | 16 | `./agent_loop/` | `../archive/r9_agent_loop_pipeline/` |
| `pipeline/README.md` | 20 | `./agent_loop/` | `../archive/r9_agent_loop_pipeline/` |
| `pipeline/feedback_loop/README.md` | 3 | `../agent_loop/` | `../../archive/r9_agent_loop_pipeline/` |
| `pipeline/feedback_loop/README.md` | 108 | `../agent_loop/README.md` | `../../archive/r9_agent_loop_pipeline/agent_loop/README.md` |

另有两处**非链接**的旧路径提法，同样待修：`pipeline/README.md:81`（规模统计里的 `agent_loop 266`）与 `pipeline/README.md:92`（包名对照表的 `agent_loop/` 行）——建议在行内注明「已归档至 `archive/r9_agent_loop_pipeline/`」。

### 5.3 ⚠️ 两处仍写着旧路径，归档时**有意未改**

| 位置 | 内容 | 为什么不改 |
| :-- | :-- | :-- |
| `pipeline/feedback_loop/tests/test_import_boundaries.py:58` | 把 `.../pipeline/agent_loop/src` 拼进 `PYTHONPATH`，用于「即使 legacy 包可 import，feedback_loop 也不会 import 它」的哨兵测试 | 该目录本轮不在改动范围内。⚠️ **这条现在指向不存在的路径**：Python 静默忽略 `PYTHONPATH` 里的无效项，所以测试**仍然通过，但已不再检验它声称的东西**（legacy 包根本没被放上路径）。这是**静默失效**，不是红灯——要恢复其效力，需把该路径改到 `archive/r9_agent_loop_pipeline/agent_loop/src` |
| `pipeline/feedback_loop/fixtures/manual_0000_identity/provenance.json:6` | `"copied_from": "pipeline/agent_loop/..."` | 这是**provenance 记录**，记的是复制发生**当时**的来源路径。改它等于篡改证据；正确读法是配合本文件 §0 的换算表 |

### 5.4 本树内部仍写着旧路径的冻结件（⛔ 一律不改）

| 文件 | 说明 |
| :-- | :-- |
| `agent_loop/fixtures/discover_integrated/0000_hldcs_manual_identity/fcstm_meta.json`（8 处）、`source_meta.json`（1 处） | 带 sha256 封印的 provenance 元数据，且写的是**更早**的 `paper_stm_repair/...` 路径。改动会破坏哈希 |
| [agent_loop/README.md](./agent_loop/README.md) 第 243 / 327 / 328 / 337 / 349 / 350 行 | shell 命令里的旧路径。归档纪律只允许重算**相对链接**，命令串不在其列——按 §6 的换算表自行替换 |
| `agent_loop/fixtures/discover_integrated/0000_hldcs_manual_identity/README.md` 第 63 / 64 行 | 同上，`DISCOVER_NL=` / `DISCOVER_FCSTM=` 的旧路径 |
| [agent_loop/README.md](./agent_loop/README.md) 第 26 行的 `` `../representation/reports/llms_emp_r45_java_60/` `` | 行内代码而非链接，未改；正确路径见 §6 |

## 6. 旧路径 → 新路径换算表

统一规则：**`pipeline/agent_loop/` → `archive/r9_agent_loop_pipeline/agent_loop/`**，即在 `paper_stm_issue_discover/` 之下**多了一层**。

| 旧 | 新 |
| :-- | :-- |
| `paper_stm_issue_discover/pipeline/agent_loop/` | `paper_stm_issue_discover/archive/r9_agent_loop_pipeline/agent_loop/` |
| `.../pipeline/agent_loop/src` | `.../archive/r9_agent_loop_pipeline/agent_loop/src` |
| `.../pipeline/agent_loop/tests` | `.../archive/r9_agent_loop_pipeline/agent_loop/tests` |
| `.../pipeline/agent_loop/fixtures/...` | `.../archive/r9_agent_loop_pipeline/agent_loop/fixtures/...` |
| 从本树看 `../feedback_loop/` | `../../../pipeline/feedback_loop/` |
| 从本树看 `../README.md`（pipeline 入口） | `../../../pipeline/README.md` |
| 从本树看 `../../selected_seed_examples/` | `../../../selected_seed_examples/` |
| 从本树看 `../../README.md`（工作区入口） | `../../../README.md` |
| 从本树看 `../representation/reports/llms_emp_r45_java_60/` | `../../../pipeline/representation/reports/llms_emp_r45_java_60/` |

### 6.1 归档时实际做了哪些内容改动

**219 个文件全部是 rename，blob 逐一比对完全一致。** 在此之上只做了归档纪律（[../README.md](../README.md) §3.6）允许的机械变换，逐条如下：

**A. 深度锚点重算（4 处，不改会静默解析到错目录）**

| 文件 | 改动 | 不改的后果 |
| :-- | :-- | :-- |
| `agent_loop/src/paper_stm_repair_loop/config.py:7` | `PAPER_ROOT = AGENT_LOOP_ROOT.parent.parent` → `.parent.parent.parent` | `PAPER_ROOT` 会解析到 `archive/`，`PAIRS_JSONL` 与 `SELECTED_ROOT` 指向不存在的路径**而不报错** |
| `agent_loop/tests/test_discover_cli.py:22` | `MANUAL_IDENTITY_DIR` 的仓库根相对串换成新路径 | 5 个测试 `FileNotFoundError` |
| `agent_loop/tests/helpers/probe_discover_evidence_choice.py:14` | `parents[6]` → `parents[7]` | `REPO_ROOT` 少一层，`sys.path` 注入错目录 |
| 仓库根 `Makefile` | 抽出 `LEGACY_AGENT_LOOP` 变量，`DISCOVER_SRC` / `LEGACY_DISCOVER_DEMO_ROOT` / `legacy-discover-test` 三处改用它 | 三个 `legacy-discover-*` 目标全部失效 |

实测：只搬不改时为 `9 failed, 257 passed`；补完前三处后回到 `1 failed, 265 passed`，与归档前一致。

**B. 相对链接深度重算（8 条，全在 [agent_loop/README.md](./agent_loop/README.md)）**

`../feedback_loop/` ×4、`../README.md` ×1、`../../selected_seed_examples/` ×2 —— 这 7 条搬迁后**指向不存在的路径**；`../../README.md` ×1 —— 这条搬迁后**仍能打开，但指向了错的文件**（`archive/README.md` 而非工作区 `README.md`）。⚠️ 后者是死链扫描器**看不见**的一类伤：链接有效，目标错了。

**C. 没有做的**

结论、数字、措辞、设计记录、更新日志、fixture 内容、provenance 元数据一律原样保留。§5.3 与 §5.4 列出的旧路径**有意未改**。

## 7. 一致性核验（归档时实测）

| 项 | 归档前 | 归档后 |
| :-- | :-- | :-- |
| 文件数（含被忽略产物） | 224 | 224 |
| 被跟踪文件数 | 219 | 219 |
| blob × 相对路径映射 | — | 219/219 完全一致（纯 rename） |
| `pytest`（仓库根 ＋ `PYTHONPATH`） | `1 failed, 265 passed` | `1 failed, 265 passed` |
| 仓库被跟踪文件总数 | 12850 | 12850 |
| 本树 Markdown 死链 | 0 | 0 |
| 被 `.gitignore` 忽略的文件 | 5（`.pytest_cache/`） | 5（同一条通用规则，路径无关） |
