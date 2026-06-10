# 资源与复现实验资产 / ASSETS

更新时间：2026-06-10 13:08:00

状态口径：🟢 可直接访问；🟡 部分公开 / 可重建但不完整；🟠 未公开 / 仅论文内描述；🔒 受限私有资产 / 难以公开获取；❓ 入口存在但当前访问异常或未完成逐文件核验。

CCF 口径：🏆 CCF A；🥈 CCF B；🥉 CCF C；⚪ 非 CCF 推荐或不适用；❓ 未核验。

## 1. 资源总览

| 资源类型 | 状态 | URL / 路径 | 说明 |
|---|---|---|---|
| 论文 | 🟢 | [arXiv](https://arxiv.org/abs/2603.29140) / [本地 PDF](./paper.pdf) | 公开预印本；本地已提取 `paper_content.txt`。 |
| 实验代码 | 🟢 | [Paul3246/nl2fsm](https://github.com/Paul3246/nl2fsm) | GitHub README 明确说明该仓库包含本论文 Python 代码；default branch `main`，HEAD `354f9aacf51b5121abb8a2e04718232185e71928`；含 `v1` 到 `v5`、`err_lim` 与 `Fault_model_approach.zip`。论文正文未给出该仓库，引用时应说明这是本轮额外核到的作者/项目仓库入口。 |
| 实验结果细则 | 🟡 | [v1/benchmark_score.txt](https://github.com/Paul3246/nl2fsm/blob/main/v1/benchmark_score.txt)、[v5/scores1.txt](https://github.com/Paul3246/nl2fsm/blob/main/v5/scores1.txt)、[v5/repertoire-sortie](https://github.com/Paul3246/nl2fsm/tree/main/v5/repertoire-sortie) | 仓库保留部分 benchmark 文本、修复统计和 Graphviz 输出；不是整理好的论文结果复现包，结果与论文表格仍需人工对齐。 |
| 数据集 / Benchmark | 🟡 | [v5/data](https://github.com/Paul3246/nl2fsm/tree/main/v5/data)、[v5/generated_text.csv](https://github.com/Paul3246/nl2fsm/blob/main/v5/generated_text.csv) | 合成 DFSM oracle 与英文描述可由代码生成，仓库含若干示例数据；没有冻结版本、许可证和标准 split。 |
| Artifact / 复现包 | 🟡 | [GitHub repo](https://github.com/Paul3246/nl2fsm) / [Fault_model_approach.zip](https://github.com/Paul3246/nl2fsm/blob/main/Fault_model_approach.zip) | 这是源代码仓 + 部分结果 / 样例数据，不是整理好的 replication package；无 release、license、`requirements.txt` / `pyproject.toml` / `setup.py`，需要自行配置 OpenAI/API 环境、检查依赖、规避仓库中的 `.env` 文件泄露风险并重建实验流程。 |

## 2. Venue 与 CCF

- **论文**：Designing FSMs Specifications from Requirements with GPT 4.0
- **发表 / 版本**：arXiv preprint, 2026, cs.SE
- **CCF 口径**：⚪
- **论文入口**：[arXiv:2603.29140](https://arxiv.org/abs/2603.29140)

## 3. 实验代码核查

仓库根目录含 `v1` 至 `v5` 五个版本、`err_lim` 错误刻画流程和 `Fault_model_approach.zip`。README 将 `v1` 对应语法修复、`v4` 对应 distinguishing-sequence 方法、`v5` 对应 checking-sequence 方法；每个版本的主入口为 `pipeline.py`。本轮核验到 default branch `main`，HEAD `354f9aacf51b5121abb8a2e04718232185e71928`；仓库无 license、release 和依赖锁文件。

## 4. 数据集 / Benchmark 核查

数据不是人工收集的工业需求，而是随机生成 DFSM oracle 后转写成英文需求描述。仓库中 `data/exemple*`、`generated_text.csv` 和 Graphviz 输出可以帮助重建小规模实验，但没有论文级冻结 benchmark 包。

## 5. 实验结果细则核查

可用的细则主要是仓库内 `benchmark_score.txt`、`correction_benchmark_score.txt`、`scores*.txt` 和 `repertoire-sortie` 图文件；论文中 5/10/25 状态实验表仍是主要结果来源。

## 6. 对 Project 1 对比实验的可用性

适合复现 `NL DFSM 描述 -> CSV DFSM -> oracle 比较 / 修复` 这条链路，用于测试 pyfcstm 生成后诊断和修复反馈设计。局限是数据合成、无真实控制系统需求、无层次/并发/时间状态机。

## 7. 风险与待复查

1. 仓库没有 release、license 或依赖锁；需要单独记录复现实验环境，并优先固定 HEAD `354f9aacf51b5121abb8a2e04718232185e71928` 或后续 release。
2. 论文正文未给 GitHub 链接，正式引用时应同时给 arXiv 与仓库 README 证据。
3. 实验可能调用真实 OpenAI API；后续复现必须按仓库 LLM 调用规范记录模型 ID、日期和 usage。
