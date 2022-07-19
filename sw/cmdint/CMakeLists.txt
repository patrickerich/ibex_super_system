add_prog(cmdint main.c)


add_custom_command(
  TARGET cmdint POST_BUILD
  COMMAND riscv32-unknown-elf-objcopy -O binary "$<TARGET_FILE:cmdint>" "$<TARGET_FILE:cmdint>.bin"
  COMMAND srec_cat "$<TARGET_FILE:cmdint>.bin" -binary -offset 0x00000000 -byte-swap 4 -o "$<TARGET_FILE:cmdint>.vmem" -vmem
  VERBATIM)