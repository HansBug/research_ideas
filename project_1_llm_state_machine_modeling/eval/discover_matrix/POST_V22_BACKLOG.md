# v22 跑完之后才能动的项

`runs/paper1/matrix-v22` 在跑期间，pipeline 的 `src/` **冻结**：每个格子是一个新起的
`python -m` 进程，中途改源码会让后启动的格子用另一份代码，产出一次异质运行且没有任何提示。
由 [check_run_homogeneity.py](./check_run_homogeneity.py) 守住。

下列各项来自本轮三份 review，全部落在 `src/` 或依赖它，因此推迟到 v22 落盘之后。
**推迟不等于降级** —— 每条都写明了它属于哪一级、以及为什么现在不做。

## 必须在 v22 **报告发布前**解决（I 级）

### I-3 run record 不记录本仓库 commit，v21 与 v22 的记录无法区分

`vars_hash`（`assertions/runtime.py:357`）覆盖 model / inspect / source_mappings /
source_exclusions / registered_vars，**不覆盖** `exclusion_roles`，也**不覆盖** `inserted_states`。
实测 0047：带与不带这两者，`tool_env_hash` 都是 `9ab85ed7…`。`discover-run-started` 有
`pyfcstm_version`，没有本仓库的 commit。

所以尽管 `cardinality` 在 16 个 scope 上变了答案，**没有任何字段能把 v22 的记录与 v21 的区分开**。

- 现在的替代：`run_manifests.json` 在 eval 侧记下开跑 commit，`--verify` 核验运行期间源码未变。
  这够支撑 v22 的报告，但它是外部记账，不是记录自带的证据。
- 正解：在 `discover-run-started` 里记 `git rev-parse HEAD`。**不要**动 `vars_hash` —— 那会改变
  断言哈希，使历史 bundle 无法比对，代价大于收益。

### I-4 已在本轮解决

eval 全量自 `8f5cb3ba` 起就是红的（`test_a_false_resting_on_a_converter_owned_element_is_reported`
断言的是政策反转前的行为），而每个 commit body 都写「eval 侧 N passed」—— 那只跑了
`test_holdout_stays_clean.py`。已修，现 215 passed。**教训记这里**：报测试数时必须说清跑的是
哪个范围。

## M 级，不阻塞（按代价从低到高）

| 项 | 内容 | 为什么不是 I |
| :-- | :-- | :-- |
| M-6 | `vacuous_containment_findings` 在 `nodes.py:50` 被 import 却从不调用 | 按 import 数会数出 8 道门、实跑 7 道，只影响门数统计的读法 |
| M-2 | `if self.inserted_states:` 使「契约里零插入态」（格集内 `0000`/`0018`）与「无契约」不可区分 | 实测两条路径在全 60 pair / 627 个 state 上零分歧；改 `None` 哨兵更干净 |
| M-3 | `_ref_lookup_keys` 有 52 个退化短键（`segment:1`、`1`），`setdefault` 先到先得 | 实测 0/1712 走到它们 —— 键序「最具体优先」使长键总是先命中。但**那个顺序现在是正确性依赖，docstring 没写** |
| M-1 | `test_exclusion_roles.py` 的 fixture 对 `synthetic_state` 已按真实形状写，另三种 kind 仍是裸名（真实是 `variable:<n>` 33/33、`event:<n>` 387/387、`state:<n>` 60/60） | 后缀索引把它掩盖了 —— 而这正是它抓不到前缀回归的原因。同一类错误让 V4/V5 死代码活了一整轮 |
| M-7 | `test_verify_still_fails_on_a_burn_that_was_not_recorded` 原地改冻结的 `holdout.json` 再 `finally` 还原；SIGKILL 会毁掉一个写一次的制品 | monkeypatch `holdout.FROZEN` 到 tmp 路径即可 |
| M-1（公平性） | `_inserted_state_role` 兜底返回 `omission_surrogate`（可采），理由写的是「丢失发现的代价更大」—— 那是拿**自己的指标**当判据，不是中立的 fail-closed | 实测兜底命中 28 次全是 `UnspecifiedInitial`（语义上正确，是设计路径），**「配对失败」的真兜底命中 0 次**。理由不当、影响为零 |
| M-2（公平性） | `prompts.py:16` 的 `"exit the current mode/road/region"` 是所有 prompt 里最后一个带领域气味的词 | 不含元素名、不含期望真值、对所有 pair 一律生效（无集中度可解释）。但 vehicle 域横跨 `0029`/`0050`（调优格）与 `0032`/`0047`（留出格），换中性词更稳 |

## 结构性的一条，不是缺陷但要记住

**`initialization_anchored` 门把 `EIS-0047-03` 封死**（预注册 §9.1）。修法显然（把门收窄到行为类
谓词，因为 `edge_declared` 问的是模型**声明**了什么，而模型可以声明任何触发的 `[*]` 出边 ——
0047 的缺陷恰恰就是这个）。

**故意不在本轮修**：那会是「在准备运行的中途、由一条台账记录驱动的规则变更」。改为预注册，使
v22 若在该记录上未命中可归因到门而非能力。**下一代次可以改，但改之前要先想清楚它是否因此把
`EIS-0047-03` 烧掉** —— 修一道被某条记录暴露的门，与看着那条记录写规则，界线很细。
