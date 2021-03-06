import RPi.GPIO as GPIO
import time
import sys
import datetime
import threading
  
#***********************************VARIABLE DECLARATIONS***********************************

global slice_speed
slice_speed = 25 # Initial DC speed set to 1/4 of full speed
global slicing
slicing = False

#***************************************MOTOR SET UP****************************************

#DC slice motor set up
RPWM = 3
LPWM = 7

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(RPWM,GPIO.OUT)
GPIO.setup(LPWM,GPIO.OUT)
GPIO.output(RPWM, GPIO.LOW)
GPIO.output(LPWM,GPIO.LOW)

#******************************************SLICING******************************************

def sliceProgram():
    global slicing  #create global
    slicing = True

    # Create rpm for dc
    global dc
    global slice_speed
    dc = GPIO.PWM(RPWM, 50)
    dc.start(slice_speed)

def stopSlicing():
  global dc
  global slicing
  slicing = False
  # try to stop slicing
  try:
    dc.stop()
  except:
    pass
  
