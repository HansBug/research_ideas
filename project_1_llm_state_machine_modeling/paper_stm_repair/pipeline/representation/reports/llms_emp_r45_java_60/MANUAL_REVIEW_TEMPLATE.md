# Phase-II final 60 组人工/LLM 对读模板

每行必须完整阅读 NL、作者最终 PlantUML、转换后 FCSTM、working contract 和 source trace，并填写本组特有的 NL/PlantUML/FCSTM 锚点、ownership/macro/capability 判断。存在 review obligation 的 case 还必须按每个 occurrence 的唯一 obligation_id 完成绑定同一 review subject 的第二遍复核。结构保真不等于行为等价。

锚点必须使用精确 occurrence 格式：PlantUML 写成 `source-ref:<raw_ref>|<完整 trimmed 源行>`；FCSTM 写成 `element-ref:<element_id>@line:<n>|<完整 trimmed FCSTM 行>`。裸 label、裸 identifier、子串和错误 scope/行号均无效；`source_normalization` 没有 FCSTM projection，其第二遍 `fcstm_anchors` 必须为空。

| case | review subject SHA-256 | working contract SHA-256 | verdict | notes |
|---|---|---|---|---|
| `0000` | `8c40455bfdb2cfa75954abd5289213b9e9d6903aebb5bdeab83ec1290da16f2b` | `ddd077c8b008bb2f7c22071c76730b52c01f5add3bd6dbb91eb5645467da79bf` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0001` | `97324eac6a64ba8cdeee02ef1a773b7172d770952f62c73f7696912bb1bbaea1` | `568ff874c5e0d79aee5bd9ed5ae20faa976881be49c203f0f7894567bd263026` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0002` | `6e0fe1a12ac509e7a17b22310778b0ed913c1004c21410c74b8038b2b404200f` | `f526a97aaab6cbcd5a9216244cbe49f9421129db62d6a11b8c082e71b655537e` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0003` | `8219b2d0672651990952a7478bd8f04ed6336178722b920fff814d06d694fa2f` | `4ce639243a209d377cf7e89001eca527751e67d1f984beab73834d784c478477` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0004` | `f8a60e145bb15ad83720de6349669e10f08239f84bf12f39523713ad9054fc61` | `de91cc1527087902fabe8ee14353f2d42b681dd7c98af5f68ff3d8668b0de02f` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0005` | `e19cbe55eeca2d8b18cf23a0652e77262ad20bfde2ed709af8189c7a701c33bc` | `21ae607d4768c0b9992bb2f323ff8fd3ed7c14166e070349be42e3ddc24bd5db` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0006` | `2e892c20bcf1471422078729b10410350a36e4bc3861ec1f52fbcc84a33daae8` | `6a2510df99c74db3580d41a3ac680bdc7eeffa86e8f44cb598e0806d6f848aa9` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0007` | `d2283e40bc3ff4f691399bf1c785376f544d9376b2125f61c3792d93692fe25a` | `8edb66844fb74fa309a4386c08f3761f6a801ff2794b577b1a81b9f6c3f7bcc6` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0008` | `be8362a96529e8ab5b1755dc76eeb9bcf13bedbe1c229f39d7410087b2f795da` | `24cfd149eed906f0005f762bd1b8c9ea29089028ded93b74bb4a9b7f6c2c0f8c` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0009` | `2ed7b00b25f152a42980cce69f0ad76baf1862bc4ec78c4415c3ba47d9d07a0e` | `e9bdf234c932274a05cb36cfe8147b9836b1821e0d0d373e4f7f87a9949ffd36` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0010` | `69cf1a3da87360d753fc325325c6d103f5e4cde1cfb90a2d55b18163e7c447ad` | `22335a3b221d0b4d30f3f270fb87ecf5667e9b92e7155aecb23afe370cac05b3` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0011` | `142d605ff34bc8438cb92dbcd957c39dbb25c23f74e1977e0c1796592e3c1f46` | `51e06c3e8bbc18f4da515828a973b7cc4172a4cee9ae1230ddc3bace408f60cf` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0012` | `d379b17978948c310268650942c78e89ade83e87d7b909154ae5d3710dc1931e` | `76a9938d67ea025282403c2ab8a36dc545bf1bdbefd25a430f5b3be47315269e` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0013` | `a8ba59336316a24da4b79572ef3bb306d94c3ddbc3714fec0c9b45fd882ca157` | `cb820a94ef20aa151298a7dcd3621814bdb89bdb2b3447f41ba83c7a8ce63b9c` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0014` | `531a165c061ac679c4fa399b1f3c3dd4a6be0c6118ea16fd42a6e35b7a1c6ca7` | `c30306adc0948e55fce48ee85e818037d103618e76616b72a57ec8d69e89704e` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0015` | `20f880cde350fead6637f5280ee44e9ff18e819b8d4339c29401e9abc16d623c` | `6ee5ac1b90472f04cfb9b2a7407fe1a5e91bebdab1ebbb256efe3dc89c845ffe` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0016` | `70d87f995697ea07cdde28095edf6ebb8380975ab2fe5e3d5dcddca1c5a5a86e` | `97e49e326d6e0bdee252c0cac204ecbbcfbe78c737b22bb72c0fdd7c71d7eb35` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0017` | `2cf55979aa98b716b0f7c55c0bcd98cb267c2aba139ce87d7ba383eceafc0b86` | `d0e6c4b889f207b33ea09ce4814006dbc230350388e7363ab3f80afe63d72b8e` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0018` | `374fa113f128bcfdabfb55c789c13298855d06a90170fa5cf54062589361b109` | `6a943223c467289d167a9fce99aba1d75f3b749419a77e6698b30b8908d32fc4` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0019` | `580b4757e16b2fb950ff8085d35740a1f663e340b7c8f8c4b95264a61e64bc7b` | `86c116c805c134a9ed4cbca9910bd8c76138c35296e6d331d0dbf2db972a28e1` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0020` | `a9ae7d5c857e382e949180d49b420ae83ca9cda95d78aab7394c6008554acd2b` | `fc88b100ae5e22121779c26cbee554c4d097aae1e3e2c2118caef8b5367bfd23` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0021` | `5f2138c5064fce6cc4cbae8a6b2ff843f6cf4e51d24e9bf2400c9437fd402d20` | `3ac8d818baebae6ea19998d59f1482e58588ae8618f3abeff145dba96421d2b7` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0022` | `007d8037868666abd610eaabe09638934482407c1036dbcfecee34632ae3ef8e` | `e76dde804d6fe009128ed262e9354e8441443e19b2ebefbdeffa6fe406228a4f` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0023` | `226521385197d27629587e14f097d08a794f72d55c1f7cae3371fa2448b2ebfa` | `6886e7279b1f19d9a0ac6c25fb46471643a249b31846e3922a58f47933909c3b` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0024` | `b70c2aa8cba5d64797dc8f2dafa2d43ffd7c974ab960be19bf39d0497f21d9ee` | `592e4be47720c9a7bc0d8f190a2532c057f36de35fbe07b868a2a1850a9d98ad` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0025` | `cc7c28c2f9f196271f6761a29d19f2e6beba3364f899c6b060a7fddb819550c5` | `df0f6c78d09e3e26ca4dc61f4fe82b9918130c10eb9bf8573c76da26b5d0a377` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0026` | `8de6eefdc01ec526a86f215acc08d44da9fab078f30ca4353bd6975e1199c9d1` | `b372b9c77c599cf6df9b3cb5bd63a470c0aaf61d6878b13a192ed6bc2b93c503` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0027` | `8ce3efebe032ebdba7f8fb010342496e5de3739aa3ad656e72d9490d32292fdc` | `93c5d940c34edc011d3507310db2e823e9c540dcf455c181cde715ee967c7959` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0028` | `a5890bc4af94c1e6e75a5f9a607b9ac5c39b1bec7392f58b1a1fc38019701140` | `4388cdb78bae80b60a8e5a533b82f0d1993b4b5e57a760e46fcc2eeb2eb20a80` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0029` | `05bd2d27f0c11f09cd285b54011d6ae59f1f1b716cb6fbe55622f3dcf351026b` | `b0c10e15f1a3af9e28961698c6996406d9d6b6e9b0fe8cd0d4fa4d79875da2be` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0030` | `28fbd0eb49957fd0bd7cd939eba45bc24b3aa3053513cb258620bade78bcd6ea` | `da20f7129163b2a4ee561618ccda480b7133ff9f6edc55c03dec465cf17363c5` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0031` | `15d6817bdcf9c8cb268dfe0c94dda485002304e0c21416b8d8bc12b09b520a74` | `f88c242f0dae5a22a6899bc463cb8184850eaedaff00d27125425a02bc2c13d3` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0032` | `7dd5c07d51088b8bb92c768577436f393f35ac78a1acedf25ba0c207c68c25e8` | `b0717978e802b270b51497050e5da35c47bc358bf3edc4b98c6cbe058b6d074d` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0033` | `d869c69bf81f1b5aef1a576784142e6d9b8145e6a3fd8786fd11ca579e4d432d` | `c411914e0467e79f5c8cee9d026c495c031a64e086fe1718e72c75dfde5dda8f` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0034` | `eb4242a26f545717ffff244d93d1857d81b9a105536f6c7993df70d15cf87cab` | `9305f5e279885921a1aa335958415c4cc2607bcdd5838bcf728b04b5dd25bb63` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0035` | `b4cf36b91880a3fe07125811d28f4cd6e023e3b9125d3457c905a3ffc3ecf2a4` | `8dde89675a80c3eca2722dcaced0f875f9480d5ce1beea98abce6f6461429b7f` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0036` | `313f2940026f43f2ca49c8c77fd17711ee4872eb6552b384139874fed16ab0f1` | `660fe7d4339891fe7ba12b18cc95bc1a5df9ffffb6ab1126fffffbd6960d89b2` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0037` | `3fee53a8038a8952b219c1bb928b217936ba16c7f43f47a3f9f225900c280982` | `84128c1d52650829d2ea3104894e90e7cc67d545038dbe02b838d332a1624b49` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0038` | `dee3e732fbc6dd40b821cc2a7b41d32dd66dc5d69c05c7e016ef182360f5047c` | `dac7c81179825db9c92b0ca09ce4440f7750fa73dd3775f6f85c8cac583fcba4` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0039` | `2eeb169de2d28a284680426da60451a5430d45d27810a3411857f4c253fa5998` | `71e8c0192f3df4d8910b271f04d94be55661e16aa66fa680c2ee5f14593f0b53` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0040` | `a8d01a175feaea2270bd75f894c86dab79406b951713ff4dc634fa8ff63a5962` | `a1951a16b8cfb9c1bfef85cbda8c9eb2cb2956a5d7678504c0fb52e6b964df46` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0041` | `9bb4a90db43246fad84de236eb311ac72ae90b98040a3d966c521dfd3aeab2b2` | `a41d3c71b1dd78d3dd0e4e9f4a4cb276c1e9c9e70028477a22f364c5ea1763de` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0042` | `ed755b3246447e2916eb8a747b6f01fe8bd88a44a0b7dcbfba908c71ac6cf74a` | `e8f8d38c310d2a87f8e64d3857aa0557a93c1ae76e3d5f8b82aa7df655516fc3` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0043` | `7c4c56b54d00c14b12825a6aaccd1a6c7a35b156cb63fcf8b3084bdbd8833c0c` | `6bda71bb3a79dec67cece81d35e6fd7e21258ba566b1da9cc3debda2d487c468` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0044` | `88a1e1dee7901eeb358f35765f526401d82ada4ec044df3f0c84649367f4db1d` | `18f58b1d3274deadcf06beb977983d54654676473eed026479cadf308f73f7ae` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0045` | `c6d68adfdbd6114152eb113aa54491a3c7eb07afe45eea2022eaf363fadec898` | `64a92b6a1efd20a8edc62dd92b57537adcc14924af63f64685ac6341e7b1b5a4` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0046` | `4b6ad1c16fe3f9af1fcef278c2d4dfbb5ae45d31fbde325be2459e74a8384a7a` | `cf32dc7dcb75a451ecde7e98613137323d5cd31b84f3c8d42acf28911160af85` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0047` | `4623ec62d88ee7cdf07f8fb9efb507ea998d875bca3e5c203ab8dfc12c20847b` | `7abc3bd191e1871d10aef826223b3b5c804f80bc8d36b4aea1c37555f6c60def` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0048` | `95eb7e8d28f712b6950a940c30b283b00824a85ef8b1f05437bc4b4876c6c081` | `93249a2d509cd1b5d91b6b58c279f917ed381ee6015235e6144c10624a32469a` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0049` | `1d98df5c08a26698496f8a2bff58052249b50285fa1906a44fe335ae6662be6c` | `c949e4cead2e62d88fbac7de047c4bf351e2e023833e0b909ad5d1b1940beb01` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0050` | `ec9c8600cecdef753271fc081055ec7b6e79c58998d99f92ab107fa6fc39f3b5` | `5c6623b026f4db2845044bdc175c069d6004e443043529e52d87355cf5fcfddc` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0051` | `c39b789e502ec132df8339db290d54ae01599cb1c9964305c30cfea7b3c38db7` | `71cf98e7d7b2dc7b1c251155960123b4fe36d487d46207fe065b8a0d2a1d60d1` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0052` | `a40c100674aabaec42d0aa0bf12dbafd3cf2c9ad4064ce005b1b6126189945f4` | `5fe7894cfb06f12dfea539b87ae0aa803faa47afd4ce3cab42e9bf08932d2678` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0053` | `fbf24e016157c879f18f1d5f13cdfa25cdc2e885a8368c4b75096675a07e040f` | `075ebf408e1274171ff8a175d76ef0312b80432d300801c18af59a1e64701e3d` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0054` | `5e5ac531b1f680243539ffd3d6e532e77b2fc9646f05ff7ec952a21b9b6195bd` | `b57812811fb8951b6c8422d0d6b3673d7d2822b53938df5c5cf59ad1a324ab91` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0055` | `62e9174ac1282022823711b26da4fee7404cfe8ce1da0340eba50d598c378cc2` | `97fa1dcedc50319a4dc3534d1f724176bc249ee4b15ad399fd907942a81c9dfb` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0056` | `94d7c7f422e15210dc40322b8b5f4209deb3c87aa4a1eb516507def3bad0fa15` | `e23a550d0cb9f39fb5dffdb5436944a2f067e54ada1f9089ba89656c048d9cbd` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0057` | `0ddce51e4229947e16fe37d98fcbd3c8888f9efeac89e5988c317bbdea83237c` | `7c28032620af012fc9ace10b007c1bcc5484f2baaa5f244adcc99be05fff5f47` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0058` | `883b74b2e0906bcc730992056e9e9ea2b773f6f42506ddf56df45516d2e196d6` | `285987e443e9b0d0ab1bc2b8ada8e91cc402626dae5c0afb27719f4b66bc9e7c` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
| `0059` | `ff8d372d6142b3154302caa9edd73c77600a92395625d52cef762c26f05aa081` | `c0ac0c9013ce623ad18fee34bacaff314ab941f4a1e42ec8535d6ee05df68837` | PENDING | 待逐组对读 ownership、macro、capability 与三元组 |
