# tb_ibex_super_system.py
import cocotb
from testbench import TestBench


@cocotb.test()
async def ibex_super_system_simple_test(dut):
    '''
        check the default test case
    '''
    dut._log.info("Running default test case.....")

    tb = TestBench(dut, period=20, period_unit='ns')
    tb.log_verbose = True
    await tb.start_clock()
    await tb.reset(delay_periods=3, reset_periods=2)
    await tb.run_for(run_periods=100000)
    # tb.stop_clock()
    # await tb.run_for(run_periods=10)

    dut._log.info("Running default test case.....done")
