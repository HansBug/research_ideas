# ABS Brake Control FSM — NL Requirement

来源：`sources/abs-fsm-brake-control/STM.md` §2

The paper implements the single-wheel ABS hydraulic regulator as a
three-state FSM coupled with a PID-based slip controller. Wheel speed and
vehicle speed are used to compute the slip ratio, and the PID output drives
the Stateflow supervisor instead of sending commands directly to the
hydraulic valves.

The FSM contains the states `increase`, `hold`, and `decrease`, where

- `increase` sets `k1=1, k2=0, n=0`,
- `hold` neutralizes both valves with `k1=0, k2=0, n=0`,
- `decrease` sets `k1=0, k2=1, n=500` to release pressure.

The transition guards split the slip-error space into four bands:

- `increase -> hold` when `slp <= 0.01`
- `hold -> increase` when `slp > 0.01`
- `hold -> decrease` when `slp < -0.01`
- `decrease -> hold` when `slp >= -0.01`

This gives a concrete discrete supervisor that maps slip-error thresholds
to inlet-valve, return-valve, and pump actions while the continuous
wheel-slip dynamics remain in the plant model.
