#!/usr/bin/env python

import RPi.GPIO as GPIO
import time
import cv2
from glob import glob
import os
import sys
import picamera
from pylepton_capture import *
from test_wifi import *
import DS1307
from i2cDetect import *
from check_usb import *
from generate_header import *
from mount_usb import *

import ntplib, datetime
from time import ctime, sleep

#Set up workspace (?)
sys.path.insert(0,'/home/pi/Desktop/')

#GPIO set up
redLED = 19
yelLED = 13
speaker = 26
j1 = 5
j2 = 6
mode = 1
timeCheck = True

#Set up camera
camera = picamera.PiCamera()
camera.led = False
picamera.PiCamera.CAPTURE_TIMEOUT = 60
#Set up LEDs and Speaker
GPIO.setmode(GPIO.BCM)
GPIO.setup(redLED, GPIO.OUT)
GPIO.setup(yelLED, GPIO.OUT)
GPIO.setup(speaker, GPIO.OUT)
try:
        #Mount USB
    mounted = mount_usb()
    print 'USB Mount state is: ' + str(mounted)
    if mounted == False:
        raise TypeError('Failed to mount usb')
    #Buzz start up sound
    GPIO.output(speaker,False)
    GPIO.output(redLED,False)
    GPIO.output(yelLED,False)
    GPIO.output(yelLED,True)
    for i in range(3):
        startSound = time.time()
        while time.time() - startSound < 0.3:
            GPIO.output(speaker,True)
        GPIO.output(speaker,False)
        stopSound = time.time()
        while time.time() - stopSound < 0.3:
            pass
    #Check internet connection
    internet = internet_on()
    for n in range (128):
	    if i2cDetect(n):
		    clockCheck = True
		    break
    if clockCheck:
        clock = DS1307.DS1307(1, 0x68)
        if internet:
            print("Can open google.com; setting RTC to NTP time.")
            #clock.write_now()
            ntpc = ntplib.NTPClient()
            clock.write_datetime(datetime.datetime.utcfromtimestamp(ntpc.request('europe.pool.ntp.org').tx_time))
        #Check clock is up to date
        try:
            t1 = clock.read_datetime()
            print("Time read from RTC:",t1.strftime("%Y-%m-%d %H:%M:%S"))
            t1 = t1.timetuple()
            if t1[0] < 2017:
                timeCheck = False
        except:
            timeCheck = False
    else:
        timeCheck = False
    #Begin running
    goTime = 700
    startTime = 0
    count = 0
    count2 = 0
    testTime = 0
    while check_usb(): #Maybe change to memory check
            if timeCheck:
            #Time Stuff - Create new folder after time limit
                if goTime-startTime >= 60*10: #If time is greater than 600 seconds or 60 seconds?
                    #Create Image Directory
                    t1 = clock.read_datetime()
                    t1 = t1.timetuple()
                    date = "%04d-%02d-%02d--"%(t1[0],t1[1],t1[2])
                    timez = "%02d-%02d-%02d"%(t1[3],t1[4],t1[5])
                    dirName = date+timez
                    fullDN = '/media/usb/'+dirName
                    os.mkdir(fullDN)
                    startTime = (t1[3]*60*60) +(t1[4]*60) +(t1[5])
                #Capture and save from the thermal camera
                t1 = clock.read_datetime()
                t1 = t1.timetuple()
                goTime = (t1[3]*60*60) +(t1[4]*60) +(t1[5])
                while goTime - testTime < 1:
                    t1 = clock.read_datetime()
                    t1 = t1.timetuple()
                    goTime = (t1[3]*60*60) +(t1[4]*60) +(t1[5])
                testTime = goTime
                timez = "%02d-%02d-%02d"%(t1[3],t1[4],t1[5])
            else:
                if count2 == 0:
                    for name in os.listdir('/media/usb/'):
                        if name[:8] == 'noclock_':
                            count3 = int(name[8:])
                            if count3 > count2:
                                count2 = count3
                if goTime-startTime >= 60*10:
                    count2 += 1
                    dirName = 'noclock_'+str(count2)
                    fullDN = '/media/usb/'+dirName
                    os.mkdir(fullDN)
                    startTime = time.time()
                timez = "0"
                goTime = time.time()
                while goTime - testTime < 1:
                    goTime = time.time()
                testTime = goTime

            startSound = time.time()
            while time.time() - startSound < 0.1:
                GPIO.output(speaker,True)
            GPIO.output(speaker,False)
            if mode == 1:
                sampleStartTime = time.time()
                image,fpa,aux = capture(flip_v=False, device = "/dev/spidev0.1")
                cv2.imwrite(fullDN+'/image_thermal_%s_%09d.png'%(timez,count),image)
                #print 'Thermal captured'
                #Capture and save from the rgb camera
                camera.capture(fullDN+'/image_rgb_%s_%09d.jpg'%(timez,count))#,quality=10)
                #print 'RGB captured'
                generate_header(fullDN,'image_thermal_%s_%09d'%(timez,count),timez,fpa,aux)
                count += 1
            elif mode == 2:
                camera.start_recording(fullDN+'/video_rgb_%s_%09d.h264'%(timez,count))
                camera.wait_recording(10)
                camera.stop_recording()
                print 'Video captured'
            elif mode == 3:
                image,fpa,aux = capture(flip_v=False, device = "/dev/spidev0.1")
                cv2.imwrite(fullDN+'/image_thermal_%s_%09d.png'%(timez,count),image)
                print 'Thermal captured'
                generate_header(fullDN,'image_thermal_%s_%09d'%(timez,count),timez,fpa,aux)

    raise TypeError('Out Of USB Storage')
    focalPlane = numpy.ones((1))*1.0
    fpa = focalPlane*fpa
    auxTemp = numpy.ones((1))*1.0
    aux = auxTemp*aux
    p = (fullDN+'/fpa_%s_%09d.txt'%(timez,count))
    a = (fullDN+'/aux_%s_%09d.txt'%(timez,count))
    numpy.savetxt(p,fpa)
    numpy.savetxt(a,aux)
    print'Elapsed time='+ str(goTime - startTime) + '[s]'
    print ' '

except Exception as e:
    error = open('/home/pi/Desktop/error.txt','w')
    error.write(str(e))
    error.close()
    print sys.exc_info()
    GPIO.output(yelLED, False)
    errorTime = time.time()
    while True:
        startSound = time.time()
        while time.time() - startSound < 1:
            GPIO.output(redLED,True)
            GPIO.output(speaker,True)
        GPIO.output(redLED,False)
        GPIO.output(speaker,False)
        stopSound = time.time()
        while time.time() - stopSound < 0.3:
            pass


