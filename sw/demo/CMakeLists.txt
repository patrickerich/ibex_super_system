add_prog(demo main.c)


add_custom_command(
  TARGET demo POST_BUILD
  COMMAND riscv32-unknown-elf-objcopy -O binary "$<TARGET_FILE:demo>" "$<TARGET_FILE:demo>.bin"
  COMMAND srec_cat "$<TARGET_FILE:demo>.bin" -binary -offset 0x00000000 -byte-swap 4 -o "$<TARGET_FILE:demo>.vmem" -vmem
  VERBATIM)