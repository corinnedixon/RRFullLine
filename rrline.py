from tkinter import *
import tkinter.font as font
import time
import RPi.GPIO as GPIO
import pepperoni
import motors
import cheese
import sauce

#***********************************VARIABLE DECLARATIONS***********************************

# Run times for each step of pizza process (in seconds)
global initial_move
initial_move = 1 # Time for movement of pizza after size/mode are set
global sauce_time
sauce_time = 3 # Time for sauce / spin
global to_cheese
to_cheese = 1 # Time of movement for pizza to cheeser
global cheese_time
cheese_time = 2 # Amount of time for putting cheese on pizza
global pepp_time
pepp_time = 2 # Amount of time for putting pepperoni on pizza
global end_pepp
end_pepp = 1 # Amount of time from pepperoni to end
global end_cheese
end_cheese = 3 # Amount of time from cheese to end
global to_beginning
to_beginning = 3 # Amount of time from end to start

# Mode / Size
global mode
mode = 0 # Default mode is 0 for cheese
global size
size = 14 # Default size is 14 inch

# Run line
global running
running = False

#Raspberry Pi set up
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

#*************************************BUTTON FUNCTIONS**************************************

def setMode(new_mode):
    global mode
    mode = new_mode
    runLine()

def setSize(new_size):
    global size
    size = new_size
    
def reset():
    motors.outProgram(30)
    time.sleep(to_beginning)
    motors.stopMoving()

def stop():
    pepperoni.stopSlicing()
    motors.stopAll()
    cheese.stopCheesing()
    sauce.stopPumping()
        
#************************************FULL LINE FUNCTION*************************************

def runLine():
    # Move horizontally to sauce
    motors.inProgram(25)
    time.sleep(initial_move)
    motors.stopMoving()
    
    # Run corresponding saucer pumps
    sauce.pumpProgram()
    motors.spinProgram(25)
    time.sleep(sauce_time)
    sauce.stopPumping()
    motors.stopSpinning()
    
    # Move horizontally to cheese
    motors.inProgram(25)
    time.sleep(to_cheese)
    motors.stopMoving()
    
    # Cheese the pizza
    cheese.cheeseProgram()
    motors.spinProgram(25)
    motors.inProgram(10)
    time.sleep(cheese_time)
    sauce.stopPumping()
    motors.stopAll()
    
    # if pepp mode, pepp and move to end...otherwise, just go to end
    if(mode == 1):
        # pepp the pizza
        motors.spinProgram(25)
        motors.inProgram(10)
        pepperoni.sliceProgram()
        time.sleep(pepp_time)
        pepperoni.stopSlicing()
        motors.stopAll()
        
        # move to end
        motors.inProgram(25)
        time.sleep(end_pepp)
        motors.stopMoving()
    else:
        # just move to end
        motors.inProgram(25)
        time.sleep(end_cheese)
        motors.stopMoving()
    
#**************************************TKINTER SET UP***************************************

# TK screen set up
screen = Tk()
#screen.overrideredirect(1)
screen.geometry('800x480')
screen.title("Full Line")

# Fonts for screen
myFont = font.Font(family='Helvetica', size=36, weight='bold')
myFontLarge = font.Font(family='Helvetica', size=50, weight='bold')

# Size buttons
fourteenButton  = Button(screen, text = "14 in.", font = myFont, bg = "white", command = lambda: setSize(14), height = 2 , width = 4)
fourteenButton.place(x=575, y=5)

twelveButton  = Button(screen, text = "12 in.", font = myFont, bg = "white", command = lambda: setSize(12), height = 2 , width = 4)
twelveButton.place(x=400, y=5)

tenButton  = Button(screen, text = "10 in.", font = myFont, bg = "white", command = lambda: setSize(10), height = 2 , width = 4)
tenButton.place(x=225, y=5)

sevenButton  = Button(screen, text = "7 in.", font = myFont, bg = "white", command = lambda: setSize(7), height = 2 , width = 4)
sevenButton.place(x=50, y=5)

# Type buttons
cheeseButton  = Button(screen, text = "Cheese", font = myFont, bg = "lightgrey", command = lambda: setMode(0), height = 1, width = 6)
cheeseButton.place(x=100, y=135)

peppButton  = Button(screen, text = "Pepp", font = myFont, bg = "lightgrey", command = lambda: setMode(1), height = 1, width = 6)
peppButton.place(x=450, y=135)

# Function buttons
resetButton  = Button(screen, text = "RESET", font = myFontLarge, bg = "lightgreen", command = reset, height = 2 , width = 6)
resetButton.place(x=100, y=210)

stopButton  = Button(screen, text = "STOP", font = myFontLarge, bg = "red", command = stop, height = 2 , width = 6)
stopButton.place(x=450, y=210)

mainloop()
