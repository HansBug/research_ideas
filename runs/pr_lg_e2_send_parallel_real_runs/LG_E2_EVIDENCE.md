# LG-E2 real-run Send/serial equivalence evidence

本文件汇总 PR-LG-E2 在修复后 clean commit 上完成的四例真实 `.env + stream` run。运行命令显式使用 `set -a; source .env; set +a; source venv/bin/activate`，但本文件不记录任何 secret。

## 1. 总体验收

- 绑定 commit：`93e4aa88d1e85c708aab022ca299b8f4fc343ae5`。
- clean commit run：4/4。
- LG-E2 SD-6 event：6 个；parallel enabled：6/6；fallback：0/6。
- serial control 对照：6/6；serial alignment ok：6/6。
- parallel/serial canonical hash 一致：6/6。
- 验收结论：`PASS`。

说明：CARA run 有 3 次 iteration，因此有 3 个 SD-6 LG-E2 event；这不是重复 run，而是同一 agent-loop 内多轮 validation/repair 的正常 evidence。

## 2. 四例 latest SD-6 对照摘要

| path | case | verdict | clean | events | latest iter/epoch | fanout/worker | serial alignment | canonical result hash | serial equivalence hash | first blocking | oracle weak | coverage hash | report |
|---|---|---|---:|---:|---|---|---:|---|---|---|---:|---|---|
| path1 | `path1_abs` | `success` | ✅ | 1 | `0`/`0` | `6`/`6` | ✅ | `sha256:f69e0e6779af534835180870edc2cc72a4700cf65a2b8655a5d7a7907ce1116a` | `sha256:b7bc12bf5da54a33884d2981d4e43c3c43b1180cdca8b7c8265117cebfe6e2fd` | `<none>` | ❌ | `sha256:efeb9c33828815a0199be23ebf9d1f0ac2c29918f5164160c3b5e3fa6866a33d` | [pr-e1-path1_abs-default-lg-e2-dotenv-clean2-f153405c](./pr-e1-path1_abs-default-lg-e2-dotenv-clean2-f153405c/report.md) |
| path1 | `path1_cara` | `success` | ✅ | 3 | `2`/`2` | `10`/`10` | ✅ | `sha256:d476d5fea2e8267be88dddced48a9bc51a42a87462a6f2970c185119a4cd0db7` | `sha256:3816e72db4858c3e31f3bf7f59c0747df32a8e2c9830beb23b10cd20a28548e6` | `<none>` | ❌ | `sha256:81297bdf0d9b6fcd2f6241ee2beda4584a432d22da9194c17e996a3c07f8349d` | [pr-e1-path1_cara-default-lg-e2-dotenv-clean2-185f7bfd](./pr-e1-path1_cara-default-lg-e2-dotenv-clean2-185f7bfd/report.md) |
| path1 | `path1_elevator` | `success` | ✅ | 1 | `0`/`0` | `8`/`8` | ✅ | `sha256:67702c515b39e2d1cadb94d3f29d819a7ac65a49b6f8900996b8cb894bf12732` | `sha256:6a62294e0b098067bd3796fc51069f7c59a891115976af3f6dd047b325a3aae2` | `<none>` | ❌ | `sha256:e66388d9188270ffb32ba8f7eca069c9975b0cc5454edd36f3da605b916d2711` | [pr-e1-path1_elevator-default-lg-e2-dotenv-clean2-40069e26](./pr-e1-path1_elevator-default-lg-e2-dotenv-clean2-40069e26/report.md) |
| path2 | `path2_lng_ems` | `success` | ✅ | 1 | `2`/`0` | `13`/`13` | ✅ | `sha256:e2f0000aa656413c37b9da55635593391cba2ffab2c822358073d1a791c84f58` | `sha256:29d7c0fafdcacf390175197f890e228b698ed9417f05ac5e9fbbd9159b27f1dd` | `<none>` | ❌ | `sha256:042a8b51064d3ab3a0db96e52b66d738bf44fcc7fba79612b8dc758059284dbe` | [pr-e1-path2_lng_ems-default-lg-e2-dotenv-clean2-945dc6e5](./pr-e1-path2_lng_ems-default-lg-e2-dotenv-clean2-945dc6e5/report.md) |

## 3. 全 SD-6 event 明细

| case | iteration | scenario_epoch | fanout | worker | parallel enabled | fallback reason | serial control | alignment | parallel canonical hash | serial canonical hash | serial equivalence hash | selected feedback digest |
|---|---:|---:|---:|---:|---:|---|---:|---:|---|---|---|---|
| `path1_abs` | 0 | 0 | 6 | 6 | ✅ | `` | ✅ | ✅ | `sha256:f69e0e6779af534835180870edc2cc72a4700cf65a2b8655a5d7a7907ce1116a` | `sha256:f69e0e6779af534835180870edc2cc72a4700cf65a2b8655a5d7a7907ce1116a` | `sha256:b7bc12bf5da54a33884d2981d4e43c3c43b1180cdca8b7c8265117cebfe6e2fd` | `sha256:74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b` |
| `path1_cara` | 0 | 0 | 7 | 7 | ✅ | `` | ✅ | ✅ | `sha256:79e0a1adee4403afa15c58fd54e300eaa7b3d3267e5e7aa850276eebdbada926` | `sha256:79e0a1adee4403afa15c58fd54e300eaa7b3d3267e5e7aa850276eebdbada926` | `sha256:76c84cd106765ada005cdc08fb1cb860fc5412ced0c3d39d06b2ec7a4eabb554` | `sha256:74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b` |
| `path1_cara` | 1 | 1 | 8 | 8 | ✅ | `` | ✅ | ✅ | `sha256:07004845816c9a98d7a664b5aca6e4fa47f4907f18d59af5cbd3877742135b65` | `sha256:07004845816c9a98d7a664b5aca6e4fa47f4907f18d59af5cbd3877742135b65` | `sha256:29708d2fd4f951cb8c7c7dff7df00782048f4560c9f0d22a1e8a37217d94c0e6` | `sha256:74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b` |
| `path1_cara` | 2 | 2 | 10 | 10 | ✅ | `` | ✅ | ✅ | `sha256:d476d5fea2e8267be88dddced48a9bc51a42a87462a6f2970c185119a4cd0db7` | `sha256:d476d5fea2e8267be88dddced48a9bc51a42a87462a6f2970c185119a4cd0db7` | `sha256:3816e72db4858c3e31f3bf7f59c0747df32a8e2c9830beb23b10cd20a28548e6` | `sha256:74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b` |
| `path1_elevator` | 0 | 0 | 8 | 8 | ✅ | `` | ✅ | ✅ | `sha256:67702c515b39e2d1cadb94d3f29d819a7ac65a49b6f8900996b8cb894bf12732` | `sha256:67702c515b39e2d1cadb94d3f29d819a7ac65a49b6f8900996b8cb894bf12732` | `sha256:6a62294e0b098067bd3796fc51069f7c59a891115976af3f6dd047b325a3aae2` | `sha256:74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b` |
| `path2_lng_ems` | 2 | 0 | 13 | 13 | ✅ | `` | ✅ | ✅ | `sha256:e2f0000aa656413c37b9da55635593391cba2ffab2c822358073d1a791c84f58` | `sha256:e2f0000aa656413c37b9da55635593391cba2ffab2c822358073d1a791c84f58` | `sha256:29d7c0fafdcacf390175197f890e228b698ed9417f05ac5e9fbbd9159b27f1dd` | `sha256:74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b` |

## 4. 可复现性与边界

- 四例均由 `runs/pr_lg_e2_send_parallel_real_runs/*/reproducibility.json` 记录 commit、dirty flag、diff hash、prompt snapshot hash、runner command 与 provider presence/redaction 信息。
- `serial_equivalence_hash` 排除 operator event 完成顺序、wall-clock timestamp、provider latency 与 raw prompt/output；hash 输入来自 canonical scenario results、selected feedback digest、scenario history summary、coverage summary、oracle weak 与最终 NFRR / eligibility / verdict 摘要。
- LG-E2 evidence 是 infrastructure/auditability evidence，不把 Send 并行耗时优化写作模型质量主贡献。
- Path2 LNG EMS 本轮 run 有效且 `main_result_eligible=true`，但 `path2_ref_model_blueprint_eligible=false`，不能宣传为 Path2 ref-model 主蓝本。

