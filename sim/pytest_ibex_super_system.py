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
fusesoc_build = PROJ_ROOT.joinpath(
    'build',
    fusesoc_elab,
    'sim-verilator').resolve()
cocotb_build = PROJ_ROOT.joinpath(
    'build', fusesoc_elab,
    'sim-cocotb'
).resolve()
fusesoc_edam = fusesoc_build.joinpath(fusesoc_elab + '.eda.yml')
sram_file = PROJ_ROOT.joinpath(
    'sw',
    'build',
    'demo',
    'demo.vmem'
).resolve()


compile_args = []
plus_args = []

vlt_files = []

verilog_includes = []
verilog_sources = []
c_includes = []
c_sources = []
cpp_includes = []
cpp_sources = []

# Make sure the Fusesoc EDAM file exists and is up to date
with subprocess.Popen(
  args=['make', 'init-sim'],
  stdout=subprocess.PIPE,
  cwd=PROJ_ROOT) as proc:
    print(proc.stdout.read().decode())

# Make sure the software has been built and is up to date
with subprocess.Popen(
  args=['make', 'build-sw'],
  stdout=subprocess.PIPE,
  cwd=PROJ_ROOT) as proc:
    print(proc.stdout.read().decode())

# Extract sources/includes from EDAM file
with open(fusesoc_edam) as eda_yaml_f:
    eda_yaml = yaml.safe_load(eda_yaml_f)
for f in eda_yaml['files']:
    if 'file_type' in f:
        # # Waiver files
        # if f['file_type'] == 'vlt':
        #     vlt_file = fusesoc_build.joinpath(f['name']).resolve()
        #     if vlt_file not in vlt_files:
        #         vlt_files.append(vlt_file)
        # Verilog sources/includes
        if f['file_type'] in ['systemVerilogSource', 'verilogSource']:
            if 'is_include_file' in f:
                if f['is_include_file']:
                    verilog_include = fusesoc_build.joinpath(
                        f['name']
                    ).parent.resolve()
                    if verilog_include not in verilog_includes:
                        verilog_includes.append(verilog_include)
                else:
                    verilog_source = fusesoc_build.joinpath(
                        f['name']
                    ).resolve()
                    if verilog_source not in verilog_sources:
                        verilog_sources.append(verilog_source)
            else:
                verilog_source = fusesoc_build.joinpath(f['name']).resolve()
                if verilog_source not in verilog_sources:
                    verilog_sources.append(verilog_source)
        # # C sources/includes
        # if f['file_type'] == 'cSource':
        #     if 'is_include_file' in f:
        #         if f['is_include_file']:
        #             c_include = fusesoc_build.joinpath(f['name']).parent.resolve()
        #             if c_include not in c_includes:
        #                 c_includes.append(c_include)
        #         else:
        #             c_source = fusesoc_build.joinpath(f['name']).resolve()
        #             if c_source not in c_sources:
        #                 c_sources.append(verilog_source)
        #     else:
        #         c_source = fusesoc_build.joinpath(f['name']).resolve()
        #         if c_source not in c_sources:
        #             c_sources.append(c_source)
        # # Cpp sources/includes
        # if f['file_type'] == 'cppSource':
        #     if 'is_include_file' in f:
        #         if f['is_include_file']:
        #             cpp_include = fusesoc_build.joinpath(f['name']).parent.resolve()
        #             if cpp_include not in cpp_includes:
        #                 cpp_includes.append(cpp_include)
        #         else:
        #             cpp_source = fusesoc_build.joinpath(f['name']).resolve()
        #             if cpp_source not in cpp_sources:
        #                 cpp_sources.append(cpp_source)
        #     else:
        #         cpp_source = fusesoc_build.joinpath(f['name']).resolve()
        #         if cpp_source not in cpp_sources:
        #             cpp_sources.append(cpp_source)


# For now merge the sources and includes (without duplicates)
includes = list(set(verilog_includes + c_includes + cpp_includes))
sources = list(set(vlt_files + verilog_sources + c_sources + cpp_sources))


# Define the timescale (comment out if not needed/used!)
timescale = '1ns/1ps'

if sim == 'verilator':
    for include in includes:
        compile_args.append(f'+incdir+{include}')
        compile_args.extend(['-CFLAGS', f'-I{include}'])
    compile_args.append(f'-GSRAMInitFile="{sram_file}"')
    compile_args.append('-DRVFI=1')
    if 'timescale' in globals():
        compile_args.extend(['--timescale-override', timescale])
    if waves:
        compile_args.append('--trace')
        compile_args.append('--trace-fst')
        compile_args.append('--trace-structs')
        compile_args.append('--trace-params')
        compile_args.extend(['--trace-max-array', '1024'])
        compile_args.extend(['--trace-threads', '2'])
    compile_args.extend(['-CFLAGS', '-std=c++11'])
    compile_args.extend(['-CFLAGS', '-Wall'])
    compile_args.extend(['-CFLAGS', '-DVM_TRACE_FMT_FST'])
    compile_args.extend(['-CFLAGS', f'-DTOPLEVEL_NAME={toplevel}'])
    compile_args.extend(['-CFLAGS', '-g'])
    compile_args.extend(['-LDFLAGS', '-pthread'])
    compile_args.extend(['-LDFLAGS', '-lutil'])
    compile_args.extend(['-LDFLAGS', '-lelf'])
    compile_args.append('-Wall')
    compile_args.append('-Wno-SELRANGE')
    compile_args.append('-Wno-WIDTH')
    compile_args.append('-Wno-DECLFILENAME')
    compile_args.append('-Wno-PINMISSING')
    compile_args.append('-Wno-PINCONNECTEMPTY')
    compile_args.append('-Wno-PINNOCONNECT')
    compile_args.extend(['--unroll-count', '72'])


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
