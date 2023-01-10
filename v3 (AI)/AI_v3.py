#Imports
import random
from Logic_v3 import Turn,Board

#Random move picker
def randomMove(activeTurn,ActiveBoard):
    activeTurn.updatePossibleMoves(ActiveBoard)
    possibleMoves = activeTurn.currentPossibleMoves



#Function to That is called within Main.py
#Convention: Turn and board are passed in, and a tuple of ordered moves are returned. 
def main(activeTurn,activeBoard):
    pass