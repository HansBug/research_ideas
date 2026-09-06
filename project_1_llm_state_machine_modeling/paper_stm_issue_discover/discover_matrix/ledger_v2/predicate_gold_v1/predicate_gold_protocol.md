# Predicate gold v1 protocol

## Status and scope

This protocol defines the evaluation-only predicate gold for the 145 current
`ledger_v2` issues. It does not change the ledger, the frozen v60 method, the
19-predicate registry, raw method or Judge output, or current/baseline semantic
decisions. Gold data must not be imported by the method package, included in a
discovery prompt, or used as a routing input.

The canonical annotation unit is one current ledger ID. The annotation first
recovers a normative obligation `O` from the author NL and source artifact. It
then compares executable candidate properties `P` with `O`. A backend `false`
is execution evidence only; it cannot establish that `P` expresses `O`.

The protocol version is `paper1.obligation-equivalent-predicate-gold.v1`.
Canonical JSON is the fact source. Tables and prose are derived views.

## What "exact" means here

`obligation-equivalent executable reference property` is the paper-facing
term. The project calls a property exact only when the following claim is
supported under an explicit FCSTM semantic profile, scope, observation model,
and environment assumption:

`O <=> P`

This is a project operationalization assembled from requirements
formalization, oracle adequacy, behavioral refinement, trace semantics,
vacuity, model checking, and UML state-machine semantics. No cited source is
claimed to define this complete rubric or a universal "most precise predicate"
ordering. In particular, there is no fixed `S < G < R < V` precision ranking.
A source-static property can be exact for an authored-edge obligation, while a
bounded or trajectory property can be only a proxy for a broader obligation.

The implication labels have the following fixed meanings:

| Relation | Interpretation | Exact gold? |
| --- | --- | --- |
| `EQUIVALENT` | `O => P` and `P => O` under the same declared semantics and assumptions | Yes, if execution and review gates also pass |
| `O_IMPLIES_P` | `P` is a necessary condition of `O`; therefore `P=false` soundly entails `O=false` | No; eligible only as a sound false proxy |
| `P_IMPLIES_O` | `P=false` does not entail `O=false` | No |
| `UNRELATED` | No defensible implication has been established | No |

The direction used for a false proxy is deliberate: from `O => P`, the
contrapositive gives `not P => not O`. Barr et al.'s oracle definitions support
reasoning in explicit implication directions, but the four labels and their
mapping to this dataset are project choices.

## Obligation normalization

Track A reads the complete author NL, author PlantUML/source, current ledger
entry and provenance, and the applicable formal semantics. It does not read a
planned predicate mapping, v60 actual predicate/input output, another track's
conclusion, or an execution result.

Each normalized obligation records:

| Dimension | Required content |
| --- | --- |
| Subject | Component and exact author/source artifact |
| Quantifier | Existential, universal, uniqueness, cardinality, or closed finite inventory |
| Trigger and precondition | Offered/dispatched/processed event, guard, state, variable, or explicit absence |
| Scope | Global, state/region local, before/after/between, or reachable configuration set |
| Response | Required or forbidden state, action, variable value, trace event, or termination observation |
| Timing | Same RTC, next stable configuration, explicit finite bound, eventuality, or sustained interval |
| Observable | Authored carrier, native state/configuration, action/effect, variable, or machine termination |
| Assumptions | Only source-backed domain, initial scope, aliases, bounds, and environment restrictions |
| Missing information | Every value needed for execution but absent from the source; it is never invented |

For `D1`, the annotation retains at least two complete source-compatible
readings and states which ledger reading is adopted. Ambiguity is not removed
to make an executable query possible. A reference model, v60 finding, old
planned mapping, or observed `false` cannot supply a missing author fact.

FRET/FRETish supports separating component, scope, condition, timing and
response rather than treating a requirement as an unstructured paraphrase.
Dwyer et al. support reusable property patterns as a specification aid. Neither
source establishes the truth of an issue-specific formalization.

## Candidate comparison

Track B independently reads the same blind source packet plus the frozen
registry, backend implementation, pyfcstm source and capability audit. It
enumerates all semantically credible candidates before execution. Every
candidate records typed inputs, provenance, assumptions, the implication
direction, and a concrete semantic gap if it is rejected.

Candidates are compared on at least these dimensions:

1. quantifier and cardinality;
2. trigger, precondition, response and observation;
3. global, temporal, owner, state, region and configuration scope;
4. RTC, next-stable, bounded, eventual and until timing;
5. pseudostate, compound transition, hierarchy, orthogonal region,
   completion, entry/exit/effect and event-consumption semantics;
6. authored direct edge, macro topology, executable trace, variable/action,
   FinalState and whole-machine termination observations;
7. added environment, domain, initial-state and bound assumptions;
8. vacuity, over/under-approximation, finite horizon, projection/lowering and
   source-attribution risks.

When several properties are equivalent to `O`, the selected property uses the
fewest extra assumptions and the closest source-backed scope, timing and
observable. Implementation length and likelihood of returning `false` are not
selection criteria. The proposal, candidate and typed-input payload is hashed
before same-issue execution.

### Mandatory semantic boundaries

- `S2 transition_exists` can be exact when `O` explicitly requires one
  authored direct carrier with those endpoints. It does not by itself express
  an event-conditioned RTC response.
- A pseudostate path such as `A -> P -> B` can complete within one compound
  transition. `S2(A,B)=false` is therefore not automatically evidence against
  an RTC obligation.
- `G1 may_reach` is guard-agnostic macro topology. It can be a sound necessary
  condition for some reachability obligations, but it does not establish event,
  guard, variable, step or timing feasibility.
- A single scenario witness can refute a universal response property, but the
  scenario is not the universal property itself.
- A UML `FinalState` denotes completion of its enclosing Region. One top-level
  Region completing denotes whole-StateMachine Behavior completion only when
  every other Region directly contained in that StateMachine is also complete.
  A terminate pseudostate instead terminates execution immediately without
  ordinary State exit behavior. A named leaf, an ordinary no-outgoing State,
  Region completion, whole-machine completion, terminate-pseudostate entry and
  pyfcstm `terminated()` are therefore distinct observations unless a checked
  backend mapping establishes a narrower correspondence.
- Initial-pseudostate carrier, trigger-set, guard/effect and owner-local source
  obligations may be expressed most exactly by source-static predicates.
- Bounded properties are exact only for an obligation with an independently
  justified bound/domain, or when a documented completeness result applies.
  Absence of a bounded counterexample is not an unbounded proof.
- No missing variable, event, target state, domain, bound or initial
  configuration may be supplied merely to make a query executable.

The 19-predicate semantics and known contract/runtime mismatches are recorded
in `predicate_semantics_capability_audit.json`. An evaluation-only oracle is
permitted only when it uses pyfcstm's native parser/model/semantics and remains
physically outside the method package and registry. PlantUML regex parsing,
fuzzy state matching, and a second hand-written state-machine runtime are
forbidden.

## Typed input provenance

Every input stores its JSON type, exact and normalized values, source role,
source path and pointer/line, stable native object ID where applicable, alias
resolution, and binding reason. Author NL/source, formal semantics, and an
explicit evaluation assumption are distinct provenance roles. Conversion
artifacts may bind an executable object only when the inventory preserves the
source attribution needed by `O`.

Input selection is source-first. The following are not admissible provenance:

- string similarity or a guessed state name;
- a regex interpretation of PlantUML;
- a reference-model element substituted for the defective author artifact;
- an old planned mapping or v60 actual input copied into gold;
- a window, bound, domain, initial configuration or stimulus changed after
  observing the verdict.

## Execution and controls

An executable proposal is run only after its proposal and request hashes are
sealed. Exact and executed-proxy dispositions require a terminal Boolean
`false` on the defective FCSTM bytes. Timeout, error, invalid input,
unsupported backend, exception, empty output and unknown are not `false`.

Receipts preserve the complete query, typed inputs, backend and code identity,
artifact hash, domain/bound/seed where applicable, start/end time, normalized
verdict, trace or static counterexample, and replay result. A composite executes
and stores every constituent without short-circuiting.

Each executed property also needs a precommitted positive control that returns
terminal Boolean `true`. A source-justified minimal repair is preferred. The
control provenance must state exactly what changed and why it repairs the same
obligation without changing unrelated semantics. The control is an error- and
binding-detection device, not proof that the property is equivalent to `O`.

Track C sees the frozen Track A/B rows and execution packet only after
execution. It independently checks the O/P relation, native bindings,
completed verdict, positive control, trace/counterexample, vacuity,
contamination and replay. `false` alone is never an exactness argument.

## Final dispositions

| Status | Final condition |
| --- | --- |
| `EXACT_FALSE` | One `EQUIVALENT` executable property, defective `false`, justified control `true`, matching replay and closed review |
| `COMPOSITE_EXACT_FALSE` | An `EQUIVALENT` non-short-circuit composition with every constituent receipted, overall defective `false`, control `true`, replay and closed review |
| `SOUND_FALSE_PROXY` | Only an `O_IMPLIES_P` property is executable; defective `false`, control `true`, replay and the missing exact dimensions remain explicit |
| `UNSUPPORTED_EXACT` | `O` is normalized, but frozen predicates, auditable composites and pyfcstm-native evaluation capabilities cannot express an equivalent executable property with source-backed inputs |
| `BLOCKED_EXECUTION` | Working state for an exact query without a Boolean result; forbidden in final canonical data |

An unsupported row still records candidates, relation directions, capability
gaps, nearest sound proxy where one exists, all three review tracks and pane5
arbitration. Unsupported is not a failed experiment and no target count is set
for exact coverage.

## Independence, arbitration and leakage

Every ledger ID receives hash-bound Track A, Track B and Track C opinions from
distinct internal reviewers. These are internal quality-assurance tracks, not
an inter-rater human study. Track A and B are blind to each other and to v60
actual output. Track C is post-proposal and post-execution by design. Conflicts
retain both positions and are resolved by pane5 from source and semantic
evidence; majority vote and confidence are not decision rules.

Gold is evaluated against frozen v60 output only after all expected rows are
final. The expected-vs-actual matrix is diagnostic. A method finding may use a
different sound, correctly attributed and actually executed property without
being downgraded. Gold never changes hit, W or K/N/I labels.

## Primary-source support and project choices

The complete claim records, locators, short quotations, support boundaries and
stable links are in `academic_claim_to_source_matrix.json`. The bounded uses are:

| Claim ID | Source and locator | What it supports here |
| --- | --- | --- |
| `PG-REQ-DWYER-1999` | Dwyer, Avrunin & Corbett, ICSE 1999, DOI `10.1145/302405.302672`, IEEE abstract | Reusable finite-state property patterns as normalization aids |
| `PG-REQ-FRET-2020` | Giannakopoulou et al., FRET, CEUR-WS 2584, Sections 1-3, PDF pp. 1-5 | Explicit component/scope/condition/timing/response fields and semantic checks |
| `PG-ORACLE-BARR-2015` | Barr et al., IEEE TSE 41(5), DOI `10.1109/TSE.2014.2372785`, Section 2.3, printed p. 510 | Oracle soundness/completeness as directional implications and partial-oracle limits |
| `PG-VACUITY-BEER-2001` | Beer et al., FMSD 18(2), DOI `10.1023/A:1008779610539`, IBM Research abstract | Vacuous truth when an antecedent cannot affect a temporal property |
| `PG-MBT-TRETMANS-2008` | Tretmans, DOI `10.1007/978-3-540-78917-8_1`, Abstract and Section 1, pp. 1-2 | Tests require a valid conformance model and do not prove absence of all errors |
| `PG-UML-INITIAL-2017` | OMG UML 2.5.1, clauses 14.2.3.2, 14.2.3.7, 14.5.6.7, pp. 307, 312, 350 | Initial pseudostate cardinality and no-trigger/no-guard constraints |
| `PG-UML-RTC-2017` | OMG UML 2.5.1, clause 14.2.3.9.1, pp. 316-317 | Event dispatch and RTC stable-configuration semantics |
| `PG-UML-COMPLETION-2017` | OMG UML 2.5.1, clauses 14.2.3.2, 14.2.3.6-7, 14.2.3.9.1, 14.5.2.1 and 14.5.2.5, pp. 307, 312-313, 316, 346 | Region FinalState completion, whole-machine completion and immediate terminate-pseudostate semantics are distinct |
| `PG-REFINEMENT-ABADI-LAMPORT-1991` | Abadi & Lamport, DOI `10.1016/0304-3975(91)90224-P`; SRC Research Report 29, Section 2.4, printed p. 11 (PDF p. 17) | Behavioral inclusion/refinement, used to require both directions for equivalence |
| `PG-TRACE-HAREL-NAAMAD-1996` | Harel & Naamad, DOI `10.1145/235321.235322`, Section 2, pp. 298-299 | Runs as semantic step/status sequences under a fixed execution profile |
| `PG-BMC-BIERE-1999` | Biere et al., DOI `10.1007/3-540-49059-0_14`, Sections 1 and 6, pp. 194, 205 | Explicit horizon and the bounded/unbounded proof boundary |
| `PG-CEX-CLARKE-2000` | Clarke et al., DOI `10.1007/10722167_15`, Section 1, pp. 154-155 | Abstract counterexamples require correspondence to a concrete execution |

The three-track workflow, pane5 arbitration, positive-control contamination
checks, four implication labels and final status taxonomy are project-engineered
controls. The sources above motivate their component concepts; they do not
validate this exact annotation process or guarantee that an internal reviewer
recovers ground truth. No measured effectiveness claim is made for this
workflow or for the positive-control construction; that unvalidated
effectiveness is an explicit method limitation rather than a literature claim.

## Mechanical release gates

Release requires all 145 current ledger IDs exactly once; matching ledger,
source and artifact hashes; schema-valid JSON/TSV/summary; zero final
`BLOCKED_EXECUTION`; completed/replayed receipts and controls for every executed
status; three distinct review tracks and closed arbitration for every row; and
academic, leakage and numeric/artifact review. Provider, method, Judge and 54x3
rerun counters must all remain zero.
