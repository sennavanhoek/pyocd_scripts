#!/usr/bin/env python3
from pyocd.core.helpers import ConnectHelper


with ConnectHelper.session_with_chosen_probe() as session:
    target = session.target
    for c in session.target.cores:
        core = session.target.cores[c]
        core_fam = core.name
        core_rev = F"r{core.cpu_revision}p{core.cpu_patch}"
        fpu = "with FPU" if core.has_fpu else "without FPU"
        print(core_fam, core_rev, fpu)
