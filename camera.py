#! /usr/bin/env python

import serial,os
import time
import commands

path=os.path.realpath("Pictures/Capture")
if os.path.exists(path):
    os.chdir(path)
else:
    os.system('mkdir -p %s'%path)
    os.chdir(path)
raw=commands.getoutput("dmesg | grep 'FTDI USB Serial Device converter now attached to'")
port=raw[-7:]
ser = serial.Serial("/dev/%s"%port, 9600, timeout=1)
prev_state=None
while True:
    ser.flushInput()
    data=ser.readline().strip()
    #print data
    if data=="0":
        if prev_state==None:
            prev_state=data
        prev_state=data
    elif data=="1":
        if prev_state==None:
            prev_state=data
        elif prev_state=="0":
            status=commands.getoutput('ls')
            if status=='':
                os.system('gphoto2 --capture-image-and-download --filename "pic00.jpg"')
            else:
                files=status.split()
                #last_file=files.sort()
                count=''.join([os.path.splitext(x)[0] for x in files][-1:])[-2:]
                #print count
                name=int(count)+01
                #print name
                os.system('gphoto2 --capture-image-and-download --filename "pic%02d.jpg"'%name)
                os.system('pkill eog &')
                os.system('eog --fullscreen pic%02d.jpg &'%name)
        prev_state=data
    else:
        pass


