# Unsupported exact properties

本清单由 `predicate_gold_v1.json` 机械生成，共 98 条。这里的 unsupported
只表示当前可信语义能力不能给出 `O <=> P` 的可执行 reference property；它不否定
ledger issue，也不把 method 的 FULL/PARTIAL hit 改成 miss。

汇总分布：

- family: `EIS=60`, `INS=28`, `VU=8`, `DIFF=2`
- D tier: `D2=60`, `D1=38`
- L tier: `L2=29`, `L1=27`, `L0=42`

机器可读字段见 [`unsupported_exact.json`](unsupported_exact.json)；平面镜像见
[`unsupported_exact.tsv`](unsupported_exact.tsv)。

## `DIFF-0010-08`

- 分类：`DIFF` / `D2` / `L0`；final relation `UNRELATED`
- 最近 proxy：无可靠 executable proxy
- unsupported reason：Pane5 final disposition is UNSUPPORTED_EXACT/UNRELATED. Track C and the independent fourth review agree on this boundary. Track C: Track A leaves the concrete auto-final completion mechanism unspecified. O may be encoded by a completion event or guard, so it does not entail an empty event tuple. Conversely, an eventless edge may have a disabling guard or fail next-stable RTC behavior. This pre-execution relation/capability rejection supports UNSUPPORTED_EXACT. The portable packet contains no execution receipt for this row, and no execution is claimed. Independent confirmation: Independent fourth source/semantics review: Track A leaves the concrete auto-final completion mechanism unspecified. O may be encoded by a completion event or guard, so it does not entail an empty event tuple. Conversely, an eventless edge may have a disabling guard or fail next-stable RTC behavior. This pre-execution relation/capability rejection supports UNSUPPORTED_EXACT. The portable packet contains no execution receipt for this row, and no execution is claimed.
- capability gap：

  - S2 omits trigger emptiness
  - S3 cannot bind an absent carrier
  - G1 omits directness and events
  - the conjunction reading lacks multi-event semantics

- arbitration：`predicate-gold-v1:DIFF-0010-08`

## `DIFF-0039-04`

- 分类：`DIFF` / `D2` / `L1`；final relation `P_IMPLIES_O`
- 最近 proxy：无可靠 executable proxy
- unsupported reason：Pane5 final disposition is UNSUPPORTED_EXACT/P_IMPLIES_O. Track C proposed UNSUPPORTED_EXACT/UNRELATED; the fourth review proposed UNSUPPORTED_EXACT/P_IMPLIES_O. Pane5 resolves the difference as follows: One direct initial carrier is sufficient for a sequential implementation, but it is not necessary because the source also permits an orthogonal repair. Its absence therefore cannot falsify O. Fourth-review evidence: The root-count proposal is not equivalent to the disjunctive obligation. Exactly one root initial carrier is one sufficient sequential encoding, while an explicit orthogonal decomposition can satisfy O with more than one region-local default. Therefore P implies O for the sequential branch, but P=false cannot refute O; exact execution remains unsupported.
- capability gap：

  - Track B fcstm_sha256=sha256:2fa721d0da9e7405120700b5c47a0ec75f70959b672273c85f7aeade80de912c is the FCSTM_META file hash, not executable model.fcstm bytes sha256:fdc4158e2512976baba84cc46cd5eecc7691a4ba434eb7b0f4efecd68a1f0352; Track C rebinds only to the Track A hash-bound model artifact.
  - Track B relation EQUIVALENT is corrected to UNRELATED; a false receipt cannot establish equivalence.
  - Track B proposed execution, but Track C rejects execution because the relation, complete typed binding, eligibility, or frozen oracle contract does not close.
  - Chronology defect: Track A records reviewed_at=2026-08-31T15:30:00Z, later than this truthful preflight freeze 2026-08-30T22:57:54.218535Z; no timestamp is fabricated to conceal it.

- arbitration：`predicate-gold-v1:DIFF-0039-04`

## `EIS-0002-02`

- 分类：`EIS` / `D2` / `L2`；final relation `UNRELATED`
- 最近 proxy：无可靠 executable proxy
- unsupported reason：Pane5 final disposition is UNSUPPORTED_EXACT/UNRELATED. Track C and the independent fourth review agree on this boundary. Track C: With a faithful FCSTM topology, each feasible execution would imply its graph path and the three-way AND would be a sound necessary condition. The packet does not license that whole-topology representation bridge, so no O/P implication is accepted in the allowed evidence scope. This pre-execution relation/capability rejection supports UNSUPPORTED_EXACT. The portable packet contains no execution receipt for this row, and no execution is claimed. Independent confirmation: Independent fourth source/semantics review: With a faithful FCSTM topology, each feasible execution would imply its graph path and the three-way AND would be a sound necessary condition. The packet does not license that whole-topology representation bridge, so no O/P implication is accepted in the allowed evidence scope. This pre-execution relation/capability rejection supports UNSUPPORTED_EXACT. The portable packet contains no execution receipt for this row, and no execution is claimed.
- capability gap：

  - G1 is guard-agnostic and existential per target; whole-model simulation is declared ineligible in the packet metadata.

- arbitration：`predicate-gold-v1:EIS-0002-02`

## `EIS-0002-03`

- 分类：`EIS` / `D1` / `L0`；final relation `UNRELATED`
- 最近 proxy：无可靠 executable proxy
- unsupported reason：Pane5 final disposition is UNSUPPORTED_EXACT/UNRELATED. Track C and the independent fourth review agree on this boundary. Track C: No selected executable P exists. Global absence of InitialState neither proves direct-child set equality nor excludes another extra child; exact child cardinality is unavailable. This pre-execution relation/capability rejection supports UNSUPPORTED_EXACT. The portable packet contains no execution receipt for this row, and no execution is claimed. Independent confirmation: Independent fourth source/semantics review: No selected executable P exists. Global absence of InitialState neither proves direct-child set equality nor excludes another extra child; exact child cardinality is unavailable. This pre-execution relation/capability rejection supports UNSUPPORTED_EXACT. The portable packet contains no execution receipt for this row, and no execution is claimed.
- capability gap：

  - S1 admits only closed-model scope; direct-member cardinality is a declared non-predicate boundary.

- arbitration：`predicate-gold-v1:EIS-0002-03`

## `EIS-0005-01`

- 分类：`EIS` / `D2` / `L0`；final relation `UNRELATED`
- 最近 proxy：无可靠 executable proxy
- unsupported reason：Pane5 final disposition is UNSUPPORTED_EXACT/UNRELATED. Track C and the independent fourth review agree on this boundary. Track C: O can be satisfied by an internal Cancel handler with no DoorShut self-edge, so O does not imply S2. An arbitrary self-edge with another or no trigger does not imply Cancel handling, so P does not imply O. This pre-execution relation/capability rejection supports UNSUPPORTED_EXACT. The portable packet contains no execution receipt for this row, and no execution is claimed. Independent confirmation: Independent fourth source/semantics review: O can be satisfied by an internal Cancel handler with no DoorShut self-edge, so O does not imply S2. An arbitrary self-edge with another or no trigger does not imply Cancel handling, so P does not imply O. This pre-execution relation/capability rejection supports UNSUPPORTED_EXACT. The portable packet contains no execution receipt for this row, and no execution is claimed.
- capability gap：

  - No missing-edge signature predicate can compare a trigger before a carrier exists.

- arbitration：`predicate-gold-v1:EIS-0005-01`

## `EIS-0005-02`

- 分类：`EIS` / `D1` / `L1`；final relation `UNRELATED`
- 最近 proxy：无可靠 executable proxy
- unsupported reason：Pane5 final disposition is UNSUPPORTED_EXACT/UNRELATED. Track C and the independent fourth review agree on this boundary. Track C: V5 is bounded and forbids later legitimate opening rather than checking static ancestry; no requirement-relative containment oracle is frozen. This pre-execution relation/capability rejection supports UNSUPPORTED_EXACT. The portable packet contains no execution receipt for this row, and no execution is claimed. Independent confirmation: Independent fourth source/semantics review: V5 is bounded and forbids later legitimate opening rather than checking static ancestry; no requirement-relative containment oracle is frozen. This pre-execution relation/capability rejection supports UNSUPPORTED_EXACT. The portable packet contains no execution receipt for this row, and no execution is claimed.
- capability gap：

  - No ancestor-relation predicate; V5 cannot express only simultaneous exclusion without forbidding later legal opening.

- arbitration：`predicate-gold-v1:EIS-0005-02`

## `EIS-0005-03`

- 分类：`EIS` / `D1` / `L0`；final relation `UNRELATED`
- 最近 proxy：无可靠 executable proxy
- unsupported reason：Pane5 final disposition is UNSUPPORTED_EXACT/UNRELATED. Track C and the independent fourth review agree on this boundary. Track C: The source does not bind a variable identity/domain, exact action text, lifecycle phase, effect expression, or transition carrier; S4/S6 values would be invented and neither covers the full obligation. This pre-execution relation/capability rejection supports UNSUPPORTED_EXACT. The portable packet contains no execution receipt for this row, and no execution is claimed. Independent confirmation: Independent fourth source/semantics review: The source does not bind a variable identity/domain, exact action text, lifecycle phase, effect expression, or transition carrier; S4/S6 values would be invented and neither covers the full obligation. This pre-execution relation/capability rejection supports UNSUPPORTED_EXACT. The portable packet contains no execution receipt for this row, and no execution is claimed.
- capability gap：

  - S1 does not support variables; S4 needs exact lifecycle phase/action; S6 needs exact carrier and parseable operation; trace_variable_delta is a declared non-predicate boundary.

- arbitration：`predicate-gold-v1:EIS-0005-03`

## `EIS-0006-02`

- 分类：`EIS` / `D2` / `L0`；final relation `UNRELATED`
- 最近 proxy：无可靠 executable proxy
- unsupported reason：Pane5 final disposition is UNSUPPORTED_EXACT/UNRELATED. Track C and the independent fourth review agree on this boundary. Track C: O is a pre/post swarm-count decrease on every attack completion. No count variable, domain, decrement, source-backed effect, lifecycle carrier, or eligible trace exists, so no executable P is legally bound. This pre-execution relation/capability rejection supports UNSUPPORTED_EXACT. The portable packet contains no execution receipt for this row, and no execution is claimed. Independent confirmation: Independent fourth source/semantics review: O is a pre/post swarm-count decrease on every attack completion. No count variable, domain, decrement, source-backed effect, lifecycle carrier, or eligible trace exists, so no executable P is legally bound. This pre-execution relation/capability rejection supports UNSUPPORTED_EXACT. The portable packet contains no execution receipt for this row, and no execution is claimed.
- capability gap：

  - trace_variable_delta is outside the frozen registry
  - S6 needs one exact carrier and one parseable operation
  - S4 needs an exact owner, lifecycle phase, and action
  - the FCSTM snapshot is source-static eligible but simulation-ineligible

- arbitration：`predicate-gold-v1:EIS-0006-02`

## `EIS-0007-01`

- 分类：`EIS` / `D2` / `L2`；final relation `UNRELATED`
- 最近 proxy：无可靠 executable proxy
- unsupported reason：Pane5 final disposition is UNSUPPORTED_EXACT/UNRELATED. Track C proposed SOUND_FALSE_PROXY/O_IMPLIES_P; the fourth review proposed UNSUPPORTED_EXACT/UNRELATED. Pane5 resolves the difference as follows: fcstm_meta explicitly withholds whole-model behavior equivalence and simulation. G1 over the converted topology is therefore not a source-guaranteed necessary condition for the author-level activation obligation. Fourth-review evidence: Independent fourth review accepts the orthogonal initialization and re-arming obligation, but not an O/P implication. The three G1 clauses inspect guard-agnostic paths in the complete native topology. Because fcstm_meta explicitly withholds whole-model behavior equivalence, an author-conforming model is not proven to entail those paths in this representation. Defective false, control true, and matching replays establish only the oracle outcomes, so the conservative disposition is UNSUPPORTED_EXACT/UNRELATED.
- capability gap：

  - G1 omits events, guards, concurrency, and RTC timing
  - V4 checks generic progress rather than required recovery
  - V3 and R1 cannot be bound without a source-specified bound or schedule
  - orthogonal_runtime_configuration is a registry boundary

- arbitration：`predicate-gold-v1:EIS-0007-01`

## `EIS-0007-03`

- 分类：`EIS` / `D2` / `L0`；final relation `UNRELATED`
- 最近 proxy：无可靠 executable proxy
- unsupported reason：Pane5 final disposition is UNSUPPORTED_EXACT/UNRELATED. Track C and the independent fourth review agree on this boundary. Track C: Accepted O requires zero unsupported top-level functional subtrees and permits deleting OperationalControls. P instead requires OperationalControls to exist and be root-reachable, so an O-satisfying deletion makes P unbindable rather than true. Its cardinality conjunct also omits requirement-relative containment. This pre-execution relation/capability rejection supports UNSUPPORTED_EXACT. The portable packet contains no execution receipt for this row, and no execution is claimed. Independent confirmation: Independent fourth source/semantics review: Accepted O requires zero unsupported top-level functional subtrees and permits deleting OperationalControls. P instead requires OperationalControls to exist and be root-reachable, so an O-satisfying deletion makes P unbindable rather than true. Its cardinality conjunct also omits requirement-relative containment. This pre-execution relation/capability rejection supports UNSUPPORTED_EXACT. The portable packet contains no execution receipt for this row, and no execution is claimed.
- capability gap：

  - S1 cannot establish requirement-relative containment
  - G1 does not check containment or owner cardinality
  - direct-member cardinality is an evaluation-only native oracle
  - runtime orthogonal configuration is not represented

- arbitration：`predicate-gold-v1:EIS-0007-03`

## `EIS-0010-01`

- 分类：`EIS` / `D2` / `L1`；final relation `UNRELATED`
- 最近 proxy：无可靠 executable proxy
- unsupported reason：Pane5 final disposition is UNSUPPORTED_EXACT/UNRELATED. Track C and the independent fourth review agree on this boundary. Track C: Track A explicitly allows environmental Power On to initiate an unlabeled root descent to HumanDriving, so O need not contain any authored Power_On transition carrier. An arbitrary carrier from an unconstrained source to HumanDriving also does not establish startup applicability. This pre-execution relation/capability rejection supports UNSUPPORTED_EXACT. The portable packet contains no execution receipt for this row, and no execution is claimed. Independent confirmation: Independent fourth source/semantics review: Track A explicitly allows environmental Power On to initiate an unlabeled root descent to HumanDriving, so O need not contain any authored Power_On transition carrier. An arbitrary carrier from an unconstrained source to HumanDriving also does not establish startup applicability. This pre-execution relation/capability rejection supports UNSUPPORTED_EXACT. The portable packet contains no execution receipt for this row, and no execution is claimed.
- capability gap：

  - S2 needs a source endpoint
  - S3 needs a chosen carrier and checks no dispatch
  - V3 needs a bound and initial scope
  - R1 needs a complete schedule
  - event_consumer_exists_in_scope is not frozen

- arbitration：`predicate-gold-v1:EIS-0010-01`

## `EIS-0010-03`

- 分类：`EIS` / `D1` / `L2`；final relation `UNRELATED`
- 最近 proxy：无可靠 executable proxy
- unsupported reason：Pane5 final disposition is UNSUPPORTED_EXACT/UNRELATED. Track C and the independent fourth review agree on this boundary. Track C: Track A adopts stable absorbing shutdown and retains formal UML termination only as D1 sensitivity. Stable shutdown needs no authored root-exit carrier, while an unrelated root-exit carrier does not establish Power_Off shutdown. This pre-execution relation/capability rejection supports UNSUPPORTED_EXACT. The portable packet contains no execution receipt for this row, and no execution is claimed. Independent confirmation: Independent fourth source/semantics review: Track A adopts stable absorbing shutdown and retains formal UML termination only as D1 sensitivity. Stable shutdown needs no authored root-exit carrier, while an unrelated root-exit carrier does not establish Power_Off shutdown. This pre-execution relation/capability rejection supports UNSUPPORTED_EXACT. The portable packet contains no execution receipt for this row, and no execution is claimed.
- capability gap：

  - V3 cannot bind terminated()
  - G1 discards event and termination
  - V4 generic progress is not termination
  - no source bound or scenario

- arbitration：`predicate-gold-v1:EIS-0010-03`

## `EIS-0010-04`

- 分类：`EIS` / `D2` / `L0`；final relation `UNRELATED`
- 最近 proxy：无可靠 executable proxy
- unsupported reason：Pane5 final disposition is UNSUPPORTED_EXACT/UNRELATED. Track C and the independent fourth review agree on this boundary. Track C: The accepted disjunctive O requires handback from AutonomousFinal but does not specify whether it is completion-event, guard, or automatic. Empty events are therefore not necessary, and empty-event endpoints alone do not exclude a disabling guard or establish RTC response. This pre-execution relation/capability rejection supports UNSUPPORTED_EXACT. The portable packet contains no execution receipt for this row, and no execution is claimed. Independent confirmation: Independent fourth source/semantics review: The accepted disjunctive O requires handback from AutonomousFinal but does not specify whether it is completion-event, guard, or automatic. Empty events are therefore not necessary, and empty-event endpoints alone do not exclude a disabling guard or establish RTC response. This pre-execution relation/capability rejection supports UNSUPPORTED_EXACT. The portable packet contains no execution receipt for this row, and no execution is claimed.
- capability gap：

  - S2 omits events
  - S3 cannot bind a missing carrier
  - conjunctive reading has no executable multi-event contract

- arbitration：`predicate-gold-v1:EIS-0010-04`

## `EIS-0013-01`

- 分类：`EIS` / `D1` / `L0`；final relation `P_IMPLIES_O`
- 最近 proxy：无可靠 executable proxy
- unsupported reason：Pane5 final disposition is UNSUPPORTED_EXACT/P_IMPLIES_O. Track C proposed UNSUPPORTED_EXACT/UNRELATED; the fourth review proposed UNSUPPORTED_EXACT/P_IMPLIES_O. Pane5 resolves the difference as follows: Exactly the three named direct members is a sufficient strict encoding, but the adopted D1 reading permits A/B regional variants of the three main kinds. O therefore does not imply the direct-set candidate. Fourth-review evidence: The adopted D1 obligation fixes three main semantic kinds, not exactly three direct vertices. Exact direct-member-set equality is one sufficient strict encoding, but its falsity cannot reject the source-compatible variant reading; no executable kind-classification oracle exists.
- capability gap：

  - S1 cannot express owner-local closed-set equality or cardinality.
  - No predicate classifies 'main' semantic kinds.

- arbitration：`predicate-gold-v1:EIS-0013-01`

## `EIS-0014-01`

- 分类：`EIS` / `D2` / `L0`；final relation `P_IMPLIES_O`
- 最近 proxy：无可靠 executable proxy
- unsupported reason：Pane5 final disposition is UNSUPPORTED_EXACT/P_IMPLIES_O. Track C proposed EXACT_FALSE/EQUIVALENT; the fourth review proposed UNSUPPORTED_EXACT/P_IMPLIES_O. Pane5 resolves the difference as follows: One unique direct initial carrier to DoorsClosing is sufficient but not necessary for cold-entry activation; a legal compound initial descent can satisfy O in the same initialization macrostep. Fourth-review evidence: The obligation is cold-entry activation of DoorsClosing, not one authored direct-edge shape. The proposed complete direct-initial contract implies O, but P=false cannot refute a legal compound initial descent; the completed false/control/replay evidence therefore remains execution evidence for an over-specific repair.
- capability gap：

  - S2 omits event/guard/cardinality fields.
  - G1 is topology-only.

- arbitration：`predicate-gold-v1:EIS-0014-01`

## `EIS-0014-02`

- 分类：`EIS` / `D1` / `L1`；final relation `P_IMPLIES_O`
- 最近 proxy：无可靠 executable proxy
- unsupported reason：Pane5 final disposition is UNSUPPORTED_EXACT/P_IMPLIES_O. Track C proposed EXACT_FALSE/EQUIVALENT; the fourth review proposed UNSUPPORTED_EXACT/P_IMPLIES_O. Pane5 resolves the difference as follows: Track A adopts behavioral execution of Accelerate on every entry. A sole incoming-transition effect can satisfy that reading while strict S4 entry-slot membership remains false. Fourth-review evidence: S4 entry membership is a sufficient strict-slot realization, but it is not equivalent to Track A's adopted behavioral obligation. Because the source-compatible sole-incoming-transition effect can execute Accelerate on every entry while S4 remains false, the completed S4 false cannot establish the adopted O is false.
- capability gap：

  - S6 cannot bind free-text Accelerate as an undeclared operation.
  - S3 checks a separate initial-transition rule.

- arbitration：`predicate-gold-v1:EIS-0014-02`

## `EIS-0015-01`

- 分类：`EIS` / `D1` / `L0`；final relation `UNRELATED`
- 最近 proxy：无可靠 executable proxy
- unsupported reason：Pane5 final disposition is UNSUPPORTED_EXACT/UNRELATED. Track C and the independent fourth review agree on this boundary. Track C: The existence of any variable and any action is not a sound issue-specific falsifier without a binding to cooking time; unrelated declarations could make it true while O remains false. No query or control was manufactured; the final Track C disposition is unsupported rather than blocked execution. Independent confirmation: An arbitrary non-routing variable plus arbitrary action can coexist with a missing cooking-time value, display, update, and cancellation semantics; conversely a finite-state encoding need not declare a native variable. The generic inventory is unrelated to the issue-specific obligation.
- capability gap：

  - S1 excludes variables.
  - S6 requires one exact carrier and parseable operation.
  - R3 requires a complete fixed scenario and abstract action.
  - Trace variable delta is a non-predicate boundary.

- arbitration：`predicate-gold-v1:EIS-0015-01`

## `EIS-0016-01`

- 分类：`EIS` / `D1` / `L1`；final relation `UNRELATED`
- 最近 proxy：无可靠 executable proxy
- unsupported reason：Pane5 final disposition is UNSUPPORTED_EXACT/UNRELATED. Track C proposed EXACT_FALSE/EQUIVALENT; the fourth review proposed UNSUPPORTED_EXACT/UNRELATED. Pane5 resolves the difference as follows: The adopted D1 reading requires three distinct usable areas but permits nested topology. Direct-parent equality is neither necessary for that reading nor sufficient for progression and usability. Fourth-review evidence: O requires three distinct usable search areas but intentionally leaves peer-versus-nested topology open. Requiring Region1/2/3 all to be direct children of SearchMission rejects the adopted nested reading, while direct containment alone does not prove progression or usability; the parent-map false receipt cannot classify O.
- capability gap：

  - Frozen predicates expose declaration and topology but not requirement-relative parent equality.

- arbitration：`predicate-gold-v1:EIS-0016-01`

## `EIS-0016-02`

- 分类：`EIS` / `D2` / `L1`；final relation `UNRELATED`
- 最近 proxy：无可靠 executable proxy
- unsupported reason：Pane5 final disposition is UNSUPPORTED_EXACT/UNRELATED. Track C and the independent fourth review agree on this boundary. Track C: Placeholder identities and one global Search declaration do not express the owner-local target obligations. No query or control was manufactured; the final Track C disposition is unsupported rather than blocked execution. Independent confirmation: The obligation requires three owner-local initial targets with distinct native identities. The converted FCSTM inserts InvalidInitial placeholders, so owner/target checks on those projection objects do not establish the author-source identity error, and no exact source-native binding is available.
- capability gap：

  - Initial vertex exists for each required owner is a registry non-predicate boundary.
  - S2 requires exact endpoint identities that are missing.
  - The projection's diagnostic placeholder names are not requirement identities.

- arbitration：`predicate-gold-v1:EIS-0016-02`

## `EIS-0016-03`

- 分类：`EIS` / `D1` / `L1`；final relation `UNRELATED`
- 最近 proxy：无可靠 executable proxy
- unsupported reason：Pane5 final disposition is UNSUPPORTED_EXACT/UNRELATED. Track C and the independent fourth review agree on this boundary. Track C: No candidate binds the missing completion proposition, post-condition, unbounded scope or fairness assumptions. No query or control was manufactured; the final Track C disposition is unsupported rather than blocked execution. Independent confirmation: No candidate binds mission completion, its relation to Finished Region3 Search, ancestor completion, fairness, or an unbounded continuation scope. A Region3 final-edge check cannot express the retained D1 boundary.
- capability gap：

  - V3 requires exact p/q/bound and cannot bind termination.
  - G2 uses a derived finite horizon and exact source/targets, none source-backed here.
  - Simulation is ineligible.

- arbitration：`predicate-gold-v1:EIS-0016-03`

## `EIS-0019-01`

- 分类：`EIS` / `D1` / `L1`；final relation `UNRELATED`
- 最近 proxy：无可靠 executable proxy
- unsupported reason：Pane5 final disposition is UNSUPPORTED_EXACT/UNRELATED. Track C and the independent fourth review agree on this boundary. Track C: Track B's V1 property formalizes only the retained deterministic-disambiguation reading. It is unrelated to the adopted obligation, and the artifact contains free-text event labels rather than source-backed typed guards or a closed variable domain. Track C did not manufacture missing events, states, phases, variables, domains, bounds, or controls; the disposition is unsupported exactness rather than blocked execution. Independent confirmation: The source permits cruise or lane_change under the same stated condition but does not settle whether nondeterminism is intentional or whether a distinguishing rule is missing. A deterministic guard/domain property would strengthen the adopted source-minimal obligation, so no exact or sound executable property can be bound without inventing priority, exclusivity, or a typed domain.
- capability gap：

  - V1 lacks source-backed domain and native guard multiset inputs.
  - The attributed FCSTM represents the condition phrases as events rather than guards.
  - No frozen predicate expresses deterministic choice distinguishability including priority.

- arbitration：`predicate-gold-v1:EIS-0019-01`

## `EIS-0019-03`

- 分类：`EIS` / `D1` / `L2`；final relation `UNRELATED`
- 最近 proxy：无可靠 executable proxy
- unsupported reason：Pane5 final disposition is UNSUPPORTED_EXACT/UNRELATED. Track C and the independent fourth review agree on this boundary. Track C: Track B's ancestor-wide direct-target coverage encodes the stronger mode-global sensitivity and also rejects valid compound RTC realizations. It is unrelated to the adopted exit-phase obligation. Track C did not manufacture missing events, states, phases, variables, domains, bounds, or controls; the disposition is unsupported exactness rather than blocked execution. Independent confirmation: The author text admits both an exit-phase reading and a mode-global auto_finished reading. Ancestor-wide direct-target coverage adopts the stronger reading and also excludes valid compound RTC realizations, so it is not equivalent to the source-minimal obligation. Missing enablement scope, event priority, and timing prevent an exact executable gold.
- capability gap：

  - ANCESTOR_EVENT_TARGET_COVERAGE requires a direct target and cannot admit a valid exit-boundary plus continuation compound transition.
  - No existing oracle executes complete hierarchical event dispatch/RTC response over all adopted source leaves.
  - The D1 exit-leaf-only reading remains a sensitivity rather than an input shortcut.

- arbitration：`predicate-gold-v1:EIS-0019-03`

## `EIS-0020-02`

- 分类：`EIS` / `D1` / `L1`；final relation `UNRELATED`
- 最近 proxy：无可靠 executable proxy
- unsupported reason：Pane5 final disposition is UNSUPPORTED_EXACT/UNRELATED. Track C and the independent fourth review agree on this boundary. Track C: Track B's three-alternative static contract is stronger than the adopted reading. Separate native event identities and an eventless AutoFinal takeover carrier do not exist and cannot be bound without choosing an unprovided normalization. Track C did not manufacture missing events, states, phases, variables, domains, bounds, or controls; the disposition is unsupported exactness rather than blocked execution. Independent confirmation: The malformed NL lists steering, brake, and '(auto final)' without resolving whether the last phrase is a third alternative or a source-state qualifier. The artifact's comma-bearing free-text trigger does not supply separate native events. Any exact property would have to choose an unprovided parsing and enablement scope.
- capability gap：

  - No source-fixed connective separates steering, brake, and AutoFinal conditions.
  - No source-attributed distinct native event objects exist for steering and brake.
  - The available static oracle is proxy-only and requires exact event tokens.

- arbitration：`predicate-gold-v1:EIS-0020-02`

## `EIS-0024-02`

- 分类：`EIS` / `D2` / `L1`；final relation `UNRELATED`
- 最近 proxy：无可靠 executable proxy
- unsupported reason：Pane5 final disposition is UNSUPPORTED_EXACT/UNRELATED. Track C and the independent fourth review agree on this boundary. Track C: No candidate is equivalent or a sound executable falsifier because the source leaves the lifecycle phase and output representation unspecified, and a bounded retention scenario would add events and a window. Track C did not manufacture missing events, states, phases, variables, domains, bounds, or controls; the disposition is unsupported exactness rather than blocked execution. Independent confirmation: The obligation conjoins output Send with retention in Approaching, but the source omits output lifecycle phase, parseable operation identity, release event, and a closed retention scenario. S4 and R4 cannot be legally bound without inventing phase, events, or window, so no exact or sound executable candidate is available.
- capability gap：

  - S4 requires an exact lifecycle phase absent from the source.
  - R4 requires a complete scenario and interval absent from the source.
  - No current property jointly observes output occurrence and retained state without fabricated inputs.

- arbitration：`predicate-gold-v1:EIS-0024-02`

## `EIS-0024-04`

- 分类：`EIS` / `D1` / `L0`；final relation `UNRELATED`
- 最近 proxy：无可靠 executable proxy
- unsupported reason：Pane5 final disposition is UNSUPPORTED_EXACT/UNRELATED. Track C and the independent fourth review agree on this boundary. Track C: S4 requires an unprovided phase and S6 would bind the obligation to one exit carrier and operation syntax. Neither candidate is entailed by the phase-agnostic O. Track C did not manufacture missing events, states, phases, variables, domains, bounds, or controls; the disposition is unsupported exactness rather than blocked execution. Independent confirmation: The source requires EmergencyStopping to send Obstacle Detected but does not fix entry/do/exit phase, operation representation, recovery trigger, or delivery timing. S4 needs an exact phase and S6 would bind one carrier syntax; neither is entailed by the phase-agnostic obligation.
- capability gap：

  - S4 requires an entry/do/exit phase not fixed by the D1 source.
  - S6 requires one parseable effect and would cover only the retained exit-effect reading.
  - No phase-agnostic state-owned output oracle exists.

- arbitration：`predicate-gold-v1:EIS-0024-04`

## `EIS-0025-01`

- 分类：`EIS` / `D1` / `L1`；final relation `UNRELATED`
- 最近 proxy：无可靠 executable proxy
- unsupported reason：Pane5 final disposition is UNSUPPORTED_EXACT/UNRELATED. Track C and the independent fourth review agree on this boundary. Track C: Track B's S5 exact-guard property encodes the retained exclusive-routing reading and is unrelated to the adopted sufficient-condition obligation. Track C did not manufacture missing events, states, phases, variables, domains, bounds, or controls; the disposition is unsupported exactness rather than blocked execution. Independent confirmation: The source supports zero-time close as a sufficient route to DoorShutWithItem, but it does not unambiguously state the converse or provide a cooking-time variable/domain. An exact S5 guard would adopt the stronger exclusive-routing reading and invent a typed expression, so execution remains unsupported.
- capability gap：

  - S5 cannot bind a variable-free natural-language zero-time phrase to one guard AST.
  - No variable type/domain or exact guard syntax is source-backed.

- arbitration：`predicate-gold-v1:EIS-0025-01`

## `EIS-0025-02`

- 分类：`EIS` / `D1` / `L0`；final relation `UNRELATED`
- 最近 proxy：无可靠 executable proxy
- unsupported reason：Pane5 final disposition is UNSUPPORTED_EXACT/UNRELATED. Track C and the independent fourth review agree on this boundary. Track C: No frozen predicate or evaluation-only property can be equivalent without a variable, data type, update function, lifecycle phase and operation identities. Track C did not manufacture missing events, states, phases, variables, domains, bounds, or controls; the disposition is unsupported exactness rather than blocked execution. Independent confirmation: The NL requires observable cooking-time display/update/cancel behavior but fixes no variable name, data type, domain, update function, action phase, or operation identity. Existing static/action/bounded properties cannot express an equivalent oracle without invented data semantics.
- capability gap：

  - The source-static backend does not expose variable declaration membership through S1.
  - No source-fixed variable/action/effect identities, types, domains, or lifecycle slots exist.
  - No composite can recover missing typed inputs.

- arbitration：`predicate-gold-v1:EIS-0025-02`

## `EIS-0026-01`

- 分类：`EIS` / `D1` / `L1`；final relation `UNRELATED`
- 最近 proxy：无可靠 executable proxy
- unsupported reason：Pane5 final disposition is UNSUPPORTED_EXACT/UNRELATED. Track C and the independent fourth review agree on this boundary. Track C: DIRECT_CHILD_HIERARCHY counts child states, not regions, and would be true on the defective artifact for the wrong reason. It is unrelated to either a genuine region-count property or the adopted mode reading. Track C did not manufacture missing events, states, phases, variables, domains, bounds, or controls; the disposition is unsupported exactness rather than blocked execution. Independent confirmation: The phrase 'three different state areas' is source-ambiguous between sibling operating modes and UML regions. Counting direct children would answer the wrong structural question and may return true for the wrong reason; region count cannot be selected as exact without choosing the stronger interpretation and inventing region roles.
- capability gap：

  - No frozen predicate or native oracle exposes UML region cardinality.
  - Direct-child state count is an unsound false-positive surrogate.
  - The intended three region identities/content are absent.

- arbitration：`predicate-gold-v1:EIS-0026-01`

## `EIS-0026-02`

- 分类：`EIS` / `D2` / `L0`；final relation `UNRELATED`
- 最近 proxy：无可靠 executable proxy
- unsupported reason：Pane5 final disposition is UNSUPPORTED_EXACT/UNRELATED. Track C and the independent fourth review agree on this boundary. Track C: S6 needs one exact parseable operation and therefore cannot express a representation-independent strict decrease when no count variable, type, domain or decrement operation exists. Track C did not manufacture missing events, states, phases, variables, domains, bounds, or controls; the disposition is unsupported exactness rather than blocked execution. Independent confirmation: A strict swarm-count decrease is source-required, but the artifact and NL provide no variable identity, type, domain, before/after binding, update operation, or lower bound. S6 and bounded properties would require invented data semantics, so exact execution is unsupported.
- capability gap：

  - S6 requires one parseable effect but the variable, type, domain, decrement amount, and operation syntax are absent.
  - No trace-variable-delta predicate exists.

- arbitration：`predicate-gold-v1:EIS-0026-02`

## `EIS-0026-03`

- 分类：`EIS` / `D2` / `L2`；final relation `UNRELATED`
- 最近 proxy：无可靠 executable proxy
- unsupported reason：Pane5 final disposition is UNSUPPORTED_EXACT/UNRELATED. Track C and the independent fourth review agree on this boundary. Track C: G1 to one chosen target and V4 one-step progress are necessary symptoms only and do not capture eventual mission continuation, events, guards or fairness. Track C did not manufacture missing events, states, phases, variables, domains, bounds, or controls; the disposition is unsupported exactness rather than blocked execution. Independent confirmation: Continuous pre-completion search makes FormationAdjustment an intermediate mission condition, but the source omits its completion event, continuation target, fairness, and time bound. G1 to one chosen target or V4 one-step progress captures only a necessary symptom, not the eventual mission-continuation obligation.
- capability gap：

  - G1 and V4 are only necessary-condition approximations.
  - No unbounded eventual-recovery/fairness property is available.
  - The behavior profile is academically ineligible.

- arbitration：`predicate-gold-v1:EIS-0026-03`

## `EIS-0027-01`

- 分类：`EIS` / `D2` / `L2`；final relation `UNRELATED`
- 最近 proxy：无可靠 executable proxy
- unsupported reason：Pane5 final disposition is UNSUPPORTED_EXACT/UNRELATED. Track C and the independent fourth review agree on this boundary. Track C: G1 to DetectingState and V4 local progress are only necessary approximations; neither expresses orthogonal synchronization, deactivation/rearm, safe configuration or eventuality. Track C did not manufacture missing events, states, phases, variables, domains, bounds, or controls; the disposition is unsupported exactness rather than blocked execution. Independent confirmation: The artifact traps all three regions after activation, but the source explicitly states activation and concurrency, not a deactivation event, rearm target, synchronization rule, or recurrence bound. A recurring collision-avoidance lifecycle is a reasonable ledger/domain inference but remains a sensitivity; G1/V4 cannot express the missing orthogonal configuration and eventuality.
- capability gap：

  - G1 discards orthogonal configuration and synchronization semantics.
  - V4 is one-step existential progress over a projection, not cycle recovery.
  - The FCSTM metadata records concurrent-region/runtime debt and simulation ineligibility.

- arbitration：`predicate-gold-v1:EIS-0027-01`

## `EIS-0029-01`

- 分类：`EIS` / `D2` / `L1`；final relation `P_IMPLIES_O`
- 最近 proxy：无可靠 executable proxy
- unsupported reason：Pane5 final disposition is UNSUPPORTED_EXACT/P_IMPLIES_O. Track C proposed EXACT_FALSE/EQUIVALENT; the fourth review proposed UNSUPPORTED_EXACT/P_IMPLIES_O. Pane5 resolves the difference as follows: The obligation requires containment under a source-named owner, not the candidate's stronger immediate-child depth. Falsity of the stronger structural property cannot falsify O. Fourth-review evidence: AutonomousMode must contain the named states, but source does not require immediate-child depth. A valid intermediate wrapper makes DIRECT_CHILD_HIERARCHY false while O remains true; the executed property is P_IMPLIES_O, not exact or a sound false proxy.
- capability gap：

  - The source names AutonomousMode as the parent of InitialState and the two driving modes; the direct-child native query checks exactly those required containment facts without asserting an exhaustive child set. The defective query completed false, the precommitted independent control completed true, and both semantic replays matched; these results verify execution but do not strengthen the preflight O/P relation.

- arbitration：`predicate-gold-v1:EIS-0029-01`

## `EIS-0029-02`

- 分类：`EIS` / `D1` / `L1`；final relation `UNRELATED`
- 最近 proxy：无可靠 executable proxy
- unsupported reason：Pane5 final disposition is UNSUPPORTED_EXACT/UNRELATED. Track C and the independent fourth review agree on this boundary. Track C: The source leaves the cruise/lane-change choice and persistence semantics ambiguous. No source-backed variable domain, priority, or complete native conflict oracle can bind an equivalent or false-sound query. No query or control was manufactured; the final Track C disposition is unsupported rather than blocked execution. Independent confirmation: The source leaves the cruise/lane-change choice and persistence semantics ambiguous. No source-backed variable domain, priority, or complete native conflict oracle can bind an equivalent or false-sound query. No query or control was manufactured; the final Track C disposition is unsupported rather than blocked execution.
- capability gap：

  - Missing finite domain and complete guard multiset.
  - No universal same-event/no-guard conflict oracle.

- arbitration：`predicate-gold-v1:EIS-0029-02`

## `EIS-0029-04`

- 分类：`EIS` / `D2` / `L0`；final relation `UNRELATED`
- 最近 proxy：无可靠 executable proxy
- unsupported reason：Pane5 final disposition is UNSUPPORTED_EXACT/UNRELATED. Track C and the independent fourth review agree on this boundary. Track C: The obligation jointly covers two owner-local default entries. The available single-owner oracle cannot express the conjunction, while native inventories include lowering carriers that cannot be silently filtered as authored defaults. No query or control was manufactured; the final Track C disposition is unsupported rather than blocked execution. Independent confirmation: The obligation jointly covers two owner-local default entries. The available single-owner oracle cannot express the conjunction, while native inventories include lowering carriers that cannot be silently filtered as authored defaults. No query or control was manufactured; the final Track C disposition is unsupported rather than blocked execution.
- capability gap：

  - One-owner initial oracle only.
  - No evaluation-oracle composite runner.
  - Native init inventory mixes authored defaults and lowering carriers for this artifact.

- arbitration：`predicate-gold-v1:EIS-0029-04`

## `EIS-0029-05`

- 分类：`EIS` / `D2` / `L2`；final relation `P_IMPLIES_O`
- 最近 proxy：无可靠 executable proxy
- unsupported reason：Pane5 final disposition is UNSUPPORTED_EXACT/P_IMPLIES_O. Track C proposed EXACT_FALSE/EQUIVALENT; the fourth review proposed UNSUPPORTED_EXACT/P_IMPLIES_O. Pane5 resolves the difference as follows: The obligation requires the source-compatible shared target relation, not one exact direct parent. The candidate narrows valid containment structures and is not O-implied. Fourth-review evidence: FinishState must be shared outside both modes, but a root-owned shared state is source-compatible. Direct ownership by AutonomousMode is not necessary, so UNIQUE_STATE_DIRECT_PARENT is P_IMPLIES_O and its false result cannot be exact gold.
- capability gap：

  - The issue-local obligation is one shared FinishState directly owned by AutonomousMode; the oracle checks uniqueness, canonical identity, and direct parent without using reachability as a surrogate. The defective query completed false, the precommitted independent control completed true, and both semantic replays matched; these results verify execution but do not strengthen the preflight O/P relation.

- arbitration：`predicate-gold-v1:EIS-0029-05`

## `EIS-0030-01`

- 分类：`EIS` / `D2` / `L0`；final relation `UNRELATED`
- 最近 proxy：无可靠 executable proxy
- unsupported reason：Pane5 final disposition is UNSUPPORTED_EXACT/UNRELATED. Track C and the independent fourth review agree on this boundary. Track C: The source requires an autonomous-final concept but supplies no bindable identity, kind, entry carrier, or completion timing. Inventing a state or treating label text as a final pseudostate is forbidden. No query or control was manufactured; the final Track C disposition is unsupported rather than blocked execution. Independent confirmation: The source requires an autonomous-final concept but supplies no bindable identity, kind, entry carrier, or completion timing. Inventing a state or treating label text as a final pseudostate is forbidden. No query or control was manufactured; the final Track C disposition is unsupported rather than blocked execution.
- capability gap：

  - Missing final identity and completion semantics.
  - No final-kind/source-condition oracle.

- arbitration：`predicate-gold-v1:EIS-0030-01`

## `EIS-0030-03`

- 分类：`EIS` / `D1` / `L1`；final relation `UNRELATED`
- 最近 proxy：无可靠 executable proxy
- unsupported reason：Pane5 final disposition is UNSUPPORTED_EXACT/UNRELATED. Track C and the independent fourth review agree on this boundary. Track C: The connective among steering, brake, and auto-final remains D1, and auto-final has no source identity. Reusing the fused artifact event would manufacture the missing semantic inputs. No query or control was manufactured; the final Track C disposition is unsupported rather than blocked execution. Independent confirmation: The connective among steering, brake, and auto-final remains D1, and auto-final has no source identity. Reusing the fused artifact event would manufacture the missing semantic inputs. No query or control was manufactured; the final Track C disposition is unsupported rather than blocked execution.
- capability gap：

  - Missing state-condition binding.
  - No universal separated-route predicate outside the unbindable static oracle.

- arbitration：`predicate-gold-v1:EIS-0030-03`

## `EIS-0033-01`

- 分类：`EIS` / `D2` / `L1`；final relation `UNRELATED`
- 最近 proxy：无可靠 executable proxy
- unsupported reason：Pane5 final disposition is UNSUPPORTED_EXACT/UNRELATED. Track C and the independent fourth review agree on this boundary. Track C: The source requires the three states to be descendants within PumpControl but does not prove immediate direct-child depth. DIRECT_CHILD_HIERARCHY is stronger: false could occur on a source-compatible nested hierarchy and therefore is not a sound falsifier. No query or control was manufactured; the final Track C disposition is unsupported rather than blocked execution. Independent confirmation: The source requires the three states to be descendants within PumpControl but does not prove immediate direct-child depth. DIRECT_CHILD_HIERARCHY is stronger: false could occur on a source-compatible nested hierarchy and therefore is not a sound falsifier. No query or control was manufactured; the final Track C disposition is unsupported rather than blocked execution.
- capability gap：

  - Track B proposed EQUIVALENT direct-child coverage; Track C rejects execution because Track A correctly records direct-versus-deeper containment as missing information.

- arbitration：`predicate-gold-v1:EIS-0033-01`

## `EIS-0034-01`

- 分类：`EIS` / `D2` / `L1`；final relation `P_IMPLIES_O`
- 最近 proxy：无可靠 executable proxy
- unsupported reason：Pane5 final disposition is UNSUPPORTED_EXACT/P_IMPLIES_O. Track C proposed EXACT_FALSE/EQUIVALENT; the fourth review proposed UNSUPPORTED_EXACT/P_IMPLIES_O. Pane5 resolves the difference as follows: The source fixes containment/shared ownership but does not require the candidate's immediate-child depth. The stronger direct-parent check cannot serve as an exact or sound false proxy. Fourth-review evidence: The phases must be within InMotion, but immediate-child depth is not required. An intermediate phase wrapper makes DIRECT_CHILD_HIERARCHY false without violating O; the executed property is P_IMPLIES_O, so exact gold is unsupported.
- capability gap：

  - The source explicitly enumerates Accelerating, Cruising, and Approaching as the three InMotion substates. The query checks these required direct children without asserting an exhaustive inventory. The defective query completed false, the precommitted independent control completed true, and both semantic replays matched; these results verify execution but do not strengthen the preflight O/P relation.

- arbitration：`predicate-gold-v1:EIS-0034-01`

## `EIS-0034-05`

- 分类：`EIS` / `D2` / `L0`；final relation `UNRELATED`
- 最近 proxy：无可靠 executable proxy
- unsupported reason：Pane5 final disposition is UNSUPPORTED_EXACT/UNRELATED. Track C and the independent fourth review agree on this boundary. Track C: The output role is source-backed, but no phase, carrier, receiver, payload, or schedule is supplied. The incoming event cannot be reused as an output-emission oracle. No query or control was manufactured; the final Track C disposition is unsupported rather than blocked execution. Independent confirmation: The output role is source-backed, but no phase, carrier, receiver, payload, or schedule is supplied. The incoming event cannot be reused as an output-emission oracle. No query or control was manufactured; the final Track C disposition is unsupported rather than blocked execution.
- capability gap：

  - Missing output slot/carrier.
  - No output-emission predicate.
  - No schedule/window.

- arbitration：`predicate-gold-v1:EIS-0034-05`

## `EIS-0035-01`

- 分类：`EIS` / `D2` / `L0`；final relation `UNRELATED`
- 最近 proxy：无可靠 executable proxy
- unsupported reason：Pane5 final disposition is UNSUPPORTED_EXACT/UNRELATED. Track C proposed SOUND_FALSE_PROXY/O_IMPLIES_P; the fourth review proposed UNSUPPORTED_EXACT/UNRELATED. Pane5 resolves the difference as follows: A direct authored carrier is not necessary for the RTC obligation because a source-compatible compound pseudostate route may satisfy it in one macrostep. Fourth-review evidence: The obligation is cold-entry reachability of DoorShut, not an authored direct-edge obligation. A compound initial route through a pseudostate can reach DoorShut in the same macrostep while S2([*], DoorShut) is false; conversely S2 ignores uniqueness, triggerlessness, and guards. The completed S2 evidence is query-correct but cannot soundly falsify O.
- capability gap：

  - Track B fcstm_sha256=sha256:e538f73da231893bfb3d9169d5e1e6a61d924b9d54b59e25f1e21ebabd9f5d3c is the FCSTM_META file hash, not executable model.fcstm bytes sha256:208d818286bf630e21aff55b3132fd29e63897dca5a2e42b9baa9a1d1cf7dfab; Track C rebinds only to the Track A hash-bound model artifact.
  - Track B relation EQUIVALENT is corrected to O_IMPLIES_P; a false receipt cannot establish equivalence.
  - Chronology defect: Track A records reviewed_at=2026-08-31T15:30:00Z, later than this truthful preflight freeze 2026-08-30T22:57:54.218535Z; no timestamp is fabricated to conceal it.

- arbitration：`predicate-gold-v1:EIS-0035-01`

## `EIS-0035-02`

- 分类：`EIS` / `D2` / `L0`；final relation `UNRELATED`
- 最近 proxy：无可靠 executable proxy
- unsupported reason：Pane5 final disposition is UNSUPPORTED_EXACT/UNRELATED. Track C proposed SOUND_FALSE_PROXY/O_IMPLIES_P; the fourth review proposed UNSUPPORTED_EXACT/UNRELATED. Pane5 resolves the difference as follows: The direct-edge candidate does not preserve the obligation's event and RTC semantics; a compound pseudostate route can satisfy O while the candidate is false. Fourth-review evidence: Door Closed must return DoorOpen to DoorShut in the same RTC, but the source does not require one direct carrier. A legal compound transition can satisfy O without the selected exact signature, while signature presence alone does not establish guard feasibility or RTC completion. The completed relation-oracle evidence therefore does not establish O_IMPLIES_P.
- capability gap：

  - Track B fcstm_sha256=sha256:e538f73da231893bfb3d9169d5e1e6a61d924b9d54b59e25f1e21ebabd9f5d3c is the FCSTM_META file hash, not executable model.fcstm bytes sha256:208d818286bf630e21aff55b3132fd29e63897dca5a2e42b9baa9a1d1cf7dfab; Track C rebinds only to the Track A hash-bound model artifact.
  - Track B relation EQUIVALENT is corrected to O_IMPLIES_P; a false receipt cannot establish equivalence.
  - Chronology defect: Track A records reviewed_at=2026-08-31T15:30:00Z, later than this truthful preflight freeze 2026-08-30T22:57:54.218535Z; no timestamp is fabricated to conceal it.

- arbitration：`predicate-gold-v1:EIS-0035-02`

## `EIS-0035-03`

- 分类：`EIS` / `D1` / `L1`；final relation `UNRELATED`
- 最近 proxy：无可靠 executable proxy
- unsupported reason：Pane5 final disposition is UNSUPPORTED_EXACT/UNRELATED. Track C and the independent fourth review agree on this boundary. Track C: The obligation depends on the zero-time data condition, but no source-backed variable domain, guard carrier, or exact transition binding exists for an executable equality check. No execution is claimed; this avoids turning an unsound relation, incomplete binding, simulation-ineligible query, or missing oracle contract into fabricated evidence. Independent confirmation: The zero-time qualification has no source-backed variable identity, domain, guard carrier, or unambiguous state invariant. The retained D1 reading cannot be converted into an equivalent executable property without inventing whether DoorOpenWithItem itself implies zero time.
- capability gap：

  - The source gives no executable variable identity or FCSTM guard expression for cooking time.

- arbitration：`predicate-gold-v1:EIS-0035-03`

## `EIS-0035-04`

- 分类：`EIS` / `D1` / `L0`；final relation `UNRELATED`
- 最近 proxy：无可靠 executable proxy
- unsupported reason：Pane5 final disposition is UNSUPPORTED_EXACT/UNRELATED. Track C and the independent fourth review agree on this boundary. Track C: The missing cooking-time variable/effects obligation cannot be recovered from a source-backed variable identity and update domain; execution would invent data semantics. No execution is claimed; this avoids turning an unsound relation, incomplete binding, simulation-ineligible query, or missing oracle contract into fabricated evidence. Independent confirmation: The cooking-time display/update/cancel obligation names behavior but supplies no variable type, value domain, owning component, display action, or update effect. Executing a data property would add semantics absent from both NL and author model, so exact gold is unsupported.
- capability gap：

  - No cooking-time variable declaration, value domain, exact display action, or update operation is supplied.

- arbitration：`predicate-gold-v1:EIS-0035-04`

## `EIS-0039-02`

- 分类：`EIS` / `D1` / `L1`；final relation `O_IMPLIES_P`
- 最近 proxy：无可靠 executable proxy
- unsupported reason：Pane5 final disposition is UNSUPPORTED_EXACT/O_IMPLIES_P. Track C and the independent fourth review agree on this boundary. Track C: Under the adopted D1 ordinary group-transition reading, O forbids both same-mode ancestor reentries. The direction is necessary-only, but the frozen oracles cannot express the conjunction of both eventless guarded forbidden carriers without changing the two-target quantifier. No execution is claimed; this avoids turning an unsound relation, incomplete binding, simulation-ineligible query, or missing oracle contract into fabricated evidence. Independent confirmation: Under the adopted D1 group-transition reading, correct switching excludes both ancestor-to-same-mode re-entry carriers, so their absence is necessary. The frozen candidate cannot bind and execute the two-target conjunction without changing its quantifier, and the completion-transition alternative remains a sensitivity; exact execution is unsupported.
- capability gap：

  - Track B fcstm_sha256=sha256:2fa721d0da9e7405120700b5c47a0ec75f70959b672273c85f7aeade80de912c is the FCSTM_META file hash, not executable model.fcstm bytes sha256:fdc4158e2512976baba84cc46cd5eecc7691a4ba434eb7b0f4efecd68a1f0352; Track C rebinds only to the Track A hash-bound model artifact.
  - Track B relation EQUIVALENT is corrected to O_IMPLIES_P; a false receipt cannot establish equivalence.
  - Track B proposed execution, but Track C rejects execution because the relation, complete typed binding, eligibility, or frozen oracle contract does not close.
  - Chronology defect: Track A records reviewed_at=2026-08-31T15:30:00Z, later than this truthful preflight freeze 2026-08-30T22:57:54.218535Z; no timestamp is fabricated to conceal it.

- arbitration：`predicate-gold-v1:EIS-0039-02`

## `EIS-0040-01`

- 分类：`EIS` / `D2` / `L0`；final relation `UNRELATED`
- 最近 proxy：无可靠 executable proxy
- unsupported reason：Pane5 final disposition is UNSUPPORTED_EXACT/UNRELATED. Track C and the independent fourth review agree on this boundary. Track C: System-wide Power Off coverage does not imply one direct Autonomous-to-exit carrier: legal leaf-specific coverage is an alternative representation. The selected source-static carrier is therefore not a necessary condition without an unsupported representation assumption. No execution is claimed; this avoids turning an unsound relation, incomplete binding, simulation-ineligible query, or missing oracle contract into fabricated evidence. Independent confirmation: Global Power Off coverage does not require a single direct Autonomous-to-final carrier: leaf-specific exits or a compound hierarchy exit can satisfy O. The selected carrier check is neither a necessary nor complete RTC property, so no executable exact or sound-falsifier disposition is available.
- capability gap：

  - Track B fcstm_sha256=sha256:06248ca6b0ee6174fb2845f3aee199454da5c5eb063efe15779c733d361b7d9c is the FCSTM_META file hash, not executable model.fcstm bytes sha256:c579c02a617c296eda99b3b343c775e3fb3916eeed20a0da1597269ecc6423a3; Track C rebinds only to the Track A hash-bound model artifact.
  - Track B relation EQUIVALENT is corrected to UNRELATED; a false receipt cannot establish equivalence.
  - Track B proposed execution, but Track C rejects execution because the relation, complete typed binding, eligibility, or frozen oracle contract does not close.
  - Chronology defect: Track A records reviewed_at=2026-08-31T15:30:00Z, later than this truthful preflight freeze 2026-08-30T22:57:54.218535Z; no timestamp is fabricated to conceal it.

- arbitration：`predicate-gold-v1:EIS-0040-01`

## `EIS-0040-03`

- 分类：`EIS` / `D2` / `L0`；final relation `UNRELATED`
- 最近 proxy：无可靠 executable proxy
- unsupported reason：Pane5 final disposition is UNSUPPORTED_EXACT/UNRELATED. Track C and the independent fourth review agree on this boundary. Track C: The initial-pseudostate triggerlessness contract needs the exact transition carrier and trigger set; Track B lacks the mandatory native carrier binding. No execution is claimed; this avoids turning an unsound relation, incomplete binding, simulation-ineligible query, or missing oracle contract into fabricated evidence. Independent confirmation: The local initial edge must be triggerless and enter AutoInitial during Autonomous entry, but the exact converted transition carrier required by S3 is not bound. An author PlantUML line number cannot be substituted for that native carrier, so execution would fabricate the binding.
- capability gap：

  - The packet does not expose the converted FCSTM transition carrier ID required by S3.
  - S3 needs an exact converted transition:line:<n> carrier; an author PlantUML line number is not that native ID.

- arbitration：`predicate-gold-v1:EIS-0040-03`

## `EIS-0042-01`

- 分类：`EIS` / `D2` / `L0`；final relation `UNRELATED`
- 最近 proxy：无可靠 executable proxy
- unsupported reason：Pane5 final disposition is UNSUPPORTED_EXACT/UNRELATED. Track C and the independent fourth review agree on this boundary. Track C: The keyOff-labelled root initial carrier requires exact S3/S5-style carrier identity and pseudostate semantics; Track B correctly exposes no executable binding. No execution is claimed; this avoids turning an unsound relation, incomplete binding, simulation-ineligible query, or missing oracle contract into fabricated evidence. Independent confirmation: The keyOff-labelled root initial edge violates initialization and lifecycle semantics, but the candidate lacks the exact native carrier needed to inspect its trigger set. Startup, start, and keyOff behavior cannot be collapsed into an unbound S3 query.
- capability gap：

  - The packet does not expose the converted FCSTM transition carrier ID required by S3.
  - S3 needs an exact converted transition:line:<n> carrier; an author PlantUML line number is not that native ID.

- arbitration：`predicate-gold-v1:EIS-0042-01`

## `EIS-0043-01`

- 分类：`EIS` / `D1` / `L1`；final relation `UNRELATED`
- 最近 proxy：无可靠 executable proxy
- unsupported reason：Pane5 final disposition is UNSUPPORTED_EXACT/UNRELATED. Track C and the independent fourth review agree on this boundary. Track C: The obligation concerns the complete PumpControl decomposition and invented Region2 contents; no selected property closes hierarchy, membership, and orthogonality together. No execution is claimed; this avoids turning an unsound relation, incomplete binding, simulation-ineligible query, or missing oracle contract into fabricated evidence. Independent confirmation: The D1 closed-decomposition reading requires hierarchy membership, completeness, and orthogonal-region semantics together. No candidate expresses all three without assuming that 'main' means direct and exhaustive or inventing a region cardinality oracle.
- capability gap：

  - The word main does not close the inventory or require direct ownership, and pyfcstm has no orthogonal-region cardinality predicate.

- arbitration：`predicate-gold-v1:EIS-0043-01`

## `EIS-0043-02`

- 分类：`EIS` / `D2` / `L0`；final relation `UNRELATED`
- 最近 proxy：无可靠 executable proxy
- unsupported reason：Pane5 final disposition is UNSUPPORTED_EXACT/UNRELATED. Track C and the independent fourth review agree on this boundary. Track C: O requires defaults for every active region and PumpState after hierarchical descent. It does not imply a direct PumpControl-owned [*]-to-PumpState edge because a legal wrapper/region descent may mediate entry; S2 would silently collapse hierarchy and omit the second region. No execution is claimed; this avoids turning an unsound relation, incomplete binding, simulation-ineligible query, or missing oracle contract into fabricated evidence. Independent confirmation: O requires valid default descent in every active region and eventual activation of PumpState. A direct PumpControl-owned [*]-to-PumpState edge is not necessary because legal wrapper/region descent can mediate entry, and it omits the second region. The S2 candidate is therefore unrelated as a falsifier.
- capability gap：

  - Track B fcstm_sha256=sha256:48298aa240854dac1cfe318b493d65196c0a6bae8ee971e9ef938274586220a5 is the FCSTM_META file hash, not executable model.fcstm bytes sha256:a00277c12f2f441c042fe9232e13e955e7d55a06a60c0ebbaeceaf8e2a9964cc; Track C rebinds only to the Track A hash-bound model artifact.
  - Track B relation EQUIVALENT is corrected to UNRELATED; a false receipt cannot establish equivalence.
  - Track B proposed execution, but Track C rejects execution because the relation, complete typed binding, eligibility, or frozen oracle contract does not close.
  - Chronology defect: Track A records reviewed_at=2026-08-31T15:30:00Z, later than this truthful preflight freeze 2026-08-30T22:57:54.218535Z; no timestamp is fabricated to conceal it.

- arbitration：`predicate-gold-v1:EIS-0043-02`

## `EIS-0044-01`

- 分类：`EIS` / `D2` / `L0`；final relation `UNRELATED`
- 最近 proxy：无可靠 executable proxy
- unsupported reason：Pane5 final disposition is UNSUPPORTED_EXACT/UNRELATED. Track C proposed SOUND_FALSE_PROXY/O_IMPLIES_P; the fourth review proposed UNSUPPORTED_EXACT/UNRELATED. Pane5 resolves the difference as follows: The proposed direct carrier is not necessary under source-compatible compound-transition semantics, so its falsity does not establish the RTC obligation's failure. Fourth-review evidence: InMotion must activate Accelerating and its entry action during initial descent, but O does not require a direct [*]-to-Accelerating carrier. A compound pseudostate route can satisfy the same RTC obligation, while S2 ignores uniqueness, trigger/guard constraints, and entry/Accelerate. The completed S2 query cannot serve as a sound proxy.
- capability gap：

  - Track B fcstm_sha256=sha256:c6b0a03d470df67f18543cd1ac922ba4454f1f65d5c5068082f030a00f57c132 is the FCSTM_META file hash, not executable model.fcstm bytes sha256:265189e17700beb0743f61ec0119c8133d8d4df9ce5077364419f888ad18a9de; Track C rebinds only to the Track A hash-bound model artifact.
  - Track B relation EQUIVALENT is corrected to O_IMPLIES_P; a false receipt cannot establish equivalence.
  - Chronology defect: Track A records reviewed_at=2026-08-31T15:30:00Z, later than this truthful preflight freeze 2026-08-30T22:57:54.218535Z; no timestamp is fabricated to conceal it.

- arbitration：`predicate-gold-v1:EIS-0044-01`

## `EIS-0045-01`

- 分类：`EIS` / `D1` / `L0`；final relation `UNRELATED`
- 最近 proxy：无可靠 executable proxy
- unsupported reason：Pane5 final disposition is UNSUPPORTED_EXACT/UNRELATED. Track C and the independent fourth review agree on this boundary. Track C: The exact mode-switching obligation depends on trigger, state condition, and takeover semantics that the packet cannot bind without adding an environment interpretation. No execution is claimed; this avoids turning an unsound relation, incomplete binding, simulation-ineligible query, or missing oracle contract into fabricated evidence. Independent confirmation: Cooking-time display and update/cancel behavior lacks a native variable, domain, action, and effect carrier. Track C's mode-switching wording does not describe this issue; the source-backed disposition is nevertheless unsupported because any executable data property would invent the missing semantics.
- capability gap：

  - No native variable, exact display/update operation, or effect carrier is source-bound.

- arbitration：`predicate-gold-v1:EIS-0045-01`

## `EIS-0046-01`

- 分类：`EIS` / `D2` / `L0`；final relation `UNRELATED`
- 最近 proxy：无可靠 executable proxy
- unsupported reason：Pane5 final disposition is UNSUPPORTED_EXACT/UNRELATED. Track C proposed SOUND_FALSE_PROXY/O_IMPLIES_P; the fourth review proposed UNSUPPORTED_EXACT/UNRELATED. Pane5 resolves the difference as follows: The candidate reduces an event-scoped RTC response to one authored direct edge. Valid pseudostate composition can satisfy O without that edge. Fourth-review evidence: The wrapper must enter a unique search-first child, but the obligation does not force one direct wrapper-to-SearchRegion initial carrier; an initial pseudostate/choice chain can satisfy the same macrostep. S2 also omits uniqueness and trigger/guard constraints, so its completed false is not a sound falsifier.
- capability gap：

  - Track B fcstm_sha256=sha256:b52049bf17c708eea1e2880c36bf5b1a1218debf7195a2114ca1437d79ddf21a is the FCSTM_META file hash, not executable model.fcstm bytes sha256:1b1d4744daa8291b98cbdd0ee8bbaeb0337bcf92915c852bfde05a11e96948c9; Track C rebinds only to the Track A hash-bound model artifact.
  - Track B relation EQUIVALENT is corrected to O_IMPLIES_P; a false receipt cannot establish equivalence.
  - Chronology defect: Track A records reviewed_at=2026-08-31T15:30:00Z, later than this truthful preflight freeze 2026-08-30T22:57:54.218535Z; no timestamp is fabricated to conceal it.

- arbitration：`predicate-gold-v1:EIS-0046-01`

## `EIS-0046-02`

- 分类：`EIS` / `D1` / `L1`；final relation `UNRELATED`
- 最近 proxy：无可靠 executable proxy
- unsupported reason：Pane5 final disposition is UNSUPPORTED_EXACT/UNRELATED. Track C and the independent fourth review agree on this boundary. Track C: Three search areas, region semantics, and MissionRegion misclassification cannot be represented by a single supported predicate without inventing region identity/cardinality. No execution is claimed; this avoids turning an unsound relation, incomplete binding, simulation-ineligible query, or missing oracle contract into fabricated evidence. Independent confirmation: The phrase 'three different state areas' has two live readings: structural regions or operational phases. Neither the identities nor concurrency/cardinality of three regions are source-fixed, so an equivalent executable property cannot be bound.
- capability gap：

  - State areas is ambiguous between operating states and UML orthogonal regions; no region identities are named.

- arbitration：`predicate-gold-v1:EIS-0046-02`

## `EIS-0047-01`

- 分类：`EIS` / `D2` / `L1`；final relation `EQUIVALENT`
- 最近 proxy：无可靠 executable proxy
- unsupported reason：Pane5 final disposition is UNSUPPORTED_EXACT/EQUIVALENT. Track C and the independent fourth review agree on this boundary. Track C: The issue-local P is exact only if it checks three distinct owner-local Idle/Braking/Clamping sets and each local initial containment. Frozen DIRECT_CHILD_HIERARCHY handles one parent and omits local initial targets; no non-short-circuit three-owner oracle contract exists. No execution is claimed; this avoids turning an unsound relation, incomplete binding, simulation-ineligible query, or missing oracle contract into fabricated evidence. Independent confirmation: The exact abstract property is three distinct owner-local Idle/Braking/Clamping sets with matching local initial containment. The defective source collapses those globally named states, so the intended owner-local identities do not exist to bind; no frozen non-short-circuit three-owner oracle executes the equivalent property.
- capability gap：

  - Track B fcstm_sha256=sha256:b010de4155d5bbd258cdc8ccd4332baa63566087261aff86b0cfa5b1fea3d345 is the FCSTM_META file hash, not executable model.fcstm bytes sha256:165f4080834fc15e7d7e472552483c2349f1507da482de728c6920bd1b527b0f; Track C rebinds only to the Track A hash-bound model artifact.
  - Track B proposed execution, but Track C rejects execution because the relation, complete typed binding, eligibility, or frozen oracle contract does not close.
  - Chronology defect: Track A records reviewed_at=2026-08-31T15:30:00Z, later than this truthful preflight freeze 2026-08-30T22:57:54.218535Z; no timestamp is fabricated to conceal it.

- arbitration：`predicate-gold-v1:EIS-0047-01`

## `EIS-0047-02`

- 分类：`EIS` / `D2` / `L0`；final relation `P_IMPLIES_O`
- 最近 proxy：无可靠 executable proxy
- unsupported reason：Pane5 final disposition is UNSUPPORTED_EXACT/P_IMPLIES_O. Track C proposed UNSUPPORTED_EXACT/UNRELATED; the fourth review proposed UNSUPPORTED_EXACT/P_IMPLIES_O. Pane5 resolves the difference as follows: One initial carrier is sufficient for the sequential reading but not necessary under the retained orthogonal reading; false cannot reject the valid alternative repair. Fourth-review evidence: Exactly one CollisionAvoidanceSystem initial carrier to a direct child would satisfy the sequential encoding, but O also permits explicit orthogonal regions with one default per region. Thus P implies one permitted form of O, while O does not imply P and P=false cannot refute the obligation.
- capability gap：

  - Track B fcstm_sha256=sha256:b010de4155d5bbd258cdc8ccd4332baa63566087261aff86b0cfa5b1fea3d345 is the FCSTM_META file hash, not executable model.fcstm bytes sha256:165f4080834fc15e7d7e472552483c2349f1507da482de728c6920bd1b527b0f; Track C rebinds only to the Track A hash-bound model artifact.
  - Track B relation EQUIVALENT is corrected to UNRELATED; a false receipt cannot establish equivalence.
  - Track B proposed execution, but Track C rejects execution because the relation, complete typed binding, eligibility, or frozen oracle contract does not close.
  - Chronology defect: Track A records reviewed_at=2026-08-31T15:30:00Z, later than this truthful preflight freeze 2026-08-30T22:57:54.218535Z; no timestamp is fabricated to conceal it.

- arbitration：`predicate-gold-v1:EIS-0047-02`

## `EIS-0047-03`

- 分类：`EIS` / `D1` / `L0`；final relation `UNRELATED`
- 最近 proxy：无可靠 executable proxy
- unsupported reason：Pane5 final disposition is UNSUPPORTED_EXACT/UNRELATED. Track C and the independent fourth review agree on this boundary. Track C: Conditional submachine activation requires an external collision trigger and initial configuration semantics; no exact eligible property binds both. No execution is claimed; this avoids turning an unsound relation, incomplete binding, simulation-ineligible query, or missing oracle contract into fabricated evidence. Independent confirmation: Conditional activation of CollisionAvoidanceSystem requires an enclosing inactive context, collision stimulus mapping, and the intended relation between composite activation and local active controls. Those dimensions are absent, so no exact executable candidate can be formed.
- capability gap：

  - The source supplies no enclosing inactive state, orthogonal configuration semantics, or event-specific activation mapping.

- arbitration：`predicate-gold-v1:EIS-0047-03`

## `EIS-0050-01`

- 分类：`EIS` / `D1` / `L1`；final relation `UNRELATED`
- 最近 proxy：无可靠 executable proxy
- unsupported reason：Pane5 final disposition is UNSUPPORTED_EXACT/UNRELATED. Track C and the independent fourth review agree on this boundary. Track C: The response omission depends on system-wide event coverage and mode hierarchy; no complete source-backed finite carrier inventory was selected. No execution is claimed; this avoids turning an unsound relation, incomplete binding, simulation-ineligible query, or missing oracle contract into fabricated evidence. Independent confirmation: The three independently sufficient takeover conditions are collapsed into one free-text event, and V3 cannot bind the in(AutoFinal) state condition plus two external alternatives without an invented event interpretation. Track C's generic coverage wording omits this collapse; the evidence still supports only UNSUPPORTED_EXACT.
- capability gap：

  - The packet supplies no native carrier mapping for the multiline label and V3 cannot express the in(auto final) state condition as a trigger alternative.

- arbitration：`predicate-gold-v1:EIS-0050-01`

## `EIS-0053-01`

- 分类：`EIS` / `D2` / `L0`；final relation `UNRELATED`
- 最近 proxy：无可靠 executable proxy
- unsupported reason：Pane5 final disposition is UNSUPPORTED_EXACT/UNRELATED. Track C and the independent fourth review agree on this boundary. Track C: O requires hierarchical entry through PumpRegion to PumpState; it does not imply a direct PumpControl-owned [*]-to-PumpState edge. The selected S2 property collapses the wrapper and changes scope. No execution is claimed; this avoids turning an unsound relation, incomplete binding, simulation-ineligible query, or missing oracle contract into fabricated evidence. Independent confirmation: PumpControl entry must descend through PumpRegion to PumpState. A direct PumpControl-owned [*]-to-PumpState edge collapses the authored wrapper and is neither required nor sufficient for the hierarchical obligation; no exact hierarchy-entry property is selected.
- capability gap：

  - Track B fcstm_sha256=sha256:e1d2e4062d6dac6647c0184921a48f7426183a191d855d276a6f12b8569b7d25 is the FCSTM_META file hash, not executable model.fcstm bytes sha256:1b5b33eae1325d5a5b9b28fef84be55c8b4f4a294b69db95f38af2e48a8edf1b; Track C rebinds only to the Track A hash-bound model artifact.
  - Track B relation EQUIVALENT is corrected to UNRELATED; a false receipt cannot establish equivalence.
  - Track B proposed execution, but Track C rejects execution because the relation, complete typed binding, eligibility, or frozen oracle contract does not close.
  - Chronology defect: Track A records reviewed_at=2026-08-31T15:30:00Z, later than this truthful preflight freeze 2026-08-30T22:57:54.218535Z; no timestamp is fabricated to conceal it.

- arbitration：`predicate-gold-v1:EIS-0053-01`

## `EIS-0055-01`

- 分类：`EIS` / `D1` / `L0`；final relation `UNRELATED`
- 最近 proxy：无可靠 executable proxy
- unsupported reason：Pane5 final disposition is UNSUPPORTED_EXACT/UNRELATED. Track C and the independent fourth review agree on this boundary. Track C: The missing cooking-time writes have no source-backed variable/effect identity or value domain suitable for exact execution. No execution is claimed; this avoids turning an unsound relation, incomplete binding, simulation-ineligible query, or missing oracle contract into fabricated evidence. Independent confirmation: The model reads a zero-time condition yet provides no cooking-time declaration, domain, write, display action, or effect carrier. The source-compatible external-HMI reading also survives. An executable exact property would have to invent the missing data contract.
- capability gap：

  - No variable declaration, domain, update operation, display action, or effect carrier is source-bound.

- arbitration：`predicate-gold-v1:EIS-0055-01`

## `EIS-0056-01`

- 分类：`EIS` / `D2` / `L1`；final relation `O_IMPLIES_P`
- 最近 proxy：无可靠 executable proxy
- unsupported reason：Pane5 final disposition is UNSUPPORTED_EXACT/O_IMPLIES_P. Track C and the independent fourth review agree on this boundary. Track C: The universal priority obligation implies the one-step successor check only under a supported non-vacuous Intercepted occurrence. V3 is behavior-oriented on a simulation-ineligible artifact and cannot establish unbounded hierarchical priority. No execution is claimed; this avoids turning an unsound relation, incomplete binding, simulation-ineligible query, or missing oracle contract into fabricated evidence. Independent confirmation: Deterministic Intercepted handling entails the proposed one-step FormationAdjustment response only for a supported, non-vacuous occurrence. The artifact is simulation-ineligible and V3 cannot establish hierarchical priority or the universal configuration set, so the necessary relation remains unexecuted and exact gold unsupported.
- capability gap：

  - V3 is finite-horizon and cannot establish the full unbounded universal requirement or priority semantics.

- arbitration：`predicate-gold-v1:EIS-0056-01`

## `EIS-0056-02`

- 分类：`EIS` / `D1` / `L1`；final relation `UNRELATED`
- 最近 proxy：无可靠 executable proxy
- unsupported reason：Pane5 final disposition is UNSUPPORTED_EXACT/UNRELATED. Track C and the independent fourth review agree on this boundary. Track C: Distinguishing guard from decrement effect requires an exact carrier and data update identity; the current projection fuses the text into an event and cannot supply the required effect binding. No execution is claimed; this avoids turning an unsound relation, incomplete binding, simulation-ineligible query, or missing oracle contract into fabricated evidence. Independent confirmation: The bracketed decrement phrase cannot be bound as an effect because no UAV-count variable, type, decrement expression, or exact effect carrier exists. Treating the projected fused event as a data update would be a lowering-based invention.
- capability gap：

  - No UAV-count variable identity, type, decrement expression, or converted carrier ID is source-bound; S6 cannot parse the free phrase as one native operation.

- arbitration：`predicate-gold-v1:EIS-0056-02`

## `INS-0001-02`

- 分类：`INS` / `D2` / `L2`；final relation `UNRELATED`
- 最近 proxy：无可靠 executable proxy
- unsupported reason：Pane5 final disposition is UNSUPPORTED_EXACT/UNRELATED. Track C and the independent fourth review agree on this boundary. Track C: O permits another source-compatible reusable configuration, while P fixes only InitialState or OperationalState. Conversely, a guard-agnostic path can be infeasible and cannot prove O. The FCSTM contract also does not license whole-topology use. This pre-execution relation/capability rejection supports UNSUPPORTED_EXACT. The portable packet contains no execution receipt for this row, and no execution is claimed. Independent confirmation: Independent fourth source/semantics review: O permits another source-compatible reusable configuration, while P fixes only InitialState or OperationalState. Conversely, a guard-agnostic path can be infeasible and cannot prove O. The FCSTM contract also does not license whole-topology use. This pre-execution relation/capability rejection supports UNSUPPORTED_EXACT. The portable packet contains no execution receipt for this row, and no execution is claimed.
- capability gap：

  - V4 strengthens the quantifier and observable; G1 drops guards, event feasibility, and RTC timing.

- arbitration：`predicate-gold-v1:INS-0001-02`

## `INS-0002-02`

- 分类：`INS` / `D2` / `L2`；final relation `UNRELATED`
- 最近 proxy：无可靠 executable proxy
- unsupported reason：Pane5 final disposition is UNSUPPORTED_EXACT/UNRELATED. Track C and the independent fourth review agree on this boundary. Track C: Under a faithful representation O would imply a topology path to PumpState and therefore the broader disjunction. The packet withholds whole-topology eligibility, and P also cannot establish eventless same-RTC continuation. This pre-execution relation/capability rejection supports UNSUPPORTED_EXACT. The portable packet contains no execution receipt for this row, and no execution is claimed. Independent confirmation: Independent fourth source/semantics review: Under a faithful representation O would imply a topology path to PumpState and therefore the broader disjunction. The packet withholds whole-topology eligibility, and P also cannot establish eventless same-RTC continuation. This pre-execution relation/capability rejection supports UNSUPPORTED_EXACT. The portable packet contains no execution receipt for this row, and no execution is claimed.
- capability gap：

  - G1 drops guards/events; V4 changes both quantifier and response observable.

- arbitration：`predicate-gold-v1:INS-0002-02`

## `INS-0002-03`

- 分类：`INS` / `D2` / `L0`；final relation `UNRELATED`
- 最近 proxy：无可靠 executable proxy
- unsupported reason：Pane5 final disposition is UNSUPPORTED_EXACT/UNRELATED. Track C and the independent fourth review agree on this boundary. Track C: No complete S3 property is bindable because the packet has no native transition carrier. Even with a carrier, S3(empty triggers) would omit the required empty guard and would be only O_IMPLIES_P. This pre-execution relation/capability rejection supports UNSUPPORTED_EXACT. The portable packet contains no execution receipt for this row, and no execution is claimed. Independent confirmation: Independent fourth source/semantics review: No complete S3 property is bindable because the packet has no native transition carrier. Even with a carrier, S3(empty triggers) would omit the required empty guard and would be only O_IMPLIES_P. This pre-execution relation/capability rejection supports UNSUPPORTED_EXACT. The portable packet contains no execution receipt for this row, and no execution is claimed.
- capability gap：

  - S3 requires a unique native transition:line:<n>; author PlantUML and FCSTM line numbers are different provenance domains.

- arbitration：`predicate-gold-v1:INS-0002-03`

## `INS-0002-04`

- 分类：`INS` / `D2` / `L0`；final relation `UNRELATED`
- 最近 proxy：无可靠 executable proxy
- unsupported reason：Pane5 final disposition is UNSUPPORTED_EXACT/UNRELATED. Track C and the independent fourth review agree on this boundary. Track C: The native carrier is absent from allowed inputs. S3 alone would check only the trigger half of the triggerless-and-guardless O. This pre-execution relation/capability rejection supports UNSUPPORTED_EXACT. The portable packet contains no execution receipt for this row, and no execution is claimed. Independent confirmation: Independent fourth source/semantics review: The native carrier is absent from allowed inputs. S3 alone would check only the trigger half of the triggerless-and-guardless O. This pre-execution relation/capability rejection supports UNSUPPORTED_EXACT. The portable packet contains no execution receipt for this row, and no execution is claimed.
- capability gap：

  - S3 carrier provenance cannot be inferred across PlantUML-to-FCSTM conversion.

- arbitration：`predicate-gold-v1:INS-0002-04`

## `INS-0002-05`

- 分类：`INS` / `D2` / `L0`；final relation `UNRELATED`
- 最近 proxy：无可靠 executable proxy
- unsupported reason：Pane5 final disposition is UNSUPPORTED_EXACT/UNRELATED. Track C and the independent fourth review agree on this boundary. Track C: No native carrier binding is present; S3 alone would omit guard absence even if binding were repaired. This pre-execution relation/capability rejection supports UNSUPPORTED_EXACT. The portable packet contains no execution receipt for this row, and no execution is claimed. Independent confirmation: Independent fourth source/semantics review: No native carrier binding is present; S3 alone would omit guard absence even if binding were repaired. This pre-execution relation/capability rejection supports UNSUPPORTED_EXACT. The portable packet contains no execution receipt for this row, and no execution is claimed.
- capability gap：

  - S3 carrier provenance cannot be inferred across PlantUML-to-FCSTM conversion.

- arbitration：`predicate-gold-v1:INS-0002-05`

## `INS-0004-01`

- 分类：`INS` / `D2` / `L2`；final relation `UNRELATED`
- 最近 proxy：无可靠 executable proxy
- unsupported reason：Pane5 final disposition is UNSUPPORTED_EXACT/UNRELATED. Track C and the independent fourth review agree on this boundary. Track C: No candidate expresses the recovery-or-explicit-termination disjunction without inventing a recovery target or strengthening all downstream progress. This pre-execution relation/capability rejection supports UNSUPPORTED_EXACT. The portable packet contains no execution receipt for this row, and no execution is claimed. Independent confirmation: Independent fourth source/semantics review: No candidate expresses the recovery-or-explicit-termination disjunction without inventing a recovery target or strengthening all downstream progress. This pre-execution relation/capability rejection supports UNSUPPORTED_EXACT. The portable packet contains no execution receipt for this row, and no execution is claimed.
- capability gap：

  - V4 rejects permitted terminal outcomes; G1 cannot target termination and requires an invented recovery state.

- arbitration：`predicate-gold-v1:INS-0004-01`

## `INS-0004-02`

- 分类：`INS` / `D2` / `L2`；final relation `UNRELATED`
- 最近 proxy：无可靠 executable proxy
- unsupported reason：Pane5 final disposition is UNSUPPORTED_EXACT/UNRELATED. Track C and the independent fourth review agree on this boundary. Track C: A fixed DoorsClosing target is invented and V4 changes the response and quantifier; no exact termination-aware oracle is frozen. This pre-execution relation/capability rejection supports UNSUPPORTED_EXACT. The portable packet contains no execution receipt for this row, and no execution is claimed. Independent confirmation: Independent fourth source/semantics review: A fixed DoorsClosing target is invented and V4 changes the response and quantifier; no exact termination-aware oracle is frozen. This pre-execution relation/capability rejection supports UNSUPPORTED_EXACT. The portable packet contains no execution receipt for this row, and no execution is claimed.
- capability gap：

  - V4 treats terminal as no progress; G1 cannot represent explicit termination as a target and needs an invented reset state.

- arbitration：`predicate-gold-v1:INS-0004-02`

## `INS-0009-03`

- 分类：`INS` / `D1` / `L2`；final relation `UNRELATED`
- 最近 proxy：无可靠 executable proxy
- unsupported reason：Pane5 final disposition is UNSUPPORTED_EXACT/UNRELATED. Track C and the independent fourth review agree on this boundary. Track C: Track A adopts business-level mode-episode completion and retains root termination only as D1 sensitivity. That O can be satisfied by a logical FinishState marker with no root-exit carrier; a root-exit carrier can also exist without auto_finished completion semantics. This pre-execution relation/capability rejection supports UNSUPPORTED_EXACT. The portable packet contains no execution receipt for this row, and no execution is claimed. Independent confirmation: Independent fourth source/semantics review: Track A adopts business-level mode-episode completion and retains root termination only as D1 sensitivity. That O can be satisfied by a logical FinishState marker with no root-exit carrier; a root-exit carrier can also exist without auto_finished completion semantics. This pre-execution relation/capability rejection supports UNSUPPORTED_EXACT. The portable packet contains no execution receipt for this row, and no execution is claimed.
- capability gap：

  - V3 cannot bind terminated() or an unbounded response
  - V4 checks generic one-step progress
  - G1/G4 discard termination and event causality
  - the FCSTM is source-static eligible but simulation-ineligible

- arbitration：`predicate-gold-v1:INS-0009-03`

## `INS-0012-01`

- 分类：`INS` / `D2` / `L2`；final relation `UNRELATED`
- 最近 proxy：无可靠 executable proxy
- unsupported reason：Pane5 final disposition is UNSUPPORTED_EXACT/UNRELATED. Track C proposed EXACT_FALSE/EQUIVALENT; the fourth review proposed UNSUPPORTED_EXACT/UNRELATED. Pane5 resolves the difference as follows: The obligation permits either genuine termination semantics or removal of the unsupported path. One direct Off-to-root-exit carrier is neither necessary across those repairs nor sufficient for executable termination. Fourth-review evidence: The obligation is genuine terminal semantics if the path is retained, or removal of the unsupported path. One direct Off-to-root-exit carrier is neither necessary across those repairs nor sufficient for behavioral termination when trigger/guard feasibility is ignored; its false result cannot adjudicate O.
- capability gap：

  - V4 does not observe true termination identity.

- arbitration：`predicate-gold-v1:INS-0012-01`

## `INS-0019-01`

- 分类：`INS` / `D2` / `L2`；final relation `UNRELATED`
- 最近 proxy：无可靠 executable proxy
- unsupported reason：Pane5 final disposition is UNSUPPORTED_EXACT/UNRELATED. Track C and the independent fourth review agree on this boundary. Track C: A guard-agnostic G1 path to collision_avoidance_deactive is at most a necessary topology symptom and does not capture concurrency, default entry, event dispatch or runtime configuration semantics. Track C did not manufacture missing events, states, phases, variables, domains, bounds, or controls; the disposition is unsupported exactness rather than blocked execution. Independent confirmation: The required collision-avoidance behavior implies that the separately authored subsystem must be reachable/active, but the source does not define whether this is orthogonal concurrency, root switching, or another composition. Guard-agnostic topology reachability cannot express concurrent active configuration, local default entry, or event dispatch, so exact execution is unsupported.
- capability gap：

  - G1 is guard/event-agnostic topology and cannot establish orthogonal concurrent activation.
  - The FCSTM metadata permits only attribution-scoped source-static use and marks behavior/simulation ineligible.

- arbitration：`predicate-gold-v1:INS-0019-01`

## `INS-0023-01`

- 分类：`INS` / `D2` / `L2`；final relation `UNRELATED`
- 最近 proxy：无可靠 executable proxy
- unsupported reason：Pane5 final disposition is UNSUPPORTED_EXACT/UNRELATED. Track C and the independent fourth review agree on this boundary. Track C: V4 one-step model progress is only a necessary proxy; it neither proves eventual lifecycle continuation nor supplies the missing condition and destination. Track C did not manufacture missing events, states, phases, variables, domains, bounds, or controls; the disposition is unsupported exactness rather than blocked execution. Independent confirmation: PumpState is a reachable nonfinal operating state with no outgoing behavior, but the source omits the event, destination, fairness, and whether the three modes are sequential or orthogonal. One-step progress is only a necessary symptom and cannot be made obligation-equivalent from the available inputs.
- capability gap：

  - V4 is narrow one-step existential progress, not full operational continuation.
  - The source does not supply a recovery target/event or terminal classification.
  - Orthogonal runtime behavior is academically ineligible for the FCSTM.

- arbitration：`predicate-gold-v1:INS-0023-01`

## `INS-0023-02`

- 分类：`INS` / `D2` / `L2`；final relation `UNRELATED`
- 最近 proxy：无可靠 executable proxy
- unsupported reason：Pane5 final disposition is UNSUPPORTED_EXACT/UNRELATED. Track C and the independent fourth review agree on this boundary. Track C: V4 one-step model progress is only a necessary proxy and does not express eventual change among operating conditions. Track C did not manufacture missing events, states, phases, variables, domains, bounds, or controls; the disposition is unsupported exactness rather than blocked execution. Independent confirmation: WaterState is a reachable monitoring/control state with no exit, yet the source supplies no exact switching condition, target, ordering, or concurrency interpretation. V4-style progress would be a necessary proxy at most and is not an exact executable reference property.
- capability gap：

  - V4 is narrow one-step existential progress, not full operational continuation.
  - The source does not supply a recovery target/event or terminal classification.
  - Orthogonal runtime behavior is academically ineligible for the FCSTM.

- arbitration：`predicate-gold-v1:INS-0023-02`

## `INS-0023-03`

- 分类：`INS` / `D2` / `L2`；final relation `UNRELATED`
- 最近 proxy：无可靠 executable proxy
- unsupported reason：Pane5 final disposition is UNSUPPORTED_EXACT/UNRELATED. Track C and the independent fourth review agree on this boundary. Track C: V4 one-step progress is only a necessary proxy and cannot prove the source's continuing multi-condition lifecycle. Track C did not manufacture missing events, states, phases, variables, domains, bounds, or controls; the disposition is unsupported exactness rather than blocked execution. Independent confirmation: MethaneState is a reachable monitoring/control state with no exit, but no source-backed transition condition, destination, fairness rule, or region interaction is available. A generic progress check loses the condition-based lifecycle semantics and cannot serve as exact gold.
- capability gap：

  - V4 is narrow one-step existential progress, not full operational continuation.
  - The source does not supply a recovery target/event or terminal classification.
  - Orthogonal runtime behavior is academically ineligible for the FCSTM.

- arbitration：`predicate-gold-v1:INS-0023-03`

## `INS-0024-01`

- 分类：`INS` / `D2` / `L2`；final relation `UNRELATED`
- 最近 proxy：无可靠 executable proxy
- unsupported reason：Pane5 final disposition is UNSUPPORTED_EXACT/UNRELATED. Track C and the independent fourth review agree on this boundary. Track C: V4 one-step progress is a necessary proxy only; it does not express the disjunction between continuing lifecycle and legitimate finality. Track C did not manufacture missing events, states, phases, variables, domains, bounds, or controls; the disposition is unsupported exactness rather than blocked execution. Independent confirmation: Stopping is reachable and structurally dead-ended, but the author source does not state whether arrival is terminal or what post-arrival lifecycle, reset, or finality is intended. The ledger's controller-lifecycle reading is plausible domain reasoning, yet no exact destination, event, or termination property can be source-bound.
- capability gap：

  - V4 is only one-step existential progress and the source lacks post-stop target/event/terminal classification.
  - The FCSTM behavior profile is academically ineligible.

- arbitration：`predicate-gold-v1:INS-0024-01`

## `INS-0027-04`

- 分类：`INS` / `D2` / `L0`；final relation `UNRELATED`
- 最近 proxy：无可靠 executable proxy
- unsupported reason：Pane5 final disposition is UNSUPPORTED_EXACT/UNRELATED. Track C and the independent fourth review agree on this boundary. Track C: S4 needs exact actions and lifecycle phases; V4 observes only successor existence. Neither candidate proves that control behavior occurred before completion. Track C did not manufacture missing events, states, phases, variables, domains, bounds, or controls; the disposition is unsupported exactness rather than blocked execution. Independent confirmation: Concurrent activation of named control states does not provide source-backed action identities, lifecycle phases, completion events, durations, or success criteria. S4 would invent actions/phases and V4 observes only successor existence; neither proves behaviorally meaningful control execution.
- capability gap：

  - S4 cannot bind unnamed action identities or lifecycle phases.
  - V4 cannot establish behavior-before-completion.
  - No existing oracle observes nonempty control execution across orthogonal regions.

- arbitration：`predicate-gold-v1:INS-0027-04`

## `INS-0029-01`

- 分类：`INS` / `D2` / `L2`；final relation `UNRELATED`
- 最近 proxy：无可靠 executable proxy
- unsupported reason：Pane5 final disposition is UNSUPPORTED_EXACT/UNRELATED. Track C and the independent fourth review agree on this boundary. Track C: CollisionAvoidance must be active with driving, but the source omits the orthogonal composition mechanism. The source-static artifact is simulation-ineligible and no exact configuration oracle can be bound without inventing concurrency semantics. No query or control was manufactured; the final Track C disposition is unsupported rather than blocked execution. Independent confirmation: CollisionAvoidance must be active with driving, but the source omits the orthogonal composition mechanism. The source-static artifact is simulation-ineligible and no exact configuration oracle can be bound without inventing concurrency semantics. No query or control was manufactured; the final Track C disposition is unsupported rather than blocked execution.
- capability gap：

  - No orthogonal configuration oracle.
  - No source-declared concurrency encoding.
  - No admissible trajectory/BMC inputs.

- arbitration：`predicate-gold-v1:INS-0029-01`

## `INS-0034-01`

- 分类：`INS` / `D2` / `L2`；final relation `UNRELATED`
- 最近 proxy：无可靠 executable proxy
- unsupported reason：Pane5 final disposition is UNSUPPORTED_EXACT/UNRELATED. Track C and the independent fourth review agree on this boundary. Track C: No continuation target, event, explicit terminal intent, bound, fairness, or environment assumption is source-backed. A global deadlock check is neither issue-local nor admitted for this source-static artifact. No query or control was manufactured; the final Track C disposition is unsupported rather than blocked execution. Independent confirmation: No continuation target, event, explicit terminal intent, bound, fairness, or environment assumption is source-backed. A global deadlock check is neither issue-local nor admitted for this source-static artifact. No query or control was manufactured; the final Track C disposition is unsupported rather than blocked execution.
- capability gap：

  - Missing response target/event or terminal intent.
  - No bound/environment/fairness.
  - V4 is global, approximate, and artifact-ineligible.

- arbitration：`predicate-gold-v1:INS-0034-01`

## `INS-0039-03`

- 分类：`INS` / `D1` / `L0`；final relation `UNRELATED`
- 最近 proxy：无可靠 executable proxy
- unsupported reason：Pane5 final disposition is UNSUPPORTED_EXACT/UNRELATED. Track C and the independent fourth review agree on this boundary. Track C: The missing condition on enter_hwy-to-cruise needs an exact source carrier and condition interpretation; the packet does not provide a source-backed executable guard contract. No execution is claimed; this avoids turning an unsound relation, incomplete binding, simulation-ineligible query, or missing oracle contract into fabricated evidence. Independent confirmation: The source does not specify the complementary cruise guard or whether the bare enter_hwy-to-cruise edge is an intentional default before later lane-change evaluation. No exact condition property can be bound without resolving that D1 sensitivity by invention.
- capability gap：

  - NL does not state the cruise branch guard or an executable else/default condition.

- arbitration：`predicate-gold-v1:INS-0039-03`

## `INS-0039-04`

- 分类：`INS` / `D1` / `L2`；final relation `UNRELATED`
- 最近 proxy：无可靠 executable proxy
- unsupported reason：Pane5 final disposition is UNSUPPORTED_EXACT/UNRELATED. Track C and the independent fourth review agree on this boundary. Track C: The termination trap depends on grouped-transition RTC and post-FinishState behavior; no exact termination or unbounded cycle oracle is available from the eligible source-static artifact. No execution is claimed; this avoids turning an unsound relation, incomplete binding, simulation-ineligible query, or missing oracle contract into fabricated evidence. Independent confirmation: The claimed post-FinishState trap depends on D1 terminal intent, ancestor group-transition semantics, and unbounded future mode conditions. No eligible oracle expresses that termination/cycle property without a fairness or environment assumption.
- capability gap：

  - No fairness/environment restriction or unbounded termination observation is source-specified.

- arbitration：`predicate-gold-v1:INS-0039-04`

## `INS-0044-03`

- 分类：`INS` / `D1` / `L0`；final relation `UNRELATED`
- 最近 proxy：无可靠 executable proxy
- unsupported reason：Pane5 final disposition is UNSUPPORTED_EXACT/UNRELATED. Track C and the independent fourth review agree on this boundary. Track C: Whether EmergencyStopping may complete requires obstacle persistence, recovery/termination intent, and completion timing not executable from a source-static edge alone. No execution is claimed; this avoids turning an unsound relation, incomplete binding, simulation-ineligible query, or missing oracle contract into fabricated evidence. Independent confirmation: Whether EmergencyStopping may complete depends on obstacle persistence and whether the diagram ends a scenario or models continuing safety control. The source supplies no clearance event, recovery target, or termination rule, so exact execution is unsupported.
- capability gap：

  - The author NL supplies no obstacle-cleared event, guard, domain, or recovery/termination rule.

- arbitration：`predicate-gold-v1:INS-0044-03`

## `INS-0049-03`

- 分类：`INS` / `D1` / `L2`；final relation `UNRELATED`
- 最近 proxy：无可靠 executable proxy
- unsupported reason：Pane5 final disposition is UNSUPPORTED_EXACT/UNRELATED. Track C and the independent fourth review agree on this boundary. Track C: The post-FinishState mode-switch cycle is an unbounded grouped-transition/termination property with no eligible exact oracle. No execution is claimed; this avoids turning an unsound relation, incomplete binding, simulation-ineligible query, or missing oracle contract into fabricated evidence. Independent confirmation: The post-FinishState loop is an unbounded termination property under the retained terminal reading and ancestor transition semantics. No source-backed environment restriction or exact termination oracle is available.
- capability gap：

  - No unbounded termination/fairness semantics or environment restriction for mode guards is supplied.

- arbitration：`predicate-gold-v1:INS-0049-03`

## `INS-0050-01`

- 分类：`INS` / `D2` / `L0`；final relation `UNRELATED`
- 最近 proxy：无可靠 executable proxy
- unsupported reason：Pane5 final disposition is UNSUPPORTED_EXACT/UNRELATED. Track C and the independent fourth review agree on this boundary. Track C: The triggered initial-pseudostate violation lacks an exact native carrier binding, so a trigger-set execution would be unsupported. No execution is claimed; this avoids turning an unsound relation, incomplete binding, simulation-ineligible query, or missing oracle contract into fabricated evidence. Independent confirmation: The root initial carrier's Power On label must be checked as a trigger-set violation on its exact native carrier. That carrier identity is not bound, and a PlantUML line cannot replace it; exact execution is unsupported.
- capability gap：

  - The packet does not expose the converted FCSTM transition carrier ID required by S3.
  - S3 needs an exact converted transition:line:<n> carrier; an author PlantUML line number is not that native ID.

- arbitration：`predicate-gold-v1:INS-0050-01`

## `INS-0053-02`

- 分类：`INS` / `D2` / `L2`；final relation `O_IMPLIES_P`
- 最近 proxy：无可靠 executable proxy
- unsupported reason：Pane5 final disposition is UNSUPPORTED_EXACT/O_IMPLIES_P. Track C and the independent fourth review agree on this boundary. Track C: Real condition-specific progress implies that every reachable stable nonterminal leaf has a successor, but V4 is behavior/BMC-oriented, the artifact is simulation-ineligible, and the unspecified-initial projection creates vacuity risk. No execution is claimed; this avoids turning an unsound relation, incomplete binding, simulation-ineligible query, or missing oracle contract into fabricated evidence. Independent confirmation: Real condition-specific switching implies progress for reachable stable leaves, but V4 needs a valid initial behavioral scope. The synthetic unspecified initial makes the artifact simulation-ineligible and creates vacuity risk, while NL omits the actual switching events; the sound necessary relation cannot be executed.
- capability gap：

  - V4 proves only existential one-step progress for topology-selected leaves, not the required condition-specific transitions or full reachability.

- arbitration：`predicate-gold-v1:INS-0053-02`

## `INS-0054-01`

- 分类：`INS` / `D2` / `L2`；final relation `O_IMPLIES_P`
- 最近 proxy：无可靠 executable proxy
- unsupported reason：Pane5 final disposition is UNSUPPORTED_EXACT/O_IMPLIES_P. Track C and the independent fourth review agree on this boundary. Track C: A legitimate Stopping continuation or explicit termination implies at least one native outgoing/inherited carrier or final marker. The selected check is not exact, and no frozen oracle implements this terminal/progress disjunction. No execution is claimed; this avoids turning an unsound relation, incomplete binding, simulation-ineligible query, or missing oracle contract into fabricated evidence. Independent confirmation: A legitimate Stopping continuation or explicit termination necessarily needs an outgoing/inherited carrier or a final marker, but that disjunction is only a necessary structural condition and no frozen oracle implements it. The missing trip-versus-machine termination intent prevents exactness.
- capability gap：

  - Track B fcstm_sha256=sha256:385641d14d3f514b8fb17022ce99604d949b75b71f15679292096ff83e83da0e is the FCSTM_META file hash, not executable model.fcstm bytes sha256:34565710c66518ff94a26e6219cb9757a0ce74c4d3d476fd851a69f7f1e9f090; Track C rebinds only to the Track A hash-bound model artifact.
  - Track B relation EQUIVALENT is corrected to O_IMPLIES_P; a false receipt cannot establish equivalence.
  - Track B proposed execution, but Track C rejects execution because the relation, complete typed binding, eligibility, or frozen oracle contract does not close.
  - Chronology defect: Track A records reviewed_at=2026-08-31T15:30:00Z, later than this truthful preflight freeze 2026-08-30T22:57:54.218535Z; no timestamp is fabricated to conceal it.

- arbitration：`predicate-gold-v1:INS-0054-01`

## `INS-0054-02`

- 分类：`INS` / `D2` / `L2`；final relation `O_IMPLIES_P`
- 最近 proxy：无可靠 executable proxy
- unsupported reason：Pane5 final disposition is UNSUPPORTED_EXACT/O_IMPLIES_P. Track C and the independent fourth review agree on this boundary. Track C: A legitimate EmergencyStopping recovery or termination implies an outgoing/inherited carrier or final marker. Arbitrary outgoing structure would not prove the required recovery, and no frozen oracle implements the disjunction. No execution is claimed; this avoids turning an unsound relation, incomplete binding, simulation-ineligible query, or missing oracle contract into fabricated evidence. Independent confirmation: A legitimate EmergencyStopping recovery or explicit termination likewise needs an outgoing/inherited carrier or final marker. Arbitrary outgoing structure would not establish safe recovery, and the source supplies no clearance event or target; the necessary condition remains unexecuted.
- capability gap：

  - Track B fcstm_sha256=sha256:385641d14d3f514b8fb17022ce99604d949b75b71f15679292096ff83e83da0e is the FCSTM_META file hash, not executable model.fcstm bytes sha256:34565710c66518ff94a26e6219cb9757a0ce74c4d3d476fd851a69f7f1e9f090; Track C rebinds only to the Track A hash-bound model artifact.
  - Track B relation EQUIVALENT is corrected to O_IMPLIES_P; a false receipt cannot establish equivalence.
  - Track B proposed execution, but Track C rejects execution because the relation, complete typed binding, eligibility, or frozen oracle contract does not close.
  - Chronology defect: Track A records reviewed_at=2026-08-31T15:30:00Z, later than this truthful preflight freeze 2026-08-30T22:57:54.218535Z; no timestamp is fabricated to conceal it.

- arbitration：`predicate-gold-v1:INS-0054-02`

## `INS-0056-01`

- 分类：`INS` / `D2` / `L2`；final relation `EQUIVALENT`
- 最近 proxy：无可靠 executable proxy
- unsupported reason：Pane5 final disposition is UNSUPPORTED_EXACT/EQUIVALENT. Track C and the independent fourth review agree on this boundary. Track C: For the issue-local closed Area1/Area2/Area3 inventory, absence of a reachable eventless guardless SCC exactly captures the asserted zero-time completion loop. No frozen evaluator implements reachable completion-SCC detection, so execution cannot be claimed. No execution is claimed; this avoids turning an unsound relation, incomplete binding, simulation-ineligible query, or missing oracle contract into fabricated evidence. Independent confirmation: For the closed Area1/Area2/Area3 completion graph, absence of a reachable eventless, guardless SCC captures RTC stabilization and is obligation-equivalent. The source-backed scope is clear, but no frozen evaluation-only oracle implements reachable completion-SCC detection, so the row remains unsupported rather than blocked.
- capability gap：

  - Track B fcstm_sha256=sha256:77c0179bf9b8d89df0e066ea21b13730333f6ec79fedd3618585997e4f996424 is the FCSTM_META file hash, not executable model.fcstm bytes sha256:efb936daa0bfa3c15b604899d7251395fd491d674c036334558571061bcc664e; Track C rebinds only to the Track A hash-bound model artifact.
  - Track B proposed execution, but Track C rejects execution because the relation, complete typed binding, eligibility, or frozen oracle contract does not close.
  - Chronology defect: Track A records reviewed_at=2026-08-31T15:30:00Z, later than this truthful preflight freeze 2026-08-30T22:57:54.218535Z; no timestamp is fabricated to conceal it.

- arbitration：`predicate-gold-v1:INS-0056-01`

## `INS-0057-01`

- 分类：`INS` / `D2` / `L0`；final relation `UNRELATED`
- 最近 proxy：无可靠 executable proxy
- unsupported reason：Pane5 final disposition is UNSUPPORTED_EXACT/UNRELATED. Track C and the independent fourth review agree on this boundary. Track C: The triggered root initial edge needs exact carrier triggerlessness and initial-pseudostate semantics; no selected native carrier binding exists. No execution is claimed; this avoids turning an unsound relation, incomplete binding, simulation-ineligible query, or missing oracle contract into fabricated evidence. Independent confirmation: The root initial edge's Possible collision detected label requires an exact native carrier trigger-set check plus initial-pseudostate semantics. No such carrier binding is available, and the absent inactive parent/submachine context remains a limitation.
- capability gap：

  - The packet does not expose the converted FCSTM transition carrier ID required by S3.
  - S3 needs an exact converted transition:line:<n> carrier; an author PlantUML line number is not that native ID.

- arbitration：`predicate-gold-v1:INS-0057-01`

## `INS-0059-03`

- 分类：`INS` / `D1` / `L1`；final relation `UNRELATED`
- 最近 proxy：无可靠 executable proxy
- unsupported reason：Pane5 final disposition is UNSUPPORTED_EXACT/UNRELATED. Track C and the independent fourth review agree on this boundary. Track C: The missing condition on enter_hwy-to-cruise requires exact carrier/condition binding; the projection's event encoding cannot be upgraded to the required guard semantics. No execution is claimed; this avoids turning an unsound relation, incomplete binding, simulation-ineligible query, or missing oracle contract into fabricated evidence. Independent confirmation: The source does not define a complementary cruise guard or an executable else/default marker. The bare enter_hwy-to-cruise edge may be an immediate default under the retained D1 reading, so no exact condition property can be bound.
- capability gap：

  - NL does not define the cruise guard or an executable else/default marker.

- arbitration：`predicate-gold-v1:INS-0059-03`

## `VU-0001-01`

- 分类：`VU` / `D2` / `L2`；final relation `UNRELATED`
- 最近 proxy：无可靠 executable proxy
- unsupported reason：Pane5 final disposition is UNSUPPORTED_EXACT/UNRELATED. Track C and the independent fourth review agree on this boundary. Track C: The accepted O does not exhaustively require InitialState or OperationalState as the recovery target. A topology path to those states also omits trigger consumption and RTC feasibility, and the topology representation is not eligible here. This pre-execution relation/capability rejection supports UNSUPPORTED_EXACT. The portable packet contains no execution receipt for this row, and no execution is claimed. Independent confirmation: Independent fourth source/semantics review: The accepted O does not exhaustively require InitialState or OperationalState as the recovery target. A topology path to those states also omits trigger consumption and RTC feasibility, and the topology representation is not eligible here. This pre-execution relation/capability rejection supports UNSUPPORTED_EXACT. The portable packet contains no execution receipt for this row, and no execution is claimed.
- capability gap：

  - G1 is guard-agnostic; V4 is universally stronger than O.

- arbitration：`predicate-gold-v1:VU-0001-01`

## `VU-0009-01`

- 分类：`VU` / `D2` / `L2`；final relation `UNRELATED`
- 最近 proxy：无可靠 executable proxy
- unsupported reason：Pane5 final disposition is UNSUPPORTED_EXACT/UNRELATED. Track C proposed SOUND_FALSE_PROXY/O_IMPLIES_P; the fourth review proposed UNSUPPORTED_EXACT/UNRELATED. Pane5 resolves the difference as follows: fcstm_meta withholds whole-model behavior equivalence, simulation and concurrent-region closure. Root G1 reachability on the converted topology is not an O-implied author-level initialization property. Fourth-review evidence: Independent fourth review accepts the requirement that CollisionAvoidanceSystem be initialized with the driving system, but does not accept root G1 reachability as O-implied under the declared representation contract. A sequential native graph path neither establishes concurrent initial occupancy nor is it guaranteed by an author-level obligation when whole-model behavior equivalence is withheld. The active forced-carrier control is true and both replays match, but Boolean closure cannot repair that semantic gap; the disposition is UNSUPPORTED_EXACT/UNRELATED.
- capability gap：

  - orthogonal_runtime_configuration is unsupported
  - G1 cannot represent simultaneous active regions
  - S2 second-initial-edge encoding is semantically wrong
  - V5 permanent occupancy changes the initial-state obligation

- arbitration：`predicate-gold-v1:VU-0009-01`

## `VU-0011-01`

- 分类：`VU` / `D2` / `L2`；final relation `UNRELATED`
- 最近 proxy：无可靠 executable proxy
- unsupported reason：Pane5 final disposition is UNSUPPORTED_EXACT/UNRELATED. Track C proposed SOUND_FALSE_PROXY/O_IMPLIES_P; the fourth review proposed UNSUPPORTED_EXACT/UNRELATED. Pane5 resolves the difference as follows: A same-RTC response may use a compound pseudostate route, so O does not require one direct event/target carrier. A guarded direct carrier also does not establish feasible event consumption or the next stable configuration. Fourth-review evidence: The selected direct event/target carrier is neither necessary nor sufficient for the RTC response. A compound route can satisfy O with P=false, and an infeasible guarded direct carrier can make P=true while O remains false; the completed false/control/replay evidence is not a sound falsifier.
- capability gap：

  - Static carrier presence does not prove event consumption or RTC feasibility.
  - V4 loses the named event and target.

- arbitration：`predicate-gold-v1:VU-0011-01`

## `VU-0017-01`

- 分类：`VU` / `D1` / `L0`；final relation `UNRELATED`
- 最近 proxy：无可靠 executable proxy
- unsupported reason：Pane5 final disposition is UNSUPPORTED_EXACT/UNRELATED. Track C and the independent fourth review agree on this boundary. Track C: A local incoming/root carrier is not necessary under the adopted external-entry reading, so the Track B property is unrelated to O rather than equivalent. No query or control was manufactured; the final Track C disposition is unsupported rather than blocked execution. Independent confirmation: Under the adopted external-entry reading, no carrier inside this artifact is necessary; under the retained self-contained reading, the property still omits collision-detection triggering and concurrent next-stable activation. No single local incoming-carrier query is equivalent or a sound falsifier.
- capability gap：

  - S2 cannot quantify over an unspecified source endpoint.
  - G1 is path connectivity, not incoming-carrier identity.
  - External-parent activation is unobservable in this artifact and remains D1 sensitivity.

- arbitration：`predicate-gold-v1:VU-0017-01`

## `VU-0040-01`

- 分类：`VU` / `D2` / `L0`；final relation `UNRELATED`
- 最近 proxy：无可靠 executable proxy
- unsupported reason：Pane5 final disposition is UNSUPPORTED_EXACT/UNRELATED. Track C and the independent fourth review agree on this boundary. Track C: The root initial edge's trigger violation requires an exact carrier-level trigger-set binding. No eligible selected property binds that native carrier. No execution is claimed; this avoids turning an unsound relation, incomplete binding, simulation-ineligible query, or missing oracle contract into fabricated evidence. Independent confirmation: The root initial carrier must be triggerless, but S3 requires its exact converted transition identity and the packet does not provide it. Power On cannot be guessed into a separate lifecycle query.
- capability gap：

  - The packet does not expose the converted FCSTM transition carrier ID required by S3.
  - S3 needs an exact converted transition:line:<n> carrier; an author PlantUML line number is not that native ID.

- arbitration：`predicate-gold-v1:VU-0040-01`

## `VU-0046-01`

- 分类：`VU` / `D1` / `L0`；final relation `UNRELATED`
- 最近 proxy：无可靠 executable proxy
- unsupported reason：Pane5 final disposition is UNSUPPORTED_EXACT/UNRELATED. Track C and the independent fourth review agree on this boundary. Track C: Universal Intercepted coverage over all active states needs a complete source-backed state domain and inherited-priority semantics; neither is bound by an eligible candidate. No execution is claimed; this avoids turning an unsound relation, incomplete binding, simulation-ineligible query, or missing oracle contract into fabricated evidence. Independent confirmation: Universal Intercepted coverage over all SearchRegion children depends on the D1 global-versus-Searching-only scope and repeat-interception behavior. No complete source-backed state domain or inherited-priority property is available.
- capability gap：

  - The source does not define whether Idle, FormationAdjustment, or Attacking belongs to the trigger scope or how repeat interception is handled.

- arbitration：`predicate-gold-v1:VU-0046-01`

## `VU-0054-01`

- 分类：`VU` / `D1` / `L0`；final relation `UNRELATED`
- 最近 proxy：无可靠 executable proxy
- unsupported reason：Pane5 final disposition is UNSUPPORTED_EXACT/UNRELATED. Track C and the independent fourth review agree on this boundary. Track C: Strict UML completion timing for a guard-only InMotion exit requires exact trigger/guard carrier semantics and compound completion state, which are not bound by a supported candidate. No execution is claimed; this avoids turning an unsound relation, incomplete binding, simulation-ineligible query, or missing oracle contract into fabricated evidence. Independent confirmation: The strict-UML reading treats the bracket-only obstacle label as a guard on a completion transition, but exact review needs the carrier's trigger/guard split and InMotion completion configuration. Those bindings are unavailable, and the informal-condition alternative remains live.
- capability gap：

  - The packet does not expose the converted FCSTM carrier ID required by S3.
  - S3 needs an exact converted transition:line:<n> carrier; an author PlantUML line number is not that native ID.

- arbitration：`predicate-gold-v1:VU-0054-01`

## `VU-0059-02`

- 分类：`VU` / `D1` / `L1`；final relation `UNRELATED`
- 最近 proxy：无可靠 executable proxy
- unsupported reason：Pane5 final disposition is UNSUPPORTED_EXACT/UNRELATED. Track C and the independent fourth review agree on this boundary. Track C: Mutual exclusion/priority among three urban maneuvers needs a complete valuation domain and scheduler policy absent from the author source. No execution is claimed; this avoids turning an unsound relation, incomplete binding, simulation-ineligible query, or missing oracle contract into fabricated evidence. Independent confirmation: Mutual exclusion or priority across the three urban maneuvers needs a closed valuation domain, environment invariant, and scheduler policy. None is supplied; executing selected valuations would silently narrow the universal obligation.
- capability gap：

  - No closed domain, environment invariant, or priority order is supplied; V1 cannot invent domain values or compare separate trigger groups beyond its exact contract.

- arbitration：`predicate-gold-v1:VU-0059-02`
