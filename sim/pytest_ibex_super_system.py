import os
import subprocess
import yaml
from cocotb_test.simulator import run
from pathlib import Path

pwd = Path(__file__).parent.resolve()
root = pwd.joinpath('..').resolve()
sim = os.getenv('SIM', 'verilator')
waves = True

fusesoc_core = 'lowrisc:ibex:ibex_super_system'
fusesoc_elab = fusesoc_core.replace(':', '_') + '_0'
fusesoc_build = root.joinpath('build', fusesoc_elab, 'sim-verilator').resolve()
cocotb_build = root.joinpath('build', fusesoc_elab, 'sim-cocotb').resolve()
fusesoc_edam = fusesoc_build.joinpath(fusesoc_elab + '.eda.yml')

compile_args = []
plus_args = []
verilog_sources = []

# Run fusesoc setup (if not run already)
if not fusesoc_build.is_dir():
    with subprocess.Popen(
      ['fusesoc', '--cores-root=.', 'run', '--target=sim',
       '--setup', fusesoc_core],
      stdout=subprocess.PIPE,
      cwd=root) as proc:
        print(proc.stdout.read().decode())

# Extract verilog sources from EDAM file
with open(fusesoc_edam) as eda_yaml_f:
    eda_yaml = yaml.safe_load(eda_yaml_f)
for f in eda_yaml['files']:
    if 'file_type' in f:
        if f['file_type'] in ['systemVerilogSource', 'verilogSource']:
            # if f['name'].endswith('.sv'):
            verilog_sources.append(fusesoc_build.joinpath(f['name']).resolve())

# Define the timescale (comment out if not needed/used!)
timescale = '1ns/1ps'

if sim == 'verilator':
    compile_args.extend(['-Wno-SELRANGE', '-Wno-WIDTH'])
    compile_args.extend(['-CFLAGS', '"-std=c++11 -Wall -DVM_TRACE_FMT_FST -DTOPLEVEL_NAME=ibex_super_system -g"'])
    compile_args.extend(['-LDFLAGS', '"-pthread -lutil -lelf"'])
    compile_args.append('-Wall')
    compile_args.append('-Wwarn-IMPERFECTSCH')
    compile_args.extend(['--unroll-count',  '72'])
    if 'timescale' in globals():
        compile_args.extend(['--timescale-override', timescale])
    if waves:
        compile_args.append('--trace')
        compile_args.append('--trace-fst')
        compile_args.append('--trace-structs')
        compile_args.append('--trace-params')
        compile_args.extend(['--trace-max-array', '1024'])
        compile_args.extend(['--trace-threads', '2'])


# print(verilog_sources)

def test_ibex_super_system():
    run(
         toplevel='ibex_super_system',
         module='tb_ibex_super_system',
         verilog_sources=verilog_sources,
         toplevel_lang='verilog',
         compile_args=compile_args,
         plus_args=plus_args,
         force_compile=True,
         sim_build=str(pwd.joinpath('..', 'build', 'sim_cocotb')),
         # Wave tracing is regulated through the compile_args
         waves=False,
       )
