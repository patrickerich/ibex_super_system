GDB := riscv32-unknown-elf-gdb
ARTY35 := xc7a35ticsg324-1L
ARTY100 := xc7a100tcsg324-1
FPGA ?= $(ARTY100)
DEVICE ?= /dev/ttyUSB1
BAUDRATE ?= 115200

HWPROG = $(PWD)/sw/build/demo/demo
# SIMPROG = $(PWD)/sw/build/blank/blank.vmem
SIMPROG = $(HWPROG).vmem

all: clean build-sw build-hw program-hw load-demo-run

.PHONY: lint
lint:
	fusesoc --cores-root=. run --target=lint \
		lowrisc:ibex:ibex_super_system

.PHONY: build-hw
build-hw:
	fusesoc --cores-root=. run --target=synth --setup --build \
		lowrisc:ibex:ibex_super_system --part $(FPGA)

.PHONY: build-sw
build-sw:
	cd sw && mkdir -p build && cd build && cmake ../ && $(MAKE)

.PHONY: program-hw
program-hw:
	fusesoc --cores-root=. run --target=synth --run \
		lowrisc:ibex:ibex_super_system
	# make -C ./build/lowrisc_ibex_super_system_0/synth-vivado/ pgm

.PHONY: start-vivado
start-vivado:
	make -C ./build/lowrisc_ibex_super_system_0/synth-vivado/ build-gui &

.PHONY: load-demo-run
load-demo-run:
	./util/load_super_system.sh run $(HWPROG)

.PHONY: load-demo-halt
load-demo-halt:
	./util/load_super_system.sh halt $(HWPROG) &

.PHONY: screen-demo
screen-demo:
	@echo "Use 'ctrl-a k' to exit the screen command"
	@sleep 3
	@screen ${DEVICE} ${BAUDRATE}

.PHONY: debug-demo
debug-demo: load-demo-halt
	$(GDB) -ex "target extended-remote localhost:3333" \
		$(HWPROG)

.PHONY: py-hello
py-hello:
	python sw/demo/uart_hello.py

.PHONY: run-sim
run-sim:
	(cd sim && python run_tests.py)

.PHONY: view-wave
view-wave:
	gtkwave -f build/lowrisc_ibex_ibex_super_system_0/sim-cocotb/dump.fst \
	        -a ./sim.wav &

.PHONY: clean-sw
clean-sw:
	-rm -rf sw/build

.PHONY: clean-hw
clean-hw:
	-rm -rf build/lowrisc_ibex_ibex_super_system_0/synth-vivado

.PHONY: clean-sim
clean-sim:
	-rm -rf build/lowrisc_ibex_ibex_super_system_0/sim-*
	-rm -rf sim/__pycache__ sim/.pytest_cache sim_build
	-rm -rf sim/sim_reports

.PHONY: clean-all
clean-all: clean-sw clean-hw clean-sim
	-rm -rf build sw/build
