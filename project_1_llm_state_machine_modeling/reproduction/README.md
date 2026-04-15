# Reproduction Workspace

This directory contains a runnable reproduction workspace for the four recently prioritized `project_1` baselines:

1. `llms_emp`
2. `ttool-ai`
3. `Requirements Capture and Evaluation in Nimbus: The Light-Control Case Study`
4. `Structure- and Event-Driven Frameworks for State Machine Modeling with Large Language Models`

The workspace is organized around four goals:

1. Download raw artifacts into local storage.
2. Repair or enrich baseline `parquet` assets when the current discussion copy is incomplete.
3. Run reproducible LLM-based baselines with the local Codex API configuration, preferring `airouter -> findcg -> miaocg`.
4. Write machine-readable result `parquet` files and a human-readable reproduction report.

## Main Entry

Use [run_all.py](./run_all.py).

Typical flow:

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

## Outputs

- Raw downloads: [data/raw](/home/zhangshaoang/oo-projects/research_ideas-2/project_1_llm_state_machine_modeling/reproduction/data/raw)
- Derived `parquet`: [data/derived](/home/zhangshaoang/oo-projects/research_ideas-2/project_1_llm_state_machine_modeling/reproduction/data/derived)
- Runtime results: [results](/home/zhangshaoang/oo-projects/research_ideas-2/project_1_llm_state_machine_modeling/reproduction/results)
- Final report: [REPRODUCTION_REPORT.md](/home/zhangshaoang/oo-projects/research_ideas-2/project_1_llm_state_machine_modeling/reproduction/REPRODUCTION_REPORT.md)

## Code Layout

- [run_all.py](/home/zhangshaoang/oo-projects/research_ideas-2/project_1_llm_state_machine_modeling/reproduction/run_all.py): CLI entry.
- [tasks.py](/home/zhangshaoang/oo-projects/research_ideas-2/project_1_llm_state_machine_modeling/reproduction/tasks.py): raw download, parquet augmentation, report generation.
- [llm_client.py](/home/zhangshaoang/oo-projects/research_ideas-2/project_1_llm_state_machine_modeling/reproduction/llm_client.py): official `openai` client wrapper with provider fallback and disk cache.
- [baseline_llms_emp.py](/home/zhangshaoang/oo-projects/research_ideas-2/project_1_llm_state_machine_modeling/reproduction/baseline_llms_emp.py): `llms_emp` reproduction.
- [baseline_ttool.py](/home/zhangshaoang/oo-projects/research_ideas-2/project_1_llm_state_machine_modeling/reproduction/baseline_ttool.py): `ttool-ai` plus local `sm/MTI` reproduction.
- [baseline_nimbus.py](/home/zhangshaoang/oo-projects/research_ideas-2/project_1_llm_state_machine_modeling/reproduction/baseline_nimbus.py): `Nimbus` fragment reproduction.
- [baseline_structure_event.py](/home/zhangshaoang/oo-projects/research_ideas-2/project_1_llm_state_machine_modeling/reproduction/baseline_structure_event.py): `Structure/Event-Driven` reproduction.

## Notes

- API keys are loaded from the current environment first and then from local `~/.codex/*.env` files when available.
- The workspace does not persist secrets into tracked files.
- Default provider order is `airouter -> findcg -> miaocg`.
- `api68886868` is intentionally excluded from the default automatic retry chain because it is less stable in this environment.
- LLM access uses the official `openai` Python client; prompt assembly uses `langchain_core.prompts.ChatPromptTemplate`.
- The client currently falls back across non-stream `responses` and `chat.completions`, then switches provider if needed.
