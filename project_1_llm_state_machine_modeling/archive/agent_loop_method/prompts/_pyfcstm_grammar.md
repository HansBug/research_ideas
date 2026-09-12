# pyfcstm DSL — comprehensive grammar reference

> Single source of truth for every agent (Modeler / Repair / future scenariogen
> sanity checks) that produces or edits pyfcstm DSL. **Every code snippet below
> has been verified to parse and convert to a state-machine model via the
> actual pyfcstm runtime**. Treat this document as authoritative; do not
> "guess from memory".
>
> The snippets below may contain human explanatory comments. Comments are **not**
> part of the DSL output contract: when generating or repairing a model, never
> emit `// ...` or `/* ... */` comments in the DSL text.

---

## 1. Top-level file structure

```
def int counter = 0;             // variable definitions (int / float) BEFORE root
def float temp = 25.0;
def int armed = 0;                // boolean-like flags use int 0/1

state Root { ... }               // EXACTLY ONE top-level state
```

**Rules**:
- All variable definitions must appear **before** the root `state Root { ... }` block.
- There must be **exactly one** top-level state. If conceptually you have multiple
  systems, wrap them in a single synthesized parent state.

---

## 2. Variable declarations

```
def int counter = 0;
def float temp = 25.0;
def int armed = 0;
```

Only `int` and `float` variable declarations are accepted by the current
pyfcstm parser. Boolean-like flags MUST be encoded as `int` variables with
`0`/`1` values, for example `def int fault = 0;`; guards should use
`fault > 0` or `fault == 0`, and effects should assign `fault = 1;` or
`fault = 0;`. Do not emit `def bool`, `true`, `false`, C-style
`!flag` flag tests, or unsupported helpers such as `max(...)` / `min(...)`.
Assignments use ordinary `x = x + 1;` syntax, not C-style `x += 1;`.

Discrete trigger names from the NL, such as button presses, reset events,
fault events or back-to-manual events, should normally be encoded as event
transitions with `:: EventName`. Do not turn several alternative events into an
undeclared boolean guard like `[A || B]`; use separate event transitions unless
the NL explicitly defines those names as boolean input variables.

Variables are referenced inside guards `[<expr>]`, effects `{ <stmt>; }`,
and lifecycle blocks (`enter` / `during` / `exit`). Every variable used
anywhere MUST be declared at the top — undeclared references fail at
**semantic validation** (passes parse, fails sem).

---

## 3. State definitions

```
state A;                                              // leaf, declaration only (no body)
state B { during { counter = counter + 1; } }         // leaf with lifecycle action
state Composite {                                     // composite (has children)
    [*] -> Child;                                     // composite MUST have an initial transition
    state Child;
}
pseudo state Junction;                                // non-stoppable routing state
```

**Rules**:
- A **composite state** (one with nested states inside) MUST contain an
  initial transition `[*] -> <one of its children>;` — otherwise the model
  doesn't know which child to enter.
- A **leaf state** has no nested children; it may have lifecycle actions
  but no `[*] -> ...` inside.
- A `pseudo state` is a routing-only state (you can transition through it,
  but the runtime never stops there at a cycle boundary).

---

## 4. Initial transition

```
[*] -> A;                                            // simple — enter A by default
[*] -> A :: Start effect { counter = 0; };           // optionally event-triggered + effect
```

Used inside any composite state body (including the root) to declare where
that scope is entered by default.

---

## 5. Lifecycle actions (inside a state body)

```
state A {
    enter { counter = 0; }                            // runs once on entry
    during { counter = counter + 1; }                 // runs each cycle while active (leaf only)
    exit  { counter = 0; }                            // runs once on exit

    enter abstract InitHardware;                      // abstract placeholder (Python handler @ runtime)
    exit abstract CloseHardware;
}
```

- `during` only runs on **leaf** active states. For composites the during
  semantics is via aspect actions (next section).
- `abstract` lifecycle blocks declare a name that pyfcstm dispatches to a
  Python handler at runtime; the DSL itself has no body for them.

---

## 6. Aspect actions `>> during before/after` (composite states ONLY)

```
state Composite {
    >> during before { counter = counter + 1; }      // before EVERY descendant leaf's during
    >> during after  { counter = counter * 2; }       // after EVERY descendant leaf's during
    [*] -> Leaf;
    state Leaf { during { counter = counter + 1; } }
}
```

Use these to express "every cycle while *anywhere in this region*, do X".

---

## 7. Transitions — SCOPE rules (the most error-prone area)

General shape:

```
Source -> Dest [SCOPE] (; | effect { ... })
```

`SCOPE` is **at most one** of the four forms below. **Event and guard are
mutually exclusive on the same transition** (the parser rejects mixing).

| Form | Event path resolved as | Semantic meaning |
| --- | --- | --- |
| `S1 -> S2 :: Tick` | `<Parent>.S1.Tick` | **LOCAL** — event lives in the source-state namespace. Two siblings each writing `:: Tick` listen to **different** events. |
| `S1 -> S2 : Tick` | `<Parent>.Tick` | **CHAIN / parent-relative** — event lives in the enclosing parent's namespace. Siblings sharing `: Tick` listen to the **same** event. |
| `S1 -> S2 : /Sub.Tick` | `<RootName>.Sub.Tick` | **ABSOLUTE** — `/` *itself represents Root* — do NOT repeat the root state name after `/`. `/Sub.Tick` means "Tick event owned by direct child Sub of the root". `/Tick` means "Tick owned by Root itself". |
| `S1 -> S2 : if [expr]` | (no event) | **GUARD** (no event); the leading `:` is REQUIRED. |

**Absolute-path warning**: if your root state is named `Plant` and you want
to reference an event under `Plant.Sub`, write `: /Sub.X` — NOT
`: /Plant.Sub.X`. Writing the root name after `/` causes pyfcstm to look
for `Plant.Plant.Sub` and fail with "Cannot find state".

**Choosing `::` vs `:`**: use `::` when the event is conceptually owned by
the source state (e.g. each operating mode has its own "timeout" event).
Use `:` (chain) or `: /...` (absolute) when one event triggers
transitions from multiple sibling states (e.g. a global "Reset" or a
parent-level "Tick" observed by several children).

### 7.1 Valid transition forms (all parse + convert)

```
A -> B;                                              // bare
A -> B effect { counter = 0; };                      // effect-only
A -> B :: Tick;                                      // event-only (LOCAL scope)
A -> B :: Tick effect { counter = 0; };              // event + effect
A -> B : Tick;                                       // event with CHAIN scope (parent's namespace)
A -> B : /Global;                                    // event with ABSOLUTE scope (Root itself)
A -> B : /Sub.Tick;                                  // event under direct child Sub of Root
A -> B : if [counter > 0];                           // guard-only (leading `:` REQUIRED)
A -> B : if [counter > 0] effect { counter = 0; };   // guard + effect
[*] -> A;                                            // initial
[*] -> A :: Start effect { counter = 0; };           // initial + event + effect
A -> [*];                                            // exit-to-parent
```

### 7.2 Invalid transition forms (parser will reject)

```
A -> B :: Tick if [counter > 0];                     // ✗ event + guard cannot coexist
A -> B :: Tick : if [counter > 0];                   // ✗ same (with explicit `:`)
A -> B if [counter > 0];                             // ✗ guard MUST have leading `:`
A -> B :: if [counter > 0];                          // ✗ `if` is not an event name — `::` expects identifier
A -> B [if [counter > 0]];                           // ✗ no operator before guard
A -> B : counter;                                    // ✗ `:` followed by bare identifier (use `:: counter` if it's an event)
```

If the NL says "event Tick triggers transition only when counter > 0", you
must encode it as a guard, **dropping the event name**:

```
A -> B : if [tick_seen >= 1 && counter > 0] effect { tick_seen = 0; };
```

(or restructure: bring the event into the model only as an indicator
variable that ``during`` increments, then transition on the variable.)

---

## 8. Forced transitions (`!` prefix)

Same SCOPE rules as ordinary transitions — except **forced transitions DO
NOT support `effect { ... }` blocks** (grammar enforces termination with
`;` only).

```
! Source -> Target :: Event;                  // any descendant of Source → Target on Event
! * -> ErrorHandler :: Error;                 // ANY descendant → ErrorHandler on Error
! * -> ErrorHandler : if [error_flag > 0];    // ANY descendant → ErrorHandler when guard true
```

Target names on forced transitions must be semantically resolvable from the
scope where the forced transition is written. If the intended target is a
nested leaf such as `Root.Mode.Manual`, either place the forced transition
inside the enclosing composite scope that can resolve `Manual`, or target a
state declared in the same scope as the forced transition. Do not write a
root-level `! * -> Manual ...` when `Manual` exists only as a nested child of
`Mode`; pyfcstm will reject it as an unknown target. In that situation, either
move the forced declaration into `Mode`, or introduce an NL-grounded root-level
fallback state and target that state from the root-level forced transition.

Forced transitions are auto-expanded by the pyfcstm model layer to every
applicable descendant — write it ONCE.

**If you need side-effects on a forced (global) escape**, put them in the
target state's `enter { ... }` lifecycle action:

```
// WRONG:  ! * -> Red :: Reset effect { timer = 0; };
// RIGHT:
state Red { enter { timer = 0; } }
! * -> Red :: Reset;
```

---

## 9. Expressions (inside guards `[...]` and effects `{ ... }`)

| Category | Operators / functions |
| --- | --- |
| Arithmetic | `+ - * / % **` |
| Bitwise | `<< >> & ^ \|` |
| Comparison | `< > <= >= == !=` |
| Logical | `&& \|\| !` (or keywords `and / or / not`) |
| Ternary | `(cond) ? a : b` |
| Math functions | `sin cos tan asin acos atan sinh cosh tanh sqrt cbrt exp log log10 log2 log1p abs ceil floor round trunc sign` |
| Constants | `PI_CONST E_CONST TAU_CONST` |

Inside `effect { ... }` you may also use nested conditionals. Action-block
conditionals use square-bracket guards: write `if [expr] { ... }` and
`else if [expr] { ... }`; never write C/JavaScript-style `if (expr)`.

```
effect {
    if [counter > 10] {
        counter = 0;
    } else if [counter > 5] {
        counter = counter + 1;
    } else {
        counter = counter * 2;
    }
}
```

---

## 10. Cycle execution semantics (the off-by-one source)

Each `cycle()` call executes the following in order:

1. **Evaluate outgoing transitions** of the current leaf state using:
   - **pre-during** variable values (i.e., values at the START of the cycle,
     BEFORE the active state's `during` block runs this cycle)
   - any events injected this cycle via `cycle(events=[...])`
2. If a transition matches (guard true / event present):
   - run its `effect { ... }` block
   - run `exit { ... }` of source state (and any ancestors being left)
   - run `enter { ... }` of target state (and any ancestors being entered)
   - run `during { ... }` of the new leaf
3. Otherwise: run `during { ... }` of the current state.

**Consequence**: NL phrasing "when timer reaches N, transition" usually
corresponds to firing on the cycle when `timer == N+1` from the
human-readable counting, because:

- previous cycle's during pushed timer to N
- next cycle's pre-during sees N, evaluates guard `>= N` → fires this
  cycle (so transition fires the cycle WHERE timer was already N at the
  start, BEFORE the during increment that would push to N+1)

**First cycle from default-init** (no `initial_state` passed to the
simulator): the runtime starts at the root state — first cycle dispatches
`[*] -> X`, then runs X's enter + first during. So `runtime.current_state`
is at the root BEFORE the first cycle and at the initial leaf AFTER it.

---

## 11. Worked examples

### Example A — Traffic light (guard-driven cyclic + global reset)

NL: Three states Red/Green/Yellow. Cycle through with timers
(Red→Green @ timer=30, Green→Yellow @ timer=25, Yellow→Red @ timer=5).
Global Reset signal forces Red.

```
def int timer = 0;

state TrafficLightController {
    ! * -> Red :: Reset;

    [*] -> Red;

    state Red {
        enter { timer = 0; }
        during { timer = timer + 1; }
    }

    state Green {
        during { timer = timer + 1; }
    }

    state Yellow {
        during { timer = timer + 1; }
    }

    Red -> Green : if [timer >= 30] effect { timer = 0; };
    Green -> Yellow : if [timer >= 25] effect { timer = 0; };
    Yellow -> Red : if [timer >= 5] effect { timer = 0; };
}
```

Notes:
- `! * -> Red :: Reset;` is forced and terminates with `;` (no effect block
  allowed). Side-effect of resetting `timer = 0` is put in `Red.enter`.
- Each guard transition uses `: if [...] effect { ... };` form.

### Example B — Synthetic actuator (event-driven)

This is a synthetic toy example for grammar illustration, not a benchmark case.

NL: A three-state actuator starts in `Waiting`; `BeginMove` moves it to
`Moving`; `ArriveDone` completes at `Done`. `ResetEvent` returns from `Done`
to `Waiting`.

```
state SyntheticActuator {
    ! Done -> Waiting :: ResetEvent;
    [*] -> Waiting;
    state Waiting;
    state Moving;
    state Done;
    Waiting -> Moving :: BeginMove;
    Moving -> Done :: ArriveDone;
}
```

Notes:
- Each event-triggered transition uses `:: <event>` (LOCAL scope) —
  `BeginMove`, `ArriveDone` and `ResetEvent` each live in their own source
  state's namespace.
- The forced `! Done -> Waiting :: ResetEvent;` means "from any descendant of
  Done, go to Waiting on ResetEvent" — in this flat model Done has no
  descendants so it is equivalent to `Done -> Waiting :: ResetEvent;`, but `!`
  is idiomatic for global-escape patterns.

### Example C — Microwave with hybrid event + guard

NL: Idle / Ready / Cooking / Paused. door_closed + start_pressed drive
forward; door_open pauses; cook_timer increments in Cooking and at 120
auto-returns to Idle. Reset forces Idle.

```
def int cook_timer = 0;

state MicrowaveController {
    ! * -> Idle :: reset;

    [*] -> Idle;

    state Idle {
        enter { cook_timer = 0; }
    }

    state Ready;

    state Cooking {
        during { cook_timer = cook_timer + 1; }
    }

    state Paused;

    Idle -> Ready :: door_closed effect { cook_timer = 0; };
    Ready -> Cooking :: start_pressed;
    Cooking -> Paused :: door_open;
    Paused -> Cooking :: door_closed;
    Cooking -> Idle : if [cook_timer >= 120];
}
```

Notes:
- Mix of event-triggered (`:: door_closed` etc.) and guard-triggered
  (`: if [cook_timer >= 120]`) — both forms coexist fine, but each
  individual transition uses only one.
- `cook_timer` reset is in `Idle.enter` (because Reset is forced and can't
  carry an effect) AND in the `Idle -> Ready` transition's effect (to
  ensure it's also reset entering Ready on door_closed).
- `Paused` has no during/effect — it just holds the state with cook_timer
  preserved.

---

## 12. Pre-output self-check

Before emitting your DSL, verify each of the following:

- [ ] All variables used in guards / effects / lifecycle blocks are
      declared at the top with `def int / def float` only; boolean-like
      flags are encoded as `int` 0/1, never `def bool`.
- [ ] There is exactly **one** top-level state.
- [ ] Every **composite** state has an `[*] -> <child>;` initial transition
      inside its body.
- [ ] No transition mixes event (`:: e` or `: e` or `: /path.e`) with
      guard (`: if [...]`).
- [ ] No transition uses `:: if [...]` (this is always a parse error;
      `if` is not an event name).
- [ ] No `if [...]` without a leading `:` operator.
- [ ] Every forced transition (`! ...`) terminates with `;` — no
      `effect { ... }` block on forced.
- [ ] Side-effects intended on a forced transition are in the target
      state's `enter { ... }` block instead.
- [ ] Absolute scope `/...` does NOT repeat the root state name after the
      slash.
- [ ] No comments are emitted in the DSL output: no `// ...`, no `/* ... */`,
      and no copied explanatory comments from this reference.
- [ ] No unknown helper function calls such as `ComputeRate(...)`, `max(...)`
      or `min(...)` are used in numeric assignments unless that function is
      explicitly supported by the expression function list above; otherwise use
      an abstract lifecycle action or a simple variable assignment grounded in
      NL.
- [ ] Action-block conditionals are written as `if [expr] { ... }`, never
      `if (expr) { ... }`; assignments do not use `+=`, `-=`, `*=`, `/=`.
- [ ] NL events are represented with `:: EventName` transitions rather than
      undeclared event-name guard variables; multiple alternative events use
      multiple transitions.
- [ ] Plain `during { ... }` is only used on leaf states. Composite states use
      `>> during before { ... }` / `>> during after { ... }` or move the action
      into descendant leaves.
