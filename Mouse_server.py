from mouse_event import *
from time import *
from socket import *
import os


addr = (gethostbyname(getfqdn()),1234)
conn = socket(AF_INET,SOCK_DGRAM)
conn.bind(addr)
print 'Connected to {0} at {1}'.format(addr[0],addr[1])
mouse = Mouse()
sx,sy = mouse.screen_size()
mouse.move_mouse((sx/2,sy/2))

def cali():
    a = time()
    while True:
        
        data = ""
        data = conn.recv(512)
        data = data.split()
        
        x = int(data[0])
        y = int(data[1])
        trig = int(data[2])
        reset = int(data[3])

        if reset == 1:
            if round(time()-a) >= 2:
                return mouse.get_position()
                
        else:
            (cux,cuy) = mouse.get_position()
            pos = (int(cux+x), int(cuy+y))
            mouse.move_mouse(pos)
            a = time() 

def ends_calib():
    print " Calibrating window ends ",
    print "\nMove cursor top left corner : ",
    (tlsx,tlsy) = cali()
    print (tlsx,tlsy)
    print "Move cursor to top right corner : ",
    (trsx,trsy) = cali()
    print (trsx,trsy)
    print "Move cursor to bottom left corner : ",
    (blsx,blsy) = cali()
    print (blsx,blsy)
    print "Move cursor to bottom right cursor : ",
    (brsx,brsy) = cali()
    print (brsx,brsy)

    p = float((trsx-tlsx)+(brsx-blsx))/2,float((brsy-trsy)+(blsy-tlsy))/2
    p = (round(sx/p[0],2),round(sy/p[1],2))
    os.system("cls")
    print "Mouse calibrated"
    sleep(2)
    return p

p = ends_calib()
a = time()
while True:
    data = ""
    data = conn.recv(512)
    data = data.split()
    
    x = int(data[0])*p[0]
    y = int(data[1])*p[1]
    trig = int(data[2])
    reset = int(data[3])

    if reset == 1:
##        mouse.move_mouse((sx/2,sy/2))
        x = y = trig = 0
        
    else:
        (cux,cuy) = mouse.get_position()
        pos = (int(cux+x), int(cuy+y))
        mouse.move_mouse(pos)
        if trig == 1 and round(time()-a,5) >= 0.0125:
            mouse.click(pos,"left")
            a = time()
        
        print "x,y : {0},\t{1}\t click : {2}".format(x,y,trig);
