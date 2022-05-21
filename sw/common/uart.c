#include "uart.h"
#include "dev_access.h"

// void uart_out(void* uart_ptr, char c) {
//   while(DEV_READ(uart_ptr + UART_STATUS_REG) & UART_STATUS_TX_FULL);

//   DEV_WRITE(uart_ptr + UART_TX_REG, c);
// }


void uart_out(uart_t uart, char c) {
  while(DEV_READ(uart + UART_STATUS_REG) & UART_STATUS_TX_FULL);

  DEV_WRITE(uart + UART_TX_REG, c);
}