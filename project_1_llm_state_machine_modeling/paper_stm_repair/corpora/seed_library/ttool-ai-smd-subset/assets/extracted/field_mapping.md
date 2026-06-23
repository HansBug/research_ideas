# field mapping: ttool-ai-smd-subset

| pairs.jsonl field | raw source | 说明 |
|---|---|---|
| `nl_text` | `assets/raw/ttool-ai_<commit>.zip` 中 `*.md` / `specification_*.md` 成员 | 作者公开系统规格 / specification。 |
| `stm0_text` | 同一 ZIP 中对应 `*.xml` 成员 | 作者 README 声称由 TTool + ChatGPT 3.5 生成的 TTool XML 工件；不是完整 TTool-AI 源码。 |
| `source_locator` | `nl_member=...;stm0_member=...` | typed locator，可由 validator 解引用 ZIP 成员。 |
| `eligibility_state` | registry 条件判断 | 标为 `conditional_final_pool`，因为有一手 NL+generated XML，但需 SMD/T0 切片、时间/信号/guard/action 审计。 |

注意：这些 XML 是完整 TTool/SysML/AVATAR 工件，不能不经切片就当成纯 T0 FSM。
