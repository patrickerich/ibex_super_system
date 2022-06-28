import os
import subprocess
import yaml
from cocotb_test.simulator import run
from pathlib import Path

PWD = Path(__file__).parent.resolve()
PROJ_ROOT = PWD.joinpath('..').resolve()
sim = os.getenv('SIM', 'verilator')
# Allow pytest to default to verilator
os.environ['SIM'] = sim
waves = True
toplevel = 'ibex_super_system'
module = 'tb_' + toplevel

fusesoc_core = f'lowrisc:ibex:{toplevel}'
fusesoc_elab = fusesoc_core.replace(':', '_') + '_0'
fusesoc_build = PROJ_ROOT.joinpath('build', fusesoc_elab, 'sim-verilator').resolve()
cocotb_build = PROJ_ROOT.joinpath('build', fusesoc_elab, 'sim-cocotb').resolve()
fusesoc_edam = fusesoc_build.joinpath(fusesoc_elab + '.eda.yml')

compile_args = []
plus_args = []
verilog_sources = []
verilog_includes = []

# Remove old results (forcibly for now)
with subprocess.Popen(
  ['rm', '-rf', str(fusesoc_build), str(cocotb_build)],
  stdout=subprocess.PIPE,
  cwd=PROJ_ROOT) as proc: 
    print(proc.stdout.read().decode())

# Generate Fusesoc EDAM file (if not existing)
with subprocess.Popen(
  ['fusesoc', '--cores-root=.', 'run', '--target=sim',
   '--setup', fusesoc_core],
  stdout=subprocess.PIPE,
  cwd=PROJ_ROOT) as proc:
    print(proc.stdout.read().decode())

# Extract verilog sources from EDAM file
with open(fusesoc_edam) as eda_yaml_f:
    eda_yaml = yaml.safe_load(eda_yaml_f)
for f in eda_yaml['files']:
    if 'file_type' in f:
        if f['file_type'] in ['systemVerilogSource', 'verilogSource']:
            if f['name'].endswith('.svh'):
                verilog_includes.append(fusesoc_build.joinpath(f['name']).parent.resolve())
            else:
                verilog_sources.append(fusesoc_build.joinpath(f['name']).resolve())

# Define the timescale (comment out if not needed/used!)
timescale = '1ns/1ps'

if sim == 'verilator':
    compile_args.append('-Wall')
    compile_args.append('-Wno-SELRANGE')
    compile_args.append('-Wno-WIDTH')
    compile_args.append('-Wno-DECLFILENAME')
    compile_args.append('-Wno-PINMISSING')
    compile_args.append('-Wno-PINCONNECTEMPTY')
    compile_args.append('-Wno-PINNOCONNECT')
    compile_args.extend(['-CFLAGS', '-std=c++11'])
    compile_args.extend(['-CFLAGS', '-Wall'])
    compile_args.extend(['-CFLAGS', '-DVM_TRACE_FMT_FST'])
    compile_args.extend(['-CFLAGS', f'-DTOPLEVEL_NAME={toplevel}'])
    compile_args.extend(['-CFLAGS', '-g'])
    compile_args.extend(['-LDFLAGS', '-pthread'])
    compile_args.extend(['-LDFLAGS', '-lutil'])
    compile_args.extend(['-LDFLAGS', '-lelf'])
    compile_args.extend(['--unroll-count', '72'])
    if 'timescale' in globals():
        compile_args.extend(['--timescale-override', timescale])
    if waves:
        compile_args.append('--trace')
        compile_args.append('--trace-fst')
        compile_args.append('--trace-structs')
        compile_args.append('--trace-params')
        compile_args.extend(['--trace-max-array', '1024'])
        compile_args.extend(['--trace-threads', '2'])
    for include in verilog_includes:
        compile_args.append(f'-I{include}')

def test_ibex_super_system():
    run(
         toplevel=toplevel,
         module=module,
         verilog_sources=verilog_sources,
         toplevel_lang='verilog',
         compile_args=compile_args,
         plus_args=plus_args,
         force_compile=True,
         sim_build=str(cocotb_build),
         # Wave tracing is handled through the compile_args
         waves=False,
       )
