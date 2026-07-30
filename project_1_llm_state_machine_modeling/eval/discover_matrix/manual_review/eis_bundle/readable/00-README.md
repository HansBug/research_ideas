# LLMS-EMP expected issue set — 逐 pair 可读台帐

↩ **正文**：[issue #172](https://github.com/HansBug/research_ideas/issues/172) ｜ ↔ **另一面**：[审计数据 gist](https://gist.github.com/HansBug/e92fb6ca165b46d19b1638f03ae93842)

本 gist 是 **expected issue set** 的逐 pair 可读面：48 个 pair、共 **129** 条 expected issue。审计数据（机读 JSON、覆盖校验、一致性检查）在**另一个 gist**，见对应 issue 正文的入口表。

## 每条记录包含什么

| 字段 | 说明 |
| --- | --- |
| 归因层 | 凭什么把这条归因于生成方。四层：`wellformedness`（模型自身即可判定）/ `nl_named`（NL 点名了该元素）/ `nl_contradiction`（与 NL 显式义务矛盾）/ `over_specification`（凭空多出且有可断言后果） |
| 缺陷方向 | 什么坏了（可达性、初始入口、守卫、层次、动作、事件、伪状态、基数）|
| 触及的元组分量 | 落在 $M = (S, E, V, Tr, A)$ 的哪个分量 |
| 断言组 | 主断言（经复跑）+ 负控 + 佐证。**负控须实测为 `True`**，否则无法排除主断言对正确模型也返回 `False` |
| 上游关联 | 逐对复核主档的 diff 下标、本 pair 的旧台帐 E1、8 格运行已发布 issue、论文两阶段 F1 |

## 必须先知道的三件事

1. **129 条中 115 条可自动验收**（主断言实测返回 `False`），**14 条现有 19 个封闭谓词表述不出**，只能人工验收。后者构成本集合的自动化上限，逐条标注在各 pair 文件里。
2. **没有一条带经实测验证的负控。** 复核者在文本里记录过负控，但无一能被自动复跑验证（从散文恢复的表达式多不可求值）。这是本集合已知的最大证据弱点。
3. **旧台帐（issue #166 的 47 条）无法与本集合做 binding 级合并** —— 其 `ledger.json` 于 2026-07-29 机器重建时丢失、从未进入 git、不可恢复；47 条中仅 5 条被重建出 `eval_assert`。因此本集合是台帐，issue #166 的 47 条降级为需逐条交代的覆盖清单（结果：5 条 `binding_match`、42 条 `same_pair_only`、**0 条 unaccounted**）。

## 判定口径

`correct` / `similar` 不计入问题（语义等价即不计）；`problem` 与 `extra` 走两条不同的判定路径 —— `problem` 判**可归因性**（Q1），`extra` 判**有害性**（Q2），因为前者的有害性由定义蕴含、后者的可归因性由来源唯一而免费。四档判定与两条路径的完整定义见 issue 正文 §0.2；归因层的判据见 §TL;DR 的归因层表。
