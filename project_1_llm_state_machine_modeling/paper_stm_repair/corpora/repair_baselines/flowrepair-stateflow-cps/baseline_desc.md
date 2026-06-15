# FlowRepair — repair baseline 记录

## 1. 基本信息

| 字段 | 内容 |
|---|---|
| baseline_id | `flowrepair-stateflow-cps` |
| 标题 | FlowRepair: Search-based automated program repair of CPS controllers modeled in Simulink-Stateflow |
| 年份 / venue | 2026 / Information and Software Technology；arXiv 2024 |
| 当前角色 | Stateflow / CPS controller repair 强条件 baseline |
| 阅读来源 | 本地 `paper_content.txt` 全文阅读 + 旁路核验材料 |

## 2. 任务、输入与输出

| 维度 | 内容 |
|---|---|
| NL / 输入 | 无自然语言需求输入；输入是待修复 Simulink/Stateflow 模型、SBFL suspiciousness ranking、passing/failing tests、test oracle、时间预算与 local tries 等配置 |
| 模型 / STM 输出 | plausible patches archive 与 partial patches archive；对象是 Simulink/Stateflow CPS controller 的状态、迁移、迁移条件、变量动作等修改后的模型变体 |
| 修正 / 补全 / refinement 方法 | 自动插桩 Stateflow；执行 passing/failing tests；用 SBFL/Tarantula 定位 state/transition suspiciousness；用 global + local search 选择组件并应用 15 类 Stateflow mutation operators；用仿真测试与 repair objectives 维护 plausible / partial patch archives |
| feedback 来源 | SBFL 覆盖轨迹、simulation-based testing verdict、regression oracle、failure active time、failure trigger time、failure severity 等 CPS-specific repair objectives |
| 自动化程度 | fault localization、mutation、仿真评估、plausible/partial archive 维护高度自动；最终 valid patch 仍需人工确认以避免 overfitting |
| LLM / agent 角色 | 无 LLM / agent loop；论文只在 future work 中提到未来可能探索 LLM as mutators |

## 3. 与本文 `<NL, STM_0> -> Better STM` 的关系

FlowRepair 是目前本库中最强的 Stateflow/Simulink repair 近邻之一：它直接修复 statechart-like CPS controller，repair operators 作用于 states、transitions、guard/condition、variable/action 等模型元素，反馈来自测试、仿真、oracle 与 fault localization。若本文后续把目标 STM 映射到 Stateflow/Simulink 且能提供仿真 oracle，它可作为 strong conditional baseline。

但它不是完整同构 baseline：任务输入不含 NL，不处理 `NL` 与 `STM_0` 的需求一致性，不使用 LLM，也不面向文本式 pyfcstm/通用状态机 DSL。更稳妥的写法是将其定位为 “Stateflow/CPS simulation-guided repair 条件 baseline + mutation/feedback/objective 设计参照”，不能声称已有方法已经解决本文的 `<NL, STM_0> -> STM_k` 闭环任务。

## 4. 证据位置

- `paper_content.txt:16-32`：摘要明确 Stateflow models、自动 search-based repair、global/local search、repair objectives、mutation operators、9 个 faulty Stateflow models、GitHub 与 Zenodo 资源。
- `paper_content.txt:71-92`：贡献包括 Stateflow repair method、open-source tool、replication package 和 9 real bugs dataset。
- `paper_content.txt:121-126`：Stateflow 被定义为 Simulink 下的 state chart 建模语言，主要元素是 states、transitions 与 boolean conditions。
- `paper_content.txt:137-180`：整体流程包含自动插桩、SBFL/Tarantula suspiciousness、仿真测试、repair objectives 与人工验证 plausible patches。
- `paper_content.txt:182-188`：算法输入/输出：Simulink model、suspiciousness ranking、plausible patch archive、partial patch archive。
- `paper_content.txt:200-255`：Algorithm 1 说明 global/local search、mutation、测试执行、plausible/partial archive 更新。
- `paper_content.txt:279-315`：三类 repair objectives：failure active time、failure trigger time、failure severity。
- `paper_content.txt:319-360`：15 个 Stateflow mutation operators 覆盖 delete / replace / insert。
- `paper_content.txt:396-425`：实验数据为 3 个 case study、9 个 faulty models；requirements 细节在 replication package。
- `paper_content.txt:433-454`：配置、运行次数与 MATLAB 2022b / Windows 10 环境。
- `paper_content.txt:541-568`：结果显示 FlowRepair 找到 plausible/valid patches 的数量及相对 baseline 的优势。
- `paper_content.txt:571-582`：作者说明外部效度、参数和随机性威胁。
- `paper_content.txt:625-635`：相关工作比较，强调 Simulink/Stateflow repair 与其他 CPS repair / NN repair 的边界。
- `paper_content.txt:648-653`：future work 提到未来可能探索 LLM as mutators。
- `paper_content.txt:655-659`：GitHub live repository 与 Zenodo replication package。

## 5. 主要风险与使用边界

- 无 NL 输入，不能直接覆盖本文的 `<NL, STM_0> -> Better STM` 需求一致性修复问题。
- 强依赖 MATLAB/Simulink/Stateflow、仿真 test oracle 与 Stateflow 模型表达；迁移到文本 DSL 需要转换层与公平性说明。
- 数据规模较小：9 个 faulty models / 3 个 case studies；作者也承认外部效度有限。
- plausible patches 可能 overfit；实验中的 valid patch 需要人工语义验证。
- 随机搜索只重复 5 次，且 1 小时预算 × 9 模型 × 2 算法已经形成较高计算成本。
- 不使用 LLM；只能作为 non-LLM search-based repair baseline 或 repair objective / mutation operator / simulation feedback 参照。
