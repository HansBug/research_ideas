# Phase-II final 60 组人工/LLM 对读模板

每行必须完整阅读 NL、作者最终 PlantUML、转换后 FCSTM、working contract 和 source trace，并填写本组特有的 NL/PlantUML/FCSTM 锚点、ownership/macro/capability 判断。存在 review obligation 的 case 还必须按每个 occurrence 的唯一 obligation_id 完成绑定同一 review subject 的第二遍复核。结构保真不等于行为等价。

锚点必须使用精确 occurrence 格式：PlantUML 写成 `source-ref:<raw_ref>|<完整 trimmed 源行>`；FCSTM 写成 `element-ref:<element_id>@line:<n>|<完整 trimmed FCSTM 行>`。裸 label、裸 identifier、子串和错误 scope/行号均无效；`source_normalization` 没有 FCSTM projection，其第二遍 `fcstm_anchors` 必须为空。

| case | review subject SHA-256 | working contract SHA-256 | verdict | notes |
|---|---|---|---|---|
| `0000` | `37f4521695506147565637dc024e47acc64e6dfdbf34945f566b4aa4d61b0e87` | `75cd2fc9bc520964648a90d51466a655af6c0fab3d43da30ee186f592e4735b8` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0001` | `5a75e91d7b8051be13e1e25b5b7a2899cbd13da6b7074267209d30f5651ee4a9` | `de60379e467dad70b045a74ef7e1571deca3f096df0986d3377d6410924050c8` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0002` | `6f7cdcb914ce6d0a2e77feed45044a2ebb268d03036a68f9ee8d435c95a35c4b` | `ee3947225dbe00a954701ba2777bb0af00b39f48cb79f1217e3550df5f47cce6` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0003` | `902d46df73efd19acafb8fae9cf1b880c69da07e48f2b35e2378f3da219e8ae3` | `465e81f08e401b24ea29477eaa076acb47962538182304de618ded04df05cee6` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0004` | `f1a41e12fc2f3a3329b50d5b90d49630023b52c5bb6d892ee21c1b488a723a37` | `0462f1e9d37daea4870eadc7c86a2a545ecc1d8fed27d8afd0d38067fe40b965` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0005` | `27a0530b88dee81e94d756fe187fdffbc5e123cb9d7a587879e04ac87ab948a1` | `61d11f0f08d17970172e1a54f2ee978b0c13d578d65eb7fa19ae9dcbf2991da2` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0006` | `ca73f03d595f27974b0ca009ca9fb633d1fea8791c03736ccd88fc152d5c5b40` | `7a0a928c30381d594256b75b9272ef4560bfd7fc2a4341d8d35d966ff674c67a` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0007` | `be8d7711ecd3a8c06a713d6ae83d1cc4c01adbbcea7640cbc677d0716fc9191b` | `2b0a34841a944fefced45e68c4ee804afbd64f0fff090f46790086d339b819f4` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0008` | `22dfa6ac59e45396d7326760a84c43d9ceb43f444e83345beb8ad9016ed8efb4` | `20f9f65dc7886988034833f7d62c07dd2671d8e8aff085fc13bff7bbfec8f31d` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0009` | `8ad4e53ae0e99ab315303ab667b4a24302fa9d005b93be439828529ac50eb89b` | `e2b079aa4c5052ee24cf74b39f9c7ffd1db732f6fce370e715f996077e42044a` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0010` | `e59e77e54e6e61afcb00b1ef0a8942676a470d476a18ca404c35236c933a27b4` | `fd91e33aa47bfd95866a328922e969c57bc5870c07ecf107d06bd39e2647901c` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0011` | `e8dae467545e868b37aa121dcd671f29f6a8e2dc050c2d7afb3424f227a89fbb` | `1a7eb46fbd9a1945794c7b7e289a9d541d57d6e599d9f6459c6f63e938f4b59c` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0012` | `7612eda19af14a43d6e653bf96fc3431809b05aef15eee14e2c3213f6f28ff3c` | `b959eaed789ea2b810af861fea7482e933ffa3cb443d7027b730d0d4e73093be` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0013` | `dd653fa7c013da4585eb77496c9b263f71823b592cb6da8ec02fda7a605232f6` | `e735aa4a26249cc5a485de1e7b692b37b37f552e59772c2c010287dac0911513` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0014` | `4e01052b25eff964d18988c6d0631b939c2e2356e95efea68ab39f3d319c090e` | `985d664900850742d8b296b978f5d9b8cf27ea67791d8969028ef9c1c21b10b1` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0015` | `037a08efbf1f5fe050d526a2cdd6d7321092f143df73f64869be85e7358108cd` | `b2a94ba54f9c36772bf6611b61fbb6cd333fc41b1c5227c6af4d3a3f4bec7cc4` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0016` | `d63342eca9d9c795d3bead4964c150a1955261ff5edabeae7a4bd289f91a3e8d` | `35a6bb56c2e9cd744213defe35c1e44e8284136460c34f189e4c54322de3632d` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0017` | `5245c77abe71502c913624cc5241963bafa62b6fb396315c13345512c8bca16b` | `ee9038ee5f1cef135bc45b2f4706b2021806e301a6ed31845b314dcc7d7d4e80` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0018` | `37d766f5cbacd80aa915cb05b6c35aaf10c2a2a642d65af4e0fd2b3be705f976` | `043dbfc2988d7a88281ac6e4463a6c92f0f09e5580b85697e009646333968fa4` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0019` | `f2e2c0ef03b6ee07b4179206ee1527e8a8b4d9488cacfaa1b96403341a8e3c78` | `f04aa780518d1098a11dd6e5347cbef410e60c6a126257aa112baa3d0a2af6d8` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0020` | `7873835e3837d9358c355792808d3191a06c16f1fc880ca9626958d6ccef1e3e` | `e76f50b2b0080f3c72e24231d39e996aa3391eca9993e41999665557d9f2b04e` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0021` | `d9ead4161790a2353201b452d05690c0d7ed1cb7784698f21621b3a8b66e2301` | `932ac7e3e52a233346f40c9cb81ee32a4923d7f671c8fb768222c686bb972c29` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0022` | `ef9aaea9423eddb64ee7ab83701de3b96e0b63d8b4eb9f127c9dcf6a6bfb163a` | `dbbd7e8f31d1ed3ddb868aa43b4c9d0e8a32bf4221fd8ed97d0dae998a7b17f2` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0023` | `84ce0c943e5114835c085fe68e7e88ddbfe190a38f8046aee83a89995cdc8c28` | `58338ab0a723d064d0beb2f26e5fa981e6fe7b6436fe658c4dd37de1d89229b0` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0024` | `ed01bfbb2eb2210abd0d456d1221328cc29b43e3617e6105f2a142659d540215` | `61749ff1b7a9ce31ef45623891e8d088a58b5cc3a7251d661c0930313a5118f4` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0025` | `c7d8a58a520d9bed9186c84a445ce80fa8dd9f00f6cffcec6d91d7481b85595a` | `a418c817b4cdb4e969ddb9461dbe6476fa60d27260a9d957137865e703acb720` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0026` | `815d2563a6bdadb7bda0d40e7fc469a2dec40601e9f7e1b2e9108b8a66465e31` | `164078530dee2e740504e46f9843b6ec27307e54aaf7883da8b9ec9eae394de7` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0027` | `b5cf17030a86c8f46b88b5135ba5f8198c19016166c3749f4fec6c2c61e214eb` | `fc147aa2e6e05029bce018869f4ef63d0f89ef67707e6414cecb183bf121e282` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0028` | `58200944c29e61904b08aeb3b2b4271936e90eda9aa13844fe14012ccd0b3df4` | `cb1a001ac54ed7182cfad2949a19027298601a25cc2820325128901c1fca8464` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0029` | `138f04c6103d6b575b84975b0ce24acf895e12abe29304aec1fd71886e7ead54` | `9715fab9fa4cfbe601497ac71f4456ec41dde88e4b8ddb345f3a513d08326721` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0030` | `2a4eac38e2854382531e16a9f11671d625eec690c0e1daba32851558835f00e7` | `08bebfe7a3e81c57d588a1917ae1954ac23b6ad990cba753cd6b5d8d0e00d2b5` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0031` | `31a52b3df98a26d3b6b8a30754874e2187e6c5a83eac6884411d6da89de385ea` | `0e1b784e488177f900997bdfef35d03e6613247e271366a0b0fa90bf2a90b79c` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0032` | `068e6a6a8eb451ccde260f2d38aceab75f6870eef19074a7ef0c581c9892137c` | `802af0dc9cbf313d0d15248928edc4cdf01c96f0d18785a72c0d94ae5a497f00` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0033` | `0bec6f4215a1557cfa16a1d5fe96f8db2b8e3e61bde9abc54169cb4692de3a39` | `9cde7260663205dcbcfd8f68f0a9f714be1dfe940c35b5acbd06fbef443af831` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0034` | `849dcf7644754b0cefc9c9360679f855819b0a93d9b544d5f530ebe6940a8de3` | `b0b922f200582715f04caeb7d1430b4deeb15e033e53e4ea335802c20eac0b15` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0035` | `4c6529384ff7c570203f18cf857a5d2bfb5908d00d9f1b8526339d3dfb7335d9` | `7437886fdcb010274f61c13cba145e7ed276d768963535c3947c4b1601fa5a5b` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0036` | `b60bbddab823eabd09091e0440936857440e25cf7e89d7e222c21de60a2536a1` | `30b7ebb6a662f1ba5285be27314001ccfb16a83a2d4028b634edf2ddfccf141d` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0037` | `d3c6c10d293d52352f7f16cb693fbd88842f77297fa5af01f7640f3962e3174d` | `48dc2c44440dd73ac0500d199544ae5b5e998edef45d5c7c70a3743097f00f57` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0038` | `c953db2ea3d1ede62e6494bb0324405abd04fccb54f1f8b554126aeaed758540` | `503072be107c63467da5ddc5ca6f08a3c3c43314e0e81c7fcd47c572d4aff685` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0039` | `7741d512346a06240049ab6027deec0a4473e389bcbc3473829fad65111d4dcb` | `09d74f888191a64d444a3f014952f1a14482c49a0f78a855d68bc61eff19ccc4` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0040` | `3f44a05fd0c58885bca7e158b9c50dca0c52ff9b9e7520f967b90a529a816724` | `52c1e41bdb3779023ec7ce42de280add2d20c51eb14ef7e0f15b62b979c58a3b` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0041` | `453da093451d42354444843c6d7f3ae2f4749f6460baf8eb217febd8c41849a1` | `bac4d94ae4c185c72eba4910dac801d426a7afeb83a23ea877a44b2e1dae2fca` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0042` | `72a51a325ab7f57af8aaed440f79d7c99a5c5051aa17bbefb86555892b06a1f3` | `27534550326e6bcd19a5e069b35ba999d7dcd6d6e5fc74a1605b19efe8848cff` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0043` | `5a6a599f96bdf038553ef9aa1a18ff8d085131c4fa2aa7b933220d77b0c41283` | `f878f528fd195be0dbfb8f457765a8c0b5ecb8cb65fb4364216428303f371244` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0044` | `aa1533b0dcef0c7fdd130c440ca896e5e998b450034a0502a0154b7210aade9c` | `ccfa96ce8c0569c8c8f473ca99eee5780f4cd83ceb97284b144c5b6c4f653eca` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0045` | `d12337ac0dcbab6cd335112f4d51526c7de2e7b52fa37369368b0a130fb0b51c` | `e73c158b6604ab4ebc35c747e91d39e988bf828637b3dbd961bebc8e15562642` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0046` | `52a1c335f04fcb604bf7f3ad9a62632e124ccb92e7dae802f33680bc38f8b6b0` | `aa668d55df04d4f9ed38c24fdc3fbf8a60be05fd1be00408aa6cd4908448653e` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0047` | `7c3744729d4e5b10bf6ef58912243de6a018fea6556f77a64d694159dfd8cb54` | `2470d4f546e33a91e62b34d3e16062cd7463bf0b804961b99dd6ca33256d6960` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0048` | `eb5eb3a25dd16a402d51fcacaf95a59e023408444497114279827e8ed76099d5` | `3da39694391f11f5bcdd2870125f64cc32819b3a036fff42e5cfca8a3817b626` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0049` | `d36db001833dd94c295fc7f867423864f7ac2947ce8a535fb1816ea43c8bd779` | `71ea2820e25f02dc1b9f0100c60c4b6623f2b8980f9bce87abf1a23da9199329` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0050` | `cc0a71d371522f98574f065c66fd03b4c9e52b331d31ad04d21076754db99023` | `c9a9f791897cdfaac696f9e6d65d05be0cb7313feb6d9415b614e99d5d8ff61e` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0051` | `dd0d633060ad37243eae1751c0688822dee643aed64d579caeded22a6105e4e4` | `286995081b02069eddc0362f78ea95e05178d686807eba6724408dd29edc2e99` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0052` | `099d29a72968a74d790a397af6d21c5628a81e7560167546032058067b80af39` | `e0431d76ffb27269a572e1d1fa79067d407bd46b819035b6b7fc5b5008a81114` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0053` | `143d4a8c97e2b70eb2f89547d49e40492bf59882ceff3af2718225bd1ca28879` | `521c40dc51f14623d080c754126fd4116731321b7b30a3537e5ba04f707e0af2` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0054` | `40a49930f8aec7bbcbec14670667d1db7908756356199e2a05f597ea74710f1c` | `89ac76d7ba5aa9b1ff91455642bca7650ebf25026baf6d27d3292aec7f0fe4a1` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0055` | `6073f0d81c9a9b5959dff6964f6879d1ef8a8d29e36d4b75b8d5557aa635f1a3` | `1391157ed74d96bc797bd0496044b349014bb2aa1cee16e3990c13fd4754e15f` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0056` | `cc0489d8f179b7b6d16430d37c5c93a1193fe486bf72b9f685ffa9acdc67eb53` | `bf440534016c2f18317d02ba47e27a7bab3a00940b827aa54dddbd36bc6df3b6` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0057` | `cf6031fdb7f0767733613885fffeb3e2ac8e6bce27914de0f008436b074ab9b6` | `1f51c7c77011a84e832ba07f0c330ad50db1c555c5827737615a015663c53592` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0058` | `7d39e1e292c3b8d1fb9f7699f20d2c25bc67124e7ca75032da29a03fe1907fd7` | `4e9cdf02e22b4dbd5a399381eb945eb003715d536c7e9a7255421cf7bc38a258` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0059` | `93c815fa62fad1cdff0f08b301737140447f3883081dd21c00d60c15dee344d8` | `5e549ade191b5157b46dc935eae1fdcf9dcdc133a730277aa04c7445212c0f28` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
