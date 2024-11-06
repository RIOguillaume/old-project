import serial
import time


ser = serial.Serial()
ser.port = "/dev/ttyTHS1"
ser.baudrate = 115200
ser.bytesize = serial.EIGHTBITS
ser.parity = serial.PARITY_NONE
ser.stopbits = serial.STOPBITS_ONE
ser.timeout = 5
ser.xomxoff = False
ser.rtscts = False
ser.dsrdtr = False
ser.writeTimeout = 2
ser.open()

def send_msg(message):
    print("msg envoyé vers l'arduino :"+message)
    ser.write((message+"|").encode())

def get_msg():
    data = ser.readline()
    if data:
        return data
    return 0

def data_available():
    if ser.in_waiting:
        return True
    else:
        return False


"""
while True:
    while ser.in_waiting:
        get_msg()
"""

