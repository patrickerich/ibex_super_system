#ifndef UART_H__
#define UART_H__

#define UART_RX_REG 0
#define UART_TX_REG 4
#define UART_STATUS_REG 8

#define UART_STATUS_RX_EMPTY 1
#define UART_STATUS_TX_FULL 2

typedef void* uart_t;

#define UART_FROM_BASE_ADDR(addr)((uart_t)(addr))

void uart_init(void);
void uart_enable(void);
int uart_in(uart_t uart);
void uart_out(uart_t uart, char c);

#endif // UART_H__
