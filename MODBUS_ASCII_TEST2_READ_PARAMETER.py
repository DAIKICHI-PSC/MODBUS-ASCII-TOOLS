#This script is to test MODBUS_ASCII_LRC with real serial communication

import serial
import time
from MODBUS_ASCII_LRC import LRC_CREATE, LRC_CHECK
from MODBUS_ASCII_CONVERTERS import RESPONSE_TO_BYTES
COMPORT = "COM6"
#COMMAND = "01039000000A"
COMMAND = "02050403FF00"
COM_TIMEOUT = 3

client = serial.Serial(port=COMPORT, baudrate=230400, bytesize=8, parity='N', stopbits=1, timeout=1.0, xonxoff=0, rtscts=0, dsrdtr=None)
print("[Serial status]")
print(client)

print("[Raw data to send]")
print(COMMAND)
ret, LRC_Command = LRC_CREATE(COMMAND) #Process data to send.
print("[Status of LRC_CREATE]")
print(ret)
print("[Processed data by LRC_CREATE]")
print(LRC_Command)
client.write(bytes(LRC_Command, 'utf-8'))

start_Time = time.time()
LRC_Command = ""
while(True):
    serial_Buffer =client.readline()
    LRC_Command = LRC_Command + serial_Buffer.decode("utf-8")
    if ("\n" in LRC_Command) == True: #Check the charactors means the end of communication.
        print("[Received raw data]")
        print(LRC_Command)
        ret, command = LRC_CHECK(LRC_Command) #Process received data.
        print("[Status of LRC_CHECK]")
        print(ret)
        print("[Processed data by LRC_CHECK]")
        print(command)
        break
    elapsed_Time = time.time() - start_Time
    if elapsed_Time > COM_TIMEOUT: #Check elapsed time of communication.
        print(">Connection time out.")
        break

ret, result = RESPONSE_TO_BYTES(command)
print(ret)
print(result)

client.close()
print("[Serial status]")
print(client)
