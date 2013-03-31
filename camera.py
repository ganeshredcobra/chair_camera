#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       camera.py
#       
#       Copyright 2013 Ganesh <ganeshredcobra@gmail.com>
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.

import serial,os
import time
import commands
import pygame
import subprocess

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
            status=commands.getoutput('ls')
            if status=='':
                os.system('gphoto2 --capture-image-and-download --filename "pic00.jpg"&')
                os.system('eog --fullscreen pic00.jpg &')
                sound.play()
            else:
                files=status.split()
                #last_file=files.sort()
                count=''.join([os.path.splitext(x)[0] for x in files][-1:])[-2:]
                #print count
                name=int(count)+01
                #print name
                #p=os.system('gphoto2 --capture-image-and-download --filename "pic%02d.jpg" &'%name)
                #time.sleep(4)
                stat,op=commands.getstatusoutput('gphoto2 --capture-image-and-download --filename "pic%02d.jpg" '%name)
                #print p
                if stat==0:
                    os.system('pkill eog &')
                    os.system('eog --fullscreen pic%02d.jpg &'%name)
                    sound.play()
                else:
                    print "No Focus"
        prev_state=data
    else:
        pass
        print "No data"


