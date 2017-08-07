from mouse_event import *
from key_event import *
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

        x = int(data[4])
        y = int(data[5])
        trig = int(data[6])
        reset = int(data[7])

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

#try:
while True:

    data = ""
    data = conn.recv(512)
    data = data.split()

    steer = float(data[0])
    thr = int(data[1])
    brk = int(data[2])
    nitr = int(data[3])
    x = int(data[4])*p[0]
    y = int(data[5])*p[1]
    trig = int(data[6])
    reset = int(data[7])

    disp = time()
    
    if reset == 1:
        print "Reset button pressed"
        
    else:
        (cux,cuy) = mouse.get_position()
        pos = (int(cux+x), int(cuy+y))
        mouse.move_mouse(pos)

        if trig == 1 and round(time()-a,5) >= 0.2:
            mouse.click(pos,"left")
            a = time()

        if(steer < -10.0 and steer > -30.0):
            PressKey(DIK_D)
        if (steer > -10):
            ReleaseKey(DIK_D)

        if(steer > 10.0 and steer < 30.0):
            PressKey(DIK_A)
        if (steer < 10):
            ReleaseKey(DIK_A)

        if thr == 1:
            PressKey(DIK_W)
        if thr == 0:
            ReleaseKey(DIK_W)

        if brk == 1:
            PressKey(DIK_S)
        if brk == 0:
            ReleaseKey(DIK_S)

        if nitr == 1:
            PressKey(DIK_SPACE)
        if nitr == 0:
            ReleaseKey(DIK_SPACE)

    print "steer : {0}\nAccelerator : {1}\nBrake : {2}\nNitrous : {3}\nMouse x : {4}\nMouse y : {5}\nTrigger : {6}".format(steer,trig,brk,nitr,x,y,trig);

##except:
##    print ' Exiting ... '
##    sleep(1)
##    socket.close()
##    sys.exit()
