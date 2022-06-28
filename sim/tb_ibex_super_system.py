# tb_ibex_super_system.py
import cocotb
from testbench import TestBench


@cocotb.test()
async def ibex_super_system_simple_test(dut):
    '''
        check the default test case
    '''
    dut._log.info("Running default test case.....")

    tb_obj = TestBench(dut, period_ns=20)
    tb_obj.log_verbose = True
    await tb_obj.start_clock()
    await tb_obj.reset_dut()

    dut._log.info("Running default test case.....done")
