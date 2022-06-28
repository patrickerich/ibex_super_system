import os
import cocotb
from cocotb.clock import Clock
# from cocotb.triggers import Timer, ReadOnly, RisingEdge, FallingEdge, NextTimeStep
from cocotb.triggers import Timer
# from cocotbext.uart import UartSource, UartSink


class TestBench():

    def __init__(self, dut, period_ns):
        '''
            Initialize the testbench
        '''
        self.dut = dut
        self.period_ns = period_ns
        self.clk_gen = None

    async def start_clock(self):
        '''
            Create and start the clock signal
        '''
        self.clk_gen = cocotb.start_soon(Clock(
            self.dut.clk_sys_i,
            self.period_ns,
            units='ns').start())

    async def reset_dut(self):
        '''
            Reset the DUT (asynchronously)
        '''
        self.dut.rst_sys_ni <= 0
        await Timer(3*self.period_ns, units='ns')
        self.dut.rst_sys_ni <= 1
