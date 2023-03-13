#Imports
import random
from Logic_v1_5 import Turn,Board
import copy

#Random move picker
def randomMove(activeTurn,ActiveBoard):

    algoBoard = copy.deepcopy(ActiveBoard)

    #First Move
    activeTurn.updatePossibleMoves(algoBoard)
    possibleMoves = activeTurn.currentPossibleMoves
    Move1 = random.choice(possibleMoves)
    Move1 = (Move1[0], random.choice(Move1[1]))
    print(Move1) #DEBUG
    roll = activeTurn.fromMoveToRoll(Move1[0],Move1[1],activeTurn.availableRolls,activeTurn.player)
    activeTurn.availableRolls.remove(roll)
    algoBoard.updateWithMove(Move1[0],Move1[1],activeTurn.player)

    activeTurn.updatePossibleMoves(algoBoard)
    possibleMoves = activeTurn.currentPossibleMoves
    Move2 = random.choice(possibleMoves)
    Move2 = (Move2[0], random.choice(Move2[1]))
    roll = activeTurn.fromMoveToRoll(Move2[0],Move2[1],activeTurn.availableRolls,activeTurn.player)
    activeTurn.availableRolls.remove(roll)
    algoBoard.updateWithMove(Move2[0],Move2[1],activeTurn.player)

    if activeTurn.doublesTurn == True:
        activeTurn.updatePossibleMoves(algoBoard)
        possibleMoves = activeTurn.currentPossibleMoves
        Move3 = random.choice(possibleMoves)
        Move3 = (Move3[0], random.choice(Move3[1]))
        roll = activeTurn.fromMoveToRoll(Move3[0],Move3[1],activeTurn.availableRolls,activeTurn.player)
        activeTurn.availableRolls.remove(roll)
        algoBoard.updateWithMove(Move3[0],Move3[1],activeTurn.player)

        activeTurn.updatePossibleMoves(algoBoard)
        possibleMoves = activeTurn.currentPossibleMoves
        Move4 = random.choice(possibleMoves)
        Move4 = (Move4[0], random.choice(Move4[1]))
        roll = activeTurn.fromMoveToRoll(Move4[0],Move4[1],activeTurn.availableRolls,activeTurn.player)
        activeTurn.availableRolls.remove(roll)

        return (Move1,Move2,Move3,Move4)
    else:
        return (Move1,Move2)


#Function to That is called within Main.py
#Convention: Turn and board are passed in, and a tuple of ordered moves are returned. 
def main(activeTurn,activeBoard):
    return randomMove(activeTurn,activeBoard)