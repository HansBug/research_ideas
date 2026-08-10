# Multi-Location Software Model Completion — repair baseline 记录

## 1. 基本信息

| 字段 | 内容 |
|---|---|
| baseline_id | `multi-location-software-model-completion` |
| 标题 | Multi-Location Software Model Completion |
| 年份 / venue | 2026 / ICSE 2026 / arXiv |
| 当前角色 | multi-location model completion 近邻 |
| 阅读来源 | 本地 `paper_content.txt` 全文阅读 + 摘要/方法/实验/资源段落核验 |

## 2. 任务、输入与输出

| 维度 | 内容 |
|---|---|
| NL / 输入 | 模型元素名/文本属性中的 lexical 信息；不是 requirements NL |
| 模型 / STM 输入 | general software models / RepairVision model histories；不限定 STM，含 event-action trigger concept 作为案例线索 |
| 修正输入 | existing local model edit / anchor focus + historical model evolution data |
| 修正输出 | predicted additional focus nodes / multi-location model completion suggestions；可与 RAMC 组合 |
| 修正 / 补全 / refinement 方法 | NextFocus：global embedding + attention neural next-focus predictor；历史 co-change learning |
| feedback 来源 | 无 verifier feedback；基于历史 co-change supervised evaluation |
| 自动化程度 | 自动推荐；非 repair loop |
| LLM / agent 角色 | NextFocus 本体非 LLM；与 RAMC 组合时使用 LLM model completion |

## 3. 与本文 source-level issue discovery / repair / closure 任务的关系

不满足本文 baseline：无 NL requirements，也无 STM_0 from NL；但对 multi-location model completion 与资产资源可作近邻。

## 4. 证据位置

paper_content.txt:13-34, 89-136, 562-755, 805-824, 1200-1224, 1356-1358

## 5. 主要风险与使用边界

model completion 范围过宽；输入不是 `NL + STM_0`；不修 formal/semantic diagnostics。
