import os
import cocotb
from cocotb.clock import Clock
# from cocotb.triggers import Timer, ReadOnly, RisingEdge, FallingEdge, NextTimeStep
from cocotb.triggers import Timer
# from cocotbext.uart import UartSource, UartSink


class TestBench():

    def __init__(self, dut, period, period_unit):
        '''
            Initialize the testbench
        '''
        self.dut = dut
        self.period = period
        self.period_unit = period_unit

    async def start_clock(self):
        '''
            Create and start the clock signal (keep a handle just in case)
        '''
        self.clk = cocotb.start_soon(Clock(
            signal=self.dut.clk_sys_i,
            period=self.period,
            units=self.period_unit).start()
        )

    async def run_for(self, periods):
        '''
            Run the DUT for a specific number of clock periods
        '''
        await Timer(periods*self.period, units=self.period_unit)

    async def reset(self, periods):
        '''
            Reset the DUT
        '''
        self.dut.rst_sys_ni.value = 0
        await self.run_for(periods)
        self.dut.rst_sys_ni.value = 1

    
        