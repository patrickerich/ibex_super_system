#include "super_system.h"
#include "dev_access.h"
#include "gpio.h"

void set_outputs(gpio_t gpio, uint32_t outputs) {
  DEV_WRITE(gpio, outputs);
}

uint32_t get_outputs(gpio_t gpio) {
  return DEV_READ(gpio);
}

void set_output_bit(gpio_t gpio, uint32_t output_bit_index,
    uint32_t output_bit) {
  output_bit &= 1;

  uint32_t output_bits = get_outputs(gpio);
  output_bits &= ~(1 << output_bit_index);
  output_bits |= (output_bit << output_bit_index);

  set_outputs(gpio, output_bits);
}

uint32_t get_output_bit(gpio_t gpio, uint32_t output_bit_index) {
  uint32_t output_bits = get_outputs(gpio);
  output_bits >>= output_bit_index;
  output_bits &= 1;

  return output_bits;
}

void simple_gpi_handler(void) __attribute__((interrupt));

void simple_gpi_handler(void) {
}

void gpi_init(void) {
  install_exception_handler(16, &simple_gpi_handler);
}

void gpi_enable(void) {
  // enable timer interrupt
  asm volatile("csrs  mie, %0\n" : : "r"(1<<16));
  // enable global interrupt
  asm volatile("csrs  mstatus, %0\n" : : "r"(0x8));
}

void gpi_disable(void) { asm volatile("csrc  mie, %0\n" : : "r"(0x00)); }
