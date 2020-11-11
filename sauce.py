
#***********************************VARIABLE DECLARATIONS***********************************

# Motor speed
global pump_speed
s1_speed = 25 # Sauce stepper motor 1 speed
s2_speed = 25 # Sauce stepper motor 2 speed
s3_speed = 25 # Sauce stepper motor 3 speed
s4_speed = 25 # Sauce stepper motor 4 speed

#***************************************MOTOR SET UP****************************************

# Sauce stepper motor set up (pumps)
S1_DIR = 36   # Direction GPIO Pin
S1_STEP = 38  # Step GPIO Pin
S2_DIR = 31   # Direction GPIO Pin
S2_STEP = 33  # Step GPIO Pin
S3_DIR = 29   # Direction GPIO Pin
S3_STEP = 27  # Step GPIO Pin
S4_DIR = 21   # Direction GPIO Pin
S4_STEP = 23  # Step GPIO Pin

GPIO.setmode(GPIO.BOARD)
GPIO.setup(S1_DIR, GPIO.OUT)
GPIO.setup(S1_STEP, GPIO.OUT)
GPIO.setup(S2_DIR, GPIO.OUT)
GPIO.setup(S2_STEP, GPIO.OUT)
GPIO.setup(S3_DIR, GPIO.OUT)
GPIO.setup(S3_STEP, GPIO.OUT)
GPIO.setup(S4_DIR, GPIO.OUT)
GPIO.setup(S4_STEP, GPIO.OUT)

#****************************************PIZZA SPIN*****************************************

#Functions for starting and stopping spin
def pumpProgram():
    global pumping  #create global
    pumping = True

    # Create new threads
    pump1 = threading.Thread(target=pumpFunc, args = (S1_STEP, s1_speed,))
    pump2 = threading.Thread(target=pumpFunc, args = (S2_STEP, s2_speed,))
    pump3 = threading.Thread(target=pumpFunc, args = (S3_STEP, s3_speed,))
    pump4 = threading.Thread(target=pumpFunc, args = (S4_STEP, s4_speed,))
    
    # Start new thread
    pump1.start()
    pump2.start()
    pump3.start()
    pump4.start()
    
def pumpFunc(motor_pin, speed):
  while pumping:
    if pumping == False:
      break
    else:
      delay = (100-speed)/40000
      GPIO.output(motor_pin, GPIO.HIGH)
      time.sleep(delay)
      GPIO.output(motor_pin, GPIO.LOW)
      time.sleep(delay)

def stopPumping():
  global pumping
  pumping = False
