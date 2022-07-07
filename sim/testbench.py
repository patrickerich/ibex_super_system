# import os
import cocotb
from cocotb.clock import Clock
from cocotb.triggers import (
    Timer,
    # ReadOnly,
    # RisingEdge,
    # FallingEdge,
    # NextTimeStep,
)
# from cocotbext.uart import UartSource, UartSink


class TestBench():

    def __init__(self, dut, period, period_unit):
        '''
            Initialize the testbench
        '''
        self.dut = dut
        self.period = period
        self.period_unit = period_unit
        self.init_inputs()

    def init_inputs(self):
        self.dut.rst_sys_ni.value = 1
        self.dut.clk_sys_i.value = 0
        self.dut.uart_rx_i.value = 1

    async def reset(self, delay_periods, reset_periods):
        '''
            Reset the DUT
        '''
        await self.run_for(delay_periods)
        self.dut.rst_sys_ni.value = 0
        await self.run_for(reset_periods)
        self.dut.rst_sys_ni.value = 1

    async def start_clock(self):
        '''
            Create and start the clock signal (keep a handle just in case)
        '''
        self.clk = cocotb.start_soon(Clock(
            signal=self.dut.clk_sys_i,
            period=self.period,
            units=self.period_unit).start()
        )

    def stop_clock(self):
        '''
            kill the clock signal
        '''
        if self.clk:
            self.clk.kill()

    async def run_for(self, run_periods):
        '''
            Run the DUT for a specific number of clock periods
        '''
        await Timer(run_periods*self.period, units=self.period_unit)
