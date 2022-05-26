GDB := riscv32-unknown-elf-gdb
ARTY35 := xc7a35ticsg324-1L
ARTY100 := xc7a100tcsg324-1
FPGA ?= $(ARTY100)
DEVICE ?= /dev/ttyUSB1
BAUDRATE ?= 115200

HWPROG = $(PWD)/sw/build/demo/demo
# SIMPROG = $(PWD)/sw/build/blank/blank.vmem
SIMPROG = $(HWPROG).vmem

all: build-sw build-hw program-hw load-demo-run

.PHONY: lint
lint:
	fusesoc --cores-root=. run --target=lint \
		lowrisc:ibex:super_system

.PHONY: build-hw
build-hw:
	fusesoc --cores-root=. run --target=synth --setup --build \
		lowrisc:ibex:super_system --part $(FPGA)

.PHONY: build-sw
build-sw:
	cd sw && mkdir -p build && cd build && cmake ../ && $(MAKE)

.PHONY: program-hw
program-hw:
	fusesoc --cores-root=. run --target=synth --run \
		lowrisc:ibex:super_system
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

.PHONY: build-sim
build-sim:
	fusesoc --cores-root=. run --target=sim --setup --build \
		lowrisc:ibex:super_system \
		--SRAMInitFile=$(SIMPROG)

.PHONY: run-sim
run-sim: build-sw build-sim
	./build/lowrisc_ibex_super_system_0/sim-verilator/Vibex_super_system +trace > build/verilator.log 2>&1

.PHONY: clean
clean:
	@rm -rf build sw/build
