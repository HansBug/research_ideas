# Track C protocol hash drift resolution

Resolution ID: `predicate-gold-v1-protocol-hash-drift-3762-to-6d91`

Machine-readable record: `project_1_llm_state_machine_modeling/paper_stm_issue_discover/discover_matrix/ledger_v2/predicate_gold_v1/review/evidence_corrections/protocol_hash_drift_resolution.json`

Canonical resolution seal: `sha256:71e8d08145e4074fa2efe01638fe63768c3b36541bcbc9736199f82a1cf3baeb`

## Verdict

`PASS_WITH_LIMITATION`. The missing historical protocol bytes were recovered exactly, so this is no longer a byte-recovery failure. The recovered UTF-8 payload is 14,555 bytes / 241 lines and hashes to `sha256:3762ebf1a108c6e61e565c5e320de388c081f2ae50619863e089e2f680a70a57`. It is embedded as base64 in the JSON record so the recovery no longer depends solely on an external session artifact.

The limitation remains real: all 31 immutable packets bind the repository path `project_1_llm_state_machine_modeling/paper_stm_issue_discover/discover_matrix/ledger_v2/predicate_gold_v1/predicate_gold_protocol.md` to `3762...`, while that same path now contains the restored frozen `sha256:6d91c5d8d439b398764529f955da44a7adc1569becfb32e132479902863dab57`. This record bridges the historical content and current review evidence without rewriting any packet, review, receipt, protocol or canonical decision.

No v60 actual predicate/input/output was read. No provider, method, Judge or 54x3 run was invoked.

## Recovery audit

The Git path/history/stash searches found no tracked historical protocol. `git fsck` reported 4,808 unreachable blobs, 15 commits and 67 trees. The reachable/unreachable blob scan checked 51,533 blobs, including 7,971 candidates sized 10-30 KiB and 141,699,528 candidate bytes; no Git blob matched `3762...`.

Targeted repository, worktree, `.omx` and named-backup searches found no second matching protocol. One broad backup traversal failed after `/tmp/fuse` disappeared; this is retained as a search limitation.

The decisive scan covered 16 Codex JSONL logs that mentioned the path/hash. It parsed 2,531 candidate string fields totaling 45,010,820 bytes without JSON errors. Three mirrored fields at line 33 of `$USER_HOME/.codex/sessions/2026/08/31/rollout-2026-08-31T05-54-58-01a054ab-2873-76c2-aa47-fc28e80a9ecd.jsonl` matched `3762...`; they are one tool output mirrored as `stdout`, `aggregated_output` and `formatted_output`.

The contemporaneous repository record `project_1_llm_state_machine_modeling/paper_stm_issue_discover/discover_matrix/ledger_v2/predicate_gold_v1/review/horizontal/academic_review_v1.md` (`sha256:407355fa77bcc7401db3855e6007498a0eff5124efee3d0ac116ae810695d305`) independently records that `3762...` was observed at `2026-08-30T22:02:26Z`.

## Protocol delta

The protocols are not byte-identical. Current `6d91...` is 15,540 bytes / 250 lines, a net increase of 985 bytes and 9 lines. There are two changed hunks:

1. The old text already said a named leaf, `FinalState`, a no-outgoing state and whole-machine `terminated()` are distinct. Current text expands this into the precise distinction among enclosing-Region completion, all top-level Regions completing, immediate terminate-pseudostate entry, ordinary State exit behavior and pyfcstm `terminated()`.
2. Current text adds the bounded UML completion citation, corrects the Abadi-Lamport locator, and explicitly states that the effectiveness of the project review/control workflow is unvalidated.

The implication taxonomy, false-is-not-exact rule, typed-input rules, vacuity/contamination/control/replay gates, boundedness boundary, RTC rules and source-attribution requirements are unchanged.

Completion/termination semantics directly touch these nine affected rows: `DIFF-0010-08`, `EIS-0009-01`, `EIS-0009-03`, `EIS-0010-03`, `EIS-0010-04`, `EIS-0010-05`, `INS-0004-01`, `INS-0004-02`, `INS-0009-03`. The 34-row fourth review reread them under current `6d91...` and `fourth_review_addendum_v1.md`; ambiguity was retained and unsupported relations were not promoted.

## Affected packets

The two manifests and all 31 packet payloads validate under `TrackCInputManifest` / `TrackCInputPacket`. Across 691 artifact refs, 660 current artifact hashes match, 31 are exactly the expected stale protocol refs, and there are zero other mismatches or missing paths. All 124 JSON pointers resolve.

| Ledger ID | Packet file SHA-256 | Packet payload SHA-256 | Executed | Fourth-review status / relation |
| --- | --- | --- | --- | --- |
| `EIS-0002-01` | `2b39437353eb803f058491d9abd657da174486abe40e3235b00b604968de0976` | `867ac03e48c1e18b534d34cb1801f24016a69ab1b01c05e7c775b348f4cbc9db` | yes | `SOUND_FALSE_PROXY / O_IMPLIES_P` |
| `EIS-0002-02` | `9f09f332037e9f6fbcf1e80de252af68f36f2eec5130504e632aadfb78fd5d07` | `a50a6cbb73f3c6045085b6bc5a3fe3fc68c0b50ef72bd747676988cc6329cfe6` | no | `UNSUPPORTED_EXACT / UNRELATED` |
| `EIS-0002-03` | `49c10bbb5e8c6e7252fa5171676b65394a37acf8e919aaa727e2978b522f2925` | `4d2816ccfff37202a238ea8e839c3181d4f711e1e5a482b5c61184f32331d280` | no | `UNSUPPORTED_EXACT / UNRELATED` |
| `EIS-0004-01` | `4d69e4eef1f062e1857e46bb37c8393d4c859cc91d56928d94573744ceeea21c` | `6e3454ba6202c115ef9c47c13b030a61d479920be95ecb157ecd1bb645dd5524` | yes | `SOUND_FALSE_PROXY / O_IMPLIES_P` |
| `EIS-0005-01` | `237ce3e0e51250aacfe5889d1b2cd3a2dd8d2b165e0d3e70f55fcd1af0aa1fd4` | `1ef8ef40085fce6777e63fecc6c1f136a707c581010b53f11b3f260806827393` | no | `UNSUPPORTED_EXACT / UNRELATED` |
| `EIS-0005-02` | `d89d0b844c4477c2d5041a6b41982309031a8365bf33b276a5a689c85d069ce0` | `5269d6e02808bf204a8f10dedb2ad8e6ec5e1a6ba87da51b29d250db520a6564` | no | `UNSUPPORTED_EXACT / UNRELATED` |
| `EIS-0005-03` | `bb06a75c27426316e03ecde07c00dee8d879eb06e7779e123773b8eed7223366` | `71d76bccbfb5d2c2fcb64a52545bf86223df6cbc9d158f884055683a5fc061d9` | no | `UNSUPPORTED_EXACT / UNRELATED` |
| `INS-0001-02` | `73c7c90ce218d52b1b34b20e35ab202c455b125260f45586fbfc30684621b897` | `c2bdc4e456ae890f806cdbce28de6c3741786284d6c6b2ffe7d0dbcbd2d2fa57` | no | `UNSUPPORTED_EXACT / UNRELATED` |
| `INS-0002-02` | `7daaa8ebf2d68e576b5ec0ce52a3c0700926677f4048163ecb6a073af941a25c` | `53dc474a42d8f54aac276d26717778f50e6fd98b9ac355fa56e50a3efd8f0a93` | no | `UNSUPPORTED_EXACT / UNRELATED` |
| `INS-0002-03` | `bfc1b42fa6f1b0e2ce1363d656494a753839571abb53f5b586e5ac05e885b3f6` | `6969f33f65e60fd7aff90176b05aaf4e859d179685081b572b9a91db47cc54d5` | no | `UNSUPPORTED_EXACT / UNRELATED` |
| `INS-0002-04` | `4dc1ebc238cdc3a16b7759568069f29df2c3c25e8e2dbbb6384248144decf700` | `ce3504c57dd8b22270af5bd092f26b4c5458ed661f07384c0880a52e5299b2f5` | no | `UNSUPPORTED_EXACT / UNRELATED` |
| `INS-0002-05` | `dc8c559f535eeb2e4e98f0115765b1ad32afa18bfec13dd203b549e8d51e39d6` | `8f3576d1c6de19394ff38ac1d2d66ff93dbb369ffc38a73ece195df8d7e27520` | no | `UNSUPPORTED_EXACT / UNRELATED` |
| `INS-0004-01` | `284bd9a37b187429e60deaf53086a43f52bb9f900e0506f31c3ee3d24e7b15e7` | `7b54e68229f86d4fa14f4e9aa88674eaee07bfc8d06ece2bf4be07cda13763cf` | no | `UNSUPPORTED_EXACT / UNRELATED` |
| `INS-0004-02` | `ae937f487e767445278f4ea26f342aa201b625f24f942049de0bf2402c86b37d` | `b21e14aca7a719a51d1dd35de5aa61ff99a1f467e5c1f62db28b80cd51db0b44` | no | `UNSUPPORTED_EXACT / UNRELATED` |
| `VU-0001-01` | `cafdf9b70421aa9f5f786fdb1e36948193f7f7501c0f9a23beb7f606af67550e` | `eb064f6911061e21c249be6825025f340d7f5cbfc140bf19a226cf4c3996cf5e` | no | `UNSUPPORTED_EXACT / UNRELATED` |
| `DIFF-0010-08` | `c5dfaf5cad713c6a66c79e9bd8718e00eb101048fe63012a91a4d2cc49e3421c` | `e3d307e7fce6a30e03bd9c7c19fcdcafc6d0893f1dadf72584ccd2b305318788` | no | `UNSUPPORTED_EXACT / UNRELATED` |
| `EIS-0006-02` | `6c2d1eb5b46c02e62ebf6eb8d3c5380f118aecd70f3d974d688d2423edcd1902` | `56a79877557be4c85f1bdfbaede3ce90f4705840ac2cc4e61b77ad73d71ecc27` | no | `UNSUPPORTED_EXACT / UNRELATED` |
| `EIS-0007-01` | `692d930790f80f9d0cb1b2f4e9f89f840a06910581d419fd445db387f29ca258` | `b87a58870dbcb59af97d81d616fe3fa1e0858916db988555477e2be04f50f89e` | yes | `UNSUPPORTED_EXACT / UNRELATED` |
| `EIS-0007-02` | `baeb46e729bfdd58893cb793c0bd3804a6496ef8963e66f9d2977c7f6de1e09f` | `d8b508c20293a76921c40c9f1303a0b5f3489f8a4bcff54bea03d805c6b5771e` | yes | `SOUND_FALSE_PROXY / O_IMPLIES_P` |
| `EIS-0007-03` | `bce7baef264d006fba2686c73ec607f80f3b2be3c06f27e616aa9bdea3161471` | `94d317fe8112e3e722b7e760cba8f9854a68e8f37a62fca04b17320551057044` | no | `UNSUPPORTED_EXACT / UNRELATED` |
| `EIS-0009-01` | `22d9042a92c2c501daac07e03a427062baf7551b129a98a29cfc02822b7e812c` | `ebd766fe7e556c36c8938ef6943026274ce9fa02c4224a90bbf9400681fd24f6` | yes | `SOUND_FALSE_PROXY / O_IMPLIES_P` |
| `EIS-0009-02` | `285ba471de756fea740b68a7f62daf2945ccbeb2bcd30b244a7a17fd2adb23cf` | `ea3795b3d772ffa5f25c131bbe16667d92b309e13af7ca94bbfe4a48ea2e7cbb` | yes | `SOUND_FALSE_PROXY / O_IMPLIES_P` |
| `EIS-0009-03` | `341edeeecb70565fa87a782ac9bb78e4d3111f1e49921ca7fee53755f4adf684` | `f2fc707d6f538b4a55695160592621f286f6b60bcb6b648227edc74def16b2d2` | yes | `SOUND_FALSE_PROXY / O_IMPLIES_P` |
| `EIS-0010-01` | `f429a21a50594a6d0fea9ea3ee2f8215df14159ca9d2f53cfa34d800863481a0` | `4d86bf0b7b59094900aaaa82098eb059bc6a67c2f1b2e4e68c86039182f2c780` | no | `UNSUPPORTED_EXACT / UNRELATED` |
| `EIS-0010-02` | `84d9f98df010a88cb0e11c837c440bf6841e9c8796f4ba53c764f8b5f61d1bbd` | `a055562e6c26aa657a0c3cf87d83105c166dd1bd72595919964086726c80267f` | yes | `EXACT_FALSE / EQUIVALENT` |
| `EIS-0010-03` | `c2d0e80360aeb2ac225316cf86d83e9ed88c8e29c53641f38df606e223036fd3` | `7443c185b114f18dae65f733b9c05522de298b47a1baa74fdbc0b1725abeb94d` | no | `UNSUPPORTED_EXACT / UNRELATED` |
| `EIS-0010-04` | `18dfa3b20be403553d9b3bb7a84e95318e66ac85ce3012df2ac1244e9d179ded` | `47abb4dc4839ec5b8f7e2001ffd74ceafb05fc0d6de7a353b2e9fbe9bbde7714` | no | `UNSUPPORTED_EXACT / UNRELATED` |
| `EIS-0010-05` | `d961f577b0bdc6150b91d6c2a7d0474217575c7432c28408c2be1b8fba3e32b0` | `864703299235a6500c5acf23abb4236c3df746d93e701b09695577e38e2c6e7a` | yes | `SOUND_FALSE_PROXY / O_IMPLIES_P` |
| `INS-0009-03` | `00b39e0e31b442ca9c277a1799242093f103246708bbe4c7fec20acd584d2570` | `360ed9ca0de4a83290377896c864be6a58dccff1bd1a78c7ff107af8c7950126` | no | `UNSUPPORTED_EXACT / UNRELATED` |
| `VU-0009-01` | `f7cb1cf26409f345a2e4e9301ccf6569f0bd070bbb5b6643250fdcf9a5da0954` | `f9e56f40625716fe193079c81f8f13f827eb9e21a657dd530fc456020a8b043a` | yes | `UNSUPPORTED_EXACT / UNRELATED` |
| `VU-0010-01` | `24bedab4ba39b2e06369dcde491aa89980e419749cba1f606516acaa2b36cb39` | `a6fd0881759bfb9ae7a7e214afb1910948c7cf961fbac0d2a59459ea74d1a8de` | yes | `SOUND_FALSE_PROXY / O_IMPLIES_P` |

Status distribution for the 31 affected rows is `UNSUPPORTED_EXACT=22`, `SOUND_FALSE_PROXY=8`, `EXACT_FALSE=1`; relation distribution is `UNRELATED=22`, `O_IMPLIES_P=8`, `EQUIVALENT=1`.

## Impact by conclusion class

- Obligation: `PASS_WITH_CURRENT_REVIEW_CLOSURE`. The completion/termination clarification has semantic relevance, but the fourth review rechecked every affected O under the current protocol and retained all source ambiguities.
- O/P relation: `PASS_WITH_RECORDED_RELATION_CORRECTIONS`. The fourth review conservatively changed `EIS-0007-01` and `VU-0009-01` from historical Track C `O_IMPLIES_P / SOUND_FALSE_PROXY` to `UNRELATED / UNSUPPORTED_EXACT`; false/control/replay did not repair the missing representation premise.
- Execution truth: `PASS_UNAFFECTED_MECHANICALLY`. Eleven executed rows retain defective `COMPLETED_BOOLEAN=false`; 20 pre-execution rejections have no fabricated receipt.
- Positive controls: `PASS_UNAFFECTED_MECHANICALLY`. Eleven active controls retain `COMPLETED_BOOLEAN=true` and control provenance. Controls do not prove equivalence.
- Replay: `PASS_UNAFFECTED_MECHANICALLY`. Eleven defective and eleven control replay audits match their normalized projections.
- Transitive protocol provenance: `PASS_WITH_HISTORICAL_PATH_LIMITATION`. Exact historical content is recovered and embedded, but the immutable packet path/hash entries remain stale against the current checkout.

## Pane5 actions

Pane5 must cite the JSON resolution when consuming either affected batch, distinguish recovered `3762...` from current `6d91...`, and verify active A/B/C/O/property hashes before arbitration. It must preserve all semantic disagreements, especially the fourth-review corrections for `EIS-0007-01` and `VU-0009-01`, and must not rewrite historical packets or silently substitute the current protocol hash into old seals.

No further byte-recovery action is required. The residual work is arbitration and explicit acknowledgement of the historical same-path limitation.
