# UPPAAL 应用验证文库总账

本文件是 `open_explore/uppaal_apps/` 论文集的总账，用于记录当前已经正式入账的 `UPPAAL` 应用验证论文、分类口径、公开性盘点、更新进展和失败/阻塞历史。

## 文档定位与使用方式

推荐使用顺序如下：

1. 先读 [README.md](./README.md)，了解本论文集定位和与 [uppaal_tech/README.md](../uppaal_tech/README.md) 的边界。
2. 再读 [GUIDE.md](./GUIDE.md)，确认筛选、分流、回填和一致性检查规范。
3. 若任务涉及单篇 `desc.md`，再读 [DESC_GUIDE.md](./DESC_GUIDE.md)。
4. 最后使用本文件查看当前统计、统一论文表、公开性清单和失败记录。

## 当前关注边界

1. 这里只收录 `UPPAAL` 被用于**形式化验证具体模型或系统**的应用论文。
2. 主贡献是 `UPPAAL` 本体技术的论文，不在这里入账，应进入 [uppaal_tech/README.md](../uppaal_tech/README.md)。
3. 只是在正文中顺带提一下 `UPPAAL` 的条目，不应正式入账。
4. 主要目标是调度、优化、测试或控制合成，但没有清晰验证任务、性质或结论的论文，当前不作为优先收录对象。

## 检索关键词簇

### 当前推荐关键词簇

- `UPPAAL + formal verification/model checking + protocol/controller/embedded system/field bus/web service/multimedia`
- `UPPAAL + safety/liveness/deadlock/response time/consistency/throughput/jitter/latency + case study`
- `UPPAAL + Philips/Bang & Olufsen/DACAPO/AF100/WS-AT + verification`
- `UPPAAL + industrial case study + protocol/control software`

### 已观察到的高命中特征

- 题目、摘要或关键词直接出现 `verification`、`analysis`、`case study`、`industrial`
- 正文明确交代被验证系统、模型抽象、性质类型和验证结果
- 官网 `Case Studies` / `Benchmarks` 反向回溯 `2010` 年前经典案例，命中率较高
- 具名系统名、协议名或产品名与 `UPPAAL` 联用，比泛搜 `application` 更稳定

### 已观察到的低命中特征

- 只有工具名，没有验证任务词
- 只有应用对象，没有 `UPPAAL`
- 只有 `optimization`、`testing`、`scheduling`，没有 `verification/model checking`
- 只搜泛 timed automata 背景，没有具名对象或协议名
- 老案例的历史模型链接经常失效，不能把“官网曾提过模型”直接当成“当前可下载”

### 检索倾向调整

- 对 `2010` 年前条目，优先沿官网案例页与 benchmark 页反向建库，再补 DOI 与 `bibtex.bib`
- 当前高价值方向已经验证为：协议通信、控制器与嵌入式、工业 field bus、multimedia `QoS`、web service transaction
- 只要用户没有明确豁免，正式入账时就同步补齐 `desc.md`
- 公开性信息默认单独入账到“案例/模型/数据公开性清单”，不再用 `详度/实现` 这类弱稳定列来代替

## 当前收录统计

| 统计项 | 数值 | 年份信息 |
|---|---:|---|
| 已收录顶层条目 | 10 | 覆盖 `1996-2010` |
| 其中已补 `desc.md` | 10 | `1996-2010` 均已完成整理 |
| 当前 `🟢 直接可用` | 8 | 主要集中于协议与控制器代表案例 |
| 当前 `🟡 可整理` | 2 | 主要是更偏方法展示或规模描述较薄的案例 |
| 当前 `⏳ 尚未提取` | 0 | 无 |
| 公开性分布 | `🟠 7 / 🔒 3` | 当前未确认有可直接获取的公开模型/数据包 |
| 最早年份 | 1996 | 首批收录始于经典协议冲突案例 |
| 最晚年份 | 2010 | 当前上界为 `WS-AT` 协议分析 |
| 当前失败/阻塞记录 | 2 | 记录见“失败与阻塞记录” |

## 按年份分布统计

| 年份 | 条目数 | 已补 `desc.md` | 备注 |
|---|---:|---:|---|
| 1996 | 1 | 1 | Philips 音频协议总线冲突案例 |
| 1997 | 3 | 3 | 收录重传协议、TDMA 启动与 B&O 工业协议 |
| 1998 | 2 | 2 | 覆盖 lip sync 与车辆换挡控制 |
| 1999 | 1 | 1 | B&O 电源控制器验证 |
| 2000 | 1 | 1 | ABB `AF100` field bus 工业案例 |
| 2003 | 1 | 1 | multimedia `QoS` 验证案例 |
| 2010 | 1 | 1 | web service transaction 协议分析 |

## 应用分类口径

| 一级领域 | 说明 | 当前正式条目数 |
|---|---|---:|
| 🛰️ 协议与通信系统 | 网络协议、通信协议、分布式交互等 | 4 |
| 🎛️ 控制器与嵌入式系统 | 控制逻辑、嵌入式控制器、实时控制软件等 | 2 |
| 🏭 工业系统与 `CPS` | 制造、工业控制、混合系统、工程案例等 | 1 |
| 🚦 交通、调度与资源系统 | 交通控制、调度、实时资源系统等 | 0 |
| 🧩 软件、架构与组件系统 | 软件组件、并发软件、软件架构等 | 3 |

说明：

1. 上表是当前版本的领域骨架，不是封闭不变的固定枚举。
2. 若后续实际收录中出现新的稳定应用簇，或现有类别已经过宽，应按实际情况动态扩充、拆分或合并领域类型。
3. 一旦发生动态调整，必须同步更新本节统计口径以及统一论文总表中的 `领域` 字段。

## 状态与公开性口径

### 条目状态

| 状态 | 含义 |
|---|---|
| 🟢 | 直接可用：已有较完整单篇 `desc.md`，能直接服务博士研究比较或案例提炼 |
| 🟡 | 可整理：有价值，但案例规模、结构细节或复用度仍略弱于主代表案例 |
| ⚪ | 未收获：不满足目标，或无法形成可靠、可追溯的产物 |
| ⏳ | 尚未提取：论文已入库，但 `desc.md` 尚未完成 |

### 案例/模型/数据可获取性

| Emoji | 含义 |
|---|---|
| 🟢 | 可直接获取：存在当前可访问的公开下载链接、仓库、补充材料页或官方案例入口，能直接拿到相应材料 |
| 🟡 | 需联系申请：原文明确说明需要联系作者、团队或项目方申请 |
| 🟠 | 信息不清：原文或官网提到材料存在，但没有稳定、清晰、当前可用的公开路径，或历史链接已失效 |
| 🔒 | 难以取得：案例强依赖企业内部资产、工业实现、受限规格或现实上难以公开的材料 |

### `UPPAAL线` 口径

| 取值 | 含义 |
|---|---|
| `UPPAAL` | 主线工具或经典 `UPPAAL` 验证 |
| `UPPAAL SMC` | 统计模型检查应用 |
| `UPPAAL Tiga` | timed game / controller synthesis 相关应用 |
| `UPPAAL CORA` | cost-optimal / priced timed automata 相关应用 |
| `UPPAAL Stratego` | 策略综合、学习或规划相关应用 |
| `UPPAAL PORT` | 组件化、本地时间或 `PORT` 线应用 |
| `ECDAR` | timed I/O specification / compositional verification 相关应用 |
| `其他 UPPAAL 谱系变体` | 其他明确属于 `UPPAAL` 谱系的变体 |

## 统一论文总表

统一字段固定为：

`年份 | Key | 标题 | 关键词 | 领域 | 被验证系统 | 系统特点 | 系统规模 | UPPAAL线 | 验证任务 | 性质类型 | 状态 | 一句话简介 | 链接`

维护规则：

1. 第一列 `年份` 为必填字段，不得省略。
2. 全表必须按年份从低到高排列；同年按 `Key` 字典序稳定排序。

| 年份 | Key | 标题 | 关键词 | 领域 | 被验证系统 | 系统特点 | 系统规模 | UPPAAL线 | 验证任务 | 性质类型 | 状态 | 一句话简介 | 链接 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1996 | `bengtsson96` | Verification of an Audio Protocol with Bus Collision Using UPPAAL | 音频协议, 总线冲突, 广播通信 | 🛰️ 协议与通信系统 | Philips 音频控制协议（双发送端冲突版本） | 单总线、广播/碰撞检测、工业背景 | `6` 个 automata；状态空间约为单发送端版的 `10^3` 倍 | `UPPAAL` | 协议碰撞处理与时序容错验证 | 安全、有界活性、时序容错 | 🟢 | 用 timed automata 验证双发送端冲突协议，并确定 `5%/6%` 容错边界。 | [paper](./bengtsson96-audio-protocol-bus-collision/) |
| 1997 | `dargenio97` | The Bounded Retransmission Protocol Must Be on Time! | 文件传输, 有界重传, 超时 | 🛰️ 协议与通信系统 | BRP 有界重传文件传输协议 | 分块传输、丢包信道、超时/中止 | 发送端/接收端 + `T1/T2` 定时器；原文未给统一状态规模 | `UPPAAL` | 服务符合性与超时参数验证 | 安全、服务符合性、时序约束 | 🟢 | 通过 timed/untimed 对照说明 BRP 正确性依赖真实超时结构。 | [paper](./dargenio97-bounded-retransmission-time/) |
| 1997 | `havelund97` | Formal Modelling and Analysis of an Audio/Video Protocol: An Industrial Case Study Using UPPAAL | 工业协议, 音视频总线, 碰撞检测 | 🛰️ 协议与通信系统 | Bang & Olufsen 音视频控制协议 | 单总线、`2800` 行汇编、工业真实协议 | `9` 个 automata；`5` 次主要迭代、约 `3` 个月；错误轨迹近 `2000` 步 | `UPPAAL` | 协议建模、错误定位与修复验证 | 安全、有界活性、一致性 | 🟢 | 通过自动诊断轨迹定位并修复 B&O 工业协议中的时序错误。 | [paper](./havelund97-audio-video-protocol/) |
| 1997 | `lonn97` | Formal Verification of a TDMA Protocol Start-Up Mechanism | `TDMA`, 启动同步, 时钟漂移 | 🛰️ 协议与通信系统 | DACAPO `TDMA` 启动机制 | 多主站、启动同步、时钟漂移 | `4` 个站点 + 总线；时钟漂移 `±10^-3` | `UPPAAL` | 启动同步与截止时间验证 | 安全、有界响应、时序约束 | 🟢 | 证明四站 TDMA 系统能在漂移条件下于有界时间内完成同步。 | [paper](./lonn97-tdma-startup-mechanism/) |
| 1998 | `bowman98` | Automatic Verification of a Lip Synchronisation Algorithm Using UPPAAL | lip sync, multimedia, `QoS` | 🧩 软件、架构与组件系统 | lip synchronization 算法 | 音视频双流同步、jitter/skew、watchdog | 音频 `30 ms`/包、视频 `40 ms`/帧；non-anchored jitter 下约 `1031 ms` | `UPPAAL` | 同步边界、timelock 与 `QoS` 验证 | `QoS` 时序、timelock/deadlock | 🟢 | 自动分析 lip sync 算法，发现它会在部分场景下先 timelock 而非正常报错。 | [paper](./bowman98-lip-synchronisation-algorithm/) |
| 1998 | `lindahl98` | Formal Design and Analysis of a Gear Controller | 换挡控制, 车辆控制, 有界响应 | 🎛️ 控制器与嵌入式系统 | 车辆 prototype gear controller | 控制 clutch/engine/gearbox，安全关键 | `46` 条公式；完整换挡 `<=1.5 s`；验证约 `2.99 s` | `UPPAAL` | 控制器设计验证与响应时间检查 | 安全、有界响应 | 🟢 | 在工业环境假设下验证换挡控制器，并把 bounded response 转成可达性分析。 | [paper](./lindahl98-gear-controller/) |
| 1999 | `havelund99` | Formal Verification of a Power Controller Using the Real-Time Model Checker UPPAAL | 电源控制, 中断处理, 音视频组件 | 🎛️ 控制器与嵌入式系统 | 音视频组件 power controller | 多任务优先级、中断无丢失、上下电 | `15` 条性质；发现并修正 `3` 个设计错误 | `UPPAAL` | 电源控制逻辑与中断安全验证 | 安全、有界响应、时序约束 | 🟢 | 验证多任务电源控制器，修正设计错误并发现中断频率上界需求。 | [paper](./havelund99-power-controller/) |
| 2000 | `david00` | Modelling and Analysis of a Commercial Field Bus Protocol | field bus, `AF100`, 工业调试 | 🏭 工业系统与 `CPS` | ABB `AF100` bus coupler / data link layer | 商业 field bus、超时/重传/信号量 | 面向 `80` 站；数百页规格 + 数千行源码；`82/35` 条性质 | `UPPAAL` | 大型工业协议错误定位 | 安全、同步正确性、时序约束 | 🟢 | 通过抽象模型快速定位 AF100 工业协议中的同步与超时错误源。 | [paper](./david00-commercial-field-bus-protocol/) |
| 2003 | `bordbar03` | Verification of Timeliness QoS Properties in Multimedia Systems | `QoS`, throughput, latency | 🧩 软件、架构与组件系统 | distributed multimedia video player 示例 | ODP/QoS 契约、QTA/test automata | video player 示例；原文未给统一 benchmark 规模 | `UPPAAL` | Timeliness `QoS` 属性构造与验证 | throughput、jitter、latency | 🟡 | 通过 QTA 把多媒体 `QoS` 属性规约为 `UPPAAL` 可达性问题。 | [paper](./bordbar03-timeliness-qos-multimedia/) |
| 2010 | `ravn10` | A Formal Analysis of the Web Services Atomic Transaction Protocol with UPPAAL | web services, distributed transaction, consistency | 🧩 软件、架构与组件系统 | `WS-AT` 分布式事务协议 | coordinator + participants、2PC/3-phase、TLA+ 对照 | 可验证至 `5` 个参与者 | `UPPAAL` | 协议一致性与工具对照验证 | 安全、一致性、可达性 | 🟡 | 把 WS-AT 从 TLA+ 转写为 `UPPAAL` 模型，并比较两类工具链的性能与扩展性。 | [paper](./ravn10-web-services-atomic-transaction/) |

## 案例/模型/数据公开性清单

| 论文 | 状态 | 案例/模型/数据 | 来源类型 | 制作/来源方式 | 可获取性 | 获取方式/链接 | 简述 |
|---|---|---|---|---|---|---|---|
| [bengtsson96](./bengtsson96-audio-protocol-bus-collision/desc.md) | 🟢 | Philips 音频协议 timed automata 案例 | 工业协议案例（历史 benchmark 入口） | 论文正文 + 官方 benchmark 历史条目 `philaudio` | 🟠 | [DOI](https://doi.org/10.1007/3-540-61474-5_73)；[UPPAAL Benchmarks](https://uppaal.org/benchmarks/) | benchmark 页仍可见案例名，但当前公开直链已失效 |
| [dargenio97](./dargenio97-bounded-retransmission-time/desc.md) | 🟢 | BRP 协议模型 | 协议案例 | 论文正文重建 | 🟠 | [DOI](https://doi.org/10.1007/BFb0035403) | 原文未提供独立模型包或仓库 |
| [lonn97](./lonn97-tdma-startup-mechanism/desc.md) | 🟢 | DACAPO 启动同步模型 | 协议案例 | 论文正文重建 | 🟠 | [论文 PDF](https://uppaal.org/texts/lp-prfts97.pdf) | 论文可得，但无独立模型入口 |
| [havelund97](./havelund97-audio-video-protocol/desc.md) | 🟢 | B&O 音视频协议工业案例 | 工业实现案例 | 工业实现 + 论文描述 + 官网案例页 | 🔒 | [DOI](https://doi.org/10.1109/REAL.1997.641264)；[UPPAAL Case Studies](https://uppaal.org/casestudies/) | 真实资产来自工业实现，论文未公开完整模型与原始协议资产 |
| [bowman98](./bowman98-lip-synchronisation-algorithm/desc.md) | 🟢 | lip sync 算法模型 | 学术算法案例 | 论文正文重建 | 🟠 | [论文 PDF](https://uppaal.org/texts/bfklm-fimcs98.pdf) | 无独立模型/输入流数据包 |
| [lindahl98](./lindahl98-gear-controller/desc.md) | 🟢 | gear controller 与环境模型 | 工业控制案例 | 工业合作需求 + 论文描述 | 🔒 | [DOI](https://doi.org/10.1007/BFb0054178) | 控制器需求与环境资产来自工业项目，难以直接公开取得 |
| [havelund99](./havelund99-power-controller/desc.md) | 🟢 | power controller 历史模型 `bopdp` / `bopdpFIXED` | 工业控制案例（历史 benchmark 入口） | 论文正文 + 官方 benchmark 历史条目 | 🟠 | [DOI](https://doi.org/10.7146/BRICS.V6I8.20065)；[UPPAAL Benchmarks](https://uppaal.org/benchmarks/) | benchmark 页仍记有模型名，但当前公开直链已失效 |
| [david00](./david00-commercial-field-bus-protocol/desc.md) | 🟢 | AF100 bus coupler 案例 | 工业协议案例 | ABB 工业规格/实现 + 论文抽象 | 🔒 | [DOI](https://doi.org/10.1109/EMRTS.2000.854004) | 案例依赖商业协议规格与实现资产，原文未公开模型包 |
| [bordbar03](./bordbar03-timeliness-qos-multimedia/desc.md) | 🟡 | video player + QTA 示例 | 方法示例案例 | 论文正文重建 | 🟠 | [DOI](https://doi.org/10.1007/978-3-540-39893-6_30) | 方法公开，但无独立 QTA 工具实现或示例模型包 |
| [ravn10](./ravn10-web-services-atomic-transaction/desc.md) | 🟡 | WS-AT `UPPAAL` 模型（历史 `rvs10.zip`） | 软件协议案例（历史 case-study 入口） | 论文正文 + 官网案例页历史链接 | 🟠 | [DOI](https://doi.org/10.1007/978-3-642-16558-0_47)；[UPPAAL Case Studies](https://uppaal.org/casestudies/) | 官网仍提历史压缩包，但当前公开链接返回 `404` |

## 初步归类与当前观察

1. 协议与通信案例仍是 `1996-2010` 早期 `UPPAAL` 应用线的主轴，占当前收录的 `4/10`。
2. 工业案例往往最能清楚说明“被验证系统是什么、错误在哪里、验证怎么帮忙修”，但公开性通常最差。
3. 老案例的官网 `Case Studies` / `Benchmarks` 入口对建库仍然很有价值，但历史工件链接大量失效，后续不能把“被提到”直接当作“可下载”。
4. 对本研究最有价值的共同点不是领域本身，而是这些论文都显式处理了环境假设、时间边界和失败模式。
5. 目前这 `10` 篇里还没有确认到“当前仍可直接下载”的公开模型/数据包，因此公开性维度更适合维护为单独清单，而不是乐观地写成“实现可得”。

## 更新日志

| 时间 | 更新内容 | 整理策略 | 本轮侧重 |
|---|---|---|---|
| 2026-03-29 | 初始化 `open_explore/uppaal_apps/`，建立 [README.md](./README.md)、[GUIDE.md](./GUIDE.md)、[SUMMARY.md](./SUMMARY.md) 三个核心文件 | 先把应用文库与 `uppaal_tech/` 拆开，固定边界与总账骨架 | 先解决结构拆分，后续再正式扩充应用条目 |
| 2026-03-31 | 重写 [README.md](./README.md)、[GUIDE.md](./GUIDE.md)、[SUMMARY.md](./SUMMARY.md)，并新增 [DESC_GUIDE.md](./DESC_GUIDE.md) | 将文库主线收紧到“使用 `UPPAAL` 对具体对象进行形式化验证”的应用论文，补齐大规模扩库所需的字段、状态和单篇规范 | 为后续批量抓取控制系统、嵌入式系统、工业 `CPS` 与协议验证文献做准备 |
| 2026-03-31 | 补充领域类型动态扩充规则，并将统计区改为显式含年份的表格 | 把领域分类从固定枚举调整为“当前骨架 + 按实际收录动态扩充”，同时强化时间维度统计与排序口径 | 为后续按年份维护大规模文献总表做准备 |
| 2026-03-31 | 首批纳入 `10` 篇 `2010` 年及以前的 `UPPAAL` 应用论文，补齐每篇的 `paper.pdf + paper_content.txt + bibtex.bib` | 基于官网 `Case Studies` 与 `Documentation` 反向筛查 `20+` 个候选，优先选择 PDF 可稳定获取且验证主线清晰的协议、控制器、工业和软件案例 | 建立 `1996-2010` 的早期应用主线骨架 |
| 2026-03-31 | 为首批 `10` 篇论文全部补齐 `desc.md`，并把总账字段改为“被验证系统 / 系统特点 / 系统规模 + 公开性清单” | 取消 `详度/实现` 两列，改为维护单篇 `desc.md`、统一论文表和“案例/模型/数据公开性清单”；同时把“默认必须写 `desc.md`”落进 [README.md](./README.md) 与 [GUIDE.md](./GUIDE.md) | 让 `uppaal_apps/` 的维护方式对齐 `baselines` 的公开性思路，并固定今后入账口径 |

## 失败与阻塞记录

| 时间 | 候选条目/对象 | 问题 | 当前处理 |
|---|---|---|---|
| 2026-03-31 | Model-Checking Real-Time Control Programs | 官网旧链接 `https://homes.cs.aau.dk/~paupet/papers/ikllmmpt-ecrts00.pdf` 与对应 `.bib.txt` 返回 `404`，无法稳定取得三件套 | 本轮未正式入账；已以 [bordbar03-timeliness-qos-multimedia/](./bordbar03-timeliness-qos-multimedia/) 补足名额，超过 `5` 天后若找到可用公开版本再重试 |
| 2026-03-31 | `philaudio.ta` / `bopdp.xml` / `rvs10.zip` 等历史工件链接 | 官网 benchmark/case-study 页仍提到历史模型入口，但当前公开直链已失效或返回 `404` | 在公开性清单中统一按 `🟠 信息不清` 处理，不误记为“模型可直接获取” |
