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
global initial_steps
initial_steps = 100 # Steps for movement of pizza after size/mode are set
global sauce_spin_steps
sauce_spin_steps = 300 # Steps that pizza spins for sauce stage

global to_cheese
to_cheese = 100 # Steps for movement of pizza to cheeser
global cheese_spin_steps
cheese_spin_steps = 100 # Steps for spinning of pizza during cheese
global cheese_steps
cheese_steps = 200 # Amount of steps for putting cheese on pizza

global pepp_steps
pepp_steps = 200 # Amount of steps for putting pepperoni on pizza
global pepp_spin_steps
pepp_spin_steps = 100 # Steps for spinning of pizza during pepperoni
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

#**************************************SETTINGS WINDOW**************************************

def settings(screen):
    # Create window for settings
    top = Toplevel()
    top.title("Full Line Settings")
    top.geometry('800x480')
    screen.overrideredirect(0)
    top.overrideredirect(1)
    
    # Font
    subFont = font.Font(family='Helvetica', size=30, weight='normal')
    
    # Action buttons
    quit  = Button(top, text = "Quit", font = subFont, fg="black", bg = "white", command = screen.destroy, height = 2, width = 6)
    quit.place(x=100, y=350)
    back  = Button(top, text = "Back", font = subFont, fg="black", bg = "white", command = top.destroy, height = 2, width = 6)
    back.place(x=550, y=350)

#*****************************************HELP MENU*****************************************

# Function for changing button text based on answer
def change(button):
    if button['text'] == "NO":
        button['text'] = "YES"
    else:
        button['text'] = "NO"

# Function for sending sos menu data to Firebase
def send(answers):
    str = "Answers:"
    for button in answers:
        str = str + " " + button['text']
    if(hasInternet):
      db.push(str)
    print(str)
    print("Sending data to Firebase")

# Function for sos menu
def sos(top):
    # Create window for help menu
    sosMenu = Toplevel()
    sosMenu.title("Saucer Help Menu")
    sosMenu.geometry('800x480')
    sosMenu.overrideredirect(1)
    
    # Fonts
    subFont = font.Font(family='Helvetica', size=30, weight='normal')
    questionFont = font.Font(family='Helvetica', size=14, weight='normal')
    
    # Questions
    q1 = Text(sosMenu, font=questionFont, height=1, width=35)
    q1.insert(INSERT, "Is it making the 14 Inch Pizza?")
    q1.place(x=25, y=20)
    
    b1  = Button(sosMenu, text = "NO", font = questionFont, fg="black", bg = "white", command = lambda: change(b1), height = 1, width = 2)
    b1.place(x=400, y=20)
    
    q2 = Text(sosMenu, font=questionFont, height=1, width=35)
    q2.insert(INSERT, "Is it making the 12 Inch Pizza?")
    q2.place(x=25, y=50)
    
    b2  = Button(sosMenu, text = "NO", font = questionFont, fg="black", bg = "white", command = lambda: change(b2), height = 1, width = 2)
    b2.place(x=400, y=50)
    
    q3 = Text(sosMenu, font=questionFont, height=1, width=35)
    q3.insert(INSERT, "Is it making the 10 Inch Pizza?")
    q3.place(x=25, y=80)
    
    b3 = Button(sosMenu, text = "NO", font = questionFont, fg="black", bg = "white", command = lambda: change(b3), height = 1, width = 2)
    b3.place(x=400, y=80)
    
    q4 = Text(sosMenu, font=questionFont, height=1, width=35)
    q4.insert(INSERT, "Is it making the 7 Inch Pizza?")
    q4.place(x=25, y=110)
    
    b4  = Button(sosMenu, text = "NO", font = questionFont, fg="black", bg = "white", command = lambda: change(b4), height = 1, width = 2)
    b4.place(x=400, y=110)
    
    q5 = Text(sosMenu, font=questionFont, height=1, width=35)
    q5.insert(INSERT, "Do sauce intake tubes have air bubbles?")
    q5.place(x=25, y=140)
    
    b5  = Button(sosMenu, text = "NO", font = questionFont, fg="black", bg = "white", command = lambda: change(b5), height = 1, width = 2)
    b5.place(x=400, y=140)
    
    q6 = Text(sosMenu, font=questionFont, height=1, width=35)
    q6.insert(INSERT, "Is the turntable motor shaft spinning?")
    q6.place(x=25, y=170)
    
    b6  = Button(sosMenu, text = "NO", font = questionFont, fg="black", bg = "white", command = lambda: change(b6), height = 1, width = 2)
    b6.place(x=400, y=170)
    
    q7 = Text(sosMenu, font=questionFont, height=1, width=35)
    q7.insert(INSERT, "Is the pizza moving across the line?")
    q7.place(x=25, y=200)
    
    b7  = Button(sosMenu, text = "NO", font = questionFont, fg="black", bg = "white", command = lambda: change(b7), height = 1, width = 2)
    b7.place(x=400, y=200)
    
    q8 = Text(sosMenu, font=questionFont, height=1, width=35)
    q8.insert(INSERT, "Is cheese being dispensed?")
    q8.place(x=25, y=230)
    
    b8  = Button(sosMenu, text = "NO", font = questionFont, fg="black", bg = "white", command = lambda: change(b8), height = 1, width = 2)
    b8.place(x=400, y=230)
    
    q9 = Text(sosMenu, font=questionFont, height=1, width=35)
    q9.insert(INSERT, "Is the pepperoni slicing?")
    q9.place(x=25, y=260)
    
    b9  = Button(sosMenu, text = "NO", font = questionFont, fg="black", bg = "white", command = lambda: change(b9), height = 1, width = 2)
    b9.place(x=400, y=260)
    
    q10 = Text(sosMenu, font=questionFont, height=1, width=35)
    q10.insert(INSERT, "Is the screen functioning properly?")
    q10.place(x=25, y=290)
    
    b10  = Button(sosMenu, text = "NO", font = questionFont, fg="black", bg = "white", command = lambda: change(b10), height = 1, width = 2)
    b10.place(x=400, y=290)
    
    q11 = Text(sosMenu, font=questionFont, height=1, width=35)
    q11.insert(INSERT, "Can you hear any grinding noise?")
    q11.place(x=25, y=320)
    
    b11  = Button(sosMenu, text = "NO", font = questionFont, fg="black", bg = "white", command = lambda: change(b11), height = 1, width = 2)
    b11.place(x=400, y=320)
    
    q12 = Text(sosMenu, font=questionFont, height=1, width=35)
    q12.insert(INSERT, "Can you hear any high pitched noise?")
    q12.place(x=25, y=350)
    
    b12  = Button(sosMenu, text = "NO", font = questionFont, fg="black", bg = "white", command = lambda: change(b12), height = 1, width = 2)
    b12.place(x=400, y=350)
    
    q13 = Text(sosMenu, font=questionFont, height=1, width=35)
    q13.insert(INSERT, "Did this problem just start?")
    q13.place(x=25, y=380)
    
    b13  = Button(sosMenu, text = "NO", font = questionFont, fg="black", bg = "white", command = lambda: change(b13), height = 1, width = 2)
    b13.place(x=400, y=380)
    
    answers = [b1,b2,b3,b4,b5,b6,b7,b8,b9,b10,b11,b12,b13]
    
    # Back button
    done  = Button(sosMenu, text = "Done", font = subFont, fg="black", bg = "white", command = lambda: send(answers), height = 2, width = 4)
    done.place(x=500, y=350)
    quit  = Button(sosMenu, text = "Quit", font = subFont, fg="black", bg = "white", command = sosMenu.destroy, height = 2, width = 4)
    quit.place(x=650, y=350)

    print("SOS\n")

# Function for help menu
def help(screen):
    # Create window for help menu
    top = Toplevel()
    top.title("Full Line Help Menu")
    top.geometry('800x480')
    top.overrideredirect(1)
    
    # Font
    subFont = font.Font(family='Helvetica', size=30, weight='normal')
    
    # Text
    txt = Text(top, font = subFont, height=1, width=22)
    txt.insert(INSERT, "Welcome to the help menu!")
    txt.place(x=25,y=25)
    
    # Action buttons
    quit  = Button(top, text = "SOS", font = subFont, fg="black", bg = "white", command = lambda: sos(top), height = 2, width = 6)
    quit.place(x=100, y=350)
    back  = Button(top, text = "Back", font = subFont, fg="black", bg = "white", command = top.destroy, height = 2, width = 6)
    back.place(x=550, y=350)


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

    # Move horizontally to sauce (slope, initial delay, steps)
    motors.inFunc(0, 0.0025, initial_steps)
    
    # Run corresponding saucer pumps
    sauce.pumpProgram()
    motors.spinFunc(0.0001, 0.001, sauce_spin_steps)
    sauce.stopPumping()
    motors.stopSpinning()
    
    # Move horizontally to cheese (slope, initial delay, steps)
    motors.inFunc(0, 0.0025, to_cheese)
    
    # Cheese the pizza
    cheese.cheeseProgram()
    motors.spinProgram(0.0001, 0.001, cheese_spin_steps)
    motors.inFunc(0.0001, 0.001, cheese_steps)
    cheese.stopCheesing()
    motors.stopAll()
    
    # if pepp mode, pepp and move to end...otherwise, just go to end
    if(mode == 1):
        # pepp the pizza
        motors.spinProgram(0.0001, 0.001, pepp_spin_steps)
        pepperoni.sliceProgram()
        motors.inFunc(0.0001, 0.001, pepp_steps)
        pepperoni.stopSlicing()
        motors.stopAll()
        
        # move to end (slope, initial delay, steps)
        motors.inFunc(0, 0.0025, end_pepp)
    else:
        # just move to end (slope, initial delay, steps)
        motors.inFunc(0, 0.0025, end_cheese)
    
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
settingsButton  = Button(screen, text = "Settings", font = myFont, bg = "grey", command = lambda: settings(screen), height = 1, width = 6)
settingsButton.place(x=50, y=380)

helpButton  = Button(screen, text = "Help", font = myFont, bg = "grey", command = lambda: help(screen), height = 1, width = 6)
helpButton.place(x=500, y=380)

mainloop()
