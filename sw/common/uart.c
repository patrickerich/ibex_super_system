#include <stdbool.h>
#include <stdio.h>

#include "uart.h"
#include "dev_access.h"
#include "super_system.h"

bool is_rx_empty(uart_t uart) {
  return (DEV_READ(uart + UART_STATUS_REG) & UART_STATUS_RX_EMPTY);
}

bool is_tx_full(uart_t uart) {
  return (DEV_READ(uart + UART_STATUS_REG) & UART_STATUS_TX_FULL);
}

int uart_in(uart_t uart) {
  int res = EOF;
  if (!is_rx_empty(uart)) {
    res = DEV_READ(uart + UART_RX_REG);
  }
  return res;
}

void uart_out(uart_t uart, char c) {
  while (is_tx_full(uart));
  DEV_WRITE(uart + UART_TX_REG, c);
}

void uart_enable(void) {
  // enable uart interrupt
  asm volatile("csrs  mie, %0\n" : : "r"(1<<16));
  // enable global interrupt
  asm volatile("csrs  mstatus, %0\n" : : "r"(1<<3));
}

void simple_uart_in_handler(void) __attribute__((interrupt));

void simple_uart_in_handler(void) {
  while (!is_rx_empty(DEFAULT_UART)) {
    uart_out(DEFAULT_UART, uart_in(DEFAULT_UART));
  }
}

void uart_init(void) {
  install_exception_handler(16, &simple_uart_in_handler);
}
