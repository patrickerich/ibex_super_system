# tb_ibex_super_system.py
import cocotb
from testbench import TestBench


@cocotb.test()
async def ibexss_demo_echo_test(dut):
    '''
        Check the echo of the demo
    '''
    dut._log.info('Verify that the demo echos (tx = rx)')

    tb = TestBench(
        dut,
        clk_period=20,
        clk_period_unit='ns',
        uart_baudrate=115200,
        uart_bits=8,
    )

    tb.connect_uart()
    await tb.start_clock()
    await tb.reset(delay_clk_periods=3, reset_clk_periods=2)
    # Give the system enough time to boot up
    await tb.run_for(clk_periods=1000)

    send_msg = b'Hello world!'
    send_msg = bytearray('Hello world!', 'utf-8')
    await tb.uart_source.write(send_msg)
    # Wait long enough...
    await tb.run_for(clk_periods=int(len(send_msg)*11*(1/20E-09)/115200))

    recv_msg = await tb.uart_sink.read(len(send_msg))

    print(f'Sent     : {send_msg}')
    print(f'Received : {recv_msg}')

    premise = (recv_msg == send_msg)
    assert premise, "Received message differs from sent message"

    dut._log.info("demo echo test.....done")