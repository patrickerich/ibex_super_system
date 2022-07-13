from pathlib import Path
from cocotb_bridge import CocotbBridge
from cocotb_test.simulator import run


build_dir =  Path(__file__).parent.joinpath('..', 'build').resolve()
sim_helper = CocotbBridge(build_dir)


def test_ibex_super_system():
    run(
         toplevel=sim_helper.toplevel,
         module=f'tb_{sim_helper.toplevel}',
         verilog_sources=sim_helper.verilog_sources,
         toplevel_lang='verilog',
         compile_args=sim_helper.compile_args,
         plus_args=sim_helper.plus_args,
         force_compile=True,
         sim_build=sim_helper.cocotb_dir,
         # Wave tracing is handled through the compile_args
         waves=False,
       )
