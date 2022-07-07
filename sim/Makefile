# Very simple Makefile for helping running/cleaning the simulations

all: clean 

.PHONY: clean
clean:
	-rm -rf __pycache__ .pytest_cache sim_build ../build/lowrisc_ibex_ibex_super_system_0/sim-cocotb/

.PHONY: purge
purge: clean
	-rm -rf sim_reports
	(cd .. && make clean-all)

.PHONY: run
run:
	python run_tests.py

.PHONY: wave
wave:
	gtkwave -f ../build/lowrisc_ibex_ibex_super_system_0/sim-cocotb/dump.fst \
	        -a ./sim.wav &
