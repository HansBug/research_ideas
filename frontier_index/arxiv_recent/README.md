# `arxiv_recent/` README

## 1. 路径定位

`arxiv_recent/` 用于存放近期 `arXiv` 软件工程方向论文的滚动索引。

当前默认主入口是：

- <https://arxiv.org/list/cs.SE/recent>

## 2. 推荐组织方式

后续默认按时间窗口组织，例如：

```text
arxiv_recent/
├── 2026-04.md
├── 2026-05.md
└── 2026-06.md
```

如果后续量级明显增大，再考虑按周拆分。

## 3. 每个时间窗口文件建议内容

每个文件默认建议包含：

1. 时间窗口说明
2. 原始候选论文元数据表
3. 初筛结果
4. 值得进一步获取 `PDF` 的候选名单

表头可直接复用 [templates/metadata_index_template.md](../templates/metadata_index_template.md)。

## 4. 维护原则

1. 优先记录 `arXiv abstract` 页，而不是裸 `PDF`。
2. 对 `LLM for SE`、需求工程、验证、修复、测试、程序分析等方向可适当提高关注度。
3. `arXiv` 结果默认更依赖摘要做初筛，因为 venue 信号本身较弱。
