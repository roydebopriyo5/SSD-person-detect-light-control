import serial
import time

#ser = serial.Serial('COM4', 9600)

def led(switch):
    if switch == 1:
        print("LED is on...") 
        #ser.write(b'H')

    else:
        print("LED is off...")
        #ser.write(b'L')
