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
    await tb.reset(periods=3)
    await tb.run_for(periods=100)

    dut._log.info("Running default test case.....done")
