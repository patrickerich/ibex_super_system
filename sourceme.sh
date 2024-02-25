THIS_SCRIPT=$(readlink -f "$0")
export PROJ_DIR=$(dirname "$THIS_SCRIPT")

# The RISCV toolchain
# RISCV_TOOLCHAIN=/opt/lowrisc/lowrisc-toolchain-rv32imcb-20220524-1/bin
RISCV_TOOLCHAIN=/opt/riscv/bin
export path=($RISCV_TOOLCHAIN $path)
export RISCV_GCC=$RISCV_TOOLCHAIN/riscv64-unknown-elf-gcc
export RISCV_OBJCOPY=$RISCV_TOOLCHAIN/riscv64-unknown-elf-objcopy

# Xilinx settings
XILINX=/opt/Xilinx/Vivado/Vivado/2021.2/settings64.sh
source $XILINX

# The python virtual environment
VENV_DIR=$PROJ_DIR/.venv
VENV_REQS=$PROJ_DIR/requirements.txt
VENV_PROMPT=${PROJ_DIR##*/}
export VENV_ACT=$VENV_DIR/bin/activate

function create_py_venv() {
    python -m venv --prompt $VENV_PROMPT --upgrade-deps $VENV_DIR
    . $VENV_ACT
    pip install wheel
    pip install -r $VENV_REQS
}

if [ ! -d $VENV_DIR ]; then
    # Create the python virtual environment if it does not already exist
    printf "\n\tPython virtual environment not found!"
    printf "\n\tSetting up Python virtual environment...\n"
    create_py_venv
else
    # Activate the python virtual environment if it already exists
    printf "\n\tPython virtual environment found!"
    printf "\n\tActivating Python virtual environment...\n"
    . $VENV_ACT
fi

# Change to the projects directory
cd $PROJ_DIR
