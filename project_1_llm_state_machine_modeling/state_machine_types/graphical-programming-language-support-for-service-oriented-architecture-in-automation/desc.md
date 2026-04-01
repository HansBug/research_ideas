# 面向自动化中面向服务体系结构的图形化编程语言支持 / Graphical Programming Language Support for Service Oriented Architecture in Automation

## 基本信息

- 标题：Graphical Programming Language Support for Service Oriented Architecture in Automation
- 中文标题：面向自动化中面向服务体系结构的图形化编程语言支持
- 作者：Alfred Theorin, Charlotta Johnsson
- 发表：Reglermöte 2012, Uppsala, Sweden, 2012
- DOI：原文未提供
- 链接：https://portal.research.lu.se/en/publications/graphical-programming-language-support-for-service-oriented-arch
- 形式主义：Grafchart / JGrafchart with `DPWS`
- 主类：📦
- 描述客体：🤝
- 所属领域：🏭
- 论文角色：工具扩展 / 服务编排载体
- 工具/实现获取方式：原文明确给出 `JGrafchart` 作为 Grafchart 的 Java 实现，并描述了内置 `DPWS Object`、设备发现和事件订阅支持。
- 标准/格式获取方式：承载方式是 `Grafchart` 图形模型、`DPWS` 设备/服务/port type/operation 结构和 `WSDL` 自描述信息。

## 简报

这篇论文的重点不是重新讲 `Grafchart` 本体，而是回答一个很工程的问题：如果工厂现场设备开始以 `DPWS` 服务的形式出现，状态机语言怎样才能以“像写本地动作一样”的方式去发现、绑定和调用这些服务。作者给 `JGrafchart` 增加了 `DPWS Object`，让服务调用、事件订阅和设备重连都能直接进入动作与条件。

- 形式主义定位：面向 service-oriented automation 的图形状态机执行载体。
- 构造方式简述：保留 `Grafchart` 的 steps/transitions/actions，再把 `DPWS` device、port type 和 operation 绑定为 `JGrafchart` 中的 I/O 对象。
- 基础设施与场景简述：依托 `JGrafchart`、`DPWS` 发现机制和 `WSDL` 自描述，服务 shop-floor integration 与设备级协调控制。

```text
自动化协调需求 -> Grafchart steps / transitions / actions -> DPWS Object + WSDL-bound services -> service-oriented process coordination
```

## 形式主义定义与核心对象

### 定义对象

论文中的核心客体不是普通本地 I/O，而是“可发现、可自描述、可重新绑定的服务设备”。状态机仍然是 `Grafchart`，但它操作的对象从静态设备变量扩展成了 `DPWS` 服务接口。

### 核心抽象

结合原文中的 `Grafchart` 骨架和 `DPWS Object` 机制，可保守整理为：

$$
G_{soa} = (S, T, A, O, B, E)
$$

上式中的符号逐项解释如下：

1. `S` 是 Grafchart 中的 steps 集合。
2. `T` 是 transitions 集合。
3. `A` 是 actions 与 conditions 集合。
4. `O` 是 `DPWS Object` 集合。
5. `B` 是对象到 `port\ type` 的绑定关系。
6. `E` 是事件订阅与通知集合。

延续 `Grafchart` 的基本切换语义，可写成：

$$
\mathrm{enabled}(t) \iff \bigwedge_{s \in pre(t)} active(s) \land cond_t
$$

$$
\mathrm{fire}(t) \Rightarrow deactivate(pre(t)) \land activate(post(t))
$$

上式中的符号逐项解释如下：

1. `pre(t)` 是转移 `t` 的前驱 step 集合。
2. `active(s)` 表示 step `s` 当前激活。
3. `cond_t` 是 guard 条件，可包含服务调用结果或事件状态。
4. `post(t)` 是后继 step 集合。

服务绑定关系可以保守写成：

$$
B(o) = p
$$

其中：

1. `o` 是某个 `DPWS Object`。
2. `p` 是它当前绑定的 `port\ type`。
3. 原文强调由于设备有唯一标识，绑定在重启或重新打开应用后可自动恢复。

### 一个最小例子与通俗解释

论文给了一个非常直接的例子：

1. 在 `JGrafchart` 中发现一个 `DPWS` 设备。
2. 其中某个 `port type` 提供 `oneWayOp`、`reqRespOp` 和 `eventOp`。
3. 用户添加一个名为 `myDPWSObj` 的 `DPWS Object` 并绑定到该 `port type`。
4. 然后就可以在状态机动作里写：

```text
myDPWSObj.oneWayOp()
ret = myDPWSObj.reqRespOp("par")
dpwsSubscribe(myDPWSObj, "PT10M")
e = dpwsHasEvent(myDPWSObj, "eventOp")
```

通俗地说，这相当于把“网络上的服务设备”伪装成“状态机里可直接调用的对象”，从而让服务编排逻辑仍然保持图形状态机风格。

### 运行 / 接受 / 转移语义

运行语义保留了 `Grafchart/JGrafchart` 的 step-transition 骨架，但 I/O 读写被替换为服务交互：

$$
call(o, op, args) \mapsto ret
$$

$$
subscribe(o, ev, \tau) \mapsto queue(ev)
$$

上式中的符号逐项解释如下：

1. `o` 是 `DPWS Object`。
2. `op` 是 one-way 或 request-response operation。
3. `args` 是调用参数。
4. `ret` 是返回值。
5. `ev` 是 notification 类型事件。
6. `\tau` 是订阅时长，例如 `PT10M`。

### 语义边界

这个扩展的边界也很清楚：

1. 它解决的是服务发现与调用如何进入状态机，不是重新定义状态机理论。
2. 它强依赖 `DPWS/WSDL` 风格的设备语义。
3. 原文明确指出 `solicit-response` 暂不支持。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 扩展骨架 | `$G_{soa} = (S, T, A, O, B, E)$` | 在 Grafchart 骨架上加入服务对象、绑定和事件。 |
| 基本切换 | `$\mathrm{enabled}(t) \iff \bigwedge_{s \in pre(t)} active(s) \land cond_t$` | 服务调用结果或事件状态可进入 guard。 |
| 绑定关系 | `$B(o)=p$` | `DPWS Object` 与 `port type` 绑定，并可自动重绑。 |
| 服务调用 | `$call(o, op, args) \mapsto ret$` | 状态机动作可像方法调用一样操作服务。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 底层仍是 Grafchart 的 step/transition 控制流。 |
| 事件 / 触发 | 强支持 | `DPWS` notification 可转成状态机条件。 |
| 守卫 / 数据 | 强支持 | 请求返回值、事件缓存和对象状态都可进入条件判断。 |
| 层次 | 部分支持 | 继承 `Grafchart/JGrafchart` 的层次结构。 |
| 并发 / 同步 | 部分支持 | 主要依赖 Grafchart 并行路径和服务事件，不是复杂同步协议理论。 |
| 时间约束 | 部分支持 | 论文涉及订阅时长和设备上线/下线，但不是显式时钟形式主义。 |
| 连续动态 / 随机性 | 不支持 | 聚焦服务化自动化协调。 |
| 可执行 / 可验证性 | 强支持 | 直接进入 `JGrafchart` 运行时并连接真实 `DPWS` 设备。 |

### 形式化问题与性质

1. `DPWS` 设备是 discoverable 和 self-describing 的，因此状态机可以做近似 plug-and-play 绑定。
2. `request-response` 与 `notification` 被映射成与本地方法调用相似的用法，降低了图形状态机接入 SOA 的门槛。
3. `DPWS Object` 名称可直接在 actions/conditions 中使用，使服务接口真正成为控制逻辑的一部分。

## 构造方式与承载格式

### 建模入口

建模入口包括：

1. 普通 `Grafchart` steps/transitions/actions。
2. `JGrafchart` 的 `DPWS Object` I/O 元素。
3. 设备发现对话框、port type 绑定和事件订阅。

### 机器可处理承载方式

机器可处理承载由两部分组成：

1. `JGrafchart` 应用模型。
2. `DPWS` 设备的 `WSDL` 描述、services、port types 和 operations。

### 交换与互操作

互操作关键不在自定义状态机格式，而在 `DPWS/WSDL` 所提供的设备发现、自描述和服务签名。状态机只是把这些接口变成自己的动作/条件。

## 配套基础设施

- 建模/编辑工具：`JGrafchart`。
- 解析/交换/元模型支持：依赖 `DPWS` discovery 和 `WSDL` 自描述；原文未展开更底层实现细节。
- 仿真/执行支持：可直接对接现实 demonstrator process。
- 验证/分析支持：论文重心在执行与集成，不在独立验证器。
- 代码生成/转换支持：原文未说明额外代码生成标准。
- 标准化或社区生态：依托 `DPWS` 和 service-oriented automation 研究线。

## 适用场景与需求前提

### 适用场景

适合车间设备通过服务暴露能力、需要图形化协调逻辑和希望快速试验 `SOA` 自动化集成的场景。

### 需求前提

1. 设备或子系统能以 `DPWS` 服务形式暴露。
2. 协调逻辑本质上仍是离散步骤和事件触发。
3. 希望服务发现、绑定和事件处理进入状态机而不是外部脚本。
4. 现场愿意接受 web-service 风格的设备交互。

### 不适用或高成本场景

如果设备接口完全不服务化、强调硬实时局部总线 IO、或需要复杂协议协商语义，这个扩展不是首选。

## 与相邻形式主义的关系

相对普通 `Grafchart/JGrafchart`，它把静态 I/O 接口提升成可发现服务；相对纯 SOA 编排语言，它保留了更贴近自动化工程师的图形状态机控制流；相对传统 PLC 顺控，它更强调设备自描述和动态绑定。

## 与本研究的关系

### 对 Project 1 的价值

它说明“状态机选型”不仅看语义，还要看最终工件能不能挂接到现场基础设施。服务化自动化场景下，状态机需要原生理解设备发现和服务调用。

### 作为目标形式主义还是中间表示

在服务化工厂或设备编排场景中，它可以直接作为目标载体；在一般研究中，它也可作为从抽象状态机到服务控制应用的后端。

### 对需求到模型生成的启发

如果需求中反复出现“设备提供某服务”“调用某操作”“订阅某事件”，那么生成纯平面状态机不够，最好同时生成服务对象和调用骨架。

### 现实限制

它依赖 `DPWS` 生态，而且只覆盖部分 `WSDL` 操作类型；跨更广泛工业协议的普适性有限。

## 重要的相关工作

### 奠基或前身工作

- `Grafchart`
- `JGrafchart`
- `DPWS`

### 同类型或同家族工作

- service-oriented process control with Grafchart
- 面向自动化的 SOA 中间件与设备通信工作

### 标准 / 格式 / 工具链工作

- `WSDL`
- `DPWS`
- `JGrafchart`

### 与本研究关系最紧的工作

- 它展示了状态机如何贴着自动化基础设施演化，而不是停留在抽象控制图。

## 文献分类总结

- 主类：📦
- 描述客体：🤝
- 所属领域：🏭
- 形式主义：Grafchart / JGrafchart with `DPWS`
- 论文角色：工具扩展 / 服务编排载体
- 核心功能：把可发现的服务设备无缝嵌入图形状态机控制逻辑。
- 关键特性：`DPWS Object`、自动重绑、事件订阅、方法式服务调用。
- 构造方式：`JGrafchart` 图形模型 + `DPWS/WSDL` 设备语义。
