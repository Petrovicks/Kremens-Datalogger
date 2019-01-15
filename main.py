#!/usr/bin/env python

#Pi hardware setup
import RPi.GPIO as GPIO

#Required for directory manipulation
import os
import sys
from glob import glob
from generate_header import *

#Required for camera capture
import picamera
from pylepton_capture import *
import cv2
import numpy

#Libraries for hardware tests
from test_wifi import *
from check_usb import *
from mount_usb import *
from i2cDetect import *

#Timekeeping
import time
import DS1307 #RTC python library
import ntplib, datetime #ntp server interfacing

#Bash scripting
import subprocess

#Set up workspace for imports
#sys.path.insert(0, '/home/pi/Desktop/')

#Hardware setup
redLED = 19 #Speaker LED
yelLED = 13 #General errors
speaker = 26
j1 = 5 #jumpers for mode setting
j2 = 6 #jumpers for mode setting
mode = 1
validTime = True

#Initialize camera
camera = picamera.PiCamera()
camera.led = False
picamera.PiCamera.CAPTURE_TIMEOUT = 60

#Initialize all GPIO after camera
GPIO.setmode(GPIO.BCM)
GPIO.setup(redLED, GPIO.OUT)
GPIO.setup(yelLED, GPIO.OUT)
GPIO.setup(speaker, GPIO.OUT)

try:
    #check USB mounting
    mounted = mount_usb()
    print 'USB mount :' + str(mounted)
    if mounted == False:
		raise TypeError('Failed to mount USB.')
    #Buzz start up sound
    GPIO.output(speaker,False)
    GPIO.output(redLED,False)
    GPIO.output(yelLED,False)
    GPIO.output(yelLED,True)

    #Beep for 0.3 seconds, silence for 0.3 seconds
    #Repeat 3 times
    for i in range(3):
    	GPIO.output(speaker, True)
    	time.sleep(0.3)
    	GPIO.output(speaker, False)
    	time.sleep(0.3)

    #Find the RTC (0 - 127)
    for n in range(128):
    	if i2cDetect(n):
    		clockCheck = True
    		break
    if clockCheck:
    	clock = DS1307.DS1307(1, 0x68) #Initializes handler for RTC with HW ADDR as 0x68
    	if internet_on():
    		print("Connection verified via google.com, setting RTC to NTP time.")
    		ntpc = ntplib.NTPClient()
    		#Obtain time from ntp server and write it to the RTC
            clock.write_datetime(datetime.datetime.utcfromtimestamp(ntpc.request('europe.pool.ntp.org').tx_time))
        #Verify the time is valid
        try:
        	rtc_time = clock.read_datetime()
        	print("Time read from RTC:",rtc_time.strftime("%Y-%m-%d %H:%M:%S"))
            bashCommand = "date -s '" + rtc_time.strftime("%Y-%m-%d %H:%M:%S") + "'"
            subprocess.call(bashCommand, shell=True)
        	rtc_time = rtc_time.timetuple()
        	if rtc_time[0] < 2000:
        		validTime = False
        except:
        	validTime = False
    else:
    	validTime = False

    #Begin main routine
    eventTime = 700
    startTime = 0
    count = 0
    count2 = 0
    testTime = 0
    while check_usb(): #Continue running as long as USB is inserted.
            if validTime:
                #Time Stuff - Create new folder after time limit
                if eventTime-startTime >= 60*10: #If time is greater than 600 seconds
                    #Get time from RTC
                    rtc_time = clock.read_datetime()

                    #Sync Pi HW clock with RTC
                    bashCommand = "date -s '" + rtc_time.strftime("%Y-%m-%d %H:%M:%S") + "'"
                    subprocess.call(bashCommand, shell=True)

                    #Create directory name using RTC time
                    rtc_time = rtc_time.timetuple()
                    dirName = "%04d-%02d-%02d--%02d-%02d-%02d"%(rtc_time[0],rtc_time[1],rtc_time[2],rtc_time[3],rtc_time[4],rtc_time[5])
                    fullDN = '/media/usb/'+dirName
                    os.mkdir(fullDN)
                    startTime = (rtc_time[3]*60*60) +(rtc_time[4]*60) +(rtc_time[5])

                #Enforce one second increments between pictures using Pi HW clock
                currentTime = time.strftime("%Y-%m-%d %H:%M:%S")
                currentTime = datetime.datetime.strptime(currentTime, "%Y-%m-%d %H:%M:%S")
                currentTime = currentTime.timetuple()
                currentTime = (currentTime[3]*60*60) + (currentTime[4]*60) + currentTime[5]

                while currentTime - eventTime < 1:
                    currentTime = time.strftime("%Y-%m-%d %H:%M:%S")
                    currentTime = datetime.datetime.strptime(currentTime, "%Y-%m-%d %H:%M:%S")
                    currentTime = currentTime.timetuple()   
                    currentTime = (currentTime[3]*60*60) + (currentTime[4]*60) + currentTime[5]                 

                #Read Pi HW clock to decrease i2c usage
                # rtc_time = time.strftime("%Y-%m-%d %H:%M:%S")
                # rtc_time = datetime.datetime.strptime(rtc_time, "%Y-%m-%d %H:%M:%S")
                # rtc_time = rtc_time.timetuple()
                # eventTime = (rtc_time[3]*60*60) +(rtc_time[4]*60) +(rtc_time[5])
                eventTime = currentTime
                timez = "%02d-%02d-%02d"%(eventTime[3],eventTime[4],eventTime[5])
            else:
                #Error with reading RTC or HW clock
                if count2 == 0:
                    for name in os.listdir('/media/usb/'):
                        if name[:8] == 'noclock_':
                            count3 = int(name[8:])
                            if count3 > count2:
                                count2 = count3
                if eventTime-startTime >= 60*10:
                    count2 += 1
                    dirName = 'noclock_'+str(count2)
                    fullDN = '/media/usb/'+dirName
                    os.mkdir(fullDN)
                    startTime = time.time()
                timez = "0"
                time.sleep(1)
            GPIO.output(speaker, True)
            time.sleep(0.1)
            GPIO.output(speaker,False)

            if mode == 1:
                image,fpa,aux = capture(flip_v=False, device = "/dev/spidev0.1")
                cv2.imwrite(fullDN+'/image_thermal_%s_%09d.png'%(timez,count),image)
                #Capture and save from the rgb camera
                camera.capture(fullDN+'/image_rgb_%s_%09d.jpg'%(timez,count))#,quality=10)
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

    #If USB is no longer mounted it is out of storage.
    #TODO: Make more robust, the usb check assumes it is mounted as sda or sda1
    raise TypeError('Out of USB Storage')
    focalPlane = numpy.ones((1))*1.0
    fpa = focalPlane*fpa
    auxTemp = numpy.ones((1))*1.0
    aux = auxTemp*aux
    p = (fullDN+'/fpa_%s_%09d.txt'%(timez,count))
    a = (fullDN+'/aux_%s_%09d.txt'%(timez,count))
    numpy.savetxt(p,fpa)
    numpy.savetxt(a,aux)
    print'Elapsed time='+ str(eventTime - startTime) + '[s]'
    print ' '

except Exception as e:
    error = open('/media/usb/error.txt','w')
    error.write(str(e))
    error.close()
    print sys.exc_info()
    GPIO.output(yelLED, False)
    errorTime = time.time()

    #Endless beep cycle on error.
    while True:
        GPIO.output(redLED,True)
        time.sleep(1)
        GPIO.output(speaker,True)
        GPIO.output(redLED,False)
        GPIO.output(speaker,False)
        time.sleep(0.3)
