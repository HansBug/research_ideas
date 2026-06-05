# `ccf_venues/` SUMMARY

> 信息更新时间：`2026-06-05 12:35`（Asia/Shanghai）

## 1. 当前整体状态

| 项目 | 数量 / 状态 |
|---|---:|
| 文库状态 | PR-4 剩余 P0 期刊已完成基础建档并与会议试点、期刊试点、PR-2 会议合流；会议 dated events、期刊 special issue dated events 与 rolling 投稿入口已在 [TIMELINE.md](./TIMELINE.md) 共存 |
| 已建立核心文档 | 5 |
| 已建立模板文件 | 4 |
| 已建立并基础核验 venue 目录 | 14 |
| 已建立并基础核验年度 README | 98 |
| 已完成会议试点 venue | 3：[`conf-a-icse`](./conf-a-icse/README.md)、[`conf-b-models`](./conf-b-models/README.md)、[`conf-b-etaps`](./conf-b-etaps/README.md) |
| 已完成期刊试点 venue | 3：[`journal-a-tse`](./journal-a-tse/README.md)、[`journal-a-tosem`](./journal-a-tosem/README.md)、[`journal-b-sosym`](./journal-b-sosym/README.md) |
| 已完成 PR-2 会议 venue | 5：[`conf-a-fse`](./conf-a-fse/README.md)、[`conf-a-ase`](./conf-a-ase/README.md)、[`conf-a-issta`](./conf-a-issta/README.md)、[`conf-b-re`](./conf-b-re/README.md)、[`conf-c-refsq`](./conf-c-refsq/README.md) |
| 已完成 PR-4 期刊 venue | 3：[`journal-b-re`](./journal-b-re/README.md)、[`journal-b-stvr`](./journal-b-stvr/README.md)、[`journal-c-sttt`](./journal-c-sttt/README.md) |
| 事实完全核验 venue 目录 | 0 |
| 默认调查范围 | 2022 至当前年份 + 2 为默认检索与占位下限；已公布 CFP / important dates 的更远未来年度也必须纳入 |
| TIMELINE 状态 | 已按事件发生年份回填 2022-2028 会议时间线、SoSyM Industry 5.0 dated event、Requirements Engineering 2026 collections dated events、期刊 rolling 表与 PR-2/PR-4 facts，见 [TIMELINE.md](./TIMELINE.md) |
| 核心人员情报状态 | 8 个会议根 README 已补会议核心人员情报；6 个期刊根 README 已补核心编辑人员画像或官方 roster 待核验入口，并保留 `核验等级 / 当前性` |
| 当前优先批次 | PR-3 后续 P0-B 形式化验证会议与 PR-5 全局收口，需沿用本轮合流后的 URL、人员、计数和 TIMELINE 规则 |

说明：当前统计表示 6 个试点 venue、5 个 PR-2 venue 与 3 个 PR-4 期刊已完成基础情报建档和部分核验，但仍不是“事实完全闭环”样板。会议侧仍存在 proceedings / DBLP 延迟公开、future CFP 未公布、多 track 计数、PACMSE / co-location、IEEE / Springer proceedings 入口待复核等问题；期刊侧仍存在 publisher issue / online-first 口径、动态投稿入口和 editorial roster 当前性待复核。

## 2. 当前可复用的既有资源

| 来源 | 当前用途 | 是否直接搬入 |
|---|---|---|
| [../VENUES.md](../VENUES.md) | 初始 venue 名录、CCF 等级、project 相关性 | 否，作为种子核验 |
| `PR #5 frontier_index/CCF_SE_A_B_C.md` | 软工相关 venue 边界与方向先验 | 否，作为参考 |
| `PR #5 frontier_index/CCF_SE_2026_DEADLINES.md` | deadline 调研字段与官方来源思路 | 否，需重新核验 |
| `PR #5 frontier_index/ccf_history/SUBMISSION_TIMELINES.md` | 近年时间线组织方式参考 | 否，需重新核验 |
| `PR #5 frontier_index/ccf_history/*/metadata/*.json` | 论文数量与 DBLP 计数的候选线索 | 否，只能作交叉核验 |

## 3. 会议试点完成情况

| Venue | CCF | 年度范围 | 根 README | 年度 README | TIMELINE | 核心人员情报 | 计数 / 状态口径 | 核验状态 |
|---|---|---|---|---:|---|---|---|---|
| ICSE | A | 2022-2028 | [conf-a-icse](./conf-a-icse/README.md) | 7 | 已同步 | 覆盖 2026/2027 GC/PC 与 Steering 代表人物；见根 README §5 | Research / Technical Track accepted papers；2026 Research Track count 待 DBLP/proceedings 复核 | 🟡 部分核验 |
| MoDELS | B | 2022-2028 | [conf-b-models](./conf-b-models/README.md) | 7 | 已同步 | 覆盖 2025/2026 GC/PC 与 Steering 代表人物，并补 DBLP / 代表作链接；见根 README §5 | DBLP `inproceedings` / 官方 accepted papers fallback，根表单元格显式写口径 | 🟡 部分核验 |
| ETAPS / TACAS | B | 2022-2028 | [conf-b-etaps](./conf-b-etaps/README.md) | 7 | 已同步 | 覆盖 TACAS 2026/2027 PC Chair、Area Chair 与 Steering 代表人物；见根 README §5 | ETAPS umbrella / TACAS 双口径分开 | 🟡 部分核验 |

## 4. PR-2 软工 / 需求会议完成情况

| Venue | CCF | 年度范围 | 根 README | 年度 README | TIMELINE | 核心人员情报 | 计数 / 状态口径 | 核验状态 |
|---|---|---|---|---:|---|---|---|---|
| FSE | A | 2022-2028 | [conf-a-fse](./conf-a-fse/README.md) | 7 | 已同步 | 覆盖 2026 GC/PC、2024 PC 与 steering / PACMSE 治理线索；见根 README §5 | FSE / ESEC-FSE slug 冻结；2024+ PACMSE issue 不重复计数；2022-2025 多数仍需 DBLP / ACM 复核 | 🟡 部分核验 |
| ASE | A | 2022-2028 | [conf-a-ase](./conf-a-ase/README.md) | 7 | 已同步 | 覆盖 2026/2025/2024/2023/2022 chair 与 AI+SE / repair / modeling 领域权威；见根 README §5 | 多 track 明确分离；已结束年度暂用 DBLP 全 proceedings fallback，不能写成 Research Track count | 🟡 部分核验 |
| ISSTA | A | 2022-2028 | [conf-a-issta](./conf-a-issta/README.md) | 7 | 已同步 | 覆盖 2026 research chair、AI/testing/analysis area chair 与测试分析领域权威；见根 README §5 | ISSTA 2024+ co-location 仅作会期关系；论文数量按 ISSTA 独立入口 / DBLP fallback | 🟡 部分核验 |
| RE | B | 2022-2028 | [conf-b-re](./conf-b-re/README.md) | 7 | 已同步 | 覆盖 2026 GC/PC 与需求工程、goal modeling、privacy / CPS RE 领域权威；见根 README §5 | Research / Industry / RE@Next / artifact / tools 分离；IEEE proceedings conference number 待补 | 🟡 部分核验 |
| REFSQ | C | 2022-2028 | [conf-c-refsq](./conf-c-refsq/README.md) | 7 | 已同步 | 覆盖 2027/2026 PC chair、General Chair 与需求质量 / ontology / NLP for RE 线索；见根 README §5 | Springer / CEUR / DBLP 入口分散，official program 与 proceedings 卷号待后续复核；按 PR-2 收录但 scope 批次归属留 PR-5 | 🟡 部分核验 |

## 5. 期刊试点完成情况

| Venue | CCF | 年度范围 | 根 README | 年度 README | TIMELINE | 核心编辑人员情报 | 计数 / 状态口径 | 核验状态 |
|---|---|---|---|---:|---|---|---|---|
| TSE | A | 2022-2028 | [journal-a-tse](./journal-a-tse/README.md) | 7 | rolling 表已同步 | 已记录 EiC 与候选 AEiC / editorial leadership 线索，保留 `核验等级 / 当前性` | DBLP `entry article` baseline：2022=284、2023=278、2024=182、2025=228、2026=98 | 🟡 部分核验 |
| TOSEM | A | 2022-2028 | [journal-a-tosem](./journal-a-tosem/README.md) | 7 | rolling 表已同步 | 已记录 EiC 与候选编辑线索，ACM DL editorial-board 动态访问受限，保留替代核验路径 | DBLP `entry article` baseline：2022=86、2023=161、2024=223、2025=242、2026=115 | 🟡 部分核验 |
| SoSyM | B | 2022-2028 | [journal-b-sosym](./journal-b-sosym/README.md) | 7 | rolling 表与 Industry 5.0 dated event 已同步 | 已记录 Editors-in-Chief / Associate Editor-in-Chief / Assistant Editors；Advisory Board 暂不展开 | DBLP `entry article` baseline：2022=108、2023=98、2024=75、2025=91、2026=30 | 🟡 部分核验 |

### 5.1 PR-4 剩余 P0 期刊完成情况

| Venue | CCF | 年度范围 | 根 README | 年度 README | TIMELINE | 核心编辑人员情报 | 计数 / 状态口径 | 核验状态 |
|---|---|---|---|---:|---|---|---|---|
| Requirements Engineering | B | 2022-2028 | [journal-b-re](./journal-b-re/README.md) | 7 | rolling 表与 2026 LLM / 30th Anniversary / REFSQ collections dated events 已同步 | 已记录 Editor-in-Chief、Honorary Editor 与 RE / traceability / NLP for RE 代表性 editorial board 成员；见根 README §3 | DBLP `entry article` baseline：2022=25、2023=26、2024=24、2025=9、2026=6；2026 仍进行中 | 🟡 部分核验 |
| STVR | B | 2022-2028 | [journal-b-stvr](./journal-b-stvr/README.md) | 7 | rolling 表已同步；未发现 active dated CFP | Wiley editorial board 官方入口受 WAF/403，已保留官方 roster 链接与待人工浏览器核验说明；可核验人物画像仍需后续补强 | DBLP `entry article` baseline：2022=31、2023=25、2024=26、2025=17；2026 DBLP 年度页未公布 | 🟡 部分核验 |
| STTT | C | 2022-2028 | [journal-c-sttt](./journal-c-sttt/README.md) | 7 | rolling 表已同步；未发现 active dated CFP | 已记录 Editor-in-Chief / Coordinating Editor、CoCha / Explain / FoMaC 主题编辑与形式化验证领域权威；见根 README §3 | DBLP `entry article` baseline：2022=51、2023=49、2024=48、2025=41、2026=14；conference-based special issue 不与会议 proceedings 混算 | 🟡 部分核验 |

## 6. 会议试点踩坑结论

1. **年度主页与正式 CFP 不能混用**：ICSE 2028 仅有 Hawaii 预告且 `home/icse-2028` 当前 Access denied；ETAPS 2028 只有主页和会期；MoDELS 2027/2028 未发布。未来年度必须写清“已有主页 / 已检索未公布 / 仅预告”。
2. **edition 年份与事件发生年份不同**：ICSE 2027、ETAPS/TACAS 2027 的主要 submission 发生在 2026 年。因此 [TIMELINE.md](./TIMELINE.md) 按事件发生年份组织，Venue 列保留会议 edition。
3. **论文数量必须绑定计数口径**：ICSE 用 Research / Technical Track accepted papers；MoDELS 多数年份用 DBLP `inproceedings` fallback；ETAPS 必须拆 `ETAPS umbrella official count` 与 `TACAS official count`。
4. **出版入口可能分散或受限**：ICSE 2025 有 proceedings 页但 2026 DBLP/proceedings 未公开；MoDELS 2024 proceedings 当前 accessDenied，2022 ACM DL 可能 403；ETAPS 部分年份只有 proceedings 总说明页或旧站 HTML。
5. **venue URL 结构会随年份变化**：MoDELS 2025 使用独立域名 `2025.models-conf.com`，2024 及以前多在 `conf.researchr.org`；ETAPS 2022 是旧站 `.html`，2023 以后多为 `/year/cfp/` 与 `/year/conferences/tacas/`。
6. **submission system 也需可点击**：ICSE 年度 HotCRP、MoDELS 年度 EasyChair、TACAS 年度 EasyChair 均应进入根 README 和年度 README；历史年度可能重定向登录或归档，备注中说明即可。
7. **Mermaid 只放日期级可视化**：`AoE`、`UTC-12h`、官方仅日期、页面版本差异等细节留在表格备注，避免 Mermaid 图过长或不可读。
8. **核心人员情报需要强制可追溯**：venue 根 README 应记录组织者、PC / Research Track chair、Steering Committee 和强相关领域权威；每行至少保留官方角色来源，并尽量补 DBLP、个人主页、代表作或近年论文链接。

### 6.1 PR-2 软工 / 需求会议踩坑

1. **FSE / ESEC-FSE / PACMSE 必须冻结命名和计数**：根目录固定 `conf-a-fse`，历史年度保留 ESEC/FSE 注记；2024+ PACMSE issue 是主论文出版口径，不额外重复计数。
2. **ISSTA co-location 不能改变计数边界**：ISSTA 与 FSE / SPLASH / ECOOP 的 co-location 只记录会期和入口关系，论文数量按 ISSTA 独立 program / proceedings / DBLP fallback。2022/2023 年度页已有官方会期但曾漏入 TIMELINE，已在本轮修复并写入 [GUIDE.md](./GUIDE.md) 的会期同步自查规则。
3. **ASE 多 track 计数风险高**：DBLP `inproceedings` fallback 往往混入 NIER、tool、industry、journal-first、artifact 等条目，SUMMARY 与根表均不能写成 Research Track count。
4. **RE / REFSQ 已结束年度 proceedings 入口分散**：RE 的 IEEE Xplore conference number、REFSQ 的 Springer LNCS / LNBIP / CEUR 卷号需要后续专门复核；当前以官方 program / DBLP fallback 支撑基础入口。
5. **需求类未来年度比 SE flagship 更早出现 CFP**：REFSQ 2027 已有 official dates，因此已进入 2026/2027 TIMELINE；RE 2027/2028 仍未发现官方主页，不得预造。

## 7. 期刊试点踩坑记录

### 7.1 TSE

- IEEE TSE 页面、IEEE CSDL archive、IEEE Author Center / Publishing Portal、IEEE CFP 各自承担不同职责，不能把一个入口写成所有字段的事实来源。
- 投稿入口区分 [IEEE Publishing Portal](https://publishingportal.ieee.org/) 入口、Author Center 说明和实际 peer-review destination；TSE 专属 ScholarOne 子站未获官方当前页确认前只写作待核验 destination，不写成既定事实。
- 核心编辑人员画像见 [journal-a-tse/README.md](./journal-a-tse/README.md)：TSE CSDL 动态页不易抓取，当前以 IEEE CS EIC 公告、TSE 官方会议页、个人 / 机构主页和 DBLP 交叉核验；表中已使用 `核验等级 / 当前性` 区分当前 roster、公告、候选与待复核线索。
- 2022-2026 已用 DBLP volume/year 建 `entry article` baseline；2026 仍可能进行中，不作为年度闭合数。
- IEEE CSDL / Early Access 与 DBLP 年度归属可能错位，后续仍需按 publisher article type 交叉核验。
- TSE 常规 rolling submission 不进入 Mermaid；未发现 active dated special issue。

### 7.2 TOSEM

- ACM DL 正文和年度 issue 入口在命令行环境下较易受动态访问影响，DBLP 年度页是更稳定的书目信息 fallback。
- 投稿入口改为 [TOSEM ScholarOne 候选入口](https://mc.manuscriptcentral.com/tosem)，并保留 ACM DL TOSEM 当前页 / ACM submission sites 作为核查入口；canonical 入口仍需人工点击 ACM DL `Submit Manuscript` 当前跳转确认。
- ACM Papers for Practitioners 不是 TOSEM canonical online-first / Just Accepted archive；当前用 [ACM DL TOSEM Just Accepted](https://dl.acm.org/journal/tosem/just-accepted) 并保留动态访问受限说明。
- 核心编辑人员画像见 [journal-a-tosem/README.md](./journal-a-tosem/README.md)：ACM DL editorial-board 在命令行环境返回 403，旧镜像 roster 存在过期风险；当前用 ACM Editors-in-Chief 总页、ACM Updates / People of ACM、个人主页 / 机构页等替代路径交叉核验，并保留 `核验等级 / 当前性`。
- Agentic AI special issue 仅能作为线索记录，未发现明确 deadline，不能写入 Gantt。
- 2022-2026 已用 DBLP volume/year 建 `entry article` baseline；2026 仍可能进行中，不作为年度闭合数。

### 7.3 SoSyM

- SoSyM 同时存在 Springer journal page、Springer collections、SoSyM official site、Manuscript Central、DBLP 多个入口；根 README 和年度 README 必须分列主页、投稿、theme section、卷期、online-first 与 DBLP。
- SoSyM 投稿入口当前记录 [Manuscript Central](https://mc.manuscriptcentral.com/sosym)，但 Industry 5.0 CFP 已提示 SoSyM online submission system 将变更；后续必须以 Springer submission guidelines / SoSyM 当前 submission notes 为准。
- 核心编辑人员画像见 [journal-b-sosym/README.md](./journal-b-sosym/README.md)：官方站和 Springer editorial board 可直接核验 Editors-in-Chief / Associate Editor-in-Chief / Assistant Editors；Advisory Board 与 Ambassadors 暂不展开，避免把“核心人员”扩成全量关系网。
- 2022-2026 已用 DBLP volume/year 建 `entry article` baseline；2026 仍可能进行中，不作为年度闭合数。
- Industry 5.0 与 Engineering of Digital Twins 是两个独立 theme section；Industry 5.0 有 2026-02-15 intent、2026-07-15 submission、2026-10-15 notification，Digital Twins 是 rolling theme section，EDTConf'26 日期不是普通 SoSyM 投稿 deadline。
- SoSyM 2026 Industry 5.0 已同步进 [TIMELINE.md](./TIMELINE.md) dated event；Digital Twins 只进 rolling / 待补记录，不进主 Mermaid。
- 2027/2028/2029+ 未发现官方年度卷期或 dated CFP；年度页写 `⏳ 已检索未公布`，不预设未来卷号。

### 7.4 PR-4 剩余期刊踩坑

- **Springer collections 会产生真正的 dated events**：Requirements Engineering 2026 的 LLM collection、30th Anniversary collection、REFSQ 2026 collection 都是期刊 collection，不是会议 deadline；带明确 submission deadline 的 collection 已进入 [TIMELINE.md](./TIMELINE.md) 表格与 Mermaid。
- **Springer collections 的月份节点不能硬凑日期**：LLM collection 的 revision / final decision 只有月份时，只能放备注，不能生成精确 milestone。
- **Wiley WAF/403 不能用第三方页面替代官方 roster**：STVR 已保留 Wiley editorial board、for-authors、Early View、volume archive 等官方入口；命令行无法读取正文时必须写“待人工浏览器核验”，不得臆造当前 Editor-in-Chief / board roster。
- **STTT conference-based special issue 风险高**：STTT 常收 TACAS、SPIN、FMICS、Runtime Verification、ECBS 等扩展 / special issue 论文；期刊 DBLP `entry article` baseline 不得与对应会议 proceedings 计数混算，也不能由会议会期反推期刊 deadline。
- **Equinocs / Wiley Authors 这类 SPA 投稿系统只能作为入口**：命令行只能看到登录或前端壳时，需说明“入口已定位，具体表单 / journal routing 待浏览器或登录核验”。
- **未来年度不预设卷号**：2027/2028 期刊年度页可以保留 rolling submission 与 archive 复查入口，但未公布 volume / DBLP 年度页时不得预造卷号或论文数量。

### 7.5 对后续流程的建议

- 后续会议填充若修改 [TIMELINE.md](./TIMELINE.md)，必须保留期刊 rolling 表与 SoSyM Industry 5.0 dated event，避免会议数据回填时误删期刊行。
- 后续若继续做年度论文数量，应单独开计数复核：以当前 DBLP `entry article` baseline 为起点，再用 publisher issue / online-first 按 article type 交叉核验，不要混用口径。
- 期刊试点暴露出的主要问题不是模板字段缺失，而是同一字段需要明确“官方入口 / 投稿入口 / 出版入口 / DBLP fallback”的证据优先级。
- 后续期刊填充必须把核心编辑人员作为情报维度：优先核验 Editor-in-Chief / Editors-in-Chief / Managing Editor / editorial leadership，记录研究方向、代表作或近 5 年论文入口，并把 roster 完整性限制写清楚。

## 8. P0 强相关 venue 后续填充清单

P0 是“强相关先做完”的后续数据填充边界。当前已有 6 个试点 venue、5 个 PR-2 venue 与 3 个 PR-4 期刊 venue 完成基础建档；未建条目仅限下表仍标为 `⏳ 待建` 的 P0-B 会议。

| 目录名 | 类型 | CCF | 主要对应 project | 批次 | 状态 |
|---|---|---|---|---|---|
| [`conf-a-icse`](./conf-a-icse/README.md) | 会议 | A | P1/P2/P3/P4 | 会议试点 | 🟡 部分核验 |
| [`conf-a-fse`](./conf-a-fse/README.md) | 会议 | A | P1/P2/P4 | PR-2 | 🟡 部分核验 |
| [`conf-a-ase`](./conf-a-ase/README.md) | 会议 | A | P1/P2/P4 | PR-2 | 🟡 部分核验 |
| [`conf-a-issta`](./conf-a-issta/README.md) | 会议 | A | P2/P3/P4 | PR-2 | 🟡 部分核验 |
| [`journal-a-tse`](./journal-a-tse/README.md) | 期刊 | A | P1/P2/P3/P4 | 期刊试点 | 🟡 部分核验 |
| [`journal-a-tosem`](./journal-a-tosem/README.md) | 期刊 | A | P1/P2/P4 | 期刊试点 | 🟡 部分核验 |
| [`conf-b-models`](./conf-b-models/README.md) | 会议 | B | P1/P2/P3 | 会议试点 | 🟡 部分核验 |
| [`conf-b-re`](./conf-b-re/README.md) | 会议 | B | P1/P2 | PR-2 | 🟡 部分核验 |
| [`journal-b-re`](./journal-b-re/README.md) | 期刊 | B | P1/P2 | PR-4 | 🟡 部分核验 |
| [`journal-b-sosym`](./journal-b-sosym/README.md) | 期刊 | B | P1/P3 | 期刊试点 | 🟡 部分核验 |
| `conf-a-fm` | 会议 | A | P2/P3 | P0-B | ⏳ 待建 |
| `conf-a-cav` | 会议 | A | P3 | P0-B | ⏳ 待建 |
| [`conf-b-etaps`](./conf-b-etaps/README.md) | 会议 | B | P3 | 会议试点 | 🟡 部分核验 |
| `conf-b-vmcai` | 会议 | B | P2/P3 | P0-B | ⏳ 待建 |
| `conf-b-issre` | 会议 | B | P2/P3 | P0-B | ⏳ 待建 |
| [`journal-b-stvr`](./journal-b-stvr/README.md) | 期刊 | B | P2/P3 | PR-4 | 🟡 部分核验 |
| `conf-c-icfem` | 会议 | C | P2/P3 | P0-B | ⏳ 待建 |
| `conf-c-spin` | 会议 | C | P3 | P0-B | ⏳ 待建 |
| `conf-c-atva` | 会议 | C | P3 | P0-B | ⏳ 待建 |
| `conf-c-icst` | 会议 | C | P2/P3/P4 | P0-B | ⏳ 待建 |
| [`conf-c-refsq`](./conf-c-refsq/README.md) | 会议 | C | P1/P2 | PR-2 | 🟡 部分核验 |
| [`journal-c-sttt`](./journal-c-sttt/README.md) | 期刊 | C | P3/P4 | PR-4 | 🟡 部分核验 |

## 9. P1 / P2 后续 venue

以下 venue 不属于当前试点数据填充目标；后续在 P0 试点与批量节奏稳定后分批推进。

| Venue | 类型 | CCF | 主要价值 | 后续批次 |
|---|---|---|---|---|
| `conf-b-saner` | 会议 | B | 维护、演化、修复 | P1 |
| `conf-b-icsme` | 会议 | B | 维护、演化、修复 | P1 |
| `conf-b-icpc` | 会议 | B | 程序理解、LLM4SE 实证 | P1 |
| `conf-b-esem` | 会议 | B | 实证评估与 benchmark | P1 |
| `journal-b-ese` | 期刊 | B | LLM4SE 实证 | P1 |
| `journal-b-jss` | 期刊 | B | 软工综合、系统案例 | P1 |
| `journal-b-ist` | 期刊 | B | 软工综合、需求/测试 | P1 |
| `journal-b-scp` | 期刊 | B | 形式化、程序与工具链 | P1 |
| `journal-b-jsep` | 期刊 | B | 演化、维护、修复 | P1 |
| `conf-c-qrs` | 会议 | C | 质量、可靠性、安全 | P1 |
| `conf-c-tase` | 会议 | C | 形式化与理论软工 | P1 |
| `journal-c-sqj` | 期刊 | C | 软件质量与评估 | P1 |
| `conf-c-apsec` | 会议 | C | 区域性软工、LLM4SE | P2 |
| `conf-c-seke` | 会议 | C | 知识工程与软工交叉 | P2 |
| `conf-c-ease` | 会议 | C | 实证评估 | P2 |
| `conf-c-msr` | 会议 | C | 仓库挖掘、数据集 | P2 |
| `conf-c-rv` | 会议 | C | 运行时验证 | P2 |

## 10. 核心 URL / 超链接覆盖口径

后续每个 venue 数据填充不得只写“主页 / CFP / 论文集见年度页”，而必须把核心 URL 直接挂进根 README、年度 README 和 [TIMELINE.md](./TIMELINE.md) 的表格中。

| 对象 | 必须直接挂链接的字段 | 说明 |
|---|---|---|
| 会议根 README 年度汇总表 | 年度主页、CFP、Important Dates、Submission system、Program / Accepted papers、Proceedings、DBLP 年度页 | 每个年份 row 都要能直接点击核心入口；未公布 / 待官网也要显式标注。 |
| 会议年度 README | 年度主页、CFP、Important Dates、Submission system、Program / Accepted papers、Proceedings、DBLP 年度页 | 年度页是事实源，必须有“年度核心 URL 索引”。 |
| 期刊根 README 年度汇总表 | 期刊主页、Author guidelines、Submission system、Special issue / CFP、Volume / issue、Online first、DBLP 年度页 | 期刊不硬套会议 deadline，但链接字段不能缺。 |
| 期刊年度 README | Author guidelines、Submission system、Special issue / topical collection、Volume / issue、Online first、Publisher article list、DBLP 年度页 | rolling 与 special issue 分开记录。 |
| TIMELINE.md | 事件官方来源、年度主页、论文集 / 名录、本库年度页 | dated event 和 rolling journal 表都必须是可点击索引。 |

缺失链接必须写 `待补`、`未公布`、`无已知` 或 `⏳ 已检索未公布`，并在证据 / 核查记录中说明核查时间；不得留空或用第三方聚合页冒充官方来源。

## 11. TIMELINE.md 同步验收口径

[TIMELINE.md](./TIMELINE.md) 是当前文库的一等入口。后续 venue 数据填充时必须同步满足：

1. `TIMELINE.md` 至少覆盖 `2022` 至当前年份 + 2；若已公布更远未来年度官方信息，也必须新增对应年份章节；年份按降序排列。
2. 当前文库采用“事件发生年份”组织时间线；会议 edition 的 ddl 落在前一年时，应在前一年章节记录，并在 Venue 列保留 edition。
3. 每个年份章节包含一张投稿事件总表，表内按时间升序排列。
4. 每个表格事件都必须链接到事件官方来源、年度主页、本库年度 README；若论文集 / 名录 / 卷期入口已发布，也必须直接挂链接。
5. 每个年份章节包含 Mermaid `gantt` 可视化；单日 deadline 用 `milestone`，多日窗口用普通任务。
6. 期刊 rolling submission 不进入 Mermaid 图；期刊 special issue / topical collection deadline 进入年度时间线。
7. 会议 dated events、期刊 rolling 表和期刊 special issue dated events 合流后必须共存，不得互相删除或用空白占位覆盖。
8. 如果年度事件过多，应拆多张 Mermaid 图，不允许生成难以阅读的超长单图。

## 12. 当前验收口径

逐 venue 数据填充时，默认检查：

1. venue README 顶部有 `信息更新时间`，文末有更新日志表。
2. venue README 的年度汇总表至少覆盖 `2022` 至当前年份 + 2；若已公布更远未来年度官方信息，也必须继续纳入；按年份降序排列。
3. 每个年份行都能跳转到年度 README。
4. 每个年份行都包含官方年度主页、CFP / Important Dates、论文集 / 论文名录或期刊卷期等核心链接；若未找到，明确写 `待补`、`未公布` 或 `⏳ 待官网`。
5. 已结束会议必须尽量包含论文数量、官方论文名录 / proceedings 链接；若只能用 `DBLP`，必须注明 fallback 口径。
6. 尚未召开的会议只要能找到官方主页、`CFP` 或 important dates，也必须入表。
7. 所有关键时间精确到分钟；官方只给日期时必须显式标注 `待补时刻`；官方给 `AoE` 时保留原时区。
8. 会议和期刊使用不同结构，不能把期刊硬写成会议式 ddl 表。
9. 证据链接优先官方来源；出版商页面用于 proceedings / volume issue；`DBLP` 仅作论文名录 fallback 或核验。
10. [SUMMARY.md](./SUMMARY.md) 统计数字与实际目录保持一致。
11. venue 根 README 必须维护核心人员情报；会议与期刊分轨记录官方角色来源、研究方向、代表作 / 近年论文入口和核验状态，期刊继续保留 `核验等级 / 当前性`。
12. 文档正文必须区分“已完成基础核验的事实”和“待补占位”，不得把待建 venue 写成已完成，也不得把已有试点 venue 写回待建。

## 13. 待补与核查记录

| Venue | 年份 | 问题 | 当前处理 | 下一步 |
|---|---|---|---|---|
| ICSE | 2028 | 年度主页当前 Access denied，仅找到 Hawaii 预告 | 根 README / 年度 README 不写成正式 CFP | 后续复查年度主页与 Research Track |
| ICSE | 2026 | accepted papers 已公开，但 proceedings / DBLP 年度页未公开 | 论文数量按官方 Research Track accepted papers 表记录，核验状态为部分核验 | 后续补 DBLP / proceedings |
| MoDELS | 2026 | submission / rebuttal 已过但 notification 尚未到达 | 当前阶段统一写作 `🟡 审稿中`，program probe 为 Access denied | notification 后复核状态并补 accepted papers / proceedings |
| MoDELS | 2027-2028 | 官方 home / dates / track 未发布 | 年度页标 `⏳ 已检索未公布` | 后续复查 researchr 与长期主页 |
| MoDELS | 2024 | proceedings 页面当前 accessDenied | 继续挂官方 URL，数量用 DBLP fallback | 后续复查 proceedings 页面 |
| ETAPS/TACAS | 2028 | 只有 ETAPS 主页，无 TACAS CFP / dates | 只记录会期，不写 TACAS submission | 后续复查 CFP 与 TACAS 分会页 |
| ETAPS/TACAS | 2024 | TACAS artifact deadline 页面版本差异 | 暂记 `2023-10-26 23:59 AoE` 并保留备注 | 后续精查官方页面 |
| TSE | 2027 / 2028 / 2029+ | 未发现官方年度卷期、online-first 年度入口或 dated special issue | 年度页写 `⏳ 已检索未公布`；不预设未来卷号 | 后续待 IEEE CSDL / DBLP 发布后补录 |
| TOSEM | 2027 / 2028 / 2029+ | 未发现官方年度卷期、online-first 年度入口或 dated special issue | 年度页写 `⏳ 已检索未公布`；不预设未来卷号 | 后续待 ACM DL / DBLP 发布后补录 |
| FSE | 2022-2026 | PACMSE / ACM DL proceedings 与 DBLP 年度页尚未逐项闭合，2025 initial notification 年份疑似官方页笔误 | 年度页保留待复核说明，TIMELINE 只同步较稳定的主 submission / notification / 会期 | 后续按 ACM DL / PACMSE article type 与 official program 逐年复核 |
| ASE | 2022-2025 | DBLP `inproceedings` fallback 是全 proceedings，不能代表 Research Track 数量 | 根 README 与年度页均显式写“非主 track count” | 后续从 official program filter 或 ACM / IEEE proceedings 分轨复核 Research Track count |
| ISSTA | 2024-2025 | co-located / joint week 与 proceedings 入口可能和 FSE / SPLASH / ECOOP 混淆 | 根 README 与年度页冻结 ISSTA 独立计数口径 | 后续复核 ACM DL / PACMSE ISSTA issue 与 official accepted papers |
| RE | 2022-2025 | IEEE Xplore proceedings conference number / stable URL 未补齐 | 年度页用 official program + DBLP fallback，publisher proceedings 写待补 | 后续按 IEEE Xplore / DBLP 逐年补 proceedings 与 research-track count |
| REFSQ | 2022-2026 | Springer LNCS / LNBIP / CEUR 与 DBLP 入口分散 | 年度页保留 official program / accepted papers，proceedings 卷号写待补 | 后续补 Springer volume、CEUR workshop 及 DBLP 分轨计数 |
| REFSQ | 2028 | 未发现官方年度主页或 CFP | 年度页写 `⏳ 已检索未公布` | 后续复查 REFSQ official / researchr series |
| SoSyM | 2027 / 2028 / 2029+ | 未发现官方年度卷期、online-first 年度入口或 dated special issue | 年度页写 `⏳ 已检索未公布`；不预设未来卷号 | 后续待 Springer / DBLP 发布后补录 |
| SoSyM | 2026 | Digital Twins 是独立 rolling theme section，且 EDTConf'26 日期是 presentation target，不是普通 SoSyM 投稿 deadline | 只放 rolling / 待补记录，不进主 dated timeline | 后续若官方给出固定 journal submission deadline，再同步年度表与 Mermaid |
| Requirements Engineering | 2026 | LLM collection revision / final decision 仅给月份，30th Anniversary 与 REFSQ 2026 collection 给日期但无具体时刻 | TIMELINE 只同步明确日期的 2026-04-30、2026-06-20、2026-06-29；月份节点留备注 | 后续若 Springer 补具体 revision / final decision 日期，再补年度表与 Mermaid |
| Requirements Engineering | 2027 / 2028 / 2029+ | 未发现官方年度卷期、DBLP 年度页或 2029+ dated CFP | 年度页写 `⏳ 已检索未公布`；不预设未来卷号 | 后续待 Springer / DBLP 发布后补录 |
| STVR | 2022-2028 / 2029+ | Wiley Online Library CLI WAF/403，editorial board、for-authors、volume / issue 正文和 Early View 需人工浏览器核验 | 保留官方 URL；用 DBLP 作为论文名录 / 计数 fallback；不臆造 roster 或 future volume | 后续用浏览器核验 Wiley editorial board、ISSN、author guidelines 与卷期正文 |
| STTT | 2022-2026 | conference-based special issue / invited / extended papers 与常规期刊 article 混在 DBLP 年度 baseline 中 | 仅写 DBLP `entry article` baseline，并在根 README 与年度页说明不得和会议 proceedings 混算 | 后续按 Springer issue TOC / article type 拆普通稿、special section 与 invited papers |
| STTT | 2027 / 2028 / 2029+ | 未发现官方年度卷期、DBLP 年度页或 active dated CFP | 年度页写 `⏳ 已检索未公布`；不预设未来卷号 | 后续待 Springer / DBLP 发布后补录 |

## 14. 更新日志

更新日志按时间降序排列，最新记录置于最上方。

| 时间 | 更新内容 |
|---|---|
| `2026-06-05 12:35` | PR-4 SUMMARY/GUIDE 专项复核：确认 14 个 venue / 98 个年度 README 统计一致，并澄清 P0 待建项不再包含 Requirements Engineering、STVR、STTT。 |
| `2026-06-05 12:18` | 完成 PR-4 剩余 P0 期刊基础建档合流：新增 Requirements Engineering、STVR、STTT 共 3 个 venue、21 个年度 README，同步 TIMELINE rolling / dated events，并记录 Springer collections、Wiley WAF/403 与 STTT conference-based special issue 计数 caveat。 |
| `2026-06-05 10:00` | 修复 PR-2 修复后复审发现的 ISSTA 2022/2023 会期漏入 TIMELINE 问题，并把会期同步检查主要沉淀到 GUIDE。 |
| `2026-06-05 08:46` | 完成 PR-2 软工 / 需求会议基础建档：新增 FSE、ASE、ISSTA、RE、REFSQ 共 5 个 venue、35 个年度 README，同步 TIMELINE，并记录 PR-2 计数 / proceedings / co-location 待补项。 |
| `2026-06-05 00:36` | 合入 PR-1B 期刊试点后完成 SUMMARY 合流：重算 6 个 venue / 42 个年度 README，保留会议试点与期刊试点事实、踩坑记录、P0 状态和待补记录。 |
| `2026-06-04 23:27` | 修复 PR-1B 复审 I 级问题：补充 TOSEM 在 ACM DL editorial-board 403 后的替代核验路径，并统一 SoSyM 复审时间戳为分钟粒度。 |
| `2026-06-04 23:04` | PR-1B 吸收 PR-1A 合流协议：SUMMARY 标注会议试点 owner，补充跨 PR 合流记录，并把 TIMELINE 事件发生年份、核心人员和模板占位协议纳入验收口径。 |
| `2026-06-04 22:20` | 同步 ICSE/MoDELS/ETAPS review 修复状态，记录根表计数口径与 MoDELS 2026 审稿中状态。 |
| `2026-06-04 22:05` | 根据 PR-1B 正式复审补充 2022-2026 DBLP `entry article` baseline，并把 TSE / TOSEM 核心人员画像改为显式证据等级分层。 |
| `2026-06-04 21:55` | 同步核心人员情报覆盖状态，记录核心人员表可追溯性试点结论，并补充更新日志降序提示。 |
| `2026-06-04 21:46` | 根据用户补充要求，把期刊核心编辑人员画像纳入 PR-1B 试点产物和后续 GUIDE 规则，三本期刊根 README 已补当前公开可核验的核心人员表。 |
| `2026-06-04 21:10` | 完成 PR-1A 会议试点：新增 ICSE、MoDELS、ETAPS/TACAS 根 README 与 2022-2028 年度 README，同步 TIMELINE，并记录试点踩坑结论。 |
| `2026-06-04 20:43` | 回填 PR-1B 期刊试点状态：完成 TSE / TOSEM / SoSyM 根 README 与 21 个年度 README，更新 TIMELINE 同步状态，并新增期刊试点踩坑记录。 |
| `2026-06-04 19:37` | 补充核心 URL / 超链接覆盖口径，要求根 README、年度 README 和 TIMELINE 都直接挂核心来源链接。 |
| `2026-06-04 18:55` | 明确默认未来检索/占位下限为当前年份 + 2（当前到 2028），更远未来若已有官方 CFP / important dates 也必须纳入。 |
