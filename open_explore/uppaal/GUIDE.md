# `uppaal/` 操作规范

本文档用于固定 [SUMMARY.md](./SUMMARY.md) 与 `open_explore/uppaal/` 的后续维护方式，作为后续 AI 在该专题下持续扩张 `UPPAAL` 文库时的统一操作规范。

## 0. 文档关系与使用顺序

`uppaal/` 下的几个核心文档分工如下：

1. [README.md](./README.md)
   - 负责解释论文集定位、纳入/排除标准、官方入口、作者主线与材料状态口径。
2. [GUIDE.md](./GUIDE.md)
   - 负责规定检索、筛选、目录维护、[SUMMARY.md](./SUMMARY.md) 回填和一致性检查的操作规范。
3. [SUMMARY.md](./SUMMARY.md)
   - 是当前论文集的总账，记录实时统计、分类分布、双维材料状态、论文清单、失败历史和本轮更新。

默认推荐顺序如下：

1. 先读 [README.md](./README.md)，确认本论文集为什么存在、收什么、不收什么。
2. 再读 [GUIDE.md](./GUIDE.md)，确认本轮工作流程、字段口径和回填要求。
3. 再读 [SUMMARY.md](./SUMMARY.md)，确认当前已收录范围、作者主线、状态分布和失败历史。
4. 如果目标条目是 thesis/合集型父路径，先读该目录自己的 `README.md`，再决定是否进入其 `paper-*` 子目录。
5. 最后进入具体论文目录，按 `bibtex.bib -> paper_content.txt -> paper.pdf（必要时）` 的顺序工作。

## 1. 目标与范围

`uppaal/` 不是一般性的 timed automata 收藏夹，而是面向 `UPPAAL` 谱系的专题文库。收集它们的直接目的如下：

1. 沉淀 `UPPAAL` 核心理论、关键算法、数据结构和工程能力的主线资料。
2. 为后续验证方法研究、工具理解、验证案例设计和相关工作写作提供稳定依据。
3. 持续积累可复用的 `UPPAAL` 应用案例，而不是只停留在工具本体介绍。

### 1.1 贡献类型 Emoji 口径

后续在 [SUMMARY.md](./SUMMARY.md) 中统一使用以下四类贡献口径：

| Emoji | 类型 | 含义 |
|---|---|---|
| 🧱 | 核心算法/数据结构 | timed automata 语义、DBM、zone、symbolic state、核心验证算法等基础工作 |
| ⚡ | 改进与扩展 | 对抽象、状态空间、优先级、priced/strategy/statistical 等能力的增强与优化 |
| 🛠️ | 工程/工具链 | 工具架构、建模语言、查询语言、教程、建模模式、用户侧工程实践 |
| 🧪 | 应用与案例 | 基于 `UPPAAL` 的具体系统、协议、软件或工业案例建模与验证工作 |

原则上每篇论文只给一个一级主分类；若同时覆盖多个方面，在 `备注` 中补充次级定位，不要在主分类里重复贴多个 emoji。

### 1.2 双维材料状态口径

`SUMMARY.md` 中的状态默认按以下两个维度维护：

1. **内容详细程度**
2. **实现可获取程度**

默认定义与 [README.md](./README.md) 保持一致，不再使用“基础材料齐全/尚未齐全”作为主状态口径。

其中“实现可获取程度”默认严格按**源码级实现**理解：

1. 官方二进制、安装包、在线服务、教程页和案例页都不能直接上调到“源码可得”。
2. 若只有可执行版本，没有源码，则最高只能评到 `🟧 仅可执行/可使用版本可得`。
3. 只有当官方或作者公开了源码仓库、源码包、核心库代码或直接对应的实现工程时，才允许评到 `🟨` 及以上。

### 1.3 非目标边界

以下工作即使和 `UPPAAL` 有远距离关系，也不属于本论文集的主任务，应避免混入：

1. 泛 timed automata / 泛 model checking 背景文献，但正文没有稳定 `UPPAAL` 关联。
2. 只是一句提到 `UPPAAL`、并未形成真实技术或应用贡献的论文。
3. 工具安装笔记、博客转载、课程作业、无稳定可追溯元信息的二手材料。
4. 没有合法 PDF、没有可靠提取文本且短期内无法补齐的条目。

## 2. 检索策略

### 2.1 技术关键词簇

后续扩张时，推荐按四条主线分别维护技术词簇，而不是只沿某一类不断膨胀：

1. `🧱` 核心算法/数据结构
   - `UPPAAL + timed automata + DBM/zone/federation/difference bound matrix/symbolic state`
2. `⚡` 改进与扩展
   - `UPPAAL + abstraction/extrapolation/priced/statistical/strategy/game/priority/reduction`
3. `🛠️` 工程/工具链
   - `UPPAAL + tutorial/user guide/modeling patterns/query language/verifyta/toolbox`
4. `🧪` 应用与案例
   - `UPPAAL + case study/industrial/application + 具体系统名`

### 2.2 作者关键词簇

人物检索簇的生成顺序必须固定如下：

1. 先以当前已收录顶层条目的 `bibtex.bib` 为主数据源统计作者。
2. 再根据频次、共现关系和覆盖的技术分支形成“核心作者主线”。
3. 再用官方 team / org / docs 只做补证，核验其是否仍有对应工具线、源码或案例入口。
4. 不允许反过来先抓 homepage team，再把人名硬塞进检索关键词簇。

当前文库中，后续应优先沿下表继续扩张：

| 作者 | 当前关联条目 | 角色判断 | 主要贡献方向 | 推荐联用分支词 |
|---|---|---|---|---|
| `Kim Guldstrand Larsen` | `lpw95`、`llpy97`、`bdl04`、`behrmann07`、`david11-*`、`david15` | `UPPAAL` 总主线牵引者 | `symbolic verification / DBM / tutorial / Tiga / SMC / Stratego` | `zones/priced/strategy/statistical` |
| `Alexandre David` | `bdl04`、`behrmann02`、`behrmann07`、`david11-*`、`david14`、`david15` | 中后期扩展主线整合者 | `architecture / Tiga / SMC / expected cost / Stratego` | `priced/strategy/game/statistical` |
| `Gerd Behrmann` | `behrmann02`、`behrmann03`、`behrmann06`、`behrmann07`、`behrmann11` | 工程架构与工具演进主线作者 | `architecture / implementation / CDD-abstraction / UPPAAL 4.0 / evolution survey` | `CDD/abstraction/tool architecture` |
| `Wang Yi` | `lpw95`、`llpy97`、`by04`、`behrmann02`、`behrmann06` | 早期语义与算法骨架作者 | `timed automata semantics / symbolic algorithms / engine foundations` | `semantics/algorithms/symbolic state` |
| `Paul Pettersson` | `lpw95`、`llpy97`、`behrmann02-secrets`、`dhlp06`、`behrmann11` | `DBM / engine / priority` 工程连接者 | `compact DBM / state-space reduction / implementation / priorities` | `priority/federation/reduction` |
| `Johan Bengtsson` | `bengtsson02`、`behrmann02-secrets`、`by04` | `DBM` 数据结构专题化奠基作者 | `clocks / DBMs / states / DBM internals / implementation detail` | `DBM/federation/implementation` |
| `Axel Legay` | `david11-statistical`、`david11-smc`、`bulychev12`、`david14` | `SMC / optimization` 分支关键协作者 | `statistical model checking / priced models / expected-cost optimization` | `statistical/expected cost/optimization` |
| `Didier Lime` | `cassez05`、`behrmann07`、`david14` | `timed games -> Tiga -> optimization` 分支协作者 | `timed games / controller synthesis / cost analysis` | `timed games/Tiga/cost` |
| `Patricia Bouyer` / `Radek Pelánek` | `bblp04` | zone abstraction 外推分支关键合作者 | `lower-upper bound extrapolation / zone abstraction` | `abstraction/extrapolation` |
| `Rajeev Alur` / `David Dill` / `David L. Dill` | `ad90`、`dill89` | `UPPAAL` 理论前史奠基者 | `timed automata semantics / dense-time verification / clock constraints` | `timed automata/history` |

执行时还应遵守以下约束：

1. 检索默认动作是“作者名 + UPPAAL + 技术分支词”联用；不要只搜作者名，否则噪声过大。
2. 对含重音或 BibTeX 转义的人名，检索时应同时尝试规范写法与 ASCII 变体，例如 `John Håkansson / John Haakansson`、`Radek Pelánek / Radek Pelanek`。
3. 若某作者当前只在一篇边缘背景论文中出现，默认不提升为核心主线，除非后续又在新增条目中反复出现。
4. 作者表不能只记“出现过没有”，还应同时维护：
   - 角色判断
   - 主要贡献方向
   - 当前文库覆盖年份
   - 当前核验到的较新 `UPPAAL` 相关年份
   - 最近性判断
   - 继续沿该作者线扩张的检索价值推断
5. 作者角色判断必须先根据当前已收录论文里的共著关系、跨分支覆盖和关键转折条目来写，再参考官方入口做补证；不允许只按 team 页面职位或主页简介臆测。
6. 如果当前文库明显偏早期，而官方工具线或 DBLP 已显示 `2010s/2020s` 仍有后续工作，必须把“年代缺口”明确写回 [SUMMARY.md](./SUMMARY.md)，不能默认文库已经代表完整演进脉络。

### 2.3 官方入口与实现可得性核验

在判断“实现可获取程度”时，默认按下面顺序核验：

1. 先看 [README.md](./README.md) 中的“官方入口索引”。
2. 优先检查官方 GitHub org：<https://github.com/UPPAALModelChecker>
3. 再检查官方 docs、downloads、case studies 和 Meta 仓库。
4. 若论文正文给出模型、源码、脚本或附录链接，再记录为额外线索。
5. 若只能拿到官方二进制、安装包或在线可用工具，而拿不到源码，则最多评为 `🟧 仅可执行/可使用版本可得`。
6. 若只有论文提到工具存在、但找不到对应源码入口，则降为 `🟧` 或 `🟥`，不要把 `downloads` 页面误写成“实现源码可得”。

额外约束如下：

1. `SUMMARY.md` 中关键词簇相关章节必须采用“压缩式整合更新”，禁止写成逐轮机械追加的检索流水账。
2. 每次扩张都要关注四类贡献的平衡，不能一直只补 `🧱` 而让 `🧪` 长期为空。
3. 如果某条检索线连续多轮低命中，应回写到 [SUMMARY.md](./SUMMARY.md) 并降权，而不是继续堆积搜索词。

## 3. 筛选、去重与失败规则

### 3.1 收录条件

默认至少满足以下一项：

1. 直接定义、解释或总结 `UPPAAL` 本体及其核心引擎能力。
2. 直接研究 `UPPAAL` 相关算法、数据结构、抽象或扩展能力。
3. 直接提供 `UPPAAL` 建模、查询、工具链或工程实践上的系统性贡献。
4. 直接使用 `UPPAAL` 在具体系统上形成有价值的应用案例。

### 3.2 降优先级条件

1. 和 `UPPAAL` 有引用关系，但正文贡献更偏外围背景。
2. 属于历史前驱理论，只能作为 `UPPAAL` 技术脉络的前置说明。
3. 应用中使用了 `UPPAAL`，但案例本身很薄，难以形成稳定经验。

### 3.3 排除条件

1. 与 `UPPAAL` 没有稳定直接关系。
2. 无法取得合法可用 PDF。
3. 即使取得 PDF，也无法生成可用 `paper_content.txt`。
4. 与已收录论文重复，且没有新增价值。

### 3.4 去重规则

1. 先按 DOI 去重。
2. DOI 缺失时按标准化标题去重。
3. 标题存在轻微差异时，再结合作者、年份、会议/期刊综合判断。

### 3.5 失败重试规则

1. 同一候选若在最近 `5` 天内已明确记录为下载失败或提取失败，默认跳过。
2. 超过 `5` 天后可以重新尝试；若再次失败，则继续追加新的失败记录。

## 4. 目录与文件规范

`uppaal/` 下每篇论文必须独占一个子目录。目录名应尽量兼顾稳定与可读性；当前基础批次采用“来源 key + 精简标题 slug”的组合。

每个论文目录至少应包含以下文件：

1. `paper.pdf`
2. `paper_content.txt`
3. `bibtex.bib`

执行时还应遵守以下约束：

1. 若源材料已有高质量 `content.md`，允许直接复制并重命名为 `paper_content.txt`。
2. 若缺少现成正文提取物，必须优先使用 `tools/pdf_extractor.py` 生成。
3. 如果某个条目来自 thesis、合集或其他带稳定子论文拆分的父路径，应把 `paper-*` 子目录一并带入，并复制其 `paper.pdf`、`content.md` 以及 `content_assets/` 等必要材料。
4. 这类父路径必须补 `README.md`，说明根目录材料与 `paper-*` 子目录的关系、推荐阅读顺序，以及哪些子目录最值得优先进入。
5. 这些 `paper-*` 子目录当前默认视为父条目的辅助阅读单元，不单独计入 [SUMMARY.md](./SUMMARY.md) 顶层论文数；若未来要升级为独立正式条目，再单独补 `bibtex.bib` 并在总账中单列。
6. 不要把外部本地绝对路径写进仓库文档；如果需要说明来源，只描述为“既有外部文库/历史材料池”等抽象来源。
7. 当前论文集基础阶段不强制每篇都写 `desc.md`，但后续一旦开始单篇分析，应保持字段结构一致。

## 5. 内容整理策略

当前 `uppaal/` 以“基础文库入库”为主，因此单篇目录默认先保证三件事：

1. PDF 原文在库。
2. BibTeX 元信息可用。
3. `paper_content.txt` 可检索可追溯。

对于带 `paper-*` 子目录的 thesis/合集型条目，还应额外保证：

1. 父目录 `README.md` 已经提供子论文导航。
2. 子目录至少具备 `paper.pdf`、`paper_content.txt` 和必要的 `content_assets/`。
3. 后续阅读与整理顺序默认是“先父目录，再子目录”，而不是跳过父条目直接散读子论文。

当后续开始做单篇深度整理时，建议优先提取以下内容：

1. 论文在 `UPPAAL` 谱系中的定位。
2. 它解决的核心技术问题或应用问题。
3. 与本博士研究的可复用关系。
4. 它在双维材料状态上的当前判断和依据。
5. 是否值得单独补 `desc.md`、对比表或专题笔记。

默认规则如下：

1. 单篇细节尽量写入未来的单篇派生文件，不要把所有观察都堆进 [SUMMARY.md](./SUMMARY.md)。
2. [SUMMARY.md](./SUMMARY.md) 只保留分类、双维状态、检索导向和一句话级摘要。

## 6. [SUMMARY.md](./SUMMARY.md) 撰写规范

[SUMMARY.md](./SUMMARY.md) 必须持续维护以下章节：

1. 文档定位与使用方式。
2. 收录边界回顾。
3. 官方入口速查。
4. 贡献类型 Emoji 口径。
5. 双维材料状态口径。
6. 检索关键词簇。
7. 年代分布与近年活动观察。
8. 作者关联与作者时间线。
9. 当前收录统计。
10. 分类分布。
11. 论文清单。
12. 更新日志。
13. 失败与阻塞记录。

维护约束如下：

1. 关键词簇相关小节默认每节最多 `10` 行，必须整合更新而不是持续累加。
2. 统计数字必须与论文表、失败表真实内容一致。
3. `🧱 / ⚡ / 🛠️` 三类条目默认合并维护在同一张统一表格中；不要再拆成三张分表。
4. 论文清单必须按年份升序维护；当前 `🧱 / ⚡ / 🛠️` 统一表要求全局按年份升序，同年按 `Key` 字典序稳定排序；若未来 `🧪` 单列，也同样按年份升序。
5. `🧪 应用与案例` 单独维护；即使当前数量为 `0`，也要保留其统计位置。
6. thesis/合集条目若带 `paper-*` 子目录，默认只以父条目在总账中记一条，并在备注中说明含有哪些子目录。
7. 双维状态必须显式写出，而不是继续使用“基础材料齐全/不齐全”作为主状态列。
8. 作者表默认要体现“角色判断 + 主要贡献方向 + 当前文库年份范围 + 当前核验到的较新年份 + 最近性判断 + 继续扩张价值推断”。
9. 论文表中的源码状态列必须按源码标准填写，不得把“可下载运行”写成“源码可得”。

## 7. 工作流程

一轮完整工作推荐按以下顺序进行：

1. 先读 [README.md](./README.md)、[GUIDE.md](./GUIDE.md)、[SUMMARY.md](./SUMMARY.md)。
2. 先补历史欠账，如缺失的 `paper_content.txt`、缺失的 `bibtex.bib`、遗漏的统计。
3. 先检查官方入口与作者线索，再做新检索或新收录。
4. 如果条目自带 `paper-*` 子论文结构，先补齐父目录 README 和子目录材料，再决定是否需要逐个补子目录 README。
5. 完成单论文目录必要文件后，再统一回填 [SUMMARY.md](./SUMMARY.md)。
6. 回填时同时给出“内容详细程度”和“实现可获取程度”的判定。
7. 回填后复核统计、一致性、分类、链接和年份顺序。

如果某轮因领域过窄或开放获取受限而无法达到大批量新增，应在更新日志中如实说明。

## 8. 质量与可追溯性要求

1. 所有收录、分类、备注和统计都应有原文依据。
2. 如果某篇论文只是“前置理论”而非直接 `UPPAAL` 工作，必须在备注中如实标明。
3. 如果证据不足，必须在 [SUMMARY.md](./SUMMARY.md) 中记为待补证或失败，而不是臆测补齐。
4. 对“实现可获取程度”的判断必须写明是来自论文、官方 GitHub org、官网下载区、案例页还是其他官方入口。
5. 对“作者仍有后续工作”的判断，必须区分“作者个人近年仍有直接论文”与“官方工具线近年仍在演化”这两件事；二者不能混写。
6. 不得在仓库文档中写入外部本地绝对路径或机器专属路径。

## 9. 与专项 GUIDE 的关系

当前 `uppaal/` 尚未设置专项 `XXXX_GUIDE.md`。如果后续开始批量生产 `desc.md`、应用案例笔记或能力分支专题，应新增相应专项 GUIDE；发生冲突时，以专项 GUIDE 对应任务的细则为准。
