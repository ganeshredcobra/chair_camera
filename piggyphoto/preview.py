import piggyphoto, pygame
import serial,os
import time
import commands

pygame.init()
sound=pygame.mixer.Sound('bonus.wav')
path=os.path.realpath("Pictures/Capture")
if os.path.exists(path):
    os.chdir(path)
else:
    os.system('mkdir -p %s'%path)
    os.chdir(path)
raw=commands.getoutput("dmesg | grep 'FTDI USB Serial Device converter now attached to'")
port=raw[-7:]
print port
ser = serial.Serial("/dev/%s"%port,baudrate=9600,timeout=1)
prev_state=None
size = width, height = 800, 600
def show(file):
    picture = pygame.image.load(file)
    pygame.display.set_mode(picture.get_size())
    main_surface = pygame.display.get_surface()
    main_surface.blit(picture, (0, 0))
    pygame.display.flip()
def quit_pressed():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return True
    return False
C = piggyphoto.camera()
C.leave_locked()
while True:
    ser.flushInput()
    data=ser.readline().strip('\r\n')
    print data
    if data=="0":
        if prev_state==None:
            prev_state=data
        prev_state=data
    elif data=="1":
        if prev_state==None:
            prev_state=data
        elif prev_state=="0":
                C.capture_preview('pic00.jpg')
                sound.play()
                show('pic00.jpg')
        prev_state=data
    else:
        pass
        print "No data"




