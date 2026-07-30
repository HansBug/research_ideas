# LLMS-EMP expected issue set — 逐 pair 可读台帐

↩ **正文**：[issue #172](https://github.com/HansBug/research_ideas/issues/172) ｜ ↔ **另一面**：[审计数据 gist](https://gist.github.com/HansBug/e92fb6ca165b46d19b1638f03ae93842)

本 gist 是 **expected issue set** 的逐 pair 可读面：48 个 pair、共 **126** 条 expected issue。审计数据（机读主档、覆盖校验、谓词复跑、一致性检查）在另一个 gist。

## 每条记录包含什么

| 字段 | 说明 |
| --- | --- |
| 归因层 | 凭什么把这条归因于生成方。四层：`wellformedness`（模型自身 + 良构性/投影语义即可判定）/ `nl_named`（NL 逐字点名该元素）/ `nl_contradiction`（与 NL 显式义务矛盾）/ `over_specification`（凭空多出且有可断言后果）|
| 缺陷方向 | 什么坏了（可达性、初始入口、守卫、层次、动作、事件、伪状态、基数）|
| 触及的元组分量 | 落在 $M = (S, E, V, Tr, A)$ 的哪个分量 |
| 断言组 | 主断言（经复跑）+ 负控 + 佐证。**负控须实测为 `True`**，否则无法排除主断言对正确模型也返回 `False`。超长表达式在表下以可复制的 code block 给出 |
| 上游关联 | 复核主档的 diff 下标、本 pair 的旧台帐 E1、8 格运行已发布 issue、论文两阶段 F1 |

## 必须先知道的四件事

1. **126 条中 112 条可自动验收**（主断言实测返回 `False`），**14 条**只能人工验收（现有 19 个封闭谓词表述不出，或表达式不可求值）。后者构成本集合的自动化上限，逐条标注在各 pair 文件里。
2. **只有 2 条带经实测验证的负控**（覆盖率 2%）。复核者在散文里记录过更多负控，但从散文恢复的表达式绝大多数不可求值。**这是本集合已知的最大证据弱点**——没有负控就无法机械排除「正确模型也返回 `False`」。
3. **旧台帐（issue #166 的 47 条）可做 binding 级交代。** frozen ledger 位于 `.omx/specs/…/ledger.json`（SHA-256 `03d8756650c0…`），其 47/47 条带 `eval_assert`。实测 **38 条 `binding_match`、9 条 `same_pair_only`、0 条 `unaccounted`**。⚠️ 本 gist 的早前版本称该台帐已丢失、仅 5 条可比——那是误判，已更正。
4. **归因门控是最重要的限制。** 按流水线自己的裁决契约，非 `safe` 的 `False` 断言强制进 `excluded_findings`、永不成为 confirmed issue。把本集合当命中率分母时必须同时报告归因分层，否则会把按设计不该上报的条目记成漏检。详见正文 §TL;DR 末的归因门控表。

## 判定口径

`correct` / `similar` 不计入问题（语义等价即不计）；`problem` 与 `extra` 走两条不同路径——`problem` 判**可归因性**，`extra` 判**有害性**，因为前者的有害性由定义蕴含、后者的可归因性由来源唯一而免费。四档判定与两条路径的完整定义见 issue 正文 §0.2。
