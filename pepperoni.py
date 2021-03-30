import RPi.GPIO as GPIO
import time
import sys
import datetime
import threading
  
#***********************************VARIABLE DECLARATIONS***********************************

global slice_speed
slice_speed = 25 # Initial DC speed set to 1/4 of full speed

#***************************************MOTOR SET UP****************************************

#DC slice motor set up
DM860T_DIR = 35
DM860T_CLK = 37

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(DM860T_DIR,GPIO.OUT)
GPIO.setup(LPWMDM860T_CLKGPIO.OUT)
GPIO.output(DM860T_DIR, GPIO.LOW)
GPIO.output(DM860T_CLK,GPIO.LOW)

#***************************************SWITCH FUNCS****************************************

#mag sensor callback
def sensorCallback(channel):
  # Called if sensor output changes
  timestamp = time.time()
  stamp = datetime.datetime.fromtimestamp(timestamp).strftime('%H:%M:%S')
  if GPIO.input(channel):
    # No magnet
    #print("Sensor HIGH " + stamp)
    return 0
  else:
    # Magnet
    #print("Sensor LOW " + stamp)
    return 1
    
#switch sensor callback
def switchCallback(channel):
  # Called if sensor output changes
  if GPIO.input(channel):
    return 0
  else:
    print("PRESSED")
    return 1

#****************************************PEP CLASS******************************************

class pep:
    def init(freq=100,pin=37):
        global bladeclk
        global oldfreq
        oldfreq=freq
        bladeclk=GPIO.PWM(pin,freq)
        bladeclk.start(0)
    
    def turn(newfreq):
        if newfreq<1:
            newfreq=1
        global oldfreq
        global bladeclk
        bladeclk.ChangeDutyCycle(50)
        for i in range(oldfreq,newfreq,10*(2*(newfreq>oldfreq)-1)):
            bladeclk.ChangeFrequency(i)
            time.sleep(.03)
        oldfreq=newfreq
            
    def stop():
        pep.turn(100)
        bladeclk.ChangeDutyCycle(0)

    def sw():
        pep.stop()
        if GPIO.input(16)==0:
            GPIO.output(16,GPIO.HIGH)
        else:
            GPIO.output(16,GPIO.LOW)
        
#********************************FUNCTIONS FOR OUTSIDE USE**********************************

def setBladeFrequency(freq):
    global bladeclk
    bladeclk.ChangeFrequency(freq)

def setBladeDutyCycle(dc):
    global bladeclk
    bladeclk.ChangeDutyCycle(dc)

def cut(bladefreq=1400,tablefreq=200):
    motors.spinProgram(tablefreq)
    pep.turn(bladefreq)

def sliceProgram():
    cut()

def stopSlicing():
  global slicing
  slicing = False
  # try to stop slicing
  try:
    pep.stop()
  except:
    pass
  
