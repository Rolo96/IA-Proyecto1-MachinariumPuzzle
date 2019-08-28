##########################################
#       Tecnologico de Costa Rica        #
#        Inteligencia Artificial         #
#               Proyecto 1               #
#               Raul Arias               #
#            Victor CHavarría            #
#            Gabriel Espinoza            #
#            Esteban Sanabria            #               
##########################################

#-----------------Imports ----------------
import tkinter as tk
import random


#---------------Globals-------------------

#Constants
DOWN_ARROW_IMAGE_NAME = "down.png"
UP_ARROW_IMAGE_NAME = "up.png"
PUZZLE_IMAGE_NAME = "puzzle.png"
MOVE_DOWN = 0
JUMP_DOWN = 1
MOVE_UP = 2
JUMP_UP = 3
MAX_ITERATIONS = 100

#States
InitialState = [-1,-1,-1,0,1,1,1,0,0,0]
EndState = [1,1,1,0,-1,-1,-1]
OpenStates = [[]]
ClosedStates = [[]]
Moves = []
Arrows = []

#Initial assigns
OpenStates.append(InitialState)
step = 1
newStates = 0

#---------------Functions-------------------

def moveDown():
    """
    Move down transition, evaluates if the movement is posible if so executes it
    """
    global OpenStates, newStates
    position = 0
    
    while position < 7:
        value = ActualState[position]
        # if is down arrow and there is a space below and the space is empty so can move
        if (value < 0 and position + 1 < 7 and ActualState[position+1] == 0):
            #Calc new state
            temporalState = ActualState[:]
            temporalState[position] = 0
            temporalState[position+1] = -1
            temporalState[7] = step
            temporalState[8] = MOVE_DOWN
            temporalState[9] = position

            #Check if new state is not in closed states
            exists = False
            for x in ClosedStates:
                if x == temporalState:
                    exists = True
            #If state was not in closed states add it to open states
            if exists == False:
                    OpenStates.append(temporalState)
                    newStates = newStates + 1
        position = position + 1
    return newStates

def jumpDown():
    """
    Jump down transition, evaluates if the movement is posible if so executes it
    """
    global OpenStates, newStates
    position = 0
    
    while position < 7:
        value = ActualState[position]
        # if is down arrow and there is two spaces below and the next space is up arrow and the next space is empty so can move
        if (value < 0 and position + 2 < 7 and ActualState[position+2] == 0 and ActualState[position+1] == 1):
            #Calc new state
            temporalState = ActualState[:]
            temporalState[position] = 0
            temporalState[position+2] = -1
            temporalState[7] = step
            temporalState[8] = JUMP_DOWN
            temporalState[9] = position

            #Check if new state is not in closed states
            exists = False
            for x in ClosedStates:
                if x == temporalState:
                    exists = True
            #If state was not in closed states add it to open states
            if exists == False:
                    OpenStates.append(temporalState)
                    newStates = newStates + 1
        position = position + 1  
    return newStates

def moveUp():
    """
    Move up transition, evaluates if the movement is posible if so executes it
    """
    global OpenStates, newStates
    position = 0
    
    while position < 7:
        value = ActualState[position]
        # if is u[ arrow and there is a space above and the space is empty so can move
        if (value > 0 and position - 1 >= 0 and ActualState[position-1] == 0):
            #Calc new state
            temporalState = ActualState[:]
            temporalState[position] = 0
            temporalState[position-1] = 1
            temporalState[7] = step
            temporalState[8] = MOVE_UP
            temporalState[9] = position

            #Check if new state is not in closed states
            exists = False
            for x in ClosedStates:
                if x == temporalState:
                    exists = True
            #If state was not in closed states add it to open states
            if exists == False:
                    OpenStates.append(temporalState)
                    newStates = newStates + 1
        position = position + 1  
    return newStates

def jumpUp():
    """
    Jump up transition, evaluates if the movement is posible if so executes it
    """
    global OpenStates, newStates
    position = 0
    
    while position < 7:
        value = ActualState[position]
        # if is down arrow and there is a space below and the space is empty so can move
        if (value > 0 and position - 2 >= 0  and ActualState[position-2] == 0 and ActualState[position-1] == -1):
            #Calc new state
            temporalState = ActualState[:]
            temporalState[position] = 0
            temporalState[position-2] = 1
            temporalState[7] = step
            temporalState[8] = JUMP_UP
            temporalState[9] = position

            #Check if new state is not in closed states
            exists = False
            for x in ClosedStates:
                if x == temporalState:
                    exists = True
            #If state was not in closed states add it to open states
            if exists == False:
                    OpenStates.append(temporalState)
                    newStates = newStates + 1
        position = position + 1  
    return newStates

def solvePuzzle():
    """
    Solve puzzle executing depth first search algoritm 
    """
    global step, newStates, ActualState, OpenStates, ClosedStates, Moves

    #First state
    ActualState = OpenStates.pop()
    #Try while max iterations
    for x in range(MAX_ITERATIONS):
        newStates = 0
        #Actual state is not end state so calc moves
        if ActualState[:7] != EndState[:]:
            moveDown()
            jumpDown()
            moveUp()
            jumpUp()

            #If there is not new states from this point
            if newStates == 0:
                nextStep = OpenStates[-1][7]
                while (len(Moves)>0):
                    if(Moves[-1][0] >= nextStep):
                       Moves.pop()
                    else:
                        break;
                ClosedStates.append(ActualState[:7])
                ActualState = OpenStates.pop()
                
            #Else use new state
            else:
                ClosedStates.append(ActualState[:7])
                Moves.append(ActualState[7:10])
                ActualState = OpenStates.pop()
        #Win
        else:
            Moves.append(ActualState[7:10])
            break;
        step = step + 1
        
#---------------GUI Functions-------------------

def nextStep():
    """
    Show next step in graphical interface
    """
    global actualStep

    #Get values
    movement = Moves[actualStep+1]
    move = movement[1]
    position = movement[2]

    #Updating arrows
    if move == MOVE_DOWN:
        canvas.move(Arrows[position], 0, 55)
        Arrows[position+1] = Arrows[position]
        Arrows[position] = None
    elif move == JUMP_DOWN:
        canvas.move(Arrows[position], 0, 105)
        Arrows[position+2] = Arrows[position]
        Arrows[position] = None
    elif move == MOVE_UP:
        canvas.move(Arrows[position], 0, -55)
        Arrows[position-1] = Arrows[position]
        Arrows[position] = None
    elif move == JUMP_UP:
        canvas.move(Arrows[position], 0, -105)
        Arrows[position-2] = Arrows[position]
        Arrows[position] = None

    #Updating step
    actualStep = actualStep + 1
    stepLabel.configure(text="Step: " + str(actualStep) + " of: " + totalStepStr)
    if actualStep >= totalStep:
        nextButton.configure(state=tk.DISABLED)
    else:
        previousButton.configure(state=tk.NORMAL)

def previousStep():
    """
    Show previous step in graphical interface
    """
    global actualStep

    #Get values
    movement = Moves[actualStep]
    move = movement[1]
    position = movement[2]

    #Updating arrows
    if move == MOVE_DOWN:
        canvas.move(Arrows[position+1], 0, -55)
        Arrows[position] = Arrows[position+1]
        Arrows[position+1] = None
    elif move == JUMP_DOWN:
        canvas.move(Arrows[position+2], 0, -105)
        Arrows[position] = Arrows[position+2]
        Arrows[position+2] = None
    elif move == MOVE_UP:
        canvas.move(Arrows[position-1], 0, 55)
        Arrows[position] = Arrows[position-1]
        Arrows[position-1] = None
    elif move == JUMP_UP:
        canvas.move(Arrows[position-2], 0, 105)
        Arrows[position] = Arrows[position-2]
        Arrows[position-2] = None

    #Updating step
    actualStep = actualStep - 1
    stepLabel.configure(text="Step: " + str(actualStep) + " of: " + totalStepStr)
    if actualStep <= 0:
        previousButton.configure(state=tk.DISABLED)
    else:
        nextButton.configure(state=tk.NORMAL)

#---------------Main-------------------
solvePuzzle()
actualStep = 0
totalStep = len(Moves)-1
totalStepStr = str(totalStep)

root = tk.Tk()
root.title("IA - Project #1")

#Creating the canvas
canvas = tk.Canvas(root, width=700, height=700)
canvas.pack()

#Creating the buttons and labels
Title = tk.Label(canvas, text = "Arrows puzzle")
Title.place(x=220, y=75)
Title.config(font=("Courier", 25))
stepLabel = tk.Label(canvas, text = "Step: " + str(actualStep) + " of: " + totalStepStr)
stepLabel.place(x=500, y=600)
stepLabel.config(font=("Courier", 15))
previousButton = tk.Button(canvas, text="Previous Step", command=previousStep, fg="black", bg="white" )
previousButton.place(x=200, y=650)
previousButton.configure(state=tk.DISABLED)
nextButton = tk.Button(canvas, text="Next Step", command=nextStep, fg="black", bg="white" )
nextButton.place(x=400, y=650)

#Loading images
puzzle_image = tk.PhotoImage(file=PUZZLE_IMAGE_NAME)
down_arrow_image = tk.PhotoImage(file=DOWN_ARROW_IMAGE_NAME)
up_arrow_image = tk.PhotoImage(file=UP_ARROW_IMAGE_NAME)

#Creating images
canvas.create_image(350, 350, anchor=tk.CENTER, image=puzzle_image)
down_arrow_1 = canvas.create_image(360, 185, image=down_arrow_image)
down_arrow_2 = canvas.create_image(360, 245, image=down_arrow_image)
down_arrow_3 = canvas.create_image(360, 295, image=down_arrow_image)
up_arrow_1 = canvas.create_image(360, 400, image=up_arrow_image)
up_arrow_2 = canvas.create_image(360, 450, image=up_arrow_image)
up_arrow_3 = canvas.create_image(360, 500, image=up_arrow_image)

#Saving arrows
Arrows.append(down_arrow_1)
Arrows.append(down_arrow_2)
Arrows.append(down_arrow_3)
Arrows.append(None)
Arrows.append(up_arrow_1)
Arrows.append(up_arrow_2)
Arrows.append(up_arrow_3)

#Mainloop
root.mainloop()
