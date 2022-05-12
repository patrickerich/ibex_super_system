GDB := riscv32-unknown-elf-gdb
ARTY35 := xc7a35ticsg324-1L
ARTY100 := xc7a100tcsg324-1
FPGA ?= $(ARTY100)
DEVICE ?= /dev/ttyUSB1
BAUDRATE ?= 115200

all: build-sw build-hw program-hw load-demo

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

.PHONY: start-vivado
start-vivado:
	make -C ./build/lowrisc_ibex_super_system_0/synth-vivado/ build-gui

.PHONY: load-demo-run
load-demo-run:
	./util/load_super_system.sh run ./sw/build/demo/demo

.PHONY: load-demo-halt
load-demo-halt:
	./util/load_super_system.sh halt ./sw/build/demo/demo &

.PHONY: screen-demo
screen-demo:
	@echo "Use 'ctrl-a k' to exit the screen command"
	@sleep 3
	@screen ${DEVICE} ${BAUDRATE}

.PHONY: debug-demo
debug-demo: load-demo-halt
	$(GDB) -ex "target extended-remote localhost:3333" \
		./sw/build/demo/demo

.PHONY: clean
clean:
	@rm -rf build sw/build
