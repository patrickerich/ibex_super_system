#!/usr/bin/env python
import datetime
import os
from pathlib import Path
import subprocess

PWD = Path(__file__).parent.resolve()
SIM = os.getenv('SIM', 'verilator')
timestamp = datetime.datetime.now().strftime("%y.%m.%d_%H.%M")
PWD.joinpath('sim_reports').mkdir(exist_ok=True)
report_file = str(PWD.joinpath('sim_reports', f'sim_report_{timestamp}.html'))
cache_dir = str(PWD.joinpath('.pytest_cache'))

sim = f'SIM={SIM}'
pytest = 'pytest'
parallel = '-n 1'
cache = f'-o cache_dir={cache_dir}'
tests = '-o python_files="pytest_*.py"'
report = f'--html={report_file}'

pytest_cmd = ' '.join([sim, pytest, parallel, cache, tests, report])

subprocess.call(pytest_cmd, shell=True, cwd=PWD)
