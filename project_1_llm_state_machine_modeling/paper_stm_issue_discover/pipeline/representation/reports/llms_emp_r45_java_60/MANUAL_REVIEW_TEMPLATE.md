# Phase-II final 60 组人工/LLM 对读模板

每行必须完整阅读 NL、作者最终 PlantUML、转换后 FCSTM、working contract 和 source trace，并填写本组特有的 NL/PlantUML/FCSTM 锚点、ownership/macro/capability 判断。存在 review obligation 的 case 还必须按每个 occurrence 的唯一 obligation_id 完成绑定同一 review subject 的第二遍复核。结构保真不等于行为等价。

锚点必须使用精确 occurrence 格式：PlantUML 写成 `source-ref:<raw_ref>|<完整 trimmed 源行>`；FCSTM 写成 `element-ref:<element_id>@line:<n>|<完整 trimmed FCSTM 行>`。裸 label、裸 identifier、子串和错误 scope/行号均无效；`source_normalization` 没有 FCSTM projection，其第二遍 `fcstm_anchors` 必须为空。

| case | review subject SHA-256 | working contract SHA-256 | verdict | notes |
|---|---|---|---|---|
| `0000` | `37f4521695506147565637dc024e47acc64e6dfdbf34945f566b4aa4d61b0e87` | `4725aa3a62ba15a48b606b98c0781a7dc7a5ec4fe3847daea9a1bbbb52130853` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0001` | `5a75e91d7b8051be13e1e25b5b7a2899cbd13da6b7074267209d30f5651ee4a9` | `6041ff51f90e93596d2352026bb69eb9f3e7a4efbffc7cd93c85723902abcf46` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0002` | `6f7cdcb914ce6d0a2e77feed45044a2ebb268d03036a68f9ee8d435c95a35c4b` | `a6edb19ad5cb43ac61057ce03c9efaa4e8c6c65e29fe482a94a20ff20fbe1615` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0003` | `902d46df73efd19acafb8fae9cf1b880c69da07e48f2b35e2378f3da219e8ae3` | `82d93410e67c65b8e0d6607c635e6d83d2a8c19aca9be87f8ac42fdac38a4a7d` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0004` | `f1a41e12fc2f3a3329b50d5b90d49630023b52c5bb6d892ee21c1b488a723a37` | `10e3079c7fe3696701cbfb6631b18d74a65faf96385aa8ce851dcea461a24e0b` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0005` | `27a0530b88dee81e94d756fe187fdffbc5e123cb9d7a587879e04ac87ab948a1` | `d1c1b710f8e7d6f0e646aba8e3b72fc53087de1a5c7daea9ece190170c0f6131` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0006` | `ca73f03d595f27974b0ca009ca9fb633d1fea8791c03736ccd88fc152d5c5b40` | `0fb657ea9212a439930a96773aadce046b8893ac3e0002e95634d557154be0e7` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0007` | `be8d7711ecd3a8c06a713d6ae83d1cc4c01adbbcea7640cbc677d0716fc9191b` | `5742d5eaf38a232a497d68bc1b79344452df86b25e2b9b4cf0255ba3234a75eb` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0008` | `22dfa6ac59e45396d7326760a84c43d9ceb43f444e83345beb8ad9016ed8efb4` | `087c459b267de95ec8b1a7489ea7c1045da206b1decfc6f80c34192a887c0343` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0009` | `8ad4e53ae0e99ab315303ab667b4a24302fa9d005b93be439828529ac50eb89b` | `052a603b604fce8c75da03766a94dcb5a5437ed4a53409fa6f4168f4486dfbf0` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0010` | `e59e77e54e6e61afcb00b1ef0a8942676a470d476a18ca404c35236c933a27b4` | `e3a1249f1b1f9109e4d0569389ff373b5f26f7c92165b63c3c95f1c299fe264b` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0011` | `e8dae467545e868b37aa121dcd671f29f6a8e2dc050c2d7afb3424f227a89fbb` | `044d2df104cfbab377987133e6dcfa73b657a41009db09725108cbfefd2caf40` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0012` | `7612eda19af14a43d6e653bf96fc3431809b05aef15eee14e2c3213f6f28ff3c` | `a20ddbdce3894de14fb22a8814d4cf67fbb09db904aab79409933e07830409b7` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0013` | `dd653fa7c013da4585eb77496c9b263f71823b592cb6da8ec02fda7a605232f6` | `8a022378a6def5b70cba9ac188b5d6fe50e9f0d0d8d747873e13b7cb4833f698` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0014` | `4e01052b25eff964d18988c6d0631b939c2e2356e95efea68ab39f3d319c090e` | `3e580936e0365a9c3d3ce0504fb82332f3c01cfffd5574337169684a6e96ead9` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0015` | `037a08efbf1f5fe050d526a2cdd6d7321092f143df73f64869be85e7358108cd` | `155f912178b5a5169392356032e52cfe07c7c7ec1460d2c0871b8e8e3033c460` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0016` | `d63342eca9d9c795d3bead4964c150a1955261ff5edabeae7a4bd289f91a3e8d` | `09d5eedfb84e75408e349f96158172d02ce168a68fdda752a1e5fe6dbdff19af` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0017` | `5245c77abe71502c913624cc5241963bafa62b6fb396315c13345512c8bca16b` | `abb8bacb961d3bfa42581e4fdfa01dc767515b3c04c88275b6b5247d70135a44` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0018` | `37d766f5cbacd80aa915cb05b6c35aaf10c2a2a642d65af4e0fd2b3be705f976` | `e225d2fd5ef07ad495dbba5d096552738ef690ef26cf80fdc1624e966dc1168e` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0019` | `f2e2c0ef03b6ee07b4179206ee1527e8a8b4d9488cacfaa1b96403341a8e3c78` | `016c047647c2cd7dd83882ad580457a14c235806a3e4c8b0bdbcd0e89900e26f` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0020` | `7873835e3837d9358c355792808d3191a06c16f1fc880ca9626958d6ccef1e3e` | `d3cb345779790cc65f9a044c746b69e3e5f8cc50261d6c4a99c7ad258c3116e0` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0021` | `d9ead4161790a2353201b452d05690c0d7ed1cb7784698f21621b3a8b66e2301` | `2c645b2f5e984b78c88c8b433e50031316d7edb76796829ef8b9809b54fbd11a` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0022` | `ef9aaea9423eddb64ee7ab83701de3b96e0b63d8b4eb9f127c9dcf6a6bfb163a` | `c3a9b9558ccb13bcfae9cd0a3f4a9e230a11e53845caba0bf028a87a5eb1738b` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0023` | `84ce0c943e5114835c085fe68e7e88ddbfe190a38f8046aee83a89995cdc8c28` | `301c1d42f9155a05776ac27695fac02a17dd2ce804bb445687c6bd842681be29` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0024` | `ed01bfbb2eb2210abd0d456d1221328cc29b43e3617e6105f2a142659d540215` | `265431d4433b343cc4391ed9f33304bc96317d68fccfa9822b6da04a1d9d6a70` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0025` | `c7d8a58a520d9bed9186c84a445ce80fa8dd9f00f6cffcec6d91d7481b85595a` | `14e913ffe55c05baef045dccb1cce25857b94af2c941c81ae7f94d2571081fee` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0026` | `815d2563a6bdadb7bda0d40e7fc469a2dec40601e9f7e1b2e9108b8a66465e31` | `223a1dacdbbe76957070fdd9f7c70dbc6d0cb1f75636c49f558d36c51b0af13d` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0027` | `b5cf17030a86c8f46b88b5135ba5f8198c19016166c3749f4fec6c2c61e214eb` | `f4b02459fb6d94366f1a9da708121e3ba1f655e6a18cd08ddf76a1c4b2c1e5e9` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0028` | `58200944c29e61904b08aeb3b2b4271936e90eda9aa13844fe14012ccd0b3df4` | `ec8bc7697ad89b1753ea7fd4f2f3f5ac980a639a0f4e7be6f1a28f4e8293ee23` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0029` | `138f04c6103d6b575b84975b0ce24acf895e12abe29304aec1fd71886e7ead54` | `06cfef2d11ec2794ac2dac9435f8bf999c32f3c0802bc9a91dd362002c5b4134` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0030` | `2a4eac38e2854382531e16a9f11671d625eec690c0e1daba32851558835f00e7` | `b67429715bc5cf6dc3d5847808693a03f32b14e19457c56ec0756fcefdbee95c` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0031` | `31a52b3df98a26d3b6b8a30754874e2187e6c5a83eac6884411d6da89de385ea` | `954b1920912a71510e8f063e7aabe1fb1c72d7a0d465d064cba8915fec97735f` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0032` | `068e6a6a8eb451ccde260f2d38aceab75f6870eef19074a7ef0c581c9892137c` | `494daa1bee278dc4b1450b6ff67eb1584624bd35673b34012a66d7df50b80d6c` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0033` | `0bec6f4215a1557cfa16a1d5fe96f8db2b8e3e61bde9abc54169cb4692de3a39` | `788c7d2e38b8143e5f9ab599c5b7198e8be6c04b5f4fc028e4189403cf62d512` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0034` | `849dcf7644754b0cefc9c9360679f855819b0a93d9b544d5f530ebe6940a8de3` | `916db7252b7d57f19071e854d6e95704d22ce2fd3ed51566cba3ba56a063ec83` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0035` | `4c6529384ff7c570203f18cf857a5d2bfb5908d00d9f1b8526339d3dfb7335d9` | `7a8dd1c1db9d3476a7251998e6e30debaa09264fc77170b09bf8ca4fada8d695` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0036` | `b60bbddab823eabd09091e0440936857440e25cf7e89d7e222c21de60a2536a1` | `51e084270ca61e09ffc3ed75ef7617e9e7bfba876dd6ca41719e662a9da25d2c` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0037` | `d3c6c10d293d52352f7f16cb693fbd88842f77297fa5af01f7640f3962e3174d` | `e805400458d9d3a7aff5cb53e0d62d1f58d2e006857181cdcf71173cbcc50abb` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0038` | `c953db2ea3d1ede62e6494bb0324405abd04fccb54f1f8b554126aeaed758540` | `d14d770bc6fde5d91754169f5624e957511d66cd29b25693ab947f648f2208e4` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0039` | `7741d512346a06240049ab6027deec0a4473e389bcbc3473829fad65111d4dcb` | `f0dd2f9f9e88eb2e6c5fc1bb68e9d69b7eecdd926b34837f45ced6c32e56afa7` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0040` | `3f44a05fd0c58885bca7e158b9c50dca0c52ff9b9e7520f967b90a529a816724` | `9dc54ad091efd0c21bb7580bddb41c5cb9e83d35a5cc92842138e04a5ef4ada3` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0041` | `453da093451d42354444843c6d7f3ae2f4749f6460baf8eb217febd8c41849a1` | `df1a12bf88860ddbfbe9653b521e63da9995c64e01df83ba74f933903f5d07f7` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0042` | `72a51a325ab7f57af8aaed440f79d7c99a5c5051aa17bbefb86555892b06a1f3` | `fd8637394a7f038c89d8a19c345fabb7ad13b8d2bfa2d3ceae205ae3fcc2eab9` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0043` | `5a6a599f96bdf038553ef9aa1a18ff8d085131c4fa2aa7b933220d77b0c41283` | `9e9a93605ad148bcb6f694841a234c83b64b8397860244eaf263d97ed456b12f` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0044` | `aa1533b0dcef0c7fdd130c440ca896e5e998b450034a0502a0154b7210aade9c` | `146627c3a8da1bbd58a3bb326a4645712fd70c9a9bec7f56cd066f0ea3e17e4d` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0045` | `d12337ac0dcbab6cd335112f4d51526c7de2e7b52fa37369368b0a130fb0b51c` | `8f600a640d589888754a15c9da43c55876f8c2f5d7a99d86636ac05eb82de53e` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0046` | `52a1c335f04fcb604bf7f3ad9a62632e124ccb92e7dae802f33680bc38f8b6b0` | `561776b09bfc37c82d29e01b3bd0dff987d5f74139891c317bab8e2ed4457fa6` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0047` | `7c3744729d4e5b10bf6ef58912243de6a018fea6556f77a64d694159dfd8cb54` | `08b8eb653b0c61222d7b8301331d0b7209016610468f8d80d54faf640edc3cb3` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0048` | `eb5eb3a25dd16a402d51fcacaf95a59e023408444497114279827e8ed76099d5` | `7c3d19a6cd5308868d4211654cb49b18105b233f3d6bf23fc4c50262f8a86ef2` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0049` | `d36db001833dd94c295fc7f867423864f7ac2947ce8a535fb1816ea43c8bd779` | `c03e72fda83d466699c7f76f7218578d483e9607aed702bc483671052488f5c5` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0050` | `cc0a71d371522f98574f065c66fd03b4c9e52b331d31ad04d21076754db99023` | `be5738c77b23064b0b429c147d0a33f4a1bd12cae2326a643f81443c55f21eb1` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0051` | `dd0d633060ad37243eae1751c0688822dee643aed64d579caeded22a6105e4e4` | `a89491268e167ec0b9dc876c87d0c4335aa186acffb08367daf11b4fbb0730ce` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0052` | `099d29a72968a74d790a397af6d21c5628a81e7560167546032058067b80af39` | `7e97dc93ff04abe24b894423d4e71bb193ff4ff6ffe0b87850e8db649836661d` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0053` | `143d4a8c97e2b70eb2f89547d49e40492bf59882ceff3af2718225bd1ca28879` | `daedf6474f76665026eb5892c6ae12b53a1f600923777aadfc93ab6129c2afdf` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0054` | `40a49930f8aec7bbcbec14670667d1db7908756356199e2a05f597ea74710f1c` | `fe344521708fdfd8f90dd1cac834eb6625b9d4677d330dc868a29d4b9783d564` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0055` | `6073f0d81c9a9b5959dff6964f6879d1ef8a8d29e36d4b75b8d5557aa635f1a3` | `ad3ea812bb5c42cc80aa831c9a1e97199284cc5fd3d0db073028aa3ac1c8c416` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0056` | `cc0489d8f179b7b6d16430d37c5c93a1193fe486bf72b9f685ffa9acdc67eb53` | `4d66cc1a7fc67d91aa8bc5ddce1fbf911e154c3c5bc892cc24bfe7dbf41c378a` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0057` | `cf6031fdb7f0767733613885fffeb3e2ac8e6bce27914de0f008436b074ab9b6` | `dd77fb81460bb9387854f420c1e3bc20da36f5b006b835d9130cdbe30cb40991` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0058` | `7d39e1e292c3b8d1fb9f7699f20d2c25bc67124e7ca75032da29a03fe1907fd7` | `a3d3eae45e7ee24946bfd1bb9fbe5edf14e704e73c14a89f8825edffc2f9180c` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0059` | `93c815fa62fad1cdff0f08b301737140447f3883081dd21c00d60c15dee344d8` | `0ba02880ce0f1718de3720821f4ed407a98cd116a1d534d2f397db4e1a6b04fa` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
