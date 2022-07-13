import os
import yaml
from pathlib import Path


class CocotbBridge:

    def __init__(self, build_dir):
        self.build_dir = Path(build_dir).resolve()
        self.sim = self.get_sim()
        self.edam = self.get_edam()
        self.eda_yaml = self.read_edam()
        self.toplevel = self.eda_yaml['toplevel']
        self.build_name = self.eda_yaml['name']
        self.verilog_includes = []
        self.verilog_sources = []
        self.waiver_files = []
        self.get_files()
        self.compile_args = []
        self.plus_args = []
        self.get_compile_args()
        self.cocotb_dir = self.build_dir.joinpath(
            self.build_name, 'sim-cocotb'
        ).resolve()

    def get_sim(self):
        sim = os.getenv('SIM', 'verilator')
        # Allow cocotb to default to verilator
        os.environ['SIM'] = sim
        # For now only verilator is supported
        if sim != 'verilator':
            raise Exception('Currently only verilator is supported!')
        return sim

    def get_edam(self):
        edam_list = list(self.build_dir.glob(f'**//sim-{self.sim}/*.eda.yml'))
        # For now simply return the first edam file found
        if len(edam_list) == 0:
            raise FileNotFoundError(
                f'An edam file could not be found (in {self.build_dir})!'
            )
        return edam_list[0]

    def read_edam(self):
        with open(self.edam) as eda_yaml_f:
            return yaml.safe_load(eda_yaml_f)

    def get_files(self):
        for f in self.eda_yaml['files']:
            if 'file_type' in f:
                if f['file_type'] in ['systemVerilogSource', 'verilogSource']:
                    if 'is_include_file' in f:
                        if f['is_include_file']:
                            verilog_include = self.edam.parent.joinpath(
                                f['name']).parent.resolve()
                            if verilog_include not in self.verilog_includes:
                                self.verilog_includes.append(verilog_include)
                        else:
                            verilog_source = self.edam.parent.joinpath(
                                f['name']).resolve()
                            if verilog_source not in self.verilog_sources:
                                self.verilog_sources.append(verilog_source)
                    else:
                        verilog_source = self.edam.parent.joinpath(
                            f['name']).resolve()
                        if verilog_source not in self.verilog_sources:
                            self.verilog_sources.append(verilog_source)
                elif f['file_type'] == 'vlt':
                    waiver_file = self.edam.parent.joinpath(
                        f['name']).resolve()
                    if waiver_file not in self.waiver_files:
                        self.waiver_files.append(waiver_file)

    def get_compile_args(self):
        if self.sim == 'verilator':
            params = self.eda_yaml['parameters']
            includes = self.verilog_includes
            options = self.eda_yaml['tool_options'][self.sim][f'{self.sim}_options']
            for param in params:
                datatype = self.eda_yaml['parameters'][param]['datatype']
                paramtype = self.eda_yaml['parameters'][param]['paramtype']
                default = self.eda_yaml['parameters'][param]['default']
                if datatype == 'bool':
                    default = int(default)
                if paramtype == 'vlogparam':
                    self.compile_args.append(f'-G{param}="{default}"')
                elif paramtype == 'vlogdefine':
                    self.compile_args.append(f'-D{param}={default}')
            for include in includes:
                self.compile_args.append(f'+incdir+{include}')
                self.compile_args.extend(['-CFLAGS', f'-I{include}'])
            for option in options:
                if '"' in option:
                    main_option = option.split('"')[0]
                    sub_options = option.split('"')[1].split()
                    for sub_option in sub_options:
                        self.compile_args.extend(
                            [main_option.strip(), sub_option.strip()]
                        )
                else:
                    self.compile_args.extend(option.split())
