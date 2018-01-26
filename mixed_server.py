import RPi.GPIO as GPIO
import mpu6050
import socket
from adxl345 import ADXL345
from math import sqrt
from time import sleep
from sys import exit

thr_pin = 26
brk_pin = 19
nitr_pin = 13
reset_pin = 23
mouse_click_pin = 17

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

##ip = raw_input("Enter the ip shown at server : ")
##port = raw_input("Enter port shown at server : ")
##address = (ip,port)

##Enter the IP address shown at server. No need to change port.
## listing all previous ips
## '192.168.201.106'
address = ('169.254.109.72',1234)

try:
    sock.connect(address)
    print ' Connected to \tIP : ' + str(address[0]) + "\t port : " + str(address[1])
except:
    print ' Connection failed ... '
    sleep(2)
    exit()

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(thr_pin, GPIO.IN,GPIO.PUD_DOWN)
GPIO.setup(brk_pin, GPIO.IN,GPIO.PUD_DOWN)
GPIO.setup(nitr_pin, GPIO.IN,GPIO.PUD_DOWN)
GPIO.setup(reset_pin, GPIO.IN,GPIO.PUD_DOWN)
GPIO.setup(mouse_pin, GPIO.IN,GPIO.PUD_DOWN)

acc = mpu6050.mpu6050(0x68)
adxl345 = ADXL345()

acc.read_accel_range(16)

accel_data = acc.get_accel_data()
axes = adxl345.getAxes(True)

zi = accel_data['z']

try:
    while True:
        data = ""
        axes = adxl345.getAxes(True)
        z = axes['z'] - zi
        accel_data = acc.get_accel_data()

        steer = int(z)
        thr = GPIO.input(thr_pin)
        brk = GPIO.input(brk_pin)
        nitr = GPIO.input(nitr_pin)
        reset = GPIO.input(reset_pin)
        click = GPIO.input(mouse_click_pin)

        data = "{} {} {} {} {} {} {} {}".format(steer,thr,brk,nitr,x,y,click,reset)
        sock.sendto(data,address)
        print data

finally:
    sock.close()
    GPIO.cleanup()
