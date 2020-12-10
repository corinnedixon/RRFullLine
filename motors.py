import RPi.GPIO as GPIO
import time
import sys
import datetime
import threading

#***********************************VARIABLE DECLARATIONS***********************************

#Rotation variables
CW = 1     # Clockwise Rotation
CCW = 0    # Counterclockwise Rotation

# Motor speeds
global spin_speed
spin_speed = 25 # Pizza spin motor speed (1/4 speed)
global move_speed
move_speed = 25 # Horizontal motion speed (1/4 speed)

#***************************************MOTOR SET UP****************************************

# Big stepper motor set up (spins)
T6_DIR = 13   # Direction GPIO Pin
T6_STEP = 15  # Step GPIO Pin

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(T6_DIR, GPIO.OUT)
GPIO.setup(T6_STEP, GPIO.OUT)

# Small stepper motor set up (moves)
T7_DIR = 24   # Direction GPIO Pin
T7_STEP = 26  # Step GPIO Pin

GPIO.setup(T7_DIR, GPIO.OUT)
GPIO.setup(T7_STEP, GPIO.OUT)

#****************************************PIZZA SPIN*****************************************

#Functions for starting and stopping spin
def spinProgram(speed):
    # Create new thread
    spin = threading.Thread(target=spinFunc, args=(speed,1,))
    # Start new thread
    spin.start()

def spinFunc(speed, steps):
  global spinning
  spinning = True
  spin_delay = (100-speed)/50000
  while spinning and steps > 0:
    if spinning == False:
      break
    else:
      GPIO.output(T6_STEP, GPIO.HIGH)
      time.sleep(spin_delay)
      GPIO.output(T6_STEP, GPIO.LOW)
      time.sleep(spin_delay)
      steps = steps - 1

def stopSpinning():
  global spinning
  spinning = False
  GPIO.output(T6_STEP, GPIO.LOW)

#**************************************PIZZA MOVEMENT***************************************
#Functions for moving motor in and out
def inFunc(slope, const, steps):
  global movingIn
  movingIn = True
  GPIO.output(T7_DIR, CCW)
  count = 0
  while movingIn and count > steps:
    move_delay = slope*count+const
    if movingIn == False:
      break
    else:
    
      GPIO.output(T7_STEP, GPIO.HIGH)
      time.sleep(move_delay)
      GPIO.output(T7_STEP, GPIO.LOW)
      time.sleep(move_delay)
      count = count + 1

def outFunc(speed, steps):
  global movingOut
  movingOut = True
  move_delay = (100-speed)/1000000
  GPIO.output(T7_DIR, CW)
  while movingOut and steps > 0:
    if movingOut == False:
      break
    else:
      GPIO.output(T7_STEP, GPIO.HIGH)
      time.sleep(move_delay)
      GPIO.output(T7_STEP, GPIO.LOW)
      time.sleep(move_delay)
      steps = steps - 1

def stopMoving():
  global movingIn
  global movingOut
  movingIn = False
  movingOut = False
  GPIO.output(T7_STEP, GPIO.LOW)
  
#**************************************STOP EVERYTHING**************************************
def stopAll():
  #All variables False
  global movingIn
  global movingOut
  movingIn = False
  movingOut = False
  global spinning
  spinning = False
  GPIO.output(T6_STEP, GPIO.LOW)
  GPIO.output(T7_STEP, GPIO.LOW)
  
