from tkinter import *
import tkinter.font as font
import time
import RPi.GPIO as GPIO
import pepperoni
import motors
import cheese
import sauce
import screens

#***********************************VARIABLE DECLARATIONS***********************************

# Run times for each step of pizza process (in seconds)
global initial_steps
initial_steps = 100 # Steps for movement of pizza after size/mode are set
global sauce_spin_steps
sauce_spin_steps = 300 # Steps that pizza spins for sauce stage
global to_cheese
to_cheese = 100 # Steps for movement of pizza to cheeser
global cheese_steps
cheese_steps = 200 # Amount of steps for putting cheese on pizza
global pepp_steps
pepp_steps = 200 # Amount of steps for putting pepperoni on pizza
global end_pepp
end_pepp = 100 # Steps from pepperoni to end
global end_cheese
end_cheese = 300 # Steps from cheese to end
global to_beginning
to_beginning = 300 # Steps from end to start

# Mode / Size
global mode
mode = -1 # No default mode
global size
size = 14 # Default size is 14 inch

# Double click
global click
click = 0

#Raspberry Pi set up
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

#*************************************BUTTON FUNCTIONS**************************************

def setMode(new_mode):
    global click
    global mode
    if mode == new_mode:
        click = click + 1
    else:
        click = 0
        mode = new_mode
    
    if click == 1:
        click = 0
        runLine()

def setSize(new_size):
    global click
    global size
    click = 0
    size = new_size
    
def reset():
    motors.outFunc(30, to_beginning)
    motors.stopMoving()

def stop():
    pepperoni.stopSlicing()
    motors.stopAll()
    cheese.stopCheesing()
    sauce.stopPumping()
        
#************************************FULL LINE FUNCTION*************************************

def runLine():
    print("RUNNING LINE\n")

    # Move horizontally to sauce
    motors.inFunc(25, initial_steps)
    
    # Run corresponding saucer pumps
    sauce.pumpProgram()
    motors.spinFunc(25, sauce_spin_steps)
    sauce.stopPumping()
    motors.stopSpinning()
    
    # Move horizontally to cheese
    motors.inFunc(25, to_cheese)
    
    # Cheese the pizza
    cheese.cheeseProgram()
    motors.spinProgram(25)
    motors.inFunc(10, cheese_steps)
    cheese.stopCheesing()
    motors.stopAll()
    
    # if pepp mode, pepp and move to end...otherwise, just go to end
    if(mode == 1):
        # pepp the pizza
        motors.spinProgram(25)
        pepperoni.sliceProgram()
        motors.inFunc(10, pepp_steps)
        pepperoni.stopSlicing()
        motors.stopAll()
        
        # move to end
        motors.inFunc(25, end_pepp)
    else:
        # just move to end
        motors.inFunc(25, end_cheese)
    
#**************************************TKINTER SET UP***************************************

# TK screen set up
screen = Tk()
screen.overrideredirect(1)
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
resetButton  = Button(screen, text = "RESET", font = myFontLarge, bg = "lightgreen", command = reset, height = 2, width = 6)
resetButton.place(x=100, y=210)

stopButton  = Button(screen, text = "STOP", font = myFontLarge, bg = "red", command = stop, height = 2, width = 6)
stopButton.place(x=450, y=210)

# Other screen buttons
settingsButton  = Button(screen, text = "Settings", font = myFont, bg = "grey", command = lambda: screens.settings(screen), height = 1, width = 4)
settingsButton.place(x=50, y=300)

helpButton  = Button(screen, text = "Help", font = myFont, bg = "grey", command = lambda: screens.help(screen), height = 1, width = 4)
helpButton.place(x=500, y=300)

mainloop()
