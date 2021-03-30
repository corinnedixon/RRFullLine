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
T6_DIR = 10   # Direction GPIO Pin
T6_STEP = 8  # Step GPIO Pin

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(T6_DIR, GPIO.OUT)
GPIO.setup(T6_STEP, GPIO.OUT)

# Small stepper motor set up (moves)
T7_DIR = 13   # Direction GPIO Pin
T7_STEP = 15  # Step GPIO Pin

GPIO.setup(T7_DIR, GPIO.OUT)
GPIO.setup(T7_STEP, GPIO.OUT)

#****************************************TABLE CLASS****************************************

class table:
    def init(pin1=8,pin2=15):
        global turnclk
        turnclk=GPIO.PWM(pin1,500)
        turnclk.start(0)
        global tranclk
        tranclk=GPIO.PWM(pin2,1000)
        tranclk.start(0)
        
    def move(dist,freq=2000,pin3=13):
        global REV

        REV = 0 #Revolution Count
        VAl = 0 #Currrent mag value
        TEMP = 0 #Previous mag value
        PRESS = 0 #switch value
        
        trandir=dist<0
        GPIO.output(pin3,trandir)
        global tranclk
        tranclk.ChangeFrequency(freq)
        tranclk.ChangeDutyCycle(50)
        for i in range(abs(dist)):
            PRESS = switchCallback(40)
            if PRESS == 1:
                break
            time.sleep(0.05)
            VAL = sensorCallback(11)

            if TEMP == 0 and VAL == 1:
                REV = REV + 1
                TEMP = 1
                print('Rvolution count: ')
                print(REV)
            else:
                TEMP = 0

        tranclk.ChangeDutyCycle(0)
        
    def turn(freq):
        global turnclk
        if freq==0:
            turnclk.ChangeDutyCycle(0)
        else:
            turnclk.ChangeDutyCycle(50)
            turnclk.ChangeFrequency(freq)
            
    def home(freq=2000):
        global tranclk
        GPIO.output(13,GPIO.HIGH)
        tranclk.ChangeDutyCycle(50)
        while GPIO.event_detected(11)==0:
            time.sleep(0.01)
        print('nice')
        tranclk.ChangeDutyCycle(0)
        
    def stopSpin():
        global turnclk
        turnclk.ChangeDutyCycle(0)
        
    def stopMove():
        global tranclk
        tranclk.ChangeDutyCycle(0)

#****************************************PIZZA SPIN*****************************************

#Functions for variable manipulation
def setSpinFrequency(freq):
    global turnclk
    turnclk.ChangeFrequency(freq)

def setSpinDutyCycle(dc):
    global turnclk
    turnclk.ChangeDutyCycle(dc)

#Functions for starting and stopping spin
def spinProgram(speed):
    # Start spinning
    table.turn(speed)

def stopSpinning():
    table.stopSpin()

#**************************************PIZZA MOVEMENT***************************************

#Functions for variable manipulation
def setMoveFrequency(freq):
    global tranclk
    tranclk.ChangeFrequency(freq)

def setMoveDutyCycle(dc):
    global tranclk
    tranclk.ChangeDutyCycle(dc)

#Functions for moving motor in and out
def goHome():
    table.home()

def moveProgram(distance):
  table.move(distance)

def stopMoving():
    table.stopMove()
  
#**************************************STOP EVERYTHING**************************************

def stopAll():
  stopSpinning()
  stopMoving()
