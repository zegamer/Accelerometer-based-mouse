from mouse_event import *
import serial
import win32api
from time import sleep


# 'r' is sensitivity...
r = 0.5 # float(raw_input(" Enter sensitivity (0-1): "));

port = "COM3"   # Hard-code your comms port and the baud rate
baud = 9600

ser = serial.Serial(port,baud)

mouse = Mouse()
counter = 0
while True:

    data = ser.readline()
    if counter <= 1:
        counter = counter+1
        continue
    data = data.split()
    x = int(data[0])
    y = int(data[1])

    cux,cuy = mouse.get_position()
    print ' At : ' + str(cux) + ' ' + str(cuy) 
    mouse.move_mouse((int(x+cux), int(y+cuy)))
    print " x : " + str(x) + "\ty : " + str(y)

    
