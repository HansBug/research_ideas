# A1-ext 运行事故记录（run record 附件）

本文件记录 2026-09-11 A1-ext 运行期间的非实验性事故；全部时间为 UTC。每条写明起止、影响范围、处置与是否进入统计。

## I-1 Sonnet 首次启动全部 HTTP 403（12:41 至 12:44）

tmux 分离会话未继承本机代理环境变量，Sonnet 泳道裸连 Anthropic，run `0242288dd7ff47c2a193eb93cf13f9a2` 的 162/162 格在 3 分钟内全部 `failed_with_receipt`，错误为 403 `Request not allowed`。同一 key 经本机代理 `127.0.0.1:17777` 直连 `/v1/models` 与 `/v1/messages` 均 200；aizzz 不走代理同样 403。处置：三个启动脚本显式导出代理并把 `127.0.0.1` 列入 `no_proxy`；失败 run 整体移至 `method/sonnet_failed_403_attempt1/` 作证据；Sonnet 以新 run `10ed3f533ec44466b38e852b46006252` 重启（12:48）。该事件属本机环境配置错误，不属于事前登记的 provider 瞬态失败，不计入重跑配额，其 162 格不进入任何统计。

## I-2 Muse 泳道 rc=127（13:30）

Muse run `6ea657d77bf04d6982e38786edfd8519` 正常完成（162/162 completed，54 pair completed），但 `logs/muse-method.exit` 记录 rc=127：原因是 Muse 运行期间原地改写了 `run_method.sh`（加代理导出），bash 按旧字节偏移续读到新文件中间的一段路径并当作命令执行。对 run 产物无影响。纪律：泳道运行期间不再原地改启动脚本。

## I-3 旧编排器未被挂起并启动重复 judge（14:30 至 14:44）

第一版 `orchestrate.py` 同步阻塞在 Muse r1 judge 上，且 `remote()` 经本地 shell 拼接导致远程 `$(nvidia-smi …)` 在本地展开为空、所有权检查恒失败。切换到 `orchestrate2.py` 时对旧实例执行 SIGSTOP，但 `pgrep -f` 命中的是 tmux 的 `bash -c` 包装进程（pid 1615595），旧 python（pid 1615600）并未挂起（左侧监控会话核实其 `/proc/status` 始终为 S）。旧实例在 14:30:47 醒来，用一小时前的内存视图覆写 `state.json`，并于 14:36:49 启动重复的 Muse r2 judge run `71922e9b668c4b4b87fe9de448cd5d15`，与新编排器 14:32:43 启动的合法 run `c387e3c643ac4db8a6add7e0bcb094a5` 并行约 7 分钟，完成 3/54 pair。处置：14:44 杀掉旧 python（其 judge 子进程因输出管道断裂随之退出），重复 run 目录移至 `judge/_aborted/muse-r2-duplicate-71922e9b`，`logs/muse-judge.exit` 追加 aborted 行；随后 `tmux kill-session -t a1ext-orch` 因精确名已不存在而前缀匹配到 `a1ext-orch2`，误杀新编排器第一实例（合法 judge 因 `start_new_session` 幸存）。14:45:11 按 `logs/*.exit` 与 `judge/` 目录手工重建 `state.json`（队列、接管中的 judge、已完成列表、Qwen 切换事实）并以会话名 `a1ext-orchestrator` 重启编排器。重复 run 的 aizzz 调用不进入任何统计；合法 Muse r2 judge 在此期间承受双倍并发，可能影响其时延但不影响判定内容。纪律：tmux 目标一律用精确名 `-t =name`；杀进程前用 `ps -o comm=` 核对可执行名。

## I-4 本机到 xai 的 8100 隧道中断（约 14:41 至 14:53:55）

原隧道所在 tmux 窗口 `0:51 e2-qwen-tunnel` 消失，时间与 I-3 的清理操作重合；此后 `curl 127.0.0.1:8100` connection refused，远程 SGLang Qwen 服务本身正常（GPU 满载、远程回环可用）。Qwen run `1dc566e6` 的格数从 14:38 起停在 69/162，`logs/qwen-method.log` 连续 `stream_chunk_timeout`。左侧监控会话于 14:53:55 以 tmux 会话 `qwen-tunnel-8100` 重建隧道（ssh pid 1741078，8100 监听挂在 ControlMaster mux pid 1740069 名下，属正常复用）。14:56 Qwen 泳道恢复写入，至 15:00 为 72 格，其中 0 格落为 provider 失败：中断期间在途请求由 method 内部 8 次 transport retry 吸收（截至 15:00 共 40 条 retry 记录，分布在 5 格），属事前登记允许的 provider 侧瞬态失败处理。新增 `tunnel_watchdog.sh`（tmux `a1ext-tunnel-watchdog`）每 60 秒探测 8100，连续两次失败写 ATTENTION 并在无进程监听时拉起备用隧道 `a1ext-tunnel-8100`。

## I-5 8100 隧道第二次中断（约 15:02 至 15:10）

左侧监控会话 14:53:55 重建的隧道把 8100 监听挂在共享 ControlMaster mux（pid 1740069）名下；`~/.ssh/config` 的 `Host xai` 配了 `ControlMaster auto` + `ControlPersist 10m` + `ProxyCommand`，所有 `-L` 转发共享同一 mux 主进程，主进程因代理抖动退出时转发一并消失。第一版 watchdog 于 15:05:18 报警并拉起备用隧道，但备用命令同样经 mux，`mux_client_forward: Port forwarding failed` 即刻退出，且它只在第 2 次失败时尝试一次、之后不再重试（缺陷）。Qwen 从 15:02 起停在 84/162 约 8 分钟。15:09:51 我方以 `-S none` 循环会话重建隧道（ssh pid 1752979，独占连接）；左侧监控会话同时也在重建，其消息把 pid 1752979 记为对方会话，我方据此在 15:13 误停了自己的循环会话，隧道再断约 1 分钟，15:14 以 `-o ControlMaster=no -o ControlPath=none` 的专用会话 `a1ext-tunnel-8100` 重建。watchdog 换为 `tunnel_watchdog3.sh`：连续两次探测失败即告警，此后每分钟在“无进程监听且精确会话不存在”时以同样参数拉起专用隧道。远程 SGLang Qwen 服务全程正常。中断期间 Qwen 无格落为 provider 失败，在途请求由 method transport retry 吸收（截至 15:11 累计 112 条 retry 记录）。原始运行三天的旧隧道（pid 495067）同为 `-S none`，与根因一致。

补记（15:36）：两次隧道中断合计使 Qwen run `1dc566e6` 的 2 格耗尽 transport retry 后以 `provider_error: Connection error.` 落为 `failed_with_receipt`（contract_extraction 阶段，落盘 15:17:07 与 15:19:56）：0009/round-1 0019/round-1 。按事前登记 §3，编排器将在 Qwen method 结束后以 `--rounds 1 --round N --pair-id P` 隔离重跑各一次，原失败回执保留在主 run 中，冻结 judge_source 时按同一键替换。

补记（16:50）：Qwen run `1dc566e6` 的 `0009/round-2` 以 `limit_exceeded: model_calls limit exceeded` 终止（contract_extraction），编排器按错误码判为非 provider 失败。核对其 audit：18 条记录中 10 条 `provider_timeout`，即 600 秒调用超时的重试逐次占用了结构化阶段 12 次 model-call 预约直至耗尽，终止原因由 provider 侧超时诱发。按事前登记 §3 的“整格以 provider 错误结束”口径，人工以同一 `run_recovery.sh` 隔离重跑一次（tmux `a1ext-recovery-0009-r2`，输出 `method/qwen_recovery/0009-r2/`）；冻结 `judge_source/qwen` 时需人工把该格替换为恢复格并更新 MANIFEST，原失败回执保留。编排器自动重跑的 provider 失败格为 `0009/r1`、`0019/r1`、`0039/r1` 及其后新增者，见 `state.json`。

## I-6 Muse r3 judge 在 pair 0059 上 schema 路径耗尽（16:43）

Muse r3 judge run `076b959315ba4d809c4591f9052b02da` 完成 53/54 pair，pair 0059 失败：第二读 `validity_primary_2` 对报告 `VB-01-a08faffc6f`（拆块 s1）连续 6 轮返回同一自相矛盾的答案（`defect_class D1` 同时把核心子句 C1 标为 REFUTED），被跨字段一致性校验拒绝，`turns limit exceeded`；最后一次重试 `provider_error=false`，即不是 provider 故障，A3 的 `recover_judge_provider.py` 按设计拒绝对 schema 失败做续跑。六轮签名完全相同，属 §12 意义上的结构性死路：同一输入下模型坚持一个校验器不接受的组合，也暴露评审端 prompt 对“D1 与 REFUTED 核心子句互斥”的引导不足，登记为待修（§10 第 2 类逃生口）。按 v61 同类先例（`0045` r1 契约抽取 `turns limit exceeded` 后用同一代码单独重采样一次并如实登记）与 A4 的 `turns limit exceeded；六次 schema 拒绝` 续接先例，对该 pair 用同一冻结代码与 profile 单独重采样一次：run `89b5f76708474770b654c7da0ddd6252`（`run_judge_pair.sh muse 3 0059`，workers 1，输出 `judge/muse/r3/89b5f76708474770b654c7da0ddd6252/`），原失败 run 与 `failures/0059.json` 保留。若重采样再次死路，则该格记为 pending=1 并在报告中披露，不做第三次。

补记（17:46）：I-6 的重采样 run `89b5f76708474770b654c7da0ddd6252` 于 17:44:57 以 rc=0 完成，`judge/muse/r3/89b5f767…/pairs/0059.json` status=completed；Muse 三轮 judge 至此 162/162。原失败 run `076b9593…` 的 53 个 pair 结果与 `failures/0059.json` 保留不动；分析脚本按 (pair, round) 合并两个 run 目录，重复键会报错，已核实无重复。

## I-7 编排器过早写 DONE（20:24）

`orchestrate2.py` 的终止条件只检查“三模型已冻结且 judge 队列为空”，未检查 `judge_running`，因此在 20:24:23 用 Popen 启动 Qwen r3 judge（run `df8f1b6a6e1a4ca39f87c4e2e9469be2`）的同一循环里写下 DONE 并退出。该 judge 以独立会话启动，不受影响，继续运行；其结束由 `logs/qwen-judge.exit` 的 end 行判定，人工接管记录。过早的 DONE 文件改名为 `DONE.premature-20260911T2024Z` 保留，最终 DONE 在 Qwen r3 结束并核对后再写。对数据无影响。

## 收尾（21:06）

三模型 486 格 method 与 486 格 judge 全部完成：Sonnet r1–r3、Muse r1–r3（r3 含 0059 重采样）、Qwen r1–r3 全部 rc=0，pending=0。DONE 于 21:06 写入。远程 Qwen 服务（xai GPU 4-7，tmux `paper1-a1ext-qwen`）与本机 8100 专用隧道（tmux `a1ext-tunnel-8100`）及 watchdog 保持运行，未擅自停止，等用户裁定。最终同格配对表由 `compare2.py` 生成并存为 `final_comparison.md`；`compare.py` / `compare2.py` 副本随目录保存。
