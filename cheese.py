import RPi.GPIO as GPIO
import time
import sys
import datetime
import threading

#***********************************VARIABLE DECLARATIONS***********************************

global cheese_speed
cheese_speed = 25 # Initial cheese speed set to 1/4 of full potential
global cheesing
cheesing = False

global shake_speed
slice_speed = 25 # Initial DC speed set to 1/4 of full speed
global shaking
shaking = False

#***************************************MOTOR SET UP****************************************

# Cheese stepper motor set up
C5_DIR = 35   # Direction GPIO Pin
C5_STEP = 37  # Step GPIO Pin

# DC shaker motor set up
C8_RPWM = 0 #FIX
C8_LPWM = 0 #FIX

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(C5_DIR, GPIO.OUT)
GPIO.setup(C5_STEP, GPIO.OUT)
GPIO.setup(C8_RPWM, GPIO.OUT)
GPIO.setup(C8_LPWM, GPIO.OUT)

#*****************************************CHEESING******************************************

# Functions for cheese dispensing
def cheeseProgram():
    global cheesing  #create global
    cheesing = True

    # Create new thread
    cheese = threading.Thread(target=cheeseFunc)
    # Start new thread
    cheese.start()
    
def cheeseFunc():
  cheese_delay = (100-cheese_speed)/50000
  while cheesing:
    if cheesing == False:
      break
    else:
      GPIO.output(C5_STEP, GPIO.HIGH)
      time.sleep(cheese_delay)
      GPIO.output(C5_STEP, GPIO.LOW)
      time.sleep(cheese_delay)

def stopCheesing():
  global cheesing
  cheesing = False
  GPIO.output(C5_STEP, GPIO.LOW)

# Functions for DC motor to shake
def shakeProgram():
    global shaking  #create global
    shaking = True

    # Create rpm for dc
    global shaker
    global shake_speed
    shaker = GPIO.PWM(C8_RPWM, 50)
    shaker.start(slice_speed)

def stopShaking():
  global shaker
  global shaking
  shaking = False
  try:
    shaker.stop()
  except:
    pass
