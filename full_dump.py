#!/usr/bin/env python3
from pyocd.core.helpers import ConnectHelper
from pyocd.flash.file_programmer import FileProgrammer

with ConnectHelper.session_with_chosen_probe() as session:
    programmer = FileProgrammer(session)
    target = session.target
    target.reset_and_halt()
    
    # Print and dump all all memory regions (including flash)
    for r in target.memory_map.regions:
        print(f"{r.name}: {r.access:<3} 0x{r.start:08X} - 0x{r.end:08X}, Size: 0x{r.length:X}")
        mem = target.read_memory_block8(r.start, r.length)
        with open(f"{r.name}_dump.bin", "wb") as f:
            f.write(bytearray(mem))