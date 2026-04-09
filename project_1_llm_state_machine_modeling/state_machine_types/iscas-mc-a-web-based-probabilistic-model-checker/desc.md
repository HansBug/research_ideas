# ISCAS MC：面向 Markov 链与 MDP 的 Web 概率模型检查器 / ISCAS MC: A Web-Based Probabilistic Model Checker

## 基本信息

- 标题：iscasMc: A Web-Based Probabilistic Model Checker
- 中文标题：ISCAS MC：面向 Markov 链与 MDP 的 Web 概率模型检查器
- 作者：Ernst Moritz Hahn，Yi Li，Sven Schewe，Andrea Turrini，Lijun Zhang
- 发表：*FM 2014: Formal Methods*，pp. 312-317，2014
- DOI：`10.1007/978-3-319-06410-9_22`
- 链接：https://doi.org/10.1007/978-3-319-06410-9_22
- 形式主义：`Markov Chains / MDP / PCTL* / ISCAS MC`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：💻 软件建模与程序行为
- 论文角色：Web 化概率模型检查平台与 `PCTL*` 线性时序求解基础设施
- 工具/实现获取方式：原文明确给出 `http://iscasmc.ios.ac.cn/IscasMC` 作为 Web 入口，并说明客户端是 HTML/JavaScript，后端是 Java 服务与工作线程。
- 标准/格式获取方式：输入承载是 `PRISM` 输入语言；性质承载是 `PCTL/PCTL*` 与基于 pattern formulas 的 `PLTL/LTL` 线性时序规格。

## 简报

这篇论文的价值，不在于新建一门概率状态机语言，而在于把概率模型检查做成“拿浏览器就能用”的网络服务。`ISCAS MC` 把 `PRISM` 风格模型、`PCTL*` 性质、`SPOT` 自动机构造、工作队列和结果回传整合成一个可远程访问的平台，特别强调对线性时序性质的高效处理。

- 形式主义定位：概率模型检查平台与 Web 基础设施，不是新的模型族。
- 构造方式简述：用户在前端提交 `PRISM` 模型与性质，后端解析模型、用 `SPOT` 处理线性子公式、构造积模型，再做 probabilistic reachability 求解。
- 基础设施与场景简述：依托 HTML/JS 前端、Java backend、MySQL、`SPOT` 与 value iteration，引导 `Markov chain / MDP + PCTL*` 的远程模型检查。

```text
PRISM model + PCTL* / pattern formulas -> parser + options -> automaton construction by SPOT -> product MDP -> reachability solving -> web result / logs
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. Markov chains。
2. Markov decision processes (`MDP`)。
3. `PCTL` 与 `PCTL*` 性质。
4. generalized Buchi / Rabin automata。
5. Web 前端、后台任务队列与模型检查引擎。

### 核心抽象

按论文支持范围，可把模型族写成：

$$
\mathcal{M} = \{\mathrm{MC}, \mathrm{MDP}\}
$$

上式中的符号逐项解释如下：

1. `MC` 表示 Markov chains。
2. `MDP` 表示 Markov decision processes。
3. 2014 版工具主要围绕这两类模型。

性质侧可以保守整理为：

$$
\Phi = \{\mathrm{PCTL}, \mathrm{PCTL}^*, \mathrm{PLTL\ patterns}\}
$$

上式中的符号逐项解释如下：

1. `PCTL` 是概率计算树逻辑。
2. `PCTL^*` 是更强的概率时序逻辑。
3. `PLTL patterns` 指论文专门支持的 absence / response 等线性时序模板公式。

论文的求解主线可压成：

$$
\mathcal{P} = \mathcal{M} \otimes \mathcal{A}_{\varphi}
$$

上式中的符号逐项解释如下：

1. `\mathcal{M}` 是输入的 `MC/MDP`。
2. `\varphi` 是给定的 `PCTL^*` 规格中的线性时序部分。
3. `\mathcal{A}_{\varphi}` 是由 `SPOT` 等工具生成的广义 `Buchi` 或进一步确定化后的自动机。
4. `\mathcal{P}` 是模型与性质自动机的积模型。

在积模型上，论文把问题进一步规约为可达性：

$$
\mathcal{P} \leadsto \mathrm{Reachability}(\mathrm{Accept})
$$

上式中的符号逐项解释如下：

1. `\mathcal{P}` 是前面的积模型。
2. `\mathrm{Accept}` 是根据接受条件识别出的接受状态集合。
3. 工具最终对这些接受状态做概率可达性求解。

### 一个最小例子与通俗解释

论文给的 benchmark 例子是 quasi birth-death process，但它真正想说明的是工作流而不是该模型细节本身。一个最小直觉例子可以理解为：

1. 先写一个 `MDP`，其中既有概率跳转，也有非确定性选择。
2. 再写一个线性性质，比如“某类请求之后最终会收到应答”。
3. `ISCAS MC` 用 `SPOT` 把线性部分编成自动机。
4. 最后把自动机和原模型做积，再把问题变成接受状态的概率可达性。

通俗地说，它像一个“网页版的概率时序属性编译器 + 模型检查服务”。用户不必在本地装整套复杂环境，只要提交模型与性质，后台就完成自动机构造、积模型和求解。

### 运行 / 接受 / 转移语义

论文的语义重点不在重新定义 `MC/MDP` 的转移规则，而在模型检查链路：

1. 对复杂 `LTL` 子公式，先由 `SPOT` 生成 generalized `Buchi` automaton。
2. 如果自动机不确定，就采用分层的 subset / breakpoint / Rabin 构造与细化。
3. 再把自动机与原模型组成积模型。
4. 最终回到概率 reachability 上，用 Jacobi 或 Gauss-Seidel 风格的 value iteration 求解。

### 语义边界

边界同样明确：

1. 2014 版工具只支持 `MC` 和 `MDP`，还不包括更广的 stochastic-game / reward families。
2. 输入主要是 `PRISM` 语言。
3. 平台重点是 `PCTL*` 与线性时序性质，不是多目标或参数化概率分析。
4. 论文展示的是 Web 平台与求解链路，不是统一交换标准。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 支持模型族 | `$\mathcal{M} = \{\mathrm{MC}, \mathrm{MDP}\}$` | 2014 版工具的核心对象。 |
| 支持规格族 | `$\Phi = \{\mathrm{PCTL}, \mathrm{PCTL}^*, \mathrm{PLTL\ patterns}\}$` | 同时支持分支与线性概率性质。 |
| 积模型 | `$\mathcal{P} = \mathcal{M} \otimes \mathcal{A}_{\varphi}$` | 线性部分先自动机构造，再与模型同步。 |
| 求解规约 | `$\mathcal{P} \leadsto \mathrm{Reachability}(\mathrm{Accept})$` | 最终仍回到概率 reachability 问题。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 围绕 `MC/MDP` 做模型检查。 |
| 事件 / 触发 | 中等支持 | 依赖 `PRISM` 模型中的动作与标签。 |
| 守卫 / 数据 | 中等支持 | 输入承载来自 `PRISM`，不是新建 DSL。 |
| 层次 | 不支持 | 主体不是层次状态机或递归模型。 |
| 并发 / 同步 | 中等支持 | 通过 `PRISM` 输入模型承载。 |
| 时间约束 | 不支持 | 不走 timed family。 |
| 连续动态 / 随机性 | 随机性很强，连续动态不支持 | 主体是概率状态模型。 |
| 可执行 / 可验证性 | 很强 | 直接面向可用的 Web 模型检查服务。 |

### 形式化问题与性质

1. 工具最突出的地方是把 `PCTL*` 的复杂线性子式处理封装进一个可直接用的 Web 平台。
2. 相比单机命令行工具，它把前端编辑、任务队列、结果查看和错误追踪都并入基础设施。
3. 相比纯学术算法论文，它更像一个“在线概率模型检查工作台”。

## 构造方式与承载格式

### 建模入口

典型入口是：

1. 在 Web 前端导入或编写 `PRISM` 模型。
2. 为模型附加 `PCTL*` 或 pattern formulas。
3. 提交成 task。
4. 后端在独立 worker 中完成分析。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `PRISM` 模型文本。
2. `PCTL/PCTL*` 公式文本。
3. `SPOT` 生成的广义 `Buchi` 自动机。
4. 产品 `MDP` 与求解日志。

### 交换与互操作

这篇论文的互操作重点在于：

1. `PRISM` 输入语言直接复用。
2. `SPOT` 被拿来做线性公式自动机构造。
3. 前端与后端共享 parser/options 接口。

## 配套基础设施

- 建模/编辑工具：Web model editor、task center、option center、example center。
- 解析/交换/元模型支持：前后端共享 `PRISM` parser 与 options 接口。
- 仿真/执行支持：不是仿真平台，主线是模型检查服务。
- 验证/分析支持：`PCTL/PCTL*`、线性时序 pattern formulas、value iteration。
- 代码生成/转换支持：主线是性质自动机构造和积模型，不是代码生成。
- 标准化或社区生态：Java engine、HTML/JS frontend、MySQL、`SPOT` 与 `PRISM` 生态共同组成基础设施。

## 适用场景与需求前提

### 适用场景

适合需要快速尝试 `MC/MDP` 概率性质、希望多人通过浏览器共享模型和任务、并关心线性时序性质处理效率的概率验证场景。

### 需求前提

1. 模型能写成 `PRISM` 输入语言。
2. 系统核心是 `MC` 或 `MDP`，而非递归、实时时钟或混成动力学。
3. 关注性质中包含 `PCTL*` 或 `LTL` 风格线性部分。
4. 团队愿意接受服务端计算、任务队列和 Web 工作流。

### 不适用或高成本场景

如果目标是 timed、recursive 或更复杂的 quantitative models，这篇论文里的 `ISCAS MC` 就不是最自然的入口。

## 与相邻形式主义的关系

相对 [a-storm-is-coming-a-modern-probabilistic-model-checker/desc.md](../a-storm-is-coming-a-modern-probabilistic-model-checker/desc.md)，它更专注 `MC/MDP + PCTL*` 的 Web 化检查体验，而不是多引擎多求解器平台；相对 [prism-40-verification-of-probabilistic-real-time-systems/desc.md](../prism-40-verification-of-probabilistic-real-time-systems/desc.md)，它复用了 `PRISM` 输入语言，但没有走概率实时主线；相对 [momba-jani-meets-python/desc.md](../momba-jani-meets-python/desc.md)，它更偏在线服务而不是 Python workflow。

## 与本研究的关系

### 对 Project 1 的价值

它说明一旦后续需要给用户或实验脚本提供“可快速调用的验证后端”，Web 化和任务队列本身也是值得建模的基础设施能力。

### 作为目标形式主义还是中间表示

更像概率验证平台，而不是最终状态机输出格式。

### 对需求到模型生成的启发

1. 如果 LLM 输出最终还要进入概率验证服务，前端格式最好直接兼容现有生态语言。
2. 公式编译、积模型和求解可以被封装在后端，不必暴露给生成器。
3. 平台化部署会改变“模型生成之后如何验证”的工程组织方式。

### 现实限制

它补的是 Web 概率模型检查平台，不解决递归、实时时钟或混成系统的更强表达需求。

## 重要的相关工作

1. [a-storm-is-coming-a-modern-probabilistic-model-checker/desc.md](../a-storm-is-coming-a-modern-probabilistic-model-checker/desc.md)：更现代、更模块化的概率模型检查平台。
2. [prism-40-verification-of-probabilistic-real-time-systems/desc.md](../prism-40-verification-of-probabilistic-real-time-systems/desc.md)：经典 `PRISM` 概率实时平台。
3. [momba-jani-meets-python/desc.md](../momba-jani-meets-python/desc.md)：面向 `JANI` 与 Python workflow 的后续工具链。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：💻 软件建模与程序行为
- 形式主义：`Markov Chains / MDP / PCTL* / ISCAS MC`
- 归类理由：主贡献是 Web 平台、任务队列和 `PCTL*` 检查基础设施，不是新的状态机本体。
