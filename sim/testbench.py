import cocotb
from cocotb.clock import Clock
from cocotb.triggers import Timer
from cocotbext.uart import UartSource, UartSink


class TestBench():

    def __init__(
        self, dut, clk_period, clk_period_unit,
        uart_baudrate=115200, uart_bits=8
    ):
        '''
            Initialize the testbench object
        '''
        self.dut = dut
        self.clk_period = clk_period
        self.clk_period_unit = clk_period_unit
        self.uart_baudrate = uart_baudrate
        self.uart_bits = uart_bits
        self.init_inputs()

    def init_inputs(self):
        '''
            Initialize the inputs
        '''
        self.dut.rst_sys_ni.value = 1
        self.dut.clk_sys_i.value = 0
        self.dut.uart_rx_i.value = 1

    def connect_uart(self):
        '''
            Connect the UART signals
        '''
        self.uart_source = UartSource(
            self.dut.uart_rx_i,
            baud=self.uart_baudrate,
            bits=self.uart_bits
        )
        self.uart_sink = UartSink(
            self.dut.uart_tx_o,
            baud=self.uart_baudrate,
            bits=self.uart_bits
        )

    async def start_clock(self):
        '''
            Create and start the clock signal (keep a handle just in case)
        '''
        self.clk = cocotb.start_soon(Clock(
            signal=self.dut.clk_sys_i,
            period=self.clk_period,
            units=self.clk_period_unit).start()
        )

    async def reset(self, delay_clk_periods, reset_clk_periods):
        '''
            Reset the DUT
        '''
        await self.run_for(delay_clk_periods)
        self.dut.rst_sys_ni.value = 0
        await self.run_for(reset_clk_periods)
        self.dut.rst_sys_ni.value = 1

    def stop_clock(self):
        '''
            kill the clock signal
        '''
        if self.clk:
            self.clk.kill()

    async def run_for(self, clk_periods):
        '''
            Run the DUT for a specific number of clk_periods
        '''
        await Timer(
            clk_periods*self.clk_period,
            units=self.clk_period_unit
        )
