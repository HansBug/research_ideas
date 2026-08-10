# FSM-Bench-20: Local LLM Benchmark for Deterministic FSM Generation

## R1.6 strict seed 核验结论

| 字段 | 结论 |
|---|---|
| bibliographic_id | Zenodo DOI `10.5281/zenodo.20517969`，publication date 2026-06-03 |
| 本地证据 | `zenodo_record.json`、`github_repo.json`、`github_contents_v1.0.0.json`、`llm-fsm-local-benchmark-v1.0.0.zip`、`extracted_sample/`；artifact-only Zenodo/GitHub record，无论文 PDF / `paper_content.txt`。 |
| strict_seed_grade | `SS-A` for literature relation；`conditional-main-pending-output-freeze` for R2 |
| artifact_usability | `SA-2`（带条件备注）：dataset / prompt / schema / code 可冻结，但公开包中 generated STM outputs / gold FSM 不是完整可用；条件性写入 caveat，不扩展 SA 枚举 |
| 是否计入 R1.6 四例下限 | 暂不计入。只有找到作者公开 generated outputs，或 PR-R2 按 tag + prompt + model digest 复跑并冻结 seed instance 后，才可升级。 |

## P1/P2/P3/P4 核验

| 谓词 | 判定 | 证据 |
|---|---|---|
| `P1_NL_INPUT` | 通过 | Zenodo 描述称包含 20 个 natural-language requirement specifications；ZIP `dataset/systems/*.json` 中含英文编号需求。 |
| `P2_T0_STM_FAMILY` | 任务 / schema 通过，实际输出未冻结 | `schema.py` / prompt 定义 deterministic FSM JSON，含 states、initial_state、events、transitions、guard、action、target、requirement；未见关键时间 / hybrid 语义。但公开 release 未包含可直接复用的 generated STM outputs，不能把 schema 通过误读为已有 `STM_0` seed。 |
| `P3_GENERATION_RELATION` | 通过 | `experimental_prompts.md` 要求将自然语言软件需求转换为 deterministic FSM；README / Zenodo 均以 deterministic FSM generation 为任务。 |
| `P4_EVIDENCE_POINTER` | 部分通过 | DOI、GitHub tag、dataset、prompt、schema、run scripts 已本地冻结；许可 / 再分发不作为升绿阻塞。但 outputs / gold 在公开 ZIP 中不可直接作为已生成 STM seed。 |

## LLM / 方法信息

- 运行方式：本地 Ollama structured JSON output。
- mandatory models：`qwen2.5-coder:7b`、`qwen2.5-coder:14b`、`llama3.1:8b`、`mistral-nemo:12b`、`gemma2:9b`、`phi3:14b`。
- optional model：`qwen2.5-coder:32b`。
- 关键配置：temperature 0.0、context 8192；具体以 ZIP 内 `README.md` / `REPRODUCIBILITY.md` / scripts 为准。

## SS / SA 解释

- `SS-A`：任务关系本身非常清楚，确实是自然语言需求到确定性 FSM JSON。
- `SA-2`（带条件备注）：Zenodo v1.0.0、GitHub tag、dataset、prompt、schema、脚本均可冻结，适合 PR-R2 做复跑型 seed；许可 / 再分发不作为升绿阻塞。但公开 release 中 `benchmark/gold/*.json` 是空 placeholder，`outputs/` / `results/` 不在 ZIP 内，不能把 headline 140-run campaign 直接当作可用 STM seed。

## R2 使用建议

1. 优先作为 **reproducible-pipeline seed candidate**，而不是已冻结 generated-output seed。
2. 若 R2 需要补足四例，建议先选 1--2 个系统，记录 ZIP hash、prompt hash、模型 digest、Ollama 版本、raw output、cleaned output、schema validation 与 eligibility，再决定是否升级。
3. 不能把 gold placeholder 或 headline G1/G2/G3 指标冒充为可直接使用的 `STM_0`。

## 风险

- DOI/version mismatch：README / CITATION 可能仍指向 `10.5281/zenodo.20516296`（v0.3.0），本 PR 使用用户给定并已核验的 v1.0.0 DOI `10.5281/zenodo.20517969`。
- 领域偏软件业务系统，不一定是控制系统。
- 需要本地复跑才会产生实际 generated FSM outputs；本 PR 不跑真实例子、不调用模型。
