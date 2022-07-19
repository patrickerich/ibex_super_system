
# from serial_device.serial_device import SerialCmdLine
from serial_device.tools import SerialCmdLine


cmdint = SerialCmdLine(id_prefix='IBEXSS', baudrate=115200)
cmdint.cmd_line()
