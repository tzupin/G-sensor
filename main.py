#!/usr/bin/env python
#

import os
import struct
import sys,getopt
import time
import datetime
import random 
import MPU6050Read
import subprocess
import RPi.GPIO as GPIO
import threading
import numpy as np

sensitive4g = 0x1c

#=========================================================================
# button control
GPIO.setmode(GPIO.BCM)
GPIO.setup(4,GPIO.IN,pull_up_down=GPIO.PUD_UP)

timeArray=[None]*100000000
#/*=========================================================================*/




# Main Program
def main(argv):
    try:
        opts,args=getopt.getopt(argv,"h:n:s:",["help=","deviceNumber"])
    except getopt.GetoptError:
        print 'usage:muti_accelerometer.py -n <deviceNumber> -s <subjectName>'
        sys.exit(2)
    '''
    if findElement(argv,'-n')==0:
        print 'usage:muti_accelerometer.py -n <deviceNumber> -s <subjectName>'
        sys.exit(2)
    if findElement(argv,'-s')==0:
        print 'usage:muti_accelerometer.py -n <deviceNumber> -s <subjectName>'
        sys.exit(2)
    '''
    for opt,arg in opts:
        if opts=='-h':
            print 'usage:muti_accelerometer.py -i <deviceNumber>'
        elif opt in ("-n","--deviceNumber"):
            deviceNum=arg
    	elif opt in ("-s","--subjectName"):
            subName=arg

    fileName=[subName+'_sensor1.txt',subName+'_sensor2.txt']
    count=0
    print ""
    print "Program Started at:"+ time.strftime("%Y-%m-%d %H:%M:%S")
    print ""

    starttime = datetime.datetime.utcnow()



    file0=open(fileName[0],'w')
    if int(deviceNum)==2:
        file1=open(fileName[1],'w')
    timeFile=open("dataTime.txt",'w')
    fileList=[file0,file1]
    accel_tmp=[0]*int(deviceNum)
    start=time.time()
    print "getting data please press button to stop........"
    while True:
        fileIndex=0
        input_state=GPIO.input(4)   #get switch state
        mpu6050 = MPU6050Read.MPU6050Read(0x68,1)
        #get gyro and accelerometer value
        gyro_xout = mpu6050.read_word_2c(0x43)
        gyro_yout = mpu6050.read_word_2c(0x45)
        gyro_zout = mpu6050.read_word_2c(0x47)
        accel_xout = mpu6050.read_word_2c(0x3b)
        accel_yout = mpu6050.read_word_2c(0x3d)
        accel_zout = mpu6050.read_word_2c(0x3f)
        accel_xout=accel_xout/16384.0
        accel_yout=accel_yout/16384.0
        accel_zout=accel_zout/16384.0
        gyro_xout=gyro_xout/131.0
        gyro_yout=gyro_yout/131.0
        gyro_zout=gyro_zout/131.0
        end=time.time()
        realtime=end-start
        fileList[fileIndex].write("%f\t%f\t%f\t%f\t%f\t%f\t%f\n" %(accel_xout,accel_yout,accel_zout,gyro_xout,gyro_yout,gyro_zout,realtime))
        #get slave sensor gyro and accelerometer value
        mpu6050_sla=MPU6050Read.MPU6050Read(0x69,1)
        gyro_xout = mpu6050_sla.read_word_2c(0x43)
        gyro_yout = mpu6050_sla.read_word_2c(0x45)
        gyro_zout = mpu6050_sla.read_word_2c(0x47)
        accel_xout = mpu6050_sla.read_word_2c(0x3b)
        accel_yout = mpu6050_sla.read_word_2c(0x3d)
        accel_zout = mpu6050_sla.read_word_2c(0x3f)
        accel_xout=accel_xout/16384.0
        accel_yout=accel_yout/16384.0
        accel_zout=accel_zout/16384.0
        gyro_xout=gyro_xout/131.0
        gyro_yout=gyro_yout/131.0
        gyro_zout=gyro_zout/131.0
        end=time.time()
        realtime=end-start
        fileList[fileIndex+1].write("%f\t%f\t%f\t%f\t%f\t%f\t%f\n" %(accel_xout,accel_yout,accel_zout,gyro_xout,gyro_yout,gyro_zout,realtime))
        count+=1
        if input_state==False:
            ttime=time.time()-start
            print "Button Pressed experimental stop"
            print "Total time : %f" %ttime
            print "Amount of data = %d" %count
            sys.exit()
            break 




if __name__=="__main__":
    sub_name=None
    main(sys.argv[1:])



