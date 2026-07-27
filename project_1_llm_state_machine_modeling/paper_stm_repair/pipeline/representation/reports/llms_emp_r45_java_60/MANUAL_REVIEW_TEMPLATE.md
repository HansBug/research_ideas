# Phase-II final 60 组人工/LLM 对读模板

每行必须完整阅读 NL、作者最终 PlantUML、转换后 FCSTM、working contract 和 source trace，并填写本组特有的 NL/PlantUML/FCSTM 锚点、ownership/macro/capability 判断。存在 review obligation 的 case 还必须按每个 occurrence 的唯一 obligation_id 完成绑定同一 review subject 的第二遍复核。结构保真不等于行为等价。

锚点必须使用精确 occurrence 格式：PlantUML 写成 `source-ref:<raw_ref>|<完整 trimmed 源行>`；FCSTM 写成 `element-ref:<element_id>@line:<n>|<完整 trimmed FCSTM 行>`。裸 label、裸 identifier、子串和错误 scope/行号均无效；`source_normalization` 没有 FCSTM projection，其第二遍 `fcstm_anchors` 必须为空。

| case | review subject SHA-256 | working contract SHA-256 | verdict | notes |
|---|---|---|---|---|
| `0000` | `37f4521695506147565637dc024e47acc64e6dfdbf34945f566b4aa4d61b0e87` | `4265ee80700f149ffab55b260e6e1cdcd631f72d969fdf80109caa7e3e84c727` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0001` | `5a75e91d7b8051be13e1e25b5b7a2899cbd13da6b7074267209d30f5651ee4a9` | `fc4bde9ff229e434b1bf1a6bba171e3f72925e20a823c1ddea820f94933ec71f` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0002` | `6f7cdcb914ce6d0a2e77feed45044a2ebb268d03036a68f9ee8d435c95a35c4b` | `c1c633c4396dea7abb64ae507b7907742976f469c579fe6b218617481a312f5c` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0003` | `902d46df73efd19acafb8fae9cf1b880c69da07e48f2b35e2378f3da219e8ae3` | `a061b62a2a1673acfb3a5a67fd3c40e087d698057816da6e65bd29af76a653f5` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0004` | `f1a41e12fc2f3a3329b50d5b90d49630023b52c5bb6d892ee21c1b488a723a37` | `80b343b2cde003721e08188386ed4202d0123a685b3589620366b91055101394` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0005` | `27a0530b88dee81e94d756fe187fdffbc5e123cb9d7a587879e04ac87ab948a1` | `f5513f32be0af8eebb8e2d0403d1e732693c7ca2fd65e06eeac1df00e8d5a83e` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0006` | `ca73f03d595f27974b0ca009ca9fb633d1fea8791c03736ccd88fc152d5c5b40` | `183ba7839ce5c8f6509dca051e16bc6b24e509aaa63d9c31ac4b65605a8ca578` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0007` | `be8d7711ecd3a8c06a713d6ae83d1cc4c01adbbcea7640cbc677d0716fc9191b` | `aa9634fb44a7ec38043bf3b7d2c35b6cc5d7c8a81b8e6f796463e2d46a5e66fb` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0008` | `22dfa6ac59e45396d7326760a84c43d9ceb43f444e83345beb8ad9016ed8efb4` | `bf8b28645ea3d386bde844cff6d777fbe0fcad2b5af2fa6872cb9363f3a4d117` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0009` | `8ad4e53ae0e99ab315303ab667b4a24302fa9d005b93be439828529ac50eb89b` | `c9aacb7ee7193dc567e3861584fe1c129dccf1ec08a861974741edc48032c356` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0010` | `e59e77e54e6e61afcb00b1ef0a8942676a470d476a18ca404c35236c933a27b4` | `8db144ecc99e0ca22efc29b23e08296cdb67b8fc23186d42694383392be00615` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0011` | `e8dae467545e868b37aa121dcd671f29f6a8e2dc050c2d7afb3424f227a89fbb` | `0af444b07a2b9c100b54df1edaa3d287fe44d2453063a12a2995d7c64a555cd4` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0012` | `7612eda19af14a43d6e653bf96fc3431809b05aef15eee14e2c3213f6f28ff3c` | `23659796584a069628a83fe84936680afd984fc90095dc38d5dda180456d8810` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0013` | `dd653fa7c013da4585eb77496c9b263f71823b592cb6da8ec02fda7a605232f6` | `b4028f524a7af9745ee178d0d021186597facdb9fbf62a4c2537b9fd1d11d916` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0014` | `4e01052b25eff964d18988c6d0631b939c2e2356e95efea68ab39f3d319c090e` | `0260ba9b4afde657e8b5b7f4470c17b2069e248ad356d68f1ebd9732a500d1d1` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0015` | `037a08efbf1f5fe050d526a2cdd6d7321092f143df73f64869be85e7358108cd` | `81b1b698eea392656989c03c000fbc5616291e2f798fe0dea3a7a4f74591dda3` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0016` | `d63342eca9d9c795d3bead4964c150a1955261ff5edabeae7a4bd289f91a3e8d` | `d0292b0c661ca27d3f92f931fbac6d7c088ad604601c2f96641d53c5d1bd8526` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0017` | `5245c77abe71502c913624cc5241963bafa62b6fb396315c13345512c8bca16b` | `8ac77d698602ab8230374e1139d1a4b239699f4ed0e20f3f94200137f7ed5b92` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0018` | `37d766f5cbacd80aa915cb05b6c35aaf10c2a2a642d65af4e0fd2b3be705f976` | `486f59a16725fa9e2729bad2c786484b56ca06ebefae3707ae12344e096f9757` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0019` | `f2e2c0ef03b6ee07b4179206ee1527e8a8b4d9488cacfaa1b96403341a8e3c78` | `e6b443e206afeb264710ea42d65854c0f4d24102ff0db269a6cd67bea9767dbe` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0020` | `7873835e3837d9358c355792808d3191a06c16f1fc880ca9626958d6ccef1e3e` | `8d09b7f211a1a9712cddbd771ddf0745f90da6302d8de03f76b3b4d604b8aca3` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0021` | `d9ead4161790a2353201b452d05690c0d7ed1cb7784698f21621b3a8b66e2301` | `35d0ce20d1ebd2bab51c513d851d66b003c0c7d20f9f7223c44aeb09e9282ebb` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0022` | `ef9aaea9423eddb64ee7ab83701de3b96e0b63d8b4eb9f127c9dcf6a6bfb163a` | `3c575b066e231bd48d43758bd9747ff6135c1bd3dbf0ec7ce38a739f41ecac2b` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0023` | `84ce0c943e5114835c085fe68e7e88ddbfe190a38f8046aee83a89995cdc8c28` | `77ea32d8bb178fb4a428b96df7f76a1d5fd756a6c03eccb9a413a7e32327bba1` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0024` | `ed01bfbb2eb2210abd0d456d1221328cc29b43e3617e6105f2a142659d540215` | `660c12022275b3da9f054ab9061691ac4771dfbf93f99c2afa14033dab76e332` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0025` | `c7d8a58a520d9bed9186c84a445ce80fa8dd9f00f6cffcec6d91d7481b85595a` | `f655e5e586387316569380b557e5a66a6ae5516ffb172bf2c005ee2e39129385` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0026` | `815d2563a6bdadb7bda0d40e7fc469a2dec40601e9f7e1b2e9108b8a66465e31` | `5c293dc92d982a75dee5d05b62536052ff54c127062c8b283b6fe06b7141f607` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0027` | `b5cf17030a86c8f46b88b5135ba5f8198c19016166c3749f4fec6c2c61e214eb` | `3be69abf44ea3cb01dde87f705eb4ea5392b04324e6d8affe4653484314612eb` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0028` | `58200944c29e61904b08aeb3b2b4271936e90eda9aa13844fe14012ccd0b3df4` | `351767f57d907d872dd4e1319f14a1c507f5d73da7e9f6a009a6a7a1c226dfb8` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0029` | `138f04c6103d6b575b84975b0ce24acf895e12abe29304aec1fd71886e7ead54` | `2ceb8c33ada2b0c83eac015a598efa934966b8c5ebda0cddf07cd104814f99f2` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0030` | `2a4eac38e2854382531e16a9f11671d625eec690c0e1daba32851558835f00e7` | `1bbc4d909b391ecf20d8a98c99b9bf214122c28b2f96cca6dbef38fc5d746d92` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0031` | `31a52b3df98a26d3b6b8a30754874e2187e6c5a83eac6884411d6da89de385ea` | `f2334441429a330ff1f91e380d28a3cc53b307c4c2a1c0ad88a7cc78d54661d8` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0032` | `068e6a6a8eb451ccde260f2d38aceab75f6870eef19074a7ef0c581c9892137c` | `6d8ebb0d6701f0b8b491a40d6a95ec0bc882a0ce8fdb89bcabc208adc403f592` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0033` | `0bec6f4215a1557cfa16a1d5fe96f8db2b8e3e61bde9abc54169cb4692de3a39` | `b1afb534547005eace86a1ec3c7378f87b0362dc866d5fc7a53a1e5d0489feda` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0034` | `849dcf7644754b0cefc9c9360679f855819b0a93d9b544d5f530ebe6940a8de3` | `9d071fb3ce099e2c712adf700427571996db092cf04a065614ec262459529c22` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0035` | `4c6529384ff7c570203f18cf857a5d2bfb5908d00d9f1b8526339d3dfb7335d9` | `d1f67a6f9fd581432c18b8dfe9f0791b11016404cc7ba60d578d6f23cec38d61` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0036` | `b60bbddab823eabd09091e0440936857440e25cf7e89d7e222c21de60a2536a1` | `62936b7ea3825130a5d6edbf37dc45246923488df493415964850ace9db91e32` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0037` | `d3c6c10d293d52352f7f16cb693fbd88842f77297fa5af01f7640f3962e3174d` | `ca677ac28639aef06965025ed30ef07a2e0579b16ffa7d131a247c3d0024841b` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0038` | `c953db2ea3d1ede62e6494bb0324405abd04fccb54f1f8b554126aeaed758540` | `d674533387dc8677187e860c1f8c772894ae25d0766c1908b8ac8f2fc856f25d` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0039` | `7741d512346a06240049ab6027deec0a4473e389bcbc3473829fad65111d4dcb` | `4968d0cfc60e5eb8d2fc8a4e8c202cd952bb8a09e5205c0d6036769f3c189a7a` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0040` | `3f44a05fd0c58885bca7e158b9c50dca0c52ff9b9e7520f967b90a529a816724` | `80356fc45c04a290cefda52eee584a90b883878a4245958fbb564ae6b1e5c3db` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0041` | `453da093451d42354444843c6d7f3ae2f4749f6460baf8eb217febd8c41849a1` | `b9d180315d9dafe85246dfa7a272ee7c9778d336a8e6c1551a7d3df2eaeb5b87` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0042` | `72a51a325ab7f57af8aaed440f79d7c99a5c5051aa17bbefb86555892b06a1f3` | `ea9057128a6ea9c17288d227972b04b33a4295cc64161db2a7a0cc0e09dfe8c1` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0043` | `5a6a599f96bdf038553ef9aa1a18ff8d085131c4fa2aa7b933220d77b0c41283` | `90e6b189932eee8969d9485821db85986389760937ed30336d86cf14aba04a6c` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0044` | `aa1533b0dcef0c7fdd130c440ca896e5e998b450034a0502a0154b7210aade9c` | `6847c571984a8a3c54e1b2e607d6ca2440b231b9bcc70e0d2e3766decd9fabed` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0045` | `d12337ac0dcbab6cd335112f4d51526c7de2e7b52fa37369368b0a130fb0b51c` | `575c5a918887e06215e368e6afb7e79938281e15dad6616ff4ff4e70de165ce1` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0046` | `52a1c335f04fcb604bf7f3ad9a62632e124ccb92e7dae802f33680bc38f8b6b0` | `ad1e7783c8d4623475ec231a8499bf4e13d6b8ed72f0238d714ce14df8ac3b5d` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0047` | `7c3744729d4e5b10bf6ef58912243de6a018fea6556f77a64d694159dfd8cb54` | `ff6290ded9f804e527a892886c2d06f2ed0ae30c4a0c94a50a06265eb6aa1a58` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0048` | `eb5eb3a25dd16a402d51fcacaf95a59e023408444497114279827e8ed76099d5` | `e254c7a0bdc481a630d475ae2deea9e0e80ff987d9a8e75f9fb3fcf0b832e186` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0049` | `d36db001833dd94c295fc7f867423864f7ac2947ce8a535fb1816ea43c8bd779` | `d0dabbd3517fa0d934d58eee2016ffc1ab60f5e7f89e8bfc17a80ffc6187e9b1` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0050` | `cc0a71d371522f98574f065c66fd03b4c9e52b331d31ad04d21076754db99023` | `16227d858ebdf4510c50fcd05496a29372a9230b74540a59cce38581652e98fd` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0051` | `dd0d633060ad37243eae1751c0688822dee643aed64d579caeded22a6105e4e4` | `8f71a388ee6304416deb59a3feab3d4dd54d496ff1cfb3db644f9eccb6c9a297` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0052` | `099d29a72968a74d790a397af6d21c5628a81e7560167546032058067b80af39` | `3e707593e7ce9f2792043b51cea313ddb87447c9779689cea7495e94ae305864` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0053` | `143d4a8c97e2b70eb2f89547d49e40492bf59882ceff3af2718225bd1ca28879` | `0c747e6f3fa0cb123f6829321d5bae39511beffa69775c788f14dfbe09f42ef5` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0054` | `40a49930f8aec7bbcbec14670667d1db7908756356199e2a05f597ea74710f1c` | `ff2daf1547abf264ab572a020f83d7933ce71ee284f087fa01dfa2a8ba7ba95a` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0055` | `6073f0d81c9a9b5959dff6964f6879d1ef8a8d29e36d4b75b8d5557aa635f1a3` | `697a0d5606803799de1a03b7505a4ab585f53e360eae9597e7a445b26fce2371` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0056` | `cc0489d8f179b7b6d16430d37c5c93a1193fe486bf72b9f685ffa9acdc67eb53` | `f57ed7613c63087ccd7fc9befbab8f6eac46adc2cd8ee19346f56b6e6b373592` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0057` | `cf6031fdb7f0767733613885fffeb3e2ac8e6bce27914de0f008436b074ab9b6` | `7422be860ad83131465f52177c3ccb34a9ab829d5bababceab0d3f81a2031553` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0058` | `7d39e1e292c3b8d1fb9f7699f20d2c25bc67124e7ca75032da29a03fe1907fd7` | `6f66ccba669ce67540c1ef0044cc1ce9ec5c58232e778b8981a69301fc54147c` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0059` | `93c815fa62fad1cdff0f08b301737140447f3883081dd21c00d60c15dee344d8` | `d6d5dbb810525819f095960a9343cba322f351e1d6ffcb739ec564e09292e07f` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
