# LLMS-EMP 60 组 PlantUML/FCSTM 主 session 人工验收

## 验收身份与口径

- 实现提交：`393a1a71c3b959210aa429fbf552ddd0d6e46acc`
- 冻结证据提交：`0de936b2b5ac0c93c67d13314601b5666758f850`
- FCSTM 文件集合 SHA-256：`591ff856f8a8985b1fcc1682d76193efeaea416be11ae84c64231abf00e17a82`
- PlantUML：`1.2024.7`，jar SHA-256 `e34c12bbe9944f1f338ca3d88c9b116b86300cc8e90b35c4086b825b5ae96d24`
- pyfcstm：`4ea23c9b153f47e5c4a2125d95b466eee6eed13e`
- 机器前置：`60/60` source parse、FCSTM parse/inspect、AST audit；`754/754` source transition macro；`0` blocked；`0` silent drop。

本账本由本轮主 session LLM 在最终 FCSTM 冻结后，按 `0000 -> 0059` 顺序逐组读取完整、带行号的 PlantUML STM0 与完整 FCSTM STM0 后填写。每组核对 state hierarchy、initial/final、全部 transition、opaque label/body/lifecycle、synthetic rationale 与 operational debt。高风险组 `0000, 0004, 0005, 0007, 0008, 0015, 0018, 0022, 0024, 0027, 0034, 0038, 0039, 0044, 0049, 0053, 0054, 0057, 0058` 又按逐 transition macro 做了第二遍核对。

`PASS` 只表示 **FCSTM + mandatory trace bundle 的结构保真通过**，不表示行为等价。60 组均因至少一项 opaque/ambiguous/unsupported operational debt 而保持 `fcstm_execution_eligible=false` 与 `discover_eligible=false`。

## 逐组账本

| case | source SHA-256 | FCSTM SHA-256 | 结构 | 主 session 对读结论 |
|---|---|---|---|---|
| `0000` | `8fd2f71b338836488e2e29fe19c4e58c4992d4186367f43efc121fae6c36db7f` | `8cba7067504a8f3f46773e9d9c39bb1a704a801526b30af53b40f9ac9d823890` | PASS | root `HumanDriving/Autonomous` 与两个 scoped `InitialState` 分离；7 条 macro、event initial wait、跨层 exit/continuation 和 body 均齐。 |
| `0001` | `566d10146e2e3b6bc3d510cbe29ece0c2dfa104ea0f4230be1989f6fe3112b2e` | `2267d61fe41edafe4ab59385c8bd3b3657f1791936b1a0e862ecc6bfda84d41a` | PASS | 4 state、root initial、5 条普通迁移与两条 body 完整对应。 |
| `0002` | `945aa398670dec96e72eb75bf7ca969371d1c7eabbd1bd9ce7c153565e35a934` | `02f822d8be21303e57f0d0f1d2f6ed53ff4a1cf441ada4a5a313d748cd21347d` | PASS | `PumpControl` hierarchy、两级 initial 与四条事件迁移逐项一致。 |
| `0003` | `01208d7d90b5c5e8c240e5c4aa9cab0e6ace084afeb752b3dfdb04d17d396150` | `a075771dfb2bcc3c4f679da2db427c609c37825601bf3b236ba1754e313e6292` | PASS | `Operate` composite、三条内部边及 root start/keyOff 保留；composite exit 使用 forced macro。 |
| `0004` | `6313557b3733707618bb785619f2b87e2f93ed3373c038222112f8cff3d2694c` | `2ce4fdaf8845d11b41a6af9b2d3992867cbc857f4bd1aff8552b55f3a4708537` | PASS | self-initial 由可停止 surrogate 保留；9 条 transition 齐；4 条 lifecycle 仅挂为 abstract hook。 |
| `0005` | `0727625138b0bac74c9332b4af3c8e653f0721cb84e44628332b3bebd3308f77` | `f7e2f0d3bca87d88834af3360639a683e3a65df6f0157163510c9c7e3c572b4e` | PASS | 16 条 source macro 齐；三条 `Open Door` deep-entry occurrence 均保留，且均在 `UnspecifiedInitial` fallback 之前。 |
| `0006` | `3dfdda2a0f6144429bd81717778a05f021bd455cad0efa0f29192f6a041b0952` | `4a1c8fc256e8ee9944712ba58387d41762b8e9b77436b09b9896506c39292d61` | PASS | UAV flat graph 的 7 state、initial、11 条普通迁移和三个 body 齐。 |
| `0007` | `2e95dc642f73f0d546f8fc356d6ac3a03283887a693a8c56797c1199da64d2b2` | `a462447491a8058b11419b545e7e2d3f9576850f40c28978a15eceee326f51d4` | PASS | 三个 collision event 分别绑定 Brake/Steer/Alert deep entry；三个 nested final hold 与 root final 均齐。 |
| `0008` | `0d7b489764211f6857eb71ab15af67f692a637c2a2a548b5e5ce7d88f255cbd2` | `04e146e89698d5dfe07aa877ab0774af3fd94022ba3bd3dd4b0edb313bf03a2a` | PASS | 28 state、27 transition、多个 scoped `ExecutionTime/Junction1` 与 TurnOff nested final 完整；时间/概率仅 opaque。 |
| `0009` | `fa210ede8e3af220ab1c96a5504e93dd8bccf4d4e06af68d15c988654c76ef53` | `ef8ba51705b530587ea0843a9faebe27b00a98acfd4f51bd05232afef56cb52b` | PASS | Autonomous/Highway/Urban/CollisionAvoidance hierarchy 与 scoped `FinishState`、26 条边一致。 |
| `0010` | `73021d0499bdbbc34299e07733dda58162aefdf297e57bd6aae76da940aaed53` | `b638507f16a5b1ff4557a3fbf76f38c0bd24a9c3ea221e050f813a924c8577bb` | PASS | 5 state、8 条 edge 与 body/`<<submachine>>` opaque metadata 齐。 |
| `0011` | `3d75fa9170ba4fdf5b0e8061e2dc1bba709824fbffb6768713232f262bb6ce28` | `11ee049e364048a6a5104413f8a9e70fd6ac28300bb24746967da343e77ff480` | PASS | 与 `0001` 同构，全部 state/edge/body 对齐。 |
| `0012` | `0314bb466726c4ba81177282e717511244fc77bf24682ba951f4103fd32b169a` | `5c2717310c343f9d3166add39113b65b2cbb0793c5f0df8146e5becc5018d9b9` | PASS | Off/Operate hierarchy、五条事件边与 composite forced exit 对齐。 |
| `0013` | `d46d378e8239a870c0e5dec9f91181ba49cd1678544697446b2503b2fd5acb07` | `d90985d4a257ea33c06078fe99f3de930fb18d3d2c472c37b4c108aaa6a978bd` | PASS | PumpControl 三子状态、两级 initial 与六条双向控制边齐。 |
| `0014` | `711124b29144fbb337739a5e7d8d97d8b7cdacd5828e71a036f0bbbae40364fc` | `890606eaa259bb7115dc6be50b169bb41989c04d1c618636e9c8315f62d068fa` | PASS | root/Approaching/EmergencyStopping 缺 initial 均 fail-closed；10 条 macro 和 generic body 齐。 |
| `0015` | `beba54d00f7620bcc9b14a882183354a7d49a56468c27fda7a0d2fd4c11b1c6b` | `6b03cc6b56e8df69b56cf442783adbc1886be3422ca9f63550ccfcd97173199d` | PASS | 六个 scoped `State1` 独立；22 条跨层 macro 齐；`Remove Item` deep entry 优先于默认 initial。 |
| `0016` | `2720cab7a2e9d2d06ff784d4e5821c4905c21408d19b0db0496b679394d06d50` | `f6174e4f88a1ababd642442fe5c1f793fd309fb0cc28680a510bbbd6e1227d43` | PASS | event-gated root initial、Search nested final、Formation/Attack 往返 macro 齐。 |
| `0017` | `f8a5658fe506ac755121a5dc3ca3e03564833a8abf51cdd1fb54dd41274b4d79` | `3ffda42026e3a95fb8b7caf1099aef898a4e3c87b5c62fda3abe14ec25b308e9` | PASS | CA/F/R/P alias 与 10 条 source edge 齐；三条 child final occurrence 未去重；CA 缺 initial fail-closed。 |
| `0018` | `7dd9957bddd73250391bc3a00775069cd896aee734df139fd35820c2893b0b9a` | `e556d42c5c057ae3182d43ff0ac087777cdd2b337c2d7bebd354b108a14ae573` | PASS | 21 条多层 macro 均有 exit/continuation/entry；8 个 missing initial placeholder 明示；fan-out/timing 不推断。 |
| `0019` | `b4c24224cccc1a34efedeafd961ef2b4867aeb0701ce8f8a0ea78691a75c936d` | `5ed44b464818f00aa1438cbb68b78ccd54f541bee11b048e3394b6f799014fc1` | PASS | note 不混入行为；Autonomous hierarchy 与 25 条行为边齐；CollisionAvoidance 缺 initial fail-closed。 |
| `0020` | `478b8db78f5465f4ced13d2ed7f455bc12bbb5c77b5d1d0b475cdc97d905b8c6` | `f36df10020b8fabe70b41f35fa10511873d7470e64a4b7101f4c62227fbd1b2e` | PASS | `stm` name、Autonomous children、两条 child-to-Human occurrence 与两个 root final 齐。 |
| `0021` | `56fdae7230f32f95dfea0227a445220448a6718f34d6de8999192a2f763783fa` | `b9a9d89e06176be4c4fd5465fb9cae3c13f52c538dbee3e11917595a4b04a474` | PASS | Train Braking flat graph 与 body 完整。 |
| `0022` | `8ea7e01c4cf73f562b0c55fed76f8f318797aa06f9ee043170e79385f326f7c5` | `57d64c17528e6ecf28c079cdb1390c8a2368094a8107d617f8445ec04b568380` | PASS | 9 条 edge 齐；`PoweredOn -> [*] / keyOff` 为真实 root final，不再生成普通 end leaf。 |
| `0023` | `3237c282856c15de2d2cc794e37cf945b24316694858ba99b94ec69521cc5e2a` | `78894c5e565298f23d94365d53ffe7494467606865ff1dd3861e605fca0eee64` | PASS | PumpControl flat graph、三条 edge 与四条 body 齐。 |
| `0024` | `0a9b42eaa34ae47557ece09f79e387a69a29da2e13d4f833a4edaaf9a42d2598` | `50e573527c805910b55976c526855b814b9a475d0241a4a9a300d87356c065c8` | PASS | InMotion-owned entry/exit hook 与 root ownerless exit 分开；ancestor reentry/普通返回共10条 macro齐。 |
| `0025` | `a4422437b46a20b3d0a4e9745b990a2bdc24ffc315d709f3450762fd7b514254` | `700ec6957e95a00d382b9b1eecac59013875789aa2cf08cce941dfb7d9c015e5` | PASS | Microwave 六状态与16条平面边逐条一致。 |
| `0026` | `894d0cfae3a1dc6b26026f6c4eb1e342402deab997113ffc849c636aa68a4aba` | `49aece10a82ff093b2df3bf4722e480b88da5333fa3c9b1bccbe3c1a7ff05bb8` | PASS | UAV 4 state、4 transition、root final 与 body 齐。 |
| `0027` | `9a0ab14a1252a2c11fb409f770f670f465e72b8fc542f5bb5e2019e476a778c6` | `d3b6b58b433f45f86dc36f2650bd5d31a2b96d25d29ec359191a35d6baffdc28` | PASS | 三条 ActiveState initial 全保留且顺序未变；multiple-initial debt 阻止宣称运行等价。 |
| `0028` | `ef9eb75e567c05b8516af0e319003e7de3b473791a3b76727595941bb1716d36` | `3e59578a7514f1ab184bf6340d2a995e6ab2e03073e85b6f5f33f320fb567dba` | PASS | Camera 19 state、25 edge 与两个 final 齐；fan-out/timing/body 仅结构保存。 |
| `0029` | `0e203bbdf499156e24ca9a904b56de5c0c2fe2564291b451cadb185885975fdd` | `27c20fd7638932ee7228b85a7daf5ba821b2e6ac5e97aacc0d1721bb80da0bfc` | PASS | Highway/Urban 普通 composite-to-descendant edge 未冒充 default initial；placeholder 与跨层 final macro 齐。 |
| `0030` | `e1c89866e4ea2332ca45c2755508cf1c0742595876037ba3c3d0ae7f10feb9c9` | `b876c868b3325b1c315c34b2d1aade862785fbe76ded3a0225c190a9d132f7a8` | PASS | 两条 root initial event wait 保持顺序；`/ [*]` 只作 opaque label。 |
| `0031` | `3d75fa9170ba4fdf5b0e8061e2dc1bba709824fbffb6768713232f262bb6ce28` | `a2fca93e7f1989effd1caa685f2b44e44694774f62bea9fd69d0ac9f2e7e1310` | PASS | 与 `0001/0011` 同构，结构与 body 齐。 |
| `0032` | `95515e5e0af74e499fafe8da9fd82fb1a94f745f719b94288e6ece5872545451` | `622170b81a91fa7bc32cb240c4adb5662c017c064054059c98e13bda161e775a` | PASS | Device 6 state、13 edge 与六条 body 齐。 |
| `0033` | `a885b2b07e8c8761bd81c54e9e326daf3a2ce3138e4cae0c305ee6c9fe8145db` | `2037af251445e2af5c1cf45ea2a6091558a89058b329cbf86263a2b772adbb8b` | PASS | `stm PumpControlSystem {}` 作为 model container，四状态七边与 body 齐。 |
| `0034` | `47368dce1df97e572f9709094956208acb6532b92405a125582d2b538b3fe283` | `034508c247959283b176072ac0363a4ce3ffe5ab719f1f5bc6a40fa7775f7d75` | PASS | directional arrow 未伪造层级；13 edge、两个 root final、五个 lifecycle hook 与三路 fan-out 齐。 |
| `0035` | `84d17e092a8e8b903382f3a07c115bb1511466a24ce5d36dee4c24d90b990a76` | `93c79f69bad2f07cc28aa18d85a2713fef4c586024be480b9154928af2c19de8` | PASS | Microwave 16 edge 与六个 body 逐条一致。 |
| `0036` | `45c41ca247c3aa1603b8fdf0aea89013d27ab65071f2932dd4c4149a4681aa5b` | `fea8159c1273766073718d6346f83c46784c3eb1d45e1eb504a04b25613e9882` | PASS | UAV 5 state、7 edge 与 slash label/body 齐。 |
| `0037` | `98186aedfa61de1b81699fd4bd301bc000ab9f0bb900f68ff062a90c6a9e3d23` | `20805a85b4b85a4cea891d191e430fa30c862e99e2f0df493a5101205be63494` | PASS | bracket endpoint 还原为六个 state；三条 root final 与全部 signal edge 齐。 |
| `0038` | `6a3092862359b6522c285a04a3cf1a796ed9462cda766a7dfe5815f2ce1b3e19` | `c460602ae931ee4fa9bacde0d6535ad038947f2e02fbfe9c2a6aec18abdcda24` | PASS | nested/root 同名实体不合并；24 edge、4 invalid initial surrogate、重复 Junction2 edge 与 placeholders 齐。 |
| `0039` | `187fb536bf88351c12f83f63d5b5d2bf1c096b0a99aa9089ce722ba07f2a0391` | `782df96661b3a942d8691f1b1e97ab3aa251469ed4980f2317f6abb3785052c0` | PASS | 26 edge、两条 root initial、两个 Highway nested final hold 与 composite-to-descendant forced edge 齐。 |
| `0040` | `42acdd25b7fad2ff8a9502db8169a3ff849a3ba164e3381d70467c97e615cf7e` | `e3817e84b86d17c816c9b7f640bde28e265e9173bb6546277bc6577e6725e544` | PASS | 双 event initial wait、Autonomous children、forced return 与 root final 齐。 |
| `0041` | `9dc040506c4abc2dc1dcee5536542e17a8b464277dc7f108c2a94941e969675e` | `f8ea16500aa0c088370432826b70b15bb14f938203d4f32571a691d29f5b5edb` | PASS | BasicBrakingDevice 平面结构与 body 齐。 |
| `0042` | `29fbe0d61ae3a876eff04656b538e326ef8e93b3df83da0bda9be7bcfb07eb97` | `e07a8489a28f68e3e5463d647d25d873755c9689ba1c7986519db96741f8c4e7` | PASS | keyOff event initial wait、Operate 三状态与7条边齐。 |
| `0043` | `aebd7f70f2529017cb257c1b3001e18cadc8222c085b3cf7a33aada16cfb3bd1` | `d0852ce9ec23cd9f5c0e7bdad6e42e6aec6d9fb6426e488be3df2e331237931e` | PASS | bracket labels 原字符串进入 named opaque event；四条边齐。 |
| `0044` | `7f5397c95cef79f21a7d18892486a912a7cdeaa1d9d9465bac47df872e0c9b6a` | `8d51164c6f1d191de45594a802f5c9da30bfd1ac678fca607fac10959eff854b` | PASS | InMotion missing initial fail-closed；9 edge、两个 final 与三个 lifecycle wrapper 齐。 |
| `0045` | `bfe9731bf60d0dc17fd31b89dec3826f9c29be2eeebb752b48b5a1289440425e` | `91705ba9f200e1a55d78ae36bf9fcb5ee886536c012c5151e775b28ad9187ce7` | PASS | 各 composite 内同名 `DoorOpenWithItem` 按 lexical scope 独立；20 条跨层/内部 edge 齐。 |
| `0046` | `709704f395b88943b357c62d4b4c1f93cb2b1e09ef0f72f8f26648de311b99fc` | `3dfdf5bb32d903419953857ce9b3da4a9b4770ee9a34e12c728f8385f6f946d7` | PASS | UAV 4 state、6 edge 与 body/slash label 齐。 |
| `0047` | `fff82632ec465f502612c40dfe4ccf552d9cf88db9e0074d533201587108ebd0` | `859be926a59315b66b8b699863aa958d0c80a1c466405b9b2c1e5af20ebaa585` | PASS | 三 alias composite 及 scoped Idle/Braking/Clamping 独立；3 final 齐；root 缺 initial fail-closed。 |
| `0048` | `91951da63cfb9eef882f8f3b45d69fbba6c22dcc4c1f1247dd4a7f91a2f079ab` | `693151e680a8b4c6dd33ec78a7630dc9391ad8d42e960e7fd274077c1b82ae0a` | PASS | 19 state、24 edge、两个 final、fan-out 与 timing body 均保留。 |
| `0049` | `85f000271f03ab4d83260494bfe73b053111cfaf660a9f3d79c7ea912063ded6` | `a8b75ab36f78ccc2f9597bf74f25bb495abd9c29ade977670c2bba78a6833776` | PASS | Highway/Urban/root 三个 `FinishState` 不合并；29 edge 与 CollisionAvoidance hierarchy 齐。 |
| `0050` | `317f517490d7ed5d6520fc8f56045625d4d9c9b870a058e6a0f1d2c21a1e24e4` | `b30001cc132aa29a9b218136993edc9c8eb72479da46397bf25c94cd1aa2dd42` | PASS | literal `\n` label 原样命名；deep chain、nested final 和两个 root final 齐。 |
| `0051` | `4f821f97dcb4ba5854519a1255f41ee39f44b23e13b77663db966d82f8d23a25` | `8446a1b907c9783555a4c083c7cc3cd805f9b5421b007525ce652a56122f654c` | PASS | Braking 平面结构与 body 齐。 |
| `0052` | `13021d64f5ea5479d51dadc86dcfd1125d4f8535cd5a807ebf54df1d8df385b1` | `2e9a687e4b7ebbd39127a927eb8260ac35ae872ad8c0d86825d05cc956d8c0bf` | PASS | Off/Operate 两级结构、8 edge 与 forced keyOff 齐。 |
| `0053` | `ce9980726ff386e89f12448d5c9cfd123590e6b3e804649ff6c3928054a1edc3` | `c5b082dcd1d567b99a3a07e2e659bb9d16a4125a25c120029e76bb8df9f07552` | PASS | 两条 PumpState 无标签 fan-out 均按源顺序保留；三条 body 齐，运行歧义单列 debt。 |
| `0054` | `096e925ebe77027797d115e656538bc942eb62e77b1e3dc426f51ae457533d14` | `bfc2b3dca8a7de65c68542aa8ffc9b71fcf90962e6434d3f8fc24795deb9095e` | PASS | 8 edge 与4条 lifecycle source item 齐；abstract hook 未冒充已注册动作行为。 |
| `0055` | `322a51f31a2fe5f946fa71caf2f1e44a4d2c7ffe089b2ca987de2ae7d009abe6` | `750004071ba8ecb96a3d6e1d090214979e072afc8e96d88f9bf53139418945e6` | PASS | Microwave 16 edge 逐条一致；`[time = 0]` 保持 opaque。 |
| `0056` | `bf93ab42299d56f2aca29149e61760019633d58293e0b2b464360e4d5c20c97f` | `78a7e6e7529e24d272fb6794349c0324db7e886bf20445a18a4f829b8ff0ce6f` | PASS | Search composite loop、4 条 root transition 与 root final 齐。 |
| `0057` | `6678019769df574ad084ce86bfe39e078fce4203e6de76b77755b89c3d037a79` | `67c243f4db94710ba103956765ba1ed33866a98661bf53a101fab211b22eebd6` | PASS | CA/FC/RC/PC hierarchy 与10条 edge 齐；event root initial 进入 CA 后停 placeholder，不猜三分支。 |
| `0058` | `5181a79ba0047ffa94d309464ba44fa0600aa5f0c939e20cd72a7f8ad674bea5` | `be359318c44dcd6785b7f3e2daf75f4a22fdd041b236ba9dd0ea43ddf15de5cf` | PASS | root-to-deep priority route、fork 三出边、22条 macro、6个 placeholder与 scoped `Join2.fork2/Flash` 齐；并发不推断。 |
| `0059` | `8ea3054bc9bc969094c2ad7f2fba4172c9234ac153608390878acf3c94425615` | `ecc2f3ef22936dd0caa44d82b8e021e31b378686e9aaafbae07a7813894d733e` | PASS | Autonomous/Highway/Urban/CollisionAvoidance hierarchy、25 条 edge 与 bracket label 原文齐。 |

## 人工结论

1. `60/60` 组在结构轴通过，未发现 state、transition、initial/final、body 或 lifecycle source fact 静默丢失。
2. 该结论依赖 `.fcstm` 与 case report/source map 的联合证据；`.fcstm` 单文件不表达 source braces、raw span 和 operational debt，不能单独宣称可逆。
3. 所有 opaque label 均被完整保存为 named event 与 raw trace，但未证明它们原本是 event、guard、effect 或 timing。
4. multiple initial、unlabeled fan-out 与 explicit fork 的全部边虽保留，当前单 active-leaf runtime 仍不能证明原行为；这些 case 以及其他有 debt 的 case 均不得进入 Discover。
