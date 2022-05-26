import time
import serial
import serial.tools.list_ports

MAX_RESPONSE_TIME = 0.1
NEXT_TRANSACTION_WAIT_TIME = 0.1
MAX_TRIES = 100


def get_port():
    port_list = [i.device for i in list(serial.tools.list_ports.comports())]
    ports = sorted(port_list, reverse=True)
    if len(ports) == 1:
        return ports[0]
    else:
        print("Available ports:")
        for idx, port in enumerate(ports):
            print(f"{idx+1: <3} : {port}")
        selection = 0
        while selection not in range(1, len(ports) + 1):
            try:
                selection = int(input("Please select a serial device: "))
            except ValueError:
                pass
        return ports[selection - 1]


def serial_get(device):
    reply = ''
    timeout = time.time() + MAX_RESPONSE_TIME
    while time.time() < timeout:
        if device.in_waiting > 0:
            try:
                reply += device.read().decode()
            except Exception:
                reply += "_ERROR_"
    return reply


def main():
    try:
        device = serial.Serial(port=get_port(), baudrate=115200)
    except serial.serialutil.SerialException:
        print('Unable to open serial port')
    else:
        count = 0
        error_count = 0
        keep_going = True
        while keep_going and count < MAX_TRIES:
            try:
                time.sleep(NEXT_TRANSACTION_WAIT_TIME)
                msg = f"Hello world ({count})"
                # print(f"Sending: {msg}", end="")
                device.write(msg.encode('utf-8'))
                received = serial_get(device)
                # print(f"Received: {received}")
                count += 1
                if received != msg:
                    error_count += 1
            except KeyboardInterrupt:
                device.close()
                keep_going = False
        error_rate = (error_count/count) * 100
        print(f"count = {count}")
        print(f"error_count = {error_count}")
        print(f"error_rate = {error_rate}%")


if __name__ == "__main__":
    main()
