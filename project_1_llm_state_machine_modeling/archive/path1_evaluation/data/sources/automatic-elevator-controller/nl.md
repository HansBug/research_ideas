# Automatic Elevator Controller — NL Requirement

来源：`sources/automatic-elevator-controller/STM.md` §2

The automatic elevator controller is built as a finite-state machine whose
state space combines floor states `F1`, `F2`, and `F3` with motion states
`MU2`, `MU3`, `MD1`, and `MD2` for upward and downward travel.

In the normal workflow, the system starts from an ideal state (on floor 1),
chooses either the up or down branch according to floor requests, stops at
the requested floor, and then immediately checks the next destination
before deciding whether to continue moving.

The controller uses `PS1/PS2/PS3` as floor-request inputs and `S1/S2/S3` as
sensing inputs for arrival. Transitions:

- From `F1`: `PS2` triggers `MU2`; `PS3` triggers `MU3`.
- From `F2`: `PS3` triggers `MU3`; `PS1` triggers `MD1`.
- From `F3`: `PS1` triggers `MD1`; `PS2` triggers `MD2`.
- Arrival sensors: `MU2 + S2 -> F2`; `MU3 + S3 -> F3`; `MD1 + S1 -> F1`;
  `MD2 + S2 -> F2`.

The `hbrg` output distinguishes upward drive, downward drive, and stop
conditions. A reset signal forces the controller back to floor 1 regardless
of the outstanding request context.
