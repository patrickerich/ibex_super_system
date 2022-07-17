#ifndef UART_H__
#define UART_H__

#include <stdbool.h>

#define UART_RX_REG 0
#define UART_TX_REG 4
#define UART_STATUS_REG 8

#define UART_STATUS_RX_EMPTY 1
#define UART_STATUS_TX_FULL 2

typedef void* uart_t;

#define UART_FROM_BASE_ADDR(addr)((uart_t)(addr))

bool is_rx_empty(uart_t uart);
bool is_tx_full(uart_t uart);
int uart_in(uart_t uart);
void uart_out(uart_t uart, char c);
void uart_enable(void);
void simple_uart_in_handler(void);
void uart_init(void);

#endif // UART_H__
