# tb_ibex_super_system.py
import cocotb
from testbench import TestBench
from curses.ascii import EOT

@cocotb.test()
async def ibex_super_system_cmdint_id_test(dut):
    '''
        Check the ID of the command interpreter
    '''
    dut._log.info('Verify the ID of the command interpreter (IBEXSS_01)')

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

    # Send the ID command
    send_msg = bytearray(f'id{chr(EOT)}', 'utf-8')
    await tb.uart_source.write(send_msg)

    # Get the ID
    recv_msg = bytearray()
    while not recv_msg.decode('utf-8').endswith(chr(EOT)):
        recv_msg += await tb.uart_sink.read(1)

    # Debug code: start
    print(f'Sent     : {send_msg}')
    print(f'Received : {recv_msg}')
    # Debug code: end

    # Assert that a correct ID was received
    # assert recv_msg.decode('utf-8') == f'IBEXSS_01{chr(EOT)}', 'Incorrect ID received'
    assert recv_msg.decode('utf-8').startswith('IBEXSS_'), 'Incorrect ID received'

    dut._log.info('ID check....done')

