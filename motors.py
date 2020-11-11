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
    global spinning  #create global
    spinning = True

    # Create new thread
    spin = threading.Thread(target=spinFunc, args=(speed,))
    # Start new thread
    spin.start()
    
def spinFunc(speed):
  while spinning:
    if spinning == False:
      break
    else:
      spin_delay = (100-speed)/50000
      GPIO.output(T6_STEP, GPIO.HIGH)
      time.sleep(spin_delay)
      GPIO.output(T6_STEP, GPIO.LOW)
      time.sleep(spin_delay)

def stopSpinning():
  global spinning
  spinning = False

#**************************************PIZZA MOVEMENT***************************************
#Functions for moving motor in and out
def inProgram(speed):
    global movingIn  #create global
    movingIn = True
    global movingOut
    movingOut = False

    # Create new thread
    moveIn = threading.Thread(target=inFunc, args=(speed,))
    # Start new thread
    moveIn.start()
    
def inFunc(speed):
  while movingIn:
    if movingIn == False:
      break
    else:
      move_delay = (100-speed)/1000000
      GPIO.output(T7_DIR, CCW)
      GPIO.output(T7_STEP, GPIO.HIGH)
      time.sleep(move_delay)
      GPIO.output(T7_STEP, GPIO.LOW)
      time.sleep(move_delay)

def outProgram(speed):
    global movingOut  #create global
    movingOut = True
    global movingIn
    movingIn = False

    # Create new thread
    moveOut = threading.Thread(target=outFunc, args=(speed,))
    # Start new thread
    moveOut.start()
    
def outFunc(speed):
  while movingOut:
    if movingOut == False:
      break
    else:
      move_delay = (100-speed)/1000000
      GPIO.output(T7_DIR, CW)
      GPIO.output(T7_STEP, GPIO.HIGH)
      time.sleep(move_delay)
      GPIO.output(T7_STEP, GPIO.LOW)
      time.sleep(move_delay)

def stopMoving():
  global movingIn
  global movingOut
  movingIn = False
  movingOut = False
  
#**************************************STOP EVERYTHING**************************************
def stopAll():
  #All variables False
  global slicing
  slicing = False
  global movingIn
  global movingOut
  movingIn = False
  movingOut = False
  global spinning
  spinning = False
  #All motors stop
  try:
    stopSpinning()
  except:
    pass
  try:
    stopMoving()
  except:
    pass
  
