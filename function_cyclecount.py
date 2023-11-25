#!/usr/bin/python3
from pyocd.core.helpers import ConnectHelper
from pyocd.core.target import Target
from pyocd.flash.file_programmer import FileProgrammer
from pyocd.debug.elf.symbols import ELFSymbolProvider
from tabulate import tabulate


# DWT Constants
DWT_CTRL = 0xE0001000
DWT_CYCCNT = DWT_CTRL + 0x04
DWT_CPICNT = DWT_CTRL + 0x08
DWT_LSUCNT = DWT_CTRL + 0x14
DWT_CTRL_CYCEVTENA = (1)
DWT_CTRL_LSUEVTENA = (1 << 20)
DWT_CTRL_CPIEVTENA = (1 << 17)


def enable_debug_regs(target):
    DWT_CONTROL_val = target.read32(DWT_CTRL)
    target.write32(DWT_CTRL, DWT_CONTROL_val | DWT_CTRL_CYCEVTENA | DWT_CTRL_LSUEVTENA | DWT_CTRL_CPIEVTENA)


def continue_until_halt(target):
    target.resume()
    while target.get_state() != Target.State.HALTED:
        pass


def wait_at(target, symbol):
    provider = ELFSymbolProvider(target.elf)
    addr = provider.get_symbol_value(symbol)
    if addr == None:
        print(F'Symbol "{symbol}" not found, exiting...')
        exit()
    
    target.set_breakpoint(addr, Target.BreakpointType.HW)
    continue_until_halt(target)
    target.remove_breakpoint(addr)


def hook(target, target_function):
    # Break at function
    wait_at(target, target_function)

    # clear debug regs
    target.write32(DWT_CYCCNT, 0)
    target.write32(DWT_LSUCNT, 0)
    target.write32(DWT_CPICNT, 0)
    
    
    # Break on return
    lr = target.read_core_register("lr")
    target.set_breakpoint(lr, Target.BreakpointType.HW)
    target.resume()
    while target.get_state() != Target.State.HALTED:
        pass
    
    # get value of debug regs
    cyccnt = target.read32(DWT_CYCCNT)
    lsucnt = target.read32(DWT_LSUCNT)
    cpicnt = target.read32(DWT_CPICNT)

    
    target.remove_breakpoint(lr)
    
    return cyccnt, lsucnt, cpicnt
    


def step_trough(target, target_function):
    trace = []

    wait_at(target, target_function)
    
    return_adr = target.read_core_register("lr")-1
    pc = target.read_core_register("pc")
    while pc != return_adr:
        trace.append(pc)
        target.step()
        pc = target.read_core_register("pc")
    
    return trace


with ConnectHelper.session_with_chosen_probe() as session:
    # Settings
    elf = "example.elf"
    target_function = "foo"
    style = "fancy_grid"
    
    #Setup
    target = session.target
    target.elf = elf
    print("Flashing board:")
    FileProgrammer(session).program(elf)
    target.reset_and_halt()
    
    # Get DWT register values
    enable_debug_regs(target)
    cyccnt, lsucnt, cpicnt = hook(target, target_function)
    
    # Do a single step trace to get the instruction count
    target.reset_and_halt()
    trace = step_trough(target, target_function)

    print("Report:")
    print(tabulate([["target_function:",       target_function],
                    ["Cycle count:",           cyccnt],
                    ["LSU count:",             lsucnt],
                    ["CPI count:",             cpicnt],
                    ["Instructions executed:", len(trace)],
                    ["Inst+LSU+CPI == CYC",    len(trace)+lsucnt+cpicnt==cyccnt]],
         tablefmt=style))

