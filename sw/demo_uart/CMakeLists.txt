add_prog(demo_uart main.c)


add_custom_command(
  TARGET demo_uart POST_BUILD
  COMMAND riscv32-unknown-elf-objcopy -O binary "$<TARGET_FILE:demo_uart>" "$<TARGET_FILE:demo_uart>.bin"
  COMMAND srec_cat "$<TARGET_FILE:demo_uart>.bin" -binary -offset 0x00000000 -byte-swap 4 -o "$<TARGET_FILE:demo_uart>.vmem" -vmem
  VERBATIM)