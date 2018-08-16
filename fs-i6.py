import serial
import os
import time

INPUT_BUFFER_SIZE = 40
INPUT_DATA_SIZE = 32
HEAD_WORD = 0x4020
NUMBER_OF_CH = 14
ACTIVE_CH = 6


def main_loop():
    port = serial.Serial('/dev/ttyS0', 115200, timeout=0.01)
    ch = []
    for i in range(NUMBER_OF_CH):
        ch.append(0)

    try:
        while True:
            data = port.read(INPUT_BUFFER_SIZE)
            msg_head = data[0] + (data[1] << 8)
            if len(data) == INPUT_DATA_SIZE and msg_head == HEAD_WORD:
                os.system('clear')

                for i in range(NUMBER_OF_CH):
                    ch[i] = data[i*2+2] + (data[i*2+3] << 8)
                if check_sum(data):
                    for i in range(ACTIVE_CH):
                        print('CH{}: {} {}'.format(i+1, stat_line(ch[i]), ch[i]))
    except KeyboardInterrupt:
        port.close()


def stat_line(value, min_val=1000, max_val=2000, length=50):
    resolution = (max_val - min_val) / length #20
    line = ''

    # Left
    for i in range(int(length/2)):
        if value <= (min_val + i * resolution):
            line += '|'
        else:
            line += ' '

    # Center
    line += '|'

    # Right
    for i in range(int(length/2)-1, -1, -1):
        if value >= (max_val - i * resolution):
            line += '|'
        else:
            line += ' '

    return line


def check_sum(data):
    sum = 0
    for i in range(INPUT_DATA_SIZE - 2):
        sum += data[i]
    sum += data[INPUT_DATA_SIZE-2] + (data[INPUT_DATA_SIZE-1] << 8)

    if sum == 0xFFFF:
        return True
    else:
        return False


def test_func():
    pass


if __name__ == '__main__':
    main_loop()
