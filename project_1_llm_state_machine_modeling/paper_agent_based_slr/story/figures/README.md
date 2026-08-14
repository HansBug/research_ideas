# figures/：S0 方法图维护说明

本目录维护第二篇论文主线文档中使用的方法图资源。当前只有一张普通流程图：

| 文件 | 用途 | 源稿口径 |
|---|---|---|
| [s0_method_flow.svg](./s0_method_flow.svg) | [../paper_story.md](../paper_story.md) §8.1 中的 S0-v2 方法普通流程图，用于展示阶段、参与者、制品、反馈门控和过程证据边界。 | **手写 / 直接维护的可控 SVG**；该 SVG 文件本身就是当前源稿与渲染资产，不是 Mermaid、drawio 或脚本生成结果。 |

## 1. 为什么普通流程图不用 Mermaid

本图曾尝试使用 Mermaid 普通流程图表达，但自动布局容易出现倒序、过扁、过高、长宽比不稳定或大面积空白，难以满足论文方法总览图的视觉阅读要求。因此当前普通流程图改为可控 SVG：节点位置、连线、颜色、图例和说明文字都在 [s0_method_flow.svg](./s0_method_flow.svg) 内直接维护。

[../paper_story.md](../paper_story.md) 中的时序 / 泳道图仍使用 Mermaid 代码块维护；那张 Mermaid 图用于说明门控责任边界，不是 [s0_method_flow.svg](./s0_method_flow.svg) 的源稿。

## 2. 后续修改规则

修改 [s0_method_flow.svg](./s0_method_flow.svg) 时，默认遵守以下规则：

1. **把 SVG 当作源稿修改**：直接编辑 SVG 中的 `<rect>`、`<text>`、`<path>`、样式和图例；不要假设存在额外 Mermaid 源码。
2. **同步图文一致性**：若阶段、门控、参与者或证据边界发生变化，必须同步检查 [../paper_story.md](../paper_story.md) §8、[../protocol.md](../protocol.md) 和 [../terminology_policy.md](../terminology_policy.md)。
3. **保留核心锚点**：图中至少应能读出 L0--L7、G0--G6、G2 模式演化反馈、G4 研究者质疑反馈、G6 过程证据边界，以及“过程证据不能支撑领域发现”的边界。
4. **真实渲染后验收**：修改后必须把 SVG 渲染为 PNG 做视觉检查，确认长宽比正常、文字可读、无大面积空白、图文含义不歧义。
5. **不要把自动生成产物伪装成源稿**：如果后续改用 drawio、Python 或其他脚本生成 SVG，应把对应源文件和生成命令一并提交，并更新本 README。

## 3. 推荐验收命令

```bash
rsvg-convert -f png \
  project_1_llm_state_machine_modeling/paper_agent_based_slr/story/figures/s0_method_flow.svg \
  -o /tmp/pr114_s0_method_flow.png
file /tmp/pr114_s0_method_flow.png
```

验收重点不是只看命令成功，而是人工打开 `/tmp/pr114_s0_method_flow.png` 检查：

- 阶段顺序是否符合 [../paper_story.md](../paper_story.md) 的 L0--L7 叙事；
- G2 / G4 反馈是否不会被误解为普通顺序阶段；
- G6 是否被理解为横切过程证据边界，而不是领域发现证据；
- 图的比例、留白和文字密度是否适合论文方法总览图。
