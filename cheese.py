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

#***************************************MOTOR SET UP****************************************

# Cheese stepper motor set up
C5_DIR = 11   # Direction GPIO Pin
C5_STEP = 35  # Step GPIO Pin

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(C5_DIR, GPIO.OUT)
GPIO.setup(C5_STEP, GPIO.OUT)

#*****************************************CHEESING******************************************

def cheeseProgram():
    global cheesing  #create global
    cheesing = True

    # Create new thread
    cheese = threading.Thread(target=cheeseFunc)
    # Start new thread
    cheese.start()
    
def cheeseFunc():
  while cheesing:
    if cheesing == False:
      break
    else:
      cheese_delay = (100-cheese_speed)/50000
      GPIO.output(C5_STEP, GPIO.HIGH)
      time.sleep(cheese_delay)
      GPIO.output(C5_STEP, GPIO.LOW)
      time.sleep(cheese_delay)

def stopCheesing():
  global cheesing
  cheesing = False
