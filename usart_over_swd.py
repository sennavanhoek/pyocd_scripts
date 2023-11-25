#!/usr/bin/env python3
from pyocd.core.helpers import ConnectHelper
from pyocd.core.target import Target
from pyocd.debug.elf.symbols import ELFSymbolProvider
from pyocd.flash.file_programmer import FileProgrammer


def continue_until_halt(target):
    """
    Continue until halt.
    """ 
    target.resume()
    while target.get_state() != Target.State.HALTED:
        pass


def wait_at(target, symbol):
    """
    Break at the address of the symbol.
    """
    provider = ELFSymbolProvider(target.elf)
    addr = provider.get_symbol_value(symbol)
    target.set_breakpoint(addr, Target.BreakpointType.HW)
    continue_until_halt(target)
    target.remove_breakpoint(addr)


def print_str(target, char_pointer):
    """
    Prints string in device memory pointed to by char_pointer.
    """ 
    char = target.read8(char_pointer)
    string = ""
    while char != 0:
        string += chr(char)
        char_pointer += 1
        char = target.read8(char_pointer)
    print(string)
    

with ConnectHelper.session_with_chosen_probe() as session:
    elf = "example.elf"
    target = session.target
    target.elf = elf
    
    #Optionally flash board
    #FileProgrammer(session).program(elf)
    
    target.reset_and_halt()
    
    # Hook send_USART_str
    while True:
        wait_at(target, "send_USART_str")
        char_pointer = target.read_core_register('r0')
        print_str(target, char_pointer)
        target.step()
    
    
