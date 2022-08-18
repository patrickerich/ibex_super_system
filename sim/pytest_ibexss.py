from pathlib import Path
from cocotb_bridge.cocotb_bridge import CocotbBridge
from cocotb_test.simulator import run


hw_build_dir = Path(__file__).parent.joinpath('..', 'build').resolve()
sw_build_dir = Path(__file__).parent.joinpath('..', 'sw', 'build').resolve()


def get_sram_file(prog):
    return sw_build_dir.joinpath(prog, f'{prog}.vmem')


def tests_ibexss_demo():
    prog = 'demo'
    sim_helper = CocotbBridge(hw_build_dir)
    sim_helper.set_vlogparam('SRAMInitFile', get_sram_file(prog))
    run(
        toplevel=sim_helper.toplevel,
        module=f'tb_ibexss_{prog}',
        verilog_sources=sim_helper.verilog_sources,
        toplevel_lang='verilog',
        compile_args=sim_helper.compile_args,
        plus_args=sim_helper.plus_args,
        force_compile=True,
        sim_build=sim_helper.cocotb_dir,
        waves=False,
       )


def tests_ibexss_cmdint():
    prog = 'cmdint'
    sim_helper = CocotbBridge(hw_build_dir)
    sim_helper.set_vlogparam('SRAMInitFile', get_sram_file(prog))
    run(
        toplevel=sim_helper.toplevel,
        module=f'tb_ibexss_{prog}',
        verilog_sources=sim_helper.verilog_sources,
        toplevel_lang='verilog',
        compile_args=sim_helper.compile_args,
        plus_args=sim_helper.plus_args,
        force_compile=True,
        sim_build=sim_helper.cocotb_dir,
        waves=False,
       )
