# Reproduction Workspace

本目录是 `project_1_llm_state_machine_modeling` 的可运行复现工作区，负责统一管理：

1. baseline 复现代码
2. 复现实验数据准备
3. 统一结果落盘
4. `expert_review` 专家评审模块
5. 人类可读的复现说明与版本化设计文档

如果你是第一次进入本目录，建议阅读顺序如下：

1. 先读 [GUIDE.md](./GUIDE.md)
2. 再看 [run_all.py](./run_all.py) 与 [REPRODUCTION_REPORT.md](./REPRODUCTION_REPORT.md)
3. 若要看专家评审模块，再进入 [expert_review/README.md](./expert_review/README.md)

## 主要入口

统一 CLI 入口是 [run_all.py](./run_all.py)。

典型运行流程：

```bash
venv/bin/pip install -r project_1_llm_state_machine_modeling/reproduction/requirements-reprod.txt

venv/bin/python project_1_llm_state_machine_modeling/reproduction/run_all.py download-raw
venv/bin/python project_1_llm_state_machine_modeling/reproduction/run_all.py augment-parquets

venv/bin/python project_1_llm_state_machine_modeling/reproduction/run_all.py run --baseline llms_emp
venv/bin/python project_1_llm_state_machine_modeling/reproduction/run_all.py run --baseline ttool
venv/bin/python project_1_llm_state_machine_modeling/reproduction/run_all.py run --baseline nimbus
venv/bin/python project_1_llm_state_machine_modeling/reproduction/run_all.py run --baseline structure_event

venv/bin/python project_1_llm_state_machine_modeling/reproduction/run_all.py report
```

## 目录结构

- [README.md](./README.md)：本层总入口说明。
- [GUIDE.md](./GUIDE.md)：本层维护与导航规范。
- [REPRODUCTION_REPORT.md](./REPRODUCTION_REPORT.md)：当前复现实验汇总报告。
- [baselines/README.md](./baselines/README.md)：各 baseline 实现入口说明。
- [data/README.md](./data/README.md)：数据目录说明。
- [results/README.md](./results/README.md)：结果目录说明。
- [expert_review/README.md](./expert_review/README.md)：专家评审模块说明。

## 代码入口

- [run_all.py](./run_all.py)：复现总调度 CLI。
- [tasks.py](./tasks.py)：下载、增强、报告生成。
- [llm_client.py](./llm_client.py)：统一 LLM provider 访问与缓存。
- [run_expert_review.py](./run_expert_review.py)：批量专家评审入口。
- [align_ttool_expert_review.py](./align_ttool_expert_review.py)：TTool-AI 人类评分对齐实验入口。
- [expert_review/batch.py](./expert_review/batch.py)：`expert_review` 内部 batch screening 入口。

## 主要子目录

- [baselines/](./baselines/)：四类 baseline 的复现实现。
- [data/](./data/)：原始与派生数据资产。
- [results/](./results/)：各 baseline 与评审产物输出。
- [expert_review/](./expert_review/)：专家评审 agent 模块与设计文档。

## Expert Review 文档入口

`expert_review` 相关文档不再散落在 `reproduction/` 根目录，而是统一收口到模块内：

- 模块说明见 [expert_review/README.md](./expert_review/README.md)
- 设计索引见 [expert_review/designs/README.md](./expert_review/designs/README.md)
- `v0` 基线资料见 [expert_review/designs/v0/README.md](./expert_review/designs/v0/README.md)
- `v1` 重构设计见 [expert_review/designs/v1/README.md](./expert_review/designs/v1/README.md)

## 运行产物

- 数据资产说明见 [data/README.md](./data/README.md)
- 结果产物说明见 [results/README.md](./results/README.md)
- 当前复现实验汇总见 [REPRODUCTION_REPORT.md](./REPRODUCTION_REPORT.md)
