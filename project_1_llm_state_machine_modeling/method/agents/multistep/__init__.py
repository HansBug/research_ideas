"""Multi-step modeling pipeline (MTI methodology applied to pyfcstm).

The 6-step pipeline:
    1. identify_state    - NL -> state list (nested + parallel hierarchy)
    2. identify_event    - NL -> event list (Internal/External)
    3. identify_variable - NL + state_list -> variable list
    4. identify_transition - NL + state + event + variable -> transitions
    5. identify_action   - NL + all upstream lists -> actions
    6. build_pyfcstm     - all elements -> complete pyfcstm DSL

Each step uses the same 7-section prompt skeleton:
    [task] + [requirements] + [upstream lists] + [step task]
    + [domain knowledge] + [format description (JSON)] + [constraint] + [opening cue]

Outputs are structured JSON (steps 1-5) and a final pyfcstm DSL (step 6),
which is the same artifact a single-prompt Modeler would produce. The agent
loop's feedback/repair machinery (Phase D-H) consumes the step-6 output
identically.
"""

from method.agents.multistep.identify_state import identify_state
from method.agents.multistep.identify_event import identify_event
from method.agents.multistep.identify_variable import identify_variable
from method.agents.multistep.identify_transition import identify_transition
from method.agents.multistep.identify_action import identify_action
from method.agents.multistep.build_pyfcstm import build_pyfcstm
from method.agents.multistep.pipeline import MultistepResult, run_multistep_modeling

__all__ = [
    "identify_state",
    "identify_event",
    "identify_variable",
    "identify_transition",
    "identify_action",
    "build_pyfcstm",
    "MultistepResult",
    "run_multistep_modeling",
]
